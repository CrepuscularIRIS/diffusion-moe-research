# GPT-5.5 Pro (Pro 扩展) AC-level Review — Unified "E+A" Paper (2026-06-26)

> Source: Playwright→GPT-5.5 Pro, chat "Frozen Diffusion LLM Review" (thought 9m21s). Independent senior
> design/novelty/AC review of the E+A bet, conditional on the rescue-audit outcome. This is a DESIGN input,
> not a result. Distilled actionable deltas first; full verbatim transcript at bottom.

## ★ ACTIONABLE DELTAS (what changes because of this review)
1. **★★ NEW MAKE-OR-BREAK CONFOUND (Q4): "truncation headroom" may be "verifier-FORMAT headroom".** If many
   768-misses already CONTAIN the correct answer but UNBOXED, the right fix is a better extractor / answer-first
   prompt / box-suffix completion — **NOT more canvas budget**. → **Add a ZERO-EXTRA-COMPUTE PARSER BASELINE**:
   from each 768 trace extract the last numeric/symbolic answer candidate and score it AS-IF-BOXED; report the
   fraction of truncation-misses recovered. If large → E (budget) is NOT the headline; pivot to the
   "answer-commit" module (see #6). **This is now a required Phase-1 control in the running rescue audit.**
2. **Lead with A, not "E+A unified" as phrased (Q1).** Strongest spine = *"A frozen block-diffusion LM can KNOW
   a verifier-equivalent solution without COMMITTING a verifier-readable surface form; the right observable is
   on-policy verifier-equivalence, not reference-token likelihood."* A = conceptual/measurement claim leads;
   E = causal payoff ONLY if the rescue audit survives the hard controls.
3. **A's surviving novel slice = the TRIPLE MISMATCH (Q2a)**, NOT "single-ref metrics are bad" (DOA — pre-empted
   by MBR decoding, AXE/CTC latent-alignment NAT, DUEL, Generative Frontiers, Hacking-Generative-Perplexity):
   (i) reference mismatch (verifier-equiv ≠ gold ref); (ii) **trajectory mismatch** (teacher-forced probes
   condition on a trajectory the model would NOT generate); (iii) **commitment mismatch** (correct evolving
   canvas, fails to emit final surface form before block/canvas limit). The 2.3%-vs-90% is publishable ONLY if
   proven not an artifact of high-noise timesteps / token shifts / answer-only scoring / poor canonicalization
   / argmax-vs-top-k.
4. **E's surviving slice (Q2b) = "verifier-calibrated MARGINAL VALUE of extra canvas budget for already-
   uncommitted reasoning traces", at the PROBLEM-level budget-allocation layer** (NOT token-acceptance). Closest
   prior art to differentiate from: **TraceLock** (learned token-commitment policy from trace-state features —
   conceptually nearest), Fast-dLLM (confidence parallel decode), APD, Learn2PD, SAS (reveal-order), Prophet
   (early-commit on confidence gaps), Rainbow Padding (EOS/padding length fix). Must beat STRONG controls:
   no_box×hit_cap interaction, length/distance-to-cap, final-entropy/slope/stability-count, **"last answer
   candidate exists but unboxed" PARSER baseline**, **"append answer/box suffix" baseline**, random-within-C,
   uniform-longer-equal-NFE, native-EB-tuned, and a **string-features-only logistic**.
5. **Resampling confound (Q4):** 768→1280 as independent draws ≠ "same reasoning + more budget". Need SAME-SEED
   paired traces and CONTINUATION-style interventions from the 768 state (Phase-2). Our 3-seed design uses
   same seed-ids across budgets but block-count differs → flag; the online-intervention exp (below) is the fix.
6. **★ HIGHER-VALUE HIDDEN CONTRIBUTION (Q4): latent-answer-convergence vs textual commitment.** If the evolving
   canvas/partial trace already contains a STABLE final answer before emission, you don't need longer
   generation — a **verifier-calibrated "answer-commit" module that extracts+boxes a stable answer from the
   trace** is more interesting than a budget ranker (connects to early-answer-convergence work). Candidate
   pivot if the parser baseline (#1) fires.
7. **Soften "not reasoning"** → "most residual *observable* errors are not explained by lack of solution
   competence under a longer/corrected commitment policy." **Don't train anything on AIME (n=30)**; exact
   paired tests + bootstrap CIs; AIME = final sign test only.

## Conditional titles/abstracts Pro would submit
- **If E survives:** *"Known but Uncommitted: Verifier-Equivalence and Adaptive Budgeting in Frozen Diffusion
  Language Models."*
- **If E killed:** *"Do Not Judge a Diffusion LM by a Reference Token: Equivalence-Class Evaluation for Frozen
  dLLMs."* (Write it as a measurement-FALSIFICATION paper, not a lament about exact-match.)
- **Venue:** ICLR if E becomes a real inference/control method; NeurIPS if it becomes a broad diagnostic
  benchmark + theory; ICML only if the budget policy is a clean decision-theoretic method with strong
  generalization. *A one-checkpoint rescue audit, even impressive, is NOT enough.*

## Killer experiments (Q3)
- **If E survives:** (E1) **budget-value FRONTIER** not one point — budgets {512,768,1024,1280,1536}, train the
  policy to predict MARGINAL utility of extra compute (not correctness); Pareto acc-vs-NFE dominating all
  controls across budgets. (E2) **turn the audit into an ONLINE INTERVENTION** from the 768 trace state:
  compare 4 branches from the SAME 768 trace {stop, full-1280-rerun, continue/extend-from-768, cheap
  answer-suffix/box completion}; if trace-risk features predict which branch works → control paper; if only
  full reruns help → mostly scheduling. ABLATION: shuffle temporal order of trace features / final-text-only
  features — if they tie, the "trace dynamics" story dies.
- **If E killed (A-only):** (A1) **equivalence-class saturation** — 10–30 verifier-equivalent references/problem
  (derivation orders, concise/verbose, renamings, answer-first/proof-first, code-style variants, model-correct
  solutions); evaluate token CE / per-position argmax / edit distance / AXE-CTC aligned losses / answer-only
  token loss vs on-policy verifier correctness; + AR control (pathology must be larger for dLLM). (A2)
  **proxy-optimization falsification matrix** across checkpoints/interventions — include the SFT that halves
  diffusion loss with 0 accuracy gain PLUS a converse intervention that improves verifier accuracy while
  leaving reference CE unchanged/worse (box-first prompting, final-answer reservation, answer-suffix). A metric
  is invalid if optimizing it doesn't improve utility AND improving utility doesn't improve it.

---

## Full verbatim transcript
(See chat "Frozen Diffusion LLM Review"; key content captured above. Raw text:)

My AC-level verdict — The strongest paper is NOT "DiffusionGemma is near-perfect and just needs more tokens"
(reads as a decoding/config note). Strongest spine: a frozen block-diffusion LM can know a verifier-equivalent
solution without committing a verifier-readable surface form; the right observable is on-policy
verifier-equivalence, not reference-token likelihood. Lead with A; E is the payoff only if the rescue audit
survives hard controls. DiffusionGemma's serving path makes "commitment" a real architectural object (vLLM:
256-token canvases denoised in parallel, committed block-by-block, entropy-bound acceptance + convergence/
step-cap rules before emitting clean argmax tokens).

[Q1/Q2/Q3/Q4 fully distilled above. Notable prior-art named: MBR decoding; AXE + CTC/Imputer latent alignment
(NAT); DUEL (likelihood under deterministic unmasking policy); Generative Frontiers; Hacking Generative
Perplexity; Fast-dLLM; APD; Learn2PD; TraceLock (closest to E); SAS; Prophet; Rainbow Padding.]
