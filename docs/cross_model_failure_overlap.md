# Cross-Model Failure Overlap Audit

This cache-only audit compares scene-level failures for the same selected messages across held-out listener families. A selected message is counted as a scene failure when at least one of the three listener prompt variants fails.

## Key Findings

- In perspective stress, GPT-5.5 mirror self-play succeeds on 0.673 of listener evaluations and has 25 scene-level failures; all GPT-5.5 mirror-failure scenes are symbolic-verifier positives (1.000).
- In perspective stress, 20 of the 22 GPT-4.1 mirror-failure scenes also fail under GPT-5.5 (0.909).
- In partial observability, GPT-5.5 mirror self-play succeeds on 0.653 and has 26 scene-level failures; all are symbolic-verifier positives (1.000).
- In partial observability, 26 of the 26 GPT-4.1 mirror-failure scenes also fail under GPT-5.5 (1.000).
- Population-play has 0 GPT-5.5 scene-level failures in perspective stress and 0 in partial observability.

## Per-Listener Summary

| Setting | Listener | Method | Success | Failure scenes | Failure symbolic rate | Failure labels |
|---|---|---|---:|---:|---:|---|
| perspective_stress | gpt-5.4-nano | direct | 0.713 | 20 | 1.000 | attribute_underspecified: 7, frame_sensitive_relation: 13 |
| perspective_stress | gpt-5.4-nano | mirror | 0.813 | 14 | 1.000 | attribute_underspecified: 10, frame_sensitive_relation: 4 |
| perspective_stress | gpt-5.4-nano | population | 1.000 | 0 | - | - |
| perspective_stress | gpt-4.1-nano | direct | 0.553 | 31 | 1.000 | attribute_underspecified: 11, frame_sensitive_relation: 20 |
| perspective_stress | gpt-4.1-nano | mirror | 0.713 | 22 | 1.000 | attribute_underspecified: 19, frame_sensitive_relation: 3 |
| perspective_stress | gpt-4.1-nano | population | 1.000 | 0 | - | - |
| perspective_stress | gpt-5.5 | direct | 0.793 | 19 | 1.000 | attribute_underspecified: 12, frame_sensitive_relation: 7 |
| perspective_stress | gpt-5.5 | mirror | 0.673 | 25 | 1.000 | attribute_underspecified: 24, frame_sensitive_relation: 1 |
| perspective_stress | gpt-5.5 | population | 1.000 | 0 | - | - |
| partial_observability | gpt-5.4-nano | direct | 0.740 | 19 | 1.000 | attribute_underspecified: 19 |
| partial_observability | gpt-5.4-nano | mirror | 0.667 | 25 | 1.000 | attribute_underspecified: 25 |
| partial_observability | gpt-5.4-nano | population | 1.000 | 0 | - | - |
| partial_observability | gpt-4.1-nano | direct | 0.700 | 23 | 1.000 | attribute_underspecified: 23 |
| partial_observability | gpt-4.1-nano | mirror | 0.660 | 26 | 1.000 | attribute_underspecified: 26 |
| partial_observability | gpt-4.1-nano | population | 1.000 | 0 | - | - |
| partial_observability | gpt-5.5 | direct | 0.740 | 21 | 1.000 | attribute_underspecified: 21 |
| partial_observability | gpt-5.5 | mirror | 0.653 | 26 | 1.000 | attribute_underspecified: 26 |
| partial_observability | gpt-5.5 | population | 1.000 | 0 | - | - |

## Mirror-Failure Overlap

| Setting | Listener failures | All-listener failures | Any-listener failures |
|---|---|---:|---:|
| partial_observability | gpt-4.1-nano: 26, gpt-5.4-nano: 25, gpt-5.5: 26 | 25 | 26 |
| perspective_stress | gpt-4.1-nano: 22, gpt-5.4-nano: 14, gpt-5.5: 25 | 10 | 30 |

## Pairwise Mirror-Failure Overlap

| Setting | Pair | Intersection | Union | Left only | Right only | Intersection / left | Intersection / right |
|---|---|---:|---:|---:|---:|---:|---:|
| partial_observability | gpt-4.1-nano vs gpt-5.4-nano | 25 | 26 | 1 | 0 | 0.962 | 1.000 |
| partial_observability | gpt-4.1-nano vs gpt-5.5 | 26 | 26 | 0 | 0 | 1.000 | 1.000 |
| partial_observability | gpt-5.4-nano vs gpt-5.5 | 25 | 26 | 0 | 1 | 1.000 | 0.962 |
| perspective_stress | gpt-4.1-nano vs gpt-5.4-nano | 10 | 26 | 12 | 4 | 0.455 | 0.714 |
| perspective_stress | gpt-4.1-nano vs gpt-5.5 | 20 | 27 | 2 | 5 | 0.909 | 0.800 |
| perspective_stress | gpt-5.4-nano vs gpt-5.5 | 11 | 28 | 3 | 14 | 0.786 | 0.440 |

## Interpretation

GPT-5.5 does not simply repair the mirror-selected messages that earlier held-out listener families found fragile. The same ambiguous or frame-sensitive mirror messages account for the frontier-listener failures, while population-play remains at zero scene-level failures in both settings.
