# Candidate Filter Ablation

Filter: `no_exact_coordinates`.

- Scenes: `10` total, `0` skipped.
- Candidates: `30` kept, `10` excluded.

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.233 | [0.100, 0.367] | - | - | 4.2 | 0.125 |
| no_coord_consensus_info | 1.000 | [1.000, 1.000] | - | - | 13.0 | 0.000 |
| no_coord_direct_first | 0.567 | [0.333, 0.800] | - | - | 8.8 | 0.094 |
| no_coord_informative | 1.000 | [1.000, 1.000] | - | - | 13.1 | 0.000 |
| no_coord_mirror | 0.533 | [0.333, 0.733] | 0.700 | 0.167 | 6.9 | 0.125 |
| no_coord_oracle | 1.000 | [1.000, 1.000] | - | - | 12.6 | 0.000 |
| no_coord_population | 0.600 | [0.367, 0.833] | 0.700 | 0.100 | 7.9 | 0.082 |
