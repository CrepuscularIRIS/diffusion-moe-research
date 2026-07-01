# DSpark 深度分析 + Occupancy Scan — 2026-07-01

> 目的：系统分析 DSpark，找到 OPEN（未被占据）的优化方向，确定下一步是否可做 + 在什么模型上做。

## 1. DSpark 是什么

**DSpark** = Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation。
DeepSeek 2026-06-27 开源，作为 DeepSeek-V4 的推理加速模块（不是独立论文，arxiv:2606.19348 = V4 paper 的一部分）。
开源训练框架 = **DeepSpec**（MIT，github.com/deepseek-ai/DeepSpec）。

### 三组件架构
1. **Parallel backbone (DFlash)** — 一次并行生成 k 个位置的 base logits
2. **Sequential Markov head** — 一阶 Markov（只看前一个 token），rank-256 低秩分解，加一个 prefix-dependent bias 修正每个位置的 logit。训练时冻结 target model，复用 embedding + output head。用 total-variation distance 损失（直接最大化 draft acceptance rate）
3. **Confidence-scheduled verification** — confidence head 输出 per-position acceptance 概率；hardware-aware scheduler 根据 GPU 负载动态调整 verification length

### 性能
- Offline: accepted length 比 EAGLE-3 高 26-31%，比 DFlash 高 16-18%
- Production (V4): per-user generation speed +60-85% (Flash), +57-78% (Pro) vs MTP-1
- Markov head 几乎无额外开销（draft length 4→16 仅增 0.2-1.3% per-round latency）

### DSpark 的核心洞察
**Suffix decay** = 并行 draft 越远，acceptance 越低（因为不知道前面的 token 实际被采样成什么）。
Markov head 通过看前一个已采样 token 来修正后续 position 的 logit → 大幅提高 suffix acceptance。
但 Markov head 只看 1 步 → **under-modeled**（DSpark 自己的 ablation 承认 RNN variant tracking full prefix 有 marginal improvement，但选了 Markov 因为更快）。

## 2. Occupancy Scan — speculative decoding 优化空间

### 已被占据

| 方向 | 占据者 | 状态 |
|---|---|---|
| Draft model distillation | Medusa (2024), EAGLE/EAGLE-2 (2024-2025) | Dense |
| Multi-head parallel draft | Medusa, Hydra (2024), Jakiro (2025, MoE) | Dense |
| Tree-structured draft + verify | SpecInfer, Sequoia (2024) | Dense |
| Training-aware speculative | Draft-Verify-Improve (2025) | Occupied |
| Lookahead decoding (parallel n-gram) | Lookahead (2024) | Occupied |
| Cross-attention between draft/target | CASD (2025) | Occupied |
| MTP heads | FastMTP (2025), DeepSeek-V3 MTP | Occupied |
| Margin-aware verification | MARS (2026) | Occupied |
| Adaptive scheduling per-request | AdaSpec (2025) | Occupied (serving) |

### 可能 OPEN 的方向

| 方向 | 为什么可能 open | 96GB 可行 |
|---|---|---|
| **Beyond-1st-order sequential head** | DSpark 自己承认 RNN variant "marginal" 但没深入；没人系统研究 2nd-order / attention-based sequential head 的 quality/speed tradeoff | ✅ head 很小 |
| **MoE-router-informed draft quality** | MoE router logits 是 free signal（已计算），但没人用 router decisions 来 inform draft confidence/selective verify | ✅ 需要 MoE target |
| **Draft-time reasoning structure** | 现有 spec-dec 都是 token-level，不 model reasoning structure | ⚠️ 需要 reasoning traces |
| **Suffix decay information-theoretic bound → designed head** | 有理论 (NeurIPS 2024 Branching RW bounds) 但没人用它来 DESIGN head | ✅ theory + small head |

## 3. 诚实评估

**最有前景 = "beyond first-order Markov" sequential head。** DSpark 留了这个口，DeepSpec 框架现成，head 小 96GB 够，测量指标清晰。

**风险：** "marginal improvement" 可能意味着 1st-order 已近 ceiling — suffix decay 主要信息在前一个 token 里。需要 DPC 来 falsify。

## 4. 推荐下一步

1. 深读 DSpark + DeepSpec 代码 — 确认 RNN variant 具体实现 + ablation 数字
2. 精确 occupancy — 搜索有没有 "higher-order sequential head for speculative decoding" 的独立工作
3. 如果 OPEN → enrich /mos-front → Pro 设计 → /object-shift-audit → 训练
4. 训练基底 = Qwen3-4B/8B (DeepSpec 框架) 或 LLaMA-3-8B，96GB 够
