"""Orchestration entry point for running the routing probe on the real model.

This module is used ONLY when the DiffusionGemma 26B model has landed. It wires
a :class:`~direction_c.probe.RoutingProbe` around ``model.generate`` (which runs
the block-diffusion denoising loop) and persists the captured routing records.

The probe itself (``probe.py``) is model-independent and unit-tested without a
model; this thin layer holds the parts that genuinely need a loaded model and a
tokenizer, so it is intentionally not exercised by the offline test suite.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
import torch

from direction_c.probe import ProbeConfig, RoutingProbe

if TYPE_CHECKING:
    from torch import nn

logger = logging.getLogger(__name__)


def run_probe(
    model: "nn.Module",
    tokenizer: Any,
    prompts: Sequence[str],
    config: ProbeConfig | None = None,
    *,
    run_name: str = "probe",
    max_new_tokens: int = 256,
    generate_kwargs: dict[str, Any] | None = None,
) -> Path:
    """Run block-diffusion denoising over ``prompts`` and record MoE routing.

    Thin orchestration layer: build the probe, attach hooks, run
    ``model.generate`` (which executes the denoising loop documented in
    ``probe.py``), then persist records bucketed by (layer, t, expert).

    Args:
        model: A loaded ``DiffusionGemmaForBlockDiffusion`` on the target device.
        tokenizer: A processor/tokenizer exposing ``apply_chat_template`` or
            ``__call__`` returning ``input_ids``.
        prompts: User prompts to denoise (each run as a separate generation).
        config: Probe configuration. If ``None``, a default is built; its
            ``num_timesteps`` SHOULD match the generation config's
            ``max_denoising_steps`` for correct t-tagging.
        run_name: Output file stem.
        max_new_tokens: Forwarded to ``generate``.
        generate_kwargs: Extra kwargs forwarded to ``model.generate`` (e.g.
            ``max_denoising_steps``). Keep ``num_timesteps`` in ``config`` in
            sync with ``max_denoising_steps`` here.

    Returns:
        Path to the persisted ``.npz`` file.
    """
    cfg = config or ProbeConfig()
    gen_kwargs = dict(generate_kwargs or {})
    # Reproducibility: seed before any sampling in the denoising loop.
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)
    logger.info(
        "run_probe: %d prompts, num_timesteps=%d, buckets=%d, seed=%d",
        len(prompts), cfg.num_timesteps, cfg.num_timestep_buckets, cfg.seed,
    )

    probe = RoutingProbe(model, cfg)
    # Verify FULL decoder MoE coverage so a class-name change under quantization
    # / module-wrapping cannot silently drop layers (MAJOR 6). num_hidden_layers
    # lives on text_config for diffusion_gemma.
    expected_layers = getattr(
        getattr(model.config, "text_config", model.config), "num_hidden_layers", None
    )
    probe.attach(expected_decoder_layers=expected_layers)
    try:
        for prompt_id, prompt in enumerate(prompts):
            input_ids = _encode_prompt(tokenizer, prompt, model)
            # Trajectory = (prompt_id, canvas_id); reset per-prompt counters so
            # call_index restarts per canvas (H4 permutation unit = trajectory).
            probe.start_prompt(prompt_id=prompt_id)
            # TODO(model-landed): for the exact-timestep + log-SNR path, wrap
            # ``model._denoising_step`` to call
            # ``probe.set_external_timestep(cur_step, log_snr)`` before each
            # decoder forward (cur_step + schedule->log-SNR come from the live
            # generation loop / sampler). See README OPEN_RISKS 1 and 6.
            with torch.no_grad():
                model.generate(input_ids, max_new_tokens=max_new_tokens, **gen_kwargs)
    finally:
        probe.detach()

    return probe.save(run_name)


def _encode_prompt(tokenizer: Any, prompt: str, model: "nn.Module") -> torch.Tensor:
    """Encode a single prompt into ``input_ids`` on the model device.

    Tries ``apply_chat_template`` first (DiffusionGemma processor convention),
    then falls back to direct tokenization.

    Args:
        tokenizer: A processor/tokenizer.
        prompt: The user prompt string.
        model: The loaded model (used to find the target device).

    Returns:
        ``input_ids`` tensor on the model's device.
    """
    device = next(model.parameters()).device
    if hasattr(tokenizer, "apply_chat_template"):
        chat = [{"role": "user", "content": prompt}]
        input_ids = tokenizer.apply_chat_template(chat, tokenize=True, return_tensors="pt")
    else:
        input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
    return input_ids.to(device)
