"""Verify DiffusionGemma loads via unsloth + can attach PEFT LoRA (SFT prerequisite)."""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
import time, torch
import unsloth
from unsloth import FastModel

MODEL = "unsloth/diffusiongemma-26B-A4B-it"

t0 = time.time()
print(f"[load] starting FastModel.from_pretrained (bf16, device_map=auto, 96GB VRAM)...", flush=True)
model, tokenizer = FastModel.from_pretrained(
    model_name=MODEL,
    load_in_4bit=False,
    dtype=torch.bfloat16,
    device_map="auto",
)
print(f"[load] ✓ model loaded in {time.time()-t0:.1f}s", flush=True)
print(f"[load] model class: {type(model).__name__}", flush=True)
print(f"[load] tokenizer/processor: {type(tokenizer).__name__}", flush=True)

# GPU memory footprint
for i in range(torch.cuda.device_count()):
    used = torch.cuda.memory_allocated(i) / 1024**3
    print(f"[mem] GPU{i}: {used:.1f} GB allocated", flush=True)

# Attach LoRA (SFT prerequisite)
t1 = time.time()
print("[lora] attaching PEFT LoRA...", flush=True)
model = FastModel.get_peft_model(model, r=16, lora_alpha=16)
print(f"[lora] ✓ LoRA attached in {time.time()-t1:.1f}s", flush=True)

print("\n✓✓✓ DiffusionGemma 加载 + LoRA 全部成功，SFT 环境就绪！", flush=True)
