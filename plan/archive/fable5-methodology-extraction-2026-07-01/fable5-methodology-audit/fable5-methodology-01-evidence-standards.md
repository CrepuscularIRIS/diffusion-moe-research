# Fable5 Methodology Review — 01. Evidence Standards

Question: how should the research system decide what is worth believing?

Grading base: the A–E scale from `epistemic-calibration.md`, plus two amendments the
corpus lacks:

- **Composition rule.** A conclusion inherits the *lowest* grade in its dependency
  chain. A claim built from B×C×D links is a D claim wearing a B abstract.
- **Independence rule.** Two B-grade lines of evidence upgrade a decision only if their
  independence is verified (different method, different source, different framing).
  Two models agreeing under shared prompt framing is one line of evidence, not two.

---

## Claim-type standards

```text
Claim type: Novelty claim ("this object / method / measurement is new")
Minimum evidence: Executed live-search occupancy map — queries listed, venues covered,
  older names expanded, hits adjudicated; plus a deletion test showing the claim is not
  a renamed occupant.
Acceptable uncertainty: Differently-named prior art may still exist; the claim is
  scoped: "not found under queries Q1..Qn as of date D."
Unacceptable uncertainty: Absence-of-recall treated as absence-of-prior-art; searches
  designed to miss (narrow vocabulary, no adjacent literatures).
Need live search: yes — always, no exception.
Need experiment: no (novelty is a literature fact, not an empirical one).
Need human judgment: depends — required for the public wording of any novelty claim.
False confidence pattern: "I am not aware of prior work" from model memory; one query
  returning nothing treated as a clean map.
Conservative error: Killing on superficially similar prior art that models a different
  object (vocabulary collision ≠ occupancy).
Overly skeptical error: Infinite search — refusing every claim because some prior art
  might exist somewhere; the negative-result standard exists to terminate search.
What would change the verdict: A search hit occupying the object AND its falsifier →
  KILL or RESCOPE; a clean targeted search → upgrade wording to "underexplored under
  stated queries."
Do-not-claim boundary: Never "first" or "novel" without an attached search log. Allowed:
  "we did not find X under the following queries."
```

```text
Claim type: Causal mechanism claim ("X improves Y because Z")
Minimum evidence: A controlled intervention with an equal-budget baseline, ≥3 seeds, a
  manipulation check (the intervention demonstrably fired), and at least one predicted
  dissociation that rival explanations do not predict.
Acceptable uncertainty: Scope — the mechanism is demonstrated on the testbed, not
  everywhere; generalization stays a hypothesis.
Unacceptable uncertainty: Correlation or narrative plausibility standing in for
  mechanism; single-seed effects; interventions never verified to have fired.
Need live search: depends — yes if the mechanism may already be established or refuted.
Need experiment: yes — always. A mechanism claim without an intervention is grade C at
  best and cannot be promoted.
Need human judgment: no for the verdict; yes if the claim will anchor a program.
False confidence pattern: The "plausible story" pattern (e.g., accepting a
  neural-collapse narrative as sufficient evidence — calibration case 6): mechanism
  language over correlational evidence.
Conservative error: Demanding full causal identification for engineering claims that
  only need "reliably reproduces under stated conditions."
Overly skeptical error: Rejecting a mechanism because confounds are conceivable even
  after they were tested and excluded.
What would change the verdict: The dissociation experiment (positive → promote;
  null → the mechanism is fiction even if the trick helps).
Do-not-claim boundary: No "because" in an abstract without intervention evidence;
  say "consistent with" for correlational support.
```

```text
Claim type: Benchmark validity claim ("benchmark B measures capability X")
Minimum evidence: Behavior under optimization pressure (does score inflation transfer
  to held-out probes?) or validation against ground truth external to the benchmark;
  a contamination check.
Acceptable uncertainty: Validity scoped to a model class, pressure type, and time
  window.
Unacceptable uncertainty: Validity by popularity ("everyone uses it"), by construction
  ("we designed it to measure X"), or by leaderboard adoption.
Need live search: yes — known contamination reports and existing critiques must be
  surfaced first.
Need experiment: yes — a pressure test or external-ground-truth comparison.
Need human judgment: depends — yes when the benchmark will anchor a claim in a public
  artifact.
False confidence pattern: Treating aggregate accuracy movement as capability movement;
  treating a benchmark the paper itself introduces as self-validating.
Conservative error: Declaring all benchmarks invalid — leaves nothing measurable and
  stalls every downstream verdict.
Overly skeptical error: Same as conservative error, plus demanding pressure tests for
  low-stakes internal diagnostics.
What would change the verdict: Elasticity evidence — score gains that do (or do not)
  transfer under controlled pressure.
Do-not-claim boundary: Never "measures X" without probe evidence; allowed: "correlates
  with X under stated conditions, unpressured."
```

```text
Claim type: Artifact readiness claim ("this is ready to ship/use")
Minimum evidence: Acceptance tests executed by someone (or a cold-context agent) other
  than the author; hostile-reader check passed; limitations explicit.
Acceptable uncertainty: Unknown edge cases outside the stated scope.
Unacceptable uncertainty: "Looks complete"; polish standing in for a fresh-environment
  run; author-only review.
Need live search: no.
Need experiment: depends — for runnable artifacts (README, demo, skill), the
  fresh-environment execution IS the experiment and is mandatory.
Need human judgment: depends on blast radius — internal log no; public benchmark yes.
False confidence pattern: Polish-as-readiness; length-as-completeness (both named in
  artifact-acceptance-review.md).
Conservative error: Endless revision of internal artifacts nobody external will read.
Overly skeptical error: Blocking a modest-but-complete artifact because it is not
  beautiful.
What would change the verdict: An acceptance test failing; a hostile reader deriving a
  stronger claim than the evidence supports.
Do-not-claim boundary: No SHIP without a named target user and at least one executed
  acceptance test.
```

```text
Claim type: Product or deployment claim ("users can / will do X with this")
Minimum evidence: Target-user behavior — e.g., N users completing the core job without
  narrative assistance (the transfer document's 5-user test) — or deployment logs. An
  internal demo is not evidence of deployment value.
Acceptable uncertainty: Segment scope; long-term retention unknown.
Unacceptable uncertainty: Happy-path demo generalized to production; team members as
  proxy users.
Need live search: yes — competitor/precedent map before any whitespace claim.
Need experiment: yes — the user test is the experiment.
Need human judgment: yes — deployment claims create external commitments.
False confidence pattern: Demo-to-deployment inflation; "it worked when we showed it."
Conservative error: Requiring production-scale evidence before any user contact.
Overly skeptical error: Discounting consistent qualitative user evidence because it is
  not a randomized trial.
What would change the verdict: Users failing the core job unaided; a buyer unable to
  name what they would stop using (the business minimum decision test).
Do-not-claim boundary: No user-value claims from internal demos alone.
```

```text
Claim type: Model capability claim ("model M can do X")
Minimum evidence: Held-out evaluation with stated prompts, seeds, and decoding
  parameters; a contamination check; comparison against the strongest dumb baseline.
Acceptable uncertainty: Capability under stated conditions only; prompt sensitivity
  reported, not hidden.
Unacceptable uncertainty: Anecdote-based capability ("it did it once"); cross-scale
  extrapolation; capability inferred from model agreement.
Need live search: depends — yes when the claim concerns current external models
  (versions and behavior change under the system's feet).
Need experiment: yes.
Need human judgment: no for internal use; yes before public statement.
False confidence pattern: Single-prompt successes; two models agreeing under shared
  framing (agreement illusion, agent-governance.md).
Conservative error: Demanding exhaustive evals for internal routing decisions.
Overly skeptical error: Treating all capability claims as unknowable because prompts
  vary — the standard is stated-conditions, not universality.
What would change the verdict: A protocol-specified eval; a contamination finding.
Do-not-claim boundary: No "can X" without an evaluation protocol attached.
```

```text
Claim type: Strategic direction claim ("this direction deserves the next N months")
Minimum evidence: A concrete stress point (not topic heat); an occupancy hypothesis;
  substrate fit demonstrated; a scheduled minimum falsifier as the first milestone.
  Grade realistically caps at B — direction claims are forecasts.
Acceptable uncertainty: The direction may die at its first falsifier; that is the
  design, not a defect.
Unacceptable uncertainty: Direction chosen on narrative fluency, topic popularity, or
  sunk context; no falsifier scheduled inside the first budget tranche.
Need live search: yes — occupancy before commitment.
Need experiment: depends — the first falsifier is part of the commitment structure, not
  a precondition of considering it.
Need human judgment: yes — mandatory; direction changes are human decisions in this
  corpus's own governance rules.
False confidence pattern: Eloquent future-narrative standing in for evidence; "the
  field is moving here" (heat = occupancy, not opportunity).
Conservative error: Only pursuing safe increments; a portfolio of sure things is a
  guaranteed-mediocrity strategy.
Overly skeptical error: Demanding experimental proof before any direction is explored —
  directions are bets structured around early kill points, not conclusions.
What would change the verdict: First falsifier result; occupancy search hit; substrate
  change.
Do-not-claim boundary: No multi-month commitment without a first-tranche kill point.
```

```text
Claim type: Research-program claim ("these results constitute a program")
Minimum evidence: ≥2 independently confirmed results under the same hard core; at least
  one *new* prediction generated by the core and then tested (positive heuristic in
  action); survival of at least one external, non-self review.
Acceptable uncertainty: The program's outer boundary; which extensions will pan out.
Unacceptable uncertainty: Program-by-vocabulary — retrofitting a unifying story over
  scattered results after the fact.
Need live search: yes — a program claim is also a large novelty claim.
Need experiment: yes — the generative prediction must have been tested, not just stated.
Need human judgment: yes — program framing locks identity and language (irreversible-
  decision-audit: narrative lock at maximum scale); promotion is human-only.
False confidence pattern: One strong paper plus eloquence presented as a program.
Conservative error: Never claiming a program, so results stay unorganized and the
  positive heuristic is never articulated or tested.
Overly skeptical error: Same, plus dismantling a productive framing because one
  peripheral prediction failed (Lakatos: peripheral failure ≠ core refutation).
What would change the verdict: A second confirmed result; a core prediction failing
  repeatedly with patches accumulating (degeneration signal).
Do-not-claim boundary: No program status from a single result; use "working thesis" in
  the state object instead.
```

---

## Closing artifacts

```text
Mechanical checklist (run in order; stop at first failure):
1. Claim written in one sentence?                       If not → not a claim yet.
2. Claim type identified?                               If not → classify first.
3. Evidence listed and graded A–E?                      If not → grade before arguing.
4. Chain rule applied (grade = min of links)?           If not → re-grade.
5. Independence of multiple evidence lines verified?    If not → count as one line.
6. Live search done where required by type?             If not → HOLD.
7. Experiment done where required by type?              If not → HOLD (or schedule falsifier).
8. Do-not-claim boundary written?                       If not → the claim is unbounded; HOLD.
9. "What would change the verdict" written?             If not → the claim is unfalsifiable; KILL after one clarification attempt.

Escalation rule:
Escalate to human when (any): grade is E; the claim enters a public artifact; the claim
commits reputation, external users, or >48 GPU-hours; models disagree after
stance-separated review. Escalate to the reference judge (not human) when: the verdict
is contested but internal, or object invention is required. Do NOT escalate: claims an
executor can resolve mechanically (local facts, grade-A checks) — over-escalation is a
named failure mode, not a virtue.

Evidence-grade table (amended):
| Grade | Meaning | Allowed action | Amendment |
| A | Direct primary evidence / verified local artifact / executed experiment | Decide under stated scope | Requires integrity check: the run actually ran and fired |
| B | Strong secondary or multiple *independent* consistent signals | Propose with marked uncertainty | Independence must be argued, not assumed |
| C | Plausible inference from partial evidence | HOLD; schedule search/test | Default state of most new ideas — not an insult |
| D | Memory, analogy, taste | Cannot promote | One clarification attempt, then KILL |
| E | Unknown, contested, or high-stakes | Escalate or refuse | Never silently downgraded to C by rewording |
| Chain | Composite claim | Grade = min(link grades) | An abstract cannot outrank its weakest premise |

Examples that must HOLD:
- Any novelty claim before its live search executes (calibration case 13).
- "Correction dynamics improve distillation because they preserve recovery operators" —
  C until the corrupted-reasoning recovery falsifier runs.
- Installing the skill layer before blind calibration (the corpus's own pending
  falsifier and next irreversible decision).
- A benchmark-validity claim supported only by the benchmark's own scores.
- A strategic pivot argued from a persuasive state-of-the-field narrative with no
  occupancy search.

Examples that can proceed:
- "The markdown file contains no Chinese characters" — grade A by local check; executor
  decides, no escalation.
- Designing (not running) a minimum falsifier for a C-grade claim — costless, reversible,
  always allowed.
- A reversible internal draft (claim registry, not narrative) written before results.
- SHIP for an internal research log that is complete, has a named user, and states its
  scope — modest artifacts with honest limits pass.
- A RESCOPE verdict issued on D-grade method claims where the measurement survivor has
  its own falsifier — rescoping is itself a low-commitment act.
```

Tradeoff summary for this file: every evidence standard trades decision latency for
error rate. The corpus is tuned to minimize false promotion; the standards above
therefore embed a known cost — systematic delay on true-but-early claims. That cost is
acceptable only because HOLD is cheap *if* HOLD verdicts carry expiry and re-entry
conditions. Without a verdict ledger (missing document type #2), HOLD silently becomes
KILL-by-neglect, and the system's real error profile is harsher than its stated one.
