#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cache-only token accounting for cached OpenAI Responses API calls."
    )
    parser.add_argument("--cache-dir", default="data/cached_responses")
    parser.add_argument("--markdown-out", default="docs/api_token_accounting.md")
    parser.add_argument("--json-out", default="results/api_token_accounting.json")
    args = parser.parse_args()

    report = analyze_cache(Path(args.cache_dir))
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path(args.markdown_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.markdown_out).write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))


def analyze_cache(cache_dir: Path) -> dict[str, Any]:
    files = sorted(cache_dir.glob("*.json"))
    rows = []
    unreadable = []
    missing_usage = []
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            unreadable.append(str(path))
            continue
        usage = usage_payload(payload)
        if not usage:
            missing_usage.append(str(path))
        rows.append(cache_row(path, payload, usage))

    return {
        "cache_dir": str(cache_dir),
        "n_cache_files": len(files),
        "n_readable": len(files) - len(unreadable),
        "n_unreadable": len(unreadable),
        "n_missing_usage": len(missing_usage),
        "totals": summarize_rows(rows),
        "by_model": grouped(rows, lambda row: (row["requested_model"], row["response_model"])),
        "by_schema_family": grouped(rows, lambda row: (row["schema_family"],)),
        "by_schema_version": grouped(rows, lambda row: (row["schema_version"],)),
        "notes": [
            "This report uses stored usage fields in data/cached_responses/*.json.",
            "It intentionally reports token accounting only; dollar cost depends on account-specific and date-specific pricing.",
            "Re-running cache-only analyses should not add tokens when the cached files are present.",
        ],
        "unreadable_examples": unreadable[:5],
        "missing_usage_examples": missing_usage[:5],
    }


def usage_payload(payload: dict[str, Any]) -> dict[str, Any]:
    usage = payload.get("usage")
    if isinstance(usage, dict) and usage:
        return usage
    usage = payload.get("data", {}).get("usage")
    if isinstance(usage, dict):
        return usage
    return {}


def cache_row(path: Path, payload: dict[str, Any], usage: dict[str, Any]) -> dict[str, Any]:
    request = payload.get("request_hash_payload", {})
    schema_version = str(request.get("schema_version", "unknown"))
    return {
        "path": str(path),
        "requested_model": str(request.get("model", "unknown")),
        "response_model": str(payload.get("data", {}).get("model", "unknown")),
        "schema_version": schema_version,
        "schema_family": schema_family(schema_version),
        "max_output_tokens": int(request.get("max_output_tokens", 0) or 0),
        "input_tokens": int(usage.get("input_tokens", 0) or 0),
        "output_tokens": int(usage.get("output_tokens", 0) or 0),
        "cached_input_tokens": int(
            usage.get("input_tokens_details", {}).get("cached_tokens", 0) or 0
        ),
        "total_tokens": int(usage.get("total_tokens", 0) or 0),
    }


def schema_family(schema_version: str) -> str:
    if schema_version.startswith("speaker"):
        return "speaker"
    if "listener" in schema_version:
        return "listener"
    return schema_version.split("-", 1)[0] if schema_version else "unknown"


def grouped(rows: list[dict[str, Any]], key_fn: Any) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[tuple(str(part) for part in key_fn(row))].append(row)
    out = []
    for key, group_rows in sorted(groups.items()):
        summary = summarize_rows(group_rows)
        if len(key) == 1:
            summary["label"] = key[0]
        else:
            summary["requested_model"] = key[0]
            summary["response_model"] = key[1]
        out.append(summary)
    return out


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_input = sum(row["input_tokens"] for row in rows)
    total_output = sum(row["output_tokens"] for row in rows)
    total_cached_input = sum(row["cached_input_tokens"] for row in rows)
    total_tokens = sum(row["total_tokens"] for row in rows)
    return {
        "n_responses": len(rows),
        "input_tokens": total_input,
        "output_tokens": total_output,
        "cached_input_tokens": total_cached_input,
        "total_tokens": total_tokens,
        "mean_total_tokens": mean(row["total_tokens"] for row in rows) if rows else 0.0,
    }


def render_markdown(report: dict[str, Any]) -> str:
    totals = report["totals"]
    lines = [
        "# API Token Accounting",
        "",
        "This cache-only report summarizes stored OpenAI Responses API usage fields.",
        "It is a reproducibility and budget-audit artifact, not a live billing statement.",
        "",
        "Dollar cost is intentionally not estimated here because pricing can depend on model, account, discounts, and date; use the provider dashboard for final billing.",
        "",
        "## Summary",
        "",
        "| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Mean tokens/response |",
        "|---:|---:|---:|---:|---:|---:|---:|",
        "| {files} | {readable} | {missing} | {input} | {output} | {total} | {mean:.1f} |".format(
            files=report["n_cache_files"],
            readable=report["n_readable"],
            missing=report["n_missing_usage"],
            input=totals["input_tokens"],
            output=totals["output_tokens"],
            total=totals["total_tokens"],
            mean=totals["mean_total_tokens"],
        ),
        "",
        "## By Model",
        "",
        "| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["by_model"]:
        lines.append(
            "| `{requested}` | `{response}` | {n} | {input} | {output} | {total} | {mean:.1f} |".format(
                requested=row["requested_model"],
                response=row["response_model"],
                n=row["n_responses"],
                input=row["input_tokens"],
                output=row["output_tokens"],
                total=row["total_tokens"],
                mean=row["mean_total_tokens"],
            )
        )

    lines.extend(
        [
            "",
            "## By Schema Family",
            "",
            "| Family | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in report["by_schema_family"]:
        lines.append(
            "| `{label}` | {n} | {input} | {output} | {total} | {mean:.1f} |".format(
                label=row["label"],
                n=row["n_responses"],
                input=row["input_tokens"],
                output=row["output_tokens"],
                total=row["total_tokens"],
                mean=row["mean_total_tokens"],
            )
        )

    lines.extend(
        [
            "",
            "Interpretation: all paper-facing API usage is recoverable from cached response files. Cache-only audits and table-generation scripts should not spend additional API budget when `data/cached_responses/` is present.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
