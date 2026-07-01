# Diffusion MoE 从第一性原理重建模 —— 研究作战手册

> **本文档是一个独立研究方向的起点，供新 Session（含 GPT 5.5 Pro 协作）接手。** 它是自包含的：不依赖创建它的对话上下文。
>
> 核心问题：diffusion 一定比不过 AR MoE 吗？如果不是，从第一性原理出发，建模/推理范式应怎么演进？
>
> **本手册的任务不是给答案，而是给一组可证伪的假设 + 攻击它们的方法。** 每个论断都标注了"如何质疑 / 如何找反例 / 如何测试"。请把每一条都当成待推翻的对象。

---

## 0. 研究方法论（先定方法，再谈内容）

**五步循环**（每个假设都走一遍）：
1. **质疑**：这个论断的隐藏前提是什么？它在什么条件下为假？
2. **找反例**：构造一个最小的反例（toy 分布 / 退化任务 / 极限参数）。能推翻就推翻。
3. **第一性原理重构**：剥到不能再剥的基本量（信息论 / 概率 / 计算预算），重新推导。
4. **优雅的可微分近似**：把重构出的理想目标，落成一个**可微、可训练、可测**的近似。优雅 = 最少的活动部件。
5. **看结果**：toy 先行，再 scale。结果说话，不为漂亮的故事辩护。

**两个横切原则**：
- **跨领域现象映射**：把 diffusion 的去噪过程，看成**另一个成熟领域的现象**（退火、最优控制、纠错解码、变分推断、不动点迭代……），借那个领域被验证过的工具，而不是从头发明。见 §4。
- **奥卡姆 / 砍冗余**：每引入一个机制，先问"去掉它会怎样"。能砍则砍。当前 diffusion 栈里大量启发式可能是历史包袱，不是必需。

**切入点不止一个**：MoE 头（routing）、SFT（objective/corruption）、RL（trajectory）、Sampling（commitment）——**任何一个都可能是杠杆点**。不要锁死在 MoE 头。见 §5。

**协作分工建议**：GPT 5.5 Pro 适合做 §4 跨领域映射的形式化推导和 §7 反例构造；本方向的实验落地在已搭好的 `diffusiongemma_sft/` 工程线上（baseline 跑通后）。

---

## 1. 第一性原理：两种 generative model 在做什么

任何 LM 都在逼近 `p(x₁,…,x_L)`，区别只在**如何分解 joint**。

### 1.1 AR：精确链式分解
`p(x) = ∏_i p(x_i | x_<i)` —— **恒等式**（chain rule），非近似。无限容量下能表示任意 joint，损失是 exact NLL。代价：严格串行 / 不可回头 / 单向。

### 1.2 Diffusion：mean-field 近似分解
reverse process 每步并行预测时 `q(x_0|x_t) ≈ ∏_i q(x_0^i|x_t)` —— `∏_i` 是**近似**。真实 posterior 各位置**相关**，factorized 丢了相关性 = **factorization barrier**。损失是 ELBO（下界，有 gap）。收益：可并行 / 可迭代修正 / 双向 / 算力可变（K→∞ 退化为 any-order AR）。

### 1.3 关键不对称
AR 把质量锁死在 exact factorization，但**放弃了"用更多算力换更好结果"和"回头修正"的动作空间**。diffusion 反过来。**所以 diffusion 的质量上限不由 factorization gap 决定，而由"能否用可迭代性 + test-time compute 把 gap 补回来"决定。**

> **质疑这一节**：「mean-field 一定有 gap」在什么情况下 gap=0？答：当真实 posterior 本身可分解时（如 token 间真独立）。**反例方向**：构造一个 token 高度耦合的 toy 任务，量化 AR vs diffusion 的 gap 随耦合强度的变化——如果 gap 不随耦合单调增，说明归因错了。

---

## 2. 质量差距三层归因（每层附攻击方法）

把 DiffusionGemma vs Gemma-4 的差距拆三层。**这是待证伪的归因，不是结论。**

### L1 — Factorization barrier（半硬）
- 根源：block 内并行的 mean-field 近似。DiffusionGemma 用 block diffusion 已把它**限制在 256-token block 内**（block 间 exact AR）。
- **质疑**：block 内的 gap 真的是主要矛盾吗？还是 block 边界处理 / self-conditioning 的问题？
- **找反例**：把 block_size 调到 1（退化成 AR）vs 调到 L（退化成纯并行），看质量曲线。若 block_size=1 仍显著差于 AR，则 gap 不在 factorization，归因错。
- **测试**：固定其他，扫 block_size ∈ {1,8,64,256,L}，画质量曲线。

### L2 — Sampling 是启发式而非 learned（**最大空白**）
- 根源：remask schedule / commitment policy / confidence threshold 全是**手工启发式**。
- **质疑**：learned policy 真比好调的启发式强吗？还是只是没调好启发式？
- **找反例**：用一个**极强的 oracle 启发式**（已知答案时的最优 commitment）作上界，learned policy 若摸不到 oracle 的一半增益，说明可学空间小。
- **测试**：oracle-commitment 上界 vs 当前启发式 vs learned policy，三者的质量-NFE 曲线。

### L3 — Post-training 生态不成熟（软，时间问题）
- AR 有成熟 SFT/DPO/GRPO/PRM；diffusion 直到 d1/TraceRL 才接上。纯工程追赶。
- **质疑**：是"生态不成熟"还是"diffusion 的 RL 信号本质更难"？（去噪轨迹长，credit assignment 难）

**当前判断（待推翻）**：L1 已被 block diffusion 缓解，L3 是时间问题，**L2 才是第一性原理能做出新东西的地方**。
> **如何推翻**：若 §2 的 block_size 扫描显示 L1 仍是主因，或 oracle 实验显示 L2 可学空间小，则这个判断错，重排优先级。

---

## 3. 把"过程"形式化：denoising 是一个 MDP

diffusion 的 reverse process 本身是一条 trajectory `x_T→…→x_0`。写成 MDP：

| MDP 元素 | diffusion 对应 |
|---|---|
| state `s_t` | 当前 canvas（部分去噪/masked 的序列） |
| action `a_t` | 这步 commit 哪些位置的哪些 token + 如何 remask |
| policy `π(a_t\|s_t)` | denoiser + commitment/remask 规则 |
| reward `R` | 最终 `x_0` 的质量（verifier / unit-test / exact-match） |
| trajectory `τ` | 整条去噪路径 |

**一旦写成 MDP，整套 policy optimization 机器都能搬过来。** 这是 §5、§6 的基础。

---

## 4. 跨领域现象映射（核心方法：借成熟理论，砍自己的冗余）

**把去噪过程看成别的领域里早被研究透的现象，借它的工具。** 每个映射都是一个潜在的"优雅可微分近似"的来源。

| 把 denoising 看成… | 该领域的成熟工具 | 能借来攻什么 | 砍掉的冗余 |
|---|---|---|---|
| **纠错码迭代解码**（LDPC/turbo） | belief propagation, message passing, bit-flipping with confidence | token commitment = bit decision；BP 比 mean-field 更准 | 启发式 confidence threshold → BP 的 soft messages |
| **变分推断 / mean-field VI** | structured VI, loopy BP, expectation propagation | factorization barrier 就是 mean-field 的已知病；structured VI 直接修 | 位置独立假设 → 结构化后验 |
| **统计物理 / 退火** | Langevin dynamics, simulated annealing, 温度调度 | 噪声级别 = 温度；退火调度理论指导 remask schedule | 手工 schedule → 物理最优退火 |
| **随机最优控制 / Schrödinger bridge** | 最优 control path, HJB 方程 | denoising path = 最优控制轨迹；给 trajectory 最优性判据 | 启发式路径 → 最优控制解 |
| **最优传输 / flow matching** | OT map, 连续性方程 | 噪声→数据的传输；flow matching 已是这视角 | 离散步 → 连续流 |
| **数值不动点迭代 / 预测-校正** | Newton/Jacobi, predictor-corrector ODE solver | 每步去噪 = 一次不动点迭代；PC 方法加 corrector | 纯 predictor → predictor+corrector |

**用法**：选一个映射，问三件事 ——
1. 那个领域里，这个问题的**最优解**长什么样？
2. 它的工具能否落成一个**可微近似**塞进 diffusion 训练/采样？
3. 落进来后，能**砍掉**当前哪个启发式？

> **最有嫌疑的两个**（GPT 5.5 Pro 可优先形式化）：
> - **纠错解码 ↔ commitment**：迭代解码里"先 commit 高置信 bit、用它们帮助解低置信 bit"是几十年优化过的，几乎直接对应 diffusion 的 commitment policy。
> - **structured VI ↔ factorization barrier**：barrier 本质是 mean-field VI 的病，统计物理/概率图模型有现成的 structured 近似，可能比从头设计 corrector 更优雅。

---

## 5. 多切入点（不止 MoE 头）

每个切入点 = 一个可独立攻的杠杆。配归因假设 + 质疑 + 测试。

### 切入点 A：Sampling / Commitment（攻 L2，最大空白）
- **假设**：把 commitment/remask 从启发式升级为 learned policy（§6 的 trajectory RL），是把"近似 gap"换成"refinement gain"的关键。
- **质疑**：refinement 的收益在第几步饱和？是否大部分增益来自前 2 步（那 learned policy 的意义就小）？
- **测试**：质量-NFE 曲线 + oracle 上界（§2-L2）。

### 切入点 B：SFT objective / corruption（攻 L1，且最便宜）
- **假设**：当前 D3PM-uniform corruption（随机 vocab 替换、逐位独立、flat loss 无 1/t 加权）是次优的。corruption schedule 和 loss 加权可能有更优雅的形式。
- **质疑**：uniform 替换 vs absorbing-mask vs structured corruption，哪个更匹配语言的 token 耦合结构？flat loss 真的对吗（NeMo 砍掉了 1/t 加权——是化简还是丢信息）？
- **找反例**：在 toy 上对比不同 corruption kernel 的最终质量，若 uniform 不是最差，说明 corruption 不是瓶颈。
- **测试**：这是**最便宜的切入点**——只改数据/loss，不碰模型，baseline 跑通后能立刻 ablation。
- **跨领域钩子**：corruption = 信道噪声模型（信息论），最优 corruption 应匹配数据的"信道容量"。

### 切入点 C：RL / trajectory-level（攻 L2/L3，对接 GSPO 类比）
- 见 §6。把 GSPO 的 sequence-level importance 升级成 diffusion 的 trajectory-level。
- **质疑**：去噪轨迹比 AR 序列长，trajectory-level importance ratio 连乘会不会方差爆炸？
- **测试**：先测 ratio 的方差量级，再决定要不要 length-normalization / stop-gradient。

### 切入点 D：MoE 头 / diffusion-aware routing（diffusion MoE **独有**维度）
- **假设**：diffusion 的 forward 有一个 AR 没有的维度——**噪声级别 t**。不同 t / 去噪阶段可能需要不同 experts（高噪声=粗规划，低噪声=细填充）。当前 router 对 t 无感知（NeMo 默认 freeze_router）。
- **质疑**：expert 真的会按 t 分化吗？还是 routing 只依赖内容？timestep-aware routing 会不会破坏 load balancing？
- **找反例**：测不同 t 下的 expert 激活分布——若**不随 t 变化**，则 timestep-aware routing 无意义，假设直接死。
- **测试**：(1) 先做激活分析（便宜，不训练）；(2) 若分化，再对比 freeze vs timestep-conditioned router。
- **为什么重要**：这是"为什么研究 diffusion **MoE** 而非 dense diffusion"的核心 differentiator。

---

## 6. RL 类比的形式化（PPO→GRPO→GSPO ↔ diffusion）

**PPO→GRPO→GSPO 的内核**：演进的是 (a) importance sampling ratio 的**粒度**（token→sequence），(b) advantage 的**估计**（value model→group baseline）。

**搬到 diffusion**（基于 §3 的 MDP）：

| 粒度 | RL 对应 | diffusion 含义 | 现状 |
|---|---|---|---|
| token/position | PPO | 每位置 commit 决策一个 ratio | d1 的 diffu-GRPO |
| step/block | ~GRPO | 每 denoising step 一个 ratio | 部分 sampler-RL |
| **trajectory** | **GSPO** | **整条去噪路径一个 importance ratio** | **几乎空白 ← 机会** |

**核心命题（待验证）**：把 GSPO 的 sequence-level importance ratio 升级成 diffusion 的 **trajectory-level ratio**（对整条去噪 path 算一个 ratio + group baseline + verifier reward），是 §5-C 的形式化。TraceRL 摸到"trajectory 信息进 post-training"的边，但**没系统做透 GSPO 式 trajectory-level importance**。

> **第一性原理质疑**：GSPO 用 sequence-level 是因为 reward 是 sequence-level 且 token-level ratio 方差大。diffusion 的 trajectory 比 sequence 更长——**trajectory-level ratio 的方差只会更大**。所以直接搬 GSPO 可能失败。**真问题**：diffusion 上正确的 importance 粒度是什么？也许是 block-level，不是 trajectory-level。**这本身就是一个可发论文的子问题。**

---

## 7. 待证伪假设清单（给测试用，逐条攻击）

把全部论断收敛成可证伪命题。**目标：尽量推翻每一条。**

| # | 假设 | 证伪方法 | 成本 |
|---|---|---|---|
| H1 | 质量差距主因是 L2（sampling 启发式），非 L1 | block_size 扫描 + oracle-commitment 上界 | 中 |
| H2 | block 内 factorization gap 已被 block diffusion 充分缓解 | block_size=1 仍差于 AR ⇒ 推翻 | 中 |
| H3 | learned commitment policy 显著优于调好的启发式 | learned vs oracle vs 启发式 的 NFE-质量曲线 | 高 |
| H4 | D3PM-uniform corruption 次优，存在更优 kernel | toy 上对比 uniform/absorbing/structured | 低 |
| H5 | flat loss（砍掉 1/t 加权）是化简而非丢信息 | 加回 1/t 加权对比 | 低 |
| H6 | MoE experts 会按噪声级别 t 分化 | 不同 t 的 expert 激活分布分析 | 低 |
| H7 | timestep-aware routing 提质且不破坏 load balance | freeze vs timestep-router 对比 | 中 |
| H8 | trajectory-level importance ratio 方差可控 | 测 ratio 方差量级 | 低 |
| H9 | diffusion 在有 verifier 的 refinement 任务上天花板 > AR | 同任务 AR vs diffusion 的 best-of-k / 迭代上限 | 高 |
| H10 | 可迭代修正的收益不在前 1-2 步就饱和 | 质量随 denoising step 的边际增益曲线 | 低 |

**优先做低成本高信息的**：H4、H5、H6、H8、H10 —— 这些便宜、能快速证伪或保留方向，且大多不依赖 RL 基建。

---

## 8. 最有潜力的切口（当前判断，待数据修正）

**D（timestep-aware routing）+ A/C（denoising-as-policy）的组合**：
- D 攻 diffusion MoE **独有**维度，是"为什么是 MoE"的 differentiator，正中"打磨 MoE 头"初衷，且 H6 用便宜的激活分析就能先证伪/保留。
- A/C 攻最大空白 L2，对接 GSPO 类比。
- B（corruption/loss）是**最便宜的热身**，baseline 跑通即可 ablation（H4/H5）。

**一个论文级假设（待证伪）**：
> 在 block-diffusion MoE 上，(1) 让 MoE router 对 denoising timestep 敏感，且 (2) 把 commitment 建模为 trajectory/block-level RL（合适粒度的 importance + group baseline + verifier reward），可在 code-repair / structured-generation 上把质量推近 AR MoE 并保持更优质量-速度 Pareto——且消融显示增益主要来自 learned commitment + timestep routing，而非更大模型。

---

## 9. diffusion 一定比不过 AR MoE 吗？—— 直接回答

**不一定。** 精确地：
- 全面碾压：很难（exact factorization 是 AR 硬优势，dense long-CoT 上 AR 有结构优势）。
- 特定任务族 + 有 verifier + refinement-heavy 场景建立更优 Pareto：现实可达。
- 质量差距可改非宿命：L1 已缓解、L3 时间问题、L2 最大空白。

**一句话**：AR 是"一遍写对"，diffusion 是"反复改对"。**有 verifier 能判对错时，"反复改对"的天花板更高**——因为 AR 没有"回头修正"这个动作空间。前提是学会**怎么改**，而非固定 schedule 瞎改。这就是研究的全部。（此论断 = H9，待证伪。）

---

## 10. 风险与边界条件

- **算力**：方向基于 LoRA + 现有 checkpoint，不预训练，2×48GB 可做小规模验证。
- **依赖 baseline**：建模实验须等 SFT baseline（工程线，见 `STAGE_PROGRESS.md`）跑通——需对照 + 工具链 + 对现有 sampling 的 hands-on 理解。
- **最大失败模式**：无 verifier 就上开放域 long-CoT——无 reward 信号时 refinement 没方向，退化成"会改但不会改对"。**必须先在可验证任务（code/JSON/math）上做。**
- **撞车**：trajectory-diffusion-RL + diffusion-aware routing 组合相对稀疏；"再做个 diffusion RL / 更大 dLLM"已拥挤。

---

## 11. 给新 Session 的交接

- **已有资产**：环境 `dllm`（transformers 5.12.1 + unsloth），模型 DiffusionGemma 26B（96GB 显存可 bf16 加载），全部数据集，16 个参考 repos（含 NeMo 官方 diffusion SFT 实现、dLLM-RL/TraceRL、Prism/DCD sampler）。详见 `STAGE_PROGRESS.md`。
- **SFT 工程线**：`diffusiongemma_sft/`，block-diffusion 训练机制已逐行扒清在 `diffusiongemma-sft-blueprint.md`。baseline 跑通后即可做 §7 的便宜 ablation（H4/H5/H6/H10）。
- **接手方式**：从 §7 的待证伪清单挑低成本项开始（H4/H5/H6/H8/H10），用 §0 的五步循环 + §4 的跨领域映射攻击。**不要先信本手册，先试着推翻它。**
- **GPT 5.5 Pro 协作**：优先用于 §4 跨领域映射的形式化推导（尤其纠错解码↔commitment、structured-VI↔factorization barrier）和 §7 反例构造。
