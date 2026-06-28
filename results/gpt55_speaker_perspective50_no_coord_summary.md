# Candidate Filter Ablation

Filter: `no_exact_coordinates`.

- Scenes: `50` total, `0` skipped.
- Candidates: `148` kept, `52` excluded.

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.787 | [0.713, 0.853] | - | - | 7.1 | 0.019 |
| no_coord_consensus_info | 0.993 | [0.980, 1.000] | - | - | 12.4 | 0.009 |
| no_coord_direct_first | 0.993 | [0.980, 1.000] | - | - | 12.8 | 0.009 |
| no_coord_informative | 0.993 | [0.980, 1.000] | - | - | 12.4 | 0.009 |
| no_coord_mirror | 0.847 | [0.773, 0.913] | 0.980 | 0.133 | 8.7 | 0.066 |
| no_coord_oracle | 1.000 | [1.000, 1.000] | - | - | 9.4 | 0.000 |
| no_coord_population | 0.833 | [0.760, 0.907] | 0.573 | -0.260 | 8.5 | 0.019 |
