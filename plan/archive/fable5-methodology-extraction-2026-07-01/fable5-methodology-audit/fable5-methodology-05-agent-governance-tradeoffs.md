# Fable5 Methodology Review — 05. Agent Governance Tradeoffs

Question: what should each actor be allowed to decide, and what should be forbidden?

Structural principle carried through this file: **route by stance and by evidence
access, not by model identity.** A "different model" reviewing with the generator's
context is contaminated; the same model class reviewing from a cold packet with an
adversarial stance is not. The corpus's role table is right; its enforcement point is
context and stance separation, not model diversity per se.

---

## Role governance

```text
Role: Methodology critic (audits the process, not individual claims)
Allowed decisions: Declare a gate skipped; declare a verdict procedurally invalid
  (e.g., DO without occupancy search); demand a missing artifact (search log, delta
  list); flag vocabulary drift across the verdict systems.
Forbidden decisions: Overturning a verdict on the merits (that is the adversarial
  reviewer's job); redesigning workflow mid-run (anti-loop rule); killing ideas.
Required inputs: The process record — verdict trail, evidence grades, search logs,
  packet provenance. Not the persuasive artifacts themselves.
Output schema: Gate audited / procedural finding / rule violated / required remedy /
  severity (advisory | blocking).
Escalation trigger: A procedural violation on a promotion-bound item → blocks the
  promotion until remedied.
Contamination risk: Low — but a critic who starts reading content instead of process
  drifts into being a second adversarial reviewer with worse separation.
Review requirement: Spot-audited by human occasionally; the critic's findings are
  themselves checkable against the record.
Tradeoff: Process audit catches gate-skipping cheaply but catches zero content errors;
  over-investing here yields procedurally immaculate false claims.
```

```text
Role: Execution agent (runs experiments, organizes artifacts, tunes, maintains logs)
Allowed decisions: Mechanical verdicts on grade-A local facts; scheduling within an
  approved budget; formatting/organization choices; flagging anomalies.
Forbidden decisions: Claim promotion; novelty judgment; declaring a run "successful"
  in claim terms (it reports outcomes; the claim owner interprets); modifying the
  falsifier's decision rule mid-run.
Required inputs: Pre-registered run spec: budget cap, seeds, kill/survive criteria,
  expected artifacts.
Output schema: Run spec ID / what ran / exit status / artifacts produced / anomalies /
  deviations from spec (any deviation voids claim-bearing use until re-approved).
Escalation trigger: Any deviation from spec; any result that would trigger a verdict
  change; budget threshold crossings.
Contamination risk: Execution masquerade — passing tests presented as strategic
  validity (agent-governance.md's named risk); the executor's report drifting into
  interpretation.
Review requirement: Code agent verifies the intervention fired; claim owner interprets.
Tradeoff: Tight specs make execution auditable but brittle — every legitimate
  adaptation (a dataloader fix) needs a re-approval loop; too loose, and the run stops
  being the pre-registered test.
```

```text
Role: Code agent (diffs, implementation correctness, intervention-fired checks)
Allowed decisions: Correct/incorrect on implementation vs spec; merge-safety of diffs;
  "the intervention actually executed and changed state."
Forbidden decisions: Whether the experiment design answers the research question;
  whether the claim is true; scope changes disguised as fixes.
Required inputs: The spec, the diff, the run logs — not the paper narrative (a code
  agent that reads the intended story starts confirming it).
Output schema: Spec conformance / defects found / intervention-fired evidence /
  silent-failure checks (mocks, hardcoded results, unused inputs) / verdict:
  conforms | defect | cannot-determine.
Escalation trigger: cannot-determine on a claim-bearing run; evidence of a silent no-op.
Contamination risk: Low for correctness; nonzero if given narrative context.
Review requirement: None routine; sampled audits.
Tradeoff: The code agent is the cheapest guard against the corpus's biggest unpatched
  hole (no experiment-integrity document) — but correctness-vs-spec cannot catch a
  wrong spec; it verifies the test was run, never that the test was right.
```

```text
Role: Live-search agent (executes occupancy and current-state searches)
Allowed decisions: Query execution and expansion (older names, adjacent literatures);
  reporting hits with sources; declaring the negative-result log ("nothing found under
  Q1..Qn as of date D").
Forbidden decisions: Novelty adjudication — mapping hits to occupied/surviving
  territory is a judgment call made by a separate adjudicator; deciding a search is
  "enough" for a high-stakes claim (that is a standard, not a search result).
Required inputs: The query set designed upstream (occupancy hypothesis), plus license
  to expand queries; the search-sufficiency standard for this claim's stakes.
Output schema: Queries run / hits (with sources and dates) / expansions performed /
  not-found log / coverage limits stated.
Escalation trigger: Hits that are close but ambiguous (operator 8's escalation: strong
  adjacent work, unclear boundary).
Contamination risk: Query design inherited from the generator can aim the search away
  from the kill; the searcher should receive the object description, not the hoped-for
  conclusion.
Review requirement: Adjudication by a non-generator; sampled query-quality audits.
Tradeoff: Cheap searches terminate too early (false novelty); exhaustive searches never
  terminate (novelty paralysis). The missing search-sufficiency standard (reading map,
  gap #1) is exactly the document that would price this tradeoff.
```

```text
Role: Experiment runner (subset of execution focused on claim-bearing runs)
Allowed decisions: None on claims. Operational decisions inside the spec envelope.
Forbidden decisions: Re-running until the number looks right (seed shopping); dropping
  "failed" seeds; adjusting the metric post hoc; interpreting.
Required inputs: Pre-registered falsifier spec with decision rule; seed list fixed in
  advance.
Output schema: All seeds reported / metric per pre-registered definition / raw
  artifacts preserved / any rerun documented with reason.
Escalation trigger: The pre-registered decision rule fires (either direction) — the
  result routes to the claim owner and auditor simultaneously (not to the generator
  first, who would frame it).
Contamination risk: Selective reporting is the quiet killer; simultaneous routing of
  results is the control.
Review requirement: Integrity check on every claim-bearing run (the corpus's missing
  document; borrow the discipline: structural check, execution check, plausibility
  check).
Tradeoff: Pre-registration prevents result-shopping but also prevents legitimate
  adaptive experimentation; the honest compromise is labeling — exploratory runs are
  allowed and cheap, but nothing exploratory bears claims.
```

```text
Role: Adversarial reviewer (attacks specific claims and artifacts)
Allowed decisions: Verdict recommendations (KILL/RESCOPE/HOLD recommendations are
  self-administrable downward); declaring an attack unresolved; demanding a specific
  missing experiment or citation.
Forbidden decisions: Upward verdicts — "this claim stands" from a single reviewer is
  weak evidence (removing objections ≠ adding support); final promotion; rewriting the
  artifact it reviews (reviewer-as-editor contaminates the next review round).
Required inputs: Cold-start packet: evidence, claim, falsifier results — no generation
  context, no prior reviews (independent, not sequential, review).
Output schema: Attack / evidence for the attack / candidate response / unresolved
  risk / verdict impact (operator 10's schema — adequate as-is).
Escalation trigger: Attack strong but a reframing may survive (→ rescope adjudication);
  reviewer and generator deadlock.
Contamination risk: Packet contamination (conclusions smuggled in); rhetoric without
  evidence (named failure mode); repeated pairing with the same generator breeds
  accommodation.
Review requirement: The packet is audited for contamination before the review is
  trusted; rotate reviewer/generator pairings.
Tradeoff: The asymmetry (down-verdicts cheap, up-verdicts expensive) is correct but
  makes the reviewer a structural pessimist; without the anti-overkill calibration
  cases (file 09), the system optimizes for impressive kills.
```

```text
Role: Human promoter
Allowed decisions: Promotion across reputation/direction/program gates; program-level
  kills; venue and announcement decisions; overriding any agent verdict WITH a recorded
  reason (unrecorded overrides corrupt the calibration record).
Forbidden decisions: None formally — but promotion without the completed packet should
  be procedurally flagged by the methodology critic, because a human deciding on a
  pitch instead of a packet is the governance system's single point of failure.
Required inputs: The completed promotion packet: claim + grade + search log + falsifier
  result + review verdicts + irreversibility audit + stated delay cost.
Output schema: Decision / packet completeness acknowledged / overrides + reasons /
  unwind condition.
Escalation trigger: None above (top of chain); laterally — a second human for
  conflicts of interest.
Contamination risk: Rubber-stamping agent consensus (agreement illusion at the top);
  fatigue from over-escalation degrading every decision's quality.
Review requirement: Post-hoc: promotion outcomes feed the calibration record — human
  verdicts are data too.
Tradeoff: Human judgment is the only place taste, venue strategy, and risk appetite
  legitimately live — and it is the scarcest, slowest, least reproducible component.
  Every unnecessary escalation spends it; every skipped escalation risks reputation.
```

---

## The seven questions

```text
1. When must generator and auditor be separate?
Whenever the output crosses a promotion gate or feeds an irreversible decision — no
exceptions, including "the generator wrote a very self-critical review." Below
promotion gates, self-review is permitted as drafting, labeled as such. Separation
means context separation first, model separation second: a cold packet to the same
model class is more independent than a warm context handed to a different model.

2. When is cold-start review mandatory?
(a) The generator produced persuasive framing; (b) the claim affects promotion;
(c) the reviewer could inherit assumptions — in practice, all promotion-gate reviews.
Corollary the corpus implies but does not state: the cold packet itself must be
audited — a packet containing the generator's conclusions is a warm review with extra
steps.

3. When is live search mandatory?
Novelty claims (always); claims about current external state — literature, benchmarks,
model versions, market, policy, legal (always); before any public claim that embeds
either. Not mandatory: internal mechanism claims on local artifacts, hypothetical
framings labeled as such. The search must meet a sufficiency standard scaled to stakes;
one query is not a search.

4. When is experiment mandatory?
Causal/mechanism claims (no promotion without intervention evidence); capability
claims (protocol-specified eval); benchmark-validity claims (pressure test or external
ground truth); and — the sharpest rule available — whenever an affordable falsifier
exists: an unrun affordable falsifier is an automatic promotion blocker, because at
that point the system is choosing not to know.

5. When is human promotion mandatory?
Reputation-bearing acts (publication, announcement, shipping to external users);
direction and program decisions (adoption AND kills); irreversible spends above a set
threshold; ethics/legal exposure; any override of a blocking gate. Everything else
should NOT be escalated — preserving human bandwidth for these is itself a governance
requirement.

6. When should model agreement be ignored?
When contexts or prompt framings are shared (one line of evidence, not several); when
the agreeing models face a common blind spot (all lack live search → agreement on
novelty is worthless); when agreement is the *output being measured* (calibration
against Fable measures fidelity, not truth). Agreement counts as evidence only under
stance-separated, context-separated review — and even then it only removes objections;
it never substitutes for a falsifier.

7. When does governance overhead become harmful?
Measurable signs: (a) escalation rate makes the human the pipeline bottleneck;
(b) process latency exceeds falsifier latency — if reviewing a claim costs more than
testing it, run the test; (c) a governance step exists that has never changed a
verdict (dead gate — remove it); (d) velocity drops without any drop in false
promotion (the meta-guide's own criterion: process that feels safer without reducing
false promotion). The corpus names over-escalation as a failure mode but gives no
budget; set one and audit it like any other claim.
```

Tradeoff summary: every governance separation buys error-independence at the price of
context loss and latency. The corpus spends aggressively on separation and is right to
at promotion gates — but it lacks the counter-pressure instrument. The dead-gate test
(question 7c) is the cheapest such instrument: any gate that has not changed a verdict
in N cycles is either measuring nothing or the system stopped producing risky work;
both cases demand attention.
