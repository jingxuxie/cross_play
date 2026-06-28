from __future__ import annotations

import json

from .data import Scene


def scene_payload(scene: Scene) -> dict[str, object]:
    return {
        "scene_id": scene.scene_id,
        "scenario_type": scene.scenario_type,
        "speaker_orientation": scene.speaker_orientation,
        "listener_orientation": scene.listener_orientation,
        "objects": [
            {
                "id": obj.id,
                "color": obj.color,
                "shape": obj.shape,
                "size": obj.size,
                "row": obj.y,
                "column": obj.x,
                "visible_to_listener": obj.visible_to_listener,
            }
            for obj in scene.objects
        ],
        "speaker_view_text": scene.speaker_view_text,
        "listener_view_text": scene.listener_view_text,
    }


def speaker_prompt(scene: Scene, k: int, mode: str = "standard") -> tuple[str, str]:
    if mode == "standard":
        return standard_speaker_prompt(scene, k)
    if mode == "no_coordinates":
        return no_coordinate_speaker_prompt(scene, k)
    raise ValueError(f"unknown speaker prompt mode: {mode}")


def standard_speaker_prompt(scene: Scene, k: int) -> tuple[str, str]:
    target = scene.target()
    target_attrs = {
        "color": target.color,
        "shape": target.shape,
        "size": target.size,
        "row": target.y,
        "column": target.x,
    }
    system = (
        "You are the SPEAKER in a situated reference game. Write short natural-language "
        "messages that help a listener identify the target object. Do not mention the "
        "hidden target ID. Use only listener-visible information. First verify the target "
        "object's attributes, then describe that exact object. Return valid JSON only."
    )
    user = (
        "Scene:\n"
        f"{json.dumps(scene_payload(scene), indent=2, sort_keys=True)}\n\n"
        f"Target object ID visible only to you: {scene.target_id}\n"
        f"Target object attributes visible to you: {json.dumps(target_attrs, sort_keys=True)}\n\n"
        f"Generate exactly {k} different messages, ordered as follows:\n"
        "1. A natural first attempt without exact row/column coordinates unless there is no other option.\n"
        "2. A concise attribute-based message.\n"
        "3. A relational or spatial message using listener-visible landmarks when possible.\n"
        "4. A fully explicit fallback that may use row/column coordinates.\n"
        "Each message should be at most 25 words.\n"
        'Return exactly this JSON shape: {"utterances": ["...", "..."]}'
    )
    return system, user


def no_coordinate_speaker_prompt(scene: Scene, k: int) -> tuple[str, str]:
    target = scene.target()
    target_attrs = {
        "color": target.color,
        "shape": target.shape,
        "size": target.size,
    }
    system = (
        "You are the SPEAKER in a situated reference game. Write short natural-language "
        "messages that help a listener identify the target object. Use only listener-visible "
        "information, never mention the hidden target ID, and never use exact row or column "
        "coordinates. Return valid JSON only."
    )
    user = (
        "Scene:\n"
        f"{json.dumps(scene_payload(scene), indent=2, sort_keys=True)}\n\n"
        f"Target object ID visible only to you: {scene.target_id}\n"
        f"Target object non-coordinate attributes visible to you: {json.dumps(target_attrs, sort_keys=True)}\n\n"
        f"Generate exactly {k} different non-coordinate messages. Do not write phrases like "
        '"row 4", "column 1", "fourth row", or "first column". Do not mention object IDs.\n'
        "Use diverse strategies in this order when possible:\n"
        "1. A contrastive attribute description.\n"
        "2. A landmark-relative description using listener-visible objects.\n"
        "3. An ordinal description such as topmost, bottommost, leftmost, or rightmost.\n"
        "4. A negative contrast such as not the one near another object.\n"
        "5. A listener-frame-safe spatial description.\n"
        "6. A concise fallback without coordinates.\n"
        "7. A second relational description with a different landmark.\n"
        "8. A second contrastive or ordinal description.\n"
        "Each message should be at most 25 words.\n"
        'Return exactly this JSON shape: {"utterances": ["...", "..."]}'
    )
    return system, user


def listener_prompt(scene: Scene, utterance: str, style: str) -> tuple[str, str]:
    if style == "train_speaker_frame":
        system = (
            "You are a LISTENER accustomed to this speaker. The speaker may use left, "
            "right, left side, or right side from the speaker's own orientation. When a "
            "message uses those terms, interpret them from the speaker's frame rather "
            "than your own. If several objects still fit equally, choose the first "
            "matching object in the candidate list. Return valid JSON only."
        )
        schema = '{"choice_id": "obj_...", "confidence": 0.0, "reason_code": "attribute|relation|position|ambiguous|other"}'
    elif style == "train_listener_frame":
        system = (
            "You are a LISTENER who interprets left, right, left side, and right side "
            "from your own listener orientation. If several objects fit equally, choose "
            "the first matching object in the candidate list. Return valid JSON only."
        )
        schema = '{"choice_id": "obj_...", "confidence": 0.0, "reason_code": "attribute|relation|position|ambiguous|other"}'
    elif style in {"careful", "train_careful", "heldout_careful"}:
        system = (
            "You are a careful LISTENER in a reference game. Privately compare all "
            "candidate objects, but reveal no reasoning. If several objects fit equally, "
            "choose the first matching object in the candidate list and set ambiguity true. "
            "Return valid JSON only."
        )
        schema = '{"choice_id": "obj_...", "confidence": 0.0, "ambiguity": false}'
    elif style in {"strict", "train_strict_last", "heldout_strict_last", "heldout_direct_last"}:
        system = (
            "You are a strict instruction-following LISTENER. Choose the object best "
            "supported by the speaker message and listener-visible scene. If several "
            "objects fit equally, choose the last matching object in the candidate list, "
            "set confidence below 0.5, and use reason_code ambiguous. Return valid JSON only."
        )
        schema = '{"choice_id": "obj_...", "confidence": 0.0, "reason_code": "attribute|relation|position|ambiguous|other"}'
    elif style in {"uncertain", "train_uncertain"}:
        system = (
            "You are an ambiguity-aware LISTENER. Choose the most likely object, but use "
            "low confidence when the message under-specifies the target. If several objects "
            "fit equally, choose the first matching object in the candidate list. Return valid JSON only."
        )
        schema = '{"choice_id": "obj_...", "confidence": 0.0, "ambiguity": false}'
    else:
        system = (
            "You are the LISTENER in a reference game. Choose the object that the speaker "
            "most likely intends. Interpret left, right, left side, and right side from "
            "your own listener orientation. If several objects fit equally, choose the "
            "first matching object in the candidate list. Return valid JSON only."
        )
        schema = '{"choice_id": "obj_...", "confidence": 0.0}'
    user = (
        f"Speaker orientation: {scene.speaker_orientation}\n"
        f"Listener orientation: {scene.listener_orientation}\n\n"
        f"Listener view:\n{scene.listener_view_text}\n\n"
        f'Speaker message:\n"{utterance}"\n\n'
        "Choose one object ID from the listener view.\n"
        f"Return exactly this JSON shape: {schema}"
    )
    return system, user
