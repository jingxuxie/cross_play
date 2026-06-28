# Concrete Workshop Paper Plan

# Do Agents Learn Pragmatics, or Just Their Partner?

**Proposed subtitle:** Cross-Play Evaluation of Communicative Self-Play in Situated Reference Games

**Target venue:** Learning from Situated and Embodied Interaction (LSEI) @ COLM 2026  
**Core theme:** Multi-agent interaction, self-play, communicative success, pragmatic reasoning, and social understanding  
**Constraint:** No local LLM; limited API budget; no large-scale training  
**Best-fit paper type:** 4–8 page workshop paper with a small released benchmark, an API-only experimental protocol, objective interaction success metrics, and strong analysis.

---

## 1. One-sentence thesis

**Communicative self-play can improve apparent pragmatic ability, but unless evaluated under partner shift, it may simply teach an agent to exploit the quirks of its simulated listener; cross-play should be a core evaluation protocol for situated pragmatic language agents.**

---

## 2. Why this can be high-impact despite small compute

The opportunity is not to train a better frontier model. The opportunity is to expose an evaluation blind spot.

Recent interactive social-agent work such as **SOTOPIA-π** argues that social skills can be improved through interaction, but also reports that LLM-based evaluators may overestimate agents trained specifically for social interaction. Your paper can make a sharper, controlled claim: **self-play success is not enough; pragmatic learning must generalize across partners.**

The paper should therefore emphasize:

1. **Objective communicative success**, not only LLM-as-judge scores.
2. **Partner shift / cross-play**, not only same-agent self-play.
3. **Small, reproducible interaction environments**, not large-scale training.
4. **Failure analysis**, showing when self-play creates brittle private conventions.

This is exactly the kind of focused insight that can work well for a workshop: simple setup, strong conceptual point, useful protocol, and reusable artifacts.

---

## 3. Recommended paper title options

Pick one:

1. **Do Agents Learn Pragmatics, or Just Their Partner? Cross-Play Evaluation of Communicative Self-Play**
2. **Cross-Play Matters: Diagnosing Partner Overfitting in LLM Pragmatic Communication**
3. **When Self-Play Speaks to Itself: Partner Overfitting in Situated Reference Games**
4. **Communicative Success Is Not Enough: Cross-Partner Evaluation for Pragmatic Language Agents**

My strongest recommendation is option 1.

---

## 4. Abstract draft

> Language agents are increasingly trained or adapted through interaction, but interactive success can conflate robust pragmatic competence with overfitting to a particular partner. We study this issue in a controlled situated reference game where a speaker observes a target object in a scene and must produce a natural-language message that enables a listener to identify the target. Because listener choices are automatically scored against ground truth, the environment provides an objective communicative-success signal without relying on LLM judges. We compare direct generation, mirror self-play selection, and population-play selection, then evaluate each speaker under cross-play with held-out listener prompts and models. We find that same-partner self-play can inflate apparent pragmatic performance while failing to generalize under partner shift, especially in relational and perspective-sensitive scenarios. Population-play reduces this overfitting by selecting messages that are robust across heterogeneous listeners. Our results suggest that cross-play should be a standard evaluation axis for language agents that learn from situated interaction.

Do not claim the empirical finding until you actually run the experiments. If results differ, adjust the abstract to match.

---

## 5. Main research questions

### RQ1: Does mirror self-play improve same-partner communicative success?

Compare direct speaker generation against a speaker that generates multiple candidate messages and selects the one that succeeds with a simulated listener from the same model/prompt family.

### RQ2: Does mirror self-play generalize under partner shift?

Evaluate the selected messages with held-out listeners that differ by prompt, decoding, and ideally model family.

### RQ3: Does population-play reduce partner overfitting?

Select candidate messages by average success across a small population of heterogeneous training listeners, then evaluate with unseen listeners.

### RQ4: Where does overfitting occur?

Analyze by scenario type: attribute-only, distractor contrast, relational reference, perspective shift, and partial observability.

---

## 6. Hypotheses

### H1: Mirror self-play increases same-listener success.

A candidate message selected against Listener A will be more likely to work for Listener A than a direct one-shot message.

### H2: Mirror self-play has a larger cross-play gap.

Mirror self-play will look better under same-listener evaluation than under held-out-listener evaluation.

Define:

```text
cross_play_gap = same_listener_success - heldout_listener_success
```

A large positive gap suggests partner overfitting.

### H3: Population-play reduces the cross-play gap.

Selecting messages that work across several training listeners should improve held-out listener success and reduce listener-specific brittleness.

### H4: Partner overfitting is strongest in genuinely pragmatic cases.

The gap should be larger in scenes requiring contrastive, relational, or perspective-sensitive language than in scenes where the target is uniquely identifiable by a simple attribute.

---

## 7. Core contribution package

Aim for these three contributions:

### Contribution 1: PRAG-CrossPlay benchmark

A small procedural situated reference-game environment with objective scoring.

Deliverables:

- scene generator;
- JSONL dataset;
- prompt templates;
- cached API outputs;
- evaluation scripts;
- paper figures and tables.

### Contribution 2: Cross-play evaluation protocol

A simple protocol that separates:

- **same-play success**: speaker evaluated by the listener used for self-play selection;
- **cross-play success**: speaker evaluated by held-out listeners;
- **generalization gap**: difference between same-play and cross-play success.

### Contribution 3: Empirical diagnosis of partner overfitting

Show whether self-play improves robust pragmatics or merely adapts to the quirks of the training listener.

---

## 8. Task design: situated reference game

### 8.1 Environment overview

Each episode contains:

- a small scene with objects;
- a target object visible to the speaker;
- a listener view without the target label;
- a speaker message;
- a listener object choice;
- automatic success/failure scoring.

The listener must choose the target object from a list of candidate objects.

The speaker may describe the target using object attributes, spatial relations, and perspective-aware references, but must not mention the hidden target ID.

### 8.2 Example episode

```json
{
  "scene_id": "rr_0042",
  "scenario_type": "relational_reference",
  "speaker_view": {
    "target_id": "obj_3",
    "objects": [
      {"id": "obj_1", "color": "red", "shape": "cube", "size": "small", "x": 1, "y": 2},
      {"id": "obj_2", "color": "blue", "shape": "sphere", "size": "large", "x": 3, "y": 2},
      {"id": "obj_3", "color": "red", "shape": "cube", "size": "large", "x": 2, "y": 2},
      {"id": "obj_4", "color": "green", "shape": "cylinder", "size": "small", "x": 2, "y": 4}
    ]
  },
  "listener_view": {
    "objects": [
      {"id": "obj_1", "description": "small red cube at row 2, column 1"},
      {"id": "obj_2", "description": "large blue sphere at row 2, column 3"},
      {"id": "obj_3", "description": "large red cube at row 2, column 2"},
      {"id": "obj_4", "description": "small green cylinder at row 4, column 2"}
    ]
  },
  "valid_target_id": "obj_3"
}
```

Good speaker message:

> Select the large red cube between the small red cube and the blue sphere.

Bad speaker message:

> Select the red cube.

The bad message is semantically true but pragmatically under-informative because there are two red cubes.

---

## 9. Scenario types

Use five scenario families. Start with the first four for the minimum viable paper.

### Type A: Unique attribute

The target is uniquely identifiable by one or two attributes.

Example:

> Select the yellow triangle.

Purpose: sanity check. Most methods should succeed.

### Type B: Distractor contrast

The target shares its most salient attribute with a distractor, so the speaker must mention the distinguishing feature.

Example:

Scene has two red cubes: one small and one large.

Good:

> Select the large red cube.

Bad:

> Select the red cube.

Purpose: tests contrastive pragmatics.

### Type C: Relational reference

The target is best identified by relation to landmarks.

Example:

> Select the red cube immediately left of the blue sphere.

Purpose: tests spatial grounding and pragmatic informativeness.

### Type D: Perspective shift

The speaker and listener have different orientations. The speaker must adapt to the listener’s frame of reference or use perspective-invariant language.

Example:

Bad:

> Select the cube on the left.

Better:

> Select the cube closer to the door.

Purpose: tests situated social reasoning: what does the listener know and how will they interpret the message?

### Type E: Partial observability / private landmark

Some landmarks visible to the speaker are not visible to the listener. The speaker must avoid referring to inaccessible information.

Example:

Bad:

> Select the cube next to the hidden star.

Better:

> Select the large red cube in the top row.

Purpose: tests listener-perspective modeling.

This is a good stretch condition. Add it after the first four are working.

---

## 10. Dataset size

### Minimum viable workshop version

Use:

```text
600 total test episodes
150 unique-attribute
150 distractor-contrast
150 relational-reference
150 perspective-shift
```

Add:

```text
200 development episodes
```

for debugging prompts and tuning the scenario generator.

### Stronger version

Use:

```text
1,000 test episodes
250 unique-attribute
250 distractor-contrast
250 relational-reference
250 perspective-shift
```

Add:

```text
200 partial-observability stress episodes
```

### Why not bigger?

A clean 600–1,000 episode benchmark with objective scoring and careful cross-play analysis is enough for a workshop paper. Bigger is less important than reproducibility and diagnostic clarity.

---

## 11. Agent setup without local LLMs

You can run the entire project through APIs.

Use three roles:

1. **Speaker model**: generates candidate messages.
2. **Training listeners**: used to select messages during self-play/population-play.
3. **Held-out listeners**: used only for final cross-play evaluation.

### 11.1 Minimal model plan

If you only have one provider, create listener diversity through prompts and decoding:

| Listener | Role | Model | Prompt style | Used for selection? | Used for final test? |
|---|---|---:|---|---:|---:|
| L_train_literal | literal listener | cheap model | direct matching | yes | no |
| L_train_careful | careful listener | cheap model | silent reasoning, final JSON | yes | no |
| L_train_uncertain | ambiguity-aware listener | cheap model | can report low confidence | yes | no |
| L_test_direct | held-out listener | cheap or mid model | different direct prompt | no | yes |
| L_test_careful | held-out listener | mid model | different careful prompt | no | yes |
| L_test_strict | held-out listener | mid or strong model | strict instruction following | no | yes |

### 11.2 Better model plan

If your API account gives access to multiple model sizes:

- use the cheapest capable model for bulk candidate generation and training listeners;
- use a slightly stronger model for held-out cross-play listeners;
- use a strong model only for a small audit of 50–100 examples.

Do not use expensive models for all episodes.

### 11.3 Important reproducibility rule

Always log:

```json
{
  "model": "model-name",
  "api_provider": "provider-name",
  "temperature": 0.0,
  "prompt_hash": "...",
  "scene_id": "...",
  "timestamp": "...",
  "input_tokens": 123,
  "output_tokens": 20,
  "raw_response": "..."
}
```

Cache every response. The paper should be reproducible from cached outputs without spending money again.

---

## 12. Methods to compare

### Method 0: Template baseline

A deterministic template describes the target with all attributes.

Example:

> Select the large red cube at row 2, column 2.

Purpose:

- checks environment validity;
- gives a non-LLM baseline;
- prevents reviewers from saying LLMs are unnecessary.

Expected behavior:

- high success in simple coordinate scenes;
- less natural language;
- may fail perspective/partial-observability if template uses speaker-centric references.

### Method 1: Direct speaker

The speaker sees the scene and target, then outputs one message.

```text
scene -> speaker -> message -> held-out listeners -> success
```

This is your main baseline.

### Method 2: Best-of-K without self-play

The speaker generates K candidate messages. Select the shortest valid candidate or the first candidate.

```text
scene -> speaker generates K messages -> heuristic selector -> held-out listeners
```

Purpose:

- distinguishes gains from “more samples” versus gains from communicative self-play.

### Method 3: Mirror self-play selection

The speaker generates K messages. A training listener from the same model/prompt family interprets each candidate. Select the candidate that makes the training listener choose the correct target.

```text
scene -> K messages -> same-family listener scores each -> select best -> held-out listeners
```

Score:

```text
score(candidate) = 1[training_listener_choice == target] - lambda * token_count
```

Use a tiny length penalty such as:

```text
lambda = 0.001
```

Purpose:

- tests whether same-partner self-play improves apparent pragmatic communication;
- likely exposes partner overfitting.

### Method 4: Population-play selection

The speaker generates K messages. Several heterogeneous training listeners interpret each candidate. Select the candidate with the highest average success.

```text
score(candidate) = mean_j 1[listener_j_choice == target] - lambda * token_count
```

Purpose:

- tests whether listener diversity improves robust pragmatics;
- likely your strongest method.

### Method 5: Population-play + interaction memory

This is a stretch method if you have time.

Procedure:

1. Run population-play on 200 development scenes.
2. Collect failures.
3. Ask a cheap model or yourself to summarize failure patterns into 5–10 general communication rules.
4. Add those rules to the speaker prompt.
5. Re-run direct and population-play on the test set.

Example learned rules:

- mention the distinguishing attribute when multiple objects share a color or shape;
- avoid left/right when listener orientation differs;
- prefer stable landmarks visible to the listener;
- do not mention object IDs;
- keep messages short but not underspecified.

This makes the paper more explicitly about **learning from interaction** rather than only test-time selection.

### Method 6: Oracle candidate upper bound

This is an analysis-only method.

For each scene, ask:

> Did any of the K generated candidates succeed under held-out listeners?

This tells you whether failures are caused by generation or selection.

Define:

```text
oracle_crossplay_success = 1 if any candidate succeeds with held-out listeners
selection_regret = oracle_crossplay_success - method_crossplay_success
```

This is very useful for paper analysis.

---

## 13. Speaker prompt template

Use structured output. Keep the prompt stable and versioned.

```text
SYSTEM:
You are the SPEAKER in a situated reference game. Your goal is to write a short natural-language message that enables a listener to identify the target object.

Rules:
- Do not mention the hidden target ID.
- Use only information available in the listener view.
- Be concise but sufficiently informative.
- If there are distractors, include the property or relation that distinguishes the target.
- If speaker and listener perspectives differ, prefer perspective-invariant descriptions.
- Return valid JSON only.

USER:
Scene:
{scene_json}

Target object ID visible only to you: {target_id}

Generate {K} different messages. Each message should be natural and at most 25 words.

Return:
{"utterances": ["...", "...", "..."]}
```

Use:

```text
K = 4 for the minimum paper
K = 8 for the stronger paper
```

---

## 14. Listener prompt templates

### 14.1 Direct listener

```text
SYSTEM:
You are the LISTENER in a reference game. You see a scene and a speaker message. Choose the object that the speaker most likely intends. Return JSON only.

USER:
Listener view:
{listener_view_json}

Speaker message:
"{utterance}"

Choose one object ID from the listener view.

Return:
{"choice_id": "obj_...", "confidence": 0.0_to_1.0}
```

### 14.2 Careful listener

```text
SYSTEM:
You are a careful listener. Privately consider all candidates, but do not reveal your reasoning. Return JSON only.

USER:
Listener view:
{listener_view_json}

Speaker message:
"{utterance}"

Choose the most likely target object. If the message is ambiguous, still choose the most likely object and set confidence below 0.5.

Return:
{"choice_id": "obj_...", "confidence": 0.0_to_1.0, "ambiguity": true_or_false}
```

### 14.3 Strict listener

```text
SYSTEM:
You are a strict instruction-following listener. You must choose the object best supported by the speaker message and the listener-visible scene. Do not use hidden information. Return JSON only.

USER:
Listener view:
{listener_view_json}

Speaker message:
"{utterance}"

Return:
{"choice_id": "obj_...", "confidence": 0.0_to_1.0, "reason_code": "attribute|relation|position|ambiguous|other"}
```

Use direct, careful, and strict prompts to create partner diversity even if you use the same API model.

---

## 15. Scoring

### 15.1 Main success metric

For each listener:

```text
success = 1[choice_id == target_id]
```

For a set of held-out listeners:

```text
crossplay_success = mean(success over held-out listeners and scenes)
```

### 15.2 Same-play success

For self-play methods:

```text
sameplay_success = mean(success with the training listener used for selection)
```

### 15.3 Cross-play gap

```text
crossplay_gap = sameplay_success - crossplay_success
```

A larger gap suggests more partner-specific adaptation.

### 15.4 Robustness across partners

Compute listener variance:

```text
listener_variance = variance(success across held-out listeners)
```

Lower variance means the message is less partner-specific.

### 15.5 Efficiency

```text
mean_tokens = average number of tokens in speaker message
```

Report success both raw and length-normalized.

### 15.6 Ambiguity proxy

Use the careful listener’s ambiguity field or low confidence:

```text
ambiguous = confidence < 0.5 or ambiguity == true
```

This is not the main metric, but useful for analysis.

### 15.7 Error categories

Hand-label 100 failures into categories:

| Error category | Description |
|---|---|
| underspecified | message does not distinguish target from distractors |
| wrong attribute | message states false target property |
| wrong relation | spatial relation is incorrect |
| perspective error | left/right or viewpoint mismatch |
| private landmark | references information unavailable to listener |
| listener misparse | message seems good but listener chooses incorrectly |
| idiosyncratic convention | message works for one listener but not others |

This qualitative analysis will make the paper much stronger.

---

## 16. Statistical analysis

Use paired comparisons by scene.

### 16.1 Confidence intervals

Bootstrap scenes with replacement and report 95% confidence intervals for:

- same-play success;
- cross-play success;
- cross-play gap;
- scenario-type success.

### 16.2 Significance tests

Use paired bootstrap or McNemar-style tests for method comparisons on the same scenes.

Recommended comparisons:

1. Direct speaker vs mirror self-play on same-play success.
2. Direct speaker vs mirror self-play on cross-play success.
3. Mirror self-play vs population-play on cross-play success.
4. Mirror self-play vs population-play on cross-play gap.

### 16.3 Do not overclaim

For a workshop paper, confidence intervals plus paired bootstrap tests are enough. Avoid presenting tiny p-values as the main contribution.

---

## 17. Experimental matrix

Minimum viable matrix:

| Method | K candidates | Training listeners | Held-out listeners | Purpose |
|---|---:|---:|---:|---|
| Template | 1 | none | 3 | non-LLM baseline |
| Direct | 1 | none | 3 | main LLM baseline |
| Best-of-K heuristic | 4 | none | 3 | controls for sampling |
| Mirror self-play | 4 | 1 | 3 | tests partner overfitting |
| Population-play | 4 | 3 | 3 | tests robust selection |
| Oracle upper bound | 4 | held-out analysis only | 3 | generation vs selection bottleneck |

Stronger matrix:

| Extra method | Why include it |
|---|---|
| K=8 population-play | tests whether more candidate diversity helps |
| interaction memory | shows learning from failures |
| partial-observability stress test | stronger situated/social reasoning claim |
| small human/self audit | validates that cross-play failures reflect real ambiguity |

---

## 18. API budget plan

The project is feasible with limited API credit if you keep messages short and cache everything.

### 18.1 Example token budget

Assume:

```text
N = 800 scenes
K = 4 candidate messages per scene
training listeners = 3
held-out listeners = 3
speaker generation call = ~500 input tokens + ~160 output tokens
listener call = ~350 input tokens + ~25 output tokens
```

Approximate calls:

```text
speaker calls = 800
listener calls = 800 * 4 * (3 training + 3 held-out) = 19,200
```

Approximate tokens:

```text
speaker input = 0.40M tokens
speaker output = 0.13M tokens
listener input = 6.72M tokens
listener output = 0.48M tokens
```

This is not a large API workload for small/cheap text models.

### 18.2 Cost-control rules

1. Start with 50 scenes before scaling.
2. Use temperature 0 for listeners to reduce repeats.
3. Cache all calls by prompt hash.
4. Use batch processing if available and if timing allows.
5. Do not use expensive reasoning models for bulk listener calls.
6. Use a stronger model only for 50–100 audit cases.
7. Run K=4 first. Increase to K=8 only if the K=4 results are unclear.

### 18.3 Example API model choices

If using OpenAI models, the GPT-4.1 launch page listed prices per 1M tokens for GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano, with nano and mini far cheaper than the full model and Batch API discounted by 50%. Verify current prices in your dashboard before running the full experiment.

Recommended pattern:

```text
bulk speaker/listener: cheapest capable model
held-out listener: cheap or mid model with different prompt
small audit: stronger model, 50–100 cases only
```

---

## 19. Implementation plan

### 19.1 Repository structure

```text
prag_crossplay/
  README.md
  requirements.txt
  configs/
    models.yaml
    prompts.yaml
    experiment_minimal.yaml
  data/
    dev_scenes.jsonl
    test_scenes.jsonl
    cached_responses/
  prag_crossplay/
    env/
      objects.py
      scene_generator.py
      validators.py
    agents/
      api_client.py
      speaker.py
      listener.py
    methods/
      template.py
      direct.py
      best_of_k.py
      mirror_selfplay.py
      population_play.py
      oracle.py
    eval/
      scoring.py
      bootstrap.py
      error_analysis.py
    viz/
      make_tables.py
      make_figures.py
  scripts/
    generate_scenes.py
    run_pilot.py
    run_generation.py
    run_selection.py
    run_crossplay_eval.py
    analyze_results.py
  paper/
    main.tex
    figures/
    tables/
```

### 19.2 Scene schema

Use JSONL, one scene per line.

```json
{
  "scene_id": "dc_000001",
  "split": "test",
  "scenario_type": "distractor_contrast",
  "target_id": "obj_3",
  "speaker_orientation": "north",
  "listener_orientation": "east",
  "objects": [
    {
      "id": "obj_1",
      "color": "red",
      "shape": "cube",
      "size": "small",
      "x": 1,
      "y": 2,
      "visible_to_listener": true
    }
  ],
  "speaker_view_text": "...",
  "listener_view_text": "...",
  "gold_minimal_description": "large red cube"
}
```

The `gold_minimal_description` is for analysis only, not shown to LLMs unless you use it for the template baseline.

### 19.3 Scene generator pseudocode

```python
def generate_scene(scenario_type, seed):
    rng = Random(seed)
    objects = sample_objects(rng)
    target = choose_target(objects, scenario_type, rng)
    objects = enforce_difficulty(objects, target, scenario_type, rng)
    speaker_view = render_speaker_view(objects, target)
    listener_view = render_listener_view(objects, scenario_type)
    validate_unique_target_possible(listener_view, target)
    return scene
```

Validation matters. Make sure a human could identify the target from a good message.

### 19.4 API caching key

Use a hash of:

```text
model name + temperature + system prompt + user prompt + schema version
```

Never pay twice for the same request.

---

## 20. Pilot experiment

Before running the full matrix, run 50 scenes:

```text
10 unique-attribute
15 distractor-contrast
15 relational-reference
10 perspective-shift
```

Check:

- JSON validity rate;
- whether the listener chooses valid IDs;
- direct baseline success;
- whether scenes are too easy or too hard;
- whether perspective-shift examples actually require perspective reasoning;
- whether any prompt accidentally leaks the target ID.

### Pilot success criteria

Proceed to full experiment only if:

```text
JSON validity > 95%
template baseline success > 85%
direct speaker success between 50% and 90%
```

If direct speaker success is above 95%, make scenes harder.

If direct speaker success is below 40%, simplify scene rendering or improve prompts.

---

## 21. Main experiment run order

Run in this order:

1. Generate dev and test scenes.
2. Run template baseline.
3. Run direct speaker on test scenes.
4. Generate K=4 candidate messages for each test scene.
5. Score candidates with training listeners.
6. Select mirror-self-play messages.
7. Select population-play messages.
8. Evaluate selected messages with held-out listeners.
9. Compute oracle candidate upper bound.
10. Bootstrap confidence intervals.
11. Sample 100 failure cases for manual error analysis.
12. Make figures and tables.

This order avoids wasting API calls before confirming the environment works.

---

## 22. Expected tables and figures

### Figure 1: Task diagram

Show one scene, the speaker view, the listener view, a candidate message, and listener choice.

### Figure 2: Same-play vs cross-play protocol

A two-panel diagram:

- mirror self-play: speaker optimized against one listener;
- cross-play: same message evaluated by held-out listeners.

### Table 1: Main results

| Method | Same-play success | Cross-play success | Cross-play gap | Mean tokens |
|---|---:|---:|---:|---:|
| Template | — | TBD | — | TBD |
| Direct | — | TBD | — | TBD |
| Best-of-K heuristic | — | TBD | — | TBD |
| Mirror self-play | TBD | TBD | TBD | TBD |
| Population-play | TBD | TBD | TBD | TBD |
| Oracle upper bound | — | TBD | — | TBD |

### Table 2: Results by scenario type

| Method | Unique | Contrast | Relational | Perspective | Overall |
|---|---:|---:|---:|---:|---:|
| Direct | TBD | TBD | TBD | TBD | TBD |
| Mirror self-play | TBD | TBD | TBD | TBD | TBD |
| Population-play | TBD | TBD | TBD | TBD | TBD |

### Figure 3: Partner-overfitting gap

Bar plot of:

```text
same-play success - cross-play success
```

for mirror self-play and population-play.

### Figure 4: Selection regret

Compare each method to the oracle candidate upper bound.

### Table 3: Manual failure analysis

| Error type | Direct | Mirror self-play | Population-play |
|---|---:|---:|---:|
| underspecified | TBD | TBD | TBD |
| perspective error | TBD | TBD | TBD |
| private landmark | TBD | TBD | TBD |
| listener misparse | TBD | TBD | TBD |
| idiosyncratic convention | TBD | TBD | TBD |

---

## 23. Result patterns and how to write them

### Pattern A: Mirror self-play improves same-play but hurts cross-play

This is the cleanest version of the paper.

Main claim:

> Self-play can create partner-specific communicative conventions that inflate apparent pragmatic success. Cross-play reveals the gap.

### Pattern B: Population-play beats mirror self-play under cross-play

This is the ideal positive result.

Main claim:

> Listener diversity is a cheap antidote to partner overfitting.

### Pattern C: Direct and mirror self-play are similar

Still publishable if you analyze why.

Possible interpretation:

> Current instruction-tuned models already produce fairly partner-robust pragmatic descriptions in simple reference games; self-play selection helps only in hard scenario types.

Then emphasize scenario-level analysis.

### Pattern D: All methods are near ceiling

Make the benchmark harder:

- add more distractors;
- add perspective shift;
- remove coordinates;
- add partial observability;
- penalize overlong descriptions;
- require listener-visible-only references.

### Pattern E: All methods are poor

Simplify:

- reduce number of objects;
- remove perspective shift for the main experiment;
- improve rendering clarity;
- use structured scene descriptions;
- include one demonstration in the prompt.

---

## 24. Four-day fast-track plan

This assumes the submission deadline is very close. If you have more time, use the longer plan in the next section.

### Day 1: Build and pilot

Deliverables:

- scene generator for four scenario types;
- JSON schema;
- speaker/listener prompts;
- 50-scene pilot;
- initial success-rate sanity check.

Decision point:

- if direct baseline is too high, add distractors and perspective cases;
- if too low, simplify rendering.

### Day 2: Main runs

Deliverables:

- 600 test scenes;
- direct baseline;
- K=4 candidate generations;
- training-listener scores;
- mirror and population selections;
- held-out cross-play evaluation.

Keep everything cached.

### Day 3: Analysis and figures

Deliverables:

- Table 1 main results;
- Table 2 scenario results;
- Figure 1 task diagram;
- Figure 2 protocol diagram;
- Figure 3 cross-play gap;
- manual analysis of 50–100 failures.

### Day 4: Write and polish

Deliverables:

- 4–8 page paper draft;
- abstract and intro finalized;
- limitations section;
- reproducibility checklist;
- appendix with prompts;
- README for artifacts.

---

## 25. Two-week stronger plan

### Days 1–2: Literature and environment

- finalize task design;
- build generator;
- validate scene difficulty;
- write related-work bullets.

### Days 3–4: Pilot and prompt stabilization

- run 100-scene pilot;
- fix invalid JSON and scene ambiguity;
- freeze prompts and seeds.

### Days 5–6: Main experiments

- run 1,000 scenes;
- K=4 and K=8 candidate generation;
- run listener population and held-out listeners.

### Days 7–8: Interaction memory extension

- collect development failures;
- distill rules;
- rerun direct and population-play with memory prompt.

### Days 9–10: Analysis

- bootstrap CIs;
- make figures;
- manual error coding;
- compute oracle upper bound and selection regret.

### Days 11–12: Writing

- full paper draft;
- related work;
- methods;
- results.

### Days 13–14: Polish

- tighten claims;
- release code/data;
- add appendix;
- proofread.

---

## 26. Paper outline for a 4–8 page workshop submission

### 1. Introduction

Key points:

- Pragmatic language use is interactive and partner-dependent.
- Self-play and simulated interaction are attractive because they provide cheap learning signals.
- But same-partner success can overestimate robust pragmatic competence.
- This paper proposes cross-play as a diagnostic protocol.

End the intro with contributions.

### 2. Related work

Cover briefly:

- situated and embodied interaction;
- reference games and pragmatic communication;
- social-agent evaluation such as SOTOPIA;
- interactive learning and self-play for language agents;
- limitations of LLM-as-judge evaluation.

Keep this short. The paper should be methods/results-heavy.

### 3. PRAG-CrossPlay task

Describe:

- scene generation;
- speaker/listener roles;
- scenario types;
- objective scoring;
- why this is situated and pragmatic.

### 4. Methods

Describe:

- direct speaker;
- best-of-K heuristic;
- mirror self-play selection;
- population-play selection;
- oracle upper bound.

### 5. Experiments

Describe:

- dataset size;
- API models and prompt variants;
- held-out listener protocol;
- metrics;
- statistical tests.

### 6. Results

Present:

- main table;
- scenario table;
- cross-play gap figure;
- oracle/regret analysis.

### 7. Qualitative analysis

Show 3–5 examples:

- mirror self-play message that works for training listener but fails held-out listeners;
- population-play message that is more robust;
- perspective-shift failure;
- underspecification failure.

### 8. Limitations and conclusion

Limitations:

- text-only grid scenes are simplified;
- listeners are LLMs rather than humans;
- prompt/model diversity is an imperfect proxy for human partner diversity;
- no weight training;
- small API-scale experiment.

Conclusion:

- cross-play should be standard for evaluating interactive pragmatic learning;
- population-based communicative selection is a cheap robustification method.

---

## 27. Related-work anchors

Use these as the core citations.

### LSEI workshop

The workshop call explicitly includes multi-agent interaction, self-play, communicative success, pragmatic reasoning, and social understanding as a relevant topic.

Reference:

- Learning from Situated and Embodied Interaction @ COLM 2026: https://learning-situated-interaction.github.io/
- OpenReview venue page: https://openreview.net/group?id=colmweb.org%2FCOLM%2F2026%2FWorkshop%2FLSEI

### SOTOPIA

SOTOPIA introduced an open-ended environment for evaluating social intelligence in language agents through role-play scenarios involving social goals, coordination, collaboration, exchange, and competition.

Reference:

- Zhou et al. 2024. SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents. https://arxiv.org/abs/2310.11667

### SOTOPIA-π

SOTOPIA-π studies interactive learning of socially intelligent language agents and reports that LLM evaluators can overestimate agents trained specifically for social interaction.

Reference:

- Wang et al. 2024. SOTOPIA-π: Interactive Learning of Socially Intelligent Language Agents. https://aclanthology.org/2024.acl-long.698/

### Pragmatic reference games

Reference games are a clean formalization of pragmatic communication because the speaker must choose an utterance that identifies a target for a listener given context and alternatives.

Reference:

- Hu, Levy, and Zaslavsky. 2021. Scalable pragmatic communication via self-supervision. https://arxiv.org/abs/2108.05799

### Clarification / ambiguity benchmarks

Useful if you add an “ask clarification” extension or discuss ambiguity.

Reference:

- Zhang et al. 2024. CLAMBER: A Benchmark of Identifying and Clarifying Ambiguous Information Needs in Large Language Models. https://arxiv.org/abs/2405.12063

### Pragmatic competence benchmarks

Useful for positioning against static pragmatic evaluation.

Reference:

- AltPrag: https://arxiv.org/html/2505.18497

### API pricing

Use current provider dashboard for final cost reporting. As a public reference, OpenAI’s GPT-4.1 launch page listed GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano prices per 1M tokens and a 50% Batch API discount for those models.

Reference:

- OpenAI GPT-4.1 API announcement: https://openai.com/index/gpt-4-1/

---

## 28. Differentiation from prior work

### Compared with SOTOPIA

SOTOPIA is broad and realistic. Your task is narrow and diagnostic.

Your advantage:

- automatic ground-truth scoring;
- controlled distractors and perspective shifts;
- explicit same-play vs cross-play comparison;
- cheap reproducibility.

### Compared with SOTOPIA-π

SOTOPIA-π studies interactive learning and social intelligence training. Your work studies whether interaction-derived success generalizes across partners.

Your advantage:

- focuses directly on evaluator/partner overfitting;
- avoids using LLM judge scores as the main metric;
- requires no large-scale training.

### Compared with classic reference-game pragmatics

Classic reference games study pragmatic utterance choice. Your work connects reference games to modern LLM self-play and cross-partner evaluation.

Your advantage:

- tests API LLM agents directly;
- introduces cross-play as an evaluation axis;
- analyzes partner-specific brittleness.

---

## 29. What not to do

Avoid:

- training a model from scratch;
- running full RL;
- relying entirely on LLM-as-judge scores;
- building a complex 3D simulator;
- using only one listener and calling it “pragmatic learning”;
- making claims about human social intelligence without human evaluation;
- adding too many scenario types before the core result is solid.

---

## 30. Minimal code skeleton

### 30.1 Candidate selection

```python
def select_mirror_selfplay(candidates, scene, training_listener, target_id):
    scored = []
    for u in candidates:
        choice = training_listener.choose(scene.listener_view, u)
        success = int(choice.choice_id == target_id)
        score = success - 0.001 * len(u.split())
        scored.append((score, u, choice))
    return max(scored, key=lambda x: x[0])
```

### 30.2 Population-play selection

```python
def select_population_play(candidates, scene, training_listeners, target_id):
    scored = []
    for u in candidates:
        successes = []
        choices = []
        for listener in training_listeners:
            choice = listener.choose(scene.listener_view, u)
            choices.append(choice)
            successes.append(int(choice.choice_id == target_id))
        score = sum(successes) / len(successes) - 0.001 * len(u.split())
        scored.append((score, u, choices))
    return max(scored, key=lambda x: x[0])
```

### 30.3 Cross-play evaluation

```python
def evaluate_crossplay(message, scene, heldout_listeners):
    results = []
    for listener in heldout_listeners:
        choice = listener.choose(scene.listener_view, message)
        results.append({
            "listener": listener.name,
            "choice_id": choice.choice_id,
            "success": int(choice.choice_id == scene.target_id),
            "confidence": choice.confidence,
        })
    return results
```

### 30.4 Bootstrap confidence intervals

```python
import random
import numpy as np


def bootstrap_ci(values, n_boot=5000, alpha=0.05):
    values = list(values)
    means = []
    for _ in range(n_boot):
        sample = [random.choice(values) for _ in values]
        means.append(np.mean(sample))
    return (
        float(np.percentile(means, 100 * alpha / 2)),
        float(np.percentile(means, 100 * (1 - alpha / 2))),
    )
```

---

## 31. Manual error-analysis template

Create a CSV like this:

```csv
scene_id,scenario_type,method,message,target_id,listener_choice,error_category,notes
rr_0042,relational_reference,mirror_selfplay,"select the red cube",obj_3,obj_1,underspecified,"two red cubes"
ps_0017,perspective_shift,direct,"select the cube on the left",obj_2,obj_4,perspective_error,"left differs by orientation"
```

Aim for:

```text
100 manually labeled failures total
~25 per major method
```

You can label these yourself. Be transparent in the paper that the manual taxonomy is author-coded.

---

## 32. Quality checklist before submission

### Core validity

- [ ] Target ID is never shown to the listener.
- [ ] Speaker messages are checked for target ID leakage.
- [ ] Listener outputs are valid object IDs.
- [ ] Same test scenes are used across methods.
- [ ] Prompts are frozen before final evaluation.
- [ ] Held-out listeners are not used for method selection.
- [ ] All responses are cached.
- [ ] Exact model versions are reported.

### Results

- [ ] Main table has confidence intervals.
- [ ] Scenario table explains where gains/losses occur.
- [ ] Cross-play gap is reported.
- [ ] Oracle upper bound is reported.
- [ ] Manual failure examples support the quantitative result.

### Paper

- [ ] Intro states the evaluation blind spot clearly.
- [ ] Related work is concise.
- [ ] Method is reproducible.
- [ ] Limitations are honest.
- [ ] Claims match actual results.
- [ ] Appendix includes prompts and schemas.

---

## 33. The strongest possible conclusion

If results support the hypothesis, the conclusion should say something like:

> Our results show that communicative success is not a sufficient proxy for pragmatic learning when the partner is fixed. Mirror self-play can improve same-partner success while producing messages that fail under cross-play. Population-play offers a cheap and simple mitigation by favoring utterances that are interpretable across heterogeneous listeners. These findings suggest that cross-play should be a standard evaluation protocol for language agents that learn from situated interaction.

If results do not support the hypothesis, use:

> In this controlled setting, we find less evidence of partner overfitting than expected. However, cross-play remains a useful diagnostic: it separates robust communicative strategies from listener-specific ones and reveals which scenario types require stronger pragmatic adaptation.

---

## 34. Final recommendation

Build the paper around this precise claim:

**Same-partner communicative success can overstate pragmatic competence; cross-play reveals whether interaction has produced robust pragmatic communication or merely partner-specific adaptation.**

The fastest high-quality version is:

1. build PRAG-CrossPlay with 600 scenes;
2. compare direct, best-of-K, mirror self-play, and population-play;
3. evaluate all methods with held-out listeners;
4. report cross-play gap and scenario-level failures;
5. release code, prompts, cached outputs, and data.

That is a realistic, distinctive, and workshop-appropriate paper you can execute without local models or large-scale training.
