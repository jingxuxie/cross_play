# API Token Accounting

This cache-only report summarizes stored OpenAI Responses API usage fields.
It is a reproducibility and budget-audit artifact, not a live billing statement.

Dollar cost is intentionally not estimated here because pricing can depend on model, account, discounts, and date; use the provider dashboard for final billing.

## Summary

| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---:|---:|---:|---:|---:|---:|---:|
| 5866 | 5866 | 0 | 1535340 | 145114 | 1680454 | 286.5 |

## By Model

| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---|---:|---:|---:|---:|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 | 301032 | 31225 | 332257 | 268.8 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 | 751850 | 68860 | 820710 | 296.3 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 1860 | 482458 | 45029 | 527487 | 283.6 |

## By Schema Family

| Family | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---:|---:|---:|---:|---:|
| `listener` | 5658 | 1373252 | 133311 | 1506563 | 266.3 |
| `speaker` | 208 | 162088 | 11803 | 173891 | 836.0 |

Interpretation: all paper-facing API usage is recoverable from cached response files. Cache-only audits and table-generation scripts should not spend additional API budget when `data/cached_responses/` is present.
