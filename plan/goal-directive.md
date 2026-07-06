<!-- Paste everything below the `---` after `/goal`. Body is <4000 chars. GOAL = boundaries + pointers + hard
     stops ONLY. PROCESS is NOT here — it is enforced in the ACTIVE surfaces (§ bottom), loaded when they run. -->
---
AMBITION: produce ONE genuine 一区 contribution (Information Fusion / ESWA). Direction self-selected. Improvement
(刷分) is PRIMARY; systems / compression / novelty OK — name the TYPE first. Contribution is human-granted.

**8 HARD CONSTRAINTS** (this doc carries ONLY these + the pointers; `/goal` guarantees you keep running, NOT that
you obey prose — so the PROCESS lives in the ACTIVE SURFACES below, enforced when each skill/script runs):

1. **AUTONOMY.** Opus DECIDES every fork + REPORTS; subagents EXECUTE; Pro ASSISTS design (never decides). NEVER
   pause the loop to ask — decide + report. Ask ONLY a genuine user-only call (new hardware · external publish · venue).
2. **DOMAIN LOCK.** 刷分 = Aerial VLN; datasets LOCKED to `VLA/aerial-vln-inventory-2026-07-05.md`. Outside the
   inventory / a far-domain jump = STOP-to-ask. Innovation = the MECHANISM on a local bench, NOT dataset-hopping.
3. **LIVE STATE.** `tree_view(run_name=aerial-vln)` FIRST at start + every 验收 — the Arbor tree is the CANONICAL
   current-node state. Update the tree FIRST at 验收, then RUNLOG. (Head/atlas = `openbuild/aerial/`.)
4. **COMPUTE.** 2×4090D. SINGLE-RUN TRAIN ≤4h target / 6h HARD cap (Monitor-kill; ETA>4h ⇒ CUT COST, don't run).
   Method = WHATEVER fits (frozen VLM ≤32B-4bit · LoRA), NOT pretraining. SCOPE-EXPAND {bigger VLM · LoRA base} =
   DECIDE, never ask.
5. **PIPELINE.** research-os v1.1: `/prospect → /forge → /prereg → run → /exp-verify → /adversary → /autopsy`.
   Each command's PROCESS (MoA-chain · operator-retrieval · self-attack · region-close) is ENFORCED IN its SKILL,
   loaded when it runs — NOT in this doc. RUN the pipeline; the skills carry the how.
6. **VALUE BAR / ANTI-RETREAT.** A BIG, honest, falsifiable Δ on a HARD, field-open problem. Occupancy RE-PRICES
   ("done" ⇒ BEAT it), never vetoes. NEVER incremental / certificate / retreat.
7. **THE ONE INVARIANT.** NUMBERS FROM ARTIFACTS; `/prereg` seals claim-runs; proposer self-grants DOWN only;
   CLAIM_STANDS = independent substrate (the Codex hook); contribution = human.
8. **HARD STOP.** STOP_AND_REPORT ONLY for a user-only call. refuted ⇒ a cheap_probe auto-ROUTES
   problemshift-vs-lateral (never ask). REGION-CLOSE ONLY when ≥2 mechanisms hit the SAME root ⇒ genuine lateral
   (atlas epitaph), not a neighbor.

**ACTIVE SURFACES — where the process is ENFORCED (the goal only points here):** skills `/prospect·/forge·/prereg·
/exp-verify·/adversary·/autopsy` (each loaded at invocation) · MoA `moa/moa_chain.sh` + `moa/router-protocol.md`
(5-Q chain · self-attack · reversibility tiering) · the Arbor tree (`aerial-vln`, node state) · `openbuild/aerial/atlas/`
(failure atlas + operator bank) · CLAUDE.md rules 6-10 (standing reference, weakest — do not rely on it alone).

WAIT: Monitor / Bash bg-wait (wait = design the next node), never ScheduleWakeup-poll; Pro poll 15-min. Keys `.env`.
