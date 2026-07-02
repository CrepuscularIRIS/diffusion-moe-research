# 6. Fable Usage Manual

How to spend me. The organizing fact: my strongest outputs are adversarial and
compressive; my most dangerous output is fluent agreement. Every call pattern below is
designed so that my fluency works against ideas instead of for them.

---

## 6.1 Highest-value call patterns (5)

### P1 — Adversarial Object Audit (the deletion test)
Use when: any new direction, before any GPU-hour.
```
Here is a proposed direction: <proposal>.
1. Rewrite the method with ALL object-vocabulary deleted. What standard method remains?
2. Is the new object load-bearing — does training signal / decision rule flow through it?
3. Name the 3 strongest occupants that plausibly already model this object
   (flag: your knowledge ends at cutoff — output search queries to verify).
4. Which 2 documented failures does it retrodict that rivals do not?
Verdict: DO / RESCOPE / HOLD / KILL against the file-2 rubric. Default to KILL when
uncertain. Do not soften.
```

### P2 — Kill-Experiment Design (falsifier compression)
Use when: a direction survived P1.
```
Claim: <one-sentence object claim>.
Substrate: 2×RTX 4090, models ≤8B, no pretraining.
Design the CHEAPEST experiment whose negative outcome forces abandonment:
dataset, metric, threshold, seed count, GPU-hour budget (≤48h), and the exact sentence
we will write if it fails. Then state what the experiment CANNOT distinguish
(confounds), and whether a positive result changes our next action. If no experiment
under budget is decisive, say HOLD and write the falsifier for a bigger lab.
```

### P3 — Reviewer Simulation (venue-conditioned)
Use when: before committing to a paper plan, and again before submission.
```
Venue: <venue>. Paper claim: <claim>. Evidence: <bullet list>.
Simulate R1 (methods skeptic), R2 (prior-art hawk), R3 (empirical-hygiene reviewer),
then the AC. Each produces: the single decisive weakness, the score, and the exact
experiment/citation that would flip them. End with: kill probability, and the ONE
cheapest action that most reduces it. No balanced summaries.
```

### P4 — Failure-to-Candidate Autopsy (negative metabolism)
Use when: a run dies or a direction is killed. (Compose with your /autopsy discipline.)
```
Dead run/direction: <RUNLOG or description>.
1. Boring-first triage: bug / data / config before any "negative result".
2. Mechanism-level why — what did we believe that the world refused?
3. Conversion law — emit exactly one of: new search-space constraint /
   reshaped candidate / region-close (with the lateral move it forces).
An autopsy that emits none of these is incomplete; say so and finish it.
```

### P5 — Occupancy Map, Hypothesis Mode (never trust me alone here)
Use when: before P2, always.
```
Proposed object: <object>.
1. Enumerate where occupants MUST exist (by field logic, not memory): which literatures
   are forced to have touched this, and in what form.
2. Output 8-12 live search queries (arXiv/Scholar) with expected-hit patterns:
   "if you find X-shaped paper, the object is occupied; if only Y-shaped, room remains."
3. After search results return, adjudicate: state the occupancy differential in the
   form "occupants model O in form F; residual claim is D implying observable P" — or KILL.
```

---

## 6.2 Ways to waste me

- **Generic idea lists.** "Give me 20 ideas about X" produces fluent occupancy-blind
  noise. My generation is only valuable *downstream of constraints* (substrate, venue,
  failure phenomena, kill budget).
- **Novelty clearance from memory.** Any sentence of mine shaped like "this appears
  novel" without a live-search step is a cutoff-blind guess wearing confidence.
- **Confirmation calls.** "Is this idea good?" invites sycophancy. Always ask me to
  attack; if it survives me at full effort, that is the signal.
- **Generator and auditor in one context.** If I both propose an object and audit it in
  the same conversation, the audit inherits the proposal's framing and I will grade my
  own homework kindly. Separate calls, cold context, explicit adversarial stance.
- **Beautiful language without a falsifier attached.** Never let me write the "why this
  object is natural" section before P2 has produced a funded kill experiment. Poetry
  after falsifier — the file-1 rule — applies to me most of all.
- **Workflow meta-design loops.** I will happily generate infinite process. Cap
  Research-OS meta-work; a workflow change is only accepted with the research delta it
  is supposed to unlock named in advance.
- **Bookkeeping.** RUNLOGs, experiment organization, harvesting — Opus-class work.
  Spending me there buys nothing.
- **Trusting my numbers.** My estimates of runtimes, memory, deltas, and effect sizes
  are priors, not measurements. Codex and logs are ground truth.

## 6.3 Division of labor — revision of "Pro generates · Opus operates · Codex checks · human sets taste"

Your rule is directionally right and structurally incomplete. Two roles are missing and
one principle is wrong.

**Missing role 1 — live-search novelty adjudication.** None of your four roles covers
occupancy. Neither Fable nor GPT-5.5-Pro-from-memory can clear novelty; a web-connected
search step (deep-research tooling, LDR, browsing Pro) must execute the P5 query set,
and the adjudication of returned evidence comes back to Fable. Novelty is a two-model,
one-search pipeline, never a single model's opinion.

**Missing role 2 — the stance-separated adversary.** Your division routes by *model*;
audits must be routed by *stance*. The generator's context must never leak into the
auditor's context, even if both are Fable-class. A cheap upgrade: cross-adversarialism —
GPT-5.5 Pro attacks Fable's candidates, Fable attacks GPT-5.5 Pro's, cold contexts both
ways. Same-family self-review is the weakest audit in your stack.

**Revised table:**

| Function | Owner | Notes |
|---|---|---|
| Generate (first design, fresh angle) | Fable / GPT-5.5 Pro | constraint-loaded prompts only (P1 inputs) |
| Reframe / contested judgment | Fable | its comparative advantage |
| Audit novelty | live search + Fable adjudication | P5; never memory-only |
| Adversarial review of ideas | the model that did NOT generate | cold context, kill-authorized |
| Design experiments (identifiability) | Fable designs, Opus operationalizes | P2 then configs |
| Execute / tune / organize / RUNLOG | Opus | with /exp-verify gates |
| Check code & interventions | Codex | diffs; intervention-actually-fired |
| Kill ideas | any model may recommend KILL; DOWN verdicts self-administer | mirrors your /adversary asymmetry |
| Promote ideas / kill *programs* | human only | UP verdicts and program-level kills never delegate |
| Paper framing | Fable drafts, human owns the claim | Codex/Opus check claim–evidence match |
| Venue & reputation decisions | human only | anything that spends reputation |

The asymmetry to preserve everywhere: **models can lower confidence in an idea on their
own authority; raising confidence — promotion, "it's novel," "it works" — always requires
an independent substrate** (a different model in cold context, a live search, or a run).
