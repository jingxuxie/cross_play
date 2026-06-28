# Additional Experiments Plan for PRAG-CrossPlay

This plan prioritizes a small number of high-value experiments that make the workshop paper more complete without turning it into a large-scale training project. The main goal is to update the paper from the current `gpt-5.4-nano` / `gpt-4.1-nano` evidence to a cleaner story with `gpt-5.5` as a current frontier held-out listener and, if budget allows, as a candidate speaker.

## Guiding principle

Do not spend API budget on broad, redundant reruns. The paper already has a strong diagnostic result: mirror self-play can achieve perfect same-play success while failing under held-out listeners, and population-play can close the gap when listener-invariant candidates are available. The new experiments should answer four reviewer questions:

1. Does the result still hold with a current frontier listener?
2. Does it hold when the frontier model is the speaker rather than only the judge/listener?
3. Does the no-coordinate limitation persist under stronger candidate generation?
4. Are the LLM-listener failures aligned with human or rule-based ambiguity judgments?

## Experiment 1: GPT-5.5 held-out listener audit

**Priority:** highest.

**Question:** Do the current selected messages still show a mirror-vs-population gap when evaluated with `gpt-5.5` listeners?

**Design:** Reuse the existing candidate sets and selected messages. Add three `gpt-5.5` held-out listener prompts to the 50-scene perspective-stress run and the 50-scene partial-observability run. Keep the listener prompts structurally parallel to the existing held-out prompt variants: careful-first, strict-last, and neutral-direct.

**No new speaker calls are required.** This makes the experiment cheap and directly comparable to the existing `gpt-5.4-nano` and `gpt-4.1-nano` audits.

**Report:**

- Cross-play success for direct, shortest, mirror, population, and oracle.
- Paired population-minus-mirror bootstrap interval.
- Listener-disagreement rate for mirror versus population.
- Whether gpt-5.5 fixes ambiguous mirror messages or still chooses distractors.

**Paper value:** This updates the paper's model story and prevents reviewers from dismissing the evidence as an artifact of older model families.

## Experiment 2: Cross-model matrix

**Priority:** high.

**Question:** Is the gap specific to one train/eval pair, or does it appear under model-family shift?

**Design:** Build a compact cross-play matrix using existing generated candidates plus new `gpt-5.5` listener evaluations.

Rows should be the selector or selected-message source:

- direct first candidate
- mirror self-play
- population-play
- consensus+info for no-coordinate settings
- oracle candidate

Columns should be held-out listener families:

- `gpt-4.1-nano`
- `gpt-5.4-nano`
- `gpt-5.5`

Run this on perspective-stress and partial-observability only.

**Report:** A matrix table with cross-play success and a second table with cross-play gaps. Add one sentence: "The same-play metric is unchanged, but held-out listener family changes the observed robustness of mirror-selected messages."

**Paper value:** Makes the cross-play argument clearer: the evaluation unit is not just a model score but robustness across partner distributions.

## Experiment 3: GPT-5.5 speaker candidate-generation audit

**Priority:** medium-high if budget permits.

**Question:** Does a stronger current speaker generate robust candidates earlier, reducing the need for population selection?

**Design:** Regenerate candidates for the 50 perspective-stress scenes with `gpt-5.5`, keeping the same four candidate roles:

1. natural first attempt,
2. concise attribute message,
3. relational/spatial message,
4. explicit fallback.

Evaluate all candidates with the existing held-out listener pool plus the new `gpt-5.5` listeners if budget allows.

**Report:**

- Direct first-candidate success.
- Oracle candidate success.
- Robust-candidate coverage at K=1, K=2, K=3, K=4.
- Mirror and population selected-message success.
- Average message length by candidate role.

**Possible outcomes:**

- If `gpt-5.5` direct messages are much stronger, the paper can say stronger speakers reduce but do not eliminate the need for cross-play evaluation.
- If `gpt-5.5` still produces ambiguous first candidates, the paper has an even stronger claim: frontier candidate generation still benefits from cross-play selection.

## Experiment 4: Stronger no-coordinate candidate generation

**Priority:** high if you want to strengthen the current limitation section.

**Question:** Is the no-coordinate failure mainly caused by weak local selection, limited candidate diversity, or intrinsically hard non-coordinate reference?

**Design:** For the 50 perspective-stress scenes, ask the speaker for K=8 candidates instead of K=4. Forbid exact row/column coordinates in the prompt. Require diversity across these categories:

- contrastive attribute description,
- landmark-relative description,
- ordinal description such as topmost/bottommost/leftmost/rightmost,
- negative contrast such as "not the one near ...",
- listener-frame-safe spatial description,
- concise final fallback without coordinates.

Evaluate the K=8 pool with held-out listeners and rerun mirror, population, informativeness prior, and consensus+info.

**Report:**

- No-coordinate oracle success at K=4 versus K=8.
- Consensus+info success at K=4 versus K=8.
- Population-play success with and without an improved informativeness tie-breaker.
- Robust non-coordinate candidate coverage.

**Paper value:** This transforms the no-coordinate result from a limitation into a diagnostic insight: cross-play reveals when population-play is selecting easy coordinate fallbacks versus genuinely listener-adapted descriptions.

## Experiment 5: Small human validation

**Priority:** medium; high impact if feasible.

**Question:** Do human listeners agree that mirror failures are ambiguous or frame-sensitive?

**Design:** Sample 20 scenes: 10 mirror failures from perspective shift, 5 mirror failures from partial observability, and 5 mirror successes. For each scene, show a human the listener-visible object list and one selected message. Ask them to choose the target object and mark whether the message is ambiguous.

**Minimal setup:** A simple Google Form or local web page is enough. Three annotators per item is sufficient for a workshop-paper sanity check.

**Report:**

- Human choice accuracy for mirror versus population messages.
- Human ambiguity rate for mirror failures versus population repairs.
- A short agreement statistic or percent majority agreement.

**Paper value:** This addresses the obvious reviewer concern that all held-out partners are still LLMs.

## Experiment 6: Rule-based ambiguity verifier

**Priority:** medium; cheap and useful.

**Question:** Can a simple symbolic verifier predict many mirror failures?

**Design:** Implement a verifier that parses color, size, shape, and coordinate mentions from selected messages. For each selected message, count how many listener-visible objects match all explicitly mentioned non-relational attributes. Flag a message as under-specified if more than one object matches.

**Report:**

- Precision/recall of the verifier against the coded failure taxonomy.
- Fraction of mirror failures flagged as under-specified.
- Fraction of population messages flagged as under-specified.

**Paper value:** This reduces dependence on LLM listener behavior and strengthens the claim that many failures are objectively under-informative.

## Recommended final experiment bundle

For the workshop paper, the best cost-quality bundle is:

1. GPT-5.5 held-out listener audit on perspective-stress and partial-observability.
2. Cross-model listener matrix.
3. K=8 no-coordinate candidate-generation audit on perspective-stress.
4. Optional 20-scene human validation if time allows.

This bundle directly improves the paper without changing the core story. The new headline can become:

> Mirror self-play overstates pragmatic robustness across multiple held-out model families, including GPT-5.5; population-play removes the gap when listener-invariant candidates exist, while no-coordinate stress tests reveal when selector design, rather than generation, is the bottleneck.

## Suggested paper edits after running these experiments

Add one new table in the main paper:

**Table: Cross-model held-out listener audit**

| Setting | Held-out listener | Direct | Mirror | Population | Oracle |
|---|---:|---:|---:|---:|---:|
| Perspective stress | gpt-4.1-nano | existing | existing | existing | existing |
| Perspective stress | gpt-5.4-nano | existing | existing | existing | existing |
| Perspective stress | gpt-5.5 | new | new | new | new |
| Partial observability | gpt-5.5 | new | new | new | new |

Add one new no-coordinate table:

| Candidate pool | Oracle | Mirror | Population | Consensus+info |
|---|---:|---:|---:|---:|
| K=4 no-coordinate | existing | existing | existing | existing |
| K=8 no-coordinate | new | new | new | new |

Add one paragraph to the discussion:

> The GPT-5.5 audit updates the model-family evidence but does not change the conceptual conclusion: same-partner communicative success is not enough. The relevant robustness question is whether messages transfer across plausible listener assumptions.

## Budget controls

Use cached candidates wherever possible. Spend new API calls first on listeners, not speakers. Listener calls are cheaper because each prompt is short and structured. Regenerate candidates with `gpt-5.5` only for the 50-scene perspective-stress set unless the listener audit changes the story substantially.

A safe execution order is:

1. Add gpt-5.5 listener evaluations for existing selected messages.
2. Add gpt-5.5 listener evaluations for all existing candidates only if the selected-message audit is interesting.
3. Regenerate K=8 no-coordinate candidates on perspective-stress.
4. Run optional human validation.

## Stopping rule

Stop once you can add two claims:

1. The mirror self-play gap persists under a current frontier held-out listener, or else the paper can explain that stronger listeners repair some ambiguities while the cross-play diagnostic remains necessary.
2. The no-coordinate limitation is better explained by candidate diversity and selector design, not by a lack of any possible non-coordinate referring expression.
