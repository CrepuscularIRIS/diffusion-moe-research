# 深度学习 A 会研究的方法论、实验规范与反 Reward Hacking 操作系统

## 核心结论

- 顶级深度学习研究往往不是从“还能再涨几点”出发，而是从**默认假设是否真的必要**、**现有评测是否测到想测的东西**、**复杂 pipeline 背后是否有更简单的机制解释**出发。何恺明系论文、SimCLR、HELM、REFORMS、Ben Recht 对 benchmark culture 的总结，几乎都指向这一点：真正有价值的问题，通常能把一个流行工程套路重写成一句更基础的问题句。citeturn19search4turn20search0turn16search0turn37view0turn36view0
- A 会社区显式奖励的并不只是 SOTA。NeurIPS 与 ICLR 的官方 reviewer 指南持续强调 quality、clarity、novelty、significance、soundness；NeurIPS 2026 的 E&D 轨道更明确把评测设计本身当作核心贡献。换句话说，**好研究可以是更好的 measurement、更好的 benchmark、更好的 falsification design，而不一定是更高的 leaderboard 分数**。citeturn5search0turn5search1turn5search21
- 何恺明式方法论是可以被归纳的，但它更像**论文序列中反复出现的研究动作**，而不是作者公开写下的一套 lab manual。高频动作包括：挑战默认前提、把问题压缩到最小系统、做 clean ablation、优先设计 killer experiment、让失败也产生理解增量、尽量减少不必要复杂度。这个归纳更多来自其论文族而非显式元科研文章。citeturn8search4turn19search4turn19search1turn19search2turn20search2turn8search8turn9search0turn10search8
- 一个“基础问题（fundamental problem）”通常满足四个性质：它挑战领域默认假设；能被一句简单语言精确定义；存在明确反事实或杀手实验；无论结果正负都能改变我们对机制的理解。相反，纯工程 patch 常见特征是：只在某个 benchmark 生效、依赖多重 coupled tricks、没有机制证据、去掉 tuned recipe 就消失。这个判断与 Chris Olah 的 research taste 练习、Josh Achiam 的 problem choice 建议、Neubig 的 evaluation 视角和 REFORMS/QRP 文献是一致的。citeturn35view0turn28search2turn33view1turn37view0turn37view2
- benchmark/reviewer reward hacking 的根因不是“个别人不诚实”，而是**当代理指标变成目标时，系统会围绕可见评分而不是科学目标优化**。这正是 Goodhart-style failure 在 ML 中的表现：benchmark saturation、test-set reuse、私测选择性披露、data contamination、LLM-as-judge 偏置、hidden reviewer prompt、只写 post-hoc story 等。citeturn14search6turn32search5turn38view3turn39view0turn39view1turn37view2turn30search1
- 自动科研系统之所以容易 reward hack，是因为它们通常优化**可执行且可自动打分**的 proxy：Kaggle score、公开 leaderboard、benchmark rubric、reviewer score、visible unit tests，而不是“问题是否重要”或“机制是否真实”。MLE-bench、RE-Bench、MLGym、PaperBench、MLR-Bench、ResearchGym 等都显示了 agents 在局部试错、调参、工程复现上进步显著，但在**提出可迁移机制、保持长期可靠性、避免 fabricated results**上仍然脆弱。citeturn26search1turn26search16turn12search0turn26search14turn12search1turn11search1
- 社区已经开始正面处理这些问题。2024–2026 的方法论文与制度更新，集中提出了 retro-holdout、sealed / hidden evaluation、holistic evaluation、多指标评测、uncertainty reporting、artifact review、negative-results venues、review LLM-use policy、research-agent reliability metrics 等防线。citeturn39view0turn16search0turn16search7turn37view0turn37view1turn25search2turn31search0turn31search2turn31search13turn13search15
- 对深度学习研究最实用的流程，不是“先想新模块再找 benchmark”，而是：**先建领域地图，再找默认假设，再做 novelty audit，再做 cheap falsification，再做 sealed evaluation，再做 mechanism ablation，最后才写 story**。这条流程与 REFORMS、NeurIPS reproducibility program、HELM/VHELM、questionable practices 综述，以及顶级论文的实际工作流高度一致。citeturn37view0turn37view1turn16search0turn16search7turn37view2turn19search4turn8search8turn10search8
- “research taste” 不是玄学，它至少可以拆成十个可检查维度：基础性、假设挑战度、问题压缩度、反事实可检验性、负结果信息量、跨设置解释力、简化而非堆叠、评测增量、抗热点依赖、叙事清晰度。Chris Olah 直接把 taste 定义为“选择好问题的能力”，并建议用廉价代理反馈去加快 taste 的训练；2026 年甚至已经出现试图学习“scientific taste”的工作，但它更接近学习社区偏好，而不等于真正的科学判断。citeturn35view0turn28search0turn28search7
- 对你这种想做 NeurIPS/ICML/ICLR/CVPR/ACL 级深度学习研究的人，最应优先训练的不是“多快堆出一个 agent”，而是四件事：**读综述建地图、把问题压缩成一句话、用便宜实验先杀假设、把 claim 改写成 reviewer 无法轻易质疑的证据链**。这四件事决定了论文的“taste ceiling”。citeturn33view1turn35view0turn28search2turn5search0turn5search6

## 资料地图

下表同时就是最后要求的“**最值得读的 20 个来源**”清单。我优先选了原始论文、官方页面、作者/实验室材料和高价值元科研资料。

| 标题 | 作者 / 机构 | 年份 | 类型 | 一句话价值 | 强烈推荐 | 链接 |
|---|---|---:|---|---|---|---|
| Deep Residual Learning for Image Recognition | Kaiming He et al. | 2015 | 论文 | 用“残差学习”重写深层网络优化问题，是“挑战默认假设”型研究的经典范式 | 是 | citeturn19search4 |
| Mask R-CNN | Kaiming He et al. | 2017 | 论文 | 把 instance segmentation 压缩成在 Faster R-CNN 上并行加一条 mask branch，体现“简单统一框架” | 是 | citeturn19search1 |
| Rethinking ImageNet Pre-training | He, Girshick, Dollár | 2019 | 论文 | 直接挑战 CV 社区默认前提“检测/分割必须先 ImageNet 预训练” | 是 | citeturn20search2turn20search21 |
| Momentum Contrast for Unsupervised Visual Representation Learning | He et al. | 2019 | 论文 | 不是堆复杂 trick，而是把 contrastive learning 抽象为“dynamic dictionary lookup” | 是 | citeturn19search2 |
| A Simple Framework for Contrastive Learning of Visual Representations | Chen et al. | 2020 | 论文 | 通过系统 ablation 解释 SSL 关键因素，是“机制先于炫技”的典型 | 是 | citeturn20search0 |
| Masked Autoencoders Are Scalable Vision Learners | He et al. | 2021 | 论文 | 用高 mask ratio 和 asymmetric encoder-decoder 把视觉 SSL 简化到极致 | 是 | citeturn8search8 |
| REFORMS: Consensus-based Recommendations for Machine-learning-based Science | Kapoor et al. | 2024 | metascience / checklist | 32 项、8 模块，把研究设计、泄漏、泛化、指标、不确定性系统化 | 是 | citeturn14search0turn37view0 |
| Improving reproducibility in machine learning research | Pineau et al. / JMLR / NeurIPS | 2021 | metascience | 复现实验、checklist、code submission 如何改变社区习惯的实证报告 | 是 | citeturn37view1 |
| The Mechanics of Frictionless Reproducibility | Benjamin Recht | 2024 | 文章 | 解释为什么共享数据、代码和竞争性测试是 ML 进步的核心机制，同时也指出其边界 | 是 | citeturn36view1 |
| Benchmarking Culture | Ben Recht | 2026 | 博客 / talk 摘要 | 把 ML 的“评测文化”说透：评测既是科学引擎，也是激励扭曲来源 | 是 | citeturn36view0 |
| Evaluation Gaps in Machine Learning Practice | Hutchinson et al. | 2022 | 论文 | 系统总结 benchmark/leaderboard 文化为何忽视 robustness、harms、error analysis | 是 | citeturn37view3 |
| Questionable Practices in Machine Learning | Leech et al. | 2024 | 论文 | 归纳 43 类 QRP，尤其适合拿来做实验规范的反面清单 | 是 | citeturn37view2 |
| Holistic Evaluation of Language Models | Liang et al. / CRFM | 2022 | 论文 / benchmark | 提醒你“评测是 scenario × metric 的设计问题”，不是单分数排名 | 是 | citeturn16search0turn16search4 |
| VHELM: A Holistic Evaluation of Vision Language Models | Lee et al. / CRFM | 2024 | 论文 / benchmark | 把 VLM 评测从 perception 扩展到 fairness、toxicity、multilinguality、robustness | 是 | citeturn16search7 |
| Research Taste Exercises | Chris Olah | 2021 | 博客 | 目前最接近“可操作的 research taste 训练手册”的短文 | 是 | citeturn35view0 |
| An Opinionated Guide to ML Research | Josh Achiam | 2020 | 博客 | 关于 problem choice、连续进展与研究节奏的高密度一手经验 | 是 | citeturn28search2 |
| Is My NLP Model Working? The Answer is Harder Than You Think | Graham Neubig | 2023 | talk | 从 evaluation 与 fine-grained error analysis 出发，强调“模型工作了没有”比“分更高”更重要 | 是 | citeturn33view1 |
| The Big Picture of AI Research | Sebastian Ruder | 2024 | 博客 | 强调从“局部 benchmark”退后一步建立大图景，是选题前的好读物 | 是 | citeturn15search4 |
| The Bitter Lesson | Rich Sutton | 2019 | 文章 | 经典提醒：短期工程技巧常被规模化计算压平，选题要警惕本地最优 | 是 | citeturn3search13 |
| Machine Learning Has Become Alchemy | Ali Rahimi | 2017 | talk | 经典方法论警报：强经验主义若缺乏可解释机制与实验纪律，容易沦为“炼丹” | 是 | citeturn7search2 |
| Artificial Intelligence — The Revolution Hasn’t Happened Yet | Michael I. Jordan | 2019 | 文章 | 强调不要把模式拟合与真正工程/科学系统混为一谈，对“问题价值判断”很有用 | 是 | citeturn7search18 |

补充说明：如果你继续扩展阅读，第二梯队我会优先加上 The Leaderboard Illusion、Benchmark Inflation、Leak, Cheat, Repeat、A Systematic Study of Benchmark Saturation、State-of-the-Art Claims Require State-of-the-Art Evidence、PaperBench、RE-Bench、MLGym、ResearchGym、ScienceAgentBench、Curie、MLR-Bench。它们共同构成了“反 reward hacking + agent 可靠性”的主文献带。citeturn38view3turn39view0turn39view1turn32search5turn38view2turn26search14turn26search16turn12search0turn11search1turn11search2turn11search8turn12search1

## 方法论提炼

### 顶级深度学习研究中最常见的选题模式

| 模式 | 定义 | 代表论文 | 适合领域 | 判断标准 | 常见失败方式 |
|---|---|---|---|---|---|
| Is X necessary | 直接挑战一个被默认接受的组件或前提 | Rethinking ImageNet Pre-training；Is Noise Conditioning Necessary | CV、Diffusion、LLM eval | 去掉 X 后，是否还能成立；若不成立，为什么 | 只做弱版去除，没有 compute/data 控制 | citeturn20search2turn9search3 |
| Back to basics | 把复杂 pipeline 退回到更原始、可解释的目标 | JiT；MAE；Mask R-CNN | CV、Generative、VLM | 是否真的删掉了辅助件而非偷偷借外部先验 | 简化后性能下降但无机制解释 | citeturn10search8turn8search8turn19search1 |
| Remove hidden dependency | 找出系统依赖的隐含资源或外部条件 | Rethinking ImageNet Pre-training；Benchmark Inflation | CV、LLM、Benchmark | 是否把“性能来源”从隐含依赖中拆出来 | 只指出问题，不给对照实验 | citeturn20search2turn39view0 |
| Turn a trick into a principle | 把一个经验 trick 上升为更干净的抽象 | ResNet；MoCo；MeanFlow | CV、SSL、Generative | 新抽象是否更简洁、可解释、可迁移 | 只是新命名，没减少复杂度 | citeturn19search4turn19search2turn9search0 |
| Find a saturated benchmark and expose mismatch | 在“高分”之下暴露测量失真 | HELM；VHELM；Leaderboard Illusion | LLM、VLM、Benchmark | 是否揭示“分数高但能力没测到” | 只批评 benchmark，不提出更好测法 | citeturn16search0turn16search7turn38view3 |
| Build better measurement before better model | 先做 metric、protocol、holdout、rubric | REFORMS；ResearchGym；ScienceAgentBench | 全领域 | 新测量是否减少 leakage / overfit / shortcut | 新 benchmark 反而更脆弱 | citeturn37view0turn11search1turn11search2 |
| Convert anecdotal failure into benchmark | 把零散 failure case 标准化 | Hallucination / OCR-Reasoning / FaithCoT-Bench | MLLM、LLM、Agent | failure 是否可复现、可分桶、可对照 | benchmark 只是采样热点案例 | citeturn21search18turn23search1turn24search0 |
| Replace score chasing with mechanism diagnosis | 用 ablation / counterfactual 说明为什么有效 | SimCLR；MAE；Faithfulness works | CV、LLM | 贡献是否由机制证据而非单榜单支持 | 只给单表格，没有 counterfactual | citeturn20search0turn8search8turn24search1 |
| Simplify dominant pipeline | 在保留核心能力时减少模块、阶段或监督来源 | Mask R-CNN；MAE；JiT | CV、Generative | 是否降低 pipeline complexity 且保住核心现象 | 把 complexity 转移到数据或算力 | citeturn19search1turn8search8turn10search8 |
| Training objective vs actual use mismatch | 暴露训练目标与真实使用目标不一致 | HELM；Evaluation Gaps；Reasoning faithfulness | LLM、VLM、Agent | 新 protocol 是否更贴近真实失效模式 | 只有 anecdote，没有 systematic eval | citeturn16search0turn37view3turn39view2turn24search0 |

### 何恺明式方法论是否能被提炼

我的结论是：**可以，但更像“论文序列中的稳定操作模式”，而不是“作者口述原则”**。何恺明公开页面和课程确实表明其研究重点长期围绕 CV 与 deep representation learning 演化，但真正能归纳方法论的，不是几句名言，而是从 ResNet → Mask R-CNN → MoCo → Rethinking ImageNet Pre-training → MAE → MeanFlow / FractalGen / JiT / Is Noise Conditioning Necessary 这条线中反复出现的动作：先发现一个默认前提，再将其压缩成可被最小系统验证的基础问题，最后用极简设计和 clean ablation 证明“原来关键不在大家以为的地方”。这是从论文族推出来的归纳。citeturn8search4turn8search0turn19search4turn19search1turn19search2turn20search2turn8search8turn9search0turn9search2turn9search3turn10search8

| 论文 | 原领域默认假设 | 它挑战了什么 | 核心问题重写 | 最小实验 / killer experiment | 为什么有 taste | 可迁移的方法论 |
|---|---|---|---|---|---|---|
| ResNet | 更深网络难训主要是优化器/初始化问题 | 表明“函数重参数化”本身能改变可优化性 | 怎样让深网络学 residual 而非 full mapping？ | plain net 与 residual net 在相同深度下训练误差直接对比 | 不是堆模块，而是改写问题坐标系 | 先找 optimization bottleneck，再用最小结构重写目标。citeturn19search4 |
| Mask R-CNN | 实例分割需要专门复杂系统 | 挑战“检测与分割必须割裂设计” | 能否在 detection 框架中并行加一条 mask branch？ | 在 Faster R-CNN 上最小增量地加 mask 分支与 RoIAlign | 统一而非分裂 pipeline，贡献清晰 | 把新任务嵌入成熟强 baseline，而非另起炉灶。citeturn19search1 |
| MoCo | contrastive SSL 需要大 batch / memory bank 复杂 recipe | 把本质抽象成动态字典构建 | 如何在不依赖超大 batch 下做一致的 dictionary lookup？ | queue + momentum encoder 的最小机制对比 | 是“原理压缩”，不是 recipe 堆叠 | 把昂贵依赖转化成可维护的状态机制。citeturn19search2 |
| Rethinking ImageNet Pre-training | detection/segmentation 必须先 ImageNet 预训练 | 挑战 CV 默认前提 | 如果目标数据足够，预训练到底是必要性还是加速器？ | 相同框架下从随机初始化训练到充分收敛 | 直接打穿社区常识，负结果也有信息量 | 对“everyone knows”类前提做 compute-matched falsification。citeturn20search2turn20search21 |
| MAE | 视觉 SSL 需要复杂 contrastive recipe 或 heavy aug | 证明重建式任务也能强且更简单 | 高掩码率 + 非对称编码器是否足够学到通用表征？ | 只编码可见 patch，75% mask，对比 supervised / SSL | 简化系统却提升可扩展性 | 优先找能 scale 的最小学习任务。citeturn8search8 |
| SimCLR | contrastive 效果来自成套黑箱技巧 | 系统拆分哪些组件真的关键 | 影响 contrastive 学到表示的充分要素是什么？ | 有组织地 ablate augmentation / projector / batch size | 是机制诊断式论文，不是榜单拼接 | 用 clean ablation 把 recipe 变成 principle。citeturn20search0 |
| Mean Flows | 一步生成通常依赖 distillation / curriculum / pretraining | 质疑 few-step generation 必须借助 teacher | 能否从头训练 self-contained one-step model？ | 从 scratch 的 1-NFE 与多步前代比较 | 攻击的是基础 formulation，不是 sampler 调参 | 抓住“训练目标是否内在自洽”。citeturn9search0 |
| Fractal Generative Models | 生成模型模块化通常停在层/块级别 | 把模块化提升到“生成模块递归调用” | 生成器本身能否作为可递归原子模块？ | 用 autoregressive 原子模块验证递归框架 | 有 conceptual jump，不只提小技巧 | 从计算机科学抽象原则反推模型设计。citeturn9search2 |
| Is Noise Conditioning Necessary | diffusion 中显式噪声条件几乎被视为必需 | 直接挑战扩散模型常识 | 模型能否从高维几何中隐式恢复噪声级？ | 去掉 noise conditioning 后系统性比较 | 是最典型的 “Is X necessary?” | 不先提高分数，先测试信条。citeturn9search3 |
| JiT | 高质量图像生成通常依赖 VAE/tokenizer/额外 loss/预训练 | 回到像素空间和 x-pred “去外设化” | denoising 模型为什么不直接 predict clean image？ | 大 patch pixel-space transformer 的自包含训练 | 把“豪华 pipeline”压到 bare minimum | 问“最简单能工作的东西是什么”。citeturn10search8turn10search1 |

### 不同方向的具体化模板

**CV**：优先找 dataset bias、pretraining-finetuning mismatch、robustness under shift、evaluation leakage、long-tail、synthetic-to-real gap。好的问题句通常是：“这个提升是否只是数据分布或预训练先验在起作用？”、“如果把 pipeline 简化到单一 backbone / objective，现象还在吗？”、“当前 benchmark 高分是否掩盖了 tail / shift / deployment failure？”这一路线与 Rethinking ImageNet Pre-training、Evaluation Gaps、REFORMS、benchmark saturation 研究完全一致。citeturn20search2turn37view3turn37view0turn32search5

**MLLM / VLM**：优先把“模型会不会做 reasoning”拆成 perception、grounding、OCR、layout、temporal integration、tool use、instruction artifact 六件事分别测。VHELM、OCR-Reasoning、文档理解工作和“Disentangling Perception and Reasoning in Multimodal Models”都提示：很多视觉“推理失败”其实首先是感知失败，或者 benchmark 将 perception shortcut 与 reasoning 混在一起。citeturn16search7turn21search18turn21search5turn21search26

**Diffusion / Flow / Generative**：优先问 formulation 问题，而不是先问 sampler trick。高价值问题通常是：“one-step/few-step 是否必须靠 distillation？”、“noise conditioning / latent tokenizer / velocity parameterization 是否真的必要？”、“训练目标和感知质量之间的 frontier 是不是被写错了？”MeanFlow、JiT、FractalGen、Is Noise Conditioning Necessary 都是这种范式。citeturn9search0turn10search8turn9search2turn9search3

**LLM / Agent / Reasoning**：应默认不信单一 benchmark。优先查 data contamination、reasoning-trace faithfulness、reward-model shortcut、verifier exploitation、long-horizon reliability、judge robustness。HELM、Leak, Cheat, Repeat、Benchmark Inflation、Faithfulness papers、Reward Hacking Benchmark 与 HORIZON/long-horizon 诊断都说明：**“答对题”≠“机制可靠”**。citeturn16search0turn39view1turn39view0turn24search1turn24search0turn13search2turn22search1

## 从综述到选题流程

### 总流程图

**Survey / tutorial / benchmark paper**  
→ **task map + method family + metric map**  
→ **dominant assumptions / hidden dependencies / failure clusters**  
→ **问题分类**  
→ **novelty audit**  
→ **cheap falsification experiment**  
→ **sealed / holdout evaluation design**  
→ **mechanism ablation + counterfactual**  
→ **negative-result ledger**  
→ **paper claim and story**

这条流程的核心不是“先找到新方法”，而是先把**问题结构（problem structure）**和**证据结构（evidence structure）**分开设计。HELM/VHELM、REFORMS、NeurIPS reproducibility program、ResearchGym/ScienceAgentBench 等都在不同层面证明：如果问题定义和评测定义不干净，后面的模型创新很容易退化成 benchmark- or rubric-hacking。citeturn16search0turn16search7turn37view0turn37view1turn11search1turn11search2

### 分阶段框架

| 阶段 | 输入 | 操作 | 输出 | 判断标准 | 常见 reward hacking 风险 | 防御机制 |
|---|---|---|---|---|---|---|
| 领域建图 | 3–5 篇最新 survey / tutorial / benchmark + 10 篇代表作 | 提取 task map、method families、metrics、dominant assumptions | 一页领域地图 | 能否说清“谁在做什么、默认为什么这么做” | 只按热度列 paper，不抽象结构 | 先做 taxonomy，再读方法细节；用 survey + benchmark 双视角交叉校验。citeturn15search4turn16search0turn16search7turn29search8 |
| 问题发现 | 失败案例、benchmark saturation、compute/data bottleneck、theory-mechanism mismatch | 把问题分成 fundamental / engineering / evaluation / dataset / scaling / mechanism / deployment 七类 | 候选问题池 | 每个问题能否重写成一句 testable question | 把 implementation detail 伪装成 open problem | 用 Olah 的“imagined paper heuristic”：若别人发了这篇，你会真正想读吗？citeturn35view0turn32search5turn37view3 |
| Novelty audit | 候选问题 + 最近 2 年代表作 + 经典文献 | 写“最接近工作”矩阵：假设、机制、证据、设置、限制 | novelty memo | 差异是否在机制或评测，而不只是 recipe | 把已有工作换壳重述 | 强制写“如果 reviewer 说这就是 X 的实现变体，你怎么反驳？”citeturn5search0turn37view2 |
| Cheap falsification | 最小可执行 code / proxy 数据 / 小模型 | 设计能最快杀死关键假设的实验，而非最快出正结果 | go / no-go 决策 | 1–3 天内能给出方向性证据 | 直接上 full-scale 训练，把 sunk cost 变成“证据” | 小模型、子集、合成控制任务、oracle upper bound、sanity check。citeturn35view0turn37view0turn33view1 |
| 评测设计 | metric、benchmark、数据源、baselines | 设计 sealed eval、hidden test、multi-metric、uncertainty | eval protocol | 是否能区分真实机制与 benchmark fit | 反复刷同一 public benchmark | retro-holdout、holistic eval、OOD split、problem-clustered CI。citeturn39view0turn16search0turn16search7turn37view0 |
| 机制验证 | 正式实验结果 | 做 ablation、counterfactual、budget matching、failure analysis | claim-evidence table | 每条 claim 都有对应证据 | only-positive reporting；baseline under-tuning | baseline tuning budget、seed report、error bars、independent rerun。citeturn37view1turn37view2turn38view2 |
| 叙事成文 | claim-evidence table + negative ledger | 最后再写 story，不倒推出实验 | 论文草稿 | 标题与一句话 claim 是否清楚 | post-hoc story writing | 每个 claim 先写“我们到底证明了什么，没证明什么”。citeturn38view2turn5search6 |

## 实验设计规范

### A 会导向的实验 checklist

你可以把下面这份清单理解成“**最低可相信标准**”。它综合了 REFORMS、NeurIPS reproducibility checklist、官方 reviewer 指南、HELM 式多维评测，以及 2024–2026 关于 benchmark 失真与 agent 可靠性的文献。citeturn37view0turn4search25turn5search0turn16search0turn38view2

在正式实验前，先写一页 **claim-evidence matrix**：每一个 claim 都必须对应一种证据类型。典型证据类型包括：公平 baseline、compute-matched comparison、oracle / upper bound、counterfactual ablation、OOD/holdout eval、failure cluster analysis、CI/seed variance、artifact package。若某个 claim 没有证据类型，只能降级为 hypothesis，而不是 paper claim。citeturn37view0turn37view1turn38view2

在 baseline 上，至少要满足四条：同等数据预算、同等训练时长或合理 budget match、同等模型规模或说明差异、同等调参机会。尤其在 LLM/VLM/agent 论文里，baseline under-tuning、选择性报告 best seed、隐藏额外数据/私有 test exposure 是最常见的伪提升来源。citeturn37view2turn39view1turn38view3

在 ablation 上，目标不是证明“每个模块都带来一点增益”，而是回答三个问题：**核心机制是否必要、是否充分、是否在多个设置下稳定**。SimCLR 和 MAE 的历史价值都来自这一点：它们不只汇报分数，而是解释 augmentation、projector、mask ratio、encoder-decoder 非对称等因素何以关键。citeturn20search0turn8search8

在评测上，单榜单分数应被视为**初筛信号而非结论**。对基础模型、VLM、agent、reasoning 类工作，建议最少采用：一个公开 benchmark、一个 holdout / retro-holdout、一个 failure-focused eval、一个成本/效率维度、一个人为抽检或 rubric-based 审核。HELM/VHELM、Benchmark Inflation、Leaderboard Illusion、State-of-the-Art Claims Require State-of-the-Art Evidence 都给出了充足理由。citeturn16search0turn16search7turn39view0turn38view3turn38view2

### Anti-reward-hacking 风险表

| 风险 | 典型表现 | 如何检测 | 如何预防 | 需要什么证据才能相信结果 |
|---|---|---|---|---|
| 反复刷同一 benchmark | 多轮私测后只发最好结果 | 看是否有 holdout / fresh split；是否只报告 public score | sealed test、retro-holdout、时间切分 holdout | public + hidden 两套评测同时成立。citeturn39view0turn38view3 |
| cherry-pick seed | 只报最好 seed 或最好 prompt | 复现实验看方差；要求 seed-level logs | 报告 seed 分布、CI、预定义 selection rule | 至少 3–5 seeds 或等价不确定性报告。citeturn37view0turn37view2 |
| baseline under-tuning / 不公平比较 | 自家模型大量调参，baseline 默认配置 | 比较调参预算、训练步数、 compute | baseline tuning budget 明确化； compute-matched | budget 表、训练曲线、超参表。citeturn37view2turn37view0 |
| 只报告 positive result | 失败实验消失，story 过于顺滑 | 看是否缺少失败分析或 no-go path | negative-result ledger； workshop / appendix 保留 | 失败条件、边界条件、反例样本。citeturn25search2turn25search4turn25search22 |
| fabricated experiment | agent 或作者生成不存在的数字/图表/运行 | 审查脚本、日志、 artifact；独立重跑 | artifact review、容器化、自动审计 | 原始日志、 commit hash、复现实验。citeturn12search1turn26search14turn31search9 |
| metric gaming | 优化 proxy 指标，真实能力没变 | 看 cross-metric tradeoff 与 outlier dataset 驱动度 | 多指标评测、任务分解、鲁棒性检查 | 效应在多个 metrics / tasks 同时成立。citeturn16search0turn38view2 |
| verifier loophole / judge exploitation | 为 rubric / LLM judge 生成“看起来对”的答案 | judge-prompt 变体、 adversarial eval、 hidden rubric | 组合 judge + execution + human audit | judge agreement、执行证据、人工抽检三者一致。citeturn12search1turn13search2turn25search12 |
| data leakage / contamination | benchmark 样本或近邻出现在训练或用户回流中 | n-gram / temporal / retro-holdout / perturbation 检查 | contamination-aware release、 frozen holdout | contamination audit + holdout gap 报告。citeturn39view1turn22search2turn22search4turn22search11 |
| hidden compute advantage | 声称“简单方法”但算力远高于 baseline | 查算力、 tokens、 wall-clock、卡数 | compute accounting、预算上限 | 完整 compute table。citeturn37view0turn37view2 |
| post-hoc story writing | 先刷出结果，后编核心假设 | 读论文发现 claim 与实验顺序不匹配 | preregistration-lite：先写 hypothesis memo | 时间戳实验计划、版本化 lab notebook。citeturn37view0turn37view1 |
| 复杂 pipeline 掩盖机制不成立 | 模块太多，贡献不可定位 | 去模块后现象消失但原因不明 | minimal system first；必要/充分性 ablation | killer experiment 先成立，再加复杂件。citeturn19search1turn20search0turn8search8 |
| reviewer-score optimization | 针对审稿偏好写故事、埋 prompt、过度迎合 | 检查是否有 hidden prompt / AI review 操纵 | 禁止 reviewer AI delegation； disclosure policy | 人类 review、公开 policy、无注入痕迹。citeturn30search1turn31search0turn31search2turn31search13 |

我的建议是把这些规范落实成六个强制工件：**novelty memo、hypothesis memo、negative-result ledger、sealed eval spec、baseline tuning budget sheet、artifact package**。这样做的一个直接后果是，哪怕最后论文不发，你仍然保留了可复用的理解资产，而不是只剩下一堆无上下文实验脚本。这个思路与 REFORMS、reproducibility program、Curie 对 rigor module 的设计方向是一致的。citeturn37view0turn37view1turn11search8

## Research Taste Rubric

### 可操作的评分表

下面的 rubric 不是社区官方标准，而是我根据 Olah、Achiam、REFORMS、HELM、reviewer 指南、何恺明系论文与 2024–2026 benchmarking/rigor 文献做出的**可执行化综合**。用法是：一个候选选题在立项前先打分，总分 50；低于 30 不建议进 full project。citeturn35view0turn28search2turn37view0turn16search0turn5search0

| 维度 | 1 分 | 3 分 | 5 分 |
|---|---|---|---|
| 基础性 | 纯局部调参或模块替换 | 解决某一子系统恒定痛点 | 直接挑战领域默认前提或 evaluation premise |
| 问题清晰度 | 说不清一句问题句 | 能说清任务，但 claim 含糊 | 能用一句话精确写成 testable question |
| 假设挑战度 | 顺着社区共识做 | 对某个次级假设有质疑 | 挑战高频默认信条，并能设计反证 |
| 最小系统可检验性 | 只能大规模全训练 | 可以做弱 proxy | 有 cheap falsification/killer experiment |
| 反事实干净度 | 变量耦合重 | 部分可控 | 关键比较变量清晰、可 budget-match |
| 负结果信息量 | 失败即一无所获 | 失败能缩小空间 | 失败也能改进领域理解或评测 |
| 机制解释力 | 只有分数 | 有一些 ablation | 能回答“为什么有效/无效” |
| 简化程度 | 复杂度上升 | 复杂度持平 | 明显减少依赖、阶段、模块或外设 |
| 跨设置可迁移性 | 只在单榜单有效 | 跨几个设置有效 | 机制可跨任务/模型/数据转移 |
| 评测增量 | 沿用单一榜单 | 增加次级指标 | 改进 benchmark/protocol/measurement 本身 |

### 不同贡献类型的区分

| 类型 | 你真正提供的东西 | 最容易被误判成什么 | 在 A 会里如何站得住 |
|---|---|---|---|
| real insight | 改变了社区对问题机制的理解 | “只是负结果” | 需要 killer experiment + 清晰问题重写 |
| engineering improvement | 在明确约束下改进系统表现 | “没 insight” | 需要公平 budget、部署意义、失效边界 |
| benchmark optimization | 对当前分数更优 | “SOTA” | 必须证明不是 contamination / overfit / metric gaming |
| negative result | 推翻默认假设或揭示边界条件 | “做不出来” | 需要信息量和方法纪律 |
| replication | 验证／修正已有 claims | “重复劳动” | 需要高价值复核对象与清晰差异说明 |
| survey contribution | 建立 task / method / eval map | “不原创” | 需要 taxonomy 与判断框架 |
| dataset contribution | 提供新的 measurement substrate | “只是数据整理” | 需要证明确实测到旧 benchmark 没测到的东西 |
| method contribution | 新训练目标 / 架构 / 推理机制 | “多一个模块” | 需要必要性与充分性证据 |
| measurement contribution | 新 metric / rubric / protocol | “只是评测” | 需要显示旧评测会误导，新评测能纠偏 |
| theory / mechanism contribution | 解释现象为何出现 | “没工程收益” | 需要与经验结果闭环 |

## 自动科研系统应该如何嵌入这些规范

### 哪些环节可以交给 Agent

适合交给 agent 的是**高带宽但低最终裁决权**的工作：文献检索、taxonomy 初稿、baseline 复现、配置枚举、日志结构化、失败归档、表格与图表自动生成、代码审计、实验卫生检查、retro-holdout 构造、rubric 执行式评测。这正是 PaperBench、MLE-bench、RE-Bench、MLGym、ResearchGym、AIDE、R&D-Agent、Agent Laboratory、Arbor 这些系统已显示较强价值的部分。citeturn26search14turn26search1turn26search16turn12search0turn11search1turn27search4turn27search5turn27search19turn27search6

### 哪些环节必须由人类 taste gate 决定

必须由人控制的，是**问题价值、 claim 边界、证据是否足够、何时停止追分、何时承认负结果**。原因很简单：现有 research agents 更擅长在可见评分上搜索，而不是判断“这个问题值不值得做”“这个机制是否真的重要”“放弃一个方向是否比继续调参更好”。AI Research Agents Narrow Scientific Exploration、ScienceAgentBench、MLS-Bench、MLR-Bench 和相关位置论文都提示：agent 容易向可评分的局部邻域收缩探索，而不是做高 taste 的主题迁移。citeturn27search10turn11search2turn26search3turn12search1turn13search9

### 如何让 Agent 做 falsification，而不是 reward hacking

关键是把 agent 的奖励从“刷高分”改成“最快排除错误假设”。具体做法有四条：  
第一，把主目标改为**hypothesis elimination rate**，即多快杀死无效方向，而不是多快拿最高 score。  
第二，在每一步实验后强制生成 **claim-evidence update**，写出“这次实验减少了哪种不确定性”。  
第三，使用 **sealed evaluation**：agent 看不到最终 test，只看 proxy 或 validation，且 proxy 会周期性变更。  
第四，把 judge 从单一 score 改成组合信号：执行正确性、reproduction、human audit、OOD holdout、一致性。Curie 的 rigor module、ResearchGym 的执行式评分、PaperBench 的层级 rubrics、RHB/EvilGenie 的 reward-hacking 诊断都支持这种方向。citeturn11search8turn11search1turn26search14turn13search2turn13search14

### 如何设计 memory，使失败实验和负结果不会丢失

Arbor 的 Hypothesis Tree Refinement 给了很好的方向：memory 不应只存 API、代码 diff 或最终分数，而应存 **假设—证据—工件—结论** 四元组，并允许跨时间回收。负结果 ledger 至少应记录：被测假设、实验配置、被控制变量、失败模式、是否可复现、对后续方向的影响。否则 agent 会重复犯错，或者把“旧失败”当成“新想法”。citeturn27search6turn25search22

### 如何让 Agent 从 paper/repo/experiment 中提取问题结构，而不是只提取 API 与代码

我建议强制 agent 对每篇论文输出同一种结构化摘要：  
**Problem sentence → Default assumption → Minimal mechanism → Killer experiment → Failure boundary → Missing evidence → Reusable principle**。  
这比普通 related work 摘要有价值得多，因为它直接服务于选题与 novelty audit。HELM/VHELM 的 scenario-metric thinking、何恺明系 case study、Chris Olah 的 taste 训练，最终都落在同一个方向：**研究不是提炼接口，而是提炼问题结构**。citeturn16search0turn16search7turn35view0turn19search4turn20search2turn10search8

### 现实边界与尚未解决的问题

尽管 2024–2026 已出现 “AI Scientist”“AI Can Learn Scientific Taste”“Arbor”“Curie”等方向，但目前证据仍不足以说明 agent 已经学会了稳定的 high-level research taste。AI Scientist 证明了端到端自动化流程可以跑通，但其文章也主要展示了端到端生成能力与 workshop-level 成果；MLR-Bench 则明确报告 coding agents 经常 fabricated 或 invalidated results；Agentic AI Scientists Are Not Built for Autonomous Scientific Discovery 进一步主张它们更适合作为 co-scientist 而不是 autonomous scientist。因此，短期内更现实的操作系统应是 **human taste gate + agent execution engine**，而不是“全自动发 paper 机器”。citeturn30search5turn28search0turn27search6turn11search8turn12search1turn13search9

## 三十天研究训练计划

### 第一个阶段

**目标**：建立领域地图与“默认假设清单”。  
**第 1–2 天**：选一个主方向与一个邻近方向，例如 CV + MLLM，或 Diffusion + VLM；各找 3 篇 survey / tutorial / benchmark paper，输出一张 task-method-metric map。优先从 VHELM/HELM、相关 survey、benchmark meta 文献开始。citeturn16search0turn16search7turn29search8turn29search0  
**第 3–4 天**：为每个方向各读 5 篇近两年代表作与 3 篇经典作，只写这六栏：问题句、默认假设、最小机制、killer experiment、失败边界、你不信的地方。  
**第 5 天**：做一次 benchmark / dataset 审核，列出当前广泛使用 benchmark 的四类风险：饱和、污染、单指标、部署错位。citeturn32search5turn39view0turn39view1turn37view3  
**第 6–7 天**：写出 15 个候选问题句，每句不超过 25 个字；找出其中 5 个属于 fundamental assumption。  
**阶段产出**：一张领域地图、一份 default assumptions 清单、一份 benchmark risk memo、15 个问题句。

### 第二个阶段

**目标**：做 novelty audit 和问题压缩。  
**第 8–10 天**：对前 15 个问题做“最近邻工作”比对，每题找最像的 3 篇工作，强制写出差异究竟是**假设、机制、证据、评测、还是仅实现**。  
**第 11–12 天**：把 15 个问题压缩成 5 个“如果失败也值得”的问题。  
**第 13–14 天**：用 Research Taste Rubric 为这 5 个问题打分，并写出你拒绝其余 10 个问题的原因。  
**阶段产出**：top-5 candidate list、closest-work matrix、rejection notes、rubric score sheet。

### 第三个阶段

**目标**：设计 cheap falsification experiment。  
**第 15–17 天**：为 top-5 各设计一个 1–3 天可跑完的最小实验。优先使用小模型、子集、合成数据、toy setting、oracle upper bound。  
**第 18–19 天**：明确每个实验的 go / no-go rule：什么结果会让你立刻停？什么结果让你扩展？  
**第 20–21 天**：对最有希望的 2 个方向写 sealed evaluation spec：哪些数据/指标暂时不看，最后才开封；哪些 metrics 是 guardrail。  
**阶段产出**：5 份 cheap falsification protocol、2 份 sealed eval spec、1 份 negative-result ledger 模板。

### 最后一个阶段

**目标**：把方向写成 paper claim 和实验协议。  
**第 22–24 天**：只针对 top-2 路线做初始实验；不追 full result，只追最先减少不确定性的证据。  
**第 25–26 天**：根据实验更新 claim-evidence matrix，把 claim 降级或升级。  
**第 27 天**：做公平比较设计：baseline、预算、seeds、metrics、ablation、counterfactual、failure cases。  
**第 28 天**：写论文摘要草稿，只允许包含已经被证据支持的 claim。  
**第 29 天**：请同学或导师扮演 reviewer，只问三件事：问题是否重要、证据是否够、是否可能只是 benchmark hacking。  
**第 30 天**：定稿一页 research brief，内容固定为：一句问题、默认假设、创新点、killer experiment、主要风险、最低可信证据包。  
**阶段产出**：一个可执行的 research brief、一份实验协议、一份稿件摘要、一份 reviewer-risk checklist。

如果你按这 30 天做完，你未必立刻得到可投论文，但你会得到更宝贵的东西：**一个能持续生产高质量问题与干净证据的 Research Operating System**。这恰恰是顶级研究者与单纯“能做实验的人”之间最重要的分界线。citeturn35view0turn28search2turn33view1turn37view0turn5search0