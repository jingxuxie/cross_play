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

from prag_crossplay.data import read_jsonl, read_scenes
from prag_crossplay.scoring import paired_method_comparison, summarize_records

EXACT_COORD_RE = re.compile(
    r"\brow\s+\d+\b|\bcolumn\s+\d+\b|\b\d+(?:st|nd|rd|th)?\s+row\b|\b\d+(?:st|nd|rd|th)?\s+column\b",
    re.IGNORECASE,
)
SPATIAL_RE = re.compile(
    r"\bleft\b|\bright\b|\bleftmost\b|\brightmost\b|\bfarthest\b|\bclosest\b|"
    r"\babove\b|\bbelow\b|\bnext to\b|\bbeside\b|\bbetween\b|\bamong\b",
    re.IGNORECASE,
)

METHODS = {
    "direct": "api_direct_first",
    "shortest": "api_best_of_k_shortest",
    "mirror": "hybrid_local_mirror_api_eval",
    "population": "hybrid_local_population_api_eval",
    "oracle": "oracle_upper_bound",
    "template": "template",
    "no_direct": "no_coord_direct_first",
    "no_shortest": "no_coord_best_of_k_shortest",
    "no_mirror": "no_coord_mirror",
    "no_population": "no_coord_population",
    "no_consensus_info": "no_coord_consensus_info",
    "no_informative": "no_coord_informative",
    "no_oracle": "no_coord_oracle",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="results/paper_claims_verification.md")
    parser.add_argument("--json-out", default="results/paper_claims_verification.json")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    check_summary_values(checks)
    check_paired_values(checks)
    check_failure_coding(checks)
    check_mechanism_counts(checks)
    check_local_extension(checks)
    check_local_benchmark600(checks)
    check_local_stronger_plan(checks)
    check_partial_api_extension(checks)
    check_api_listener_leave_one_out(checks)
    check_selection_regret(checks)
    check_candidate_pool(checks)
    check_candidate_budget(checks)
    check_candidate_role_selection(checks)
    check_random_candidate_baseline(checks)
    check_message_length_audit(checks)
    check_listener_disagreement(checks)
    check_listener_confidence_audit(checks)
    check_failure_taxonomy(checks)
    check_interaction_memory_rules(checks)
    check_qualitative_examples(checks)
    check_reviewer_checklist(checks)
    check_plan_coverage(checks)
    check_integrity_audit(checks)
    check_api_token_accounting(checks)
    check_required_text(checks)

    failed = [check for check in checks if not check["ok"]]
    report = {
        "n_checks": len(checks),
        "n_failed": len(failed),
        "checks": checks,
    }
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown_report(checks), encoding="utf-8")
    print(markdown_report(checks))
    if failed:
        raise SystemExit(1)


def check_summary_values(checks: list[dict[str, Any]]) -> None:
    cases = [
        (
            "mixed_full",
            "results/hybrid_api_pilot50_allcand_records.jsonl",
            {
                ("direct", "success"): 0.840,
                ("shortest", "success"): 0.740,
                ("mirror", "success"): 0.907,
                ("mirror", "sameplay_success"): 1.000,
                ("mirror", "crossplay_gap"): 0.093,
                ("population", "success"): 1.000,
                ("population", "sameplay_success"): 1.000,
                ("oracle", "success"): 1.000,
            },
        ),
        (
            "stress_gpt54",
            "results/perspective_stress50_hybrid_records.jsonl",
            {
                ("direct", "success"): 0.713,
                ("shortest", "success"): 0.420,
                ("mirror", "success"): 0.813,
                ("mirror", "sameplay_success"): 1.000,
                ("mirror", "crossplay_gap"): 0.187,
                ("population", "success"): 1.000,
                ("oracle", "success"): 1.000,
            },
        ),
        (
            "stress_gpt41",
            "results/perspective_stress50_gpt41nano_records.jsonl",
            {
                ("direct", "success"): 0.553,
                ("shortest", "success"): 0.367,
                ("mirror", "success"): 0.713,
                ("mirror", "sameplay_success"): 1.000,
                ("mirror", "crossplay_gap"): 0.287,
                ("population", "success"): 1.000,
                ("oracle", "success"): 1.000,
            },
        ),
        (
            "stress_no_coord",
            "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
            {
                ("no_direct", "success"): 0.553,
                ("no_shortest", "success"): 0.367,
                ("no_mirror", "success"): 0.580,
                ("no_mirror", "sameplay_success"): 1.000,
                ("no_mirror", "crossplay_gap"): 0.420,
                ("no_population", "success"): 0.420,
                ("no_population", "sameplay_success"): 0.520,
                ("no_consensus_info", "success"): 0.760,
                ("no_informative", "success"): 0.760,
                ("no_oracle", "success"): 0.793,
            },
        ),
        (
            "mixed_no_coord",
            "results/hybrid_api_pilot50_no_coord_records.jsonl",
            {
                ("no_direct", "success"): 0.840,
                ("no_shortest", "success"): 0.740,
                ("no_mirror", "success"): 0.787,
                ("no_mirror", "sameplay_success"): 0.880,
                ("no_mirror", "crossplay_gap"): 0.093,
                ("no_population", "success"): 0.773,
                ("no_population", "sameplay_success"): 0.813,
                ("no_consensus_info", "success"): 0.920,
                ("no_informative", "success"): 0.900,
                ("no_oracle", "success"): 0.960,
            },
        ),
    ]
    for label, path, expected in cases:
        summary = summarize_records(read_jsonl(path))
        for (method_key, metric), expected_value in expected.items():
            method = METHODS[method_key]
            actual = summary["by_method"][method][metric]
            add_numeric_check(
                checks,
                f"{label}.{method}.{metric}",
                actual,
                expected_value,
                decimals=3,
                source=path,
            )


def check_paired_values(checks: list[dict[str, Any]]) -> None:
    cases = [
        (
            "mixed_full.pop_minus_mirror",
            "results/hybrid_api_pilot50_allcand_records.jsonl",
            METHODS["population"],
            METHODS["mirror"],
            None,
            0.093,
            (0.027, 0.173),
            0.0024,
            50,
        ),
        (
            "mixed_full.perspective_pop_minus_mirror",
            "results/hybrid_api_pilot50_allcand_records.jsonl",
            METHODS["population"],
            METHODS["mirror"],
            "perspective_shift",
            0.367,
            (0.133, 0.600),
            0.0004,
            10,
        ),
        (
            "stress_gpt54.pop_minus_mirror",
            "results/perspective_stress50_hybrid_records.jsonl",
            METHODS["population"],
            METHODS["mirror"],
            None,
            0.187,
            (0.100, 0.287),
            0.0000,
            50,
        ),
        (
            "stress_gpt41.pop_minus_mirror",
            "results/perspective_stress50_gpt41nano_records.jsonl",
            METHODS["population"],
            METHODS["mirror"],
            None,
            0.287,
            (0.193, 0.380),
            0.0000,
            50,
        ),
        (
            "stress_no_coord.consensus_minus_mirror",
            "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
            METHODS["no_consensus_info"],
            METHODS["no_mirror"],
            None,
            0.180,
            (0.100, 0.267),
            0.0000,
            50,
        ),
        (
            "mixed_no_coord.consensus_minus_mirror",
            "results/hybrid_api_pilot50_no_coord_records.jsonl",
            METHODS["no_consensus_info"],
            METHODS["no_mirror"],
            None,
            0.133,
            (0.033, 0.233),
            0.0040,
            50,
        ),
    ]
    for label, path, method_a, method_b, scenario, diff, ci, p_value, n_pairs in cases:
        comp = paired_method_comparison(read_jsonl(path), method_a, method_b, scenario_type=scenario)
        add_numeric_check(checks, f"{label}.n_pairs", comp["n_pairs"], n_pairs, decimals=0, source=path)
        add_numeric_check(checks, f"{label}.diff", comp["diff_a_minus_b"], diff, decimals=3, source=path)
        add_numeric_check(checks, f"{label}.ci_low", comp["diff_ci95"][0], ci[0], decimals=3, source=path)
        add_numeric_check(checks, f"{label}.ci_high", comp["diff_ci95"][1], ci[1], decimals=3, source=path)
        add_numeric_check(
            checks,
            f"{label}.p_boot",
            comp["paired_bootstrap_p_two_sided"],
            p_value,
            decimals=4,
            source=path,
        )


def check_failure_coding(checks: list[dict[str, Any]]) -> None:
    path = "results/perspective_stress50_gpt41nano_mirror_failures_coded.csv"
    with Path(path).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    counts = Counter(row["author_category"] for row in rows)
    add_numeric_check(checks, "coded_failures.total", len(rows), 43, decimals=0, source=path)
    add_numeric_check(
        checks,
        "coded_failures.underspecified_distractor",
        counts["underspecified_distractor"],
        38,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "coded_failures.perspective_frame_error",
        counts["perspective_frame_error"],
        5,
        decimals=0,
        source=path,
    )

    partial_path = "results/partial_observability_api50_mirror_failures_coded.csv"
    with Path(partial_path).open(newline="", encoding="utf-8") as f:
        partial_rows = list(csv.DictReader(f))
    partial_counts = Counter(row["author_category"] for row in partial_rows)
    add_numeric_check(checks, "partial_coded_failures.total", len(partial_rows), 50, decimals=0, source=partial_path)
    add_numeric_check(
        checks,
        "partial_coded_failures.underspecified_distractor",
        partial_counts["underspecified_distractor"],
        50,
        decimals=0,
        source=partial_path,
    )

    partial_no_coord_path = "results/partial_observability_api50_no_coord_mirror_failures_coded.csv"
    with Path(partial_no_coord_path).open(newline="", encoding="utf-8") as f:
        partial_no_coord_rows = list(csv.DictReader(f))
    partial_no_coord_counts = Counter(row["author_category"] for row in partial_no_coord_rows)
    add_numeric_check(
        checks,
        "partial_no_coord_coded_failures.total",
        len(partial_no_coord_rows),
        59,
        decimals=0,
        source=partial_no_coord_path,
    )
    add_numeric_check(
        checks,
        "partial_no_coord_coded_failures.underspecified_distractor",
        partial_no_coord_counts["underspecified_distractor"],
        59,
        decimals=0,
        source=partial_no_coord_path,
    )


def check_mechanism_counts(checks: list[dict[str, Any]]) -> None:
    full = read_jsonl("results/perspective_stress50_gpt41nano_audit.jsonl")
    stress_no = read_jsonl("results/perspective_stress50_gpt41nano_no_coord_audit.jsonl")
    mixed_no = read_jsonl("results/hybrid_api_pilot50_no_coord_audit.jsonl")

    add_numeric_check(
        checks,
        "mechanism.stress_full.population_exact_coord",
        count_regex(full, "population_selected", EXACT_COORD_RE),
        50,
        decimals=0,
        source="results/perspective_stress50_gpt41nano_audit.jsonl",
    )
    add_numeric_check(
        checks,
        "mechanism.stress_full.mirror_exact_coord",
        count_regex(full, "mirror_selected", EXACT_COORD_RE),
        17,
        decimals=0,
        source="results/perspective_stress50_gpt41nano_audit.jsonl",
    )
    add_numeric_check(
        checks,
        "mechanism.stress_no_coord.population_spatial",
        count_regex(stress_no, "population_selected", SPATIAL_RE),
        4,
        decimals=0,
        source="results/perspective_stress50_gpt41nano_no_coord_audit.jsonl",
    )
    add_numeric_check(
        checks,
        "mechanism.stress_no_coord.consensus_info_spatial",
        count_regex(stress_no, "consensus_info_selected", SPATIAL_RE),
        50,
        decimals=0,
        source="results/perspective_stress50_gpt41nano_no_coord_audit.jsonl",
    )
    stress_sources = Counter(row["consensus_info_source"] for row in stress_no)
    add_numeric_check(
        checks,
        "mechanism.stress_no_coord.consensus_info_fallback",
        stress_sources["informativeness_fallback"],
        50,
        decimals=0,
        source="results/perspective_stress50_gpt41nano_no_coord_audit.jsonl",
    )
    mixed_sources = Counter(row["consensus_info_source"] for row in mixed_no)
    add_numeric_check(
        checks,
        "mechanism.mixed_no_coord.consensus_source",
        mixed_sources["consensus"],
        32,
        decimals=0,
        source="results/hybrid_api_pilot50_no_coord_audit.jsonl",
    )
    add_numeric_check(
        checks,
        "mechanism.mixed_no_coord.fallback_source",
        mixed_sources["informativeness_fallback"],
        18,
        decimals=0,
        source="results/hybrid_api_pilot50_no_coord_audit.jsonl",
    )


def check_integrity_audit(checks: list[dict[str, Any]]) -> None:
    path = "results/benchmark_integrity_audit.json"
    if not Path(path).exists():
        add_bool_check(checks, "integrity_audit.exists", False, source=path)
        return
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    add_numeric_check(
        checks,
        "integrity_audit.n_failed",
        report.get("n_failed", -1),
        0,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "integrity_audit.n_checks",
        report.get("n_checks", -1),
        158,
        decimals=0,
        source=path,
    )
    groups = {row.get("name"): row for row in report.get("summary", {}).get("groups", [])}
    local_group = groups.get("local_benchmark600", {})
    add_numeric_check(
        checks,
        "integrity_audit.local_benchmark600.scenes",
        local_group.get("n_scenes", -1),
        600,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "integrity_audit.local_benchmark600.record_rows",
        local_group.get("record_rows", -1),
        10800,
        decimals=0,
        source=path,
    )
    model_versions = {
        (row.get("requested_model"), row.get("response_model"))
        for row in report.get("summary", {}).get("cache", {}).get("model_versions", [])
    }
    add_bool_check(
        checks,
        "integrity_audit.has_exact_gpt54_version",
        ("gpt-5.4-nano", "gpt-5.4-nano-2026-03-17") in model_versions,
        source=path,
    )
    add_bool_check(
        checks,
        "integrity_audit.has_exact_gpt41_version",
        ("gpt-4.1-nano", "gpt-4.1-nano-2025-04-14") in model_versions,
        source=path,
    )


def check_api_token_accounting(checks: list[dict[str, Any]]) -> None:
    path = "results/api_token_accounting.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    totals = report["totals"]
    add_numeric_check(checks, "api_token_accounting.n_cache_files", report["n_cache_files"], 3520, decimals=0, source=path)
    add_numeric_check(checks, "api_token_accounting.n_readable", report["n_readable"], 3520, decimals=0, source=path)
    add_numeric_check(checks, "api_token_accounting.n_missing_usage", report["n_missing_usage"], 0, decimals=0, source=path)
    add_numeric_check(checks, "api_token_accounting.input_tokens", totals["input_tokens"], 940088, decimals=0, source=path)
    add_numeric_check(checks, "api_token_accounting.output_tokens", totals["output_tokens"], 87829, decimals=0, source=path)
    add_numeric_check(checks, "api_token_accounting.total_tokens", totals["total_tokens"], 1027917, decimals=0, source=path)

    by_model = {
        (row["requested_model"], row["response_model"]): row
        for row in report["by_model"]
    }
    expected_models = {
        ("gpt-4.1-nano", "gpt-4.1-nano-2025-04-14"): {
            "responses": 750,
            "total_tokens": 207207,
        },
        ("gpt-5.4-nano", "gpt-5.4-nano-2026-03-17"): {
            "responses": 2770,
            "total_tokens": 820710,
        },
    }
    for key, values in expected_models.items():
        row = by_model[key]
        label = ".".join(key)
        add_numeric_check(
            checks,
            f"api_token_accounting.{label}.responses",
            row["n_responses"],
            values["responses"],
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"api_token_accounting.{label}.total_tokens",
            row["total_tokens"],
            values["total_tokens"],
            decimals=0,
            source=path,
        )


def check_local_extension(checks: list[dict[str, Any]]) -> None:
    scene_path = "data/partial_observability_local50_scenes.jsonl"
    summary_path = "results/partial_observability_local50_summary.json"
    scenes = read_scenes(scene_path)
    hidden_private = [
        scene
        for scene in scenes
        if any(
            obj.id == scene.metadata.get("private_landmark_id") and not obj.visible_to_listener
            for obj in scene.objects
        )
    ]
    add_numeric_check(checks, "partial_local.n_scenes", len(scenes), 50, decimals=0, source=scene_path)
    add_numeric_check(
        checks,
        "partial_local.hidden_private_landmarks",
        len(hidden_private),
        50,
        decimals=0,
        source=scene_path,
    )

    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    expected = {
        ("direct", "success"): 0.493,
        ("mirror_selfplay", "success"): 0.653,
        ("mirror_selfplay", "sameplay_success"): 1.000,
        ("mirror_selfplay", "crossplay_gap"): 0.347,
        ("population_play", "success"): 1.000,
        ("population_play", "sameplay_success"): 1.000,
        ("oracle_upper_bound", "success"): 1.000,
    }
    for (method, metric), expected_value in expected.items():
        add_numeric_check(
            checks,
            f"partial_local.{method}.{metric}",
            summary["by_method"][method][metric],
            expected_value,
            decimals=3,
            source=summary_path,
        )


def check_local_benchmark600(checks: list[dict[str, Any]]) -> None:
    scene_path = "data/local_benchmark600_scenes.jsonl"
    report_path = "results/local_benchmark600_check.json"
    scenes = read_scenes(scene_path)
    scenario_counts = Counter(scene.scenario_type for scene in scenes)
    add_numeric_check(checks, "local_benchmark600.n_scenes", len(scenes), 600, decimals=0, source=scene_path)
    for scenario in [
        "unique_attribute",
        "distractor_contrast",
        "relational_reference",
        "perspective_shift",
    ]:
        add_numeric_check(
            checks,
            f"local_benchmark600.{scenario}.n_scenes",
            scenario_counts[scenario],
            150,
            decimals=0,
            source=scene_path,
        )

    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    obs = report["key_observations"]
    expected = {
        "mirror_cross": 0.631,
        "mirror_same": 1.000,
        "mirror_gap": 0.369,
        "population_cross": 1.000,
        "template_cross": 1.000,
        "oracle_cross": 1.000,
        "perspective_mirror_cross": 0.158,
        "perspective_mirror_gap": 0.842,
    }
    for key, expected_value in expected.items():
        add_numeric_check(
            checks,
            f"local_benchmark600.{key}",
            obs[key],
            expected_value,
            decimals=3,
            source=report_path,
        )


def check_local_stronger_plan(checks: list[dict[str, Any]]) -> None:
    scene_path = "data/local_stronger_plan1200_scenes.jsonl"
    report_path = "results/local_stronger_plan_k8.json"
    scenes = read_scenes(scene_path)
    scenario_counts = Counter(scene.scenario_type for scene in scenes)
    add_numeric_check(checks, "local_stronger_plan.n_scenes", len(scenes), 1200, decimals=0, source=scene_path)
    expected_counts = {
        "unique_attribute": 250,
        "distractor_contrast": 250,
        "relational_reference": 250,
        "perspective_shift": 250,
        "partial_observability": 200,
    }
    for scenario, expected in expected_counts.items():
        add_numeric_check(
            checks,
            f"local_stronger_plan.{scenario}.n_scenes",
            scenario_counts[scenario],
            expected,
            decimals=0,
            source=scene_path,
        )

    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    obs = report["key_observations"]
    expected_obs = {
        "initial_no_coord_oracle_k4": 0.870,
        "initial_no_coord_oracle_k8": 0.995,
        "partial_no_coord_oracle_k4": 0.495,
        "partial_no_coord_oracle_k8": 0.997,
        "initial_no_coord_consensus_k8": 0.992,
        "partial_no_coord_consensus_k8": 0.997,
        "combined_full_population_k8": 1.000,
    }
    for key, expected_value in expected_obs.items():
        add_numeric_check(
            checks,
            f"local_stronger_plan.{key}",
            obs[key],
            expected_value,
            decimals=3,
            source=report_path,
        )

    budget = {(row["scope"], row["filter"], row["k"]): row for row in report["budget_rows"]}
    budget_expected = {
        ("combined_1200", "no_exact_coordinates", 4): {"oracle": 0.808, "robust": 0.613},
        ("combined_1200", "no_exact_coordinates", 8): {"oracle": 0.995, "robust": 0.990},
        ("partial_200", "no_exact_coordinates", 8): {"oracle": 0.997, "robust": 0.995},
    }
    for key, values in budget_expected.items():
        row = budget[key]
        label = ".".join(str(part) for part in key)
        add_numeric_check(
            checks,
            f"local_stronger_plan.budget.{label}.oracle",
            row["oracle_success"],
            values["oracle"],
            decimals=3,
            source=report_path,
        )
        add_numeric_check(
            checks,
            f"local_stronger_plan.budget.{label}.robust_scene_rate",
            row["robust_scene_rate"],
            values["robust"],
            decimals=3,
            source=report_path,
        )

    selectors = {
        (row["scope"], row["filter"], row["k"], row["method"]): row
        for row in report["selector_rows"]
    }
    selector_expected = {
        ("combined_1200", "no_exact_coordinates", 8, "consensus+info"): 0.993,
        ("combined_1200", "no_exact_coordinates", 8, "population"): 0.984,
        ("combined_1200", "full", 8, "population"): 1.000,
    }
    for key, expected_value in selector_expected.items():
        row = selectors[key]
        label = ".".join(str(part) for part in key)
        add_numeric_check(
            checks,
            f"local_stronger_plan.selector.{label}.success",
            row["success"],
            expected_value,
            decimals=3,
            source=report_path,
        )


def check_partial_api_extension(checks: list[dict[str, Any]]) -> None:
    summary_path = "results/partial_observability_api50_summary.json"
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    expected = {
        ("api_direct_first", "success"): 0.740,
        ("api_best_of_k_shortest", "success"): 0.313,
        ("hybrid_local_mirror_api_eval", "success"): 0.667,
        ("hybrid_local_mirror_api_eval", "sameplay_success"): 1.000,
        ("hybrid_local_mirror_api_eval", "crossplay_gap"): 0.333,
        ("hybrid_local_population_api_eval", "success"): 1.000,
        ("hybrid_local_population_api_eval", "sameplay_success"): 1.000,
        ("oracle_upper_bound", "success"): 1.000,
    }
    for (method, metric), expected_value in expected.items():
        add_numeric_check(
            checks,
            f"partial_api.{method}.{metric}",
            summary["by_method"][method][metric],
            expected_value,
            decimals=3,
            source=summary_path,
        )

    no_coord_path = "results/partial_observability_api50_no_coord_summary.json"
    no_coord = json.loads(Path(no_coord_path).read_text(encoding="utf-8"))
    no_coord_expected = {
        ("no_coord_direct_first", "success"): 0.740,
        ("no_coord_best_of_k_shortest", "success"): 0.313,
        ("no_coord_mirror", "success"): 0.607,
        ("no_coord_mirror", "sameplay_success"): 0.920,
        ("no_coord_mirror", "crossplay_gap"): 0.313,
        ("no_coord_population", "success"): 0.727,
        ("no_coord_consensus_info", "success"): 0.987,
        ("no_coord_informative", "success"): 0.973,
        ("no_coord_oracle", "success"): 1.000,
    }
    for (method, metric), expected_value in no_coord_expected.items():
        add_numeric_check(
            checks,
            f"partial_api_no_coord.{method}.{metric}",
            no_coord["by_method"][method][metric],
            expected_value,
            decimals=3,
            source=no_coord_path,
        )

    audit_path = "results/partial_observability_api50_check.json"
    audit = json.loads(Path(audit_path).read_text(encoding="utf-8"))["message_audit"]
    add_numeric_check(
        checks,
        "partial_api.private_landmark_candidate_refs",
        audit.get("private_landmark_candidate_refs", 0),
        0,
        decimals=0,
        source=audit_path,
    )
    add_numeric_check(
        checks,
        "partial_api.coordinate_candidates",
        audit.get("coordinate_candidates", 0),
        50,
        decimals=0,
        source=audit_path,
    )
    add_numeric_check(
        checks,
        "partial_api.mirror_private_refs",
        audit["selected"].get("mirror_selected.private_landmark_ref", 0),
        0,
        decimals=0,
        source=audit_path,
    )
    add_numeric_check(
        checks,
        "partial_api.population_private_refs",
        audit["selected"].get("population_selected.private_landmark_ref", 0),
        0,
        decimals=0,
        source=audit_path,
    )


def check_api_listener_leave_one_out(checks: list[dict[str, Any]]) -> None:
    path = "results/api_listener_leave_one_out.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    expected = {
        "mixed_50": {
            "mirror": 0.953,
            "population": 0.973,
            "oracle": 1.000,
            "diff": 0.020,
            "n_units": 150,
        },
        "perspective_gpt54": {
            "mirror": 0.907,
            "population": 0.933,
            "oracle": 1.000,
            "diff": 0.027,
            "n_units": 150,
        },
        "perspective_gpt41": {
            "mirror": 0.847,
            "population": 0.940,
            "oracle": 1.000,
            "diff": 0.093,
            "n_units": 150,
        },
        "partial_observability": {
            "mirror": 0.767,
            "population": 0.940,
            "oracle": 1.000,
            "diff": 0.173,
            "n_units": 150,
        },
    }
    by_label = {dataset["label"]: dataset for dataset in report["datasets"]}
    for label, values in expected.items():
        dataset = by_label[label]
        summary = dataset["summary"]
        paired = dataset["paired_population_minus_mirror"]
        add_numeric_check(
            checks,
            f"api_loo.{label}.mirror",
            summary["loo_api_mirror"]["success"],
            values["mirror"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"api_loo.{label}.population",
            summary["loo_api_population"]["success"],
            values["population"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"api_loo.{label}.oracle",
            summary["loo_api_oracle"]["success"],
            values["oracle"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"api_loo.{label}.population_minus_mirror",
            paired["diff_population_minus_mirror"],
            values["diff"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"api_loo.{label}.n_units",
            paired["n_units"],
            values["n_units"],
            decimals=0,
            source=path,
        )


def check_selection_regret(checks: list[dict[str, Any]]) -> None:
    path = "results/selection_regret_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run_method = {
        (run["label"], row["method_label"]): row
        for run in report["runs"]
        for row in run["rows"]
    }
    expected = {
        ("mixed_50_full", "mirror"): 0.093,
        ("perspective_gpt54_full", "mirror"): 0.187,
        ("perspective_gpt41_full", "mirror"): 0.287,
        ("partial_observability_full", "mirror"): 0.333,
        ("mixed_50_full", "population"): 0.000,
        ("perspective_gpt54_full", "population"): 0.000,
        ("perspective_gpt41_full", "population"): 0.000,
        ("partial_observability_full", "population"): 0.000,
        ("mixed_50_no_coord", "consensus+info"): 0.040,
        ("perspective_gpt41_no_coord", "consensus+info"): 0.033,
        ("partial_observability_no_coord", "consensus+info"): 0.013,
    }
    for (run_label, method_label), expected_value in expected.items():
        row = by_run_method[(run_label, method_label)]
        add_numeric_check(
            checks,
            f"selection_regret.{run_label}.{method_label}",
            row["regret"],
            expected_value,
            decimals=3,
            source=path,
        )


def check_candidate_pool(checks: list[dict[str, Any]]) -> None:
    path = "results/candidate_pool_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run = {run["label"]: run for run in report["runs"]}

    availability_expected = {
        "mixed_50_full": {"robust_rate": 1.000, "mean_robust": 3.300, "oracle": 1.000},
        "perspective_gpt54_full": {"robust_rate": 1.000, "mean_robust": 2.440, "oracle": 1.000},
        "perspective_gpt41_full": {"robust_rate": 1.000, "mean_robust": 2.140, "oracle": 1.000},
        "partial_observability_full": {"robust_rate": 1.000, "mean_robust": 2.580, "oracle": 1.000},
        "mixed_50_no_coord": {"robust_rate": 0.920, "mean_robust": 2.300, "oracle": 0.960},
        "perspective_gpt41_no_coord": {"robust_rate": 0.660, "mean_robust": 1.140, "oracle": 0.793},
        "partial_observability_no_coord": {"robust_rate": 1.000, "mean_robust": 1.580, "oracle": 1.000},
    }
    for run_label, expected in availability_expected.items():
        pool = by_run[run_label]["candidate_pool"]
        add_numeric_check(
            checks,
            f"candidate_pool.{run_label}.robust_scene_rate",
            pool["robust_candidate_scene_rate"],
            expected["robust_rate"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"candidate_pool.{run_label}.mean_robust_candidates",
            pool["mean_robust_candidates"],
            expected["mean_robust"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"candidate_pool.{run_label}.oracle_success",
            pool["oracle_success"],
            expected["oracle"],
            decimals=3,
            source=path,
        )

    method_expected = {
        ("mixed_50_full", "mirror"): {"robust": 0.860, "oracle_match": 0.860},
        ("perspective_gpt54_full", "mirror"): {"robust": 0.720, "oracle_match": 0.720},
        ("perspective_gpt41_full", "mirror"): {"robust": 0.560, "oracle_match": 0.560},
        ("partial_observability_full", "mirror"): {"robust": 0.500, "oracle_match": 0.500},
        ("mixed_50_full", "population"): {"robust": 1.000, "oracle_match": 1.000},
        ("perspective_gpt54_full", "population"): {"robust": 1.000, "oracle_match": 1.000},
        ("perspective_gpt41_full", "population"): {"robust": 1.000, "oracle_match": 1.000},
        ("partial_observability_full", "population"): {"robust": 1.000, "oracle_match": 1.000},
        ("mixed_50_no_coord", "consensus+info"): {"robust": 0.880, "oracle_match": 0.940},
        ("perspective_gpt41_no_coord", "consensus+info"): {"robust": 0.620, "oracle_match": 0.920},
        ("partial_observability_no_coord", "consensus+info"): {"robust": 0.980, "oracle_match": 0.980},
    }
    by_run_method = {
        (run["label"], row["method_label"]): row
        for run in report["runs"]
        for row in run["methods"]
    }
    for (run_label, method_label), expected in method_expected.items():
        row = by_run_method[(run_label, method_label)]
        add_numeric_check(
            checks,
            f"candidate_pool.{run_label}.{method_label}.selected_robust_rate",
            row["selected_robust_rate"],
            expected["robust"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"candidate_pool.{run_label}.{method_label}.oracle_match_rate",
            row["oracle_match_rate"],
            expected["oracle_match"],
            decimals=3,
            source=path,
        )


def check_candidate_budget(checks: list[dict[str, Any]]) -> None:
    path = "results/candidate_budget_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run_k = {
        (run["label"], row["k"]): row
        for run in report["runs"]
        for row in run["prefix_rows"]
    }
    expected = {
        ("mixed_50_full", 1): {"oracle": 0.840, "robust": 0.780},
        ("mixed_50_full", 2): {"oracle": 0.853, "robust": 0.800},
        ("mixed_50_full", 3): {"oracle": 0.960, "robust": 0.920},
        ("mixed_50_full", 4): {"oracle": 1.000, "robust": 1.000},
        ("perspective_gpt54_full", 1): {"oracle": 0.713, "robust": 0.600},
        ("perspective_gpt54_full", 2): {"oracle": 0.787, "robust": 0.680},
        ("perspective_gpt54_full", 3): {"oracle": 0.893, "robust": 0.820},
        ("perspective_gpt54_full", 4): {"oracle": 1.000, "robust": 1.000},
        ("perspective_gpt41_full", 1): {"oracle": 0.553, "robust": 0.380},
        ("perspective_gpt41_full", 2): {"oracle": 0.620, "robust": 0.400},
        ("perspective_gpt41_full", 3): {"oracle": 0.793, "robust": 0.660},
        ("perspective_gpt41_full", 4): {"oracle": 1.000, "robust": 1.000},
        ("partial_observability_full", 1): {"oracle": 0.740, "robust": 0.620},
        ("partial_observability_full", 2): {"oracle": 0.747, "robust": 0.620},
        ("partial_observability_full", 3): {"oracle": 1.000, "robust": 1.000},
        ("partial_observability_full", 4): {"oracle": 1.000, "robust": 1.000},
    }
    for (run_label, k), values in expected.items():
        row = by_run_k[(run_label, k)]
        add_numeric_check(
            checks,
            f"candidate_budget.{run_label}.k{k}.oracle",
            row["oracle_success"],
            values["oracle"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"candidate_budget.{run_label}.k{k}.robust_scene_rate",
            row["robust_scene_rate"],
            values["robust"],
            decimals=3,
            source=path,
        )


def check_candidate_role_selection(checks: list[dict[str, Any]]) -> None:
    path = "results/candidate_role_selection_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run_method = {
        (run["label"], row["method_label"]): row
        for run in report["runs"]
        for row in run["methods"]
    }
    expected = {
        ("mixed_50_full", "mirror"): {
            "attribute_short": 0.760,
            "coordinate_fallback": 0.140,
        },
        ("mixed_50_full", "population"): {
            "attribute_short": 0.500,
            "coordinate_fallback": 0.420,
        },
        ("perspective_gpt54_full", "population"): {
            "attribute_short": 0.000,
            "coordinate_fallback": 1.000,
        },
        ("perspective_gpt41_full", "population"): {
            "attribute_short": 0.000,
            "coordinate_fallback": 1.000,
        },
        ("partial_observability_full", "population"): {
            "attribute_short": 0.000,
            "coordinate_fallback": 1.000,
        },
        ("mixed_50_no_coord", "consensus+info"): {
            "attribute_short": 0.320,
            "relational_or_spatial": 0.360,
            "coordinate_fallback": 0.000,
        },
        ("perspective_gpt41_no_coord", "consensus+info"): {
            "attribute_short": 0.000,
            "relational_or_spatial": 0.580,
            "coordinate_fallback": 0.000,
        },
        ("partial_observability_no_coord", "consensus+info"): {
            "attribute_short": 0.000,
            "relational_or_spatial": 0.460,
            "coordinate_fallback": 0.000,
        },
        ("perspective_gpt41_no_coord", "population"): {
            "attribute_short": 0.920,
            "relational_or_spatial": 0.080,
            "coordinate_fallback": 0.000,
        },
    }
    for (run_label, method_label), values in expected.items():
        row = by_run_method[(run_label, method_label)]
        add_numeric_check(
            checks,
            f"candidate_role_selection.{run_label}.{method_label}.n_scenes",
            row["n_scenes"],
            50,
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"candidate_role_selection.{run_label}.{method_label}.unresolved",
            row["n_unresolved"],
            0,
            decimals=0,
            source=path,
        )
        for role, expected_value in values.items():
            add_numeric_check(
                checks,
                f"candidate_role_selection.{run_label}.{method_label}.{role}",
                row["role_rates"][role],
                expected_value,
                decimals=3,
                source=path,
            )


def check_random_candidate_baseline(checks: list[dict[str, Any]]) -> None:
    path = "results/random_candidate_baseline.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run = {run["label"]: run for run in report["runs"]}
    expected = {
        "mixed_50_full": {
            "candidates": 4.000,
            "random": 0.865,
            "robust_pick": 0.825,
            "primary": "population",
            "minus_random": 0.135,
        },
        "perspective_gpt54_full": {
            "candidates": 4.000,
            "random": 0.715,
            "robust_pick": 0.610,
            "primary": "population",
            "minus_random": 0.285,
        },
        "perspective_gpt41_full": {
            "candidates": 4.000,
            "random": 0.657,
            "robust_pick": 0.535,
            "primary": "population",
            "minus_random": 0.343,
        },
        "partial_observability_full": {
            "candidates": 4.000,
            "random": 0.753,
            "robust_pick": 0.645,
            "primary": "population",
            "minus_random": 0.247,
        },
        "mixed_50_no_coord": {
            "candidates": 3.000,
            "random": 0.820,
            "robust_pick": 0.767,
            "primary": "consensus+info",
            "minus_random": 0.100,
        },
        "perspective_gpt41_no_coord": {
            "candidates": 3.000,
            "random": 0.542,
            "robust_pick": 0.380,
            "primary": "consensus+info",
            "minus_random": 0.218,
        },
        "partial_observability_no_coord": {
            "candidates": 3.000,
            "random": 0.671,
            "robust_pick": 0.527,
            "primary": "consensus+info",
            "minus_random": 0.316,
        },
    }
    for label, values in expected.items():
        row = by_run[label]
        add_numeric_check(
            checks,
            f"random_baseline.{label}.n_scenes",
            row["n_scenes"],
            50,
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"random_baseline.{label}.mean_candidates",
            row["mean_candidates"],
            values["candidates"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"random_baseline.{label}.random_expected",
            row["random_expected_success"],
            values["random"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"random_baseline.{label}.random_robust_pick_rate",
            row["random_robust_pick_rate"],
            values["robust_pick"],
            decimals=3,
            source=path,
        )
        add_bool_check(
            checks,
            f"random_baseline.{label}.primary_method",
            row["primary_method"] == values["primary"],
            source=path,
        )
        add_numeric_check(
            checks,
            f"random_baseline.{label}.primary_minus_random",
            row["primary_minus_random"],
            values["minus_random"],
            decimals=3,
            source=path,
        )


def check_message_length_audit(checks: list[dict[str, Any]]) -> None:
    path = "results/message_length_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run = {run["label"]: run for run in report["runs"]}
    expected = {
        "mixed_50_full": {
            "primary": "population",
            "mirror_tokens": 5.56,
            "primary_tokens": 6.82,
            "direct_tokens": 9.26,
            "template_tokens": 10.00,
            "token_delta": 1.26,
            "success_delta": 0.093,
        },
        "perspective_gpt54_full": {
            "primary": "population",
            "mirror_tokens": 7.40,
            "primary_tokens": 10.22,
            "direct_tokens": 11.70,
            "template_tokens": 10.00,
            "token_delta": 2.82,
            "success_delta": 0.187,
        },
        "perspective_gpt41_full": {
            "primary": "population",
            "mirror_tokens": 7.40,
            "primary_tokens": 10.22,
            "direct_tokens": 11.70,
            "template_tokens": 10.00,
            "token_delta": 2.82,
            "success_delta": 0.287,
        },
        "partial_observability_full": {
            "primary": "population",
            "mirror_tokens": 6.50,
            "primary_tokens": 9.66,
            "direct_tokens": 9.96,
            "template_tokens": 10.00,
            "token_delta": 3.16,
            "success_delta": 0.333,
        },
        "mixed_50_no_coord": {
            "primary": "consensus+info",
            "mirror_tokens": 5.00,
            "primary_tokens": 9.38,
            "direct_tokens": 9.26,
            "template_tokens": None,
            "token_delta": 4.38,
            "success_delta": 0.133,
        },
        "perspective_gpt41_no_coord": {
            "primary": "consensus+info",
            "mirror_tokens": 8.28,
            "primary_tokens": 12.54,
            "direct_tokens": 11.70,
            "template_tokens": None,
            "token_delta": 4.26,
            "success_delta": 0.180,
        },
        "partial_observability_no_coord": {
            "primary": "consensus+info",
            "mirror_tokens": 7.56,
            "primary_tokens": 12.76,
            "direct_tokens": 9.96,
            "template_tokens": None,
            "token_delta": 5.20,
            "success_delta": 0.380,
        },
    }
    for label, values in expected.items():
        run = by_run[label]
        methods = {row["method_label"]: row for row in run["methods"]}
        pair = run["primary_vs_mirror"]
        add_bool_check(
            checks,
            f"message_length.{label}.primary_method",
            run["primary_method"] == values["primary"],
            source=path,
        )
        add_numeric_check(
            checks,
            f"message_length.{label}.mirror_tokens",
            methods["mirror"]["mean_tokens"],
            values["mirror_tokens"],
            decimals=2,
            source=path,
        )
        add_numeric_check(
            checks,
            f"message_length.{label}.primary_tokens",
            methods[values["primary"]]["mean_tokens"],
            values["primary_tokens"],
            decimals=2,
            source=path,
        )
        add_numeric_check(
            checks,
            f"message_length.{label}.direct_tokens",
            methods["direct"]["mean_tokens"],
            values["direct_tokens"],
            decimals=2,
            source=path,
        )
        if values["template_tokens"] is not None:
            add_numeric_check(
                checks,
                f"message_length.{label}.template_tokens",
                methods["template"]["mean_tokens"],
                values["template_tokens"],
                decimals=2,
                source=path,
            )
        add_numeric_check(
            checks,
            f"message_length.{label}.token_delta",
            pair["token_delta"],
            values["token_delta"],
            decimals=2,
            source=path,
        )
        add_numeric_check(
            checks,
            f"message_length.{label}.success_delta",
            pair["success_delta"],
            values["success_delta"],
            decimals=3,
            source=path,
        )


def check_listener_disagreement(checks: list[dict[str, Any]]) -> None:
    path = "results/listener_disagreement_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run_method = {
        (run["label"], row["method_label"]): row
        for run in report["runs"]
        for row in run["methods"]
    }
    expected = {
        ("mixed_50_full", "mirror"): {"split": 0.080, "unanimous": 0.860},
        ("perspective_gpt54_full", "mirror"): {"split": 0.180, "unanimous": 0.720},
        ("perspective_gpt41_full", "mirror"): {"split": 0.360, "unanimous": 0.560},
        ("partial_observability_full", "mirror"): {"split": 0.500, "unanimous": 0.500},
        ("mixed_50_full", "population"): {"split": 0.000, "unanimous": 1.000},
        ("perspective_gpt54_full", "population"): {"split": 0.000, "unanimous": 1.000},
        ("perspective_gpt41_full", "population"): {"split": 0.000, "unanimous": 1.000},
        ("partial_observability_full", "population"): {"split": 0.000, "unanimous": 1.000},
        ("mixed_50_no_coord", "consensus+info"): {"split": 0.080, "unanimous": 0.880},
        ("perspective_gpt41_no_coord", "consensus+info"): {"split": 0.260, "unanimous": 0.620},
        ("partial_observability_no_coord", "consensus+info"): {"split": 0.020, "unanimous": 0.980},
        ("partial_observability_no_coord", "mirror"): {"split": 0.540, "unanimous": 0.420},
    }
    for (run_label, method_label), values in expected.items():
        row = by_run_method[(run_label, method_label)]
        add_numeric_check(
            checks,
            f"listener_disagreement.{run_label}.{method_label}.split",
            row["split_success_rate"],
            values["split"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"listener_disagreement.{run_label}.{method_label}.unanimous_success",
            row["unanimous_success_rate"],
            values["unanimous"],
            decimals=3,
            source=path,
        )


def check_listener_confidence_audit(checks: list[dict[str, Any]]) -> None:
    path = "results/listener_confidence_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_run_method = {
        (run["label"], row["method_label"]): row
        for run in report["runs"]
        for row in run["methods"]
    }
    add_numeric_check(
        checks,
        "listener_confidence.threshold",
        report["high_confidence_threshold"],
        0.8,
        decimals=1,
        source=path,
    )
    expected = {
        ("perspective_gpt41_full", "mirror"): {
            "ambiguity": 0.000,
            "high_conf_failure": 0.147,
            "scene_high_conf_failure": 0.280,
        },
        ("perspective_gpt41_no_coord", "mirror"): {
            "ambiguity": 0.000,
            "high_conf_failure": 0.280,
            "scene_high_conf_failure": 0.480,
        },
        ("perspective_gpt41_full", "population"): {
            "high_conf_failure": 0.000,
            "scene_high_conf_failure": 0.000,
        },
        ("partial_observability_no_coord", "consensus+info"): {
            "high_conf_failure": 0.000,
            "scene_high_conf_failure": 0.000,
        },
        ("partial_observability_full", "mirror"): {
            "ambiguity": 0.140,
            "high_conf_failure": 0.073,
        },
    }
    for (run_label, method_label), values in expected.items():
        row = by_run_method[(run_label, method_label)]
        if "ambiguity" in values:
            add_numeric_check(
                checks,
                f"listener_confidence.{run_label}.{method_label}.ambiguity",
                row["ambiguity_rate"],
                values["ambiguity"],
                decimals=3,
                source=path,
            )
        if "high_conf_failure" in values:
            add_numeric_check(
                checks,
                f"listener_confidence.{run_label}.{method_label}.high_conf_failure",
                row["high_confidence_failure_rate"],
                values["high_conf_failure"],
                decimals=3,
                source=path,
            )
        if "scene_high_conf_failure" in values:
            add_numeric_check(
                checks,
                f"listener_confidence.{run_label}.{method_label}.scene_high_conf_failure",
                row["scene_high_confidence_failure_rate"],
                values["scene_high_conf_failure"],
                decimals=3,
                source=path,
            )


def check_failure_taxonomy(checks: list[dict[str, Any]]) -> None:
    path = "results/failure_taxonomy_audit.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    by_set = {row["label"]: row for row in report["failure_sets"]}
    expected_sets = {
        "perspective_gpt41_full_mirror": {
            "total": 43,
            "underspecified": 38,
            "perspective": 5,
        },
        "partial_observability_full_mirror": {
            "total": 50,
            "underspecified": 50,
            "perspective": 0,
        },
        "partial_observability_no_coord_mirror": {
            "total": 59,
            "underspecified": 59,
            "perspective": 0,
        },
    }
    for label, values in expected_sets.items():
        row = by_set[label]
        counts = row["category_counts"]
        add_numeric_check(
            checks,
            f"failure_taxonomy.{label}.total",
            row["n_failures"],
            values["total"],
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"failure_taxonomy.{label}.underspecified",
            counts["underspecified_distractor"],
            values["underspecified"],
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"failure_taxonomy.{label}.perspective",
            counts["perspective_frame_error"],
            values["perspective"],
            decimals=0,
            source=path,
        )
    combined = report["combined"]
    combined_counts = combined["category_counts"]
    add_numeric_check(
        checks,
        "failure_taxonomy.combined.total",
        combined["n_failures"],
        152,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "failure_taxonomy.combined.underspecified",
        combined_counts["underspecified_distractor"],
        147,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "failure_taxonomy.combined.perspective",
        combined_counts["perspective_frame_error"],
        5,
        decimals=0,
        source=path,
    )
    other = (
        combined["n_failures"]
        - combined_counts["underspecified_distractor"]
        - combined_counts["perspective_frame_error"]
    )
    add_numeric_check(
        checks,
        "failure_taxonomy.combined.other",
        other,
        0,
        decimals=0,
        source=path,
    )


def check_interaction_memory_rules(checks: list[dict[str, Any]]) -> None:
    path = "results/interaction_memory_rules.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    combined = report["combined"]
    add_numeric_check(
        checks,
        "interaction_memory_rules.combined.failure_rows",
        combined["n_failure_rows"],
        152,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "interaction_memory_rules.combined.failure_scenes",
        combined["n_failure_scenes"],
        76,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "interaction_memory_rules.combined.mean_repair_success",
        combined["mean_repair_success_on_failure_scenes"],
        0.991,
        decimals=3,
        source=path,
    )
    add_numeric_check(
        checks,
        "interaction_memory_rules.combined.repair_all_success",
        combined["repair_all_success_scene_rate"],
        0.987,
        decimals=3,
        source=path,
    )
    add_numeric_check(
        checks,
        "interaction_memory_rules.combined.repair_rule_cue",
        combined["repair_rule_cue_rate"],
        1.000,
        decimals=3,
        source=path,
    )
    rule_counts = combined["rule_counts"]
    add_numeric_check(
        checks,
        "interaction_memory_rules.rule.disambiguate_shared_attributes",
        rule_counts["disambiguate_shared_attributes"],
        147,
        decimals=0,
        source=path,
    )
    add_numeric_check(
        checks,
        "interaction_memory_rules.rule.avoid_frame_sensitive_only",
        rule_counts["avoid_frame_sensitive_only"],
        5,
        decimals=0,
        source=path,
    )

    by_set_category = {
        (failure_set["label"], row["category"]): row
        for failure_set in report["failure_sets"]
        for row in failure_set["by_category"]
    }
    expected = {
        ("perspective_full_mirror", "perspective_frame_error"): {
            "rows": 5,
            "scenes": 3,
            "repair_success": 1.000,
            "cue": 1.000,
        },
        ("perspective_full_mirror", "underspecified_distractor"): {
            "rows": 38,
            "scenes": 19,
            "repair_success": 1.000,
            "cue": 1.000,
        },
        ("partial_observability_full_mirror", "underspecified_distractor"): {
            "rows": 50,
            "scenes": 25,
            "repair_success": 1.000,
            "cue": 1.000,
        },
        ("partial_observability_no_coord_mirror", "underspecified_distractor"): {
            "rows": 59,
            "scenes": 29,
            "repair_success": 0.977,
            "cue": 1.000,
        },
    }
    for (set_label, category), values in expected.items():
        row = by_set_category[(set_label, category)]
        add_numeric_check(
            checks,
            f"interaction_memory_rules.{set_label}.{category}.rows",
            row["failure_rows"],
            values["rows"],
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"interaction_memory_rules.{set_label}.{category}.scenes",
            row["failure_scenes"],
            values["scenes"],
            decimals=0,
            source=path,
        )
        add_numeric_check(
            checks,
            f"interaction_memory_rules.{set_label}.{category}.repair_success",
            row["mean_repair_success_on_failure_scenes"],
            values["repair_success"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"interaction_memory_rules.{set_label}.{category}.cue",
            row["repair_rule_cue_rate"],
            values["cue"],
            decimals=3,
            source=path,
        )


def check_qualitative_examples(checks: list[dict[str, Any]]) -> None:
    path = "results/qualitative_failure_examples.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    add_numeric_check(checks, "qualitative_examples.n_examples", report["n_examples"], 4, decimals=0, source=path)
    by_label = {example["label"]: example for example in report["examples"]}
    expected = {
        "perspective_underspecification": {
            "scene": "ps_000005",
            "category": "underspecified_distractor",
            "mirror": 1 / 3,
            "repair": 1.000,
        },
        "perspective_frame_error": {
            "scene": "ps_000011",
            "category": "perspective_frame_error",
            "mirror": 2 / 3,
            "repair": 1.000,
        },
        "partial_observability_underspecification": {
            "scene": "po_000005",
            "category": "underspecified_distractor",
            "mirror": 1 / 3,
            "repair": 1.000,
        },
        "partial_observability_no_coordinate_repair": {
            "scene": "po_000000",
            "category": "underspecified_distractor",
            "mirror": 1 / 3,
            "repair": 1.000,
        },
    }
    for label, values in expected.items():
        example = by_label[label]
        add_bool_check(
            checks,
            f"qualitative_examples.{label}.scene",
            example["scene_id"] == values["scene"],
            source=path,
        )
        add_bool_check(
            checks,
            f"qualitative_examples.{label}.category",
            example["failure_category"] == values["category"],
            source=path,
        )
        add_numeric_check(
            checks,
            f"qualitative_examples.{label}.mirror_success",
            example["mirror_outcome"]["success_rate"],
            values["mirror"],
            decimals=3,
            source=path,
        )
        add_numeric_check(
            checks,
            f"qualitative_examples.{label}.repair_success",
            example["repair_outcome"]["success_rate"],
            values["repair"],
            decimals=3,
            source=path,
        )


def check_reviewer_checklist(checks: list[dict[str, Any]]) -> None:
    path = "results/reviewer_checklist.json"
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    add_numeric_check(checks, "reviewer_checklist.n_items", report["n_items"], 19, decimals=0, source=path)
    add_numeric_check(checks, "reviewer_checklist.n_failed", report["n_failed"], 0, decimals=0, source=path)
    by_name = {item["name"]: item for item in report["items"]}
    expected = {
        "Target ID is never shown to the listener.": "Core validity",
        "Speaker messages are checked for target ID leakage.": "Core validity",
        "Listener outputs are valid object IDs.": "Core validity",
        "Same test scenes are used across methods.": "Core validity",
        "Prompts are frozen before final evaluation.": "Core validity",
        "Held-out listeners are not used for method selection.": "Core validity",
        "All responses are cached.": "Core validity",
        "Exact model versions are reported.": "Core validity",
        "Main table has confidence intervals.": "Results",
        "Scenario table explains where gains/losses occur.": "Results",
        "Cross-play gap is reported.": "Results",
        "Oracle upper bound is reported.": "Results",
        "Manual failure examples support the quantitative result.": "Results",
        "Intro states the evaluation blind spot clearly.": "Paper",
        "Related work is concise.": "Paper",
        "Method is reproducible.": "Paper",
        "Limitations are honest.": "Paper",
        "Claims match actual results.": "Paper",
        "Appendix includes prompts and schemas.": "Paper",
    }
    for name, section in expected.items():
        row = by_name.get(name, {})
        add_bool_check(
            checks,
            f"reviewer_checklist.{slug_name(name)}.present",
            bool(row),
            source=path,
        )
        add_bool_check(
            checks,
            f"reviewer_checklist.{slug_name(name)}.section",
            row.get("section") == section,
            source=path,
        )
        add_bool_check(
            checks,
            f"reviewer_checklist.{slug_name(name)}.pass",
            row.get("status") == "PASS",
            source=path,
        )


def check_plan_coverage(checks: list[dict[str, Any]]) -> None:
    path = "results/plan_coverage_audit.json"
    if not Path(path).exists():
        add_bool_check(checks, "plan_coverage.exists", False, source=path)
        return
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    add_numeric_check(checks, "plan_coverage.n_items", report["n_items"], 24, decimals=0, source=path)

    count_expectations = {
        "status_counts": {"covered": 17, "partial": 6, "open": 1},
        "core_status_counts": {"covered": 17, "partial": 2, "open": 0},
        "stretch_status_counts": {"covered": 0, "partial": 4, "open": 1},
    }
    for group, expected_counts in count_expectations.items():
        actual_counts = report[group]
        for status, expected in expected_counts.items():
            add_numeric_check(
                checks,
                f"plan_coverage.{group}.{status}",
                actual_counts[status],
                expected,
                decimals=0,
                source=path,
            )
    add_numeric_check(
        checks,
        "plan_coverage.open_or_partial",
        len(report["open_or_partial"]),
        7,
        decimals=0,
        source=path,
    )

    by_item = {row["plan_item"]: row for row in report["items"]}
    expected_status = {
        "Use development episodes for debugging prompts and tuning the generator.": "partial",
        "Hand-label roughly 100 failures into interpretable categories.": "partial",
        "Run a 1,000-scene benchmark and 200 partial-observability stress episodes.": "partial",
        "Evaluate K=8 candidate generation in addition to K=4.": "partial",
        "Run an actual interaction-memory prompt rerun after distilling rules from failures.": "partial",
        "Validate failures with human or independent non-LLM judgments.": "open",
        "Publish the artifact as a public repository or submission bundle.": "partial",
    }
    for item, status in expected_status.items():
        row = by_item.get(item)
        add_bool_check(checks, f"plan_coverage.item.{slug_name(item)}.present", row is not None, source=path)
        add_bool_check(
            checks,
            f"plan_coverage.item.{slug_name(item)}.{status}",
            bool(row) and row.get("status") == status,
            source=path,
        )


def check_submission_readiness(checks: list[dict[str, Any]]) -> None:
    path = "results/submission_readiness_audit.json"
    if not Path(path).exists():
        add_bool_check(checks, "submission_readiness.exists", False, source=path)
        return
    report = json.loads(Path(path).read_text(encoding="utf-8"))
    add_numeric_check(
        checks,
        "submission_readiness.n_failed",
        report.get("n_failed", -1),
        0,
        decimals=0,
        source=path,
    )
    add_bool_check(
        checks,
        "submission_readiness.no_open_actions",
        int(report.get("n_actions", 999)) == 0,
        source=path,
    )


def check_required_text(checks: list[dict[str, Any]]) -> None:
    snippets = [
        ("paper/main.tex", "consensus+info reaches 0.760"),
        ("paper/main.tex", "consensus+info success of 0.920"),
        ("paper/main.tex", "candidate-role audit makes this concrete"),
        ("paper/main.tex", "coordinate-fallback slot in 1.000 of scenes"),
        ("paper/main.tex", "short attribute-only slot in 0.000"),
        ("paper/main.tex", "gpt-5.4-nano-2026-03-17"),
        ("paper/main.tex", "generated protocol appendix"),
        ("paper/main.tex", "reviewer-facing artifact guide"),
        ("paper/main.tex", "cache-only leave-one-listener-out analysis"),
        ("paper/main.tex", "selection-regret audit makes this decomposition explicit"),
        ("paper/main.tex", "mirror self-play leaves regrets of 0.093, 0.187, 0.287, and 0.333"),
        ("paper/main.tex", "consensus+info reduces regret to 0.040"),
        ("paper/main.tex", "candidate-pool audit asks whether any candidate succeeds"),
        ("paper/main.tex", "population-play selects a robust candidate in 1.000 of scenes"),
        ("paper/main.tex", "robust non-coordinate candidates remain available in 0.920, 0.660, and 1.000"),
        ("paper/main.tex", "A uniform-random candidate baseline rules out the explanation that any candidate would do"),
        ("paper/main.tex", "random expected success is 0.865, 0.715, 0.657, and 0.753"),
        ("paper/main.tex", "population-play improves over random by 0.135, 0.285, 0.343, and 0.247"),
        ("paper/main.tex", "consensus+info improves over random by 0.100, 0.218, and 0.316"),
        ("paper/main.tex", "prefix-$K$ candidate-budget audit shows why the four-candidate protocol is useful"),
        ("paper/main.tex", "from 0.380 at $K=1$ to 0.660 at $K=3$ and 1.000 at $K=4$"),
        ("paper/main.tex", "listener-disagreement audit shows the same pattern"),
        ("paper/main.tex", "split held-out outcomes in 0.080, 0.180, 0.360, and 0.500"),
        ("paper/main.tex", "consensus+info reduces split outcomes from mirror's 0.540 to 0.020"),
        ("paper/main.tex", "listener-confidence audit further shows that self-reported uncertainty is not"),
        ("paper/main.tex", "mirror self-play still produces high-confidence failures"),
        ("paper/main.tex", "In scene \\texttt{ps\\_000005}"),
        ("paper/main.tex", "In scene \\texttt{ps\\_000011}"),
        ("paper/main.tex", "A generated qualitative appendix adds two partial-observability examples"),
        ("paper/main.tex", "consensus+info repair that raises held-out success from 0.333 to 1.000"),
        ("paper/main.tex", "API-population selection uses the other two"),
        ("paper/main.tex", "0.940 vs. 0.847"),
        ("paper/main.tex", "benchmark integrity audit"),
        ("paper/main.tex", "\\section{Related Work}"),
        ("paper/main.tex", "We generate five scenario families"),
        ("paper/main.tex", "We report three bounded API experiments"),
        ("paper/main.tex", "The paper contributes: (i) PRAG-CrossPlay"),
        ("paper/main.tex", "no-API 600-scene balanced local sweep"),
        ("docs/local_stronger_plan_k8.md", "Local Stronger-Plan K=8 Diagnostic"),
        ("docs/local_stronger_plan_k8.md", "No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8."),
        ("docs/local_stronger_plan_k8.md", "No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8."),
        ("docs/local_stronger_plan_k8.md", "Full-candidate local K=8 population-play reaches 1.000 over all 1,200 scenes."),
        ("docs/protocol_and_prompts.md", "PRAG-CrossPlay Protocol, Prompts, and Schemas"),
        ("docs/protocol_and_prompts.md", "Speaker Prompt"),
        ("docs/protocol_and_prompts.md", "Record Schema"),
        ("docs/protocol_and_prompts.md", "a bounded `partial_observability` support run"),
        ("docs/api_token_accounting.md", "API Token Accounting"),
        ("docs/api_token_accounting.md", "3520 | 3520 | 0 | 940088 | 87829 | 1027917"),
        ("docs/api_token_accounting.md", "`gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770"),
        ("docs/artifact_guide.md", "PRAG-CrossPlay Artifact Guide"),
        ("docs/artifact_guide.md", "Claim-To-Evidence Map"),
        ("docs/artifact_guide.md", "API Token Accounting"),
        ("docs/artifact_guide.md", "3520 cached responses have complete usage metadata totaling 1027917 tokens"),
        ("docs/artifact_guide.md", "Local Stronger-Plan K=8 Diagnostic"),
        ("docs/artifact_guide.md", "No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8"),
        ("docs/artifact_guide.md", "No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8"),
        ("docs/artifact_guide.md", "At K=8 without exact coordinates, consensus+info reaches 0.992 on the initial 1,000 scenes and 0.997 on partial-observability scenes"),
        ("docs/artifact_guide.md", "API Listener Leave-One-Out Mechanism Check"),
        ("docs/artifact_guide.md", "Selection Regret Audit"),
        ("docs/artifact_guide.md", "Candidate Pool Robustness Audit"),
        ("docs/artifact_guide.md", "Candidate Budget Audit"),
        ("docs/artifact_guide.md", "Candidate Role Selection Audit"),
        ("docs/artifact_guide.md", "Random Candidate Baseline"),
        ("docs/artifact_guide.md", "Listener Disagreement Audit"),
        ("docs/artifact_guide.md", "Qualitative Failure Examples"),
        ("docs/artifact_guide.md", "Reviewer Checklist"),
        ("docs/artifact_guide.md", "Plan Coverage Audit"),
        ("docs/artifact_guide.md", "full-candidate population-play has zero regret"),
        ("docs/artifact_guide.md", "population-play selects a robust candidate in 1.000 of scenes"),
        ("docs/artifact_guide.md", "alternate-model perspective robust-scene coverage rises from 0.380 at K=1 to 1.000 at K=4"),
        ("docs/artifact_guide.md", "Full-candidate population coordinate-fallback rates: mixed_50_full=0.420, perspective_gpt54_full=1.000, perspective_gpt41_full=1.000, partial_observability_full=1.000"),
        ("docs/artifact_guide.md", "No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000"),
        ("docs/artifact_guide.md", "population-play improves over random by 0.135, 0.285, 0.343, and 0.247"),
        ("docs/artifact_guide.md", "consensus+info improves over random by 0.100, 0.218, and 0.316"),
        ("docs/artifact_guide.md", "Message Length Audit"),
        ("docs/artifact_guide.md", "full-candidate population selected messages average 6.82, 10.22, 10.22, and 9.66 tokens"),
        ("docs/artifact_guide.md", "mirror split-outcome rates are 0.080, 0.180, 0.360, and 0.500"),
        ("docs/artifact_guide.md", "Listener Confidence Audit"),
        ("docs/artifact_guide.md", "alternate-model perspective ambiguity flags are 0.000 while mirror high-confidence failure rates are 0.147 and 0.280"),
        ("docs/artifact_guide.md", "Failure Taxonomy Audit"),
        ("docs/artifact_guide.md", "147 of 152 coded listener-level mirror failures are underspecified-distractor cases"),
        ("docs/artifact_guide.md", "Interaction Memory Rule Audit"),
        ("docs/artifact_guide.md", "Coded failure rows: 152; unique failure scenes: 76"),
        ("docs/artifact_guide.md", "repair cue satisfies derived rule in 1.000 of failure scenes"),
        ("docs/artifact_guide.md", "four cache-only examples show mirror-selected messages failing held-out listeners"),
        ("docs/artifact_guide.md", "Section 32 reviewer checklist passes all 19 core-validity, results, and paper items"),
        ("docs/artifact_guide.md", "Items passed: 19/19"),
        ("docs/artifact_guide.md", "Core scope: 17 covered, 2 partial, 0 open."),
        ("docs/artifact_guide.md", "Stretch scope: 0 covered, 4 partial, 1 open."),
        ("docs/artifact_guide.md", "The artifact package explicitly distinguishes completed core requirements from stretch gaps"),
        ("docs/artifact_guide.md", "Local Benchmark-Scale Sanity Check"),
        ("docs/artifact_guide.md", "600 local scenes balanced across four initial scenario families"),
        ("docs/artifact_guide.md", "partial_observability_api50 | `data/partial_observability_local50_scenes.jsonl` | 50"),
        ("docs/artifact_guide.md", "cache-only API listener leave-one-out improves population over mirror"),
        ("docs/artifact_guide.md", "0 candidate messages reference private landmarks"),
        ("docs/artifact_guide.md", "all 50 full-run mirror failures are underspecified-distractor choices"),
        ("docs/artifact_guide.md", "local_benchmark600 | `data/local_benchmark600_scenes.jsonl` | 600 | 10800"),
        ("docs/artifact_guide.md", "158/158 integrity checks pass"),
        ("docs/local_benchmark600_check.md", "Mirror self-play has same-play 1.000 but cross-play 0.631"),
        ("docs/local_benchmark600_check.md", "perspective_shift | 0.000 | 0.158 | 1.000 | 0.842"),
        ("docs/api_listener_leave_one_out.md", "API Listener Leave-One-Out Analysis"),
        ("docs/api_listener_leave_one_out.md", "partial_observability | scene_eval_listener | 150 | 0.940 | 0.767 | 0.173"),
        ("docs/selection_regret_audit.md", "perspective_gpt41_full | mirror | 50 | 0.713 | 1.000 | 0.287"),
        ("docs/selection_regret_audit.md", "partial_observability_no_coord | consensus+info | 50 | 0.987 | 1.000 | 0.013"),
        ("docs/candidate_pool_audit.md", "perspective_gpt41_no_coord | no_exact_coordinates | 50 | 3.00 | 1.14 | 0.660 | 0.793"),
        ("docs/candidate_pool_audit.md", "partial_observability_no_coord | consensus+info | 0.987 | 0.980 | 0.980"),
        ("docs/candidate_budget_audit.md", "perspective_gpt41_full | 4 | 1.000 | 1.000"),
        ("docs/candidate_budget_audit.md", "partial_observability_full | 3 | 1.000 | 1.000"),
        ("docs/candidate_role_selection_audit.md", "Candidate Role Selection Audit"),
        ("docs/candidate_role_selection_audit.md", "perspective_gpt54_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000"),
        ("docs/candidate_role_selection_audit.md", "perspective_gpt41_no_coord | no_exact_coordinates | consensus+info | 50 | 0.760 | 0.420 | 0.000 | 0.580 | 0.000"),
        ("docs/candidate_role_selection_audit.md", "No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000"),
        ("docs/random_candidate_baseline.md", "Random Candidate Baseline"),
        ("docs/random_candidate_baseline.md", "perspective_gpt41_full | full | 50 | 4.00 | 0.657 | 0.535 | population | 0.343"),
        ("docs/random_candidate_baseline.md", "partial_observability_no_coord | no_exact_coordinates | 50 | 3.00 | 0.671 | 0.527 | consensus+info | 0.316"),
        ("docs/message_length_audit.md", "Message Length Audit"),
        ("docs/message_length_audit.md", "perspective_gpt41_full | full | population | 50 | 1.000 | 10.22 | 0.098"),
        ("docs/message_length_audit.md", "partial_observability_no_coord | consensus+info | 50 | 0.380 | [0.280, 0.473] | 5.20"),
        ("docs/listener_disagreement_audit.md", "partial_observability_full | mirror | 50 | 0.667 | 0.500 | 0.500"),
        ("docs/listener_disagreement_audit.md", "partial_observability_no_coord | consensus+info | 50 | 0.987 | 0.980 | 0.020"),
        ("docs/listener_confidence_audit.md", "Listener Confidence Audit"),
        ("docs/listener_confidence_audit.md", "perspective_gpt41_full | mirror | 150 | 0.713 | 0.877 | 0.000 | 0.677 | 0.147 | 0.280"),
        ("docs/listener_confidence_audit.md", "perspective_gpt41_no_coord | mirror | 150 | 0.580 | 0.835 | 0.000 | 0.771 | 0.280 | 0.480"),
        ("docs/listener_confidence_audit.md", "partial_observability_no_coord | consensus+info | 150 | 0.987 | 0.889 | 0.000 | 0.000 | 0.000 | 0.000"),
        ("docs/failure_taxonomy_audit.md", "Failure Taxonomy Audit"),
        ("docs/failure_taxonomy_audit.md", "combined | 152 | 147 | 5 | 0"),
        ("docs/interaction_memory_rules.md", "Interaction Memory Rule Audit"),
        ("docs/interaction_memory_rules.md", "Coded failure rows: 152. Unique failure scenes: 76."),
        ("docs/interaction_memory_rules.md", "Repair cue satisfies derived rule in 1.000 of failure scenes."),
        ("docs/interaction_memory_rules.md", "If exact coordinates are disallowed, prefer the relational/spatial candidate"),
        ("docs/qualitative_failure_examples.md", "Qualitative Failure Examples"),
        ("docs/qualitative_failure_examples.md", "Perspective scene with frame-sensitive relation"),
        ("docs/qualitative_failure_examples.md", "No-coordinate repair using consensus+info"),
        ("docs/qualitative_failure_examples.md", "0.333 (1/3) | consensus+info | 1.000 (3/3)"),
        ("docs/reviewer_checklist.md", "Reviewer Checklist"),
        ("docs/reviewer_checklist.md", "Section 32 of the original workshop plan"),
        ("docs/reviewer_checklist.md", "Items passed: 19/19"),
        ("docs/reviewer_checklist.md", "Held-out listeners are not used for method selection."),
        ("docs/reviewer_checklist.md", "Claims match actual results."),
        ("docs/plan_coverage_audit.md", "Plan Coverage Audit"),
        ("docs/plan_coverage_audit.md", "Overall: 17 covered, 6 partial, 1 open across 24 plan items."),
        ("docs/plan_coverage_audit.md", "Core scope: 17 covered, 2 partial, 0 open."),
        ("docs/plan_coverage_audit.md", "Stretch scope: 0 covered, 4 partial, 1 open."),
        ("docs/partial_observability_local_check.md", "mirror self-play | 0.653 | 1.000 | 0.347"),
        ("docs/partial_observability_api50_check.md", "Candidate messages referencing private landmarks: 0"),
        ("docs/partial_observability_api50_check.md", "no_coord_consensus_info | 0.987"),
        ("docs/partial_observability_api50_check.md", "| underspecified_distractor | 50 |"),
        ("docs/partial_observability_api50_check.md", "| underspecified_distractor | 59 |"),
        ("docs/paper_claims_iteration_002.md", "Consensus+info selector: cross-play `0.920`"),
        ("paper/main.tex", "partial-observability stress check"),
        ("paper/main.tex", "message-length audit rules out a pure verbosity explanation"),
        ("paper/main.tex", "Across 152 listener-level failures, 147 are underspecified"),
        ("paper/main.tex", "no coded failures are"),
        ("paper/main.tex", "mirror self-play obtains 0.667 cross-play success"),
        ("paper/main.tex", "all 50 full-run mirror failures and all 59 no-coordinate mirror"),
        ("REPRODUCE.md", "--partial 50"),
        ("REPRODUCE.md", "scripts/analyze_partial_observability_api.py"),
        ("REPRODUCE.md", "scripts/analyze_api_token_accounting.py"),
        ("REPRODUCE.md", "cached Responses API files contain `1,027,917` total tokens"),
        ("REPRODUCE.md", "scripts/analyze_local_benchmark.py"),
        ("REPRODUCE.md", "local_benchmark600_check.json"),
        ("REPRODUCE.md", "scripts/analyze_local_stronger_plan.py"),
        ("REPRODUCE.md", "No-coordinate oracle success rises from `0.808` at K=4 to `0.995` at K=8 over all `1,200` local scenes"),
        ("REPRODUCE.md", "scripts/analyze_selection_regret.py"),
        ("REPRODUCE.md", "mirror self-play regret is `0.093`, `0.187`, `0.287`, and `0.333`"),
        ("REPRODUCE.md", "scripts/analyze_candidate_pool.py"),
        ("REPRODUCE.md", "robust non-coordinate candidate availability is `0.920`, `0.660`, and `1.000`"),
        ("REPRODUCE.md", "scripts/analyze_candidate_budget.py"),
        ("REPRODUCE.md", "alternate-model perspective robust-scene coverage is `0.380` at `K=1`"),
        ("REPRODUCE.md", "scripts/analyze_candidate_role_selection.py"),
        ("REPRODUCE.md", "no-coordinate consensus+info uses the relational/spatial slot in `0.580`"),
        ("REPRODUCE.md", "scripts/analyze_random_candidate_baseline.py"),
        ("REPRODUCE.md", "population-play beats the uniform-random selector by `0.135`, `0.285`, `0.343`, and `0.247`"),
        ("REPRODUCE.md", "scripts/analyze_message_length_audit.py"),
        ("REPRODUCE.md", "full-candidate population-play messages average `6.82`, `10.22`, `10.22`, and `9.66`"),
        ("REPRODUCE.md", "scripts/analyze_listener_disagreement.py"),
        ("REPRODUCE.md", "full-candidate mirror split-outcome rates are `0.080`, `0.180`, `0.360`, and"),
        ("REPRODUCE.md", "scripts/analyze_listener_confidence_audit.py"),
        ("REPRODUCE.md", "mirror self-play still produces high-confidence failures in `0.147`"),
        ("REPRODUCE.md", "scripts/analyze_failure_taxonomy.py"),
        ("REPRODUCE.md", "147` of `152` coded listener-level mirror failures are `underspecified_distractor`"),
        ("REPRODUCE.md", "scripts/analyze_interaction_memory_rules.py"),
        ("REPRODUCE.md", "`152` coded failure rows collapse into two active rules"),
        ("REPRODUCE.md", "mean repair success on those failure scenes is `0.991`"),
        ("REPRODUCE.md", "scripts/make_qualitative_examples.py"),
        ("REPRODUCE.md", "docs/qualitative_failure_examples.md"),
        ("REPRODUCE.md", "scripts/make_reviewer_checklist.py"),
        ("REPRODUCE.md", "docs/reviewer_checklist.md"),
        ("REPRODUCE.md", "scripts/audit_plan_coverage.py"),
        ("REPRODUCE.md", "docs/plan_coverage_audit.md"),
        ("REPRODUCE.md", "core scope has `17` covered, `2` partial, and `0` open items"),
        ("REPRODUCE.md", "stretch scope has `0` covered, `4` partial, and `1` open item"),
        ("REPRODUCE.md", "partial_observability_api50_mirror_failures_coded.csv"),
        ("REPRODUCE.md", "scripts/make_artifact_guide.py"),
        ("REPRODUCE.md", "scripts/analyze_api_listener_leave_one_out.py"),
        ("REPRODUCE.md", "scripts/audit_submission_readiness.py"),
        ("REPRODUCE.md", "scripts/export_colm_submission.py"),
        ("REPRODUCE.md", "scripts/export_protocol_appendix.py"),
        ("REPRODUCE.md", "scripts/audit_benchmark_integrity.py"),
        ("REPRODUCE.md", "scripts/verify_paper_claims.py"),
        ("README.md", "paper/colm2026_submission.pdf"),
        ("README.md", "docs/api_token_accounting.md"),
        ("README.md", "docs/local_benchmark600_check.md"),
        ("README.md", "docs/local_stronger_plan_k8.md"),
        ("README.md", "docs/artifact_guide.md"),
        ("README.md", "docs/api_listener_leave_one_out.md"),
        ("README.md", "docs/selection_regret_audit.md"),
        ("README.md", "docs/candidate_pool_audit.md"),
        ("README.md", "docs/candidate_budget_audit.md"),
        ("README.md", "docs/candidate_role_selection_audit.md"),
        ("README.md", "docs/random_candidate_baseline.md"),
        ("README.md", "docs/message_length_audit.md"),
        ("README.md", "docs/listener_disagreement_audit.md"),
        ("README.md", "docs/listener_confidence_audit.md"),
        ("README.md", "docs/failure_taxonomy_audit.md"),
        ("README.md", "docs/interaction_memory_rules.md"),
        ("README.md", "docs/qualitative_failure_examples.md"),
        ("README.md", "docs/reviewer_checklist.md"),
        ("README.md", "docs/plan_coverage_audit.md"),
        ("README.md", "docs/partial_observability_api50_check.md"),
        ("paper/colm2026_submission.tex", "\\usepackage[submission]{colm2026_conference}"),
    ]
    for path, snippet in snippets:
        text = Path(path).read_text(encoding="utf-8")
        add_bool_check(checks, f"text.{path}.{snippet}", contains_snippet(text, snippet), source=path)


def count_regex(rows: list[dict[str, Any]], field: str, regex: re.Pattern[str]) -> int:
    return sum(1 for row in rows if regex.search(str(row.get(field, ""))))


def contains_snippet(text: str, snippet: str) -> bool:
    if snippet in text:
        return True
    compact_text = re.sub(r"\s+", " ", text)
    compact_snippet = re.sub(r"\s+", " ", snippet)
    return compact_snippet in compact_text


def slug_name(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def add_numeric_check(
    checks: list[dict[str, Any]],
    name: str,
    actual: float,
    expected: float,
    *,
    decimals: int,
    source: str,
) -> None:
    actual_rounded = round(float(actual), decimals)
    expected_rounded = round(float(expected), decimals)
    checks.append(
        {
            "name": name,
            "ok": actual_rounded == expected_rounded,
            "actual": format_value(actual_rounded, decimals),
            "expected": format_value(expected_rounded, decimals),
            "source": source,
        }
    )


def add_bool_check(checks: list[dict[str, Any]], name: str, ok: bool, *, source: str) -> None:
    checks.append(
        {
            "name": name,
            "ok": bool(ok),
            "actual": "present" if ok else "missing",
            "expected": "present",
            "source": source,
        }
    )


def format_value(value: float, decimals: int) -> str:
    if decimals == 0:
        return str(int(round(value)))
    return f"{value:.{decimals}f}"


def markdown_report(checks: list[dict[str, Any]]) -> str:
    lines = [
        "# Paper Claims Verification",
        "",
        f"Checks passed: {sum(1 for check in checks if check['ok'])}/{len(checks)}.",
        "",
        "| Status | Check | Actual | Expected | Source |",
        "|---|---|---:|---:|---|",
    ]
    for check in checks:
        status = "PASS" if check["ok"] else "FAIL"
        lines.append(
            f"| {status} | `{check['name']}` | {check['actual']} | {check['expected']} | `{check['source']}` |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
