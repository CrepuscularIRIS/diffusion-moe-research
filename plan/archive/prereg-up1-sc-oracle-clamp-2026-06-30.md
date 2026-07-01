# PREREGISTRATION — UP-1 Stage-0A: One-Step SC Oracle-Clamp Causal-Leverage Test

> SEALED CONTRACT (tree node 5.9.5.1). Frozen 2026-06-30 BEFORE any GPU. Kill-only measure-first
> necessary-condition gate. NO head training, NO full generation in Stage-0A. Design route:
> Opus /mos-front → Codex object-shift-audit (DOWNGRADE) + taste-critic (ENGINEERING) → Stage-0 preflight
> (killed the probe-AUC plan) → Pro 扩展 reframe (oracle clamp) → Codex SELECT (FIX-FIRST, 7 fixes baked in here).
> No post-result edits to metric / controls / thresholds / split.

## 0. One-line question
Does the frozen model's **native self-conditioning channel** have **correctness-specific causal leverage** —
i.e., can injecting a *verified-correct, answer-scrubbed* clean-estimate at a decision step move the next
denoising step toward the verified-correct continuation **more than** matched non-correct controls — BEFORE we
commit to training any head? If even this best-case oracle cannot, a learned head (strictly harder) is dead → SEAL.

## 1. Hypothesis
- **H1 (causal-leverage):** at EB decision steps t∈[0.4,0.8], an answer-scrubbed verified-correct clean-estimate
  injected via the native `decoder.self_conditioning` gate moves the next-step native logits toward the
  verified-correct continuation **strictly more** than every non-correct control, with problem-clustered 95% CI
  lower bound > 0.
- **H0 (null = the banked Pareto negative extends to the training axis):** the scrubbed-correct injection moves
  next-step logits toward correct no more than generic/confound controls → the SC channel carries no deployable
  correctness leverage → the frozen near-ceiling model's output is information-complete at the SC interface too.

## 2. Design — Stage-0A (one extra decoder forward per arm; dev-40; KILL-ONLY)
For each problem q in **L5-dev-40** (the 40 non-sealed problems; sealed L5-holdout[40:134]+AIME UNTOUCHED):
1. **Native pass:** run native frozen EB generation; at each decision step k with t∈[0.4,0.8] record the native
   state (canvas z_k, frozen hidden state h_k, native clean estimate m^native_k, native logits L^native_k).
   Record native final verified-correctness (stratification only).
2. **Oracle target (verified-correct clean estimate) + scrub** — BUILD DECISION (executor, Codex-reviewed):
   construct m^correct_k as a *verified-correct* clean estimate for q. Two admissible sources, pick the cleaner
   per format-alignment: (a) a native verified-correct trajectory of q (natural canvas alignment; for the 2–5
   native-wrong problems, sample-K or fall back to (b)); (b) teacher-force the MATH gold SOLUTION for q.
   **Invariant:** the source MUST be verified-correct. Apply the **answer-equivalence scrubber** → m^correct_scrub_k:
   remove the final boxed answer, all numeric/algebraic spans equal to derived answer values, and ALL positions
   after the first point at which the final answer is recoverable. The scrubber is **implemented + unit-tested**
   (final-span removal alone is INSUFFICIENT, per Codex fix #2).
3. **Arms (each = inject a target into the SC pre-hook, run EXACTLY ONE more decoder forward, read next-step logits):**
   - `A0_native` — no injection (baseline next-step logits).
   - `A1_correct_inclusive` — m^correct_k (conservative: probability moved only within native top-k). Upper bound; may leak.
   - `A2_correct_scrubbed` — m^correct_scrub_k (conservative within top-k). **The deployable-analog signal.**
   - `C1_same_problem_wrong` — clean estimate from a same-problem verifier-WRONG trajectory (or wrong-answer
     teacher-forcing). Same context, wrong answer.
   - `C2_swap_same_answer` — m^correct from a DIFFERENT problem with the same final answer string.
   - `C3_swap_diff_answer` — m^correct from an unrelated problem.
   - `C4_position_shuffle` — m^correct_scrub with frontier positions permuted.
   - `C5_time_shuffle` — m^correct from a different step k'.
   - `C6_entropy_matched` — random target matched to m^correct's entropy + top-k mass (nonsemantic).
4. **Outcome Y(q,k):** alignment of the resulting next-step native logits with the **verified-correct
   continuation** at the frontier positions (CE↓ / logit-margin↑ / KL↓ toward the gold continuation token).
   Leakage control is on the injected TREATMENT (scrubbed), not the outcome.
5. **Primary statistic — frozen difference-in-differences (Codex fix #1):** ΔY(arm) = Y(arm) − Y(`A0_native`).
   Signal = ΔY(`A2_correct_scrubbed`) vs the control set {C1…C6}. Problem-clustered bootstrap (cluster = q;
   all decision states within q are one cluster), 95% CI.

## 3. Pre-declared KILL / falsifier (Stage-0A)
KILL (→ SEAL the training axis, do NOT train a head) if ANY:
- (a) ΔY(`A2_correct_scrubbed`) ≤ 0 (scrubbed-correct does not move next-step logits toward correct); OR
- (b) ΔY(`A2_correct_scrubbed`) does NOT exceed **every** control C1…C6 with problem-clustered 95% CI lower
  bound > 0 (scrubbed gain indistinguishable from a confound — context-only, answer-string, generic perturbation,
  or structure-shuffled); OR
- (c) ΔY(`A1_correct_inclusive`) ≫ ΔY(`A2_correct_scrubbed`) while `A2` ≈ controls (all leverage is
  answer-leakage = the PSC-Bridge 5.9.4 failure mode reproduced).

## 4. PASS (Stage-0A) → licenses Stage-0B, NOT a positive claim
ΔY(`A2_correct_scrubbed`) > 0 AND > all C1…C6 (CI lower bound > 0) AND not reproduced by the leak arm pattern.
**dev-40 is KILL-ONLY:** a PASS does NOT claim final accuracy will improve and is NOT a threshold-tuning set; it
only licenses Stage-0B (full generation, forced matched-NFE schedule) and, later, Stage-2 head training.

## 5. NFE / wall-clock accounting (Codex fix #3, #5)
Matched **by construction**: each arm = exactly ONE additional decoder forward from the same native state; no
arm gets more compute. Stage-0B (only if 0A passes) uses a forced fixed schedule with identical decoder-call
counts per problem/arm. Oracle-target acquisition cost (teacher-forcing / sampling) reported SEPARATELY; NO
deployable speed claim from any oracle arm.

## 6. Stage-2 predeclared baseline (Codex fix #7; taste-critic requirement — frozen now)
If Stage-0A+0B pass and a head is trained, SUCCESS requires beating, on a SEALED hard set (L5-holdout/AIME),
by ≥2pp verified accuracy at matched NFE + wall-clock with clean controls: (i) native EB, (ii)
always-deepen-to-matched-mean, AND (iii) a **same-supervision / same-compute** trained baseline — a
BackPlay-style scalar correction head + a verifier-supervised reranker/allocator of equal params/compute. Native
+ always-deepen alone are insufficient.

## 7. Integrity / engineering
- Shard guard `integrity()` 7+5→12 must pass at load (SystemExit on fail).
- `replay/no-op` invariant: `A0_native` reproduced exactly by a null injection (plumbing check; abort if not).
- Metrics generation/verifier-based; diffusion loss diagnostic only.
- Build base: psc-oracle worktree @ a0cb9a2; reuse model load + EB sampler + `decoder.self_conditioning`
  pre-hook + verifier + dev loader; build-new: decoder-hidden capture (decoder.norm), oracle-target+scrubber,
  the 9 arms, the difference-in-differences + problem-clustered bootstrap, CPU unit tests (mirror the 100-test
  embflow convention; the 26B is never loaded in tests).
- Budget: ≤3h dev; kill-9 on overrun OR >30min zero-output. ONE 26B job (nvidia-smi recheck before launch).

## 8. Preregister hash
Freeze SHA256 of this file's bytes (computed at dispatch) into the RUNLOG + tree before the run; no edits after.
