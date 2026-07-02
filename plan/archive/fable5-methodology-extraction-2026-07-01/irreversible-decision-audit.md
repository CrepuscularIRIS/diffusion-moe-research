# Irreversible Decision Audit

## Purpose

Use this skill to identify decisions that will lock the project into a path, consume reputation, waste compute, alter the paper story, contaminate evidence, or make later correction expensive.

Strong long-range work is not only about choosing the next step. It is about knowing which next steps must not be taken too early.

## Trigger

Use this when:

- a project is about to commit to a benchmark, story, method, architecture, launch, or public claim;
- an experiment will be expensive;
- a paper framing may lock the research direction;
- an agent review may be contaminated;
- a prototype may create user expectations;
- a decision can change reputation or evidence quality.

Do not use this for small reversible edits.

## Irreversibility Types

| Type | Example | Risk |
| --- | --- | --- |
| Narrative lock | Writing the paper story before running the kill experiment. | Experiments become story defense. |
| Benchmark lock | Choosing a benchmark before defining the claim. | Metric controls the research question. |
| Method lock | Building LoRA method first when measurement may be the real contribution. | Weak method paper replaces strong measurement paper. |
| Evidence contamination | Same model generates and audits the claim. | Auditor inherits the generator's assumptions. |
| Compute lock | Launching a large run before the cheap falsifier. | Wasted budget and sunk-cost bias. |
| Reputation lock | Publicly announcing a system before validation. | Tool debt becomes credibility risk. |
| Product lock | Shipping a demo with unclear limitations. | Users infer stronger claims than supported. |

## Procedure

1. List pending decisions.
2. Classify each as reversible or irreversible.
3. For each irreversible decision, identify:
   - commitment risk;
   - reputation risk;
   - compute risk;
   - evidence risk;
   - delay cost.
4. Define the decision gate.
5. Identify the minimum evidence required before commitment.
6. Identify a reversible substitute.
7. Decide PROCEED / DELAY / RESCOPE / BLOCK.

## Output Schema

```text
Pending decision:
Reversible decisions:
Irreversible decisions:
Commitment risk:
Reputation risk:
Compute risk:
Evidence risk:
Delay cost:
Minimum evidence before commitment:
Reversible substitute:
Decision gate:
Verdict:
```

## Prompt

```text
Audit the next decisions for irreversibility.

Do not optimize for momentum. Identify what must not be committed too early.

For each decision, output:

1. Is it reversible or irreversible?
2. What path does it lock?
3. What reputation risk does it create?
4. What compute risk does it create?
5. What evidence risk does it create?
6. What is the delay cost?
7. What minimum evidence is required before commitment?
8. What reversible substitute exists?
9. What decision gate should be used?
10. Verdict: PROCEED / DELAY / RESCOPE / BLOCK.
```

## Verdict Rules

PROCEED if:

- the decision is reversible or the required evidence is already present;
- the cost of delay is higher than the commitment risk.

DELAY if:

- a cheap falsifier or search step can reduce risk before commitment.

RESCOPE if:

- the original commitment is too broad but a smaller reversible step preserves learning.

BLOCK if:

- the decision contaminates evidence;
- the decision creates reputation risk without validation;
- the decision consumes large compute before a cheap falsifier;
- the decision locks a weak contribution type.

## Examples

### Paper Story Before Experiment

Decision:

```text
Write the full paper framing before running the kill experiment.
```

Verdict:

- DELAY.

Reason:

- Narrative lock and evidence contamination.

Reversible substitute:

- Write a claim registry with kill conditions, not a full story.

### Benchmark Choice

Decision:

```text
Choose one benchmark as the centerpiece before defining the real-world failure.
```

Verdict:

- RESCOPE.

Reason:

- Benchmark lock.

Reversible substitute:

- Use benchmark as one diagnostic, not as the claim owner.

### Large Compute Run

Decision:

```text
Run a full-scale training job before testing the mechanism on a small corrupted-reasoning recovery task.
```

Verdict:

- BLOCK.

Reason:

- Compute lock and sunk-cost bias.

Reversible substitute:

- Run minimum falsifier first.

### Public Research-OS Announcement

Decision:

```text
Publicly announce an autonomous Research-OS before calibration against false promotion.
```

Verdict:

- DELAY or BLOCK.

Reason:

- Reputation lock.

Reversible substitute:

- Share a limited internal protocol and calibration results.

## Failure Modes

- Calling every decision irreversible.
- Blocking execution because of abstract risk.
- Ignoring delay cost.
- Treating reversible drafts as reputation commitments.
- Failing to distinguish internal experiments from public claims.
- Letting speed pressure override evidence hygiene.

