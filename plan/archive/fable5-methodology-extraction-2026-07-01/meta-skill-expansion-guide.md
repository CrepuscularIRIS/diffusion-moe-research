# Meta-Skill Expansion Guide

This file adds six high-level capabilities to the first Research-OS skill layer.

The purpose is not to create an infinite workflow. The purpose is to capture the parts of Fable that matter for long-range research work:

- what to believe;
- what to remember;
- who should judge;
- whether an artifact is shippable;
- how to transfer operators across domains;
- what decisions must not be made too early.

## Added Meta-Skills

| Skill | Core Question | Main Failure Prevented |
| --- | --- | --- |
| `epistemic-calibration.md` | What do we know, guess, need to search, or need to test? | Novelty-by-memory and overclaiming. |
| `context-compression-state.md` | What is the current decision state after a large context? | Summary drift and lost commitments. |
| `agent-governance.md` | Which model or actor should do which judgment? | Self-review and context contamination. |
| `artifact-acceptance-review.md` | Is this artifact ready for another person to use? | Shipping unclear or unsupported work. |
| `cross-domain-operator-transfer.md` | How does a research operator transfer outside research? | Mistaking vocabulary transfer for real transfer. |
| `irreversible-decision-audit.md` | Which next steps lock the path or risk reputation, compute, or evidence quality? | Premature commitment. |

## When To Use This Layer

Use the meta-skill layer when the question is not only "what is the idea?", but one of:

- Can this claim be trusted?
- What should remain in working memory?
- Should the same model be allowed to judge its own output?
- Is this artifact shippable?
- Does this operator transfer to another domain?
- Will this decision lock the project into a weak path?

## When Not To Use This Layer

Do not use these skills for:

- ordinary coding;
- ordinary summarization;
- ordinary idea lists;
- generic literature overviews;
- UI generation;
- making a plan that no one will execute;
- confirming a belief already held by the user.

## Integration With The Existing Protocol

The first Research-OS layer is:

```text
Domain / Idea
-> Stress-point scan
-> Object extraction
-> Deletion test
-> Occupancy hypothesis
-> Minimum falsifier
-> Reviewer attack
-> DO / RESCOPE / HOLD / KILL
-> Conversion law
```

The meta-skill layer wraps it:

```text
Before:
epistemic calibration
agent governance
irreversibility audit

During:
context compression state
cross-domain operator transfer

After:
artifact acceptance review
failure conversion
calibration update
```

## Standard Meta-Skill Report Header

Every meta-skill should start with:

```text
Task:
Decision needed:
Available evidence:
Uncertainty source:
Who is allowed to decide:
What output will be actionable:
```

## Standard Verdicts

| Verdict | Meaning |
| --- | --- |
| ACCEPT | The artifact, claim, decision, or transfer is ready under stated limits. |
| REVISE | The core is useful but needs explicit fixes before use. |
| HOLD | Evidence is insufficient; search, experiment, or human input is needed. |
| RESCOPE | The original target is too broad, but a narrower useful version survives. |
| KILL | The claim, artifact, transfer, or decision should not proceed. |

## Escalation Rule

Opus can execute the checklist. Fable or a human should be used when:

- object invention is required;
- novelty depends on ambiguous prior art;
- the artifact could affect reputation;
- the decision is hard to reverse;
- multiple agents disagree;
- the evidence grade is low but commitment cost is high.

## Anti-Loop Rule

Stop expanding workflow when:

- the next document would only rename an existing operator;
- no new kill condition is added;
- no new output schema is added;
- the new process does not change a decision;
- the process makes the system feel safer without reducing false promotion.

