# Executable Enrich Protocol

This document turns the `enrich.md` methodology into a repeatable protocol for cross-domain research ideation and falsification.

The protocol starts from stress points, not ideas.

```text
Domain / Idea
-> Stress-point scan
-> Old object / new object extraction
-> Deletion test
-> Occupancy hypothesis + live-search query set
-> Minimum falsifier
-> Reviewer attack
-> DO / RESCOPE / HOLD / KILL
-> Conversion law
```

## Input Packet

Every run should start with:

```text
Domain:
Candidate idea, if any:
Target task:
Real-world goal:
Dominant metric:
Known failures:
Representative methods:
Deployment or substrate constraints:
Available compute / data:
Desired output type:
```

## Step 1. Field Stress Scan

Question:

```text
Where is the field under pressure?
```

Check:

- metric-goal divergence;
- epicycle density;
- practitioner-paper gap;
- substrate cut.

Output:

```text
Stress point:
Observed symptoms:
Likely old object:
Potential missing object:
Search queries:
```

Rule:

Do not generate a research idea until at least one stress point is concrete.

## Step 2. Object Inventory

Question:

```text
What are mainstream methods actually modeling?
```

Examples of old objects:

- closed-set posterior;
- next-token likelihood;
- average benchmark score;
- static sample quality;
- endpoint answer;
- single-modality embedding;
- one-step policy success.

Output:

```text
Old object:
Why the field models it:
What it explains:
What it fails to explain:
```

Rule:

If the old object cannot be stated, the idea is not ready.

## Step 3. Failure Inventory

Question:

```text
Which failures repeatedly appear but are not explained by the old objective?
```

Output:

```text
Failure:
Old-object explanation:
Why explanation is insufficient:
Missing variable:
Diagnostic evidence:
```

Rule:

A candidate object must explain at least one repeated failure better than the old object.

## Step 4. Candidate Missing Object

Question:

```text
Is there a more natural object: support, field, trajectory, instrument, recovery, geometry, causal invariant, or pressure-aware benchmark?
```

Output:

```text
Candidate object:
Failure explained:
Prediction:
Forbidden observation:
Potential contribution type:
```

Rule:

Generate at most 3 candidate objects before method design.

## Step 5. Occupancy Map

Question:

```text
Which literatures already occupy this object?
```

Output:

```text
Object:
Likely older names:
Adjacent literatures:
Search queries:
Likely occupied territory:
Potential surviving territory:
Live-search requirement:
```

Rule:

No DO verdict is allowed without an occupancy hypothesis. For current fields, live search is required before strong novelty claims.

## Step 6. Deletion Test

Question:

```text
If we delete the object language, is anything lost?
```

Output:

```text
Original language:
Plain rewrite:
Lost prediction:
Lost constraint:
Laundering risk:
Verdict impact:
```

Rule:

If deletion changes nothing, mark KILL unless measurement or diagnostic value survives.

## Step 7. Minimum Falsifier

Question:

```text
What is the cheapest experiment that would kill this idea?
```

Output:

```text
Core claim:
Cheapest testbed:
Strong baseline:
Kill result:
Survival result:
Budget:
```

Rule:

Prefer a 48-100 GPU-hour falsifier when possible. If the first test requires a large benchmark, mark HOLD or convert to infrastructure.

## Step 8. Reviewer Attack

Question:

```text
How would a strong reviewer reject this?
```

Attack:

- novelty;
- necessity;
- baseline;
- measurement;
- scope;
- causal explanation;
- deployment relevance.

Output:

```text
Attack:
Evidence:
Candidate response:
Unresolved risk:
Verdict impact:
```

Rule:

If a basic reviewer attack removes the contribution, choose KILL or RESCOPE.

## Step 9. Verdict

Use:

```text
DO:
The object survives deletion, occupancy, falsifier, and reviewer attack.

RESCOPE:
The original method dies, but a narrower object, measurement, benchmark, taxonomy, instrument, or constraint survives.

HOLD:
The object might be real, but evidence, occupancy, or falsifier quality is insufficient.

KILL:
The object collapses into a trick, prior art owns it, no falsifier exists, or reviewer attack removes the value.
```

Output:

```text
Verdict:
What survives:
What dies:
Required next evidence:
Do-not-claim boundary:
```

## Step 10. Conversion Law

Question:

```text
If the idea dies, what knowledge remains?
```

Output:

```text
Dead claim:
Failure reason:
Converted constraint:
New measurement or taxonomy:
Future exclusion rule:
```

Rule:

Do not waste failure. Convert it into a constraint, benchmark need, taxonomy, or exclusion rule.

## Domain Transfer Templates

### VLA

Do not start with:

```text
Design a new policy.
```

Start with:

```text
Which embodied failures do current benchmarks fail to instrument?
Which failures are grounding failures, planning failures, perception failures, or control failures?
```

Likely rescope:

- benchmark instrument;
- sim-to-real failure taxonomy;
- grounding failure decomposition.

### MLLM

Do not start with:

```text
Add information geometry fusion.
```

Start with:

```text
Which hallucination or conflict case requires cross-modal evidence routing?
```

Likely rescope:

- modality conflict resolution;
- hallucination attribution;
- cross-modal calibration.

### Diffusion LLM

Do not start with:

```text
Invent a new sampler trick.
```

Start with:

```text
Is performance sampler-limited or model-limited?
```

Likely rescope:

- oracle-gap decomposition;
- sampler-limited versus model-limited measurement.

### SFT Distillation

Do not start with:

```text
Make the student more like the teacher.
```

Start with:

```text
Can recovery operators or correction dynamics be separated from answer imitation?
```

Likely falsifier:

- corrupted-reasoning recovery test.

### Dataset Evaluation

Do not start with:

```text
Create a data quality score.
```

Start with:

```text
How does the benchmark behave under optimization pressure?
```

Likely contribution:

- anti-Goodhart benchmark;
- pressure-aware dataset evaluation;
- failure-mode coverage metric.

### Research-OS

Do not start with:

```text
Build an autonomous scientist.
```

Start with:

```text
Does the system reduce false promotion of weak ideas under adversarial review?
```

Likely falsifier:

- blind verdict calibration against Fable, experts, or later evidence.

## Final Report Template

```text
Domain:
Candidate:

1. Stress-point scan
2. Old object inventory
3. Failure inventory
4. Candidate missing objects
5. Occupancy hypothesis
6. Deletion test
7. Minimum falsifier
8. Reviewer attack
9. Verdict
10. Conversion law

Next action:
Escalation required:
```

