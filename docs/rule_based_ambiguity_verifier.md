# Rule-Based Ambiguity Verifier

This cache-only verifier is an independent non-LLM check on whether selected messages are objectively under-informative or frame-sensitive. It parses exact row/column mentions, target color/size/shape mentions, and left/right frame-sensitive cues, then counts compatible listener-visible objects.

## Coded Failure Alignment

| Failure set | Rows | Under-spec recall | Frame recall | Symbolic recall | Under-spec precision | Label counts |
|---|---:|---:|---:|---:|---:|---|
| perspective_alt_model_mirror | 43 | 1.000 | 1.000 | 1.000 | 1.000 | attribute_underspecified: 38, frame_sensitive_relation: 5 |
| partial_observability_mirror | 50 | 1.000 | - | 1.000 | 1.000 | attribute_underspecified: 50 |
| partial_observability_no_coord_mirror | 59 | 1.000 | - | 1.000 | 1.000 | attribute_underspecified: 59 |
| combined | 152 | 1.000 | 1.000 | 1.000 | 1.000 | attribute_underspecified: 147, frame_sensitive_relation: 5 |

## Selected-Message Audit

| Run | Method | Success | Failure scenes | Symbolic flag | Under-spec flag | Frame flag | Failure symbolic flag |
|---|---|---:|---:|---:|---:|---:|---:|
| mixed_50_full | direct | 0.840 | 11 | 0.500 | 0.360 | 0.140 | 1.000 |
| mixed_50_full | mirror | 0.907 | 7 | 0.320 | 0.260 | 0.060 | 1.000 |
| mixed_50_full | oracle | 1.000 | 0 | 0.240 | 0.200 | 0.040 | - |
| mixed_50_full | population | 1.000 | 0 | 0.080 | 0.080 | 0.000 | - |
| mixed_50_full | shortest | 0.740 | 15 | 0.440 | 0.440 | 0.000 | 1.000 |
| perspective_gpt54_full | direct | 0.713 | 20 | 1.000 | 0.240 | 0.760 | 1.000 |
| perspective_gpt54_full | mirror | 0.813 | 14 | 0.660 | 0.480 | 0.180 | 1.000 |
| perspective_gpt54_full | oracle | 1.000 | 0 | 0.520 | 0.300 | 0.220 | - |
| perspective_gpt54_full | population | 1.000 | 0 | 0.000 | 0.000 | 0.000 | - |
| perspective_gpt54_full | shortest | 0.420 | 35 | 1.000 | 1.000 | 0.000 | 1.000 |
| perspective_gpt41_full | direct | 0.553 | 31 | 1.000 | 0.240 | 0.760 | 1.000 |
| perspective_gpt41_full | mirror | 0.713 | 22 | 0.660 | 0.480 | 0.180 | 1.000 |
| perspective_gpt41_full | oracle | 1.000 | 0 | 0.340 | 0.180 | 0.160 | - |
| perspective_gpt41_full | population | 1.000 | 0 | 0.000 | 0.000 | 0.000 | - |
| perspective_gpt41_full | shortest | 0.367 | 41 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_full | direct | 0.740 | 19 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_full | mirror | 0.667 | 25 | 0.520 | 0.520 | 0.000 | 1.000 |
| partial_observability_full | oracle | 1.000 | 0 | 0.300 | 0.300 | 0.000 | - |
| partial_observability_full | population | 1.000 | 0 | 0.000 | 0.000 | 0.000 | - |
| partial_observability_full | shortest | 0.313 | 49 | 1.000 | 1.000 | 0.000 | 1.000 |
| mixed_50_no_coord | consensus+info | 0.920 | 6 | 0.500 | 0.300 | 0.200 | 1.000 |
| mixed_50_no_coord | direct | 0.840 | 11 | 0.500 | 0.360 | 0.140 | 1.000 |
| mixed_50_no_coord | mirror | 0.787 | 14 | 0.460 | 0.380 | 0.080 | 1.000 |
| mixed_50_no_coord | oracle | 0.960 | 4 | 0.460 | 0.340 | 0.120 | 1.000 |
| mixed_50_no_coord | population | 0.773 | 13 | 0.460 | 0.460 | 0.000 | 1.000 |
| mixed_50_no_coord | shortest | 0.740 | 15 | 0.460 | 0.460 | 0.000 | 1.000 |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 19 | 1.000 | 0.000 | 1.000 | 1.000 |
| perspective_gpt41_no_coord | direct | 0.553 | 31 | 1.000 | 0.240 | 0.760 | 1.000 |
| perspective_gpt41_no_coord | mirror | 0.580 | 32 | 1.000 | 0.480 | 0.520 | 1.000 |
| perspective_gpt41_no_coord | oracle | 0.793 | 17 | 1.000 | 0.360 | 0.640 | 1.000 |
| perspective_gpt41_no_coord | population | 0.420 | 39 | 1.000 | 0.920 | 0.080 | 1.000 |
| perspective_gpt41_no_coord | shortest | 0.367 | 41 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_no_coord | consensus+info | 0.987 | 1 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_no_coord | direct | 0.740 | 19 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_no_coord | mirror | 0.607 | 29 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_no_coord | oracle | 1.000 | 0 | 1.000 | 1.000 | 0.000 | - |
| partial_observability_no_coord | population | 0.727 | 20 | 1.000 | 1.000 | 0.000 | 1.000 |
| partial_observability_no_coord | shortest | 0.313 | 49 | 1.000 | 1.000 | 0.000 | 1.000 |

## Interpretation

- On the combined coded failure set, symbolic ambiguity recall is 1.000; attribute-under-specification recall is 1.000; and frame-sensitive recall is 1.000.
- In the alternate-model perspective run, the verifier flags 1.000 of mirror failure scenes while flagging 0.000 of population messages.
- In partial observability, it flags 1.000 of mirror failure scenes while flagging 0.000 of population messages.
- In no-coordinate partial observability, it flags 1.000 of mirror failure scenes while flagging 1.000 of consensus+info messages.

The result supports the paper's qualitative interpretation without using another LLM listener: the coded mirror failures are predictable from visible object ambiguity or frame-sensitive left/right language alone. The verifier is deliberately conservative for no-coordinate messages: it ignores relational repairs, so successful consensus+info messages can still be flagged when their color/size/shape words alone match multiple listener-visible objects.
