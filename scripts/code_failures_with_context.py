#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import SceneObject, read_scenes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--failures", required=True)
    parser.add_argument("--scene-file", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--table-out", default=None)
    parser.add_argument("--tex-out", default=None)
    args = parser.parse_args()

    scenes = {scene.scene_id: scene for scene in read_scenes(args.scene_file)}
    coded = []
    with Path(args.failures).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            scene = scenes[row["scene_id"]]
            target = object_by_id(scene.objects, row["target_id"])
            choice = object_by_id(scene.objects, row["choice_id"])
            category, note = code_failure(row["message"], target, choice)
            coded.append(
                {
                    **row,
                    "author_category": category,
                    "target_description": describe(target),
                    "choice_description": describe(choice),
                    "author_note": note,
                }
            )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(coded[0]))
        writer.writeheader()
        writer.writerows(coded)

    counts = count_categories(coded)
    if args.table_out:
        Path(args.table_out).write_text(markdown_counts(counts), encoding="utf-8")
    if args.tex_out:
        Path(args.tex_out).write_text(latex_counts(counts), encoding="utf-8")
    print(f"wrote {len(coded)} coded failures to {out}: {counts}")


def code_failure(message: str, target: SceneObject, choice: SceneObject) -> tuple[str, str]:
    msg = message.lower()
    target_attrs = (target.size, target.color, target.shape)
    choice_attrs = (choice.size, choice.color, choice.shape)
    same_basic = target_attrs == choice_attrs
    uses_frame = bool(re.search(r"\bleft|right|leftmost|rightmost\b", msg))
    uses_coordinate = bool(re.search(r"\brow\s+\d+|\bcolumn\s+\d+", msg))
    if uses_frame and not uses_coordinate:
        return (
            "perspective_frame_error",
            "Frame-sensitive left/right language selects the distractor under the held-out listener perspective.",
        )
    if same_basic and not uses_coordinate:
        return (
            "underspecified_distractor",
            "The message names attributes shared by the target and distractor but omits a disambiguating coordinate or landmark.",
        )
    if not uses_coordinate:
        return (
            "underspecified_other",
            "The message omits an unambiguous coordinate and the held-out listener chooses another plausible object.",
        )
    return (
        "listener_misparse_or_other",
        "The message contains a disambiguating cue, so the failure may be listener parsing or another issue.",
    )


def object_by_id(objects: list[SceneObject], obj_id: str) -> SceneObject:
    for obj in objects:
        if obj.id == obj_id:
            return obj
    raise KeyError(obj_id)


def describe(obj: SceneObject) -> str:
    return f"{obj.id}: {obj.size} {obj.color} {obj.shape} at row {obj.y}, column {obj.x}"


def count_categories(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["author_category"]] = counts.get(row["author_category"], 0) + 1
    return dict(sorted(counts.items()))


def markdown_counts(counts: dict[str, int]) -> str:
    rows = ["| Rubric category | Count |", "|---|---:|"]
    for category, count in counts.items():
        rows.append(f"| {category} | {count} |")
    return "\n".join(rows) + "\n"


def latex_counts(counts: dict[str, int]) -> str:
    rows = ["\\begin{tabular}{lr}", "\\toprule", "Rubric category & Count \\\\", "\\midrule"]
    for category, count in counts.items():
        rows.append(f"{category.replace('_', ' ')} & {count} \\\\")
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


if __name__ == "__main__":
    main()
