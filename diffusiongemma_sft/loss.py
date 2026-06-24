"""Loss functions for DiffusionGemma block-diffusion SFT (model-independent).

Clean re-implementation of the NeMo dLLM loss path (pure tensor logic, no model):

- ``block_diffusion_loss`` — flat masked CE over the selected canvas, mirroring
  ``BlockDiffusionCrossEntropyLoss`` (nemo_automodel/components/loss/dllm_loss.py:164-233).
  ALL supervised canvas positions (corrupted AND uncorrupted) are scored; there is
  NO ``1/t`` reweighting (that is the absorbing-MASK ELBO weight, inapplicable to
  the D3PM-uniform kernel) and ``noise_mask`` does NOT gate the loss.
- ``encoder_ar_loss`` — standard causal next-token CE on the clean sequence,
  mirroring ``encoder_ar_loss`` (dllm_loss.py:47-78), supported on
  ``attention_mask[:, :-1] & attention_mask[:, 1:]``.
- ``softcap_logits`` — ``tanh(logits / cap) * cap`` in fp32, mirroring
  ``_softcap_logits`` (models/diffusion_gemma/model.py:513-519).
"""

from __future__ import annotations

import torch
import torch.nn.functional as F


def softcap_logits(logits: torch.Tensor, cap: float | None) -> torch.Tensor:
    """Apply Gemma final-logit softcapping in fp32.

    Mirrors model.py:513-519: upcast to fp32, then (if ``cap`` is set)
    ``tanh(logits / cap) * cap``. CE is computed on these fp32 softcapped logits.

    Args:
        logits: Raw logits, any shape ``[..., V]``.
        cap: ``final_logit_softcapping`` value; ``None`` disables capping (only
            the fp32 upcast is applied).

    Returns:
        fp32 logits, same shape, softcapped to ``(-cap, cap)`` when ``cap`` is set.
    """
    out = logits.to(torch.float32)
    if cap is not None:
        out = torch.tanh(out / cap) * cap
    return out


def _per_token_nll(logits: torch.Tensor, target_ids: torch.Tensor) -> torch.Tensor:
    """Per-token negative log-likelihood, shape ``target_ids.shape`` (dllm_loss.py:31-44)."""
    vocab = logits.size(-1)
    return F.cross_entropy(
        logits.reshape(-1, vocab),
        target_ids.reshape(-1).to(logits.device),
        reduction="none",
    ).reshape(target_ids.shape)


def block_diffusion_loss(
    logits: torch.Tensor,
    target_ids: torch.Tensor,
    canvas_loss: torch.Tensor,
    num_diffusion_tokens: int | None = None,
) -> torch.Tensor:
    """Flat masked cross-entropy over the selected canvas (dllm_loss.py:192-233).

    The DiffusionGemma checkpoint uses D3PM-uniform corruption, so the loss is a
    plain mean CE over ALL supervised canvas positions (the ``canvas_loss``
    support — corrupted AND uncorrupted). ``noise_mask`` is intentionally NOT
    used and there is NO ``1/t`` reweighting.

    Args:
        logits: Canvas logits (fp32, softcapped), shape ``[B, R, V]``.
        target_ids: Clean canvas token ids, shape ``[B, R]``.
        canvas_loss: Boolean / {0,1} support mask, shape ``[B, R]`` — supervised
            AND valid AND in the step-selected block (from ``build_response_window``).
        num_diffusion_tokens: Global supervised-canvas-token count for the
            denominator (summed across grad-acc microbatches / DP ranks). If
            ``None``, normalizes by the local support count in this microbatch.

    Returns:
        Scalar diffusion loss.

    Raises:
        ValueError: On shape mismatch between ``logits[..., :2]`` and the masks.
    """
    if logits.dim() != 3:
        raise ValueError(f"logits must be [B, R, V], got shape {tuple(logits.shape)}")
    if logits.shape[:2] != target_ids.shape or target_ids.shape != canvas_loss.shape:
        raise ValueError(
            f"shape mismatch: logits {tuple(logits.shape)}, target_ids "
            f"{tuple(target_ids.shape)}, canvas_loss {tuple(canvas_loss.shape)}"
        )

    token_nll = _per_token_nll(logits, target_ids)  # [B, R]
    mask = canvas_loss.bool().to(token_nll.dtype)
    loss = (token_nll * mask).sum()

    denom = num_diffusion_tokens if num_diffusion_tokens is not None else int(mask.sum().item())
    return loss / max(denom, 1)


def encoder_ar_loss(
    encoder_logits: torch.Tensor,
    clean_ids: torch.Tensor,
    attention_mask: torch.Tensor | None = None,
    num_ar_tokens: int | None = None,
) -> torch.Tensor:
    """Autoregressive next-token CE on the encoder's causal logits (dllm_loss.py:47-78).

    A standard causal-LM cross-entropy over the clean full sequence, scored where
    BOTH the current and next position are valid (non-pad). The shift aligns
    ``encoder_logits[:, :-1]`` (prediction at position i) with ``clean_ids[:, 1:]``
    (token at position i+1).

    Args:
        encoder_logits: Encoder logits over the clean sequence (fp32, softcapped),
            shape ``[B, S, V]``.
        clean_ids: Clean token ids, shape ``[B, S]``.
        attention_mask: Boolean / {0,1} non-pad mask, shape ``[B, S]``. The scored
            positions are ``attention_mask[:, :-1] & attention_mask[:, 1:]``. If
            ``None``, all next-token positions count.
        num_ar_tokens: Global valid next-token count for the denominator. If
            ``None``, normalizes by the local valid count.

    Returns:
        Scalar AR loss.

    Raises:
        ValueError: On non-3D logits or a shape mismatch with ``clean_ids``.
    """
    if encoder_logits.dim() != 3:
        raise ValueError(f"encoder_logits must be [B, S, V], got shape {tuple(encoder_logits.shape)}")
    if encoder_logits.shape[:2] != clean_ids.shape:
        raise ValueError(
            f"encoder_logits {tuple(encoder_logits.shape)} and clean_ids "
            f"{tuple(clean_ids.shape)} must agree on [B, S]"
        )

    logits = encoder_logits[:, :-1, :]
    targets = clean_ids[:, 1:]
    nll = _per_token_nll(logits, targets)  # [B, S-1]
    if attention_mask is not None:
        valid = attention_mask.bool()
        mask = (valid[:, :-1] & valid[:, 1:]).to(nll.dtype)
    else:
        mask = torch.ones_like(nll)
    loss = (nll * mask).sum()

    denom = num_ar_tokens if num_ar_tokens is not None else int(mask.sum().item())
    return loss / max(denom, 1)
