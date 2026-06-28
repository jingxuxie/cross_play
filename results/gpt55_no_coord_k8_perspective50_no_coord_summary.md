# Candidate Filter Ablation

Filter: `no_exact_coordinates`.

- Scenes: `50` total, `0` skipped.
- Candidates: `400` kept, `0` excluded.

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 1.000 | [1.000, 1.000] | - | - | 4.6 | 0.000 |
| no_coord_consensus_info | 0.900 | [0.820, 0.967] | - | - | 12.9 | 0.049 |
| no_coord_direct_first | 0.973 | [0.927, 1.000] | - | - | 11.7 | 0.009 |
| no_coord_informative | 0.900 | [0.820, 0.967] | - | - | 12.9 | 0.049 |
| no_coord_mirror | 0.953 | [0.907, 0.987] | 1.000 | 0.047 | 5.0 | 0.019 |
| no_coord_oracle | 1.000 | [1.000, 1.000] | - | - | 4.6 | 0.000 |
| no_coord_population | 0.993 | [0.973, 1.000] | 0.560 | -0.433 | 6.5 | 0.009 |
