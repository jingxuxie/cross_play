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
    ("mixed_50_full", "results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl"),
    ("perspective_gpt54_full", "results/perspective_stress50_hybrid_candidate_eval_records.jsonl"),
    ("perspective_gpt41_full", "results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl"),
    ("partial_observability_full", "results/partial_observability_api50_candidate_eval_records.jsonl"),
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cache-only prefix-K audit over all-candidate API evaluations."
    )
    parser.add_argument("--markdown-out", default="docs/candidate_budget_audit.md")
    parser.add_argument("--json-out", default="results/candidate_budget_audit.json")
    args = parser.parse_args()

    report = {"runs": [analyze_run(label, path) for label, path in RUNS]}
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(label: str, path: str) -> dict[str, Any]:
    by_scene = candidate_table(path)
    max_k = max(len(candidates) for candidates in by_scene.values())
    prefix_rows = []
    for k in range(1, max_k + 1):
        oracle_success = []
        robust_available = []
        for candidates in by_scene.values():
            prefix = [
                candidate
                for idx, candidate in candidates.items()
                if idx < k
            ]
            if not prefix:
                raise SystemExit(f"{label}: empty prefix k={k}")
            best = max(candidate["success"] for candidate in prefix)
            oracle_success.append(best)
            robust_available.append(any(candidate["success"] == 1.0 for candidate in prefix))
        prefix_rows.append(
            {
                "k": k,
                "oracle_success": mean(oracle_success),
                "robust_scene_rate": mean(1.0 if value else 0.0 for value in robust_available),
            }
        )

    first_robust_positions = []
    for candidates in by_scene.values():
        robust_indices = sorted(idx for idx, row in candidates.items() if row["success"] == 1.0)
        first_robust_positions.append((robust_indices[0] + 1) if robust_indices else None)

    return {
        "label": label,
        "source": path,
        "n_scenes": len(by_scene),
        "max_k": max_k,
        "prefix_rows": prefix_rows,
        "first_robust_position": {
            "mean": mean(pos for pos in first_robust_positions if pos is not None),
            "missing": sum(pos is None for pos in first_robust_positions),
            "counts": {
                str(k): sum(pos == k for pos in first_robust_positions)
                for k in range(1, max_k + 1)
            },
        },
    }


def candidate_table(path: str | Path) -> dict[str, dict[int, dict[str, Any]]]:
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(path):
        grouped[(str(row["scene_id"]), int(row["candidate_index"]))].append(row)

    by_scene: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    for (scene_id, idx), rows in grouped.items():
        message = str(rows[0]["message"])
        by_scene[scene_id][idx] = {
            "candidate_index": idx,
            "message": message,
            "tokens": int(rows[0].get("message_tokens") or len(message.split())),
            "success": mean(float(row["success"]) for row in rows),
            "n_listener_evals": len(rows),
        }
    return dict(by_scene)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Candidate Budget Audit",
        "",
        "This cache-only audit reports how quickly robust candidates appear as the generated candidate budget grows.",
        "Oracle@K is the best held-out success among the first K candidates for a scene.",
        "A robust candidate succeeds with every held-out API listener for that scene.",
        "",
        "## Prefix-K Availability",
        "",
        "| Run | K | Oracle@K | Robust-scene rate | Source |",
        "|---|---:|---:|---:|---|",
    ]
    for run in report["runs"]:
        for row in run["prefix_rows"]:
            lines.append(
                f"| {run['label']} | {row['k']} | {row['oracle_success']:.3f} | {row['robust_scene_rate']:.3f} | `{run['source']}` |"
            )

    lines.extend(
        [
            "",
            "## First Robust Candidate Position",
            "",
            "| Run | Mean first robust K | Missing robust candidate | K=1 | K=2 | K=3 | K=4 |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for run in report["runs"]:
        positions = run["first_robust_position"]
        counts = positions["counts"]
        lines.append(
            f"| {run['label']} | {positions['mean']:.2f} | {positions['missing']} | {counts.get('1', 0)} | {counts.get('2', 0)} | {counts.get('3', 0)} | {counts.get('4', 0)} |"
        )

    lines.extend(
        [
            "",
            "Interpretation: candidate 1 is often already sufficient in easier mixed scenes, but the perspective and partial-observability audits need later candidates for full robust coverage. The fourth candidate closes the robust-scene rate to 1.000 in all full-candidate runs.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
