"""Leakage / structure tests for the block-causal training mask.

Mirrors NeMo tests/.../test_diffusion_gemma_mask.py. THE gate test is the strict
``block_q > block_kv`` leakage invariant: a canvas block must NOT attend the
clean encoder copy of its own (or later) tokens. A regression to ``>=`` is silent
total leakage and these assertions catch it.

Pure torch / CPU — no GPU, no model forward.
"""

import torch

from diffusiongemma_sft.data.mask import (
    build_batched_block_mask,
    build_block_diffusion_training_mask,
)


def test_output_shape_and_dtype():
    bs, resp, enc, blk = 2, 8, 8, 4
    keep, keep_sliding = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    assert keep.shape == (bs, 1, resp, enc + resp)
    assert keep_sliding.shape == (bs, 1, resp, enc + resp)
    assert keep.dtype == torch.bool
    assert keep_sliding.dtype == torch.bool


# ---------------------------------------------------------------------------
# THE leakage invariant: strict block_q > block_kv at the own-block boundary.
# ---------------------------------------------------------------------------


def test_leakage_block_i_masked_at_encoder_block_start():
    """Block-i canvas query is MASKED at clean encoder position i*block_size.

    prefix=0 => encoder holds the clean response only, so encoder position p has
    response-relative offset p. Canvas block i covers [i*blk, (i+1)*blk). The
    first clean position of block i is encoder column i*blk; the strict-> boundary
    masks it (and everything after) — that is the answer it is denoising.
    """
    bs, blk = 1, 4
    resp = enc = 16  # 4 blocks of size 4, encoder == clean response
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    num_blocks = resp // blk
    for i in range(num_blocks):
        q = i * blk  # a query inside block i (its first position)
        # MASKED: own-block start and every later clean encoder column.
        for p in range(i * blk, enc):
            assert not keep[0, 0, q, p], (
                f"LEAKAGE: block {i} query attends clean encoder pos {p} (>= own block start)"
            )
        # VISIBLE: all strictly-earlier clean encoder columns.
        for p in range(0, i * blk):
            assert keep[0, 0, q, p], f"block {i} query should attend earlier clean encoder pos {p}"


def test_strict_boundary_differs_from_non_strict():
    """A buggy ``>=`` mask would additionally expose the own block; ours must not.

    This is the test that would FAIL if the implementation used ``>=`` instead of
    the strict ``>``: ``strict & own_block`` must be empty.
    """
    bs, blk = 1, 4
    resp = enc = 12
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    q_block = torch.arange(resp) // blk
    enc_block = torch.arange(enc) // blk
    leaky = q_block[:, None] >= enc_block[None, :]  # the BUG (>=)
    strict = keep[0, 0, :, :enc]
    own_block = q_block[:, None] == enc_block[None, :]
    assert (leaky & own_block).any(), "test setup: leaky mask should expose own block"
    assert not (strict & own_block).any(), "LEAKAGE: strict mask exposes own clean block"


def test_every_query_in_block_sees_same_encoder_blocks():
    """All queries in block i share the same offset-block-causal encoder visibility."""
    bs, blk = 1, 4
    resp = enc = 16
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    for i in range(resp // blk):
        rows = [keep[0, 0, i * blk + j, :enc] for j in range(blk)]
        for r in rows[1:]:
            assert torch.equal(rows[0], r)


# ---------------------------------------------------------------------------
# Block-diagonal canvas (M_BD): block i never attends canvas block j != i.
# ---------------------------------------------------------------------------


def test_canvas_block_diagonal():
    bs, blk = 1, 4
    resp = enc = 16
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    canvas = keep[0, 0, :, enc:]  # [Lq, canvas_len]
    q_block = torch.arange(resp) // blk
    kv_block = torch.arange(resp) // blk
    same_block = q_block[:, None] == kv_block[None, :]
    assert canvas[same_block].all(), "canvas should attend bidirectionally within its own block"
    assert not canvas[~same_block].any(), "canvas block i must not attend canvas block j != i"


# ---------------------------------------------------------------------------
# Prompt prefix always visible; tail padding never visible.
# ---------------------------------------------------------------------------


def test_prompt_prefix_always_visible():
    bs, blk, prefix = 1, 4, 5
    resp = 8
    enc = prefix + resp
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=prefix, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    assert keep[0, 0, :, :prefix].all(), "all prompt columns must be visible to every canvas block"


def test_tail_padding_never_visible():
    bs, blk, prefix = 1, 4, 0
    resp = 8
    enc = resp + 6  # 6 extra padding columns
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=prefix, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    pad = keep[0, 0, :, prefix + resp : enc]
    assert not pad.any(), "tail padding encoder columns must never be attended"


def test_per_example_prefix_lengths():
    """A 1-D prefix tensor offsets the response start per example."""
    blk, resp = 4, 8
    prefixes = torch.tensor([0, 4])
    enc = int(prefixes.max()) + resp
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=prefixes, response_length=resp, enc_len=enc, block_size=blk
    )
    assert not keep[0, 0, 0, 0]  # example 0: prefix 0 -> block-0 masked at col 0
    assert keep[1, 0, 0, 3], "example-1 prompt column should be visible"
    assert not keep[1, 0, 0, 4], "example-1 own-block clean start should be masked"


def test_single_block_masks_entire_encoder():
    """block_size == response_length => one block => entire encoder masked."""
    bs = 1
    resp = enc = 8
    keep, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=resp, batch_size=bs
    )
    assert not keep[0, 0, :, :enc].any(), "single block: no strictly-earlier clean column exists"
    assert keep[0, 0, :, enc:].all(), "single block canvas should be fully bidirectional"


# ---------------------------------------------------------------------------
# Sliding variant respects the window and is a subset of the full mask.
# ---------------------------------------------------------------------------


def test_sliding_is_subset_of_full():
    bs, blk = 1, 4
    resp = enc = 32
    keep, keep_sliding = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs, sliding_window=8
    )
    assert (keep | ~keep_sliding).all(), "sliding mask must be a subset of the full mask"


def test_sliding_window_block_anchored():
    """Encoder sliding window is BLOCK-ANCHORED (constant per block, not per query)."""
    bs, blk, window = 1, 4, 8
    resp = enc = 32
    _, keep_sliding = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs, sliding_window=window
    )
    enc_part = keep_sliding[0, 0, :, :enc]
    for j in range(resp):
        valid_cache = (j // blk) * blk  # prefix=0; cache end at the query's block boundary
        lo = valid_cache - window + 1
        for k in enc_part[j].nonzero().flatten().tolist():
            assert lo <= k < valid_cache, (
                f"query {j} (block {j // blk}) kept encoder col {k} outside window [{lo}, {valid_cache})"
            )
    for b in range(resp // blk):
        rows = enc_part[b * blk : (b + 1) * blk]
        assert (rows == rows[0]).all(), f"block {b}: encoder window varies across its queries"


def test_sliding_keeps_prompt_for_early_block():
    """Block 0's short cache (< window) => no lower bound => prompt survives."""
    bs, blk, window = 1, 4, 16
    prefix, resp = 6, 16
    seq = prefix + resp
    full, sliding = build_block_diffusion_training_mask(
        prefix_lengths=prefix, response_length=resp, enc_len=seq, block_size=blk, batch_size=bs, sliding_window=window
    )
    f, s = full[0, 0], sliding[0, 0]
    block0, prompt = slice(0, blk), slice(0, prefix)
    assert f[block0, prompt].any(), "setup: prompt should be visible to block 0 in the full mask"
    assert torch.equal(f[block0, prompt], s[block0, prompt]), (
        "block-anchored sliding removed block-0's prompt visibility"
    )


def test_sliding_none_equals_full():
    bs, blk = 1, 4
    resp = enc = 16
    keep, keep_sliding = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs, sliding_window=None
    )
    assert torch.equal(keep, keep_sliding)


# ---------------------------------------------------------------------------
# Additive-mask variant.
# ---------------------------------------------------------------------------


def test_additive_mask_values():
    bs, blk = 1, 4
    resp = enc = 8
    keep_bool, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs
    )
    add_full, _ = build_block_diffusion_training_mask(
        prefix_lengths=0, response_length=resp, enc_len=enc, block_size=blk, batch_size=bs, dtype=torch.float32
    )
    assert add_full.dtype == torch.float32
    assert (add_full[keep_bool] == 0).all()
    assert (add_full[~keep_bool] == torch.finfo(torch.float32).min).all()


# ---------------------------------------------------------------------------
# Batched assembly: per-example response lengths + pad-row self-diagonal.
# ---------------------------------------------------------------------------


def test_batched_block_mask_pad_row_keeps_self_diagonal():
    """A degenerate / shorter row keeps each canvas query's self-diagonal so the
    softmax row is never all -inf (train_ft.py:983-987)."""
    blk = 4
    enc_len = 12
    prefix_lengths = torch.tensor([0, 2])
    response_lengths = torch.tensor([8, 4])  # row 0 longer
    canvas_len = int(response_lengths.max())  # R = 8
    mask_full, mask_sliding = build_batched_block_mask(
        prefix_lengths=prefix_lengths,
        response_lengths=response_lengths,
        canvas_len=canvas_len,
        enc_len=enc_len,
        block_size=blk,
        sliding_window=None,
        dtype=torch.float32,
    )
    assert mask_full.shape == (2, 1, canvas_len, enc_len + canvas_len)
    # Every query row of every example attends at least one key (no all -inf row).
    finite = mask_full > torch.finfo(torch.float32).min
    assert finite.any(dim=-1).all(), "some softmax row is fully masked (-inf)"
    # Pad rows of row 1 (j >= 4): self-diagonal at canvas col j must be attended.
    for j in range(4, canvas_len):
        assert mask_full[1, 0, j, enc_len + j] == 0, f"pad row {j} lost its self-diagonal"


def test_batched_block_mask_leakage_per_example():
    """Per-example block-causal: row's block-i query masked at its own clean block start."""
    blk = 4
    enc_len = 16
    prefix_lengths = torch.tensor([0, 4])
    response_lengths = torch.tensor([12, 8])
    canvas_len = int(response_lengths.max())
    mask_full, _ = build_batched_block_mask(
        prefix_lengths=prefix_lengths,
        response_lengths=response_lengths,
        canvas_len=canvas_len,
        enc_len=enc_len,
        block_size=blk,
        sliding_window=None,
        dtype=torch.float32,
    )
    neg = torch.finfo(torch.float32).min
    # Example 1: prefix 4, block 0 query (canvas row 0) masked at its own clean
    # encoder block start (abs col 4) but sees the prompt col 3.
    assert mask_full[1, 0, 0, 3] == 0, "example-1 prompt column should be visible"
    assert mask_full[1, 0, 0, 4] == neg, "example-1 own clean block start must be masked"
