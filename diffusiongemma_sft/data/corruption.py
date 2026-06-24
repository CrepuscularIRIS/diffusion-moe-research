"""D3PM-uniform forward corruption for DiffusionGemma block-diffusion SFT.

Mirrors NeMo's ``corrupt_uniform_random`` (nemo_automodel/components/datasets/dllm/
corruption.py:223-294). Key properties verified against the reference:

- One corruption level ``t ~ U(eps, 1)`` is sampled PER SEQUENCE (block_size=None path).
- Each supervised position is independently corrupted with probability ``t``.
- Replacement is a UNIFORM RANDOM vocab token (NOT a [MASK] token — DiffusionGemma
  uses D3PM-uniform, matching the checkpoint's own canvas init/renoising).
- ``p_mask`` is all ones: the loss is a flat CE with NO 1/t reweighting.

The corruption is applied to the full clean sequence; only positions where
``loss_mask`` is true are eligible for corruption (prompt tokens stay clean).
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class CorruptionConfig:
    """Immutable config for D3PM-uniform corruption."""

    vocab_size: int = 262144
    eps: float = 1e-3


def corrupt_uniform_random(
    input_ids: torch.Tensor,
    loss_mask: torch.Tensor,
    config: CorruptionConfig,
    generator: torch.Generator | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Apply D3PM-uniform corruption to the supervised region.

    Args:
        input_ids: Clean token ids, shape ``[B, S]``.
        loss_mask: Supervised-position mask (1 on assistant/EOS-fill tokens),
            shape ``[B, S]``; bool or {0,1} float.
        config: Corruption hyperparameters.
        generator: Optional torch.Generator for reproducible sampling. Should be
            on the same device as ``input_ids``.

    Returns:
        noisy: Corrupted token ids, shape ``[B, S]``.
        noise_mask: Bool mask of positions that were actually corrupted,
            shape ``[B, S]``. (Returned for inspection; the SFT loss does NOT
            gate on it — loss is over all supervised canvas tokens.)
    """
    if input_ids.dim() != 2:
        raise ValueError(f"input_ids must be [B, S], got shape {tuple(input_ids.shape)}")
    if input_ids.shape != loss_mask.shape:
        raise ValueError(
            f"input_ids {tuple(input_ids.shape)} and loss_mask "
            f"{tuple(loss_mask.shape)} must match"
        )

    device = input_ids.device
    b, s = input_ids.shape
    loss_bool = loss_mask.bool()

    # One corruption level t ~ U(eps, 1) per sequence.
    t = config.eps + (1.0 - config.eps) * torch.rand(
        (b, 1), device=device, generator=generator
    )

    # Each supervised position independently corrupted with probability t.
    draw = torch.rand((b, s), device=device, generator=generator)
    noise_mask = (draw < t) & loss_bool

    # Replacement = uniform random vocab token.
    random_tokens = torch.randint(
        0, config.vocab_size, (b, s), device=device, generator=generator
    )
    noisy = torch.where(noise_mask, random_tokens, input_ids)

    return noisy, noise_mask


def corruption_generator(
    base_seed: int,
    step: int,
    microbatch_idx: int,
    rank: int,
    device: torch.device | str = "cpu",
) -> torch.Generator:
    """Build the reproducible generator NeMo uses for corruption.

    Seed formula (train_ft.py:244-262): the ``(2 << 42)`` offset decorrelates the
    corruption stream from block-selection (``1 << 42``) and self-conditioning (``+0``).
    """
    gen = torch.Generator(device=device)
    gen.manual_seed(base_seed + 7919 * step + microbatch_idx + 104729 * rank + (2 << 42))
    return gen
