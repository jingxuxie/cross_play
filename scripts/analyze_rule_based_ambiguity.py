#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import Scene, SceneObject, read_jsonl, read_scenes, write_jsonl


SCENE_FILES = [
    "data/dev_scenes.jsonl",
    "data/perspective_stress50_scenes.jsonl",
    "data/partial_observability_local50_scenes.jsonl",
]

RUNS = [
    {
        "label": "mixed_50_full",
        "records": "results/hybrid_api_pilot50_allcand_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "perspective_gpt54_full",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "perspective_gpt41_full",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "partial_observability_full",
        "records": "results/partial_observability_api50_records.jsonl",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
    },
    {
        "label": "mixed_50_no_coord",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
            "oracle": "no_coord_oracle",
        },
    },
    {
        "label": "perspective_gpt41_no_coord",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
            "oracle": "no_coord_oracle",
        },
    },
    {
        "label": "partial_observability_no_coord",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "methods": {
            "direct": "no_coord_direct_first",
            "shortest": "no_coord_best_of_k_shortest",
            "mirror": "no_coord_mirror",
            "population": "no_coord_population",
            "consensus+info": "no_coord_consensus_info",
            "info prior": "no_coord_informative",
            "oracle": "no_coord_oracle",
        },
    },
]

CODED_FAILURES = [
    {
        "label": "perspective_alt_model_mirror",
        "path": "results/perspective_stress50_gpt41nano_mirror_failures_coded.csv",
    },
    {
        "label": "partial_observability_mirror",
        "path": "results/partial_observability_api50_mirror_failures_coded.csv",
    },
    {
        "label": "partial_observability_no_coord_mirror",
        "path": "results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
    },
]

COLORS = {"red", "green", "blue", "yellow", "purple", "orange"}
SIZES = {"small", "large"}
SHAPE_SYNONYMS = {
    "sphere": {"sphere", "spheres", "ball", "balls"},
    "cube": {"cube", "cubes", "block", "blocks"},
    "cylinder": {"cylinder", "cylinders"},
    "cone": {"cone", "cones"},
    "pyramid": {"pyramid", "pyramids"},
}
FRAME_RE = re.compile(r"\b(left|right|leftmost|rightmost)\b", re.IGNORECASE)
ROW_RES = [
    re.compile(r"\brow\s+(\d+)\b", re.IGNORECASE),
    re.compile(r"\b(\d+)(?:st|nd|rd|th)?\s+row\b", re.IGNORECASE),
]
COL_RES = [
    re.compile(r"\bcol(?:umn)?\s+(\d+)\b", re.IGNORECASE),
    re.compile(r"\b(\d+)(?:st|nd|rd|th)?\s+col(?:umn)?\b", re.IGNORECASE),
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rule-based, non-LLM ambiguity verifier for selected PRAG-CrossPlay messages."
    )
    parser.add_argument("--markdown-out", default="docs/rule_based_ambiguity_verifier.md")
    parser.add_argument("--json-out", default="results/rule_based_ambiguity_verifier.json")
    parser.add_argument("--units-out", default="results/rule_based_ambiguity_verifier_units.jsonl")
    args = parser.parse_args()

    scenes = load_scenes(SCENE_FILES)
    units = []
    runs = []
    for spec in RUNS:
        run, run_units = analyze_run(spec, scenes)
        runs.append(run)
        units.extend(run_units)
    coded = analyze_coded_failures(scenes)
    report = {
        "description": "Cache-only symbolic verifier over selected messages. It parses target color/size/shape mentions, exact row/column mentions, and left/right frame-sensitive cues.",
        "runs": runs,
        "coded_taxonomy_alignment": coded,
        "key_findings": key_findings(runs, coded),
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_jsonl(args.units_out, units)
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def load_scenes(paths: list[str]) -> dict[str, Scene]:
    scenes: dict[str, Scene] = {}
    for path in paths:
        for scene in read_scenes(path):
            scenes[scene.scene_id] = scene
    return scenes


def analyze_run(spec: dict[str, Any], scenes: dict[str, Scene]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    records = read_jsonl(spec["records"])
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    method_names = set(spec["methods"].values())
    for row in records:
        if str(row["method"]) in method_names:
            grouped[(str(row["scene_id"]), str(row["method"]))].append(row)

    units = []
    for (scene_id, method), rows in sorted(grouped.items()):
        scene = scenes[scene_id]
        messages = sorted({str(row["message"]) for row in rows})
        if len(messages) != 1:
            raise SystemExit(f"{spec['records']}: multiple messages for {scene_id}/{method}: {messages}")
        verdict = classify_message(messages[0], scene)
        units.append(
            {
                "run": spec["label"],
                "records": spec["records"],
                "scene_id": scene_id,
                "scenario_type": scene.scenario_type,
                "method": method,
                "method_label": label_for_method(spec["methods"], method),
                "message": messages[0],
                "success": mean(float(row["success"]) for row in rows),
                "n_listener_rows": len(rows),
                **verdict,
            }
        )

    by_label = defaultdict(list)
    for unit in units:
        by_label[unit["method_label"]].append(unit)
    method_rows = [summarize_method(label, rows) for label, rows in sorted(by_label.items())]
    return (
        {
            "label": spec["label"],
            "records": spec["records"],
            "n_units": len(units),
            "methods": method_rows,
        },
        units,
    )


def classify_message(message: str, scene: Scene) -> dict[str, Any]:
    target = scene.target()
    visible = scene.listener_objects()
    rows = parse_numbers(message, ROW_RES)
    cols = parse_numbers(message, COL_RES)
    exact_coord = bool(rows and cols)
    coordinate_matches = [
        obj.id
        for obj in visible
        if (not rows or obj.y in rows) and (not cols or obj.x in cols)
    ]
    target_coordinate_match = target.id in coordinate_matches if rows or cols else False

    target_attrs = mentioned_target_attrs(message, target)
    attr_matches = [
        obj.id
        for obj in visible
        if all(getattr(obj, attr) == value for attr, value in target_attrs.items())
    ]
    orientation_shift = scene.speaker_orientation != scene.listener_orientation
    frame_sensitive = (
        bool(FRAME_RE.search(message))
        and not exact_coord
        and (scene.scenario_type == "perspective_shift" or orientation_shift)
    )

    if exact_coord and coordinate_matches == [target.id]:
        label = "coordinate_specific"
    elif frame_sensitive:
        label = "frame_sensitive_relation"
    elif target_attrs and len(attr_matches) > 1:
        label = "attribute_underspecified"
    elif target_attrs and attr_matches == [target.id]:
        label = "attribute_unique"
    elif exact_coord:
        label = "coordinate_mismatch_or_partial"
    else:
        label = "unparsed_or_relational"

    return {
        "verifier_label": label,
        "symbolic_ambiguity_flag": label in {"attribute_underspecified", "frame_sensitive_relation"},
        "attribute_underspecified_flag": label == "attribute_underspecified",
        "frame_sensitive_flag": label == "frame_sensitive_relation",
        "target_attrs_mentioned": sorted(target_attrs),
        "attribute_match_count": len(attr_matches) if target_attrs else None,
        "attribute_match_ids": attr_matches if target_attrs else [],
        "row_mentions": sorted(rows),
        "column_mentions": sorted(cols),
        "coordinate_match_count": len(coordinate_matches) if rows or cols else None,
        "coordinate_match_ids": coordinate_matches if rows or cols else [],
        "target_coordinate_match": target_coordinate_match,
        "orientation_shift": orientation_shift,
    }


def mentioned_target_attrs(message: str, target: SceneObject) -> dict[str, str]:
    msg = message.lower()
    attrs: dict[str, str] = {}
    if word_present(msg, target.size):
        attrs["size"] = target.size
    if word_present(msg, target.color):
        attrs["color"] = target.color
    if any(word_present(msg, term) for term in SHAPE_SYNONYMS[target.shape]):
        attrs["shape"] = target.shape
    return attrs


def parse_numbers(message: str, regexes: list[re.Pattern[str]]) -> set[int]:
    out = set()
    for regex in regexes:
        for match in regex.finditer(message):
            out.add(int(match.group(1)))
    return out


def word_present(text: str, word: str) -> bool:
    return bool(re.search(rf"\b{re.escape(word)}\b", text, flags=re.IGNORECASE))


def label_for_method(methods: dict[str, str], method_name: str) -> str:
    for label, name in methods.items():
        if name == method_name:
            return label
    return method_name


def summarize_method(label: str, units: list[dict[str, Any]]) -> dict[str, Any]:
    failures = [unit for unit in units if float(unit["success"]) < 1.0]
    return {
        "method_label": label,
        "n_scenes": len(units),
        "mean_success": mean(float(unit["success"]) for unit in units),
        "failure_scenes": len(failures),
        "symbolic_ambiguity_rate": rate(units, "symbolic_ambiguity_flag"),
        "attribute_underspecified_rate": rate(units, "attribute_underspecified_flag"),
        "frame_sensitive_rate": rate(units, "frame_sensitive_flag"),
        "failure_symbolic_ambiguity_rate": rate(failures, "symbolic_ambiguity_flag") if failures else None,
        "failure_attribute_underspecified_rate": rate(failures, "attribute_underspecified_flag") if failures else None,
        "failure_frame_sensitive_rate": rate(failures, "frame_sensitive_flag") if failures else None,
        "label_counts": count_labels(units),
    }


def rate(rows: list[dict[str, Any]], key: str) -> float:
    return mean(1.0 if row[key] else 0.0 for row in rows)


def count_labels(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        label = str(row["verifier_label"])
        counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items()))


def analyze_coded_failures(scenes: dict[str, Scene]) -> dict[str, Any]:
    rows = []
    by_set = []
    for spec in CODED_FAILURES:
        with Path(spec["path"]).open(newline="", encoding="utf-8") as f:
            set_rows = []
            for row in csv.DictReader(f):
                verdict = classify_message(row["message"], scenes[row["scene_id"]])
                out = {**row, "failure_set": spec["label"], **verdict}
                rows.append(out)
                set_rows.append(out)
        by_set.append(summarize_coded_set(spec["label"], spec["path"], set_rows))
    return {
        "failure_sets": by_set,
        "combined": summarize_coded_set("combined", ";".join(spec["path"] for spec in CODED_FAILURES), rows),
    }


def summarize_coded_set(label: str, source: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    underspecified = [row for row in rows if row["author_category"] == "underspecified_distractor"]
    frame = [row for row in rows if row["author_category"] == "perspective_frame_error"]
    predicted_under = [row for row in rows if row["attribute_underspecified_flag"]]
    true_under = [row for row in predicted_under if row["author_category"] == "underspecified_distractor"]
    predicted_symbolic = [row for row in rows if row["symbolic_ambiguity_flag"]]
    true_symbolic = [
        row
        for row in predicted_symbolic
        if row["author_category"] in {"underspecified_distractor", "perspective_frame_error"}
    ]
    return {
        "label": label,
        "source": source,
        "n_rows": len(rows),
        "n_underspecified_distractor": len(underspecified),
        "n_perspective_frame_error": len(frame),
        "attribute_underspecified_predictions": len(predicted_under),
        "symbolic_ambiguity_predictions": len(predicted_symbolic),
        "underspecified_precision": len(true_under) / len(predicted_under) if predicted_under else None,
        "underspecified_recall": (
            sum(1 for row in underspecified if row["attribute_underspecified_flag"]) / len(underspecified)
            if underspecified
            else None
        ),
        "frame_sensitive_recall": (
            sum(1 for row in frame if row["frame_sensitive_flag"]) / len(frame) if frame else None
        ),
        "symbolic_precision": len(true_symbolic) / len(predicted_symbolic) if predicted_symbolic else None,
        "symbolic_recall": (
            sum(
                1
                for row in rows
                if row["author_category"] in {"underspecified_distractor", "perspective_frame_error"}
                and row["symbolic_ambiguity_flag"]
            )
            / sum(
                1
                for row in rows
                if row["author_category"] in {"underspecified_distractor", "perspective_frame_error"}
            )
            if rows
            else None
        ),
        "verifier_label_counts": count_labels(rows),
    }


def key_findings(runs: list[dict[str, Any]], coded: dict[str, Any]) -> dict[str, Any]:
    combined = coded["combined"]
    perspective = next(run for run in runs if run["label"] == "perspective_gpt41_full")
    partial = next(run for run in runs if run["label"] == "partial_observability_full")
    partial_no = next(run for run in runs if run["label"] == "partial_observability_no_coord")
    return {
        "coded_symbolic_recall": combined["symbolic_recall"],
        "coded_underspecified_recall": combined["underspecified_recall"],
        "coded_frame_sensitive_recall": combined["frame_sensitive_recall"],
        "perspective_mirror_failure_symbolic_rate": method_row(perspective, "mirror")[
            "failure_symbolic_ambiguity_rate"
        ],
        "perspective_population_symbolic_rate": method_row(perspective, "population")[
            "symbolic_ambiguity_rate"
        ],
        "partial_mirror_failure_symbolic_rate": method_row(partial, "mirror")[
            "failure_symbolic_ambiguity_rate"
        ],
        "partial_population_symbolic_rate": method_row(partial, "population")[
            "symbolic_ambiguity_rate"
        ],
        "partial_no_coord_mirror_failure_symbolic_rate": method_row(partial_no, "mirror")[
            "failure_symbolic_ambiguity_rate"
        ],
        "partial_no_coord_consensus_symbolic_rate": method_row(partial_no, "consensus+info")[
            "symbolic_ambiguity_rate"
        ],
    }


def method_row(run: dict[str, Any], label: str) -> dict[str, Any]:
    for row in run["methods"]:
        if row["method_label"] == label:
            return row
    raise KeyError(label)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Rule-Based Ambiguity Verifier",
        "",
        "This cache-only verifier is an independent non-LLM check on whether selected messages are objectively under-informative or frame-sensitive. It parses exact row/column mentions, target color/size/shape mentions, and left/right frame-sensitive cues, then counts compatible listener-visible objects.",
        "",
        "## Coded Failure Alignment",
        "",
        "| Failure set | Rows | Under-spec recall | Frame recall | Symbolic recall | Under-spec precision | Label counts |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in report["coded_taxonomy_alignment"]["failure_sets"] + [
        report["coded_taxonomy_alignment"]["combined"]
    ]:
        lines.append(
            "| {label} | {n_rows} | {under_recall} | {frame_recall} | {symbolic_recall} | {under_precision} | {counts} |".format(
                label=row["label"],
                n_rows=row["n_rows"],
                under_recall=fmt_optional(row["underspecified_recall"]),
                frame_recall=fmt_optional(row["frame_sensitive_recall"]),
                symbolic_recall=fmt_optional(row["symbolic_recall"]),
                under_precision=fmt_optional(row["underspecified_precision"]),
                counts=", ".join(f"{k}: {v}" for k, v in row["verifier_label_counts"].items()),
            )
        )

    lines.extend(
        [
            "",
            "## Selected-Message Audit",
            "",
            "| Run | Method | Success | Failure scenes | Symbolic flag | Under-spec flag | Frame flag | Failure symbolic flag |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for run in report["runs"]:
        for row in run["methods"]:
            if row["method_label"] not in {"direct", "shortest", "mirror", "population", "consensus+info", "oracle"}:
                continue
            lines.append(
                "| {run} | {method} | {success} | {failures} | {symbolic} | {under} | {frame} | {failure_symbolic} |".format(
                    run=run["label"],
                    method=row["method_label"],
                    success=fmt(row["mean_success"]),
                    failures=row["failure_scenes"],
                    symbolic=fmt(row["symbolic_ambiguity_rate"]),
                    under=fmt(row["attribute_underspecified_rate"]),
                    frame=fmt(row["frame_sensitive_rate"]),
                    failure_symbolic=fmt_optional(row["failure_symbolic_ambiguity_rate"]),
                )
            )

    findings = report["key_findings"]
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- On the combined coded failure set, symbolic ambiguity recall is {fmt(findings['coded_symbolic_recall'])}; attribute-under-specification recall is {fmt(findings['coded_underspecified_recall'])}; and frame-sensitive recall is {fmt_optional(findings['coded_frame_sensitive_recall'])}.",
            f"- In the alternate-model perspective run, the verifier flags {fmt(findings['perspective_mirror_failure_symbolic_rate'])} of mirror failure scenes while flagging {fmt(findings['perspective_population_symbolic_rate'])} of population messages.",
            f"- In partial observability, it flags {fmt(findings['partial_mirror_failure_symbolic_rate'])} of mirror failure scenes while flagging {fmt(findings['partial_population_symbolic_rate'])} of population messages.",
            f"- In no-coordinate partial observability, it flags {fmt(findings['partial_no_coord_mirror_failure_symbolic_rate'])} of mirror failure scenes while flagging {fmt(findings['partial_no_coord_consensus_symbolic_rate'])} of consensus+info messages.",
            "",
            "The result supports the paper's qualitative interpretation without using another LLM listener: the coded mirror failures are predictable from visible object ambiguity or frame-sensitive left/right language alone. The verifier is deliberately conservative for no-coordinate messages: it ignores relational repairs, so successful consensus+info messages can still be flagged when their color/size/shape words alone match multiple listener-visible objects.",
        ]
    )
    return "\n".join(lines) + "\n"


def fmt(value: float) -> str:
    return f"{value:.3f}"


def fmt_optional(value: float | None) -> str:
    return "-" if value is None else fmt(value)


if __name__ == "__main__":
    main()
