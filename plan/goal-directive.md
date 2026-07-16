<!-- /goal CONTRACT. Turn 1: load the `engineer` skill (DRIVER). The engineer TRIGGERS the 7 step-skills
     in order via the Skill tool, and EACH step-skill then INVOKES its designated agent(s) via the
     Agent tool:
       1 observe-recall → lit-suite ∥ web-recon ∥ moa-panel   (concurrent breadth burst; + browser seed)
       2 lit-seal       → browser Scholar tab                 (main-loop; no agent)
       3 author-card    → moa-panel ∥ sol-math                (+ browser GPT-5.6, main-loop)
       4 build-run      → grok-verifier                       (grok-coder = A/B code-gen alternative)
       5 predict-launch → spend-gate                          (only if run > ~1 GPU-day)
       6 diagnose-gap   → sol-math / moa-panel / abduction    (keyed to contradiction / dead probes / surprise)
       7 update-claim   → claim-gate → grok-verifier          (certifies anything leaving the loop)
     Each skill ALSO fires directly on natural-language requests (see the skill's own description).
     This file = objective + domain + bindings only; the mechanics live in the skills. -->
---
OBJECTIVE: research competitive at **NeurIPS / ICLR / ICSE / FSE / AAAI** — think as an algorithm
engineer; PARAMETER-EFFICIENT RELIABILITY ADAPTATION is the central target, studied as a cross-
architecture research PLATFORM. Contribution = the mechanism-level claim (WHERE adaptation lives · does
ONE layer suffice); the model is the vehicle. Publication = human.
DELIVERABLE: a **CONTRIBUTION-COMPLETE package** — a layer-selective RL result beating fair (compute-/
tuning-matched) baselines (LoRA-all · frozen+head · full-parameter RL) on selective-verification metrics
WITH the mechanism diagnosed (which layer, why), OR a held-out-validated claim about where reliability
adaptation lives — plus the honest evidence map and a releasable repo (NOT the paper).
NON-GOALS: reproduction-only; benchmark deltas WITHOUT a mechanism; a scorer that gates nothing;
manuscript polish before contribution-completeness.
DECISION-CHANGE: a practitioner's choice — WHICH layer to post-train · run a container vs abstain ·
answer/retrieve/abstain — must move because of the claim; else it does not count.

DOMAIN — **LAYER-SELECTIVE RL PLATFORM — clean-slate `layer-select-verify` (v7.1).** FOUNDATION strategy
= single-layer GRPO (arXiv 2607.01232 "Is One Layer Enough?": freeze all, unfreeze ONE middle layer
~40–60% depth → up to 114% of full-RL gain). Use it as the BASELINE for CROSS-ARCHITECTURE × CROSS-DOMAIN
studies; recurring claim = where selective-verification adaptation lives + does one layer suffice.
Substrate `/data/projects/` (README) + `/data/models/`:
- METHOD: veRL fork `external/layer-selective-rl/` + PDF (⚠ `single_layer_grpo.py` ABSENT — STEP ZERO
  builds it: freeze all, unfreeze `layers[k]`, run GRPO).
- MODELS LOCAL (no download; coder may re-pull): Qwen2.5-VL-7B (28L, freeze vision-enc→scan decoder) /
  3B (36L) · Qwen3.5-4B-VL HYBRID (8 full-attn {4,8,…,32} + 24 linear-attn) · Qwen3.5-9B/27B-FP8 ·
  Qwopus3.5-9B-Coder · DiffusionGemma-26B (block-diffusion, DEFERRED).
- DOMAINS: (1) evidence-conflict ABSTENTION (ANSWER/RETRIEVE/ABSTAIN) — MMDeepResearch/VDR/DocVQA/ChartQA
  (downloaded); (2) selective CODE verification (SKIP/LOCAL/FULL, verifiable container reward) — SWE-bench
  Verified + SWE-Explore (`external/SWE-bench/`).
- ENTRY candidates (engineer selects via breadth burst): **A** = do RL gains concentrate in the FULL-attn
  vs LINEAR-attn layers of Qwen3.5-4B hybrid? (NOVEL, not in the paper; immediate) · **B** = 3-action
  multimodal policy on Qwen2.5-VL-7B (direct Project-1 path) · **C** = DiffusionGemma layer-locus
  (high-effort, deferred). Baselines: single-layer vs LoRA-all vs frozen+head vs full-RL.
**STEP ZERO (cheap): build the skeleton → `--scan` a local model (free param counts) → confirm the
layer-freeze GRPO runs → ONE small single-layer run vs LoRA-all + frozen+head on a small slice (SWE
20–50 issues or a doc-QA subset).** Then Observe→bottleneck→`openbuild/layer-select-verify/card.md`.
ENVELOPE: STOP_AND_REPORT at the FIRST of {skeleton+scan+first single-layer-vs-full comparison · clear
GO/KILL · ~2–4 GPU-days · human gate}. WORLD-MODEL line (`wm-distract-robust` + v1–v4) READ-ONLY.

BINDINGS (full = CLAUDE.md §2): env `/data/projects/` + `/data/models/` USER-MANAGED (inventory first;
new large data = spend-gate) · 2×4090D 49GB (GPU1 first, both concurrent, priced never capped; STEP ZERO
= scan+smoke) · executors = Sonnet · roles = v7.1 breadth-burst fleet (consultation never decision): MoA
+ `web-recon` (grok+codex ∥) · MODELING engineer + GPT-5.6 browser + sol + Opus subagent (cross-family) ·
VERIFIER Grok · LITERATURE lit-suite + Scholar 精读 · keys `.env` · guards `tools/guards/` at claim-gate.
CONSTRAINT: selective-verification protocol — calibration + risk–coverage (AUROC/AUPRC · AURC · ECE ·
container-reduction@90%-recall / Acc@abstain · cost-per-correct); ≥3 seeds; baselines compute-/tuning-
matched per claim (claim-gate check 3).
