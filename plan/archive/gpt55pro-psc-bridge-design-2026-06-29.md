# GPT-5.5 Pro 扩展 — PSC-Bridge deep design (2026-06-29, chat "Frozen Diffusion LLM Design")

> Routed after V1+② clean negatives exhausted the post-hoc axes (Codex: pivot upstream). Pro's pick for the one
> live UPSTREAM lever + a GENUINELY cheap training-free oracle (the future-SC-injection bound — NOT the
> uninformative gold-rescue). Primarily a few-step SPEEDUP bet (48-step quality at ~24 NFEs); Pro shares the
> accuracy skepticism. Tree node 5.9 (campaign), candidate for 5.9.3.

## The lever — PSC-Bridge (Predictive Self-Conditioning Bridge)
Transport the model's BELIEF STATE forward in denoising time, not its tokens. At step k, position i, native:
`p_{k,i}=softmax(ℓ/T)`, SC fed next step `m=scale·p·W`. PSC-Bridge replaces ONLY the stored SC belief for the
NEXT forward with an e-geodesic (simplex secant/momentum) extrapolation:
`log p̃_{k,i} = log p_{k,i} + α_{k,i}·(log p_{k,i} − log p_{k-1,i}) − logZ`, then feed `m̃=scale·p̃·W` into the
EXISTING trained SC gated-MLP. **Do NOT** change accept_canvas / current-token decision; **do NOT** move canvas
embeddings continuously; **do NOT** Euclidean-snap; **do NOT** touch backbone/router/experts/embedding/LM-head.
Only learned object = a scalar `α_{k,i}=α_max·σ(g_φ(f))` from a tiny <20k-param MLP on BORING features
[H(p_k),H(p_{k-1}),ΔH,KL(p_k‖p_{k-1}),max_v p_k,1{x_k=x_{k-1}},i/255,k/48]. Trust region KL(p̃‖p_k)≤ρ∈{.25,.5,1}
nats; α=0 for low-entropy positions. α_max=2 → 2× step compression. (Train target AFTER oracle passes: regress
p̃·W → teacher future SC `sg(p^teacher_{k+Δ}·W)` from native 48-step traces; correct-only weighting optional.)

## ★ MEASURE-FIRST cheap oracle (the decisive gate — training-free)
Question: can the native SC channel carry SKIPPED denoising info if given oracle FUTURE self-conditioning? If no → do not train.
- Probe set: 80–150 fixed-seed AIME-24 + MATH-L5 pairs biased HARD (native uses ≥32 NFEs; mix of full-correct/wrong). Score final answer with math_verify only.
- Log a full native 48-step trajectory; store m_k=p_k·W per step (48×256×2816 bf16 — large but OK for a probe).
- Compressed schedule S=24, τ_j=⌊j·48/24⌋. **DIRECT oracle:** at compressed step j, run frozen model on replay canvas + current SC, native EB updates the canvas, then inject the STORED future teacher SC `m̃_j=m^teacher_{τ_{j+1}}` (NOT teacher tokens/canvas — only the future SC embedding). Upper bound on channel capacity. **SCALAR oracle:** per-position α-grid {0,.25,.5,1,1.5,2,3,4} minimizing ‖softmax(logp'_j+α·(logp'_j−logp'_{j-1}))·W − m^teacher_{τ_{j+1}}‖² → upper bound for the EXACT adapter family.
- Metrics: VerifiedAcc@24 vs native-24 (hard cap) and native-48; rescue@24=Pr[PSC-24 correct | native-24 wrong & native-48 correct]; mean NFEs.
- **PRE-DECLARED PASS/KILL** (direct oracle, all three): Acc(directPSC-24) ≥ Acc(native-48) − 2pp; ≥ Acc(native-24) + 5pp; ≥ max(neg controls) + 4pp; AND rescue ≥15%. Scalar oracle: ≥ half the direct lift AND +3pp over native-24. KILL the whole lever if the DIRECT oracle fails (the trained SC gate cannot exploit skipped future belief). Direct passes / scalar fails → kill the scalar-secant adapter (consider a more expressive tiny adapter only if direct lift is large). Scalar passes → run the small training job.
- **NEGATIVE CONTROLS (≥4):** entropy-matched sharpening (kills "you just sharpened"); wrong-prompt future SC (kills non-semantic scale/manifold); position-shuffled future SC (kills if confidence-only); time-reversed/stale SC (kills "any SC disturbance helps"). If any control matches the oracle → not semantic transport → kill.

## Novelty slice (vs the overlap list)
Defensible = "frozen-backbone self-conditioning TIME-transport: a tiny probability-simplex bridge that ADVANCES
the model's native SC belief while leaving the token sampler + denoiser unchanged." Differentiation: pMF/partial-
masking (changes state space/objective — PSC doesn't); MeanFlow/reflow (learns continuous data-space velocity /
new generator — PSC predicts a future SC posterior-mean inside an existing discrete dLLM); JiT/ELF/DSL-LLaDA
(continuous embedding-flow canvas — PSC keeps canvas discrete, touches only native p·W SC); SDTT/DiDi
(distillation few-step student — PSC is not a student, doesn't distill the denoiser); LRD (mixture canvas tokens
+ finalization change — PSC acts one layer earlier at the SC injection point, no finalization change);
Loopholing (ADDS a latent bypass — PSC TIME-ADVANCES the EXISTING trained bypass). Biggest overclaim risk: the
direct oracle leaks trajectory-specific info → a positive proves CONTROLLABILITY not LEARNABILITY (why the
scalar-grid oracle matters).

## Honest stance (Pro, aligned with our negative synthesis)
Pro would NOT bet first on a frozen-adapter ACCURACY gain (AIME/MATH-L5 errors are likely wrong latent
trajectories already representationally committed — consistent with our V1+② negatives = post-hoc on the native
Pareto). PSC-Bridge is a SPEED bet (48-step quality at ~24 NFEs). The accuracy variant's separate gate = a
verified-positive DONOR-SC oracle (replay a wrong trajectory injecting a verified-CORRECT donor's future SC
embeddings only; require wrong→correct rescue ≥15% while wrong/other-prompt/shuffled donors stay <3%). If both
fail → state plainly: only denoiser retraining / finetuning / architecture-level transport moves the frontier
(the STRONG form of `plan/frozen-pareto-negative-synthesis.md`).
