# PRAG-CrossPlay Protocol, Prompts, and Schemas

This appendix records the exact protocol surface used by the paper-facing
artifacts. It is generated from the implementation so prompt and schema
descriptions do not drift from the code.

## Source Files

- Scene source for prompt examples: `data/perspective_stress50_scenes.jsonl`.
- Record schema source: `results/perspective_stress50_gpt41nano_records.jsonl`.
- Candidate schema source: `results/perspective_stress50_hybrid_candidates.jsonl`.
- Prompt implementation: `prag_crossplay/prompts.py`.
- Selection implementation: `prag_crossplay/methods.py` and `prag_crossplay/local_agents.py`.

## Cached Model Versions

| Requested model | Response model | Cached responses |
|---|---|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 3107 |

## Task Protocol

Each scene is a situated reference game. The speaker receives the scene,
the hidden target object ID, and the target attributes. The listener sees
only the candidate-object list and the speaker message, then returns one
object ID from that list. Success is scored as `choice_id == target_id`.
Generated speaker messages are audited for object-ID leakage; listener
choices and success flags are checked against the source scenes by
`scripts/audit_benchmark_integrity.py`.

Implemented scenario families: `unique_attribute`, `distractor_contrast`, `relational_reference`, `perspective_shift`, `partial_observability`. The current API paper results use the first four families plus a bounded `partial_observability` support run; the same family is also included as a no-API local benchmark extension.

The speaker prompt includes the hidden target ID only so the model knows
which object to describe. The system instruction explicitly forbids
mentioning that ID, and the integrity audit checks all generated and
evaluated messages for `obj_*` leakage.

## Example Scene Payload

```json
{
  "listener_orientation": "east",
  "listener_view_text": "Scene ps_000005. You face east.\nRows increase from top to bottom; columns increase from left to right.\nCandidate objects:\n- obj_1: small green sphere at row 4, column 1\n- obj_5: large red cube at row 2, column 3\n- obj_4: large purple cylinder at row 5, column 5\n- obj_2: small green sphere at row 1, column 4\n- obj_3: large red cylinder at row 4, column 2",
  "objects": [
    {
      "color": "green",
      "column": 1,
      "id": "obj_1",
      "row": 4,
      "shape": "sphere",
      "size": "small",
      "visible_to_listener": true
    },
    {
      "color": "red",
      "column": 3,
      "id": "obj_5",
      "row": 2,
      "shape": "cube",
      "size": "large",
      "visible_to_listener": true
    },
    {
      "color": "purple",
      "column": 5,
      "id": "obj_4",
      "row": 5,
      "shape": "cylinder",
      "size": "large",
      "visible_to_listener": true
    },
    {
      "color": "green",
      "column": 4,
      "id": "obj_2",
      "row": 1,
      "shape": "sphere",
      "size": "small",
      "visible_to_listener": true
    },
    {
      "color": "red",
      "column": 2,
      "id": "obj_3",
      "row": 4,
      "shape": "cylinder",
      "size": "large",
      "visible_to_listener": true
    }
  ],
  "scenario_type": "perspective_shift",
  "scene_id": "ps_000005",
  "speaker_orientation": "north",
  "speaker_view_text": "Scene ps_000005 (perspective_shift).\nYou face north; the listener faces east.\nRows increase from top to bottom; columns increase from left to right.\nVisible objects:\n- obj_1: small green sphere at row 4, column 1\n- obj_5: large red cube at row 2, column 3\n- obj_4: large purple cylinder at row 5, column 5\n- obj_2: small green sphere at row 1, column 4\n- obj_3: large red cylinder at row 4, column 2"
}
```

## Speaker Prompt

### System

```text
You are the SPEAKER in a situated reference game. Write short natural-language messages that help a listener identify the target object. Do not mention the hidden target ID. Use only listener-visible information. First verify the target object's attributes, then describe that exact object. Return valid JSON only.
```

### User

```text
Scene:
{
  "listener_orientation": "east",
  "listener_view_text": "Scene ps_000005. You face east.\nRows increase from top to bottom; columns increase from left to right.\nCandidate objects:\n- obj_1: small green sphere at row 4, column 1\n- obj_5: large red cube at row 2, column 3\n- obj_4: large purple cylinder at row 5, column 5\n- obj_2: small green sphere at row 1, column 4\n- obj_3: large red cylinder at row 4, column 2",
  "objects": [
    {
      "color": "green",
      "column": 1,
      "id": "obj_1",
      "row": 4,
      "shape": "sphere",
      "size": "small",
      "visible_to_listener": true
    },
    {
      "color": "red",
      "column": 3,
      "id": "obj_5",
      "row": 2,
      "shape": "cube",
      "size": "large",
      "visible_to_listener": true
    },
    {
      "color": "purple",
      "column": 5,
      "id": "obj_4",
      "row": 5,
      "shape": "cylinder",
      "size": "large",
      "visible_to_listener": true
    },
    {
      "color": "green",
      "column": 4,
      "id": "obj_2",
      "row": 1,
      "shape": "sphere",
      "size": "small",
      "visible_to_listener": true
    },
    {
      "color": "red",
      "column": 2,
      "id": "obj_3",
      "row": 4,
      "shape": "cylinder",
      "size": "large",
      "visible_to_listener": true
    }
  ],
  "scenario_type": "perspective_shift",
  "scene_id": "ps_000005",
  "speaker_orientation": "north",
  "speaker_view_text": "Scene ps_000005 (perspective_shift).\nYou face north; the listener faces east.\nRows increase from top to bottom; columns increase from left to right.\nVisible objects:\n- obj_1: small green sphere at row 4, column 1\n- obj_5: large red cube at row 2, column 3\n- obj_4: large purple cylinder at row 5, column 5\n- obj_2: small green sphere at row 1, column 4\n- obj_3: large red cylinder at row 4, column 2"
}

Target object ID visible only to you: obj_1
Target object attributes visible to you: {"color": "green", "column": 1, "row": 4, "shape": "sphere", "size": "small"}

Generate exactly 4 different messages, ordered as follows:
1. A natural first attempt without exact row/column coordinates unless there is no other option.
2. A concise attribute-based message.
3. A relational or spatial message using listener-visible landmarks when possible.
4. A fully explicit fallback that may use row/column coordinates.
Each message should be at most 25 words.
Return exactly this JSON shape: {"utterances": ["...", "..."]}
```

## No-Coordinate Speaker Prompt

This K=8 prompt mode is used by the GPT-5.5 Experiment 4 no-coordinate candidate-generation audit. It forbids exact row/column references and asks for diverse listener-visible alternatives.

### System

```text
You are the SPEAKER in a situated reference game. Write short natural-language messages that help a listener identify the target object. Use only listener-visible information, never mention the hidden target ID, and never use exact row or column coordinates. Return valid JSON only.
```

### User

```text
Scene:
{
  "listener_orientation": "east",
  "listener_view_text": "Scene ps_000005. You face east.\nRows increase from top to bottom; columns increase from left to right.\nCandidate objects:\n- obj_1: small green sphere at row 4, column 1\n- obj_5: large red cube at row 2, column 3\n- obj_4: large purple cylinder at row 5, column 5\n- obj_2: small green sphere at row 1, column 4\n- obj_3: large red cylinder at row 4, column 2",
  "objects": [
    {
      "color": "green",
      "column": 1,
      "id": "obj_1",
      "row": 4,
      "shape": "sphere",
      "size": "small",
      "visible_to_listener": true
    },
    {
      "color": "red",
      "column": 3,
      "id": "obj_5",
      "row": 2,
      "shape": "cube",
      "size": "large",
      "visible_to_listener": true
    },
    {
      "color": "purple",
      "column": 5,
      "id": "obj_4",
      "row": 5,
      "shape": "cylinder",
      "size": "large",
      "visible_to_listener": true
    },
    {
      "color": "green",
      "column": 4,
      "id": "obj_2",
      "row": 1,
      "shape": "sphere",
      "size": "small",
      "visible_to_listener": true
    },
    {
      "color": "red",
      "column": 2,
      "id": "obj_3",
      "row": 4,
      "shape": "cylinder",
      "size": "large",
      "visible_to_listener": true
    }
  ],
  "scenario_type": "perspective_shift",
  "scene_id": "ps_000005",
  "speaker_orientation": "north",
  "speaker_view_text": "Scene ps_000005 (perspective_shift).\nYou face north; the listener faces east.\nRows increase from top to bottom; columns increase from left to right.\nVisible objects:\n- obj_1: small green sphere at row 4, column 1\n- obj_5: large red cube at row 2, column 3\n- obj_4: large purple cylinder at row 5, column 5\n- obj_2: small green sphere at row 1, column 4\n- obj_3: large red cylinder at row 4, column 2"
}

Target object ID visible only to you: obj_1
Target object non-coordinate attributes visible to you: {"color": "green", "shape": "sphere", "size": "small"}

Generate exactly 8 different non-coordinate messages. Do not write phrases like "row 4", "column 1", "fourth row", or "first column". Do not mention object IDs.
Use diverse strategies in this order when possible:
1. A contrastive attribute description.
2. A landmark-relative description using listener-visible objects.
3. An ordinal description such as topmost, bottommost, leftmost, or rightmost.
4. A negative contrast such as not the one near another object.
5. A listener-frame-safe spatial description.
6. A concise fallback without coordinates.
7. A second relational description with a different landmark.
8. A second contrastive or ordinal description.
Each message should be at most 25 words.
Return exactly this JSON shape: {"utterances": ["...", "..."]}
```

## Held-Out Listener Prompts

### `heldout_direct_last` System

```text
You are a strict instruction-following LISTENER. Choose the object best supported by the speaker message and listener-visible scene. If several objects fit equally, choose the last matching object in the candidate list, set confidence below 0.5, and use reason_code ambiguous. Return valid JSON only.
```

### `heldout_direct_last` User

```text
Speaker orientation: north
Listener orientation: east

Listener view:
Scene ps_000005. You face east.
Rows increase from top to bottom; columns increase from left to right.
Candidate objects:
- obj_1: small green sphere at row 4, column 1
- obj_5: large red cube at row 2, column 3
- obj_4: large purple cylinder at row 5, column 5
- obj_2: small green sphere at row 1, column 4
- obj_3: large red cylinder at row 4, column 2

Speaker message:
"It is a small green sphere."

Choose one object ID from the listener view.
Return exactly this JSON shape: {"choice_id": "obj_...", "confidence": 0.0, "reason_code": "attribute|relation|position|ambiguous|other"}
```

### `heldout_careful` System

```text
You are a careful LISTENER in a reference game. Privately compare all candidate objects, but reveal no reasoning. If several objects fit equally, choose the first matching object in the candidate list and set ambiguity true. Return valid JSON only.
```

### `heldout_careful` User

```text
Speaker orientation: north
Listener orientation: east

Listener view:
Scene ps_000005. You face east.
Rows increase from top to bottom; columns increase from left to right.
Candidate objects:
- obj_1: small green sphere at row 4, column 1
- obj_5: large red cube at row 2, column 3
- obj_4: large purple cylinder at row 5, column 5
- obj_2: small green sphere at row 1, column 4
- obj_3: large red cylinder at row 4, column 2

Speaker message:
"It is a small green sphere."

Choose one object ID from the listener view.
Return exactly this JSON shape: {"choice_id": "obj_...", "confidence": 0.0, "ambiguity": false}
```

### `heldout_strict_last` System

```text
You are a strict instruction-following LISTENER. Choose the object best supported by the speaker message and listener-visible scene. If several objects fit equally, choose the last matching object in the candidate list, set confidence below 0.5, and use reason_code ambiguous. Return valid JSON only.
```

### `heldout_strict_last` User

```text
Speaker orientation: north
Listener orientation: east

Listener view:
Scene ps_000005. You face east.
Rows increase from top to bottom; columns increase from left to right.
Candidate objects:
- obj_1: small green sphere at row 4, column 1
- obj_5: large red cube at row 2, column 3
- obj_4: large purple cylinder at row 5, column 5
- obj_2: small green sphere at row 1, column 4
- obj_3: large red cylinder at row 4, column 2

Speaker message:
"It is a small green sphere."

Choose one object ID from the listener view.
Return exactly this JSON shape: {"choice_id": "obj_...", "confidence": 0.0, "reason_code": "attribute|relation|position|ambiguous|other"}
```

## Deterministic Training Listeners

| Listener | Frame assumption | Tie-break | Relation weight |
|---|---|---|---:|
| `L_train_mirror_speaker_frame` | `speaker` | `first` | 8 |
| `L_train_strict_map` | `listener` | `high_id` | 8 |
| `L_train_relation` | `listener` | `low_id` | 11 |

## Record Schema

| Field | Type |
|---|---|
| `ambiguity` | `bool` |
| `choice_id` | `str` |
| `confidence` | `float` |
| `listener` | `str` |
| `message` | `str` |
| `message_tokens` | `int` |
| `method` | `str` |
| `raw_response` | `str` |
| `reason_code` | `str` |
| `sameplay_success` | `float | null` |
| `scenario_type` | `str` |
| `scene_id` | `str` |
| `split` | `str` |
| `success` | `int` |
| `target_id` | `str` |
| `candidate_index` | `int` |
| `oracle_candidate_index` | `int` |

## Candidate Schema

| Field | Type |
|---|---|
| `candidates` | `list` |
| `mirror_local_choices` | `list` |
| `mirror_selected` | `str` |
| `population_local_choices` | `list` |
| `population_selected` | `str` |
| `scenario_type` | `str` |
| `scene_id` | `str` |
| `speaker_cache_path` | `str` |
| `speaker_cached` | `bool` |
| `speaker_raw` | `str` |
| `speaker_usage` | `object` |
| `target` | `object` |
| `target_id` | `str` |

## Paper-Facing Integrity Checks

The current benchmark integrity report passes 290/290 checks.
It verifies source-scoped scene coverage, target IDs, listener choice IDs,
success flags, generated-message object-ID leakage, candidate selection
membership, local selector choice IDs, speaker cache paths, cache JSON
readability, and exact cached response model versions.
