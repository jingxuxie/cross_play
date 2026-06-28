# Partial-Observability Local Stress Check

Date: 2026-06-27

This is a local, no-API benchmark extension for the Type E scenario in
`cross_play_pragmatics_workshop_plan.md`. It is not used as a paper-facing API
result in the current draft. Its purpose is to make the released benchmark
cover private-landmark cases and to provide a cheap sanity check before any
future API or human evaluation.

## Setup

Command:

```bash
conda run -n cross_play python scripts/run_local_pilot.py \
  --unique 0 --contrast 0 --relational 0 --perspective 0 --partial 50 \
  --seed 20260627 \
  --scene-out data/partial_observability_local50_scenes.jsonl \
  --records-out results/partial_observability_local50_records.jsonl \
  --summary-out results/partial_observability_local50_summary.json \
  --markdown-out results/partial_observability_local50_summary.md
```

Artifacts:

- `data/partial_observability_local50_scenes.jsonl`
- `results/partial_observability_local50_records.jsonl`
- `results/partial_observability_local50_summary.json`
- `results/partial_observability_local50_summary.md`

## Result

| Method | Cross-play success | Same-play success | Gap |
|---|---:|---:|---:|
| direct | 0.493 | - | - |
| best-of-K shortest | 0.493 | - | - |
| mirror self-play | 0.653 | 1.000 | 0.347 |
| population-play | 1.000 | 1.000 | 0.000 |
| oracle upper bound | 1.000 | - | - |
| template | 1.000 | - | - |

## Interpretation

The scenario creates a target and distractor with matching visible attributes,
plus a private landmark that is visible to the speaker but hidden from the
listener. The direct baseline therefore tends to produce brittle messages such
as `Select the green sphere left of the red cylinder`, where the red cylinder is
not in the listener view. Local mirror self-play still has a large cross-play
gap because its fixed partner can resolve some ambiguous messages. Population
selection finds the robust coordinate fallback in this deterministic local
setting.

This supports adding partial observability to the released benchmark, but it
does not replace the API listener evidence in the current paper.
