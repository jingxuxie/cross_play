# Figure 1 Placeholder Specification

## Goal

Figure 1 should let a reviewer understand the paper without reading the methods section. It should visually answer:

> Same-play says the message works with the partner used for selection. Cross-play asks whether that same message works with new listeners.

## Recommended layout

Use a three-panel horizontal figure.

### Panel A: Situated reference game

Draw a small 5x5 grid or clean object-list visualization.

Include:

- Speaker sees the hidden target ID, e.g. `target = obj_1`.
- Listener sees only candidate objects.
- Two objects share attributes, e.g. two small green spheres.
- Speaker and listener have different orientations, e.g. speaker faces north and listener faces east.
- Label the intended object and distractor, but make it visually clear that the listener does not receive the target ID.

Suggested mini example:

- Target: small green sphere at row 4, column 1.
- Distractor: small green sphere at row 1, column 4.
- Mirror-selected message: “It’s a small green sphere.”
- Robust message: “The small green sphere at row 4, column 1.”

### Panel B: Message selection protocol

Show a flow:

1. LLM speaker produces K candidate utterances.
2. Mirror self-play scores candidates with one fixed local listener.
3. Population-play scores candidates with three heterogeneous local listeners.
4. The selected message is sent to held-out listeners.

Use color or line style to distinguish:

- Mirror path: one listener, high same-play, brittle cross-play.
- Population path: multiple listeners, robust cross-play.

Add the phrase:

> Same-play selects; cross-play evaluates.

### Panel C: Headline result

Plot grouped bars for cross-play success.

Minimum bars:

- Perspective stress, GPT-5.5 listener:
  - Mirror: 0.67
  - Population: 1.00
- Partial observability, GPT-5.5 listener:
  - Mirror: 0.65
  - Population: 1.00

Optional secondary annotation:

- “Mirror same-play = 1.00 in both settings”
- “Population-play = 1.00 cross-play across all six listener-family rows”

## Caption idea

“PRAG-CrossPlay evaluates whether messages selected by communicative success with one partner transfer to held-out listeners. Mirror self-play can select fluent but under-informative messages that succeed with the training listener. Population-play selects messages that satisfy multiple listener assumptions and transfers better under cross-play.”

## Plotting notes

- Keep it schematic and clean, not data-heavy.
- Use one memorable example message pair.
- Do not include all audit numbers.
- Make the right panel a tiny headline chart, not a full results table.
- This should be Figure 1 and should appear immediately after the introduction.
