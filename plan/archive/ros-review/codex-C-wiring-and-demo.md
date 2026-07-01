# Codex-C - ROS Wiring and Kill-Reviewer Demo

Inputs read:
- `plan/research-operating-system.md`
- `plan/goal-directive.md`
- `plan/operating-manual.md`
- `plan/paper-draft.md`
- `plan/frozen-pareto-negative-synthesis.md`

## Job 1 - Wiring

### Minimal surviving gates

Keep only gates that either bind to a human/external fact or cheaply produce adversarial evidence. Do not turn the loop into a fixed pipeline.

| Loop point | Gate | Fires when | Output | Stop rule |
|---|---|---|---|---|
| SELECT | Taste gate | New Track, new thesis, or any lead intended to become a paper claim | Taste Card plus anti-reward-hacking rule | Human taste decision required before treating it as a paper-worthy direction. Tactical variants inside an already approved direction can proceed by Codex SELECT. |
| SELECT | External-decision stub | Any candidate promoted as paper-worthy | One sentence: who changes what decision if true | If unanswerable, downgrade to internal note or engineering result. |
| Pre-experiment | Preregister | Every experiment, dev or sealed | Timestamped H/falsifier/acceptance/metric/split/negative-control | Agent may not score or inspect sealed data until this exists. |
| Cross-system compare | Baseline champion | Any "beats X", frontier, dominance, or architecture-comparison claim | Independent adversary report plus optimized baseline config | No comparison claim without sign-off or an explicit "baseline not maximal" downgrade. |
| DECIDE | Kill reviewers | Before bank-as-positive, paper promotion, or broad negative synthesis | Four kill-only persona outputs | Any standing kill blocks promotion; agent may fix, rerun, or downgrade. |
| DECIDE | Negative grade | Any failed method or null result | Failed-attempt / scoped-negative / structural-negative | No broad negative language unless scope, falsifier, and controls justify structural-negative. |
| Pivot | Pivot ledger | Any thesis change after seeing results | Original claim, result, failed reason, new claim, saw-results-first flag | Tactical redesign can continue; thesis/paper pivot returns to SELECT taste gate. |
| Paper mode | Claim-evidence + human decision gate | Any draft, title, abstract, or external-facing claim | Claim-evidence matrix plus external-decision answer | Agent may draft, but may not decide publishability, scope expansion, or architecture-advantage language alone. |

### Exact goal-directive edit

`plan/goal-directive.md` is already size-constrained. Do not append a new section. Replace line 13:

```md
RULES: pre-declare hypothesis/falsifier/acceptance/negative-control. Metrics = generation/verifier-based (diffusion loss diagnostic only). B_test SEALED. AUTONOMY: do NOT ask the user to choose -- decide, proceed, report.
```

with this compact replacement:

```md
RULES: prereg H/falsifier/accept/neg-ctrl+metric/split; gen/verifier metrics; B_test sealed. ROS: SELECT taste; compare baseline-champion; DECIDE kill-reviewers; pivot ledger; paper human gate. AUTONOMY: run loop; no self-set success/scope/paper.
```

Rationale: the goal prompt should carry only the hard boundary. The detailed routing belongs in the operating manual.

### Exact operating-manual edit

Add the following section after `## 5. Science protocol (the kernel - gate every move)`:

```md
### 5.1 Research OS taste and anti-Goodhart gates

Principle: goal mode is autonomous for search, implementation, falsification, and evidence collection. It is not autonomous for defining success, broadening scope, or deciding that a result is externally publishable.

Minimal routing:

| Loop point | Gate | Required action |
|---|---|---|
| SELECT | Taste gate | For a new Track, new thesis, or paper-aiming direction, prepare the Taste Card: field belief, bottleneck, clean reformulation, minimal system, killer experiment, anti-reward-hack rule, understanding gain, title test. Human taste decision gates paper-worthiness. Codex may still select tactical experiments inside an already approved direction. |
| SELECT | External-decision stub | For any paper-aiming direction, write: "If true, who changes what decision?" If there is no concrete decision-maker, continue only as internal engineering unless the human overrides. |
| Pre-experiment | Preregister | Before scoring, freeze hypothesis, falsifier, acceptance threshold, metric, split, negative control, budget, and commands in RUNLOG/tree metadata. Sealed splits remain immutable. |
| Cross-system compare | Baseline champion | Before any "beats X", "dominates", "frontier", or architecture-comparison claim, assign an independent reviewer/agent to make the opposing baseline win. The claim is blocked until the champion signs off or the text is downgraded to "not baseline-maximal". |
| DECIDE | Kill reviewers | Before positive banking or paper promotion, run four kill-only reviewers: Metric Skeptic, Baseline Maximalist, Scope Lawyer, Impact Nihilist. Standing kills block promotion, not tactical iteration. |
| DECIDE | Negative grade | Grade nulls as failed-attempt, scoped-negative, or structural-negative. Structural-negative requires predeclared falsifier, live negative controls, locality/confound checks, and sealed confirmation if claimed externally. |
| Pivot | Pivot ledger | When the thesis changes after results are known, append a RUNLOG/tree entry with original claim, result, failed reason, new claim, and whether the new claim was seen-results-first. Tactical redesign continues; paper-thesis pivot returns to SELECT. |
| Paper mode | Claim-evidence and human decision | Before title/abstract/external claim, list each claim with its evidence type: fair-baseline, compute-matched, oracle, counterfactual, OOD holdout, CI, sealed reproduce, or human-scope decision. Claims without evidence are downgraded. Human gate decides paper-worthiness and scope. |

Autonomy boundary:
- The agent may unilaterally observe, ideate, create tactical variants, preregister experiments, dispatch worktree executors, tune implementation, run dev/sealed evals under frozen contracts, update tree/RUNLOG, rerun failed harnesses, and bank clean evidence as evidence.
- The agent may not unilaterally choose a new paper-worthy direction, change success metrics after seeing evidence, broaden scope, declare a result publishable, declare "architecture advantage", or decide that an external claim survives a standing kill condition.
- "Do not ask the user to choose" means do not ask for tactical experiment choices. It does not override the human taste+decision gate for direction selection and paper-mode promotion.
- If a human is unavailable, Pro/Codex may prepare a TASTE-UNVERIFIED recommendation, but the result remains blocked from paper-mode promotion until the human gate is satisfied.
```

Also amend the §2 loop sentence from:

```md
OBSERVE -> IDEATE -> SELECT -> DISPATCH+verify -> DECIDE -> (pass+publishable: bank & advance . FAIL: re-IDEATE with the new evidence) -> loop.
```

to:

```md
OBSERVE -> IDEATE -> SELECT(+taste gate only for new/paper directions) -> DISPATCH+verify -> DECIDE(+kill reviewers before promotion) -> (pass: bank evidence & advance . FAIL: re-IDEATE . paper/publishable: human decision gate) -> loop.
```

This preserves continuous goal-mode autonomy while removing the current ambiguity where "pass+publishable" can be self-declared.

## Job 2 - Live Demo: Kill-Only Reviewers

Context used: the paper draft claims a verified wall-clock frontier on MATH-L5 for DiffusionGemma vs Gemma-4 AR under HF-vs-HF serving on 2x4090. The frozen-Pareto synthesis supports a scoped negative: several post-hoc fixed-generator interventions do not move the native dLLM budget-Pareto, but it is explicitly not a universal "only retraining works" claim.

### Metric Skeptic - kill conditions only

- Kill if the S(B) / verified-answers-per-second metric was selected after observing that dLLM has a candidate-arrival-rate advantage, rather than frozen before the comparison with timestamped protocol.
- Kill if the same paper would not be written if AR won on S(B); that would make S(B) a pro-diffusion story device rather than a neutral deployment utility.
- Kill if the log-B AUC window, budgets {768,1280,2048}, or "fair 2048" framing were chosen after curve inspection and no predeclared grid/range artifact exists.
- Kill if "verified answers per second" is presented as the deployment utility without a scope gate for exact-verifier tasks; outside verifier-rich branching, it may be the wrong objective.
- Kill if per-verified-second collapses serving throughput, verifier availability, candidate quality, and architecture into one headline without a claim-evidence split.
- Kill if pass@k, raw benchmark quality, cost/FLOP, energy, and no-verifier regimes are omitted when they would reverse or neutralize the deployment conclusion.

### Baseline Maximalist - kill conditions only

- Kill top-venue and dominance claims if the AR baseline is only HF `generate` and not the strongest realistic serving stack available to a deployer: vLLM, SGLang, tensor parallelism, continuous batching, flash-attn-compatible substitutes, compile/CUDA graph paths, or documented impossibility with evidence.
- Kill if no independent baseline champion tried to make AR win by tuning batch size, padding, KV cache, serving mode, prompt format, stopping policy, and parallel repeated sampling.
- Kill if the wall-clock advantage depends materially on HF pipeline/serving overhead rather than model-family decoding structure.
- Kill if throughput mode does not model realistic multi-request serving where continuous batching can change AR's time-to-first-verifier-correct.
- Kill if dLLM uses its shipped optimized sampler while AR is constrained to a less optimized generic stack and the headline still says "dominates" rather than "HF-vs-HF on 2x4090".
- Kill architecture language if the paper lacks profiler/accounting that separates AR per-step cost, dLLM canvas-pass cost, KV effects, batching effects, NFE depth, and GPU utilization.

### Scope Lawyer - kill conditions only

- Kill any claim that exceeds MATH-L5, 134 problems, seed-matched small-sample eval, one model pair, HF serving, and 2x4090 hardware.
- Kill unqualified "diffusion models buy more verified reasoning per second"; the evidence supports "this shipped dLLM pair under this verifier-rich setup".
- Kill "architecture advantage" language unless it is explicitly downgraded to a deployment measurement and not a causal architecture ablation.
- Kill "dominates the verified wall-clock frontier" unless every occurrence carries the scoped frontier definition, budget grid, verifier, hardware, and serving context.
- Kill "arrival-rate mechanism" if it is used causally beyond the measured decomposition; fewer forward-pass invocations is not by itself a controlled architecture proof.
- Kill broad use of the frozen-Pareto negative as support for Track-1 unless the text preserves its own scope: fixed frozen DiffusionGemma, tested post-hoc classes, native budget-Pareto, verifier-rich hard set.
- Kill "just run the largest budget" outside the six-action grid / MATH-L5 / 3-seed setting.

### Impact Nihilist - kill conditions only

- Kill as a top-venue paper if no real deployer decision is changed beyond "on 2x4090 with HF serving and exact math verifier, choose DiffusionGemma@2048 over Gemma-4 AR@2048".
- Kill if the result does not alter a serving, model-selection, benchmark-design, or training-research decision for a named audience.
- Kill if serious deployers would immediately ask for vLLM/SGLang or production-batching numbers before changing anything.
- Kill if the paper has no released harness/raw traces/verifier manifest sufficient for other labs to reproduce the wall-clock frontier.
- Kill if the deployment takeaway ignores that the AR sibling may have better raw model quality outside the verifier-rich branch/deepen regime.
- Kill if the frozen-Pareto synthesis is used as impact without showing that external researchers care about ruling out those post-hoc dLLM interventions on more than this single model/domain.

## Overall Verdict

True epistemic status: workshop-measurement with a strong internal positive and useful scoped structural-negative companion. It is not yet a top-venue result, and it is not yet a systems artifact. The current draft is most defensible as a measurement paper about the correct utility for verifier-rich branching under a specific shipped pair and serving stack.

Before any "architecture advantage" language is allowed:

1. Baseline champion must sign off on a strongest-realistic AR baseline: vLLM/SGLang or documented impossibility, tuned batching/continuous batching/KV/parallel sampling, and second hardware if the claim is wall-clock general.
2. The scope must expand or be causally controlled: at least AIME plus code/Olympiad-style verifier tasks and preferably a second matched pair, or a mirrored/controlled ablation that separates architecture from model-family and serving differences.
3. The claim-evidence matrix must split "deployment win", "serving artifact", "forward-pass-depth effect", and "architecture effect"; only the last can use architecture language, and only after profiler/FLOP/latency evidence survives the baseline champion.

