#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl, read_scenes

OBJ_ID_RE = re.compile(r"\bobj_\d+\b", re.IGNORECASE)

GROUPS = [
    {
        "name": "local_benchmark600",
        "scene_file": "data/local_benchmark600_scenes.jsonl",
        "record_files": [
            "results/local_benchmark600_records.jsonl",
        ],
        "candidate_files": [],
        "audit_files": [],
    },
    {
        "name": "mixed_50",
        "scene_file": "data/dev_scenes.jsonl",
        "record_files": [
            "results/hybrid_api_pilot50_allcand_records.jsonl",
            "results/hybrid_api_pilot50_no_coord_records.jsonl",
            "results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl",
        ],
        "candidate_files": [
            "results/hybrid_api_pilot50_allcand_candidates.jsonl",
        ],
        "audit_files": [
            "results/hybrid_api_pilot50_no_coord_audit.jsonl",
        ],
    },
    {
        "name": "perspective_stress_50",
        "scene_file": "data/perspective_stress50_scenes.jsonl",
        "record_files": [
            "results/perspective_stress50_hybrid_records.jsonl",
            "results/perspective_stress50_gpt41nano_records.jsonl",
            "results/gpt55_perspective_selected_records.jsonl",
            "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
            "results/perspective_stress50_hybrid_candidate_eval_records.jsonl",
            "results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl",
            "results/gpt55_speaker_perspective20_records.jsonl",
            "results/gpt55_speaker_perspective20_candidate_eval_records.jsonl",
            "results/gpt55_speaker_perspective50_records.jsonl",
            "results/gpt55_speaker_perspective50_candidate_eval_records.jsonl",
            "results/gpt55_speaker_perspective50_no_coord_records.jsonl",
            "results/gpt55_no_coord_k8_perspective50_records.jsonl",
            "results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl",
            "results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl",
        ],
        "candidate_files": [
            "results/perspective_stress50_hybrid_candidates.jsonl",
            "results/gpt55_speaker_perspective20_candidates.jsonl",
            "results/gpt55_speaker_perspective50_candidates.jsonl",
            "results/gpt55_no_coord_k8_perspective50_candidates.jsonl",
        ],
        "audit_files": [
            "results/perspective_stress50_gpt41nano_audit.jsonl",
            "results/gpt55_perspective_selected_audit.jsonl",
            "results/perspective_stress50_gpt41nano_no_coord_audit.jsonl",
            "results/gpt55_speaker_perspective50_no_coord_audit.jsonl",
            "results/gpt55_no_coord_k8_perspective50_no_coord_audit.jsonl",
        ],
    },
    {
        "name": "partial_observability_api50",
        "scene_file": "data/partial_observability_local50_scenes.jsonl",
        "record_files": [
            "results/partial_observability_api50_records.jsonl",
            "results/gpt41_partial_observability_selected_records.jsonl",
            "results/gpt55_partial_observability_selected_records.jsonl",
            "results/partial_observability_api50_candidate_eval_records.jsonl",
            "results/partial_observability_api50_no_coord_records.jsonl",
        ],
        "candidate_files": [
            "results/partial_observability_api50_candidates.jsonl",
        ],
        "audit_files": [
            "results/gpt41_partial_observability_selected_audit.jsonl",
            "results/gpt55_partial_observability_selected_audit.jsonl",
            "results/partial_observability_api50_no_coord_audit.jsonl",
        ],
    },
]

SELECTED_FIELDS = [
    "mirror_selected",
    "population_selected",
    "consensus_info_selected",
    "informative_selected",
    "oracle_selected",
]
LOCAL_CHOICE_FIELDS = [
    "mirror_local_choices",
    "population_local_choices",
    "consensus_info_local_choices",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="results/benchmark_integrity_audit.md")
    parser.add_argument("--json-out", default="results/benchmark_integrity_audit.json")
    parser.add_argument("--cache-dir", default="data/cached_responses")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    warnings: list[str] = []
    summary: dict[str, Any] = {"groups": []}

    scene_id_sources: dict[str, list[str]] = defaultdict(list)
    loaded_groups = []
    for group in GROUPS:
        scene_file = group["scene_file"]
        scenes = read_scenes(scene_file)
        loaded_groups.append((group, scenes))
        for scene in scenes:
            scene_id_sources[scene.scene_id].append(scene_file)
        validate_scenes(scene_file, scenes, checks)

    overlaps = {sid: paths for sid, paths in scene_id_sources.items() if len(paths) > 1}
    if overlaps:
        sample = ", ".join(sorted(overlaps)[:8])
        warnings.append(
            "Scene IDs overlap across source scene files; validation is scoped by "
            f"scene file. Sample overlaps: {sample}."
        )

    for group, scenes in loaded_groups:
        scene_by_id = {scene.scene_id: scene for scene in scenes}
        group_summary = {
            "name": group["name"],
            "scene_file": group["scene_file"],
            "n_scenes": len(scenes),
            "record_rows": 0,
            "candidate_rows": 0,
            "audit_rows": 0,
            "speaker_cache_paths": 0,
        }
        for path in group["record_files"]:
            group_summary["record_rows"] += validate_record_file(path, scene_by_id, checks)
        for path in group["candidate_files"]:
            rows, cache_paths = validate_candidate_file(path, scene_by_id, checks)
            group_summary["candidate_rows"] += rows
            group_summary["speaker_cache_paths"] += cache_paths
        for path in group["audit_files"]:
            group_summary["audit_rows"] += validate_audit_file(path, scene_by_id, checks)
        summary["groups"].append(group_summary)

    summary["cache"] = summarize_cache(Path(args.cache_dir), checks)

    report = {
        "n_checks": len(checks),
        "n_failed": sum(1 for check in checks if not check["ok"]),
        "checks": checks,
        "warnings": warnings,
        "summary": summary,
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown_report(report), encoding="utf-8")
    print(markdown_report(report))
    if report["n_failed"]:
        raise SystemExit(1)


def validate_scenes(path: str, scenes: list[Any], checks: list[dict[str, Any]]) -> None:
    add_check(checks, f"{path}.nonempty", bool(scenes), f"{len(scenes)} scenes")
    scene_ids = [scene.scene_id for scene in scenes]
    duplicate_scene_ids = sorted(id_ for id_, count in Counter(scene_ids).items() if count > 1)
    add_check(
        checks,
        f"{path}.unique_scene_ids_within_file",
        not duplicate_scene_ids,
        "no duplicates" if not duplicate_scene_ids else ", ".join(duplicate_scene_ids[:5]),
    )
    bad_targets = []
    hidden_targets = []
    duplicate_objects = []
    for scene in scenes:
        object_ids = [obj.id for obj in scene.objects]
        if scene.target_id not in object_ids:
            bad_targets.append(scene.scene_id)
        if scene.target_id not in {obj.id for obj in scene.listener_objects()}:
            hidden_targets.append(scene.scene_id)
        if len(object_ids) != len(set(object_ids)):
            duplicate_objects.append(scene.scene_id)
    add_check(
        checks,
        f"{path}.target_id_in_scene",
        not bad_targets,
        "all targets present" if not bad_targets else ", ".join(bad_targets[:5]),
    )
    add_check(
        checks,
        f"{path}.target_visible_to_listener",
        not hidden_targets,
        "all targets visible" if not hidden_targets else ", ".join(hidden_targets[:5]),
    )
    add_check(
        checks,
        f"{path}.unique_object_ids_per_scene",
        not duplicate_objects,
        "all object IDs unique" if not duplicate_objects else ", ".join(duplicate_objects[:5]),
    )


def validate_record_file(path: str, scene_by_id: dict[str, Any], checks: list[dict[str, Any]]) -> int:
    rows = read_jsonl(path)
    add_check(checks, f"{path}.nonempty", bool(rows), f"{len(rows)} rows")
    bad_scene = []
    bad_target = []
    bad_choice = []
    bad_success = []
    leaks = []
    method_scenes: dict[str, set[str]] = defaultdict(set)
    scene_method_counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        scene_id = str(row.get("scene_id", ""))
        method = str(row.get("method", ""))
        scene = scene_by_id.get(scene_id)
        if scene is None:
            bad_scene.append(scene_id)
            continue
        method_scenes[method].add(scene_id)
        scene_method_counts[(scene_id, method)] += 1
        if row.get("target_id") != scene.target_id:
            bad_target.append(scene_id)
        choice_id = str(row.get("choice_id", ""))
        valid_ids = {obj.id for obj in scene.listener_objects()}
        if choice_id not in valid_ids:
            bad_choice.append(f"{scene_id}:{choice_id}")
        expected_success = int(choice_id == scene.target_id)
        if int(row.get("success", -1)) != expected_success:
            bad_success.append(scene_id)
        message = str(row.get("message", ""))
        if OBJ_ID_RE.search(message):
            leaks.append(f"{scene_id}:{message}")

    add_check(
        checks,
        f"{path}.scene_ids_known",
        not bad_scene,
        "all rows mapped to source scene file" if not bad_scene else sample(bad_scene),
    )
    add_check(
        checks,
        f"{path}.target_ids_match_source",
        not bad_target,
        "all row target IDs match source scenes" if not bad_target else sample(bad_target),
    )
    add_check(
        checks,
        f"{path}.choice_ids_valid",
        not bad_choice,
        "all listener choices are valid candidate object IDs" if not bad_choice else sample(bad_choice),
    )
    add_check(
        checks,
        f"{path}.success_flags_consistent",
        not bad_success,
        "all success flags equal choice_id == target_id" if not bad_success else sample(bad_success),
    )
    add_check(
        checks,
        f"{path}.messages_no_object_id_leakage",
        not leaks,
        "no generated/evaluated message contains obj_* IDs" if not leaks else sample(leaks),
    )
    if method_scenes:
        scene_sets = list(method_scenes.values())
        common_scene_set = all(scene_set == scene_sets[0] for scene_set in scene_sets[1:])
        add_check(
            checks,
            f"{path}.same_scene_set_across_methods",
            common_scene_set,
            f"{len(scene_sets[0])} scenes per method" if common_scene_set else method_scene_detail(method_scenes),
        )
        counts = set(scene_method_counts.values())
        add_check(
            checks,
            f"{path}.balanced_rows_per_scene_method",
            len(counts) == 1,
            f"{next(iter(counts))} rows per scene-method" if len(counts) == 1 else f"row counts {sorted(counts)}",
        )
    return len(rows)


def validate_candidate_file(path: str, scene_by_id: dict[str, Any], checks: list[dict[str, Any]]) -> tuple[int, int]:
    rows = read_jsonl(path)
    add_check(checks, f"{path}.nonempty", bool(rows), f"{len(rows)} rows")
    bad_scene = []
    bad_target = []
    empty_candidates = []
    selection_not_in_candidates = []
    leaks = []
    bad_local_choice = []
    missing_cache = []
    cache_paths = 0
    for row in rows:
        scene_id = str(row.get("scene_id", ""))
        scene = scene_by_id.get(scene_id)
        if scene is None:
            bad_scene.append(scene_id)
            continue
        if row.get("target_id") != scene.target_id:
            bad_target.append(scene_id)
        candidates = [str(msg) for msg in row.get("candidates", [])]
        if not candidates:
            empty_candidates.append(scene_id)
        for message in candidates:
            if OBJ_ID_RE.search(message):
                leaks.append(f"{scene_id}:{message}")
        for field in ("mirror_selected", "population_selected"):
            if field in row and row[field] not in candidates:
                selection_not_in_candidates.append(f"{scene_id}:{field}")
        valid_ids = {obj.id for obj in scene.listener_objects()}
        bad_local_choice.extend(invalid_local_choices(row, valid_ids, scene_id))
        cache_path = row.get("speaker_cache_path")
        if cache_path:
            cache_paths += 1
            if not Path(str(cache_path)).exists():
                missing_cache.append(str(cache_path))

    add_check(checks, f"{path}.scene_ids_known", not bad_scene, ok_or_sample(bad_scene, "all rows mapped"))
    add_check(checks, f"{path}.target_ids_match_source", not bad_target, ok_or_sample(bad_target, "all targets match"))
    add_check(checks, f"{path}.candidate_lists_nonempty", not empty_candidates, ok_or_sample(empty_candidates, "all rows have candidates"))
    add_check(
        checks,
        f"{path}.candidates_no_object_id_leakage",
        not leaks,
        "no candidate contains obj_* IDs" if not leaks else sample(leaks),
    )
    add_check(
        checks,
        f"{path}.selections_are_candidates",
        not selection_not_in_candidates,
        "mirror/population selections come from candidate lists" if not selection_not_in_candidates else sample(selection_not_in_candidates),
    )
    add_check(
        checks,
        f"{path}.local_choice_ids_valid",
        not bad_local_choice,
        "all local selector choices are valid object IDs" if not bad_local_choice else sample(bad_local_choice),
    )
    add_check(
        checks,
        f"{path}.speaker_cache_paths_exist",
        not missing_cache,
        f"{cache_paths} speaker cache paths exist" if not missing_cache else sample(missing_cache),
    )
    return len(rows), cache_paths


def validate_audit_file(path: str, scene_by_id: dict[str, Any], checks: list[dict[str, Any]]) -> int:
    rows = read_jsonl(path)
    add_check(checks, f"{path}.nonempty", bool(rows), f"{len(rows)} rows")
    bad_scene = []
    leaks = []
    bad_local_choice = []
    for row in rows:
        scene_id = str(row.get("scene_id", ""))
        scene = scene_by_id.get(scene_id)
        if scene is None:
            bad_scene.append(scene_id)
            continue
        valid_ids = {obj.id for obj in scene.listener_objects()}
        for field in SELECTED_FIELDS:
            if field in row and OBJ_ID_RE.search(str(row[field])):
                leaks.append(f"{scene_id}:{field}:{row[field]}")
        for field in ("candidates", "kept_candidates"):
            for message in row.get(field, []) or []:
                if OBJ_ID_RE.search(str(message)):
                    leaks.append(f"{scene_id}:{field}:{message}")
        for method, message in (row.get("methods") or {}).items():
            if OBJ_ID_RE.search(str(message)):
                leaks.append(f"{scene_id}:methods.{method}:{message}")
        bad_local_choice.extend(invalid_local_choices(row, valid_ids, scene_id))

    add_check(checks, f"{path}.scene_ids_known", not bad_scene, ok_or_sample(bad_scene, "all rows mapped"))
    add_check(
        checks,
        f"{path}.messages_no_object_id_leakage",
        not leaks,
        "no audit candidate/selection contains obj_* IDs" if not leaks else sample(leaks),
    )
    add_check(
        checks,
        f"{path}.local_choice_ids_valid",
        not bad_local_choice,
        "all local selector choices are valid object IDs" if not bad_local_choice else sample(bad_local_choice),
    )
    return len(rows)


def invalid_local_choices(row: dict[str, Any], valid_ids: set[str], scene_id: str) -> list[str]:
    bad = []
    for field in LOCAL_CHOICE_FIELDS:
        for choice in row.get(field, []) or []:
            choice_id = str(choice.get("choice_id", ""))
            if choice_id not in valid_ids:
                bad.append(f"{scene_id}:{field}:{choice_id}")
    return bad


def summarize_cache(cache_dir: Path, checks: list[dict[str, Any]]) -> dict[str, Any]:
    files = sorted(cache_dir.glob("*.json"))
    add_check(checks, "data/cached_responses.cache_files_present", bool(files), f"{len(files)} cache files")
    model_counts: Counter[tuple[str, str]] = Counter()
    unreadable = []
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            unreadable.append(str(path))
            continue
        requested = str(payload.get("request_hash_payload", {}).get("model", "unknown"))
        actual = str(payload.get("data", {}).get("model", "unknown"))
        model_counts[(requested, actual)] += 1
    add_check(
        checks,
        "data/cached_responses.cache_files_readable",
        not unreadable,
        "all cache files parse as JSON" if not unreadable else sample(unreadable),
    )
    return {
        "n_cache_files": len(files),
        "model_versions": [
            {"requested_model": requested, "response_model": actual, "n": count}
            for (requested, actual), count in sorted(model_counts.items())
        ],
    }


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "ok": bool(ok), "detail": detail})


def sample(values: list[str], n: int = 5) -> str:
    suffix = "" if len(values) <= n else f" ... ({len(values)} total)"
    return ", ".join(values[:n]) + suffix


def ok_or_sample(values: list[str], ok_text: str) -> str:
    return ok_text if not values else sample(values)


def method_scene_detail(method_scenes: dict[str, set[str]]) -> str:
    return ", ".join(f"{method}:{len(scenes)}" for method, scenes in sorted(method_scenes.items()))


def markdown_report(report: dict[str, Any]) -> str:
    checks = report["checks"]
    lines = [
        "# Benchmark Integrity Audit",
        "",
        f"Checks passed: {sum(1 for check in checks if check['ok'])}/{len(checks)}.",
        "",
        "## Artifact Summary",
        "",
        "| Group | Source scenes | Record rows | Candidate rows | Audit rows | Speaker cache paths |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for group in report["summary"]["groups"]:
        lines.append(
            "| {name} | {n_scenes} | {record_rows} | {candidate_rows} | {audit_rows} | {speaker_cache_paths} |".format(
                **group
            )
        )

    lines.extend(
        [
            "",
            "## Cached Model Versions",
            "",
            "| Requested model | Response model | Cached responses |",
            "|---|---|---:|",
        ]
    )
    for row in report["summary"]["cache"]["model_versions"]:
        lines.append(f"| `{row['requested_model']}` | `{row['response_model']}` | {row['n']} |")

    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        for warning in report["warnings"]:
            lines.append(f"- {warning}")

    lines.extend(
        [
            "",
            "## Checks",
            "",
            "| Status | Check | Detail |",
            "|---|---|---|",
        ]
    )
    for check in checks:
        status = "PASS" if check["ok"] else "FAIL"
        lines.append(f"| {status} | `{check['name']}` | {check['detail']} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
