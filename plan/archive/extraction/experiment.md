# Extraction: Experiment Repo Methodology
Extracted: 2026-06-29
Source: `/home/lingxufeng/agent/Experiment` (602 MB Bash-driven research harness)
Audience: DiffusionGemma autonomous research loop; compare against existing L1/L2 kernel

---

## 1. What It Is

Experiment is a Bash-driven autonomous research harness built around a shared blackboard of JSON artifacts. Every research decision — hypothesis, probe design, result, negative finding, claim — is a machine-readable JSON file with a schema, SHA-256 hash, and declared downstream consumer. The core thesis, stated in `CLAUDE.md`, is: **"autonomous research loops become more reliable when failures are converted into observable mechanism variables before code mutation."** The pipeline spine is `FailureCase → FailureCluster → MechanismHypothesis → ProbePlan → ProbeResult → NegativeCase/Evidence → ClaimEvidenceTable → PromotionPacket`. The V4 upgrade adds an abductive reasoning layer: `ArchitectureDeductionMap → DesignIntentReconstruction → AbductiveSearchTree → AbductiveExplanationSet → DeductivePrediction` before the experiment execution. A four-role Codex Meta-Auditor layer (Orchestration / PromptPath / CLI / Evidence) continuously audits the harness itself, producing JSON findings that are advisory only.

---

## 2. Core Methodology / Workflow Spine

### Phase 0-3: Failure-to-Hypothesis

```
FailureCase          — concrete, content-addressable failure (metric + localization + sha256)
  → FailureCluster   — group by causal signature
  → MechanismHypothesis — 5-question format; MUST answer all 5 or it is only a "module idea"
  → ProbePlan        — minimal falsification experiment; single changed variable; run command
  → ProbeResult      — bash-deterministic decision; LLM interpretation is optional/non-binding
  → NegativeCase     — first-class research output; must shrink search space ≥2 items
  → ClaimEvidenceTable — living document; SHA256 of every supporting artifact
  → PromotionPacket  — final gate; tiered by claim_mode
```

### V4 Full Reasoning Lane (under construction)

```
ArchitectureDeductionMap        — understand the target repo before touching it
  → DesignIntentReconstruction  — reverse-abduce why baseline was designed this way
  → AbductiveSearchTree         — persistent auditable tree of competing hypotheses
  → AbductiveExplanationSet     — ≥3 candidate mechanisms per failure cluster; each with falsifier + discriminating probe
  → DeductivePrediction         — "If M under C, observable O moves direction D by threshold T, control K does not move"
  → ProbePlan / BenchmarkSpec
  → ProbeResult / BenchmarkResult
  → InductivePattern            — summarize patterns across ≥2 results (scope + exceptions + claim boundary)
  → ClaimEvidenceTable
  → PromotionPacket / RecipeNote
```

### Multi-Engine Role Assignment

From `CLAUDE.md` and `blackboard/MANIFEST.md`:

| Role | Engine | Contract |
|------|--------|----------|
| Diverge / generate mechanisms | Gemini | isolated per lens; prevent lens convergence |
| Veto / audit / reward-hacking check | Codex (`CODEX_ROLE=evidence_audit`) | cold-read; isolated per review |
| Orchestration audit | Codex (`CODEX_ROLE=orchestrator_audit`) | checks bash ordering, gate emission, stale state |
| Converge / orchestrate | Claude Opus | isolated |
| Execute / patch | Claude Sonnet | isolated per patch |
| Synthesize long context | Kimi | `shared_readonly` allowed |
| Router / scheduler | MiniMax | `long_lived_router`; no semantic votes |

**SessionContract hard rule (file: `docs/SESSION_CONTRACT.md`):**
> "Same session CANNOT serve both producer AND reviewer of the same artifact."
> "All shared info between dispatchers MUST be written as a blackboard artifact."

---

## 3. Experiment Standards / Specs

### 3.1 claim_mode Tier System

Every artifact from probe design through promotion carries a `claim_mode` field that gates controls and reviewer count:

| claim_mode | Goal | Controls required | Reviewers | Verdict vocab |
|------------|------|-------------------|-----------|---------------|
| `score_recipe` (T0) | honest score / replication | execution_verification + ≥1 falsifier | 1 (owner or Codex role) | `recipe_accepted` |
| `mechanism_probe` (T1) | mechanism discovery | T0 + negative_control + locality + counterfactual | 2 (cross-family) | `mechanism_supported` |
| `paper_claim` (T2) | paper-bound promotion | T1 + holdout + cross-subject + variance (3 seeds) + novelty_check | 3 (D-C-S quorum) | `promotion_candidate` |

Explicit rule (`prompts/artifact_promotion.md`): "Do NOT auto-upgrade `claim_mode`. If a result only meets recipe rules, ship it as `recipe_note`, not as a stripped-down `paper_claim`."

### 3.2 Probe Validity Gates

From `prompts/artifact_probe_plan.md`:
- Single changed variable rule: `intervention.changed_variable` is exactly one variable; multi-variable changes are ablation studies, not falsification probes.
- `question` field must include "more than", "differs from", or "exceeds" — otherwise not falsifiable (auto-reject).
- `result_that_falsifies[]` must include numeric or comparative thresholds (≥1 at T0, ≥3 at T1/T2).
- `required_probes` must come from a closed 6-set: `sensitivity_probe | locality_probe | counterfactual_probe | negative_control | equal_compute_control | variance_probe`. Novel probe types escalate to owner.
- T0 tier first: for a new mechanism, always propose T0 (cheapest probe). T1/T2 only after T0 supports.

**Execution verification anti-no-op (cycle-2 lesson, encoded in schema):**
Every probe must specify `execution_verification.log_assertion`: a regex run against the retrain/eval log that MUST match if the intervention executed. If no match → `decision` auto-downgrades to `implementation_bug` regardless of metric delta. This is the critical "silent patch failure" guard.

### 3.3 Forbidden Files Gate

From `bin/validate_intervention.sh`:
```
G4: forbidden_file_globs MUST include eval.py, tests/**, baseline_psnr
G5: must_fire_assertion required if intervention_class != no_change
```
Result: the eval script, test set, and baseline are sealed; no agent may touch them.

### 3.4 Reward-Hacking Checklist

Every `ProbeResult` carries:
```json
"reward_hacking_checks": {
  "metric_visual_mismatch": "pass | fail | skipped",
  "target_region_not_moved": "pass | fail | skipped",
  "subject_overfit": "pass | fail | skipped",
  "holdout_regression": "pass | fail | skipped",
  "eval_path_tampering": "pass | fail | skipped"
}
```
Rule: `decision=support` with any `reward_hacking_checks.*=fail` → forced flip to `reject` by Codex audit gate.

### 3.5 NegativeCase Discipline

From `prompts/artifact_negative_case.md`:
1. `what_was_ruled_out[]` must have ≥2 items — "If only 1, the probe was too ambiguous; downgrade to `inconclusive`, not `reject`."
2. `remaining_alternatives[]` must be non-empty — if no alternative survives, the cluster itself is wrong; escalate.
3. `future_retry_condition` must name a specific new observable (not "if we get more data").
4. `next_recommended_probe` routes toward an un-tested alternative mechanism from the source hypothesis.

Anti-patterns (auto-reject): `what_was_ruled_out` empty, `future_retry_condition: "more research needed"`, disconfirmed mechanism restated as a metric failure rather than a causal claim.

### 3.6 ContextBundle: File-Based Context Handoff

Schema: `schemas/context_bundle.schema.json`. Every dispatcher that calls a CLI must prepend a ContextBundle to the prompt.

```json
{
  "bundle_id": "bundle_<slug>",
  "run_id": "<links to ExperimentRunManifest>",
  "must_read": ["<path>", "..."],          // agent MUST read these
  "input_hashes": {"<path>": "sha256:<64hex>"},  // stale detection
  "short_context": "<1-3 sentence goal summary>",
  "forbidden_assumptions": ["<explicit anti-patterns>"],
  "recent_negative_cases": ["<paths to ruled-out mechanisms>"]
}
```

If ContextBundle is missing → LLM must stop and return `{"error":"missing_context_bundle"}` rather than hallucinating.

### 3.7 Invocation Header (universal prompt header)

Every prompt file in `prompts/` begins with the same invocation header block (`<!-- INVOCATION_HEADER_PIPE_028 -->`):
```
1. Goal source of truth: locate ContextBundle block appended after this prompt.
2. Hard rules: do NOT repeat negative_cases; do NOT violate forbidden_assumptions; MUST cite ≥1 must_read path in provenance.
3. Downstream contract: your JSON is consumed by <specific dispatcher>. Field names matter; do not rename keys.
```

### 3.8 IdeaSeed / IdeaCritic Filter

`prompts/artifact_idea_seed.md`: produce ≤7 ranked ideas, each with:
```
kind: param_tweak | training_recipe | code_operator | architectural | data_augmentation
convertible_to_mechanism: bool
novelty_vs_prior_art: low | med | high
```
Must not: propose patches, exceed 7 ideas, repeat NegativeCases, propose paper-level claims.

`prompts/artifact_idea_critic.md` (Codex, low-cost filter): for each idea, audit:
1. Experimentable today within budget?
2. param_tweak masquerading as mechanism?
3. Convertible to FailureCase / MechanismHypothesis pair?
4. Overlaps with known NegativeCase?
Output: `{verdict: accept|revise|reject, convert_target, blocking_overlap}`.

---

## 4. Reusable Artifacts — Quoted Prompts, Templates, Rubrics

### 4.1 MechanismHypothesis 5-Question Hard Rules
Source: `prompts/artifact_mechanism_hypothesis.md`

```
A hypothesis MUST answer all 5 questions. If any is missing, the artifact
is **only a module idea**, not a research hypothesis:

1. What is the mechanism variable? → `mechanism_variable.name + definition`
2. How can it be observed? → `mechanism_variable.how_to_observe[]` (≥3)
3. Which probe would support it? → `required_probes[]` (≥2 from closed set)
4. Which result would falsify it? → `falsifiers[]` (≥3)
5. What are the alternative mechanisms? → `alternative_mechanisms[]` (≥3)
```

Extra rules:
- `intervention.name` must be concrete ("Add boundary-mask reweighting in renderer output L2 with coeff α∈[0.5,2.0]"), not generic verbs ("improve loss").
- `falsifiers` must be negative observations: "If Y is observed, the mechanism is wrong" — not "we will test X".
- Status starts at `proposed` for diverge stage; Codex (or owner) promotes to `ready_for_probe`.

### 4.2 DeductivePrediction Template
Source: `schemas/deductive_prediction.schema.json`

```json
{
  "kind": "deductive_prediction",
  "prediction_id": "pred_<slug>",
  "if_mechanism_true": "<claim that follows>",
  "condition": "<experimental condition>",
  "intervention": "<what we change>",
  "expected_observation": {
    "metric": "<metric_name>",
    "direction": "> | < | >= | <= | == | !=",
    "threshold": "<numeric or formula>"
  },
  "required_control": "<control condition or null>",
  "falsified_if": "<one sentence>"
}
```
Companion `PredictionOutcome` (lives in ProbeResult):
```json
{
  "kind": "prediction_outcome",
  "prediction_id": "<links to DeductivePrediction>",
  "observed_value": <number|string|null>,
  "control_value": <number|string|null>,
  "outcome": "supported | falsified | inconclusive | not_measured",
  "evidence_refs": ["<path>"]
}
```

### 4.3 ContextBundle Invocation Header (copy-paste for any prompt)
Source: `prompts/artifact_mechanism_hypothesis.md` header block

```markdown
> **Invocation Header** (read this BEFORE producing output)
>
> 1. **Goal source of truth**: locate the `## ContextBundle (must consume)`
>    block appended AFTER this prompt. It carries `short_context`,
>    `forbidden_assumptions`, `recent_negative_cases`, and `must_read` digest.
>    If that block is missing → STOP and return `{"error":"missing_context_bundle"}`.
> 2. **Hard rules**:
>    - Do NOT repeat any failure listed in `recent_negative_cases`.
>    - Do NOT violate any item in `forbidden_assumptions`.
>    - Your output MUST cite at least one `must_read` path in its provenance field.
> 3. **Downstream contract**: your JSON output is consumed by
>    **<specific downstream dispatcher>**. Field names matter — do not rename keys.
```

### 4.4 ClaimEvidenceTable claim_type Taxonomy
Source: `prompts/artifact_claim_evidence.md`

| claim_type | When to use | Evidence requirement |
|---|---|---|
| `observation_claim` | reporting failure / metric pattern | FailureCase or per_frame metrics |
| `mechanism_claim` | claiming X mediates Y | requires falsifiers AND controls |
| `intervention_claim` | claiming patch P helps cluster C | requires ProbeResult |
| `robustness_claim` | claiming holds across subjects/seeds | requires transfer or variance evidence |
| `efficiency_claim` | claiming equal quality at less compute | requires equal-quality OR equal-compute comparison |
| `negative_result_claim` | claiming X does NOT help | requires NegativeCase |
| `limitation_claim` | acknowledging boundary of method | MUST NOT be deleted to weaken story |

### 4.5 SessionContract Per-Role Isolation Table
Source: `docs/SESSION_CONTRACT.md`

| Agent type | Session policy | Rationale |
|---|---|---|
| Gemini idea / mechanism lens | `isolated` per lens | Prevent lens convergence into one story |
| Codex reviewer / auditor | `isolated` per review | Cold-read artifacts, no producer framing |
| ClaudeCode patch implementor | `isolated` per patch | Each patch is independent unit-of-work |
| Kimi long synthesis | `shared_readonly` allowed | Long-context distillation needs accumulated reads |
| Router / scheduler | `long_lived_router` allowed | Routing decisions only, no scientific judgment |
| Promotion selector | `isolated` | Selection cannot be biased by prior framing |

### 4.6 Probe Anti-Patterns (auto-reject checklist)
Source: `prompts/artifact_probe_plan.md`

```
- question without "more than" / "differs from" / "exceeds" — not falsifiable
- expected_result_if_true empty — no prediction = no science
- result_that_falsifies < 1 item (T0) / < 3 items (T1+) — too easy to escape
- controls.negative_control: "none" at T1+ — every mechanism_probe needs a negative
- runtime_budget.max_minutes > 180 for T0 — too expensive to fail
- claim_mode missing or invalid — gate strength is undefined
- Calling something mechanism_probe while skipping T1 controls
```

### 4.7 AbductiveExplanationSet Minimum Gate
Source: `schemas/abductive_explanation_set.schema.json`

Per gate L1219-1224: must name ≥2 alternative explanations; for each:
- `explains[]` — what it accounts for
- `does_not_explain[]` — what it cannot account for
- `distinguishing_probe` — probe ID that separates this from top alternative
- `status: alive | downweighted | ruled_out`
- `downweight_reason` — required when status != alive
- `next_best_discriminator` — probe that separates the top-two alive explanations

### 4.8 Sidecar Evidence Boundaries
Source: `CLAUDE.md` §"Sidecar Evidence Boundaries"

```
agentmemory: May recall decisions, rejected branches, prior context.
  It is NOT evidence. Recalled facts must re-link to artifacts before claims.

Local Deep Research / browser: May produce SourceTrace, PaperCard, DatasetCandidate.
  Raw retrieval is NOT evidence until SourceVerificationGate passes.

Academic Research Skills: Provide gate patterns. These become verifier gates or
  artifact fields, NOT separate agents.
```

---

## 5. Command / Skill Candidates

These are discrete units that map cleanly to `/ideate`-style skills:

| Candidate | 1-line purpose | Trigger | Engine |
|---|---|---|---|
| `/idea-seed` | Generate ≤7 ranked experiment ideas from current best result + failure state | After negative result or stale loop | Opus (with ContextBundle pre-check) |
| `/idea-critic` | Filter idea list: experimentable? mechanism-convertible? NegativeCase overlap? | After `/idea-seed` emits | Codex (evidence_audit role) |
| `/mechanism-build` | Convert FailureCluster to ≥3 competing MechanismHypotheses with falsifiers | After cluster formation | Gemini (diverge) + Codex (veto) |
| `/probe-design` | Convert one MechanismHypothesis to minimal ProbePlan (T0 first; single changed variable; log_assertion) | After mechanism selected | Codex (orchestrator_audit) |
| `/negative-register` | Convert rejected ProbeResult to structured NegativeCase shrinking search space ≥2 items | On probe rejection | Codex (evidence_audit) |
| `/claim-check` | Audit active claims: sha256 valid, negative controls present, claim_mode honest, no silent no-ops | On promotion request | Codex (evidence_audit) |
| `/context-bundle` | Build and inject ContextBundle (short_context, forbidden_assumptions, recent_neg_cases, sha256 hashes) before any LLM call | Pre-dispatch; always | Bash + Opus |
| `/deductive-predict` | Convert AbductiveExplanationSet node to DeductivePrediction (observable + direction + threshold + control) | After mechanism selected for probing | Codex (prediction-writer role) |
| `/inductive-pattern` | Summarize patterns across ≥2 probe results (scope, exceptions, claim boundary) | After ≥2 ProbeResults available | Codex (evidence_audit) |
| `/session-contract` | Enforce isolation: producer ≠ reviewer; assign session_policy per agent role | Before any multi-engine dispatch | Bash validator |

---

## 6. NEW vs Our Kernel

### NEW — Adopt

**1. ContextBundle as mandatory LLM pre-flight (`schemas/context_bundle.schema.json`)**
We have no equivalent. Every LLM call in our Arbor loop can use session memory from prior turns, which causes the "proposing already-ruled-out directions" failure mode. The ContextBundle fix: build an explicit JSON with `short_context`, `forbidden_assumptions`, `recent_negative_cases` (paths to NegativeCase artifacts), and `must_read` (paths with sha256 for stale detection). Prepend it to every LLM call. If missing → stop with error, not hallucination. Direct adoption for DiffusionGemma: any call to Opus/GPT-5.5-Pro should include a ContextBundle listing the ruled-out DiffusionGemma directions and must-read prior-art files.

**2. claim_mode tier system (`prompts/_README.md`, `prompts/artifact_promotion.md`)**
Our kernel has "score≠mechanism" but no formal tier with escalating control requirements. This system adds: `score_recipe` (T0, recipe-level, 1 reviewer), `mechanism_probe` (T1, locality+negative_control mandatory), `paper_claim` (T2, cross-subject variance + novelty check). Explicit upgrade-blocker: "Do NOT auto-upgrade claim_mode." Directly adoptable for our gradient-field direction — our SFT experiments produce recipe-level results; we should formally label them T0 and not treat them as mechanism claims.

**3. NegativeCase as first-class structured output (`prompts/artifact_negative_case.md`)**
We record failures but don't formalize them. The Experiment pattern: every rejection must name (a) ≥2 things ruled out, (b) ≥1 surviving alternative, (c) concrete retry condition (specific new observable, not "more data"), (d) next_recommended_probe. This converts each failure into search-space reduction. Directly adoptable for DiffusionGemma: when a training direction fails, write a structured NegativeCase before moving to next direction.

**4. Execution verification anti-no-op (`prompts/artifact_probe_plan.md` §cycle-2 lesson)**
Every probe declares `execution_verification.log_assertion` — a regex that MUST match in the training log to prove the intervention fired. If no match → auto-downgrade to `implementation_bug`. This is critical for diffusion training where e.g. a loss weight override can silently be ignored by Trainer's config merge. We have no equivalent guard.

**5. IdeaSeed → IdeaCritic two-step filter (`prompts/artifact_idea_seed.md`, `prompts/artifact_idea_critic.md`)**
Producer generates ≤7 ranked ideas with `convertible_to_mechanism: bool` and `kind` enum. Critic filters for: budget feasibility, mechanism-convertibility, NegativeCase overlap. The ≤7 cap on IdeaSeed is a concrete swarm-noise guard we do not currently enforce. The `kind` enum (param_tweak | training_recipe | code_operator | architectural | data_augmentation) cleanly separates score-seeking from mechanism work.

**6. AbductiveExplanationSet with ≥3 competing explanations (`schemas/abductive_explanation_set.schema.json`)**
Our Arbor tree tracks directions but doesn't enforce ≥3 competing causal explanations per failure node. The AES requirement: each cluster must have ≥2 candidate mechanisms, each with `distinguishing_probe` that separates it from the next-best alternative. Prevents "easiest patch over best explanation" bias. For DiffusionGemma Track 2: when a gradient-field intervention fails, we should generate ≥3 competing causal explanations before pivoting.

**7. MechanismAnalogMap schema (`schemas/mechanism_analog_map.schema.json`)**
Formalized cross-domain transfer: target_failure_ref, adjacent_mechanism_ref, isomorphism_argument, adaptation_constraints[], strength_score [0,1], counter_arguments[]. Our cross-domain mapping (e.g. "JiT/MeanFlow to frozen dLLM") is prose-only. A structured MechanismAnalogMap with isomorphism_argument and counter_arguments would strengthen novelty claims.

**8. DeductivePrediction as a separate schema step (`schemas/deductive_prediction.schema.json`)**
Our MechanismHypothesis has falsifiers, but predictions and outcomes are not explicitly decoupled as machine-readable pairs. The Experiment pattern adds `DeductivePrediction` (if M under C, metric O moves direction D ≥ threshold T, control K does not move) and `PredictionOutcome` (observed_value vs. control_value, outcome: supported | falsified | inconclusive). This makes the "is the mechanism real" verdict deterministic.

**9. InductivePattern artifact (`V4_New_Goal.md` §InductivePattern)**
After ≥2 probe results, summarize: pattern, scope, supporting_results[], exceptions[], confidence, claim_boundary. We have no equivalent artifact that accumulates evidence across experiment cycles. For DiffusionGemma: after running ≥2 gradient-field probes, an InductivePattern would let us say "across T0 and T1 probes, continuous embedding targets consistently improve generation quality on GSM8K reasoning tasks but not on factual recall."

**10. 4-way Meta-Auditor architecture (orchestration / prompt-path / CLI / evidence)**
Our self-auditing is ad hoc. The Experiment pattern defines four specific Codex roles that produce JSON findings (not prose) from specific telemetry inputs. Key: each auditor has hard "must not" constraints (e.g., "Meta-Orchestration Auditor must NOT propose science changes"). This prevents scope creep in audit output.

### OVERLAPS with our kernel

| Experiment artifact | Our kernel equivalent | Status |
|---|---|---|
| MechanismHypothesis 5-question schema | Our 5-field MechanismHypothesis (silent_axiom → mechanism → hypothesis → observable → falsifier) | OVERLAP — Experiment version adds: `how_to_observe` paths (≥3), closed-set `required_probes`, `alternative_mechanisms` (≥3). Both require ≥3 falsifiers. Ours is richer on the axiom side; theirs on the observability side. |
| D-C-S (Diverge-Critique-Select) engine separation | Our multi-engine (Opus generates, Codex selects/reviews, GPT-5.5-Pro novelty+design) | OVERLAP — same principle, different labels. Their role naming (diverger→Gemini, critic→Codex, converger→Opus) is cleaner. |
| Blackboard shared artifact store | Arbor idea tree + RUNLOG | PARTIAL OVERLAP — both use structured state files, but their blackboard is finer-grained (separate dirs per artifact type, sha256 hashes on everything, JSONL event log). |
| ProbeResult decision is bash-deterministic | Our L2 "score improvement alone never confirms a mechanism; require verifier" | OVERLAP |
| Sealed eval/test guard | Our L2 "eval scripts / test sets / baselines are sealed" | EXACT OVERLAP |
| Score ≠ mechanism check | Our L2 "score improvement alone never confirms a mechanism" | EXACT OVERLAP |
| Generator / critic / selector isolation | Our L2 "generator/critic/selector ISOLATION across distinct models" | EXACT OVERLAP — their SessionContract formalizes it more rigorously |
| NegativeCase (any form) | Our "a failure must shrink the search space" | PARTIAL OVERLAP — our principle is correct but not operationalized as a structured artifact |

### SKIP

- All Bash dispatcher / CLI wrapper implementation (`dispatchers/*.sh`, `bin/*.sh`, `tools/*.sh`) — infrastructure, not methodology
- PeopleSnapshot / avatar / PSNR domain-specific metrics — irrelevant to DiffusionGemma
- Multica control plane (issues/queue management) — we use Arbor idea tree for structure; no need to adopt Multica
- GPU lane / job queue management — environment-specific
- Local Deep Research / Agora / Spotlight source acquisition machinery — we use Zotero + Playwright → GPT-5.5-Pro for literature
- V4-C sidecar LDR wiring — complex Ollama dependency; not applicable to our setup

---

## 7. Top-3 Highest-Value Takeaways

### Takeaway 1: ContextBundle as LLM Pre-Flight (Immediately Adoptable)

**What**: A JSON artifact (`short_context` + `forbidden_assumptions` + `recent_negative_cases` paths + `must_read` paths with sha256) prepended to every LLM call. If missing → LLM must return `{"error":"missing_context_bundle"}` not hallucinate.

**Why high value**: Our current loop has no explicit mechanism to prevent Opus or GPT-5.5-Pro from re-proposing already-falsified directions. The `recent_negative_cases` field and the invocation header hard rule ("do NOT repeat any failure listed in recent_negative_cases") directly address this. The sha256 on `must_read` artifacts enables stale detection.

**Adoption path**: Before any `/ideate` or GPT-5.5-Pro query in the DiffusionGemma loop, build a ContextBundle JSON (can be a simple YAML/JSON file in `plan/`) with: current goal (from `plan/goal-directive.md`), forbidden_assumptions (from pruned Arbor nodes), recent_negative_cases (from ruled-out Track 1/2 directions), must_read paths (HekaiMing.md, plan/paper-draft.md). Prepend to the prompt.

### Takeaway 2: claim_mode Tier + Honest NegativeCase (Architecture for Our Claim Ladder)

**What**: Three-tier claim ladder (score_recipe < mechanism_probe < paper_claim) with explicit controls required per tier. NegativeCase as a structured artifact that must: rule out ≥2 things, name ≥1 surviving alternative, give a concrete retry condition, route to a next discriminating probe.

**Why high value**: Our Track 1 (wall-clock frontier) produced results that we are promoting to paper level. The Experiment's gate for `paper_claim` requires: locality probe, negative control, cross-subject, 3-seed variance, novelty check. Our Track 2 (gradient-field) is generating hypotheses. The IdeaCritic's question "param_tweak masquerading as mechanism?" is directly relevant to our continuous-embedding-target ideas — we need to be honest about which are T0 recipe ideas and which are T1 mechanism claims.

**Adoption path**: For each DiffusionGemma hypothesis in the Arbor tree, assign a `claim_mode` field at creation time. When a Track 2 experiment fails, write a structured NegativeCase (what ruled out, what survived, retry condition) before the next `/ideate` call.

### Takeaway 3: Execution Verification Anti-No-Op (Critical for DiffusionGemma Training)

**What**: Every ProbePlan must declare `execution_verification.log_assertion` — a regex over the training log that MUST match to prove the intervention actually fired. If no match → auto-downgrade to `implementation_bug`. Motivated by "patches with conditional guards frequently no-op silently when dict shape differs across phases."

**Why high value**: This is the exact failure mode we have encountered in DiffusionGemma SFT: config changes that appear to apply but are overridden by Trainer defaults; loss weight modifications that pass unit tests but don't activate during the actual block-diffusion forward pass. We have no systematic guard for this. The log_assertion pattern is cheap to add (just grep the training log for a specific parameter printout or loss component activation).

**Adoption path**: For each DiffusionGemma experiment, declare before launch: which log line (or loss component output) proves the intervention fired. At evaluation time, grep for it. If absent → the experiment is `implementation_bug`, not `support` or `reject`. This is a one-line discipline change that eliminates entire classes of false negatives.

---

## Appendix: Key File Paths

| File | Content |
|---|---|
| `/home/lingxufeng/agent/Experiment/CLAUDE.md` | System overview; V4 cognitive model; multi-engine role map |
| `/home/lingxufeng/agent/Experiment/docs/SESSION_CONTRACT.md` | Per-role session isolation policy |
| `/home/lingxufeng/agent/Experiment/prompts/_README.md` | 7 core prompts; claim_mode gate table; what is NOT in the loop |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_mechanism_hypothesis.md` | 5-question schema; D-C-S stage guidance; anti-patterns |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_probe_plan.md` | Single-variable rule; execution_verification; T0/T1/T2 controls table |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_negative_case.md` | search_space shrink rule; retry_condition discipline |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_claim_evidence.md` | claim_type taxonomy; sha256 requirement; promotion rules |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_promotion.md` | Tiered promotion gates; reward-hacking checklist; anti-patterns |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_idea_seed.md` | IdeaSeed schema; ≤7 cap; kind enum |
| `/home/lingxufeng/agent/Experiment/prompts/artifact_idea_critic.md` | IdeaCritic filter questions; shortlist output |
| `/home/lingxufeng/agent/Experiment/schemas/context_bundle.schema.json` | ContextBundle JSON schema |
| `/home/lingxufeng/agent/Experiment/schemas/deductive_prediction.schema.json` | DeductivePrediction + PredictionOutcome schemas |
| `/home/lingxufeng/agent/Experiment/schemas/abductive_explanation_set.schema.json` | AES schema; ≥2 candidate gate |
| `/home/lingxufeng/agent/Experiment/schemas/mechanism_analog_map.schema.json` | Cross-domain transfer schema |
| `/home/lingxufeng/agent/Experiment/schemas/novelty_risk_report.schema.json` | NoveltyRiskReport schema |
| `/home/lingxufeng/agent/Experiment/V4_New_Goal.md` | Full V4 reasoning lane artifacts; V4-Full pass criteria |
| `/home/lingxufeng/agent/Experiment/blackboard/MANIFEST.md` | Dispatcher → Agent → CLI map |
