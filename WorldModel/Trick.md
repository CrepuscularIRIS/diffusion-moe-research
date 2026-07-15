A few framing notes before the analysis itself. First, my knowledge is reliable up to roughly **January 2026**, so I can't cover the "up to July 2026" window fully, and I did not run live searches for this reply — everything below is from my knowledge base, with citations to primary papers as I remember them. Where I'm not fully certain of a paper's exact claim or a repo's current state, I mark it. If you enable web search / deep research, the biggest gaps to fill are 2025–2026 arXiv work on world-model evaluation and the exact identity of "R2-Dreamer," which I don't recognize as a canonical name — you may mean **R2I ("Recall to Imagine," Samsami et al., ICLR 2024)**, the S4-based Dreamer for memory tasks, or an internal/very recent variant. I'll treat it as a Dreamer-family RSSM/SSM model.

---

## 1. Executive summary

The world-model literature contains a rich but **scattered and non-standardized** set of oracle-style diagnostics. Almost none of your 20 families is entirely novel, but very few have been systematized, and several (residual-matched error injection, confidence-gated oracle queries, component-wise replacement matrices at evaluation time) exist only as fragments. The most robust findings across the literature that your panel should exploit:

1. **Prediction accuracy and control utility are decoupled.** "Objective mismatch" (Lambert et al., L4DC 2020) showed one-step likelihood correlates poorly with closed-loop return. The value-equivalence principle (Grimm et al., NeurIPS 2020) gives the theory: a model only needs to be correct on value-relevant functionals. Implication: pixel/PSNR/FVD diagnostics are weak; ranking- and value-based diagnostics are strong.
2. **Open-loop metrics do not predict closed-loop performance.** Demonstrated repeatedly: exposure bias / compounding errors (Ross & Bagnell; scheduled sampling, Bengio et al. 2015; Lambert & Pister, "Investigating Compounding Prediction Errors," 2022), and most sharply in driving, where Dauner et al. (CoRL 2023, "Parting with Misconceptions…") showed open-loop nuPlan metrics and closed-loop performance can anti-correlate. Your "teacher-forced vs closed-loop conversion gap" is a real, named phenomenon; measuring it is cheap and decisive.
3. **Privileged-state upper bounds are standard practice in adjacent fields but rarely used *diagnostically* in modern WM papers.** State-based SAC as an upper bound for pixel agents (DrQ, RAD, CURL papers all report it); Learning by Cheating (Chen et al., CoRL 2019); privileged teacher → student distillation (Lee et al., Science Robotics 2020; RMA, Kumar et al., RSS 2021); asymmetric actor-critic (Pinto et al., 2017). The teacher–student pipeline is exactly your "oracle → deployable" conversion, already validated.
4. **Uncertainty-penalized offline MBRL explicitly frames the true model error as the oracle.** MOPO (Yu et al., 2020) and MOReL (Kidambi et al., 2020) motivate learned penalties as proxies for the ideal (oracle) error; M2AC gates rollouts on estimated error. Oracle-uncertainty experiments exist but are underexploited in online Dreamer/TD-MPC-style systems.
5. **Harness bugs are a first-order effect.** "Deep RL that Matters" (Henderson et al.), "Implementation Matters" (Engstrom et al.), and Machado et al.'s ALE revisit (sticky actions, frame-skip semantics) justify your family 20 as step zero.

**Headline recommendations** (defended in §6–8): the single most informative cheap intervention is the **2×2 oracle-model/oracle-planner factorization combined with periodic ground-truth re-anchoring sweeps**; the easiest is the **teacher-forced vs closed-loop gap plus horizon ladder** (no simulator-state access needed); the most publication-novel is **residual-matched structured error injection**; the most dangerous/misleading is **naïve oracle latent injection into a policy trained on learned latents** (interface mismatch confound).

---

## 2. Terminology map for your seven-way distinction

| Your category | Established names in the literature |
|---|---|
| Diagnostic oracle intervention | Largely **non-standard**; fragments appear as "oracle ablation," "ground-truth baseline," "upper bound with true state." No unifying term. |
| Privileged-information upper bound | "Privileged information" (Vapnik's LUPI), "privileged agent" (Learning by Cheating), "state-based upper bound" (pixel RL), "asymmetric actor-critic" |
| Teacher–student training | "Privileged distillation," "teacher–student," "policy distillation," RMA's "base policy + adaptation module" |
| Deployable algorithm | — |
| Ordinary ablation | "Ablation study" (removes a component; oracle interventions *replace* with ground truth — worth stating explicitly in a paper, reviewers conflate them) |
| Causal evaluation-time intervention | Closest umbrella: "interventional evaluation," "counterfactual evaluation"; in interpretability, "activation patching / causal tracing" is the direct analogue and worth citing for framing |
| Harness sanity check | "Sanity checks," "environment validation," "reproducibility checklist" (NeurIPS checklist lineage; Machado et al. for ALE semantics) |

The activation-patching analogy is genuinely useful framing for a paper: your latent-injection experiments are causal mediation analysis on a world-model agent.

---

## 3. Status of the 20 intervention families in the literature

**(1) Oracle latent-state injection.** Partially established. The dominant published form is *training-time*: state-based agent as upper bound (ubiquitous in DrQ/RAD/CURL-era pixel RL; also DMC papers report state vs pixel gaps). Dreamer-specific eval-time injection (swap z_t for GT simulator state) is rare because the policy's input distribution is the learned latent — you must either (a) train a small policy head on GT state in imagination-free mode, or (b) learn a GT-state→latent encoder (a "re-encoder"), which reintroduces learning. A cleaner published relative: **probing** — decoding GT variables (agent position, object pose) from latents, done in the Memory Maze paper (Pasukonis et al.) and many representation-analysis works. Probing answers "is the information present?" without the interface confound; injection answers "is it used?". Do both. TD-MPC2 is friendlier here since its latent is decoder-free and the model can be retrained cheaply on GT state inputs.

**(2) Oracle transition replacement.** Established as "planning with the true/ground-truth dynamics." Wang et al.'s MBRL benchmark (2019) includes ground-truth-dynamics baselines; the MPC literature (PETS, Chua et al. 2018) implicitly gives the ceiling; MuZero-line work discusses true-model MCTS. Key published conclusion: a strong optimizer with a learned model **exploits model errors** ("model exploitation," Kurutach et al. 2018; adversarial-example view of planners), so condition (2) vs (1) differences can be inflated. In DMC, `physics.get_state()`/`set_state()` makes simulator-query dynamics feasible for MPPI-style planners (TD-MPC2) at modest cost; for Dreamer it breaks imagination's parallel rollout structure and is more invasive.

**(3) Oracle reward/value/termination.** Under-published as a *diagnostic*, but strongly motivated: DreamerV2/V3 ablations show continuation ("discount") prediction matters a lot in episodic tasks; the value-equivalence and objective-mismatch results imply reward/value errors can dominate even with good dynamics. In goal/navigation literature there is a direct precedent for your "oracle STOP": vision-language navigation papers routinely report **oracle success rate / oracle stopping** as an upper bound — that terminology transfers cleanly. This family is cheap in all three codebases (replace `reward_head`/`cont_head` outputs with simulator queries during imagination or during evaluation rollouts) and, in my assessment, **the most likely to produce a surprising result** (termination/reward errors silently capping performance).

**(4) Oracle observation/decoder factorization.** Fragmentary. The video-prediction community knows FVD/PSNR ≠ utility; DIAMOND (Alonso et al., NeurIPS 2024) argued visual fidelity of action-conditioned details matters for RL and that prior WMs dropped small task-relevant details (your family 10 concern); TD-MPC/TD-MPC2 and Dreamer's own "no-reconstruction" ablations show reconstruction is neither necessary nor sufficient. The clean 2×2 (latent-rollout × decoder) factorization you propose has, to my knowledge, **not been published as a systematic diagnostic** — modest novelty available.

**(5) Teacher-forced vs closed-loop.** Well established conceptually (exposure bias, DAgger, compounding errors; Lambert & Pister 2022 study compounding explicitly; driving open/closed-loop gap per Dauner et al.). What's missing in the WM literature: a standard **conversion-gap metric** reported per model. Cheap, requires no simulator internals, works on all architectures.

**(6) Temporal oracle pulses / re-anchoring.** Mostly non-standard as a diagnostic. Important observation: **Dreamer's RSSM already implements this machinery** — the posterior is an observation-conditioned correction of the prior; "open-loop" evaluation in Dreamer papers means rolling the prior without posterior updates. So "re-anchor every k steps" = "apply posterior every k steps," a ~20-line change in DreamerV3. The performance-vs-reset-frequency curve is, as far as I know, unpublished as a systematic result and directly feeds a deployable method (uncertainty-triggered re-anchoring / active sensing). This is one of my top picks. Related literature: observation dropout / "blind" rollouts, filtering theory (measurement updates), and event-triggered state estimation in control — cite the control literature for novelty positioning.

**(7) Component-wise replacement matrix.** Not published as such for modern WMs. Fragments exist (families 1–3 pieces). The matrix framing is your organizing novelty, but beware combinatorics and interface confounds (each oracle swap changes downstream input distributions; components co-adapted during training may fail with oracle inputs *for interface reasons, not competence reasons*). Mitigation: brief adapter fine-tuning of downstream heads per cell, with the adapter budget held constant — report both zero-shot and adapted numbers.

**(8) Oracle model × oracle planner 2×2.** The cleanest causal design in your list. Precedents: Wang et al. 2019 (true dynamics + learned planners); "Evaluating Model-Based Planning and Planner Amortization" (Byravan et al.) separates planner from model contributions; MCTS-with-true-model literature. The known asymmetry to expect: strong planners exploit learned models (cell 3 vs 1 can *underperform*), which itself is a diagnostic signal, not a confound, if you report it as exploitation.

**(9) Privileged context injection.** Well established under **hidden-parameter MDPs** (Doshi-Velez & Konidaris), **contextual MDPs** (Hallak et al.), the **CARL** benchmark (Benjamins et al., "Contextualize Me"), online system identification (**UP-OSI**, Yu et al., RSS 2017: universal policy with true params vs online-inferred params — precisely your oracle-context vs inferred-context comparison), **RMA** (Kumar et al., 2021), and meta-RL context inference (PEARL, VariBAD). The oracle→deployable conversion here is *already proven* (RMA), which cuts novelty for the method but strengthens it as a diagnostic with known follow-up. CARL is explicitly designed for hidden-vs-visible-context comparisons and fits your compute.

**(10) Oracle objects/relations.** Established in the object-centric literature: C-SWM (Kipf et al.), OP3, SlotFormer; SAVi uses first-frame GT hints; several works compare GT object state vs learned slots for downstream RL (e.g., Yoon et al., ICML 2023, on pre-trained object-centric representations for RL). DIAMOND's motivation (small task-relevant objects lost by latents) supports the hypothesis. OC-STORM-style models are the natural testbed. Partially saturated as a *representation* claim; less saturated as a *dynamics-vs-parsing* factorization (GT masks + learned interaction model vs learned masks + GT-ish interaction).

**(11) Oracle uncertainty / true-error access.** Motivated explicitly by MOPO/MOReL (true error as the ideal penalty), M2AC (error-gated rollouts), Plan2Explore (latent disagreement as the learned proxy). An eval-time experiment giving the planner the *true* one-step error (computable in sim) and measuring the gain over ensemble-disagreement proxies is cheap in TD-MPC2 and, to my knowledge, not reported systematically for online pixel WMs. Strong pick.

**(12) Confidence-gated oracle queries.** Non-standard in WM literature. Nearest neighbors: active perception, "asking for help" in navigation/VLN, learning-to-defer, selective prediction (risk–coverage curves — borrow that terminology from selective classification). The success-vs-query-budget curve is a genuinely underexplored artifact and converts directly into active sensing / adaptive computation. High novelty, moderate implementation cost.

**(13)–(14) Structured / residual-matched error injection.** The most underexplored families on your list. Precedents are thin: noise-robustness studies use i.i.d. Gaussian perturbations; sim-to-real work studies specific biases (latency, friction) but not as a *taxonomy of model-error structure at matched magnitude*; fault-injection is a term from dependability engineering, not WM research. The hypothesis that *temporally correlated bias damages closed-loop control far more than matched-magnitude white noise* is well supported by control theory intuition and scattered empirical hints (compounding-error studies) but lacks a definitive WM paper. **This is where I see the clearest publishable methodology contribution** (and it fits Information Fusion/Sciences framing: characterizing and simulating realistic model residuals, reliability analysis).

**(15) Action counterfactual fidelity.** Emerging, terminology unsettled ("action controllability," "action-conditioned fidelity"). Driving/video world models (GAIA-style, Genie-style) are known to produce plausible but weakly action-conditioned futures; DIAMOND and several 2024–2025 evaluations raise it. A crisp metric — *rank agreement of action sequences between model and simulator from matched states* — is cheap and largely unstandardized. Good novelty; pairs naturally with (16).

**(16) Policy-ranking agreement / optimization lift.** Precedents: model-based off-policy evaluation and OPE benchmarks report rank correlations; objective-mismatch work implies ranking is the right target; "optimization lift" as a named metric is non-standard. Measuring whether CEM/MPPI improvement inside the model transfers to the environment (and where it inverts — exploitation onset) is cheap in TD-MPC2 and diagnostic gold.

**(17) Horizon ladder.** Partially established: MBPO's branched short rollouts and its theory are exactly "short horizons are safe"; Dreamer's imagination horizon H=15/16 is a folk constant with some ablations; "model rollout truncation" and terminal value functions are standard. The *adaptive* horizon (uncertainty-chosen stopping) has some prior work (e.g., M2AC-style gating, dynamic horizon papers) but is not saturated for Dreamer/TD-MPC2-class systems.

**(18) Learned vs oracle history.** Established mostly as memory-task benchmarks (Memory Maze; POPGym; R2I) plus probing. Explicit history-swap interventions (GT-history-conditioned hidden state vs policy-generated) are rare; feasible in R2I/Dreamer since the recurrent state is exposed.

**(19) Metamorphic/equivariance tests.** "Metamorphic testing" comes from software engineering; applied to DNNs and some RL testing papers. In WM research the closest is structural evaluation of implicit world models (Vafa et al., NeurIPS 2024, "Evaluating the World Model Implicit in a Generative Model") and equivariant-model literature. Cheap, label-free, great for catching harness/preprocessing bugs; low ceiling as a standalone contribution.

**(20) Harness validation.** Established as folklore + reproducibility literature (Henderson; Engstrom; Machado's sticky actions; action-repeat/frame-stack discrepancies across repos are a documented source of incomparable numbers, including known differences in DMC action-repeat conventions across Dreamer/TD-MPC lineages). Non-negotiable step zero; never a paper by itself, but a paragraph that reviewers reward.

---

## 4. Condensed ranked strategy table (top 12; full 24-column table is better generated as a working spreadsheet once you confirm the target repos)

| # | Strategy | Terminology status | Separates | Retrain? | Sim access | Cost (2×48GB) | Decisive metric | Best repo | Follow-up method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Oracle reward + termination (eval-time head swap) | Non-standard ("oracle success/STOP" in VLN) | dynamics vs utility assignment | No | reward/term fn | Hours | Δreturn | DreamerV3, TD-MPC2 | task-aware WM, separate termination model |
| 2 | Periodic GT re-anchoring, frequency sweep | Non-standard; posterior-reset in RSSM terms | drift vs catastrophic error; model vs policy | No | obs or state | Hours | return vs k curve shape | DreamerV3/R2I | uncertainty-triggered reset (AAAI Route A) |
| 3 | 2×2 model×planner factorization | Fragmented precedents | model- vs planner-limited | Partial | full step fn | Days | 4-cell returns + exploitation sign | TD-MPC2 | targeted: planning vs model research |
| 4 | Teacher-forced vs closed-loop gap + horizon ladder | Established (exposure bias, compounding) | open/closed-loop; horizon | No | none | Hours | conversion gap; collapse horizon | all | adaptive horizon |
| 5 | Oracle uncertainty (true error) to planner | Motivated by MOPO/M2AC, unpublished online | calibration vs planner use of uncertainty | No | error computation | Hours–day | Δreturn vs ensemble proxy | TD-MPC2 | calibrated conservative planning |
| 6 | Policy-ranking agreement / optimization lift | Semi-standard (OPE) | prediction vs decision utility | No | eval rollouts | Hours | Spearman ρ; lift curve | TD-MPC2, DreamerV3 | exploitation-robust planning |
| 7 | Structured error injection at matched magnitude | Underexplored | which error structure kills control | No (oracle base) | full | Days | damage per error type | DMC + MPPI | robustness benchmark; IF/IS Route B |
| 8 | Residual-matched synthetic errors | Novel | realism of robustness evals | No | full | Days | closed-loop failure reproduction | same | Route B core |
| 9 | Oracle context (CARL/HiP-MDP) | Established (UP-OSI, RMA, CARL) | context inference vs dynamics learning | Yes (small) | params | Days | OOD Δreturn | CARL+TD-MPC2 | test-time context inference |
| 10 | Action-counterfactual fidelity | Emerging | causal action-conditioning vs plausibility | No | resets to state | Hours | action-rank agreement | DIAMOND/STORM/IRIS | controllability losses |
| 11 | Probing + oracle latent injection (with adapter) | Probing standard; injection non-standard | perception vs use-of-information | Small head | state | Day | probe R²; Δreturn | TD-MPC2 first | privileged distillation |
| 12 | Confidence-gated oracle queries | Novel (borrow risk–coverage) | sparse vs global model failure | No | state on demand | Day | return vs budget curve | DreamerV3 | active sensing |

Harness validation (family 20) and metamorphic checks (19) sit above the table as preconditions, not ranked entries.

---

## 5. Repository-level notes (from knowledge; verify versions)

**DreamerV3** (`danijar/dreamerv3`, JAX; PyTorch reimplementations exist, e.g., NM512/dreamerv3-torch — the PyTorch port is easier to surgically modify). Complete training code; no broad official checkpoint zoo (budget for training your own; DMC-scale runs fit comfortably on one 48GB GPU, several in parallel). Key intervention points: the RSSM `obs_step`/`img_step` split (re-anchoring = calling posterior on schedule during eval/imagination), `reward`/`cont` heads (family 1 swaps), imagination rollout loop (horizon ladder). DMC wrappers can be extended to expose `physics.get_state()` in `info` with ~10 lines. Two-GPU suitability: excellent for DMC/Crafter/Atari-100k/Memory Maze.

**TD-MPC2** (`nicklashansen/tdmpc2`, PyTorch). Clean, compact codebase; **official checkpoints are provided** (single-task and multi-task), which is a major advantage — many of your eval-time diagnostics need *no training at all*. MPPI planner in `plan()` is the natural seam: swap latent dynamics for simulator queries (slow but feasible at small population sizes), inject true error penalties, run ranking-agreement and 2×2 experiments. Decoder-free latents make the oracle-state variant a small retrain of the encoder/heads. **Start here.**

**IRIS / STORM / DIAMOND** (official repos exist for all three; Atari-100k focus). Good for families 4, 10, 15 (token/diffusion rollout fidelity, action-conditioning). Atari lacks a clean GT state (RAM state is a partial substitute; ALE exposes RAM), so oracle-state families are awkward — use these for observation-space and action-fidelity diagnostics, not state injection. DIAMOND's CSGO demo is out of scope for your compute.

**R2I** (if that's your "R2-Dreamer"): official code was released with the ICLR 2024 paper; Memory Maze + POPGym are the right envs for family 18. If R2-Dreamer is instead a 2026 model, it likely post-dates my knowledge.

**Environments**: DMC exposes full physics state (best oracle substrate); **DMC-GB2** for distribution-shift representation tests; **CARL** purpose-built for context experiments; Meta-World exposes state and success signals (good for oracle-termination); Crafter has an achievement-based harness good for reward/termination diagnostics; MiniGrid/Memory Maze for memory; Atari-100k for transformer/diffusion WM comparability.

---

## 6. The Bottleneck Panel (8 experiments, ~1 week wall-clock)

Precondition (Day 0): harness validation — deterministic replay, action-repeat/frame-stack audit against reference configs, random-policy and scripted-oracle scores, reward/termination recomputation from states.

1. **Teacher-forced vs closed-loop gap** (no retrain; all models). Stop rule: if gap is small and returns are still poor → problem is not rollout drift; go to 3/4.
2. **Horizon ladder with GT reset after H** (no retrain). Smooth degradation → compounding error (model direction); cliff at H* → catastrophic-event structure (family 13 direction).
3. **Oracle reward + termination, learned dynamics** (no retrain). Large gain → utility-assignment bottleneck; research task-aware heads, kill dynamics-architecture work.
4. **Oracle dynamics (sim query) + learned reward/value + learned planner** (no retrain; TD-MPC2). Compare against 3 to complete the factorization.
5. **2×2 completion: learned model + oracle planner proxy** (privileged MPC on true state as "oracle planner"; partial retrain of nothing — use a scripted or PETS-on-true-state planner). Neither oracle helps → suspect action space, benchmark, or harness.
6. **Re-anchoring frequency sweep k ∈ {1,2,5,10,25,∞}** (no retrain, Dreamer). k=1 failing to recover → policy/value problem, not model; shape of curve → drift vs isolated errors.
7. **Ranking agreement + optimization lift** (no retrain). ρ high but lift negative → exploitation; research conservative planning.
8. **Oracle uncertainty penalty vs ensemble penalty** (no retrain, TD-MPC2). Oracle helps, ensemble doesn't → calibration bottleneck; both fail → planner ignores uncertainty.

Every arm has a pre-registered interpretation; the panel kills directions cheaply: (3), (5), and (6@k=1) are your three **idea-killers**.

---

## 7. Explicit answers to your eight final questions

- **Most likely to reveal a useful bottleneck:** oracle reward+termination swap (panel #3) combined with the re-anchoring sweep (#6). Both attack components the community under-examines relative to dynamics architecture, and both have historically hidden failure modes (continuation-prediction errors; drift-vs-catastrophe ambiguity).
- **Easiest to implement:** teacher-forced vs closed-loop gap + horizon ladder — pure evaluation-loop code, no simulator internals, works on TD-MPC2 checkpoints today.
- **Highest potential novelty:** residual-matched structured error injection (families 13–14), followed by confidence-gated oracle-query budget curves.
- **Most likely to mislead:** naïve oracle latent injection (family 1) — interface/distribution mismatch between GT state and the learned latent space makes the downstream policy fail for reasons unrelated to competence; also cell (oracle model + strong learned planner) can *understate* model quality via exploitation asymmetry. Report zero-shot and adapter-tuned numbers, and always pair injection with probing.
- **Most naturally converted to a deployable algorithm:** re-anchoring → uncertainty-triggered latent reset / active sensing (RMA and event-triggered estimation give precedent and theory hooks); oracle context → test-time context inference is the second, with RMA as prior art to differentiate from.
- **Three repositories to modify first:** TD-MPC2 (checkpoints + clean planner seam), DreamerV3-PyTorch (RSSM posterior seam), and CARL's env wrappers (context exposure); STORM/IRIS third if the action-fidelity thread matters to you.
- **Three idea-killing experiments:** panel #3 (oracle reward/termination), #5 (neither-oracle-helps cell), #6 at k=1.
- **First-week plan:** Day 0–1: harness audit + TD-MPC2 checkpoints running on DMC with state-exposing wrappers. Day 2: gap + horizon ladder on 4–6 tasks. Day 3: oracle reward/termination swap. Day 4: simulator-query dynamics in MPPI (small population) → 2×2 cells. Day 5: re-anchoring sweep in Dreamer-PyTorch on 2 tasks + Memory Maze. Weekend: ranking-agreement/lift and oracle-uncertainty runs; write the decision memo.

---

## 8. Route A vs Route B, saturation, and Go/No-Go

**Route A (AAAI): uncertainty-triggered latent re-anchoring / adaptive imagination correction.** One failure mode (rollout drift), one intervention-derived hypothesis (sparse corrections at the right moments recover most oracle headroom), a compact method (disagreement- or error-triggered posterior resets and/or adaptive horizons), full feasibility on your hardware. It must be differentiated from M2AC-style gating and standard replanning — the differentiator is *evaluation-time latent correction from observations/active sensing rather than rollout truncation*. Strongest single AAAI direction from your list; adaptive horizons is the fallback if the reset curves are boring.

**Route B (journal): reliability-characterized model-error fusion.** Estimate the empirical residual structure of trained WMs (autocorrelation, heteroscedasticity, state/action dependence, rare catastrophic modes), show Gaussian-noise robustness benchmarks are unrealistic, and build a reliability-aware fusion of multiple predictors (deterministic/ensemble/short-vs-long-horizon) weighted by calibrated per-source reliability, evaluated across DMC/CARL/Meta-World with statistical and calibration analysis. This genuinely fits **Information Fusion** (multi-source reliability fusion is their core remit) better than Information Sciences; if the contribution ends up being mainly the residual-characterization methodology rather than the fusion mechanism, reposition to Information Sciences.

**Saturated:** yet another latent-dynamics architecture on Atari-100k/DMC leaderboards; generic ensemble-disagreement exploration; reconstruction-vs-no-reconstruction ablations; object-centric-slots-help-generalization claims without dynamics factorization; Gaussian-noise robustness tables.

**Underexplored:** conversion-gap and ranking-agreement as standard reported metrics; error-structure taxonomies at matched magnitude; oracle-query budget curves; termination/continuation modeling as a first-class component; eval-time causal intervention framing borrowed from interpretability.

**Go:** re-anchoring (A), residual-matched errors (B), oracle reward/termination diagnostics, ranking-agreement metrics, oracle-uncertainty-vs-ensemble. **Conditional Go:** oracle context (only if you can clearly differentiate from RMA/UP-OSI/PEARL). **No-Go as primary contributions:** oracle latent injection as a headline result (confounded), metamorphic tests alone, harness work alone, anything requiring DIAMOND-scale video WM training on two GPUs.

If you'd like, I can expand any single section — e.g., the full 24-column strategy table as a spreadsheet, or a concrete file-level modification plan for TD-MPC2 and DreamerV3-PyTorch — and a web-search pass would let me verify the 2025–2026 literature and the R2-Dreamer identity before you commit the first week.