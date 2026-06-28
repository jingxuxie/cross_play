#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RUNS = [
    {
        "setting": "Perspective stress",
        "listener": "gpt-5.4-nano",
        "summary": "results/perspective_stress50_hybrid_summary.json",
        "paired": "results/perspective_stress50_population_vs_mirror_paired.json",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
        "oracle_source": "all-candidate eval",
    },
    {
        "setting": "Perspective stress",
        "listener": "gpt-4.1-nano",
        "summary": "results/perspective_stress50_gpt41nano_summary.json",
        "paired": "results/perspective_stress50_gpt41nano_population_vs_mirror_paired.json",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
        "oracle_source": "all-candidate eval",
    },
    {
        "setting": "Perspective stress",
        "listener": "gpt-5.5",
        "summary": "results/gpt55_perspective_selected_summary.json",
        "paired": "results/gpt55_perspective_selected_population_vs_mirror_paired.json",
        "methods": {
            "direct": "direct_first",
            "shortest": "best_of_k_shortest",
            "mirror": "mirror_selfplay",
            "population": "population_play",
            "prior_oracle": "prior_listener_oracle",
        },
        "oracle_source": "implied by population=1.000",
    },
    {
        "setting": "Partial observability",
        "listener": "gpt-5.4-nano",
        "summary": "results/partial_observability_api50_summary.json",
        "paired": "results/partial_observability_api50_population_vs_mirror_paired.json",
        "methods": {
            "direct": "api_direct_first",
            "shortest": "api_best_of_k_shortest",
            "mirror": "hybrid_local_mirror_api_eval",
            "population": "hybrid_local_population_api_eval",
            "oracle": "oracle_upper_bound",
        },
        "oracle_source": "all-candidate eval",
    },
    {
        "setting": "Partial observability",
        "listener": "gpt-4.1-nano",
        "summary": "results/gpt41_partial_observability_selected_summary.json",
        "paired": "results/gpt41_partial_observability_selected_population_vs_mirror_paired.json",
        "methods": {
            "direct": "direct_first",
            "shortest": "best_of_k_shortest",
            "mirror": "mirror_selfplay",
            "population": "population_play",
            "prior_oracle": "prior_listener_oracle",
        },
        "oracle_source": "implied by population=1.000",
    },
    {
        "setting": "Partial observability",
        "listener": "gpt-5.5",
        "summary": "results/gpt55_partial_observability_selected_summary.json",
        "paired": "results/gpt55_partial_observability_selected_population_vs_mirror_paired.json",
        "methods": {
            "direct": "direct_first",
            "shortest": "best_of_k_shortest",
            "mirror": "mirror_selfplay",
            "population": "population_play",
            "prior_oracle": "prior_listener_oracle",
        },
        "oracle_source": "implied by population=1.000",
    },
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", default="results/cross_model_listener_audit.json")
    parser.add_argument("--markdown-out", default="docs/cross_model_listener_audit.md")
    parser.add_argument("--table-out", default="paper/tables/cross_model_listener_audit.md")
    parser.add_argument("--tex-out", default="paper/tables/cross_model_listener_audit.tex")
    args = parser.parse_args()

    rows = [load_run(spec) for spec in RUNS]
    report = {
        "rows": rows,
        "interpretation": (
            "Population-play is 1.000 in all cross-model rows, while mirror self-play "
            "drops under every held-out listener family and remains weak under GPT-5.5."
        ),
    }
    write_text(args.json_out, json.dumps(report, indent=2, sort_keys=True) + "\n")
    write_text(args.markdown_out, markdown_report(rows))
    write_text(args.table_out, markdown_table(rows))
    write_text(args.tex_out, tex_table(rows))
    print(markdown_report(rows))


def load_run(spec: dict[str, Any]) -> dict[str, Any]:
    summary = json.loads(Path(spec["summary"]).read_text(encoding="utf-8"))
    by_method = summary["by_method"]
    methods = spec["methods"]
    population = metric(by_method, methods["population"])
    oracle_source = spec["oracle_source"]
    if "oracle" in methods:
        oracle = metric(by_method, methods["oracle"])
    elif population["success"] == 1.0:
        oracle = {"success": 1.0, "success_ci95": [1.0, 1.0]}
    else:
        oracle = metric(by_method, methods["prior_oracle"])
        oracle_source = "prior-listener oracle message"
    row = {
        "setting": spec["setting"],
        "listener": spec["listener"],
        "n_scenes": summary["overall"]["n_scenes"],
        "direct": metric(by_method, methods["direct"]),
        "shortest": metric(by_method, methods["shortest"]),
        "mirror": metric(by_method, methods["mirror"]),
        "population": population,
        "oracle": oracle,
        "oracle_source": oracle_source,
        "prior_listener_oracle": (
            metric(by_method, methods["prior_oracle"]) if "prior_oracle" in methods else None
        ),
        "population_minus_mirror": overall_paired(spec["paired"]),
        "summary_source": spec["summary"],
        "paired_source": spec["paired"],
    }
    return row


def metric(by_method: dict[str, Any], method: str) -> dict[str, Any]:
    stats = by_method[method]
    return {
        "method": method,
        "success": stats["success"],
        "success_ci95": list(stats["success_ci95"]),
    }


def overall_paired(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data
    for row in data:
        if row.get("scenario_type") is None:
            return row
    raise ValueError(f"no overall paired comparison in {path}")


def markdown_report(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Cross-Model Held-Out Listener Audit",
        "",
        "This table combines existing held-out listener runs with new selected-message audits for GPT-5.5 and the missing GPT-4.1 partial-observability column.",
        "",
        markdown_table(rows).strip(),
        "",
        "## Gap Table",
        "",
        gap_table(rows).strip(),
        "",
        "Notes:",
        "- GPT-5.5 rows reuse existing speaker candidates and evaluate selected messages only.",
        "- When population-play has 1.000 success, the same candidate pool's true oracle is also 1.000; no all-candidate GPT-5.5 rerun is needed to establish the oracle ceiling.",
        "- `Prior oracle` is the message selected as oracle by the earlier listener family, then evaluated by the listed listener family.",
        "",
    ]
    return "\n".join(lines)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Setting | Held-out listener | Direct | Shortest | Mirror | Population | Oracle | Prior oracle | Oracle source |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {setting} | {listener} | {direct} | {shortest} | {mirror} | {population} | {oracle} | {prior} | {source} |".format(
                setting=row["setting"],
                listener=row["listener"],
                direct=fmt(row["direct"]["success"]),
                shortest=fmt(row["shortest"]["success"]),
                mirror=fmt(row["mirror"]["success"]),
                population=fmt(row["population"]["success"]),
                oracle=fmt(row["oracle"]["success"]),
                prior=fmt(row["prior_listener_oracle"]["success"]) if row["prior_listener_oracle"] else "-",
                source=row["oracle_source"],
            )
        )
    return "\n".join(lines) + "\n"


def gap_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Setting | Held-out listener | Population - mirror | 95% CI | n pairs | p_boot |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        paired = row["population_minus_mirror"]
        ci = paired["diff_ci95"]
        lines.append(
            "| {setting} | {listener} | {diff} | [{lo}, {hi}] | {n} | {p} |".format(
                setting=row["setting"],
                listener=row["listener"],
                diff=fmt(paired["diff_a_minus_b"]),
                lo=fmt(ci[0]),
                hi=fmt(ci[1]),
                n=paired["n_pairs"],
                p=fmt(paired["paired_bootstrap_p_two_sided"], digits=4),
            )
        )
    return "\n".join(lines) + "\n"


def tex_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "\\begin{tabular}{llrrrrr}",
        "\\toprule",
        "Setting & Listener & Direct & Mirror & Population & Oracle & Pop.-Mirror \\\\",
        "\\midrule",
    ]
    for row in rows:
        paired = row["population_minus_mirror"]
        lines.append(
            "{setting} & {listener} & {direct} & {mirror} & {population} & {oracle} & {gap} \\\\".format(
                setting=escape_tex(row["setting"]),
                listener=escape_tex(row["listener"]),
                direct=fmt(row["direct"]["success"]),
                mirror=fmt(row["mirror"]["success"]),
                population=fmt(row["population"]["success"]),
                oracle=fmt(row["oracle"]["success"]),
                gap=fmt(paired["diff_a_minus_b"]),
            )
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(lines)


def fmt(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def escape_tex(text: str) -> str:
    return text.replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


def write_text(path: str | Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
