# Candidate Pool Robustness Audit

This cache-only audit asks whether robust held-out candidates were available and whether each selector chose one.
A robust candidate succeeds with every held-out API listener for that scene.

## Candidate Availability

| Run | Filter | Scenes | Candidates/scene | Robust candidates/scene | Scenes with robust candidate | Oracle success |
|---|---|---:|---:|---:|---:|---:|
| mixed_50_full | full | 50 | 4.00 | 3.30 | 1.000 | 1.000 |
| perspective_gpt54_full | full | 50 | 4.00 | 2.44 | 1.000 | 1.000 |
| perspective_gpt41_full | full | 50 | 4.00 | 2.14 | 1.000 | 1.000 |
| partial_observability_full | full | 50 | 4.00 | 2.58 | 1.000 | 1.000 |
| mixed_50_no_coord | no_exact_coordinates | 50 | 3.00 | 2.30 | 0.920 | 0.960 |
| perspective_gpt41_no_coord | no_exact_coordinates | 50 | 3.00 | 1.14 | 0.660 | 0.793 |
| partial_observability_no_coord | no_exact_coordinates | 50 | 3.00 | 1.58 | 1.000 | 1.000 |

## Selector Capture

| Run | Method | Selected success | Selected robust rate | Oracle-match rate |
|---|---|---:|---:|---:|
| mixed_50_full | direct | 0.840 | 0.780 | 0.780 |
| mixed_50_full | shortest | 0.740 | 0.700 | 0.700 |
| mixed_50_full | mirror | 0.907 | 0.860 | 0.860 |
| mixed_50_full | population | 1.000 | 1.000 | 1.000 |
| perspective_gpt54_full | direct | 0.713 | 0.600 | 0.600 |
| perspective_gpt54_full | shortest | 0.420 | 0.300 | 0.300 |
| perspective_gpt54_full | mirror | 0.813 | 0.720 | 0.720 |
| perspective_gpt54_full | population | 1.000 | 1.000 | 1.000 |
| perspective_gpt41_full | direct | 0.553 | 0.380 | 0.380 |
| perspective_gpt41_full | shortest | 0.367 | 0.180 | 0.180 |
| perspective_gpt41_full | mirror | 0.713 | 0.560 | 0.560 |
| perspective_gpt41_full | population | 1.000 | 1.000 | 1.000 |
| partial_observability_full | direct | 0.740 | 0.620 | 0.620 |
| partial_observability_full | shortest | 0.313 | 0.020 | 0.020 |
| partial_observability_full | mirror | 0.667 | 0.500 | 0.500 |
| partial_observability_full | population | 1.000 | 1.000 | 1.000 |
| mixed_50_no_coord | direct | 0.840 | 0.780 | 0.840 |
| mixed_50_no_coord | shortest | 0.740 | 0.700 | 0.720 |
| mixed_50_no_coord | mirror | 0.787 | 0.720 | 0.780 |
| mixed_50_no_coord | population | 0.773 | 0.740 | 0.760 |
| mixed_50_no_coord | consensus+info | 0.920 | 0.880 | 0.940 |
| mixed_50_no_coord | info prior | 0.900 | 0.840 | 0.900 |
| perspective_gpt41_no_coord | direct | 0.553 | 0.380 | 0.580 |
| perspective_gpt41_no_coord | shortest | 0.367 | 0.180 | 0.360 |
| perspective_gpt41_no_coord | mirror | 0.580 | 0.360 | 0.580 |
| perspective_gpt41_no_coord | population | 0.420 | 0.220 | 0.420 |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 0.620 | 0.920 |
| perspective_gpt41_no_coord | info prior | 0.760 | 0.620 | 0.920 |
| partial_observability_no_coord | direct | 0.740 | 0.620 | 0.620 |
| partial_observability_no_coord | shortest | 0.313 | 0.020 | 0.020 |
| partial_observability_no_coord | mirror | 0.607 | 0.420 | 0.420 |
| partial_observability_no_coord | population | 0.727 | 0.600 | 0.600 |
| partial_observability_no_coord | consensus+info | 0.987 | 0.980 | 0.980 |
| partial_observability_no_coord | info prior | 0.973 | 0.960 | 0.960 |

Interpretation: the full-candidate runs usually contain all-listener-robust messages, and population-play consistently selects them. After exact-coordinate candidates are removed, robust non-coordinate candidates become less available in the alternate-model perspective audit, but consensus+info captures most of the remaining oracle success.
