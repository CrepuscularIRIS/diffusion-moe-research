# Fable5 Methodology Review — 08. Execution Boundaries

Question: which parts of this methodology can be executed mechanically, and which
require higher-level judgment?

Reading rule for this file: "mechanical" means an executor can perform it from the
schema with no taste, given the inputs; "judgment-heavy" means outcomes depend on a
call the schema cannot force. Every operator below contains both — the design question
is whether the judgment-heavy core is isolated and routed, or smeared across the whole
operator so nothing can be delegated.

---

```text
Operator: Epistemic calibration
Mechanical part: Claim-type classification from the fixed list; checking whether a
  search/experiment exists for the claim; applying the grade-gated promotion table
  (C → HOLD, D → cannot promote); applying the chain rule (min of link grades).
Judgment-heavy part: The A/B boundary ("strong secondary evidence" vs "plausible
  inference"); judging independence of evidence lines; recognizing that a claim was
  worded to dodge its true type (a novelty claim dressed as a value judgment).
Required inputs: One-sentence claim; evidence list with sources; claim's downstream use.
Output schema: The document's own schema — adequate.
Safe automatic decisions: HOLD on unsearched novelty; refuse-to-promote on D; grade A
  for verified local facts; demand for a missing falsifier.
Unsafe automatic decisions: Automatic B grades (inflation risk is one-directional —
  everything argues for its own upgrade); automatic E→escalate on every hard question
  (escalation flooding).
Escalation trigger: Grade disputes at the A/B and C/D boundaries; any E.
Failure modes: Grade inflation through repetition (a C claim graded five times drifts
  up); treating the grade as the verdict; wording games that reclassify claims.
Calibration tests: Seeded claim sets with known grades; check boundary agreement, not
  just class agreement; adversarial rewordings of the same claim must get the same
  grade.
```

```text
Operator: Context compression state
Mechanical part: Extracting explicit decisions, kills, and pending falsifiers that are
  literally marked in the record; schema completeness checking; carrying forward the
  do-not-repeat list verbatim.
Judgment-heavy part: Distinguishing a decision from a strongly-worded opinion in the
  record; deciding what is load-bearing enough to keep; naming the next IRREVERSIBLE
  decision (not the next task) — the single hardest field in the schema.
Required inputs: The full record; the previous state object (for diffing).
Output schema: The document's schema — adequate; add: provenance line (who compressed,
  from what range, when).
Safe automatic decisions: Flagging schema fields left empty; refusing to drop any
  previously-listed dead region without an explicit revival note.
Unsafe automatic decisions: Silently promoting open assumptions to resolved decisions
  (the document's own named failure); merging two conflicting state objects.
Escalation trigger: Contradiction between the new state and the previous one; two
  agents' compressions disagree on what was decided.
Failure modes: Beautiful-summary drift; loss of killed regions (zombie revival);
  authority laundering — the state object citing itself as the source of a decision.
Calibration tests: Compress the same record twice with different agents; diff the
  state objects; any divergence on resolved-decisions or dead-regions is a defect.
```

```text
Operator: Agent governance
Mechanical part: Role-conflict table lookup (generator ≠ final auditor; executor ≠
  claim owner); the cold-start/live-search/human triggers as written rules; packet
  contamination checklist (does the packet contain conclusions?).
Judgment-heavy part: Judging whether framing is "persuasive enough" to force
  cold-start; sizing the governance response to the stakes (the materiality threshold
  the corpus lacks); detecting agreement illusion in practice.
Required inputs: The decision, its promotion/irreversibility status, available agents,
  who produced what under which context.
Output schema: The document's schema — adequate.
Safe automatic decisions: BLOCK self-review at promotion gates (categorical); require
  live search on novelty (categorical); flag missing packet elements.
Unsafe automatic decisions: Auto-assigning human escalation for anything "important"
  (floods the scarcest resource); auto-approving governance because roles are
  nominally separate (names ≠ contexts).
Escalation trigger: Role conflicts with no clean assignment; repeated dead-gate
  findings (a gate that never fires).
Failure modes: Governance theater (titles separated, context shared); over-escalation;
  treating more agents as more governance.
Calibration tests: Inject a self-review case and a shared-context "agreement" case
  into routine flow; the operator must catch both without being told to look.
```

```text
Operator: Artifact acceptance review
Mechanical part: Type identification; schema completeness (trigger? inputs? outputs?
  limitations?); executing defined acceptance tests (fresh-environment run, copyable
  commands); verdict table application once test results exist.
Judgment-heavy part: The hostile-reader simulation — predicting the strongest wrong
  claim a motivated reader extracts; deciding what must be CUT (cutting is a taste
  act); blast-radius estimation.
Required inputs: The artifact; its named target user; its claim; executed test results.
Output schema: The document's schema — adequate with the blast-radius line added.
Safe automatic decisions: REVISE on any missing schema element; HOLD on missing
  evidence for decision-guiding artifacts; KILL on redundancy with an existing
  artifact it contradicts.
Unsafe automatic decisions: SHIP on polish signals (the exact failure the gate
  exists to catch — an automated SHIP is polish-as-readiness with extra steps);
  KILL on style grounds.
Escalation trigger: SHIP verdicts for public/reputation-bearing artifacts → human;
  disagreement between acceptance verdict and the claim's epistemic verdict.
Failure modes: Gate that always REVISEs (trains route-around); checklist pass
  mistaken for hostile-reader pass.
Calibration tests: Feed it a polished-but-never-run README (must not SHIP) and a
  modest-but-complete log (must SHIP) — both directions matter.
```

```text
Operator: Cross-domain operator transfer
Mechanical part: The four-part acceptance test as a checklist (decision named? evidence
  type named? attack run? kill condition added?); deletion test on the transferred
  language.
Judgment-heavy part: Judging whether the target domain's pressure point is genuinely
  analogous; pricing where the transfer breaks; distinguishing convergence (they
  already do this) from transfer.
Required inputs: Source operator + its decision function; target domain; a REAL pending
  decision in the target domain (no live decision → do not run).
Output schema: The document's schema — adequate.
Safe automatic decisions: KILL transfers that name no changeable decision; KILL
  transfers whose "evidence" is still research vocabulary.
Unsafe automatic decisions: ACCEPT on checklist completion alone — a fake transfer can
  fill every field plausibly; acceptance needs the target-domain stakeholder attack
  answered, which is judgment.
Escalation trigger: Transfers that would install standing process in an organization
  (the blast radius of a bad one is organizational, not personal).
Failure modes: Vocabulary transfer; rebranding the domain's existing practice;
  transfer into domains without decision pressure.
Calibration tests: Case 17-style inputs (renamed A/B test) must come back REVISE/KILL;
  a genuine spike-before-rewrite case must come back ACCEPT.
```

```text
Operator: Irreversible decision audit
Mechanical part: Lock-type classification from the seven-type table; checking for a
  named reversible substitute; checking the minimum-evidence gate against the claim's
  grade; verdict table application.
Judgment-heavy part: Pricing the delay cost honestly (the audit's systematically
  underweighted side); estimating full unwind cost including trust and identity;
  judging when commitment itself creates value.
Required inputs: The pending decision; its evidence packet; deadline/priority context.
Output schema: The document's schema PLUS a mandatory delay-cost line (file 04
  amendment).
Safe automatic decisions: BLOCK large compute before a cheap falsifier exists
  (categorical); BLOCK self-review acceptance (categorical); DELAY public claims
  lacking validation.
Unsafe automatic decisions: Automatic BLOCK on anything classified irreversible —
  the operator's own first failure mode ("calling every decision irreversible")
  becomes policy if automated.
Escalation trigger: All verdicts on reputation-bearing decisions → human; BLOCK
  verdicts contested by a stated delay cost.
Failure modes: Universal brake; ignoring delay cost; treating internal drafts as
  reputation commitments.
Calibration tests: Include cases where the correct verdict is PROCEED (deadline-bound,
  evidence present) — an audit calibrated only on BLOCK cases becomes a veto engine.
```

```text
Operator: Enrich scan (stress-point scan)
Mechanical part: Collecting the input packet (goal, metrics, failures, substrate);
  running the four detectors as checklists (goal vs metric written side by side;
  patch inventory; paper-claim vs practitioner-complaint table; substrate deltas).
Judgment-heavy part: Deciding a stress point is CONCRETE rather than a rephrased
  topic trend (the named failure: "treating a popular topic as a stress point");
  choosing which of several stress points is load-bearing.
Required inputs: Domain description, metrics, failure reports, substrate constraints —
  and honesty about which of these came from live sources vs memory.
Output schema: The protocol's schema — adequate.
Safe automatic decisions: Refusing to emit ideas before a stress point exists (the
  protocol's own gate — mechanically enforceable and valuable).
Unsafe automatic decisions: Auto-ranking stress points; auto-accepting memory-derived
  "practitioner complaints" as evidence (they need sources).
Escalation trigger: Conflicting stress signals; a domain where object invention seems
  required.
Failure modes: Popularity-as-pressure; stress points crafted to justify a
  pre-existing idea (reverse-engineered scan).
Calibration tests: Give the scanner a hot-but-healthy field; it must return "no
  concrete stress point" rather than manufacture one.
```

```text
Operator: Object audit (modeling-object extraction)
Mechanical part: Schema completion (old object stated? task-need stated? failures
  listed?); checking that a forbidden observation is present in the output; routing
  to deletion test next.
Judgment-heavy part: The core act — naming what current methods ACTUALLY model and
  what the task actually needs — is the single most judgment-dense step in the entire
  methodology; the schema can verify an answer exists, not that it is right.
Required inputs: The idea, the method family, documented failures.
Output schema: Operator 6's schema — adequate.
Safe automatic decisions: KILL when no forbidden observation can be stated (the
  operator's own kill condition — mechanically checkable: is the field empty?).
Unsafe automatic decisions: Accepting the old-object statement as correct because it
  is grammatical — a wrong old-object diagnosis silently invalidates everything
  downstream, and no checklist detects it.
Escalation trigger: Conceptually new or contested objects (the operator's own rule);
  disagreement between two independent object audits of the same idea.
Failure modes: Renamed tricks passing as objects; wrong diagnosis of the old object;
  object language accepted for its beauty.
Calibration tests: Run two independent audits on the same idea; divergent old-object
  statements = the case is judgment-heavy, route up. Seed known-laundering cases.
```

```text
Operator: Deletion test
Mechanical part: Producing the plain rewrite; diffing the two versions; checking
  whether any prediction/constraint/diagnostic appears ONLY in the original; the
  verdict table on the diff result.
Judgment-heavy part: Writing a FAIR plain rewrite — a strawman rewrite (too crude)
  fakes a surviving difference; an overly generous rewrite (imports the object's
  content into "plain" language) fakes laundering. The rewrite's fairness is the test.
Required inputs: Candidate description, core terms, implementation sketch, claimed
  predictions.
Output schema: Operator 7's schema — adequate.
Safe automatic decisions: KILL when the candidate is verbatim-unchanged after
  deletion; RESCOPE routing when a diagnostic survives.
Unsafe automatic decisions: KILL on early-stage language after zero
  operationalization attempts (the operator's own noted harshness failure — file 03's
  one-attempt rule applies).
Escalation trigger: The one-attempt case: language dies but the auditor suspects a
  real object underneath.
Failure modes: Strawman rewrites; generosity laundering; deletion-test theater where
  the rewrite is never actually attempted, just asserted.
Calibration tests: Seed pairs where ground truth is known (a real shift and a renamed
  trick with similar surface language); both directions must be caught.
```

```text
Operator: Occupancy hypothesis
Mechanical part: Query generation from templates (older names, adjacent literatures,
  cross-vocabulary synonyms); listing literatures that must-have-touched the object;
  the HOLD-before-search rule (categorical).
Judgment-heavy part: Adjudicating returned hits — "is this paper the same object or a
  vocabulary collision?" is exactly the deletion test applied to someone else's paper,
  and it is judgment; predicting where differently-named prior art hides.
Required inputs: The object, domain, keywords; then live-search results (the operator
  is TWO stages: hypothesis [pre-search, mechanical-ish] and adjudication
  [post-search, judgment]).
Output schema: Operator 8's schema — adequate; add: search-sufficiency statement
  (queries run / coverage claimed / date).
Safe automatic decisions: HOLD any novelty claim pre-search; KILL when search shows
  object AND falsifier owned (with adjudication confirmed).
Unsafe automatic decisions: Novelty confirmation from clean search results alone —
  clean results also mean bad queries; sufficiency must be judged.
Escalation trigger: Close-but-ambiguous hits (operator's own rule); method occupied /
  measurement unclear.
Failure modes: Vocabulary-blind search (missing prior art under other names);
  search-to-miss (queries inherited from a motivated generator); infinite search.
Calibration tests: Seed objects with KNOWN prior art under different vocabulary; the
  operator must find it or its sufficiency statement must admit the gap.
```

```text
Operator: Minimum falsifier
Mechanical part: Budget-cap enforcement; schema completeness (kill result stated?
  survival result stated? baseline named?); the demonstration check ("can this test
  only show upside?" — detectable: if no outcome is labeled KILL, reject).
Judgment-heavy part: Choosing the cheapest setting where the effect SHOULD appear
  (too easy = meaningless survival; too hard = meaningless death); choosing the
  strongest DUMB baseline (baseline choice is where falsifiers are quietly rigged).
Required inputs: Core claim, predicted effect, substrate limits, candidate testbeds.
Output schema: Operator 9's schema — adequate.
Safe automatic decisions: Rejecting falsifiers with no pre-committed kill result;
  HOLD when the cheapest test exceeds substrate; rejecting post-hoc metric changes.
Unsafe automatic decisions: Approving the testbed/baseline choice automatically —
  this is the rigging surface.
Escalation trigger: The falsifier itself looks like a publishable instrument
  (operator's own rule); testbed choice contested.
Failure modes: Demonstration-in-disguise; strawman baselines; falsifiers whose
  negative outcome is unattributable (confounded design — either result explains
  nothing).
Calibration tests: Review seeded falsifier designs where one is secretly a demo;
  the operator must reject it. Check: for approved falsifiers, was the kill result
  honored when it fired? (Post-hoc audit of decision-rule compliance.)
```

```text
Operator: Rescope or kill
Mechanical part: Schema completion; the independent-falsifier check (does the survivor
  have one? — presence is checkable); the softer-claim test as a wording diff
  (is the survivor the dead claim with hedges added?).
Judgment-heavy part: The independent value judgment — "would we fund the survivor
  fresh?" requires taste about what the field/domain values; distinguishing a genuine
  measurement survivor from an ablation table with ambitions.
Required inputs: What died and why; surviving observation; occupancy map; contribution-
  type list.
Output schema: Operator 11's schema — adequate.
Safe automatic decisions: KILL when the survivor has no independent falsifier
  (categorical); RESCOPE routing when method-dies/measurement-survives pattern is
  explicit.
Unsafe automatic decisions: RESCOPE as default kindness — automation will drift
  toward RESCOPE because it closes tickets without conflict; the fund-it-fresh
  question resists automation precisely because it is the honest one.
Escalation trigger: Contested measurement-vs-method boundary (operator's own rule).
Failure modes: Zombie scoping; polite kills; killing measurements with their methods.
Calibration tests: The suite's case 3 (both directions: Opus killing survivable
  measurement AND Opus rescoping an empty survivor).
```

```text
Operator: Failure conversion
Mechanical part: Schema completion (dead claim / reason / constraint / exclusion
  rule); checking the constraint is stated as a binding rule, not a lesson narrative;
  ledger insertion with scope and review date.
Judgment-heavy part: Judging whether the failure GENERALIZES (the operator's own kill
  condition: it may not); writing the constraint at the right scope — too narrow
  binds nothing, too broad becomes superstition.
Required inputs: Verified failure reason (bug/data/config excluded FIRST — a
  conversion from an unverified failure converts noise into policy).
Output schema: Operator 12's schema — adequate; add: scope + review date.
Safe automatic decisions: Refusing to close a KILL/RESCOPE without a conversion
  artifact (the discipline is mechanically enforceable); flagging narrative-only
  postmortems.
Unsafe automatic decisions: Auto-inserting constraints into the binding ledger —
  a wrong constraint silently blocks good future candidates; ledger insertion needs
  review.
Escalation trigger: The failure suggests a new object or program (operator's own
  rule); a proposed constraint would block an active candidate.
Failure modes: Profundity inflation ("every failure is a deep lesson"); constraint
  scar tissue; converting unverified failures.
Calibration tests: Seed a bug-caused failure dressed as a research negative; the
  operator must route it to triage, not conversion.
```

```text
Operator: Domain transfer enrich (cross-domain enrich pipeline)
Mechanical part: Running the pipeline stages in order with their gates (the stage
  sequence is itself mechanical: scan → objects → failures → candidates → deletion →
  occupancy → falsifier → attack → verdict → conversion); the ≤3-candidates cap;
  stage-skipping detection.
Judgment-heavy part: Every stage's core (as decomposed above) — the pipeline
  mechanizes the ORDER and the GATES, not the calls; plus the domain-translation
  judgment (does this domain's evidence standard differ?).
Required inputs: The protocol's input packet, honestly sourced.
Output schema: The protocol's final report template — adequate.
Safe automatic decisions: Refusing verdicts when stages were skipped; enforcing the
  candidate cap; enforcing conversion on every death.
Unsafe automatic decisions: End-to-end automated verdicts on anything promotion-bound —
  the pipeline run by an executor produces a well-FORMATTED verdict; whether it is
  well-FOUNDED depends on the judgment cores, which must be routed per the table
  below.
Escalation trigger: Any stage's own escalation fires; verdicts of DO (promotion-bound
  by definition).
Failure modes: Template-driven pre-judgment (the domain templates anchor "likely
  rescopes" before evidence — reading-map finding); pipeline theater (all stages
  formally present, none load-bearing).
Calibration tests: The full suite (cases 1–12), scored on boundary agreement and
  falsifier quality, not just verdict class.
```

---

## Closing artifacts

```text
What can be automated (mechanical, executor-safe):
- Gate enforcement: no-DO-without-occupancy, no-promotion-with-unrun-affordable-
  falsifier, no-close-without-conversion, budget caps, candidate caps, stage order.
- Schema completeness checks across all operators.
- Categorical blocks: self-review at promotion gates; large compute before cheap
  falsifier; novelty claims pre-search.
- Grade-table application once grades are assigned; chain-rule (min) computation.
- Verdict-table lookups once test results exist.
- Ledger operations: do-not-repeat carryforward, dead-region preservation, expiry
  flagging.

What should be assisted (agent drafts, judgment reviews):
- Plain rewrites for deletion tests (agent drafts; fairness reviewed).
- Query-set generation for occupancy (agent generates; sufficiency judged).
- Falsifier design (agent proposes testbed/baseline; rigging surface reviewed).
- Hostile-reader simulation; stakeholder attacks (agent simulates; blind spots
  reviewed).
- State-object compression (agent compresses; decision/opinion boundary spot-checked).

What should remain human:
- Promotion across reputation, direction, and program gates; program-level kills.
- The fund-it-fresh judgment on rescopes that will consume real budget.
- Delay-cost vs commitment-risk pricing on deadline-bound irreversible decisions.
- Overrides of any categorical block (recorded, always).
- Setting the thresholds themselves: escalation budget, calibration pass bar,
  materiality lines — meta-parameters are human property.

What should require search:
- Every novelty claim; every current-state claim (models, benchmarks, market, law);
  occupancy adjudication inputs; public claims embedding either.

What should require experiment:
- Every causal/mechanism claim before promotion; capability claims; benchmark
  validity under pressure; any claim with an affordable unrun falsifier — the
  affordable-falsifier rule is the sharpest boundary in the system: below it, the
  system may reason; at it, the system must measure.
```

Tradeoff summary: mechanization buys consistency and audit-trail at the price of
judgment displacement — every automated gate invites optimizing the gate instead of the
quality it proxies (the system's own anti-Goodhart lesson applied to itself). The
protection is the placement rule used throughout this file: automate the GATES and the
BOOKKEEPING, route the CORES (object naming, rewrite fairness, hit adjudication,
baseline choice, fund-it-fresh) to judgment explicitly. A system that automates its
cores will pass its own checklists while its verdicts quietly detach from reality.
