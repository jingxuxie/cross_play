# Candidate Budget Audit

This cache-only audit reports how quickly robust candidates appear as the generated candidate budget grows.
Oracle@K is the best held-out success among the first K candidates for a scene.
A robust candidate succeeds with every held-out API listener for that scene.

## Prefix-K Availability

| Run | K | Oracle@K | Robust-scene rate | Source |
|---|---:|---:|---:|---|
| mixed_50_full | 1 | 0.840 | 0.780 | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl` |
| mixed_50_full | 2 | 0.853 | 0.800 | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl` |
| mixed_50_full | 3 | 0.960 | 0.920 | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl` |
| mixed_50_full | 4 | 1.000 | 1.000 | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl` |
| perspective_gpt54_full | 1 | 0.713 | 0.600 | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl` |
| perspective_gpt54_full | 2 | 0.787 | 0.680 | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl` |
| perspective_gpt54_full | 3 | 0.893 | 0.820 | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl` |
| perspective_gpt54_full | 4 | 1.000 | 1.000 | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl` |
| perspective_gpt41_full | 1 | 0.553 | 0.380 | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl` |
| perspective_gpt41_full | 2 | 0.620 | 0.400 | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl` |
| perspective_gpt41_full | 3 | 0.793 | 0.660 | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl` |
| perspective_gpt41_full | 4 | 1.000 | 1.000 | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl` |
| partial_observability_full | 1 | 0.740 | 0.620 | `results/partial_observability_api50_candidate_eval_records.jsonl` |
| partial_observability_full | 2 | 0.747 | 0.620 | `results/partial_observability_api50_candidate_eval_records.jsonl` |
| partial_observability_full | 3 | 1.000 | 1.000 | `results/partial_observability_api50_candidate_eval_records.jsonl` |
| partial_observability_full | 4 | 1.000 | 1.000 | `results/partial_observability_api50_candidate_eval_records.jsonl` |

## First Robust Candidate Position

| Run | Mean first robust K | Missing robust candidate | K=1 | K=2 | K=3 | K=4 |
|---|---:|---:|---:|---:|---:|---:|
| mixed_50_full | 1.50 | 0 | 39 | 1 | 6 | 4 |
| perspective_gpt54_full | 1.90 | 0 | 30 | 4 | 7 | 9 |
| perspective_gpt41_full | 2.56 | 0 | 19 | 1 | 13 | 17 |
| partial_observability_full | 1.76 | 0 | 31 | 0 | 19 | 0 |

Interpretation: candidate 1 is often already sufficient in easier mixed scenes, but the perspective and partial-observability audits need later candidates for full robust coverage. The fourth candidate closes the robust-scene rate to 1.000 in all full-candidate runs.
