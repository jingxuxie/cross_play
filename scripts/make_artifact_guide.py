#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl, read_scenes


METHOD_LABELS = {
    "api_direct_first": "direct",
    "api_best_of_k_shortest": "shortest",
    "hybrid_local_mirror_api_eval": "mirror",
    "hybrid_local_population_api_eval": "population",
    "oracle_upper_bound": "oracle",
    "no_coord_mirror": "mirror",
    "no_coord_population": "population",
    "no_coord_consensus_info": "consensus+info",
    "no_coord_informative": "info prior",
    "no_coord_oracle": "oracle",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="docs/artifact_guide.md")
    args = parser.parse_args()

    report = build_report()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote {out}")


def build_report() -> dict[str, Any]:
    return {
        "datasets": dataset_cards(),
        "result_groups": integrity_groups(),
        "cache": cache_summary(),
        "api_token_accounting": api_token_accounting(),
        "headline_results": headline_results(),
        "cross_model_listener": cross_model_listener(),
        "cross_model_failure_overlap": cross_model_failure_overlap(),
        "gpt55_speaker_smoke": gpt55_speaker_smoke(),
        "gpt55_followup_plan_status": gpt55_followup_plan_status(),
        "human_validation_packet": human_validation_packet(),
        "no_coord_results": no_coord_results(),
        "local_benchmark": local_benchmark(),
        "local_stronger_plan": local_stronger_plan(),
        "api_leave_one_out": api_leave_one_out(),
        "selection_regret": selection_regret(),
        "candidate_pool": candidate_pool(),
        "candidate_budget": candidate_budget(),
        "candidate_role_selection": candidate_role_selection(),
        "random_candidate_baseline": random_candidate_baseline(),
        "message_length_audit": message_length_audit(),
        "listener_disagreement": listener_disagreement(),
        "listener_confidence": listener_confidence(),
        "failure_taxonomy": failure_taxonomy(),
        "rule_based_ambiguity": rule_based_ambiguity(),
        "interaction_memory_rules": interaction_memory_rules(),
        "qualitative_examples": qualitative_examples(),
        "reviewer_checklist": reviewer_checklist(),
        "plan_coverage": plan_coverage(),
        "quality_gates": quality_gates(),
        "claim_map": claim_map(),
        "core_files": core_files(),
    }


def dataset_cards() -> list[dict[str, Any]]:
    specs = [
        ("local_benchmark600", "data/local_benchmark600_scenes.jsonl"),
        ("mixed_50", "data/dev_scenes.jsonl"),
        ("perspective_stress_50", "data/perspective_stress50_scenes.jsonl"),
        ("partial_observability_api50", "data/partial_observability_local50_scenes.jsonl"),
    ]
    cards = []
    for name, path in specs:
        scenes = read_scenes(path)
        scenario_counts = Counter(scene.scenario_type for scene in scenes)
        private_landmarks = sum(
            1
            for scene in scenes
            if any(
                obj.id == scene.metadata.get("private_landmark_id")
                and not obj.visible_to_listener
                for obj in scene.objects
            )
        )
        cards.append(
            {
                "name": name,
                "path": path,
                "n_scenes": len(scenes),
                "scenario_counts": dict(sorted(scenario_counts.items())),
                "private_landmarks": private_landmarks,
            }
        )
    return cards


def integrity_groups() -> list[dict[str, Any]]:
    integrity = read_json("results/benchmark_integrity_audit.json")
    return integrity.get("summary", {}).get("groups", [])


def cache_summary() -> dict[str, Any]:
    integrity = read_json("results/benchmark_integrity_audit.json")
    return integrity.get("summary", {}).get("cache", {})


def api_token_accounting() -> dict[str, Any] | None:
    path = Path("results/api_token_accounting.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/api_token_accounting.md",
        "n_cache_files": report["n_cache_files"],
        "n_readable": report["n_readable"],
        "n_missing_usage": report["n_missing_usage"],
        "totals": report["totals"],
        "by_model": report["by_model"],
        "by_schema_family": report["by_schema_family"],
    }


def headline_results() -> list[dict[str, Any]]:
    return [
        result_row(
            "mixed_50",
            "results/hybrid_api_pilot50_allcand_summary.json",
            "results/hybrid_api_pilot50_population_vs_mirror_paired.json",
        ),
        result_row(
            "perspective_stress_50",
            "results/perspective_stress50_hybrid_summary.json",
            "results/perspective_stress50_population_vs_mirror_paired.json",
        ),
        result_row(
            "perspective_stress_50_alt_model",
            "results/perspective_stress50_gpt41nano_summary.json",
            "results/perspective_stress50_gpt41nano_population_vs_mirror_paired.json",
        ),
        result_row(
            "partial_observability_api50",
            "results/partial_observability_api50_summary.json",
            "results/partial_observability_api50_population_vs_mirror_paired.json",
        ),
    ]


def no_coord_results() -> list[dict[str, Any]]:
    return [
        no_coord_row(
            "mixed_50_no_coord",
            "results/hybrid_api_pilot50_no_coord_summary.json",
            "results/hybrid_api_pilot50_no_coord_consensus_info_vs_mirror_paired.json",
        ),
        no_coord_row(
            "perspective_stress_50_no_coord",
            "results/perspective_stress50_gpt41nano_no_coord_summary.json",
            "results/perspective_stress50_gpt41nano_no_coord_consensus_info_vs_mirror_paired.json",
        ),
        no_coord_row(
            "partial_observability_api50_no_coord",
            "results/partial_observability_api50_no_coord_summary.json",
            None,
        ),
    ]


def cross_model_listener() -> dict[str, Any] | None:
    path = Path("results/cross_model_listener_audit.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/cross_model_listener_audit.md",
        "table": "paper/tables/cross_model_listener_audit.tex",
        "rows": report["rows"],
        "interpretation": report["interpretation"],
    }


def cross_model_failure_overlap() -> dict[str, Any] | None:
    path = Path("results/cross_model_failure_overlap.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/cross_model_failure_overlap.md",
        "units": "results/cross_model_failure_overlap_units.jsonl",
        "runs": report["runs"],
        "overlap": report["overlap"],
        "key_findings": report["key_findings"],
    }


def gpt55_speaker_smoke() -> dict[str, Any] | None:
    path = Path("results/gpt55_speaker_smoke.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    sources = {source["label"]: source for source in report["sources"]}
    gpt55 = sources["gpt55_speaker"]
    existing = sources["existing_gpt54_speaker"]
    progress = report.get("progress_extension")
    progress_payload = None
    if progress:
        mirror = method_row(progress, "hybrid_local_mirror_api_eval")
        progress_payload = {
            "n_scenes": progress["n_scenes"],
            "direct_success": method_row(progress, "api_direct_first")["success"],
            "shortest_success": method_row(progress, "api_best_of_k_shortest")["success"],
            "mirror_success": mirror["success"],
            "mirror_sameplay": mirror["sameplay_success"],
            "mirror_gap": mirror["crossplay_gap"],
            "population_success": method_row(progress, "hybrid_local_population_api_eval")["success"],
            "oracle_success": method_row(progress, "oracle_upper_bound")["success"],
            "k1_robust": progress["candidate_budget"][0]["robust_scene_rate"],
            "k2_robust": progress["candidate_budget"][1]["robust_scene_rate"],
            "uncached_speaker_calls": progress["speaker_usage"]["uncached_speaker_calls"],
            "uncached_speaker_tokens": progress["speaker_usage"]["uncached_total_tokens"],
        }
    return {
        "source": str(path),
        "markdown": "docs/gpt55_speaker_smoke_report.md",
        "script": "scripts/analyze_gpt55_speaker_smoke.py",
        "same_scene_count": report["comparison"]["same_scene_count"],
        "existing_direct_success": report["comparison"]["existing_direct_success"],
        "gpt55_direct_success": report["comparison"]["gpt55_direct_success"],
        "existing_mirror_success": report["comparison"]["existing_mirror_success"],
        "gpt55_mirror_success": report["comparison"]["gpt55_mirror_success"],
        "existing_population_success": report["comparison"]["existing_population_success"],
        "gpt55_population_success": report["comparison"]["gpt55_population_success"],
        "existing_k1_robust": existing["candidate_budget"][0]["robust_scene_rate"],
        "gpt55_k1_robust": gpt55["candidate_budget"][0]["robust_scene_rate"],
        "uncached_speaker_calls": gpt55["speaker_usage"]["uncached_speaker_calls"],
        "speaker_total_tokens": gpt55["speaker_usage"]["total_tokens"],
        "progress_extension": progress_payload,
    }


def gpt55_followup_plan_status() -> dict[str, Any] | None:
    path = Path("results/gpt55_followup_plan_status.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/gpt55_followup_plan_status.md",
        "script": "scripts/audit_gpt55_followup_plan.py",
        "summary": report["summary"],
        "items": report["items"],
        "claim_boundary": report["paper_claim_boundary"],
        "next_best_steps": report["next_best_steps"],
    }


def human_validation_packet() -> dict[str, Any] | None:
    path = Path("results/human_validation_answer_key.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/human_validation_packet.md",
        "html": "docs/human_validation_packet.html",
        "items": "data/human_validation_items.jsonl",
        "response_template": "data/human_validation_response_template.csv",
        "script": "scripts/make_human_validation_packet.py",
        "summary": report["summary"],
        "analysis_plan": report["analysis_plan"],
    }


def local_benchmark() -> dict[str, Any] | None:
    path = Path("results/local_benchmark600_check.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    obs = report["key_observations"]
    return {
        "source": str(path),
        "scene_file": report["scene_file"],
        "records_file": report["records_file"],
        "n_scenes": report["n_scenes"],
        "scenario_counts": report["scenario_counts"],
        "mirror_cross": obs["mirror_cross"],
        "mirror_same": obs["mirror_same"],
        "mirror_gap": obs["mirror_gap"],
        "population_cross": obs["population_cross"],
        "template_cross": obs["template_cross"],
        "oracle_cross": obs["oracle_cross"],
        "perspective_mirror_cross": obs["perspective_mirror_cross"],
        "perspective_mirror_gap": obs["perspective_mirror_gap"],
    }


def local_stronger_plan() -> dict[str, Any] | None:
    path = Path("results/local_stronger_plan_k8.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/local_stronger_plan_k8.md",
        "scene_file": report["scene_file"],
        "n_scenes": report["n_scenes"],
        "scenario_counts": report["scenario_counts"],
        "key_observations": report["key_observations"],
        "budget_rows": report["budget_rows"],
        "selector_rows": report["selector_rows"],
    }


def api_leave_one_out() -> list[dict[str, Any]]:
    path = Path("results/api_listener_leave_one_out.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for dataset in report["datasets"]:
        summary = dataset["summary"]
        paired = dataset["paired_population_minus_mirror"]
        rows.append(
            {
                "label": dataset["label"],
                "source": str(path),
                "mirror": summary["loo_api_mirror"]["success"],
                "population": summary["loo_api_population"]["success"],
                "oracle": summary["loo_api_oracle"]["success"],
                "diff": paired["diff_population_minus_mirror"],
                "ci": paired["diff_ci95"],
            }
        )
    return rows


def selection_regret() -> list[dict[str, Any]]:
    path = Path("results/selection_regret_audit.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        for row in run["rows"]:
            if row["method_label"] not in {"mirror", "population", "consensus+info"}:
                continue
            rows.append(
                {
                    "label": run["label"],
                    "source": str(path),
                    "method": row["method_label"],
                    "method_success": row["method_success"],
                    "oracle_success": row["oracle_success"],
                    "regret": row["regret"],
                    "ci": row["regret_ci95"],
                }
            )
    return rows


def candidate_pool() -> dict[str, list[dict[str, Any]]]:
    path = Path("results/candidate_pool_audit.json")
    if not path.exists():
        return {"availability": [], "selectors": []}
    report = read_json(str(path))
    availability = []
    selectors = []
    for run in report["runs"]:
        pool = run["candidate_pool"]
        availability.append(
            {
                "label": run["label"],
                "filter": run["filter"],
                "source": str(path),
                "n_scenes": run["n_scenes"],
                "mean_candidates": pool["mean_candidates"],
                "mean_robust_candidates": pool["mean_robust_candidates"],
                "robust_scene_rate": pool["robust_candidate_scene_rate"],
                "oracle_success": pool["oracle_success"],
            }
        )
        for row in run["methods"]:
            if row["method_label"] not in {"mirror", "population", "consensus+info"}:
                continue
            selectors.append(
                {
                    "label": run["label"],
                    "source": str(path),
                    "method": row["method_label"],
                    "selected_success": row["selected_success"],
                    "selected_robust_rate": row["selected_robust_rate"],
                    "oracle_match_rate": row["oracle_match_rate"],
                }
            )
    return {"availability": availability, "selectors": selectors}


def candidate_budget() -> list[dict[str, Any]]:
    path = Path("results/candidate_budget_audit.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        for row in run["prefix_rows"]:
            rows.append(
                {
                    "label": run["label"],
                    "source": str(path),
                    "k": row["k"],
                    "oracle_success": row["oracle_success"],
                    "robust_scene_rate": row["robust_scene_rate"],
                }
            )
    return rows


def candidate_role_selection() -> dict[str, Any]:
    path = Path("results/candidate_role_selection_audit.json")
    if not path.exists():
        return {"rows": [], "summary": {}}
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        for row in run["methods"]:
            if row["method_label"] not in {"mirror", "population", "consensus+info"}:
                continue
            rates = row["role_rates"]
            rows.append(
                {
                    "label": run["label"],
                    "filter": run["filter"],
                    "source": str(path),
                    "method": row["method_label"],
                    "n_scenes": row["n_scenes"],
                    "success": row["success"],
                    "natural_first": rates["natural_first"],
                    "attribute_short": rates["attribute_short"],
                    "relational_or_spatial": rates["relational_or_spatial"],
                    "coordinate_fallback": rates["coordinate_fallback"],
                    "unresolved": row["n_unresolved"],
                }
            )
    return {"rows": rows, "summary": report["summary"]}


def random_candidate_baseline() -> list[dict[str, Any]]:
    path = Path("results/random_candidate_baseline.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        rows.append(
            {
                "label": run["label"],
                "filter": run["filter"],
                "source": str(path),
                "n_scenes": run["n_scenes"],
                "mean_candidates": run["mean_candidates"],
                "random_expected": run["random_expected_success"],
                "random_robust_pick": run["random_robust_pick_rate"],
                "primary_method": run["primary_method"],
                "primary_minus_random": run["primary_minus_random"],
                "ci": run["primary_minus_random_ci95"],
            }
        )
    return rows


def message_length_audit() -> list[dict[str, Any]]:
    path = Path("results/message_length_audit.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        methods = {row["method_label"]: row for row in run["methods"]}
        pair = run["primary_vs_mirror"]
        rows.append(
            {
                "label": run["label"],
                "filter": run["filter"],
                "source": str(path),
                "primary_method": run["primary_method"],
                "mirror_tokens": methods["mirror"]["mean_tokens"],
                "primary_tokens": methods[run["primary_method"]]["mean_tokens"],
                "template_tokens": methods.get("template", {}).get("mean_tokens"),
                "direct_tokens": methods.get("direct", {}).get("mean_tokens"),
                "primary_success": methods[run["primary_method"]]["success"],
                "mirror_success": methods["mirror"]["success"],
                "direct_success": methods.get("direct", {}).get("success"),
                "success_delta": pair["success_delta"],
                "token_delta": pair["token_delta"],
                "token_ci": pair["token_delta_ci95"],
            }
        )
    return rows


def listener_disagreement() -> list[dict[str, Any]]:
    path = Path("results/listener_disagreement_audit.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        for row in run["methods"]:
            if row["method_label"] not in {"mirror", "population", "consensus+info"}:
                continue
            rows.append(
                {
                    "label": run["label"],
                    "source": str(path),
                    "method": row["method_label"],
                    "success": row["success"],
                    "unanimous_success_rate": row["unanimous_success_rate"],
                    "split_success_rate": row["split_success_rate"],
                    "unanimous_failure_rate": row["unanimous_failure_rate"],
                    "choice_disagreement_rate": row["choice_disagreement_rate"],
                }
            )
    return rows


def listener_confidence() -> list[dict[str, Any]]:
    path = Path("results/listener_confidence_audit.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for run in report["runs"]:
        for row in run["methods"]:
            if row["method_label"] not in {"mirror", "population", "consensus+info"}:
                continue
            rows.append(
                {
                    "label": run["label"],
                    "source": str(path),
                    "method": row["method_label"],
                    "success": row["success"],
                    "mean_confidence": row["mean_confidence"],
                    "ambiguity_rate": row["ambiguity_rate"],
                    "mean_failure_confidence": row["mean_failure_confidence"],
                    "high_confidence_failure_rate": row["high_confidence_failure_rate"],
                    "scene_high_confidence_failure_rate": row["scene_high_confidence_failure_rate"],
                }
            )
    return rows


def failure_taxonomy() -> dict[str, Any] | None:
    path = Path("results/failure_taxonomy_audit.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/failure_taxonomy_audit.md",
        "sets": report["failure_sets"],
        "combined": report["combined"],
    }


def rule_based_ambiguity() -> dict[str, Any] | None:
    path = Path("results/rule_based_ambiguity_verifier.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/rule_based_ambiguity_verifier.md",
        "units": "results/rule_based_ambiguity_verifier_units.jsonl",
        "combined": report["coded_taxonomy_alignment"]["combined"],
        "key_findings": report["key_findings"],
    }


def interaction_memory_rules() -> dict[str, Any] | None:
    path = Path("results/interaction_memory_rules.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/interaction_memory_rules.md",
        "sets": report["failure_sets"],
        "combined": report["combined"],
        "prompt_snippet": report["prompt_snippet"],
    }


def qualitative_examples() -> list[dict[str, Any]]:
    path = Path("results/qualitative_failure_examples.json")
    if not path.exists():
        return []
    report = read_json(str(path))
    rows = []
    for example in report["examples"]:
        rows.append(
            {
                "title": example["title"],
                "scene_id": example["scene_id"],
                "category": example["failure_category"],
                "mirror_success": example["mirror_outcome"]["success_rate"],
                "repair_label": example["repair_label"],
                "repair_success": example["repair_outcome"]["success_rate"],
                "source": str(path),
            }
        )
    return rows


def reviewer_checklist() -> dict[str, Any] | None:
    path = Path("results/reviewer_checklist.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    sections: dict[str, dict[str, int]] = {}
    for item in report["items"]:
        section = sections.setdefault(item["section"], {"passed": 0, "failed": 0})
        if item["status"] == "PASS":
            section["passed"] += 1
        else:
            section["failed"] += 1
    return {
        "source": str(path),
        "markdown": "docs/reviewer_checklist.md",
        "n_items": report["n_items"],
        "n_failed": report["n_failed"],
        "sections": sections,
    }


def plan_coverage() -> dict[str, Any] | None:
    path = Path("results/plan_coverage_audit.json")
    if not path.exists():
        return None
    report = read_json(str(path))
    return {
        "source": str(path),
        "markdown": "docs/plan_coverage_audit.md",
        "n_items": report["n_items"],
        "status_counts": report["status_counts"],
        "core_status_counts": report["core_status_counts"],
        "stretch_status_counts": report["stretch_status_counts"],
        "open_or_partial": report["open_or_partial"],
    }


def result_row(label: str, summary_path: str, paired_path: str) -> dict[str, Any]:
    summary = read_json(summary_path)["by_method"]
    paired = first_overall_pair(read_json(paired_path))
    mirror = summary["hybrid_local_mirror_api_eval"]
    population = summary["hybrid_local_population_api_eval"]
    oracle = summary["oracle_upper_bound"]
    return {
        "label": label,
        "summary_path": summary_path,
        "paired_path": paired_path,
        "mirror_cross": mirror["success"],
        "mirror_same": mirror.get("sameplay_success"),
        "mirror_gap": mirror.get("crossplay_gap"),
        "population_cross": population["success"],
        "oracle_cross": oracle["success"],
        "diff": paired["diff_a_minus_b"],
        "ci": paired["diff_ci95"],
        "p": paired["paired_bootstrap_p_two_sided"],
    }


def no_coord_row(label: str, summary_path: str, paired_path: str | None) -> dict[str, Any]:
    summary = read_json(summary_path)["by_method"]
    paired = first_overall_pair(read_json(paired_path)) if paired_path else None
    return {
        "label": label,
        "summary_path": summary_path,
        "paired_path": paired_path or "-",
        "mirror_cross": summary["no_coord_mirror"]["success"],
        "population_cross": summary["no_coord_population"]["success"],
        "consensus_cross": summary["no_coord_consensus_info"]["success"],
        "oracle_cross": summary["no_coord_oracle"]["success"],
        "diff": paired["diff_a_minus_b"] if paired else None,
        "ci": paired["diff_ci95"] if paired else None,
        "p": paired["paired_bootstrap_p_two_sided"] if paired else None,
    }


def first_overall_pair(rows: list[dict[str, Any]]) -> dict[str, Any]:
    for row in rows:
        if row.get("scenario_type") is None:
            return row
    return rows[0]


def quality_gates() -> list[dict[str, Any]]:
    gates = [
        ("benchmark integrity", "results/benchmark_integrity_audit.json"),
        ("paper claims", "results/paper_claims_verification.json"),
        ("reviewer checklist", "results/reviewer_checklist.json"),
        ("submission readiness", "results/submission_readiness_audit.json"),
    ]
    out = []
    for name, path in gates:
        report = read_json(path)
        out.append(
            {
                "name": name,
                "path": path,
                "checks": report.get("n_checks", report.get("n_items", "?")),
                "failed": report.get("n_failed", "?"),
                "warnings": report.get("n_warn", 0),
                "actions": report.get("n_actions", 0),
            }
        )
    return out


def claim_map() -> list[dict[str, str]]:
    return [
        {
            "claim": "Same-play can overstate held-out communicative success.",
            "evidence": "results/paper_claims_verification.md; results/*_population_vs_mirror_paired.md",
            "anchor": "mirror same-play is 1.000 while cross-play is lower in mixed, perspective, alternate-model, and partial-observability runs",
        },
        {
            "claim": "The mirror self-play gap persists under GPT-5.5 and across held-out listener families.",
            "evidence": "docs/cross_model_listener_audit.md; docs/cross_model_failure_overlap.md; results/cross_model_listener_audit.json; results/cross_model_failure_overlap.json; paper/tables/cross_model_listener_audit.tex",
            "anchor": "population-minus-mirror gaps are 0.187, 0.287, and 0.327 on perspective stress and 0.333, 0.340, and 0.347 on partial observability; 20 of 22 GPT-4.1 perspective mirror-failure scenes and 26 of 26 partial-observability scenes also fail under GPT-5.5",
        },
        {
            "claim": "A bounded GPT-5.5 speaker smoke improves first-candidate quality but does not make mirror selection the robust selector.",
            "evidence": "docs/gpt55_speaker_smoke_report.md; results/gpt55_speaker_smoke.json",
            "anchor": "on the same 10 perspective-stress scenes, direct-first rises from 0.800 to 1.000 and mirror rises from 0.667 to 0.867; the 50-scene speaker audit has GPT-5.5 direct-first 0.993, mirror 0.853, and population-play 1.000",
        },
        {
            "claim": "The GPT-5.5 follow-up evidence is explicitly bounded by covered, partial, and future rows.",
            "evidence": "docs/gpt55_followup_plan_status.md; results/gpt55_followup_plan_status.json",
            "anchor": "follow-up plan status is 4 covered, 2 partial, and 0 future, with no missing evidence paths",
        },
        {
            "claim": "The human-validation extension is protocol-ready but has no collected human labels yet.",
            "evidence": "docs/human_validation_packet.md; data/human_validation_items.jsonl; results/human_validation_answer_key.json",
            "anchor": "the prepared packet has 20 participant-safe items: 10 perspective mirror failures, 5 partial-observability mirror failures, and 5 mirror-success controls",
        },
        {
            "claim": "Population-play closes the observed full-candidate cross-play gaps.",
            "evidence": "paper/tables/mixed50.tex; paper/tables/perspective_stress50.tex; paper/tables/perspective_altmodel50.tex; results/partial_observability_api50_summary.json",
            "anchor": "population cross-play is 1.000 in all full-candidate paper-facing runs",
        },
        {
            "claim": "The strongest full-candidate result depends on explicit listener-invariant fallbacks.",
            "evidence": "paper/tables/perspective_stress50_gpt41nano_no_coord.tex; paper/tables/selection_mechanisms_stress_no_coord.tex",
            "anchor": "no-coordinate stress population drops to 0.420 while consensus+info reaches 0.760",
        },
        {
            "claim": "Partial-observability failures are under-informativeness failures, not private-landmark leakage.",
            "evidence": "docs/partial_observability_api50_check.md; results/partial_observability_api50_check.json; results/partial_observability_api50_mirror_failures_coded.csv",
            "anchor": "0 candidate messages reference private landmarks; all 50 full-run mirror failures are underspecified-distractor choices",
        },
        {
            "claim": "The population-selection effect is not only a deterministic-local-listener artifact.",
            "evidence": "docs/api_listener_leave_one_out.md; results/api_listener_leave_one_out.json",
            "anchor": "cache-only API listener leave-one-out improves population over mirror in all four cached runs",
        },
        {
            "claim": "Most full-candidate failures are selector regret rather than missing candidates.",
            "evidence": "docs/selection_regret_audit.md; results/selection_regret_audit.json",
            "anchor": "full-candidate population-play has zero regret; mirror regret is 0.093, 0.187, 0.287, and 0.333 across the API runs",
        },
        {
            "claim": "Full-candidate population-play succeeds by selecting available all-listener-robust candidates.",
            "evidence": "docs/candidate_pool_audit.md; results/candidate_pool_audit.json",
            "anchor": "every full-candidate run has a robust candidate in every scene; population-play selects a robust candidate in 1.000 of scenes",
        },
        {
            "claim": "The four-candidate protocol materially increases robust candidate availability in harder audits.",
            "evidence": "docs/candidate_budget_audit.md; results/candidate_budget_audit.json",
            "anchor": "alternate-model perspective robust-scene coverage rises from 0.380 at K=1 to 1.000 at K=4",
        },
        {
            "claim": "Selector behavior corresponds to different generated candidate roles.",
            "evidence": "docs/candidate_role_selection_audit.md; results/candidate_role_selection_audit.json",
            "anchor": "full-candidate population uses coordinate fallbacks in 1.000 of perspective and partial-observability stress scenes, while no-coordinate consensus+info uses the short attribute slot in 0.000 of those harder scenes",
        },
        {
            "claim": "Selector gains are not explained by uniformly choosing any generated candidate.",
            "evidence": "docs/random_candidate_baseline.md; results/random_candidate_baseline.json",
            "anchor": "population-play improves over random by 0.135, 0.285, 0.343, and 0.247 in the full-candidate runs; consensus+info improves over random by 0.100, 0.218, and 0.316 in no-coordinate runs",
        },
        {
            "claim": "Selector gains are not solely a message-length artifact.",
            "evidence": "docs/message_length_audit.md; results/message_length_audit.json",
            "anchor": "full-candidate population selected messages average 6.82, 10.22, 10.22, and 9.66 tokens, while direct messages can be longer than mirror and still less successful",
        },
        {
            "claim": "Population-play turns available robust candidates into unanimous held-out listener agreement.",
            "evidence": "docs/listener_disagreement_audit.md; results/listener_disagreement_audit.json",
            "anchor": "mirror split-outcome rates are 0.080, 0.180, 0.360, and 0.500 across full-candidate runs; population split-outcome rate is 0.000",
        },
        {
            "claim": "Listener self-reported confidence and ambiguity are not substitutes for cross-play.",
            "evidence": "docs/listener_confidence_audit.md; results/listener_confidence_audit.json",
            "anchor": "alternate-model perspective ambiguity flags are 0.000 while mirror high-confidence failure rates are 0.147 and 0.280",
        },
        {
            "claim": "Representative failures reflect real target-distractor ambiguity or frame sensitivity.",
            "evidence": "docs/failure_taxonomy_audit.md; docs/qualitative_failure_examples.md; results/qualitative_failure_examples.json",
            "anchor": "147 of 152 coded listener-level mirror failures are underspecified-distractor cases and 5 are perspective-frame errors",
        },
        {
            "claim": "A rule-based non-LLM verifier recovers the coded mirror-failure taxonomy.",
            "evidence": "docs/rule_based_ambiguity_verifier.md; results/rule_based_ambiguity_verifier.json; results/rule_based_ambiguity_verifier_units.jsonl",
            "anchor": "combined coded failure set has symbolic ambiguity recall 1.000, attribute-under-specification recall 1.000, and frame-sensitive recall 1.000",
        },
        {
            "claim": "The coded failures induce a small interaction-memory rule set.",
            "evidence": "docs/interaction_memory_rules.md; results/interaction_memory_rules.json",
            "anchor": "152 coded failure rows collapse into disambiguate-shared-attributes and avoid-frame-sensitive-only rules; cached repairs satisfy the derived cue in 1.000 of failure scenes",
        },
        {
            "claim": "The original pre-submission checklist is backed by concrete artifacts.",
            "evidence": "docs/reviewer_checklist.md; results/reviewer_checklist.json",
            "anchor": "Section 32 reviewer checklist passes all 19 core-validity, results, and paper items",
        },
        {
            "claim": "The artifact package explicitly distinguishes completed core requirements from stretch gaps.",
            "evidence": "docs/plan_coverage_audit.md; results/plan_coverage_audit.json",
            "anchor": "core scope has 17 covered, 2 partial, 0 open items; stretch scope has 2 covered, 3 partial, 0 open after adding independent non-LLM validation",
        },
        {
            "claim": "The released generator supports a benchmark-scale local sanity sweep.",
            "evidence": "docs/local_benchmark600_check.md; results/local_benchmark600_check.json",
            "anchor": "600 local scenes balanced across four initial scenario families; mirror same-play is 1.000 but cross-play is 0.631",
        },
        {
            "claim": "The local artifact supports the stronger-plan 1,000+200 scale and K=8 diagnostic.",
            "evidence": "docs/local_stronger_plan_k8.md; results/local_stronger_plan_k8.json",
            "anchor": "no-coordinate oracle over 1,200 local scenes rises from 0.808 at K=4 to 0.995 at K=8",
        },
        {
            "claim": "The cached benchmark artifacts are internally consistent.",
            "evidence": "results/benchmark_integrity_audit.md",
            "anchor": "242/242 integrity checks pass",
        },
        {
            "claim": "API usage is bounded and cache-replayable.",
            "evidence": "docs/api_token_accounting.md; results/api_token_accounting.json",
            "anchor": "5866 cached responses have complete usage metadata totaling 1680454 tokens",
        },
    ]


def core_files() -> list[tuple[str, str]]:
    return [
        ("Editable paper", "paper/main.tex"),
        ("Compiled paper", "paper/main.pdf"),
        ("COLM submission source", "paper/colm2026_submission.tex"),
        ("COLM submission PDF", "paper/colm2026_submission.pdf"),
        ("Protocol and prompts", "docs/protocol_and_prompts.md"),
        ("API token accounting", "docs/api_token_accounting.md"),
        ("Cross-model held-out listener audit", "docs/cross_model_listener_audit.md"),
        ("Cross-model failure overlap audit", "docs/cross_model_failure_overlap.md"),
        ("GPT-5.5 speaker smoke report", "docs/gpt55_speaker_smoke_report.md"),
        ("GPT-5.5 speaker 20-scene records", "results/gpt55_speaker_perspective20_records.jsonl"),
        ("GPT-5.5 speaker 20-scene candidates", "results/gpt55_speaker_perspective20_candidates.jsonl"),
        ("GPT-5.5 speaker 20-scene candidate eval", "results/gpt55_speaker_perspective20_candidate_eval_records.jsonl"),
        ("GPT-5.5 speaker 50-scene records", "results/gpt55_speaker_perspective50_records.jsonl"),
        ("GPT-5.5 speaker 50-scene candidates", "results/gpt55_speaker_perspective50_candidates.jsonl"),
        ("GPT-5.5 speaker 50-scene candidate eval", "results/gpt55_speaker_perspective50_candidate_eval_records.jsonl"),
        ("GPT-5.5 follow-up plan status", "docs/gpt55_followup_plan_status.md"),
        ("Human validation packet", "docs/human_validation_packet.md"),
        ("Human validation participant items", "data/human_validation_items.jsonl"),
        ("Human validation response template", "data/human_validation_response_template.csv"),
        ("600-scene local sanity check", "docs/local_benchmark600_check.md"),
        ("Local stronger-plan K=8 diagnostic", "docs/local_stronger_plan_k8.md"),
        ("Local stronger-plan scene file", "data/local_stronger_plan1200_scenes.jsonl"),
        ("API listener leave-one-out report", "docs/api_listener_leave_one_out.md"),
        ("Selection regret audit", "docs/selection_regret_audit.md"),
        ("Candidate pool robustness audit", "docs/candidate_pool_audit.md"),
        ("Candidate budget audit", "docs/candidate_budget_audit.md"),
        ("Candidate role selection audit", "docs/candidate_role_selection_audit.md"),
        ("Random candidate baseline", "docs/random_candidate_baseline.md"),
        ("Message length audit", "docs/message_length_audit.md"),
        ("Listener disagreement audit", "docs/listener_disagreement_audit.md"),
        ("Listener confidence audit", "docs/listener_confidence_audit.md"),
        ("Failure taxonomy audit", "docs/failure_taxonomy_audit.md"),
        ("Rule-based ambiguity verifier", "docs/rule_based_ambiguity_verifier.md"),
        ("Interaction memory rules", "docs/interaction_memory_rules.md"),
        ("Qualitative failure examples", "docs/qualitative_failure_examples.md"),
        ("Reviewer checklist", "docs/reviewer_checklist.md"),
        ("Plan coverage audit", "docs/plan_coverage_audit.md"),
        ("Partial-observability failure audit", "docs/partial_observability_api50_check.md"),
        ("Claim verifier", "scripts/verify_paper_claims.py"),
        ("Integrity audit", "scripts/audit_benchmark_integrity.py"),
        ("Readiness audit", "scripts/audit_submission_readiness.py"),
        ("API token accounting script", "scripts/analyze_api_token_accounting.py"),
        ("Cross-model listener audit script", "scripts/analyze_cross_model_listener_audit.py"),
        ("Cross-model failure overlap script", "scripts/analyze_cross_model_failure_overlap.py"),
        ("GPT-5.5 speaker smoke script", "scripts/analyze_gpt55_speaker_smoke.py"),
        ("GPT-5.5 follow-up status script", "scripts/audit_gpt55_followup_plan.py"),
        ("Human validation packet script", "scripts/make_human_validation_packet.py"),
        ("Local benchmark analysis script", "scripts/analyze_local_benchmark.py"),
        ("Local stronger-plan diagnostic script", "scripts/analyze_local_stronger_plan.py"),
        ("API listener leave-one-out script", "scripts/analyze_api_listener_leave_one_out.py"),
        ("Selection regret script", "scripts/analyze_selection_regret.py"),
        ("Candidate pool audit script", "scripts/analyze_candidate_pool.py"),
        ("Candidate budget audit script", "scripts/analyze_candidate_budget.py"),
        ("Candidate role selection script", "scripts/analyze_candidate_role_selection.py"),
        ("Random candidate baseline script", "scripts/analyze_random_candidate_baseline.py"),
        ("Message length audit script", "scripts/analyze_message_length_audit.py"),
        ("Listener disagreement audit script", "scripts/analyze_listener_disagreement.py"),
        ("Listener confidence audit script", "scripts/analyze_listener_confidence_audit.py"),
        ("Failure taxonomy script", "scripts/analyze_failure_taxonomy.py"),
        ("Rule-based ambiguity verifier script", "scripts/analyze_rule_based_ambiguity.py"),
        ("Interaction memory rule script", "scripts/analyze_interaction_memory_rules.py"),
        ("Qualitative examples script", "scripts/make_qualitative_examples.py"),
        ("Reviewer checklist script", "scripts/make_reviewer_checklist.py"),
        ("Plan coverage audit script", "scripts/audit_plan_coverage.py"),
        ("Reproduction commands", "REPRODUCE.md"),
    ]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# PRAG-CrossPlay Artifact Guide",
        "",
        "This guide maps the paper's main claims to the concrete files that support them.",
        "It is generated from the current JSON/JSONL artifacts and is intended as a reviewer-facing entry point.",
        "",
        "## Core Files",
        "",
        "| Role | Path |",
        "|---|---|",
    ]
    for role, path in report["core_files"]:
        lines.append(f"| {role} | `{path}` |")

    lines.extend(
        [
            "",
            "## Dataset Cards",
            "",
            "| Dataset | Source | Scenes | Scenario counts | Hidden private landmarks |",
            "|---|---|---:|---|---:|",
        ]
    )
    for row in report["datasets"]:
        lines.append(
            f"| {row['name']} | `{row['path']}` | {row['n_scenes']} | {format_counts(row['scenario_counts'])} | {row['private_landmarks']} |"
        )

    lines.extend(
        [
            "",
            "## Result Artifact Groups",
            "",
            "| Group | Scene file | Scenes | Record rows | Candidate rows | Audit rows | Speaker cache paths |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in report["result_groups"]:
        lines.append(
            "| {name} | `{scene_file}` | {n_scenes} | {record_rows} | {candidate_rows} | {audit_rows} | {speaker_cache_paths} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Cached Response Models",
            "",
            f"Cache files: {report['cache'].get('n_cache_files', '?')}.",
            "",
            "| Requested model | Response model | Cached responses |",
            "|---|---|---:|",
        ]
    )
    for row in report["cache"].get("model_versions", []):
        lines.append(
            f"| `{row['requested_model']}` | `{row['response_model']}` | {row['n']} |"
        )

    if report["api_token_accounting"]:
        accounting = report["api_token_accounting"]
        totals = accounting["totals"]
        lines.extend(
            [
                "",
                "## API Token Accounting",
                "",
                "This cache-only budget audit summarizes stored Responses API usage metadata. It reports tokens, not dollar cost, because billing depends on account-specific and date-specific pricing.",
                "",
                "| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Source |",
                "|---:|---:|---:|---:|---:|---:|---|",
                f"| {accounting['n_cache_files']} | {accounting['n_readable']} | {accounting['n_missing_usage']} | {totals['input_tokens']} | {totals['output_tokens']} | {totals['total_tokens']} | `{accounting['source']}` |",
                "",
                "| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens |",
                "|---|---|---:|---:|---:|---:|",
            ]
        )
        for row in accounting["by_model"]:
            lines.append(
                f"| `{row['requested_model']}` | `{row['response_model']}` | {row['n_responses']} | {row['input_tokens']} | {row['output_tokens']} | {row['total_tokens']} |"
            )

    lines.extend(
        [
            "",
            "## Headline Full-Candidate Results",
            "",
            "| Run | Mirror cross | Mirror same | Gap | Population cross | Oracle | Pop-minus-mirror 95% CI | Source |",
            "|---|---:|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in report["headline_results"]:
        lines.append(
            f"| {row['label']} | {fmt(row['mirror_cross'])} | {fmt(row['mirror_same'])} | {fmt(row['mirror_gap'])} | {fmt(row['population_cross'])} | {fmt(row['oracle_cross'])} | {fmt(row['diff'])} [{fmt(row['ci'][0])}, {fmt(row['ci'][1])}] | `{row['summary_path']}` |"
        )

    if report["cross_model_listener"]:
        cross = report["cross_model_listener"]
        lines.extend(
            [
                "",
                "## Cross-Model Held-Out Listener Audit",
                "",
                cross["interpretation"],
                "",
                "| Setting | Held-out listener | Direct | Mirror | Population | Oracle | Pop-minus-mirror 95% CI | Source |",
                "|---|---|---:|---:|---:|---:|---|---|",
            ]
        )
        for row in cross["rows"]:
            paired = row["population_minus_mirror"]
            ci = paired["diff_ci95"]
            lines.append(
                "| {setting} | {listener} | {direct} | {mirror} | {population} | {oracle} | {diff} [{lo}, {hi}] | `{source}` |".format(
                    setting=row["setting"],
                    listener=row["listener"],
                    direct=fmt(row["direct"]["success"]),
                    mirror=fmt(row["mirror"]["success"]),
                    population=fmt(row["population"]["success"]),
                    oracle=fmt(row["oracle"]["success"]),
                    diff=fmt(paired["diff_a_minus_b"]),
                    lo=fmt(ci[0]),
                    hi=fmt(ci[1]),
                    source=row["summary_source"],
                )
            )
        lines.extend(
            [
                "",
                "GPT-5.5 rows reuse cached speaker candidates and evaluate selected messages only; because population-play reaches 1.000, the same candidate pool's oracle ceiling is also 1.000.",
            ]
        )

    if report["cross_model_failure_overlap"]:
        overlap = report["cross_model_failure_overlap"]
        findings = overlap["key_findings"]
        lines.extend(
            [
                "",
                "## Cross-Model Failure Overlap Audit",
                "",
                "This cache-only audit checks whether GPT-5.5 repairs the same selected mirror messages that fail under earlier held-out listener families.",
                f"In perspective stress, {findings['perspective_gpt41_gpt55_mirror_failure_overlap']} of 22 GPT-4.1 mirror-failure scenes also fail under GPT-5.5; in partial observability, {findings['partial_gpt41_gpt55_mirror_failure_overlap']} of 26 do.",
                f"All GPT-5.5 mirror-failure scenes are symbolic-verifier positives in both settings, and GPT-5.5 population-play has {findings['perspective_gpt55_population_failure_scenes']} perspective-stress failures and {findings['partial_gpt55_population_failure_scenes']} partial-observability failures.",
                "",
                "| Setting | Listener failures | All-listener failures | Any-listener failures | Source |",
                "|---|---|---:|---:|---|",
            ]
        )
        for row in overlap["overlap"]:
            counts = ", ".join(
                f"{listener}: {count}"
                for listener, count in row["mirror_failures"].items()
            )
            lines.append(
                f"| {row['setting']} | {counts} | {row['all_listener_failure_scenes']} | {row['any_listener_failure_scenes']} | `{overlap['source']}` |"
            )

    if report["gpt55_speaker_smoke"]:
        smoke = report["gpt55_speaker_smoke"]
        lines.extend(
            [
                "",
                "## GPT-5.5 Speaker Smoke",
                "",
                "This section keeps the original 10-scene same-scene smoke comparison and, when present, the full GPT-5.5 speaker audit for all perspective-stress scenes.",
                "",
                "| Same scenes | Existing direct | GPT-5.5 direct | Existing mirror | GPT-5.5 mirror | Existing population | GPT-5.5 population | K=1 robust scenes | Uncached GPT-5.5 speaker calls | Source |",
                "|---:|---:|---:|---:|---:|---:|---:|---|---:|---|",
                "| {same} | {existing_direct} | {gpt55_direct} | {existing_mirror} | {gpt55_mirror} | {existing_population} | {gpt55_population} | {existing_k1} to {gpt55_k1} | {calls} | `{source}` |".format(
                    same=smoke["same_scene_count"],
                    existing_direct=fmt(smoke["existing_direct_success"]),
                    gpt55_direct=fmt(smoke["gpt55_direct_success"]),
                    existing_mirror=fmt(smoke["existing_mirror_success"]),
                    gpt55_mirror=fmt(smoke["gpt55_mirror_success"]),
                    existing_population=fmt(smoke["existing_population_success"]),
                    gpt55_population=fmt(smoke["gpt55_population_success"]),
                    existing_k1=fmt(smoke["existing_k1_robust"]),
                    gpt55_k1=fmt(smoke["gpt55_k1_robust"]),
                    calls=smoke["uncached_speaker_calls"],
                    source=smoke["source"],
                ),
                f"The GPT-5.5 speaker run records {smoke['speaker_total_tokens']} speaker tokens and writes its human-readable report to `{smoke['markdown']}`.",
            ]
        )
        if smoke["progress_extension"]:
            progress = smoke["progress_extension"]
            extension_label = (
                "50-scene speaker audit"
                if progress["n_scenes"] >= 50
                else f"{progress['n_scenes']}-scene extension"
            )
            lines.extend(
                [
                    "",
                    f"{extension_label}:",
                    "",
                    "| Scenes | Direct | Shortest | Mirror | Mirror same-play | Mirror gap | Population | Oracle | K=1 robust | K=2 robust | Uncached speaker calls | Uncached speaker tokens |",
                    "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
                    "| {scenes} | {direct} | {shortest} | {mirror} | {sameplay} | {gap} | {population} | {oracle} | {k1} | {k2} | {calls} | {tokens} |".format(
                        scenes=progress["n_scenes"],
                        direct=fmt(progress["direct_success"]),
                        shortest=fmt(progress["shortest_success"]),
                        mirror=fmt(progress["mirror_success"]),
                        sameplay=fmt(progress["mirror_sameplay"]),
                        gap=fmt(progress["mirror_gap"]),
                        population=fmt(progress["population_success"]),
                        oracle=fmt(progress["oracle_success"]),
                        k1=fmt(progress["k1_robust"]),
                        k2=fmt(progress["k2_robust"]),
                        calls=progress["uncached_speaker_calls"],
                        tokens=progress["uncached_speaker_tokens"],
                    ),
                    "This extension is the current paper-facing speaker-generation evidence when it covers all 50 perspective-stress scenes.",
                ]
            )

    if report["gpt55_followup_plan_status"]:
        status = report["gpt55_followup_plan_status"]
        summary = status["summary"]
        lines.extend(
            [
                "",
                "## GPT-5.5 Follow-Up Plan Status",
                "",
                "This generated claim-boundary audit maps `additional_experiments_gpt55_plan.md` to the current evidence package.",
                f"Covered: {summary['covered']}. Partial: {summary['partial']}. Future: {summary['future']}. Missing evidence paths: {summary['missing_evidence_paths']}.",
                "",
                "| Status | Experiment | Interpretation |",
                "|---|---|---|",
            ]
        )
        for row in status["items"]:
            lines.append(
                f"| {row['status']} | {row['title']} | {row['interpretation']} |"
            )
        lines.extend(
            [
                "",
                "Claim boundary: " + " ".join(status["claim_boundary"]),
            ]
        )

    if report["human_validation_packet"]:
        human = report["human_validation_packet"]
        summary = human["summary"]
        condition_counts = format_counts_equals(summary["condition_counts"])
        lines.extend(
            [
                "",
                "## Human Validation Packet",
                "",
                "This protocol artifact prepares the optional 20-scene human validation sample. It has no collected human annotations, so it should not be cited as human-validation evidence yet.",
                "",
                "| Items | Condition counts | Participant items | Response template | Answer key |",
                "|---:|---|---|---|---|",
                f"| {summary['n_items']} | {condition_counts} | `{human['items']}` | `{human['response_template']}` | `{human['source']}` |",
                "",
                "Participant-facing files exclude condition labels, scene IDs, target IDs, and held-out success rates.",
            ]
        )

    lines.extend(
        [
            "",
            "## No-Coordinate Ablations",
            "",
            "| Run | Mirror | Population | Consensus+info | Oracle | Consensus-minus-mirror 95% CI | Source |",
            "|---|---:|---:|---:|---:|---|---|",
        ]
    )
    for row in report["no_coord_results"]:
        if row["diff"] is None:
            diff_text = "-"
        else:
            diff_text = f"{fmt(row['diff'])} [{fmt(row['ci'][0])}, {fmt(row['ci'][1])}]"
        lines.append(
            f"| {row['label']} | {fmt(row['mirror_cross'])} | {fmt(row['population_cross'])} | {fmt(row['consensus_cross'])} | {fmt(row['oracle_cross'])} | {diff_text} | `{row['summary_path']}` |"
        )

    if report["local_benchmark"]:
        row = report["local_benchmark"]
        lines.extend(
            [
                "",
                "## Local Benchmark-Scale Sanity Check",
                "",
                "This no-API check validates the released generator and local evaluation pipeline at the 600-scene scale specified by the original workshop plan. It is artifact support, not one of the paper-facing API listener results.",
                "",
                "| Scenes | Scenario counts | Mirror cross | Mirror same | Gap | Population | Template | Oracle | Perspective mirror | Source |",
                "|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
                f"| {row['n_scenes']} | {format_counts(row['scenario_counts'])} | {fmt(row['mirror_cross'])} | {fmt(row['mirror_same'])} | {fmt(row['mirror_gap'])} | {fmt(row['population_cross'])} | {fmt(row['template_cross'])} | {fmt(row['oracle_cross'])} | {fmt(row['perspective_mirror_cross'])} | `{row['source']}` |",
            ]
        )

    if report["local_stronger_plan"]:
        local = report["local_stronger_plan"]
        obs = local["key_observations"]
        budget_rows = [
            row
            for row in local["budget_rows"]
            if row["filter"] == "no_exact_coordinates" and row["k"] in {4, 8}
        ]
        selector_rows = [
            row
            for row in local["selector_rows"]
            if (
                row["filter"] == "no_exact_coordinates"
                and row["k"] == 8
                and row["method"] in {"population", "consensus+info", "oracle"}
            )
            or (
                row["scope"] == "combined_1200"
                and row["filter"] == "full"
                and row["k"] == 8
                and row["method"] == "population"
            )
        ]
        lines.extend(
            [
                "",
                "## Local Stronger-Plan K=8 Diagnostic",
                "",
                "This no-API diagnostic exercises the stronger-plan 1,000 initial-family plus 200 partial-observability scale. It is artifact support, not a paper-facing API listener result.",
                "No-coordinate oracle success on the initial 1,000 scenes rises from {k4} at K=4 to {k8} at K=8.".format(
                    k4=fmt(obs["initial_no_coord_oracle_k4"]),
                    k8=fmt(obs["initial_no_coord_oracle_k8"]),
                ),
                "No-coordinate oracle success on the 200 partial-observability scenes rises from {k4} at K=4 to {k8} at K=8.".format(
                    k4=fmt(obs["partial_no_coord_oracle_k4"]),
                    k8=fmt(obs["partial_no_coord_oracle_k8"]),
                ),
                "At K=8 without exact coordinates, consensus+info reaches {initial} on the initial 1,000 scenes and {partial} on partial-observability scenes.".format(
                    initial=fmt(obs["initial_no_coord_consensus_k8"]),
                    partial=fmt(obs["partial_no_coord_consensus_k8"]),
                ),
                "",
                "| Scope | Filter | K | Scenes | Candidates/scene | Robust-scene rate | Oracle | Source |",
                "|---|---|---:|---:|---:|---:|---:|---|",
            ]
        )
        for row in budget_rows:
            lines.append(
                f"| {row['scope']} | {row['filter']} | {row['k']} | {row['n_scenes']} | {fmt(row['mean_candidates'])} | {fmt(row['robust_scene_rate'])} | {fmt(row['oracle_success'])} | `{local['source']}` |"
            )
        lines.extend(
            [
                "",
                "| Scope | Filter | K | Method | Success | Exact-coordinate selection | Source |",
                "|---|---|---:|---|---:|---:|---|",
            ]
        )
        for row in selector_rows:
            lines.append(
                f"| {row['scope']} | {row['filter']} | {row['k']} | {row['method']} | {fmt(row['success'])} | {fmt(row['exact_coordinate_selection_rate'])} | `{local['source']}` |"
            )

    if report["api_leave_one_out"]:
        lines.extend(
            [
                "",
                "## API Listener Leave-One-Out Mechanism Check",
                "",
                "This cache-only post-hoc check selects candidates with one or two API listener prompt variants and evaluates on the held-out prompt.",
                "",
                "| Run | API mirror | API population | Oracle | Population-minus-mirror 95% CI | Source |",
                "|---|---:|---:|---:|---|---|",
            ]
        )
        for row in report["api_leave_one_out"]:
            lines.append(
                f"| {row['label']} | {fmt(row['mirror'])} | {fmt(row['population'])} | {fmt(row['oracle'])} | {fmt(row['diff'])} [{fmt(row['ci'][0])}, {fmt(row['ci'][1])}] | `{row['source']}` |"
            )

    if report["selection_regret"]:
        lines.extend(
            [
                "",
                "## Selection Regret Audit",
                "",
                "Regret is oracle candidate success minus selected-message success, averaged by scene.",
                "",
                "| Run | Method | Success | Oracle | Regret | 95% CI | Source |",
                "|---|---|---:|---:|---:|---|---|",
            ]
        )
        for row in report["selection_regret"]:
            lines.append(
                f"| {row['label']} | {row['method']} | {fmt(row['method_success'])} | {fmt(row['oracle_success'])} | {fmt(row['regret'])} | [{fmt(row['ci'][0])}, {fmt(row['ci'][1])}] | `{row['source']}` |"
            )

    if report["candidate_pool"]["availability"]:
        lines.extend(
            [
                "",
                "## Candidate Pool Robustness Audit",
                "",
                "A robust candidate succeeds with every held-out API listener for that scene.",
                "",
                "| Run | Filter | Scenes | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle | Source |",
                "|---|---|---:|---:|---:|---:|---:|---|",
            ]
        )
        for row in report["candidate_pool"]["availability"]:
            lines.append(
                f"| {row['label']} | {row['filter']} | {row['n_scenes']} | {fmt(row['mean_candidates'])} | {fmt(row['mean_robust_candidates'])} | {fmt(row['robust_scene_rate'])} | {fmt(row['oracle_success'])} | `{row['source']}` |"
            )
        lines.extend(
            [
                "",
                "| Run | Method | Selected success | Robust-selection rate | Oracle-match rate | Source |",
                "|---|---|---:|---:|---:|---|",
            ]
        )
        for row in report["candidate_pool"]["selectors"]:
            lines.append(
                f"| {row['label']} | {row['method']} | {fmt(row['selected_success'])} | {fmt(row['selected_robust_rate'])} | {fmt(row['oracle_match_rate'])} | `{row['source']}` |"
            )

    if report["candidate_budget"]:
        lines.extend(
            [
                "",
                "## Candidate Budget Audit",
                "",
                "Oracle@K is the best held-out success among the first K generated candidates.",
                "",
                "| Run | K | Oracle@K | Robust-scene rate | Source |",
                "|---|---:|---:|---:|---|",
            ]
        )
        for row in report["candidate_budget"]:
            lines.append(
                f"| {row['label']} | {row['k']} | {fmt(row['oracle_success'])} | {fmt(row['robust_scene_rate'])} | `{row['source']}` |"
            )

    if report["candidate_role_selection"]["rows"]:
        role_report = report["candidate_role_selection"]
        summary = role_report["summary"]
        lines.extend(
            [
                "",
                "## Candidate Role Selection Audit",
                "",
                "This cache-only audit maps each selected message back to its original generated candidate slot.",
                "",
                "| Run | Filter | Method | Scenes | Success | Natural first | Attribute short | Relational/spatial | Coordinate fallback | Unresolved | Source |",
                "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
            ]
        )
        for row in role_report["rows"]:
            lines.append(
                f"| {row['label']} | {row['filter']} | {row['method']} | {row['n_scenes']} | {fmt(row['success'])} | {fmt(row['natural_first'])} | {fmt(row['attribute_short'])} | {fmt(row['relational_or_spatial'])} | {fmt(row['coordinate_fallback'])} | {row['unresolved']} | `{row['source']}` |"
            )
        lines.extend(
            [
                "",
                "Full-candidate population coordinate-fallback rates: {rates}.".format(
                    rates=format_label_rates(summary["full_population_coordinate_fallback_rates"])
                ),
                "No-coordinate consensus+info attribute-short rates: {rates}.".format(
                    rates=format_label_rates(summary["no_coord_consensus_attribute_short_rates"])
                ),
            ]
        )

    if report["random_candidate_baseline"]:
        lines.extend(
            [
                "",
                "## Random Candidate Baseline",
                "",
                "The random selector is uniform over available generated candidates and is computed from cached held-out listener evaluations.",
                "",
                "| Run | Filter | Candidates/scene | Random expected | Random robust-pick | Primary selector | Primary-minus-random 95% CI | Source |",
                "|---|---|---:|---:|---:|---|---|---|",
            ]
        )
        for row in report["random_candidate_baseline"]:
            lines.append(
                f"| {row['label']} | {row['filter']} | {fmt(row['mean_candidates'])} | {fmt(row['random_expected'])} | {fmt(row['random_robust_pick'])} | {row['primary_method']} | {fmt(row['primary_minus_random'])} [{fmt(row['ci'][0])}, {fmt(row['ci'][1])}] | `{row['source']}` |"
            )

    if report["message_length_audit"]:
        lines.extend(
            [
                "",
                "## Message Length Audit",
                "",
                "This cache-only audit checks whether selector gains are explained by simply choosing longer messages.",
                "",
                "| Run | Filter | Primary | Mirror tokens | Primary tokens | Token delta | Success delta | Direct tokens | Template tokens | Source |",
                "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
            ]
        )
        for row in report["message_length_audit"]:
            lines.append(
                f"| {row['label']} | {row['filter']} | {row['primary_method']} | {fmt(row['mirror_tokens'])} | {fmt(row['primary_tokens'])} | {fmt(row['token_delta'])} | {fmt(row['success_delta'])} | {fmt(row['direct_tokens'])} | {fmt(row['template_tokens'])} | `{row['source']}` |"
            )

    if report["listener_disagreement"]:
        lines.extend(
            [
                "",
                "## Listener Disagreement Audit",
                "",
                "A split outcome means the selected message succeeds for some held-out listeners but fails for others in the same scene.",
                "",
                "| Run | Method | Success | Unanimous success | Split outcome | Unanimous failure | Choice disagreement | Source |",
                "|---|---|---:|---:|---:|---:|---:|---|",
            ]
        )
        for row in report["listener_disagreement"]:
            lines.append(
                f"| {row['label']} | {row['method']} | {fmt(row['success'])} | {fmt(row['unanimous_success_rate'])} | {fmt(row['split_success_rate'])} | {fmt(row['unanimous_failure_rate'])} | {fmt(row['choice_disagreement_rate'])} | `{row['source']}` |"
            )

    if report["listener_confidence"]:
        lines.extend(
            [
                "",
                "## Listener Confidence Audit",
                "",
                "This cache-only audit checks whether held-out listener confidence and ambiguity flags diagnose selected-message failures.",
                "",
                "| Run | Method | Success | Mean confidence | Ambiguity | Failure confidence | High-conf failure rows | High-conf failure scenes | Source |",
                "|---|---|---:|---:|---:|---:|---:|---:|---|",
            ]
        )
        for row in report["listener_confidence"]:
            lines.append(
                f"| {row['label']} | {row['method']} | {fmt(row['success'])} | {fmt(row['mean_confidence'])} | {fmt(row['ambiguity_rate'])} | {fmt(row['mean_failure_confidence'])} | {fmt(row['high_confidence_failure_rate'])} | {fmt(row['scene_high_confidence_failure_rate'])} | `{row['source']}` |"
            )

    if report["failure_taxonomy"]:
        taxonomy = report["failure_taxonomy"]
        combined = taxonomy["combined"]
        counts = combined["category_counts"]
        other = (
            combined["n_failures"]
            - counts["underspecified_distractor"]
            - counts["perspective_frame_error"]
        )
        lines.extend(
            [
                "",
                "## Failure Taxonomy Audit",
                "",
                "This cache-only audit combines the rubric-coded listener-level mirror failures used in the paper.",
                "",
                "| Failure set | Rows | Underspecified distractor | Perspective-frame error | Other coded categories | Source |",
                "|---|---:|---:|---:|---:|---|",
            ]
        )
        for row in taxonomy["sets"]:
            row_counts = row["category_counts"]
            row_other = (
                row["n_failures"]
                - row_counts["underspecified_distractor"]
                - row_counts["perspective_frame_error"]
            )
            lines.append(
                f"| {row['display']} | {row['n_failures']} | {row_counts['underspecified_distractor']} | {row_counts['perspective_frame_error']} | {row_other} | `{row['path']}` |"
            )
        lines.extend(
            [
                "",
                "| Combined rows | Rows | Underspecified distractor | Perspective-frame error | Other coded categories | Source |",
                "|---|---:|---:|---:|---:|---|",
                f"| combined | {combined['n_failures']} | {counts['underspecified_distractor']} | {counts['perspective_frame_error']} | {other} | `{taxonomy['source']}` |",
            ]
        )

    if report["rule_based_ambiguity"]:
        verifier = report["rule_based_ambiguity"]
        combined = verifier["combined"]
        findings = verifier["key_findings"]
        lines.extend(
            [
                "",
                "## Rule-Based Ambiguity Verifier",
                "",
                "This cache-only non-LLM verifier parses target attributes, row/column mentions, and perspective-sensitive left/right cues.",
                "",
                "| Coded rows | Under-spec recall | Frame recall | Symbolic recall | Under-spec precision | Source |",
                "|---:|---:|---:|---:|---:|---|",
                f"| {combined['n_rows']} | {fmt(combined['underspecified_recall'])} | {fmt(combined['frame_sensitive_recall'])} | {fmt(combined['symbolic_recall'])} | {fmt(combined['underspecified_precision'])} | `{verifier['source']}` |",
                "",
                "| Check | Rate |",
                "|---|---:|",
                f"| perspective mirror failure scenes flagged | {fmt(findings['perspective_mirror_failure_symbolic_rate'])} |",
                f"| perspective population messages flagged | {fmt(findings['perspective_population_symbolic_rate'])} |",
                f"| partial-observability mirror failure scenes flagged | {fmt(findings['partial_mirror_failure_symbolic_rate'])} |",
                f"| partial-observability population messages flagged | {fmt(findings['partial_population_symbolic_rate'])} |",
            ]
        )

    if report["interaction_memory_rules"]:
        memory = report["interaction_memory_rules"]
        combined = memory["combined"]
        lines.extend(
            [
                "",
                "## Interaction Memory Rule Audit",
                "",
                "This replay-only audit derives future speaker-prompt rules from the coded mirror failures and checks whether cached repairs instantiate the relevant cue.",
                "",
                "| Failure set | Repair selector | Category | Failure rows | Failure scenes | Repair success | Repair all-success scenes | Repair cue satisfies rule | Source |",
                "|---|---|---|---:|---:|---:|---:|---:|---|",
            ]
        )
        for failure_set in memory["sets"]:
            for row in failure_set["by_category"]:
                lines.append(
                    f"| {failure_set['label']} | {failure_set['repair_label']} | {row['category']} | {row['failure_rows']} | {row['failure_scenes']} | {fmt(row['mean_repair_success_on_failure_scenes'])} | {fmt(row['repair_all_success_scene_rate'])} | {fmt(row['repair_rule_cue_rate'])} | `{memory['source']}` |"
                )
        lines.extend(
            [
                "",
                "Coded failure rows: {rows}; unique failure scenes: {scenes}; rule counts: {counts}; mean repair success on failure scenes: {success}; repair cue satisfies derived rule in {cue} of failure scenes.".format(
                    rows=combined["n_failure_rows"],
                    scenes=combined["n_failure_scenes"],
                    counts=format_counts(combined["rule_counts"]),
                    success=fmt(combined["mean_repair_success_on_failure_scenes"]),
                    cue=fmt(combined["repair_rule_cue_rate"]),
                ),
            ]
        )

    if report["qualitative_examples"]:
        lines.extend(
            [
                "",
                "## Qualitative Failure Examples",
                "",
                "Representative cache-only examples link selected messages to held-out listener choices and scene context.",
                "These four cache-only examples show mirror-selected messages failing held-out listeners while population or consensus+info repairs succeed.",
                "",
                "| Example | Scene | Category | Mirror success | Repair | Repair success | Source |",
                "|---|---|---|---:|---|---:|---|",
            ]
        )
        for row in report["qualitative_examples"]:
            lines.append(
                f"| {row['title']} | `{row['scene_id']}` | {row['category']} | {fmt(row['mirror_success'])} | {row['repair_label']} | {fmt(row['repair_success'])} | `{row['source']}` |"
            )

    if report["reviewer_checklist"]:
        checklist = report["reviewer_checklist"]
        lines.extend(
            [
                "",
                "## Reviewer Checklist",
                "",
                "This materializes Section 32 of the original workshop plan as a generated checklist tied to current artifacts.",
                f"Items passed: {checklist['n_items'] - checklist['n_failed']}/{checklist['n_items']}.",
                "",
                "| Section | Passed | Failed | Source |",
                "|---|---:|---:|---|",
            ]
        )
        for section, counts in checklist["sections"].items():
            lines.append(
                f"| {section} | {counts['passed']} | {counts['failed']} | `{checklist['markdown']}` |"
            )

    if report["plan_coverage"]:
        coverage = report["plan_coverage"]
        counts = coverage["status_counts"]
        core = coverage["core_status_counts"]
        stretch = coverage["stretch_status_counts"]
        lines.extend(
            [
                "",
                "## Plan Coverage Audit",
                "",
                "This generated audit maps the original workshop plan to the current artifacts and separates claimed core coverage from partial or open stretch items.",
                f"Overall: {counts['covered']} covered, {counts['partial']} partial, {counts['open']} open across {coverage['n_items']} plan items.",
                f"Core scope: {core['covered']} covered, {core['partial']} partial, {core['open']} open.",
                f"Stretch scope: {stretch['covered']} covered, {stretch['partial']} partial, {stretch['open']} open.",
                "",
                "| Status | Scope | Plan item | Detail | Source |",
                "|---|---|---|---|---|",
            ]
        )
        for row in coverage["open_or_partial"]:
            lines.append(
                f"| {row['status']} | {row['scope']} | {row['plan_item']} | {row['detail']} | `{coverage['markdown']}` |"
            )

    lines.extend(
        [
            "",
            "## Claim-To-Evidence Map",
            "",
            "| Claim | Evidence files | Anchor |",
            "|---|---|---|",
        ]
    )
    for row in report["claim_map"]:
        lines.append(f"| {row['claim']} | `{row['evidence']}` | {row['anchor']} |")

    lines.extend(
        [
            "",
            "## Quality Gates",
            "",
            "| Gate | Checks | Failed | Warnings | Open actions | Source |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in report["quality_gates"]:
        lines.append(
            f"| {row['name']} | {row['checks']} | {row['failed']} | {row['warnings']} | {row['actions']} | `{row['path']}` |"
        )

    lines.extend(
        [
            "",
            "## Refresh Commands",
            "",
            "These commands do not require new API calls when the cached artifacts are present.",
            "",
            "```bash",
            "conda run -n cross_play python scripts/audit_benchmark_integrity.py \\",
            "  --markdown-out results/benchmark_integrity_audit.md \\",
            "  --json-out results/benchmark_integrity_audit.json",
            "",
            "conda run -n cross_play python scripts/verify_paper_claims.py \\",
            "  --markdown-out results/paper_claims_verification.md \\",
            "  --json-out results/paper_claims_verification.json",
            "",
            "conda run -n cross_play python scripts/run_local_pilot.py \\",
            "  --seed 7 --k 4 \\",
            "  --unique 150 --contrast 150 --relational 150 --perspective 150 --partial 0 \\",
            "  --scene-out data/local_benchmark600_scenes.jsonl \\",
            "  --records-out results/local_benchmark600_records.jsonl \\",
            "  --summary-out results/local_benchmark600_summary.json \\",
            "  --markdown-out results/local_benchmark600_summary.md",
            "",
            "conda run -n cross_play python scripts/analyze_local_benchmark.py \\",
            "  --scene-file data/local_benchmark600_scenes.jsonl \\",
            "  --records results/local_benchmark600_records.jsonl \\",
            "  --markdown-out docs/local_benchmark600_check.md \\",
            "  --json-out results/local_benchmark600_check.json",
            "",
            "conda run -n cross_play python scripts/analyze_local_stronger_plan.py \\",
            "  --scene-out data/local_stronger_plan1200_scenes.jsonl \\",
            "  --markdown-out docs/local_stronger_plan_k8.md \\",
            "  --json-out results/local_stronger_plan_k8.json",
            "",
            "conda run -n cross_play python scripts/analyze_cross_model_failure_overlap.py \\",
            "  --json-out results/cross_model_failure_overlap.json \\",
            "  --markdown-out docs/cross_model_failure_overlap.md \\",
            "  --units-out results/cross_model_failure_overlap_units.jsonl",
            "",
            "conda run -n cross_play python scripts/analyze_api_listener_leave_one_out.py \\",
            "  --records mixed_50=results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl \\",
            "  --records perspective_gpt54=results/perspective_stress50_hybrid_candidate_eval_records.jsonl \\",
            "  --records perspective_gpt41=results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl \\",
            "  --records partial_observability=results/partial_observability_api50_candidate_eval_records.jsonl \\",
            "  --markdown-out docs/api_listener_leave_one_out.md \\",
            "  --json-out results/api_listener_leave_one_out.json \\",
            "  --tex-out paper/tables/api_listener_leave_one_out.tex",
            "",
            "conda run -n cross_play python scripts/analyze_selection_regret.py \\",
            "  --markdown-out docs/selection_regret_audit.md \\",
            "  --json-out results/selection_regret_audit.json",
            "",
            "conda run -n cross_play python scripts/analyze_candidate_pool.py \\",
            "  --markdown-out docs/candidate_pool_audit.md \\",
            "  --json-out results/candidate_pool_audit.json",
            "",
            "conda run -n cross_play python scripts/analyze_candidate_budget.py \\",
            "  --markdown-out docs/candidate_budget_audit.md \\",
            "  --json-out results/candidate_budget_audit.json",
            "",
            "conda run -n cross_play python scripts/analyze_candidate_role_selection.py \\",
            "  --markdown-out docs/candidate_role_selection_audit.md \\",
            "  --json-out results/candidate_role_selection_audit.json",
            "",
            "conda run -n cross_play python scripts/analyze_random_candidate_baseline.py \\",
            "  --markdown-out docs/random_candidate_baseline.md \\",
            "  --json-out results/random_candidate_baseline.json",
            "",
            "conda run -n cross_play python scripts/analyze_message_length_audit.py \\",
            "  --markdown-out docs/message_length_audit.md \\",
            "  --json-out results/message_length_audit.json",
            "",
            "conda run -n cross_play python scripts/analyze_listener_disagreement.py \\",
            "  --markdown-out docs/listener_disagreement_audit.md \\",
            "  --json-out results/listener_disagreement_audit.json",
            "",
            "conda run -n cross_play python scripts/analyze_failure_taxonomy.py \\",
            "  --markdown-out docs/failure_taxonomy_audit.md \\",
            "  --json-out results/failure_taxonomy_audit.json \\",
            "  --tex-out paper/tables/failure_taxonomy_combined.tex",
            "",
            "conda run -n cross_play python scripts/analyze_rule_based_ambiguity.py \\",
            "  --markdown-out docs/rule_based_ambiguity_verifier.md \\",
            "  --json-out results/rule_based_ambiguity_verifier.json \\",
            "  --units-out results/rule_based_ambiguity_verifier_units.jsonl",
            "",
            "conda run -n cross_play python scripts/analyze_interaction_memory_rules.py \\",
            "  --markdown-out docs/interaction_memory_rules.md \\",
            "  --json-out results/interaction_memory_rules.json",
            "",
            "conda run -n cross_play python scripts/make_qualitative_examples.py \\",
            "  --markdown-out docs/qualitative_failure_examples.md \\",
            "  --json-out results/qualitative_failure_examples.json",
            "",
            "conda run -n cross_play python scripts/make_reviewer_checklist.py \\",
            "  --markdown-out docs/reviewer_checklist.md \\",
            "  --json-out results/reviewer_checklist.json",
            "",
            "conda run -n cross_play python scripts/audit_plan_coverage.py \\",
            "  --markdown-out docs/plan_coverage_audit.md \\",
            "  --json-out results/plan_coverage_audit.json",
            "",
            "conda run -n cross_play python scripts/audit_submission_readiness.py \\",
            "  --markdown-out results/submission_readiness_audit.md \\",
            "  --json-out results/submission_readiness_audit.json",
            "",
            "conda run -n cross_play python scripts/make_artifact_guide.py \\",
            "  --out docs/artifact_guide.md",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def read_json(path: str | None) -> Any:
    if path is None:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def method_row(source: dict[str, Any], method: str) -> dict[str, Any]:
    for row in source["methods"]:
        if row["method"] == method:
            return row
    raise KeyError(method)


def format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}:{value}" for key, value in counts.items())


def format_counts_equals(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={value}" for key, value in counts.items())


def format_label_rates(rows: list[dict[str, Any]]) -> str:
    return ", ".join(f"{row['label']}={row['rate']:.3f}" for row in rows)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    main()
