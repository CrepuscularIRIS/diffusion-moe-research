"""Longer block-diffusion SFT baseline run for DiffusionGemma on GSM8K.

Sibling of ``train.py`` (the committed 20-step smoke path is NOT modified). Reuses
``train.py``'s proven helpers verbatim (``_build_balanced_device_map``,
``_self_conditioning_coin``, ``set_seed``, ``gpu_mem_report``) and the same
two-pass forward + block-diffusion/encoder-AR loss. Adds only what a real baseline
needs on top of the smoke loop:

  - a longer schedule (``--max-steps`` ~480, ~2-3h wall-clock at ~20s/step),
  - a DEV HOLDOUT split (last ``--dev-holdout`` jsonl rows are excluded from
    training so they can be used for a clean dev exact-match eval),
  - periodic checkpointing (``--ckpt-every`` steps -> ``outputs/<run>/step_<n>/``),
  - a tailable per-step loss log (``outputs/<run>/loss_log.jsonl``) recording
    diff_loss / ar_loss / lr / step-time so progress is monitorable + the smoothed
    curve is reproducible from disk.

EVAL DISCIPLINE: B_test = GSM8K TEST split is SEALED and never touched here. The
dev holdout is carved from GSM8K-TRAIN only.

Run:
    python -m diffusiongemma_sft.train_baseline --max-steps 480 --ckpt-every 100 \
        --dev-holdout 300 --run-dir outputs/diffusiongemma_sft_baseline
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass, replace

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import torch

from diffusiongemma_sft.data.collator import CollatorConfig, DLLMCollator, build_response_window
from diffusiongemma_sft.data.corruption import (
    CorruptionConfig,
    corrupt_uniform_random,
    corruption_generator,
)
from diffusiongemma_sft.data.dataset import ChatJsonlDataset
from diffusiongemma_sft.loss import block_diffusion_loss, encoder_ar_loss
from diffusiongemma_sft.model_forward import freeze_router, two_pass_forward
from diffusiongemma_sft.train import (
    TrainConfig,
    _build_balanced_device_map,
    _self_conditioning_coin,
    gpu_mem_report,
    set_seed,
)


@dataclass(frozen=True)
class BaselineConfig:
    """Baseline-run knobs layered over the smoke ``TrainConfig`` (immutable)."""

    run_dir: str = "outputs/diffusiongemma_sft_baseline"
    dev_holdout: int = 300  # last N jsonl rows reserved for dev eval (NOT trained on)
    ckpt_every: int = 100  # save a LoRA checkpoint every N optimizer steps
    log_every: int = 1  # write a loss-log row every N optimizer steps


def _ema(values: list[float], alpha: float = 0.08) -> list[float]:
    """Exponential moving average of a 1-D series (for a smoothed loss curve)."""
    out: list[float] = []
    s = None
    for v in values:
        s = v if s is None else alpha * v + (1 - alpha) * s
        out.append(s)
    return out


def _save_checkpoint(model, run_dir: str, step: int) -> str:
    """Save the LoRA adapter for ``step`` and return its path."""
    ckpt_dir = os.path.join(run_dir, f"step_{step}")
    os.makedirs(ckpt_dir, exist_ok=True)
    model.save_pretrained(ckpt_dir)
    return ckpt_dir


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-path", default=TrainConfig.data_path)
    ap.add_argument("--max-steps", type=int, default=480)
    ap.add_argument("--batch-size", type=int, default=TrainConfig.batch_size)
    ap.add_argument("--grad-accum", type=int, default=TrainConfig.grad_accum)
    ap.add_argument("--lr", type=float, default=TrainConfig.lr)
    ap.add_argument("--warmup-steps", type=int, default=30)
    ap.add_argument("--run-dir", default=BaselineConfig.run_dir)
    ap.add_argument("--dev-holdout", type=int, default=BaselineConfig.dev_holdout)
    ap.add_argument("--ckpt-every", type=int, default=BaselineConfig.ckpt_every)
    args = ap.parse_args()

    # Layer the baseline schedule over the proven smoke TrainConfig (one source of truth
    # for block_size / max_seq_len / lora / corruption hyperparams).
    cfg = replace(
        TrainConfig(),
        data_path=args.data_path,
        max_steps=args.max_steps,
        batch_size=args.batch_size,
        grad_accum=args.grad_accum,
        lr=args.lr,
        warmup_steps=args.warmup_steps,
    )
    bcfg = BaselineConfig(
        run_dir=args.run_dir, dev_holdout=args.dev_holdout, ckpt_every=args.ckpt_every
    )
    set_seed(cfg.seed)
    os.makedirs(bcfg.run_dir, exist_ok=True)
    log_path = os.path.join(bcfg.run_dir, "loss_log.jsonl")
    # Fresh log per run (so a tail always reflects the current run).
    log_f = open(log_path, "w", encoding="utf-8")

    # Record the full config + provenance for reproducibility.
    import subprocess

    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:  # noqa: BLE001
        git_hash = "unknown"
    meta = {
        "git_hash": git_hash,
        "train_config": asdict(cfg),
        "baseline_config": asdict(bcfg),
        "argv": vars(args),
    }
    with open(os.path.join(bcfg.run_dir, "run_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"[baseline] run_dir={bcfg.run_dir} git={git_hash[:8]} "
          f"max_steps={cfg.max_steps} dev_holdout={bcfg.dev_holdout}")

    # 1. Load model + tokenizer (identical explicit device-map path as the smoke run).
    dtype = torch.bfloat16
    from transformers import AutoTokenizer
    from transformers.models.diffusion_gemma import DiffusionGemmaForBlockDiffusion

    device_map = _build_balanced_device_map(num_layers=30, split=16)
    model = DiffusionGemmaForBlockDiffusion.from_pretrained(
        cfg.model_name, dtype=dtype, device_map=device_map, attn_implementation="eager",
    )
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    gpu_mem_report("after-load")

    n_frozen = freeze_router(model)
    print(f"[lora] froze {n_frozen} router params")
    from peft import LoraConfig, get_peft_model

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

    # 2. Data: TRAIN = all rows MINUS the last `dev_holdout` (the dev-eval slice).
    ds_full = ChatJsonlDataset(cfg.data_path, tokenizer, cfg.max_seq_len)
    n_total = len(ds_full)
    if bcfg.dev_holdout >= n_total:
        raise ValueError(f"dev_holdout {bcfg.dev_holdout} >= dataset size {n_total}")
    train_indices = list(range(n_total - bcfg.dev_holdout))
    train_ds = torch.utils.data.Subset(ds_full, train_indices)
    print(f"[data] total={n_total} train={len(train_ds)} "
          f"dev_holdout(last)={bcfg.dev_holdout} (rows {n_total - bcfg.dev_holdout}..{n_total - 1})")

    collator = DLLMCollator(CollatorConfig(
        pad_token_id=tokenizer.pad_token_id or 0,
        eos_token_id=tokenizer.eos_token_id or 1,
        block_size=cfg.block_size,
        pad_seq_len_divisible=cfg.block_size,
        max_seq_len=cfg.max_seq_len,
    ))
    # Seeded generator so the data order is reproducible across the run.
    g = torch.Generator().manual_seed(cfg.seed)
    loader = torch.utils.data.DataLoader(
        train_ds, batch_size=cfg.batch_size, shuffle=True,
        collate_fn=collator, drop_last=True, generator=g,
    )

    # 3. Optimizer + cosine schedule over LoRA params only.
    trainable = [p for p in model.parameters() if p.requires_grad]
    optim = torch.optim.AdamW(trainable, lr=cfg.lr, betas=(0.95, 0.99), weight_decay=cfg.weight_decay)
    pct_start = min(0.3, max(cfg.warmup_steps / max(cfg.max_steps, 1), 0.05))
    sched = torch.optim.lr_scheduler.OneCycleLR(
        optim, max_lr=cfg.lr, total_steps=cfg.max_steps,
        pct_start=pct_start, anneal_strategy="cos",
    )

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    corruption_cfg = CorruptionConfig(vocab_size=cfg.vocab_size, eps=cfg.eps)

    # 4. Training loop (epoch-wrapped: 7173 rows >> 480 steps, but loop defensively).
    model.train()
    step = 0
    optim.zero_grad()
    diff_hist: list[float] = []
    ar_hist: list[float] = []
    t_last = time.time()
    epoch = 0
    while step < cfg.max_steps:
        epoch += 1
        for mb_idx, batch in enumerate(loader):
            input_ids = batch["input_ids"].to(device)
            loss_mask = batch["loss_mask"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            bsz = input_ids.shape[0]

            gen = corruption_generator(cfg.seed, step=step, microbatch_idx=mb_idx, rank=0, device=device)
            noisy, _ = corrupt_uniform_random(input_ids, loss_mask, corruption_cfg, generator=gen)

            window = build_response_window(
                input_ids, loss_mask, attention_mask, noisy,
                block_size=cfg.block_size, step=step, microbatch_idx=mb_idx, base_seed=cfg.seed,
            )
            window = {k: (v.to(device) if torch.is_tensor(v) else
                          {kk: vv.to(device) for kk, vv in v.items()} if isinstance(v, dict) else v)
                      for k, v in window.items()}

            do_sc = _self_conditioning_coin(bsz, cfg.self_conditioning_p, cfg.seed, step, mb_idx).to(device)

            canvas_logits, encoder_logits = two_pass_forward(
                model, input_ids, attention_mask, window, do_sc
            )

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

                d = float(diff_loss.item())
                a = float(ar_loss.item())
                diff_hist.append(d)
                ar_hist.append(a)
                now = time.time()
                step_time = now - t_last
                t_last = now
                lr = sched.get_last_lr()[0]

                # NaN/Inf -> pre-declared death sentence. Save what we have, then abort.
                if not (d == d and a == a) or d == float("inf") or a == float("inf"):
                    print(f"[DIVERGED] step {step}: diff={d} ar={a} -> GATE-FAIL (NaN/Inf)")
                    log_f.write(json.dumps({"step": step, "diff": d, "ar": a, "lr": lr,
                                            "diverged": True}) + "\n")
                    log_f.flush()
                    _save_checkpoint(model, bcfg.run_dir, step)
                    log_f.close()
                    raise SystemExit("training diverged (NaN/Inf) -> GATE-FAIL")

                log_f.write(json.dumps({
                    "step": step, "epoch": epoch, "diff": round(d, 5), "ar": round(a, 5),
                    "lr": lr, "step_time_s": round(step_time, 2),
                    "diff_ema": round(_ema(diff_hist)[-1], 5),
                    "ar_ema": round(_ema(ar_hist)[-1], 5),
                }) + "\n")
                log_f.flush()

                if step == 1 or step % 10 == 0:
                    print(f"[step {step}/{cfg.max_steps}] diff={d:.4f} "
                          f"(ema {_ema(diff_hist)[-1]:.4f}) ar={a:.4f} "
                          f"lr={lr:.2e} t={step_time:.1f}s")
                if step == 1 or step % 25 == 0:
                    gpu_mem_report(f"step{step}")

                if step % bcfg.ckpt_every == 0:
                    ckpt = _save_checkpoint(model, bcfg.run_dir, step)
                    print(f"  ✓ checkpoint -> {ckpt}")

                if step >= cfg.max_steps:
                    break

    # 5. Final adapter + summary stats.
    final_dir = os.path.join(bcfg.run_dir, "final")
    os.makedirs(final_dir, exist_ok=True)
    model.save_pretrained(final_dir)
    log_f.close()

    diff_ema = _ema(diff_hist)
    ar_ema = _ema(ar_hist)
    summary = {
        "steps": step,
        "diff_start_ema": round(diff_ema[0], 4) if diff_ema else None,
        "diff_end_ema": round(diff_ema[-1], 4) if diff_ema else None,
        "ar_start_ema": round(ar_ema[0], 4) if ar_ema else None,
        "ar_end_ema": round(ar_ema[-1], 4) if ar_ema else None,
        "final_adapter": final_dir,
        "log_path": log_path,
    }
    with open(os.path.join(bcfg.run_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ saved final LoRA adapter -> {final_dir}")
    print(f"[summary] {json.dumps(summary)}")


if __name__ == "__main__":
    main()
