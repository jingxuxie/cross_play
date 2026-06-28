# Listener Disagreement Audit

This cache-only audit summarizes held-out listener agreement for each selected message.
A split outcome means the selected message succeeds for some held-out listeners but fails for others in the same scene.

| Run | Method | Scenes | Success | Unanimous success | Split outcome | Unanimous failure | Choice disagreement | Confidence |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| mixed_50_full | direct | 50 | 0.840 | 0.780 | 0.120 | 0.100 | 0.120 | 0.737 |
| mixed_50_full | shortest | 50 | 0.740 | 0.700 | 0.080 | 0.220 | 0.080 | 0.782 |
| mixed_50_full | mirror | 50 | 0.907 | 0.860 | 0.080 | 0.060 | 0.080 | 0.819 |
| mixed_50_full | population | 50 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.960 |
| perspective_gpt54_full | direct | 50 | 0.713 | 0.600 | 0.180 | 0.220 | 0.180 | 0.678 |
| perspective_gpt54_full | shortest | 50 | 0.420 | 0.300 | 0.220 | 0.480 | 0.240 | 0.665 |
| perspective_gpt54_full | mirror | 50 | 0.813 | 0.720 | 0.180 | 0.100 | 0.180 | 0.776 |
| perspective_gpt54_full | population | 50 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.999 |
| perspective_gpt41_full | direct | 50 | 0.553 | 0.380 | 0.360 | 0.260 | 0.380 | 0.837 |
| perspective_gpt41_full | shortest | 50 | 0.367 | 0.180 | 0.420 | 0.400 | 0.440 | 0.896 |
| perspective_gpt41_full | mirror | 50 | 0.713 | 0.560 | 0.360 | 0.080 | 0.360 | 0.877 |
| perspective_gpt41_full | population | 50 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.999 |
| partial_observability_full | direct | 50 | 0.740 | 0.620 | 0.320 | 0.060 | 0.320 | 0.806 |
| partial_observability_full | shortest | 50 | 0.313 | 0.020 | 0.700 | 0.280 | 0.700 | 0.616 |
| partial_observability_full | mirror | 50 | 0.667 | 0.500 | 0.500 | 0.000 | 0.500 | 0.741 |
| partial_observability_full | population | 50 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.999 |
| mixed_50_no_coord | mirror | 50 | 0.787 | 0.720 | 0.120 | 0.160 | 0.120 | 0.761 |
| mixed_50_no_coord | population | 50 | 0.773 | 0.740 | 0.060 | 0.200 | 0.060 | 0.793 |
| mixed_50_no_coord | consensus+info | 50 | 0.920 | 0.880 | 0.080 | 0.040 | 0.080 | 0.782 |
| mixed_50_no_coord | info prior | 50 | 0.900 | 0.840 | 0.120 | 0.040 | 0.120 | 0.727 |
| perspective_gpt41_no_coord | mirror | 50 | 0.580 | 0.360 | 0.460 | 0.180 | 0.460 | 0.835 |
| perspective_gpt41_no_coord | population | 50 | 0.420 | 0.220 | 0.440 | 0.340 | 0.460 | 0.883 |
| perspective_gpt41_no_coord | consensus+info | 50 | 0.760 | 0.620 | 0.260 | 0.120 | 0.260 | 0.869 |
| perspective_gpt41_no_coord | info prior | 50 | 0.760 | 0.620 | 0.260 | 0.120 | 0.260 | 0.869 |
| partial_observability_no_coord | mirror | 50 | 0.607 | 0.420 | 0.540 | 0.040 | 0.540 | 0.700 |
| partial_observability_no_coord | population | 50 | 0.727 | 0.600 | 0.360 | 0.040 | 0.360 | 0.776 |
| partial_observability_no_coord | consensus+info | 50 | 0.987 | 0.980 | 0.020 | 0.000 | 0.020 | 0.889 |
| partial_observability_no_coord | info prior | 50 | 0.973 | 0.960 | 0.040 | 0.000 | 0.040 | 0.880 |

Interpretation: mirror-selected messages often produce split held-out listener outcomes in the harder audits, while full-candidate population-play produces unanimous success in all scenes. No-coordinate consensus+info sharply reduces split outcomes relative to mirror self-play.
