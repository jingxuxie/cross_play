# Reviewer Checklist

This generated checklist materializes Section 32 of the original workshop plan against the current artifacts.
Items passed: 19/19.

## Core validity

| Status | Plan item | Evidence | Detail |
|---|---|---|---|
| PASS | Target ID is never shown to the listener. | `docs/protocol_and_prompts.md`, `prag_crossplay/prompts.py` | The hidden target identity is only flagged in the speaker prompt; listener prompts expose candidate IDs only as selectable object labels. |
| PASS | Speaker messages are checked for target ID leakage. | `results/benchmark_integrity_audit.json`, `results/benchmark_integrity_audit.md` | Integrity checks cover generated/evaluated messages, candidate lists, and ablation audit rows for obj_* leakage. |
| PASS | Listener outputs are valid object IDs. | `results/benchmark_integrity_audit.json`, `results/benchmark_integrity_audit.md` | Every result row has a listener choice that is a valid candidate object ID, and success flags are recomputed from choice_id == target_id. |
| PASS | Same test scenes are used across methods. | `results/benchmark_integrity_audit.json`, `results/benchmark_integrity_audit.md` | The integrity audit checks same-scene coverage and balanced rows per scene-method for the paper-facing record files. |
| PASS | Prompts are frozen before final evaluation. | `docs/protocol_and_prompts.md`, `prag_crossplay/prompts.py`, `scripts/export_protocol_appendix.py` | The prompt appendix is generated from the current implementation and records the exact speaker and held-out listener prompts used by the cached artifacts. |
| PASS | Held-out listeners are not used for method selection. | `paper/main.tex`, `prag_crossplay/methods.py`, `prag_crossplay/local_agents.py` | Mirror, population, and consensus+info selection use local training-listener feedback or text priors; held-out API labels are reserved for evaluation and oracle analysis. |
| PASS | All responses are cached. | `data/cached_responses/`, `results/benchmark_integrity_audit.json` | The integrity audit confirms cached response files are present and parse as JSON. |
| PASS | Exact model versions are reported. | `results/benchmark_integrity_audit.json`, `docs/protocol_and_prompts.md`, `paper/main.tex` | The cache audit and paper report exact response model snapshots for both API listener families. |

## Results

| Status | Plan item | Evidence | Detail |
|---|---|---|---|
| PASS | Main table has confidence intervals. | `paper/tables/mixed50.tex`, `paper/main.tex`, `results/paper_claims_verification.json` | The main mixed-results table includes 95% intervals, and paired interval claims are covered by the claim verifier. |
| PASS | Scenario table explains where gains/losses occur. | `paper/tables/mixed50_by_scenario.tex`, `paper/main.tex`, `docs/artifact_guide.md` | The paper localizes the mixed-pilot degradation to perspective-shift scenes and links the scenario table to the artifact guide. |
| PASS | Cross-play gap is reported. | `paper/main.tex`, `paper/tables/mixed50.tex`, `results/paper_claims_verification.json` | The paper defines and reports same-play minus held-out cross-play gaps for the main self-play selectors. |
| PASS | Oracle upper bound is reported. | `paper/main.tex`, `paper/tables/mixed50.tex`, `docs/selection_regret_audit.md` | The paper and audits report oracle candidate success to separate generation failures from selector failures. |
| PASS | Manual failure examples support the quantitative result. | `docs/qualitative_failure_examples.md`, `results/qualitative_failure_examples.json`, `paper/main.tex` | The qualitative appendix and paper examples show mirror-selected messages failing held-out listeners while population or consensus+info repairs succeed. |

## Paper

| Status | Plan item | Evidence | Detail |
|---|---|---|---|
| PASS | Intro states the evaluation blind spot clearly. | `paper/main.tex` | The introduction frames self-play success as a possible blind spot and asks whether selected messages transfer to held-out listeners. |
| PASS | Related work is concise. | `paper/main.tex`, `paper/references.bib`, `results/submission_readiness_audit.json` | The readiness audit confirms the Related Work section exists and the bibliography is populated without inflating the workshop draft past the page target. |
| PASS | Method is reproducible. | `REPRODUCE.md`, `docs/protocol_and_prompts.md`, `scripts/audit_benchmark_integrity.py` | The reproduction file, protocol appendix, and integrity audit expose the command path and protocol surface for the paper-facing artifacts. |
| PASS | Limitations are honest. | `paper/main.tex`, `results/submission_readiness_audit.json` | The limitations section explicitly narrows the claims to small diagnostic API-listener experiments. |
| PASS | Claims match actual results. | `scripts/verify_paper_claims.py`, `results/paper_claims_verification.json`, `results/paper_claims_verification.md` | The claim verifier recomputes numeric and required text claims from checked-in result files. |
| PASS | Appendix includes prompts and schemas. | `docs/protocol_and_prompts.md`, `scripts/export_protocol_appendix.py` | The generated protocol appendix includes prompt text, listener styles, and result/candidate schemas. |
