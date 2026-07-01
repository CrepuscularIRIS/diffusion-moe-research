# Novelty audit — interventional/constructive router framing (DeepResearch, 2026-06-25)

**Source:** DeepResearch via Playwright (thought 6m37s), chat "Diffusion MoE Novelty Audit".
Refines the 2026-06-24 audit for the PIVOTED (post-identifiability-wall) framing.

## Verdict: NOVEL & defensible — but ONLY framed narrowly. NOT pre-empted.
Sell it as **causal + schedule-invariant router-conditioning analysis for diffusion-LANGUAGE MoEs**,
NOT as "timestep-aware MoE for diffusion" (that's pre-empted).

**Best claim wording (DeepResearch):** "We provide the first causal and schedule-shift analysis of
whether diffusion-language MoE routers directly use denoising-time information, and show when expert
allocation should condition on nominal timestep, denoising progress, or both."

## Closest prior art (cite + differentiate)
| Paper | What | Overlap |
|---|---|---|
| **EC-DLM** arXiv:2604.01622 (2026) | expert-choice routing in DLMs; timestep-dependent expert CAPACITY as fn of mask ratio; code released | **CLOSEST.** Pre-empts "timestep-dependent compute in DLM-MoE". Does NOT do the causal t-swap or t-vs-progress schedule-shift identification. |
| **TEAM** arXiv:2602.08404 (2026) | temporal-spatial consistency of MoE-dLLM expert activation → ~1.9× accel | observes routing consistency across denoising levels; acceleration, not causal |
| **MoDE** arXiv:2412.12953 (ICLR'25) | noise-conditioned expert routing for diffusion *policies*; compares noise-only vs token-only routing | strong NON-language overlap; pre-empts "noise-conditioned routing in diffusion MoE" broadly; no DLM, no frozen-h causal, no schedule-shift |
| **Diff-MoE** (ICML'25) | time-aware + space-adaptive experts for DiT | strong vision overlap; pre-empts "time-aware diffusion MoE experts"; no causal router readout |
| **DiT-MoE** 2407.11633 (2024) | DiT-MoE scaling; expert-selection-by-timestep heatmaps | pre-empts CORRELATIONAL "specialization by timestep" (vision); not causal |
| Switch-DiT 2403.09176; DTR (Denoising Task Routing, ICLR'24); eDiff-I 2211.01324 | stage-specialized denoisers / channel routing | foundational stage-specialization; broad |
| Causal audit of expert importance 2606.10703 (2026); Probing Semantic Routing 2502.10928 (EMNLP'25 Findings) | causal/interventional router analysis (token-level) | METHOD overlap only; not diffusion t/progress swapping |

## What is pre-empted (do NOT claim as firsts)
- "Diffusion experts specialize by timestep/noise." (eDiff-I, DTR, Switch-DiT, DiT-MoE, Diff-MoE, MoDE)
- "Timestep/noise-aware routing improves diffusion." (MoDE, Diff-MoE, Switch-DiT, DTR)
- "DLM-MoE compute should vary across denoising steps." (EC-DLM, TEAM)

## Reconciliation with the architecture finding (CRITICAL)
- DeepResearch's strongest novel claim (freeze-h, swap-only-router-t causal probe) needs **a router WITH
  a t-input**. Our feasibility audit proved **DiffusionGemma's router has NO t-input** (routes purely on
  noised content). DeepResearch independently corroborates: "I did not find… an explicit claim that the
  router itself is conditioned on timestep/noise/progress."
- → So "base diffusion-LM MoE routers do NOT use denoising-time, and passive specialization-by-t is
  non-identifiable" is itself a **novel empirical + methodological finding** (the paper's motivation).
- → The realizable novel CORE = the CONSTRUCTIVE program: ADD t/progress/hybrid conditioning to the
  router, measure held-out utility under SCHEDULE SHIFT; the causal swap-t audit then applies to the
  AUGMENTED router (does it actually use t, and does that generalize under schedule shift).

## Differentiation angles (make it defensible)
1. Causal router t-swap audit on a router WITH explicit t_router (freeze h, swap t) — top-k overlap, gate KL/JSD, load shift, downstream delta.
2. Upstream-confound control — swap t upstream (h changes via norm/scale) → separates "router reads t" from "representation already encodes t".
3. Timestep vs progress vs hybrid routers, tested under CHANGED denoising schedules (nominal t and progress de-align).
4. **Progress must NOT be only mask ratio** (else EC-DLM too close) — use remaining-mask fraction, accepted-token fraction, entropy/confidence reduction, commitment rate, hidden-state stabilization.
5. **Utility, not interpretability** — show the causal diagnosis predicts which router generalizes / improves held-out likelihood/quality/FLOPs under schedule shift. "A pure heatmap paper is much easier to reject."

## Main reviewer risk + answer
Risk: "EC-DLM already studies timestep-dependent expert allocation; MoDE/Diff-MoE already condition on
noise/timestep." Answer: those study architectural/resource benefits; **we study the causal mechanism
(does the router directly read t vs react to a t-transformed representation) and which variable
generalizes under denoising-schedule shift** — in a diffusion *language* model.

## EC-DLM deep-read (full PDF 2604.01622, 2026-06-26) — differentiation CONFIRMED + a design risk found
**What EC-DLM actually does:** (1) argues Expert-Choice (EC) routing > Token-Choice (TC) for DLM-MoE
(deterministic load balance, 2× faster training); (2) because EC expert CAPACITY `c` is an external
knob, schedule it by denoising step — `k(r)`, r=mask ratio; **finding: give MORE CAPACITY to LOW-mask-
ratio (late) steps** (linear-reverse scheduler wins; mech: low-mask steps learn ~7-20× faster); (3)
retrofit pretrained TC DLMs (LLaDA-MoE) to EC by swapping ONLY the gate → faster convergence + better
GSM8K/HumanEval/MedQA.
**Our differentiation is REAL and orthogonal:**
- EC-DLM conditions **CAPACITY** (how many tokens per expert) on t. We condition the **routing DECISION**
  (the per-token expert SCORES, via `+g(emb(t))`) on t. EC-DLM never adds a t-term to the router scores
  → the two mechanisms are ORTHOGONAL. Our question ("should the routing DECISION depend on t?") is
  genuinely unasked by EC-DLM.
- EC-DLM is on **EC** routing; DiffusionGemma (our model) is **TC** (top-8/128). We study decision-
  conditioning in the DEPLOYED TC model — a different axis from the EC/capacity one.
**DESIGN RISK this read surfaced (act on it):** EC-DLM's t-signal IS the mask ratio `r`. In our D3PM-
uniform SFT, the sampled scalar `t~U(eps,1)` ≈ the realized corrupted-token FRACTION (mask ratio) — they
differ only by ~binomial noise (~0.03 std at 256 tok). So **Arm B (t-scalar) ≈ Arm D (mask-ratio-as-t)**
→ the "B beats D" EC-DLM-killer is WEAK in our single-corruption setup (Codex already hinted this). →
**REFRAME:** the PRIMARY result is **B vs A** (does decision-conditioning on the denoising step help at
all, capacity-matched?); the EC-DLM differentiation is CONCEPTUAL (decision vs capacity, TC vs EC) made
in related-work + framing, NOT a "B beats D" number. Keep D as a minor robustness arm, do not over-claim.
**Also noted:** EC-DLM evaluates Answer-EM on GSM8K for LLaDA-MoE (their generation eval works) — a hint
that our broken DiffusionGemma generation eval is fixable and/or LLaDA-MoE is an alternative testbed.
