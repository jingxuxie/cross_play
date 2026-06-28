#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


LENGTH_PENALTY = 0.001


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Cache-only leave-one-listener-out analysis over all-candidate API "
            "evaluations. No API calls are made."
        )
    )
    parser.add_argument(
        "--records",
        action="append",
        required=True,
        help="Dataset spec in the form label=path/to/all_candidate_records.jsonl.",
    )
    parser.add_argument("--markdown-out", required=True)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--tex-out", default=None)
    args = parser.parse_args()

    datasets = [parse_spec(spec) for spec in args.records]
    report = {"datasets": []}
    for label, path in datasets:
        rows = read_jsonl(path)
        report["datasets"].append(analyze_dataset(label, path, rows))

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(markdown_report(report), encoding="utf-8")
    if args.tex_out:
        Path(args.tex_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.tex_out).write_text(tex_table(report), encoding="utf-8")
    print(markdown_report(report))


def parse_spec(spec: str) -> tuple[str, str]:
    if "=" not in spec:
        raise SystemExit(f"--records must have form label=path, got {spec!r}")
    label, path = spec.split("=", 1)
    if not label or not path:
        raise SystemExit(f"--records must have form label=path, got {spec!r}")
    return label, path


def analyze_dataset(label: str, path: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_scene: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_scene[str(row["scene_id"])].append(row)

    method_rows: list[dict[str, Any]] = []
    paired_units: list[dict[str, Any]] = []
    for scene_id, scene_rows in sorted(by_scene.items()):
        listeners = sorted({str(row["listener"]) for row in scene_rows})
        candidates = candidate_table(scene_rows)
        if len(listeners) < 3:
            raise SystemExit(f"{path}: expected at least 3 listeners for {scene_id}, got {listeners}")

        for eval_listener in listeners:
            direct_index = 0
            shortest_index = min(candidates, key=lambda idx: (candidates[idx]["tokens"], idx))
            oracle_index = select_by_listener(candidates, [eval_listener])

            method_rows.append(record(label, scene_id, eval_listener, "loo_api_direct_first", direct_index, candidates))
            method_rows.append(record(label, scene_id, eval_listener, "loo_api_shortest", shortest_index, candidates))
            method_rows.append(record(label, scene_id, eval_listener, "loo_api_oracle", oracle_index, candidates))

            train_listeners = [listener for listener in listeners if listener != eval_listener]
            pop_index = select_by_listener(candidates, train_listeners)
            pop_row = record(
                label,
                scene_id,
                eval_listener,
                "loo_api_population",
                pop_index,
                candidates,
                train_listeners=train_listeners,
            )
            method_rows.append(pop_row)

            mirror_successes = []
            mirror_indices = []
            for train_listener in train_listeners:
                mirror_index = select_by_listener(candidates, [train_listener])
                mirror_row = record(
                    label,
                    scene_id,
                    eval_listener,
                    "loo_api_mirror",
                    mirror_index,
                    candidates,
                    train_listeners=[train_listener],
                )
                method_rows.append(mirror_row)
                mirror_successes.append(mirror_row["success"])
                mirror_indices.append(mirror_index)

            paired_units.append(
                {
                    "dataset": label,
                    "scene_id": scene_id,
                    "eval_listener": eval_listener,
                    "population_success": pop_row["success"],
                    "mirror_success": mean(mirror_successes),
                    "population_candidate_index": pop_index,
                    "mirror_candidate_indices": mirror_indices,
                }
            )

    summary = summarize(method_rows)
    paired = paired_population_minus_mirror(paired_units)
    return {
        "label": label,
        "source": path,
        "n_scenes": len(by_scene),
        "listeners": sorted({str(row["listener"]) for row in rows}),
        "n_candidate_eval_rows": len(rows),
        "summary": summary,
        "paired_population_minus_mirror": paired,
        "paired_units": paired_units,
    }


def candidate_table(rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for row in rows:
        idx = int(row["candidate_index"])
        entry = out.setdefault(
            idx,
            {
                "message": str(row["message"]),
                "tokens": int(row.get("message_tokens") or len(str(row["message"]).split())),
                "by_listener": {},
            },
        )
        entry["by_listener"][str(row["listener"])] = {
            "success": float(row["success"]),
            "confidence": float(row.get("confidence") or 0.0),
            "choice_id": row.get("choice_id"),
        }
    return out


def select_by_listener(candidates: dict[int, dict[str, Any]], listeners: list[str]) -> int:
    def key(idx: int) -> tuple[float, float, int]:
        candidate = candidates[idx]
        train_success = mean(candidate["by_listener"][listener]["success"] for listener in listeners)
        score = train_success - LENGTH_PENALTY * candidate["tokens"]
        return (score, -candidate["tokens"], -idx)

    return max(candidates, key=key)


def record(
    dataset: str,
    scene_id: str,
    eval_listener: str,
    method: str,
    candidate_index: int,
    candidates: dict[int, dict[str, Any]],
    *,
    train_listeners: list[str] | None = None,
) -> dict[str, Any]:
    candidate = candidates[candidate_index]
    success = candidate["by_listener"][eval_listener]["success"]
    train_success = (
        mean(candidate["by_listener"][listener]["success"] for listener in train_listeners)
        if train_listeners
        else None
    )
    return {
        "dataset": dataset,
        "scene_id": scene_id,
        "eval_listener": eval_listener,
        "method": method,
        "candidate_index": candidate_index,
        "message": candidate["message"],
        "message_tokens": candidate["tokens"],
        "success": success,
        "train_success": train_success,
        "crossplay_gap": train_success - success if train_success is not None else None,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out = {}
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_method[row["method"]].append(row)
    for method, method_rows in sorted(by_method.items()):
        successes = [float(row["success"]) for row in method_rows]
        train_values = [
            float(row["train_success"])
            for row in method_rows
            if row.get("train_success") is not None
        ]
        out[method] = {
            "n_records": len(method_rows),
            "n_scenes": len({row["scene_id"] for row in method_rows}),
            "n_eval_listeners": len({row["eval_listener"] for row in method_rows}),
            "success": mean(successes),
            "success_ci95": bootstrap_ci(method_rows),
            "train_success": mean(train_values) if train_values else None,
            "crossplay_gap": (mean(train_values) - mean(successes)) if train_values else None,
            "mean_tokens": mean(float(row["message_tokens"]) for row in method_rows),
        }
    return out


def paired_population_minus_mirror(units: list[dict[str, Any]]) -> dict[str, Any]:
    diffs = [row["population_success"] - row["mirror_success"] for row in units]
    ci = bootstrap_values(diffs)
    p = two_sided_bootstrap_p(diffs)
    return {
        "n_units": len(units),
        "unit": "scene_eval_listener",
        "mean_population": mean(row["population_success"] for row in units),
        "mean_mirror": mean(row["mirror_success"] for row in units),
        "diff_population_minus_mirror": mean(diffs),
        "diff_ci95": ci,
        "paired_bootstrap_p_two_sided": p,
    }


def bootstrap_ci(rows: list[dict[str, Any]], n_boot: int = 5000, seed: int = 0) -> tuple[float, float]:
    # Resample scene/eval-listener units, not individual mirror train-listener rows.
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["scene_id"], row["eval_listener"])].append(row)
    unit_means = [mean(float(row["success"]) for row in unit_rows) for unit_rows in grouped.values()]
    return bootstrap_values(unit_means, n_boot=n_boot, seed=seed)


def bootstrap_values(values: list[float], n_boot: int = 5000, seed: int = 0) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in values]
        boot.append(mean(sample))
    boot.sort()
    return (boot[int(0.025 * (len(boot) - 1))], boot[int(0.975 * (len(boot) - 1))])


def two_sided_bootstrap_p(values: list[float], n_boot: int = 5000, seed: int = 0) -> float:
    if not values:
        return 1.0
    rng = random.Random(seed)
    boot = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in values]
        boot.append(mean(sample))
    p_le_zero = sum(1 for value in boot if value <= 0) / len(boot)
    p_ge_zero = sum(1 for value in boot if value >= 0) / len(boot)
    return min(1.0, 2 * min(p_le_zero, p_ge_zero))


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# API Listener Leave-One-Out Analysis",
        "",
        "This is a cache-only post-hoc analysis over all-candidate API listener evaluations.",
        "For each scene, one API listener prompt is held out for evaluation.",
        "The mirror selector chooses a candidate using one different API listener prompt; the population selector chooses using the other two.",
        "This probes whether listener-population selection helps across API prompt variants without making new API calls.",
        "",
        "## Summary",
        "",
        "| Dataset | Method | Eval rows | Cross-play | 95% CI | Train success | Gap | Tokens |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    method_order = [
        "loo_api_direct_first",
        "loo_api_shortest",
        "loo_api_mirror",
        "loo_api_population",
        "loo_api_oracle",
    ]
    for dataset in report["datasets"]:
        summary = dataset["summary"]
        for method in method_order:
            stats = summary[method]
            ci = stats["success_ci95"]
            lines.append(
                "| {dataset} | {method} | {n} | {success:.3f} | [{lo:.3f}, {hi:.3f}] | {train} | {gap} | {tokens:.1f} |".format(
                    dataset=dataset["label"],
                    method=method,
                    n=stats["n_records"],
                    success=stats["success"],
                    lo=ci[0],
                    hi=ci[1],
                    train=fmt(stats["train_success"]),
                    gap=fmt(stats["crossplay_gap"]),
                    tokens=stats["mean_tokens"],
                )
            )
    lines.extend(
        [
            "",
            "## Paired Population-Minus-Mirror",
            "",
            "| Dataset | Unit | N | Population | Mirror | Diff | 95% CI | p_boot |",
            "|---|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for dataset in report["datasets"]:
        paired = dataset["paired_population_minus_mirror"]
        ci = paired["diff_ci95"]
        lines.append(
            "| {dataset} | {unit} | {n} | {pop:.3f} | {mirror:.3f} | {diff:.3f} | [{lo:.3f}, {hi:.3f}] | {p:.4f} |".format(
                dataset=dataset["label"],
                unit=paired["unit"],
                n=paired["n_units"],
                pop=paired["mean_population"],
                mirror=paired["mean_mirror"],
                diff=paired["diff_population_minus_mirror"],
                lo=ci[0],
                hi=ci[1],
                p=paired["paired_bootstrap_p_two_sided"],
            )
        )
    lines.append("")
    lines.append(
        "Interpretation: this is not a replacement for the main held-out evaluation, because it reuses the same cached API listener pool for post-hoc splits. It is useful as a mechanism check: if population selection improves leave-one-listener-out success, the main result is less likely to be an artifact of the deterministic local selector alone."
    )
    lines.append("")
    return "\n".join(lines)


def tex_table(report: dict[str, Any]) -> str:
    rows = [
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Dataset & Mirror & Population & Oracle & Pop-Mirror & 95\\% CI \\\\",
        "\\midrule",
    ]
    for dataset in report["datasets"]:
        summary = dataset["summary"]
        paired = dataset["paired_population_minus_mirror"]
        ci = paired["diff_ci95"]
        rows.append(
            "{dataset} & {mirror:.3f} & {pop:.3f} & {oracle:.3f} & {diff:.3f} & [{lo:.3f}, {hi:.3f}] \\\\".format(
                dataset=escape_tex(dataset["label"]),
                mirror=summary["loo_api_mirror"]["success"],
                pop=summary["loo_api_population"]["success"],
                oracle=summary["loo_api_oracle"]["success"],
                diff=paired["diff_population_minus_mirror"],
                lo=ci[0],
                hi=ci[1],
            )
        )
    rows.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(rows)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


def escape_tex(text: str) -> str:
    return text.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


if __name__ == "__main__":
    main()
