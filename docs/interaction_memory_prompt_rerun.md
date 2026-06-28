# Interaction-Memory Prompt Rerun

This bounded API audit tests whether the failure-derived interaction-memory rules can repair the mirror-failure items prepared for human validation. It is not a human-subjects result; it is a prompt-rerun diagnostic on the same sampled failure scenes.

## Summary

Items: 15. Conditions: partial_mirror_failure=5, perspective_mirror_failure=10. Speaker/listener model: `gpt-5.5`.

| Method | Success | Same-play | Gap | Mean tokens | Records |
|---|---:|---:|---:|---:|---:|
| mirror_selfplay | 0.422 | - | - | 4.8 | 45 |
| interaction_memory_prompt | 1.000 | - | - | 10.2 | 45 |
| population_play | 1.000 | - | - | 10.5 | 45 |

## By Condition

| Condition | Method | Items | Success | Mean tokens |
|---|---|---:|---:|---:|
| partial_mirror_failure | mirror_selfplay | 5 | 0.333 | 3.0 |
| partial_mirror_failure | interaction_memory_prompt | 5 | 1.000 | 10.6 |
| partial_mirror_failure | population_play | 5 | 1.000 | 10.6 |
| perspective_mirror_failure | mirror_selfplay | 10 | 0.467 | 5.7 |
| perspective_mirror_failure | interaction_memory_prompt | 10 | 1.000 | 10.0 |
| perspective_mirror_failure | population_play | 10 | 1.000 | 10.5 |

## Paired Comparisons

| Condition | A | B | N | Mean A | Mean B | Diff A-B | 95% CI | p_boot |
|---|---|---|---:|---:|---:|---:|---:|---:|
| overall | interaction_memory_prompt | mirror_selfplay | 15 | 1.000 | 0.422 | 0.578 | [0.444, 0.667] | 0.0000 |
| overall | interaction_memory_prompt | population_play | 15 | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | 1.0000 |
| partial_mirror_failure | interaction_memory_prompt | mirror_selfplay | 5 | 1.000 | 0.333 | 0.667 | [0.667, 0.667] | 0.0000 |
| perspective_mirror_failure | interaction_memory_prompt | mirror_selfplay | 10 | 1.000 | 0.467 | 0.533 | [0.333, 0.667] | 0.0000 |

## Generated Messages

| Item | Condition | Scene | Failed mirror message | Memory message |
|---|---|---|---|---|
| HVAL_001 | perspective_mirror_failure | `ps_000000` | It’s a large red sphere. | Select the large red sphere at row 4, column 1. |
| HVAL_002 | perspective_mirror_failure | `ps_000003` | Find the small yellow sphere left of the large green cube. | Select the small yellow sphere at row 4, column 1. |
| HVAL_003 | perspective_mirror_failure | `ps_000004` | It’s a large red sphere. | Select the large red sphere at row 4, column 1. |
| HVAL_004 | perspective_mirror_failure | `ps_000005` | It’s a small green sphere. | Select the small green sphere at row 4, column 1. |
| HVAL_005 | perspective_mirror_failure | `ps_000008` | It’s a small blue cube. | Select the small blue cube at row 4, column 1. |
| HVAL_006 | perspective_mirror_failure | `ps_000009` | Large blue cube. | Select the large blue cube at row 4, column 1. |
| HVAL_007 | perspective_mirror_failure | `ps_000011` | Find the large yellow cube left of the purple cylinder. | Select the large yellow cube at row 4, column 1. |
| HVAL_008 | perspective_mirror_failure | `ps_000012` | It’s a small blue sphere. | Select the small blue sphere at row 4, column 1. |
| HVAL_009 | perspective_mirror_failure | `ps_000013` | It’s a large yellow cube. | Select the large yellow cube at row 4, column 1. |
| HVAL_010 | perspective_mirror_failure | `ps_000018` | Small red sphere. | Select the small red sphere at row 4, column 1. |
| HVAL_011 | partial_mirror_failure | `po_000000` | Large red sphere. | Select the large red sphere at row 3, column 2. |
| HVAL_012 | partial_mirror_failure | `po_000004` | Large red sphere. | The large red sphere at row 3, column 2, directly above the green cylinder. |
| HVAL_013 | partial_mirror_failure | `po_000005` | Small green sphere. | The small green sphere at row 3, column 2. |
| HVAL_014 | partial_mirror_failure | `po_000006` | Large yellow sphere. | Select the large yellow sphere at row 3, column 2. |
| HVAL_015 | partial_mirror_failure | `po_000008` | Small blue cube. | Select the small blue cube at row 3, column 2. |

## Claim Boundary

Safe to claim: on this bounded human-packet failure sample, the distilled rules can be used as a prompt memory to generate replacement messages and evaluate them under the same GPT-5.5 held-out listener styles.
Not safe to claim: this is not evidence that human listeners agree, nor that an online learning system would discover the rules without the author-coded failure analysis.
