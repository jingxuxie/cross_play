# Cross-Model Held-Out Listener Audit

This table combines existing held-out listener runs with new selected-message audits for GPT-5.5 and the missing GPT-4.1 partial-observability column.

| Setting | Held-out listener | Direct | Shortest | Mirror | Population | Oracle | Prior oracle | Oracle source |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Perspective stress | gpt-5.4-nano | 0.713 | 0.420 | 0.813 | 1.000 | 1.000 | - | all-candidate eval |
| Perspective stress | gpt-4.1-nano | 0.553 | 0.367 | 0.713 | 1.000 | 1.000 | - | all-candidate eval |
| Perspective stress | gpt-5.5 | 0.793 | 0.507 | 0.673 | 1.000 | 1.000 | 0.893 | implied by population=1.000 |
| Partial observability | gpt-5.4-nano | 0.740 | 0.313 | 0.667 | 1.000 | 1.000 | - | all-candidate eval |
| Partial observability | gpt-4.1-nano | 0.700 | 0.560 | 0.660 | 1.000 | 1.000 | 0.947 | implied by population=1.000 |
| Partial observability | gpt-5.5 | 0.740 | 0.453 | 0.653 | 1.000 | 1.000 | 0.960 | implied by population=1.000 |

## Gap Table

| Setting | Held-out listener | Population - mirror | 95% CI | n pairs | p_boot |
|---|---|---:|---:|---:|---:|
| Perspective stress | gpt-5.4-nano | 0.187 | [0.100, 0.287] | 50 | 0.0000 |
| Perspective stress | gpt-4.1-nano | 0.287 | [0.193, 0.380] | 50 | 0.0000 |
| Perspective stress | gpt-5.5 | 0.327 | [0.233, 0.420] | 50 | 0.0000 |
| Partial observability | gpt-5.4-nano | 0.333 | [0.240, 0.427] | 50 | 0.0000 |
| Partial observability | gpt-4.1-nano | 0.340 | [0.247, 0.433] | 50 | 0.0000 |
| Partial observability | gpt-5.5 | 0.347 | [0.253, 0.440] | 50 | 0.0000 |

Notes:
- GPT-5.5 rows reuse existing speaker candidates and evaluate selected messages only.
- When population-play has 1.000 success, the same candidate pool's true oracle is also 1.000; no all-candidate GPT-5.5 rerun is needed to establish the oracle ceiling.
- `Prior oracle` is the message selected as oracle by the earlier listener family, then evaluated by the listed listener family.
