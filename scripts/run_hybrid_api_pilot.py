#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.api_client import OpenAIResponsesClient
from prag_crossplay.data import read_scenes, write_jsonl
from prag_crossplay.local_agents import Choice, template_message, training_listeners
from prag_crossplay.methods import (
    evaluate_candidates,
    evaluate_message,
    oracle_rows_from_candidate_records,
    select_mirror_selfplay,
    select_population_play,
    select_shortest,
)
from prag_crossplay.prompts import listener_prompt, speaker_prompt
from prag_crossplay.scoring import markdown_table, summarize_records, write_summary


class ApiHeldoutListener:
    def __init__(self, client: OpenAIResponsesClient, name: str, style: str) -> None:
        self.client = client
        self.name = name
        self.style = style

    def choose(self, scene, utterance: str) -> Choice:
        system, user = listener_prompt(scene, utterance, self.style)
        payload, result = self.client.call_json(
            system,
            user,
            max_output_tokens=120,
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene-file", default="data/dev_scenes.jsonl")
    parser.add_argument("--max-scenes", type=int, default=12)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument(
        "--speaker-prompt",
        choices=["standard", "no_coordinates"],
        default="standard",
    )
    parser.add_argument(
        "--speaker-max-output-tokens",
        type=int,
        default=None,
        help="Override speaker response cap; defaults to 220 for K<=4 and 700 otherwise.",
    )
    parser.add_argument(
        "--temperature",
        type=parse_temperature,
        default=0.0,
        help="Sampling temperature, or 'none' to omit the API parameter.",
    )
    parser.add_argument(
        "--reasoning-effort",
        type=parse_optional_string,
        default=None,
        help="Reasoning effort, or 'omit' to omit the API parameter.",
    )
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument("--records-out", default="results/hybrid_api_pilot_records.jsonl")
    parser.add_argument("--summary-out", default="results/hybrid_api_pilot_summary.json")
    parser.add_argument("--candidates-out", default="results/hybrid_api_pilot_candidates.jsonl")
    parser.add_argument("--all-candidate-records-out", default=None)
    parser.add_argument("--checkpoint-every", type=int, default=1)
    args = parser.parse_args()

    scenes = read_scenes(args.scene_file)
    if args.max_scenes > 0:
        scenes = scenes[: args.max_scenes]
    client = OpenAIResponsesClient(
        model=args.model,
        temperature=args.temperature,
        reasoning_effort=args.reasoning_effort,
        cache_dir=args.cache_dir,
    )
    local_train = training_listeners()
    heldout = [
        ApiHeldoutListener(client, "L_test_direct_last_api", "heldout_direct_last"),
        ApiHeldoutListener(client, "L_test_careful_api", "heldout_careful"),
        ApiHeldoutListener(client, "L_test_strict_last_api", "heldout_strict_last"),
    ]
    heldout_fns = [listener.choose for listener in heldout]

    records: list[dict[str, Any]] = []
    all_candidate_records: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    speaker_max_output_tokens = (
        args.speaker_max_output_tokens
        if args.speaker_max_output_tokens is not None
        else (220 if args.k <= 4 else 700)
    )
    speaker_schema_version = (
        "speaker-v2-target-attrs"
        if args.speaker_prompt == "standard"
        else f"speaker-{args.speaker_prompt}-v1-target-attrs"
    )
    for scene_index, scene in enumerate(scenes, start=1):
        system, user = speaker_prompt(scene, args.k, mode=args.speaker_prompt)
        payload, speaker_result = client.call_json(
            system,
            user,
            max_output_tokens=speaker_max_output_tokens,
            schema_version=speaker_schema_version,
        )
        candidates = [str(x).strip() for x in payload.get("utterances", []) if str(x).strip()]
        candidates = candidates[: args.k] or [template_message(scene)]

        mirror = select_mirror_selfplay(scene, candidates, local_train[0].choose)
        population = select_population_play(scene, candidates, [listener.choose for listener in local_train])
        shortest = select_shortest(candidates)
        candidate_eval_rows = evaluate_candidates(scene, candidates, heldout_fns)
        all_candidate_records.extend(candidate_eval_rows)

        records.extend(evaluate_message(scene, "template", template_message(scene), heldout_fns))
        records.extend(evaluate_message(scene, "api_direct_first", candidates[0], heldout_fns))
        records.extend(evaluate_message(scene, "api_best_of_k_shortest", shortest["message"], heldout_fns))
        records.extend(
            evaluate_message(
                scene,
                "hybrid_local_mirror_api_eval",
                mirror["message"],
                heldout_fns,
                sameplay_choices=mirror["choices"],
            )
        )
        records.extend(
            evaluate_message(
                scene,
                "hybrid_local_population_api_eval",
                population["message"],
                heldout_fns,
                sameplay_choices=population["choices"],
            )
        )
        records.extend(oracle_rows_from_candidate_records(candidate_eval_rows, candidates))

        candidate_rows.append(
            {
                "scene_id": scene.scene_id,
                "scenario_type": scene.scenario_type,
                "target_id": scene.target_id,
                "target": scene.target().__dict__,
                "candidates": candidates,
                "speaker_prompt": args.speaker_prompt,
                "speaker_schema_version": speaker_schema_version,
                "speaker_raw": speaker_result.text,
                "speaker_cached": speaker_result.cached,
                "speaker_usage": speaker_result.usage,
                "speaker_cache_path": speaker_result.cache_path,
                "mirror_selected": mirror["message"],
                "mirror_local_choices": [choice.__dict__ for choice in mirror["choices"]],
                "population_selected": population["message"],
                "population_local_choices": [choice.__dict__ for choice in population["choices"]],
            }
        )
        if args.checkpoint_every and scene_index % args.checkpoint_every == 0:
            write_jsonl(args.records_out, records)
            write_jsonl(args.candidates_out, candidate_rows)
            if args.all_candidate_records_out:
                write_jsonl(args.all_candidate_records_out, all_candidate_records)
            print(f"checkpoint {scene_index}/{len(scenes)} scenes", flush=True)

    write_jsonl(args.records_out, records)
    write_jsonl(args.candidates_out, candidate_rows)
    if args.all_candidate_records_out:
        write_jsonl(args.all_candidate_records_out, all_candidate_records)
    summary = summarize_records(records)
    write_summary(args.summary_out, summary)
    print(markdown_table(summary))
    print(f"wrote records={args.records_out} candidates={args.candidates_out} summary={args.summary_out}")


def parse_temperature(value: str) -> float | None:
    if value.lower() in {"none", "null", "omit"}:
        return None
    return float(value)


def parse_optional_string(value: str) -> str | None:
    if value.lower() in {"none_param", "null", "omit"}:
        return None
    return value


if __name__ == "__main__":
    main()
