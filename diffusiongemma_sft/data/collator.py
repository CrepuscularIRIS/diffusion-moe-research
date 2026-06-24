"""Collator + response-window slicer for DiffusionGemma block-diffusion SFT.

Two model-independent pieces (pure tensor logic, no model weights):

1. ``DLLMCollator`` (``response_window=True`` mode) — clean re-implementation of
   NeMo's ``DLLMCollator`` (nemo_automodel/components/datasets/dllm/collate.py:35-246).
   Takes a list of unshifted samples ``{input_ids, loss_mask, attention_mask}``
   and produces block-aligned batch tensors with the two-stage padding layout::

       [real tokens][EOS block-pad, loss=1, attended][PAD global-pad, loss=0, not attended]

   The EOS block-fill rounds the RESPONSE length (measured from the first
   supervised position) up to a ``block_size`` multiple, so the canvas grid is a
   whole number of blocks. The EOS-fill is supervised (loss=1) and attended
   (attention=1): the model must learn to emit EOS to terminate a block.

2. ``build_response_window`` — clean re-implementation of NeMo's
   ``_build_response_window`` (recipes/dllm/train_ft.py:830-942). Slices the
   noised batch to the response region, building canvas / target / loss tensors
   ``[B, R]`` (``R = max response length``), block-causal masks, and decoder
   position ids. Applies one-canvas-per-step block selection
   (train_ft.py:895-912).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional

import torch

from diffusiongemma_sft.data.mask import build_batched_block_mask


@dataclass(frozen=True)
class CollatorConfig:
    """Immutable config for ``DLLMCollator`` in response-window mode.

    Defaults match the DiffusionGemma SFT recipe (block_size=256, EOS-fill
    aligned to ``lcm(block_size, pad_seq_len_divisible) = 256``).
    """

    pad_token_id: int = 0
    eos_token_id: int = 1
    block_size: int = 256
    pad_seq_len_divisible: int = 256
    max_seq_len: Optional[int] = None


def _first_supervised_index(loss_mask: list, default: int) -> int:
    """First index where ``loss_mask`` is truthy (the response start), else
    ``default`` (no supervised token -> treat the whole sample as prefix).

    Mirrors collate.py:171-178.
    """
    for i, v in enumerate(loss_mask):
        if v:
            return i
    return default


def _count_supervised_runs(loss_mask: list) -> int:
    """Number of contiguous supervised runs in a raw ``loss_mask`` (collate.py:103)."""
    return sum(1 for i, v in enumerate(loss_mask) if v and (i == 0 or not loss_mask[i - 1]))


class DLLMCollator:
    """Collator for DiffusionGemma block-diffusion SFT (response-window mode).

    Goes directly from variable-length sample dicts to block-aligned tensors in a
    single pass. Each sample must carry ``input_ids``, ``loss_mask`` and
    ``attention_mask`` (the unshifted format produced upstream by the dataset).

    Mirrors NeMo collate.py:35-246 with ``response_window=True``,
    ``supervise_padding=False``.
    """

    def __init__(self, config: CollatorConfig) -> None:
        self.config = config

    def __call__(self, batch: List[Dict[str, list]]) -> Dict[str, torch.Tensor]:
        """Collate a list of samples into block-aligned batch tensors.

        Args:
            batch: List of dicts, each with list-valued ``input_ids``,
                ``loss_mask`` and ``attention_mask`` of the same per-sample length.

        Returns:
            Dict with ``input_ids`` ``[B, T]`` (long), ``loss_mask`` ``[B, T]``
            (float), ``attention_mask`` ``[B, T]`` (long), ``input_lengths``
            ``[B]`` (long). ``T`` is the block-aligned target length.

        Raises:
            ValueError: On an empty batch or a sample missing required keys /
                mismatched field lengths.
            AssertionError: On a multi-turn ``loss_mask`` (>1 supervised run) —
                the response window needs a single contiguous response.
        """
        cfg = self.config
        if not batch:
            raise ValueError("DLLMCollator received an empty batch")
        for s in batch:
            for key in ("input_ids", "loss_mask", "attention_mask"):
                if key not in s:
                    raise ValueError(f"sample missing required key {key!r}")
            n = len(s["input_ids"])
            if len(s["loss_mask"]) != n or len(s["attention_mask"]) != n:
                raise ValueError("input_ids / loss_mask / attention_mask length mismatch in sample")

        content_lengths = torch.tensor([len(s["input_ids"]) for s in batch], dtype=torch.long)

        # Single-turn guard (EVERY batch, collate.py:101-109): the response window
        # needs the supervised response to be ONE contiguous run in the RAW
        # loss_mask. A multi-turn mask would mis-window an intervening user turn
        # into the response canvas. Use mask_history=True upstream to collapse.
        for s in batch:
            runs = _count_supervised_runs(s["loss_mask"])
            if runs > 1:
                raise AssertionError(
                    f"DLLMCollator: loss_mask has {runs} supervised runs (multi-turn); the "
                    "block-diffusion response window needs a single contiguous response. "
                    "Set mask_history=True on the dataset to supervise only the final turn."
                )

        # Response start per sample = first supervised position (collate.py:117-120).
        prefix_lengths = torch.tensor(
            [_first_supervised_index(s["loss_mask"], len(s["input_ids"])) for s in batch],
            dtype=torch.long,
        )

        fill_ends = self._block_fill_ends(content_lengths, prefix_lengths)
        target_len = self._compute_target_length(fill_ends)

        input_ids = self._pad_and_fill(
            [s["input_ids"] for s in batch],
            content_lengths,
            fill_ends,
            target_len,
            pad_value=cfg.pad_token_id,
            block_pad_value=cfg.eos_token_id,
        )
        loss_mask = self._pad_and_fill(
            [s["loss_mask"] for s in batch],
            content_lengths,
            fill_ends,
            target_len,
            pad_value=0,
            block_pad_value=1,  # EOS block-fill IS supervised (collate.py:140-148)
        ).float()
        attention_mask = self._pad_and_fill(
            [s["attention_mask"] for s in batch],
            content_lengths,
            fill_ends,
            target_len,
            pad_value=0,
            block_pad_value=1,  # EOS block-fill IS attended (collate.py:121-122,155-162)
        )

        return {
            "input_ids": input_ids,
            "loss_mask": loss_mask,
            "attention_mask": attention_mask,
            "input_lengths": content_lengths,
        }

    def _block_fill_ends(self, content_lengths: torch.Tensor, prefix_lengths: torch.Tensor) -> torch.Tensor:
        """Per-sample end of the EOS block-fill, RESPONSE-RELATIVE (collate.py:180-197).

        The fill rounds the response length (from ``prefix``, the response start)
        up to a ``block_size`` multiple, so ``fill_end - prefix`` is a whole
        number of canvas blocks.
        """
        cfg = self.config
        cl = content_lengths
        if cfg.max_seq_len is not None:
            cl = cl.clamp(max=cfg.max_seq_len)
        bs = cfg.block_size
        if bs is None or bs <= 1:
            return cl.clone()
        prefix = prefix_lengths.clamp(max=cl)
        resp = (cl - prefix).clamp(min=0)
        resp_blocks = ((resp + bs - 1) // bs) * bs
        return prefix + resp_blocks

    def _compute_target_length(self, fill_ends: torch.Tensor) -> int:
        """Batch target length: max fill_end rounded to ``lcm(block_size, psd)``,
        capped at ``max_seq_len`` (collate.py:199-212)."""
        cfg = self.config
        max_len = int(fill_ends.max().item()) if fill_ends.numel() else 0

        psd = cfg.pad_seq_len_divisible
        bs = cfg.block_size
        if psd is not None and psd > 1:
            alignment = math.lcm(bs or 1, psd)
            max_len = ((max_len + alignment - 1) // alignment) * alignment

        if cfg.max_seq_len is not None:
            max_len = min(max_len, cfg.max_seq_len)

        return max(max_len, 1)

    @staticmethod
    def _pad_and_fill(
        samples: List[list],
        content_lengths: torch.Tensor,
        fill_ends: torch.Tensor,
        target_len: int,
        pad_value: int,
        block_pad_value: int,
        dtype: torch.dtype = torch.long,
    ) -> torch.Tensor:
        """Pad variable-length lists to ``target_len`` with two-stage fill
        (collate.py:214-245).

        For each sample:
          - ``[0, content_length)``        -> original content
          - ``[content_length, fill_end)`` -> ``block_pad_value`` (EOS block-fill)
          - ``[fill_end, target_len)``     -> ``pad_value`` (stage-2 global pad)
        """
        b = len(samples)
        out = torch.full((b, target_len), pad_value, dtype=dtype)

        for i in range(b):
            cl = int(content_lengths[i].item())
            seq = samples[i]
            copy_len = min(cl, target_len, len(seq))
            out[i, :copy_len] = torch.tensor(seq[:copy_len], dtype=dtype)

            fe = min(int(fill_ends[i].item()), target_len)
            if fe > cl:
                out[i, cl:fe] = block_pad_value

        return out


def _split_prompt_response(loss_mask: torch.Tensor, seq_len: int) -> torch.Tensor:
    """Per-row prefix length = first supervised index (strategy.py:841-863).

    Rows with no supervised token are treated as all-prompt (prefix = seq_len).

    Args:
        loss_mask: Supervised mask, shape ``[B, S]``; bool or {0,1} float.
        seq_len: Sequence length ``S`` (fallback prefix for unsupervised rows).

    Returns:
        ``prefix_lengths`` of shape ``[B]`` (long).
    """
    lm = loss_mask.bool()
    has_sup = lm.any(dim=1)
    first_sup = torch.argmax(lm.int(), dim=1)  # first True index; 0 if none
    return torch.where(has_sup, first_sup, torch.full_like(first_sup, seq_len))


def build_response_window(
    input_ids: torch.Tensor,
    loss_mask: torch.Tensor,
    attention_mask: torch.Tensor,
    noisy: torch.Tensor,
    block_size: int,
    *,
    step: int,
    microbatch_idx: int = 0,
    base_seed: int = 42,
    sliding_window: Optional[int] = 1024,
    mask_dtype: torch.dtype = torch.float32,
) -> Dict[str, torch.Tensor]:
    """Slice the noised batch to the response window and build the block masks.

    Clean re-implementation of NeMo ``_build_response_window`` (train_ft.py:830-942)
    plus one-canvas-per-step block selection (train_ft.py:895-912). Pure tensor
    logic — no model.

    The encoder consumes the CLEAN full sequence ``input_ids [B, S]``; the decoder
    canvas is the noised response region, gathered to width ``R = max response
    length``. Shorter responses are right-padded and their pad positions dropped
    from the (sliced) loss / noise masks.

    Args:
        input_ids: Clean token ids, shape ``[B, S]``.
        loss_mask: Supervised mask over the full sequence, ``[B, S]`` (bool/float).
        attention_mask: Non-pad mask over the full sequence, ``[B, S]`` (bool/{0,1}).
        noisy: Corrupted token ids (from ``corrupt_uniform_random``), ``[B, S]``.
        block_size: Diffusion block size (256 for the ckpt).
        step: Global training step (seeds the one-canvas block selection).
        microbatch_idx: Grad-accumulation microbatch index (per-mb independent draw).
        base_seed: Base seed; the selection stream uses
            ``base_seed + 7919*step + microbatch_idx + (1 << 42)`` to decorrelate
            from the corruption (``2 << 42``) and self-cond (``+0``) streams.
        sliding_window: Sliding-window size for the sliding mask variant; ``None``
            makes the sliding mask equal the full mask.
        mask_dtype: Floating dtype of the additive attention masks.

    Returns:
        Dict with:
          - ``canvas_ids`` ``[B, R]`` — noised response tokens (decoder input).
          - ``target_ids`` ``[B, R]`` — clean response tokens (CE targets).
          - ``canvas_loss`` ``[B, R]`` bool — supervised AND valid AND in the
            step-selected block (the diffusion loss support).
          - ``decoder_position_ids`` ``[B, R]`` — absolute positions (RoPE align).
          - ``decoder_padding_mask`` ``[B, R]`` bool — True on pad canvas rows.
          - ``encoder_padding_mask`` ``[B, S]`` bool — True on pad encoder cols.
          - ``decoder_attention_mask`` — dict with ``full_attention`` and
            ``sliding_attention`` additive masks ``[B, 1, R, S + R]``.
          - ``prefix_lengths`` ``[B]``, ``response_lengths`` ``[B]``, ``R`` (int).

    Raises:
        ValueError: On non-2D / mismatched-shape inputs.
    """
    for name, t in (("input_ids", input_ids), ("loss_mask", loss_mask),
                    ("attention_mask", attention_mask), ("noisy", noisy)):
        if t.dim() != 2:
            raise ValueError(f"{name} must be [B, S], got shape {tuple(t.shape)}")
    if not (input_ids.shape == loss_mask.shape == attention_mask.shape == noisy.shape):
        raise ValueError("input_ids / loss_mask / attention_mask / noisy must share shape [B, S]")

    batch_size, seq_len = input_ids.shape
    device = input_ids.device

    prefix_lengths = _split_prompt_response(loss_mask, seq_len)  # [B]
    effective_lengths = attention_mask.to(device=device, dtype=torch.long).sum(dim=1)  # [B]
    response_lengths = (effective_lengths - prefix_lengths).clamp(min=0)  # [B]

    canvas_len = int(response_lengths.max().item()) if batch_size else 0
    # Degenerate batch with no supervised tokens: keep a 1-wide canvas so the
    # forward/loss shapes stay valid; the empty loss_mask zeroes the loss.
    canvas_len = max(canvas_len, 1)

    # Gather each canvas position into the absolute sequence:
    # canvas pos j of example b <- absolute pos prefix_lengths[b] + j.
    offsets = torch.arange(canvas_len, device=device)[None, :]  # [1, R]
    abs_idx = prefix_lengths[:, None] + offsets  # [B, R]
    valid = (abs_idx < effective_lengths[:, None]) & (offsets < response_lengths[:, None])  # [B, R]
    gather_idx = abs_idx.clamp(max=seq_len - 1)  # clamp pad positions for gather

    def _gather(t: torch.Tensor) -> torch.Tensor:
        return torch.gather(t, 1, gather_idx)

    canvas_ids = _gather(noisy)
    target_ids = _gather(input_ids)
    canvas_loss = _gather(loss_mask.bool()) & valid  # pad canvas positions are unsupervised
    decoder_position_ids = abs_idx.clamp(max=seq_len - 1)

    # One-canvas-per-step (train_ft.py:895-912): restrict the diffusion loss to a
    # single randomly-chosen response block per example. The forward still
    # denoises all blocks; only the selected block's supervised tokens are scored.
    canvas_block_id = (offsets // block_size).expand(batch_size, -1)  # [B, R]
    num_valid_blocks = ((response_lengths - 1).clamp(min=0) // block_size + 1).clamp(min=1)  # [B]
    sel_seed = base_seed + 7919 * step + int(microbatch_idx) + (1 << 42)
    gen = torch.Generator().manual_seed(sel_seed)
    sel_block = torch.floor(torch.rand(batch_size, generator=gen) * num_valid_blocks.float().cpu()).long()
    sel_block = sel_block.to(device)  # [B]
    canvas_loss = canvas_loss & (canvas_block_id == sel_block[:, None])

    mask_full, mask_sliding = build_batched_block_mask(
        prefix_lengths=prefix_lengths,
        response_lengths=response_lengths,
        canvas_len=canvas_len,
        enc_len=seq_len,
        block_size=block_size,
        sliding_window=sliding_window,
        device=device,
        dtype=mask_dtype,
    )

    encoder_padding_mask = attention_mask.to(device=device, dtype=torch.bool).logical_not()

    return {
        "canvas_ids": canvas_ids,
        "target_ids": target_ids,
        "canvas_loss": canvas_loss,
        "decoder_position_ids": decoder_position_ids,
        "decoder_padding_mask": valid.logical_not(),
        "encoder_padding_mask": encoder_padding_mask,
        "decoder_attention_mask": {"full_attention": mask_full, "sliding_attention": mask_sliding},
        "prefix_lengths": prefix_lengths,
        "response_lengths": response_lengths,
        "R": canvas_len,
    }
