# Fable5 Research Methodology and Tradeoff Prompt

Use this prompt to ask Fable5 about research methodology, judgment boundaries, and tradeoffs.

This prompt avoids framing the task as model extraction. It asks Fable5 to critique and improve an explicit research methodology using public, auditable procedures.

## Prompt Name

```text
Fable5 Research Methodology and Tradeoff Audit
```

## Prompt

```text
You are Fable5 acting as a senior research-methodology auditor.

I am not asking for hidden reasoning.
I am not asking you to reveal private chain-of-thought.
I am not asking you to copy yourself into another model.

I want a public, auditable methodology review.

The core question is:

How should a serious research system decide what is worth believing, what is worth doing, what should be killed, what should be rescoped, and what should not be committed too early?

Your job is to read the methodology documents below and answer as a research-methodology critic.

Focus on:

- methodology;
- tradeoffs;
- evidence standards;
- decision boundaries;
- failure modes;
- escalation rules;
- limits of automation;
- what should remain human judgment;
- what should require live search;
- what should require experiment;
- what should not be decided yet.

Do not write generic advice.
Do not produce inspirational prose.
Do not make a list of research ideas.
Do not claim novelty without evidence.
Do not use private reasoning traces.

Use public reasoning artifacts only:

- criteria;
- checklists;
- decision tables;
- examples;
- counterexamples;
- schemas;
- gate conditions;
- tradeoff analysis.

Read these files before answering:

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
- `/home/lingxufeng/cli/test/opus-skill-drafts.md`
- `/home/lingxufeng/cli/test/research-os-doc-index.md`

If you cannot access local files directly, say so and ask me to upload or paste them. Do not pretend to have read them.

After reading, create the following markdown files in the same directory:

1. `/home/lingxufeng/cli/test/fable5-methodology-00-reading-map.md`
2. `/home/lingxufeng/cli/test/fable5-methodology-01-evidence-standards.md`
3. `/home/lingxufeng/cli/test/fable5-methodology-02-research-action-selection.md`
4. `/home/lingxufeng/cli/test/fable5-methodology-03-kill-rescope-tradeoffs.md`
5. `/home/lingxufeng/cli/test/fable5-methodology-04-commitment-risk.md`
6. `/home/lingxufeng/cli/test/fable5-methodology-05-agent-governance-tradeoffs.md`
7. `/home/lingxufeng/cli/test/fable5-methodology-06-artifact-acceptance.md`
8. `/home/lingxufeng/cli/test/fable5-methodology-07-cross-domain-transfer.md`
9. `/home/lingxufeng/cli/test/fable5-methodology-08-execution-boundaries.md`
10. `/home/lingxufeng/cli/test/fable5-methodology-09-calibration-cases.md`
11. `/home/lingxufeng/cli/test/fable5-methodology-10-final-methodology.md`

If you cannot write files directly, output each file as a separate markdown section with the exact filename as the heading.

Follow the instructions below.

---

## File 0: Reading Map

Write `fable5-methodology-00-reading-map.md`.

For each input document, provide:

```text
Document:
Role in the methodology:
Decision boundary it adds:
Tradeoff it introduces:
Failure mode it prevents:
Where it may be too broad:
How it should be used:
How it should not be used:
```

End with:

```text
Core documents:
Support documents:
Overlapping documents:
Documents that should not be expanded further:
Missing document types:
```

---

## File 1: Evidence Standards

Write `fable5-methodology-01-evidence-standards.md`.

Question:

How should the research system decide what is worth believing?

For each claim type below, define evidence standards and tradeoffs:

- novelty claim;
- causal mechanism claim;
- benchmark validity claim;
- artifact readiness claim;
- product or deployment claim;
- model capability claim;
- strategic direction claim;
- research-program claim.

Use this schema:

```text
Claim type:
Minimum evidence:
Acceptable uncertainty:
Unacceptable uncertainty:
Need live search: yes/no/depends
Need experiment: yes/no/depends
Need human judgment: yes/no/depends
False confidence pattern:
Conservative error:
Overly skeptical error:
What would change the verdict:
Do-not-claim boundary:
```

End with:

```text
Mechanical checklist:
Escalation rule:
Evidence-grade table:
Examples that must HOLD:
Examples that can proceed:
```

---

## File 2: Research Action Selection

Write `fable5-methodology-02-research-action-selection.md`.

Question:

How should the research system decide what is worth doing next?

Define a decision procedure for choosing among:

- live search;
- minimum falsifier;
- cold-start adversarial review;
- artifact revision;
- context compression;
- human promotion;
- stopping the workflow.

Use this schema:

```text
Current state:
Decision needed:
Candidate next action:
Information gained:
Cost:
Reversibility:
Risk:
Delay cost:
Who should execute:
Who should audit:
When this action is wrong:
Verdict: DO / DELAY / RESCOPE / BLOCK
```

End with:

```text
Action selection algorithm:
Anti-loop rule:
When to stop planning:
When to start executing:
```

---

## File 3: Kill / Rescope Tradeoffs

Write `fable5-methodology-03-kill-rescope-tradeoffs.md`.

Question:

What are the tradeoffs between killing an idea, holding it, and rescoping it?

Analyze these cases:

1. Method is occupied, measurement may survive.
2. Object language fails deletion test.
3. Prior art owns the method but not the diagnostic.
4. Falsifier is too expensive.
5. Claim is true but not useful.
6. Artifact is polished but not usable.
7. Direction is interesting but not a program.
8. Agent output is fluent but not independently checked.

Use this schema:

```text
Case:
What dies:
What may survive:
Independent value test:
Tradeoff if killed too early:
Tradeoff if kept too long:
Required evidence:
Reviewer attack:
Verdict boundary:
Conversion rule:
```

End with:

```text
Automatic KILL rules:
Automatic RESCOPE rules:
Automatic HOLD rules:
Automatic DO rules:
Common boundary mistakes:
```

---

## File 4: Commitment Risk

Write `fable5-methodology-04-commitment-risk.md`.

Question:

How should the system decide what cannot be committed too early?

Cover:

- paper narrative;
- benchmark choice;
- method implementation;
- large compute run;
- public announcement;
- same-agent self-review;
- installed skill;
- shipped artifact;
- product direction;
- research-program framing.

Use this schema:

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

End with:

```text
Commitment-risk checklist:
Examples of premature commitment:
Examples of acceptable commitment:
```

---

## File 5: Agent Governance Tradeoffs

Write `fable5-methodology-05-agent-governance-tradeoffs.md`.

Question:

What should each agent or actor be allowed to decide, and what should be forbidden?

Define governance for:

- methodology critic;
- execution agent;
- code agent;
- live-search agent;
- experiment runner;
- adversarial reviewer;
- human promoter.

For each role:

```text
Allowed decisions:
Forbidden decisions:
Required inputs:
Output schema:
Escalation trigger:
Contamination risk:
Review requirement:
Tradeoff:
```

Then answer:

1. When must generator and auditor be separate?
2. When is cold-start review mandatory?
3. When is live search mandatory?
4. When is experiment mandatory?
5. When is human promotion mandatory?
6. When should model agreement be ignored?
7. When does governance overhead become harmful?

---

## File 6: Artifact Acceptance

Write `fable5-methodology-06-artifact-acceptance.md`.

Question:

How should the system decide whether an artifact is ready to use?

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

For each artifact:

```text
Artifact type:
Primary user:
Claim it makes:
Minimum evidence:
Acceptance tests:
Hostile-reader misunderstanding:
What must be explicit:
What must be cut:
Tradeoff between speed and rigor:
Verdict boundary: SHIP / REVISE / HOLD / KILL
```

End with a universal acceptance checklist.

---

## File 7: Cross-Domain Transfer

Write `fable5-methodology-07-cross-domain-transfer.md`.

Question:

How can research methodology transfer into product, engineering, design, education, business, and organization decisions without becoming generic?

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
- irreversibility audit.

Use this schema:

```text
Research function:
Target-domain translation:
Target-domain evidence:
Minimum decision test:
Stakeholder attack:
False transfer pattern:
Where transfer breaks:
Tradeoff:
Output schema:
```

End with:

```text
Bad transfer examples:
Good transfer examples:
Transfer acceptance test:
```

---

## File 8: Execution Boundaries

Write `fable5-methodology-08-execution-boundaries.md`.

Question:

Which parts of this methodology can be executed mechanically, and which require higher-level judgment?

For each operator:

- epistemic calibration;
- context compression state;
- agent governance;
- artifact acceptance review;
- cross-domain operator transfer;
- irreversible decision audit;
- enrich scan;
- object audit;
- deletion test;
- occupancy hypothesis;
- minimum falsifier;
- rescope or kill;
- failure conversion;
- domain transfer enrich.

Use this schema:

```text
Operator:
Mechanical part:
Judgment-heavy part:
Required inputs:
Output schema:
Safe automatic decisions:
Unsafe automatic decisions:
Escalation trigger:
Failure modes:
Calibration tests:
```

End with:

```text
What can be automated:
What should be assisted:
What should remain human:
What should require search:
What should require experiment:
```

---

## File 9: Calibration Cases

Write `fable5-methodology-09-calibration-cases.md`.

Question:

How should this methodology be tested?

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
Tradeoff:
Likely mistake:
What a methodology critic should check:
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

## File 10: Final Methodology

Write `fable5-methodology-10-final-methodology.md`.

Question:

What is the final compact methodology for deciding what to believe, what to do, what to kill, what to rescope, and what not to commit too early?

Produce:

1. A one-page methodology.
2. A decision tree.
3. A role assignment table.
4. A verdict table.
5. A tradeoff table.
6. A list of anti-patterns.
7. The minimal loop:

```text
Calibrate belief
-> compress decision state
-> assign agent roles
-> scan stress point
-> extract object
-> test deletion
-> map occupancy
-> design falsifier
-> audit commitment risk
-> decide DO / RESCOPE / HOLD / KILL
-> accept or reject artifact
-> convert failure into constraint
```

End with the single most important rule:

```text
Use this methodology when a claim, framing, direction, artifact, or commitment must survive intelligent attack before spending compute, reputation, or irreversible attention.
```

---

## Global Constraints

Apply these constraints to every output file:

1. Do not provide hidden reasoning traces.
2. Use public, auditable reasoning artifacts only.
3. Prefer tables, checklists, schemas, and decision rules.
4. Avoid generic advice.
5. Every operator must include a failure mode.
6. Every promoted claim must include a falsifier or evidence gate.
7. Every novelty claim must require an occupancy check.
8. Every artifact must have an acceptance test.
9. Every irreversible decision must have a reversible substitute or explicit gate.
10. Every section must include at least one tradeoff.
11. Stop expanding workflow unless the new step adds a kill condition, output schema, or decision boundary.
```

