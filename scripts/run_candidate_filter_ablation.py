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

from prag_crossplay.data import read_jsonl, read_scenes, write_jsonl
from prag_crossplay.local_agents import training_listeners
from prag_crossplay.methods import (
    score_choice,
    select_mirror_selfplay,
    select_population_play,
    select_shortest,
    token_count,
)
from prag_crossplay.scoring import (
    markdown_table,
    paired_comparison_markdown,
    paired_method_comparison,
    summarize_records,
    write_summary,
)

EXACT_COORD_RE = re.compile(
    r"\brow\s+\d+\b|\bcolumn\s+\d+\b|\b\d+(?:st|nd|rd|th)?\s+row\b|\b\d+(?:st|nd|rd|th)?\s+column\b",
    re.IGNORECASE,
)

METHOD_LABELS = {
    "no_coord_direct_first": "Direct first",
    "no_coord_best_of_k_shortest": "Best-of-K shortest",
    "no_coord_mirror": "Mirror self-play",
    "no_coord_population": "Population-play",
    "no_coord_consensus_info": "Consensus+info",
    "no_coord_informative": "Informativeness prior",
    "no_coord_oracle": "Oracle candidate",
}

METHOD_ORDER = [
    "no_coord_direct_first",
    "no_coord_best_of_k_shortest",
    "no_coord_mirror",
    "no_coord_population",
    "no_coord_consensus_info",
    "no_coord_informative",
    "no_coord_oracle",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Recompute selection after filtering candidate messages, reusing cached "
            "all-candidate held-out listener evaluations. This makes no API calls."
        )
    )
    parser.add_argument("--scene-file", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--candidate-records", required=True)
    parser.add_argument("--records-out", required=True)
    parser.add_argument("--summary-out", required=True)
    parser.add_argument("--markdown-out", required=True)
    parser.add_argument("--paired-json-out", required=True)
    parser.add_argument("--paired-markdown-out", required=True)
    parser.add_argument("--audit-out", default=None)
    parser.add_argument("--table-out", default=None)
    parser.add_argument("--tex-out", default=None)
    parser.add_argument("--scenario-table-out", default=None)
    parser.add_argument("--scenario-tex-out", default=None)
    parser.add_argument(
        "--filter",
        choices=["no_exact_coordinates"],
        default="no_exact_coordinates",
    )
    args = parser.parse_args()

    scenes = {scene.scene_id: scene for scene in read_scenes(args.scene_file)}
    candidate_rows = read_jsonl(args.candidates)
    candidate_eval_rows = read_jsonl(args.candidate_records)
    eval_by_scene_index = _index_candidate_eval_rows(candidate_eval_rows)

    train = training_listeners()
    records: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    skipped = 0
    total_candidates = 0
    kept_candidates = 0

    for candidate_row in candidate_rows:
        scene = scenes[candidate_row["scene_id"]]
        candidates = [str(message) for message in candidate_row["candidates"]]
        kept = [
            (index, message)
            for index, message in enumerate(candidates)
            if keep_candidate(message, args.filter)
        ]
        total_candidates += len(candidates)
        kept_candidates += len(kept)
        if not kept:
            skipped += 1
            continue

        kept_messages = [message for _, message in kept]
        first = {"message": kept_messages[0], "score": None, "choices": []}
        shortest = select_shortest(kept_messages)
        mirror = select_mirror_selfplay(scene, kept_messages, train[0].choose)
        population = select_population_play(scene, kept_messages, [listener.choose for listener in train])
        informative = select_informative(kept)
        consensus_info = select_consensus_else_informative(scene, kept, train)
        oracle = select_oracle_from_cached_eval(scene.scene_id, kept, eval_by_scene_index)

        selections = [
            ("no_coord_direct_first", first, None),
            ("no_coord_best_of_k_shortest", shortest, None),
            ("no_coord_mirror", mirror, sameplay_success(mirror["choices"], scene.target_id)),
            ("no_coord_population", population, sameplay_success(population["choices"], scene.target_id)),
            ("no_coord_consensus_info", consensus_info, None),
            ("no_coord_informative", informative, None),
            ("no_coord_oracle", oracle, None),
        ]
        for method, selection, sameplay in selections:
            original_index = selected_original_index(kept, str(selection["message"]))
            records.extend(
                copy_selected_eval_rows(
                    eval_by_scene_index[(scene.scene_id, original_index)],
                    method=method,
                    sameplay=sameplay,
                    filter_name=args.filter,
                    source_candidate_index=original_index,
                    candidate_pool_size=len(kept),
                    excluded_candidate_count=len(candidates) - len(kept),
                )
            )

        audit_rows.append(
            {
                "scene_id": scene.scene_id,
                "scenario_type": scene.scenario_type,
                "filter": args.filter,
                "original_candidate_count": len(candidates),
                "kept_candidate_count": len(kept),
                "kept_candidate_indices": [index for index, _ in kept],
                "kept_candidates": kept_messages,
                "mirror_selected": mirror["message"],
                "mirror_local_choices": [choice.__dict__ for choice in mirror["choices"]],
                "population_selected": population["message"],
                "population_local_choices": [choice.__dict__ for choice in population["choices"]],
                "consensus_info_selected": consensus_info["message"],
                "consensus_info_source": consensus_info["source"],
                "consensus_info_local_choices": [
                    choice.__dict__ for choice in consensus_info["choices"]
                ],
                "informative_selected": informative["message"],
                "oracle_selected": oracle["message"],
            }
        )

    write_jsonl(args.records_out, records)
    if args.audit_out:
        write_jsonl(args.audit_out, audit_rows)

    summary = summarize_records(records)
    summary["candidate_filter"] = {
        "name": args.filter,
        "skipped_scenes": skipped,
        "total_scenes": len(candidate_rows),
        "total_candidates": total_candidates,
        "kept_candidates": kept_candidates,
        "excluded_candidates": total_candidates - kept_candidates,
    }
    write_summary(args.summary_out, summary)
    markdown = ablation_markdown(summary, records)
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown, encoding="utf-8")

    comparisons = [
        paired_method_comparison(
            records,
            "no_coord_population",
            "no_coord_mirror",
            scenario_type=None,
        ),
        paired_method_comparison(
            records,
            "no_coord_population",
            "no_coord_mirror",
            scenario_type="perspective_shift",
        ),
    ]
    Path(args.paired_json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.paired_json_out).write_text(
        json.dumps(comparisons, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    Path(args.paired_markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.paired_markdown_out).write_text(
        paired_comparison_markdown(comparisons),
        encoding="utf-8",
    )

    if args.table_out:
        Path(args.table_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.table_out).write_text(ablation_table_markdown(summary), encoding="utf-8")
    if args.tex_out:
        Path(args.tex_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.tex_out).write_text(ablation_table_tex(summary), encoding="utf-8")
    if args.scenario_table_out:
        Path(args.scenario_table_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.scenario_table_out).write_text(scenario_table_markdown(summary), encoding="utf-8")
    if args.scenario_tex_out:
        Path(args.scenario_tex_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.scenario_tex_out).write_text(scenario_table_tex(summary), encoding="utf-8")

    print(markdown)


def keep_candidate(message: str, filter_name: str) -> bool:
    if filter_name == "no_exact_coordinates":
        return not EXACT_COORD_RE.search(message)
    raise ValueError(f"unknown filter {filter_name}")


def _index_candidate_eval_rows(rows: list[dict[str, Any]]) -> dict[tuple[str, int], list[dict[str, Any]]]:
    indexed: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        indexed[(row["scene_id"], int(row["candidate_index"]))].append(row)
    return dict(indexed)


def sameplay_success(choices: list[Any], target_id: str) -> float:
    return mean(score_choice(choice, target_id) for choice in choices)


def select_oracle_from_cached_eval(
    scene_id: str,
    kept: list[tuple[int, str]],
    eval_by_scene_index: dict[tuple[str, int], list[dict[str, Any]]],
) -> dict[str, Any]:
    def score(item: tuple[int, str]) -> tuple[float, int]:
        index, message = item
        rows = eval_by_scene_index[(scene_id, index)]
        return (mean(float(row["success"]) for row in rows), -token_count(message))

    index, message = max(kept, key=score)
    return {"message": message, "score": score((index, message)), "choices": []}


def select_informative(kept: list[tuple[int, str]]) -> dict[str, Any]:
    _, message = max(
        kept,
        key=lambda item: (
            informativeness_score(item[1]),
            token_count(item[1]),
            item[1],
        ),
    )
    return {"message": message, "score": informativeness_score(message), "choices": []}


def select_consensus_else_informative(
    scene: Any,
    kept: list[tuple[int, str]],
    train: list[Any],
) -> dict[str, Any]:
    scored = []
    for _, message in kept:
        choices = [listener.choose(scene, message) for listener in train]
        local_success = mean(score_choice(choice, scene.target_id) for choice in choices)
        scored.append(
            {
                "message": message,
                "choices": choices,
                "local_success": local_success,
                "informativeness": informativeness_score(message),
                "tokens": token_count(message),
            }
        )
    consensus = [
        row
        for row in scored
        if row["local_success"] >= 1.0
    ]
    if consensus:
        best = max(
            consensus,
            key=lambda row: (
                row["informativeness"],
                -row["tokens"],
                row["message"],
            ),
        )
        return {
            "message": best["message"],
            "score": best["local_success"],
            "choices": best["choices"],
            "source": "consensus",
        }

    best = max(
        scored,
        key=lambda row: (
            row["informativeness"],
            row["tokens"],
            row["message"],
        ),
    )
    return {
        "message": best["message"],
        "score": best["informativeness"],
        "choices": best["choices"],
        "source": "informativeness_fallback",
    }


def informativeness_score(message: str) -> int:
    text = message.lower()
    patterns = [
        r"\bonly\b|\bunique\b",
        r"\bleftmost\b|\brightmost\b|\bfarthest\b|\bclosest\b",
        r"\bleft\b|\bright\b|\babove\b|\bbelow\b",
        r"\btop\b|\bbottom\b",
        r"\bof the\b|\bnext to\b|\bbeside\b",
        r"\bamong\b|\bbetween\b",
    ]
    return sum(1 for pattern in patterns if re.search(pattern, text))


def selected_original_index(kept: list[tuple[int, str]], message: str) -> int:
    for index, kept_message in kept:
        if kept_message == message:
            return index
    raise KeyError(message)


def copy_selected_eval_rows(
    rows: list[dict[str, Any]],
    *,
    method: str,
    sameplay: float | None,
    filter_name: str,
    source_candidate_index: int,
    candidate_pool_size: int,
    excluded_candidate_count: int,
) -> list[dict[str, Any]]:
    copied = []
    for row in rows:
        out = dict(row)
        out["method"] = method
        out["sameplay_success"] = sameplay
        out["candidate_filter"] = filter_name
        out["source_candidate_index"] = source_candidate_index
        out["candidate_pool_size"] = candidate_pool_size
        out["excluded_candidate_count"] = excluded_candidate_count
        copied.append(out)
    return copied


def ablation_markdown(summary: dict[str, Any], records: list[dict[str, Any]]) -> str:
    filt = summary["candidate_filter"]
    return (
        "# Candidate Filter Ablation\n\n"
        f"Filter: `{filt['name']}`.\n\n"
        f"- Scenes: `{filt['total_scenes']}` total, `{filt['skipped_scenes']}` skipped.\n"
        f"- Candidates: `{filt['kept_candidates']}` kept, `{filt['excluded_candidates']}` excluded.\n\n"
        + markdown_table(summary)
    )


def ablation_table_markdown(summary: dict[str, Any]) -> str:
    rows = [
        "| Method | Cross-play | Same-play | Gap | Mean tokens |",
        "|---|---:|---:|---:|---:|",
    ]
    for method in METHOD_ORDER:
        stats = summary["by_method"][method]
        rows.append(
            "| {label} | {cross:.3f} | {same} | {gap} | {tokens:.1f} |".format(
                label=METHOD_LABELS[method],
                cross=stats["success"],
                same=fmt(stats.get("sameplay_success")),
                gap=fmt(stats.get("crossplay_gap")),
                tokens=stats["mean_tokens"],
            )
        )
    return "\n".join(rows) + "\n"


def ablation_table_tex(summary: dict[str, Any]) -> str:
    rows = [
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Method & Cross-play & Same-play & Gap & Tokens \\\\",
        "\\midrule",
    ]
    for method in METHOD_ORDER:
        stats = summary["by_method"][method]
        rows.append(
            "{label} & {cross:.3f} & {same} & {gap} & {tokens:.1f} \\\\".format(
                label=METHOD_LABELS[method],
                cross=stats["success"],
                same=fmt(stats.get("sameplay_success")),
                gap=fmt(stats.get("crossplay_gap")),
                tokens=stats["mean_tokens"],
            )
        )
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def scenario_table_markdown(summary: dict[str, Any]) -> str:
    rows = [
        "| Scenario | " + " | ".join(METHOD_LABELS[method] for method in METHOD_ORDER) + " |",
        "|---|" + "|".join(["---:"] * len(METHOD_ORDER)) + "|",
    ]
    for scenario, by_method in sorted(summary["by_scenario_method"].items()):
        cells = []
        for method in METHOD_ORDER:
            stats = by_method.get(method)
            cells.append("-" if stats is None else f"{stats['success']:.3f}")
        rows.append(f"| {pretty_scenario(scenario)} | " + " | ".join(cells) + " |")
    return "\n".join(rows) + "\n"


def scenario_table_tex(summary: dict[str, Any]) -> str:
    rows = [
        "\\begin{tabular}{lrrrrrrr}",
        "\\toprule",
        "Scenario & Direct & Shortest & Mirror & Population & Cons.+info & Info prior & Oracle \\\\",
        "\\midrule",
    ]
    for scenario, by_method in sorted(summary["by_scenario_method"].items()):
        cells = []
        for method in METHOD_ORDER:
            stats = by_method.get(method)
            cells.append("-" if stats is None else f"{stats['success']:.3f}")
        rows.append(f"{pretty_scenario(scenario)} & " + " & ".join(cells) + " \\\\")
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def pretty_scenario(scenario: str) -> str:
    return scenario.replace("_", " ")


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    main()
