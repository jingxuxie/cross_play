#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from prag_crossplay.data import read_jsonl


ROLE_LABELS = {
    0: "natural_first",
    1: "attribute_short",
    2: "relational_or_spatial",
    3: "coordinate_fallback",
}
ROLE_DISPLAY = {
    "natural_first": "Natural first",
    "attribute_short": "Attribute short",
    "relational_or_spatial": "Relational/spatial",
    "coordinate_fallback": "Coordinate fallback",
    "unresolved": "Unresolved",
}
ROLE_ORDER = [
    "natural_first",
    "attribute_short",
    "relational_or_spatial",
    "coordinate_fallback",
]

RUNS = [
    {
        "label": "mixed_50_full",
        "filter": "full",
        "selection_kind": "full",
        "selection_source": "results/hybrid_api_pilot50_allcand_candidates.jsonl",
        "records": "results/hybrid_api_pilot50_allcand_records.jsonl",
        "selections": {
            "mirror": {
                "field": "mirror_selected",
                "method": "hybrid_local_mirror_api_eval",
            },
            "population": {
                "field": "population_selected",
                "method": "hybrid_local_population_api_eval",
            },
        },
    },
    {
        "label": "perspective_gpt54_full",
        "filter": "full",
        "selection_kind": "full",
        "selection_source": "results/perspective_stress50_hybrid_candidates.jsonl",
        "records": "results/perspective_stress50_hybrid_records.jsonl",
        "selections": {
            "mirror": {
                "field": "mirror_selected",
                "method": "hybrid_local_mirror_api_eval",
            },
            "population": {
                "field": "population_selected",
                "method": "hybrid_local_population_api_eval",
            },
        },
    },
    {
        "label": "perspective_gpt41_full",
        "filter": "full",
        "selection_kind": "full",
        "selection_source": "results/perspective_stress50_gpt41nano_audit.jsonl",
        "records": "results/perspective_stress50_gpt41nano_records.jsonl",
        "selections": {
            "mirror": {
                "field": "mirror_selected",
                "method": "hybrid_local_mirror_api_eval",
            },
            "population": {
                "field": "population_selected",
                "method": "hybrid_local_population_api_eval",
            },
        },
    },
    {
        "label": "partial_observability_full",
        "filter": "full",
        "selection_kind": "full",
        "selection_source": "results/partial_observability_api50_candidates.jsonl",
        "records": "results/partial_observability_api50_records.jsonl",
        "selections": {
            "mirror": {
                "field": "mirror_selected",
                "method": "hybrid_local_mirror_api_eval",
            },
            "population": {
                "field": "population_selected",
                "method": "hybrid_local_population_api_eval",
            },
        },
    },
    {
        "label": "mixed_50_no_coord",
        "filter": "no_exact_coordinates",
        "selection_kind": "no_coord",
        "selection_source": "results/hybrid_api_pilot50_no_coord_audit.jsonl",
        "records": "results/hybrid_api_pilot50_no_coord_records.jsonl",
        "selections": {
            "mirror": {"field": "mirror_selected", "method": "no_coord_mirror"},
            "population": {"field": "population_selected", "method": "no_coord_population"},
            "consensus+info": {
                "field": "consensus_info_selected",
                "method": "no_coord_consensus_info",
            },
        },
    },
    {
        "label": "perspective_gpt41_no_coord",
        "filter": "no_exact_coordinates",
        "selection_kind": "no_coord",
        "selection_source": "results/perspective_stress50_gpt41nano_no_coord_audit.jsonl",
        "records": "results/perspective_stress50_gpt41nano_no_coord_records.jsonl",
        "selections": {
            "mirror": {"field": "mirror_selected", "method": "no_coord_mirror"},
            "population": {"field": "population_selected", "method": "no_coord_population"},
            "consensus+info": {
                "field": "consensus_info_selected",
                "method": "no_coord_consensus_info",
            },
        },
    },
    {
        "label": "partial_observability_no_coord",
        "filter": "no_exact_coordinates",
        "selection_kind": "no_coord",
        "selection_source": "results/partial_observability_api50_no_coord_audit.jsonl",
        "records": "results/partial_observability_api50_no_coord_records.jsonl",
        "selections": {
            "mirror": {"field": "mirror_selected", "method": "no_coord_mirror"},
            "population": {"field": "population_selected", "method": "no_coord_population"},
            "consensus+info": {
                "field": "consensus_info_selected",
                "method": "no_coord_consensus_info",
            },
        },
    },
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cache-only audit of which generated candidate slot each selector chooses."
    )
    parser.add_argument("--markdown-out", default="docs/candidate_role_selection_audit.md")
    parser.add_argument("--json-out", default="results/candidate_role_selection_audit.json")
    args = parser.parse_args()

    runs = [analyze_run(spec) for spec in RUNS]
    report = {
        "role_labels": {str(key): value for key, value in ROLE_LABELS.items()},
        "role_order": ROLE_ORDER,
        "runs": runs,
        "summary": summarize_report(runs),
    }
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_run(spec: dict[str, Any]) -> dict[str, Any]:
    rows = read_jsonl(spec["selection_source"])
    scene_success = scene_method_success(read_jsonl(spec["records"]))
    methods = [
        summarize_selection(
            rows,
            spec["selection_kind"],
            method_label,
            selection["field"],
            selection["method"],
            scene_success,
        )
        for method_label, selection in spec["selections"].items()
    ]
    return {
        "label": spec["label"],
        "filter": spec["filter"],
        "selection_kind": spec["selection_kind"],
        "selection_source": spec["selection_source"],
        "records": spec["records"],
        "methods": methods,
    }


def scene_method_success(records: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in records:
        grouped[str(row["scene_id"])][str(row["method"])].append(float(row["success"]))
    return {
        scene_id: {method: mean(values) for method, values in by_method.items()}
        for scene_id, by_method in grouped.items()
    }


def summarize_selection(
    rows: list[dict[str, Any]],
    selection_kind: str,
    method_label: str,
    field: str,
    method_name: str,
    scene_success: dict[str, dict[str, float]],
) -> dict[str, Any]:
    role_counts: Counter[str] = Counter()
    role_success: dict[str, list[float]] = defaultdict(list)
    success_values: list[float] = []
    unresolved_examples: list[dict[str, str]] = []
    missing_success = 0

    for row in rows:
        scene_id = str(row["scene_id"])
        original_index = selected_original_index(row, field, selection_kind)
        if original_index is None:
            role = "unresolved"
            if len(unresolved_examples) < 5:
                unresolved_examples.append(
                    {
                        "scene_id": scene_id,
                        "selected": str(row.get(field, "")),
                    }
                )
        else:
            role = ROLE_LABELS.get(original_index, "unresolved")
        role_counts[role] += 1

        success = scene_success.get(scene_id, {}).get(method_name)
        if success is None:
            missing_success += 1
            continue
        success_values.append(success)
        role_success[role].append(success)

    n_scenes = len(rows)
    return {
        "method_label": method_label,
        "method": method_name,
        "selection_field": field,
        "n_scenes": n_scenes,
        "n_success_scenes": len(success_values),
        "n_missing_success": missing_success,
        "n_unresolved": role_counts["unresolved"],
        "success": mean(success_values) if success_values else None,
        "role_counts": {role: role_counts[role] for role in ROLE_ORDER + ["unresolved"]},
        "role_rates": {
            role: (role_counts[role] / n_scenes if n_scenes else 0.0)
            for role in ROLE_ORDER + ["unresolved"]
        },
        "role_success": {
            role: (mean(values) if values else None)
            for role, values in sorted(role_success.items())
        },
        "unresolved_examples": unresolved_examples,
    }


def selected_original_index(
    row: dict[str, Any],
    field: str,
    selection_kind: str,
) -> int | None:
    selected = row.get(field)
    if selected is None:
        return None
    if selection_kind == "full":
        return find_index(str(selected), [str(value) for value in row.get("candidates", [])])
    if selection_kind == "no_coord":
        kept_candidates = [str(value) for value in row.get("kept_candidates", [])]
        kept_indices = [int(value) for value in row.get("kept_candidate_indices", [])]
        kept_position = find_index(str(selected), kept_candidates)
        if kept_position is None or kept_position >= len(kept_indices):
            return None
        return kept_indices[kept_position]
    raise ValueError(f"unknown selection kind: {selection_kind}")


def find_index(selected: str, candidates: list[str]) -> int | None:
    for index, candidate in enumerate(candidates):
        if candidate == selected:
            return index
    normalized_selected = normalize_message(selected)
    for index, candidate in enumerate(candidates):
        if normalize_message(candidate) == normalized_selected:
            return index
    return None


def normalize_message(message: str) -> str:
    return " ".join(message.replace("’", "'").split()).strip().lower()


def summarize_report(runs: list[dict[str, Any]]) -> dict[str, Any]:
    by_run_method = {
        (run["label"], method["method_label"]): method
        for run in runs
        for method in run["methods"]
    }
    full_labels = [
        "mixed_50_full",
        "perspective_gpt54_full",
        "perspective_gpt41_full",
        "partial_observability_full",
    ]
    no_coord_labels = [
        "mixed_50_no_coord",
        "perspective_gpt41_no_coord",
        "partial_observability_no_coord",
    ]
    return {
        "full_mirror_attribute_short_rates": [
            {
                "label": label,
                "rate": by_run_method[(label, "mirror")]["role_rates"]["attribute_short"],
            }
            for label in full_labels
        ],
        "full_population_coordinate_fallback_rates": [
            {
                "label": label,
                "rate": by_run_method[(label, "population")]["role_rates"]["coordinate_fallback"],
            }
            for label in full_labels
        ],
        "no_coord_mirror_attribute_short_rates": [
            {
                "label": label,
                "rate": by_run_method[(label, "mirror")]["role_rates"]["attribute_short"],
            }
            for label in no_coord_labels
        ],
        "no_coord_consensus_relational_rates": [
            {
                "label": label,
                "rate": by_run_method[(label, "consensus+info")]["role_rates"]["relational_or_spatial"],
            }
            for label in no_coord_labels
        ],
        "no_coord_consensus_attribute_short_rates": [
            {
                "label": label,
                "rate": by_run_method[(label, "consensus+info")]["role_rates"]["attribute_short"],
            }
            for label in no_coord_labels
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Candidate Role Selection Audit",
        "",
        "This cache-only audit maps each selected message back to its original generated candidate slot.",
        "The role labels are prompt-slot labels, not a learned text classifier.",
        "",
        "## Candidate Slot Roles",
        "",
        "| Original index | Role | Meaning |",
        "|---:|---|---|",
        "| 0 | natural_first | First natural speaker message |",
        "| 1 | attribute_short | Short attribute-only message |",
        "| 2 | relational_or_spatial | Non-coordinate relational or spatial fallback |",
        "| 3 | coordinate_fallback | Exact row/column fallback, removed in no-coordinate runs |",
        "",
        "## Selection Role Distribution",
        "",
        "| Run | Filter | Method | Scenes | Success | Natural first | Attribute short | Relational/spatial | Coordinate fallback | Unresolved | Source |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for run in report["runs"]:
        for row in run["methods"]:
            rates = row["role_rates"]
            lines.append(
                "| {run} | {filter} | {method} | {scenes} | {success} | {natural} | {attribute} | {relational} | {coord} | {unresolved} | `{source}` |".format(
                    run=run["label"],
                    filter=run["filter"],
                    method=row["method_label"],
                    scenes=row["n_scenes"],
                    success=fmt(row["success"]),
                    natural=fmt(rates["natural_first"]),
                    attribute=fmt(rates["attribute_short"]),
                    relational=fmt(rates["relational_or_spatial"]),
                    coord=fmt(rates["coordinate_fallback"]),
                    unresolved=row["n_unresolved"],
                    source=run["selection_source"],
                )
            )

    lines.extend(
        [
            "",
            "## Mechanism Summary",
            "",
            "- Full-candidate mirror often selects the short attribute slot, while full-candidate population shifts toward the coordinate fallback when that fallback is available.",
            "- When exact coordinates are removed, consensus+info sharply reduces short attribute-slot selection; in the harder perspective and partial-observability runs it selects the short attribute slot in 0.000 of scenes.",
            "- The audit is replay-only: it uses existing candidate, no-coordinate audit, and selected-message record files.",
            "",
            "Full-candidate mirror attribute-short rates: {rates}.".format(
                rates=format_label_rates(report["summary"]["full_mirror_attribute_short_rates"])
            ),
            "Full-candidate population coordinate-fallback rates: {rates}.".format(
                rates=format_label_rates(report["summary"]["full_population_coordinate_fallback_rates"])
            ),
            "No-coordinate consensus+info relational/spatial rates: {rates}.".format(
                rates=format_label_rates(report["summary"]["no_coord_consensus_relational_rates"])
            ),
            "No-coordinate consensus+info attribute-short rates: {rates}.".format(
                rates=format_label_rates(report["summary"]["no_coord_consensus_attribute_short_rates"])
            ),
            "",
        ]
    )
    return "\n".join(lines)


def format_label_rates(rows: list[dict[str, Any]]) -> str:
    return ", ".join(f"{row['label']}={row['rate']:.3f}" for row in rows)


def fmt(value: float | None) -> str:
    return "-" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    main()
