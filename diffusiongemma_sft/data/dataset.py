"""Chat dataset: OpenAI-messages JSONL -> unshifted tokenized samples.

Produces the ``{input_ids, loss_mask, attention_mask}`` format consumed by
``DLLMCollator`` (same-length lists, single supervised run). The supervised
region is the LAST assistant turn; everything before it is context.

Loss-mask construction (the two-pass prefix method):
  - DiffusionGemma's chat template renders an assistant turn as
    ``<|turn>model\\n{content}<turn|>\\n`` (content passes through ``strip_thinking``).
  - ``add_generation_prompt=True`` injects ``<|channel>thought\\n<channel|>`` which
    is NOT present in a fully-rendered assistant turn, so it is NOT a clean prefix.
  - Instead we tokenize ``messages[:-1]`` (context, no generation prompt) and the
    full ``messages``; the context is a clean prefix of the full sequence, and the
    suffix is exactly the supervised assistant turn.

Design note: the supervised span includes the ``<|turn>model\\n`` turn-opener and
the closing ``<turn|>\\n``. For the GSM8K smoke-test this is fine (NeMo's unshifted
mask likewise covers the whole assistant turn). TODO when aligning to the model's
reasoning-channel inference format: GSM8K has no thought/response split, so training
turns differ slightly from the ``<|channel>thought...<channel|>`` generation prompt.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import torch
from torch.utils.data import Dataset


def load_diffusiongemma_tokenizer(model_name: str = "unsloth/diffusiongemma-26B-A4B-it"):
    """Load the tokenizer from the local cache (no model weights needed)."""
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(model_name)


def _apply(tokenizer, messages: list) -> list:
    """Tokenize a message list with the chat template, return raw input_ids."""
    return tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=False,
        return_dict=True,
    )["input_ids"]


def tokenize_chat_sample(
    messages: list,
    tokenizer,
    max_seq_len: int = 1024,
) -> dict:
    """Convert one chat sample to ``{input_ids, loss_mask, attention_mask}``.

    Args:
        messages: OpenAI chat messages; the LAST entry must be the assistant turn.
        tokenizer: A DiffusionGemma chat tokenizer.
        max_seq_len: Right-truncate the sequence to this length.

    Returns:
        Dict of equal-length python lists: ``input_ids`` (int), ``loss_mask``
        (0/1 int, 1 over the final assistant turn), ``attention_mask`` (all 1).

    Raises:
        ValueError: If the last message is not an assistant turn, or the context
            tokenization is not a prefix of the full tokenization.
    """
    if not messages or messages[-1].get("role") != "assistant":
        raise ValueError("tokenize_chat_sample expects the last message to be the assistant turn")

    context = messages[:-1]
    full_ids = _apply(tokenizer, messages)
    ctx_ids = _apply(tokenizer, context) if context else []

    if full_ids[: len(ctx_ids)] != ctx_ids:
        raise ValueError(
            "context tokenization is not a prefix of the full tokenization; "
            "chat-template rendering is inconsistent for this sample"
        )

    loss_mask = [0] * len(ctx_ids) + [1] * (len(full_ids) - len(ctx_ids))

    # Right-truncate to max_seq_len (GSM8K is short; rarely triggers).
    if len(full_ids) > max_seq_len:
        full_ids = full_ids[:max_seq_len]
        loss_mask = loss_mask[:max_seq_len]

    attention_mask = [1] * len(full_ids)
    return {"input_ids": full_ids, "loss_mask": loss_mask, "attention_mask": attention_mask}


@dataclass
class ChatJsonlDataset(Dataset):
    """Lazily tokenizes an OpenAI-messages JSONL into unshifted SFT samples."""

    jsonl_path: str
    tokenizer: object
    max_seq_len: int = 1024

    def __post_init__(self) -> None:
        path = Path(self.jsonl_path)
        if not path.exists():
            raise FileNotFoundError(f"JSONL not found: {path}")
        with path.open(encoding="utf-8") as f:
            self._rows = [json.loads(line)["messages"] for line in f if line.strip()]

    def __len__(self) -> int:
        return len(self._rows)

    def __getitem__(self, idx: int) -> dict:
        return tokenize_chat_sample(self._rows[idx], self.tokenizer, self.max_seq_len)
