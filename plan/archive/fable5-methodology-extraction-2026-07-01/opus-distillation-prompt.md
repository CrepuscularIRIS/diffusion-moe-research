# Opus Distillation Prompt

Use this prompt after Fable has produced the audit files and the public procedure extraction.

The goal is not to make Opus sound like Fable. The goal is to make Opus execute Fable's external protocol reliably.

## Prompt

```text
You are Opus operating inside my Research-OS.

Your job is not to imitate Fable's style. Your job is to distill Fable's research procedure into stable executable skills.

Read the attached Fable audit files and extract a reusable protocol for cross-domain research ideation and falsification.

Output:

1. Fable-to-Opus Operator Library

Extract 8-12 operators such as:

- stress-point scan;
- metric-goal divergence detection;
- epicycle-density scan;
- practitioner-paper gap;
- substrate cut;
- modeling-object extraction;
- deletion test;
- occupancy hypothesis;
- minimum falsifier compression;
- reviewer attack;
- rescope decision;
- conversion law.

For each operator, specify:

- trigger;
- required inputs;
- step-by-step external procedure;
- output schema;
- kill condition;
- common failure mode;
- when to escalate back to Fable.

2. Skill Files Draft

Convert the operators into `.claude/skills`-style prompt modules:

- `stress-point-scan`;
- `object-deletion-test`;
- `occupancy-hypothesis`;
- `minimum-falsifier`;
- `rescope-or-kill`;
- `failure-conversion`;
- `cross-domain-enrich`.

3. Meta-Skill Files Draft

Convert Fable's broader long-range work capabilities into second-layer skill modules:

- `epistemic-calibration`;
- `context-compression-state`;
- `agent-governance`;
- `artifact-acceptance-review`;
- `cross-domain-operator-transfer`;
- `irreversible-decision-audit`.

For each meta-skill, specify:

- trigger;
- required inputs;
- step-by-step external procedure;
- output schema;
- automatic HOLD / RESCOPE / KILL conditions;
- escalation rules;
- common failure modes;
- anti-loop condition.

4. Opus Execution Rules

Define what Opus is allowed to decide mechanically, and what must be escalated to Fable or human.

5. Calibration Suite

Create 10 test cases from different domains:

- VLA;
- MLLM fusion;
- Diffusion LLM;
- SFT distillation;
- benchmark evaluation;
- information compression;
- graph/tree/matrix representation;
- autonomous research workflow;
- medical AI;
- recommender systems.

For each test case, provide the expected verdict pattern: DO / RESCOPE / HOLD / KILL, and the reason.

6. Generalized Cross-Domain Protocol

Give the final protocol for applying the `enrich.md` methodology to any new field.

Important:

- Do not produce new research ideas unless required by the protocol.
- Do not write beautiful methodology prose.
- Convert Fable's taste into executable checks.
- Default to KILL or RESCOPE when evidence is insufficient.
- Escalate to Fable only for contested judgment, object invention, or adversarial reframing.
```

## Expected Opus Failure Modes

Watch for:

- being too permissive and promoting weak ideas to DO;
- treating RESCOPE as DO;
- skipping the occupancy hypothesis;
- writing falsifiers that are actually demonstrations;
- preserving beautiful language after the deletion test fails;
- failing to separate method novelty from measurement novelty;
- escalating too late when object invention is required.

## Acceptance Criteria

The Opus output is acceptable only if:

- every operator has a trigger and output schema;
- every promoted candidate has a minimum falsifier;
- every novelty claim has an occupancy map;
- every RESCOPE states what died and what survived;
- every KILL produces a reusable exclusion rule when possible;
- every escalation condition is explicit.
