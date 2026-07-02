# 3. Direction Map — pressure-tested against your actual context

Substrate: 2×RTX 4090/4090D (≈48GB total). No pretraining. Venues: ESWA / Information
Fusion / Q1 journals / strong workshops / top-tier if the object is strong.

**Caveat that applies to every occupancy judgment below:** my prior-art knowledge ends at
my training cutoff (Jan 2026). Every "room exists" claim is a hypothesis that must be
verified by live search before any GPU-hour is spent. That is not a disclaimer; it is
rule 1 of the audit.

---

## 3.1 Directions with real Modeling-Object-Shift room

### A. SFT distillation / reasoning correction dynamics — **strongest fit. DO.**

- **Current object:** token-level imitation of teacher trajectories — p_T(y|x) matched
  on clean, correct CoT text. Distillation = behavior cloning on geodesics.
- **Candidate new object:** the teacher's **error-recovery operator** — the conditional
  dynamics from a perturbed/erroneous reasoning state back to the solution manifold.
  Learn the contraction field around trajectories, not the trajectories alone.
- **Why real room:** the distribution-matching line (SeqKD, MiniLLM, DistiLLM, GKD) is
  crowded, but it treats *where* to match (on-policy vs off-policy), not *what* —
  recovery competence as a separable, transferable quantity is not the standard frame.
  The isomorphism to diffusion/DAgger is exact: clean-trajectory SFT fails off-manifold
  because supervised states are measure-zero; robustness lives in the field, not the path.
- **Why possibly fake:** it may collapse to "data augmentation with corrupted CoT +
  corrections," which IS occupied (LEMA-style learning-from-mistakes, RISE, self-
  correction SFT, 2023–2025). The object is only real if recovery competence
  **dissociates** from trajectory accuracy — models matched on clean accuracy that
  differ measurably in recovery.
- **Minimum falsifier:** equal-token-budget, equal-teacher-query-budget distillation of
  a 1.5–3B student two ways (standard CoT vs recovery-mix); evaluate continue-from-
  corrupted-state accuracy on GSM8K/MATH perturbation suites, ≥3 seeds. No dissociation
  → kill. <100 GPU-hours.
- **Likely level:** strong workshop → ACL/EMNLP/TMLR main if the dissociation is clean;
  Q1 journal as floor.

### B. Dataset evaluation / benchmark anti-Goodhart — **best compute fit. DO.**

- **Current object:** static per-sample quality; benchmark = pile of samples; leaderboard
  = ground truth.
- **Candidate new object:** the benchmark as a **measurement instrument under
  optimization pressure** — its score-to-capability transfer function ("Goodhart
  elasticity"): how much of a score gain on B survives on held-out capability probes
  after targeted optimization (SFT on adjacent data, prompt search) at fixed budget.
- **Why real room:** psychometrics/IRT gives static item discrimination (and IRT-for-
  leaderboards exists — Rodriguez et al.); contamination and robust-eval literatures
  (GSM-Symbolic-class) document the *symptoms*. Modeling the **derivative under
  pressure** as the benchmark's first-class property is, to my cutoff knowledge, not the
  standard frame. Goodhart's law is a claim about a derivative; nobody measures the
  derivative per-benchmark.
- **Why possibly fake:** degenerates into "yet another dataset-quality metric" —
  self-licking (rubric C5). The probes-are-also-benchmarks regress must be handled by
  pre-registration and relative (not absolute) elasticity claims.
- **Minimum falsifier:** if elasticity estimates are unstable across model pairs and
  seeds (rank correlation < ~0.5 across replications), the object is not measurable —
  kill. Also kill if trivial baselines (contamination detectors, perplexity heuristics,
  static IRT) predict transfer gaps equally well. Inference + light LoRA only — ideal
  for 2×4090.
- **Likely level:** NeurIPS Datasets & Benchmarks / TMLR; feeds every other direction
  (it is also your Research-OS's internal evaluation science). Q1 journal compatible.

### C. Masked discrete diffusion — **room exists, but only at the sampler. RESCOPE.**

- **Current object:** per-position token marginals trained under random mask schedules;
  sampling = confidence-heuristic unmasking.
- **Candidate new object:** the **commit/revise policy over the lattice** — which
  positions to trust, in what order, when to revise — with the network frozen. All joint
  structure that training factorizes away must re-enter at inference through ordering;
  therefore ordering carries measurable information.
- **Why real room:** frozen LLaDA/Dream-class checkpoints fit in 48GB; verifiable tasks
  (code with tests, math with answers) give free oracle reward for order search; the
  oracle-gap experiment (does *any* ordering beat confidence heuristics at matched NFE?)
  is a one-week, self-killing first experiment.
- **Why possibly fake:** highest occupancy velocity of anything on your list — remasking
  samplers (ReMDM-class), planned-denoising (DDPD), entropy orderings, plus the entire
  2019 NAT lineage (Mask-Predict) already own "order matters." See file 5 — I attack
  this one myself.
- **Likely level:** workshop → main conference only if the oracle gap is large;
  measurement-paper floor at TMLR.

### D. Diffusion loss / x0–score–velocity migration — **RESCOPE to measurement.**

The parameterizations are already unified in theory (v-prediction, ELBO-with-augmentation
views). No object-shift room in the objective itself. The residual question — *what does
each parameterization do to learned representations at small scale, for discriminative
reuse* — is a legitimate measurement paper feasible on 2×4090, and it feeds direction B's
methodology. As a method direction: dead. As a measurement direction: modest, safe, Q1.

---

## 3.2 Directions that are probably fake sophistication — be harsh

### MLLM multimodal fusion ("token concat → information-geometric alignment") — **KILL as object-shift; demote to normal engineering if you need Q1 volume.**

This is the poster child of object laundering. There is no observable that distinguishes
"information-geometric alignment" from "add a contrastive/alignment loss to cross-
attention" — occupied since ALBEF/BLIP (2021–22) and the bread and butter of Information
Fusion the journal. It fails the deletion test (C1) before breakfast. Publishable at
ESWA/Inf-Fusion as ordinary work — fine, if paper count is the goal — but do not spend
object-shift attention on it, and do not let the Research-OS dress it in geometry
vocabulary.

### VLA / manipulation / LIBERO / RoboTwin — **KILL as method direction at this substrate.**

The object-shift move here ("action prediction → action-correction field") is *already
the field standard*: diffusion policies and flow-matching policies ARE correction-field
models of action. Occupied at the core by groups with fleets of robots and thousands of
GPUs. On 2×4090 you can LoRA an OpenVLA-class model and run sim evals slowly; any LIBERO
delta will be attacked as sim-only and under-tuned. The *survivable rescope*: VLA
**evaluation** — LIBERO/RoboTwin success-rate metrics hide failure structure; apply
direction B's instrument-analysis to embodied benchmarks. Compute-light, under-occupied,
and merges two of your interests instead of losing to both.

### Information compression / matrix–graph–tree representations — **KILL until attached to a failure.**

As stated these are not directions; they are vocabulary in search of a task. No
phenomenon, no metric, no falsifier — pure idea-theater risk. The moment one of them is
attached to a concrete documented failure (e.g., a specific fusion failure that a graph
object retrodicts), re-enter through the rubric. Until then: zero GPU-hours, zero
writing-hours.

### Autonomous research workflow as a *paper* direction — **HOLD.**

Real genre (tooling school), but it is your named recurring failure mode: workflow
obsession substituting for research delta. The Research-OS is the *substrate*, and its
evaluation science is direction B. Write the workflow paper only when it has produced
≥2 externally validated research results — then it is an evidence-backed systems paper
instead of a promissory note. Workshop-level until then.

---

## 3.3 Task assignment (summary — full manual in file 6)

- **Fable (me):** adversarial reframing; object audits (deletion test, C1–C3); kill-
  experiment design; occupancy *hypothesis* generation + search-query design; reviewer
  simulation; autopsies; paper-framing compression; contested judgment calls.
- **Not Fable:** final novelty adjudication (cutoff-blind); long mechanical execution;
  RUNLOG bookkeeping; code-diff correctness; and — critically — never generator and
  auditor *in the same context window*.
- **Opus:** experiment execution and organization, tuning, harvesting, RUNLOG,
  turning designs into runnable configs.
- **Codex:** diffs, implementation correctness, intervention-actually-fired checks
  (your existing /exp-verify discipline).
- **Human (only):** promotion thresholds; program-level kills; venue strategy; taste
  priors; anything that spends reputation.

Your division "Pro generates · Opus operates · Codex checks · human sets taste" is
missing two roles and one principle — see file 6 §6.3 for the revision (short version:
add a *live-search novelty role* and a *stance-separated adversary*; route by stance,
not by model).
