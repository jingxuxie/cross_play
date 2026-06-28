#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


METHODS = [
    "api_direct_first",
    "api_best_of_k_shortest",
    "hybrid_local_mirror_api_eval",
    "hybrid_local_population_api_eval",
    "oracle_upper_bound",
]
LABELS = {
    "api_direct_first": "Direct",
    "api_best_of_k_shortest": "Best-of-K",
    "hybrid_local_mirror_api_eval": "Mirror",
    "hybrid_local_population_api_eval": "Population",
    "oracle_upper_bound": "Oracle",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mixed-records", default="results/hybrid_api_pilot50_records.jsonl")
    parser.add_argument("--stress-records", default="results/perspective_stress50_hybrid_records.jsonl")
    parser.add_argument("--alt-records", default="results/perspective_stress50_gpt41nano_records.jsonl")
    parser.add_argument("--failures", default="results/perspective_stress50_mirror_failures.csv")
    parser.add_argument("--out-dir", default="paper/tables")
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed = read_jsonl(args.mixed_records)
    stress = read_jsonl(args.stress_records)
    alt = read_jsonl(args.alt_records) if Path(args.alt_records).exists() else []
    write_text(out_dir / "mixed50_by_scenario.md", scenario_markdown(mixed))
    write_text(out_dir / "mixed50_by_scenario.tex", scenario_latex(mixed))
    write_text(out_dir / "perspective_stress50_regret.md", regret_markdown(stress))
    write_text(out_dir / "perspective_stress50_regret.tex", regret_latex(stress))
    if alt:
        write_text(out_dir / "perspective_altmodel50.md", altmodel_markdown(stress, alt))
        write_text(out_dir / "perspective_altmodel50.tex", altmodel_latex(stress, alt))
    write_text(out_dir / "perspective_stress50_error_counts.md", error_counts_markdown(args.failures))
    write_text(out_dir / "perspective_stress50_error_counts.tex", error_counts_latex(args.failures))
    write_text(out_dir / "crossplay_gap_bars.tex", gap_bars_latex())
    print(f"wrote analysis artifacts to {out_dir}")


def scenario_markdown(records: list[dict]) -> str:
    grouped = group_success(records, ["scenario_type", "method"])
    scenarios = sorted({row["scenario_type"] for row in records})
    rows = ["| Scenario | Direct | Best-of-K | Mirror | Population | Oracle |", "|---|---:|---:|---:|---:|---:|"]
    for scenario in scenarios:
        cells = [fmt(grouped.get((scenario, method))) for method in METHODS]
        rows.append(f"| {scenario} | " + " | ".join(cells) + " |")
    return "\n".join(rows) + "\n"


def scenario_latex(records: list[dict]) -> str:
    grouped = group_success(records, ["scenario_type", "method"])
    scenarios = sorted({row["scenario_type"] for row in records})
    rows = [
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Scenario & Direct & Best-of-K & Mirror & Population & Oracle \\\\",
        "\\midrule",
    ]
    for scenario in scenarios:
        cells = [fmt(grouped.get((scenario, method))) for method in METHODS]
        rows.append(f"{pretty(scenario)} & " + " & ".join(cells) + " \\\\")
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def regret_markdown(records: list[dict]) -> str:
    regrets = selection_regrets(records)
    rows = ["| Method | Selection regret vs. oracle |", "|---|---:|"]
    for method in METHODS[:-1]:
        rows.append(f"| {LABELS[method]} | {regrets[method]:.3f} |")
    return "\n".join(rows) + "\n"


def regret_latex(records: list[dict]) -> str:
    regrets = selection_regrets(records)
    rows = ["\\begin{tabular}{lr}", "\\toprule", "Method & Regret \\\\", "\\midrule"]
    for method in METHODS[:-1]:
        rows.append(f"{LABELS[method]} & {regrets[method]:.3f} \\\\")
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def altmodel_markdown(primary: list[dict], alternate: list[dict]) -> str:
    rows = [
        "| Held-out model | Direct | Best-of-K | Mirror | Population | Oracle |",
        "|---|---:|---:|---:|---:|---:|",
        "| gpt-5.4-nano | " + " | ".join(fmt(group_success(primary, ["method"]).get((method,))) for method in METHODS) + " |",
        "| gpt-4.1-nano | " + " | ".join(fmt(group_success(alternate, ["method"]).get((method,))) for method in METHODS) + " |",
    ]
    return "\n".join(rows) + "\n"


def altmodel_latex(primary: list[dict], alternate: list[dict]) -> str:
    primary_scores = group_success(primary, ["method"])
    alternate_scores = group_success(alternate, ["method"])
    rows = [
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Held-out model & Direct & Best-of-K & Mirror & Population & Oracle \\\\",
        "\\midrule",
        "gpt-5.4-nano & "
        + " & ".join(fmt(primary_scores.get((method,))) for method in METHODS)
        + " \\\\",
        "gpt-4.1-nano & "
        + " & ".join(fmt(alternate_scores.get((method,))) for method in METHODS)
        + " \\\\",
        "\\bottomrule",
        "\\end{tabular}",
        "",
    ]
    return "\n".join(rows)


def error_counts_markdown(failure_csv: str) -> str:
    counts = failure_counts(failure_csv)
    rows = ["| Auto category | Count |", "|---|---:|"]
    for category, count in sorted(counts.items()):
        rows.append(f"| {category} | {count} |")
    return "\n".join(rows) + "\n"


def error_counts_latex(failure_csv: str) -> str:
    counts = failure_counts(failure_csv)
    rows = ["\\begin{tabular}{lr}", "\\toprule", "Auto category & Count \\\\", "\\midrule"]
    for category, count in sorted(counts.items()):
        rows.append(f"{category.replace('_', ' ')} & {count} \\\\")
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def gap_bars_latex() -> str:
    # Widths are scaled in centimeters: 0.187 -> 1.87cm, 0.093 -> 0.93cm.
    return r"""\begin{tabular}{lll}
\toprule
Setting & Gap & Same-play minus cross-play \\
\midrule
Mixed 50, mirror & 0.093 & \rule{0.93cm}{6pt} \\
Mixed 50, population & 0.000 &  \\
Perspective stress, mirror & 0.187 & \rule{1.87cm}{6pt} \\
Perspective stress, population & 0.000 &  \\
\bottomrule
\end{tabular}
"""


def group_success(records: list[dict], keys: list[str]) -> dict[tuple, float]:
    grouped: dict[tuple, list[float]] = defaultdict(list)
    for row in records:
        grouped[tuple(row[key] for key in keys)].append(float(row["success"]))
    return {key: mean(values) for key, values in grouped.items()}


def selection_regrets(records: list[dict]) -> dict[str, float]:
    by_scene_method: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in records:
        by_scene_method[(row["scene_id"], row["method"])].append(float(row["success"]))
    scene_ids = sorted({scene_id for scene_id, _ in by_scene_method})
    out = {}
    for method in METHODS[:-1]:
        diffs = []
        for scene_id in scene_ids:
            oracle = mean(by_scene_method[(scene_id, "oracle_upper_bound")])
            current = mean(by_scene_method[(scene_id, method)])
            diffs.append(oracle - current)
        out[method] = mean(diffs)
    return out


def failure_counts(path: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    with Path(path).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            counts[row["auto_error_category"]] += 1
    return dict(counts)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


def pretty(scenario: str) -> str:
    return scenario.replace("_", " ").title()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
