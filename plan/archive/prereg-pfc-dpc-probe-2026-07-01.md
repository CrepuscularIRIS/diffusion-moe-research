# PREREGISTRATION — PFC DPC probe (Parallel Frontier Recoverability Contract) — 2026-07-01

> Sealed BEFORE the run. Arbor node 5.13.1.1. Gates whether PFC (Parallel Frontier Certificate training,
> plan/gpt55pro-parallel-frontier-certificate-2026-07-01.md) may proceed to training. Frozen forward passes
> only — no training. Metric = generation/verifier only.
> Object-shift-audit verdict = ELIGIBLE_FOR_BACK_HALF (all T1-T6 pass); audit concerns folded below.

## HYPOTHESIS
LLaDA-8B's math reasoning traces contain exploitable PARALLEL STRUCTURE: independent subcomputations
occupy predictable dependency layers, stabilize at denoising times correlated with dependency depth
(not just text position), and are conditionally recoverable from the problem + declared ancestors
(not requiring the full serialized prefix). This parallel structure is the substrate for PFC training.

## STAGES
- **Stage 0**: Validate certificate compiler on 20-30 MATH-500 DEV solutions (answer-preserving, locally
  checkable). GO gate: >90% of solutions yield valid certificates with correct final answers.
- **Stage 1**: Instrumented LLaDA-8B generation on 40 MATH-500 DEV problems at 128 steps, logging per-step
  top-1 predictions for stabilization-time computation.
- **Stage 2**: Full DPC analysis (Steps A-E, Step D REQUIRED per audit).

## FALSIFIERS (pre-declared — ANY ⇒ direction dead before training)
1. **Compiler fails**: <90% of correct LLaDA solutions compile to valid, answer-preserving certificates.
2. **No parallelizable mass**: PMASS < 0.25 (median, across problems with ≥5 atoms).
3. **Stabilization = text order**: ARNESS_resid (Spearman partial) > 0.6 after depth control.
4. **Ancestor-only recoverability bad** (Step D, REQUIRED): median Δprefix > 0.5 nats/token on independent
   result atoms (model can't predict sub-results from dependencies alone, needs serialized prefix).
5. **Peers help too much**: median |Δpeer| > 0.3 for independent atoms (same-layer peers are NOT independent).

## ACCEPTANCE (GO — all required for DPC_PASS)
PMASS ≥ 0.25 · ARNESS_resid ≤ 0.6 · compiler ≥ 90% · Δprefix ≤ 0.5 · |Δpeer| ≤ 0.3 for independents.

## METRIC
Per-step top-1 predictions (from instrumented generation), atom-level dependency structure, forward-pass NLL
under corrupted contexts. NO diffusion loss, NO reference-token agreement, NO verifier accuracy (this probe
measures the SUBSTRATE for training, not the training outcome).

## SPLIT
MATH-500 DEV (level-stratified, ~250 problems; use 40 for the DPC probe, 8 per level). Sealed holdout
untouched. The DPC is descriptive on frozen logs — no training, no evaluation on sealed data.

## MASK DISTRIBUTION (pre-registered as FIXED per audit)
If the DPC passes and training proceeds:
40% standard i.i.d. token masks · 25% whole-cell · 20% whole-layer · 10% ancestor-only · 5% merge/final.
These are FIXED and must NOT be tuned post-hoc.

## PLATFORM
LLaDA-8B-Instruct, conda env `llada`, 2×RTX-4090D. Generation at 128 steps, gen_length=512, block_length=64.
Verify model loads correctly with a simple probe before the full run.
