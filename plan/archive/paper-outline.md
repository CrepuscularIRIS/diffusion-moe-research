# Paper Outline — "Known but Slow to the Wrong Place / Verified Reasoning per Second" (DRAFT, 2026-06-27)

> Consolidates the whole diffusion-MoE run. Built from: the RATIFIED wall-clock-frontier result (tree 5.8,
> branch worktree-agent-aa411b381a8c95d40@3e873bd), the E-kill (5.7.1) + A-falsification (5.1.2), Pro's
> redesign + AC review + novelty audit, and Codex's ratification-with-caveats. Working draft; the allocator
> section is conditional on node 5.8 allocator subagent.

## Title (candidates)
1. **"Do Diffusion Language Models Buy More Verified Reasoning per Second?"** (primary — matches the claim)
2. "Correct Answers per Second: A Verified Wall-Clock Frontier for Frozen Diffusion vs Autoregressive LMs"

## One-paragraph thesis
For verifiable reasoning, the deployment-relevant utility is not tokens/sec, pass@k, or single-reference
likelihood — it is **verified correct answers per wall-clock second**. We define the time-to-first-verifier-
correct frontier S(B)=Pr[∃ completed candidate y within wall-clock B : U_x(y)=1] and, on a SHIPPED matched-
family pair (frozen DiffusionGemma 26B-A4B block-diffusion vs its AR sibling Gemma-4 26B-A4B-it), show the
diffusion model dominates this frontier at fair (non-truncated, accuracy-matched) budgets — driven by a
candidate-arrival-rate (NFE/token-depth) advantage, decomposable as S(B)≈1−(1−p)^⌊rB⌋ governed by r·p, not
tokens/sec. We provide the decomposition, a compute-optimal allocator, honest serving caveats, and two
companion negative results that motivate the metric.

## Contributions (claims, each backed)
C1. **The metric.** Verified-success-vs-wall-clock frontier S(B) as the right deployment utility for
    exact-verifier reasoning (vs tokens/sec / pass@k / TPF / reference-likelihood). [novel framing]
C2. **The result.** On MATH-L5, frozen DiffusionGemma dominates the S(B) frontier vs its matched AR sibling at
    the FAIR @2048 budget (AR non-truncated, acc 0.836≈0.823): ~5.3×(tp)/~6.5×(serial) verified-correct/sec;
    frontier-AUC Δ tp 1.79 CI[1.66,1.91], serial 1.80 CI[1.69,1.91] (Codex-recomputed). Holds in BOTH serial &
    throughput. [ratified]
C3. **The mechanism (decomposition).** S(B)≈mean_i[1−(1−p_i)^⌊rB⌋] (per-problem-p MIXTURE; pooled-p fits
    poorly). The dLLM edge is candidate-arrival-rate r, NOT per-candidate-correctness p (matched at 2048,
    0.823 vs 0.836). ★ HONEST framing (Codex): dLLM uses ~24× fewer forward-pass INVOCATIONS (~44 vs ~1068),
    but per-pass compute is NOT equal (one dLLM canvas-pass ≈ 3.6× an AR cached step) → the FAIR claim is the
    OBSERVED **6.7× serial / 5.4× throughput** wall-clock speedup in candidate arrival, NOT "24× cheaper
    compute." Branch vs deepen: deepen>branch. [allocator subagent Part 1, Codex-ratified-with-caveats]
C4. **The compute-allocation bound (clean NEGATIVE — method layer is DEAD).** A learned outer-loop allocator
    is significantly WORSE than always-dLLM-deepen@2048 (ΔAUC −0.16 CI[−0.28,−0.06]); a PERFECT oracle beats
    it by only ~1% (ΔAUC 0.030 CI[0.016,0.049]) → no exploitable allocation headroom on this grid/3-seed/
    MATH-L5: "just run deepen@2048." Scoped bound, not a universal impossibility. [allocator Part 2, falsifier
    fired, Codex-ratified] → NOT a method paper; the simplification IS a result.
C5. **Two companion negatives that motivate the metric** (the project's earlier rounds, reframed):
    (a) trace-dynamics adaptive compute does NOT work (E-kill) → the rational unit is the completed candidate,
        not the internal trace;
    (b) reference-token observability is noise-regime-dependent (A-falsification) → off-policy likelihood
        probes mislead; on-policy verified success is the right observable.

## Section plan
1. Intro — deployment utility = correct-answers/sec; the three things people measure wrong (tokens/sec, pass@k,
   reference-likelihood); our frontier + matched-family shipped pair.
2. Setup — frozen DiffusionGemma 26B-A4B (block masked diffusion MoE, 256-canvas, EB-sampler) vs Gemma-4
   26B-A4B-it (AR); 2×4090; exact verifiers (math_verify+\boxed{}); MATH-L5 (+ AIME/LiveCodeBench in v2).
   FAIR-budget protocol (per-budget no-box/truncation control); HF-vs-HF serving fairness (both KV-cache+SDPA,
   no vLLM); pre-registered falsifiers.
3. Metric & decomposition — S(B), AUC_logC, time-to-50%; the r×p arrival-process model (C3 figure).
4. Main result — Figure 1: S(B) dLLM-vs-AR @{768,1280,2048}×{serial,throughput}; the fair-budget dominance;
   branch-vs-deepen panel. (C2)
5. Allocator (C4, conditional).
6. Companion negatives (C5): trace-adaptive-compute fails; reference-observability is regime-dependent.
7. Related work / novelty (the NOVEL-ONLY-WITH-X positioning): differentiate vs SDAR (matched-family but no
   S(B); owns causal-ablation → we claim DEPLOYMENT not architecture theorem), DiffusionGemma card (quality+
   speed separate; trails on raw quality → our win is the wall-clock frontier in the branching regime),
   Large-Language-Monkeys/Snell (branch+verify pre-empted → novelty = the dLLM arrival-rate), Fast-dLLM/
   EB-Sampler/dLLM-Serve (throughput not verified-frontier), I-DLM, Beyond-Autoregression (code, pass@k not
   S(B)), DUEL/AXE/MBR (measurement).
8. Limitations / honest caveats — deployment not causal (SDAR); vLLM-served AR could narrow THROUGHPUT (NFE
   gap is structural); 3-seed AR, MATH-L5-primary; DiffusionGemma trails on raw quality.
9. Reproducibility — harness, verifier version manifest, raw traces, seeds.

## Venue (Codex-calibrated 2026-06-27): BELOW NeurIPS/ICML main-track AS-IS (one benchmark domain, one model
## pair, one HW/serving stack, and the allocator method-layer is DEAD). Workshop / Findings / COLM / ML-systems-
## eval-track now. TOP-VENUE path is open ONLY after the GENERALITY phase: AIME-25/26 + LiveCodeBench +
## OlympiadBench, a vLLM-served AR baseline, and ideally a 2nd hardware node. (Multi-day GPU + infra commitment.)

## Remaining work to submission (the "X")
- [running] Allocator + r×p decomposition on existing data (node 5.8 subagent).
- [GPU, next] Hard benchmarks: AIME-2024/25/26, LiveCodeBench (fresh), OlympiadBench — the generality the
  novelty audit requires (lead with the frontier on code, not pass@k).
- [GPU, next] Systems robustness: batch/prompt/KV warm-cold sweeps; a vLLM-served AR comparison (the key caveat).
- [cheap] 6-seed AR @1280/2048; record math_verify version manifest.
- Write §3–§4 from the ratified numbers; assemble figures from FIGURE_data.json.
