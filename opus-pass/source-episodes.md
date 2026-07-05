# Source Episodes — provenance + demoted cases (opus-pass)

> The raw episodes each operator was reverse-inferred from, plus operators DEMOTED to source-episode
> (explains a case but doesn't transfer, or lacks a cheap probe). Reports:
> `AI建模对象转移案例研究.md` (AI案例), `deeper-research-report.md` (report-1, a prior extraction — used as
> cross-check only), `deep-research-report (2).md` (report-2), `deep-research-report (3).md` (report-3),
> `deep-research-report (4).md` (report-4), `机器人建模对象图谱.md` (机器人), `科学计算建模范式转移.md` (科学计算).

## Provenance map (operator ← episodes it was inferred from)

| operator | primary source episodes |
|---|---|
| memory-kernel-closure | Mori–Zwanzig (科学计算 #1; report-3), Predictive State Representations (report-4), S4/SSM (AI案例 B), own-anomaly "~3 nats sequential bias" (project autopsy ledger) |
| observable-lifting | Koopman, Carleman, Perron–Frobenius, Takens, Lax pairs (科学计算 #2-6), DMD/EDMD/HAVOK/Koopman-MPC (report-3) |
| multiscale-correction-hierarchy | Multigrid, Algebraic Multigrid (report-3) |
| collective-variable-ization | Metadynamics, Diffusion Maps, MSM, VAMP/VAMPnets (report-3), Onsager–Machlup, Kramers rate (科学计算 #30-31) |
| flux-conservation-ization | Godunov/Finite-Volume, Lattice Boltzmann (report-3), Spatio-Temporal FlowNet (机器人; AI案例), GFlowNet (report-2) |
| factor-graph-ization | Factor graph + sum-product, Tanner, LDPC, Turbo (report-3; 科学计算 #33-34), Physics-Based RL logic (AI案例 C) |
| far-interaction-compression | Fast Multipole Method, Boundary Element Method (科学计算 #21,#29; report-3) |
| conservation-structure-ization | Symplectic integrators, Variational integrators, Port-Hamiltonian (科学计算 #17-19; report-3) |
| ratio-ization | NCE (report-2/3), DPO (AI案例 C; report-2), CPC/SimCLR (report-2), Speculative Decoding accept-rate (AI案例) |
| correction-field-ization | DSM/Score Matching/SMLD (AI案例 A; report-2), Diffusion Policy (机器人 #1) |
| path-straightening | Rectified Flow, Flow Matching (AI案例 A; report-2), Benamou–Brenier (科学计算 #11; report-3) |
| transport-coupling-ization | WGAN, Sinkhorn, Gromov–Wasserstein (科学计算 #14-16; report-2/3), Transporter (机器人 #17) |
| particle-measure-ization | SVGD (AI案例 A), EnKF/EKI (科学计算 #36; report-3), PETS/PILCO (report-4), SPH/MPM (report-3) |
| set-ization | Deep Sets (report-2), Slot Attention/FOCUS (机器人; report-4) |
| graph-ization | MPNN (report-2), Interaction Networks/OODP (report-4), scene-graph planning/SayPlan/HOV-SG (机器人; report-4) |
| object-slot-ization | Slot Attention (AI案例 C; 机器人), FOCUS/SOLD/COMPAS (机器人; report-4) |
| field-ization | NeRF (AI案例; report-2), LERF/NDF/iMAP/ConceptFusion (机器人; report-4) |
| affordance-field-ization | Where2Act, AO-Grasp, VoxPoser, CLIPort, Contact-GraspNet (机器人; report-4) |
| correspondence-field-ization | Transporter (机器人 #17; report-4), PerAct, NDF (report-4) |
| operator-lifting | DeepONet, FNO (AI案例 D; 科学计算; report-2/3), Operator Inference/DIMON/PINO (report-3) |
| sparse-support-ization | Sparse Coding/ICA (report-2), Compressed Sensing (科学计算 #37; report-3), SINDy (report-3) |
| polarization-ization | Polar Codes (科学计算 #33; report-3, which explicitly flags the spec-decode transfer) |
| invariant-ization | IRM/ICP (report-2/3), Clinical Foundation Models (AI案例 E), Group DRO (report-2) |
| group-equivariance-ization | GDN (机器人 #3), Group-Equivariant CNN/Clifford (report-2/3), PP-GraspNet (机器人) |
| belief-ization | Kalman/POMDP/PSR (report-3/4), RMA (机器人 #26), PlaNet/Dreamer/MuZero (report-4) |
| distribution-output-ization | Distributional RL (report-2), ProMP/Diffusion Policy (机器人; report-4), SAC (AI案例; report-2) |
| coverage-set-ization | Conformal Prediction (report-2/3) |
| latent-variable-ization | VAE/VI (report-2), Neural Processes (AI案例 B), Latent ODE/PEARL (report-3/4) |
| information-bottleneck-ization | IB/VIB (report-2), CPC (report-2), IB (科学计算 #35) |
| persistent-topology-ization | Persistent Homology (report-3), TDA (AI案例 table) |
| order-parameter-ization | Renormalization Group (科学计算 #25; report-3), Wang–Landau (report-3) |
| residual-ization | ResNet/Residual Physics (report-2/3), Residual RL/RWM (机器人; report-4) |
| context-ization | PEARL/RMA/UP-OSI/Domain-Randomization/SimOpt/VariBAD (机器人; report-4) |
| skill-option-ization | Options/MAXQ (report-4), DMP/LMP (机器人 #19), Play-plans/SDP/Voyager (机器人; report-4) |
| chunk-ization | ACT (机器人 #7), VQ-BeT/Diff-Control (机器人; report-4), ProMP (report-4) |
| sufficient-summary-functionalization | DFT, Born–Oppenheimer, Homogenization (科学计算 #26-28; report-3) |
| implicit-topology-ization | Level Set / Phase Field (科学计算 #20; report-3), GIGA/TSDF (机器人) |
| executable-spec-ization | Eureka/ARCHIE/PRM4RL (机器人; report-4), PDDLStream/Logic-Geometric-Programming (report-4) |

## Notable long-tail episodes (under-transferred into ML — the highest-value provenance)

These are the episodes that most justify the bank: field-famous operators that never crossed into ML.
- **Mori–Zwanzig / generalized Langevin** (stat-mech) → memory-kernel-closure. The archetype for "un-modeled
  DOFs = memory + noise," and the direct match for our own ~3-nats dLLM sequential-bias anomaly.
- **Koopman / Carleman / HAVOK** (dynamical systems) → observable-lifting. Nonlinearity-for-dimension trade,
  block-linear forecasting — barely used in decoding.
- **Multigrid / Algebraic Multigrid** (numerical linear algebra) → multiscale-correction-hierarchy. The
  coarse↔fine V-cycle is a near-perfect template for speculative decoding, essentially untried there.
- **Polar codes** (coding theory) → polarization-ization. Inducing a reliable/frozen split — a genuinely
  novel spec-decode operator.
- **Fast Multipole / Boundary Element** (numerical PDE) → far-interaction-compression. Hierarchical low-rank
  far-field ↔ long-context attention.
- **Factor graph / LDPC / Turbo** (coding/inference) → factor-graph-ization. Turbo's extrinsic-message loop
  prefigures iterative draft/target reconciliation.
- **Symplectic / Port-Hamiltonian** (geometric mechanics) → conservation-structure-ization. Long-horizon
  invariant preservation for world-model rollouts.
- **DFT / Born–Oppenheimer / Homogenization** (comp. chemistry/physics) → sufficient-summary-functionalization.
  A *sufficiency theorem* move (prove the low-dim summary suffices), rare in ML.
- **Metadynamics / MSM / VAMP** (molecular dynamics) → collective-variable-ization. Slow-coordinate discovery
  for skill/exploration and failure precursors.

## Demoted to source-episode / ARCHIVE (good concept, not yet a transferable operator here)

| demoted item | why demoted (not KEEP) | disposition |
|---|---|---|
| concept-bottlenecking (CBM) | sharp differential (test-time concept intervention) + cheap probe, but cross-domain episodes are thin (CBM + clinical only); hasn't transferred to generative/runtime | ARCHIVE — revisit when VLA/MLLM cases accrue |
| soft-target-ization (distillation) | has a clean differential (inter-class dark knowledge) + probe, but is closer to a supervised-target rewrite than an object-shift *family*; also pure canon | ARCHIVE as a distillation-chapter operator (kept out of KEEP to avoid diluting long-tail bias) |
| low-rank-delta-ization (LoRA) | strong, but the repetition clusters in PEFT only; it is a parameter-adaptation trick, not a modeling-object shift with a mechanism differential | ARCHIVE — PEFT branch |
| prompt/prefix-externalization | "task → conditioning object" is useful, but the differential depends on a specific base-model interface, not a domain-free prediction | ARCHIVE — needs a concrete runtime/VLA differential |
| hypernetwork parameter-generation | "weights as output object" is real but source episodes are sparse and the cheap probe is ill-defined pre-training | ARCHIVE — no clean cheap probe |
| semantic-residual-ization (RDA) | genuine (scalar → per-subtask diagnostic vector) with a clean probe, but currently one source line (reward design); fold under residual-ization until it repeats | SOURCE-EPISODE — candidate to promote |
| density-of-states-ization (Wang–Landau) | elegant (model DOS not temp-specific samples), but niche; folded into order-parameter-ization as a positive example | SOURCE-EPISODE |
| worst-group-reweighting (Group DRO) | more objective-reweighting than a new mediating object; kept as a positive example under invariant-ization | SOURCE-EPISODE |
| Gato / RT-2 "tokenize everything" | flagged even by the source reports as boundary/interface-repacking; no new predict/measure/control object | SOURCE-EPISODE (see anti-patterns for the pure form) |

## Cross-check against the prior extraction (report-1 / deeper-research-report.md)
report-1 independently produced 32 KEEP operators with the same schema. This pass agrees on the core
(ratio/score/energy/denoising/flow/transport/latent; set/graph/slot/field/affordance/correspondence/operator/
observable; factor-graph/flux/particle/collective-var/level-set/belief/trajectory-dist/chunk; skill/plan/
residual/context/memory-kernel/ensemble/invariant/manifold). This pass DIVERGES by (a) promoting more
long-tail math operators report-1 omitted — multiscale-correction-hierarchy, far-interaction-compression,
conservation-structure-ization, sparse-support-ization, **polarization-ization**, persistent-topology,
order-parameter-ization, sufficient-summary-functionalization, coverage-set-ization — because they generate
distinct killable spec-decode/dLLM candidates; and (b) merging report-1's energyization into
correction-field/affordance-field (energy is a carrier, and its differential — argmin/ranking — is captured by
those two), and merging manifoldization into group-equivariance-ization + conservation-structure-ization.

## Ilya-27 pass provenance (2026-07-04 — Fable5 propose → Opus corrosion; papers = `papers/IlyaSutskever_Shared_27Papers`)

Operator ← source paper (Ilya-27 net-new. STATUS after the 2026-07-04 re-audit: N4–N7 = ★ object-shift cards in `operators.md`; N8/N9 = RECLASSIFIED to its meta/eval subsection [no longer ★]; N10 = DEMOTED to this file — see the re-audit section below):
| operator | source paper(s) |
|---|---|
| N4 two-part-code-ization ★★ | MDL tutorial (Grünwald) + Keeping NNs Simple (Hinton–van Camp) + Kolmogorov book; trajectory facet ← Coffee Automaton (Aaronson/Carroll/Ouellette, 1405.6903) |
| N5 bits-back-refund-pricing ★ | Keeping NNs Simple §5–7 (Hinton–van Camp) + Variational Lossy Autoencoder |
| N6 program-store-factorization ★ | Neural Turing Machines (Graves et al., 1410.5401) |
| N7 selection-output-ization ★ | Pointer Networks (Vinyals et al., 1506.03134) |
| N8 performance-law-ization — RECLASSIFIED → meta/eval | Scaling Laws for Neural LMs (Kaplan et al., 2001.08361; floor term ← Chinchilla) |
| N9 simplicity-weighted-aggregation — RECLASSIFIED → meta/eval | Machine Super Intelligence (Legg–Hutter Υ) |
| N10 regeneration-depth-ization — DEMOTED (see re-audit section below) | Bennett logical depth via Coffee Automaton §2.3 + Antunes–Fortnow |

Folded / held (not promoted): structure-noise-bipartition → folded into N4 (trajectory facet) ·
linearization-as-latent (Order Matters) → refinement note on #14 set-ization · endpoint-variation-localization
(First Law of Complexity) → HELD, canon-discount (= influence functions / adjoint / implicit-diff).

Canon deduped, NO card (the discount rule): ResNet ×2 → #32 residual-ization · Dilated Conv → #3 + #32 ·
Relation Nets / Relational RNN → #15 + #16 · MPNN + Neural Quantum Chem → #15 + #20 · Attention · AlexNet ·
Deep Speech 2 · GPipe · NMT-align · 3 LSTM/RNN blogs · Annotated Transformer · RNN-dropout = backbone/scaling/
expository/reg-knob (see `anti-patterns.md` for the killed forms).

## 2026-07-04 re-audit demotions (independent Opus + GPT-5.5/codex — both agreed)

Two independent corrosion re-audits (main-loop Opus + GPT-5.5 via codex) each flagged these: they PASS the
deletion test (a real differential) but lack a killable LIVE-direction `generation_test`. DEMOTED from
`operators.md` to here — content preserved below so each is revivable; not deleted.

- **N10 `regeneration-depth-ization`** (Bennett logical depth; Coffee Automaton §2.3 + Antunes–Fortnow).
  MOVE: structure = the SEQUENTIAL COMPUTE to regenerate an object from a near-minimal description (depth),
  not description length; equal-size / equal-likelihood objects can differ enormously in depth. DIFFERENTIAL:
  matched-likelihood samples diverge FIRST when the sequential budget is cut (fewer denoising steps / shorter
  CoT / wider parallel commits); resists amortization into a small fast student. PROBE: sweep the sequential
  budget on matched-likelihood outputs, record which fail first. Distinct from N4 (TIME-to-regenerate vs
  description-length/SPACE). WHY DEMOTED: proxy-sensitive (which regenerator?), uncomputable, generates only
  on the archived dLLM/spec-decode directions. REVIVE if a diffusion-LLM / speculative-decoding direction goes live.
- **#30 `persistent-topology-ization`** (Persistent Homology / TDA). MOVE: replace fixed-scale geometric
  features with birth–death topological features (persistence diagram / barcode) across a filtration.
  DIFFERENTIAL: scale-dependent topological signatures stable under small perturbation, distinguishing
  structures a Euclidean distance conflates. PROBE: persistence diagram vs feature-distance on a toy embedding;
  test perturbation stability. WHY DEMOTED: no killable live-direction candidate. REVIVE if a latent-topology /
  OOD-detection direction goes live.
- **#31 `order-parameter-ization`** (Renormalization Group; mean-field / phase transitions; Wang–Landau).
  MOVE: track a coarse order parameter + its coarse-graining/RG flow, watching for a sharp transition in a
  control parameter. DIFFERENTIAL: universality (detail-independence near a transition), the transition
  location, and data-collapse under rescaling. PROBE: sweep a control parameter (data/model size, temperature,
  noise); look for a sharp jump + data-collapse. WHY DEMOTED: no concrete VLA/diffusion/spec-decode
  generation_test. REVIVE if a training-dynamics / grokking / emergence / phase-transition direction goes live.

Also flagged (single-engine DEMOTE call, KEPT in `operators.md` with ⚠ in the index — needs a live
generation_test or faces demotion next pass): **#21 sparse-support-ization**, **#36 sufficient-summary-functionalization**.
RECLASSIFIED (not demoted) to a meta/eval subsection of `operators.md`: **N8 performance-law-ization**,
**N9 simplicity-weighted-aggregation** (both operate on a meta-object — a performance law / an evaluation
measure — not on the modeling object of the system under study).
