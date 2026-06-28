# Random Candidate Baseline

This cache-only audit compares learned or heuristic selectors with a uniform random selector over the same generated candidate pool.
The random baseline is computed exactly as the average held-out success of available candidates in each scene, then averaged over scenes.

## Summary

| Run | Filter | Scenes | Candidates/scene | Random expected | Random robust-pick rate | Primary selector | Primary-minus-random 95% CI | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| mixed_50_full | full | 50 | 4.00 | 0.865 | 0.825 | population | 0.135 [0.078, 0.193] | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl` |
| perspective_gpt54_full | full | 50 | 4.00 | 0.715 | 0.610 | population | 0.285 [0.227, 0.345] | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl` |
| perspective_gpt41_full | full | 50 | 4.00 | 0.657 | 0.535 | population | 0.343 [0.282, 0.405] | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl` |
| partial_observability_full | full | 50 | 4.00 | 0.753 | 0.645 | population | 0.247 [0.217, 0.277] | `results/partial_observability_api50_candidate_eval_records.jsonl` |
| mixed_50_no_coord | no_exact_coordinates | 50 | 3.00 | 0.820 | 0.767 | consensus+info | 0.100 [0.036, 0.167] | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl` |
| perspective_gpt41_no_coord | no_exact_coordinates | 50 | 3.00 | 0.542 | 0.380 | consensus+info | 0.218 [0.156, 0.280] | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl` |
| partial_observability_no_coord | no_exact_coordinates | 50 | 3.00 | 0.671 | 0.527 | consensus+info | 0.316 [0.271, 0.360] | `results/partial_observability_api50_candidate_eval_records.jsonl` |

## Method Details

| Run | Method | Success | Minus random | 95% CI |
|---|---|---:|---:|---|
| mixed_50_full | direct | 0.840 | -0.025 | [-0.082, 0.028] |
| mixed_50_full | shortest | 0.740 | -0.125 | [-0.192, -0.062] |
| mixed_50_full | mirror | 0.907 | 0.042 | [-0.018, 0.103] |
| mixed_50_full | population | 1.000 | 0.135 | [0.078, 0.193] |
| mixed_50_full | oracle | 1.000 | 0.135 | [0.078, 0.193] |
| perspective_gpt54_full | direct | 0.713 | -0.002 | [-0.088, 0.078] |
| perspective_gpt54_full | shortest | 0.420 | -0.295 | [-0.382, -0.205] |
| perspective_gpt54_full | mirror | 0.813 | 0.098 | [0.000, 0.193] |
| perspective_gpt54_full | population | 1.000 | 0.285 | [0.227, 0.345] |
| perspective_gpt54_full | oracle | 1.000 | 0.285 | [0.227, 0.345] |
| perspective_gpt41_full | direct | 0.553 | -0.103 | [-0.178, -0.027] |
| perspective_gpt41_full | shortest | 0.367 | -0.290 | [-0.358, -0.222] |
| perspective_gpt41_full | mirror | 0.713 | 0.057 | [-0.027, 0.145] |
| perspective_gpt41_full | population | 1.000 | 0.343 | [0.282, 0.405] |
| perspective_gpt41_full | oracle | 1.000 | 0.343 | [0.282, 0.405] |
| partial_observability_full | direct | 0.740 | -0.013 | [-0.092, 0.060] |
| partial_observability_full | shortest | 0.313 | -0.440 | [-0.500, -0.385] |
| partial_observability_full | mirror | 0.667 | -0.087 | [-0.177, 0.005] |
| partial_observability_full | population | 1.000 | 0.247 | [0.217, 0.277] |
| partial_observability_full | oracle | 1.000 | 0.247 | [0.217, 0.277] |
| mixed_50_no_coord | direct | 0.840 | 0.020 | [-0.033, 0.073] |
| mixed_50_no_coord | shortest | 0.740 | -0.080 | [-0.133, -0.029] |
| mixed_50_no_coord | mirror | 0.787 | -0.033 | [-0.091, 0.022] |
| mixed_50_no_coord | population | 0.773 | -0.047 | [-0.111, 0.013] |
| mixed_50_no_coord | consensus+info | 0.920 | 0.100 | [0.036, 0.167] |
| mixed_50_no_coord | info prior | 0.900 | 0.080 | [0.011, 0.147] |
| mixed_50_no_coord | oracle | 0.960 | 0.140 | [0.080, 0.204] |
| perspective_gpt41_no_coord | direct | 0.553 | 0.011 | [-0.060, 0.082] |
| perspective_gpt41_no_coord | shortest | 0.367 | -0.176 | [-0.242, -0.109] |
| perspective_gpt41_no_coord | mirror | 0.580 | 0.038 | [-0.022, 0.100] |
| perspective_gpt41_no_coord | population | 0.420 | -0.122 | [-0.189, -0.056] |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 0.218 | [0.156, 0.280] |
| perspective_gpt41_no_coord | info prior | 0.760 | 0.218 | [0.156, 0.280] |
| perspective_gpt41_no_coord | oracle | 0.793 | 0.251 | [0.196, 0.304] |
| partial_observability_no_coord | direct | 0.740 | 0.069 | [-0.002, 0.138] |
| partial_observability_no_coord | shortest | 0.313 | -0.358 | [-0.416, -0.302] |
| partial_observability_no_coord | mirror | 0.607 | -0.064 | [-0.149, 0.024] |
| partial_observability_no_coord | population | 0.727 | 0.056 | [-0.029, 0.140] |
| partial_observability_no_coord | consensus+info | 0.987 | 0.316 | [0.271, 0.360] |
| partial_observability_no_coord | info prior | 0.973 | 0.302 | [0.253, 0.349] |
| partial_observability_no_coord | oracle | 1.000 | 0.329 | [0.289, 0.369] |

Interpretation: a random selector is strong when many candidates are already robust, but it remains below population-play in every full-candidate run and below consensus+info in every no-coordinate run. This supports the selector-regret interpretation: candidate generation often contains a robust message, but selecting it is still the key problem.
