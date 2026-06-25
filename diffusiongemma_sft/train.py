"""Minimal block-diffusion SFT training loop for DiffusionGemma (GSM8K smoke run).

Wires the whole pipeline: unsloth load + LoRA (experts/router frozen) -> ChatJsonlDataset
-> DLLMCollator -> D3PM corruption -> response window -> two-pass forward -> diffusion +
encoder-AR loss -> backward. Single-GPU / small-batch first; scale later.

Run (after the model finishes downloading):
    python -m diffusiongemma_sft.prep_gsm8k --output data/gsm8k_chat_train.jsonl
    python -m diffusiongemma_sft.train --max-steps 20 --batch-size 1 --grad-accum 8

Memory budget (2x RTX 4090 D 48GB = 96GB total; 26B-A4B bf16 LoRA):
  - weights 26B x 2B = ~52GB -> device_map="auto" splits across 2 GPUs ~26GB/card
  - LoRA + AdamW (LoRA-only) ~1-2GB
  - logit peak (V=262144!): encoder_logits[B,1024,V]fp32=1.07GB + CE softmax ~1GB +
    canvas/sc_logits ~0.5GB ~= 3GB, concentrated on the lm_head card
  - activations (gradient checkpointing ON) ~ a few GB
  - per-card peak ~32-35GB < 48GB, ~13GB headroom at batch=1 / GSM8K-short sequences.
  OOM levers if a card gets tight: lower --max-seq-len, keep batch_size=1, or switch the
  encoder-AR loss to a chunked cross-entropy (avoid materializing [B,S,V] at once).

NOTE: the model forward and LoRA wiring can only be validated once the 26B weights are
present. Points flagged "VERIFY@load" below need a live check on first run.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
# Reduce allocator fragmentation (must be set before `import torch`).
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import torch

from diffusiongemma_sft.data.collator import CollatorConfig, DLLMCollator, build_response_window
from diffusiongemma_sft.data.corruption import (
    CorruptionConfig,
    corrupt_uniform_random,
    corruption_generator,
)
from diffusiongemma_sft.data.dataset import ChatJsonlDataset, load_diffusiongemma_tokenizer
from diffusiongemma_sft.loss import block_diffusion_loss, encoder_ar_loss
from diffusiongemma_sft.model_forward import freeze_router, two_pass_forward


@dataclass(frozen=True)
class TrainConfig:
    model_name: str = "unsloth/diffusiongemma-26B-A4B-it"
    data_path: str = "data/gsm8k_chat_train.jsonl"
    # diffusion
    block_size: int = 256
    max_seq_len: int = 1024
    vocab_size: int = 262144
    eps: float = 1e-3
    self_conditioning_p: float = 0.5
    encoder_loss_weight: float = 1.0
    # optim
    batch_size: int = 1
    grad_accum: int = 8
    lr: float = 1.5e-4
    weight_decay: float = 1e-4
    max_steps: int = 20
    warmup_steps: int = 5
    grad_clip: float = 1.0
    # lora
    lora_r: int = 16
    lora_alpha: int = 16
    # misc
    seed: int = 42
    load_in_4bit: bool = False  # 96GB VRAM -> bf16 full-precision LoRA preferred


def set_seed(seed: int) -> None:
    import random

    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _build_balanced_device_map(num_layers: int = 30, split: int = 16) -> dict:
    """Explicit 2-GPU module device_map for DiffusionGemma (see load-path note in main).

    encoder.layers[i] and decoder.layers[i] share storage (tied), so each pair MUST go to
    the same device. The three tied embeddings (encoder/decoder embed_tokens + lm_head) are
    co-located on cuda:0. Layers [0, split) -> cuda:0, [split, num_layers) -> cuda:1.
    """
    device_map = {
        "model.encoder.language_model.embed_tokens": 0,
        "model.encoder.language_model.norm": 1,
        "model.encoder.language_model.rotary_emb": 0,
        "model.encoder.vision_tower": 0,
        "model.encoder.embed_vision": 0,
        "model.decoder.embed_tokens": 0,
        "model.decoder.norm": 1,
        "model.decoder.rotary_emb": 0,
        "model.decoder.self_conditioning": 1,
        "lm_head": 0,
    }
    for i in range(num_layers):
        dev = 0 if i < split else 1
        device_map[f"model.encoder.language_model.layers.{i}"] = dev
        device_map[f"model.decoder.layers.{i}"] = dev
    return device_map


def _self_conditioning_coin(batch_size: int, p: float, seed: int, step: int, mb_idx: int) -> torch.Tensor:
    """Per-example self-conditioning coin [B] bool (seed matches the corruption stream offset 0)."""
    gen = torch.Generator().manual_seed(seed + 7919 * step + mb_idx)
    return torch.rand(batch_size, generator=gen) < p


def gpu_mem_report(tag: str, warn_gib: float = 44.0) -> None:
    """Print per-GPU memory via nvidia-smi (ground truth; torch stats miss device_map loads)."""
    import subprocess

    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits"],
            text=True,
        )
        parts = []
        for line in out.strip().splitlines():
            idx, used = (x.strip() for x in line.split(","))
            used_gib = float(used) / 1024
            flag = "  <-- NEAR LIMIT" if used_gib > warn_gib else ""
            parts.append(f"GPU{idx} used={used_gib:.1f}G{flag}")
        print(f"[mem:{tag}] " + " | ".join(parts))
    except Exception as e:  # noqa: BLE001
        print(f"[mem:{tag}] nvidia-smi failed: {e}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-path", default=TrainConfig.data_path)
    ap.add_argument("--max-steps", type=int, default=TrainConfig.max_steps)
    ap.add_argument("--batch-size", type=int, default=TrainConfig.batch_size)
    ap.add_argument("--grad-accum", type=int, default=TrainConfig.grad_accum)
    ap.add_argument("--lr", type=float, default=TrainConfig.lr)
    ap.add_argument("--load-in-4bit", action="store_true")
    args = ap.parse_args()
    cfg = TrainConfig(
        data_path=args.data_path,
        max_steps=args.max_steps,
        batch_size=args.batch_size,
        grad_accum=args.grad_accum,
        lr=args.lr,
        load_in_4bit=args.load_in_4bit,
    )
    set_seed(cfg.seed)

    # 1. Load model + tokenizer.
    #    FIRST-RUN FIX (unsloth device_map broken): unsloth's FastDiffusionModel "slow /
    #    transformers-only path" left ALL weights on the META device (device_map="balanced"
    #    ignored -> 0GB on both GPUs -> meta-device crash). transformers' own
    #    `from_pretrained(device_map="balanced"/"auto")` ALSO silently leaves everything on
    #    meta for this arch (5.12.1 + accelerate 1.13.0). Root cause: heavy weight tying
    #    (encoder.layers[i] <-> decoder.layers[i], and lm_head <-> decoder.embed <->
    #    encoder.embed) defeats accelerate's auto device-map / tied-param dispatch.
    #    Fix: an EXPLICIT module-level device_map that (a) keeps encoder.layers[i] and the
    #    tied decoder.layers[i] on the SAME device (so the shared storage is allocated once),
    #    and (b) co-locates the three tied embeddings + lm_head on cuda:0. This actually
    #    materializes + splits the ~52GB checkpoint (~38GB GPU0 / ~28GB GPU1 at peak).
    dtype = torch.bfloat16
    from transformers import AutoTokenizer
    from transformers.models.diffusion_gemma import DiffusionGemmaForBlockDiffusion

    device_map = _build_balanced_device_map(num_layers=30, split=16)
    model = DiffusionGemmaForBlockDiffusion.from_pretrained(
        cfg.model_name, dtype=dtype, device_map=device_map, attn_implementation="eager",
    )
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)

    # 2. Freeze router, then attach LoRA via plain PEFT.
    gpu_mem_report("after-load")  # VERIFY@load: weights should split ~balanced across both cards
    n_frozen = freeze_router(model)
    print(f"[lora] froze {n_frozen} router params")  # VERIFY@load: expect >0, and NOT dense-MLP
    from peft import LoraConfig, get_peft_model

    # FIRST-RUN FIX (LoRA targets): a bare suffix list (["q_proj", ...]) matched the vision
    # tower's `Gemma4ClippableLinear` (a non-nn.Linear wrapper PEFT rejects) AND the frozen
    # `router.proj`. Anchor to the TEXT encoder/decoder layer projections (all plain
    # nn.Linear) with a path regex, so LoRA lands on attn q/k/v/o + dense MLP gate/up/down
    # only -- never the fused 3D experts, never the router, never the vision tower.
    lora_targets = (
        r".*(encoder\.language_model|decoder)\.layers\.\d+\."
        r"(self_attn|mlp)\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)$"
    )
    model = get_peft_model(
        model,
        LoraConfig(
            r=cfg.lora_r, lora_alpha=cfg.lora_alpha, target_modules=lora_targets,
            lora_dropout=0.0, bias="none", task_type=None,
        ),
    )
    model.print_trainable_parameters()

    # 3. Data.
    ds = ChatJsonlDataset(cfg.data_path, tokenizer, cfg.max_seq_len)
    collator = DLLMCollator(CollatorConfig(
        pad_token_id=tokenizer.pad_token_id or 0,
        eos_token_id=tokenizer.eos_token_id or 1,
        block_size=cfg.block_size,
        pad_seq_len_divisible=cfg.block_size,
        max_seq_len=cfg.max_seq_len,
    ))
    loader = torch.utils.data.DataLoader(
        ds, batch_size=cfg.batch_size, shuffle=True, collate_fn=collator, drop_last=True
    )

    # 4. Optimizer + cosine schedule over trainable (LoRA) params only.
    trainable = [p for p in model.parameters() if p.requires_grad]
    optim = torch.optim.AdamW(trainable, lr=cfg.lr, betas=(0.95, 0.99), weight_decay=cfg.weight_decay)
    # Clamp warmup fraction to (0, 0.3] so tiny smoke runs (max_steps < warmup) don't break OneCycleLR.
    pct_start = min(0.3, max(cfg.warmup_steps / max(cfg.max_steps, 1), 0.05))
    sched = torch.optim.lr_scheduler.OneCycleLR(
        optim, max_lr=cfg.lr, total_steps=cfg.max_steps,
        pct_start=pct_start, anneal_strategy="cos",
    )

    # Inputs go to the device holding encoder.embed_tokens (cuda:0 in the device_map).
    # With the split load `next(model.parameters()).device` is unreliable; pin to cuda:0.
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    corruption_cfg = CorruptionConfig(vocab_size=cfg.vocab_size, eps=cfg.eps)

    # 5. Training loop.
    model.train()
    step = 0
    optim.zero_grad()
    while step < cfg.max_steps:
        for mb_idx, batch in enumerate(loader):
            input_ids = batch["input_ids"].to(device)
            loss_mask = batch["loss_mask"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            bsz = input_ids.shape[0]

            # corruption (D3PM-uniform)
            gen = corruption_generator(cfg.seed, step=step, microbatch_idx=mb_idx, rank=0, device=device)
            noisy, _ = corrupt_uniform_random(input_ids, loss_mask, corruption_cfg, generator=gen)

            # response window (carve canvas + block-causal masks)
            window = build_response_window(
                input_ids, loss_mask, attention_mask, noisy,
                block_size=cfg.block_size, step=step, microbatch_idx=mb_idx, base_seed=cfg.seed,
            )
            window = {k: (v.to(device) if torch.is_tensor(v) else
                          {kk: vv.to(device) for kk, vv in v.items()} if isinstance(v, dict) else v)
                      for k, v in window.items()}

            do_sc = _self_conditioning_coin(bsz, cfg.self_conditioning_p, cfg.seed, step, mb_idx).to(device)

            # two-pass forward
            canvas_logits, encoder_logits = two_pass_forward(
                model, input_ids, attention_mask, window, do_sc
            )

            # loss = diffusion (canvas) + encoder AR (co-trained)
            diff_loss = block_diffusion_loss(canvas_logits, window["target_ids"], window["canvas_loss"])
            ar_loss = encoder_ar_loss(encoder_logits, input_ids, attention_mask)
            loss = (diff_loss + cfg.encoder_loss_weight * ar_loss) / cfg.grad_accum
            loss.backward()

            if (mb_idx + 1) % cfg.grad_accum == 0:
                torch.nn.utils.clip_grad_norm_(trainable, cfg.grad_clip)
                optim.step()
                sched.step()
                optim.zero_grad()
                step += 1
                print(f"[step {step}/{cfg.max_steps}] diff={diff_loss.item():.4f} "
                      f"ar={ar_loss.item():.4f} lr={sched.get_last_lr()[0]:.2e}")
                if step == 1 or step % 5 == 0:
                    gpu_mem_report(f"step{step}")  # watch for any card approaching 48GB
                if step >= cfg.max_steps:
                    break

    out_dir = "outputs/diffusiongemma_lora_gsm8k"
    os.makedirs(out_dir, exist_ok=True)
    model.save_pretrained(out_dir)
    print(f"✓ saved LoRA adapter -> {out_dir}")


if __name__ == "__main__":
    main()
