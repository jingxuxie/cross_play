#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import Scene, write_scenes
from prag_crossplay.local_agents import candidate_messages, heldout_listeners, training_listeners
from prag_crossplay.methods import score_choice, select_mirror_selfplay, select_population_play, token_count
from prag_crossplay.scenes import generate_scenes


EXACT_COORD_RE = re.compile(
    r"\brow\s+\d+\b|\bcolumn\s+\d+\b|\b\d+(?:st|nd|rd|th)?\s+row\b|\b\d+(?:st|nd|rd|th)?\s+column\b",
    re.IGNORECASE,
)

METHOD_LABELS = {
    "mirror": "Mirror",
    "population": "Population",
    "consensus+info": "Consensus+info",
    "oracle": "Oracle",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a no-API stronger-plan diagnostic at 1,000+200 local scenes and K=8."
    )
    parser.add_argument("--seed", type=int, default=20260628)
    parser.add_argument("--max-k", type=int, default=8)
    parser.add_argument("--scene-out", default="data/local_stronger_plan1200_scenes.jsonl")
    parser.add_argument("--markdown-out", default="docs/local_stronger_plan_k8.md")
    parser.add_argument("--json-out", default="results/local_stronger_plan_k8.json")
    args = parser.parse_args()

    report = build_report(seed=args.seed, max_k=args.max_k, scene_out=args.scene_out)
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def build_report(*, seed: int, max_k: int, scene_out: str) -> dict[str, Any]:
    counts = {
        "unique_attribute": 250,
        "distractor_contrast": 250,
        "relational_reference": 250,
        "perspective_shift": 250,
        "partial_observability": 200,
    }
    scenes = generate_scenes(counts, split="stronger_local", seed=seed)
    write_scenes(scene_out, scenes)
    scenario_counts = dict(sorted(Counter(scene.scenario_type for scene in scenes).items()))
    scene_groups = {
        "initial_1000": [scene for scene in scenes if scene.scenario_type != "partial_observability"],
        "partial_200": [scene for scene in scenes if scene.scenario_type == "partial_observability"],
        "combined_1200": scenes,
    }

    candidate_cache = {scene.scene_id: candidate_messages(scene, k=max_k) for scene in scenes}
    eval_cache = {
        scene.scene_id: evaluate_candidates(scene, candidate_cache[scene.scene_id])
        for scene in scenes
    }

    budget_rows: list[dict[str, Any]] = []
    selector_rows: list[dict[str, Any]] = []
    for group_name, group_scenes in scene_groups.items():
        for filter_name in ["full", "no_exact_coordinates"]:
            for k in [1, 4, max_k]:
                budget_rows.append(
                    candidate_budget_row(group_name, group_scenes, candidate_cache, eval_cache, k, filter_name)
                )
            for k in [4, max_k]:
                selector_rows.extend(
                    selector_summary_rows(group_name, group_scenes, candidate_cache, eval_cache, k, filter_name)
                )

    return {
        "source_plan": "cross_play_pragmatics_workshop_plan.md",
        "seed": seed,
        "scene_file": scene_out,
        "n_scenes": len(scenes),
        "scenario_counts": scenario_counts,
        "candidate_protocol": {
            "max_k": max_k,
            "note": "The first four local candidate slots match the existing K=4 protocol; slots 5-8 add local non-coordinate fallbacks for no-API stronger-plan diagnostics.",
        },
        "budget_rows": budget_rows,
        "selector_rows": selector_rows,
        "key_observations": key_observations(budget_rows, selector_rows),
    }


def evaluate_candidates(scene: Scene, candidates: list[str]) -> list[dict[str, Any]]:
    heldout = heldout_listeners()
    rows = []
    for candidate_index, message in enumerate(candidates):
        choices = [listener.choose(scene, message) for listener in heldout]
        successes = [score_choice(choice, scene.target_id) for choice in choices]
        rows.append(
            {
                "candidate_index": candidate_index,
                "message": message,
                "tokens": token_count(message),
                "heldout_success": mean(successes),
                "robust": all(successes),
                "exact_coordinate": bool(EXACT_COORD_RE.search(message)),
            }
        )
    return rows


def candidate_budget_row(
    group_name: str,
    scenes: list[Scene],
    candidate_cache: dict[str, list[str]],
    eval_cache: dict[str, list[dict[str, Any]]],
    k: int,
    filter_name: str,
) -> dict[str, Any]:
    candidate_counts = []
    robust_counts = []
    robust_scene_flags = []
    oracle_successes = []
    skipped = 0
    for scene in scenes:
        rows = candidate_rows(eval_cache[scene.scene_id], k, filter_name)
        if not rows:
            skipped += 1
            continue
        candidate_counts.append(len(rows))
        robust_counts.append(sum(1 for row in rows if row["robust"]))
        robust_scene_flags.append(any(row["robust"] for row in rows))
        oracle_successes.append(max(row["heldout_success"] for row in rows))
    return {
        "scope": group_name,
        "filter": filter_name,
        "k": k,
        "n_scenes": len(scenes),
        "skipped_scenes": skipped,
        "mean_candidates": mean(candidate_counts),
        "mean_robust_candidates": mean(robust_counts),
        "robust_scene_rate": mean(robust_scene_flags),
        "oracle_success": mean(oracle_successes),
    }


def selector_summary_rows(
    group_name: str,
    scenes: list[Scene],
    candidate_cache: dict[str, list[str]],
    eval_cache: dict[str, list[dict[str, Any]]],
    k: int,
    filter_name: str,
) -> list[dict[str, Any]]:
    method_values: dict[str, list[float]] = {method: [] for method in METHOD_LABELS}
    sameplay_values: dict[str, list[float]] = {"mirror": [], "population": []}
    exact_rates: dict[str, list[bool]] = {method: [] for method in METHOD_LABELS}
    token_values: dict[str, list[int]] = {method: [] for method in METHOD_LABELS}
    consensus_sources: Counter[str] = Counter()
    skipped = 0

    train = training_listeners()
    for scene in scenes:
        candidates = filtered_messages(candidate_cache[scene.scene_id], k, filter_name)
        if not candidates:
            skipped += 1
            continue
        eval_rows = eval_cache[scene.scene_id]

        mirror = select_mirror_selfplay(scene, candidates, train[0].choose)
        population = select_population_play(scene, candidates, [listener.choose for listener in train])
        consensus = select_consensus_else_informative(scene, candidates, train)
        oracle = select_oracle(eval_rows, k, filter_name)
        selections = {
            "mirror": mirror,
            "population": population,
            "consensus+info": consensus,
            "oracle": oracle,
        }
        for method, selection in selections.items():
            message = str(selection["message"])
            method_values[method].append(heldout_success(eval_rows, message))
            exact_rates[method].append(bool(EXACT_COORD_RE.search(message)))
            token_values[method].append(token_count(message))
        sameplay_values["mirror"].append(mean(score_choice(choice, scene.target_id) for choice in mirror["choices"]))
        sameplay_values["population"].append(
            mean(score_choice(choice, scene.target_id) for choice in population["choices"])
        )
        consensus_sources[str(consensus["source"])] += 1

    out = []
    for method in METHOD_LABELS:
        out.append(
            {
                "scope": group_name,
                "filter": filter_name,
                "k": k,
                "method": method,
                "n_scenes": len(scenes),
                "skipped_scenes": skipped,
                "success": mean(method_values[method]),
                "sameplay_success": mean(sameplay_values[method]) if method in sameplay_values else None,
                "crossplay_gap": (
                    mean(sameplay_values[method]) - mean(method_values[method])
                    if method in sameplay_values
                    else None
                ),
                "exact_coordinate_selection_rate": mean(exact_rates[method]),
                "mean_tokens": mean(token_values[method]),
                "consensus_source_counts": dict(sorted(consensus_sources.items()))
                if method == "consensus+info"
                else {},
            }
        )
    return out


def candidate_rows(rows: list[dict[str, Any]], k: int, filter_name: str) -> list[dict[str, Any]]:
    prefix = [row for row in rows if int(row["candidate_index"]) < k]
    if filter_name == "full":
        return prefix
    if filter_name == "no_exact_coordinates":
        return [row for row in prefix if not row["exact_coordinate"]]
    raise ValueError(f"unknown filter {filter_name}")


def filtered_messages(candidates: list[str], k: int, filter_name: str) -> list[str]:
    messages = candidates[:k]
    if filter_name == "full":
        return messages
    if filter_name == "no_exact_coordinates":
        return [message for message in messages if not EXACT_COORD_RE.search(message)]
    raise ValueError(f"unknown filter {filter_name}")


def select_consensus_else_informative(scene: Scene, candidates: list[str], train: list[Any]) -> dict[str, Any]:
    scored = []
    for message in candidates:
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
    consensus = [row for row in scored if row["local_success"] >= 1.0]
    if consensus:
        best = max(consensus, key=lambda row: (row["informativeness"], -row["tokens"], row["message"]))
        return {"message": best["message"], "choices": best["choices"], "source": "consensus"}
    best = max(scored, key=lambda row: (row["informativeness"], row["tokens"], row["message"]))
    return {"message": best["message"], "choices": best["choices"], "source": "informativeness_fallback"}


def select_oracle(rows: list[dict[str, Any]], k: int, filter_name: str) -> dict[str, Any]:
    kept = candidate_rows(rows, k, filter_name)
    best = max(kept, key=lambda row: (row["heldout_success"], -row["tokens"], row["message"]))
    return {"message": best["message"]}


def heldout_success(rows: list[dict[str, Any]], message: str) -> float:
    for row in rows:
        if row["message"] == message:
            return float(row["heldout_success"])
    raise KeyError(message)


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


def key_observations(
    budget_rows: list[dict[str, Any]],
    selector_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    budget = {(row["scope"], row["filter"], row["k"]): row for row in budget_rows}
    selectors = {
        (row["scope"], row["filter"], row["k"], row["method"]): row
        for row in selector_rows
    }
    return {
        "initial_no_coord_oracle_k4": budget[("initial_1000", "no_exact_coordinates", 4)]["oracle_success"],
        "initial_no_coord_oracle_k8": budget[("initial_1000", "no_exact_coordinates", 8)]["oracle_success"],
        "partial_no_coord_oracle_k4": budget[("partial_200", "no_exact_coordinates", 4)]["oracle_success"],
        "partial_no_coord_oracle_k8": budget[("partial_200", "no_exact_coordinates", 8)]["oracle_success"],
        "initial_no_coord_consensus_k8": selectors[
            ("initial_1000", "no_exact_coordinates", 8, "consensus+info")
        ]["success"],
        "partial_no_coord_consensus_k8": selectors[
            ("partial_200", "no_exact_coordinates", 8, "consensus+info")
        ]["success"],
        "combined_full_population_k8": selectors[("combined_1200", "full", 8, "population")]["success"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    obs = report["key_observations"]
    lines = [
        "# Local Stronger-Plan K=8 Diagnostic",
        "",
        "This generated no-API diagnostic exercises the stronger-plan scale locally: 1,000 initial-family scenes plus 200 partial-observability stress scenes.",
        "It is artifact support for scale and K=8 candidate diversity, not a replacement for the cached API listener results in the paper.",
        "",
        f"Scene file: `{report['scene_file']}`",
        f"Seed: `{report['seed']}`",
        "",
        "## Dataset",
        "",
        "| Scenario type | Scenes |",
        "|---|---:|",
    ]
    for scenario, count in report["scenario_counts"].items():
        lines.append(f"| {scenario} | {count} |")

    lines.extend(
        [
            "",
            "## Key Observations",
            "",
            f"- No-coordinate oracle success on the initial 1,000 scenes rises from {fmt(obs['initial_no_coord_oracle_k4'])} at K=4 to {fmt(obs['initial_no_coord_oracle_k8'])} at K=8.",
            f"- No-coordinate oracle success on the 200 partial-observability scenes rises from {fmt(obs['partial_no_coord_oracle_k4'])} at K=4 to {fmt(obs['partial_no_coord_oracle_k8'])} at K=8.",
            f"- At K=8 without exact coordinates, consensus+info reaches {fmt(obs['initial_no_coord_consensus_k8'])} on the initial 1,000 scenes and {fmt(obs['partial_no_coord_consensus_k8'])} on partial-observability scenes.",
            f"- Full-candidate local K=8 population-play reaches {fmt(obs['combined_full_population_k8'])} over all 1,200 scenes.",
            "",
            "## Candidate Budget",
            "",
            "| Scope | Filter | K | Scenes | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle success |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in report["budget_rows"]:
        lines.append(
            f"| {row['scope']} | {row['filter']} | {row['k']} | {row['n_scenes']} | {fmt(row['mean_candidates'])} | {fmt(row['mean_robust_candidates'])} | {fmt(row['robust_scene_rate'])} | {fmt(row['oracle_success'])} |"
        )

    lines.extend(
        [
            "",
            "## Selector Summary",
            "",
            "| Scope | Filter | K | Method | Success | Same-play | Gap | Exact-coordinate selection | Tokens |",
            "|---|---|---:|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in report["selector_rows"]:
        lines.append(
            f"| {row['scope']} | {row['filter']} | {row['k']} | {METHOD_LABELS[row['method']]} | {fmt(row['success'])} | {fmt(row['sameplay_success'])} | {fmt(row['crossplay_gap'])} | {fmt(row['exact_coordinate_selection_rate'])} | {fmt(row['mean_tokens'])} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The local diagnostic supports two bounded stronger-plan conclusions: the released generator runs at the 1,000+200 scale, and K=8 can add useful non-coordinate candidate diversity after the original four slots.",
            "The result should stay scoped as local evidence because the paper-facing listener claims still come from cached API runs.",
            "",
        ]
    )
    return "\n".join(lines)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{float(value):.3f}"


if __name__ == "__main__":
    main()
