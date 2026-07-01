<!-- Paste everything below the `---` after `/goal`. Body is <3000 chars. -->
---
OBJECTIVE: FINAL round on DiffusionGemma-26B MoE (frozen) — the Verified Wall-Clock Frontier: same hardware · verifier · prompts, does the dLLM yield MORE verified answers/sec than matched AR? Two jobs: (1) HARDEN the WIN-NEEDS-FIX frontier (tree 5.8) to Level-A; (2) push it with DSpark systems levers (frozen). Experiment-FORWARD: real runs, real Δ.

PLATFORM: DiffusionGemma-26B-A4B MoE (PRIMARY) + matched AR; frozen (no retrain). Verify shard SHAs on load (digit-blind lesson). ★Only Level-A counts (fixed ckpt + generation/verifier + independent review + reproducible raw; layers A/B/C = tech-report §1.2). Diffusion-loss & reference-token = INVALID proxy.

JOB1 HARDEN: fix the Codex WIN-NEEDS-FIX gaps — full AR@1280 + fair AR@2048 & dLLM@2048, store FULL raw generations, fix the audit bug, rerun bootstrap. (@768 edge was mostly AR-truncation; @1280+ needs a fair baseline to count.)

JOB2 DSPARK LEVERS (frozen, no retrain; DSpark-analysis.md): #1 token-level STABILITY/confidence head → early-commit stable blocks (\boxed{}), free canvas; #3 lightweight intra-block sequential/Markov head → inject intra-block dependency at inference; #2 LOSSLESS dynamic canvas (first-step entropy → truncate WITHOUT lowering verifier pass-rate). Each must beat AR at verified-answers/sec.

ENGINES (§1): Opus=PI/route/decide · Sonnet-5=executor subagents (`model:sonnet`, all code/exp) · Pro=Playwright `Pro 扩展` (KEEP ALIVE) · Codex=AUTO review HOOK on every diff (advisory DOWN-only; /codex:rescue RETIRED).

★ROUTE-FIRST (§5.0): most work = EXPERIMENT_RUN → Sonnet-5 + /exp-verify. Heavy suite ONLY at a CLAIM BOUNDARY: any "beats AR/faster/frontier" → /baseline-champion (fair AR: matched budget, PAIRED stats) + /reward-hack-audit (≥3 seeds, raw gens). Systems lane skips object-shift. Each cycle emits 1 progress-token (§5.0), else spinning.

EXECUTION (§2/§5 loop): OBSERVE→SELECT(Opus+KILL-gates+hook)→DISPATCH(/context-bundle→Sonnet-5 worktree; 1 GPU job, nvidia-smi first, measure-first)→VERIFY(/exp-verify)→DECIDE(null→/bank-negative)→BACKPROP(tree FIRST)→FAIL|NEG: AUTO-PIVOT(next lever, NO user Q)→LOOP. Caps §2.

FORBIDDEN (banked dead): compute-allocator/always-deepen (≈oracle, ~1% ΔAUC) · He-line/gradient-field (saturated) · masked-diff-reasoning · SFT-as-quality-lever · SC-target-on-frozen · timestep-router-audit (no t input).

READ: plan/README → operating-manual (§1, §5.0) → diffusionmoe-technical-report-2026-06-27 → DSpark-analysis → tree_view(diffusion-moe) → RUNLOG. Keys .env.

RULES (§5.1): pre-seal {hyp/falsifier/acceptance/neg-control/metric/split}; metric = generation/verifier only; sealed test untouched. PIVOT autonomously (NO which-direction Qs); self-grant ONLY DOWN; strong verdicts = INDEPENDENT (Codex hook)+machine-enforced; contribution/paper = HARD-BLOCK→human.

RUN-STOPS: a Level-A result beating matched AR (baseline-champion signed) → HARD-BLOCK→human · OR levers exhausted · OR caps. A banked negative = CYCLE-progress, NOT a run-stop.
