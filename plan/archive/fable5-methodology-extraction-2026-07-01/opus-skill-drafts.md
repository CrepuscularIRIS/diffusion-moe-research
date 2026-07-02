# Opus Skill Drafts

These are skill-style prompt modules for Opus. They are not final installed skills. They are drafts that can be copied into a skill system.

## Skill Layers

Layer 1 handles research ideation and falsification:

- `stress-point-scan`;
- `object-deletion-test`;
- `occupancy-hypothesis`;
- `minimum-falsifier`;
- `rescope-or-kill`;
- `failure-conversion`;
- `cross-domain-enrich`.

Layer 2 handles epistemic hygiene, context state, governance, artifact acceptance, transfer, and irreversibility:

- `epistemic-calibration`;
- `context-compression-state`;
- `agent-governance`;
- `artifact-acceptance-review`;
- `cross-domain-operator-transfer`;
- `irreversible-decision-audit`.

Use Layer 2 around Layer 1 when the decision affects belief, memory, model assignment, shipping, cross-domain reuse, or commitment risk.

## Skill: stress-point-scan

Trigger:

- A new domain or idea is proposed.
- The user asks for research directions before any specific method exists.

Inputs:

- domain name;
- target task;
- dominant metrics;
- known failures;
- practitioner complaints;
- recent literature if available.

Procedure:

1. State the field's real goal.
2. State what the dominant metric rewards.
3. Detect metric-goal divergence.
4. Detect epicycle density.
5. Detect practitioner-paper gap.
6. Detect substrate cut.
7. Produce 2-4 stress points.
8. Do not generate ideas yet.

Output:

```text
Domain:
Goal:
Metric:
Stress points:
Evidence:
Likely old object:
Candidate missing object:
Required next check:
```

Automatic KILL:

- No stress point can be stated concretely.

Escalate:

- Multiple incompatible missing objects look plausible.

## Skill: object-deletion-test

Trigger:

- A candidate claims to be a modeling-object shift.

Inputs:

- candidate description;
- old object;
- new object;
- claimed failure explanation;
- implementation sketch.

Procedure:

1. Remove the new-object vocabulary.
2. Rewrite the idea as a plain method.
3. Ask whether any prediction disappears.
4. Ask whether any forbidden observation disappears.
5. If nothing changes, mark post-hoc object laundering.
6. If a falsifiable constraint disappears, preserve the object.

Output:

```text
Object language:
Plain rewrite:
What disappeared:
Prediction preserved:
Forbidden observation:
Laundering risk:
Verdict:
```

Automatic KILL:

- The idea is unchanged after deletion.

Automatic RESCOPE:

- The method dies, but the deletion test reveals a measurement or diagnostic.

Escalate:

- Object language is weak but may point to a real missing object.

## Skill: occupancy-hypothesis

Trigger:

- A candidate appears novel.

Inputs:

- candidate object;
- domain;
- likely adjacent literatures;
- keywords;
- possible older names.

Procedure:

1. Generate 5-10 likely prior-art search queries.
2. List adjacent literatures that probably touched the object.
3. Predict what those literatures likely own.
4. Separate method occupancy from measurement occupancy.
5. Require live search before promotion to DO.
6. State what novelty could survive.

Output:

```text
Object:
Likely prior names:
Search queries:
Expected occupied territory:
Potential surviving territory:
Live-search requirement:
Verdict before search:
```

Automatic HOLD:

- Occupancy cannot be assessed without search.

Automatic KILL:

- Search shows the object, method, and falsifier are all already owned.

Escalate:

- Prior art is close but the surviving measurement boundary is unclear.

## Skill: minimum-falsifier

Trigger:

- A candidate has survived object extraction and occupancy checks.

Inputs:

- core claim;
- predicted effect;
- strongest baseline;
- available compute;
- target dataset or toy setting;
- failure mode.

Procedure:

1. Write the core claim in one sentence.
2. Choose the cheapest setting where the claim should appear.
3. Choose a strong dumb baseline.
4. Define the kill result.
5. Define the survival result.
6. Set a budget cap.
7. Reject tests that only demonstrate upside.

Output:

```text
Core claim:
Cheapest test:
Baseline:
Kill result:
Survival result:
Budget:
Decision rule:
```

Automatic KILL:

- No cheap falsifier can distinguish the object from a trick.

Automatic HOLD:

- The falsifier requires large infrastructure.

Escalate:

- The falsifier itself may be a publishable benchmark or instrument.

## Skill: rescope-or-kill

Trigger:

- A candidate fails as originally framed.

Inputs:

- failed claim;
- failure evidence;
- surviving observation;
- occupancy map;
- possible contribution types.

Procedure:

1. Name the killed component.
2. Name the surviving component.
3. Ask whether the survivor has independent value.
4. Ask whether it has its own falsifier.
5. Map the survivor to method, measurement, benchmark, taxonomy, instrument, or constraint.
6. Choose RESCOPE only if the survivor can stand alone.
7. Choose KILL if the survivor is only a weaker version of the dead claim.

Output:

```text
Killed component:
Surviving component:
Contribution type:
Independent falsifier:
Rescope statement:
Final verdict:
```

Automatic RESCOPE:

- Method novelty dies but measurement novelty survives.

Automatic KILL:

- Nothing survives except a softer claim.

Escalate:

- The boundary between measurement and method contribution is contested.

## Skill: failure-conversion

Trigger:

- A candidate is RESCOPE or KILL.

Inputs:

- failed claim;
- failure reason;
- evidence;
- related future directions.

Procedure:

1. Write the failed claim.
2. Write the failure reason.
3. Convert the failure into a constraint.
4. Identify future ideas that the constraint rules out.
5. Identify whether the failure suggests a benchmark, diagnostic, or taxonomy.
6. Store the conversion as a reusable rule.

Output:

```text
Dead claim:
Failure reason:
Converted constraint:
Future exclusion rule:
New candidate type:
```

Automatic KILL:

- The failure does not generalize.

Escalate:

- The failure suggests a new modeling object.

## Skill: cross-domain-enrich

Trigger:

- The user wants to apply the `enrich.md` methodology to a new field.

Inputs:

- domain;
- target task;
- known methods;
- metrics;
- failures;
- deployment context;
- compute and data constraints.

Procedure:

1. Run stress-point scan.
2. Build object inventory.
3. Build failure inventory.
4. Propose at most 3 missing objects.
5. Run deletion test.
6. Run occupancy hypothesis.
7. Define minimum falsifier.
8. Run reviewer attack.
9. Decide DO / RESCOPE / HOLD / KILL.
10. Convert failure into reusable constraints.

Output:

```text
Domain:
Stress points:
Old objects:
Failure inventory:
Candidate missing objects:
Deletion-test result:
Occupancy map:
Minimum falsifier:
Reviewer attack:
Verdict:
Conversion law:
Next action:
```

Automatic KILL:

- No missing object survives deletion and reviewer attack.

Automatic RESCOPE:

- The object is occupied as a method but survives as measurement, taxonomy, or benchmark.

Escalate:

- New object invention, contested verdict, or adversarial reframing is required.
