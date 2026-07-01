# Ideas — Gradient-Field / Embedding-Flow on Frozen DiffusionGemma (Track 2)

> Output of the `research-ideation` pipeline (Arbor-decoupled). Stops at a ranked, review-survived
> shortlist; executing a winner is a separate step (worktree subagent). Started 2026-06-28.
> Engines: Opus (generate/explore/R1-R2-R5) · Codex `codex:codex-rescue` (R4 rigor + SELECT) ·
> Playwright→GPT-5.5 **Pro 扩展** (novelty R3 + AC; project override = Pro-only tier).

## Stage 0 — Brief
- **Claim space:** does a LIGHTWEIGHT ADAPTER on **FROZEN DiffusionGemma 26B-A4B** (block masked
  discrete-diffusion MoE; 256-canvas; D3PM-uniform *discrete-token* corruption; ~44.5-step
  EntropyBoundSampler; tied embed/lm_head dim 2816, scale √2816; **no timestep signal anywhere**), using
  Kaiming-He-line targets (JiT clean-prediction · MeanFlow average-velocity · pMF output=clean/loss=velocity
  separation · ELF embedding-flow · MAR+DiffLoss continuous-token), improve **verified generation** —
  primarily **few-step accuracy-vs-NFE**?
- **Frontier:** Track 1 ratified — frozen dLLM = MATH-L5 **0.823 @ ~44.5 NFE / 770 tok / 5.05 s**, 5–7×
  faster than its AR sibling; edge = NFE/token-depth efficiency. dLLM by budget: MATH-L5 0.56@768 /
  0.80@1280 / 0.82@2048; AIME-24 0.16@768 / 0.41@1280. E (learned commitment) **killed**; A (reference-token
  non-observability) **falsified** (t=1.0 artifact); H4 retired (no-t, non-identifiable); H5 (feed-t into
  frozen router) built but **AMBIGUOUS on diffusion loss + never generation-evaluated**. He-line branch
  (tree node 5.3) DEFERRED, **never built**.
- **Goal anchor:** a rigorous positive-OR-negative finding, NeurIPS/ICML/ICLR tier. Negatives = success.

## Stage 1 — Landscape (solved / tried-dead / open / borrowable)
- **Solved/ratified:** wall-clock frontier (above); empirical sampler ~44.5 steps (max 48, early-stops ~93%,
  entropy_bound 0.1); soft-embedding projection `softmax(logits)@W_embed·√d` already exists in-model.
- **Tried-dead:** E, A, M-PCRH, H4, H5 (see frontier). Do not re-tread.
- **Open (never built):** node 5.3 He-line — C1 clean-prediction-toward-verifier-utility, C2 few-step/MeanFlow,
  C3 ELF embedding-flow adapter.
- **Borrowable infra:** D3PM corruption, block-diffusion loss, LoRA attach (router/experts frozen), two-pass
  forward, embedding/lm_head access — all in `diffusiongemma_sft/`. **H5's reusable "feed-t-externally"
  mechanism** = `sinusoidal_time_embedding → per-layer MLP → reversible router monkeypatch`
  (`worktrees/agent-a4607307e978848fb/diffusiongemma_sft/router_t_adapter.py`). Wall-clock harness
  (`gen_dllm/verify/analyze`) + verifiers + AR sibling on `worktree-agent-aa411b381a8c95d40`.
- **Must-build:** continuous embedding corruption `x_t=a(t)x+s(t)ε`; velocity/embedding loss; embedding-space
  flow/ODE sampler; few-step NFE control (shipped sampler can't be forced to N steps).
- **Decisive constraints:** (i) no-t → any flow head must be **fed t externally** (H5 pattern); (ii) hidden
  states are **discrete-CE-shaped** → "indifferent, not hostile" to continuous embeddings — *this risk IS the
  research question*; (iii) **diffusion loss is an invalid quality proxy** → verified-generation only;
  (iv) near-ceiling → only high-headroom positive is **few-step (≤12 NFE) at ~0.80 MATH-L5**, else a clean
  negative; (v) few-step = **distillation** → novelty risk vs SDTT/MeanFlow/consistency.

## Stage 2 — Probe Block
```
Q1 bottleneck CLASS = OBJECTIVE/REPRESENTATION + STOPPING. Quality near-ceiling but sampling ~44.5 NFE;
   hidden states discrete-CE-shaped → whether they encode a continuous clean-embedding/velocity field is open.
Q2 hidden assumption = "a dLLM's denoising target must be discrete-token CE / mask-recovery." Drop it →
   predict clean EMBEDDING / embedding-VELOCITY, loss in flow space, output via tied lm_head → opens few-step
   (average-velocity) generation + a measurement of whether discrete features carry continuous structure.
Q3 elephant = the He-line is measured by FID/quality; THIS model has no quality headroom + diffusion loss is
   invalid → the only honest payoff is NFE-at-matched-verified-accuracy, or a negative.
Q4 Hamming = YES: "can a frozen discrete dLLM be made few-step by a light embedding-space velocity head?" is
   the most important + novel + verifier-measurable slice; it extends our one ratified positive.
```

---

## Candidates (de-duped by mechanism; 5-field MechanismHypothesis). Strong cross-generator convergence.

### Cluster G — Cheap no-training GATES (measure-first; all 4 generators led here)

**G1 — Free soft-embedding centroid vs argmax** (zero-fit, ~2 GPU-h)
- silent_axiom: the in-model soft-embedding centroid `softmax(logits)@W_embed·√d` is a throwaway intermediate;
  only the argmax/sampled token is decision-usable.
- mechanism: decode the model's OWN soft-embedding centroid by nearest-neighbour in the tied table (0 params).
- hypothesis: at high-entropy positions (those that drive truncation errors) the centroid points into the
  correct **equivalence-class** region better than argmax, because a diffuse softmax averages over a valid
  synonym set instead of collapsing to one mode.
- observable: verified-token accuracy (equiv-class, band t~U(0.4,0.8)) of centroid−argmax on top-quartile-entropy
  positions; **GO if ≥ +3 pts**.
- falsifier: 200 verified GSM8K/MATH traces, forward-only. neg-control: random (non-high-entropy) positions ≈0.
  equal-compute: argmax at identical #forwards. holdout: AIME-24. *kill if centroid ≤ argmax.*
- tags: cost ~2 GPU-h · novelty LOW (we READ the centroid, don't train a velocity loss) · threatened_by (iv).

**G2 — Oracle linear clean-embedding readout** (closed-form ridge, ~4 GPU-h + CPU) — PROGRAM GO/NO-GO
- silent_axiom: discrete-CE hidden states do NOT linearly encode the clean continuous target embedding e₀.
- mechanism: one ridge map W: hℓ(t)→e₀ (gold-token embedding) fit on verified traces; decode ê₀ via NN/lm_head.
- hypothesis: the clean-embedding direction is linearly present mid-depth (it must be, to feed the in-model
  soft-embedding projection) → an oracle W decodes a token beating native argmax, quantifying the headroom a
  trained velocity head could capture.
- observable: held-out verified-token acc of ê₀-decode − native argmax (band t~U(0.4,0.8)); **GO for the program
  if ≥ +5 pts; clean NEGATIVE for the whole velocity-head program if ≤ +1.**
- falsifier: fit 5k / test 5k held-out positions. neg-control: shuffle e₀ targets → ≤ native (rules out leakage).
  equal-compute: PCA-then-argmax at matched rank. holdout: layer sweep + AIME.
- tags: cost ~4 GPU-h · novelty MED (we test *decodability* as a gate; RADD/JiT ship a head) · threatened_by G1.

**G3 — Soft-embedding ingestion feasibility probe** (no training, ~3-8 GPU-h) — INGESTION GATE
- silent_axiom: the frozen backbone can ingest off-manifold convex combinations of vocab embeddings (soft tokens).
- mechanism: each step feed the previous step's token-distribution **expectation** `Σ pᵢeᵢ` (temperature τ) into
  the soft-embedding pathway instead of a hard token.
- hypothesis: carrying the soft expectation forward preserves per-step distributional info that hard sampling
  destroys → verified answer reached in fewer revealing steps.
- observable: at matched NFE soft-carry ≥ hard baseline; soft-carry hits 0.80 MATH-L5 at **≤25 NFE**; acc(τ)
  curve (τ→0 must recover hard baseline; collapse for all τ>0 = broken manifold).
- falsifier: for ALL τ∈{0.1..1.0} soft-carry < hard at every NFE → **kills the continuous-flow program**
  (G2/H1/H2/H3). neg-control: τ→0 reproduces hard baseline (wiring sanity). equal-compute: equal NFE. holdout: AIME.
- tags: cost ~3-8 GPU-h, no training · novelty LOW (diagnostic) · threatened_by (ii) — soft states are strictly
  off-manifold inputs the net never saw (D3PM gives a real token or [MASK], never a blend).

**G4 — Training-free embedding-DDIM sampler** (inference-only, ~5-15 GPU-h)
- silent_axiom: getting few-step out of this model requires *training* a new head.
- mechanism: each step take the frozen model's clean-token argmax over all positions, embed it, take a
  DDIM-style linear step in embedding space toward it, re-noise, snap-to-token; 4-12 steps, 0 new params.
- hypothesis: the model's own clean prediction is already a usable jump target — DDIM-on-embeddings extracts
  few-step behaviour for free **iff** the embedding manifold is smooth (direct cheap probe of risk ii).
- observable: training-free 8-NFE verified MATH-L5 > frozen-sampler-capped-at-8-NFE by **≥ +0.03**.
- falsifier: sweep NFE∈{4,6,8,12} sealed; **kill the continuous-flow direction if it NEVER beats frozen-capped
  at any budget**. neg-control: random-direction embedding step. holdout: AIME.
- tags: cost ~5-15 GPU-h · novelty MED (DDIM/x0-samplers) · threatened_by (ii).

**G5 — NFE-floor oracle** (oracle scheduling, inference-only, ~30-60 GPU-h) — bounds the WHOLE schedule/commit class
- silent_axiom: the frozen 44.5-step denoiser *contains* a ≤12-step verified generator a light head can "unlock."
- mechanism: keep the frozen per-step call; replace the heuristic remask/commit/stop with an ORACLE; sweep NFE;
  read the NFE-floor = min NFE for oracle scheduling to reach 95% of full-NFE verified accuracy.
- hypothesis: few-step fails because the verified computation is distributed across the per-step *map*, not the
  schedule → no light scheduling head over the same calls can compress it.
- observable: oracle-scheduled acc at NFE≤12 stays ≤ baseline@12 + 3pp while full-NFE hits ceiling → floor ≫12.
- falsifier (oracle = upper bound): oracle ≥ any learned schedule; if oracle reaches ≥95% full-NFE acc at NFE≤12
  the negative is OVERTURNED (commitment program alive). neg-control: random commit-order ≤ heuristic.
- tags: cost ~30-60 GPU-h · novelty MED · excludes-if-fires: the ENTIRE scheduling/commitment class (re-derives
  the E-kill as a structural floor) · threatened_by (iii).

**G6 — Truncation budget-vs-information arbiter** (no-early-stop, ~8 GPU-h) — LEVER ARBITER
- silent_axiom: truncation loses accuracy because the model lacks the info at stop-time (a representational gap).
- mechanism (inversion): oracle no-stop — run the sampler to a large fixed cap (disable early stop) and verify.
- hypothesis: truncation is a stopping-heuristic artifact, not a representational gap → removing early-stop
  recovers most AIME/MATH-L5 failures → redirects the program from embedding heads to a stop/length controller.
- observable: AIME-24 gain from no-early-stop vs default; **≥+10 pts → embedding heads DEPRIORITIZED; ≤+2 →
  truncation is representational → heads justified** (report tokens/wall-clock to stay honest vs the lead).
- falsifier: re-run AIME/MATH-L5 at extended cap. neg-control: extended steps on already-correct must not regress.
- tags: cost ~8 GPU-h · novelty LOW (diagnostic) · arbitrates G2/H1/H2/H3.

### Cluster H — Few-step velocity / clean-prediction HEADS (the payload; training, GATED on Cluster G)

**H1 — MeanFlow average-velocity embedding-ODE head** (~40-80 GPU-h) — highest ceiling
- silent_axiom: a discrete-diffusion dLLM *must* take ~44 small steps (intrinsically un-jumpable trajectory).
- mechanism: a per-layer **average-velocity adapter head** fed external (r,t) that predicts the MeanFlow average
  velocity u(x_t,r,t) from the partially-masked canvas embedding to the clean-answer embedding; inference =
  4-12-step embedding-ODE, snap to tokens via tied lm_head once/step.
- hypothesis: average-velocity helps because the bottleneck is per-step commit granularity not capacity — the
  frozen backbone already encodes the answer manifold; averaging converts many local commits into a few large
  well-conditioned jumps (and smooths the field, partly defusing ii).
- observable: few-step acc-vs-NFE strictly dominates the frozen frontier (AUC Δ CI-LB>0) with **MATH-L5 ≥0.80
  at ≤12 NFE**.
- falsifier: train ~1M-param head on verified rollouts, 8-NFE on sealed MATH-L5; kill if acc<0.80 AND ≤
  frozen-capped-at-8. neg-control: shuffled (r,t) per row must collapse gain. holdout: AIME.
- tags: cost ~40-80 GPU-h · novelty HIGH (MeanFlow/iMF vision + SDTT 2410.21035) — delta = avg-velocity
  continuous flow on a FROZEN DISCRETE-dLLM tied embedding · threatened_by (ii).

**H2 — Decoupled clean-out / velocity-loss adapter (pMF separation)** (~40-80 GPU-h) — de-risked sibling of H1
- silent_axiom: few-step heads must regress velocity — but a dLLM is natively an x0-predictor, so forcing
  velocity output fights the frozen parameterization.
- mechanism: an adapter that **outputs the clean-answer embedding** (the regime the backbone already produces)
  but is **trained with a pMF velocity-space loss**, then few-step-sampled by finite-differencing the
  clean-prediction sequence.
- hypothesis: matching output to the backbone's native clean-prediction while supervising in velocity space
  keeps every query on-manifold → few-step integration well-conditioned even if the raw velocity field is rough
  (routes around the ii-risk that threatens H1).
- observable: at matched NFE, H2 frontier-AUC ≥ H1 and ≥ frozen; MATH-L5 **≥0.78 at ≤12 NFE** with lower
  off-manifold/garbage-rate than H1.
- falsifier: H1-vs-H2 head-to-head equal NFE/data sealed; kill H2 if it beats neither frozen-capped nor H1's
  garbage-rate. neg-control: clean-out head with plain CE (no velocity loss) — if it matches H2, velocity loss
  is inert. holdout: AIME.
- tags: cost ~40-80 GPU-h · novelty HIGH (pMF vision) — delta = "x0-native backbones are the natural pMF host,
  first in a discrete dLLM" · threatened_by (v) distillation overlap.

**H3 — Self-distilled embedding-velocity head, high-entropy-only** (~24 GPU-h) — GATED on G1/G2/G6
- silent_axiom: improving a near-ceiling model needs a better objective on ALL positions.
- mechanism: a ~1M-param residual head v(h) nudging the soft-embedding centroid toward its OWN more-denoised
  later-step centroid (self-distilled one-step embedding-velocity), applied only where entropy is high.
- hypothesis: a self-distilled velocity nudge on high-entropy positions raises verified gen by giving the
  parallel sampler a better one-step clean-embedding estimate exactly where it commits prematurely.
- observable: verified acc on AIME/MATH-L5 vs frozen at **equal wall-clock**; GO if ≥+3 pts at no wall-clock cost.
- falsifier: train head ~1 GPU-day. neg-control: apply to RANDOM positions → no gain. equal-compute: spend the
  head's extra forwards on more sampler steps. holdout: MATH-500 non-regression.
- tags: cost ~24 GPU-h · novelty HIGH (pMF/MAR-DiffLoss) — delta = self-distillation-from-own-trajectory +
  high-entropy-only + frozen backbone · threatened_by (i)(ii)(iv).

**H4 — Verifier-curated success-conditioned reflow adapter** (~60-120 GPU-h) — lowest SDTT overlap
- silent_axiom: distillation straightens the student toward the teacher's full output distribution (which
  contains the teacher's wrong answers) → the student inherits error modes.
- mechanism: a rectified-flow **reflow adapter** trained ONLY on verifier-confirmed-correct finals: embed the
  correct answer, continuous-corrupt, train (r,t) adapter to predict the straight velocity back to the correct
  embedding.
- hypothesis: deleting wrong-answer mass from the flow target straightens the field toward correct manifolds →
  a few big steps land on correct answers more often (few-step error compounds along contaminated targets).
- observable: at 8 NFE, verified-only adapter beats all-rollouts adapter by **≥+0.05 abs MATH-L5** and ≥0.75 abs.
- falsifier: verified-only vs all-rollouts at equal data count, @8 NFE sealed; kill if gap<0.05 or abs<0.75.
  neg-control: train on verifier-WRONG-only (must be strictly worse). holdout: AIME.
- tags: cost ~60-120 GPU-h · novelty MED-HIGH (SDTT + rectified-flow reflow) — delta = external-verifier
  data-selection on the flow target · threatened_by (iv)(v).

### Cluster N — Designed-as-negative oracle bounds (publishable kills that exclude ≥2 hypotheses)

**N1 — Embedding-space straight-line decodability oracle** (oracle MeanFlow integrator, ~20-40 GPU-h)
- mechanism: at each of K few-step nodes inject the ORACLE average velocity (displacement to the teacher-forced
  clean embedding), integrate in embedding space, decode intermediates via tied lm_head.
- hypothesis (negative): embedding few-step FAILS because discrete-CE hidden states make the straight-line
  interpolant decode to incoherent intermediates → the trajectory is not embedding-integrable.
- observable: oracle integrator ≤ baseline@NFE even WITH oracle velocity; intermediate token-validity collapses
  at low NFE. **Overturn:** oracle reaches ≥95% full-NFE acc at K≤12 → field IS integrable → build the adapter.
- falsifier/oracle bound: oracle velocity ≥ any learned head. neg-control: shuffled/wrong clean target worse.
- excludes-if-fires: BOTH continuous-embedding-velocity-adapter AND embedding-consistency-distillation.
- tags: ~20-40 GPU-h · novelty MED-HIGH (MeanFlow target as oracle diagnostic on a frozen discrete dLLM).

**N2 — Wrong-space inversion: embedding vs logit-simplex vs hidden** (~25-45 GPU-h)
- mechanism: run the N1 oracle integrator in three spaces — (a) tied-embedding, (b) pre-softmax logit/simplex
  (where D3PM actually operates), (c) hidden-state — compare verified-gen-vs-NFE.
- hypothesis: embedding-space velocity FAILS while logit-simplex is better → the He-line *space choice* is the
  error, not the adapter.
- observable: embedding-oracle ≥10pp WORSE than logit-oracle at NFE≤12 → He-line continuous-embedding framing
  specifically refuted; if both fail within 2pp → space is not the issue (deeper compose bound, N1).
- excludes-if-fires: "embedding is the right space" (favor categorical-flow) OR both → both light-adapter programs.
- tags: ~25-45 GPU-h · novelty MED (head-to-head oracle-per-space on a frozen MoE dLLM is new).

**N3 — "Missing-t is NOT the bottleneck" ablation ladder** (~40-80 GPU-h) — extends/bounds H5
- mechanism: a t-conditioning ladder on the velocity head — {no-t, discrete mask-ratio (H5 surrogate), oracle
  continuous-t per-layer FiLM} at fixed NFE.
- hypothesis: feeding t FAILS to move verified-gen-vs-NFE because the binding constraint is the frozen per-step
  map; t helps diffusion LOSS (reproducing H5) but NOT verified few-step accuracy — a loss/metric dissociation.
- observable: verified-gen flat (±2pp) across the ladder while diffusion loss improves monotonically with t.
  **Overturn:** oracle-continuous-t-FiLM lifts verified-gen ≥5pp at NFE≤12 → missing-t was real.
- excludes-if-fires: "add-timestep-fixes-few-step" AND retroactively bounds H5 (loss-gain ≠ gen-gain).
- tags: ~40-80 GPU-h · novelty LOW-MED (vs H5/TimeStep-Master) · the loss/gen dissociation is the contribution.

### Cluster X — adjacent / lower-priority (parked unless a gate redirects here)
- **X1 Uncommitted-residual joint re-denoise** (~6 GPU-h): mask top-K high-entropy *uncommitted* positions and
  run one joint frozen re-denoise — tests the M-PCRH death insight ("coupling lives in the uncommitted residual").
  Off the strict He-line but cheap + decisive vs a prior kill.
- **X2 Stochastic-interpolant mask↔token bridge** (~10-25 GPU-h): graded `e_t=α·e_clean+(1−α)·e_[MASK]` input;
  novelty MED; analogy misleads ([MASK] is an absorbing sink, no half-masked data support).
- **X3 Adaptive unmasking schedule / commit-or-jump gate** (~15-40 GPU-h): **HIGH overlap with
  Learning-Unmasking-Policies 2512.09106** (flagged near-pre-emption) — deprioritized.

---

## Convergence finding (all four independent generators)
1. **Run a cheap no-training GATE first** — the program's whole value rides on one fact: do the frozen
   discrete-CE hidden states / embedding manifold host a decodable continuous clean-embedding/velocity field?
   Candidates G1/G2/G3/G4 are 2-15 GPU-h decisive probes of exactly this.
2. **Two arbiter probes** (G5 NFE-floor, G6 truncation-budget) tell us whether *representation* is even the
   right lever before any head is trained — and either can bank a clean publishable negative.
3. **The payload (Cluster H) is GATED**: only fund a velocity/clean-prediction head if a gate shows life.
4. **Designed negatives (Cluster N) use ORACLE upper bounds** → a failure reads "even the oracle can't,"
   excluding ≥2 hypotheses (decisive, not "our method failed").

---

## Stage 6 — SELECT (Codex, independent)
**Pick = G4 (training-free embedding-DDIM few-step sampler).** Codex rigor pass flagged **G1/G2 as TRAPS**
(reduce to reference-token / equivalence-class diagnostics → replay the *falsified-A* failure mode; cannot
license Cluster-H). G4 wins: cheap, no-training, **directly measures verified few-step accuracy at controlled
NFE**. Sharpest falsifier: across sealed NFE {4,6,8,12}, G4 never beats the frozen capped-NFE sampler by a
meaningful margin on verified MATH-L5. Risks: (1) false negative from the crude argmax→embedding DDIM path (a
learned head could pick a better trajectory) — so a G4 negative routes to **N1 (oracle bound)** before
abandoning; (2) implementation confound in the capped-NFE baseline. Positive → **H2** (pMF clean-out, has a
plain-CE inertness control); negative → **N1**.

## Stage 3 + 4 — Novelty + formal design (Pro 扩展, 2026-06-28) → `plan/archive/gpt55pro-G4-design-2026-06-28.md`
- **Novelty:** no lethal pivot for the exact combination; defensible slice = *"intervention-level
  verified-generation test for whether a frozen large discrete masked-dLLM hosts a decodable continuous
  clean-data / average-velocity field in its tied embedding space."* Closest threats: ELF (trains end-to-end;
  we probe a frozen checkpoint), Loopholing (trains the soft-carryover pathway; we externally probe + oracle
  arm), MeanFlow/iMF/pMF/JiT (vision/from-scratch), SDTT/DiMO/CDLM (distillation/consistency), ReMDM/Fast-dLLM
  (inference samplers = direct G4 baselines).
- **Design (frozen build contract):** G4-SOFT (no-param forward hook = the REAL test) vs G4-HARD (token-only
  control whose negative does NOT falsify the program); linear mask→clean bridge schedule; snap_E primary;
  fair Native-K-rescaled/subsampled baselines (not first-K-of-48); N1a (codec sanity) + N1b (oracle-to-basin,
  avoids final-clamp tautology) = decisive structural kill. GO ∃K Δ≥0.03 & bootstrap LB>0; N1 structural kill
  max_K A_N1b<0.95·A_full≈0.7885. Venue: G4 alone=workshop/Findings; G4+N1 decisive-negative=top-venue-plausible.
- **Stage 5 peer review:** compressed to the goal-directive's two independent gates (Codex rigor+SELECT above;
  Pro novelty+AC here) — same-substrate Opus R1/R2/R5 dropped as redundant per the autonomy directive.

## NEXT — DISPATCH (separate step; this skill stops at ideas)
Worktree subagent builds G4-SOFT / G4-HARD / Native-K-rescaled / Native-K-subsampled / N1a / N1b per the build
contract, runs a 32-problem DEV smoke FIRST (hook / no-NaN / tokenizer / verifier), reports; Codex adjudicates
before the sealed MATH-L5 run. Tree node 5.3.1.
