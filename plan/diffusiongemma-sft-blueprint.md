# DiffusionGemma 26B-A4B Block-Diffusion SFT — 技术蓝图

> 来源：逐行研读 NVIDIA-NeMo-Automodel 的官方 DiffusionGemma SFT 实现 + transformers `modeling_diffusion_gemma.py`。
> 目标：用 **unsloth 加载** DiffusionGemma + **自写 block-diffusion 训练循环** 复现 SFT（数据先 GSM8K 跑通，再换 Jackrong）。
> 所有 file_path:line 可核对。

## 0. 两个开工前必读的关键警告

**(A) transformers 的模型 forward 与 NeMo 的训练 forward 不是同一个契约。**
- `transformers/models/diffusion_gemma/modeling_diffusion_gemma.py:1627` `DiffusionGemmaForBlockDiffusion.forward` 是**推理** forward：接收 `decoder_input_ids`(canvas) + 外部传入的 `self_conditioning_logits`，跑**一遍** decode，**只返回** canvas `logits`（+ `encoder_last_hidden_state`，不是 encoder logits）。它**不做**内部的两遍 self-conditioning，**不返回** `encoder_logits`。
- `nemo_automodel/components/models/diffusion_gemma/model.py:521` 的 `DiffusionGemmaForBlockDiffusion.forward` 才是 recipe 实际调用的**训练** forward：接收 `canvas_ids`，encoder 跑一次 + decoder 跑**两次**（pass-1 no-grad 出 self-cond 信号，pass-2 带 grad），返回 `DiffusionGemmaOutput(logits, encoder_logits)`。
- **结论**：要复刻训练行为，必须自己复现 NeMo `model.py` 的 forward（~150 行），或手动驱动 transformers 模型做两遍 pass。

**(B) 没有现成的 HF 内部 loss 路径可用。** transformers encoder 声明 `accepts_loss_kwargs = False`（`modeling_diffusion_gemma.py:980-981`）。line 980 附近的 "loss/labels filtering" 只是这个 flag + 多模态 placeholder 逻辑，**不是** diffusion loss。所有 SFT loss 在 recipe 外部计算（见第 4 节）。

---

## 1. 数据构造（collator）

### 1a. 样本 → unshifted 格式（dataset 层，非 collator）
`ChatDataset`（`nemo_automodel/components/datasets/llm/chat_dataset.py`），配置 `unshifted: true`, `mask_history: true`（`diffusion_gemma_sft.yaml:122-133`）。
- 每行 `{"messages":[{user},{assistant}]}` → `format_chat_template(..., unshifted=True)`（`formatting_utils.py:446-476`）：返回 **`input_ids`**（全长，**不** shift）、**`loss_mask`**（assistant/监督 token 处为 1）、**`attention_mask`**。不产生 shift 后的 labels —— corruption 需要同 index 的干净 token，所以不 shift。
- `prep_gsm8k.py` 写 `messages=[user(question), assistant(answer)]`，监督区 = answer。
- `mask_history=True` → 折叠成**最后一段连续监督后缀**（`chat_dataset.py:407-428`）。**必须**：collator 若见到 >1 段监督会 `AssertionError`（`collate.py:101-109`）。

### 1b. Collator：`DLLMCollator`（`nemo_automodel/components/datasets/dllm/collate.py`）
DiffusionGemma 走 `response_window=True`（`train_ft.py:746`）。每 batch（`collate.py:81-169`）：
1. 单轮守卫（`:101-109`）：拒绝 raw `loss_mask` 有 >1 段监督的样本。
2. `prefix_lengths` = 每样本首个监督 index（= response 起点 = prompt 长度）。
3. **两段 block 对齐 padding**，布局 `[真实token][EOS块填充, loss=1, attended][PAD全局填充, loss=0, not attended]`：
   - `fill_ends`：response 长度向上取整到 `block_size`(256) 的倍数，**response 相对**：`fill_end = prefix + ceil(resp/bs)*bs`。
   - `target_len`：batch 内 `fill_end` 最大值，再取整到 `lcm(block_size, pad_seq_len_divisible)`(均256)，上限 `max_seq_len`。
   - `_pad_and_fill`：`[0,content)` 拷内容，`[content,fill_end)` 填 **EOS**，`[fill_end,target_len)` 填 **pad**(0)。
4. 字段填充值：
   - `input_ids`: pad=`pad_token_id`(0), block-fill=`eos_token_id`。
   - `loss_mask`（`:140-148`）: pad=0, **block-fill=1**（EOS 块填充也是监督的 —— 让模型学会发 EOS 终止 block）。
   - `attention_mask`（`:155-162`）: pad=0, **block-fill=1**（attended）。
5. 返回 `{input_ids, loss_mask(float), attention_mask, input_lengths}`，均 `[B, target_len]`。**这里没有 decoder_input_ids** —— canvas 在 recipe 里切。

### 1c. prompt/answer 如何映射到 encoder/canvas（关键洞察）
**collator 不把 prompt/answer 拆成两份。** 整条序列（prompt+answer+EOS填充）留在 `input_ids`。encoder context vs decoder canvas 的拆分在 recipe forward 时做（`_build_response_window`, `train_ft.py:830-942`）：
- **Encoder 输入** = **干净全序列** `input_ids [B,S]`。
- **Decoder canvas** = **仅 noised 的 response 区**，从 noised 序列 gather 出来。canvas 宽度 `R = batch 内最长 response`，短的右 pad 并从 loss 丢弃。
- **`canvas_length=256` 是 block_size（diffusion block 粒度），不是 canvas 张量宽度**（宽度 = 最长 response，动态）。验证：`canvas_len = response_lengths.max()`（`train_ft.py:865`）；`block_size = dllm_block_size or canvas_length`（`:893`）。
- canvas 构造（`train_ft.py:870-891`）：canvas 位置 `j` 例 `b` → 绝对 index `prefix_lengths[b]+j`；`valid=(abs_idx<eff_len)&(j<resp_len)`；`canvas_ids=gather(noisy)`, `target_ids=gather(clean)`, `canvas_loss=gather(loss_mask)&valid`, `decoder_position_ids=abs_idx`（绝对位置，RoPE 对齐干净 encoder keys）。

### 1d. 哪些位置算 loss
- **Diffusion loss**（canvas）：`canvas_loss = gather(loss_mask) & valid & (canvas_block_id == sel_block)` —— 仅 **step 选中的那一个 block** 内的监督 response token（one-canvas-per-step, `train_ft.py:895-912`）。是该 block 全部监督 token，**不只**被 corrupt 的。
- **Encoder AR loss**：全 valid 序列的 next-token 对 = `attention_mask[:,:-1] & attention_mask[:,1:]`。
- **被 mask 掉**：全局 pad、未选中的 canvas block。

---

## 2. 前向加噪 / corruption（block-diffusion 核心）

策略 `BlockDiffusionStrategy`（`strategy.py:757-877`），kernel `corrupt_uniform_random`（`corruption.py:223-294`）。

**是 D3PM-uniform corruption —— 没有 `[MASK]` token。**（`strategy.py:810-817`，`block_size=None`）
1. 每序列采一个 corruption level **`t ~ U(eps,1)`**：`t = eps + (1-eps)*rand(B,1)`（`corruption.py:276`）。`block_size=None` → 每例一个 `t`。
2. `noise_mask = (rand(B,L) < t) & loss_mask.bool()`（`:284-285`）—— 每监督位独立以概率 `t` corrupt。
3. **替换 = 均匀随机 vocab token**：`random_tokens = randint(0, vocab_size, (B,L))`; `noisy = where(noise_mask, random_tokens, input_ids)`（`:288-289`）。
4. **`p_mask` 全 1**（`:292`）—— uniform kernel 用 flat loss，**无 1/t 重加权**（1/p 是 absorbing-MASK ELBO 权重，不适用 uniform kernel）。

**复现种子**（`train_ft.py:244-262`）：`base_seed + 7919*step + microbatch_idx + 104729*rank + (2<<42)`。`(2<<42)` 与 block 选择(`1<<42`)、self-cond(`+0`) 解耦。

**"diffusion mask" 含义**（`test_diffusion_gemma_mask.py` + `attention_mask.py`）：不是 corruption mask，是 decoder 的**块因果注意力 mask**，形状 `[B,1,R,enc_len+R]`：
- **左列 `[0,enc_len)`** = 干净 encoder KV。`M_OBC`（offset-block-causal）：block `i` 的 canvas query 仅当其 response-block index **严格** `< i` 才看 encoder 列（`attention_mask.py:165`, `q_block > enc_block`）。**严格 `>` 是防泄漏不变量** —— `>=` 会让 canvas 看到正在去噪的干净答案（loss 崩溃；`test_diffusion_gemma_mask.py:48-104` 断言）。prompt 列（`enc_rel<0`）哨兵 block id `−1` → 永远可见。
- **右列 `[enc_len, enc_len+R)`** = noised canvas KV。`M_BD`（块对角）：block `i` 仅在 block `i` 内双向（`attention_mask.py:167-170`）。
- **sliding 变体**（`:175-208`）：25 个 sliding 层用块锚定窗口；层 {5,11,17,23,29} 用 full mask。`sliding_window=1024`。
- 逐例组装 `_build_batched_block_mask`（`train_ft.py:944-988`）；pad query 行保留自对角线，避免 softmax 全 `−inf`。

---

## 3. Self-conditioning

配置 `self_conditioning: true`，概率 `self_conditioning_p = 0.5`（`train_ft.py:768`）。**逐例硬币、decoder 两遍 forward、仅 pass-2 backprop**（`model.py:623-667`）：
- **硬币**（`train_ft.py:990-1006`）：`do_self_conditioning = rand(B) < 0.5`，`[B]` bool，种子 `base+7919*step+mb_idx`。
- **Pass-1**（`model.py:646-656`）：**总是**跑 decode，`torch.no_grad()`，`self_conditioning_logits=None`（→ 零软嵌入）。出 `sc_logits = softcap(pass1_hidden).detach()`。总是跑保证 FSDP collective 每步一致。
- **Pass-2**（`model.py:658-667`）：真正 grad pass，喂 `self_conditioning_logits=sc_logits` + `self_conditioning_mask=do_sc`。
- **信号如何进入**（`model.py:254-265` / `modeling_diffusion_gemma.py:1248-1257`）：`soft_emb = softmax(sc_logits, fp32) @ embed_tokens.weight * embed_scale`；逐例门控 `soft_emb *= mask[:,None,None]`（硬币 False → 置零 = 无 self-cond）；`inputs_embeds = self_conditioning(inputs_embeds, soft_emb)`，其中 `DiffusionGemmaSelfConditioning` 是带 pre/post RMSNorm 的门控 MLP（`modeling_diffusion_gemma.py:762-795`）。
- 即：启用且训练时 **2 遍 decode**；pass-1 no-grad 总跑；硬币只门控 pass-2 是否消费信号。encoder 跑一次。

---

## 4. Diffusion loss

`BlockDiffusionCrossEntropyLoss`（`dllm_loss.py:164-233`），经 `BlockDiffusionStrategy.create_loss_fn`（`strategy.py:793-797`）。注意 YAML `loss_fn: MaskedCrossEntropy` 被**覆盖**（dLLM recipe 从 strategy 建 loss，`train_ft.py:149`）。

### 4a. Diffusion 项（canvas loss）
**对选中 block 内全部监督 canvas token 的 flat masked CE —— corrupt 与未 corrupt 都算，无 1/p 加权**（`dllm_loss.py:220-231`）：
```
token_nll = cross_entropy(logits[B,R,V], target_ids[B,R], reduction="none")  # [B,R]
mask      = loss_mask.bool()        # noise_mask 显式丢弃（dllm_loss.py:226 `del noise_mask`）
loss      = (token_nll * mask).sum() / max(num_diffusion_tokens, 1)
```
- **loss 支撑 = canvas_mask（全部监督 canvas 位），非 noise-gated。**
- `num_diffusion_tokens` = 全局 all-reduce 的 `window["loss_mask"].sum()`（`train_ft.py:783-828`）。
- one-canvas-per-step：forward 去噪全部 block，loss 只在逐例随机选中的 block 上（`sel_block`，种子 `base+7919*step+mb_idx+(1<<42)`）。

### 4b. Encoder AR 项（co-trained，不在 diffusion loss 类里）
recipe 的 `_forward_backward_step`（`train_ft.py:1132-1143`）加 `encoder_ar_loss`（`dllm_loss.py:47-78`）：对**干净**序列的标准 causal next-token CE，支撑 `attention_mask[:,:-1] & attention_mask[:,1:]`，归一 `num_ar_tokens`，权重 `encoder_loss_weight=1.0`。
```
total_microbatch_loss = diffusion_loss + 1.0 * encoder_ar_loss
```
仅 `self.training` 且 `encoder_logits is not None` 时加。

### 4c. 与标准 causal-LM loss 的关键区别
- diffusion 项目标 = **同 (unshifted) index 的干净 token**，canvas 上无 `labels=input_ids[:,1:]` shift。
- loss 是**双向 block**（canvas 在 block 内双向），非左到右。
- 无 1/t 重加权（uniform kernel，flat CE）。
- 两个 loss 相加：diffusion(canvas) + AR(encoder)。
- 全局 token 归一：每 microbatch loss 除以**全局** all-reduce 分母，backward 再 `* dp_group_size`（`train_ft.py:1149`）。

### 4d. Logit softcapping
`_softcap_logits`（`model.py:513-519` / `modeling_diffusion_gemma.py:1675-1679`）：
```
logits = lm_head(hidden).to(fp32)
if cap is not None: logits = tanh(logits/cap)*cap
```
canvas、encoder（训练）、pass-1 self-cond logits 都过。`final_logit_softcapping` 来自 `text_config`。CE 在这些 fp32 softcapped logits 上算。

---

## 5. 训练配置要点

| 参数 | 值 | 作用 |
|---|---|---|
| `canvas_length` | 256 | = block_size（diffusion block 粒度）；canvas 张量宽度 = batch 最长 response |
| `dllm.block_size` | 256 | 块因果 mask + one-canvas 选择 |
| `dllm.vocab_size` | 262144 | corrupt_uniform_random 随机 token 替换范围（**必填**） |
| `dllm.eps` | 0.001 | corruption level `t` 下界 |
| `self_conditioning` | true | 启用两遍 self-cond（p=0.5） |
| `freeze_router` | true | 冻结 MoE gate `proj.weight`+`scale`；experts 仍可训（`model.py:462-482`） |
| `self_conditioning_p` | 0.5 | 逐例 self-cond 硬币概率 |
| `encoder_loss_weight` | 1.0 | co-trained AR loss 权重 |
| `torch_dtype` | float32 | **fp32 master weights**（AdamW 状态 fp32） |
| `mp_policy.param_dtype` | bfloat16 | **bf16 compute** |
| `mp_policy.reduce/output_dtype` | float32 | fp32 梯度规约 + 输出 |
| optimizer | AdamW, lr 1.5e-4, betas(0.95,0.99), wd 1e-4 | |
| LR sched | cosine, warmup 25, min 1.5e-5 | |
| dist | FSDP2, EP=8, activation ckpt on | **我们只有 2 GPU，需改 EP** |

**fp32 master + bf16 compute**：fp32 加载；NeMo `_restore_loaded_dtype=False`（`train_ft.py:100-104`）保住 fp32 master；FSDP2 `MixedPrecisionPolicy` compute 用 bf16、grad 规约 fp32、AdamW 更新 fp32 master；logits forward 中显式 upcast fp32。

**LoRA 变体**（`diffusion_gemma_lora.yaml:71-83`）：LoRA 仅 attention q/k/v/o + dense MLP gate/up/down；**不**在 EP-sharded experts、router、tied lm_head。dim=16, alpha=32。

---

## 6. 最小可复现训练循环骨架（伪代码）

**必须复现 NeMo 的两遍 model forward**（transformers forward 不会做）。两选项：(A) 重实现 encode/decode 拆分（推荐，对照 model.py）；(B) 驱动 transformers `DiffusionGemmaForBlockDiffusion` 做两遍 pass + 外部 self_conditioning_logits。

```python
BLOCK=256; EPS=1e-3; VOCAB=262144; SC_P=0.5; SW=1024; ENC_LOSS_W=1.0
# 来自 DLLMCollator(response_window=True): input_ids[B,S]干净, loss_mask[B,S]float, attention_mask[B,S]
clean = input_ids.clone()

# 1. CORRUPTION (D3PM-uniform, 无 mask token)  corruption.py:276-292
gen = torch.Generator(device).manual_seed(BASE + 7919*step + mb_idx + 104729*rank + (2<<42))
t = EPS + (1-EPS)*torch.rand((B,1), device=device, generator=gen)
noise_mask = (torch.rand((B,S),device=device,generator=gen) < t) & loss_mask.bool()
rand_tok = torch.randint(0, VOCAB, (B,S), device=device, generator=gen)
noisy = torch.where(noise_mask, rand_tok, clean)

# 2. RESPONSE WINDOW: 从 noised 序列切 canvas  train_ft.py:830-942
prefix_len = first_supervised_index_per_row(loss_mask)      # = prompt 长度 [B]
eff_len = attention_mask.long().sum(1)
resp_len = (eff_len - prefix_len).clamp(min=0)
R = int(resp_len.max())
off = torch.arange(R,device=device)[None]
abs_idx = prefix_len[:,None] + off
valid = (abs_idx < eff_len[:,None]) & (off < resp_len[:,None])
gidx = abs_idx.clamp(max=S-1)
canvas_ids  = noisy.gather(1, gidx);  target_ids = clean.gather(1, gidx)
canvas_loss = loss_mask.bool().gather(1, gidx) & valid
dec_pos_ids = abs_idx.clamp(max=S-1); dec_pad_mask = ~valid
# one-canvas-per-step  train_ft.py:895-912
blk_id = (off//BLOCK).expand(B,-1)
n_blocks = ((resp_len-1).clamp(min=0)//BLOCK + 1).clamp(min=1)
g2 = torch.Generator().manual_seed(BASE + 7919*step + mb_idx + (1<<42))
sel = torch.floor(torch.rand(B,generator=g2)*n_blocks.float().cpu()).long().to(device)
canvas_loss = canvas_loss & (blk_id == sel[:,None])
# 块因果 mask [B,1,R,S+R]  attention_mask.py
mask_full, mask_sliding = build_batched_block_mask(prefix_len, resp_len, R, S, BLOCK, SW, ...)
dec_mask = {"full_attention":mask_full, "sliding_attention":mask_sliding}
enc_pad_mask = ~attention_mask.bool()

# 3. SELF-COND 硬币  train_ft.py:990-1006
g3 = torch.Generator().manual_seed(BASE + 7919*step + mb_idx)
do_sc = torch.rand(B, generator=g3) < SC_P

# 4. FORWARD: encode 一次, decode 两次  model.py:599-668
with autocast(bf16):
    enc_kv, enc_hidden = model.encode(clean, position_ids=arange(S), padding_mask=enc_pad_mask, return_hidden=True)
    encoder_logits = softcap(lm_head(enc_hidden).float())
    with torch.no_grad():                                    # pass-1 总跑
        h1 = model.decode(canvas_ids, encoder_kv=enc_kv, decoder_position_ids=dec_pos_ids,
                          decoder_masks=dec_mask, decoder_padding_mask=dec_pad_mask, self_conditioning_logits=None)
        sc_logits = softcap(lm_head(h1).float()).detach()
    h2 = model.decode(canvas_ids, encoder_kv=enc_kv, decoder_position_ids=dec_pos_ids,
                      decoder_masks=dec_mask, decoder_padding_mask=dec_pad_mask,
                      self_conditioning_logits=sc_logits, self_conditioning_mask=do_sc)
    logits = softcap(lm_head(h2).float())                    # canvas-only

# 5. LOSS  dllm_loss.py:220-231 + 47-78
num_diff = global_allreduce(canvas_loss.sum())
nll = F.cross_entropy(logits.reshape(-1,V), target_ids.reshape(-1), reduction="none").reshape(B,R)
diff_loss = (nll * canvas_loss.float()).sum() / max(num_diff,1)   # FLAT, 无1/t, noise_mask 不用
ar_valid = attention_mask.bool()
num_ar = global_allreduce((ar_valid[:,:-1]&ar_valid[:,1:]).sum())
ar_nll = F.cross_entropy(encoder_logits[:,:-1].reshape(-1,V), clean[:,1:].reshape(-1), reduction="none").reshape(B,S-1)
ar_mask = (ar_valid[:,:-1]&ar_valid[:,1:]).float()
ar_loss = (ar_nll*ar_mask).sum() / max(num_ar,1)
loss = diff_loss + ENC_LOSS_W*ar_loss
(loss * dp_group_size).backward()    # 多卡全局 token 归一; 单卡 dp_group_size=1
# clip grad norm 1.0; AdamW(fp32 master).step; zero_grad; lr_scheduler.step
```

**unsloth 移植要点**：
- `softcap` = `final_logit_softcapping`（读 config）。
- transformers 等价：encoder pass = `model.model.encoder(...)` 填 `Cache`，再 `model.model.decoder(decoder_input_ids=canvas_ids, past_key_values=cache, self_conditioning_logits=..., self_conditioning_mask=..., decoder_attention_mask=dec_mask(dict), decoder_position_ids=dec_pos_ids)`。**传 dict 形式 mask 绕过内部 mask 构造**（`modeling_diffusion_gemma.py:1272-1278`）。encoder logits 需 `encoder_last_hidden_state`（`:1451`）+ 自己的 lm_head。
- `freeze_router`：每层 `gate.proj.weight.requires_grad_(False)`, `gate.scale.requires_grad_(False)`（`model.py:473-482`）。
- 单卡：`global_allreduce` = 恒等，`dp_group_size=1`。

## 文件地图
- recipe/训练循环：`nemo_automodel/recipes/dllm/train_ft.py`（`DiffusionGemmaSFTRecipe`:703, response window:830, fwd/bwd:1008, 分母:783）
- 策略/corruption dispatch：`nemo_automodel/recipes/dllm/strategy.py`（`BlockDiffusionStrategy`:757）
- corruption kernel：`nemo_automodel/components/datasets/dllm/corruption.py`（`corrupt_uniform_random`:223）
- collator：`nemo_automodel/components/datasets/dllm/collate.py`（`DLLMCollator`:35）
- loss：`nemo_automodel/components/loss/dllm_loss.py`（`BlockDiffusionCrossEntropyLoss`:164, `encoder_ar_loss`:47）
- 块因果 mask：`nemo_automodel/components/models/diffusion_gemma/attention_mask.py`（`build_block_diffusion_training_mask`:73）
- NeMo 训练 model forward：`nemo_automodel/components/models/diffusion_gemma/model.py`（forward:521, encode/decode:180/235, freeze_router:462, softcap:513）
- transformers 推理 model：`transformers/models/diffusion_gemma/modeling_diffusion_gemma.py`（forward:1627, Model.forward:1516, decoder:1214, self-cond:762）
- mask 测试（泄漏门）：`tests/unit_tests/models/diffusion_gemma/test_diffusion_gemma_mask.py`
