#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import write_scenes
from prag_crossplay.scenes import count_by_type, generate_scenes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/dev_scenes.jsonl")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--split", default="dev")
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
        split=args.split,
        seed=args.seed,
    )
    write_scenes(args.out, scenes)
    print(f"wrote {len(scenes)} scenes to {args.out}: {count_by_type(scenes)}")


if __name__ == "__main__":
    main()
