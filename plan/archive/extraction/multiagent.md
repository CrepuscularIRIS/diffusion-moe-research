# Methodology Extraction: MultiAgent Hypothesis Discovery System

**Source**: `/home/lingxufeng/agent/MultiAgent`
**Extracted**: 2026-06-29
**Purpose**: Harvest experiment-discipline / workflow patterns reusable for the frozen DiffusionGemma research loop.

---

## 1. What It Is

A domain-agnostic multi-agent control plane for hypothesis discovery and falsification. The system defines **6 reasoning phases** (P0 Context → P1 Understand → P2 Locate → P3 Hypothesize → P4 Predict → P5 Evidence/Converge), **5 specialized agents** mapped to distinct CLI profiles (reader-mapper/Kimi, diverger/Gemini, critic/Codex, converger/Claude, executor/Claude), **26 skills**, **3 domain adapters** (research-experiment, quant-factor, algorithm-benchmark), and a complete **artifact + schema contract** enforced by deterministic state reducers. Its distinguishing design principle is strict separation of six inference operations (Forward Deduction, Reverse Abduction, Pure Abduction, Deduction From Hypothesis, Counter-Abduction, Induction) as labeled fields in every artifact, preventing the common failure of collapsing all reasoning into one vague paragraph. The system is equally applicable to ML research, quant factor discovery, and algorithm engineering.

---

## 2. Core Methodology / Workflow Spine

### 6-Phase Pipeline

```
P0 Context     → SourcePack, KnownFactsLedger, UnknownsLedger, ContradictionLedger
P1 Understand  → ArchitectureDeductionMap (forward deduction),
                 DesignIntentReconstruction (reverse abduction)
P2 Locate      → FailureOrGapCase, ParadigmFrictionReport
P3 Hypothesize → AbductiveHypothesisSet (≥3 orthogonal),
                 OrthogonalBranchMatrix, HiddenKnowledgeDisclosure
P4 Predict     → DeductivePrediction, MinimalVerificationPlan (L0/L1 MVE ≤50 lines),
                 ProbePlan (L2), HypothesisContract, IdentifiabilityPlan
P5 Converge    → CriticReview, CounterAbductionReview, ConvergenceState,
                 InductivePattern, handoff to executor
```

### Agent-to-CLI Routing Contract

| Agent | CLI | Role |
|---|---|---|
| reader-mapper | Kimi | Long reading, SourcePack; output is `candidate_context` until reviewed |
| diverger | Gemini | Orthogonal hypothesis generation; output is `candidate` until reviewed |
| critic | Codex | Inference separation, falsifiability, leakage/confounder audit |
| converger | Claude | Select, predict, design test, build HypothesisContract |
| executor | Claude | Execute MVE/probe only after valid handoff; write result artifacts |

**Mainline Gatekeeper Rule**: Gemini/Kimi output is raw candidate material. It may NOT mutate SearchTreeState, ResearchDAGState, claim maturity, or Truth Layer until Claude normalizes it AND Codex audits it. Every Gemini/Kimi-origin artifact must carry:

```yaml
origin_cli: gemini-cli | kimi-code
mainline_status: candidate
reviewed_by: claude | codex
```

### Six Inference Operations (must appear as SEPARATE labeled fields in every artifact)

| Operation | Given → Infer | Key Artifacts |
|---|---|---|
| Forward Deduction | Architecture rules → expected behavior | ArchitectureDeductionMap |
| Reverse Abduction | Observed choices → likely design intent | DesignIntentReconstruction |
| Pure Abduction | Anomaly/failure → mechanism hypotheses | AbductiveHypothesisSet |
| Deduction From Hypothesis | Mechanism → predictions, falsifiers, tests | DeductivePrediction, ProbePlan |
| Counter-Abduction | Verifier result → updated belief, branch action | CounterAbductionReview, ConvergenceState |
| Induction | Repeated observations → scoped pattern | InductivePattern, ClaimEvidenceTable |

---

## 3. Experiment Standards / Specs

### Verification Ladder (enforced, no skipping)

```
L0  Thought Test   — logically coherent? obvious counterexamples?
L1  Synthetic/MVE  — ≤50-line idealized script; must pass before scaling
L2  Real Probe     — small real-data test with controls
L3  Full Run       — full experiment / backtest / benchmark
```
L3 is blocked until L0/L1 pass or a documented waiver exists.

### Hypothesis Spec (unified schema)

```yaml
hypothesis:
  id:
  domain: research | quant | algorithm
  phenomenon:
  mechanism:
  condition:
  predicted_observable:
  falsifier:
  minimal_test:
  negative_control:
  alternative_mechanisms:
  expected_failure_mode:
  source_artifacts:
  inference_trace:
    deduction:
    reverse_abduction:
    pure_abduction:
    induction:
```

### Failure Typing Protocol A-E (mandatory before counter-abduction conclusion)

| Type | Signal | Next Action |
|---|---|---|
| A | Effect in predicted direction but below threshold | REVISE — strengthen intervention; stay on same branch |
| B | Effect present but controlled by alternative cause | REVISE — add controls; retest same hypothesis |
| C | No effect in predicted direction, or opposite | PRUNE — write NegativeCase; return to P3 |
| D | Unexpected systematic pattern (not noise) | SPLIT — revise causal chain; best discoveries come from here |
| E | Crash, NaN, sanity violation | FIX CODE, RERUN — do NOT revise the hypothesis |

**Critical**: Confusing Type C (dead mechanism) with Type E (implementation bug) is the most expensive misclassification. ResultForensics artifact is mandatory before deciding.

### ResultForensics (mandatory post-mortem)

```yaml
result_forensics:
  hypothesis_id:
  result_artifact:
  result_hash:
  expected: {metric, direction, threshold}
  observed: {metric_value, direction_observed, delta_from_expected, variance_across_seeds}
  classification_inputs:
    crashed_or_invalid: true | false
    effect_in_predicted_direction: true | false | partial
    effect_magnitude_vs_threshold: above | below | at
    controls_show_same_effect: true | false | not_tested
    pattern_systematic_not_noise: true | false | unclear
  failure_type: {type: A|B|C|D|E|success, rationale}
  alternative_explanations_considered: []
  next_action: {action: revise|prune|split|fix_code|declare_support, target}
```

### Claim Maturity Ladder

| Level | Name | Required Evidence |
|---|---|---|
| L0 | Conjecture | None; must be labeled |
| L1 | Hypothesis | inference_trace showing which reasoning produced it |
| L2 | Prediction | DeductivePrediction with falsifier and threshold |
| L3 | Supported | ProbeResult / BenchmarkResult artifact with hash |
| L4 | Promoted | ClaimEvidenceTable + integrity audit + reviewer signoff |

**Two most expensive errors**: (1) L0 treated as L2 — conjecture written as testable prediction; (2) L3 treated as L4 — single positive probe promoted without negative controls.

### R1-R12 Anti-Cheating Rules (Research Constitution)

| Rule | Statement |
|---|---|
| R1 | Scores ≠ discovery; transferable mechanisms = discovery |
| R2 | All complexity defaults guilty; needs ablation proof |
| R3 | Never report best seed only; show seed distribution |
| R4 | Never let test feedback become training signal |
| R5 | Single dataset ≠ mechanism validity |
| R6 | New method must explain "why baseline fails here" |
| R7 | Any theory must include failure condition |
| R8 | Agents free to switch direction but must leave decision trail |
| R9 | Prioritize compressed explanations over indicator stacking |
| R10 | If score and explanation conflict, suspect the score |
| R11 | If multiple agents converge on same direction, raise exploration temperature |
| R12 | Low-scoring direction with clear failure signal → allow diagnostic, don't auto-eliminate |

### AConferenceIdeaScore (10-dimension bottleneck)

```yaml
idea_score:
  axiom_break:               # 1-10: Does this challenge something fundamental?
  mechanism_clarity:          # 1-10: Can you explain the mechanism in one paragraph?
  operator_minimality:        # 1-10: Is the intervention the smallest possible?
  falsifiability:            # 1-10: Does the falsifier actually falsify?
  experiment_identifiability: # 1-10: Does the experiment isolate the mechanism?
  equal_compute_fairness:    # 1-10: Is the comparison fair?
  boundary_map_quality:      # 1-10: Do we know where it works and fails?
  transfer_potential:        # 1-10: Would this work in other domains?
  narrative_compression:     # 1-10: Can the story be told simply?
  evidence_grounding:        # 1-10: Does every claim have evidence?
  bottleneck_score:          # min() of ALL above — this IS the final score
  bottleneck_dimension:      # which dimension is the bottleneck
  recommended_fix:           # one action to raise the bottleneck
```

Bottleneck principle: 9/10 on everything, 2/10 on falsifiability → score is 2.

### Orthogonality Protocol for P3

Six path types for branches (each branch declares exactly one):

- `SOTA-extension` — extend current frontier mechanism
- `Failure-repair` — directly repair known failure cluster
- `First-principle-injection` — inject axiom/mechanism from AxiomBank
- `Domain-interpolation` — borrow mechanism from adjacent domain
- `Axiom-challenge` — challenge a hidden assumption in the field
- `Evaluation-reframe` — build/modify benchmark to expose failure

**Rejection rule**: Two branches that differ only in surface name but test the same mechanism variable must be merged or replaced.

**Gate**: P3 must not finalize AbductiveHypothesisSet if all branches come from the same perspective lens.

### Reward-Framing Guard

| Condition | Allowed Action |
|---|---|
| Support result + identifiability PASS | Promote mechanism claim |
| Support result + identifiability WARN | Route to more probes (not promotion) |
| Support result + identifiability FAIL | Downgrade to outcome-support only, no mechanism claim |
| Highest score among branches | Not a promotion signal by itself |

---

## 4. Reusable Artifacts — Actual Prompts / Templates / Rubrics

### 4.1 Surprise Detection Self-Check (from `hypothesis-discovery-core/SKILL.md`)

```
At the end of every skill's output, answer:
- [ ] What in this output surprised me? Name the specific finding.
- [ ] If nothing surprised me, did I genuinely engage with the evidence or just fill the schema?
- [ ] What would a skeptical reader's first objection be? Write it down.
- [ ] Does my output reduce the search space, or did I just add options without eliminating any?

If all four answers are empty or generic, the output is likely shallow. Revise before submitting.
```
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/hypothesis-discovery-core/SKILL.md`

### 4.2 Search Space Reduction Accounting (from `hypothesis-discovery-core/SKILL.md`)

```yaml
search_space_status:
  alive_at_start: <N>
  eliminated:
    - hypothesis_id:
      reason:
  added:
    - hypothesis_id:
      justification:
  net_change: <+/- M>
  expansion_justified: <true/false — if net positive, why?>
```

If net change is positive across three consecutive phases → trigger convergence review.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/hypothesis-discovery-core/SKILL.md`

### 4.3 Prior vs Posterior Dual-Column Log (from `hypothesis-discovery-core/SKILL.md`)

```yaml
prior_posterior_log:
  - step: "<current reasoning step>"
    prior: "<what I believed before this step>"
    posterior: "<what the evidence now shows>"
    delta: "<what changed and why>"
```

**Detection rule**: If prior == posterior for every entry, the agent did not learn — it confirmed. This catches agents generating "insights" that are reformulations of their priors.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/hypothesis-discovery-core/SKILL.md`

### 4.4 Operator Algebra (12 Transforms for hypothesis generation, from `abduction-search/SKILL.md`)

```
| Transform | Thinking Prompt |
|---|---|
| Axis Rotation | "What if the mechanism operates on a different dimension entirely?" |
| Fixed-to-Adaptive | "What if this fixed parameter were conditioned on input?" |
| Explicit-to-Latent | "What if this external process were internalized as latent state?" |
| One-pass-to-Iterative | "What if a single forward pass became iterative refinement?" |
| Dense-to-State | "What if global computation used finite state memory instead?" |
| Posthoc-to-Endogenous | "What if this post-processing step were built into the model?" |
| Scalar-to-Field | "What if this single score became a spatiotemporal field?" |
| Module-to-Protocol | "What if we changed the protocol (training, eval, data) not the module?" |
| Average-to-Routing | "What if average fusion became selective routing?" |
| Static-to-Dynamical | "What if static structure became a dynamical system (ODE, feedback)?" |
| Local-to-Conservation | "What quantity is conserved? What quantity is broken? Follow the break." |
| Benchmark-to-Microscope | "What if we built a benchmark that directly observes the mechanism?" |
```

Use 3-4 most relevant transforms per problem. Document which were considered and skipped.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/abduction-search/SKILL.md`

### 4.5 PerspectiveMatrix (7 technical lenses, from `abduction-search/SKILL.md`)

```yaml
perspective_matrix:
  failure_or_gap_id:
  perspectives:
    - lens: information_theory
      phenomenon_rewritten_as: "<failure in terms of entropy, channel capacity, MI, compression>"
      mechanism_candidates: []
      blind_spots_exposed: "<what this lens reveals that default framing misses>"
      cheap_test: "<minimal experiment that would discriminate this lens's prediction>"
    - lens: optimization
      ...
    - lens: geometry_topology
      ...
    - lens: systems
      ...
    - lens: causal_inference
      ...
    - lens: economics_game_theory
      ...
    - lens: cognitive_science
      ...
  cross_lens_disagreements:
    - "<two lenses whose predictions diverge — this is a hypothesis seed>"
  unanimous_dismissals:
    - "<what all lenses would dismiss — possible blind spot worth probing>"
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/abduction-search/SKILL.md`

### 4.6 MechanismCompositionGraph (from `abduction-search/SKILL.md`)

7 composition types: `serial | parallel | gating | residual | dual | distillation | protocol_plus_module`

```yaml
mechanism_composition_graph:
  nodes:
    - mechanism_id:
      mechanism_variable:
      role: primary | supporting | competing | substitute
  edges:
    - source:
      target:
      composition_relation: serial | parallel | gating | residual | dual | distillation | protocol_plus_module
      condition:
  predicted_synergy: "<non-additive effect neither mechanism produces alone>"
  predicted_failure_if_component_removed:
    - if_removed:
      predicted_degradation:
  minimal_composition: "<smallest set needed to produce predicted synergy>"
  ablation_plan:
    - A_only:
    - B_only:
    - A_plus_B:
    - inert_replacement_for_A:
    - inert_replacement_for_B:
  conflict_resolutions: []
```

**Gate**: Any P4 plan for a composed mechanism must include A-only, B-only, A+B, AND inert-replacement ablations (or documented waiver). Without the full ablation cascade, the contribution is unidentified.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/abduction-search/SKILL.md`

### 4.7 Silent Axiom Mining Protocol (from `abduction-search/SKILL.md`)

```
Before generating any hypothesis:
1. List 3 things everyone in this field assumes but never states explicitly.
2. For each silent axiom:
   a. What evidence supports it? (Strong or just traditional?)
   b. What would be true if this axiom were false?
   c. What anomalies are consistent with the axiom being false?
   d. What experiment would be the cheapest way to test it?
3. Any axiom where (a) is weak and (c) has hits → Axiom-challenge branch candidate.

If Silent Axiom Mining produces zero candidates, the mining was superficial.
Real fields always have unstated assumptions.
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/abduction-search/SKILL.md`

### 4.8 Three-Frame Self-Adversarial Review (from `cross-model-review-discipline/SKILL.md`)

```
Frame 1: Correctness Audit — write findings BEFORE starting Frame 2
  - Does every claim have a specific evidence pointer (file:line, artifact:field)?
  - Do numbers in artifact match numbers in source data?
  - Is anything claimed "observed" that was actually "inferred"?

Frame 2: Assumption Challenge — write findings BEFORE starting Frame 3
  - What are the 3 strongest assumptions this artifact makes without stating them?
  - Is there a simpler explanation? (Parsimony check)
  - If you had to argue AGAINST this artifact's main claim, what is your best argument?

Frame 3: Red Team
  - Where could data leakage hide in the experimental setup?
  - What happens with different random seeds?
  - Could this result be an artifact of the evaluation metric?
  - What is the most likely way this hypothesis could be "right for the wrong reason"?
  - Reviewer 2: what would destroy it?
```

Rule: Frame 3 Red Team must name at least one vulnerability (real artifacts always have one). If zero, the review was lazy.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/cross-model-review-discipline/SKILL.md`

### 4.9 IdentifiabilityPlan (from `minimal-test-design/SKILL.md`)

```yaml
identifiability_plan:
  hypothesis_id:
  causal_question: "<the specific causal claim — 'X causes Y via mechanism M'>"
  treatment:
  outcome:
  competing_mechanisms:
    - mechanism_id:
      how_it_explains:
  confounders:
    - confounder:
      control_method:
  mediator:
  negative_control:
  placebo:
  invariance_test: "<what should NOT change if the mechanism is real>"
  what_result_distinguishes_hypothesis_from_alternatives: |
    "If we observe <specific result pattern>, target mechanism is supported AND
    alternative <mechanism_id> is ruled out because <reason>."
```

Mandatory at L2+. Without `what_result_distinguishes_hypothesis_from_alternatives`, a "support" verdict is equally explained by a competing mechanism.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/minimal-test-design/SKILL.md`

### 4.10 Vital Signs Diagnostics — Pre-Training Checks (from `experiment-design-patterns/SKILL.md`)

```
| Vital Sign | What to Measure | What It Catches |
|---|---|---|
| Feature rank | Effective rank of hidden representations | Representation collapse |
| Token uniformity | Entropy of attention distribution | Degenerate attention |
| Gradient conflict | Cosine similarity between gradients of different loss terms | Conflicting objectives |
| Layer contribution | Magnitude of residual stream update per layer | Dead layers |
| Loss landscape | Loss surface around initialization | Pathological landscape |
| Convergence speed | Loss after N steps (N << full training) | Wrong LR or architecture mismatch |
```

Cheap diagnostics (minutes, not hours) that prevent wasted training GPU-days.
file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/experiment-design-patterns/SKILL.md`

### 4.11 5 Probe Design Patterns (from `experiment-design-patterns/SKILL.md`)

```
1. Locality Probe: Does the mechanism operate where we think? Change mechanism in ONE region; measure if effect is localized.
2. Sensitivity Probe: Vary mechanism parameter continuously; look for smooth dose-response curve (real mechanism) vs noise (spurious).
3. Counterfactual Probe: Remove mechanism COMPLETELY, measure what breaks. Zero effect = not a real mechanism.
4. Equal-Compute Control: Give baseline same computational budget (params, FLOPs, time). If baseline catches up = mechanism is just more compute.
5. Ablation Cascade: Remove components ONE AT A TIME. Use INERT REPLACEMENT (neutral version), not deletion (which confounds mechanism removal with architecture change).
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/experiment-design-patterns/SKILL.md`

### 4.12 Four-Ledger Knowledge Disclosure (from `knowledge-disclosure/SKILL.md`)

Quality gate — disclosure is complete when:
- [ ] KnownFactsLedger has ≥1 entry marked `model_prior` (if zero, honesty is suspect)
- [ ] UnknownsLedger has ≥1 entry that would change hypothesis direction if resolved
- [ ] ContradictionLedger is non-empty OR includes explicit "no contradictions found" with justification
- [ ] HiddenKnowledgeDisclosure names at least one specific model prior or methodological bias
- [ ] No entry cites `read_artifact` without naming the specific file/path

Per-cycle ImplicitKnowledgeBlock (appended to EVERY artifact, not just phase start):

```yaml
implicit:
  silent_priors:
    - "<specific assumption I made but did not state>"
  unspoken_alternatives:
    - path: "<approach I considered but did not pursue>"
      why_skipped: "<honest reason>"
  failure_dna:
    - "<if something went wrong, what is the root cause deeper than the surface error?>"
  hidden_dependencies:
    - "<seed, CUDA version, data ordering, or other environmental factor>"
  skeptical_PI_questions:
    - question: "<hardest question a skeptical PI would ask>"
      honest_answer: "<my actual answer, not a deflection>"
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/knowledge-disclosure/SKILL.md`

### 4.13 Context Budgeting Policy (from `research-context-budgeting/SKILL.md`)

```
P0 Context:    HIGH budget — reading everything is the job
P1 Understand: MEDIUM — produce maps, drop raw sources after extraction
P2 Locate:     MEDIUM — consume P1 maps, find failures, drop P0 material
P3 Hypothesize: LOW — carry ONLY failure cases + axiom references; drop everything else
P4 Predict:    MEDIUM — retrieve specific upstream details as needed
P5 Evidence:   HIGH — final audit, but verify freshness of each artifact
```

**P3 Warning**: P3 is where stale context causes the most damage. Agents carrying P0/P1 material generate "obvious" hypotheses — variations of what they already read, not genuinely surprising mechanisms.

Context-as-Action Policy:
```
Keep    — recent critical errors, active hypothesis state
Drop    — verbose old code, resolved issues, superseded hypotheses
Compress — long source summaries, detailed logs → one-line summary
Retrieve — relevant past failures, specific upstream artifact sections
Verify  — weak memory → re-read; strong artifact with hash → trust
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/research-context-budgeting/SKILL.md`

### 4.14 P3 Hypothesize Issue Template (from `templates/P3-hypothesize.md`)

```yaml
# Acceptance Criteria (machine-checkable)
- [ ] HiddenKnowledgeDisclosure emitted before hypotheses
- [ ] AbductiveHypothesisSet contains >= 3 candidates
- [ ] Each candidate has: mechanism_variable, falsifier, predicted_observable, path_type
- [ ] Each candidate declares exactly one of: SOTA-extension, Failure-repair,
      First-principle-injection, Domain-interpolation, Axiom-challenge, Evaluation-reframe
- [ ] No two candidates share the same mechanism variable with different surface names
- [ ] OrthogonalBranchMatrix shows distinct mechanism variables across branches
- [ ] All statements tagged inference_type: pure_abduction
```

file: `/home/lingxufeng/agent/MultiAgent/templates/P3-hypothesize.md`

### 4.15 CriticReview + Devil's Advocate Protocol (from `critique-gate/SKILL.md`)

```
For each hypothesis or claim under review, construct the strongest attack from three angles:
1. Confounder Attack: "What other variable could produce the same observation? What experiment
   distinguishes the proposed mechanism from this confounder?"
2. Parsimony Attack: "What simpler mechanism explains the data equally well? If a simpler
   explanation exists and has not been ruled out, the complex hypothesis is premature."
3. Boundary Attack: "At what input/scale/condition does the mechanism break? Does it degrade
   gracefully (real mechanism with scope limits) or catastrophically (implementation artifact)?"

Steel-Man rule: Before writing any finding, state the strongest version of what the artifact
claims. Then attack THAT version, not a simplified or weakened version.
Evidence Chain Tracing:
  claim → evidence → experiment → probe design → prediction → hypothesis → mechanism → anomaly
  At which link does the chain first weaken? That weakest link is the finding.
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/critique-gate/SKILL.md`

### 4.16 Paradigm Friction Detection (from `idealation-methodology/SKILL.md`)

```
| Pattern | Symptom | Intervention |
|---|---|---|
| Refined Mediocrity | Incremental improvements never challenge core assumptions | Force one Axiom-challenge branch per cycle |
| Cognitive Comfort Zone | Staying in familiar methods when problem needs different tools | Apply 3 Operator Algebra transforms from unfamiliar domains |
| Resource Path Dependence | Continuing direction due to sunk cost, not promise | Ask: "If starting fresh with this knowledge, would I take this path?" |
```

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/idealation-methodology/SKILL.md`

### 4.17 Completion Contract (from `CLAUDE.md`)

```
Issue done ≠ complete
Artifact exists ≠ complete
Completion = artifact + manifest + state_delta + reducer_applied + semantic_validator PASS
```

file: `/home/lingxufeng/agent/MultiAgent/CLAUDE.md`

### 4.18 Hypothesis Portfolio Routing Schema (from `hypothesis-portfolio-routing/SKILL.md`)

Stall detection — a branch is stalled when:
- No new evidence in 3+ verification cycles
- All remaining falsifiers require L3 without L1/L2 passing
- Cost exceeds allocated budget
- Branch revised 3+ times without convergence

Routing priority order:
1. High expected value AND low verification cost
2. Branches that falsify the most alternatives simultaneously
3. High novelty (avoid refined mediocrity)
4. Highest evidence debt (reduce uncertainty first)

file: `/home/lingxufeng/agent/MultiAgent/.claude/skills/hypothesis-portfolio-routing/SKILL.md`

---

## 5. Command/Skill Candidates

| Name | 1-line Purpose | Trigger | Engine |
|---|---|---|---|
| `/failure-type` | Classify a failed experiment as A/B/C/D/E before deciding next action | After any probe/experiment returns non-success | Opus (main, read ResultForensics) |
| `/hypothesis-score` | Score a hypothesis on 10-dimension AConferenceIdeaScore, identify bottleneck | Before committing to L2/L3 | Opus + Codex second-pass |
| `/silent-axiom-mine` | Surface 3+ unstated field assumptions; generate Axiom-challenge branch candidates | At P3 ideation, before hypothesis generation | Opus |
| `/operator-transform` | Apply 12 Operator Algebra transforms to current mechanism; generate orthogonal alternatives | When P3 branches look like surface variants | Opus (GPT-5.5 Pro for deep mode) |
| `/perspective-matrix` | Reframe the failure through 7 technical lenses; find disagreements between lenses as hypothesis seeds | When P3 hypotheses are all from the same angle | GPT-5.5 Pro (multiple distinct framings) |
| `/mechanism-composition` | Map how candidate mechanisms compose (serial/parallel/gating/etc.); generate ablation plan | When contribution involves multiple mechanisms | Opus |
| `/vital-signs` | Run pre-training diagnostics (feature rank, attention uniformity, gradient conflict, dead layers) | Before any L3 GPU run | Opus + Bash (actual measurement) |
| `/identifiability-check` | Produce IdentifiabilityPlan: what result distinguishes hypothesis from alternatives? | Before finalizing ProbePlan | Opus |
| `/critic-3frame` | Three-frame self-adversarial review (Correctness → Assumption Challenge → Red Team) | Before handoff of any HypothesisContract or ClaimEvidenceTable | Codex (or Claude subagent with context isolation) |
| `/prior-posterior-log` | Force prior-vs-posterior dual-column log; flag if prior==posterior (agent didn't learn) | After each experiment or reasoning step | Opus |
| `/search-space-accounting` | Track alive/eliminated/added hypothesis counts; trigger convergence review if net positive 3+ phases | After each P3/P4/P5 cycle | Opus |
| `/surprise-check` | End-of-step self-check: what surprised me? Did I reduce the search space? | After any artifact is produced | Opus |
| `/context-budget` | Apply phase-appropriate context budget; tag stale items; detect model_prior smuggled as fact | At start of each phase | Opus |
| `/paradigm-friction` | Diagnose which friction pattern blocks progress (Refined Mediocrity / Comfort Zone / Path Dependence) | When research direction feels stuck | GPT-5.5 Pro |

---

## 6. NEW vs Our Kernel — Comparison

### ADOPT (genuinely new, high value)

**1. Failure Typing Protocol A-E**
Our kernel knows "failed experiments must shrink search space" but does not distinguish Type C (dead mechanism → prune) from Type E (implementation bug → fix code, not hypothesis). This is a critical operational distinction that could have saved us GPU-days on the direction-C persistence experiments. Adopt fully.

**2. Prior vs Posterior Dual-Column Log**
Our kernel has no explicit mechanism to detect when an agent's "insight" is just a reformulation of its prior belief. The dual-column log makes this visible: if prior==posterior after an experiment, the experiment taught nothing. Adopt as a mandatory per-cycle artifact.

**3. Surprise Detection Self-Check**
"What surprised me?" as a mandatory end-of-step question that blocks output if all answers are empty or generic. Our kernel has skeptical-default as a disposition but no operational mechanism to enforce it. Adopt.

**4. Search Space Reduction Accounting**
Our kernel says "a failure must shrink the search space" but provides no tracking mechanism. The `search_space_status` schema (alive_at_start, eliminated, added, net_change) with a trigger for convergence review when net positive 3+ consecutive phases is concrete and automatable. Adopt.

**5. AConferenceIdeaScore (10-dimension bottleneck)**
Our kernel lacks a structured scoring system for ideas. The bottleneck principle — final score = min() of all dimensions — directly encodes our "identify the weak link" approach. The 10 dimensions (especially `operator_minimality`, `experiment_identifiability`, `boundary_map_quality`) are precisely the dimensions where our track-2 gradient-field ideas need stress-testing. Adopt.

**6. Operator Algebra (12 transforms)**
Our kernel has cross-domain structural mapping but no enumerated transform catalog. The 12 transforms (especially Scalar-to-Field → directly maps to our embedding-field framing; Module-to-Protocol → training/eval changes not architecture; Average-to-Routing → MoE-style routing) are directly applicable to our current diffusion MoE research. Adopt.

**7. PerspectiveMatrix (7 technical lenses)**
Our kernel's cross-domain structural mapping is similar in spirit but lacks the formalism of running 7 distinct lenses and explicitly recording disagreements between lenses as hypothesis seeds. The `unanimous_dismissals` field also surfaces potential blind spots. Adopt for P3 ideation.

**8. MechanismCompositionGraph**
Our work involves at least 3 composed mechanisms (frozen DLLM + timestep router + gradient/velocity field). The composition algebra and mandatory A-only/B-only/A+B/inert-replacement ablation plan is exactly what our experiments need to distinguish contributions. Adopt.

**9. Silent Axiom Mining**
Our kernel's first-principles reduction is similar but less operational. The explicit 4-step protocol (list unstated assumption → check evidence strength → check anomaly consistency → cheapest test) is more actionable. The rule "if zero candidates, mining was superficial" prevents lazy pass-throughs. Adopt.

**10. IdentifiabilityPlan**
Our kernel has falsifiability-first but lacks a structured artifact that asks "what result distinguishes THIS hypothesis from the alternative mechanisms?" The `what_result_distinguishes_hypothesis_from_alternatives` field is the concrete operationalization of our falsification principle. Adopt.

**11. Vital Signs Diagnostics**
Pre-GPU diagnostics: feature rank, attention uniformity, gradient conflict, dead layers. Our current practice runs training then diagnoses from loss curves. These cheap pre-run checks (minutes) could prevent wasted GPU days. Directly applicable to our SFT baseline experiments. Adopt.

**12. Reward-Framing Guard**
"No artifact may promote a hypothesis solely because it has the highest score — it must also pass identifiability." Our kernel has score≠mechanism but lacks this as an explicit routing gate that blocks promotion. Directly fixes the problem we observed with diffusion loss as quality proxy. Adopt.

**13. Three-Frame Self-Adversarial Review**
Our kernel has generator/critic/selector isolation across distinct models, but within a single engine context, there is no structured protocol. The three-frame protocol (Correctness → Assumption Challenge → Red Team, each frame written before next begins) with mandatory "Frame 3 must find at least one vulnerability" provides cognitive isolation within Claude. Adopt for high-stakes artifact reviews.

**14. R1-R12 Anti-Cheating Rules**
Our 8 science kernels overlap with some (especially R1=score≠mechanism, R3=show seed distribution, R4=no test feedback in training) but miss others. Specifically NEW: R8 (switch direction but leave decision trail), R11 (multi-agent convergence = raise exploration temperature), R12 (low-scoring direction with clear failure signal → allow diagnostic). The Arbor tree captures R8 partially; R11 and R12 are new operational rules. Adopt R11 and R12.

**15. Per-Cycle ImplicitKnowledgeBlock**
Beyond the four ledgers (emitted at phase start), requiring `silent_priors, unspoken_alternatives, failure_dna, hidden_dependencies, skeptical_PI_questions` on EVERY reasoning output is more granular than our existing disclosure. The `failure_dna` field (what is the root cause deeper than the surface error?) and `skeptical_PI_questions` are directly applicable. Adopt.

**16. Context Budgeting with P3 Low-Budget Warning**
The explicit rule that P3 (hypothesis generation) must be aggressively pruned explains a failure mode we have likely encountered: carrying too much context from earlier phases causes the LLM to generate obvious hypothesis variants rather than genuinely new mechanisms. Adopt as an explicit protocol.

**17. Paradigm Friction Detection (3 patterns)**
Refined Mediocrity / Cognitive Comfort Zone / Resource Path Dependence with specific interventions. The Resource Path Dependence intervention ("if starting fresh with this knowledge, would I take this path?") is a forcing function that our loop currently lacks. Adopt for `/goal` cycle reviews.

### OVERLAPS (already in our kernel, no action needed)

- **Falsifiable-before-build** → our L1 (falsify-before-build); their L0/L1 verification ladder
- **Evidence ≠ memory** → our science kernel #2; their "agentmemory recalls, does not certify"
- **Score ≠ mechanism** → our science kernel #3; their R1 + reward-framing guard
- **Sealed eval/test** → our science kernel #3 (SEALED eval/test); their "eval-path changes forbidden in probe patches"
- **Multi-engine isolation** → our Opus/Codex/GPT-5.5 split; their reader-mapper/diverger/critic/converger/executor + CLI routing contract
- **MechanismHypothesis 5-field schema** → our (silent_axiom→mechanism→hypothesis→observable→falsifier); their HypothesisSpec (adds negative_control, inference_trace — slightly richer)
- **Idea tree structure** → our Arbor MCP idea tree; their SearchTreeState + ResearchDAGState (more formal, schema-validated)
- **Claim-ladder** → our recipe→mechanism→paper claim-ladder; their L0-L4 maturity levels
- **Negative result must shrink search space** → our science kernel #7; their NegativeCase + Failure Typing C = prune

### SKIP (platform-specific or implementation artifacts)

- Multica platform orchestration (labels, issue lifecycle, daemon, runtime objects) — Arbor covers this for us
- LangGraph JSON config and routing scripts — our `/goal` + Arbor handles routing
- StateDelta YAML reducer / SearchTreeState schema files — our Arbor tree + RUNLOG is the equivalent
- Validation shell scripts (`validate-truth-layer.sh`, etc.) — project-specific to their artifact directories
- Specific artifact manifest format (`artifacts/manifest.json`) — not needed; our experiment results live in worktrees

---

## 7. Top-3 Highest-Value Takeaways

### Takeaway 1: Failure Typing A-E is the single most operationally valuable addition

Our current loop conflates "experiment failed" → "revise hypothesis." The A-E taxonomy (especially the Type E = implementation bug = fix code NOT hypothesis distinction) would have prevented at least one wasted iteration in our track-1 work. The mandatory `ResultForensics` artifact before any counter-abduction conclusion is a concrete gate. Implement this immediately as a required step after every probe in direction-C.

### Takeaway 2: The AConferenceIdeaScore bottleneck principle gives our `/ideate` a structured exit criterion

Our ideation loop generates candidates but has no structured way to declare one "ready to build." The 10-dimension scoring with `bottleneck_score = min()` means the weakest dimension is the score, and the fix is always single-pointed (raise the bottleneck dimension). For track-2 gradient-field work: the current bottleneck is likely `experiment_identifiability` (does the experiment isolate velocity-field vs CE objective as the causal variable?) — exactly what the IdentifiabilityPlan artifact would formalize.

### Takeaway 3: MechanismCompositionGraph + full ablation cascade is exactly the missing piece for our multi-mechanism claims

Our track-2 direction combines at least: frozen DLLM substrate + timestep-conditioned router + gradient/velocity-field training objective. The MechanismCompositionGraph schema (composition type + predicted synergy + predicted_failure_if_component_removed + ablation plan with A-only/B-only/A+B/inert-replacement) is the formal structure that turns "these three things together work" into a defensible mechanism claim. Without it, a reviewer can always argue the gain came from one component alone. Implement before any L3 GPU run on track-2.
