#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


METHOD_LABELS = {
    "template": "Template",
    "api_direct_first": "Direct",
    "api_best_of_k_shortest": "Best-of-K shortest",
    "hybrid_local_mirror_api_eval": "Mirror self-play",
    "hybrid_local_population_api_eval": "Population-play",
    "oracle_upper_bound": "Oracle candidate",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--paired", default=None)
    parser.add_argument("--out-dir", default="paper/tables")
    parser.add_argument("--name", default="main_results")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    table = _results_table(summary)
    (out_dir / f"{args.name}.tex").write_text(table, encoding="utf-8")
    (out_dir / f"{args.name}.md").write_text(_markdown_results_table(summary), encoding="utf-8")
    if args.paired:
        paired = json.loads(Path(args.paired).read_text(encoding="utf-8"))
        (out_dir / f"{args.name}_paired.tex").write_text(_paired_table(paired), encoding="utf-8")
        (out_dir / f"{args.name}_paired.md").write_text(_markdown_paired_table(paired), encoding="utf-8")
    print(f"wrote paper tables to {out_dir}")


def _results_table(summary: dict) -> str:
    rows = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Method & Cross-play & 95\\% CI & Same-play & Gap \\\\",
        "\\midrule",
    ]
    order = [
        "template",
        "api_direct_first",
        "api_best_of_k_shortest",
        "hybrid_local_mirror_api_eval",
        "hybrid_local_population_api_eval",
        "oracle_upper_bound",
    ]
    for method in order:
        if method not in summary["by_method"]:
            continue
        stats = summary["by_method"][method]
        ci = stats["success_ci95"]
        same = "--" if stats["sameplay_success"] is None else f"{stats['sameplay_success']:.3f}"
        gap = "--" if stats["crossplay_gap"] is None else f"{stats['crossplay_gap']:.3f}"
        rows.append(
            f"{METHOD_LABELS[method]} & {stats['success']:.3f} & [{ci[0]:.3f}, {ci[1]:.3f}] & {same} & {gap} \\\\"
        )
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def _markdown_results_table(summary: dict) -> str:
    rows = [
        "| Method | Cross-play | 95% CI | Same-play | Gap |",
        "|---|---:|---:|---:|---:|",
    ]
    for method, label in METHOD_LABELS.items():
        if method not in summary["by_method"]:
            continue
        stats = summary["by_method"][method]
        ci = stats["success_ci95"]
        same = "-" if stats["sameplay_success"] is None else f"{stats['sameplay_success']:.3f}"
        gap = "-" if stats["crossplay_gap"] is None else f"{stats['crossplay_gap']:.3f}"
        rows.append(f"| {label} | {stats['success']:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] | {same} | {gap} |")
    return "\n".join(rows) + "\n"


def _paired_table(comparisons: list[dict]) -> str:
    rows = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Scenario & $N$ & Pop. & Mirror & Diff. \\\\",
        "\\midrule",
    ]
    for comp in comparisons:
        if comp["n_pairs"] == 0:
            continue
        scenario = comp["scenario_type"] or "overall"
        ci = comp["diff_ci95"]
        rows.append(
            f"{scenario.replace('_', ' ')} & {comp['n_pairs']} & {comp['mean_a']:.3f} & {comp['mean_b']:.3f} & {comp['diff_a_minus_b']:.3f} [{ci[0]:.3f}, {ci[1]:.3f}] \\\\"
        )
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def _markdown_paired_table(comparisons: list[dict]) -> str:
    rows = [
        "| Scenario | N | Population | Mirror | Diff | 95% CI | p_boot |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for comp in comparisons:
        if comp["n_pairs"] == 0:
            continue
        scenario = comp["scenario_type"] or "overall"
        ci = comp["diff_ci95"]
        rows.append(
            f"| {scenario} | {comp['n_pairs']} | {comp['mean_a']:.3f} | {comp['mean_b']:.3f} | {comp['diff_a_minus_b']:.3f} | [{ci[0]:.3f}, {ci[1]:.3f}] | {comp['paired_bootstrap_p_two_sided']:.4f} |"
        )
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    main()
