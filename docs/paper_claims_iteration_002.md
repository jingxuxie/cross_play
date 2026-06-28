# Paper Claims Memo: Iteration 002

Date: 2026-06-27

## Main Claim Supported So Far

In controlled situated reference games, same-partner communicative success can
overstate robust pragmatic success under partner shift. The clearest failure
mode is perspective-sensitive reference: mirror self-play accepts short
utterances that its partner resolves correctly, while held-out listeners often
choose the distractor. Population-play mitigates this by selecting messages that
are interpretable across heterogeneous local listener models.

## Strongest Quantitative Evidence

### Mixed 50-scene pilot

File: `results/hybrid_api_pilot50_records.jsonl`

- Mirror self-play: cross-play `0.907`, same-play `1.000`, gap `0.093`.
- Population-play: cross-play `1.000`, same-play `1.000`, gap `0.000`.
- Paired population-minus-mirror difference: `0.093`,
  95% bootstrap CI `[0.027, 0.173]`, paired bootstrap `p=0.0024`.
- In perspective-shift scenes only: population-minus-mirror difference `0.367`,
  95% CI `[0.133, 0.600]`, paired bootstrap `p=0.0004`.

### Perspective-stress replication

File: `results/perspective_stress50_hybrid_records.jsonl`

- Direct first candidate: `0.713`.
- Best-of-K shortest: `0.420`.
- Mirror self-play: cross-play `0.813`, same-play `1.000`, gap `0.187`.
- Population-play: cross-play `1.000`, same-play `1.000`, gap `0.000`.
- Oracle candidate upper bound: `1.000`.
- Paired population-minus-mirror difference: `0.187`,
  95% bootstrap CI `[0.100, 0.287]`, paired bootstrap `p=0.0000`.

The oracle ceiling matters: candidate generation is not the bottleneck in this
stress set. The failures are caused by selecting brittle candidates.

### Alternate held-out model audit

File: `results/perspective_stress50_gpt41nano_records.jsonl`

This reuses the same 50 perspective-stress scenes and the same API-generated
candidates, but evaluates final messages with `gpt-4.1-nano` held-out listeners
instead of `gpt-5.4-nano` listeners.

- Direct first candidate: `0.553`.
- Best-of-K shortest: `0.367`.
- Mirror self-play: cross-play `0.713`, same-play `1.000`, gap `0.287`.
- Population-play: cross-play `1.000`, same-play `1.000`, gap `0.000`.
- Oracle candidate upper bound: `1.000`.
- Paired population-minus-mirror difference: `0.287`,
  95% bootstrap CI `[0.193, 0.380]`, paired bootstrap `p=0.0000`.

Interpretation: the main result is not specific to the original held-out API
model. The alternate model is harsher on ambiguous mirror-selected messages, but
population-play remains at the oracle upper bound.

### No-exact-coordinate ablation

Files:

- `results/perspective_stress50_gpt41nano_no_coord_records.jsonl`.
- `results/perspective_stress50_gpt41nano_no_coord_summary.md`.
- `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl`.
- `results/hybrid_api_pilot50_no_coord_records.jsonl`.
- `results/hybrid_api_pilot50_no_coord_summary.md`.
- `paper/tables/selection_mechanisms_stress_full.md`.
- `paper/tables/selection_mechanisms_stress_no_coord.md`.
- `paper/tables/selection_mechanisms_mixed_no_coord.md`.

This is a cache-only ablation that removes candidate messages explicitly
mentioning row or column numbers, then recomputes selection while reusing cached
held-out candidate evaluations.

Perspective-stress, alternate held-out model:

- Scenes: `50`, skipped scenes: `0`.
- Candidates kept: `150`; exact-coordinate candidates excluded: `50`.
- Mirror self-play: cross-play `0.580`, same-play `1.000`, gap `0.420`.
- Population-play: cross-play `0.420`, same-play `0.520`, gap `0.100`.
- Consensus+info selector: cross-play `0.760`.
- Text-only informativeness prior: cross-play `0.760`.
- Oracle candidate upper bound: `0.793`.
- Consensus+info versus mirror: paired difference `0.180`,
  95% bootstrap CI `[0.100, 0.267]`, paired bootstrap `p=0.0000`.

Mixed 50-scene pilot, original held-out model:

- Scenes: `50`, skipped scenes: `0`.
- Candidates kept: `150`; exact-coordinate candidates excluded: `50`.
- Mirror self-play: cross-play `0.787`, same-play `0.880`, gap `0.093`.
- Population-play: cross-play `0.773`, same-play `0.813`, gap `0.040`.
- Consensus+info selector: cross-play `0.920`.
- Text-only informativeness prior: cross-play `0.900`.
- Oracle candidate upper bound: `0.960`.
- Consensus+info versus mirror: paired difference `0.133`,
  95% bootstrap CI `[0.033, 0.233]`, paired bootstrap `p=0.0040`.
- By scenario, the consensus+info gains concentrate in
  relational-reference scenes (`0.889` versus mirror `0.578`) and
  perspective-shift scenes (`0.767` versus mirror `0.567`).

Interpretation: the strongest population-play result should be framed as robust
fallback selection when exact listener-invariant coordinates are available. The
no-coordinate ablation is more diagnostic than confirmatory: it shows that
robust non-coordinate candidates often exist, but the current local population
selector does not reliably identify them. A simple consensus+info selector
recovers most of the no-coordinate oracle by trusting unanimous local support
when available and otherwise falling back to an explicit informativeness prior.

Mechanism counts:

- In the full perspective-stress audit, population-play selected exact
  row/column coordinates in `50/50` scenes; mirror selected exact coordinates in
  `17/50`.
- In the perspective-stress no-coordinate audit, naive population-play selected
  spatially informative messages in `4/50` scenes, while consensus+info selected
  spatially informative messages in `50/50`.
- In the mixed no-coordinate audit, consensus+info used local consensus in
  `32/50` scenes and the informativeness fallback in `18/50`.

## Representative Failure

Scene `ps_000023`:

- Target: `obj_1`, small blue sphere at row 4, column 1.
- Candidate selected by mirror: `It's a small blue sphere.`
- Held-out direct/strict listeners choose `obj_2`, another small blue sphere.
- Population selection: `The target is the small blue sphere at row 4, column 1.`

Failure category: underspecified reference under perspective shift.

Scene `ps_000003`:

- Target: `obj_1`, small yellow sphere at row 4, column 1.
- Distractor: `obj_2`, small yellow sphere at row 1, column 4.
- Mirror selected: `Find the small yellow sphere left of the large green cube.`
- All three alternate-model held-out listeners chose the distractor, consistent
  with a perspective-frame interpretation mismatch.
- Population selected: `The target is at row 4, column 1: a small yellow
  sphere.`

Failure category: perspective-frame error.

Alternate-model coded failures:

- File: `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv`.
- Rubric-coded listener-level failures: 43 total.
- `underspecified_distractor`: 38.
- `perspective_frame_error`: 5.
- Representative perspective-frame failure: scene `ps_000003`, where all
  alternate-model held-out listeners chose the distractor.

## Claims To Avoid For Now

- Do not claim full LLM self-play training improves or hurts pragmatics. The
  strongest current result is hybrid: API speaker candidates, local simulated
  selection partners, API held-out listeners.
- Do not claim population-play always fixes partner overfitting. It works in the
  main setting by selecting explicit, listener-invariant fallbacks; without exact
  coordinates, the current local population selector can be worse than mirror,
  while consensus+info recovers much of the available robust-candidate signal.
- Do not claim general social intelligence. The benchmark tests situated
  reference under controlled partner shift.
- Do not overclaim all scenario types. Unique-attribute and distractor-contrast
  cases are near ceiling; the main empirical effect is perspective shift, with
  a smaller relational-reference signal.

## Next Paper-Grade Additions

- Add a 100- or 200-scene perspective-stress run after adding async or Batch API
  support.
- Add a figure showing same-play versus cross-play gaps by scenario.
