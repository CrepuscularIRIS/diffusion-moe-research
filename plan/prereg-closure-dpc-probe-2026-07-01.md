# PREREGISTRATION — Closure-Utility-Head DPC probe (frozen O0, measure-first, NO training) — 2026-07-01

> Sealed BEFORE the run (RULES §5.1). Arbor node 5.11.2.1. Gates whether O1 (Closure-Utility Head,
> plan/gpt55pro-closure-utility-head-2026-07-01.md) may proceed to training. Frozen forward passes only —
> no training, no diffusion loss, no reference-token metric. Metric = generation/verifier only.
> Object-shift-audit verdict = DOWNGRADE_TO_TACTICAL_VARIANT; ELIGIBLE unlocks only if this probe yields
> dpc_check=DIFFERENTIAL_PATTERN_FOUND.

## HYPOTHESIS
On frozen DiffusionGemma-26B O0 generation over MATH-L5 + AIME-2024, the **closure-strandedness stratum S**
(S0 none / S1 candidate-only / S2 candidate+tight-budget / S3 candidate+tight-budget+terminal-rank-discordance)
predicts verifier-rescue by an **O0-matched closure oracle** (insert T(a)="\nTherefore, \boxed{a}." into masked
tail slots, a extracted from the model's OWN committed scratchwork, no extra steps, no change to committed
reasoning) MONOTONICALLY, concentrated in S3 — ABOVE shuffled-S, generic-difficulty, and the DeadlineBox
surface-form rival. I.e. a trained hidden-state closure signal has real headroom O0's factorized commit misses.

## FALSIFIER (pre-declared — ANY ⇒ object dead before training)
- S3 contains <40% of truncation-labeled failures, OR
- O0-matched closure oracle rescues <20% of S3 failures, OR
- overall verified-gain upper bound <+3pp on AIME/MATH-L5 AND <25% relative truncation-failure reduction, OR
- median first-valid-answer step in rescued logs does NOT move ≥25% earlier at identical step count/commit quota, OR
- **shuffled-S predicts rescue nearly as well as real S** (shuffled-S3 enrichment >25% of real; shuffled-S logistic coeff not null), OR
- **generic-difficulty absorbs S** (adding S improves AUC <0.05 OR odds-ratio for S3 <2.0 OR effect collapses under item-clustered SEs), OR
- **DeadlineBox captures ≥70% of closure-oracle rescues** (then it's deterministic terminalization, not a modeling object), OR
- **[audit gap 3] confident-wrong false-positive:** on S0–S2 states the closure oracle FALSELY triggers and produces confidently-wrong committed answers at a rate that nets the verified-gain negative (5.9.2 precedent: naive forcing = −42pp). If forcing net-harms once false-positives are counted, the trained-selector premise is unsafe.

## ACCEPTANCE (GO — all required to declare DIFFERENTIAL_PATTERN_FOUND)
S3 ≥40% of truncation failures · oracle rescues ≥20% of S3 · overall ≥+3pp OR ≥25% rel truncation reduction ·
median step ≥25% earlier · real-S ≫ shuffled-S · S survives generic-difficulty (AUC≥+0.05, OR≥2.0, clustered-SE
robust) · DeadlineBox captures <70% AND high-S carries extra hidden-state/rank signal DeadlineBox misses ·
net-positive AFTER counting false-positive confident-wrong on S0–S2.

## NEGATIVE CONTROLS (mandatory)
1. **Shuffled-S**: shuffle S within task × difficulty × step-decile × output-length bins; monotone curve must vanish.
2. **Generic-difficulty regression**: Y=closure-oracle-rescued on {mean entropy, max confidence, mask count,
   step fraction, prompt length, generated length, remaining slots, O0 item pass-rate, task FE}; then add S.
3. **DeadlineBox rival** (capacity-tightness-gated force-fill, NO hidden-state head) — [audit gap 2] run SEPARATELY
   from the older 5.9.2 force-box control (which lacked the capacity gate); report BOTH, do not conflate.
4. **[audit gap 3] Confident-wrong control**: measure oracle false-positive rate + net verified Δ on S0–S2.

## METRIC (generation/verifier ONLY)
Verifier pass/fail on final \boxed{} answer (existing sealed MATH-L5/AIME verifier); per-S-bin oracle rescue
rate; overall verified-gain upper bound (pp); truncation-failure relative reduction; median first-valid-answer
step. NO diffusion loss, NO reference-token agreement, NO teacher forcing.

## SPLIT
Dev = a MATH-L5/AIME subset for pipeline validation + threshold sanity (measure-first timing probe first).
Sealed holdout = the remainder of MATH-L5 (134) + AIME-2024 (30) for the reported GO-gate numbers. The verifier
+ problem sets are SEALED — never modified. (The DPC is descriptive on frozen logs, so leakage risk is low, but
report dev vs holdout separately.)

## RIVAL CAVEAT (claim language — [audit gap 1])
AG-GRPO (trained closure-like signal via full-policy post-training) is the more structurally dangerous rival.
It is NOT run empirically here (no training in this probe); any downstream claim must state O1's novelty as a
FROZEN-backbone closure selector trained from logged truncation states, NOT vs a fully post-trained policy.

## SUBSTRATE / MEASURE-FIRST
Frozen DiffusionGemma-26B, 2×RTX-4090 (verify shard SHAs on load; ground-truth 7+5→12 before trusting).
Needs per-step logit instrumentation of the EntropyBoundSampler (per-position top-k logits + EBS commit rank +
mask set + committed tokens). Stage 0 (no GPU): audit existing wall-clock-5.8 logs for reusable fields.
Stage 1 (GPU): re-instrument on a ~30-problem subset (timing probe) before the full MATH-L5+AIME run.
