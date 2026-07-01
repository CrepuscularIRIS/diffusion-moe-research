# N2 Pre-registration AMENDMENT v2 — dev-gate forced a gate re-spec (2026-06-28)

> FROZEN before any SEALED N2 data is seen (integrity-preserving). Triggered by the N2 dev-gate (n=32):
> the v1 sanity gate fired `sanity_failed_STOP` for the WRONG reason. Two independent reviews (Codex DECIDE +
> the executor) converged: the GoldTop1 round-trip gate is mis-calibrated (teacher non-uniqueness). This doc
> voids that gate, freezes a replacement, and adds the controls needed to separate mechanism from artifact.
> Supersedes `n2-amendment-codex-2026-06-28.md` FIX 3 sanity-gate clause. Tree node 5.3.1.1.

## What the dev-gate showed (n=32 MATH≤4 @2048, ceiling=1.0, integrity '7+5'→'12' OK, zero NaN)
Verified-accuracy @K12 (the contractual top-line): native 0.94 | g4_soft_cont **0.97** | nat_discrete 0.94 |
nat_cont 0.875 | n2a 0.84 | n2b 0.78. @K6: native 0.72 | g4_soft_cont 0.625 | nat_discrete 0.66 | nat_cont
0.47 | n2a 0.41 | n2b 0.56. NFE comparable (g4_soft_cont 24.8 vs native 21.6 @K12). vs the SNAP versions
(prior sealed): g4_soft(snap) 0.06 → g4_soft_cont 0.97; n1b 0.63 → n2b 0.78; n1a 0.72 → n2a 0.84. Removing the
per-step NN-snap recovers +15…+90 pts. ★ This points toward **snap-was-the-codec-artifact** (the N1b kill was
codec-confounded), the OPPOSITE of the broad "no usable continuous interface" negative.

## Why the v1 sanity gate is VOID (mis-specified, not waived for convenience)
v1 gate = n2a round-trip GoldTop1 ≥0.99 (feed exact clean E[y*]; does argmax f_θ(E[y*])==y* per token?).
- GoldTop1 reads 0.14–0.17 for n2a BUT also only **0.45 for the on-manifold, in-distribution `nat_discrete`**
  control whose verified acc is 0.94. A metric that reads ~0.2–0.45 when the model is fed its NATIVE input and
  still solves the problem is decoupled from correctness — it is dominated by **teacher non-uniqueness** (the
  model emits correct answers via different tokens/phrasing). The amendment v1 itself says "token recovery is
  interpretive only; verified acc is the main metric" — so building the STOP gate on GoldTop1 was an error.
- Numerical preservation is fine: carried-latent relerr ‖Z_{K-1}−E[y*]‖/‖E[y*]‖ = 0.082 @K12; scale OK
  (estar_norm≈87.5, z_norm≈48, √2816=53); zero NaN. The interface is numerically sane; it is not an exact echo.
- **Decision:** the GoldTop1≥0.99 round-trip / GoldTop1≥0.90 consumability gates are declared MIS-SPECIFIED for
  answer-level N2 claims and VOID. We make NO claim that the interface is an exact clean-token autoencoder.

## FROZEN REPLACEMENT SANITY GATE (v2) — based on verified-acc + numerical preservation + a teacher-free probe
The codec-free path is "numerically valid enough to interpret" iff ALL hold at every declared K:
1. **Numerical preservation:** n2a carried-latent relerr ≤ 0.10 (@K12) / ≤ 0.20 (@K6); zero NaN; z/estar norm ratio in [0.4,1.6].
2. **Oracle answer recovery (the real top-line):** n2a verified-acc ≥ 0.90·native_K (the oracle round-trip recovers ~native ANSWER accuracy). This replaces "exact-token echo" with "answer-faithful echo," robust to teacher non-uniqueness.
3. **Teacher-free echo diagnostic (logged, interpretive):** feed e(v) for a fixed set of RANDOM valid tokens v (no reasoning trace) at the cleanest level; report argmax-recovery and relerr — isolates interface numerics from reasoning rewriting. (Not a hard gate — a sanity diagnostic; flag if recovery ≪ native's own clean self-consistency.)
If 1&2 hold → PROCEED (interface interpretable). If 1 or 2 fail → STOP (genuine interface limitation).
ALL per-K bins use the existing problem-clustered bootstrap CIs (PASS/FAIL/INCONCLUSIVE), declared-K coverage as in v1.

## REQUIRED NEW CONTROLS (the final-commit-artifact disambiguator — Codex DECIDE)
The live confound: g4_soft_cont 0.97 even > oracle nat_cont 0.875 → maybe the continuous trajectory is irrelevant
and the single final model-argmax commit does the work. Add:
- **commit-only / K=1 baseline** (`commit_only`): feed the initial (noisiest) state, do ONE model-argmax commit,
  no continuous trajectory. If this already ≈0.97 → trajectory irrelevant → final-commit artifact.
- **step-ablation**: run g4_soft_cont (and native_rescaled, and n2b) at K ∈ {1,2,3,6,12,24}, NFE-accounted. A real
  denoising trajectory ⇒ acc RISES with K (and lags native at low K, as already seen @K6). Flat-from-K=1 ⇒ artifact.
- **trajectory-matched controls**: add a native-discrete ITERATIVE carrier and a native-continuous ITERATIVE carrier
  so (i)/(ii)/(iii) compare like-for-like (current nat_discrete/nat_cont are per-level read probes, NOT comparable
  to the iterative g4_soft_cont — fixes the g4_soft_cont>nat_cont non-comparability).
- **final-call perturbation**: randomize/perturb ONLY the final model call while keeping the prior trajectory; if
  acc collapses only there, attribution is the final commit.

## VERDICT SPLIT (report TWO questions, not one combined success)
- **Q1 — snap artifact?** Does removing the snap recover answer-acc vs the snap version (g4_soft_cont vs g4_soft;
  n2b vs n1b; n2a vs n1a), CI-backed at all declared K? YES ⇒ the snap codec was a major artifact; the prior N1b
  structural-kill was codec-confounded → WITHDRAW N1b as evidence for "model can't integrate a continuous field."
- **Q2 — continuous-trajectory mechanism?** Does the continuous TRAJECTORY (not the final commit) do the work?
  Decided by step-ablation (acc rises with K) + commit_only being LOW + final-call-perturbation collapsing only at
  the end. YES ⇒ "the frozen discrete dLLM hosts a usable continuous embedding-flow interface accessible WITHOUT
  training, by NOT snapping" (the strong, top-venue positive). NO (commit_only already high) ⇒ the recovery is a
  final-decoder effect, not continuous integration → narrower claim.
- Top-venue positive requires Q1=YES AND Q2=YES on SEALED (n=134 hard + AIME). Q1=YES, Q2=NO ⇒ still a strong
  "codec-artifact localization" result (withdraw N1b) but not a continuous-mechanism claim.

## Plan
Implement controls + replacement gate + verdict-split → re-run DEV gate (validate the new gate + read step-ablation)
→ if PROCEED, run SEALED N2 (MATH-L5 n=134 + slopes + AIME) → Codex DECIDE on Q1/Q2 → Pro 扩展 novelty/framing of
the emerging positive. Integrity: this v2 is frozen BEFORE any sealed N2 data.
