"""End-to-end data/loss pipeline integration (everything except model forward).

Wires the real modules together on real tokenized samples to prove the interfaces
and tensor shapes line up: dataset -> collator -> corruption -> response_window ->
mask -> diffusion/AR loss. Logits are random stand-ins for the model forward; we
only assert shapes/finiteness, not numerical correctness.
"""

import os

import pytest
import torch

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from diffusiongemma_sft.data.collator import CollatorConfig, DLLMCollator, build_response_window
from diffusiongemma_sft.data.corruption import (
    CorruptionConfig,
    corrupt_uniform_random,
    corruption_generator,
)
from diffusiongemma_sft.data.dataset import load_diffusiongemma_tokenizer, tokenize_chat_sample
from diffusiongemma_sft.loss import block_diffusion_loss, encoder_ar_loss

BLOCK = 256
FAKE_VOCAB = 1000  # small stand-in vocab for random logits (targets clamped)


@pytest.fixture(scope="module")
def tokenizer():
    return load_diffusiongemma_tokenizer()


def test_full_data_pipeline(tokenizer):
    # 1. Real tokenized samples (varied response lengths).
    msgs_list = [
        [{"role": "user", "content": "What is 2+2?"},
         {"role": "assistant", "content": "Step by step, 2+2 = 4. " * 12}],
        [{"role": "user", "content": "Name a color."},
         {"role": "assistant", "content": "A nice color is blue. " * 20}],
    ]
    samples = [tokenize_chat_sample(m, tokenizer, max_seq_len=768) for m in msgs_list]

    # 2. Collate (block-aligned padding, response-window mode).
    collator = DLLMCollator(CollatorConfig(
        pad_token_id=tokenizer.pad_token_id or 0,
        eos_token_id=tokenizer.eos_token_id or 1,
        block_size=BLOCK,
        pad_seq_len_divisible=BLOCK,
        max_seq_len=1024,
    ))
    batch = collator(samples)
    B, S = batch["input_ids"].shape
    assert batch["loss_mask"].shape == (B, S)
    assert S % BLOCK == 0, "collator must block-align the sequence length"

    # 3. Corruption (D3PM-uniform).
    gen = corruption_generator(42, step=0, microbatch_idx=0, rank=0)
    noisy, _ = corrupt_uniform_random(
        batch["input_ids"], batch["loss_mask"], CorruptionConfig(), generator=gen
    )
    assert noisy.shape == batch["input_ids"].shape
    # corruption only touches supervised positions
    assert torch.equal(
        noisy[batch["loss_mask"] == 0], batch["input_ids"][batch["loss_mask"] == 0]
    )

    # 4. Response window: carve canvas + build block-causal masks.
    window = build_response_window(
        batch["input_ids"], batch["loss_mask"], batch["attention_mask"], noisy,
        block_size=BLOCK, step=0,
    )
    R = window["canvas_ids"].shape[1]
    assert window["canvas_ids"].shape == (B, R)
    assert window["target_ids"].shape == (B, R)
    assert window["canvas_loss"].shape == (B, R)
    dec_mask = window["decoder_attention_mask"]
    assert "full_attention" in dec_mask and "sliding_attention" in dec_mask
    # block-causal mask covers encoder (S) + canvas (R) keys
    assert dec_mask["full_attention"].shape[-1] == S + R
    # one-canvas-per-step: supervised canvas tokens are a subset of the raw response mask
    assert window["canvas_loss"].sum() <= (window["target_ids"] >= 0).sum()

    # 5. Losses with random stand-in logits (model forward not involved).
    canvas_logits = torch.randn(B, R, FAKE_VOCAB)
    enc_logits = torch.randn(B, S, FAKE_VOCAB)
    target = window["target_ids"].clamp(min=0, max=FAKE_VOCAB - 1)
    clean = batch["input_ids"].clamp(min=0, max=FAKE_VOCAB - 1)

    diff_loss = block_diffusion_loss(canvas_logits, target, window["canvas_loss"])
    ar_loss = encoder_ar_loss(enc_logits, clean, batch["attention_mask"])
    total = diff_loss + 1.0 * ar_loss

    assert torch.isfinite(diff_loss) and diff_loss.item() > 0
    assert torch.isfinite(ar_loss) and ar_loss.item() > 0
    assert torch.isfinite(total)


def test_pipeline_gradients_flow(tokenizer):
    """Loss must be differentiable w.r.t. logits (sanity for backward)."""
    msgs = [[{"role": "user", "content": "Hi"},
             {"role": "assistant", "content": "Hello there. " * 15}]]
    samples = [tokenize_chat_sample(m, tokenizer, max_seq_len=512) for m in msgs]
    collator = DLLMCollator(CollatorConfig(block_size=BLOCK, pad_seq_len_divisible=BLOCK))
    batch = collator(samples)
    gen = corruption_generator(1, step=0, microbatch_idx=0, rank=0)
    noisy, _ = corrupt_uniform_random(batch["input_ids"], batch["loss_mask"], CorruptionConfig(), generator=gen)
    window = build_response_window(
        batch["input_ids"], batch["loss_mask"], batch["attention_mask"], noisy, block_size=BLOCK, step=0
    )
    B, R = window["canvas_ids"].shape
    logits = torch.randn(B, R, FAKE_VOCAB, requires_grad=True)
    target = window["target_ids"].clamp(min=0, max=FAKE_VOCAB - 1)
    loss = block_diffusion_loss(logits, target, window["canvas_loss"])
    loss.backward()
    assert logits.grad is not None and torch.isfinite(logits.grad).all()
