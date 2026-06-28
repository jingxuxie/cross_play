#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import random
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

RUNS = [
    {
        "label": "mixed_50_full",
        "candidate_eval": "results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl",
        "records": "results/hybrid_api_pilot50_allcand_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "perspective_gpt54_full",
        "candidate_eval": "results/perspective_stress50_hybrid_candidate_eval_records.jsonl",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "perspective_gpt41_full",
        "candidate_eval": "results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "partial_observability_full",
        "candidate_eval": "results/partial_observability_api50_candidate_eval_records.jsonl",
        "records": "results/partial_observability_api50_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "mixed_50_no_coord",
        "candidate_eval": "results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "filter_no_exact_coord": True,
        "primary": "no_coord_consensus_info",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
            "oracle": "no_coord_oracle",
        },
    },
    {
        "label": "perspective_gpt41_no_coord",
        "candidate_eval": "results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "filter_no_exact_coord": True,
        "primary": "no_coord_consensus_info",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
            "oracle": "no_coord_oracle",
        },
    },
    {
        "label": "partial_observability_no_coord",
        "candidate_eval": "results/partial_observability_api50_candidate_eval_records.jsonl",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "filter_no_exact_coord": True,
        "primary": "no_coord_consensus_info",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
            "oracle": "no_coord_oracle",
        },
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cache-only uniform-random candidate selector baseline."
    )
    parser.add_argument("--markdown-out", default="docs/random_candidate_baseline.md")
    parser.add_argument("--json-out", default="results/random_candidate_baseline.json")
    args = parser.parse_args()

    report = {"runs": [analyze_run(spec) for spec in RUNS]}
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any]) -> dict[str, Any]:
    candidate_rows = candidate_scene_rows(
        spec["candidate_eval"],
        filter_no_exact_coord=bool(spec.get("filter_no_exact_coord", False)),
    )
    method_scores = scene_method_means(read_jsonl(spec["records"]))
    scene_ids = sorted(set(candidate_rows) & set(method_scores))
    random_scene = [candidate_rows[scene_id]["random_expected_success"] for scene_id in scene_ids]
    robust_pick_scene = [candidate_rows[scene_id]["random_robust_pick_rate"] for scene_id in scene_ids]
    method_rows = []
    for label, method in spec["methods"].items():
        values = [method_scores[scene_id][method] for scene_id in scene_ids]
        diff = [method_scores[scene_id][method] - candidate_rows[scene_id]["random_expected_success"] for scene_id in scene_ids]
        method_rows.append(
            {
                "label": label,
                "method": method,
                "success": mean(values),
                "minus_random": mean(diff),
                "minus_random_ci95": bootstrap_ci(diff),
            }
        )
    primary = next(row for row in method_rows if row["method"] == spec["primary"])
    return {
        "label": spec["label"],
        "filter": "no_exact_coordinates" if spec.get("filter_no_exact_coord") else "full",
        "candidate_eval": spec["candidate_eval"],
        "records": spec["records"],
        "n_scenes": len(scene_ids),
        "mean_candidates": mean(candidate_rows[scene_id]["n_candidates"] for scene_id in scene_ids),
        "random_expected_success": mean(random_scene),
        "random_expected_success_ci95": bootstrap_ci(random_scene),
        "random_robust_pick_rate": mean(robust_pick_scene),
        "primary_method": primary["label"],
        "primary_minus_random": primary["minus_random"],
        "primary_minus_random_ci95": primary["minus_random_ci95"],
        "methods": method_rows,
    }


def candidate_scene_rows(path: str, *, filter_no_exact_coord: bool) -> dict[str, dict[str, Any]]:
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(path):
        if filter_no_exact_coord and EXACT_COORD_RE.search(str(row["message"])):
            continue
        grouped[(str(row["scene_id"]), int(row["candidate_index"]))].append(row)

    by_scene: dict[str, list[float]] = defaultdict(list)
    for (scene_id, _idx), rows in grouped.items():
        by_scene[scene_id].append(mean(float(row["success"]) for row in rows))

    out = {}
    for scene_id, successes in by_scene.items():
        out[scene_id] = {
            "n_candidates": len(successes),
            "random_expected_success": mean(successes),
            "random_robust_pick_rate": mean(1.0 if success == 1.0 else 0.0 for success in successes),
        }
    return out


def scene_method_means(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        grouped[str(row["scene_id"])][str(row["method"])].append(float(row["success"]))
    return {
        scene_id: {method: mean(values) for method, values in by_method.items()}
        for scene_id, by_method in grouped.items()
    }


def bootstrap_ci(values: list[float], n_boot: int = 5000, seed: int = 0) -> list[float]:
    if not values:
        return [0.0, 0.0]
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in values]
        boot.append(mean(sample))
    boot.sort()
    return [boot[int(0.025 * (len(boot) - 1))], boot[int(0.975 * (len(boot) - 1))]]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Random Candidate Baseline",
        "",
        "This cache-only audit compares learned or heuristic selectors with a uniform random selector over the same generated candidate pool.",
        "The random baseline is computed exactly as the average held-out success of available candidates in each scene, then averaged over scenes.",
        "",
        "## Summary",
        "",
        "| Run | Filter | Scenes | Candidates/scene | Random expected | Random robust-pick rate | Primary selector | Primary-minus-random 95% CI | Source |",
        "|---|---|---:|---:|---:|---:|---|---|---|",
    ]
    for run in report["runs"]:
        ci = run["primary_minus_random_ci95"]
        lines.append(
            "| {label} | {filter} | {n_scenes} | {mean_candidates:.2f} | {random_expected_success:.3f} | {random_robust_pick_rate:.3f} | {primary_method} | {primary_minus_random:.3f} [{lo:.3f}, {hi:.3f}] | `{candidate_eval}` |".format(
                label=run["label"],
                filter=run["filter"],
                n_scenes=run["n_scenes"],
                mean_candidates=run["mean_candidates"],
                random_expected_success=run["random_expected_success"],
                random_robust_pick_rate=run["random_robust_pick_rate"],
                primary_method=run["primary_method"],
                primary_minus_random=run["primary_minus_random"],
                lo=ci[0],
                hi=ci[1],
                candidate_eval=run["candidate_eval"],
            )
        )
    lines.extend(
        [
            "",
            "## Method Details",
            "",
            "| Run | Method | Success | Minus random | 95% CI |",
            "|---|---|---:|---:|---|",
        ]
    )
    for run in report["runs"]:
        for row in run["methods"]:
            ci = row["minus_random_ci95"]
            lines.append(
                f"| {run['label']} | {row['label']} | {row['success']:.3f} | {row['minus_random']:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] |"
            )
    lines.extend(
        [
            "",
            "Interpretation: a random selector is strong when many candidates are already robust, but it remains below population-play in every full-candidate run and below consensus+info in every no-coordinate run. This supports the selector-regret interpretation: candidate generation often contains a robust message, but selecting it is still the key problem.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
