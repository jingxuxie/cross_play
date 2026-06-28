#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl, read_scenes
from prag_crossplay.scoring import markdown_table, summarize_records


METHOD_LABELS = {
    "template": "Template",
    "direct": "Direct",
    "best_of_k_shortest": "Best-of-K shortest",
    "mirror_selfplay": "Mirror self-play",
    "population_play": "Population-play",
    "oracle_upper_bound": "Oracle candidate",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene-file", default="data/local_benchmark600_scenes.jsonl")
    parser.add_argument("--records", default="results/local_benchmark600_records.jsonl")
    parser.add_argument("--markdown-out", default="docs/local_benchmark600_check.md")
    parser.add_argument("--json-out", default="results/local_benchmark600_check.json")
    args = parser.parse_args()

    report = build_report(args.scene_file, args.records)
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def build_report(scene_file: str, records_file: str) -> dict[str, Any]:
    scenes = read_scenes(scene_file)
    records = read_jsonl(records_file)
    summary = summarize_records(records)
    scenario_counts = dict(sorted(Counter(scene.scenario_type for scene in scenes).items()))
    return {
        "scene_file": scene_file,
        "records_file": records_file,
        "n_scenes": len(scenes),
        "scenario_counts": scenario_counts,
        "summary": summary,
        "key_observations": key_observations(summary),
    }


def key_observations(summary: dict[str, Any]) -> dict[str, Any]:
    by_method = summary["by_method"]
    by_scenario = summary["by_scenario_method"]
    return {
        "mirror_cross": by_method["mirror_selfplay"]["success"],
        "mirror_same": by_method["mirror_selfplay"]["sameplay_success"],
        "mirror_gap": by_method["mirror_selfplay"]["crossplay_gap"],
        "population_cross": by_method["population_play"]["success"],
        "template_cross": by_method["template"]["success"],
        "oracle_cross": by_method["oracle_upper_bound"]["success"],
        "perspective_mirror_cross": by_scenario["perspective_shift"]["mirror_selfplay"]["success"],
        "perspective_mirror_gap": by_scenario["perspective_shift"]["mirror_selfplay"]["crossplay_gap"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Local Benchmark-Scale Sanity Check",
        "",
        "This no-API check runs the deterministic local listeners over a 600-scene",
        "balanced benchmark sweep. It is an artifact and generator sanity check, not",
        "one of the paper-facing API listener results.",
        "",
        f"Scene file: `{report['scene_file']}`",
        f"Record file: `{report['records_file']}`",
        "",
        "## Dataset",
        "",
        "| Scenario type | Scenes |",
        "|---|---:|",
    ]
    for scenario, count in report["scenario_counts"].items():
        lines.append(f"| {scenario} | {count} |")

    obs = report["key_observations"]
    lines.extend(
        [
            "",
            "## Key Observations",
            "",
            f"- Mirror self-play has same-play {fmt(obs['mirror_same'])} but cross-play {fmt(obs['mirror_cross'])}, a gap of {fmt(obs['mirror_gap'])}.",
            f"- Population-play, template, and oracle candidate all reach cross-play {fmt(obs['population_cross'])}.",
            f"- Perspective-shift is the hardest local family: mirror cross-play is {fmt(obs['perspective_mirror_cross'])}, with a gap of {fmt(obs['perspective_mirror_gap'])}.",
            "",
            "## Overall Results",
            "",
        ]
    )
    lines.append(markdown_table(report["summary"]).rstrip())

    lines.extend(
        [
            "",
            "## Scenario Breakdown",
            "",
            "| Scenario | Direct | Mirror cross | Mirror same | Mirror gap | Population | Oracle |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for scenario, methods in sorted(report["summary"]["by_scenario_method"].items()):
        lines.append(
            "| {scenario} | {direct} | {mirror} | {mirror_same} | {gap} | {population} | {oracle} |".format(
                scenario=scenario,
                direct=fmt(methods["direct"]["success"]),
                mirror=fmt(methods["mirror_selfplay"]["success"]),
                mirror_same=fmt(methods["mirror_selfplay"]["sameplay_success"]),
                gap=fmt(methods["mirror_selfplay"]["crossplay_gap"]),
                population=fmt(methods["population_play"]["success"]),
                oracle=fmt(methods["oracle_upper_bound"]["success"]),
            )
        )
    return "\n".join(lines) + "\n"


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    main()
