# Qualitative Failure Examples

Cache-only representative qualitative examples linking selected messages, held-out listener choices, and generated scene context.
The examples are selected deterministically from cached artifacts and make no API calls.

## Summary

| Example | Scene | Category | Mirror success | Repair | Repair success | Source |
|---|---|---|---:|---|---:|---|
| Perspective scene with attribute underspecification | `ps_000005` | underspecified_distractor | 0.333 (1/3) | population | 1.000 (3/3) | `results/perspective_stress50_gpt41nano_records.jsonl` |
| Perspective scene with frame-sensitive relation | `ps_000011` | perspective_frame_error | 0.667 (2/3) | population | 1.000 (3/3) | `results/perspective_stress50_gpt41nano_records.jsonl` |
| Partial-observability scene with visible distractor ambiguity | `po_000005` | underspecified_distractor | 0.333 (1/3) | population | 1.000 (3/3) | `results/partial_observability_api50_records.jsonl` |
| No-coordinate repair using consensus+info | `po_000000` | underspecified_distractor | 0.333 (1/3) | consensus+info | 1.000 (3/3) | `results/partial_observability_api50_no_coord_records.jsonl` |

## Perspective scene with attribute underspecification

- Scene: `ps_000005` (perspective_shift); speaker faces `north`, listener faces `east`.
- Target: obj_1: small green sphere at row 4, column 1 (visible)
- Confuser chosen by at least one held-out listener: obj_2: small green sphere at row 1, column 4 (visible)
- Private landmark ID: `-`
- Mirror-selected message: "It’s a small green sphere."
- population message: "The target is the small green sphere at row 4, column 1."
- Interpretation: The mirror-selected message names attributes shared by the target and distractor. The population-selected message adds a listener-invariant coordinate fallback.

| Listener | Mirror choice | Mirror success | Repair choice | Repair success |
|---|---|---:|---|---:|
| `gpt-4.1-nano:careful` | `obj_1` | 1 | `obj_1` | 1 |
| `gpt-4.1-nano:direct_last` | `obj_2` | 0 | `obj_1` | 1 |
| `gpt-4.1-nano:strict_last` | `obj_2` | 0 | `obj_1` | 1 |

Sources: `results/perspective_stress50_gpt41nano_audit.jsonl`; `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv`.

## Perspective scene with frame-sensitive relation

- Scene: `ps_000011` (perspective_shift); speaker faces `north`, listener faces `east`.
- Target: obj_1: large yellow cube at row 4, column 1 (visible)
- Confuser chosen by at least one held-out listener: obj_2: large yellow cube at row 1, column 4 (visible)
- Private landmark ID: `-`
- Mirror-selected message: "Find the large yellow cube left of the purple cylinder."
- population message: "Go to row 4, column 1: the large yellow cube."
- Interpretation: The mirror-selected relation uses left/right language that is brittle under partner orientation shift. The population selector chooses an unambiguous fallback.

| Listener | Mirror choice | Mirror success | Repair choice | Repair success |
|---|---|---:|---|---:|
| `gpt-4.1-nano:careful` | `obj_2` | 0 | `obj_1` | 1 |
| `gpt-4.1-nano:direct_last` | `obj_1` | 1 | `obj_1` | 1 |
| `gpt-4.1-nano:strict_last` | `obj_1` | 1 | `obj_1` | 1 |

Sources: `results/perspective_stress50_gpt41nano_audit.jsonl`; `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv`.

## Partial-observability scene with visible distractor ambiguity

- Scene: `po_000005` (partial_observability); speaker faces `north`, listener faces `north`.
- Target: obj_1: small green sphere at row 3, column 2 (visible)
- Confuser chosen by at least one held-out listener: obj_2: small green sphere at row 3, column 4 (visible)
- Private landmark ID: `obj_3`
- Mirror-selected message: "Small green sphere."
- population message: "The target is the small green sphere at row 3, column 2."
- Interpretation: The failure does not require private-landmark leakage: the mirror message is simply too short to distinguish two listener-visible same-attribute objects.

| Listener | Mirror choice | Mirror success | Repair choice | Repair success |
|---|---|---:|---|---:|
| `L_test_careful_api` | `obj_1` | 1 | `obj_1` | 1 |
| `L_test_direct_last_api` | `obj_2` | 0 | `obj_1` | 1 |
| `L_test_strict_last_api` | `obj_2` | 0 | `obj_1` | 1 |

Sources: `results/partial_observability_api50_candidates.jsonl`; `results/partial_observability_api50_mirror_failures_coded.csv`.

## No-coordinate repair using consensus+info

- Scene: `po_000000` (partial_observability); speaker faces `north`, listener faces `north`.
- Target: obj_1: large red sphere at row 3, column 2 (visible)
- Confuser chosen by at least one held-out listener: obj_2: large red sphere at row 3, column 4 (visible)
- Private landmark ID: `obj_3`
- Mirror-selected message: "Large red sphere."
- consensus+info message: "The large red sphere in the upper-left area of the scene."
- Interpretation: After exact coordinates are filtered out, consensus+info can still repair the mirror failure by selecting a more informative visible cue.

| Listener | Mirror choice | Mirror success | Repair choice | Repair success |
|---|---|---:|---|---:|
| `L_test_careful_api` | `obj_1` | 1 | `obj_1` | 1 |
| `L_test_direct_last_api` | `obj_2` | 0 | `obj_1` | 1 |
| `L_test_strict_last_api` | `obj_2` | 0 | `obj_1` | 1 |

Sources: `results/partial_observability_api50_no_coord_audit.jsonl`; `results/partial_observability_api50_no_coord_mirror_failures_coded.csv`.
