# Local Stronger-Plan K=8 Diagnostic

This generated no-API diagnostic exercises the stronger-plan scale locally: 1,000 initial-family scenes plus 200 partial-observability stress scenes.
It is artifact support for scale and K=8 candidate diversity, not a replacement for the cached API listener results in the paper.

Scene file: `data/local_stronger_plan1200_scenes.jsonl`
Seed: `20260628`

## Dataset

| Scenario type | Scenes |
|---|---:|
| distractor_contrast | 250 |
| partial_observability | 200 |
| perspective_shift | 250 |
| relational_reference | 250 |
| unique_attribute | 250 |

## Key Observations

- No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8.
- No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8.
- At K=8 without exact coordinates, consensus+info reaches 0.992 on the initial 1,000 scenes and 0.997 on partial-observability scenes.
- Full-candidate local K=8 population-play reaches 1.000 over all 1,200 scenes.

## Candidate Budget

| Scope | Filter | K | Scenes | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle success |
|---|---|---:|---:|---:|---:|---:|---:|
| initial_1000 | full | 1 | 1000 | 1.000 | 0.250 | 0.250 | 0.502 |
| initial_1000 | full | 4 | 1000 | 4.000 | 2.736 | 1.000 | 1.000 |
| initial_1000 | full | 8 | 1000 | 8.000 | 6.612 | 1.000 | 1.000 |
| initial_1000 | no_exact_coordinates | 1 | 1000 | 1.000 | 0.250 | 0.250 | 0.502 |
| initial_1000 | no_exact_coordinates | 4 | 1000 | 2.750 | 1.486 | 0.736 | 0.870 |
| initial_1000 | no_exact_coordinates | 8 | 1000 | 6.750 | 5.362 | 0.989 | 0.995 |
| partial_200 | full | 1 | 200 | 1.000 | 0.000 | 0.000 | 0.487 |
| partial_200 | full | 4 | 200 | 4.000 | 1.000 | 1.000 | 1.000 |
| partial_200 | full | 8 | 200 | 8.000 | 4.935 | 1.000 | 1.000 |
| partial_200 | no_exact_coordinates | 1 | 200 | 1.000 | 0.000 | 0.000 | 0.487 |
| partial_200 | no_exact_coordinates | 4 | 200 | 3.000 | 0.000 | 0.000 | 0.495 |
| partial_200 | no_exact_coordinates | 8 | 200 | 7.000 | 3.935 | 0.995 | 0.997 |
| combined_1200 | full | 1 | 1200 | 1.000 | 0.208 | 0.208 | 0.499 |
| combined_1200 | full | 4 | 1200 | 4.000 | 2.447 | 1.000 | 1.000 |
| combined_1200 | full | 8 | 1200 | 8.000 | 6.332 | 1.000 | 1.000 |
| combined_1200 | no_exact_coordinates | 1 | 1200 | 1.000 | 0.208 | 0.208 | 0.499 |
| combined_1200 | no_exact_coordinates | 4 | 1200 | 2.792 | 1.238 | 0.613 | 0.808 |
| combined_1200 | no_exact_coordinates | 8 | 1200 | 6.792 | 5.124 | 0.990 | 0.995 |

## Selector Summary

| Scope | Filter | K | Method | Success | Same-play | Gap | Exact-coordinate selection | Tokens |
|---|---|---:|---|---:|---:|---:|---:|---:|
| initial_1000 | full | 4 | Mirror | 0.628 | 1.000 | 0.372 | 0.004 | 5.368 |
| initial_1000 | full | 4 | Population | 1.000 | 1.000 | 0.000 | 0.264 | 7.250 |
| initial_1000 | full | 4 | Consensus+info | 1.000 | - | - | 0.264 | 9.750 |
| initial_1000 | full | 4 | Oracle | 1.000 | - | - | 0.399 | 7.250 |
| initial_1000 | full | 8 | Mirror | 0.628 | 1.000 | 0.372 | 0.004 | 5.234 |
| initial_1000 | full | 8 | Population | 1.000 | 1.000 | 0.000 | 0.190 | 6.940 |
| initial_1000 | full | 8 | Consensus+info | 1.000 | - | - | 0.166 | 8.667 |
| initial_1000 | full | 8 | Oracle | 1.000 | - | - | 0.021 | 6.528 |
| initial_1000 | no_exact_coordinates | 4 | Mirror | 0.626 | 0.996 | 0.370 | 0.000 | 5.344 |
| initial_1000 | no_exact_coordinates | 4 | Population | 0.870 | 0.864 | -0.006 | 0.000 | 5.666 |
| initial_1000 | no_exact_coordinates | 4 | Consensus+info | 0.741 | - | - | 0.000 | 8.250 |
| initial_1000 | no_exact_coordinates | 4 | Oracle | 0.870 | - | - | 0.000 | 5.666 |
| initial_1000 | no_exact_coordinates | 8 | Mirror | 0.626 | 0.996 | 0.370 | 0.000 | 5.210 |
| initial_1000 | no_exact_coordinates | 8 | Population | 0.981 | 0.942 | -0.039 | 0.000 | 6.482 |
| initial_1000 | no_exact_coordinates | 8 | Consensus+info | 0.992 | - | - | 0.000 | 8.197 |
| initial_1000 | no_exact_coordinates | 8 | Oracle | 0.995 | - | - | 0.000 | 6.462 |
| partial_200 | full | 4 | Mirror | 0.657 | 1.000 | 0.343 | 0.485 | 7.425 |
| partial_200 | full | 4 | Population | 1.000 | 1.000 | 0.000 | 1.000 | 10.000 |
| partial_200 | full | 4 | Consensus+info | 1.000 | - | - | 1.000 | 10.000 |
| partial_200 | full | 4 | Oracle | 1.000 | - | - | 1.000 | 10.000 |
| partial_200 | full | 8 | Mirror | 0.657 | 1.000 | 0.343 | 0.005 | 6.465 |
| partial_200 | full | 8 | Population | 1.000 | 1.000 | 0.000 | 0.020 | 8.040 |
| partial_200 | full | 8 | Consensus+info | 1.000 | - | - | 0.005 | 8.040 |
| partial_200 | full | 8 | Oracle | 1.000 | - | - | 0.020 | 8.040 |
| partial_200 | no_exact_coordinates | 4 | Mirror | 0.495 | 0.515 | 0.020 | 0.000 | 5.000 |
| partial_200 | no_exact_coordinates | 4 | Population | 0.495 | 0.505 | 0.010 | 0.000 | 5.000 |
| partial_200 | no_exact_coordinates | 4 | Consensus+info | 0.487 | - | - | 0.000 | 9.000 |
| partial_200 | no_exact_coordinates | 4 | Oracle | 0.495 | - | - | 0.000 | 5.000 |
| partial_200 | no_exact_coordinates | 8 | Mirror | 0.657 | 1.000 | 0.343 | 0.000 | 6.465 |
| partial_200 | no_exact_coordinates | 8 | Population | 0.997 | 0.998 | 0.002 | 0.000 | 8.015 |
| partial_200 | no_exact_coordinates | 8 | Consensus+info | 0.997 | - | - | 0.000 | 8.040 |
| partial_200 | no_exact_coordinates | 8 | Oracle | 0.997 | - | - | 0.000 | 8.015 |
| combined_1200 | full | 4 | Mirror | 0.632 | 1.000 | 0.368 | 0.084 | 5.711 |
| combined_1200 | full | 4 | Population | 1.000 | 1.000 | 0.000 | 0.387 | 7.708 |
| combined_1200 | full | 4 | Consensus+info | 1.000 | - | - | 0.387 | 9.792 |
| combined_1200 | full | 4 | Oracle | 1.000 | - | - | 0.499 | 7.708 |
| combined_1200 | full | 8 | Mirror | 0.632 | 1.000 | 0.368 | 0.004 | 5.439 |
| combined_1200 | full | 8 | Population | 1.000 | 1.000 | 0.000 | 0.162 | 7.123 |
| combined_1200 | full | 8 | Consensus+info | 1.000 | - | - | 0.139 | 8.562 |
| combined_1200 | full | 8 | Oracle | 1.000 | - | - | 0.021 | 6.780 |
| combined_1200 | no_exact_coordinates | 4 | Mirror | 0.604 | 0.916 | 0.311 | 0.000 | 5.287 |
| combined_1200 | no_exact_coordinates | 4 | Population | 0.808 | 0.804 | -0.003 | 0.000 | 5.555 |
| combined_1200 | no_exact_coordinates | 4 | Consensus+info | 0.699 | - | - | 0.000 | 8.375 |
| combined_1200 | no_exact_coordinates | 4 | Oracle | 0.808 | - | - | 0.000 | 5.555 |
| combined_1200 | no_exact_coordinates | 8 | Mirror | 0.631 | 0.997 | 0.365 | 0.000 | 5.419 |
| combined_1200 | no_exact_coordinates | 8 | Population | 0.984 | 0.952 | -0.032 | 0.000 | 6.737 |
| combined_1200 | no_exact_coordinates | 8 | Consensus+info | 0.993 | - | - | 0.000 | 8.171 |
| combined_1200 | no_exact_coordinates | 8 | Oracle | 0.995 | - | - | 0.000 | 6.721 |

## Interpretation

The local diagnostic supports two bounded stronger-plan conclusions: the released generator runs at the 1,000+200 scale, and K=8 can add useful non-coordinate candidate diversity after the original four slots.
The result should stay scoped as local evidence because the paper-facing listener claims still come from cached API runs.
