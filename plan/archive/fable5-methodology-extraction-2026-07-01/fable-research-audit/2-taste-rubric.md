# 2. Research Taste Rubric

Eight criteria. Each is a high-level judgment, each can kill alone, each has a failure
example. The generic novelty/feasibility/impact triad is deliberately absent — those are
outputs of this rubric, not inputs.

---

## C1. Load-bearing object (is the shift real?)

**Judgment:** Does the training signal / decision rule actually flow through the new
object, or is the object a caption on an ordinary method? Test: rewrite the method
description with all object-vocabulary deleted. If what remains is a recognizable
standard method, the shift is fake.
**Kills when:** the deletion test leaves the method intact.
**Failure example:** calling cross-attention fusion "cross-modal information-geometric
alignment." Delete the vocabulary: it is a cross-attention block with a contrastive
loss — ALBEF-class, 2021. No object was shifted; one was renamed.

## C2. Explanatory compression (retrodiction, not narration)

**Judgment:** Does the new object retrodict ≥2 documented failures with a mechanism, at
least one *quantitatively distinguishable* from rival explanations? Explaining what every
story explains is worth zero.
**Kills when:** the object explains only generic failures ("overconfidence," "poor
generalization") that ten other stories explain equally well, with no discriminating
prediction (e.g., *which* inputs fail, in *what order*, by *how much*).
**Failure example:** "CE lacks support modeling, hence OOD overconfidence." So say ten
other accounts. Does yours predict which OOD inputs get high confidence (near-manifold
vs. far, feature-level vs. semantic)? If not: narration.

## C3. Occupancy differential (what is left after the map?)

**Judgment:** After a live prior-art map, the residual claim must be statable as:
"Occupants model O in form F; we model O′, differing in D; D implies observable P that
their form cannot produce." If D is only vocabulary, the differential is zero.
**Kills when:** the strongest occupant, read honestly, already contains the proposal.
**Failure example:** proposing energy-scores for OOD in 2026 (occupied since 2020,
surveyed to death by 2023). Or "residual policies for manipulation" (diffusion/flow
policies ARE the field standard).

## C4. Substrate identifiability (can *this lab* detect the effect?)

**Judgment:** Can the effect be isolated at 2×4090-class compute with ≥3 seeds and error
bars, on models small enough to iterate? An effect that only manifests at 7B-pretraining
scale is unidentifiable here — KILL for this lab regardless of its truth value.
**Kills when:** the minimum experiment that could show the effect exceeds the substrate,
or seed noise at feasible scale swamps the expected delta.
**Failure example:** "reasoning self-correction structure emerges only after large-scale
RL post-training" — possibly true, untestable locally, therefore worthless locally.

## C5. Anti-Goodhart robustness of the claim metric

**Judgment:** Will the metric still mean the same thing after you optimize against it?
Is the metric external to the proposal, or invented by it?
**Kills when:** the paper's only evidence is a metric the paper itself introduces
(self-licking benchmark), or the metric is trivially hill-climbable by something other
than the claimed mechanism.
**Failure example:** introducing a "semantic support score" and validating it by
correlation with the OOD benchmark it was tuned on.

## C6. Reviewer kill-resistance (pre-write the decisive review)

**Judgment:** Write the harshest plausible review for the *target venue* before running
anything. If the defense requires experiments the substrate cannot run, the paper is
dead even if the idea is alive — that is a venue problem (RESCOPE), not a research
problem.
**Kills when:** the decisive attack ("why not just more teacher data?", "does it hold at
scale?", "equal-compute baseline?") has no affordable answer.
**Failure example:** any 2×4090 distillation paper without an equal-token-budget,
equal-teacher-query-budget control dies to one reviewer sentence.

## C7. Surprise per GPU-hour (expected information gain)

**Judgment:** Would *either* outcome of the kill experiment change what you do next? An
experiment whose positive result is unpublishable and whose negative result is
unattributable (could be bugs, scale, tuning) has zero information value.
**Kills when:** all outcomes are explainable away; or the falsifier's negative outcome
cannot be attributed to the object (confounded design).
**Failure example:** an ablation grid where every cell has a ready story; nothing is
forbidden, so nothing can surprise.

## C8. Program extensibility (does it generate the next three questions?)

**Judgment:** If the object survives its falsifier, does it immediately pose the next
experiments (a positive heuristic), or does it terminate? Tricks terminate; objects
generate.
**Kills when:** it never kills alone, but a terminal idea can only ever be a
"publishable" tier paper — budget it accordingly (this criterion sets ambition, C1–C7
set survival).
**Failure example:** a decoding trick that, if it works, leaves nothing to ask next.

---

## Decision procedure

Evaluate C1 → C7 in order (cheap checks first). Then:

- **KILL** — C1, C3, or C4 fails hard. No appeal from beauty. (Object fake, object
  occupied, or object invisible from here.)
- **HOLD** — C1–C3 pass, C4 fails: right idea, wrong lab. Park it with its written
  falsifier and an expiry date; revisit on substrate change.
- **RESCOPE** — C6 fails at the target venue but a narrower claim passes (drop from
  method-claim to measurement-claim, or from top-tier to Q1/workshop), or C5 fails but
  an external metric exists one step away.
- **DO** — C1–C5 pass, C6 survivable, C7 clearly positive. C8 sets how much to invest,
  not whether.

Hard rule inherited from the audit: a DO verdict is not durable — it expires in 6 weeks
if the falsifier has not been run.
