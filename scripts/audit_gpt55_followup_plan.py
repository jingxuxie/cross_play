#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PLAN_PATH = "additional_experiments_gpt55_plan.md"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit current artifacts against the GPT-5.5 follow-up experiment plan."
    )
    parser.add_argument("--json-out", default="results/gpt55_followup_plan_status.json")
    parser.add_argument("--markdown-out", default="docs/gpt55_followup_plan_status.md")
    args = parser.parse_args()

    report = build_report()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def build_report() -> dict[str, Any]:
    items = [
        item(
            "exp1_gpt55_listener_audit",
            "Experiment 1: GPT-5.5 held-out listener audit",
            "covered",
            [
                "results/cross_model_listener_audit.json",
                "docs/cross_model_listener_audit.md",
                "results/gpt55_perspective_selected_records.jsonl",
                "results/gpt55_partial_observability_selected_records.jsonl",
            ],
            "Fifty-scene perspective-stress and partial-observability selected-message audits include GPT-5.5 listeners, paired population-minus-mirror gaps, and cross-model context.",
        ),
        item(
            "exp2_cross_model_matrix",
            "Experiment 2: cross-model listener matrix",
            "covered",
            [
                "results/cross_model_listener_audit.json",
                "paper/tables/cross_model_listener_audit.tex",
                "docs/cross_model_failure_overlap.md",
            ],
            "The artifact has gpt-4.1-nano, gpt-5.4-nano, and gpt-5.5 listener-family rows for perspective stress and partial observability, plus failure-overlap diagnostics.",
        ),
        item(
            "exp3_gpt55_speaker_generation",
            "Experiment 3: GPT-5.5 speaker candidate-generation audit",
            "covered",
            [
                "results/gpt55_speaker_smoke.json",
                "docs/gpt55_speaker_smoke_report.md",
                "results/gpt55_speaker_perspective10_candidates.jsonl",
                "results/gpt55_speaker_perspective20_candidates.jsonl",
                "results/gpt55_speaker_perspective20_records.jsonl",
                "results/gpt55_speaker_perspective20_candidate_eval_records.jsonl",
                "results/gpt55_speaker_perspective50_candidates.jsonl",
                "results/gpt55_speaker_perspective50_records.jsonl",
                "results/gpt55_speaker_perspective50_candidate_eval_records.jsonl",
            ],
            "The original same-10-scene smoke shows GPT-5.5 speaker direct-first improves from 0.800 to 1.000 and mirror from 0.667 to 0.867, while population stays 1.000. The full 50-scene perspective-stress speaker audit has direct-first 0.993, mirror 0.853 despite same-play 1.000, population 1.000, and oracle 1.000 under GPT-5.5 held-out listeners.",
        ),
        item(
            "exp4_k8_no_coordinate_generation",
            "Experiment 4: stronger no-coordinate candidate generation",
            "partial",
            [
                "results/local_stronger_plan_k8.json",
                "docs/local_stronger_plan_k8.md",
                "docs/candidate_budget_audit.md",
            ],
            "The no-API local K=8 diagnostic supports the candidate-diversity explanation, but the cached API speaker artifacts remain K=4.",
        ),
        item(
            "exp5_human_validation",
            "Experiment 5: small human validation",
            "partial",
            [
                "data/human_validation_items.jsonl",
                "data/human_validation_response_template.csv",
                "docs/human_validation_packet.md",
                "docs/rule_based_ambiguity_verifier.md",
                "results/human_validation_answer_key.json",
            ],
            "The 20-item participant-safe annotation packet and response template are prepared, but no human annotations are present. The current completed independent support remains the rule-based ambiguity verifier.",
        ),
        item(
            "exp6_rule_based_verifier",
            "Experiment 6: rule-based ambiguity verifier",
            "covered",
            [
                "results/rule_based_ambiguity_verifier.json",
                "docs/rule_based_ambiguity_verifier.md",
                "results/rule_based_ambiguity_verifier_units.jsonl",
            ],
            "The rule-based verifier recovers the coded mirror-failure taxonomy with symbolic ambiguity, attribute-under-specification, and frame-sensitive recall all at 1.000.",
        ),
    ]
    return {
        "plan": PLAN_PATH,
        "summary": summarize(items),
        "items": items,
        "paper_claim_boundary": [
            "Safe to claim: the mirror gap persists under GPT-5.5 held-out listeners, and the cross-model matrix supports the core cross-play argument.",
            "Safe to claim: the 50-scene GPT-5.5 speaker audit shows stronger speakers reduce first-candidate brittleness but do not remove the value of population selection.",
            "Not yet safe as paper headline: API K=8 no-coordinate generation or human listener validation.",
        ],
        "next_best_steps": [
            "If API budget allows, run API K=8 no-coordinate candidate generation for the perspective-stress scenes.",
            "Collect three annotations per item from the prepared 20-scene human validation packet before making human-alignment claims.",
            "Keep the current K=8 no-coordinate evidence framed as local diagnostic support unless an API K=8 run is added.",
        ],
    }


def item(
    key: str,
    title: str,
    status: str,
    evidence_paths: list[str],
    interpretation: str,
) -> dict[str, Any]:
    return {
        "key": key,
        "title": title,
        "status": status,
        "evidence": [
            {"path": path, "present": Path(path).exists()}
            for path in evidence_paths
        ],
        "interpretation": interpretation,
    }


def summarize(items: list[dict[str, Any]]) -> dict[str, int]:
    statuses = {status: 0 for status in ["covered", "partial", "future"]}
    for row in items:
        statuses[row["status"]] += 1
    statuses["total"] = len(items)
    statuses["missing_evidence_paths"] = sum(
        1
        for row in items
        for evidence in row["evidence"]
        if not evidence["present"]
    )
    return statuses


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# GPT-5.5 Follow-Up Plan Status",
        "",
        f"Plan source: `{report['plan']}`.",
        "",
        "This generated audit maps the additional GPT-5.5 experiment plan to current artifacts. It is a claim-boundary document: covered rows can support paper claims, partial rows should stay auxiliary, and future rows should not be claimed as completed.",
        "",
        "## Summary",
        "",
        f"Covered: {summary['covered']}. Partial: {summary['partial']}. Future: {summary['future']}. Missing evidence paths: {summary['missing_evidence_paths']}.",
        "",
        "| Status | Experiment | Evidence | Interpretation |",
        "|---|---|---|---|",
    ]
    for row in report["items"]:
        evidence = ", ".join(
            f"`{entry['path']}`" if entry["present"] else f"`{entry['path']}` missing"
            for entry in row["evidence"]
        )
        lines.append(
            f"| {row['status']} | {row['title']} | {evidence} | {row['interpretation']} |"
        )

    lines.extend(["", "## Claim Boundary", ""])
    lines.extend(f"- {line}" for line in report["paper_claim_boundary"])
    lines.extend(["", "## Next Best Steps", ""])
    lines.extend(f"- {line}" for line in report["next_best_steps"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
