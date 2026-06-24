"""Unit tests for DLLMCollator and build_response_window (model-independent)."""

import math

import pytest
import torch

from diffusiongemma_sft.data.collator import (
    CollatorConfig,
    DLLMCollator,
    build_response_window,
)


def _sample(prompt_len: int, resp_len: int, pad_id: int = 0, tok_start: int = 100):
    """Build one unshifted sample: [prompt tokens (loss=0)][response tokens (loss=1)].

    All real tokens are attended (attention_mask=1). Token ids are distinct so we
    can check exact slicing.
    """
    n = prompt_len + resp_len
    input_ids = list(range(tok_start, tok_start + n))
    loss_mask = [0] * prompt_len + [1] * resp_len
    attention_mask = [1] * n
    return {"input_ids": input_ids, "loss_mask": loss_mask, "attention_mask": attention_mask}


# ---------------------------------------------------------------------------
# DLLMCollator: two-stage block-aligned padding.
# ---------------------------------------------------------------------------


def test_collator_block_fill_and_global_pad():
    """[real][EOS-fill loss=1 attended][global pad loss=0 not attended]."""
    bs = 4
    cfg = CollatorConfig(pad_token_id=0, eos_token_id=1, block_size=bs, pad_seq_len_divisible=bs)
    collator = DLLMCollator(cfg)
    # Sample A: prompt 2, resp 3 -> resp rounds 3->4, fill_end = 2+4 = 6.
    # Sample B: prompt 1, resp 5 -> resp rounds 5->8, fill_end = 1+8 = 9.
    a = _sample(2, 3, tok_start=100)
    b = _sample(1, 5, tok_start=200)
    out = collator([a, b])

    # target_len = max(fill_end) rounded to lcm(4,4)=4 => max(6,9)=9 -> 12.
    assert out["input_ids"].shape == (2, 12)

    # Sample A: content [0,5), EOS-fill [5,6), global pad [6,12).
    ids_a = out["input_ids"][0]
    assert ids_a[:5].tolist() == list(range(100, 105)), "content preserved"
    assert ids_a[5].item() == 1, "EOS block-fill token"
    assert ids_a[6:].eq(0).all(), "global pad = pad_token_id"

    lm_a = out["loss_mask"][0]
    assert lm_a[:2].eq(0).all(), "prompt loss=0"
    assert lm_a[2:6].eq(1).all(), "response + EOS-fill loss=1"
    assert lm_a[6:].eq(0).all(), "global pad loss=0"

    am_a = out["attention_mask"][0]
    assert am_a[:6].eq(1).all(), "content + EOS-fill attended"
    assert am_a[6:].eq(0).all(), "global pad not attended"


def test_collator_fill_end_is_block_aligned_response_relative():
    """fill_end - prefix is a whole number of blocks (response-relative)."""
    bs = 4
    cfg = CollatorConfig(block_size=bs, pad_seq_len_divisible=bs)
    collator = DLLMCollator(cfg)
    s = _sample(prompt_len=3, resp_len=2)  # resp 2 -> 4; fill_end = 3+4 = 7
    out = collator([s])
    lm = out["loss_mask"][0]
    # supervised span = response (2) + EOS fill (2) = 4 = one block.
    assert int(lm.sum().item()) == 4
    # supervised region is [3, 7).
    sup_idx = lm.nonzero().flatten().tolist()
    assert sup_idx == [3, 4, 5, 6]
    assert (len(sup_idx)) % bs == 0


def test_collator_rejects_multi_turn():
    """A loss_mask with >1 supervised run raises (single-turn guard)."""
    cfg = CollatorConfig(block_size=4, pad_seq_len_divisible=4)
    collator = DLLMCollator(cfg)
    multi = {
        "input_ids": list(range(8)),
        "loss_mask": [0, 1, 1, 0, 0, 1, 1, 0],  # two runs
        "attention_mask": [1] * 8,
    }
    with pytest.raises(AssertionError, match="supervised runs"):
        collator([multi])


def test_collator_target_len_lcm_alignment():
    """target_len rounds to lcm(block_size, pad_seq_len_divisible)."""
    cfg = CollatorConfig(block_size=4, pad_seq_len_divisible=6)  # lcm = 12
    collator = DLLMCollator(cfg)
    s = _sample(prompt_len=1, resp_len=1)  # resp 1 -> 4, fill_end = 5 -> round to 12
    out = collator([s])
    assert out["input_ids"].shape[1] == math.lcm(4, 6)


# ---------------------------------------------------------------------------
# build_response_window: canvas slicing, width, block alignment, one-canvas.
# ---------------------------------------------------------------------------


def _collated_batch(prompt_resp_pairs, block_size=4):
    cfg = CollatorConfig(pad_token_id=0, eos_token_id=1, block_size=block_size, pad_seq_len_divisible=block_size)
    collator = DLLMCollator(cfg)
    samples = [_sample(p, r, tok_start=1000 + 1000 * i) for i, (p, r) in enumerate(prompt_resp_pairs)]
    return collator(samples), cfg


def test_response_window_slices_prompt_and_answer():
    """canvas/target gather the response region; prompt stays in the encoder."""
    block_size = 4
    batch, cfg = _collated_batch([(2, 3), (1, 5)], block_size=block_size)
    clean = batch["input_ids"]
    # No corruption here: noisy == clean so target == canvas, easy to check slicing.
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
        block_size=block_size, step=0,
    )
    # prefix_lengths = first supervised index = prompt length.
    assert win["prefix_lengths"].tolist() == [2, 1]
    # response_lengths = effective_len - prefix. Effective len = attended count.
    #   A: resp 3 rounds to 4, fill_end=2+4=6. content 5 + EOS-fill 1 = 6 attended,
    #      prefix 2 -> resp 4.
    #   B: resp 5 rounds to 8, fill_end=1+8=9. content 6 + EOS-fill 3 = 9 attended,
    #      prefix 1 -> resp 8.
    assert win["response_lengths"].tolist() == [4, 8]
    R = win["R"]
    assert R == 8, "canvas width = max response length"
    assert win["target_ids"].shape == (2, R)

    # Sample A target row [0:4) = clean response tokens (encoder positions 2..5).
    assert win["target_ids"][0, :4].tolist() == clean[0, 2:6].tolist()
    # Sample B target row [0:8) = clean response tokens (encoder positions 1..8).
    assert win["target_ids"][1, :8].tolist() == clean[1, 1:9].tolist()


def test_response_window_canvas_width_equals_longest_response():
    block_size = 4
    batch, _ = _collated_batch([(3, 2), (0, 9)], block_size=block_size)
    clean = batch["input_ids"]
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
        block_size=block_size, step=0,
    )
    R = win["R"]
    assert R == int(win["response_lengths"].max().item())
    assert win["canvas_ids"].shape[1] == R


def test_response_window_pad_rows_dropped_from_loss():
    """Shorter responses are right-padded; pad canvas positions are unsupervised."""
    block_size = 4
    batch, _ = _collated_batch([(2, 3), (1, 5)], block_size=block_size)
    clean = batch["input_ids"]
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
        block_size=block_size, step=0,
    )
    R = win["R"]
    resp = win["response_lengths"]
    # decoder_padding_mask True beyond each row's response length.
    pad = win["decoder_padding_mask"]
    for b in range(2):
        assert not pad[b, : resp[b]].any(), "real response positions are not pad"
        assert pad[b, resp[b] : R].all(), "positions beyond response are pad"
    # canvas_loss never set on a pad position.
    assert not (win["canvas_loss"] & pad).any()


def test_response_window_one_canvas_per_step_single_block():
    """canvas_loss keeps exactly ONE block's supervised tokens per row.

    Use a row whose response spans multiple blocks; assert the surviving
    supervised positions all share a single block id.
    """
    block_size = 4
    # prompt 0, resp 12 -> 3 blocks of supervised tokens.
    batch, _ = _collated_batch([(0, 12)], block_size=block_size)
    clean = batch["input_ids"]
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
        block_size=block_size, step=0,
    )
    R = win["R"]
    canvas_loss = win["canvas_loss"][0]  # [R]
    offsets = torch.arange(R)
    block_id = offsets // block_size
    sel_blocks = block_id[canvas_loss].unique()
    assert sel_blocks.numel() == 1, f"one-canvas-per-step kept blocks {sel_blocks.tolist()}, expected 1"
    # Within the selected block, all supervised (valid, non-pad) positions kept.
    sel = int(sel_blocks.item())
    in_block = block_id == sel
    valid = ~win["decoder_padding_mask"][0]
    expected = in_block & valid
    assert torch.equal(canvas_loss, expected), "selected block should keep ALL its supervised tokens"


def test_response_window_one_canvas_reproducible_and_step_varies():
    """Same (step, mb, seed) -> same block selection; different step can differ."""
    block_size = 4
    batch, _ = _collated_batch([(0, 16)], block_size=block_size)  # 4 blocks, room to differ
    clean = batch["input_ids"]

    def sel_block(step):
        win = build_response_window(
            clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
            block_size=block_size, step=step, microbatch_idx=0, base_seed=42,
        )
        cl = win["canvas_loss"][0]
        offsets = torch.arange(win["R"])
        return (offsets // block_size)[cl].unique()

    s0a = sel_block(0)
    s0b = sel_block(0)
    assert torch.equal(s0a, s0b), "selection must be reproducible for the same seed/step"
    # Scan a few steps; at least one should pick a different block (4 blocks available).
    blocks = {int(sel_block(s).item()) for s in range(8)}
    assert len(blocks) > 1, "block selection should vary across steps"


def test_response_window_decoder_position_ids_are_absolute():
    """Decoder position ids are the response tokens' absolute positions (RoPE align)."""
    block_size = 4
    batch, _ = _collated_batch([(3, 5)], block_size=block_size)
    clean = batch["input_ids"]
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
        block_size=block_size, step=0,
    )
    resp = int(win["response_lengths"][0].item())
    pos = win["decoder_position_ids"][0, :resp]
    # absolute positions = prefix + [0..resp): prefix=3 -> [3,4,5,6,7].
    assert pos.tolist() == [3 + j for j in range(resp)]


def test_response_window_mask_shapes():
    block_size = 4
    batch, _ = _collated_batch([(2, 3), (1, 5)], block_size=block_size)
    clean = batch["input_ids"]
    S = clean.shape[1]
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], clean.clone(),
        block_size=block_size, step=0,
    )
    R = win["R"]
    full = win["decoder_attention_mask"]["full_attention"]
    sliding = win["decoder_attention_mask"]["sliding_attention"]
    assert full.shape == (2, 1, R, S + R)
    assert sliding.shape == (2, 1, R, S + R)


def test_response_window_corruption_keeps_target_clean():
    """canvas_ids come from noisy; target_ids come from clean (different where corrupted)."""
    block_size = 4
    batch, _ = _collated_batch([(0, 8)], block_size=block_size)
    clean = batch["input_ids"]
    noisy = clean.clone()
    noisy[0, 2] = 999  # corrupt one response token in the encoder-space
    win = build_response_window(
        clean, batch["loss_mask"], batch["attention_mask"], noisy,
        block_size=block_size, step=0,
    )
    # canvas position 2 (prefix 0) reflects noisy; target reflects clean.
    assert win["canvas_ids"][0, 2].item() == 999
    assert win["target_ids"][0, 2].item() == clean[0, 2].item()
