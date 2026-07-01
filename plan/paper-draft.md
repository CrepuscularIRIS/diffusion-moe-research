# Do Diffusion Language Models Buy More Verified Reasoning per Second?

*A verified wall-clock scaling-frontier study of a frozen block-diffusion LM vs its matched autoregressive sibling.*

**Status:** workshop/Findings-tier draft (2026-06-28). Scope: one benchmark domain (MATH level-5), one shipped
matched-family model pair, one HF-vs-HF serving stack on 2×RTX 4090. Generality (more benchmarks, vLLM-served
AR, second hardware) is explicit future work. All claims are generation/verifier-based; every experiment was
pre-registered with falsifiers and independently re-checked (Codex GPT-5.5: AUCs recomputed from raw).

---

## Abstract
For verifiable reasoning the deployment-relevant utility is neither tokens/sec, pass@k, nor single-reference
likelihood — it is **verified correct answers per wall-clock second**. We define the *time-to-first-verifier-
correct* frontier S(B)=Pr[∃ completed candidate y within wall-clock budget B : U_x(y)=1] and evaluate it on a
**shipped matched-family pair**: frozen DiffusionGemma 26B-A4B (block masked discrete-diffusion MoE) and its
autoregressive sibling Gemma-4 26B-A4B-it, under identical hardware, prompts, exact verifier, batching and KV
cache. On MATH level-5, at a **fair, accuracy-matched budget** (2048 tokens, where the AR sibling is no longer
truncation-limited and the two models reach equal per-candidate accuracy, 0.823 vs 0.836), the diffusion model
**dominates the verified wall-clock frontier**: frontier-AUC advantage 1.79 (throughput) / 1.80 (serial),
bootstrap 95% CI excluding 0; **6.7× serial / 5.4× throughput** speedup to matched accuracy; ~5.3× more verified
answers per second. A decomposition S(B)≈mean_i[1−(1−p_i)^⌊rB⌋] shows the advantage is driven by
candidate-*arrival-rate* r (the diffusion model emits a checkable answer in ~44 model invocations / ~770 tokens
vs the AR model's ~1068 sequential tokens), **not** by per-candidate correctness p. We further show, via two
pre-registered companion negatives, *why* this is the right thing to measure: (i) a learned trace-dynamics
adaptive-compute controller carries no exploitable signal (the rational unit is the completed candidate, not the
internal trace), and (ii) off-policy reference-token likelihood is a noise-regime artifact (the realistic
denoising band recovers it). A learned compute allocator does **not** beat the trivial "just run the largest
budget" policy (a perfect oracle gains ~1%), so the result is a measurement+mechanism contribution, not a method.
We are explicit that this is a *deployment* comparison (both models HF-served; a vLLM-served AR could narrow the
throughput gap — the serving-independent component is the diffusion model's lower forward-pass *depth*), not a
causal architecture ablation.

---

## 1. Introduction
Three quantities are commonly reported for diffusion LMs and dismissed as decisive: **tokens/sec** (a throughput
proxy that ignores correctness), **pass@k** (ignores wall-clock), and **single-reference token likelihood /
diffusion loss** (we show it is regime-dependent and a poor quality proxy). The quantity a practitioner with an
exact verifier (math, code) actually cares about is **how quickly a verifier-correct answer arrives**. We make
that the object of study: the verified wall-clock frontier S(B), on the two checkpoints a user can actually
choose between today — a shipped block-diffusion LM and its same-family AR sibling.

Contributions: **(C1)** the S(B) verified-wall-clock-frontier metric and an arrival-process decomposition;
**(C2)** a ratified result — the diffusion model dominates the frontier at a fair, accuracy-matched budget;
**(C3)** the mechanism — the edge is candidate arrival-rate (forward-pass depth), not accuracy; **(C4)** a
clean negative — there is no exploitable compute-allocation headroom (just run the largest budget); **(C5)**
two companion negatives that motivate the metric (trace-adaptive compute fails; reference-likelihood misleads).

## 2. Setup
**Models.** DiffusionGemma 26B-A4B-it (Gemma-4 block masked discrete-diffusion MoE; 256-token canvas; ~48-step
EntropyBoundSampler with adaptive early-commit; t∈[0.4,0.8]) vs Gemma-4 26B-A4B-it (AR), the matched-family
sibling. Both frozen, bf16, 2×RTX 4090, identical prompts. **Verifier:** `math_verify` on the final `\boxed{}`
answer, identical and symmetric across models (audited: when a model commits a boxed answer it is almost never
wrong; failures are genuine no-box truncations — AR@2048: 336 pass / 8 boxed-wrong / 50 no-box).
**Serving fairness (HF-vs-HF).** AR uses HF `generate` with KV-cache + SDPA + left-padded batching (vLLM /
flash-attn are not importable for this MoE → documented; naive eager-unbatched AR is never used). The diffusion
model uses its shipped block-parallel sampler; batching *hurts* it (early-stop stragglers), so batch=1 is its
best throughput (no batching credit — conservative vs the batched AR). **Data.** MATH level-5 (134 problems),
seed-matched seeds {7,42,123}; budgets {768,1280,2048} tokens. **Pre-registration.** Falsifiers frozen before
scoring; a clean kill counts as success.

## 3. The metric and its decomposition
**Metric.** S(B)=Pr_x[∃ completed candidate within per-problem wall-clock B : verifier=1], on a log-B axis;
we report frontier AUC, fixed-accuracy speedup, and fixed-wall-clock Δ, with paired problem-cluster bootstrap CIs,
in BOTH serial-latency and saturated-throughput modes.
**Arrival-process model.** Treating candidates as i.i.d. arrivals, S(B)≈1−(1−p)^⌊rB⌋ with arrival-rate r
(candidates/sec) and per-candidate correctness p. The homogeneous (pooled-p) form fits poorly (RMSE 0.08–0.32);
the **per-problem-p mixture** S(B)≈mean_i[1−(1−p_i)^⌊rB⌋] fits well (RMSE 0.03–0.16). For small p the low-budget
frontier is governed by **r·p**, not tokens/sec — so a diffusion model wins only when its arrival-rate gain
beats any per-candidate-accuracy loss.

| arm | p (acc/cand) | pass@all | no-box | r serial (c/s) | r tp | NFE (fwd) | len (tok) |
|---|---|---|---|---|---|---|---|
| dLLM 768  | 0.560 | 0.664 | 0.418 | 0.266 | 0.266 | 32.1 | 637 |
| dLLM 1280 | 0.801 | 0.896 | 0.124 | 0.212 | 0.212 | 41.4 | 742 |
| **dLLM 2048** | **0.823** | 0.918 | 0.060 | 0.198 | 0.198 | **44.5** | 771 |
| AR 768    | 0.368 | 0.455 | 0.632 | 0.045 | 0.108 | 708 | 708 |
| AR 1280   | 0.719 | 0.769 | 0.274 | 0.034 | 0.061 | 924 | 924 |
| **AR 2048**   | **0.836** | 0.888 | 0.144 | 0.030 | 0.037 | **1068** | 1068 |

At the fair 2048 budget p is matched (0.823 vs 0.836) while the diffusion model's arrival-rate is **6.7× higher
(serial)** and it uses **~24× fewer forward-pass invocations** (44.5 vs 1068). *Honest accounting:* a diffusion
canvas-pass is not free — it costs ~3.6× a single AR cached step on this hardware — so the fair, observed claim
is the **6.7× serial / 5.4× throughput** wall-clock speedup, not "24× cheaper compute." The forward-pass-*depth*
reduction (~24× fewer sequential model invocations) is the serving-independent root of the advantage.

## 4. Main result — the diffusion model dominates the verified wall-clock frontier
**Frontier-AUC advantage Δ(dLLM−AR) over log wall-clock (paired problem-cluster bootstrap 95% CI):**

| budget | serial Δ | tp Δ | regime |
|---|---|---|---|
| 768  | 1.67 [1.44, 1.91] | 1.14 [0.97, 1.32] | AR truncation-limited |
| 1280 | 1.90 [1.76, 2.04] | 1.53 [1.40, 1.64] | AR truncation-limited |
| **2048** | **1.80 [1.69, 1.91]** | **1.79 [1.66, 1.91]** | **FAIR (matched, non-truncated)** |

All six CIs exclude 0 — the diffusion model dominates at every budget, **including the fair 2048 budget in both
serial and throughput modes** (the make-or-break check: the win does not vanish under matched AR batching).
At @2048, both reach ~0.83 accuracy but the diffusion model gets there **6.0–9.1× faster (serial) / 4.3–8.3×
(throughput)**; per-verified-second 0.163 vs 0.031 (≈5.3×, tp). **Branch vs deepen:** spending budget on longer
single candidates beats more short candidates — Δ(branch@768 − deepen@1280) AUC = −0.41 [−0.53, −0.29].
*Figure 1* (FIGURE_data.json): Panel A solve-rate vs log wall-clock, dLLM vs AR @{768,1280,2048}×{serial,tp};
Panel B branch-vs-deepen.

## 5. No compute-allocation headroom (clean negative)
A natural follow-up is a compute-optimal outer-loop allocator (how many candidates × which budget × model
routing). On this data it is a **clean negative**: a cross-fitted learned router is *worse* than the trivial
"always run diffusion-deepen@2048" policy (ΔAUC −0.16 [−0.28, −0.06]); a **perfect per-problem oracle** beats it
by only **~1%** (ΔAUC 0.030 [0.016, 0.049]). There is essentially nothing to allocate — deepen@2048 is
near-Pareto-dominant per problem (scoped to this 6-action grid / 3 seeds / MATH-L5). This *simplifies* the
practitioner takeaway ("just run the largest budget") and is reported as a bound, not a method.

## 6. Companion negatives — why this is the right thing to measure
**(a) Trace-dynamics adaptive compute fails.** A learned risk-ranker over the diffusion trace (entropy decay,
churn, renoise, commit dynamics) carries no exploitable signal for *where* to spend budget: within the
truncation-risk set it ranks below random, ties simple controls, a real temporal-shuffle ablation ties, and it
adds nothing over the sampler's own effort counter even when allowed it. *Implication:* the rational compute
unit is the completed, verifier-checkable candidate — not the internal trace. (This motivates the candidate-
arrival framing of §3.)
**(b) Reference-token likelihood is a noise-regime artifact.** Teacher-forced per-position agreement with the
gold reference appears catastrophically low (~3%) *only at the maximum-noise step (t=1.0), which lies outside the
sampler's deployed band [0.4,0.8]*. Under the realistic band, an oracle equivalence-class reference bank recovers
token observability (top-10 → 0.99) and the residual non-predictivity of reference-NLL for verifier success is
weak and task-dependent. *Implication:* off-policy reference-likelihood / diffusion-loss is the wrong observable;
on-policy verified success is right — exactly the metric of this paper.

## 7. Related work and the surviving novel slice
Every *ingredient* is crowded — repeated-sampling-and-verify (Self-Consistency; Large Language Monkeys; Snell
et al. compute-optimal TTS), diffusion-LM throughput (Fast-dLLM, EB-Sampler, dLLM-Serve), matched AR-vs-diffusion
reasoning (SDAR — closest; mirrored-checkpoint causal study; I-DLM; DreamReasoner), diffusion code-gen (Beyond
Autoregression), and measurement critiques (DUEL, AXE/CTC, MBR, Hacking-Generative-Perplexity). To our knowledge
**no prior work reports the matched-family, exact-verifier, time-to-first-verifier-correct frontier S(B) with a
branch/deepen decomposition on a shipped sibling pair**. We do **not** claim a causal architecture theorem
(SDAR's mirrored-training design owns that territory); we claim a **deployment** comparison of two checkpoints a
user can choose between, with the *correct-answers-per-second* utility and its r·p decomposition as the
contribution. The branch axis (pass@k) is pre-empted; the novelty is that the diffusion architecture changes the
wall-clock *arrival rate* of verifier-correct candidates.

## 8. Limitations and future work
Single benchmark domain (MATH-L5), single matched pair, single HF-vs-HF serving stack, 3 AR seeds (6 for the
diffusion model at ≤1280). The wall-clock gap is amplified by the AR model's HF pipeline-parallel throughput
ceiling — a **vLLM-served AR** (tensor-parallel, continuous batching) could narrow the *throughput* gap; the
*serving-independent* advantage is the diffusion model's lower forward-pass depth. The diffusion model also
*trails* the AR sibling on raw benchmark quality (per the official card) — the win is specifically the wall-clock
frontier in the exact-verifier branching regime, not raw quality. **Generality phase (to reach top venue):**
AIME-2024/25/26, LiveCodeBench, OlympiadBench; a vLLM-served AR baseline; a second hardware node; 6-seed AR; a
`math_verify`-version manifest. We release the harness, verifier, raw traces, and seeds.

---
### Reproducibility / artifacts
Harness, verifiers, analysis, frontier/bootstrap code + raw per-(problem,seed,budget) traces: branch
`worktree-agent-aa411b381a8c95d40` (`3e873bd`, wall-clock frontier) and `worktree-agent-a84989eee7761a7e0`
(`8b33d0c`, decomposition+allocator). Companion negatives: `worktree-agent-a8574f53f824af3f1` (trace-adaptive,
E), `worktree-agent-a32f81c50e13c165b` (equivalence-class saturation, A). Independent validation: Codex GPT-5.5
recomputed all headline AUCs from raw. Design/novelty: `plan/archive/research-redesign-verified-wallclock-frontier.md`,
`plan/archive/gpt55pro-novelty-wallclock-2026-06-27.md`.
