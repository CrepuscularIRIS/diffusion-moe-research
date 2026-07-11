# Phase-1 Refactor — Execution Record + Review + Remaining Plan (2026-07-10)

> Companion to `plan/workflow-audit-2026-07-09.md`, `plan/runtime-harness-decision-2026-07-09.md`,
> `plan/comet-adoption-plugin-cleanup-2026-07-09.md`. This records what the Phase-1 "simplify" refactor
> actually did, the review that gated it, and what remains. **User supplements below in §6.**

## 1. Tasks executed (subagent-driven, audit after each)

| Task | Change | Review outcome |
|---|---|---|
| **T1** | Enforcement-hole fix: `adversary/SKILL.md` (+runtime) + `research-tooling-channels.md` + `research-operating-system.md` no longer name the DELETED Codex auto-hook as the `CLAIM_STANDS` substrate → context-free GPT-5.6 / agy-Gemini / human. `research-tooling-channels.md` fully rewritten (Sonnet-4.6 executors, GPT-5.6 one-lane, plugins-removed). | audit **PASS** |
| **T4** | `.claude/CLAUDE.md` (§1/§2/§4/§5/§6) + `moa/router-protocol.md` → GPT-5.6 **one lane, 3 roles** (search+triage · claim-review · workflow-exec); codex plugin GONE (`/codex:rescue` dropped); file-memory SOLE layer (agentmemory MCP disconnected). | audit **FAIL → 10 residuals fixed** (5 flagged + 5 self-caught bare-`Pro`) → re-verified CLEAN |
| **T2** | `openbuild/auto_trust/DATA_ASSETS.md` VLA "CURRENT MAINLINE" → ARCHIVED + optical-SAR redirect banner. | self-verified CLEAN |

## 2. Cross-file code review — VERDICT: PASS-WITH-ISSUES (both issues fixed)

The 6 changed files tell ONE coherent story (GPT-5.6/codex-gone/Sonnet-4.6/optical-SAR-active); invariant + MoA
roster intact; no stale-as-active defects within them. Two issues it caught, now FIXED:
- 🔴 **CRITICAL** — CLAUDE.md §4/§7 pointed to `plan/ai-research-conduct-principles.md`, which had been **deleted**
  (unstaged working-tree deletion). It is the science protocol (falsifier-before-dispatch, sealed evals) — load-bearing.
  **Restored from git** (143 lines); all pointers (CLAUDE.md + README) resolve.
- 🟠 **HIGH** — `plan/goal-directive.md` (the active `/goal` input) still routed escalation to `/codex:rescue`
  (lines 10, 41) → fixed to context-free GPT-5.6 / agy-Gemini. Body 3455/4000.

## 3. NEW FINDING — skill-usage telemetry (2026-07-10)

`prospect 5× · forge 5× · prereg 7× · autopsy 11× · adversary 2×` — but **`exp-verify` NEVER used**, and
`find-skills` never used.
- `find-skills` unused = **fine** (utility skill, not part of the loop).
- **`exp-verify` = 0 is the process-over-product breaker, QUANTIFIED.** It is the only command that requires an
  actually-executed run with real artifacts. Zero uses ⇒ **no experiment has ever been verified** across the whole
  project history, while ideation/contract/autopsy ceremony fired 28×. Moreover `adversary` (2×) *requires* a prior
  `/exp-verify VERIFIED` per its own contract → it fired **without the gate it depends on** = the unenforced
  gate-ordering both audits flagged.
- **Actionable:** (a) north-star = make `exp-verify` go 0→1 with a **real MM-OVSeg reproduction number**; (b) add the
  harness guard **"no `/adversary` without a prior `/exp-verify` VERIFIED artifact"** (already on the ~6-invariant
  list — now EVIDENCED as needed).

## 4. Remaining Phase-1 tasks

- **T4 DONE 2026-07-10 — gpu_queue + guards wired into CLAUDE.md via plan/sdd-pipeline-enforcement-2026-07-10.md**
- **T5** — rewrite/archive `plan/scouting/README.md` (still ranks TbV/OpenFly/C5 + dead data paths) for optical-SAR.
- **T6** — init an `optical-sar` Arbor session + point `.arbor/active-run` at it (currently `aerial-vln`; audit P0.1).
- **T7 (lower priority — reference/history, CLAUDE.md wins conflicts)** — `plan/operating-manual.md` §1 engine-stack +
  `plan/moa-advisor-panel-design-2026-07-04.md` still describe the old `Pro 扩展`/`超高`/Codex-Stop-gate stack.

## 5. Then — the actual work (not more pipeline)

Resolve the MM-OVSeg HF asset gate → run the reproduction → **`/exp-verify` it** (0→1). Everything above is the
enabling refactor; the deliverable is the verified reproduction number, not the harness.

## 6. User supplement
<!-- add below -->
