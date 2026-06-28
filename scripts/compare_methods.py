#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl
from prag_crossplay.scenes import SCENARIO_TYPES
from prag_crossplay.scoring import paired_comparison_markdown, paired_method_comparison


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("records")
    parser.add_argument("--method-a", required=True)
    parser.add_argument("--method-b", required=True)
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--markdown-out", default=None)
    args = parser.parse_args()

    records = read_jsonl(args.records)
    comparisons = [
        paired_method_comparison(records, args.method_a, args.method_b, scenario_type=None)
    ]
    for scenario_type in SCENARIO_TYPES:
        comparisons.append(
            paired_method_comparison(
                records,
                args.method_a,
                args.method_b,
                scenario_type=scenario_type,
            )
        )
    md = paired_comparison_markdown(comparisons)
    print(md)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps(comparisons, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_out:
        Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.markdown_out).write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
