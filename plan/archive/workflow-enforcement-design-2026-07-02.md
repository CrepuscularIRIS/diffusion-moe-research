# Workflow Enforcement Redesign — the Monitor-anchored launch gate

> **Status: DESIGN (approved shape, not yet implemented).** For the next task: the VLA-era rewrite of
> `goal-directive.md` + `operating-manual.md`. This session did NOT modify either — it only backed up
> `plan/` (`backups/plan-backup-2026-07-02_pre-VLA-rewrite.tar.gz`) and settled this design.
> Source: Fable5's 2026-07-02 retrospective (`plan/retrospective-workflow-audit-2026-07-02.md`) +
> this brainstorming session. 大道至简 — no new gates; enforce the ones that exist.

## 1. The problem (Fable5's diagnosis — enforcement, not content)

The DSpark/DiffusionMoE machinery's **content was sound; every violated rule already existed**
(ceiling-probe-first, `/irreversible-decision-audit` before big runs, ≤12h cap, `nvidia-smi` first,
read-from-artifact). They lost to **momentum at the hot moment**. Concretely:
- `/prereg` fired 1 of ≥4 claim-bearing runs; `/exp-verify`/`/adversary`/`/compass`/`/artifact-acceptance`
  effectively never fired.
- ~5–6 GPU·h wasted vs ~3 informative: trained before the probe; launched a from-scratch run with a ~41h
  ETA against a ≤12h cap (no ETA-arithmetic step); **ignored a decisive step-500 kill signal (1.63 vs 6.16)
  and restarted from step 0** (~90 min); used unbatched HF `.generate` (0.1 samp/s) where vLLM is 20–50×.
- Public archive shipped **wrong numbers** — baselines back-computed from a mis-remembered average; same
  author/hour was correct when *reading the JSON*, wrong when *writing from memory*.

**Two root causes:** (a) rules-in-prompts lose to momentum; (b) write-from-memory vs read-from-artifact.

## 2. The principle (Fable5's angle — the thing to carry forward)

**Bind the action to its precondition; don't add another rule to remember.** Make the existing rules
*fire* at the hot moment structurally. Read numbers from artifact files, never from context memory.

## 3. The decision

A **Monitor-anchored launch gate** — procedural (a forced ritual), with a **Monitor** as its teeth.
**No blocking hooks** (they conflict with the existing global hook stack + are unstable). **No new gates.**
**Scope: every long-running dispatch (GPU training AND any job with ETA > 30 min** — data generation, large
eval, downloads).

### 3.1 The launch ritual (for any >30-min dispatch)
1. Fill the `/prereg` **launch-arithmetic** block:
   - `ETA vs ≤cap` (compute the ETA; if ETA > cap → do not launch, RESCOPE).
   - `data-sufficiency ratio` = samples ÷ the baseline's training volume (a tiny ratio predicts failure —
     the from-scratch 4.5K-vs-500K case would have been caught here).
   - `kill-checkpoint {step_or_metric, threshold, action=KILL}` — the decisive early signal.
   - `resume-failure = STOP` (a resume error never silently restarts from 0).
2. **Arm a Monitor** on the job's log, `grep -E --line-buffered` covering **{progress metric | kill-threshold
   crossing | `Traceback|resume-failed|OOM|Killed|FAILED`}** (coverage rule: silence ≠ success — the filter
   must match every terminal state, not just the happy path).
3. Dispatch.

### 3.2 Why the Monitor is the forcing function (and why it beats a hook here)
- You **cannot write the Monitor filter without the kill-checkpoint threshold** → the launch-arithmetic is
  forced as a precondition of arming, not as a remembered rule.
- Once armed, the Monitor **re-invokes the agent the moment the metric crosses the threshold** — even after
  attention has moved on. The two worst DSpark failures (ignored kill signal + resume-restart) become
  structurally impossible.
- It is **agent-armed, per-run** → **zero conflict** with the global hook stack (the reason a `PreToolUse`
  blocking hook is rejected here).

### 3.3 Number-drift (the artifact-fidelity half)
- **`eval_run`** is the structural antidote: scores flow from the actual command output into the Arbor tree
  with no human transcription. ADOPT NOW (was deferred in §6.3).
- **`/artifact-acceptance`** fires at the public/GitHub handoff (its designed moment).
- **Rule (read-from-artifact):** no number ships in any report/README/claim that was not read from an
  artifact file *this session*. Merge executor worktrees before archiving (the stranded Qwen3-4B artifact
  was invisible to the archive → conflated report).

### 3.4 `/compass` cadence + GPU
- `/compass` trigger = the countable **"after every 2nd `/autopsy`"** (already set); optional `cron`
  heartbeat as a wall-clock backstop only.
- GPU concurrency is **platform-scoped** (already fixed): 4B/8B-class = one job per GPU, pair
  candidate+control across the two 4090Ds (an idle 2nd GPU mid-campaign is a bug).

## 4. Mechanism reference (why each was chosen or rejected)

| Mechanism | What it is | Conflict risk | Use here |
|---|---|---|---|
| **Hook** | auto, event-triggered on tool calls/lifecycle; can BLOCK | HIGH (global stack) | **rejected** |
| **Monitor** | agent-armed watcher on a command's stdout; each line re-invokes the agent; per-run | none | **kill-checkpoint / resume / OOM** — the teeth |
| **Cron / ScheduleWakeup** | re-runs a *prompt* on a schedule/delay; polls | low | wall-clock backstop only (`/compass` heartbeat; a launch+cap one-shot KILL reminder) |
| **Procedural gate** | forced ritual (fill the launch-checklist before dispatch) | none | the launch-arithmetic `/prereg` |
| **Prose** | a rule in the doc | none | the floor; loses to momentum alone |

## 5. The one-line binding for the goal-directive (what the next task must weave in)
> **No long-running dispatch (>30 min or any GPU train) without (a) a `/prereg` carrying the
> launch-arithmetic block AND (b) an armed Monitor on its kill-checkpoint.** One binding covers most of what
> failed in DSpark.

## 6. Carry-over research discipline (not enforcement, but same lesson)
Probe-first: run the cheap decomposition *before* building the method. DSpark's ceiling-probe = VLA's
"is the failure actually **fusion-limited** vs grounding/head?" — run it before building the fusion adapter,
or the method half is mis-aimed.

## 7. Keep (do not touch — these worked)
Pro-designed candidates · the DPC falsify-before-build pattern · the conversion law (every null emits a next
candidate) · campaign-1's pre-GPU occupancy kills · the one invariant (proposer = DOWN verdicts only).

## 8. Open for the next task
- Weave §3 + §5 into the rewritten `goal-directive.md` (VLA) and `operating-manual.md` (§2/§4/§5).
- The VLA *research* plan (Papers A/B, StarVLA+LIBERO-Plus) is a separate thread in `VLA/*.md`; its
  outstanding gate is the GAF-VLA occupancy check vs ST4VLA + 2026-Q2 (route to Pro) — independent of this
  enforcement design.
