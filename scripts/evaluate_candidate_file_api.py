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
from prag_crossplay.local_agents import Choice, template_message, training_listeners
from prag_crossplay.methods import (
    evaluate_candidates,
    evaluate_message,
    oracle_rows_from_candidate_records,
    select_mirror_selfplay,
    select_population_play,
    select_shortest,
)
from prag_crossplay.prompts import listener_prompt
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
    parser.add_argument("--scene-file", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument("--records-out", required=True)
    parser.add_argument("--summary-out", required=True)
    parser.add_argument("--all-candidate-records-out", default=None)
    parser.add_argument("--audit-out", default=None)
    parser.add_argument("--max-scenes", type=int, default=0)
    parser.add_argument("--checkpoint-every", type=int, default=1)
    args = parser.parse_args()

    scenes = {scene.scene_id: scene for scene in read_scenes(args.scene_file)}
    candidate_rows = [
        json.loads(line)
        for line in Path(args.candidates).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if args.max_scenes > 0:
        candidate_rows = candidate_rows[: args.max_scenes]

    client = OpenAIResponsesClient(model=args.model, cache_dir=args.cache_dir)
    heldout = [
        ApiHeldoutListener(client, f"{args.model}:direct_last", "heldout_direct_last"),
        ApiHeldoutListener(client, f"{args.model}:careful", "heldout_careful"),
        ApiHeldoutListener(client, f"{args.model}:strict_last", "heldout_strict_last"),
    ]
    heldout_fns = [listener.choose for listener in heldout]
    train = training_listeners()

    records: list[dict[str, Any]] = []
    all_candidate_records: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    for index, candidate_row in enumerate(candidate_rows, start=1):
        scene = scenes[candidate_row["scene_id"]]
        candidates = [str(message) for message in candidate_row["candidates"]]
        mirror = select_mirror_selfplay(scene, candidates, train[0].choose)
        population = select_population_play(scene, candidates, [listener.choose for listener in train])
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

        audit_rows.append(
            {
                "scene_id": scene.scene_id,
                "scenario_type": scene.scenario_type,
                "target_id": scene.target_id,
                "target": scene.target().__dict__,
                "source_candidate_file": args.candidates,
                "heldout_model": args.model,
                "candidates": candidates,
                "mirror_selected": mirror["message"],
                "mirror_local_choices": [choice.__dict__ for choice in mirror["choices"]],
                "population_selected": population["message"],
                "population_local_choices": [choice.__dict__ for choice in population["choices"]],
            }
        )

        if args.checkpoint_every and index % args.checkpoint_every == 0:
            write_outputs(args, records, all_candidate_records, audit_rows, summary=False)
            print(f"checkpoint {index}/{len(candidate_rows)} scenes", flush=True)

    write_outputs(args, records, all_candidate_records, audit_rows, summary=True)
    print(markdown_table(summarize_records(records)))
    print(f"wrote records={args.records_out} summary={args.summary_out}")


def write_outputs(
    args: argparse.Namespace,
    records: list[dict[str, Any]],
    all_candidate_records: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    summary: bool,
) -> None:
    write_jsonl(args.records_out, records)
    if args.all_candidate_records_out:
        write_jsonl(args.all_candidate_records_out, all_candidate_records)
    if args.audit_out:
        write_jsonl(args.audit_out, audit_rows)
    if summary:
        write_summary(args.summary_out, summarize_records(records))


if __name__ == "__main__":
    main()
