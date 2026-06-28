# Local Benchmark-Scale Sanity Check

This no-API check runs the deterministic local listeners over a 600-scene
balanced benchmark sweep. It is an artifact and generator sanity check, not
one of the paper-facing API listener results.

Scene file: `data/local_benchmark600_scenes.jsonl`
Record file: `results/local_benchmark600_records.jsonl`

## Dataset

| Scenario type | Scenes |
|---|---:|
| distractor_contrast | 150 |
| perspective_shift | 150 |
| relational_reference | 150 |
| unique_attribute | 150 |

## Key Observations

- Mirror self-play has same-play 1.000 but cross-play 0.631, a gap of 0.369.
- Population-play, template, and oracle candidate all reach cross-play 1.000.
- Perspective-shift is the hardest local family: mirror cross-play is 0.158, with a gap of 0.842.

## Overall Results

| Method | Cross-play success | 95% CI | Same-play success | Gap | Mean tokens | Listener stdev |
|---|---:|---:|---:|---:|---:|---:|
| best_of_k_shortest | 0.628 | [0.607, 0.648] | - | - | 4.0 | 0.306 |
| direct | 0.623 | [0.588, 0.658] | - | - | 6.2 | 0.104 |
| mirror_selfplay | 0.631 | [0.598, 0.663] | 1.000 | 0.369 | 5.3 | 0.168 |
| oracle_upper_bound | 1.000 | [1.000, 1.000] | - | - | 7.2 | 0.000 |
| population_play | 1.000 | [1.000, 1.000] | 1.000 | 0.000 | 7.2 | 0.000 |
| template | 1.000 | [1.000, 1.000] | - | - | 10.0 | 0.000 |

## Scenario Breakdown

| Scenario | Direct | Mirror cross | Mirror same | Mirror gap | Population | Oracle |
|---|---:|---:|---:|---:|---:|---:|
| distractor_contrast | 0.504 | 0.676 | 1.000 | 0.324 | 1.000 | 1.000 |
| perspective_shift | 0.000 | 0.158 | 1.000 | 0.842 | 1.000 | 1.000 |
| relational_reference | 0.989 | 0.689 | 1.000 | 0.311 | 1.000 | 1.000 |
| unique_attribute | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 |
