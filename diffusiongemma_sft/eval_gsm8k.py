"""GSM8K dev exact-match evaluation for the DiffusionGemma block-diffusion SFT baseline.

Generates answers for a DEV holdout (carved from GSM8K-TRAIN) with the real
denoising loop (``DiffusionGemmaForBlockDiffusion.generate``, reusing the same
explicit ``_build_balanced_device_map`` as training), extracts the final numeric
answer, and computes exact-match accuracy against the gold ``#### <answer>``.

EVAL DISCIPLINE: B_test = GSM8K TEST split is SEALED -> never loaded here. The dev
slice is the LAST ``--dev-holdout`` rows of the TRAIN jsonl (same rows the baseline
training EXCLUDED), so it is on data the model never trained on.

Decoding is the model's shipped ``generation_config.json`` (EntropyBoundSampler,
t_max=0.8/t_min=0.4, max_denoising_steps=48), with a fixed seed for reproducibility.

Run (SFT adapter):
    python -m diffusiongemma_sft.eval_gsm8k \
        --adapter outputs/diffusiongemma_sft_baseline/final \
        --dev-holdout 300 --n-eval 200 --out outputs/diffusiongemma_sft_baseline/eval_sft.json

Run (pretrained baseline, no adapter):
    python -m diffusiongemma_sft.eval_gsm8k --no-adapter --n-eval 200 \
        --out outputs/diffusiongemma_sft_baseline/eval_pretrained.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import torch

from diffusiongemma_sft.train import (
    TrainConfig,
    _build_balanced_device_map,
    gpu_mem_report,
    set_seed,
)

# ---- answer extraction ------------------------------------------------------

_GSM8K_GOLD_RE = re.compile(r"####\s*(-?[\d,]*\.?\d+)")
_NUM_RE = re.compile(r"-?\$?[\d,]*\.?\d+")


def _norm_number(s):
    """Normalize a numeric string: strip $/commas, drop a trailing '.0', etc."""
    if s is None:
        return None
    s = s.replace(",", "").replace("$", "").strip().rstrip(".")
    if not s:
        return None
    try:
        f = float(s)
    except ValueError:
        return None
    if f == int(f):
        return str(int(f))
    return repr(f)


def extract_gold(answer):
    """Pull the gold numeric answer (after the GSM8K '#### ' marker)."""
    m = _GSM8K_GOLD_RE.search(answer)
    return _norm_number(m.group(1)) if m else None


def extract_pred(text):
    """Extract the predicted numeric answer from a generation.

    Priority: an explicit '#### <num>' marker (the model may mimic GSM8K format);
    otherwise the LAST number in the text (the conventional GSM8K eval heuristic).
    """
    m = _GSM8K_GOLD_RE.search(text)
    if m:
        return _norm_number(m.group(1))
    nums = _NUM_RE.findall(text)
    return _norm_number(nums[-1]) if nums else None


# ---- evaluation -------------------------------------------------------------


def load_dev_rows(data_path, dev_holdout, n_eval):
    """Return the first ``n_eval`` rows of the dev holdout (last ``dev_holdout`` jsonl rows)."""
    with open(data_path, encoding="utf-8") as f:
        rows = [json.loads(line)["messages"] for line in f if line.strip()]
    dev = rows[len(rows) - dev_holdout:]
    out = []
    for msgs in dev[:n_eval]:
        user = next(m["content"] for m in msgs if m["role"] == "user")
        gold = next(m["content"] for m in msgs if m["role"] == "assistant")
        out.append({"question": user, "gold_raw": gold, "gold": extract_gold(gold)})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-path", default=TrainConfig.data_path)
    ap.add_argument("--adapter", default="outputs/diffusiongemma_sft_baseline/final",
                    help="LoRA adapter dir (ignored if --no-adapter)")
    ap.add_argument("--no-adapter", action="store_true",
                    help="evaluate the pretrained model (LoRA disabled) for the baseline delta")
    ap.add_argument("--dev-holdout", type=int, default=300)
    ap.add_argument("--n-eval", type=int, default=200)
    ap.add_argument("--max-new-tokens", type=int, default=512)
    ap.add_argument("--add-generation-prompt", action="store_true",
                    help=("Use the model-card inference prompt suffix. By default eval matches the "
                          "SFT target prefix, where the assistant turn opener is generated."))
    ap.add_argument("--out", default="outputs/diffusiongemma_sft_baseline/eval_sft.json")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    set_seed(args.seed)
    dtype = torch.bfloat16
    from transformers import AutoTokenizer
    from transformers.models.diffusion_gemma import DiffusionGemmaForBlockDiffusion

    device_map = _build_balanced_device_map(num_layers=30, split=16)
    model = DiffusionGemmaForBlockDiffusion.from_pretrained(
        TrainConfig.model_name, dtype=dtype, device_map=device_map, attn_implementation="eager",
    )
    tokenizer = AutoTokenizer.from_pretrained(TrainConfig.model_name)
    gpu_mem_report("after-load")

    used_adapter = None
    if not args.no_adapter:
        from peft import PeftModel

        model = PeftModel.from_pretrained(model, args.adapter)
        used_adapter = args.adapter
        print(f"[eval] loaded LoRA adapter -> {args.adapter}")
    else:
        print("[eval] pretrained model (no adapter) -> baseline")
    model.eval()

    dev = load_dev_rows(args.data_path, args.dev_holdout, args.n_eval)
    use_generation_prompt = args.add_generation_prompt or args.no_adapter
    print(f"[eval] dev rows={len(dev)} (last {args.dev_holdout} of train jsonl), "
          f"max_new_tokens={args.max_new_tokens}, add_generation_prompt={use_generation_prompt}")

    device = getattr(
        model,
        "device",
        torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
    )
    correct = 0
    skipped_gold = 0
    records = []
    t0 = time.time()

    for i, ex in enumerate(dev):
        if ex["gold"] is None:  # malformed gold -> exclude from denominator
            skipped_gold += 1
            continue
        msgs = [{"role": "user", "content": ex["question"]}]
        enc = tokenizer.apply_chat_template(
            msgs,
            tokenize=True,
            add_generation_prompt=use_generation_prompt,
            return_dict=True,
            return_tensors="pt",
        )
        if hasattr(enc, "to"):
            enc = enc.to(device)
        else:
            enc = {k: v.to(device) if torch.is_tensor(v) else v for k, v in enc.items()}
        input_ids = enc["input_ids"]

        with torch.no_grad():
            out = model.generate(**enc, max_new_tokens=args.max_new_tokens)
        seq = out.sequences if hasattr(out, "sequences") else out
        prompt_len = input_ids.shape[1]
        new_ids = seq[0][prompt_len:]
        text = tokenizer.decode(new_ids, skip_special_tokens=True)
        raw_text = tokenizer.decode(new_ids, skip_special_tokens=False)
        pred = extract_pred(text)
        is_correct = pred is not None and pred == ex["gold"]
        correct += int(is_correct)

        tokens_per_forward = getattr(out, "tokens_per_forward", None)
        if tokens_per_forward is not None:
            tokens_per_forward = float(tokens_per_forward[0].detach().cpu())

        records.append({
            "idx": i, "gold": ex["gold"], "pred": pred, "correct": is_correct,
            "prompt_tokens": prompt_len,
            "generated_tokens": int(new_ids.shape[0]),
            "tokens_per_forward": tokens_per_forward,
            "gen": text[:600],
            "gen_raw": raw_text[:600],
        })
        if (i + 1) % 10 == 0:
            elapsed = time.time() - t0
            graded = len(records)
            acc_so_far = correct / max(graded, 1)
            print(f"[eval {i + 1}/{len(dev)}] acc={acc_so_far:.3f} "
                  f"({correct}/{graded}) {elapsed / (i + 1):.1f}s/ex")

    graded = len(records)
    acc = correct / max(graded, 1)
    elapsed = time.time() - t0
    result = {
        "model": "sft" if used_adapter else "pretrained",
        "adapter": used_adapter,
        "n_eval_requested": args.n_eval,
        "n_graded": graded,
        "n_skipped_malformed_gold": skipped_gold,
        "correct": correct,
        "exact_match_accuracy": round(acc, 4),
        "max_new_tokens": args.max_new_tokens,
        "add_generation_prompt": use_generation_prompt,
        "decoding": "shipped generation_config.json (EntropyBoundSampler, t_max=0.8/t_min=0.4, "
                    "max_denoising_steps=48)",
        "seed": args.seed,
        "dev_holdout": args.dev_holdout,
        "wall_clock_s": round(elapsed, 1),
        "sec_per_example": round(elapsed / max(graded, 1), 2),
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"summary": result, "records": records}, f, indent=2)
    print("=" * 60)
    print(f"[RESULT] {json.dumps(result)}")
    print(f"[eval] wrote {args.out}")


if __name__ == "__main__":
    main()
