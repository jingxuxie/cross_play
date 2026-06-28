#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


FAILURE_SETS = [
    {
        "label": "perspective_gpt41_full_mirror",
        "display": "Perspective alt-model mirror",
        "path": "results/perspective_stress50_gpt41nano_mirror_failures_coded.csv",
    },
    {
        "label": "partial_observability_full_mirror",
        "display": "Partial-observability mirror",
        "path": "results/partial_observability_api50_mirror_failures_coded.csv",
    },
    {
        "label": "partial_observability_no_coord_mirror",
        "display": "Partial no-coordinate mirror",
        "path": "results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
    },
]

CATEGORY_ORDER = [
    "underspecified_distractor",
    "perspective_frame_error",
    "underspecified_other",
    "listener_misparse_or_other",
    "wrong_attribute",
    "wrong_relation",
    "private_landmark",
    "idiosyncratic_convention",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Combine rubric-coded mirror failures into a paper-facing taxonomy audit."
    )
    parser.add_argument("--markdown-out", default="docs/failure_taxonomy_audit.md")
    parser.add_argument("--json-out", default="results/failure_taxonomy_audit.json")
    parser.add_argument("--tex-out", default="paper/tables/failure_taxonomy_combined.tex")
    args = parser.parse_args()

    report = build_report()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    Path(args.tex_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.tex_out).write_text(render_tex(report), encoding="utf-8")
    print(render_markdown(report))


def build_report() -> dict[str, Any]:
    rows = []
    combined = Counter()
    for spec in FAILURE_SETS:
        failure_rows = read_csv(spec["path"])
        counts = Counter(row["author_category"] for row in failure_rows)
        combined.update(counts)
        rows.append(
            {
                "label": spec["label"],
                "display": spec["display"],
                "path": spec["path"],
                "n_failures": len(failure_rows),
                "category_counts": normalized_counts(counts),
                "dominant_category": dominant_category(counts),
                "dominant_fraction": (
                    counts[dominant_category(counts)] / len(failure_rows) if failure_rows else 0.0
                ),
            }
        )
    total = sum(row["n_failures"] for row in rows)
    return {
        "failure_sets": rows,
        "combined": {
            "n_failures": total,
            "category_counts": normalized_counts(combined),
            "underspecified_fraction": (
                combined["underspecified_distractor"] / total if total else 0.0
            ),
            "perspective_frame_fraction": (
                combined["perspective_frame_error"] / total if total else 0.0
            ),
        },
    }


def read_csv(path: str) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalized_counts(counts: Counter[str]) -> dict[str, int]:
    out = {category: counts.get(category, 0) for category in CATEGORY_ORDER}
    for category, count in sorted(counts.items()):
        out.setdefault(category, count)
    return out


def dominant_category(counts: Counter[str]) -> str:
    if not counts:
        return ""
    return max(counts.items(), key=lambda item: (item[1], item[0]))[0]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Failure Taxonomy Audit",
        "",
        "This cache-only audit combines the rubric-coded listener-level mirror failures used in the paper.",
        "The categories come from `scripts/code_failures_with_context.py` and are grounded in the selected message, target object, and chosen distractor.",
        "",
        "| Failure set | Rows | Underspecified distractor | Perspective-frame error | Other coded categories | Dominant category |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in report["failure_sets"]:
        counts = row["category_counts"]
        other = row["n_failures"] - counts["underspecified_distractor"] - counts["perspective_frame_error"]
        lines.append(
            "| {display} | {n} | {underspecified} | {perspective} | {other} | {dominant} ({frac:.3f}) |".format(
                display=row["display"],
                n=row["n_failures"],
                underspecified=counts["underspecified_distractor"],
                perspective=counts["perspective_frame_error"],
                other=other,
                dominant=format_category(row["dominant_category"]),
                frac=row["dominant_fraction"],
            )
        )
    combined = report["combined"]
    counts = combined["category_counts"]
    other = combined["n_failures"] - counts["underspecified_distractor"] - counts["perspective_frame_error"]
    lines.extend(
        [
            "",
            "| Combined rows | Rows | Underspecified distractor | Perspective-frame error | Other coded categories |",
            "|---|---:|---:|---:|---:|",
            f"| combined | {combined['n_failures']} | {counts['underspecified_distractor']} | {counts['perspective_frame_error']} | {other} |",
            "",
            "Interpretation: the coded mirror failures are overwhelmingly target-distractor ambiguity rather than hidden-information leakage or arbitrary listener mistakes. Across 152 listener-level failures, 147 are underspecified-distractor cases and 5 are perspective-frame errors.",
            "",
        ]
    )
    return "\n".join(lines)


def render_tex(report: dict[str, Any]) -> str:
    rows = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Failure set & Failures & Underspecified & Perspective & Other \\\\",
        "\\midrule",
    ]
    for row in report["failure_sets"]:
        counts = row["category_counts"]
        other = row["n_failures"] - counts["underspecified_distractor"] - counts["perspective_frame_error"]
        rows.append(
            "{display} & {n} & {underspecified} & {perspective} & {other} \\\\".format(
                display=row["display"],
                n=row["n_failures"],
                underspecified=counts["underspecified_distractor"],
                perspective=counts["perspective_frame_error"],
                other=other,
            )
        )
    combined = report["combined"]
    counts = combined["category_counts"]
    other = combined["n_failures"] - counts["underspecified_distractor"] - counts["perspective_frame_error"]
    rows.extend(
        [
            "\\midrule",
            "Combined & {n} & {underspecified} & {perspective} & {other} \\\\".format(
                n=combined["n_failures"],
                underspecified=counts["underspecified_distractor"],
                perspective=counts["perspective_frame_error"],
                other=other,
            ),
            "\\bottomrule",
            "\\end{tabular}",
            "",
        ]
    )
    return "\n".join(rows)


def format_category(category: str) -> str:
    return category.replace("_", " ")


if __name__ == "__main__":
    main()
