# Message Length Audit

This cache-only audit checks whether selector gains are explained by simply choosing longer messages.
Length is measured with the stored whitespace token count used in the experiment records.

## Method Lengths

| Run | Filter | Method | Scenes | Success | Mean tokens | Success/token |
|---|---|---|---:|---:|---:|---:|
| mixed_50_full | full | template | 50 | 1.000 | 10.00 | 0.100 |
| mixed_50_full | full | direct | 50 | 0.840 | 9.26 | 0.091 |
| mixed_50_full | full | shortest | 50 | 0.740 | 4.32 | 0.171 |
| mixed_50_full | full | mirror | 50 | 0.907 | 5.56 | 0.163 |
| mixed_50_full | full | population | 50 | 1.000 | 6.82 | 0.147 |
| mixed_50_full | full | oracle | 50 | 1.000 | 5.96 | 0.168 |
| perspective_gpt54_full | full | template | 50 | 1.000 | 10.00 | 0.100 |
| perspective_gpt54_full | full | direct | 50 | 0.713 | 11.70 | 0.061 |
| perspective_gpt54_full | full | shortest | 50 | 0.420 | 4.58 | 0.092 |
| perspective_gpt54_full | full | mirror | 50 | 0.813 | 7.40 | 0.110 |
| perspective_gpt54_full | full | population | 50 | 1.000 | 10.22 | 0.098 |
| perspective_gpt54_full | full | oracle | 50 | 1.000 | 8.42 | 0.119 |
| perspective_gpt41_full | full | template | 50 | 1.000 | 10.00 | 0.100 |
| perspective_gpt41_full | full | direct | 50 | 0.553 | 11.70 | 0.047 |
| perspective_gpt41_full | full | shortest | 50 | 0.367 | 4.58 | 0.080 |
| perspective_gpt41_full | full | mirror | 50 | 0.713 | 7.40 | 0.096 |
| perspective_gpt41_full | full | population | 50 | 1.000 | 10.22 | 0.098 |
| perspective_gpt41_full | full | oracle | 50 | 1.000 | 9.18 | 0.109 |
| partial_observability_full | full | template | 50 | 1.000 | 10.00 | 0.100 |
| partial_observability_full | full | direct | 50 | 0.740 | 9.96 | 0.074 |
| partial_observability_full | full | shortest | 50 | 0.313 | 4.04 | 0.078 |
| partial_observability_full | full | mirror | 50 | 0.667 | 6.50 | 0.103 |
| partial_observability_full | full | population | 50 | 1.000 | 9.66 | 0.104 |
| partial_observability_full | full | oracle | 50 | 1.000 | 9.32 | 0.107 |
| mixed_50_no_coord | no_exact_coordinates | direct | 50 | 0.840 | 9.26 | 0.091 |
| mixed_50_no_coord | no_exact_coordinates | shortest | 50 | 0.740 | 4.32 | 0.171 |
| mixed_50_no_coord | no_exact_coordinates | mirror | 50 | 0.787 | 5.00 | 0.157 |
| mixed_50_no_coord | no_exact_coordinates | population | 50 | 0.773 | 5.26 | 0.147 |
| mixed_50_no_coord | no_exact_coordinates | consensus+info | 50 | 0.920 | 9.38 | 0.098 |
| mixed_50_no_coord | no_exact_coordinates | info prior | 50 | 0.900 | 12.36 | 0.073 |
| mixed_50_no_coord | no_exact_coordinates | oracle | 50 | 0.960 | 6.28 | 0.153 |
| perspective_gpt41_no_coord | no_exact_coordinates | direct | 50 | 0.553 | 11.70 | 0.047 |
| perspective_gpt41_no_coord | no_exact_coordinates | shortest | 50 | 0.367 | 4.58 | 0.080 |
| perspective_gpt41_no_coord | no_exact_coordinates | mirror | 50 | 0.580 | 8.28 | 0.070 |
| perspective_gpt41_no_coord | no_exact_coordinates | population | 50 | 0.420 | 5.04 | 0.083 |
| perspective_gpt41_no_coord | no_exact_coordinates | consensus+info | 50 | 0.760 | 12.54 | 0.061 |
| perspective_gpt41_no_coord | no_exact_coordinates | info prior | 50 | 0.760 | 12.54 | 0.061 |
| perspective_gpt41_no_coord | no_exact_coordinates | oracle | 50 | 0.793 | 9.38 | 0.085 |
| partial_observability_no_coord | no_exact_coordinates | direct | 50 | 0.740 | 9.96 | 0.074 |
| partial_observability_no_coord | no_exact_coordinates | shortest | 50 | 0.313 | 4.04 | 0.078 |
| partial_observability_no_coord | no_exact_coordinates | mirror | 50 | 0.607 | 7.56 | 0.080 |
| partial_observability_no_coord | no_exact_coordinates | population | 50 | 0.727 | 9.32 | 0.078 |
| partial_observability_no_coord | no_exact_coordinates | consensus+info | 50 | 0.987 | 12.76 | 0.077 |
| partial_observability_no_coord | no_exact_coordinates | info prior | 50 | 0.973 | 12.86 | 0.076 |
| partial_observability_no_coord | no_exact_coordinates | oracle | 50 | 1.000 | 11.52 | 0.087 |

## Primary Selector Versus Mirror

| Run | Primary | Scenes | Success delta | Success delta 95% CI | Token delta | Token delta 95% CI |
|---|---|---:|---:|---|---:|---|
| mixed_50_full | population | 50 | 0.093 | [0.027, 0.173] | 1.26 | [0.66, 1.92] |
| perspective_gpt54_full | population | 50 | 0.187 | [0.100, 0.287] | 2.82 | [2.00, 3.66] |
| perspective_gpt41_full | population | 50 | 0.287 | [0.193, 0.380] | 2.82 | [2.00, 3.66] |
| partial_observability_full | population | 50 | 0.333 | [0.240, 0.427] | 3.16 | [2.22, 4.10] |
| mixed_50_no_coord | consensus+info | 50 | 0.133 | [0.033, 0.233] | 4.38 | [3.30, 5.52] |
| perspective_gpt41_no_coord | consensus+info | 50 | 0.180 | [0.100, 0.267] | 4.26 | [3.24, 5.28] |
| partial_observability_no_coord | consensus+info | 50 | 0.380 | [0.280, 0.473] | 5.20 | [3.98, 6.42] |

Interpretation: population-play and consensus+info often select longer messages than mirror self-play, but length alone does not explain the gains. Direct messages are longer than mirror in the perspective and partial-observability full-candidate runs while remaining less successful, and full-candidate population messages stay at or below the 10-token template scale in all but the main perspective-stress run.
