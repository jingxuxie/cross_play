# Paper Claims Verification

Checks passed: 1027/1027.

| Status | Check | Actual | Expected | Source |
|---|---|---:|---:|---|
| PASS | `mixed_full.api_direct_first.success` | 0.840 | 0.840 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.api_best_of_k_shortest.success` | 0.740 | 0.740 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.hybrid_local_mirror_api_eval.success` | 0.907 | 0.907 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.hybrid_local_mirror_api_eval.sameplay_success` | 1.000 | 1.000 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.hybrid_local_mirror_api_eval.crossplay_gap` | 0.093 | 0.093 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.hybrid_local_population_api_eval.success` | 1.000 | 1.000 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.hybrid_local_population_api_eval.sameplay_success` | 1.000 | 1.000 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.oracle_upper_bound.success` | 1.000 | 1.000 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `stress_gpt54.api_direct_first.success` | 0.713 | 0.713 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.api_best_of_k_shortest.success` | 0.420 | 0.420 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.hybrid_local_mirror_api_eval.success` | 0.813 | 0.813 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.hybrid_local_mirror_api_eval.sameplay_success` | 1.000 | 1.000 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.hybrid_local_mirror_api_eval.crossplay_gap` | 0.187 | 0.187 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.hybrid_local_population_api_eval.success` | 1.000 | 1.000 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.oracle_upper_bound.success` | 1.000 | 1.000 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt41.api_direct_first.success` | 0.553 | 0.553 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.api_best_of_k_shortest.success` | 0.367 | 0.367 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.hybrid_local_mirror_api_eval.success` | 0.713 | 0.713 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.hybrid_local_mirror_api_eval.sameplay_success` | 1.000 | 1.000 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.hybrid_local_mirror_api_eval.crossplay_gap` | 0.287 | 0.287 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.hybrid_local_population_api_eval.success` | 1.000 | 1.000 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.oracle_upper_bound.success` | 1.000 | 1.000 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_no_coord.no_coord_direct_first.success` | 0.553 | 0.553 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_best_of_k_shortest.success` | 0.367 | 0.367 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_mirror.success` | 0.580 | 0.580 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_mirror.sameplay_success` | 1.000 | 1.000 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_mirror.crossplay_gap` | 0.420 | 0.420 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_population.success` | 0.420 | 0.420 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_population.sameplay_success` | 0.520 | 0.520 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_consensus_info.success` | 0.760 | 0.760 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_informative.success` | 0.760 | 0.760 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.no_coord_oracle.success` | 0.793 | 0.793 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_direct_first.success` | 0.840 | 0.840 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_best_of_k_shortest.success` | 0.740 | 0.740 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_mirror.success` | 0.787 | 0.787 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_mirror.sameplay_success` | 0.880 | 0.880 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_mirror.crossplay_gap` | 0.093 | 0.093 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_population.success` | 0.773 | 0.773 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_population.sameplay_success` | 0.813 | 0.813 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_consensus_info.success` | 0.920 | 0.920 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_informative.success` | 0.900 | 0.900 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.no_coord_oracle.success` | 0.960 | 0.960 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_full.pop_minus_mirror.n_pairs` | 50 | 50 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.pop_minus_mirror.diff` | 0.093 | 0.093 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.pop_minus_mirror.ci_low` | 0.027 | 0.027 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.pop_minus_mirror.ci_high` | 0.173 | 0.173 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.pop_minus_mirror.p_boot` | 0.0024 | 0.0024 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.perspective_pop_minus_mirror.n_pairs` | 10 | 10 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.perspective_pop_minus_mirror.diff` | 0.367 | 0.367 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.perspective_pop_minus_mirror.ci_low` | 0.133 | 0.133 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.perspective_pop_minus_mirror.ci_high` | 0.600 | 0.600 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `mixed_full.perspective_pop_minus_mirror.p_boot` | 0.0004 | 0.0004 | `results/hybrid_api_pilot50_allcand_records.jsonl` |
| PASS | `stress_gpt54.pop_minus_mirror.n_pairs` | 50 | 50 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.pop_minus_mirror.diff` | 0.187 | 0.187 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.pop_minus_mirror.ci_low` | 0.100 | 0.100 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.pop_minus_mirror.ci_high` | 0.287 | 0.287 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt54.pop_minus_mirror.p_boot` | 0.0000 | 0.0000 | `results/perspective_stress50_hybrid_records.jsonl` |
| PASS | `stress_gpt41.pop_minus_mirror.n_pairs` | 50 | 50 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.pop_minus_mirror.diff` | 0.287 | 0.287 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.pop_minus_mirror.ci_low` | 0.193 | 0.193 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.pop_minus_mirror.ci_high` | 0.380 | 0.380 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_gpt41.pop_minus_mirror.p_boot` | 0.0000 | 0.0000 | `results/perspective_stress50_gpt41nano_records.jsonl` |
| PASS | `stress_no_coord.consensus_minus_mirror.n_pairs` | 50 | 50 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.consensus_minus_mirror.diff` | 0.180 | 0.180 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.consensus_minus_mirror.ci_low` | 0.100 | 0.100 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.consensus_minus_mirror.ci_high` | 0.267 | 0.267 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `stress_no_coord.consensus_minus_mirror.p_boot` | 0.0000 | 0.0000 | `results/perspective_stress50_gpt41nano_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.consensus_minus_mirror.n_pairs` | 50 | 50 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.consensus_minus_mirror.diff` | 0.133 | 0.133 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.consensus_minus_mirror.ci_low` | 0.033 | 0.033 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.consensus_minus_mirror.ci_high` | 0.233 | 0.233 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `mixed_no_coord.consensus_minus_mirror.p_boot` | 0.0040 | 0.0040 | `results/hybrid_api_pilot50_no_coord_records.jsonl` |
| PASS | `coded_failures.total` | 43 | 43 | `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv` |
| PASS | `coded_failures.underspecified_distractor` | 38 | 38 | `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv` |
| PASS | `coded_failures.perspective_frame_error` | 5 | 5 | `results/perspective_stress50_gpt41nano_mirror_failures_coded.csv` |
| PASS | `partial_coded_failures.total` | 50 | 50 | `results/partial_observability_api50_mirror_failures_coded.csv` |
| PASS | `partial_coded_failures.underspecified_distractor` | 50 | 50 | `results/partial_observability_api50_mirror_failures_coded.csv` |
| PASS | `partial_no_coord_coded_failures.total` | 59 | 59 | `results/partial_observability_api50_no_coord_mirror_failures_coded.csv` |
| PASS | `partial_no_coord_coded_failures.underspecified_distractor` | 59 | 59 | `results/partial_observability_api50_no_coord_mirror_failures_coded.csv` |
| PASS | `mechanism.stress_full.population_exact_coord` | 50 | 50 | `results/perspective_stress50_gpt41nano_audit.jsonl` |
| PASS | `mechanism.stress_full.mirror_exact_coord` | 17 | 17 | `results/perspective_stress50_gpt41nano_audit.jsonl` |
| PASS | `mechanism.stress_no_coord.population_spatial` | 4 | 4 | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl` |
| PASS | `mechanism.stress_no_coord.consensus_info_spatial` | 50 | 50 | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl` |
| PASS | `mechanism.stress_no_coord.consensus_info_fallback` | 50 | 50 | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl` |
| PASS | `mechanism.mixed_no_coord.consensus_source` | 32 | 32 | `results/hybrid_api_pilot50_no_coord_audit.jsonl` |
| PASS | `mechanism.mixed_no_coord.fallback_source` | 18 | 18 | `results/hybrid_api_pilot50_no_coord_audit.jsonl` |
| PASS | `partial_local.n_scenes` | 50 | 50 | `data/partial_observability_local50_scenes.jsonl` |
| PASS | `partial_local.hidden_private_landmarks` | 50 | 50 | `data/partial_observability_local50_scenes.jsonl` |
| PASS | `partial_local.direct.success` | 0.493 | 0.493 | `results/partial_observability_local50_summary.json` |
| PASS | `partial_local.mirror_selfplay.success` | 0.653 | 0.653 | `results/partial_observability_local50_summary.json` |
| PASS | `partial_local.mirror_selfplay.sameplay_success` | 1.000 | 1.000 | `results/partial_observability_local50_summary.json` |
| PASS | `partial_local.mirror_selfplay.crossplay_gap` | 0.347 | 0.347 | `results/partial_observability_local50_summary.json` |
| PASS | `partial_local.population_play.success` | 1.000 | 1.000 | `results/partial_observability_local50_summary.json` |
| PASS | `partial_local.population_play.sameplay_success` | 1.000 | 1.000 | `results/partial_observability_local50_summary.json` |
| PASS | `partial_local.oracle_upper_bound.success` | 1.000 | 1.000 | `results/partial_observability_local50_summary.json` |
| PASS | `local_benchmark600.n_scenes` | 600 | 600 | `data/local_benchmark600_scenes.jsonl` |
| PASS | `local_benchmark600.unique_attribute.n_scenes` | 150 | 150 | `data/local_benchmark600_scenes.jsonl` |
| PASS | `local_benchmark600.distractor_contrast.n_scenes` | 150 | 150 | `data/local_benchmark600_scenes.jsonl` |
| PASS | `local_benchmark600.relational_reference.n_scenes` | 150 | 150 | `data/local_benchmark600_scenes.jsonl` |
| PASS | `local_benchmark600.perspective_shift.n_scenes` | 150 | 150 | `data/local_benchmark600_scenes.jsonl` |
| PASS | `local_benchmark600.mirror_cross` | 0.631 | 0.631 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.mirror_same` | 1.000 | 1.000 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.mirror_gap` | 0.369 | 0.369 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.population_cross` | 1.000 | 1.000 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.template_cross` | 1.000 | 1.000 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.oracle_cross` | 1.000 | 1.000 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.perspective_mirror_cross` | 0.158 | 0.158 | `results/local_benchmark600_check.json` |
| PASS | `local_benchmark600.perspective_mirror_gap` | 0.842 | 0.842 | `results/local_benchmark600_check.json` |
| PASS | `local_stronger_plan.n_scenes` | 1200 | 1200 | `data/local_stronger_plan1200_scenes.jsonl` |
| PASS | `local_stronger_plan.unique_attribute.n_scenes` | 250 | 250 | `data/local_stronger_plan1200_scenes.jsonl` |
| PASS | `local_stronger_plan.distractor_contrast.n_scenes` | 250 | 250 | `data/local_stronger_plan1200_scenes.jsonl` |
| PASS | `local_stronger_plan.relational_reference.n_scenes` | 250 | 250 | `data/local_stronger_plan1200_scenes.jsonl` |
| PASS | `local_stronger_plan.perspective_shift.n_scenes` | 250 | 250 | `data/local_stronger_plan1200_scenes.jsonl` |
| PASS | `local_stronger_plan.partial_observability.n_scenes` | 200 | 200 | `data/local_stronger_plan1200_scenes.jsonl` |
| PASS | `local_stronger_plan.initial_no_coord_oracle_k4` | 0.870 | 0.870 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.initial_no_coord_oracle_k8` | 0.995 | 0.995 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.partial_no_coord_oracle_k4` | 0.495 | 0.495 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.partial_no_coord_oracle_k8` | 0.997 | 0.997 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.initial_no_coord_consensus_k8` | 0.992 | 0.992 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.partial_no_coord_consensus_k8` | 0.997 | 0.997 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.combined_full_population_k8` | 1.000 | 1.000 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.budget.combined_1200.no_exact_coordinates.4.oracle` | 0.808 | 0.808 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.budget.combined_1200.no_exact_coordinates.4.robust_scene_rate` | 0.613 | 0.613 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.budget.combined_1200.no_exact_coordinates.8.oracle` | 0.995 | 0.995 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.budget.combined_1200.no_exact_coordinates.8.robust_scene_rate` | 0.990 | 0.990 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.budget.partial_200.no_exact_coordinates.8.oracle` | 0.997 | 0.997 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.budget.partial_200.no_exact_coordinates.8.robust_scene_rate` | 0.995 | 0.995 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.selector.combined_1200.no_exact_coordinates.8.consensus+info.success` | 0.993 | 0.993 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.selector.combined_1200.no_exact_coordinates.8.population.success` | 0.984 | 0.984 | `results/local_stronger_plan_k8.json` |
| PASS | `local_stronger_plan.selector.combined_1200.full.8.population.success` | 1.000 | 1.000 | `results/local_stronger_plan_k8.json` |
| PASS | `partial_api.api_direct_first.success` | 0.740 | 0.740 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.api_best_of_k_shortest.success` | 0.313 | 0.313 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.hybrid_local_mirror_api_eval.success` | 0.667 | 0.667 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.hybrid_local_mirror_api_eval.sameplay_success` | 1.000 | 1.000 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.hybrid_local_mirror_api_eval.crossplay_gap` | 0.333 | 0.333 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.hybrid_local_population_api_eval.success` | 1.000 | 1.000 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.hybrid_local_population_api_eval.sameplay_success` | 1.000 | 1.000 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api.oracle_upper_bound.success` | 1.000 | 1.000 | `results/partial_observability_api50_summary.json` |
| PASS | `partial_api_no_coord.no_coord_direct_first.success` | 0.740 | 0.740 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_best_of_k_shortest.success` | 0.313 | 0.313 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_mirror.success` | 0.607 | 0.607 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_mirror.sameplay_success` | 0.920 | 0.920 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_mirror.crossplay_gap` | 0.313 | 0.313 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_population.success` | 0.727 | 0.727 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_consensus_info.success` | 0.987 | 0.987 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_informative.success` | 0.973 | 0.973 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api_no_coord.no_coord_oracle.success` | 1.000 | 1.000 | `results/partial_observability_api50_no_coord_summary.json` |
| PASS | `partial_api.private_landmark_candidate_refs` | 0 | 0 | `results/partial_observability_api50_check.json` |
| PASS | `partial_api.coordinate_candidates` | 50 | 50 | `results/partial_observability_api50_check.json` |
| PASS | `partial_api.mirror_private_refs` | 0 | 0 | `results/partial_observability_api50_check.json` |
| PASS | `partial_api.population_private_refs` | 0 | 0 | `results/partial_observability_api50_check.json` |
| PASS | `cross_model_listener.rows` | 6 | 6 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_5_4_nano.mirror` | 0.813 | 0.813 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_5_4_nano.population` | 1.000 | 1.000 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_5_4_nano.gap` | 0.187 | 0.187 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_4_1_nano.mirror` | 0.713 | 0.713 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_4_1_nano.population` | 1.000 | 1.000 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_4_1_nano.gap` | 0.287 | 0.287 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_5_5.mirror` | 0.673 | 0.673 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_5_5.population` | 1.000 | 1.000 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.perspective_stress.gpt_5_5.gap` | 0.327 | 0.327 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_5_4_nano.mirror` | 0.667 | 0.667 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_5_4_nano.population` | 1.000 | 1.000 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_5_4_nano.gap` | 0.333 | 0.333 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_4_1_nano.mirror` | 0.660 | 0.660 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_4_1_nano.population` | 1.000 | 1.000 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_4_1_nano.gap` | 0.340 | 0.340 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_5_5.mirror` | 0.653 | 0.653 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_5_5.population` | 1.000 | 1.000 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_listener.partial_observability.gpt_5_5.gap` | 0.347 | 0.347 | `results/cross_model_listener_audit.json` |
| PASS | `cross_model_failure_overlap.perspective_gpt55_mirror_success` | 0.673 | 0.673 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_gpt55_mirror_failure_scenes` | 25 | 25 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_gpt55_mirror_failure_symbolic_rate` | 1.000 | 1.000 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_gpt55_population_failure_scenes` | 0 | 0 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_gpt41_gpt55_mirror_failure_overlap` | 20 | 20 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_gpt41_gpt55_overlap_over_gpt41` | 0.909 | 0.909 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_all_listener_mirror_failure_scenes` | 10 | 10 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_any_listener_mirror_failure_scenes` | 30 | 30 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_gpt55_mirror_success` | 0.653 | 0.653 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_gpt55_mirror_failure_scenes` | 26 | 26 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_gpt55_mirror_failure_symbolic_rate` | 1.000 | 1.000 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_gpt55_population_failure_scenes` | 0 | 0 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_gpt41_gpt55_mirror_failure_overlap` | 26 | 26 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_gpt41_gpt55_overlap_over_gpt41` | 1.000 | 1.000 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_all_listener_mirror_failure_scenes` | 25 | 25 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_any_listener_mirror_failure_scenes` | 26 | 26 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_stress.gpt-4.1-nano` | 22 | 22 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_stress.gpt-5.4-nano` | 14 | 14 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_stress.gpt-5.5` | 25 | 25 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_stress.all` | 10 | 10 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.perspective_stress.any` | 30 | 30 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_observability.gpt-4.1-nano` | 26 | 26 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_observability.gpt-5.4-nano` | 25 | 25 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_observability.gpt-5.5` | 26 | 26 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_observability.all` | 25 | 25 | `results/cross_model_failure_overlap.json` |
| PASS | `cross_model_failure_overlap.partial_observability.any` | 26 | 26 | `results/cross_model_failure_overlap.json` |
| PASS | `gpt55_speaker_smoke.same_scene_count` | 10 | 10 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.existing_direct_success` | 0.800 | 0.800 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.gpt55_direct_success` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.direct_first_gain` | 0.200 | 0.200 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.existing_mirror_success` | 0.667 | 0.667 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.gpt55_mirror_success` | 0.867 | 0.867 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.mirror_gain` | 0.200 | 0.200 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.existing_population_success` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.gpt55_population_success` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.population_gain` | 0.000 | 0.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.oracle_gain` | 0.000 | 0.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.existing_k1_robust` | 0.700 | 0.700 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.gpt55_k1_robust` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.uncached_speaker_calls` | 10 | 10 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_smoke.speaker_tokens` | 8485 | 8485 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.api_direct_first.success` | 0.993 | 0.993 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.api_best_of_k_shortest.success` | 0.800 | 0.800 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.hybrid_local_mirror_api_eval.success` | 0.853 | 0.853 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.hybrid_local_mirror_api_eval.sameplay_success` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.hybrid_local_mirror_api_eval.crossplay_gap` | 0.147 | 0.147 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.hybrid_local_population_api_eval.success` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.oracle_upper_bound.success` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.n_scenes` | 50 | 50 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.k1_robust` | 0.980 | 0.980 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.k2_robust` | 1.000 | 1.000 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.uncached_speaker_calls` | 30 | 30 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_speaker_50scene.uncached_speaker_tokens` | 25478 | 25478 | `results/gpt55_speaker_smoke.json` |
| PASS | `gpt55_no_coord_k8.k4_kept_candidates` | 148 | 148 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k4_excluded_candidates` | 52 | 52 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k4_coordinate_violations` | 52 | 52 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k4_oracle` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k4_population` | 0.833 | 0.833 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k4_consensus_info` | 0.993 | 0.993 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_kept_candidates` | 400 | 400 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_excluded_candidates` | 0 | 0 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_coordinate_violations` | 0 | 0 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_direct_first` | 0.973 | 0.973 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_shortest` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_population` | 0.993 | 0.993 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_consensus_info` | 0.900 | 0.900 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_oracle` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_filter.kept` | 400 | 400 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_filter.excluded` | 0 | 0 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.k8_coordinate_audit.violations` | 0 | 0 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k1.oracle` | 0.973 | 0.973 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k1.robust_scene_rate` | 0.960 | 0.960 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k1.mean_robust_candidates` | 0.960 | 0.960 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k2.oracle` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k2.robust_scene_rate` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k2.mean_robust_candidates` | 1.960 | 1.960 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k4.oracle` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k4.robust_scene_rate` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k4.mean_robust_candidates` | 3.780 | 3.780 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k8.oracle` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k8.robust_scene_rate` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.budget.k8.mean_robust_candidates` | 7.420 | 7.420 | `results/gpt55_no_coord_k8_comparison.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_direct_first` | 0.973 | 0.973 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_best_of_k_shortest` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_mirror` | 0.953 | 0.953 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_population` | 0.993 | 0.993 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_consensus_info` | 0.900 | 0.900 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_informative` | 0.900 | 0.900 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.no_coord_oracle` | 1.000 | 1.000 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.filter_kept` | 400 | 400 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_no_coord_k8.summary.filter_excluded` | 0 | 0 | `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json` |
| PASS | `gpt55_followup_plan_status.covered` | 5 | 5 | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.partial` | 1 | 1 | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.future` | 0 | 0 | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.total` | 6 | 6 | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.missing_evidence_paths` | 0 | 0 | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.exp1_gpt55_listener_audit.covered` | present | present | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.exp2_cross_model_matrix.covered` | present | present | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.exp3_gpt55_speaker_generation.covered` | present | present | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.exp4_k8_no_coordinate_generation.covered` | present | present | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.exp5_human_validation.partial` | present | present | `results/gpt55_followup_plan_status.json` |
| PASS | `gpt55_followup_plan_status.exp6_rule_based_verifier.covered` | present | present | `results/gpt55_followup_plan_status.json` |
| PASS | `human_validation_packet.n_items` | 20 | 20 | `results/human_validation_answer_key.json` |
| PASS | `human_validation_packet.perspective_mirror_failure` | 10 | 10 | `results/human_validation_answer_key.json` |
| PASS | `human_validation_packet.partial_mirror_failure` | 5 | 5 | `results/human_validation_answer_key.json` |
| PASS | `human_validation_packet.mirror_success_control` | 5 | 5 | `results/human_validation_answer_key.json` |
| PASS | `human_validation_packet.participant_items` | 20 | 20 | `data/human_validation_items.jsonl` |
| PASS | `human_validation_packet.no_participant_label_fields` | present | present | `data/human_validation_items.jsonl` |
| PASS | `human_validation_packet.response_template_rows` | 20 | 20 | `data/human_validation_response_template.csv` |
| PASS | `api_loo.mixed_50.mirror` | 0.953 | 0.953 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.mixed_50.population` | 0.973 | 0.973 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.mixed_50.oracle` | 1.000 | 1.000 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.mixed_50.population_minus_mirror` | 0.020 | 0.020 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.mixed_50.n_units` | 150 | 150 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt54.mirror` | 0.907 | 0.907 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt54.population` | 0.933 | 0.933 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt54.oracle` | 1.000 | 1.000 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt54.population_minus_mirror` | 0.027 | 0.027 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt54.n_units` | 150 | 150 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt41.mirror` | 0.847 | 0.847 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt41.population` | 0.940 | 0.940 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt41.oracle` | 1.000 | 1.000 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt41.population_minus_mirror` | 0.093 | 0.093 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.perspective_gpt41.n_units` | 150 | 150 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.partial_observability.mirror` | 0.767 | 0.767 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.partial_observability.population` | 0.940 | 0.940 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.partial_observability.oracle` | 1.000 | 1.000 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.partial_observability.population_minus_mirror` | 0.173 | 0.173 | `results/api_listener_leave_one_out.json` |
| PASS | `api_loo.partial_observability.n_units` | 150 | 150 | `results/api_listener_leave_one_out.json` |
| PASS | `selection_regret.mixed_50_full.mirror` | 0.093 | 0.093 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.perspective_gpt54_full.mirror` | 0.187 | 0.187 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.perspective_gpt41_full.mirror` | 0.287 | 0.287 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.partial_observability_full.mirror` | 0.333 | 0.333 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.mixed_50_full.population` | 0.000 | 0.000 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.perspective_gpt54_full.population` | 0.000 | 0.000 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.perspective_gpt41_full.population` | 0.000 | 0.000 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.partial_observability_full.population` | 0.000 | 0.000 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.mixed_50_no_coord.consensus+info` | 0.040 | 0.040 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.perspective_gpt41_no_coord.consensus+info` | 0.033 | 0.033 | `results/selection_regret_audit.json` |
| PASS | `selection_regret.partial_observability_no_coord.consensus+info` | 0.013 | 0.013 | `results/selection_regret_audit.json` |
| PASS | `candidate_pool.mixed_50_full.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_full.mean_robust_candidates` | 3.300 | 3.300 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_full.oracle_success` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.mean_robust_candidates` | 2.440 | 2.440 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.oracle_success` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.mean_robust_candidates` | 2.140 | 2.140 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.oracle_success` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.mean_robust_candidates` | 2.580 | 2.580 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.oracle_success` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_no_coord.robust_scene_rate` | 0.920 | 0.920 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_no_coord.mean_robust_candidates` | 2.300 | 2.300 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_no_coord.oracle_success` | 0.960 | 0.960 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_no_coord.robust_scene_rate` | 0.660 | 0.660 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_no_coord.mean_robust_candidates` | 1.140 | 1.140 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_no_coord.oracle_success` | 0.793 | 0.793 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_no_coord.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_no_coord.mean_robust_candidates` | 1.580 | 1.580 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_no_coord.oracle_success` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_full.mirror.selected_robust_rate` | 0.860 | 0.860 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_full.mirror.oracle_match_rate` | 0.860 | 0.860 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.mirror.selected_robust_rate` | 0.720 | 0.720 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.mirror.oracle_match_rate` | 0.720 | 0.720 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.mirror.selected_robust_rate` | 0.560 | 0.560 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.mirror.oracle_match_rate` | 0.560 | 0.560 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.mirror.selected_robust_rate` | 0.500 | 0.500 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.mirror.oracle_match_rate` | 0.500 | 0.500 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_full.population.selected_robust_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_full.population.oracle_match_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.population.selected_robust_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt54_full.population.oracle_match_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.population.selected_robust_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_full.population.oracle_match_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.population.selected_robust_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_full.population.oracle_match_rate` | 1.000 | 1.000 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_no_coord.consensus+info.selected_robust_rate` | 0.880 | 0.880 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.mixed_50_no_coord.consensus+info.oracle_match_rate` | 0.940 | 0.940 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_no_coord.consensus+info.selected_robust_rate` | 0.620 | 0.620 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.perspective_gpt41_no_coord.consensus+info.oracle_match_rate` | 0.920 | 0.920 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_no_coord.consensus+info.selected_robust_rate` | 0.980 | 0.980 | `results/candidate_pool_audit.json` |
| PASS | `candidate_pool.partial_observability_no_coord.consensus+info.oracle_match_rate` | 0.980 | 0.980 | `results/candidate_pool_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k1.oracle` | 0.840 | 0.840 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k1.robust_scene_rate` | 0.780 | 0.780 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k2.oracle` | 0.853 | 0.853 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k2.robust_scene_rate` | 0.800 | 0.800 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k3.oracle` | 0.960 | 0.960 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k3.robust_scene_rate` | 0.920 | 0.920 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k4.oracle` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.mixed_50_full.k4.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k1.oracle` | 0.713 | 0.713 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k1.robust_scene_rate` | 0.600 | 0.600 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k2.oracle` | 0.787 | 0.787 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k2.robust_scene_rate` | 0.680 | 0.680 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k3.oracle` | 0.893 | 0.893 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k3.robust_scene_rate` | 0.820 | 0.820 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k4.oracle` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt54_full.k4.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k1.oracle` | 0.553 | 0.553 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k1.robust_scene_rate` | 0.380 | 0.380 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k2.oracle` | 0.620 | 0.620 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k2.robust_scene_rate` | 0.400 | 0.400 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k3.oracle` | 0.793 | 0.793 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k3.robust_scene_rate` | 0.660 | 0.660 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k4.oracle` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.perspective_gpt41_full.k4.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k1.oracle` | 0.740 | 0.740 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k1.robust_scene_rate` | 0.620 | 0.620 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k2.oracle` | 0.747 | 0.747 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k2.robust_scene_rate` | 0.620 | 0.620 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k3.oracle` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k3.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k4.oracle` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_budget.partial_observability_full.k4.robust_scene_rate` | 1.000 | 1.000 | `results/candidate_budget_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.mirror.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.mirror.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.mirror.attribute_short` | 0.760 | 0.760 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.mirror.coordinate_fallback` | 0.140 | 0.140 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.population.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.population.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.population.attribute_short` | 0.500 | 0.500 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_full.population.coordinate_fallback` | 0.420 | 0.420 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt54_full.population.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt54_full.population.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt54_full.population.attribute_short` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt54_full.population.coordinate_fallback` | 1.000 | 1.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_full.population.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_full.population.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_full.population.attribute_short` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_full.population.coordinate_fallback` | 1.000 | 1.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_full.population.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_full.population.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_full.population.attribute_short` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_full.population.coordinate_fallback` | 1.000 | 1.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_no_coord.consensus+info.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_no_coord.consensus+info.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_no_coord.consensus+info.attribute_short` | 0.320 | 0.320 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_no_coord.consensus+info.relational_or_spatial` | 0.360 | 0.360 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.mixed_50_no_coord.consensus+info.coordinate_fallback` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.consensus+info.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.consensus+info.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.consensus+info.attribute_short` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.consensus+info.relational_or_spatial` | 0.580 | 0.580 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.consensus+info.coordinate_fallback` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_no_coord.consensus+info.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_no_coord.consensus+info.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_no_coord.consensus+info.attribute_short` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_no_coord.consensus+info.relational_or_spatial` | 0.460 | 0.460 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.partial_observability_no_coord.consensus+info.coordinate_fallback` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.population.n_scenes` | 50 | 50 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.population.unresolved` | 0 | 0 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.population.attribute_short` | 0.920 | 0.920 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.population.relational_or_spatial` | 0.080 | 0.080 | `results/candidate_role_selection_audit.json` |
| PASS | `candidate_role_selection.perspective_gpt41_no_coord.population.coordinate_fallback` | 0.000 | 0.000 | `results/candidate_role_selection_audit.json` |
| PASS | `random_baseline.mixed_50_full.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_full.mean_candidates` | 4.000 | 4.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_full.random_expected` | 0.865 | 0.865 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_full.random_robust_pick_rate` | 0.825 | 0.825 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_full.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_full.primary_minus_random` | 0.135 | 0.135 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt54_full.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt54_full.mean_candidates` | 4.000 | 4.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt54_full.random_expected` | 0.715 | 0.715 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt54_full.random_robust_pick_rate` | 0.610 | 0.610 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt54_full.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt54_full.primary_minus_random` | 0.285 | 0.285 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_full.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_full.mean_candidates` | 4.000 | 4.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_full.random_expected` | 0.657 | 0.657 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_full.random_robust_pick_rate` | 0.535 | 0.535 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_full.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_full.primary_minus_random` | 0.343 | 0.343 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_full.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_full.mean_candidates` | 4.000 | 4.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_full.random_expected` | 0.753 | 0.753 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_full.random_robust_pick_rate` | 0.645 | 0.645 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_full.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_full.primary_minus_random` | 0.247 | 0.247 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_no_coord.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_no_coord.mean_candidates` | 3.000 | 3.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_no_coord.random_expected` | 0.820 | 0.820 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_no_coord.random_robust_pick_rate` | 0.767 | 0.767 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_no_coord.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.mixed_50_no_coord.primary_minus_random` | 0.100 | 0.100 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_no_coord.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_no_coord.mean_candidates` | 3.000 | 3.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_no_coord.random_expected` | 0.542 | 0.542 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_no_coord.random_robust_pick_rate` | 0.380 | 0.380 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_no_coord.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.perspective_gpt41_no_coord.primary_minus_random` | 0.218 | 0.218 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_no_coord.n_scenes` | 50 | 50 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_no_coord.mean_candidates` | 3.000 | 3.000 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_no_coord.random_expected` | 0.671 | 0.671 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_no_coord.random_robust_pick_rate` | 0.527 | 0.527 | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_no_coord.primary_method` | present | present | `results/random_candidate_baseline.json` |
| PASS | `random_baseline.partial_observability_no_coord.primary_minus_random` | 0.316 | 0.316 | `results/random_candidate_baseline.json` |
| PASS | `message_length.mixed_50_full.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_full.mirror_tokens` | 5.56 | 5.56 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_full.primary_tokens` | 6.82 | 6.82 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_full.direct_tokens` | 9.26 | 9.26 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_full.template_tokens` | 10.00 | 10.00 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_full.token_delta` | 1.26 | 1.26 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_full.success_delta` | 0.093 | 0.093 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.mirror_tokens` | 7.40 | 7.40 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.primary_tokens` | 10.22 | 10.22 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.direct_tokens` | 11.70 | 11.70 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.template_tokens` | 10.00 | 10.00 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.token_delta` | 2.82 | 2.82 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt54_full.success_delta` | 0.187 | 0.187 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.mirror_tokens` | 7.40 | 7.40 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.primary_tokens` | 10.22 | 10.22 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.direct_tokens` | 11.70 | 11.70 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.template_tokens` | 10.00 | 10.00 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.token_delta` | 2.82 | 2.82 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_full.success_delta` | 0.287 | 0.287 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.mirror_tokens` | 6.50 | 6.50 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.primary_tokens` | 9.66 | 9.66 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.direct_tokens` | 9.96 | 9.96 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.template_tokens` | 10.00 | 10.00 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.token_delta` | 3.16 | 3.16 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_full.success_delta` | 0.333 | 0.333 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_no_coord.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_no_coord.mirror_tokens` | 5.00 | 5.00 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_no_coord.primary_tokens` | 9.38 | 9.38 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_no_coord.direct_tokens` | 9.26 | 9.26 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_no_coord.token_delta` | 4.38 | 4.38 | `results/message_length_audit.json` |
| PASS | `message_length.mixed_50_no_coord.success_delta` | 0.133 | 0.133 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_no_coord.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_no_coord.mirror_tokens` | 8.28 | 8.28 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_no_coord.primary_tokens` | 12.54 | 12.54 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_no_coord.direct_tokens` | 11.70 | 11.70 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_no_coord.token_delta` | 4.26 | 4.26 | `results/message_length_audit.json` |
| PASS | `message_length.perspective_gpt41_no_coord.success_delta` | 0.180 | 0.180 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_no_coord.primary_method` | present | present | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_no_coord.mirror_tokens` | 7.56 | 7.56 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_no_coord.primary_tokens` | 12.76 | 12.76 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_no_coord.direct_tokens` | 9.96 | 9.96 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_no_coord.token_delta` | 5.20 | 5.20 | `results/message_length_audit.json` |
| PASS | `message_length.partial_observability_no_coord.success_delta` | 0.380 | 0.380 | `results/message_length_audit.json` |
| PASS | `listener_disagreement.mixed_50_full.mirror.split` | 0.080 | 0.080 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.mixed_50_full.mirror.unanimous_success` | 0.860 | 0.860 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt54_full.mirror.split` | 0.180 | 0.180 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt54_full.mirror.unanimous_success` | 0.720 | 0.720 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt41_full.mirror.split` | 0.360 | 0.360 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt41_full.mirror.unanimous_success` | 0.560 | 0.560 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_full.mirror.split` | 0.500 | 0.500 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_full.mirror.unanimous_success` | 0.500 | 0.500 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.mixed_50_full.population.split` | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.mixed_50_full.population.unanimous_success` | 1.000 | 1.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt54_full.population.split` | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt54_full.population.unanimous_success` | 1.000 | 1.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt41_full.population.split` | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt41_full.population.unanimous_success` | 1.000 | 1.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_full.population.split` | 0.000 | 0.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_full.population.unanimous_success` | 1.000 | 1.000 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.mixed_50_no_coord.consensus+info.split` | 0.080 | 0.080 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.mixed_50_no_coord.consensus+info.unanimous_success` | 0.880 | 0.880 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt41_no_coord.consensus+info.split` | 0.260 | 0.260 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.perspective_gpt41_no_coord.consensus+info.unanimous_success` | 0.620 | 0.620 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_no_coord.consensus+info.split` | 0.020 | 0.020 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_no_coord.consensus+info.unanimous_success` | 0.980 | 0.980 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_no_coord.mirror.split` | 0.540 | 0.540 | `results/listener_disagreement_audit.json` |
| PASS | `listener_disagreement.partial_observability_no_coord.mirror.unanimous_success` | 0.420 | 0.420 | `results/listener_disagreement_audit.json` |
| PASS | `listener_confidence.threshold` | 0.8 | 0.8 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_full.mirror.ambiguity` | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_full.mirror.high_conf_failure` | 0.147 | 0.147 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_full.mirror.scene_high_conf_failure` | 0.280 | 0.280 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_no_coord.mirror.ambiguity` | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_no_coord.mirror.high_conf_failure` | 0.280 | 0.280 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_no_coord.mirror.scene_high_conf_failure` | 0.480 | 0.480 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_full.population.high_conf_failure` | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.perspective_gpt41_full.population.scene_high_conf_failure` | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.partial_observability_no_coord.consensus+info.high_conf_failure` | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.partial_observability_no_coord.consensus+info.scene_high_conf_failure` | 0.000 | 0.000 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.partial_observability_full.mirror.ambiguity` | 0.140 | 0.140 | `results/listener_confidence_audit.json` |
| PASS | `listener_confidence.partial_observability_full.mirror.high_conf_failure` | 0.073 | 0.073 | `results/listener_confidence_audit.json` |
| PASS | `failure_taxonomy.perspective_gpt41_full_mirror.total` | 43 | 43 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.perspective_gpt41_full_mirror.underspecified` | 38 | 38 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.perspective_gpt41_full_mirror.perspective` | 5 | 5 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.partial_observability_full_mirror.total` | 50 | 50 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.partial_observability_full_mirror.underspecified` | 50 | 50 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.partial_observability_full_mirror.perspective` | 0 | 0 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.partial_observability_no_coord_mirror.total` | 59 | 59 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.partial_observability_no_coord_mirror.underspecified` | 59 | 59 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.partial_observability_no_coord_mirror.perspective` | 0 | 0 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.combined.total` | 152 | 152 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.combined.underspecified` | 147 | 147 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.combined.perspective` | 5 | 5 | `results/failure_taxonomy_audit.json` |
| PASS | `failure_taxonomy.combined.other` | 0 | 0 | `results/failure_taxonomy_audit.json` |
| PASS | `rule_based_ambiguity.combined.n_rows` | 152 | 152 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.combined.n_underspecified_distractor` | 147 | 147 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.combined.n_perspective_frame_error` | 5 | 5 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.combined.underspecified_precision` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.combined.underspecified_recall` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.combined.frame_sensitive_recall` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.combined.symbolic_recall` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.findings.perspective_mirror_failure_symbolic_rate` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.findings.perspective_population_symbolic_rate` | 0.000 | 0.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.findings.partial_mirror_failure_symbolic_rate` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.findings.partial_population_symbolic_rate` | 0.000 | 0.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.findings.partial_no_coord_mirror_failure_symbolic_rate` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `rule_based_ambiguity.findings.partial_no_coord_consensus_symbolic_rate` | 1.000 | 1.000 | `results/rule_based_ambiguity_verifier.json` |
| PASS | `interaction_memory_rules.combined.failure_rows` | 152 | 152 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.combined.failure_scenes` | 76 | 76 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.combined.mean_repair_success` | 0.991 | 0.991 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.combined.repair_all_success` | 0.987 | 0.987 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.combined.repair_rule_cue` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.rule.disambiguate_shared_attributes` | 147 | 147 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.rule.avoid_frame_sensitive_only` | 5 | 5 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.perspective_frame_error.rows` | 5 | 5 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.perspective_frame_error.scenes` | 3 | 3 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.perspective_frame_error.repair_success` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.perspective_frame_error.cue` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.underspecified_distractor.rows` | 38 | 38 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.underspecified_distractor.scenes` | 19 | 19 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.underspecified_distractor.repair_success` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.perspective_full_mirror.underspecified_distractor.cue` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_full_mirror.underspecified_distractor.rows` | 50 | 50 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_full_mirror.underspecified_distractor.scenes` | 25 | 25 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_full_mirror.underspecified_distractor.repair_success` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_full_mirror.underspecified_distractor.cue` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_no_coord_mirror.underspecified_distractor.rows` | 59 | 59 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_no_coord_mirror.underspecified_distractor.scenes` | 29 | 29 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_no_coord_mirror.underspecified_distractor.repair_success` | 0.977 | 0.977 | `results/interaction_memory_rules.json` |
| PASS | `interaction_memory_rules.partial_observability_no_coord_mirror.underspecified_distractor.cue` | 1.000 | 1.000 | `results/interaction_memory_rules.json` |
| PASS | `qualitative_examples.n_examples` | 4 | 4 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_underspecification.scene` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_underspecification.category` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_underspecification.mirror_success` | 0.333 | 0.333 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_underspecification.repair_success` | 1.000 | 1.000 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_frame_error.scene` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_frame_error.category` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_frame_error.mirror_success` | 0.667 | 0.667 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.perspective_frame_error.repair_success` | 1.000 | 1.000 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_underspecification.scene` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_underspecification.category` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_underspecification.mirror_success` | 0.333 | 0.333 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_underspecification.repair_success` | 1.000 | 1.000 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_no_coordinate_repair.scene` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_no_coordinate_repair.category` | present | present | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_no_coordinate_repair.mirror_success` | 0.333 | 0.333 | `results/qualitative_failure_examples.json` |
| PASS | `qualitative_examples.partial_observability_no_coordinate_repair.repair_success` | 1.000 | 1.000 | `results/qualitative_failure_examples.json` |
| PASS | `reviewer_checklist.n_items` | 19 | 19 | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.n_failed` | 0 | 0 | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.target_id_is_never_shown_to_the_listener.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.target_id_is_never_shown_to_the_listener.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.target_id_is_never_shown_to_the_listener.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.speaker_messages_are_checked_for_target_id_leakage.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.speaker_messages_are_checked_for_target_id_leakage.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.speaker_messages_are_checked_for_target_id_leakage.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.listener_outputs_are_valid_object_ids.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.listener_outputs_are_valid_object_ids.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.listener_outputs_are_valid_object_ids.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.same_test_scenes_are_used_across_methods.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.same_test_scenes_are_used_across_methods.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.same_test_scenes_are_used_across_methods.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.prompts_are_frozen_before_final_evaluation.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.prompts_are_frozen_before_final_evaluation.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.prompts_are_frozen_before_final_evaluation.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.held_out_listeners_are_not_used_for_method_selection.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.held_out_listeners_are_not_used_for_method_selection.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.held_out_listeners_are_not_used_for_method_selection.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.all_responses_are_cached.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.all_responses_are_cached.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.all_responses_are_cached.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.exact_model_versions_are_reported.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.exact_model_versions_are_reported.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.exact_model_versions_are_reported.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.main_table_has_confidence_intervals.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.main_table_has_confidence_intervals.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.main_table_has_confidence_intervals.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.scenario_table_explains_where_gains_losses_occur.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.scenario_table_explains_where_gains_losses_occur.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.scenario_table_explains_where_gains_losses_occur.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.cross_play_gap_is_reported.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.cross_play_gap_is_reported.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.cross_play_gap_is_reported.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.oracle_upper_bound_is_reported.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.oracle_upper_bound_is_reported.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.oracle_upper_bound_is_reported.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.manual_failure_examples_support_the_quantitative_result.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.manual_failure_examples_support_the_quantitative_result.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.manual_failure_examples_support_the_quantitative_result.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.intro_states_the_evaluation_blind_spot_clearly.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.intro_states_the_evaluation_blind_spot_clearly.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.intro_states_the_evaluation_blind_spot_clearly.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.related_work_is_concise.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.related_work_is_concise.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.related_work_is_concise.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.method_is_reproducible.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.method_is_reproducible.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.method_is_reproducible.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.limitations_are_honest.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.limitations_are_honest.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.limitations_are_honest.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.claims_match_actual_results.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.claims_match_actual_results.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.claims_match_actual_results.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.appendix_includes_prompts_and_schemas.present` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.appendix_includes_prompts_and_schemas.section` | present | present | `results/reviewer_checklist.json` |
| PASS | `reviewer_checklist.appendix_includes_prompts_and_schemas.pass` | present | present | `results/reviewer_checklist.json` |
| PASS | `plan_coverage.n_items` | 24 | 24 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.status_counts.covered` | 20 | 20 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.status_counts.partial` | 4 | 4 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.status_counts.open` | 0 | 0 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.core_status_counts.covered` | 17 | 17 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.core_status_counts.partial` | 2 | 2 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.core_status_counts.open` | 0 | 0 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.stretch_status_counts.covered` | 3 | 3 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.stretch_status_counts.partial` | 2 | 2 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.stretch_status_counts.open` | 0 | 0 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.open_or_partial` | 4 | 4 | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.use_development_episodes_for_debugging_prompts_and_tuning_the_generator.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.use_development_episodes_for_debugging_prompts_and_tuning_the_generator.partial` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.hand_label_roughly_100_failures_into_interpretable_categories.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.hand_label_roughly_100_failures_into_interpretable_categories.partial` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.run_a_1_000_scene_benchmark_and_200_partial_observability_stress_episodes.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.run_a_1_000_scene_benchmark_and_200_partial_observability_stress_episodes.partial` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.evaluate_k_8_candidate_generation_in_addition_to_k_4.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.evaluate_k_8_candidate_generation_in_addition_to_k_4.covered` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.run_an_actual_interaction_memory_prompt_rerun_after_distilling_rules_from_failures.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.run_an_actual_interaction_memory_prompt_rerun_after_distilling_rules_from_failures.partial` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.validate_failures_with_human_or_independent_non_llm_judgments.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.validate_failures_with_human_or_independent_non_llm_judgments.covered` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.publish_the_artifact_as_a_public_repository_or_submission_bundle.present` | present | present | `results/plan_coverage_audit.json` |
| PASS | `plan_coverage.item.publish_the_artifact_as_a_public_repository_or_submission_bundle.covered` | present | present | `results/plan_coverage_audit.json` |
| PASS | `integrity_audit.n_failed` | 0 | 0 | `results/benchmark_integrity_audit.json` |
| PASS | `integrity_audit.n_checks` | 290 | 290 | `results/benchmark_integrity_audit.json` |
| PASS | `integrity_audit.local_benchmark600.scenes` | 600 | 600 | `results/benchmark_integrity_audit.json` |
| PASS | `integrity_audit.local_benchmark600.record_rows` | 10800 | 10800 | `results/benchmark_integrity_audit.json` |
| PASS | `integrity_audit.has_exact_gpt54_version` | present | present | `results/benchmark_integrity_audit.json` |
| PASS | `integrity_audit.has_exact_gpt41_version` | present | present | `results/benchmark_integrity_audit.json` |
| PASS | `integrity_audit.has_exact_gpt55_version` | present | present | `results/benchmark_integrity_audit.json` |
| PASS | `api_token_accounting.n_cache_files` | 7113 | 7113 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.n_readable` | 7113 | 7113 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.n_missing_usage` | 0 | 0 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.input_tokens` | 1874818 | 1874818 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.output_tokens` | 177461 | 177461 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.total_tokens` | 2052279 | 2052279 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.gpt-4.1-nano.gpt-4.1-nano-2025-04-14.responses` | 1236 | 1236 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.gpt-4.1-nano.gpt-4.1-nano-2025-04-14.total_tokens` | 332257 | 332257 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.gpt-5.4-nano.gpt-5.4-nano-2026-03-17.responses` | 2770 | 2770 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.gpt-5.4-nano.gpt-5.4-nano-2026-03-17.total_tokens` | 820710 | 820710 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.gpt-5.5.gpt-5.5-2026-04-23.responses` | 3107 | 3107 | `results/api_token_accounting.json` |
| PASS | `api_token_accounting.gpt-5.5.gpt-5.5-2026-04-23.total_tokens` | 899312 | 899312 | `results/api_token_accounting.json` |
| PASS | `text.paper/main.tex.consensus+info reaches 0.760` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.consensus+info success of 0.920` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.A candidate-role audit shows` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.coordinate-fallback slot in 1.000 of scenes` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.naive population-play selects a spatially informative message in only 4 of 50` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.gpt-5.4-nano-2026-03-17` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.gpt-5.5-2026-04-23` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.generated prompt and schema documentation` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.artifact guide mapping paper claims` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.population-minus-mirror difference is 0.327` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.\label{tab:crossmodel}` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.cache-only leave-one-listener-out analysis` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.selection-regret audit makes this decomposition explicit` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.mirror self-play leaves regrets of 0.093, 0.187, 0.287, and 0.333` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.consensus+info reduces regret to 0.040` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.candidate-pool audit asks whether any candidate succeeds` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.population-play selects a robust candidate in 1.000 of scenes` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.robust non-coordinate candidates remain available in 0.920, 0.660, and 1.000` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.A uniform-random candidate baseline rules out the explanation that any candidate would do` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.Random expected success is 0.865, 0.715, 0.657, and 0.753` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.population-play improves over random by 0.135, 0.285, 0.343, and 0.247` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.consensus+info improves over random by 0.100, 0.218, and 0.316` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.prefix-$K$ candidate-budget audit shows why the four-candidate protocol is useful` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.from 0.380 at $K=1$ to 0.660 at $K=3$ and 1.000 at $K=4$` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.A held-out listener-disagreement audit shows` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.split held-out outcomes in 0.080, 0.180, 0.360, and 0.500` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.consensus+info reduces split outcomes from mirror's 0.540 to 0.020` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.listener-confidence audit further shows that self-reported uncertainty is not` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.mirror self-play still produces high-confidence failures` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.In scene \texttt{ps\_000005}` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.In scene \texttt{ps\_000011}` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.A rule-based ambiguity verifier` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.recovers all 152 coded mirror-failure labels` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.A generated qualitative appendix adds two partial-observability examples` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.consensus+info repair that raises held-out success from 0.333 to 1.000` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.API-population selection uses the other two` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.0.940 vs. 0.847` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.benchmark integrity audit` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.\section{Related Work}` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.We generate five scenario families` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.We report three bounded API experiments` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.a 50-scene \texttt{gpt-5.5} speaker-generation audit` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.token-accounting report over 7,113 cached responses` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.The dedicated API K=8 no-coordinate run changes this interpretation` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.400 of 400 generated candidates survive the exact-coordinate filter` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.population-play rises from 0.833 to 0.993` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.consensus+info drops from 0.993 to 0.900` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.direct first-candidate success to 0.993` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.mirror selection still reaches only 0.853 cross-play success` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.paired population-minus-mirror difference of 0.147` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.The paper makes three contributions` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.no-API 600-scene balanced local sweep` | present | present | `paper/main.tex` |
| PASS | `text.docs/local_stronger_plan_k8.md.Local Stronger-Plan K=8 Diagnostic` | present | present | `docs/local_stronger_plan_k8.md` |
| PASS | `text.docs/local_stronger_plan_k8.md.No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8.` | present | present | `docs/local_stronger_plan_k8.md` |
| PASS | `text.docs/local_stronger_plan_k8.md.No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8.` | present | present | `docs/local_stronger_plan_k8.md` |
| PASS | `text.docs/local_stronger_plan_k8.md.Full-candidate local K=8 population-play reaches 1.000 over all 1,200 scenes.` | present | present | `docs/local_stronger_plan_k8.md` |
| PASS | `text.docs/protocol_and_prompts.md.PRAG-CrossPlay Protocol, Prompts, and Schemas` | present | present | `docs/protocol_and_prompts.md` |
| PASS | `text.docs/protocol_and_prompts.md.Speaker Prompt` | present | present | `docs/protocol_and_prompts.md` |
| PASS | `text.docs/protocol_and_prompts.md.Record Schema` | present | present | `docs/protocol_and_prompts.md` |
| PASS | `text.docs/protocol_and_prompts.md.a bounded `partial_observability` support run` | present | present | `docs/protocol_and_prompts.md` |
| PASS | `text.docs/api_token_accounting.md.API Token Accounting` | present | present | `docs/api_token_accounting.md` |
| PASS | `text.docs/api_token_accounting.md.7113 | 7113 | 0 | 1874818 | 177461 | 2052279` | present | present | `docs/api_token_accounting.md` |
| PASS | `text.docs/cross_model_listener_audit.md.Cross-Model Held-Out Listener Audit` | present | present | `docs/cross_model_listener_audit.md` |
| PASS | `text.docs/cross_model_listener_audit.md.Perspective stress | gpt-5.5 | 0.793 | 0.507 | 0.673 | 1.000 | 1.000` | present | present | `docs/cross_model_listener_audit.md` |
| PASS | `text.docs/cross_model_listener_audit.md.Partial observability | gpt-5.5 | 0.740 | 0.453 | 0.653 | 1.000 | 1.000` | present | present | `docs/cross_model_listener_audit.md` |
| PASS | `text.docs/cross_model_failure_overlap.md.Cross-Model Failure Overlap Audit` | present | present | `docs/cross_model_failure_overlap.md` |
| PASS | `text.docs/cross_model_failure_overlap.md.20 of the 22 GPT-4.1 mirror-failure scenes also fail under GPT-5.5` | present | present | `docs/cross_model_failure_overlap.md` |
| PASS | `text.docs/cross_model_failure_overlap.md.26 of the 26 GPT-4.1 mirror-failure scenes also fail under GPT-5.5` | present | present | `docs/cross_model_failure_overlap.md` |
| PASS | `text.docs/cross_model_failure_overlap.md.Population-play has 0 GPT-5.5 scene-level failures` | present | present | `docs/cross_model_failure_overlap.md` |
| PASS | `text.docs/gpt55_speaker_smoke_report.md.GPT-5.5 Speaker Smoke` | present | present | `docs/gpt55_speaker_smoke_report.md` |
| PASS | `text.docs/gpt55_speaker_smoke_report.md.Existing speaker direct-first success under GPT-5.5 is 0.800; GPT-5.5 speaker direct-first success is 1.000.` | present | present | `docs/gpt55_speaker_smoke_report.md` |
| PASS | `text.docs/gpt55_speaker_smoke_report.md.50-Scene Speaker Audit` | present | present | `docs/gpt55_speaker_smoke_report.md` |
| PASS | `text.docs/gpt55_speaker_smoke_report.md.| 50 | 0.993 | 0.800 | 0.853 | 1.000 | 0.147 | 1.000 | 1.000 |` | present | present | `docs/gpt55_speaker_smoke_report.md` |
| PASS | `text.docs/gpt55_speaker_smoke_report.md.The same-scene table remains a smoke comparison; the extension section is the current paper-facing Experiment 3 speaker result when it has 50 scenes.` | present | present | `docs/gpt55_speaker_smoke_report.md` |
| PASS | `text.docs/gpt55_followup_plan_status.md.GPT-5.5 Follow-Up Plan Status` | present | present | `docs/gpt55_followup_plan_status.md` |
| PASS | `text.docs/gpt55_followup_plan_status.md.Covered: 5. Partial: 1. Future: 0. Missing evidence paths: 0.` | present | present | `docs/gpt55_followup_plan_status.md` |
| PASS | `text.docs/gpt55_followup_plan_status.md.Safe to claim: the API K=8 no-coordinate run shows robust non-coordinate expressions are available` | present | present | `docs/gpt55_followup_plan_status.md` |
| PASS | `text.docs/gpt55_followup_plan_status.md.Not yet safe as paper headline: human listener validation.` | present | present | `docs/gpt55_followup_plan_status.md` |
| PASS | `text.docs/gpt55_no_coord_k8_report.md.GPT-5.5 K=8 No-Coordinate Audit` | present | present | `docs/gpt55_no_coord_k8_report.md` |
| PASS | `text.docs/gpt55_no_coord_k8_report.md.K=4 filtered baseline keeps 148 candidates and excludes 52 coordinate candidates; K=8 keeps 400 and excludes 0.` | present | present | `docs/gpt55_no_coord_k8_report.md` |
| PASS | `text.docs/gpt55_no_coord_k8_report.md.The dedicated K=8 no-coordinate prompt produced 0 exact-coordinate candidates across 50 scenes.` | present | present | `docs/gpt55_no_coord_k8_report.md` |
| PASS | `text.docs/gpt55_no_coord_k8_report.md.| Population | 0.833 | 0.993 | +0.160 |` | present | present | `docs/gpt55_no_coord_k8_report.md` |
| PASS | `text.docs/gpt55_no_coord_k8_report.md.| Consensus+info | 0.993 | 0.900 | -0.093 |` | present | present | `docs/gpt55_no_coord_k8_report.md` |
| PASS | `text.docs/human_validation_packet.md.Human Validation Packet` | present | present | `docs/human_validation_packet.md` |
| PASS | `text.docs/human_validation_packet.md.Items: 20. Condition counts: mirror_success_control=5, partial_mirror_failure=5, perspective_mirror_failure=10.` | present | present | `docs/human_validation_packet.md` |
| PASS | `text.docs/human_validation_packet.md.Participant files exclude condition labels, scene IDs, target IDs, and held-out success rates.` | present | present | `docs/human_validation_packet.md` |
| PASS | `text.docs/api_token_accounting.md.`gpt-5.4-nano` | `gpt-5.4-nano-2026-03-17` | 2770` | present | present | `docs/api_token_accounting.md` |
| PASS | `text.docs/artifact_guide.md.PRAG-CrossPlay Artifact Guide` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Claim-To-Evidence Map` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.API Token Accounting` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.7113 cached responses have complete usage metadata totaling 2052279 tokens` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Cross-Model Failure Overlap Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.20 of 22 GPT-4.1 mirror-failure scenes also fail under GPT-5.5` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.All GPT-5.5 mirror-failure scenes are symbolic-verifier positives` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.GPT-5.5 Speaker Smoke` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.direct-first rises from 0.800 to 1.000 and mirror rises from 0.667 to 0.867` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.This section keeps the original 10-scene same-scene smoke comparison` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.50-scene speaker audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.| 50 | 0.993 | 0.800 | 0.853 | 1.000 | 0.147 | 1.000 | 1.000 | 0.980 | 1.000 | 30 | 25478 |` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.GPT-5.5 Follow-Up Plan Status` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Covered: 5. Partial: 1. Future: 0. Missing evidence paths: 0.` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.The GPT-5.5 follow-up evidence is explicitly bounded by covered, partial, and future rows.` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.GPT-5.5 K=8 No-Coordinate Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.K=8 keeps 400 non-coordinate candidates and excludes 0` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.K=8 population-play improves from 0.833 to 0.993` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.consensus+info is not monotonic` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Human Validation Packet` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.the prepared packet has 20 participant-safe items` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Participant-facing files exclude condition labels, scene IDs, target IDs, and held-out success rates.` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Local Stronger-Plan K=8 Diagnostic` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.No-coordinate oracle success on the initial 1,000 scenes rises from 0.870 at K=4 to 0.995 at K=8` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.No-coordinate oracle success on the 200 partial-observability scenes rises from 0.495 at K=4 to 0.997 at K=8` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.At K=8 without exact coordinates, consensus+info reaches 0.992 on the initial 1,000 scenes and 0.997 on partial-observability scenes` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.API Listener Leave-One-Out Mechanism Check` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Selection Regret Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Candidate Pool Robustness Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Candidate Budget Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Candidate Role Selection Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Random Candidate Baseline` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Listener Disagreement Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Qualitative Failure Examples` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Reviewer Checklist` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Plan Coverage Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.full-candidate population-play has zero regret` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.population-play selects a robust candidate in 1.000 of scenes` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.alternate-model perspective robust-scene coverage rises from 0.380 at K=1 to 1.000 at K=4` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Full-candidate population coordinate-fallback rates: mixed_50_full=0.420, perspective_gpt54_full=1.000, perspective_gpt41_full=1.000, partial_observability_full=1.000` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.population-play improves over random by 0.135, 0.285, 0.343, and 0.247` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.consensus+info improves over random by 0.100, 0.218, and 0.316` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Message Length Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.full-candidate population selected messages average 6.82, 10.22, 10.22, and 9.66 tokens` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.mirror split-outcome rates are 0.080, 0.180, 0.360, and 0.500` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Listener Confidence Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.alternate-model perspective ambiguity flags are 0.000 while mirror high-confidence failure rates are 0.147 and 0.280` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Failure Taxonomy Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.147 of 152 coded listener-level mirror failures are underspecified-distractor cases` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Rule-Based Ambiguity Verifier` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.combined coded failure set has symbolic ambiguity recall 1.000, attribute-under-specification recall 1.000, and frame-sensitive recall 1.000` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.perspective mirror failure scenes flagged` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Interaction Memory Rule Audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Coded failure rows: 152; unique failure scenes: 76` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.repair cue satisfies derived rule in 1.000 of failure scenes` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.four cache-only examples show mirror-selected messages failing held-out listeners` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Section 32 reviewer checklist passes all 19 core-validity, results, and paper items` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Items passed: 19/19` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Core scope: 17 covered, 2 partial, 0 open.` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Stretch scope: 3 covered, 2 partial, 0 open.` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.stretch scope has 3 covered, 2 partial, 0 open after adding the API K=8 no-coordinate audit` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.Local Benchmark-Scale Sanity Check` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.600 local scenes balanced across four initial scenario families` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.partial_observability_api50 | `data/partial_observability_local50_scenes.jsonl` | 50` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.cache-only API listener leave-one-out improves population over mirror` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.0 candidate messages reference private landmarks` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.all 50 full-run mirror failures are underspecified-distractor choices` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.local_benchmark600 | `data/local_benchmark600_scenes.jsonl` | 600 | 10800` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/artifact_guide.md.290/290 integrity checks pass` | present | present | `docs/artifact_guide.md` |
| PASS | `text.docs/local_benchmark600_check.md.Mirror self-play has same-play 1.000 but cross-play 0.631` | present | present | `docs/local_benchmark600_check.md` |
| PASS | `text.docs/local_benchmark600_check.md.perspective_shift | 0.000 | 0.158 | 1.000 | 0.842` | present | present | `docs/local_benchmark600_check.md` |
| PASS | `text.docs/api_listener_leave_one_out.md.API Listener Leave-One-Out Analysis` | present | present | `docs/api_listener_leave_one_out.md` |
| PASS | `text.docs/api_listener_leave_one_out.md.partial_observability | scene_eval_listener | 150 | 0.940 | 0.767 | 0.173` | present | present | `docs/api_listener_leave_one_out.md` |
| PASS | `text.docs/selection_regret_audit.md.perspective_gpt41_full | mirror | 50 | 0.713 | 1.000 | 0.287` | present | present | `docs/selection_regret_audit.md` |
| PASS | `text.docs/selection_regret_audit.md.partial_observability_no_coord | consensus+info | 50 | 0.987 | 1.000 | 0.013` | present | present | `docs/selection_regret_audit.md` |
| PASS | `text.docs/candidate_pool_audit.md.perspective_gpt41_no_coord | no_exact_coordinates | 50 | 3.00 | 1.14 | 0.660 | 0.793` | present | present | `docs/candidate_pool_audit.md` |
| PASS | `text.docs/candidate_pool_audit.md.partial_observability_no_coord | consensus+info | 0.987 | 0.980 | 0.980` | present | present | `docs/candidate_pool_audit.md` |
| PASS | `text.docs/candidate_budget_audit.md.perspective_gpt41_full | 4 | 1.000 | 1.000` | present | present | `docs/candidate_budget_audit.md` |
| PASS | `text.docs/candidate_budget_audit.md.partial_observability_full | 3 | 1.000 | 1.000` | present | present | `docs/candidate_budget_audit.md` |
| PASS | `text.docs/candidate_role_selection_audit.md.Candidate Role Selection Audit` | present | present | `docs/candidate_role_selection_audit.md` |
| PASS | `text.docs/candidate_role_selection_audit.md.perspective_gpt54_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000` | present | present | `docs/candidate_role_selection_audit.md` |
| PASS | `text.docs/candidate_role_selection_audit.md.perspective_gpt41_no_coord | no_exact_coordinates | consensus+info | 50 | 0.760 | 0.420 | 0.000 | 0.580 | 0.000` | present | present | `docs/candidate_role_selection_audit.md` |
| PASS | `text.docs/candidate_role_selection_audit.md.No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000` | present | present | `docs/candidate_role_selection_audit.md` |
| PASS | `text.docs/random_candidate_baseline.md.Random Candidate Baseline` | present | present | `docs/random_candidate_baseline.md` |
| PASS | `text.docs/random_candidate_baseline.md.perspective_gpt41_full | full | 50 | 4.00 | 0.657 | 0.535 | population | 0.343` | present | present | `docs/random_candidate_baseline.md` |
| PASS | `text.docs/random_candidate_baseline.md.partial_observability_no_coord | no_exact_coordinates | 50 | 3.00 | 0.671 | 0.527 | consensus+info | 0.316` | present | present | `docs/random_candidate_baseline.md` |
| PASS | `text.docs/message_length_audit.md.Message Length Audit` | present | present | `docs/message_length_audit.md` |
| PASS | `text.docs/message_length_audit.md.perspective_gpt41_full | full | population | 50 | 1.000 | 10.22 | 0.098` | present | present | `docs/message_length_audit.md` |
| PASS | `text.docs/message_length_audit.md.partial_observability_no_coord | consensus+info | 50 | 0.380 | [0.280, 0.473] | 5.20` | present | present | `docs/message_length_audit.md` |
| PASS | `text.docs/listener_disagreement_audit.md.partial_observability_full | mirror | 50 | 0.667 | 0.500 | 0.500` | present | present | `docs/listener_disagreement_audit.md` |
| PASS | `text.docs/listener_disagreement_audit.md.partial_observability_no_coord | consensus+info | 50 | 0.987 | 0.980 | 0.020` | present | present | `docs/listener_disagreement_audit.md` |
| PASS | `text.docs/listener_confidence_audit.md.Listener Confidence Audit` | present | present | `docs/listener_confidence_audit.md` |
| PASS | `text.docs/listener_confidence_audit.md.perspective_gpt41_full | mirror | 150 | 0.713 | 0.877 | 0.000 | 0.677 | 0.147 | 0.280` | present | present | `docs/listener_confidence_audit.md` |
| PASS | `text.docs/listener_confidence_audit.md.perspective_gpt41_no_coord | mirror | 150 | 0.580 | 0.835 | 0.000 | 0.771 | 0.280 | 0.480` | present | present | `docs/listener_confidence_audit.md` |
| PASS | `text.docs/listener_confidence_audit.md.partial_observability_no_coord | consensus+info | 150 | 0.987 | 0.889 | 0.000 | 0.000 | 0.000 | 0.000` | present | present | `docs/listener_confidence_audit.md` |
| PASS | `text.docs/failure_taxonomy_audit.md.Failure Taxonomy Audit` | present | present | `docs/failure_taxonomy_audit.md` |
| PASS | `text.docs/failure_taxonomy_audit.md.combined | 152 | 147 | 5 | 0` | present | present | `docs/failure_taxonomy_audit.md` |
| PASS | `text.docs/rule_based_ambiguity_verifier.md.Rule-Based Ambiguity Verifier` | present | present | `docs/rule_based_ambiguity_verifier.md` |
| PASS | `text.docs/rule_based_ambiguity_verifier.md.combined | 152 | 1.000 | 1.000 | 1.000 | 1.000` | present | present | `docs/rule_based_ambiguity_verifier.md` |
| PASS | `text.docs/rule_based_ambiguity_verifier.md.symbolic ambiguity recall is 1.000` | present | present | `docs/rule_based_ambiguity_verifier.md` |
| PASS | `text.docs/interaction_memory_rules.md.Interaction Memory Rule Audit` | present | present | `docs/interaction_memory_rules.md` |
| PASS | `text.docs/interaction_memory_rules.md.Coded failure rows: 152. Unique failure scenes: 76.` | present | present | `docs/interaction_memory_rules.md` |
| PASS | `text.docs/interaction_memory_rules.md.Repair cue satisfies derived rule in 1.000 of failure scenes.` | present | present | `docs/interaction_memory_rules.md` |
| PASS | `text.docs/interaction_memory_rules.md.If exact coordinates are disallowed, prefer the relational/spatial candidate` | present | present | `docs/interaction_memory_rules.md` |
| PASS | `text.docs/qualitative_failure_examples.md.Qualitative Failure Examples` | present | present | `docs/qualitative_failure_examples.md` |
| PASS | `text.docs/qualitative_failure_examples.md.Perspective scene with frame-sensitive relation` | present | present | `docs/qualitative_failure_examples.md` |
| PASS | `text.docs/qualitative_failure_examples.md.No-coordinate repair using consensus+info` | present | present | `docs/qualitative_failure_examples.md` |
| PASS | `text.docs/qualitative_failure_examples.md.0.333 (1/3) | consensus+info | 1.000 (3/3)` | present | present | `docs/qualitative_failure_examples.md` |
| PASS | `text.docs/reviewer_checklist.md.Reviewer Checklist` | present | present | `docs/reviewer_checklist.md` |
| PASS | `text.docs/reviewer_checklist.md.Section 32 of the original workshop plan` | present | present | `docs/reviewer_checklist.md` |
| PASS | `text.docs/reviewer_checklist.md.Items passed: 19/19` | present | present | `docs/reviewer_checklist.md` |
| PASS | `text.docs/reviewer_checklist.md.Held-out listeners are not used for method selection.` | present | present | `docs/reviewer_checklist.md` |
| PASS | `text.docs/reviewer_checklist.md.Claims match actual results.` | present | present | `docs/reviewer_checklist.md` |
| PASS | `text.docs/plan_coverage_audit.md.Plan Coverage Audit` | present | present | `docs/plan_coverage_audit.md` |
| PASS | `text.docs/plan_coverage_audit.md.Overall: 20 covered, 4 partial, 0 open across 24 plan items.` | present | present | `docs/plan_coverage_audit.md` |
| PASS | `text.docs/plan_coverage_audit.md.Core scope: 17 covered, 2 partial, 0 open.` | present | present | `docs/plan_coverage_audit.md` |
| PASS | `text.docs/plan_coverage_audit.md.Stretch scope: 3 covered, 2 partial, 0 open.` | present | present | `docs/plan_coverage_audit.md` |
| PASS | `text.docs/partial_observability_local_check.md.mirror self-play | 0.653 | 1.000 | 0.347` | present | present | `docs/partial_observability_local_check.md` |
| PASS | `text.docs/partial_observability_api50_check.md.Candidate messages referencing private landmarks: 0` | present | present | `docs/partial_observability_api50_check.md` |
| PASS | `text.docs/partial_observability_api50_check.md.no_coord_consensus_info | 0.987` | present | present | `docs/partial_observability_api50_check.md` |
| PASS | `text.docs/partial_observability_api50_check.md.| underspecified_distractor | 50 |` | present | present | `docs/partial_observability_api50_check.md` |
| PASS | `text.docs/partial_observability_api50_check.md.| underspecified_distractor | 59 |` | present | present | `docs/partial_observability_api50_check.md` |
| PASS | `text.docs/paper_claims_iteration_002.md.Consensus+info selector: cross-play `0.920`` | present | present | `docs/paper_claims_iteration_002.md` |
| PASS | `text.paper/main.tex.Partial-observability support check` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.message-length audit rules out a pure verbosity explanation` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.A scene-level overlap audit shows that 20 of 22 alternate-model perspective mirror-failure scenes` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.Across 152 listener-level failures, 147 are underspecified` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.no coded failures are` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.mirror self-play obtains 0.667 cross-play success` | present | present | `paper/main.tex` |
| PASS | `text.paper/main.tex.all 50 full-run mirror failures and all 59 no-coordinate mirror` | present | present | `paper/main.tex` |
| PASS | `text.REPRODUCE.md.--partial 50` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_partial_observability_api.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_api_token_accounting.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.cached Responses API files contain `2,052,279` total tokens` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/run_selected_listener_audit.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_cross_model_listener_audit.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.GPT-5.5 mirror self-play is `0.673`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_cross_model_failure_overlap.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.`20` of `22` GPT-4.1 mirror-failure scenes also fail` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.`26` of `26` GPT-4.1 mirror-failure scenes also fail` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_gpt55_speaker_smoke.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.50-scene speaker audit has GPT-5.5 direct-first `0.993`, mirror self-play `0.853`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/audit_gpt55_followup_plan.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.follow-up experiments covered, `1` partial, and `0` future` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_gpt55_no_coord_k8.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.K=8 no-coordinate prompt produced `0` exact-coordinate candidates` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.population-play improves from `0.833` to `0.993`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/make_human_validation_packet.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.Participant-facing files omit target IDs, condition labels, scene IDs, and held-out success rates.` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_local_benchmark.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.local_benchmark600_check.json` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_local_stronger_plan.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.No-coordinate oracle success rises from `0.808` at K=4 to `0.995` at K=8 over all `1,200` local scenes` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_selection_regret.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.mirror self-play regret is `0.093`, `0.187`, `0.287`, and `0.333`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_candidate_pool.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.robust non-coordinate candidate availability is `0.920`, `0.660`, and `1.000`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_candidate_budget.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.alternate-model perspective robust-scene coverage is `0.380` at `K=1`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_candidate_role_selection.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.no-coordinate consensus+info uses the relational/spatial slot in `0.580`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_random_candidate_baseline.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.population-play beats the uniform-random selector by `0.135`, `0.285`, `0.343`, and `0.247`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_message_length_audit.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.full-candidate population-play messages average `6.82`, `10.22`, `10.22`, and `9.66`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_listener_disagreement.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.full-candidate mirror split-outcome rates are `0.080`, `0.180`, `0.360`, and` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_listener_confidence_audit.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.mirror self-play still produces high-confidence failures in `0.147`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_failure_taxonomy.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.147` of `152` coded listener-level mirror failures are `underspecified_distractor`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_rule_based_ambiguity.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.symbolic ambiguity recall is `1.000`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_interaction_memory_rules.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.`152` coded failure rows collapse into two active rules` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.mean repair success on those failure scenes is `0.991`` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/make_qualitative_examples.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.docs/qualitative_failure_examples.md` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/make_reviewer_checklist.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.docs/reviewer_checklist.md` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/audit_plan_coverage.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.docs/plan_coverage_audit.md` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.core scope has `17` covered, `2` partial, and `0` open items` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.stretch scope has `3` covered, `2` partial, and `0` open items` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.partial_observability_api50_mirror_failures_coded.csv` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/make_artifact_guide.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/analyze_api_listener_leave_one_out.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/audit_submission_readiness.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/export_colm_submission.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/export_protocol_appendix.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/audit_benchmark_integrity.py` | present | present | `REPRODUCE.md` |
| PASS | `text.REPRODUCE.md.scripts/verify_paper_claims.py` | present | present | `REPRODUCE.md` |
| PASS | `text.README.md.paper/colm2026_submission.pdf` | present | present | `README.md` |
| PASS | `text.README.md.docs/api_token_accounting.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/cross_model_listener_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/cross_model_failure_overlap.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/gpt55_speaker_smoke_report.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/gpt55_no_coord_k8_report.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/gpt55_followup_plan_status.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/human_validation_packet.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/rule_based_ambiguity_verifier.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/local_benchmark600_check.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/local_stronger_plan_k8.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/artifact_guide.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/api_listener_leave_one_out.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/selection_regret_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/candidate_pool_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/candidate_budget_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/candidate_role_selection_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/random_candidate_baseline.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/message_length_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/listener_disagreement_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/listener_confidence_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/failure_taxonomy_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/interaction_memory_rules.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/qualitative_failure_examples.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/reviewer_checklist.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/plan_coverage_audit.md` | present | present | `README.md` |
| PASS | `text.README.md.docs/partial_observability_api50_check.md` | present | present | `README.md` |
| PASS | `text.paper/colm2026_submission.tex.\usepackage[submission]{colm2026_conference}` | present | present | `paper/colm2026_submission.tex` |
