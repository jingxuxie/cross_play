#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


COORD_RE = re.compile(r"\brow\s+\d+\b|\bcolumn\s+\d+\b", re.IGNORECASE)
SPATIAL_RE = re.compile(
    r"\bleft\b|\bright\b|\bleftmost\b|\brightmost\b|\babove\b|\bbelow\b|"
    r"\bnext to\b|\bbeside\b|\bbetween\b|\btop\b|\bbottom\b",
    re.IGNORECASE,
)
FRAME_RE = re.compile(r"\bleft\b|\bright\b|\bleftmost\b|\brightmost\b", re.IGNORECASE)

RULES = {
    "underspecified_distractor": {
        "rule_id": "disambiguate_shared_attributes",
        "rule": "If a visible distractor shares the target's basic attributes, do not use a bare attribute phrase; add a listener-visible coordinate or spatial relation.",
    },
    "perspective_frame_error": {
        "rule_id": "avoid_frame_sensitive_only",
        "rule": "When speaker and listener perspectives differ, avoid relying only on frame-sensitive left/right language; prefer listener-invariant coordinates or unambiguous visible anchors.",
    },
    "private_landmark": {
        "rule_id": "avoid_private_landmarks",
        "rule": "Never refer to landmarks or objects hidden from the listener; use listener-visible discriminators.",
    },
    "listener_misparse_or_other": {
        "rule_id": "inspect_listener_misparse",
        "rule": "If a message already contains a discriminator but fails, inspect parser/listener behavior before changing the speaker rule.",
    },
    "underspecified_other": {
        "rule_id": "add_visible_discriminator",
        "rule": "If a message leaves multiple plausible referents, add a visible discriminator.",
    },
}

FAILURE_SETS = [
    {
        "label": "perspective_full_mirror",
        "coded_failures": "results/perspective_stress50_gpt41nano_mirror_failures_coded.csv",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "mirror_method": "hybrid_local_mirror_api_eval",
        "repair_method": "hybrid_local_population_api_eval",
        "repair_label": "population",
    },
    {
        "label": "partial_observability_full_mirror",
        "coded_failures": "results/partial_observability_api50_mirror_failures_coded.csv",
        "records": "results/partial_observability_api50_records.jsonl",
        "mirror_method": "hybrid_local_mirror_api_eval",
        "repair_method": "hybrid_local_population_api_eval",
        "repair_label": "population",
    },
    {
        "label": "partial_observability_no_coord_mirror",
        "coded_failures": "results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "mirror_method": "no_coord_mirror",
        "repair_method": "no_coord_consensus_info",
        "repair_label": "consensus+info",
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Derive replay-only interaction-memory rules from coded mirror failures."
    )
    parser.add_argument("--markdown-out", default="docs/interaction_memory_rules.md")
    parser.add_argument("--json-out", default="results/interaction_memory_rules.json")
    args = parser.parse_args()

    sets = [analyze_failure_set(spec) for spec in FAILURE_SETS]
    report = {
        "rules": rule_rows(),
        "failure_sets": sets,
        "combined": combined_summary(sets),
        "prompt_snippet": prompt_snippet(),
    }
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_failure_set(spec: dict[str, str]) -> dict[str, Any]:
    failure_rows = read_coded_failures(spec["coded_failures"])
    units = scene_method_units(read_jsonl(spec["records"]))
    scene_categories: dict[str, Counter[str]] = defaultdict(Counter)
    for row in failure_rows:
        scene_categories[row["scene_id"]][row["author_category"]] += 1

    scene_rows = []
    for scene_id, categories in sorted(scene_categories.items()):
        mirror = units[(scene_id, spec["mirror_method"])]
        repair = units[(scene_id, spec["repair_method"])]
        primary_category = categories.most_common(1)[0][0]
        scene_rows.append(
            {
                "scene_id": scene_id,
                "categories": dict(categories),
                "primary_category": primary_category,
                "rule_id": rule_for_category(primary_category)["rule_id"],
                "failure_rows": sum(categories.values()),
                "mirror_message": mirror["message"],
                "repair_message": repair["message"],
                "mirror_success": mirror["success"],
                "repair_success": repair["success"],
                "repair_all_success": repair["all_success"],
                "mirror_cues": cue_profile(mirror["message"]),
                "repair_cues": cue_profile(repair["message"]),
                "repair_satisfies_rule": repair_satisfies_rule(primary_category, repair["message"]),
            }
        )

    by_category = []
    for category, count in sorted(Counter(row["author_category"] for row in failure_rows).items()):
        category_scenes = [row for row in scene_rows if category in row["categories"]]
        by_category.append(summarize_category(category, count, category_scenes))

    return {
        "label": spec["label"],
        "coded_failures": spec["coded_failures"],
        "records": spec["records"],
        "mirror_method": spec["mirror_method"],
        "repair_method": spec["repair_method"],
        "repair_label": spec["repair_label"],
        "n_failure_rows": len(failure_rows),
        "n_failure_scenes": len(scene_rows),
        "category_counts": dict(sorted(Counter(row["author_category"] for row in failure_rows).items())),
        "by_category": by_category,
        "scene_rows": scene_rows,
    }


def read_coded_failures(path: str) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def scene_method_units(records: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[(str(row["scene_id"]), str(row["method"]))].append(row)
    units = {}
    for key, rows in grouped.items():
        messages = sorted({str(row["message"]) for row in rows})
        if len(messages) != 1:
            raise SystemExit(f"{key}: expected one selected message, found {len(messages)}")
        successes = [float(row["success"]) for row in rows]
        units[key] = {
            "scene_id": key[0],
            "method": key[1],
            "message": messages[0],
            "success": mean(successes),
            "all_success": all(value == 1.0 for value in successes),
            "n_rows": len(rows),
        }
    return units


def summarize_category(
    category: str,
    failure_rows: int,
    scene_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    repairs = [row["repair_success"] for row in scene_rows]
    return {
        "category": category,
        "rule_id": rule_for_category(category)["rule_id"],
        "rule": rule_for_category(category)["rule"],
        "failure_rows": failure_rows,
        "failure_scenes": len(scene_rows),
        "mean_mirror_success_on_failure_scenes": mean(row["mirror_success"] for row in scene_rows),
        "mean_repair_success_on_failure_scenes": mean(repairs) if repairs else None,
        "repair_all_success_scene_rate": rate(row["repair_all_success"] for row in scene_rows),
        "repair_rule_cue_rate": rate(row["repair_satisfies_rule"] for row in scene_rows),
        "repair_coordinate_rate": rate(row["repair_cues"]["coordinate"] for row in scene_rows),
        "repair_spatial_rate": rate(row["repair_cues"]["spatial"] for row in scene_rows),
        "repair_attribute_short_rate": rate(row["repair_cues"]["attribute_short"] for row in scene_rows),
    }


def combined_summary(sets: list[dict[str, Any]]) -> dict[str, Any]:
    category_counts: Counter[str] = Counter()
    rule_counts: Counter[str] = Counter()
    n_failure_rows = 0
    n_failure_scenes = 0
    repair_successes = []
    repair_all_success = []
    repair_rule_cues = []
    for failure_set in sets:
        n_failure_rows += failure_set["n_failure_rows"]
        n_failure_scenes += failure_set["n_failure_scenes"]
        category_counts.update(failure_set["category_counts"])
        for row in failure_set["scene_rows"]:
            rule_counts[row["rule_id"]] += row["failure_rows"]
            repair_successes.append(row["repair_success"])
            repair_all_success.append(row["repair_all_success"])
            repair_rule_cues.append(row["repair_satisfies_rule"])
    return {
        "n_failure_rows": n_failure_rows,
        "n_failure_scenes": n_failure_scenes,
        "category_counts": dict(sorted(category_counts.items())),
        "rule_counts": dict(sorted(rule_counts.items())),
        "mean_repair_success_on_failure_scenes": mean(repair_successes) if repair_successes else None,
        "repair_all_success_scene_rate": rate(repair_all_success),
        "repair_rule_cue_rate": rate(repair_rule_cues),
    }


def cue_profile(message: str) -> dict[str, bool]:
    tokens = message.replace(".", " ").replace(",", " ").split()
    coordinate = bool(COORD_RE.search(message))
    spatial = bool(SPATIAL_RE.search(message))
    frame = bool(FRAME_RE.search(message))
    return {
        "coordinate": coordinate,
        "spatial": spatial,
        "frame_term": frame,
        "attribute_short": len(tokens) <= 6 and not coordinate and not spatial,
    }


def repair_satisfies_rule(category: str, message: str) -> bool:
    cues = cue_profile(message)
    if category == "underspecified_distractor":
        return cues["coordinate"] or cues["spatial"]
    if category == "perspective_frame_error":
        return cues["coordinate"] or not cues["frame_term"]
    if category == "private_landmark":
        return "hidden" not in message.lower() and "private" not in message.lower()
    return cues["coordinate"] or cues["spatial"] or not cues["attribute_short"]


def rule_for_category(category: str) -> dict[str, str]:
    return RULES.get(category, RULES["underspecified_other"])


def rule_rows() -> list[dict[str, str]]:
    return [
        {"category": category, **rule}
        for category, rule in sorted(RULES.items())
    ]


def prompt_snippet() -> list[str]:
    return [
        "If another visible object shares the target's size/color/shape, add a visible discriminator such as row/column or an unambiguous spatial relation.",
        "When speaker and listener perspectives differ, avoid relying only on left/right; prefer listener-invariant coordinates or visible anchors.",
        "Use only listener-visible landmarks; never mention hidden or private landmarks.",
        "If exact coordinates are disallowed, prefer the relational/spatial candidate over a short attribute-only candidate when both seem locally acceptable.",
    ]


def rate(values: Any) -> float:
    values = list(values)
    return mean(1.0 if value else 0.0 for value in values) if values else 0.0


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Interaction Memory Rule Audit",
        "",
        "This replay-only audit materializes the workshop plan's interaction-memory idea without making new API calls.",
        "It derives speaker rules from the coded mirror-failure files and checks whether cached repair selectors instantiate the relevant cue on the same failure scenes.",
        "",
        "## Failure-Derived Speaker Rules",
        "",
        "| Rule ID | Triggering failure category | Speaker rule |",
        "|---|---|---|",
    ]
    for row in report["rules"]:
        lines.append(f"| {row['rule_id']} | `{row['category']}` | {row['rule']} |")

    lines.extend(
        [
            "",
            "## Repair Coverage By Failure Set",
            "",
            "| Failure set | Repair selector | Category | Failure rows | Failure scenes | Mirror success on scenes | Repair success on scenes | Repair all-success scenes | Repair cue satisfies rule | Repair coordinate | Repair spatial | Repair short-attribute |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for failure_set in report["failure_sets"]:
        for row in failure_set["by_category"]:
            lines.append(
                "| {label} | {repair} | {category} | {failure_rows} | {failure_scenes} | {mirror_success:.3f} | {repair_success:.3f} | {all_success:.3f} | {cue:.3f} | {coord:.3f} | {spatial:.3f} | {short:.3f} |".format(
                    label=failure_set["label"],
                    repair=failure_set["repair_label"],
                    category=row["category"],
                    failure_rows=row["failure_rows"],
                    failure_scenes=row["failure_scenes"],
                    mirror_success=row["mean_mirror_success_on_failure_scenes"],
                    repair_success=row["mean_repair_success_on_failure_scenes"],
                    all_success=row["repair_all_success_scene_rate"],
                    cue=row["repair_rule_cue_rate"],
                    coord=row["repair_coordinate_rate"],
                    spatial=row["repair_spatial_rate"],
                    short=row["repair_attribute_short_rate"],
                )
            )

    combined = report["combined"]
    lines.extend(
        [
            "",
            "## Combined Summary",
            "",
            f"Coded failure rows: {combined['n_failure_rows']}. Unique failure scenes: {combined['n_failure_scenes']}.",
            f"Rule counts: {format_counts(combined['rule_counts'])}.",
            f"Mean repair success on failure scenes: {combined['mean_repair_success_on_failure_scenes']:.3f}.",
            f"Repair all-success scene rate: {combined['repair_all_success_scene_rate']:.3f}.",
            f"Repair cue satisfies derived rule in {combined['repair_rule_cue_rate']:.3f} of failure scenes.",
            "",
            "## Prompt Snippet For A Future Interaction-Memory Run",
            "",
            "```text",
        ]
    )
    for index, rule in enumerate(report["prompt_snippet"], start=1):
        lines.append(f"{index}. {rule}")
    lines.extend(
        [
            "```",
            "",
            "Interpretation: the current paper does not claim a new interaction-memory experiment.",
            "This artifact shows that the coded failures collapse into a small reusable rule set, and that existing population or consensus+info repairs usually instantiate those rules on the same failure scenes.",
            "",
        ]
    )
    return "\n".join(lines)


def format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}:{value}" for key, value in counts.items())


if __name__ == "__main__":
    main()
