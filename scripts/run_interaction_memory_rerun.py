#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.api_client import OpenAIResponsesClient, parse_json_object
from prag_crossplay.data import Scene, read_jsonl, read_scenes, write_jsonl
from prag_crossplay.local_agents import Choice
from prag_crossplay.methods import evaluate_message, token_count
from prag_crossplay.prompts import listener_prompt, scene_payload
from prag_crossplay.scoring import paired_method_comparison, summarize_records, write_summary
from scripts.run_hybrid_api_pilot import parse_optional_string, parse_temperature


RULES = [
    "If another visible object shares the target's size/color/shape, add a visible discriminator such as row/column or an unambiguous spatial relation.",
    "When speaker and listener perspectives differ, avoid relying only on left/right; prefer listener-invariant coordinates or visible anchors.",
    "Use only listener-visible landmarks; never mention hidden or private landmarks.",
    "If exact coordinates are disallowed, prefer the relational/spatial candidate over a short attribute-only candidate when both seem locally acceptable.",
]

DEFAULT_CONDITIONS = ["perspective_mirror_failure", "partial_mirror_failure"]


class ApiHeldoutListenerCapped:
    def __init__(
        self,
        client: OpenAIResponsesClient,
        name: str,
        style: str,
        max_output_tokens: int,
    ) -> None:
        self.client = client
        self.name = name
        self.style = style
        self.max_output_tokens = max_output_tokens

    def choose(self, scene: Scene, utterance: str) -> Choice:
        system, user = listener_prompt(scene, utterance, self.style)
        schema_version = f"listener-{self.style}-v1"
        result = self.client.call(
            system,
            user,
            max_output_tokens=self.max_output_tokens,
            schema_version=schema_version,
        )
        try:
            payload = parse_json_object(result.text)
        except ValueError:
            retry_cap = max(600, self.max_output_tokens * 3)
            result = self.client.call(
                system,
                user,
                max_output_tokens=retry_cap,
                schema_version=f"{schema_version}-retry{retry_cap}",
            )
            payload = parse_json_object(result.text)
        valid_ids = {obj.id for obj in scene.listener_objects()}
        choice_id = str(payload.get("choice_id", ""))
        if choice_id not in valid_ids:
            choice_id = sorted(valid_ids)[0]
        return Choice(
            listener=self.name,
            choice_id=choice_id,
            confidence=float(payload.get("confidence", 0.0) or 0.0),
            ambiguity=bool(payload.get("ambiguity", False)),
            reason_code=str(payload.get("reason_code", "other")),
            raw_response=result.text,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a small GPT-5.5 interaction-memory prompt rerun on human-packet mirror failures."
    )
    parser.add_argument("--answer-key", default="results/human_validation_answer_key.json")
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument("--temperature", type=parse_temperature, default=0.0)
    parser.add_argument("--reasoning-effort", type=parse_optional_string, default=None)
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument("--conditions", nargs="+", default=DEFAULT_CONDITIONS)
    parser.add_argument("--max-items", type=int, default=15)
    parser.add_argument("--speaker-max-output-tokens", type=int, default=180)
    parser.add_argument("--listener-max-output-tokens", type=int, default=300)
    parser.add_argument("--strict-listener-max-output-tokens", type=int, default=300)
    parser.add_argument("--records-out", default="results/interaction_memory_prompt_rerun_records.jsonl")
    parser.add_argument("--messages-out", default="results/interaction_memory_prompt_rerun_messages.jsonl")
    parser.add_argument("--summary-out", default="results/interaction_memory_prompt_rerun_summary.json")
    parser.add_argument("--markdown-out", default="docs/interaction_memory_prompt_rerun.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    items = selected_items(args.answer_key, set(args.conditions), args.max_items)
    scene_cache = load_scene_cache(items)
    baseline = load_gpt55_baselines()

    client = OpenAIResponsesClient(
        model=args.model,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        cache_dir=args.cache_dir,
    )
    heldout = [
        ApiHeldoutListenerCapped(
            client,
            f"{args.model}:direct_last",
            "heldout_direct_last",
            args.listener_max_output_tokens,
        ),
        ApiHeldoutListenerCapped(
            client,
            f"{args.model}:careful",
            "heldout_careful",
            args.listener_max_output_tokens,
        ),
        ApiHeldoutListenerCapped(
            client,
            f"{args.model}:strict_last",
            "heldout_strict_last",
            args.strict_listener_max_output_tokens,
        ),
    ]
    heldout_fns = [listener.choose for listener in heldout]

    records: list[dict[str, Any]] = []
    message_rows: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        scene = scene_cache[item["scene_file"]][item["scene_id"]]
        system, user = memory_speaker_prompt(scene, item)
        if args.dry_run:
            message = "[dry-run]"
            speaker_result = None
            payload = {}
        else:
            payload, speaker_result = client.call_json(
                system,
                user,
                max_output_tokens=args.speaker_max_output_tokens,
                schema_version="interaction-memory-speaker-v1",
            )
            message = str(payload.get("message", "")).strip()
            if not message:
                utterances = payload.get("utterances", [])
                if isinstance(utterances, list) and utterances:
                    message = str(utterances[0]).strip()
            if not message:
                raise RuntimeError(f"{item['item_id']}: empty memory-speaker message")

        baseline_rows = baseline.get(item["scene_id"], {})
        message_rows.append(
            {
                "item_id": item["item_id"],
                "condition": item["condition"],
                "scene_id": item["scene_id"],
                "scene_file": item["scene_file"],
                "scenario_type": scene.scenario_type,
                "target_id": scene.target_id,
                "target_description": item["target_description"],
                "failed_mirror_message": item["message"],
                "failed_mirror_success_original": item["heldout_success_rate"],
                "gpt55_mirror_success": baseline_success(baseline_rows, "mirror_selfplay"),
                "gpt55_population_success": baseline_success(baseline_rows, "population_play"),
                "memory_message": message,
                "memory_message_tokens": token_count(message) if not args.dry_run else None,
                "rules": RULES,
                "speaker_model": args.model,
                "speaker_prompt_schema": "interaction-memory-speaker-v1",
                "speaker_cached": None if speaker_result is None else speaker_result.cached,
                "speaker_usage": None if speaker_result is None else speaker_result.usage,
                "speaker_cache_path": None if speaker_result is None else speaker_result.cache_path,
                "speaker_raw": None if speaker_result is None else speaker_result.text,
            }
        )
        if not args.dry_run:
            for row in evaluate_message(scene, "interaction_memory_prompt", message, heldout_fns):
                row["item_id"] = item["item_id"]
                row["condition"] = item["condition"]
                row["failed_mirror_message"] = item["message"]
                records.append(row)
        print(f"{index}/{len(items)} {item['item_id']} {item['scene_id']}: {message}", flush=True)

    write_jsonl(args.messages_out, message_rows)
    if not args.dry_run:
        baseline_record_rows = baseline_records_for_items(items, baseline)
        all_records = baseline_record_rows + records
        write_jsonl(args.records_out, all_records)
        summary = summarize_rerun(items, message_rows, all_records)
        write_summary(args.summary_out, summary)
        Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.markdown_out).write_text(render_markdown(summary), encoding="utf-8")
        print(render_markdown(summary))
    else:
        print(f"dry-run wrote messages={args.messages_out}")


def selected_items(answer_key_path: str, conditions: set[str], max_items: int) -> list[dict[str, Any]]:
    data = json.loads(Path(answer_key_path).read_text(encoding="utf-8"))
    items = [item for item in data["items"] if item["condition"] in conditions]
    if max_items > 0:
        items = items[:max_items]
    if not items:
        raise RuntimeError("no matching answer-key items")
    return items


def load_scene_cache(items: list[dict[str, Any]]) -> dict[str, dict[str, Scene]]:
    scene_files = sorted({item["scene_file"] for item in items})
    return {
        scene_file: {scene.scene_id: scene for scene in read_scenes(scene_file)}
        for scene_file in scene_files
    }


def load_gpt55_baselines() -> dict[str, dict[str, list[dict[str, Any]]]]:
    paths = [
        "results/gpt55_perspective_selected_records.jsonl",
        "results/gpt55_partial_observability_selected_records.jsonl",
    ]
    out: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for path in paths:
        if not Path(path).exists():
            continue
        for row in read_jsonl(path):
            if row["method"] in {"mirror_selfplay", "population_play"}:
                out[row["scene_id"]][row["method"]].append(row)
    return {scene_id: dict(by_method) for scene_id, by_method in out.items()}


def memory_speaker_prompt(scene: Scene, item: dict[str, Any]) -> tuple[str, str]:
    target = scene.target()
    target_attrs = {
        "color": target.color,
        "shape": target.shape,
        "size": target.size,
        "row": target.y,
        "column": target.x,
    }
    system = (
        "You are the SPEAKER in a situated reference game. You previously saw a message "
        "fail under held-out listeners. Use the interaction-memory rules to write one "
        "short replacement message that lets the listener identify the exact target. "
        "Use only listener-visible information, never mention the hidden target ID, and "
        "return valid JSON only."
    )
    user = (
        "Scene:\n"
        f"{json.dumps(scene_payload(scene), indent=2, sort_keys=True)}\n\n"
        f"Target object ID visible only to you: {scene.target_id}\n"
        f"Target object attributes visible to you: {json.dumps(target_attrs, sort_keys=True)}\n"
        f"Previously failed message: {json.dumps(item['message'])}\n"
        f"Observed failure condition: {item['condition']}\n\n"
        "Interaction-memory rules:\n"
        + "\n".join(f"{idx}. {rule}" for idx, rule in enumerate(RULES, start=1))
        + "\n\n"
        "Write exactly one replacement message, at most 25 words. Prefer coordinates only "
        "when they are the clearest listener-invariant visible discriminator.\n"
        'Return exactly this JSON shape: {"message": "..."}'
    )
    return system, user


def baseline_success(rows_by_method: dict[str, list[dict[str, Any]]], method: str) -> float | None:
    rows = rows_by_method.get(method, [])
    if not rows:
        return None
    return mean(float(row["success"]) for row in rows)


def baseline_records_for_items(
    items: list[dict[str, Any]],
    baseline: dict[str, dict[str, list[dict[str, Any]]]],
) -> list[dict[str, Any]]:
    item_by_scene = {item["scene_id"]: item for item in items}
    rows = []
    for scene_id, by_method in baseline.items():
        if scene_id not in item_by_scene:
            continue
        item = item_by_scene[scene_id]
        for method in ["mirror_selfplay", "population_play"]:
            for row in by_method.get(method, []):
                copied = dict(row)
                copied["item_id"] = item["item_id"]
                copied["condition"] = item["condition"]
                rows.append(copied)
    return rows


def summarize_rerun(
    items: list[dict[str, Any]],
    message_rows: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    summary = summarize_records(records)
    comparisons = [
        paired_method_comparison(records, "interaction_memory_prompt", "mirror_selfplay"),
        paired_method_comparison(records, "interaction_memory_prompt", "population_play"),
    ]
    for condition in sorted({item["condition"] for item in items}):
        comparisons.append(
            paired_method_comparison(
                records,
                "interaction_memory_prompt",
                "mirror_selfplay",
                scenario_type=None,
                n_boot=5000,
                seed=stable_seed(condition),
            )
        )
        comparisons[-1]["condition"] = condition
        comparisons[-1] = paired_condition_comparison(
            records,
            "interaction_memory_prompt",
            "mirror_selfplay",
            condition,
            seed=stable_seed(condition),
        )

    return {
        "n_items": len(items),
        "condition_counts": dict(Counter(item["condition"] for item in items)),
        "speaker_model": message_rows[0]["speaker_model"] if message_rows else None,
        "prompt_schema": "interaction-memory-speaker-v1",
        "rules": RULES,
        "by_method": summary["by_method"],
        "by_condition_method": by_condition_method(records),
        "comparisons": comparisons,
        "messages": message_rows,
    }


def paired_condition_comparison(
    records: list[dict[str, Any]],
    method_a: str,
    method_b: str,
    condition: str,
    seed: int,
) -> dict[str, Any]:
    filtered = [row for row in records if row.get("condition") == condition]
    comp = paired_method_comparison(filtered, method_a, method_b, n_boot=5000, seed=seed)
    comp["condition"] = condition
    return comp


def by_condition_method(records: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        grouped[str(row.get("condition", "unknown"))][row["method"]].append(row)
    out = {}
    for condition, by_method in grouped.items():
        out[condition] = {}
        for method, rows in by_method.items():
            out[condition][method] = {
                "n_records": len(rows),
                "n_items": len({row["item_id"] for row in rows}),
                "success": mean(float(row["success"]) for row in rows),
                "mean_tokens": mean(float(row["message_tokens"]) for row in rows),
            }
    return dict(sorted(out.items()))


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Interaction-Memory Prompt Rerun",
        "",
        "This bounded API audit tests whether the failure-derived interaction-memory rules can repair the mirror-failure items prepared for human validation. It is not a human-subjects result; it is a prompt-rerun diagnostic on the same sampled failure scenes.",
        "",
        "## Summary",
        "",
        f"Items: {report['n_items']}. Conditions: {format_counts(report['condition_counts'])}. Speaker/listener model: `{report['speaker_model']}`.",
        "",
        "| Method | Success | Same-play | Gap | Mean tokens | Records |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for method in ["mirror_selfplay", "interaction_memory_prompt", "population_play"]:
        stats = report["by_method"].get(method)
        if not stats:
            continue
        lines.append(
            "| {method} | {success:.3f} | {same} | {gap} | {tokens:.1f} | {records} |".format(
                method=method,
                success=stats["success"],
                same=fmt(stats.get("sameplay_success")),
                gap=fmt(stats.get("crossplay_gap")),
                tokens=stats["mean_tokens"],
                records=stats["n_records"],
            )
        )

    lines.extend(["", "## By Condition", "", "| Condition | Method | Items | Success | Mean tokens |", "|---|---|---:|---:|---:|"])
    for condition, by_method in report["by_condition_method"].items():
        for method in ["mirror_selfplay", "interaction_memory_prompt", "population_play"]:
            stats = by_method.get(method)
            if not stats:
                continue
            lines.append(
                f"| {condition} | {method} | {stats['n_items']} | {stats['success']:.3f} | {stats['mean_tokens']:.1f} |"
            )

    lines.extend(["", "## Paired Comparisons", "", "| Condition | A | B | N | Mean A | Mean B | Diff A-B | 95% CI | p_boot |", "|---|---|---|---:|---:|---:|---:|---:|---:|"])
    for comp in report["comparisons"]:
        if comp["n_pairs"] == 0:
            continue
        condition = comp.get("condition", "overall")
        ci = comp["diff_ci95"]
        lines.append(
            "| {condition} | {a} | {b} | {n} | {ma:.3f} | {mb:.3f} | {diff:.3f} | [{lo:.3f}, {hi:.3f}] | {p:.4f} |".format(
                condition=condition,
                a=comp["method_a"],
                b=comp["method_b"],
                n=comp["n_pairs"],
                ma=comp["mean_a"],
                mb=comp["mean_b"],
                diff=comp["diff_a_minus_b"],
                lo=ci[0],
                hi=ci[1],
                p=comp["paired_bootstrap_p_two_sided"],
            )
        )

    lines.extend(["", "## Generated Messages", "", "| Item | Condition | Scene | Failed mirror message | Memory message |", "|---|---|---|---|---|"])
    for row in report["messages"]:
        lines.append(
            f"| {row['item_id']} | {row['condition']} | `{row['scene_id']}` | {row['failed_mirror_message']} | {row['memory_message']} |"
        )

    lines.extend(["", "## Claim Boundary", ""])
    lines.append(
        "Safe to claim: on this bounded human-packet failure sample, the distilled rules can be used as a prompt memory to generate replacement messages and evaluate them under the same GPT-5.5 held-out listener styles."
    )
    lines.append(
        "Not safe to claim: this is not evidence that human listeners agree, nor that an online learning system would discover the rules without the author-coded failure analysis."
    )
    return "\n".join(lines) + "\n"


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


def format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))


def stable_seed(text: str) -> int:
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(text)) % 10000


if __name__ == "__main__":
    main()
