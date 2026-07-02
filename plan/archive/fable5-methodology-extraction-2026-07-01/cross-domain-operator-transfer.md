# Cross-Domain Operator Transfer

## Purpose

Use this skill to transfer a research judgment operator into another domain such as product, engineering, design, education, business, or organization management.

The goal is not vocabulary transfer. The goal is to preserve the decision function.

## Trigger

Use this when:

- a research operator seems useful outside research;
- a product, engineering, design, or organization decision needs the same structure;
- the user asks to generalize `enrich.md`;
- a methodology is being converted into a broader operating system.

Do not use this when:

- the target domain has no decision pressure;
- the transferred operator would only rename common sense;
- no observable decision changes.

## Transfer Table

| Research Operator | Cross-Domain Operator | Preserved Function |
| --- | --- | --- |
| Modeling-object shift | Problem-object shift | Ask whether the wrong thing is being optimized. |
| Minimum falsifier | Minimum decision test | Find the cheapest test that can change the decision. |
| Reviewer attack | Stakeholder attack | Simulate the strongest objection from an affected party. |
| Deletion test | Value-proposition deletion test | Remove fancy language and see if value remains. |
| Occupancy map | Competitor / precedent map | Check whether the space is already owned. |
| Metric contract | Success contract | Align measured success with real success. |
| Rescope | Degrade gracefully | Convert a failed big claim into a smaller useful deliverable. |
| Failure conversion | Lesson-to-constraint conversion | Turn failure into a rule for future decisions. |

## Procedure

1. Name the source operator.
2. State its decision function in research.
3. Name the target domain.
4. Identify the analogous pressure point.
5. Identify what counts as evidence in the target domain.
6. Identify what counts as a falsifier in the target domain.
7. Translate the output schema.
8. Run a deletion test to ensure it is not vocabulary transfer.
9. State where the transfer breaks.

## Output Schema

```text
Source operator:
Research decision function:
Target domain:
Target-domain pressure point:
Transferred operator:
Evidence in target domain:
Minimum decision test:
Stakeholder attack:
Output schema:
Where transfer breaks:
Verdict:
```

## Prompt

```text
Transfer the following research operator into a new domain.

Do not transfer vocabulary. Transfer the decision function.

Output:

1. Source operator.
2. Original research decision function.
3. Target domain.
4. Analogous pressure point.
5. Evidence type in the target domain.
6. Minimum decision test.
7. Stakeholder attack.
8. Output schema.
9. Where the transfer breaks.
10. Verdict: ACCEPT / REVISE / HOLD / KILL.
```

## Domain Examples

### Product

Research:

```text
Deletion test
```

Product transfer:

```text
Remove the story, branding, and AI language. Does the user still get a concrete job done better?
```

Minimum decision test:

```text
Give the prototype to 5 target users and check whether they complete the core job without being sold the narrative.
```

### Engineering

Research:

```text
Minimum falsifier
```

Engineering transfer:

```text
Build the smallest load, latency, or correctness test that would kill the architecture.
```

Minimum decision test:

```text
Run a spike that isolates the bottleneck before committing to a large rewrite.
```

### Design

Research:

```text
Reviewer attack
```

Design transfer:

```text
Run stakeholder attack: novice user, power user, accessibility reviewer, business owner.
```

Minimum decision test:

```text
Can the intended user complete the primary workflow without explanatory text?
```

### Education

Research:

```text
Metric-goal divergence
```

Education transfer:

```text
Does the assessment reward real understanding or test-taking adaptation?
```

Minimum decision test:

```text
Give transfer problems that require the concept in a new context.
```

### Business

Research:

```text
Occupancy map
```

Business transfer:

```text
Map competitors, substitutes, existing workflows, and budget owners before claiming whitespace.
```

Minimum decision test:

```text
Can a buyer name what they would stop using or stop paying for?
```

### Organization Management

Research:

```text
Agent governance
```

Organization transfer:

```text
Separate proposer, executor, reviewer, and approver for decisions with political or financial risk.
```

Minimum decision test:

```text
Can the reviewer reject the proposal without social penalty or context contamination?
```

## Failure Modes

- Transferring labels instead of tests.
- Ignoring what counts as evidence in the target domain.
- Over-generalizing a research pattern into management jargon.
- Missing stakeholders.
- Failing to define a decision that would change.
- Keeping a transfer that produces no new kill condition.

