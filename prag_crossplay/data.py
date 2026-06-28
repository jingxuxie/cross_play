from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class SceneObject:
    id: str
    color: str
    shape: str
    size: str
    x: int
    y: int
    visible_to_listener: bool = True


@dataclass(frozen=True)
class Scene:
    scene_id: str
    split: str
    scenario_type: str
    target_id: str
    speaker_orientation: str
    listener_orientation: str
    objects: list[SceneObject]
    speaker_view_text: str
    listener_view_text: str
    gold_minimal_description: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def target(self) -> SceneObject:
        for obj in self.objects:
            if obj.id == self.target_id:
                return obj
        raise KeyError(f"target_id {self.target_id!r} not found in {self.scene_id}")

    def listener_objects(self) -> list[SceneObject]:
        return [obj for obj in self.objects if obj.visible_to_listener]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scene":
        objects = [SceneObject(**obj) for obj in data["objects"]]
        payload = dict(data)
        payload["objects"] = objects
        return cls(**payload)


def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_scenes(path: str | Path, scenes: Iterable[Scene]) -> None:
    write_jsonl(path, (scene.to_dict() for scene in scenes))


def read_scenes(path: str | Path) -> list[Scene]:
    return [Scene.from_dict(row) for row in read_jsonl(path)]
