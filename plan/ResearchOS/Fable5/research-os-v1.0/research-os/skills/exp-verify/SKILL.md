---
name: exp-verify
description: Verify a run is REAL before its numbers are trusted — structural (no mock/hardcoded result, intervention path reachable) → execution (exit 0, artifact exists, intended data consumed) → anti-no-op (the intervention provably FIRED and changed state vs baseline). Run after every dispatch; a claim-bearing run must be VERIFIED before /adversary.
version: 1.0.0
tags: [Infrastructure, Verification, AntiNoOp]
dependencies: []
---

# Exp-Verify — the run must be real before the number means anything

A cheap mechanical check between "the script finished" and "the number counts." It judges whether the
**run** was real; `/adversary` judges whether the effect and claim are.

## Three stages (stop at the first hard FAIL)
1. **Structural (static).** No mock / stub / hardcoded result (`return 0.95`, fixtures as outputs).
   The intervention path is actually reachable on the evaluated path. All declared inputs are consumed —
   no dead args that make the run independent of the variable under study.
2. **Execution.** Exit 0 on the real data path. The expected artifact exists and is non-empty. The
   intended split was actually read — not a cached skip-if-exists returning a stale result (fresh-run
   marker / timestamp / row count).
3. **Anti-no-op + plausibility (the key stage).** Evidence the intervention **fired and changed state**:
   a logged counter/diff showing the new path executed and the output differs from baseline in the
   expected way. Numbers not degenerate: not exactly 0.0 / 1.0 / NaN, not baseline-identical to many
   decimals — suspicious-perfect is guilty until explained.

Verdict: `VERIFIED` · `FAILED-STRUCTURAL` · `FAILED-EXECUTION` · `FAILED-NOOP` · `FAILED-PLAUSIBILITY`,
with per-stage evidence.

## Critical rules
- **A no-op intervention FAILS even if the metric improved** — "on vs off changes nothing at runtime" is
  the single most important catch.
- `VERIFIED` means "real run", NOT "real effect" and NOT "claim stands" — the claim still faces
  `/adversary`; a null still owes an `/autopsy`.
- A FAIL here is a boring failure: fix and re-run; nothing gets banked.

## Write-through
The eval runs via Arbor `eval_run` (score recorded from actual output); this gate stands between that
score and anyone trusting it. Verdict → the node insight; a fail keeps `eval_status = failed_to_run`.
