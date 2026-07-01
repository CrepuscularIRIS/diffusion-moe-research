# Related work + contribution framing (deep prior-art read, 2026-06-26)

> Source: Opus subagent deep-read of TEAM/MoDE/LLaDA-MoE + EC-DLM (my read) + DeepResearch #1.
> This RE-ANCHORS the contribution honestly. Read before writing the intro/related-work or claiming novelty.

## ⚠️ CORRECTION (2026-06-26, post-H5 3-seed + confound ablation + Codex adjudication) — supersedes §2/§3 below
Two errors in the original "implicit-channel" framing, caught by the H5 result + Codex independent review:
1. **The corruption is D3PM-UNIFORM (random-token replacement), NOT `[MASK]`** (`diffusiongemma_sft/data/corruption.py`,
   `corrupt_uniform_random`). So a content-only router does NOT get the noise level "for free as the fraction of
   [MASK] tokens in h" — corrupted positions are valid random tokens, not a flag, so the corrupted-fraction is
   **not cheaply derivable from h**. The original §2 "implicit channel = [MASK]-fraction" claim is WRONG; arm D's
   mask-ratio (from the oracle `noise_mask`) is an **ORACLE** signal h lacks easy access to. This makes a POSITIVE
   (conditioning helps) the *expected*, less-surprising outcome — and it did: **B,D < A by ~0.41 nats, 3/3 seeds.**
2. **Frame the claim around REAL-vs-SHUFFLE (within-adapter), NOT B−A.** Arm A is a weak constant baseline
   (zero-input MLP → degenerate optimization; B-const@0.5=4.43 even beats A=4.71), so B−A overstates level-signal
   attribution. The airtight evidence: **shuffling the per-row level on a trained adapter HURTS by 0.27–0.42 nats
   (3/3 seeds)** → the adapter genuinely reads the per-sequence level (input-scale/gradient artifact RULED OUT).
   const@0.5 recovers the *average* correction; per-row variation adds the rest (strongest at high corruption).
- **Conservative claim wording (Codex-approved):** "A router-only adapter trained on per-sequence corruption-level
  signal learns to use it: replacing correct per-sequence levels with shuffled values consistently degrades held-out
  diffusion CE by 0.27–0.42 nats across three seeds, while a fixed mid-level constant recovers only part of the gain
  — confirming the adapter extracts row-specific information beyond a fixed average correction."
- **NOT supported (do not write):** the full 0.41 nat B−A is all level-signal (A is weak); ANY generation-quality
  gain (gen eval broken); schedule/distribution generalization (single 64-row GSM8K-dev bank); "explicit t is
  necessary" (mask-ratio ties raw t — equivalent scalar proxies). The §4 below ("Arm E degenerate") still holds.

## The honest novelty position (do NOT overclaim)
- **The MECHANISM is NOT novel.** Additive timestep-on-gate `G(z,t)=F(z)+E(t)` is established in VISION diffusion
  MoE: **TimeStep Master (2503.07416)** is functionally identical to our `R'(z,t)=proj(z)+g(emb(t))`; also
  Expert Race (2503.16057), ALTER (2505.21817), CARE-Edit (2603.08589), DiT-MoE. → **Never claim the adapter
  mechanism as a contribution.**
- **The QUESTION was answered in robotics (near-null).** **MoDE (2412.12953, ICLR'25)** routes diffusion-policy
  experts purely on noise level and ablates token-only (0.845) vs noise-only (0.851) routing → essentially TIED.
  So "should the routing decision depend on the diffusion variable?" already has a near-null answer in control.
  → **A null result for us is the EXPECTED, publishable outcome**, not a failure (pre-register it as such).
- **The defensible SLICE = regime + controlled question + structural finding:** the first *controlled* test of
  **decision-level** timestep conditioning in a **diffusion-LANGUAGE** MoE, as a **deployed-model adapter**
  (router-only), measured by **capacity-matched held-out diffusion loss**, **separated from capacity-conditioning
  (EC-DLM 2604.01622)**. Plus the empirical/structural finding that diffusion-LM routers are content-only.

## Closest prior art (cite + differentiate)
| Paper | id / venue | What | How we differ |
|---|---|---|---|
| **MoDE** | 2412.12953 / ICLR'25 | diffusion-POLICY (robotics) MoE; gate routes on NOISE-ONLY; ablates token-only vs noise-only (0.845 vs 0.851, ~tied) | language not control; ADD t to a CONTENT router (not replace); deployed-model adapter (router-only) not from-scratch; metric = held-out diffusion loss not task success |
| **TimeStep Master** | 2503.07416 / vision | gate `G(z,t)=F(z)+E(t)` — SAME additive form | vision image gen; we don't claim the mechanism; we ask the controlled language question + decision-vs-capacity |
| **EC-DLM** | 2604.01622 / 2026 | EC routing; conditions expert CAPACITY on mask-ratio | we condition the routing DECISION (scores), orthogonal to capacity; TC not EC |
| **TEAM** | 2602.08404 / preprint | caches/prunes the EXISTING content router across steps for 2.2× speedup (SDAR) | acceleration, router untouched; independent evidence dLLM routers are content-only + step-stable |
| **LLaDA-MoE** | 2509.24389 / 2025 | from-scratch masked-diffusion LM MoE; gate = Router(h_t), hidden-state ONLY | generality check: confirms diffusion-LM routers route on content, not t (not a DiffusionGemma quirk) |
| **RADD** | (Ou et al.) | masked diffusion needs NO explicit time t as a Transformer input | theory: explains WHY dLLM routers are time-agnostic; our compute-allocation question is ORTHOGONAL to RADD's distributional-sufficiency |

## Design implications (acted on / noted)
1. **Re-anchor the contribution sentence** away from "we propose timestep-conditioned routing" → "first controlled
   study of whether the routing DECISION in a diffusion-LANGUAGE MoE should depend on the denoising step, as a
   deployed adapter, distinct from capacity (EC-DLM); a null is a structural finding."
2. **Implicit-channel honesty (key for the falsifier):** a content-only router has IMPLICIT access to the noise
   level via the fraction of [MASK] tokens encoded in h. So "no explicit t" ≠ "no t information." Our A-vs-B tests
   whether making t EXPLICIT at the decision adds anything BEYOND the implicit channel. This is why a null is
   expected AND interesting.
3. **Theory hook:** RADD = the optimal denoiser *distribution* is time-independent (a marginal-prediction claim).
   Our question = does the *router* benefit from explicit t for *sparse expert allocation* (a compute-allocation
   claim)? Orthogonal — state this to avoid "experts specialize by t" naivety.
4. **Arm E (content-blind t-only) — NOTED but likely DEGENERATE for token-choice:** MoDE's noise-only gate is
   per-step-GLOBAL (whole policy); a content-blind gate in a token-choice dLLM sends ALL tokens to the same
   experts (no token differentiation) → trivially bad, not the MoDE finding. So keep A/B/D; do NOT add a naive
   content-blind arm. If we want the MoDE contrast, do it as ANALYSIS (variance of routing explained by t vs
   content), not a degenerate arm.
5. **Keep A/B/D**, primary result = **B vs A** (does explicit t help beyond the implicit channel?). D (mask-ratio)
   ≈ B in single-corruption (see EC-DLM note). Pre-register the null as the clean, publishable outcome.

## Related-work paragraph draft (subagent; refine for the paper)
> Conditioning sparse routing on the diffusion step has been explored almost entirely in vision and control. In
> image/video diffusion transformers, timestep-conditioned gates are common — TimeStep Master (2503.07416) uses an
> additive gate G(z,t)=F(z)+E(t), and Expert Race (2503.16057), ALTER (2505.21817), CARE-Edit (2603.08589) allocate
> or specialize experts by timestep — while in robotics, MoDE (2412.12953, ICLR'25) routes diffusion-policy experts
> purely on the noise level and finds noise-only routing essentially tied with content-only (0.851 vs 0.845).
> Diffusion *language* MoEs, by contrast, route on content alone: LLaDA-MoE (2509.24389) uses a hidden-state-only
> linear gate, SDAR's router is content-based and step-stable (exploited by TEAM, 2602.08404, for acceleration),
> and masked diffusion LMs are conventionally time-agnostic (RADD shows time t need not be a Transformer input).
> dLLM-MoE work that touches the denoising step changes the router's *capacity* (EC-DLM, 2604.01622) or caches its
> decision for speed (TEAM), not its *decision*. We ask whether the routing *decision* in a deployed, content-only
> diffusion-language MoE (DiffusionGemma 26B-A4B) should depend on the denoising step, via a lightweight adapter
> R'(z,t)=proj(z)+g(emb(t)) trained router-only and evaluated by capacity-matched held-out diffusion loss; to our
> knowledge this is the first controlled test of decision-level timestep conditioning in a diffusion-language MoE,
> and we treat a null as a publishable structural finding about diffusion-LM routers.

## Uncertainty flags (verify before camera-ready)
- MoDE venue (ICLR'25) author-stated — confirm. Expert Race/ALTER venues unverified (treat as arXiv).
- TEAM = unrefereed preprint. Content-only-router claim verified for LLaDA-MoE + SDAR(via TEAM) + DiffusionGemma;
  scope universal-sounding claims to "all public diffusion-LM MoE routers we examined".
- Mechanism-novelty conclusion is FIRM (TimeStep Master identical) — claim only the language+adapter+controlled slice.

## DeepResearch #2 confirmation (2026-06-26; LAST DeepResearch — future novelty uses 超高)
- **No DLM-MoE conditions the router on t** — LLaDA-MoE (content hidden-state linear router), DiffusionGemma,
  Dream, MMaDA, SDAR all content-only (no public evidence of timestep-conditioned router logits). Our
  structural finding holds beyond DiffusionGemma.
- **Mechanism precedent (add to citations): M3ViT (NeurIPS'22)** — concatenates a task embedding to feed the
  shared router = same family as "condition the gate by an external signal". Plus TimeStep Master/MoDE. → the
  adapter mechanism is NOT novel; the slice is.
- **Causal precedent:** arXiv:2603.11114 (MoE routing patterns cluster by task, permutation baselines) — related
  but not the interventional freeze-h/swap-t test.
- **DEFENSIBLE CLAIM (DR#2 wording):** "To our knowledge, first retrofit and controlled evaluation of
  timestep/noise-conditioned router-logit adaptation in a DEPLOYED discrete diffusion-language MoE, separated
  from capacity scheduling and compared to a capacity-matched content-only router by held-out diffusion loss."
- **NOTE:** H5 1-seed result is POSITIVE (B<A by 0.41), so the contribution is now a positive (not null) finding
  IF the 3-seed + the content-conditioned capacity-fairness control (A') hold.
