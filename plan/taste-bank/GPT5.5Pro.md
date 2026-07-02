I treated the uploaded reports as episode evidence, but re-ran the gate instead of inheriting the existing 32-card bank. The reports already define the right admission rule—remove old complexity, produce a differential prediction, support a cheap probe, and be falsifiable—while warning that carrier names, bigger models, token unification, and module additions are not operators by themselves.  I therefore pruned/merged to **22 KEEP operators** and added the two seed-anomaly operators as first-class cards.

I use **VERIFIED-against-paper** when I checked the source paper/project/official abstract directly, and **INFERRED** when the transferable operator or transfer prediction is my reverse-inference from the episode or from your seed anomaly.

---

# KEEP operators, ranked by generativity × transfer breadth

## 1. `lag-kernelization`

**operator_name**
`lag-kernelization`

**one_sentence_core_move**
Do not ask longer context to implicitly absorb residual dependence; carve the unresolved sequential dependence into an explicit learned lag/memory kernel.

**old_object_pattern → new_object_pattern**
Markov state / longer context window / independent token canvas → resolved state plus lagged residual kernel over omitted temporal degrees of freedom.

**mathematical_frame**
memory-kernel / Volterra convolution / predictive-state residual / generalized Langevin closure.

**core_simplification**
It makes the omitted history simpler: instead of expanding the entire context or hidden state, it gives the missing non-Markov effect a small carrier whose support, sign, and lag length can be measured.

**differential_prediction**
A fixed sequential-dependency residue should remain after context extension, but disappear or sharply shrink when a learned lag term is added; shuffling or zeroing the lag should restore the residue. **INFERRED** from your diffusion-LLM seed anomaly; Mori–Zwanzig’s “unresolved variables become memory + noise” mechanism is **VERIFIED-against-paper/source**.   ([arXiv][1])

**cheap_probe**
Freeze the diffusion-LLM backbone and train a tiny lag head on held-out denoising loss: A = content-only, B = content + lag, C = content + lag shuffled/zeroed. Kill if B does not improve over A, or if C does not collapse back toward A.

**failure_signature**
A stable lag-shaped dependency remains after larger context, larger canvas, or more denoising steps; a small learned lag term helps disproportionately.

**transfer_targets**
diffusion-LLM joint assembly: lag-conditioned denoising head; speculative decoding: delay-aware draft correction; systems: queue/backlog memory kernel; VLA: sensor-latency or action-history kernel.

**positive_examples · negative_examples/when_it_misleads**
Positive: Mori–Zwanzig closure, HAVOK forcing, predictive-state representations, structured state-space kernels. Negative: “just add more context,” arbitrary RNN hidden state, or a generic cache with no lag-shuffle falsifier.

**source_episodes**
Mori–Zwanzig formalism; HAVOK; S4/SSM-style memory; your diffusion-LLM fixed ~3-nats anomaly; prior held-out diffusion-loss probe design with shuffled/zeroed controls.   

---

## 2. `recoverability-gated-fusion`

**operator_name**
`recoverability-gated-fusion`

**one_sentence_core_move**
Before reweighting modalities, test whether any modality is actually recoverable from the others; only then treat reliability as a routing object.

**old_object_pattern → new_object_pattern**
Always-fuse / always-reweight modality scores → recoverability matrix plus reliability policy over redundant, conflicting, or indispensable evidence.

**mathematical_frame**
conditional redundancy graph / information-recovery matrix / reliability posterior / decision arbitration.

**core_simplification**
It removes impossible rescue work: if every modality is individually necessary and no modality can be reconstructed from the others, fusion reweighting has no redundant evidence to exploit.

**differential_prediction**
Reliability reweighting helps under benign conflict or missing/noisy single modalities, but cannot help when recoverable_fraction ≈ 0 and every modality’s removal collapses success; in that regime, forced reweighting should either do nothing or degrade performance. **INFERRED** from your VLA seed anomaly; related multimodal conflict/reliability behavior is **VERIFIED-against-paper**.   

**cheap_probe**
Compute a leave-one-modality-out matrix and a tiny conditional imputer/probe before training: for each modality (m), test whether (z_m) or task-relevant residuals are predictable from (z_{\neg m}). Kill fusion-reweighting if all removals collapse success and all conditional recovery probes fail.

**failure_signature**
All single-modality ablations are fatal; pairwise substitutions do not restore task success; reliability weights saturate but success does not recover.

**transfer_targets**
VLA multimodal fusion: precondition check before reliability router; MLLM grounding: detect irreducible modality conjunction; OOD/robustness: separate redundancy failures from contradiction failures; dataset evaluation: label “non-recoverable multimodal tasks.”

**positive_examples · negative_examples/when_it_misleads**
Positive: DCR/ADA-style arbitration under modality conflict; EBMC-style reliability and trust distillation when remaining modalities compensate; context-specific credibility measures. Negative: reweighting when the task is genuinely conjunctive, text-only fallback on proprioceptive-contact tasks, or treating complementarity as redundancy.

**source_episodes**
VLA recoverable_fraction ≈ 0 anomaly; DCR/ADA conflict arbitration; EBMC modality reliability/trust distillation; C2MF context-specific credibility.   

---

## 3. `dependency-bounded-assembly`

**operator_name**
`dependency-bounded-assembly`

**one_sentence_core_move**
Replace independent parallel commits with an explicit dependency graph over candidate pieces, then assemble only low-coupling sets.

**old_object_pattern → new_object_pattern**
Token-wise confidence / factorized parallel denoising / independent draft acceptances → dependency-constrained commit set.

**mathematical_frame**
dependency graph / conditional-independence test / attention-derived coupling / conflict graph.

**core_simplification**
It makes joint assembly simpler by removing the false factorization assumption; the expensive object is no longer the full joint distribution, only the dependency boundary among candidate commits.

**differential_prediction**
High-confidence tokens that are strongly mutually dependent should fail when committed together, while lower-confidence but conditionally independent sets can be safely committed in parallel. **VERIFIED-against-paper** for discrete diffusion parallel decoding work identifying dependence as the bottleneck. ([arXiv][2])

**cheap_probe**
On frozen model samples, estimate pairwise dependency from attention, conditional entropy, or remask sensitivity; compare confidence-only commit order vs dependency-pruned commit sets on denoising loss and exact-match repair.

**failure_signature**
Parallel decoding gets speed but loses correctness; confidence is high but simultaneous token commitment breaks syntax, math, or code consistency.

**transfer_targets**
diffusion-LLM joint assembly: dependency-pruned commit policy; speculative decoding: accept multiple draft tokens only if dependency graph is sparse; systems: batch jobs only when resource couplings are low.

**positive_examples · negative_examples/when_it_misleads**
Positive: dependency-guided discrete diffusion decoding, conditional-independence parallel sampling, speculative verification. Negative: confidence thresholding alone, entropy-only unmasking, or assuming attention weights are dependencies without a remask-sensitivity test.

**source_episodes**
DAPD, PUNT, DEMASK, Block Diffusion, speculative decoding. ([arXiv][2])

---

## 4. `factor-message-localization`

**operator_name**
`factor-message-localization`

**one_sentence_core_move**
Turn an intractable global constraint into local factors that exchange messages.

**old_object_pattern → new_object_pattern**
Global joint distribution / dense consistency constraint / whole-system verification → factor graph with local factors and messages.

**mathematical_frame**
factor graph / bipartite graph / sum-product messages / belief propagation.

**core_simplification**
It removes global enumeration by making every constraint local and reusable; the model no longer has to solve the whole joint object at once.

**differential_prediction**
Local factor marginals should identify which constraint caused failure, and replacing one local factor should change only its Markov blanket before affecting global belief. **VERIFIED-against-paper** for factor-graph/sum-product formulation.  ([IEEE Xplore][3])

**cheap_probe**
Hand-build a tiny factor graph over existing model outputs—syntax, tool schema, visual evidence, action feasibility—and compare local message diagnostics to a monolithic verifier on a small held-out set.

**failure_signature**
The system fails globally but no module can identify which assumption broke; dense fusion or dense verification gives a scalar score only.

**transfer_targets**
MLLM grounding: factors for object, relation, geometry, language; speculative decoding: local consistency messages; systems: dependency graph for latency/failure localization.

**positive_examples · negative_examples/when_it_misleads**
Positive: factor graphs, Tanner graphs, LDPC, turbo decoding, physics-based relational RL. Negative: ordinary GNN layers with no factor semantics; a graph visualization that does not produce local marginals.

**source_episodes**
Factor Graphs + Sum-Product; Tanner Graph Codes; LDPC; Turbo Codes.  

---

## 5. `flux-balance-localization`

**operator_name**
`flux-balance-localization`

**one_sentence_core_move**
Replace pairwise correlation with a conserved source–sink flow ledger.

**old_object_pattern → new_object_pattern**
Node similarity / static adjacency / attention weights → local fluxes across boundaries with conservation constraints.

**mathematical_frame**
numerical flux / continuity equation / source-sink graph / transport ledger.

**core_simplification**
It removes unaccounted “teleporting evidence”: interactions are represented as what leaves one cell/node and enters another, so conservation violations become visible.

**differential_prediction**
The new object predicts conservation error, bottleneck location, and source–sink attribution; a correlation graph can be accurate on average while violating the ledger locally. **INFERRED** from finite-volume and FlowNet episodes.  

**cheap_probe**
Wrap current attention or routing outputs in a conservation audit: compute inflow, outflow, residual, and bottleneck residual before training a new model.

**failure_signature**
Attention finds plausible neighbors but violates physical/resource/accounting constraints; forecasts look smooth but create or destroy mass, tokens, queue load, or evidence.

**transfer_targets**
systems throughput/latency: request-flow ledger; diffusion-LLM: token-mass transport during remasking; VLA: contact-force or object-flow conservation; dataset evaluation: distribution-shift source–sink map.

**positive_examples · negative_examples/when_it_misleads**
Positive: Godunov/finite volume, lattice Boltzmann, spatio-temporal FlowNet. Negative: calling softmax attention “flow” without conservation or source–sink residuals.

**source_episodes**
Godunov finite-volume methods; Lattice Boltzmann; Spatio-Temporal FlowNet.  

---

## 6. `multiscale-residual-coarsening`

**operator_name**
`multiscale-residual-coarsening`

**one_sentence_core_move**
Stop correcting all errors at one scale; move the stubborn residual onto a coarser object where it becomes local.

**old_object_pattern → new_object_pattern**
Single-resolution error / flat token correction / one-level verifier → residual hierarchy with restriction, coarse correction, and prolongation.

**mathematical_frame**
multigrid / coarse variables / residual hierarchy / prolongation–restriction operators.

**core_simplification**
It separates easy high-frequency errors from hard low-frequency/global errors; the model no longer asks a local smoother to fix global drift.

**differential_prediction**
A flat local corrector should rapidly remove local noise but stall on low-frequency/global errors; a coarse residual pass should remove the stalled component. **INFERRED** from multigrid episodes.  

**cheap_probe**
Run a frozen model error spectrum: bucket residuals by local vs global span, then test a cheap coarse summary corrector before full retraining.

**failure_signature**
Iterative refinement improves early then plateaus; remaining errors are global consistency, long-range constraint, or document-level plan errors.

**transfer_targets**
speculative decoding: phrase/block/document-level verifier hierarchy; diffusion-LLM: coarse-to-fine canvas correction; VLA: task-level then action-level correction; systems: cluster-level then request-level scheduling.

**positive_examples · negative_examples/when_it_misleads**
Positive: geometric multigrid, algebraic multigrid, hierarchical planners. Negative: multi-layer networks without explicit residual transfer across scales.

**source_episodes**
Multigrid; Algebraic Multigrid; hierarchical residual correction.  

---

## 7. `polarization-partitioning`

**operator_name**
`polarization-partitioning`

**one_sentence_core_move**
Transform a continuum of medium-confidence choices into polarized reliable and unreliable subchannels.

**old_object_pattern → new_object_pattern**
Uniform uncertain channel / undifferentiated token confidence / average reliability → polarized subchannels with reliable set and frozen/noisy set.

**mathematical_frame**
channel polarization / recursive transform / reliability ordering / frozen set.

**core_simplification**
It removes the need to treat every position equally; computation and supervision are concentrated on subchannels that become predictably reliable.

**differential_prediction**
After the transform, reliability should become more bimodal; using reliable channels while freezing or deferring noisy ones should improve speed or accuracy over treating all positions uniformly. **VERIFIED-against-paper** for polar coding.  ([arXiv][4])

**cheap_probe**
Apply a small fixed transform over token positions, draft heads, or modality streams and plot reliability entropy before/after; kill if reliability does not polarize.

**failure_signature**
Many medium-confidence positions cause expensive verification; confidence thresholds are unstable across examples.

**transfer_targets**
speculative decoding: polarize draft tokens into accept-fast vs verify-later; distillation-fidelity: allocate teacher supervision to reliable subchannels; diffusion-LLM: commit reliable canvas positions and remask noisy ones.

**positive_examples · negative_examples/when_it_misleads**
Positive: Polar Codes, reliability-ordered decoding, frozen bits. Negative: arbitrary pruning, top-k confidence, or static easy/hard labels without a transform that increases polarization.

**source_episodes**
Polar Codes; channel polarization.  

---

## 8. `barrier-certificate-localization`

**operator_name**
`barrier-certificate-localization`

**one_sentence_core_move**
Replace soft penalties over future trajectories with a local certificate that forbids leaving the safe set.

**old_object_pattern → new_object_pattern**
Heuristic safety reward / reranker / full-horizon trajectory penalty → barrier certificate over current state derivative.

**mathematical_frame**
control barrier function / forward-invariant set / Lie derivative / local QP filter.

**core_simplification**
It removes the need to search the whole future to certify safety; the hard object is a local inequality at the boundary.

**differential_prediction**
The barrier should reject unsafe actions even when the policy or reward model ranks them highly, and the rejection should correlate with boundary-crossing risk. **VERIFIED-against-paper/source**.  ([IEEE Xplore][5])

**cheap_probe**
Before training, define a candidate barrier on logged trajectories and measure whether barrier violations predict future failure better than reward or confidence.

**failure_signature**
Safety failures are rare but catastrophic; average reward improves while boundary violations persist.

**transfer_targets**
VLA reliability: safety filter over actions; MLLM grounding: geometric no-go certificate; systems: latency/SLA barrier before dispatch; speculative decoding: schema-validity barrier before token acceptance.

**positive_examples · negative_examples/when_it_misleads**
Positive: Control Barrier Functions, safety QP filters. Negative: adding a penalty term and calling it a barrier; barriers with no forward-invariance test.

**source_episodes**
Control Barrier Functions in robotics/control.  

---

## 9. `observable-lifting`

**operator_name**
`observable-lifting`

**one_sentence_core_move**
Trade nonlinear state evolution for linear evolution in a richer observable space.

**old_object_pattern → new_object_pattern**
Nonlinear raw state dynamics / direct next-state predictor → lifted observables with approximately linear operator evolution.

**mathematical_frame**
Koopman operator / EDMD dictionary / spectral modes / lifted linear predictor.

**core_simplification**
It makes nonlinear evolution simpler by moving nonlinearity into the observation map; planning and extrapolation become linear algebra in the lifted space.

**differential_prediction**
A lifted linear predictor should extrapolate dominant timescales and regime transitions better than a raw-state next-step model, even when one-step error is similar. **VERIFIED-against-paper** for Koopman/EDMD.  ([arXiv][6])

**cheap_probe**
Fit EDMD or a linear probe on frozen hidden states; compare long-horizon rollout, spectral stability, and failure-regime separability to raw next-state regression.

**failure_signature**
One-step predictions look good but rollout drifts; hidden-state trajectories show coherent oscillatory or slow modes that the model does not exploit.

**transfer_targets**
speculative decoding correction: block-linear hidden predictor; VLA world models: lifted MPC; systems: telemetry mode forecasting; OOD: spectral shift detector.

**positive_examples · negative_examples/when_it_misleads**
Positive: Koopman operator, DMD, EDMD, Koopman MPC. Negative: PCA-only compression with no operator or spectral prediction.

**source_episodes**
Koopman Operator; DMD; EDMD; Koopman MPC. 

---

## 10. `operator-lifting`

**operator_name**
`operator-lifting`

**one_sentence_core_move**
Lift learning from instance input-output pairs to a reusable map between function families.

**old_object_pattern → new_object_pattern**
Fixed-grid instance predictor / point-to-point regression → function-to-function operator.

**mathematical_frame**
neural operator / branch–trunk decomposition / Fourier kernel / graph integral kernel.

**core_simplification**
It removes per-instance retraining and grid binding; boundary conditions, resolutions, and geometries become inputs to one reusable operator.

**differential_prediction**
The model should generalize to unseen resolution, boundary condition, or geometry better than an instance predictor with similar capacity. **VERIFIED-against-paper** for DeepONet and neural-operator framing.  ([arXiv][7])

**cheap_probe**
Train a tiny operator on a toy family with held-out resolution or boundary conditions; kill if it behaves like a larger pointwise regressor.

**failure_signature**
Every new condition or resolution requires retraining; data are many samples from the same mechanism but the model treats them as unrelated.

**transfer_targets**
VLA: scene-function → affordance-function policy operator; distillation-fidelity: teacher function → student function matching; systems: workload curve → latency curve operator.

**positive_examples · negative_examples/when_it_misleads**
Positive: DeepONet, FNO, Graph Neural Operator, PINO. Negative: multi-output regression without held-out family generalization.

**source_episodes**
DeepONet; FNO; Graph Neural Operator; PINO.  

---

## 11. `affordance-fielding`

**operator_name**
`affordance-fielding`

**one_sentence_core_move**
Replace “what object is this?” with “where and how can the agent act?”

**old_object_pattern → new_object_pattern**
Object class / global pose / text plan / fixed primitive → spatial actionability, value, or constraint field.

**mathematical_frame**
affordance field / 3D value map / voxel energy field / heatmap over interaction points.

**core_simplification**
It removes the category-to-planner cascade; task-relevant geometry is directly represented as a spatial field that can be optimized or replanned over.

**differential_prediction**
The field should predict actionable contact points and recover under perturbations before any full policy training; a class/pose pipeline should fail on unknown objects or ambiguous instructions. **VERIFIED-against-paper** for VoxPoser/Transporter-style spatial formulation and **INFERRED** for the de-domained operator.   ([arXiv][8])

**cheap_probe**
Freeze perception; train or synthesize a small actionability/value map and evaluate contact-point recall, perturbation replanning, and open-vocabulary target grounding.

**failure_signature**
The model names the object correctly but cannot decide where to touch, push, avoid, or place.

**transfer_targets**
VLA multimodal fusion: language + vision + geometry as field sum; MLLM grounding: 3D language-conditioned fields; robotics: zero-shot constraint maps.

**positive_examples · negative_examples/when_it_misleads**
Positive: VoxPoser, Where2Act, CLIPort, PerAct, Contact-GraspNet, AO-Grasp. Negative: saliency maps not used for control; text plans with no executable spatial carrier.

**source_episodes**
VoxPoser, Where2Act, CLIPort, PerAct, Contact-GraspNet.  

---

## 12. `correspondence-fielding`

**operator_name**
`correspondence-fielding`

**one_sentence_core_move**
Turn action prediction into spatial correspondence rather than direct coordinate regression.

**old_object_pattern → new_object_pattern**
SE(3) pose regression / single action vector / keypoint coordinate → pick-place correspondence field or spatial transport operator.

**mathematical_frame**
correlation field / transport operator / dense correspondence map.

**core_simplification**
It removes global pose estimation as an intermediate bottleneck; geometry is solved as local matching and displacement.

**differential_prediction**
The model should preserve equivariance under translations/rotations and expose multiple feasible target correspondences; direct regression should average or break symmetry. **VERIFIED-against-paper** for Transporter Networks’ spatial-displacement formulation.  ([arXiv][9])

**cheap_probe**
Use frozen visual features and a correlation head on synthetic relocation tasks; test equivariance, multi-target recall, and occlusion robustness.

**failure_signature**
Pose/action heads collapse on symmetric objects, deformables, occlusion, or cross-resolution UI/robot screens.

**transfer_targets**
VLA robotics: correspondence action head; MLLM grounding: region-to-region matching; systems/UI agents: click/drag as screen correspondence.

**positive_examples · negative_examples/when_it_misleads**
Positive: Transporter Networks, PerAct, Contact-GraspNet. Negative: attention heatmaps that are never used as the action object.

**source_episodes**
Transporter Networks; PerAct; Contact-GraspNet; Avoid Everything. 

---

## 13. `object-slotting`

**operator_name**
`object-slotting`

**one_sentence_core_move**
Force a scene representation to decompose into persistent, exchangeable object carriers.

**old_object_pattern → new_object_pattern**
Global latent / whole-frame feature map / monolithic world state → object-slot set with factorized latent dynamics.

**mathematical_frame**
slot set / factorized latent variables / competitive attention / object graph.

**core_simplification**
It makes object identity and object interaction simpler: each object gets a carrier, so global features no longer have to remember all bindings at once.

**differential_prediction**
Slot interventions, swaps, occlusions, and object-count extrapolation should produce localized effects; global latents should entangle or drift identities. **INFERRED** from object-centric world-model episodes.  

**cheap_probe**
Freeze perception and train a slot probe; evaluate swapping, occlusion persistence, counterfactual object drops, and count extrapolation before full policy training.

**failure_signature**
Object identity drifts; adding distractor objects breaks planning; global latent reacts to irrelevant object movement.

**transfer_targets**
VLA reliability: object-level modality binding; MLLM grounding: slot-language alignment; OOD: compositional object extrapolation.

**positive_examples · negative_examples/when_it_misleads**
Positive: Slot Attention, FOCUS, SOLD, COMPAS, object-centric dynamics. Negative: DETR queries or region tokens with no persistence/intervention semantics.

**source_episodes**
Slot Attention; FOCUS; SOLD; COMPAS; object-centric world models.  

---

## 14. `belief-sufficiency`

**operator_name**
`belief-sufficiency`

**one_sentence_core_move**
Replace raw observation history with the smallest uncertainty-bearing state sufficient for planning.

**old_object_pattern → new_object_pattern**
Observation stack / recurrent hidden state / current sensor frame → posterior belief over task-relevant hidden state.

**mathematical_frame**
belief state / Bayes filter / latent stochastic state / predictive-state representation.

**core_simplification**
It compresses history into a state object that carries uncertainty, so planning does not need the entire past.

**differential_prediction**
Belief entropy should predict when information-gathering actions are valuable; replacing belief with raw history should lose active sensing behavior. **VERIFIED-against-source/report** for Kalman/POMDP-style belief shift.  

**cheap_probe**
Train a small belief probe from short histories and test whether it predicts oracle hidden variables, failure probability, and value of information.

**failure_signature**
Failures arise from hidden state, occlusion, calibration, or uncertainty, not from immediate perception accuracy.

**transfer_targets**
VLA partial observability; MLLM temporal memory; systems uncertainty-aware scheduling; OOD active diagnosis.

**positive_examples · negative_examples/when_it_misleads**
Positive: Kalman Filter, POMDP belief, PlaNet/Dreamer RSSM, RMA/VariBAD. Negative: arbitrary RNN state with no uncertainty or information-gathering test.

**source_episodes**
Kalman Filter; POMDP belief; PlaNet; Dreamer; PEARL; VariBAD; RMA.  

---

## 15. `gap-contextification`

**operator_name**
`gap-contextification`

**one_sentence_core_move**
Turn distribution shift or sim-to-real mismatch into an online-estimated context variable.

**old_object_pattern → new_object_pattern**
Single robust policy / fixed simulator / shift as nuisance noise → latent context, extrinsics belief, or simulator-parameter posterior.

**mathematical_frame**
latent context variable / online system ID / task posterior / domain distribution.

**core_simplification**
It gives the shift a small object instead of forcing the main model to be robust to every possible environment at once.

**differential_prediction**
A few seconds or few examples should cluster environment/embodiment shift and improve adaptation; static robust baselines should fail on clustered but unseen shifts. **INFERRED** from PEARL/RMA/SimOpt episodes.  

**cheap_probe**
Fit a context encoder from short histories; test whether context clusters known conditions and predicts residual error before training a full adaptive policy.

**failure_signature**
The base model is mostly right but fails systematically by environment, robot embodiment, load, temperature, user, or simulator setting.

**transfer_targets**
VLA: embodiment/context token; systems: machine-state context for latency prediction; OOD: domain posterior; distillation: context-conditioned student.

**positive_examples · negative_examples/when_it_misleads**
Positive: PEARL, RMA, UP-OSI, Domain Randomization, SimOpt, VariBAD. Negative: task ID one-hot that cannot be inferred online.

**source_episodes**
PEARL; RMA; UP-OSI; Domain Randomization; SimOpt; VariBAD.  ([arXiv][10])

---

## 16. `ensemble-measure-lifting`

**operator_name**
`ensemble-measure-lifting`

**one_sentence_core_move**
Replace a single estimate or full covariance with a small empirical measure of hypotheses.

**old_object_pattern → new_object_pattern**
Point estimate / single Gaussian / full covariance matrix → ensemble particles, sample covariance, empirical posterior.

**mathematical_frame**
empirical measure / ensemble flow / sample covariance / particle belief.

**core_simplification**
It avoids storing or learning a huge covariance while preserving enough spread information for decisions.

**differential_prediction**
Ensemble spread should correlate with OOD, failure, or planning regret; a point model may remain confidently wrong. **INFERRED** from EnKF/PETS/SVGD episodes. 

**cheap_probe**
Run 5–20 lightweight heads or perturbation particles over frozen features and check spread-error correlation on held-out slices.

**failure_signature**
Single model confidence is miscalibrated; the system fails on uncertainty-sensitive decisions or rare OOD cases.

**transfer_targets**
OOD/robustness: spread-based abstention; VLA: particle belief for hidden objects/contact; systems: uncertainty-aware routing; speculative decoding: accept-risk ensemble.

**positive_examples · negative_examples/when_it_misleads**
Positive: EnKF, EKI, PETS, SVGD, particle filters. Negative: bagging only for accuracy gains with no decision use of ensemble spread.

**source_episodes**
Ensemble Kalman Filter; Ensemble Kalman Inversion; PETS; SVGD.  

---

## 17. `collective-variable-compression`

**operator_name**
`collective-variable-compression`

**one_sentence_core_move**
Compress raw trajectories into slow variables, bottlenecks, or metastable states that control rare transitions.

**old_object_pattern → new_object_pattern**
Full high-dimensional trajectory / raw trace / frame sequence → collective variables, free-energy surface, metastable-state graph.

**mathematical_frame**
collective variables / Markov state model / diffusion maps / VAMP singular functions / free-energy surface.

**core_simplification**
It removes fast irrelevant motion and retains slow decision-relevant coordinates.

**differential_prediction**
Failures and regime changes should align with slow variables or metastable transitions better than with raw PCA or local reconstruction error. **VERIFIED-against-paper** for VAMPnets/metadynamics-style episodes; transfer is **INFERRED**.  ([美国国家科学院院刊][11])

**cheap_probe**
Compute diffusion maps/VAMP/MSM on frozen trajectories or hidden states; test whether slow coordinates predict failures, skill boundaries, or OOD slices.

**failure_signature**
Long traces are hard to interpret; rare failures occur at hidden regime changes; PCA clusters look pretty but do not predict transitions.

**transfer_targets**
dataset evaluation: latent coverage by slow modes; VLA: skill discovery and failure precursors; diffusion-LLM: reasoning-mode transitions; systems: incident-state graph.

**positive_examples · negative_examples/when_it_misleads**
Positive: Metadynamics, Diffusion Maps, MSM, VAMP, VAMPnets. Negative: UMAP/PCA visualization with no transition/timescale prediction.

**source_episodes**
Metadynamics; Diffusion Maps; MSM; VAMP; VAMPnets; Information Bottleneck.  

---

## 18. `transport-coupling`

**operator_name**
`transport-coupling`

**one_sentence_core_move**
Replace similarity scoring with an explicit plan for how mass/evidence moves between two supports.

**old_object_pattern → new_object_pattern**
Cosine similarity / hard matching / KL or JS distance / direct pose regression → transport coupling, cost matrix, density path.

**mathematical_frame**
optimal transport / Sinkhorn coupling / Wasserstein geometry / Gromov-Wasserstein / transport plan.

**core_simplification**
It makes alignment errors visible: support mismatch, many-to-one assignment, and unmatched mass become part of the object rather than hidden inside a scalar score.

**differential_prediction**
When embeddings look similar but alignment is wrong, the coupling matrix should reveal mass splits, holes, or support mismatch; simple similarity cannot. **INFERRED** from OT episodes; Flow Matching’s vector-field/path use is **VERIFIED-against-paper**.  ([arXiv][12])

**cheap_probe**
Compute Sinkhorn plans between video/action/language segments or teacher/student logits and inspect coupling entropy, unmatched mass, and support mismatch before training.

**failure_signature**
High similarity but wrong grounding; dataset duplicates hide missing modes; student matches average teacher logits but misses structure.

**transfer_targets**
multimodal fusion: video-language-action alignment; dataset condensation: support coverage; distillation-fidelity: teacher-student coupling; VLA: correspondence planning.

**positive_examples · negative_examples/when_it_misleads**
Positive: Sinkhorn OT, WGAN, Gromov-Wasserstein, Benamou–Brenier dynamic OT, Flow Matching. Negative: adding a “Wasserstein loss” without inspecting or using a coupling object.

**source_episodes**
Sinkhorn; WGAN; Gromov-Wasserstein; Benamou–Brenier; Flow Matching; Transporter Networks.  ([arXiv][12])

---

## 19. `implicit-boundary-fielding`

**operator_name**
`implicit-boundary-fielding`

**one_sentence_core_move**
Replace explicit boundaries with an implicit field whose zero level set carries topology.

**old_object_pattern → new_object_pattern**
Front points / mesh boundary / bounding box / sharp interface → signed-distance, level-set, phase, or occupancy field.

**mathematical_frame**
level-set function / SDF / Hamilton–Jacobi PDE / phase field.

**core_simplification**
It removes explicit topology maintenance; merging, splitting, contact, and curvature live inside one scalar field.

**differential_prediction**
Topology changes should remain stable and differentiable under field evolution; explicit front/box tracking should require special-case repairs. **INFERRED** from level-set/phase-field episodes.  

**cheap_probe**
Convert existing boxes/masks to SDFs and test sub-voxel interpolation, topology perturbations, and gradient-guided correction.

**failure_signature**
Boxes or masks break under holes, contact, occlusion, merging, or deformable geometry.

**transfer_targets**
MLLM grounding: language-conditioned SDFs; VLA: contact boundary and safety fields; OOD: topology-stable object representation.

**positive_examples · negative_examples/when_it_misleads**
Positive: Level Set Method, phase field, TSDF, neural SDF, GIGA. Negative: high-resolution voxel grid with no continuous query or zero-level semantics.

**source_episodes**
Level Set Method; phase-field; TSDF/GIGA; implicit neural fields.  

---

## 20. `trajectory-chunking`

**operator_name**
`trajectory-chunking`

**one_sentence_core_move**
Model temporally coherent action chunks rather than isolated one-step actions.

**old_object_pattern → new_object_pattern**
Single-step Markov action / pointwise trajectory imitation → multi-step chunk, phase primitive, or attractor object.

**mathematical_frame**
chunked sequence / phase variable / dynamical movement primitive / trajectory distribution.

**core_simplification**
It removes high-frequency jitter and compounding single-step error by making short-horizon consistency the modeled object.

**differential_prediction**
There should be an optimal chunk horizon where jitter and compounding error fall without losing feedback responsiveness. **INFERRED** from ACT/DMP/ProMP episodes.  

**cheap_probe**
Train mini action heads for 1, 4, 8, 16-step chunks on the same frozen features; plot smoothness, intervention latency, and rollout success.

**failure_signature**
Single-step policy jitters, accumulates tiny errors, or cannot maintain phase in periodic or bimanual tasks.

**transfer_targets**
VLA robotics: latent action chunks; diffusion-LLM: blockwise joint assembly; systems: batched execution chunks; speculative decoding: chunk-level draft verification.

**positive_examples · negative_examples/when_it_misleads**
Positive: ACT, DMP, ProMP, Diff-Control. Negative: frame skip or action repeat without a learned chunk object.

**source_episodes**
ACT; DMP; ProMP; Diff-Control.  

---

## 21. `path-straightening`

**operator_name**
`path-straightening`

**one_sentence_core_move**
Make the generative or control path itself the object, then remove unnecessary curvature.

**old_object_pattern → new_object_pattern**
Arbitrary iterative refinement / random diffusion path / many-step rollout → low-curvature transport path or straightened velocity field.

**mathematical_frame**
rectified flow / displacement interpolation / velocity field / probability path.

**core_simplification**
It makes integration simpler: fewer solver steps are needed because the path has less curvature and less accumulated numerical error.

**differential_prediction**
At equal model quality, lower path curvature should predict better low-step sampling or rollout; crooked paths should degrade faster when step count is reduced. **VERIFIED-against-paper** for Flow Matching’s path/velocity framing; straightening transfer is **INFERRED**.  ([arXiv][12])

**cheap_probe**
Estimate path curvature or velocity residual on frozen trajectories and compare 1/2/4/8-step quality before retraining.

**failure_signature**
More denoising/refinement steps help, but low-step generation collapses; interpolation path is visibly curved or stiff.

**transfer_targets**
diffusion-LLM: low-step masked assembly; speculative decoding: straight hidden-state block flow; VLA: continuous action rollout; systems: smooth schedule migration.

**positive_examples · negative_examples/when_it_misleads**
Positive: Flow Matching, Rectified Flow, Benamou–Brenier displacement paths. Negative: generic smoothing regularizers with no low-step prediction.

**source_episodes**
Flow Matching; Rectified Flow; Benamou–Brenier dynamic OT.  ([arXiv][12])

---

## 22. `manifold-intrinsicization`

**operator_name**
`manifold-intrinsicization`

**one_sentence_core_move**
Move coordinates onto the intrinsic manifold or algebra where the symmetry is native.

**old_object_pattern → new_object_pattern**
Euclidean pose vector / Euler angles / independent scalar channels → Lie-group, group-equivariant, or multivector field.

**mathematical_frame**
Lie group / Riemannian manifold / group convolution / Clifford algebra / equivariant field.

**core_simplification**
It removes coordinate singularities and repeated data augmentation for symmetries that should be built into the object.

**differential_prediction**
Rotation, reflection, or coordinate-frame perturbations should preserve errors and predictions; Euclidean parameterizations should show discontinuities or sample inefficiency. **INFERRED** from group-equivariant and robot-pose episodes. 

**cheap_probe**
Run synthetic coordinate transforms on frozen features and compare continuity/equivariance error for Euclidean vs manifold heads.

**failure_signature**
Pose predictions fail at rotation wraparounds, coordinate-frame changes, or symmetric 6-DoF grasps.

**transfer_targets**
VLA: SE(3) action head; MLLM grounding: group-equivariant 3D fields; OOD robustness: coordinate-invariant features; robotics: grasp/manipulation diffusion on manifold.

**positive_examples · negative_examples/when_it_misleads**
Positive: Group Equivariant CNNs, GDN on SO(3)×R, Clifford Neural Layers, SE(3)-equivariant descriptor fields. Negative: using quaternions but training with naive Euclidean losses that ignore manifold geometry.

**source_episodes**
Group Equivariant CNNs; Clifford Neural Layers; GDN; Neural Descriptor Fields.  

---

# Final validator: held-out problem = VLA reliability-fusion

Held-out problem: a VLA task suite where language, vision, and proprioception are all individually necessary, removing any one modality collapses success, and recoverable_fraction ≈ 0. This is deliberately hostile to naive reliability reweighting.

Each KEEP operator had to generate a concrete candidate that can be killed cheaply:

| operator                           | killable candidate on VLA reliability-fusion                                             | discriminator + cheap probe                                                                        |
| ---------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `lag-kernelization`                | Add a small modality-lag kernel over recent proprioception/vision states.                | Should reduce failure only when lag order is preserved; shuffle lag kills.                         |
| `recoverability-gated-fusion`      | Run a recoverability gate before any fusion router.                                      | If leave-one-out recovery matrix is near zero, block reliability-reweighting as main intervention. |
| `dependency-bounded-assembly`      | Fuse only modality decisions with low conditional-dependency conflict.                   | Conditional MI/remask sensitivity predicts which joint commits fail.                               |
| `factor-message-localization`      | Represent language, vision, proprioception, contact, and task constraints as factors.    | Local factor residual identifies the failing modality/constraint better than scalar confidence.    |
| `flux-balance-localization`        | Track evidence/constraint flow from modalities into action decisions.                    | Failures show source–sink imbalance; ordinary attention weights do not.                            |
| `multiscale-residual-coarsening`   | Coarse task belief first, fine action fusion second.                                     | Coarse residual pass removes global task failures that fine fusion cannot.                         |
| `polarization-partitioning`        | Polarize modality features into reliable/frozen vs uncertain/defer channels.             | Reliability entropy becomes more bimodal; if not, kill.                                            |
| `barrier-certificate-localization` | Add hard safety/feasibility barrier after fused action.                                  | High-confidence fused actions violating barrier are rejected and reduce unsafe failures.           |
| `observable-lifting`               | Learn lifted linear dynamics over fused VLA hidden state.                                | Lifted spectrum predicts rollout failures better than raw hidden confidence.                       |
| `operator-lifting`                 | Learn scene-function → affordance-function operator.                                     | Holds across unseen scene layouts/resolutions; point predictor fails.                              |
| `affordance-fielding`              | Produce 3D actionability/constraint field instead of a text plan or action vector.       | Field predicts valid contact points under perturbation before policy training.                     |
| `correspondence-fielding`          | Use vision-language-proprioception correspondence field for pick/place/action alignment. | Equivariance and multi-site recall beat direct action regression.                                  |
| `object-slotting`                  | Bind each modality to persistent object slots.                                           | Slot drops/swaps cause localized changes; global fusion collapses nonlocally.                      |
| `belief-sufficiency`               | Maintain uncertainty-bearing task belief over hidden object/contact state.               | Belief entropy predicts information-gathering value and failure.                                   |
| `gap-contextification`             | Infer embodiment/environment context online.                                             | Short-history context clusters shift and improves adaptation; static robust model does not.        |
| `ensemble-measure-lifting`         | Use small ensemble of fused beliefs/actions.                                             | Spread correlates with OOD/failure; if not, kill.                                                  |
| `collective-variable-compression`  | Extract slow skill/contact variables from trajectories.                                  | Failure boundaries align with slow variables better than raw features.                             |
| `transport-coupling`               | Use OT coupling between language goals, object slots, and action segments.               | Coupling exposes unmatched mass/alignment holes; cosine does not.                                  |
| `implicit-boundary-fielding`       | Represent contact/no-go/object boundary as SDF/level set.                                | Topology/contact perturbations remain differentiable; boxes/masks break.                           |
| `trajectory-chunking`              | Predict short coherent action chunks conditioned on fused belief.                        | There is a chunk length that lowers jitter without hurting feedback.                               |
| `path-straightening`               | Straighten latent action refinement path.                                                | Low-step rollout degrades less when curvature is lower.                                            |
| `manifold-intrinsicization`        | Put 6-DoF actions and object relations on SE(3)/equivariant fields.                      | Rotation/frame OOD error drops; Euclidean head has discontinuities.                                |

The key validator result is that the seed failure does **not** say “build a better reliability router.” It says: first test recoverability. If recoverability is absent, the model needs a conjunctive/synergy object—belief, factor graph, object-slot field, or affordance field—not a reweighting object.

---

# ARCHIVE / KILL list

The earlier bank already marked several useful but not-yet-broad-enough candidates as ARCHIVE and rejected pseudo-operators whose deletion test fails. I keep that posture but make the reasons sharper. 

## ARCHIVE

| item                                    | reason                                                                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `prediction-setification`               | Good cheap probe, but current evidence is mostly conformal prediction; not enough cross-domain object-shift reuse yet.   |
| `concept-bottlenecking`                 | Strong for interpretability/intervention, but still too concentrated in CBM/medical-style episodes for this bank.        |
| `soft-target-distillation`              | Important supervision-object shift, but narrower than a reusable modeling-object operator here.                          |
| `low-rank-deltaization`                 | Powerful PEFT move, but currently more parameter-adaptation than general object-shift operator.                          |
| `prompt-conditioning-externalization`   | Useful interface move, but differential predictions depend heavily on base-model API.                                    |
| `executable-specification-codification` | Eureka/code-as-reward is promising, but evidence is still concentrated in reward/program ecosystems.                     |
| `worst-groupization`                    | Practical robustness tool, but mostly objective reweighting; keep as neighbor of invariantization, not independent KEEP. |
| `action-tokenization`                   | Boundary case: sometimes useful, but unless tokenization creates a new measurable object, it fails the deletion test.    |

## KILL

| pseudo_operator                                  | one-line reason                                                                                             |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `tokenization`                                   | Deleting “token” usually deletes no prediction; it is often an interface, not an object shift.              |
| `bigger-backbone`                                | More capacity does not specify a simpler object or a new discriminator.                                     |
| `bigger-data-scaling`                            | Better coverage is not a modeling-object shift.                                                             |
| `module-adding`                                  | “Add memory/graph/adapter” is not an operator unless memory/graph/adapter carries a falsifiable new object. |
| `carrier-name-dropping`                          | “Use OT / causality / diffusion / graph / energy” names a carrier, not a move.                              |
| `multimodal-concatenation`                       | Concatenation has no recoverability, conflict, or sufficiency object.                                       |
| `reliability-reweighting-without-recoverability` | Seed anomaly kills it: if recoverable_fraction ≈ 0, there is no redundant modality to reweight toward.      |
| `longer-context-as-memory`                       | Seed anomaly kills it: context length alone did not remove the lag residue; only explicit lag did.          |
| `attention-as-explanation`                       | Attention only counts if it supports an intervention, correspondence, dependency, or message object.        |
| `benchmarkization`                               | A benchmark exposes failure signatures but does not itself generate a modeling move.                        |

[1]: https://arxiv.org/html/2604.20453v1?utm_source=chatgpt.com "Significance and Limitations of the Projection Operator ..."
[2]: https://arxiv.org/html/2603.12996v1?utm_source=chatgpt.com "Dependency-Aware Parallel Decoding via Attention for ..."
[3]: https://ieeexplore.ieee.org/document/910572/?utm_source=chatgpt.com "Factor graphs and the sum-product algorithm"
[4]: https://arxiv.org/abs/0807.3917?utm_source=chatgpt.com "Channel polarization: A method for constructing capacity-achieving codes for symmetric binary-input memoryless channels"
[5]: https://ieeexplore.ieee.org/document/7782377?utm_source=chatgpt.com "Control Barrier Function Based Quadratic Programs for ..."
[6]: https://arxiv.org/abs/1408.4408?utm_source=chatgpt.com "A Data-Driven Approximation of the Koopman Operator"
[7]: https://arxiv.org/abs/1910.03193?utm_source=chatgpt.com "DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators"
[8]: https://arxiv.org/abs/2307.05973?utm_source=chatgpt.com "VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models"
[9]: https://arxiv.org/abs/2010.14406?utm_source=chatgpt.com "Rearranging the Visual World for Robotic Manipulation"
[10]: https://arxiv.org/abs/2107.04034?utm_source=chatgpt.com "RMA: Rapid Motor Adaptation for Legged Robots"
[11]: https://www.pnas.org/doi/10.1073/pnas.202427399?utm_source=chatgpt.com "Escaping free-energy minima"
[12]: https://arxiv.org/abs/2210.02747?utm_source=chatgpt.com "Flow Matching for Generative Modeling"
