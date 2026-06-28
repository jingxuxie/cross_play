#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Callable


StatusFn = Callable[[], tuple[str, str]]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit current artifacts against the original workshop plan scope."
    )
    parser.add_argument("--markdown-out", default="docs/plan_coverage_audit.md")
    parser.add_argument("--json-out", default="results/plan_coverage_audit.json")
    args = parser.parse_args()

    report = build_report()
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def build_report() -> dict[str, Any]:
    ctx = Context()
    items = [item.evaluate(ctx) for item in plan_items()]
    counts = count_statuses(items)
    core_items = [row for row in items if row["scope"] == "core"]
    stretch_items = [row for row in items if row["scope"] == "stretch"]
    return {
        "source_plan": "cross_play_pragmatics_workshop_plan.md",
        "status_definitions": {
            "covered": "Current artifacts directly satisfy the plan item.",
            "partial": "Current artifacts address the item only at smaller scale, narrower scope, or as diagnostic support.",
            "open": "The item remains future work and is not claimed by the paper.",
        },
        "n_items": len(items),
        "status_counts": counts,
        "core_status_counts": count_statuses(core_items),
        "stretch_status_counts": count_statuses(stretch_items),
        "items": items,
        "open_or_partial": [row for row in items if row["status"] != "covered"],
    }


class Context:
    def __init__(self) -> None:
        self._json: dict[str, Any] = {}
        self._text: dict[str, str] = {}

    def exists(self, path: str) -> bool:
        return Path(path).exists()

    def text(self, path: str) -> str:
        if path not in self._text:
            p = Path(path)
            self._text[path] = p.read_text(encoding="utf-8") if p.exists() else ""
        return self._text[path]

    def paper_text(self) -> str:
        key = "__assembled_paper__"
        if key not in self._text:
            main_path = Path("paper/main.tex")
            paper = main_path.read_text(encoding="utf-8") if main_path.exists() else ""
            base = main_path.parent

            def expand_input(match: re.Match[str]) -> str:
                rel = match.group(1).strip()
                input_path = base / (rel if rel.endswith(".tex") else f"{rel}.tex")
                if not input_path.exists():
                    return match.group(0)
                return "\n" + input_path.read_text(encoding="utf-8") + "\n"

            self._text[key] = re.sub(r"\\input\{([^}]+)\}", expand_input, paper)
        return self._text[key]

    def json(self, path: str) -> dict[str, Any]:
        if path not in self._json:
            p = Path(path)
            self._json[path] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        return self._json[path]

    def contains(self, path: str, snippet: str) -> bool:
        text = self.text(path)
        if snippet in text:
            return True
        return re.sub(r"\s+", " ", snippet) in re.sub(r"\s+", " ", text)

    def contains_paper(self, snippet: str) -> bool:
        text = self.paper_text()
        if snippet in text:
            return True
        return re.sub(r"\s+", " ", snippet) in re.sub(r"\s+", " ", text)

    def git_remote_contains(self, snippet: str) -> bool:
        return snippet in self.text(".git/config")


class PlanItem:
    def __init__(
        self,
        section: str,
        scope: str,
        plan_item: str,
        evidence: list[str],
        check: StatusFn,
    ) -> None:
        self.section = section
        self.scope = scope
        self.plan_item = plan_item
        self.evidence = evidence
        self.check = check

    def evaluate(self, ctx: Context) -> dict[str, Any]:
        status, detail = self.check()
        return {
            "section": self.section,
            "scope": self.scope,
            "plan_item": self.plan_item,
            "status": status,
            "detail": detail,
            "evidence": self.evidence,
        }


def plan_items() -> list[PlanItem]:
    ctx = Context()

    def covered_if(condition: bool, covered_detail: str, fallback: str = "Required evidence is missing.") -> tuple[str, str]:
        return ("covered", covered_detail) if condition else ("open", fallback)

    return [
        PlanItem(
            "Core contribution package",
            "core",
            "Contribution 1: PRAG-CrossPlay benchmark with scene generator, JSONL data, prompt templates, cached outputs, evaluation scripts, figures, and tables.",
            [
                "prag_crossplay/scenes.py",
                "data/local_benchmark600_scenes.jsonl",
                "docs/protocol_and_prompts.md",
                "data/cached_responses/",
                "scripts/audit_benchmark_integrity.py",
                "paper/tables/",
            ],
            lambda: covered_if(
                all(
                    ctx.exists(path)
                    for path in [
                        "prag_crossplay/scenes.py",
                        "data/local_benchmark600_scenes.jsonl",
                        "docs/protocol_and_prompts.md",
                        "scripts/audit_benchmark_integrity.py",
                        "paper/tables/mixed50.tex",
                    ]
                )
                and ctx.json("results/benchmark_integrity_audit.json").get("n_failed") == 0,
                "Benchmark artifacts, prompt appendix, cached-response checks, evaluation scripts, and paper tables are present and integrity-checked.",
            ),
        ),
        PlanItem(
            "Core contribution package",
            "core",
            "Contribution 2: cross-play protocol separates same-play success, cross-play success, and generalization gap.",
            ["paper/main.tex", "paper/tables/mixed50.tex", "docs/artifact_guide.md"],
            lambda: covered_if(
                ctx.contains_paper("same-play success minus held-out cross-play success")
                and ctx.contains("paper/tables/mixed50.tex", "Gap")
                and ctx.contains("docs/artifact_guide.md", "Mirror cross"),
                "Paper and artifact guide report same-play, cross-play, and gap values.",
            ),
        ),
        PlanItem(
            "Core contribution package",
            "core",
            "Contribution 3: empirical diagnosis of partner overfitting.",
            ["paper/main.tex", "results/paper_claims_verification.json", "docs/failure_taxonomy_audit.md"],
            lambda: covered_if(
                ctx.json("results/paper_claims_verification.json").get("n_failed") == 0
                and ctx.contains_paper("Mirror self-play achieves perfect same-partner success but drops under cross-play")
                and ctx.contains("docs/failure_taxonomy_audit.md", "combined | 152 | 147 | 5 | 0"),
                "Claims, mechanism audits, and coded failures support the partner-overfitting diagnosis.",
            ),
        ),
        PlanItem(
            "Task and scenarios",
            "core",
            "Implement the five scenario families, with the first four as the minimum viable paper and partial observability as a stretch condition.",
            ["prag_crossplay/scenes.py", "docs/protocol_and_prompts.md", "data/partial_observability_local50_scenes.jsonl"],
            lambda: covered_if(
                all(
                    token in ctx.text("docs/protocol_and_prompts.md")
                    for token in [
                        "unique_attribute",
                        "distractor_contrast",
                        "relational_reference",
                        "perspective_shift",
                        "partial_observability",
                    ]
                ),
                "All five scenario families are implemented and documented; partial observability is included as a bounded support run.",
            ),
        ),
        PlanItem(
            "Dataset scale",
            "core",
            "Minimum viable benchmark scale: 600 test episodes balanced over four initial scenario families.",
            ["data/local_benchmark600_scenes.jsonl", "results/local_benchmark600_check.json"],
            lambda: covered_if(
                ctx.json("results/local_benchmark600_check.json").get("n_scenes") == 600,
                "A no-API 600-scene balanced local benchmark validates the released generator at the planned scale.",
            ),
        ),
        PlanItem(
            "Dataset scale",
            "core",
            "Use development episodes for debugging prompts and tuning the generator.",
            ["data/dev_scenes.jsonl", "results/hybrid_api_pilot50_allcand_summary.json"],
            lambda: (
                "partial",
                "The project uses a 50-scene dev/API pilot, not the 200 development episodes suggested by the stronger plan.",
            ),
        ),
        PlanItem(
            "Experiments",
            "core",
            "Run the minimum method matrix: template, direct, best-of-K, mirror self-play, population-play, and oracle upper bound.",
            ["results/hybrid_api_pilot50_allcand_summary.json", "results/local_benchmark600_summary.json"],
            lambda: covered_if(
                required_methods_present(ctx, "results/hybrid_api_pilot50_allcand_summary.json")
                and required_methods_present(ctx, "results/local_benchmark600_summary.json", local=True),
                "Minimum method matrix is present in both cached API pilot summaries and the 600-scene local benchmark.",
            ),
        ),
        PlanItem(
            "Experiments",
            "core",
            "Use bounded API runs with cached speaker/listener calls and held-out listener prompts/models.",
            ["data/cached_responses/", "results/api_token_accounting.json", "docs/protocol_and_prompts.md"],
            lambda: covered_if(
                int(ctx.json("results/api_token_accounting.json").get("n_cache_files", 0)) >= 3520
                and ctx.contains("docs/protocol_and_prompts.md", "Held-Out Listener Prompts"),
                "All cached API responses have usage metadata and the held-out listener prompt surface is documented.",
            ),
        ),
        PlanItem(
            "Experiments",
            "core",
            "Evaluate partner shift with held-out listener prompts and at least one alternate held-out model family.",
            ["results/perspective_stress50_gpt41nano_summary.json", "docs/artifact_guide.md"],
            lambda: covered_if(
                ctx.contains("docs/artifact_guide.md", "perspective_stress_50_alt_model")
                and ctx.contains("docs/protocol_and_prompts.md", "gpt-4.1-nano-2025-04-14"),
                "Held-out prompt variants and the alternate gpt-4.1-nano listener audit are documented.",
            ),
        ),
        PlanItem(
            "Experiments",
            "core",
            "Add hard-case diagnostics if results are near ceiling: perspective stress, no-coordinate ablation, and partial observability.",
            [
                "results/perspective_stress50_gpt41nano_no_coord_summary.json",
                "results/partial_observability_api50_check.json",
                "docs/candidate_budget_audit.md",
            ],
            lambda: covered_if(
                ctx.exists("results/perspective_stress50_gpt41nano_no_coord_summary.json")
                and ctx.exists("results/partial_observability_api50_check.json")
                and ctx.contains("docs/candidate_budget_audit.md", "perspective_gpt41_full | 4 | 1.000 | 1.000"),
                "Hard-case diagnostics are present: perspective stress, no-coordinate ablations, candidate-budget audit, and partial observability.",
            ),
        ),
        PlanItem(
            "Metrics and statistics",
            "core",
            "Report objective success, same-play, cross-play, cross-play gap, bootstrap confidence intervals, and paired comparisons.",
            ["paper/main.tex", "paper/tables/mixed50.tex", "results/*_paired.json"],
            lambda: covered_if(
                ctx.contains_paper("95\\% bootstrap interval")
                and ctx.contains("paper/tables/mixed50.tex", "95\\% CI")
                and ctx.contains_paper("cross-play gap"),
                "Objective success, gaps, CIs, and paired comparison claims are reported and verifier-covered.",
            ),
        ),
        PlanItem(
            "Metrics and statistics",
            "core",
            "Analyze robustness across partners and ambiguity/confidence proxies.",
            ["docs/listener_disagreement_audit.md", "docs/listener_confidence_audit.md"],
            lambda: covered_if(
                ctx.contains("docs/listener_disagreement_audit.md", "split outcome")
                and ctx.contains("docs/listener_confidence_audit.md", "High-conf failure"),
                "Listener-disagreement and confidence audits cover partner-robustness and ambiguity/confidence diagnostics.",
            ),
        ),
        PlanItem(
            "Failure analysis",
            "core",
            "Hand-label roughly 100 failures into interpretable categories.",
            [
                "results/perspective_stress50_gpt41nano_mirror_failures_coded.csv",
                "results/partial_observability_api50_mirror_failures_coded.csv",
                "results/partial_observability_api50_no_coord_mirror_failures_coded.csv",
                "docs/failure_taxonomy_audit.md",
            ],
            lambda: (
                "partial",
                "There are 152 author-coded listener-level mirror failures across paper-facing hard cases, but not a balanced 100-failure sample across all major methods.",
            ),
        ),
        PlanItem(
            "Analysis artifacts",
            "core",
            "Separate generation failures from selector failures with oracle upper bound and selection regret.",
            ["docs/selection_regret_audit.md", "docs/candidate_pool_audit.md"],
            lambda: covered_if(
                ctx.exists("results/selection_regret_audit.json")
                and ctx.exists("results/candidate_pool_audit.json")
                and ctx.contains("docs/artifact_guide.md", "Selection Regret Audit")
                and ctx.contains("docs/artifact_guide.md", "Candidate Pool Robustness Audit"),
                "Selection-regret and candidate-pool audits separate missing candidates from selector regret.",
            ),
        ),
        PlanItem(
            "Analysis artifacts",
            "core",
            "Rule out simple explanations such as any candidate would do or longer messages are enough.",
            ["docs/random_candidate_baseline.md", "docs/message_length_audit.md"],
            lambda: covered_if(
                ctx.exists("results/random_candidate_baseline.json")
                and ctx.exists("results/message_length_audit.json")
                and ctx.contains("docs/artifact_guide.md", "Random Candidate Baseline")
                and ctx.contains("docs/artifact_guide.md", "Message Length Audit"),
                "Random-candidate and message-length audits address two simple alternative explanations.",
            ),
        ),
        PlanItem(
            "Analysis artifacts",
            "core",
            "Produce qualitative examples showing mirror failure and population or consensus repair.",
            ["docs/qualitative_failure_examples.md", "results/qualitative_failure_examples.json", "paper/main.tex"],
            lambda: covered_if(
                ctx.contains("docs/qualitative_failure_examples.md", "No-coordinate repair using consensus+info")
                and ctx.contains_paper("In scene \\texttt{ps\\_000005}"),
                "Paper and generated appendix include qualitative mirror-failure and repair examples.",
            ),
        ),
        PlanItem(
            "Paper package",
            "core",
            "Write a 4-8 page workshop paper with intro, related work, task, methods, experiments, results, qualitative analysis, limitations, and conclusion.",
            ["paper/main.tex", "paper/main.pdf", "results/submission_readiness_audit.json"],
            lambda: covered_if(
                ctx.json("results/submission_readiness_audit.json").get("n_failed") == 0
                and ctx.json("results/submission_readiness_audit.json").get("n_actions") == 0,
                "Readiness audit confirms required sections, 8-page PDFs, final-template export, and no open actions.",
            ),
        ),
        PlanItem(
            "Paper package",
            "core",
            "Release a reproducible artifact package with README, protocol appendix, cached outputs, verification scripts, and quality checklist.",
            ["README.md", "REPRODUCE.md", "docs/protocol_and_prompts.md", "docs/reviewer_checklist.md", "docs/artifact_guide.md"],
            lambda: covered_if(
                ctx.exists("README.md")
                and ctx.exists("REPRODUCE.md")
                and ctx.contains("docs/reviewer_checklist.md", "Items passed: 19/19")
                and ctx.contains("docs/artifact_guide.md", "## Quality Gates"),
                "README, reproduction commands, prompt appendix, reviewer checklist, and artifact guide are present.",
            ),
        ),
        PlanItem(
            "Paper package",
            "core",
            "Keep claims conservative and limitations honest.",
            ["paper/main.tex", "docs/paper_claims_iteration_002.md", "results/paper_claims_verification.json"],
            lambda: covered_if(
                ctx.json("results/paper_claims_verification.json").get("n_failed") == 0
                and ctx.contains_paper("The current experiments are intentionally small and diagnostic")
                and ctx.contains("docs/paper_claims_iteration_002.md", "Do not claim"),
                "Claim verifier passes and limitations/conservative-claim notes are explicit.",
            ),
        ),
        PlanItem(
            "Stronger-plan extensions",
            "stretch",
            "Run a 1,000-scene benchmark and 200 partial-observability stress episodes.",
            [
                "cross_play_pragmatics_workshop_plan.md",
                "data/local_stronger_plan1200_scenes.jsonl",
                "docs/local_stronger_plan_k8.md",
                "results/local_stronger_plan_k8.json",
            ],
            lambda: (
                "partial",
                "A no-API local diagnostic now runs the stronger 1,000 initial-family plus 200 partial-observability scale, but the paper-facing API listener runs remain bounded 50-scene diagnostics.",
            ),
        ),
        PlanItem(
            "Stronger-plan extensions",
            "stretch",
            "Evaluate K=8 candidate generation in addition to K=4.",
            ["docs/candidate_budget_audit.md", "docs/local_stronger_plan_k8.md", "results/local_stronger_plan_k8.json"],
            lambda: (
                "partial",
                "The local stronger-plan diagnostic evaluates K=8 candidate slots and shows added non-coordinate diversity; cached API speaker artifacts remain K=4.",
            ),
        ),
        PlanItem(
            "Stronger-plan extensions",
            "stretch",
            "Run an actual interaction-memory prompt rerun after distilling rules from failures.",
            ["docs/interaction_memory_rules.md", "results/interaction_memory_rules.json"],
            lambda: (
                "partial",
                "A replay-only interaction-memory rule audit is present, but no new memory-prompt generation/evaluation run is claimed.",
            ),
        ),
        PlanItem(
            "Stronger-plan extensions",
            "stretch",
            "Validate failures with human or independent non-LLM judgments.",
            ["REPRODUCE.md", "paper/main.tex"],
            lambda: (
                "open",
                "The paper explicitly notes that held-out listeners are API LLMs and broader human validation remains future work.",
            ),
        ),
        PlanItem(
            "Release engineering",
            "stretch",
            "Publish the artifact as a public repository or submission bundle.",
            ["README.md", "REPRODUCE.md"],
            lambda: covered_if(
                ctx.git_remote_contains("github.com/jingxuxie/cross_play"),
                "The artifact package is in a git repository configured for the public GitHub release target.",
                "The local artifact package is complete and reproducible, but public publishing is separate work.",
            ),
        ),
    ]


def required_methods_present(ctx: Context, path: str, *, local: bool = False) -> bool:
    by_method = ctx.json(path).get("by_method", {})
    if local:
        required = {
            "template",
            "direct",
            "best_of_k_shortest",
            "mirror_selfplay",
            "population_play",
            "oracle_upper_bound",
        }
    else:
        required = {
            "template",
            "api_direct_first",
            "api_best_of_k_shortest",
            "hybrid_local_mirror_api_eval",
            "hybrid_local_population_api_eval",
            "oracle_upper_bound",
        }
    return required.issubset(set(by_method))


def count_statuses(items: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"covered": 0, "partial": 0, "open": 0}
    for item in items:
        counts[item["status"]] += 1
    return counts


def render_markdown(report: dict[str, Any]) -> str:
    counts = report["status_counts"]
    core = report["core_status_counts"]
    stretch = report["stretch_status_counts"]
    lines = [
        "# Plan Coverage Audit",
        "",
        "This generated audit maps the original workshop plan to the current checked artifacts.",
        "It distinguishes completed core workshop-paper requirements from stronger-plan or release tasks that remain partial or open.",
        "",
        f"Overall: {counts['covered']} covered, {counts['partial']} partial, {counts['open']} open across {report['n_items']} plan items.",
        f"Core scope: {core['covered']} covered, {core['partial']} partial, {core['open']} open.",
        f"Stretch scope: {stretch['covered']} covered, {stretch['partial']} partial, {stretch['open']} open.",
        "",
        "## Coverage Table",
        "",
        "| Status | Scope | Section | Plan item | Evidence | Detail |",
        "|---|---|---|---|---|---|",
    ]
    for row in report["items"]:
        evidence = ", ".join(f"`{path}`" for path in row["evidence"])
        lines.append(
            f"| {row['status']} | {row['scope']} | {row['section']} | {row['plan_item']} | {evidence} | {row['detail']} |"
        )

    lines.extend(
        [
            "",
            "## Remaining Partial Or Open Items",
            "",
            "| Status | Scope | Plan item | Detail |",
            "|---|---|---|---|",
        ]
    )
    for row in report["open_or_partial"]:
        lines.append(f"| {row['status']} | {row['scope']} | {row['plan_item']} | {row['detail']} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
