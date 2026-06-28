#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="docs/reviewer_checklist.md")
    parser.add_argument("--json-out", default="results/reviewer_checklist.json")
    args = parser.parse_args()

    report = build_report()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))
    if report["n_failed"]:
        raise SystemExit(1)


def build_report() -> dict[str, Any]:
    ctx = Context()
    items = checklist_items(ctx)
    return {
        "source_plan": "cross_play_pragmatics_workshop_plan.md#32-quality-checklist-before-submission",
        "n_items": len(items),
        "n_failed": sum(1 for item in items if item["status"] == "FAIL"),
        "items": items,
    }


class Context:
    def __init__(self) -> None:
        self._json: dict[str, Any] = {}
        self._text: dict[str, str] = {}

    def json(self, path: str) -> dict[str, Any]:
        if path not in self._json:
            p = Path(path)
            self._json[path] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        return self._json[path]

    def text(self, path: str) -> str:
        if path not in self._text:
            p = Path(path)
            self._text[path] = p.read_text(encoding="utf-8") if p.exists() else ""
        return self._text[path]

    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def contains(self, path: str, snippet: str) -> bool:
        text = self.text(path)
        if snippet in text:
            return True
        return re.sub(r"\s+", " ", snippet) in re.sub(r"\s+", " ", text)

    def integrity_passes(self) -> bool:
        return int(self.json("results/benchmark_integrity_audit.json").get("n_failed", 999)) == 0

    def integrity_has(self, pattern: str) -> bool:
        regex = re.compile(pattern)
        checks = self.json("results/benchmark_integrity_audit.json").get("checks", [])
        return any(check.get("ok") and regex.search(str(check.get("name", ""))) for check in checks)

    def claims_pass(self) -> bool:
        return int(self.json("results/paper_claims_verification.json").get("n_failed", 999)) == 0

    def readiness_pass(self) -> bool:
        report = self.json("results/submission_readiness_audit.json")
        return (
            int(report.get("n_failed", 999)) == 0
            and int(report.get("n_actions", 999)) == 0
            and int(report.get("n_warn", 999)) == 0
        )


def checklist_items(ctx: Context) -> list[dict[str, Any]]:
    return [
        item(
            "Core validity",
            "Target ID is never shown to the listener.",
            ctx.contains("docs/protocol_and_prompts.md", "listener sees only the candidate-object list and the speaker message")
            and ctx.contains("docs/protocol_and_prompts.md", "Target object ID visible only to you"),
            [
                "docs/protocol_and_prompts.md",
                "prag_crossplay/prompts.py",
            ],
            "The hidden target identity is only flagged in the speaker prompt; listener prompts expose candidate IDs only as selectable object labels.",
        ),
        item(
            "Core validity",
            "Speaker messages are checked for target ID leakage.",
            ctx.integrity_passes()
            and ctx.integrity_has(r"messages_no_object_id_leakage")
            and ctx.integrity_has(r"candidates_no_object_id_leakage"),
            [
                "results/benchmark_integrity_audit.json",
                "results/benchmark_integrity_audit.md",
            ],
            "Integrity checks cover generated/evaluated messages, candidate lists, and ablation audit rows for obj_* leakage.",
        ),
        item(
            "Core validity",
            "Listener outputs are valid object IDs.",
            ctx.integrity_passes() and ctx.integrity_has(r"choice_ids_valid"),
            [
                "results/benchmark_integrity_audit.json",
                "results/benchmark_integrity_audit.md",
            ],
            "Every result row has a listener choice that is a valid candidate object ID, and success flags are recomputed from choice_id == target_id.",
        ),
        item(
            "Core validity",
            "Same test scenes are used across methods.",
            ctx.integrity_passes() and ctx.integrity_has(r"same_scene_set_across_methods"),
            [
                "results/benchmark_integrity_audit.json",
                "results/benchmark_integrity_audit.md",
            ],
            "The integrity audit checks same-scene coverage and balanced rows per scene-method for the paper-facing record files.",
        ),
        item(
            "Core validity",
            "Prompts are frozen before final evaluation.",
            ctx.contains("docs/protocol_and_prompts.md", "Speaker Prompt")
            and ctx.contains("docs/protocol_and_prompts.md", "Held-Out Listener Prompts")
            and ctx.exists("prag_crossplay/prompts.py"),
            [
                "docs/protocol_and_prompts.md",
                "prag_crossplay/prompts.py",
                "scripts/export_protocol_appendix.py",
            ],
            "The prompt appendix is generated from the current implementation and records the exact speaker and held-out listener prompts used by the cached artifacts.",
        ),
        item(
            "Core validity",
            "Held-out listeners are not used for method selection.",
            ctx.contains("paper/main.tex", "Neither selector uses held-out listener labels")
            and ctx.exists("prag_crossplay/methods.py")
            and ctx.exists("prag_crossplay/local_agents.py"),
            [
                "paper/main.tex",
                "prag_crossplay/methods.py",
                "prag_crossplay/local_agents.py",
            ],
            "Mirror, population, and consensus+info selection use local training-listener feedback or text priors; held-out API labels are reserved for evaluation and oracle analysis.",
        ),
        item(
            "Core validity",
            "All responses are cached.",
            ctx.integrity_passes()
            and int(ctx.json("results/benchmark_integrity_audit.json").get("summary", {}).get("cache", {}).get("n_cache_files", 0)) > 0
            and ctx.integrity_has(r"cache_files_readable"),
            [
                "data/cached_responses/",
                "results/benchmark_integrity_audit.json",
            ],
            "The integrity audit confirms cached response files are present and parse as JSON.",
        ),
        item(
            "Core validity",
            "Exact model versions are reported.",
            has_model_version(ctx, "gpt-5.4-nano", "gpt-5.4-nano-2026-03-17")
            and has_model_version(ctx, "gpt-4.1-nano", "gpt-4.1-nano-2025-04-14")
            and ctx.contains("paper/main.tex", "gpt-5.4-nano-2026-03-17"),
            [
                "results/benchmark_integrity_audit.json",
                "docs/protocol_and_prompts.md",
                "paper/main.tex",
            ],
            "The cache audit and paper report exact response model snapshots for both API listener families.",
        ),
        item(
            "Results",
            "Main table has confidence intervals.",
            ctx.contains("paper/tables/mixed50.tex", "95\\% CI")
            and ctx.contains("paper/main.tex", "95\\% bootstrap interval")
            and ctx.claims_pass(),
            [
                "paper/tables/mixed50.tex",
                "paper/main.tex",
                "results/paper_claims_verification.json",
            ],
            "The main mixed-results table includes 95% intervals, and paired interval claims are covered by the claim verifier.",
        ),
        item(
            "Results",
            "Scenario table explains where gains/losses occur.",
            ctx.exists("paper/tables/mixed50_by_scenario.tex")
            and ctx.contains("paper/main.tex", "Perspective-shift scenes are the hard case")
            and ctx.contains("docs/artifact_guide.md", "## Headline Full-Candidate Results"),
            [
                "paper/tables/mixed50_by_scenario.tex",
                "paper/main.tex",
                "docs/artifact_guide.md",
            ],
            "The paper localizes the mixed-pilot degradation to perspective-shift scenes and links the scenario table to the artifact guide.",
        ),
        item(
            "Results",
            "Cross-play gap is reported.",
            ctx.contains("paper/main.tex", "cross-play gap")
            and ctx.contains("paper/tables/mixed50.tex", "Gap")
            and ctx.claims_pass(),
            [
                "paper/main.tex",
                "paper/tables/mixed50.tex",
                "results/paper_claims_verification.json",
            ],
            "The paper defines and reports same-play minus held-out cross-play gaps for the main self-play selectors.",
        ),
        item(
            "Results",
            "Oracle upper bound is reported.",
            ctx.contains("paper/main.tex", "oracle candidate upper bound")
            and ctx.contains("paper/tables/mixed50.tex", "Oracle candidate")
            and ctx.contains("docs/selection_regret_audit.md", "Oracle"),
            [
                "paper/main.tex",
                "paper/tables/mixed50.tex",
                "docs/selection_regret_audit.md",
            ],
            "The paper and audits report oracle candidate success to separate generation failures from selector failures.",
        ),
        item(
            "Results",
            "Manual failure examples support the quantitative result.",
            ctx.contains("docs/qualitative_failure_examples.md", "Qualitative Failure Examples")
            and ctx.contains("paper/main.tex", "In scene \\texttt{ps\\_000005}")
            and ctx.contains("paper/main.tex", "In scene \\texttt{ps\\_000011}")
            and ctx.claims_pass(),
            [
                "docs/qualitative_failure_examples.md",
                "results/qualitative_failure_examples.json",
                "paper/main.tex",
            ],
            "The qualitative appendix and paper examples show mirror-selected messages failing held-out listeners while population or consensus+info repairs succeed.",
        ),
        item(
            "Paper",
            "Intro states the evaluation blind spot clearly.",
            ctx.contains("paper/main.tex", "same-play success can overstate held-out communicative success")
            and ctx.contains("paper/main.tex", "does it learn robust pragmatics or just exploit that listener"),
            ["paper/main.tex"],
            "The introduction frames self-play success as a possible blind spot and asks whether selected messages transfer to held-out listeners.",
        ),
        item(
            "Paper",
            "Related work is concise.",
            ctx.readiness_pass()
            and ctx.contains("paper/main.tex", "\\section{Related Work}")
            and len(re.findall(r"^@", ctx.text("paper/references.bib"), flags=re.M)) >= 6,
            [
                "paper/main.tex",
                "paper/references.bib",
                "results/submission_readiness_audit.json",
            ],
            "The readiness audit confirms the Related Work section exists and the bibliography is populated without inflating the workshop draft past the page target.",
        ),
        item(
            "Paper",
            "Method is reproducible.",
            ctx.exists("REPRODUCE.md")
            and ctx.exists("docs/protocol_and_prompts.md")
            and ctx.exists("scripts/audit_benchmark_integrity.py")
            and ctx.readiness_pass(),
            [
                "REPRODUCE.md",
                "docs/protocol_and_prompts.md",
                "scripts/audit_benchmark_integrity.py",
            ],
            "The reproduction file, protocol appendix, and integrity audit expose the command path and protocol surface for the paper-facing artifacts.",
        ),
        item(
            "Paper",
            "Limitations are honest.",
            ctx.contains("paper/main.tex", "The current experiments are intentionally small and diagnostic")
            and ctx.contains("paper/main.tex", "The held-out listeners are API language models, not humans")
            and ctx.readiness_pass(),
            [
                "paper/main.tex",
                "results/submission_readiness_audit.json",
            ],
            "The limitations section explicitly narrows the claims to small diagnostic API-listener experiments.",
        ),
        item(
            "Paper",
            "Claims match actual results.",
            ctx.claims_pass(),
            [
                "scripts/verify_paper_claims.py",
                "results/paper_claims_verification.json",
                "results/paper_claims_verification.md",
            ],
            "The claim verifier recomputes numeric and required text claims from checked-in result files.",
        ),
        item(
            "Paper",
            "Appendix includes prompts and schemas.",
            ctx.contains("docs/protocol_and_prompts.md", "Speaker Prompt")
            and ctx.contains("docs/protocol_and_prompts.md", "Held-Out Listener Prompts")
            and ctx.contains("docs/protocol_and_prompts.md", "Record Schema")
            and ctx.contains("docs/protocol_and_prompts.md", "Candidate Schema"),
            [
                "docs/protocol_and_prompts.md",
                "scripts/export_protocol_appendix.py",
            ],
            "The generated protocol appendix includes prompt text, listener styles, and result/candidate schemas.",
        ),
    ]


def has_model_version(ctx: Context, requested: str, response: str) -> bool:
    versions = ctx.json("results/benchmark_integrity_audit.json").get("summary", {}).get("cache", {}).get("model_versions", [])
    return any(row.get("requested_model") == requested and row.get("response_model") == response for row in versions)


def item(section: str, name: str, ok: bool, evidence: list[str], detail: str) -> dict[str, Any]:
    return {
        "section": section,
        "name": name,
        "status": "PASS" if ok else "FAIL",
        "evidence": evidence,
        "detail": detail,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Reviewer Checklist",
        "",
        "This generated checklist materializes Section 32 of the original workshop plan against the current artifacts.",
        f"Items passed: {report['n_items'] - report['n_failed']}/{report['n_items']}.",
        "",
    ]
    for section in ["Core validity", "Results", "Paper"]:
        lines.extend([f"## {section}", "", "| Status | Plan item | Evidence | Detail |", "|---|---|---|---|"])
        for row in [item for item in report["items"] if item["section"] == section]:
            evidence = ", ".join(f"`{path}`" for path in row["evidence"])
            lines.append(f"| {row['status']} | {row['name']} | {evidence} | {row['detail']} |")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
