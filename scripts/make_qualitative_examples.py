#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import Scene, SceneObject, read_jsonl, read_scenes


EXACT_COORD_RE = re.compile(r"\brow\s+\d+\b|\bcolumn\s+\d+\b", re.IGNORECASE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="docs/qualitative_failure_examples.md")
    parser.add_argument("--json-out", default="results/qualitative_failure_examples.json")
    args = parser.parse_args()

    report = build_report()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {args.markdown_out} and {args.json_out}")


def build_report() -> dict[str, Any]:
    examples = [
        example_from_coded_failure(
            label="perspective_underspecification",
            title="Perspective scene with attribute underspecification",
            scene_file="data/perspective_stress50_scenes.jsonl",
            records_file="results/perspective_stress50_gpt41nano_records.jsonl",
            audit_file="results/perspective_stress50_gpt41nano_audit.jsonl",
            coded_failures_file="results/perspective_stress50_gpt41nano_mirror_failures_coded.csv",
            failure_category="underspecified_distractor",
            mirror_method="hybrid_local_mirror_api_eval",
            repair_method="hybrid_local_population_api_eval",
            repair_field="population_selected",
            repair_label="population",
            interpretation=(
                "The mirror-selected message names attributes shared by the target and distractor. "
                "The population-selected message adds a listener-invariant coordinate fallback."
            ),
        ),
        example_from_coded_failure(
            label="perspective_frame_error",
            title="Perspective scene with frame-sensitive relation",
            scene_file="data/perspective_stress50_scenes.jsonl",
            records_file="results/perspective_stress50_gpt41nano_records.jsonl",
            audit_file="results/perspective_stress50_gpt41nano_audit.jsonl",
            coded_failures_file="results/perspective_stress50_gpt41nano_mirror_failures_coded.csv",
            failure_category="perspective_frame_error",
            mirror_method="hybrid_local_mirror_api_eval",
            repair_method="hybrid_local_population_api_eval",
            repair_field="population_selected",
            repair_label="population",
            interpretation=(
                "The mirror-selected relation uses left/right language that is brittle under partner "
                "orientation shift. The population selector chooses an unambiguous fallback."
            ),
        ),
        example_from_coded_failure(
            label="partial_observability_underspecification",
            title="Partial-observability scene with visible distractor ambiguity",
            scene_file="data/partial_observability_local50_scenes.jsonl",
            records_file="results/partial_observability_api50_records.jsonl",
            audit_file="results/partial_observability_api50_candidates.jsonl",
            coded_failures_file="results/partial_observability_api50_mirror_failures_coded.csv",
            failure_category="underspecified_distractor",
            mirror_method="hybrid_local_mirror_api_eval",
            repair_method="hybrid_local_population_api_eval",
            repair_field="population_selected",
            repair_label="population",
            interpretation=(
                "The failure does not require private-landmark leakage: the mirror message is simply "
                "too short to distinguish two listener-visible same-attribute objects."
            ),
        ),
        no_coordinate_repair_example(),
    ]
    return {
        "description": (
            "Cache-only representative qualitative examples linking selected messages, held-out "
            "listener choices, and generated scene context."
        ),
        "n_examples": len(examples),
        "examples": examples,
    }


def example_from_coded_failure(
    *,
    label: str,
    title: str,
    scene_file: str,
    records_file: str,
    audit_file: str,
    coded_failures_file: str,
    failure_category: str,
    mirror_method: str,
    repair_method: str,
    repair_field: str,
    repair_label: str,
    interpretation: str,
) -> dict[str, Any]:
    coded_row = first_coded_failure(coded_failures_file, failure_category)
    scene_id = coded_row["scene_id"]
    scenes = {scene.scene_id: scene for scene in read_scenes(scene_file)}
    audits = {row["scene_id"]: row for row in read_jsonl(audit_file)}
    grouped_records = group_records(records_file)

    scene = scenes[scene_id]
    audit = audits[scene_id]
    mirror_message = coded_row["message"]
    repair_message = audit[repair_field]
    mirror_rows = rows_for(grouped_records, scene_id, mirror_method, mirror_message)
    repair_rows = rows_for(grouped_records, scene_id, repair_method, repair_message)

    return assemble_example(
        label=label,
        title=title,
        scene=scene,
        failure_category=failure_category,
        mirror_message=mirror_message,
        repair_message=repair_message,
        repair_label=repair_label,
        mirror_rows=mirror_rows,
        repair_rows=repair_rows,
        source_records=records_file,
        source_audit=audit_file,
        source_coding=coded_failures_file,
        interpretation=interpretation,
    )


def no_coordinate_repair_example() -> dict[str, Any]:
    scene_file = "data/partial_observability_local50_scenes.jsonl"
    records_file = "results/partial_observability_api50_no_coord_records.jsonl"
    audit_file = "results/partial_observability_api50_no_coord_audit.jsonl"
    scenes = {scene.scene_id: scene for scene in read_scenes(scene_file)}
    audits = {row["scene_id"]: row for row in read_jsonl(audit_file)}
    grouped_records = group_records(records_file)

    for scene_id in sorted(audits):
        audit = audits[scene_id]
        mirror_message = audit["mirror_selected"]
        repair_message = audit["consensus_info_selected"]
        if EXACT_COORD_RE.search(repair_message):
            continue
        mirror_rows = rows_for(grouped_records, scene_id, "no_coord_mirror", mirror_message)
        repair_rows = rows_for(grouped_records, scene_id, "no_coord_consensus_info", repair_message)
        if not mirror_rows or not repair_rows:
            continue
        if outcome_summary(mirror_rows)["success_rate"] < 1.0 and outcome_summary(repair_rows)["success_rate"] == 1.0:
            return assemble_example(
                label="partial_observability_no_coordinate_repair",
                title="No-coordinate repair using consensus+info",
                scene=scenes[scene_id],
                failure_category="underspecified_distractor",
                mirror_message=mirror_message,
                repair_message=repair_message,
                repair_label="consensus+info",
                mirror_rows=mirror_rows,
                repair_rows=repair_rows,
                source_records=records_file,
                source_audit=audit_file,
                source_coding="results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
                interpretation=(
                    "After exact coordinates are filtered out, consensus+info can still repair the "
                    "mirror failure by selecting a more informative visible cue."
                ),
            )
    raise RuntimeError("could not find no-coordinate consensus+info repair example")


def assemble_example(
    *,
    label: str,
    title: str,
    scene: Scene,
    failure_category: str,
    mirror_message: str,
    repair_message: str,
    repair_label: str,
    mirror_rows: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    source_records: str,
    source_audit: str,
    source_coding: str,
    interpretation: str,
) -> dict[str, Any]:
    target = object_by_id(scene, scene.target_id)
    first_failed_choice = next((row["choice_id"] for row in mirror_rows if not row["success"]), None)
    confuser = object_by_id(scene, first_failed_choice) if first_failed_choice else None
    return {
        "label": label,
        "title": title,
        "scene_id": scene.scene_id,
        "scenario_type": scene.scenario_type,
        "speaker_orientation": scene.speaker_orientation,
        "listener_orientation": scene.listener_orientation,
        "failure_category": failure_category,
        "target": describe(target),
        "confuser": describe(confuser) if confuser else "-",
        "private_landmark_id": scene.metadata.get("private_landmark_id", "-"),
        "mirror_message": mirror_message,
        "repair_label": repair_label,
        "repair_message": repair_message,
        "mirror_outcome": outcome_summary(mirror_rows),
        "repair_outcome": outcome_summary(repair_rows),
        "source_records": source_records,
        "source_audit": source_audit,
        "source_coding": source_coding,
        "interpretation": interpretation,
    }


def first_coded_failure(path: str, category: str) -> dict[str, str]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["author_category"] == category:
                return row
    raise KeyError(f"{category} not found in {path}")


def group_records(path: str) -> dict[tuple[str, str, str], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(path):
        grouped[(row["scene_id"], row["method"], row["message"])].append(row)
    return grouped


def rows_for(
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]],
    scene_id: str,
    method: str,
    message: str,
) -> list[dict[str, Any]]:
    rows = grouped.get((scene_id, method, message), [])
    return sorted(rows, key=lambda row: row["listener"])


def outcome_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    successes = sum(int(row["success"]) for row in rows)
    choices = Counter(row["choice_id"] for row in rows)
    return {
        "n": n,
        "successes": successes,
        "success_rate": successes / n if n else 0.0,
        "choices": dict(sorted(choices.items())),
        "listeners": [
            {
                "listener": row["listener"],
                "choice_id": row["choice_id"],
                "success": int(row["success"]),
                "reason_code": row.get("reason_code", "other"),
            }
            for row in rows
        ],
    }


def object_by_id(scene: Scene, obj_id: str | None) -> SceneObject | None:
    if not obj_id:
        return None
    for obj in scene.objects:
        if obj.id == obj_id:
            return obj
    return None


def describe(obj: SceneObject | None) -> str:
    if obj is None:
        return "-"
    visibility = "visible" if obj.visible_to_listener else "hidden"
    return f"{obj.id}: {obj.size} {obj.color} {obj.shape} at row {obj.y}, column {obj.x} ({visibility})"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Qualitative Failure Examples",
        "",
        report["description"],
        "The examples are selected deterministically from cached artifacts and make no API calls.",
        "",
        "## Summary",
        "",
        "| Example | Scene | Category | Mirror success | Repair | Repair success | Source |",
        "|---|---|---|---:|---|---:|---|",
    ]
    for ex in report["examples"]:
        lines.append(
            f"| {ex['title']} | `{ex['scene_id']}` | {ex['failure_category']} | "
            f"{fmt_rate(ex['mirror_outcome'])} | {ex['repair_label']} | "
            f"{fmt_rate(ex['repair_outcome'])} | `{ex['source_records']}` |"
        )

    for ex in report["examples"]:
        lines.extend(
            [
                "",
                f"## {ex['title']}",
                "",
                f"- Scene: `{ex['scene_id']}` ({ex['scenario_type']}); speaker faces `{ex['speaker_orientation']}`, listener faces `{ex['listener_orientation']}`.",
                f"- Target: {ex['target']}",
                f"- Confuser chosen by at least one held-out listener: {ex['confuser']}",
                f"- Private landmark ID: `{ex['private_landmark_id']}`",
                f"- Mirror-selected message: {quote(ex['mirror_message'])}",
                f"- {ex['repair_label']} message: {quote(ex['repair_message'])}",
                f"- Interpretation: {ex['interpretation']}",
                "",
                "| Listener | Mirror choice | Mirror success | Repair choice | Repair success |",
                "|---|---|---:|---|---:|",
            ]
        )
        repair_by_listener = {row["listener"]: row for row in ex["repair_outcome"]["listeners"]}
        for row in ex["mirror_outcome"]["listeners"]:
            repair = repair_by_listener.get(row["listener"])
            if repair is None:
                repair_choice = "-"
                repair_success = "-"
            else:
                repair_choice = f"`{repair['choice_id']}`"
                repair_success = str(repair["success"])
            lines.append(
                f"| `{row['listener']}` | `{row['choice_id']}` | {row['success']} | {repair_choice} | {repair_success} |"
            )
        lines.extend(
            [
                "",
                f"Sources: `{ex['source_audit']}`; `{ex['source_coding']}`.",
            ]
        )

    return "\n".join(lines) + "\n"


def fmt_rate(outcome: dict[str, Any]) -> str:
    return f"{outcome['success_rate']:.3f} ({outcome['successes']}/{outcome['n']})"


def quote(text: str) -> str:
    return f'"{text}"'


if __name__ == "__main__":
    main()
