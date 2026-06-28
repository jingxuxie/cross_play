# Candidate Filter Ablation

Filter: `no_exact_coordinates`.

- Scenes: `50` total, `0` skipped.
- Candidates: `150` kept, `50` excluded.

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.740 | [0.627, 0.853] | - | - | 4.3 | 0.000 |
| no_coord_consensus_info | 0.920 | [0.847, 0.980] | - | - | 9.4 | 0.000 |
| no_coord_direct_first | 0.840 | [0.747, 0.920] | - | - | 9.3 | 0.016 |
| no_coord_informative | 0.900 | [0.820, 0.967] | - | - | 12.4 | 0.000 |
| no_coord_mirror | 0.787 | [0.680, 0.887] | 0.880 | 0.093 | 5.0 | 0.025 |
| no_coord_oracle | 0.960 | [0.913, 0.993] | - | - | 6.3 | 0.016 |
| no_coord_population | 0.773 | [0.660, 0.873] | 0.813 | 0.040 | 5.3 | 0.009 |
