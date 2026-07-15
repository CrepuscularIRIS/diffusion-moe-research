# 面向两张 48GB GPU 的世界模型选题 Deep Research 报告

## 执行摘要与最终结论

**A 执行摘要**

到 **2026 年 7 月**，如果目标是在 **6—12 个月**内，用 **两张 48GB GPU** 做出一条能投 AAAI 的紧凑算法线，再并行铺一条更系统、偏可靠性与融合的一区期刊线，那么最合理的起点不是追逐“大而全”的视频生成世界模型，也不是卷已经高度拥挤的 Atari 100k 纯分数竞赛，而是选择一个 **可单卡复现、PyTorch 友好、代码完整、能在控制变量下拆分“动力学偏移 / 视觉干扰 / 任务变化”** 的 **决策耦合型 latent world model**。按这个标准，**R2-Dreamer** 是当前最适合做主基线的方案；**TD-MPC2** 是最适合做辅助强基线与 planning-oriented 对照的方案；**DreamerV3** 更适合作为“经典参考上界 / 同源对照”，但由于官方公开实现是 JAX、而你当前工程偏好是 PyTorch，因此它更适合通过 **R2-Dreamer 统一仓库中的 DreamerV3 PyTorch reproduction** 来落地，而不是直接把官方 JAX 代码作为主工程底座。R2-Dreamer 的优势在于：它是 **ICLR 2026** 的官方 PyTorch 仓库，直接覆盖 **DMC Vision / DMC Subtle / Meta-World / Crafter / Atari 100k / Memory Maze / IsaacLab**，并且作者明确报告在与其 DreamerV3 reproduction 同一代码框架下，R2-Dreamer **较 DreamerV3 训练快约 1.59×**；同时仓库还集成一个 **约 5× faster** 的 PyTorch DreamerV3 baseline，适合做统一消融与公平对照。TD-MPC2 的优势则是：代码成熟、MIT 许可、公开了 **300+ checkpoints**，支持 **104 个连续控制任务**、**单任务在线 RL** 与 **多任务离线 RL**，并且仓库明确写出 **单任务在线 RL 推荐 8GB GPU 即可运行**，这对你的两张 48GB GPU 来说非常友好。 citeturn16search8turn19search9turn6view2turn31search12turn16search10turn6view1turn20search8turn27view4

真正值得做的科学问题，不再是“世界模型能不能生成更好看的视频”，而是：**在未见动力学、策略诱导 OOD、以及长期 imagination compounding error 下，模型能否“知道自己什么时候不可靠”，并把这种不可靠性转化为更稳健的闭环决策机制。** 这正是 Route A 最适合瞄准的核心。与此同时，如果你把 Route B 改写成“**缺失、噪声、冲突、多时间尺度条件下的多源证据融合与可靠世界模型**”，并把工作重心放在 **pixels + proprio/state + context** 的多源融合、**fast/slow dynamics**、**uncertainty decomposition + calibration**、以及 **missing / asynchronous / corrupted modality** 的系统实验，那么它会更稳地落在 **Information Sciences** 的口味上；若想冲 **Information Fusion**，就必须让“fusion”成为论文主角，而不是把特征拼接伪装成融合创新。Information Fusion 的官方 Aims & Scope 明确强调 **multi-sensor, multi-source, multi-process information fusion**，并鼓励 **feature / decision / multilevel fusion、multi-look temporal fusion、imperfect / incomplete environments、resource-aware fusion architectures**；单纯“把图像和状态拼起来喂进 RSSM”并不够。相比之下，Information Sciences 更强调 **information / knowledge engineering、intelligent systems、modelling、adaptive systems 与 theory-practice balance**，对“可靠世界模型 + uncertainty + missing modality + complexity/statistical analysis”的容忍度更高。 citeturn15search2turn26search4turn24view0turn24view1

**M 最终 Go / No-Go 结论**

我的总体判断是：**Route A 明确 Go；Route B 条件性 Go；Information Fusion 默认 No-Go，除非你主动把它改造成真正的 multi-source fusion 论文。** 更具体地说，若你在未来两周内完成 **R2-Dreamer 最小复现 + TD-MPC2 对照复现 + CARL/DMC-GB2 环境打通**，并确认单卡显存、吞吐、日志与指标可以稳定跑通，那么主线应该立即收敛到一条紧凑、统一、审稿人容易理解的 AAAI 路线：**Calibrated Adaptive World Models for Robust Planning under Dynamics Shifts**。如果这一步失败，fallback 才是把 **TD-MPC2** 升级为主基线、将世界模型研究问题收缩为 planning-oriented implicit world model 的可靠性问题。Route B 则适合在 Route A 的基础设施之上展开，但必须避免重复投稿：它应该围绕 **多源融合、信息缺失、冲突证据处理、时间尺度分解、校准与统计显著性** 来重写，而不是再讲一遍“uncertainty helps robust planning”。 citeturn16search8turn6view2turn16search10turn6view1turn24view0turn24view1

下表先给出你要求的十个最终直答。

| 直答问题 | 结论 | 依据 |
|---|---|---|
| 最推荐的一个主基线 | **R2-Dreamer** | 官方 PyTorch；直接支持 DMC Vision / DMC Subtle / Meta-World / Crafter / Atari 100k / Memory Maze；在统一代码框架下相对 DreamerV3 更快；适合单卡最小实验。citeturn16search8turn6view2turn19search9turn31search12 |
| 最推荐的一个辅助基线 | **TD-MPC2** | 代码成熟，MIT，300+ checkpoints，支持 state/pixel、单任务在线与多任务离线，单任务在线推荐 8GB GPU。citeturn16search10turn6view1turn20search8turn27view4 |
| 最推荐的两个环境家族 | **DMC 生态** 与 **CARL-DMC** | DMC 生态可拆视觉干扰、长期控制和微小视觉目标；CARL 可单独操控 gravity / friction / mass / joint strength 等动力学上下文。citeturn23academia15turn22view0turn21view5turn21view0turn37search11 |
| 最适合两张 48GB GPU 的实验组织方式 | **一张卡一个完整 run；另一张卡跑另一随机种子或另一基线/消融；避免显存合并幻想；只在仓库原生支持时使用 DDP。** | TD-MPC2 单任务本就可在低显存运行；R2-Dreamer 单卡可作为默认执行单元，符合你“单卡先跑通”的工程约束。citeturn6view1turn6view2 |
| AAAI 路线最值得研究的一个问题 | **已校准的 epistemic uncertainty 能否驱动自适应 imagination horizon，并在 dynamics shift + policy-induced OOD 下提高闭环回报与 policy-ranking agreement。** | 这是当前决策耦合世界模型最欠缺、又可在 CARL + DMC-GB2 上低成本验证的问题。citeturn15search2turn26search4turn35search8turn14search2 |
| Information Sciences 路线最值得研究的一个问题 | **在像素、低维本体状态与上下文参数存在缺失、噪声、冲突和异步时，如何做 uncertainty-guided multi-source fusion，使世界模型更可校准、更耐 OOD。** | 这更贴近 Information Sciences 对 intelligent systems / modelling / adaptive systems 的期待。citeturn24view1turn23academia14turn21view0 |
| Information Fusion 是否真正适合 | **默认不适合；存在 scope mismatch。** 只有当论文显式做 **multi-source / multi-process / multilevel fusion、缺失/冲突证据处理、资源约束下动态专家选择** 时才真正匹配。 | 官方 Aims & Scope 明确要求 multi-sensor / multi-source / multi-process fusion。citeturn24view0 |
| 哪些已有论文最接近拟议方法 | **R2-Dreamer、Plan To Predict、Calibrated MBRL、RWM-U、Policy-Driven World Model Adaptation、WIMLE、Imperfect World Models are Exploitable。** | 它们分别覆盖 decoder-free 表征、uncertainty-foreseeing、校准、不确定性惩罚、policy-aware adaptation、多模态不确定性建模与 exploitability 理论。citeturn16search8turn35search8turn14search7turn14search2turn35search11turn35search2turn26search4 |
| 哪个研究想法最可能因缺乏新意而失败 | **“在 Dreamer / R2-Dreamer 上简单加 ensemble + uncertainty penalty + multi-step consistency”** | 这很容易被审稿人视为模块拼接；近年相关思想已在 uncertainty-aware MBRL 与 policy-aware adaptation 中多次出现。citeturn14search2turn35search11turn35search8turn35search2 |
| 下一步首先应该复现哪三个实验 | **R2-Dreamer on DMC Vision；R2-Dreamer on CARL-DMC dynamics shift；TD-MPC2 rgb on matched DMC tasks。** | 这三项最能同时验证代码、算力、对照公平性与最终选题可行性。citeturn6view2turn21view0turn6view1 |

## 研究地图与关键文献

**B 研究地图**

从 **2023—2026** 的研究脉络看，“世界模型”已经不是单一范式，而是至少包含两大主轴：其一是 **决策耦合型 world model**，核心目的是通过 latent imagination、implicit planning 或 learned simulator 来提升策略学习和规划；其二是 **视频生成型 world model**，核心目的是生成高保真、长时域、具交互性的未来观测。对你当前的算力与论文目标而言，应优先站在第一主轴上，用第二主轴的工作来理解评测缺口和未来趋势，但不要把其作为首轮主线，因为后者往往隐含更大的数据、模型和训练代价。DreamerV3、R2-Dreamer、TD-MPC2 都属于明显的 **decision-coupled world models**；DIAMOND、Vid2World、World4RL 更接近 **video-generation-driven interactive simulators**。这两类工作的评价标准并不相同：前者更该关注闭环决策、counterfactual fidelity、policy ranking 与 exploitability，后者常被视觉质量与 controllability 主导。 citeturn16search9turn16search8turn16search10turn19search2turn32search10turn26search15turn15search2

| 类别 | 核心代表 | 研究重心 | 对你项目的相关性 |
|---|---|---|---|
| latent state-space world models | PlaNet、Dreamer、DreamerV3、R2-Dreamer citeturn37search2turn37search1turn16search9turn16search8 | 学 latent dynamics、reward、value，再在 latent imagination 中优化策略 | **最高**：最贴近 Route A |
| reconstruction-based Dreamer 类 | Dreamer、DreamerV3 citeturn37search1turn16search9 | 以重建目标稳定表征学习 | **高**：经典强参考 |
| decoder-free predictive world models | TD-MPC2、R2-Dreamer citeturn16search10turn16search8 | 去掉像素 decoder，把 capacity 留给 task-relevant dynamics / planning | **最高**：最合算力约束 |
| planning-oriented implicit world models | TD-MPC2、TD-MPC 系列 citeturn16search10turn32search15 | 强调 latent MPC 与 local trajectory optimization | **高**：最强 planning 对照 |
| transformer world models | IRIS、STORM、TWM citeturn19search3turn7search4turn10search5 | 长程依赖、token/sequence 建模 | **中**：Atari 强，但与连续控制主线略远 |
| diffusion world models | DIAMOND、Horizon Imagination、Vid2World、World4RL citeturn19search2turn14search0turn32search10turn26search15 | 高保真视觉预测、交互式 video simulator | **中低**：有启发，但首轮成本偏高 |
| object-centric / causal world models | OC-STORM、Counterfactual World Models citeturn20search11turn15search5 | 以对象与干预一致性提升可解释性和 controllability | **中**：可作后续 extension |
| uncertainty-aware world models | PETS、Calibrated MBRL、RWM-U、WIMLE、P2P citeturn34search3turn14search7turn14search2turn35search2turn35search8 | 区分 epistemic / aleatoric，抑制模型偏差与 exploitability | **最高**：Route A / B 共同核心 |
| multimodal / multi-source / multi-timescale | DMC-VB、Newt、WPT citeturn23academia14turn36search1turn36search15 | 多源输入、 demonstrations、language 或多时间尺度建模 | **高**：Route B 的自然支点 |
| offline / online MBRL | MOPO、MOReL、TD-MPC2、RWM-U、ROMBRL citeturn34search0turn34search1turn16search10turn14search2turn35search11 | 数据支持、保守优化、world-model planning under shift | **中高**：可借鉴评价与 uncertainty 方案 |
| 视频生成型 vs 决策耦合型 | DIAMOND / Vid2World vs Dreamer / TD-MPC2 / R2-Dreamer citeturn19search2turn32search10turn16search9turn16search10turn16search8 | 前者偏 realism，后者偏 control utility | **必须严格区分** |

截至 **2026 年 7 月**，**决策耦合世界模型最缺少的不是新 backbone，而是“可靠决策”视角下的统一评价协议与轻量、可校准的不确定性感知机制。** 最新 position paper 直接指出，当前文献常把 **视频 realism / 一步误差 / 视觉指标** 与 **planning usefulness / policy optimization utility** 混在一起，造成 claim 与 evidence 错配；而 exploitability 理论工作则进一步表明，**不完美世界模型几乎天然可被策略利用**，因此只报告最终回报而不报告 exploitability、ranking inversion 和 calibration，是不够的。 citeturn15search2turn26search4turn26search1

与此对应，**最拥挤且不适合资源有限团队进入的方向** 包括三类。第一类是 **foundation-model-scale 视频世界模型**，例如把互联网规模视频扩散模型改造成交互 world model，这类工作往往依赖大规模预训练与较重推理开销；Vid2World 的官方 repo 就明确是在“repurpose internet-scale pretrained video diffusion models”。第二类是 **多百任务 generalist multitask world model scaling**，如 Newt / MMBench 和 WPT，虽然学术价值极高，但其 benchmark 本身就扩展到了数十到两百任务与 demonstrations / language 条件，明显超出本项目首轮算力预算。第三类是 **Atari 100k 纯分数追逐**，IRIS、STORM、TWM、DIAMOND 已经把 token / transformer / diffusion 三条线都卷得很深，而这些成果对你要做的 dynamics shift、CARL context generalization、continuous control robustness 并不天然对齐。 citeturn32search10turn36search1turn36search15turn19search3turn7search4turn10search5turn19search2

**仍缺乏统一可信评价协议的问题**，主要包括：策略诱导分布偏移下世界模型的 closed-loop validity；counterfactual action fidelity；长时 imagination 删除/保留的合理 horizon；以及 uncertainty 是否真的和真实 rollout 误差相关。现有基准能分别覆盖其中部分维度，但还缺一套被社区广泛接受的“同一预算、同一任务、同一 shift、同时报告 model metrics 与 decision metrics”的标准协议。DMC-GB / DMC-GB2 和 Distracting Control 把视觉泛化拆得很清楚；CARL 把 dynamics context 拆得很清楚；DMC-VB 则把 state / pixel 配对数据与 distractor 离线评测做得很扎实；但这些基准之间尚未自然整合成一个主流 world-model reliability benchmark。 citeturn22view0turn21view5turn22view1turn21view0turn23academia14turn15search2

**一步预测误差、PSNR/SSIM 和最终任务回报都各自有明显缺陷。** 一步预测误差无法反映 compounding error，也无法检验模型是否在干预下保持 action sensitivity；PSNR/SSIM 更偏向视觉保真，经常高估“背景、纹理、静态区域”的重要性，却可能忽略任务关键的小目标或 reward-relevant causal feature，R2-Dreamer 在 DMC-Subtle 的结果正说明“小而关键的视觉对象”可以决定控制性能；最终任务回报则把 world model quality、policy optimizer、探索噪声、甚至 exploitability 混在一起，单独看回报无法知道提升到底来自于更好的模型，还是策略学会了利用模型漏洞。 citeturn15search2turn16search8turn16search12turn19search14

因此，我建议你把评测分成一个 **L4—L7 决策型指标矩阵**。其中 **counterfactual action fidelity** 应通过“固定观测前缀、分叉动作、比较真实环境与世界模型在短期 reward / successor feature / terminal event 上的一致性”来测；**closed-loop rollout validity** 则通过 real-env synchronized evaluation，统计 imagined policy 在真实环境的 return drop、trajectory divergence 和 failure mode consistency；**reward / value prediction** 不能只看 one-step MSE，而要看 horizon-conditioned error growth；**policy-ranking agreement** 可用 Kendall’s tau 或 Spearman 相关，比较一组不同 policies 在 world model 中与真实环境中的排序一致性；**optimization lift** 则定义为“同一真实交互预算下，利用 world model 优化后，相对不利用该 world model 的对照提升”；**model exploitability** 则看 ranking inversion、虚假高回报 imagined policy 的 real-env collapse 频率；**uncertainty calibration** 要报告 coverage、NLL、ECE/ENCE 与 error-uncertainty correlation；**OOD detection** 则应区分 dynamics / visual / task 三类 shift 分别报告 AUROC / AUPRC；**long-horizon consistency** 则应用 horizon sweep 画出 error-growth / ranking-agreement decay 曲线，而不是只报一个固定 rollout 长度。上述设计并非完全照搬已有基准，而是把最新 position paper 的评价思想与你的 DMC / CARL 资源条件对齐后的可执行版本。 citeturn15search2turn26search4turn14search7turn33search4

现有世界模型在 **policy-induced distribution shift** 下失败，根本原因主要有三层。第一层是 **objective mismatch**：模型多按 MLE 或一步监督目标拟合训练分布，却在下游被策略拿去做多步优化与 OOD 探索。第二层是 **distribution shift amplification**：策略一旦朝着模型高估区域优化，就会把自己推向模型最没见过、也最容易犯错的区域；P2P 和 ROMBRL 都在不同设置下正面指出了这种 model-learning / model-usage mismatch。第三层是 **exploitability inevitability**：最新理论工作表明，除非强约束策略类或控制 horizon，不完美 world model 通常都存在可被利用的偏差。 citeturn35search8turn35search11turn26search4turn26search1

你提出的 **dynamics change、visual change、task change 分开评价** 是完全正确的，而且应当写进论文 protocol。**Dynamics shift** 用 CARL-DMC 这类上下文化物理参数变化 benchmark；**visual shift** 用 DMC-GB / DMC-GB2 / Distracting Control / DMC-VB；**task shift** 则用 Meta-World MT10/ML10/MT50 这类 goal / task family 变化，或者 Crafter / Procgen / MiniGrid 这类组合泛化环境。只有这样，才能避免“方法其实只是对 background 更稳”却被误写成“对 dynamics 更可靠”的常见误判。 citeturn21view0turn22view0turn21view5turn22view1turn23academia14turn22view4turn21view1turn8search9turn21view4turn22view3

关于 **epistemic** 与 **aleatoric** uncertainty，在世界模型中可实现且可校准的方法，实用上最重要的是五类。第一类是 **ensemble / bootstrap heads / latent disagreement**，优点是直接、鲁棒、和 world model 兼容性好，PETS、RWM-U、latent disagreement pretraining 都证明了这条线可用；缺点是训练与推理成本线性增加，而且容易把“参数量更大”误判成“方法更好”。第二类是 **Bayesian approximation**，例如 dropout / Laplace / variational tricks，优点是单模型改造较轻，缺点是校准稳定性依赖实现。第三类是 **distributional / heteroscedastic prediction**，适合承载 aleatoric uncertainty，但对 epistemic 的表达较弱。第四类是 **evidential learning**，单次前向即可给出不确定性，但在 OOD 下过度自信与不稳定是常见问题。第五类是 **conformal prediction**，优点是可以给出有限样本 coverage 解释，适合做 deployment-time wrapper；缺点是严格条件下依赖 exchangeability，且用于 sequential rollout 时必须处理时间相关性和在线再校准。你的项目最可行的组合，不是把这些方法都塞进来，而是以 **small latent ensemble + calibration head / post-hoc calibration + disagreement-based horizon control** 为主，再把 conformal 作为评测或 wrapper，而不是核心训练机制。 citeturn34search3turn14search7turn14search2turn33search3turn14search11turn33search4

**纯虚拟环境就足以充分验证的问题** 包括：uncertainty calibration、OOD detection、counterfactual fidelity、exploitability、policy-ranking agreement、adaptive horizon、multi-source fusion 在缺失/噪声/冲突条件下的可靠性，以及多时间尺度 dynamics 是否改善 long-horizon consistency。真正需要真实机器人的，通常是“和真实感知噪声、接触建模、硬件时延、sim-to-real”强绑定的问题；而你当前拟议的两个路线，都完全可以在虚拟 benchmark 中得到充分验证。 citeturn15search2turn21view0turn23academia14turn22view4

**C 关键综述与定位论文**

下表列出我认为与你选题决策最关键的 **14 篇综述 / 定位 / benchmark 论文**。这些文献的价值不在于“泛泛综述世界模型”，而在于给 Route A/Route B 提供理论位置、评价框架和 benchmark 选择依据。

| 类型 | 论文 | 年份 / 场所 | 为什么关键 | 来源 |
|---|---|---|---|---|
| 奠基 | *World Models*, Ha & Schmidhuber | 2018, arXiv | 最早系统提出“在梦中训练 agent”的现代 world model 范式 | citeturn37search0 |
| 奠基 | *Learning Latent Dynamics for Planning from Pixels* (PlaNet), Hafner et al. | 2019, ICML | 引入 RSSM + latent planning，是 Dreamer 系与大量 latent world model 的祖先 | citeturn37search2turn37search10 |
| 奠基 | *Dream to Control*, Hafner et al. | 2020, ICLR | 把 latent imagination 与 actor-critic 打通，直接通向 DreamerV3/R2-Dreamer | citeturn37search1turn37search9 |
| 基准 | *dm_control: Software and Tasks for Continuous Control* | 2020 | DMC 生态的官方入口 | citeturn23academia15turn22view2 |
| 基准 | *The Distracting Control Suite* | 2021 | 视觉干扰 benchmark 的典型起点 | citeturn22view1 |
| 基准 | *CARL: A Benchmark for Contextual and Adaptive RL* / *The Case for Context in RL* | 2022 | 系统拆解 context / dynamics shift，是 Route A 的关键 benchmark 依据 | citeturn37search7turn21view0turn37search11 |
| 基准 | *Evaluating Long-Term Memory in 3D Mazes* | 2022 | 解释为什么长时记忆不是现有 world model 默认会解决的问题 | citeturn9search15turn21view2 |
| 综述 | *A Survey on Model-Based Reinforcement Learning* | 2024 | 对 uncertainty、model bias、planning / learning 两大分支梳理较好 | citeturn12search9turn12search13 |
| benchmark / position | *DMC-VB* | 2024, NeurIPS D&B | 把 state/pixel pairing、visual distractors 和 offline representation gap 明确化 | citeturn23academia14turn23search2 |
| 总览综述 | *Understanding World or Predicting Future? A Comprehensive Survey of World Models* | 2025, survey | 从定义到应用的宏观框架，适合建立领域地图 | citeturn12search3turn12search7 |
| 总览综述 | *World Models: A Comprehensive Survey of Architectures...* | 2026, arXiv survey | 2026 视角的最新归纳，可用来补 2025 之后分支 | citeturn12search4 |
| 定位 | *Mastering Diverse Control Tasks through World Models* (DreamerV3) | 2025, Nature | 现代 Dreamer 主参考文献；也说明单 A100 可复现是现实目标 | citeturn16search1turn29search8 |
| 评价立场 | *How Should World Models Be Evaluated? A Decision-Making-Centric Position* | 2026, arXiv | 你提的很多评价问题，这篇几乎是直接回答 | citeturn15search2 |
| 可靠性理论 | *Imperfect World Models are Exploitable* | 2026, arXiv | 明确为什么 world model 仅看回报不够，必须纳入 exploitability | citeturn26search4turn26search1 |

**D 与两条路线直接相关的原始论文**

下面给一份更贴近 Route A / Route B 的 **22 篇核心原始论文**。我把它们分成“基线主干”“可靠性/不确定性”“泛化与数据生态”三组。对于 2025—2026 的工作，我优先用了 arXiv / OpenReview / 项目页 / 官方代码页，而不是二手解读。  

| 分组 | 论文 | 价值 | 来源 |
|---|---|---|---|
| 基线主干 | *R2-Dreamer: Redundancy-Reduced World Models without Decoders or Augmentation* | 你当前最优主基线候选 | citeturn16search8turn16search0 |
| 基线主干 | *Mastering Diverse Domains through World Models* / Nature version | 经典 Dreamer 参考系 | citeturn16search9turn16search1 |
| 基线主干 | *TD-MPC2: Scalable, Robust World Models for Continuous Control* | 最强 planning-oriented 对照 | citeturn16search10turn16search6 |
| 基线主干 | *Transformers are Sample-Efficient World Models* (IRIS) | Transformer world model 的早期强基线 | citeturn19search3turn20search10 |
| 基线主干 | *STORM* | 随机 Transformer world model，Atari 强基线 | citeturn7search4turn7search7 |
| 基线主干 | *Transformer-based World Models Are Happy With 100k Interactions* (TWM) | 另一个 Atari transformer WM 强对照 | citeturn10search5turn9search2 |
| 基线主干 | *Diffusion for World Modeling: Visual Details Matter in Atari* (DIAMOND) | 扩散世界模型代表 | citeturn19search2turn16search7 |
| 可靠性 / uncertainty | *Plan To Predict* | uncertainty-foreseeing 思想很接近 Route A，但更多是 state MBRL 框架 | citeturn35search8turn35search0 |
| 可靠性 / uncertainty | *Calibrated Model-Based Deep Reinforcement Learning* | “uncertainty 必须校准” 的经典论断 | citeturn14search7 |
| 可靠性 / uncertainty | *PETS* | ensemble + epistemic / aleatoric 区分的经典参考 | citeturn34search3 |
| 可靠性 / uncertainty | *When to Trust Your Model* (MBPO) | 短模型 rollout 与 model usage trade-off 的经典依据 | citeturn34search2turn34search10 |
| 可靠性 / uncertainty | *MOPO* | uncertainty-penalized offline MBRL 标志性工作 | citeturn34search0turn34search16 |
| 可靠性 / uncertainty | *MOReL* | pessimistic model-based offline RL 与 exploitability 相关 | citeturn34search1turn34search9 |
| 可靠性 / uncertainty | *RWM-U* | 明确把 epistemic uncertainty 和长时 rollout 结合，最接近你想做的“可靠 world model”之一 | citeturn14search2turn14search6 |
| 可靠性 / uncertainty | *WIMLE* | 2026 新工作，mode-covering + uncertainty-aware world model | citeturn35search2turn35search10turn35search14 |
| 可靠性 / uncertainty | *Policy-Driven World Model Adaptation for Robust Offline MBRL* | policy-aware / world-model adaptation 方向的重要对照 | citeturn35search11turn35search3 |
| 可靠性 / uncertainty | *Imperfect World Models are Exploitable* | Route A 中 exploitability 指标的理论依据 | citeturn26search4turn26search1 |
| 可靠性 / uncertainty | *Counterfactual World Models* | 如果想把 counterfactual fidelity 写得更硬，这篇值得跟进 | citeturn15search5 |
| 泛化 / 表征 | *Learning Latent Dynamic Robust Representations for World Models* | 对 exogenous noise / task-relevant feature 很接近 Route A 的泛化问题 | citeturn35search1turn35search13 |
| 泛化 / 数据生态 | *DMC-VB* | Route B 多源/离线/表征融合最优 benchmark 之一 | citeturn23academia14turn23search2 |
| 泛化 / 多任务 | *Generalist World Model Pre-Training for Efficient RL* | 多源、多任务、reward-free offline data 的代表，但首轮不建议主打 | citeturn36search15turn36search5 |
| 泛化 / 多任务 | *Learning Massively Multitask World Models for Continuous Control* (Newt) | 2026 多任务 world model scaling 的前沿，也说明该方向对你当前算力过于激进 | citeturn36search1turn36search17turn36search3 |

## 基线、仓库、环境与算力评估

**E 官方仓库与复现状态表**

先给“仓库可用性”而不是“论文分数”。因为对你的项目来说，**能稳定安装并在单卡跑出最小实验** 比“论文里的 SOTA 曲线”更重要。

| 仓库 | 最近更新 / 许可证 | 训练脚本 / 评测脚本 / Docker | checkpoint / 数据 | 复现状态判断 | 主要风险 | 来源 |
|---|---|---|---|---|---|---|
| **R2-Dreamer** | `546e4fa`，约 2 个月前；MIT | 有 `train.py`，有 Dockerfile，extras 覆盖 dmc / metaworld / crafter / memorymaze / isaaclab | 无 release；README 给出 benchmark 和预算 | **代码新但完整**；最适合作为研究底座 | 仓库很新，仅 8 commits；社区复现积累少 | citeturn19search9turn6view2turn31search12 |
| **DreamerV3** | `e3f0224`，约 2 个月前；MIT | 有 Dockerfile；训练说明完整 | 官方 repo 未突出公开 checkpoint；有 `scores` 目录 | **方法权威，但工程不最优** | 官方公开实现是 JAX；对 PyTorch 项目不友好 | citeturn19search8turn6view0 |
| **TD-MPC2** | 已抓取页面未给明确 commit；MIT | `train.py` / `evaluate.py` / Dockerfile 完整 | 300+ checkpoints；30-task / 80-task datasets 公开 | **当前最成熟对照之一** | Meta-World 依赖 `gym==0.21.0`、MuJoCo 2.1.0，安装有历史包袱 | citeturn6view1turn27view4turn32search12 |
| **DIAMOND** | 页面未提明确最近 commit；MIT | `src/main.py` 训练、`play.py` 可视化；requirements 完整 | Hugging Face 提供 pretrained world models / agents | **可运行，但偏 Atari/扩散路线** | 推理与训练成本都较高；不适合首轮主线 | citeturn6view3turn20search9 |
| **IRIS** | 最新 commit 文本未可靠提取；GPL-3.0 | `src/main.py`、脚本齐全 | 官方说明 release code and models | **Atari 线很扎实** | 许可证更强；与连续控制主线距离较远 | citeturn6view4turn13view3turn20search10 |
| **STORM** | `e8be598`，约 4 个月前；**未见清晰 license 声明** | `train.sh` / `eval.sh` 完整 | 给出 demonstration trajectory 压缩包 | **可跑，但不再维护** | README 明确说该 repo 已不再维护，推荐 OC-STORM | citeturn20search3turn17view0 |
| **DMC-GB2 repo** | 无 release；MIT | config 明确；与 DMC-GB / DCS 集成 | 含部分视频背景数据 | **基准有用，但不是 world model 主仓库** | 更适合作为外部 benchmark，而非算法底座 | citeturn21view5 |
| **Minari** | 最近 2 周内更新；标准库项目 | CLI 完整；`minari list remote/show/download` | 远程数据集与生成工具完备 | **离线实验基础设施成熟** | 与像素 world model 的直接耦合需自行处理 | citeturn10search4turn22view5turn21view3 |

一个关键结论是：**如果你要“少踩工程坑、又能在单卡上先跑通”，R2-Dreamer 与 TD-MPC2 的组合明显优于 DreamerV3 官方 JAX + 自己再搭 benchmark。** R2-Dreamer 仓库虽然新，但它恰好把你最关心的几个因素合在一起：**PyTorch、DMC / Meta-World / Crafter / Memory Maze、Dreamer baseline、decoder-free 研究空间。** TD-MPC2 则提供一个成熟、现实、planning-oriented 的对照面。 citeturn6view2turn31search12turn6view1turn27view4

**F 环境、数据集与基准比较表**

下面这张表按“你能不能用它做严谨实验”来评，而不是按“社区流行度”来评。我把 **在线 / 离线、可控偏移、视觉干扰、长时记忆、多模态潜力、下载/生成成本、与三大基线兼容性** 都放进去。

| 环境 / 数据 | 在线 / 离线 | 观测 / 动作 / 任务数 | 可改物理参数 | 视觉干扰 | 程序地图 / 组合泛化 | 长时记忆 | 多模态融合潜力 | 标准划分 | 成本与瓶颈 | 与 R2 / Dv3 / TD2 兼容性 | 维护状态与推荐用途 | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **DMC state / vision** | 在线 | state 或 pixel；连续；多任务 suite | 基础 suite 本身有限，但可通过改 MJCF / wrapper 扩展 | 原生无 | 否 | 中 | 中 | 标准任务成熟 | 生成成本低；CPU+GPU 都友好 | **R2 强、Dv3 强、TD2 强** | **首选基础环境家族** | citeturn23academia15turn6view2turn27view4 |
| **DMC-GB** | 在线测试基准 | pixel；连续；围绕 DMC 任务 | 否，主打视觉泛化 | **强**，color/video easy-hard | 否 | 中 | 低 | 有 train/test mode | 需要背景资源；比原 DMC 略重 | R2 / Dreamer 可接；TD2 需自接 wrapper | **视觉 OOD 首选** | citeturn22view0 |
| **DMC-GB2** | 在线测试基准 | pixel；连续；整合 DMC-GB + DCS | 否 | **更强**，含 geo/photo + DCS | 否 | 中 | 低 | 明确 test modes | 和 DMC-GB 相近；成本可控 | 需自接，但非常值得 | **高优先级视觉 shift benchmark** | citeturn21view5 |
| **Distracting Control Suite** | 在线测试基准 | pixel；连续；DMC 扩展 | 否 | **强**，背景/颜色/相机 | 否 | 中 | 低 | 难度分级 | 需要 DAVIS 2017 | 兼容 Dreamer / R2，TD2 需包装 | 用于验证纯 visual robustness | citeturn22view1turn22view0 |
| **CARL-DMC** | 在线 | state/pixel/context；连续；多环境上下文扩展 | **强**：gravity / friction / mass / joint strength 等 | 可与 DMC visual 叠加 | 否 | 中 | **高**：context 天然可作为额外源 | 有 contextual split 思路 | 生成成本低；非常适合 controlled OOD | 需少量接入工作；R2 最合适 | **动力学 shift 首选** | citeturn21view0turn37search11 |
| **Meta-World** | 在线 | state 或 render；连续；50 tasks | 可做 goal/task shift，不擅长物理 context | 弱，需自加渲染干扰 | 多任务 / meta 泛化强 | 中 | 中 | MT1/10/50, ML1/10/45 | contact dynamics 比 DMC 更难；CPU 稍重 | R2 已支持；TD2 已支持；官方 Dv3 需额外接入 | **任务变化与 manipulation 扩展首选** | citeturn22view4turn21view1 |
| **Crafter** | 在线 | pixel；离散；单环境但多能力维度 | 否 | 原生一般 | **有组合性** | 中高 | 低 | reward / score 体系成熟 | 生成成本低；适合 general ability | R2 与 Dv3 已支持；TD2 不适合 | 用作“泛能力单环境”备选 | citeturn8search9turn8search1turn6view2 |
| **Procgen** | 在线 | pixel；离散；16 envs | 否 | 原生风格变化 | **强**，程序化生成 | 中 | 低 | train/test seed 明确 | 单核速度高 | Dreamer 类可接；TD2 主线不建议 | 更适合 generalization，对 Route A 非首选 | citeturn8search2turn21view4 |
| **MiniGrid** | 在线 / 离线可造数 | symbolic / RGB；离散；多任务 | 可程序化改规则与地图 | 可加但非强项 | **强** | 中高 | **中高**：可与 mission/context 融合 | 文档与任务族清晰 | 很轻量，CPU 友好 | 需额外接入；对 Dreamer 离散版可行 | **低成本 OOD / memory 备选** | citeturn9search0turn22view3 |
| **Memory Maze** | 在线 + offline repr dataset | pixel；离散；多尺寸 maze | 否 | 一般 | randomized mazes | **强** | 中 | 标准尺寸与 probe 信息 | 单次训练较长；长时依赖难 | R2 已支持；Dreamer 生态可接；TD2 不自然 | **长时记忆专用扩展 benchmark** | citeturn21view2turn6view2 |
| **Atari 100k** | 在线 | pixel；离散；26 games | 否 | 原生复杂视觉 | 低 | 中 | 低 | 协议成熟 | 训练耗时仍不低，且离散特化 | IRIS/STORM/DIAMOND 擅长；R2 支持 | **若做 Atari 线可用，但不建议首轮主打** | citeturn19search3turn7search4turn19search2 |
| **Minari / D4RL 迁移数据** | 离线 | 多为 state；连续；多数据集 | 取决于源 env | 一般 | 一般 | 低 | 低到中 | dataset id 标准化 | 下载成本低到中；存储可控 | 对 offline MBRL 很友好，对 pixel fusion 不够 | **Route B 离线补充，不是主 benchmark** | citeturn22view5turn8search3turn10search0turn8search15 |
| **DMC-VB** | **离线 benchmark** | state + pixel pairs；连续；36 subsets | 否，但任务含 locomotion + ant maze | **强**，静态与动态 distractors | 否 | 中 | **高**：state/pixel pairing 极适合 fusion | benchmark 设计完整 | 数据规模较大；按子集下载 | 需自接到 world model 流程，但价值极高 | **Route B 首选离线多源 benchmark** | citeturn23academia14turn23search0turn23search1 |

如果只允许你优先投入两个环境家族，我的建议仍然是：**第一优先是 DMC 生态**，因为它能把 DMC Vision、DMC-Subtle、DMC-GB2、Distracting Control 组织成一条视觉/OOD/长期控制的统一协议；**第二优先是 CARL-DMC**，因为它能把 dynamics shift 从视觉问题中解耦出来。只有在你要做更强的任务变化 / manipulation 泛化时，才把 **Meta-World** 作为第三优先。Route B 若要走多源融合，则再额外引入 **DMC-VB** 作为离线多模态／paired state-pixel benchmark。 citeturn6view2turn22view0turn21view5turn21view0turn23academia14turn22view4

**G 基线比较与算力评估表**

下表把你要求的 “算法选择 + 算力可行性 + 可修改性 + 复现风险” 合在一起。凡是官方没有公开的显存或训练时长，我明确写成 **未知** 或 **估算**。

| 算法 | 年份 / 场所 | 核心架构 | 重建式 / decoder-free | online / offline | state / pixel | 动作 | 多任务 | 规划 | 显式 uncertainty | 官方环境支持 | 单任务默认步数 / 标准预算 | 参数量 | 官方 GPU / 训练时间 | 两张 48GB 可行性 | 修改难度 | 复现风险 | 研究起点推荐 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **R2-Dreamer** | 2026, ICLR | RSSM + redundancy reduction on latent rep | **decoder-free** | online | state + pixel | 连续/离散均支持多 benchmark | 非显式 task-conditioned 多任务，但多 benchmark 支持好 | imagination actor-critic，非 MPC | 否 | DMC Proprio 500K；DMC Vision 1M；DMC Subtle 1M；Meta-World 1M；Atari 100k 400K；Crafter 1M；Memory Maze 100M | **官方仓库明确给出 benchmark budgets** | 官方未统一报告 | 官方未公开 GPU 小时；仅报告较其 Dreamer baseline 约 1.59× 更快 | **强可行**；单卡先跑 DMC/Meta-World 没问题 | **低到中** | **中**：仓库新 | **A+** | citeturn16search8turn6view2turn19search13 |
| **DreamerV3** | 2025, Nature | RSSM + reconstruction + actor-critic imagination | **reconstruction-based** | online | state + pixel，多域 | 连续/离散 | 论文层面跨 150+ tasks；公开代码非多任务库定位 | imagination actor-critic | 否 | 多环境；repo 有 atari/crafter configs，论文跨 150+ tasks | 官方无统一单任务默认；依 task 而变 | 官方 README 未统一给出 | **单 A100/GPU**；官方未给统一训练时长 | **可行**，但 JAX 工程不优 | 中 | 中 | **B+** 作为参考，不宜做主底座 | citeturn16search1turn16search9turn29search8turn27view0 |
| **TD-MPC2** | 2024, ICLR | implicit latent model + value-guided MPC | **decoder-free / implicit** | online + offline | state + DMControl rgb | 连续为主 | **支持**，含 mt30/mt80 | **显式规划强** | 否 | DMControl 39、Meta-World 50、ManiSkill2 5、MyoSuite 10 | 示例含 `dog-run steps=7000000`；不同任务默认不同 | **单任务默认 5M；多任务 1/5/19/48/317M** | 单任务在线推荐 **≥8GB 显存**；317M 训练需 **≥24GB** | **非常可行**；48GB 余量大 | 中 | 低到中 | **A** | citeturn6view1turn27view4turn20search8 |
| **IRIS** | 2023, ICLR | discrete autoencoder + autoregressive Transformer | 生成式 token world model | online | pixel | 离散 | 否 | 无显式 MPC | 否 | Atari 100k | Atari 100k 标准预算 | 官方未统一给出 | 官方 GPU 信息未找到 | **可行**，但不对齐主问题 | 中 | 中 | **B-** | citeturn19search3turn6view4turn20search10 |
| **STORM** | 2023, NeurIPS | stochastic Transformer world model | 生成式 / 非 decoder-free | online | pixel | 离散 | 否 | 无显式 MPC | 隐式随机性，不等于显式校准 uncertainty | Atari 100k | Atari 100k 标准预算 | README 给 2L512D8H 架构，但无总参数量 | **单 3090** 训练 Atari 100k agent 约 **4.3 小时**（作者报告） | **可行**，但方向偏 Atari | 中 | **高**：repo 已停止维护 | **C+** | citeturn7search4turn17view0 |
| **DIAMOND** | 2024, NeurIPS Spotlight | diffusion world model in pixel space | 非 Dreamer 派；高保真生成 | online | pixel | 离散 | 否 | 可 interactive simulation，但非典型 MPC | 否 | Atari 100k；CSGO demo | Atari 100k 标准预算；CSGO 额外 87h static gameplay WM demo | 官方未统一给出 | 官方 GPU/显存未清楚公开；训练时长未知 | **技术上可跑，但不适合作为首轮主线** | 高 | 中 | **B-** 作为对比灵感 | citeturn19search2turn16search15turn19search6turn6view3 |
| **TWM** | 2023 | Transformer-XL world model | token/sequence model | online | pixel | 离散 | 否 | 无显式 MPC | 否 | Atari 100k | Atari 100k 标准预算 | 未公开 | 未公开 | 可行但与主线偏离 | 中 | 中 | C | citeturn10search5turn9search2 |
| **WIMLE** | 2026, ICLR | IMLE world model + ensembles / latent sampling | stochastic world model | online MBRL | 官方页强调多模态 dynamics | 连续为主 | 否 | synthetic rollout weighting | **是** | 官方 code 可用 | 官方未给统一预算 | 未知 | 未知 | **方法上值得读，不适合首个复现对象** | 高 | 中高：较新 | B | citeturn35search2turn35search10turn35search14 |
| **Newt** | 2026, ICLR | language-conditioned multitask TD-MPC2 variant | implicit / multitask world model | online + demo pretraining | state / optional image / language | 连续 | **强**，200 tasks | planning + multitask adaptation | 否 | MMBench 200 tasks | benchmark 本身就是大规模 | 多模型尺度 | 工程上强调 accelerated pipeline，但对你太大 | **不建议** 作为首轮 | 高 | 高 | **No** for current project | citeturn36search1turn36search3turn36search17 |

在你的硬件约束下，一个最重要的判断是：**“能否单次训练装进显存”不是充分条件，关键是完整实验矩阵是否可承受。** 这意味着像 DIAMOND、Newt、WPT 这类方法，即便某个单次 run 未必绝对不可行，也很可能在“多任务 × 多种子 × 多基线 × 多消融”的实验维度上失控；而 R2-Dreamer / DreamerV3 / TD-MPC2 这类紧凑 latent world model 则更符合“消费级工作站完整做完实验”的现实边界。 citeturn6view2turn6view1turn36search1turn36search15turn32search10

**算力等级估算**

下面三档是我按你的约束给出的 **实验组织建议**。凡非官方报告的时间/显存，我都明确标为 **估算**。

| 实验等级 | 推荐内容 | 总环境步数 | GPU 并发策略 | 单卡峰值显存 | CPU / 内存 | 存储需求 | 预计运行结构 | 可提前停止 | checkpoint 复用 |
|---|---|---:|---|---|---|---|---|---|---|
| **等级 0 复现验证** | 2 个任务；1 seed；R2-Dreamer + TD-MPC2；优先 DMC Vision 或 state DMC | **约 0.5M—1.5M**（估算） | GPU0 跑 R2，GPU1 跑 TD2；同任务对齐预算 | R2：**约 12—24GB**；TD2：**约 8—16GB**（估算，结合官方最低建议） | **16—24 CPU cores；32—64GB RAM** | **50—200GB**（含 logs / checkpoints / 少量视频） | 先跑短 budget sanity run，再扩到最小可学习曲线 | **可以**：若日志、显存、吞吐或 reward 曲线异常立即停 | **高**：sanity checkpoint 可直接续跑 |
| **等级 1 选题可行性** | 4—6 tasks；3 seeds；R2 + TD2 + Dreamer baseline；关键消融 | **约 18M—45M**（按 1M 级预算估算） | 两张卡各自独立队列：一张主方法/消融，一张强基线/补种子 | **约 16—28GB**（R2 / Dreamer）；TD2 更低 | **24—32 CPU cores；64—128GB RAM** | **0.5—1.5TB** | 先 DMC Vision，再 CARL； shortest-to-longest 任务调度 | **可以**：明显失败的组件提前砍掉 | **高**：shared encoder / pretrained WM 可在同任务复用 |
| **等级 2 完整投稿实验** | 两个环境家族；8—12 tasks；3—5 seeds；完整 OOD / calibration / ranking / exploitability | **约 80M—200M**（估算，取决于任务数和 budget） | 仍坚持“一卡一 run”；不要靠复杂并行救场 | **约 16—32GB**；避免把模型做大到必须 FSDP | **32+ CPU cores；128GB RAM 更稳** | **1—3TB** | 按 family 分批：DMC 组与 CARL / Meta-World 组交替执行 | **部分可以**：早期就能淘汰弱 baseline 或低价值 shift 类型 | **中高**：同环境 checkpoint、同 backbone 可复用，但跨 shift 仍需重训 |

这些估算的依据主要来自两端：一端是 **R2-Dreamer 仓库对各 benchmark 给出的预算**，例如 DMC Vision / Meta-World 多为 **1M**，DMC Proprio 为 **500K**；另一端是 **TD-MPC2 官方对单任务在线 RL 的最低显存要求（8GB）与大模型训练要求（24GB for 317M）**。因此，对两张 48GB GPU 来说，**真正合理的组织方式是“多 run 并发”，不是“单个 run 堆大模型”**。 citeturn6view2turn6view1

## 路线A的候选研究方案

**H 面向 AAAI 的紧凑算法路线**

你的暂定主题 **“Calibrated Adaptive World Models for Robust Planning under Dynamics Shifts”** 是有潜力的，但前提是必须把论文核心收缩成一个**简洁、统一、可被实验证伪的科学假设**。如果把你列出的所有模块都堆进去——ensemble、多头动力学、calibration loss、multi-step consistency、adaptive horizon、uncertainty-penalized MPC、test-time context inference、online adaptation、policy-aware learning、防 exploit 正则——那几乎必然会被 AAAI 审稿人看成 **module soup**。相反，最有希望的版本应该只保留一条主线：**uncertainty 不是被动报告，而是主动控制 imagination 的使用方式。** 这与 P2P 的“uncertainty-foreseeing”思想相邻，但你可以把问题落到 **decoder-free / compact latent world model、dynamics shift、calibration 与 closed-loop decision utility** 上，从而形成和 P2P、RWM-U、ROMBRL 不同的论文身份。 citeturn35search8turn14search2turn35search11turn26search4

### 最佳中心假设

我最推荐的中心假设是：

> **若一个轻量级 decoder-free latent world model 能够对其多步预测误差给出可校准的 epistemic uncertainty，那么把该 uncertainty 用作“imagination control signal”而非仅作辅助诊断，将在未见动力学与 policy-induced OOD 下同时提升 closed-loop return、policy-ranking agreement 与 model exploitability robustness。**

这个假设之所以好，有四个原因。第一，它**足够聚焦**：围绕 uncertainty 的“用途”而非“存在”。第二，它**有清晰对照**：同样的 world model，同样的 uncertainty estimator，只比较“是否用 uncertainty 控制 imagination horizon / penalty / branch selection”。第三，它**适合你的算力**：不需要超级大模型，只需要在 R2-Dreamer 或其 Dreamer baseline 上加少量 heads 或小 ensemble。第四，它**契合 2026 评测风向**：不仅能报 return，也能报 calibration、ranking agreement、exploitability。 citeturn15search2turn16search8turn26search4turn14search7

### 哪些组件有新意，哪些已被做烂

**真正有研究新意、且与你的资源匹配的组合**，我认为是以下三类。

第一类是 **small latent ensemble 或 epistemic multi-head + calibration + adaptive imagination horizon**。这里的创新不是“有 ensemble”，因为 PETS、RWM-U、latent disagreement 都早就说明 ensemble 有用；创新点在于你把 **calibrated uncertainty** 转成一个 **horizon controller**，并且在 **R2-Dreamer 这类 decoder-free visual world model** 上验证其对 **CARL dynamics shift** 的闭环收益，这一组合截至 2026 年 7 月仍未被充分做透。 citeturn34search3turn14search2turn16search8turn21view0

第二类是 **policy-aware uncertainty calibration**。ROMBRL 强调 policy-driven adaptation，P2P 强调 uncertainty-foreseeing，但它们都不在你最关心的“轻量视觉 latent world model + online benchmark + strict compute budget”设置里。如果你把 uncertainty 的校准集或 calibration objective 设计成 **更贴近 actor 实际访问分布**，而不是只对 replay distribution 校准，那么这会比常规 post-hoc temperature scaling 更有科学味道。 citeturn35search11turn35search8turn14search7

第三类是 **exploitability-aware regularization**。2026 的 exploitability 理论给了你一个新评测抓手。如果你能证明：某个简单的 uncertainty-aware actor regularizer 不是仅提升了回报，而是 **降低了 ranking inversion / exploitability gap**，那么论文新意会明显更强。 citeturn26search4turn15search2

相反，**已经被做得比较充分、或很容易被质疑为 incremental 的东西** 包括：单独加一个 uncertainty head 却不做 calibration 和 decision-level usage；单独加 multi-step consistency loss 却不说明它如何改善 closed-loop utility；单独加 latent ensemble 但不做 parameter-matched baseline；以及 generic test-time adaptation / online adaptation 但没有明确 dynamics context 设定。单独看这些模块都不新，而组合过多又会显得“为了赢 benchmark 而堆件”。 citeturn14search2turn35search2turn35search11turn35search1

### 三个最有可能成功的方法设计

**设计一：CAWM-H**

这是我最推荐的 AAAI 主稿方案。核心是：在 **R2-Dreamer** 上增加一个 **小型 latent epistemic head**，用 **3-head transition predictor** 或 **small bootstrap latent heads** 近似 epistemic uncertainty；然后对 **h-step rollout error / reward error** 做一个轻量 calibration（可以是 reliability loss，也可以是 post-hoc isotonic / temperature-like monotonic calibrator，具体形式可简化）；最后让 actor imagination 时的 horizon 从固定值变成 **uncertainty-adaptive horizon**，例如当 cumulative epistemic risk 超阈值时截断 imagined rollout，或用 risk-adjusted returns 替代原想象回报。它与最近工作的差异在于：**不是仅估计 uncertainty，也不是仅惩罚 reward，而是直接控制 imagination 的长度与使用方式。** citeturn16search8turn35search8turn14search7turn15search2

**设计二：CAWM-C**

这个版本在 CAWM-H 的基础上增加一个 **短上下文窗口 context inference module**。你不要求知道 CARL 的真实 context label，而是让模型从最近 **K 个 transition** 推断一个低维 latent context，并把 uncertainty 分解为 “与当前 context mismatch 相关的 epistemic” 和 “环境内生噪声相关的 aleatoric proxy”。其价值不在于做全套 meta-RL，而在于说明：**当 dynamics shift 可被近期 transition 快速识别时，uncertainty-guided horizon control 可以变得更积极，不必一味保守。** 这和传统 contextual RL 的区别在于，你不是为了 few-shot optimal control，而是为了 **world model reliability gating**。 citeturn21view0turn37search7turn15search2

**设计三：CAWM-X**

这个版本面向“防止策略利用模型错误”。方法上保持轻量：仍用 R2-Dreamer backbone，但在 actor loss 中加入一项 **uncertainty-weighted conservative regularizer**，强制 actor 避免把概率质量推向 predicted exploitability high 的区域。一个最简单的实现就是：对 imagined trajectories 的 return 乘上一个基于 calibrated uncertainty 的衰减，或在 actor update 时惩罚 uncertainty-gradients 最大的动作方向。其亮点在于它直接对齐 **model exploitability** 指标，而不是只对齐 average return。 citeturn26search4turn15search2

### 我最推荐的具体论文版本

如果只能选一个最终 AAAI 版本，我会选 **设计一 CAWM-H**。原因很简单：它最统一、最清楚、最容易讲述，且在 7 页 AAAI-27 主文限制下更容易压缩。AAAI-27 目前官方要求是 **7 页技术正文 + references / checklist 额外页**，不是 8 页正文，所以你原先设想的“8 页会议论文”必须进一步提炼。 citeturn25view0

### 最小可发表实验

最小可发表实验不应该超过以下配置：

- 主基线：R2-Dreamer；
- 强对照：TD-MPC2、同仓库 Dreamer baseline；
- 环境：**DMC Vision** 2 个任务 + **CARL-DMC** 2 个 dynamics-shift 任务；
- shift：至少 **gravity** 和 **friction / mass** 两种；
- seeds：3；
- 指标：return、uncertainty calibration、policy-ranking agreement、horizon vs error-growth curve；
- ablation：无 calibration、固定 horizon、仅 uncertainty penalty、parameter-matched extra-head baseline。 citeturn6view2turn21view0turn15search2turn26search4

如果这套最小实验跑出来后，**ID return 不掉、OOD return 提高、ranking agreement 改善、uncertainty 与真实多步误差相关性显著增加**，那么论文已经有 AAAI 的雏形。真正重要的是：一定要有 **negative result-friendly** 的报告方式。若 calibration 提高但回报不升，也要坦诚说明“uncertainty quality 与 decision lift 并不自动一致”，这反而更学术。 citeturn15search2turn14search7

### AAAI 级完整实验

完整 AAAI 级实验，我建议分为四块。

第一块是 **ID 与 OOD 主结果**：DMC Vision + CARL-DMC，必要时附加 DMC-GB2。第二块是 **decision-centric metrics**：counterfactual fidelity、policy ranking、optimization lift、exploitability。第三块是 **可靠性诊断**：ECE/ENCE、coverage、uncertainty-error correlation、horizon sweep。第四块是 **成本与公平性**：同预算训练曲线、同参数量对照、one-GPU feasibility 附表。最多只额外加一个 **Meta-World MT10/MT1** 或 **Crafter** 家族作为跨 family 补充，不建议再加 Procgen、MiniGrid、Memory Maze 一起上，否则成本会迅速失控。 citeturn21view0turn22view0turn21view5turn22view4turn8search9turn15search2

### 必须包含的强基线与消融

**必须包含的强基线**：R2-Dreamer、TD-MPC2、Dreamer baseline。若你方法最终只在 R2-Dreamer 上有效，而在 Dreamer baseline 上效果微弱，这不是问题；但你至少要说明它为什么更适合 decoder-free world model。若审稿页数允许，再加一个 **P2P** 或 uncertainty-aware state MBRL 作为思想对照即可，不必强行全部复现。 citeturn16search8turn16search10turn35search8

**必须包含的消融**，至少有六项：  
其一，uncertainty estimator 的容量 ablation；其二，calibration on/off；其三，fixed-vs-adaptive horizon；其四，uncertainty used only for logging vs used for control；其五，parameter-matched extra-head baseline；其六，real context label vs inferred context（若用了 CAWM-C）。没有这些，AAAI 审稿人很容易认为收益来自额外参数量或更保守 actor，而不是来自你的核心思想。 citeturn14search7turn14search2turn26search4

### 最可能导致拒稿的原因

最可能的拒稿理由，我认为有五个。第一，**创新点看起来像“R2-Dreamer + uncertainty head 的自然延伸”**。第二，**没有强 decision-centric evaluation，只报 return**。第三，**dynamics shift 与 visual shift 混在一起，导致 claim 不清**。第四，**ensemble 增益无法排除只是参数量增益**。第五，**实验预算不公平，例如 Dreamer / TD-MPC2 / R2 在不同步数、不同预处理、不同 action repeat 下比较**。这五点必须提前在实验 protocol 上堵住。 citeturn15search2turn26search4turn6view1turn6view2

### AAAI 论文贡献组织与题目建议

按 AAAI-27 **7 页正文** 的现实限制，我建议贡献组织如下：第一页半写问题定义与评价缺口；接下来一页写方法假设与 uncertainty-as-control；再一页写学习目标与 calibration；两页写主实验与指标；半页写消融与失败案例；半页写局限与讨论。把复杂长表、环境实现、更多曲线全部放 supplement。 citeturn25view0

我推荐的英文标题有两个候选：

- **Calibrated Adaptive World Models for Robust Planning under Dynamics Shifts**
- **When to Stop Imagining: Calibrated Uncertainty for Robust Latent World Models**

摘要结构建议是：  
先指出 latent world models 在 unseen dynamics 与 policy-induced OOD 下的失败；  
再指出现有 uncertainty 多用于 passive diagnostics，而不是 controlling imagination；  
接着给出你的方法 —— compact decoder-free world model + calibrated epistemic estimation + adaptive imagination horizon；  
最后用一句话概括 DMC / CARL 上在 return、ranking agreement 和 exploitability 上的提升，并声明单 GPU feasibility。 citeturn15search2turn16search8turn26search4

## 路线B的候选研究方案

**I 面向 Information Sciences 或 Information Fusion 的系统路线**

Route B 的价值在于：它不需要和 Route A 争同一个“主创新点”。Route A 强调 **uncertainty controls imagination for robust planning**；Route B 完全可以强调 **如何融合多源、多时间尺度、质量不均、缺失或冲突的信息，使世界模型更可靠**。这里的关键不是比 AAAI 线“更大更全”，而是 **问题定义更系统、实验矩阵更完整、统计与敏感性分析更细**。 citeturn24view1turn24view0

### 更适合 Information Sciences 还是 Information Fusion

我的结论是：**更适合 Information Sciences，Information Fusion 只在你主动做“真正意义上的融合”时才值得冲。** 这不是贬低 Information Fusion，而是它的 scope 更严格。官方 Aims & Scope 明确写的是 **multi-sensor, multi-source, multi-process information fusion**，并列举了 **feature / decision / multilevel fusion、multi-look temporal fusion、imperfect / incomplete environments、resource optimization**。如果你只是把图像 embedding、proprio embedding 和 context embedding concat 后喂进一个 RSSM，那更像是普通 multimodal modelling，而不是 fusion research。相反，Information Sciences 对 intelligent systems、adaptive systems、modelling、information theory / data fusion / uncertainty 更宽容，只要你的理论解释、系统实验和统计分析足够扎实，就更容易成立。 citeturn24view0turn24view1

### 哪些定义足以构成真正的信息融合贡献

在你列出的候选定义中，**足以构成 Information Fusion 论文内核** 的，不是“多模态”本身，而是下面这些更严格的版本：  
其一，**图像观测、低维本体状态和环境上下文参数** 作为真正不同来源的信息，且存在 **missing/corrupted/asynchronous** 场景，由模型做 **confidence-weighted multilevel fusion**；  
其二，**快时间尺度 vs 慢时间尺度 dynamics** 的层次融合，不只是多层 RNN，而是明确处理不同 temporal evidence 在不同 horizon 上的可靠性；  
其三，**deterministic / probabilistic / ensemble predictors** 的动态融合，且融合权重由 uncertainty、missingness 和 compute budget 共同决定；  
其四，**epistemic 与 aleatoric uncertainty 的分解、再融合与校准**，并在冲突证据下进行 decision-level conflict handling。  
换句话说，Route B 若想冲 Information Fusion，方法框架里必须有“**source-aware, confidence-aware, time-aware fusion**”三件套。 citeturn24view0turn14search11turn33search4

### 最佳方法框架

我最推荐的 Route B 框架叫：

> **Uncertainty-Guided Multi-Source and Multi-Timescale Fusion World Model**

它包含三层。第一层是 **source-specific encoders**：pixel encoder、proprio/state encoder、context encoder。第二层是 **fusion-aware latent dynamics**：构建 fast latent（短时控制细节）与 slow latent（context / task / long-horizon regularity）两条时间尺度，并使用 uncertainty-gated fusion 把不同源的信息注入不同时间尺度。第三层是 **reliability head**：同时预测 rollout uncertainty、source confidence、missingness mask consistency，并支持 decision-level fusion 或 branch reweighting。这个框架最容易落在 Information Sciences；若想更偏 Information Fusion，可以把第二层替换为 **multilevel fusion block**，并显式处理 source conflict。 citeturn24view1turn24view0turn23academia14turn21view0

### 是否需要误差界、校准保证或复杂度分析

如果投稿 **Information Sciences**，我建议至少补三类分析：  
一是 **complexity analysis**，说明多源 fusion 相比单源 Dreamer/R2 的额外参数和推理代价；  
二是 **calibration analysis**，例如分 source、分 horizon 的 NLL / coverage / ENCE；  
三是 **statistical robustness analysis**，即 missing rate、noise scale、context corruption、fusion temperature 对结果的敏感性。  
如果你真的想试 **Information Fusion**，则最好再加一项 **conflict-aware theoretical argument**，如为什么某类 gating / product-of-experts / evidential combination 在 source 冲突时应更稳健；不一定需要完整误差界，但需要显式阐明“fusion 机制与 imperfect / incomplete information”的对应关系。 citeturn24view0turn24view1turn14search11turn33search4

### 至少两个环境家族与三种退化条件

我建议 Route B 的实验基座是：

- **DMC-VB**：因为它提供 **state + pixel pairs**，且 visual distractor 设计系统，非常适合做 offline / multimodal fusion。  
- **CARL-DMC**：因为它提供明确的 dynamics context，能把 context 作为第三信息源加入，并测试 context inference / missing context / noisy context。  
如需第三家族，优先加 **Meta-World**，因为它可以补 task shift 与 manipulation dynamics，但不是首发必要项。 citeturn23academia14turn21view0turn22view4

三种最重要的信息退化条件应当是：  
**多模态缺失**，例如 pixel missing、state dropout、context missing；  
**传感器噪声 / 污染**，例如 proprio Gaussian noise、pixel corruption、context label corruption；  
**异步 / 冲突证据**，例如 context 延迟、state 与 pixel time offset、不同 source 对未来 reward 给出不一致置信。  
这三类比单纯“加噪声”更有 fusion 味道，也更贴近期刊读者偏好。 citeturn24view0turn23academia14turn21view0

### 期刊论文实验矩阵与统计检验

期刊稿要比 AAAI 稿更系统。建议实验矩阵至少包含：

1. 两个环境家族：DMC-VB + CARL-DMC；  
2. 三类退化：missing modality、sensor noise、dynamics/context shift；  
3. 两个 horizon 维度：短期 planning（例如 5–15 steps）和长期 rollout（例如 30–50 steps）；  
4. 三类对照：single-source、naive concat、uncertainty-free fusion；  
5. 三到五个 seeds；  
6. 每组都报 **mean ± std / 95% CI**。 citeturn23academia14turn21view0turn24view1

统计上，我建议使用：  
**paired bootstrap over tasks × seeds** 估计主结果置信区间；  
**Wilcoxon signed-rank** 或 **paired t-test** 比较 task-level improvements；  
报告 **effect size**；  
并对 calibration 曲线做 **reliability diagram + slope/intercept + coverage deviation**。  
这套分析更像期刊稿，而不是会议稿。 citeturn14search11turn33search4

### 如何避免与路线A重复

Route A 与 Route B 的重叠会出现在 backbone 与部分 benchmark 上，但**中心贡献必须完全不同**。  
Route A 的命题是：**uncertainty 如何控制 imagination 与 planning**。  
Route B 的命题是：**不完备、多源、多时间尺度信息如何被可靠融合成更可信的 world model**。  
因此，Route A 可以只用 pixel + latent uncertainty；Route B 则必须把 **state / proprio / context / multi-timescale / missingness** 做成论文核心。Route A 的关键图是 “return / ranking / exploitability vs uncertainty-guided horizon”；Route B 的关键图则应是 “fusion under missing / noisy / asynchronous inputs vs single-source baselines”。 citeturn15search2turn24view0turn24view1

### 推荐题目与完整大纲

如果面向 **Information Sciences**，我推荐的英文题目是：

**Reliable World Models from Imperfect Inputs: Uncertainty-Guided Multi-Source and Multi-Timescale Fusion under Missing and Shifted Observations**

如果硬要瞄 **Information Fusion**，则可以写成：

**Conflict-Aware Multi-Source and Multi-Timescale Fusion for Calibrated World Models under Missing and Shifted Evidence**

一个适合期刊稿的完整大纲是：  
引言；相关工作；问题定义与 source degradation taxonomy；fusion-aware world model；uncertainty decomposition 与 calibration；theoretical / complexity analysis；benchmarks 与 data generation；主实验；missing/noisy/asynchronous sensitivity；统计检验；failure cases；结论。  
其中 **failure cases** 在期刊稿里非常重要，它能帮你证明 fusion 何时失效，而不是只展示最好结果。 citeturn24view1turn24view0

## 重叠、边界、最小复现与未来四周计划

**J 两条路线的重叠、边界与发表风险**

两条路线最健康的关系不是“一个 conference 短稿、一个 journal 扩展版”，而是 **共享 infrastructure、分离 hypothesis**。共享的部分可以包括：R2-Dreamer 工程底座、DMC wrapper、CARL integration、统一 logging、decision-centric evaluation toolkit、calibration plotting utilities。独立的部分则必须包括：Route A 的 algorithmic novelty、Route B 的 fusion formulation、环境条件、主指标、主图表和中心假设。否则会触发 AAAI 与期刊的双重风险：会议稿被质疑不够新，期刊稿被质疑只是扩展实验。 citeturn25view0turn24view1

从投稿风险看，**Route A 的最大风险是“看上去太 incremental”**；**Route B 的最大风险是“看上去不像真正的 fusion paper”**。前者要靠统一假设与 decision-centric metrics 解决；后者要靠 source-aware / time-aware / conflict-aware 的方法定义与多退化实验矩阵解决。 citeturn15search2turn24view0turn24view1

**K 推荐的最小复现计划**

第一步，不要先复现论文最强结果，而要先复现 **最小系统链路**。我建议前 7 天只做三件事：  
其一，**R2-Dreamer on DMC Vision** 的 1—2 个任务，确认安装、日志、显存、checkpoint、视频渲染全通。  
其二，**同仓库 Dreamer baseline** 跑同样任务，验证 unified codebase 的公平性。  
其三，**TD-MPC2 on matched DMC rgb tasks**，验证 planning-oriented 对照可用。  
这一步的目标不是性能，而是确保所有系统组件真实可运行。 citeturn6view2turn6view1

第二步，打通 **CARL-DMC**，先只选 **gravity** 与 **friction** 两类 context shift。只要能做到“同一任务、训练 context 固定、测试 context 改变”，你就已经拥有了 Route A 的核心实验条件。第三步，再引入 **DMC-GB2**，但只用 1 个 visual mode 做 sanity check，不要一开始全开。这样做的好处是：你能早期把 dynamics shift 与 visual shift 分开。 citeturn21view0turn21view5

**L 未来四周的调研和工程计划**

**第一周**：  
完成 R2-Dreamer、Dreamer baseline、TD-MPC2 的环境安装与最小训练；记录显存峰值、steps/sec、checkpoint 频率、video logging 代价；同时把 DMC / CARL wrapper 接口统一。 citeturn6view2turn6view1turn21view0

**第二周**：  
完成 DMC Vision + CARL-DMC 的等级 0 复现；实现基础决策型指标，包括 rollout error growth、uncertainty-error correlation、policy-ranking agreement 原型。不要急着写新算法。 citeturn15search2turn21view0

**第三周**：  
实现 Route A 最小方法：small latent ensemble 或 multi-head、简单 calibration、adaptive horizon；跑 2 个 DMC 任务 + 2 个 CARL shifts，先看曲线是否出现“校准改善但回报不升”“回报升但 ranking 不升”等分岔情况。若全部失效，立即转向更简单版本。 citeturn14search7turn26search4

**第四周**：  
根据第三周结果做第一次 Go / No-Go 分叉。  
若 Route A 已显示正信号，就扩到 3 seeds 和更多任务，开始整理 AAAI 叙事。  
若 Route A 信号弱，但你已打通 DMC-VB / state-pixel pairing，则可并行开启 Route B 的 fusion skeleton。  
若 R2-Dreamer 仓库在关键地方不稳定，就把 **TD-MPC2 提升为主对照 / 甚至新主线底座**，但保留 R2 作为研究对象。 citeturn23academia14turn6view1turn6view2

**你特别要求检查的风险，我的最终判断如下。**

- **新基线过于近期、代码不稳定**：R2-Dreamer 真实存在此风险，因为仓库很新、commit 很少；所以它是“高价值、但需等级 0 验证”的主基线，而不是无条件下注。 citeturn19search9turn6view2  
- **基线仓库结果无法复现**：STORM 已明确不再维护；DreamerV3 官方是 JAX；Meta-World 在 TD-MPC2 中有依赖兼容提醒。必须优先选择统一、可控的软件栈。 citeturn17view0turn6view0turn27view4  
- **环境版本 / MuJoCo 不兼容**：这是现实风险，尤其是 Meta-World。TD-MPC2 README 已明确提醒需要 MuJoCo 2.1.0 和旧 gym。 citeturn27view4  
- **不同观测预处理与训练预算导致不公平**：这是最常见审稿点。必须统一 DMC wrapper、frame stack / resize / action repeat、训练总步数，并同时报告 budget-normalized curves。 citeturn22view0turn15search2  
- **只提高最终回报但世界模型指标没改善**：按 2026 的评价趋势，这不够。必须同时报 calibration / ranking / exploitability。 citeturn15search2turn26search4  
- **只提高预测指标但闭环控制没改善**：同样不够；这正是你应规避的 claim/evidence mismatch。 citeturn15search2  
- **uncertainty 与真实误差不相关**：这是 Route A 最大技术风险，所以要先做“uncertainty usefulness diagnosis”，再做 actor 集成。 citeturn14search7turn14search2  
- **ensemble 提升仅来自参数量**：必须做 parameter-matched baseline。 citeturn34search3turn14search2  
- **OOD 测试泄漏训练分布**：DMC-GB2/CARL 必须在 split protocol 上写清楚。 citeturn21view5turn21view0  
- **任务过多导致成本失控**：首轮坚决不碰 Newt / WPT 规模；Route A 最多一个额外 family。 citeturn36search1turn36search15  
- **研究问题被 2025—2026 arXiv 已解决**：若你只是做 policy-aware uncertainty penalty，很容易撞到 P2P / ROMBRL / RWM-U；所以必须强调“calibrated uncertainty as imagination controller under dynamics shift”。 citeturn35search8turn35search11turn14search2  
- **方法只是给 Dreamer / TD-MPC2 加常规模块**：这就是最应该避免的写法。要围绕一个统一科学假设，而不是“拼组件赢表格”。 citeturn15search2turn26search4

综合所有证据，我的最终建议很明确：  
**主线选 R2-Dreamer；强对照用 TD-MPC2；环境核心选 DMC 生态 + CARL-DMC；AAAI 线只做一个统一问题——校准的不确定性如何控制 imagination；期刊线优先投 Information Sciences，围绕多源、多时间尺度、缺失与冲突条件下的可靠融合；Information Fusion 只有在你把 fusion 定义得非常硬时才值得尝试。**  
这套组合既尊重你当前的硬件现实，也最大化了论文在 6—12 个月内落地的概率。 citeturn16search8turn6view2turn16search10turn6view1turn21view0turn22view0turn21view5turn24view1turn24view0