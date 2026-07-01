# DiffusionGemma MoE 项目 — 阶段性成果

> 更新于 2026-06-24。本文档记录"环境搭建 + 复现 SFT"阶段的成果，作为后续工作的基线。

## 1. 项目目标

打磨 **DiffusionGemma 26B-A4B**（block-diffusion MoE 语言模型）的微调与建模。两条线：

- **线 A（工程复现，第一关）**：用 unsloth 加载 DiffusionGemma + 自写 block-diffusion SFT 训练循环，先用 GSM8K 跑通流程，再换 Jackrong reasoning 数据。
- **线 B（建模研究，待启动）**：从第一性原理重新建模 Diffusion MoE 的训练/推理范式，探索能否逼近甚至在特定维度超过 AR MoE。

## 2. 已完成

### 2.1 训练环境（conda env `dllm`）
- 硬件：**2× RTX 4090 D 48GB = 96GB 显存**（足够 bf16 全精度加载 26B / 52GB）
- 软件：Python 3.13.5 + **torch 2.7.1+cu126** + **transformers 5.12.1** + unsloth 2026.6.9 + peft 0.19.1 + trl 1.6.0 + bitsandbytes
- 关键避坑：
  - unsloth 用 `pip install --no-deps` 安装，避免把 torch 误升级到 2.10
  - **DiffusionGemma 需要 transformers 5.12.1**（≤5.5.0 不识别 `diffusion_gemma`）；unsloth 标称 ≤5.5.0 的警告可忽略（FastDiffusionModel 是 slow-path，不受版本绑定）
  - 已验证：transformers 5.12.1 原生识别 `diffusion_gemma`（128 experts/30 层），unsloth FastDiffusionModel 可用

### 2.2 资源下载（全部在 `/data/huggingface/hub`，5.7T 盘）
- **模型**：`unsloth/diffusiongemma-26B-A4B-it`（🔄 校验式重下中 — 发现 7/11 分片下载损坏，正自动重下校验）
- **Jackrong 10 个数据集**（dataset.md）：全部完成（~56GB，含 GLM/Kimi 各 25-30GB）
- **报告推荐 12 个数据集**（DiffusionGemma.md）：全部完成（NuminaMath、OpenThoughts、gsm8k、CodeForce_SAGA、humaneval_infilling、JSONSchemaBench、AgentTrove 等）
- **GitHub 16 个 repos**（`/home/lingxufeng/huggingface/repos/`）：Jackrong-llm-finetuning-guide、NVIDIA-NeMo-Automodel、LLaDA/LLaDA2、Dream/Dream-Coder/DreamOn、dInfer、dFactory、DiffuCoder、dLLM-RL、Prism、DCD 等
- 下载避坑：`HF_HUB_DISABLE_XET=1` + `--max-workers 2` + 重试循环（Xet 后端会开 80+ 连接撑爆网络栈）

### 2.3 技术蓝图与代码
- **`plan/diffusiongemma-sft-blueprint.md`**：逐行扒清 NeMo 官方 DiffusionGemma SFT 的完整训练机制（collator、D3PM-uniform corruption、块因果 mask、两遍 self-conditioning、diffusion loss + encoder AR loss）
- **`diffusiongemma_sft/data/corruption.py`**：D3PM-uniform 加噪模块 ✅（6 个单测全过）

## 3. 关键技术发现

1. **Jackrong 脚本不适用**：Jackrong 唯一训练脚本是 GSPO（RL）+ AR 模型 Qwopus，不是 SFT 也不是 diffusion。
2. **unsloth 只负责加载**：FastDiffusionModel 提供加载 + 4bit + LoRA + 推理，**无训练 loss**。
3. **transformers forward 是推理版**：`DiffusionGemmaForBlockDiffusion.forward` 一遍 decode、只返回 canvas logits。训练需要的**两遍 self-conditioning + encoder AR logits** 只在 NeMo 的 `model.py` 里 —— 必须自己复现（encoder 一次 + decoder 两次）。
4. **block diffusion 机制**：corruption 是 D3PM-uniform（随机 vocab 替换，无 mask token）；canvas = 从噪声序列切出的 response 区；loss = 选中 block 的监督 token 上的 flat masked CE（无 1/t 加权）+ encoder AR loss；experts/router 冻结，LoRA 只在 attention + dense MLP。

## 4. 工程线代码（全部完成）

| 模块 | 依赖模型权重 | 状态 |
|------|:---:|------|
| `data/corruption.py`（D3PM-uniform 加噪） | ❌ | ✅ 完成 + 单测 |
| `data/collator.py`（response-window 切 canvas） | ❌ | ✅ 完成 + 单测 |
| `data/mask.py`（块因果 mask + 泄漏不变量） | ❌ | ✅ 完成 + 单测（翻转 `>`→`>=` 必失败验证） |
| `data/dataset.py`（messages→tokenized，真实 tokenizer） | ❌ | ✅ 完成 + 单测 |
| `loss.py`（diffusion + AR loss + softcap） | ❌ | ✅ 完成 + 单测 |
| `prep_gsm8k.py`（GSM8K→messages，7473 行） | ❌ | ✅ 完成 |
| `model_forward.py`（两遍 forward） | ✅ | ✅ 写完（基于确认的源码行为，**未实测**） |
| `train.py`（训练循环 + LoRA + 显存安全） | ✅ | ✅ 写完（**未实测**） |

**测试**：56 个单测全过（含端到端集成测试：dataset→collator→corruption→response_window→mask→loss + 梯度 backward）。整条数据/loss 管线已用真实 GSM8K + tokenizer 验证，仅缺 model_forward 的实测（等模型权重）。

## 5. 模型下载诊断（最终方案）

网络对 huggingface.co 不稳，踩过三个坑，最终方案：
- **禁用 Xet**（`HF_HUB_DISABLE_XET=1`）— Xet 后端开 80+ 连接撑爆网络栈
- **禁用 hf_transfer**（`HF_HUB_ENABLE_HF_TRANSFER=0`）— 138 连接触发 HF 限流 → 0 速度
- **`--max-workers 2`** — 这个网络下的最优解，稳定 1.7 MB/s（停掉竞争的其他模型下载后）
- **下载+校验循环** — 网络中断会损坏分片（大小达标但 header 坏），每轮 safetensors 校验 + 删损坏重下

## 6. 交接给科研/arbor 的工程线（首跑必查 + 成功判据）

工程脚手架已就绪，剩下是"在真实模型上跑起来 + 调试"，这正是 arbor executor 该做的（Direction SFT gate）。**但 `model_forward.py` / `train.py` 是基于源码静态分析写的，没在 26B 上跑过——首跑大概率要调几处。** 交接时必查（train.py 里标了 `VERIFY@load`）：

| 首跑必查点 | 可能的问题 | 在哪查 |
|---|---|---|
| device_map="balanced" 是否两卡均衡 | 某卡先满 → OOM | `gpu_mem_report("after-load")` |
| `freeze_router` 参数名匹配 | over/under-match（误冻 dense MLP，或漏冻 router） | 打印 frozen 数 + 抽查 named_parameters |
| LoRA target（FastDiffusionModel.get_peft_model） | 是否落在 attn+dense MLP，没碰 experts | print_trainable_parameters |
| 显存峰值（V=262144 的 logits） | encoder_logits[B,S,V] 峰值超预算 | 每步 `gpu_mem_report` |
| encoder/decoder 接口细节 | attention_mask 格式 / position_ids / cache 类型不符 | 首个 forward 的报错 |
| GSM8K chat 格式简化 | thought-channel 不对齐（dataset.py 标了 TODO） | 仅影响质量，不影响跑通 |

**"基本跑通"成功判据**（不需要复现 SOTA）：
1. 模型加载不 OOM，两卡均衡
2. 一个完整 training step 跑通（forward + loss + backward + optimizer.step）不爆显存
3. `diff_loss` 和 `ar_loss` 都是**有限值**（非 NaN/Inf），且多步后**不发散**（理想是缓慢下降）
4. 满足以上即 gate 通过 → Direction A / C 的训练实验可以接着做

一条命令：`python -m diffusiongemma_sft.train --max-steps 20 --batch-size 1`

## 7. 开放研究问题（线 B，已移交科研 session）

详见 `diffusion-moe-first-principles-framing.md` + `research-goal.md`。核心：质量差距主因是 L2（启发式 sampling），用 learned commitment policy（trajectory-level RL）+ timestep-aware MoE routing 攻它。
