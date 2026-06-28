#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl, read_scenes
from prag_crossplay.local_agents import training_listeners
from prag_crossplay.prompts import listener_prompt, scene_payload, speaker_prompt
from prag_crossplay.scenes import SCENARIO_TYPES


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene-file", default="data/perspective_stress50_scenes.jsonl")
    parser.add_argument("--records", default="results/perspective_stress50_gpt41nano_records.jsonl")
    parser.add_argument("--candidates", default="results/perspective_stress50_hybrid_candidates.jsonl")
    parser.add_argument("--integrity", default="results/benchmark_integrity_audit.json")
    parser.add_argument("--out", default="docs/protocol_and_prompts.md")
    args = parser.parse_args()

    scenes = read_scenes(args.scene_file)
    if not scenes:
        raise SystemExit(f"no scenes in {args.scene_file}")
    scene = scenes[0]
    records = read_jsonl(args.records)
    candidates = read_jsonl(args.candidates)
    integrity = json.loads(Path(args.integrity).read_text(encoding="utf-8"))

    speaker_system, speaker_user = speaker_prompt(scene, k=4)
    listener_sections = OrderedDict(
        [
            ("heldout_direct_last", listener_prompt(scene, "It is a small green sphere.", "heldout_direct_last")),
            ("heldout_careful", listener_prompt(scene, "It is a small green sphere.", "heldout_careful")),
            ("heldout_strict_last", listener_prompt(scene, "It is a small green sphere.", "heldout_strict_last")),
        ]
    )

    text = render_appendix(
        scene_file=args.scene_file,
        records_file=args.records,
        candidates_file=args.candidates,
        scene=scene,
        speaker_system=speaker_system,
        speaker_user=speaker_user,
        listener_sections=listener_sections,
        record_schema=infer_schema(records),
        candidate_schema=infer_schema(candidates),
        integrity=integrity,
    )

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"wrote {args.out}")


def render_appendix(
    *,
    scene_file: str,
    records_file: str,
    candidates_file: str,
    scene: Any,
    speaker_system: str,
    speaker_user: str,
    listener_sections: OrderedDict[str, tuple[str, str]],
    record_schema: dict[str, str],
    candidate_schema: dict[str, str],
    integrity: dict[str, Any],
) -> str:
    model_rows = integrity.get("summary", {}).get("cache", {}).get("model_versions", [])
    lines = [
        "# PRAG-CrossPlay Protocol, Prompts, and Schemas",
        "",
        "This appendix records the exact protocol surface used by the paper-facing",
        "artifacts. It is generated from the implementation so prompt and schema",
        "descriptions do not drift from the code.",
        "",
        "## Source Files",
        "",
        f"- Scene source for prompt examples: `{scene_file}`.",
        f"- Record schema source: `{records_file}`.",
        f"- Candidate schema source: `{candidates_file}`.",
        "- Prompt implementation: `prag_crossplay/prompts.py`.",
        "- Selection implementation: `prag_crossplay/methods.py` and `prag_crossplay/local_agents.py`.",
        "",
        "## Cached Model Versions",
        "",
        "| Requested model | Response model | Cached responses |",
        "|---|---|---:|",
    ]
    for row in model_rows:
        lines.append(f"| `{row['requested_model']}` | `{row['response_model']}` | {row['n']} |")

    lines.extend(
        [
            "",
            "## Task Protocol",
            "",
            "Each scene is a situated reference game. The speaker receives the scene,",
            "the hidden target object ID, and the target attributes. The listener sees",
            "only the candidate-object list and the speaker message, then returns one",
            "object ID from that list. Success is scored as `choice_id == target_id`.",
            "Generated speaker messages are audited for object-ID leakage; listener",
            "choices and success flags are checked against the source scenes by",
            "`scripts/audit_benchmark_integrity.py`.",
            "",
            "Implemented scenario families: "
            + ", ".join(f"`{scenario}`" for scenario in SCENARIO_TYPES)
            + ". The current API paper results use the first four families plus "
            "a bounded `partial_observability` support run; the same family is "
            "also included as a no-API local benchmark extension.",
            "",
            "The speaker prompt includes the hidden target ID only so the model knows",
            "which object to describe. The system instruction explicitly forbids",
            "mentioning that ID, and the integrity audit checks all generated and",
            "evaluated messages for `obj_*` leakage.",
            "",
            "## Example Scene Payload",
            "",
            "```json",
            json.dumps(scene_payload(scene), indent=2, sort_keys=True),
            "```",
            "",
            "## Speaker Prompt",
            "",
            "### System",
            "",
            "```text",
            speaker_system,
            "```",
            "",
            "### User",
            "",
            "```text",
            speaker_user,
            "```",
            "",
            "## Held-Out Listener Prompts",
            "",
        ]
    )
    for name, (system, user) in listener_sections.items():
        lines.extend(
            [
                f"### `{name}` System",
                "",
                "```text",
                system,
                "```",
                "",
                f"### `{name}` User",
                "",
                "```text",
                user,
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Deterministic Training Listeners",
            "",
            "| Listener | Frame assumption | Tie-break | Relation weight |",
            "|---|---|---|---:|",
        ]
    )
    for listener in training_listeners():
        lines.append(
            f"| `{listener.name}` | `{listener.frame}` | `{listener.tie_break}` | {listener.relation_weight} |"
        )

    lines.extend(
        [
            "",
            "## Record Schema",
            "",
            schema_table(record_schema),
            "",
            "## Candidate Schema",
            "",
            schema_table(candidate_schema),
            "",
            "## Paper-Facing Integrity Checks",
            "",
            f"The current benchmark integrity report passes {integrity.get('n_checks', 0) - integrity.get('n_failed', 0)}/{integrity.get('n_checks', 0)} checks.",
            "It verifies source-scoped scene coverage, target IDs, listener choice IDs,",
            "success flags, generated-message object-ID leakage, candidate selection",
            "membership, local selector choice IDs, speaker cache paths, cache JSON",
            "readability, and exact cached response model versions.",
            "",
        ]
    )
    return "\n".join(lines)


def infer_schema(rows: list[dict[str, Any]]) -> dict[str, str]:
    field_types: dict[str, set[str]] = defaultdict(set)
    field_order: list[str] = []
    for row in rows:
        for key, value in row.items():
            if key not in field_types:
                field_order.append(key)
            field_types[key].add(type_name(value))
    return OrderedDict((key, " | ".join(sorted(field_types[key]))) for key in field_order)


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def schema_table(schema: dict[str, str]) -> str:
    lines = ["| Field | Type |", "|---|---|"]
    for key, value_type in schema.items():
        lines.append(f"| `{key}` | `{value_type}` |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
