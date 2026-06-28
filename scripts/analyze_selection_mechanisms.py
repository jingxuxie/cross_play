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
from prag_crossplay.methods import token_count

EXACT_COORD_RE = re.compile(
    r"\brow\s+\d+\b|\bcolumn\s+\d+\b|\b\d+(?:st|nd|rd|th)?\s+row\b|\b\d+(?:st|nd|rd|th)?\s+column\b",
    re.IGNORECASE,
)
SPATIAL_RE = re.compile(
    r"\bleft\b|\bright\b|\bleftmost\b|\brightmost\b|\bfarthest\b|\bclosest\b|"
    r"\babove\b|\bbelow\b|\bnext to\b|\bbeside\b|\bbetween\b|\bamong\b",
    re.IGNORECASE,
)
CONTRAST_RE = re.compile(r"\bonly\b|\bunique\b|\bother\b|\banother\b", re.IGNORECASE)

METHODS = [
    (
        "mirror",
        "mirror_selected",
        ("no_coord_mirror", "hybrid_local_mirror_api_eval"),
        "Mirror",
    ),
    (
        "population",
        "population_selected",
        ("no_coord_population", "hybrid_local_population_api_eval"),
        "Population",
    ),
    (
        "consensus_info",
        "consensus_info_selected",
        ("no_coord_consensus_info",),
        "Consensus+info",
    ),
    ("informative", "informative_selected", ("no_coord_informative",), "Info prior"),
    ("oracle", "oracle_selected", ("no_coord_oracle", "oracle_upper_bound"), "Oracle"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", required=True)
    parser.add_argument("--records", default=None)
    parser.add_argument("--name", required=True)
    parser.add_argument("--markdown-out", required=True)
    parser.add_argument("--tex-out", required=True)
    args = parser.parse_args()

    audit_rows = read_jsonl(args.audit)
    record_success = load_record_success(args.records) if args.records else {}
    rows = analyze(audit_rows, record_success, args.name)

    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown_table(rows), encoding="utf-8")
    Path(args.tex_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.tex_out).write_text(tex_table(rows), encoding="utf-8")
    print(markdown_table(rows))


def load_record_success(path: str | Path) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in read_jsonl(path):
        grouped[row["method"]].append(float(row["success"]))
    return {method: mean(values) for method, values in grouped.items()}


def analyze(
    audit_rows: list[dict[str, Any]],
    record_success: dict[str, float],
    dataset_name: str,
) -> list[dict[str, Any]]:
    out = []
    for short_name, field, record_methods, label in METHODS:
        selected = [str(row[field]) for row in audit_rows if field in row and row.get(field)]
        if not selected:
            continue
        source_counts: Counter[str] = Counter()
        if short_name == "consensus_info":
            source_counts.update(
                str(row.get("consensus_info_source", "unknown"))
                for row in audit_rows
                if row.get(field)
            )
        out.append(
            {
                "dataset": dataset_name,
                "method": label,
                "n": len(selected),
                "crossplay": first_present(record_success, record_methods),
                "exact_coord_rate": rate(EXACT_COORD_RE.search(message) for message in selected),
                "spatial_rate": rate(SPATIAL_RE.search(message) for message in selected),
                "contrast_rate": rate(CONTRAST_RE.search(message) for message in selected),
                "mean_tokens": mean(token_count(message) for message in selected),
                "source": source_summary(source_counts),
            }
        )
    return out


def markdown_table(rows: list[dict[str, Any]]) -> str:
    table = [
        "| Dataset | Method | Cross-play | Exact coord | Spatial cue | Contrast cue | Tokens | Source |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        table.append(
            "| {dataset} | {method} | {crossplay} | {exact:.2f} | {spatial:.2f} | {contrast:.2f} | {tokens:.1f} | {source} |".format(
                dataset=row["dataset"],
                method=row["method"],
                crossplay=fmt(row["crossplay"]),
                exact=row["exact_coord_rate"],
                spatial=row["spatial_rate"],
                contrast=row["contrast_rate"],
                tokens=row["mean_tokens"],
                source=row["source"],
            )
        )
    return "\n".join(table) + "\n"


def tex_table(rows: list[dict[str, Any]]) -> str:
    table = [
        "\\begin{tabular}{llrrrrl}",
        "\\toprule",
        "Dataset & Method & Cross-play & Coord & Spatial & Tokens & Source \\\\",
        "\\midrule",
    ]
    for row in rows:
        table.append(
            "{dataset} & {method} & {crossplay} & {exact:.2f} & {spatial:.2f} & {tokens:.1f} & {source} \\\\".format(
                dataset=escape_tex(row["dataset"]),
                method=escape_tex(row["method"]),
                crossplay=fmt(row["crossplay"]),
                exact=row["exact_coord_rate"],
                spatial=row["spatial_rate"],
                tokens=row["mean_tokens"],
                source=escape_tex(row["source"]),
            )
        )
    table.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(table)


def rate(values: Any) -> float:
    values = list(values)
    return mean(1.0 if value else 0.0 for value in values) if values else 0.0


def source_summary(counts: Counter[str]) -> str:
    if not counts:
        return "-"
    total = sum(counts.values())
    return ", ".join(f"{name}:{count}/{total}" for name, count in sorted(counts.items()))


def first_present(values: dict[str, float], keys: tuple[str, ...]) -> float | None:
    for key in keys:
        if key in values:
            return values[key]
    return None


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


def escape_tex(text: str) -> str:
    return text.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


if __name__ == "__main__":
    main()
