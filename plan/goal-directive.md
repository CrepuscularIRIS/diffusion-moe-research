<!-- Paste everything below the `---` after `/goal`. Body is <3000 chars. -->
---
OBJECTIVE: OPTIMIZATION/IMPROVEMENT (NOT val) on DiffusionGemma-26B MoE — SOLVE ONE HARD PROBLEM: the FACTORIZATION BARRIER (block-parallel denoising assumes per-position independence → many tokens/step lose quality). DSpark only patches it with a first-order MARKOV head — under-modeled. GOAL: push how far the MoE can reliably COMMIT per step BEYOND Markov — a DSpark × DiffusionMoE crossover (a cheap MoE-informed higher-order dependency head, no re-serialize). Deliverable = a METHOD that IMPROVES generation (better verified quality at matched compute, or more tokens/step at equal quality), NOT a benchmark.

METHOD = STRICTLY enrich (Modeling-Object-Shift, /mos-front): WRONG object = per-position independent block prediction; RIGHT = the dependency-structured joint prediction Markov under-models. Occupancy-scan FIRST — is the beyond-Markov slice OPEN? (KILLED = frozen post-hoc joint-readout for REASONING-novelty, tree 5.5/5.9/5.10.3; NEW = a TRAINED longer-range dependency head for GENERATION-QUALITY — distinct goal+substrate). Pro designs the object → /object-shift-audit → preregister → train+measure.

PLATFORM: DiffusionGemma-26B-A4B MoE (PRIMARY); LLaDA-8B (trainable, headroom) for a cheap prototype. Verify shard SHAs. Metric = generation/verifier improvement only; diffusion-loss/reference-token INVALID.

ENGINES (§1): Opus=PI/route/executor (subagents inherit session model) · Pro=Playwright `Pro 扩展` LEAP (KEEP ALIVE) · Codex=AUTO review HOOK (DOWN-only; /codex:rescue RETIRED).

★ROUTE-FIRST (§5.0): DESIGN=NEW_DIRECTION→/mos-front(occupancy FIRST→Pro)→/object-shift-audit. TRAIN/measure=EXPERIMENT_RUN→executor subagent+/exp-verify. Improvement claim→/baseline-champion+/reward-hack-audit. 1 token/cycle or spinning.

EXECUTION: run the §2/§5 loop — OBSERVE factorization gaps → /mos-front(occupancy→Pro) → /object-shift-audit → preregister → executor worktree (1 GPU, nvidia-smi first, measure-first) → /exp-verify → null→/bank-negative → tree FIRST → NEG: AUTO-PIVOT (next beyond-Markov lever, NO user Q). Caps §2.

FORBIDDEN (banked dead): FROZEN post-hoc joint-readout for REASONING-novelty (5.5/5.9/5.10.3) · He-line continuous-flow on discrete masked (saturated) · compute-allocator/always-deepen · SFT-as-quality-lever · SC-target-on-frozen · wall-clock EVALUATION (dropped).

READ: plan/README → operating-manual(§1,§5.0) → enrich.md → DSpark-analysis → diffusionmoe-technical-report-2026-06-27 → tree_view(diffusion-moe). Keys .env.

RULES (§5.1): pre-seal {hyp/falsifier/acceptance/neg-control/metric/split}; metric generation/verifier only; sealed test untouched. PIVOT autonomously (NO which-dir Qs); self-grant ONLY DOWN; strong verdicts INDEPENDENT (hook / object-shift-audit)+machine-enforced; contribution/paper→human.

RUN-STOPS: a preregistered IMPROVEMENT solving the barrier (measured Δ, baseline-champion signed) → HARD-BLOCK→human · OR beyond-Markov space exhausted · OR caps. Banked negative = CYCLE-progress, NOT a run-stop.
