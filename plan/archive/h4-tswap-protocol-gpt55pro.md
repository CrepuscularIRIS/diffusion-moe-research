# H4 → interventional t-swap protocol (GPT-5.5 Pro, 2026-06-25)

**Source:** GPT-5.5 Pro (专业), ChatGPT chat "Diffusion-MoE Routing Analysis" (thought 7m36s).
Full transcript in that chat; this is the distilled, executable plan. Confirms the identifiability
wall and replaces the passive H4 test with an interventional + utility program.

## Verdict on passive logs (Q1) — DEAD, with a proof
- **Non-identifiability:** timestep bucket, call index, denoising progress, and hidden-state evolution
  are the SAME ordered variable in single-schedule logs. For any t-specialized alternative `s(Y|T_c)`
  there is a progress-only null `q(Y|P)=s(Y|f(P))` giving the identical observed distribution → for ANY
  test, power against that observationally-identical alternative is ≤ α. That IS the measured dichotomy
  (partition-changing null → inflated; partition-preserving → no power).
- **Conditioning on progress also fails** (positivity violation): once you condition on progress/call
  index, `Pr(T=t | progress, track) ∈ {0,1}` — a point mass; nothing left to test.
- Passive logs honestly support only the DESCRIPTIVE claim "routing drifts strongly over the denoising
  trajectory" (`I(Y;c|r,p)>0`). **Drop the 29/30 free-shuffle headline as causal evidence.**

## The reframe (the important move)
- **Descriptive H4** ("experts are denoising-STAGE specialized") — passive logs already support this.
- **Causal/router H4** ("the router would pick different experts if ONLY the timestep embedding changed
  while hidden state stayed fixed") — interventional only. This is a controlled-direct-effect question.
- **And H4 need NOT be t-specific to justify the router** (Q3): a t-conditioned router is worth building
  if timestep is a cheap stable proxy for denoising stage — UNLESS it's brittle under schedule changes,
  in which case progress/hybrid conditioning wins. The deliverable is UTILITY, not a p-value.

## EXPERIMENT 1 — router-only t-swap (controlled direct effect)
**Estimand (per layer ℓ):** `θ_ℓ = E[ d( R_ℓ(z_true, t'), R_ℓ(z_true, t_c) ) ]` — hold the exact router
input `z_true` fixed; change only the timestep value the router sees; measure routing change `d`.

**State capture (deterministic eval):** fixed seed, dropout off, no routing noise, **pre-capacity**
router logits (exclude batch/capacity-overflow artifacts). For each unit u=(traj,pos,call,layer) cache:
`h_pre` (hidden state BEFORE timestep-conditioned norm/modulation), `z_true` (exact router input after
true-t preprocessing), baseline logits over 128 experts, baseline top-8 set + gate dist.

**4-WAY LOCAL FACTORIAL — separates "router reads t" from "t-conditioned LayerNorm/scale" (critical):**
let `M_ℓ(h, t)` = timestep-conditioned preprocessing before router, `R_ℓ(z, t)` = router given input + router-t.
- `Y00 = R(M(h,t_c), t_c)` baseline
- `Y01 = R(M(h,t_c), t')`  → **D_R = clean router-read-t effect**
- `Y10 = R(M(h,t'),  t_c)` → **D_M = effect of t-conditioned norm/scale via the representation**
- `Y11 = R(M(h,t'),  t')`  → **D_F = full local t effect**
- If D_R≈0 but D_M/D_F large → router does NOT read t directly; routing changes because t changes the
  representation. (If the current router has no separable t input, Y01=Y00 by construction → can only
  test representation-mediated sensitivity, or evaluate a NEW router adapter.)

**Swap distributions (pre-registered):** same-t placebo (FALSIFIER, must be ≈0); adjacent-t (smoothness);
same-bucket-other-t (fine vs coarse phase); different-bucket / far-t with |Δc|∈{6,12,24,36} (stage-level);
random-other-t (global average — pair with the others to avoid mistaking off-manifold sensitivity).

**Routing-distance d:** top-k turnover `1-|S00∩S01|/8`; Jaccard; **gate TV** (preferred — top-k flips on
tiny margins); centered-logit displacement (catches sub-top-k + diagnoses tie-driven flips).

**Inference:** NO permutation surrogate (the intervention IS the counterfactual). Clustered bootstrap
(cluster by trajectory, ideally prompt/seed); maxT / simultaneous intervals across 30 layers. The key
output is the **causal effect curve θ_ℓ(|Δc|)** with same-t/adjacent/same-bucket/far baselines, not a p.

**Falsifiers:** same-t placebo ≠ 0 → contaminated/nondeterministic/capacity artifact; router-only swap = 0
while passive MI huge → passive was drift, not t-reading; effect only in Y10 not Y01 → it's norm/scale;
far swaps move routing but adjacent/same-bucket show no dose-response → off-manifold, not real specialization.

**GO threshold to justify a t-conditioned router — require ALL THREE:**
- A. router-only effect (far/diff-bucket): `θ_top ≥ 0.125` (≥1 of 8 experts changes) OR `θ_TV ≥ 0.05–0.10`.
- B. dose-response: `D_same ≈ 0 < D_adjacent < D_far`.
- C. utility (Experiment 2): a small router-adapter improves held-out objective ~0.5–1% rel, or equal
  quality with meaningfully better routing/load efficiency. (If t-swap is real but utility is null →
  H4 may be true but architecturally irrelevant.)

## EXPERIMENT 2 — crossed schedule × router-t utility (de-risks the whole direction)
**Step 1 — schedule-varied state bank:** cache hidden states under ≥2–3 schedules (normal 48-call,
compressed 24, expanded 96, warped early/late) so absolute timestep/noise-level and realized progress are
NOT aligned. Compute NON-tautological progress summaries (token entropy, change-rate vs prev call,
denoising-residual magnitude, hidden norm/PCA coordinate, confidence) — NOT bucket/normalized-call-index.
**Step 2 — re-route each cached state over a grid of router-t** (true/adjacent/same-bucket/diff-bucket/
early-mid-late) → same-state-different-t = t-effect; different-state-same-t = progress effect.
**Step 3 — compare 4 router variants** (train/adapt ONLY the router, freeze the rest): content-only `R(h)`,
t-conditioned `R(h,t)`, progress-conditioned `R(h,P̂)`, hybrid `R(h,t,P̂)`; eval on normal + warped schedules.

**Decision table:**
| result | interpretation | build |
|---|---|---|
| t-swap large; R(h,t) wins normal+warped | strong t-specific H4 | t-conditioned router |
| t-swap small; R(h,P̂) wins | progress-specific | progress-conditioned router |
| R(h,t) wins normal, fails warped | t is a brittle proxy | progress/hybrid |
| hybrid wins | both matter | hybrid router |
| none improves held-out objective | passive MI was descriptive drift | do NOT build around H4 |

## Recommendation (GPT-5.5 Pro)
Reframe the passive result as **strong denoising-stage routing drift** (descriptive), drop the passive
p-value headline, and make the **core H4 evidence interventional** (Exp 1) + **utility-grounded** (Exp 2).
