# GPT-5.5 Pro 扩展 — N2 positive-pivot novelty + framing + design verdict (2026-06-28)

> Source: Playwright→GPT-5.5 **Pro 扩展**, chat "Novelty and Design Critique" (思考 10m34s). Routed after the N2
> dev-gate showed removing the per-step snap recovers near-native accuracy (g4_soft_cont 0.97≈native 0.94).
> This is the deep-design + novelty gate for the EMERGING POSITIVE. Tree node 5.3.1.1.

## ★ VERDICT: conditional top-venue YES — but REFRAME
A plausible NeurIPS/ICML paper, but NOT as "continuous language flows already exist in frozen dLLMs" (too
crowded). Write it as a **mechanistic inference-time discovery in frozen dLLMs**, not a new continuous-diffusion
modeling paradigm. Defensible one-sentence contribution:
> "A frozen production-scale discrete diffusion LLM can be decoded through a continuous expected-embedding
> carrier at INFERENCE time with ZERO training; the failure of plug-in embedding-DDIM is caused not by absence
> of a continuous denoising interface but by a lossy tied-embedding nearest-token SNAP codec."

3-claim structure (in order): (1) nearest-token snap is a destructive codec for tied-embedding diffusion
trajectories; (2) the failure is localizable with gold-oracle + Voronoi-geometry controls; (3) removing
intermediate snap exposes a usable frozen continuous carrier that recovers native-level few-step math accuracy.
Framing = **cautionary + constructive** (the cautionary "snap is the hidden bug" is harder to attack than the
positive "free continuous decoder" alone). Title style: "Don't Snap: Continuous Carriers for Frozen Discrete
Diffusion LMs" / "The Snap Codec Is the Bottleneck". AVOID "Discrete Diffusion LMs Already Contain Continuous
Flows" (invites every continuous-LM paper as a novelty objection).

## ★ CLOSEST PRIOR ART — must cite + differentiate (novelty threats, ranked)
- **LRD (Latent Refinement Decoding)** — BIGGEST threat. Two-stage inference keeping masked positions as
  distributional mixtures of predicted tokens + mask embeddings before finalizing confident tokens; reports
  LLaDA/Dream gains incl MATH500-style. ⇒ MANDATORY: implement a training-free LRD/top-k/soft-masked analogue
  baseline. If our method ≈ this, novelty = the Voronoi-snap FAILURE ANALYSIS, not the carrier.
- **DSL-LLaDA** — adapts a pretrained masked dLM into a continuous embedding-space denoiser, defers hard commit
  to final step. Diff: DSL TRAINS/adapts; ours is zero-training, inference-only.
- **CoDAR** — identifies token rounding / FINAL projection as a bottleneck, adds a LEARNED contextual decoder.
  Diff: ours is INTERMEDIATE nearest-neighbor snap in a tied table; remedy = NO learned decoder. Wording: "Prior
  work identifies final discretization as a bottleneck; we show a different operational failure — intermediate
  NN-snap alone destroys an otherwise-usable continuous trajectory, even under gold-clean oracle embeddings."
- **EvoToken-DLM**, **Soft-Masked Diffusion LMs** — continuous relaxation but TRAINED/adapted.
- **Loopholing DLMs** — "categorical sampling wall" + trained latent pathway. Ours = tied-embedding NN-CODEC
  wall in a FROZEN model. Don't claim "wholly new distribution preservation."
- **ELF / LangFlow / Flow-Map LMs** — train the continuous interface; not frozen-discrete inference.
- **SDTT / DiDi-Instruct / ReMDM** — distillation/remasking; threaten only an ACCELERATION claim, not zero-training.
- **Sampler-vs-denoiser error decomposition** — SUPPORTS our oracle-control logic (separate model capacity from
  sampler/codec error).
Reviewer-safe novelty line: "first / among-first TRAINING-FREE continuous carrier exposed in a FROZEN production
discrete dLLM, with a tied-embedding Voronoi codec-geometry diagnosis." NOT "first continuous flow decoder for
language"; NOT "nobody noticed rounding is bad."

## ★ MANDATORY additions before the top-venue claim (beyond the sealed run + step-ablation already underway)
1. **LRD / top-k expected-embedding carrier baseline** (training-free): each step take top-k probs, form expected
   tied embedding, optionally mix with mask per schedule, commit at block end. Report k∈{1,4,16,full}. k=1≈argmax/
   self-conditioning; full=our expectation carrier; intermediate k shows whether gain is distributional-softness
   or the DDIM update. + an LRD-style mixture (mask⊕predicted) baseline.
2. **Multi-snap-metric Voronoi diagnostics** (KILL-SHOT control): compare Euclidean-NN, cosine-NN, mean-centered,
   norm-normalized, and logit-argmax-via-tied-head SNAP. If EVERY snap variant fails → codec result robust. If one
   variant fixes it → the claim narrows to "wrong snap metric," not "snap per se." + Voronoi RETENTION curve
   (does min‖z−e_v‖ stay at v=gold along z=α·e_gold+(1−α)·ē?) + nearest-neighbor MARGIN curve (tiny/negative ⇒
   snap instability). + token-class breakdown (numerals/operators/newline/boxed-answer/rare) + block-position +
   timestep-where-snap-first-destructive. These are mostly OFFLINE (embedding-table geometry) — cheap.
3. **Structured final-call / trajectory controls** (kill "final argmax does everything"): run the SAME final
   commit from several states — true continuous trajectory, K=1 direct, SHUFFLED-step trajectory, random convex
   combos of prior states, native-discrete snapped — same final timestep/prompt/block/budget. True trajectory must win.
4. **Wall-clock + throughput curves** (honest): NFE-matched AND wall-clock-matched. DO NOT sell acceleration —
   DiffusionGemma already adaptive-stops ~12–16 steps; K=12 continuous at comparable NFE is NOT a speed claim.
   Frame: "continuous carry restores quality lost by naive snap at few-step budgets; acceleration is conditional."
5. **Generality check** (≥1): another discrete dLM with embedding injection, OR another task family (code/instruction/
   synthetic token-recovery), OR synthetic controlled prompts with known target path. Reduces "one-model hack."
6. **Subset provenance**: pre-define the n=134 hard-headroom subset WITHOUT using our method's outcomes; report
   full MATH-500 or the exact selection rule. Verifier: report format-failure separately from math-failure.
The killer plot: **accuracy vs K overlaid with snap wrong-token-rate / Voronoi retention by timestep** — if snap
failure rises exactly where accuracy collapses, the paper is hard to dismiss.

## ★ KILL CRITERIA (any ⇒ top-venue positive dies)
- Sealed n=134 doesn't reproduce / g4_soft_cont CI overlaps no-gain vs native few-step.
- AIME directionally contradicts MATH.
- K=1/commit-only ≈ K=12 (trajectory claim collapses → "final embedding input helps," much weaker).
- Step-ablation non-monotone/unstable without explanation.
- A simple LRD/top-k baseline matches/beats us (kills "novel decoder"; mechanism paper survives).
- A corrected snap metric (cosine/logit-argmax) fixes the failure (claim narrows to "wrong NN metric").
- Wall-clock much worse AND mechanism not valued.
- Oracle contamination leaks gold into real decoder (FATAL — keep oracle arms fully separated).
- Result depends on the hard-headroom subset definition.
- Verifier artifacts (format/length/parsability) dominate the gain.

## ★ Minimum results
- TOP-VENUE: sealed n=134 no-snap K12 statistically ties native high-quality OR ≫ native few-step at matched NFE;
  AIME directionally consistent; K1≪K12; snap catastrophic across budgets; gold+snap oracle shows codec loss;
  Voronoi diagnostics quantitatively explain snap failure; LRD/top-k baseline included (underperforms or folded
  into our family); wall-clock honest; claims scoped to DiffusionGemma (unless +1 model).
- FINDINGS/workshop (if positive weakens): per-step snap ≪ no-snap consistently; gold+snap oracle codec loss;
  Voronoi diagnostics predict failures; no-snap recovers ≥half the snap-induced gap AND beats native few-step at
  some matched NFE (stat-sig); clean K-ablation; NO acceleration claims. "Nearest-token snap is a hidden failure
  mode in frozen discrete-diffusion LLM decoding."
