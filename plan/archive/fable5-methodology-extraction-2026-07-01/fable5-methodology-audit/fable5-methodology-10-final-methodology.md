# Fable5 Methodology Review — 10. Final Methodology

Question: what is the final compact methodology for deciding what to believe, what to
do, what to kill, what to rescope, and what not to commit too early?

---

## 1. One-page methodology

```text
BELIEVE
Grade every claim A–E before arguing about it. A composite claim's grade is the MIN of
its links. Novelty and current-state claims are grade D until a live search with a
sufficiency log executes. Mechanism claims are grade C until an intervention with a
manipulation check runs. Two agreeing sources count once unless their independence
(context, stance, blind spots) is argued. Elegance, fluency, consensus, and polish are
not evidence types.

DO
Choose the action with the highest expected verdict-change per unit cost:
compress state before hand-offs; search before compute; falsify before building;
cold-review before promoting; revise only against named deltas; stop when two cycles
change no verdict. An affordable, unrun falsifier is an automatic promotion blocker —
at that point the system is choosing not to know.

KILL / RESCOPE / HOLD
KILL when the deletion test changes nothing (after one operationalization attempt),
when occupancy owns both object and falsifier, when no decision flips on the claim's
truth, or when the survivor is only a softer restatement. RESCOPE only when the
survivor has independent value — its own falsifier, its own users, fundable if
proposed fresh. HOLD only with an expiry date and a re-entry condition; a HOLD without
either is a KILL executed dishonestly. Every death converts: constraint, exclusion
rule, instrument spec, or region-close — or the autopsy is incomplete.

COMMIT
Classify every pending decision by lock type (narrative, benchmark, method, evidence,
compute, reputation, product). Irreversible decisions require: a minimum-evidence gate
met at grade, a named reversible substitute, a concretely stated delay cost, and —
for reputation, direction, and program locks — a human signature on a completed
packet. Categorical blocks, no exceptions: self-review at promotion gates; large
compute before the cheap falsifier; public capability claims before validation.

GOVERN
Route by stance and evidence access, not model identity. Generator ≠ auditor at every
promotion gate; auditors receive cold packets (evidence, not conclusions). Down-
verdicts are self-administrable; up-verdicts require an independent substrate; final
promotion is human. Automate gates and bookkeeping; route judgment cores (object
naming, rewrite fairness, hit adjudication, baseline choice, fund-it-fresh) to
explicit judgment. Audit the governance itself: a gate that never changes a verdict
is dead; an escalation rate that makes the human the bottleneck is a defect.
```

## 2. Decision tree

```text
New claim / idea / artifact / commitment arrives
│
├─ Is it a commitment (locks path, budget, reputation)?
│   ├─ Reversible → decide fast, log, proceed.
│   └─ Irreversible → evidence gate met? substitute named? delay cost stated?
│        ├─ all yes → human signs → PROCEED
│        ├─ evidence short, cheap step exists → DELAY (run search/falsifier first)
│        ├─ too broad, smaller reversible step learns the same → RESCOPE
│        └─ contaminates evidence / unvalidated public claim / big compute
│           before cheap test → BLOCK
│
├─ Is it an artifact crossing a use boundary?
│   └─ Acceptance path: target user? claim ≤ evidence? non-author test executed?
│      hostile-reader pass? → SHIP / REVISE (named deltas) / HOLD (missing
│      evidence) / KILL (unsupported core or contradictory redundancy)
│
└─ It is a claim / idea:
    1. State it in one sentence + its do-not-claim boundary. Cannot? → not ready.
    2. Grade evidence (chain rule). D after one clarification → KILL.
    3. Stress point concrete? No → no idea generation yet.
    4. Deletion test. Nothing lost after one operationalization attempt → KILL
       (delta-bearing engineering may proceed honestly relabeled).
    5. Occupancy: hypothesis → live search → adjudication by non-generator.
       Object + falsifier owned → KILL. Method owned, measurement free → RESCOPE.
       Unsearched → HOLD (no novelty wording).
    6. Minimum falsifier: affordable? → run it (pre-committed kill result).
       Unaffordable → HOLD with expiry + substrate re-entry, or convert to
       instrument candidate.
    7. Cold-start reviewer attack. Unresolved attack removing the contribution →
       KILL/RESCOPE. Survived → assemble promotion packet.
    8. Human promotion. Then, and only then: narrative, announcement, scale.
    9. On any death: conversion law → constraint / exclusion / instrument /
       region-close, into the ledger with scope + review date.
```

## 3. Role assignment table

| Function | Owner | Forbidden to | Key control |
| --- | --- | --- | --- |
| Generate candidates, drafts, framings | Generator agent | Final-audit its own output at any promotion gate | Label self-review as drafting |
| Execute runs, organize artifacts | Executor | Interpret results into claims; deviate from spec silently | Pre-registered spec; deviations void claim-bearing use |
| Verify code, diffs, intervention-fired | Code agent | Judge experiment design or claim truth | Receives spec + logs, never the narrative |
| Execute searches, log negatives | Live-search agent | Adjudicate novelty | Sufficiency log (queries, dates, coverage) |
| Adjudicate search hits | Non-generator adjudicator | — | Deletion test applied to occupants |
| Attack claims and artifacts | Cold-start adversarial reviewer | Up-verdicts alone; editing what it reviews | Cold packet audited for smuggled conclusions |
| Audit process and gates | Methodology critic | Overturning verdicts on merits | Reads the record, not the pitch |
| Design falsifiers | Falsifier designer | Building the demo it tests | Pre-committed kill result or reject |
| Promote, kill programs, announce | Human | Deciding from a pitch instead of a packet | Completed packet required; overrides recorded |

## 4. Verdict table (unified across the corpus's four vocabularies)

| Situation | Claims/ideas | Artifacts | Commitments | Meaning |
| --- | --- | --- | --- | --- |
| Passes all gates | DO | SHIP | PROCEED | Act under stated scope |
| Core dies, independent survivor exists | RESCOPE | REVISE | RESCOPE | Smaller thing, own falsifier/deltas |
| Evidence insufficient, decidable later | HOLD (+ expiry) | HOLD | DELAY (+ delay cost) | Park with re-entry condition |
| Nothing survives / contamination / unsupported | KILL (+ conversion) | KILL | BLOCK | Stop; bank the constraint |

Rule: any verdict issued without its parenthetical companion (expiry, conversion,
delay cost, deltas) is incomplete and procedurally invalid.

## 5. Tradeoff table

| Tradeoff | Cheap side | Expensive side | Balancing rule |
| --- | --- | --- | --- |
| False promotion vs false kill | Killing is cheap per-act | Killed real objects are invisible losses | One operationalization attempt before deletion-kills; anti-overkill cases in calibration |
| Governance hygiene vs velocity | Separation prevents contamination | Latency, context loss, human bottleneck | Dead-gate test; escalation budget; review only what a falsifier can't settle faster |
| HOLD safety vs zombie accumulation | HOLD avoids wrong verdicts | Un-expired HOLDs rot into de-facto beliefs | Mandatory expiry + re-entry condition |
| Commitment risk vs delay cost | Blocking prevents lock-in | Windows close; blocking is never locally punished | No BLOCK/DELAY without a stated delay cost and substitute |
| Search depth vs novelty paralysis | More queries, more coverage | Search never terminates | Sufficiency standard scaled to stakes; scoped wording |
| Mechanization vs judgment displacement | Gates automate cleanly | Automated cores detach verdicts from reality | Automate gates and bookkeeping; route cores to judgment |
| Calibration fidelity vs accuracy | Agreement with the reference judge is measurable | The judge is not ground truth | Second label source from outcomes; rotate/hold-out cases |
| Pipeline discipline vs serendipity | Stages prevent laundering | Method-first ideas arrive out of order | Cheap kills may short-circuit; re-entry is always via the gates, not around them |

## 6. Anti-patterns

```text
1. Object laundering — renaming a standard method in object vocabulary; caught by the
   deletion test, prevented by demanding a forbidden observation.
2. Novelty by memory — "I'm not aware of prior work" as evidence; no novelty wording
   without a search log.
3. Fluent self-review — harshness mistaken for independence; structure, not style,
   makes a review independent.
4. Agreement illusion — shared framing counted as multiple witnesses.
5. Demonstration wearing a falsifier costume — a test with no outcome labeled KILL.
6. Polish as readiness — the artifact gate's founding failure; acceptance tests are
   executed, not inferred from formatting.
7. RESCOPE as polite KILL — survivors with no independent falsifier; zombie scoping.
8. HOLD without expiry — deferred kills executed dishonestly; zombie beliefs.
9. Narrative lock — the story written before the kill experiment; experiments become
   story defense.
10. Veto engine — irreversibility audits that only ever BLOCK; no delay cost stated,
    no substitute named.
11. Escalation flooding — grade-A questions routed to humans; caution spending the
    wrong resource.
12. Workflow metastasis — new process steps adding no kill condition, schema, or
    boundary; the anti-loop rule exists to be enforced, including against this review.
13. Un-nameable-doubt HOLD — "something might be wrong" without a checkable gap;
    infinite audit as a way to never say yes.
14. Conversion skipped — deaths that bank nothing; the most expensive purchase the
    system makes (negative results) thrown away.
15. Vocabulary transfer — research operators exported as jargon; no target-domain
    decision changes, no new kill condition arrives.
```

## 7. The minimal loop

```text
Calibrate belief
-> compress decision state
-> assign agent roles
-> scan stress point
-> extract object
-> test deletion
-> map occupancy
-> design falsifier
-> audit commitment risk
-> decide DO / RESCOPE / HOLD / KILL
-> accept or reject artifact
-> convert failure into constraint
```

Loop invariants (what makes one pass legitimate):
- every belief entering the loop carries a grade; every composite, the min of its links;
- the state object distinguishes dead regions from active candidates before roles run;
- no idea precedes a concrete stress point; no verdict precedes the deletion test;
- no novelty wording precedes the search log; no promotion precedes the falsifier
  when one is affordable;
- no irreversible act precedes its gate, substitute, and stated delay cost;
- no verdict leaves without its companion (expiry / conversion / deltas / delay cost);
- and the loop itself is subject to the dead-gate test: any stage that has not changed
  a verdict in recent memory is audited, not venerated.

---

## Final rule

```text
Use this methodology when a claim, framing, direction, artifact, or commitment must
survive intelligent attack before spending compute, reputation, or irreversible
attention.
```

And its converse, which the corpus implies and this review makes explicit: when the
act is cheap, reversible, and private — draft, explore, run the toy, sketch the wild
object — do not spend the machinery on it. The gates exist to make bold exploration
safe to run at full speed below them, not to slow everything above them equally.
