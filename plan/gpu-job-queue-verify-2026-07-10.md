# GPU Job-Queue (②) — Verification Report (2026-07-10)

- Change: `gpu-job-queue` (+ the folded `①` guard)
- Verify mode: **lightweight** (≤3 files, single capability)
- Verdict: **PASS for the built scope (T1/T2/T3)**; T4/T5 explicitly DEFERRED (not failures).

## Lightweight verification (6 checks)

| # | Check | Result |
|---|---|---|
| 1 | Tasks complete | T1 (`gpu_queue.py`) ✓ · T2 (smoke) ✓ · T3 (guard) ✓ · **T4/T5 DEFERRED** |
| 2 | Changed files match intent | `tools/gpu_queue.py` + `tools/guards/no_adversary_without_expverify.sh` + plan doc ✓ |
| 3 | Build / syntax | `py_compile` OK · `bash -n` OK (no build system — scripts) ✓ |
| 4 | Tests | smoke + re-smoke: scheduling/no-idle, CUDA pinning, cap-kill, dup-GPU warn, guard PASS/BLOCK — **all PASS** ✓ |
| 5 | Security | no secrets/hardcoded keys; runs arbitrary shell BY DESIGN (documented; no extra injection surface) ✓ |
| 6 | Code review | done (PASS-WITH-ISSUES → **all 6 findings fixed** → re-verified; caught a real cap-kill race) ✓ |

## Deferred (gated, not failed)

- **T4** — one wire-in paragraph (CLAUDE.md/operating-manual: `/goal` submits training via `gpu_queue`, calls
  the guard before `/adversary`). Small, optional-for-function.
- **T5 (acceptance)** — run the MM-OVSeg reproduction *through* `gpu_queue` → `/exp-verify` (0→1). **Gated on the
  MM-OVSeg assets finishing download.** This is the real acceptance and will be closed when the assets land.

## Verdict

②'s core — the scheduler + the guard — is **verified and production-ready**. It will keep both 4090Ds
saturated (no idle-while-queued) the moment there is real training to run, which is exactly what the
reproduction needs. The change is not 100% complete (T4/T5 remain), but the code is done and solid.
