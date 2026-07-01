# PREREGISTRATION — UP-1 v2: Bounded Sibling-Pair SC Oracle Kill-Test (Test A)

> SEALED CONTRACT (tree node 5.9.5.2). Frozen 2026-06-30 BEFORE any build/GPU. The DECISIVE go/no-go for
> the SC-target adapter axis. Designed by Pro 扩展 (chat "SC-target oracle策略分析") after the v1 one-step
> oracle-clamp was banked as a confounded `failed-attempt` (tree 5.9.5.1). De-confounds v1: final-accuracy
> outcome (not one-step logP) + native/state-level-aligned teachers (not gold-reference wording) + profile-
> matched nulls. No post-hoc metric/scope edits.

## 0. One-line question
On a frozen near-ceiling dLLM, does injecting a verified-CORRECT native fork's scrubbed self-conditioning
clean-estimate into a verified-WRONG fork's run (from the SAME saved EB state) **causally rescue the FINAL
verified answer**, MORE than profile-matched wrong/random nulls? If even this best-case oracle can't, the
SC-target oracle→head line is dead.

## 1. Hypothesis
- **H1:** Acc(A=scrubbed-CORRECT) − max(Acc(Cw=scrubbed-WRONG), Acc(Cr=scrubbed-RANDOM)) ≥ 10–15pp on final
  verified accuracy over mined sibling-pair frontiers, problem-clustered.
- **H0 (kill):** A does not exceed the matched nulls by the margin → the SC channel has no correctness-specific
  causal leverage even as a future-aligned oracle → the trained-head bet is not worth pursuing.

## 2. Design (Test A; bounded; NO training)
**Unit = sibling-pair frontier** (the de-confound):
1. Run native EB generation; save the sampler+canvas+hidden state at a frontier t₀≈0.6 (t∈[0.5,0.7]).
2. From that SAME saved state, fork K=8–16 native continuations (common-random-number controlled).
3. Keep a frontier ONLY if it yields ≥1 final-verified-CORRECT fork AND ≥1 final-verified-WRONG fork.
   - τ+ = a verified-correct fork (the oracle teacher; native/state-aligned by construction).
   - τ− = a verified-wrong fork (same-problem wrong null).
   - τr = an unrelated trajectory (random null), profile-matched.

**Arms** (each = inject the arm's scrubbed SC clean-estimate at the decision steps of the WRONG fork's run,
then COMPLETE the generation to the final answer; verify with the SAME math_verify):
- `A`  = scrubbed-CORRECT (τ+'s SC clean-estimate, scrub mask M).
- `Cw` = scrubbed-WRONG (τ−'s SC clean-estimate, scrub mask M, profile-matched to A).
- `Cr` = scrubbed-RANDOM (τr, scrub mask M, profile-matched to A).
- `cached native / no-op` — only to confirm the selected wrong-baseline state (NOT a primary contrast).

**Outcome:** `Y = 1[final answer verified-correct after full continuation]`. One-step logP is DROPPED.

## 3. Matched-null discipline (the v1 lesson — non-negotiable)
Per frontier t, per injected position/block, A/Cw/Cr MUST share: same scrub mask M_{i,t}; per-position/block
L2 norm; clean-estimate entropy; top-1 margin / sharpness; affected-position set; injection schedule; extra
NFE / hook overhead; common random numbers for the continuation. (If A is sharp at a position, Cw/Cr equally
sharp; if A heavily scrubbed, Cw/Cr equally.) Otherwise the test measures disruption, not correctness.

## 4. Pre-declared KILL (any one fires → kill the SC-target axis, pivot)
- Δ = Acc(A) − max(Acc(Cw), Acc(Cr)) < 10–15pp (problem-clustered).
- A "wins" only at the one-step logit but not at the final answer.
- A random/profile null rescues ≥ A.
- Answer-region-mask (hard-mask the final-answer / boxed region SC components) collapses A's gain → it was an
  answer-attractor injection, not reasoning leverage.
- sample-K mining needs an uneconomically large K to find sibling pairs (the "target factory" doesn't hold).
- PILOT FAIL: in N=16, A does NOT achieve ≥6–7 A-only wins with max-null ~0–1.

## 5. PASS = a CAUSAL UPPER BOUND only (NOT a license to train)
A clean pilot pass (A ≥6–7/16 A-only wins, max-null ~0–1, Δ≥10–15pp) only proves the SC channel CAN be
causally steered by a correct teacher. It does NOT prove a deployable head. Gating ladder (each must pass
before the next):
- **Test A** (this) → causal-channel upper bound. Then expand to 50–60 independent problem-level frontiers.
- **Test B — online predictability:** train a small head, PROBLEM-HELDOUT, input = deployment-visible state
  only (prompt, current canvas, hidden state, native SC, randomness-so-far — NOT the future). Check (i) ẑ
  predicts (z+ − z−) above null (cosine/contrastive/R²); (ii) injecting ẑ beats Cw/Cr on final accuracy. If
  oracle A wins but learned ẑ does not → oracle LEAKAGE, not leverage.
- **Test C — answer-leak audit:** probe whether the final answer is decodable from the injected SC carrier;
  whether answer-region-masking collapses the effect; whether only the answer-bearing component is effective.
- Only after A+B+C pass → train the head; SEALED AIME used ONCE at the very end (never for mining/tuning/selection).

## 6. Data (non-sealed; harder regime — L5 is smoke-only)
Mine sibling pairs on a HARDER non-sealed set, native pass@1 in the 40–70% band: NuminaMath-1.5 (offline in
cache) preferred; Omni-MATH / OlympiadBench math-text if obtainable offline. NEVER AIME (sealed; final eval
only). Feasibility precheck is INTRINSIC: if 100–200 hard problems × K=8/16 can't yield ≥16 (pilot) clean
paired frontiers, the target factory doesn't hold → that itself is the kill.

## 7. Integrity / engineering
- Shard guard `integrity()` 7+5→12 at load. Run UNBUFFERED (`conda run --no-capture-output` + `python -u -X
  faulthandler`) — NO `conda run` buffering, NO systemd-scope wrapper (both caused the v1 false-"hang").
- Metrics generation/verifier-based (final math_verify). Diffusion loss never a signal.
- Build base: psc-oracle / sc-oracle-clamp worktree; reuse model load + EB sampler + SC pre-hook + verifier +
  the scrubber + the profile/matched-null machinery from stage0a.py; build-new: fork-from-saved-EB-state +
  full-gen-to-verified-answer + NuminaMath loader + the borderline-frontier miner. CPU unit tests (26B never
  loaded in tests).
- Budget: bounded; ONE 26B job (nvidia-smi first); ≤3h dev; measure-first auto-reduce N; kill-9 on overrun /
  >30min zero-output (watch the UNBUFFERED log).

## 8. Preregister hash
Freeze SHA256 at dispatch into tree + RUNLOG; no edits after.
