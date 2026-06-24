"""Forward-hook instrumentation for DiffusionGemma MoE routing during denoising.

This module attaches forward hooks to every MoE router in a DiffusionGemma
model and records, per (layer, denoising-timestep, token), the experts selected
(top-k indices) and their routing weights. Records are bucketed by denoising
timestep ``t`` and persisted to disk for offline analysis by ``metrics``.

================================================================================
REAL MODULE NAMES (verified by reading transformers 5.12.1 source -- NOT guessed)
================================================================================
Source root:
    transformers/models/diffusion_gemma/modeling_diffusion_gemma.py
    transformers/models/diffusion_gemma/generation_diffusion_gemma.py

MoE building blocks (modeling_diffusion_gemma.py):
- ``DiffusionGemmaTextRouter`` (class def @ L493). The gate/router. Its forward
  (L506-527) returns a 3-tuple:
      (router_probabilities[B*S, E], top_k_weights[B*S, K], top_k_index[B*S, K])
  The gate Linear is ``router.proj`` (``nn.Linear(hidden_size, num_experts)``,
  L502). top-k selection uses ``torch.topk(..., k=config.top_k_experts)`` (L515).
- ``DiffusionGemmaTextExperts`` (class def @ L531). The experts container; expert
  weights are 3-D Parameters ``experts.gate_up_proj`` (L539) and
  ``experts.down_proj`` (L540). Its forward (L543) takes ``top_k_index`` and
  ``top_k_weights`` from the router.
- MoE block lives inside the *layer* classes (no separate "MoE block" class):
  ``DiffusionGemmaEncoderTextLayer`` (L570) and ``DiffusionGemmaDecoderTextLayer``
  (L644). Each holds ``self.router`` (L591 / L666) and ``self.experts``
  (L592 / L667) and calls them at L629-630 (encoder) / L704-705 (decoder).

Model wiring (modeling_diffusion_gemma.py):
- ``DiffusionGemmaForBlockDiffusion`` (L1597) -> ``self.model`` is a
  ``DiffusionGemmaModel`` (L1471).
- ``DiffusionGemmaModel.decoder`` is a ``DiffusionGemmaDecoderModel`` (L1168);
  its layers are ``model.decoder.layers[i].router`` for i in 0..num_hidden_layers-1.
- ``DiffusionGemmaModel.encoder`` is a ``DiffusionGemmaEncoderModel`` (L979);
  its routers are ``model.encoder.language_model.layers[i].router`` (the text
  model is ``DiffusionGemmaEncoderTextModel`` @ L865).

Timestep interface (generation_diffusion_gemma.py):
- ``DiffusionGemmaGenerationMixin.generate`` (L545). Outer loop over canvases;
  inner denoising loop at L757: ``for cur_step in reversed(range(1, max_denoising_steps+1))``.
  ``cur_step`` IS the denoising timestep t (counts down N..1).
- Each inner iteration calls ``_denoising_step`` (L1003), which at L1029 runs the
  decoder forward exactly ONCE per step. The MoE routers in the decoder therefore
  fire once per denoising timestep. ``cur_step`` is NOT passed to the model
  forward, so this probe correlates router captures with t by counting decoder
  forward passes (see ``RoutingProbe._decoder_pre_hook``).

CONFIG FACTS (from the model's config.json text_config):
    num_experts=128, top_k_experts=8, num_hidden_layers=30, hidden_size=2816,
    moe_intermediate_size=704, canvas_length=256.

H4 SCHEMA (protocol plan/h4-test-protocol.md §5): each RouterRecord carries the
exchangeability-unit metadata: trajectory = (prompt_id, canvas_id), denoising
call_index s, timestep t + bucket b(t), and per-token positions (the token rows).
The track key is (prompt_id, canvas_id, position); the permutation unit is the
trajectory. TODO (cannot wire without the live model, see README OPEN_RISKS 6/7):
log_snr per call, canvas-state hash, per-position token id / mask-active flag /
confidence, post-capacity dispatched experts + overflow flag, run-level provenance
hashes. These are sensitivity-analysis fields; the PRIMARY test uses only the core
fields above with PRE-capacity router top-k.
================================================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

from direction_c.config import ProbeConfig, RouterRecord
from direction_c.persistence import save_records
from direction_c.probe_utils import parse_router_location, to_numpy

# Private aliases kept for the hook-mechanism tests that import them by name.
_parse_router_location = parse_router_location
_to_numpy = to_numpy

if TYPE_CHECKING:  # avoid importing transformers/torch.nn types at runtime import
    from torch import nn

logger = logging.getLogger(__name__)

# Verified class names (string-matched so the probe needs no transformers import
# and degrades gracefully if the model is absent). See module docstring.
ROUTER_CLASS_NAME: str = "DiffusionGemmaTextRouter"
DECODER_MODEL_CLASS_NAME: str = "DiffusionGemmaDecoderModel"
ENCODER_MODEL_CLASS_NAME: str = "DiffusionGemmaEncoderModel"


class RoutingProbe:
    """Attaches forward hooks to every MoE router and records selections.

    Usage::

        probe = RoutingProbe(model, config)
        probe.attach(expected_decoder_layers=model.config.text_config.num_hidden_layers)
        try:
            for prompt_id, prompt in enumerate(prompts):
                probe.start_prompt(prompt_id=prompt_id)   # REQUIRED per prompt
                model.generate(...)
        finally:
            probe.detach()
        probe.save("run0")

    CRITICAL for direct callers (not using ``run_probe``): you MUST call
    ``start_prompt()`` / ``start_trajectory()`` (alias) before generating EACH
    prompt. It resets the per-canvas denoising-call counter and canvas index and
    advances the trajectory id. Skipping it lets the call index / timestep
    mapping carry a stale offset across prompts -- the FATAL-2 bug -- and corrupts
    the trajectory key ``(prompt_id, canvas_id, position)`` that the H4 test's
    exchangeability unit (the trajectory) depends on. ``run_probe`` does this for
    you; manual loops must not omit it.

    The probe is model-independent at import time: it discovers router modules
    by class name at ``attach`` time, so this file can be imported and the
    metrics tested without the 26B model present.
    """

    def __init__(self, model: "nn.Module", config: ProbeConfig) -> None:
        """Initialize the probe.

        Args:
            model: A ``DiffusionGemmaForBlockDiffusion`` (or compatible) module.
            config: The :class:`ProbeConfig` controlling capture behavior.
        """
        self._model = model
        self._config = config
        self._handles: list[Any] = []
        self._records: list[RouterRecord] = []
        # Decoder forward-pass counter == per-canvas denoising CALL index s.
        # RESET at every new canvas (encoder forward) and every new prompt, so
        # the call index / timestep mapping never carries a stale offset across
        # canvases/prompts (H4 permutation unit = trajectory = prompt+canvas).
        self._decoder_pass: int = 0
        self._canvas_idx: int = 0
        # H4 trajectory metadata: the current prompt id (set per prompt) and the
        # external true cur_step (preferred over the pass-counter fallback).
        self._prompt_id: int = 0
        self._external_timestep: int | None = None
        self._external_log_snr: float = float("nan")
        # Monotonic id assigned to each router invocation (collision-free key).
        self._next_record_id: int = 0
        # Identity map of router module -> (tower, layer_idx), filled at attach.
        self._router_meta: dict[int, tuple[str, int]] = {}

    @property
    def records(self) -> list[RouterRecord]:
        """Return the list of captured :class:`RouterRecord` objects."""
        return self._records

    def attach(self, *, expected_decoder_layers: int | None = None) -> int:
        """Register hooks on all routers, the decoder model, and the encoder.

        Args:
            expected_decoder_layers: If given, assert that exactly this many
                distinct decoder layer indices ``0..expected-1`` were hooked,
                and fail loudly otherwise. This guards against silent partial
                coverage when quantization / module-wrapping changes class names
                (fixes MAJOR 6). Pass ``30`` for DiffusionGemma 26B-A4B.

        Returns:
            The number of router modules hooked.

        Raises:
            RuntimeError: If no routers are found, or if the expected decoder
                layer set is not fully covered.
        """
        n_routers, decoder_layers = self._register_router_hooks()
        self._register_canvas_step_hooks()
        if n_routers == 0:
            raise RuntimeError(
                f"No '{ROUTER_CLASS_NAME}' modules found; is this a DiffusionGemma model?"
            )
        if expected_decoder_layers is not None:
            expected = set(range(expected_decoder_layers))
            missing = sorted(expected - decoder_layers)
            extra = sorted(decoder_layers - expected)
            if missing or extra:
                raise RuntimeError(
                    f"Decoder router coverage mismatch: expected layers "
                    f"{sorted(expected)}, hooked {sorted(decoder_layers)} "
                    f"(missing={missing}, unexpected={extra}). Refusing to run "
                    f"with partial MoE coverage."
                )
            logger.info("Verified full decoder coverage: %d layers", expected_decoder_layers)
        logger.info("RoutingProbe attached to %d router modules", n_routers)
        return n_routers

    def detach(self) -> None:
        """Remove all registered hooks."""
        for handle in self._handles:
            handle.remove()
        self._handles.clear()
        logger.info("RoutingProbe detached (%d records captured)", len(self._records))

    def reset(self) -> None:
        """Clear captured records and all counters (keeps hooks attached)."""
        self._records.clear()
        self._decoder_pass = 0
        self._canvas_idx = 0
        self._prompt_id = 0
        self._external_timestep = None
        self._external_log_snr = float("nan")
        self._next_record_id = 0

    def start_prompt(self, prompt_id: int | None = None) -> None:
        """Begin a new trajectory: reset per-prompt counters; set prompt id.

        Resets the per-canvas call counter and canvas index so timestep tagging
        starts cleanly for each prompt. Records and ids are NOT cleared, so
        multiple prompts accumulate into one dataset. The H4 trajectory key is
        ``(prompt_id, canvas_id)``.

        Args:
            prompt_id: Identifier for this prompt. If ``None``, auto-increments.
        """
        self._decoder_pass = 0
        self._canvas_idx = 0
        self._external_timestep = None
        self._external_log_snr = float("nan")
        self._prompt_id = self._prompt_id + 1 if prompt_id is None else prompt_id

    # Backwards-compatible alias used in earlier code paths.
    start_trajectory = start_prompt

    def set_canvas_index(self, canvas_idx: int) -> None:
        """Set the encoder-side canvas index used to tag encoder router records.

        Args:
            canvas_idx: The autoregressive canvas index (reset to 0 per prompt).
        """
        self._canvas_idx = canvas_idx

    def set_external_timestep(self, cur_step: int | None,
                              log_snr: float = float("nan")) -> None:
        """Stamp the TRUE denoising timestep (and optional log-SNR) for the next call.

        The preferred path: a caller that can observe the generation loop's
        ``cur_step`` (e.g. by wrapping ``_denoising_step``) calls this with the
        exact ``cur_step`` before each decoder forward, overriding the
        pass-counter fallback. Pass ``None`` to revert to the fallback.

        Args:
            cur_step: The denoising timestep ``t`` for the upcoming decoder
                forward, or ``None`` to use the pass-counter fallback.
            log_snr: Optional per-call noise level / log-SNR for sensitivity
                analyses. Defaults to ``nan`` (not exposed).
        """
        self._external_timestep = cur_step
        self._external_log_snr = log_snr

    # -- internal hook wiring -------------------------------------------------

    def _register_router_hooks(self) -> tuple[int, set[int]]:
        count = 0
        decoder_layers: set[int] = set()
        for name, module in self._model.named_modules():
            if type(module).__name__ != ROUTER_CLASS_NAME:
                continue
            tower, layer_idx = _parse_router_location(name)
            if tower == "encoder" and not self._config.capture_encoder:
                continue
            self._router_meta[id(module)] = (tower, layer_idx)
            handle = module.register_forward_hook(self._router_forward_hook)
            self._handles.append(handle)
            if tower == "decoder":
                decoder_layers.add(layer_idx)
            count += 1
        return count, decoder_layers

    def _register_canvas_step_hooks(self) -> None:
        """Hook the decoder (per-step counter) and encoder (canvas boundary)."""
        hooked_decoder = False
        for module in self._model.modules():
            cls_name = type(module).__name__
            if cls_name == DECODER_MODEL_CLASS_NAME:
                self._handles.append(
                    module.register_forward_pre_hook(self._decoder_pre_hook)
                )
                hooked_decoder = True
            elif cls_name == ENCODER_MODEL_CLASS_NAME:
                # The encoder runs once at the start of each canvas; use it as a
                # canvas boundary to RESET the per-canvas decoder pass counter.
                self._handles.append(
                    module.register_forward_pre_hook(self._encoder_pre_hook)
                )
        if not hooked_decoder:
            logger.warning(
                "No '%s' found; decoder timestep tracking disabled (records get t=-1)",
                DECODER_MODEL_CLASS_NAME,
            )

    def _encoder_pre_hook(self, module: "nn.Module", args: tuple, kwargs: dict | None = None) -> None:
        """Mark a new canvas: reset the per-canvas pass counter, bump canvas idx."""
        self._decoder_pass = 0
        self._canvas_idx += 1

    def _decoder_pre_hook(self, module: "nn.Module", args: tuple, kwargs: dict | None = None) -> None:
        """Increment the per-canvas decoder forward-pass counter."""
        self._decoder_pass += 1

    def _current_decoder_timestep(self) -> int:
        """Return the raw denoising timestep ``t`` for the current decoder pass.

        Preferred path: if an external caller stamped the true ``cur_step`` via
        :meth:`set_external_timestep`, return it directly (exact, no modulo).

        Fallback path: map the per-canvas 1-indexed pass ``p`` to
        ``t = num_timesteps - (p - 1)``. ``_decoder_pass`` is reset to 0 at each
        canvas boundary (encoder pre-hook) and each prompt (``start_prompt``),
        so NO stale offset leaks across canvases/prompts -- which is what caused
        FATAL 2. The residual risk (documented in README OPEN_RISKS #1) is only
        WITHIN a single canvas that early-exits before ``num_timesteps`` passes:
        the LAST step's ``t`` would still be tagged from the high end of the
        schedule. The external-timestep path removes even that residual risk and
        is the recommended mode for the real run.
        """
        if self._external_timestep is not None:
            return max(1, int(self._external_timestep))
        n = self._config.num_timesteps
        pass_in_canvas = (self._decoder_pass - 1) % n if n > 0 else 0
        return max(1, n - pass_in_canvas)

    def _router_forward_hook(
        self,
        module: "nn.Module",
        inputs: tuple,
        output: tuple,
    ) -> None:
        """Capture (layer, t, token) -> expert selection from a router forward.

        ``output`` is the router's return tuple
        ``(router_probabilities, top_k_weights, top_k_index)`` (see source).
        """
        tower, layer_idx = self._router_meta.get(id(module), ("decoder", -1))
        try:
            router_probs, top_k_weights, top_k_index = output[0], output[1], output[2]
        except (TypeError, IndexError):  # defensive: unexpected output shape
            logger.warning("Router output not a 3-tuple at layer %d; skipping", layer_idx)
            return

        if tower == "decoder":
            timestep = self._current_decoder_timestep()
            call_index = self._decoder_pass
        else:
            timestep = self._canvas_idx
            call_index = -1
        t_bucket = self._config.bucket_of(timestep) if tower == "decoder" else timestep

        probs_arr: np.ndarray | None = None
        if self._config.capture_logits:
            probs_arr = _to_numpy(router_probs)

        record_id = self._next_record_id
        self._next_record_id += 1
        self._records.append(
            RouterRecord(
                record_id=record_id,
                layer_idx=layer_idx,
                tower=tower,
                timestep=timestep,
                t_bucket=t_bucket,
                top_k_index=_to_numpy(top_k_index).astype(np.int32),
                top_k_weights=_to_numpy(top_k_weights).astype(np.float32),
                prompt_id=self._prompt_id,
                canvas_id=self._canvas_idx,
                call_index=call_index,
                log_snr=self._external_log_snr,
                pre_capacity=True,
                router_probabilities=probs_arr,
            )
        )

    # -- persistence ----------------------------------------------------------

    def save(self, run_name: str) -> Path:
        """Persist captured records to a single ``.npz`` keyed by (layer, t, expert).

        Delegates to :func:`direction_c.persistence.save_records`, which stores
        flat columnar arrays so downstream code can group by
        ``(tower, layer_idx, t_bucket, expert)`` without loading torch.

        Args:
            run_name: Used to name the output file ``<run_name>_routing.npz``.

        Returns:
            The path to the written ``.npz`` file.
        """
        return save_records(self._records, self._config, run_name)
