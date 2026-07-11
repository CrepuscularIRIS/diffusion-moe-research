# Missing Attack-Angles Audit — 2026-07-10

> User question: has the pipeline overlooked a critical angle of attack, beyond the machined axes
> (schools · types · frames · operators · diagnostic-tricks · reconstruction · atlas/necessity-gate)?
> **This file = evaluation criteria for future goal implementation.** Each axis below carries the
> goal-time evaluation question. Verified against the live skill texts (not assumed); ranked by
> (impact × how completely it is absent). Anti-accretion applies: every adoption FOLDS into an existing
> part — zero new commands.

## A1. Identifiability + synthetic-world validation (the OSSE rung) — the biggest true gap
**What:** before empirically testing an attribution/separation/mechanism claim on real data, (i) argue the
target quantity is IDENTIFIABLE in principle from the observables, and (ii) build a controllable synthetic
world where the latent ground truth (failure source, corruption, conflict) is KNOWN and injected — the method
must win there first. A method that cannot attribute in a world where the answer is known is dead, at near-zero
GPU cost.
**Evidence from our own history:** the water campaign's leak-injectors WERE this pattern (and worked: GATE-2
5/5); the DA reconstruction named it (OSSE); yet P0 MM-OVSeg burned the phenomenon gate discovering
empirically that conflict signals ≈ chance — an identifiability probe on a synthetic optical-SAR conflict
generator would likely have predicted this cheaper. The move exists in campaign history but is NOT a named
rung anywhere in the live pipeline.
**Fold:** one line in `/prereg` BRACKET guidance + one family in the diagnostic-tricks catalog:
*"attribution/source-separation claims add an IDENTIFIABILITY line: the synthetic-injection world where the
answer is known, and the method's score there. Fail there ⇒ dead before real data."*
**Goal-time evaluation question:** does every attribution/separation claim carry a synthetic-world result
before its real-data phenomenon gate?

## A2. Data-intervention as an attack move — the arsenal is model-only
**What:** the taste arsenal (`frames · operators · 视角转换 · elegant modeling`) only ever attacks the MODEL.
Elite practice attacks the DATA at least as often: targeted hard-case collection/synthesis, relabeling,
re-weighting, hard-negative mining, curriculum, filtering. In 刷分 mode the cheapest true lever after error
analysis is frequently data, not mechanism — and a "would 200 targeted examples fix this cluster?" probe is
hours, not a training run.
**Evidence:** `/forge` step 3 forces school/frame/operator candidates — all model-side; the 刷分 loop's
武器库 lists no data move; data appears only as a NO-GO check (launch-arithmetic sufficiency ratio).
**Fold:** one clause in `/forge` step 3: *"if the atlas marks the failure signature data-shaped (long-tail,
coverage gap, label noise), one candidate MUST be a data intervention, bracketed by its own oracle (train on
the fixed data ceiling)."*
**Goal-time question:** when a failure cluster is data-shaped, did a data-intervention candidate compete
against the mechanism candidates?

## A3. Raw-failure forensics made literal (become-one-with-the-data)
**What:** aggregate metrics hide the failure's shape. The requirement to have EYEBALLED N raw failure cases
(images/rollouts/transcripts) before designing an attack exists only as spirit, not artifact.
**Evidence:** `/forge` FAILURE-SIGNATURE asks "which examples fail" but accepts aggregates; per-example
regression fires only post-hoc in `/adversary` A. The aerial 2-DOF bug and the AVDN action-space bug were both
caught by *looking at raw rollouts*, late.
**Fold:** one clause in the `/forge` FAILURE-SIGNATURE field: *"cite the artifact of ≥20 raw failure cases
read (path), not only aggregate numbers — no signature from aggregates alone."*
**Goal-time question:** can every /forge card point to the raw examples its author actually read?

## A4. Negative-space + incentive-audit mine (endorsed in Perspective.md, never wired)
**What:** `/prospect` mines contradictions, graveyards, capability deltas — all *visible* literature. The
avoided-object scan (what the field systematically does NOT work on, and the incentive that maintains the
avoidance — easy metrics, free datasets, incumbent-flattering stories) is a distinct, high-leverage problem
source. Perspective.md T10 + #7 endorsed it; it never entered the skill.
**Delta vs the existing graveyard mine:** graveyard = promised-but-undelivered; negative space =
never-promised-because-avoided + WHY it stays avoided (which also predicts adoption friction).
**Fold:** one sub-bullet in `/prospect` Mine 2.
**Goal-time question:** did problem-finding name at least one avoided object and its maintaining incentive?

## A5. Trend/slope credibility (the small-compute 一区 multiplier)
**What:** under a 4–6h cap we cannot win by absolute scale; we CAN win by reporting the TREND — does the
method's Δ grow/hold/vanish across data sizes, model sizes, or held-out events? A 3-point slope is a far
stronger claim than one point, and cheap. Battery-2 asks "doesn't-scale?" rhetorically; nothing measures it.
**Fold:** optional SLOPE line in the `/prereg` CONFIRMATORY block: *"Δ at 3 scales/datasets + the fitted
direction; a claim whose Δ shrinks with scale is scoped to small-scale."*
**Goal-time question:** does the paper-main claim carry a slope, not just a point?

## A6. Adaptive/worst-case stress for reliability claims (thesis-specific)
**What:** for selective-prediction/abstention claims specifically, the reviewer-grade attack is an ADAPTIVE
one: a shift/adversary chosen to maximize accepted-set error (game the confidence signal), not the average
corruption battery. `/prereg` FULL "stress" and `/adversary` D "first realistic perturbation" gesture at it;
no worst-case search exists.
**Fold:** one line in the `/adversary` A checklist, active only for reliability-type claims: *"report
worst-case accepted-set error over the held-out shift family, not only the mean."*
**Goal-time question:** has the reliability claim survived the shift chosen to break it?

## A7. Effect-size meta-analysis to calibrate ACCEPT/MDE (small)
**What:** ACCEPT thresholds and POWER/MDE currently rest on guessed effect sizes. Reading the last ~5 papers'
Δs on the exact benchmark (venue-taste already reads them for STYLE) calibrates what Δ is publishable and
what MDE the experiment needs.
**Fold:** one column in the venue-taste/atlas row: `typical published Δ`.

## Deliberately absent (checked — not gaps)
- **Timing / 位置感 / contribution taste** — human-supplied by design (spark.md verdict; do not automate).
- **Paper-craft** — deferred to the PAPER-SKELETON trigger; correct.
- **Sequential experiment ordering** — Battery 1 (uncertainty-first SELECT) covers it.
- **Harness validation, oracle brackets, counterfactual corruption** — already machined (diagnostic tricks).
- **Compute-profile fit at direction selection** — burned once (water), now encoded in the goal's domain lock.

## Adoption rule (anti-accretion)
All seven folds are single lines/clauses inside existing parts — no new command, no new axis file. A1–A3 are
the load-bearing three; A4–A7 are cheap sharpenings. If any fold produces ceremony (synthetic worlds nobody
trains against, data candidates that never win), cut it back per the standing watch-rule.

> A1–A7 folds IMPLEMENTED 2026-07-10 — prereg (IDENTIFIABILITY · SLOPE · PROPOSERS), forge
> (data-intervention · raw-failures · reconstruction pass), prospect (negative-space mine), adversary
> (worst-case stress), venue-taste Δ column + FableTrick A8. Independence caveat still open: the
> cross-family blind-spot query has not run yet.

## Independence caveat
This scan is Opus-solo. The pipeline's own thesis (taste = panel + gates + atlas, not one model's weights)
says a single-model blind-spot scan has blind spots. Before freezing this list into goal evaluation criteria,
run ONE context-free GPT-5.6 query (and optionally a MoA breadth pass) on exactly this question — "what
fundamental methodological axis is missing from this pipeline?" with the axis inventory attached — and
reconcile. A cross-family miss list that comes back empty is itself evidence the set is near-complete.
