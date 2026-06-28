# GPT-5.5 K=8 No-Coordinate Audit

GPT-5.5 no-coordinate candidate generation comparison for Experiment 4. K=4 filters the standard GPT-5.5 speaker candidates; K=8 uses the dedicated no-coordinate prompt and GPT-5.5 held-out listeners.

## Key Observations

- K=4 filtered baseline keeps 148 candidates and excludes 52 coordinate candidates; K=8 keeps 400 and excludes 0.
- The dedicated K=8 no-coordinate prompt produced 0 exact-coordinate candidates across 50 scenes.
- Oracle success is 1.000 at K=4 and 1.000 at K=8, so the hard limitation is not lack of any non-coordinate expression.
- K=8 population-play improves from 0.833 to 0.993; shortest reaches 1.000.
- Consensus+info falls from 0.993 to 0.900, showing that the informativeness heuristic can over-select brittle long relational messages.

## Method Comparison

| Method | K=4 filtered | K=8 no-coordinate | Delta |
|---|---:|---:|---:|
| Direct first | 0.993 | 0.973 | -0.020 |
| Shortest | 0.787 | 1.000 | +0.213 |
| Mirror | 0.847 | 0.953 | +0.107 |
| Population | 0.833 | 0.993 | +0.160 |
| Consensus+info | 0.993 | 0.900 | -0.093 |
| Info prior | 0.993 | 0.900 | -0.093 |
| Oracle | 1.000 | 1.000 | +0.000 |

## Candidate Budget

### gpt55_k4_filtered

| K | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle |
|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.980 | 0.980 | 0.993 |
| 2 | 2.000 | 1.540 | 1.000 | 1.000 |
| 4 | 2.960 | 2.500 | 1.000 | 1.000 |

### gpt55_k8_no_coordinate_prompt

| K | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle |
|---:|---:|---:|---:|---:|
| 1 | 1.000 | 0.960 | 0.960 | 0.973 |
| 2 | 2.000 | 1.960 | 1.000 | 1.000 |
| 4 | 4.000 | 3.780 | 1.000 | 1.000 |
| 8 | 8.000 | 7.420 | 1.000 | 1.000 |

## Claim Boundary

- Safe: GPT-5.5 can generate robust non-coordinate referring expressions on all 50 perspective-stress scenes.
- Safe: increasing to K=8 improves population and mirror selection, but the heuristic consensus+info selector is not monotonic.
- Do not claim: consensus+info is the best no-coordinate selector for GPT-5.5 K=8; shortest and population are stronger in this run.
