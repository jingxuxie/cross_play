# Listener Confidence Audit

This cache-only audit checks whether held-out listener self-reported confidence and ambiguity flags explain selected-message failures.
A high-confidence failure is a listener row with `success=0` and confidence at least `0.8`.

| Run | Method | Rows | Success | Confidence | Ambiguity | Failure confidence | High-conf failure rows | High-conf failure scenes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| mixed_50_full | direct | 150 | 0.840 | 0.737 | 0.000 | 0.242 | 0.040 | 0.120 |
| mixed_50_full | shortest | 150 | 0.740 | 0.782 | 0.007 | 0.536 | 0.147 | 0.240 |
| mixed_50_full | mirror | 150 | 0.907 | 0.819 | 0.007 | 0.336 | 0.033 | 0.060 |
| mixed_50_full | population | 150 | 1.000 | 0.960 | 0.000 | - | 0.000 | 0.000 |
| perspective_gpt54_full | direct | 150 | 0.713 | 0.678 | 0.000 | 0.288 | 0.087 | 0.200 |
| perspective_gpt54_full | shortest | 150 | 0.420 | 0.665 | 0.020 | 0.618 | 0.373 | 0.640 |
| perspective_gpt54_full | mirror | 150 | 0.813 | 0.776 | 0.000 | 0.386 | 0.073 | 0.200 |
| perspective_gpt54_full | population | 150 | 1.000 | 0.999 | 0.000 | - | 0.000 | 0.000 |
| perspective_gpt41_full | direct | 150 | 0.553 | 0.837 | 0.000 | 0.803 | 0.327 | 0.520 |
| perspective_gpt41_full | shortest | 150 | 0.367 | 0.896 | 0.000 | 0.849 | 0.493 | 0.680 |
| perspective_gpt41_full | mirror | 150 | 0.713 | 0.877 | 0.000 | 0.677 | 0.147 | 0.280 |
| perspective_gpt41_full | population | 150 | 1.000 | 0.999 | 0.000 | - | 0.000 | 0.000 |
| partial_observability_full | direct | 150 | 0.740 | 0.806 | 0.033 | 0.487 | 0.127 | 0.200 |
| partial_observability_full | shortest | 150 | 0.313 | 0.616 | 0.187 | 0.570 | 0.400 | 0.600 |
| partial_observability_full | mirror | 150 | 0.667 | 0.741 | 0.140 | 0.230 | 0.073 | 0.120 |
| partial_observability_full | population | 150 | 1.000 | 0.999 | 0.000 | - | 0.000 | 0.000 |
| mixed_50_no_coord | mirror | 150 | 0.787 | 0.761 | 0.007 | 0.528 | 0.120 | 0.200 |
| mixed_50_no_coord | population | 150 | 0.773 | 0.793 | 0.007 | 0.585 | 0.140 | 0.220 |
| mixed_50_no_coord | consensus+info | 150 | 0.920 | 0.782 | 0.000 | 0.233 | 0.020 | 0.020 |
| mixed_50_no_coord | info prior | 150 | 0.900 | 0.727 | 0.000 | 0.253 | 0.027 | 0.040 |
| perspective_gpt41_no_coord | mirror | 150 | 0.580 | 0.835 | 0.000 | 0.771 | 0.280 | 0.480 |
| perspective_gpt41_no_coord | population | 150 | 0.420 | 0.883 | 0.000 | 0.836 | 0.440 | 0.640 |
| perspective_gpt41_no_coord | consensus+info | 150 | 0.760 | 0.869 | 0.000 | 0.878 | 0.200 | 0.360 |
| perspective_gpt41_no_coord | info prior | 150 | 0.760 | 0.869 | 0.000 | 0.878 | 0.200 | 0.360 |
| partial_observability_no_coord | mirror | 150 | 0.607 | 0.700 | 0.147 | 0.339 | 0.133 | 0.200 |
| partial_observability_no_coord | population | 150 | 0.727 | 0.776 | 0.087 | 0.368 | 0.100 | 0.140 |
| partial_observability_no_coord | consensus+info | 150 | 0.987 | 0.889 | 0.000 | 0.000 | 0.000 | 0.000 |
| partial_observability_no_coord | info prior | 150 | 0.973 | 0.880 | 0.000 | 0.000 | 0.000 | 0.000 |

Interpretation: listener self-reports are not a substitute for cross-play evaluation. In the alternate-model perspective runs, ambiguity flags are `0.000`, yet mirror self-play still produces high-confidence failures in `0.147` of full-candidate listener rows and `0.280` of no-coordinate listener rows. Full-candidate population-play has no held-out failures in these caches, so its high-confidence failure rate is `0.000`; in the no-coordinate perspective audit, consensus+info reduces but does not eliminate overconfident failures.
