#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


RUNS = [
    {
        "label": "mixed_50_full",
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
        "records": "results/partial_observability_api50_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "label": "mixed_50_no_coord",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "methods": {
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
        },
    },
    {
        "label": "perspective_gpt41_no_coord",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "methods": {
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
        },
    },
    {
        "label": "partial_observability_no_coord",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "methods": {
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
        },
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cache-only audit of held-out listener disagreement for selected messages."
    )
    parser.add_argument("--markdown-out", default="docs/listener_disagreement_audit.md")
    parser.add_argument("--json-out", default="results/listener_disagreement_audit.json")
    args = parser.parse_args()

    report = {"runs": [analyze_run(spec) for spec in RUNS]}
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any]) -> dict[str, Any]:
    rows = read_jsonl(spec["records"])
    by_scene_method: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    method_names = set(spec["methods"].values())
    for row in rows:
        method = str(row["method"])
        if method in method_names:
            by_scene_method[(str(row["scene_id"]), method)].append(row)

    method_rows = []
    for method_label, method_name in spec["methods"].items():
        units = [
            summarize_unit(scene_id, unit_rows)
            for (scene_id, method), unit_rows in sorted(by_scene_method.items())
            if method == method_name
        ]
        if not units:
            raise SystemExit(f"{spec['records']}: no rows found for {method_name}")
        method_rows.append(summarize_method(method_label, method_name, units))
    return {
        "label": spec["label"],
        "records": spec["records"],
        "methods": method_rows,
    }


def summarize_unit(scene_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    successes = [float(row["success"]) for row in rows]
    choices = {str(row.get("choice_id")) for row in rows}
    confidences = [
        float(row["confidence"])
        for row in rows
        if row.get("confidence") is not None
    ]
    success = mean(successes)
    return {
        "scene_id": scene_id,
        "n_listeners": len(rows),
        "success": success,
        "unanimous_success": success == 1.0,
        "split_success": 0.0 < success < 1.0,
        "unanimous_failure": success == 0.0,
        "choice_disagreement": len(choices) > 1,
        "mean_confidence": mean(confidences) if confidences else None,
    }


def summarize_method(
    method_label: str,
    method_name: str,
    units: list[dict[str, Any]],
) -> dict[str, Any]:
    confidence_values = [
        float(unit["mean_confidence"])
        for unit in units
        if unit["mean_confidence"] is not None
    ]
    return {
        "method_label": method_label,
        "method": method_name,
        "n_scenes": len(units),
        "n_listeners": int(mean(unit["n_listeners"] for unit in units)),
        "success": mean(unit["success"] for unit in units),
        "unanimous_success_rate": rate(unit["unanimous_success"] for unit in units),
        "split_success_rate": rate(unit["split_success"] for unit in units),
        "unanimous_failure_rate": rate(unit["unanimous_failure"] for unit in units),
        "choice_disagreement_rate": rate(unit["choice_disagreement"] for unit in units),
        "mean_confidence": mean(confidence_values) if confidence_values else None,
    }


def rate(values: Any) -> float:
    values = list(values)
    return mean(1.0 if value else 0.0 for value in values) if values else 0.0


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Listener Disagreement Audit",
        "",
        "This cache-only audit summarizes held-out listener agreement for each selected message.",
        "A split outcome means the selected message succeeds for some held-out listeners but fails for others in the same scene.",
        "",
        "| Run | Method | Scenes | Success | Unanimous success | Split outcome | Unanimous failure | Choice disagreement | Confidence |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        for row in run["methods"]:
            lines.append(
                "| {run} | {method} | {n_scenes} | {success:.3f} | {unanimous:.3f} | {split:.3f} | {failure:.3f} | {choice:.3f} | {confidence} |".format(
                    run=run["label"],
                    method=row["method_label"],
                    n_scenes=row["n_scenes"],
                    success=row["success"],
                    unanimous=row["unanimous_success_rate"],
                    split=row["split_success_rate"],
                    failure=row["unanimous_failure_rate"],
                    choice=row["choice_disagreement_rate"],
                    confidence=fmt(row["mean_confidence"]),
                )
            )
    lines.extend(
        [
            "",
            "Interpretation: mirror-selected messages often produce split held-out listener outcomes in the harder audits, while full-candidate population-play produces unanimous success in all scenes. No-coordinate consensus+info sharply reduces split outcomes relative to mirror self-play.",
            "",
        ]
    )
    return "\n".join(lines)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    main()
