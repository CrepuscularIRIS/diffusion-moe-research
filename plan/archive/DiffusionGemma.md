# Diffusion MoE Language Models 逼近主流 AR MoE 质量的研究路线

## Executive Summary

- **这个方向值得做，但不值得从“纯预训练新模型”起步。** 过去 18 个月里，Diffusion LLM 已从“概念验证”快速推进到可与同规模 AR 模型接近的阶段：LLaDA 8B 获得了 NeurIPS 2025 oral，Dream 7B、Dream-Coder 7B、LLaDA-MoE、LLaDA2.0-flash、DiffusionGemma 都表明“并行去噪 + 半自回归块生成 + 稀疏 MoE/高效采样”是一条真实存在的能力曲线；但从零训练仍然昂贵，LLaDA-MoE 报告了约 20T token 训练量，LLaDA2.0-flash 报告了 100B/6.1B-active 级别的 MoE 扩展，这对本科/硕士阶段不现实。citeturn20view1turn17view0turn34view1turn9view12

- **Diffusion LLM 相比 AR LLM 的最大真实优势，不是“无条件更聪明”，而是**：并行 token/block 生成、双向上下文、天然适合 infill/edit/repair、以及通过额外 denoising steps 进行 test-time compute scaling。DiffusionGemma 官方明确把卖点放在高吞吐本地推理与双向自纠错；Google 报告其在 RTX 5090 上可达 700+ tok/s、单卡 H100 上可达 1000+ tok/s。citeturn21view0turn10view0

- **当前质量差距仍然存在，而且在复杂 reasoning / coding 上很明显。** DiffusionGemma 与同骨干 Gemma 4 26B A4B 相比，在 MMLU-Pro、AIME 2026、LiveCodeBench、GPQA 等指标上存在显著落后，例如官方模型卡给出的 AIME 2026 no-tools 为 69.1% vs 88.3%，LiveCodeBench v6 为 69.1% vs 77.1%。这说明“更快”并不自动等于“更强”。citeturn10view0turn10view1

- **质量瓶颈不应只归咎于 MoE。** 最新文献更一致地指向四个耦合问题：一是 diffusion objective 与训练—推理不一致；二是 few-step/fast-step 下的 factorization barrier 与 joint dependency 建模不足；三是 decoder/sampler/token commitment policy 仍大量依赖启发式；四是 diffusion 专用 post-training 数据与 RL 生态还远不如 AR 成熟。citeturn35search1turn31search14turn31search6turn20view2turn20view0

- **“Diffusion MoE”已经存在，而且不是单一方向。** 至少可以分为三条：一条是 Google 的 “Gemma-4 MoE backbone + block diffusion decoder” 路线；一条是 InclusionAI 的 LLaDA-MoE 与 LLaDA2.0-flash 路线；还有一条是 Dream/Dream-Coder 与后续 sampler/infilling/TraceRL 生态。现阶段最值得借鉴的，不是纯粹“再做一个 MoE”，而是把 **MoE + repair/infill 数据 + verifier-guided sampler + diffusion-aware post-training** 打包成完整 recipe。citeturn9view12turn34view0turn34view1turn17view1turn17view2

- **从 Jackrong 迁移时，最自然的落点不是先做开放域长链思维，而是先做**：代码修复、代码 infilling、JSON 修复、格式约束生成、bad-to-good repair、工具调用格式化。这些任务更符合 diffusion 的“整体草稿—局部重写—多步修复”生成范式，也更容易用 verifier 明确打分。Dream-Coder、DreamOn、DiffuCoder、JSONSchemaBench、CodeForce-SAGA、HumanEval-Infilling 等都支持这一判断。citeturn17view2turn19search3turn17view5turn26search3turn26search17turn25search1

- **如果目标是“尽量逼近 AR MoE 的质量”，最有希望的主线不是直接上 GRPO/GSPO 全家桶，而是**：先做 AR teacher → Diffusion student 的 repair-trace distillation，再做 verifier-filtered SFT，最后做轻量 diffusion-aware RL 或 trajectory-level RL。d1 已经证明 masked SFT + diffu-GRPO 有效，TraceRL 进一步证明“把推理轨迹信息带进 post-training”可以显著改善数学和代码任务。citeturn20view2turn20view0

- **作为本科/硕士科研项目，最适合作为论文贡献的点，不是“再做一个更大的 dLLM”，而是**：提出一个可复现、低算力、面向 repair/infill 的 Diffusion MoE post-training recipe，并用 verifier-guided sampler 或 token-commit policy 给出新 Pareto frontier。这个切口既能避开大厂预训练军备竞赛，也与 2025–2026 年最活跃的论文空白高度对齐。citeturn17view8turn17view7turn31search1turn31search14turn20view3

## Field Map

如果把这个领域画成研究地图，核心不是“Diffusion 替代 AR”，而是“在并行生成这条大轴上，不同模型家族如何在速度、依赖建模、推理质量之间重新分配预算”。近两年的综述已经把这件事讲得很清楚：AR、非 AR、半自回归、masked diffusion、block diffusion、parallel decoding、speculative decoding、test-time scaling，本质上都在研究 **如何减少严格 left-to-right 的串行瓶颈**。citeturn17view9turn17view10turn16view12

```text
AR LLM
  ├─ Dense AR
  ├─ AR MoE
  ├─ Speculative Decoding
  └─ Blockwise / Semi-AR

Non-AR / Parallel LM
  ├─ Masked LM / Infilling LM
  ├─ Discrete Diffusion LM
  │    ├─ Full-sequence masked diffusion
  │    ├─ Block diffusion / multi-canvas diffusion
  │    ├─ Sequential diffusion / adaptive block diffusion
  │    └─ Diffusion MoE
  └─ Other insertion / deletion-insertion / consistency variants

Post-training Stack
  ├─ Distillation
  │    ├─ AR → Diffusion adaptation
  │    ├─ reasoning distillation
  │    ├─ repair-trace distillation
  │    └─ trajectory distillation
  ├─ SFT / LoRA / QLoRA
  ├─ Preference / verifier filtering
  └─ RL for diffusion
       ├─ diffu-GRPO / d1
       ├─ TraceRL
       └─ sampler-aware RL

Inference Stack
  ├─ remasking policy
  ├─ confidence / entropy stopping
  ├─ token commitment policy
  ├─ hierarchical search / self-verification
  ├─ block-size scheduling
  └─ verifier-guided reranking / self-consistency
```

对你的项目最关键的关系有三条。第一，**Diffusion MoE 不是单独一层，而是“diffusion objective + semi-AR block decoding + sparse routing”的组合**；只改成 MoE，并不会自动解决质量问题。第二，**Jackrong 路线天然落在 post-training stack**，因此迁移时不应该先碰预训练，而应该先改数据格式、SFT 目标和 sampler。第三，**repair / infill / structured output** 是 diffusion 真正有比较优势的任务族，而不是所有通用问答都天然占优。citeturn10view0turn22view0turn17view0turn19search3turn26search3

## Literature Review

下面把文献分成四组：综述与基础、AR→Diffusion 迁移、Diffusion MoE 与大模型扩展、post-training 与 sampler。为了避免把“新 arXiv”“OpenReview 已接收论文”“官方模型卡/技术文档”混在一起，我单独标出来源状态。

**综述与基础文献**

| 文献 | 作者 | 年份 | 发表状态 | 核心观点 | 与本项目关系 | 是否值得精读 | 来源 |
|---|---|---:|---|---|---|---|---|
| *A Survey on Diffusion Language Models* | Tianyi Li 等 | 2025/2026 | arXiv v3 | 系统梳理 DLM 的训练、推理、控制、应用与挑战，强调并行生成与双向上下文优势，同时承认质量与效率之间仍有张力。 | 这是最适合你开题阶段建立全局框架的综述。 | **是** | citeturn17view9 |
| *Discrete Diffusion in Large Language and Multimodal Models: A Survey* | Runpeng Yu, Qi Li, Xinchao Wang | 2025 | arXiv | 更聚焦 discrete diffusion / dMLLM，把语言与多模态一起讲，并强调 full-attention、multi-token parallel decoding、fine-grained control。 | 如果你考虑后面延展到多模态或 tool-use，这篇更贴近系统视角。 | **是** | citeturn17view10 |
| *A Survey on Parallel Text Generation: From Parallel Decoding to Diffusion Language Models* | 未在抓取片段显示完整作者 | 2025 | arXiv | 把 speculative decoding、semi-AR、diffusion 放进同一 taxonomy；强调“parallel text generation”是更大的母问题。 | 有助于你避免把 diffusion 单独看成孤立路线。 | **是** | citeturn16view12 |
| *Promises, Outlooks and Challenges of Diffusion Language Models* | 未在抓取片段显示完整作者 | 2024 | arXiv | 早期总结 diffusion 文本建模的机会与限制。 | 可作为 related work 的历史综述补充。 | 选读 | citeturn36search16 |
| *Diffusion-LM Improves Controllable Text Generation* | Xiang Lisa Li 等 | 2022 | NeurIPS 2022 | 连续 latent diffusion 在 controllable generation 上展现优势。 | 是“为什么 diffusion 在 controllable/editing 更自然”的历史源头。 | 选读 | citeturn36search0 |
| *Structured Denoising Diffusion Models in Discrete State-Spaces* | Jacob Austin 等 | 2021 | NeurIPS 2021 Poster | D3PM 奠定 discrete diffusion 的结构化转移矩阵框架。 | 是离散扩散建模的基础。 | 选读 | citeturn36search1 |
| *Simplified and Generalized Masked Diffusion for Discrete Data* | Jiaxin Shi 等 | 2024 | arXiv | 把 masked diffusion 的连续时间变分目标重新整理成更清晰的加权交叉熵视角，并支持 state-dependent masking。 | 对你设计 diffusion-aware SFT / corruption schedule 很重要。 | **是** | citeturn36search2turn36search10 |

**里程碑与核心模型**

| 文献 | 作者 | 年份 | 状态 | 解决的问题 | 关键结论 | 与本项目关系 | 来源 |
|---|---|---:|---|---|---|---|---|
| *Large Language Diffusion Models* | Shen Nie 等 | 2025 | NeurIPS 2025 oral | 证明从零训练的大规模 diffusion LM 可以接近 LLaMA 3 8B 级别能力。 | LLaDA 8B 说明 diffusion 并不是“只能做填空”的小众范式。 | 你的领域基石。 | citeturn20view1turn16view0 |
| *Dream 7B: Diffusion Large Language Models* | Jiacheng Ye 等 | 2025 | arXiv | 进一步把开源 dLLM 做到 7B 并在 general/math/code 上超过更早 diffusion 模型。 | Dream 把“可用的 open dLLM”推到实战附近。 | 适合作为非 Gemma 备选基线。 | citeturn17view1turn9view1 |
| *Dream-Coder 7B* | Zhihui Xie 等 | 2025 | arXiv | 面向代码的 diffusion LLM，强调 any-order generation。 | 复杂算法任务会 sketch-first、简单任务会 left-to-right、理解任务会 interleaved reasoning。 | 对“repair/infill 先落地”非常关键。 | citeturn17view2turn9view2 |
| *DiffuCoder* | Shansan Gong 等 | 2025 | arXiv | 系统分析 masked diffusion 在代码任务上的训练与推理问题。 | 直接把“代码结构约束强，sampler/objective 尤其重要”说透。 | 你的实验设计几乎必读。 | citeturn17view5turn9view10 |
| *LLaDA-MoE* | Fengqi Zhu 等 | 2025 | arXiv / HF paper | 把稀疏 MoE 正式引入 diffusion LM。 | 7B 容量、1.4B active、20T 预训练 token，说明 Diffusion MoE 已经从概念进入工程化。 | 这是你主题最直接的先行工作。 | citeturn17view0turn34view0 |
| *LLaDA2.0: Scaling Up Diffusion Language Models to 100B* | InclusionAI 团队 | 2025 | HF paper / open model | 把 dLLM 扩到 100B/6.1B-active，并在多项基准接近 Qwen3-30B-A3B。 | 说明 dLLM 的规模扩展与 MoE 扩展正在发生。 | 用来回答“能否向 AR MoE 逼近”。 | citeturn34view1turn9view11 |
| *DiffusionGemma model overview* | Google DeepMind / Google AI | 2026 | 官方文档/模型卡 | 把 Gemma 4 26B A4B 改造成 block-autoregressive multi-canvas discrete diffusion 模型。 | 重点是低延迟、高吞吐、本地部署与双向自纠错，而不是绝对 SOTA 质量。 | 你若要基于 Gemma 生态迁移，这就是首选起点。 | citeturn9view12turn10view0 |

**AR → Diffusion 迁移与混合范式**

| 文献 | 年份 | 状态 | 主要想法 | 对你最重要的启示 | 来源 |
|---|---:|---|---|---|---|
| *Scaling Diffusion Language Models via Adaptation from Autoregressive Models* | 2025 | ICLR 2025 Poster | 通过 continual pretraining 把 GPT2/LLaMA 从 AR 适配成 DiffuGPT / DiffuLLaMA，不必从零训练。 | 这是“Jackrong 蒸馏数据能否直接迁移到 diffusion”的最直接证据之一。 | citeturn37view0 |
| *Efficient-DLM: From Autoregressive to Diffusion Language Models, and Beyond in Speed* | 2025 | arXiv | 系统研究 AR-to-dLM conversion，目标是保留 AR 准确率同时获得更好的速度。 | 如果你想从成熟 AR teacher 迁移，这是最应该跟踪的新论文。 | citeturn17view3 |
| *Large Language Models to Diffusion Finetuning* | 2025 | ICML 2025 Poster | 不改原有权重、通过 diffusion finetuning 让预训练 LLM 获得 test-time compute scaling 能力。 | 说明“AR 与 diffusion 不一定二选一”，可以做混合增强。 | citeturn37view1 |
| *Sequential Diffusion Language Models* | 2025/2026 | ICLR 2026 submitted | 用 Next Sequence Prediction 统一 next-token 与 next-block，最小代价 retrofit 现有 AR 模型。 | 它其实是你问题里“难道回到 loop LLM / semi-AR 吗”的一个非常强回答：**是，但要更系统地做。** | citeturn37view2 |

**Post-training、RL、Sampler 与推理时扩展**

| 文献 | 年份 | 状态 | 核心贡献 | 对本项目的价值 | 来源 |
|---|---:|---|---|---|---|
| *d1: Scaling Reasoning in Diffusion Large Language Models via Reinforcement Learning* | 2025 | NeurIPS 2025 spotlight | 提出 masked SFT + diffu-GRPO，把 reasoning post-training 正式带入 masked dLLM。 | 直接回答“GRPO 能不能迁移到 diffusion”：能，但要改成 diffusion-aware policy gradient。 | citeturn20view2 |
| *Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models* | 2026 | ICLR 2026 Poster | TraceRL：把 inference trajectory 信息纳入 post-training，并引入 diffusion-based value model。 | 对“repair traces / verifier-guided learning / process reward”尤其有启发。 | citeturn20view0 |
| *Prism* | 2026 | arXiv / 官方 repo 标注 ICML 2026 | 用 hierarchical search + partial remasking + self-verification 做高效 test-time scaling。 | 说明 dLLM 的 reasoning 提升不一定先靠 RL，sampler 本身就能大幅改进。 | citeturn17view7turn9view5 |
| *Saber* | 2025/2026 | arXiv | 针对代码任务设计 adaptive acceleration + backtracking remasking；平均 Pass@1 +1.9%，平均 251.4% speedup。 | 说明 code 场景里 sampler 直接决定质量—速度前沿。 | citeturn6search11turn17view8 |
| *Deferred Commitment Decoding* | 2026 | arXiv | 基于不确定性延迟 token commitment，平均精度提升 1.73%，最大可达 16.5%。 | 很适合做 verifier-guided 或 confidence-aware sampler 的复现基线。 | citeturn31search14 |
| *Learning Unmasking Policies for Diffusion Language Models* | 2025/2026 | arXiv / Apple repo | 把 unmask/commit 策略从启发式变为学习问题。 | 若要做 sampler 学术贡献，这是很值得跟的方向。 | citeturn31search6turn32search2 |
| *Breaking the Factorization Barrier in Diffusion Language Models* | 2026 | ICML 2026 / arXiv | 指出并行预测时的独立性假设导致质量退化，并提出 CoDD。 | 这是你回答“为什么 diffusion 质量差”的理论支点之一。 | citeturn35search1turn35search10 |
| *When to Commit? Towards Variable-Size Self-Contained Blocks* | 2026 | arXiv | 从 self-containedness 定义 block 边界，解决 fixed block 的训练推理失配。 | 对 block diffusion / multi-canvas Gemma 路线很相关。 | citeturn31search5 |
| *Learning a Token-Commitment Policy for Diffusion LLMs* | 2026 | arXiv | 将 token commitment 建模为可学习的 trace-state policy。 | 这是“verifier-guided sampler”之外的另一条高价值贡献线。 | citeturn31search1 |
| *DreamOn: Diffusion Language Models for Code Infilling Beyond Fixed-Size Canvas* | 2026 | OpenReview | 变长代码 infilling，性能达到或接近强 AR infilling 基线。 | 强烈支持你先攻 infill/repair 而不是长链开放问答。 | citeturn19search3turn32search10 |

从这批文献可以得出一个相对稳的判断：**Diffusion LLM 的主战场已经从“能不能做”切换到“如何在固定算力下做得更对”**。现在最有价值的增量不是再写一篇“我们也做了 dLLM”，而是围绕 **AR→Diffusion 迁移、repair/infill 数据蒸馏、trajectory-aware post-training、token commitment policy、verifier-guided decoding** 做系统性 recipe。citeturn37view0turn20view0turn31search1turn19search3turn35search1

## Open-source Repository Map

下面这张表按“对你这个项目的直接可用性”排序，而不是按知名度排序。由于 GitHub/HF 的 star 会波动，我保留的是本次检索时页面可见或检索快照中的数量/最近可见更新。

| 仓库 / 资源 | 现状 | 训练代码 | 推理代码 | 权重 | LoRA / 多卡 / MoE | 近端可见更新与热度 | 适合用途 | 判断 |
|---|---|---|---|---|---|---|---|---|
| `google/diffusiongemma-26B-A4B-it` + `google/hackable_diffusion` + Gemma adapter | 官方 | 有，JAX adapter 与官方 recipe | 有，Transformers/vLLM/SGLang/MLX | 有 | DiffusionGemma 支持；NeMo 还支持 LoRA；MoE 骨干 | `hackable_diffusion` 132★；Google 文档 2026-06-10 发布；官方支持 Gemma adapter citeturn22view1turn21view0turn9view3 | 以 Gemma 为起点做官方路线迁移 | **可直接复现** |
| `NVIDIA-NeMo/Automodel` DiffusionGemma recipe | 官方生态 | 有，full SFT / LoRA | 有 | 直接拉 HF checkpoint | FSDP2 + EP=8，多卡，LoRA，MoE | 616★；文档最后更新 2026-06-11；单机 8×H100 验证 citeturn22view0turn21view2 | 最稳的工程化微调起点 | **可直接复现** |
| `ML-GSAI/LLaDA` | 官方 | 有 | 有 | 有 | 主要是 dense dLLM；可做后续 sampler 实验 | 3.8k★；配套 NeurIPS 2025 oral citeturn23view0turn20view1 | 经典 dLLM 基线 | **可直接复现** |
| `inclusionAI/dInfer` | 官方 | 否，以推理为主 | 有 | 支持多模型 | 支持 LLaDA、LLaDA-MoE、LLaDA2 | 472★；v0.2.0 发布于 2025-12-21 citeturn23view3turn9view4 | 高吞吐推理、sampler 对比 | **可直接复现** |
| `inclusionAI/LLaDA2.X` / `inclusionAI/LLaDA-MoE-*` | 官方 | 部分开放，更多是模型卡 + 推理 | 有 | 有 | 明确支持 MoE；LLaDA2.0-flash 为 100B/6.1B-active | LLaDA2.X README 显示 2026-02 发布 2.1；LLaDA-MoE 模型卡显示 7B/1.4B-active、1000+ tok/s with dInfer citeturn9view11turn34view0turn34view1 | Diffusion MoE 对标参考 | **可直接复现但训练细节有限** |
| `DreamLM/Dream` | 官方 | 有，2025-09-26 公开训练代码 | 有 | 有 | 暂未主打 MoE，但完整 dLLM 生态成熟 | 1.3k★；Dream 7B 对外公开 citeturn23view1turn32search3 | 非 Gemma 路线对照组 | **可直接复现** |
| `DreamLM/Dream-Coder` / `DreamLM/DreamOn` | 官方 | 有 | 有 | 有 | 代码/infilling 聚焦 | Dream-Coder 104★；DreamOn 117★，组织页显示更新到 2026-02-03 citeturn23view2turn32search10 | code / infilling / repair 最佳参考 | **可直接复现** |
| `apple/ml-diffucoder` | 官方 | 有 | 有 | 有 | 面向 code 的 SFT / RL 路线，可与 Open-R1 结合 | 825★；论文与代码同步开放 citeturn9view10 | 代码任务 recipe、分析训练目标 | **可直接复现** |
| `Gen-Verse/dLLM-RL` | 官方 | 有 | 有 | TraDo 系列 | RL/post-training，兼容 full-/block-attn dLLM | 510★；对应 ICLR 2026 TraceRL citeturn23view5turn20view0 | diffusion-aware RL 主线 | **可直接复现** |
| `viiika/Prism` | 官方 | 否，以推理框架为主 | 有 | 否 | 对多 dLLM 通用 | 21★；repo 自标注 ICML 2026 citeturn23view4turn9view5 | test-time scaling / verifier 基线 | **可直接复现** |
| `shuyingte/DCD` | 官方 | 否，以 decoding 为主 | 有 | 否 | 通用 decoding 框架 | 6★；官方代码已发布 citeturn32search1 | uncertainty-aware commitment 基线 | **可直接复现** |
| `apple/ml-rl-dllm` | 官方 | 有 | 有 | 未必有完整权重 | unmask policy 学习 | 官方配套 *Learning Unmasking Policies* citeturn32search2 | token commitment / sampler 学习 | **可直接复现** |
| `R6410418/Jackrong-llm-finetuning-guide` | 社区项目 | 有 | 有 | 有配套模型/流程说明 | LoRA / QLoRA / GRPO / GSPO / GGUF 等齐全 | 约 1.5k★、250 forks；2026 年仍有活跃 issue citeturn11search1turn11search3turn11search7 | 你的原始工程蓝图 | **核心参考** |
| `Unsloth` DiffusionGemma 文档 | 社区工程 | 有 | 有 | 面向 HF 权重 | 明确支持 DiffusionGemma 训练/微调 | 文档页 2026-06-15 显示“可直接 train and fine-tune DiffusionGemma” citeturn27search4 | 单机轻量实验 | **推荐作轻量入口** |
| `LLaMA-Factory` | 社区工程 | AR 生态很强 | 有 | 多模型 | Gemma/MoE/LoRA/RL 很强，但未见官方 DiffusionGemma 专页 | 文档支持 Gemma、Mixtral-MoE、RLHF/DPO/KTO 等 citeturn28view1 | 可借用数据/训练框架，但需要改 model wrapper | **需要大改** |
| `axolotl` | 社区工程 | 有 | 有 | 多模型 | 2025-09 起支持 text diffusion；MoE/LoRA/GRPO 很强 | 2025-09 明确加入 text diffusion；2026 年支持 Gemma4、Qwen3.5 MoE、SonicMoE fused LoRA 等 citeturn28view2 | 若要融合 AR+MoE+diffusion 工程，价值很高 | **需要中等改动** |
| `TRL` / `OpenRLHF` / `verl` | 官方/社区 RL 框架 | 有 | 有 | 面向 AR 为主 | GRPO/DPO/PPO 完整，但默认 token-in-token-out | TRL v1、OpenRLHF、verl 都强调 SFT/GRPO/DPO/PPO，但没有原生 diffusion trajectory API citeturn29search0turn29search1turn29search5 | 可借 optimizer/infra，不适合作为第一阶段直接上手 | **只能部分参考** |

一个很现实的结论是：**做 DiffusionGemma 最稳的起点是 Google 官方 + NeMo/Unsloth；做 Diffusion MoE 的“质量—速度研究”最稳的对照组是 LLaDA-MoE/LLaDA2 + dInfer + Prism/DCD/TraceRL；做代码与 repair 任务最稳的实验土壤是 Dream-Coder / DreamOn / DiffuCoder。** 你不需要在第一阶段自己发明整个训练栈。citeturn21view0turn22view0turn34view0turn34view1turn19search3turn17view5

## Model Comparison and Technical Bottlenecks

先给出一个面向你项目需求的模型对比表。这里的“适合本项目程度”不是绝对强弱，而是“是否适合被你拿来做 Diffusion MoE + post-training + sampler 研究”。

| 模型 | 参数规模 | Active 参数 | 是否 MoE | 开源权重 | 是否支持官方/公开微调 | 官方/公开代码 | 基准与质量信号 | 推理速度信号 | 训练/微调难度 | 适合程度 | 来源 |
|---|---:|---:|---|---|---|---|---|---|---|---|---|
| DiffusionGemma 26B-A4B-it | 25.2B | 3.8B | 是 | 是 | 是，NeMo 有 full SFT 与 LoRA | 是 | 与 Gemma 4 同骨干相比，在 MMLU-Pro、AIME、LiveCodeBench 等明显落后 | RTX 5090 700+ tok/s；H100 1000+ tok/s | 中等偏高；NeMo 建议 8×H100 | **非常高** | citeturn10view0turn21view0turn22view0 |
| Gemma 4 26B-A4B | 25.2B | 3.8B | 是 | 是 | 是 | 是 | 官方 benchmark 显著强于 DiffusionGemma | AR 基线；速度快但非 diffusion 并行范式 | 中等 | 作为 teacher / ceiling 很高 | citeturn10view1 |
| Qwen3-30B-A3B | 30B | 3B | 是 | 是 | 是 | 是 | 官方博客称小 MoE 模型整体很强，是强 AR MoE 参照 | 推荐 vLLM/SGLang，本地生态成熟 | 中等 | 作为 AR student/teacher 基线很高 | citeturn15view0 |
| DeepSeek-V3-0324 | 社区常引用约 671B | 社区常引用约 37B | 是 | 是 | 主要侧重推理部署 | 是 | HF 卡展示 reasoning、coding、中文写作都有明显提升 | 大模型，部署门槛高 | 很高 | 更适合作 quality ceiling，不适合作第一阶段基线 | citeturn15view1turn13search4 |
| LLaDA 8B | 8B | 8B | 否 | 是 | 是 | 是 | NeurIPS 2025 oral；接近 LLaMA3 8B | 速度依赖 sampler/系统实现 | 中等 | 经典 dense dLLM 基线 | citeturn20view1turn23view0 |
| LLaDA-MoE-7B-A1B | 7.03B | 1.4B | 是 | 是 | 主要是研究/二开 | 是 | 官方称 code / math / tool-use 强；与 Qwen2.5-3B-Instruct 接近 | dInfer 推荐 1000+ tok/s | 中等 | **非常高** | citeturn34view0turn17view0 |
| LLaDA2.0-flash | 100B | 6.1B | 是 | 是 | 有 dFactory/FSDP2 信息 | 部分公开 | 模型卡上多项指标接近 Qwen3-30B-A3B | repo 称 up to 535 tok/s；2.1× 加速版本已发布 | 很高 | 作为“远期上限/对照”很高 | citeturn34view1turn9view11 |
| Dream 7B | 7B | 未特别强调 sparse active | 否 | 是 | 是 | 是 | general / math / code 全面提升，强于更早 diffusion 基线 | 中等 | 中等 | 适合作第二基线 | citeturn17view1turn9view1 |
| Dream-Coder 7B | 7B | 未特别强调 sparse active | 否 | 是 | 是 | 是 | LiveCodeBench pass@1 21.4%，是开放 diffusion code 模型强基线 | 中等 | 中等 | **对 code/repair/infill 极高** | citeturn9view2 |

从这个表里可以看出一个很关键的事实：**今天真正“可工程化启动”的 Diffusion MoE 路线只有两条半。** 一条是 DiffusionGemma；一条是 LLaDA-MoE / LLaDA2；“半条”是把 Dream/Dream-Coder 与外部 MoE 工程栈耦合起来。前两条分别代表 Google 的工业级 block diffusion 路线与 InclusionAI 的开源 dLLM-MoE 路线。citeturn9view12turn34view0turn34view1

### 质量差距到底来自哪里

**不是“MoE 不行”，而是 objective、sampler 与数据一起拖后腿。** LLaDA-MoE 和 LLaDA2.0-flash 的存在本身就说明 MoE 可以帮助 diffusion 提升 capacity/efficiency；但 DiffusionGemma 与 Gemma 4 同骨干对比时仍明显落后，说明把 backbone 换成 diffusion 之后，损失主要不在 backbone 参数量，而在生成目标与推理算法。citeturn10view0turn10view1turn17view0turn34view1

**第一个瓶颈是 factorization barrier。** 并行预测多个 token 时，很多 dLLM 仍以位置独立的边缘分布近似联合分布；这在数学推理、代码、结构化生成中尤其吃亏，因为这些任务的 token 依赖高度耦合。*Breaking the Factorization Barrier in Diffusion Language Models* 直接把这件事定性为结构性失配，而不是简单“模型不够大”。citeturn35search1turn35search5

**第二个瓶颈是 training–inference mismatch。** 训练时 full-sequence/noised context，推理时却常常变成 fixed-block semi-AR、启发式 commit、固定 remask 规则。Deferred Commitment、Variable-Size Self-Contained Blocks、Learning Unmasking Policies 等工作都在试图修这个缝。也就是说，很多质量损失其实发生在 decoder/scheduler，而不完全发生在 backbone。citeturn31search14turn31search5turn31search6

**第三个瓶颈是 post-training 生态滞后。** AR 模型已经拥有大量成熟的 SFT、DPO、GRPO、PRM、verifier、tool-RL recipe；Diffusion LLM 直到 d1 和 TraceRL 出现，才真正把 RL 与 process supervision 系统接上。这个空档意味着 diffusion 模型即便有很强 base 能力，也常常缺少针对 reasoning/code 的高强度后训练。citeturn20view2turn20view0turn29search0turn29search1

**第四个瓶颈是数据形态不匹配。** AR 蒸馏数据通常是 `prompt -> final answer` 或 `prompt -> CoT -> final`；但 diffusion 更适合看到“被扰动的答案、损坏的草稿、局部错误的 reasoning、需要修复的 JSON / code span、显式 critique -> revise -> final 轨迹”。DreamOn、DiffuCoder、CodeForce-SAGA、JSONSchemaBench 之所以重要，不是因为它们“更大”，而是因为它们的 supervision 更像 diffusion 的逆过程。citeturn19search3turn17view5turn26search17turn26search3

### DiffusionGemma 为什么快，又为什么可能弱

DiffusionGemma 的快，官方解释得非常直接：AR 模型的瓶颈常在 memory bandwidth，而 block diffusion 可以一次并行处理 256-token canvas，把瓶颈转成 compute，并更充分利用 GPU tensor cores；同时它基于 Gemma 4 的 26B/3.8B-active MoE，使活跃参数规模仍接近 4B 模型级别。citeturn21view0turn10view0turn10view1

但它可能弱，也同样有很清楚的证据链。第一，官方 benchmark 里与 Gemma 4 同骨干相比存在明显质量差距，尤其是 AIME、GPQA、LiveCodeBench、BigBench Hard、MMMU Pro 等。第二，官方模型卡对用途的描述更偏向内容生成、聊天、总结、图文理解、研究/教育，而其限制部分明确提到高复杂度任务、事实准确性、常识、细微语言现象仍可能受限。综合起来看，它更像一个**高吞吐、低延迟、可本地部署、适合 edit/repair/structured generation 的实验性开源模型**，而不是现成的 reasoning/coding 统治者。citeturn10view0turn33view0turn33view1

因此，对你的项目来说，**DiffusionGemma 最合理的目标不是“一步到位追平 Qwen/DeepSeek”，而是先把它推到在某些任务子域里接近甚至超过同 active-parameter AR MoE 的质量—速度 Pareto frontier。** 最可能做到这一点的子域，不是自由形式长篇推理，而是 code repair、code infilling、JSON schema constrained generation、tool-call formatting、局部事实修复、文档改写与多轮草稿修订。citeturn21view0turn19search3turn26search3

## Jackrong Migration Plan

Jackrong 路线的优点是把 **数据蒸馏 → SFT / LoRA / QLoRA → reasoning 数据整理 → GRPO / GSPO 等 post-training → 可复现开源工程** 串成了一条很实用的流水线。这个结构本身不需要推翻；要改的是 **样本格式、损失目标、采样接口、奖励定义**。Jackrong 仓库当前就明确覆盖了 SFT、GRPO、GSPO、数据蒸馏与本地部署等组成件，因此你真正需要做的是“把同一条工程路线变为 diffusion-aware”，而不是另起炉灶。citeturn11search7turn11search0

### 迁移总原则

**原则一：teacher 仍然以强 AR MoE 为主，student 先不要自己预训练。** 最实际的 teacher 是 Gemma 4 26B A4B、Qwen3-30B-A3B、甚至更大但只做离线蒸馏的 DeepSeek-V3；student 则先用 DiffusionGemma 或 LLaDA-MoE。这样你既继承了 Jackrong 擅长的数据蒸馏路线，也避免了从零训练 dLLM 的巨大成本。citeturn10view1turn15view0turn15view1turn11search7

**原则二：先把 SFT 样本改造成 diffusion-friendly 监督，而不是急着上 RL。** d1 的结果已经说明，masked SFT 本身就能显著提升 reasoning；TraceRL 也表明 trajectory 信息很重要。换言之，第一阶段更像是“让 student 学会如何修”，第二阶段才是“让 student 学会如何选修复轨迹”。citeturn20view2turn20view0

**原则三：把 GRPO/GSPO 的“action”从 next-token 改写成 trajectory / commit / denoise decision。** 对 diffusion 来说，一个自然的 MDP 单位不是单 token，而是一步 denoising 后的 whole-canvas state、被 commit 的 token 子集、或者 block boundary / remask policy 的选择。d1 的 diffu-GRPO、TraceRL、DiFFPO 都沿着这个方向在做。citeturn20view2turn20view0turn20view3

### 数据集建议

下面给出一个面向你项目的“优先做、而且能真正喂给 diffusion”的数据集表。评价标准不是纯下载量，而是与你的任务适配度。

| 数据集 | 规模 | 类型 | 许可证/可得性 | 为什么适合 diffusion | 适合 Jackrong-style 蒸馏 | 优先级 | 来源 |
|---|---:|---|---|---|---|---|---|
| `AI-MO/NuminaMath-1.5` | ~900k | 数学 CoT / post-training | Apache-2.0 | 适合做 reasoning→repair/noise 变体 | 很适合 | 高 | citeturn24search4turn24search20 |
| `AI-MO/NuminaMath-CoT` | ~860k | 数学 CoT | Apache-2.0 | 可构造 masked reasoning / corrupted final | 很适合 | 高 | citeturn24search0turn24search16 |
| `open-thoughts/OpenThoughts-114k` | 114k | 高质量 reasoning | 开放项目 | math/science/code/puzzles 覆盖广，适合 teacher distill | 很适合 | 高 | citeturn24search1turn24search13 |
| `open-thoughts/AgentTrove` | 1.70M 行 | agent traces | 开放项目 | 非常适合 trajectory / tool-use repair / multi-turn verifier | 适合 | 高 | citeturn26search2 |
| `open-thoughts/OpenThoughts-Agent-SFT-ColdStartForRL-10K` | 10k | 冷启动 agent SFT | 开放项目 | 非常适合作为 diffusion tool-use 冷启动格式数据 | 适合 | 中高 | citeturn26search14 |
| `openai/gsm8k` | 8.5k | 数学 reasoning | 开放 | 小而干净，适合作基线和 sanity check | 很适合 | 高 | citeturn24search2turn24search10 |
| `opencompass/CodeForce_SAGA` | 未在片段给出精确行数 | code self-correction | 开放 | 名字就指向 Self-Correction-Augmented，天然适合 repair traces | 很适合 | 高 | citeturn26search17 |
| `loubnabnl/humaneval_infilling` | 1033/5815/1640/164 任务 | code infilling | 开放 | 直接契合 infill diffusion | 可用于蒸馏与评估 | 高 | citeturn25search1 |
| `bigcode/santacoder-fim-task` | 4,792 | fill-in-the-middle | 开放 | 适合训练 bad-span→fixed-span | 适合 | 高 | citeturn25search2 |
| `epfl-dlab/JSONSchemaBench` | ~10k schema | structured JSON | 开放 | structured output / schema repair 的天然 benchmark | 适合 | 高 | citeturn26search3 |
| `BitAgent/bfcl_shuffle_full` / BFCL | 评测集 | tool calling | 开放 | 适合 tool-call formatting 与 verifier reward | 适合 | 中高 | citeturn24search7turn24search3 |
| `openbmb/UltraFeedback` | 64k prompts / 256k samples | preference | 开放 | 可做 verifier / preference model，不直接做 diffusion SFT | 适合偏后阶段 | 中 | citeturn25search3 |
| `bigcode/the-stack-v2-dedup` | 3B+ files | code pretraining | 需遵守使用条款 | 适合做 continued pretraining / domain adaptation，不适合第一阶段 | 一般 | 低 | citeturn25search0 |

### 三种建议数据格式

最重要的不是再多收集多少数据，而是把现有 Jackrong 样本转换为更适合 diffusion 的 supervision 形式。

**普通 SFT**

```json
{"messages":[
  {"role":"system","content":"You are a helpful assistant."},
  {"role":"user","content":"Solve: If Alice has 12 apples and gives away 5, how many remain?"},
  {"role":"assistant","content":"Alice has 7 apples remaining."}
]}
```

**Repair SFT**

```json
{"prompt":"Write a valid JSON object for a flight booking request.",
 "bad_draft":"{destination: 'Tokyo', depart_date: '2026-07-01', passengers: two}",
 "critique":"Keys must be quoted, strings must use double quotes, and passengers must be an integer.",
 "target":"{\"destination\":\"Tokyo\",\"depart_date\":\"2026-07-01\",\"passengers\":2}"}
```

**Diffusion Denoise SFT**

```json
{"prompt":"Implement a Python function that returns the factorial of n.",
 "corrupted_target":"def factorial(n):\n    if n == 0:\n        return 0\n    return n * factorial(n-2)",
 "mask_spans":[[34,53],[66,85]],
 "target":"def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)"}
```

对 DiffusionGemma / block diffusion 更进一步，你可以直接构造 **multi-canvas denoise records**：把最终答案随机切成 256-token canvas，按不同 corruption level 产生多个带噪版本，训练模型恢复 clean canvas。这与 NeMo AutoModel 给出的 DiffusionGemma 训练机制非常一致：uniform-random corruption、self-conditioning、只监督 final response turn、router 冻结。citeturn22view0

### 迁移后的训练路线

第一阶段不是 RL，而是 **Diffusion SFT 三件套**：

1. `prompt -> final` 的普通 SFT，保证模型有基本任务对齐。
2. `prompt + bad draft + critique -> corrected final` 的 repair SFT，注入“修”能力。
3. `corrupted final / partial final / masked reasoning -> clean final` 的 denoise SFT，注入真正贴近 diffusion 的逆过程监督。  
   这三者可以共用 Jackrong 现有的数据清洗、去重、过滤、教师蒸馏框架，只是输出 schema 改了。citeturn11search7turn20view2turn17view5

然后再加两个后处理层：

- **verifier-filtered SFT**：先不用 RL，先让 teacher/verifier 给 training samples 打分，只保留“能过 schema / unit test / exact answer / tool-call validator”的正样本与高价值负样本。
- **trajectory-aware post-training**：如果第一阶段已经观察到 sampler 与 repair data 有收益，再用 d1 / TraceRL 的思想做轻量化 diffusion RL。citeturn20view2turn20view0turn26search3

## Proposed Research Direction and Experimental Plan

### 最推荐的主线

我最推荐的题目主线是：

**Repair-Trace Distillation for Diffusion MoE: 用 AR Teacher 生成 critique-revise-final 与 denoise 轨迹，再结合 verifier-guided sampler，把 DiffusionGemma / LLaDA-MoE 推到 code repair、JSON repair、tool-call formatting 上的高质量—高速度 Pareto frontier。**

这条线最强的地方在于，它同时利用了三件已经被 2025–2026 文献证明有效、但还没有被系统打包的方法：

- AR → diffusion adaptation 是可行的。citeturn37view0turn17view3
- diffusion-aware RL / trajectory-aware post-training 是可行的，但成本较高。citeturn20view2turn20view0
- sampler / commitment policy / verifier 自身就能带来显著提升。citeturn17view7turn17view8turn31search14turn31search1

这意味着你完全可以把项目拆成由浅入深的论文式增量：

- 第一层贡献：数据格式与训练 recipe。
- 第二层贡献：repair/infill 任务上的 diffusion 专用蒸馏。
- 第三层贡献：verifier-guided 或 confidence-aware sampler。
- 第四层贡献：轻量 diffusion-aware RL。  

这比一上来就挑战“开放域 reasoning 追平 DeepSeek/Qwen”现实得多，也更容易写成技术报告、workshop paper，甚至运气好能冲主会 workshop / Findings。citeturn19search3turn20view0turn20view2

### 两条备选线

**备选线一：Task-aware Denoising Schedule。**  
核心问题是不同任务是否应该采用不同 noise schedule / remask policy / block size。DiffuCoder、Saber、Deferred Commitment、Variable-size blocks 的共同信号是：代码、数学、结构化输出的最优采样策略并不相同。这个方向计算更友好，适合硕士阶段做扎实 ablation。citeturn17view5turn17view8turn31search14turn31search5

**备选线二：MoE Routing Analysis in Diffusion Denoising。**  
研究 timestep-aware routing、confidence-aware routing、不同噪声级别专家是否分工不同、router 是否应冻结等。DiffusionGemma 的 NeMo 指南明确建议 SFT 时冻结 router；而你可以把“冻结 vs 仅专家 LoRA vs timestep-conditioned router”作为重点分析对象。这个方向更偏科研，新颖性强，但工程难度也更高。citeturn22view0turn17view0

### 四阶段实验路线

**Stage 0：baseline 与工具链打通**

- 跑通 `google/diffusiongemma-26B-A4B-it` 的本地推理与基线测评。
- 跑通 `inclusionAI/LLaDA-MoE-7B-A1B-Instruct` + `dInfer`。
- 跑通至少一个 AR MoE 对照，例如 `Qwen3-30B-A3B`。  
目标不是刷分，而是先把评测、吞吐、schema validator、unit-test harness 全部打通。citeturn21view0turn34view0turn15view0

**Stage 1：dataset conversion**

把 Jackrong 风格数据转换成三套格式：

- 普通 SFT。
- Repair SFT。
- Denoise SFT。  

优先任务：GSM8K 小样本、HumanEval-Infilling、SantaCoder-FIM、JSONSchemaBench、一个 tool-calling 子集。这样你能很快看出 diffusion 的收益到底出现在什么任务上。citeturn24search2turn25search1turn25search2turn26search3turn24search7

**Stage 2：LoRA SFT**

- DiffusionGemma：先用 NeMo/Unsloth 跑 LoRA。
- LLaDA-MoE：优先用公开推理代码 + 自建轻量 LoRA wrapper；如果太重，先在 LLaDA dense 上验证 recipe。
- 对比 ordinary SFT vs repair SFT vs denoise SFT。  
这里的关键观测不是单一准确率，而是 **速度不变时质量是否提升，或质量不变时 steps 是否下降**。citeturn22view0turn27search4turn34view0

**Stage 3：repair / infill / denoise distillation**

- 用 AR teacher 生成 `bad draft -> critique -> revised final`。
- 对 code 任务生成 failing unit tests + revised solution。
- 对 JSON 任务生成 schema violation explanation + repaired JSON。
- 对 reasoning 任务生成 masked / corrupted rationale，再让 diffusion student 恢复。  
这一步是你最有机会做出独特贡献的地方。citeturn20view2turn19search3turn26search3turn26search17

**Stage 4：sampler / verifier / RL**

先做便宜的，再做贵的：

- 先做：Entropy bound / confidence bound / DCD / Prism / verifier rerank / self-consistency。
- 再做：轻量 diffusion-aware RL，如 d1-style diffu-GRPO 或 TraceRL 的简化版。
- 暂时不要第一阶段就碰 full-scale preference RLHF。citeturn10view0turn17view7turn31search14turn20view2turn20view0

### 推荐实验矩阵

| 变量 | 取值 |
|---|---|
| denoising steps | 8 / 16 / 32 / 64 |
| canvas length | 128 / 256 / 512 |
| remasking policy | random / low-confidence / entropy-bound / deferred-commit |
| confidence threshold | 0.7 / 0.8 / 0.9 |
| entropy threshold | 0.05 / 0.1 / 0.2 |
| verifier | none / schema validator / unit-test / answer checker |
| reranking | none / best-of-4 / best-of-8 |
| self-consistency | 1 / 4 / 8 samples |
| block policy | fixed / variable-size block / task-aware block |
| reward guidance | none / offline filter / light RL |

这个矩阵不是为了一次性全跑完，而是帮助你画出三张 Pareto 图：

- 质量 vs latency
- 质量 vs NFE
- format-validity vs latency  

Saber、Prism、Deferred Commitment、Token-Level Early Stopping、Prophet 等新工作都在强调一件事：**sampler 不是推理细节，而是 diffusion LLM 的核心能力放大器。**citeturn17view8turn17view7turn31search14turn6search5turn6search1

### Benchmark 与评估协议

核心问题应写成一句话：

> 在相同或相近 active parameter 预算下，Diffusion MoE 经由 distillation / repair-SFT / sampler tuning / verifier-guided post-training 后，能否在 code repair、structured generation、tool formatting 上接近 AR MoE，同时保持明显更好的吞吐或更低延迟。  

建议 benchmark 分三层：

**第一层：便宜且可快速迭代**

- GSM8K
- HumanEval-Infilling
- SantaCoder-FIM
- JSONSchemaBench
- BFCL 子集 / tool-call formatting  

**第二层：中等成本**

- MATH / MATH-500
- MBPP / HumanEval
- LiveCodeBench 子集
- Chinese reasoning 子集
- 长上下文 summarization / document repair  

**第三层：最终报告用**

- MMLU-Pro
- GPQA
- AIME subset
- LiveCodeBench 完整版本
- latency / throughput / 显存占用 / NFE / active parameter  

指标必须同时报告：

- accuracy / pass@1 / pass@k
- JSON validity / tool-call exactness
- repair success rate
- verifier score
- latency
- tokens/sec
- denoising steps / committed tokens
- cost / GPU-hours
- Pareto frontier  

这个协议和 DiffusionGemma、LLaDA2.0-flash、Dream-Coder 的官方报告口径是兼容的，也能直接把“快但是弱”转化为“在某类任务上更优的质量—速度权衡”。citeturn10view0turn34view1turn9view2

## Risk Analysis and Final Recommendation

### 风险判断

**算力风险很真实。** 从零训练 Diffusion MoE 基本不适合你当前阶段。LLaDA-MoE 报告约 20T token 训练；LLaDA2.0-flash 走到了 100B/6.1B-active；DiffusionGemma 官方 SFT recipe 也以单机 8×H100 为验证配置。你可以做的是 **LoRA / adapter / continued SFT / sampler / verifier / lightweight RL**，而不是预训练竞赛。citeturn17view0turn34view1turn22view0

**工程风险主要在“框架不统一”。** DiffusionGemma 走 Gemma/Transformers/vLLM/NeMo/Unsloth 生态；LLaDA 系列有自己的推理实现与模型 wrapper；Dream/Dream-Coder 又是一套自己的训练代码。因此第一阶段最忌讳“大一统工程”。你应该先做可独立运行的小实验，再把共性抽出来。citeturn21view0turn34view0turn9view1

**论文撞车风险中等，但不是最高。** “做个更大的 dLLM”“再做个 generic RL for diffusion reasoning”已经很拥挤；而 **repair-trace distillation、JSON/schema repair、tool formatting、task-aware sampler、MoE routing analysis** 仍然相对稀疏，尤其是结合 DiffusionGemma 或 LLaDA-MoE 的系统 recipe。citeturn20view0turn20view2turn31search1turn26search3

**最容易失败的路线，是一上来就追开放域 long-CoT 而没有 verifier。** diffusion 在复杂推理上的收益高度依赖 post-training 与 test-time scaling；没有明确 reward / checker，很容易只得到“会想但不够准”的结果。d1、TraceRL、Prism 的共同经验都是：**要么有可验证奖励，要么有轨迹/自验证机制。**citeturn20view2turn20view0turn17view7

### 最终建议

**这个方向值得做。** 但值得做的不是“Diffusion MoE 很火，我也做一个”，而是把它收缩成一个你能打透的研究问题。综合现有文献、公开模型与仓库生态，我给你的明确建议是：

1. **第一阶段先做什么**  
   先用 DiffusionGemma 或 LLaDA-MoE 跑通 `code repair / code infilling / JSON repair / tool-call formatting` 的 LoRA SFT 与 verifier-filtered SFT；不要一开始做开放域 long-CoT。citeturn22view0turn34view0turn19search3turn26search3

2. **最可能成功的任务是什么**  
   `Code infilling + repair` 与 `JSON/schema-constrained generation` 最可能先做出亮点。Dream-Coder、DreamOn、DiffuCoder 与 JSONSchemaBench 的证据都在同一个方向上：diffusion 的“草稿—重写—修复”归纳偏置与这些任务天然对齐。citeturn17view2turn19search3turn17view5turn26search3

3. **哪些路线暂时不要碰**  
   不要碰从零预训练 Diffusion MoE；不要把 full RLHF / 大规模 preference RL 当成第一阶段；不要一开始就追求在 MMLU-Pro / GPQA / AIME 上全面追平 Qwen3 / DeepSeek。citeturn17view0turn34view1turn20view0turn20view2

4. **如果目标是论文，怎么包装 contribution**  
   最好的包装不是“新模型更大”，而是“**一个把 AR 教师、repair traces、diffusion-aware denoise SFT、verifier-guided sampler 组合起来的低成本可复现 recipe，在 repair/infill/structured-output 上把 Diffusion MoE 的质量推近 AR MoE，同时保持更优 latency/throughput**”。这类贡献对 workshop paper、技术报告、开源项目都很友好。citeturn17view7turn31search14turn20view0

### 论文或技术报告级研究题目

**中文题目**  
**面向修复与结构化生成的 Diffusion MoE 语言模型后训练：基于 AR 教师蒸馏、去噪监督与验证器引导采样的质量—速度协同优化**

**英文题目**  
**Repair-Driven Post-Training for Diffusion MoE Language Models: AR-Teacher Distillation, Denoise Supervision, and Verifier-Guided Sampling Toward AR-MoE Quality**

### 两周最小复现实验计划

| 周期 | 目标 | 交付物 |
|---|---|---|
| 第 1–2 天 | 跑通 DiffusionGemma / LLaDA-MoE 推理，接上测评脚本 | baseline 日志、吞吐脚本、JSON/unit-test validator |
| 第 3–4 天 | 构造 3 套数据：普通 SFT、repair SFT、denoise SFT | 转换脚本、20k–50k 样本数据集 |
| 第 5–7 天 | 跑 LoRA SFT，先在 JSON repair 与 HumanEval-Infilling 小集上看结果 | 第一版 checkpoint、loss 曲线、定性样例 |
| 第 8–10 天 | 加 verifier filtering 与 best-of-k rerank | filtered SFT 对比报告 |
| 第 11–14 天 | 测 8/16/32 steps、不同 remask policy 与 latency | 一张 Pareto 图 + 一页技术备忘录 |

### 六到八周完整项目计划

| 阶段 | 时间 | 核心任务 | 目标 |
|---|---|---|---|
| 基线阶段 | 第 1 周 | 打通模型、评测、validator | 可重复 baseline |
| 数据阶段 | 第 2–3 周 | AR teacher 生成 repair traces / corrupted targets | 拿到高质量 diffusion-friendly 数据 |
| 微调阶段 | 第 4–5 周 | LoRA SFT、repair-SFT、denoise-SFT | 找到最有效的监督组合 |
| 推理阶段 | 第 6 周 | DCD / Prism / verifier rerank / self-consistency | 画质量—速度 Pareto |
| 强化阶段 | 第 7 周 | 轻量 d1-style diffu-GRPO 或 TraceRL-lite | 验证 RL 是否进一步收益 |
| 论文阶段 | 第 8 周 | ablation、可视化、相关工作与写作 | 技术报告 / 投稿初稿 |

### 仓库目录建议

```text
diffusion-moe-research/
  README.md
  docs/
    survey_notes.md
    experiment_log.md
    proposal.md
  configs/
    model/
      diffusiongemma_lora.yaml
      llada_moe_lora.yaml
    data/
      repair_sft.yaml
      denoise_sft.yaml
    eval/
      json_repair.yaml
      humaneval_infill.yaml
  data/
    raw/
    processed/
    teacher_traces/
    verifier_labels/
  scripts/
    convert_jackrong_to_sft.py
    build_repair_pairs.py
    build_denoise_pairs.py
    run_lora_sft.sh
    run_eval.sh
  src/
    data/
    trainers/
    samplers/
    verifiers/
    eval/
    utils/
  notebooks/
    qualitative_analysis.ipynb
    pareto_plots.ipynb
  outputs/
    checkpoints/
    metrics/
    figures/
```

### 适合发给 Claude Code / Codex / Kimi Code 的实现 Prompt

```text
你是一名资深 AI Systems Engineer。请基于一个已有的 Hugging Face / Transformers 工程，帮我实现一个“Diffusion-aware post-training pipeline”，目标模型优先支持：
1) google/diffusiongemma-26B-A4B-it
2) inclusionAI/LLaDA-MoE-7B-A1B-Instruct

请完成以下任务：
- 实现三种训练数据格式：
  A. 普通 SFT：prompt -> final
  B. Repair SFT：prompt + bad_draft + critique -> corrected_final
  C. Denoise SFT：corrupted_target / masked_reasoning -> clean_target
- 数据输入格式统一为 JSONL，可从 ShareGPT/OpenAI messages 转换
- 保留可插拔 verifier 接口，支持：
  - JSON schema validator
  - Python unit-test runner
  - exact-answer checker
- 实现 LoRA 微调入口，并支持：
  - 训练/验证集切分
  - gradient accumulation
  - bf16
  - wandb 或 tensorboard 日志
- 实现推理实验脚本，支持：
  - denoising steps: 8/16/32/64
  - remasking policy: random / confidence / entropy / deferred
  - best-of-k rerank
  - latency、success rate、format validity 统计
- 输出：
  - 可运行的 train.py / infer.py / eval.py
  - 配置文件样例
  - 一个 README，说明如何复现最小实验
要求：
- 尽可能复用官方模型接口
- 不要写过度抽象的框架
- 先保证小规模实验可跑通，再考虑大规模扩展
- 代码要包含清晰注释、异常处理、日志输出
```

### 适合写 Related Work 的文献分类表

| 类别 | 代表文献 | 你论文里该怎么写 |
|---|---|---|
| Diffusion LLM 总综述 | DLM Survey、Discrete Diffusion Survey、Parallel Text Generation Survey | 交代大图景、研究版图与未解问题 |
| 从零训练的大模型 dLLM | LLaDA、Dream | 说明 dLLM 已能在基础能力上接近同规模 AR |
| Diffusion MoE | LLaDA-MoE、LLaDA2.0-flash、DiffusionGemma | 说明 MoE 已进入 dLLM，但 recipe 仍不成熟 |
| AR→Diffusion 迁移 | DiffuLLaMA/Adaptation、Efficient-DLM、L2D、SDLM | 说明无需从零训，可以继承成熟 AR 模型 |
| 代码/infilling 专项 | DiffuCoder、Dream-Coder、DreamOn | 支撑你先做 repair/infill 的任务选择 |
| RL / Post-training | d1、TraceRL、DiFFPO | 说明 diffusion-aware RL 已存在但仍早期 |
| Sampler / 解码 | Prism、Saber、DCD、Token-Commitment、Unmasking Policy | 突出 sampler 是 dLLM 的核心优化点 |
| 理论与瓶颈 | Factorization Barrier、Provable Acceleration、Commit/Block papers | 说明质量差距来自结构性与推理算法问题 |

### 适合写 Proposal 的摘要

本项目研究如何通过蒸馏、后训练、采样与架构级改造，使 Diffusion MoE Language Models 在保持高吞吐与低延迟优势的同时，尽量逼近主流 Autoregressive MoE LLM 的质量。我们将基于现有开源工程路线，把面向 AR LLM 的数据蒸馏、SFT、LoRA 与 RL 配方迁移到 DiffusionGemma 与 LLaDA-MoE 等离散扩散语言模型上。相比直接追求开放域长链推理的全面对齐，本项目聚焦于代码修复、代码填空、JSON 修复与工具调用格式化等更符合 diffusion 生成机制的任务，并引入 repair-trace distillation、denoise supervision 与 verifier-guided sampling，以系统研究 diffusion objective、sampler 与 post-training 数据之间的耦合关系。项目预期交付一套低成本、可复现的 Diffusion MoE 后训练 recipe，并通过质量—速度 Pareto 评估回答一个核心问题：在相近 active parameter 预算下，Diffusion MoE 是否能够在特定任务上逼近 AR MoE 的质量，同时保留显著的推理速度优势。citeturn10view0turn17view0turn19search3turn20view0turn17view7

### 最后一条明确结论

如果你的目标是**做成项目、做出论文、还能真正复现**，我建议你把主线切成一句话：

> **不要先证明 Diffusion MoE 全面追平 AR MoE；先证明在 repair / infill / structured generation 这些 diffusion 天然占优的任务上，通过 Jackrong-style 蒸馏数据改造、repair-trace SFT、以及 verifier-guided sampler，DiffusionGemma 或 LLaDA-MoE 可以把质量显著推近 AR MoE，并形成更好的质量—速度 Pareto。**

这是当前最现实、最有贡献密度、也最适合本科/硕士阶段做出像样成果的路线。citeturn21view0turn34view0turn17view5turn19search3turn20view0turn17view7