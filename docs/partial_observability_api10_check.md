# Partial-Observability API Pilot

Exploratory 10-scene API stress check for private-landmark scenes. This is a support artifact, not a main paper claim.

Scenes: 10.

## Main Results

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| api_best_of_k_shortest | 0.233 | [0.100, 0.367] | - | - | 4.2 | 0.125 |
| api_direct_first | 0.567 | [0.333, 0.800] | - | - | 8.8 | 0.094 |
| hybrid_local_mirror_api_eval | 0.733 | [0.533, 0.933] | 1.000 | 0.267 | 7.6 | 0.189 |
| hybrid_local_population_api_eval | 1.000 | [1.000, 1.000] | 1.000 | 0.000 | 9.6 | 0.000 |
| oracle_upper_bound | 1.000 | [1.000, 1.000] | - | - | 9.6 | 0.000 |
| template | 1.000 | [1.000, 1.000] | - | - | 10.0 | 0.000 |

Population minus mirror:
- n pairs: 10
- diff: 0.267
- 95% CI: [0.067, 0.467]
- paired bootstrap p: 0.0108

## No-Coordinate Ablation

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.233 | [0.100, 0.367] | - | - | 4.2 | 0.125 |
| no_coord_consensus_info | 1.000 | [1.000, 1.000] | - | - | 13.0 | 0.000 |
| no_coord_direct_first | 0.567 | [0.333, 0.800] | - | - | 8.8 | 0.094 |
| no_coord_informative | 1.000 | [1.000, 1.000] | - | - | 13.1 | 0.000 |
| no_coord_mirror | 0.533 | [0.333, 0.733] | 0.700 | 0.167 | 6.9 | 0.125 |
| no_coord_oracle | 1.000 | [1.000, 1.000] | - | - | 12.6 | 0.000 |
| no_coord_population | 0.600 | [0.367, 0.833] | 0.700 | 0.100 | 7.9 | 0.082 |

Consensus+info minus mirror after removing exact row/column candidates:
- n pairs: 10
- diff: 0.467
- 95% CI: [0.267, 0.667]
- paired bootstrap p: 0.0000

## Message Audit

- Generated candidate messages: 40.
- Exact-coordinate candidates: 10.
- Candidate messages referencing private landmarks: 0.
- Mirror selected private-landmark references: 0.
- Population selected private-landmark references: 0.
- Mirror selected exact-coordinate messages: 6.
- Population selected exact-coordinate messages: 10.

## Mirror Failure Examples

- `po_000005`: 1/3 held-out listeners succeed; message: "Small green sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.
- `po_000023`: 1/3 held-out listeners succeed; message: "It’s a small blue sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.
- `po_000027`: 1/3 held-out listeners succeed; message: "It’s a large red cylinder."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.
- `po_000031`: 1/3 held-out listeners succeed; message: "It’s a small green sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.

Interpretation: the prompt mostly prevents explicit private-landmark references in this small run. The residual failures are under-specification failures: mirror self-play sometimes accepts short attribute-only descriptions that fit both the target and distractor, while population/consensus selection favors row/column or informative visible relations.
