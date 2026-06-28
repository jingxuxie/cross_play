# Partial-Observability API Pilot

Bounded 50-scene API stress check for private-landmark scenes.

Scenes: 50.

## Main Results

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| api_best_of_k_shortest | 0.313 | [0.247, 0.380] | - | - | 4.0 | 0.146 |
| api_direct_first | 0.740 | [0.647, 0.833] | - | - | 10.0 | 0.113 |
| hybrid_local_mirror_api_eval | 0.667 | [0.573, 0.760] | 1.000 | 0.333 | 6.5 | 0.236 |
| hybrid_local_population_api_eval | 1.000 | [1.000, 1.000] | 1.000 | 0.000 | 9.7 | 0.000 |
| oracle_upper_bound | 1.000 | [1.000, 1.000] | - | - | 9.3 | 0.000 |
| template | 1.000 | [1.000, 1.000] | - | - | 10.0 | 0.000 |

Population minus mirror:
- n pairs: 50
- diff: 0.333
- 95% CI: [0.240, 0.427]
- paired bootstrap p: 0.0000

## No-Coordinate Ablation

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| no_coord_best_of_k_shortest | 0.313 | [0.247, 0.380] | - | - | 4.0 | 0.146 |
| no_coord_consensus_info | 0.987 | [0.960, 1.000] | - | - | 12.8 | 0.009 |
| no_coord_direct_first | 0.740 | [0.647, 0.833] | - | - | 10.0 | 0.113 |
| no_coord_informative | 0.973 | [0.933, 1.000] | - | - | 12.9 | 0.019 |
| no_coord_mirror | 0.607 | [0.520, 0.713] | 0.920 | 0.313 | 7.6 | 0.222 |
| no_coord_oracle | 1.000 | [1.000, 1.000] | - | - | 11.5 | 0.000 |
| no_coord_population | 0.727 | [0.640, 0.820] | 0.827 | 0.100 | 9.3 | 0.137 |

Consensus+info minus mirror after removing exact row/column candidates:
- n pairs: 50
- diff: 0.380
- 95% CI: [0.280, 0.473]
- paired bootstrap p: 0.0000

## Message Audit

- Generated candidate messages: 200.
- Exact-coordinate candidates: 50.
- Candidate messages referencing private landmarks: 0.
- Mirror selected private-landmark references: 0.
- Population selected private-landmark references: 0.
- Mirror selected exact-coordinate messages: 24.
- Population selected exact-coordinate messages: 50.

## Coded Mirror Failure Categories

Source: `results/partial_observability_api50_mirror_failures_coded.csv`.

| Rubric category | Count |
|---|---:|
| underspecified_distractor | 50 |

No-coordinate mirror failures:

Source: `results/partial_observability_api50_no_coord_mirror_failures_coded.csv`.

| Rubric category | Count |
|---|---:|
| underspecified_distractor | 59 |

## Mirror Failure Examples

- `po_000000`: 1/3 held-out listeners succeed; message: "Large red sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.
- `po_000004`: 1/3 held-out listeners succeed; message: "Large red sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.
- `po_000005`: 1/3 held-out listeners succeed; message: "Small green sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.
- `po_000006`: 1/3 held-out listeners succeed; message: "Large yellow sphere."; failed listeners: L_test_direct_last_api, L_test_strict_last_api; choices: obj_2, obj_2.

Interpretation: the prompt mostly prevents explicit private-landmark references in this run. The residual failures are under-specification failures: mirror self-play sometimes accepts short attribute-only descriptions that fit both the target and distractor, while population/consensus selection favors row/column or informative visible relations. The coded mirror-failure files support this interpretation: all coded full-run mirror failures and all coded no-coordinate mirror failures are underspecified-distractor choices.
