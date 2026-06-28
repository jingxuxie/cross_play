# API Listener Leave-One-Out Analysis

This is a cache-only post-hoc analysis over all-candidate API listener evaluations.
For each scene, one API listener prompt is held out for evaluation.
The mirror selector chooses a candidate using one different API listener prompt; the population selector chooses using the other two.
This probes whether listener-population selection helps across API prompt variants without making new API calls.

## Summary

| Dataset | Method | Eval rows | Cross-play | 95% CI | Train success | Gap | Tokens |
|---|---|---:|---:|---:|---:|---:|---:|
| mixed_50 | loo_api_direct_first | 150 | 0.840 | [0.780, 0.893] | - | - | 9.3 |
| mixed_50 | loo_api_shortest | 150 | 0.740 | [0.667, 0.807] | - | - | 4.3 |
| mixed_50 | loo_api_mirror | 300 | 0.953 | [0.920, 0.980] | 1.000 | 0.047 | 5.7 |
| mixed_50 | loo_api_population | 150 | 0.973 | [0.947, 0.993] | 1.000 | 0.027 | 5.9 |
| mixed_50 | loo_api_oracle | 150 | 1.000 | [1.000, 1.000] | - | - | 5.7 |
| perspective_gpt54 | loo_api_direct_first | 150 | 0.713 | [0.640, 0.780] | - | - | 11.7 |
| perspective_gpt54 | loo_api_shortest | 150 | 0.420 | [0.347, 0.500] | - | - | 4.6 |
| perspective_gpt54 | loo_api_mirror | 300 | 0.907 | [0.863, 0.947] | 1.000 | 0.093 | 7.8 |
| perspective_gpt54 | loo_api_population | 150 | 0.933 | [0.893, 0.967] | 1.000 | 0.067 | 8.2 |
| perspective_gpt54 | loo_api_oracle | 150 | 1.000 | [1.000, 1.000] | - | - | 7.8 |
| perspective_gpt41 | loo_api_direct_first | 150 | 0.553 | [0.473, 0.633] | - | - | 11.7 |
| perspective_gpt41 | loo_api_shortest | 150 | 0.367 | [0.293, 0.447] | - | - | 4.6 |
| perspective_gpt41 | loo_api_mirror | 300 | 0.847 | [0.797, 0.890] | 1.000 | 0.153 | 8.1 |
| perspective_gpt41 | loo_api_population | 150 | 0.940 | [0.900, 0.973] | 1.000 | 0.060 | 8.9 |
| perspective_gpt41 | loo_api_oracle | 150 | 1.000 | [1.000, 1.000] | - | - | 8.1 |
| partial_observability | loo_api_direct_first | 150 | 0.740 | [0.667, 0.807] | - | - | 10.0 |
| partial_observability | loo_api_shortest | 150 | 0.313 | [0.240, 0.387] | - | - | 4.0 |
| partial_observability | loo_api_mirror | 300 | 0.767 | [0.717, 0.813] | 1.000 | 0.233 | 7.8 |
| partial_observability | loo_api_population | 150 | 0.940 | [0.900, 0.973] | 1.000 | 0.060 | 9.0 |
| partial_observability | loo_api_oracle | 150 | 1.000 | [1.000, 1.000] | - | - | 7.8 |

## Paired Population-Minus-Mirror

| Dataset | Unit | N | Population | Mirror | Diff | 95% CI | p_boot |
|---|---|---:|---:|---:|---:|---:|---:|
| mixed_50 | scene_eval_listener | 150 | 0.973 | 0.953 | 0.020 | [0.007, 0.037] | 0.0068 |
| perspective_gpt54 | scene_eval_listener | 150 | 0.933 | 0.907 | 0.027 | [0.010, 0.047] | 0.0012 |
| perspective_gpt41 | scene_eval_listener | 150 | 0.940 | 0.847 | 0.093 | [0.063, 0.123] | 0.0000 |
| partial_observability | scene_eval_listener | 150 | 0.940 | 0.767 | 0.173 | [0.133, 0.213] | 0.0000 |

Interpretation: this is not a replacement for the main held-out evaluation, because it reuses the same cached API listener pool for post-hoc splits. It is useful as a mechanism check: if population selection improves leave-one-listener-out success, the main result is less likely to be an artifact of the deterministic local selector alone.
