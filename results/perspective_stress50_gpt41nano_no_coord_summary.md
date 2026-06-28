# Candidate Filter Ablation

Filter: `no_exact_coordinates`.

- Scenes: `50` total, `0` skipped.
- Candidates: `150` kept, `50` excluded.

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.367 | [0.260, 0.473] | - | - | 4.6 | 0.109 |
| no_coord_consensus_info | 0.760 | [0.653, 0.853] | - | - | 12.5 | 0.043 |
| no_coord_direct_first | 0.553 | [0.440, 0.673] | - | - | 11.7 | 0.019 |
| no_coord_informative | 0.760 | [0.653, 0.853] | - | - | 12.5 | 0.043 |
| no_coord_mirror | 0.580 | [0.467, 0.680] | 1.000 | 0.420 | 8.3 | 0.071 |
| no_coord_oracle | 0.793 | [0.693, 0.873] | - | - | 9.4 | 0.009 |
| no_coord_population | 0.420 | [0.307, 0.527] | 0.520 | 0.100 | 5.0 | 0.099 |
