#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import random
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
        "filter": "full",
        "records": "results/hybrid_api_pilot50_allcand_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "mirror": "hybrid_local_mirror_api_eval",
        "methods": {
            "template": "template",
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "perspective_gpt54_full",
        "filter": "full",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "mirror": "hybrid_local_mirror_api_eval",
        "methods": {
            "template": "template",
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "perspective_gpt41_full",
        "filter": "full",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "mirror": "hybrid_local_mirror_api_eval",
        "methods": {
            "template": "template",
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "partial_observability_full",
        "filter": "full",
        "records": "results/partial_observability_api50_records.jsonl",
        "primary": "hybrid_local_population_api_eval",
        "mirror": "hybrid_local_mirror_api_eval",
        "methods": {
            "template": "template",
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "mixed_50_no_coord",
        "filter": "no_exact_coordinates",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "primary": "no_coord_consensus_info",
        "mirror": "no_coord_mirror",
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
        "filter": "no_exact_coordinates",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "primary": "no_coord_consensus_info",
        "mirror": "no_coord_mirror",
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
        "filter": "no_exact_coordinates",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "primary": "no_coord_consensus_info",
        "mirror": "no_coord_mirror",
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
        description="Cache-only audit of selected-message length and success efficiency."
    )
    parser.add_argument("--markdown-out", default="docs/message_length_audit.md")
    parser.add_argument("--json-out", default="results/message_length_audit.json")
    args = parser.parse_args()

    report = {"runs": [analyze_run(spec) for spec in RUNS]}
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any]) -> dict[str, Any]:
    records = read_jsonl(spec["records"])
    scene_method = scene_method_units(records)
    rows = []
    for method_label, method_name in spec["methods"].items():
        units = [
            by_method[method_name]
            for by_method in scene_method.values()
            if method_name in by_method
        ]
        if not units:
            raise SystemExit(f"{spec['records']}: no rows found for {method_name}")
        rows.append(summarize_method(method_label, method_name, units))
    pair = paired_primary_vs_mirror(scene_method, spec["primary"], spec["mirror"])
    primary_label = label_for_method(spec["methods"], spec["primary"])
    mirror_label = label_for_method(spec["methods"], spec["mirror"])
    return {
        "label": spec["label"],
        "filter": spec["filter"],
        "records": spec["records"],
        "primary_method": primary_label,
        "mirror_method": mirror_label,
        "methods": rows,
        "primary_vs_mirror": pair,
    }


def scene_method_units(records: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        grouped[str(row["scene_id"])][str(row["method"])].append(row)
    units: dict[str, dict[str, dict[str, Any]]] = {}
    for scene_id, by_method in grouped.items():
        units[scene_id] = {}
        for method, rows in by_method.items():
            messages = {str(row["message"]) for row in rows}
            tokens = [float(row["message_tokens"]) for row in rows]
            units[scene_id][method] = {
                "scene_id": scene_id,
                "method": method,
                "success": mean(float(row["success"]) for row in rows),
                "message_tokens": mean(tokens),
                "n_distinct_messages": len(messages),
            }
    return units


def summarize_method(
    method_label: str,
    method_name: str,
    units: list[dict[str, Any]],
) -> dict[str, Any]:
    success = mean(unit["success"] for unit in units)
    mean_tokens = mean(unit["message_tokens"] for unit in units)
    return {
        "method_label": method_label,
        "method": method_name,
        "n_scenes": len(units),
        "success": success,
        "mean_tokens": mean_tokens,
        "success_per_token": success / mean_tokens if mean_tokens else 0.0,
        "messages_per_scene": mean(unit["n_distinct_messages"] for unit in units),
    }


def paired_primary_vs_mirror(
    scene_method: dict[str, dict[str, dict[str, Any]]],
    primary_method: str,
    mirror_method: str,
) -> dict[str, Any]:
    scene_ids = sorted(
        scene_id
        for scene_id, by_method in scene_method.items()
        if primary_method in by_method and mirror_method in by_method
    )
    success_diffs = [
        scene_method[scene_id][primary_method]["success"]
        - scene_method[scene_id][mirror_method]["success"]
        for scene_id in scene_ids
    ]
    token_diffs = [
        scene_method[scene_id][primary_method]["message_tokens"]
        - scene_method[scene_id][mirror_method]["message_tokens"]
        for scene_id in scene_ids
    ]
    return {
        "n_scenes": len(scene_ids),
        "success_delta": mean(success_diffs),
        "success_delta_ci95": bootstrap_ci(success_diffs),
        "token_delta": mean(token_diffs),
        "token_delta_ci95": bootstrap_ci(token_diffs),
        "tokens_per_success_point": (
            mean(token_diffs) / mean(success_diffs) if mean(success_diffs) else None
        ),
    }


def bootstrap_ci(values: list[float], n_boot: int = 5000, seed: int = 0) -> list[float]:
    if not values:
        return [0.0, 0.0]
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        boot.append(mean(rng.choice(values) for _ in values))
    boot.sort()
    return [boot[int(0.025 * (len(boot) - 1))], boot[int(0.975 * (len(boot) - 1))]]


def label_for_method(methods: dict[str, str], method_name: str) -> str:
    for label, name in methods.items():
        if name == method_name:
            return label
    return method_name


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Message Length Audit",
        "",
        "This cache-only audit checks whether selector gains are explained by simply choosing longer messages.",
        "Length is measured with the stored whitespace token count used in the experiment records.",
        "",
        "## Method Lengths",
        "",
        "| Run | Filter | Method | Scenes | Success | Mean tokens | Success/token |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        for row in run["methods"]:
            lines.append(
                "| {run} | {filter} | {method} | {n_scenes} | {success:.3f} | {tokens:.2f} | {eff:.3f} |".format(
                    run=run["label"],
                    filter=run["filter"],
                    method=row["method_label"],
                    n_scenes=row["n_scenes"],
                    success=row["success"],
                    tokens=row["mean_tokens"],
                    eff=row["success_per_token"],
                )
            )

    lines.extend(
        [
            "",
            "## Primary Selector Versus Mirror",
            "",
            "| Run | Primary | Scenes | Success delta | Success delta 95% CI | Token delta | Token delta 95% CI |",
            "|---|---|---:|---:|---|---:|---|",
        ]
    )
    for run in report["runs"]:
        pair = run["primary_vs_mirror"]
        lines.append(
            "| {run} | {primary} | {n_scenes} | {success:.3f} | [{slo:.3f}, {shi:.3f}] | {tokens:.2f} | [{tlo:.2f}, {thi:.2f}] |".format(
                run=run["label"],
                primary=run["primary_method"],
                n_scenes=pair["n_scenes"],
                success=pair["success_delta"],
                slo=pair["success_delta_ci95"][0],
                shi=pair["success_delta_ci95"][1],
                tokens=pair["token_delta"],
                tlo=pair["token_delta_ci95"][0],
                thi=pair["token_delta_ci95"][1],
            )
        )

    lines.extend(
        [
            "",
            "Interpretation: population-play and consensus+info often select longer messages than mirror self-play, but length alone does not explain the gains. Direct messages are longer than mirror in the perspective and partial-observability full-candidate runs while remaining less successful, and full-candidate population messages stay at or below the 10-token template scale in all but the main perspective-stress run.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
