#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl
from prag_crossplay.scoring import paired_method_comparison


SOURCES = [
    {
        "label": "existing_gpt54_speaker",
        "description": "Existing perspective-stress speaker candidates evaluated with GPT-5.5 listeners on the first 10 scenes.",
        "records": "results/gpt55_existing_speaker_perspective10_records.jsonl",
        "summary": "results/gpt55_existing_speaker_perspective10_summary.json",
        "candidates": "results/perspective_stress50_hybrid_candidates.jsonl",
        "candidate_eval_records": "results/gpt55_existing_speaker_perspective10_candidate_eval_records.jsonl",
        "audit": "results/gpt55_existing_speaker_perspective10_audit.jsonl",
        "speaker_model": "gpt-5.4-nano",
        "listener_model": "gpt-5.5",
    },
    {
        "label": "gpt55_speaker",
        "description": "GPT-5.5 speaker candidates evaluated with GPT-5.5 listeners on the same first 10 scenes.",
        "records": "results/gpt55_speaker_perspective10_records.jsonl",
        "summary": "results/gpt55_speaker_perspective10_summary.json",
        "candidates": "results/gpt55_speaker_perspective10_candidates.jsonl",
        "candidate_eval_records": "results/gpt55_speaker_perspective10_candidate_eval_records.jsonl",
        "audit": "results/gpt55_speaker_perspective10_candidates.jsonl",
        "speaker_model": "gpt-5.5",
        "listener_model": "gpt-5.5",
    },
]

PROGRESS_SOURCE = {
    "label": "gpt55_speaker_50scene",
    "description": "GPT-5.5 speaker candidates evaluated with GPT-5.5 listeners on all 50 perspective-stress scenes.",
    "records": "results/gpt55_speaker_perspective50_records.jsonl",
    "summary": "results/gpt55_speaker_perspective50_summary.json",
    "candidates": "results/gpt55_speaker_perspective50_candidates.jsonl",
    "candidate_eval_records": "results/gpt55_speaker_perspective50_candidate_eval_records.jsonl",
    "audit": "results/gpt55_speaker_perspective50_candidates.jsonl",
    "speaker_model": "gpt-5.5",
    "listener_model": "gpt-5.5",
}

METHODS = [
    "api_direct_first",
    "api_best_of_k_shortest",
    "hybrid_local_mirror_api_eval",
    "hybrid_local_population_api_eval",
    "oracle_upper_bound",
    "template",
]

ROLE_LABELS = {
    0: "natural_first",
    1: "attribute_short",
    2: "relational_or_spatial",
    3: "coordinate_fallback",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare a bounded GPT-5.5 speaker smoke against existing speaker candidates."
    )
    parser.add_argument("--json-out", default="results/gpt55_speaker_smoke.json")
    parser.add_argument("--markdown-out", default="docs/gpt55_speaker_smoke_report.md")
    args = parser.parse_args()

    sources = [analyze_source(spec) for spec in SOURCES]
    progress_extension = (
        analyze_source(PROGRESS_SOURCE)
        if Path(PROGRESS_SOURCE["records"]).exists()
        and Path(PROGRESS_SOURCE["summary"]).exists()
        and Path(PROGRESS_SOURCE["candidates"]).exists()
        and Path(PROGRESS_SOURCE["candidate_eval_records"]).exists()
        else None
    )
    report = {
        "description": (
            "Bounded 10-scene perspective-stress smoke test for Experiment 3. "
            "It compares existing GPT-5.4-nano speaker candidates with newly generated "
            "GPT-5.5 speaker candidates under the same GPT-5.5 held-out listeners."
        ),
        "sources": sources,
        "progress_extension": progress_extension,
        "comparison": compare_sources(sources),
        "interpretation": (
            "The GPT-5.5 speaker improves direct first-candidate success on this small "
            "sample, but local mirror selection can still select brittle messages. "
            "Population-play remains the robust selector in both candidate pools. The "
            "50-scene extension, when present, is the paper-facing speaker-generation audit."
        ),
    }
    write_json(args.json_out, report)
    write_text(args.markdown_out, render_markdown(report))
    print(render_markdown(report))


def analyze_source(spec: dict[str, str]) -> dict[str, Any]:
    records = read_jsonl(spec["records"])
    summary = json.loads(Path(spec["summary"]).read_text(encoding="utf-8"))
    candidate_rows = read_jsonl(spec["candidates"])[: summary["overall"]["n_scenes"]]
    candidate_eval_records = read_jsonl(spec["candidate_eval_records"])
    method_rows = []
    for method in METHODS:
        if method not in summary["by_method"]:
            continue
        stats = summary["by_method"][method]
        method_rows.append(
            {
                "method": method,
                "success": stats["success"],
                "success_ci95": stats["success_ci95"],
                "sameplay_success": stats.get("sameplay_success"),
                "crossplay_gap": stats.get("crossplay_gap"),
                "mean_tokens": stats["mean_tokens"],
                "failure_scenes": count_failure_scenes(records, method),
            }
        )
    return {
        "label": spec["label"],
        "description": spec["description"],
        "speaker_model": spec["speaker_model"],
        "listener_model": spec["listener_model"],
        "records": spec["records"],
        "summary": spec["summary"],
        "candidates": spec["candidates"],
        "candidate_eval_records": spec["candidate_eval_records"],
        "n_scenes": summary["overall"]["n_scenes"],
        "methods": method_rows,
        "population_minus_mirror": paired_method_comparison(
            records,
            "hybrid_local_population_api_eval",
            "hybrid_local_mirror_api_eval",
            n_boot=5000,
            seed=0,
        ),
        "candidate_budget": candidate_budget(candidate_eval_records),
        "candidate_roles": candidate_roles(candidate_rows),
        "speaker_usage": speaker_usage(candidate_rows),
    }


def compare_sources(sources: list[dict[str, Any]]) -> dict[str, Any]:
    by_label = {source["label"]: source for source in sources}
    existing = by_label["existing_gpt54_speaker"]
    gpt55 = by_label["gpt55_speaker"]
    return {
        "same_scene_count": len(
            set(scene_ids(existing["records"])) & set(scene_ids(gpt55["records"]))
        ),
        "direct_first_gain": method_success(gpt55, "api_direct_first")
        - method_success(existing, "api_direct_first"),
        "mirror_gain": method_success(gpt55, "hybrid_local_mirror_api_eval")
        - method_success(existing, "hybrid_local_mirror_api_eval"),
        "population_gain": method_success(gpt55, "hybrid_local_population_api_eval")
        - method_success(existing, "hybrid_local_population_api_eval"),
        "oracle_gain": method_success(gpt55, "oracle_upper_bound")
        - method_success(existing, "oracle_upper_bound"),
        "gpt55_direct_success": method_success(gpt55, "api_direct_first"),
        "existing_direct_success": method_success(existing, "api_direct_first"),
        "gpt55_mirror_success": method_success(gpt55, "hybrid_local_mirror_api_eval"),
        "existing_mirror_success": method_success(existing, "hybrid_local_mirror_api_eval"),
        "gpt55_population_success": method_success(gpt55, "hybrid_local_population_api_eval"),
        "existing_population_success": method_success(existing, "hybrid_local_population_api_eval"),
    }


def candidate_budget(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_scene_index: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        by_scene_index[str(row["scene_id"])][int(row["candidate_index"])].append(float(row["success"]))
    rows = []
    for k in range(1, 5):
        oracle_success = []
        robust = []
        for by_index in by_scene_index.values():
            means = [
                mean(values)
                for index, values in by_index.items()
                if index < k
            ]
            if not means:
                continue
            oracle_success.append(max(means))
            robust.append(any(value == 1.0 for value in means))
        rows.append(
            {
                "k": k,
                "oracle_success": mean(oracle_success),
                "robust_scene_rate": mean(1.0 if value else 0.0 for value in robust),
            }
        )
    return rows


def candidate_roles(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_role: dict[int, list[str]] = defaultdict(list)
    for row in candidate_rows:
        for index, message in enumerate(row["candidates"][:4]):
            by_role[index].append(str(message))
    rows = []
    for index in range(4):
        messages = by_role[index]
        rows.append(
            {
                "role": ROLE_LABELS[index],
                "candidate_index": index,
                "n_messages": len(messages),
                "mean_tokens": mean(len(message.split()) for message in messages),
                "coordinate_rate": mean(1.0 if exact_coordinate(message) else 0.0 for message in messages),
                "left_right_rate": mean(1.0 if left_right(message) else 0.0 for message in messages),
            }
        )
    return rows


def speaker_usage(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [row for row in candidate_rows if "speaker_usage" in row]
    if not rows:
        return {
            "speaker_calls": 0,
            "uncached_speaker_calls": 0,
            "total_tokens": 0,
            "uncached_total_tokens": 0,
        }
    return {
        "speaker_calls": len(rows),
        "uncached_speaker_calls": sum(1 for row in rows if not row.get("speaker_cached")),
        "total_tokens": sum(int(row.get("speaker_usage", {}).get("total_tokens", 0) or 0) for row in rows),
        "uncached_total_tokens": sum(
            int(row.get("speaker_usage", {}).get("total_tokens", 0) or 0)
            for row in rows
            if not row.get("speaker_cached")
        ),
    }


def scene_ids(records_path: str) -> set[str]:
    return {str(row["scene_id"]) for row in read_jsonl(records_path)}


def method_success(source: dict[str, Any], method: str) -> float:
    for row in source["methods"]:
        if row["method"] == method:
            return float(row["success"])
    raise KeyError(method)


def count_failure_scenes(records: list[dict[str, Any]], method: str) -> int:
    by_scene: dict[str, list[float]] = defaultdict(list)
    for row in records:
        if row["method"] == method:
            by_scene[str(row["scene_id"])].append(float(row["success"]))
    return sum(1 for values in by_scene.values() if mean(values) < 1.0)


def exact_coordinate(message: str) -> bool:
    text = message.lower()
    return bool(re.search(r"\brow\s+\d+\b", text) and re.search(r"\bcol(?:umn)?\s+\d+\b", text))


def left_right(message: str) -> bool:
    return bool(re.search(r"\b(left|right|leftmost|rightmost)\b", message.lower()))


def render_markdown(report: dict[str, Any]) -> str:
    comparison = report["comparison"]
    progress = report.get("progress_extension")
    lines = [
        "# GPT-5.5 Speaker Smoke",
        "",
        "This bounded, cache-backed smoke test compares existing perspective-stress speaker candidates with newly generated GPT-5.5 speaker candidates on the same first 10 scenes, evaluated by GPT-5.5 held-out listener prompts.",
        "",
        "## Key Findings",
        "",
        f"- Existing speaker direct-first success under GPT-5.5 is {fmt(comparison['existing_direct_success'])}; GPT-5.5 speaker direct-first success is {fmt(comparison['gpt55_direct_success'])}.",
        f"- Existing speaker mirror self-play success under GPT-5.5 is {fmt(comparison['existing_mirror_success'])}; GPT-5.5 speaker mirror self-play is {fmt(comparison['gpt55_mirror_success'])}.",
        f"- Population-play and oracle are {fmt(comparison['existing_population_success'])}/{fmt(method_success(label_source(report, 'existing_gpt54_speaker'), 'oracle_upper_bound'))} for existing candidates and {fmt(comparison['gpt55_population_success'])}/{fmt(method_success(label_source(report, 'gpt55_speaker'), 'oracle_upper_bound'))} for GPT-5.5 candidates.",
        "- Interpretation: stronger speaker generation improves the first candidate in this small sample, but mirror selection still leaves a same-play/cross-play gap; population selection remains robust.",
        "",
        "## Method Summary",
        "",
        "| Source | Method | Success | 95% CI | Same-play | Gap | Failure scenes | Mean tokens |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for source in report["sources"]:
        for row in source["methods"]:
            ci = row["success_ci95"]
            lines.append(
                "| {source} | {method} | {success} | [{lo}, {hi}] | {same} | {gap} | {failures} | {tokens} |".format(
                    source=source["label"],
                    method=row["method"],
                    success=fmt(row["success"]),
                    lo=fmt(ci[0]),
                    hi=fmt(ci[1]),
                    same=fmt_optional(row["sameplay_success"]),
                    gap=fmt_optional(row["crossplay_gap"]),
                    failures=row["failure_scenes"],
                    tokens=f"{row['mean_tokens']:.1f}",
                )
            )

    lines.extend(
        [
            "",
            "## Candidate Budget",
            "",
            "| Source | K | Oracle@K | Robust-scene rate |",
            "|---|---:|---:|---:|",
        ]
    )
    for source in report["sources"]:
        for row in source["candidate_budget"]:
            lines.append(
                f"| {source['label']} | {row['k']} | {fmt(row['oracle_success'])} | {fmt(row['robust_scene_rate'])} |"
            )

    lines.extend(
        [
            "",
            "## Candidate Roles",
            "",
            "| Source | Role | Mean tokens | Coordinate rate | Left/right rate |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for source in report["sources"]:
        for row in source["candidate_roles"]:
            lines.append(
                f"| {source['label']} | {row['role']} | {row['mean_tokens']:.1f} | {fmt(row['coordinate_rate'])} | {fmt(row['left_right_rate'])} |"
            )

    if progress:
        is_full = progress["n_scenes"] >= 50
        section_title = "50-Scene Speaker Audit" if is_full else f"{progress['n_scenes']}-Scene Extension"
        scope_note = (
            "A full continuation extends the GPT-5.5 speaker run to all 50 perspective-stress scenes."
            if is_full
            else (
                "A bounded continuation extends the GPT-5.5 speaker run from 10 to "
                f"{progress['n_scenes']} perspective-stress scenes."
            )
        )
        direct = method_success(progress, "api_direct_first")
        shortest = method_success(progress, "api_best_of_k_shortest")
        mirror = method_success(progress, "hybrid_local_mirror_api_eval")
        mirror_same = method_metric(progress, "hybrid_local_mirror_api_eval", "sameplay_success")
        mirror_gap = method_metric(progress, "hybrid_local_mirror_api_eval", "crossplay_gap")
        population = method_success(progress, "hybrid_local_population_api_eval")
        oracle = method_success(progress, "oracle_upper_bound")
        lines.extend(
            [
                "",
                f"## {section_title}",
                "",
                f"{scope_note} It keeps the same candidate-generation prompt, listener prompts, and local selection procedures.",
                "",
                "| Scenes | Direct | Shortest | Mirror | Mirror same-play | Mirror gap | Population | Oracle |",
                "|---:|---:|---:|---:|---:|---:|---:|---:|",
                "| {scenes} | {direct} | {shortest} | {mirror} | {same} | {gap} | {population} | {oracle} |".format(
                    scenes=progress["n_scenes"],
                    direct=fmt(direct),
                    shortest=fmt(shortest),
                    mirror=fmt(mirror),
                    same=fmt_optional(mirror_same),
                    gap=fmt_optional(mirror_gap),
                    population=fmt(population),
                    oracle=fmt(oracle),
                ),
                "",
                "| K | Oracle@K | Robust-scene rate |",
                "|---:|---:|---:|",
            ]
        )
        for row in progress["candidate_budget"]:
            lines.append(
                f"| {row['k']} | {fmt(row['oracle_success'])} | {fmt(row['robust_scene_rate'])} |"
            )
        usage = progress["speaker_usage"]
        lines.extend(
            [
                "",
                "Budget note: the {scenes}-scene extension has {calls} total speaker rows, {uncached} uncached speaker calls, {tokens} recorded speaker tokens, and {uncached_tokens} uncached speaker tokens. Earlier scenes reused the prior cache where available.".format(
                    scenes=progress["n_scenes"],
                    calls=usage["speaker_calls"],
                    uncached=usage["uncached_speaker_calls"],
                    tokens=usage["total_tokens"],
                    uncached_tokens=usage["uncached_total_tokens"],
                ),
                "",
                "Interpretation: on {scenes} scenes, GPT-5.5 direct-first is {direct} and mirror self-play is {mirror} despite same-play {same}; population-play remains {population}. This supports the speaker-generation result at the planned perspective-stress scale.".format(
                    scenes=progress["n_scenes"],
                    direct=fmt(direct),
                    mirror=fmt(mirror),
                    same=fmt_optional(mirror_same),
                    population=fmt(population),
                ),
            ]
        )

    lines.extend(
        [
            "",
            "## Budget Note",
            "",
            f"The GPT-5.5 speaker run made {label_source(report, 'gpt55_speaker')['speaker_usage']['uncached_speaker_calls']} uncached speaker calls over 10 scenes, using {label_source(report, 'gpt55_speaker')['speaker_usage']['total_tokens']} recorded speaker tokens. Listener calls were cache-backed where identical selected-message evaluations already existed; missing candidate evaluations were cached under `data/cached_responses/`.",
            "",
            "The same-scene table remains a smoke comparison; the extension section is the current paper-facing Experiment 3 speaker result when it has 50 scenes.",
        ]
    )
    return "\n".join(lines) + "\n"


def label_source(report: dict[str, Any], label: str) -> dict[str, Any]:
    for source in report["sources"]:
        if source["label"] == label:
            return source
    raise KeyError(label)


def method_metric(source: dict[str, Any], method: str, metric: str) -> float | None:
    for row in source["methods"]:
        if row["method"] == method:
            value = row.get(metric)
            return None if value is None else float(value)
    raise KeyError(method)


def fmt(value: float) -> str:
    return f"{value:.3f}"


def fmt_optional(value: float | None) -> str:
    return "-" if value is None else fmt(value)


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: str, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
