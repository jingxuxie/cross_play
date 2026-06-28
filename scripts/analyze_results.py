#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.scoring import load_and_summarize, markdown_table, write_summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("records")
    parser.add_argument("--summary-out", default=None)
    parser.add_argument("--markdown-out", default=None)
    args = parser.parse_args()
    summary = load_and_summarize(args.records)
    print(markdown_table(summary))
    if args.summary_out:
        write_summary(args.summary_out, summary)
    if args.markdown_out:
        Path(args.markdown_out).write_text(markdown_table(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
