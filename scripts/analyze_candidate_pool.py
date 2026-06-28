#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


EXACT_COORD_RE = re.compile(
    r"\brow\s+\d+\b|\bcolumn\s+\d+\b|\b\d+(?:st|nd|rd|th)?\s+row\b|\b\d+(?:st|nd|rd|th)?\s+column\b",
    re.IGNORECASE,
)

FULL_RUNS = [
    {
        "label": "mixed_50_full",
        "candidate_eval": "results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl",
        "records": "results/hybrid_api_pilot50_allcand_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "label": "perspective_gpt54_full",
        "candidate_eval": "results/perspective_stress50_hybrid_candidate_eval_records.jsonl",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "label": "perspective_gpt41_full",
        "candidate_eval": "results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "label": "partial_observability_full",
        "candidate_eval": "results/partial_observability_api50_candidate_eval_records.jsonl",
        "records": "results/partial_observability_api50_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
]

NO_COORD_RUNS = [
    {
        "label": "mixed_50_no_coord",
        "candidate_eval": "results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
        },
        "filter_no_exact_coord": True,
    },
    {
        "label": "perspective_gpt41_no_coord",
        "candidate_eval": "results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
        },
        "filter_no_exact_coord": True,
    },
    {
        "label": "partial_observability_no_coord",
        "candidate_eval": "results/partial_observability_api50_candidate_eval_records.jsonl",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
        },
        "filter_no_exact_coord": True,
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cache-only audit of candidate-pool robustness and selector capture."
    )
    parser.add_argument("--markdown-out", default="docs/candidate_pool_audit.md")
    parser.add_argument("--json-out", default="results/candidate_pool_audit.json")
    args = parser.parse_args()

    runs = [analyze_run(spec) for spec in FULL_RUNS + NO_COORD_RUNS]
    report = {"runs": runs}
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any]) -> dict[str, Any]:
    candidate_table = load_candidate_table(
        spec["candidate_eval"],
        filter_no_exact_coord=bool(spec.get("filter_no_exact_coord", False)),
    )
    selected = load_selected_indices(spec["records"], candidate_table, spec["methods"])
    scene_rows = []
    for scene_id, candidates in sorted(candidate_table.items()):
        successes = {idx: candidate["success"] for idx, candidate in candidates.items()}
        max_success = max(successes.values())
        robust_indices = [idx for idx, value in successes.items() if value == 1.0]
        scene_rows.append(
            {
                "scene_id": scene_id,
                "n_candidates": len(candidates),
                "n_robust_candidates": len(robust_indices),
                "has_robust_candidate": bool(robust_indices),
                "oracle_success": max_success,
                "oracle_candidate_indices": [
                    idx for idx, value in successes.items() if value == max_success
                ],
            }
        )

    method_rows = []
    for method_label, method_name in spec["methods"].items():
        method_rows.append(method_summary(method_label, method_name, selected, candidate_table))

    n_scenes = len(scene_rows)
    return {
        "label": spec["label"],
        "candidate_eval": spec["candidate_eval"],
        "records": spec["records"],
        "filter": "no_exact_coordinates" if spec.get("filter_no_exact_coord") else "full",
        "n_scenes": n_scenes,
        "candidate_pool": {
            "mean_candidates": mean(row["n_candidates"] for row in scene_rows),
            "mean_robust_candidates": mean(row["n_robust_candidates"] for row in scene_rows),
            "scenes_with_robust_candidate": sum(row["has_robust_candidate"] for row in scene_rows),
            "robust_candidate_scene_rate": mean(
                1.0 if row["has_robust_candidate"] else 0.0 for row in scene_rows
            ),
            "oracle_success": mean(row["oracle_success"] for row in scene_rows),
        },
        "methods": method_rows,
    }


def load_candidate_table(
    path: str | Path,
    *,
    filter_no_exact_coord: bool,
) -> dict[str, dict[int, dict[str, Any]]]:
    by_candidate: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(path):
        if filter_no_exact_coord and EXACT_COORD_RE.search(str(row["message"])):
            continue
        by_candidate[(str(row["scene_id"]), int(row["candidate_index"]))].append(row)

    by_scene: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    for (scene_id, idx), rows in by_candidate.items():
        successes = [float(row["success"]) for row in rows]
        message = str(rows[0]["message"])
        by_scene[scene_id][idx] = {
            "candidate_index": idx,
            "message": message,
            "tokens": int(rows[0].get("message_tokens") or len(message.split())),
            "success": mean(successes),
            "n_listener_evals": len(rows),
        }
    return dict(by_scene)


def load_selected_indices(
    records_path: str | Path,
    candidate_table: dict[str, dict[int, dict[str, Any]]],
    methods: dict[str, str],
) -> dict[tuple[str, str], int]:
    method_names = set(methods.values())
    selected: dict[tuple[str, str], int] = {}
    for row in read_jsonl(records_path):
        method = str(row["method"])
        if method not in method_names:
            continue
        scene_id = str(row["scene_id"])
        key = (scene_id, method)
        if key in selected:
            continue
        if "source_candidate_index" in row:
            selected[key] = int(row["source_candidate_index"])
        elif "candidate_index" in row and method.startswith("no_coord_"):
            selected[key] = int(row["candidate_index"])
        else:
            selected[key] = message_to_index(scene_id, str(row["message"]), candidate_table)
    return selected


def message_to_index(
    scene_id: str,
    message: str,
    candidate_table: dict[str, dict[int, dict[str, Any]]],
) -> int:
    candidates = candidate_table[scene_id]
    for idx, row in candidates.items():
        if normalize(row["message"]) == normalize(message):
            return idx
    raise SystemExit(f"Could not map selected message for {scene_id!r}: {message!r}")


def method_summary(
    method_label: str,
    method_name: str,
    selected: dict[tuple[str, str], int],
    candidate_table: dict[str, dict[int, dict[str, Any]]],
) -> dict[str, Any]:
    rows = []
    for scene_id, candidates in sorted(candidate_table.items()):
        key = (scene_id, method_name)
        if key not in selected:
            raise SystemExit(f"Missing selected candidate for {scene_id} / {method_name}")
        idx = selected[key]
        if idx not in candidates:
            raise SystemExit(f"Selected candidate {idx} for {scene_id} / {method_name} is outside the audited pool")
        selected_success = candidates[idx]["success"]
        max_success = max(candidate["success"] for candidate in candidates.values())
        rows.append(
            {
                "scene_id": scene_id,
                "selected_candidate_index": idx,
                "selected_success": selected_success,
                "selected_is_robust": selected_success == 1.0,
                "selected_matches_oracle": selected_success == max_success,
            }
        )
    return {
        "method_label": method_label,
        "method": method_name,
        "selected_success": mean(row["selected_success"] for row in rows),
        "selected_robust_rate": mean(1.0 if row["selected_is_robust"] else 0.0 for row in rows),
        "oracle_match_rate": mean(1.0 if row["selected_matches_oracle"] else 0.0 for row in rows),
    }


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Candidate Pool Robustness Audit",
        "",
        "This cache-only audit asks whether robust held-out candidates were available and whether each selector chose one.",
        "A robust candidate succeeds with every held-out API listener for that scene.",
        "",
        "## Candidate Availability",
        "",
        "| Run | Filter | Scenes | Candidates/scene | Robust candidates/scene | Scenes with robust candidate | Oracle success |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        pool = run["candidate_pool"]
        lines.append(
            "| {label} | {filter} | {n_scenes} | {cands:.2f} | {robust:.2f} | {scene_rate:.3f} | {oracle:.3f} |".format(
                label=run["label"],
                filter=run["filter"],
                n_scenes=run["n_scenes"],
                cands=pool["mean_candidates"],
                robust=pool["mean_robust_candidates"],
                scene_rate=pool["robust_candidate_scene_rate"],
                oracle=pool["oracle_success"],
            )
        )

    lines.extend(
        [
            "",
            "## Selector Capture",
            "",
            "| Run | Method | Selected success | Selected robust rate | Oracle-match rate |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for run in report["runs"]:
        for row in run["methods"]:
            lines.append(
                "| {label} | {method} | {success:.3f} | {robust:.3f} | {oracle_match:.3f} |".format(
                    label=run["label"],
                    method=row["method_label"],
                    success=row["selected_success"],
                    robust=row["selected_robust_rate"],
                    oracle_match=row["oracle_match_rate"],
                )
            )

    lines.extend(
        [
            "",
            "Interpretation: the full-candidate runs usually contain all-listener-robust messages, and population-play consistently selects them. After exact-coordinate candidates are removed, robust non-coordinate candidates become less available in the alternate-model perspective audit, but consensus+info captures most of the remaining oracle success.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
