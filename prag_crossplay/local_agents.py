from __future__ import annotations

import re
from dataclasses import dataclass

from .data import Scene, SceneObject
from .scenes import COLORS, SHAPES, SIZES


@dataclass(frozen=True)
class Choice:
    listener: str
    choice_id: str
    confidence: float
    ambiguity: bool
    reason_code: str
    raw_response: str = ""


class HeuristicListener:
    def __init__(
        self,
        name: str,
        frame: str = "listener",
        tie_break: str = "first",
        relation_weight: int = 8,
        coordinate_weight: int = 12,
    ) -> None:
        self.name = name
        self.frame = frame
        self.tie_break = tie_break
        self.relation_weight = relation_weight
        self.coordinate_weight = coordinate_weight

    def choose(self, scene: Scene, utterance: str) -> Choice:
        objects = scene.listener_objects()
        scores = {obj.id: 0 for obj in objects}
        utterance_l = utterance.lower()
        attrs = _mentioned_attrs(utterance_l)
        reason = "attribute" if attrs else "other"

        for obj in objects:
            for attr_type, values in attrs.items():
                obj_value = getattr(obj, attr_type)
                if obj_value in values:
                    scores[obj.id] += 2
                else:
                    scores[obj.id] -= 2

        coord = _parse_coordinate(utterance_l)
        if coord is not None:
            reason = "position"
            row, col = coord
            for obj in objects:
                scores[obj.id] += self.coordinate_weight if (obj.y, obj.x) == (row, col) else -3

        rel = _parse_relation(utterance_l)
        if rel is not None:
            term, landmark_phrase = rel
            landmark = _find_landmark(objects, landmark_phrase)
            if landmark is not None:
                reason = "relation"
                frame_orientation = _frame_orientation(scene, self.frame)
                dx, dy = _direction_vector(term, frame_orientation)
                wanted = (landmark.x + dx, landmark.y + dy)
                for obj in objects:
                    scores[obj.id] += self.relation_weight if (obj.x, obj.y) == wanted else -2

        side = _parse_side(utterance_l)
        if side is not None and rel is None:
            reason = "position"
            frame_orientation = _frame_orientation(scene, self.frame)
            candidates = _objects_matching_attrs(objects, attrs) or objects
            side_ids = _extreme_side_ids(candidates, side, frame_orientation)
            for obj in objects:
                if obj.id in side_ids:
                    scores[obj.id] += 7

        max_score = max(scores.values()) if scores else 0
        tied = [obj for obj in objects if scores[obj.id] == max_score]
        ambiguity = len(tied) > 1
        chosen = _break_tie(tied, self.tie_break)
        confidence = 0.9 if max_score > 0 and not ambiguity else 0.38 if max_score > 0 else 0.2
        if ambiguity:
            reason = "ambiguous" if reason == "attribute" else reason
        return Choice(
            listener=self.name,
            choice_id=chosen.id,
            confidence=confidence,
            ambiguity=ambiguity,
            reason_code=reason,
            raw_response=f"scores={scores}",
        )


def training_listeners() -> list[HeuristicListener]:
    return [
        HeuristicListener("L_train_mirror_speaker_frame", frame="speaker", tie_break="first"),
        HeuristicListener("L_train_strict_map", frame="listener", tie_break="high_id"),
        HeuristicListener("L_train_relation", frame="listener", tie_break="low_id", relation_weight=11),
    ]


def heldout_listeners() -> list[HeuristicListener]:
    return [
        HeuristicListener("L_test_listener_frame", frame="listener", tie_break="high_id"),
        HeuristicListener("L_test_direct_map", frame="listener", tie_break="low_id"),
        HeuristicListener("L_test_relation_strict", frame="listener", tie_break="last", relation_weight=10),
    ]


def template_message(scene: Scene) -> str:
    target = scene.target()
    return (
        f"Select the {target.size} {target.color} {target.shape} "
        f"at row {target.y}, column {target.x}."
    )


def direct_message(scene: Scene) -> str:
    target = scene.target()
    if scene.scenario_type == "unique_attribute":
        return f"Select the {target.color} {target.shape}."
    if scene.scenario_type == "distractor_contrast":
        return f"Select the {target.color} {target.shape}."
    if scene.scenario_type == "relational_reference":
        landmark = _scene_obj(scene, str(scene.metadata["landmark_id"]))
        return (
            f"Select the {target.color} {target.shape} immediately left of "
            f"the {landmark.color} {landmark.shape}."
        )
    if scene.scenario_type == "perspective_shift":
        return f"Select the {target.color} {target.shape} on the {scene.metadata['speaker_side']}."
    if scene.scenario_type == "partial_observability":
        landmark = _scene_obj(scene, str(scene.metadata["private_landmark_id"]))
        return (
            f"Select the {target.color} {target.shape} left of the "
            f"{landmark.color} {landmark.shape}."
        )
    return template_message(scene)


def candidate_messages(scene: Scene, k: int = 4) -> list[str]:
    target = scene.target()
    messages: list[str] = []
    if scene.scenario_type == "unique_attribute":
        messages = [
            f"Select the {target.color} {target.shape}.",
            f"Select the {target.size} {target.color} {target.shape}.",
            template_message(scene),
            f"Choose the only {target.color} {target.shape} in the scene.",
            f"Choose the unique {target.size} {target.color} {target.shape}.",
            f"Pick the {target.color} {target.shape} that has no matching distractor.",
            f"Select the target object with {target.color} color and {target.shape} shape.",
            f"Choose the visible {target.size} {target.color} object.",
        ]
    elif scene.scenario_type == "distractor_contrast":
        messages = [
            f"Select the {target.color} {target.shape}.",
            f"Select the {target.size} {target.color} {target.shape}.",
            template_message(scene),
            f"Choose the {target.size} one among the {target.color} {target.shape}s.",
            f"Choose the {target.size} {target.shape} among the matching {target.color} objects.",
            f"Select the {target.size} object from the pair of {target.color} {target.shape}s.",
            f"Pick the {target.size} {target.color} one, not the other {target.color} {target.shape}.",
            f"Select the {target.size} member of the repeated {target.color} {target.shape} pair.",
        ]
    elif scene.scenario_type == "relational_reference":
        landmark = _scene_obj(scene, str(scene.metadata["landmark_id"]))
        messages = [
            f"Select the {target.color} {target.shape}.",
            (
                f"Select the {target.color} {target.shape} immediately left of "
                f"the {landmark.color} {landmark.shape}."
            ),
            template_message(scene),
            (
                f"Choose the {target.size} {target.color} {target.shape} next to "
                f"the {landmark.color} {landmark.shape}."
            ),
            (
                f"Select the {target.size} {target.color} {target.shape} immediately left of "
                f"the {landmark.color} {landmark.shape}."
            ),
            f"Select the object immediately left of the {landmark.color} {landmark.shape}.",
            (
                f"Pick the {target.color} {target.shape} left of the large "
                f"{landmark.color} {landmark.shape}."
            ),
            (
                f"Choose the {target.size} object left of the "
                f"{landmark.color} {landmark.shape} landmark."
            ),
        ]
    elif scene.scenario_type == "perspective_shift":
        landmark = _scene_obj(scene, str(scene.metadata["landmark_id"]))
        messages = [
            f"Select the {target.color} {target.shape} on the {scene.metadata['speaker_side']}.",
            template_message(scene),
            (
                f"Select the {target.color} {target.shape} beside the "
                f"{landmark.color} {landmark.shape} at row {target.y}, column {target.x}."
            ),
            f"Select the {target.color} {target.shape}.",
            (
                f"Select the {target.color} {target.shape} below of the "
                f"{landmark.color} {landmark.shape}."
            ),
            (
                f"Select the {target.size} {target.color} {target.shape} below of the "
                f"{landmark.color} {landmark.shape}."
            ),
            f"Select the object below of the {landmark.color} {landmark.shape}.",
            (
                f"Choose the {target.size} object below of the large "
                f"{landmark.color} {landmark.shape}."
            ),
        ]
    elif scene.scenario_type == "partial_observability":
        private_landmark = _scene_obj(scene, str(scene.metadata["private_landmark_id"]))
        visible_landmark = _scene_obj(scene, str(scene.metadata["visible_landmark_id"]))
        messages = [
            (
                f"Select the {target.color} {target.shape} left of the "
                f"{private_landmark.color} {private_landmark.shape}."
            ),
            f"Select the {target.size} {target.color} {target.shape}.",
            template_message(scene),
            (
                f"Select the {target.color} {target.shape} above the "
                f"{visible_landmark.color} {visible_landmark.shape}."
            ),
            (
                f"Select the {target.color} {target.shape} above of the "
                f"{visible_landmark.color} {visible_landmark.shape}."
            ),
            (
                f"Select the {target.size} {target.color} {target.shape} above of the "
                f"{visible_landmark.color} {visible_landmark.shape}."
            ),
            f"Select the object above of the {visible_landmark.color} {visible_landmark.shape}.",
            (
                f"Choose the {target.size} object above of the large "
                f"{visible_landmark.color} {visible_landmark.shape}."
            ),
        ]
    else:
        messages = [template_message(scene)]

    deduped = list(dict.fromkeys(messages))
    return (deduped + [template_message(scene)])[:k]


def _scene_obj(scene: Scene, obj_id: str) -> SceneObject:
    for obj in scene.objects:
        if obj.id == obj_id:
            return obj
    raise KeyError(obj_id)


def _mentioned_attrs(text: str) -> dict[str, set[str]]:
    return {
        "color": {x for x in COLORS if re.search(rf"\b{x}\b", text)},
        "shape": {x for x in SHAPES if re.search(rf"\b{x}s?\b", text)},
        "size": {x for x in SIZES if re.search(rf"\b{x}\b", text)},
    }


def _parse_coordinate(text: str) -> tuple[int, int] | None:
    match = re.search(r"row\s+(\d+)\D+column\s+(\d+)", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    match = re.search(r"column\s+(\d+)\D+row\s+(\d+)", text)
    if match:
        return int(match.group(2)), int(match.group(1))
    return None


def _parse_relation(text: str) -> tuple[str, str] | None:
    match = re.search(r"\b(left|right|above|below) of (?:the )?(.+?)(?:\.|,|$)", text)
    if match:
        return match.group(1), match.group(2)
    return None


def _parse_side(text: str) -> str | None:
    if re.search(r"\b(on|to|at)\s+the\s+left\b|\bleftmost\b", text):
        return "left"
    if re.search(r"\b(on|to|at)\s+the\s+right\b|\brightmost\b", text):
        return "right"
    return None


def _find_landmark(objects: list[SceneObject], phrase: str) -> SceneObject | None:
    phrase_l = phrase.lower()
    best: tuple[int, SceneObject] | None = None
    for obj in objects:
        score = int(obj.color in phrase_l) + int(obj.shape in phrase_l) + int(obj.size in phrase_l)
        if score and (best is None or score > best[0]):
            best = (score, obj)
    return best[1] if best else None


def _objects_matching_attrs(
    objects: list[SceneObject],
    attrs: dict[str, set[str]],
) -> list[SceneObject]:
    active = {k: v for k, v in attrs.items() if v}
    if not active:
        return []
    out = []
    for obj in objects:
        if all(getattr(obj, attr_type) in values for attr_type, values in active.items()):
            out.append(obj)
    return out


def _frame_orientation(scene: Scene, frame: str) -> str:
    if frame == "speaker":
        return scene.speaker_orientation
    return scene.listener_orientation


def _direction_vector(term: str, orientation: str) -> tuple[int, int]:
    # x increases east, y increases south.
    north = {"left": (-1, 0), "right": (1, 0), "above": (0, -1), "below": (0, 1)}
    east = {"left": (0, -1), "right": (0, 1), "above": (1, 0), "below": (-1, 0)}
    south = {"left": (1, 0), "right": (-1, 0), "above": (0, 1), "below": (0, -1)}
    west = {"left": (0, 1), "right": (0, -1), "above": (-1, 0), "below": (1, 0)}
    return {"north": north, "east": east, "south": south, "west": west}[orientation][term]


def _extreme_side_ids(objects: list[SceneObject], side: str, orientation: str) -> set[str]:
    vectors = {
        "north": {"left": (-1, 0), "right": (1, 0)},
        "east": {"left": (0, -1), "right": (0, 1)},
        "south": {"left": (1, 0), "right": (-1, 0)},
        "west": {"left": (0, 1), "right": (0, -1)},
    }
    dx, dy = vectors[orientation][side]
    values = {obj.id: dx * obj.x + dy * obj.y for obj in objects}
    best = max(values.values())
    return {obj_id for obj_id, value in values.items() if value == best}


def _break_tie(objects: list[SceneObject], tie_break: str) -> SceneObject:
    if tie_break == "last":
        return objects[-1]
    if tie_break == "low_id":
        return sorted(objects, key=lambda obj: obj.id)[0]
    if tie_break == "high_id":
        return sorted(objects, key=lambda obj: obj.id)[-1]
    return objects[0]
