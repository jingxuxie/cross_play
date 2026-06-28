#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl, read_scenes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("records")
    parser.add_argument("--scene-file", default="data/dev_scenes.jsonl")
    parser.add_argument("--out", required=True)
    parser.add_argument("--method", default=None)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    scenes = {scene.scene_id: scene for scene in read_scenes(args.scene_file)}
    rows = []
    for row in read_jsonl(args.records):
        if row["success"]:
            continue
        if args.method and row["method"] != args.method:
            continue
        scene = scenes.get(row["scene_id"])
        rows.append(
            {
                "scene_id": row["scene_id"],
                "scenario_type": row["scenario_type"],
                "method": row["method"],
                "message": row["message"],
                "target_id": row["target_id"],
                "choice_id": row["choice_id"],
                "listener": row["listener"],
                "confidence": row["confidence"],
                "reason_code": row["reason_code"],
                "auto_error_category": _auto_error_category(scene, row["message"], row["reason_code"]),
                "notes": "",
            }
        )
        if args.limit and len(rows) >= args.limit:
            break

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scene_id",
                "scenario_type",
                "method",
                "message",
                "target_id",
                "choice_id",
                "listener",
                "confidence",
                "reason_code",
                "auto_error_category",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} failures to {out}")


def _auto_error_category(scene, message: str, reason_code: str) -> str:
    msg = message.lower()
    if scene is None:
        return "unknown"
    if scene.scenario_type == "perspective_shift" and re.search(r"\bleft|right|leftmost|rightmost\b", msg):
        return "perspective_error"
    if reason_code == "ambiguous":
        return "underspecified"
    if scene.scenario_type == "relational_reference" and not re.search(r"\bleft|right|above|below|next to|beside\b", msg):
        return "underspecified"
    if not re.search(r"\brow\s+\d+|column\s+\d+\b", msg) and scene.scenario_type in {
        "perspective_shift",
        "relational_reference",
    }:
        return "underspecified"
    return "listener_misparse_or_other"


if __name__ == "__main__":
    main()
