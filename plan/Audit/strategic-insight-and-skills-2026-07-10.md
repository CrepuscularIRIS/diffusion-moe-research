# Strategic Insight + High-Value Skill Candidates — 2026-07-10

> Reflective assessment (not a task record). Drawn from mining every campaign in the archive this session
> — dLLM · DSpark · VLA-manipulation · aerial/AVDN · OpenFly/AirNav · C5/BEV · water · optical-SAR — not just
> the active one. Companion to `plan/Audit/latent-issues-audit-2026-07-10.md` +
> `plan/Audit/missing-axes-2026-07-10.md`.

---

## Part 1 — The critical insight

**Your binding constraint is problem-selection feasibility, not pipeline quality — and your effort is
allocated as if it were the reverse.**

### The cross-campaign evidence
Stripped of narrative, here is how every campaign actually died:

| Campaign | Cause of death | Kill type |
|---|---|---|
| Aerial VLA / AVDN | SOTA needs the GeoChat RS-init, never publicly released | feasibility (asset) |
| OpenFly / AirNav reliability-fusion | no deployable signal recovers the ceiling; needs a GeoChat-class base | feasibility (asset) |
| Optical-SAR MM-OVSeg | reproduction PASSED (73.61) but the phenomenon didn't exist (+0.02 AUROC over a trivial floor) | feasibility (no phenomenon) |
| C5 / BEV | <2% headroom on standard benchmarks; only a hand-constructed favorable regime showed anything | feasibility (no headroom) |
| Water | wrong compute profile (CPU-heavy) for a 2×4090 envelope | feasibility (compute) |
| dLLM / VLA-manipulation | occupied / tuned-incumbent walls | feasibility (occupancy) |

**Every one is a feasibility kill, not a method kill.** None died because a mechanism wasn't clever enough.
They died on properties knowable *before* the weeks of setup, each answerable in hours at selection time:
- (a) is the SOTA baseline reproducible from **released** assets (no unreleased-init blocker)?
- (b) does headroom / a phenomenon demonstrably exist on the **real, standard** benchmark (one oracle probe)?
- (c) does a win fit **≤4h / 2×4090**?

Each campaign was killed by exactly one of those three.

### The asymmetry you may not see from inside it
**You have built a world-class *post-commitment* kill apparatus and a nearly-absent *pre-commitment*
feasibility apparatus.** A training run cannot launch without `/prereg` + launch arithmetic + a kill-checkpoint.
But *choosing an entire direction* — which costs 10–50× a training run — is gated by a hunch and a scouting
report. **The most expensive decision you make is the least gated one.**

The whole `/prospect → /forge → /adversary` engine presupposes a feasible substrate. Substrate feasibility is
exactly what keeps failing. So the engine runs beautifully on ground that was never winnable, produces an
honest "strong diagnosis, no method win," and you pivot. You built a superb engine for the last 90% of the
problem and keep getting killed in the first 10% you spend the least structured effort on.

### Why it persists (the uncomfortable half)
Building pipeline is more tractable and more rewarding than confronting that the last four problems were dead
at selection. So effort flows to the machinery — research-os v0.4→v1.1, MoA panels, guards, atlas, operators,
the reconstruction axis, the missing-axes audit. You even had to invent an anti-accretion rule because
accretion kept happening. That is `Perspective.md`'s "the audit becomes the procrastination engine" —
operating at the **campaign** level, where it is invisible because each individual kill looks like legitimate
science.

### The decision change
**Invert the gating. Make direction commitment the MOST-gated decision you make, not the least.**
Before any environment setup, a hard pre-commitment gate must answer the three envelope questions with cheap
evidence (a released-checkpoint check · one oracle/headroom probe on the real benchmark · compute-profile
arithmetic). Any failure → the direction never enters the pipeline. Route that gate through the external
brain / MoA the way you route a mechanism fork.

Do this and the "no method win" outcome mostly disappears — not because your methods get better, but because
you stop spending months proving that unwinnable problems are unwinnable. **The pipeline is not your problem;
it is ready. Stop improving it.**

> Honest caveat: this is my read across the archive and could be wrong, or you may value the pipeline-building
> and the exploration as goals in themselves. But if the stated goal is ONE 一区 method contribution, the
> evidence says selection — not execution — is where it is being lost.

---

## Part 2 — High-value recurring workflows to package as skills

Based on the work you repeatedly ask for. **Ordering is deliberate: #1 is the only one that attacks the
insight above; the rest are efficiency on things you already do. Given that insight, resist building more
than these.**

### 1. Direction-preflight (feasibility gate) — build this FIRST
- **What:** a structured pre-commitment check that runs the three envelope questions
  (released-SOTA reproducibility · phenomenon/headroom oracle probe on the real benchmark · ≤4h/2×4090 fit)
  and returns GO / NO-GO with cheap evidence for each, routed through one external-brain + MoA review,
  **before any setup**.
- **Why it is the highest-value skill you could own:** it converts the single most expensive recurring
  mistake — entering a structurally-dead direction — into an hours-long gate. It is the operational form of
  the Part-1 insight.
- **When:** every time the heading changes or a new substrate is proposed, before environment work. The gate
  the aerial, water, C5, and MM-OVSeg campaigns each needed and didn't have.

### 2. Campaign-redirect
- **What:** the coherent heading-flip ritual — update all canonical direction docs together (CLAUDE.md §3,
  goal-directive under the 4000-char cap, README, memory index + topic-file statuses, the campaign RUNLOG
  banner), park (not delete) the old direction with a REOPEN-IF, carry the root lesson forward, then run the
  stale-ref guard to prove no doc still names the old heading as active.
- **Why:** you do this often (VLA→optical-SAR→VLA in one session alone), and it is demonstrably error-prone —
  doc-drift is a documented recurring failure in your own audits, and even this session's redirect produced a
  duplicate memory line and two over-budget trims. A checklist skill makes it mechanical and drift-proof.
- **When:** any time the user redirects the active domain.

### 3. Research-OS drift & latent-issue audit
- **What:** the audit you kept asking for this session — cross-check the live pipeline against its own
  principles + campaign history; surface enforcement gaps (rules that exist but aren't invoked), stale
  routers, unwired guards, missing methodological axes; output a ranked findings doc with fix-now vs accept.
- **Why:** you request this shape repeatedly ("refine the workflow docs," "assess latent issues," "identify
  missing angles"); it is how the system stays honest between campaigns. Packaging fixes the variance — each
  audit currently re-derives its own method.
- **When:** after any consolidation, before an autonomous launch, periodically. **Caveat consistent with the
  insight:** cap its cadence — this is the skill most capable of becoming the procrastination engine, so it
  fires on a trigger, not on a whim.

### 4. Reproduce-first substrate onboarding
- **What:** the STEP-ZERO ritual — env inventory → released-checkpoint presence check → **small smoke,
  abort-on-fail** → reproduce the published number within tolerance → phenomenon/failure-shape gate — each
  step writing a marker the existing `tools/guards/` already consume.
- **Why:** it mechanizes your #1 recurring root lesson ("reproduce+validate the real SOTA as step zero; we
  inverted it"), re-learned across multiple campaigns, plus the abort-on-fail discipline from today. A skill
  makes the lesson unskippable instead of a paragraph re-written each time.
- **When:** entering any new substrate, immediately after the feasibility gate says GO.

### Not worth a standalone skill
- **Memory curation** — fold into #2 (campaign-redirect).
- **MoA dispatch / reconcile** — already scripted (`moa/moa_panel.sh` + `moa/router-protocol.md`).

---

## Recommendation
Build **only #1 (direction-preflight) now**, and live with it across a few real direction decisions before
adding the others — precisely because the Part-1 insight says the reflex is to over-invest in the machinery.
The other three are genuine efficiency wins, but they are not the constraint.
