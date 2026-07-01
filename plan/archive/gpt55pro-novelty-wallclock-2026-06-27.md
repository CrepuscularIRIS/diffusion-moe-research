# GPT-5.5 Pro — Novelty/Prior-Art Audit: Verified Wall-Clock Frontier (2026-06-27)

> Source: Playwright→GPT-5.5 Pro, chat "Novelty Audit for dLLM". Verdict on the wall-clock-frontier claim.

## ★ VERDICT: NOVEL-ONLY-WITH-X
**No exact pre-emption found** of the precise experiment (matched-family SHIPPED dLLM/AR pair, same hardware/
prompts, EXACT verifier, the **S(B) = time-to-first-verifier-correct frontier over wall-clock budgets**, with
branch-vs-deepen separated). BUT the broad version is heavily crowded — reviewers can cite prior work for every
INGREDIENT except the exact combination. Surviving slice is real but NOT enough as "DiffusionGemma is faster on
AIME"; it needs a **compute-allocation / decomposition** contribution.

**X (required for top-venue) = exact S(B) verifier-success frontier + branch/deepen decomposition + a
compute-optimal outer-loop allocator + robust systems controls.** Without X → pre-empted as "dLLM throughput +
sample-and-verify benchmarking" (workshop/Findings/eval-track tier).

## Closest pre-emptions (differentiate explicitly)
- **SDAR** (Synergistic Diffusion-AutoRegression) — MOST DANGEROUS: controlled AR-vs-block-diffusion from a
  shared Qwen3-30B-A3B checkpoint (mirrored training → causal attribution), reports AIME-24/25, LiveMathBench,
  LiveCodeBench-v5/v6, majority/pass@k, TPF, tokens/sec. BUT does NOT report S(B) (time-to-first-verified per
  wall-clock) on a shipped matched sibling. SDAR OWNS the causal-architecture-ablation territory → we must NOT
  claim a causal architecture theorem; claim a DEPLOYMENT comparison of two shipped siblings.
- **DiffusionGemma model card** — already compares DiffusionGemma 26B-A4B vs Gemma-4 26B-A4B on standard
  benchmarks + speed, but quality & speed SEPARATELY (not the frontier). ★ IMPORTANT: the card shows
  DiffusionGemma TRAILS Gemma-4 on AIME-2026-no-tools & LiveCodeBench-v6 quality while claiming higher gen
  speed → our "win" must be specifically the WALL-CLOCK FRONTIER (speed compensating for lower quality in the
  exact-verifier BRANCHING regime), never raw quality.
- **I-DLM** (Introspective DLM) — DLM matching same-scale AR quality + better serving (AIME-24, LCB-v6); not
  DiffusionGemma, not S(B), no branch/deepen.
- **Beyond Autoregression** (dLLM code-gen empirical) — 9 dLLMs vs AR on HumanEval/MBPP/LCB, exec oracles,
  pass@k + tokens/sec; but pass@k & throughput SEPARATELY (not S(B)), and DISABLES KV-cache for fairness
  (differs from our deployment-style fair batching). Strongest pre-emption for the future LiveCodeBench part.
- Efficiency (Fast-dLLM/v2, EB-Sampler, dLLM-Serve [RTX4090!]) = throughput yes, verifier frontier no.
- Test-time-scaling (Self-consistency, **Large Language Monkeys** [branch/pass@k kill-shot], Snell
  compute-optimal, When-to-Solve-When-to-Verify) → BRANCH + verification is PRE-EMPTED; novelty must be that
  the dLLM ARCHITECTURE changes the wall-clock ARRIVAL RATE of correct candidates, not pass@k.
- ParallelBench etc. = parallel decoding struggles on sequential reasoning (a rebuttal asset, not pre-emption).

## ★ Sharpest defensible novel slice
"First matched-family DEPLOYMENT evaluation of a shipped open-weight block-diffusion reasoning LM and its
matched AR sibling on exact-verifier reasoning/code, measuring the full wall-clock time-to-first-verifier-
correct frontier S(B) and decomposing branch-vs-deepen under identical hardware/prompts/verifier/batching/cache."
→ The PAPER's core = treat candidate generation as an ARRIVAL PROCESS: S_m(B)=Pr[min_j T_correct ≤ B];
**S(B) ≈ 1−(1−p)^⌊rB⌋** ⇒ a dLLM wins only when its candidate-arrival-rate speedup r beats its per-candidate-
correctness loss p; for small p the frontier ≈ **r·p**, NOT tokens/sec. THAT decomposition is the contribution.

## Kill-shots → rebuttals (have data for each)
A "sample+verify solved" → those treat the generator as a black box & scale abstract compute; they don't test
whether a diffusion generator changes the wall-clock arrival rate vs a matched AR sibling (DiffusionGemma even
TRAILS on quality, so the winner = product of r×p×completion-time). B "throughput documented" → tokens/sec is
the WRONG utility; correct-answers/sec (S(B)) is the missing coupled quantity. C "wall-clock impl-dependent" →
report S(B) + decomposition (candidate/sec, correct/candidate, verifier time, length, NFE) across batch/prompt
sweeps; HF-vs-HF fair, vLLM-AR caveat. D "matched-family ≠ causal" → claim DEPLOYMENT choice, not architecture
theorem (cede causal to SDAR). E "parallel decoding struggles on sequential reasoning" → makes the win MORE
interesting (wins via branching DESPITE reasoning limits = exactly our thesis).

## Path to top-venue (the X, concrete)
1. The S(B) frontier metric (AUC, time-to-50%, low/high-budget regimes, bootstrap CIs/benchmark) — ✓ HAVE (MATH-L5).
2. Branch vs deepen — ✓ HAVE (deepen wins).
3. The r×p arrival-process decomposition (candidate/sec, correct/candidate, length, NFE) — write it up from data.
4. A learned/calibrated OUTER-LOOP compute allocator (how many candidates, how long each, AR-vs-dLLM routing),
   calibrate on MATH-L5 → transfer to AIME/LiveCodeBench — NEEDED (this is the method layer).
5. Hostile systems appendix (warm/cold KV, batch+prompt sweeps, quantization, verifier-time in/out, ≥1 more HW
   if feasible) — NEEDED.
6. Hard exact benchmarks: AIME-2024/25/26, OlympiadBench/MATH-L5, fresh LiveCodeBench — NEEDED (code more
   pre-empted → lead with the frontier there, not pass@k).
Negative-result tier: a strong negative ("parallel-canvas decoding improves candidate arrival but not depth;
value entirely mediated by r×p; quality gaps can erase raw speedups") is still publishable (workshop/Findings/
eval), stronger with the allocator + decomposition.
