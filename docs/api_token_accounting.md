# API Token Accounting

This cache-only report summarizes stored OpenAI Responses API usage fields.
It is a reproducibility and budget-audit artifact, not a live billing statement.

Dollar cost is intentionally not estimated here because pricing can depend on model, account, discounts, and date; use the provider dashboard for final billing.

## Summary

| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---:|---:|---:|---:|---:|---:|---:|
| 7171 | 7171 | 0 | 1898304 | 181766 | 2080070 | 290.1 |

## By Model

| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---|---:|---:|---:|---:|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 | 301032 | 31225 | 332257 | 268.8 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 | 751850 | 68860 | 820710 | 296.3 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 3165 | 845422 | 81681 | 927103 | 292.9 |

## By Schema Family

| Family | Responses | Input tokens | Output tokens | Total tokens | Mean tokens/response |
|---|---:|---:|---:|---:|---:|
| `interaction` | 15 | 12913 | 1317 | 14230 | 948.7 |
| `listener` | 6898 | 1680843 | 163834 | 1844677 | 267.4 |
| `speaker` | 258 | 204548 | 16615 | 221163 | 857.2 |

Interpretation: all paper-facing API usage is recoverable from cached response files. Cache-only audits and table-generation scripts should not spend additional API budget when `data/cached_responses/` is present.
