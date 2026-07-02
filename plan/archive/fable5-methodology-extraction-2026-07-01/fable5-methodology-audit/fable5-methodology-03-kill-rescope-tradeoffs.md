# Fable5 Methodology Review — 03. Kill / Rescope / Hold Tradeoffs

Question: what are the tradeoffs between killing an idea, holding it, and rescoping it?

Framing note: KILL, HOLD, and RESCOPE are not points on a severity scale. They are
answers to three different questions. KILL answers "is there anything here?" (no).
RESCOPE answers "is the surviving part a different, smaller contribution with its own
falsifier?" (yes). HOLD answers "could this be decided now with affordable evidence?"
(no — so park it with a re-entry condition). The most common boundary error in the
corpus's own calibration suite is treating RESCOPE as "KILL but polite."

---

## Case analyses

```text
Case: 1. Method is occupied, measurement may survive.
What dies: The headline method claim ("our learned policy beats heuristics").
What may survive: The decomposition/measurement the method was built on (e.g.,
  sampler-limited vs model-limited attribution via oracle search).
Independent value test: Would the measurement be worth publishing if the method had
  never been proposed? Does it have its own falsifier (e.g., oracle gap ≈ 0 kills the
  measurement claim too)?
Tradeoff if killed too early: The system discards the only durable contribution —
  measurements outlive the samplers that occupy the method space.
Tradeoff if kept too long: The measurement becomes a fig leaf; the team keeps building
  the dead method "to strengthen the measurement paper."
Required evidence: Occupancy map showing method territory owned; a falsifier for the
  measurement that does not route through the dead method.
Reviewer attack: "This is a method paper wearing a measurement costume."
Verdict boundary: RESCOPE only if the measurement stands with the method deleted
  entirely from the writeup; otherwise KILL.
Conversion rule: Dead method → constraint ("method-space X occupied as of date D; do
  not re-enter without a differential") + the surviving measurement becomes its own
  candidate with its own gate.
```

```text
Case: 2. Object language fails the deletion test.
What dies: The object claim — the vocabulary was decorative; what remains is a standard
  method.
What may survive: The standard method itself, if it has a delta (as engineering work,
  honestly labeled); occasionally a diagnostic that the failed language accidentally
  pointed at.
Independent value test: With all object vocabulary removed, does the rewrite still
  forbid any observation or predict any failure ordering? If yes, the object was real
  but badly stated — rewrite, don't kill.
Tradeoff if killed too early: Early-stage object language is often under-operationalized
  rather than empty (operator 7's own noted failure mode: "too harsh on early object
  language"); killing at first vagueness destroys fragile-but-real reframings.
Tradeoff if kept too long: Laundering becomes institutional — the system's papers grow
  a reputation for vocabulary inflation, a compounding reviewer-trust cost.
Required evidence: The deletion-test artifact itself: original language, plain rewrite,
  list of what disappeared.
Reviewer attack: "Delete section 3's terminology and the method is ALBEF-class
  engineering."
Verdict boundary: KILL the object claim when nothing disappears under deletion after
  ONE operationalization attempt; RESCOPE to honest engineering if a delta exists.
Conversion rule: Failed language → laundering pattern added to the do-not-repeat list
  (specific phrases, e.g., "information-geometric alignment" without an observable).
```

```text
Case: 3. Prior art owns the method but not the diagnostic.
What dies: Method novelty.
What may survive: A diagnostic/instrument the occupants never built (e.g., the field
  has samplers but no attribution of where the error lives).
Independent value test: Do the occupants' papers *need* this diagnostic and lack it?
  Would the diagnostic change how occupants compare their own methods?
Tradeoff if killed too early: The system walks away from the cheapest kind of durable
  contribution — instruments are low-compute and highly citable by the very occupants
  who killed the method.
Tradeoff if kept too long: Diagnostic inflation — every dead method retroactively
  claims a "diagnostic contribution," and RESCOPE becomes a face-saving ritual.
Required evidence: Occupancy map explicitly separating method occupancy from
  measurement occupancy (operator 8, step 5 — the corpus gets this right).
Reviewer attack: "The diagnostic is an ablation table, not an instrument."
Verdict boundary: RESCOPE only if the diagnostic has (a) users other than this project
  and (b) its own falsifier (it could fail to discriminate). Otherwise KILL.
Conversion rule: Method death funds the instrument's requirements list: what the
  occupants cannot currently observe becomes the instrument's spec.
```

```text
Case: 4. Falsifier is too expensive.
What dies: Nothing yet — and that is the danger: nothing can die, so nothing can be
  believed either.
What may survive: The claim as a parked hypothesis; sometimes the falsifier itself
  converts into an infrastructure/benchmark contribution (protocol step 7's rule).
Independent value test: Is there a cheaper proxy falsifier with stated loss of
  identification power? Is the infrastructure needed to make it cheap itself a
  contribution?
Tradeoff if killed too early: Killing claims merely because this lab cannot test them
  conflates "false" with "unaffordable" — and silently shrinks the research frontier to
  the substrate's shadow.
Tradeoff if kept too long: Zombie accumulation — unfalsifiable-in-practice claims sit
  in HOLD, absorb attention, and are gradually treated as validated by survival.
Required evidence: A written falsifier with real budget estimate; a documented search
  for cheaper proxies; an expiry date.
Reviewer attack: Not applicable pre-publication — the attack here is internal: "this
  HOLD is a KILL you are not admitting."
Verdict boundary: HOLD with written falsifier + expiry (default 6 weeks per the state
  discipline) when a substrate change could make it affordable; KILL-for-this-lab when
  no plausible substrate change would.
Conversion rule: Expensive falsifier → infrastructure candidate ("what tool would make
  this test cheap?") or → explicit region-close with the substrate condition that would
  reopen it.
```

```text
Case: 5. Claim is true but not useful.
What dies: The claim's status as a research direction (e.g., a statistically real 0.1%
  gain that changes no decision, or a mechanism finding in a setting nobody deploys).
What may survive: A constraint or calibration datum ("effect exists but is bounded by
  ε; do not build on it").
Independent value test: Does any downstream decision change if this claim is true vs
  false? If no decision changes, the claim has zero action value regardless of truth.
Tradeoff if killed too early: Some true-but-small effects compound or become large
  under a different substrate; killing the *record* of them wastes the evidence.
Tradeoff if kept too long: True-but-useless claims are the most seductive zombies —
  they survive every attack (they are true!) while producing nothing.
Required evidence: An explicit decision-relevance statement: name one decision that
  flips on this claim. Failure to name one is the kill condition.
Reviewer attack: "So what?" — the least sophisticated and most lethal review sentence.
Verdict boundary: KILL as a direction; ARCHIVE as evidence (the distinction matters:
  kill the pursuit, keep the datum).
Conversion rule: True-but-useless → recorded bound ("effect ≤ ε under conditions C")
  in the constraint ledger; future candidates citing this effect must show why their
  setting escapes the bound.
```

```text
Case: 6. Artifact is polished but not usable.
What dies: The SHIP verdict — polish is explicitly not readiness
  (artifact-acceptance-review's first named failure mode).
What may survive: The artifact core, after revision against acceptance tests; the
  polish itself is sunk cost, not evidence.
Independent value test: Can a person who did not build it complete the enabled action
  (run the README, apply the skill, reproduce the report) without hidden context?
Tradeoff if killed too early: Discarding a 90%-usable artifact over fixable gaps wastes
  the accumulated work — REVISE exists precisely for this.
Tradeoff if kept too long: A polished-but-unusable artifact in circulation is worse
  than none: it consumes trust, and hostile readers extract stronger claims than it
  supports.
Required evidence: An executed acceptance test by a non-author (fresh-environment run,
  cold-agent application).
Reviewer attack: Hostile-reader misunderstanding — "this demo implies production
  readiness."
Verdict boundary: REVISE when deltas are enumerable; HOLD when the missing piece is
  evidence (not writing); KILL when the artifact's claim is unsupported at the core.
Conversion rule: Each acceptance failure becomes a checklist item for the artifact
  type — the acceptance suite grows from real failures, not imagined ones.
```

```text
Case: 7. Direction is interesting but not a program.
What dies: The program claim — the framing that a set of results shares a hard core and
  generates predictions.
What may survive: Individual papers; a "working thesis" entry in the state object,
  which is the honest name for a pre-program.
Independent value test: Has the alleged core generated ≥1 new tested prediction that a
  no-core view would not have produced? (File 01's research-program standard.)
Tradeoff if killed too early: Programs are grown, not born; refusing all program
  framing keeps work permanently fragmented and forfeits the compounding returns of a
  positive heuristic.
Tradeoff if kept too long: Premature program framing is narrative lock at maximum
  scale — experiments become story defense, and the identity cost of unwinding grows
  monotonically.
Required evidence: Two independently confirmed results + one tested generative
  prediction + one survived external review.
Reviewer attack: "These are three papers with a shared adjective."
Verdict boundary: RESCOPE to "direction with a working thesis" (state-object entry,
  revisable) — the program claim itself goes to HOLD with the two-results gate as
  re-entry condition.
Conversion rule: The unproven core is written as an explicit falsifiable thesis in the
  state object, so the day it earns program status is detectable rather than declared.
```

```text
Case: 8. Agent output is fluent but not independently checked.
What dies: The output's authority — not necessarily its content.
What may survive: The content, after cold-start review or mechanical verification;
  fluency is orthogonal to correctness, which is precisely why it is dangerous.
Independent value test: Does the output survive an auditor who saw only the evidence
  packet, not the persuasive context? For factual pieces: do the checkable claims check?
Tradeoff if killed too early: Discarding all unaudited agent output makes the audit
  chain the bottleneck for everything, including trivia (over-governance failure mode).
Tradeoff if kept too long: Fluent-unverified output is the primary vector of false
  promotion in an LLM-driven system — every gate downstream inherits its errors with
  interest.
Required evidence: Scale by consequence: mechanical verification for local facts;
  cold-start review for promotion-bound claims; live search for novelty content.
Reviewer attack: (internal) "Which of these statements has a source outside the model
  that produced it?"
Verdict boundary: BLOCK from promotion until independently checked; freely usable as
  draft material below promotion gates.
Conversion rule: Each caught fluency-failure becomes a calibration case for the suite —
  the mismatch taxonomy grows from real contamination events.
```

---

## Closing artifacts

```text
Automatic KILL rules:
- Deletion test changes nothing after one operationalization attempt.
- Occupancy search shows object AND falsifier both owned.
- Survivor of a failed claim is only a softer restatement of the dead claim.
- No decision changes whether the claim is true or false ("so what" failure).
- Claim remains grade D after one clarification attempt.
- No evidence type can even be named for the claim.

Automatic RESCOPE rules:
- Method occupancy confirmed + measurement survivor with its own independent falsifier.
- Object language dies but a delta-bearing engineering contribution remains (relabel
  honestly, no object vocabulary).
- Program claim unproven but individual results are sound → rescope to working thesis.
- Broad claim fails reviewer attack, but a narrower claim survives it at a lower venue.

Automatic HOLD rules:
- Novelty-bearing claim before live search executes.
- Evidence grade C with a specified but not-yet-run falsifier.
- Falsifier exceeds substrate but a plausible substrate change exists → HOLD with
  expiry and re-entry condition (no expiry = zombie; see boundary mistakes).
- Artifact whose missing piece is evidence rather than writing.

Automatic DO rules:
- Grade A/B evidence + occupancy hypothesis (searched, if novelty-bearing) + funded
  falsifier with pre-committed kill result + survived cold-start attack.
- The falsifier itself: designing one is always DO for any live C-grade claim.

Common boundary mistakes:
1. RESCOPE as polite KILL — issuing RESCOPE with a survivor that has no independent
   falsifier. Test: if the "survivor" can't die on its own, it isn't alive on its own.
2. KILL that destroys the measurement along with the method (calibration suite case 3's
   named Opus risk).
3. HOLD without expiry — the zombie factory; HOLD must carry a re-entry condition and a
   date or it is a deferred KILL executed dishonestly.
4. Treating survival of attacks as promotion evidence — surviving review only removes
   objections; only falsifiers add support.
5. Converting nothing on death — a KILL that emits no constraint, exclusion rule, or
   instrument spec wastes the most expensive thing the system buys: negative results.
```

Tradeoff summary: the corpus's verdict machinery is asymmetric by design — cheap to
kill, expensive to promote. The under-priced risk is the false negative: fragile real
objects killed at first vagueness (case 2) and unaffordable truths killed as
unaffordable (case 4). The compensating mechanisms must be procedural, because no
reviewer instinct will supply them: one mandatory operationalization attempt before a
deletion-kill, and expiry-bearing HOLDs instead of quiet kills for substrate-limited
claims.
