# Artifact Acceptance Review

## Purpose

Use this skill to decide whether an artifact is ready for another person to use.

This applies to:

- paper drafts;
- experiment reports;
- READMEs;
- system architectures;
- demos;
- benchmarks;
- skills;
- prompt packs;
- frontend pages;
- research logs.

The review asks whether the artifact is usable, supported, explicit, and safe to ship under its stated scope.

## Trigger

Use this when:

- a document, system, demo, or result is about to be shared;
- a skill or prompt pack is about to become reusable;
- an experiment report will support a claim;
- an artifact may influence future decisions;
- a hostile reader could misunderstand the claim.

Do not use this for throwaway notes unless they will be reused.

## Acceptance Questions

```text
Is this artifact usable by another person?
What claim does it make?
What evidence supports the claim?
What is missing before shipping?
What would a hostile reader misunderstand?
What must be cut?
What must be made explicit?
Ship / revise / kill?
```

## Procedure

1. Identify artifact type.
2. Identify target user.
3. State the artifact's claim.
4. State what the artifact enables the user to do.
5. Check whether inputs are specified.
6. Check whether outputs are specified.
7. Check whether evidence supports the claim.
8. Check whether limitations are explicit.
9. Run hostile-reader misunderstanding.
10. Identify missing acceptance tests.
11. Decide SHIP / REVISE / HOLD / KILL.

## Output Schema

```text
Artifact:
Artifact type:
Target user:
Primary claim:
Enabled action:
Supporting evidence:
Missing evidence:
Ambiguity:
Hostile-reader misunderstanding:
What must be cut:
What must be made explicit:
Acceptance tests:
Verdict:
Required changes:
```

## Verdict Rules

SHIP if:

- the target user is clear;
- the claim is explicit;
- the artifact can be used without hidden context;
- evidence and limitations are stated;
- no critical misunderstanding remains.

REVISE if:

- the core artifact is useful but unclear, underspecified, or overclaimed.

HOLD if:

- evidence is missing and the artifact would guide decisions.

KILL if:

- the artifact's claim is unsupported;
- the artifact is redundant with existing materials;
- the artifact creates more confusion than action;
- the artifact cannot pass a hostile-reader check.

## Prompt

```text
Review this artifact for acceptance.

Do not praise it. Decide whether another person can use it safely.

Output:

1. Artifact type.
2. Target user.
3. Primary claim.
4. Enabled action.
5. Supporting evidence.
6. Missing evidence.
7. Ambiguity.
8. Hostile-reader misunderstanding.
9. What must be cut.
10. What must be made explicit.
11. Acceptance tests.
12. Verdict: SHIP / REVISE / HOLD / KILL.
13. Required changes.
```

## Artifact-Specific Checks

### Paper Draft

- Is the contribution type explicit?
- Is the claim narrower than the evidence?
- Are baselines and prior art adequate?
- Is the falsifier acknowledged?
- Would a reviewer understand why this is not a trick?

### Experiment Report

- Is the hypothesis stated before results?
- Are baselines strong enough?
- Are failure cases included?
- Are negative results preserved?
- Does the report distinguish observation from explanation?

### README

- Can a new user run it?
- Are prerequisites listed?
- Are commands copyable?
- Is the expected output shown?
- Are known limitations stated?

### Skill

- Does it have a trigger?
- Does it define required inputs?
- Does it provide an output schema?
- Does it have kill or escalation conditions?
- Does it prevent its own common failure modes?

### Demo

- Does the demo prove the claim or only show a happy path?
- Is the setup reproducible?
- Are edge cases visible?
- Is the user journey clear?
- Does it avoid overclaiming production readiness?

## Failure Modes

- Treating polish as readiness.
- Treating length as completeness.
- Shipping without target user.
- Hiding limitations.
- Confusing internal notes with reusable artifacts.
- Accepting a prompt pack with no calibration.

