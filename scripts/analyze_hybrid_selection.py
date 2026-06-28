#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.api_client import OpenAIResponsesClient
from prag_crossplay.data import read_scenes, write_jsonl
from prag_crossplay.local_agents import Choice, training_listeners
from prag_crossplay.methods import evaluate_message, select_mirror_selfplay, select_population_play
from prag_crossplay.prompts import listener_prompt
from prag_crossplay.scoring import markdown_table, summarize_records, write_summary


class CachedApiListener:
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
    parser.add_argument("--candidates", default="results/api_pilot6_frame_candidates.jsonl")
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument("--records-out", default="results/hybrid_pilot6_records.jsonl")
    parser.add_argument("--summary-out", default="results/hybrid_pilot6_summary.json")
    args = parser.parse_args()

    scenes = {scene.scene_id: scene for scene in read_scenes(args.scene_file)}
    candidate_rows = [json.loads(line) for line in Path(args.candidates).read_text().splitlines() if line.strip()]
    train = training_listeners()
    client = OpenAIResponsesClient(model=args.model, cache_dir=args.cache_dir)
    heldout = [
        CachedApiListener(client, "L_test_direct_last_api", "heldout_direct_last"),
        CachedApiListener(client, "L_test_careful_api", "heldout_careful"),
        CachedApiListener(client, "L_test_strict_last_api", "heldout_strict_last"),
    ]
    heldout_fns = [listener.choose for listener in heldout]

    records: list[dict[str, Any]] = []
    audit_rows = []
    for row in candidate_rows:
        scene = scenes[row["scene_id"]]
        candidates = list(row["candidates"])
        mirror = select_mirror_selfplay(scene, candidates, train[0].choose)
        population = select_population_play(scene, candidates, [listener.choose for listener in train])
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
        audit_rows.append(
            {
                "scene_id": scene.scene_id,
                "scenario_type": scene.scenario_type,
                "target_id": scene.target_id,
                "candidates": candidates,
                "mirror_selected": mirror["message"],
                "mirror_local_choices": [choice.__dict__ for choice in mirror["choices"]],
                "population_selected": population["message"],
                "population_local_choices": [choice.__dict__ for choice in population["choices"]],
            }
        )

    write_jsonl(args.records_out, records)
    audit_out = str(Path(args.records_out).with_name(Path(args.records_out).stem + "_audit.jsonl"))
    write_jsonl(audit_out, audit_rows)
    summary = summarize_records(records)
    write_summary(args.summary_out, summary)
    print(markdown_table(summary))
    print(f"wrote records={args.records_out} audit={audit_out} summary={args.summary_out}")


if __name__ == "__main__":
    main()
