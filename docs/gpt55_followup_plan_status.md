# GPT-5.5 Follow-Up Plan Status

Plan source: `additional_experiments_gpt55_plan.md`.

This generated audit maps the additional GPT-5.5 experiment plan to current artifacts. It is a claim-boundary document: covered rows can support paper claims, partial rows should stay auxiliary, and future rows should not be claimed as completed.

## Summary

Covered: 5. Partial: 1. Future: 0. Missing evidence paths: 0.

| Status | Experiment | Evidence | Interpretation |
|---|---|---|---|
| covered | Experiment 1: GPT-5.5 held-out listener audit | `results/cross_model_listener_audit.json`, `docs/cross_model_listener_audit.md`, `results/gpt55_perspective_selected_records.jsonl`, `results/gpt55_partial_observability_selected_records.jsonl` | Fifty-scene perspective-stress and partial-observability selected-message audits include GPT-5.5 listeners, paired population-minus-mirror gaps, and cross-model context. |
| covered | Experiment 2: cross-model listener matrix | `results/cross_model_listener_audit.json`, `paper/tables/cross_model_listener_audit.tex`, `docs/cross_model_failure_overlap.md` | The artifact has gpt-4.1-nano, gpt-5.4-nano, and gpt-5.5 listener-family rows for perspective stress and partial observability, plus failure-overlap diagnostics. |
| covered | Experiment 3: GPT-5.5 speaker candidate-generation audit | `results/gpt55_speaker_smoke.json`, `docs/gpt55_speaker_smoke_report.md`, `results/gpt55_speaker_perspective10_candidates.jsonl`, `results/gpt55_speaker_perspective20_candidates.jsonl`, `results/gpt55_speaker_perspective20_records.jsonl`, `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl`, `results/gpt55_speaker_perspective50_candidates.jsonl`, `results/gpt55_speaker_perspective50_records.jsonl`, `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl` | The original same-10-scene smoke shows GPT-5.5 speaker direct-first improves from 0.800 to 1.000 and mirror from 0.667 to 0.867, while population stays 1.000. The full 50-scene perspective-stress speaker audit has direct-first 0.993, mirror 0.853 despite same-play 1.000, population 1.000, and oracle 1.000 under GPT-5.5 held-out listeners. |
| covered | Experiment 4: stronger no-coordinate candidate generation | `results/gpt55_no_coord_k8_comparison.json`, `docs/gpt55_no_coord_k8_report.md`, `results/gpt55_no_coord_k8_perspective50_candidates.jsonl`, `results/gpt55_no_coord_k8_perspective50_candidate_eval_records.jsonl`, `results/gpt55_no_coord_k8_perspective50_no_coord_summary.json`, `results/gpt55_speaker_perspective50_no_coord_summary.json`, `results/local_stronger_plan_k8.json`, `docs/local_stronger_plan_k8.md` | The 50-scene GPT-5.5 K=8 no-coordinate API run produces 400/400 non-coordinate candidates, oracle success 1.000, shortest 1.000, population 0.993, and shows consensus+info is not monotonic because it drops to 0.900. |
| partial | Experiment 5: small human validation | `data/human_validation_items.jsonl`, `data/human_validation_response_template.csv`, `docs/human_validation_packet.md`, `docs/rule_based_ambiguity_verifier.md`, `results/human_validation_answer_key.json` | The 20-item participant-safe annotation packet and response template are prepared, but no human annotations are present. The current completed independent support remains the rule-based ambiguity verifier. |
| covered | Experiment 6: rule-based ambiguity verifier | `results/rule_based_ambiguity_verifier.json`, `docs/rule_based_ambiguity_verifier.md`, `results/rule_based_ambiguity_verifier_units.jsonl` | The rule-based verifier recovers the coded mirror-failure taxonomy with symbolic ambiguity, attribute-under-specification, and frame-sensitive recall all at 1.000. |

## Claim Boundary

- Safe to claim: the mirror gap persists under GPT-5.5 held-out listeners, and the cross-model matrix supports the core cross-play argument.
- Safe to claim: the 50-scene GPT-5.5 speaker audit shows stronger speakers reduce first-candidate brittleness but do not remove the value of population selection.
- Safe to claim: the API K=8 no-coordinate run shows robust non-coordinate expressions are available, while selector design remains the bottleneck.
- Not yet safe as paper headline: human listener validation.

## Next Best Steps

- Use the K=8 no-coordinate result to revise the limitation section: generation is not the bottleneck under GPT-5.5, but consensus+info needs a better tie-breaker.
- Collect three annotations per item from the prepared 20-scene human validation packet before making human-alignment claims.
