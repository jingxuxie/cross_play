#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = [
    "Introduction",
    "Related Work",
    "PRAG-CrossPlay Task",
    "Methods",
    "Experiments",
    "Results",
    "Qualitative Analysis",
    "Limitations",
    "Conclusion",
]

REQUIRED_ARTIFACTS = [
    "paper/main.tex",
    "paper/main.pdf",
    "paper/colm2026_submission.tex",
    "paper/colm2026_submission.pdf",
    "paper/colm2026_conference.sty",
    "paper/colm2026_conference.bst",
    "paper/references.bib",
    "docs/protocol_and_prompts.md",
    "docs/artifact_guide.md",
    "docs/api_token_accounting.md",
    "docs/cross_model_listener_audit.md",
    "docs/local_benchmark600_check.md",
    "docs/local_stronger_plan_k8.md",
    "docs/api_listener_leave_one_out.md",
    "docs/selection_regret_audit.md",
    "docs/candidate_pool_audit.md",
    "docs/candidate_budget_audit.md",
    "docs/candidate_role_selection_audit.md",
    "docs/random_candidate_baseline.md",
    "docs/message_length_audit.md",
    "docs/listener_disagreement_audit.md",
    "docs/listener_confidence_audit.md",
    "docs/failure_taxonomy_audit.md",
    "docs/interaction_memory_rules.md",
    "docs/qualitative_failure_examples.md",
    "docs/reviewer_checklist.md",
    "docs/plan_coverage_audit.md",
    "docs/paper_claims_iteration_002.md",
    "docs/partial_observability_local_check.md",
    "docs/partial_observability_api50_check.md",
    "results/paper_claims_verification.json",
    "results/benchmark_integrity_audit.json",
    "results/api_token_accounting.json",
    "results/cross_model_listener_audit.json",
    "results/local_benchmark600_check.json",
    "results/local_benchmark600_summary.json",
    "results/local_benchmark600_records.jsonl",
    "data/local_benchmark600_scenes.jsonl",
    "results/local_stronger_plan_k8.json",
    "data/local_stronger_plan1200_scenes.jsonl",
    "results/api_listener_leave_one_out.json",
    "results/selection_regret_audit.json",
    "results/candidate_pool_audit.json",
    "results/candidate_budget_audit.json",
    "results/candidate_role_selection_audit.json",
    "results/random_candidate_baseline.json",
    "results/message_length_audit.json",
    "results/listener_disagreement_audit.json",
    "results/listener_confidence_audit.json",
    "results/failure_taxonomy_audit.json",
    "results/interaction_memory_rules.json",
    "results/qualitative_failure_examples.json",
    "results/reviewer_checklist.json",
    "results/plan_coverage_audit.json",
    "results/partial_observability_api50_check.json",
    "results/partial_observability_api50_mirror_failures_coded.csv",
    "results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
    "scripts/export_colm_submission.py",
    "scripts/analyze_api_token_accounting.py",
    "scripts/run_selected_listener_audit.py",
    "scripts/analyze_cross_model_listener_audit.py",
    "scripts/analyze_local_benchmark.py",
    "scripts/analyze_local_stronger_plan.py",
    "scripts/analyze_partial_observability_api.py",
    "scripts/make_artifact_guide.py",
    "scripts/analyze_api_listener_leave_one_out.py",
    "scripts/analyze_selection_regret.py",
    "scripts/analyze_candidate_pool.py",
    "scripts/analyze_candidate_budget.py",
    "scripts/analyze_candidate_role_selection.py",
    "scripts/analyze_random_candidate_baseline.py",
    "scripts/analyze_message_length_audit.py",
    "scripts/analyze_listener_disagreement.py",
    "scripts/analyze_listener_confidence_audit.py",
    "scripts/analyze_failure_taxonomy.py",
    "scripts/analyze_interaction_memory_rules.py",
    "scripts/make_qualitative_examples.py",
    "scripts/make_reviewer_checklist.py",
    "scripts/audit_plan_coverage.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper", default="paper/main.tex")
    parser.add_argument("--pdf", default="paper/main.pdf")
    parser.add_argument("--markdown-out", default="results/submission_readiness_audit.md")
    parser.add_argument("--json-out", default="results/submission_readiness_audit.json")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    actions: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    paper_path = Path(args.paper)
    paper = read_tex_with_inputs(paper_path) if paper_path.exists() else ""

    check_required_artifacts(checks)
    check_pdf(checks, warnings, Path(args.pdf))
    check_paper_structure(checks, paper)
    check_artifact_guide(checks)
    check_claim_verifiers(checks)
    check_template_status(checks, actions, paper)
    check_colm_submission(checks, warnings)
    check_claim_discipline(checks, paper)

    report = {
        "n_checks": len(checks),
        "n_failed": sum(1 for check in checks if check["status"] == "FAIL"),
        "n_warn": sum(1 for check in checks if check["status"] == "WARN") + len(warnings),
        "n_actions": len(actions),
        "checks": checks,
        "warnings": warnings,
        "actions": actions,
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown_report(report), encoding="utf-8")
    print(markdown_report(report))
    if report["n_failed"]:
        raise SystemExit(1)


def check_required_artifacts(checks: list[dict[str, Any]]) -> None:
    for path in REQUIRED_ARTIFACTS:
        add_check(
            checks,
            f"artifact.{path}",
            "PASS" if Path(path).exists() else "FAIL",
            "present" if Path(path).exists() else "missing",
        )


def check_pdf(checks: list[dict[str, Any]], warnings: list[dict[str, str]], pdf_path: Path) -> None:
    if not pdf_path.exists():
        add_check(checks, "pdf.exists", "FAIL", str(pdf_path))
        return
    info = pdfinfo(pdf_path)
    if not info:
        warnings.append({"name": "pdfinfo.available", "detail": "could not read PDF metadata with pdfinfo"})
        return
    pages = int(info.get("Pages", "0"))
    add_check(checks, "pdf.pages_positive", "PASS" if pages > 0 else "FAIL", str(pages))
    add_check(
        checks,
        "pdf.pages_within_workshop_range",
        "PASS" if 4 <= pages <= 8 else "WARN",
        f"{pages} pages; target plan is 4-8 pages",
    )
    encrypted = info.get("Encrypted", "unknown")
    add_check(checks, "pdf.not_encrypted", "PASS" if encrypted == "no" else "WARN", encrypted)


def pdfinfo(pdf_path: Path) -> dict[str, str]:
    try:
        proc = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError:
        return {}
    if proc.returncode != 0:
        return {}
    out: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            out[key.strip()] = value.strip()
    return out


def check_paper_structure(checks: list[dict[str, Any]], paper: str) -> None:
    add_check(checks, "paper.has_abstract", "PASS" if "\\begin{abstract}" in paper else "FAIL", "abstract environment")
    for section in REQUIRED_SECTIONS:
        add_check(
            checks,
            f"paper.section.{section}",
            "PASS" if f"\\section{{{section}}}" in paper else "FAIL",
            "present" if f"\\section{{{section}}}" in paper else "missing",
        )
    table_refs = len(re.findall(r"\\begin\{table\}", paper))
    figure_refs = len(re.findall(r"\\begin\{figure\}", paper))
    add_check(
        checks,
        "paper.tables",
        "PASS" if table_refs >= 2 else "WARN",
        f"{table_refs} main-text table environments; detailed tables are artifact-linked",
    )
    add_check(checks, "paper.figures", "PASS" if figure_refs >= 1 else "WARN", f"{figure_refs} figure environments")
    bib_entries = len(re.findall(r"^@", Path("paper/references.bib").read_text(encoding="utf-8"), flags=re.M))
    add_check(checks, "paper.references", "PASS" if bib_entries >= 6 else "WARN", f"{bib_entries} bibliography entries")


def check_artifact_guide(checks: list[dict[str, Any]]) -> None:
    path = Path("docs/artifact_guide.md")
    if not path.exists():
        add_check(checks, "artifact_guide.exists", "FAIL", "missing")
        return
    text = path.read_text(encoding="utf-8")
    required = [
        "# PRAG-CrossPlay Artifact Guide",
        "## Dataset Cards",
        "## Claim-To-Evidence Map",
        "API Token Accounting",
        "Cross-Model Held-Out Listener Audit",
        "Population-play is 1.000 in all cross-model rows",
        "GPT-5.5 rows reuse cached speaker candidates and evaluate selected messages only",
        "Local Benchmark-Scale Sanity Check",
        "Local Stronger-Plan K=8 Diagnostic",
        "600 local scenes balanced across four initial scenario families",
        "No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8",
        "No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8",
        "At K=8 without exact coordinates, consensus+info reaches 0.992 on the initial 1,000 scenes and 0.997 on partial-observability scenes",
        "API Listener Leave-One-Out Mechanism Check",
        "Selection Regret Audit",
        "Candidate Pool Robustness Audit",
        "Candidate Budget Audit",
        "Candidate Role Selection Audit",
        "Random Candidate Baseline",
        "Message Length Audit",
        "Listener Disagreement Audit",
        "Listener Confidence Audit",
        "Failure Taxonomy Audit",
        "Interaction Memory Rule Audit",
        "Qualitative Failure Examples",
        "Reviewer Checklist",
        "Plan Coverage Audit",
        "full-candidate population-play has zero regret",
        "population-play selects a robust candidate in 1.000 of scenes",
        "alternate-model perspective robust-scene coverage rises from 0.380 at K=1 to 1.000 at K=4",
        "Full-candidate population coordinate-fallback rates: mixed_50_full=0.420, perspective_gpt54_full=1.000, perspective_gpt41_full=1.000, partial_observability_full=1.000",
        "No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000",
        "population-play improves over random by 0.135, 0.285, 0.343, and 0.247",
        "consensus+info improves over random by 0.100, 0.218, and 0.316",
        "full-candidate population selected messages average 6.82, 10.22, 10.22, and 9.66 tokens",
        "mirror split-outcome rates are 0.080, 0.180, 0.360, and 0.500",
        "alternate-model perspective ambiguity flags are 0.000 while mirror high-confidence failure rates are 0.147 and 0.280",
        "147 of 152 coded listener-level mirror failures are underspecified-distractor cases",
        "Coded failure rows: 152; unique failure scenes: 76",
        "repair cue satisfies derived rule in 1.000 of failure scenes",
        "four cache-only examples show mirror-selected messages failing held-out listeners",
        "Section 32 reviewer checklist passes all 19 core-validity, results, and paper items",
        "Items passed: 19/19",
        "Core scope: 17 covered, 2 partial, 0 open.",
        "Stretch scope: 1 covered, 3 partial, 1 open.",
        "stretch scope has 1 covered, 3 partial, 1 open and keeps human validation open",
        "partial_observability_api50",
        "cache-only API listener leave-one-out improves population over mirror",
        "0 candidate messages reference private landmarks",
        "all 50 full-run mirror failures are underspecified-distractor choices",
        "local_benchmark600 | `data/local_benchmark600_scenes.jsonl` | 600 | 10800",
        "194/194 integrity checks pass",
        "4982 cached responses have complete usage metadata totaling 1410092 tokens",
    ]
    for snippet in required:
        add_check(
            checks,
            f"artifact_guide.{slug(snippet)}",
            "PASS" if snippet in text else "FAIL",
            "present" if snippet in text else "missing",
        )


def check_claim_verifiers(checks: list[dict[str, Any]]) -> None:
    verifier_path = Path("results/paper_claims_verification.json")
    if verifier_path.exists():
        verifier = json.loads(verifier_path.read_text(encoding="utf-8"))
        add_check(
            checks,
            "claims_verifier.no_failed_checks",
            "PASS" if verifier.get("n_failed") == 0 else "FAIL",
            f"{verifier.get('n_checks', '?')} checks, {verifier.get('n_failed', '?')} failed",
        )
    else:
        add_check(checks, "claims_verifier.no_failed_checks", "FAIL", "missing verifier JSON")

    integrity_path = Path("results/benchmark_integrity_audit.json")
    if integrity_path.exists():
        integrity = json.loads(integrity_path.read_text(encoding="utf-8"))
        add_check(
            checks,
            "integrity_audit.no_failed_checks",
            "PASS" if integrity.get("n_failed") == 0 else "FAIL",
            f"{integrity.get('n_checks', '?')} checks, {integrity.get('n_failed', '?')} failed",
        )
    else:
        add_check(checks, "integrity_audit.no_failed_checks", "FAIL", "missing integrity audit JSON")


def check_template_status(checks: list[dict[str, Any]], actions: list[dict[str, str]], paper: str) -> None:
    colm_source = Path("paper/colm2026_submission.tex")
    colm_pdf = Path("paper/colm2026_submission.pdf")
    colm_text = colm_source.read_text(encoding="utf-8") if colm_source.exists() else ""
    has_colm_submission = (
        colm_pdf.exists()
        and r"\usepackage[submission]{colm2026_conference}" in colm_text
        and r"\bibliographystyle{colm2026_conference}" in colm_text
    )
    if not has_colm_submission:
        uses_article = bool(re.search(r"\\documentclass(?:\[[^\]]+\])?\{article\}", paper))
        detail = "generic article class" if uses_article else "missing generated COLM submission target"
        add_check(checks, "template.final_venue_template", "WARN", detail)
        actions.append(
            {
                "name": "Generate COLM submission target",
                "detail": "Run scripts/export_colm_submission.py and compile paper/colm2026_submission.tex before submission.",
            }
        )
    else:
        add_check(checks, "template.final_venue_template", "PASS", "paper/colm2026_submission.pdf uses COLM submission style")


def check_colm_submission(checks: list[dict[str, Any]], warnings: list[dict[str, str]]) -> None:
    source = Path("paper/colm2026_submission.tex")
    pdf = Path("paper/colm2026_submission.pdf")
    if not source.exists():
        add_check(checks, "colm_source.exists", "FAIL", str(source))
        return
    text = source.read_text(encoding="utf-8")
    add_check(
        checks,
        "colm_source.uses_submission_template",
        "PASS" if r"\usepackage[submission]{colm2026_conference}" in text else "FAIL",
        "COLM submission package",
    )
    add_check(
        checks,
        "colm_source.has_line_numbers",
        "PASS" if r"\ifcolmsubmission" in text and r"\linenumbers" in text else "FAIL",
        "line numbers enabled for submission mode",
    )
    add_check(
        checks,
        "colm_source.uses_colm_bibliography_style",
        "PASS" if r"\bibliographystyle{colm2026_conference}" in text else "FAIL",
        "COLM bibliography style",
    )
    if not pdf.exists():
        add_check(checks, "colm_pdf.exists", "FAIL", str(pdf))
        return
    info = pdfinfo(pdf)
    if not info:
        warnings.append({"name": "colm_pdfinfo.available", "detail": "could not read COLM PDF metadata with pdfinfo"})
        return
    pages = int(info.get("Pages", "0"))
    add_check(checks, "colm_pdf.pages_positive", "PASS" if pages > 0 else "FAIL", str(pages))
    add_check(
        checks,
        "colm_pdf.pages_within_submission_range",
        "PASS" if 4 <= pages <= 9 else "WARN",
        f"{pages} pages; target submission range is 4-9 pages",
    )
    encrypted = info.get("Encrypted", "unknown")
    add_check(checks, "colm_pdf.not_encrypted", "PASS" if encrypted == "no" else "WARN", encrypted)


def check_claim_discipline(checks: list[dict[str, Any]], paper: str) -> None:
    required_phrases = [
        "The current experiments are intentionally small and diagnostic",
        "The held-out listeners are API language models, not humans",
        "The strongest population-play result relies on exact coordinate fallbacks",
        "broader claims require larger balanced runs",
    ]
    for phrase in required_phrases:
        add_check(
            checks,
            f"claims.limitation.{slug(phrase)}",
            "PASS" if contains_phrase(paper, phrase) else "WARN",
            "present" if contains_phrase(paper, phrase) else "missing",
        )


def read_tex_with_inputs(path: Path, seen: set[Path] | None = None) -> str:
    """Read a TeX file and inline local \input{...} targets for text checks."""
    seen = set() if seen is None else seen
    resolved = path.resolve()
    if resolved in seen or not path.exists():
        return ""
    seen.add(resolved)
    text = path.read_text(encoding="utf-8")

    def replace_input(match: re.Match[str]) -> str:
        raw = match.group(1)
        child = (path.parent / raw).with_suffix(".tex")
        if not child.exists():
            child = path.parent / raw
        return read_tex_with_inputs(child, seen)

    return re.sub(r"\\input\{([^}]+)\}", replace_input, text)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:60]


def contains_phrase(text: str, phrase: str) -> bool:
    compact_text = re.sub(r"\s+", " ", text)
    compact_phrase = re.sub(r"\s+", " ", phrase)
    return compact_phrase in compact_text


def add_check(checks: list[dict[str, Any]], name: str, status: str, detail: str) -> None:
    checks.append({"name": name, "status": status, "detail": detail})


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Submission Readiness Audit",
        "",
        f"Checks: {report['n_checks'] - report['n_failed']}/{report['n_checks']} non-failing.",
        f"Warnings: {report['n_warn']}.",
        f"Open actions: {report['n_actions']}.",
        "",
    ]
    if report["actions"]:
        lines.extend(["## Open Actions", ""])
        for action in report["actions"]:
            lines.append(f"- **{action['name']}**: {action['detail']}")
        lines.append("")
    if report["warnings"]:
        lines.extend(["## Tool Warnings", ""])
        for warning in report["warnings"]:
            lines.append(f"- `{warning['name']}`: {warning['detail']}")
        lines.append("")
    lines.extend(
        [
            "## Checks",
            "",
            "| Status | Check | Detail |",
            "|---|---|---|",
        ]
    )
    for check in report["checks"]:
        lines.append(f"| {check['status']} | `{check['name']}` | {check['detail']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
