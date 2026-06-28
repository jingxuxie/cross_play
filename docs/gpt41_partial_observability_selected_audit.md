# gpt-4.1-nano Selected-Message Listener Audit

This run reuses cached speaker candidates and evaluates selected messages with three held-out listener prompts.

- Scene file: `data/partial_observability_local50_scenes.jsonl`.
- Candidate file: `results/partial_observability_api50_candidates.jsonl`.
- Scenes: `50`.
- Listener calls represented: `750`.
- True same-model oracle evaluated: `False`.

## Results

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| best_of_k_shortest | 0.560 | [0.480, 0.647] | - | - | 4.0 | 0.269 |
| direct_first | 0.700 | [0.613, 0.787] | - | - | 10.0 | 0.198 |
| mirror_selfplay | 0.660 | [0.573, 0.753] | - | - | 6.5 | 0.241 |
| population_play | 1.000 | [1.000, 1.000] | - | - | 9.7 | 0.000 |
| prior_listener_oracle | 0.947 | [0.893, 0.987] | - | - | 9.3 | 0.038 |

## Paired Comparisons

| Scenario | A | B | N | Mean A | Mean B | Diff A-B | 95% CI | p_boot |
|---|---|---|---:|---:|---:|---:|---:|---:|
| overall | population_play | mirror_selfplay | 50 | 1.000 | 0.660 | 0.340 | [0.247, 0.433] | 0.0000 |
| overall | prior_listener_oracle | mirror_selfplay | 50 | 0.947 | 0.660 | 0.287 | [0.193, 0.380] | 0.0000 |
