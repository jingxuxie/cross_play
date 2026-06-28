# PRAG-CrossPlay

PRAG-CrossPlay is a small situated reference-game benchmark for testing whether
communicative self-play produces robust pragmatic messages or partner-specific
conventions. The initial implementation is deliberately lightweight: scene
generation, local simulated listeners, selection methods, scoring, and an
OpenAI API pilot runner all use the Python standard library.

## Cache and token accounting

The cached Responses API files include usage metadata. This command summarizes
the cache without making API calls.

```bash
conda run -n cross_play python scripts/analyze_api_token_accounting.py \
  --markdown-out docs/api_token_accounting.md \
  --json-out results/api_token_accounting.json
```

The current report is `docs/api_token_accounting.md`: `7,171` cached responses
have complete usage metadata and contain `2,080,070` total tokens. Dollar cost
is not estimated from cached files; use the provider dashboard for final
billing.

## Fast local pilot

```bash
conda run -n cross_play python scripts/run_local_pilot.py
```

This writes:

- `data/dev_scenes.jsonl`
- `results/local_pilot_records.jsonl`
- `results/local_pilot_summary.json`
- `results/local_pilot_summary.md`

## Benchmark-scale local sanity check

The original workshop plan calls for a 600-scene balanced benchmark scale. This
no-API check exercises that scale with deterministic local listeners; it is an
artifact and generator sanity check, not a paper-facing API result.

```bash
conda run -n cross_play python scripts/run_local_pilot.py \
  --seed 7 --k 4 \
  --unique 150 --contrast 150 --relational 150 --perspective 150 --partial 0 \
  --scene-out data/local_benchmark600_scenes.jsonl \
  --records-out results/local_benchmark600_records.jsonl \
  --summary-out results/local_benchmark600_summary.json \
  --markdown-out results/local_benchmark600_summary.md

conda run -n cross_play python scripts/analyze_local_benchmark.py \
  --scene-file data/local_benchmark600_scenes.jsonl \
  --records results/local_benchmark600_records.jsonl \
  --markdown-out docs/local_benchmark600_check.md \
  --json-out results/local_benchmark600_check.json
```

The current report is `docs/local_benchmark600_check.md`: mirror self-play has
same-play `1.000` but cross-play `0.631`, while population-play, template, and
oracle candidate reach cross-play `1.000`.

## Local stronger-plan K=8 diagnostic

This no-API diagnostic exercises the stronger-plan scale with `1,000` initial
family scenes, `200` partial-observability scenes, and K=8 local candidate
slots. It is artifact support for scale and candidate diversity, not a
paper-facing API result.

```bash
conda run -n cross_play python scripts/analyze_local_stronger_plan.py \
  --scene-out data/local_stronger_plan1200_scenes.jsonl \
  --markdown-out docs/local_stronger_plan_k8.md \
  --json-out results/local_stronger_plan_k8.json
```

The current report is `docs/local_stronger_plan_k8.md`: no-coordinate oracle
success rises from `0.808` at K=4 to `0.995` at K=8 over all `1,200` local
scenes, and no-coordinate consensus+info reaches `0.993` at K=8.

## Optional partial-observability local stress check

The released generator also supports private-landmark scenes, where the speaker
can see a landmark hidden from the listener. The local run below is a no-API
sanity check; the following cached API support check is the paper-facing
partial-observability result.

```bash
conda run -n cross_play python scripts/run_local_pilot.py \
  --unique 0 --contrast 0 --relational 0 --perspective 0 --partial 50 \
  --seed 20260627 \
  --scene-out data/partial_observability_local50_scenes.jsonl \
  --records-out results/partial_observability_local50_records.jsonl \
  --summary-out results/partial_observability_local50_summary.json \
  --markdown-out results/partial_observability_local50_summary.md
```

There is also a cached API support check on the 50 private-landmark scenes. It
tests whether the partial-observability extension shows the same same-play
versus cross-play failure mode under API listeners.

```bash
conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --max-scenes 50 \
  --model gpt-5.4-nano \
  --records-out results/partial_observability_api50_records.jsonl \
  --summary-out results/partial_observability_api50_summary.json \
  --candidates-out results/partial_observability_api50_candidates.jsonl \
  --all-candidate-records-out results/partial_observability_api50_candidate_eval_records.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/analyze_partial_observability_api.py
```

The compact report is `docs/partial_observability_api50_check.md`. It includes
the private-landmark audit and coded mirror-failure counts showing that all
full-run and no-coordinate mirror failures are underspecified-distractor
choices.

## Cross-model held-out listener audit

The follow-up cross-model audit reuses cached speaker candidates and selected
messages, then evaluates those messages with `gpt-4.1-nano`, `gpt-5.4-nano`,
and `gpt-5.5` listener families. The current report is
`docs/cross_model_listener_audit.md`. Population-play remains at cross-play
`1.000` in all six setting/listener rows, while mirror self-play ranges from
`0.653` to `0.813`; the GPT-5.5 population-minus-mirror gaps are `0.327` on
perspective stress and `0.347` on partial observability.

```bash
conda run -n cross_play python scripts/analyze_cross_model_listener_audit.py \
  --json-out results/cross_model_listener_audit.json \
  --markdown-out docs/cross_model_listener_audit.md \
  --table-out paper/tables/cross_model_listener_audit.md \
  --tex-out paper/tables/cross_model_listener_audit.tex
```

## Cross-model failure overlap audit

The failure-overlap audit is a cache-only companion to the cross-model table. It
checks whether GPT-5.5 repairs the same mirror-selected messages that fail under
earlier held-out listener families. The current report is
`docs/cross_model_failure_overlap.md`: in perspective stress, `20` of `22`
GPT-4.1 mirror-failure scenes also fail under GPT-5.5; in partial observability,
`26` of `26` do. All GPT-5.5 mirror-failure scenes are symbolic-verifier
positives, while GPT-5.5 population-play has zero scene-level failures in both
settings.

```bash
conda run -n cross_play python scripts/analyze_cross_model_failure_overlap.py \
  --json-out results/cross_model_failure_overlap.json \
  --markdown-out docs/cross_model_failure_overlap.md \
  --units-out results/cross_model_failure_overlap_units.jsonl
```

## GPT-5.5 speaker smoke

The Experiment 3 smoke report is `docs/gpt55_speaker_smoke_report.md`. It
compares existing perspective-stress speaker candidates with newly generated
GPT-5.5 speaker candidates on the same first 10 scenes, evaluated by GPT-5.5
held-out listener prompts. GPT-5.5 direct-first rises from `0.800` to `1.000`,
mirror self-play rises from `0.667` to `0.867`, and population-play remains
`1.000` for both candidate pools. The full 50-scene speaker audit has GPT-5.5
direct-first `0.993`, mirror self-play `0.853` despite same-play `1.000`, and
population-play `1.000`. This is now paper-facing Experiment 3 evidence under
GPT-5.5 held-out listeners.

```bash
conda run -n cross_play python scripts/analyze_gpt55_speaker_smoke.py \
  --json-out results/gpt55_speaker_smoke.json \
  --markdown-out docs/gpt55_speaker_smoke_report.md
```

## GPT-5.5 K=8 no-coordinate audit

Experiment 4 now has a paper-facing API run in
`docs/gpt55_no_coord_k8_report.md`. The dedicated GPT-5.5 no-coordinate prompt
produces `400` candidate messages across the 50 perspective-stress scenes, with
`0` exact-coordinate violations. Relative to the K=4 filtered baseline,
population-play improves from `0.833` to `0.993`, mirror improves from `0.847`
to `0.953`, and the oracle remains `1.000`. Consensus+info drops from `0.993`
to `0.900`, so the safe claim is that robust non-coordinate expressions are
available and selector design remains the bottleneck, not that consensus+info
dominates at K=8.

```bash
conda run -n cross_play python scripts/analyze_gpt55_no_coord_k8.py \
  --json-out results/gpt55_no_coord_k8_comparison.json \
  --markdown-out docs/gpt55_no_coord_k8_report.md
```

## GPT-5.5 follow-up plan status

The generated status report `docs/gpt55_followup_plan_status.md` maps
`additional_experiments_gpt55_plan.md` to the current artifacts. It currently
marks `5` follow-up experiments covered, `1` partial, and `0` future with no
missing evidence paths. Use it as a claim-boundary check before promoting human
validation into paper headline claims.

```bash
conda run -n cross_play python scripts/audit_gpt55_followup_plan.py \
  --json-out results/gpt55_followup_plan_status.json \
  --markdown-out docs/gpt55_followup_plan_status.md
```

## Human validation packet

The optional human-validation extension is protocol-ready in
`docs/human_validation_packet.md`. It contains `20` participant-safe items:
`10` perspective mirror failures, `5` partial-observability mirror failures,
and `5` mirror-success controls. It also writes a response template and a
researcher-only answer key. No human annotations are present yet, so this is not
human-validation evidence.

```bash
conda run -n cross_play python scripts/make_human_validation_packet.py \
  --items-out data/human_validation_items.jsonl \
  --responses-out data/human_validation_response_template.csv \
  --answer-key-out results/human_validation_answer_key.json \
  --markdown-out docs/human_validation_packet.md \
  --html-out docs/human_validation_packet.html
```

## Cache-only API listener leave-one-out check

The all-candidate API evaluation caches can also be reused for a post-hoc
leave-one-listener-out mechanism check. This analysis holds out one API listener
prompt for evaluation, selects candidates with the remaining prompt or prompts,
and makes no API calls.

```bash
conda run -n cross_play python scripts/analyze_api_listener_leave_one_out.py \
  --records mixed_50=results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl \
  --records perspective_gpt54=results/perspective_stress50_hybrid_candidate_eval_records.jsonl \
  --records perspective_gpt41=results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl \
  --records partial_observability=results/partial_observability_api50_candidate_eval_records.jsonl \
  --markdown-out docs/api_listener_leave_one_out.md \
  --json-out results/api_listener_leave_one_out.json \
  --tex-out paper/tables/api_listener_leave_one_out.tex
```

The current report is `docs/api_listener_leave_one_out.md`.

## Cache-only selection regret audit

The all-candidate records also support a selector-regret audit: oracle candidate
success minus each method's selected-message success, averaged by scene. This
checks whether remaining failures are caused by missing good candidates or by
choosing the wrong candidate.

```bash
conda run -n cross_play python scripts/analyze_selection_regret.py \
  --markdown-out docs/selection_regret_audit.md \
  --json-out results/selection_regret_audit.json
```

The current report is `docs/selection_regret_audit.md`. Full-candidate
population-play has zero regret in the paper-facing API runs; after removing
coordinate fallbacks, consensus+info reduces regret to `0.040`, `0.033`, and
`0.013` in the mixed, perspective, and partial-observability checks.

## Cache-only candidate-pool robustness audit

The candidate-pool audit checks whether each scene contains an all-listener
robust candidate and whether each selector captures one. This reuses cached
all-candidate evaluations and makes no API calls.

```bash
conda run -n cross_play python scripts/analyze_candidate_pool.py \
  --markdown-out docs/candidate_pool_audit.md \
  --json-out results/candidate_pool_audit.json
```

The current report is `docs/candidate_pool_audit.md`. Every full-candidate run
has at least one robust candidate in all scenes, and population-play selects a
robust candidate in `1.000` of scenes. After exact coordinates are removed, the
alternate-model perspective audit has robust non-coordinate candidates in
`0.660` of scenes, while consensus+info matches the oracle in `0.920`.

## Cache-only candidate-budget audit

The candidate-budget audit checks how quickly robust held-out candidates appear
as the generated candidate budget grows from the first candidate to all four
candidate messages.

```bash
conda run -n cross_play python scripts/analyze_candidate_budget.py \
  --markdown-out docs/candidate_budget_audit.md \
  --json-out results/candidate_budget_audit.json
```

The current report is `docs/candidate_budget_audit.md`. In the alternate-model
perspective audit, robust-scene coverage rises from `0.380` at `K=1` to `0.660`
at `K=3` and `1.000` at `K=4`.

## Cache-only candidate-role selection audit

The candidate-role audit maps each selected message back to its original
generated candidate slot. It checks whether selectors choose the short
attribute-only candidate, a relational/spatial fallback, or an exact coordinate
fallback.

```bash
conda run -n cross_play python scripts/analyze_candidate_role_selection.py \
  --markdown-out docs/candidate_role_selection_audit.md \
  --json-out results/candidate_role_selection_audit.json
```

The current report is `docs/candidate_role_selection_audit.md`. In the harder
full-candidate perspective and partial-observability runs, population-play uses
the coordinate fallback in `1.000` of scenes; after exact coordinates are
removed, consensus+info uses the short attribute slot in `0.000` of those
harder scenes.

## Cache-only random-candidate baseline

The random-candidate baseline compares selectors with the exact expected
success of choosing uniformly from the same generated candidate pool. This
checks whether selector gains are larger than what would happen if any
candidate were chosen.

```bash
conda run -n cross_play python scripts/analyze_random_candidate_baseline.py \
  --markdown-out docs/random_candidate_baseline.md \
  --json-out results/random_candidate_baseline.json
```

The current report is `docs/random_candidate_baseline.md`. Population-play
beats the uniform-random selector in all four full-candidate runs; consensus+info
beats it in all three no-coordinate runs.

## Cache-only message-length audit

The message-length audit checks whether selector gains are just a consequence
of choosing longer generated messages. It reuses cached selected-message records
and makes no API calls.

```bash
conda run -n cross_play python scripts/analyze_message_length_audit.py \
  --markdown-out docs/message_length_audit.md \
  --json-out results/message_length_audit.json
```

The current report is `docs/message_length_audit.md`. Full-candidate
population-play messages average `6.82`, `10.22`, `10.22`, and `9.66` tokens,
while direct messages can be longer than mirror self-play and still less
successful.

## Cache-only listener-disagreement audit

The listener-disagreement audit checks whether a selected message produces
unanimous held-out success, unanimous failure, or split outcomes across held-out
listeners in the same scene.

```bash
conda run -n cross_play python scripts/analyze_listener_disagreement.py \
  --markdown-out docs/listener_disagreement_audit.md \
  --json-out results/listener_disagreement_audit.json
```

The current report is `docs/listener_disagreement_audit.md`. Mirror self-play
has split held-out outcomes in `0.080`, `0.180`, `0.360`, and `0.500` of scenes
across the full-candidate API runs, while population-play has `0.000`.

## Cache-only listener-confidence audit

The listener-confidence audit checks whether held-out listener confidence and
ambiguity self-reports diagnose selected-message failures. It reuses cached
selected-message records and makes no API calls.

```bash
conda run -n cross_play python scripts/analyze_listener_confidence_audit.py \
  --markdown-out docs/listener_confidence_audit.md \
  --json-out results/listener_confidence_audit.json
```

The current report is `docs/listener_confidence_audit.md`. In the
alternate-model perspective runs, ambiguity flags are `0.000`, yet mirror
self-play produces high-confidence failures in `0.147` of full-candidate
listener rows and `0.280` of no-coordinate listener rows.

## Cache-only failure taxonomy audit

The failure-taxonomy audit combines the rubric-coded listener-level mirror
failures used in the paper. It makes no API calls and writes the combined paper
table.

```bash
conda run -n cross_play python scripts/analyze_failure_taxonomy.py \
  --markdown-out docs/failure_taxonomy_audit.md \
  --json-out results/failure_taxonomy_audit.json \
  --tex-out paper/tables/failure_taxonomy_combined.tex
```

The current report is `docs/failure_taxonomy_audit.md`: `147` of `152` coded
listener-level mirror failures are `underspecified_distractor` cases and `5`
are `perspective_frame_error` cases.

## Rule-based ambiguity verifier

The rule-based verifier is an independent non-LLM check on the coded failure
taxonomy. It parses selected messages for visible target attributes, exact
row/column mentions, and perspective-sensitive left/right cues.

```bash
conda run -n cross_play python scripts/analyze_rule_based_ambiguity.py \
  --markdown-out docs/rule_based_ambiguity_verifier.md \
  --json-out results/rule_based_ambiguity_verifier.json \
  --units-out results/rule_based_ambiguity_verifier_units.jsonl
```

The current report is `docs/rule_based_ambiguity_verifier.md`: on the `152`
coded mirror-failure rows, symbolic ambiguity recall is `1.000`.

## Cache-only interaction-memory rule audit

The interaction-memory rule audit derives a small future speaker-rule list from
the coded mirror failures and checks whether cached repair selectors instantiate
the relevant cue on those same failure scenes. It makes no API calls.

```bash
conda run -n cross_play python scripts/analyze_interaction_memory_rules.py \
  --markdown-out docs/interaction_memory_rules.md \
  --json-out results/interaction_memory_rules.json
```

The current report is `docs/interaction_memory_rules.md`: the `152` coded
failure rows collapse into two active rules, and cached population or
consensus+info repairs satisfy the derived cue in `1.000` of failure scenes.

## Interaction-memory prompt rerun

This bounded GPT-5.5 prompt rerun asks the speaker to use the distilled
interaction-memory rules on sampled mirror-failure items from the prepared
human-validation packet.

```bash
conda run -n cross_play python scripts/run_interaction_memory_rerun.py \
  --max-items 15 --temperature omit \
  --records-out results/interaction_memory_prompt_rerun_records.jsonl \
  --messages-out results/interaction_memory_prompt_rerun_messages.jsonl \
  --summary-out results/interaction_memory_prompt_rerun_summary.json \
  --markdown-out docs/interaction_memory_prompt_rerun.md
```

The current report is `docs/interaction_memory_prompt_rerun.md`: on 15
human-packet mirror-failure items, the interaction-memory prompt reaches
`1.000` held-out success versus mirror self-play `0.422`, matching
population-play at `1.000`.

## Cache-only qualitative failure examples

The qualitative appendix selects representative cached scenes where
mirror-selected messages fail at least one held-out listener and a population or
consensus+info repair succeeds.

```bash
conda run -n cross_play python scripts/make_qualitative_examples.py \
  --markdown-out docs/qualitative_failure_examples.md \
  --json-out results/qualitative_failure_examples.json
```

The current report is `docs/qualitative_failure_examples.md`. It includes four
examples: perspective underspecification, a frame-sensitive relation, a
partial-observability visible-distractor ambiguity, and a no-coordinate
consensus+info repair.

## Reviewer checklist

The original workshop plan includes a pre-submission checklist. This command
materializes that list against the current artifacts and fails if any item is no
longer supported.

```bash
conda run -n cross_play python scripts/make_reviewer_checklist.py \
  --markdown-out docs/reviewer_checklist.md \
  --json-out results/reviewer_checklist.json
```

The current report is `docs/reviewer_checklist.md`.

## Cache-only plan coverage audit

The plan-coverage audit maps the original workshop plan to the current
artifacts and keeps core paper coverage separate from partial or open stretch
work. It makes no API calls.

```bash
conda run -n cross_play python scripts/audit_plan_coverage.py \
  --markdown-out docs/plan_coverage_audit.md \
  --json-out results/plan_coverage_audit.json
```

The current report is `docs/plan_coverage_audit.md`: core scope has `17`
covered, `2` partial, and `0` open items; stretch scope has `4` covered, `1`
partial, and `0` open items.

## Artifact guide

For a reviewer-facing map from paper claims to source scenes, cached result
files, tables, and verification outputs, generate:

```bash
conda run -n cross_play python scripts/make_artifact_guide.py \
  --out docs/artifact_guide.md
```

The current guide is `docs/artifact_guide.md`.

## Tiny cached API pilot

Run this only after inspecting the local pilot. It uses
`/home/eston/colm_workshop/apikey.txt`, caches every response under
`data/cached_responses/`, and defaults to a four-scene smoke test.

```bash
conda run -n cross_play python scripts/run_api_pilot.py --max-scenes 4
```

Use the API pilot to check JSON validity, listener prompt behavior, and whether
the local difficulty patterns survive real model calls before scaling.

## Current methods

- `template`: deterministic attribute plus coordinate description.
- `direct`: one local speaker message with known hard-case weaknesses.
- `best_of_k_shortest`: controls for candidate multiplicity.
- `mirror_selfplay`: selects against one training listener.
- `population_play`: selects against three heterogeneous training listeners.
- `oracle_upper_bound`: best candidate under held-out listeners.

The local simulator is not a paper result. Its job is to debug the benchmark,
selection code, metrics, and scenario difficulty before spending API budget.

## Current paper draft

The current workshop-paper draft is maintained in `paper/main.tex` and compiles
to `paper/main.pdf` with:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The COLM-formatted submission target is generated from that source:

```bash
conda run -n cross_play python scripts/export_colm_submission.py \
  --source paper/main.tex \
  --out paper/colm2026_submission.tex

cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error colm2026_submission.tex
```

This produces `paper/colm2026_submission.pdf`.

The strongest current result is the 50-scene perspective-stress replication:
mirror self-play reaches same-play `1.000` but cross-play `0.813`, while
population-play reaches cross-play `1.000` on the same API-generated candidates.
An exact-coordinate ablation on the alternate-model audit shows a sharper
limitation: without row/column candidates, robust non-coordinate candidates
still exist, but the current local population selector no longer finds them
reliably. The same cache-only filter on the mixed pilot shows that a simple
consensus+info selector recovers much of the no-coordinate oracle. See
`docs/protocol_and_prompts.md`, `results/benchmark_integrity_audit.md`,
`results/submission_readiness_audit.md`, `docs/paper_claims_iteration_002.md`,
`docs/artifact_guide.md`,
`docs/api_listener_leave_one_out.md`,
`docs/cross_model_failure_overlap.md`,
`docs/selection_regret_audit.md`,
`docs/candidate_pool_audit.md`,
`docs/candidate_budget_audit.md`,
`docs/local_stronger_plan_k8.md`,
`docs/random_candidate_baseline.md`,
`docs/listener_disagreement_audit.md`,
`docs/rule_based_ambiguity_verifier.md`,
`docs/qualitative_failure_examples.md`,
`docs/reviewer_checklist.md`,
`docs/plan_coverage_audit.md`,
`docs/local_benchmark600_check.md`,
`docs/partial_observability_local_check.md`,
`docs/partial_observability_api50_check.md`, and `REPRODUCE.md` for the exact
artifact trail.
