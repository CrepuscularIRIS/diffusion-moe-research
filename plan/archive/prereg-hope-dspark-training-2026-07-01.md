# PREREGISTRATION — HOPE-DSpark Training Experiment — 2026-07-01

> Sealed BEFORE training. Arbor run dspark-head, node 1.1. DPC PASSED (median suffix TV=0.380, 19x threshold).
> Object-shift audit: ELIGIBLE_FOR_BACK_HALF (all T1-T6 pass).

## HYPOTHESIS
A higher-order sequential correction head (HOPE-DSpark) that conditions on x_{k-2} in addition to x_{k-1}
achieves higher accepted length than DSpark's 1st-order Markov head, because the target model's distribution
at position k is ~38% TV-sensitive to x_{k-2} (DPC finding).

## 3-ARM EXPERIMENT (per audit: ablate exposure-bias separately)
- **Arm A**: DSpark VanillaMarkov baseline (1st-order, rank-256) — existing DeepSpec checkpoint or retrained
- **Arm B**: DSpark VanillaMarkov retrained with sampled-prefix data (Pathwise-TV) — tests exposure-bias fix
- **Arm C**: HOPE-DSpark (2nd-order pair path + prefix attention + entropy gate + sampled-prefix training)

All arms trained with identical compute budget (same FLOPs, same data, same DeepSpec TV-distance loss).
Target model: Qwen2.5-7B-Instruct (already cached, 15GB). If DeepSpec doesn't natively support Qwen2.5,
adapt the config.

## FALSIFIERS
1. Arm C does not beat Arm A by ≥3% relative accepted length → head doesn't help
2. Arm B matches Arm C → architecture unnecessary, exposure-bias fix is the whole story
3. Latency of HOPE head exceeds 5% per-round overhead → too expensive

## ACCEPTANCE (all required)
- C > A by ≥3% relative accepted length (primary)
- C > B by ≥1% (architecture contributes beyond just training fix)
- C's per-round latency overhead < 5% vs A
- Measured on ≥3 diverse benchmarks (code, math, chat)

## METRIC
- Primary: accepted length (mean across benchmarks)
- Secondary: tokens/sec end-to-end
- Reported per-benchmark (code, math, chat) and aggregate

## PLATFORM
- Target: Qwen2.5-7B-Instruct (cached at /data/huggingface)
- Hardware: 2×RTX-4090D (96GB total)
- Framework: DeepSpec (TV-distance loss, freeze target)
- Training: reduce global_batch_size to fit 2 GPUs (gradient accumulation)
- Head parameters: pair_MLP_hidden=128, prefix_attention_heads=1, prefix_attention_dim=64

## TRAINING SCHEDULE (per audit: sampled-prefix training)
Phase 1: Train pair path + gate on 80% teacher-forced + 20% DSpark-sampled prefixes
Phase 2: Mixed 50/50 teacher-forced + HOPE-sampled prefixes
Arm B gets the same prefix schedule but with VanillaMarkov architecture (no pair path / attention)

## MASK DISTRIBUTION (pre-registered FIXED)
Standard DeepSpec loss: 0.9×TV + 0.1×CE, decay gamma=4.0. No modification to loss weighting.

## EVAL BENCHMARKS
Use DeepSpec's built-in eval_datasets: gsm8k, math500, humaneval, mt-bench (subset).
Report accepted length per benchmark + aggregate.
