# H4 architecture verdict → pivot to a CONSTRUCTIVE router experiment (2026-06-25)

**Source:** Opus feasibility agent (read-only audit of transformers 5.12.1
`models/diffusion_gemma/`), smoke-confirmed. Decisive.

## Verdict: DiffusionGemma's MoE router has NO timestep input — anywhere
- Router `forward(self, hidden_states)` — single input = the residual hidden state.
  `proj: Linear(hidden→128 experts, bias=False)`, scale-free RMSNorm, per-dim/per-expert scales.
  None is a function of t. (`modeling_diffusion_gemma.py:493-527`, `modular:417-439`.)
- **No timestep/noise embedding exists in the whole package** — sweep for
  `timestep|temb|sigma|noise_level|adaln|modulation|scale_shift|FiLM` = ZERO hits. No AdaLN/FiLM.
- The denoiser forward never receives a timestep; generation passes only `decoder_input_ids`
  (current canvas) + `self_conditioning_logits`. Noise level enters ONLY implicitly via the noised
  canvas (uniform/random-token discrete diffusion: random vocab → entropy-commit → renoise). The
  48-step schedule only sets an OUTPUT-logit temperature, not the forward.

## Consequence: the t-swap factorial collapses
| cell | realizable on frozen model? |
|---|---|
| Y00 = R(M(h,t_c), t_c) | YES (standard forward) |
| Y10 = R(M(h,t'), t_c)  | YES — but this IS D_M (build canvas at t', re-run) |
| Y01 = R(M(h,t_c), t')  | **NO — router has no t input → ≡ Y00** |
| Y11 = R(M(h,t'), t')   | collapses → ≡ Y10 |

- **Strong-H4 ("router reads t directly") is architecturally VACUOUS**, not merely hard.
- Even D_M has no separable `M(h,t)`: `h` is fully downstream of `t` (canvas pattern + self-cond);
  you cannot hold `h` fixed while varying `t`. The only well-posed passive question is "does realized
  routing depend on denoising step" — which is EXACTLY the confounded passive H4 we already killed.

## The redirect (this is the convergence)
Both routes to "do experts specialize by t" are dead: passive = denoising-trend confounded
(identifiability wall); frozen-interventional = impossible (no t input). The remaining, well-posed,
NOVEL, and CONSTRUCTIVE question is the original **H5**:

> **Does ADDING explicit timestep/progress conditioning to the router improve a diffusion-LM MoE?**

The model currently routes purely on (noised) content — it never sees t explicitly. So "does giving the
router t/progress help?" is genuinely open and a clean paper question, with a built-in null: the canvas
content may already encode everything the router needs (t redundant).

### Proposed experiment (constructive; replaces the dead t-swap probe)
- **Adapter:** `R'(z, t_r) = proj(z) + g(emb(t_r))` — a small MLP `g` on a sinusoidal timestep/progress
  embedding, ADDED to router logits. Variants: content-only `R(h)` (frozen baseline), `R(h,t)`,
  `R(h, P̂)` (P̂ = non-tautological progress: canvas entropy / change-rate / residual norm),
  hybrid `R(h,t,P̂)`. Train ONLY the router/adapter; freeze the rest.
- **Metric (KEY UNBLOCK):** held-out DIFFUSION LOSS (forward pass) — sidesteps the broken
  block-diffusion generation eval entirely. Secondary: routing load balance, compute-quality.
- **Falsifier:** no variant beats the frozen content-only router on held-out diffusion loss (≥3 seeds)
  → explicit t/progress conditioning is redundant → do NOT build around it (clean negative, publishable).
- **Schedule-robustness (the discriminator):** also eval under warped schedules (24/48/96 steps) — a
  t-conditioned router that helps on 48 but breaks on warped → t is a brittle proxy → prefer progress/hybrid.
- **Controls:** content-only frozen router = negative control; same-architecture random-init adapter
  (untrained) = sanity; locality = only the router/adapter changes, experts + backbone frozen.

## Hook points (no weight change, for any measurement-only pass)
`model.decoder.layers[L].router` (L=0..29; decoder = denoiser, carries the noise; encoder sees clean
prompt). Capture z via `register_forward_pre_hook` (`args[0]` = `[B*S, 2816]`); capture decision via
`register_forward_hook` (`top_k_index`, pre-capacity — the dense expert loop drops nothing). Dropout-free
already; deterministic given z. Smoke: `scratchpad/router_tswap_smoke.py`.

## Status
- **H4 (passive/probing) — RETIRED** as posed (vacuous on this arch + confounded in passive logs).
  Its value: a methodological negative result (identifiability wall + no-t-input) worth a paper section.
- **H5 (constructive t/progress-conditioned router utility) — now the PRIMARY Direction-C experiment**,
  unblocked by using held-out diffusion loss. Pending: novelty scan (DeepResearch) + Codex SELECT.
