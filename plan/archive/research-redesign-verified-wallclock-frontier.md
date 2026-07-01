# Research Redesign #2 — "Verified Wall-Clock Scaling Frontier" (2026-06-27)

> Source: GPT-5.5 Pro (Pro 扩展) program-level redesign after BOTH original leads died (E killed, A-strong
> falsified — both independently Codex-validated). This SUPERSEDES the equivalence-class spine
> (`plan/research-redesign-equivalence-class.md`) as the PRIMARY direction. Pending Codex rigor + SELECT-confirm.

## The pivot (problem/setup change, NOT a continuation of E or A)
**Thesis:** *Frozen block-diffusion LMs are valuable, if at all, because they are FAST PROPOSAL GENERATORS for
verifier-scaled reasoning. The right observable is VERIFIED SUCCESS as a function of WALL-CLOCK COMPUTE, with a
matched AR sibling control.* The paper is no longer "look at the diffusion trace / likelihood"; it is **"what
does block diffusion actually BUY when the task has an exact verifier?"** Exploits the model's real advertised
distinction: parallel denoising over token canvases (a SPEED structure), not a better reasoning distribution.

## Sharp claim (the one top-venue-reachable contribution)
*For verifiable reasoning, the useful compute unit in a frozen dLLM is a completed, verifier-checkable
CANDIDATE, not an internal denoising trace. DiffusionGemma's only top-venue-relevant advantage over its
matched AR sibling is whether it moves the verified-success-vs-wall-clock frontier.*

## Novelty (vs the two crowded spaces)
- NOT another sampler/commitment paper (EB-Sampler, TraceLock, Fast-dLLM, Prophet, APD, AXON crowd the
  internal-unmask/commit space).
- NOT another likelihood/eval paper (DUEL exact-likelihood; Generative-Frontiers frontier-eval;
  Hacking-GenPPL). The novelty = **matched-family AR vs dLLM, same hardware/prompts/exact-verifiers/wall-clock**
  → isolates the inference ARCHITECTURE. Answers a question reviewers immediately grasp: *does this shipped
  frozen dLLM buy more correct answers per second than its AR sibling?*

## ★ FIRST EXPERIMENT — branch-vs-deepen, dLLM-vs-AR verified scaling frontier
Primary metric: **S(B) = Pr_{x∼D}[∃ y ∈ G_≤B(x): V(x,y)=1]**, B = wall-clock seconds/problem on the SAME
2×4090 box, G_≤B = completed candidates generated within budget B, V = math_verify / code-exec. Plot S(B) vs
**log wall-clock**.
Arms:
1. **DiffusionGemma BRANCH** — many independent 768- or 1280-token candidates.
2. **DiffusionGemma DEEPEN** — spend compute extending fewer candidates 768→1280.
3. **AR Gemma-4-26B-A4B sibling BRANCH** — same prompts, same max-token budgets, same parser/verifier, same
   hardware, fairly batched/tuned.
4. **static-N vs oracle** — static N samples/problem; oracle only as an UPPER BOUND (not a claim).
Datasets: **MATH-L5 + AIME-2024** (the headroom); for a serious submission add ONE hard verifiable set —
LiveCodeBench (code, exec-based, contest-fresh) or OlympiadBench / OlymMATH / Omni-MATH (math). Do NOT use
GSM8K/HumanEval/MBPP/MATH-500 as primary (ceiling).

### Pre-declared FALSIFIER (kill the top-venue program unless the first full run shows ≥1):
- **Frontier dominance:** DiffusionGemma has a statistically clear higher verified-success AUC over log
  wall-clock than the AR sibling on MATH-L5 (paired problem-level bootstrap CIs).
- **Practical speedup:** at fixed accuracy, DiffusionGemma reaches it at **≥2× lower wall-clock**; OR at fixed
  wall-clock gives **≥5 abs points MATH-L5** or **≥8–10 points aggregated AIME**.
- **Branch beats deepen:** marginal compute on additional independent candidates beats longer traces (except
  maybe the high-budget tail).
KILL if advantage <1.3×, only on the cherry-picked rescue set, disappears under matched wall-clock batching, or
depends on a verifier/parser loophole.

### Headline figure (2 panels)
- Panel A: verified solve-rate vs wall-clock s/problem — DiffusionGemma vs AR sibling, bootstrapped
  problem-level CIs.
- Panel B: within DiffusionGemma, branch-vs-deepen frontier ("more independent 768/1280 candidates" vs "extend
  fewer traces").
"That figure either gives you a paper or kills the program fast."

## Assets used (strongest first)
Generation harness, verifiers, the **AR sibling (`google/gemma-4-26B-A4B-it`, downloaded + smoke-tested)**,
sampler instrumentation, the **984-trace rescue dataset** (becomes motivation/diagnostic: rescue exists but
isn't selectively allocatable → the rational compute unit is the completed candidate). The D3PM scorer +
equivalence banks → APPENDIX, not center.

## Surviving findings → folded in (NOT the center)
- Noise-level dependence of reference observability = workshop/Findings unless heavily generalized (weak
  BestNLL→success correlation is damaging) → appendix / cautionary.
- "Rescue real but not allocatable" = strong cautionary section, weak standalone → motivation.
- Coherent story: "we tried trace-level adaptive compute (failed under controls); we tried
  likelihood/observability (fair sampler-band scoring removed the dramatic mismeasurement); the only object
  that moved task quality was outer-loop verified candidate generation."

## Q3 — framing
ABANDON "frozen DiffusionGemma as the scientific object"; KEEP it as a "proposal engine." Do NOT spend 2 weeks
on LoRA to the 26B denoiser/router (instability/contamination/reviewer-skepticism/benchmark-tuning optics).
Best light-adaptation pivot — ONLY after the wall-clock frontier is positive — = a **problem-level COMPUTE
ALLOCATOR** (inputs: prompt metadata, first-k completed candidates, answer-cluster counts, validity/parse
status, final entropy, NFE, length, dLLM-vs-AR disagreement; actions: stop / sample-more-dLLM / deepen-dLLM /
sample-AR; model: logistic/GBDT/tiny-MLP — NO trace-RNN, NO LoRA; baselines: static-N, entropy, NFE,
self-consistency, oracle). This directly answers the failed E: trace dynamics useless WITHIN-trace, but
final-candidate / problem-level signals may allocate OUTER-loop compute. If the wall-clock frontier is
NEGATIVE → pivot to harder tasks (LiveCodeBench/OlympiadBench/...), not adaptation.

## 2-week plan (Pro Q4)
- **Day 1:** freeze protocol (prompts, max lengths, sampling settings, parser, verifier, batch sizes, timeout
  rules, wall-clock measurement). Tune throughput on a small dev set only. Report s/problem, candidates/problem,
  tokens/sec, NFE.
- **Day 2 (CHEAP — existing 984 traces):** estimate pass@1/2/3 @768 & @1280, same-seed DEEPEN rescue vs
  independent-seed BRANCH rescue. Does "extend the same trace" even compete with "launch another candidate"? If
  branch already dominates deepen → the bridge from failed E to the new thesis.
- **Days 3–5 (decisive):** matched AR/dLLM frontier on MATH-L5 + AIME-2024, equal wall-clock, paired
  problem-level bootstrap. Kill criteria by end of Day 5.
- **Days 6–9:** add ONE hard verifiable benchmark only if Day-5 is alive (no easy benchmarks).
- **Days 10–12:** diagnostics (pass@N vs wall-clock to show time-normalized not sample-count cherry-picking;
  answer-clustering/diversity vs collapse; verifier FP audit; branch-vs-deepen; AR fair batching; optional tiny
  outer-loop allocator only after static curves are strong).
- **Days 13–14:** write around ONE claim. Title: *"Do Diffusion Language Models Buy More Verified Reasoning per
  Second?"*

## ★ v2 — CODEX-HARDENED BUILD CONTRACT (frozen; build to THIS) — SELECT-CONFIRM + PROCEED-TO-BUILD
> Codex (2026-06-27): PART 1 SELECT-CONFIRM (wall-clock frontier > noise-band measurement > E). PART 2
> PROCEED-TO-BUILD + 6 must-fixes. Also READ the 984 traces → early signal: **DEEPEN already > BRANCH** within
> dLLM (same-seed 1280 fixes 96/159 of 768-failures vs 35/159 for an extra 768 branch; 3-seed, underpowered,
> NOT wall-clock-normalized). ⇒ the "branch>deepen" falsifier is unlikely; the **dLLM-vs-AR wall-clock frontier
> is the real crux** (even if deepen wins within dLLM, does dLLM beat AR per verified-second?).

1. **WALL-CLOCK FAIRNESS (pre-condition before any headline number):** AR MUST use KV-cache (`use_cache=True`),
   batched prompts, bf16, SDPA/FlashAttention (vLLM if Gemma-4-MoE-compatible — currently `vllm`/`flash_attn`
   NOT importable → verify compat/install OR fall back to HF generate + SDPA, DOCUMENT which). Naive eager
   unbatched AR is DISALLOWED as a headline. dLLM uses batched parallel-canvas decode. Report BOTH serial
   per-problem latency AND saturated throughput; accept only if the conclusion holds across BOTH modes.
   Required metrics: engine/version, batch size, GPU mem, tokens/sec, candidates/sec, verifier time, s/problem,
   NFE/forward-steps, parse-fail rate. **Explicit KILL: dLLM advantage vanishes under matched AR batching.**
   (Note: dLLM ~50GB and AR ~50GB cannot both reside on 2×4090 at once → run dLLM arms, unload, run AR arms.)
2. **BRANCH/DEEPEN definitions (precise + fairly costed in NFE AND wall-clock):** Branch = independent full
   candidates, independent seeds, fixed budget cap. dLLM deepen = TRUE continuation 768→1280 if the harness
   supports it, else "longer-budget rerun" charged a FULL extra forward pass. **AR deepen MUST use KV-cache
   continuation 768→1280, NOT a fresh rerun** (else unfair to AR).
3. **DIVERSITY guard:** FREEZE temperature/top-p/top-k/seed schedule on a DEV set before any test run. Report
   canonical-answer unique-rate/problem. **pass@k computed over UNIQUE CANONICAL answers, not raw completions.**
4. **FALSIFIER thresholds:** ≥2× speedup = real. ≥5pts MATH-L5 needs CI (134 probs → ~7 problems, wide CI);
   **AIME-2024 = sign-check SECONDARY, not primary.** "branch>deepen" alone is NOT venue-sufficient unless
   cost-normalized with bootstrap CI. **Pre-declare B_min/B_max for the log-wall-clock AUC integration.**
5. **VERIFIER guards (mandatory, before build):** LOCK parser before generation; accept ONLY final
   boxed/final-answer extraction (never "gold appears anywhere"); canonicalize answers; fail ambiguous
   multi-answer outputs; dedup canonical answers before oracle/diversity stats; manually audit ≥20 verifier
   passes + ≥10 parse-fails before citing.
6. **DAY-2 diagnostic feasibility:** existing 984 traces (3 seeds) = a WARNING not a green light. Minimum
   upgrade for a decisive branch-vs-deepen verdict: **≥8 independent seeds/problem @768 AND @1280 on MATH-L5**,
   paired problem-level bootstrap CI, BATCHED wall-clock. Until then Day-2 is directional only.

**Single most-likely misleading result (Codex):** a FAKE dLLM speed win from under-optimized AR decoding.
Prevention: AR fast-path qualification is a HARD pre-condition + the explicit kill in fix #1.

## Harsh bottom line (Pro)
Without a clear verified-success-per-second win over the AR sibling, frozen DiffusionGemma is NOT a top-venue
paper in two weeks. The wall-clock frontier figure decides it fast — which is exactly what we want.
