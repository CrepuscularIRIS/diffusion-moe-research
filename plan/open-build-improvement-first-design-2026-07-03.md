# Design — "Open the build": improvement-first · survey-evidenced · 2-GPU pipelined (2026-07-03)

> **Status: APPROVED (user, 2026-07-03).** A GOAL + operating-manual change only — research-os v1.0 plugin is
> NOT touched (anti-accretion). Trigger: the VLA-fusion region is CLOSED (crux image-bridge probe = NO-GAP,
> base ACS 0.997; ~7 probes / 0 positives) — the frozen model already saturates our synthetic composition
> tasks. Root cause: we probed where the model is already strong. Fix: build on real HF datasets that surveys
> already say are hard, improvement-first, judged by type.

## §1 — Value bar (improvement-first, any honest non-eval type)
The 一区 contribution is a **big, honest, falsifiable Δ on a HARD, field-acknowledged-open problem**.
Improvement (刷分) is the **primary** path; systems / compression / novelty also count, each judged by its own
`research-types.md` bar. **Name the TYPE first. No evaluation-type.** Occupancy **re-prices, never vetoes** —
"done" ⇒ *beat it / measure what they didn't*, NOT downgrade (this is the fix for Pro's 做过了→降级 reflex; it
was already the rule, the goal's novelty-framing overrode it). **ANTI-RETREAT kept:** hard + big-Δ +
fair-baselined, never incremental 刷分, never a certificate/retreat.

## §2 — Training gate (MODE: FAST → BUILD-on-evidence)
Keep size-first, swap the cheap signal from *local synthetic probe* (kept saturating → never trained) to
**real-dataset headroom**: survey-evidenced hard problem → matching **HF dataset** → cheap headroom eval on the
REAL data (does the frozen base fail? Δ room?) → **yes ⇒ evidenced target ⇒ commit the ~4h train.** Kill only
if the base already solves it, or it's a pure capability wall. Training is now *reachable*.

## §3 — Entry: Pro-survey-mining across domains (`/prospect` Mine 2, taste-shaped)
Default entry = Pro mines **综述 + capability-deltas** across **多模态融合 · 信息压缩 · 矩阵表示 · OOD/semantic-support**
(+ taste-derived neighbors) for **long-acknowledged-open / recurring-hard** problems (future-work graveyard,
repeated "still unsolved", missing head-to-heads) — each with a candidate **HF dataset** + WHY-it's-hard + a
cheap headroom test. Datasets/models/platform **expandable from HuggingFace** (π0.7/π0.5, …; prefer HF). Pro
designs the improvement *mechanism* using the frames/operators axes (the elegant-math-modeling, protected).

## §4 — 2-GPU hybrid parallelism (operating-manual §5.3)
- **Default = pipeline:** while a run occupies the GPU(s), the main loop designs/searches the *next* node (the
  productive use of the ~4h wait; §4.9).
- **Split = when two evidenced targets are queued,** each fitting one GPU: GPU0=Idea-1 / GPU1=Idea-2 burst,
  then reconverge. **Each split run = its own Arbor node + its own worktree** (no dueling writes).
- WAIT discipline unchanged: 4h train → Monitor/bg-wait → consume→verdict, never a ScheduleWakeup poll.

## §5 — Untouched (guardrails)
research-os v1.0 plugin NOT modified (anti-accretion); the 4 axes (schools/types/frames/operators = the
elegant-math-modeling) stay and get *used* by improvement-first design. Kept: the one invariant ·
artifact-fidelity · `/prereg` seals claim-runs · `/adversary` the claim gate · **REGION-CLOSE** (VLA-fusion
stays closed; VLA = one domain option, not the mandate) · no-eval-type.
