# Design (PARKED): Decouple the pipeline from elapsed time — evidence/budget-gated, not schedule-paced

> **STATUS: PARKED / future work (2026-07-13).** Decision: run the `world-model-v2` goal test FIRST on
> research-os v4.0 as-is; implement this redesign afterward. This doc is implementation-ready so a future
> session can pick it up cold. Sibling context: `plan/Audit/pipeline-devils-advocate-audit-2026-07-13.md`
> (the audit that produced v4.0) and `plan/research-os-v4-four-gates-plan-2026-07-13.md` (the v4.0 plan).
> Backup of the pre-v4.0 corpus: git tag `v3.7-pre-v4.0-backup` + `backups/pre-v4.0-2026-07-13/`.

## 1. The problem (user framing, 2026-07-13)

The pipeline should be driven by **evidence accumulation, uncertainty reduction, compute budgets, and
stopping criteria** — NOT by fixed elapsed time. Time-as-ceiling (a budget you spend down) and
time-as-measurement (ETA, throughput) are fine; time-as-**schedule** (a calendar rhythm the agent paces
itself to) is not. Concretely wanted:

- Gates fire on accumulated evidence, not "after several days."
- Progress keys on confidence / information gain / decision quality, not calendar time.
- Independent probes run in **parallel**, not serialized into a "Week-1 then Week-2" narrative.
- If enough evidence arrives in an hour, advance **immediately** — don't wait for an assumed schedule.
- Net goal: cut end-to-end time-to-a-promising-direction while preserving decision rigor.

## 2. Grounding — what the LIVE v4.0 corpus actually contains

Audited `skills/*/SKILL.md` for every temporal reference (grep). Finding: **the live skills are mostly
already clean; they use time as a resource ceiling or a measurement, not as a schedule.** The explicit
calendar pacing the user worried about is NOT in the skills.

| Reference | Location | Kind | Verdict |
|---|---|---|---|
| `> ~1 GPU-day` admit trigger | admit §When it fires | compute **budget** | keep (maybe restate as device-hours) |
| `≤2h wall-clock` hunch budget | conductor HUNCH lane | resource ceiling, but **time-as-proxy** | **reframe** |
| `2h+ no progress`, `>30 min zero-output` | operate §3/§4 | liveness/safety circuit-breakers | keep |
| `60-second timing probe`, ETA, device-hours | operate §1/§3 | **measurement** instruments | keep |
| "localize … in hours, without retraining" | tricks (desc) | descriptive class label | keep (harmless) |
| `≤12 dispatched cycles`, `≤3 consecutive inconclusive` | conductor bounded-autonomy | **count/evidence-based** | keep (already correct) |
| `cost-of-kill: <GPU-h / wall-clock>` | autopsy extraction row | measurement | keep |

**The real schedule ("Week-1 probes → Week-2 gate", "4-week ramp", "1–2 weeks to admit") lives only in
`plan/world-model-direction-2026-07-11.md` — archived history the fresh restart does not load.** So the
gap is not "rip out a hardcoded timeline." It is: **nothing states the principle that forbids
schedule-based reasoning**, which is why the conductor GENERATED a Week-N plan last campaign. Fix the
generator's principle, not a literal.

## 3. Recommended design — "Principle + targeted cleanup" (surgical, matches v4.0 gates-not-scripts)

Rejected alternative: a formal {evidence, confidence, budget} STATE MACHINE with typed states
(Devil.md §8). It reproduces the machinery v4.0 deliberately cut; the audit rated it the heaviest
option. The principle below buys the same behavior at a fraction of the mass.

### 3.1 The load-bearing principle (NEW — add once, in `conductor/SKILL.md`, §1)

> **Time is a resource you SPEND and a quantity you MEASURE — never a schedule you PACE to.** Budgets
> (device-hours, dispatched cycles, sealed-eval accesses) are ceilings; ETA/throughput are measurements.
> No gate, transition, or plan is keyed to elapsed calendar time. Every transition fires on
> **EVIDENCE + CONFIDENCE + BUDGET**: when the evidence a gate needs is in, advance *now* — one hour or
> one week of wall-clock is irrelevant if the evidence threshold is met, and a full budget with the
> evidence still absent is a STOP, not a "keep going, it's only day 3." Independent probes **fan out in
> parallel** (a portfolio, not a narrative); serialize only on a true data dependency. **A generated
> plan sequenced by calendar week instead of by {evidence-milestone → gate → budget-tranche} is a bug —
> rewrite it in milestone/tranche form.**

This is a *principle*, not a mechanism — it constrains how the conductor reasons and what plans it
emits, without adding a state machine.

### 3.2 Literal reframes (small, in-place)

- **Hunch budget (conductor):** the binding limits are already `no GPU training · no sealed split`; the
  `≤2h wall-clock` is a redundant time-*proxy* for "cheap, non-committal." Reframe to a **commitment**
  ceiling: `no GPU training · no sealed split · no new infrastructure · one cheap probe`. Optionally keep
  wall-clock only as a soft illustration ("usually minutes-to-an-hour"), explicitly labeled non-binding.
- **admit trigger:** restate `> ~1 GPU-day` as `> ~1 device-day of compute (≈ N device-hours)` to drop
  the calendar word while keeping the budget meaning. (Behaviorally unchanged.)
- **operate circuit-breakers (`2h+`, `>30 min`):** annotate as **liveness timeouts on a possibly-hung
  process**, explicitly "not pacing." No numeric change — a hung job is legitimately measured in time.
- **Keep untouched:** 60-second timing probe, ETA/device-hours, tricks "in hours" (all measurement/
  descriptive).

### 3.3 Parallelism default (SELECT loop — the biggest behavioral win)

Today `prospect` emits 3–7 cards + **ONE** recommended first probe, and `forge` picks #1 — implicitly
serial. Change to a **portfolio**: emit the cheap kill-probes for the top-K candidates as a **parallel
batch**, dispatch concurrently (operate §2 free-device auto-dispatch + pipeline parallelism already
support this), kill fast on results, then concentrate GPU-scale budget on the few survivors. This *is*
the intended rhythm ("eliminate most ideas via cheap probes, allocate the big budget to survivors") —
but triggered by probe **results**, never by a calendar. Add the explicit fan-out instruction to
`prospect` (emit a probe *batch*, ranked) and/or `operate` (dispatch the SELECT-loop probe batch
concurrently, one Monitor per probe).

### 3.4 Regeneration guard (cheap, prevents relapse)

Add to the plan-writing convention (conductor write-through and/or `admit` one-pager): **a campaign plan
is structured by {evidence-milestone → gate → budget-tranche}, never by calendar week/day.** Optional
lightweight lint (autopsy programme-pulse or a `tools/guards/` check): flag plan/RUNLOG text matching
`Week-\d|Day-\d|\d+-week ramp` as a schedule-pacing smell to rewrite.

### 3.5 (Optional) name the budget-tranche ladder — formalize escalation without a state machine

Consider naming the escalation explicitly in `operate`/`admit`: **hunch-tranche** (no GPU, one probe) →
**probe-tranche** (< ~1 device-day, cheap diagnostics, `/admit` not yet required) → **admitted-campaign
tranche** (metered device-hours, `/admit` passed). Escalation between tranches is gated by evidence, not
elapsed time. This gives the "cheap-first, expensive-only-for-survivors" rhythm a concrete budget spine
while staying a paragraph, not a subsystem.

## 4. Scope of the eventual implementation

Files likely touched (all in `/home/lingxufeng/cli/research-os/skills/`): `conductor` (principle +
hunch reframe + regeneration convention), `operate` (parallel dispatch of the probe batch + tranche
ladder + circuit-breaker annotation), `prospect` (emit probe portfolio, not one probe), `admit`
(device-hours wording + tranche). Small, additive-then-subtractive; net near-zero or negative lines.
Do it as a short subagent-driven-development pass or direct edits; re-sync runtime; bump version to
4.1.0. Keep every honesty invariant untouched — this changes *pacing*, not *rigor*.

## 5. Open questions to resolve at implementation time

1. Hunch budget: drop the `2h` entirely, or keep it as an explicitly-non-binding illustration?
2. Regeneration guard: soft (pulse smell-check) or hard (a `tools/guards/` gate on plan text)?
3. Budget-tranche ladder (§3.5): worth naming explicitly, or does the principle (§3.1) + existing admit
   threshold already cover it?
4. Parallelism: cap K (how many candidate probes fan out at once) by device count, or by a probe-budget
   ceiling? (Ties to operate's concurrency math.)
5. Does `admit` itself need any change, or is it already budget-triggered (only wording)?
