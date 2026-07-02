# Context Compression State

## Purpose

Use this skill to compress a large context into a decision state, not a generic summary.

The output should preserve:

- the current thesis;
- open assumptions;
- resolved decisions;
- contradictions;
- dead regions;
- active candidates;
- pending falsifiers;
- the next irreversible decision.

This skill prevents summary drift, lost commitments, and repeated workflow loops.

## Trigger

Use this when:

- a conversation or document set exceeds working memory;
- several agents have produced outputs;
- the project is about to make a decision;
- prior conclusions may be lost after compaction;
- there are multiple candidate directions;
- the user asks "where are we?" or "what should happen next?"

Do not use this for ordinary summarization.

## Compression Target

Compress toward action, not coverage.

A good compression answers:

```text
What is currently believed?
What is still uncertain?
What has been rejected?
What decisions are binding?
What would be costly to change?
What must happen next?
```

## Procedure

1. Identify the current thesis.
2. Extract all explicit decisions already made.
3. Extract all open assumptions.
4. Extract contradictions or unresolved disagreements.
5. List dead regions:
   - killed ideas;
   - occupied claims;
   - rejected framings;
   - forbidden shortcuts.
6. List active candidates.
7. List pending falsifiers.
8. List evidence gaps.
9. Identify the next irreversible decision.
10. Write a compact state object that another agent can resume from.

## Output Schema

```text
Current thesis:

Resolved decisions:
- ...

Open assumptions:
- ...

Contradictions:
- ...

Dead regions:
- ...

Active candidates:
- ...

Pending falsifiers:
- ...

Evidence gaps:
- ...

Next irreversible decision:

Recommended next action:

Do-not-repeat:
- ...
```

## Decision-State Quality Bar

The compression is acceptable only if:

- it distinguishes dead regions from active candidates;
- it names the next decision, not just the next task;
- it preserves uncertainty;
- it can be used by a fresh agent without reading the full context;
- it does not re-open killed ideas without new evidence.

## Prompt

```text
Compress the following context into a decision state, not a summary.

Output:

1. Current thesis.
2. Resolved decisions.
3. Open assumptions.
4. Contradictions.
5. Dead regions.
6. Active candidates.
7. Pending falsifiers.
8. Evidence gaps.
9. Next irreversible decision.
10. Recommended next action.
11. Do-not-repeat list.

Preserve uncertainty and killed regions.
Do not produce a narrative summary.
Do not generate new ideas unless they are required by an unresolved decision.
```

## Failure Modes

- Producing a beautiful summary instead of a state object.
- Losing killed claims.
- Converting unresolved assumptions into facts.
- Forgetting the next decision.
- Treating all candidates as equally alive.
- Re-opening workflow design when execution should begin.

## Example State Object

```text
Current thesis:
Fable's value should be distilled into auditable protocols, not imitated as style.

Resolved decisions:
- Use external procedures, not hidden chain-of-thought.
- Opus executes stable checks.
- Fable handles contested judgment.
- Human controls promotion.

Open assumptions:
- Fable's prior-art judgment needs live-search support.
- Opus can learn boundary rules through calibration.

Dead regions:
- Generic idea lists.
- Ordinary summaries.
- Workflow expansion without new kill conditions.

Active candidates:
- Epistemic calibration.
- Agent governance.
- Artifact acceptance review.

Pending falsifiers:
- Blind Fable-vs-Opus verdict calibration.

Next irreversible decision:
Whether to turn these drafts into installed skills.

Recommended next action:
Run 10 calibration cases before installing permanent skills.
```

