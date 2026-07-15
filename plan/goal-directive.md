<!-- /goal CONTRACT — `conductor` reads this turn 1. Load conductor FIRST: it owns the loop, four gates,
     engine division, value bar, invariants — this file does NOT restate them, only WHAT + live state.
     Full bindings mirrored in CLAUDE.md §2; only non-obvious load-bearing ones repeated below. -->
---
OBJECTIVE: research competitive at top-tier **Information Sciences** + **AAAI**. Contribution = the
decision-relevant scientific claim; the world model is the vehicle. Submission/publication = human.
DELIVERABLE (2026-07-14): a **CONTRIBUTION-COMPLETE package** — a computable construct, a held-out-
validated predictor, OR an intervention beating fair baselines, plus the honest evidence map (all
prerequisites for a paper, NOT the paper). EVIDENCE-COMPLETE (characterization only) ≠ done; mature
abstract+conclusion only at package P(success) ≥ ~0.85 (ledger row).
NON-GOALS: reproduction-only results; benchmark deltas on saturated slices that change no decision;
certificates/diagnostics that gate nothing; manuscript polish before contribution-completeness.
DECISION-CHANGE: a WM practitioner's choice between adaptation/monitoring strategies moves because of
the claim — no decision moves ⇒ the result does not count.

DOMAIN — **WORLD MODELS, CLEAN RESTART (2026-07-15), purpose = exercise the rebuilt /prospect:**
cold-start a NEW empty Arbor run `world-model-v3` (fresh root node, expanded independently; do NOT
resume `world-model` or `world-model-v2` — both archived). Begin at **/prospect**, re-ideate from zero;
first move = RECALL (memory + ledger lessons + domain banks) → /prospect. This EVALUATES the new
prospecting process (Mine 7 incumbent-algorithm autopsy · selection jury · JURY-MODE · refine ·
micro-pilot → /admit), NOT a repeat of completed work.
**REPRODUCTION IS DONE — SKIP IT:** baselines reproduced + frozen at `/data/projects/world-model-lab/
logs/step0/*/latest.pt` (R2-Dreamer · TD-MPC2 · DreamerV3) — INVENTORY and REUSE, never re-reproduce or
rebuild. Priors CARRIED: lessons L1–L10, `WorldModel/` operator+trick banks, `judgment/capabilities.md`
+ `taste-anchors.md`, reproduced envs. Archived `world-model`+`world-model-v2` runs (plans-of-record,
rows J1–J12) READ-ONLY — the re-anchoring, contact-mode, and v2 consistency-collapse threads are
REGION-CLOSED / PARKED, do not reopen.

BINDINGS (full set = CLAUDE.md §2; non-obvious load-bearing only):
- env `/data/projects/world-model-lab/` — USER-MANAGED, holds it ALL: `papers/` (精读) · `datasets/` ·
  `checkpoints/` + `logs/step0/*/latest.pt` (frozen R2-Dreamer · TD-MPC2 · DreamerV3). Inventory FIRST;
  REUSE the frozen `.pt`, never rebuild; new large datasets/checkpoints need approval.
- hardware 2×4090D 48GB (GPU1 preferred, both concurrent); compute priced, never hard-capped.
- engines: conductor=Opus · executors=Sonnet (worktrees) · external brain=GPT-5.6 browser (review +
  arXiv search) · reviewer=Grok (claims + code review) · MoA panel = 5 families multi-instance
  (`moa/router-protocol.md`; codex = forensic lane for autopsy/abduce). Reach for external brain / MoA /
  reviewer on irreversible forks; tactical forks decided by MoA, never escalated to human; keys in `.env`.

SKILL INVOCATION (pointer manifest, reinforces conductor §5 — NOT restated mechanics): sub-skills must
be LOADED via the Skill tool the moment their trigger fires, never improvised — improvising = the
discipline silently never fires. Triggers→loads: `ledger` (recall · every forecast call · 验收 resolve ·
pulse) · `abduce` (every backward inference / autopsy why) · `tricks` (probe/KILL/BRACKET by symptom) ·
`operate` (every dispatch/launch/wait/kill) · `externalize` (re-entry · tree write-through) · gate skills
`prospect`·`forge`·`admit`·`prereg`·`exp-verify`·`adversary`. Mechanics stay in the skills (DRY).

CONSTRAINT: statistical floor for DMC-class benches — ≥5 seeds + paired stats (rliable-IQM).
