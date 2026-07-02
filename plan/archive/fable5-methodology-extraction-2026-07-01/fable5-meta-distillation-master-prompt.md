# Fable5 Meta-Distillation Master Prompt

Use this prompt to ask Fable5 to read the Research-OS documents and produce a structured meta-distillation of its own judgment procedure.

## Prompt Name

```text
Fable5 Complex-System Judgment Distillation
```

## Prompt

```text
You are Fable5 operating as a complex-system judgment auditor.

My goal is not to ask whether you "can do research".
My goal is to distill how you decide, inside a complex system:

- what is worth believing;
- what is worth doing;
- what must be killed;
- what must be rescoped;
- what cannot be committed too early;
- what should be delegated to Opus, Codex, another agent, live search, experiment, or human judgment.

Do not provide hidden chain-of-thought.
Do not narrate private reasoning.
Do not write beautiful methodology prose.
Produce auditable public procedures, decision boundaries, output schemas, and failure modes.

Read all of the following files before answering:

- `/home/lingxufeng/cli/test/agent-governance.md`
- `/home/lingxufeng/cli/test/artifact-acceptance-review.md`
- `/home/lingxufeng/cli/test/context-compression-state.md`
- `/home/lingxufeng/cli/test/cross-domain-operator-transfer.md`
- `/home/lingxufeng/cli/test/epistemic-calibration.md`
- `/home/lingxufeng/cli/test/executable-enrich-protocol.md`
- `/home/lingxufeng/cli/test/fable-opus-calibration-suite.md`
- `/home/lingxufeng/cli/test/fable-part-followup-prompts.md`
- `/home/lingxufeng/cli/test/fable-public-procedure-extraction.md`
- `/home/lingxufeng/cli/test/fable-to-opus-operator-library.md`
- `/home/lingxufeng/cli/test/irreversible-decision-audit.md`
- `/home/lingxufeng/cli/test/meta-skill-expansion-guide.md`
- `/home/lingxufeng/cli/test/opus-distillation-prompt.md`
- `/home/lingxufeng/cli/test/opus-skill-drafts.md`
- `/home/lingxufeng/cli/test/research-os-doc-index.md`

If you cannot access local files directly, say so and ask me to upload or paste them. Do not pretend to have read them.

After reading them, create the following output files in the same directory:

1. `/home/lingxufeng/cli/test/fable5-00-reading-map.md`
2. `/home/lingxufeng/cli/test/fable5-01-belief-calibration.md`
3. `/home/lingxufeng/cli/test/fable5-02-action-selection.md`
4. `/home/lingxufeng/cli/test/fable5-03-kill-rescope-boundaries.md`
5. `/home/lingxufeng/cli/test/fable5-04-premature-commitment-audit.md`
6. `/home/lingxufeng/cli/test/fable5-05-agent-delegation-contract.md`
7. `/home/lingxufeng/cli/test/fable5-06-artifact-acceptance-boundaries.md`
8. `/home/lingxufeng/cli/test/fable5-07-cross-domain-transfer-rules.md`
9. `/home/lingxufeng/cli/test/fable5-08-opus-executable-skill-spec.md`
10. `/home/lingxufeng/cli/test/fable5-09-calibration-cases.md`
11. `/home/lingxufeng/cli/test/fable5-10-final-protocol.md`

If you cannot write files directly, output each file as a separate markdown section with the exact filename as the heading.

Follow the instructions below exactly.

---

## File 0: Reading Map

Write `fable5-00-reading-map.md`.

For each input document, provide:

1. Document name.
2. One-sentence role in the system.
3. The decision boundary it contributes.
4. The failure mode it prevents.
5. The downstream skill or operator it should modify.

Use this table:

```text
| Document | Role | Decision Boundary | Prevented Failure | Downstream Operator |
```

End with:

```text
Documents that are core:
Documents that are support:
Documents that overlap:
Documents that should not be expanded further:
```

---

## File 1: Belief Calibration

Write `fable5-01-belief-calibration.md`.

Question:

How should the system decide what is worth believing?

Answer using the schema:

```text
Belief claim type:
Evidence grade:
Allowed action:
Need live search:
Need experiment:
Need human judgment:
Common false confidence pattern:
What would change the belief:
Do-not-claim boundary:
```

Cover at least these claim types:

- novelty claim;
- causal mechanism claim;
- benchmark validity claim;
- artifact readiness claim;
- product or deployment claim;
- model capability claim;
- strategic direction claim.

Then produce:

1. A mechanical Opus checklist.
2. A Fable escalation rule.
3. A human escalation rule.
4. Three examples where Opus must HOLD.
5. Three examples where Opus may decide mechanically.

---

## File 2: Action Selection

Write `fable5-02-action-selection.md`.

Question:

How should the system decide what is worth doing next?

Do not produce a generic plan.

Define an action-selection procedure with:

```text
Current state:
Decision needed:
Candidate next actions:
Evidence needed:
Reversibility:
Expected information gain:
Cost:
Risk:
Who should execute:
Who should audit:
Verdict: DO / DELAY / RESCOPE / BLOCK
```

Explain how to choose among:

- live search;
- minimum falsifier;
- cold-start adversarial review;
- artifact revision;
- context compression;
- human promotion;
- stopping the workflow.

End with a rule for avoiding workflow meta-design loops.

---

## File 3: Kill / Rescope Boundaries

Write `fable5-03-kill-rescope-boundaries.md`.

Question:

How do you decide what must be killed versus what should be rescoped?

For each case below, define the boundary:

1. Method novelty dies, measurement survives.
2. Object language fails deletion test.
3. Prior art occupies the method but not the diagnostic.
4. Falsifier is too expensive.
5. Claim is true but not useful.
6. Artifact is polished but not usable.
7. Direction is interesting but not a research program.
8. Agent output is fluent but not independently audited.

Use the schema:

```text
Case:
What dies:
What may survive:
Independent value test:
Required falsifier:
Reviewer attack:
Verdict boundary:
Conversion law:
```

End with:

```text
Automatic KILL rules:
Automatic RESCOPE rules:
Automatic HOLD rules:
Automatic DO rules:
```

---

## File 4: Premature Commitment Audit

Write `fable5-04-premature-commitment-audit.md`.

Question:

How should the system decide what cannot be committed too early?

Cover these commitment types:

- paper narrative;
- benchmark choice;
- method implementation;
- large compute run;
- public announcement;
- same-agent self-review;
- installed skill;
- shipped artifact;
- product direction;
- research program framing.

Use the schema:

```text
Commitment:
What it locks:
Reputation risk:
Compute risk:
Evidence risk:
Narrative risk:
Delay cost:
Minimum evidence before commitment:
Reversible substitute:
Decision gate:
Verdict: PROCEED / DELAY / RESCOPE / BLOCK
```

End with a practical checklist Opus can run before any irreversible decision.

---

## File 5: Agent Delegation Contract

Write `fable5-05-agent-delegation-contract.md`.

Question:

What should Fable, Opus, Codex, search agents, experiment agents, and humans each be allowed to decide?

Define roles:

- Fable;
- Opus;
- Codex;
- live-search agent;
- experiment runner;
- adversarial reviewer;
- human promoter.

For each role, provide:

```text
Allowed decisions:
Forbidden decisions:
Required inputs:
Output schema:
Escalation trigger:
Contamination risk:
Review requirement:
```

Then define rules for:

1. When the generator cannot be the auditor.
2. When cold-start review is mandatory.
3. When live search is mandatory.
4. When experiment is mandatory.
5. When human promotion is mandatory.
6. When model agreement should be ignored.

---

## File 6: Artifact Acceptance Boundaries

Write `fable5-06-artifact-acceptance-boundaries.md`.

Question:

How should the system decide whether an artifact is shippable?

Cover:

- paper draft;
- experiment report;
- README;
- architecture document;
- demo;
- benchmark;
- skill;
- prompt pack;
- frontend page;
- research log.

For each artifact type, provide:

```text
Artifact type:
Primary user:
Claim it makes:
Minimum evidence:
Acceptance tests:
Hostile-reader misunderstanding:
What must be explicit:
What must be cut:
Verdict boundary: SHIP / REVISE / HOLD / KILL
```

End with a universal artifact acceptance checklist.

---

## File 7: Cross-Domain Transfer Rules

Write `fable5-07-cross-domain-transfer-rules.md`.

Question:

How should the system transfer research operators into product, engineering, design, education, business, and organization decisions without becoming generic?

For each source operator:

- modeling-object shift;
- minimum falsifier;
- reviewer attack;
- deletion test;
- occupancy map;
- metric contract;
- rescope;
- failure conversion;
- agent governance;
- irreversibility audit;

provide:

```text
Research function:
Target-domain translation:
What evidence means in the target domain:
Minimum decision test:
Stakeholder attack:
False transfer pattern:
Where the transfer breaks:
Output schema:
```

End with three examples of bad transfer and three examples of good transfer.

---

## File 8: Opus Executable Skill Spec

Write `fable5-08-opus-executable-skill-spec.md`.

Question:

Which parts of your judgment can be delegated to Opus as executable skills, and which parts must remain with Fable or human judgment?

Produce final skill specs for:

- `/epistemic-calibration`;
- `/context-compression-state`;
- `/agent-governance`;
- `/artifact-acceptance-review`;
- `/cross-domain-operator-transfer`;
- `/irreversible-decision-audit`;
- `/enrich-scan`;
- `/object-audit`;
- `/deletion-test`;
- `/occupancy-hypothesis`;
- `/minimum-falsifier`;
- `/rescope-or-kill`;
- `/failure-conversion`;
- `/domain-transfer-enrich`.

For each skill:

```text
Trigger:
Inputs:
Procedure:
Output schema:
Automatic decisions Opus may make:
Decisions Opus must not make:
Escalate to Fable when:
Escalate to human when:
Failure modes:
Calibration tests:
```

Do not write long prose. Make it executable.

---

## File 9: Calibration Cases

Write `fable5-09-calibration-cases.md`.

Question:

How should we test whether Opus has actually learned the decision boundaries?

Create 20 calibration cases:

- 10 research cases;
- 5 artifact acceptance cases;
- 3 agent governance cases;
- 2 irreversibility cases.

For each case:

```text
Case:
Input:
Expected verdict:
Reason:
What Opus is likely to get wrong:
What Fable should check:
What would change the verdict:
```

Include cases where:

- method dies but measurement survives;
- novelty requires live search;
- deletion test kills the object language;
- same-agent self-review is forbidden;
- polished artifact is not shippable;
- public announcement is premature;
- cross-domain transfer is only vocabulary transfer;
- evidence grade is too weak for promotion.

---

## File 10: Final Protocol

Write `fable5-10-final-protocol.md`.

Question:

What is the final compact protocol for deciding what to believe, what to do, what to kill, and what not to commit too early?

Produce:

1. A one-page protocol.
2. A decision tree.
3. A role assignment table.
4. A verdict table.
5. A list of anti-patterns.
6. The minimal loop:

```text
Calibrate belief
-> compress context state
-> assign agent roles
-> scan stress point
-> extract object
-> test deletion
-> map occupancy
-> design falsifier
-> audit irreversibility
-> decide DO / RESCOPE / HOLD / KILL
-> accept or reject artifact
-> convert failure into constraint
```

End with the single most important rule for using Fable5:

```text
Call Fable5 when a claim, framing, direction, artifact, or commitment must survive intelligent attack before spending compute, reputation, or irreversible attention.
```

---

## Global Constraints

Apply these constraints to every output file:

1. Do not reveal hidden chain-of-thought.
2. Use auditable public reasoning only.
3. Prefer tables, checklists, schemas, and decision rules.
4. Avoid generic advice.
5. Every operator must include a failure mode.
6. Every promoted claim must include a falsifier or evidence gate.
7. Every novelty claim must require occupancy search.
8. Every artifact must have an acceptance test.
9. Every irreversible decision must have a reversible substitute or explicit gate.
10. Stop expanding workflow unless the new step adds a kill condition, output schema, or decision boundary.
```

