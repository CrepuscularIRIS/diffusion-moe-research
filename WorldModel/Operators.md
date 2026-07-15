# World-Model Operator Bank Audit (Independent Research-Methodology Audit, cutoff July 2026)

## TL;DR
- About half of the multimodal-derived operator bank transfers to world models; the strongest WM-native operators are belief-ization, context-ization, and residual-ization, while recoverability-gated-fusion and bits-back-refund-pricing are largely multimodal/VLA-biased and must be demoted to WM-CONDITIONAL or archived.
- The highest-value NEW operators discovered are model-exploitability-ization, policy-ranking-preservation, occupancy-weighted-accuracy, and failure-boundary modeling — each passes the object-shift and differential-prediction gates and is testable on DMC/Meta-World with two 48GB GPUs.
- The single primary research direction under the given hardware is model-exploitability-ization tested on TD-MPC2 (324 checkpoints publicly released), because it makes a decision-relevant differential prediction, has a cheap frozen-checkpoint probe, and routes cleanly to an AAAI-style compact paper.

## Key Findings
The 2025–2026 WM state of the art has bifurcated. On one branch, decoder-free latent MBRL (R2-Dreamer, ICLR 2026; NE-Dreamer, 2026; TD-MPC2, ICLR 2024) shows that representation objectives, not reconstruction, drive control. On the other, large video/generative world models (Dreamer 4, arXiv 2509.24527, Sept 2025; Genie 3; NVIDIA Cosmos) achieve high visual fidelity but weak decision utility — a gap now measured directly by closed-loop benchmarks (World-in-World, arXiv 2510.18135, Oct 2025; WorldModelBench, NeurIPS 2025; WorldArena, arXiv 2602.08971, Feb 2026). WorldArena quantifies this over 14 representative models: perceptual realism shows only "a weak correlation with action planning performance (r = 0.360)," and "high visual fidelity remains insufficient to provide strong predictive or decision-relevant signals for complex embodied reasoning." WorldModelBench similarly reveals "systematic failures, such as violations of gravity or mass conservation, that remain invisible to standard visual metrics," with "FID or FVD correlate[ing] weakly with downstream planning or control performance." This reframes almost every candidate operator around a decision-utility differential rather than a prediction-loss differential — the organizing principle of this audit.

## Details

### (A) Executive summary of bank transfer
An operator bank originally derived from multimodal/VLA models transfers only partially. Operators that name a modeling object already central to sequential decision-making under partial observability — belief-ization, context-ization, latent-variable-ization, residual-ization, distribution-output-ization — are WM-NATIVE or WM-ADAPTABLE. Operators whose motivating complexity is redundant multi-source sensing (recoverability-gated-fusion, some forms of coverage-set-ization) are multimodal-biased: in single-camera DMC/Meta-World there are no genuinely redundant or conflicting sources, so they survive only as WM-CONDITIONAL. Operators that are actually implementation families (graph-ization, object-slot-ization when reduced to "add slots") risk collapsing into anti-patterns unless they carry a persistence/differential test. Net effect: the bank should SHRINK — kill 1, archive 2, merge 3 pairs, and promote 6 new precise, killable operators.

### (B) World-model failure-signature map (20 signatures)
1. **Strong one-step, poor long-horizon rollout** — symptom: 1-step MSE low, k-step diverges. Explanations: (i) exposure bias / teacher-forcing–autoregressive mismatch; (ii) genuinely multimodal futures collapsed to a mean. Diagnostic: compare teacher-forced vs free-running rollout error curves; inject scheduled sampling. Metrics: k-step latent error, imagined return. Operators: memory-kernel-closure, residual-ization, horizon-adaptive. Literature: partially addressed (Self Forcing, AR Forcing 2025–2026).
2. **Strong teacher-forced, weak policy-induced rollout** — Explanations: (i) occupancy/distribution shift; (ii) model exploitability. Diagnostic: model error under on-policy vs behavior occupancy. Operators: occupancy-weighted-accuracy, model-exploitability-ization. Literature: addressed conceptually (objective-mismatch survey 2023; edge-of-reach, NeurIPS 2024).
3. **Good visual quality, poor action-conditioned fidelity** — Diagnostic: counterfactual-action queries; action-swap tests. Operators: counterfactual-action-fidelity, operator-lifting. Literature: strongly flagged (World-in-World, WorldModelBench, WorldArena).
4. **Accurate dynamics, poor planning** — Explanations: (i) value/reward mismatch; (ii) planner exploits model. Diagnostic: oracle-reward substitution; policy-ranking probe. Operators: policy-ranking-preservation, error-budget-allocation.
5. **Accurate state, wrong reward/termination** — Diagnostic: oracle reward/termination replacement. Operators: oracle-factorization (diagnostic), distribution-output-ization on reward.
6. **In-distribution control collapses under changed mass/friction/gravity/delay** — Diagnostic: oracle-context conditioning vs learned inference (CARL). Operators: context-ization, transition-family-modeling, invariant-ization. Literature: DALI (NeurIPS 2025), Dreaming of Many Worlds (RLC 2024).
7. **Strong average return, rare catastrophic failure** — Diagnostic: risk-sensitive rollout, failure-boundary probe. Operators: failure-boundary-modeling, barrier-certificate-localization, distribution-output-ization.
8. **Ensemble disagreement uncorrelated with actual error** — Diagnostic: reliability-diagram/calibration; conformal coverage. Operators: coverage-set-ization (conformal), information-bottleneck.
9. **Longer history gives diminishing returns** — Diagnostic: memory-length sweep; Mori–Zwanzig kernel truncation. Operators: memory-kernel-closure.
10. **Model-free beats planning with learned model** — Diagnostic: value-equivalence probe; policy-ranking correlation. Operators: policy-ranking-preservation, model-exploitability.
11. **Planner improves model return but reduces real return** (classic exploitability) — Diagnostic: real-vs-imagined return gap under optimized plan. Operators: model-exploitability-ization. Literature: MOPO/MOReL/COMBO; edge-of-reach (NeurIPS 2024).
12. **Increasing rollout horizon abruptly damages performance** — Diagnostic: horizon sweep with error-budget accounting. Operators: horizon-adaptive-modeling, error-budget-allocation.
13. **Pixel reconstruction improves but control does not** — Diagnostic: decoder-free swap (R2-Dreamer). Operators: information-bottleneck, observable-lifting. Literature: strongly addressed (R2-Dreamer, NE-Dreamer 2026).
14. **Object identity drifts under occlusion/rearrangement** — Diagnostic: persistence/tracking probe across occlusion. Operators: object-slot-ization (with persistence test), particle-measure-ization.
15. **Model fails when object count changes** — Diagnostic: vary N objects at test. Operators: object-slot-ization, graph-ization.
16. **Different tasks require full retraining** — Diagnostic: context-inference probe; skill reuse. Operators: context-ization, skill-option-ization, transition-family.
17. **Fast local predictions correct but global task progress wrong** — Diagnostic: collective-variable / reward-to-go probe. Operators: collective-variable-ization, multiscale-correction-hierarchy.
18. **Physical quantities drift despite low local error** — Diagnostic: conserved-quantity monitor over rollout. Operators: conservation-structure-ization.
19. **Context labels solve OOD but learned context inference fails** — Diagnostic: oracle-context vs inferred-context return gap. Operators: context-ization (online inferability requirement). Literature: DALI.
20. **Multimodal reliability weighting fails to rescue missing/corrupted sources** — Diagnostic: controlled corruption/dropout of a source. Operators: recoverability-gated-fusion (WM-CONDITIONAL).

### (C) Existing-bank corrosion table (status per operator)
- **belief-ization** — WM-NATIVE. Object: hidden vector → posterior over latent state with uncertainty used in planning. Closest WM lit: RSSM stochastic latent, POMDP belief planning (BetaZero, DualSMC). Duplication risk vs latent-variable-ization: HIGH — resolved below.
- **context-ization** — WM-ADAPTABLE (→ WM-NATIVE if online-inferable). Object: task-ID → online-inferred latent context governing transition/reward. Closest: DALI (2025), Dreaming of Many Worlds (2024). Requires online inferability + rapid adaptation, not mere task-ID.
- **memory-kernel-closure** — WM-CONDITIONAL. Object: Markov latent → non-Markovian generalized-Langevin closure with explicit memory kernel. Test: must predict something a generic RSSM does not (calibrated memory length under coarse-graining).
- **particle-measure-ization** — WM-CONDITIONAL. Requires particles to actively influence inference/planning (DualSMC-style); else KILL.
- **residual-ization** — WM-ADAPTABLE. Requires a semantically meaningful base model (analytic sim, Koopman linear model); else KILL.
- **observable-lifting** — WM-ADAPTABLE. Object: raw state → lifted observables with (near-)linear dynamics (Koopman/EDMD).
- **multiscale-correction-hierarchy** — WM-CONDITIONAL. Requires scale-specific error correction, not just multi-timescale features.
- **conservation-structure-ization** — WM-CONDITIONAL. Requires invariant prediction, not just a physics loss.
- **collective-variable-ization** — WM-ADAPTABLE. Object: full state → slow collective variables governing task progress.
- **invariant-ization** — WM-ADAPTABLE (causal invariant prediction across contexts).
- **distribution-output-ization** — WM-NATIVE (already in DreamerV3 twohot/symlog reward and continue heads).
- **coverage-set-ization** — META/EVALUATION → WM-ADAPTABLE via conformal rollout sets.
- **latent-variable-ization** — WM-NATIVE but MERGE-adjacent with belief-ization.
- **information-bottleneck-ization** — WM-NATIVE (R2-Dreamer is explicitly a tractable surrogate for an extended Sequential Information Bottleneck objective).
- **graph-ization** — SPLIT (architecture family vs relational-structure operator).
- **object-slot-ization** — WM-CONDITIONAL (requires persistence test).
- **factor-graph-ization** — MERGE with graph-ization/object-slot.
- **skill-option-ization** — WM-ADAPTABLE.
- **chunk-ization** — WM-ADAPTABLE (action chunking; scalable offline MBRL, 2025).
- **operator-lifting** — WM-ADAPTABLE (neural-operator/transition-operator over functions).
- **recoverability-gated-fusion** — WM-CONDITIONAL (needs genuinely redundant/conflicting sources).
- **barrier-certificate-localization** — WM-ADAPTABLE (safety/viability); merge representation into failure-boundary-modeling.
- **two-part-code-ization** — META/EVALUATION (MDL description-length diagnostic).
- **bits-back-refund-pricing** — ARCHIVE/KILL for WM (multimodal-coding-biased; no decision differential).

**Belief-ization vs latent-variable-ization: GENUINELY SEPARATE** only when the latent carries uncertainty consumed for information-gathering/planning. A deterministic RSSM `h_t` is latent-variable-ization without belief-ization; add posterior variance actually consulted by the planner (e.g., UCB gating in ELVIS, arXiv 2605.04709) and it becomes belief-ization. Recommendation: keep both, define belief-ization = latent-variable-ization + (uncertainty consumed by decision).

### (D) Promoted WM operator cards (abbreviated schema)

**model-exploitability-ization** — status WM-NATIVE (new). Core move: model the worst-case error the optimizing policy/planner can find, not average error. Old object: expected transition error under data distribution. New object: policy-conditioned/occupancy-weighted discrepancy or pessimistic uncertainty set. WM component: uncertainty model + transition model + planner. Regime: state or pixel, offline/online, planning-based. Frame: robust MDP / two-player model-policy game. Simplification: relocates error accounting from data occupancy to policy-reachable occupancy. Differential prediction: the imagined-vs-real return gap grows with planner strength even when held-out 1-step error is flat. Cheap probe: on a frozen TD-MPC2 checkpoint, measure imagined return of the MPPI-optimal plan vs executed real return, sweeping planner iterations/samples. Oracle/intervention: replace learned model with simulator for the same plan (this is exactly the edge-of-reach diagnostic — Sims, Lu & Teh, NeurIPS 2024, arXiv:2402.12527, show "if the learned dynamics model is replaced by the true error-free dynamics, existing model-based methods completely fail," motivating their Reach-Aware Value Learning). Failure signatures: #11, #2, #10. Closed-loop readout: real return under increasingly optimized plans. Kill criterion: kill if the imagined-real gap does not increase with planner budget — threshold <5% gap growth from 6→24 MPPI iterations. Closest existing operator: coverage-set-ization/pessimism. Dedup defense: unlike generic uncertainty penalties it predicts a planner-budget-dependent gap. Sources: MOPO/MOReL/COMBO; edge-of-reach; objective-mismatch survey (2023). Repos: TD-MPC2 (planner decoupled → frozen probe possible), DreamerV3. Compute: one GPU, hours. AAAI fit: strong. Info Sciences fit: plausible. Info Fusion fit: scope-mismatch.

**policy-ranking-preservation** — status WM-NATIVE (new). Core move: train/evaluate the model to preserve the ORDERING of actions/plans/policies by value, not to predict states. Old object: next-state prediction. New object: order-isomorphism between imagined and real returns. WM component: value model / evaluation protocol / transition model. Differential prediction: two models with identical 1-step error can differ in Kendall-τ between imagined and real plan rankings. Cheap probe: on frozen TD-MPC2/DreamerV3, sample K plans, correlate imagined vs real returns (Kendall-τ). Oracle: simulator returns as ground-truth ranking. Failure signatures: #4, #10. Kill criterion: kill if ranking-τ tracks 1-step error monotonically (no separation) — then redundant with prediction loss. Closest existing operator: value-equivalent models / decision-aware model learning; distinct because it targets ordinal, not cardinal, value. Related 2025–2026 work: ESNR / "Towards Policy-Aware World Models"; dWorldEval (policy ranking via discrete diffusion WM). Repos: all three. Compute: one GPU. AAAI fit: strong. Info Sciences fit: strong.

**context-ization (online-inferable)** — status WM-NATIVE. Core move: infer a latent context governing dynamics/reward from interaction history, online, and adapt rapidly. Old object: single stationary transition. New object: history-conditioned transition family with an inferred context variable. WM component: context estimator + action-conditioned dynamics. Differential prediction: counterfactual consistency — DALI (NeurIPS 2025, arXiv:2508.20294, v3 dated 15 Jan 2026) shows "perturbing a dimension encoding gravity... results in imagined rollouts where objects fall faster or slower," and reports "+96.4% gains over context-unaware baselines, often surpassing ground-truth context-aware baselines in extrapolation tasks." Cheap probe: CARL-DMC train on subset of contexts, test extrapolation; compare oracle-context vs inferred-context return. Oracle: privileged context injection. Failure signatures: #6, #16, #19. Kill criterion: kill if oracle context improves normalized return <2% (no headroom) OR if inferred context cannot close >50% of the oracle gap. Sources: DALI; Dreaming of Many Worlds (RLC 2024). Repos: DreamerV3 (DALI built on it). Compute: two GPUs, ~1–2 days. AAAI fit: strong. Info Sciences fit: strong. Info Fusion fit: plausible only if fusing multiple context sources.

**occupancy-weighted-accuracy** — status WM-ADAPTABLE (new). Core move: weight model accuracy by current/future reachable visitation, not uniform data. Old object: uniform prediction loss. New object: occupancy-reweighted loss / truncated rollouts anchored to reachable set. Differential prediction: model with lower uniform error but worse on-occupancy error yields worse policy. Cheap probe: reweight held-out error by policy occupancy; correlate with return. Failure signature: #2. Closest: MBPO truncation / policy-aware model learning. Dedup: must show reweighting changes the mediating object (loss target), not just a schedule. Kill criterion: kill if occupancy reweighting does not change model ranking vs uniform. Repos: DreamerV3, TD-MPC2. AAAI fit: plausible. Info Sciences fit: plausible.

**failure-boundary-modeling** — status WM-ADAPTABLE (new). Core move: model the boundary separating recoverable from irreversible states. Old object: reward/return prediction. New object: viability/reachability certificate (recoverable-set indicator). WM component: continuation model / value model / uncertainty model. Differential prediction: distinguishes rare catastrophic tail from low-return-but-recoverable states; average return does not. Cheap probe: label episodes by irreversibility in Meta-World/Crafter; probe whether latent linearly separates recoverable vs not. Oracle: simulator reset to test recoverability. Failure signature: #7. Closest: barrier-certificate-localization, reachability certificates (2022–2026), CBFs. Dedup: failure-boundary is the object; barrier-certificate is one representation of it. Kill criterion: kill if recoverable/irreversible states are already linearly separable in a vanilla DreamerV3 latent (>0.8 AUC would kill novelty). Repos: DreamerV3, TD-MPC2. AAAI fit: plausible. Info Sciences fit: strong.

**memory-kernel-closure** — status WM-CONDITIONAL. Core move: replace Markov latent transition with an explicit finite-memory (Mori–Zwanzig/GLE) closure. Old object: Markov RSSM step. New object: non-Markovian autoregressive closure with learned memory operators + truncation length K. Differential prediction vs generic RSSM: predicts a calibrated memory length K at which added history stops helping (a Mori–Zwanzig-specific observable) and improved stability under coarse-grained/partial observation. Cheap probe: on Memory Maze / partial-observation DMC, sweep memory length vs RSSM `deter` size; test if a kernel-truncation curve exists that RSSM lacks. Failure signatures: #9, #1. Kill criterion: kill if a size-matched RSSM matches the closure at all memory lengths (the key saturation risk). Sources: data-driven Mori–Zwanzig (SIAM J. Appl. Dyn. Syst.); neural closure models (2020–2026). AAAI fit: plausible. Info Sciences fit: strong (dynamical-systems venue).

### (E) Newly discovered candidates
- **Promoted**: model-exploitability-ization; policy-ranking-preservation; occupancy-weighted-accuracy; failure-boundary-modeling; transition-family-modeling (distinct latent operator over transition functions); horizon-adaptive-modeling (as adaptive-computation policy, not schedule knob).
- **Archive**: two-part-code-ization (diagnostic only); coverage-set-ization as standalone (fold into conformal-rollout evaluation).
- **Killed**: bits-back-refund-pricing (no WM decision differential).
- **Merged**: belief-ization ⊇ latent-variable-ization + uncertainty-consumed; factor-graph-ization → graph-ization; barrier-certificate-localization → failure-boundary-modeling representation.
- **Unresolved** (insufficient evidence): re-anchoring/latent-reset as a general operator (may reduce to filtering/test-time adaptation); operator-lifting/neural-operator transition models for control decision utility.

### (F) Deduplication map
- belief-ization ≈ latent-variable-ization + particle-measure-ization when uncertainty is consumed by the planner; keep belief-ization as superset, particle-measure as one implementation restricted to when particles influence inference.
- context-ization ≈ transition-family-modeling ≈ hidden-parameter MDP: context-ization infers a point/posterior context; transition-family models a distribution/operator over transition functions; keep both, distinguished by object (context variable vs operator over functions).
- model-exploitability-ization ⊂ occupancy-weighted-accuracy family (both re-weight by policy-reachable occupancy); exploitability is the adversarial/worst-case corner, occupancy-weighting the expectation corner.
- failure-boundary-modeling ≈ barrier-certificate-localization ≈ reachability/viability; merge representations under one object.
- residual-ization ≈ multiscale-correction-hierarchy when residual is applied per scale.
- information-bottleneck-ization ≈ R2-Dreamer's redundancy-reduction (both compress task-irrelevant info).

### (G) Anti-pattern additions (WM-specific pseudo-operators to reject)
"just increase imagination horizon" (fails; horizon has a cliff, #12); "add a reconstruction decoder" (R2-Dreamer shows removing it helps and trains 1.59× faster than DreamerV3); "add an uncertainty head" (fails unless uncertainty is consumed by decision and calibrated, #8); "use a larger latent"; "use Transformer dynamics" (architecture, not operator); "train on more environments" (data knob); "add object slots without persistence tests" (#14); "physics-informed loss without invariant prediction" (#18); "multi-timescale features without scale-specific error correction" (#17). Each is rejected by Gate10.

### (H) Repository implementation table (verified via official repos + code wikis; unverified items flagged)

**DreamerV3** (github.com/danijar/dreamerv3, JAX):
- World model incl. RSSM/heads: `dreamerv3/agent.py`, class `WorldModel`; actor-critic + imagination: class `ImagActorCritic`. NN blocks (encoder/decoder/RSSM cell/heads) in `dreamerv3/nets.py` (exact class names within `nets.py` UNVERIFIED). Config `dreamerv3/configs.yaml`. RSSM defaults verified: `deter: 8192, stoch: 32, classes: 64, free_nats: 1.0`. Imagination horizon H=15 and loss scales (β_pred 1.0, β_dyn 0.5, β_rep 0.1) are standard values; literal YAML key spellings UNVERIFIED. Modify transition → full retraining. No pretrained weights released (only score logs). Frozen-checkpoint probe only if you train your own.
- Component to modify for exploitability/ranking probes: `ImagActorCritic` imagination loop (read-only) + reward/continue heads in `WorldModel`.

**TD-MPC2** (github.com/nicklashansen/tdmpc2, PyTorch):
- Agent: `tdmpc2/tdmpc2.py`, class `TDMPC2`; implicit world model (encode/next/reward/Q/pi): `tdmpc2/common/world_model.py`, class `WorldModel`; SimNorm/NormedLinear/Ensemble/enc in `tdmpc2/common/layers.py`; MPPI planner in `TDMPC2.plan()` with `_estimate_value()`. Planning defaults confirmed verbatim (Hansen et al., ICLR 2024): "Samples num_pi_trajs = 24 trajectories... Sample num_samples = 512 action sequences... Roll out each trajectory... for horizon = 3 steps... Select num_elites = 64 best trajectories... softmax-weighted (temperature = 0.5)." Decoder-free, latent MPC. Checkpoints: tdmpc2.com/models states "We open-source a total of 324 TD-MPC2 model checkpoints, including 12 multi-task models (ranging from 1M to 317M parameters)," with 312 single-task checkpoints across 104 tasks in 4 domains → frozen-checkpoint probes fully supported; planner modifiable without retraining; dynamics modification requires retraining. `common/buffer.py` and trainer class names lightly verified.
- Best repo for the primary experiment because the planner is decoupled and checkpoints exist.

**R2-Dreamer** (github.com/NM512/r2dreamer, PyTorch, ICLR 2026):
- RSSM: `rssm.py`; networks incl. projector head: `networks.py`; world-model+behavior orchestration and rep-loss selection: `dreamer.py`; config flag `model.rep_loss ∈ {r2dreamer, dreamer, infonce, dreamerpro}` (verified verbatim from README). Benchmarks: dmc(proprio/vision/subtle), atari100k, crafter, metaworld, memorymaze. No checkpoints released. Modify transition → full retraining. Internal class names UNVERIFIED.
- Best repo for information-bottleneck / representation-object experiments (rep_loss swap is a clean single-flag intervention).

Confounders across all: reward/return scale normalization (symlog / TD-MPC2 `RunningScale`) can mask model-error effects; replay-buffer staleness conflates occupancy shift; seed variance on DMC is high (report ≥5 seeds).

### (I) Two-GPU generation-test plan for top operators (hardware: 2×~48GB, no cluster)
1. **model-exploitability-ization (primary)**. Week-1 probe: frozen TD-MPC2 checkpoints, measure imagined-vs-real return gap vs MPPI iterations/samples on 5 DMC tasks (read-only, hours). Minimal experiment: add occupancy/pessimism-weighted model loss to TD-MPC2 training on 6 DMC + 3 Meta-World tasks, 5 seeds. Stopping rule: proceed only if the frozen probe shows gap grows ≥5% from 6→24 iterations. Expansion: DMC-GB2 distractors and CARL context shifts.
2. **context-ization (online-inferable)**. Week-1 probe: reproduce DALI oracle-vs-inferred gap on CARL-DMC Walker (gravity, actuator strength). Minimal: DreamerV3 + context encoder, extrapolation split, 5 seeds. Stopping rule: oracle context must give ≥2% normalized return; kill otherwise. Expansion: multi-context inference.
3. **policy-ranking-preservation**. Week-1 probe: frozen TD-MPC2/DreamerV3, Kendall-τ of imagined vs simulator returns over K=64 plans. Minimal: add a ranking-consistency auxiliary loss; test τ improvement and closed-loop return. Stopping rule: proceed only if τ separates from 1-step error across two checkpoints.
4. **failure-boundary-modeling**. Week-1 probe: linear-probe recoverable vs irreversible states in frozen DreamerV3 latents on Crafter/Meta-World. Minimal: viability-indicator head + risk-aware planning. Stopping rule: proceed only if the vanilla latent does NOT already linearly separate (>0.8 AUC would kill novelty).
All four reject large-scale video pretraining and fit two 48GB GPUs.

### (J) Publication routing
- **AAAI-style compact algorithmic route (strongest)**: model-exploitability-ization or policy-ranking-preservation — single clean algorithmic change, cheap frozen-checkpoint evidence, DMC/Meta-World benchmarks. Venue fit: **strong**.
- **Information Sciences route (strongest)**: memory-kernel-closure or failure-boundary-modeling — dynamical-systems / uncertainty framing, richer theory. Venue fit: **strong**.
- **Information Fusion route**: ONLY genuine if fusing multiple information sources whose reliability/conflict is explicitly modeled — e.g., fusing multiple model members + multiple timescales + epistemic/aleatoric channels with reliability routing (covariance-intersection / Dempster-Shafer style). context-ization with multi-source context inference or ensemble-fusion could qualify; a single latent with multiple heads does NOT. Venue fit: **plausible only under genuine multi-source scope; otherwise scope-mismatch**.

### (K) Final operator bank retrieval index
| Operator | Failure signature | Core move | WM status | Generation-test status |
|---|---|---|---|---|
| belief-ization | POMDP/uncertainty ignored | posterior consumed by planner | WM-NATIVE | probe-ready |
| context-ization | OOD dynamics shift (#6/#19) | online-infer latent context | WM-NATIVE | DALI-validated |
| model-exploitability-ization | planner beats real (#11) | worst-case policy-reachable error | WM-NATIVE (new) | frozen-probe-ready |
| policy-ranking-preservation | MF>planning (#10) | preserve value ordering | WM-NATIVE (new) | frozen-probe-ready |
| occupancy-weighted-accuracy | on-policy rollout weak (#2) | reachable-visitation-weighted loss | WM-ADAPTABLE (new) | probe-ready |
| failure-boundary-modeling | rare catastrophe (#7) | recoverable/irreversible boundary | WM-ADAPTABLE (new) | probe-ready |
| memory-kernel-closure | history plateaus (#9) | non-Markov GLE closure | WM-CONDITIONAL | saturation-risk |
| residual-ization | drift over base (#1) | correction on semantic base | WM-ADAPTABLE | needs base model |
| information-bottleneck-ization | recon≠control (#13) | compress task-irrelevant | WM-NATIVE | R2-Dreamer rep_loss swap |
| object-slot-ization | identity drift (#14/#15) | persistent object tokens | WM-CONDITIONAL | needs persistence test |
| distribution-output-ization | wrong reward tail (#5) | full predictive distribution | WM-NATIVE | in DreamerV3 |
| horizon-adaptive-modeling | horizon cliff (#12) | uncertainty-gated rollout length | WM-CONDITIONAL | ELVIS-style probe |
| recoverability-gated-fusion | fusion fails (#20) | reliability-routed sources | WM-CONDITIONAL | needs redundant sources |

## Answers to the 15 questions
1. **Most natively aligned**: belief-ization (RSSM stochastic latent is already a belief-state approximation; but only counts as belief-ization when uncertainty is consumed by decision).
2. **Most multimodal/VLA-biased**: recoverability-gated-fusion (assumes genuinely redundant/conflicting sources absent in single-camera control).
3. **Demote first**: bits-back-refund-pricing (no WM decision differential) → ARCHIVE/KILL.
4. **Merge two**: belief-ization + latent-variable-ization (into belief-ization = latent + uncertainty-consumed).
5. **Strongest low-compute AAAI**: model-exploitability-ization (frozen-checkpoint probe on the 324 released TD-MPC2 weights).
6. **Strongest Information Sciences**: memory-kernel-closure (Mori–Zwanzig dynamical-systems framing); failure-boundary-modeling a close second.
7. **Genuine Information Fusion?** Only under genuine multi-source scope (multi-model + multi-timescale + epistemic/aleatoric with reliability routing); a single latent with multiple heads is scope inflation. Verdict: **plausible but narrow — do not force it.**
8. **Most important missing operator**: model-exploitability-ization (directly targets the dominant closed-loop failure #11).
9. **Highest risk of being a renamed existing method**: occupancy-weighted-accuracy (overlaps MBPO truncation / policy-aware model learning) — must show a changed mediating object.
10. **Three cheap probes before any full reproduction**: (a) frozen-checkpoint imagined-vs-real return gap vs planner budget (exploitability); (b) Kendall-τ plan ranking imagined vs simulator (policy-ranking); (c) oracle-context vs inferred-context return gap (context-ization).
11. **Oracle intervention that most efficiently localizes a WM bottleneck**: component replacement / oracle-factorization — swap oracle state, transition, reward, termination one at a time and read the return recovered by each (this is precisely the edge-of-reach diagnostic that exposed model-based collapse under a true dynamics model).
12. **Testable on a frozen checkpoint**: model-exploitability-ization and policy-ranking-preservation (TD-MPC2's 324 released checkpoints).
13. **Most likely to fail the generation test**: memory-kernel-closure (a size-matched RSSM may match it — high saturation risk) and object-slot-ization (persistence may not help control).
14. **Primary direction under two 48GB GPUs**: model-exploitability-ization on TD-MPC2.
15. **Retain only as diagnostic/evaluation protocol**: oracle-factorization of world-model errors (and two-part-code-ization) — powerful probes, not deployable methods.

## Recommendations
1. **Start now** with the frozen-checkpoint exploitability probe on TD-MPC2 (324 released weights) — it is the cheapest decisive test and gates the entire primary direction. Benchmark that changes the plan: if the imagined-real gap does NOT grow with planner budget (<5% from 6→24 MPPI iterations), pivot to policy-ranking-preservation.
2. **In parallel** run the context-ization oracle-gap probe on CARL-DMC (DreamerV3/DALI). Threshold: oracle context <2% normalized-return improvement kills the direction.
3. **Use R2-Dreamer's `model.rep_loss` flag** as the controlled testbed for information-bottleneck claims (single-flag intervention, no confounds).
4. **Treat oracle-factorization** as your standing diagnostic harness for every operator, not a paper contribution.
5. **Route the winner to AAAI** (compact algorithmic) and the dynamical-systems operator (memory-kernel-closure / failure-boundary) to Information Sciences; pursue Information Fusion only if a genuine multi-source setup emerges.

## Caveats
- Some 2025–2026 arXiv IDs (R2-Dreamer 2603.18202, NE-Dreamer 2603.02765, Dreamer 4 2509.24527, DALI 2508.20294, WorldArena 2602.08971) follow the 2026 numbering scheme; treated as established where an official repo or venue (ICLR 2026, NeurIPS 2025, Nature 2025) corroborates.
- DreamerV3 imagination-horizon/loss-weight YAML key spellings and internal `nets.py` class names are UNVERIFIED (values are standard); TD-MPC2 `buffer.py`/trainer class names lightly verified; R2-Dreamer internal class names UNVERIFIED.
- Several adjacent-field operators (Mori–Zwanzig, Koopman, CBFs) are established in physics/control but their DECISION-UTILITY differential in WMs is INFERRED, not yet demonstrated — hence WM-CONDITIONAL status. This is a deliberate epistemic guardrail against importing mathematical sophistication without a measurable control differential.
- Claims about video-WM decision-utility gaps are ESTABLISHED by closed-loop benchmarks (World-in-World, WorldModelBench, WorldArena r=0.360 realism-vs-planning correlation); claims about specific operator headroom are HYPOTHESES to be tested by the probes above, not results.
- The edge-of-reach finding (learned-model methods collapse when given true dynamics) is the single most important corroboration for prioritizing exploitability/occupancy operators over pure prediction-accuracy operators.