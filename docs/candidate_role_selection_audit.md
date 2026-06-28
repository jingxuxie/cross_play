# Candidate Role Selection Audit

This cache-only audit maps each selected message back to its original generated candidate slot.
The role labels are prompt-slot labels, not a learned text classifier.

## Candidate Slot Roles

| Original index | Role | Meaning |
|---:|---|---|
| 0 | natural_first | First natural speaker message |
| 1 | attribute_short | Short attribute-only message |
| 2 | relational_or_spatial | Non-coordinate relational or spatial fallback |
| 3 | coordinate_fallback | Exact row/column fallback, removed in no-coordinate runs |

## Selection Role Distribution

| Run | Filter | Method | Scenes | Success | Natural first | Attribute short | Relational/spatial | Coordinate fallback | Unresolved | Source |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| mixed_50_full | full | mirror | 50 | 0.907 | 0.000 | 0.760 | 0.100 | 0.140 | 0 | `results/hybrid_api_pilot50_allcand_candidates.jsonl` |
| mixed_50_full | full | population | 50 | 1.000 | 0.000 | 0.500 | 0.080 | 0.420 | 0 | `results/hybrid_api_pilot50_allcand_candidates.jsonl` |
| perspective_gpt54_full | full | mirror | 50 | 0.813 | 0.020 | 0.480 | 0.160 | 0.340 | 0 | `results/perspective_stress50_hybrid_candidates.jsonl` |
| perspective_gpt54_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0 | `results/perspective_stress50_hybrid_candidates.jsonl` |
| perspective_gpt41_full | full | mirror | 50 | 0.713 | 0.020 | 0.480 | 0.160 | 0.340 | 0 | `results/perspective_stress50_gpt41nano_audit.jsonl` |
| perspective_gpt41_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0 | `results/perspective_stress50_gpt41nano_audit.jsonl` |
| partial_observability_full | full | mirror | 50 | 0.667 | 0.020 | 0.500 | 0.000 | 0.480 | 0 | `results/partial_observability_api50_candidates.jsonl` |
| partial_observability_full | full | population | 50 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0 | `results/partial_observability_api50_candidates.jsonl` |
| mixed_50_no_coord | no_exact_coordinates | mirror | 50 | 0.787 | 0.040 | 0.860 | 0.100 | 0.000 | 0 | `results/hybrid_api_pilot50_no_coord_audit.jsonl` |
| mixed_50_no_coord | no_exact_coordinates | population | 50 | 0.773 | 0.020 | 0.840 | 0.140 | 0.000 | 0 | `results/hybrid_api_pilot50_no_coord_audit.jsonl` |
| mixed_50_no_coord | no_exact_coordinates | consensus+info | 50 | 0.920 | 0.320 | 0.320 | 0.360 | 0.000 | 0 | `results/hybrid_api_pilot50_no_coord_audit.jsonl` |
| perspective_gpt41_no_coord | no_exact_coordinates | mirror | 50 | 0.580 | 0.300 | 0.480 | 0.220 | 0.000 | 0 | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl` |
| perspective_gpt41_no_coord | no_exact_coordinates | population | 50 | 0.420 | 0.000 | 0.920 | 0.080 | 0.000 | 0 | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl` |
| perspective_gpt41_no_coord | no_exact_coordinates | consensus+info | 50 | 0.760 | 0.420 | 0.000 | 0.580 | 0.000 | 0 | `results/perspective_stress50_gpt41nano_no_coord_audit.jsonl` |
| partial_observability_no_coord | no_exact_coordinates | mirror | 50 | 0.607 | 0.380 | 0.580 | 0.040 | 0.000 | 0 | `results/partial_observability_api50_no_coord_audit.jsonl` |
| partial_observability_no_coord | no_exact_coordinates | population | 50 | 0.727 | 0.500 | 0.400 | 0.100 | 0.000 | 0 | `results/partial_observability_api50_no_coord_audit.jsonl` |
| partial_observability_no_coord | no_exact_coordinates | consensus+info | 50 | 0.987 | 0.540 | 0.000 | 0.460 | 0.000 | 0 | `results/partial_observability_api50_no_coord_audit.jsonl` |

## Mechanism Summary

- Full-candidate mirror often selects the short attribute slot, while full-candidate population shifts toward the coordinate fallback when that fallback is available.
- When exact coordinates are removed, consensus+info sharply reduces short attribute-slot selection; in the harder perspective and partial-observability runs it selects the short attribute slot in 0.000 of scenes.
- The audit is replay-only: it uses existing candidate, no-coordinate audit, and selected-message record files.

Full-candidate mirror attribute-short rates: mixed_50_full=0.760, perspective_gpt54_full=0.480, perspective_gpt41_full=0.480, partial_observability_full=0.500.
Full-candidate population coordinate-fallback rates: mixed_50_full=0.420, perspective_gpt54_full=1.000, perspective_gpt41_full=1.000, partial_observability_full=1.000.
No-coordinate consensus+info relational/spatial rates: mixed_50_no_coord=0.360, perspective_gpt41_no_coord=0.580, partial_observability_no_coord=0.460.
No-coordinate consensus+info attribute-short rates: mixed_50_no_coord=0.320, perspective_gpt41_no_coord=0.000, partial_observability_no_coord=0.000.
