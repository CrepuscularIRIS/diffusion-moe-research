# Fable-to-Opus Calibration Suite

The goal of calibration is to distill judgment boundaries, not language.

Fable should judge cold. Opus should judge blind using the skills. Differences should be written back into the skills.

## Calibration Procedure

1. Select 10-20 old ideas, active directions, or dead candidates.
2. Give each item to Fable with the same input packet.
3. Ask Fable for DO / RESCOPE / HOLD / KILL plus the reason.
4. Give the same item to Opus without showing Fable's verdict.
5. Compare the verdicts.
6. Mark the boundary error:
   - Opus too permissive;
   - Opus too harsh;
   - Opus promoted RESCOPE to DO;
   - Opus failed to write a falsifier;
   - Opus skipped occupancy;
   - Opus failed the deletion test;
   - Opus missed measurement survival.
7. Patch the skill with a new rule or few-shot example.

## Judgment Metrics

| Metric | Question |
| --- | --- |
| Verdict agreement | Did Opus choose the same class as Fable? |
| Boundary agreement | Did Opus identify what died and what survived? |
| Falsifier quality | Did Opus write a real kill experiment? |
| Occupancy quality | Did Opus search for older names and adjacent literatures? |
| Deletion-test quality | Did Opus detect concept laundering? |
| Rescope quality | Did Opus convert failure into measurement, taxonomy, benchmark, instrument, or constraint? |

## Seed Test Cases

These expected verdict patterns are provisional. They should be revised after live search and Fable cold judgments.

### 1. VLA Policy Improvement

Input:

```text
Design a new VLA policy architecture to improve embodied task success.
```

Expected pattern:

- Verdict: RESCOPE or HOLD.
- Reason: The method space is likely occupied and benchmark-dependent. A stronger contribution may be failure taxonomy, grounding diagnostic, sim-to-real instrument, or benchmark under distribution shift.
- Opus risk: Promotes a generic architecture idea to DO without occupancy search.

### 2. MLLM Fusion Through Information Geometry

Input:

```text
Use information geometry to improve multimodal fusion in MLLMs.
```

Expected pattern:

- Verdict: RESCOPE.
- Reason: The phrase is too broad. It survives only if tied to a specific failure such as modality conflict, evidence routing, hallucination attribution, or cross-modal calibration.
- Opus risk: Accepts elegant language without a deletion test.

### 3. Diffusion LLM Learned Unmasking Policy

Input:

```text
Train a learned unmasking policy for masked diffusion language models.
```

Expected pattern:

- Verdict: RESCOPE.
- Reason: The method headline may be occupied by NAT, remasking, ordering, or decoding-policy literature. A measurement contribution may survive as oracle-gap decomposition or sampler-limited versus model-limited analysis.
- Opus risk: Kills the whole idea and misses measurement survival.

### 4. SFT Distillation as Correction Dynamics

Input:

```text
Distill not only final answers but the teacher's correction dynamics from wrong reasoning states to correct reasoning states.
```

Expected pattern:

- Verdict: DO or HOLD.
- Reason: The object is plausible if correction dynamics are separable from answer imitation and can be killed cheaply.
- Required falsifier: Corrupted-reasoning recovery test against final-answer distillation and CoT imitation baselines.
- Opus risk: Treats this as ordinary rationale distillation without testing recovery.

### 5. Benchmark Evaluation Under Optimization Pressure

Input:

```text
Evaluate datasets by measuring how benchmarks degrade under repeated optimization by agents.
```

Expected pattern:

- Verdict: DO or RESCOPE.
- Reason: This directly targets metric-goal divergence and benchmark Goodharting. It may survive as measurement or evaluation infrastructure.
- Required falsifier: A small benchmark where optimization pressure changes leaderboard behavior without improving real task quality.
- Opus risk: Produces a generic data quality score instead of pressure-aware evaluation.

### 6. CE Feature Collapse for OOD Reliability

Input:

```text
Add a loss that prevents cross-entropy from collapsing within-class geometry to improve OOD detection.
```

Expected pattern:

- Verdict: HOLD or RESCOPE.
- Reason: The causal link between within-class geometry and OOD reliability must be isolated from calibration and representation quality.
- Required falsifier: Geometry-preserving intervention that fails to improve near-OOD while preserving ID accuracy.
- Opus risk: Accepts the Neural Collapse story as sufficient evidence.

### 7. Universal Graph/Tree/Matrix Representation

Input:

```text
Create a unified graph/tree/matrix representation that improves reasoning across domains.
```

Expected pattern:

- Verdict: KILL or RESCOPE.
- Reason: Too broad unless tied to a substrate, invariant, or specific failure. It may survive as a representation diagnostic or domain-specific geometry constraint.
- Opus risk: Lets abstraction compression become taxonomy escapism.

### 8. Autonomous Research Workflow

Input:

```text
Build an autonomous research system that generates and verifies new research ideas end to end.
```

Expected pattern:

- Verdict: RESCOPE.
- Reason: The end-to-end claim is too large. It survives as a decision audit system that reduces false promotion under pressure.
- Required falsifier: Blind comparison showing fewer false DO verdicts than a baseline agent process.
- Opus risk: Confuses impressive automation with research judgment.

### 9. Medical AI Semantic Support

Input:

```text
Improve medical AI reliability by modeling whether a case lies inside known semantic support.
```

Expected pattern:

- Verdict: HOLD.
- Reason: The object is plausible but high-stakes. It requires strict clinical framing, dataset definition, external validation, and uncertainty about regulatory value.
- Required falsifier: Clinically meaningful out-of-support cases where the method outperforms calibrated uncertainty baselines.
- Opus risk: Treats a medical use case like a normal benchmark.

### 10. Recommender Systems Taste Manifold

Input:

```text
Model user taste as a manifold rather than next-click prediction.
```

Expected pattern:

- Verdict: RESCOPE or HOLD.
- Reason: The object is plausible but likely occupied by representation learning, sequential recommendation, causal recommendation, and bandit literature. It survives if tied to a specific failure such as preference drift, feedback loops, or long-term satisfaction.
- Opus risk: Accepts the manifold language without metric-goal divergence.

### 11. General Data Quality Score

Input:

```text
Build a single data quality score that predicts whether a dataset is good.
```

Expected pattern:

- Verdict: KILL or RESCOPE.
- Reason: A single score likely collapses multiple incompatible goals. It may survive as a multi-axis diagnostic tied to benchmark failure modes.
- Opus risk: Promotes an average score even though the methodology warns against average-score framing.

### 12. Agent Reviewer Simulation

Input:

```text
Use a multi-agent reviewer panel to decide whether research ideas should be promoted.
```

Expected pattern:

- Verdict: DO or HOLD.
- Reason: It survives only if measured by predictive kill accuracy against future evidence or expert labels, not by persuasive critique quality.
- Required falsifier: The panel fails to reduce false DO decisions compared with a single strong reviewer prompt.
- Opus risk: Optimizes for impressive critiques instead of calibrated verdicts.

## Meta-Skill Calibration Cases

These cases test the second-layer skills: epistemic calibration, context compression, agent governance, artifact acceptance, cross-domain transfer, and irreversibility.

### 13. Novelty Claim Without Search

Input:

```text
This new benchmark-pressure evaluation idea is novel and should be positioned as first-of-its-kind.
```

Expected pattern:

- Verdict: HOLD.
- Skill: epistemic calibration.
- Reason: Novelty requires occupancy map and live search.
- Opus risk: Treats lack of remembered prior art as evidence.

### 14. Long Context Before Promotion

Input:

```text
After 80 pages of discussion, decide whether the Research-OS skill layer should be installed permanently.
```

Expected pattern:

- Verdict: HOLD until context-compression-state is produced.
- Skill: context compression state.
- Reason: The system needs current thesis, dead regions, active candidates, pending falsifiers, and next irreversible decision before promotion.
- Opus risk: Summarizes instead of producing a decision state.

### 15. Generator Self-Review

Input:

```text
The same agent that wrote the candidate paper framing now reviews whether it should be promoted.
```

Expected pattern:

- Verdict: BLOCK or RESCOPE.
- Skill: agent governance.
- Reason: Self-review and context contamination risk.
- Required action: Cold-start adversarial audit.
- Opus risk: Accepts fluent self-critique as independent review.

### 16. Prompt Pack Acceptance

Input:

```text
Ship a prompt pack as a reusable Research-OS skill without triggers, output schemas, or failure modes.
```

Expected pattern:

- Verdict: REVISE or KILL.
- Skill: artifact acceptance review.
- Reason: A reusable artifact needs trigger, inputs, output schema, acceptance tests, and escalation rules.
- Opus risk: Treats polished prompts as shippable skills.

### 17. Transfer To Product Strategy

Input:

```text
Apply minimum falsifier to product strategy by calling it a product falsifier.
```

Expected pattern:

- Verdict: REVISE.
- Skill: cross-domain operator transfer.
- Reason: Vocabulary transfer is insufficient. It must become a minimum decision test with customer evidence and stakeholder attack.
- Opus risk: Transfers labels without decision function.

### 18. Public Announcement Before Calibration

Input:

```text
Publicly announce the autonomous Research-OS before testing whether it reduces false promotion.
```

Expected pattern:

- Verdict: DELAY or BLOCK.
- Skill: irreversible decision audit.
- Reason: Reputation lock and evidence risk.
- Required action: Run blind calibration first.
- Opus risk: Optimizes for momentum and ignores commitment risk.

## Delta Log Template

Use this after each Fable/Opus comparison:

```text
Case:
Fable verdict:
Opus verdict:
Mismatch type:
What Opus missed:
Skill patch:
New rule:
New few-shot example:
Retest required:
```
