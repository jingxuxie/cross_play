#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.api_client import OpenAIResponsesClient
from prag_crossplay.data import read_jsonl, read_scenes, write_jsonl
from prag_crossplay.local_agents import Choice
from prag_crossplay.methods import (
    evaluate_candidates,
    evaluate_message,
    oracle_rows_from_candidate_records,
    select_shortest,
)
from prag_crossplay.prompts import listener_prompt
from prag_crossplay.scoring import (
    markdown_table,
    paired_comparison_markdown,
    paired_method_comparison,
    summarize_records,
    write_summary,
)


class ApiHeldoutListener:
    def __init__(
        self,
        client: OpenAIResponsesClient,
        model: str,
        style: str,
        max_output_tokens: int,
    ) -> None:
        self.client = client
        self.model = model
        self.style = style
        self.name = f"{model}:{style_label(style)}"
        self.max_output_tokens = max_output_tokens

    def choose(self, scene: Any, utterance: str) -> Choice:
        system, user = listener_prompt(scene, utterance, self.style)
        payload, result = self.client.call_json(
            system,
            user,
            max_output_tokens=self.max_output_tokens,
            schema_version=f"listener-{self.style}-v1",
        )
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
        description=(
            "Evaluate already-selected messages with a new held-out API listener model. "
            "This reuses cached speaker candidates and makes no speaker calls."
        )
    )
    parser.add_argument("--scene-file", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--model", default="gpt-5.5")
    parser.add_argument(
        "--temperature",
        type=parse_temperature,
        default=None,
        help="Sampling temperature, or 'none' to omit the API parameter. Default: none.",
    )
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument(
        "--reasoning-effort",
        type=parse_optional_string,
        default="none",
        help="Reasoning effort, or 'omit' to omit the API parameter. Default: none.",
    )
    parser.add_argument("--listener-max-output-tokens", type=int, default=256)
    parser.add_argument("--max-scenes", type=int, default=0)
    parser.add_argument("--records-out", required=True)
    parser.add_argument("--summary-out", required=True)
    parser.add_argument("--markdown-out", required=True)
    parser.add_argument("--paired-json-out", required=True)
    parser.add_argument("--paired-markdown-out", required=True)
    parser.add_argument("--audit-out", required=True)
    parser.add_argument(
        "--include-existing-oracle-message",
        action="store_true",
        help=(
            "Evaluate the oracle candidate selected by an existing all-candidate "
            "record file. This is cheap but is not a same-model oracle."
        ),
    )
    parser.add_argument(
        "--existing-candidate-records",
        default=None,
        help="Prior all-candidate records used only to recover a prior-listener oracle message.",
    )
    parser.add_argument(
        "--evaluate-all-candidates",
        action="store_true",
        help="Also evaluate every candidate with this listener model and compute a true same-model oracle.",
    )
    parser.add_argument(
        "--all-candidate-records-out",
        default=None,
        help="Required with --evaluate-all-candidates.",
    )
    parser.add_argument("--checkpoint-every", type=int, default=1)
    args = parser.parse_args()

    if args.include_existing_oracle_message and not args.existing_candidate_records:
        raise SystemExit("--existing-candidate-records is required with --include-existing-oracle-message")
    if args.evaluate_all_candidates and not args.all_candidate_records_out:
        raise SystemExit("--all-candidate-records-out is required with --evaluate-all-candidates")

    scenes = read_scenes(args.scene_file)
    if args.max_scenes > 0:
        scenes = scenes[: args.max_scenes]
    scenes_by_id = {scene.scene_id: scene for scene in scenes}
    candidate_rows = [row for row in read_jsonl(args.candidates) if row["scene_id"] in scenes_by_id]
    prior_oracle_by_scene = (
        prior_oracle_messages(args.existing_candidate_records)
        if args.include_existing_oracle_message
        else {}
    )

    client = OpenAIResponsesClient(
        model=args.model,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        cache_dir=args.cache_dir,
    )
    listeners = [
        ApiHeldoutListener(
            client,
            args.model,
            "heldout_direct_last",
            args.listener_max_output_tokens,
        ),
        ApiHeldoutListener(
            client,
            args.model,
            "heldout_careful",
            args.listener_max_output_tokens,
        ),
        ApiHeldoutListener(
            client,
            args.model,
            "heldout_strict_last",
            args.listener_max_output_tokens,
        ),
    ]
    listener_fns = [listener.choose for listener in listeners]

    records: list[dict[str, Any]] = []
    candidate_eval_records: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    for scene_index, candidate_row in enumerate(candidate_rows, start=1):
        scene = scenes_by_id[candidate_row["scene_id"]]
        candidates = [str(message) for message in candidate_row["candidates"]]
        selections = selected_messages(candidate_row, candidates)
        if args.include_existing_oracle_message:
            prior_oracle = prior_oracle_by_scene.get(scene.scene_id)
            if prior_oracle:
                selections.append(("prior_listener_oracle", prior_oracle))

        scene_candidate_records: list[dict[str, Any]] = []
        if args.evaluate_all_candidates:
            scene_candidate_records = evaluate_candidates(scene, candidates, listener_fns)
            candidate_eval_records.extend(scene_candidate_records)

        for method, message in selections:
            records.extend(evaluate_message(scene, method, message, listener_fns))
        if args.evaluate_all_candidates:
            records.extend(oracle_rows_from_candidate_records(scene_candidate_records, candidates))

        audit_rows.append(
            {
                "scene_id": scene.scene_id,
                "scenario_type": scene.scenario_type,
                "candidate_count": len(candidates),
                "methods": {method: message for method, message in selections},
                "evaluated_all_candidates": args.evaluate_all_candidates,
            }
        )

        if args.checkpoint_every and scene_index % args.checkpoint_every == 0:
            write_outputs(args, records, audit_rows, candidate_eval_records)
            print(f"checkpoint {scene_index}/{len(candidate_rows)} scenes", flush=True)

    write_outputs(args, records, audit_rows, candidate_eval_records)
    summary = summarize_records(records)
    write_summary(args.summary_out, summary)
    markdown = report_markdown(args, records, summary)
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown, encoding="utf-8")

    comparisons = paired_comparisons(records)
    Path(args.paired_json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.paired_json_out).write_text(
        json.dumps(comparisons, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    Path(args.paired_markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.paired_markdown_out).write_text(
        paired_comparison_markdown(comparisons),
        encoding="utf-8",
    )

    print(markdown)


def style_label(style: str) -> str:
    if style == "heldout_direct_last":
        return "direct_last"
    if style == "heldout_careful":
        return "careful"
    if style == "heldout_strict_last":
        return "strict_last"
    return style


def parse_temperature(value: str) -> float | None:
    if value.lower() in {"none", "null", "omit"}:
        return None
    return float(value)


def parse_optional_string(value: str) -> str | None:
    if value.lower() in {"none_param", "null", "omit"}:
        return None
    return value


def selected_messages(candidate_row: dict[str, Any], candidates: list[str]) -> list[tuple[str, str]]:
    selections = [
        ("direct_first", candidates[0]),
        ("best_of_k_shortest", str(select_shortest(candidates)["message"])),
    ]
    if candidate_row.get("mirror_selected"):
        selections.append(("mirror_selfplay", str(candidate_row["mirror_selected"])))
    if candidate_row.get("population_selected"):
        selections.append(("population_play", str(candidate_row["population_selected"])))
    return selections


def prior_oracle_messages(records_path: str | Path) -> dict[str, str]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(records_path):
        if row["method"] == "oracle_upper_bound":
            grouped.setdefault(row["scene_id"], []).append(row)
    return {scene_id: rows[0]["message"] for scene_id, rows in grouped.items()}


def paired_comparisons(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    comparisons = [
        paired_method_comparison(records, "population_play", "mirror_selfplay"),
    ]
    if any(row["method"] == "prior_listener_oracle" for row in records):
        comparisons.append(
            paired_method_comparison(records, "prior_listener_oracle", "mirror_selfplay")
        )
    if any(row["method"] == "oracle_upper_bound" for row in records):
        comparisons.append(
            paired_method_comparison(records, "oracle_upper_bound", "mirror_selfplay")
        )
    return comparisons


def write_outputs(
    args: argparse.Namespace,
    records: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    candidate_eval_records: list[dict[str, Any]],
) -> None:
    write_jsonl(args.records_out, records)
    write_jsonl(args.audit_out, audit_rows)
    if args.evaluate_all_candidates:
        write_jsonl(args.all_candidate_records_out, candidate_eval_records)


def report_markdown(args: argparse.Namespace, records: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        f"# {args.model} Selected-Message Listener Audit",
        "",
        "This run reuses cached speaker candidates and evaluates selected messages with three held-out listener prompts.",
        "",
        f"- Scene file: `{args.scene_file}`.",
        f"- Candidate file: `{args.candidates}`.",
        f"- Scenes: `{summary['overall']['n_scenes']}`.",
        f"- Listener calls represented: `{len(records)}`.",
        f"- True same-model oracle evaluated: `{args.evaluate_all_candidates}`.",
        "",
        "## Results",
        "",
        markdown_table(summary).strip(),
        "",
        "## Paired Comparisons",
        "",
        paired_comparison_markdown(paired_comparisons(records)).strip(),
        "",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
