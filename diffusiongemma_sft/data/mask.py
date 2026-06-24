"""Block-causal training attention mask for DiffusionGemma block diffusion.

Clean re-implementation of NeMo's ``build_block_diffusion_training_mask``
(nemo_automodel/components/models/diffusion_gemma/attention_mask.py:73-220).
This is the highest correctness-risk piece of the SFT path — read the leakage
invariant below before changing anything.

Layout
------
At inference the model runs the shared transformer twice: once *causally* over
the clean prefix to populate a per-layer KV cache (the "encoder" KV), and once
*bidirectionally* over the noised ``canvas`` (the "decoder"). Each decoder layer
concatenates ``[encoder_KV ; canvas_KV]`` along the key axis, so a decoder query
attends over a key axis of length ``S + R`` where ``S = enc_len`` and
``R = response_length``.

For training we run the whole sequence at once and supervise all response
blocks jointly. The encoder holds the **clean** full sequence (prompt + full
response); the canvas holds the **noised** full response. The training mask
therefore has shape ``[B, 1, R, S + R]`` and splits column-wise into:

* **Left columns** ``[0, S)`` — clean encoder KV, ``M_OBC`` (offset-block-causal).
  A canvas query in block ``i`` may attend a clean encoder column only if that
  column belongs to a response block **strictly before** block ``i``. Prompt
  columns (encoder positions ``< prefix_len``, response-relative offset ``< 0``)
  get a sentinel block id ``-1`` and are always visible.
* **Right columns** ``[S, S + R)`` — noised canvas KV, ``M_BD`` (block-diagonal).
  Canvas block ``i`` attends bidirectionally within block ``i`` only, never to
  another canvas block.

Leakage invariant (THE correctness property)
---------------------------------------------
``M_OBC`` uses a **strict** ``block_q > block_kv`` comparison
(attention_mask.py:165). A canvas query in block ``i`` MUST be masked against the
clean encoder column at response-relative position ``i * block_size`` (the first
clean token of its own block) and every later clean position. Using ``>=``
instead of ``>`` is silent **total leakage**: the canvas would see the clean
answer for the very tokens it is being trained to denoise, the loss would
collapse, and the model would learn nothing. ``test_mask.py`` asserts exactly
this boundary (mirrors NeMo test_diffusion_gemma_mask.py:48-104).
"""

from __future__ import annotations

import torch


def _block_ids(num_positions: int, block_size: int, device: torch.device) -> torch.Tensor:
    """Response-relative block index for each of ``num_positions`` positions.

    Mirrors attention_mask.py:68-70.
    """
    return torch.arange(num_positions, device=device) // block_size


def _to_additive(keep: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    """Convert a boolean keep-mask to an additive mask (``0`` / ``-inf``).

    Mirrors attention_mask.py:216-220.
    """
    additive = torch.zeros(keep.shape, dtype=dtype, device=keep.device)
    additive.masked_fill_(~keep, torch.finfo(dtype).min)
    return additive


def build_block_diffusion_training_mask(
    prefix_lengths: torch.Tensor | int,
    response_length: int,
    enc_len: int,
    block_size: int,
    *,
    sliding_window: int | None = None,
    batch_size: int | None = None,
    device: torch.device | str = "cpu",
    dtype: torch.dtype | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Build the block-causal training mask and its sliding-window variant.

    The canvas (decoder query axis) has length ``response_length`` (= ``R``). The
    key axis is ``[encoder_KV (enc_len = S) ; canvas_KV (R)]``, so the returned
    masks have shape ``[B, 1, R, S + R]``.

    Mirrors NeMo attention_mask.py:73-213.

    Args:
        prefix_lengths: Per-example prompt length(s) in the encoder, i.e. the
            number of leading clean encoder positions that are prompt (always
            attendable). An ``int`` is broadcast to all examples; a 1-D tensor of
            shape ``[B]`` gives per-example prefixes. The response occupies
            encoder positions ``[prefix, prefix + response_length)``.
        response_length: Canvas length ``R`` (number of noised response positions).
        enc_len: Total encoder key length ``S`` (prompt + response + any tail
            padding columns). Must satisfy ``enc_len >= max(prefix) + response_length``.
        block_size: Diffusion block size (``canvas_length``; 256 for the ckpt).
        sliding_window: If given, the sliding variant additionally restricts the
            encoder columns to a BLOCK-ANCHORED window ending at the canvas
            block's cache boundary. If ``None`` the sliding variant equals the
            full mask.
        batch_size: Batch dimension. Required when ``prefix_lengths`` is an int;
            inferred from the tensor otherwise.
        device: Device for the returned tensors.
        dtype: If ``None`` (default) return boolean *keep* masks (``True`` =
            attend). If a floating dtype, return an **additive** mask
            (``0`` where attended, ``-inf`` where masked).

    Returns:
        Tuple ``(mask_full, mask_sliding)``:

        * ``mask_full`` — ``M_OBC`` (left cols) ∪ ``M_BD`` (right cols), for the
          5 full-attention layers ``{5, 11, 17, 23, 29}``.
        * ``mask_sliding`` — ``mask_full`` ∩ sliding-window, for the 25 sliding
          layers (``sliding_window = 1024`` for the ckpt).

        Each has shape ``[B, 1, response_length, enc_len + response_length]``.

    Raises:
        ValueError: On a malformed ``prefix_lengths`` shape, a missing
            ``batch_size`` for the int form, negative prefixes, or an ``enc_len``
            too small to hold ``prefix + response_length``.
    """
    device = torch.device(device)

    if isinstance(prefix_lengths, int):
        if batch_size is None:
            raise ValueError("batch_size must be provided when prefix_lengths is an int")
        prefix = torch.full((batch_size,), prefix_lengths, dtype=torch.long, device=device)
    else:
        prefix = prefix_lengths.to(device=device, dtype=torch.long)
        if prefix.ndim != 1:
            raise ValueError(f"prefix_lengths tensor must be 1-D [B], got shape {tuple(prefix.shape)}")
        if batch_size is None:
            batch_size = prefix.shape[0]
        elif batch_size != prefix.shape[0]:
            raise ValueError(f"batch_size {batch_size} != prefix_lengths length {prefix.shape[0]}")

    if (prefix < 0).any():
        raise ValueError("prefix_lengths must be non-negative")
    if (prefix + response_length > enc_len).any():
        raise ValueError(
            f"enc_len ({enc_len}) too small: need prefix + response_length <= enc_len "
            f"(max prefix {int(prefix.max())}, response_length {response_length})"
        )

    canvas_len = response_length  # key axis is [enc_len ; canvas_len]

    # Canvas query block index (response-relative): [Lq]
    q_block = _block_ids(canvas_len, block_size, device)  # [Lq]

    # --- Left columns: clean encoder KV -> M_OBC (offset-block-causal) ---
    enc_pos = torch.arange(enc_len, device=device)  # absolute encoder position
    # Response-relative offset of each encoder column, per example: [B, enc_len].
    # Prompt columns (offset < 0) get a sentinel block id -1 so that any canvas
    # block (block_q >= 0) strictly exceeds them => prompt always visible.
    enc_rel = enc_pos[None, :] - prefix[:, None]  # [B, enc_len]
    enc_block = torch.where(
        enc_rel >= 0,
        enc_rel // block_size,
        torch.full_like(enc_rel, -1),
    )  # [B, enc_len]
    # Columns that are tail padding beyond the response are never attendable.
    enc_is_valid = enc_rel < response_length  # [B, enc_len]

    # M_OBC: STRICT block_q > block_kv. THE leakage invariant lives here
    # (attention_mask.py:165). A non-strict >= would expose the canvas block's
    # own clean answer tokens.
    m_obc = (q_block[None, :, None] > enc_block[:, None, :]) & enc_is_valid[:, None, :]  # [B, Lq, enc_len]

    # --- Right columns: noised canvas KV -> M_BD (block-diagonal) ---
    kv_block = _block_ids(canvas_len, block_size, device)  # [Lkv_canvas]
    m_bd = q_block[:, None] == kv_block[None, :]  # [Lq, canvas_len]
    m_bd = m_bd[None].expand(batch_size, -1, -1)  # [B, Lq, canvas_len]

    keep = torch.cat([m_obc, m_bd], dim=2)  # [B, Lq, key_len]
    keep = keep.unsqueeze(1)  # [B, 1, Lq, key_len]

    # --- Sliding-window variant (attention_mask.py:176-208) ---
    if sliding_window is None:
        keep_sliding = keep.clone()
    else:
        # Block-anchored encoder sliding window. When canvas block b is denoised,
        # the encoder cache holds prompt + response blocks 0..b-1, ending at the
        # absolute boundary ``valid_cache_b = prefix + b*block_size``. A sliding
        # layer keeps the last ``sliding_window`` encoder columns ending at that
        # boundary: ``[valid_cache_b - sliding_window + 1, valid_cache_b)``. This
        # window is CONSTANT for every query in block b (anchored to the block
        # boundary, NOT the query's own position). The upper bound is already
        # imposed by M_OBC; the window only adds the lower bound. Canvas (M_BD)
        # columns get NO sliding band (M_BD already confines them to the block).
        block_start = q_block * block_size  # [Lq] response-relative start of each query's block
        valid_cache = prefix[:, None] + block_start[None, :]  # [B, Lq] abs cache end for the block
        enc_abs = torch.arange(enc_len, device=device)  # [enc_len]
        enc_within = enc_abs[None, None, :] >= (valid_cache[:, :, None] - sliding_window + 1)  # [B, Lq, enc_len]
        canvas_within = torch.ones((batch_size, canvas_len, canvas_len), dtype=torch.bool, device=device)
        within = torch.cat([enc_within, canvas_within], dim=2)  # [B, Lq, key_len]
        keep_sliding = keep & within[:, None]

    if dtype is None:
        return keep, keep_sliding

    return _to_additive(keep, dtype), _to_additive(keep_sliding, dtype)


def build_batched_block_mask(
    *,
    prefix_lengths: torch.Tensor,
    response_lengths: torch.Tensor,
    canvas_len: int,
    enc_len: int,
    block_size: int,
    sliding_window: int | None,
    device: torch.device | str = "cpu",
    dtype: torch.dtype = torch.float32,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Assemble the ``[B, 1, R, S + R]`` additive mask from per-example builds.

    Mirrors NeMo ``_build_batched_block_mask`` (train_ft.py:944-988). Each example
    has its own ``response_length`` (= the row's number of real response tokens);
    the builder is called per example and the result is placed into a padded
    additive mask of common width ``canvas_len`` (= ``R = max response length``).

    Pad query rows (``j >= response_length``) keep their canvas self-diagonal
    unmasked, so the shared transformer never sees an all-``-inf`` softmax row;
    those rows are unsupervised and discarded from the loss.

    Args:
        prefix_lengths: Per-example prompt lengths, shape ``[B]``.
        response_lengths: Per-example real response lengths, shape ``[B]``.
        canvas_len: Common canvas width ``R`` (= ``max(response_lengths)``).
        enc_len: Encoder key length ``S`` (full clean sequence length).
        block_size: Diffusion block size.
        sliding_window: Sliding window size, or ``None`` for full == sliding.
        device: Device for the returned tensors.
        dtype: Floating dtype of the additive masks.

    Returns:
        Tuple ``(mask_full, mask_sliding)``, each ``[B, 1, canvas_len, enc_len + canvas_len]``.
    """
    device = torch.device(device)
    batch_size = int(prefix_lengths.shape[0])
    key_len = enc_len + canvas_len
    neg = torch.finfo(dtype).min
    mask_full = torch.full((batch_size, 1, canvas_len, key_len), neg, dtype=dtype, device=device)
    mask_sliding = torch.full((batch_size, 1, canvas_len, key_len), neg, dtype=dtype, device=device)

    for b in range(batch_size):
        resp = int(response_lengths[b].item())
        if resp > 0:
            full_b, sliding_b = build_block_diffusion_training_mask(
                prefix_lengths=int(prefix_lengths[b].item()),
                response_length=resp,
                enc_len=enc_len,
                block_size=block_size,
                sliding_window=sliding_window,
                batch_size=1,
                device=device,
                dtype=dtype,
            )
            # Encoder columns [0, enc_len) and this example's canvas columns
            # [enc_len, enc_len + resp) map directly; the rest stay masked.
            mask_full[b, 0, :resp, :enc_len] = full_b[0, 0, :, :enc_len]
            mask_full[b, 0, :resp, enc_len : enc_len + resp] = full_b[0, 0, :, enc_len:]
            mask_sliding[b, 0, :resp, :enc_len] = sliding_b[0, 0, :, :enc_len]
            mask_sliding[b, 0, :resp, enc_len : enc_len + resp] = sliding_b[0, 0, :, enc_len:]
        # Every canvas query row attends at least its own canvas position so no
        # softmax row is fully masked (real rows already keep this via M_BD).
        diag = enc_len + torch.arange(canvas_len, device=device)
        rows = torch.arange(canvas_len, device=device)
        mask_full[b, 0, rows, diag] = 0
        mask_sliding[b, 0, rows, diag] = 0
    return mask_full, mask_sliding
