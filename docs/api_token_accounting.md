# API Token Accounting

This cache-only report summarizes stored OpenAI Responses API usage fields.
It is a reproducibility and budget-audit artifact, not a live billing statement.

Dollar cost is intentionally not estimated here because pricing can depend on model, account, discounts, and date; use the provider dashboard for final billing.

## Summary

| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---:|---:|---:|---:|---:|---:|---:|
| 3520 | 3520 | 0 | 940088 | 87829 | 1027917 | 292.0 |

## By Model

| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---|---:|---:|---:|---:|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 750 | 188238 | 18969 | 207207 | 276.3 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 | 751850 | 68860 | 820710 | 296.3 |

## By Schema Family

| Family | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---:|---:|---:|---:|---:|
| `listener` | 3362 | 817510 | 78988 | 896498 | 266.7 |
| `speaker` | 158 | 122578 | 8841 | 131419 | 831.8 |

Interpretation: all paper-facing API usage is recoverable from cached response files. Cache-only audits and table-generation scripts should not spend additional API budget when `data/cached_responses/` is present.
