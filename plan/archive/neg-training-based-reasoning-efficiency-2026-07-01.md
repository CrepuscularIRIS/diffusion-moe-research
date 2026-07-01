# Banked Negative — Training-Based Reasoning Efficiency Campaign — 2026-07-01

> Arbor tree 5.13 (done). Self-graded DOWN. RUN-STOP: training-based optimization space exhausted.

## Campaign Summary
Three directions explored to make discrete masked-diffusion LLM reasoning more token-efficient:

### Direction 1: Parallel Frontier Certificate (PFC) Training (5.13.1, KILLED)
- Pro-designed: train on dependency-layered certificates where same-depth cells are independently denoisable
- Object-shift audit: PASS (ELIGIBLE)
- DPC Steps A-C: GO (PMASS=0.928, ARNESS_resid=0.576)
- **DPC Step D: KILL** — Δprefix = 3.33 nats/token (threshold ≤0.5). The model has ~3 nats sequential bias. It CANNOT predict reasoning atoms from dependency context alone — it requires the serialized prefix. Parallel recoverability doesn't exist in the pretrained model.

### Direction 2: Verifier-Compressed Certificate SFT (5.13.2, NEGATIVE)
- Train LLaDA-8B on NuminaMath with standard vs. length-filtered (compressed) solutions
- **Standard SFT degrades the model by -20pp** (62.5% → 42.5%)
- Compressed SFT mitigates to -5pp (57.5%) — **concept validated** but insufficient
- L5 (hard problems): compressed SFT improves 25% → 37.5% while standard SFT destroys to 0%
- ROOT CAUSE: masked-CE SFT is misaligned with reasoning quality

### Direction 3: RL-Based Methods (OCCUPIED)
- DCoLT (arXiv 2505.10446): +5.7% MATH, +9.8% GSM8K on LLaDA via REINFORCE
- GDPO, Step-Aware PO, Entropy-Guided, d-TreeRPO, etc. — crowded space
- The ONLY demonstrated method for dLLM reasoning improvement, but OCCUPIED

## Key Scientific Findings

1. **The factorization barrier in discrete masked-diffusion LLMs is REASONING-LENGTH dominated** (DPC on DiffusionGemma-26B: correct answers = 689 tokens, wrong = 1120 tokens; EBS handles terminals correctly).

2. **Pretrained dLLMs have ~3 nats sequential bias** (PFC DPC Step D on LLaDA-8B: Δprefix=3.33). Reasoning atoms are NOT independently recoverable from dependency context — the model fundamentally expects sequential text.

3. **Masked-CE SFT is misaligned with dLLM reasoning quality** (SFT on NuminaMath: -20pp with standard solutions, -5pp with compressed). Optimizing the diffusion loss doesn't improve verified-answer accuracy. This is consistent across models (DiffusionGemma: SFT halved diff loss for 0% accuracy gain; LLaDA: SFT loss drops to 0.49 but accuracy drops by 5pp).

4. **Compressed training solutions are dramatically better for dLLM SFT** (+15pp over standard SFT; L5 improves while standard L5 collapses). Solution length interacts adversely with the masked-diffusion training objective.

5. **Outcome-based RL (not text-prediction SFT) is the right training signal for dLLM reasoning** — DCoLT's REINFORCE on denoising trajectories works because it optimizes the verified answer, not token prediction. This is the only demonstrated improvement method but is OCCUPIED.

## Transferable Insight
For discrete masked-diffusion LLMs, the training objective (predict masked tokens from context) creates a fundamental misalignment: lower diffusion loss ≠ better reasoning. Any reasoning improvement must optimize the OUTCOME (via RL/verifier reward), not the TEXT (via masked-CE). This occupied space is the only known viable approach, making the enrich methodology's SFT-based directions a dead end for reasoning quality improvement.

## Artifacts
- `outputs/closure_dpc/` — DiffusionGemma DPC (164 problems instrumented)
- `outputs/pfc_dpc/` — LLaDA PFC DPC (40 problems instrumented + Step D counterfactuals)
- `outputs/sft_experiment/` — SFT training results (two LoRA models + evals)
- `plan/gpt55pro-parallel-frontier-certificate-2026-07-01.md` — Pro's PFC design
- `plan/osa-parallel-frontier-certificate-2026-07-01.json` — Object-shift audit
