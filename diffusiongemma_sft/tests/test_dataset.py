"""Tests for the chat dataset / loss-mask construction (uses the real tokenizer)."""

import os

import pytest

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from diffusiongemma_sft.data.dataset import (
    load_diffusiongemma_tokenizer,
    tokenize_chat_sample,
)


@pytest.fixture(scope="module")
def tokenizer():
    return load_diffusiongemma_tokenizer()


def test_loss_mask_single_run_over_assistant(tokenizer):
    msgs = [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "It is 4."},
    ]
    s = tokenize_chat_sample(msgs, tokenizer)
    ids, lm, am = s["input_ids"], s["loss_mask"], s["attention_mask"]
    assert len(ids) == len(lm) == len(am)
    # exactly one contiguous supervised run (DLLMCollator requires this)
    runs = sum(1 for i, v in enumerate(lm) if v and (i == 0 or not lm[i - 1]))
    assert runs == 1, f"expected 1 supervised run, got {runs}"
    # prompt region is unsupervised, assistant region supervised
    assert lm[0] == 0 and lm[-1] == 1
    # attention all ones (padding happens later in the collator)
    assert all(v == 1 for v in am)


def test_supervised_span_decodes_to_assistant(tokenizer):
    msgs = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there friend"},
    ]
    s = tokenize_chat_sample(msgs, tokenizer)
    ids, lm = s["input_ids"], s["loss_mask"]
    sup_ids = [t for t, m in zip(ids, lm) if m == 1]
    decoded = tokenizer.decode(sup_ids)
    assert "Hi there friend" in decoded, f"assistant content missing from supervised span: {decoded!r}"


def test_prompt_region_excludes_assistant_content(tokenizer):
    msgs = [
        {"role": "user", "content": "Name a color"},
        {"role": "assistant", "content": "Magenta"},
    ]
    s = tokenize_chat_sample(msgs, tokenizer)
    ids, lm = s["input_ids"], s["loss_mask"]
    prompt_ids = [t for t, m in zip(ids, lm) if m == 0]
    decoded = tokenizer.decode(prompt_ids)
    assert "Magenta" not in decoded, "assistant content leaked into the unsupervised prompt region"
    assert "Name a color" in decoded


def test_truncation_respects_max_seq_len(tokenizer):
    msgs = [
        {"role": "user", "content": "word " * 500},
        {"role": "assistant", "content": "answer " * 500},
    ]
    s = tokenize_chat_sample(msgs, tokenizer, max_seq_len=128)
    assert len(s["input_ids"]) == 128
    assert len(s["loss_mask"]) == 128
    assert len(s["attention_mask"]) == 128


def test_rejects_non_assistant_last(tokenizer):
    with pytest.raises(ValueError):
        tokenize_chat_sample(
            [{"role": "user", "content": "hi"}], tokenizer
        )
