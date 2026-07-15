<!-- The /goal CONTRACT — the `conductor` skill reads this on turn 1. Copy-paste launch string + how-to
     = plan/LAUNCH-world-model-v2.md. Load `conductor` FIRST: it owns the loop, the four gates, the engine
     division, the value bar, and the invariants — this file does NOT restate them. It carries only WHAT +
     live state. Full bindings (all paths/hardware/keys) are mirrored in CLAUDE.md §2; only the non-obvious
     load-bearing ones are repeated below. -->
---
OBJECTIVE: research competitive at top-tier **Information Sciences** + **AAAI**. The contribution is the
decision-relevant scientific claim; the world model is the vehicle. Submission/publication = human.
DELIVERABLE (ruling 2026-07-14): a **CONTRIBUTION-COMPLETE experimental package** — a computable
construct, a held-out-validated predictor, or an intervention beating fair baselines, plus the honest
evidence map — i.e., all prerequisites for a paper, NOT the finished paper. EVIDENCE-COMPLETE
(characterization only) never counts as done; mature abstract+conclusion drafted only when the
package's forecast P(success) ≥ ~0.85 (ledger row).
NON-GOALS: reproduction-only results; benchmark deltas on saturated slices that change no decision;
certificates/diagnostics that gate nothing; manuscript polishing before contribution-completeness.
DECISION-CHANGE: a WM practitioner's choice between adaptation/monitoring strategies moves because of the
claim — if no decision moves, the result does not count.

DOMAIN — **WORLD MODELS, FRESH RESTART (2026-07-13):** cold-start a NEW empty Arbor run `world-model-v2`
(do NOT resume the archived `world-model` run); begin at **/prospect**, re-ideate from zero. First move =
RECALL (memory + ledger lessons + domain banks) → /prospect. Priors CARRIED, not reset: the methodology
lessons, the `WorldModel/` operator+trick banks, and the already-reproduced envs (inventory before
rebuilding). Archived history (the old `world-model` run + its plan-of-record + forecast rows J1–J12) is
READ-ONLY — scan only to avoid re-litigating a dead slice; the re-anchoring and contact-mode threads are
REGION-CLOSED, do not reopen.

BINDINGS (full set = CLAUDE.md §2; only the non-obvious load-bearing ones here):
- env `/data/projects/world-model-lab/` — USER-MANAGED, holds it ALL: `papers/` (精读 source) ·
  `datasets/` · `checkpoints/` + `logs/step0/*/latest.pt` (the frozen reproduced R2-Dreamer · TD-MPC2 ·
  DreamerV3 ckpts). Inventory FIRST; REUSE the frozen `.pt`, never re-reproduce or rebuild what exists;
  new large datasets/checkpoints need approval.
- hardware 2×4090D 48GB (GPU1 preferred, both concurrent); compute priced, never hard-capped.
- engines: conductor=Opus · executors=Sonnet (worktrees) · external brain=GPT-5.6 browser (review +
  arXiv search) · reviewer=Grok (claims + implementation-level code review) · MoA panel = 5 families
  multi-instance (`moa/router-protocol.md`; codex = forensic lane for autopsy/abduce only). The skills
  surface these — reach for external brain / MoA / reviewer on irreversible forks; tactical forks are
  decided by MoA, never escalated to the human; keys in `.env` (never commit).

SKILL INVOCATION (belt-and-suspenders with conductor §5 — a pointer manifest, NOT restated mechanics):
the loop's mechanics live in sub-skills that must be LOADED via the Skill tool the moment their trigger
fires, never improvised from the conductor's summary — improvising = the discipline silently never
fires. Binding triggers→loads: `ledger` (goal-start recall · every forecast-bearing call · 验收
resolution · pulse curation) · `abduce` (every backward inference / `/autopsy` why / latent-root) ·
`tricks` (probe/KILL/BRACKET design, retrieved by symptom) · `operate` (every dispatch/launch/wait/kill)
· `externalize` (re-entry after compaction · tree write-through) · the gate/loop skills `prospect` ·
`forge` · `admit` · `prereg` · `exp-verify` · `adversary`. Mechanics stay in the skills (DRY); this line
only guarantees they get loaded.

CONSTRAINT: statistical floor for DMC-class benches — ≥5 seeds + paired stats (rliable-IQM).
