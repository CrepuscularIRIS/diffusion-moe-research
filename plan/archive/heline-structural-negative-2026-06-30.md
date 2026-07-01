# Structural negative — the He-line / loss-function-revolution thesis is untestable on headroom-capable language diffusion (2026-06-30)

> Banked outcome of the Track-3 `/goal` ("TEST the He-line thesis on a small TRAINABLE diffusion-LM").
> Grade: **scoped→structural-PENDING** (independently assessed by the taste/object-shift gate + Pro 扩展;
> a full structural-negative *contribution* write-up would still go through the promotion gate). Not
> self-certified.

## The thesis (now closed on this substrate class)
"Diffusion = loss-function revolution": move a diffusion-LM's training target from cross-entropy on
discrete tokens to a continuous gradient/velocity-field / clean-x0 / embedding-flow target (the He / JiT /
MeanFlow / pMF / ELF line), and gain verified math-reasoning accuracy.

## The structural kill (why it's untestable here, not just "S-MEx0 was flawed")
**The experimental object does not exist on headroom-capable language diffusion.**
- Every public language-diffusion LM with real math headroom is **discrete masked (absorbing-state)
  diffusion**: LLaDA-8B, Dream-7B, DiffusionGemma-26B. Their training objective is *already*
  `−log p_θ(x0 | xt)` — a **categorical clean-x0 predictor** (CE only on masked tokens). There is **no
  noise/ε → clean-x0 target migration** to perform; the baseline IS clean-x0 prediction.
- Swapping CE for an embedding-space regression (clean-x0 codeword / L2) only changes the **scoring rule**
  over the identical modeling object and identical decode path. CE elicits the categorical posterior;
  embedding-L2 elicits the conditional **mean** `E[e(x0)|xt]`, which for a (frequently multimodal) masked
  posterior corresponds to **no real token mode**, then gets re-discretized at decode. So:
  - if the pure (β=0, no-margin) regression **loses** to CE → it only shows "a proper categorical scoring
    rule fits a categorical posterior better" (≈ tautology for the thesis);
  - if a hard-negative **margin** wins → it's multiclass separation / regularization (a CE-surrogate), not
    the embedding-flow object.
  Either outcome is **uninterpretable for the He-line thesis**.
- Substrates where the x0/velocity shift is *real* — continuous-embedding diffusion (ELF, Plaid/RePlaid:
  flow-matching / Gaussian diffusion in embedding space, discretize last) — exist only at **OWT/LM1B/PPL
  scale with ~20× compute gap vs AR**. **No math headroom.** Training olympiad/MATH-level headroom from
  these on 2×48GB is new-model-family-building, not a minimal experiment.

## Three convergent independent kills
1. **Frozen-26B (prior, tree 5.9.5):** SC-target on the frozen near-ceiling DiffusionGemma died —
   no headroom · early-commit · frozen. Same substrate-mismatch class.
2. **Independent taste + object-shift gate (this run):** KILLed S-MEx0 — COSMETIC-RESHIFT; masked-CE
   already predicts clean-x0; the margin is a CE-surrogate; frozen-codebook CE isn't the strongest baseline.
3. **Pro 扩展 structural verdict (this run, chat "模型设计决策分析"):** "B. 结构性不通" — the object doesn't
   exist on discrete; continuous has no headroom; do not spend MATH/olympiad budget; bank + switch topics.

## What this rules OUT vs what survives
- **Ruled out:** testing the *target-migration* (x0/velocity vs noise) form of the He-line thesis on any
  available headroom-capable language diffusion LM. The contrast has **no identifiable variable** there.
- **Survives (but requires a NEW thesis):** Pro's two adjacent directions —
  - (a) **discrete-dLLM-native training/sampling consistency** (posterior-bridge consistency, few-step
    denoising, remasking, confidence calibration, token-level noise scheduling; cf. CDLM/MPDC path
    consistency on discrete diffusion). KEEPS LLaDA/Dream headroom + the built `heline/` infra, but the
    thesis becomes "discrete-diffusion consistency/sampling-alignment → reasoning gains," NOT a loss
    revolution.
  - (b) **continuous-DLM latent geometry** (ELF/RePlaid line: learnable embeddings, likelihood-bound
    geometry, noise schedule, final discretization). He-bar clean, but short-term benchmark is
    OWT/LM1B/PPL, not MATH/olympiad.

## Transferable lesson (forbidden-assumption for future cycles)
The He-line "predict-x0/velocity vs predict-noise" object-shift is a **continuous-diffusion** concept. On
language it is **definitionally absent** wherever there is math headroom (all headroom dLLMs are discrete and
already predict clean-x0), and **present only where there is no headroom** (continuous-embedding dLLMs). Do
not propose a "change the diffusion-LM target/loss" experiment on a discrete masked-diffusion base and call
it a He-line object-shift — it is a cosmetic re-scoring of the same categorical posterior.

## Optional record-keeping (NOT pursued by default)
Pro: at most a tiny β=0 pure-regression vs native-trainable-lm-head CE sanity run, pre-registered ONLY as a
"discrete masked posterior is unsuited to Euclidean clean-codeword regression" negative control — never
dressed as a He-line test. Low value (near-tautological); skipped unless explicitly wanted.
