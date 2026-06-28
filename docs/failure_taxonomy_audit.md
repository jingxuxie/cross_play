# Failure Taxonomy Audit

This cache-only audit combines the rubric-coded listener-level mirror failures used in the paper.
The categories come from `scripts/code_failures_with_context.py` and are grounded in the selected message, target object, and chosen distractor.

| Failure set | Rows | Underspecified distractor | Perspective-frame error | Other coded categories | Dominant category |
|---|---:|---:|---:|---:|---|
| Perspective alt-model mirror | 43 | 38 | 5 | 0 | underspecified distractor (0.884) |
| Partial-observability mirror | 50 | 50 | 0 | 0 | underspecified distractor (1.000) |
| Partial no-coordinate mirror | 59 | 59 | 0 | 0 | underspecified distractor (1.000) |

| Combined rows | Rows | Underspecified distractor | Perspective-frame error | Other coded categories |
|---|---:|---:|---:|---:|
| combined | 152 | 147 | 5 | 0 |

Interpretation: the coded mirror failures are overwhelmingly target-distractor ambiguity rather than hidden-information leakage or arbitrary listener mistakes. Across 152 listener-level failures, 147 are underspecified-distractor cases and 5 are perspective-frame errors.
