# 4. Three Candidate Research Objects

Exactly three. Each passed the file-2 rubric to at least RESCOPE level before being
written down; each carries its own falsifier. Occupancy statements are cutoff-limited
hypotheses (Jan 2026) — live-search verification is a precondition for any of these
entering the run queue.

---

## Candidate 1: Recovery-Operator Distillation

### One-sentence thesis
Distillation should transfer the teacher's **error-recovery operator** — the correction
dynamics from erroneous reasoning states back to the solution manifold — rather than the
teacher's clean trajectory distribution.

### Old modeling object
p_T(y|x) on clean, correct chains of thought: token-level imitation of geodesics.
Distillation = behavior cloning.

### New modeling object
The teacher's conditional correction operator C: (problem x, corrupted state s̃) →
continuation returning to the correct solution manifold. The student learns the
contraction **field around** trajectories, not only the trajectories.

### Why the new object is more natural
First principles: supervised trajectories are measure-zero in reasoning-state space. At
inference the student leaves the supervised manifold within a few tokens (exposure bias;
in imitation-learning terms, DAgger's covariate-shift argument — the analogy is exact:
CoT SFT *is* behavior cloning). What makes a system robust off-manifold is not the
geodesic but the field that points home from everywhere — precisely diffusion's lesson
versus one-shot generation, and ResNet's lesson (model the correction, not the mapping).
The natural transferable quantity is therefore the contraction rate of the teacher's
dynamics, and trajectory imitation simply does not observe it.

### Failure phenomena explained
1. Distilled students are more brittle than teachers to perturbed premises at *matched
   clean accuracy* (GSM-Symbolic/GSM-PLUS-class findings).
2. Error snowballing: forced to continue from an injected mid-CoT error, teachers often
   recover; distilled students rarely do.
3. Longer CoT can *hurt* small distilled models — error accumulation without contraction.
4. Self-consistency (majority voting) helps teachers proportionally more than distilled
   students — student samples share systematic off-manifold drift.
5. Why on-policy KD (GKD) beats off-policy SFT: it samples off-manifold states — but
   implicitly and without structure. Recovery distillation is the explicit version, which
   is why GKD is the load-bearing baseline, not a footnote.

### Minimal method form (2×4090)
Teacher: 32B–72B via API or a 7B local teacher. Student: Qwen2.5-1.5B/3B, LoRA or full
FT with ZeRO across 2×24GB. Pipeline: harvest (x, CoT) pairs → generate corrupted states
(truncate + inject typed errors: arithmetic slip, premise misrecall, variable swap) →
query teacher to continue from corrupted state → build recovery pairs → SFT on a
recovery/clean mixture. Control: standard CoT SFT at **equal total tokens and equal
teacher-query budget**. Eval: clean GSM8K/MATH + a continue-from-corrupted-state suite +
perturbation robustness. Diagnostic: contraction rate — distance-to-correct-trajectory
decay after perturbation, as a function of training mixture.

### Minimum falsifying experiment
≥3 seeds, equal budgets. If recovery-mix SFT fails to improve corrupted-state
continuation accuracy beyond seed noise, or buys it only by losing more clean accuracy
than it gains — kill immediately. <100 GPU-hours. Secondary falsifier (the object test,
not just the method test): if recovery competence does **not dissociate** from clean
accuracy across model pairs — i.e., matched-accuracy models never differ in recovery —
the "separable operator" object is fiction, kill the framing even if the trick helps.

### Strongest reviewer attack
"This is error-correction data augmentation — LEMA / RISE / self-correction SFT already
do this. GKD already visits off-manifold states. You renamed data augmentation as an
'operator'."

### Preemptive defense
Baselines must include LEMA-style mistake-learning, GKD, and standard SeqKD at equal
budgets. The claim is narrowed to the dissociation: recovery competence is a separable,
transferable quantity — demonstrated by (a) double dissociation (matched clean accuracy,
different recovery; matched recovery, different accuracy), (b) cross-task recovery
transfer (train recovery on arithmetic, test contraction on logic), (c) the contraction-
rate diagnostic predicting downstream robustness better than clean accuracy does. If the
dissociation holds, the object is real regardless of the augmentation resemblance; if it
doesn't, the falsifier already killed it before a reviewer could.

### Likely venue positioning
ICLR/NeurIPS workshop first; ACL/EMNLP main or TMLR if the dissociation is clean; Q1
journal (ESWA-class) as floor. The mechanism story, not the delta, is the contribution.

### Confidence
**B.** Mechanism is first-principles sound and substrate-perfect; the risk is
concentrated in occupancy (2024–25 self-correction literature is dense — live search
mandatory) and in the real possibility that the dissociation experiment returns null,
which would be a clean, publishable-as-negative kill.

---

## Candidate 2: Goodhart Elasticity — the benchmark as a measurement instrument under optimization pressure

### One-sentence thesis
Dataset/benchmark evaluation should model a benchmark's **score-to-capability transfer
function under optimization pressure**, not the static quality of its samples.

### Old modeling object
Per-sample quality and aggregate accuracy; the benchmark as a passive pile of samples;
the leaderboard as ground truth.

### New modeling object
Per-benchmark (and per-item) **elasticity** ε(B) = ∂(held-out capability)/∂(benchmark
score) measured under controlled optimization pressure — targeted SFT on adjacent data,
prompt search, light RL — at fixed budget. The benchmark's first-class property is how
its meaning *degrades when used*.

### Why the new object is more natural
Psychometrics established a century ago that an instrument's value is validity, not item
polish — IRT models items by discrimination and difficulty. But ML benchmarks live under
a condition psychometrics never faced: the measured population *optimizes against the
instrument*. Goodhart's law is a statement about a derivative; the natural object is
therefore that derivative, measured, per benchmark. Static quality metrics are the wrong
object in exactly the way p(y|x) was the wrong object for OOD: they describe the
artifact, not the artifact-under-use.

### Failure phenomena explained
1. Leaderboard rank inversions after contamination events.
2. Benchmark saturation without capability gain (GSM8K↑ while GSM-Symbolic-style
   perturbed accuracy stalls).
3. Small models "beating" larger ones after targeted SFT — high-elasticity-looking
   scores from low-transfer optimization.
4. Dataset-quality filtering that *hurts* downstream: quality ≠ discrimination.
5. Rank instability across prompt formats — items with near-zero discrimination under
   pressure dominating aggregate scores.

### Minimal method form (2×4090)
4–6 benchmarks (GSM8K, MMLU slices, HumanEval, one perturbation-probe set) × 5–8 open
models (1.5B–8B) × 3 pressure types (LoRA-SFT on benchmark-adjacent data, prompt search,
few-shot selection) at fixed budgets. Measure score inflation on B vs movement on
pre-registered held-out probes; fit elasticity per benchmark and per item (IRT-style).
Pure inference + light LoRA — the direction on your list that fits 2×4090 best.

### Minimum falsifying experiment
If elasticity is not a stable property — rank correlation of ε(B) across model pairs and
seeds < ~0.5 — the object is not measurable; kill. Also kill if contamination detectors,
perplexity heuristics, or *static* IRT predict transfer gaps equally well (then the
"under pressure" part added nothing).

### Strongest reviewer attack
"Your held-out 'capability probes' are themselves benchmarks — infinite regress; and
this is the contamination/robust-evaluation literature plus IRT-for-leaderboards,
repackaged."

### Preemptive defense
Regress: pre-registered probe sets, elasticity reported as *relative* orderings (B1 vs
B2 under identical pressure), never absolute capability claims; sensitivity analysis
swapping probe sets. Prior art: static IRT and contamination detection are included as
baselines to beat — the delta is the dynamic term, and the falsifier above explicitly
kills the paper if the dynamic term is empty. The anti-Goodhart criterion applies to
itself: ε is validated by *predicting* future documented failures (held-out
contamination events, later-released perturbation suites), not by a metric we invent.

### Likely venue positioning
NeurIPS Datasets & Benchmarks / TMLR / dataset tracks; strong Q1 journal fit. Doubles as
the internal evaluation science of your Research-OS — every other direction consumes it.

### Confidence
**B+.** Best substrate fit on the list, self-applying methodology, moderate occupancy
risk in a busy area (contamination, dynamic benchmarks, IRT lines must be live-searched);
main risk is the falsifier itself — elasticity may genuinely be too noisy to be an
object, and that answer is cheap to obtain.

---

## Candidate 3: The Unmasking Policy as the Modeling Object of Masked Diffusion LLMs

### One-sentence thesis
In masked-diffusion language models, the object worth modeling is the **commit/revise
policy over the token lattice** — which marginals to trust, in what order, when to
revise — with the network frozen; the field is good enough, the dynamics is the binding
constraint.

### Old modeling object
Per-position conditional marginals trained under random mask schedules; sampling
delegated to confidence-heuristic unmasking.

### New modeling object
The unmasking/revision policy as a first-class sequential decision process over the
lattice, learned or optimized separately from the network.

### Why the new object is more natural
Masked-diffusion training factorizes an intractable joint into per-position marginals;
every bit of joint structure discarded by that factorization must be reintroduced at
inference through *ordering and revision*. Parallel-decoding failures are conditional-
independence errors by construction. Therefore the information is provably in the
ordering; the only question is whether it is exploitable — which is measurable directly.

### Failure phenomena explained
1. Quality collapse at low step counts / high parallelism (independence violations).
2. Non-monotone quality vs number of denoising steps.
3. Masked LLMs trailing AR at matched parameters on reasoning, with the gap shrinking
   under better inference procedures — sampler-limited, not model-limited.
4. Remasking/revision helping unevenly across task types.
5. Position and length biases of confidence-based unmasking.

### Minimal method form (2×4090)
Frozen LLaDA-8B / Dream-7B (fits in 48GB inference). Stage 1 — the oracle: best-of-N
*order search* on verifiable tasks (code with unit tests, math with checkable answers =
free oracle reward), quality at matched NFE vs confidence heuristics. Stage 2 — only if
the oracle gap is large: distill searched orderings into a small policy head; compare at
matched NFE and wall-clock.

### Minimum falsifying experiment
Run the oracle FIRST. If exhaustive-ish order search cannot beat confidence-based
unmasking by a clear margin at fixed NFE on verifiable tasks, then ordering carries no
exploitable signal and the entire object dies in ~1 week of inference compute. This is
the cheapest self-kill on the list.

### Strongest reviewer attack
"Remasking samplers, planned-denoising, entropy orderings, and the entire 2019 NAT
lineage (Mask-Predict) already own 'order matters' — this is a decoding-heuristics paper
wearing modeling-object language."

### Preemptive defense
Reframe the deliverable as a *decomposition*: how much of masked diffusion's quality gap
is sampler-limited vs model-limited — a scientific measurement no individual sampler
paper delivers; existing samplers become baselines inside the measurement. NFE- and
wall-clock-matched comparisons throughout.

### Likely venue positioning
ICLR/NeurIPS workshop; main conference only if the oracle gap is large; TMLR as the
measurement-paper floor.

### Confidence
**B−.** The falsifier is beautiful and cheap, but this sits in the fastest-moving
occupancy zone on your list, and the method half is structurally vulnerable — which is
why I attack it myself in file 5.
