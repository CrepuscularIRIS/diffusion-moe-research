# 复杂 AI 系统诊断的高信息增益实验设计深度研究

这份报告把你关心的“聪明、低成本、因果可解释、能快速排错”的实验模式，统一整理成一套面向复杂 AI 系统的诊断学方法库。核心观点很简单：**最有价值的实验不是“把模块删掉看会不会掉点”的普通 ablation，而是通过受控干预、上界构造、负对照、复现实验合同和配对统计设计，把竞争性失败机制彼此拉开。** 这类设计在因果推断中对应 intervention / negative control，在最优实验设计中对应 expected information gain，在序列决策中对应闭环-开环差距、分布漂移和局部反事实重放，在软件测试中对应 differential testing、metamorphic testing 与 oracle-deficient testing。citeturn8search8turn8search11turn21search10turn21search18turn3search2turn3search0

文中若出现“本文统称”字样，表示该术语在不同社区并不完全统一：例如具身智能里常说 oracle perception / oracle navigation，因果社区会说 intervention / counterfactual / negative control，软件测试社区会说 differential testing / metamorphic relation，而 agent 评测社区最近又强调 harness effects、replay/freeze policy 和 evidence-admission contract。把这些名字映射到一个诊断学框架，本身就是这份报告的主要价值之一。citeturn11search0turn11search6turn22search1turn22search10turn9search4turn3search10

## 实验设计分类法

如果把诊断实验按“它真正改动了什么”来分，最有用的分类不是按模型架构，而是按**干预对象**、**因果强度**、**离部署距离**和**能否快速排除一类解释**。干预对象大致有六类：输入信息、模态配对、内部状态与记忆、动作与控制、训练分布、评测与执行框架。因果强度从弱到强通常是：相关性分析 < 普通 ablation < 受控替换 < 反事实编辑 < 上界/下界构造 < 负对照与复现实验合同。离部署距离则从“纯评测时插拔”到“轻量探针训练”再到“需完整重训”。真正高价值的实验，往往是**评测时即可做、只改一个变量、能在几小时内强力区分两种失败机制**。这与最优实验设计、主动学习里“以最小代价最大化模型后验收缩/信息增益”的原则一致。citeturn21search10turn21search18turn21search9turn21search16

你特别要求区分的几组概念，最好写成实验前的“研究合同”。第一，**普通 ablation 不等于因果干预**：删掉一个模块通常同时改变容量、优化路径、接口分布和训练稳定性；而 oracle replacement、counterfactual corruption、negative control 则是在“其他条件尽量固定”的前提下改一个变量，因此更接近因果解释。第二，**诊断上界不等于可部署方法**：比如 shortest-path ceiling、oracle perception ceiling、oracle stop head，目的是定位瓶颈而不是给最终系统部署。第三，**随机噪声鲁棒性不等于持久偏置鲁棒性**：白噪声、时间相关噪声、常值偏置、漂移偏置和稀疏灾难性故障对应完全不同的机制。第四，**离线预测质量不等于闭环效用**：teacher-forced accuracy、token-level loss、state prediction quality 经常与 closed-loop utility 脱节。第五，**信息可得性不等于信息可用性**：给模型更多信息后若几乎不涨，瓶颈通常不在“缺信息”，而在表示、接口或策略。第六，**模态贡献不等于跨模态交互**：单独遮蔽某一模态只能看边际贡献，不能看 synergistic interaction。第七，**模型失败不等于评测 harness 失败**：近期 agent 评测已经明确表明，不同 harness、不同 replay/freeze policy、不同 evidence-admission contract 会显著改变结论。citeturn8search8turn8search11turn32search11turn1search11turn1search0turn17search7turn9search4turn22search7

对多模态、具身和多智能体系统，最值得优先做的不是“全量大扫除”，而是先做四类**快筛实验**。第一类是**上界类**：oracle perception、oracle control、oracle stop、shortest-path ceiling，这些实验能在几分钟内告诉你瓶颈大头是否压根不在该模块。第二类是**转换差距类**：teacher-forced vs closed-loop、offline vs rollout、seen vs unseen、clean vs corrupted，它们区分“监督拟合没问题但闭环崩”的经典失败模式。第三类是**对照类**：mismatched pairs、negative controls、ground-truth replay、paired episodes，这类实验最擅长发现隐藏泄漏、主观评测错误和 harness bug。第四类是**局部反事实类**：counterfactual modality edits、single-agent knockout、message pruning、history rewrite / history pruning，最适合复杂 agentic pipelines。citeturn24search2turn12search2turn11search0turn11search6turn1search0turn1search11turn18search1turn22search10turn30search3turn31search12turn10search2turn26search0

## 可复用实验模式总表

下面的总表按“跨任务可复用”而不是按论文流派组织。为保证可读性，我把它拆成两段连续表；成本等级是本文综合判断，分为**极低 / 低 / 中 / 高**，分别大致对应“纯评测分钟级”“纯评测小时级”“轻量重训或探针训练”“完整重训或大规模仿真”。

**总表上半部**

| 模式 | 核心科学问题 | 最小设置 | 关键控制变量 | 决定性度量 | 正 / 负 / 歧义解释 | 常见混杂与失效 | 代表工作 | 重训 | 成本 | 多模态具身 / 多智能体适配 | 方法句 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 特权信息注入 | 失败究竟来自缺失信息，还是不会使用已有信息？ | 在评测时给 agent 注入 GT 子目标、地图、状态或下一步提示 | 注入内容、带宽、时机、频率 | 任务增益 Δ 与 oracle ceiling 距离 | 正：信息瓶颈；负：策略/表示瓶颈；歧义：仅局部场景缺信息 | 注入格式改变了接口难度；hint 本身过强 | LUPI 与其后续、PRISM 的 oracle perception、LUMINA 的 oracle interventions。citeturn15search12turn15search0turn11search0turn31search12 | 否 | 低 | VLN 中注入 room ID / waypoint；MAS 中注入共享计划摘要或全局状态片段 | “We inject privileged state information only at evaluation time to test whether failures are information-limited rather than policy-limited.” |
| 特权上界与能力天花板 | 在理想子模块下，系统最高能到哪里？ | 用 oracle shortest path / oracle stop / oracle perception 计算 ceiling | 哪个子模块被理想化；是否允许完美 STOP | ceiling 与当前性能差值 | 大 gap：该子模块可能主导瓶颈；小 gap：优化该子模块回报有限 | 上界若改变任务定义，就不再是同一问题 | Habitat 的 SPL/最短路定义、VLN 的 OSR、SPOC 的 shortest-path imitation。citeturn7search4turn7search8turn24search2turn12search2 | 否 | 极低 | 具身导航可做 geometry-only ceiling；MAS 可做 oracle coordinator ceiling | “We report an oracle ceiling by replacing the target component with ground truth while keeping the downstream policy fixed.” |
| 信息质量阶梯 | 性能对信息质量下降的响应曲线是什么？ | 从 GT 到高质量估计再到低质量估计，逐级退化输入 | 噪声强度、缺失率、证据冲突、模态依赖度 | 性能-信息质量曲线斜率与拐点 | 早崩：脆弱；晚崩：接口健壮；分段崩：存在阈值效应 | 不同退化方式不可比；退化可能改变任务难度 | MM-AQA 的 evidence sufficiency / visual dependency、LVLM corruption benchmarking。citeturn23search0turn23search2turn16search10 | 否 | 低 | 可从 clean RGB→blur→遮挡→错配文本；MAS 可从完整共享状态→延迟摘要→压缩消息 | “We evaluate the policy along an information-quality ladder rather than a single clean/corrupt split.” |
| 组件级 oracle replacement | 谁是主瓶颈：感知、记忆、规划还是控制？ | 逐个把模块替换成 oracle，其余模块保持不变 | 被替换模块、接口契约、同步方式 | 每次替换带来的边际增益 | 单一模块大增益：主瓶颈明确；多模块都小增益：问题更像系统耦合或评测限制 | oracle 模块往往有更干净接口 | PRISM、Habitat OracleNavAction、LUMINA 的 planning/state/history oracle。citeturn11search0turn11search6turn31search12 | 否 | 低 | 先 oracle perception，再 oracle navigation，再 oracle stop；MAS 可逐个 oracle 某 agent 的计划或记忆 | “Each subsystem is replaced with an oracle in isolation to estimate its marginal diagnostic value.” |
| 时间局部 oracle 脉冲 / 状态重置 | 错误是局部可恢复的，还是一旦偏航就不可逆？ | 在若干时刻短暂给 oracle 修正，或 reset 到已访问状态 | 脉冲时机、持续步数、reset 位置 | 单次干预后的恢复率与长期成功率 | 少量脉冲即可恢复：局部纠偏足够；频繁脉冲仍无效：深层瓶颈 | 脉冲可能改变探索分布 | The Power of Resets、stochastic resetting。citeturn31search0turn31search8turn31search6 | 否 | 低 | 具身导航可在拐角或 first error 后 reset；MAS 可在冲突回合插入共享一致性修正 | “We apply sparse oracle corrections at selected timesteps to identify whether failures are locally recoverable.” |
| 置信门控 / 选择性部署 | 模型知道自己不知道吗？ | 保留 base policy，仅加 confidence gate / abstain option | 置信阈值、拒答代价、覆盖率目标 | risk-coverage curve、AURC、hazard blocking | 风险随 coverage 快速下降：可校准；几乎不降：过度自信或分数无信息 | confidence 可能只反映 prompt style，不反映任务风险 | Selective Classification、MM-AQA、autonomous agent abstention benchmarks。citeturn4search0turn4search8turn23search0turn23search1 | 否 | 极低 | 具身 agent 可在证据不足时暂停求助；MAS 可只在高不确定节点启动协作 | “We evaluate selective deployment by sweeping confidence thresholds and plotting risk against coverage.” |
| 反事实模态腐蚀 | 某模态的错误是通过单模态捷径还是跨模态交互传播的？ | 瞄准单一模态做可控 corruption / contradiction | 腐蚀种类、强度、持续性、是否与其他模态冲突 | 性能下降、校准漂移、跨模态一致性变化 | 仅腐蚀某模态即崩：高度依赖该模态；出现矛盾时反而自信：融合失真 | 腐蚀可能破坏语义而非仅降质 | Treble Counterfactual VLMs、LVLM corruption benchmarks。citeturn16search5turn16search9turn16search10 | 否 | 低 | 比如只腐蚀深度、音频或文本；MAS 可只腐蚀某个 agent 的私有观测 | “We counterfactually corrupt one modality at a time to separate modality reliance from cross-modal fusion quality.” |
| 错配对照 / shuffled modality / mismatched pair | 模型到底在做 grounding，还是在利用统计偏差？ | 打乱图文、观测-指令、agent-message 配对但保留边缘分布 | 打乱子空间、是否保持词袋/对象频率 | 正例-负例差、chance gap | 错配后仍高分：大概率有泄漏或 shortcut；错配即归零：至少依赖配对 | 错配过强会造成“太容易”的伪证据 | Winoground、SugarCrepe、Mismatch Quest。citeturn27search0turn27search2turn18search1turn18search7turn16search3 | 否 | 极低 | VLN 可打乱 instruction 与 trajectory；MAS 可打乱消息来源 ID 与内容 | “We construct mismatched-pair controls that preserve marginal statistics while destroying the causal pairing.” |
| 必要性-充分性测试 | 某特征/模态/消息是“必要”的、“充分”的，还是两者都不是？ | 做 remove-only 与 inject-only 两组对照 | 删除对象、注入对象、注入位置与强度 | PNS 风格指标、remove gap 与 inject gain | remove 大 / inject 也大：既必要又充分；仅 remove 大：必要非充分；仅 inject 大：可替代线索存在 | remove 可能触发 OOD；inject 可能格式不自然 | 多模态 PNS 表征学习、Treble 的 direct-effect 分解。citeturn17search1turn16search5 | 否 | 低 | 对 VLN 可删 landmark 再注入 GT landmark；MAS 可删某条消息再注入 oracle 消息 | “We test necessity with removal and sufficiency with controlled insertion under matched contexts.” |
| 几何上界 / 仿真动作空间上界 | 失败是不是来自动作空间或几何约束，而非认知模块？ | 用最短路或 oracle nav 执行几何可达的最优动作 | 是否忽略感知误差、是否允许碰撞最优解 | SR/SPL 与 shortest-path ratio | 几何上界高而真实性能低：更像感知/策略问题；几何上界也低：任务本身受物理/动作空间限制 | 上界可能依赖 simulator 特权 | Habitat shortest-path metrics、OracleNavAction、SPOC。citeturn7search4turn7search8turn11search6turn12search2 | 否 | 极低 | 适合 ObjectNav、VLN-CE、移动操作 | “We estimate a geometry-only ceiling by replacing decision-making with shortest-path or oracle-navigation rollouts.” |
| GT replay / harness validation | 低分是模型错，还是 evaluator / harness / environment contract 错？ | 回放 GT 轨迹、已知可行工具序列或 reference solution | replay policy、冻结版本、证据准入标准 | GT 是否被判成功、日志是否一致 | GT 都过不了：先修 harness；GT 能过但模型过不了：才看模型 | 数据版本漂移、环境非确定性 | Executable benchmarking suite 的 replay/freeze contract、Harness-Bench。citeturn22search1turn22search7turn22search10turn9search4 | 否 | 极低 | 工具 agent 可回放 reference tool trace；具身 agent 可回放 expert demonstration | “Before attributing failures to the model, we replay a verified reference trajectory through the exact evaluation harness.” |
| 教师强制与闭环转换差距 | 离线学得好为什么闭环跑不好？ | 同一模型同时报告 teacher-forced、student-forced、closed-loop | rollout 来源、暴露比例、解码策略 | conversion gap = offline metric − closed-loop utility | gap 大：暴露偏差/误差累积；gap 小：问题更像信息不足或目标错配 | teacher-forced 指标常高估实际控制能力 | DAgger、Scheduled Sampling、Speaker-Follower、UT。citeturn1search0turn1search11turn2search1turn0search0 | 视实现而定 | 低到中 | VLN 几乎必做；MAS 可做 oracle history vs self-generated history | “We quantify the teacher-forced to closed-loop conversion gap under matched models and data.” |
| 暴露偏差 / covariate-shift probe | 性能是否主要被自生成历史带来的分布漂移摧毁？ | 从 expert prefix 逐步混入 agent-generated prefix | 混入比例、步长、回滚策略 | 错误随 prefix 污染比例的增长曲线 | 早期陡降：高暴露偏差；平缓：更像稳态能力不足 | prefix 污染同时改变难样本比例 | DAgger、Scheduled Sampling、online imitation in navigation。citeturn1search0turn1search11turn2search4 | 可选 | 低到中 | 对具身任务尤其有效；MAS 可对共享白板/记忆做 prefix pollution | “We interpolate between expert-generated and agent-generated histories to probe covariate-shift sensitivity.” |
| 跨分布 train-test 矩阵 | 系统在什么分布变化下失效，变化类型是否可分解？ | 以 domain × test-domain 矩阵而非单一 split 评估 | 场景、时间、传感器、语言风格、动力学 | 矩阵热图、worst-group、OOD gap | 若只在少数维度崩：机制较明确；若全矩阵都差：基础能力不足 | 选模策略会掩盖 DG 结论 | WILDS、DomainBed、OoD-Bench。citeturn20search0turn20search8turn20search6turn20search14turn20search9 | 否 | 低到中 | VLN 可 scene×instruction-style×embodiment；MAS 可 task family×team topology | “We evaluate a full train–test distribution matrix to localize which shift dimension actually breaks the system.” |

**总表下半部**

| 模式 | 核心科学问题 | 最小设置 | 关键控制变量 | 决定性度量 | 正 / 负 / 歧义解释 | 常见混杂与失效 | 代表工作 | 重训 | 成本 | 多模态具身 / 多智能体适配 | 方法句 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 第一不可逆错误定位 | 任务何时“已经输掉了”，而不是最后一步才失败？ | 标注 first irreversible error 或 decisive failure step | 不可逆定义、容错窗口、任务子阶段 | 到首错步的存活曲线、首错类型分布 | 早错主导：应做早期感知/对齐；晚错主导：应做 stopping/recovery | 短暂偏航未必不可逆 | ALFRED 的不可逆状态变化、Who&When、VerifyMAS。citeturn7search1turn19search10turn19search5turn19search1 | 否 | 中 | 对长程操作、导航和多 agent 协作都极有价值 | “For each failed episode, we localize the first irreversible error rather than only the terminal failure.” |
| 结构化错误注入 | 系统对哪类现实故障最脆弱：常值偏置、漂移、时间相关噪声还是稀疏灾难？ | 在传感器、动作或消息通道中按模板注入错误 | 幅度、持续时长、自相关、稀疏率 | 失败率、恢复时间、校准恶化 | 只怕偏置不怕白噪声：估计/校准问题；只怕稀疏灾难：恢复机制弱 | 注入分布若不真实，诊断外推性差 | AV fault injection、GRAD 的 temporally-coupled perturbations、steering bias faults。citeturn32search1turn32search4turn32search11turn32search8 | 否 | 低 | VLN 可对深度、里程计、STOP logits 注入；MAS 可对消息延迟/丢包/恶意包注入 | “We inject parameterized bias, drift, temporally-correlated noise, and sparse catastrophic faults to separate robustness regimes.” |
| 残差匹配合成误差 | 真实世界 residual 与合成噪声不一致时，结论还成立吗？ | 先拟合真实误差残差，再按残差统计生成 synthetic corruption | 残差分布、协方差、频谱、上下文依赖 | synthetic-real gap 在 matched / unmatched 下的变化 | matched 才能复现问题：说明过去 robustness 实验失真；两者都复现：机制较稳 | 残差估计本身可能偏 | Mind the Residual Gap、audio-visual sim2real 中测量 spectral difference。citeturn6search6turn6search1 | 否 | 中 | 适合 sim2real、传感器建模、跨模态同步误差 | “Synthetic perturbations are sampled to match the empirical residual statistics observed in real deployments.” |
| 变形 / 等变测试 | 模型是否满足应有的不变性或可逆性关系？ | 构造旋转、平移、尺度、坐标变换、动作逆操作等 follow-up case | 变换族、强度、组合顺序 | metamorphic relation violation rate | 违例高：实现 bug 或表征不稳；违例低但原任务仍差：问题在别处 | 某些任务天然不应完全不变 | Metamorphic testing review、DeepTest、DeepXplore、LLMORPH。citeturn3search2turn3search10turn3search1turn3search0turn0search6 | 否 | 极低 | 具身任务尤其适合坐标系与动作逆变换；MAS 适合 agent renaming / permutation invariance | “We verify metamorphic relations under controlled geometric and coordinate transformations instead of relying on pointwise labels only.” |
| oracle 感知配 learned control 与其对偶 | 系统是 perception-limited 还是 control/planning-limited？ | 运行两组：oracle perception + learned policy；learned perception + oracle control | 感知 oracle 形式、控制 oracle 粒度 | 两组 ceiling 的相对差距 | 前者高后者低：感知已够、控制差；前者低后者高：感知主导；都低：世界模型/任务理解问题 | 两个 oracle 接口不对称 | PRISM、Habitat oracle navigation。citeturn11search0turn11search6 | 否 | 低 | 这是多模态具身系统最该优先做的对偶实验之一 | “We compare oracle-perception/learned-control against learned-perception/oracle-control under matched tasks.” |
| 动作分量替换 | 是哪个动作子通道在拖后腿：STOP、转向、速度、抓取、消息发送？ | 只替换一个 action component 为 oracle | 被替换分量、替换频率、分量耦合 | 单分量替换带来的 Δsuccess | 仅替换 STOP 就大涨：停止判定是瓶颈；仅替换 heading：方向控制是瓶颈 | 连续动作分量可能强耦合 | Mind the Gap 里的 OSR/SR 分离、OracleNavAction。citeturn24search2turn11search6 | 否 | 极低 | 对导航、操作、消息发送频率控制都好用 | “We replace one action component at a time with an oracle to identify the control bottleneck.” |
| 因果记忆控制 | agent 失败是因为没记住、记错、写坏，还是不会检索？ | 比较 no-memory、registered memory、agent-written memory、expert-written history、history-pruned history | 写入策略、摘要粒度、检索窗口、冲突处理 | 多轮任务成功率、冲突解析率、记忆污染率 | expert history≫agent history：写入质量瓶颈；registered≫unregistered：检索/索引瓶颈 | 更长上下文可能只是 token 更多，不是 memory 机制更好 | MemoryAgentBench、MemoryArena、LUMINA。citeturn25search3turn25search7turn25search15turn31search12 | 否 | 低 | MAS 中可对共享黑板、私有记忆和摘要代理分别做对照 | “We compare expert-authored, agent-authored, and pruned histories to isolate memory registration and retrieval failures.” |
| 风险-覆盖与 abstention | 在需要安全保守的场景里，拒答/暂停值不值？ | 允许 agent abstain，并画风险-覆盖曲线 | abstain trigger、授权条件、证据缺口类型 | Safety Rate、Usability Rate、AURC | 可在小覆盖损失下大降风险：值得部署；几乎无改善：分数不可校准 | benchmark 若默认“必须行动”，会系统性压制 abstention | Selective Classification、MM-AQA、autonomous abstention competence。citeturn4search0turn23search0turn23search1 | 否 | 极低 | 适合工具 agent、医疗 VLM、企业 agent、协作 swarms | “We evaluate abstention as a first-class action and report risk–coverage trade-offs rather than forced-answer accuracy alone.” |
| 集合值 / 软专家动作监督 | 专家是否其实允许一族动作，而不是单点动作？ | 用 action set、soft labels 或 teacher distribution 替代 hard label | 集合宽度、teacher entropy、温度 | set-consistency、closed-loop robustness | set-supervision 更稳：原来的 hard labels 过刚；无差异：单点标签足够 | set 太宽会丧失辨识力 | CLIC / set-valued action supervision。citeturn29search0turn29search3 | 常需轻量训练 | 中 | 适合连续控制、语言行动空间与多解任务 | “We replace pointwise expert actions with set-valued or soft supervision to test whether label over-specificity is the bottleneck.” |
| 配对 episode 统计评估 | 观察到的小提升是真进步，还是种子噪声？ | 用相同 seeds / 相同任务实例配对比较 A 与 B | 公共随机数、paired seeds、bootstrap 方案 | paired delta、BCa CI、sign-flip test | paired 显著而 unpaired 不显著：原评估方差过大；都不显著：别过度宣称 | 若配对不严格，同步失配会污染效应 | paired bootstrap、paired seed evaluation、common random numbers。citeturn30search2turn30search6turn30search0turn30search4turn30search3 | 否 | 极低 | 导航同地图同指令同随机扰动；MAS 同任务同 agent 初始化 | “All model comparisons use paired episodes with shared randomness and confidence intervals on per-episode deltas.” |
| 失败转移矩阵 | 系统是“偶发失手”还是“进入坏状态后一路恶化”？ | 把轨迹分成若干 failure states，统计转移矩阵 | 状态定义、窗口大小、是否含恢复态 | 失败吸收率、恢复概率、状态间转移熵 | 高吸收：需要早检和 reset；高恢复：局部修补足够 | 状态划分过粗会丢失机制 | Who&When、FMMDP。citeturn19search5turn13search18 | 否 | 低到中 | 适合长程具身与协作流程 | “We summarize trajectories with a failure-transition matrix to distinguish recoverable deviations from absorbing failure modes.” |
| 负对照 / shortcut / leakage 检测 | 模型是否利用了与目标无关的作弊线索？ | 设计 negative control exposure / outcome，或 blind baseline | 对照变量选择、共享 confounder、盲模型能力 | 盲模型得分、negative-control effect | 盲模型高分或负对照显著：高度可疑；负对照无效：更可信 | 负对照选错会失去诊断力 | Negative control 方法综述、SugarCrepe、contamination surveys。citeturn8search11turn8search15turn18search1turn18search13turn9search3turn9search19 | 否 | 极低 | 可做 image-blind、text-blind、tool-blind、identity-blind baseline | “We include negative controls and blind baselines to detect shortcut learning, leakage, or benchmark contamination.” |
| 廉价 kill test | 这条研究路线值得完整训练吗？ | 先在 frozen features / tiny probe / few-shot setting 上做快筛 | probe 类型、样本量、是否冻结 backbone | 低成本 proxy 与最终目标的单调性 | 若最简单上界都打不开：大项目应先停；若快筛强：再投 full-scale 训练 | proxy 相关性不足会误杀好想法 | linear probing 作为表示快筛、representation evaluation protocols。citeturn28search1turn28search0 | 常为轻量训练 | 极低到低 | 可在 frozen VLM 表征上做导航目标预测或消息价值预测 | “We use a frozen-representation probe as a kill test before committing to full end-to-end training.” |
| 随机误差 vs 持久偏置与过度承诺 | 错误是随机波动，还是系统性偏向并伴随过度自信？ | 对比白噪声、常值偏置、漂移偏置、间歇偏置 | 偏置形态、自相关、置信阈值 | 平均误差、偏差方向、ECE、拒答率 | 对偏置极敏感但对白噪声还好：校准/坐标系问题；高置信持续错：commitment failure | 偏置可能被后处理抵消 | sensor/actuator bias studies、temporally-coupled RL robustness、MM-AQA。citeturn32search8turn6search4turn32search11turn23search0 | 否 | 低 | 适合深度/里程计/消息可信度诊断 | “We separately test random noise, persistent bias, and overconfident commitment because they imply different bottleneck classes.” |
| 限制源差分面板 | 系统更像 perception-limited、representation-limited、supervision-limited、policy-limited、action-space-limited 还是 evaluation-limited？ | 组合做 oracle perception、oracle control、teacher-forcing、shortest-path ceiling、GT replay | 面板中的每一项是否保持接口一致 | 各 ceiling / gap 的相对排序 | 通过排序直接给出优先修复顺序 | 若面板项目接口不统一，会误导排序 | PRISM、LUMINA、Habitat oracle nav、Harness-Bench。citeturn11search0turn31search12turn11search6turn22search10 | 否 | 中 | 这是把多个快筛组装成一个可复用诊断 protocol | “We run a bottleneck panel of matched interventions to rank likely limiting factors across perception, policy, action space, and evaluation.” |
| 差分测试 / cross-referencing oracles | 谁错了：模型本身，还是某个实现 / harness / backend？ | 在同一输入上比较多个独立系统或多个 harness | 比较对象数量、共享输入、判定规则 | disagreement rate、corner-case yield | 少数系统离群：更像实现或配置问题；普遍一致失败：更像任务本身难 | 多系统若共享缺陷，会形成假共识 | DeepXplore、Harness-Bench。citeturn3search0turn3search12turn9search4 | 否 | 低 | 对 tool-using agents、VLM backends、不同感知栈尤其有效 | “We use differential testing across independently implemented systems to expose corner cases without manual labels.” |
| 单 agent 反事实敲除 / credit assignment | 团队奖励该归因给谁，单个 agent 或单步动作到底有多关键？ | 固定其余 agent，仅对一个 agent 的动作或存在做反事实替换 | 敲除对象、固定上下文、基线定义 | counterfactual value / marginal contribution | 大边际贡献：关键 agent / 决策；贡献接近零：冗余或替代性强 | 直接删 agent 可能改变协作结构 | COMA、Exact Is Easier、AXIS。citeturn10search2turn10search17turn10search0turn9search6 | 否 | 中 | 适合 AgentSwarm、协作规划、swarm robotics | “We estimate each agent’s contribution through counterfactual action substitution while holding teammates fixed.” |
| 消息 / 通道 / 拓扑干预 | 多智能体增益来自有用通信，还是来自冗余 token 堆积？ | 对消息做 pruning、延迟、带宽压缩或拓扑重连 | 消息预算、图拓扑、剪枝规则 | 性能-通信曲线、CMV、成本-收益比 | 轻剪枝不掉点：通信冗余；换拓扑大幅掉点：协调方式是瓶颈 | 剪枝也会改变推理深度 | AgentPrune、CMV、AGP、BVME、MultiAgentBench topology study。citeturn26search0turn26search9turn26search8turn10search1turn26search4turn7search15 | 否 | 低到中 | 对 AgentSwarm 最有复用价值 | “We intervene on communication budget and topology to test whether collaboration gains come from useful messages or redundant chatter.” |

## 多模态具身智能体最值得优先做的十个实验

对多模态 embodied navigation、VLA、VLM 控制器而言，我认为信息增益最高的十个实验，不是“最大而全”，而是“最能在一天内砍掉错误研究方向”的那类。

首先应做的是**oracle 感知 vs oracle 控制的对偶替换**。这几乎是所有具身系统的第一诊断实验，因为它直接区分 perception-limited 与 control/planning-limited。PRISM 已明确采用 oracle perception 来隔离视觉检测误差，而 Habitat 则提供了 oracle navigation action 这种近乎现成的控制上界。若 oracle perception 一上就涨很多，而 oracle control 涨幅小，说明视觉 grounding 是主瓶颈；反之则是规划/控制问题。citeturn11search0turn11search6

第二是**teacher-forced vs closed-loop conversion gap**。在 VLN、长程操作和 instruction following 中，很多系统 teacher-forced 指标看起来不错，但一 rollout 就崩。DAgger、Scheduled Sampling 和 VLN 社区关于 teacher forcing / student forcing 的长期经验都说明，这个 gap 是诊断 compounding error、exposure bias 和 self-history 污染的最直接信号。citeturn1search0turn1search11turn2search1

第三是**oracle stop / action-component substitution**。VLN 社区已经明确观察到 SR 与 OSR 之间存在长期被忽略的 gap；高 OSR、低 SR 通常意味着 agent 已经经过目标附近，但“不会停”或“停错了地方”。因此在导航里单独替换 STOP、在操作里单独替换 grasp trigger、在 VLA 里单独替换 termination head，是极其便宜但异常锋利的实验。citeturn24search2turn24search6

第四是**geometry-only ceiling**。如果 shortest-path / oracle nav ceiling 本身就不高，你就不该把精力主要花在感知编码器上；相反，如果 geometry-only ceiling 很高但真实成功率很低，问题更可能在多模态 grounding、策略学习或 stop logic。Habitat 的 SPL 与 shortest-path 定义、SPOC 的 shortest-path imitation 都说明了这种 ceiling 的诊断价值。citeturn7search4turn7search8turn12search2

第五是**第一不可逆错误定位**。ALFRED 的任务天然包含不可逆状态变化，因此特别适合标记“哪一步开始已经输掉了”。对具身系统来说，terminal failure 往往把真正原因淹没在 cascaded error 里；first irreversible error 则能把“错过关键拐角”“抓错第一次对象”“把不可逆对象处理错”从后续连锁失败里切出来。citeturn7search1turn19search10

第六是**反事实模态腐蚀 + 错配对照成对使用**。单做 corruption 只能告诉你“噪声时会掉点”，但做成对实验——例如“只腐蚀图像”“只腐蚀文本”“图文互相矛盾”“图文错配但边缘分布不变”——就能把“模态边际贡献”“跨模态交互质量”“shortcut 依赖”三件事区分开。Winoground、SugarCrepe、Treble Counterfactual VLMs 的价值正在于此。citeturn27search0turn18search1turn16search5

第七是**结构化误差注入而不是只加 i.i.d. 白噪声**。真实机器人更常见的是常值偏置、漂移、时间相关误差和稀疏灾难性错误，而不是独立同分布噪声。GRAD 明确把 temporally-coupled perturbations 当成与传统鲁棒 RL 不同的问题；自动驾驶 fault injection 与 actuator bias 文献也表明，常值偏置、漂移偏置和间歇故障的表现机制截然不同。citeturn32search11turn32search8turn32search4

第八是**跨分布 train-test 矩阵**，而非单一 unseen split。对具身任务，最好至少把 scene、language style、sensor fidelity、embodiment 或 dynamics 拆成矩阵，否则你只能知道“unseen 差”，却不知道差在语言、视觉、运动学还是仿真 fidelity。WILDS、DomainBed 和 OoD-Bench 提供了非常成熟的矩阵化思维。citeturn20search0turn20search6turn20search9

第九是**GT replay / harness validation**。在能回放 expert demonstration 的任务里，这一步应该被视为必做 sanity check。Recent agent benchmarking work 明确强调 replay/freeze policy 和 evidence-admission contract；对 embodied simulators 同样适用——在归咎模型之前，先确认 evaluator 会把 reference solution 判成成功。citeturn22search1turn22search10turn9search4

第十是**限制作源差分面板**。把前九项中的少数关键实验以统一接口合成一个 bottleneck panel，可以非常快地给出优先级排序：perception 上界、control 上界、teacher-forcing gap、stop 替换、geometry ceiling、GT replay。这个面板式设计的优点不在于“新”，而在于它能把“信息不足、表示不足、监督不足、策略不足、动作空间不足、评测不足”放在一张图里比较。citeturn11search0turn11search6turn22search10

## 多智能体与 AgentSwarm 最值得优先做的十个实验

多智能体系统的最大问题，不是单体能力差，而是**归因难、接口多、协作成本高、评测容易被 harness 和协议设计污染**。因此高价值实验与具身系统相似，但重点更偏向 credit assignment、消息因果性和 memory/harness。

第一优先是**单 agent 反事实敲除 / credit assignment**。COMA 用 counterfactual baseline 解决多智能体 credit assignment，近期 “Exact Is Easier” 进一步指出，简单“移除一个 agent 看效果”常常扭曲了本来要测的贡献。对 AgentSwarm，正确做法通常是固定队友与任务上下文，只替换某 agent 的某个动作或消息。citeturn10search2turn10search17turn10search0

第二是**消息剪枝与 message value 评估**。如果轻度 pruning 不掉性能，说明 swarm 的增益主要不是“更聪明地协作”，而可能只是因为更长上下文带来偶然好处。AgentPrune、CMV 和带宽约束通信文献把这一点做得很清楚：消息必须被当成可干预变量，而不是默认越多越好。citeturn26search0turn26search9turn26search8turn26search4

第三是**通信拓扑干预**。MultiAgentBench 已经在星型、链式、树型、图型等多种 protocol 上评测；如果拓扑一换结果就变，瓶颈往往不在 base model，而在 orchestration design。如果拓扑怎么换都差不多，则协作层可能只是“表面复杂”。citeturn7search15turn7search7

第四是**共享记忆与历史重写控制**。MemoryAgentBench 和 MemoryArena 都强调，memory agent 的核心不是单次检索，而是多轮写入、冲突解析和跨会话依赖。对 AgentSwarm，最有信息增益的对照是 expert-written shared memory、agent-written shared memory、history-pruned summary 和无记忆四组对比。citeturn25search3turn25search15turn31search12

第五是**abstention / authority gap 实验**。近期 agent benchmark 的一个关键批评是：很多框架默认“继续行动”总比“拒绝行动”好，这会系统性强化 compliance bias。对企业 AgentSwarm 尤其如此——没有足够授权、证据或工具访问时，最好的行为经常是暂停、上报或请求确认。citeturn23search1turn23search4

第六是**反事实证据编辑**。医疗多智能体诊断最近的工作表明，“如果删掉这个症状 / 改写这条证据，诊断会不会变”是非常强的 hypothesis test。把同样的设计移植到 AgentSwarm，可以直接检测某条 observation、某条消息或某个共享结论是否真在驱动团队决策。citeturn31search7turn31search3

第七是**配对 episode 统计评估**。多智能体系统常常方差更高、路径更多、交互更长，因此 paired episodes、shared randomness 和 bootstrap CIs 在这里尤其重要。否则团体协议的一点小改进，很容易只是 seeds 与 sample path 差异。citeturn30search2turn30search0turn30search3

第八是**失败归因与 decisive error localization**。Who&When 与 VerifyMAS 之所以有价值，在于它们不再问“这个系统总分多少”，而是问“哪个 agent 在什么时候把任务带进不可恢复区域”。这对 AgentSwarm 几乎是必要条件。citeturn19search5turn19search1

第九是**harness A/B 与 orchestration effect 测试**。Harness-Bench 的结论非常重要：模型能力和 harness 配置经常缠在一起。对 AgentSwarm，这意味着你必须把 coordinator 策略、工具调用约束、工作空间隔离、日志裁剪、超时策略视为实验变量。否则“换模型涨了”可能其实是“换 harness 涨了”。citeturn9search4turn22search10

第十是**blind baseline 与负对照**。如果去掉图像、去掉工具结果、去掉 agent identity、甚至只保留流程模板仍能得到高分，说明 benchmark 或 swarm 协议里存在严重 shortcut。多智能体系统尤其容易被 agent role naming、任务模板、工具返回格式等伪线索污染。citeturn8search11turn18search13turn9search3

## 基于症状选择下一个诊断实验的决策树

如果你现在只能再做一个实验，我建议按下面这棵“症状驱动树”走，而不是随机再加 ablation。

当**离线指标高、闭环成功率低**时，先做**teacher-forced vs closed-loop conversion-gap**；若 gap 很大，再做**expert-history vs self-history** 和 **first irreversible error localization**，优先排查 exposure bias 与 compounding error。citeturn1search0turn1search11turn19search5

当**系统经常“走到附近却不算成功”**时，先做**oracle stop / action-component substitution**，再看 **OSR-SR gap** 或其任务等价物；若只替换 STOP 就显著上涨，不要先改 backbone。citeturn24search2turn24search6

当**怀疑是感知问题，但不确定是不是策略不会用信息**时，先做**oracle perception + learned control**；若大涨，再做**信息质量阶梯**与**反事实模态腐蚀**，区分“缺信息”和“用不好信息”。若涨幅很小，则做 **oracle control / geometry ceiling**。citeturn11search0turn11search6turn23search0

当**clean 环境好、真实环境差**时，不要只加白噪声；先测**结构化错误注入**与**残差匹配合成误差**，区分随机噪声脆弱、持久偏置脆弱与感知-控制接口失配。citeturn32search11turn32search8turn6search6turn6search1

当**更换 prompt、harness 或 orchestration 后结果波动很大**时，先做**GT replay / harness validation** 与 **Harness A/B differential testing**；若 reference solution 都不能稳定通过，先停下模型研究。citeturn22search1turn22search10turn9search4

当**模型似乎利用了捷径**时，优先做**mismatched-pair controls**、**blind baselines** 和 **negative controls**；如果 blind baseline 很强，任何新模型增益都不值得认真解读。citeturn27search0turn18search13turn8search11

当**多智能体系统比单智能体更贵但并不更好**时，先做**message pruning / topology intervention**；若轻剪枝不掉点，系统主要问题不是“缺协作”，而是“协作噪声过大”。citeturn26search0turn26search8turn7search15

当**不确定该把资源投给哪条研究路线**时，先做**廉价 kill test**：frozen representation probe、oracle ceiling、paired small-scale eval。如果这些快筛都不给力，再做 full training 通常只是昂贵地确认失败。citeturn28search1turn28search0turn30search2

## 可验证自主研究实验模板

下面给出一个适合写进论文方法部分或内部研究规范的“Verifiable Autonomous Research”模板。它的关键不在格式，而在**强制你把可验证性、反事实性、对照、配对统计和 harness 合同写清楚**。

**研究主张**：一句话写明你要验证的机制性命题，例如“系统失败主要由 STOP 决策，而非路径跟随能力导致”。

**竞争假设**：至少列出两个 mutually informative 的替代解释，例如“感知瓶颈”“停靠瓶颈”“评测器误判”“动作空间 ceiling”。

**最小干预**：明确只改一个变量，写出 intervention operator，例如“将 STOP head 替换为 oracle stop，其余模块与参数冻结”。

**正对照与负对照**：正对照证明实验足够有力，负对照证明实验不会被 shortcut 或 leakage 驱动。负对照可采用 mismatched-pair、blind baseline、negative control exposure/outcome。citeturn8search11turn18search13

**上界与下界**：同时报告当前系统、诊断上界、以及必要时的 trivial baseline / blind baseline。没有 ceiling 的增益通常不知该如何解释。citeturn7search4turn24search2

**闭环而非仅离线**：若任务是序列决策，必须报告 closed-loop 指标，并给出 teacher-forced/closed-loop gap。citeturn1search0turn1search11

**配对评估**：同实例、同 seeds、共享随机数；报告 per-episode delta、bootstrap CI 和显著性检验，而不是只报均值。citeturn30search2turn30search3

**评测合同**：写清 evaluator 版本、replay/freeze policy、evidence-admission contract、超时策略、日志字段与 artifact 保存方式。citeturn22search1turn22search10

**失败定位**：至少保存首个不可逆错误的截图、观测、动作、消息、内部状态摘要与 evaluator 证据。多智能体任务要额外保存 agent-level attribution。citeturn19search5turn19search1

**停止规则**：预先写明何时认为某条研究路线被 falsify，例如“若 oracle stop 提升 < 1%，则不再优先研究 stop module”。这与最优实验设计和可证伪研究原则一致。citeturn21search10turn21search11

一个适合 methodology section 的一句话版本可以是：**“We evaluate each hypothesized bottleneck with a single-variable paired intervention, include oracle ceilings and negative controls, verify the evaluation harness via reference replay, and report closed-loop paired confidence intervals on per-episode deltas.”** 这一模板几乎可以原样迁移到 VLN、VLA、tool-using agents 和 AgentSwarm。citeturn22search1turn30search2turn8search11

## 判断实验结果是否足以支持因果瓶颈主张的核查清单

一个结果若要支持“这是因果瓶颈”的说法，我建议至少满足以下条件。

第一，实验是否是**受控干预而非普通删改**。也就是：你改的是一个变量，而不是同时改了容量、训练预算、接口和损失。否则它更像相关性证据，而不是机制证据。citeturn8search8

第二，是否存在**竞争假设之间的可分离预测**。高信息增益实验的美感在于，不同假设会给出明显不同的结果模式。例如 oracle perception、oracle control、oracle stop 三者的差分组合，就能把几种瓶颈清晰分开。citeturn11search0turn11search6turn24search2

第三，是否同时报告了**上界、下界和负对照**。没有 oracle ceiling，你不知道改进空间是否值得做；没有 blind baseline 或 negative control，你不知道结果是否来自 shortcut。citeturn8search11turn18search13

第四，是否验证了**harness 没坏**。若 GT replay 不能稳定通过，或者不同 harness 结论差异大到超过模型差异，则因果主张应先暂停。citeturn22search1turn9search4

第五，是否使用了**闭环指标**。对 embodied 与 agentic 系统，只报离线 loss、teacher-forced accuracy 或单步 imitation accuracy，通常不足以支持“瓶颈在这里”的结论。citeturn1search0turn1search11

第六，是否区分了**随机误差**与**持久偏置**。如果你的鲁棒性实验只加 i.i.d. 噪声，却把结果外推到 sensor drift、coordinate bias 或 intermittent fault，上述外推通常站不住。citeturn32search11turn32search8

第七，是否采用了**配对统计设计**。在高方差 sequential tasks 中，不配对的平均数比较太容易把随机 seed 差异误判为机制差异。citeturn30search2turn30search0

第八，结果是否具有**跨任务可复用性**。若同一实验模式在导航、工具调用和多智能体三个场景都指向同一类瓶颈，证据强度会高很多；如果只在一个 benchmark、一个 harness、一个 prompt 模板下成立，主张就应更保守。citeturn22search10turn7search15turn9search16

第九，是否能定位到**首个不可逆错误**或**关键转移**。若你只能看到 terminal failure，而不能指出“何时、因为什么变量、进入了哪种坏状态”，那么“瓶颈”通常只是后见之明式的标签。citeturn19search5turn13search18

第十，结论是否明确写成**局部因果命题**而非全局真理。更科学的写法是：“在此 evaluator、此任务家族、此干预预算下，STOP decision appears to be the dominant recoverable bottleneck.” 而不是“我们的系统主要受 STOP 限制”。因果主张的边界条件必须一开始就写清楚。citeturn21search11turn8search8

## 仍缺乏满意诊断实验的开放缺口

尽管近两年 agent、VLM 和多智能体评测进展很快，但一些关键缺口仍然没有被满意解决。

第一个缺口是**真实部署误差协方差的残差匹配诊断**。我们已经有很多 corruption benchmark，但大多数仍是“单噪声、独立噪声、视觉噪声”，很少能同时匹配跨模态、跨时间、跨控制环的真实 residual structure。现有 sim2real 和 bias-induced residual work 已经说明“合成得不对，诊断就会错”，但还没有形成标准套件。citeturn6search1turn6search6turn16search10

第二个缺口是**长程具身任务的 first irreversible error benchmark**。ALFRED 暗示了不可逆性的重要性，Who&When 与 VerifyMAS 开始做多智能体 decisive step attribution，但具身导航/操作社区仍缺乏统一、低成本、可比较的“首个致命错误”标注协议。citeturn7search1turn19search5turn19search1

第三个缺口是**把 memory 写入质量、检索质量、压缩失真和冲突解析分开测的因果记忆实验**。MemoryAgentBench 与 MemoryArena 已经把 memory 作为独立能力来评估，但“写错了”“忘掉了”“压缩坏了”“被旧错误记忆污染了”这几类机制，仍缺少统一的干预式分辨实验。citeturn25search3turn25search15

第四个缺口是**将 abstention competence 融入具身与协作任务的标准协议**。MM-AQA 和 autonomous abstention benchmarks 说明该问题非常真，但具身导航、工具调用和 AgentSwarm 仍主要按“完成了没”打分，而不是“是否应该行动”。这会系统性低估高风险保守策略的价值。citeturn23search0turn23search1

第五个缺口是**模型失败与 harness 失败的规范化分离**。Harness-Bench 与 executable benchmarking suite 已经把 replay/freeze policy、evidence-admission contract、declared drivers 提上日程，但复杂工具链与多 agent orchestration 里的评测合同仍远未标准化。换言之，今天很多“agent benchmark”其实还没有把系统和评测器真正拆开。citeturn22search1turn22search10turn9search4

第六个缺口是**大规模 swarms 的 coalition-level causal diagnostics**。COMA、difference rewards 和单 agent 敲除适合小中规模协作，但当 team topology 动态变化、消息有层次、agent 角色可替换时，单 agent marginal contribution 已不足以解释 coalition failure。近期工作开始研究 message value、topology pruning 与 exact credit assignment，但还缺少 swarm 级、可视化、低成本的统一协议。citeturn10search2turn10search0turn26search8turn26search0

第七个缺口是**多模态交互而非单模态贡献的标准化诊断**。Winoground、SugarCrepe、Treble、MultiSHAP 都朝这个方向前进，但绝大多数实验仍停留在“遮住图像掉多少点/遮住文本掉多少点”。社区仍缺一套普遍接受的、可迁移到具身任务的“interaction-first”诊断标准。citeturn27search0turn18search1turn16search5turn17search7

第八个缺口是**VLN / embodied benchmark 的统一可诊断性设计**。VLNVerse 明确指出现有 VLN benchmarks 在物理 realism、sim-to-real insight 和 task fragmentation 上存在不足；这不仅是 benchmark 问题，也是诊断实验无法复用的问题。未来 benchmark 若不把 oracle ceilings、 reset hooks、 negative controls、 GT replay、 failure attribution 作为原生功能，诊断效率仍会很低。citeturn0search5turn0search1

综合来看，当前最缺的并不是新的大模型、也不是更复杂的训练 recipe，而是**跨模态、跨闭环、跨多智能体、跨 harness 的“标准诊断接口”**：统一的 oracle hooks、统一的 replay contract、统一的 paired-eval protocol、统一的 abstention-aware metrics，以及统一的 failure-state representation。近期的 agent benchmarking、memory benchmarking、abstention benchmarking 和 multi-agent attribution 工作已经给了非常好的起点，但距离成为像 train/val/test split 一样自然的研究基础设施，还有明显距离。citeturn22search10turn25search15turn23search1turn19search1turn7search15