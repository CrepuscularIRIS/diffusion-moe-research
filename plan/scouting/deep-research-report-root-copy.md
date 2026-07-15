# Aerial VLN 中自生成记忆可靠性门控融合的占位图谱

## 结论先行

基于我对**Aerial / Ground VLN、Embodied Navigation、VLA 导航相邻工作**的主线检索，**你的机制并非“完全无人涉足”**，因为已有工作分别占住了：长时历史记忆建模、历史与当前观测的联合融合、固定权重的 memory/local fusion、冗余驱动的历史采样、感知不确定性感知、语义进度建模，以及 exposure bias / state drift 的训练级纠偏。**但我没有在已审阅的一线主源文献里看到**这样一个被明确提出并完整实现的机制：**把“由 agent 自己轨迹生成的空间记忆，其可靠性会因自诱导漂移而内生、时变地变化”当作一个在线 fusion 问题，并用 drift / consistency / progress 一类内生信号，在闭环 aerial VLN 中逐步门控“history vs. current observation”的信任分配。**因此，我对你的占位判定是：**PARTIALLY occupied，但核心切口仍然 OPEN。** citeturn7view0turn5view0turn23view2turn31view0turn20view6turn20view7

如果你要投 **Information Fusion / ESWA**，最稳的 framing 不是泛称“uncertainty-aware navigation”，而是：**“closed-loop aerial VLN 中，自生成空间记忆的内生可靠性门控融合”**，更具体一点可以写成：**Endogenous reliability-gated fusion of self-generated spatial memory and current observation for closed-loop aerial VLN under self-induced drift**。这个 framing 既避开了“uncertainty in VLN”这一已被相邻工作部分占住的大类，又能和 AerialVLA、OpenFly-Agent、CityNav/HETT、VER、BudVLN / Dual-Anchoring 这些最邻近占位形成清晰边界。 citeturn7view0turn27view1turn11view0turn23view2turn20view6turn20view7

## 最近邻占位图谱

下表不是“论文清单”，而是按**与你的机制最接近的占位方式**组织的 OCCUPANCY ATLAS。

| 现有工作 | 它已经占住了什么 | 与你的机制差在哪里 | 它留下的开放切片 |
|---|---|---|---|
| **AerialVLA**，AAAI 2026，面向 UAV VDN / AVDN 邻域 citeturn7view0turn6view3 | 用 **HSTF** 从历史观测构造**持续演化的 global map**，再把**当前视图、历史表征、对话历史**一起送入 LLM；图示还明确标出了 **Frozen** 视觉部分与 **LoRA** 调参，因而它是你“frozen VLM + LoRA + aerial closed-loop + history fusion”设定下最接近的现成占位。 citeturn7view0turn6view3turn7view1 | 它把历史当作**应被编码并联合处理的上下文**，不是**应被估计可靠性并按时刻门控的证据源**。其公式是把当前 visual token、history token、dialog token 统一并入 backbone，并未给出基于 drift / consistency / progress 的显式可靠性 gate。 citeturn7view0turn7view1 | **把“由自身轨迹生成的 global history map”视为可能失真的 memory，并在推理时按可靠性动态调小其权重**，仍未被这条线占住。 citeturn7view0turn7view1 |
| **OpenFly-Agent**，OpenFly，ICLR 2026 接收 citeturn4view0turn3view1 | 占住了 **current observation + historical keyframes** 的 aerial VLN 范式，并提出 **adaptive frame-level token-sampling** 来抑制历史冗余；当前帧保留 256 tokens，历史 keyframe 被压缩进 memory bank。 citeturn4view0turn5view0turn5view2 | 它的“adaptive”针对的是**冗余压缩 / token budgeting**，不是对**自生成历史是否已因漂移而不可信**的在线度量；历史被压缩，但不是被“质疑”。 citeturn5view0turn5view2 | **从 redundancy-aware sampling 走向 reliability-aware trust allocation**，尤其是在偏航后抑制错误 history，而不是只做 keyframe 选取，仍是空位。 citeturn5view0turn5view2 |
| **HETT**，AAAI 2026，基于 CityNav citeturn26view0turn27view1 | 占住了 **CityNav 上“历史网格图 + 当前视图 + landmark + pose”联合送入 cross-modal transformer** 的两阶段粗到细导航框架；它明确把历史视觉特征动态聚合为 structured spatial memory。 citeturn26view0turn27view1 | 这里的“dynamic”是**memory 更新**与**coarse-to-fine 推理**，不是**history 与 current observation 的可靠性门控融合**；其 token 级联合作用是统一 transformer 融合，而非 reliability gate。 citeturn27view1 | **把历史 grid map 的可信度显式建模为 time-varying latent，并驱动 coarse/fine 两级对 history 的信任切换**，仍未被占住。 citeturn27view1 |
| **VER**，CVPR 2024，ground VLN citeturn21view5turn23view2 | 这是你问题里**最接近“memory vs current fusion”**的已发表工作之一：它把**local action probabilities**（来自当前 volume state）与**global action probabilities**（来自 episodic memory）相结合，最终融合式里有一个**learnable weight \(W_g\)**。 citeturn23view2turn23view4 | 它确实做了 memory/local 的融合，但 **\(W_g\)** 是**可学习参数**，不是由**当前 episode 的 drift / consistency / progress**在线产生的 state-dependent gate；也没有把“self-generated memory corruption”单独提为问题。 citeturn23view2turn23view4 | **从 static learned weight 升级到 per-step endogenous reliability gate**，是你最容易守住、也最容易向审稿人解释的差异。 citeturn23view4 |
| **HAMT**，NeurIPS 2021，ground VLN 长历史基线 citeturn28search1turn28search3 | 占住了“**text + long-horizon history + current observation** 联合用于 action prediction”的主干命题，是许多后续长历史 VLN 的共同起点。 citeturn28search1turn28search3 | 它强调的是**如何高效编码全部过去观测**，而不是**过去观测在偏航后何时不应再被信任**；也没有把内生 memory reliability 作为独立变量。 citeturn28search1turn28search3 | **“history exists” 与 “history should be trusted” 之间的空档**，仍是开放区域。 citeturn28search1turn28search3 |

对你的问题一的直接回答是：**我没有找到已正式发表并明确“用 confidence / uncertainty / reliability gate 在线控制 history-vs-current observation 融合”的 aerial VLN 成熟先例；最近邻工作更多是联合融合、固定加权、时间压缩、或历史采样。**其中真正“机制上最近”的是 **VER 的 static learned weight**；真正“场景上最近”的是 **AerialVLA / OpenFly-Agent / HETT**。 citeturn23view4turn7view0turn5view0turn27view1

## 问题表述是否已经被占住

如果把你的命题拆成两半，结论会更准确。第一半——**“历史记忆是 agent 自己滚出来的，因此在闭环执行中会受到自诱导误差影响”**——这件事在相邻文献里其实已经被不同表述碰到了。BudVLN 把问题表述为 **exposure bias** 与 **instruction-state misalignment**：推理时的小偏差会累计成更大的错误，而 DAgger 式修正本身也可能与语言语义发生错位。Dual-Anchoring 则更直接地把症状称为 **State Drift**，并强调要防止 agent 的 internal state 与 physical reality 脱耦。AerialVLA、HETT、GridMM、ESceme 这些则都默认“历史应被存起来并继续用”，等于承认 history 在闭环里会深刻影响后续决策。 citeturn20view6turn20view7turn7view1turn27view1turn20view0turn21view8

但第二半——**“自生成空间记忆的可靠性本身是一个内生、时变的 fusion 变量，应该在线估计并直接控制 history/current 的融合权重”**——在我审阅到的主源文献里，**没有被清晰地提出为一个独立问题设定**。VER 把 local 与 global memory 用 learnable scalar 融合，说明“memory vs current”可被视作两个证据源；UAOR、AdaNav、Uncertainty-Aware Gaussian Map 又说明“entropy / uncertainty”可以成为动态控制信号；Progress-Think 进一步说明“progress”可以被显式建模并注入策略上下文。**但这些线索尚未被揉合成你要的那个问题表述：memory reliability as an endogenous, time-varying fusion gate.** citeturn23view4turn22view1turn21view3turn21view1turn31view0

所以，对问题二我的判断是：**“self-generated spatial memory 的可靠性是内生且时变”这句话作为一般性直觉，并不新；但把它定义成一个明确的在线 fusion 问题，并在 aerial VLN 中落到 history/current trust gate 上，这个 framing 仍然相当新。**最稳妥的写法不是宣称“首次发现 drift 会污染记忆”，而是宣称：**现有工作大多把 drift 当成训练稳定性、规划误差或历史冗余问题，而不是当成 history-current fusion 的在线可靠性估计问题。** citeturn20view6turn20view7turn24view1turn23view4turn31view0

## 邻近前沿仍然打开的切片

下面这张图谱更像“边界巡航图”，用来回答你的问题三：**相邻方向已经走到哪，哪里还空着。**

| 邻近方向中的代表工作 | 已占住的切口 | 为什么还不是你的机制 | 仍然开放的 slice |
|---|---|---|---|
| **GridMM**，ICCV 2023 citeturn20view0turn21view7 | 用动态增长的 grid memory map 表征历史环境，并通过 instruction relevance aggregation 过滤无关历史特征。 citeturn20view0turn21view7 | 它过滤的是**instruction irrelevance / noise**，不是**drift-induced unreliability**。 | **“relevance ≠ reliability”**：与指令相关不代表在当前偏航状态下仍可信。 |
| **ESceme**，IJCV 2025 版本源自 2023 arXiv citeturn21view8turn18search7 | 用 episodic scene memory 在重访场景时唤醒过往记忆，扩大当前决策视野。 citeturn21view8 | 其核心是假设“过去访问可被有效召回”，没有显式问“这些回忆此刻是否被自己错误轨迹污染”。 | **从 memory recall 走向 memory self-doubt** 仍然空缺。 |
| **UAOR**，2026 VLA 预印本 citeturn22view0turn22view1 | 用 **Action Entropy** 在高不确定层触发 observation reinjection，属于典型 uncertainty-triggered fusion/control。 citeturn22view0turn22view1 | 它 reinject 的是**当前 observation evidence**，对象是 VLA 内部层，不是导航中的**history map vs current view**二元信任分配。 | **把 uncertainty signal 用到“memory should be muted now”而不是“observe more now”**，仍未占住。 |
| **Uncertainty-Aware Gaussian Map**，2026 预印本 citeturn21view0turn21view1 | 把 geometric / semantic / appearance uncertainty 显式融入 VLN 的 3D map / observation space。 citeturn21view1 | 这里的不确定性主要是**感知/建图层面的 perceptual uncertainty**，不是**由 agent 自身闭环偏航造成的 memory trust collapse**。 | **从 perceptual uncertainty 走向 endogenous memory reliability** 仍然开放。 |
| **Progress-Think**，CVPR 2026 citeturn31view0 | 把 semantic progress 作为显式中间状态，注入导航上下文，改善长程一致性。 citeturn31view0 | 它证明了 progress 是有价值的，但 progress 在这里用于**instruction advancement reasoning**，不是直接用来**门控 history/current 融合**。 | **把 progress stall / inconsistency 变成 memory trust gate 的驱动信号**，仍然是空位。 |

再往“drift / exposure bias”这条边走，BudVLN 和 Dual-Anchoring 已经非常接近你的问题意识：前者强调 **continuous online retrospective rectification** 来减轻 exposure bias 与 instruction-state misalignment，后者强调通过 **Instruction Progress Anchoring + Memory Landmark Anchoring** 来缓解 state drift。它们说明领域开始承认“internal state 会漂”。但二者都更偏向**训练/正则/anchoring**，而不是你想做的**推理时、逐步、显式的 history-current reliability gate**。 citeturn20view6turn20view7

在 “memory-gating in nav RL / embodied nav” 这一边，RoboTron-Nav 与 OpenFly-Agent 都已经做了**自适应历史采样**：前者基于相对距离与语义相似度来减少重访冗余，后者做 adaptive frame-level token-sampling 与 keyframe 压缩。**但这条线解决的是 cost / redundancy，不是 trust / recoverability。**换句话说，它们在问“历史里哪些帧值得留”，你在问“即便留着，这些历史现在还应不应该信”。这正是你最适合守住的开放切口。 citeturn24view1turn24view2turn5view0turn5view2

## AVDN、OpenFly、CityNav 的专项核查

先看 **AVDN**。原始 AVDN 论文提出的是人机对话式 aerial navigation 数据集与 HAA-Transformer，模型输入是 dialog 与 visual observations，并通过人类注意力辅助训练提升表现，但我没有在其方法描述里看到 history reliability estimation 或 history/current gating。换言之，AVDN 这条线占住了“**对话历史 + 视觉历史能帮助 aerial navigation**”，没有占住“**对话/视觉历史本身会因自诱导漂移而失真，因而需要在线降权**”。 citeturn12view0turn13view0turn13view3turn13view4

再看 **OpenFly**。OpenFly-Agent 明确把**语言、当前观测、历史 keyframes**作为输入，并加入 **adaptive frame-level token-sampling** 来缓解历史冗余；实验设置里当前帧保留高 token 容量，而历史 keyframe 被强压缩进小 memory bank。这个设计很接近你要讨论的“history 与 current 的资源分配”，但它的判别标准是**冗余与效率**，不是**history 是否已被错误轨迹污染**。因此，OpenFly 上已经有“adaptive history compression”，但还没有“adaptive history trust”。 citeturn4view0turn5view0turn5view2

最后看 **CityNav**。CityNav 原始论文给 baseline 注入的是 **GSM geographic semantic map**，而且该 map 作为 auxiliary modality 被**append 进 GRU 序列**；这更像是把**外部地理语义**加进决策，而非让 agent 评估“自己滚出来的历史记忆是否可信”。此后 **CityNavAgent** 把历史轨迹存成 topological graph 来帮助长期规划；**HETT** 又把历史视觉聚合成 historical grid map 并与 landmark / instruction / pose / current view token 一起送入两阶段 transformer。到这里为止，CityNav 线已经把**外部地图、历史图、多阶段规划、全局记忆图**几乎都占住了，但**“self-generated memory reliability gate”**这个精确位点仍未被占。 citeturn11view0turn11view1turn9view0turn27view1

因此，对你的问题四，我的结论是：**在 aerial VLN，尤其是 AVDN / OpenFly / CityNav 这三条基准线上，我没有检到“基于 endogenous drift / consistency / progress 信号，对 history-vs-current observation 做显式可靠性门控融合”的已发表先例。**我检到的是四类相邻设计：**静态联合融合、固定权重融合、冗余驱动的历史采样、结构化历史地图/图记忆。**这四类都与您的方案邻近，但都没有完全占住你的机制。 citeturn7view0turn5view0turn23view4turn11view0turn9view0turn27view1

## 最终判定与最可守住的 framing

我的最终判定是：**PARTIALLY occupied。**如果你把 claim 写成“我做 uncertainty-aware VLN”或者“我做 adaptive history fusion”，会很危险，因为 UAOR、Uncertainty-Aware Gaussian Map、Progress-Think、VER、RoboTron-Nav、OpenFly-Agent 都会把你的 novelty 快速稀释掉。相反，如果你把 claim 缩到下面这一句，防守性会显著更强：**现有工作未显式建模 closed-loop aerial VLN 中“由 agent 自身轨迹生成的空间记忆”之内生、时变可靠性，也未利用该可靠性去在线门控 history 与 current observation 的融合。** citeturn22view1turn21view1turn31view0turn23view4turn24view1turn5view0

我建议你在论文里把最核心的 unoccupied framing 定为：

**自生成空间记忆的内生可靠性门控融合**  
**Endogenous reliability-gated fusion of self-generated spatial memory and current observation for closed-loop aerial vision-language navigation**

这个 framing 最可守住，因为它把你的贡献同时钉在四个点上：  
一是 **self-generated memory**，不是外部地图；  
二是 **endogenous reliability**，不是泛化的 uncertainty；  
三是 **online fusion gate**，不是训练时纠偏或历史压缩；  
四是 **closed-loop aerial VLN**，不是通用 manipulation VLA。上述四点在我审阅到的 AerialVLA、OpenFly-Agent、CityNav / CityNavAgent / HETT、VER、HAMT、GridMM、ESceme、UAOR、Uncertainty-Aware Gaussian Map、Progress-Think、BudVLN / Dual-Anchoring 主源里，**没有被同一篇工作同时占住。**因此，**你的机制不是“完全无邻居”，但它的最精确占位依然是 OPEN。** citeturn7view0turn5view0turn9view0turn27view1turn23view4turn28search1turn20view0turn21view8turn22view1turn21view1turn31view0turn20view6turn20view7