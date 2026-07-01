# Structural Result — A Frozen Near-Ceiling Discrete-Diffusion LLM Is Pareto-Optimal to Post-Hoc Inference-Time Intervention

> Banked 2026-06-29 (Codex SELECT = "bank the negative synthesis; legitimate loop stopping point"). The
> He-level continuous-loop campaign's outcome: not a new positive method, but a **clean, falsifiable, non-obvious
> structural negative** that unifies this project's kills and explains Track-1. Arbor tree node 5.9 (+ 5.9.1/5.9.2).

## The claim (scoped — do NOT overclaim "only retraining can ever work")
> For a FIXED, frozen, production-scale discrete-diffusion LLM (DiffusionGemma 26B-A4B) operating near its
> **native budget-accuracy Pareto frontier**, post-hoc inference-time interventions over **commitment,
> stopping, compute-allocation, within-block factorization, and representation-routing** do NOT move the
> verified-accuracy / compute frontier. **Changing what the generator PRODUCES (its weights/target via
> training) is the remaining untested axis.**

One-principle reading (the He-aesthetic, applied to a *negative*): the frozen generator already extracts
essentially all the verified accuracy its weights + token budget allow; re-routing, re-timing, re-ordering, or
re-combining its existing outputs is **information-free** — the lever, if any, is upstream of the fixed forward.

## Evidence (this campaign + prior kills), all generation/verifier-based
| Axis | Intervention | Result | Where |
|---|---|---|---|
| **Factorization** | ① V1 — joint re-denoise of the high-entropy UNCOMMITTED residual via native self-conditioning | **CLEAN NEG**: fixed 0/10 wrong; = random-position = uniform-SC = "one more denoise"; only WRONG conditioning hurt; no locality. Per-position factorization is free even in the residual. **SEALED-CONFIRMED** (L5-holdout n=94: joint 0.7447 ≈ independent 0.7553, Δ−0.011; shuffled control −19pp). | tree 5.9.1/5.9.3; dev L5-dev-40@2048 + sealed L5-holdout |
| **Stopping / allocation** | ② anti-truncation output-presence observer (bank-on-solved / spend-on-truncation at matched mean) | **CLEAN NEG**: observer 0.95@774tok == always-deepen-to-matched-mean 0.95@774; sits ON the native budget-Pareto; 9/10 no-box→correct is real premature-readout but native early-stop self-banks budget equally. **SEALED-CONFIRMED** (L5-holdout n=94: observer 0.7872 == always-deepen-matched 0.7872; forcebox control −42pp). | tree 5.9.2/5.9.3; dev L5-dev-40@{768,1280} + sealed L5-holdout |
| **Representation-routing (embedding-flow)** | training-free few-step embedding-DDIM / continuous carriers | **NARROWED**: Euclidean snap = Voronoi trap; right-metric/no-snap carriers MATCH native but never beat it (no speed win; model already adaptive-few-step). | tree 5.3.1/5.3.1.1; `plan/archive/gpt55pro-novelty-framing-2026-06-28.md` |
| **Commitment ranking** | E learned trace-dynamics ranker | KILLED (AUC below random; = the nfe counter). | tree 5.7 |
| **Problem-level allocation** | learned compute-allocator | DEAD (PERFECT oracle beats always-deepen by only ~1% ΔAUC → "just deepen"). | tree 5.8.1 |
| **Measurement** | reference-token / equivalence-class observability (A) | FALSIFIED (the "2.3%" was a t=1.0 artifact outside the sampler band). | tree 5.1 |
| **Upstream SC-time-transport (training-free)** | PSC-Bridge oracle — inject the model's OWN stored future self-conditioning belief into a compressed 24-step replay (the one *upstream*, non-post-hoc lever; e-geodesic secant fed to the native SC gate) | **CLEAN NEG (ARTIFACT/LEAKAGE_KILL)**: direct-oracle +5pp over native_24 is reproduced EXACTLY (acc+strata) by the final-SC leakage control → trajectory leakage, not a deployable mechanism; replay_null==native_24 (plumbing OK); deployed adaptive native (0.95 @ 34 NFE) DOMINATES the forced-48 ceiling + oracle alike. Pro's gate vetoes the training path (oracle failed). | tree 5.9.4; dev L5-dev-40 (Codex DECIDE=ARTIFACT, bank-dev) |

Recurring mechanism: **every one of these acts post-hoc on a FIXED generator output** (and the one *upstream*
training-free lever — SC-time-transport — fails its necessary-condition oracle gate via answer-leakage). None
changes the weights or the trained target. The convergence of **seven** independent attempts on the same null
is the result. **SCOPE (Codex, cycle 18):** this does NOT prove "only retraining can EVER move the frontier"
(over-reach); it proves these tested classes + a training-free SC-transport oracle yield no clean deployable
mechanism, and the frozen generator's native adaptive sampling dominates them.

## Why this is non-obvious + valuable (not "our method didn't work")
1. **It excludes ≥5 plausible directions** with controls + locality + matched-compute, not by failure-to-tune.
2. **It explains Track-1** (the one banked POSITIVE: frozen DiffusionGemma dominates the verified
   wall-clock frontier vs matched AR): the model is *near-optimal at extracting its own capability*, which is
   precisely why its parallel/few-step decoding is safe AND fast. The negative synthesis is the mechanistic
   companion to the wall-clock paper.
3. **It re-localizes the field's headroom**: for frozen production dLLMs near ceiling, inference-time "smarter
   decoding" papers (commit/stop/allocate/factorize) are bounded by the budget-Pareto; the open lever is
   training the generator (target/loss), which is where the He-line (JiT/MeanFlow/pMF/ELF) actually lives.

## ★ PRE-REGISTERED FALSIFIER (frozen before the sealed confirmation; anti-p-hacking)
The synthesis is BROKEN by: **any fixed-generator (no-weight-change) intervention that beats native AND
always-deepen-to-matched-mean by ≥2pp verified accuracy at matched NFE AND matched wall-clock, with the
negative/locality/anti-verifier-surface controls intact, on a sealed hard set (L5-holdout or AIME).** No such
intervention has been found across six attempts.

## ★ Sealed confirmation — DONE 2026-06-29 (bg bgd8tpl7s, MASTER_EXIT=0): BOTH nulls reproduce → BANKED
Pre-registered NON-SEALED dev = MATH-500 L5[:40]; SEALED HOLDOUT = L5[40:134] (n=94, CPU-verified disjoint,
overlap 0) + AIME (future-work). Integrity gate `7+5→12 ok=True` on both seal halves. **Neither falsifier fired.**

- **V1 residual-joint on L5-holdout @2048, K=8, 6 arms (n=94).** native 0.7447.
  joint **0.7447** (0 repair / 0 damage) ≈ independent **0.7553** → joint−independent Δ=**−0.0106** CI[−0.0319, 0];
  auto-verdict **CLEAN_NEGATIVE**. **Negative control LIVE:** shuffled (wrong-SC) **0.5532**, joint−shuffled
  Δ=**+0.1915** CI[0.117, 0.277] (18 damaged) → the harness demonstrably *can* detect a real effect, so the null
  is **not** a dead probe. benign(uniform-SC) 0.7553 ≈ joint; plus1_vanilla **0.7447 = native exactly**;
  random_residual **0.7447 = native exactly** (no locality). → factorization free even in the uncommitted residual.
- **② output-presence observer on L5-holdout (one cap=2048 trace/problem → arms post-hoc sliced, n=94).**
  native_eb@1280 **0.766** (929 tok), @768 0.479. observer_s1/s2_cap{1536,2048} **0.7872** (1024–1242 tok).
  **always_deepen_matched** (budget 2048, target 1108 tok) **0.7872** at mean **969 tok** → observer == always-
  deepen-to-matched-mean (**+0 pp**) at *equal/lower* budget; sits ON the native budget-Pareto. forcebox@1280
  **0.3404** ≪ native 0.766 → **not** a verifier-surface hack. Disambiguator: 29/47 native-no-box→correct under
  observer (5/47 forcebox) = REAL premature-readout; **correct→wrong regressions = 0**; but native budget self-banks
  it equally → schema-aware stop adds nothing over a higher uniform budget.

Result: both pre-declared dev nulls reproduce on the sealed holdout with their negative controls firing
(V1 shuffled −19 pp; ② forcebox −42 pp). The negative synthesis is **BANKED** (tree 5.9 done, 5.9.3 added).

## Future work (explicitly OUT of this frozen-inference loop)
- **PSC-Bridge training path is VETOED by its own gate (cycle 18).** Pro's design pre-declared "train the scalar-α
  adapter only AFTER the training-free oracle passes." The oracle FAILED (LEAKAGE_KILL; native-EB dominates), so the
  cheap-adapter SC-time-transport is not worth a training run. This *closes* the one training-free upstream lever.
- **UP-1 (a genuinely upstream, weight-changing axis — NOT frozen-inference):** a tiny ON-MANIFOLD adapter trained on
  verifier-correct trajectories that REFINES what the generator PRODUCES (its SC clean-estimate / denoising target).
  This is the ONLY axis the campaign did not falsify — but it is a TRAINING commitment, outside the FROZEN-inference
  scope of this goal, and the scoped synthesis does NOT assert it will work (Codex: no universal "only retraining"
  claim). Treat as a separate project with its own gate, not a continuation of this loop. Novelty-risky vs
  pMF/SDTT/ELF/LRD/SCMDM; thin headroom (near-ceiling).
- AIME generality of the negatives; the full native budget frontier figure; one more discrete dLM for the structural claim.
