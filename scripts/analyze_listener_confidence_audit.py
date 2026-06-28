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


HIGH_CONFIDENCE_THRESHOLD = 0.8

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
        description="Cache-only audit of held-out listener confidence and overconfident failures."
    )
    parser.add_argument("--markdown-out", default="docs/listener_confidence_audit.md")
    parser.add_argument("--json-out", default="results/listener_confidence_audit.json")
    parser.add_argument("--threshold", type=float, default=HIGH_CONFIDENCE_THRESHOLD)
    args = parser.parse_args()

    report = {
        "high_confidence_threshold": args.threshold,
        "runs": [analyze_run(spec, threshold=args.threshold) for spec in RUNS],
    }
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any], *, threshold: float) -> dict[str, Any]:
    rows = read_jsonl(spec["records"])
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    method_names = set(spec["methods"].values())
    for row in rows:
        method = str(row["method"])
        if method in method_names:
            by_method[method].append(row)

    method_rows = []
    for method_label, method_name in spec["methods"].items():
        method_rows.append(
            summarize_method(
                method_label,
                method_name,
                by_method.get(method_name, []),
                threshold=threshold,
                source=spec["records"],
            )
        )
    return {
        "label": spec["label"],
        "records": spec["records"],
        "methods": method_rows,
    }


def summarize_method(
    method_label: str,
    method_name: str,
    rows: list[dict[str, Any]],
    *,
    threshold: float,
    source: str,
) -> dict[str, Any]:
    if not rows:
        raise SystemExit(f"{source}: no rows found for {method_name}")

    confidences = [float(row.get("confidence") or 0.0) for row in rows]
    successes = [float(row["success"]) for row in rows]
    ambiguity = [1.0 if bool(row.get("ambiguity")) else 0.0 for row in rows]
    success_confidences = [
        float(row.get("confidence") or 0.0)
        for row in rows
        if int(row["success"]) == 1
    ]
    failure_confidences = [
        float(row.get("confidence") or 0.0)
        for row in rows
        if int(row["success"]) == 0
    ]
    high_confidence_failures = [
        row
        for row in rows
        if int(row["success"]) == 0 and float(row.get("confidence") or 0.0) >= threshold
    ]

    by_scene: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_scene[str(row["scene_id"])].append(row)
    scene_high_confidence_failures = [
        any(
            int(row["success"]) == 0 and float(row.get("confidence") or 0.0) >= threshold
            for row in scene_rows
        )
        for scene_rows in by_scene.values()
    ]

    failure_count = len(failure_confidences)
    return {
        "method_label": method_label,
        "method": method_name,
        "n_scenes": len(by_scene),
        "n_rows": len(rows),
        "success": mean(successes),
        "mean_confidence": mean(confidences),
        "ambiguity_rate": mean(ambiguity),
        "mean_success_confidence": mean(success_confidences) if success_confidences else None,
        "mean_failure_confidence": mean(failure_confidences) if failure_confidences else None,
        "high_confidence_failure_rate": len(high_confidence_failures) / len(rows),
        "failure_high_confidence_rate": len(high_confidence_failures) / failure_count if failure_count else 0.0,
        "scene_high_confidence_failure_rate": rate(scene_high_confidence_failures),
    }


def rate(values: Any) -> float:
    values = list(values)
    return mean(1.0 if value else 0.0 for value in values) if values else 0.0


def render_markdown(report: dict[str, Any]) -> str:
    threshold = float(report["high_confidence_threshold"])
    lines = [
        "# Listener Confidence Audit",
        "",
        "This cache-only audit checks whether held-out listener self-reported confidence and ambiguity flags explain selected-message failures.",
        f"A high-confidence failure is a listener row with `success=0` and confidence at least `{threshold:.1f}`.",
        "",
        "| Run | Method | Rows | Success | Confidence | Ambiguity | Failure confidence | High-conf failure rows | High-conf failure scenes |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        for row in run["methods"]:
            lines.append(
                "| {run} | {method} | {rows} | {success:.3f} | {confidence:.3f} | {ambiguity:.3f} | {fail_conf} | {high_rows:.3f} | {high_scenes:.3f} |".format(
                    run=run["label"],
                    method=row["method_label"],
                    rows=row["n_rows"],
                    success=row["success"],
                    confidence=row["mean_confidence"],
                    ambiguity=row["ambiguity_rate"],
                    fail_conf=fmt(row["mean_failure_confidence"]),
                    high_rows=row["high_confidence_failure_rate"],
                    high_scenes=row["scene_high_confidence_failure_rate"],
                )
            )

    lines.extend(
        [
            "",
            "Interpretation: listener self-reports are not a substitute for cross-play evaluation. In the alternate-model perspective runs, ambiguity flags are `0.000`, yet mirror self-play still produces high-confidence failures in `0.147` of full-candidate listener rows and `0.280` of no-coordinate listener rows. Full-candidate population-play has no held-out failures in these caches, so its high-confidence failure rate is `0.000`; in the no-coordinate perspective audit, consensus+info reduces but does not eliminate overconfident failures.",
            "",
        ]
    )
    return "\n".join(lines)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    main()
