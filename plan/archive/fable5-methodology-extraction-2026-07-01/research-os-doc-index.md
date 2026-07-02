# Research-OS Document Index

These files operationalize the `enrich.md` methodology into auditable prompts, operator libraries, calibration tasks, and skill drafts.

Use them in this order:

1. `fable-public-procedure-extraction.md`
   Ask Fable to externalize its public research procedure without hidden chain-of-thought.

2. `fable-part-followup-prompts.md`
   Ask Fable one focused follow-up at a time for each audit file.

3. `fable-to-opus-operator-library.md`
   Use the extracted procedure as a stable operator library for Opus.

4. `opus-distillation-prompt.md`
   Give Opus the Fable audit files and ask it to convert taste into executable checks.

5. `opus-skill-drafts.md`
   Convert the operator library into skill-style prompt modules.

6. `fable-opus-calibration-suite.md`
   Build a calibration set to compare Fable verdicts and Opus verdicts.

7. `executable-enrich-protocol.md`
   Apply the final cross-domain protocol to any new field or idea.

8. `meta-skill-expansion-guide.md`
   Add the second-layer meta-skills without entering workflow expansion loops.

9. `epistemic-calibration.md`
   Decide what is known, guessed, searchable, testable, or blocked.

10. `context-compression-state.md`
    Compress long context into a decision state rather than a generic summary.

11. `agent-governance.md`
    Assign generator, auditor, searcher, falsifier, executor, and promoter roles without judgment contamination.

12. `artifact-acceptance-review.md`
    Decide whether a paper, report, README, demo, benchmark, skill, prompt pack, or log is shippable.

13. `cross-domain-operator-transfer.md`
    Transfer research operators into product, engineering, design, education, business, and organization decisions.

14. `irreversible-decision-audit.md`
    Identify decisions that lock path, reputation, compute, evidence, or narrative.

15. `fable5-research-methodology-tradeoff-prompt.md`
    Recommended Fable5 prompt for methodology and tradeoff review without model-extraction framing.

16. `fable5-methodology-audit/`
    Fable5's second-stage methodology review outputs, plus local quality assessment.

Core principle:

> Do not ask for hidden thoughts. Ask for auditable public procedure: criteria used, alternatives rejected, decision triggers, falsifiers, and evidence that would change the verdict.

Anti-loop principle:

> Stop adding workflow when the next document adds no new kill condition, output schema, or decision boundary.
