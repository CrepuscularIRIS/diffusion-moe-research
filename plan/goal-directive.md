<!-- Paste everything below the `---` after `/goal`. Body is <3000 chars. -->
---
OBJECTIVE: OPTIMIZATION/IMPROVEMENT (NOT val/eval) on 2×4090D (96GB). The problem: PARALLEL REASONING IS LESS TOKEN-EFFICIENT THAN SERIAL — DiffusionGemma's factorization barrier is reasoning-length, not token-coordination (DPC finding; EBS handles terminals correctly). GOAL: make diffusion-LM reasoning MORE TOKEN-EFFICIENT per step — better quality at same budget, or same quality with fewer steps. BROADER than frozen post-hoc heads (exhausted). TRAIN, change architecture/sampling/loss — anything 96GB + improves generation.

METHOD = STRICTLY enrich (/mos-front). WRONG object = treat each denoising step as equally informative (flat budget); RIGHT = restructure how the model ALLOCATES reasoning across steps. Occupancy-scan FIRST. Prior kills (5.11/5.9/5.10 frozen exhausted; He-line saturated) constrain but do NOT close training-based interventions. Pro designs the object → /object-shift-audit → preregister → train+measure.

PLATFORM: LLaDA-8B = PRIMARY trainable (full-finetune fits 96GB; 62.5% MATH-500, ~42% headroom). DiffusionGemma-26B-A4B MoE = inference+LoRA. Verify shard SHAs. Metric = generation/verifier only; diffusion-loss/ref-token INVALID.

CANDIDATE DIRECTIONS (occupancy decides; Pro designs): denoising-trajectory curriculum (front-load reasoning) · step-aware loss reweighting · parallel CoT scaffolding (parallel-friendly decomposition) · DSpark speculative draft-verify (dLLM breadth + corrector depth).

ENGINES (§1): Opus=PI/route/executor (subagents inherit session model) · Pro=Playwright `Pro 扩展` LEAP (KEEP ALIVE) · Codex=AUTO review HOOK (DOWN-only; /codex:rescue RETIRED).

★ROUTE-FIRST (§5.0): DESIGN=NEW_DIRECTION→/mos-front(occupancy→Pro)→/object-shift-audit. TRAIN=EXPERIMENT_RUN→executor+/exp-verify. Improvement claim→/baseline-champion+/reward-hack-audit. 1 token/cycle or spinning.

EXECUTION: §2/§5 loop — OBSERVE(reasoning-length failures) → /mos-front → /object-shift-audit → preregister → executor worktree (1 GPU, nvidia-smi first) → /exp-verify → null→/bank-negative → tree FIRST → NEG: AUTO-PIVOT (NO user Q). Caps §2.

FORBIDDEN: post-hoc frozen heads (5.11 exhausted) · He-line continuous-flow on discrete (saturated) · compute-allocator/always-deepen · wall-clock EVALUATION framing · frozen-only interventions on DiffusionGemma.

READ: operating-manual(§1,§5.0) → enrich.md → DSpark-analysis → diffusionmoe-technical-report-2026-06-27. Keys .env.

RULES (§5.1): pre-seal {hyp/falsifier/acceptance/neg-control/metric/split}; metric generation/verifier only; sealed test untouched. PIVOT autonomously (NO which-dir Qs); self-grant ONLY DOWN; strong verdicts INDEPENDENT+machine-enforced; contribution/paper→human.

RUN-STOPS: a preregistered IMPROVEMENT with measured Δ (baseline-champion signed) → HARD-BLOCK→human · OR training-based optimization space exhausted · OR caps. Banked negative = CYCLE-progress, NOT a run-stop.
