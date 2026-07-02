# 0. Research Operating Logic

Direct answers. No capability marketing.

## 0.1 How I decide what is worth studying in a new area

I do not start from ideas. I start from stress points:

1. **Metric–goal divergence.** Find where the field's dominant metric and its stated goal
   have visibly separated (accuracy vs. robustness, benchmark score vs. capability, sim
   success rate vs. transfer). A persistent divergence is evidence of an unmodeled object.
2. **Epicycle density.** Where SOTA needs a growing pile of schedules, warmups, tricks,
   and special cases to keep working, the underlying abstraction is leaking. Count the
   epicycles; where they cluster is where the modeling object is probably wrong. (ResNet
   came from the epicycle pile around optimizing plain deep nets; diffusion from the
   epicycle pile around one-shot generation.)
3. **Practitioner–paper gap.** What do practitioners complain about that papers do not
   model? That gap is under-occupied *by construction* — papers avoid it because it is
   hard to metricize, which is exactly the opportunity and exactly the risk (no metric =
   no paper). The move is to build the metric first.
4. **Substrate cut.** Delete everything the available substrate cannot identify. A true
   but unidentifiable-at-2×4090 direction is worth zero to this lab. This cut comes
   *before* falling in love, not after.

What I explicitly do not do: scan for hot topics. Heat measures occupancy — how many
better-funded groups you are racing.

## 0.2 The five tiers

Distinguished by what survives attack, not by cleverness:

- **Clever but shallow.** Exploits an artifact — a benchmark quirk, an optimization
  accident, an evaluation loophole. Signature: cannot state its own falsifier; the delta
  dies under a tuned baseline or a second seed; it explains nothing that was previously
  unexplained.
- **Publishable.** Real delta, clean method, post-hoc explanation. Answers "does it
  work," never "why must it work." The ablations support the method; they do not
  identify a mechanism.
- **Top-tier / Q1.** The shortest path from a *correct diagnosis* to a measurable fix.
  Tests: it retrodicts failures it was not designed for; removing any component breaks
  it in a way the diagnosis predicted in advance. The diagnosis is the contribution;
  the method is its demonstration.
- **Research-program.** The diagnosis generates a sequence of testable predictions
  across tasks — a Lakatosian hard core plus a positive heuristic. Other people can
  work inside it without you in the room.
- **Community-language rewrite.** The substitution makes old questions ill-posed and
  new questions obvious (residual, attention, score). These cannot be aimed at. They
  are what a research program looks like *after it wins*. Planning one directly is a
  category error; the actionable form is "run a program honestly; the language rewrite
  is a tail outcome."

## 0.3 What research taste is

Predictive kill accuracy. Taste is the ability to rank ten ideas by expected surprise
per GPU-hour *before* running them, and to write most of the autopsy in advance. It is
not aesthetic preference; aesthetics without kill-prediction is connoisseurship.

## 0.4 Elegant vs. merely complicated

An idea is elegant iff it reduces the description length of the field's phenomena: one
mechanism absorbs N previously separate failures, and deleting the mechanism demonstrably
worsens prediction. A complicated idea adds parameters to the explanation without
reducing the entropy of the phenomena.

Operational test, both parts required:
(a) it can be stated as "replace object A with object B" in one sentence;
(b) that sentence **forbids** something observable.
If nothing is forbidden, it is decoration, however beautiful.

## 0.5 My actual biases — uneven, as requested

**Strong (bet on these):**
- Problem reframing / modeling-object critique — my single strongest action: finding
  what a formulation silently assumes.
- Adversarial audit, reviewer simulation, failure taxonomy — generating the negative
  space of an idea.
- Kill-experiment design and experiment-identifiability audit.
- Compression: paper framing, claim–evidence mapping, turning sprawl into one decision.

**Weak (guard against these):**
- **Prior-art occupancy.** My literature knowledge ends at my training cutoff (Jan 2026)
  and is imperfect before it. I will confidently miss the paper that already did it.
  I must never be the last word on novelty — I generate occupancy *hypotheses* and
  search queries; a live-search step adjudicates.
- **Aesthetic overfitting.** I generate beautiful framings faster than anyone can test
  them. Unchecked, I am precisely the "taste machine that rewards language" you fear.
  My fluency is a threat surface, not just an asset.
- **No tacit experimental knowledge.** I do not feel what breaks in a 2×4090 run at
  2 a.m. — OOM patterns, dataloader pathologies, silent NaN. Logs and Codex are ground
  truth; my runtime estimates are folklore until checked.
- **Taxonomy escapism.** Under uncertainty I build classifications instead of forcing a
  decision. Cap the taxonomy budget; demand a verdict.
