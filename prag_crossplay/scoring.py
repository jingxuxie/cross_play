from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

from .data import read_jsonl, write_jsonl


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {
        "overall": _summarize_group(records),
        "by_method": {},
        "by_scenario_method": {},
    }
    for method, rows in _group(records, "method").items():
        summary["by_method"][method] = _summarize_group(rows)
    for key, rows in _group(records, "scenario_type", "method").items():
        scenario, method = key.split("||")
        summary["by_scenario_method"].setdefault(scenario, {})[method] = _summarize_group(rows)
    return summary


def paired_method_comparison(
    records: list[dict[str, Any]],
    method_a: str,
    method_b: str,
    scenario_type: str | None = None,
    n_boot: int = 5000,
    seed: int = 0,
) -> dict[str, Any]:
    rows = [
        row
        for row in records
        if row["method"] in {method_a, method_b}
        and (scenario_type is None or row["scenario_type"] == scenario_type)
    ]
    scores = _scene_method_means(rows)
    scene_ids = sorted(
        scene_id
        for scene_id, by_method in scores.items()
        if method_a in by_method and method_b in by_method
    )
    diffs = [scores[scene_id][method_a] - scores[scene_id][method_b] for scene_id in scene_ids]
    if not diffs:
        return {
            "method_a": method_a,
            "method_b": method_b,
            "scenario_type": scenario_type,
            "n_pairs": 0,
            "mean_a": None,
            "mean_b": None,
            "diff_a_minus_b": None,
            "diff_ci95": None,
            "paired_bootstrap_p_two_sided": None,
        }
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        sample = [rng.choice(diffs) for _ in diffs]
        boot.append(mean(sample))
    boot.sort()
    lo = boot[int(0.025 * (len(boot) - 1))]
    hi = boot[int(0.975 * (len(boot) - 1))]
    p_le_zero = sum(1 for value in boot if value <= 0) / len(boot)
    p_ge_zero = sum(1 for value in boot if value >= 0) / len(boot)
    p_two = min(1.0, 2 * min(p_le_zero, p_ge_zero))
    mean_a = mean(scores[scene_id][method_a] for scene_id in scene_ids)
    mean_b = mean(scores[scene_id][method_b] for scene_id in scene_ids)
    return {
        "method_a": method_a,
        "method_b": method_b,
        "scenario_type": scenario_type,
        "n_pairs": len(scene_ids),
        "mean_a": mean_a,
        "mean_b": mean_b,
        "diff_a_minus_b": mean(diffs),
        "diff_ci95": (lo, hi),
        "paired_bootstrap_p_two_sided": p_two,
    }


def paired_comparison_markdown(comparisons: list[dict[str, Any]]) -> str:
    rows = [
        "| Scenario | A | B | N | Mean A | Mean B | Diff A-B | 95% CI | p_boot |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for comp in comparisons:
        scenario = comp["scenario_type"] or "overall"
        if comp["n_pairs"] == 0:
            rows.append(f"| {scenario} | {comp['method_a']} | {comp['method_b']} | 0 | - | - | - | - | - |")
            continue
        ci = comp["diff_ci95"]
        rows.append(
            "| {scenario} | {a} | {b} | {n} | {ma:.3f} | {mb:.3f} | {diff:.3f} | [{lo:.3f}, {hi:.3f}] | {p:.4f} |".format(
                scenario=scenario,
                a=comp["method_a"],
                b=comp["method_b"],
                n=comp["n_pairs"],
                ma=comp["mean_a"],
                mb=comp["mean_b"],
                diff=comp["diff_a_minus_b"],
                lo=ci[0],
                hi=ci[1],
                p=comp["paired_bootstrap_p_two_sided"],
            )
        )
    return "\n".join(rows) + "\n"


def write_summary(path: str | Path, summary: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def markdown_table(summary: dict[str, Any]) -> str:
    rows = [
        "| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for method, stats in sorted(summary["by_method"].items()):
        ci = f"[{stats['success_ci95'][0]:.3f}, {stats['success_ci95'][1]:.3f}]"
        same = _fmt(stats.get("sameplay_success"))
        gap = _fmt(stats.get("crossplay_gap"))
        rows.append(
            "| {method} | {success:.3f} | {ci} | {same} | {gap} | {tokens:.1f} | {stdev:.3f} |".format(
                method=method,
                success=stats["success"],
                ci=ci,
                same=same,
                gap=gap,
                tokens=stats["mean_tokens"],
                stdev=stats["listener_success_stdev"],
            )
        )
    return "\n".join(rows) + "\n"


def load_and_summarize(records_path: str | Path) -> dict[str, Any]:
    return summarize_records(read_jsonl(records_path))


def _summarize_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
    successes = [float(row["success"]) for row in rows]
    same_values = [
        float(row["sameplay_success"])
        for row in rows
        if row.get("sameplay_success") is not None
    ]
    listener_means = [
        mean([float(row["success"]) for row in listener_rows])
        for listener_rows in _group(rows, "listener").values()
    ]
    sameplay = mean(same_values) if same_values else None
    success = mean(successes) if successes else 0.0
    return {
        "n_records": len(rows),
        "n_scenes": len({row["scene_id"] for row in rows}),
        "success": success,
        "success_ci95": bootstrap_ci_by_scene(rows),
        "sameplay_success": sameplay,
        "crossplay_gap": (sameplay - success) if sameplay is not None else None,
        "mean_tokens": mean([float(row["message_tokens"]) for row in rows]) if rows else 0.0,
        "listener_success_stdev": pstdev(listener_means) if len(listener_means) > 1 else 0.0,
        "json_valid_rate": mean([1.0 for _ in rows]) if rows else 0.0,
    }


def _scene_method_means(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        grouped[row["scene_id"]][row["method"]].append(float(row["success"]))
    return {
        scene_id: {method: mean(values) for method, values in by_method.items()}
        for scene_id, by_method in grouped.items()
    }


def bootstrap_ci_by_scene(
    rows: list[dict[str, Any]],
    n_boot: int = 1000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    by_scene = list(_group(rows, "scene_id").values())
    if not by_scene:
        return (0.0, 0.0)
    rng = random.Random(seed)
    means = []
    for _ in range(n_boot):
        sample_rows = []
        for _ in by_scene:
            sample_rows.extend(rng.choice(by_scene))
        means.append(mean(float(row["success"]) for row in sample_rows))
    means.sort()
    lo = means[int((alpha / 2) * (len(means) - 1))]
    hi = means[int((1 - alpha / 2) * (len(means) - 1))]
    return (lo, hi)


def _group(rows: list[dict[str, Any]], *keys: str) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out["||".join(str(row[key]) for key in keys)].append(row)
    return dict(out)


def _fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


def copy_records(src: str | Path, dst: str | Path) -> None:
    write_jsonl(dst, read_jsonl(src))
