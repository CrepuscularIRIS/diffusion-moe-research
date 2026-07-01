# Research Redesign — Equivalence-Class Evaluation of Diffusion LMs (2026-06-26)

> Source: GPT-5.5 Pro (专业) first-principles redesign + the 4 pivotal post-fix findings (RUNLOG Cycle 7b).
> Supersedes the residual-calibration slice as the PRIMARY direction. This is the new research spine.

> ### ★ RESOLVED BET (Codex SELECT, 2026-06-26 — after the failure-profiling evidence) — READ FIRST
> The bet is **"E + A UNIFIED"**, NOT A standalone: *"Correctness in dLLMs is a verifier-defined equivalence
> class; DiffusionGemma's residual verifiable-task failures are either MIS-MEASURED surface forms (A) or
> UN-COMMITTED solutions / sampler truncation (E) — not reasoning failures. The intervention is
> verifier-calibrated COMMITMENT + BUDGET allocation."* Roles: **A (below) = the measurement spine/objective**;
> **E = the lead method** (adaptive answer-commitment / budget controller on AIME/MATH-L5); D = E's risk head;
> B = the correctness-compute frontier plot; C (Kaiming-He) = deferred future-training (not killed).
> **★ LEAD FIRST EXPERIMENT = the 768-vs-1280 matched-compute RESCUE AUDIT** (see `plan/goal-directive.md`
> "CURRENT BET" for the full protocol + success/kill thresholds): does a learned risk-ranker that allocates
> extra budget to high-truncation-risk problems beat uniform-bigger-budget AND the EB-sampler's native
> early-stop AT MATCHED COMPUTE? If heuristics/uniform match it → E is engineering, fall back to A alone.
> The Branch-A "Reference-Swap Falsification" below remains the cheap parallel measurement experiment.
> Profiling evidence (tree node 5.6): model near-ceiling except AIME 73%/MATH-L5; truncation is the dominant
> failure mode; "thinking mode" is a trap.

## Why we pivoted (the premise shift)
After repairing the silently-corrupted, digit-blind checkpoint, the TRUE picture emerged:
1. Pretrained DiffusionGemma = **90% GSM8K** exact-match; LoRA SFT = 88% (tied) despite **halving** held-out
   diffusion loss (7.66→3.62). → SFT/diffusion-loss gains do NOT translate to task accuracy.
2. **Held-out diffusion loss is an invalid quality proxy.**
3. **Surface-form / equivalence-class diversity**: teacher-forced per-position argmax matches the gold-REFERENCE
   token only **2.3%**, yet free-gen exact-match = **90%**. The model reaches correct answers via different
   surface forms; it is **jointly coherent**, not "cursed". ALL reference-token / teacher-forced probes
   (diffusion loss, the co-commit oracle, H5 ΔNLL) systematically mismeasure it.
4. GSM8K is saturated; the forward-pass-loss methodology we leaned on is invalid as a success signal.

## PRIMARY (bet): "One Reference Is Not a Target — Equivalence-Class Evaluation of Diffusion LMs"
**Thesis.** Large diffusion LMs can be sequence-coherent while being severely mismeasured by single-reference
token metrics; the correct target for reasoning/code is **verifier-defined equivalence-class utility**, not
reference-token CE/ELBO/diffusion-loss. DiffusionGemma demonstrates high sequence-level coherence despite
extremely low single-reference token agreement.

**Formal object.** For a verifier U_x, let A_x = {y : U_x(y)=1} (acceptable set). A sampler S is *jointly
coherent under diverse realizations* if Pr_{y∼q_{θ,S}}[y∈A_x] is high while single-reference agreement
RefAgree(x) = (1/|r_x|) Σ_i 1[argmax_v p_θ(v | r̃_t,x,i) = r_{x,i}] is low. The key quantity is the
**equivalence/reference gap** G(x) = Acc(x) − RefProxy(x) (large positive ⇒ useful mass on correct outputs,
not on the dataset's one reference string).

**Novelty / differentiation.** NOT another sampler/router/remasker/commitment policy — it attacks the
**measurement assumption** under all of them. Differentiate from: RADD 2406.03736 / MDLM 2406.07524 (improve
objectives); **DUEL** (exact sampler likelihood); **Generative Frontiers** + **Hacking Generative Perplexity**
(critique *unconditional* text metrics); NAT translation **AXE / latent-alignment** (single-ref CE penalizes
multimodality/word-order); **MBR decoding** (sequence-level expected utility). Our sharper, dLLM-specific claim:
**in verifiable conditional generation, reference-token probes can FALSELY diagnose a coherent large dLLM as
broken/incoherent — and dLLM-specific published probes/design decisions would have reached the WRONG
scientific conclusion on DiffusionGemma** (this last point is the antidote to "single-ref metrics are
obviously bad").

### ★ Cheapest decisive FIRST experiment — Reference-Swap Falsification
For 100–200 prompts across GSM8K (saturated sanity) + MATH + code:
- **Reference pool** R_x = { dataset reference, DiffusionGemma-correct generation, (AR-correct if an AR
  baseline is available), **canonical answer-only** }.
- **Configs**: base, LoRA SFT step_1000, ~3 sampler settings (steps × entropy-bound).
- **Metrics vs EACH reference**: diffusion loss, gold-in-top-k, teacher-forced argmax agreement,
  **on-policy regeneration** L_regen, and the **verifier accuracy** (oracle, reference-independent).
- **DECISIVE POSITIVE**: reference-token rankings of checkpoints/samplers **flip** depending on which *correct*
  reference is chosen, while verifier accuracy is unchanged; loss improvements still fail to predict utility;
  the model scores HIGH on its OWN correct generations (on-policy regen) but LOW on the dataset reference.
- **PRE-DECLARED FALSIFIER**: if multi-reference / canonical-answer-only references RESTORE a high correlation
  ρ(reference proxy, oracle utility), the paper dies / narrows to a warning note. Also dies if: the 2.3%
  vanishes after canonical-answer-only + EOS/padding + corruption-regime fixes; AR baselines show the same
  magnitude/structure (⇒ it's "single-ref CoT eval is bad", not a dLLM contribution); on-policy regen is ALSO
  low for correct DiffusionGemma outputs (⇒ the model isn't coherent on its own outputs).
- **CONTROLS (or it's killable)**: strict answer canonicalization/parser; canonical answer-only prompts (NOT
  just free CoT); EOS/padding + canvas-truncation + position-offset + prompt-leakage audit; teacher-forced
  corruption regime MATCHED to the real D3PM-uniform inference; AR Gemma-4 baseline (with its *fast* decode
  path); paired prompt-level bootstrap CIs; stratify by answer/output length. Headline: ρ(reference proxy,
  oracle utility) ≈ 0 or negative across configs while generation-level verifier metrics stay stable.

## The right METRIC family (replaces reference-token CE everywhere)
Primary = **correctness–compute frontier** F(C) = E_x[ max_{j≤k(C)} U_x(y_j) ], C = wall-clock | total NFEs |
generated tokens | samples. Report AUC_logC, C@80%, C@90%, pass@k, majority@k, latency-per-correct.
NFE-matched comparisons only *inside* DiffusionGemma; wall-clock + quality-matched vs AR. Reference CE /
diffusion loss / gold-in-top-k / teacher-forced argmax appear ONLY as diagnostics, never as success metrics.

## PAYOFF section (Direction 2): "Correctness–Latency Frontiers for Frozen DiffusionGemma"
DiffusionGemma's real value = lower LOCAL latency at MATCHED correctness on verifiable tasks (it's a low-batch
consumer-GPU speed model; Google says quality < standard Gemma 4). Grid steps {4,8,12,16,24,48} × entropy-bound
{0.05,0.1,0.2,0.4} × temperature; compare to AR Gemma-4 (its intended fast path). Accuracy vs wall-clock and vs
total tokens, paired bootstrap CIs. Falsifier: not faster at matched accuracy after AR fast-decode/speculative
⇒ efficiency angle dies. Must NOT be "just a benchmark" — carry the Direction-1 metric insight (+ optionally a
tiny adaptive-compute head, Direction 3).

## OPTIONAL (Direction 3): "Verifier-Calibrated Trace Risk" (adaptive compute)
Tiny frozen-feature head predicts Pr[U_x(y)=1 | trace features: entropy decay, #renoise events, token churn,
final entropy, commit batch sizes, late-step answer stability, on-policy regen] → stop/resample/spend-more.
NOT the dead CRF path (sequence-level, not co-commit-token repair). Falsifier: no gain over final-entropy/
confidence baselines on the correctness–latency AUC. Scope to verifiable reasoning/code (commit confidence is
regime-dependent — 2606.14620).

## Execution order
0. **Profiling (in flight)**: find error-rich tasks (MATH/AIME/code) for real headroom + the Pareto.
1. **Reference-Swap Falsification** (Direction-1 cheapest decisive) — Codex-rigor the design, then run.
2. If it survives → build out the 5-measurement suite (Family A) + Direction-2 Pareto (Family B).
3. Direction 3 (trace-risk) only if a method section is wanted.

## ★ MINIMAL FIRST EXPERIMENT (Codex-hardened, go/no-go before the full suite)
**Blockers to clear FIRST:** (1) RECOMPUTE the "2.3% reference agreement" under the EXACT D3PM-uniform
random-token corruption regime (NOT [MASK], correct self-conditioning, content-only) — confirm it's admissible;
(2) verifier (numeric exact-match) confirmed working on base (done: 90% GSM8K).
**Setup:** 100 GSM8K dev prompts FIXED before generation; require ≥80 with a verified-correct DiffusionGemma
reference (first-correct under FIXED seed order, NOT best-by-loss) else no-go. Configs: `base` + `LoRA SFT
step_1000`.
**3 references/prompt:** `R_dataset` (GSM8K answer), `R_dg` (first verified-correct DG generation, disjoint
seeds), `R_canon` (answer-only `#### <normalized>`).
**Primary metric:** per-token **D3PM reference NLL** under exact uniform corruption (same corruption seeds),
**content-only** tokens. **Secondary:** reference top-10 recall (content-only). **Utility:** numeric verifier
exact-match (reference-independent).
**Anti-circularity (Codex):** lock the reference pool before scoring; full cross-score matrix (every config ×
every reference); **EXCLUDE the diagonal** (a config scoring its own output) from the primary claim; disjoint
generation/scoring seeds.
**Pre-declared thresholds:** verifier stability `|Acc_base − Acc_sft| ≤ 5pp` (paired bootstrap 95%CI ∋ 0);
ranking FLIP: `Δ_R = NLL_base,R − NLL_sft,R`, require `Δ_dataset ≥ +0.25 nats` (CI>0) AND `Δ_dg ≤ −0.10 nats`
(CI<0); EOS guard: flip holds on CONTENT-ONLY tokens (report content/EOS/all separately). Canonical control:
if `R_canon` restores verifier-consistent ranking and the dataset/DG flip disappears → NARROW the claim to
"free-CoT single references are bad" (do NOT proceed to the full suite). AR Gemma-4 baseline deferred to after
the DG-only core survives.
**Headline artifact:** the decision table — "standard dLLM training loss on dataset refs says SFT improved
strongly, verifier accuracy says base≈SFT, and the loss-winner changes with the reference surface ⇒ you would
have shipped the wrong checkpoint."

## What we REUSE / what's now diagnostic-only
- REUSE: the working generation harness (`eval_gsm8k.py`), the sealed-bank + real-vs-shuffle scaffolding, the
  EntropyBoundSampler grid, `two_pass_forward` for teacher-forced reference scoring.
- DEMOTED to diagnostic-only: held-out diffusion loss, gold-in-top-k, teacher-forced argmax, H5 ΔNLL,
  the M-PCRH co-commit oracle. None are success metrics anymore.
