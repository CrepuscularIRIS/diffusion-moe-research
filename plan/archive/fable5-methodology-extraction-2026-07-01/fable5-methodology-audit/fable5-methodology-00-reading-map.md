# Fable5 Methodology Review — 00. Reading Map

Scope note: this file audits the corpus as a *methodology*, not as prose. Judgments below
are about decision boundaries, redundancy, and gaps. Per the corpus's own anti-loop rule,
this review adds no new workflow step; it consolidates and criticizes.

---

## Document-by-document map

```text
Document: agent-governance.md
Role in the methodology: Assigns judgment roles (generator / executor / auditor / searcher / falsifier / promoter) and forbids role collisions.
Decision boundary it adds: Generation and audit must be separated at promotion gates; cold-start packets, live search, and human judgment each get explicit triggers.
Tradeoff it introduces: Judgment hygiene vs throughput — every separation adds latency, cost, and a hand-off where context is lost.
Failure mode it prevents: Self-review, context contamination, agreement illusion, novelty-by-memory, false promotion.
Where it may be too broad: "Require human judgment when the decision changes project direction" — almost every research decision changes direction at some scale; a materiality threshold is missing.
How it should be used: As a pre-flight check at every promotion gate and before any adversarial review is trusted.
How it should not be used: As a task scheduler, or on small local edits (its own exclusion); not as proof of quality — separated roles can still all be wrong.
```

```text
Document: artifact-acceptance-review.md
Role in the methodology: SHIP / REVISE / HOLD / KILL gate for artifacts crossing a person or agent boundary.
Decision boundary it adds: "Usable by another person without hidden context" plus a hostile-reader misunderstanding check.
Tradeoff it introduces: Speed vs rigor at the shipping boundary; every acceptance pass delays reuse.
Failure mode it prevents: Polish-as-readiness; shipping without a target user; hidden limitations.
Where it may be too broad: Ten artifact types share one procedure but only five have type-specific checks; evidence thresholds are not scaled to blast radius (an internal log and a public benchmark get the same gate).
How it should be used: Whenever an artifact will influence decisions or be reused by someone who did not produce it.
How it should not be used: On throwaway notes; as a substitute for claim validation — an artifact can be SHIP-ready while the claim inside it is still HOLD.
```

```text
Document: context-compression-state.md
Role in the methodology: Converts long context into a resumable decision state (thesis, dead regions, active candidates, pending falsifiers, next irreversible decision).
Decision boundary it adds: Dead regions may not be re-opened without new evidence; the next decision (not the next task) must be named.
Tradeoff it introduces: Compression loses nuance vs full context loses tractability; once written, the state object becomes authoritative and its errors propagate to every downstream agent.
Failure mode it prevents: Summary drift, lost commitments, re-litigating killed ideas, workflow re-opening.
Where it may be too broad: No versioning or merge rule when two compressions of the same context disagree; no record of who compressed and under what stance.
How it should be used: At compaction boundaries, agent hand-offs, and immediately before promotion decisions.
How it should not be used: As ordinary summarization; as a replacement for underlying evidence — the state object should cite artifacts, not absorb them.
```

```text
Document: cross-domain-operator-transfer.md
Role in the methodology: Ports decision functions (not vocabulary) from research into product, engineering, design, education, business, organization.
Decision boundary it adds: A transfer is valid only if an observable decision changes; the transfer itself must pass a deletion test.
Tradeoff it introduces: Reach vs dilution — every transfer risks flattening a sharp research gate into management jargon.
Failure mode it prevents: Vocabulary transfer; renamed common sense.
Where it may be too broad: Domain examples are single-shot illustrations; there is no acceptance metric for a transferred operator in sustained use (did it actually kill anything in the target domain within N uses?).
How it should be used: When a non-research decision has real promotion pressure and a definable minimum decision test.
How it should not be used: When the target domain has no decision pressure (its own exclusion); as a branding exercise for ordinary practices.
```

```text
Document: epistemic-calibration.md
Role in the methodology: Evidence grading (A–E) and routing of claims to search, experiment, mechanical decision, or escalation.
Decision boundary it adds: Grade-gated promotion — DO requires A/B; C defaults to HOLD; D-after-clarification defaults to KILL; E escalates.
Tradeoff it introduces: Calibration cost vs decision speed; grade inflation vs analysis paralysis.
Failure mode it prevents: Novelty-by-memory, confident speculation, elegance-as-evidence.
Where it may be too broad: Single-claim scope only — no composition rule for claim chains (a conclusion resting on B×C×D links has no defined grade); "strong secondary evidence" for grade B is itself a judgment call with no examples at the A/B boundary.
How it should be used: At every promotion gate and before any factual assertion enters an artifact.
How it should not be used: On local reversible edits (its own exclusion); as a way to avoid deciding — grading is an input to a verdict, not a verdict.
```

```text
Document: executable-enrich-protocol.md
Role in the methodology: The canonical Layer-1 pipeline: stress scan → object inventory → failure inventory → candidate object → occupancy → deletion test → minimum falsifier → reviewer attack → verdict → conversion law.
Decision boundary it adds: No idea before a concrete stress point; ≤3 candidate objects before method design; no DO without an occupancy hypothesis; every death converts to a constraint.
Tradeoff it introduces: Pipeline discipline vs serendipity — strictly staged flow suppresses ideas that arrive method-first and only later reveal their object.
Failure mode it prevents: Idea-first ideation, laundering, unfalsifiable elegance, wasted failures.
Where it may be too broad: The domain templates pre-assign "likely rescopes" (VLA → taxonomy, MLLM → conflict resolution, …) without evidence; this anchors verdicts before the pipeline runs — a verdict-anchoring risk inside an anti-anchoring protocol.
How it should be used: As the single canonical encoding of Layer 1; all other encodings should defer to it.
How it should not be used: Running all ten steps on trivially killable inputs — cheap kills (deletion test, one search query) should short-circuit the pipeline.
```

```text
Document: fable-opus-calibration-suite.md
Role in the methodology: Blind verdict comparison between the reference judge and the executor, with a mismatch taxonomy and a skill-patch delta log.
Decision boundary it adds: Skills are patched only from observed verdict mismatches, not from taste.
Tradeoff it introduces: Fidelity-to-Fable vs accuracy-to-world — the metric is agreement with Fable, but Fable is not ground truth; perfect calibration reproduces Fable's errors at scale.
Failure mode it prevents: Installing uncalibrated skills.
Where it may be too broad: No pass/fail threshold (how much agreement, over how many cases, licenses installation); expected verdicts were authored inside the same system that is being calibrated — label contamination, only partially acknowledged ("provisional").
How it should be used: As a regression suite before skill installation and after every skill patch; supplemented with outcome-grounded labels (later evidence, external review results) as they accumulate.
How it should not be used: As proof that the system reduces false promotion — that claim needs labels grounded outside the system.
```

```text
Document: fable-part-followup-prompts.md
Role in the methodology: Extraction scaffolding — one focused prompt per audit module to avoid polished-summary outputs.
Decision boundary it adds: One module per pass; required per-signal deliverables (definitions, symptoms, false positives, checklists).
Tradeoff it introduces: Depth per module vs total extraction cost (many sessions).
Failure mode it prevents: Shallow single-pass extraction that yields style instead of operators.
Where it may be too broad: Prompts demand fixed counts ("3 symptoms, 2 false positives") — forced symmetry invites fabricated items to fill quotas.
How it should be used: During the extraction phase only.
How it should not be used: After extraction completes — this is scaffolding and should be retired, not maintained.
```

```text
Document: fable-public-procedure-extraction.md
Role in the methodology: The extraction contract: public procedure, not chain-of-thought; a quality bar that rejects vague or taxonomy-only answers.
Decision boundary it adds: Answers without decision triggers, mind-changing evidence, or KILL/RESCOPE distinctions are rejected.
Tradeoff it introduces: A public reconstruction is auditable but is a rationalization of process, not a recording of it — it should be treated as a normative procedure to test, never as a faithful description of how judgments were actually produced.
Failure mode it prevents: Style imitation; beautiful taxonomies without kill conditions.
Where it may be too broad: "Alternatives considered and rejected" invites plausible confabulation; the quality bar should additionally require that stated alternatives be independently checkable.
How it should be used: Once per major audit, to seed the operator library.
How it should not be used: Repeatedly on the same artifact — returns diminish and confabulation risk grows.
```

```text
Document: fable-to-opus-operator-library.md
Role in the methodology: Twelve operators with triggers, inputs, procedures, schemas, kill conditions, and escalation rules — the most execution-ready encoding of Layer 1.
Decision boundary it adds: Every operator carries an automatic kill condition and a named escalation trigger.
Tradeoff it introduces: Mechanical executability vs judgment residue — each operator's central step (name the missing object, judge independent value, pick the strongest dumb baseline) is exactly the part the schema cannot mechanize.
Failure mode it prevents: Imitating taste as style; operators without exit conditions.
Where it may be too broad: Overlaps opus-skill-drafts.md nearly one-to-one; two independently patched encodings of the same operators will drift.
How it should be used: As the canonical operator reference for execution agents.
How it should not be used: Patched in parallel with the skill drafts — designate one source of truth and generate the other from it.
```

```text
Document: irreversible-decision-audit.md
Role in the methodology: PROCEED / DELAY / RESCOPE / BLOCK gate over lock-in decisions; seven irreversibility types (narrative, benchmark, method, evidence, compute, reputation, product).
Decision boundary it adds: Every irreversible decision needs a minimum-evidence bar and a reversible substitute before it may proceed.
Tradeoff it introduces: Commitment risk vs delay cost — named explicitly, but no pricing rule is given for delay cost, so the tradeoff is asserted rather than computable.
Failure mode it prevents: Narrative lock, compute lock, reputation lock, evidence contamination, sunk-cost momentum.
Where it may be too broad: Trigger "an experiment will be expensive" has no threshold; without one, the audit can be invoked on everything and becomes a veto on execution.
How it should be used: Before benchmark selection, paper framing, large runs, public claims, skill installation, and shipping.
How it should not be used: On small reversible edits (its own exclusion); as a standing reason to never announce or never commit.
```

```text
Document: meta-skill-expansion-guide.md
Role in the methodology: Integration map wrapping Layer 2 (belief, memory, governance, acceptance, transfer, irreversibility) around Layer 1; carries the anti-loop rule.
Decision boundary it adds: A new workflow step is admissible only if it adds a kill condition, an output schema, or a decision boundary.
Tradeoff it introduces: Wrapper completeness vs process weight — acknowledged by its own anti-loop rule.
Failure mode it prevents: Infinite workflow expansion; process that feels safer without reducing false promotion.
Where it may be too broad: It introduces a fourth verdict vocabulary (ACCEPT/REVISE/HOLD/RESCOPE/KILL) alongside DO/RESCOPE/HOLD/KILL, SHIP/REVISE/HOLD/KILL, and PROCEED/DELAY/RESCOPE/BLOCK — with no mapping table between them.
How it should be used: As the map for when Layer 2 must wrap Layer 1.
How it should not be used: As precedent for adding a third layer — by its own rule, the next meta-layer must add a kill condition no existing document has.
```

```text
Document: opus-skill-drafts.md
Role in the methodology: Skill-formatted packaging of the Layer-1 operators, with automatic KILL/RESCOPE/escalate conditions per skill.
Decision boundary it adds: Skills carry automatic verdict conditions, not just procedures.
Tradeoff it introduces: Installation readiness vs duplication — it is a near-copy of the operator library in different packaging.
Failure mode it prevents: Installing skills without triggers, schemas, or failure modes.
Where it may be too broad: Same drift risk as the operator library; also, drafts are explicitly pre-calibration, yet nothing in the file itself marks them un-installable — the guard lives in a different document.
How it should be used: As the packaging step, generated from the operator library, after calibration passes.
How it should not be used: Installed before the pending falsifier (blind calibration) has been run — the corpus's own state object lists this as the next irreversible decision.
```

```text
Document: research-os-doc-index.md
Role in the methodology: Entry point; usage order; two governing principles (public procedure only; anti-loop).
Decision boundary it adds: Document ordering; the anti-loop principle as a corpus-level gate.
Tradeoff it introduces: Fixed reading order vs actual dependency structure (calibration is listed after protocol use; in practice calibration must gate installation, not follow it).
Failure mode it prevents: Using extraction documents out of order; extraction drift.
Where it may be too broad: It references `opus-distillation-prompt.md` and `fable5-research-methodology-tradeoff-prompt.md`, which are not present in the provided set — the index is out of sync with the corpus it indexes. An index that cannot be trusted about file existence undermines its role as the entry point.
How it should be used: As the entry point, after reconciling it with the actual file set.
How it should not be used: As evidence of corpus completeness.
```

---

## Classification

```text
Core documents:
- executable-enrich-protocol.md        (canonical Layer-1 pipeline)
- epistemic-calibration.md             (belief gate)
- agent-governance.md                  (judgment-role gate)
- irreversible-decision-audit.md       (commitment gate)
- artifact-acceptance-review.md        (shipping gate)

Support documents:
- context-compression-state.md         (state persistence across compaction/hand-off)
- fable-opus-calibration-suite.md      (validation harness — support until it gains a pass/fail standard)
- cross-domain-operator-transfer.md    (optional extension; only when a target-domain decision exists)
- meta-skill-expansion-guide.md        (integration map + anti-loop rule)
- research-os-doc-index.md             (entry point; currently stale)

Overlapping documents:
- fable-to-opus-operator-library.md ↔ opus-skill-drafts.md ↔ executable-enrich-protocol.md
  Three encodings of the same Layer-1 operators. Keep the protocol as canon, the library
  as the operator reference, and *generate* the skill drafts from the library. Do not
  patch all three independently.
- fable-public-procedure-extraction.md ↔ fable-part-followup-prompts.md
  Extraction scaffolding; both retire once extraction is complete.

Documents that should not be expanded further:
- Both extraction scaffolds (their job is done once the library exists).
- The three Layer-1 encodings (consolidate; expansion multiplies drift).
- meta-skill-expansion-guide.md (by its own anti-loop rule: a new meta-skill must add a
  kill condition, schema, or boundary that none of the six existing ones has — none of
  the obvious candidates does).

Missing document types:
1. Live-search execution protocol — every document says "require live search"; none
   defines what a sufficient search is: query count, venue coverage, older-name
   expansion, and the negative-result standard ("not found under queries Q1..Qn as of
   date D"). Without this, "live search required" degrades into one lazy query.
2. Verdict ledger with expiry — HOLD and un-run DO verdicts have no persistence rules;
   context-compression-state gestures at it, but there is no durable registry with
   expiry dates, re-entry conditions, and do-not-repeat enforcement across sessions.
3. Calibration pass/fail standard — agreement thresholds, minimum case counts, and
   (critically) a second label source grounded in outcomes rather than in Fable.
4. Experiment-integrity verification — nothing in this corpus checks that a falsifier
   actually ran, fired its intervention, and consumed its intended data; a passing
   number from a broken run defeats every gate upstream of it.
5. Disagreement-resolution protocol — "escalate" is named everywhere, but there is no
   procedure for what the escalation target does with a Fable/Opus split verdict.
6. Unified verdict vocabulary — one mapping table across the four verdict sets.
7. Governance budget — a cap on escalation rate and process overhead, so the anti-loop
   rule becomes measurable instead of aspirational.
```
