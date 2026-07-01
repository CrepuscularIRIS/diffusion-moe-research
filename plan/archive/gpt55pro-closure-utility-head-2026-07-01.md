# GPT-5.5 Pro (Pro 扩展) design — O1 = Closure-Utility Head — 2026-07-01

> Lateral-jump re-IDEATE after the tree-5.11.1 occupancy kill (beyond-Markov dependency head OCCUPIED by
> DEMASK/CoDD/FeF-DLLM). Pro designed the near-original object; Opus packaged (verbatim). NOT self-certified —
> eligibility comes ONLY from `/object-shift-audit`. Arbor node 5.11.2. Chat: chatgpt.com/c/6a44a91a.

## Object-shift (enrich)
- **WRONG object O0** = frozen DiffusionGemma factorized denoiser `p0(x0|xt) = ∏_{i∈Mt} p0(x^i | h^i)`, with
  EntropyBoundSampler committing positions by confidence/entropy. It models per-position token identity but is
  BLIND to *closure* — whether the trajectory is already answer-ready and merely failing to materialize a final
  `\boxed{}` answer before the budget runs out (the DOMINANT documented failure mode).
- **RIGHT object O1** = a small trained **Closure-Utility Head** `gθ(Ht, xt, Mt) → (zt, ui, ri)`:
  - `zt` : "close now" scalar (is the trajectory verifier-closable NOW?).
  - `ui` : per-position verifier-utility / terminal-span priority.
  - `ri` : optional tiny role label `{none, box-open, answer-token, box-close/eos}`.
  - Token identities stay from O0 except a **narrow finite-state terminal bias** over canonical final-answer
    syntax (`\boxed{`, `}`, newline/eos, and candidate-answer tokens COPIED from the model's own committed
    scratchwork). **No pairwise scores, no joint inference, no remasking, no extra steps, no dynamic budget.**
  - Effective commit score `s_i^(1) = s_i^(0) + λ · zt · ui`, where `s_i^(0)` is the O0 confidence/entropy
    score. **Same number of positions committed per step as O0** — O1 only changes WHICH masks get committed
    when the model is solution-ready but not closing.
- **relation_to_O0**: O1 is a re-ranking of O0's own commit decision by a trained closure-utility signal; it
  does NOT change token marginals, step count, or commit quota. It is a *closure selector*, not a scheduler and
  not a dependency model.
- **Honest closest rival (do NOT claim as novelty)**: answer-suffix / answer-guided training exists (AG-GRPO,
  ACL 2026). The narrowed novelty = a FROZEN-backbone, verifier-utility **closure selector trained from logged
  truncation states**, not full policy post-training.

## Training target (generation/verifier labels ONLY)
For each O0 logged state `st = (xt, Ht, p0, Mt)`, construct a minimal terminalization candidate
`T(a) = "\nTherefore, \boxed{a}."` where `a` is extracted from the model's OWN committed reasoning / stable
high-confidence residual tokens. Label `st` **positive** iff inserting `T(a)` into currently-masked tail slots,
WITHOUT changing committed reasoning and WITHOUT extra steps, makes the verifier pass. Train:
- `zt = 1` for the earliest verifier-closable states.
- `ui = 1` for slots in the minimal terminal span.
- `ri` only for finite terminal roles.
**No diffusion loss. No reference-token agreement. No teacher forcing to gold solutions.**

## Pre-training DIFFERENTIAL-PREDICTION CONTRACT (run on existing O0 logs BEFORE training)
Strata `S = closure-strandedness`. High S ⇔ ALL true:
1. No valid final answer currently committed.
2. A candidate answer is extractable from committed scratchwork / stable residual tokens.
3. Remaining expected commit capacity is tight but sufficient for `T(a)`.
4. O0 assigns nontrivial local probability to terminal tokens, but EBS ranks those positions BELOW
   filler/reasoning positions.
Bins (3–4): `S0 none` · `S1 candidate-only` · `S2 candidate+tight-budget` ·
`S3 candidate+tight-budget+terminal-rank-discordance`.

**Prediction:** verifier rescue from an O0-matched closure oracle is MONOTONE in S, concentrated in `S3`.

**GO thresholds (all required):**
- `S3` contains ≥40% of truncation-labeled failures.
- O0-matched closure oracle rescues ≥20% of `S3` failures.
- Overall verified gain upper bound ≥ **+3 pp** on AIME-2024 / MATH-L5, OR ≥25% relative reduction in
  truncation failures.
- Median first-valid-final-answer step in rescued successful logs moves EARLIER by ≥25%, at identical step
  count and commit quota.
If these do not hold → **the object is dead before training.**

## Controls + rival (the honesty audit)
- **Shuffled-S negative control:** shuffle S within task × difficulty × step-decile × output-length bins.
  Expect the monotone `S0<S1<S2<S3` curve to disappear; shuffled-`S3` enrichment ≤25% of real; shuffled-S
  logistic coeff null. **KILL if shuffled S predicts rescue nearly as well as real S.**
- **Generic-difficulty control:** fit `Y=closure-oracle-rescued` on {mean entropy, max confidence, mask count,
  step fraction, prompt length, generated length, remaining slots, O0 item pass-rate, task fixed effects},
  THEN add S. GO only if adding S improves AUC ≥0.05 AND odds-ratio ≥2.0 for `S3`, without collapsing under
  item-level clustered SEs. **KILL if S is just "hard / long / late".**
- **Rival baseline — DeadlineBox** (the brutal surface-form baseline; == the frozen force-fill that the 5.9
  Pareto-null already tested): same answer extractor + same canonical terminal template, NO hidden-state head.
  Rule: if no valid final answer and remaining commit capacity ≤ `L(T(a)) + ε`, force-fill `\boxed{a}` into
  tail masks. O1 is worth training ONLY IF: DeadlineBox captures <70% of closure-oracle rescues AND high-S
  states carry extra hidden-state / rank-discordance signal DeadlineBox misses. **KILL if DeadlineBox gets most
  of the gain** (then it's deterministic terminalization, not a modeling object).

## FINAL kill condition — do NOT train O1 unless ALL pass
1. oracle upper bound ≥ +3 pp
2. real S ≫ shuffled S
3. S survives generic-difficulty controls
4. DeadlineBox does NOT capture the gain
5. O0 top-k/top-p contains the needed terminal tokens in most high-S states

## If any fail → SATURATED; named jump target
Declare the math-truncation substrate saturated; honest jump = **tool-call / JSON-schema / code-repair
generation**, where the closure object becomes parser-verifiable STRUCTURAL terminalization rather than
near-ceiling math reasoning. (CFG-constrained diffusion decoding already covers hard syntax — arXiv 2508.10111 —
but semantic field repair + tool-call editing still have headroom.)

## Opus packaging notes (for /object-shift-audit + occupancy)
- Occupancy: NOT the dependency-head family (DEMASK/CoDD/FeF-DLLM) — different object (closure, not coupling).
  Not a generic unmasking policy (same quota; closure selector). Rival AG-GRPO flagged + novelty narrowed.
- FORBIDDEN cleared: TRAINED (not frozen post-hoc joint-readout 5.5/5.9/5.10.3); not compute-allocator (same
  quota, no dynamic budget); not SFT-diffusion-loss; not SC-target; not remasking; not wall-clock evaluation.
- The 5.9.2 frozen anti-truncation kill is RESPECTED by construction: DeadlineBox (≈ the frozen force-fill) is
  the rival O1 must beat; the DPC oracle-upper-bound gate re-tests closure headroom cheaply on existing logs.
- author_engine: leap=Pro, packaging=Opus; self_certified=false.
