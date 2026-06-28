# PRAG-CrossPlay Artifact Guide

This guide maps the paper's main claims to the concrete files that support them.
It is generated from the current JSON/JSONL artifacts and is intended as a reviewer-facing entry point.

## Core Files

| Role | Path |
|---|---|
| Editable paper | `paper/main.tex` |
| Compiled paper | `paper/main.pdf` |
| COLM submission source | `paper/colm2026_submission.tex` |
| COLM submission PDF | `paper/colm2026_submission.pdf` |
| Protocol and prompts | `docs/protocol_and_prompts.md` |
| API token accounting | `docs/api_token_accounting.md` |
| Cross-model held-out listener audit | `docs/cross_model_listener_audit.md` |
| 600-scene local sanity check | `docs/local_benchmark600_check.md` |
| Local stronger-plan K=8 diagnostic | `docs/local_stronger_plan_k8.md` |
| Local stronger-plan scene file | `data/local_stronger_plan1200_scenes.jsonl` |
| API listener leave-one-out report | `docs/api_listener_leave_one_out.md` |
| Selection regret audit | `docs/selection_regret_audit.md` |
| Candidate pool robustness audit | `docs/candidate_pool_audit.md` |
| Candidate budget audit | `docs/candidate_budget_audit.md` |
| Candidate role selection audit | `docs/candidate_role_selection_audit.md` |
| Random candidate baseline | `docs/random_candidate_baseline.md` |
| Message length audit | `docs/message_length_audit.md` |
| Listener disagreement audit | `docs/listener_disagreement_audit.md` |
| Listener confidence audit | `docs/listener_confidence_audit.md` |
| Failure taxonomy audit | `docs/failure_taxonomy_audit.md` |
| Interaction memory rules | `docs/interaction_memory_rules.md` |
| Qualitative failure examples | `docs/qualitative_failure_examples.md` |
| Reviewer checklist | `docs/reviewer_checklist.md` |
| Plan coverage audit | `docs/plan_coverage_audit.md` |
| Partial-observability failure audit | `docs/partial_observability_api50_check.md` |
| Claim verifier | `scripts/verify_paper_claims.py` |
| Integrity audit | `scripts/audit_benchmark_integrity.py` |
| Readiness audit | `scripts/audit_submission_readiness.py` |
| API token accounting script | `scripts/analyze_api_token_accounting.py` |
| Cross-model listener audit script | `scripts/analyze_cross_model_listener_audit.py` |
| Local benchmark analysis script | `scripts/analyze_local_benchmark.py` |
| Local stronger-plan diagnostic script | `scripts/analyze_local_stronger_plan.py` |
| API listener leave-one-out script | `scripts/analyze_api_listener_leave_one_out.py` |
| Selection regret script | `scripts/analyze_selection_regret.py` |
| Candidate pool audit script | `scripts/analyze_candidate_pool.py` |
| Candidate budget audit script | `scripts/analyze_candidate_budget.py` |
| Candidate role selection script | `scripts/analyze_candidate_role_selection.py` |
| Random candidate baseline script | `scripts/analyze_random_candidate_baseline.py` |
| Message length audit script | `scripts/analyze_message_length_audit.py` |
| Listener disagreement audit script | `scripts/analyze_listener_disagreement.py` |
| Listener confidence audit script | `scripts/analyze_listener_confidence_audit.py` |
| Failure taxonomy script | `scripts/analyze_failure_taxonomy.py` |
| Interaction memory rule script | `scripts/analyze_interaction_memory_rules.py` |
| Qualitative examples script | `scripts/make_qualitative_examples.py` |
| Reviewer checklist script | `scripts/make_reviewer_checklist.py` |
| Plan coverage audit script | `scripts/audit_plan_coverage.py` |
| Reproduction commands | `REPRODUCE.md` |

## Dataset Cards

| Dataset | Source | Scenes | Scenario counts | Hidden private landmarks |
|---|---|---:|---|---:|
| local_benchmark600 | `data/local_benchmark600_scenes.jsonl` | 600 | distractor_contrast:150, perspective_shift:150, relational_reference:150, unique_attribute:150 | 0 |
| mixed_50 | `data/dev_scenes.jsonl` | 50 | distractor_contrast:15, perspective_shift:10, relational_reference:15, unique_attribute:10 | 0 |
| perspective_stress_50 | `data/perspective_stress50_scenes.jsonl` | 50 | perspective_shift:50 | 0 |
| partial_observability_api50 | `data/partial_observability_local50_scenes.jsonl` | 50 | partial_observability:50 | 50 |

## Result Artifact Groups

| Group | Scene file | Scenes | Record rows | Candidate rows | Audit rows | Speaker cache paths |
|---|---|---:|---:|---:|---:|---:|
| local_benchmark600 | `data/local_benchmark600_scenes.jsonl` | 600 | 10800 | 0 | 0 | 0 |
| mixed_50 | `data/dev_scenes.jsonl` | 50 | 2550 | 50 | 50 | 50 |
| perspective_stress_50 | `data/perspective_stress50_scenes.jsonl` | 50 | 4800 | 50 | 150 | 50 |
| partial_observability_api50 | `data/partial_observability_local50_scenes.jsonl` | 50 | 4050 | 50 | 150 | 50 |

## Cached Response Models

Cache files: 4982.

| Requested model | Response model | Cached responses |
|---|---|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 976 |

## API Token Accounting

This cache-only budget audit summarizes stored Responses API usage metadata. It reports tokens, not dollar cost, because billing depends on account-specific and date-specific pricing.

| Cache files | Readable | Missing usage | Input tokens | Output tokens | Total tokens | Source |
|---:|---:|---:|---:|---:|---:|---|
| 4982 | 4982 | 0 | 1287186 | 122906 | 1410092 | `results/api_token_accounting.json` |

| Requested model | Response model | Responses | Input tokens | Output tokens | Total tokens |
|---|---|---:|---:|---:|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 | 301032 | 31225 | 332257 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 | 751850 | 68860 | 820710 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 976 | 234304 | 22821 | 257125 |

## Headline Full-Candidate Results

| Run | Mirror cross | Mirror same | Gap | Population cross | Oracle | Pop-minus-mirror 95% CI | Source |
|---|---:|---:|---:|---:|---:|---|---|
| mixed_50 | 0.907 | 1.000 | 0.093 | 1.000 | 1.000 | 0.093 [0.027, 0.173] | `results/hybrid_api_pilot50_allcand_summary.json` |
| perspective_stress_50 | 0.813 | 1.000 | 0.187 | 1.000 | 1.000 | 0.187 [0.100, 0.287] | `results/perspective_stress50_hybrid_summary.json` |
| perspective_stress_50_alt_model | 0.713 | 1.000 | 0.287 | 1.000 | 1.000 | 0.287 [0.193, 0.380] | `results/perspective_stress50_gpt41nano_summary.json` |
| partial_observability_api50 | 0.667 | 1.000 | 0.333 | 1.000 | 1.000 | 0.333 [0.240, 0.427] | `results/partial_observability_api50_summary.json` |

## Cross-Model Held-Out Listener Audit

Population-play is 1.000 in all cross-model rows, while mirror self-play drops under every held-out listener family and remains weak under GPT-5.5.

| Setting | Held-out listener | Direct | Mirror | Population | Oracle | Pop-minus-mirror 95% CI | Source |
|---|---|---:|---:|---:|---:|---|---|
| Perspective stress | gpt-5.4-nano | 0.713 | 0.813 | 1.000 | 1.000 | 0.187 [0.100, 0.287] | `results/perspective_stress50_hybrid_summary.json` |
| Perspective stress | gpt-4.1-nano | 0.553 | 0.713 | 1.000 | 1.000 | 0.287 [0.193, 0.380] | `results/perspective_stress50_gpt41nano_summary.json` |
| Perspective stress | gpt-5.5 | 0.793 | 0.673 | 1.000 | 1.000 | 0.327 [0.233, 0.420] | `results/gpt55_perspective_selected_summary.json` |
| Partial observability | gpt-5.4-nano | 0.740 | 0.667 | 1.000 | 1.000 | 0.333 [0.240, 0.427] | `results/partial_observability_api50_summary.json` |
| Partial observability | gpt-4.1-nano | 0.700 | 0.660 | 1.000 | 1.000 | 0.340 [0.247, 0.433] | `results/gpt41_partial_observability_selected_summary.json` |
| Partial observability | gpt-5.5 | 0.740 | 0.653 | 1.000 | 1.000 | 0.347 [0.253, 0.440] | `results/gpt55_partial_observability_selected_summary.json` |

GPT-5.5 rows reuse cached speaker candidates and evaluate selected messages only; because population-play reaches 1.000, the same candidate pool's oracle ceiling is also 1.000.

## No-Coordinate Ablations

| Run | Mirror | Population | Consensus+info | Oracle | Consensus-minus-mirror 95% CI | Source |
|---|---:|---:|---:|---:|---|---|
| mixed_50_no_coord | 0.787 | 0.773 | 0.920 | 0.960 | 0.133 [0.033, 0.233] | `results/hybrid_api_pilot50_no_coord_summary.json` |
| perspective_stress_50_no_coord | 0.580 | 0.420 | 0.760 | 0.793 | 0.180 [0.100, 0.267] | `results/perspective_stress50_gpt41nano_no_coord_summary.json` |
| partial_observability_api50_no_coord | 0.607 | 0.727 | 0.987 | 1.000 | - | `results/partial_observability_api50_no_coord_summary.json` |

## Local Benchmark-Scale Sanity Check

This no-API check validates the released generator and local evaluation pipeline at the 600-scene scale specified by the original workshop plan. It is artifact support, not one of the paper-facing API listener results.

| Scenes | Scenario counts | Mirror cross | Mirror same | Gap | Population | Template | Oracle | Perspective mirror | Source |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 600 | distractor_contrast:150, perspective_shift:150, relational_reference:150, unique_attribute:150 | 0.631 | 1.000 | 0.369 | 1.000 | 1.000 | 1.000 | 0.158 | `results/local_benchmark600_check.json` |

## Local Stronger-Plan K=8 Diagnostic

This no-API diagnostic exercises the stronger-plan 1,000 initial-family plus 200 partial-observability scale. It is artifact support, not a paper-facing API listener result.
No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8.
No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8.
At K=8 without exact coordinates, consensus+info reaches 0.992 on the initial 1,000 scenes and 0.997 on partial-observability scenes.

| Scope | Filter | K | Scenes | Candidates/scene | Robust-scene rate | Oracle | Source |
|---|---|---:|---:|---:|---:|---:|---|
| initial_1000 | no_exact_coordinates | 4 | 1000 | 2.750 | 0.736 | 0.870 | `results/local_stronger_plan_k8.json` |
| initial_1000 | no_exact_coordinates | 8 | 1000 | 6.750 | 0.989 | 0.995 | `results/local_stronger_plan_k8.json` |
| partial_200 | no_exact_coordinates | 4 | 200 | 3.000 | 0.000 | 0.495 | `results/local_stronger_plan_k8.json` |
| partial_200 | no_exact_coordinates | 8 | 200 | 7.000 | 0.995 | 0.997 | `results/local_stronger_plan_k8.json` |
| combined_1200 | no_exact_coordinates | 4 | 1200 | 2.792 | 0.613 | 0.808 | `results/local_stronger_plan_k8.json` |
| combined_1200 | no_exact_coordinates | 8 | 1200 | 6.792 | 0.990 | 0.995 | `results/local_stronger_plan_k8.json` |

| Scope | Filter | K | Method | Success | Exact-coordinate selection | Source |
|---|---|---:|---|---:|---:|---|
| initial_1000 | no_exact_coordinates | 8 | population | 0.981 | 0.000 | `results/local_stronger_plan_k8.json` |
| initial_1000 | no_exact_coordinates | 8 | consensus+info | 0.992 | 0.000 | `results/local_stronger_plan_k8.json` |
| initial_1000 | no_exact_coordinates | 8 | oracle | 0.995 | 0.000 | `results/local_stronger_plan_k8.json` |
| partial_200 | no_exact_coordinates | 8 | population | 0.997 | 0.000 | `results/local_stronger_plan_k8.json` |
| partial_200 | no_exact_coordinates | 8 | consensus+info | 0.997 | 0.000 | `results/local_stronger_plan_k8.json` |
| partial_200 | no_exact_coordinates | 8 | oracle | 0.997 | 0.000 | `results/local_stronger_plan_k8.json` |
| combined_1200 | full | 8 | population | 1.000 | 0.162 | `results/local_stronger_plan_k8.json` |
| combined_1200 | no_exact_coordinates | 8 | population | 0.984 | 0.000 | `results/local_stronger_plan_k8.json` |
| combined_1200 | no_exact_coordinates | 8 | consensus+info | 0.993 | 0.000 | `results/local_stronger_plan_k8.json` |
| combined_1200 | no_exact_coordinates | 8 | oracle | 0.995 | 0.000 | `results/local_stronger_plan_k8.json` |

## API Listener Leave-One-Out Mechanism Check

This cache-only post-hoc check selects candidates with one or two API listener prompt variants and evaluates on the held-out prompt.

| Run | API mirror | API population | Oracle | Population-minus-mirror 95% CI | Source |
|---|---:|---:|---:|---|---|
| mixed_50 | 0.953 | 0.973 | 1.000 | 0.020 [0.007, 0.037] | `results/api_listener_leave_one_out.json` |
| perspective_gpt54 | 0.907 | 0.933 | 1.000 | 0.027 [0.010, 0.047] | `results/api_listener_leave_one_out.json` |
| perspective_gpt41 | 0.847 | 0.940 | 1.000 | 0.093 [0.063, 0.123] | `results/api_listener_leave_one_out.json` |
| partial_observability | 0.767 | 0.940 | 1.000 | 0.173 [0.133, 0.213] | `results/api_listener_leave_one_out.json` |

## Selection Regret Audit

Regret is oracle candidate success minus selected-message success, averaged by scene.

| Run | Method | Success | Oracle | Regret | 95% CI | Source |
|---|---|---:|---:|---:|---|---|
| mixed_50_full | mirror | 0.907 | 1.000 | 0.093 | [0.027, 0.173] | `results/selection_regret_audit.json` |
| mixed_50_full | population | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | `results/selection_regret_audit.json` |
| perspective_gpt54_full | mirror | 0.813 | 1.000 | 0.187 | [0.100, 0.287] | `results/selection_regret_audit.json` |
| perspective_gpt54_full | population | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | `results/selection_regret_audit.json` |
| perspective_gpt41_full | mirror | 0.713 | 1.000 | 0.287 | [0.193, 0.380] | `results/selection_regret_audit.json` |
| perspective_gpt41_full | population | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | `results/selection_regret_audit.json` |
| partial_observability_full | mirror | 0.667 | 1.000 | 0.333 | [0.240, 0.427] | `results/selection_regret_audit.json` |
| partial_observability_full | population | 1.000 | 1.000 | 0.000 | [0.000, 0.000] | `results/selection_regret_audit.json` |
| mixed_50_no_coord | mirror | 0.787 | 0.960 | 0.173 | [0.080, 0.273] | `results/selection_regret_audit.json` |
| mixed_50_no_coord | population | 0.773 | 0.960 | 0.187 | [0.093, 0.293] | `results/selection_regret_audit.json` |
| mixed_50_no_coord | consensus+info | 0.920 | 0.960 | 0.040 | [0.000, 0.093] | `results/selection_regret_audit.json` |
| perspective_gpt41_no_coord | mirror | 0.580 | 0.793 | 0.213 | [0.133, 0.293] | `results/selection_regret_audit.json` |
| perspective_gpt41_no_coord | population | 0.420 | 0.793 | 0.373 | [0.267, 0.480] | `results/selection_regret_audit.json` |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 0.793 | 0.033 | [0.007, 0.073] | `results/selection_regret_audit.json` |
| partial_observability_no_coord | mirror | 0.607 | 1.000 | 0.393 | [0.293, 0.487] | `results/selection_regret_audit.json` |
| partial_observability_no_coord | population | 0.727 | 1.000 | 0.273 | [0.180, 0.373] | `results/selection_regret_audit.json` |
| partial_observability_no_coord | consensus+info | 0.987 | 1.000 | 0.013 | [0.000, 0.040] | `results/selection_regret_audit.json` |

## Candidate Pool Robustness Audit

A robust candidate succeeds with every held-out API listener for that scene.

| Run | Filter | Scenes | Candidates/scene | Robust candidates/scene | Robust-scene rate | Oracle | Source |
|---|---|---:|---:|---:|---:|---:|---|
| mixed_50_full | full | 50 | 4.000 | 3.300 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| perspective_gpt54_full | full | 50 | 4.000 | 2.440 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| perspective_gpt41_full | full | 50 | 4.000 | 2.140 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| partial_observability_full | full | 50 | 4.000 | 2.580 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| mixed_50_no_coord | no_exact_coordinates | 50 | 3.000 | 2.300 | 0.920 | 0.960 | `results/candidate_pool_audit.json` |
| perspective_gpt41_no_coord | no_exact_coordinates | 50 | 3.000 | 1.140 | 0.660 | 0.793 | `results/candidate_pool_audit.json` |
| partial_observability_no_coord | no_exact_coordinates | 50 | 3.000 | 1.580 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |

| Run | Method | Selected success | Robust-selection rate | Oracle-match rate | Source |
|---|---|---:|---:|---:|---|
| mixed_50_full | mirror | 0.907 | 0.860 | 0.860 | `results/candidate_pool_audit.json` |
| mixed_50_full | population | 1.000 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| perspective_gpt54_full | mirror | 0.813 | 0.720 | 0.720 | `results/candidate_pool_audit.json` |
| perspective_gpt54_full | population | 1.000 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| perspective_gpt41_full | mirror | 0.713 | 0.560 | 0.560 | `results/candidate_pool_audit.json` |
| perspective_gpt41_full | population | 1.000 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| partial_observability_full | mirror | 0.667 | 0.500 | 0.500 | `results/candidate_pool_audit.json` |
| partial_observability_full | population | 1.000 | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| mixed_50_no_coord | mirror | 0.787 | 0.720 | 0.780 | `results/candidate_pool_audit.json` |
| mixed_50_no_coord | population | 0.773 | 0.740 | 0.760 | `results/candidate_pool_audit.json` |
| mixed_50_no_coord | consensus+info | 0.920 | 0.880 | 0.940 | `results/candidate_pool_audit.json` |
| perspective_gpt41_no_coord | mirror | 0.580 | 0.360 | 0.580 | `results/candidate_pool_audit.json` |
| perspective_gpt41_no_coord | population | 0.420 | 0.220 | 0.420 | `results/candidate_pool_audit.json` |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 0.620 | 0.920 | `results/candidate_pool_audit.json` |
| partial_observability_no_coord | mirror | 0.607 | 0.420 | 0.420 | `results/candidate_pool_audit.json` |
| partial_observability_no_coord | population | 0.727 | 0.600 | 0.600 | `results/candidate_pool_audit.json` |
| partial_observability_no_coord | consensus+info | 0.987 | 0.980 | 0.980 | `results/candidate_pool_audit.json` |

## Candidate Budget Audit

Oracle@K is the best held-out success among the first K generated candidates.

| Run | K | Oracle@K | Robust-scene rate | Source |
|---|---:|---:|---:|---|
| mixed_50_full | 1 | 0.840 | 0.780 | `results/candidate_budget_audit.json` |
| mixed_50_full | 2 | 0.853 | 0.800 | `results/candidate_budget_audit.json` |
| mixed_50_full | 3 | 0.960 | 0.920 | `results/candidate_budget_audit.json` |
| mixed_50_full | 4 | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| perspective_gpt54_full | 1 | 0.713 | 0.600 | `results/candidate_budget_audit.json` |
| perspective_gpt54_full | 2 | 0.787 | 0.680 | `results/candidate_budget_audit.json` |
| perspective_gpt54_full | 3 | 0.893 | 0.820 | `results/candidate_budget_audit.json` |
| perspective_gpt54_full | 4 | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| perspective_gpt41_full | 1 | 0.553 | 0.380 | `results/candidate_budget_audit.json` |
| perspective_gpt41_full | 2 | 0.620 | 0.400 | `results/candidate_budget_audit.json` |
| perspective_gpt41_full | 3 | 0.793 | 0.660 | `results/candidate_budget_audit.json` |
| perspective_gpt41_full | 4 | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| partial_observability_full | 1 | 0.740 | 0.620 | `results/candidate_budget_audit.json` |
| partial_observability_full | 2 | 0.747 | 0.620 | `results/candidate_budget_audit.json` |
| partial_observability_full | 3 | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| partial_observability_full | 4 | 1.000 | 1.000 | `results/candidate_budget_audit.json` |

## Candidate Role Selection Audit

This cache-only audit maps each selected message back to its original generated candidate slot.

| Run | Filter | Method | Scenes | Success | Natural first | Attribute short | Relational/spatial | Coordinate fallback | Unresolved | Source |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| mixed_50_full | full | mirror | 50 | 0.907 | 0.000 | 0.760 | 0.100 | 0.140 | 0 | `results/candidate_role_selection_audit.json` |
| mixed_50_full | full | population | 50 | 1.000 | 0.000 | 0.500 | 0.080 | 0.420 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt54_full | full | mirror | 50 | 0.813 | 0.020 | 0.480 | 0.160 | 0.340 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt54_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt41_full | full | mirror | 50 | 0.713 | 0.020 | 0.480 | 0.160 | 0.340 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt41_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0 | `results/candidate_role_selection_audit.json` |
| partial_observability_full | full | mirror | 50 | 0.667 | 0.020 | 0.500 | 0.000 | 0.480 | 0 | `results/candidate_role_selection_audit.json` |
| partial_observability_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0 | `results/candidate_role_selection_audit.json` |
| mixed_50_no_coord | no_exact_coordinates | mirror | 50 | 0.787 | 0.040 | 0.860 | 0.100 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| mixed_50_no_coord | no_exact_coordinates | population | 50 | 0.773 | 0.020 | 0.840 | 0.140 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| mixed_50_no_coord | no_exact_coordinates | consensus+info | 50 | 0.920 | 0.320 | 0.320 | 0.360 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt41_no_coord | no_exact_coordinates | mirror | 50 | 0.580 | 0.300 | 0.480 | 0.220 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt41_no_coord | no_exact_coordinates | population | 50 | 0.420 | 0.000 | 0.920 | 0.080 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| perspective_gpt41_no_coord | no_exact_coordinates | consensus+info | 50 | 0.760 | 0.420 | 0.000 | 0.580 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| partial_observability_no_coord | no_exact_coordinates | mirror | 50 | 0.607 | 0.380 | 0.580 | 0.040 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| partial_observability_no_coord | no_exact_coordinates | population | 50 | 0.727 | 0.500 | 0.400 | 0.100 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |
| partial_observability_no_coord | no_exact_coordinates | consensus+info | 50 | 0.987 | 0.540 | 0.000 | 0.460 | 0.000 | 0 | `results/candidate_role_selection_audit.json` |

Full-candidate population coordinate-fallback rates: mixed_50_full=0.420, perspective_gpt54_full=1.000, perspective_gpt41_full=1.000, partial_observability_full=1.000.
No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000.

## Random Candidate Baseline

The random selector is uniform over available generated candidates and is computed from cached held-out listener evaluations.

| Run | Filter | Candidates/scene | Random expected | Random robust-pick | Primary selector | Primary-minus-random 95% CI | Source |
|---|---|---:|---:|---:|---|---|---|
| mixed_50_full | full | 4.000 | 0.865 | 0.825 | population | 0.135 [0.078, 0.193] | `results/random_candidate_baseline.json` |
| perspective_gpt54_full | full | 4.000 | 0.715 | 0.610 | population | 0.285 [0.227, 0.345] | `results/random_candidate_baseline.json` |
| perspective_gpt41_full | full | 4.000 | 0.657 | 0.535 | population | 0.343 [0.282, 0.405] | `results/random_candidate_baseline.json` |
| partial_observability_full | full | 4.000 | 0.753 | 0.645 | population | 0.247 [0.217, 0.277] | `results/random_candidate_baseline.json` |
| mixed_50_no_coord | no_exact_coordinates | 3.000 | 0.820 | 0.767 | consensus+info | 0.100 [0.036, 0.167] | `results/random_candidate_baseline.json` |
| perspective_gpt41_no_coord | no_exact_coordinates | 3.000 | 0.542 | 0.380 | consensus+info | 0.218 [0.156, 0.280] | `results/random_candidate_baseline.json` |
| partial_observability_no_coord | no_exact_coordinates | 3.000 | 0.671 | 0.527 | consensus+info | 0.316 [0.271, 0.360] | `results/random_candidate_baseline.json` |

## Message Length Audit

This cache-only audit checks whether selector gains are explained by simply choosing longer messages.

| Run | Filter | Primary | Mirror tokens | Primary tokens | Token delta | Success delta | Direct tokens | Template tokens | Source |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| mixed_50_full | full | population | 5.560 | 6.820 | 1.260 | 0.093 | 9.260 | 10.000 | `results/message_length_audit.json` |
| perspective_gpt54_full | full | population | 7.400 | 10.220 | 2.820 | 0.187 | 11.700 | 10.000 | `results/message_length_audit.json` |
| perspective_gpt41_full | full | population | 7.400 | 10.220 | 2.820 | 0.287 | 11.700 | 10.000 | `results/message_length_audit.json` |
| partial_observability_full | full | population | 6.500 | 9.660 | 3.160 | 0.333 | 9.960 | 10.000 | `results/message_length_audit.json` |
| mixed_50_no_coord | no_exact_coordinates | consensus+info | 5.000 | 9.380 | 4.380 | 0.133 | 9.260 | - | `results/message_length_audit.json` |
| perspective_gpt41_no_coord | no_exact_coordinates | consensus+info | 8.280 | 12.540 | 4.260 | 0.180 | 11.700 | - | `results/message_length_audit.json` |
| partial_observability_no_coord | no_exact_coordinates | consensus+info | 7.560 | 12.760 | 5.200 | 0.380 | 9.960 | - | `results/message_length_audit.json` |

## Listener Disagreement Audit

A split outcome means the selected message succeeds for some held-out listeners but fails for others in the same scene.

| Run | Method | Success | Unanimous success | Split outcome | Unanimous failure | Choice disagreement | Source |
|---|---|---:|---:|---:|---:|---:|---|
| mixed_50_full | mirror | 0.907 | 0.860 | 0.080 | 0.060 | 0.080 | `results/listener_disagreement_audit.json` |
| mixed_50_full | population | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| perspective_gpt54_full | mirror | 0.813 | 0.720 | 0.180 | 0.100 | 0.180 | `results/listener_disagreement_audit.json` |
| perspective_gpt54_full | population | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| perspective_gpt41_full | mirror | 0.713 | 0.560 | 0.360 | 0.080 | 0.360 | `results/listener_disagreement_audit.json` |
| perspective_gpt41_full | population | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| partial_observability_full | mirror | 0.667 | 0.500 | 0.500 | 0.000 | 0.500 | `results/listener_disagreement_audit.json` |
| partial_observability_full | population | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| mixed_50_no_coord | mirror | 0.787 | 0.720 | 0.120 | 0.160 | 0.120 | `results/listener_disagreement_audit.json` |
| mixed_50_no_coord | population | 0.773 | 0.740 | 0.060 | 0.200 | 0.060 | `results/listener_disagreement_audit.json` |
| mixed_50_no_coord | consensus+info | 0.920 | 0.880 | 0.080 | 0.040 | 0.080 | `results/listener_disagreement_audit.json` |
| perspective_gpt41_no_coord | mirror | 0.580 | 0.360 | 0.460 | 0.180 | 0.460 | `results/listener_disagreement_audit.json` |
| perspective_gpt41_no_coord | population | 0.420 | 0.220 | 0.440 | 0.340 | 0.460 | `results/listener_disagreement_audit.json` |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 0.620 | 0.260 | 0.120 | 0.260 | `results/listener_disagreement_audit.json` |
| partial_observability_no_coord | mirror | 0.607 | 0.420 | 0.540 | 0.040 | 0.540 | `results/listener_disagreement_audit.json` |
| partial_observability_no_coord | population | 0.727 | 0.600 | 0.360 | 0.040 | 0.360 | `results/listener_disagreement_audit.json` |
| partial_observability_no_coord | consensus+info | 0.987 | 0.980 | 0.020 | 0.000 | 0.020 | `results/listener_disagreement_audit.json` |

## Listener Confidence Audit

This cache-only audit checks whether held-out listener confidence and ambiguity flags diagnose selected-message failures.

| Run | Method | Success | Mean confidence | Ambiguity | Failure confidence | High-conf failure rows | High-conf failure scenes | Source |
|---|---|---:|---:|---:|---:|---:|---:|---|
| mixed_50_full | mirror | 0.907 | 0.819 | 0.007 | 0.336 | 0.033 | 0.060 | `results/listener_confidence_audit.json` |
| mixed_50_full | population | 1.000 | 0.960 | 0.000 | - | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| perspective_gpt54_full | mirror | 0.813 | 0.776 | 0.000 | 0.386 | 0.073 | 0.200 | `results/listener_confidence_audit.json` |
| perspective_gpt54_full | population | 1.000 | 0.999 | 0.000 | - | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| perspective_gpt41_full | mirror | 0.713 | 0.877 | 0.000 | 0.677 | 0.147 | 0.280 | `results/listener_confidence_audit.json` |
| perspective_gpt41_full | population | 1.000 | 0.999 | 0.000 | - | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| partial_observability_full | mirror | 0.667 | 0.741 | 0.140 | 0.230 | 0.073 | 0.120 | `results/listener_confidence_audit.json` |
| partial_observability_full | population | 1.000 | 0.999 | 0.000 | - | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| mixed_50_no_coord | mirror | 0.787 | 0.761 | 0.007 | 0.528 | 0.120 | 0.200 | `results/listener_confidence_audit.json` |
| mixed_50_no_coord | population | 0.773 | 0.793 | 0.007 | 0.585 | 0.140 | 0.220 | `results/listener_confidence_audit.json` |
| mixed_50_no_coord | consensus+info | 0.920 | 0.782 | 0.000 | 0.233 | 0.020 | 0.020 | `results/listener_confidence_audit.json` |
| perspective_gpt41_no_coord | mirror | 0.580 | 0.835 | 0.000 | 0.771 | 0.280 | 0.480 | `results/listener_confidence_audit.json` |
| perspective_gpt41_no_coord | population | 0.420 | 0.883 | 0.000 | 0.836 | 0.440 | 0.640 | `results/listener_confidence_audit.json` |
| perspective_gpt41_no_coord | consensus+info | 0.760 | 0.869 | 0.000 | 0.878 | 0.200 | 0.360 | `results/listener_confidence_audit.json` |
| partial_observability_no_coord | mirror | 0.607 | 0.700 | 0.147 | 0.339 | 0.133 | 0.200 | `results/listener_confidence_audit.json` |
| partial_observability_no_coord | population | 0.727 | 0.776 | 0.087 | 0.368 | 0.100 | 0.140 | `results/listener_confidence_audit.json` |
| partial_observability_no_coord | consensus+info | 0.987 | 0.889 | 0.000 | 0.000 | 0.000 | 0.000 | `results/listener_confidence_audit.json` |

## Failure Taxonomy Audit

This cache-only audit combines the rubric-coded listener-level mirror failures used in the paper.

| Failure set | Rows | Underspecified distractor | Perspective-frame error | Other coded categories | Source |
|---|---:|---:|---:|---:|---|
| Perspective alt-model mirror | 43 | 38 | 5 | 0 | `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv` |
| Partial-observability mirror | 50 | 50 | 0 | 0 | `results/partial_observability_api50_mirror_failures_coded.csv` |
| Partial no-coordinate mirror | 59 | 59 | 0 | 0 | `results/partial_observability_api50_no_coord_mirror_failures_coded.csv` |

| Combined rows | Rows | Underspecified distractor | Perspective-frame error | Other coded categories | Source |
|---|---:|---:|---:|---:|---|
| combined | 152 | 147 | 5 | 0 | `results/failure_taxonomy_audit.json` |

## Interaction Memory Rule Audit

This replay-only audit derives future speaker-prompt rules from the coded mirror failures and checks whether cached repairs instantiate the relevant cue.

| Failure set | Repair selector | Category | Failure rows | Failure scenes | Repair success | Repair all-success scenes | Repair cue satisfies rule | Source |
|---|---|---|---:|---:|---:|---:|---:|---|
| perspective_full_mirror | population | perspective_frame_error | 5 | 3 | 1.000 | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| perspective_full_mirror | population | underspecified_distractor | 38 | 19 | 1.000 | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| partial_observability_full_mirror | population | underspecified_distractor | 50 | 25 | 1.000 | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| partial_observability_no_coord_mirror | consensus+info | underspecified_distractor | 59 | 29 | 0.977 | 0.966 | 1.000 | `results/interaction_memory_rules.json` |

Coded failure rows: 152; unique failure scenes: 76; rule counts: avoid_frame_sensitive_only:5, disambiguate_shared_attributes:147; mean repair success on failure scenes: 0.991; repair cue satisfies derived rule in 1.000 of failure scenes.

## Qualitative Failure Examples

Representative cache-only examples link selected messages to held-out listener choices and scene context.
These four cache-only examples show mirror-selected messages failing held-out listeners while population or consensus+info repairs succeed.

| Example | Scene | Category | Mirror success | Repair | Repair success | Source |
|---|---|---|---:|---|---:|---|
| Perspective scene with attribute underspecification | `ps_000005` | underspecified_distractor | 0.333 | population | 1.000 | `results/qualitative_failure_examples.json` |
| Perspective scene with frame-sensitive relation | `ps_000011` | perspective_frame_error | 0.667 | population | 1.000 | `results/qualitative_failure_examples.json` |
| Partial-observability scene with visible distractor ambiguity | `po_000005` | underspecified_distractor | 0.333 | population | 1.000 | `results/qualitative_failure_examples.json` |
| No-coordinate repair using consensus+info | `po_000000` | underspecified_distractor | 0.333 | consensus+info | 1.000 | `results/qualitative_failure_examples.json` |

## Reviewer Checklist

This materializes Section 32 of the original workshop plan as a generated checklist tied to current artifacts.
Items passed: 19/19.

| Section | Passed | Failed | Source |
|---|---:|---:|---|
| Core validity | 8 | 0 | `docs/reviewer_checklist.md` |
| Results | 5 | 0 | `docs/reviewer_checklist.md` |
| Paper | 6 | 0 | `docs/reviewer_checklist.md` |

## Plan Coverage Audit

This generated audit maps the original workshop plan to the current artifacts and separates claimed core coverage from partial or open stretch items.
Overall: 17 covered, 6 partial, 1 open across 24 plan items.
Core scope: 17 covered, 2 partial, 0 open.
Stretch scope: 0 covered, 4 partial, 1 open.

| Status | Scope | Plan item | Detail | Source |
|---|---|---|---|---|
| partial | core | Use development episodes for debugging prompts and tuning the generator. | The project uses a 50-scene dev/API pilot, not the 200 development episodes suggested by the stronger plan. | `docs/plan_coverage_audit.md` |
| partial | core | Hand-label roughly 100 failures into interpretable categories. | There are 152 author-coded listener-level mirror failures across paper-facing hard cases, but not a balanced 100-failure sample across all major methods. | `docs/plan_coverage_audit.md` |
| partial | stretch | Run a 1,000-scene benchmark and 200 partial-observability stress episodes. | A no-API local diagnostic now runs the stronger 1,000 initial-family plus 200 partial-observability scale, but the paper-facing API listener runs remain bounded 50-scene diagnostics. | `docs/plan_coverage_audit.md` |
| partial | stretch | Evaluate K=8 candidate generation in addition to K=4. | The local stronger-plan diagnostic evaluates K=8 candidate slots and shows added non-coordinate diversity; cached API speaker artifacts remain K=4. | `docs/plan_coverage_audit.md` |
| partial | stretch | Run an actual interaction-memory prompt rerun after distilling rules from failures. | A replay-only interaction-memory rule audit is present, but no new memory-prompt generation/evaluation run is claimed. | `docs/plan_coverage_audit.md` |
| open | stretch | Validate failures with human or independent non-LLM judgments. | The paper explicitly notes that held-out listeners are API LLMs and broader human validation remains future work. | `docs/plan_coverage_audit.md` |
| partial | stretch | Publish the artifact as a public repository or submission bundle. | The local artifact package is complete and reproducible, but this workspace is not currently a git repository, so public publishing is separate work. | `docs/plan_coverage_audit.md` |

## Claim-To-Evidence Map

| Claim | Evidence files | Anchor |
|---|---|---|
| Same-play can overstate held-out communicative success. | `results/paper_claims_verification.md; results/*_population_vs_mirror_paired.md` | mirror same-play is 1.000 while cross-play is lower in mixed, perspective, alternate-model, and partial-observability runs |
| The mirror self-play gap persists under GPT-5.5 and across held-out listener families. | `docs/cross_model_listener_audit.md; results/cross_model_listener_audit.json; paper/tables/cross_model_listener_audit.tex` | population-minus-mirror gaps are 0.187, 0.287, and 0.327 on perspective stress and 0.333, 0.340, and 0.347 on partial observability |
| Population-play closes the observed full-candidate cross-play gaps. | `paper/tables/mixed50.tex; paper/tables/perspective_stress50.tex; paper/tables/perspective_altmodel50.tex; results/partial_observability_api50_summary.json` | population cross-play is 1.000 in all full-candidate paper-facing runs |
| The strongest full-candidate result depends on explicit listener-invariant fallbacks. | `paper/tables/perspective_stress50_gpt41nano_no_coord.tex; paper/tables/selection_mechanisms_stress_no_coord.tex` | no-coordinate stress population drops to 0.420 while consensus+info reaches 0.760 |
| Partial-observability failures are under-informativeness failures, not private-landmark leakage. | `docs/partial_observability_api50_check.md; results/partial_observability_api50_check.json; results/partial_observability_api50_mirror_failures_coded.csv` | 0 candidate messages reference private landmarks; all 50 full-run mirror failures are underspecified-distractor choices |
| The population-selection effect is not only a deterministic-local-listener artifact. | `docs/api_listener_leave_one_out.md; results/api_listener_leave_one_out.json` | cache-only API listener leave-one-out improves population over mirror in all four cached runs |
| Most full-candidate failures are selector regret rather than missing candidates. | `docs/selection_regret_audit.md; results/selection_regret_audit.json` | full-candidate population-play has zero regret; mirror regret is 0.093, 0.187, 0.287, and 0.333 across the API runs |
| Full-candidate population-play succeeds by selecting available all-listener-robust candidates. | `docs/candidate_pool_audit.md; results/candidate_pool_audit.json` | every full-candidate run has a robust candidate in every scene; population-play selects a robust candidate in 1.000 of scenes |
| The four-candidate protocol materially increases robust candidate availability in harder audits. | `docs/candidate_budget_audit.md; results/candidate_budget_audit.json` | alternate-model perspective robust-scene coverage rises from 0.380 at K=1 to 1.000 at K=4 |
| Selector behavior corresponds to different generated candidate roles. | `docs/candidate_role_selection_audit.md; results/candidate_role_selection_audit.json` | full-candidate population uses coordinate fallbacks in 1.000 of perspective and partial-observability stress scenes, while no-coordinate consensus+info uses the short attribute slot in 0.000 of those harder scenes |
| Selector gains are not explained by uniformly choosing any generated candidate. | `docs/random_candidate_baseline.md; results/random_candidate_baseline.json` | population-play improves over random by 0.135, 0.285, 0.343, and 0.247 in the full-candidate runs; consensus+info improves over random by 0.100, 0.218, and 0.316 in no-coordinate runs |
| Selector gains are not solely a message-length artifact. | `docs/message_length_audit.md; results/message_length_audit.json` | full-candidate population selected messages average 6.82, 10.22, 10.22, and 9.66 tokens, while direct messages can be longer than mirror and still less successful |
| Population-play turns available robust candidates into unanimous held-out listener agreement. | `docs/listener_disagreement_audit.md; results/listener_disagreement_audit.json` | mirror split-outcome rates are 0.080, 0.180, 0.360, and 0.500 across full-candidate runs; population split-outcome rate is 0.000 |
| Listener self-reported confidence and ambiguity are not substitutes for cross-play. | `docs/listener_confidence_audit.md; results/listener_confidence_audit.json` | alternate-model perspective ambiguity flags are 0.000 while mirror high-confidence failure rates are 0.147 and 0.280 |
| Representative failures reflect real target-distractor ambiguity or frame sensitivity. | `docs/failure_taxonomy_audit.md; docs/qualitative_failure_examples.md; results/qualitative_failure_examples.json` | 147 of 152 coded listener-level mirror failures are underspecified-distractor cases and 5 are perspective-frame errors |
| The coded failures induce a small interaction-memory rule set. | `docs/interaction_memory_rules.md; results/interaction_memory_rules.json` | 152 coded failure rows collapse into disambiguate-shared-attributes and avoid-frame-sensitive-only rules; cached repairs satisfy the derived cue in 1.000 of failure scenes |
| The original pre-submission checklist is backed by concrete artifacts. | `docs/reviewer_checklist.md; results/reviewer_checklist.json` | Section 32 reviewer checklist passes all 19 core-validity, results, and paper items |
| The artifact package explicitly distinguishes completed core requirements from stretch gaps. | `docs/plan_coverage_audit.md; results/plan_coverage_audit.json` | core scope has 17 covered, 2 partial, 0 open items; stretch scope has 4 partial items and keeps human validation open |
| The released generator supports a benchmark-scale local sanity sweep. | `docs/local_benchmark600_check.md; results/local_benchmark600_check.json` | 600 local scenes balanced across four initial scenario families; mirror same-play is 1.000 but cross-play is 0.631 |
| The local artifact supports the stronger-plan 1,000+200 scale and K=8 diagnostic. | `docs/local_stronger_plan_k8.md; results/local_stronger_plan_k8.json` | no-coordinate oracle over 1,200 local scenes rises from 0.808 at K=4 to 0.995 at K=8 |
| The cached benchmark artifacts are internally consistent. | `results/benchmark_integrity_audit.md` | 194/194 integrity checks pass |
| API usage is bounded and cache-replayable. | `docs/api_token_accounting.md; results/api_token_accounting.json` | 4982 cached responses have complete usage metadata totaling 1410092 tokens |

## Quality Gates

| Gate | Checks | Failed | Warnings | Open actions | Source |
|---|---:|---:|---:|---:|---|
| benchmark integrity | 194 | 0 | 0 | 0 | `results/benchmark_integrity_audit.json` |
| paper claims | 828 | 0 | 0 | 0 | `results/paper_claims_verification.json` |
| reviewer checklist | 19 | 0 | 0 | 0 | `results/reviewer_checklist.json` |
| submission readiness | 161 | 0 | 2 | 0 | `results/submission_readiness_audit.json` |

## Refresh Commands

These commands do not require new API calls when the cached artifacts are present.

```bash
conda run -n cross_play python scripts/audit_benchmark_integrity.py \
  --markdown-out results/benchmark_integrity_audit.md \
  --json-out results/benchmark_integrity_audit.json

conda run -n cross_play python scripts/verify_paper_claims.py \
  --markdown-out results/paper_claims_verification.md \
  --json-out results/paper_claims_verification.json

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

conda run -n cross_play python scripts/analyze_local_stronger_plan.py \
  --scene-out data/local_stronger_plan1200_scenes.jsonl \
  --markdown-out docs/local_stronger_plan_k8.md \
  --json-out results/local_stronger_plan_k8.json

conda run -n cross_play python scripts/analyze_api_listener_leave_one_out.py \
  --records mixed_50=results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl \
  --records perspective_gpt54=results/perspective_stress50_hybrid_candidate_eval_records.jsonl \
  --records perspective_gpt41=results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl \
  --records partial_observability=results/partial_observability_api50_candidate_eval_records.jsonl \
  --markdown-out docs/api_listener_leave_one_out.md \
  --json-out results/api_listener_leave_one_out.json \
  --tex-out paper/tables/api_listener_leave_one_out.tex

conda run -n cross_play python scripts/analyze_selection_regret.py \
  --markdown-out docs/selection_regret_audit.md \
  --json-out results/selection_regret_audit.json

conda run -n cross_play python scripts/analyze_candidate_pool.py \
  --markdown-out docs/candidate_pool_audit.md \
  --json-out results/candidate_pool_audit.json

conda run -n cross_play python scripts/analyze_candidate_budget.py \
  --markdown-out docs/candidate_budget_audit.md \
  --json-out results/candidate_budget_audit.json

conda run -n cross_play python scripts/analyze_candidate_role_selection.py \
  --markdown-out docs/candidate_role_selection_audit.md \
  --json-out results/candidate_role_selection_audit.json

conda run -n cross_play python scripts/analyze_random_candidate_baseline.py \
  --markdown-out docs/random_candidate_baseline.md \
  --json-out results/random_candidate_baseline.json

conda run -n cross_play python scripts/analyze_message_length_audit.py \
  --markdown-out docs/message_length_audit.md \
  --json-out results/message_length_audit.json

conda run -n cross_play python scripts/analyze_listener_disagreement.py \
  --markdown-out docs/listener_disagreement_audit.md \
  --json-out results/listener_disagreement_audit.json

conda run -n cross_play python scripts/analyze_failure_taxonomy.py \
  --markdown-out docs/failure_taxonomy_audit.md \
  --json-out results/failure_taxonomy_audit.json \
  --tex-out paper/tables/failure_taxonomy_combined.tex

conda run -n cross_play python scripts/analyze_interaction_memory_rules.py \
  --markdown-out docs/interaction_memory_rules.md \
  --json-out results/interaction_memory_rules.json

conda run -n cross_play python scripts/make_qualitative_examples.py \
  --markdown-out docs/qualitative_failure_examples.md \
  --json-out results/qualitative_failure_examples.json

conda run -n cross_play python scripts/make_reviewer_checklist.py \
  --markdown-out docs/reviewer_checklist.md \
  --json-out results/reviewer_checklist.json

conda run -n cross_play python scripts/audit_plan_coverage.py \
  --markdown-out docs/plan_coverage_audit.md \
  --json-out results/plan_coverage_audit.json

conda run -n cross_play python scripts/audit_submission_readiness.py \
  --markdown-out results/submission_readiness_audit.md \
  --json-out results/submission_readiness_audit.json

conda run -n cross_play python scripts/make_artifact_guide.py \
  --out docs/artifact_guide.md
```
