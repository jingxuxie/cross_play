#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import Scene, SceneObject, read_jsonl, read_scenes, write_jsonl


RUNS = {
    "perspective": {
        "scene_file": "data/perspective_stress50_scenes.jsonl",
        "records_file": "results/perspective_stress50_gpt41nano_records.jsonl",
        "method": "hybrid_local_mirror_api_eval",
    },
    "partial_observability": {
        "scene_file": "data/partial_observability_local50_scenes.jsonl",
        "records_file": "results/partial_observability_api50_records.jsonl",
        "method": "hybrid_local_mirror_api_eval",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a participant-safe 20-item human validation packet."
    )
    parser.add_argument("--items-out", default="data/human_validation_items.jsonl")
    parser.add_argument("--responses-out", default="data/human_validation_response_template.csv")
    parser.add_argument("--answer-key-out", default="results/human_validation_answer_key.json")
    parser.add_argument("--markdown-out", default="docs/human_validation_packet.md")
    parser.add_argument("--html-out", default="docs/human_validation_packet.html")
    args = parser.parse_args()

    packet = build_packet()
    write_jsonl(args.items_out, packet["participant_items"])
    write_response_template(args.responses_out, packet["participant_items"])
    write_json(args.answer_key_out, packet["answer_key"])
    write_text(args.markdown_out, render_markdown(packet, args.items_out, args.responses_out, args.answer_key_out, args.html_out))
    write_text(args.html_out, render_html(packet))
    print(render_markdown(packet, args.items_out, args.responses_out, args.answer_key_out, args.html_out))


def build_packet() -> dict[str, Any]:
    sampled = []
    sampled.extend(sample_run("perspective", "perspective_mirror_failure", want_success=False, n=10))
    sampled.extend(sample_run("partial_observability", "partial_mirror_failure", want_success=False, n=5))
    sampled.extend(sample_run("perspective", "mirror_success_control", want_success=True, n=5))

    participant_items = []
    answer_items = []
    for index, row in enumerate(sampled, start=1):
        item_id = f"HVAL_{index:03d}"
        participant_items.append(participant_item(item_id, row))
        answer_items.append(answer_item(item_id, row))

    summary = {
        "n_items": len(sampled),
        "condition_counts": dict(Counter(row["condition"] for row in sampled)),
        "source_counts": dict(Counter(row["source"] for row in sampled)),
        "participant_safe_fields": [
            "item_id",
            "message",
            "listener_orientation",
            "object_options",
        ],
        "label_fields_kept_out_of_participant_packet": [
            "condition",
            "scene_id",
            "target_id",
            "heldout_success_rate",
        ],
    }
    return {
        "summary": summary,
        "participant_items": participant_items,
        "answer_key": {
            "description": (
                "Answer key for the human validation packet. Do not distribute this file "
                "to annotators."
            ),
            "summary": summary,
            "items": answer_items,
            "analysis_plan": analysis_plan(),
        },
    }


def sample_run(source: str, condition: str, *, want_success: bool, n: int) -> list[dict[str, Any]]:
    spec = RUNS[source]
    scenes = {scene.scene_id: scene for scene in read_scenes(spec["scene_file"])}
    by_scene = records_by_scene(spec["records_file"], spec["method"])
    candidates = []
    for scene_id in sorted(by_scene):
        rows = by_scene[scene_id]
        success_rate = mean(float(row["success"]) for row in rows)
        if want_success and success_rate != 1.0:
            continue
        if not want_success and success_rate >= 1.0:
            continue
        scene = scenes[scene_id]
        message = rows[0]["message"]
        candidates.append(
            {
                "source": source,
                "condition": condition,
                "scene": scene,
                "message": message,
                "method": spec["method"],
                "records_file": spec["records_file"],
                "scene_file": spec["scene_file"],
                "heldout_rows": rows,
                "heldout_success_rate": success_rate,
            }
        )
    if len(candidates) < n:
        raise RuntimeError(f"needed {n} rows for {condition}, found {len(candidates)}")
    return candidates[:n]


def records_by_scene(path: str, method: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in read_jsonl(path):
        if row["method"] == method:
            grouped[row["scene_id"]].append(row)
    return {scene_id: sorted(rows, key=lambda row: row["listener"]) for scene_id, rows in grouped.items()}


def participant_item(item_id: str, row: dict[str, Any]) -> dict[str, Any]:
    scene: Scene = row["scene"]
    return {
        "item_id": item_id,
        "listener_orientation": scene.listener_orientation,
        "message": row["message"],
        "object_options": [object_option(obj) for obj in scene.listener_objects()],
        "questions": [
            "Which object is the message referring to?",
            "Is the message ambiguous from the listener-visible information?",
        ],
    }


def answer_item(item_id: str, row: dict[str, Any]) -> dict[str, Any]:
    scene: Scene = row["scene"]
    choices = Counter(record["choice_id"] for record in row["heldout_rows"])
    return {
        "item_id": item_id,
        "condition": row["condition"],
        "source": row["source"],
        "scene_id": scene.scene_id,
        "scenario_type": scene.scenario_type,
        "method": row["method"],
        "message": row["message"],
        "target_id": scene.target_id,
        "target_description": describe_object(scene.target()),
        "heldout_success_rate": row["heldout_success_rate"],
        "heldout_choices": dict(sorted(choices.items())),
        "records_file": row["records_file"],
        "scene_file": row["scene_file"],
    }


def object_option(obj: SceneObject) -> dict[str, Any]:
    return {
        "object_id": obj.id,
        "description": describe_object(obj),
    }


def describe_object(obj: SceneObject) -> str:
    return f"{obj.size} {obj.color} {obj.shape} at row {obj.y}, column {obj.x}"


def analysis_plan() -> list[str]:
    return [
        "Collect three independent annotations per item.",
        "Primary accuracy: fraction of annotations whose chosen_object_id matches target_id.",
        "Primary ambiguity rate: fraction of annotations marked ambiguous.",
        "Report rates by condition: perspective_mirror_failure, partial_mirror_failure, and mirror_success_control.",
        "Do not use this packet as human-validation evidence until external annotations are collected.",
    ]


def write_response_template(path: str, items: list[dict[str, Any]]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "annotator_id",
                "item_id",
                "chosen_object_id",
                "ambiguous",
                "confidence_1_to_5",
                "notes",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "annotator_id": "",
                    "item_id": item["item_id"],
                    "chosen_object_id": "",
                    "ambiguous": "",
                    "confidence_1_to_5": "",
                    "notes": "",
                }
            )


def render_markdown(
    packet: dict[str, Any],
    items_out: str,
    responses_out: str,
    answer_key_out: str,
    html_out: str,
) -> str:
    summary = packet["summary"]
    lines = [
        "# Human Validation Packet",
        "",
        "This packet prepares the 20-scene human validation proposed in `additional_experiments_gpt55_plan.md`. It contains no collected human annotations, so it is a protocol artifact rather than a validation result.",
        "",
        "## Files",
        "",
        f"- Participant-safe items: `{items_out}`",
        f"- Response template: `{responses_out}`",
        f"- Static annotation page: `{html_out}`",
        f"- Researcher-only answer key: `{answer_key_out}`",
        "",
        "## Summary",
        "",
        f"Items: {summary['n_items']}. Condition counts: {format_counts(summary['condition_counts'])}.",
        "",
        "Participant files exclude condition labels, scene IDs, target IDs, and held-out success rates. The answer key keeps those fields for analysis after annotation.",
        "",
        "## Annotation Instructions",
        "",
        "For each item, annotators see a referring message and listener-visible object options. They should choose the object the message refers to and mark whether the message is ambiguous from the visible information.",
        "",
        "Recommended collection: three independent annotations per item. Report accuracy and ambiguity rate by condition only after annotations are collected.",
        "",
        "## Item Preview",
        "",
        "| Item | Message | Options |",
        "|---|---|---|",
    ]
    for item in packet["participant_items"]:
        options = "<br>".join(
            f"{option['object_id']}: {option['description']}"
            for option in item["object_options"]
        )
        lines.append(f"| {item['item_id']} | {item['message']} | {options} |")
    return "\n".join(lines) + "\n"


def render_html(packet: dict[str, Any]) -> str:
    cards = []
    for item in packet["participant_items"]:
        options = "\n".join(
            '<label><input type="radio" name="{item_id}_choice" value="{object_id}"> '
            '<span class="object-id">{object_id}</span>: {description}</label>'.format(
                item_id=html.escape(item["item_id"]),
                object_id=html.escape(option["object_id"]),
                description=html.escape(option["description"]),
            )
            for option in item["object_options"]
        )
        cards.append(
            """<section class="item">
  <h2>{item_id}</h2>
  <p class="message">{message}</p>
  <fieldset>
    <legend>Which object is the message referring to?</legend>
    {options}
  </fieldset>
  <label class="select">Ambiguous?
    <select name="{item_id}_ambiguous">
      <option value=""></option>
      <option value="yes">yes</option>
      <option value="no">no</option>
    </select>
  </label>
  <label class="select">Confidence
    <select name="{item_id}_confidence">
      <option value=""></option>
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
      <option value="5">5</option>
    </select>
  </label>
</section>
""".format(
                item_id=html.escape(item["item_id"]),
                message=html.escape(item["message"]),
                options=options,
            )
        )
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>PRAG-CrossPlay Human Validation Packet</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; max-width: 980px; line-height: 1.45; }}
    .item {{ border: 1px solid #ccc; padding: 16px; margin: 16px 0; }}
    .message {{ font-weight: 700; }}
    label {{ display: block; margin: 8px 0; }}
    .object-id {{ font-family: monospace; }}
    .select {{ margin-top: 12px; }}
  </style>
</head>
<body>
  <h1>PRAG-CrossPlay Human Validation Packet</h1>
  <p>Choose the object referred to by each message and mark whether the message is ambiguous from the listed objects.</p>
  {cards}
</body>
</html>
""".format(cards="\n".join(cards))


def format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))


def write_json(path: str, data: dict[str, Any]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: str, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
