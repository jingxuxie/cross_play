# Iteration 001 Report

Date: 2026-06-27

## What Was Built

- Standard-library PRAG-CrossPlay scaffold:
  - procedural scene generator for unique-attribute, distractor-contrast,
    relational-reference, and perspective-shift scenes;
  - local heuristic training and held-out listeners;
  - template, direct, best-of-K, mirror self-play, population-play, and oracle
    upper-bound methods;
  - OpenAI Responses API client with hash-based response caching;
  - local, full-API, and hybrid API experiment scripts.

Key files:

- `scripts/run_local_pilot.py`
- `scripts/run_api_pilot.py`
- `scripts/run_hybrid_api_pilot.py`
- `scripts/analyze_hybrid_selection.py`
- `results/local_pilot_summary.md`
- `results/hybrid_api_pilot12_summary.json`
- `results/hybrid_api_pilot12_candidates.jsonl`
- `results/hybrid_api_pilot50_summary.md`
- `results/hybrid_api_pilot50_candidates.jsonl`

## Local Simulator Pilot

Command:

```bash
conda run -n cross_play python scripts/run_local_pilot.py
```

Overall:

| Method | Cross-play | Same-play | Gap |
|---|---:|---:|---:|
| template | 1.000 | - | - |
| direct | 0.640 | - | - |
| best-of-K shortest | 0.587 | - | - |
| mirror self-play | 0.627 | 1.000 | 0.373 |
| population-play | 1.000 | 1.000 | 0.000 |
| oracle upper bound | 1.000 | - | - |

Interpretation: the local benchmark has the intended diagnostic behavior. Mirror
self-play can select short ambiguous messages that work for its partner but fail
under held-out listeners; population-play selects robust messages.

## Full API Six-Scene Smoke

Model: `gpt-5.4-nano`.

The API transport and caching work. The first prompt made the speaker overuse
coordinates and hit ceiling. After prompting for a natural first attempt and
adding target attributes, direct/best-of-K exposed one ambiguous perspective
failure, while API mirror and API population both selected robust messages.

Result: useful as a plumbing and prompt sanity check, but not yet a partner
overfitting result.

## Hybrid API Pilot

Setup:

- API speaker generates K=4 candidates.
- Local fixed listener selects mirror-self-play messages.
- Local population of three listeners selects population-play messages.
- API held-out listeners evaluate selected messages.

Command:

```bash
conda run -n cross_play python scripts/run_hybrid_api_pilot.py --max-scenes 12 --model gpt-5.4-nano --records-out results/hybrid_api_pilot12_records.jsonl --summary-out results/hybrid_api_pilot12_summary.json --candidates-out results/hybrid_api_pilot12_candidates.jsonl
```

Overall:

| Method | Cross-play | Same-play | Gap |
|---|---:|---:|---:|
| template | 1.000 | - | - |
| api direct first | 0.889 | - | - |
| api best-of-K shortest | 0.917 | - | - |
| hybrid local mirror | 0.917 | 1.000 | 0.083 |
| hybrid local population | 1.000 | 1.000 | 0.000 |
| oracle upper bound | 1.000 | - | - |

Perspective-shift subset:

| Method | Cross-play | Same-play | Gap |
|---|---:|---:|---:|
| api direct first | 0.556 | - | - |
| api best-of-K shortest | 0.667 | - | - |
| hybrid local mirror | 0.667 | 1.000 | 0.333 |
| hybrid local population | 1.000 | 1.000 | 0.000 |
| oracle upper bound | 1.000 | - | - |

Representative failure:

- Scene `ps_000043`, target `obj_1`: small yellow sphere at row 4, column 1.
- Mirror selected: `Small yellow sphere.`
- Local mirror listener: success, but ambiguous.
- API held-out listeners chose `obj_2`, the other small yellow sphere.
- Population selected: `If needed: small yellow sphere at row 4, column 1.`
- API held-out listeners succeeded.

Interpretation: this is the first paper-relevant signal. A fixed simulated
partner can make a short ambiguous API-generated message look successful, while
cross-play with held-out API listeners exposes the ambiguity. A local population
of heterogeneous listeners mitigates this by selecting explicit candidates.

## Hybrid API 50-Scene Pilot

Command:

```bash
conda run -n cross_play python scripts/run_hybrid_api_pilot.py --max-scenes 50 --model gpt-5.4-nano --records-out results/hybrid_api_pilot50_records.jsonl --summary-out results/hybrid_api_pilot50_summary.json --candidates-out results/hybrid_api_pilot50_candidates.jsonl
```

Overall:

| Method | Cross-play | Same-play | Gap | 95% CI |
|---|---:|---:|---:|---:|
| template | 1.000 | - | - | [1.000, 1.000] |
| api direct first | 0.840 | - | - | [0.747, 0.920] |
| api best-of-K shortest | 0.740 | - | - | [0.627, 0.853] |
| hybrid local mirror | 0.907 | 1.000 | 0.093 | [0.833, 0.967] |
| hybrid local population | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| oracle upper bound | 1.000 | - | - | [1.000, 1.000] |

Scenario-level result:

- Unique attribute and distractor contrast are at ceiling for all strong
  methods.
- Relational reference shows a smaller mirror gap:
  `mirror=0.933`, `population=1.000`, `gap=0.067`.
- Perspective shift is the main stress case:
  `direct=0.600`, `best-of-K=0.400`, `mirror=0.633`,
  `population=1.000`, `oracle=1.000`.
- The perspective-shift mirror gap is `1.000 - 0.633 = 0.367`.

Interpretation: the larger pilot preserves the paper-relevant signal. The
speaker usually generates at least one robust candidate, as shown by the oracle
ceiling. A fixed mirror listener often accepts a short ambiguous candidate, so
same-play success overstates held-out communicative success. A heterogeneous
local population reliably selects the robust candidate.

## Cost

The cache currently contains 1173 OpenAI responses:

```json
{"input_tokens": 312411, "output_tokens": 28634}
```

Approximate spend at the current nano-class pricing assumption used here:
`$0.0983`.

## Next Experimental Step

Do not scale the full API self-play path yet; it is slower and did not reveal a
gap in the small pilot. The next efficient experiment should make the hybrid
path paper-grade:

Before a 600-scene run, add:

- a scenario-balanced scene sampler for API pilots;
- cached all-candidate held-out records for selection-regret analysis;
- a CSV export of failure cases for manual coding;
- one harder perspective variant where coordinates are absent from the first
  three candidates but available in the fallback.
- bootstrap paired difference tests for mirror versus population by scenario.

## Iteration 002 Update: Perspective Stress Replication

Implemented:

- all-candidate held-out logging in `scripts/run_hybrid_api_pilot.py`;
- paired bootstrap method comparisons in `scripts/compare_methods.py`;
- failure-case CSV export in `scripts/export_failures.py`;
- paper table generation in `scripts/make_paper_tables.py`;
- paper-facing claims memo in `docs/paper_claims_iteration_002.md`.

Stress setup:

- 50 new perspective-shift scenes in
  `data/perspective_stress50_scenes.jsonl`;
- API speaker generates K=4 candidates;
- local mirror and local population select from those candidates;
- API held-out listeners evaluate selected messages;
- every candidate is also evaluated to compute oracle upper bound.

Perspective-stress results:

| Method | Cross-play | Same-play | Gap | 95% CI |
|---|---:|---:|---:|---:|
| template | 1.000 | - | - | [1.000, 1.000] |
| api direct first | 0.713 | - | - | [0.600, 0.813] |
| api best-of-K shortest | 0.420 | - | - | [0.293, 0.540] |
| hybrid local mirror | 0.813 | 1.000 | 0.187 | [0.720, 0.900] |
| hybrid local population | 1.000 | 1.000 | 0.000 | [1.000, 1.000] |
| oracle upper bound | 1.000 | - | - | [1.000, 1.000] |

Paired test:

- population minus mirror = `0.187`;
- 95% bootstrap CI `[0.100, 0.287]`;
- paired bootstrap `p=0.0000`.

Selection-regret analysis relative to oracle:

- direct first candidate: `0.287`;
- best-of-K shortest: `0.580`;
- hybrid local mirror: `0.187`;
- hybrid local population: `0.000`.

Failure export:

- `results/perspective_stress50_mirror_failures.csv`;
- 28 held-out listener failures for mirror self-play;
- automatic categories are mostly `underspecified` and `perspective_error`.

Paper-ready artifacts:

- `paper/tables/mixed50.tex`;
- `paper/tables/mixed50_paired.tex`;
- `paper/tables/perspective_stress50.tex`;
- `paper/tables/perspective_stress50_paired.tex`;
- `docs/paper_claims_iteration_002.md`.

Updated cost:

```json
{"input_tokens": 539409, "output_tokens": 48843}
```

Approximate spend at the same nano-class pricing assumption: `$0.1689`.
