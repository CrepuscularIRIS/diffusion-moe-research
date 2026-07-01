# H4 identifiability wall — statistical/causal design request

**For:** GPT-5.5 Pro (专业). **From:** Diffusion-MoE research project (Opus coordinator).
**Type:** hard statistical + causal experimental design. Please address the 3 questions at the end.

## Setting
- Model: **DiffusionGemma 26B-A4B** — a *block discrete-diffusion* language model (not autoregressive). It generates a 256-token "canvas" by iterative denoising over ~48 denoising calls; an **MoE router** picks **top-8 of 128 experts** per token-position per layer (30 decoder layers).
- **Hypothesis H4:** "MoE experts **specialize by denoising timestep t**." H4 is the motivating premise for our novel contribution (Direction C): an explicit **timestep-conditioned router** in a diffusion-language MoE.
- We tried to test H4 from **passive routing logs**: for each (trajectory, token-position, denoising-call, layer) we logged the top-8 expert IDs + gate mass. Pilot: 6 prompts × up to 48 calls × ~43 positions × 30 layers × 128 experts.

## The test we built (and its failure)
- **Statistic:** track-stratified conditional mutual information / G, with track = (trajectory, token-position): `T_L = MI(timestep-bucket B ; expert E | track)`, summed over tracks; K=8 equal-count timestep buckets; trajectory-synchronous design.
- **Null:** permutation of the per-call timestep-bucket labels within each trajectory (the "free shuffle"); shared-draw maxT FWER across 30 layers.
- A real-orbit validity gate confirmed the *test machinery* is exact-by-construction (Hemerik–Goeman); that part is fine.

## The fundamental problem we discovered (validation-first, quantified)
**Routing drift is a global MONOTONE DENOISING TREND, not stationary noise:**
- Lag-Jaccard of the routed expert set decays **0.67 (lag-1) → 0.44 (lag-10) → 0.35 (lag-20) → 0.13 (lag-47)**, monotone, **no plateau**.
- Within-track first-half vs second-half expert-distribution **total variation = 0.41** (strong trend; >0.3 = strong).
- Adjacent-call Jaccard **0.809** vs random-pair 0.579.

**The timestep buckets are contiguous blocks of call-order** (bucket = which ~1/8 of the denoising trajectory). So **bucket label and routing are BOTH monotone in call index.** The observed bucket→expert partition is therefore the **maximum-MI configuration**, which forces a dichotomy:

| null family | type-I (real-geometry AR-trend **H0**, no genuine t-effect) | power (planted genuine t-tilt) |
|---|---|---|
| free shuffle (current) | **fwer = 1.00** (catastrophic) | high |
| circular-shift / AR-surrogate | fwer = 0.41 | ~0 recovery |
| monotone re-segmentation | fwer = 0.79 | ~0 recovery |
| block-label permutation (permute the K=8 contiguous blocks) | fwer = 0.047 (OK) | **ZERO power** (MI-invariant on ~equal blocks) |

- **Negative control:** with the trend removed (no drift), free=0.031, circ=0.052 → calibrated. So the **monotone drift is the SOLE cause** of inflation (not the harness, not contiguous geometry per se).
- **Trend gradient:** circ fwer 0.10 (ρ=0.5) → 0.19 (0.85) → 0.41 (0.98); never ≤ 0.065. free = 1.00 under *any* drift.
- **Honest real-pilot verdict by null:** free → 29/30 layers "significant" (ΔNMI 0.137); circ → 2/30; reseg → 2/30; block → 0/30. The "29/30" headline exists **only** under the invalid free shuffle.

**Mechanism / the wall:** under a monotone denoising trend with contiguous ~equal buckets, *any partition-CHANGING null inflates* (observed = max-MI) and *any partition-PRESERVING null is MI-degenerate (zero power)*. There is no middle ground for a within-trajectory label-permutation test. **In passive logs, "the router reads the timestep embedding t" is statistically indistinguishable from "routing drifts because the hidden state/canvas evolves as it denoises" — both produce the same monotone bucket→expert association.**

**The estimand collinearity:** bucket is itself ≈ a deterministic monotone function of denoising progress. So "does timestep add information *beyond a smooth monotone function of denoising progress*?" risks conditioning away the entire signal.

## Questions (please be concrete and rigorous)
1. **Is any confound-robust PASSIVE-LOG estimand/test possible?** Define estimand + null precisely; argue type-I control under the monotone-trend DGP **and** non-trivial power; resolve the bucket≈progress collinearity. Is the right question "expert depends on t" or "expert depends on t beyond what content/position/denoising-progress predict"? If passive is hopeless, say so decisively.
2. **If we must go interventional, design the t-SWAP INTERVENTION precisely.** Freeze the canvas/hidden state at a denoising step; re-run only the routing computation with the **t-embedding swapped** to another timestep's value; measure whether top-k expert selection changes. Specify: the exact protocol; the statistic; the null/baseline (swap to random-other-t vs adjacent-t); **controls for the fact that the timestep also drives conditioned LayerNorm/scale** (so a naive swap changes more than "what the router reads"); the falsifier; and the effect size that would justify building a timestep-conditioned router.
3. **Does H4 even need to be t-specifically (vs progress-specifically) true** for the Direction-C timestep-conditioned router to be worth building? What is the **minimal** experiment that cleanly distinguishes the two and de-risks the whole direction?
