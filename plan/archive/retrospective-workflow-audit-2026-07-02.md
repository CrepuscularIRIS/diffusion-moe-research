# Retrospective Workflow Audit — 2026-07-02

> Abductive review of the three experiment bodies (`failed-experiments/`, `dspark-head-experiment/`,
> `diffusiongemma_sft/`) + both Arbor trees (`diffusion-moe`, `dspark-head`) + the goal machinery
> (`goal-directive.md`, `operating-manual.md`, research-os commands). Question: what do these
> campaigns reveal about workflow defects, and what is the minimal structural fix?

---

## 1. Timeline reconstruction (DSpark campaign, 2026-07-01 13:33 → 07-02 06:00, from file mtimes + logs)

| Time (EDT) | Event | Assessment |
|---|---|---|
| 07-01 ~13:33 | HOPE iter1–4 training (from-scratch; iter1 catastrophic, iter4 −4.8% w/ train/infer mismatch) | Ran BEFORE the ceiling probe, violating the goal's own "CEILING-PROBE first" heuristic #1 |
| 07-01 23:19 | Ceiling probe (baseline_profile.json) | The right first move — done ~10h late |
| 07-01 23:52 | Cache prep, 4506 samples | — |
| 07-02 ~00:00–01:15 | From-scratch RSMH (GPU0) + **vanilla Markov retrain (GPU1)** launched, 2810 steps; tree logged "ETA ~41h/experiment" | Launched despite (a) banked constraint 1.2 (from-scratch fails), (b) trivially computable data gap (4.5K vs the baseline's ~500K = 100× short), (c) §2's own ≤12h cap. Vanilla retrain answers nothing — the released checkpoint IS the vanilla baseline |
| 07-02 01:15 | step-500 eval: both at 1.63 vs 6.16 baseline | **Decisive kill information available here** |
| 07-02 ~01:16 | RSMH resume FAILED → training **restarted from step 0**; both GPUs kept burning | Kill info did not gate continuation; a resume failure was answered with a restart, not a stop |
| 07-02 02:49 | User intervened ("为什么我们要重新训练？杀死进程") → killed; warm-start RSMH launched | The pivot the loop should have made itself at 01:15 |
| 07-02 02:49–04:46 | RSMH warm-start (GPU0) + FIR warm-start (GPU1) in parallel; evals done | Correct execution: parallel GPUs, ~90 min each. Post-train inline eval crashed (init_process_group twice) — plumbing friction |
| 07-02 05:58 | Data regen with HF `.generate()` at **0.1 samples/s** (ETA 195 min for 2000); killed at 540 | Wrong tool — vLLM/batching is ~20–50× faster for this |
| 07-02 06:00 | confidence_sweep dir created, **empty**; user closed the direction | The cheap inference-time angle was reached last, after the compute was spent |

Wasted compute ≈ 5–6 GPU·h (from-scratch arc after its own kill signal + redundant vanilla retrain)
vs ~3 GPU·h of informative runs (probe + two warm-starts). The user's complaint ("3h 实验硬做成 8h")
is quantitatively accurate.

## 2. Findings (ranked by severity)

### F1 — CRITICAL: shipped numbers written from memory, not artifacts (+ stranded worktree artifacts)
The public `failed-experiments` reports 05–08 contained: (a) a flat "4.73" baseline for all three
benchmarks with per-benchmark absolutes **back-computed** from that average (real: 6.16/3.46/3.68);
(b) a DPC section that **conflated two separate runs**: the bundled artifact was the main-loop
Qwen2.5-7B probe (mean TV 0.380), while the quoted numbers ("Qwen3-4B", "28–31% TV", "E[τ] 3.09→6.00
= +94%") came from an executor-agent probe whose artifact sat in an **unmerged git worktree**
(`agent-acbc2b6863723fef8`), invisible to the archive — initially this audit itself concluded the
E[τ] probe "was never run" until the worktree search found it (recovered and bundled 2026-07-02);
(c) the "+94% E[τ] ceiling" framing was misleading regardless — 6.00 is the trivial perfect-acceptance
bound and 3.09 a marginalization proxy, while the real released head already achieves 6.16 on gsm8k.
Meanwhile `dspark-head-experiment/README.md`, written in the same session, had the warm-start numbers
RIGHT — because it was written from the JSONs. Root causes: **prose written from conversation memory
with nothing forcing a read-from-artifact at writing time**, and **executor worktrees not merged
before archiving** (their artifacts then only exist as context memories, which is how two runs
blended). `/artifact-acceptance` (built for exactly this handoff) never fired before the GitHub push.
**Status: corrected and pushed 2026-07-02 with CORRECTION notes + both DPC artifacts bundled.**

### F2 — Compute discipline: every failure was of a rule that already existed
- Goal heuristic said ceiling-probe FIRST → training ran first (10h).
- §2 caps say ≤3h dev / ≤12h sealed → a 41h-ETA run was launched with no ETA arithmetic step.
- The banked constraint (from-scratch fails) + one division (4.5K/500K) predicted the failure pre-launch.
- The step-500 checkpoint eval existed but gated nothing; a resume failure triggered restart-from-0.
- Redundant control: retraining vanilla Markov from scratch when the released checkpoint is the baseline.

### F3 — The discipline commands were mandated but skipped under momentum
Across the campaign: `/prereg` fired once (HOPE) out of ≥4 claim-bearing runs; `/exp-verify` left no
record; `/adversary` never ran (the −16% mechanism claim shipped with a KNOWN confound — tree 1.5
names "frozen-backbone conflict + data mismatch", the reports dropped the confound);
`/irreversible-decision-audit` did not fire before the compute-locking launches; `/compass` never
fired (~5 cycles in one day — it was due). The v0.5/v0.6 CONTENT is right; compliance is
memory-gated prompt-layer, and a hot loop loses to momentum.

### F4 — The cheap-angle ladder was designed but not walked
Tree 1.1.1 planned Probe C: offline acceptance replay with an oracle 2nd-order correction — the exact
"稍微换一个角度" experiment that measures the capture ceiling with ZERO training. It was skipped in
favor of training runs. The empty confidence_sweep (inference-time angle) came last, at closure.
Pattern: **the loop defaults to "train the thing" when a replay/oracle/reranking probe answers the
same question 100× cheaper.**

### F5 — Tree/memory hygiene at close-out
dspark-head node 1.1 left `in_progress` after campaign close; diffusion-moe left ~6 dangling
`in_progress/pending` nodes (5, 5.3, 5.3.1.1, 5.8.2, 5.10.2, 5.12…). Milder recurrence of the #1
process bug: statuses not reconciled at closure, and unverified numbers (phantom E[τ]) not purged.

### F6 — Stale platform assumptions
§2's "only ONE 26B GPU job at a time" (dLLM-era) silently persisted into the 4B campaign; GPU1 sat
idle until the user complained twice. GPU policy was never re-derived for the new platform.

### What WORKED (keep)
Pro-designed candidates (HOPE/RSMH/FIR/CLR) were genuinely better-shaped than local designs; the DPC
probe pattern (cheap falsifier before build) killed two dLLM directions at 0 GPU; the conversion law
emitted real next-candidates at every null; warm-start pivot executed cleanly once triggered;
campaign-1's occupancy/DPC gates blocked GPU pre-spend repeatedly ("NO GPU spent on intervention");
`diffusiongemma_sft/` has real tests; archives were produced at all (negative-result publication).

## 3. Abductive synthesis — two root causes explain all six findings

1. **Rules live in prompts; the loop runs on momentum.** F2, F3, F6: every violated rule already
   existed in goal-directive/§2/§5. A rule that requires remembering to invoke a command at a hot
   moment will be skipped exactly when it matters. Fix = attach the rule to an artifact the loop
   MUST touch anyway (the prereg file, the training launch, the git push), not to a separate command
   invocation.
2. **Write-from-memory instead of read-from-artifact.** F1, F5: numbers and statuses drift the moment
   prose is produced without a mechanical read of the source. The same session produced a correct
   table (read from JSON) and a fabricated one (recalled from context).

## 4. Improvements adopted (minimal — no new gates; v0.4 died of gate proliferation)

| # | Change | Where |
|---|---|---|
| I1 | **Artifact-fidelity rule**: every number in a shipped/banked doc is read from its artifact file at writing time, with the path cited per table; any push to a public remote REQUIRES `/artifact-acceptance` whose checklist now includes "recompute each number from its cited source" | op-manual §4 lesson 8 |
| I2 | **Launch arithmetic inside `/prereg`** (not a new command): measured sec/step × steps = ETA (>cap ⇒ redesign); data-sufficiency ratio vs the reference recipe; declared kill-checkpoint {step, threshold, action=KILL — a resume failure is a STOP, never a silent restart-from-0} | op-manual §4 lesson 9 |
| I3 | **Cheap-signal ladder**: for head/method work, the forge KILL experiment defaults to an inference-time replay/oracle probe when one exists; no training run before its oracle-replay upper bound is measured | op-manual §4 lesson 9 |
| I4 | **Platform-scoped GPU policy**: jobs-per-GPU derived from the CURRENT platform's memory footprint at campaign start; small-model campaigns pair candidate+control across both GPUs; generation-heavy steps use vLLM/batching, with samples/s measured in the first minute and abort if ETA > budget | op-manual §2 + §4 lesson 10 |
| I5 | **Close-out sweep**: on direction close, reconcile ALL descendant node statuses + purge any number lacking an artifact from tree/memory/reports | op-manual §6.2 |
| I6 | **/compass trigger hardening**: fires after every 2nd `/autopsy`, not "every 3–5 cycles" (which never fired) | op-manual §5.2 note |

## 5. Verdict on the goal machinery itself

- **goal-directive.md**: content sound — it already encoded ceiling-probe-first, the audit step, and
  GPU discipline. The defect is enforcement, not text. For the next (VLA) goal: keep the same
  skeleton; add one line binding TRAIN to "prereg-with-launch-arithmetic exists".
- **operating-manual.md**: two real defects fixed — the stale 1-GPU rule (§2) and the deferral of
  `eval_run`/`tree_set_meta` adoption (§6.3) which would have written scores into the tree
  mechanically (F1's structural antidote). Caps existed without an ETA-check step (fixed via I2).
- **research-os commands**: individually well-designed; none malfunctioned — they were NOT INVOKED.
  The failure mode is trigger design (descriptive "fires when…" prose), not command content.
  `/exp-verify`'s anti-no-op check could not have caught F1 (which happens at REPORT time, after the
  run) — `/artifact-acceptance` is the right owner and now explicitly checks number fidelity.
- **Layer-2 (v0.6)**: `/irreversible-decision-audit` is precisely the compute-lock detector this
  campaign needed and never called. Binding it into `/prereg`'s launch-arithmetic block (I2) makes it
  structural for training runs; it remains standalone for narrative/benchmark/reputation locks.
