from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .data import Scene
from .local_agents import Choice

ListenerFn = Callable[[Scene, str], Choice]


def token_count(text: str) -> int:
    return len(text.split())


def score_choice(choice: Choice, target_id: str) -> int:
    return int(choice.choice_id == target_id)


def select_shortest(candidates: list[str]) -> dict[str, Any]:
    message = min(candidates, key=lambda msg: (token_count(msg), msg))
    return {"message": message, "score": None, "details": []}


def select_mirror_selfplay(
    scene: Scene,
    candidates: list[str],
    listener: ListenerFn,
    length_penalty: float = 0.001,
) -> dict[str, Any]:
    scored = []
    for message in candidates:
        choice = listener(scene, message)
        success = score_choice(choice, scene.target_id)
        score = success - length_penalty * token_count(message)
        scored.append({"message": message, "score": score, "choices": [choice]})
    return max(scored, key=lambda row: row["score"])


def select_population_play(
    scene: Scene,
    candidates: list[str],
    listeners: list[ListenerFn],
    length_penalty: float = 0.001,
) -> dict[str, Any]:
    scored = []
    for message in candidates:
        choices = [listener(scene, message) for listener in listeners]
        mean_success = sum(score_choice(choice, scene.target_id) for choice in choices) / len(choices)
        score = mean_success - length_penalty * token_count(message)
        scored.append({"message": message, "score": score, "choices": choices})
    return max(scored, key=lambda row: row["score"])


def evaluate_message(
    scene: Scene,
    method: str,
    message: str,
    listeners: list[ListenerFn],
    sameplay_choices: list[Choice] | None = None,
) -> list[dict[str, Any]]:
    records = []
    sameplay_success = None
    if sameplay_choices is not None:
        sameplay_success = sum(
            int(choice.choice_id == scene.target_id) for choice in sameplay_choices
        ) / len(sameplay_choices)

    for listener in listeners:
        choice = listener(scene, message)
        records.append(
            {
                "scene_id": scene.scene_id,
                "split": scene.split,
                "scenario_type": scene.scenario_type,
                "method": method,
                "message": message,
                "message_tokens": token_count(message),
                "target_id": scene.target_id,
                "listener": choice.listener,
                "choice_id": choice.choice_id,
                "success": int(choice.choice_id == scene.target_id),
                "confidence": choice.confidence,
                "ambiguity": choice.ambiguity,
                "reason_code": choice.reason_code,
                "sameplay_success": sameplay_success,
                "raw_response": choice.raw_response,
            }
        )
    return records


def evaluate_candidates(
    scene: Scene,
    candidates: list[str],
    listeners: list[ListenerFn],
    method: str = "all_candidate",
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for candidate_index, message in enumerate(candidates):
        rows = evaluate_message(scene, method, message, listeners)
        for row in rows:
            row["candidate_index"] = candidate_index
        records.extend(rows)
    return records


def oracle_rows_from_candidate_records(
    candidate_records: list[dict[str, Any]],
    candidates: list[str],
) -> list[dict[str, Any]]:
    by_index: dict[int, list[dict[str, Any]]] = {}
    for row in candidate_records:
        by_index.setdefault(int(row["candidate_index"]), []).append(row)
    best_index = max(
        by_index,
        key=lambda idx: (
            sum(float(row["success"]) for row in by_index[idx]) / len(by_index[idx]),
            -token_count(candidates[idx]),
        ),
    )
    oracle_rows = []
    for row in by_index[best_index]:
        copied = dict(row)
        copied["method"] = "oracle_upper_bound"
        copied["oracle_candidate_index"] = best_index
        oracle_rows.append(copied)
    return oracle_rows


def oracle_crossplay(
    scene: Scene,
    candidates: list[str],
    listeners: list[ListenerFn],
) -> list[dict[str, Any]]:
    candidate_rows = []
    for message in candidates:
        rows = evaluate_message(scene, "oracle_candidate", message, listeners)
        mean_success = sum(row["success"] for row in rows) / len(rows)
        candidate_rows.append((mean_success, -token_count(message), message, rows))
    _, _, best_message, best_rows = max(candidate_rows)
    for row in best_rows:
        row["method"] = "oracle_upper_bound"
        row["message"] = best_message
    return best_rows
