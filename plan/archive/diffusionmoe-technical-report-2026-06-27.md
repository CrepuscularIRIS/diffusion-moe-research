# DiffusionMOE / DiffusionGemma 技术报告

> 日期：2026-06-27  
> 范围：汇总 2026-06-24（周三）至 2026-06-27（周六）的 DiffusionMOE / DiffusionGemma 研究进程、Arbor 树节点、`plan/` 下当前与归档实验方案、工作树实验结果、已证伪方向、下一步推进计划，以及 `DiffusionGemma.md` 与 `HekaiMing.md` 两份背景文档的路线信息。  
> 关键结论：当前主线已经从“学 commitment + timestep-aware router”连续收缩并重构为 **Verified Wall-Clock Scaling Frontier**：把 frozen DiffusionGemma 视作 verifiable reasoning 的快速 proposal generator，核心问题变为“同一硬件、同一 verifier、同一 prompt 下，dLLM 是否比 matched AR sibling 产生更多 verified correct answers per second”。

---

## 0. 执行摘要

从周三到现在，项目经历了四次实质性重构：

1. **原始主线**：用 learned commitment policy + timestep-aware MoE routing 缩小 DiffusionGemma 与 AR MoE 的质量差距。
2. **第一次重构**：H4 被动 routing 日志不可识别，且 DiffusionGemma router 没有 timestep 输入；Direction C 从“证明专家按 timestep 分化”转为“构造性地添加 t/progress router adapter”。
3. **第二次重构**：发现本地 checkpoint shard 损坏，模型 digit-blind，导致 6/24-6/26 的所有绝对任务结论污染。修复后真实模型在 GSM8K、HumanEval、MBPP、MATH-500 近乎 ceiling，SFT diffusion loss 降低不转化为 accuracy，forward/reference-token 指标失效。
4. **第三次重构**：E（learned budget/commitment allocation）被预注册 rescue audit 干净杀死；A（equivalence-class reference-token non-observability）强形式被 saturation 实验证伪；当前转向 5.8 **Verified Wall-Clock Frontier**。

当前状态不是“没有结果”，而是已经完成了一批高价值的负结果筛选：

- **H4 passive causal claim 死**：timestep / call-index / denoising progress / hidden state evolution 在单 schedule passive logs 中是同一个有序变量，无法区分 timestep specialization 与 progress drift。
- **strong-H4 router reads t 死**：DiffusionGemma MoE router `forward(self, hidden_states)` 没有 timestep/noise/progress 输入。
- **SFT-as-quality-lever 死/降级**：SFT step_1000 diffusion loss 明显下降，但 fixed checkpoint 上 task accuracy 与 pretrained 打平甚至略低。
- **M-PCRH committed-set joint refinement 死**：fixed model 上仍然 coverage_on_base_wrong@16 只有 0.090，`|C_t|>=4` oracle-rescuable 只有 0.006，说明 committed set 不是 joint coupling 的主战场。
- **E learned budget allocator 死**：768→1280 的 rescue phenomenon 真实，但 trace dynamics 无法在 conditional truncation set 内有效预测谁值得加预算。
- **A strong form 死**：2-4% reference-token agreement 是 `t=1.0` 高噪声 artifact；在 sampler 实际 `t∈[0.4,0.8]` 区间，用 verifier-equivalent bank 后 Top10@30 恢复到 0.989（MATH-L5）。

当前仍活跃的主线是：

- **Branch F / node 5.8：Verified Wall-Clock Scaling Frontier**。初步 artifact 显示 DiffusionGemma 在 MATH-L5 上以更低 wall-clock 达到较高 verified solve rate，但 Codex adversarial validation 判定为 **WIN-NEEDS-FIX**：@768 的 dLLM 优势大部分是 AR budget truncation artifact；@1280 frontier 方向可能真实，但必须补齐 full AR@1280、加入 fair high-budget AR@2048 + dLLM@2048、存 full raw generations、修复 audit bug、重跑 bootstrap。

---

## 1. 信息源与证据层级

### 1.1 主证据源

本报告使用下列本地 artifact：

- Arbor canonical tree：`.arbor/sessions/diffusion-moe/.coordinator/idea_tree.json`
- Arbor chronological log：`.arbor/sessions/diffusion-moe/RUNLOG.md`
- 早期队列/归档：`.arbor/sessions/diffusion-moe/archive/{QUEUE.md,BLOCKED.md,review_debt.md,jobs/*}`
- 当前计划：`plan/*.md`
- 归档计划：`plan/archive/*.md`
- 实验输出：
  - `outputs/diffusiongemma_sft_baseline/{run_meta.json,summary.json,loss_log.jsonl}`
  - `.claude/worktrees/agent-a063aedce852d9538/outputs/profiling/*`
  - `.claude/worktrees/agent-a32f81c50e13c165b/outputs/saturation/*`
  - `.claude/worktrees/agent-a8574f53f824af3f1/outputs/rescue_audit/*`
  - `.claude/worktrees/agent-aa411b381a8c95d40/outputs/wallclock/*`
  - `.claude/worktrees/agent-aa3c2553c1f3a181d/outputs/mpcrh_probe/*`
  - `.claude/worktrees/agent-abc568ea35eb43760/outputs/mpcrh_probe/*`
  - `.claude/worktrees/agent-a4607307e978848fb/outputs/h5_*`
- 背景路线文档：
  - `DiffusionGemma.md`
  - `HekaiMing.md`

### 1.2 证据分层

为了避免把污染结果写成贡献，本报告采用三层证据：

| 层级 | 含义 | 是否可作为论文结论 |
|---|---|---|
| A | fixed checkpoint + generation/verifier metric + independent review + raw artifact 可复现 | 可以 |
| B | fixed checkpoint + forward/teacher-forced diagnostic，或 generation 但仍需 fair-control fix | 只能作为诊断/待验证 |
| C | corrupted checkpoint 或 pre-fix 结果 | 只能作为“曾经误导过我们”的过程证据，不能作为模型结论 |

这条分界非常重要。2026-06-26 发现本地 shard 损坏后，所有 pre-fix 绝对结论都必须降级。相对/工具链信息可保留，但不能作为模型能力结论。

---

## 2. 背景路线：从 DiffusionGemma.md 与 HekaiMing.md 读取出的起点

### 2.1 DiffusionGemma.md 的原始判断

`DiffusionGemma.md` 给出的路线不是“从零预训练一个 diffusion MoE”，而是：

1. **以现有开源模型为起点**：DiffusionGemma、LLaDA-MoE、LLaDA2、Dream/Dream-Coder。
2. **任务选择应偏向 diffusion 归纳偏置强的场景**：code repair、code infilling、JSON/schema repair、tool-call formatting、局部修复与 structured generation。
3. **质量差距不是单纯 MoE 问题**：关键瓶颈是 objective、sampler/commitment policy、training-inference mismatch、post-training 生态与数据形态不匹配。
4. **主评价应是质量-速度 Pareto**：accuracy/pass@k/verifier success 与 latency/NFE/wall-clock/token/sec 一起报告。

该文档的核心 proposal 是：

> Repair-Driven Post-Training for Diffusion MoE Language Models: AR-Teacher Distillation, Denoise Supervision, and Verifier-Guided Sampling Toward AR-MoE Quality.

在当前实验之后，这条路线被部分验证、部分重写：

- “repair/infill/structured generation 更适合 diffusion”仍是合理方向，但当前阶段没有直接进入这些任务，因为 fixed model 在 GSM8K/HumanEval/MBPP/MATH-500 已接近 ceiling，真正 headroom 在 AIME/MATH-L5。
- “质量-速度 Pareto”从背景建议上升为当前主线：node 5.8 的 wall-clock verified frontier。
- “verifier-guided sampler / commitment policy”经过 E rescue audit 后被削弱：budget headroom 真实，但 trace dynamics 不足以学出值得写论文的 allocation policy。

### 2.2 HekaiMing.md 的 Kaiming-He 方法迁移

`HekaiMing.md` 将何恺明近期生成模型路线拆为三条思想：

1. **JiT / clean prediction**：让 denoising 真正预测 clean data，而不是 noise/velocity。
2. **MeanFlow / iMF / pMF**：从瞬时速度场改为跨时间区间平均传输，支撑 fewer-step / one-step generation。
3. **ELF / embedding flow**：语言 diffusion 不必死磕 discrete token id，可以在 continuous embedding/logit/simplex 空间做 flow，最后再离散化。

这份文档明确警告：不要直接把 MeanFlow 套在 token id 上。合理路线是三层：

1. **clean-token / clean-embedding audit**：在 frozen DiffusionGemma 上加小 head，比较 standard diffusion loss、clean-token CE、clean-embedding regression + token CE。
2. **ELF-style adapter**：`x_clean = Embedding[token_ids]`，构造 `x_t = α(t)x_clean + σ(t)ε`，训练 `v_θ(x_t,t,condition)` 或 `x0_θ(x_t,t,condition)`，最后 `logits = x0_θ W_embed^T`。
3. **MeanFlow/iMF one-step**：在 embedding space 学 `u_θ(z_t,r,t,prompt)`，从区间平均速度推导少步或一步更新。

当前 Arbor node 5.3 对这条路线的状态是 **DEFERRED — NOT killed**。原因不是理论不成立，而是：

- 当前已验证 headroom 主要是 wall-clock proposal frontier，而不是训练目标本身。
- H5 / SFT 已证明 forward/diffusion-loss 指标可能与 verifier quality 脱节。
- 若要做 Kaiming-He 方法迁移，必须以 generation/verifier 指标约束，而不是只看 diffusion loss。

因此，Kaiming-He 分支应保留为未来 Branch C：

> train toward verifier utility / equivalence-class behavior, not reference CE; 用 continuous embedding flow + clean prediction 作为训练目标迁移的载体。

---

## 3. 数学框架：为什么研究不断 pivot

### 3.1 AR 与 diffusion 的基本分解

AR LM 使用链式法则：

$$
p_\theta(x_{1:L})=\prod_{i=1}^{L}p_\theta(x_i\mid x_{<i}).
$$

这是联合分布的精确分解，代价是严格串行。Block diffusion / discrete diffusion 在每一步 reverse denoising 中更接近：

$$
q_\theta(x_0\mid x_t,c)\approx \prod_{i\in M_t}q_\theta(x^i_0\mid x_t,c),
$$

其中 `M_t` 是当前 noised/masked/corrupted positions，`c` 是 prompt/context。这个并行因式分解引入 factorization barrier：真实 posterior 一般为

$$
p(x_0^{M_t}\mid x_t,c)\neq \prod_{i\in M_t}p(x_0^i\mid x_t,c).
$$

早期手册据此提出 L1/L2/L3 分解：

- L1：factorization barrier
- L2：sampler/commitment policy 是启发式
- L3：post-training 生态不成熟

但 fixed checkpoint 后的实验证据修改了权重：DiffusionGemma 在多个任务已接近 ceiling，最明显的问题不是“不会推理”，而是在 hard tasks 中 **没有在预算内提交 verifier-readable final answer**。这使研究重点从内部 posterior/trace 转向外层 verified candidate frontier。

### 3.2 Verifier equivalence class 与 reference proxy 的失效

对每个问题 `x`，定义 verifier utility：

$$
U_x(y)\in\{0,1\},
$$

可接受答案集合：

$$
A_x=\{y:U_x(y)=1\}.
$$

真正关心的是 sampler distribution `q_{\theta,S}(y|x)` 在 `A_x` 上的质量：

$$
\mathrm{Acc}(x)=\Pr_{y\sim q_{\theta,S}(\cdot|x)}[y\in A_x].
$$

而 reference-token proxy 只对某一个 gold surface `r_x` 评分，例如 teacher-forced argmax agreement：

$$
\mathrm{RefAgree}(x,r_x)
=\frac{1}{|r_x|}\sum_{i=1}^{|r_x|}
\mathbf{1}\Big[
\arg\max_v p_\theta(v\mid \tilde r_{x,t},x,i)=r_{x,i}
\Big].
$$

若 `A_x` 中存在大量 surface forms，则 `RefAgree` 与 `Acc` 可以分离。Branch A 原本试图证明强分离：

$$
G(x)=\mathrm{Acc}(x)-\mathrm{RefProxy}(x)
$$

显著为正，且即使扩展到 verifier-equivalent reference bank 仍无法恢复 observability。

Saturation 结果修改了这个结论：在 `t=1.0` 高噪声 worst-case 下确实 collapse，但在 EntropyBoundSampler 实际 `t∈[0.4,0.8]` 区间，oracle equivalence bank 可以恢复 token observability。因此强 A 不成立，剩余仅是 regime-dependent measurement caveat。

### 3.3 H4 passive logs 的不可识别性证明

H4 原问题：MoE experts 是否按 denoising timestep `t` 分工？

在单 schedule passive log 中，每条 trajectory 有 call index/progress `P`，而 timestep bucket `T` 是 `P` 的确定函数：

$$
T=f(P).
$$

设观测变量 `Y` 是 expert routing decision。任意“timestep specialization”备择模型：

$$
p_1(Y\mid T)=s(Y\mid T)
$$

都存在一个 progress-only null：

$$
p_0(Y\mid P)=s(Y\mid f(P)).
$$

由于 `T=f(P)`，两个模型诱导相同的观测联合分布：

$$
p_1(Y,T,P)=p_0(Y,T,P).
$$

因此任何只基于 passive logs 的检验 `φ(Y,T,P)` 都无法区分二者：

$$
\mathbb{E}_{p_1}[\phi]=\mathbb{E}_{p_0}[\phi].
$$

如果检验在 null 下控制 type-I error：

$$
\mathbb{E}_{p_0}[\phi]\le \alpha,
$$

则对这个 observationally identical alternative 的 power 也满足：

$$
\mathbb{E}_{p_1}[\phi]\le \alpha.
$$

这就是 RUNLOG 与 GPT-5.5 Pro 对 H4 的核心判定：“passive supports only descriptive denoising-stage drift, not causal router reads t.”

尝试 conditioning on progress 也失败，因为 positivity 违反：

$$
\Pr(T=t\mid P=p,\text{track})\in\{0,1\}.
$$

在给定 progress/call-index 后，timestep 没有可比较的变化，因果效应无从估计。

### 3.4 Budget allocation 的离线决策形式化

Rescue audit 定义 cheap budget `B0=768` 与 larger budget `B1=1280`。对每个问题 `i`，观测：

$$
c_i^0=\mathbf{1}[\text{correct at }B0],\quad
c_i^1=\mathbf{1}[\text{correct at }B1].
$$

若策略按 score `s_i` 选择集合 `S_K` 升级到 `B1`，离线 realized accuracy 为：

$$
\mathrm{Acc}(S_K)=
\frac{1}{N}\left(
\sum_{i\in S_K}c_i^1+
\sum_{i\notin S_K}c_i^0
\right).
$$

总 compute 用 NFE 计：

$$
C(S_K)=
\sum_i \mathrm{NFE}_i^0+
\sum_{i\in S_K}(\mathrm{NFE}_i^1-\mathrm{NFE}_i^0).
$$

matched-NFE curve 比较的是相同 `C` 下不同 policy 的 `Acc(C)`，而不是直接比较某一个 K。

v2 进一步定义 conditional truncation set：

$$
\mathcal{C}=\{i:\text{no_box@768}_i\vee \text{hit_cap@768}_i\}.
$$

因为无条件 no_box/hit_cap 接近 trivial oracle，真正问题变成：在 `C` 内，trace dynamics 是否能排序 rescue-positive：

$$
y_i = c_i^1-c_i^0>0.
$$

结论是否定的：trace dynamics ranker 没有显著超过简单控制、string-only/final-only、shuffle control 或 nfe-alone。

### 3.5 Wall-clock verified frontier 的主公式

当前主线把计算单位从内部 trace 改为 completed candidate。给定 wall-clock budget `B`，生成集合：

$$
G_{\le B}(x)=\{y_j:\text{candidate }j\text{ completed within wall-clock }B\}.
$$

Verified success frontier：

$$
S(B)=\Pr_{x\sim D}\left[
\exists y\in G_{\le B}(x):V(x,y)=1
\right].
$$

论文级核心比较是：

$$
\Delta \mathrm{AUC}
=\int_{\log B_{\min}}^{\log B_{\max}}
\left(S_{\mathrm{dLLM}}(e^u)-S_{\mathrm{AR}}(e^u)\right)\,du,
$$

并报告 fixed-accuracy speedup：

$$
\mathrm{Speedup}(a)=
\frac{B_{\mathrm{AR}}(a)}{B_{\mathrm{dLLM}}(a)},
\quad
B_m(a)=\inf\{B:S_m(B)\ge a\}.
$$

Codex 当前要求的 fair-budget 修复，本质是在避免把 AR 截断造成的 no-box failure 误读成 dLLM intrinsic quality advantage。必须在 AR no-box rate 足够低的预算点上重新比较 frontier。

---

## 4. Arbor 树节点完整汇总

Arbor session：`diffusion-moe`。当前 `idea_tree.json` 有 20 个节点。

| 节点 | 状态 | 主题 | 结论/当前处理 |
|---|---|---|---|
| ROOT | pending | Research session | 根节点；结构由 node 1-5 组成。 |
| 1 | pruned | Direction C: timestep-aware routing analysis / H4 | 已被 node 5 supersede。H4 被动证据不可识别；base router 无 t 输入；H5 在 corrupted checkpoint + invalid diffusion-loss proxy 下只保留为诊断。 |
| 1.1 | done | C1 expert-activation analysis harness | 工具链完成，62 tests pass；shared-draw permutation、negative controls、full-pipeline 2x test 均已 harden。 |
| 1.2 | done, score 0.85 | H4 pilot verdict | 最初 29/30 layers significant 只能作为 free-shuffle artifact；GPT-5.5 Pro 证明 passive H4 causal claim 不可识别。 |
| 1.3 | pending | H4 scaled verdict | 旧计划残留。由于 H4 passive design 已退休，不应直接继续；应标记 obsolete 或 archive。 |
| 2 | done | SFT gate | 训练 pipeline 跑通；pre-fix eval 0.0 是 corrupted checkpoint 误导；fixed model 上 pretrained 90% GSM8K，SFT step_1000 88%，SFT 不提升 task accuracy。 |
| 3 | pruned | Direction A learned commitment policy via trajectory RL | 与 SAS / Learning Unmasking Policies / TraceLock 高重叠；后续被重构为 measurement + budget audit，而非原始 RL controller。 |
| 4 | done | Novelty scan | 21 sources / 406 cites；learned commitment 高重叠；explicit t-conditioned router in diffusion language MoE 是窄 novel slice；L2>L1 thesis 必须 soften。 |
| 5 | in_progress | Trunk pivot 2026-06-26 | checkpoint shard 修复后的新树根。所有旧绝对结果污染；真实模型近 ceiling；当前路线从 A/E 转到 wall-clock frontier。 |
| 5.1 | done | Branch A: equivalence-class evaluation | strong form falsified。Saturation 显示 sampler-matched band 下 equivalence bank 恢复 observability。 |
| 5.1.1 | done | Recompute 2.3% under exact D3PM | t=1.0 下 dataset-ref argmax 0.043/0.034 vs verifier 0.90/0.75；core phenomenon real but later证明是 high-noise/worst-case regime。 |
| 5.1.2 | done | Oracle equivalence-class saturation | MATH-L5 Top10@30=0.989，surface recovery falsifier fired；GSM8K bank not saturated且 Spearman@30=0.548。A strong-form falsified。 |
| 5.2 | pending | Branch B: correctness-latency frontier | standalone benchmark 被 demote；现在成为 node 5.8 的 support figure/metric family。 |
| 5.3 | pending | Branch C: Kaiming-He methods | deferred, not killed。未来可做 verifier-utility clean prediction / embedding-flow / MeanFlow-style adapters。 |
| 5.4 | pending | Branch D: verifier-calibrated trace risk | folded into Branch E；不单独 sell。 |
| 5.5 | pruned | M-PCRH committed-set CRF/parity head | fixed model 上 kill survives：committed set coupling headroom太小。不要复活 committed-set joint refinement。 |
| 5.6 | done | Profiling / headroom map | fixed model near ceiling；真实 headroom 在 AIME 73% 与 MATH-L5 83%；主失败模式是 truncation/budget。 |
| 5.7 | done | Branch E budget/commitment method | E method killed。Budget rescue phenomenon 真实，但 trace dynamics ranker 无可发表信号。 |
| 5.7.1 | done | 768-vs-1280 rescue audit | Phase-0 gate pass：rescue+=36, inversions=0, acc@768 0.605→0.838；Phase-1 kill：learned dynamics不胜控制，temporal shuffle ties。 |
| 5.8 | in_progress | Branch F: verified wall-clock frontier | 当前主线。初步 positive 但 Codex 判 WIN-NEEDS-FIX；需 fair-budget rerun 与 raw archival。 |

---

## 5. 时间线：2026-06-24 周三至 2026-06-27 周六

### 2026-06-24：工程与原始研究框架

周三的主要工作是搭建工程基线与研究目标：

- `STAGE_PROGRESS.md` 记录 conda env `dllm`、2×RTX 4090D、torch 2.7.1、transformers 5.12.1、unsloth 2026.6.9。
- `diffusiongemma_sft/` 实现了 D3PM-uniform corruption、response-window collator、block-causal mask、dataset、loss、model_forward、train loop；56 个单测通过。
- `diffusion-moe-first-principles-framing.md` 提出 L1/L2/L3 分解、denoising-as-MDP、H1-H10 假设。
- `research-goal.md` 定义最初 ultimate goal：learned commitment + timestep-aware routing closes gap vs AR MoE。
- `novelty-audit-2026-06-24.md` 提前发现 learned commitment policy 高重叠，Direction C 是较窄但可防守的 novel slice。

当时的核心判断是：先做 C（expert-by-t analysis）→ SFT gate → A（learned commitment）。

### 2026-06-25：H4 统计检验、SFT gate、H4 不可识别性

关键节点：

1. **H4 pilot 先出现 29/30 layers significant**，但 gate 判断不稳。后续大样本 null rerun 发现原 gate failure 部分是 `r_null=200` 的 Monte Carlo artifact。
2. 继续 harden verdict null 后，发现真正问题不是实现 bug，而是 passive logs 的 fundamental identifiability wall：timestep bucket 与 progress/call index 是同一 ordered variable，不能 causal 地归因到 router reads t。
3. GPT-5.5 Pro 给出 t-swap / controlled-direct-effect 方案，但随后 architecture audit 发现 DiffusionGemma router 没有 timestep input，Y01≡Y00，strong-H4 在 base arch 上 vacuous。
4. H5 constructive adapter 被提出：`R'(z,t_r)=proj(z)+g(emb(t_r))`，只训练 router/adapter，冻结 backbone/experts。
5. SFT training 完成 1000 steps，24 min，5 个 LoRA checkpoints，summary：
   - `diff_start_ema=9.7919`
   - `diff_end_ema=4.0652`
   - `ar_start_ema=10.0235`
   - `ar_end_ema=4.5311`
6. 当时 GSM8K dev eval 全 0.0，被误判为 generation harness bug；后续证明这是 checkpoint shard 损坏导致。

### 2026-06-26 上半天：H5、M-PCRH、checkpoint corruption

H5 跑出了 forward-loss positive：

| seed | A content-only | B h+t | D h+mask-ratio | B-A |
|---|---:|---:|---:|---:|
| 42 | 4.708 | 4.300 | 4.290 | -0.409 |
| 123 | 4.676 | 4.299 | 4.279 | -0.377 |
| 7 | 4.684 | 4.251 | 4.267 | -0.432 |

但这个结果后来被降级，原因：

- 它基于 corrupted checkpoint。
- 指标是 held-out diffusion loss，fixed checkpoint 后证明此指标不预测 verifier task quality。
- H5 仍有诊断价值：per-row level signal 确实被 adapter 使用，shuffle/const controls 支持这一点；但不能作为主贡献。

M-PCRH 初始 probe 给出 NO-GO：

- pretrained coverage_on_base_wrong@16 = 0.028
- SFT coverage_on_base_wrong@16 = 0.134
- `OracleRescuable@16(|C_t|>=4)=0.000`
- unary_explains_strict = 0.946 / 0.903

但当时也受 corrupted checkpoint 怀疑。随后 fixed checkpoint 复跑显示 kill survives，但数值有所变化。

同日发现关键 substrate bug：

- `model-00001-of-00011.safetensors` silent corruption。
- 该 shard 保存 `embed_tokens.weight`， tied to `lm_head`。
- 损坏导致 238188/262144 vocab rows 近零，约 91%，包括 digits 与大量 punctuation。
- 修复后验证：`7+5→12`，`12×3→36`，GSM8K dev 3/3。

这一步是整个项目的分水岭：pre-fix 的绝对任务结论全部污染。

### 2026-06-26 中后段：fixed model 后的真实结果与 E/A 重构

fixed model 真实评估：

- pretrained DiffusionGemma：GSM8K exact-match 0.900（54/60 dev）
- SFT step_1000：0.883，和 pretrained 打平
- SFT diffusion loss 大幅改善但无 task gain，说明 diffusion/reference-token loss 是 poor quality proxy
- profiling：
  - GSM8K sanity：100%
  - HumanEval：97.5%
  - MBPP@1280：92.5%
  - MATH-500@1280：93.8%
  - AIME-2024：73%
  - MATH-L5：约 83%
- “thinking mode” 是陷阱：AIME 从 73% 降到 0%。
- 主要 failure mode 是 truncation / early-stop / budget，而不是 reasoning。

基于 profiling，提出 E+A unified：

- A：measurement spine，verifier-defined equivalence class。
- E：method payoff，adaptive answer-commitment / budget allocation。
- D：E 的 trace-risk head。
- B：correctness-compute frontier plot。
- C：Kaiming-He future training，deferred。

### 2026-06-26 晚：Rescue audit 杀死 E

Rescue audit v2 的 primary question 被 Codex 改为 conditional within-C：

$$
\mathcal{C}=\{\text{no_box@768 OR hit_cap@768}\}.
$$

Phase-0 结果：

- MATH-L5 problems = 134
- acc@768 = 0.605
- acc@1280 = 0.838
- rescue-positive = 36（gate threshold 25）
- `|C|=105`
- rescues-within-C = 36
- inversions = 0
- within-C fail fraction 0.776 → 0.288

这说明 budget rescue phenomenon 真实。

Phase-1 结果：

- learned dynamics AUC = 566.89
- random = 587.80
- best fixed-direction control `heuristic_final_entropy` = 604.70
- delta learned - best control = -37.819，95% CI [-83.080, 3.015]
- learned(dynamics+nfe) vs nfe-alone = +21.590，95% CI [-5.335, 53.123]，ties
- full_dynamics - surface_only = +5.838，95% CI [-27.083, 40.350]
- real temporal shuffle ties：real 561.22 vs shuffled best 572.81，delta -11.593，CI [-48.533, 17.653]
- parser baseline clean recovery：MATH 1.9%，AIME 0%

结论：E 作为 learned method 死。正确表述不是“预算没用”，而是“预算 rescue 真实，但 trace dynamics 没有可发表的 selective allocation 信号”。

### 2026-06-26 深夜：A saturation 杀死 strong A

Blocker recompute 首先确认 t=1.0 下 reference collapse 是真实的：

- dataset-ref argmax agreement：
  - GSM8K 0.043
  - MATH 0.034
- verifier accuracy：
  - GSM8K 0.90
  - MATH 0.75
- top-k / probability mass / canonicalization 都没有恢复。

但 saturation phase 发现这是 regime-dependent：

MATH-L5, sampler-matched `t~U(0.4,0.8)`：

| K | Top1@K | Top10@K | BestNLL@K |
|---:|---:|---:|---:|
| 1 | 0.670 | 0.876 | 1.782 |
| 3 | 0.718 | 0.896 | 1.534 |
| 5 | 0.757 | 0.913 | 1.327 |
| 10 | 0.835 | 0.946 | 0.893 |
| 20 | 0.917 | 0.980 | 0.434 |
| 30 | 0.943 | 0.989 | 0.292 |

MATH-L5 verdict：

- bank saturated：late/early=0.137，ΔTop10=0.010
- surface-recovery falsifier fired：Top10@30=0.989 ≥ 0.80
- predictive falsifier did not fire：Spearman 0.209 [0.023,0.384]
- verdict：A-WEAKENED

GSM8K：

- Top1@K1=0.528 → Top1@30=0.843
- Top10@30=0.950
- bank not saturated
- Spearman@30=0.548，predictive falsifier fired
- verdict：INCONCLUSIVE but weakens A。

结论：strong A “verified-equivalence saturation does not recover reference-token observability” 不成立。`t=1.0` 是 sampler 不使用的 worst-case；实际 sampler band 中 oracle bank 恢复了 observability。

### 2026-06-27：Verified wall-clock frontier 成为新主线

GPT-5.5 Pro program redesign 给出新主线：

> Frozen block-diffusion LMs are valuable, if at all, as fast proposal generators for verifier-scaled reasoning.

初步 wallclock artifact：

MATH-L5，当前 VERDICT.md seed filter `[7,42,123]`：

| arm | per-cand acc | pass@all | no-box | serial s/prob | throughput s/prob |
|---|---:|---:|---:|---:|---:|
| ar768 | 0.368 | 0.455 | 0.632 | 22.37 | 9.29 |
| ar1280 | 0.753 | 0.761 | 0.241 | 28.51 | 16.37 |
| dllm768 | 0.560 | 0.664 | 0.418 | 3.76 | 3.76 |
| dllm1280 | 0.801 | 0.896 | 0.124 | 4.72 | 4.72 |

Throughput b1280：

- AUC_dLLM = 3.12
- AUC_AR = 1.60
- delta = 1.52，95% CI [1.40,1.64]
- fixed-acc speedup examples：4.71x, 3.71x, 6.73x

但 Codex validation 判定：

- @768 dLLM win largely AR budget truncation artifact。
- AR parse fails 主要是 no_box at cap，非 parser bug。
- @1280 frontier 方向可能真实，但原 verdict 使用 stale partial AR@1280，raw gitignored，不可完全复现。
- 必须做 fair-budget fix：full AR@1280、AR@2048 + dLLM@2048、raw full storage、analysis bug fix、batch sweep。

---

## 6. 现有实验结果矩阵

### 6.1 SFT baseline

| 项目 | 结果 |
|---|---|
| 训练配置 | DiffusionGemma 26B-A4B, GSM8K train, block_size 256, batch 1, grad_accum 8, LoRA r=16, lr 1.5e-4, max_steps 1000 |
| 训练耗时 | 24.0 min |
| diff EMA | 9.7919 → 4.0652 |
| AR EMA | 10.0235 → 4.5311 |
| checkpoints | step_200, 400, 600, 800, 1000, final |
| pre-fix eval | 全 0.0，无效，checkpoint digit-blind |
| fixed eval | pretrained 90% GSM8K，SFT step_1000 88%，无 task gain |
| 决策 | pipeline 可跑，但 SFT-on-diffusion-loss 不是当前 lever |

### 6.2 H4 / H5

| 项目 | 结果 |
|---|---|
| H4 passive | free-shuffle 29/30 layers significant，但 causal evidence 死 |
| 不可识别性 | `T=f(P)`，passive logs 无法区分 timestep vs progress |
| architecture | base router 无 timestep/noise/progress input |
| H5 pre-fix | B(h+t) 比 A(content) 低约 0.406 nats，real beats shuffle/const |
| H5 fixed status | 未复跑为 task metric；因 corrupted checkpoint + invalid diffusion loss，被 demote 为 diagnostic |

### 6.3 M-PCRH

| 模型/条件 | coverage_on_base_wrong@16 | OracleRescuable@16 overall | OracleRescuable@16 `|C_t|>=4` | 结论 |
|---|---:|---:|---:|---|
| pre-fix pretrained | 0.0281 | 0.0279 | 0.0000 | contaminated but already no-go |
| pre-fix SFT | 0.1344 | 0.1192 | 0.0000 | contaminated |
| fixed pretrained | 0.0897 | 0.0877 | 0.0057 | kill survives structurally |

解释：EntropyBoundSampler committed set 是 confident positions，joint coupling 最弱。真正 coupling 若存在，更可能在 uncommitted high-entropy residual，而非 co-commit set。

### 6.4 Profiling

| Task | Accuracy | 备注 |
|---|---:|---|
| GSM8K sanity | 1.000 | ceiling |
| HumanEval | 0.975 | near ceiling |
| MBPP @768 | 0.825 | 1280 后 0.925 |
| MBPP @1280 | 0.925 | budget improves |
| MATH sample @768 | 0.833 | level 5 0.583 |
| MATH sample @1280 | 0.938 | level 5 0.833 |
| AIME @1280 | 0.733 | 11/15 |
| Thinking mode AIME | 0.000 | truncates thought channel |

### 6.5 Rescue audit

| 指标 | 数值 |
|---|---:|
| MATH-L5 N | 134 |
| acc@768 | 0.605 |
| acc@1280 | 0.838 |
| rescue-positive | 36 |
| inversions | 0 |
| `|C|` | 105 |
| parser clean recovery MATH | 0.019 |
| parser clean recovery AIME | 0.000 |
| learned dynamics AUC | 566.89 |
| random AUC | 587.80 |
| best fixed control | heuristic_final_entropy 604.70 |
| learned - best CI | [-83.080, 3.015] |
| final decision | KILL E |

### 6.6 Saturation

| Task | 主结果 | 决策 |
|---|---|---|
| MATH-L5 | Top1@K1 0.670 → Top1@30 0.943；Top10@30 0.989；Spearman 0.209 | A-WEAKENED，surface recovery fired |
| GSM8K | Top1@K1 0.528 → Top1@30 0.843；Top10@30 0.950；Spearman 0.548 | INCONCLUSIVE but predictive falsifier weakens A |

### 6.7 Wall-clock frontier

| 指标 | 当前结果 | caveat |
|---|---:|---|
| dLLM1280 pass@all | 0.896 | seed-filter artifact; fair rerun needed |
| AR1280 pass@all | 0.761 | AR still truncated at 1280 |
| throughput b1280 AUC delta | +1.52 [1.40,1.64] | likely but not final |
| branch vs deepen | deepen wins | branch_beats_deepen not fired |
| current verdict | WIN-NEEDS-FAIR-BUDGET | not yet final paper result |

---

## 7. 已归档内容与用途

`plan/archive/` 下的内容可分为四类。

### 7.1 工程复现归档

- `STAGE_PROGRESS.md`：环境、数据下载、SFT 工程脚手架、模型下载诊断。当前用途是说明工程起点与早期成功判据。
- `diffusiongemma-sft-blueprint.md`：NeMo DiffusionGemma SFT 的逐行机制拆解，包括 D3PM-uniform corruption、self-conditioning、diffusion loss、encoder AR loss、LoRA targets。当前用途是训练实现参考。

### 7.2 研究框架归档

- `diffusion-moe-first-principles-framing.md`：原始 L1/L2/L3 分解、denoising-as-MDP、H1-H10 假设。当前用途是解释项目如何从第一性原理启动，但许多假设已经被后续证据重排。
- `research-goal.md`：原始 autonomous loop spec。当前用途是历史目标记录；其中 C/SFT/A dependencies 已被 node 5 pivot supersede。

### 7.3 H4 / H5 与 novelty 归档

- `h4-test-protocol.md`：早期 H4 conditional-MI/permutation 设计。
- `h4-confound-gpt55pro-query.md`：向 GPT-5.5 Pro 提出的 H4 identifiability question。
- `h4-tswap-protocol-gpt55pro.md`：passive H4 dead proof 与 t-swap protocol。
- `h4-architecture-verdict-and-pivot.md`：router 无 timestep input 的架构 verdict 与 H5 constructive pivot。
- `novelty-audit-2026-06-24.md`：第一次 prior-art audit。
- `novelty-audit-2026-06-25-interventional.md`：constructive router framing 的 novelty audit。
- `related-work-and-framing.md`：H5 与 EC-DLM/MoDE/TEAM/LLaDA-MoE 的差异化。

这些内容当前的价值是 methodological negative-result 与 related-work differentiation，不再是主实验路线。

### 7.4 M-PCRH 与 ideation 归档

- `ideas-diffusion-moe.md`：ideation pipeline，最终输出 M-PCRH 计划。
- `mpcrh-design-gpt55pro.md`：GPT-5.5 Pro 对 M-PCRH 的 CRF/parity-check formal design。尽管 M-PCRH committed-set 方向被 kill，此文档仍可作为未来 uncommitted residual CRF 或 verifier-oracle variant 的设计素材。

### 7.5 过程/工具归档

- `arbor-cc-plugin-design.md`、`arbor-codex-routing.md`、`arbor-peer-review-refactor-plan.md`、`stophook.md`：Arbor/Claude Code 运行机制、stop hook、review gate、routing policy。当前属于流程历史，不是研究结果。
- `autopilot-distill-fidelity.md`、`cot-distill-fidelity-audit.md`：更早 CoT/distillation fidelity 项目，当前不属于 DiffusionMOE 主线，只提供方法论参考。

---

## 8. 已抛弃 / 已降级方向

### 8.1 抛弃：H4 passive causal claim

原因：不可识别。任何 timestep-specialized alternative 都可以由 progress-only null 完全复现观测分布。

保留价值：descriptive “routing drifts across denoising stage” 可以作为观察，但不能作为 causal router specialization。

### 8.2 抛弃：strong-H4 base router reads timestep

原因：架构上无 t input。router 只有 hidden states，没有 `temb`、`noise_level`、AdaLN、FiLM。

保留价值：base model content-only routing 是一个结构发现；“添加 t/progress 是否有用”仍是可构造实验，但当前不做主线。

### 8.3 降级：H5 t/progress router adapter

原因：pre-fix checkpoint + diffusion loss metric invalid。forward-loss positive 不能外推到 generation/verifier quality。

保留价值：作为未来 training-target 或 router-conditioning diagnostic。若复活，必须用 fixed model + generation/verifier endpoint。

### 8.4 抛弃：SFT diffusion loss 作为成功指标

原因：SFT diffusion loss 大幅下降但 GSM8K exact-match 无提升。reference-token CE / diffusion loss 与 verifier utility 不一致。

保留价值：SFT pipeline 仍可作为工程能力；loss 仅诊断，不作为质量指标。

### 8.5 抛弃：M-PCRH over committed set

原因：fixed model 上 co-commit set oracle headroom 太小。EntropyBoundSampler 接受的是 confident positions，joint coupling 不在这里。

保留价值：uncommitted residual / correctness-oracle / verifier-oriented variant 未被杀死，但必须重做问题定义。

### 8.6 抛弃：Direction A 原始 learned commitment RL

原因：prior art 高重叠，且 fixed evidence 指向 outer-loop budget/frontier，而非内部 token-order RL。

保留价值：revocable commitment 概念可作为 future work，但不是当前 paper center。

### 8.7 抛弃：Branch E learned trace-risk allocation

原因：预注册 rescue audit 证明 budget rescue 真实但 trace dynamics 无可用排序信号。

保留价值：clean negative 可写为 cautionary：within-trace dynamics 不足以支持 selective budget allocation；outer-loop completed-candidate frontier 更合理。

### 8.8 抛弃：Branch A strong equivalence-class non-observability

原因：sampler-matched band 下 verifier-equivalent bank 恢复 token observability；2-4% collapse 是 `t=1.0` artifact。

保留价值：高噪声 teacher-forced probes 会误导；single-reference metrics 有局限，但不能写成强 top-venue 主 claim。

---

## 9. 当前主线：Verified Wall-Clock Frontier

### 9.1 研究问题

当前最清晰的问题：

> Do frozen block-diffusion language models buy more verified reasoning per second than their matched autoregressive siblings?

这不是 sampler 内部机制论文，也不是 likelihood/eval 论文，而是架构级效率-正确性问题：

- dLLM 的真实优势是 parallel 256-token canvas denoising / lower wall-clock。
- AR 的优势是 sequential chain / stronger standard generation path。
- verifier tasks 允许用 completed candidate as compute unit。

### 9.2 当前实验设计

数据：

- Primary：MATH-L5 134 problems。
- Secondary sign-check：AIME-2024 30 problems。

模型：

- dLLM：`unsloth/diffusiongemma-26B-A4B-it` fixed checkpoint。
- AR sibling：`google/gemma-4-26B-A4B-it`。

Arms：

- dLLM branch / deepen，budgets 768, 1280, pending 2048。
- AR branch / deepen，budgets 768, 1280, pending 2048。
- static-N / oracle upper bound as diagnostics。

Metrics：

- `S(B)` verified success vs wall-clock。
- AUC over log wall-clock。
- fixed-accuracy speedup。
- pass@k over unique canonical answers。
- no-box/truncation rate。
- parser/verifier manual audit。

### 9.3 当前未完成的 rigor fixes

Codex 要求必须完成：

1. 完整 AR@1280 full 6 seeds，不能使用 stale partial。
2. 添加 AR@2048 + dLLM@2048，使 AR no-box rate 降到 fair operating point（目标 <10-15%）。
3. 修复 `analyze.py:180` audit gold-field bug。
4. 新 arms 存储 full raw generations，不只存 `gen_tail`。
5. 文档化 AR batch sweep 至 bs32。
6. 从 final data 重新跑 bootstrap 与 verdict。
7. headline 改为 frontier：dLLM 用更低 wall-clock 达到 high verified accuracy；不声称 @768 per-candidate accuracy intrinsic advantage。

---

## 10. 下一步推进计划

### P0：完成 node 5.8 fair-budget rerun

验收标准：

- `outputs/wallclock/` 下存在 full raw JSONL（含 AR/dLLM 1280/2048 full generations）。
- AR@2048 no-box rate 足够低，或者明确说明仍 truncated。
- fixed bug 后重新生成 `VERDICT.md`。
- paired problem-level bootstrap 重新计算 `ΔAUC`、fixed-accuracy speedup、fixed-wall-clock delta。
- 手动 audit 至少 20 pass + 10 parse-fail，确认 verifier 对两模型对称。

若通过：

- 将 5.8 标为 confirmed positive。
- 扩展一个 hard verifiable set：优先 LiveCodeBench 或 OlympiadBench/OlymMATH。
- 写 paper spine：verified success per second, not trace-level policy。

若失败：

- 若 dLLM advantage 在 fair AR budget 消失，则 5.8 kill。
- 进入 P2：Kaiming-He / ELF-style training target，或换 hard task / structured generation。

### P1：同步修正文档状态

当前 `goal-directive.md` 和 `operating-manual.md` 仍写 E+A unified 为 current bet，已经滞后。建议：

- 更新 `goal-directive.md`：current bet 改为 node 5.8 verified wall-clock frontier。
- 更新 `operating-manual.md`：live branch 状态改为 A/E killed, 5.8 active。
- Arbor node 1.3 标注 obsolete/pruned，避免未来误跑 H4 scaled passive verdict。
- 将 `research-redesign-equivalence-class.md` 标为 superseded by `research-redesign-verified-wallclock-frontier.md`。

### P2：保留但暂不启动 Kaiming-He Branch C

如果 5.8 confirmed，可以把 Kaiming-He 路线作为 future work：

1. clean prediction audit：

$$
\mathcal{L}_{cleanCE}=-\sum_i\log p_\phi(x^i_0\mid x_t,c,t)
$$

对比 standard diffusion loss 与 verifier metrics。

2. embedding-flow adapter：

$$
z_0=E[x_0],\quad z_t=\alpha(t)z_0+\sigma(t)\epsilon,
$$

训练：

$$
\hat z_0=f_\phi(z_t,t,c),\quad
\ell_\phi=\hat z_0 W_E^\top.
$$

3. MeanFlow/iMF average transition：

$$
u_\phi(z_t,r,t,c)\approx \frac{z_t-z_r}{t-r}
$$

并以 few-step verified generation 为最终指标。

但启动条件必须是：generation/verifier endpoint clear，不能再只看 reference-token loss。

### P3：归档负结果为论文素材

即使 5.8 positive，负结果也应保留为 motivation/appendix：

- H4 passive不可识别：说明内部 trace probes 容易 confound。
- E killed：说明 within-trace dynamics 不能支撑 selective compute。
- A strong falsified：说明 high-noise teacher-forced metric 会制造假 pathology。
- M-PCRH killed：说明 committed confident set 不是 joint coupling 的主战场。

这些负结果共同支持 5.8 的问题定义：completed verifier-checkable candidate 才是合理 compute unit。

---

## 11. 可写成论文的当前叙事

### 11.1 主叙事

标题候选：

> Do Diffusion Language Models Buy More Verified Reasoning per Second?

核心 claim：

> For verifiable reasoning, a frozen block-diffusion LM should be evaluated as a fast proposal generator. The relevant frontier is verified success vs wall-clock under a matched AR sibling control, not internal trace likelihood or reference-token denoising metrics.

### 11.2 论文结构

1. Introduction：AR sequential correctness vs dLLM parallel proposal generation。
2. Pitfalls：为什么 trace-level metrics/commitment policies/reference-token probes 误导。
3. Method：matched-family wall-clock frontier protocol。
4. Experiments：MATH-L5/AIME + hard set；dLLM vs AR sibling；branch vs deepen。
5. Diagnostics：no-box/truncation, unique answers, parser audit, batching fairness。
6. Negative results appendix：H4, E, A, M-PCRH。
7. Future work：ELF-style clean prediction / MeanFlow adapters toward verifier utility。

---

## 12. 结论

截至 2026-06-27，DiffusionMOE 项目已经从“做一个 learned sampler/router 方法”转为“定义并验证 block-diffusion LM 在 verifiable tasks 上的真实优势：verified correct answers per wall-clock second”。这不是简单换题，而是由一系列预注册 falsifier 推动的收缩：

- routing causal probe 不可识别；
- router 无 t input；
- SFT loss 不代表 quality；
- trace dynamics 无法预测 budget rescue；
- equivalence-class non-observability 强形式被 fair regime 证伪；
- committed-set joint refinement 无 headroom；
- 真正剩下的正向信号是：DiffusionGemma 可能作为快速 proposal engine，在相同硬件上用更短时间产生 verified correct candidate。

下一步的关键不是再提出新想法，而是把 node 5.8 fair-budget 复跑做干净。若 2048 fair-budget 下 dLLM 仍有明确 frontier AUC / fixed-accuracy speedup，项目第一次拥有 top-venue-shaped positive。若该优势消失，应该果断 kill 5.8，并把现有负结果整理成 honest negative-results synthesis 或转向 Kaiming-He/ELF-style training target。

