# Fable5 Methodology Review — 04. Commitment Risk

Question: how should the system decide what cannot be committed too early?

Base machinery: `irreversible-decision-audit.md` (lock types, reversible substitutes,
PROCEED/DELAY/RESCOPE/BLOCK). Amendment applied throughout: every DELAY and BLOCK must
state its delay cost explicitly — an audit that only counts commitment risk is a veto
engine, not a decision instrument.

---

```text
Commitment: Paper narrative (writing the full story/framing).
What it locks: The research question's shape; which experiments count as "supporting";
  the interpretation of future results (experiments become story defense).
Reputation risk: Low pre-submission; high once circulated.
Compute risk: Indirect — narrative-driven experiments burn compute defending the story.
Evidence risk: High — narrative lock is evidence contamination at the design level.
Narrative risk: Maximal by definition.
Delay cost: Low — a claim registry preserves all planning value of a narrative.
Minimum evidence before commitment: Falsifier run and survived; occupancy searched;
  reviewer attack survived.
Reversible substitute: Claim registry with kill conditions (the audit document's own
  substitute); framing bullets, not prose.
Decision gate: Has the kill experiment for the central claim returned?
Verdict: DELAY until the central falsifier returns; PROCEED afterward.
```

```text
Commitment: Benchmark choice (one benchmark as the claim's centerpiece).
What it locks: The research question itself — the metric becomes the claim owner; all
  tuning targets it; anti-Goodhart pressure inverts into Goodhart pressure.
Reputation risk: Medium — a benchmark later shown contaminated taints the result.
Compute risk: Medium — re-running on a replacement benchmark doubles eval cost.
Evidence risk: High — single-benchmark evidence cannot distinguish capability from
  benchmark fit.
Narrative risk: The benchmark's framing colonizes the paper's framing.
Delay cost: Low — using several diagnostics costs little before the claim is fixed.
Minimum evidence before commitment: The real-world failure defined first; the
  benchmark validated as an instrument for THAT failure (contamination check, known
  critiques searched).
Reversible substitute: Benchmark as one diagnostic among several, none owning the claim.
Decision gate: Can the claim be stated without naming the benchmark? If not, the
  benchmark is the claim — RESCOPE.
Verdict: RESCOPE (diagnostic role) until the claim is benchmark-independent.
```

```text
Commitment: Method implementation (building the full method first).
What it locks: Contribution type — method-paper framing displaces a possibly stronger
  measurement paper (method lock); sunk implementation biases every later verdict.
Reputation risk: Low.
Compute risk: Medium — implementation and tuning time.
Evidence risk: Medium — the implemented method becomes the lens for all analysis.
Narrative risk: "We built it, so the paper is about it."
Delay cost: Real when the method is on the critical path of the falsifier — sometimes
  a minimal implementation IS the falsifier; the gate is scope, not existence.
Minimum evidence before commitment: The rescope question answered first: is the
  contribution method or measurement? (Case 1/3 boundaries in file 03.)
Reversible substitute: Minimal-form implementation sufficient for the falsifier only
  (the protocol's "minimal method form"), no engineering beyond the kill test.
Decision gate: Does any implementation beyond the falsifier's needs precede the
  falsifier's result?
Verdict: PROCEED for falsifier-scoped implementation; DELAY everything beyond it.
```

```text
Commitment: Large compute run.
What it locks: Budget (gone), and judgment — sunk cost converts "should we continue"
  into "how do we justify"; a large run's result also anchors all future small runs.
Reputation risk: Internal only, unless announced.
Compute risk: Maximal — the category's defining risk.
Evidence risk: Medium — one large run without seeds/ablations produces impressive,
  fragile numbers.
Narrative risk: Large runs demand large stories to justify them retroactively.
Delay cost: Real when external deadlines exist — but a cheap falsifier costs days
  against a run costing weeks; the ratio nearly always favors the falsifier.
Minimum evidence before commitment: The cheap falsifier has run AND survived; the
  large run's incremental question ("what does scale add?") is stated and is not
  answerable at small scale.
Reversible substitute: Staged runs with kill checkpoints (abort criteria pre-committed
  at 10%/25% of budget).
Decision gate: Written answer to "what does this run tell us that the falsifier did
  not?" plus pre-committed abort criteria.
Verdict: BLOCK before the cheap falsifier; PROCEED after, with staged checkpoints.
```

```text
Commitment: Public announcement.
What it locks: Reputation (the system's and the operator's); external expectations;
  the freedom to quietly kill the announced thing (announced projects die loudly).
Reputation risk: Maximal.
Compute risk: Indirect — announced systems demand maintenance compute.
Evidence risk: High — announcement pressure degrades evidence standards for everything
  that supports the announced claim ("we said it works, so find that it works").
Narrative risk: The announcement becomes the narrative everyone defends.
Delay cost: Occasionally real (priority claims, community timing) — must be argued,
  not assumed; "momentum" is not a delay cost.
Minimum evidence before commitment: The announced claim at grade A/B; calibration or
  validation results for system claims (the corpus's own case: no Research-OS
  announcement before blind false-promotion calibration).
Reversible substitute: Limited internal share with named recipients; preprint scoped
  to what the evidence supports; "early results" framing with explicit limits.
Decision gate: Would we be comfortable if the announcement were quoted against the
  weakest supporting evidence line? (Chain rule from file 01: the announcement's grade
  is the min of its claims' grades.)
Verdict: DELAY by default; BLOCK for capability/system claims lacking validation;
  PROCEED only from a completed promotion packet, human-signed.
```

```text
Commitment: Same-agent self-review (accepting a generator's review of its own output).
What it locks: The evidence channel — once a self-review is accepted as "review," the
  audit trail is contaminated and cannot be un-contaminated retroactively; downstream
  consumers cannot distinguish it from independent review.
Reputation risk: Low per instance; systemic over time (the system's verdicts stop
  meaning anything).
Compute risk: None — that is the temptation; self-review is free.
Evidence risk: Maximal per unit cost — the defining evidence-contamination case.
Narrative risk: Fluent self-critique launders the generator's framing as scrutiny.
Delay cost: The honest cost of separation is one extra agent session — small, bounded,
  and always affordable at promotion gates.
Minimum evidence before commitment: None exists — there is no evidence level at which
  self-review becomes independent review.
Reversible substitute: Cold-start review packet to a separate agent (evidence only, no
  conclusions); below promotion gates, self-review is usable as drafting, labeled as such.
Decision gate: Is the output crossing a promotion boundary? Then reviewer ≠ generator,
  no exceptions.
Verdict: BLOCK at promotion gates, categorically; PROCEED below them with labeling.
```

```text
Commitment: Installed skill (a procedure becomes standing agent behavior).
What it locks: Every future session's behavior; errors compound silently across all
  work the skill touches; uninstalling requires noticing the harm, which installed
  skills themselves can mask.
Reputation risk: Indirect — the skill's failure modes propagate into shipped artifacts.
Compute risk: Low direct; high indirect if the skill mis-routes work.
Evidence risk: High — an installed judgment skill IS an evidence standard; installing
  an uncalibrated one changes what the system believes everywhere at once.
Narrative risk: Installed process feels validated by existing ("we have a skill for
  this" ≠ "this works").
Delay cost: Low — drafts are invocable manually while calibration runs.
Minimum evidence before commitment: Blind calibration passed against a stated
  threshold (the corpus lacks the threshold — set one: e.g., verdict-class agreement on
  ≥80% of ≥15 cases, zero false-DO) — and the calibration labels must not be authored
  solely by the system under test.
Reversible substitute: Draft skills invoked explicitly per-session (current state of
  opus-skill-drafts.md), never auto-triggered.
Decision gate: The calibration suite's delta log exists, is non-empty, and its patches
  have been retested.
Verdict: DELAY — this is the corpus's own "next irreversible decision," and it is
  correctly parked pending calibration.
```

```text
Commitment: Shipped artifact.
What it locks: External users' expectations and workflows; the claim the artifact
  embodies (hostile readers extract the strongest reading, which then must be defended).
Reputation risk: Scales with distribution and with the gap between polish and support —
  a polished artifact with weak evidence is a reputation short position.
Compute risk: Maintenance burden.
Evidence risk: Medium — shipped artifacts get cited as evidence by others.
Narrative risk: The artifact's implicit claim outruns its documented claim.
Delay cost: Real for artifacts blocking other people; measure by who is waiting.
Minimum evidence before commitment: Acceptance review passed (SHIP verdict) including
  a non-author acceptance test and hostile-reader check.
Reversible substitute: Scoped release — named users, stated limits, feedback channel;
  version marked pre-1.0 with explicit non-claims.
Decision gate: SHIP verdict from an acceptance reviewer who is not the author.
Verdict: PROCEED with SHIP verdict; REVISE/HOLD paths per the acceptance document.
```

```text
Commitment: Product direction.
What it locks: Roadmap, hiring/tooling choices, which research gets resourced; the
  direction becomes the lens for evaluating all subsequent evidence.
Reputation risk: High externally if announced; internally it locks team identity.
Compute risk: High — direction misallocation is the largest compute risk there is,
  dwarfing any single run.
Evidence risk: High — direction lock creates system-wide confirmation pressure.
Narrative risk: Directions are narratives with budgets.
Delay cost: High and real — markets and fields move; this is the one commitment where
  delay cost can genuinely rival commitment risk, and the audit must price both.
Minimum evidence before commitment: Strategic-direction standard from file 01: stress
  point + occupancy/competitor map (live-searched) + substrate fit + first-tranche kill
  point scheduled.
Reversible substitute: Time-boxed exploration tranche with pre-committed continue/kill
  criteria at its end.
Decision gate: Human promotion with the full packet; no direction commitment on agent
  consensus alone.
Verdict: PROCEED as tranche with kill point; BLOCK open-ended commitment.
```

```text
Commitment: Research-program framing.
What it locks: The lab's language, identity, and evaluation criteria — a program
  framing decides what counts as progress for years; unwinding one costs identity, not
  just time (narrative lock at maximum scale).
Reputation risk: High — programs are announced identities.
Compute risk: High cumulative — programs direct all future runs.
Evidence risk: High — degenerating programs absorb refutations as "patches needed."
Narrative risk: Maximal and structural — a program IS a narrative with a hard core.
Delay cost: Low — the working-thesis substitute captures all coordination value.
Minimum evidence before commitment: File 01's research-program standard: ≥2 independent
  confirmed results + ≥1 tested generative prediction + survived external review.
Reversible substitute: "Working thesis" entry in the decision-state object — revisable,
  unannounced, but explicit enough to be falsified.
Decision gate: Human-only promotion; the two-results gate is checkable, so check it.
Verdict: DELAY until the gate is met; RESCOPE to working thesis meanwhile.
```

---

## Closing artifacts

```text
Commitment-risk checklist (before any commitment):
1. Which lock type is this? (narrative / benchmark / method / evidence / compute /
   reputation / product — per the audit document's table)
2. What is the reversible substitute, named concretely? (No substitute identified →
   the audit is incomplete, not the commitment approved.)
3. What is the minimum evidence gate, and is it met at the required grade?
4. What is the delay cost, stated as concretely as the commitment risk? ("momentum"
   and "excitement" are not delay costs; a deadline, a blocking user, a priority
   window are.)
5. Who signs? (Reputation-bearing and direction-setting commitments: human only.)
6. What is the pre-committed unwind condition if the commitment proves wrong?

Examples of premature commitment (from the corpus and its cases):
- Writing the paper story before the kill experiment (narrative lock — DELAY).
- Announcing the autonomous Research-OS before blind false-promotion calibration
  (reputation lock — the calibration suite's case 18: DELAY/BLOCK).
- Full-scale training before the corrupted-reasoning recovery falsifier (compute
  lock — the audit document's own example: BLOCK).
- Installing the skill layer before running the 10-case calibration (the state
  object's named next irreversible decision — DELAY).
- Accepting a generator's fluent self-critique as the promotion review (evidence
  contamination — BLOCK).

Examples of acceptable commitment:
- Falsifier-scoped implementation before any verdict — it IS the test apparatus.
- A claim registry with kill conditions written before results — reversible, and it
  sharpens the falsifier.
- Scoped internal shipping of a draft skill invoked manually per-session.
- A time-boxed direction tranche with a pre-committed kill point at its end.
- Publishing a negative result whose autopsy and conversion are complete — this
  commitment is cheap, honest, and banks the constraint publicly.
```

Tradeoff summary: the commitment machinery's known failure mode is symmetrical to its
purpose — an audit that can BLOCK anything will, over time, BLOCK everything, because
blocking is never locally punished (the audit document names this: "calling every
decision irreversible," "ignoring delay cost"). The structural fix is embedded above:
no DELAY or BLOCK verdict is complete without a concretely stated delay cost and a
named reversible substitute. An audit that cannot supply both is itself incomplete.
