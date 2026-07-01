# JOB2 — DSpark systems levers on frozen DiffusionGemma-26B: design + occupancy + kill-risk

> Tree 5.8.3. Systems lane: skips object-shift ceremony → cheap OBSERVE precheck → measured Δ → /baseline-champion.
> Frozen (no retrain). Metric = verified-answers/sec (generation/verifier ONLY). Sealed MATH-L5 untouched.

## The unifying frame + the baseline discipline (critical)
Every lever is a FROZEN, inference-time change to the dLLM sampler that should raise verified-answers/sec.
Measured with the SAME frontier protocol as JOB1 (S(B) vs wall-clock, Frontier-AUC, per-verified-sec) —
the modified sampler is a NEW arm.

**Two baselines, and (b) is the real test:**
- (a) matched AR sibling — the goal's stated bar. But dLLM ALREADY dominates AR at FAIR budget (JOB1), so
  "beats AR" is nearly free for any working dLLM sampler and is NOT evidence the lever adds anything.
- (b) the **un-modified EB-sampler dLLM** — the lever's VALUE is its marginal Δ over what we already have.
  ACCEPTANCE PRIMARY = Δ(lever − EB-dLLM) verified-ans/sec > 0 with CI excluding 0. Goal-required SECONDARY
  = still beats AR. A lever that beats AR but ties the EB-sampler dLLM is a NULL (adds nothing).

**Tuning discipline (anti-reward-hack):** levers #1/#2 have a threshold (stability/entropy). Tuning it on the
test set = reward-hack. Tune on a DEV split (or use a fixed principled threshold), evaluate on sealed MATH-L5.

## Lever ranking (PI skeptical call; each gated by a cheap OBSERVE precheck BEFORE any GPU dispatch)

### Lever #1 — token-level stability early-commit  [FIRST — most promising, cheapest]
- Mechanism (frozen): per-position stability signal = the model's own token entropy / logit-margin across
  denoising steps (NO trained head). When the \boxed{} block is stable (margin > τ for k steps), commit it and
  free the canvas for remaining positions → fewer NFE → faster per candidate → more candidates/sec.
- OBSERVE precheck (on existing dLLM raw, AFTER JOB1-A releases the files): measure NFE/forward-pass
  distribution and how many forward passes occur AFTER the boxed answer first becomes stable. If there is a
  meaningful "wasted" NFE tail post-boxed-stability → headroom. If EB-sampler already stops at stability → ~saturated.
- KILL-RISK: MEDIUM. The EB-sampler ALREADY early-stops (dLLM@2048 uses ~40 fwd passes, no-box 0.06). Lever #1
  only has value if there is residual post-stability NFE the entropy-stop leaves on the table. Occupancy
  (confidence-based unmasking / Fast-dLLM) matters little in the SYSTEMS frame IF the Δ is real & additive.

### Lever #2 — lossless dynamic canvas  [SECOND — distinguish from the KILLED allocator]
- Mechanism (frozen): first-few-step entropy → predict the needed canvas length → truncate canvas (fewer
  positions to denoise) WITHOUT lowering verifier pass-rate. "Lossless" = pass-rate must not drop.
- OBSERVE precheck: distribution of actual answer length (gen_tokens) vs the fixed canvas size. Many problems
  using << canvas → truncation headroom.
- KILL-RISK: MEDIUM-HIGH. FORBIDDEN list bans "compute-allocator/always-deepen" (5.8.1: oracle beats
  always-deepen@2048 by ~1% ΔAUC). Lever #2 is DISTINCT (per-problem canvas SIZE / #positions, not step/budget
  allocation) — but must PROVE the distinction is real, not cosmetic. Subsumption risk: if EB-sampler early-stop
  already captures the canvas-shrink gain (fewer tokens ⇒ fewer NFE already), lever #2 adds nothing.

### Lever #3 — intra-block sequential/Markov dependency  [THIRD — highest kill-risk]
- Mechanism (frozen, training-free variant): sequential/L2R unmasking WITHIN a block (unmask fewer tokens/step
  conditioned on already-unmasked) to model the joint instead of independent marginals.
- KILL-RISK: HIGH. (1) The just-banked masked-diffusion-reasoning saturation negative showed factorization is
  NOT the reasoning bottleneck at high step (1-tok/step control flat). (2) Frozen sequential unmasking TRADES
  speed for marginal quality — fewer tokens/step ⇒ more NFE ⇒ slower ⇒ likely net-NEGATIVE verified-ans/sec.
- OBSERVE precheck (cheap, may CHEAP-KILL pre-compute): at FIXED budget on MATH-L5, does reducing tokens/step
  (more sequential) raise dLLM accuracy AT ALL? If flat (as the saturation negative predicts) → kill before GPU.

## Pre-seal skeleton (per lever, filled at its DISPATCH)
- Hypothesis: Δ(lever − EB-dLLM) verified-ans/sec > 0 (CI excl. 0) AND beats AR AND pass-rate not lowered (lossless).
- Falsifier: Δ CI includes 0 (null) OR pass-rate drops > 1pp (not lossless) OR slower net (NFE↑ outweighs).
- Neg-control: threshold τ→∞ (lever off) must recover EB-sampler exactly; DEV-tuned τ evaluated on sealed only.
- Metric: verified-ans/sec, Frontier-AUC, per-verified-sec, no-box. NO diffusion-loss.
- Split: MATH-L5 sealed; threshold tuned on a DEV subset (or AIME/held-out), never on the sealed eval.

## Sequencing
JOB1 certified baseline → Lever #1 OBSERVE precheck → (if headroom) dispatch #1 measured run → /baseline-champion
→ Lever #2 → Lever #3 (or cheap-kill #3 pre-compute if the tokens/step OBSERVE is flat). AUTO-PIVOT on null: next lever.
