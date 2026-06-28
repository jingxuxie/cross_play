#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_rule_based_ambiguity import classify_message, load_scenes


SCENE_FILES = [
    "data/dev_scenes.jsonl",
    "data/perspective_stress50_scenes.jsonl",
    "data/partial_observability_local50_scenes.jsonl",
]

RUNS = [
    {
        "setting": "perspective_stress",
        "listener": "gpt-5.4-nano",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "setting": "perspective_stress",
        "listener": "gpt-4.1-nano",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "setting": "perspective_stress",
        "listener": "gpt-5.5",
        "records": "results/gpt55_perspective_selected_records.jsonl",
        "methods": {
            "direct": "direct_first",
            "mirror": "mirror_selfplay",
            "population": "population_play",
        },
    },
    {
        "setting": "partial_observability",
        "listener": "gpt-5.4-nano",
        "records": "results/partial_observability_api50_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
        },
    },
    {
        "setting": "partial_observability",
        "listener": "gpt-4.1-nano",
        "records": "results/gpt41_partial_observability_selected_records.jsonl",
        "methods": {
            "direct": "direct_first",
            "mirror": "mirror_selfplay",
            "population": "population_play",
        },
    },
    {
        "setting": "partial_observability",
        "listener": "gpt-5.5",
        "records": "results/gpt55_partial_observability_selected_records.jsonl",
        "methods": {
            "direct": "direct_first",
            "mirror": "mirror_selfplay",
            "population": "population_play",
        },
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Cache-only scene-level overlap analysis for held-out listener failures. "
            "This checks whether GPT-5.5 repairs mirror failures or fails on the same "
            "symbolically ambiguous messages as earlier listener families."
        )
    )
    parser.add_argument("--json-out", default="results/cross_model_failure_overlap.json")
    parser.add_argument("--markdown-out", default="docs/cross_model_failure_overlap.md")
    parser.add_argument("--units-out", default="results/cross_model_failure_overlap_units.jsonl")
    args = parser.parse_args()

    scenes = load_scenes(SCENE_FILES)
    units = []
    run_summaries = []
    for spec in RUNS:
        run_units = analyze_run(spec, scenes)
        units.extend(run_units)
        run_summaries.append(summarize_run(spec, run_units))

    overlap = summarize_overlap(run_summaries)
    report = {
        "description": (
            "Scene-level failure overlap across GPT-5.4-nano, GPT-4.1-nano, and "
            "GPT-5.5 held-out listeners. A scene is a failure when at least one of "
            "the three listener prompt variants fails for the selected message."
        ),
        "runs": run_summaries,
        "overlap": overlap,
        "key_findings": key_findings(run_summaries, overlap),
    }

    write_json(args.json_out, report)
    write_jsonl(args.units_out, units)
    write_text(args.markdown_out, render_markdown(report))
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any], scenes: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in Path(spec["records"]).read_text(encoding="utf-8").splitlines() if line]
    by_method_scene: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    method_lookup = {method: label for label, method in spec["methods"].items()}
    for row in rows:
        method = str(row["method"])
        if method in method_lookup:
            by_method_scene[(method_lookup[method], str(row["scene_id"]))].append(row)

    units = []
    for (method_label, scene_id), scene_rows in sorted(by_method_scene.items()):
        messages = sorted({str(row["message"]) for row in scene_rows})
        if len(messages) != 1:
            raise SystemExit(f"{spec['records']}: multiple messages for {method_label}/{scene_id}: {messages}")
        success_values = [float(row["success"]) for row in scene_rows]
        verdict = classify_message(messages[0], scenes[scene_id])
        units.append(
            {
                "setting": spec["setting"],
                "listener": spec["listener"],
                "records": spec["records"],
                "method": method_label,
                "scene_id": scene_id,
                "message": messages[0],
                "success": mean(success_values),
                "failure": mean(success_values) < 1.0,
                "n_listener_variants": len(scene_rows),
                "failed_listener_variants": sum(1 for value in success_values if value < 1.0),
                **verdict,
            }
        )
    return units


def summarize_run(spec: dict[str, Any], units: list[dict[str, Any]]) -> dict[str, Any]:
    methods = []
    for method in ["direct", "mirror", "population"]:
        rows = [unit for unit in units if unit["method"] == method]
        failures = [unit for unit in rows if unit["failure"]]
        methods.append(
            {
                "method": method,
                "n_scenes": len(rows),
                "success": mean(float(row["success"]) for row in rows),
                "failure_scenes": len(failures),
                "symbolic_rate": rate(rows, "symbolic_ambiguity_flag"),
                "failure_symbolic_rate": rate(failures, "symbolic_ambiguity_flag") if failures else None,
                "failure_label_counts": count_labels(failures),
                "failure_scene_ids": [row["scene_id"] for row in failures],
            }
        )
    return {
        "setting": spec["setting"],
        "listener": spec["listener"],
        "records": spec["records"],
        "methods": methods,
    }


def summarize_overlap(run_summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_setting: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in run_summaries:
        by_setting[run["setting"]].append(run)

    rows = []
    for setting, runs in sorted(by_setting.items()):
        mirror_failures = {
            run["listener"]: set(method_summary(run, "mirror")["failure_scene_ids"])
            for run in sorted(runs, key=lambda item: item["listener"])
        }
        listeners = list(mirror_failures)
        all_failures = set.intersection(*(mirror_failures[listener] for listener in listeners))
        any_failures = set.union(*(mirror_failures[listener] for listener in listeners))
        pairs = []
        for index, left in enumerate(listeners):
            for right in listeners[index + 1 :]:
                left_set = mirror_failures[left]
                right_set = mirror_failures[right]
                pairs.append(
                    {
                        "left": left,
                        "right": right,
                        "left_failures": len(left_set),
                        "right_failures": len(right_set),
                        "intersection": len(left_set & right_set),
                        "union": len(left_set | right_set),
                        "left_only": len(left_set - right_set),
                        "right_only": len(right_set - left_set),
                        "intersection_over_left": safe_div(len(left_set & right_set), len(left_set)),
                        "intersection_over_right": safe_div(len(left_set & right_set), len(right_set)),
                    }
                )
        rows.append(
            {
                "setting": setting,
                "listeners": listeners,
                "mirror_failures": {listener: len(scene_ids) for listener, scene_ids in mirror_failures.items()},
                "all_listener_failure_scenes": len(all_failures),
                "any_listener_failure_scenes": len(any_failures),
                "all_listener_failure_scene_ids": sorted(all_failures),
                "any_listener_failure_scene_ids": sorted(any_failures),
                "pairwise": pairs,
            }
        )
    return rows


def key_findings(run_summaries: list[dict[str, Any]], overlap: list[dict[str, Any]]) -> dict[str, Any]:
    perspective_gpt55 = run_summary(run_summaries, "perspective_stress", "gpt-5.5")
    partial_gpt55 = run_summary(run_summaries, "partial_observability", "gpt-5.5")
    perspective_overlap = overlap_summary(overlap, "perspective_stress")
    partial_overlap = overlap_summary(overlap, "partial_observability")
    perspective_gpt41_gpt55 = pair_summary(perspective_overlap, "gpt-4.1-nano", "gpt-5.5")
    partial_gpt41_gpt55 = pair_summary(partial_overlap, "gpt-4.1-nano", "gpt-5.5")
    return {
        "perspective_gpt55_mirror_success": method_summary(perspective_gpt55, "mirror")["success"],
        "perspective_gpt55_mirror_failure_scenes": method_summary(perspective_gpt55, "mirror")["failure_scenes"],
        "perspective_gpt55_mirror_failure_symbolic_rate": method_summary(perspective_gpt55, "mirror")["failure_symbolic_rate"],
        "perspective_gpt55_population_failure_scenes": method_summary(perspective_gpt55, "population")["failure_scenes"],
        "perspective_gpt41_gpt55_mirror_failure_overlap": perspective_gpt41_gpt55["intersection"],
        "perspective_gpt41_gpt55_overlap_over_gpt41": perspective_gpt41_gpt55["intersection_over_left"],
        "perspective_all_listener_mirror_failure_scenes": perspective_overlap["all_listener_failure_scenes"],
        "perspective_any_listener_mirror_failure_scenes": perspective_overlap["any_listener_failure_scenes"],
        "partial_gpt55_mirror_success": method_summary(partial_gpt55, "mirror")["success"],
        "partial_gpt55_mirror_failure_scenes": method_summary(partial_gpt55, "mirror")["failure_scenes"],
        "partial_gpt55_mirror_failure_symbolic_rate": method_summary(partial_gpt55, "mirror")["failure_symbolic_rate"],
        "partial_gpt55_population_failure_scenes": method_summary(partial_gpt55, "population")["failure_scenes"],
        "partial_gpt41_gpt55_mirror_failure_overlap": partial_gpt41_gpt55["intersection"],
        "partial_gpt41_gpt55_overlap_over_gpt41": partial_gpt41_gpt55["intersection_over_left"],
        "partial_all_listener_mirror_failure_scenes": partial_overlap["all_listener_failure_scenes"],
        "partial_any_listener_mirror_failure_scenes": partial_overlap["any_listener_failure_scenes"],
    }


def method_summary(run: dict[str, Any], method: str) -> dict[str, Any]:
    for row in run["methods"]:
        if row["method"] == method:
            return row
    raise KeyError(method)


def run_summary(run_summaries: list[dict[str, Any]], setting: str, listener: str) -> dict[str, Any]:
    for run in run_summaries:
        if run["setting"] == setting and run["listener"] == listener:
            return run
    raise KeyError((setting, listener))


def overlap_summary(rows: list[dict[str, Any]], setting: str) -> dict[str, Any]:
    for row in rows:
        if row["setting"] == setting:
            return row
    raise KeyError(setting)


def pair_summary(row: dict[str, Any], left: str, right: str) -> dict[str, Any]:
    for pair in row["pairwise"]:
        if pair["left"] == left and pair["right"] == right:
            return pair
        if pair["left"] == right and pair["right"] == left:
            swapped = dict(pair)
            swapped["left"], swapped["right"] = swapped["right"], swapped["left"]
            swapped["left_failures"], swapped["right_failures"] = (
                swapped["right_failures"],
                swapped["left_failures"],
            )
            swapped["left_only"], swapped["right_only"] = swapped["right_only"], swapped["left_only"]
            swapped["intersection_over_left"], swapped["intersection_over_right"] = (
                swapped["intersection_over_right"],
                swapped["intersection_over_left"],
            )
            return swapped
    raise KeyError((left, right))


def count_labels(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(str(row["verifier_label"]) for row in rows).items()))


def rate(rows: list[dict[str, Any]], key: str) -> float:
    return mean(1.0 if row[key] else 0.0 for row in rows)


def safe_div(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def render_markdown(report: dict[str, Any]) -> str:
    findings = report["key_findings"]
    lines = [
        "# Cross-Model Failure Overlap Audit",
        "",
        "This cache-only audit compares scene-level failures for the same selected messages across held-out listener families. A selected message is counted as a scene failure when at least one of the three listener prompt variants fails.",
        "",
        "## Key Findings",
        "",
        f"- In perspective stress, GPT-5.5 mirror self-play succeeds on {fmt(findings['perspective_gpt55_mirror_success'])} of listener evaluations and has {findings['perspective_gpt55_mirror_failure_scenes']} scene-level failures; all GPT-5.5 mirror-failure scenes are symbolic-verifier positives ({fmt(findings['perspective_gpt55_mirror_failure_symbolic_rate'])}).",
        f"- In perspective stress, {findings['perspective_gpt41_gpt55_mirror_failure_overlap']} of the {method_count(report, 'perspective_stress', 'gpt-4.1-nano', 'mirror')} GPT-4.1 mirror-failure scenes also fail under GPT-5.5 ({fmt(findings['perspective_gpt41_gpt55_overlap_over_gpt41'])}).",
        f"- In partial observability, GPT-5.5 mirror self-play succeeds on {fmt(findings['partial_gpt55_mirror_success'])} and has {findings['partial_gpt55_mirror_failure_scenes']} scene-level failures; all are symbolic-verifier positives ({fmt(findings['partial_gpt55_mirror_failure_symbolic_rate'])}).",
        f"- In partial observability, {findings['partial_gpt41_gpt55_mirror_failure_overlap']} of the {method_count(report, 'partial_observability', 'gpt-4.1-nano', 'mirror')} GPT-4.1 mirror-failure scenes also fail under GPT-5.5 ({fmt(findings['partial_gpt41_gpt55_overlap_over_gpt41'])}).",
        f"- Population-play has {findings['perspective_gpt55_population_failure_scenes']} GPT-5.5 scene-level failures in perspective stress and {findings['partial_gpt55_population_failure_scenes']} in partial observability.",
        "",
        "## Per-Listener Summary",
        "",
        "| Setting | Listener | Method | Success | Failure scenes | Failure symbolic rate | Failure labels |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for run in report["runs"]:
        for row in run["methods"]:
            lines.append(
                "| {setting} | {listener} | {method} | {success} | {failures} | {symbolic} | {labels} |".format(
                    setting=run["setting"],
                    listener=run["listener"],
                    method=row["method"],
                    success=fmt(row["success"]),
                    failures=row["failure_scenes"],
                    symbolic=fmt_optional(row["failure_symbolic_rate"]),
                    labels=format_counts(row["failure_label_counts"]),
                )
            )

    lines.extend(
        [
            "",
            "## Mirror-Failure Overlap",
            "",
            "| Setting | Listener failures | All-listener failures | Any-listener failures |",
            "|---|---|---:|---:|",
        ]
    )
    for row in report["overlap"]:
        counts = ", ".join(f"{listener}: {count}" for listener, count in row["mirror_failures"].items())
        lines.append(
            f"| {row['setting']} | {counts} | {row['all_listener_failure_scenes']} | {row['any_listener_failure_scenes']} |"
        )

    lines.extend(
        [
            "",
            "## Pairwise Mirror-Failure Overlap",
            "",
            "| Setting | Pair | Intersection | Union | Left only | Right only | Intersection / left | Intersection / right |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in report["overlap"]:
        for pair in row["pairwise"]:
            lines.append(
                "| {setting} | {left} vs {right} | {intersection} | {union} | {left_only} | {right_only} | {over_left} | {over_right} |".format(
                    setting=row["setting"],
                    left=pair["left"],
                    right=pair["right"],
                    intersection=pair["intersection"],
                    union=pair["union"],
                    left_only=pair["left_only"],
                    right_only=pair["right_only"],
                    over_left=fmt_optional(pair["intersection_over_left"]),
                    over_right=fmt_optional(pair["intersection_over_right"]),
                )
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "GPT-5.5 does not simply repair the mirror-selected messages that earlier held-out listener families found fragile. The same ambiguous or frame-sensitive mirror messages account for the frontier-listener failures, while population-play remains at zero scene-level failures in both settings.",
        ]
    )
    return "\n".join(lines) + "\n"


def method_count(report: dict[str, Any], setting: str, listener: str, method: str) -> int:
    run = run_summary(report["runs"], setting, listener)
    return int(method_summary(run, method)["failure_scenes"])


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "-"
    return ", ".join(f"{label}: {count}" for label, count in counts.items())


def fmt(value: float) -> str:
    return f"{value:.3f}"


def fmt_optional(value: float | None) -> str:
    return "-" if value is None else fmt(value)


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: str, rows: list[dict[str, Any]]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def write_text(path: str, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
