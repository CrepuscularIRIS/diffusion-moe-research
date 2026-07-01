<!-- Paste everything below the `---` after `/goal`. Body is <3000 chars. -->
---
OBJECTIVE: OPTIMIZATION/IMPROVEMENT on speculative decoding — SOLVE the SUFFIX DECAY problem BEYOND DSpark's first-order Markov head. DSpark (arxiv:2606.19348) proved a lightweight 1st-order Markov head cuts suffix decay (+26-31% vs EAGLE-3) but is under-modeled (RNN variant = "marginal improvement", unexplored). GOAL: design and train a BETTER sequential head (higher-order / attention-based / context-aware) that achieves measurably higher accepted length than the 1st-order Markov baseline, on a 96GB (2×4090D) budget.

METHOD = STRICTLY enrich (/mos-front). WRONG object = position-independent parallel draft (DFlash baseline); RIGHT = dependency-structured sequential correction BEYOND 1st-order Markov. Occupancy-scan FIRST — is the "higher-order sequential head for speculative decoding" slice OPEN? (DSpark=1st-order; EAGLE/Medusa/Hydra=parallel-only; Jakiro=MoE draft, no seq head). Pro designs the object → /object-shift-audit → preregister → train + measure.

PLATFORM: target model = Qwen3-4B or LLaMA-3-8B (fits 96GB with draft head). Use **DeepSpec** (MIT, deepseek-ai/DeepSpec) — freezes target, TV-distance loss. Metric = **accepted length** (primary) + tokens/sec (secondary) vs DSpark's 1st-order Markov baseline on same target model.

CANDIDATE DESIGNS (occupancy decides; Pro designs): 2nd/3rd-order conditional · lightweight cross-attention over draft prefix · gated RNN (improved DSpark variant) · MoE-router-informed draft quality.

ENGINES (§1): Opus=PI/route/executor (subagents inherit session model) · Pro=Playwright `Pro 扩展` LEAP (KEEP ALIVE) · Codex=AUTO review HOOK (DOWN-only; /codex:rescue RETIRED).

★ROUTE-FIRST (§5.0): DESIGN=NEW_DIRECTION→/mos-front(occupancy→Pro)→/object-shift-audit. TRAIN=EXPERIMENT_RUN→executor+/exp-verify. Improvement claim→/baseline-champion(1st-order Markov)+/reward-hack-audit. 1 token/cycle or spinning.

EXECUTION: §2/§5 loop — OBSERVE(suffix decay failures in Markov-head drafts) → /mos-front → /object-shift-audit → preregister → executor worktree (1 GPU, nvidia-smi first) → /exp-verify → null→/bank-negative → tree FIRST → NEG: AUTO-PIVOT (NO user Q). Caps §2.

FORBIDDEN: dLLM/LLaDA/DiffusionGemma (CLOSED, do NOT cross-contaminate) · He-line · wall-clock eval framing · compute-allocator.

READ: operating-manual(§1,§5.0) → DSpark-analysis → dspark-deep-analysis-2026-07-01 → enrich.md. Keys .env.

RULES (§5.1): pre-seal {hyp/falsifier/acceptance/neg-control/metric/split}; metric = accepted length + tokens/sec; sealed test untouched. PIVOT autonomously (NO which-dir Qs); self-grant ONLY DOWN; strong verdicts INDEPENDENT+machine-enforced; contribution/paper→human.

RUN-STOPS: a preregistered IMPROVEMENT with measured Δ in accepted length vs 1st-order Markov (baseline-champion signed) → HARD-BLOCK→human · OR higher-order-head space exhausted · OR caps. Banked negative = CYCLE-progress, NOT a run-stop.
