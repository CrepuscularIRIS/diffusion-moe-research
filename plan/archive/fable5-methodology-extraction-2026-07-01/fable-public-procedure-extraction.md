# Fable Public Procedure Extraction

## Purpose

Use this document to ask Fable to turn a strong research audit into an auditable process manual.

The goal is not to obtain hidden chain-of-thought. The goal is to extract public decision operators that Opus can learn, test, and execute.

## Seven Components To Extract

| Component | Question To Ask | Purpose |
| --- | --- | --- |
| A. Stress-point scan | How do you detect pressure points in a field? | Generalize beyond one domain. |
| B. Object extraction | How do you decide the old object and the missing object? | Convert intuition into objects. |
| C. Deletion test | What remains if the new-object language is deleted? | Prevent concept laundering. |
| D. Occupancy hypothesis | Which literatures have probably already touched this object? | Prevent fake novelty. |
| E. Falsifier compression | How do you choose the cheapest kill experiment? | Prevent elegant but unfalsifiable ideas. |
| F. Rescope logic | Why is this RESCOPE rather than KILL? | Train judgment at the boundary. |
| G. Conversion law | How does a dead idea become a constraint or new candidate? | Turn failure into knowledge. |

## Prompt

```text
I do not want hidden chain-of-thought.

I want an auditable reconstruction of your public research procedure.

You just produced the research audit files. Now decompose how you did it into reusable cognitive operators.

For each section you wrote - operating logic, enrich audit, taste rubric, direction map, candidates, kill review, usage manual - answer:

1. Input signals used
   What concrete information did you rely on?

2. Decision operators applied
   What rule, heuristic, or test transformed the input into the output?

3. Alternatives considered and rejected
   What plausible interpretations did you discard, and why?

4. Kill / rescope trigger
   What exact observation moved the verdict toward DO, RESCOPE, HOLD, or KILL?

5. What would change your mind
   What live-search result, experiment result, or substrate change would reverse the verdict?

6. Reusable rule
   Compress this section into one operational rule that Opus could apply in another domain.

7. Failure mode of the rule
   When would this rule produce false negatives or false positives?

Do not narrate your private thoughts. Produce a process manual that can be audited, taught, and converted into skills.
```

## Required Output Schema

For each audit section, Fable should output:

```text
Section:
Input signals:
Decision operators:
Alternatives rejected:
Kill / rescope trigger:
Mind-changing evidence:
Reusable rule:
Failure mode:
Opus checklist:
```

## Quality Bar

The answer is useful only if it exposes decision boundaries.

Reject answers that:

- only summarize the previous files;
- use vague terms such as "interesting", "promising", or "elegant" without tests;
- produce a beautiful taxonomy without kill conditions;
- fail to name what evidence would reverse the verdict;
- fail to distinguish KILL from RESCOPE.

