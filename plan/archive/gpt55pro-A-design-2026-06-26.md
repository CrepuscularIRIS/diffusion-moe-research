# GPT-5.5 Pro (Pro 扩展) — Data-Informed A-Paper Design (2026-06-26)

> Source: Playwright→GPT-5.5 Pro, chat "Data-Informed Paper Review". Follow-up to the AC review, after the
> E-kill. This is the design spine for the LEAD paper (Branch A, equivalence-class measurement). Distilled
> actionable deltas first; full verbatim at bottom.

## ★ AC verdict + the claim to make (reframed — use THIS wording)
A is the paper; E is a negative-control SECTION. **Defensible claim (narrow & strong):** *"For a frozen
block-diffusion LM on verifier-scored reasoning/code tasks, off-policy reference-token denoising is not a
reliable observable of task competence, even when the model's on-policy sample distribution contains
verifier-correct solutions. The right measurement target is verifier-equivalent on-policy behavior, not
agreement with any one reference string."* **Stop saying "knows"** → "has on-policy access to verifier-equivalent
solutions" / "places sample mass on the verifier-correct equivalence class."

## ★ Q1 — RUN EQUIVALENCE-CLASS SATURATION FIRST (the cheapest decisive A experiment)
NOT the proxy-matrix (too easy to dismiss as "bad proxies"), NOT a bare reference-swap (works→"single-ref
artifact"; fails→"probe artifact"). **Oracle equivalence-class saturation WITH model-own references** attacks
the most dangerous AC objection ("the 2.3% just means the official solution is one arbitrary surface").
Protocol (build to this):
- **Data:** verifier-backed, problem-deduplicated set from the 984-trace audit. Report MATH-L5/AIME/code
  separately; **CLUSTER ALL CIs BY PROBLEM** (problem-level is the primary unit, not trace). The 2.3%-vs-90%
  contrast is MOTIVATION only — give a problem-level reference-proxy statistic for the real claim.
- **Per-problem frozen reference bank R_i (≤30 verifier-equivalent refs), built BEFORE scoring, charitable to
  the reference-likelihood baseline:** official gold; diverse verified AR-solver/prompt/seed full solutions;
  verified DiffusionGemma on-policy 1280-budget solutions from distinct seeds; canonical answer-only templates
  (\boxed{a}, "the answer is …", equivalent LaTeX, simplified fractions/radicals/sets/intervals); for code,
  independently-generated accepted solutions + minimal accepted snippets. **Dedup before scoring** by
  normalized final answer + token edit-distance + solution-shape tags. **NEVER select refs by teacher-forced
  score.** <10 verified refs → "low-bank" sensitivity panel only; main panel = K≥30 subset + all-problem
  sensitivity.
- **Nested K ∈ {1,3,5,10,20,30}**: K=1 = official ref; K>1 sample nested banks 100× (always include official),
  report mean/CI; + one oracle-mix K=30 row.
- **Teacher-forced scoring under the EXACT D3PM-uniform regime, BLOCKWISE** (finalized 256-blocks provided
  exactly; current canvas corrupted; prompt/pad/EOS-tail excluded; score generated-solution tokens only;
  ≥16 corruption draws from the sampler-matched timestep distribution). Keep visible-token copy accuracy as a
  separate sanity metric (don't let uncorrupted tokens inflate the score).
- **Metrics:** BestNLL@K(i)=min_r TFNLL; Top1@K, Top10@K (max over bank of argmax / rank≤10 on corrupted
  positions); **AUC@K = AUC(−BestNLL@K, V_i)** where V_i = on-policy verifier label/pass-rate at 1280. If V is
  near-all-positive, use Spearman ρ vs pass-rate over multiple samples.
- **PRE-DECLARED FALSIFIER (A falsified/weakened if ANY):** (a) saturation repairs the proxy — by K=30,
  BestNLL@K becomes a good verifier surrogate (AUC≥0.75 problem-clustered CI-LB≥0.65, or Spearman≥0.5);
  (b) model-own refs repair the probe — on the subset including DG's own correct 1280 outputs, Top10@K jumps
  AR-like (corrupted-pos Top10≥80%, median target rank≤10) → 2.3% was "wrong reference surface", not a deep
  pathology; (c) bank not saturated — K20→30 improvement >25% of K1→10 → INCONCLUSIVE (can't claim multi-ref
  fails while the curve climbs).
- **★ THE ONE HEADLINE — Figure 1: "Verified-equivalence saturation does not recover reference-token
  observability."** Panel A: K vs {Top1@K, Top10@K, BestNLL@K} w/ problem-clustered bootstrap CIs (incl. the
  current K=1 2.3% as leftmost) — should rise a little then saturate FAR BELOW "recovered". Panel B: K vs
  AUC@K/Spearman vs on-policy verifier pass-rate (random line at 0.5; verifier pass-rate on separate scale).
  If Fig 1 doesn't look like that, the A paper is not ready.

## Q2 — the novel slice SURVIVES (as a narrow measurement paper)
**Sharpest surviving claim = the THREE-WAY SEPARATION:** for frozen block-diffusion LMs, reference-token
observability ≠ denoising/commitment-trajectory observability ≠ verifier-readable final commitment — on
verifier-scored tasks, (i) teacher-forced reference-denoising fails to measure on-policy verifier-equivalent
competence EVEN after reference-set expansion; (ii) trace-dynamics features fail to predict where extra budget
helps (the E-kill); (iii) truncated outputs fail because no verifier-readable surface form was committed, not
because the answer is trivially extractable (parser ~1.9%). Positioning vs prior art: **DUEL** — don't fight
it (different: even proper on-policy likelihood ≠ right observable for verifier utility; include as baseline if
applicable to the shipped sampler, else state precisely why not). **AXE/CTC latent alignment** — survive only
after cheap alignment controls (shift sweep, monotonic alignment, answer-span). **MBR** — compatible (utility
must BE verifier-equivalence; "just sample & rerank" = an on-policy verifier-equivalence method, supports the
thesis). **Generative-Frontiers / Hacking-GenPPL** — yours is narrower (verifier-scored reasoning, not gen-PPL).
**★ MINIMAL AR CONTROL REQUIRED:** closest AR Gemma-4 26B/A4B-it; same prompts/verifier/canonicalization,
matched on-policy accuracy + output length. Pathology is dLLM-specific ONLY IF the AR control does NOT collapse
on its OWN verified surfaces while the dLLM does. Use NLL/rank/Top10/predictive-power (NOT argmax; sampled AR
text isn't argmax token-by-token).

## Q3 — 11 AC kill-shots, each with its preempting control (the validity battery)
1. "2.3% vs 90% invalid comparison" → keep as motivation only; main proof = problem-level BestNLL@K/Top10@K
   AUC/Spearman vs on-policy verifier pass-rate. 2. "one-reference artifact" → Q1 saturation. 3. "wrong
   timestep" → t∈{0.01,0.03,0.05,0.10,0.20,0.40,0.60,0.80}+sampler-matched; curves for all-pos / corrupted-only
   / visible-copy sanity (near-0 corruption must copy). 4. "argmax too harsh" → target-token rank, Top5/10/50,
   NLL, entropy-normalized NLL, calibration (survives only if refs are low-rank/non-predictive after
   saturation). 5. "off-by-one/shift/block-boundary bug" → shift sweep Δ∈[−5,5]; BOS/EOS/pad/whitespace
   variants; block-boundary stratification (first16/mid/last16/cross-canvas); AXE/CTC monotonic-alignment;
   tokenizer round-trip; synthetic copy-denoise sanity. 6. "whole-solution hides answer knowledge" →
   final-answer-span-only / last-line / \boxed{} span / answer-only templates / cloze-infill (prefix given,
   only answer corrupted) / numeral-vs-symbol-vs-prose categories (claim survives only if answer-span ALSO
   fails). 7. "canonicalization explains it" → canonical variant union as answer-only refs. 8. "raw vs
   sampler-processed logits" → raw vs processed; with/without self-conditioning; exact pre-commit logits; exact
   entropy-bound/acceptance policy; same temp/top-k/p as harness (DiffusionGemma docs emphasize
   denoise/renoise/entropy-stop). 9. "verifier too lenient" → stratified audit (verifier-correct-ref-low /
   verifier-wrong-ref-high / rescued / parser-miss); ≥2 normalizers + human spot-check; code: hidden/mutation
   tests. 10. "generic CoT badness" → AR sibling self-reference control (the critical contrast = own-surface
   recoverability). 11. "single model/tiny benchmark/leakage" → problem-clustered bootstrap, leave-one-problem-
   out, a 2nd dLLM if affordable else scope title as a DiffusionGemma CASE STUDY (don't overclaim "diffusion LMs").

## Q4 — the E-kill IS an asset (short main section, ~1–1.5pp): "Obvious repairs do not explain the gap"
Logic: budget rescue is REAL (36/134, 0 inversions); parser rescue is NOT the explanation (~1.9% MATH/0% AIME);
learned commitment allocation is NOT supported (dynamics/temporal-order/dynamics+nfe fail to beat simple
controls). **Careful wording:** NOT "not budget-fixable" → say *"failures are budget-SENSITIVE but not
selectively budget-ALLOCATABLE from the observed 768-step trace dynamics."* **Cheap extra analysis that makes
it land (on existing 984 traces): a SELECTIVE-ESCALATION UTILITY CURVE** — within C, label y=1[wrong@768→
correct@1280]; for each score family {dynamics-CV, shuffled-dynamics, final-entropy, nfe@768, dynamics+nfe,
parser-flag, random, oracle} rank traces by predicted rescue value; for escalation fraction q∈{5,10,20,30,50,
100%} report rescues-captured / accuracy-gained / extra-NFE / gain-per-1k-NFE / problem-clustered CI. Figure:
oracle far above; learned-dynamics≈shuffled≈random; nfe/final-entropy the only weak simple controls →
"extra budget rescues real failures, but the 768 trace exposes no usable signal for WHERE to spend it."
Main paper = one decision-curve figure + a compact table of the 3 kill facts (rescue exists / parser can't
explain / adaptive ranking fails); classifier details to appendix.

## Execution implications (for our run)
- The in-flight **Blocker-#1 recompute** (node 5.1.1) = the probe-validity + K=1 + artifact-battery PREREQUISITE
  of this saturation experiment; its result gates whether we proceed (CONFIRM) or redesign (ARTIFACT).
- If CONFIRM → Codex-rigor the SATURATION design (this doc Q1) → build (needs the 30-ref bank: external AR
  solver solutions + DG-1280 solutions + canonical templates; an AR Gemma-4 control). 
- E-asset selective-escalation curve = cheap CPU analysis on the existing 984 traces (do during saturation).
- AR Gemma-4 26B/A4B-it availability = a dependency to confirm.

---
## Full verbatim transcript
(Saved above in distilled form; raw text is in the chat "Data-Informed Paper Review". Key prior art named:
DUEL, AXE + CTC latent alignment, MBR decoding, Generative Frontiers, Hacking Generative Perplexity. Repeated
emphasis: problem-level clustering, model-own references, the AR self-surface control, and corrupted-only
scoring under the exact D3PM regime.)
