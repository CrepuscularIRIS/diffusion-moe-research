"""Two-pass block-diffusion forward for DiffusionGemma SFT.

The transformers ``DiffusionGemmaForBlockDiffusion.forward`` is an INFERENCE forward
(one decode pass, canvas logits only). Training needs the two-pass self-conditioning
+ co-trained encoder AR logits that live in NeMo's re-implemented forward. This module
reproduces that by driving the model's internal encoder/decoder directly:

  encoder ONCE  -> KV cache + encoder hidden (for the AR loss)
  decoder TWICE -> pass-1 (no-grad, no self-cond) gives the self-cond signal;
                   pass-2 (grad, self-cond gated per-example) gives canvas logits.

Verified against transformers ``modeling_diffusion_gemma.py``:
  - ``DiffusionGemmaModel.forward`` (:1516) shows encoder->cache->decoder wiring.
  - The decoder attention (:446-452) reads the encoder KV and ``cat``s the canvas KV
    in a LOCAL var; it does NOT call ``past_key_values.update()`` -> it does not write
    back to the cache. So the SAME encoder cache is safely reused across both decoder
    passes without contamination.
  - The encoder auto-creates a ``DynamicCache`` when ``past_key_values=None`` (:911-912).
  - Passing ``decoder_attention_mask`` as a dict bypasses the model's internal mask
    construction (:1272-1278), so we feed our own block-causal mask from build_response_window.

Gradient correctness: the encoder runs under grad (its params train via the AR loss
and via canvas-loss backprop through the cache). Pass-1 is wrapped in ``torch.no_grad``
and the signal is ``.detach()``ed. Pass-2 runs under grad; reading the grad-carrying
encoder KV from the cache lets the canvas loss backprop into the encoder.
"""

from __future__ import annotations

import re

import torch

from diffusiongemma_sft.loss import softcap_logits

# MoE router parameter name patterns (DiffusionGemmaTextRouter). The experts (fused 3D
# GroupedExperts) stay trainable; only the gate/router is frozen, matching NeMo's
# ``freeze_router`` and the LoRA-target choice in unsloth's FastDiffusionModel.
_ROUTER_PARAM_PATTERNS = (
    re.compile(r"\brouter\b"),
    re.compile(r"\bgate\b.*\bproj\b"),
    re.compile(r"\bgate\b.*\bscale\b"),
)


def _model_softcap(model) -> float | None:
    """Resolve final_logit_softcapping from the model (falls back to text_config)."""
    cap = getattr(model, "final_logit_softcapping", None)
    if cap is None:
        cap = getattr(getattr(model.config, "text_config", model.config), "final_logit_softcapping", None)
    return cap


def two_pass_forward(
    model,
    clean_ids: torch.Tensor,
    encoder_attention_mask: torch.Tensor,
    window: dict,
    do_self_conditioning: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Run the block-diffusion training forward.

    Args:
        model: A loaded ``DiffusionGemmaForBlockDiffusion``.
        clean_ids: Clean full sequence ``[B, S]`` (prompt + response + EOS-fill).
        encoder_attention_mask: ``[B, S]`` (1 over real/EOS-fill tokens, 0 over pad).
        window: Output of ``build_response_window`` — must contain ``canvas_ids`` ``[B, R]``,
            ``decoder_position_ids`` ``[B, R]``, and ``decoder_attention_mask`` (a dict with
            ``full_attention`` / ``sliding_attention`` ``[B, 1, R, S+R]``).
        do_self_conditioning: ``[B]`` bool, per-example self-conditioning coin.

    Returns:
        canvas_logits: ``[B, R, V]`` fp32 softcapped logits over the canvas (grad).
        encoder_logits: ``[B, S, V]`` fp32 softcapped logits over the clean sequence (grad),
            for the co-trained encoder AR loss.
    """
    cap = _model_softcap(model)
    lm_head = model.lm_head

    # 1. Encoder once (grad): encode the clean sequence as context, fill the KV cache.
    encoder_outputs = model.model.encoder(
        input_ids=clean_ids,
        attention_mask=encoder_attention_mask,
    )
    cache = encoder_outputs.past_key_values
    encoder_logits = softcap_logits(lm_head(encoder_outputs.last_hidden_state).float(), cap)

    canvas_ids = window["canvas_ids"]
    decoder_mask = window["decoder_attention_mask"]  # dict -> bypass internal mask build
    decoder_position_ids = window["decoder_position_ids"]

    # 2. Decoder pass-1 (no grad, no self-conditioning): produce the self-cond signal.
    #    Decoder does not write the cache, so pass-2 reuses the same `cache`.
    with torch.no_grad():
        h1 = model.model.decoder(
            decoder_input_ids=canvas_ids,
            past_key_values=cache,
            self_conditioning_logits=None,
            self_conditioning_mask=None,
            decoder_attention_mask=decoder_mask,
            decoder_position_ids=decoder_position_ids,
        )
        sc_logits = softcap_logits(lm_head(h1.last_hidden_state).float(), cap).detach()

    # 3. Decoder pass-2 (grad): self-conditioning gated per-example by the coin.
    h2 = model.model.decoder(
        decoder_input_ids=canvas_ids,
        past_key_values=cache,
        self_conditioning_logits=sc_logits,
        self_conditioning_mask=do_self_conditioning,
        decoder_attention_mask=decoder_mask,
        decoder_position_ids=decoder_position_ids,
    )
    canvas_logits = softcap_logits(lm_head(h2.last_hidden_state).float(), cap)

    return canvas_logits, encoder_logits


def freeze_router(model) -> int:
    """Freeze MoE router/gate params in-place; experts stay trainable. Returns count frozen.

    NOTE: parameter-name patterns are a best guess (DiffusionGemmaTextRouter). Verify the
    actual frozen names against ``model.named_parameters()`` once the model is loaded, and
    tighten ``_ROUTER_PARAM_PATTERNS`` if it over/under-matches (e.g. avoid freezing
    ``gate_proj`` of the dense MLP — that is NOT the router).
    """
    frozen = 0
    for name, param in model.named_parameters():
        # The dense MLP's gate_proj/up_proj/down_proj must NOT be frozen; only the router gate.
        if "gate_proj" in name or "up_proj" in name or "down_proj" in name:
            continue
        if any(pat.search(name) for pat in _ROUTER_PARAM_PATTERNS):
            param.requires_grad_(False)
            frozen += 1
    return frozen
