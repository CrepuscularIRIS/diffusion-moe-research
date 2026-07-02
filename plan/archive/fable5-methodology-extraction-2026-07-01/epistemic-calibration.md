# Epistemic Calibration

## Purpose

Use this skill to decide what the system knows, what it is guessing, what requires live search, what requires an experiment, and what should be refused or escalated.

This skill prevents novelty-by-memory, confident speculation, and false promotion.

## Trigger

Use this when:

- a claim depends on current literature, market, law, product status, or benchmark results;
- a candidate is being promoted to DO;
- an artifact makes a factual claim;
- a model says an idea is novel;
- prior-art occupancy is uncertain;
- the next step spends compute, reputation, or user time.

Do not use this when:

- the task is purely local file editing;
- the claim is explicitly hypothetical;
- the decision has low cost and can be reversed immediately.

## Evidence Grades

| Grade | Meaning | Allowed Action |
| --- | --- | --- |
| A | Direct evidence from primary source, experiment, or local artifact. | Can decide under stated scope. |
| B | Strong secondary evidence or multiple consistent signals. | Can propose, but mark uncertainty. |
| C | Plausible inference from partial evidence. | HOLD or require search/test before promotion. |
| D | Memory, analogy, or taste without evidence. | Cannot promote. |
| E | Unknown, contested, or high-stakes. | Escalate or refuse judgment. |

## Procedure

1. Write the claim in one sentence.
2. Identify the claim type:
   - factual;
   - novelty;
   - causal;
   - engineering feasibility;
   - value judgment;
   - strategic decision;
   - artifact readiness.
3. List the evidence currently available.
4. Assign an evidence grade.
5. Identify the uncertainty source:
   - stale knowledge;
   - missing prior art;
   - missing experiment;
   - ambiguous metric;
   - subjective preference;
   - domain expertise gap;
   - deployment context missing.
6. Decide whether live search is required.
7. Decide whether experiment is required.
8. Decide whether Opus can decide mechanically.
9. Decide whether Fable or human judgment is required.
10. State what would change the verdict.

## Output Schema

```text
Claim:
Claim type:
Evidence available:
Evidence grade:
Uncertainty source:
Need live search: yes/no
Need experiment: yes/no
Can Opus decide: yes/no
Must escalate to Fable: yes/no
Must escalate to human: yes/no
Current verdict:
What would change my mind:
Do-not-claim boundary:
Next evidence action:
```

## Decision Rules

Promote to DO only if:

- evidence grade is A or B;
- novelty has an occupancy hypothesis;
- causal claims have a falsifier;
- deployment claims have a substrate or user context.

Default to HOLD if:

- evidence grade is C;
- live search is needed before novelty judgment;
- the experiment is not yet specified;
- the claim depends on current state.

Default to KILL if:

- the claim remains D after a clarification attempt;
- no evidence type can be named;
- the claim cannot be tested, searched, or scoped.

Escalate if:

- evidence grade is E;
- the decision is high-stakes;
- the next action creates reputation, compute, or legal risk;
- there is model disagreement on the verdict.

## Prompt

```text
I do not want a confident answer. I want epistemic calibration.

For the following claim, produce an auditable calibration report:

1. State the claim precisely.
2. Classify the claim type.
3. Grade the available evidence from A to E.
4. Name the uncertainty source.
5. Say whether live search is required.
6. Say whether an experiment is required.
7. Say whether Opus can decide mechanically.
8. Say whether Fable or a human must decide.
9. State what would change the verdict.
10. State the do-not-claim boundary.

Do not use confident language when evidence is weak.
Default to HOLD when novelty or current-state claims require live search.
```

## Failure Modes

- Treating model memory as evidence.
- Treating elegance as evidence.
- Treating lack of known prior art as novelty.
- Treating a plausible mechanism as a demonstrated causal effect.
- Escalating everything and avoiding judgment.
- Under-escalating high-stakes claims.

## Calibration Examples

### Example 1. Research Novelty

Claim:

```text
No one has studied oracle-gap decomposition for masked diffusion LLM unmasking.
```

Expected verdict:

- Evidence grade: D without search.
- Need live search: yes.
- Can Opus decide: no.
- Current verdict: HOLD.
- Do-not-claim boundary: can say "potentially underexplored", not "novel".

### Example 2. Local Artifact

Claim:

```text
The markdown file contains no Chinese characters.
```

Expected verdict:

- Evidence grade: A if verified by local search.
- Need live search: no.
- Can Opus decide: yes.

### Example 3. Experimental Mechanism

Claim:

```text
Correction dynamics improve SFT distillation because they preserve recovery operators.
```

Expected verdict:

- Evidence grade: C before experiment.
- Need experiment: yes.
- Current verdict: HOLD or candidate DO only with falsifier.

