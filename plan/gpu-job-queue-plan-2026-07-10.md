# GPU Job-Queue (+ one autonomous guard) — Plan (2026-07-10)

> Comet-artifact structure (Proposal / Design / Tasks), but built directly — Comet's human-in-loop workflow
> was declined for autonomous `/goal` execution (see `plan/comet-adoption-plugin-cleanup-2026-07-09.md` §… +
> `plan/phase1-refactor-review-2026-07-10.md`). Comet = reference/planning only. `/goal` stays the driver.

## Proposal (Why + What)

**Why.** Two failures the telemetry made concrete:
- **GPU underutilization.** 2× RTX 4090D, but jobs run unbalanced: when GPU0's job finishes it **idles** while
  GPU1 keeps training — no scheduler pulls the next job onto the freed GPU. The Monitor *watches* one job; it
  does not *schedule* across GPUs. (Both GPUs idle right now = zero experiments running.)
- **`exp-verify` = 0 ever.** No experiment has been verified across the whole project. The imminent MM-OVSeg
  reproduction MUST run utilized AND pass `/exp-verify` (0→1).

**What.** A tiny **autonomous** GPU job-queue that keeps both 4090Ds busy, plus **one** folded-in autonomous
guard (the `①` collapse): *no `/adversary` without a prior `/exp-verify` VERIFIED artifact*. No Comet install;
`/goal` submits jobs + reads status.

**Non-goals.**
- NOT a distributed / multi-node / multi-user scheduler.
- NOT Coral (③, deferred to method-search — Coral is a grader-driven optimization engine, wrong shape for raw
  GPU scheduling).
- NOT the Comet harness (declined: human-in-loop blocking gates ≠ autonomous `/goal`).
- NOT a method-search / hyperparameter optimizer (that's ③).
- NO persistent multi-tenant daemon in v1 (batch mode first; daemon only if streaming submission is needed).

**Acceptance (the bound that keeps this honest).**
1. When ≥2 jobs are queued, **both GPUs stay busy** — no GPU idles while a job waits.
2. Each job is pinned to one GPU, logged, and hard-killed at the 6h cap (CLAUDE.md rule 2).
3. The MM-OVSeg reproduction runs *through the queue* and then passes `/exp-verify` (**0→1**) — the real test.
4. The guard **blocks** any `/adversary` that lacks a prior `/exp-verify` VERIFIED artifact (autonomous PASS/FAIL).

## Design (How)

**`tools/gpu_queue.py`** (python stdlib only; ~100 lines):
- **`gpu_queue.py run <job.sh> [<job.sh> …]`** — 2 worker slots bound to GPU 0 and GPU 1. Loop: while jobs remain
  or slots busy → when a slot is free and the queue is non-empty, pop the next job and launch
  `CUDA_VISIBLE_DEVICES=<g> setsid bash <job.sh>`, detached, logging to `logs/<job>.<ts>.log`; record
  `{gpu, pid, job, start}` in `gpu_queue_state.json`. On slot free → pull next. **6h hard cap per job**
  (SIGTERM→SIGKILL). Exit when queue empty + both slots idle; print a summary (per-job exit code, duration,
  last log lines).
- **`gpu_queue.py status`** — read `gpu_queue_state.json` → per-GPU `{idle | running <job> <elapsed>}` +
  queued count + recent completions. This is what the `/goal` parent polls (Monitor discipline: parent owns the
  wait via status polls; the queue is the scheduler, not a blocking call).
- **Autonomous-safe:** no human interaction; survives session boundaries (detached, `wget -c`-style resumable
  jobs where applicable); logs + state json are the source of truth.
- **GPU policy:** honor CLAUDE.md rule 2 as a soft hint (heavy→GPU1, light→GPU0) but the core job is just "keep
  both busy"; single-train ≤4h target / 6h hard cap enforced per job.

**`tools/guards/no_adversary_without_expverify.sh`** (the `①` collapse, autonomous):
- Given a node/claim id, check for an `/exp-verify` VERIFIED artifact (a sealed marker file the exp-verify step
  writes). `exit 0` = PASS (proceed), `exit 1` = BLOCK. No human pause. `/goal` calls it before `/adversary`.
- Optional (thin): a `.research-state.json` (Arbor-adjacent external state) recording
  `{campaign, active_phase, prereg_sealed, expverify_status}` the `/goal` loop reads at gate boundaries — the
  ONLY Comet-pattern survivor, and only if it earns its keep over the guard alone.

```
   /goal loop  ──submit batch──▶  gpu_queue.py run   ─pin CVD=0/1─▶  GPU0 ▓▓▓  (next job pulled on free)
      │         ◀──status poll───                    ─────────────▶  GPU1 ▓▓▓
      │
      └─ before /adversary ──▶ guard: exp-verify VERIFIED artifact? ── PASS→proceed / BLOCK→run /exp-verify first
```

## Tasks

- [ ] **T1** Write `tools/gpu_queue.py` (`run` + `status`; 2 slots; CUDA pinning; 6h cap; logs + state json).
- [ ] **T2** Smoke test: 3 trivial jobs (`sleep`+`nvidia-smi` echo) across 2 GPUs → verify both slots used, no
      idle-while-queued, accurate `status`, and the cap logic (test with a short cap). *Autonomous, no GPU-heavy run.*
- [ ] **T3** Write `tools/guards/no_adversary_without_expverify.sh` (+ optional `.research-state.json`);
      autonomous PASS/FAIL.
- [ ] **T4** Wire-in: one paragraph in CLAUDE.md/operating-manual — `/goal` submits training via `gpu_queue`,
      calls the guard before `/adversary`.
- [ ] **T5 (the acceptance test)** When MM-OVSeg assets are ready: run the reproduction *through* `gpu_queue`,
      keeping both GPUs busy, then `/exp-verify` it (**0→1**).

## Deferred / declined
- **① full Comet harness** — declined (human-in-loop ≠ autonomous). Collapsed to the one guard in T3.
- **③ Coral** — deferred to the method-search phase (grader = the `/prereg` sealed eval), evaluated only after a
  reproduced baseline exists.
