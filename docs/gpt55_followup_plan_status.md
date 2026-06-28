# GPT-5.5 Follow-Up Plan Status

Plan source: `additional_experiments_gpt55_plan.md`.

This generated audit maps the additional GPT-5.5 experiment plan to current artifacts. It is a claim-boundary document: covered rows can support paper claims, partial rows should stay auxiliary, and future rows should not be claimed as completed.

## Summary

Covered: 4. Partial: 2. Future: 0. Missing evidence paths: 0.

| Status | Experiment | Evidence | Interpretation |
|---|---|---|---|
| covered | Experiment 1: GPT-5.5 held-out listener audit | `results/cross_model_listener_audit.json`, `docs/cross_model_listener_audit.md`, `results/gpt55_perspective_selected_records.jsonl`, `results/gpt55_partial_observability_selected_records.jsonl` | Fifty-scene perspective-stress and partial-observability selected-message audits include GPT-5.5 listeners, paired population-minus-mirror gaps, and cross-model context. |
| covered | Experiment 2: cross-model listener matrix | `results/cross_model_listener_audit.json`, `paper/tables/cross_model_listener_audit.tex`, `docs/cross_model_failure_overlap.md` | The artifact has gpt-4.1-nano, gpt-5.4-nano, and gpt-5.5 listener-family rows for perspective stress and partial observability, plus failure-overlap diagnostics. |
| covered | Experiment 3: GPT-5.5 speaker candidate-generation audit | `results/gpt55_speaker_smoke.json`, `docs/gpt55_speaker_smoke_report.md`, `results/gpt55_speaker_perspective10_candidates.jsonl`, `results/gpt55_speaker_perspective20_candidates.jsonl`, `results/gpt55_speaker_perspective20_records.jsonl`, `results/gpt55_speaker_perspective20_candidate_eval_records.jsonl`, `results/gpt55_speaker_perspective50_candidates.jsonl`, `results/gpt55_speaker_perspective50_records.jsonl`, `results/gpt55_speaker_perspective50_candidate_eval_records.jsonl` | The original same-10-scene smoke shows GPT-5.5 speaker direct-first improves from 0.800 to 1.000 and mirror from 0.667 to 0.867, while population stays 1.000. The full 50-scene perspective-stress speaker audit has direct-first 0.993, mirror 0.853 despite same-play 1.000, population 1.000, and oracle 1.000 under GPT-5.5 held-out listeners. |
| partial | Experiment 4: stronger no-coordinate candidate generation | `results/local_stronger_plan_k8.json`, `docs/local_stronger_plan_k8.md`, `docs/candidate_budget_audit.md` | The no-API local K=8 diagnostic supports the candidate-diversity explanation, but the cached API speaker artifacts remain K=4. |
| partial | Experiment 5: small human validation | `data/human_validation_items.jsonl`, `data/human_validation_response_template.csv`, `docs/human_validation_packet.md`, `docs/rule_based_ambiguity_verifier.md`, `results/human_validation_answer_key.json` | The 20-item participant-safe annotation packet and response template are prepared, but no human annotations are present. The current completed independent support remains the rule-based ambiguity verifier. |
| covered | Experiment 6: rule-based ambiguity verifier | `results/rule_based_ambiguity_verifier.json`, `docs/rule_based_ambiguity_verifier.md`, `results/rule_based_ambiguity_verifier_units.jsonl` | The rule-based verifier recovers the coded mirror-failure taxonomy with symbolic ambiguity, attribute-under-specification, and frame-sensitive recall all at 1.000. |

## Claim Boundary

- Safe to claim: the mirror gap persists under GPT-5.5 held-out listeners, and the cross-model matrix supports the core cross-play argument.
- Safe to claim: the 50-scene GPT-5.5 speaker audit shows stronger speakers reduce first-candidate brittleness but do not remove the value of population selection.
- Not yet safe as paper headline: API K=8 no-coordinate generation or human listener validation.

## Next Best Steps

- If API budget allows, run API K=8 no-coordinate candidate generation for the perspective-stress scenes.
- Collect three annotations per item from the prepared 20-scene human validation packet before making human-alignment claims.
- Keep the current K=8 no-coordinate evidence framed as local diagnostic support unless an API K=8 run is added.
