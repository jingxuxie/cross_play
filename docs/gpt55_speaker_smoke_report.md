# GPT-5.5 Speaker Smoke

This bounded, cache-backed smoke test compares existing perspective-stress speaker candidates with newly generated GPT-5.5 speaker candidates on the same first 10 scenes, evaluated by GPT-5.5 held-out listener prompts.

## Key Findings

- Existing speaker direct-first success under GPT-5.5 is 0.800; GPT-5.5 speaker direct-first success is 1.000.
- Existing speaker mirror self-play success under GPT-5.5 is 0.667; GPT-5.5 speaker mirror self-play is 0.867.
- Population-play and oracle are 1.000/1.000 for existing candidates and 1.000/1.000 for GPT-5.5 candidates.
- Interpretation: stronger speaker generation improves the first candidate in this small sample, but mirror selection still leaves a same-play/cross-play gap; population selection remains robust.

## Method Summary

| Source | Method | Success | 95% CI | Same-play | Gap | Failure scenes | Mean tokens |
|---|---|---:|---:|---:|---:|---:|---:|
| existing_gpt54_speaker | api_direct_first | 0.800 | [0.600, 1.000] | - | - | 3 | 11.3 |
| existing_gpt54_speaker | api_best_of_k_shortest | 0.500 | [0.400, 0.600] | - | - | 10 | 4.8 |
| existing_gpt54_speaker | hybrid_local_mirror_api_eval | 0.667 | [0.467, 0.867] | 1.000 | 0.333 | 5 | 7.7 |
| existing_gpt54_speaker | hybrid_local_population_api_eval | 1.000 | [1.000, 1.000] | 1.000 | 0.000 | 0 | 11.0 |
| existing_gpt54_speaker | oracle_upper_bound | 1.000 | [1.000, 1.000] | - | - | 0 | 10.5 |
| existing_gpt54_speaker | template | 1.000 | [1.000, 1.000] | - | - | 0 | 10.0 |
| gpt55_speaker | api_direct_first | 1.000 | [1.000, 1.000] | - | - | 0 | 12.9 |
| gpt55_speaker | api_best_of_k_shortest | 0.833 | [0.633, 0.967] | - | - | 3 | 6.7 |
| gpt55_speaker | hybrid_local_mirror_api_eval | 0.867 | [0.667, 1.000] | 1.000 | 0.133 | 2 | 7.6 |
| gpt55_speaker | hybrid_local_population_api_eval | 1.000 | [1.000, 1.000] | 1.000 | 0.000 | 0 | 9.5 |
| gpt55_speaker | oracle_upper_bound | 1.000 | [1.000, 1.000] | - | - | 0 | 8.2 |
| gpt55_speaker | template | 1.000 | [1.000, 1.000] | - | - | 0 | 10.0 |

## Candidate Budget

| Source | K | Oracle@K | Robust-scene rate |
|---|---:|---:|---:|
| existing_gpt54_speaker | 1 | 0.800 | 0.700 |
| existing_gpt54_speaker | 2 | 0.800 | 0.700 |
| existing_gpt54_speaker | 3 | 1.000 | 1.000 |
| existing_gpt54_speaker | 4 | 1.000 | 1.000 |
| gpt55_speaker | 1 | 1.000 | 1.000 |
| gpt55_speaker | 2 | 1.000 | 1.000 |
| gpt55_speaker | 3 | 1.000 | 1.000 |
| gpt55_speaker | 4 | 1.000 | 1.000 |

## Candidate Roles

| Source | Role | Mean tokens | Coordinate rate | Left/right rate |
|---|---|---:|---:|---:|
| existing_gpt54_speaker | natural_first | 11.3 | 0.000 | 0.700 |
| existing_gpt54_speaker | attribute_short | 4.8 | 0.000 | 0.000 |
| existing_gpt54_speaker | relational_or_spatial | 11.8 | 0.000 | 1.000 |
| existing_gpt54_speaker | coordinate_fallback | 11.0 | 1.000 | 0.000 |
| gpt55_speaker | natural_first | 12.9 | 0.000 | 1.000 |
| gpt55_speaker | attribute_short | 6.7 | 0.000 | 0.600 |
| gpt55_speaker | relational_or_spatial | 10.9 | 0.000 | 1.000 |
| gpt55_speaker | coordinate_fallback | 9.5 | 1.000 | 0.000 |

## 50-Scene Speaker Audit

A full continuation extends the GPT-5.5 speaker run to all 50 perspective-stress scenes. It keeps the same candidate-generation prompt, listener prompts, and local selection procedures.

| Scenes | Direct | Shortest | Mirror | Mirror same-play | Mirror gap | Population | Oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 | 0.993 | 0.800 | 0.853 | 1.000 | 0.147 | 1.000 | 1.000 |

| K | Oracle@K | Robust-scene rate |
|---:|---:|---:|
| 1 | 0.993 | 0.980 |
| 2 | 1.000 | 1.000 |
| 3 | 1.000 | 1.000 |
| 4 | 1.000 | 1.000 |

Budget note: the 50-scene extension has 50 total speaker rows, 30 uncached speaker calls, 42472 recorded speaker tokens, and 25478 uncached speaker tokens. Earlier scenes reused the prior cache where available.

Interpretation: on 50 scenes, GPT-5.5 direct-first is 0.993 and mirror self-play is 0.853 despite same-play 1.000; population-play remains 1.000. This supports the speaker-generation result at the planned perspective-stress scale.

## Budget Note

The GPT-5.5 speaker run made 10 uncached speaker calls over 10 scenes, using 8485 recorded speaker tokens. Listener calls were cache-backed where identical selected-message evaluations already existed; missing candidate evaluations were cached under `data/cached_responses/`.

The same-scene table remains a smoke comparison; the extension section is the current paper-facing Experiment 3 speaker result when it has 50 scenes.
