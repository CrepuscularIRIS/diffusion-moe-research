<!-- Paste everything below the `---` after `/goal`. Body is <3000 chars. -->
---
OBJECTIVE: IMPROVEMENT on speculative decoding — design and train a BETTER sequential correction head than DSpark's 1st-order Markov (arxiv:2606.19348). DSpark proved a lightweight Markov head cuts suffix decay +26-31% vs EAGLE-3 but is under-modeled (RNN variant = "marginal improvement", unexplored). GOAL: measurably higher accepted length on 96GB. IMPROVEMENT work (enrich schools B/H), NOT novelty — "higher-order conditioning should help" is obvious; the contribution is the measured Δ.

TYPE = IMPROVEMENT 刷分 (op-manual §5.0): no novelty gates — verification is TYPE-scoped. Loop: /forge candidate → /prereg → train (DeepSpec) → measure accepted length → /exp-verify → /adversary at the claim boundary (A Δ-reality: ≥3 seeds, neg-control, sealed holdout; B baseline-fairness: make the 1st-order Markov baseline win, paired stats). Occupancy = "has this EXACT improvement been measured on this target" NOT "does anyone work in this area" (never a veto).

PLATFORM: target = Qwen3-4B or LLaMA-3-8B (fits 96GB with draft head). DeepSpec (MIT, deepseek-ai/DeepSpec) — freezes target, TV-distance loss. Metric = accepted length (primary) + tokens/sec (secondary) vs 1st-order Markov baseline on same target.

CANDIDATE SEED (the /forge backlog is LIVE — regenerate from each /autopsy conversion law; NOT a fixed menu): 2nd/3rd-order conditional · lightweight cross-attention over draft prefix · gated RNN (improved DSpark variant) · hybrid Markov+attention · MoE-router-informed confidence.

ENGINES (§1): Opus=PI/route/executor (subagents inherit session model) · Pro=Playwright `Pro 扩展` (deep design if needed; KEEP ALIVE) · Codex=AUTO review HOOK (DOWN-only; /codex:rescue RETIRED).

EXECUTION: §5.2 generator + §5.1 discipline loop — OBSERVE(suffix decay in Markov-head drafts) → /forge(pick a candidate) → /prereg → TRAIN(DeepSpec, executor worktree, 1 GPU, nvidia-smi first) → MEASURE(accepted length + tokens/sec) → /exp-verify → Δ>0? → /adversary(A+B, vs 1st-order Markov) → DECIDE → BACKPROP(tree FIRST) → no Δ: /autopsy(CONVERSION LAW → constraint/candidate/region-close) → AUTO-PIVOT (NO user Q). /compass every 3–5 cycles. Caps §2.

FORBIDDEN: dLLM/LLaDA/DiffusionGemma (CLOSED, do NOT cross-contaminate) · novelty-gate framing on 刷分 work (wrong type) · He-line · wall-clock eval framing.

READ: operating-manual(§1,§5.0,§5.1,§5.2) → DSpark-analysis → dspark-deep-analysis-2026-07-01 → enrich.md. Keys .env.

RULES (§5.1): /prereg seals {hyp/mechanism/falsifier/accept/neg-control/metric/split/seeds} before any claim-bearing run; sealed test untouched. PIVOT autonomously (NO which-dir Qs); self-grant ONLY DOWN; CLAIM_STANDS = independent (Codex hook); contribution/paper → human.

RUN-STOPS: a measured Δ vs 1st-order Markov (/adversary CLAIM_STANDS, independent) → HARD-BLOCK→human · OR /compass STOP_AND_REPORT (backlog dry after /autopsy regeneration + 2 re-/prospect rounds) · OR caps. A banked negative WITH its conversion-law output = CYCLE-progress, NOT a run-stop.
