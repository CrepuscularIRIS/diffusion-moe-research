# Methodology + Beatless Research Engine — Extraction Report
# Extracted: 2026-06-29
# Source repos: /home/lingxufeng/research/methodology · /home/lingxufeng/research/beatless-research
# Purpose: harvest reusable research discipline for DiffusionGemma autonomous loop

---

## 1. What it is

Two companion repos that together form a complete autonomous AI-research pipeline: `methodology/` is the philosophical and experimental-science kernel — formalising *how to think* (Idealation V5.2 道/器/术/势, V19 Paradigm Vision, Update.md experiment disciplines, plan/Regulations.md three core principles) — while `beatless-research/` is the engineering engine that executes that kernel as a 23-stage ACP multi-agent loop with venue-aware novelty gates, orthogonal niche fan-out, and contract-based isolated experiment execution. The two repos were built by the same researcher and cross-reference each other constantly: the beatless constitution YAML (v1.0.4) is essentially the methodology docs compiled into enforceable gates. The key operational product is: given a topic, get from raw idea to venue-grade experiment design in ~50 minutes, with hard gates blocking LLM verbal-pattern-matching from masquerading as genuine novelty.

---

## 2. Core Methodology / Workflow Spine

### 2.1 Idea Formalism — the Five-Tuple

Every research idea is a 5-tuple (from `methodology/V19_PARADIGM_VISION.md`):

```
Idea = <Silent_Axiom, Anomaly, Mechanism_Variable, Operator_Rewrite, Killer_Experiment>
```

Example:
```
fixed-depth residual accumulation          ← Silent Axiom (nobody challenged it)
→ depth-direction contribution dilution anomaly  ← Anomaly (real failure)
→ layer-contribution / gradient distribution     ← Mechanism Variable
→ replace additive with content-dependent retrieval  ← Operator Rewrite (minimal)
→ verify depth amplitude, gradient distribution, scaling law, equal-compute gain  ← Killer Experiment
```

This is stronger than a free-text hypothesis because every slot is structurally distinct and forces pre-commitment before GPU spend.

### 2.2 The 12 Operator Algebra Transforms

A closed vocabulary of idea-generation moves (`V19_PARADIGM_VISION.md`):

| Transform | Action |
|---|---|
| Axis Rotation | Rotate mechanism across dimensions (sequence attention → depth attention) |
| Fixed-to-Adaptive | Fixed constant → conditional mechanism |
| Explicit-to-Latent | External process → latent state (CoT → latent loop) |
| One-pass-to-Iterative | Single forward → iterative solve |
| Dense-to-State | Global quadratic → finite state memory |
| Posthoc-to-Endogenous | Post-processing → model-internal |
| Scalar-to-Field | Single score → spatiotemporal field |
| Module-to-Protocol | Don't change model, change protocol |
| Average-to-Routing | Average fusion → selection/routing |
| Static-to-Dynamical | Structure as ODE/feedback system |
| Local-to-Conservation | Find conserved/broken quantities |
| Benchmark-to-Microscope | Benchmark observes mechanism, not just scores |

### 2.3 The Idealation V5.2 Framework (道/器/术/势)

**道 (Way) — 10 First-Principles Axioms** (`methodology/Idealation.md`):
- Physics: Symmetry/Conservation, Energy Minimization, Scale Invariance, Thermodynamics/Entropy
- Math: Topology/Geometry, Sparsity/Low-Rank, Orthogonality, Duality
- Information: Information Bottleneck, Minimum Description Length

Any new method must ground to ≥1 axiom or it is mechanistically unanchored.

**器 (Arsenal) — 20 Meta-Functionality Library (MF-01 to MF-20)**: Global dependency modeling, local feature extraction, gradient flow stabilization, sequential gating, structural aggregation, adversarial distribution approximation, iterative denoising, parameter-efficient adaptation, physics-process differentiability, information bottleneck compression, multiscale fusion, conditional controllable generation, linear-complexity sequence modeling, sparse expert activation, topological feature extraction, geometric constraint embedding, feature disentanglement, cross-modal representation unification, latent space representation learning, differentiable planning. New concept must diff ≥3 algorithmic lines vs closest meta-function or flag as RENAMING SUSPECT.

**术 (Tactics) — 3 Innovation Modes**:
- Standard mode: decompose → weapon-match → integrate (SOTA papers, 3-6 months)
- Cost-efficiency mode: find unused deep principle → design cheap differentiable approximation → justify via theory depth not engineering complexity (1-2 months)
- Extreme mode: identify core axiom → design counterfactual experiment → look for "conservation-breaking" signals → invent new axiom from break point

**势 (Stance) — 3 Mandatory SOPs**:
- Weekly 4h cross-domain reading (Cell, Physics Review, Econ Quarterly — not your field)
- Anomaly Signal Log: every result violating theory expectation must be logged with conservation-breaking type; reviewed every Friday
- Dual-column experiment records: left = prior hypothesis (before), right = posterior attribution (after); distinguishes genuine insight from hindsight

### 2.4 Experimental Science Disciplines (`methodology/Update.md`)

**6 mandatory experimental conditions:**
1. Interventiable causal variable: "I change X, Y must monotonically change" with clean implementation
2. Double-validation logical completeness: every hypothesis pre-declares its killer experiment (negative direction) and executes it
3. Three-layer non-skippable experimental protocol:
   - Mechanism probe (synthetic/controlled, verifies core causal mechanism exists)
   - Capability boundary scan (real data + extreme tests, defines coordinates where method fails)
   - Insight extraction experiment (visualization/principles, transfers findings across tasks)
4. Multi-level vital signs monitoring (not just loss/acc): optimization dynamics (weight update ratio, gradient noise scale), representation health (feature rank, inter-layer CKA, token uniformity), generalization diagnostics (generalization gap growth rate, sharpness-aware metric)
5. Single-variable ablation discipline: each ablation changes exactly one operator form; information pathway count unchanged; only functional module replaced
6. Failure sample anatomy: structured diagnostic report per failure (attention entropy, feature margin, gradient conflict degree); synthesize adversarial pressure samples

**6 research decision gates** (hard gates, no bypass):
1. Topic gate: can you express it as "X causes Y to fail under Z conditions" in one sentence?
2. Hypothesis signature gate: written as "if P changes, then Q monotonically changes, via mechanism E"; killer experiment listed
3. Mechanism verification gate: in synthetic experiment, is mediator effect significant? If not confirmed, BANNED from spending GPU on real data
4. Failure boundary registration gate: method's collapse boundary defined across data dimension/model depth/SNR axes
5. Insight extraction gate: can you output one reusable design principle in "when seeing phenomenon A, prefer constraint B"?
6. Narrative integration gate: does the story form "phenomenon→pain→hypothesis→killer→mechanism→boundary→principle" closed loop?

### 2.5 Three Core Research Architecture Principles (`methodology/plan/Regulations.md`)

**Principle 1 — Parallel + Orthogonal Coverage:**
- ≥3 niches (directions) per cycle; each niche's "core question" in one sentence; cosine-overlap must be <0.6 between any pair (enforced by orchestrator)
- If ≥2 niches converge to same experimental change in previous cycle → force reassign (entropy collapse = R11)
- Must dispatch in same message (not serial)

**Principle 2 — Triple Heterogeneous Review:**
- Writer ≠ reviewer (hard constraint)
- Pass 1 (Codex): correctness dimension, diff vs claim vs numbers, any mismatch = flag
- Pass 2 (Gemini): assumption-challenge, probe p-hacking, demand compression, challenge hidden premises
- Pass 3 (Claude red-team in fresh context): try to prove shortcut/leakage/seed cherry-pick/overfit/dataset reuse
- BLOCK if any R1/R4/R5/R6/R7/R10 triggered; FLAG if R2/R3/R8/R9/R11/R12

**Principle 3 — Surface Implicit Knowledge (declared "most important" in the doc):**
Every generator cycle MUST output a structured implicit block:
```yaml
implicit:
  silent_priors: "<assumptions taken for granted but not stated in prompt>"
  unspoken_alternatives: "<options considered but not tried, with honest reason why>"
  failure_dna: "<root cause one layer deeper than commit message>"
  hidden_dependencies: "<environmental premises prompt didn't ask about: seed, CUDA, upstream data>"
  what_a_skeptical_PI_would_ask: "<3 hardest questions you least want to answer, with initial answers>"
evidence_pointers:
  - "<file:line | log | commit SHA — each implicit field needs one>"
```
Rationale: LLM "reasoning" is only the explicit chain; actual priors that drive conclusions go unrecorded. Without surfacing these, self-critique is surface-level theater.

### 2.6 Constitution v1.0.4 Hard Gates (`beatless-research/rules/constitution/v1.0.4-draft.yaml`)

**Gate 1 — Minimal Differentiation Sentence (MDS):**
```
"Unlike <citekey>, which <prior approach mechanism>, our work <minimal precise gap with math/algorithm term>."
```
- MDS length ≥80 characters
- Must contain math/algorithm/information-theory term
- Must ground to ≥1 primal axiom from §J

**Gate 2 — Renaming Detector:**
- List ≥5 essentially-identical existing concepts
- Pseudocode line-diff ≥3 lines vs each closest existing concept
- Design 5-min mechanism-separation experiment

**Gate 3 — Token-Preserving Ablation:**
```
AB-1: weak_label_only (baseline 1)
AB-2: unstructured_rationale (baseline 2)
AB-3: perfect_structured_prior (our method)
AB-4: corrupted_but_ordered (control)
AB-5: shuffled_perfect_structure (DECISIVE — must run)
AB-6: random_noise_control (control)
AB-7: oracle_strong_label (upper bound)
```
Decision rule: If AB-5 ≈ AB-3 (shuffled equals perfect structure) → method is just rationale supervision rebrand → REJECT

**Gate 4 — Dual Metric:**
- Hidden-test accuracy ↑ vs naive distillation
- CAPA / error-overlap with weak supervisor ↓
Either missing → REVISE

### 2.7 Dual-CLI ACP Routing Architecture (`methodology/Goal.md`)

8-phase architecture where each phase has explicit Proposer + Validator roles with different models:

| Phase | Proposer | Validator | What |
|---|---|---|---|
| 0 Reproduce | — | — | Baseline without LLM |
| 1 Failure Mining | Kimi | GPT | worst-K / cluster grinding vs artifact noise |
| 2 Axiom Discovery | Gemini | Opus | 5-lens axiom search vs "silent assumption" check |
| 3 Operator Compilation | GPT | Opus | axiom → operator rewrite → minimal code change |
| 4 Feasibility Audit | GPT | Gemini | implementability + literature counter-search |
| 5 Mechanism Probe | Opus | GPT | synthetic probe + 3 controls + killer condition |
| 6 Code Mutation | Opus | GPT | minimal unified diff → diff validation |
| 7 Benchmark Eval | — | — | Pure compute; then Kimi extract → Opus interpret |
| 8 Promotion Decision | Opus | GPT (devil's advocate) | metacognitive judgment + 3 confounders |

The Gemini anti-sycophancy constraint is hard-wired: every Gemini response must end with:
```
Do NOT agree with the previous analysis. Find what is WRONG.
List 3 specific factual errors or logical gaps.
```

### 2.8 Orthogonal Niche Fan-Out (`beatless-research/SOTA-CHASING-ACP-LOOP.md`)

5 mutually-exclusive attack vectors with mutual-exclusivity proof:

| Niche | Dimension | Forbidden | Mandatory |
|---|---|---|---|
| N1 repr | Representation learning | — | Self-supervised pretrain head |
| N2 loss | Loss function | Don't modify model.py forward | ≥1 of contrastive/focal/OT/energy/quantile |
| N3 aug | Data augmentation | Don't modify model.py | ≥3 augs including 1 domain-specific |
| N4 calib | Post-hoc calibration | No retrain (model weights frozen) | temperature-scaling/Platt/conformal/energy-score |
| N5 arch | Architecture search | — | Modify model.py ≥3 places |

Mutual exclusivity: N2/N3/N4 don't modify model; N5 must modify model; N1 is the only one that can run independently adding a pretrain head. Guarantees 5 independent search paths and prevents collapse to "all finetune transformer."

---

## 3. Experiment Standards / Specs (Gates, Checklists, Schemas)

### 3.1 7 Mandatory Artifacts before GPU Spend (`V19_PARADIGM_VISION.md`)

1. **AxiomCard**: old assumption + why nobody challenged it
2. **AnomalyCard**: real failure/anomaly that triggered the idea
3. **MechanismDAG**: X → M1 → M2 → Y multi-hop causal chain (not a single-hop correlation)
4. **OperatorPatch**: minimal implementable structural change (must be diff-expressible)
5. **ProbeSuite**: synthetic mechanism experiment + negative control + equal-compute controls
6. **BoundaryMap**: where method works/fails (axes: length, noise, frequency, depth, scale)
7. **ClaimEvidenceTable**: each paper claim → log line + table row + figure + code diff

### 3.2 AConferenceIdeaScore (min-form)

```python
score = min(
    axiom_break_score,       # does it challenge a first-principle?
    mechanism_clarity,       # can you specify M1→M2 in DAG?
    operator_minimality,     # is the change minimal diff?
    falsifiability,          # is there a specific killer experiment?
    experiment_identifiability, # can mechanism be separated empirically?
    equal_compute_fairness,  # same compute as baseline?
    boundary_map_quality,    # explicit failure coordinates?
    transfer_potential,      # works on ≥2 domains?
    narrative_compression,   # one-sentence explainability?
    evidence_grounding       # every claim has pointer?
)
```

The min-aggregation is important: prevents a single strong dimension (e.g. impressive story) from masking critical failures (no falsifier).

### 3.3 Gaps Archive Protocol

- Stage 8 must output ≥10 gap candidates
- ALL candidates kept in `gaps_archive/` even if score <7
- Each gap entry must have: mds, renaming_audit, axiom_grounding, meta_function_diff, tactis_six_dim, 5min_falsifier, venue_fit, publishability_score
- Only ≥7 go into main flow; lower-score kept for cross-idea recycling
- Rationale: low-score gaps in one context may become high-value in a different framing

### 3.4 Venue-Aware Experiment Design (§O)

Three distinct Stage 9 output schemas:
- **A会** (NeurIPS/ICML/ICLR): problem_formulation.md (P(z|x,y_w,b)), closest_prior_MDS.yaml, renaming_check.md, ablation_matrix.yaml (≥4 including AB-5), dual_metric_protocol.md, cross_validation_plan.md (≥2 tasks + ≥2 model pairs), proposition.md (≥1 formal claim), reproducibility_checklist.md, tactis_audit.md, negative_science_report.md
- **ESWA**: application_scenario.md, algorithm_modules.md, thick_experiments.yaml (≥3 datasets, ≥8 baselines), sensitivity_analysis.md, statistical_significance.md (p-value/CI)
- **Information Fusion**: fusion_formulation.md, multi_source_design.md (≥2 weak supervisors), fusion_operator.md with complexity analysis, incomplete_imprecise_handling.md

### 3.5 RalphLoop Artifact Verification Protocol (`methodology/RalphLoop.md`)

Mandatory event ordering per iteration:
```
narrative_check → T2_pass → methodology_analysis → causal_analysis → module_invocations → promotion_*
```

Field-level verification schemas for each artifact:

| Artifact | Critical field check |
|---|---|
| narrative_check | narrative_score must be float; must exist |
| T2_pass | idea_id must NOT be null (provenance break if null) |
| methodology_analysis | hypothesis_compiled must be True |
| causal_analysis | predicted_chain must NOT contain "learning_dynamics" (hardcoded mediator = FAIL) |
| module_invocations | all 9 modules must have called_count ≥1 (proves import has runtime call) |
| promotion_decision | claim_string non-empty; check_outcomes non-empty dict; idea_id matches T2_pass |

### 3.6 program.md Contract Pattern (`beatless-research/sota-templates/`)

Per-niche execution contract with these mandatory sections:
```markdown
## Goal
- Metric, direction, current SOTA, stop criterion (score threshold OR iter count OR wallclock)

## Niche directive
<1 paragraph: which specific SOTA failure mode this niche attacks, why it's a gap>

## Forbidden APIs (HARD — violation = iter rejected)
<specific forbidden operations, enforceable from train.py source text>

## Mandatory priors (HARD — checkable in train.py source)
<must-use components, must-report output fields>

## Hardware budget
<GPU, per-iter wallclock, total wallclock, VRAM ceiling>

## Diversity constraint
<cosine similarity check vs other niches; threshold; reject rule>

## Output format (each iter)
<structured output that wave scheduler parses into results.tsv>

## File contracts
| File | Mutable? | Owner |
## Anti-cheat reminders
<explicit list of what counts as leakage vs baseline fairness>
```

This contract pattern ensures agents operate on an unambiguous specification that can be reviewed and audited.

---

## 4. Reusable Artifacts — Quoted Prompts, Templates, Rubrics

### 4.1 Knowledge-Dump Protocol Prompt (R-HET-4)

From `beatless-research/REFACTOR-PLAN-v2.md §3.3`:

```
在回答前, 先用 schema=[item, confidence, source, why_relevant]
列出你关于该 topic 已知的 ≥30 条信息 (含失败的 / 被推翻的 / 小众的 /
confidence=low 的). 禁止只列 top-cited 5-10 项.
```

The English equivalent for our use:
```
Before answering, first dump ALL you know about this topic using schema:
[item, confidence, source, why_relevant]. List ≥30 items including:
failed/disproven results, low-confidence hunches, minority positions.
FORBIDDEN: listing only top-cited 5-10 items.
```

**Why to lift this**: LLMs default to listing consensus top-5. This forces the long tail of dark knowledge into the visible context before reasoning begins.

**File**: `/home/lingxufeng/research/beatless-research/REFACTOR-PLAN-v2.md` §3.3 R-HET-4

### 4.2 Implicit Block Template (Principle 3)

From `methodology/plan/Regulations.md`:

```yaml
explicit:
  reasoning_trace: "<what you wrote/ran/observed in this cycle>"
  result: "<metric delta / decision / commit SHA>"

implicit:
  silent_priors: |
    <premises taken for granted but not requested by prompt.
     e.g. "I assumed batch_size doesn't affect this comparison because...">
  unspoken_alternatives: |
    <options considered but not tried + HONEST technical reason why.
     e.g. "Did not try LoRA rank=64 because I felt rank=16 was enough;
     basis for that intuition: ...">
  failure_dna: |
    <root cause one layer deeper than the commit message.
     "Surface reason is X, but more likely Y, because I didn't follow thread Z">
  hidden_dependencies: |
    <environmental premises prompt didn't ask about: seed, CUDA version,
     driver, undocumented upstream data property, race condition reviewer missed>
  what_a_skeptical_PI_would_ask: |
    <3 hardest questions you least want to answer, with honest initial answers>

evidence_pointers:
  - "<file:line | log line | commit SHA | dataset key — one per implicit field>"
```

**File**: `/home/lingxufeng/research/methodology/plan/Regulations.md`

### 4.3 Renaming Detector Prompt

From `beatless-research/rules/constitution/v1.0.4-draft.yaml §N gate_2`:

```
anti_rebrand_self_check:
  - "List ≥5 existing concepts that are essentially identical to this proposal (draw from the 20 meta-functions library)"
  - "Give pseudocode line diff ≥3 lines (our method vs each existing_i)"
  - "Design a 5-minute mechanism-separation experiment:
     if our method and the most similar existing method are run on the same synthetic data,
     what specific quantitative divergence would prove they are mechanistically different?"
```

**File**: `/home/lingxufeng/research/beatless-research/rules/constitution/v1.0.4-draft.yaml`

### 4.4 Negative Science Audit Block

From `constitution/v1.0.4-draft.yaml §M`:

```yaml
negative_science_audit:
  tools:
    NS-1: "Information lower-bound prover: What is the theoretical performance ceiling?
           How far is current SOTA from that ceiling?
           If SOTA is near ceiling → reassess project value"
    NS-2: "Topology obstacle analyzer: Is the target property mathematically possible?
           Does it violate topological invariants? If yes → this path is closed, ABORT"
    NS-3: "Computational complexity evaluator: Is there a known NP-Hard barrier?
           If yes → switch to approximation or heuristic"
    NS-4: "Hardware constraint simulator: Can the design achieve performance on target hardware?
           If over budget → simplify before writing a single line of code"
```

**File**: `/home/lingxufeng/research/beatless-research/rules/constitution/v1.0.4-draft.yaml`

### 4.5 Final Explainability Test Template (§Q)

```
"I achieve <meta_function from the 20-element library> via <method/component>,
 grounded in <primal_axiom from 10-element list>,
 solving <specific problem>."

Examples:
- "I build a gradient highway (MF-03, P-PHY-2) via residual connections, solving deep network degradation."
- "I compute all-position relationships in parallel (MF-01, P-MATH-4) via self-attention, breaking RNN serial bottleneck."
```

**File**: `/home/lingxufeng/research/methodology/Idealation.md` §3.2

### 4.6 AConferenceIdeaScore Priority Formula

From `methodology/V19_PARADIGM_VISION.md`:

```
priority = SOTA_gap
         + anomaly_severity
         + axiom_tension
         + mechanism_identifiability
         + transfer_potential
         - engineering_complexity
         - evidence_debt
```

Use this to rank competing hypotheses in the Arbor idea tree; negative terms prevent proposing complex-but-cheap-to-build ideas.

### 4.7 Heterogeneity Rules (Multi-Engine Isolation Contract)

From `beatless-research/REFACTOR-PLAN-v2.md §3.3`:

```yaml
R-HET-1: writer != reviewer
  - producer = Opus    → reviewer ∈ {Codex, Gemini}
  - producer = Sonnet  → reviewer ∈ {Codex, Opus}
  - producer = Gemini  → reviewer ∈ {Codex, Opus}

R-HET-2: Stage 8 three-engine parallelism (HYPOTHESIS_GEN)
  Launch simultaneously:
    - Opus: primary proposal (metacognitive + axiom-aligned + multi-round deepening)
    - Gemini: first-principles proposal (derive from 10 axioms)
    - Codex: attack-vector only (1 call, give 1-3 adversarial perspectives, stop)

R-HET-3: Model boundary constraints (hard)
  - Gemini: forbidden from retrieval/search/code review (hallucination too high)
  - Kimi: forbidden from reasoning/evaluation
  - Codex review role: not responsible for "hypothesis was wrong" backstop (that's bounce-back to Stage 8)
```

---

## 5. Command / Skill Candidates

| Name | 1-line purpose | Trigger | Engine |
|---|---|---|---|
| `/axiom-ground` | Force-ground a mechanism claim to ≥1 of 10 first-principles axioms; output the final-explainability sentence | Before any hypothesis is logged to Arbor tree | Opus (reasoning quality) |
| `/operator-transform` | Apply one or more of 12 Operator Algebra Transforms to an existing idea; produce a diversified variant set | During IDEATE cycle when "direction clear, design unsatisfying" | Opus → then GPT-5.5 Pro for deep scheme |
| `/renaming-detector` | Run Gate 2: list ≥5 closest concepts from the 20-element meta-function library + ≥3-line diff vs each; stamp RENAMING_SUSPECT or CLEAR | After any hypothesis is generated, before Arbor node is promoted | Codex (code-level diff reasoning) |
| `/neg-science-audit` | Run the 4 negative-science tools (information lower bound / topology / NP-hard / hardware); ABORT if any blocks | Before DISPATCH gate, replacing manual feasibility check | Opus (mathematical reasoning) |
| `/implicit-surface` | Force generator to produce the structured implicit block (silent_priors / unspoken_alternatives / failure_dna / hidden_dependencies / skeptical_PI_questions) | End of every IDEATE or OBSERVE step | Same engine as generator (self-audit) |
| `/boundary-map` | Given a method that shows improvement, scan capability boundary on axes: input length / noise / frequency / depth / scale; produce BoundaryMap artifact | After first positive result in experiment cycle | Opus subagent in worktree |
| `/knowledge-dump` | Force KNOWLEDGE-DUMP pre-step: dump ≥30 items on topic with confidence + source before reasoning | Start of any research analysis step where priors matter | Same engine as primary reasoner |
| `/artifact-checklist` | Verify 7 mandatory pre-GPU artifacts are complete; gate on any missing | Before DISPATCH (before any GPU experiment) | Codex (checklist review) |
| `/orthogonal-niche-split` | Given a hypothesis, decompose into ≥3 orthogonal attack niches (cosine-overlap <0.6); produce program.md contract per niche | When translating a hypothesis into executable experiments | Opus (structure) → user reviews |
| `/acoscore` | Compute AConferenceIdeaScore (min-form across 10 dimensions) for a candidate idea; surface the bottleneck dimension | After hypothesis generation, before SELECT | Codex (structured scoring) |

---

## 6. NEW vs Our Kernel

### Genuinely NEW — ADOPT

**1. Five-Tuple Idea formalism** (`Silent_Axiom, Anomaly, Mechanism_Variable, Operator_Rewrite, Killer_Experiment`)
Our kernel has a 5-field MechanismHypothesis (`silent_axiom→mechanism→hypothesis→observable→falsifier`) which is close, but the beatless formalism is sharper: it demands an explicit *Anomaly* (a real observed failure that motivated the idea — not just a logical gap) and an *Operator_Rewrite* (a code-diffable change). Our "mechanism→observable" is logically correct but can be filled with vague text. The five-tuple forces concrete commitments.

**2. 12 Operator Algebra Transforms**
We have no systematic ideation vocabulary. The 12 transforms give our loop a closed set of "idea moves" — when IDEATE stalls, apply Axis Rotation or Fixed-to-Adaptive and get a structurally distinct variant. For the DiffusionGemma direction specifically: Explicit-to-Latent (CoT → latent loop), Dense-to-State (discrete tokens → continuous embedding state), and Scalar-to-Field (loss scalar → gradient/velocity field) are directly applicable.

**3. Surface Implicit Knowledge protocol (Principle 3 + R-HET-4 Knowledge-Dump)**
Our kernel says "evidence≠memory" and "generator/critic/selector ISOLATION" but does not prescribe how to elicit the hidden priors that drive reasoning. The structured `implicit` block — especially `failure_dna` and `what_a_skeptical_PI_would_ask` — is a mechanical anti-sycophancy tool we are missing. The Knowledge-Dump pre-step (≥30 items including confidence=low) is orthogonal to our L1 "skeptical default" and addresses a different failure mode (selective recall, not selective framing).

**4. Renaming Detector gate (≥5 concepts + ≥3-line diff)**
Our kernel has "falsifiability-first" and implicitly guards against rebrand but provides no mechanical threshold. The ≥5-concept + ≥3-line diff requirement is operational: it can be run as a Codex task and produces a verifiable artifact. For DiffusionGemma: MeanFlow / JiT / pMF / ELF are exactly the 4-5 closest concepts; a formal diff against each would sharpen our novelty claim without relying on GPT-5.5 Pro alone.

**5. Mandatory BoundaryMap artifact**
We seal eval but don't systematically map where the method fails. The BoundaryMap (axes: input length, noise, frequency, depth, scale) converts a binary "method works/doesn't" into a coordinate system. For DiffusionGemma this means: at what conditioning strength / noise level / sequence length does the gradient-field approach degrade? This is needed for the paper anyway.

**6. Parallel Orthogonal Coverage (Principle 1, cosine-overlap enforcement)**
Our Arbor tree tracks multiple nodes but does not enforce orthogonality. Two nodes can be essentially identical framings. The cosine-overlap <0.6 check (applied to one-sentence niche summaries) and the entropy collapse rule (R11: if ≥2 niches converge to same change, force reassign) are cheap to add to the tree discipline.

**7. Token-Preserving Ablation gate (AB-5 shuffled_perfect_structure)**
Our L2 kernel says "score improvement alone never confirms a mechanism" but doesn't specify how to test it. The AB-5 ablation (shuffled version of our method that preserves tokens/structure but scrambles order/role) is the decisive test. If AB-5 ≈ AB-3 (our method), we are adding rationale supervision, not structure. This is directly applicable to DiffusionGemma embedding-flow work: shuffle the gradient-field conditioning and see if performance holds.

**8. Cognitive Debt Dashboard + GhostVarTracer**
We track hypothesis status in the Arbor tree but not: (a) unclosed risk items with age; (b) pending falsifier experiments; (c) anomalies that expired without follow-up; (d) environment variable confounders (CUDA version, dataloader order). The ghost variable tracker is especially relevant for diffusion experiments where checkpoint shard bugs (our Jun24-26 incident) are exactly "hidden_dependencies" that contaminate results.

**9. HypothesisBranch version control (main/experiment branches with divergence point tracking)**
Our RUNLOG is chronological but flat. The branch metaphor (each alternative hypothesis is a branch with a declared divergence point from the main causal chain, either merged or archived with failure reason) is cleaner for multi-directional exploration.

**10. AConferenceIdeaScore (min-form) and Priority Formula**
We have no formal scoring of competing hypotheses before SELECT. The min-aggregation prevents strong-story/weak-mechanism ideas from winning selection. The priority formula's negative terms (engineering_complexity, evidence_debt) counterbalance the positive terms in a way our current Arbor tree does not.

### OVERLAPS — Already Covered

- 10 First-Principles Axioms: our "silent_axiom" field implicitly uses the same physics/math/information taxonomy; we have the axiom list in our Idealation reference
- TACTIS checklist: we reference this in our architecture review but don't enforce it mechanically (could be promoted to a hard gate)
- Negative Science 4 tools: our "failure must shrink the search space" L2 kernel covers the spirit; the 4-tool formalism is slightly more concrete (topology obstacle / NP-hard / hardware bounds) — worth formalizing
- Multi-engine isolation (Opus generates / Codex selects / GPT-5.5 novelty): our L3 multi-engine routing does this; the `R-HET-1/2/3` rules are a formalized version of what we already do informally
- One-variable ablation discipline: our "one-variable + negative-control + locality" L2 kernel covers this
- Score ≠ mechanism: explicit in our L2 kernel
- Sealed eval/test: explicit in our L2 kernel ("eval scripts / test sets / baselines are sealed")
- Falsifier-before-build: explicit in our L1 cognitive loop

### SKIP — Not Applicable

- Specific benchmark program.md templates (TSB-AD, GADBench, MolPCBA, OpenOOD-IN200): domain-specific SOTA-chasing templates, not relevant to dLLM research
- Kimi CLI integration and ACP session pool implementation: infrastructure detail tied to their toolchain, not ours
- GPU discipline rules (CUDA_VISIBLE_DEVICES, nvidia-smi pre-check, wave scheduler): already handled by our env; not in the methodology layer
- Stage 4 literature collect specifics (Kimi DR multi-source): we use GPT-5.5 Pro via Playwright; different toolchain
- PPTX/paper writing Stage 16-23: explicitly deprecated in their own docs
- Docker isolation details: they moved to working-dir isolation anyway

---

## 7. Top-3 Highest-Value Takeaways

### Takeaway 1: The Implicit Block is the Missing Anti-Sycophancy Layer

Our L1 "skeptical default" and L3 "generator/critic/selector isolation" operate on *explicit* outputs. But sycophancy and reward hacking live in *implicit* priors: what the generator assumed but didn't state, what alternatives it considered but suppressed, what environment dependencies it didn't mention. The structured `implicit` block (especially `failure_dna` and `what_a_skeptical_PI_would_ask`) creates a mandatory evidence trail for reviewers to challenge the generator at the right depth. Lift the template verbatim into our OBSERVE and IDEATE steps. Cost: adds ~300 tokens per cycle. Value: catches the class of failures our current L2 "evidence≠memory" kernel does not reach.

### Takeaway 2: BoundaryMap + AB-5 Ablation as the Two Minimal Pre-Paper Experiments

For our DiffusionGemma embedding-flow direction, we will eventually need to answer: (a) when does the gradient-field target fail? (b) is the performance gain from structure or just from more supervision tokens? Both questions can be answered by running exactly the BoundaryMap scan and the AB-5 shuffled-condition ablation. These are not overhead — they are the two experiments that distinguish a publishable claim from an interesting engineering demo. Adopt both as hard gates in the Arbor DISPATCH checklist immediately.

### Takeaway 3: Five-Tuple + 12 Transforms as the Productized Ideation API

Our `/ideate` equivalent currently produces free-text hypothesis descriptions. Requiring each idea to fill the five-tuple (Silent_Axiom, Anomaly, Mechanism_Variable, Operator_Rewrite, Killer_Experiment) and to name the Operator Transform used (one of 12) converts ideation from creative writing into a structured commitment. The Operator Algebra also provides a finite search space for GPT-5.5 Pro redesign prompts: instead of "redesign the gradient-field approach," we can say "apply Fixed-to-Adaptive and Scalar-to-Field transforms to the current MeanFlow-style target and propose 3 specific operator rewrites." This makes the Pro routing calls more precise and the outputs more comparable.
