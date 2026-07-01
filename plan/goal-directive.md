<!-- Paste everything below the `---` after `/goal`. Body is <3000 chars. -->
---
OBJECTIVE: IMPROVEMENT on speculative decoding — design and train a BETTER sequential correction head than DSpark's 1st-order Markov (arxiv:2606.19348). DSpark proved a lightweight Markov head cuts suffix decay +26-31% vs EAGLE-3 but is under-modeled (RNN variant = "marginal improvement", unexplored). GOAL: measurably higher accepted length on 96GB (2×4090D). This is IMPROVEMENT work (enrich type H/B: empirical + engineering), NOT novelty-seeking — the idea "higher-order conditioning should help" is obvious; the contribution is the measured Δ.

LANE = IMPROVEMENT (§5.0): skip /mos-front and /object-shift-audit (those are for novelty). Instead: design → train (DeepSpec framework) → measure accepted length → /baseline-champion (1st-order Markov baseline) + /exp-verify + /reward-hack-audit at claim boundary. Occupancy check = "has this EXACT improvement been done and measured on this target" NOT "does anyone work in this area."

PLATFORM: target model = Qwen3-4B or LLaMA-3-8B (fits 96GB with draft head). Use DeepSpec (MIT, deepseek-ai/DeepSpec) — freezes target, TV-distance loss. Metric = accepted length (primary) + tokens/sec (secondary) vs 1st-order Markov baseline on same target.

CANDIDATE DESIGNS (iterate by measured Δ, not by occupancy): 2nd/3rd-order conditional (condition on 2-3 preceding tokens) · lightweight cross-attention over draft prefix · gated RNN (improved DSpark variant) · hybrid Markov+attention · MoE-router-informed confidence (MoE-specific free signal).

ENGINES (§1): Opus=PI/route/executor (subagents inherit session model) · Pro=Playwright `Pro 扩展` (deep design if needed; KEEP ALIVE) · Codex=AUTO review HOOK (DOWN-only; /codex:rescue RETIRED).

EXECUTION: §2/§5 loop — OBSERVE(suffix decay pattern in Markov-head drafts on the target model) → DESIGN(pick a candidate head architecture) → TRAIN(DeepSpec, executor worktree, 1 GPU, nvidia-smi first) → MEASURE(accepted length + tokens/sec) → /exp-verify → Δ > 0? → /baseline-champion(1st-order Markov) + /reward-hack-audit → DECIDE → BACKPROP(tree FIRST) → no Δ: AUTO-PIVOT to next candidate design (NO user Q). Caps §2.

FORBIDDEN: dLLM/LLaDA/DiffusionGemma (CLOSED, do NOT cross-contaminate) · /mos-front or /object-shift-audit on improvement work (wrong lane) · He-line · wall-clock eval framing.

READ: operating-manual(§1,§5.0) → DSpark-analysis → dspark-deep-analysis-2026-07-01 → enrich.md. Keys .env.

RULES (§5.1): pre-seal {hyp/falsifier/acceptance/neg-control/metric/split}; metric = accepted length + tokens/sec; sealed test untouched. PIVOT autonomously (NO which-dir Qs); self-grant ONLY DOWN; strong verdicts INDEPENDENT+machine-enforced; contribution/paper→human.

RUN-STOPS: a measured Δ in accepted length vs 1st-order Markov (baseline-champion signed) → HARD-BLOCK→human · OR all candidate head architectures exhausted with no Δ · OR caps. Banked negative = CYCLE-progress, NOT a run-stop.
