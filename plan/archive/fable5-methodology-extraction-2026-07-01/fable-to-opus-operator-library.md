# Fable-to-Opus Operator Library

This library turns Fable's research taste into operators that Opus can execute mechanically.

Opus should not imitate Fable's style. Opus should execute these checks, produce auditable reports, and escalate only contested judgments.

## Verdict Labels

| Verdict | Meaning |
| --- | --- |
| DO | The object is plausibly under-modeled, occupied literature does not already solve it, and a cheap falsifier exists. |
| RESCOPE | The headline method is weak, occupied, or too broad, but a measurement, taxonomy, benchmark, constraint, or narrower object survives. |
| HOLD | The idea may be real, but evidence is insufficient, the falsifier is not cheap, or occupancy is unclear. |
| KILL | The object collapses into a trick, prior art likely owns it, no meaningful falsifier exists, or the value proposition dies under reviewer attack. |

## 1. Stress-Point Scan

Trigger: A domain or idea is proposed before any method design.

Required inputs:

- domain description;
- representative tasks and metrics;
- recent paper titles or abstracts when available;
- known practitioner complaints;
- target substrate such as hardware, benchmark, data, or deployment setting.

External procedure:

1. List the field's stated goal.
2. List the metrics that papers optimize.
3. Compare goal and metric.
4. Look for repeated patches, exceptions, and special-case modules.
5. Compare practitioner pain with paper claims.
6. Identify any substrate change that invalidates old assumptions.
7. Produce 2-4 pressure points before proposing any idea.

Output schema:

```text
Domain:
Stated goal:
Dominant metrics:
Stress points:
Evidence for each stress point:
Likely old object:
Possible missing object:
Do not generate ideas until:
```

Kill condition:

- No concrete stress point can be stated without vague language.

Common failure mode:

- Treating a popular topic as a stress point.

Escalate to Fable when:

- the domain has strong conflicting signals or requires object invention.

## 2. Metric-Goal Divergence Detection

Trigger: A benchmark or metric appears to reward behavior that differs from the real goal.

Required inputs:

- task goal;
- metric definition;
- examples of leaderboard optimization;
- known failure cases.

External procedure:

1. Write the real-world goal in one sentence.
2. Write what the metric actually measures.
3. List behaviors that improve the metric without improving the goal.
4. Check whether papers optimize those behaviors.
5. Identify the old object encoded by the metric.
6. Propose the missing object required by the real goal.

Output schema:

```text
Goal:
Metric:
Divergence:
Metric-hacking behavior:
Old object:
Missing object:
Test:
```

Kill condition:

- The metric aligns with the goal under realistic deployment conditions.

Common failure mode:

- Calling any imperfect metric divergent without showing a specific exploit.

Escalate to Fable when:

- the missing object is unclear but the divergence appears important.

## 3. Epicycle-Density Scan

Trigger: A field contains many patches, modules, losses, or exceptions.

Required inputs:

- method family;
- common add-ons;
- ablation patterns;
- failure modes.

External procedure:

1. List recurring patches.
2. Ask what failure each patch repairs.
3. Group patches by hidden cause.
4. Ask whether one missing object explains multiple patches.
5. Run a deletion test: if patch names disappear, what remains?

Output schema:

```text
Patch cluster:
Failures repaired:
Shared hidden cause:
Candidate missing object:
Deletion-test result:
```

Kill condition:

- The patches address independent engineering constraints rather than one missing object.

Common failure mode:

- Over-compressing unrelated improvements into one elegant theory.

Escalate to Fable when:

- several patch clusters can be compressed in competing ways.

## 4. Practitioner-Paper Gap

Trigger: Papers claim progress, but builders complain about different failures.

Required inputs:

- paper claims;
- practitioner reports;
- deployment logs or anecdotal failures;
- benchmark setup.

External procedure:

1. State the paper world's success condition.
2. State the practitioner's failure condition.
3. Identify what the benchmark cannot observe.
4. Map the hidden failure to a missing object.
5. Define a diagnostic benchmark or instrument.

Output schema:

```text
Paper success:
Practitioner failure:
Unobserved variable:
Missing object:
Diagnostic:
```

Kill condition:

- Practitioner complaints are caused by implementation quality, not a research object.

Common failure mode:

- Treating deployment annoyance as scientific novelty.

Escalate to Fable when:

- the gap suggests a new measurement regime rather than a method.

## 5. Substrate Cut

Trigger: A new substrate changes the cost, latency, data, compute, or interface assumptions of a field.

Required inputs:

- old substrate assumptions;
- new substrate constraints;
- system bottlenecks;
- method dependencies.

External procedure:

1. Describe the old substrate.
2. Describe the new substrate.
3. List assumptions invalidated by the change.
4. Identify methods that become impractical or newly possible.
5. Ask whether the old modeling object was tied to the old substrate.

Output schema:

```text
Old substrate:
New substrate:
Invalidated assumptions:
Old object at risk:
New object suggested:
System test:
```

Kill condition:

- The substrate change does not affect the bottleneck or evidence standard.

Common failure mode:

- Rebranding normal scaling as a substrate cut.

Escalate to Fable when:

- substrate change implies a new research program.

## 6. Modeling-Object Extraction

Trigger: An idea claims to be more than a new loss, module, or trick.

Required inputs:

- proposed idea;
- current method family;
- failure modes;
- claimed explanation.

External procedure:

1. State what current methods actually model.
2. State what the task truly needs.
3. Name the missing object.
4. Explain which failures the missing object predicts.
5. State which observations the missing object forbids.
6. Write a minimal experiment that tests the object, not the implementation.

Output schema:

```text
Old object:
Missing object:
Failure explained:
Forbidden observation:
Minimum object test:
Verdict:
```

Kill condition:

- The missing object cannot forbid any observable result.

Common failure mode:

- Renaming a method trick as an object.

Escalate to Fable when:

- the missing object is conceptually new or contested.

## 7. Deletion Test

Trigger: A candidate uses elegant object language.

Required inputs:

- candidate description;
- core terms;
- implementation sketch;
- expected effects.

External procedure:

1. Remove the new-object vocabulary.
2. Rewrite the candidate in plain method language.
3. Ask whether any prediction, constraint, or diagnostic disappears.
4. If nothing disappears, mark laundering risk.
5. If a testable prediction disappears, keep the object alive.

Output schema:

```text
Original object language:
Plain rewrite:
What disappeared:
Laundering risk:
Surviving prediction:
Verdict:
```

Kill condition:

- The candidate is unchanged after object language is removed.

Common failure mode:

- Being too harsh on early object language before it has been operationalized.

Escalate to Fable when:

- the idea is conceptually strong but currently under-specified.

## 8. Occupancy Hypothesis

Trigger: A candidate appears novel.

Required inputs:

- missing object;
- adjacent literatures;
- keywords;
- likely older names for the same object.

External procedure:

1. Generate likely prior-art names.
2. Generate search queries.
3. Identify literatures that must have touched the object.
4. Predict what prior art probably owns.
5. Separate method occupancy from measurement occupancy.
6. Decide whether novelty survives as method, benchmark, taxonomy, or instrument.

Output schema:

```text
Object:
Likely prior names:
Search queries:
Occupied territory:
Surviving territory:
Required live search:
```

Kill condition:

- The entire object and its proposed falsifier are already occupied.

Common failure mode:

- Missing prior art because it uses different vocabulary.

Escalate to Fable when:

- live search finds strong adjacent work but boundary remains ambiguous.

## 9. Minimum Falsifier Compression

Trigger: A candidate survives initial object and occupancy checks.

Required inputs:

- candidate object;
- predicted effect;
- baseline;
- available compute and data;
- evaluation target.

External procedure:

1. State the one claim that must be true.
2. State the cheapest setting where it should appear.
3. Select the strongest dumb baseline.
4. Define the result that kills the claim.
5. Cap the experiment at a small budget.
6. Reject experiments that only show possible upside.

Output schema:

```text
Core claim:
Cheapest testbed:
Baseline:
Kill result:
Survival result:
Budget:
Decision after test:
```

Kill condition:

- No cheap experiment can distinguish the object from a trick.

Common failure mode:

- Designing a demonstration instead of a falsifier.

Escalate to Fable when:

- the only falsifier requires a large benchmark or new infrastructure.

## 10. Reviewer Attack

Trigger: Before promoting a candidate to DO.

Required inputs:

- candidate report;
- falsifier;
- occupancy map;
- claimed contribution.

External procedure:

1. Attack novelty.
2. Attack necessity.
3. Attack measurement validity.
4. Attack baseline strength.
5. Attack scope creep.
6. Attack whether the object predicts anything.
7. Convert unresolved attacks into HOLD, RESCOPE, or KILL.

Output schema:

```text
Attack:
Evidence:
Candidate response:
Unresolved risk:
Verdict impact:
```

Kill condition:

- A basic reviewer attack removes the contribution.

Common failure mode:

- Producing adversarial rhetoric without concrete evidence.

Escalate to Fable when:

- the attack is strong but the candidate may be reframed.

## 11. Rescope-Or-Kill Decision

Trigger: A candidate fails as originally framed.

Required inputs:

- killed component;
- surviving observation;
- occupancy map;
- possible contribution types.

External procedure:

1. Identify exactly what died.
2. Identify what observation remains unexplained.
3. Ask whether the survivor is a contribution type: measurement, benchmark, taxonomy, instrument, constraint, or narrower object.
4. If the survivor has its own falsifier, choose RESCOPE.
5. If the survivor has no independent value, choose KILL.

Output schema:

```text
Killed part:
Surviving part:
New contribution type:
Independent falsifier:
Rescope statement:
Final verdict:
```

Kill condition:

- The survivor is only a weaker version of the dead claim.

Common failure mode:

- Keeping a dead idea alive through vague narrowing.

Escalate to Fable when:

- method dies but measurement may survive.

## 12. Failure Conversion Law

Trigger: An idea receives RESCOPE or KILL.

Required inputs:

- failure reason;
- killed claim;
- surviving constraint;
- possible neighboring domains.

External procedure:

1. Name the failure precisely.
2. Convert failure into a constraint.
3. Ask which future candidates must obey this constraint.
4. Ask whether the failure reveals a benchmark, taxonomy, or diagnostic.
5. Store the conversion as reusable knowledge.

Output schema:

```text
Dead claim:
Failure reason:
Converted constraint:
New candidate type:
Future exclusion rule:
```

Kill condition:

- The failure does not generalize beyond this candidate.

Common failure mode:

- Treating every failure as profound.

Escalate to Fable when:

- the failure suggests a new object or research program.

