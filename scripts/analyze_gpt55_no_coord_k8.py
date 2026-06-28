#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


EXACT_COORD_RE = re.compile(
    r"\brow\s+\d+\b|"
    r"\bcolumn\s+\d+\b|"
    r"\b\d+(?:st|nd|rd|th)?\s+row\b|"
    r"\b\d+(?:st|nd|rd|th)?\s+column\b|"
    r"\b(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+(?:row|column)\b",
    re.IGNORECASE,
)

METHODS = [
    "no_coord_direct_first",
    "no_coord_best_of_k_shortest",
    "no_coord_mirror",
    "no_coord_population",
    "no_coord_consensus_info",
    "no_coord_informative",
    "no_coord_oracle",
]

METHOD_LABELS = {
    "no_coord_direct_first": "Direct first",
    "no_coord_best_of_k_shortest": "Shortest",
    "no_coord_mirror": "Mirror",
    "no_coord_population": "Population",
    "no_coord_consensus_info": "Consensus+info",
    "no_coord_informative": "Info prior",
    "no_coord_oracle": "Oracle",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare GPT-5.5 K=4 and K=8 no-coordinate speaker artifacts."
    )
    parser.add_argument(
        "--k4-summary",
        default="results/gpt55_speaker_perspective50_no_coord_summary.json",
    )
    parser.add_argument(
        "--k4-candidates",
        default="results/gpt55_speaker_perspective50_candidates.jsonl",
    )
    parser.add_argument(
        "--k4-candidate-records",
        default="results/gpt55_speaker_perspective50_candidate_eval_records.jsonl",
    )
    parser.add_argument(
        "--k8-summary",
        default="results/gpt55_no_coord_k8_perspective50_no_coord_summary.json",
    )
    parser.add_argument(
        "--k8-candidates",
        default="results/gpt55_no_coord_k8_perspective50_candidates.jsonl",
    )
    parser.add_argument(
        "--k8-candidate-records",
        default="results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl",
    )
    parser.add_argument("--json-out", default="results/gpt55_no_coord_k8_comparison.json")
    parser.add_argument("--markdown-out", default="docs/gpt55_no_coord_k8_report.md")
    args = parser.parse_args()

    report = build_report(args)
    write_json(args.json_out, report)
    write_text(args.markdown_out, render_markdown(report))
    print(render_markdown(report))


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    k4 = analyze_condition(
        label="gpt55_k4_filtered",
        summary_path=args.k4_summary,
        candidates_path=args.k4_candidates,
        candidate_records_path=args.k4_candidate_records,
        prefix_k=4,
    )
    k8 = analyze_condition(
        label="gpt55_k8_no_coordinate_prompt",
        summary_path=args.k8_summary,
        candidates_path=args.k8_candidates,
        candidate_records_path=args.k8_candidate_records,
        prefix_k=8,
    )
    return {
        "description": (
            "GPT-5.5 no-coordinate candidate generation comparison for Experiment 4. "
            "K=4 filters the standard GPT-5.5 speaker candidates; K=8 uses the dedicated "
            "no-coordinate prompt and GPT-5.5 held-out listeners."
        ),
        "conditions": [k4, k8],
        "method_deltas": method_deltas(k4, k8),
        "key_observations": key_observations(k4, k8),
        "claim_boundary": [
            "Safe: GPT-5.5 can generate robust non-coordinate referring expressions on all 50 perspective-stress scenes.",
            "Safe: increasing to K=8 improves population and mirror selection, but the heuristic consensus+info selector is not monotonic.",
            "Do not claim: consensus+info is the best no-coordinate selector for GPT-5.5 K=8; shortest and population are stronger in this run.",
        ],
    }


def analyze_condition(
    *,
    label: str,
    summary_path: str,
    candidates_path: str,
    candidate_records_path: str,
    prefix_k: int,
) -> dict[str, Any]:
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    candidate_rows = read_jsonl(candidates_path)
    candidate_records = read_jsonl(candidate_records_path)
    return {
        "label": label,
        "summary_path": summary_path,
        "candidates_path": candidates_path,
        "candidate_records_path": candidate_records_path,
        "prefix_k": prefix_k,
        "n_scenes": summary["overall"]["n_scenes"],
        "candidate_filter": summary.get("candidate_filter", {}),
        "coordinate_audit": coordinate_audit(candidate_rows),
        "method_rows": method_rows(summary),
        "candidate_budget": candidate_budget(candidate_records, candidate_rows, prefix_k),
    }


def coordinate_audit(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    violations = []
    candidate_counts = []
    for row in candidate_rows:
        candidates = [str(message) for message in row["candidates"]]
        candidate_counts.append(len(candidates))
        for index, message in enumerate(candidates):
            if EXACT_COORD_RE.search(message):
                violations.append(
                    {
                        "scene_id": row["scene_id"],
                        "candidate_index": index,
                        "message": message,
                    }
                )
    return {
        "n_scenes": len(candidate_rows),
        "candidate_count_histogram": dict(sorted(Counter(candidate_counts).items())),
        "coordinate_violation_count": len(violations),
        "coordinate_violation_by_index": dict(
            sorted(Counter(row["candidate_index"] for row in violations).items())
        ),
        "examples": violations[:5],
    }


def method_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for method in METHODS:
        stats = summary["by_method"][method]
        rows.append(
            {
                "method": method,
                "label": METHOD_LABELS[method],
                "success": stats["success"],
                "success_ci95": stats["success_ci95"],
                "sameplay_success": stats.get("sameplay_success"),
                "crossplay_gap": stats.get("crossplay_gap"),
                "mean_tokens": stats["mean_tokens"],
            }
        )
    return rows


def candidate_budget(
    records: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    max_k: int,
) -> list[dict[str, Any]]:
    allowed: dict[str, set[int]] = {}
    for row in candidate_rows:
        allowed[str(row["scene_id"])] = {
            index
            for index, message in enumerate(row["candidates"])
            if not EXACT_COORD_RE.search(str(message))
        }

    by_scene_index: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        by_scene_index[str(row["scene_id"])][int(row["candidate_index"])].append(float(row["success"]))

    rows = []
    for k in sorted({1, 2, 4, max_k}):
        candidate_counts = []
        robust_counts = []
        robust_scene_flags = []
        oracle_successes = []
        for scene_id, by_index in by_scene_index.items():
            candidate_means = [
                mean(values)
                for index, values in sorted(by_index.items())
                if index < k and index in allowed[scene_id]
            ]
            if not candidate_means:
                continue
            candidate_counts.append(len(candidate_means))
            robust_counts.append(sum(1 for value in candidate_means if value == 1.0))
            robust_scene_flags.append(any(value == 1.0 for value in candidate_means))
            oracle_successes.append(max(candidate_means))
        rows.append(
            {
                "k": k,
                "mean_candidates": mean(candidate_counts),
                "mean_robust_candidates": mean(robust_counts),
                "robust_scene_rate": mean(1.0 if flag else 0.0 for flag in robust_scene_flags),
                "oracle_success": mean(oracle_successes),
            }
        )
    return rows


def method_deltas(k4: dict[str, Any], k8: dict[str, Any]) -> list[dict[str, Any]]:
    k4_by_method = {row["method"]: row for row in k4["method_rows"]}
    k8_by_method = {row["method"]: row for row in k8["method_rows"]}
    return [
        {
            "method": method,
            "label": METHOD_LABELS[method],
            "k4_success": k4_by_method[method]["success"],
            "k8_success": k8_by_method[method]["success"],
            "delta": k8_by_method[method]["success"] - k4_by_method[method]["success"],
        }
        for method in METHODS
    ]


def key_observations(k4: dict[str, Any], k8: dict[str, Any]) -> dict[str, Any]:
    k4_methods = {row["method"]: row for row in k4["method_rows"]}
    k8_methods = {row["method"]: row for row in k8["method_rows"]}
    return {
        "k4_kept_candidates": k4["candidate_filter"]["kept_candidates"],
        "k4_excluded_candidates": k4["candidate_filter"]["excluded_candidates"],
        "k8_kept_candidates": k8["candidate_filter"]["kept_candidates"],
        "k8_excluded_candidates": k8["candidate_filter"]["excluded_candidates"],
        "k4_coordinate_violations": k4["coordinate_audit"]["coordinate_violation_count"],
        "k8_coordinate_violations": k8["coordinate_audit"]["coordinate_violation_count"],
        "k4_oracle": k4_methods["no_coord_oracle"]["success"],
        "k8_oracle": k8_methods["no_coord_oracle"]["success"],
        "k4_population": k4_methods["no_coord_population"]["success"],
        "k8_population": k8_methods["no_coord_population"]["success"],
        "k4_consensus_info": k4_methods["no_coord_consensus_info"]["success"],
        "k8_consensus_info": k8_methods["no_coord_consensus_info"]["success"],
        "k8_shortest": k8_methods["no_coord_best_of_k_shortest"]["success"],
        "k8_direct_first": k8_methods["no_coord_direct_first"]["success"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    obs = report["key_observations"]
    lines = [
        "# GPT-5.5 K=8 No-Coordinate Audit",
        "",
        report["description"],
        "",
        "## Key Observations",
        "",
        f"- K=4 filtered baseline keeps {obs['k4_kept_candidates']} candidates and excludes {obs['k4_excluded_candidates']} coordinate candidates; K=8 keeps {obs['k8_kept_candidates']} and excludes {obs['k8_excluded_candidates']}.",
        f"- The dedicated K=8 no-coordinate prompt produced {obs['k8_coordinate_violations']} exact-coordinate candidates across 50 scenes.",
        f"- Oracle success is {fmt(obs['k4_oracle'])} at K=4 and {fmt(obs['k8_oracle'])} at K=8, so the hard limitation is not lack of any non-coordinate expression.",
        f"- K=8 population-play improves from {fmt(obs['k4_population'])} to {fmt(obs['k8_population'])}; shortest reaches {fmt(obs['k8_shortest'])}.",
        f"- Consensus+info falls from {fmt(obs['k4_consensus_info'])} to {fmt(obs['k8_consensus_info'])}, showing that the informativeness heuristic can over-select brittle long relational messages.",
        "",
        "## Method Comparison",
        "",
        "| Method | K=4 filtered | K=8 no-coordinate | Delta |",
        "|---|---:|---:|---:|",
    ]
    for row in report["method_deltas"]:
        lines.append(
            f"| {row['label']} | {fmt(row['k4_success'])} | {fmt(row['k8_success'])} | {fmt_signed(row['delta'])} |"
        )

    lines.extend(["", "## Candidate Budget", ""])
    for condition in report["conditions"]:
        lines.extend(
            [
                f"### {condition['label']}",
                "",
                "| K | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle |",
                "|---:|---:|---:|---:|---:|",
            ]
        )
        for row in condition["candidate_budget"]:
            lines.append(
                f"| {row['k']} | {fmt(row['mean_candidates'])} | {fmt(row['mean_robust_candidates'])} | {fmt(row['robust_scene_rate'])} | {fmt(row['oracle_success'])} |"
            )
        lines.append("")

    lines.extend(["## Claim Boundary", ""])
    lines.extend(f"- {line}" for line in report["claim_boundary"])
    lines.append("")
    return "\n".join(lines)


def fmt(value: float | int | None) -> str:
    return "-" if value is None else f"{float(value):.3f}"


def fmt_signed(value: float) -> str:
    return f"{value:+.3f}"


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: str, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
