# Scoped landscape-negative — masked-diffusion-LM REASONING is saturated for He-bar novelty (2026-06-30)

> Banked outcome of the OPEN `/goal` ("OPEN autonomous research on the diffusion-LM platform — deliver a real
> contribution OR a clean banked negative"). Grade: **scoped-negative** (self-graded DOWN; independently
> corroborated by 2× GPT-5.5-Pro audits, 2× Codex SELECT gates, and the project's own prior architectural audit).
> Negatives = success. NO GPU was spent on any intervention — the gates blocked every dispatch before compute.

## The scoped, falsifiable claim
Under the goal's constraints — a **He-bar** (minimal-mechanism, *diffusion-specific*, surviving a **1-token/step
high-step control**), **non-occupied** contribution on the masked-diffusion-LM **REASONING** platform
(trainable **LLaDA-8B-Instruct** / MATH-500 + frozen **DiffusionGemma-26B-A4B**, 2×RTX-4090D), with
frozen-26B-improvement · He-line x0/velocity target-migration · post-hoc compute-allocation/scheduling
**forbidden** — **no such direction survives**, because:
1. the LLaDA-8B MATH **accuracy ceiling is reached at 128 denoising steps and is FLAT to 512** (=1 token/step);
   the few-step collapse is a **coherence/SPEED** phenomenon only;
2. of the residual ceiling errors, **~73% are base-model reasoning/algebra errors** (the derivation itself is
   wrong — not diffusion-addressable), ~7% scoring artifacts, and only **~20% (~7.5% of items)** are the
   diffusion-flavored "answer-corruption" mode (correct derivation, wrong final boxed token);
3. **every diffusion-specific accuracy lever is occupied** by ≥2026 prior art (factorization/joint-readout;
   order/AR-tax; verifier-free self-revision);
4. the **MoE-diffusion-specific routing question is architecturally vacuous** (the DiffusionGemma router has no
   timestep input) and its passive form is statistically unidentifiable.

**FALSIFIER (pre-declared):** a diffusion-specific intervention that, at **matched high-step (≥128) NFE** with a
1-token/step control intact, raises **verified** MATH-500 accuracy by **≥3pp over native**, is **not subsumed**
by CoDD / ADJUST / ADAS / ReMDM / Targeted-Remasking / No-Compute-Left-Behind, **and exhibits a mechanism that
would NOT equally apply to an AR model** (i.e. genuinely diffusion-specific, not a generic reasoning gain), breaks
this negative.

> **Calibration (Codex):** this is sound as a **research-gate / landscape negative, NOT a theorem.** The 128→512
> flatness alone is statistically underpowered (n=40 DEV); the decisive evidence is the **512-step 1-token/step
> trace classification** (residual failures are mostly ordinary algebra/reasoning, only a small answer-corruption
> slice a diffusion mechanism could plausibly touch). The bank does not claim "diffusion can never help reasoning";
> it claims "no *non-occupied* diffusion-specific *minimal mechanism* currently survives the 1-token/high-step
> MATH-500 control as a plausible accuracy contribution, under these exclusions."

## OBSERVE evidence (real, sealed; `outputs/heline/stepsweep_probe.json`)
Native LLaDA-8B-Instruct, MATH-500 DEV-40, gen=512/block=64, native sampler (temperature 0, low-confidence remask):

| steps | tok/step | acc | boxed_rate |
|---|---|---|---|
| 8 | 64 | .025 | .00 |
| 16 | 32 | .000 | .03 |
| 32 | 16 | .050 | .10 |
| 64 | 8 | .350 | .72 |
| 128 | 4 | **.625** | .95 |
| 256 | 2 | .600 | 1.00 |
| 512 | 1 | **.625** | 1.00 |

- **Coherence cliff** below 64 steps (boxed_rate → 0): the few-step regime is gross incoherence (under-denoising),
  i.e. a SPEED problem (occupied territory), not "right-pieces-wrong-assembly".
- **Ceiling flat 128→512**: more denoising does not raise accuracy → the residual errors are structural.
- **Ceiling-error trace classification** (15 wrong-but-boxed @512=1 token/step): ~73% genuine reasoning/algebra
  (e.g. "8 = 4²"; derived an interval inequality backwards "8/3 ≤ p < 3/5"; expansion error → 7u+14; "−55 ≥ 0
  holds for all reals"); ~7% scoring artifact ([-2,7] ≡ x∈[-2,7]); ~20% answer-corruption (3√3/4 → "simplified"
  to √3/2; derived x=0 but boxed 4). The diffusion-flavored signal is a small residual.

## The 6 convergent, independently-verified kills
| # | Direction | Why dead | Evidence |
|---|---|---|---|
| 1 | He-line x0/velocity **target-migration** | structurally absent on discrete masked diffusion (masked-CE already predicts clean-x0) | `plan/heline-structural-negative-2026-06-30.md` (Pro verdict "结构性不通") |
| 2 | Frozen-26B **inference-time** (commit/stop/allocate/factorize/route/embed-flow + SC-transport oracle) | 7-kill structural negative; native budget-Pareto optimal | `plan/frozen-pareto-negative-synthesis.md` (sealed) |
| 3 | **Factorization / joint-readout** as an accuracy lever | occupied + premise fails the 1-token control (speed, not accuracy) | CoDD 2603.00045, ADJUST 2509.22738, ADAS 2606.10829, DCD 2410.01949, EDLM 2410.21357, DEMASK 2604.02560; Codex KILL |
| 4 | **D1** diffusion-as-reasoning-tax / order audit | occupied | No-Compute-Left-Behind 2510.19990, Thinking-Out-of-Order 2601.22035, Beyond-Surface-Reasoning 2510.09544, Reasoning-or-Rationalization 2603.01190, APD 2506.00413, Parallelism-Generation-Order 2601.15593 |
| 5 | **D4** verifier-free within-trajectory self-revision | occupied (≥7 papers) | ReMDM 2503.00307, Self-Correcting-MDM 2602.11590, Decoupled-Self-Correction 2601.06428, ME-DLM 2605.09603, Targeted-Remasking 2605.26436 (fixes 59.4% last-mile corruptions), Corrective-DLM 2512.15596 |
| 6 | **MoE denoising-time routing audit** (Pro's last lead) | architecturally vacuous (router has NO timestep input) + passive form is an identifiability wall (h fully downstream of t) already gate-failed; constructive H5 = Direction-C, banked in #2 | `plan/archive/h4-architecture-verdict-and-pivot.md` (project's own Opus audit) |

## Forbidden-assumptions for future cycles (do NOT re-attempt on this platform)
- Do NOT propose a joint-readout/copula/energy/selector/scheduler/remasking variant as a masked-diffusion math
  ACCURACY lever — occupied and the LLaDA ceiling is reason-bound.
- Do NOT attribute the LLaDA-8B MATH ceiling to the diffusion sampler — ~73% is base-model reasoning.
- Do NOT pose "DiffusionGemma experts specialize by timestep" — the router has no t input (vacuous) and the
  passive question is unidentifiable.

## What survives — NEW-GOAL pivots (NOT autonomous; surfaced for the user's next `/goal`)
These change the TASK or SUBSTRATE (a scope change the autonomous loop may not self-grant), so they are
recommendations, not actions taken:
- **(a) Non-monotonic CONSTRAINT tasks** (Sudoku / multi-hole code repair / structured infilling / proof-hole)
  where diffusion's bidirectional canvas may be *genuinely necessary* (Google's own DiffusionGemma guide uses
  Sudoku as the bidirectional/self-correction showcase). Partly probed (Parallelism 2601.15593 shows a Sudoku
  advantage) — needs a sharper open slice.
- **(b) Leave masked-absorbing diffusion** → uniform-state / continuous-embedded-flow (ELF 2605.10938,
  Scaling-Beyond-Masked 2602.15014). He-bar clean, but the He-line negative warns continuous has **no math
  headroom** (PPL/OWT scale) — a model-family build, not a 2×4090 minimal experiment.
- **(c) The diffusion-beats-AR DATA-EFFICIENCY angle** (Diffusion-Beats-AR-in-Data-Constrained 2507.15857,
  DLMs-are-Super-Data-Learners 2511.03276) — the one place diffusion reportedly *beats* AR is data-constrained
  pretraining, NOT reasoning. A different question (already partly published).

## Additional occupancy surfaced by the bank-confirmation (Codex)
- **MoE-diffusion beyond t-routing**: active and occupied (TEAM, EC-DLM) — constructive router changes become a
  trained-router/capacity-policy direction outside this banked lane.
- **Evaluation/measurement reform**: scope-shifted — LogicDiff's own results show 8-shot CoT lifts the baseline
  ~70% and removes the gap, so an eval-reform does not attack the *high-step* MATH ceiling here.
- **Trainable-LLaDA objective-alignment** (planner-aware training, learned unmasking, trajectory RL,
  consistency/introspective DLMs): the obvious "align training with diffusion decoding" space is already covered.

## Grade & provenance
- **Grade: scoped-negative** (NOT structural — no single pre-registered falsifier fired on a sealed holdout with
  live controls; it is a constraint-bound landscape conclusion / research-gate, not a theorem). Self-graded DOWN
  per §5.1; **independently confirmed** by Codex (adversarial premature-stop probe → BANK-AND-CONCLUDE).
- **Independent corroboration (5 substrates):** GPT-5.5-Pro ×2 (chats "Masked Diffusion LM审计" → C-minus;
  "开放式对抗性思维" → saturation) · Codex GPT-5.5 ×2 (factorization SELECT → KILL; bank-confirmation →
  BANK-AND-CONCLUDE) · the project's own H4 architecture audit (router has no t input). Web prior-art triangulation
  independent of Pro. Tree nodes 5.10.3 (factorization, pruned) + 5.10.4 (saturation synthesis, done).
- **NO GPU spent on any intervention** — every dispatch blocked pre-compute by the gates. Cost = OBSERVE
  measurement only (one native step-sweep, job bxwtegokx). This is the anti-Goodhart system functioning: it
  converted "a hot, crowded subfield" into a banked landscape negative instead of a wasted me-too training run.
