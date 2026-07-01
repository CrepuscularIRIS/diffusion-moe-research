# Pre-registration — JOB1-A: Level-A certification of the Verified Wall-Clock Frontier

> Goal (2026-07-01 FINAL round), tree 5.8.2.1. Fires at DISPATCH. Metric = generation/verifier ONLY.
> This cycle spends **NO new GPU** — it certifies EXISTING stored raw to Level-A. Sealed set untouched.

## Context (as-found)
The fair-budget wall-clock rerun already exists (unmerged worktree `agent-aa411b381a8c95d40`,
branch `worktree-agent-aa411b381a8c95d40`, commit 3e873bd), `outputs/wallclock/`. VERDICT.md =
TOP-VENUE-ALIVE @FAIR 2048. But it was **never run through the independent Level-A gates**, and the
analysis trusts the stored `correct` bit rather than re-deriving it from `gen_full`. This cycle closes
the "independent review + reproducible raw" Level-A ingredients on the fair (2048) arms.

Fair budget = 2048 (AR no-box < 0.15). Both 2048 arms store `gen_full` (AR ~8k chars, dLLM ~1.6k) +
`gold` → re-derivable. Seeds present @2048: {42,123,7} (3, seed-matched). MATH-L5 = 134 sealed problems.

## Hypothesis (H)
On MATH-L5 at the FAIR budget 2048, the frozen dLLM (DiffusionGemma-26B-A4B) dominates the matched AR
sibling (gemma-4-26B-A4B-it) on the verified-success-vs-wall-clock frontier — Frontier-AUC(dLLM−AR) > 0
with 95% CI excluding 0 AND per-verified-second(dLLM) ≥ 2× per-verified-second(AR) at matched accuracy —
**AND this survives independent re-derivation of `correct` from stored `gen_full` via the sealed verifier.**

## Falsifier (ANY fires ⇒ H DOWN / NEEDS-FIX)
1. Re-running the sealed `math_verify` on stored `gen_full` changes AR **or** dLLM per-arm accuracy@2048
   by **> 2pp** vs the stored `correct` bits (⇒ stored correctness untrustworthy).
2. Fair-budget Frontier-AUC(dLLM−AR)@2048 95% CI **includes 0** after re-bootstrap from re-derived raw.
3. Per-verified-second speedup(dLLM/AR)@2048 at matched accuracy **< 2×**.
4. Verifier shown **asymmetric**: AR parse-fails are a parser artifact (a recoverable boxed answer exists
   in `gen_full` that the parser missed) rather than genuine budget truncation, on manual re-audit of
   ≥20 pass + ≥10 parse-fail per model.

## Acceptance (ALL required for CERTIFIED_LEVEL_A)
- Per-arm acc@2048 (both models) reproduces from `gen_full` within 2pp of stored.
- Frontier-AUC(dLLM−AR)@2048 CI > 0 (serial AND throughput).
- Matched-accuracy per-verified-second speedup ≥ 2×.
- Verifier symmetric + sound on manual re-audit.
- reward-hack-audit union guard set CLEAN (below).
- ≥3 seeds at fair budget (met: 3), reported as **mean ± std across seeds**, not best-run.

## Negative controls
- **Token-shuffle**: shuffle the token order of each `gen_full` before verifying → verified accuracy must
  collapse toward ~0 (confirms the verifier rewards genuine answers, not surface tokens).
- **Seed-variance**: report mean ± std across seeds {42,123,7}; the headline may not cherry-pick a seed.
- **No-mock / anti-no-op**: re-derivation must actually call the verifier on real text (assert non-trivial
  parse-rate; assert per-record verifier output varies).

## Metric
Generation/verifier ONLY: verified solve-rate S(B), Frontier-AUC over log wall-clock, per-verified-second,
no-box (truncation) rate. **Diffusion-loss / reference-token metrics are INVALID and forbidden here.**

## Split
MATH-L5 (134 sealed problems) + sealed MATH-500-L5 gold. The executor MUST NOT modify the problem set,
the gold, or the verifier logic (sealed). It may only re-run the existing verifier on stored generations.

## Decision rule
- ALL acceptance met ⇒ CERTIFIED_LEVEL_A → JOB1 headline stands at 2048; then decide (based on whether the
  audit flags them material) whether to spend bounded GPU on 6-seed symmetry + 1280 full-raw backfill.
- Any falsifier fires ⇒ NEEDS_FIX/BROKEN → record the finding (bank-negative if structural), fix, re-audit.
- Independent substrate: dispatched to a Sonnet-5 executor (fresh context); Codex review hook audits the
  diff on completion (advisory, binding-DOWN). This IS the reward-hack-audit mechanism for this claim.
