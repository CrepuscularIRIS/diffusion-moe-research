# GPT-5.5 Pro 扩展 — N2 codec-free disambiguation + framing (2026-06-28)

> Source: Playwright→GPT-5.5 **Pro 扩展**, chat "Frozen DiffusionGemma Experiment". Resolves the codec-confound
> in the G4/N1 result (N1a oracle WTR 0.92-0.96 ⇒ the tied-embedding nearest-neighbor snap codec is itself
> lossy, so N1b's structural-kill is codec-confounded). This doc = framing verdict + the FROZEN BUILD CONTRACT
> for the N2 continuous-handoff arm. Tree node 5.3.2.

## ★ FRAMING VERDICT (Pro)
- **Claim A (supported, NARROWED):** "Training-free embedding-space few-step decoding does NOT transfer to this
  frozen discrete masked dLLM by reusing the tied token embedding/lm-head as a continuous state + nearest-
  neighbor token codec. The tied-embedding NN codec is not lossless for the tested DDIM mask↔clean interpolant;
  repeated intermediate projection through it destroys even the ORACLE trajectory (WTR 0.92-0.96, 16-28% final
  answer loss)." Do NOT broaden to "no lossless multi-block codec exists" (a learned/model-head/simplex/no-snap
  decoder might work).
- **Claim B (NOT cleanly supported yet):** "the frozen dLLM cannot integrate a continuous embedding velocity
  field few-step" — N1a invalidated this interpretation. Internal line: **"N1b fires the preregistered
  structural-kill, but after N1a it must be reported as a CODEC-CONFOUNDED kill, not clean evidence the model
  can't consume continuous trajectories."**
- **Publishability:** A alone = workshop/Findings (with the sealed 134-run + a geometry appendix). TOP-VENUE
  needs the codec-free N2 arm (else "you diagnosed a bad projection, not the continuous-consumption question").
- **Top-venue wording:** "We identify an INTERFACE failure in plug-in continuous decoding for a frozen
  production-scale discrete diffusion LLM. The failure is not insufficient NFE nor a poor learned clean-token
  estimator alone: an ORACLE clean-estimate control fails because the tied embedding table does not define a
  stable intermediate token codec for the mask↔clean path. A cautionary counterexample to porting continuous
  embedding-flow methods to frozen discrete dLLMs by reusing input/output embeddings WITHOUT training the
  continuous state interface." (Compatible with ELF, which TRAINS the interface.)
- **Contribution one-liner:** "A falsified plug-in acceleration hypothesis, localized by oracle controls to the
  tied-embedding codec geometry of a frozen block-diffusion LLM."

## ★ N2 CONTINUOUS-HANDOFF ARM — BUILD CONTRACT (codec-free; frozen; ~few GPU-h)
**Core principle:** NEVER decode active-block intermediate states to token IDs. The active 256-canvas stays a
tensor in embedding space until block commit; previously-committed blocks remain normal discrete tokens
(block-AR). This removes the repeated NN-snap codec = the confound.

**Continuous DDIM update (per active block, no intermediate snap):** schedule Z_j = a_j·X0 + b_j·R (a_0=0,b_0=1,
a_K=1,b_K=0; R = e_mask broadcast for the mask→clean line). Step: feed Z_j via the embedding hook → logits
ℓ_j = f_θ(context, Z_j, j) → P_j = softmax(ℓ_j/τ) (same τ as G4-SOFT). Clean estimate: X0_model = P_j·E
(model) or X0_oracle = E[y*] (oracle). Update R_j=(Z_j − a_j·X0)/b_j ; Z_{j+1}=a_{j+1}·X0 + b_{j+1}·R_j
(rectified line: Z_{j+1}=(1−λ_{j+1})·e_mask + λ_{j+1}·X0). **Do NOT apply NN_E(Z_{j+1}) at any intermediate step.**

**Embedding hook** (no params): register_forward_hook on get_input_embeddings; override active-canvas rows of
the embedding output with Z_j (keep input_ids = prompt+committed+[MASK]×256 for scaffolding/masks/cache).
Match the model's embedding SCALE (√d) exactly.

**Self-conditioning = a LOGGED condition** (DiffusionGemma allocates SC buffers — don't change silently):
primary SC_{j+1}=P_j; controls SC=δ_{y*} (oracle steps), SC=0 (if path allows). Report if conclusions differ.

### Subarms
- **N2a — continuous oracle round-trip** (X0=E[y*] every step, no snap): SANITY GATE. Must reach exact-token
  round-trip ≥0.995 AND AnswerAcc ≥0.95·A_full (0.893). **If N2a fails → STOP, the codec-free path is not
  validated (don't interpret N2b).**
- **N2b — continuous oracle-to-basin** (X0=E[y*] for j<K−1; at j=K−1 use P_{K−1}=softmax(f_θ(Z_{K−1})), commit
  ŷ=argmax_v P_{K−1,v} — by the MODEL distribution, NOT NN-decode of the centroid): the CLEAN replacement for N1b.
- **G4-SOFT-CONT** (X0=P_j·E every step, no snap, final commit by model argmax): is the catastrophic G4-SOFT
  due to the snap codec or a bad continuous field?

### Metrics (preregister): verified MATH acc (top-line) + per-step consumability read curves —
GoldTop1(j)=mean 1[argmax P_{j,i}=y*_i], GoldNLL(j)=−mean log P_{j,i,y*_i}, GoldMargin(j). Decisive node = j=K−1.

### Pre-registered decision (A_full=0.94, target 0.95·A_full=0.893):
- **Sanity:** N2a ≥0.893 AND round-trip ≥0.995, else STOP.
- **Upgrade A→qualified-B** iff: N2a passes; N2b FAILS (<0.893 @K6&K12, CIs below) ; consumability fails near
  commit (GoldTop1(K−1)<0.90, or continuous read curve >5pp below a matched discrete/native read baseline); AND
  G4-SOFT-CONT does NOT recover native. Then: "even after removing repeated intermediate snapping, this frozen
  dLLM does not provide a usable continuous tied-embedding denoising interface for few-step decoding under the
  tested mask↔clean DDIM path" (scoped to this checkpoint/interface/no-training/path).
- **Codec is the culprit** iff N2a passes AND N2b recovers (≥0.893) → WITHDRAW N1b as evidence for B. Then:
  G4-SOFT-CONT recovers → snap codec was the main culprit for both; G4-SOFT-CONT still fails → model CAN read
  oracle continuous states but training-free soft estimates don't define a usable few-step field (still valuable).

### Failure modes to control: (1) scale mismatch (hook after embedding scaling; log norms); (2) hidden
re-discretization (assert no sampler converts active states→IDs; perturbation test: random nudge to one active
position must change next logits); (3) self-conditioning ambiguity (log/control); (4) final-decoder ambiguity
(commit by model argmax, NOT NN-decode of P·E); (5) teacher non-uniqueness (verified acc is the main metric;
token recovery is interpretive only); (6) OOD MoE routing (log router entropy / expert overlap soft-vs-token).

## Novelty positioning
Continuous language-flow methods TRAIN the continuous interface; this asks whether a FROZEN discrete dLLM
already contains one for free — it does not, through tied-embedding NN DDIM. Complementary to: Loopholing
("sampling wall" of categorical collapse → we find a Voronoi/codec wall); ELF / Flow-Map LMs (train the
interface; few-step discrete diffusion degrades without it); MeanFlow/pMF (few-step needs a trained
shortcut/average-velocity map, not a sampler swap); sampler-centric oracle papers (separate denoiser vs
sampler error — N1a is analogous but isolates the embedding-state→token CHANNEL). The codec-geometry finding
(tied-embedding Voronoi cells do not preserve the mask↔clean line, even under an oracle, strongly enough to
destroy multi-block verified reasoning) appears NOVEL as an inference-time diagnostic on a production-scale
frozen masked dLLM — citable WITH the WTR curve + answer loss + the codec-free N2 arm.
