#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import write_jsonl, write_scenes
from prag_crossplay.local_agents import (
    candidate_messages,
    direct_message,
    heldout_listeners,
    template_message,
    training_listeners,
)
from prag_crossplay.methods import (
    evaluate_message,
    oracle_crossplay,
    select_mirror_selfplay,
    select_population_play,
    select_shortest,
)
from prag_crossplay.scenes import generate_scenes
from prag_crossplay.scoring import markdown_table, summarize_records, write_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--scene-out", default="data/dev_scenes.jsonl")
    parser.add_argument("--records-out", default="results/local_pilot_records.jsonl")
    parser.add_argument("--summary-out", default="results/local_pilot_summary.json")
    parser.add_argument("--markdown-out", default="results/local_pilot_summary.md")
    parser.add_argument("--unique", type=int, default=10)
    parser.add_argument("--contrast", type=int, default=15)
    parser.add_argument("--relational", type=int, default=15)
    parser.add_argument("--perspective", type=int, default=10)
    parser.add_argument("--partial", type=int, default=0)
    args = parser.parse_args()

    scenes = generate_scenes(
        {
            "unique_attribute": args.unique,
            "distractor_contrast": args.contrast,
            "relational_reference": args.relational,
            "perspective_shift": args.perspective,
            "partial_observability": args.partial,
        },
        split="dev",
        seed=args.seed,
    )
    write_scenes(args.scene_out, scenes)

    train = training_listeners()
    heldout = heldout_listeners()
    heldout_fns = [listener.choose for listener in heldout]
    records = []
    for scene in scenes:
        candidates = candidate_messages(scene, k=args.k)
        records.extend(evaluate_message(scene, "template", template_message(scene), heldout_fns))
        records.extend(evaluate_message(scene, "direct", direct_message(scene), heldout_fns))
        best = select_shortest(candidates)
        records.extend(evaluate_message(scene, "best_of_k_shortest", best["message"], heldout_fns))
        mirror = select_mirror_selfplay(scene, candidates, train[0].choose)
        records.extend(
            evaluate_message(
                scene,
                "mirror_selfplay",
                mirror["message"],
                heldout_fns,
                sameplay_choices=mirror["choices"],
            )
        )
        pop = select_population_play(scene, candidates, [listener.choose for listener in train])
        records.extend(
            evaluate_message(
                scene,
                "population_play",
                pop["message"],
                heldout_fns,
                sameplay_choices=pop["choices"],
            )
        )
        records.extend(oracle_crossplay(scene, candidates, heldout_fns))

    write_jsonl(args.records_out, records)
    summary = summarize_records(records)
    write_summary(args.summary_out, summary)
    Path(args.markdown_out).write_text(markdown_table(summary), encoding="utf-8")
    print(Path(args.markdown_out).read_text(encoding="utf-8"))
    print(f"wrote scenes={args.scene_out} records={args.records_out} summary={args.summary_out}")


if __name__ == "__main__":
    main()
