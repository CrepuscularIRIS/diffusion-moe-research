# FINAL round status — Verified Wall-Clock Frontier + DSpark levers (2026-07-01)

> Living status doc for the FINAL /goal round. Becomes the human hand-off for the RUN-STOP
> ("Level-A result beating matched AR, baseline-champion signed → HARD-BLOCK→human").
> Tree 5.8.* · RUNLOG "NEW GOAL 2026-07-01". Updated as async gates land.

## JOB1 — HARDEN the frontier to Level-A  →  ✅ CERTIFIED_LEVEL_A (from raw)

**Result (frozen DiffusionGemma-26B-A4B dLLM vs matched AR sibling gemma-4-26B-A4B-it, MATH-L5 sealed, 134 problems, FAIR budget 2048):**

| @2048 (both non-truncated) | dLLM | AR | note |
|---|---|---|---|
| verified accuracy | 0.823 | 0.836 | MATCHED (AR marginally higher) |
| verified-answers/sec | **5.30× (tp) / 6.59× (serial)** | 1× | the claim |
| Frontier-AUC(dLLM−AR) SERIAL | **1.804, CI[1.691,1.914]** | — | CI>0 |
| Frontier-AUC(dLLM−AR) THROUGHPUT | **1.790, CI[1.664,1.908]** | — | CI>0 |
| no-box (truncation) | 0.060 | 0.144 | AR fair (<0.15) |

**Why it is Level-A (independent, no-GPU certification — tree 5.8.2.1):**
- Re-derived `correct` for every 2048 record from stored `gen_full` via the SEALED `verify_math` (not the
  trusted stored bit): **0/402 mismatch on BOTH arms**, 0 gold mismatches. Headline reproduces exactly.
- Verifier SOUND: char-shuffle + wrong-gold neg-controls both collapse to 0.000 (the pre-declared
  *whitespace* token-shuffle was mis-specified — a single `\boxed{}` survives it; the executor caught this and
  ran the stronger controls). Verifier symmetric: 17% of AR parse-fails are missed-box (< 30% threshold), rest
  genuine truncation.
- Seed mean±std (3 seeds {42,123,7}): AR 0.836±0.016, dLLM 0.823±0.009 — not a lucky seed.
- All 4 pre-declared falsifiers NOT fired. `analyze.py:180` gold-field audit bug fixed.
- Deliverables: `outputs/wallclock_levelA_audit/{verdict.json,AUDIT_REPORT.md,run_audit.py}`.
- Reproduced-from-raw artifacts live in worktree `agent-aa411b381a8c95d40` (branch
  `worktree-agent-aa411b381a8c95d40`, commit 3e873bd); 2048 arms store full raw gens.

**Core claim scope (the honest firewall):** the SERVING-INDEPENDENT advantage is dLLM's NFE/forward-pass
efficiency (~40 forward passes / ~600-770 tokens vs AR ~770-1070 sequential tokens). Both models are HF-bound
(no vLLM/TP in-env); a production AR serving stack could narrow the THROUGHPUT gap but not the per-request
SERIAL (NFE-bound) advantage. → this is exactly what the independent Pro fairness review is stress-testing.

**Residual (non-blocking) gaps:** @768/@1280 arms lack `gen_full` (AR-truncated, not the headline); AR@1280/2048
+ dLLM@2048 are 3-seed (the audit did NOT flag 3-seed as material — tight CIs, small std); artifacts unmerged.

### JOB1 independent fair-AR sign-off (baseline-champion) — ⏳ PENDING (GPT-5.5 Pro, Playwright)
Routed the fairness attack to GPT-5.5 Pro (serving-stack attack, metric-gaming, strawman check, single strongest
objection, verdict DEFENSIBLE_AS_FRAMED / NEEDS_VLLM_AR / FATALLY_UNFAIR). [FILL WHEN LANDS]

## JOB2 — DSpark systems levers (frozen)  →  ⏳ OBSERVE probe running

**Prior from aggregate NFE (stored dLLM@2048):** the EB-sampler is ALREADY efficient + dynamic-canvas
(median 36 forward passes, ~23 tok/forward, canvas median 768 ≪ 2048 budget). Strong subsumption prior for
levers #1/#2; low ceiling (they can only polish an already-winning number ~10-20%, not change the qualitative win).

- Lever #1 (token-stability early-commit) — trajectory probe measuring post-boxed-stability wasted NFE. [PENDING]
- Lever #2 (lossless dynamic canvas) — probe measuring early-entropy length prediction vs current dynamic stop. [PENDING]
- Lever #3 (intra-block dependency) — deferred (highest kill-risk; factorization not the reasoning bottleneck per
  the banked masked-diffusion-reasoning negative; frozen sequential = speed-for-quality trade). [PENDING decision]

Probe on MATH-500 **level-4** DEV (disjoint from sealed level-5). GO if headroom > 15%, else SUBSUMED. [FILL WHEN LANDS]

## Run-stop status
JOB1 = a Level-A result beating matched AR on verified-answers/sec. Once Pro signs the fairness (baseline-champion),
this satisfies the RUN-STOP → HARD-BLOCK to human for promotion (cannot self-promote to "contribution/paper").
JOB2 continues autonomously (AUTO-PIVOT on null) until levers exhausted / banked-subsumed / caps.
