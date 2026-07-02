# Fable Part Follow-Up Prompts

Use one prompt at a time. Do not ask Fable to answer every module in one pass, because that tends to produce a polished summary instead of operational detail.

## 0. Operating Logic

```text
Focus only on `0-operating-logic.md`.

You claimed that you start from:

- metric-goal divergence;
- epicycle density;
- practitioner-paper gap;
- substrate cut.

I want to know how to operationalize this in any new field.

For each of the four signals:

1. Define the signal precisely.
2. Give 3 observable symptoms in a literature landscape.
3. Give 3 search queries that would reveal it.
4. Give 2 false-positive cases where the signal looks present but is not.
5. Give 1 example from VLA, MLLM, Diffusion LLM, or dataset evaluation.
6. Show how this signal leads to an old modeling object.
7. Show how this signal suggests a missing object.
8. State what experiment would test whether the missing object is real.
9. Convert the signal into a reusable Opus checklist.

End with a general algorithm:

Given a new domain D, how should Opus scan for stress points before generating any idea?

Do not provide hidden chain-of-thought. Provide an auditable external procedure.
```

## 1. Audit of Enrich

```text
Focus only on `1-audit-of-enrich.md`.

You warned that an old-object / new-object table can become post-hoc object laundering.

Operationalize this warning.

Answer:

1. What is post-hoc object laundering?
2. What observable symptoms indicate that a proposed object shift is only a renamed trick?
3. What deletion test should Opus run?
4. What would remain after deleting the new-object language in a genuine object shift?
5. What would remain after deleting it in a fake object shift?
6. Give 3 examples: one genuine shift, one fake shift, and one borderline RESCOPE case.
7. What reviewer attack would expose laundering?
8. What minimum experiment would separate a real missing object from a vocabulary upgrade?
9. Convert the result into a checklist for Opus.

End with an output schema for an object-audit report.
```

## 2. Taste Rubric

```text
Focus only on `2-taste-rubric.md`.

You defined research taste as predictive kill accuracy, not aesthetic preference.

For each criterion in the taste rubric:

1. Define the criterion in operational terms.
2. Specify the boundary between weak, acceptable, and strong.
3. Give a false-positive example.
4. Give a false-negative example.
5. State what evidence would demote a candidate.
6. State what evidence would promote a candidate.
7. Give a reviewer-style attack question.
8. Convert the criterion into a scoring rule Opus can apply mechanically.

Then provide:

- a 0-2 scoring table;
- automatic KILL conditions;
- automatic RESCOPE conditions;
- escalation conditions for Fable or human judgment.
```

## 3. Direction Map

```text
Focus only on `3-direction-map.md`.

You converted a list of research directions into DO / RESCOPE / HOLD / KILL verdicts.

Explain the procedure.

For each direction:

1. What field-level pressure point was detected?
2. What old object is the field probably over-modeling?
3. What missing object might matter?
4. What occupancy risk exists?
5. What minimum falsifier exists?
6. What made the verdict DO, RESCOPE, HOLD, or KILL?
7. What evidence would reverse the verdict?
8. What would be the safest rescope if the original idea is occupied?

End with a reusable domain-verdict algorithm for Opus.
```

## 4. Candidates

```text
Focus only on `4-candidates.md`.

You generated a small number of candidate objects rather than a large list of ideas.

Operationalize that constraint.

Answer:

1. How did you avoid generating 20 surface ideas?
2. What made a candidate a modeling object rather than a method trick?
3. What did each candidate explain that the old object failed to explain?
4. What is the deletion test for each candidate?
5. What literature occupancy did you assume?
6. What cheap falsifier did you require?
7. What would make each candidate become a measurement paper instead of a method paper?
8. What would make each candidate die completely?

End with a candidate-generation protocol that limits Opus to 3 objects before any method design.
```

## 5. Kill Review

```text
Focus only on `5-kill-review.md`.

You sometimes chose RESCOPE instead of KILL.

I want the boundary rule.

For each reviewed candidate:

1. What part was killed?
2. What part survived?
3. Why was the surviving part not just a weaker version of the dead idea?
4. What evidence forced RESCOPE rather than DO?
5. What evidence prevented KILL?
6. What would make the rescope no longer valuable?
7. What conversion law turned the dead method into a constraint, measurement, benchmark, or taxonomy?
8. What reviewer attack should Opus run before accepting RESCOPE?

End with a RESCOPE-vs-KILL decision tree.
```

## 6. Usage Manual

```text
Focus only on `6-usage-manual.md`.

Convert the usage manual into Opus-executable skills.

For each call mode:

- Adversarial Object Audit;
- Kill-Experiment Design;
- Reviewer Simulation;
- Failure-to-Candidate Autopsy;
- Occupancy Map;

provide:

1. Trigger condition.
2. Required inputs.
3. Step-by-step external procedure.
4. Output schema.
5. Automatic KILL condition.
6. Automatic RESCOPE condition.
7. Failure mode.
8. When Opus must escalate back to Fable or human judgment.

End with a minimal command set:

- `/enrich-scan`;
- `/object-audit`;
- `/deletion-test`;
- `/occupancy-hypothesis`;
- `/minimum-falsifier`;
- `/rescope-or-kill`;
- `/failure-conversion`;
- `/domain-transfer-enrich`.
```

