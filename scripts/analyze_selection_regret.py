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
        "records": "results/hybrid_api_pilot50_allcand_records.jsonl",
        "oracle": "oracle_upper_bound",
        "methods": [
            "api_direct_first",
            "api_best_of_k_shortest",
            "hybrid_local_mirror_api_eval",
            "hybrid_local_population_api_eval",
        ],
    },
    {
        "label": "perspective_gpt54_full",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "oracle": "oracle_upper_bound",
        "methods": [
            "api_direct_first",
            "api_best_of_k_shortest",
            "hybrid_local_mirror_api_eval",
            "hybrid_local_population_api_eval",
        ],
    },
    {
        "label": "perspective_gpt41_full",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "oracle": "oracle_upper_bound",
        "methods": [
            "api_direct_first",
            "api_best_of_k_shortest",
            "hybrid_local_mirror_api_eval",
            "hybrid_local_population_api_eval",
        ],
    },
    {
        "label": "partial_observability_full",
        "records": "results/partial_observability_api50_records.jsonl",
        "oracle": "oracle_upper_bound",
        "methods": [
            "api_direct_first",
            "api_best_of_k_shortest",
            "hybrid_local_mirror_api_eval",
            "hybrid_local_population_api_eval",
        ],
    },
    {
        "label": "mixed_50_no_coord",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "oracle": "no_coord_oracle",
        "methods": [
            "no_coord_direct_first",
            "no_coord_best_of_k_shortest",
            "no_coord_mirror",
            "no_coord_population",
            "no_coord_consensus_info",
            "no_coord_informative",
        ],
    },
    {
        "label": "perspective_gpt41_no_coord",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "oracle": "no_coord_oracle",
        "methods": [
            "no_coord_direct_first",
            "no_coord_best_of_k_shortest",
            "no_coord_mirror",
            "no_coord_population",
            "no_coord_consensus_info",
            "no_coord_informative",
        ],
    },
    {
        "label": "partial_observability_no_coord",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "oracle": "no_coord_oracle",
        "methods": [
            "no_coord_direct_first",
            "no_coord_best_of_k_shortest",
            "no_coord_mirror",
            "no_coord_population",
            "no_coord_consensus_info",
            "no_coord_informative",
        ],
    },
]

METHOD_LABELS = {
    "api_direct_first": "direct",
    "api_best_of_k_shortest": "shortest",
    "hybrid_local_mirror_api_eval": "mirror",
    "hybrid_local_population_api_eval": "population",
    "no_coord_direct_first": "direct",
    "no_coord_best_of_k_shortest": "shortest",
    "no_coord_mirror": "mirror",
    "no_coord_population": "population",
    "no_coord_consensus_info": "consensus+info",
    "no_coord_informative": "info prior",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="docs/selection_regret_audit.md")
    parser.add_argument("--json-out", default="results/selection_regret_audit.json")
    args = parser.parse_args()

    report = {"runs": [analyze_run(spec) for spec in RUNS]}
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any]) -> dict[str, Any]:
    records = read_jsonl(spec["records"])
    scene_method = scene_method_means(records)
    rows = []
    for method in spec["methods"]:
        rows.append(method_regret(scene_method, method, spec["oracle"]))
    return {
        "label": spec["label"],
        "records": spec["records"],
        "oracle_method": spec["oracle"],
        "rows": rows,
    }


def scene_method_means(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        grouped[str(row["scene_id"])][str(row["method"])].append(float(row["success"]))
    return {
        scene_id: {method: mean(values) for method, values in methods.items()}
        for scene_id, methods in grouped.items()
    }


def method_regret(
    scene_method: dict[str, dict[str, float]],
    method: str,
    oracle_method: str,
    n_boot: int = 5000,
    seed: int = 0,
) -> dict[str, Any]:
    scene_ids = sorted(
        scene_id
        for scene_id, by_method in scene_method.items()
        if method in by_method and oracle_method in by_method
    )
    regrets = [
        scene_method[scene_id][oracle_method] - scene_method[scene_id][method]
        for scene_id in scene_ids
    ]
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        sample = [rng.choice(regrets) for _ in regrets]
        boot.append(mean(sample))
    boot.sort()
    lo = boot[int(0.025 * (len(boot) - 1))]
    hi = boot[int(0.975 * (len(boot) - 1))]
    return {
        "method": method,
        "method_label": METHOD_LABELS[method],
        "n_scenes": len(scene_ids),
        "method_success": mean(scene_method[scene_id][method] for scene_id in scene_ids),
        "oracle_success": mean(scene_method[scene_id][oracle_method] for scene_id in scene_ids),
        "regret": mean(regrets),
        "regret_ci95": [lo, hi],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Selection Regret Audit",
        "",
        "Selection regret is oracle candidate success minus method success, averaged by scene.",
        "It separates candidate-generation failures from selector failures without making new API calls.",
        "",
        "| Run | Method | Scenes | Method success | Oracle | Regret | 95% CI |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        for row in run["rows"]:
            ci = row["regret_ci95"]
            lines.append(
                "| {run} | {method} | {n_scenes} | {method_success:.3f} | {oracle_success:.3f} | {regret:.3f} | [{lo:.3f}, {hi:.3f}] |".format(
                    run=run["label"],
                    method=row["method_label"],
                    n_scenes=row["n_scenes"],
                    method_success=row["method_success"],
                    oracle_success=row["oracle_success"],
                    regret=row["regret"],
                    lo=ci[0],
                    hi=ci[1],
                )
            )
    lines.extend(
        [
            "",
            "Interpretation: full-candidate population-play has zero regret in the paper-facing runs, while mirror self-play leaves nonzero oracle-achievable success on the table. In the no-coordinate ablations, consensus+info sharply reduces but does not always eliminate regret, showing that selector quality remains the bottleneck when explicit coordinate fallbacks are removed.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
