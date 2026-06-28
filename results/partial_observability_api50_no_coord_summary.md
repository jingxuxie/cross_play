# Candidate Filter Ablation

Filter: `no_exact_coordinates`.

- Scenes: `50` total, `0` skipped.
- Candidates: `150` kept, `50` excluded.

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.313 | [0.247, 0.380] | - | - | 4.0 | 0.146 |
| no_coord_consensus_info | 0.987 | [0.960, 1.000] | - | - | 12.8 | 0.009 |
| no_coord_direct_first | 0.740 | [0.647, 0.833] | - | - | 10.0 | 0.113 |
| no_coord_informative | 0.973 | [0.933, 1.000] | - | - | 12.9 | 0.019 |
| no_coord_mirror | 0.607 | [0.520, 0.713] | 0.920 | 0.313 | 7.6 | 0.222 |
| no_coord_oracle | 1.000 | [1.000, 1.000] | - | - | 11.5 | 0.000 |
| no_coord_population | 0.727 | [0.640, 0.820] | 0.827 | 0.100 | 9.3 | 0.137 |
