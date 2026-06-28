# gpt-5.5 Selected-Message Listener Audit

This run reuses cached speaker candidates and evaluates selected messages with three held-out listener prompts.

- Scene file: `data/perspective_stress50_scenes.jsonl`.
- Candidate file: `results/perspective_stress50_hybrid_candidates.jsonl`.
- Scenes: `50`.
- Listener calls represented: `750`.
- True same-model oracle evaluated: `False`.

## Results

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| best_of_k_shortest | 0.507 | [0.460, 0.553] | - | - | 4.6 | 0.019 |
| direct_first | 0.793 | [0.713, 0.873] | - | - | 11.7 | 0.047 |
| mirror_selfplay | 0.673 | [0.580, 0.773] | - | - | 7.4 | 0.217 |
| population_play | 1.000 | [1.000, 1.000] | - | - | 10.2 | 0.000 |
| prior_listener_oracle | 0.893 | [0.827, 0.947] | - | - | 9.2 | 0.019 |

## Paired Comparisons

| Scenario | A | B | N | Mean A | Mean B | Diff A-B | 95% CI | p_boot |
|---|---|---|---:|---:|---:|---:|---:|---:|
| overall | population_play | mirror_selfplay | 50 | 1.000 | 0.673 | 0.327 | [0.233, 0.420] | 0.0000 |
| overall | prior_listener_oracle | mirror_selfplay | 50 | 0.893 | 0.673 | 0.220 | [0.113, 0.327] | 0.0000 |
