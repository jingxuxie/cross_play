# Benchmark Integrity Audit

Checks passed: 290/290.

## Artifact Summary

| Group | Source scenes | Record rows | Candidate rows | Audit rows | Speaker cache paths |
|---|---:|---:|---:|---:|---:|
| local_benchmark600 | 600 | 10800 | 0 | 0 | 0 |
| mixed_50 | 50 | 2550 | 50 | 50 | 50 |
| perspective_stress_50 | 50 | 11100 | 170 | 250 | 170 |
| partial_observability_api50 | 50 | 4050 | 50 | 150 | 50 |

## Cached Model Versions

| Requested model | Response model | Cached responses |
|---|---|---:|
| `gpt-4.1-nano` | `gpt-4.1-nano-2025-04-14` | 1236 |
| `gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770 |
| `gpt-5.5` | `gpt-5.5-2026-04-23` | 3165 |

## Warnings

- Scene IDs overlap across source scene files; validation is scoped by scene file. Sample overlaps: ps_000040, ps_000041, ps_000042, ps_000043, ps_000044, ps_000045, ps_000046, ps_000047.

## Checks

| Status | Check | Detail |
|---|---|---|
| PASS | `data/local_benchmark600_scenes.jsonl.nonempty` | 600 scenes |
| PASS | `data/local_benchmark600_scenes.jsonl.unique_scene_ids_within_file` | no duplicates |
| PASS | `data/local_benchmark600_scenes.jsonl.target_id_in_scene` | all targets present |
| PASS | `data/local_benchmark600_scenes.jsonl.target_visible_to_listener` | all targets visible |
| PASS | `data/local_benchmark600_scenes.jsonl.unique_object_ids_per_scene` | all object IDs unique |
| PASS | `data/dev_scenes.jsonl.nonempty` | 50 scenes |
| PASS | `data/dev_scenes.jsonl.unique_scene_ids_within_file` | no duplicates |
| PASS | `data/dev_scenes.jsonl.target_id_in_scene` | all targets present |
| PASS | `data/dev_scenes.jsonl.target_visible_to_listener` | all targets visible |
| PASS | `data/dev_scenes.jsonl.unique_object_ids_per_scene` | all object IDs unique |
| PASS | `data/perspective_stress50_scenes.jsonl.nonempty` | 50 scenes |
| PASS | `data/perspective_stress50_scenes.jsonl.unique_scene_ids_within_file` | no duplicates |
| PASS | `data/perspective_stress50_scenes.jsonl.target_id_in_scene` | all targets present |
| PASS | `data/perspective_stress50_scenes.jsonl.target_visible_to_listener` | all targets visible |
| PASS | `data/perspective_stress50_scenes.jsonl.unique_object_ids_per_scene` | all object IDs unique |
| PASS | `data/partial_observability_local50_scenes.jsonl.nonempty` | 50 scenes |
| PASS | `data/partial_observability_local50_scenes.jsonl.unique_scene_ids_within_file` | no duplicates |
| PASS | `data/partial_observability_local50_scenes.jsonl.target_id_in_scene` | all targets present |
| PASS | `data/partial_observability_local50_scenes.jsonl.target_visible_to_listener` | all targets visible |
| PASS | `data/partial_observability_local50_scenes.jsonl.unique_object_ids_per_scene` | all object IDs unique |
| PASS | `results/local_benchmark600_records.jsonl.nonempty` | 10800 rows |
| PASS | `results/local_benchmark600_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/local_benchmark600_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/local_benchmark600_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/local_benchmark600_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/local_benchmark600_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/local_benchmark600_records.jsonl.same_scene_set_across_methods` | 600 scenes per method |
| PASS | `results/local_benchmark600_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.nonempty` | 900 rows |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/hybrid_api_pilot50_allcand_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.nonempty` | 1050 rows |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/hybrid_api_pilot50_no_coord_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.nonempty` | 600 rows |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/hybrid_api_pilot50_allcand_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 12 rows per scene-method |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.nonempty` | 50 rows |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.target_ids_match_source` | all targets match |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.candidate_lists_nonempty` | all rows have candidates |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.candidates_no_object_id_leakage` | no candidate contains obj_* IDs |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.selections_are_candidates` | mirror/population selections come from candidate lists |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/hybrid_api_pilot50_allcand_candidates.jsonl.speaker_cache_paths_exist` | 50 speaker cache paths exist |
| PASS | `results/hybrid_api_pilot50_no_coord_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/hybrid_api_pilot50_no_coord_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/hybrid_api_pilot50_no_coord_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/hybrid_api_pilot50_no_coord_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.nonempty` | 900 rows |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/perspective_stress50_hybrid_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.nonempty` | 900 rows |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/perspective_stress50_gpt41nano_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt55_perspective_selected_records.jsonl.nonempty` | 750 rows |
| PASS | `results/gpt55_perspective_selected_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_perspective_selected_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_perspective_selected_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_perspective_selected_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_perspective_selected_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_perspective_selected_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_perspective_selected_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.nonempty` | 1050 rows |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.nonempty` | 600 rows |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/perspective_stress50_hybrid_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 12 rows per scene-method |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.nonempty` | 600 rows |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/perspective_stress50_gpt41nano_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 12 rows per scene-method |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.nonempty` | 360 rows |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.same_scene_set_across_methods` | 20 scenes per method |
| PASS | `results/gpt55_speaker_perspective20_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.nonempty` | 240 rows |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.same_scene_set_across_methods` | 20 scenes per method |
| PASS | `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 12 rows per scene-method |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.nonempty` | 900 rows |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_speaker_perspective50_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.nonempty` | 600 rows |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 12 rows per scene-method |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.nonempty` | 1050 rows |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_speaker_perspective50_no_coord_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.nonempty` | 900 rows |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_no_coord_k8_perspective50_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.nonempty` | 1200 rows |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 24 rows per scene-method |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.nonempty` | 1050 rows |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.nonempty` | 50 rows |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.target_ids_match_source` | all targets match |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.candidate_lists_nonempty` | all rows have candidates |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.candidates_no_object_id_leakage` | no candidate contains obj_* IDs |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.selections_are_candidates` | mirror/population selections come from candidate lists |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/perspective_stress50_hybrid_candidates.jsonl.speaker_cache_paths_exist` | 50 speaker cache paths exist |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.nonempty` | 20 rows |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.target_ids_match_source` | all targets match |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.candidate_lists_nonempty` | all rows have candidates |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.candidates_no_object_id_leakage` | no candidate contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.selections_are_candidates` | mirror/population selections come from candidate lists |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_speaker_perspective20_candidates.jsonl.speaker_cache_paths_exist` | 20 speaker cache paths exist |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.target_ids_match_source` | all targets match |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.candidate_lists_nonempty` | all rows have candidates |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.candidates_no_object_id_leakage` | no candidate contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.selections_are_candidates` | mirror/population selections come from candidate lists |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_speaker_perspective50_candidates.jsonl.speaker_cache_paths_exist` | 50 speaker cache paths exist |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.target_ids_match_source` | all targets match |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.candidate_lists_nonempty` | all rows have candidates |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.candidates_no_object_id_leakage` | no candidate contains obj_* IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.selections_are_candidates` | mirror/population selections come from candidate lists |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_candidates.jsonl.speaker_cache_paths_exist` | 50 speaker cache paths exist |
| PASS | `results/perspective_stress50_gpt41nano_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/perspective_stress50_gpt41nano_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/perspective_stress50_gpt41nano_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/perspective_stress50_gpt41nano_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_perspective_selected_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt55_perspective_selected_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_perspective_selected_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/gpt55_perspective_selected_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_speaker_perspective50_no_coord_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt55_speaker_perspective50_no_coord_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_speaker_perspective50_no_coord_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/gpt55_speaker_perspective50_no_coord_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/gpt55_no_coord_k8_perspective50_no_coord_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/partial_observability_api50_records.jsonl.nonempty` | 900 rows |
| PASS | `results/partial_observability_api50_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/partial_observability_api50_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/partial_observability_api50_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/partial_observability_api50_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/partial_observability_api50_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/partial_observability_api50_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/partial_observability_api50_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.nonempty` | 750 rows |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt41_partial_observability_selected_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.nonempty` | 750 rows |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/gpt55_partial_observability_selected_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.nonempty` | 600 rows |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/partial_observability_api50_candidate_eval_records.jsonl.balanced_rows_per_scene_method` | 12 rows per scene-method |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.nonempty` | 1050 rows |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.scene_ids_known` | all rows mapped to source scene file |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.target_ids_match_source` | all row target IDs match source scenes |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.choice_ids_valid` | all listener choices are valid candidate object IDs |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.success_flags_consistent` | all success flags equal choice_id == target_id |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.messages_no_object_id_leakage` | no generated/evaluated message contains obj_* IDs |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.same_scene_set_across_methods` | 50 scenes per method |
| PASS | `results/partial_observability_api50_no_coord_records.jsonl.balanced_rows_per_scene_method` | 3 rows per scene-method |
| PASS | `results/partial_observability_api50_candidates.jsonl.nonempty` | 50 rows |
| PASS | `results/partial_observability_api50_candidates.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/partial_observability_api50_candidates.jsonl.target_ids_match_source` | all targets match |
| PASS | `results/partial_observability_api50_candidates.jsonl.candidate_lists_nonempty` | all rows have candidates |
| PASS | `results/partial_observability_api50_candidates.jsonl.candidates_no_object_id_leakage` | no candidate contains obj_* IDs |
| PASS | `results/partial_observability_api50_candidates.jsonl.selections_are_candidates` | mirror/population selections come from candidate lists |
| PASS | `results/partial_observability_api50_candidates.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/partial_observability_api50_candidates.jsonl.speaker_cache_paths_exist` | 50 speaker cache paths exist |
| PASS | `results/gpt41_partial_observability_selected_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt41_partial_observability_selected_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt41_partial_observability_selected_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/gpt41_partial_observability_selected_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/gpt55_partial_observability_selected_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/gpt55_partial_observability_selected_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/gpt55_partial_observability_selected_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/gpt55_partial_observability_selected_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `results/partial_observability_api50_no_coord_audit.jsonl.nonempty` | 50 rows |
| PASS | `results/partial_observability_api50_no_coord_audit.jsonl.scene_ids_known` | all rows mapped |
| PASS | `results/partial_observability_api50_no_coord_audit.jsonl.messages_no_object_id_leakage` | no audit candidate/selection contains obj_* IDs |
| PASS | `results/partial_observability_api50_no_coord_audit.jsonl.local_choice_ids_valid` | all local selector choices are valid object IDs |
| PASS | `data/cached_responses.cache_files_present` | 7171 cache files |
| PASS | `data/cached_responses.cache_files_readable` | all cache files parse as JSON |
