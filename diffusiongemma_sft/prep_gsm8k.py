"""Convert GSM8K to OpenAI-messages JSONL for DiffusionGemma block-diffusion SFT.

Raw ``openai/gsm8k`` is ``{question, answer}``; the training pipeline consumes the
OpenAI chat-messages schema (a ``messages`` list per row), with the assistant turn
as the supervised region. Reads from the local HF cache (offline).

Usage:
    python -m diffusiongemma_sft.prep_gsm8k --split train --output data/gsm8k_chat_train.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="data/gsm8k_chat_train.jsonl", help="output JSONL path")
    parser.add_argument("--split", default="train", help="GSM8K split (train/test)")
    parser.add_argument("--config", default="main", help="GSM8K config (main/socratic)")
    parser.add_argument("--limit", type=int, default=0, help="cap rows (0 = all); useful for smoke tests")
    args = parser.parse_args()

    # Use the local cache; do not hit the network. load_dataset("openai/gsm8k")
    # tries to resolve a Hub loading script even offline, so we locate the cached
    # parquet via snapshot_download and read it directly with pandas.
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    import pandas as pd
    from huggingface_hub import snapshot_download

    snap = snapshot_download("openai/gsm8k", repo_type="dataset", local_files_only=True)
    parquet_path = Path(snap) / args.config / f"{args.split}-00000-of-00001.parquet"
    if not parquet_path.exists():
        raise FileNotFoundError(f"GSM8K parquet not found: {parquet_path}")
    df = pd.read_parquet(parquet_path)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n = 0
    with out_path.open("w", encoding="utf-8") as f:
        for question, answer in zip(df["question"], df["answer"]):
            messages = [
                {"role": "user", "content": str(question)},
                {"role": "assistant", "content": str(answer)},
            ]
            f.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
            n += 1
            if args.limit and n >= args.limit:
                break
    print(f"Wrote {n} rows -> {out_path}")


if __name__ == "__main__":
    main()
