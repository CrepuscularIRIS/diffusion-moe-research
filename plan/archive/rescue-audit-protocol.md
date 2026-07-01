# Branch E — Lead Experiment: 768-vs-1280 Matched-Compute RESCUE AUDIT (DRAFT for Codex rigor-review)

> Status: DRAFT v1 (Opus generated, 2026-06-26). Pre-registration for the lead-method experiment of the
> "E+A unified" bet. MUST pass Codex rigor-review-before-build before dispatch to a worktree subagent.
> Grounded in: substrate map of profiling worktree `agent-a063aedce852d9538`; dataset counts verified offline.

## 0. One-paragraph thesis (the question this experiment answers)
DiffusionGemma's residual verifiable-task failures are dominated by **sampler TRUNCATION** (reasons correctly,
never commits `\boxed{}` before the 256-token canvas / block budget runs out), not reasoning (profiling node
5.6: MATH 83→94% and MBPP 82→92% from `max_new_tokens` 768→1280 alone; 3/4 AIME + 2/3 MATH misses are
truncation). **Branch E asks the LEAD question:** can a tiny **verifier-calibrated risk-ranker**, given a
*fixed extra compute budget*, allocate that budget to the truncation-prone problems **better than** (a) the
EntropyBoundSampler's native early-stop, (b) uniform-bigger-budget, (c) random, and (d) trivial surface
heuristics {no-box@cap, generated-length, final-entropy}? If a *learned* ranker cannot beat trivial heuristics
at matched compute → E is **engineering, not a paper** → fall back to A (measurement spine). Either way the
result advances the goal (a clean KILL is success).

## 1. Hypothesis / Falsifier / Acceptance (pre-declared, frozen before any scoring)
- **H_E (directional):** At MATCHED total compute, budget allocated by a learned risk-ranker R(features@768)
  yields strictly higher verifier accuracy on AIME-2024 + held-out MATH-L5 than the best of the
  {native-EB, uniform-bigger, random, no-box, length, final-entropy} controls.
- **PRIMARY ACCEPTANCE (either suffices, both reported):**
  1. **Beat-best-control:** Acc(learned) − Acc(best non-learned control) ≥ **+5 pp**, prompt-level paired
     bootstrap 95% CI lower bound > 0; AND
  2. **Recovery fraction:** learned allocation recovers ≥ **30%** of the full-1280 accuracy gain
     (Acc_all1280 − Acc_all768) **at matched compute** (i.e., spending only the same total NFE budget that
     a uniform partial upgrade would), paired bootstrap CI > 0; AND
  3. **Locality co-metric:** truncation-failure fraction (no-box AND/OR hit-cap) at least **halved** on the
     reallocated set vs the 768 baseline.
  → Declare E a PAPER if (1 OR 2) holds AND (3) holds.
- **PRE-DECLARED FALSIFIER / KILL:** any non-learned control (esp. no-box@cap or final-entropy) matches the
  learned ranker within the paired-bootstrap CI (CI for Δ contains 0) → **E is engineering, KILL E as a
  method, fall back to A alone.** Also KILL if rescue-positives are too few to estimate (< ~15 across the
  combined train+test pools) → the phenomenon is too rare to build a method on (report as a measurement note).

## 2. Estimands & compute accounting (what "matched compute" means — frozen)
- **Compute currency = total NFEs** (= Σ_problems denoising_steps × canvas_blocks_used). Report wall-clock and
  generated-token totals as secondary. NFE-matched comparisons happen ONLY inside DiffusionGemma.
- **Budget axis** = `max_new_tokens` ∈ {768, 1280} ⇒ {3, 5} canvas blocks of 256 (block-diffusion). 768 = the
  "cheap" baseline budget B0; 1280 = the "rescue" budget B1.
- **Allocation game (OFFLINE, no re-generation once both runs + traces exist):** Baseline gives every problem
  B0. A policy picks a subset S (|S| = K) to "upgrade" to B1; the rest stay at B0. Realized accuracy =
  Σ_{x∈S} correct@B1(x) + Σ_{x∉S} correct@B0(x). Total compute = Σ NFE@B0 + Σ_{x∈S}(NFE@B1 − NFE@B0).
- **Matched-compute curve:** sweep K from 0 to N; for EACH policy plot Acc vs total-NFE. The decisive
  comparison is **policies AT THE SAME total-NFE** (interpolate on the NFE axis). Headline number = area
  between learned and best-control curves, plus Acc at the NFE budget where uniform-bigger spends its average.
- **Controls are all evaluated on the SAME offline outcome tables** (correct@B0, correct@B1, NFE@B0, NFE@B1),
  so the only thing that differs between policies is the *ranking that picks S*. This isolates "the ranking"
  as the single variable.

## 3. Data (frozen pools; B_test sealed)
- **TRAIN pool (ranker fit):** MATH-500 level-5 = **134 problems** (full L5; not the stride-12 the profiling
  used). Source `HuggingFaceH4/MATH-500` split=test, filter level==5, deterministic order by `unique_id`.
- **TEST pool (cross-distribution, primary):** **AIME-2024 = 30 problems** (`Maxwell-Jia/AIME_2024` train,
  full I+II — profiling used only 15). Plus **held-out MATH-L5** via 5-fold CV within the 134 (report both).
- **Power note (FLAG for Codex):** AIME N=30 ⇒ 5pp ≈ 1.5 problems — borderline. Mitigations: (i) lead on the
  recovery-fraction + matched-NFE-curve metric (uses the whole pool, more powerful than a single pp gap);
  (ii) 5-fold CV on MATH-L5 (134) as the higher-powered primary, AIME as cross-distribution generalization;
  (iii) OPTION to download AIME-2023 + AIME-2025 (~45–60 more) for test power — needs network + HF token.
  Codex to rule on whether to expand before building.
- **Sealed layer (NEVER modified):** verifier (`math_verify` + `\boxed{}` extractor), dataset rows, the EB
  sampler config. No tuning of the verifier or sampler thresholds to the outcome.

## 4. Generation plan (what the worktree subagent BUILDS & RUNS)
For every problem in {MATH-L5 134, AIME-2024 30} at BOTH budgets B0=768 and B1=1280:
- **Decode = shipped `generation_config.json`** (EntropyBoundSampler, t_max=0.8/t_min=0.4,
  max_denoising_steps=48, entropy_bound=0.1), reusing `_build_balanced_device_map(30, split=16)`, bf16, eager.
  Reuse the profiling loaders/verifiers verbatim (sealed).
- **Stochasticity control:** **M = 3 seeds** per (problem, budget) — seeds {42,123,7}. `correct@B` :=
  majority-correct over seeds (and report pass@1 mean). This (a) de-noises "rescue" labels and (b) lets us
  measure **budget-inversions** (correct@B0 → wrong@B1) to confirm budget monotonicity is the real effect.
- **★ INSTRUMENTATION (the missing piece — must be built):** hook the EntropyBoundSampler denoising loop to
  log, PER PROBLEM × SEED × BUDGET, a trace-feature vector available **from the B0 run only** (the ranker may
  use ONLY B0-observable features — no peeking at B1):
  - blocks_used, denoising_steps_used, generated_tokens, hit_cap (gen_tokens≥budget), early_stopped;
  - per-step mean token entropy → {final_entropy, entropy_decay_slope, entropy_at_step_k};
  - #renoise/remask events, token churn (Σ position re-commits), commit-batch sizes per step,
    late-step answer stability (does a `\boxed{}` appear and stay in the last J steps?);
  - no_box@B0 (no `\boxed{}` in B0 output), surface features (prompt tokens, operator density).
  Persist as JSONL: one record per (problem, seed, budget) with all features + correctness + NFE.
  **Build discipline:** the instrumentation hook is unit-tested on a tiny fake-sampler fixture BEFORE the 26B
  run (mirrors how direction_c/h4 was built), and must be a *read-only* hook (must not change generation —
  verify by asserting instrumented vs un-instrumented outputs are identical on a 3-problem smoke).

## 5. The policies (one ranking variable; everything else identical)
All consume the SAME offline outcome+trace tables; each outputs a ranking → pick top-K for upgrade:
1. **learned (the method):** tiny model (L2-logistic AND gradient-boosted trees, report both; pick by CV)
   on B0 trace features → P(rescue) = P(wrong@B0 ∧ correct@B1). Fit on MATH-L5, applied to AIME (frozen).
2. **native-EB:** trust the sampler — upgrade the problems the EB sampler *did not* early-stop / that used
   the most blocks at B0 (i.e., "the sampler already says these are hard").
3. **uniform-bigger:** no ranking — give everyone the same intermediate budget B' s.t. total NFE matches the
   top-K-upgrade compute (the trivial "just raise the budget for all" baseline).
4. **random:** random subset S (negative control; 1000 resamples → CI).
5. **heuristic-nobox:** rank by no_box@B0 then hit_cap@B0 (the *trivially-right* truncation signal).
6. **heuristic-length:** rank by generated_tokens@B0 (proxy for "ran long / hit cap").
7. **heuristic-final-entropy:** rank by final_entropy@B0 (needs instrumentation).
8. **oracle (ceiling, not a control):** rank by true rescue label — upper bound on any ranking's value.

## 6. Negative controls & locality (or the result is uninterpretable)
- **NC1 score-shuffle:** permute the learned ranker's scores across problems → must collapse to ≈ random
  (proves the ranker carries real signal, not a label leak).
- **NC2 genuine-flip filter:** rescues must be TRUNCATION rescues. Stratify rescued problems by B0 failure
  mode; a "rescue" of a problem that was `genuine-wrong-answer@B0` (emitted a wrong `\boxed{}`, then correct
  @B1) is stochastic noise, NOT budget → report truncation-rescues separately; the locality claim (§1.3) uses
  ONLY truncation-mode rescues.
- **NC3 budget-inversion audit:** count correct@B0→wrong@B1. If inversions ≈ rescues, "budget helps" is noise
  not signal → the whole premise weakens (report; may trigger redesign).
- **LOCALITY:** the learned ranker's advantage must concentrate on no-box/hit-cap problems; show the gain
  vanishes when those strata are removed.

## 7. Reproducible evidence to emit (the 验收 artifact)
- `outputs/rescue_audit/traces_{math_l5,aime}_{768,1280}.jsonl` (per problem×seed×budget; features+correct+NFE).
- `outputs/rescue_audit/paired_table.csv` (problem, correct@B0, correct@B1, NFE@B0, NFE@B1, B0 features, mode).
- `outputs/rescue_audit/matched_compute_curves.json` (Acc vs total-NFE per policy + bootstrap CIs).
- `outputs/rescue_audit/VERDICT.md` (the decision table: each acceptance/kill criterion with its number+CI).
- All commands + exit codes appended to RUNLOG; git branch/commit recorded; seeds fixed; checkpoint shard SHA
  integrity asserted at load (lesson #1).

## 8. Estimated cost (timing-probe FIRST — lesson #2)
~ (134+30) problems × 3 seeds × 2 budgets = 984 generations. Profiling reported AIME ~6.4 s/ex @1280; assume
~10–30 s/ex with instrumentation ⇒ ~3–8 GPU-h on the 2×4090 (serialize; one 26B fits). The subagent MUST run
a 3-problem timing probe and extrapolate before launching the full sweep; kill any job that overruns 2× its
estimate (lesson #5). The ranker fit + offline allocation analysis is CPU-seconds (cheap).

## 9. Open design questions explicitly routed to Codex (rigor-review-before-build)
1. **Power:** is AIME N=30 + MATH-L5 5-fold CV (134) enough, or expand with AIME-2023/2025 (network) BEFORE
   building? What is the minimum rescue-positive count to even attempt the ranker (we pre-set ~15)?
2. **Counterfactual validity:** is 3-seed majority the right stochasticity control, or do we need coupled
   noise (B0 trajectory = prefix of B1)? Block-diffusion changes #blocks with budget, so trajectories diverge
   — is the offline "upgrade to observed B1 outcome" counterfactual admissible? Any leakage?
2b. **Is the matched-NFE curve the right primary** vs the single ≥5pp gap (which is underpowered on AIME=30)?
3. **Feature leakage:** any B0 feature that secretly encodes B1 (e.g., none should — but audit the list).
4. **Trivial-control risk:** if no-box@cap is the near-oracle signal, is E *dead on arrival* (a learned ranker
   can't beat the trivially-right rule)? Should we pre-emptively reframe E to a HARDER question (e.g., predict
   rescue among the *already-hit-cap* set, where no-box is constant and a learned signal must come from trace
   dynamics)? — this may be the make-or-break design fix.
5. **Verdict required:** DESIGN-SOUND / SOUND-WITH-FIXES (list them) / NEEDS-REDESIGN (→ escalate to GPT-5.5
   Pro). Do NOT rubber-stamp; attack the design.

---

# ★ v2 — CODEX-HARDENED, FROZEN PRE-REGISTRATION (this section supersedes v1; build to THIS)
> Codex rigor-review verdict (2026-06-26, GPT-5.5 xhigh): **SOUND-WITH-FIXES**. The fixes below are baked in.
> Core fix: the v1 unconditional question is **dead-on-arrival as a method claim** (no_box@cap is a near-oracle
> trivial control) → the PRIMARY question is **reframed to be CONDITIONAL on the observable truncation set C**.

## v2.A The reframed scientific question (PRIMARY)
Let **C = { problems with no_box@768 OR hit_cap@768 }** — the set any trivial rule already flags as
truncation-risk. *Within C*, the trivial signals are (near-)constant, so the real question is:
**do TRACE-DYNAMICS features rank the rescuable problems within C better than {final-entropy, length,
native-EB, random}, at matched NFE?** This is the non-trivial, publishable question. Unconditional
whole-pool recovery (v1 §1.2) is now SECONDARY/context only.

## v2.B Frozen design changes (apply ALL)
1. **Primary pool = MATH-L5 (134) with nested 5-fold CV.** AIME-2024 (30) = **external generalization
    sign-check ONLY**, never a method-claim power source (N=30 ⇒ 5pp≈1.5 problems). (Optional, only if a
    reviewer wants AIME as primary: download AIME-2023+2025 first — needs network/HF token.)
2. **Phase-0 positive-count GATE (hard):** after generating the paired tables, COUNT problem-level
    rescue-positives (wrong@768→correct@1280) on MATH-L5. If **< ~25 positives → DO NOT fit/claim a learned
    ranker**; report E as "phenomenon too rare to build a method on" (measurement note) and fall back to A.
    Use GBDT only if positives ≳ 40; else logistic only. STOP-and-report at this gate.
3. **Labels = seed-level expected uplift,** not majority-correct: estimate Ê[correct@1280 − correct@768] per
    problem over the 3 seeds (seeds {42,123,7}, SAME seed-ids across budgets); analyze with **problem-cluster
    bootstrap**. Add more seeds for discordant/candidate cases if label instability or inversions are material.
4. **Leakage-safe feature contract (FROZEN):** ranker uses **B0-only** features. In the CONDITIONAL primary,
    **EXCLUDE no_box, hit_cap, and generated-length** (they define/are constant on C) — the learned model may
    use ONLY trace-DYNAMICS: {final_entropy, entropy_decay_slope, entropy_at_step_k, #renoise, token_churn,
    commit_batch_sizes, late-step answer-stability}. Also EXCLUDE dataset-id, fold-id, problem-order, and any
    gold/answer-derived feature; no feature transform chosen after seeing labels. Nested CV; AIME = sealed holdout.
5. **Budget-inversions (correct@768→wrong@1280)** are counted and reported as NEGATIVE uplift; if inversions
    are comparable in count to rescues → "budget helps" is noise → redirect (the premise weakens).
6. **Instrumentation = SCALAR per-step stats in-loop** (the sampler exposes entropy, accepted masks, renoise
    masks, decoder-pass counts). Do NOT retain logit tensors. **Assert instrumented==uninstrumented outputs**
    on a 3-problem smoke before the full run (read-only hook).

## v2.C Frozen acceptance / kill (revised)
- **PAPER (E is the lead method) iff,** on the CONDITIONAL (within-C) matched-NFE / AUC metric:
  learned ranker beats the **best non-learned control** with **paired problem-cluster bootstrap 95% CI
  lower bound > 0**, AND a meaningful effect size = recovers **≥ 20% of the oracle-within-C recoverable
  uplift**, AND the truncation-failure fraction on the reallocated set is **at least halved**.
- **KILL (E is engineering → fall back to A) iff** any trivial/non-learned control (esp. final-entropy or
  length) matches the learned ranker **within the paired-bootstrap CI**, OR the Phase-0 gate fails (<~25
  positives). A KILL here is a SUCCESS per the goal (clean negative; A becomes the spine).
- AIME result is reported as directional corroboration only (sign agreement), not as an acceptance gate.

## v2.D Build phases for the worktree subagent (STOP-and-report at the gate)
- **Phase 0** (generation + gate): instrument sampler (unit-test on fake fixture + identical-output smoke) →
  timing probe (3 problems) → generate MATH-L5(134)+AIME(30) × seeds{42,123,7} × budgets{768,1280} with
  traces → build `paired_table.csv` + per-trace JSONL → **report rescue-positive count, |C|, rescues-within-C,
  inversions.** If gate fails → STOP, write VERDICT.md (E too rare), hand back.
- **Phase 1** (only if gate passes): fit conditional ranker (nested CV on MATH-L5) on trace-dynamics features
  → matched-NFE allocation within C vs controls → cluster-bootstrap CIs → apply frozen to AIME C-set →
  `matched_compute_curves.json` + `VERDICT.md` (every criterion with number+CI). Record commands+exit codes.
