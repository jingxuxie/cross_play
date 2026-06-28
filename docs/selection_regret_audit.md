# Selection Regret Audit

Selection regret is oracle candidate success minus method success, averaged by scene.
It separates candidate-generation failures from selector failures without making new API calls.

| Run | Method | Scenes | Method success | Oracle | Regret | 95% CI |
|---|---|---:|---:|---:|---:|---:|
| mixed_50_full | direct | 50 | 0.840 | 1.000 | 0.160 | [0.073, 0.253] |
| mixed_50_full | shortest | 50 | 0.740 | 1.000 | 0.260 | [0.147, 0.380] |
| mixed_50_full | mirror | 50 | 0.907 | 1.000 | 0.093 | [0.027, 0.173] |
| mixed_50_full | population | 50 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] |
| perspective_gpt54_full | direct | 50 | 0.713 | 1.000 | 0.287 | [0.180, 0.400] |
| perspective_gpt54_full | shortest | 50 | 0.420 | 1.000 | 0.580 | [0.453, 0.700] |
| perspective_gpt54_full | mirror | 50 | 0.813 | 1.000 | 0.187 | [0.100, 0.287] |
| perspective_gpt54_full | population | 50 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] |
| perspective_gpt41_full | direct | 50 | 0.553 | 1.000 | 0.447 | [0.333, 0.567] |
| perspective_gpt41_full | shortest | 50 | 0.367 | 1.000 | 0.633 | [0.527, 0.733] |
| perspective_gpt41_full | mirror | 50 | 0.713 | 1.000 | 0.287 | [0.193, 0.380] |
| perspective_gpt41_full | population | 50 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] |
| partial_observability_full | direct | 50 | 0.740 | 1.000 | 0.260 | [0.167, 0.360] |
| partial_observability_full | shortest | 50 | 0.313 | 1.000 | 0.687 | [0.620, 0.753] |
| partial_observability_full | mirror | 50 | 0.667 | 1.000 | 0.333 | [0.240, 0.427] |
| partial_observability_full | population | 50 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] |
| mixed_50_no_coord | direct | 50 | 0.840 | 0.960 | 0.120 | [0.047, 0.207] |
| mixed_50_no_coord | shortest | 50 | 0.740 | 0.960 | 0.220 | [0.120, 0.327] |
| mixed_50_no_coord | mirror | 50 | 0.787 | 0.960 | 0.173 | [0.080, 0.273] |
| mixed_50_no_coord | population | 50 | 0.773 | 0.960 | 0.187 | [0.093, 0.293] |
| mixed_50_no_coord | consensus+info | 50 | 0.920 | 0.960 | 0.040 | [0.000, 0.093] |
| mixed_50_no_coord | info prior | 50 | 0.900 | 0.960 | 0.060 | [0.013, 0.120] |
| perspective_gpt41_no_coord | direct | 50 | 0.553 | 0.793 | 0.240 | [0.153, 0.327] |
| perspective_gpt41_no_coord | shortest | 50 | 0.367 | 0.793 | 0.427 | [0.320, 0.533] |
| perspective_gpt41_no_coord | mirror | 50 | 0.580 | 0.793 | 0.213 | [0.133, 0.293] |
| perspective_gpt41_no_coord | population | 50 | 0.420 | 0.793 | 0.373 | [0.267, 0.480] |
| perspective_gpt41_no_coord | consensus+info | 50 | 0.760 | 0.793 | 0.033 | [0.007, 0.073] |
| perspective_gpt41_no_coord | info prior | 50 | 0.760 | 0.793 | 0.033 | [0.007, 0.073] |
| partial_observability_no_coord | direct | 50 | 0.740 | 1.000 | 0.260 | [0.167, 0.360] |
| partial_observability_no_coord | shortest | 50 | 0.313 | 1.000 | 0.687 | [0.620, 0.753] |
| partial_observability_no_coord | mirror | 50 | 0.607 | 1.000 | 0.393 | [0.293, 0.487] |
| partial_observability_no_coord | population | 50 | 0.727 | 1.000 | 0.273 | [0.180, 0.373] |
| partial_observability_no_coord | consensus+info | 50 | 0.987 | 1.000 | 0.013 | [0.000, 0.040] |
| partial_observability_no_coord | info prior | 50 | 0.973 | 1.000 | 0.027 | [0.000, 0.067] |

Interpretation: full-candidate population-play has zero regret in the paper-facing runs, while mirror self-play leaves nonzero oracle-achievable success on the table. In the no-coordinate ablations, consensus+info sharply reduces but does not always eliminate regret, showing that selector quality remains the bottleneck when explicit coordinate fallbacks are removed.
