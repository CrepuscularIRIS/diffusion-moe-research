# Pipeline Devil's-Advocate Audit — 2026-07-13

> Commissioned via /systematic-debugging. Question: why does the pipeline not reliably converge on
> research topics worth pursuing, and is the failure-case treatment fundamentally flawed?
> Method: Phase-1 root-cause investigation BEFORE fixes — (1) full read of the 12 research-os skills
> + 3 conductor references (~1,796 lines) + project layer (~600 lines); (2) subagent audit of the
> empirical track record (4 campaigns, 6 dead slices, ledger-archive J1–J12, lessons L1–L8);
> (3) subagent audit of the banks + MoA/external-brain/Arbor integration; (4) review of
> plan/Audit/Step/{GPT1,GPT2,Devil}.md.

---

## 1. ROOT CAUSE (the Phase-1 verdict)

**The failure is architectural, not a wording problem and not primarily a model-capability problem.**

**~85% of the instruction mass and 100% of the BINDING gates sit on the problem-SOLVING side of the
loop (prereg / exp-verify / adversary / autopsy). Problem SELECTION has procedures but no binding
gates, no grounded external input at admission time, and its generative feedstock is the pipeline's
own failure residue — which, on strong incumbent substrates, is systematically marginal.**

Empirical support (subagent audit of the record, file citations therein):

- **~70% of sunk cost (~10–12 of ~15 GPU-days across aerial-VLN, optical-SAR, WM J1/J6/J8/J9/J11-12)
  went to topics a stronger selection-time gate would have rejected or heavily down-priced.**
  - Aerial-VLN: invented on an SR-7 self-built base while known SOTA was 28.3 — no
    reproduce-SOTA-first gate (`openbuild/aerial/LESSONS.md` §"never reproduced SOTA"). ~6–7 GPU-days.
  - J1 adaptive-horizon: occupancy 精读 found it SATURATED — but *after* it had been the
    plan-of-record "main design" for a day. Selection preceded the occupancy audit.
  - J6/J8/J11: all attacked MARGINAL phenomena mined from own failure logs (0.4% oracle return gain;
    +0.19 correlation; 0.438 < 0.50 exploitability) — magnitude was checkable pre-flight and wasn't.
  - J9/J11-12: substrate properties (goal-variance, replay determinism) discovered mid-campaign.
- **The gate machinery learns one funeral behind.** L7 (substrate/magnitude pre-flight) — the ONE
  lesson that addresses selection — was distilled FROM the deaths it would have prevented. L1–L6 and
  L8 are execution/calibration patches. Four architecture-level patches already exist on this same
  wound (L1 low priors, L2 phenomenon≠recipe, L7, the HUNCH lane, the symmetric-gates rule, the
  value-bar-external ruling): by the systematic-debugging 3-fix rule, this is a wrong-architecture
  signal, not a needs-another-lesson signal.
- **Autopsy output is banked, not reused.** Aerial's accessibility-ladder finding fed nothing;
  BRIGHT's fork options (a/b/c) were never pursued; the relaxation ladders generated across the
  record produced zero adopted rungs. The "negative metabolism" produces archives, not direction.
- **The two best direction-level moves in the whole record came from OUTSIDE the loop** — the
  GPT-5.6 deep-research strategy report and the GPT-5.6 strategic pivot — i.e., from grounded
  external frontier signal, not from the failure-metabolism.

Secondary root: **rule mass accretes after every failure** (~2,400 standing lines and growing), which
raises process load and trigger ambiguity without touching the selection asymmetry. The corpus itself
knows this — it contains ≥5 anti-ceremony clauses (gate-pressure check, "prereg >20 lines is
documenting", "no ceremony between moments", process-budget pulse, HUNCH lane) — a system that needs
five escape valves is telling you the main path is over-pressurized.

---

## 2. The four devil's-advocate challenges, adjudicated against evidence

### 2.1 "The model can't discover high-taste, novel research problems" — PARTLY TRUE, and the design should stop pretending otherwise

Evidence FOR: every internally-generated direction died (J1 saturated, J6/J8 marginal, J11 not
exploitable); the two direction-setting wins were externally grounded (deep-research report; GPT-5.6
pivot) or human redirects. Internal taste, as currently fed, is below the venue bar.

Evidence AGAINST over-reading this: the internal machinery is EXCELLENT at the complementary skill —
killing honestly and cheaply (L5: kills better-calibrated than builds; J7 Brier 0.04; every kill in
the record was honest). The pipeline is a first-rate **falsification engine** attached to a
second-rate **problem generator**.

Consequence: don't try to prompt-engineer taste into the generator. Re-route: (a) ground selection in
LIVE external frontier signal at prospect time (the browser lane is the only search-grounded engine
and currently fires almost exclusively post-hoc); (b) make selection empirical-first — prefer
problems where a pre-flight probe shows a LARGE structured phenomenon (L7 as an admission gate, not
an autopsy lesson); (c) put the human at direction-admission with a one-page brief (Devil.md §20 —
human currently enters only at promotion, after the cost is sunk).

### 2.2 "Failure-case modeling is over-aggressive / biased toward marginal niches" — TRUE as the PRIMARY feedstock, FALSE as a boundary tool

The conductor's own spine says it: "FAILURE cases → compress to the root → attack the root."
`/prospect` Mine 1 is "own-log ANOMALIES FIRST". The banks agent confirmed there is **no success or
capability bank anywhere** — failure atlas, anti-patterns, kill registers only. GPT2's diagnosis is
locally confirmed: mining residuals of strong incumbents yields marginal phenomena BY CONSTRUCTION
(the incumbent already ate the large effects). J6/J8/J11 are three consecutive instances.

But the anti-thesis also holds (Devil.md §4–5): success-mining has cherry-picking/survivorship
failure modes, and the record's failure-derived CONSTRAINTS were genuinely valuable (L-series priors
measurably improved forecasts). Verdict: **failures are the right input for boundaries, calibration,
and kill-priors; the wrong primary input for generation.** Keep failure→constraint/lesson; move the
generative feedstock to (i) frontier signal (live search), (ii) surprising SUCCESSES / capability
deltas (one new mine + one bank with corrosion discipline — Devil §4's discovered-slice vs
confirmed-slice grading), (iii) magnitude-screened phenomena.

### 2.3 "The pipeline is over-engineered; simplifying would improve it" — TRUE for the generative half, FALSE for the honesty kernel

Numbers: ~2,400 standing lines; 8-field prospect cards + 10-field forge cards + ~20-field prereg +
7-item programme pulse + 6 write conventions + 8 trick families + 5-step abduce. The empirical record
shows which components actually changed decisions:

- **Earned their mass (keep, binding):** prereg kernel {hypothesis, metric, sealed split, accept/KILL,
  seeds, FORECAST} — the ledger rows demonstrably calibrated (J7 forecast low, died as forecast);
  exp-verify anti-no-op (caught the J6 RNG artifact class); the DOWN-only/CLAIM_STANDS invariant;
  launch arithmetic + kill-checkpoints; sealed-split protection; occupancy 精读 (killed J1 for ~0 GPU).
- **No evidence of decision impact in the entire record (cut or demote to advisory):** IDEATION-TAGs;
  the RECONSTRUCTION field as a per-card requirement; the schools/frames forced-diversity machinery
  (collapse to one line: "≥1 rival-frame candidate carrying a DIFF-PREDICTION"); the 6-round MoA
  chain ceiling (2–3 rounds were decisive in every recorded use); the 7-item programme pulse (3 items
  did the work: surprise accounting, process budget, diversity); most of externalize's ceremony
  beyond the six write conventions.
- **Deletion test (Devil §3) as standing policy:** any card field that, if left empty, would not
  change the next action, is decoration — run this test at each pulse and cut. Target: ~30–40%
  corpus reduction with zero loss of binding constraints.

### 2.4 "Prompts are over-explicit; let the model assume roles naturally" — TRUE for generative reasoning, FALSE for adversarial/verification reasoning

The asymmetry that resolves this tradeoff, stated once:

> **Be explicit exactly where the model's incentives are misaligned with truth (self-verification,
> claim-grading, post-hoc rationalization) and where physics is non-negotiable (GPUs, budget, sealed
> data). Be goal-shaped everywhere the model's incentives are aligned (ideation, mechanism design,
> experiment creativity).**

Rationale with evidence: scripted verification works because it is adversarial-to-self and checkable
(anti-no-op, pre-mapped discriminator branches, evidence grades — each blocked a real failure in the
record). Scripted GENERATION under-performs because a strong model fills mandatory fields as a form
(Devil §3's "flow performance") — the record's card fields did not decide anything; probes and
occupancy did. Concretely: prospect/forge keep only {Q · WHY-NOW with magnitude evidence · KILL ·
COST}, plus goal + constraints + the banks as RETRIEVAL (a prior, not a recipe); abduce compresses to
its 2-line kernel ("≥3 mechanisms incl. boring+incumbent; pre-map every discriminator branch before
looking") with the rest as reference.

---

## 3. Verdict on the three audit documents

- **GPT1.md** — not a pipeline audit; a per-idea risk table for one drone-navigation idea. ADOPT its
  FORMAT as a lightweight direction-admission artifact: the "problem → consequence → mitigation"
  table plus **"the 3 first experiments, each of which can kill the direction"** (its §21). That
  triple-kill-first pattern is the strongest transferable idea and slots into the admission gate.
- **GPT2.md** — thesis CONFIRMED by the local record (rigorous solver, weak selector; cost-ordering
  eats value judgment; failure has full metabolism, success has none). ADOPT: the two-loop split
  (problem-discovery ≠ problem-solving), value-score vs first-step-cost separation ("value decides
  WHAT, information-gain decides WHERE TO START"), a Capability Atlas + capability-prospect mine.
  REJECT the full 5-module Success-Expansion apparatus — implement as ONE mine + ONE bank file, or it
  reproduces the over-engineering failure on the success side (Devil §18's scope-explosion warning).
- **Devil.md** — the most valuable of the three. ADOPT: NON-GOALS + DECISION-CHANGE in the goal
  contract (§2); the field-deletion test (§3); discovered/confirmed/mechanistic slice grading (§4);
  EXECUTION/DESIGN/INFERENCE-valid layering of verification (§14 — L8/J11-v4 was precisely a
  DESIGN-validity failure that exp-verify structurally cannot catch); relaxation-ladder caps
  MAX-RELAXATIONS + MINIMUM-STAKES (§17 — J11's v3→v4→v5 triple recut is the local instance);
  earlier human entry (§20); red-team question 9 ("what evidence would stop the whole program") asked
  at every region-close. REJECT for now: multi-conductor redundancy and sealed-set access budgets —
  real risks, but the priced-not-blocked versions suffice at this team size.

---

## 4. Stage-by-stage: explicit vs free

| Stage | KEEP EXPLICIT (binding) | MAKE FREE / CUT | Why (evidence) |
|---|---|---|---|
| Goal contract | bindings (env/hardware/keys/engines); **ADD: NON-GOALS · DECISION-CHANGE** | — | proxy-goal capture (Devil §2); contract is currently what-to-do only |
| /prospect | **NEW binding admission gate** (see §5); banks as retrieval | 8-field card → 4 fields; IDEATION-TAGs; per-card RECONSTRUCTION | no card field decided anything in the record; selection is where 70% of cost leaked |
| /forge | KILL-per-candidate · two-sentence test · ORACLE/TRIVIAL bracket before training · necessity check as pricing | forced-diversity axes machinery → one rival-frame line; MoA fires on genuinely irreversible only | brackets + kills carried the record; axes never surfaced a winner |
| /prereg | the whole kernel + FORECAST row + launch arithmetic (strongest component in the record) | trim the optional blocks that never fired | J7 Brier 0.04; ETA discipline post-L3 |
| run / operate | GPU policy · measured-ETA · kill-checkpoints · ownership tests | — | hard physics; user-designated as explicit |
| /exp-verify | 3 stages + surprising-result extension; **ADD: DESIGN-VALID layer** (unit/positivity/MNAR/confound checklist, pre-run) | — | J11-v4 passed execution-validity while design-invalid; L8 exists but isn't mechanized |
| /adversary | the invariant (DOWN-only self-grant; CLAIM_STANDS independent) — untouchable | — | cheap, worked every time it fired |
| /autopsy | conversion law (≥1 of constraint/candidate/close); ladder with **MAX-RELAXATIONS + MINIMUM-STAKES cap** | 7-item pulse → 3; extraction schema changes (§5) | ladders were generated-never-adopted; the pulse items beyond 3 never fired |
| conductor | engine division · autonomy boundary · **ADD: selection-loop/solving-loop split + human checkpoint at direction admission** | trim duplicated rules restated from sub-skills | single-point epistemic failure (Devil §7); human currently enters post-sunk-cost |

---

## 5. What to extract, per knowledge structure

**Failure cases (atlas/autopsy rows)** — current schema {dead-because, reopen-if, constraint} keeps
the epitaph but loses the selection lesson. New row schema:
`{phenomenon-magnitude (the number that was too small) · which ADMISSION gate would have caught it ·
substrate property that killed it (determinism/goal-variance/SOTA-gap) · transferable constraint ·
cost-of-kill}`. Purpose: every death mechanically sharpens the ADMISSION gate, not just the atlas.

**Successes (new, single file: capability bank)** — at every CLAIM_STANDS or surprising PASS:
`{capability observed · minimal conditions (what it survived ablating) · corrosion check passed
(contamination/shortcut/slice-search — Devil §4 discipline) · transfer targets · boundary (where it
stopped) · grade: DISCOVERED / CONFIRMED / MECHANISTIC}`. Feeds a new prospect mine. One file, one
mine — no further machinery.

**High-impact-paper mining (精读)** — currently extracts occupancy + operator cards (mechanism-side).
ADD one field per 精读: **the paper's selection rationale** — what magnitude/decision made this
problem matter, what the authors measured FIRST to convince themselves (their step-zero probe). This
is the missing taste signal; the operator banks already capture the mechanism signal well (the banks
audit found them the best-engineered layer: uniform schema, numeric kill criteria, deletion-tested,
retrieval-indexed — change nothing structural there).

**Candidate/operator banks** — keep as is, plus: an INGESTION path (MoA-surfaced or probe-surviving
operators enter through the existing corrosion gate instead of waiting for a manual audit pass), and
the staleness rule already implicit in Trick.md (dated facts carry their cutoff; principles don't).

---

## 6. Strategic tool combination (MoA · browser external brain · Arbor)

Current state (from the integration audit): all three tools point at the SOLVING loop. The external
brain is a **late sequential judge** (event-triggered: forks, region-closes, claim review); MoA fires
at forge/irreversible forks with genuinely differentiated lanes (per-lane prompts + structured
dropout are real) but is **codebase/cost-blind** and its output feeds no bank; Arbor is a **passive
one-way log** — nothing reads tree state into consults automatically, and no verdict writes back.

Redesign — point the trio at SELECTION, and wire them into a cycle:

1. **External brain → front of the loop (its unique capability is LIVE SEARCH — using it mainly
   post-hoc wastes exactly what makes it irreplaceable).**
   - `/prospect` frontier scan at goal-start/region-close: live field map, capability deltas,
     what-just-became-possible — grounding WHY-NOW in the actual frontier instead of memory.
   - **Admission-time venue micro-review** (one query per direction, ~minutes): "would a result of
     plausible magnitude M on substrate S clear venue V?" — the existing role-4, moved from
     region-close to admission. DROP stays advisory mid-loop; at admission it's a price signal.
   - Late roles (claim review, region-close review) unchanged.
2. **MoA → problem-level diversity, cost-aware.**
   - Fire the differentiated panel at PROBLEM GENERATION (per-lane mines/disciplines/dropout), not
     only at approach generation — GPT2's discovery loop gets the diversity engine that currently
     only the solving loop enjoys.
   - Fix codebase-blindness: every lane brief carries the 5-line inventory {hardware, envs,
     checkpoints, measured throughputs} so "cheap probe" suggestions are runnable as stated.
   - Diversity is judged by DIFF-PREDICTIONS, not vocabulary (Devil §11's candidate-distinction
     matrix): two lanes whose predictions match under every probe are one lane.
3. **Arbor → active state machine and the shared substrate of every consult.**
   - Node meta stores the ADMISSION-gate data (measured magnitude, determinism check, SOTA-gap,
     venue micro-verdict) so the gate is mechanical, like the existing merge-gate pattern.
   - Boundary triggers: promotion/region-close auto-assembles the packet (`generate_report` +
     artifact paths) → fires the external review → **verdict written back to node meta**. The tree
     stops being an audit log and becomes the loop's control state.
   - Every consult (panel lane, external brain, reviewer) receives `tree_view(fmt="constraints")` +
     the derived synthesis as its context floor — one substrate, three engines, no
     paraphrase-of-paraphrase.
   - Complementarity, stated once: **MoA = breadth (parallel diverse hypotheses, tool-free) ·
     external brain = grounding (live search + venue calibration) · Arbor = state (what is dead,
     open, and proven).** Selection quality = breadth × grounding × state; today selection gets
     almost none of the three.

---

## 7. Prioritized changes

**P0 — attacks the root cause; cheap; do before the next campaign cycle:**
1. **Binding ADMISSION GATE at direction adoption** (the L7 content, promoted from lesson to gate):
   reproduce-or-verify SOTA on the substrate · measured phenomenon magnitude (large + structured, a
   number not an adjective) · goal-variance check · replay-determinism check · occupancy 精读 ·
   venue micro-review. Nothing GPU-heavy dispatches on an unadmitted direction. (Historical
   counterfactual: ~70% of sunk cost.)
2. **External-brain frontier scan at /prospect** (goal-start + region-close), replacing own-log
   anomalies as the FIRST mine; anomalies stay as a mine, demoted from first.
3. **Goal contract adds NON-GOALS + DECISION-CHANGE.**
4. **Human checkpoint at direction admission** — a one-page brief (the GPT1-style risk table + the
   3 kill-first experiments), async, non-blocking for cheap probes; blocking for GPU-scale commitment.

**P1 — structural hygiene:**
5. Capability bank + capability mine (one file, one mine, corrosion-graded).
6. Field-deletion pass over the corpus (~30–40% cut; the §2.3 keep/cut lists).
7. exp-verify DESIGN-VALID layer (mechanize L8).
8. Autopsy: new extraction schema (§5) + ladder caps (MAX-RELAXATIONS, MINIMUM-STAKES per rung).

**P2 — tool wiring:**
9. Arbor active triggers + verdict write-back; consult context floor = constraints view + derived synthesis.
10. MoA at problem-generation, cost-aware lane briefs, DIFF-PREDICTION-based diversity check.
11. Bank ingestion path for MoA/probe-surviving operators.
12. Red-team pulse at every region-close: Devil §22's nine questions, ending with "what evidence
    would stop this program entirely" — no answer ⇒ the program has no brakes.

**Explicitly NOT recommended:** rebuilding the solving loop (it is the proven half); softening the
honesty invariants (untouchable per design principle 3); adopting GPT2's full success-expansion
module suite; multi-conductor redundancy at current team size.
