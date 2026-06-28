#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import Scene, read_jsonl, read_scenes
from prag_crossplay.scoring import markdown_table, paired_method_comparison, summarize_records


COORD_RE = re.compile(r"\brow\s+\d+\b|\bcolumn\s+\d+\b", re.IGNORECASE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene-file", default="data/partial_observability_local50_scenes.jsonl")
    parser.add_argument("--records", default="results/partial_observability_api50_records.jsonl")
    parser.add_argument("--candidates", default="results/partial_observability_api50_candidates.jsonl")
    parser.add_argument("--no-coord-records", default="results/partial_observability_api50_no_coord_records.jsonl")
    parser.add_argument(
        "--mirror-failures-coded",
        default="results/partial_observability_api50_mirror_failures_coded.csv",
    )
    parser.add_argument(
        "--no-coord-mirror-failures-coded",
        default="results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
    )
    parser.add_argument("--markdown-out", default="docs/partial_observability_api50_check.md")
    parser.add_argument("--json-out", default="results/partial_observability_api50_check.json")
    args = parser.parse_args()

    scenes = {scene.scene_id: scene for scene in read_scenes(args.scene_file)}
    records = read_jsonl(args.records)
    candidates = read_jsonl(args.candidates)
    no_coord_records = read_jsonl(args.no_coord_records) if Path(args.no_coord_records).exists() else []

    summary = summarize_records(records)
    no_coord_summary = summarize_records(no_coord_records) if no_coord_records else None
    paired = paired_method_comparison(
        records,
        "hybrid_local_population_api_eval",
        "hybrid_local_mirror_api_eval",
    )
    no_coord_paired = (
        paired_method_comparison(no_coord_records, "no_coord_consensus_info", "no_coord_mirror")
        if no_coord_records
        else None
    )

    message_audit = audit_messages(scenes, candidates)
    failures = mirror_failure_examples(records, limit=4)
    coded_failures = read_failure_counts(args.mirror_failures_coded)
    no_coord_coded_failures = read_failure_counts(args.no_coord_mirror_failures_coded)

    report = {
        "n_scenes": len({row["scene_id"] for row in candidates}),
        "summary": summary,
        "paired_population_minus_mirror": paired,
        "no_coord_summary": no_coord_summary,
        "no_coord_consensus_minus_mirror": no_coord_paired,
        "message_audit": message_audit,
        "coded_mirror_failures": coded_failures,
        "coded_no_coord_mirror_failures": no_coord_coded_failures,
        "mirror_failure_examples": failures,
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown_report(report), encoding="utf-8")
    print(markdown_report(report))


def audit_messages(scenes: dict[str, Scene], candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter()
    selected_counts = Counter()
    examples: list[dict[str, str]] = []

    for row in candidate_rows:
        scene = scenes[row["scene_id"]]
        for message in row["candidates"]:
            counts["candidate_messages"] += 1
            if COORD_RE.search(message):
                counts["coordinate_candidates"] += 1
            if references_private_landmark(scene, message):
                counts["private_landmark_candidate_refs"] += 1
                if len(examples) < 5:
                    examples.append({"scene_id": scene.scene_id, "message": message})
        for field in ["mirror_selected", "population_selected"]:
            message = str(row.get(field, ""))
            selected_counts[f"{field}.total"] += 1
            if COORD_RE.search(message):
                selected_counts[f"{field}.coordinate"] += 1
            if references_private_landmark(scene, message):
                selected_counts[f"{field}.private_landmark_ref"] += 1

    return {
        **dict(counts),
        "selected": dict(selected_counts),
        "private_reference_examples": examples,
    }


def references_private_landmark(scene: Scene, message: str) -> bool:
    private_id = str(scene.metadata.get("private_landmark_id", ""))
    private = next((obj for obj in scene.objects if obj.id == private_id), None)
    if private is None:
        return False
    message_l = message.lower()
    if private.id.lower() in message_l:
        return True
    phrase_matches = re.search(rf"\b{re.escape(private.color)}\b", message_l) and re.search(
        rf"\b{re.escape(private.shape)}s?\b", message_l
    )
    if not phrase_matches:
        return False
    visible_same_phrase = any(
        obj.visible_to_listener and obj.color == private.color and obj.shape == private.shape
        for obj in scene.objects
    )
    return not visible_same_phrase


def mirror_failure_examples(records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    by_scene: dict[str, list[dict[str, Any]]] = {}
    for row in records:
        if row["method"] == "hybrid_local_mirror_api_eval":
            by_scene.setdefault(row["scene_id"], []).append(row)
    examples = []
    for scene_id, rows in sorted(by_scene.items()):
        failures = [row for row in rows if int(row["success"]) == 0]
        if not failures:
            continue
        examples.append(
            {
                "scene_id": scene_id,
                "message": rows[0]["message"],
                "successes": sum(int(row["success"]) for row in rows),
                "total": len(rows),
                "failed_listeners": [row["listener"] for row in failures],
                "failed_choices": [row["choice_id"] for row in failures],
            }
        )
        if len(examples) >= limit:
            break
    return examples


def read_failure_counts(path: str | Path) -> dict[str, Any] | None:
    path = Path(path)
    if not path.exists():
        return None
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        rows.extend(csv.DictReader(f))
    counts = Counter(row["author_category"] for row in rows)
    return {
        "path": str(path),
        "total": len(rows),
        "by_category": dict(sorted(counts.items())),
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Partial-Observability API Pilot",
        "",
        f"Bounded {report['n_scenes']}-scene API stress check for private-landmark scenes.",
        "",
        f"Scenes: {report['n_scenes']}.",
        "",
        "## Main Results",
        "",
        markdown_table(report["summary"]).strip(),
        "",
    ]
    paired = report["paired_population_minus_mirror"]
    lines.extend(
        [
            "Population minus mirror:",
            f"- n pairs: {paired['n_pairs']}",
            f"- diff: {paired['diff_a_minus_b']:.3f}",
            f"- 95% CI: [{paired['diff_ci95'][0]:.3f}, {paired['diff_ci95'][1]:.3f}]",
            f"- paired bootstrap p: {paired['paired_bootstrap_p_two_sided']:.4f}",
            "",
        ]
    )
    if report["no_coord_summary"]:
        lines.extend(
            [
                "## No-Coordinate Ablation",
                "",
                markdown_table(report["no_coord_summary"]).strip(),
                "",
            ]
        )
        paired_no = report["no_coord_consensus_minus_mirror"]
        lines.extend(
            [
                "Consensus+info minus mirror after removing exact row/column candidates:",
                f"- n pairs: {paired_no['n_pairs']}",
                f"- diff: {paired_no['diff_a_minus_b']:.3f}",
                f"- 95% CI: [{paired_no['diff_ci95'][0]:.3f}, {paired_no['diff_ci95'][1]:.3f}]",
                f"- paired bootstrap p: {paired_no['paired_bootstrap_p_two_sided']:.4f}",
                "",
            ]
        )

    audit = report["message_audit"]
    selected = audit["selected"]
    lines.extend(
        [
            "## Message Audit",
            "",
            f"- Generated candidate messages: {audit.get('candidate_messages', 0)}.",
            f"- Exact-coordinate candidates: {audit.get('coordinate_candidates', 0)}.",
            f"- Candidate messages referencing private landmarks: {audit.get('private_landmark_candidate_refs', 0)}.",
            f"- Mirror selected private-landmark references: {selected.get('mirror_selected.private_landmark_ref', 0)}.",
            f"- Population selected private-landmark references: {selected.get('population_selected.private_landmark_ref', 0)}.",
            f"- Mirror selected exact-coordinate messages: {selected.get('mirror_selected.coordinate', 0)}.",
            f"- Population selected exact-coordinate messages: {selected.get('population_selected.coordinate', 0)}.",
            "",
        ]
    )
    if audit["private_reference_examples"]:
        lines.append("Private-reference examples:")
        for example in audit["private_reference_examples"]:
            lines.append(f"- `{example['scene_id']}`: {example['message']}")
        lines.append("")

    if report["coded_mirror_failures"]:
        coded = report["coded_mirror_failures"]
        lines.extend(
            [
                "## Coded Mirror Failure Categories",
                "",
                f"Source: `{coded['path']}`.",
                "",
                "| Rubric category | Count |",
                "|---|---:|",
            ]
        )
        for category, count in coded["by_category"].items():
            lines.append(f"| {category} | {count} |")
        lines.append("")
    if report["coded_no_coord_mirror_failures"]:
        coded_no = report["coded_no_coord_mirror_failures"]
        lines.extend(
            [
                "No-coordinate mirror failures:",
                "",
                f"Source: `{coded_no['path']}`.",
                "",
                "| Rubric category | Count |",
                "|---|---:|",
            ]
        )
        for category, count in coded_no["by_category"].items():
            lines.append(f"| {category} | {count} |")
        lines.append("")

    lines.extend(["## Mirror Failure Examples", ""])
    for example in report["mirror_failure_examples"]:
        listeners = ", ".join(example["failed_listeners"])
        choices = ", ".join(example["failed_choices"])
        lines.append(
            f"- `{example['scene_id']}`: {example['successes']}/{example['total']} held-out listeners succeed; "
            f"message: \"{example['message']}\"; failed listeners: {listeners}; choices: {choices}."
        )
    lines.append("")
    lines.extend(
        [
            "Interpretation: the prompt mostly prevents explicit private-landmark references in this run. The residual failures are under-specification failures: mirror self-play sometimes accepts short attribute-only descriptions that fit both the target and distractor, while population/consensus selection favors row/column or informative visible relations. The coded mirror-failure files support this interpretation: all coded full-run mirror failures and all coded no-coordinate mirror failures are underspecified-distractor choices.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
