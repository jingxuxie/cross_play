# Interaction Memory Rule Audit

This replay-only audit materializes the workshop plan's interaction-memory idea without making new API calls.
It derives speaker rules from the coded mirror-failure files and checks whether cached repair selectors instantiate the relevant cue on the same failure scenes.

## Failure-Derived Speaker Rules

| Rule ID | Triggering failure category | Speaker rule |
|---|---|---|
| inspect_listener_misparse | `listener_misparse_or_other` | If a message already contains a discriminator but fails, inspect parser/listener behavior before changing the speaker rule. |
| avoid_frame_sensitive_only | `perspective_frame_error` | When speaker and listener perspectives differ, avoid relying only on frame-sensitive left/right language; prefer listener-invariant coordinates or unambiguous visible anchors. |
| avoid_private_landmarks | `private_landmark` | Never refer to landmarks or objects hidden from the listener; use listener-visible discriminators. |
| disambiguate_shared_attributes | `underspecified_distractor` | If a visible distractor shares the target's basic attributes, do not use a bare attribute phrase; add a listener-visible coordinate or spatial relation. |
| add_visible_discriminator | `underspecified_other` | If a message leaves multiple plausible referents, add a visible discriminator. |

## Repair Coverage By Failure Set

| Failure set | Repair selector | Category | Failure rows | Failure scenes | Mirror success on scenes | Repair success on scenes | Repair all-success scenes | Repair cue satisfies rule | Repair coordinate | Repair spatial | Repair short-attribute |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| perspective_full_mirror | population | perspective_frame_error | 5 | 3 | 0.444 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| perspective_full_mirror | population | underspecified_distractor | 38 | 19 | 0.333 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| partial_observability_full_mirror | population | underspecified_distractor | 50 | 25 | 0.333 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| partial_observability_no_coord_mirror | consensus+info | underspecified_distractor | 59 | 29 | 0.322 | 0.977 | 0.966 | 1.000 | 0.000 | 1.000 | 0.000 |

## Combined Summary

Coded failure rows: 152. Unique failure scenes: 76.
Rule counts: avoid_frame_sensitive_only:5, disambiguate_shared_attributes:147.
Mean repair success on failure scenes: 0.991.
Repair all-success scene rate: 0.987.
Repair cue satisfies derived rule in 1.000 of failure scenes.

## Prompt Snippet For A Future Interaction-Memory Run

```text
1. If another visible object shares the target's size/color/shape, add a visible discriminator such as row/column or an unambiguous spatial relation.
2. When speaker and listener perspectives differ, avoid relying only on left/right; prefer listener-invariant coordinates or visible anchors.
3. Use only listener-visible landmarks; never mention hidden or private landmarks.
4. If exact coordinates are disallowed, prefer the relational/spatial candidate over a short attribute-only candidate when both seem locally acceptable.
```

Interpretation: the current paper does not claim a new interaction-memory experiment.
This artifact shows that the coded failures collapse into a small reusable rule set, and that existing population or consensus+info repairs usually instantiate those rules on the same failure scenes.
