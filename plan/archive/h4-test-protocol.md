# H4 Test Protocol — "Do MoE experts specialize by denoising timestep t?"

> Statistical protocol for Direction C / hypothesis H4 on DiffusionGemma 26B-A4B.
> Designed by GPT-5.5 Pro (2026-06-24) after two adversarial Codex reviews killed
> the original max-JS-vs-bucket-0-CI test for (a) independent-per-layer shuffles,
> (b) too-weak FWER validation, (c) **broken token exchangeability** (position/
> canvas/prompt confound t). Authoritative raw transcript: `h4-test-protocol-pro-raw.txt`.
> This doc is the implementation spec AND the seed for the paper's methods section.

## 0. Pre-registered estimand (lock BEFORE seeing routing results)

**Claim (passive-log strength):** *For fixed prompt, generated canvas/trajectory, and
token position, the MoE routing distribution carries statistically reliable information
about the denoising timestep bucket.*

- α = 0.05.
- Track unit `i = (prompt_id, trajectory/canvas_id, position p)`.
- Timestep variable `b(t) ∈ {1..K}`, **K = 8** equal-count buckets (or equal-width in
  log-SNR if the schedule is nonuniform). **Do not tune K after seeing effects.** If
  multiple bucketizations are explored, fold the choice into the max-statistic correction
  or use a held-out pilot split.
- **Honesty caveat (must appear in the paper):** passive logs establish *within-trajectory
  timestep ASSOCIATION*, not causal "experts read the timestep embedding." A causal claim
  requires a **timestep-swap intervention** (freeze canvas state, replay router with a
  different t-embedding, test if expert selection changes). Phrase the passive result as
  "expert usage is conditionally time-aligned within fixed prompt/canvas/position tracks."

## 1. Null + exchangeability unit + permutation (the core fix)

**Per-visit expert mass** (primary = unweighted top-k): `Y_{rspLe} = (1/k)·Σ_q 1{E_{rspLq}=e}`,
k=8, so Σ_e Y = 1 per routed visit. (Gate-weighted + top-1 as robustness checks.)

**Null (per layer L):** `H_{0,L}: Y_{rspL·} ⊥ b_{rs} | (prompt, canvas, position)`, in the
randomization-inference form: the per-call slices are exchangeable w.r.t. the timestep
labels within a trajectory, conditional on r, p, routing vectors, missingness, and all
non-timestep metadata. Global null = ∩_L H_{0,L}.

**Permutation = TRAJECTORY-SYNCHRONOUS timestep relabeling:**
- For each trajectory/canvas r, draw ONE permutation `π_r ∈ S_{T_r}` of its denoising-call
  indices. Relabel `b^{(π)}_{rs} = b_{r,π_r(s)}`.
- Apply the **same π_r** to all positions p, all layers L, all experts/ranks/logits, all
  statistics. I.e. keep each whole decoder-call slice `{Y_{rspL·}: p, L}` intact and only
  reassign its timestep label.
- **Held fixed:** prompt/canvas/position ids, call index s, selected experts, ranks,
  logits/gate weights, all cross-layer + top-k + same-canvas/same-timestep correlations,
  missingness, checkpoint/config.
- **Why not independent per-(track) shuffles:** positions within one canvas at one timestep
  share the same denoising state/model call → NOT independent; independent shuffles
  fabricate datasets the block-diffusion process could not produce. Independent within-track
  permutation is only a *secondary sensitivity analysis*, never the primary claim.

**Validity:** product group `G = ∏_r S_{T_r}`. Under H0, conditional on the orbit
`{gD: g∈G}`, the observed labeling is uniform → randomization p-value
`p = (1 + Σ_m 1{M(g_m D) ≥ M(D)}) / (B_perm + 1)` is finite-sample valid + super-uniform.
Validity comes from exchangeability of the relabeling, NOT asymptotics — so the statistic
may be arbitrarily complex (max over layers, MI, etc.).

## 2. Statistic — track-stratified conditional MI / G (replaces max-JS)

Per track i=(r,p), layer L, bucket b, expert e: `C^{(L)}_{ibe} = Σ_{s: b_{rs}=b} Y_{rspLe}`.
Marginals `C^{(L)}_{i·e}`, `n_{ib} = Σ_e C^{(L)}_{ibe}`, `n_i = Σ_b n_{ib}`.

**Layer statistic (G / stratified LR):**
`T_L = 2 Σ_i Σ_b Σ_e C^{(L)}_{ibe} · log( (C^{(L)}_{ibe} · n_i) / (n_{ib} · C^{(L)}_{i·e}) )`
(terms with C=0 contribute 0; **no pseudocounts**). Equivalently `T_L = 2 N_L · I_L(E;B|track)`,
`N_L = Σ_i n_i`.

- **Do NOT use pooled expert histograms** (reintroduces prompt/canvas/position imbalance).
- **Do NOT use asymptotic χ²** p-values — calibrate by the permutation in §1/§3.
- Max-pairwise-JS is allowed only as a *post-hoc localization/visualization* statistic; if
  reported, fold its (L,b,b') hypotheses into the SAME joint max-statistic correction.

**Effect sizes (report these, not just a binary call):**
- `I_L(E;B|track) = T_L / (2 N_L)` (nats/visit); normalized `NMI_L = I_L / H(B|track)`.
- Bias-corrected excess `ΔNMI_L = (I_L^obs − median_π I_L^{(π)}) / H(B|track)` (MI is
  positively biased; subtract the permutation-null median).
- Cluster bootstrap over independent trajectories/canvases (or prompts), ≥2,000 resamples,
  for 95% CIs and permutation null bands across layers.

## 3. FWER correction — single shared permutation draw across all layers

`M(D) = max_{L=1..30} T_L(D)`. For each permutation m, compute ALL 30 layer stats using the
SAME trajectory-synchronous relabeling, `M^{(m)} = max_L T_L^{(m)}`.
- **Global p** = `(1 + Σ_m 1{M^{(m)} ≥ M_obs}) / (B_perm + 1)`; reject global null iff ≤ α.
- **Layer-wise single-step maxT:** `p_L^adj = (1 + Σ_m 1{M^{(m)} ≥ T_L^obs}) / (B_perm+1)`.
- Optional Westfall–Young step-down maxT (same draws) for more localization power, labeled
  secondary.
- **B_perm ≥ 9,999 (use 19,999 for the paper).**
- **One shared draw must feed all layers (and all bucket-pair stats). Never independent
  per-layer shuffles.** ← this is the exact bug that failed Codex review twice.

## 4. Validation (type-I + power) — must detect a 2× inflation

**Type-I, R_null = 5,000 (10,000 camera-ready), validate the FULL pipeline at α=0.05 (& 0.01):**
- **Null A (most important):** permutation-orbit null on REAL logs — relabel timesteps within
  each trajectory via the allowed group, treat as "observed," run the whole test. Preserves
  all real structure; FWER must be controlled if code is correct.
- **Null B:** generative heterogeneous-track null — sample expert mass from per-track baseline
  `q̂_{iLe} = C^{(L)}_{i·e}/n_i`, independent of bucket. Tests whether track heterogeneity
  alone causes false positives.
- **Null C:** autocorrelated no-specialization null (AR(1) within trajectory, constant
  marginal) — block diffusion has strong adjacent-timestep dependence. If full-shuffle inflates
  here, add pre-registered **block / circular-shift permutations** (block length from ACF) or a
  trajectory-level wild-cluster bootstrap as the autocorrelation-robust sensitivity test.
- **Pass criterion:** one-sided 95% Clopper–Pearson upper bound `U_0.95 ≤ 0.065` at α=0.05
  (MC SE ≈ 0.0031 at true 0.05 with R=5,000 → a true 0.10 is decisively rejected). Report the
  null p-value histogram + rejection rates at α∈{0.01,0.05,0.10}.

**Power:** planted-effect generator on real design — tilt `q_{iLbe}(δ) ∝ q̂_{iLe}·exp(δ g_b h_e)`
with early/late specialist sets A/B, sweep δ∈{0,.05,.1,.2,.35,.5,.75}, R_power=1,000. Report
global detection prob, planted-layer identification after maxT, ΔNMI distribution, 80%-power
effect threshold. Pre-declare the smallest meaningful effect or report the full power curve.

## 5. Required logged metadata (probe schema extension)

Current (layer, timestep, expert ids, record_id, token index) is INSUFFICIENT. Add:
- **Trajectory-level (once/canvas):** prompt_id (+text/tokenization hash), trajectory/canvas_id,
  final-output hash, seed, decode settings, total steps T, schedule, noise/log-SNR per step,
  checkpoint hash, config (30L/128E/top_k8/router type), precision, batch id+composition,
  capacity-factor settings, and **whether logged experts are pre- or post-capacity**.
- **Call-level (per denoising call):** trajectory_id, call_index s, exact t, bucket b(t),
  noise/log-SNR, canvas-state hash, skipped/truncated flag.
- **Visit-level (per call×position):** trajectory_id, call_index, t, position p,
  `visit_id = traj+call+p`, current token id, mask/noise status, padding/special/active flag,
  per-position confidence/entropy if exposed.
- **Routing-event-level (per visit×layer):** visit_id, layer, ordered top-k expert ids, ranks,
  selected logits, gate probs, full 128 logits if feasible, router temp/noise,
  **pre-capacity selected experts** (primary), post-capacity dispatched experts + overflow flag,
  `event_id = visit_id+layer`.
- **Primary test uses PRE-capacity router top-k** (post-capacity carries batch-load artifacts).

## 6. Block-diffusion pitfalls (handled above)

1. Position visited repeatedly → longitudinal track, never IID tokens.
2. Same-canvas positions correlated → trajectory-synchronous relabeling (not per-position).
3. Adjacent timesteps correlated → coarse buckets + autocorrelated-null validation +
   block/circular-shift sensitivity; cluster-bootstrap CIs; no causal claim w/o intervention.
4. Load-balancing/capacity → use pre-capacity choices; else log overflow + sensitivity reruns.
5. Token state evolves with t → phrase as "time-aligned within tracks"; intervention for causal.
6. Bucket choice = hidden multiple testing → pre-register K=8 (or fold into max-stat).
7. Sparse expert-bucket cells → fine; permutation-calibrated, no pseudocounts, no asymptotic χ².

## 7. Pseudocode

End-to-end reference implementation (build per-visit expert mass → stratified-G per layer →
trajectory-synchronous permutation generator → shared-draw null across all layers → global +
layerwise maxT p-values → effect sizes) is in `h4-test-protocol-pro-raw.txt` §"End-to-end
pseudocode". Implement `direction_c/h4_test.py` (+ probe/persistence schema extension) against it.
