# Literature and Positioning Notes

The paper should make a diagnostic evaluation claim rather than a broad claim
about social intelligence.

Core anchors from the plan:

- SOTOPIA evaluates social intelligence in open-ended language-agent role-play.
- SOTOPIA-pi studies interactive learning and notes that evaluator behavior can
  overestimate agents trained for social interaction.
- Zero-shot coordination work gives the closest methodological analogy:
  Other-Play argues that naive self-play can learn specialized conventions that
  fail with novel partners, and Any-Play emphasizes broader inter-algorithm
  cross-play rather than only same-algorithm pairings.
- Pragmatic reference-game work motivates using context and alternatives to
  evaluate whether a message is informative for a listener.
- PRAG-CrossPlay's differentiator is objective target-choice scoring plus an
  explicit same-partner versus held-out-partner split.

Implementation implication:

- Use held-out listeners only for evaluation and oracle analysis.
- Report same-play success and cross-play success separately.
- Avoid claiming "learning" unless an interaction-memory or adaptation stage is
  actually run.
- For the API pilot, make ambiguity resolution conventions explicit in prompt
  variants. This creates a controlled partner-shift stress test rather than
  relying on accidental model quirks.

API note as of the current project setup:

- The original plan mentions GPT-4.1-era pricing. The current official pricing
  page lists nano-class GPT-5.4 models as the cheapest text option exposed there,
  so the scaffold defaults to `gpt-5.4-nano` for tiny pilots.
