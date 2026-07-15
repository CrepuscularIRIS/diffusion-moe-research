# Judgment Ledger — the pipeline's model of its OWN research judgment

> **FIRST-CLASS COMPONENT (admitted 2026-07-12 under the §0.4 criterion).** Everything else in the repo models
> the *field* (operator bank), the *experiment* (trick bank), or the *execution* (Arbor tree / RUNLOG). This
> models the remaining unmodeled object: **the quality and evolution of our research judgment** — the calls made
> under uncertainty, whether they were right, and what systematic biases they reveal. It is a LONG-TERM
> accumulation, built and refined like memory, persisting across campaigns.
>
> **Scope ruling (2026-07-12):** meta-analysis of HUMAN steering decisions is the human's own process — the
> pipeline never autopsies the user's corrections. The pipeline's reciprocal duty: a field-level strategic
> direction fork it cannot confidently decide is PAUSED to the human (with the ledger evidence attached),
> never guessed.

## Two layers (mirrors the memory design)

| File | Role | Cadence |
|---|---|---|
| `ledger.md` | **Append-only forecast log.** One row per judgment: the call, a falsifiable forecast, its basis, and a pre-named RESOLVER. Written BEFORE the outcome is knowable; a post-hoc edited row is VOID (same rule as prereg). | write at decision time · resolve when the resolver fires |
| `lessons.md` | **The curated distillation** — calibration priors + systematic biases ("we overestimate X by ~2×"), refined over time like memory. New forecasts APPLY these priors as explicit corrections. | distill at each programme pulse + campaign close · recall at goal-start |

## The unit: a judgment row

A judgment is loggable iff it has all four fields — no resolver ⇒ unfalsifiable ⇒ not a judgment, don't log it.

```
| id | date | type | the call (one sentence) | forecast | basis | resolver (event) | outcome (date) | score | lesson |
```

- **forecast** — a probability (for binary calls) or a numeric estimate with a range (for costs/effects).
  Calibration-tag the basis: {verified · inferred · guess}.
- **basis** — what produced the number: operator card / MoA panel / Second-Brain read / historical prior / gut.
  (Later analysis asks: which basis is best calibrated?)
- **resolver** — the concrete future event that scores the row (a probe verdict, 精读, Phase-1 exit,
  submission-time search). Every row names one at write time.
- **score** — Brier `(p − outcome)²` for probabilities; log-ratio error for numeric estimates.
- **lesson** — filled ONLY on surprise (large score). Routine confirmations get a score, not prose.

## Decision types (log these; skip trivia)

| Type | What | Typical resolver |
|---|---|---|
| `SELECT` | which candidate/probe/direction gets the next run — P(it clears its pre-registered bar) | the run's verdict |
| `PREREG` | every claim-bearing run: P(ACCEPT) + predicted effect size + predicted cost (the mandatory FORECAST line of `/prereg` mirrors here) | `/exp-verify` + verdict |
| `OCCUPANCY` | novelty/saturation call ("this slice is open/taken") | local 精读 · submission-time search |
| `KILL/PARK` | direction-death call | reopen events · external literature |
| `COST` | launch-arithmetic estimate (ETA / GPU-hours) vs actual | the run itself |
| `HUMAN-STEER` | a fork escalated to the human: record the fork, the options presented, the human's choice, the eventual outcome. Record only — analysis of these is the HUMAN's process. | downstream outcome |

## Loop wiring

- **WRITE:** at every `/prereg` (FORECAST line mandatory) · every SELECT that routes a training-eating run ·
  every occupancy/kill call that routes work. Log the judgments that ROUTE real work; don't farm easy rows.
- **RESOLVE:** when the named resolver fires (`/exp-verify`, `/adversary`, 精读, Phase exits) — resolving open
  rows is part of that 验收, same standing as the tree update.
- **DISTILL:** at each programme pulse (after every 2nd `/autopsy`) + campaign close: recompute the calibration
  summary in `lessons.md`, update/add priors, prune stale ones. Distillation is CURATION — few strong priors
  beat many weak notes.
- **APPLY:** when writing any new forecast, check `lessons.md` first and state the correction explicitly
  ("raw instinct 0.7; L2 mechanism-conversion prior caps at 0.4 → logging 0.4").
- **RECALL:** `lessons.md` is read at goal-start + before every claim-bearing `/forge`, alongside `MEMORY.md`.

## Anti-gaming (the ledger is subject to the same integrity rules as evidence)

Forecasts precede outcomes (append-only; edits void) · every row has a resolver at write time · the ledger is
never cited as evidence FOR a claim (it scores the judge, not the experiment) · calibration numbers in
`lessons.md` are recomputed from the rows, never recalled from memory (artifact-fidelity applies to ourselves).
