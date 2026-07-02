# Agent Governance

## Purpose

Use this skill to decide which agent should generate, review, search, execute, or promote work.

The goal is not task scheduling. The goal is judgment hygiene:

- prevent self-review;
- prevent context contamination;
- prevent false promotion;
- prevent novelty-by-memory;
- prevent model agreement illusion;
- prevent cheap execution from pretending to be judgment.

## Trigger

Use this when:

- multiple models or agents are available;
- an artifact needs adversarial review;
- novelty or prior art is being judged;
- a generator wants to review its own output;
- one model's fluent agreement could bias the process;
- the project has promotion gates.

Do not use this when:

- the task is a small local edit;
- there is no judgment boundary;
- the output has no promotion risk.

## Agent Roles

| Role | Responsibility | Must Be Separated From |
| --- | --- | --- |
| Generator | Produce candidates, drafts, or implementations. | Final auditor. |
| Executor | Run code, experiments, formatting, or mechanical checks. | Claim owner. |
| Auditor | Attack claims and artifacts. | Generator context when possible. |
| Searcher | Verify current facts and prior art. | Memory-only novelty judgment. |
| Falsifier | Design kill experiments. | Demo builder. |
| Promoter | Decide whether to ship or commit. | Single-model agreement. |

## Governance Risks

| Risk | Symptom | Control |
| --- | --- | --- |
| Self-review | Same agent generates and approves. | Use separate auditor. |
| Context contamination | Auditor sees persuasive generation context. | Cold-start review packet. |
| False promotion | Weak idea becomes DO due to fluency. | Require falsifier and reviewer attack. |
| Novelty by memory | Agent claims novelty without search. | Require occupancy map and live search. |
| Agreement illusion | Multiple models agree because prompt framing is shared. | Use stance-separated prompts. |
| Execution masquerade | Passing tests treated as strategic validity. | Separate engineering verification from claim validation. |

## Procedure

1. Identify the decision to be made.
2. Identify whether the decision is generation, execution, search, audit, falsification, or promotion.
3. Assign an agent role.
4. Check for role conflicts.
5. Decide whether the auditor needs a cold-start packet.
6. Decide whether live search is required.
7. Decide whether Fable or human judgment is required.
8. Define the promotion gate.
9. Record contamination risks.

## Output Schema

```text
Decision:
Required role:
Proposed agent:
Role conflicts:
Context contamination risk:
Need cold-start audit: yes/no
Need live search: yes/no
Need adversarial stance: yes/no
Promotion gate:
Escalation target:
Governance verdict:
```

## Prompt

```text
Design agent governance for this decision.

Do not schedule tasks generically. Prevent judgment contamination.

For the decision below, specify:

1. Which role is needed: generator, executor, auditor, searcher, falsifier, or promoter.
2. Which agent should perform it.
3. Which agents must not perform it.
4. Whether a cold-start audit packet is required.
5. Whether live search is required.
6. Whether the same model is forbidden from self-review.
7. What promotion gate must be passed.
8. What contamination or agreement illusion risk exists.
9. Whether Fable or human judgment is required.
```

## Decision Rules

Use cold-start audit when:

- the generator produced persuasive framing;
- the claim affects promotion;
- the reviewer may inherit assumptions from the generator.

Require live search when:

- novelty is claimed;
- current literature matters;
- product, policy, legal, benchmark, or model status matters.

Require human judgment when:

- reputational risk is high;
- ethical or legal risk exists;
- the artifact will be externally published;
- the decision changes project direction.

## Failure Modes

- Treating more agents as better governance.
- Letting all agents see the same persuasive context.
- Asking an executor to make a taste judgment.
- Asking a generator to kill its own idea.
- Treating consensus as correctness.
- Escalating everything and slowing the system.

## Example

```text
Decision:
Promote "correction dynamics distillation" to a paper direction.

Required role:
Auditor + searcher + falsifier.

Role conflicts:
The generator cannot be final auditor.

Need cold-start audit:
Yes.

Need live search:
Yes, because novelty and occupancy matter.

Promotion gate:
Object survives deletion test, occupancy map, and minimum falsifier.

Escalation target:
Fable for contested framing; human for final promotion.
```

