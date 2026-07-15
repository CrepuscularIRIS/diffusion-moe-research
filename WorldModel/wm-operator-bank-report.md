# World Model Operator Bank — corrosion audit of the Taste Operator Bank (opus-pass, 45 cards)

**Scope.** Full audit of `operators.md` (45 KEEP cards = 43 object-shift + 2 meta) against the world-model (WM) domain as defined in the brief; discovery pass over WM literature and adjacent fields; promoted WM cards; two-GPU generation-test plan. Research cutoff July 2026.

**Evidence grades used throughout:** `[paper]` established by a primary paper · `[claimed]` author-claimed, not independently reproduced · `[repo]` observed directly in repository code during this audit · `[inferred]` researcher inference · `[unverified]` plausible from memory but not re-checked against a source in this pass.

**Missing inputs.** `source-episodes.md` and `anti-patterns.md` were not provided; where the bank references them, provenance is taken at face value and flagged. Nothing in this audit depends on their contents.

---

## A. Executive summary

**How much of the bank transfers.** Of the 43 object-shift cards, only **3 are genuinely WM-native** (belief-ization, context-ization, skill-option-ization; latent-variable-ization and information-bottleneck-ization are WM-native historically but saturated — they are the incumbent, not a hypothesis generator). **2 are WM-adaptable** with a real rewrite (memory-kernel-closure, multiscale-correction-hierarchy), and **5 merge** into 3 sharper WM operators (observable-lifting + collective-variable-ization → `transfer-operator-ization`; ratio-ization → `policy-ranking-ization`; invariant-ization + operator-lifting → into `transition-family-factorization`). **12 are WM-conditional** (valid only under an explicit regime: multi-object pixels, safety constraints, physical structure, redundant sources, external memory, diffusion backbone). **~14 archive** (meaningful, no WM probe), and **5 are killed for WM**: graph-ization, distribution-output-ization, chunk-ization, polarization-ization, and bits-back-refund-pricing — the last because in WM the KL-refund *is* the incumbent RSSM objective (PlaNet/Dreamer ELBO), so the deletion test fails by construction.

**Bias diagnosis.** The bank's ★ grants were earned on VLA-robustness, VLA-fusion, diffusion-LLM, and speculative-decoding campaigns. Cards whose stars come only from those campaigns (chunk-ization, polarization-ization, dependency-bounded-assembly, selection-output-ization, affordance/correspondence-field) have **no valid WM generation test** and were demoted or archived here. The most VLA-biased card is **chunk-ization** (ACT-lineage action chunking: its benefits — imitation smoothness, per-step-verification cost — do not survive translation into a WM differential that skill-option-ization or multiscale-correction doesn't already make).

**New operators discovered.** Three promoted: `model-exploitability-objectization` (policy-conditioned error replaces average error; addresses the central WM pathology, failure signatures 2/10/11), `policy-ranking-ization` (ordinal decision-order preservation as the modeled object; the WM rewrite of ratio-ization, carefully deduped against value equivalence), and `event-triggered-re-anchoring` (innovation-gated replanning/state-refresh replaces fixed-cadence planning; classical in control [paper: event-triggered MPC], transfer to learned latent WM planners open as of 2026-06 [claimed: AdaJEPA lists it as future work, arXiv 2606.32026]). One promoted as META: `oracle-factorization-of-WM-errors`. One important **negative** discovery: horizon-adaptive imagination (a §14 candidate) is **already saturated in 2025–26** — Neubay (arXiv 2512.04341) makes uncertainty-adaptive truncation its decisive component in offline MBRL, and ELVIS (arXiv 2605.04709) does uncertainty-triggered soft truncation for visual latent MPC — so "adaptive horizon" is recorded as an incumbent formulation and a new anti-pattern entry, not a card.

**Net result.** 45 cards → a WM bank of **5 top-tier operators** (transition-family-factorization, model-exploitability-objectization, event-triggered-re-anchoring, policy-ranking-ization, belief-ization-rewritten), ~8 middle/conditional actives, 3 meta/diagnostic protocols. Smaller and more killable, as required.

---

## B. World-model failure-signature map

Legend: **Dx** = minimum diagnostic to separate explanations. **Ops** = candidate operators (final names). **Lit** = whether 2023–26 WM literature already addresses it (✔ saturated / ~ partial / ✘ open).

| # | Symptom | Competing explanations (≥2) | Minimum diagnostic (Dx) | Metrics | Ops | Lit |
|---|---|---|---|---|---|---|
| 1 | Strong 1-step, poor long-horizon rollout | (a) compounding input-distribution shift; (b) missing slow/unresolved variables (closure error); (c) decoder-only degradation | k-anchored rollouts: re-anchor latent to posterior every k steps, sweep k; if error collapses for small k → (a); if a fixed-lag history readout beats the latent → (b) | error-vs-horizon curves per k; lag-regression R² | event-triggered-re-anchoring, memory-kernel-closure, multiscale-correction, transfer-operator | ~ (compounding error studied; k-anchor sweep rarely reported) |
| 2 | Strong teacher-forced, weak policy-induced rollout | (a) occupancy shift (policy leaves data support); (b) active exploitation (policy seeks model errors) | freeze policy: measure model error on-policy vs replay; then optimize actor against frozen model and re-measure | occupancy-weighted error; imagined-vs-real return gap G | model-exploitability-objectization | ~ (objective-mismatch line 2020–23; online G rarely instrumented) |
| 3 | Good visual quality, poor action-conditioned fidelity | (a) action pathway ignored; (b) action–visual confounding in data | counterfactual action divergence: same start state, different actions; compare model divergence vs simulator divergence | divergence-ratio curve vs horizon | counterfactual-action-fidelity probe (META) | ~ (video-WM critique emerging) |
| 4 | Accurate dynamics, poor planning | (a) reward/termination head error; (b) planner exploits small errors; (c) horizon mis-set | oracle component swap: plan with learned dynamics + oracle reward, and vice versa | Δreturn per swapped component | oracle-factorization (META), policy-ranking, exploitability | ~ |
| 5 | Accurate state, wrong reward/termination | (a) head capacity/loss weighting; (b) reward depends on info the bottleneck dropped | linear probe reward from frozen latent; if probe succeeds → head problem, else → representation problem | probe R²; oracle-reward Δreturn | oracle-factorization; IB (rate allocation) | ~ |
| 6 | Collapse under mass/friction/gravity/delay change | (a) no context capacity; (b) context inferable but encoder discards it; (c) planner can't consume context | oracle-context injection vs learned inference; frozen history→parameter probe | inference-gap = return(oracle-ctx) − return(learned); probe R² | transition-family-factorization | ~ (HiP-MDP/CaDM/CARL line; pixel-Dreamer inference gap open) |
| 7 | Strong average return, rare catastrophic failure | (a) rare transitions unmodeled; (b) risk-neutral planning objective | evaluate CVaR under simulator-seeded rare starts vs mean; check model error concentrated on rare transitions | CVaR-vs-mean gap; per-transition error tail | failure-boundary (barrier), coverage-set, particle-measure | ~ |
| 8 | Ensemble disagreement uncorrelated with error | (a) members share data/inductive bias (correlated errors); (b) disagreement measures parameter variance, not dynamics epistemics | disagreement-vs-error calibration on controlled OOD slice; compare to a retrieval/novelty baseline | AURC / calibration curve | coverage-set (recalibration); exploitability (occupancy-weighted eval) | ~ |
| 9 | Longer history gives diminishing returns | (a) task nearly Markov in latent; (b) recurrent state saturates/forgets; (c) aliasing needs structured memory, not length | fixed-lag probes: predict hidden vars from raw lag-k windows vs latent; kernel-truncation sweep | probe R² vs lag; error vs kernel length | memory-kernel-closure, belief-ization, program-store-factorization | ~ |
| 10 | Model-free outperforms planning with learned model | (a) planner exploits model errors; (b) planner/horizon mis-set; (c) critic already internalizes model info | run same planner with oracle dynamics: if planner+oracle wins → model at fault; else planner at fault | return: {planner+model, planner+oracle, model-free} | oracle-factorization, exploitability, policy-ranking | ~ |
| 11 | Planner raises model return, lowers real return | canonical exploitation; or reward-model over-optimism specifically | component-wise G: recompute imagined return with oracle reward on imagined states | G decomposition | model-exploitability-objectization | ~ (offline pessimism ✔; online G ✘) |
| 12 | Increasing rollout horizon abruptly damages performance | (a) compounding error crosses trust boundary; (b) value bootstrap mismatch at horizon | horizon sweep with per-state error accounting; swap bootstrap value with oracle returns | return vs H; per-state divergence step | (saturated: uncertainty-adaptive truncation — Neubay [paper], ELVIS [claimed]) | ✔ 2025–26 |
| 13 | Pixel reconstruction improves, control doesn't | decision-irrelevant bits dominate rate; or actor–model interface mismatch | probe task variables from latent; compare decoder-based vs decoder-free objective at fixed backbone | probe R²; return | IB family (saturated: TIA, Denoised MDP, DreamerPro, RePo, R2-Dreamer [paper]) | ✔ |
| 14 | Object identity drifts under occlusion/rearrangement | (a) binding failure; (b) memory failure | occlusion re-ID probe on frozen features: slot vs global latent | re-ID accuracy across occlusion length | object-slot-ization (conditional) | ~ (prediction ✔, control ✘) |
| 15 | Fails when object count changes | (a) global-latent capacity; (b) no exchangeable structure | count-extrapolation eval, train ≤k test >k | return / error vs count | object-slot-ization; program-store (registry) | ~ |
| 16 | Each task requires complete retraining | (a) interference; (b) missing task/context conditioning | multitask model + oracle task-context injection vs inferred | Δreturn per task | transition-family-factorization; skill-option | ~ (TD-MPC2 multitask [paper]) |
| 17 | Local predictions right, global progress wrong | (a) missing slow variables; (b) no subgoal/timescale structure | spectral analysis of latent transition (slow modes); jumpy k-step model comparison | spectral gap; k-step vs 1-step composed error | transfer-operator-ization, multiscale-correction, skill-option | ~ |
| 18 | Physical quantities drift despite low local error | no conserved structure in the update | invariant-drift metric (energy/momentum) vs horizon; structure-preserving vs plain integrator at equal step error | drift slope | conservation-structure (conditional) | ~ (HNN line ✔ in physics ML, ✘ in control WM) |
| 19 | Oracle context solves OOD; learned inference fails | (a) encoder discards identifying info; (b) insufficient excitation (needs probing actions) | history→context probe on frozen encoder; then dual-control test: does an information-seeking action policy close the gap? | probe R²; gap vs excitation | transition-family (inference half); belief-ization (info value) | ✘ (the sharpest open seam found) |
| 20 | Multimodal reliability weighting fails under corruption | (a) static fusion weights; (b) no redundancy exists to exploit | recoverability screen: leave-one-source-out + conditional imputer before any router training | recoverable-fraction matrix | recoverability-gated-fusion (conditional) | ✘ in WM (multimodal WM small) |

Retrieval discipline: signatures 2/10/11 → exploitability; 6/16/19 → transition-family; 1/9 → closure/re-anchoring; 12/13 → saturated, do not build there without a genuinely new differential.

---

## C. Existing-bank corrosion table (all 45 cards)

Statuses: `WM-NATIVE` / `WM-ADAPTABLE` / `WM-CONDITIONAL` / `META/EVALUATION` / `ARCHIVE` / `MERGE` / `KILL`. "Gen-test valid?" refers to the card's existing generation test read as a WM test.

| Card | WM status | Verdict & required rewrite | Gen-test valid for WM? | Duplication risk |
|---|---|---|---|---|
| **N1 recoverability-gated-fusion ★★** | **WM-CONDITIONAL** | VLA-native origin (own CAF-VLA anomaly). Survives in WM **only** when genuinely redundant sources exist: modalities, ensemble members, or **multi-horizon value estimates** (STEVE, Buckman et al. 2018, is the WM-native precedent of reliability-weighted fusion across horizons [paper]). Rewrite: recoverability screen over {k-step estimators / members / sensors} before any reliability router. In proprio-DMC there is no redundancy → operator inapplicable. | ✘ (VLA screen) → replacement: leave-one-evidence-out on value-expansion estimators | vs coverage-set (calibration) — distinct: routing vs guarantee |
| **N2 barrier-certificate-localization ★** | **WM-CONDITIONAL** | Merge with §14 failure-boundary-modeling into one safety-regime card. WM rewrite: learn/probe a recoverability boundary in latent space; oracle labels via simulator resets. | ✘ (logged-trajectory probe is fine but not WM-specific) → frozen-latent recoverability probe | vs coverage-set; vs Lyapunov/HJ-reachability lit |
| N3 dependency-bounded-assembly ★ | ARCHIVE | Spec-decode/dLLM native. Only speculative WM analog (parallel latent token commits in transformer WMs) has no probe today. | ✘ | — |
| **N4 two-part-code-ization ★★** | **META/EVALUATION** | Keep as a WM *evaluation* operator: prequential codelength of trajectories as model comparison at equal fit; residual-compressibility probe (gzip/LM-compress model errors) to detect complexity-purchased gains. Not an object shift for the WM itself. | ~ → WM eval test: does trajectory codelength rank checkpoints by closed-loop return better than 1-step loss? | vs N8 performance-law (different meta-object) |
| **N5 bits-back-refund-pricing ★** | **KILL (for WM)** | In WM the KL-refund **is the incumbent**: the RSSM ELBO already prices stochastic latents at KL(post‖prior) (PlaNet 2019 → DreamerV3 [paper]). Deletion test fails by construction: no unique WM prediction remains. Content already lives in every baseline. | ✘ | = incumbent |
| N6 program-store-factorization ★ | **WM-CONDITIONAL** (memory regime) | WM rewrite: parametric-compression vs indexed-retention of past states — external addressable store for a world model. Differential survives: capacity cliff exactly at training-episode length; test-time store extension with zero weight change. Regime: Memory Maze / DMLab-style memory tasks. | ~ → Memory Maze cliff probe (train ≤n corridor, test ≫n) | vs memory-kernel (opposite axis: compress vs retain) — keep both, axis is the dedup defense |
| N7 selection-output-ization ★ | ARCHIVE | Output-retyping to index-into-input has no current WM carrier with a probe (a "select next state from a registry/particle set" model is speculative). | ✘ | vs particle-measure |
| N8 performance-law-ization (meta) | META/EVALUATION | Applies to WM directly (return-vs-model-size/data laws; TD-MPC2 reports scaling curves [paper]). Use for two-GPU budget allocation, not as a card. | ~ | — |
| N9 simplicity-weighted-aggregation (meta) | ARCHIVE | Benchmark re-pricing is not the current WM bottleneck; no killable WM candidate. | ✘ | — |
| **1 memory-kernel-closure ★** | **WM-ADAPTABLE ⚠** | Real WM roots (Mori–Zwanzig; PSR). The required rewrite must answer the brief's §13 challenge: what does an explicit kernel predict that a bigger RSSM/GRU does not? Answer: (i) **lag-structured error** — a fixed-lag linear readout of raw history beats the recurrent latent exactly at the lags where the kernel is heavy; (ii) **observability-dependent kernel structure** — masking different state components (e.g., velocities vs positions in DMC-proprio) changes the fitted kernel in the direction MZ predicts (unresolved-variable timescales), which a generic recurrence does not predict [inferred]. Highest risk in the keep set of failing its generation test. | ~ (the dLLM test is invalid for WM) → replacement below (§D-middle) | vs S4/recurrence (relabel risk); vs program-store (opposite axis) |
| **2 observable-lifting ★** | **MERGE** → `transfer-operator-ization` | Koopman/EDMD and VAMP/MSM study the same transfer operator; the bank splits one spectral object into two cards (prediction-linearity readout vs slow-mode/timescale readout). Merge; keep both differentials as readouts of one card. | ~ (spec-decode test invalid) → EDMD on frozen RSSM latents: does one linear map match k-step nonlinear rollout, and does its spectrum predict drift growth? | with #4 (the merge) |
| **3 multiscale-correction-hierarchy ★** | **WM-ADAPTABLE** | WM rewrite: coarse k-step "jumpy" transition + fine 1-step corrector with explicit restriction/prolongation of *error*, predicting a **plateaued error-vs-horizon curve** (vs monotone compounding) and horizon-sublinear planning cost. Must be distinguished from ordinary hierarchical WMs (Director; Clockwork-VAE lineage [unverified detail]) by the scale-specific *error-correction* object. | ✘ (spec-decode) → frozen-latent jump-head probe (§D-middle) | vs skill-option (temporal abstraction of *actions*, not of *error*) |
| **4 collective-variable-ization** | **MERGE** → `transfer-operator-ization` | See #2. The VAMP/MSM face contributes the timescale/metastability differential and the exploration-revisit failure signature. | ✘ → merged probe | with #2 |
| 5 flux-conservation-ization ★ | WM-CONDITIONAL | Physical/resource-budget WMs only (contact force flux, conserved quantities on graphs). No probe on target benchmarks now. Low priority. | ✘ | vs conservation-structure |
| 6 factor-graph-ization ★ | ARCHIVE | For WM, factored transition + message passing collapses either into object-slot (entities) or causal sparsity (→ transition-family's invariant half). No independent WM differential with a cheap probe. | ✘ | high (object-slot; invariant) |
| 7 far-interaction-compression | ARCHIVE | In WM this becomes "compress distant history/objects" — an architecture/efficiency concern (Gate 10 adjacency) without a WM differential beyond program-store's. | ✘ | vs program-store |
| 8 conservation-structure-ization | WM-CONDITIONAL | Physical WM regime, state input. Differential intact: bounded invariant drift over long horizons vs secular drift at equal step error. Cheap on DMC pendulum/acrobot (state). Saturated for toy physics (HNN line 2019–23), thin for decision-making WMs [inferred]. | ~ → drift-vs-return test in a planner loop | vs flux-conservation |
| **9 ratio-ization ★** | **MERGE** → `policy-ranking-ization` | The WM face of "fit the ratio/ordering the consumer uses" *is* decision-order preservation: the planner consumes a ranking of plans, not calibrated returns. Merged into the promoted card. | ~ → rank-correlation probe (§D) | with value-equivalence lit (see dedup map) |
| 10 correction-field-ization | ARCHIVE | In WM, the score/denoising object is the **incumbent** of diffusion world models (DIAMOND, NeurIPS 2024 [paper]). No generative headroom as a card. | ✘ | = diffusion-WM incumbent |
| 11 path-straightening ★ | WM-CONDITIONAL (diffusion-WM regime) | Legit conditional rewrite: curvature of the denoising path predicts few-step imagination fidelity → cheap imagination for diffusion WMs. Compute-feasible at DIAMOND/Atari-100k scale. | ~ → curvature vs few-step planning-return correlation on a frozen diffusion WM | vs consistency-distillation lit (partial saturation [unverified]) |
| 12 transport-coupling-ization ★ | ARCHIVE | No WM-specific differential with a cheap probe; offline-WM distribution shift as OT is analysis, not an object shift. | ✘ | — |
| 13 particle-measure-ization | WM-CONDITIONAL | §13 challenge answered: particles must **enter inference or planning** (multimodal posterior → plan hedging / disambiguating actions), else it is ensemble-for-accuracy (PETS — saturated [paper]). Regime: partial observability with genuinely multimodal beliefs (aliased mazes). | ~ → bimodal-posterior toy: does a Gaussian RSSM fail where a particle belief plans a disambiguation detour? | vs belief-ization (particle = implementation of belief; keep only if the *measure* is load-bearing) |
| 14 set-ization | MERGE/ARCHIVE | WM content (exchangeable variable-count entities) lives in object-slot. | ✘ | object-slot |
| **15 graph-ization ★** | **KILL (for WM)** | Gate 10: carrier noun. The surviving WM differentials (count extrapolation, edge intervention, error localization) are exactly object-slot-ization's differentials plus relational factorization; a separate "graph" card is a module label. | ✘ | object-slot |
| 16 object-slot-ization ★ | WM-CONDITIONAL | Regime: multi-object pixel WMs. Saturated for video prediction (Slot Attention lineage), **not** for closed-loop control — the required rewrite adds a mandatory `closed_loop_readout` (return under occlusion/rearrangement/count shift), not just re-ID probes. | ~ → keep frozen-feature persistence probe, add closed-loop gate | vs set-ization (absorbed), graph-ization (killed) |
| 17 field-ization | ARCHIVE | Representation choice for robotics perception; not a WM object shift. | ✘ | — |
| 18 affordance-field-ization ★ | ARCHIVE (VLA-native) | Policy/perception object, not a WM object. Star earned on VLA fusion; no WM test. | ✘ | — |
| 19 correspondence-field-ization ★ | ARCHIVE (VLA-native) | Action-head object; same verdict. | ✘ | — |
| **20 operator-lifting ★** | **MERGE** → `transition-family-factorization` | The function-space half of the transition-family object: dynamics as an operator over a family, enabling zero-shot new parameters. Context inference (#33) is the other half. | ~ → absorbed | with #33/#23 |
| 21 sparse-support-ization ⚠ | WM-CONDITIONAL | State-input regime: SINDy-style sparse dynamics identification; differential = exact active-support recovery + residual sparsity. Low priority vs pixel-based targets. | ~ | vs residual-ization |
| **22 polarization-ization ★** | **KILL (for WM)** | No WM carrier: there is no recursive channel-combining transform over WM components that induces reliability bimodalization; every attempted mapping (ensemble members, rollout positions) is forced relabeling. Star is spec-decode-only. | ✘ | — |
| **23 invariant-ization ★** | **MERGE** → `transition-family-factorization` | Invariance (what is stable across environments) and context (what varies, low-dim, inferable) are the two halves of one factorization of a transition family. Keeping them separate double-counts one object. | ~ → absorbed (worst-context return becomes a readout) | with #33/#20 |
| 24 group-equivariance-ization | WM-CONDITIONAL | Equivariant dynamics models; physical/object regime; moderate saturation in equivariant RL [unverified]. Keep as conditional; probe = OOD-rotation rollout error. | ~ | vs conservation-structure |
| **25 belief-ization ★** | **WM-NATIVE — promote (rewritten)** | The most WM-native card in the bank (POMDP belief, filtering, RSSM posterior). Required rewrite: separate it from latent-variable-ization by making the differential **decision-theoretic**, not representational: (i) value of information — epistemic actions emerge; (ii) latent-reset recovery follows a posterior-contraction curve; (iii) masking belief *uncertainty* (keeping the mean) destroys return only on aliased tasks. Full card in §D. | ~ (spec-decode test invalid) → replaced | vs latent-variable-ization (the substrate), particle-measure (an implementation) |
| **26 distribution-output-ization** | **KILL (for WM)** | Gate 10 ("add uncertainty") + Gate 6 (PETS 2018, distributional RL — fully absorbed). Every decision-relevant remnant lives in belief (info value), coverage-set (guarantee), exploitability (pessimism). First card to demote. | ✘ | belief / coverage-set / exploitability |
| 27 coverage-set-ization | WM-CONDITIONAL | Safe/robust planning regime: conformal sets over dynamics/reward predictions constraining the planner. Trivial cheap probe (split-conformal wrapper on a frozen model — no training). Active 2023–25 area (conformal decision/safe MPC [unverified]), so demand a WM-specific differential: set size vs planning-regret correlation. | ~ | vs barrier (guarantee vs boundary object) |
| 28 latent-variable-ization | ARCHIVE (saturated substrate) | WM-native and foundational — and therefore generatively dead: every baseline is already this operator. Keep as dedup anchor only. | ✘ | anchor |
| 29 information-bottleneck-ization | ARCHIVE (saturated) | WM-native, heavily mined 2021–26: TIA, Denoised MDP, DreamerPro, RePo, and now R2-Dreamer's redundancy-reduction objective (ICLR 2026 [paper]) are all points on this family. New work requires a genuinely different differential (decision-utility rate allocation across WM components), else it's the incumbent. | ✘ as-is | = incumbent family |
| **32 residual-ization ★** | WM-CONDITIONAL | Requires a semantically meaningful base model (physics prior, nominal simulator, frozen pretrained WM). Differential intact: residual sparsity localized at contacts/shift regions; fast re-adaptation by re-fitting only the residual. Not applicable to from-scratch pixel WMs. | ~ → sim+residual probe on state-based tasks | vs N4 two-part-code (meta vs object), vs test-time adaptation lit |
| **33 context-ization** | **WM-NATIVE — promote as `transition-family-factorization`** | The strongest WM card. Rewrite absorbs #20 + #23: object = family {T_c} = invariant mechanism × low-dim online-inferable context with a posterior. Full card in §D. Roots: HiP-MDP (Doshi-Velez & Konidaris), CaDM (Lee et al. 2020), PEARL, RMA, VariBAD [papers]. | ~ → replaced with CARL-DMC probe | vs meta-RL (policy adaptation vs dynamics factorization) |
| 34 skill-option-ization | WM-NATIVE (middle tier) | Hierarchical WM lineage (Director, SkiMo [papers]); keep. Absorbs chunk-ization's only WM-valid content (temporally extended prediction units — valid only when units are learned/searchable, not fixed-length blocks). | ~ → jumpy skill-space rollout error per wall-clock | vs multiscale-correction (error vs action abstraction) |
| **35 chunk-ization ★** | **KILL (for WM)** | The most VLA-biased card (ACT lineage). Its differentials (jitter, per-step verification cost, block commitment) are imitation/serving concerns; the WM-translatable remnant (multi-step prediction units) is fully covered by #34 and #3. | ✘ | #34/#3 |
| 36 sufficient-summary-functionalization ⚠ | META/EVALUATION | The collapse test (fix the summary, is the property fixed?) is a first-rate WM diagnostic: is return a function of the candidate context/CV/belief statistic? Keep as protocol inside oracle-factorization; not an object card. | ~ | — |
| 37 implicit-topology-ization | ARCHIVE | Contact-boundary SDF inside latent WMs is speculative; no probe. | ✘ | vs barrier |
| 38 executable-spec-ization | ARCHIVE | Reward-program synthesis is agent-side, not a WM object shift. | ✘ | — |

---

## D. Promoted WM operator cards

### D.1 `transition-family-factorization` (rewritten context-ization; absorbs invariant-ization, operator-lifting) — TOP TIER

```text
operator_name: transition-family-factorization
status: WM-NATIVE (promoted)
one_sentence_core_move: replace one pooled transition model with a factored family {T_c}: an invariant mechanism backbone × a low-dimensional latent context c that is online-inferable from short interaction history, with adaptation = posterior inference rather than retraining.
old_object_pattern: a single transition function trained on pooled multi-environment data; variation absorbed into weights or treated as noise.
new_object_pattern: invariant backbone + context variable with a posterior p(c | history); optionally an operator-valued map c ↦ T_c (function-space half, ex operator-lifting).
world_model_component: transition model + environment-context estimator + posterior state estimator.
world_model_regime: multi-task/multi-env; state or pixel; online or offline; planning- or actor-based; hidden dynamics parameters.
mathematical_frame: hidden-parameter MDP; hierarchical Bayes; system identification; neural operator (function family).
core_simplification: environment variation is localized in a few inferable dimensions instead of spread through all weights; OOD adaptation becomes filtering, not fine-tuning.
differential_prediction: (i) a frozen history→c probe predicts held-out physical parameters (mass/friction/gravity/delay) above a state-only baseline; (ii) return degrades smoothly with context-posterior error and oracle-context injection recovers most of the OOD gap (the "inference gap" is measurable and non-zero); (iii) information-seeking (probing) actions early in an episode increase context information and later return — a pooled model predicts none of these. [failure sig 6/16/19]
cheap_probe: CARL-DMC walker/pendulum (or hand-modified DMC XMLs) with mass/friction sweeps; linear probe on the frozen recurrent state of a trained DreamerV3/R2-Dreamer agent regressing the true parameters; oracle-context-injected variant for the gap. 1 GPU, <1 day, no retraining for the probe.
oracle_or_intervention_probe: oracle context injection; controlled parameter shift; latent reset (does context re-inference recover faster than state re-inference?).
failure_signature: collapse under changed dynamics parameters; per-task retraining; oracle context works but learned inference fails (sig 19).
closed_loop_readout: normalized return on held-out contexts, zero-shot and few-episode.
horizon_readout: rollout error vs horizon stratified by context distance from training range.
ood_readout: return vs parameter distance; interpolation vs extrapolation split.
decision_utility_readout: inference gap = return(oracle c) − return(inferred c).
model_exploitability_readout: imagined-vs-real return gap per context bucket.
positive_evidence: HiP-MDP [paper]; CaDM (Lee et al. 2020) [paper]; PEARL, VariBAD, RMA [papers]; CARL benchmark results showing context-conditioning matters [paper, details unverified this pass].
negative_evidence: context inference degrades under pixel input and weak excitation [inferred from sig-19 pattern; to be established by the probe itself].
kill_criterion: kill if oracle-context injection improves normalized return by <2% across ≥3 CARL-DMC tasks, or if the frozen history→c probe fails to beat the state-only baseline by R² margin ≥0.1 on held-out parameters.
positive_examples: mass/friction/gravity/delay shifts; embodiment variation.
negative_examples: one-hot task-ID conditioning (not online-inferable); domain randomization without an explicit context object.
closest_existing_operator: latent-variable-ization (substrate); meta-RL fast adaptation.
dedup_defense: vs meta-RL: the object is a factored *dynamics family* with an identifiable c, not fast policy adaptation; vs invariant-ization: same factorization, invariance is the backbone half (worst-context return is a readout here, not a separate card); vs operator-lifting: c ↦ T_c is this card's function-space half.
source_papers: Doshi-Velez & Konidaris (HiP-MDP); Lee et al. 2020 (CaDM); Rakelly et al. 2019 (PEARL); Zintgraf et al. (VariBAD); Kumar et al. (RMA); Benjamins et al. (CARL).
official_repositories: automl/CARL [unverified path]; NM512/r2dreamer [repo]; nicklashansen/tdmpc2 [repo].
compute_profile: probe: 1 GPU-day on existing checkpoints; minimal method run: 2 GPUs × ~1 week (3 tasks × 2 seeds each side).
AAAI_fit: strong (compact mechanism: context head + injection ablation + inference-gap analysis).
Information_Sciences_fit: strong (systematic multi-context study, identifiability/calibration analysis, extensive ablation).
Information_Fusion_fit: weak-plausible (fusing history evidence across timescales only if reliability is explicitly modeled).
generation_test: PASSED — candidate: "Closing the context-inference gap in pixel world models": measure the gap on CARL-DMC with R2-Dreamer; add an excitation-aware context posterior (auxiliary identifiability loss + optional probing bonus); kill per criterion above; route AAAI (compact) or Information Sciences (systematic).
```

### D.2 `model-exploitability-objectization` (new; merges §14 model-exploitability + occupancy-aware model learning) — TOP TIER

```text
operator_name: model-exploitability-objectization
status: WM-ADAPTABLE (promoted; new card)
one_sentence_core_move: replace average model accuracy with a policy-conditioned error object — the discrepancy weighted by (or maximized over) the occupancy of the policy that is being optimized against the model — and treat its growth, not the loss curve, as the model-quality signal.
old_object_pattern: uniform/replay-weighted prediction loss as the measure of model quality.
new_object_pattern: exploitability functional G(π, M) = J_M(π) − J_env(π) and occupancy-weighted discrepancy d_ρπ(M); two regimes: current-policy weighting (occupancy-aware) and optimized/adversarial-policy weighting (exploitability frontier).
world_model_component: uncertainty model + imagination procedure + evaluation protocol; secondarily the training loss weighting.
world_model_regime: online actor-based (Dreamer) and planning-based (TD-MPC2); offline (where it reduces to the pessimism literature — see dedup).
mathematical_frame: occupancy measures; adversarial risk; distribution shift under optimization (Goodhart).
core_simplification: model error stops being a global scalar; only error the optimizer can find and occupy matters — everything else is provably irrelevant to closed-loop return at fixed policy class.
differential_prediction: (i) G grows during actor optimization while average validation loss is flat (dissociation); (ii) G predicts imminent real-return collapse earlier than loss does; (iii) interventions that cap G (occupancy-weighted retraining, imagination truncation in high-G regions, pessimism only where G concentrates) improve real return with unchanged average loss. The incumbent (loss-centric) formulation predicts none of these dissociations. [failure sigs 2/10/11]
cheap_probe: instrument imagined return (already computed in Dreamer-style training [repo: r2dreamer dreamer.py `_imagine`/`_lambda_return`]) vs periodic real eval return across saved checkpoints; plot G(t) against loss(t); zero retraining, ~hours on logged runs.
oracle_or_intervention_probe: oracle dynamics swap inside imagination (simulator rollout for the same imagined actions) to decompose G into dynamics vs reward vs value components.
failure_signature: teacher-forced good / policy-rollout bad; planner beats model return but loses real return; model-free outperforms planning.
closed_loop_readout: real return vs G trajectory; return after G-capping intervention.
horizon_readout: G vs imagination horizon (where does exploitation concentrate?).
ood_readout: G under context shift (combines with D.1).
decision_utility_readout: G is itself the decision-utility gap.
model_exploitability_readout: primary object.
positive_evidence: model exploitation documented since Dyna-era; MBPO analysis of compounding error [paper]; objective-mismatch line (Lambert et al. 2020) [paper]; offline pessimism (MOPO/MOReL) works by bounding a G-like quantity [papers].
negative_evidence: on some benchmarks G≈0 throughout (well-covered data) — then the operator is inert there.
kill_criterion: kill if across ≥3 standard tasks |corr(G, subsequent real-return change)| < 0.2 while loss shows the same information (partial correlation of G with return controlling for loss < 0.1), or if G ≈ 0 everywhere (no exploitation exists to model).
positive_examples: DMC quadruped/hopper online Dreamer runs; TD-MPC2 with aggressive planner settings.
negative_examples: pessimism penalty as a tuned knob with no measured G (that is the killed reg-knob pattern).
closest_existing_operator: distribution-output-ization (killed), coverage-set (guarantee, not policy-conditioned), ratio-ization.
dedup_defense: vs MOPO/MOReL: those are offline penalty *methods*; this is an online, measured *object* whose trajectory is the signal, and the offline penalty is one intervention among several; vs objective-mismatch/VaGram: those re-weight training loss by value gradients; this conditions on the optimizing policy's occupancy and includes the adversarial regime; vs Plan2Explore: exploration bonus ≠ exploitability accounting.
source_papers: Janner et al. 2019 (MBPO); Lambert et al. 2020 (objective mismatch); Yu et al. 2020 (MOPO); Kidambi et al. 2020 (MOReL); Voelcker et al. (VaGram) [papers; exact venues unverified this pass].
official_repositories: NM512/r2dreamer [repo]; nicklashansen/tdmpc2 [repo].
compute_profile: probe free on logged runs; intervention study 2 GPUs × 1–2 weeks.
AAAI_fit: strong (G-monitor + one capping mechanism + decisive closed-loop delta).
Information_Sciences_fit: strong (uncertainty/analysis framing, multi-env study).
Information_Fusion_fit: scope mismatch.
generation_test: PASSED — candidate: "Exploitability-gated imagination": monitor G online; truncate/penalize imagination only in state regions contributing to G growth; differential: real return improves at unchanged average loss; kill per criterion.
```

### D.3 `event-triggered-re-anchoring` (new; from event-triggered control + filtering innovation tests) — TOP TIER

```text
operator_name: event-triggered-re-anchoring
status: WM-ADAPTABLE (promoted; new card; native to control theory)
one_sentence_core_move: replace fixed-cadence replanning/state-refresh with an innovation-gated trigger — recompute the plan (or re-anchor the latent to the posterior) only when the observed innovation (prior-vs-posterior divergence) exceeds a bound, otherwise reuse the committed plan.
old_object_pattern: replan every step (TD-MPC2 default MPPI [repo: tdmpc2.py `_plan` called per act]) or fixed action-repeat; imagination anchored on a fixed schedule.
new_object_pattern: a model-trust monitor: innovation signal ν_t = D(prior_t ‖ posterior_t) (KL already computed by the RSSM [repo: r2dreamer rssm.py `obs_step`/`kl_loss`]) + a threshold policy over {reuse plan, replan, re-anchor}.
world_model_component: planner/MPC module + posterior state estimator + rollout horizon controller.
world_model_regime: planning-based (TD-MPC2, Dreamer-MPC variants); online; state or pixel; also applicable to actor-based agents as re-anchoring of imagination starts.
mathematical_frame: event-triggered control; filtering innovation/whiteness tests; computation-return Pareto.
core_simplification: planning compute stops being a fixed cost per step; it is spent only where the model is surprised — the expensive object shrinks from "plan always" to "detect when the committed plan's premises broke."
differential_prediction: (i) the return-vs-compute Pareto of the triggered policy dominates every fixed-cadence baseline (replan-every-k for all k) on at least some tasks; (ii) trigger events are temporally structured — concentrated at contacts, perturbations, and stochastic branchings — not uniform (a schedule-knob reading predicts no structure); (iii) the innovation threshold traces a smooth compute-return frontier. [failure sigs 1/12-adjacent, compute-efficiency axis]
cheap_probe: frozen TD-MPC2 checkpoint; wrap `act()` with plan-caching + trigger on latent-consistency error (predicted next z vs encoded observed z); sweep threshold; measure return + planner-call count. 1 GPU, hours, zero retraining.
oracle_or_intervention_probe: oracle trigger (trigger on true simulator-state deviation) establishes headroom; latent reset tests re-anchoring value directly.
failure_signature: planning compute dominates wall-clock at equal return; performance insensitive to replanning frequency in calm regions but sensitive at rare events.
closed_loop_readout: return at matched (and reduced) planner-call budgets.
horizon_readout: committed-plan age distribution; error growth during reuse windows.
ood_readout: trigger-rate shift under perturbed dynamics (should rise — a free drift detector).
decision_utility_readout: Δreturn vs Δcompute against fixed-cadence frontier.
model_exploitability_readout: reused plans are open-loop — G during reuse windows must be monitored (connects to D.2).
positive_evidence: event-triggered MPC with guarantees is established in control, incl. learned GP dynamics (learning-based event-triggered MPC, arXiv 2110.12214) [paper]; event-triggered replanning reduces compute in robotic MPC [papers].
negative_evidence: none found for latent-WM planners; AdaJEPA (arXiv 2606.32026) explicitly lists event-triggered adaptation/replanning as *future work* [claimed] — evidence the transfer is open as of 2026-06, and a saturation risk to re-check at submission time.
kill_criterion: kill if no threshold achieves ≥40% planner-call reduction at ≤2% return loss across 3 DMC/Meta-World tasks, or if trigger events are temporally uniform (no structure — then it is action-repeat relabeled).
positive_examples: contact-rich Meta-World tasks; perturbed DMC.
negative_examples: fixed action-repeat; periodic replanning with a tuned period (the incumbent, not the operator).
closest_existing_operator: chunk-ization (killed — fixed blocks, no trigger object); belief-ization (supplies the innovation signal but not the trigger policy).
dedup_defense: vs filtering: Dreamer already filters every step — the new object is the *trigger + plan-reuse policy*, not the filter; vs action repeat: state-dependent, not fixed; vs eMPC: the transfer target (learned latent WMs, innovation measured in learned latent space) and the Pareto/structure differentials are new.
source_papers: Heemels et al. (event-triggered control survey); arXiv 2110.12214 (GP event-triggered MPC); AdaJEPA arXiv 2606.32026 (adjacent, future-work mention).
official_repositories: nicklashansen/tdmpc2 [repo: tdmpc2/tdmpc2.py `act`, `_plan`; config.yaml `mpc: true, horizon: 3, iterations: 6`]; NM512/r2dreamer [repo: dreamer.py `act(obs, state, eval)`; rssm.py `obs_step`].
compute_profile: probe: 1 GPU, <1 day on pretrained checkpoints; paper-scale: 2 GPUs × 1–2 weeks.
AAAI_fit: strong (one mechanism, decisive Pareto plot, oracle-trigger headroom, tiny overhead) — the bank's best low-compute AAAI route.
Information_Sciences_fit: plausible (adaptive computation analysis across envs).
Information_Fusion_fit: scope mismatch.
generation_test: PASSED — candidate: "Plan less, re-anchor on surprise": eval-time trigger wrapper on TD-MPC2 + R2-Dreamer-MPC; differentials (i)–(iii); kill per criterion; expansion: train-time triggered imagination anchoring.
```

### D.4 `policy-ranking-ization` (new; absorbs ratio-ization's WM face) — TOP TIER

```text
operator_name: policy-ranking-ization
status: WM-ADAPTABLE (promoted; highest renaming risk — see dedup)
one_sentence_core_move: make the modeled object the ORDERING the decision procedure induces over candidate actions/plans/policies, not the fidelity of state/reward prediction — train and evaluate the world model on rank agreement with environment returns.
old_object_pattern: transition/reward models trained on MSE/likelihood, consumed by a planner that only ever uses the induced ranking of candidates.
new_object_pattern: an ordinal object: the rank statistic (e.g., Kendall-τ) between model-evaluated and environment-evaluated candidate plan returns, as both a diagnostic and a trainable target.
world_model_component: transition + reward + value models jointly, via the planner interface; evaluation protocol.
world_model_regime: planning-based (MPPI/CEM: TD-MPC2) primarily; discrete-action tree planners (MuZero-style) secondarily.
mathematical_frame: ordinal statistics; decision-focused (predict-then-optimize) learning; value equivalence.
core_simplification: the model may be arbitrarily wrong in every metric the planner does not consume; only order preservation over the planner's candidate distribution is paid for.
differential_prediction: (i) checkpoints with equal 1-step loss differ widely in plan-rank τ, and τ predicts closed-loop return where loss does not (dissociation); (ii) training with a ranking loss on candidate sets improves return without improving (possibly worsening) prediction loss; (iii) rank degradation with horizon is a sharper early-warning than error growth. [failure sigs 4/10/13]
cheap_probe: frozen TD-MPC2 checkpoint: sample N=64 plans from the planner's own distribution [repo: `_plan` elites], score each by model (`_estimate_value`) and by simulator rollout, compute τ; repeat across checkpoints/tasks; correlate τ vs actual return. 1 GPU, <1 day, no retraining.
oracle_or_intervention_probe: oracle reward with learned dynamics (and vice versa) localizes which component breaks the ordering; counterfactual action queries are the unit test.
failure_signature: accurate dynamics but poor planning; pixel loss improves, control does not.
closed_loop_readout: return of planner using rank-trained vs likelihood-trained model at equal capacity.
horizon_readout: τ vs candidate-plan horizon.
ood_readout: τ under context shift (does ordering survive where accuracy does not? — ratio-ization's stable-ordering claim, now with a WM readout).
decision_utility_readout: τ→return regression is the object.
model_exploitability_readout: rank training can increase exploitability (model tuned to please the planner) — must be co-monitored with D.2's G.
positive_evidence: value equivalence principle (Grimm et al. 2020/2021) [papers]; MuZero's value-equivalent latent [paper]; decision-aware MBRL / IterVAML line [papers, details unverified this pass].
negative_evidence: value-equivalence theory shows cardinal Bellman-equivalence suffices — if τ and Bellman error are empirically collinear, this card is a relabel (that is the kill test).
kill_criterion: kill if across checkpoints/tasks the partial correlation of τ with closed-loop return, controlling for 1-step loss AND Bellman error, is <0.1 — then ordinal adds nothing over value equivalence.
positive_examples: TD-MPC2 checkpoints mid-training; models under distractor shift.
negative_examples: "decision-aware" as a loss-reweighting knob with no measured ordering.
closest_existing_operator: ratio-ization (absorbed); value-equivalence (the incumbent theory to beat).
dedup_defense: value equivalence is CARDINAL (Bellman-operator agreement); this is ORDINAL over the planner's actual candidate distribution, measurable planner-in-the-loop on frozen models — the differential is the dissociation test itself, pre-registered.
source_papers: Grimm et al., The Value Equivalence Principle (NeurIPS 2020) and follow-up; Schrittwieser et al. (MuZero); Farahmand (IterVAML); D'Oro et al. / Nikishin et al. (decision-aware) [papers; exact list to finalize at writing time].
official_repositories: nicklashansen/tdmpc2 [repo].
compute_profile: probe 1 GPU-day; rank-training study 2 GPUs × 2 weeks.
AAAI_fit: plausible (needs the training-side win, not just the diagnostic).
Information_Sciences_fit: strong (evaluation/analysis + method, multi-env).
Information_Fusion_fit: scope mismatch.
generation_test: PASSED — candidate: "Rank-faithful world models": τ-diagnostic study + listwise rank fine-tuning of the TD-MPC2 model on planner candidates; kill per criterion.
```

### D.5 `belief-ization` (rewritten) — TOP TIER

```text
operator_name: belief-ization (WM rewrite)
status: WM-NATIVE (promoted; the most natively-aligned card in the bank)
one_sentence_core_move: replace a point latent with a posterior over hidden state whose UNCERTAINTY is load-bearing for decisions — information gathering, hedging, and recovery — not merely a training-time regularizer.
old_object_pattern: deterministic latent, or a stochastic latent whose distribution never changes a decision (the saturated RSSM default).
new_object_pattern: a belief b_t = p(s_t | history) with decision-relevant functionals: entropy, value of information, posterior-contraction rate.
world_model_component: posterior state estimator + stochastic latent + planner/actor interface.
world_model_regime: partial observability (Memory Maze, MiniGrid aliased tasks, occluded manipulation); online.
mathematical_frame: POMDP / Bayesian filtering; value of information.
core_simplification: hidden-state ambiguity gets one dedicated object (the belief) instead of leaking into every prediction as unexplained variance.
differential_prediction: (i) epistemic actions emerge — the agent sacrifices immediate reward to reduce belief entropy, and the sacrifice is predicted by value-of-information; (ii) after a forced latent reset, return recovery follows the posterior-contraction curve (observability-dependent), which a point-latent model cannot predict; (iii) ablating belief uncertainty (feeding the mean, zeroing variance) destroys return ONLY on aliased tasks and is harmless on fully observed ones — a clean 2×2. [failure sigs 9/19]
cheap_probe: frozen R2-Dreamer/DreamerV3 checkpoint on Memory Maze [repo: envs/memorymaze.py]: (a) latent-reset recovery curves; (b) entropy-vs-return-event correlation; (c) mean-only ablation at eval. 1 GPU, ~1 day, no retraining.
oracle_or_intervention_probe: oracle state substitution (upper bound); latent reset; controlled observation corruption (posterior should widen — a falsifiable calibration claim).
failure_signature: history length gives diminishing returns; failures trace to hidden state, not capacity.
closed_loop_readout: return on aliased vs non-aliased task pairs under the 2×2 ablation.
horizon_readout: imagination quality vs belief entropy at anchor.
ood_readout: posterior widening under corruption (calibration under shift).
decision_utility_readout: value-of-information estimate vs realized epistemic-action frequency.
model_exploitability_readout: overconfident beliefs are an exploitation surface — co-monitor G.
positive_evidence: POMDP theory; Dreamer's posterior/prior machinery [papers]; Memory Maze results showing memory is the bottleneck [paper, details unverified].
negative_evidence: on standard DMC, RSSM stochasticity often behaves as regularization only [inferred] — which is exactly what the 2×2 ablation tests.
kill_criterion: kill if mean-only ablation changes return by <2% on ≥2 aliased tasks (uncertainty not load-bearing), or if reset-recovery curves are indistinguishable across observability conditions.
positive_examples: Memory Maze; heaven-hell / T-maze style tasks.
negative_examples: calling any RNN state a belief; ensembles-for-accuracy (see particle-measure).
closest_existing_operator: latent-variable-ization (substrate — the dedup line is "distribution exists" vs "distribution decides").
dedup_defense: vs latent-variable-ization: differential is decision-theoretic (i)–(iii), none of which follow from having a posterior; vs particle-measure: implementation choice inside this card, promoted separately only if multimodality is load-bearing.
source_papers: Kaelbling et al. (POMDP); Hafner et al. (PlaNet/Dreamer); Pasukonis et al. (Memory Maze) [unverified citation detail].
official_repositories: NM512/r2dreamer [repo: rssm.py obs_step posterior; memorymaze env extra].
compute_profile: probe 1 GPU-day; method work 2 GPUs × 2 weeks.
AAAI_fit: plausible.
Information_Sciences_fit: strong (uncertainty + partial observability analysis).
Information_Fusion_fit: weak (belief updating as evidence fusion is stretchable — do not stretch).
generation_test: PASSED — candidate: "Is the RSSM latent a belief? A 2×2 dissociation and what it takes to make uncertainty load-bearing" (diagnostic + one mechanism: entropy-aware planning bonus).
```

### D.6 Middle-tier cards (compact — full schema deferred until their missing probe is run)

**`transfer-operator-ization`** (merged #2 + #4; WM-ADAPTABLE). Object: the spectral transfer operator of the latent dynamics; readouts: (a) one linear map in a lifted space matches k-step nonlinear rollout (Koopman face); (b) spectral gap/slow modes predict task timescales and metastable revisits (VAMP face). Cheap probe: EDMD fit on frozen RSSM latent trajectories; compare k-step reconstruction vs the model's own rollout; check whether eigenvalue error predicts drift shape. Kill if linear-lift ≈ nonlinear at no horizon or spectrum is uninformative of drift. Missing piece before promotion: evidence the lift helps *planning*, not just analysis. Saturation: Koopman-RL exists 2020–24 [unverified]; the frozen-latent-diagnostic angle appears open [inferred].

**`multiscale-correction-hierarchy`** (WM-ADAPTABLE). WM rewrite: coarse k-step jump predictor + fine 1-step corrector with explicit error restriction/prolongation. Differential: plateaued error-vs-horizon; planning cost sublinear in horizon. Cheap probe: train a small k-jump head on frozen latents (no WM retraining); compose jumps vs step-wise rollout; measure drift. Kill if composed-jump error ≥ step-wise everywhere. Dedup: Director/hierarchy = action abstraction; this is *error* abstraction.

**`memory-kernel-closure`** (WM-ADAPTABLE ⚠). WM probe: on DMC-proprio with masked velocities, fit (a) recurrent latent, (b) fixed-lag linear readouts of raw history, (c) latent + low-rank kernel head over lagged embeddings; differential: kernel weight concentrates at lags matching the masked variables' timescales, and changing the mask moves the kernel as MZ predicts. Kill if kernel weight ≈ 0 or mask-invariant. Flagged the most likely of the keeps to fail (a well-sized RSSM may leave no lag-structured residue).

**`skill-option-ization`** (WM-NATIVE, middle). Keep with the SkiMo/Director-style differential: skill-space rollouts give lower long-horizon error per wall-clock and per model call; boundaries align with re-plan triggers (synergy with D.3). Saturation moderate — require the wall-clock-normalized readout, which the literature under-reports [inferred].

**`program-store-factorization`** (WM-CONDITIONAL, memory regime). Probe: Memory Maze corridor-length cliff (train ≤n, test ≫n) for parametric-memory WMs; then test-time store extension. Distinct axis from memory-kernel (retain-and-address vs compress).

**META protocols kept:** `oracle-factorization-of-WM-errors` (see §E.1), `two-part-code-ization` (prequential-codelength model comparison + residual-compressibility audit of claimed gains), `counterfactual-action-fidelity` probe (sig 3), `sufficient-summary collapse test` (inside oracle-factorization).

### D.7 Conditional-tier register (regime-locked; promote only when the regime is the actual target)

object-slot-ization (multi-object pixels; closed-loop gate mandatory) · particle-measure-ization (multimodal beliefs entering planning) · coverage-set-ization (safety/abstention; probe is free) · barrier/failure-boundary (safety; frozen-latent recoverability probe) · residual-ization (semantic base model available) · conservation-structure-ization (physical, state input) · recoverability-gated-fusion (genuine redundant sources; STEVE-lineage rewrite) · path-straightening (diffusion-WM, DIAMOND-scale) · group-equivariance (symmetry-rich dynamics) · sparse-support/SINDy (state input, interpretability) · flux-conservation (resource/physical budget) · program-store (memory tasks).

---

## E. Newly discovered candidates — disposition

**Promoted (3 + 1 meta):** model-exploitability-objectization (D.2) · event-triggered-re-anchoring (D.3) · policy-ranking-ization (D.4) · oracle-factorization-of-WM-errors (META — E.1).

**E.1 `oracle-factorization-of-WM-errors` (META/EVALUATION, promoted as protocol).** Decompose closed-loop failure by component substitution at evaluation: {oracle state (posterior←simulator state), oracle context, oracle transition (simulator step inside imagination), oracle reward, oracle termination, oracle value}. Deliverable: a per-task bottleneck profile. This is §14's oracle-factorization + error-budget-allocation merged — the budget is only meaningful once oracle swaps ground it; as bookkeeping alone it was correctly suspected of vacuity. It is a protocol, not an object shift: it changes what experiments are run, not what the model represents. Retain as the bank's standard first move on any new WM failure.

**Recorded as saturated (1):** horizon-adaptive modeling ("trust-horizon"). The object shift is real, and 2025–26 literature has claimed it: Neubay makes quantile-thresholded uncertainty truncation the decisive component for long-horizon offline MBRL [paper, arXiv 2512.04341]; ELVIS does uncertainty-triggered soft truncation in visual latent MPC [claimed, arXiv 2605.04709]; earlier MBPO/M2AC/adaptive-rollout work covers the training-rollout side [papers]. Verdict: incumbent formulation + new anti-pattern entry (§G). Any future card here needs a differential neither paper makes (none identified this pass).

**Archived (2):** counterfactual-action-fidelity as an *operator* (kept as META probe; as an object it belongs to video-WM regimes outside the compute envelope) · rare-event-reweighted imagination (importance-weighted imagination toward catastrophic transitions; real gap for sig 7, but no cheap probe designed that avoids simulator-privileged resets — revisit).

**Merged (3):** occupancy-aware model learning → D.2 (current-policy regime) · failure-boundary modeling → N2 barrier card · error-budget-allocation → E.1.

**Killed (1):** "counterfactual-action fidelity as training loss for video WMs at benchmark scale" — fails Gate 8 (compute) in every variant considered.

**Unresolved (2):** dual-control-ization (identification-aware probing actions) — currently expressed as differential (iii) of D.1 and (i) of D.5; if the CARL probe shows a large excitation-limited inference gap, split it into its own card · transition-family via neural operators at function-space level (zero-shot c interpolation) — awaits D.1's probe outcome.

---

## F. Deduplication map

| Cluster | Members | Resolution |
|---|---|---|
| Spectral/transfer operator | observable-lifting, collective-variable-ization | MERGE → transfer-operator-ization (one operator, two readouts) |
| Transition family | context-ization, invariant-ization, operator-lifting, (meta-RL lit) | MERGE → transition-family-factorization; invariance = backbone half, operator = function-space half |
| Decision-order | ratio-ization, policy-ranking, value-equivalence (lit), decision-aware MBRL (lit) | policy-ranking-ization absorbs ratio's WM face; MUST beat value-equivalence in the pre-registered dissociation or die |
| Policy-conditioned error | model-exploitability, occupancy-aware learning, MOPO/MOReL pessimism (lit) | one card (D.2), two regimes; offline pessimism = one intervention |
| Uncertainty outputs | distribution-output (killed), belief, coverage-set, particle-measure | belief = decision-relevant posterior; coverage-set = guarantee; particle = implementation; distribution-output had no remainder |
| Memory | memory-kernel (compress w/ lag structure), program-store (retain & address), belief (sufficiency), far-interaction (archived) | orthogonal axes kept; far-interaction folded out |
| Temporal abstraction | skill-option, chunk-ization (killed), multiscale-correction | skills = learned action units; multiscale = error hierarchy; chunk had no WM remainder |
| Safety | barrier-certificate, failure-boundary (§14), coverage-set, implicit-topology (archived) | barrier+boundary merged; coverage-set separate (statistical vs dynamical object) |
| Objects/relations | graph-ization (killed), set-ization (folded), object-slot, factor-graph (archived) | object-slot is the sole carrier |
| Trigger/schedule | event-triggered-re-anchoring, action-repeat (incumbent), trust-horizon (saturated) | re-anchoring = when to LOOK/replan; horizon = how far to IMAGINE (saturated); keep only the former |

---

## G. Anti-pattern additions (WM-specific pseudo-operators)

From the brief, confirmed: just-increase-imagination-horizon · add-a-reconstruction-decoder · add-an-uncertainty-head · use-a-larger-latent · use-Transformer-dynamics · train-on-more-environments · add-object-slots-without-persistence-and-closed-loop-tests · physics-informed-loss-without-invariant-prediction · multi-timescale-features-without-scale-specific-error-correction.

Newly added by this audit:
1. **adaptive-horizon-as-novelty** — post-Neubay/ELVIS, uncertainty-truncated rollouts are the incumbent; claiming them without a new differential is a knob (2026 update to the schedule-knob rule).
2. **KL-refund-relabeling** — describing the RSSM ELBO in bits-back vocabulary and claiming an operator (killed N5's WM face).
3. **ensemble-equals-belief** — ensembles-for-accuracy presented as belief modeling without any decision-side functional (kills the lazy reading of #13/#25).
4. **context-as-task-ID** — one-hot or given-at-test conditioning presented as context inference (violates D.1's online-inferability requirement).
5. **representation-objective-swap-without-decision-differential** — replacing reconstruction with contrastive/redundancy-reduction/next-embedding objectives and reporting only return parity; a contribution needs a differential beyond "different loss, similar return" (the IB-family saturation rule; R2-Dreamer clears it via the DMC-Subtle regime claim + compute [paper], most followers will not).
6. **prediction-loss-as-decision-evidence** — any decision-oriented claim supported solely by FVD/PSNR/1-step MSE (enforces §5.5; policy-ranking's τ or a closed-loop readout required).
7. **oracle-result-as-method** — reporting oracle-context/state/trigger headroom as if it were a deployable gain (enforces §5.4).

---

## H. Repository implementation table

All paths below marked [repo] were verified by downloading and inspecting the repositories on 2026-07-11. danijar/dreamerv3 internals beyond the entry point are [unverified].

| | R2-Dreamer (NM512/r2dreamer) | DreamerV3 | TD-MPC2 (nicklashansen/tdmpc2) |
|---|---|---|---|
| Verified layout | `train.py`, `trainer.py`, `dreamer.py` (class `Dreamer`: `act(obs,state,eval)`, `_imagine(start,imag_horizon)`, `_lambda_return`, `clone_and_freeze`), `rssm.py` (class `RSSM`: `obs_step`, `img_step`, `imagine_with_action`, `kl_loss`), `networks.py`, `configs/configs.yaml`, `configs/model/_base_.yaml` (`imag_horizon: 15`, `rep_loss: r2dreamer|dreamer|infonce|dreamerpro`), envs: dmc, dmc_subtle, memorymaze, metaworld, crafter, atari, isaaclab [repo] | Two options: (a) the PyTorch DreamerV3 reproduction inside r2dreamer (`rep_loss=dreamer`) — same verified paths as left, recommended; (b) danijar/dreamerv3 (JAX): entry `dreamerv3/main.py`, config `dreamerv3/configs.yaml` [repo-README]; internal module paths [unverified] | `tdmpc2/train.py`, `tdmpc2/evaluate.py`, `tdmpc2/tdmpc2.py` (class `TDMPC2`: `act`, `_plan` (MPPI), `_estimate_value`, `update_pi`, `_td_target`), `tdmpc2/common/world_model.py`, `tdmpc2/config.yaml` (`mpc: true`, `horizon: 3`, `iterations: 6`, `num_samples: 512`, `num_elites: 64`), envs: dmcontrol, metaworld, maniskill, myosuite [repo] |
| D.1 transition-family | Add context head to `networks.py`; condition `RSSM.img_step` on c; probe: linear regression on frozen `get_feat` outputs vs env parameters; oracle injection = feed true params as c. Retraining: probe no; method yes. Env access: parameter-modified DMC (edit `envs/dmc.py` task kwargs) or CARL [unverified path]. Metrics: inference gap, probe R². ~1 GPU-day probe. Confounder: probe leakage from proprio state — include state-only baseline. | Same via option (a). | Condition `world_model.py` dynamics on c (task-embedding machinery already exists for multitask — reuse it [repo: `task` argument threaded through `act`/`_plan`]); oracle c = task/param embedding set externally. |
| D.2 exploitability G | Log imagined λ-returns (already computed in `_cal_grad`/`_lambda_return`) vs periodic eval return; zero code beyond logging. Frozen-checkpoint: yes (`clone_and_freeze`). Confounder: imagined and real returns use different discounting — normalize. | Same via (a); in JAX repo, imagined returns are logged scalars [unverified]. | G = `_estimate_value` of executed plan vs realized return; log in `evaluate.py`. Frozen: yes. |
| D.3 event-triggered re-anchoring | Trigger = KL(prior‖posterior) per step: compute `RSSM.prior(deter)` vs `obs_step` posterior inside `Dreamer.act`; for Dreamer the "re-anchor" variant gates how often imagination starts are refreshed / policy latent is trusted open-loop. Frozen checkpoint: yes. | Same via (a). | Primary target. Wrap `TDMPC2.act`: cache the planned action sequence from `_plan`; per step compute latent-consistency error (predicted next z from `world_model` dynamics vs encoded obs); replan only on threshold crossing, else pop cached action (warm-start logic for `_prev_mean` already present in `_plan` [repo]). Eval-only change in `evaluate.py`. Metrics: return, planner calls, trigger-time histogram. Confounders: plan staleness interacts with `horizon: 3` — sweep cache length ≤ horizon; stochastic envs inflate triggers — include noise-floor calibration. |
| D.4 policy-ranking τ | Imagination-based candidate scoring vs simulator rollouts started from `env.physics.get_state()` (DMC supports state get/set [unverified API detail]); heavier than TD-MPC2 route. | Same. | Cleanest: sample elite plans in `_plan`, score with `_estimate_value`, replay same action sequences in the simulator, compute Kendall-τ. Needs env reset-to-state: DMC yes [unverified], Meta-World partial [unverified] — verify before committing. Frozen: yes. |
| D.5 belief 2×2 | Memory Maze env included [repo: `envs/memorymaze.py`, extra `memorymaze`]. Latent reset = reinitialize state in `act` via `get_initial_state`; mean-only ablation = replace stochastic sample with mode in `RSSM.get_feat` inputs at eval. Frozen: yes. | Same via (a). | Not the right harness (no posterior object). |

Expected experiment sizes: every probe ≤1 GPU-day on existing/1-seed checkpoints; each method-level study 2 GPUs × 1–2 weeks (≥3 tasks × ≥3 seeds per arm).

---

## I. Two-GPU generation-test plan (top 4)

Hardware assumption: 2 × 48 GB, independent; one run per GPU; all base agents (R2-Dreamer/DreamerV3-torch 12–25M configs, TD-MPC2 5M default) fit comfortably [repo: size configs].

**Week 1 — three frozen-checkpoint probes in parallel with 2 baseline trainings.**
- GPU-A trains 2–3 TD-MPC2 checkpoints (walker-run, quadruped-walk, one Meta-World task) while GPU-B trains one R2-Dreamer(rep_loss=dreamer) Memory Maze 9×9 + one DMC-vision agent, checkpointing every 100k steps.
- Probe 1 (exploitability G): pure logging on both — G(t) vs loss(t) curves. Stopping rule: if |partial corr(G, Δreturn | loss)| < 0.1 on all tasks → demote D.2 to META (monitor only).
- Probe 2 (event trigger): eval-time wrapper on TD-MPC2 checkpoints; threshold sweep. Stopping rule = kill criterion (≥40% planner-call cut at ≤2% return loss, structured triggers) — decidable in 2 GPU-days.
- Probe 3 (context/inference gap): parameter-modified DMC (mass/friction grid) rollouts through frozen encoders → history→parameter probe + oracle-context injected replan. Stopping rule: oracle gap <2% on all 3 tasks → demote D.1 for this regime.

**Week 2 — decision gate.** Rank surviving operators by measured headroom (oracle gap for D.1, Pareto dominance for D.3, dissociation strength for D.2/D.4). Commit both GPUs to the winner's minimal method experiment; keep the runner-up as the paper's diagnostic section.

**Expansion paths.** D.3 → AAAI paper: triggered TD-MPC2 + triggered Dreamer anchoring, 2 env families, oracle-trigger headroom, Pareto plots. D.1 → Information Sciences paper: full CARL-DMC grid, identifiability analysis, excitation study (dual-control probe), calibration of the context posterior. D.2 rides along in both as the monitoring instrument.

**Pre-registration rule (integrity §22):** each probe's kill criterion is written down (above) before the probe runs; a probe that dies is reported in the bank as negative evidence, not re-tuned.

---

## J. Publication routing

- **Strongest AAAI route:** event-triggered-re-anchoring (D.3). One mechanism, one page of math (trigger + reuse policy), oracle-trigger headroom, decisive compute-return Pareto on DMC+Meta-World, near-zero overhead, 8-page-shaped. Risk to manage: re-run the saturation search at submission time (the AdaJEPA future-work note is an invitation to others too).
- **Strongest Information Sciences route:** transition-family-factorization (D.1). Systematic multi-context empirical study + identifiability/calibration analysis + inference-gap theory-lite; the venue rewards breadth and ablation depth the operator naturally produces.
- **Information Fusion:** conditional go, one honest framing only — reliability-modeled fusion of heterogeneous predictive evidence inside a WM agent: k-step model-based value estimates + ensemble members + (if pixels+proprio) two sensor streams, with an explicit recoverability/conflict screen (rewritten N1, STEVE lineage). A single latent with multiple heads, or "posterior update as fusion," is scope inflation — do not submit that. If the target benchmarks stay proprio-only DMC, skip the venue.

---

## K. Final operator bank — retrieval index

| Operator | Failure signature (reach for it when…) | Core move | WM status | Gen-test |
|---|---|---|---|---|
| transition-family-factorization | collapse under changed dynamics params; oracle context works, inference fails (6/16/19) | factor dynamics into invariant mechanism × inferable low-dim context | NATIVE · Top | PASSED (probe queued) |
| model-exploitability-objectization | teacher-forced good, policy-rollout bad; planner wins in model, loses in env (2/10/11) | policy-conditioned error object G replaces average loss | ADAPTABLE · Top | PASSED (probe queued) |
| event-triggered-re-anchoring | planning compute flat-costed; surprises are rare and localized (1/12-adj) | innovation-gated replan/re-anchor replaces fixed cadence | ADAPTABLE · Top | PASSED (probe queued) |
| policy-ranking-ization | accurate dynamics, poor planning; pixel loss ↑ control ↛ (4/10/13) | model the plan ORDERING the planner consumes | ADAPTABLE · Top | PASSED (dissociation pre-registered) |
| belief-ization (rewritten) | hidden-state failures; history saturates (9/19) | posterior whose uncertainty is decision-load-bearing | NATIVE · Top | PASSED (2×2 designed) |
| transfer-operator-ization | fast-local-right global-wrong; basin revisits (17) | spectral transfer operator of latent dynamics | ADAPTABLE · Mid | needs planning-relevance probe |
| multiscale-correction-hierarchy | error compounds monotonically with horizon (1/17) | coarse jump + fine correction on an error hierarchy | ADAPTABLE · Mid | needs jump-head probe |
| memory-kernel-closure | longer history sub-linear; lag-correlated failures (9) | explicit memory kernel for dropped DOFs | ADAPTABLE ⚠ · Mid | most likely to fail |
| skill-option-ization | rollouts too deep; recurring sub-behaviors (16/17) | temporally-extended learned units | NATIVE · Mid | needs wall-clock readout |
| program-store-factorization | cliff at training episode length (9/15) | size-invariant program × addressable store | CONDITIONAL · Mid | Memory-Maze cliff probe |
| oracle-factorization-of-errors | any unexplained closed-loop failure (4/5/10) | component-swap bottleneck profile | META | protocol (standard first move) |
| two-part-code-ization | rank equal-loss WMs; audit complexity-purchased gains | prequential codelength + residual compressibility | META | eval test defined |
| conditional register (§D.7) | regime-specific | 12 cards | CONDITIONAL | on demand |

---

## Mandatory final answers (§21)

1. **Most natively aligned with world models:** belief-ization — POMDP/filtering roots, and its machinery is literally the RSSM posterior (latent-variable-ization is more foundational but saturated into the substrate).
2. **Most multimodal/VLA-biased:** chunk-ization (ACT-lineage; its differentials are imitation/serving concerns). Runners-up: recoverability-gated-fusion (rescuable via the STEVE-lineage rewrite), affordance/correspondence-field (not rescuable as WM objects).
3. **Demote first:** distribution-output-ization — fails Gate 10 ("add uncertainty") and Gate 6 (PETS/distributional-RL saturation) simultaneously, with every decision-relevant remnant already housed elsewhere.
4. **Merge which two:** observable-lifting + collective-variable-ization → transfer-operator-ization (one spectral object, two readouts). Secondary merges executed: ratio-ization→policy-ranking; {context, invariant, operator-lifting}→transition-family.
5. **Strongest low-compute AAAI potential:** event-triggered-re-anchoring — frozen-checkpoint, eval-time-only probe; compact mechanism; decisive Pareto readout.
6. **Strongest Information Sciences potential:** transition-family-factorization (systematic multi-context study + identifiability and calibration analysis).
7. **Genuine Information Fusion direction?** Narrowly yes, in exactly one form: reliability/recoverability-modeled fusion of heterogeneous predictive evidence (multi-horizon value estimates à la STEVE + ensemble members + genuinely distinct sensor streams). Anything less — multiple heads on one latent, posterior-update-as-fusion — is scope inflation; on proprio-only benchmarks the answer is no.
8. **Most important missing operator:** model-exploitability-objectization — it names the central WM pathology (signatures 2, 10, 11) that the old bank had no card for.
9. **Highest risk of being a renamed existing method:** policy-ranking-ization (vs value equivalence / decision-aware MBRL); hence its pre-registered dissociation kill test. (Among cards already killed: bits-back-refund-pricing, which in WM simply renames the RSSM ELBO.)
10. **Three cheap probes before any full reproduction:** (a) exploitability-gap G(t) logging across saved checkpoints; (b) frozen history→context probe + oracle-context injection on parameter-shifted DMC; (c) eval-time trigger-threshold sweep on TD-MPC2.
11. **Most efficient bottleneck-localizing oracle intervention:** posterior substitution with simulator ground-truth state at evaluation — one intervention cleanly splits estimation vs transition vs planning/value bottlenecks; oracle-context injection is the companion for OOD regimes.
12. **Testable on a frozen checkpoint:** event-triggered-re-anchoring (fully) — also the G-monitor, the τ rank probe, the belief 2×2, and the conformal wrapper.
13. **Most likely to fail its generation test:** memory-kernel-closure (a well-sized recurrent latent may leave no lag-structured residue; its ⚠ is retained). Bits-back already failed and is killed.
14. **Primary research direction under two 48 GB GPUs:** transition-family-factorization on CARL-style DMC with R2-Dreamer/TD-MPC2, with the exploitability monitor instrumented throughout — largest measured-headroom potential, two venue routes, and every step within budget. (If Week-1 probes invert the headroom ordering, event-triggered-re-anchoring takes the slot; the plan in §I decides this empirically, not by taste.)
15. **Retain only as diagnostic/evaluation protocol:** oracle-factorization-of-WM-errors (with the sufficient-summary collapse test and the counterfactual-action-fidelity probe inside it), plus two-part-code-ization as the model-comparison/audit instrument.

---

## Integrity notes (§22 compliance)

No operator was preserved for pedigree: two starred cards were killed (polarization, chunk), one ★★ was regime-restricted (recoverability-gated-fusion), and one starred Ilya-27 card was killed as the WM incumbent (bits-back). One attractive §14 candidate was surrendered to the 2025–26 literature rather than renamed (adaptive horizon). Oracle probes are labeled as headroom instruments, never as methods. Every promoted card carries a numerical kill criterion written before its probe runs. The bank shrank: 45 cards in, 5 top-tier + 8 active mid/meta out, with the rest regime-locked, archived, or dead.
