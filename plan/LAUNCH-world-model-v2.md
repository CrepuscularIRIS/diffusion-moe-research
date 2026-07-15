# LAUNCH — World Models v2 (research-os v4.0 "Four Gates")

**How to use:** open a fresh Claude Code session in `/home/lingxufeng/huggingface`, then copy the ONE
line inside the code block below and paste it as your message. That is the built-in `/goal` condition —
it bootstraps the `conductor` skill (research-os plugin), which reads the full contract in
`plan/goal-directive.md` and drives the campaign autonomously. Do NOT paste this whole file; paste only
the code block.

> The condition is the only thing the main model sees verbatim on turn 1. Everything else — the loop,
> the four gates, the engine division, the value bar, the invariants — lives in the `conductor` skill +
> `plan/goal-directive.md`, which the conductor reads on turn 1. Keep the condition short; it just
> bootstraps + anchors the run + encodes the stop-gate.

```
/goal Load and use the `conductor` skill, then read plan/goal-directive.md as the full contract and follow it. This is a FRESH restart of the WORLD MODELS direction toward top-tier Information Sciences + AAAI — cold-start a NEW empty Arbor run `world-model-v2` (do NOT resume the archived `world-model` run) and begin immediately at /prospect, re-ideating from zero. Run the research-os v4.0 loop: SELECT (prospect → admit GATE-0: the six admission checks + one-pager before ANY direction-scale or GPU-training commitment) then SOLVE (forge → prereg → run → exp-verify → {claim ⇒ adversary → me | null ⇒ autopsy}); hunches and cheap probes stay FREE below the admit gate. Executors = Sonnet subagents in worktrees; keep the methodological lessons in judgment/lessons.md and the WorldModel/ banks as priors; inventory /data/projects/world-model-lab/ before rebuilding anything (envs already reproduced). STOP and return to me ONLY at a HUMAN decision — a claim ready for contribution/publication, a large-resource / destructive / field-level fork, or a stall the ledger cannot resolve; otherwise keep driving the loop without pausing for confirmation.
```

---

## What happens after you paste it

1. **Turn 1** — the conductor loads, runs its session protocol (RECALL project memory + ledger lessons +
   `tree_view(fmt="constraints")` + domain banks → INVENTORY the env → orient in the tree), and, finding
   a cold start, enters `/prospect`.
2. **SELECT loop** — `/prospect` mines problems (external frontier scan first, then capability bank,
   own-log anomalies, literature, benchmark critique) → 3–7 four-field cards → a candidate heading toward
   direction-scale spend exits to **`/admit`** (GATE 0): SOTA-verified · magnitude · goal-variance ·
   substrate-mechanics · occupancy · venue micro-review, plus the one-pager with three kill-first
   experiments. `/admit` **prices**, it does not veto — it only refuses to unlock GPU-scale spend for a
   direction no external venue review will clear, and surfaces the one-pager to you at GPU-scale.
3. **SOLVE loop** — `/forge` → `/prereg` (GATE 1) → run (Sonnet worktree executors) → `/exp-verify`
   (GATE 2, incl. the DESIGN-VALID layer) → `/adversary` (GATE 3) on a claim, else `/autopsy` on a null.
4. **It returns to you** only at the human-decision boundary named in the condition. Everything else —
   hunches, cheap probes, ideation, mechanism design — runs free between the gates.

## Notes
- Contract of record: `plan/goal-directive.md` (OBJECTIVE · NON-GOALS · DECISION-CHANGE · DOMAIN ·
  CONDUCT · BINDINGS · CONSTRAINT). Edit the DOMAIN there, not this launch string, when the direction
  changes.
- Bindings the conductor will honor: env `/data/projects/world-model-lab/` (user-managed, inventory
  first); hardware 2×4090D (GPU1 preferred, both concurrent); reviewer = Grok; external brain = GPT-5.6
  browser; MoA panel scripts in `moa/`; keys in `.env` (never committed).
- Backup of the pre-v4.0 pipeline: git tag `v3.7-pre-v4.0-backup` + `backups/pre-v4.0-2026-07-13/`.
