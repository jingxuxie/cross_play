# Reproducing Current PRAG-CrossPlay Artifacts

All commands assume the workspace root:

```bash
cd /home/eston/colm_workshop/cross_play
```

The current experiments use the `cross_play` conda environment and cache OpenAI
Responses API calls under `data/cached_responses/`. Re-running the same commands
should mostly reuse cached responses.

## Cache and token accounting

This cache-only report summarizes stored OpenAI Responses API usage fields. It
does not estimate dollar cost, because final billing can depend on account,
discount, model, and date-specific pricing.

```bash
conda run -n cross_play python scripts/analyze_api_token_accounting.py \
  --markdown-out docs/api_token_accounting.md \
  --json-out results/api_token_accounting.json
```

Current result: `7,113` cached Responses API files contain `2,052,279` total
tokens, with `0` missing usage records.

## Local sanity pilot

```bash
conda run -n cross_play python scripts/run_local_pilot.py
```

Outputs:

- `data/dev_scenes.jsonl`
- `results/local_pilot_records.jsonl`
- `results/local_pilot_summary.json`
- `results/local_pilot_summary.md`

## Benchmark-scale local sanity check

This no-API check exercises the 600-scene scale from the original workshop plan
with deterministic local listeners. It supports the released benchmark artifact;
the paper-facing listener results are still the bounded cached API runs below.

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

Current local benchmark-scale result:

- `600` scenes balanced across four initial scenario families;
- mirror self-play: cross-play `0.631`, same-play `1.000`, gap `0.369`;
- perspective-shift mirror cross-play: `0.158`;
- population-play, template, and oracle candidate: cross-play `1.000`.

## Local stronger-plan K=8 diagnostic

This no-API diagnostic exercises the stronger-plan scale with `1,000` initial
family scenes, `200` partial-observability scenes, and K=8 local candidate
slots. It supports artifact-scale and candidate-diversity claims only; the
paper-facing listener results remain the bounded cached API runs.

```bash
conda run -n cross_play python scripts/analyze_local_stronger_plan.py \
  --scene-out data/local_stronger_plan1200_scenes.jsonl \
  --markdown-out docs/local_stronger_plan_k8.md \
  --json-out results/local_stronger_plan_k8.json
```

Current local stronger-plan result:

- `1,200` local scenes: `250` each for the four initial scenario families and
  `200` partial-observability scenes;
- No-coordinate oracle success rises from `0.808` at K=4 to `0.995` at K=8
  over all `1,200` local scenes;
- no-coordinate consensus+info reaches `0.993` at K=8;
- full-candidate local K=8 population-play reaches `1.000`.

## Optional partial-observability local stress check

This no-API extension covers private-landmark scenes where the speaker can see a
landmark that is hidden from the listener. The local result is a benchmark
sanity check; the cached API support run below is the paper-facing
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

Current local result:

- direct: cross-play `0.493`;
- mirror self-play: cross-play `0.653`, same-play `1.000`, gap `0.347`;
- population-play: cross-play `1.000`, same-play `1.000`;
- oracle upper bound: cross-play `1.000`.

## Exploratory partial-observability API check

This bounded API support run evaluates the 50 private-landmark scenes. It checks
whether the partial-observability extension produces the same kind of same-play
versus cross-play gap under API listeners. Re-running should mostly use cached
responses after the first run.

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

conda run -n cross_play python scripts/analyze_results.py \
  results/partial_observability_api50_records.jsonl \
  --summary-out results/partial_observability_api50_summary.json \
  --markdown-out results/partial_observability_api50_summary.md

conda run -n cross_play python scripts/compare_methods.py \
  results/partial_observability_api50_records.jsonl \
  --method-a hybrid_local_population_api_eval \
  --method-b hybrid_local_mirror_api_eval \
  --json-out results/partial_observability_api50_population_vs_mirror_paired.json \
  --markdown-out results/partial_observability_api50_population_vs_mirror_paired.md

conda run -n cross_play python scripts/run_candidate_filter_ablation.py \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --candidates results/partial_observability_api50_candidates.jsonl \
  --candidate-records results/partial_observability_api50_candidate_eval_records.jsonl \
  --records-out results/partial_observability_api50_no_coord_records.jsonl \
  --summary-out results/partial_observability_api50_no_coord_summary.json \
  --markdown-out results/partial_observability_api50_no_coord_summary.md \
  --paired-json-out results/partial_observability_api50_no_coord_population_vs_mirror_paired.json \
  --paired-markdown-out results/partial_observability_api50_no_coord_population_vs_mirror_paired.md \
  --audit-out results/partial_observability_api50_no_coord_audit.jsonl \
  --table-out paper/tables/partial_observability_api50_no_coord.md \
  --tex-out paper/tables/partial_observability_api50_no_coord.tex \
  --scenario-table-out paper/tables/partial_observability_api50_no_coord_by_scenario.md \
  --scenario-tex-out paper/tables/partial_observability_api50_no_coord_by_scenario.tex

conda run -n cross_play python scripts/export_failures.py \
  results/partial_observability_api50_records.jsonl \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --method hybrid_local_mirror_api_eval \
  --out results/partial_observability_api50_mirror_failures.csv

conda run -n cross_play python scripts/code_failures_with_context.py \
  --failures results/partial_observability_api50_mirror_failures.csv \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --out results/partial_observability_api50_mirror_failures_coded.csv \
  --table-out paper/tables/partial_observability_api50_error_counts.md \
  --tex-out paper/tables/partial_observability_api50_error_counts.tex

conda run -n cross_play python scripts/export_failures.py \
  results/partial_observability_api50_no_coord_records.jsonl \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --method no_coord_mirror \
  --out results/partial_observability_api50_no_coord_mirror_failures.csv

conda run -n cross_play python scripts/code_failures_with_context.py \
  --failures results/partial_observability_api50_no_coord_mirror_failures.csv \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --out results/partial_observability_api50_no_coord_mirror_failures_coded.csv \
  --table-out paper/tables/partial_observability_api50_no_coord_error_counts.md \
  --tex-out paper/tables/partial_observability_api50_no_coord_error_counts.tex

conda run -n cross_play python scripts/analyze_partial_observability_api.py \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --records results/partial_observability_api50_records.jsonl \
  --candidates results/partial_observability_api50_candidates.jsonl \
  --no-coord-records results/partial_observability_api50_no_coord_records.jsonl \
  --mirror-failures-coded results/partial_observability_api50_mirror_failures_coded.csv \
  --no-coord-mirror-failures-coded results/partial_observability_api50_no_coord_mirror_failures_coded.csv \
  --markdown-out docs/partial_observability_api50_check.md \
  --json-out results/partial_observability_api50_check.json
```

Current exploratory result:

- mirror self-play: cross-play `0.667`, same-play `1.000`, gap `0.333`;
- population-play: cross-play `1.000`, same-play `1.000`;
- after removing exact row/column candidates, consensus+info reaches `0.987`
  while mirror self-play reaches `0.607`;
- the generated candidate audit found `0` private-landmark references.
- rubric coding classifies all `50` full-run mirror failures and all `59`
  no-coordinate mirror failures as `underspecified_distractor`.

## Mixed 50-scene hybrid pilot

```bash
conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --max-scenes 50 \
  --model gpt-5.4-nano \
  --records-out results/hybrid_api_pilot50_allcand_records.jsonl \
  --summary-out results/hybrid_api_pilot50_allcand_summary.json \
  --candidates-out results/hybrid_api_pilot50_allcand_candidates.jsonl \
  --all-candidate-records-out results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl
```

## Perspective-stress replication

```bash
conda run -n cross_play python scripts/generate_scenes.py \
  --out data/perspective_stress50_scenes.jsonl \
  --split perspective_stress \
  --seed 20260627 \
  --unique 0 --contrast 0 --relational 0 --perspective 50

conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --max-scenes 50 \
  --model gpt-5.4-nano \
  --records-out results/perspective_stress50_hybrid_records.jsonl \
  --summary-out results/perspective_stress50_hybrid_summary.json \
  --candidates-out results/perspective_stress50_hybrid_candidates.jsonl \
  --all-candidate-records-out results/perspective_stress50_hybrid_candidate_eval_records.jsonl \
  --checkpoint-every 1
```

Current headline result:

- mirror self-play: cross-play `0.813`, same-play `1.000`;
- population-play: cross-play `1.000`, same-play `1.000`;
- paired population-minus-mirror difference: `0.187`, 95% CI `[0.100, 0.287]`.

## Analysis artifacts

```bash
conda run -n cross_play python scripts/analyze_results.py \
  results/perspective_stress50_hybrid_records.jsonl \
  --summary-out results/perspective_stress50_hybrid_summary.json \
  --markdown-out results/perspective_stress50_hybrid_summary.md

conda run -n cross_play python scripts/compare_methods.py \
  results/perspective_stress50_hybrid_records.jsonl \
  --method-a hybrid_local_population_api_eval \
  --method-b hybrid_local_mirror_api_eval \
  --json-out results/perspective_stress50_population_vs_mirror_paired.json \
  --markdown-out results/perspective_stress50_population_vs_mirror_paired.md

conda run -n cross_play python scripts/export_failures.py \
  results/perspective_stress50_hybrid_records.jsonl \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --method hybrid_local_mirror_api_eval \
  --out results/perspective_stress50_mirror_failures.csv

conda run -n cross_play python scripts/make_paper_tables.py \
  --summary results/perspective_stress50_hybrid_summary.json \
  --paired results/perspective_stress50_population_vs_mirror_paired.json \
  --out-dir paper/tables \
  --name perspective_stress50

conda run -n cross_play python scripts/make_analysis_artifacts.py
```

## Alternate held-out model audit

This reuses `results/perspective_stress50_hybrid_candidates.jsonl` and evaluates
the same candidates with `gpt-4.1-nano` held-out listeners.

```bash
conda run -n cross_play python scripts/evaluate_candidate_file_api.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --candidates results/perspective_stress50_hybrid_candidates.jsonl \
  --model gpt-4.1-nano \
  --records-out results/perspective_stress50_gpt41nano_records.jsonl \
  --summary-out results/perspective_stress50_gpt41nano_summary.json \
  --all-candidate-records-out results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl \
  --audit-out results/perspective_stress50_gpt41nano_audit.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/compare_methods.py \
  results/perspective_stress50_gpt41nano_records.jsonl \
  --method-a hybrid_local_population_api_eval \
  --method-b hybrid_local_mirror_api_eval \
  --json-out results/perspective_stress50_gpt41nano_population_vs_mirror_paired.json \
  --markdown-out results/perspective_stress50_gpt41nano_population_vs_mirror_paired.md

conda run -n cross_play python scripts/export_failures.py \
  results/perspective_stress50_gpt41nano_records.jsonl \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --method hybrid_local_mirror_api_eval \
  --out results/perspective_stress50_gpt41nano_mirror_failures.csv

conda run -n cross_play python scripts/code_failures_with_context.py \
  --failures results/perspective_stress50_gpt41nano_mirror_failures.csv \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --out results/perspective_stress50_gpt41nano_mirror_failures_coded.csv \
  --table-out paper/tables/perspective_stress50_gpt41nano_error_counts.md \
  --tex-out paper/tables/perspective_stress50_gpt41nano_error_counts.tex
```

Current alternate-model result:

- mirror self-play: cross-play `0.713`, same-play `1.000`;
- population-play: cross-play `1.000`, same-play `1.000`;
- paired population-minus-mirror difference: `0.287`, 95% CI `[0.193, 0.380]`.

## Cross-model selected-message listener audit

This follow-up reuses cached speaker candidates and selected messages, then
evaluates those messages with additional held-out listener families. The
`gpt-5.5` rows are selected-message audits, not new speaker calls.

```bash
conda run -n cross_play python scripts/run_selected_listener_audit.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --candidates results/perspective_stress50_hybrid_candidates.jsonl \
  --model gpt-5.5 \
  --records-out results/gpt55_perspective_selected_records.jsonl \
  --summary-out results/gpt55_perspective_selected_summary.json \
  --markdown-out docs/gpt55_perspective_selected_audit.md \
  --paired-json-out results/gpt55_perspective_selected_population_vs_mirror_paired.json \
  --paired-markdown-out results/gpt55_perspective_selected_population_vs_mirror_paired.md \
  --audit-out results/gpt55_perspective_selected_audit.jsonl \
  --include-existing-oracle-message \
  --existing-candidate-records results/perspective_stress50_gpt41nano_records.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/run_selected_listener_audit.py \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --candidates results/partial_observability_api50_candidates.jsonl \
  --model gpt-4.1-nano \
  --temperature 0.0 \
  --reasoning-effort omit \
  --records-out results/gpt41_partial_observability_selected_records.jsonl \
  --summary-out results/gpt41_partial_observability_selected_summary.json \
  --markdown-out docs/gpt41_partial_observability_selected_audit.md \
  --paired-json-out results/gpt41_partial_observability_selected_population_vs_mirror_paired.json \
  --paired-markdown-out results/gpt41_partial_observability_selected_population_vs_mirror_paired.md \
  --audit-out results/gpt41_partial_observability_selected_audit.jsonl \
  --include-existing-oracle-message \
  --existing-candidate-records results/partial_observability_api50_records.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/run_selected_listener_audit.py \
  --scene-file data/partial_observability_local50_scenes.jsonl \
  --candidates results/partial_observability_api50_candidates.jsonl \
  --model gpt-5.5 \
  --records-out results/gpt55_partial_observability_selected_records.jsonl \
  --summary-out results/gpt55_partial_observability_selected_summary.json \
  --markdown-out docs/gpt55_partial_observability_selected_audit.md \
  --paired-json-out results/gpt55_partial_observability_selected_population_vs_mirror_paired.json \
  --paired-markdown-out results/gpt55_partial_observability_selected_population_vs_mirror_paired.md \
  --audit-out results/gpt55_partial_observability_selected_audit.jsonl \
  --include-existing-oracle-message \
  --existing-candidate-records results/partial_observability_api50_records.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/analyze_cross_model_listener_audit.py
```

Current cross-model result: population-play is `1.000` in all six
setting/listener rows, while GPT-5.5 mirror self-play is `0.673` on
perspective stress and `0.653` on partial observability.

## Cross-model failure overlap audit

This cache-only companion audit checks whether GPT-5.5 fixes the same
mirror-selected messages that fail under earlier held-out listener families. It
also attaches rule-based ambiguity labels to the failed scene-level messages.

```bash
conda run -n cross_play python scripts/analyze_cross_model_failure_overlap.py \
  --json-out results/cross_model_failure_overlap.json \
  --markdown-out docs/cross_model_failure_overlap.md \
  --units-out results/cross_model_failure_overlap_units.jsonl
```

Current result:

- in perspective stress, `20` of `22` GPT-4.1 mirror-failure scenes also fail
  under GPT-5.5;
- in partial observability, `26` of `26` GPT-4.1 mirror-failure scenes also fail
  under GPT-5.5;
- all GPT-5.5 mirror-failure scenes are symbolic-verifier positives, and
  GPT-5.5 population-play has zero scene-level failures in both settings.

## GPT-5.5 speaker smoke

This auxiliary Experiment 3 smoke compares existing perspective-stress speaker
candidates with newly generated GPT-5.5 speaker candidates on the same first 10
scenes. The analysis command below is offline once the JSONL artifacts are
present.

```bash
conda run -n cross_play python scripts/analyze_gpt55_speaker_smoke.py \
  --json-out results/gpt55_speaker_smoke.json \
  --markdown-out docs/gpt55_speaker_smoke_report.md
```

Current result: on the same first 10 scenes, GPT-5.5 speaker direct-first is
`1.000` and mirror self-play is `0.867`, versus `0.800` and `0.667` for the
existing speaker candidates; population-play is `1.000` for both. The full
50-scene speaker audit has GPT-5.5 direct-first `0.993`, mirror self-play
`0.853` despite same-play `1.000`, and population-play `1.000`. This is now
paper-facing Experiment 3 evidence under GPT-5.5 held-out listeners.

To regenerate the raw API artifacts, run the following cache-backed commands.
They may spend API budget if the corresponding files under
`data/cached_responses/` are absent.

```bash
conda run -n cross_play python scripts/evaluate_candidate_file_api.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --candidates results/perspective_stress50_hybrid_candidates.jsonl \
  --model gpt-5.5 \
  --temperature none \
  --reasoning-effort none \
  --records-out results/gpt55_existing_speaker_perspective10_records.jsonl \
  --summary-out results/gpt55_existing_speaker_perspective10_summary.json \
  --all-candidate-records-out results/gpt55_existing_speaker_perspective10_candidate_eval_records.jsonl \
  --audit-out results/gpt55_existing_speaker_perspective10_audit.jsonl \
  --max-scenes 10 \
  --checkpoint-every 1

conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --max-scenes 10 \
  --k 4 \
  --model gpt-5.5 \
  --temperature none \
  --reasoning-effort none \
  --records-out results/gpt55_speaker_perspective10_records.jsonl \
  --summary-out results/gpt55_speaker_perspective10_summary.json \
  --candidates-out results/gpt55_speaker_perspective10_candidates.jsonl \
  --all-candidate-records-out results/gpt55_speaker_perspective10_candidate_eval_records.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --max-scenes 20 \
  --k 4 \
  --model gpt-5.5 \
  --temperature none \
  --reasoning-effort none \
  --records-out results/gpt55_speaker_perspective20_records.jsonl \
  --summary-out results/gpt55_speaker_perspective20_summary.json \
  --candidates-out results/gpt55_speaker_perspective20_candidates.jsonl \
  --all-candidate-records-out results/gpt55_speaker_perspective20_candidate_eval_records.jsonl \
  --checkpoint-every 1

conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --max-scenes 50 \
  --k 4 \
  --model gpt-5.5 \
  --temperature none \
  --reasoning-effort none \
  --records-out results/gpt55_speaker_perspective50_records.jsonl \
  --summary-out results/gpt55_speaker_perspective50_summary.json \
  --candidates-out results/gpt55_speaker_perspective50_candidates.jsonl \
  --all-candidate-records-out results/gpt55_speaker_perspective50_candidate_eval_records.jsonl \
  --checkpoint-every 1
```

## GPT-5.5 K=8 no-coordinate audit

Experiment 4 evaluates whether the no-coordinate limitation persists when the
speaker gets a dedicated K=8 GPT-5.5 prompt that forbids exact row/column
references.

The cache-backed raw run is:

```bash
conda run -n cross_play python scripts/run_hybrid_api_pilot.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --max-scenes 50 \
  --k 8 \
  --model gpt-5.5 \
  --speaker-prompt no_coordinates \
  --temperature none \
  --reasoning-effort none \
  --records-out results/gpt55_no_coord_k8_perspective50_records.jsonl \
  --summary-out results/gpt55_no_coord_k8_perspective50_summary.json \
  --candidates-out results/gpt55_no_coord_k8_perspective50_candidates.jsonl \
  --all-candidate-records-out results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl \
  --checkpoint-every 1
```

The no-coordinate replay and comparison are offline once those records exist:

```bash
conda run -n cross_play python scripts/run_candidate_filter_ablation.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --candidates results/gpt55_no_coord_k8_perspective50_candidates.jsonl \
  --candidate-records results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl \
  --records-out results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl \
  --summary-out results/gpt55_no_coord_k8_perspective50_no_coord_summary.json \
  --markdown-out results/gpt55_no_coord_k8_perspective50_no_coord_summary.md \
  --paired-json-out results/gpt55_no_coord_k8_perspective50_no_coord_population_vs_mirror_paired.json \
  --paired-markdown-out results/gpt55_no_coord_k8_perspective50_no_coord_population_vs_mirror_paired.md \
  --audit-out results/gpt55_no_coord_k8_perspective50_no_coord_audit.jsonl \
  --table-out paper/tables/gpt55_no_coord_k8_perspective50_no_coord.md \
  --tex-out paper/tables/gpt55_no_coord_k8_perspective50_no_coord.tex \
  --scenario-table-out paper/tables/gpt55_no_coord_k8_perspective50_no_coord_by_scenario.md \
  --scenario-tex-out paper/tables/gpt55_no_coord_k8_perspective50_no_coord_by_scenario.tex

conda run -n cross_play python scripts/analyze_gpt55_no_coord_k8.py \
  --json-out results/gpt55_no_coord_k8_comparison.json \
  --markdown-out docs/gpt55_no_coord_k8_report.md
```

Current result: the K=8 no-coordinate prompt produced `0`
exact-coordinate candidates across `400` candidates. Oracle remains `1.000`,
shortest reaches `1.000`, population-play improves from `0.833` to `0.993`,
and consensus+info drops from `0.993` to `0.900`, so the safe claim is
generation availability plus selector-design bottleneck.

## GPT-5.5 follow-up plan status

This cache/offline audit maps `additional_experiments_gpt55_plan.md` to current
artifacts and makes the claim boundary explicit.

```bash
conda run -n cross_play python scripts/audit_gpt55_followup_plan.py \
  --json-out results/gpt55_followup_plan_status.json \
  --markdown-out docs/gpt55_followup_plan_status.md
```

Current result: `5` follow-up experiments covered, `1` partial, and `0` future,
with `0` missing evidence paths. The report treats the 50-scene GPT-5.5 speaker
audit and API K=8 no-coordinate generation as covered; human listener validation
remains incomplete.

## Human validation packet

This prepares the optional 20-item human validation sample. It does not include
collected annotations and should not be cited as human-validation evidence.

```bash
conda run -n cross_play python scripts/make_human_validation_packet.py \
  --items-out data/human_validation_items.jsonl \
  --responses-out data/human_validation_response_template.csv \
  --answer-key-out results/human_validation_answer_key.json \
  --markdown-out docs/human_validation_packet.md \
  --html-out docs/human_validation_packet.html
```

Current packet: `10` perspective mirror failures, `5` partial-observability
mirror failures, and `5` mirror-success controls. Participant-facing files omit
target IDs, condition labels, scene IDs, and held-out success rates.

## No-exact-coordinate ablation

This cache-only ablation reuses the alternate-model all-candidate records. It
does not make API calls.

```bash
conda run -n cross_play python scripts/run_candidate_filter_ablation.py \
  --scene-file data/perspective_stress50_scenes.jsonl \
  --candidates results/perspective_stress50_hybrid_candidates.jsonl \
  --candidate-records results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl \
  --records-out results/perspective_stress50_gpt41nano_no_coord_records.jsonl \
  --summary-out results/perspective_stress50_gpt41nano_no_coord_summary.json \
  --markdown-out results/perspective_stress50_gpt41nano_no_coord_summary.md \
  --paired-json-out results/perspective_stress50_gpt41nano_no_coord_population_vs_mirror_paired.json \
  --paired-markdown-out results/perspective_stress50_gpt41nano_no_coord_population_vs_mirror_paired.md \
  --audit-out results/perspective_stress50_gpt41nano_no_coord_audit.jsonl \
  --table-out paper/tables/perspective_stress50_gpt41nano_no_coord.md \
  --tex-out paper/tables/perspective_stress50_gpt41nano_no_coord.tex \
  --scenario-table-out paper/tables/perspective_stress50_gpt41nano_no_coord_by_scenario.md \
  --scenario-tex-out paper/tables/perspective_stress50_gpt41nano_no_coord_by_scenario.tex

conda run -n cross_play python scripts/compare_methods.py \
  results/perspective_stress50_gpt41nano_no_coord_records.jsonl \
  --method-a no_coord_consensus_info \
  --method-b no_coord_mirror \
  --json-out results/perspective_stress50_gpt41nano_no_coord_consensus_info_vs_mirror_paired.json \
  --markdown-out results/perspective_stress50_gpt41nano_no_coord_consensus_info_vs_mirror_paired.md
```

Current no-exact-coordinate result:

- mirror self-play: cross-play `0.580`, same-play `1.000`;
- population-play: cross-play `0.420`, same-play `0.520`;
- consensus+info selector: cross-play `0.760`;
- text-only informativeness prior: cross-play `0.760`;
- oracle candidate upper bound: cross-play `0.793`.

Mixed-pilot no-exact-coordinate ablation:

```bash
conda run -n cross_play python scripts/run_candidate_filter_ablation.py \
  --scene-file data/dev_scenes.jsonl \
  --candidates results/hybrid_api_pilot50_allcand_candidates.jsonl \
  --candidate-records results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl \
  --records-out results/hybrid_api_pilot50_no_coord_records.jsonl \
  --summary-out results/hybrid_api_pilot50_no_coord_summary.json \
  --markdown-out results/hybrid_api_pilot50_no_coord_summary.md \
  --paired-json-out results/hybrid_api_pilot50_no_coord_population_vs_mirror_paired.json \
  --paired-markdown-out results/hybrid_api_pilot50_no_coord_population_vs_mirror_paired.md \
  --audit-out results/hybrid_api_pilot50_no_coord_audit.jsonl \
  --table-out paper/tables/mixed50_no_coord.md \
  --tex-out paper/tables/mixed50_no_coord.tex \
  --scenario-table-out paper/tables/mixed50_no_coord_by_scenario.md \
  --scenario-tex-out paper/tables/mixed50_no_coord_by_scenario.tex

conda run -n cross_play python scripts/compare_methods.py \
  results/hybrid_api_pilot50_no_coord_records.jsonl \
  --method-a no_coord_consensus_info \
  --method-b no_coord_mirror \
  --json-out results/hybrid_api_pilot50_no_coord_consensus_info_vs_mirror_paired.json \
  --markdown-out results/hybrid_api_pilot50_no_coord_consensus_info_vs_mirror_paired.md
```

Current mixed no-exact-coordinate result:

- mirror self-play: cross-play `0.787`, same-play `0.880`;
- population-play: cross-play `0.773`, same-play `0.813`;
- consensus+info selector: cross-play `0.920`;
- text-only informativeness prior: cross-play `0.900`;
- oracle candidate upper bound: cross-play `0.960`.

Selection-mechanism summaries:

```bash
conda run -n cross_play python scripts/analyze_selection_mechanisms.py \
  --name stress-full \
  --audit results/perspective_stress50_gpt41nano_audit.jsonl \
  --records results/perspective_stress50_gpt41nano_records.jsonl \
  --markdown-out paper/tables/selection_mechanisms_stress_full.md \
  --tex-out paper/tables/selection_mechanisms_stress_full.tex

conda run -n cross_play python scripts/analyze_selection_mechanisms.py \
  --name stress-no-coord \
  --audit results/perspective_stress50_gpt41nano_no_coord_audit.jsonl \
  --records results/perspective_stress50_gpt41nano_no_coord_records.jsonl \
  --markdown-out paper/tables/selection_mechanisms_stress_no_coord.md \
  --tex-out paper/tables/selection_mechanisms_stress_no_coord.tex

conda run -n cross_play python scripts/analyze_selection_mechanisms.py \
  --name mixed-no-coord \
  --audit results/hybrid_api_pilot50_no_coord_audit.jsonl \
  --records results/hybrid_api_pilot50_no_coord_records.jsonl \
  --markdown-out paper/tables/selection_mechanisms_mixed_no_coord.md \
  --tex-out paper/tables/selection_mechanisms_mixed_no_coord.tex
```

## Cache-only API listener leave-one-out check

This post-hoc mechanism check reuses all-candidate API listener evaluations.
For each scene, it holds out one API listener prompt for evaluation, selects
with one remaining prompt for API-mirror or the other two prompts for
API-population, and makes no API calls.

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

Current leave-one-out result:

- mixed 50: API-population `0.973`, API-mirror `0.953`;
- perspective stress with `gpt-5.4-nano`: API-population `0.933`,
  API-mirror `0.907`;
- perspective stress with `gpt-4.1-nano`: API-population `0.940`,
  API-mirror `0.847`;
- partial observability: API-population `0.940`, API-mirror `0.767`.

## Cache-only selection regret audit

This report computes oracle candidate success minus selected-message success by
scene. It checks whether failures are due to missing candidates or selector
regret.

```bash
conda run -n cross_play python scripts/analyze_selection_regret.py \
  --markdown-out docs/selection_regret_audit.md \
  --json-out results/selection_regret_audit.json
```

Current result:

- full-candidate population-play has zero regret in the mixed, perspective,
  alternate-model, and partial-observability API runs;
- mirror self-play regret is `0.093`, `0.187`, `0.287`, and `0.333` in those
  same runs;
- after exact row/column candidates are removed, consensus+info regret is
  `0.040`, `0.033`, and `0.013` in the mixed, perspective, and
  partial-observability checks.

## Cache-only candidate-pool robustness audit

This report checks whether all-listener-robust candidates are available in each
scene and whether each selector captures them.

```bash
conda run -n cross_play python scripts/analyze_candidate_pool.py \
  --markdown-out docs/candidate_pool_audit.md \
  --json-out results/candidate_pool_audit.json
```

Current result:

- every full-candidate run has at least one robust candidate in every scene;
- full-candidate population-play selects a robust candidate in `1.000` of
  scenes, while mirror robust-selection rates are `0.860`, `0.720`, `0.560`,
  and `0.500`;
- after exact row/column candidates are removed, robust non-coordinate
  candidate availability is `0.920`, `0.660`, and `1.000` in the mixed,
  alternate-model perspective, and partial-observability checks.

## Cache-only candidate-budget audit

This report computes oracle success and all-listener-robust candidate
availability after the first `K` generated candidates.

```bash
conda run -n cross_play python scripts/analyze_candidate_budget.py \
  --markdown-out docs/candidate_budget_audit.md \
  --json-out results/candidate_budget_audit.json
```

Current result:

- alternate-model perspective robust-scene coverage is `0.380` at `K=1`,
  `0.660` at `K=3`, and `1.000` at `K=4`;
- partial-observability robust-scene coverage is `0.620` at `K=1` and `1.000`
  at `K=3`.

## Cache-only candidate-role selection audit

This report maps each selected message back to the original generated candidate
slot. It checks whether selectors choose the short attribute-only candidate, a
relational/spatial fallback, or an exact coordinate fallback.

```bash
conda run -n cross_play python scripts/analyze_candidate_role_selection.py \
  --markdown-out docs/candidate_role_selection_audit.md \
  --json-out results/candidate_role_selection_audit.json
```

Current result:

- full-candidate population-play uses the coordinate fallback in `1.000` of
  perspective and partial-observability stress scenes;
- no-coordinate consensus+info uses the short attribute slot in `0.000` of the
  harder perspective and partial-observability scenes;
- no-coordinate consensus+info uses the relational/spatial slot in `0.580` of
  alternate-model perspective scenes and `0.460` of partial-observability
  scenes.

## Cache-only random-candidate baseline

This report computes the exact expected success of a selector that chooses
uniformly at random from the same generated candidate pool. It makes no API
calls.

```bash
conda run -n cross_play python scripts/analyze_random_candidate_baseline.py \
  --markdown-out docs/random_candidate_baseline.md \
  --json-out results/random_candidate_baseline.json
```

Current result:

- population-play beats the uniform-random selector by `0.135`, `0.285`,
  `0.343`, and `0.247` in the four full-candidate API runs;
- consensus+info beats the uniform-random selector by `0.100`, `0.218`, and
  `0.316` in the no-coordinate mixed, perspective, and partial-observability
  runs.

## Cache-only message-length audit

This audit checks whether selector gains are just verbosity. It reuses selected
message records and makes no API calls.

```bash
conda run -n cross_play python scripts/analyze_message_length_audit.py \
  --markdown-out docs/message_length_audit.md \
  --json-out results/message_length_audit.json
```

Current result:

- full-candidate population-play messages average `6.82`, `10.22`, `10.22`,
  and `9.66` tokens;
- population-play is `1.26`, `2.82`, `2.82`, and `3.16` tokens longer than
  mirror self-play on average in the four full-candidate runs;
- direct messages are longer than mirror in the perspective and
  partial-observability full-candidate runs while remaining less successful.

## Cache-only listener-disagreement audit

This report summarizes whether each selected message produces unanimous
held-out success, split held-out outcomes, or unanimous held-out failure across
the held-out listener prompts.

```bash
conda run -n cross_play python scripts/analyze_listener_disagreement.py \
  --markdown-out docs/listener_disagreement_audit.md \
  --json-out results/listener_disagreement_audit.json
```

Current result:

- full-candidate mirror split-outcome rates are `0.080`, `0.180`, `0.360`, and
  `0.500`, while full-candidate population-play has `0.000` split outcomes in
  all four runs;
- no-coordinate partial-observability consensus+info reduces split outcomes
  from mirror's `0.540` to `0.020`.

## Cache-only listener-confidence audit

This report checks whether held-out listener confidence and ambiguity flags
explain selected-message failures. It reuses selected-message records and makes
no API calls.

```bash
conda run -n cross_play python scripts/analyze_listener_confidence_audit.py \
  --markdown-out docs/listener_confidence_audit.md \
  --json-out results/listener_confidence_audit.json
```

Current result:

- in the alternate-model perspective runs, ambiguity flags are `0.000`;
- mirror self-play still produces high-confidence failures in `0.147` of
  full-candidate listener rows and `0.280` of no-coordinate listener rows;
- no-coordinate partial-observability consensus+info has `0.000`
  high-confidence failure rows.

## Cache-only failure taxonomy audit

This audit combines the rubric-coded listener-level mirror failures used in the
paper and writes the combined paper table.

```bash
conda run -n cross_play python scripts/analyze_failure_taxonomy.py \
  --markdown-out docs/failure_taxonomy_audit.md \
  --json-out results/failure_taxonomy_audit.json \
  --tex-out paper/tables/failure_taxonomy_combined.tex
```

Current result:

- `147` of `152` coded listener-level mirror failures are
  `underspecified_distractor` cases;
- the remaining `5` are `perspective_frame_error` cases;
- there are `0` other coded categories in the combined paper-facing failure
  sets.

## Rule-based ambiguity verifier

This non-LLM verifier parses selected messages for target attributes, exact
row/column mentions, and perspective-sensitive left/right cues. It makes no API
calls and checks whether the coded mirror failures are predictable from the
listener-visible scene alone.

```bash
conda run -n cross_play python scripts/analyze_rule_based_ambiguity.py \
  --markdown-out docs/rule_based_ambiguity_verifier.md \
  --json-out results/rule_based_ambiguity_verifier.json \
  --units-out results/rule_based_ambiguity_verifier_units.jsonl
```

Current result:

- on the `152` coded mirror-failure rows, symbolic ambiguity recall is `1.000`;
- attribute-under-specification recall is `1.000`;
- frame-sensitive recall is `1.000`.

## Cache-only interaction-memory rule audit

This audit derives a compact future speaker-rule list from the coded
mirror-failure files and checks whether cached repair selectors instantiate the
relevant cue on those same failure scenes. It makes no API calls and should be
read as replay-only support for the interaction-memory stretch idea, not as a
new prompted generation experiment.

```bash
conda run -n cross_play python scripts/analyze_interaction_memory_rules.py \
  --markdown-out docs/interaction_memory_rules.md \
  --json-out results/interaction_memory_rules.json
```

Current result:

- `152` coded failure rows collapse into two active rules:
  `disambiguate_shared_attributes` and `avoid_frame_sensitive_only`;
- cached population or consensus+info repairs satisfy the derived cue in
  `1.000` of the `76` unique failure scenes;
- mean repair success on those failure scenes is `0.991`.

## Cache-only qualitative failure examples

This report selects representative cached scenes where mirror-selected messages
fail at least one held-out listener and a population or consensus+info repair
succeeds. It makes no API calls.

```bash
conda run -n cross_play python scripts/make_qualitative_examples.py \
  --markdown-out docs/qualitative_failure_examples.md \
  --json-out results/qualitative_failure_examples.json
```

Current result:

- `docs/qualitative_failure_examples.md` contains four examples:
  perspective underspecification, a frame-sensitive relation,
  partial-observability visible-distractor ambiguity, and a no-coordinate
  consensus+info repair;
- the no-coordinate repair example improves from mirror `0.333` held-out
  success to consensus+info `1.000`.

## Reviewer checklist

This generated report materializes the original plan's Section 32
pre-submission checklist against the current artifacts. It makes no API calls.

```bash
conda run -n cross_play python scripts/make_reviewer_checklist.py \
  --markdown-out docs/reviewer_checklist.md \
  --json-out results/reviewer_checklist.json
```

Expected output:

- `docs/reviewer_checklist.md`;
- `results/reviewer_checklist.json`;
- all 19 core-validity, results, and paper checklist items pass.

## Plan coverage audit

This generated report maps the original workshop plan to the current artifacts.
It makes no API calls and separates completed core paper scope from partial or
open stretch work.

```bash
conda run -n cross_play python scripts/audit_plan_coverage.py \
  --markdown-out docs/plan_coverage_audit.md \
  --json-out results/plan_coverage_audit.json
```

Expected output:

- `docs/plan_coverage_audit.md`;
- `results/plan_coverage_audit.json`;
- core scope has `17` covered, `2` partial, and `0` open items;
- stretch scope has `3` covered, `2` partial, and `0` open items.

## Protocol appendix

This exports the exact paper-facing task protocol, prompts, listener styles,
training-listener settings, and observed result/candidate schemas.

```bash
conda run -n cross_play python scripts/export_protocol_appendix.py \
  --out docs/protocol_and_prompts.md
```

Expected output:

- `docs/protocol_and_prompts.md`.

## Artifact guide

This writes a reviewer-facing map from paper claims to source scene files,
cached result files, tables, and verification outputs. It does not make API
calls.

```bash
conda run -n cross_play python scripts/make_artifact_guide.py \
  --out docs/artifact_guide.md
```

Expected output:

- `docs/artifact_guide.md`.

## Benchmark integrity audit

This checks the paper-facing scene, result, candidate, audit, and cache
artifacts for object-ID leakage in generated messages, valid listener choices,
consistent success flags, balanced scene coverage across methods, speaker cache
paths, and exact response model versions.

```bash
conda run -n cross_play python scripts/audit_benchmark_integrity.py \
  --markdown-out results/benchmark_integrity_audit.md \
  --json-out results/benchmark_integrity_audit.json
```

Expected output:

- all checks pass in `results/benchmark_integrity_audit.md`.

## Claim verification

This recomputes the paper-facing numeric and text claims from the checked-in
records and tables.

```bash
conda run -n cross_play python scripts/verify_paper_claims.py \
  --markdown-out results/paper_claims_verification.md \
  --json-out results/paper_claims_verification.json
```

Expected output:

- all checks pass in `results/paper_claims_verification.md`.

## Paper build

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Expected output:

- `paper/main.pdf`, currently 8 pages.

## COLM submission build

The repository also keeps a generated COLM submission target. It preserves
`paper/main.tex` as the editable source while applying the COLM style file,
submission bibliography style, line numbers, and non-`H` float placement needed
by the venue template.

```bash
conda run -n cross_play python scripts/export_colm_submission.py \
  --source paper/main.tex \
  --out paper/colm2026_submission.tex

cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error colm2026_submission.tex
```

Expected output:

- `paper/colm2026_submission.pdf`, currently 8 pages.

## Submission readiness audit

This checks the compiled paper, required support artifacts, claim and integrity
verifiers, section structure, page count, limitation language, and final-template
status.

```bash
conda run -n cross_play python scripts/audit_submission_readiness.py \
  --markdown-out results/submission_readiness_audit.md \
  --json-out results/submission_readiness_audit.json
```

Expected output:

- no failing checks in `results/submission_readiness_audit.md`;
- no open actions.

## Current limitations to address before submission

- The strongest result is hybrid selection, not full LLM weight training or RL.
- Held-out listeners are API LLMs, not human participants.
- Alternate-model mirror failure categories are rubric-coded; broader human
  validation remains future work.
- The COLM target is generated from the editable generic draft; inspect the
  generated PDF before uploading.
