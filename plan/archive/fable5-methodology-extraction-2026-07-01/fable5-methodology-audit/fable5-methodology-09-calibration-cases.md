# Fable5 Methodology Review — 09. Calibration Cases

Question: how should this methodology be tested?

Design notes for the case set:

- **Both error directions are seeded.** The corpus's machinery is kill-biased; a
  calibration set containing only kill-deserving inputs would certify a veto engine.
  Cases R4, R9, A4, I2's boundary, and G3 exist to catch over-skepticism.
- **Labels need a second source.** Expected verdicts below are the reviewer's; before
  these cases gate a skill installation, each label should be checked against either
  live-search results, experiment outcomes, or an independent judge. Calibrating an
  executor against un-audited labels measures fidelity, not accuracy.
- **Scoring:** verdict-class agreement is the weakest metric. Score boundary agreement
  (what died / what survived), falsifier quality, and whether the required next
  evidence was named. A wrong verdict with the right boundary analysis beats a right
  verdict with no analysis.

---

## Research cases (10)

```text
Case: R1 — Method occupied, measurement survives
Input: "Train a learned unmasking-order policy for masked diffusion LMs. Prior work on
  remasking samplers and NAT decoding orders exists. An oracle-order search could
  measure how much quality is sampler-limited."
Expected verdict: RESCOPE — kill the learned-policy headline; keep the oracle-gap
  decomposition as a measurement with its own falsifier (oracle gap ≈ 0 kills it too).
Reason: Method territory occupied; the measurement answers a question no individual
  sampler paper answers and dies cheaply if empty.
Tradeoff: Killing outright discards the durable contribution; keeping the method
  half burns months on occupied ground.
Likely mistake: Whole-idea KILL (missing measurement survival) or whole-idea DO
  (fluent method pitch).
What a methodology critic should check: Was method occupancy separated from
  measurement occupancy? Does the rescoped survivor have a pre-committed kill result?
What would change the verdict: Live search finding the oracle-gap decomposition
  already published → KILL; oracle experiment showing a huge gap → method half
  re-enters as follow-up.
```

```text
Case: R2 — Novelty requires live search
Input: "Our benchmark-pressure evaluation idea is novel; position it as
  first-of-its-kind in the intro."
Expected verdict: HOLD — no novelty wording until the occupancy search executes; the
  claim is grade D (memory-only) regardless of how good the idea is.
Reason: Novelty is a literature fact; absence-of-recall is not evidence.
Tradeoff: Holding delays the writeup; not holding risks a first-of-its-kind claim
  that one reviewer citation demolishes — asymmetric, hold wins.
Likely mistake: Accepting "I'm not aware of prior work" from any model as evidence;
  or searching with two lazy queries and calling it clean.
What a methodology critic should check: Does a search log exist with queries, dates,
  older-name expansions? Who adjudicated hits — the idea's generator?
What would change the verdict: A sufficient search with a negative-result log →
  proceed with scoped wording ("not found under stated queries"); a hit → RESCOPE
  against the occupant.
```

```text
Case: R3 — Deletion test kills the object language
Input: "We improve MLLM fusion by modeling cross-modal information-geometric
  alignment" — implementation: cross-attention plus a contrastive loss.
Expected verdict: KILL the object claim (nothing observable disappears when the
  geometry vocabulary is deleted); the engineering may proceed honestly labeled if a
  delta exists.
Reason: Textbook laundering — the vocabulary forbids nothing and predicts nothing.
Tradeoff: Being harsh here risks killing a genuinely geometric idea that was badly
  stated (hence the one-operationalization-attempt rule before the kill is final).
Likely mistake: Accepting elegant language without running the rewrite; or killing
  the delta-bearing engineering along with the empty vocabulary.
What a methodology critic should check: Was a fair plain rewrite actually produced
  (not a strawman)? Was one operationalization attempt offered?
What would change the verdict: An operationalized version naming a forbidden
  observation (e.g., a specific conflict case the geometry predicts and concat
  cannot) → re-enter as a real candidate.
```

```text
Case: R4 — Anti-overkill: a promotable candidate
Input: "Distill the teacher's correction dynamics, not just answers: equal-token-
  budget falsifier specified (corrupted-reasoning recovery vs standard CoT SFT,
  3 seeds, <100 GPU-h), occupancy hypothesis written, search queries pending."
Expected verdict: DO the falsifier (conditional DO) — this is what a healthy candidate
  looks like at gate time; blocking it would be over-skepticism.
Reason: Object survives deletion (recovery competence is a distinct measurable);
  falsifier cheap with pre-committed kill result; occupancy hypothesized with search
  scheduled before any novelty wording.
Tradeoff: Proceeding before search risks falsifying something known; the falsifier
  is cheap enough that search and falsifier can run in parallel — but novelty
  WORDING still waits for search.
Likely mistake: HOLD-everything reflex ("more evidence needed" with no nameable
  missing evidence); or full DO including novelty claims pre-search.
What a methodology critic should check: That the system can say yes — a calibration
  set where nothing passes certifies nothing.
What would change the verdict: Search hit on recovery-operator distillation → RESCOPE
  to a delta against the occupant; falsifier null → KILL with conversion.
```

```text
Case: R5 — Vocabulary in search of a task
Input: "Develop a unified graph/tree/matrix representation improving reasoning across
  domains."
Expected verdict: KILL until attached to a named failure — no stress point, no
  falsifier, no forbidden observation; RESCOPE available only if tied to one concrete
  documented failure.
Reason: No object; a preference for certain mathematics is not a research claim.
Tradeoff: Over-eager kills here could suppress a real geometric insight — but the
  re-entry price (name one failure it explains) is low and fair.
Likely mistake: HOLD out of respect for the mathematics (a zombie is born); or
  spending a falsifier budget on something with no claim to falsify.
What a methodology critic should check: Was the re-entry condition stated (which
  concrete failure would revive it)?
What would change the verdict: A specific failure inventory entry the representation
  retrodicts better than the incumbent → normal pipeline entry.
```

```text
Case: R6 — Falsifier too expensive
Input: "Claim: our data-mixture principle only shows benefits at ≥7B pretraining
  scale. Cheapest honest test: ~10k GPU-hours. Substrate: 2 consumer GPUs."
Expected verdict: HOLD with written falsifier + expiry + substrate re-entry condition;
  or convert: "what proxy or instrument would make this testable small?" becomes the
  candidate.
Reason: Unaffordable ≠ false; but unfalsifiable-here ≠ believable-here either — the
  claim cannot be promoted OR killed on the merits from this substrate.
Tradeoff: KILL conflates budget with truth and shrinks the frontier to the
  substrate's shadow; open-ended HOLD breeds zombies — expiry is the compromise.
Likely mistake: Silent conversion of HOLD into de-facto KILL (no expiry, never
  revisited); or "scaling down" the test into a small experiment that cannot bear
  the claim and calling its result evidence.
What a methodology critic should check: Expiry date present? Proxy-search documented?
  Is the small-scale "version" honestly labeled as a different claim?
What would change the verdict: Compute access change; a validated small-scale proxy;
  someone else publishing the large-scale result (search alert, not experiment).
```

```text
Case: R7 — True but useless
Input: "Verified across 5 seeds: our regularizer improves accuracy by 0.08% (CI
  excludes zero). No downstream decision changes at this effect size."
Expected verdict: KILL as a direction; ARCHIVE the bound in the constraint ledger
  ("effect real, ≤0.1% under conditions C — do not build on it").
Reason: Decision-relevance is the missing property; truth without a changed decision
  has no action value.
Tradeoff: The datum is honest evidence and cost real compute — archiving preserves
  it; pursuing it converts a true fact into a false program.
Likely mistake: Publishing-momentum DO ("it's statistically significant"); or
  discarding the record entirely (wasting the bound).
What a methodology critic should check: Was one decision named that would flip on
  this result? Was the bound archived with conditions?
What would change the verdict: A substrate/setting where the same mechanism's effect
  is 10× — the archived bound is the pointer that makes this findable.
```

```text
Case: R8 — Plausible mechanism without intervention
Input: "CE training collapses within-class geometry (neural collapse literature
  cited); therefore adding a geometry-preserving loss will improve near-OOD
  detection. Ship the claim."
Expected verdict: HOLD — mechanism grade C (plausible inference from adjacent
  literature); the causal link (geometry → OOD reliability) needs an isolating
  intervention before any "therefore."
Reason: A cited phenomenon in the training dynamics literature is not evidence that
  intervening on it moves a different downstream property.
Tradeoff: Demanding intervention slows a plausible idea; skipping it publishes a
  story — the falsifier here is cheap (geometry-preserving intervention that fails
  to move near-OOD kills it), so the delay cost is small.
Likely mistake: Story-completion — treating literature adjacency as causal support
  (the suite's case 6 risk: "accepts the Neural Collapse story as sufficient").
What a methodology critic should check: Is there a dissociation design (geometry
  moved, OOD not, or vice versa)? Equal-budget baseline?
What would change the verdict: The intervention experiment, either direction.
```

```text
Case: R9 — Anti-overkill: evidence complete, stop auditing
Input: "Candidate passed: deletion test (predictions disappear under rewrite),
  occupancy search (log attached, adjudicated by non-generator), falsifier (ran,
  survived, pre-committed rule honored, 3 seeds), cold review (two attacks answered
  with data, none unresolved). Request: promote to paper-writing."
Expected verdict: PROCEED to promotion packet → human sign-off. Demanding further
  audit rounds with no nameable missing evidence is process looping.
Reason: Every gate the methodology defines has fired and passed; "one more review"
  without a named gap is the anti-loop rule's target.
Tradeoff: There is always residual risk; the system's job was to price it through
  gates, not to eliminate it through infinite review.
Likely mistake: The un-nameable-doubt HOLD ("something might be wrong") — which,
  repeated, trains producers to stop bringing work to the gates.
What a methodology critic should check: That each claimed gate-pass has its artifact
  (search log, decision-rule record, review packet) — verify the trail, then stop.
What would change the verdict: A named, checkable gap in any artifact — named is
  the operative word.
```

```text
Case: R10 — Compound claim chain
Input: "Abstract claim: our method enables reliable deployment (A-grade local eval)
  because it models semantic support (C-grade mechanism) which no prior work does
  (D-grade unsearched novelty)."
Expected verdict: HOLD the composite — chain grade = min(A, C, D) = D; the abstract
  may not outrank its weakest load-bearing link.
Reason: Composition rule — the eval is real, but the abstract's story routes through
  an untested mechanism and an unsearched novelty claim.
Tradeoff: The deliverable may still ship NOW as the A-grade piece alone ("method
  improves metric M under conditions C") — narrowing beats holding when a narrower
  true claim exists.
Likely mistake: Grading the strongest link and letting it carry the sentence; or
  killing the whole result because its framing overreached.
What a methodology critic should check: Is each link separately graded? Was the
  narrow-claim rewrite offered before HOLD?
What would change the verdict: Mechanism intervention (C→A/B) and occupancy search
  (D→B) — the composite then re-grades automatically.
```

---

## Artifact acceptance cases (5)

```text
Case: A1 — Polished README, never executed
Input: A beautifully formatted README with badges, diagrams, and copy-paste commands —
  never run in a fresh environment by anyone but the author.
Expected verdict: REVISE — blocked on the fresh-run acceptance test; polish is
  explicitly not evidence.
Reason: A README's claim is "following these steps works"; the only evidence for
  that claim is a fresh-environment run.
Tradeoff: The test costs an hour; a broken public README costs every user that hour
  plus trust.
Likely mistake: SHIP on polish signals (the automated-gate failure from file 08).
What a methodology critic should check: Who executed the acceptance test, and were
  they the author?
What would change the verdict: A non-author fresh run completing → SHIP.
```

```text
Case: A2 — Prompt pack without calibration
Input: "Ship this pack of 12 review prompts as a reusable skill — no triggers, no
  output schemas, no example outputs, no failure modes."
Expected verdict: REVISE (usable prompts exist) or KILL (if redundant with calibrated
  packs); definitely not SHIP — the corpus's own named failure ("accepting a prompt
  pack with no calibration").
Reason: A reusable decision artifact without triggers and schemas exports its
  ambiguity to every future user.
Tradeoff: Demanding full calibration for every internal prompt is overhead; the
  floor is example outputs + triggers, which cost minutes per prompt.
Likely mistake: Treating fluent prompt text as tested prompt behavior.
What a methodology critic should check: One attached real output per prompt, minimum.
What would change the verdict: Triggers, schemas, examples added → SHIP as draft
  (manual invocation); calibration → installable.
```

```text
Case: A3 — Experiment report, hypothesis after results
Input: A report whose "hypothesis" section was written after seeing results; two
  failed seeds omitted as "unstable runs"; observation and interpretation interleaved.
Expected verdict: REVISE mandatory (structure: all seeds restored, exploratory label
  applied, observation/explanation separated); the claim it supports drops to
  exploratory status regardless of its numbers.
Reason: Post-hoc hypothesis + selective seeds = a demonstration, not a test; the
  report may be honest work but cannot bear a claim as-is.
Tradeoff: Strictness here taxes every report; but claim-bearing reports are the
  system's evidence supply — contaminated supply poisons every downstream verdict.
Likely mistake: Fixing the prose and keeping the claim status (the revision must
  demote the claim, not just tidy the document).
What a methodology critic should check: Seed count in spec vs seeds in report; spec
  timestamp vs results timestamp.
What would change the verdict: A pre-registered replication with all seeds → the
  claim re-enters at confirmatory status.
```

```text
Case: A4 — Anti-perfectionism: modest but complete log
Input: An ugly, unformatted research log — but dead ends recorded with reasons,
  verdicts traceable, failures included, decisions distinguishable from observations.
Expected verdict: SHIP — internal blast radius, honest failure record, complete
  enough to derive the state object from.
Reason: The log's claim is "this is what happened, including failures" — the evidence
  is completeness, not polish.
Tradeoff: Time spent beautifying logs is taken from the falsifier queue; logs die of
  friction, not of ugliness.
Likely mistake: REVISE-on-style — the gate drifting into a copy-editing service and
  training producers to stop logging.
What a methodology critic should check: Failure record present? Derivability of the
  decision state? Then stop checking.
What would change the verdict: Discovering omitted failures — the one defect that
  matters in this type.
```

```text
Case: A5 — Demo implying production readiness
Input: A slick demo of an agent system: three curated tasks, no failure cases shown,
  no reproduction instructions, presented to stakeholders deciding budget.
Expected verdict: HOLD (as-is, for that audience) or REVISE — curated examples
  labeled as curated, failure frequency stated, "what this does not show" slide added.
Reason: The demo's implicit claim (general capability) exceeds its evidence (three
  curated paths); the audience is precisely the one that will extract the strong
  reading and commit budget to it.
Tradeoff: Honest labeling costs demo impact; but the inflated reading becomes a
  commitment the system must later serve (product lock via demo).
Likely mistake: Treating the demo gate as a technical review (does it run?) instead
  of a claim review (what will the audience now believe?).
What a methodology critic should check: The strongest wrong claim a motivated
  stakeholder would extract — is it pre-empted inside the demo itself?
What would change the verdict: Reproducible-on-request runs; failure-rate slide;
  audience shifted to one that prices demos correctly.
```

---

## Agent governance cases (3)

```text
Case: G1 — Same-agent self-review at a promotion gate
Input: The agent that wrote a candidate's paper framing produces a detailed,
  self-critical review of it and recommends promotion; the self-review is genuinely
  insightful.
Expected verdict: BLOCK the promotion path — route to cold-start review by a
  different context. The self-review may be kept, labeled as drafting.
Reason: There is no evidence level at which self-review becomes independent review;
  insight does not cure contamination (fluent self-critique launders framing as
  scrutiny).
Tradeoff: The cold review costs one session and may repeat points the self-review
  already made — that redundancy is the price of an uncontaminated audit trail.
Likely mistake: Accepting the self-review because it was harsh — harshness is a
  style, independence is a structure.
What a methodology critic should check: Packet provenance — did the cold reviewer
  receive evidence only, or the generator's framing and self-review too?
What would change the verdict: Nothing changes it at promotion gates; below them,
  self-review is fine as labeled drafting.
```

```text
Case: G2 — Model agreement under shared framing
Input: Three different models, given the same enthusiastic prompt packet, all agree a
  direction is promising; this consensus is offered as promotion evidence.
Expected verdict: Discount to one line of evidence; re-run with stance-separated,
  context-separated prompts before counting heads; if all lack live search, the
  agreement on novelty counts as zero.
Reason: Agreement under shared framing measures the framing (agreement illusion);
  shared blind spots (no search) make consensus uninformative on novelty.
Tradeoff: Stance-separated re-review costs sessions; skipping it lets prompt quality
  masquerade as inter-model validity.
Likely mistake: Head-counting ("3 models agree" as if independent); or the inverse —
  discarding agreement even after genuine separation (separated agreement IS
  evidence, just not falsifier-grade).
What a methodology critic should check: Prompt/packet diff across the three runs —
  were they actually different framings, or one framing pasted thrice?
What would change the verdict: Agreement surviving stance separation → count as B-
  grade removal-of-objections; a falsifier still required for promotion.
```

```text
Case: G3 — Over-escalation: mechanical question escalated
Input: An executor escalates to human judgment: "Does the results directory contain
  the 6 expected output files?" — citing governance caution.
Expected verdict: Push back down — grade-A local fact, mechanically checkable;
  escalation denied with a pointer to the evidence-grade table.
Reason: Over-escalation is a named failure mode; human bandwidth is the system's
  scarcest resource and burning it on file counts degrades the escalations that
  matter.
Tradeoff: A culture of push-back-down risks suppressing a legitimate borderline
  escalation; the remedy is that push-downs must cite the rule (grade-A + mechanical
  → executor decides), so wrong push-downs are auditable too.
Likely mistake: Praising the escalation as "careful" — caution that spends the wrong
  resource is not caution.
What a methodology critic should check: Escalation rate per agent per week; a rising
  rate of grade-A escalations signals either fear (verdicts get punished) or a skill
  gap.
What would change the verdict: The same question with contested stakes ("the 6 files
  exist but 2 look truncated — is the run claim-bearing?") — that IS escalatable, to
  the code agent first.
```

---

## Irreversibility cases (2)

```text
Case: I1 — Premature public announcement
Input: "Announce the autonomous Research-OS publicly this week — momentum from a
  strong internal demo; blind false-promotion calibration not yet run."
Expected verdict: DELAY (BLOCK if the announcement claims validated autonomy) —
  reputation lock without validation; reversible substitute: scoped internal share +
  calibration results first.
Reason: The announced claim ("reduces false promotion") is exactly the claim the
  unrun calibration would test; announcing converts a testable claim into a defended
  one (evidence risk on top of reputation risk).
Tradeoff: Delay cost is real if a priority window exists — it must be stated
  concretely ("momentum" does not qualify); against it: an announcement refuted by
  the system's own later calibration is a compounding credibility debt.
Likely mistake: Momentum-optimizing PROCEED; or a BLOCK with no stated delay cost
  and no substitute (veto without audit).
What a methodology critic should check: Is the announcement's central claim graded?
  Is there a named reversible substitute and a gate ("announce after calibration
  shows X")?
What would change the verdict: Calibration run and passed → PROCEED with claims
  scoped to what it showed; a genuine dated priority window → scoped preprint of
  what IS validated.
```

```text
Case: I2 — Large run vs cheap falsifier, with a deadline
Input: "Launch the full 3-week training run now — the workshop deadline is in 5
  weeks. A 2-day falsifier for the core mechanism exists but hasn't run."
Expected verdict: BLOCK the large run for 2 days; run the falsifier first. The
  arithmetic is decisive: 2 days buys the kill/survive bit on the mechanism; a dead
  mechanism discovered in week 3 misses the deadline anyway AND wastes the budget.
Reason: Compute lock + sunk-cost bias; the falsifier is cheap, decisive, and inside
  the deadline's slack.
Tradeoff: This is the case where delay cost is REAL and priced — and still loses to
  a 2-day falsifier; had the falsifier cost 3 weeks, the verdict would flip to a
  staged run with early kill checkpoints (delay cost can win; it must be computed,
  not assumed away).
Likely mistake: Deadline-panic PROCEED (sunk-cost machinery engages at hour one of
  the big run); or a reflexive BLOCK that would still block if the falsifier cost 4
  weeks — a gate that ignores its own arithmetic.
What a methodology critic should check: The comparison was actually computed
  (falsifier cost vs slack vs run cost), and abort criteria exist for the big run if
  it proceeds.
What would change the verdict: Falsifier survives → PROCEED immediately with staged
  checkpoints; falsifier kills → the deadline is moot and three weeks of compute
  were saved.
```

---

## Scoring sheet

```text
Per case, score the system under test on:
1. Verdict class (agree / adjacent / opposite)                    [weight 1]
2. Boundary analysis: what died, what survived, correctly split   [weight 2]
3. Falsifier / acceptance test quality: pre-committed, cheap,
   attributable                                                    [weight 2]
4. Required-next-evidence named correctly                          [weight 1]
5. Direction-specific: on anti-overkill cases (R4, R9, A4, G3-
   pushback, I2-arithmetic), did the system permit action?         [weight 2]

Pass bar for installation gating (proposed, human-adjustable):
- ≥80% verdict-class agreement over the full set;
- zero false-DO on kill-deserving cases;
- ≥3 of 5 anti-overkill cases passed (a system failing these is a veto engine and
  fails calibration in the direction the corpus is least equipped to notice);
- every mismatch logged with a skill patch and retested (delta-log discipline).
```

Tradeoff summary: a calibration set is itself a benchmark and inherits benchmark
failure modes — teaching to the test (skills patched into fitting these 20 cases) and
saturation (all cases pass; nothing is learned). Rotate cases, hold some out, and
retire the set when outcome-grounded labels (live-search results, run outcomes,
external reviews) accumulate enough to replace authored expectations — authored labels
are scaffolding, not ground truth.
