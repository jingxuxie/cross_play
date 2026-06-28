# API Token Accounting

This cache-only report summarizes stored OpenAI Responses API usage fields.
It is a reproducibility and budget-audit artifact, not a live billing statement.

Dollar cost is intentionally not estimated here because pricing can depend on model, account, discounts, and date; use the provider dashboard for final billing.

## Summary

| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---:|---:|---:|---:|---:|---:|---:|
| 7113 | 7113 | 0 | 1874818 | 177461 | 2052279 | 288.5 |

## By Model

| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---|---:|---:|---:|---:|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 | 301032 | 31225 | 332257 | 268.8 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 | 751850 | 68860 | 820710 | 296.3 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 3107 | 821936 | 77376 | 899312 | 289.4 |

## By Schema Family

| Family | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---:|---:|---:|---:|---:|
| `listener` | 6855 | 1670270 | 160846 | 1831116 | 267.1 |
| `speaker` | 258 | 204548 | 16615 | 221163 | 857.2 |

Interpretation: all paper-facing API usage is recoverable from cached response files. Cache-only audits and table-generation scripts should not spend additional API budget when `data/cached_responses/` is present.
