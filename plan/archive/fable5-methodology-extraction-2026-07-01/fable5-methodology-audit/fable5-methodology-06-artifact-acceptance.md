# Fable5 Methodology Review — 06. Artifact Acceptance

Question: how should the system decide whether an artifact is ready to use?

Two amendments to `artifact-acceptance-review.md` applied throughout:

1. **Blast-radius scaling.** The gate's strictness scales with distribution: private
   note < team-internal < cross-team < public. The corpus applies one gate to all; that
   over-polices internal artifacts and under-polices public ones.
2. **Artifact ≠ claim.** An artifact can be SHIP while its central claim is HOLD — if
   and only if the artifact states the claim's status honestly. Conflating the two
   gates causes both failure modes: shipped overclaims and blocked honest reports.

---

```text
Artifact type: Paper draft
Primary user: Reviewers, then the field; secondarily the lab's future self.
Claim it makes: The stated contribution (method/measurement/benchmark/taxonomy) at a
  stated evidence level.
Minimum evidence: Falsifier run and survived; occupancy search log attached; claim
  narrower than evidence (not equal to — narrower); baselines at equal budget.
Acceptance tests: Contribution type explicit in one sentence? Every "because" backed by
  an intervention? Reviewer-attack pass done cold? Limitations section survives the
  hostile reader? The falsifier acknowledged in-text?
Hostile-reader misunderstanding: Reading a measurement paper as a weak method paper;
  reading scoped claims as general ones ("improves distillation" vs "improves
  corrupted-state recovery at equal token budget on GSM8K-class tasks").
What must be explicit: Contribution type; evidence scope; what was NOT tested; compute
  substrate; the do-not-claim boundary in the authors' own words.
What must be cut: Object vocabulary that fails the deletion test; any claim whose grade
  is below the abstract's implied grade (chain rule).
Tradeoff between speed and rigor: Submission deadlines are real; the honest compromise
  is cutting claims to match evidence rather than delaying to match claims.
Verdict boundary: SHIP (submit) when claims ≤ evidence and cold review passed; REVISE
  when overclaim is fixable by narrowing; HOLD when the central falsifier hasn't
  returned; KILL when the contribution fails the deletion test at the core.
```

```text
Artifact type: Experiment report
Primary user: The claim owner and future agents resuming from state.
Claim it makes: "This run happened as specified and produced these outcomes."
Minimum evidence: Pre-registered spec attached; all seeds reported; artifacts
  preserved; integrity check (intervention fired; data consumed; exit clean).
Acceptance tests: Hypothesis stated before results? Baselines at equal budget? Failure
  cases and negative seeds included? Observation separated from explanation (two
  sections, not interleaved)? Could a cold agent re-run from this report alone?
Hostile-reader misunderstanding: Reading an exploratory run as a confirmatory one —
  the report must carry its own label (exploratory | claim-bearing).
What must be explicit: Deviations from spec (any); seeds; the decision rule and whether
  it fired; what this run cannot distinguish (confounds).
What must be cut: Interpretive narrative in the results section; retroactive hypothesis
  language ("as expected" on unexpected results).
Tradeoff between speed and rigor: Full reports for every exploratory run would halt
  exploration; the compromise: lightweight logs for exploratory runs, full reports
  reserved for claim-bearing runs — but the label is mandatory on both.
Verdict boundary: SHIP when integrity-checked and complete; REVISE for missing
  structure; HOLD when integrity cannot be verified (a plausible number from an
  unverifiable run is worth nothing); KILL never — even failed runs get reports (the
  conversion law needs them).
```

```text
Artifact type: README
Primary user: A new user with zero conversation context.
Claim it makes: "Following these steps produces the stated result."
Minimum evidence: One fresh-environment execution by a non-author (or cold agent) —
  this is non-negotiable; a README that has never been followed is a hypothesis.
Acceptance tests: Prerequisites listed and versioned? Commands copy-paste runnable?
  Expected output shown? Failure symptoms and fixes for the two most likely breaks?
  Known limitations stated?
Hostile-reader misunderstanding: Assuming maintained support; assuming the happy path
  covers their environment.
What must be explicit: Tested environments; what is NOT supported; time/resource cost
  of the setup.
What must be cut: Aspirational sections ("coming soon"); options that were never tested.
Tradeoff between speed and rigor: The fresh-run test costs an hour and is the entire
  difference between documentation and fiction; there is no legitimate speed case for
  skipping it on anything another person will run.
Verdict boundary: SHIP after fresh-run passes; REVISE on any fresh-run friction; HOLD
  if the underlying tool is still changing daily (README churn is worse than README
  absence); KILL if redundant with an existing doc it contradicts.
```

```text
Artifact type: Architecture document
Primary user: Implementers and future maintainers deciding where changes go.
Claim it makes: "The system is structured this way, for these reasons, under these
  constraints."
Minimum evidence: Conformance spot-check against the actual code/system (an
  architecture doc describing an intended-but-unbuilt structure must say so); the
  load-bearing constraints listed with their consequences.
Acceptance tests: Can an implementer locate where a new feature goes? Are the
  rejected alternatives recorded with reasons (else they will be re-proposed)? Are
  invariants distinguished from preferences? Is there a dated "as of" stamp?
Hostile-reader misunderstanding: Treating described structure as enforced structure;
  treating preferences as invariants.
What must be explicit: What breaks if each invariant is violated; which parts are
  aspirational; the update trigger (when must this doc be revised).
What must be cut: Diagrams that duplicate code without adding constraint information;
  motivational prose about the architecture's elegance.
Tradeoff between speed and rigor: Architecture docs rot faster than any other type;
  a smaller doc with an update trigger beats a complete doc without one.
Verdict boundary: SHIP with conformance check + date stamp; REVISE when described and
  actual structure diverge; HOLD during active restructuring; KILL when the code has
  moved so far the doc misleads.
```

```text
Artifact type: Demo
Primary user: A stakeholder deciding whether to invest attention, budget, or trust.
Claim it makes: Implicitly, always more than intended — a demo IS a claim-inflation
  device; the gate exists to bound it.
Minimum evidence: The demo path reproducible by a non-author; edge-case behavior known
  (not necessarily good — known); an explicit statement of what the demo does NOT show.
Acceptance tests: Does the demo prove the claim or only a happy path? Is the setup
  reproducible? Would the stakeholder's likely generalization ("so it works") be true?
  Is production-readiness explicitly disclaimed where absent?
Hostile-reader misunderstanding: Demo-to-deployment inflation — the single most
  reliable misreading in the genre; assume it will happen and pre-empt it in the demo
  itself, not in a caveat document nobody reads.
What must be explicit: Cherry-picking, if any (curated examples labeled as curated);
  latency/cost hidden by the demo setup; failure frequency.
What must be cut: Any capability shown that cannot be reproduced on request.
Tradeoff between speed and rigor: Demos have real timing value (funding, alignment);
  the compromise is honest curation — show the best case, label it as the best case.
Verdict boundary: SHIP with explicit non-claims; REVISE when the implicit claim
  overruns evidence; HOLD when a live audience would extract a capability claim the
  system cannot support on request; KILL when the demo only works with intervention.
```

```text
Artifact type: Benchmark
Primary user: Other researchers (including adversarially-motivated ones) ranking
  methods.
Claim it makes: "Score differences on this instrument track real capability
  differences" — the strongest claim any artifact in this list makes.
Minimum evidence: Discrimination evidence (known-better vs known-worse systems
  separate); pressure behavior characterized (what happens under targeted
  optimization); contamination surface documented; baseline spread reported.
Acceptance tests: Do trivial baselines score low? Does the metric survive its own
  paper's optimization attempts? Is the scoring code deterministic and public? Are
  saturation and gaming modes discussed with predicted symptoms?
Hostile-reader misunderstanding: Treating the benchmark as measuring the general
  capability named in its title rather than the specific instrumented behavior.
What must be explicit: What the benchmark cannot measure; expected lifetime (when
  should the community distrust it); the update/retirement policy.
What must be cut: Capability language in the title/abstract beyond what discrimination
  evidence supports.
Tradeoff between speed and rigor: A benchmark shipped fast and gamed early poisons the
  field's evidence supply — this artifact type justifies the slowest gate in the list;
  blast radius is maximal because others build on it.
Verdict boundary: SHIP only with discrimination + pressure evidence; REVISE for
  documentation gaps; HOLD without pressure characterization; KILL if the paper's own
  method is the only thing that scores well (self-licking instrument).
```

```text
Artifact type: Skill (installed agent procedure)
Primary user: Future agent sessions — which is what makes it dangerous: the user
  cannot push back.
Claim it makes: "Executing this procedure produces better decisions than not executing
  it."
Minimum evidence: Blind calibration against a stated threshold (file 04's installed-
  skill gate); trigger precision checked (does it fire when it should and NOT when it
  shouldn't); every failure mode listed with a detection sign.
Acceptance tests: Trigger + inputs + output schema + kill/escalation conditions all
  present (the corpus's own skill checks)? Calibration delta log exists and its
  patches retested? Does the skill prevent its own most likely misuse?
Hostile-reader misunderstanding: An agent applying the skill outside its trigger
  envelope because the description was broad ("use for research decisions").
What must be explicit: Non-triggers (when NOT to fire); the escalation path; the
  skill's own failure modes.
What must be cut: Motivational framing; any step without a decision consequence.
Tradeoff between speed and rigor: Draft skills invoked manually cost nothing to use
  and nothing to retract; installation converts a tool into standing behavior — the
  rigor gate belongs at installation, not drafting. Draft freely; install slowly.
Verdict boundary: SHIP (install) only post-calibration; REVISE for missing schema
  elements; HOLD pre-calibration (the corpus's current, correct state); KILL when the
  skill's decisions never diverge from no-skill behavior (dead gate test).
```

```text
Artifact type: Prompt pack
Primary user: Operators (human or agent) invoking prompts they did not write.
Claim it makes: "These prompts elicit the intended behavior reliably."
Minimum evidence: Each prompt run at least once with output attached (a prompt pack
  with no example outputs is untested by definition); variance noted where high.
Acceptance tests: Does each prompt state its trigger and required inputs? Are expected
  outputs shown? Is there at least one known-bad usage example? Calibration exists for
  packs feeding decisions (the corpus's named failure: "accepting a prompt pack with
  no calibration")?
Hostile-reader misunderstanding: Treating prompts as deterministic APIs; ignoring
  model-version sensitivity.
What must be explicit: Model/version assumptions; sensitivity warnings; what to do
  with malformed output.
What must be cut: Redundant near-duplicate prompts (each additional variant dilutes
  maintenance); prompts never actually run.
Tradeoff between speed and rigor: Prompt packs are cheap to write and expensive to
  debug downstream; one attached example output per prompt is the minimum honest test
  and costs minutes.
Verdict boundary: SHIP with examples + triggers; REVISE missing either; HOLD if the
  underlying model is about to change; KILL for untested packs presented as tested.
```

```text
Artifact type: Frontend page
Primary user: End users with zero context and no tolerance for explanation.
Claim it makes: "The primary workflow is completable, and displayed information is
  true."
Minimum evidence: The primary workflow completed by a non-author without explanatory
  text (the design minimum decision test from the transfer document); displayed claims
  (numbers, statuses) traced to sources.
Acceptance tests: Core job completable unaided? Error and empty states present?
  Displayed data live-or-labeled (mock data marked as mock)? Accessibility pass at the
  level the audience requires?
Hostile-reader misunderstanding: Users believing displayed numbers are live/current
  when they are cached or mocked — a truthfulness failure, not a design failure.
What must be explicit: Data freshness; what is clickable vs decorative; supported
  browsers/devices if constrained.
What must be cut: Placeholder content that could be mistaken for real data; controls
  that do nothing.
Tradeoff between speed and rigor: Visual polish is the cheapest thing to add and the
  most misleading signal of readiness (polish-as-readiness applies doubly here);
  spend the gate on the workflow test, not the pixel review.
Verdict boundary: SHIP when the unaided-completion test passes and data is honest;
  REVISE for workflow friction; HOLD for mocked data unmarked; KILL for pages whose
  claim (the displayed information) is unsupported.
```

```text
Artifact type: Research log
Primary user: The future self and agents resuming from state; occasionally auditors.
Claim it makes: "This is what actually happened, in order, including failures."
Minimum evidence: Completeness of the failure record — a log containing only successes
  is not a log, it is marketing to oneself; timestamps; enough detail to reconstruct
  decisions.
Acceptance tests: Are dead ends recorded with reasons? Can the verdict trail be
  reconstructed? Are decisions distinguishable from observations? Would the
  context-compression state object be derivable from this log alone?
Hostile-reader misunderstanding: Treating logged hypotheses as logged conclusions —
  the log must mark epistemic status inline.
What must be explicit: What was NOT tried and why; verdict changes with triggers.
What must be cut: Nothing retroactively — logs are append-only; editing a research log
  is evidence tampering against oneself.
Tradeoff between speed and rigor: Logging tax is real and continuous; the compromise
  is structural: log verdict changes, kills, and anomalies always; log routine
  progress sparsely. A log optimized for completeness dies of friction.
Verdict boundary: SHIP by default (internal, low blast radius, honesty > polish);
  REVISE only for missing failure records; HOLD never; KILL never — an imperfect log
  beats no log unconditionally.
```

---

## Universal acceptance checklist

```text
For any artifact, in order:
1. Target user named? (No user → not an artifact; it's a note.)
2. Primary claim stated in one sentence?
3. Claim's evidence grade ≥ the grade the artifact's tone implies? (Chain rule: an
   artifact cannot sound more certain than its weakest load-bearing claim.)
4. One acceptance test EXECUTED by a non-author (scaled to blast radius:
   cold-agent check for internal, human non-author for public)?
5. Hostile-reader pass done — what is the strongest wrong claim a motivated reader
   could extract, and does the artifact pre-empt it?
6. Limitations and non-claims explicit IN the artifact (not in a side channel)?
7. Cut list applied — everything that fails the deletion test or exceeds evidence?
8. Verdict assigned from the artifact's own boundary table (SHIP/REVISE/HOLD/KILL),
   with required changes enumerated for REVISE.
9. Blast radius recorded — who can this artifact mislead, at what cost?
10. For SHIP: is the claim's own verdict (DO/HOLD/etc.) honestly stated inside the
    artifact? (SHIP-with-HOLD-claim is legal only with the label visible.)
```

Tradeoff summary: acceptance review is the last gate before an artifact starts
producing consequences the system no longer controls. Its cost structure is favorable —
review is cheap relative to retraction — but only if the gate discriminates: a gate
that REVISEs everything trains producers to route around it. The dead-gate test applies
here too: an acceptance gate that has never returned SHIP unchanged is miscalibrated in
one direction; one that never returns KILL is miscalibrated in the other.
