# Banked Negative — Closure-Utility Head DPC Probe — 2026-07-01

> Arbor node 5.11.2 (pruned) / 5.11.2.1 (done). Self-graded DOWN.

## Direction
**Closure-Utility Head (O1)** — a trained closure-selector on frozen DiffusionGemma-26B that re-ranks O0's commit decision by a verifier-derived closure signal, targeting the truncation-dominant failure mode (correct reasoning but no \boxed{} committed before budget).

## Hypothesis
Terminal-rank discordance in O0's EntropyBoundSampler creates a learnable closure signal — the model assigns nontrivial probability to terminal tokens (\boxed{}, eos) but EBS deprioritizes them, causing truncation failures that a trained closure head can rescue.

## Falsifier
DPC probe on frozen O0 logs: S3 (candidate+tight-budget+terminal-rank-discordance) must contain ≥40% of truncation failures, and oracle must rescue ≥20% of S3 failures.

## Result: KILLED at DPC
**S3 = 0 out of 28 truncation failures (0%)**. All 7 GO gates FAIL:
- G1: S3 fraction = 0.0 (threshold ≥0.40) → FAIL
- G2: Oracle rescues S3 = 0 (threshold ≥0.20) → FAIL
- G3: Overall gain = +0.61pp / 3.6% truncation reduction (threshold ≥3pp or ≥25%) → FAIL
- G4: Shuffled-S control = skipped (S3=0) → FAIL
- G5: Generic-difficulty = AUC delta 0.0, S adds nothing → FAIL
- G6: DeadlineBox captures 100% of the sole rescue → FAIL
- G7: False-positive net gain = -22 (23 FP, 1 rescue) → FAIL

## Failure Type
**A: Premise falsified.** The closure-stranding mechanism does not occur on this model+task.

## Evidence
- All 28 truncation failures have remaining_mask_frac ≈ 0 (all positions committed) with terminal tokens at logit_rank=0 (top-ranked by EBS, prob≈1.0)
- Every truncation failure is "reasoning incomplete" — the model ran out of budget mid-computation, not "closure stranded"
- The model's EBS correctly prioritizes \boxed{}/eos tokens whenever they appear; it does not deprioritize them
- Oracle rescue rate: 1/164 (0.6%), with DeadlineBox capturing that same 1 rescue
- Oracle HARMS overall: 19.5% false-positive rate on correct problems (wrong answer extracted from reasoning)

## Transferable Insight
**DiffusionGemma-26B's factorized denoiser has NO closure coordination problem at the token level.** The EntropyBoundSampler correctly commits terminal tokens with rank 0 whenever they appear. The factorization barrier manifests as **reasoning-length limitations** (parallel reasoning needs more tokens than serial to reach the same answer), NOT answer-materialization failures. Any beyond-Markov improvement on this model must target reasoning efficiency/quality, not post-hoc coordination of terminal tokens.

## Artifacts
- `outputs/closure_dpc/DPC_RESULT.json` — full gate results
- `outputs/closure_dpc/DPC_REPORT.md` — formatted report
- `outputs/closure_dpc/dllm_math_l5_1280_instrumented.jsonl` — 134 MATH-L5 trajectories
- `outputs/closure_dpc/dllm_aime_1280_instrumented.jsonl` — 30 AIME trajectories
- `plan/prereg-closure-dpc-probe-2026-07-01.md` — sealed preregistration
- `plan/gpt55pro-closure-utility-head-2026-07-01.md` — Pro-designed O1 spec

## Jump Target (named in Pro design)
Tool-call / JSON-schema / code-repair generation — where closure becomes parser-verifiable structural terminalization rather than near-ceiling math reasoning.
