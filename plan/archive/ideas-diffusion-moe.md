# Ideas — diffusion-moe (research-ideation campaign, 2026-06-26)

> Multi-engine ideation (超高 novelty / 专业 design / Codex rigor+select). STOPS at a ranked
> falsifiable shortlist; executing a winner is separate. Engines: DeepResearch DEPRECATED → 超高.

## Stage 0 — BRIEF (frame)
**Target claim space:** close the diffusion-vs-AR quality gap on VERIFIABLE tasks (code/math/structured)
for **DiffusionGemma 26B-A4B** (block discrete-diffusion MoE LM; TC router, top-8/128, 30 layers; 2×4090
bf16). The 3-layer gap: L1 factorization barrier (mitigated by block diffusion) · **L2 heuristic sampling
= the biggest gap** · L3 post-training immaturity. Levers: A sampling/commitment · B SFT-corruption ·
C trajectory-RL · D timestep-aware MoE routing.

**Current frontier (this session's evidence):**
- *Known / working:* SFT pipeline works (held-out diffusion loss 3.62 vs 7.66 pretrained). **Held-out
  DIFFUSION LOSS (forward pass) = the working metric** (the block-diffusion GENERATION eval is broken —
  0.0 incl. pretrained — parked). H5 (decision-level t-conditioned router) = **POSITIVE 1-seed** (B 4.30 <
  A 4.71, capacity-matched; t-ablation confirms); 3-seed verifying now.
- *Tried-and-dead (don't re-tread):* passive specialization-by-t (H4) = NON-identifiable (denoising-trend
  confound; free-shuffle fwer=1.00). t-swap on the FROZEN model = VACUOUS (router has NO t-input). The
  additive-t-on-gate MECHANISM = pre-empted (TimeStep-Master 2503.07416, MoDE ICLR'25, M3ViT NeurIPS'22).
  EC-DLM (2604.01622) owns timestep-CAPACITY scheduling. Learned-commitment policy = HIGH-OVERLAP (SAS
  2606.23567, learning-unmasking-policies 2512.09106).
- *Open frontier:* L2 sampling/commitment/remasking/REVOCATION policy (differentiated from SAS); MoE-routing
  innovations SPECIFIC to the parallel NON-CAUSAL denoising structure (cross-position / cross-step routing
  coordination — not per-token-per-step content routing); cross-domain mechanisms (control theory, sequential
  decision-making, ECC, search/SAT) mapped onto iterative denoising.

**Goal anchor / what a GOOD idea looks like:** a falsifiable, cheap-to-test (held-out diffusion loss or a
small fixable harness), MDP-framed lever on L2 or D, with an ORACLE upper bound + an honest causal caveat,
runnable on a FROZEN or lightly-adapted 26B (2×4090), small high-info probe over big training, each with a
pre-declared falsifier (+ negative control, equal-compute, holdout).

---
## Stage 1 — LANDSCAPE (3 Explore agents)
**SOLVED:** SFT (diff loss 3.62<7.66); held-out-diffusion-loss metric; H5 1-seed positive.
**TRIED-AND-DEAD:** passive H4 (trend confound); t-swap (no router t-input); additive-t-on-gate mechanism
(TimeStep-Master/MoDE/M3ViT); learned-commitment RL (SAS 2606.23567 + 2512.09106 pre-empt); thesis L2≫L1
(CoDD 2603.00045 counter); vision t-routing.
**CROSSED-DOMAIN tools (ranked transferable):** ① SPRT/optimal-stopping (commit-vs-keep as sequential test;
breaks: tokens interdependent) ② belief-propagation/iterative-decoding (denoise = message-passing; breaks:
loopy fully-connected, marginal≠joint) ③ anytime/adaptive-budget (reallocate steps easy→hard tokens) ④ MPC
rollout-lookahead ⑤ CDCL/SAT (commit=assignment, conflict→remask) ⑥ bandits (position=arm) ⑦ draft-verify
⑧ Kalman.
**RECENT FRONTIER:** adaptive-unmasking = HOT+CROWDED (LearningUnmaskingPolicies ICML'26 2512.09106, LESS
2606.16908, ADAS, SAS); parallel-decode HOT (ReFusion, DAPD 2603.12996 dependency-aware, cond-indep-testing
2510.21961); **MoE-routing-for-diffusion = the HOTTEST GENUINELY-OPEN frontier** → cross-token routing
COORDINATION (route jointly across the canvas, not per-token-independent — NOBODY does it), position×difficulty
expert specialization, ProbMoE-style capacity-free; test-time "rewrite-until-correct" exploiting revisability
(Prism 2602.01842, Stitching 2602.22871); theory: confidence-decoding provably-efficient (2603.22248).

### THE BINDING CONSTRAINT (shapes everything): held-out DIFFUSION LOSS is a MARGINAL per-token, teacher-forced
forward-pass metric. It CAN see ROUTING/representation changes that improve per-token denoising (H5's B<A proved
this) but CANNOT see SAMPLING/COMMITMENT-policy quality, JOINT coherence, or generation — those need the (broken)
generation eval. → two families: (i) ROUTING/architecture levers measurable NOW via diffusion loss; (ii) SAMPLING/
COMMITMENT/test-time levers that REQUIRE fixing the generation harness first (high-leverage enabler).

## Stage 2 — PROBE BLOCK
- **Q1 First principles (bottleneck class):** TWO bottlenecks. (a) ROUTING/representation — experts are assigned
  per-token-independently, ignoring the non-causal canvas structure (the MoE differentiator; H5 showed routing
  moves the loss). (b) STOPPING/CREDIT-ASSIGNMENT — commitment uses MARGINAL confidence per token/step, ignoring
  joint coherence + sequential structure (the L2 gap; but needs generation to measure). Evidence: H5 B<A (routing
  matters); frontier = commitment crowded, routing-coordination open; diffusion loss is marginal.
- **Q2 Hidden assumption:** "routing is per-token-independent" → drop it: tokens COORDINATE expert choice across the
  canvas (open). AND "commitment = marginal confidence threshold" → drop it: sequential/joint stopping (SPRT/BP).
- **Q3 Elephant:** the cheap metric (diffusion loss) is MARGINAL → blind to the JOINT coherence that IS the quality
  gap; the metric that sees it (generation) is BROKEN. Fixing the harness is the highest-leverage unblock.
- **Q4 Hamming:** the defensible MoE slice = cross-token routing COORDINATION (most-open, MoE-specific, diffusion-
  loss-measurable, distinct from EC-DLM-capacity + t-decision). The biggest QUALITY lever = L2 commitment, gated
  on the harness fix. Pursue both: routing-coordination NOW (cheap, measurable), harness-fix to unlock L2.

## Stage 2 — CANDIDATES (9, from 3 isolated Opus generators) + CHECKPOINT

**THEME 1 — cross-token ROUTING COORDINATION (diffusion-loss-measurable NOW; MoE-specific; open frontier):**
- **R1 · Routing-consensus (BP on gate logits)** [G1-A]. axiom: gate is a per-position independent argmax of
  W·h_i. mechanism: insert `g'_i=(1−α)g_i+α·Σ_j w_ij g_j` (w=confidence×attention-similarity) before top-k —
  confident neighbors pull NOISED positions toward locally-consistent experts; train α+kernel only, experts
  frozen. hyp: noised positions have uninformative h_i → mis-route; borrowing routing evidence corrects it.
  obs: held-out marginal CE Δ≤−0.05 nats AND drop in top-noise quartile ≥2× bottom quartile. falsifier:
  α=0 recovers baseline; **position-SHUFFLED kernel reproducing the gain ⇒ it's logit-temperature not consensus, KILL.**
- **R2 · Expert-compatibility CRF (coalition)** [G1-B]. pairwise CRF (low-rank 128×128 compatibility M) + mean-field
  → complementary expert teams. Higher novelty, depth-mediated/weaker chain. falsifier: M=identity baseline; layer-localized null.
- **R3 · Stable-matching routing at finite capacity (Gale-Shapley)** [G1-C]. replace greedy overflow-drop with a
  STABLE token↔expert matching at training capacity C; near-zero params. falsifier: at C=∞ must be a no-op (bounds it);
  random-tie-break greedy matching it ⇒ contention benign, KILL. (Gated on running the forward at finite C.)

**THEME 2 — COMMITMENT / stopping / REVOCATION (L2); all share a forward-pass ORACLE proxy (no generation):**
> SHARED PROXY "commitment-trajectory replay": teacher-forced denoise held-out GT seqs; policy P freezes positions;
> track commit-precision vs commit-recall; the ORACLE commits each position at the first step its argmax=GT → a
> precision CEILING; compare policies at MATCHED recall (=equal compute). Pure forward passes. Sidesteps broken eval.
- **C-SPRT · Sequential-probability-ratio commitment** [G2-1]. axiom: single-step marginal confidence is sufficient.
  mechanism: accumulate a cumulative LLR across denoising steps, commit at a Wald boundary (sample-OPTIMAL, training-free).
  diff vs SAS/LUP: closed-form + guarantee, zero training. obs: closes ≥30% of greedy→oracle precision gap at matched
  recall. falsifier: temporal-shuffle the per-position step evidence ⇒ if ≈real, accumulation inert.
- **C-REVOKE · Conflict-driven revocable re-masking (CDCL for diffusion)** [G2-2] ★novelty. axiom: commitment is
  IRREVOCABLE (the AR inheritance). mechanism: after committing v_i, recompute p_t'(v_i|richer canvas); on POSTERIOR
  DRIFT (v_i loses argmax by margin δ) RE-MASK v_i + neighborhood and re-fill — weaponizes diffusion's UNIQUE revisability
  AR lacks; verifier-coupled variant (parse/bracket check) for code/math. obs: drift = erroneous-commit detector AUC≥0.70;
  drift-targeted re-mask recovery > base. falsifier: AUC≈0.5; random re-mask of equal count recovers as many ⇒ vacuous;
  **must beat spending the same forwards on more denoising steps.**
- **C-ROUTE · Route-stability commitment gate** [G2-3]. axiom: commit reads only OUTPUT confidence, ignores the ROUTER.
  mechanism: commit when the position's top-k EXPERT SET has stabilized (MoE-internal signal dense models lack), not just
  when output-confident. obs: route-stability adds ΔAUC≥0.03 over confidence-only for erroneous-commit prediction.
  falsifier: ΔAUC≈0; shuffle expert-ids → collapse; **partial out step-index (guard the H4 denoising-trend confound).**
  (A clean null is itself publishable — consistent with "router is content-only".)

**THEME 3 — the ELEPHANT: the marginal metric is blind to JOINT COHERENCE; generation (which sees it) is broken:**
- **M-FIX · Canvas-assembly differential probe (UNBLOCK, highest leverage)** [G3-C2]. reconstruct the inference
  generation canvas component-by-component (chat-template / block-causal mask / position_ids / mask-id / commit schedule),
  assert equality vs the TRAINING canvas, report the FIRST divergent component; invariant: forcing inference=training canvas
  reproduces CE≈3.62. obs: post-fix pretrained EM>0 on a 50-prompt smoke (vs 0.0). falsifier: all components equal but EM=0
  ⇒ genuine joint-incoherence (→ M-PCRH); negative: fixed harness must also decode LLaDA-MoE. UNLOCKS sampling/commitment/
  test-time + the H5 schedule-shift discriminator.
- **M-PLL · Self-conditioned PLL gap (PROXY)** [G3-C1] ★foundational. the forward-pass quantity the marginal CE is blind
  to: Δ = CE(masked set | model's OWN argmax context) − CE(masked set | CLEAN context) = the JOINT-COHERENCE deficit.
  hyp: generation EM is governed by robustness to conditioning on one's own errors, not marginal CE. obs: Spearman
  ρ(SC-PLL-gap, EM) > 0.7 AND > ρ(marginal-CE, EM)+0.2 across a panel where generation works (LLaDA-MoE + fixed
  DiffusionGemma). falsifier: Δρ≤0.05; random-position self-corruption must NOT predict EM. ENABLES generation-free iteration.
- **M-PCRH · Parity-check refinement head (novel ECC transfer)** [G3-C3] ★novelty. axiom: parallel per-position argmax =
  the joint belief (= "independent bit decisions violating the code's parity" in LDPC). mechanism: a small 2-4-layer
  MESSAGE-PASSING head over co-unmasked positions' top-k candidates (one BP sweep over a learned factor graph) → corrected
  logits p'_i that down-weight jointly-inconsistent combos BEFORE argmax; train head only on JOINT-NLL (= M-PLL's gap).
  obs: held-out joint-NLL over co-committed sets drops ≥10% vs frozen marginals. falsifier: ≤2% over 3 seeds ⇒ no
  exploitable joint structure; ablate message-passing (T=0 MLP, equal params) must not capture it; **must beat one more
  denoising step (same FLOPs).**

### CHECKPOINT synthesis — top picks + INTERLOCK (this is the value)
The candidates are not independent — they form a coherent program around the ELEPHANT (marginal metric blind to joint
coherence):
- **M-FIX + M-PLL crack the METRIC** (enablers): M-FIX restores generation (unlocks the whole sampling/commitment/
  test-time class + H5 schedule-shift); M-PLL gives a generation-FREE joint-coherence proxy that keeps the project moving
  even if M-FIX slips. Cheap, foundational.
- **M-PCRH is the flagship NOVEL MECHANISM** — directly attacks the joint-coherence gap (the real quality deficit) via an
  ECC/BP cross-token refinement head, measurable via joint-NLL (M-PLL's quantity), with the decisive "beat one-more-step"
  control. Most defensible novelty (no one does learned cross-token belief-propagation refinement on a diffusion-LM MoE).
- **R1 (routing-consensus)** is the cheapest NOVEL routing mechanism, diffusion-loss-measurable NOW (no harness needed),
  MoE-open-frontier, airtight falsifier — the best "ship something this week" candidate.
- **C-REVOKE** is the deepest "why diffusion beats AR" lever (revisability), forward-proxy-measurable; commitment space is
  crowded but revocability is its genuine differentiator.
**Recommended SELECT priority (pre-novelty-scan):** M-PLL (foundational, cheap) ≈ R1 (cheap, measurable now) → M-PCRH
(flagship novelty) → M-FIX (enabler) → C-REVOKE (deepest lever). M-FIX is a prerequisite for the commitment family.

## Stage 3 — NOVELTY (GPT-5.5 超高, 2026-06-26) — ranked by defensible novelty
1. **M-PLL (self-conditioned PLL gap): NOVEL.** Closest = PLL/pseudo-perplexity (Salazar 1910.14659, CLEAN-context),
   exposure-bias/scheduled-sampling (Bengio 1506.03099, AR), self-conditioning (Strudel 2211.04236, diff sense). The
   exact "own-argmax-context CE − clean-context CE as a DLM joint-coherence/self-error diagnostic" is NOT pre-empted.
   Frame as "a self-error/joint-coherence diagnostic that exposes the gap hidden by marginal denoising loss" (a
   diagnostic ABOVE the MDLM objective, not a new loss). Risk: "just exposure bias for MLMs" → defense: bidirectional,
   parallel, jointly self-induced. **→ the NOVEL centerpiece.**
2. **R1 (routing-consensus): cite-and-differentiate (narrow).** CLOSEST COLLISION = **Graph-of-Tokens / Attention-Aware
   SMoE (Nguyen 2505.00792)** — already does cross-token similarity/attention-coordinated routing; also ProMoE
   (2510.24711, vision). So do NOT claim "first cross-token coordinated MoE routing." Defensible slice = the masked-
   diffusion-LANGUAGE, NOISE/confidence-aware angle (clean positions stabilize NOISED positions' routing under the
   changing mask field); must ablate mask-ratio/confidence/noised-vs-clean, not just "attention-smooth logits". Severity MED.
3. **M-PCRH (parity-check refinement): cite-and-differentiate, HIGH collision.** The ECC/BP analogy is fresh, BUT
   "parallel-DLM marginals are jointly inconsistent → add lightweight structured correction before commit" is HEAVILY
   OCCUPIED by a 2026 cluster: **DEMASK 2604.02560** (dependency predictor, pairwise influences), **Mean-Field Parallel
   Decoding 2606.15805** (variational fixed-point), **ME-DLM 2605.09603** (edit-refinement for joint consistency),
   **Unified-Energy 2606.09159**; + NAT (Mask-Predict 1904.09324, Levenshtein 1905.11006). Viable ONLY as a specific
   learned BP/logit-correction head that BEATS those baselines at matched forward passes. Reviewers: "why not DEMASK +
   mean-field + ME-DLM in different clothing?" Severity MED-HIGH.
4. **C-REVOKE (revocable re-masking): LETHAL — DROP.** Already a full subfield: **ReMDM 2503.00307, RemeDi/self-reflective
   2509.23653, PRISM 2510.01384, ProSeCo 2602.11590, D3IM/SCOPE 2606.01026, T2M 2604.18738, NAVIRA 2606.06031.** "Remask
   committed tokens on drift" is done; CDCL vocab is not novelty. → cite as related/baseline; salvage only as an internal
   detail of M-PLL/M-PCRH with a specific conflict-certificate (posterior-drift theorem / causal poison-token test).

**超高 RECOMMENDED PAPER = M-PLL (+ maybe R1):** *"Standard masked/diffusion-LM loss measures clean-context marginal
denoising, but generation fails under SELF-INDUCED context errors. We introduce the Self-Conditioned PLL Gap as a
diagnostic/predictor of generation quality, then test whether diffusion-MoE routing (noise-aware consensus) reduces it."*
Use M-PCRH only with a sharply different head beating the 2026 cluster; DROP C-REVOKE as a claim.

> COLLISIONS SURFACED TO USER (pipeline: do not silently rewrite). Pending user ratification → Stage 4 design (专业) on
> the M-PLL+R1 program, then Stage 5 review + Stage 6 select.

*(Stage 4 design (专业), Stage 5 review, Stage 6 select append below.)*

## Stage 4 — DEEP DESIGN (专业) — DONE → full design in `plan/mpcrh-design-gpt55pro.md`
**Sharp novel claim (non-derivative):** M-PCRH = a *frozen-backbone, pre-commit, TOKEN-VALUED, top-k
CRF/parity-check layer*. At each denoising step it builds a sparse factor graph over the EXACT positions the
base sampler would co-commit; variables = token CANDIDATES (not binary commit flags); learned compatibility
factors define a NORMALIZED joint conditional over the co-commit tuple; BP → bounded per-position LOGIT
RESIDUALS added before the parallel commit. Train only the head (15-50M); backbone/MoE/router/scheduler frozen.
**Differentiators (the crux):** vs DEMASK ("which positions safe?" → selection) we ask "given these positions,
which token TUPLE is jointly plausible?" and KEEP THE COMMIT SET FIXED; vs Mean-Field (training-free, binary
commit flags) ours is LEARNED, token-valued, revises LOGITS; vs ME-DLM (post-hoc edits a completed draft) ours
is PRE-commit; vs Unified-Energy (don't sell as "energy" — a CRF has an energy → reviewer bait) sell as a small
amortized parity-check decoder with exact top-k joint NLL. Humility line: "we report top-k(+TAIL) joint NLL, NOT
full-vocab likelihood."
**Architecture:** maximum-spanning-FOREST CRF (treewidth-bounded → EXACT log-partition by sum-product, O(|E|K²));
A_i=TopK(ℓ_i)∪{TAIL}(+gold in train); row/col-centered low-rank pairwise factors (so they can't act as unaries —
honest joint ablation); BP → clipped δ-logit residuals. Loopy/LDPC version = later, NCE/Bethe-labeled, ablation only.
**Metric/objective:** exact truncated joint-NLL on the gold tuple over the base co-commit set; ΔJ-NLL@K = base-indep
− M-PCRH (forward pass, no generation). Pre-registered success (ΔJ-NLL@16>0, bootstrap-CI excl 0; ≥0.03 nats/5%
rel; beats equal-param UNARY-MLP by ≥25% of its gain; shuffled-edge loses ≥half; beats model-commit base+1; 3 seeds).
**KEY first step = the CHEAP ORACLE GO/NO-GO (before building the head, forward-pass-only):**
- Probe A: top-k joint RESCUE CEILING — frac of co-commit sets where base tuple is WRONG but all gold ∈ top-k AND ≥2
  positions coupled (the rescuable region). GO only if sizable.
- Probe B: UNARY-oracle vs JOINT-oracle — if a per-position reranker already explains the recoverable errors, a joint
  head is UNNECESSARY (kill).
- Probe D: no-training FUTURE-NLL oracle — fill C_t with candidate tuples, run one forward, score by future gold NLL;
  does a different JOINT choice lower future NLL vs independent argmax? (the cleanest no-train test of the hypothesis).
- Probe E: tiny CRF vs unary MLP (1-5M) — GO only if the CRF beats the unary probe on problem-level splits.
**Controls that decide it:** equal-param UNARY-MLP (if it matches → joint story dead); shuffled/random graph; T=0
identity; **one-more-denoising-step (mandatory — must beat model-commit base+1).** Kill if: top-k coverage <50-60%;
no beat over unary-MLP; shuffled≈real; vanishes on problem-level split; one-more-step wins; or generation (once
fixed) shows no gain.
**Biggest threat:** metric mismatch (teacher-forced top-k joint-NLL may not transfer to closed-loop generation) →
the safe claim is mechanistic ("M-PCRH reduces measured co-commit joint incoherence"); the strong claim needs the
fixed harness + GSM8K/HumanEval confirm. Also: position M-PCRH as COMPLEMENTARY to DEMASK/Mean-Field (they select C,
we revise values in C).
**RECOMMENDED FIRST BUILD:** run Probes A/D/E first; only if GO, build **M-PCRH-Forest@K16** (the forest's EXACT
normalized joint objective is the defensible asset vs "another heuristic dependency-aware sampler").

## Stage 5+6 — RIGOR REVIEW + SELECT (Codex GPT-5.5-xhigh) → VERDICT: MODIFY (proceed, tightened)
The design is directionally strong but the protocol needs tightening BEFORE the causal claim holds:
1. **CANDIDATE-SUPPORT LEAKAGE (main gap, reward-hacking surface):** the PRIMARY metric must NOT inject gold —
   use DEPLOYMENT support `TopK ∪ {TAIL}` only (gold-included = diagnostic only, reported separately), else
   ΔJ-NLL@K is an oracle-support score. FREEZE/audit TAIL residuals (mass→unmodeled TAIL can improve NLL without
   improving generation).
2. **Stricter controls:** add distance/degree/step/entropy-MATCHED shuffled graphs, distance-only topology, and
   real-topology zero-pairwise ablations (row/col centering alone doesn't prove "joint consistency").
3. **Teacher-forced confound:** a head trained/eval'd on CLEAN teacher-forced canvases may learn a clean-context
   correction that fails on MODEL-COMMITTED contexts → add a self-conditioned / model-commit REPLAY subset before
   any generation-adjacent claim. (Note: this is the M-PLL self-conditioned idea, now folded in as a control.)
4. **Differentiation OK if kept NARROW** (fixed commit set + token-valued CRF/BP + exact truncated joint-NLL);
   Unified-Energy is the closest collision → add a same-support top-k ENERGY baseline or state as a limitation.
5. **Metric-mismatch doesn't kill it:** the mechanistic claim ("frozen-backbone token-valued CRF head reduces
   measured co-commit top-k joint-NLL") is publishable with the tightened controls; the STRONG claim ("improves
   generation/code/math") needs the harness fixed.

### FINAL SELECT (Stage 6) — the pre-registered FIRST experiment
**Run Probe A + Probe B FIRST (not D/E):** support/rescue audit on PROBLEM-LEVEL held-out logged states, K=8/16,
**DEPLOYMENT SUPPORT ONLY**, stratified by |C_t| / step / task / entropy / base-wrong. Pure forward passes.
**KILL / reframe (pre-registered)** if at K=16 ANY of: top-k tuple coverage on base-wrong co-commit sets < 60%;
oracle-rescuable high-risk sets < 10-15%; OR the UNARY oracle explains ≥ 80-90% of recoverable errors (→ a joint
head is unnecessary; use a per-position reranker). If GO → Probe D (future-NLL oracle) → Probe E (tiny CRF vs
unary) → only then build **M-PCRH-Forest@K16** with the tightened controls.
**Top first-run risk:** the rescuable region DISAPPEARS once gold-injected support + clean-teacher-forced optimism
are removed. **GPU-gated** behind the H5 3-seed run; strong claim gated on the generation-harness fix.

### IDEATION PIPELINE COMPLETE. Output = this vetted, executable M-PCRH plan. Executing it is a SEPARATE step
(the next experiment = Probe A+B support/rescue audit; GPU-gated behind H5). Per the kernel: stops at the reviewed
shortlist; the oracle GO/NO-GO is the first falsifiable run when the GPU frees.

## Stage 4 note (superseded by the DONE block above)
- **User SELECTED M-PCRH** (ambitious; attacks the joint-coherence gap directly). 专业 (GPT-5.5 Pro) designing:
  sharp differentiation from the 2026 cluster (DEMASK/Mean-Field/ME-DLM/Unified-Energy), the message-passing
  architecture, the joint-NLL training objective, a falsifiable protocol (baselines @ matched forward passes +
  "beat one-more-step" control), and an ORACLE GO/NO-GO probe (does oracle joint-consistent reranking of top-k
  lower held-out loss BEFORE building the head). Chat: "DiffusionGemma M-PCRH Design". Primary metric = held-out
  JOINT-NLL (forward pass, no broken generation eval needed).
