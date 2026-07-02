# Fable5 Methodology Review — 07. Cross-Domain Transfer

Question: how can research methodology transfer into product, engineering, design,
education, business, and organization decisions without becoming generic?

Governing test (from `cross-domain-operator-transfer.md`, kept and sharpened): a
transfer is real only if (1) the *decision function* moves, not the vocabulary; (2) the
target domain supplies its own evidence type; (3) at least one named decision would
change; (4) the transfer adds a kill condition the target domain did not already have.
Condition (4) is the sharpest: most fake transfers fail it — the target domain already
practiced the substance under another name, and the transfer only rebrands it.

---

```text
Research function: Modeling-object shift — ask whether the field optimizes the wrong
  object before improving the optimization.
Target-domain translation: Problem-object shift — "are we improving the wrong thing?"
  Product: optimizing feature count when the object is time-to-first-value. Org:
  optimizing utilization when the object is cycle time.
Target-domain evidence: A metric-goal divergence demonstrated in the domain's own
  data: the optimized number improved while the outcome it proxies did not.
Minimum decision test: Name one KPI the team would STOP reporting if the object shift
  is right. No stoppable KPI → the shift is commentary, not a decision.
Stakeholder attack: "You are renaming our KPI debate as research methodology" — from
  the owner of the current metric, who has budget attached to it.
False transfer pattern: Declaring every disagreement about priorities an "object
  shift"; the term inflates until it means "I disagree."
Where transfer breaks: Domains where the object is externally fixed (regulatory
  metrics, contractual SLAs) — the object cannot shift regardless of its wrongness;
  the operator degrades into complaint.
Tradeoff: High leverage when it fires (redirects entire efforts) vs high social cost —
  object shifts attack the legitimacy of existing work; deploy with the evidence in
  hand, not as an opener.
Output schema: Current optimized object / evidence of divergence from real goal /
  proposed object / KPI to stop / decision that changes / owner of the change.
```

```text
Research function: Minimum falsifier — the cheapest experiment whose negative result
  forces abandonment.
Target-domain translation: Minimum decision test — the cheapest observation that would
  change the decision. Engineering: the spike that isolates the bottleneck before the
  rewrite. Product: 5 users attempting the core job unassisted.
Target-domain evidence: Behavioral/system observations, not opinions: load test
  results, task-completion rates, conversion deltas.
Minimum decision test: Before any commitment >X (budget/weeks), a written test with a
  pre-committed abandonment result. If no observation could change the decision, the
  decision is not being made on evidence — say so explicitly.
Stakeholder attack: "We already know the answer; the test is delay theater" — from
  whoever has already committed emotionally to the build.
False transfer pattern: Tests designed to pass (demos wearing test costumes) — the
  target-domain version of falsifier-as-demonstration; also: infinite pilots as
  procrastination.
Where transfer breaks: Decisions whose evidence only exists post-commitment (org
  redesigns, brand repositioning) — where staged reversibility, not falsification, is
  the honest instrument.
Tradeoff: Kill-tests save large commitments but tax small ones; a falsifier
  requirement on every decision is bureaucracy — scale the requirement to the
  commitment size.
Output schema: Decision at stake / test / cost / pre-committed kill result /
  pre-committed proceed result / expiry date.
```

```text
Research function: Reviewer attack — simulate the strongest objection before
  submission.
Target-domain translation: Stakeholder attack — simulate the strongest objection from
  each affected party BEFORE the decision meeting: novice user, power user, security,
  finance, the team whose roadmap this displaces.
Target-domain evidence: Attacks grounded in the stakeholder's actual incentives and
  past objections — not generic devil's advocacy.
Minimum decision test: At least one simulated attack must have changed the proposal
  before it is presented. Zero changes → the simulation was theater.
Stakeholder attack (on the operator itself): "You are pre-litigating instead of
  asking us" — real stakeholders resent being simulated when they were available;
  simulation complements consultation, never replaces available stakeholders.
False transfer pattern: Adversarial rhetoric without evidence (the operator's own
  named failure mode, imported intact); strawman attacks that flatter the proposal.
Where transfer breaks: Low-stakes reversible decisions — attack simulation on a
  two-day experiment costs more than the experiment.
Tradeoff: Cheap resilience-testing vs anchoring — a proposal hardened against
  simulated attacks can become over-fitted to them, brittle against the real objection
  nobody simulated.
Output schema: Stakeholder / their incentive / strongest attack / evidence /
  proposal change made or risk accepted / residual exposure.
```

```text
Research function: Deletion test — remove the object vocabulary; check whether
  anything observable is lost.
Target-domain translation: Value-proposition deletion test — remove the story,
  branding, and category language ("AI-powered", "platform", "intelligent"); check
  whether a concrete job is still done measurably better.
Target-domain evidence: The de-narrated description still names: user, job, delta,
  and how the delta is measured.
Minimum decision test: Give five target users the de-narrated version; do they still
  want it? (The transfer document's own test — correct as written.)
Stakeholder attack: "Positioning IS value in this market" — partially true: brand
  carries real information; the test scopes to whether ONLY the story remains.
False transfer pattern: Using the deletion test to kill all differentiation language —
  the goal is detecting empty language, not banning language.
Where transfer breaks: Markets where the narrative is the product (luxury, status
  goods, some developer-tool categories) — deletion removes the actual mechanism of
  value; the operator needs a scope statement there, not application.
Tradeoff: Prevents story-driven roadmaps vs risks under-valuing legitimate positioning
  work; the boundary requires domain judgment (which is why this operator does not
  fully mechanize — see file 08).
Output schema: Full pitch / de-narrated rewrite / what disappeared / job still done? /
  measurable delta remaining / verdict.
```

```text
Research function: Occupancy map — who already owns this object, in what form, with
  what results.
Target-domain translation: Competitor/precedent map — competitors, substitutes,
  internal prior attempts, and adjacent teams' roadmaps, mapped BEFORE claiming
  whitespace. Org version: has this reorg/process been tried here before, and what
  killed it?
Target-domain evidence: Named occupants with dates and outcomes; for business: what a
  buyer currently uses and pays for; for org: the memo from the last attempt.
Minimum decision test: Can a buyer name what they would stop using or stop paying for?
  (Transfer document's test — kept.) Org variant: can anyone name why the last attempt
  died, and what is different now?
Stakeholder attack: "The market is different now" / "that was before X" — sometimes
  true; the map must date its entries so this attack can be evaluated instead of
  merely asserted.
False transfer pattern: Feature-grid competitor analysis (vocabulary-level occupancy)
  instead of job-level occupancy — two products with different feature lists can
  occupy the same job.
Where transfer breaks: Genuinely new-category creation, where the absence of occupants
  is the thesis — there the map's role inverts: it must explain WHY the space is
  empty (usually: no demand, or a structural blocker the newcomer hasn't seen).
Tradeoff: Prevents re-entering graveyards vs breeds excessive deference to incumbents;
  an occupancy map is an input to differentiation, not a stop sign.
Output schema: Space claimed / occupants + dates + outcomes / what they own / what
  survives / why the surviving gap exists (demand absent? blocker? overlooked?).
```

```text
Research function: Metric contract — the success metric must be validated against the
  real goal and robust to being optimized.
Target-domain translation: Success contract — before launch, write what success
  measurably means, what would count as failure, and which gaming behaviors the metric
  must resist (support tickets closed fast vs problems actually solved).
Target-domain evidence: The metric's behavior under pressure in the domain's own
  history — every incentivized metric in the org that has already been gamed is
  evidence about the next one.
Minimum decision test: For each proposed metric: name one behavior that improves the
  metric while hurting the goal. If the team cannot name one, they have not thought
  about it; if they can, the contract must address it.
Stakeholder attack: "You are over-engineering; we just need a number to track" — from
  whoever wants the dashboard shipped; the answer is the org's own gamed-metric
  history.
False transfer pattern: Contract theater — writing the failure condition so vaguely
  ("if metrics degrade materially") that it can never fire.
Where transfer breaks: Exploratory phases where premature metric contracts freeze
  learning — a two-week-old product optimizing a contract is worse than one watching
  everything loosely.
Tradeoff: Anti-Goodhart robustness vs metric agility; contracts must have revision
  clauses or they become the new Goodhart target themselves.
Output schema: Goal / metric / validation link / named gaming behavior / counter /
  failure condition (specific) / revision trigger.
```

```text
Research function: Rescope — when the big claim dies, extract the smaller contribution
  with independent value.
Target-domain translation: Degrade gracefully — the failed product becomes a feature;
  the failed platform becomes a tool; the failed reorg becomes one team's improved
  process. Valid ONLY if the survivor passes an independent value test.
Target-domain evidence: The survivor has its own users/buyers/adopters who would want
  it never having heard of the original ambition.
Minimum decision test: Would we fund the small version if it had been proposed
  directly? If no — it is a face-saving remnant, not a rescope; kill it.
Stakeholder attack: "This is the same failed project with a smaller banner" — often
  correct; the independent-value test is the answer, and if it can't be answered,
  the attack wins.
False transfer pattern: Zombie scoping — serial rescopes that never die, each
  consuming a quarter (the "soft-narrowing" boundary mistake from file 03, imported).
Where transfer breaks: When the large version's fixed costs don't scale down
  (infrastructure, compliance) — the small version inherits big-version costs and
  drowns; some things only exist at scale.
Tradeoff: Salvages sunk investment vs prolongs dying efforts; the rescope's expiry
  date is mandatory equipment.
Output schema: What died / cause / survivor / independent value evidence / would-we-
  fund-it-fresh answer / expiry + success criterion.
```

```text
Research function: Failure conversion — every dead idea emits a constraint, exclusion
  rule, or new candidate.
Target-domain translation: Lesson-to-constraint conversion — postmortems that end in a
  RULE, not a narrative: "vendor integrations >X weeks require a kill checkpoint at
  week 2" rather than "we learned a lot about integration complexity."
Target-domain evidence: The converted constraint demonstrably blocks or reshapes at
  least one subsequent decision within N months — an unused constraint was a
  narrative wearing a rule costume.
Minimum decision test: Every postmortem's output section contains ≥1 of: a new
  gate, a new exclusion, a revived alternative with its trigger. None → the
  postmortem is incomplete, run it again.
Stakeholder attack: "Rules from one failure overfit to that failure" — legitimate;
  constraints need scope statements and their own expiry/review dates.
False transfer pattern: Blame laundering — converting a judgment failure into a
  process rule so nobody is accountable; also constraint inflation until the rulebook
  itself fails the deletion test.
Where transfer breaks: True one-off failures (a vendor's bankruptcy) — forcing a
  general rule from a non-generalizing event produces superstition, the operator's own
  "treating every failure as profound" mode.
Tradeoff: Compounding organizational memory vs accumulating scar tissue; the
  constraint ledger needs periodic pruning by the same dead-gate test as everything
  else.
Output schema: Failure / mechanism / converted rule + scope / first decision it must
  bind / review date.
```

```text
Research function: Agent governance — separate generator, auditor, searcher, executor,
  promoter; forbid self-review at promotion gates.
Target-domain translation: Decision governance — separate proposer, reviewer, and
  approver for decisions with financial/political/irreversibility risk; the reviewer
  must be able to reject without social penalty and without inheriting the proposer's
  framing (cold-start = reviewing the data before hearing the pitch).
Target-domain evidence: Rejection actually happens at a nonzero rate; reviews change
  outcomes; the org's history of self-approved failures.
Minimum decision test: Can the reviewer reject without penalty and without
  contamination? (Transfer document's test — kept.) Auditable version: when did this
  review function last reject anything?
Stakeholder attack: "This is bureaucracy; we're too small for role separation" —
  partially right: the governance budget question (file 05, Q7) transfers intact;
  separation belongs at irreversible/promotion decisions only.
False transfer pattern: Org-chart theater — separated titles, shared context: the
  approver sits in the pitch meeting, then "independently" approves.
Where transfer breaks: Crisis response — separation latency exceeds decision windows;
  crisis governance is pre-authorization + post-hoc audit, not inline review.
Tradeoff: Error-independence vs speed and trust-cost; over-separation in small teams
  destroys more value through latency than it saves through hygiene.
Output schema: Decision class / proposer / reviewer (context-cold?) / approver /
  rejection rate history / escalation path.
```

```text
Research function: Irreversibility audit — identify what must not be committed early;
  demand reversible substitutes and evidence gates.
Target-domain translation: One-way-door screening — classify pending decisions as
  reversible (decide fast, delegate) vs irreversible (gate: minimum evidence +
  reversible substitute + explicit sign-off). Hiring commitments, public pricing,
  platform choices, brand promises are the classic one-way doors.
Target-domain evidence: The actual unwind cost, estimated honestly — including the
  costs that don't appear on invoices (trust, morale, market signal).
Minimum decision test: For each pending commitment: what is the reversible substitute,
  and what evidence gate opens the one-way door? No substitute nameable and no gate
  defined → the decision is not ready to be made.
Stakeholder attack: "Everything is reversible if you're willing to pay" — technically
  true and practically evasive; the audit prices the unwind, it doesn't deny its
  possibility.
False transfer pattern: Calling every decision irreversible (the source document's own
  first failure mode) — used as a universal brake by whoever prefers the status quo.
Where transfer breaks: Domains where commitment itself creates the value
  (partnerships, credible market signals, morale-bearing announcements) — reversible
  substitutes can be worth strictly less than the commitment; the audit must weigh
  commitment value, not only commitment risk.
Tradeoff: Prevented lock-ins vs decision latency and signaling weakness; the delay-
  cost line (file 04's amendment) is mandatory here too.
Output schema: Decision / door type / unwind cost (full) / reversible substitute /
  evidence gate / delay cost / verdict PROCEED-DELAY-RESCOPE-BLOCK.
```

---

## Closing artifacts

```text
Bad transfer examples:
1. "Product falsifier" as a renamed A/B test the team already ran routinely — no new
   kill condition added; vocabulary transfer (calibration suite case 17's pattern).
2. "Our roadmap needs an occupancy map" delivered as a feature-comparison grid — the
   decision function (job-level occupancy, named stoppable spend) never moved.
3. A "metric contract" whose failure condition is "significant degradation" — contract
   theater; can never fire; adds no decision boundary.
4. Postmortems retitled "failure conversions" that still end in narrative lessons —
   the RULE output was never enforced.
5. "Agent governance for the design team" that assigns reviewer titles while everyone
   attends the same pitch — separation of names, not of context.

Good transfer examples:
1. Engineering: a 3-day spike with a pre-committed abandonment threshold before a
   6-month rewrite — minimum falsifier with real kill result, and the rewrite was in
   fact abandoned when the spike showed the bottleneck elsewhere.
2. Product: de-narrated value prop given to 5 users; 4 could not say what the product
   did → repositioning killed before launch spend (deletion test changing a decision).
3. Business: pre-entry precedent map found two dead attempts at the same wedge, both
   killed by the same procurement blocker; entry re-scoped to a segment without the
   blocker (occupancy map converting into a constraint).
4. Org: capex approvals restructured so the reviewer receives the data packet before
   the pitch meeting; rejection rate moved from 0% to a nonzero rate (cold-start
   governance measurably changing outcomes).
5. Support org: ticket-closure-speed metric replaced under a success contract naming
   the gaming behavior (premature closes) and its counter (reopen-rate pairing) —
   anti-Goodhart transfer with a named exploit and counter.

Transfer acceptance test (all four required):
1. Decision function moved — a named decision in the target domain now has a
   different gate, input, or kill condition than before.
2. Target-domain evidence defined — the operator consumes the domain's own evidence
   type, not research vocabulary.
3. A stakeholder attack was run against the transfer itself and answered.
4. New kill condition — the transfer lets the target domain kill something it
   previously could not kill cleanly. If the domain already did this under another
   name, log it as convergence, not transfer, and do not rebrand their practice.
```

Tradeoff summary: cross-domain transfer is where this methodology is most tempted to
become a brand. The four-part acceptance test is deliberately harsh because the failure
mode is asymmetric: a failed research transfer costs a workshop's attention; a
successful *fake* transfer installs research jargon as management process across an
organization, where the deletion test it teaches would kill it.
