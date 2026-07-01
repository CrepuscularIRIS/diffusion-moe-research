# Ideas — He-Level Elegant Generation on FROZEN DiffusionGemma 26B-A4B

> `research-ideation` pipeline (Arbor-decoupled). Stops at a ranked, review-survived shortlist; executing a
> winner is a separate step (worktree subagent). Started 2026-06-28 (broadened `/goal`: the gradient-field /
> embedding-flow line is now *reflection input*, not the thesis — find a He-LEVEL elegant method, direction
> NOT pre-baked, found+corrected by /ideate→Codex SELECT).
> Engines: Opus (explore/generate/R1-R2-R5) · Codex `codex:codex-rescue` (R4 rigor + SELECT) ·
> Playwright→GPT-5.5 **Pro 扩展** (novelty R3 + AC). Supersedes the *scope* of `plan/ideas-gradient-field.md`
> (that 16-cand list = the now-narrowed embedding-flow campaign; extended/reflected-on here, not discarded).

## Stage 0 — Brief
- **Claim space:** find a **Kaiming-He-LEVEL elegant** generation method (simplest target in the RIGHT
  geometry, fewest moving parts) on **FROZEN DiffusionGemma 26B-A4B** (block masked DISCRETE-diffusion MoE;
  256-canvas; D3PM-uniform discrete-token corruption, no [MASK] — noised anchor = valid-vocab embedding
  centroid ē; ~44.5/48-step EntropyBoundSampler, early-stops ~93%, band t∈[0.4,0.8]; token-choice top-8/128
  router reads ONLY hidden state, NO timestep; tied embed/lm_head d=2816, scale √d≈53.07). Lightweight
  inference-time or tiny on-manifold adapter only. Metric = **verified generation** (math_verify); diffusion
  loss DIAGNOSTIC-ONLY.
- **Frontier:** Track-1 wall-clock frontier RATIFIED (frozen dLLM ~5–7× verified-reasoning/sec vs matched AR;
  the one completed positive — don't re-derive). Near-ceiling quality (GSM8K 100%, MATH-500 94%, HumanEval
  97.5%); real headroom only **AIME-24 73% / MATH-L5 83%**; dominant residual failure = **sampler TRUNCATION
  / no-box** (no-box 0.418@768 → 0.060@2048; 768→1280 alone lifts MATH 83→94%), NOT reasoning.
- **Goal anchor:** a He-level elegant result (one principle, fewest parts) — a real WIN (few-step speedup at
  matched verified-acc, OR an anti-truncation quality win), OR a clean structural negative that sharpens the
  next /ideate. Negatives = success.

## Stage 1 — Landscape (4 isolated EXPLORE mappers: substrate / kill-list / cross-domain / open-frontier)

### Solved / ratified (don't re-tread)
- Wall-clock frontier (Track-1) — the one positive; generalize or go orthogonal, don't re-derive.
- Empirical sampler ~44.5/48 steps, early-stops ~93%; the model is ALREADY adaptive-few-step.
- The narrowed embedding-flow finding (codec-metric mismatch; "Don't Snap"/right-metric) — only MATCHES native.

### Tried-and-dead (do NOT re-propose without a SPECIFIC counter)
- **Measurement-mismeasure:** A equivalence-class "2.3%" = t=1.0 artifact OUTSIDE sampler band (oracle recovers
  Top1@30=0.943); diffusion-loss-as-proxy (SFT halved loss, 0 acc gain); single-reference-token scoring.
- **Commitment / scheduling / allocator:** E trace-dynamics ranker KILLED (AUC below random; just the nfe
  counter); problem-level compute-allocator DEAD (PERFECT oracle beats always-deepen by only ~1% ΔAUC →
  "just run deepen@2048"); branch<deepen; "bigger budget" is the trivial baseline. Space is CROWDED + has no
  headroom.
- **Timestep:** H4 passive non-identifiable (trend≡t confound; "29/30 layers" = free-shuffle artifact); H4
  interventional architecturally VACUOUS (router has no t-port); H5 feed-t lowered diffusion loss but NEVER
  gen-evaluated + on the corrupted ckpt (loss≠gen).
- **Embedding-flow narrowing:** G4 Euclidean-NN snap = Voronoi trap (retention 0.72 vs cosine/logit 0.92);
  N1b structural-kill was CODEC-CONFOUNDED; broad "no continuous interface" claim WITHDRAWN; the right-metric/
  no-snap carrier only MATCHES native (NFE 24.8 vs 21.6 → NO speed win) — narrower-but-publishable, NOT He-level.
- **Other:** M-PCRH committed-set joint-refinement KILLED (co-commit set ~independent; |C|≥4 rescuable 0.006);
  "thinking-mode" rescue TRAP (AIME 73→0); SFT-as-lever (tied acc); prior-art pre-emption (SAS 2606.23567,
  Learning-Unmasking-Policies 2512.09106, TraceLock, Fast-dLLM, RemeDi, ELF, LRD, SDTT/DiDi).
- **Recurring LESSONS:** (1) wrong-metric / premature discretization → use sampler-matched regime + model's
  OWN inner-product geometry + verified-gen metric; (2) score-up≠mechanism → pre-declare + beat the trivial
  control (nfe-counter / always-deepen / final-entropy / plain-CE / random) with CI>0; (3) near-ceiling ⇒ only
  few-step/speed OR clean-negative is headroom, dominant residual = TRUNCATION; (4) oracle designed-negatives
  decisive BUT prove the codec/oracle lossless first (the N1b→N2 reversal); (5) kills have been artifacts —
  never self-ratify (independent Codex DECIDE); (6) commitment/sampler space crowded + no headroom; (7) match
  the budget/compute regime or it's non-evaluable.

### Open / borrowable (the live surface)
- **Native `self_conditioning_logits` channel (E1 #1 underused lever):** the model was TRAINED to consume a
  soft distribution carrier — `softmax(logits)@W·scale → trained gated-MLP → add to canvas`. This is the
  model's OWN **on-manifold** continuous interface. The narrowed embedding-flow line fed E[e] via the
  *off-manifold* canvas hook; it NEVER routed the flow through the native SC channel. Training-free.
- **Decoder never writes KV cache** → cheap unlimited full-canvas re-forwards against a frozen context →
  parallel-in-step / fixed-point (Picard/Jacobi) / Anderson / corrector iteration is affordable.
- **`max_denoising_steps` is "Unused" except as loop-bound + temperature-schedule denominator** → can decouple
  #forwards from temperature resolution; can force exact-K (disable stopping criteria).
- **Warm-startable canvas** (seed a distributional/continuous initial guess); **`self_conditioning_mask`** =
  per-example 0/1 gate (free CFG-style conditional/unconditional toggle); **argmax_canvas vs current_canvas**
  kept separate (keep a clean draft while exploring).
- **Anti-truncation as a CONTROL problem (E3-F + E4-α convergence):** early-stop is OPEN-LOOP on a categorical
  entropy bound; close the loop on output-presence (high-prob `\boxed` in tail) — one-flag; disambiguates
  premature-readout (win) vs unfinished-reasoning (clean negative). Re-point the "right-geometry" lever from
  the (narrowed) sampling trajectory to the (untouched, high-headroom) STOP/commit decision using the same
  tied-embedding Voronoi-margin geometry — zero-train. Must beat native entropy-bound stop at MATCHED NFE
  (else it's the dead allocator).
- **Uncommitted-residual joint posterior (E4-β / X1):** M-PCRH killed coupling in the COMMITTED set; the
  uncommitted high-entropy residual is explicitly UN-killed — cheap decisive probe of the factorization barrier.
- **Reusable infra:** `patched_denoiser` monkeypatch of `_denoising_step` (universal injection point);
  `CanvasEmbeddingHook`; full negative-control battery (commit_only/echo/shuffled/nat_discrete/nat_cont/snap
  variants/Voronoi audit/consumability curves/paired-bootstrap CI bins); wall-clock harness + sealed verifiers.

## Stage 2 — Probe Block (≥2 evidence each)
```
Q1 bottleneck CLASS = STOPPING/OUTPUT-COMMITMENT (truncation dominant: no-box 0.418@768→0.060@2048; +budget
   fixes MATH 83→94%) ⊕ REPRESENTATION/INTERFACE (does the frozen discrete-CE backbone host a usable continuous
   clean-distribution field via the RIGHT, on-manifold interface? — N2: yes via inner-product geometry, but
   only tested the off-manifold hook → matched native).
Q2 hidden assumptions: (a) "to carry a soft state we must inject embeddings via the canvas hook" — FALSE, the
   model has a TRAINED self_conditioning_logits channel (on-manifold); drop it → an on-manifold continuous
   carrier the narrowing never tested. (b) "early-stop is fixed" — FALSE, it's open-loop entropy; close the
   loop on output-presence. (c) "within-block positions independent" — sampler factorizes; coupling may live
   in the uncommitted residual.
Q3 elephant: near-ceiling + already-adaptive-few-step ⇒ few-step SPEED headroom thin (g4_soft_cont matches
   native) AND quality headroom thin (6pt truncation gap @ fair budget). He-elegance and headroom point
   OPPOSITE ways; the honest payoff is their intersection (a real WIN) or a clean decisive negative.
Q4 Hamming = YES: "can the model's OWN trained interface/geometry unlock a win (few-step or anti-truncation)
   the wrong (Euclidean/off-manifold) interface couldn't?" extends the N2 narrowing with the one interface it
   skipped (native SC), attacks the actual residual failure (truncation), stays He-elegant, cheap+verifiable.
```

---

## Stage 2 — Candidates (3 isolated Opus generators × {geometry/interface, anti-truncation control, transport/factorization}; de-duped into 5 clusters). 5-field MechanismHypothesis each.

### Cluster I — Native self-conditioning channel as the ON-MANIFOLD soft carrier (the interface the embedding-flow narrowing skipped)
**I1 — SC-Carry (discretize-last soft carry through the NATIVE channel)** ★ foundational; tests Q2 head-on
- axiom: to carry a soft clean-distribution you must inject E[e] via the OFF-manifold canvas hook + snap each step.
- mechanism: `_denoising_step` rewrite — pass the full pre-snap logit distribution p_k forward as `self_conditioning_logits` (model's trained softmax→@W·scale→gated-MLP consumes it), ZERO intermediate snap, SINGLE terminal snap_H. The g4_soft_cont info re-routed through the on-manifold carrier.
- hypothesis: beats g4_soft_cont (which only matched native) because the gated-MLP was TRAINED to consume this distribution → soft state stays on-manifold → cleaner contraction → fewer forwards at iso-quality OR higher quality at iso-NFE.
- observable: at iso-acc MATH-L5, NFE < native 21.6 (≤18); OR at iso-NFE, AIME +≥2 abs.
- falsifier: vs {native few-step, g4_soft_cont}; neg=uniform/garbage into SC (must not help); equal-NFE; AIME holdout. MUST beat native AND g4_soft_cont; kill if only matches → Q2 axiom falsified. {~0.5-1 GPU-day · novelty MED vs ELF/pMF · He 5}
**I2 — SC-Extrapolation (Anderson/Aitken on the carrier)** — the speed-win bet
- mechanism: feed extrapolated p̂=p_k+α(p_k−p_{k−1}) (Aitken/Anderson in logit space, re-projected to simplex) as SC; discretize last. hypothesis: refinement is a simplex contraction → extrapolation reaches the fixed point in fewer forwards (training-free, vs SDTT distillation). observable: NFE to iso-acc MATH-L5 −≥20% (≤17), acc ±0.5%. falsifier: α=0 (=native SC, must beat); neg=α<0 must hurt; equal-NFE. {~1 GPU-day · novelty MED · He 4}
**I3 — SC Warm-Start (seed the carrier from a one-forward prior)** — the carrier's INITIAL condition
- mechanism: seed step-0 SC logits from a single prompt-conditioned forward (on-manifold soft anchor vs the centroid-ē start). hypothesis: the ē-anchor start sits in a poor basin inviting confident-wrong collapse; a soft prior moves the start into the answer basin. observable: MATH-L5 +≥1 (reduced confident-wrong) OR NFE −≥15%. falsifier: neg=seed from a MISMATCHED prompt (must not help); equal-compute=native +1 step (must beat). {~0.5 GPU-day · novelty MED-LOW · He 4}

### Cluster II — Anti-truncation / output-completion CONTROL (close the open-loop stop; the dominant-failure lens)
**II1 — Luenberger output-presence observer (closed-loop bidirectional stop)** ★ flagship "close the open loop"
- axiom: the stop predicate is a function of internal stability/entropy alone; answer-presence is never observed.
- mechanism: observable y=P(complete `\boxed{}` in argmax_canvas tail) from existing logits; rewrite stop to a bidirectional law — STOP when y≥τ_high (bank NFE on solved), VETO stop + keep denoising when entropy-says-stop but y<τ_high (spend banked NFE on truncation-prone). One observable, one inequality; net ΔNFE≈0.
- hypothesis: the entropy stop fires early on problems whose reasoning is done but whose box isn't allocated; reallocating STOPPING TIME (early-out on presence, late-out on absence) gives truncation cases the compute easy cases didn't need.
- observable: at matched mean-NFE, no-box 0.30→<0.10; MATH-L5 +≥3; AIME flat-or-up; locality: NFE-saved≈NFE-spent.
- falsifier: native EB-stop vs observer-gated, matched mean-NFE; neg=gate on a RANDOM tail token (must not help); holdout AIME (τ on MATH-L5 dev). MUST beat native stop AND always-deepen@matched-budget. Disambiguator: extend-then-force-box → correct ⇒ premature stop (win) / wrong ⇒ unfinished (clean negative). {LOW · novelty LOW-MED vs EB-Sampler/SAS/Fast-dLLM (they accelerate; none gate STOPPING on an output observable) · He 5}
**II2 — Reference-governor / deadbeat answer-slot (force-land the box before the boundary)**
- mechanism: RESERVE last R≈24 tokens as a protected answer slot; within H steps of the boundary, force-land a `\boxed{…}` scaffold (inject `\boxed{`+`}`, model fills interior via free re-forwards). Target-rewrite only, ZERO extra forwards. hypothesis: truncation is structural non-emission (sampler never allocates box tokens before canvas ends), not unknown value. observable: on native-no-box subset @matched budget, force-land recovers ≥40% to correct; MATH-L5 +≥3; already-boxed must not drop. falsifier: neg=fill slot with random/uniform-argmax value (must not recover); equal-NFE (0 added forwards); holdout. Built-in disambiguator (forced-box-correct=emission failure win / confident-wrong=genuine non-completion negative). {LOW-MED · novelty MED · He 4}
**II3 — MPC receding-horizon step-reallocation (within fixed budget)** — highest measurement risk
- mechanism: cheap 1-2 step lookahead re-forward; cost-to-go J=(steps-to-box)+λ·answer-uncertainty; allocate next step (refine vs advance) to min J; rollouts CHARGED to budget (matched-NFE). hypothesis: truncation = misallocated compute (refining settled tokens while the tail starves). observable: matched total-NFE, no-box<0.10, tail-NFE-fraction↑. falsifier: greedy-1-step vs uniform at identical total NFE; neg=anti-cost (minimize box progress, must be worse). {MED-HIGH · novelty MED (vs Prophet) · He 3}
**II4 — EOS-deferred commit (discretize-last on the stop token)** — cheapest truncation attack
- mechanism: hold EOS/pad in the soft SC carrier, forbidden from winning any argmax snap until ALL content positions reach their SC fixed point; one scheduling rule on one token id. hypothesis: truncation = EOS reaching low entropy before a long derivation finishes. observable: truncation −≥40% rel; AIME +≥2; length up ONLY on previously-truncated items (locality). falsifier: neg=defer a RANDOM non-EOS id (must not help); equal-NFE; locality (non-truncated must not regress); kill if gain = uniform length inflation. {~0.5 GPU-day · novelty LOW · He 5}
**II5 — SC-Guidance / CFG via the native `self_conditioning_mask`** — anti-under-commitment
- mechanism: per-step contrast forward-A(mask=1) vs forward-B(mask=0); guided=logits_A+w·(logits_A−logits_B); snap from guided. Native mask gives the conditional/unconditional pair free. hypothesis: truncation=under-commitment; amplifying the SC direction sharpens under-committed answer tokens, suppresses premature EOS. observable: AIME +≥2 & MATH-L5 +≥1 at w∈[0.5,2], truncation −≥30% rel. falsifier: w=0 (=native, must beat); neg=guide AWAY (−w must hurt); equal-compute vs native@2×steps (2 forwards/step). {~1-2 GPU-day · novelty MED-LOW · He 4}

### Cluster III — RIGHT-GEOMETRY on the commit/stop DECISION (re-point the narrowed-trajectory geometry to the untouched stop; EXPLORE Lever α)
**III1 — Voronoi-margin geometric commit signal (vs categorical entropy-bound)** ★ cheapest offline pre-kill
- axiom: stopping confidence is correctly measured by categorical softmax ENTROPY (EB-Sampler). Entropy is the right geometry.
- mechanism: tied embed/lm_head ⇒ logit = inner product with a token embedding ⇒ decision surface = Voronoi tessellation; margin = top-logit − runner-up = distance to the nearest cell boundary (a subtraction on existing logits). Replace the stop's confidence on box-value tokens: stop = (box present) ∧ (min margin ≥ m*). Commit on geometric decisiveness, not categorical peakedness.
- hypothesis: entropy is geometry-blind — a softmax can be peaked while the state sits NEAR a Voronoi boundary between numerically-adjacent answer tokens (digit confusions, cf. the digit-blind ckpt history); margin measures boundary-distance directly → catches under-committed answers entropy calls "confident," cutting premature stops AND confidently-wrong boxes.
- observable: OFFLINE pre-check (cheapest possible) — on logged gens, AUC(margin vs verify) > AUC(entropy vs verify) on box-value tokens; then live, matched mean-NFE: no-box↓ AND confidently-wrong-box↓, MATH-L5↑.
- falsifier: KILL BEFORE any sampler change if margin-AUC ≤ entropy-AUC on logged traces; else swap gate, matched-NFE; neg=margin on RANDOM non-answer tokens (must not help); holdout AIME (m* on MATH-L5 dev). Must beat native entropy stop. {LOW; offline pre-kill · novelty LOW-MED (swap categorical entropy→tied-embedding Voronoi margin as the COMMIT criterion) · He 5}
**III2 — Sample-and-hold answer latch (disturbance rejection / anti-overwrite)**
- mechanism: once box-value tokens cross a geometric commit margin (reuse III1's m), FREEZE those positions (remove from later `_denoising_step` updates); canvas keeps reasoning elsewhere but can't disturb the committed answer. hypothesis: some correct answers FORM then get denoised AWAY (digit-blind churn). observable: OFFLINE pre-kill — measure box-value token CHURN on native runs (correct box forms then changes); if churn≈0 → no-op (clean negative: truncation=non-emission not destruction); if high, latch → no-box↓, high-churn-subset acc↑. falsifier: neg=latch RANDOM tokens (must hurt/no-op); equal-NFE. {LOW; offline pre-kill · novelty MED · He 4}
**III3 — SC fixed-point stop (carrier-residual stop vs entropy-band)** — adjudicates Q1's STOPPING⊕REPRESENTATION XOR
- mechanism: halt when SC-distribution residual ‖p_k−p_{k−1}‖ (KL in the model's own softmax geometry) at ANSWER-region positions < τ (reuses the carrier's distribution, no extra forward). observable: asymmetric Pareto — NFE≤18 on easy at iso-acc AND truncation −≥30% on hard → AIME +≥1.5. falsifier: neg=residual on a RANDOM region (must not help); equal-NFE; KILL if it reproduces the entropy-stop Pareto → stopping is NOT the bottleneck (Q1→REPRESENTATION). {~0.5 GPU-day · novelty LOW · He 4}

### Cluster IV — Few-step TRANSPORT in the model's own logit geometry (numerical-analysis tools; cheap re-forwards)
**IV1 — Exponential integrator: analytic centroid-decay + model nonlinear correction** ★ best real-WIN speed bet, deeply He
- axiom: the whole reverse step must be computed by the model; its forward has no analytically-known linear part.
- mechanism: D3PM-uniform corruption gives an EXACTLY known linear part — the distribution decays toward uniform / E[e_t]=ᾱ_t e₀+(1−ᾱ_t)ē with known schedule ᾱ_t. Split ẋ=Ax+N(x): A = the analytic decay operator from the corruption kernel (closed-form e^{AΔ}, in probability/logit space via the SC carrier), N = the model's nonlinear correction (one re-forward). ETD1/ETD-RK2 step → the analytic part de-biases toward the clean simplex FOR FREE, model supplies only the correction → larger stable steps. snap_H.
- hypothesis: native re-derives the known centroid-decay numerically every step; handling it in closed form lets each re-forward target only the nonlinear correction → fewer NFE at equal accuracy, IF centroid-decay is the dominant stiffness.
- observable: verified-gen at matched NFE; WIN = equal acc at fewer NFE with the gap GROWING as Δ increases (signature of exact linear handling).
- falsifier: ETD1 at K∈{4,8} vs native/Euler at matched NFE; neg=A=0 control (reduces to explicit Euler — if A=0≈real A, the split adds nothing → clean negative); mechanism control = verify empirical logit decay matches ᾱ; A is from the forward KERNEL, NOT an energy gradient (defuses the logits-as-∇E caveat). {LOW-MED · novelty MED (ETD/DPM-Solver standard in continuous Gaussian diffusion; discrete D3PM-uniform-to-centroid in logit space on a frozen dLLM under-explored) · He 5}
**IV2 — Logit-space Anderson-accelerated implicit large-step solve** — risky flagship, leans negative
- mechanism: treat t→t−Δ as x=F_t(x); solve by Anderson(m=2-3) minimizing the LOGIT residual (mix logits = correct unconstrained geometry), feed back via SC; K_big∈{4,6,8}. hypothesis: stiffness = inter-position coupling in the uncommitted residual; joint fixed-point per step advances further. observable: ≥native acc at ≤0.7× NFE. falsifier: must beat plain Picard (same K_big) AND native@matched-NFE; neg=damping0/random-position-update; report logit-residual contraction (oscillation ⇒ non-contractive ⇒ kill). {MED · novelty LOW-MED · He 4}
**IV3 — Training-free MeanFlow-of-transport (logit-secant jump)** — shipped as a DESIGNED-NEGATIVE class-closer (~90%)
- mechanism: 2 probe re-forwards (t, t−δ); average logit-velocity v̄=Δ/δ; one big extrapolated jump logit(0)≈logit(t)+t·v̄; snap_H. hypothesis: the frozen logit trajectory is ~affine mid-noise → one jump lands at the same argmax. observable: match native at ~2-3 NFE/block. falsifier: must beat single Euler step (δ→0); on-record neg=the embedding-flow few-step result; measure trajectory curvature (high ⇒ affine fails ⇒ predicted kill). {LOW · novelty HIGH-overlap (mostly a control) · He 3}
**IV4 — Heun predictor-corrector with SC as the 2nd-order coupling carrier**
- mechanism: trapezoidal logit step — predict v(x_t), correct by re-forward at t−Δ with SC fed the PREDICTOR's distribution, average slopes. hypothesis: SC is a trained on-manifold joint-distribution carrier → 2nd-order step more accurate per NFE than two 1st-order native steps. observable: Heun-PC (2NFE/step) beats native (2 steps) at matched NFE. falsifier: neg=corrector WITHOUT SC routing (if ≈, SC carries no coupling); equal-NFE. {LOW · novelty MED (SC-as-corrector-carrier is the slice) · He 4}

### Cluster V — JOINT FACTORIZATION in the uncommitted residual (M-PCRH killed the COMMITTED set; the residual is explicitly UN-killed)
**V1 — Uncommitted-residual joint re-denoise (the X1 probe)** ★ DECISIVE, near-free, attacks per-candidate accuracy
- axiom: within-block positions are independent — the high-entropy uncommitted residual can be denoised position-by-position.
- mechanism: run native to mid-step; pick top-K high-entropy UNCOMMITTED positions; re-noise exactly those to ē; ONE joint frozen re-denoise conditioned on the fixed committed context AND each other's current soft distributions via SC. Compare joint fill vs independent native fill of the SAME K positions; updates in logit space.
- hypothesis: the residual is where genuine inter-position dependence lives (committed set already shown independent: |C|≥4 rescuable 0.006) → resolving the joint posterior fixes COORDINATED errors (multi-token numbers, balanced expressions) independent filling gets wrong.
- observable: PER-CANDIDATE accuracy MATH-L5/AIME, joint vs independent, same canvas; WIN = joint ≥ +2-3 abs OR |residual|≥4 rescuable ≫ 0.006.
- falsifier: one X1 run; neg=SHUFFLED cross-conditioning (residual conditioned on RANDOM others — if ≈ joint, no coupling); equal-NFE (joint = +1 re-forward); locality (gains must concentrate on mutually-high-MI positions, e.g. digits of one number). KILL if joint≈independent ⇒ factorization holds everywhere ⇒ closes the joint-coupling class (major clean negative). {VERY LOW (handful of re-forwards on existing canvases, no training) · novelty LOW (diagnostic; finding novel either way) · He 5 if it wins}
**V2 — Residual-restricted Anderson relaxation (V1+IV2 fusion; commit-gated joint solve)** — capstone, GATED on V1
- mechanism: freeze EntropyBound-committed positions as context; Anderson(m=2-3) logit-space fixed-point relaxation over ONLY the uncommitted high-entropy residual, cross-conditioned via SC. Locality (from M-PCRH) makes the solve cheap and targets exactly where coupling lives. hypothesis: the residual is the only place the joint fixed point differs from the independent update → concentrate compute there. observable: verified-gen at matched NFE AND per-candidate acc; WIN = both ≥native at ≤native NFE, acc up on coordinated-error cases. falsifier: must beat plain Picard-on-residual AND whole-canvas IV2; neg=relax a RANDOM equal-size subset (if ≈, locality false); PRE-KILLED if V1 returns a clean negative. {MED · novelty LOW-MED · He 5}

## Convergence finding (across the 3 isolated generators + the 4 EXPLORE mappers)
1. **Two independent generators + two independent explorers converged on ANTI-TRUNCATION as the real headroom** (the dominant residual failure), attacked via the model's OWN inner-product geometry on the STOP/commit decision (II1/III1) — re-pointing the narrowed "right-geometry" lever from the (match-only) sampling trajectory to the (untouched, high-headroom) stop. Cheapest decisive bets; III1/III2 have OFFLINE pre-kills (no GPU sampler change).
2. **The native `self_conditioning_logits` channel** is the one on-manifold interface the embedding-flow narrowing never tested (it used the off-manifold hook) — Cluster I tests whether it unlocks a WIN where the hook only MATCHED native.
3. **Two genuinely He-MODELING speed/quality bets exploit STRUCTURAL facts unique to this substrate:** IV1 (the corruption kernel's analytic linear part — closed-form, model supplies only the nonlinear correction) and V1 (the explicitly-un-killed uncommitted-residual joint posterior). Each is either a real WIN or a clean class-closing negative.
4. **Honest prior (EXPLORE-4 + kernel lesson 3):** headroom is thin (near-ceiling + ~6pt truncation gap @ fair budget; already adaptive-few-step) → weight "publishable clean decisive negative" above "He-level positive," consistent with the directive (negatives = success). Designed-negatives shipped: IV3 (class-closer), V1 (factorization-class), the A=0/random/shuffle controls throughout.

## TOP CANDIDATES → Stage 3 NOVELTY (Pro 扩展) + Stage 4-5-6
Routed to Pro 扩展 for prior-art (most-novel, highest-value, span all four lenses): **IV1** (exponential integrator / kernel operator-splitting), **V1** (uncommitted-residual joint), **III1+II1** (geometric Voronoi-margin commit + output-presence observer = the anti-truncation right-geometry slice), **I1** (native-SC on-manifold carrier). Submitted 2026-06-29 (chat "ML Paper Prior-Art Audit", Pro 扩展, 15-min poll).

## Stage 5 (partial) — R4 RIGOR (Codex `codex:codex-rescue`, independent; generator never self-selects)
Global gate Codex imposed: every positive = verified-generation only, matched by COUNTED forwards + wall-clock, must beat {native, always-deepen/static-budget, nfe/final-entropy, AND the v3 right-metric/top-k/LRD carriers where relevant}; output-format candidates need parser/suffix/force-box controls or they are **verifier-surface hacks**.
- **PROMOTE: V1** (uncommitted-residual joint — best cheap class-closer; sufficient if independent baseline uses the SAME K positions + same +1 forward, shuffled-cross-conditioning included, gains localize to high-MI spans), **II4** (EOS-deferred commit — clean one-token falsifier; sufficient if locality strict + random-token-defer no-op + not length-inflation).
- **REVISE (+ the one fix):** I1 (must beat g4_soft_cont/cosine/logit + top-k/LRD at exact NFE, else = the narrowed codec rerouted), I2 (add no-SC over-relax/temperature baseline), II1 (add zero-extra parser/suffix/force-box baseline + no-box/wrong-box/parse-fail stratification — high reward-hack risk), II2 (suffix/scaffold-only baseline; recovery from generated interior not injected surface), II5 (add temperature/logit-scale sharpening baseline at 2× cost), III1 (require incremental AUC over {box-present, entropy, final-entropy, nfe} offline AND live), III2 (predeclare churn threshold ≥5%; if churn≈0 → reject as non-emission), III3 (add final-entropy/nfe/box-presence baselines; need Pareto dominance), IV1 (add native-schedule/logit-temperature rescale + v3 right-metric/top-k baselines; require gap grows as K shrinks; novelty unverified→Pro), IV2 (beat Picard + damped Picard + native at counted NFE; kill on oscillation), IV4 (add predictor-only/Heun-without-SC/two-native-step baselines), V2 (HARD-GATED behind V1: run only if V1 CI-LB ≥ +2pp or residual-rescuable ≫ 0.006; auto-reject if V1 negative).
- **REJECT:** I3 (warm-start = initializer/extra-compute tuning; +1pt too small for He-level), II3 (collapses to the dead allocator/MPC; rollout-charging unenforceable; not He-elegant), IV3 (designed-negative only — KEEP as a control under IV1/IV2, not a candidate).
- **Codex provisional ranking (rigor×info-gain×He-elegance per GPU, novelty deferred to Pro):** ① **V1** (sharpest falsifier: joint≈independent≈shuffled on same residual positions; risk: accidental extra compute / K-selection leakage). ② **III1+II1 as ONE anti-truncation gate** (best match to actual headroom; falsifier: box/margin observer adds nothing over entropy+nfe+parser/suffix at matched NFE; risk: verifier-surface inflation). ③ **IV1** (best He-elegance speed bet IF novelty survives Pro; falsifier: A=0 or schedule/temperature rescale matches ETD, or gap doesn't grow at smaller K; risk: kernel operator misaligned with the model's actual reverse dynamics). I1 NOT recommended as lead (risks tying the v3 carriers → repeats "matches native").

## Stage 5 — R1 SOUNDNESS + R2 SIGNIFICANCE (independent Opus critics ≠ generators; top-3 leads)
**Tri-substrate convergence: V1 ranks #1 on BOTH soundness (R1: V1>IV1>III1+II1) and expected-outcome significance (R2: V1>III1+II1>IV1); Codex rigor ranked V1 #1 too.** Refinements:
- **V1 (uncommitted-residual joint)** — R1 SOUND-WITH-FIX (soundest of the three; symmetric class-closing falsifier, low hack surface). Fixes: (a) DEMOTE the `|residual|≥4 rescuable ≫0.006` OR-clause from WIN to diagnostic (it's an oracle upper-bound — same class as the dead always-deepen oracle); only method-achieved "joint ≥+2-3 abs verified at matched +1 forward" counts as a positive. (b) ADD an entropy-matched BENIGN cross-conditioning control (centroid/uniform, or self-SC-only) so a shuffled-degradation can't masquerade as coupling. (c) independent arm MUST get the same +1 forward on the same K. R2 MEDIUM-HIGH — deepest question (does per-position factorization lose anything?); positive headline "coordinated multi-token errors live in the uncommitted residual; one joint re-denoise recovers them"; likely-negative headline (still publishable, complements Track-1) "per-position factorization is free even in the high-entropy residual → why parallel decoding is safe."
- **III1+II1 (anti-truncation gate)** — R1 SOUND-WITH-FIX, HEAVIEST lift: the observable y=P(box present) is near-circular with the failure metric (no-box) → biggest verifier-surface hazard in the set. MANDATORY (promote from optional): primary metric = math_verify VERIFIED-CORRECT never box-presence; full anti-surface battery (parser-only/suffix/force-box-with-extracted-value); no-box vs wrong-box vs parse-fail stratification; III1 offline pre-kill = INCREMENTAL AUC over {entropy, box-present, final-entropy, nfe}; matched-NFE is data-dependent (emergent) → require full NFE-accuracy PARETO dominance, not a single matched-mean point; REFRAME win as speed-at-matched-quality (the accuracy-gain framing collides with the ~1% allocator ceiling). R2 MEDIUM — aims at the dominant failure (highest value IF clean) but significance hostage to the matched-NFE clause + verifier-surface contamination + decoding-heuristic flavor; built-in disambiguator (extend→force-box: correct=premature-readout / wrong=unfinished) makes even the negative useful.
- **IV1 (exponential integrator)** — R1 SOUND-WITH-FIX (cleanest matched-NFE, lowest hack surface) BUT conceptual risk: A is the FORWARD kernel's linear part; ETD needs the linearization of the REVERSE dynamics — e^{AΔ} may be a glorified step-size/temperature rescale; and A is linear in PROBABILITY space while N(model) is in LOGIT space (coordinate-split weakens the "principled" story). Fixes: add logit-temperature/step-rescale baseline + normalized/projected-Euler control; GATE on empirical-logit-decay-matches-ᾱ pre-check; A=0 is the decisive executioner. R2 MEDIUM — most He-ELEGANT shape, THINNEST headroom (~15-25% NFE best case) + HIGHEST contribution-swallow risk (same speed lane as the already-banked Track-1 frontier → must be orthogonal/multiplicative).
- **Promoter-consensus:** V1 promoted by ≥2 independent substrates (Codex rigor + R1 + R2) cleanly. Anti-truncation gate + IV1 promoted on soundness+significance WITH the fixes above (novelty pending Pro).

## Stage 3 — NOVELTY (Playwright→GPT-5.5 Pro 扩展, 2026-06-29, chat "ML Paper Prior-Art Audit")
Per-candidate overlap classification (LETHAL / NEAR-FRONTAL / DEFENSIBLE-SLICE):
- **III1+II1 (anti-truncation) — SPLIT:** **3a output-presence observer = DEFENSIBLE-SLICE** (novelty = task-conditioned verified-answer-presence stopping at matched mean compute, targeted at fixed-canvas hard-math truncation). **3b Voronoi-margin commit = NEAR-FRONTAL — Prophet (2508.19982, training-free top-2 confidence-gap early-commit) nearly pre-empts it** → demote margin to a commit-safety DIAGNOSTIC, and make it geometrically EXACT: distance ∝ (logit_i−logit_j)/‖e_i−e_j‖, NOT raw top-minus-runner-up (norms/temperature/bias matter). Observer must be framed as schema-aware answer-completion (not a MATH `\boxed{}` hack) + beat EB / Prophet / LESS / KLASS / "always spend more" at matched mean-NFE+wall-clock, with the truncation-rescue decomposition table (no-box→correct, NOT no-box→wrong-box).
- **V1 (uncommitted-residual) — NEAR-FRONTAL, defensible if sharply scoped.** Biggest threat **LRD (2510.11052, distributional mixtures + predictive feedback)**; also RCD (2601.22954), SCMDM (2604.26985), Loopholing (2510.19304), Fast-dLLM/APD/CoRe/ReMDM. Defensible slice = a frozen, on-manifold, ONE extra joint pass over ONLY the high-entropy uncommitted residual (accepted tokens fixed, no training, no new latent pathway). Must show TARGETED coordinated-error repair (multi-digit numbers/signs/units/boxed spans), not aggregate accuracy, and beat "one more vanilla denoise / remask-refine / random-residual / entropy-matched-residual" at matched compute.
- **IV1 (exponential integrator) — DEFENSIBLE-SLICE only.** Conceptually owned by **DPM-Solver (2206.00927) / DEIS (2204.13902) / DPM-Solver++ (2211.01095) / SEEDS / operator-splitting** ("integrate the linear part exactly, model the nonlinear residual" is OLD); discrete foundations D3PM (2107.03006), CTMC (2211.16750). Defensible slice = training-free ETD for a FROZEN production discrete dLLM exploiting the D3PM-uniform contraction-toward-centroid via the native SC channel. Overclaim risk: if the reverse dLLM dynamics aren't a calibrated probability-flow ODE, it's "a schedule trick dressed as numerical analysis" → MUST show the closed-form kernel-split beats a TUNED larger-jump schedule (not just changed steps). Bar: 1.5–2× (not 1.1×) at matched verified-acc, else an engineering footnote.
- **I1 (native-SC soft-carry) — LETHAL for the broad claim.** DiffusionGemma's OWN trained self-conditioning (logits→softmax·W→gated-MLP) + LRD/Loopholing/SCMDM/RCD/DSL-LLaDA/ELF crowd "continuous carrier until final discretization." Survives ONLY as a controlled interface ablation (native-SC on-manifold > off-manifold embedding-injection at matched budget) for #1/#2. Do NOT lead.
- ★ **NEW PRIOR-ART Pro surfaced (must-cite; reviewer ammunition):** *DiffusionGemma-specific papers already exist* — **arXiv:2606.14620** "Neither Parallel Nor Sequential: How DiffusionGemma Actually Commits Tokens" (analyzes commitment / EB-stopping / batching / early-stop) and **arXiv:2606.20560** "How Transparent is DiffusionGemma?" (native self-conditioning = softmax-logit·embedding via gated-MLP, EB re-noise/argmax). Commit/stop: EB-Sampler (2505.24857), Prophet (2508.19982), LESS (2606.16908), KLASS (2511.05664), Stability-Weighted Decoding (2604.17068). Length/truncation: **DAEDAL (2508.00819), ρ-EOS (2601.22527), LR-DLLM (2602.07546), VSB/"When to Commit?" (2604.23994)** — directly address variable-length/EOS in masked dLMs (must differentiate for #3).
- **Pro's lead recommendation:** LEAD with **#3 (anti-truncation, observer-first, margin-as-diagnostic)** — the only one cleanly attacking the stated dominant failure with real-WIN (not match-faster) potential; PAIR with **#2/V1** if residual-repair evidence is real; keep **#1** as an optional acceleration layer; DEMOTE **#4** to an ablation. Title-level claim: *"frozen discrete dLLMs fail hard math not because they can't reason, but because local entropy-bound stopping is misaligned with global answer completion; a schema-aware closed-loop stop controller recovers truncation at fixed mean compute."*
- **★ DIVERGENCE to adjudicate at SELECT:** Pro (novelty×headroom×elegance) → LEAD #3 anti-truncation. Codex-R4 + R1-soundness + R2-significance → V1 first (soundest, cheapest-decisive, symmetric class-closing falsifier, lowest hack-surface). Not contradictory if ordered: V1 = cheapest decisive probe + bankable clean negative (gates V2); #3-observer = highest-headroom real-WIN lead method (with the full anti-verifier-surface battery + matched-NFE Pareto + de-scoped margin). Codex Stage-6 SELECT adjudicates the execution order.

## Reject→Accept action list (carry to dispatch)
- All anti-truncation arms (II1/III1/II2/II4): add the **anti-verifier-surface battery** (parser-only / answer-suffix / force-box-with-random-value baselines; stratify no-box vs wrong-box vs parse-fail; report REAL verified correctness, not box-presence).
- V1: pre-register K-selection rule WITHOUT method outcomes; charge the +1 joint forward in NFE; ship the shuffled-cross-conditioning negative + the |C|≥4-rescuable-vs-0.006 comparison.
- IV1: ship the A=0 control + native-schedule/temperature-rescale control + v3 right-metric/top-k carrier baselines; the WIN signature is "gap grows as K shrinks."
- I1: head-to-head vs g4_soft_cont/g4_cosine_snap/g4_logitargmax_snap/top-k/LRD at EXACT matched NFE; promote only if it BEATS (not matches) native AND those carriers.
- Novelty status: **Pro 扩展 audit COMPLETE** (Stage 3 above). Dedicated Codex Stage-6 SELECT in-flight to confirm execution order; reconciled SELECT below.

---

## Stage 6 — SELECT (independent selectors reconciled) + FINAL RANKED SHORTLIST
Two independent selectors disagreed on the *lead* but agree once framed as execution ORDER (not either/or):
- **Rigor axis** (Codex R4 + R1 soundness + R2 significance): **V1 first** — soundest, cheapest, symmetric class-closing falsifier, lowest verifier-hack surface, gates V2.
- **Novelty×headroom axis** (Pro 扩展 + Pro AC-ranking): **#3 anti-truncation observer is the LEAD METHOD** — only candidate cleanly attacking the dominant failure (truncation) with real-WIN (not match-faster) potential; defensible slice = schema-aware verified-answer-presence stopping at matched mean compute.
- **Reconciliation (the actual program):** run the **cheapest-decisive probe first, then the highest-headroom lead method**, both with their mandated controls. This is what both axes endorse.

### FINAL RANKED SHORTLIST (pick = the program; execute top-down)

**① LEAD-A / FIRST PROBE — V1: uncommitted-residual joint re-denoise** (cheapest, soundest, decisive)
- One principle: per-position factorization is the load-bearing assumption of parallel diffusion decoding — test it where it's *un-killed* (the high-entropy residual; M-PCRH killed only the committed set, |C|≥4 rescuable 0.006).
- WIN = at matched +1 forward, joint ≥ +2–3 abs verified on MATH-L5/AIME with repair CONCENTRATED on coordinated spans (multi-digit numbers/signs/units/boxed). NEGATIVE = joint ≈ independent ≈ shuffled ⇒ a clean structural law ("factorization is free even in the residual → why parallel decoding is safe"), completes M-PCRH, complements Track-1.
- Controls (R1/Codex/Pro-merged): same K positions both arms; same +1 forward to the independent arm; shuffled-cross-conditioning negative; entropy-matched BENIGN cross-conditioning (rules out shuffle-poison); locality on high-MI spans; DROP the oracle `|C|≥4 rescuable` OR-clause as a WIN (diagnostic only); pre-register K by entropy WITHOUT method outcomes. Novelty: NEAR-FRONTAL vs LRD → scope as frozen, on-manifold, residual-only, no training.
- Cost ~very low; gates V2 (residual-restricted Anderson) only if V1 CI-LB ≥ +2pp.

**② LEAD-B / HEADROOM METHOD — III1+II1 (observer-first): closed-loop output-presence stop** (highest real-WIN ceiling on the dominant failure)
- One principle: the native stop is open-loop on LOCAL token entropy, but verified hard-math needs a GLOBAL answer object present → close the loop on schema-aware answer-presence, reallocating a FIXED mean budget from solved to truncation-prone instances.
- WIN = matched mean-NFE + matched wall-clock, statistically-significant verified-acc gain on MATH-L5/AIME via the truncation-rescue decomposition (no-box→correct UP, regression DOWN), beating EB / Prophet / LESS / KLASS / "always spend more". NEGATIVE (still publishable) = extend-then-force-box yields confident-wrong ⇒ "unfinished reasoning, not premature readout" — closes the smarter-stopping class for this model.
- MANDATORY controls (R1/Codex/Pro): primary metric = VERIFIED-CORRECT never box-presence; anti-verifier-surface battery (parser-only / suffix / force-box-with-extracted-value); no-box vs wrong-box vs parse-fail stratification; full NFE-accuracy PARETO dominance (mean-NFE is emergent, not a knob); schema-aware (not a MATH-`\boxed{}` hack). **De-scope 3b: Voronoi-margin → commit-safety DIAGNOSTIC only** (Prophet 2508.19982 pre-empts the margin-as-commit-signal), and make it geometrically exact ∝(logit_i−logit_j)/‖e_i−e_j‖. Must differentiate DAEDAL/ρ-EOS/VSB/LR-DLLM (length/EOS) + the DiffusionGemma-specific 2606.14620/2606.20560.

**③ SIDECAR — IV1: exponential-integrator kernel-splitting** (most He-elegant shape; speed layer)
- Defensible slice = training-free ETD for a frozen production discrete dLLM exploiting the analytic D3PM-uniform contraction-toward-centroid via the native SC channel. Run as an acceleration layer on top of ①/② ONLY if it cleanly cuts NFE without hurting truncation rescue. Bar: 1.5–2× at matched verified-acc + ablation that the kernel-split beats a TUNED larger-jump schedule (A=0 control decisive) + gap-grows-as-K-shrinks signature; else a solver footnote. Novelty DEFENSIBLE-SLICE only (DPM-Solver/DEIS/DPM-Solver++/SEEDS).

**④ ABLATION ONLY — I1: native-SC vs off-manifold-hook carrier** (novelty LETHAL as a standalone) — keep solely as the interface control showing ①/② should route through the native trained SC channel, not the off-manifold embedding hook.

**REJECTED (Codex R4):** I2, I3 (initializer/over-relax tuning), II2/II3/II5 fold into ②'s battery or the dead-allocator, III2/III3 (subsumed by ②), IV2/IV4 (generic acceleration; behind IV1), IV3 (designed-negative control, not a candidate), V2 (gated behind V1).

**Most novelty-sensitive (reconcile if Codex dedicated-SELECT or a deeper scan flips):** ② depends on Prophet/EB/KLASS differentiation surviving; if the observer ties them at matched NFE, ② degrades to the clean-negative ("stopping isn't the lever"). ① is novelty-robust (the finding is publishable either direction).

**Independent Codex selection** = satisfied by the **R4 provisional ranking** (Codex independently ranked V1 > anti-truncation gate > IV1, with falsifiers + first-run risks), reconciled here with Pro 扩展's novelty+AC ranking and R1/R2. A dedicated 4th Codex SELECT call was dispatched as extra confirmation but stalled (~6 min no output, xhigh); NOT blocked on — it is redundant with R4+reconciliation. If it lands with a divergence it gets appended here.

**STOP AT IDEAS.** Dispatch (worktree executor for ① V1 first — cheapest decisive, then ② observer with the anti-surface battery) is the SEPARATE next step, per the skill + the directive's "FIRST STEP = /ideate (reflect, don't execute yet)."


---
## LOOP PROGRESS (continuous-loop dispatch)
- **① V1 (uncommitted-residual joint) — DISPATCHED → CLEAN NEGATIVE (banked, Codex DECIDE ratified, 2026-06-29).**
  Dev L5-dev-40@2048 (pre-registered non-sealed split): joint=native=0.900, FIXED 0 wrong→right; no locality
  (random=joint), correct-SC≈uniform-SC, channel-live (shuffled poisons), model at fixed point (plus1 moved 140/0
  fixes). Extends M-PCRH → factorization free even in the residual (complements Track-1). Class CLOSED; sealed
  holdout (L5[40:134]+AIME) preserved. Tree 5.9.1 done. Branch v1-residual @369eea7.
- **② III1+II1 anti-truncation observer — DISPATCHING (builder).** Truncation headroom is at budget 768/1280
  (no-box high), not @2048. Matched-mean-compute (bank-on-solved / spend-on-truncation) is the non-trivial test
  vs the dead allocator; full anti-verifier-surface battery + Pareto + margin-as-diagnostic mandatory.
