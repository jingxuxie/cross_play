from __future__ import annotations

import random
from collections import Counter
from typing import Iterable

from .data import Scene, SceneObject

COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]
SHAPES = ["cube", "sphere", "cylinder", "cone", "pyramid"]
SIZES = ["small", "large"]
SCENARIO_TYPES = [
    "unique_attribute",
    "distractor_contrast",
    "relational_reference",
    "perspective_shift",
    "partial_observability",
]


def generate_scenes(
    counts: dict[str, int],
    split: str,
    seed: int = 0,
    start_index: int = 0,
) -> list[Scene]:
    rng = random.Random(seed)
    scenes: list[Scene] = []
    builders = {
        "unique_attribute": _unique_attribute,
        "distractor_contrast": _distractor_contrast,
        "relational_reference": _relational_reference,
        "perspective_shift": _perspective_shift,
        "partial_observability": _partial_observability,
    }
    for scenario_type, count in counts.items():
        if scenario_type not in builders:
            raise ValueError(f"unknown scenario_type {scenario_type}")
        for i in range(count):
            scene_index = start_index + len(scenes)
            scene_rng = random.Random(rng.randrange(10**12))
            scene = builders[scenario_type](scene_rng, split, scene_index)
            scenes.append(scene)
    rng.shuffle(scenes)
    return scenes


def count_by_type(scenes: Iterable[Scene]) -> dict[str, int]:
    return dict(Counter(scene.scenario_type for scene in scenes))


def _unique_attribute(rng: random.Random, split: str, idx: int) -> Scene:
    color = rng.choice(COLORS)
    shape = rng.choice(SHAPES)
    size = rng.choice(SIZES)
    target = _obj("obj_1", color, shape, size, 2, 2)
    objects = [target]
    used_attrs = {(color, shape)}
    for obj_id, pos in zip(["obj_2", "obj_3", "obj_4"], [(4, 1), (1, 4), (5, 5)]):
        c, s = _sample_attr_pair(rng, used_attrs)
        objects.append(_obj(obj_id, c, s, rng.choice(SIZES), *pos))
    rng.shuffle(objects)
    return _finalize(
        split=split,
        idx=idx,
        prefix="ua",
        scenario_type="unique_attribute",
        target_id=target.id,
        objects=objects,
        speaker_orientation="north",
        listener_orientation="north",
        gold=f"{color} {shape}",
        metadata={"diagnostic": "target has a unique color-shape pair"},
    )


def _distractor_contrast(rng: random.Random, split: str, idx: int) -> Scene:
    color = rng.choice(COLORS)
    shape = rng.choice(SHAPES)
    target_size = rng.choice(SIZES)
    distractor_size = "large" if target_size == "small" else "small"
    target = _obj("obj_1", color, shape, target_size, 2, 3)
    distractor = _obj("obj_2", color, shape, distractor_size, 4, 3)
    used_attrs = {(color, shape)}
    objects = [target, distractor]
    for obj_id, pos in zip(["obj_3", "obj_4", "obj_5"], [(1, 1), (5, 1), (3, 5)]):
        c, s = _sample_attr_pair(rng, used_attrs)
        objects.append(_obj(obj_id, c, s, rng.choice(SIZES), *pos))
    rng.shuffle(objects)
    return _finalize(
        split=split,
        idx=idx,
        prefix="dc",
        scenario_type="distractor_contrast",
        target_id=target.id,
        objects=objects,
        speaker_orientation="north",
        listener_orientation="north",
        gold=f"{target_size} {color} {shape}",
        metadata={"contrast_attribute": "size", "distractor_id": distractor.id},
    )


def _relational_reference(rng: random.Random, split: str, idx: int) -> Scene:
    color = rng.choice(["red", "green", "purple", "orange"])
    shape = rng.choice(["cube", "cylinder", "cone"])
    size = rng.choice(SIZES)
    landmark_color = rng.choice([c for c in COLORS if c != color])
    landmark_shape = rng.choice([s for s in SHAPES if s != shape])
    target = _obj("obj_1", color, shape, size, 2, 3)
    landmark = _obj("obj_2", landmark_color, landmark_shape, "large", 3, 3)
    distractor = _obj("obj_3", color, shape, size, 5, 2)
    objects = [
        target,
        landmark,
        distractor,
        _obj("obj_4", rng.choice(COLORS), rng.choice(SHAPES), rng.choice(SIZES), 1, 1),
        _obj("obj_5", rng.choice(COLORS), rng.choice(SHAPES), rng.choice(SIZES), 4, 5),
    ]
    rng.shuffle(objects)
    return _finalize(
        split=split,
        idx=idx,
        prefix="rr",
        scenario_type="relational_reference",
        target_id=target.id,
        objects=objects,
        speaker_orientation="north",
        listener_orientation="north",
        gold=f"{color} {shape} immediately left of the {landmark_color} {landmark_shape}",
        metadata={
            "relation": "left_of",
            "landmark_id": landmark.id,
            "landmark_color": landmark_color,
            "landmark_shape": landmark_shape,
            "distractor_id": distractor.id,
        },
    )


def _perspective_shift(rng: random.Random, split: str, idx: int) -> Scene:
    color = rng.choice(["red", "blue", "green", "yellow"])
    shape = rng.choice(["cube", "sphere"])
    size = rng.choice(SIZES)
    landmark_color = rng.choice([c for c in COLORS if c != color])
    landmark_shape = rng.choice([s for s in SHAPES if s != shape])
    # Speaker faces north: lower x is "left". Listener faces east: lower y is "left".
    target = _obj("obj_1", color, shape, size, 1, 4)
    distractor = _obj("obj_2", color, shape, size, 4, 1)
    landmark = _obj("obj_3", landmark_color, landmark_shape, "large", 2, 4)
    objects = [
        target,
        distractor,
        landmark,
        _obj("obj_4", rng.choice(COLORS), rng.choice(SHAPES), rng.choice(SIZES), 5, 5),
        _obj("obj_5", rng.choice(COLORS), rng.choice(SHAPES), rng.choice(SIZES), 3, 2),
    ]
    rng.shuffle(objects)
    return _finalize(
        split=split,
        idx=idx,
        prefix="ps",
        scenario_type="perspective_shift",
        target_id=target.id,
        objects=objects,
        speaker_orientation="north",
        listener_orientation="east",
        gold=f"{size} {color} {shape} at row 4, column 1",
        metadata={
            "speaker_side": "left",
            "listener_side_of_target": "right",
            "landmark_id": landmark.id,
            "landmark_color": landmark_color,
            "landmark_shape": landmark_shape,
            "distractor_id": distractor.id,
        },
    )


def _partial_observability(rng: random.Random, split: str, idx: int) -> Scene:
    color = rng.choice(["red", "blue", "green", "yellow"])
    shape = rng.choice(["cube", "sphere", "cylinder"])
    size = rng.choice(SIZES)
    private_color = rng.choice([c for c in COLORS if c != color])
    private_shape = rng.choice([s for s in SHAPES if s != shape])
    visible_color = rng.choice([c for c in COLORS if c not in {color, private_color}])
    visible_shape = rng.choice([s for s in SHAPES if s not in {shape, private_shape}])
    target = _obj("obj_1", color, shape, size, 2, 3)
    distractor = _obj("obj_2", color, shape, size, 4, 3)
    private_landmark = _obj("obj_3", private_color, private_shape, "large", 3, 3, visible_to_listener=False)
    visible_landmark = _obj("obj_4", visible_color, visible_shape, "large", 2, 4)
    objects = [
        target,
        distractor,
        private_landmark,
        visible_landmark,
        _obj("obj_5", rng.choice(COLORS), rng.choice(SHAPES), rng.choice(SIZES), 5, 5),
    ]
    rng.shuffle(objects)
    return _finalize(
        split=split,
        idx=idx,
        prefix="po",
        scenario_type="partial_observability",
        target_id=target.id,
        objects=objects,
        speaker_orientation="north",
        listener_orientation="north",
        gold=f"{size} {color} {shape} at row 3, column 2",
        metadata={
            "diagnostic": "private landmark is visible to speaker but hidden from listener",
            "private_landmark_id": private_landmark.id,
            "private_landmark_color": private_color,
            "private_landmark_shape": private_shape,
            "visible_landmark_id": visible_landmark.id,
            "visible_landmark_color": visible_color,
            "visible_landmark_shape": visible_shape,
            "distractor_id": distractor.id,
        },
    )


def _finalize(
    split: str,
    idx: int,
    prefix: str,
    scenario_type: str,
    target_id: str,
    objects: list[SceneObject],
    speaker_orientation: str,
    listener_orientation: str,
    gold: str,
    metadata: dict[str, object],
) -> Scene:
    scene_id = f"{prefix}_{idx:06d}"
    base = Scene(
        scene_id=scene_id,
        split=split,
        scenario_type=scenario_type,
        target_id=target_id,
        speaker_orientation=speaker_orientation,
        listener_orientation=listener_orientation,
        objects=objects,
        speaker_view_text="",
        listener_view_text="",
        gold_minimal_description=gold,
        metadata=metadata,
    )
    return Scene(
        **{
            **base.to_dict(),
            "objects": objects,
            "speaker_view_text": render_speaker_view(base),
            "listener_view_text": render_listener_view(base),
        }
    )


def render_speaker_view(scene: Scene) -> str:
    lines = [
        f"Scene {scene.scene_id} ({scene.scenario_type}).",
        f"You face {scene.speaker_orientation}; the listener faces {scene.listener_orientation}.",
        "Rows increase from top to bottom; columns increase from left to right.",
        "Visible objects:",
    ]
    for obj in scene.objects:
        lines.append(f"- {_object_description(obj)}")
    return "\n".join(lines)


def render_listener_view(scene: Scene) -> str:
    lines = [
        f"Scene {scene.scene_id}. You face {scene.listener_orientation}.",
        "Rows increase from top to bottom; columns increase from left to right.",
        "Candidate objects:",
    ]
    for obj in scene.listener_objects():
        lines.append(f"- {_object_description(obj)}")
    return "\n".join(lines)


def _object_description(obj: SceneObject) -> str:
    return (
        f"{obj.id}: {obj.size} {obj.color} {obj.shape} "
        f"at row {obj.y}, column {obj.x}"
    )


def _obj(
    obj_id: str,
    color: str,
    shape: str,
    size: str,
    x: int,
    y: int,
    *,
    visible_to_listener: bool = True,
) -> SceneObject:
    return SceneObject(
        id=obj_id,
        color=color,
        shape=shape,
        size=size,
        x=x,
        y=y,
        visible_to_listener=visible_to_listener,
    )


def _sample_attr_pair(rng: random.Random, used: set[tuple[str, str]]) -> tuple[str, str]:
    for _ in range(100):
        pair = (rng.choice(COLORS), rng.choice(SHAPES))
        if pair not in used:
            used.add(pair)
            return pair
    raise RuntimeError("could not sample unique attribute pair")
