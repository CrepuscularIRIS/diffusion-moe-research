# Branch A — Lead Experiment: Oracle Equivalence-Class SATURATION (FROZEN, Codex-hardened)

> Pre-registration for the lead A experiment. Sources: GPT-5.5 Pro A-design (`plan/gpt55pro-A-design-2026-06-26.md`
> Q1) + Codex rigor-review (2026-06-26, PROCEED-TO-BUILD with 8 must-fixes) + the CONFIRMED-REAL recompute
> (node 5.1.1, `worktree-agent-a6c7037f7a10061de`). Build to THIS. A clean falsification is a SUCCESS.

## 0. The claim under test (Codex-sharpened — neither self-defeating, trivially-true, nor unfalsifiable)
*"For frozen DiffusionGemma 26B-A4B on verifier-scored reasoning tasks, a PRE-LOCKED bank of verifier-equivalent
reference surfaces — INCLUDING sanitized model-own correct samples — only PARTIALLY recovers teacher-forced
reference-token rank/likelihood (Top10 ~50–66%, NOT AR-like ~80–100%) AND provides NO reliable problem-level
surrogate for on-policy verifier success under the sampler-matched corruption distribution (AUC≈0.5,
Spearman≈0)."* I.e. expanding to an oracle equivalence class does not turn reference-token denoising into a
competence observable; the right target is verifier-equivalent on-policy behavior.

## 1. TWO SEPARATE pre-declared falsifiers (do NOT merge — Codex fix #3)
- **Surface-recovery falsifier:** by K=30, on the subset including sanitized DG-own refs, **Top10@K ≥ 0.80 AND
  median target rank ≤ 10** → the probe is surface-repairable → WEAKEN the claim to "partial recovery, still
  non-predictive" (do NOT claim full mismeasurement).
- **Predictive falsifier (kills A):** BestNLL@K becomes a verifier surrogate — **Spearman(−BestNLL@K, on-policy
  verifier pass-rate) ≥ 0.5**, OR **AUC ≥ 0.75 with problem-clustered CI-LB ≥ 0.65** on pass-rate∈[0.2,0.8]
  strata → A is DEFEATED (route to redesign).
- **Inconclusive:** bank not saturated (see §6) → no claim.
- A SURVIVES iff: Top10@K stays < 0.80 (or, if it clears 0.80, the predictive metrics stay at chance) AND the
  predictive falsifier does NOT fire AND the bank is saturated.

## 2. Data (frozen; problem-level is the unit)
- Verifier-backed, problem-deduplicated set from the 984-trace audit: **MATH-L5 (134)** + **GSM8K-sanity** +
  (AIME/code if cleanly available — report each task SEPARATELY). Cluster ALL CIs BY PROBLEM (Codex #7).
- On-policy verifier label/pass-rate V_i per problem: use the 1280-budget generations. **Coarse 3-seed
  pass-rate may be too granular for Spearman → generate additional on-policy 1280 samples (e.g. 8–16 seeds) per
  problem to get a finer V_i** (GPU; the only generation cost here). Decide N_seeds by a power check.

## 3. Per-problem frozen reference bank R_i (≤30 verifier-equivalent refs) — Codex #1, #5
Compose (charitable to the reference-likelihood baseline): official gold; **sanitized DG-own verified 1280
on-policy solutions from seeds DISJOINT from the V_i-label seeds**; canonical answer-only templates (\boxed{a},
"the answer is …", equivalent LaTeX, simplified fractions/radicals/sets/intervals); [phase-2: diverse verified
AR-solver solutions]. 
- **★ STRIP pad/template artifacts before building (Codex #1, bug e):** truncate DG-own at EOS/<eos>; NEVER
  include `<pad>`(id 0)/`<turn|>`/chat-template tokens in `content_ids`. Re-verify every DG-own ref still
  passes the verifier after sanitization.
- **Dedup BEFORE scoring** by normalized final answer + token edit-distance + solution-shape tags. **NEVER
  select/dedup refs by teacher-forced score.**
- **Anti-circularity as CODE ASSERTIONS (Codex #5):** refs locked before any scoring; DG-own seeds ⟂ V_i seeds
  (assert); dedup not by TF-score (assert); emit a bank manifest SHA. <10 verified refs/problem → low-bank
  sensitivity panel only; main panel = K≥30 subset + all-problem sensitivity.

## 4. Scoring — teacher-forced, EXACT D3PM-uniform, BLOCKWISE (reuse recompute toolchain)
Reuse `worktree-agent-a6c7037f7a10061de/diffusiongemma_sft/refswap_recompute/{build_refs,score_refs,analyze}.py`
+ the verifiers. Blockwise: finalized 256-blocks provided exactly; current canvas corrupted (p=t uniform
replacement, NOT [MASK]); 2-pass self-conditioning; **content-only generated-solution tokens** (exclude
prompt/pad/EOS/template — fix the content-only labeling). Keep visible-token copy accuracy as a separate sanity
metric.
- **★ PRIMARY scoring regime = the SAMPLER-MATCHED corruption/timestep distribution (Codex #2)** — the actual
  block-diffusion sampler's t-distribution, ≥16 draws. Report the full t-sweep {0.01,0.05,0.1,0.2,0.4,0.6,0.8,
  1.0} as SECONDARY (t=1.0 = worst-case, NOT the headline). Low-noise copy must be high (scorer sanity).

## 5. Nested K + metrics (Codex #4)
- **Nested K ∈ {1,3,5,10,20,30}**; for K>1 sample nested banks 100× (always include official ref); + oracle-mix
  K=30. K=1 = official ref (the leftmost = the recompute's dataset-ref point).
- Per-problem: **BestNLL@K** (min TFNLL over bank), **Top1@K**, **Top10@K** (max over bank, corrupted positions).
- **★ PRIMARY predictive metric = Spearman(−BestNLL@K, on-policy verifier pass-rate)** over the multi-seed V_i
  (AUC is ill-posed at saturation). Report **AUC only on pass-rate∈[0.2,0.8] strata**. 
- **1000-rep problem-clustered bootstrap CIs on ALL metrics (Codex #7,#8).** Per-task separately.

## 6. K-saturation criterion (Codex #6) — both required for SATURATED
SATURATED iff **(K20→30 improvement) < 25% of (K1→10 improvement)** AND **absolute ΔTop10(K20→30) < 0.02**;
else INCONCLUSIVE (cannot claim "multi-ref fails" while the curve climbs).

## 7. Headline artifact — Figure 1 "Verified-equivalence saturation does not recover reference-token observability"
- Panel A: K (x) vs {Top1@K, Top10@K, BestNLL@K} with problem-clustered CIs; leftmost = K=1 (the 4.3% point);
  expected shape = small rise then saturate FAR BELOW an AR-like "recovered" band.
- Panel B: K vs Spearman/AUC vs on-policy verifier pass-rate; random line at 0.5; verifier pass-rate on a
  separate scale.
- Decision table: surface-falsifier result, predictive-falsifier result, saturation verdict, per task.

## 8. Phases
- **Phase 1 (build NOW):** {official + sanitized DG-own + canonical} refs, full pipeline, MATH-L5 + GSM8K.
  Unit-test the ref-sanitizer (no pad/template ids) + the bootstrap + the K-saturation logic on a fake fixture
  BEFORE the 26B scoring. Checkpoint integrity check at load. Timing-probe first.
- **Phase 2 (after Phase 1 returns):** add the AR Gemma-4 control (identify + download the closest public AR
  Gemma-4 26B/A4B-it; matched prompts/verifier/canonicalization/length; the dLLM-specific claim needs AR NOT
  to collapse on its OWN verified surfaces while the dLLM does). Plus the E-asset selective-escalation curve on
  the 984 traces.

## 9. Evidence to emit
`outputs/saturation/{bank_manifest.json (+SHA), scores_*.jsonl, saturation_curves.json, FIGURE1_data.json,
VERDICT.md (each falsifier + saturation verdict + numbers+CIs, per task)}`; commands+exit codes in RUN_COMMANDS.log;
fixed seeds; checkpoint shard integrity asserted at load.
