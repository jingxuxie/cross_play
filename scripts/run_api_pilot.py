#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.api_client import OpenAIResponsesClient
from prag_crossplay.data import read_scenes, write_jsonl
from prag_crossplay.local_agents import Choice, template_message
from prag_crossplay.methods import (
    evaluate_message,
    oracle_crossplay,
    select_mirror_selfplay,
    select_population_play,
    select_shortest,
)
from prag_crossplay.prompts import listener_prompt, speaker_prompt
from prag_crossplay.scoring import markdown_table, summarize_records, write_summary


class ApiListener:
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
        choice_id = str(payload.get("choice_id", ""))
        valid_ids = {obj.id for obj in scene.listener_objects()}
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
    parser.add_argument("--max-scenes", type=int, default=4)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument("--records-out", default="results/api_pilot_records.jsonl")
    parser.add_argument("--summary-out", default="results/api_pilot_summary.json")
    parser.add_argument("--candidates-out", default="results/api_pilot_candidates.jsonl")
    args = parser.parse_args()

    client = OpenAIResponsesClient(
        model=args.model,
        temperature=args.temperature,
        cache_dir=args.cache_dir,
    )
    scenes = read_scenes(args.scene_file)[: args.max_scenes]
    train = [
        ApiListener(client, "L_train_speaker_frame_api", "train_speaker_frame"),
        ApiListener(client, "L_train_listener_frame_api", "train_listener_frame"),
        ApiListener(client, "L_train_strict_last_api", "train_strict_last"),
    ]
    heldout = [
        ApiListener(client, "L_test_direct_last_api", "heldout_direct_last"),
        ApiListener(client, "L_test_careful_api", "heldout_careful"),
        ApiListener(client, "L_test_strict_last_api", "heldout_strict_last"),
    ]
    heldout_fns = [listener.choose for listener in heldout]
    records: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for scene in scenes:
        system, user = speaker_prompt(scene, args.k)
        payload, speaker_result = client.call_json(
            system,
            user,
            max_output_tokens=220,
            schema_version="speaker-v2-target-attrs",
        )
        candidates = [str(x).strip() for x in payload.get("utterances", []) if str(x).strip()]
        candidates = candidates[: args.k]
        if not candidates:
            candidates = [template_message(scene)]
        candidate_rows.append(
            {
                "scene_id": scene.scene_id,
                "scenario_type": scene.scenario_type,
                "target_id": scene.target_id,
                "target": scene.target().__dict__,
                "candidates": candidates,
                "speaker_raw": speaker_result.text,
                "speaker_cached": speaker_result.cached,
                "speaker_usage": speaker_result.usage,
                "speaker_cache_path": speaker_result.cache_path,
            }
        )

        records.extend(evaluate_message(scene, "template", template_message(scene), heldout_fns))
        records.extend(evaluate_message(scene, "api_direct_first", candidates[0], heldout_fns))
        best = select_shortest(candidates)
        records.extend(evaluate_message(scene, "api_best_of_k_shortest", best["message"], heldout_fns))
        mirror = select_mirror_selfplay(scene, candidates, train[0].choose)
        candidate_rows[-1]["mirror_selected"] = mirror["message"]
        candidate_rows[-1]["mirror_train_choices"] = [choice.__dict__ for choice in mirror["choices"]]
        records.extend(
            evaluate_message(
                scene,
                "api_mirror_selfplay",
                mirror["message"],
                heldout_fns,
                sameplay_choices=mirror["choices"],
            )
        )
        pop = select_population_play(scene, candidates, [listener.choose for listener in train])
        candidate_rows[-1]["population_selected"] = pop["message"]
        candidate_rows[-1]["population_train_choices"] = [choice.__dict__ for choice in pop["choices"]]
        records.extend(
            evaluate_message(
                scene,
                "api_population_play",
                pop["message"],
                heldout_fns,
                sameplay_choices=pop["choices"],
            )
        )
        records.extend(oracle_crossplay(scene, candidates, heldout_fns))

    write_jsonl(args.candidates_out, candidate_rows)
    write_jsonl(args.records_out, records)
    summary = summarize_records(records)
    write_summary(args.summary_out, summary)
    print(markdown_table(summary))
    print(f"wrote records={args.records_out} summary={args.summary_out}")


if __name__ == "__main__":
    main()
