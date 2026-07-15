# Backward-Reasoning in the Pipeline — Is Deeper Credit Assignment a Tradeoff?

*Audit note, 2026-07-15. Trigger: the three-modes-of-backward-reasoning discussion (post-hoc
reflection · credit assignment · inverse planning) and the two proposed pipeline hardenings —
(a) autopsy must name the EARLIEST decision on the LATENT-ROOT chain (cross-cycle credit), (b) enforce
credit-assignment DEPTH. Question posed: is this a tradeoff or a free improvement?*

---

## Verdict (one line)

**It is a tradeoff — the bias–variance, explore–exploit, and speed–rigor families, mapped onto research
meta-reasoning.** The three backward modes are not free wins; each is an *operating point* that pays for
what it buys. The pipeline mostly sits at defensible points already. Of the two proposed hardenings, the
DEPTH one is redundant (already handled by scale-to-stakes) and the CROSS-CYCLE-CREDIT one is
**net-negative unless it carries a "known-at-the-time" counterfactual guard** — otherwise it manufactures
confident-but-wrong early roots (hindsight bias).

---

## 1. Why it is not free: the three modes are points on dials, not upgrades

| Mode | Buys you | Costs you (the other end of the dial) |
|---|---|---|
| **Post-hoc reflection** (adversary · exp-verify · jury) | Cheap, low-variance "is the claim real" | Does NOT localize the causal step — low information about *what to change* |
| **Credit assignment** (abduce · autopsy failure-locus · ledger Brier) | Localizes the decision that mattered | Higher variance + higher cost + hindsight-bias risk; wrong attribution is *confidently* wrong |
| **Inverse planning / forward-sim** (admit kill-first-3 · tricks oracle-ceiling · forge DIFF-PRED) | Prunes high-risk paths before spend | Biases toward *legible* directions the forward model can score — under-explores high-variance upside |

Moving "up" each row is not strictly better. It trades a cheap, robust, uninformative signal for an
expensive, fragile, informative one. That is the definition of a tradeoff, not an improvement.

---

## 2. The specific tradeoff axes (and where the pipeline currently sits)

**A. Credit granularity ↔ attribution variance (bias–variance).**
This is the RL problem verbatim. Fine-grained step-level credit ("the assumption at step 12 killed the
run at step 80") is high-variance — you may blame a decision that was correct given what was known.
Coarse outcome credit ("the direction didn't clear the venue bar") is low-variance but tells you nothing
about *which knob to turn*.
- *Where we sit:* `/autopsy` scales `abduce` to stakes (hunch-null → one-line why; claim-bearing kill →
  full 5-step abduce). This is a **correct adaptive operating point** — spend variance-reduction effort
  only where the decision is expensive. Do not flatten it into a fixed depth rule.

**B. Exploit the forward model ↔ explore (explore–exploit).**
Mode-3 planning (admit's kill-first, ledger forecasts, taste-rank) chooses the lowest-*predicted*-risk
path. Over-trusting that forward model prunes exactly the directions it under-predicts — the high-upside
weird ones.
- *Where we sit:* the HUNCH lane + value-bar-EXTERNAL rule + "internal gates PRICE, never veto" are the
  explicit explore-preserving counterweights. Reasonable, but the bias is real: a legible, ledger-scorable
  direction will always out-compete an illegible one at `/admit`. The v3 self-occupancy risk (re-deriving
  v2 in new vocabulary) is an *exploit* failure — the forward model keeps recommending the neighborhood it
  can score.

**C. Rigor ↔ velocity (speed–rigor).**
Every backward-reasoning step is latency. Deeper credit assignment = more discriminating probes, more
consults, more wall-clock before the next forward move.
- *Where we sit:* the four-gates-not-scripts design + the "documents ≠ progress / persistence" rule are
  the velocity guards. The standing failure mode ("a few fixes, a document, stop") is what *too much*
  backward-reasoning-as-ceremony looks like. More machinery here is not obviously good.

**D. Machinery ↔ gameability (the meta-tradeoff).**
Every added backward-reasoning requirement is new surface area that can be filled *shallowly* — the
"every gate passed the hollow work" audit finding (v2). A rule that says "name the earliest root" gets a
plausible-sounding root written in, not a true one. Adding rigor can *reduce* real rigor by diluting
attention across more mandatory fields.

---

## 3. The near-contradiction the pipeline resolves by separation

Your synthesis — *"reinterpret the past based on the final outcome, while using forward simulation to
plan the future"* — contains a live tension with our honesty invariant:

- **Hindsight reinterpretation is the ENGINE of credit assignment** (Hindsight Critic, HER-style
  relabeling): you re-read the trajectory *knowing the outcome* to find what mattered.
- **Hindsight reinterpretation is FORBIDDEN on evidence** by the honest-evidence invariant: prereg before
  a claim-bearing run, and a post-hoc-edited forecast row is VOID.

These are not actually in conflict — the pipeline resolves them by **separating the objects**: you may
reinterpret *judgments and roots* freely (that is what `ledger` DISTILL and autopsy LATENT-ROOT do), but
you may never reinterpret *sealed numbers* (prereg, verify markers). The tradeoff is only dangerous when
the two blur — i.e., when an outcome-driven story about "what the run really showed" edits the reading of
the run. The invariant exists precisely to hold that line. So this one is a *managed* tradeoff, and the
management (separate the reinterpretable judgment from the immutable evidence) is already load-bearing.

---

## 4. Verdict on the two proposed hardenings

**(a) "Autopsy must name the EARLIEST decision on the LATENT-ROOT chain" (cross-cycle credit).**
- *The pull is real:* v2 ran ~15 cycles to evidence-complete-dead when the root was arguably the early
  admission of goal-invariant DMC locomotion (L7, distilled LATE). Long-horizon credit is genuinely weak.
- *But naive form is net-negative:* forcing every kill to blame an *earliest* decision maximizes
  attribution variance and hindsight bias. Most early decisions looked correct given information then;
  blaming them confidently teaches the loop the wrong lesson and could suppress reasonable early bets.
- **Ship only with a guard:** the named early root must pass a **counterfactual-known-at-the-time test** —
  *"was this decision wrong GIVEN what was knowable when it was made, or only in hindsight?"* If only in
  hindsight, it is banked as an **unknowable-then** contingency (informs priors), NOT charged as a
  process error. This converts raw hindsight credit into calibrated credit and is the analog of a
  properly baselined advantage (GAE) rather than raw return. With the guard: worth it. Without it:
  net-negative.

**(b) "Enforce credit-assignment DEPTH."**
- **Reject as a fixed rule.** `/autopsy`'s scale-to-stakes already sets depth adaptively, which is the
  correct operating point on axis A. A fixed depth floor spends variance-reduction effort on cheap kills
  where it is wasted, and adds gameable ceremony (axis D). The existing dial is right; do not replace an
  adaptive control with a constant.

---

## 5. Recommendation

1. **Do not add machinery; tune one existing dial.** The only defensible change is adding the
   *known-at-the-time counterfactual* to autopsy's LATENT-ROOT step (one line in the extraction row:
   `root-was-knowable-then: yes/no`). This *sharpens* credit assignment's calibration without adding a
   new gate — it makes the existing credit step less hindsight-biased, i.e., it moves us *down* the
   variance axis for free.
2. **Watch the explore–exploit dial (axis B) as the live risk**, not the depth dial. The forward model
   (ledger + taste) keeps recommending v2's neighborhood; that is the current, concrete cost of Mode-3
   planning, and it is not fixed by more credit assignment.
3. **Treat the honesty separation (§3) as the invariant it is** — the one place the tradeoff turns
   dangerous is evidence-relabeling, and that is already guarded. Keep it guarded.

---

## Synthesis

Backward reasoning is not "more is better." It is a set of dials with real costs — variance, foregone
exploration, latency, and gameability. The pipeline already occupies mostly sane operating points
(adaptive abduce depth, external value bar + hunch lane for exploration, prereg for the
credit-vs-evidence separation). The genuine weakness — slow cross-cycle credit — should be fixed by
*calibrating* the existing credit step (a known-at-the-time counterfactual), not by mandating more depth
or more roots. Deeper is not the goal; **better-baselined** is.
