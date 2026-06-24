# Novelty / Prior-Art Audit — Diffusion MoE (2026-06-24)

> Source: Playwright → ChatGPT DeepResearch (10 min, **21 sources, 406 citations**),
> chat "Novelty Audit for ML". This is the pre-GPU originality check (research-goal
> §6 Check 6 / peer-review reviewer R3), run **before** any compute investment.
> Conducted by an independent engine (GPT-5.5 DeepResearch), so it is isolated from
> the Opus main loop per the science protocol.

---

## 0. Bottom line (3 verdicts)

1. **Direction A / contribution (1) — "learned commitment policy via trajectory RL"
   — is in HIGH-OVERLAP territory.** Two near-frontal hits appeared in the last ~6
   months, one **two days before this scan**. The *method category* (lightweight
   policy on a (frozen) dLLM, trained with GRPO/RL, reward = correctness + steps)
   is taken. GSPO-vs-GRPO is an implementation detail, not a novelty source.
2. **Direction C / contribution (2) — "explicit timestep-conditioned router in a
   diffusion *language* MoE" — is the DEFENSIBLE novel slice.** No language paper
   found that feeds t into the router itself. **This validates the C-first ordering.**
3. **Thesis "L2 dominates L1" must be SOFTENED.** It collides head-on with CoDD,
   which argues the factorization barrier (L1) is real and cheaply fixable. CoDD/APD
   must become controlled baselines, not hand-waved.

---

## 1. Overlap map (closest prior art, with arXiv IDs)

| Work | arXiv | Overlap w/ (1) learned commitment | Overlap w/ (2) t-aware MoE routing | Audit verdict |
|------|-------|-----------------------------------|------------------------------------|---------------|
| **SAS / "Scheduling Thoughts"** | 2606.23567 (**2026-06-22**) | **LETHAL**: frozen denoiser + lightweight order policy + GRPO + language tasks; any-order + semi-AR | none | **(1)'s most dangerous overlap — must single-section differentiate** |
| **Learning Unmasking Policies for DLMs** | 2512.09106 | **Near-frontal**: MDP over masked-diffusion sampling, lightweight policy on pretrained dLLM, GRPO, reward = correctness+steps | none | **(1) major threat; differ only by commit-vs-remask + target model** |
| **RemeDi** (Self-Reflective Remasking) | 2509.23653 | **High (functional)**: low-confidence tokens re-masked; Remask SFT + Remask RL | none | Bakes remask **into the backbone** (vs our frozen-backbone external controller) — must differentiate if we claim remask |
| **Fast-dLLM** | 2505.22618 | **Direct**: confidence-threshold parallel decoding = the hand-crafted rule we'd replace | none | Cite + compare as the heuristic baseline |
| **APD** / **Learn2PD** | 2506.00413 / 2509.25188 | High: learned/adaptive parallel-decode policy; Learn2PD ≈ lightweight filter on frozen model | none | Weaken "learned controller" novelty; cite |
| **d1 / DCoLT-LLaDOU / TraceRL / DiffuCoder** | 2504.12216 / 2505.10446 / 2509.06949 / 2506.20639 | RL on dLLM for reasoning/code (mostly optimize the **model**, not a frozen-model sampler) | none | Cite — kills "diffusion LM + RL + verifiable reward" as a new point |
| **EC-DLM** | 2604.01622 | none | **High**: expert-choice routing + **timestep-dependent expert capacity** in a DLM | **(2)'s most dangerous prior — but it tunes *capacity*, not t-as-router-input** |
| **TEAM** | 2602.08404 | none | Medium: exploits routing temporal consistency across denoising levels (inference-time activation/caching) | Cite as near neighbor; not t-conditioned training |
| **LLaDA-MoE** | 2509.24389 | none | Base: scratch-trained sparse-MoE diffusion LM | Cite as MoE-dLLM base |
| **Vision MoE: DiT-MoE / DiffMoE / Diff-MoE / eDiff-I / EC-DiT** | (various) | none | **Strong conceptual**: expert-by-timestep preference, noise-level capacity, expert-specific t-conditioning, stage-split denoisers — but in **vision** | Cite as conceptual ancestors of (2) |
| **CoDD** | 2603.00045 | none | none | **Strongest counter to the L2>L1 thesis** — factorization barrier real, cheap tractable-inference fix; must be a controlled baseline |
| **SDTT / LSD / ECDM** | 2410.21035 / 2509.19962 / 2512.12889 | Neighbor: diffusion distillation / learned few-step samplers (distillation route, not frozen-model verifier-RL) | none | Method neighborhood, not full overlap |
| **dInfer** | 2510.08666 | "decoding strategy" as a first-class optimization object | serves MoE-dLLM inference | Systems prior |
| **Block Diffusion (BD3-LMs)** | 2503.09573 | Defines the block-diffusion regime we target | none | Core setting prior — must cite |
| **LLaDA / LLaDA2.0** | 2502.09992 / 2512.15745 | Base dLLM family; LLaDA2.0 = AR→dLLM conversion + MoE variants | LLaDA2.0 shows MoE+block-diffusion at scale, no explicit t-router | Cite as closest family |
| **Dream / Dream-Coder / DreamOn** | 2508.15487 / 2509.01142 / 2602.01326 | Context-adaptive noise reschedule; verifiable-reward RL post-train; length-control state machine | none | "Sampling matters" + controller-style decoding priors |
| **DiffusionGemma official** (model card / dev guide / DeepMind) | — | **Very high**: 26B/3.8B-active MoE, 256 canvas, entropy-bounded denoising, renoising of unselected tokens, adaptive stopping — *exactly* the hand-crafted sampler we'd replace | **Very high**: it *is* the target block-diffusion MoE | Must cite; basis for the frozen-backbone audit. (No formal PDF found — official materials only.) |

---

## 2. Defensible novel slice (the claim to make)

**Do NOT claim:** "first to replace hand-crafted unmask/commit schedule with a learned
controller trained by trajectory-level RL." → eaten by Learning Unmasking Policies + SAS.

**DO claim (compressed):**
> On **block-diffusion MoE language models**, a **revocable learned commitment
> controller** + an **explicit timestep-conditioned language-MoE router**, evaluated by
> **frozen-denoiser controlled experiments** that quantify *how much of the
> diffusion-vs-AR quality gap is recoverable by inference-control alone* on verifiable
> structured tasks.

Four load-bearing qualifiers (each is a defensibility boundary):
1. **block-diffusion MoE / DiffusionGemma** — a production-grade *public* MoE, not a
   generic masked dLLM. Mainstream learned-scheduling papers don't target this.
2. **revocable commitment** — the controller decides whether *already-committed* tokens
   are **revoked and re-masked**, with the backbone **frozen** (vs unmask/order policies
   in Learning Unmasking Policies / Adaptive Order / SAS; vs RemeDi which trains remask
   into the backbone). External, reversible decision layer on a frozen model.
3. **explicit t-conditioned router in a diffusion *language* MoE** — claim narrowly:
   *first to feed t directly into the router (logits/dispatch depend on t) in a language
   diffusion MoE, plus a mechanistic study of whether experts already self-specialize by
   t.* NOT "first t-aware MoE in diffusion" (vision did it); NOT "first t-aware expert
   allocation in dLLM" (EC-DLM did capacity).
4. **audit framing, not a pure method paper** — see §4.

Title candidates:
- *Revocable Commitment Control for Block-Diffusion MoE Language Models*
- *Disentangling Scheduling and Factorization in Block-Diffusion MoE via Frozen-Backbone Verifier RL*
- *Timestep-Conditioned Routing for Diffusion Language MoE with Frozen Commitment Control*

---

## 3. Full-overlap verdict

- **Contribution (1):** "largely already done" if defined as *frozen denoiser + lightweight
  controller + trajectory RL + verifier reward*. SAS is the closest to full overlap.
  Remaining space = revocable commitment + DiffusionGemma/block-diffusion-MoE target +
  audit framing. Method-level novelty alone is **not** defensible.
- **Contribution (2):** **no fully-same-topic language paper found.** EC-DLM (capacity) and
  TEAM (inference temporal consistency) are near priors; vision MoE has conceptual
  ancestors. "First explicit t-conditioned router in a diffusion language MoE + expert-
  specialization-by-t analysis" is **narrow but defensible.**

---

## 4. Recommended pivots (re-frame, do not delete)

**Pivot 1 — recenter (1) on "revocable commitment under block-diffusion MoE"**, demoting
"learned scheduling" to an implementation detail. Strongest comparison set: Fast-dLLM,
Learn2PD, Learning Unmasking Policies, SAS, RemeDi.

**Pivot 2 — recast the paper as an empirical L1-vs-L2 dissection.** Minimum **three
frozen-backbone control arms**:
- (a) controller/scheduler only,
- (b) factorization correction only (CoDD-/APD-type dependency fix),
- (c) both.
If (a) recovers most of the gap and (b) matters mainly in few-step regimes → thesis is
persuasive. If (b) dominates → a valuable counter-result. **This maps directly to H1**
and gives H1 a clean, publishable design either way.

**Pivot 3 (best) — bind (1)+(2) into ONE story: denoising-stage compute allocation.**
- early noisy steps → broader / exploratory routing;
- late low-entropy steps → specialized / constrained routing;
- controller decides commit/revoke, router decides *who* handles this timestep's tokens.
Turns "two loose ideas" into one unified thesis about stage-wise compute allocation in
language diffusion — not yet written for language diffusion (vision has ancestors).

---

## 5. Softened thesis (replaces the flat "L2 > L1")

> On verifiable structured tasks, a **substantial fraction** of the diffusion-vs-AR gap is
> recoverable by **learned inference control on a frozen block-diffusion MoE**;
> factorization corrections (CoDD/APD) remain an **important competing explanation and
> control**, especially in few-step regimes.

---

## 6. Must-cite-and-differentiate (front-of-paper, not buried in related work)

- **(1):** Fast-dLLM (2505.22618), Learn2PD (2509.25188), Learning Unmasking Policies
  (2512.09106), **SAS (2606.23567)**, RemeDi (2509.23653).
- **RL background:** d1 (2504.12216), DCoLT/LLaDOU (2505.10446), TraceRL (2509.06949),
  DiffuCoder (2506.20639), Dream-Coder (2509.01142).
- **Thesis (L1 vs L2):** CoDD (2603.00045), APD (2506.00413), DiffusionGemma official.
- **(2):** LLaDA-MoE (2509.24389), TEAM (2602.08404), EC-DLM (2604.01622), + vision
  Diff-MoE / DiffMoE / DiT-MoE / eDiff-I.
- **Setting:** Block Diffusion (2503.09573), LLaDA (2502.09992), LLaDA2.0 (2512.15745).

---

## 7. Implications for the Arbor run (review debt → next IDEATE)

- **[CONFIRMS] C-first ordering.** Direction C (t-aware routing + the H4 specialization
  study) is the defensible novel slice. The C1 toolchain (H4: do experts specialize by t?)
  is exactly the mechanistic study that grounds (2). Keep C as the spearhead.
- **[REFRAME, not kill] Direction A.** Recenter on *revocable* commitment + frozen-backbone
  audit; add the CoDD/APD factorization-correction control arm (Pivot 2 = H1 design).
- **[SOFTEN] thesis** per §5. **Recommendation only** — do NOT silently rewrite
  `plan/diffusion-moe-first-principles-framing.md`; surface to user for ratification.
- **[ADOPT] Pivot 3** as the paper spine (stage-wise compute allocation) — pending user
  ratification; strongest single-story framing.
- **[CITE] sealed list** in §6 — populate the tree `related_work` fields.
- **Caveat:** simulated DeepResearch ≠ exhaustive. Re-run a novelty scan before any merge
  of a novel claim (Check 6), and especially watch SAS / EC-DLM follow-ups.
