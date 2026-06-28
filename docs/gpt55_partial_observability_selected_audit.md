# gpt-5.5 Selected-Message Listener Audit

This run reuses cached speaker candidates and evaluates selected messages with three held-out listener prompts.

- Scene file: `data/partial_observability_local50_scenes.jsonl`.
- Candidate file: `results/partial_observability_api50_candidates.jsonl`.
- Scenes: `50`.
- Listener calls represented: `750`.
- True same-model oracle evaluated: `False`.

## Results

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| best_of_k_shortest | 0.453 | [0.400, 0.507] | - | - | 4.0 | 0.047 |
| direct_first | 0.740 | [0.653, 0.827] | - | - | 10.0 | 0.113 |
| mirror_selfplay | 0.653 | [0.560, 0.747] | - | - | 6.5 | 0.245 |
| population_play | 1.000 | [1.000, 1.000] | - | - | 9.7 | 0.000 |
| prior_listener_oracle | 0.960 | [0.907, 1.000] | - | - | 9.3 | 0.028 |

## Paired Comparisons

| Scenario | A | B | N | Mean A | Mean B | Diff A-B | 95% CI | p_boot |
|---|---|---|---:|---:|---:|---:|---:|---:|
| overall | population_play | mirror_selfplay | 50 | 1.000 | 0.653 | 0.347 | [0.253, 0.440] | 0.0000 |
| overall | prior_listener_oracle | mirror_selfplay | 50 | 0.960 | 0.653 | 0.307 | [0.213, 0.400] | 0.0000 |
