# Direction C — Timestep-Aware MoE Routing Analysis (Hypothesis H4)

Model-independent instrumentation + metrics to test **H4: DiffusionGemma's MoE
experts specialize by denoising timestep `t`.** Built and unit-tested **without
loading the 26B model** — the code is wired against the *real* `diffusion_gemma`
internals (transformers 5.12.1) discovered by reading source, not by running it.

## Layout

| File | Role | Lines |
|------|------|------:|
| `config.py` | `ProbeConfig` (frozen run config + `bucket_of`) and `RouterRecord` (+ trajectory/canvas/call/log-SNR/pre-capacity fields) | 116 |
| `probe.py` | Forward-hook instrumentation: hooks every MoE router, tags each capture by denoising timestep + trajectory/canvas/call; per-canvas/prompt reset (direct callers MUST call `start_prompt()` per prompt); full-coverage assertion | 392 |
| `probe_utils.py` | Pure helpers (`parse_router_location`, lazy-torch `to_numpy`) | 53 |
| `persistence.py` | Columnar `.npz` save/load keyed collision-free by `(record_id, layer, token, expert)`; `load_h4_dataset` builds the track-structured `H4Dataset`; torch-free on read | 321 |
| `runner.py` | `run_probe()` orchestration around `model.generate` (used ONLY with the real model) | 120 |
| `metrics.py` | Descriptive functions: usage dist, entropy, load balance, specialization, pairwise JS, bootstrap noise floor (auxiliary; not the H4 primary) | 391 |
| `h4_data.py` | Track-structured `H4Dataset` + per-visit expert-mass construction | 174 |
| `h4_test.py` | The H4 protocol test: stratified-G statistic, trajectory-synchronous permutation, shared-draw maxT FWER, effect sizes, cluster bootstrap | 391 |
| `h4_validation.py` | Null generators (synthetic-orbit / B / C / **X-corr cross-layer**) + planted-effect power + Clopper-Pearson + `null_a_real_orbit` (real-data gate) | 400 |
| `h4_broken.py` | **TEST-ONLY** broken per-layer-independent permutation + discrimination harness (proves the shared draw is load-bearing); NOT in the production path | 136 |
| `tests/test_metrics.py` | Synthetic-distribution unit tests (no model) | — |
| `tests/test_probe_hooks.py` | Hook-mechanism + persistence round-trip tests with a tiny FAKE MoE module (no model) | — |
| `tests/test_h4_decision.py` | H4 validation: type-I (synthetic orbit / B / C) + cross-layer-correlated discrimination (correct vs broken) + full-pipeline 2× detection + real-orbit gate smoke + power | — |

Run tests: `conda run -n dllm python -m pytest direction_c/tests/ -q`. The
analysis layer (`metrics`, `persistence`, `h4_*`, `config`) imports **torch-free**;
`RoutingProbe`/`run_probe` are lazy-loaded (`direction_c.__getattr__`) so the test
and analysis code runs without torch.

## Real module names (verified, NOT guessed)

Source: `transformers/models/diffusion_gemma/modeling_diffusion_gemma.py` and
`.../generation_diffusion_gemma.py` (transformers 5.12.1).

| Concept | Class / attribute | Source ref |
|---------|-------------------|-----------|
| Router (gate) | `DiffusionGemmaTextRouter` | modeling L493 |
| Gate Linear | `router.proj` = `nn.Linear(hidden_size, num_experts, bias=False)` | modeling L502 |
| Router forward return | `(router_probabilities[B*S,E], top_k_weights[B*S,K], top_k_index[B*S,K])` | modeling L506–527 |
| top-k select | `torch.topk(router_probabilities, k=config.top_k_experts)` | modeling L515 |
| Experts container | `DiffusionGemmaTextExperts` | modeling L531 |
| Expert weights | `experts.gate_up_proj` `[E, 2*moe_int, hidden]`, `experts.down_proj` `[E, hidden, moe_int]` | modeling L539–540 |
| MoE block (no separate class) | held inside `DiffusionGemmaEncoderTextLayer` (L570) / `DiffusionGemmaDecoderTextLayer` (L644); `self.router` (L591/L666), `self.experts` (L592/L667); called at L629–630 / L704–705 | — |
| Decoder model | `DiffusionGemmaDecoderModel` | modeling L1168 |
| Decoder routers path | `model.decoder.layers[i].router`, `i ∈ [0, 30)` | modeling L1197–1202 |
| Encoder routers path | `model.encoder.language_model.layers[i].router` | modeling L979, L865, L883 |
| Top model | `DiffusionGemmaForBlockDiffusion` → `self.model` (`DiffusionGemmaModel` L1471, `.encoder`/`.decoder` L1497–1498) | modeling L1597 |

The probe matches routers by **class name string** (`DiffusionGemmaTextRouter`)
via `named_modules()`, so it needs no transformers import and the metrics suite
runs with the model absent. The router's return tuple index 0 is also the
`OutputRecorder` HF uses for `router_logits` (modeling L869/L1180), confirming
index 0 = full per-token probabilities.

## Timestep interface

Source: `generation_diffusion_gemma.py`.

- `DiffusionGemmaGenerationMixin.generate` (L545): outer autoregressive loop
  over canvases; inner **denoising loop** at L757:
  `for cur_step in reversed(range(1, generation_config.max_denoising_steps + 1))`.
  **`cur_step` IS the denoising timestep `t`** (counts down `N…1`).
- Each inner iteration calls `_denoising_step` (L1003), which runs the decoder
  **exactly once** per step (L1029). So decoder MoE routers fire **once per
  denoising timestep**.
- `cur_step` is **not** passed to the model `forward`. The probe therefore
  correlates router captures with `t` by counting **decoder forward passes**: a
  pre-forward hook on `DiffusionGemmaDecoderModel` increments a counter; the
  1-indexed pass `p` within a canvas maps to `t = num_timesteps − (p − 1)`
  (see `RoutingProbe._current_decoder_timestep`). `ProbeConfig.num_timesteps`
  **must equal** the generation config's `max_denoising_steps` for correct tags.
- Encoder routers fire once per canvas (prefill / AR step), so their tag is the
  canvas index, not a denoising `t`. Encoder capture is off by default
  (`capture_encoder=False`).

## Config facts (from `config.json` → `text_config`)

| Field | Value |
|-------|------:|
| `num_experts` | **128** |
| `top_k_experts` | **8** |
| `num_hidden_layers` | **30** |
| `hidden_size` | 2816 |
| `moe_intermediate_size` | 704 |
| `canvas_length` | 256 |
| architecture | `DiffusionGemmaForBlockDiffusion` (`model_type: diffusion_gemma`) |

Snapshot read:
`/data/huggingface/hub/models--unsloth--diffusiongemma-26B-A4B-it/snapshots/fe82f78.../config.json`

## H4 test (track-stratified conditional-MI / G with trajectory-synchronous FWER)

Implements `plan/h4-test-protocol.md` (designed by GPT-5.5 Pro after two earlier
designs were rejected). Authoritative detail + pseudocode:
`plan/h4-test-protocol-pro-raw.txt`. Implemented in `direction_c/h4_test.py`,
data model in `h4_data.py`, validation in `h4_validation.py`.

**Pre-registered estimand (lock BEFORE seeing routing results):** *For fixed
prompt, generated canvas/trajectory, and token position, the MoE routing
distribution carries statistically reliable information about the denoising
timestep bucket.*

**Pre-registration (do NOT change after seeing results):**
- `alpha = 0.05`; `K = 8` equal-count timestep buckets `b(t)`.
- Track unit `i = (prompt_id, canvas_id, position p)` (prompt+canvas folded into
  `traj_idx`); permutation unit = the **trajectory** (one prompt + one canvas).
- Layer set = all decoder MoE layers `0..num_hidden_layers-1` (i.e. `0..29`).
- `B_perm = 19999` (paper) / `>= 9999` (min); smaller allowed for fast tests.
- Primary statistic = stratified-G; primary permutation = trajectory-synchronous;
  correction = shared-draw maxT. Primary expert mass = **unweighted top-k**
  (gate-weighted / top-1 are robustness checks). Primary uses **pre-capacity**
  router top-k.

**Statistic (per layer L)** — track-stratified conditional MI / G:
`T_L = 2 Σ_i Σ_b Σ_e C_ibe · log( (C_ibe · n_i) / (n_ib · C_i·e) )`, with
per-visit expert mass `Y` (unweighted top-k, sums to 1), C=0 terms contribute 0,
**no pseudocounts, no asymptotic χ²**. `T_L = 2 N_L · I_L(E;B|track)`. The old
max-pairwise-JS is demoted to optional post-hoc localization (folded into the
same correction if reported).

**Permutation (the core fix)** — TRAJECTORY-SYNCHRONOUS timestep relabeling: for
each trajectory `r` draw ONE permutation of its denoising-call indices; apply the
SAME relabeling of per-call bucket labels to all positions, all layers, all
experts, all statistics. Positions within a canvas at one timestep share the
denoising state, so they are NOT independently shuffleable; independent shuffles
would fabricate datasets the block-diffusion process could not produce.

**FWER** — `M = max_L T_L`; ONE shared permutation draw feeds ALL 30 layers each
iteration; global `p = (1+#{M^(m) >= M_obs})/(B_perm+1)`, reject global null iff
`<= alpha`; layer-wise single-step maxT adjusted p `p_L^adj =
(1+#{M^(m) >= T_L^obs})/(B_perm+1)`.

**Effect sizes:** `I_L = T_L/(2 N_L)` (nats/visit), `NMI_L = I_L/H(B|track)`,
bias-corrected `ΔNMI_L = (I_L^obs − median_π I_L^(π))/H(B|track)`, and
`cluster_bootstrap_nmi` 95% CI over trajectories.

`run_h4_test(dataset, ...) -> H4Result(supported, p_global, significant_layers,
per_layer=[LayerH4Result(...)], ...)`. H4 is FALSIFIED iff `supported is False`
(global null not rejected).

**Honesty caveat (must appear in the paper):** passive logs establish
*within-trajectory timestep ASSOCIATION* only ("expert usage is conditionally
time-aligned within fixed prompt/canvas/position tracks"), NOT causal "experts
read the timestep embedding." A causal claim requires a **timestep-swap
intervention**: freeze the canvas state, replay the router with a different
t-embedding, and test whether expert selection changes. That intervention is
out of scope for this passive-logging toolchain.

### Validation results (the proof, `tests/test_h4_decision.py`)

Type-I pass criterion (protocol §4): one-sided 95% Clopper-Pearson UPPER bound
`U_0.95 <= 0.065` at `alpha=0.05` — tight enough to reject a 2× inflation
(true 0.10 → `U_0.95 ≈ 0.11` at R=2000, far above 0.065). NOT `alpha + 3·SE`.

These are **SYNTHETIC-structure** checks. A synthetic generator cannot reproduce
the real model's actual track heterogeneity, top-k/cross-layer dependence,
sparsity, or missingness. The protocol's TRUE Null A (permutation-orbit on REAL
captured logs, `h4_validation.null_a_real_orbit`) is a **MANDATORY
pre-publication gate** that runs only once the 26B model produces logs — see
"Real-data Null A gate" below. Do not present the synthetic FWER numbers as
real-structure evidence.

| Synthetic null | what it preserves | R_null (in-test) | empirical FWER | U_0.95 |
|----------------|-------------------|------------------|----------------|--------|
| **A (synthetic)** orbit-relabel on synthetic data | synthetic track structure only | 2000 | ~0.050 | ~0.059 ✓ |
| **B** heterogeneous-track | per-track expert law ⟂ bucket | 2000 | ~0.054 | ~0.063 ✓ |
| **C** autocorrelated AR(1) ρ=0.8 | adjacent-call dependence (block diffusion) | 800 | ~0.047 | ~0.060 ✓ |

**Discriminating negative control (proves the shared draw is load-bearing).**
On a CROSS-LAYER-CORRELATED null (`make_null_xcorr`: a shared per-(traj,call)
latent perturbs all layers identically but is ⟂ bucket, so H0 holds while `T_L`
is positively correlated across layers), the in-test harness (`h4_broken.py`,
TEST-ONLY) runs the global maxT with the correct shared draw vs a deliberately
broken per-layer-INDEPENDENT draw and shows they are MEASURABLY different:
- **CORRECT (shared draw):** global-null p-values ≈ Uniform(0,1) — KS-uniform
  p ≈ 0.75 (NOT rejected), FWER ≈ 0.04.
- **BROKEN (per-layer independent):** mis-calibrated — KS-uniform p ≈ 1e-22
  (decisively rejected), null p-values skewed high (mean ≈ 0.62), i.e. the
  destroyed cross-layer correlation inflates the permutation max threshold and
  the test loses calibration.
This is the test that the earlier Null A/B alone could NOT provide: those
independent-ish synthetic tracks let a broken per-layer permutation pass too, so
they proved nothing about the shared draw. The cross-layer-correlated null +
broken-variant comparison is the discriminator.

**Full-pipeline 2× detection.** A separate test runs the ACTUAL `run_h4_test()`
end-to-end on a genuine weak H0-violation (a small planted `t→expert` tilt) tuned
so the true global rejection rate ≈ 0.10, and asserts the empirical CP upper
bound EXCEEDS 0.065 — proving the pipeline + bound actually flag a 2× situation
(not just that the CP arithmetic is right).

**Power:** planted logit-tilt `q(δ) ∝ q̂·exp(δ g_b h_e)` with early/late
specialist sets; global detection rises 0 → ~1 over δ∈{0,0.5,0.9}; the planted
layer is identified after maxT at δ=0.5–0.9; detection at δ=0 stays ≈ α.

### Real-data Null A gate (MANDATORY before any H4 claim)

`h4_validation.null_a_real_orbit(real_dataset, r_null=5000, ...)` runs the
protocol's true Null A on REAL probe logs: it repeatedly relabels timesteps
within each trajectory via the test's own allowed group, treats each relabeled
dataset as "observed," runs the full test, and requires `U_0.95 <= 0.065`.
Because the labels come from the test's own null group, a passing FWER on the
REAL data's structure is the only evidence that the implementation is calibrated
on the actual model — the synthetic checks above are necessary but not
sufficient. This gate CANNOT run until the 26B model produces logs; it is a
required step of the C2/H4 run, not an offline-only check.

## Run command when the model lands

```python
import torch
from transformers import DiffusionGemmaForBlockDiffusion, AutoProcessor
from direction_c import ProbeConfig, run_probe

MODEL = "/data/huggingface/hub/models--unsloth--diffusiongemma-26B-A4B-it/snapshots/fe82f78ffb05c3790ffc1229fec0bfe5ab6c57be"
MAX_DENOISING_STEPS = 64  # MUST match ProbeConfig.num_timesteps below

model = DiffusionGemmaForBlockDiffusion.from_pretrained(
    MODEL, dtype=torch.bfloat16, device_map="auto"
)
processor = AutoProcessor.from_pretrained(MODEL)

cfg = ProbeConfig(
    num_experts=128, top_k=8,
    num_timesteps=MAX_DENOISING_STEPS,  # keep in sync with generate kwarg
    num_timestep_buckets=8,
    capture_encoder=False,
    output_dir="direction_c/outputs",
    seed=42,
)

# Verifiable-domain prompts only; do NOT use the sealed GSM8K test split.
prompts = ["Repair this function: ...", "Generate JSON matching schema: ..."]

path = run_probe(
    model, processor, prompts, cfg,
    run_name="h4_dirC_run0",
    max_new_tokens=256,
    generate_kwargs={"max_denoising_steps": MAX_DENOISING_STEPS},
)
```

For the preferred timestep-tagging path, wrap `_denoising_step` so the true
`cur_step` is stamped before each decoder forward (removes even the within-canvas
residual risk):

```python
import types
from direction_c import ProbeConfig, RoutingProbe

probe = RoutingProbe(model, cfg)
probe.attach(expected_decoder_layers=model.config.text_config.num_hidden_layers)
orig = model._denoising_step
def _wrapped(self, *a, cur_step, **k):
    probe.set_external_timestep(int(cur_step))
    return orig(*a, cur_step=cur_step, **k)
model._denoising_step = types.MethodType(_wrapped, model)
# ... run generate per prompt, calling probe.start_prompt() before each ...
```

Then run the H4 test offline (no model needed):

```python
from direction_c import load_h4_dataset, run_h4_test, cluster_bootstrap_nmi

dataset = load_h4_dataset(path, tower="decoder", mode="unweighted")  # primary
res = run_h4_test(dataset, alpha=0.05, b_perm=19999, seed=12345)     # pre-registered
print("H4 supported (global null rejected):", res.supported, "p_global =", res.p_global)
print("significant layers (maxT):", res.significant_layers)
for lr in res.per_layer:
    print(lr.layer_idx, round(lr.t_stat, 2), round(lr.p_adj_maxt, 4),
          round(lr.nmi, 4), round(lr.delta_nmi, 4))
lo, hi = cluster_bootstrap_nmi(dataset, layer=res.significant_layers[0], n_boot=2000)
```

Equivalent CLI smoke (offline, fake model): the full save→load round-trip is in
`tests/test_probe_hooks.py::test_multi_record_per_cell_roundtrip_no_overwrite`;
the full type-I + power validation is in `tests/test_h4_decision.py` (Null A/B/C
+ planted-effect power).

## Reproducibility

`seed` is recorded in `ProbeConfig` and persisted into every `.npz`. `run_probe`
seeds `torch` and `numpy` before generation. Record git hash, env (`conda env:
dllm`, transformers 5.12.1, torch 2.7.1+cu126), and the exact `generate` kwargs
alongside outputs.

## OPEN_RISKS (unverifiable without the model)

1. **Within-canvas early-exit timestep skew (residual).** The pass-counter
   fallback now resets at every canvas boundary (encoder pre-hook) and every
   prompt (`start_prompt`), so NO stale offset leaks across canvases/prompts
   (this was FATAL 2, fixed). The only residual risk is a single canvas that
   **early-exits** before `num_timesteps` decoder passes (generate L788 /
   adaptive stopping): that canvas's last step would still be tagged from the
   high end of the schedule. **Mitigation:** use the external-timestep path
   (`probe.set_external_timestep(cur_step)` from a `_denoising_step` wrapper,
   shown above) which stamps the exact `cur_step` and removes this entirely; or
   disable adaptive diffusion stopping for the probe run. `test_external_timestep_overrides_fallback`
   verifies the stamping path on the fake model; the wrapper itself needs the
   real model to confirm `_denoising_step`'s `cur_step` kwarg signature.
2. **Multi-canvas pooling (intended).** Records from all canvases that share the
   same denoising `t` are pooled into the same `t_bucket` (we study `t`, not
   canvas index). Per-canvas effects are therefore not separated. Verified
   correct under the fake multi-canvas simulation
   (`test_decoder_pass_resets_per_canvas_no_timestep_contamination`); confirm the
   pooling is acceptable for the science question once the model is loaded.
3. **`use_experts_implementation` decorator.** `DiffusionGemmaTextExperts` is
   wrapped by `@use_experts_implementation` (modeling L530), which may swap the
   experts kernel. This does **not** affect the probe — we hook the *router*
   (`DiffusionGemmaTextRouter`), whose output tuple is the selection signal.
   But the router's `top_k_index` is what the experts consume, so no separate
   experts hook is needed. Verify the router still returns the 3-tuple under the
   active experts implementation when the model loads.
4. **bf16 / device.** `_to_numpy` casts captured tensors to fp32 CPU; verified
   only on CPU fp32 fake tensors. The cast path for bf16-CUDA tensors is
   standard but untested without the model.
5. **Encoder MoE timestep semantics.** Encoder routers are tagged by canvas
   index, not denoising `t`; their use for H4 is secondary. Untested against the
   real encoder/prefill call pattern.
6. **Metadata schema fields requiring the live model (protocol §5).** The probe
   logs the CORE fields the test needs: `trajectory_id = (prompt_id, canvas_id)`,
   `call_index s`, `t` + bucket `b(t)`, position `p`, layer, ordered top-k expert
   ids, and gate probs (when `capture_logits=True`). The following protocol §5
   fields are **TODO** because they cannot be obtained without running the model:
   - **`log_snr` per call:** wired as a field (`set_external_timestep(t, log_snr)`)
     but the schedule→log-SNR map must come from the loaded model's
     `generation_config`/sampler. Currently `nan` (placeholder). TODO.
   - **canvas-state hash / per-position token id / mask-active flag / per-position
     confidence-entropy:** require the live denoising loop's tensors; not exposed
     to a router forward hook. TODO — needed for the "you're measuring token-state
     evolution, not timestep" sensitivity analysis, NOT for the primary test.
   - **prompt/output/checkpoint/config hashes, seed, decode settings, batch
     composition:** trajectory-level provenance; wire from the run harness when
     the model lands. TODO.
7. **Pre- vs post-capacity experts.** The probe records `pre_capacity=True`
   because `DiffusionGemmaTextRouter` exposes the pre-capacity top-k directly
   (the primary per protocol §5). DiffusionGemma's experts container
   (`@use_experts_implementation`) applies any capacity AFTER the router; logging
   post-capacity *dispatched* experts + an overflow flag is a TODO that needs the
   live experts kernel. Primary test is unaffected (uses pre-capacity top-k).
8. **Schedule nonuniformity → bucket definition.** `K=8` buckets are equal-count
   over the *call index* here. If the real denoising schedule is nonuniform, the
   protocol prefers equal-width buckets in log-SNR; that requires the model's
   schedule (see risk 6, `log_snr`). Re-bucketization choices must be folded into
   the maxT correction or chosen on a pilot split — do NOT tune K after seeing
   results.
