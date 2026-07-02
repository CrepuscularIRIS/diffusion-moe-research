# Fable5 Methodology Review — 02. Research Action Selection

Question: how should the system decide what is worth doing next?

Governing principle: choose the action with the highest expected verdict-change per unit
cost, subject to ordering constraints (search before compute; audit before promotion;
compression before hand-off). An action that cannot change any verdict is not work; it
is motion.

---

## Candidate action analyses

```text
Current state: A candidate claim involves novelty, current literature, market, or
  model status; occupancy is a hypothesis, not a map.
Decision needed: Can this claim's occupancy be trusted enough to spend on it?
Candidate next action: LIVE SEARCH
Information gained: Occupancy facts; older names; adjacent-literature hits; a
  negative-result log that upgrades novelty wording from D to B.
Cost: Low (minutes–hours; no compute).
Reversibility: Fully reversible.
Risk: Poorly designed queries give false confidence in a clean map (the search "passes"
  because it was aimed to miss).
Delay cost: Near zero — search is almost never the wrong first move for novelty claims.
Who should execute: Live-search agent (web-connected).
Who should audit: A separate adjudicator maps hits to "occupied / surviving" territory;
  the claim's generator must not adjudicate its own search results.
When this action is wrong: The claim does not depend on external state (local artifact
  facts); or search is being used to procrastinate on an affordable falsifier that would
  settle more.
Verdict: DO — mandatory before any DO promotion of a novelty-bearing claim.
```

```text
Current state: A claim survived deletion test and occupancy hypothesis; it asserts a
  mechanism or an effect; a ≤48 GPU-hour test exists.
Decision needed: Is the object real or a story?
Candidate next action: MINIMUM FALSIFIER
Information gained: The highest-value bit in the system — kill or survive, with a
  pre-committed decision rule.
Cost: Bounded by the budget cap (protocol: prefer 48–100 GPU-hours).
Reversibility: Compute is spent but nothing is locked; results are information either way.
Risk: A falsifier that is secretly a demonstration (only shows upside — named failure
  mode in operator 9); a broken run producing a plausible number (no integrity check in
  this corpus).
Delay cost: High if delayed — every downstream artifact built before the falsifier is
  narrative risk.
Who should execute: Experiment runner (executor role).
Who should audit: Code agent verifies the intervention fired; falsifier designer
  verifies the decision rule was applied as pre-registered.
When this action is wrong: Occupancy not yet checked (may falsify something already
  known); the cheapest test exceeds substrate (→ HOLD, not a bigger run); the claim is
  not yet stated sharply enough to kill.
Verdict: DO — the default action for any C-grade mechanism claim with an affordable test.
```

```text
Current state: An artifact or claim is approaching a promotion gate; its framing was
  produced by a generator with persuasive context.
Decision needed: Does this survive attack by someone who did not build it?
Candidate next action: COLD-START ADVERSARIAL REVIEW
Information gained: Decisive weaknesses; the difference between fluency and support;
  which attacks have affordable answers.
Cost: Low–medium (one agent session + packet preparation).
Reversibility: Fully reversible.
Risk: Packet preparation smuggles the generator's framing into the "cold" context
  (contamination via packet); reviewer produces adversarial rhetoric without evidence
  (named failure mode of operator 10).
Delay cost: Low — but nonzero when it stalls artifacts with no promotion risk.
Who should execute: An agent that has not seen the generation context; different stance;
  ideally different model family.
Who should audit: Governance check on the packet itself: does it contain conclusions or
  only evidence?
When this action is wrong: No promotion boundary is being crossed (its own trigger
  exclusion); or it substitutes for an affordable experiment — review cannot settle what
  a falsifier can.
Verdict: DO at every promotion gate; BLOCK the promotion if skipped.
```

```text
Current state: A review or falsifier has returned specific deltas on an artifact whose
  core is useful.
Decision needed: Is revision worth more than the next new result?
Candidate next action: ARTIFACT REVISION
Information gained: None directly — revision converts existing evidence into usable form.
Cost: Author time; agent time.
Reversibility: Fully reversible.
Risk: Polish loop — revising toward beauty instead of toward the named deltas;
  revision as procrastination against the next kill test.
Delay cost: Medium when the artifact blocks others (a README blocking reproduction);
  low otherwise.
Who should execute: Execution agent or original author.
Who should audit: Acceptance reviewer, against the delta list only — new demands beyond
  the list re-enter as a new review, not scope creep.
When this action is wrong: Revising before any review has produced deltas (polishing on
  taste); revising an artifact whose claim is still HOLD (claim first, artifact second).
Verdict: DO only against a named delta list; otherwise DELAY.
```

```text
Current state: Context exceeds working memory; multiple agents have produced outputs;
  a decision or hand-off is imminent.
Decision needed: What is actually believed, dead, active, and next?
Candidate next action: CONTEXT COMPRESSION (decision state)
Information gained: None new — prevents loss: dead regions, pending falsifiers,
  binding decisions, the next irreversible step.
Cost: Low.
Reversibility: The state object is revisable, but errors in it propagate silently to
  every agent that resumes from it — practically semi-irreversible.
Risk: Beautiful-summary failure (narrative instead of state); killed ideas resurrected
  because a dead region was dropped; assumptions promoted to facts in compression.
Delay cost: Compounds — skipping compression before a hand-off taxes every later step.
Who should execute: Any agent with full-context access.
Who should audit: Spot-check against the raw record: every "resolved decision" must
  trace to an actual decision event; every dead region to an actual kill.
When this action is wrong: Context is small and no hand-off is near (its own
  exclusion); or compression is used to re-open workflow design when execution should
  begin (named failure mode).
Verdict: DO before any hand-off, promotion, or compaction; otherwise DELAY.
```

```text
Current state: A claim has grade A/B evidence, survived cold review, has an occupancy
  map, and its falsifier has run and survived.
Decision needed: Commit reputation, budget, or public claim?
Candidate next action: HUMAN PROMOTION
Information gained: A binding commitment plus human-held context (venue strategy,
  taste, risk appetite) that no agent in this corpus is authorized to hold.
Cost: Human attention — the scarcest resource in the loop.
Reversibility: Low — promotion typically triggers irreversible acts (announcement,
  large run, installation).
Risk: Human rubber-stamps agent consensus (agreement illusion reaching the top);
  or human becomes bottleneck for decisions that needed no promotion.
Delay cost: Real — promotion queues stall everything gated behind them.
Who should execute: Human only.
Who should audit: The irreversibility audit runs BEFORE the promotion request is filed,
  so the human decides on a completed packet, not a pitch.
When this action is wrong: Requested for reversible internal steps (over-escalation);
  requested before the evidence gates so the human is asked to substitute judgment for
  missing evidence.
Verdict: DO only with the full packet (grades, search log, falsifier result, review
  verdicts, irreversibility audit); otherwise BLOCK the request itself.
```

```text
Current state: Recent cycles produce no new kill conditions, no verdict changes, no new
  evidence grades; or the queue is empty of claims that any affordable action can move.
Decision needed: Is continued activity extracting information or simulating progress?
Candidate next action: STOP THE WORKFLOW
Information gained: None — stopping conserves budget and prevents process from
  manufacturing artifacts to justify itself.
Cost: Psychological only; feels like failure, is not.
Reversibility: Fully reversible — stopped workflows restart from the state object.
Risk: Stopping just before a decisive result (mitigated: check pending falsifiers
  first — never stop with a funded, runnable falsifier idle); stopping used to avoid a
  hard verdict.
Delay cost: Zero by definition if the stop test passed.
Who should execute: Whoever holds the state object; human ratifies if a program is
  being paused.
Who should audit: The stop decision itself is logged in the state object with the
  restart condition.
When this action is wrong: Pending falsifiers are funded and runnable; a promotion
  packet is one action from complete.
Verdict: DO when two consecutive cycles change no verdict and add no kill condition;
  this is the anti-loop rule applied to execution.
```

---

## Closing artifacts

```text
Action selection algorithm:
1. If context exceeds working memory or a hand-off/promotion is imminent:
     → CONTEXT COMPRESSION first. (Cheap; everything else degrades without it.)
2. For the top active candidate, identify its blocking uncertainty:
     a. External-state uncertainty (novelty, market, model status) → LIVE SEARCH.
     b. Mechanism/effect uncertainty with affordable test          → MINIMUM FALSIFIER.
     c. Framing uncertainty at a promotion gate                    → COLD-START REVIEW.
     d. Usability uncertainty with named deltas                    → ARTIFACT REVISION.
3. Order among unblocked candidates: highest expected verdict-change per unit cost;
   search before compute; audit before promotion; never run a falsifier on an
   unsearched novelty claim.
4. When a claim clears all gates → assemble the promotion packet → HUMAN PROMOTION.
5. After every KILL/RESCOPE → run failure conversion before selecting the next action.
6. If no action can change any verdict → STOP.

Anti-loop rule:
An action is admissible only if it can change a verdict, change an evidence grade, or
add a kill condition. Two consecutive cycles without any of the three → STOP and
escalate the stop decision to the state object. (This extends the corpus's
document-level anti-loop rule to execution: the original rule stops workflow expansion;
this one stops workflow *churn*.)

When to stop planning:
- The next planning artifact would only rename an existing operator or re-partition the
  same decisions (meta-skill-expansion-guide rule).
- The plan already names: next falsifier, budget cap, kill result, and owner. More plan
  after that point is narrative.
- Planning is being used to defer an affordable falsifier — the falsifier IS the plan's
  next line.

When to start executing:
All four present: (1) a stated claim with a do-not-claim boundary; (2) an occupancy
hypothesis (with live search done if novelty-bearing); (3) a falsifier with budget cap
and pre-committed kill/survive results; (4) an assigned executor separate from the
claim owner. Missing any one → the next action is to produce it, not to run.
```

Tradeoff summary: this ordering privileges cheap information (search, review) over
expensive information (compute) and privileges kill-tests over demonstrations. Its known
cost: it is slow to reward positive results, because every positive step queues behind an
audit. The compensating rule is the admissibility test — audits that cannot change a
verdict are inadmissible, which keeps the audit chain from becoming the loop itself.
