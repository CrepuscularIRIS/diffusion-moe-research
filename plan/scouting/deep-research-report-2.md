# 面向 Information Fusion 与 ESWA 的小实验室前沿选题侦察

## 结论先行

在你给定的硬约束下，我最看好的首选方向是**水网中的信念修复：区分漏损、传感器失真与需求漂移，并把“要不要重观测”做成可校准决策**。它同时满足几个关键条件：公开数据已经在 2024–2025 年真正成形；2025–2026 的社区工作仍主要停留在检测与定位，还没有把问题正式改写为**冲突证据下的根因 belief maintenance + calibration + re-observation**；而且首个 go/no-go pilot 完全可以用 L-TOWN/Modena/DiTEC-WDN 的公开场景、轻量树模型或小型时序模型，在 4–6 小时内跑出是否值得继续的结论。citeturn5academia0turn5academia2turn33academia0turn33academia1turn33academia2

两个最强备选分别是**陈旧 HD 地图信念维护**，以及**智能楼宇分层计量账本修复**。前者有很强的未来相关性：2025–2026 刚出现面向 3D HD map updating 的城市级基准、长期维护方法与道路施工区多模态数据，但大多数工作仍停在“检测到变化/更新地图”，尚未把“不再信任旧地图”的阈值与重采样策略做成 calibrated belief。后者则非常 ESWA 友好：公开楼宇数据已经开始包含分层计量结构与 labeled issues，而近期研究又指出 HVAC/FDD 文献的可复现性与公开数据状况仍明显不足，这给“可部署的账本一致性 + 传感器信任修复”留下了很大的空位。citeturn15academia0turn15academia1turn17academia0turn22academia0turn22academia1turn6academia1

整体上，2025–2026 的外部信号很一致：数字孪生的**质量保证**和**同步**问题正在升温，ASQAP 2025 已经把 digital-twin-based quality assurance、verification、validation 单独拉成 workshop，而 2026 的综述仍把 twin synchronization 列为关键未解问题；这与“在 stale、partial、conflicting、asynchronous evidence 下维护可用信念”的实验室口味高度同向。另一个现实限制是：当前会话里实际可见的附件只有 Taste Operator Bank，因此下面的 operator 映射只把它当作**故障签名检索菜单**，不把它当作方向来源本身。citeturn23academia3turn21academia3 fileciteturn0file0

## 评分总表

下面的打分均采用 **1–5 分，5 分更优**。其中“基线安全”表示被简单强基线一把秒掉的风险较低；“工程安全”表示实现风险较低；“Kill 清晰”表示 4–6 小时 pilot 后能否快速止损。

| 排名 | 候选 | 味道 | 实用必要性 | 未来相关性 | IF 适配 | ESWA 适配 | 数据可得 | 6h 试点 | 基线安全 | 工程安全 | Kill 清晰 | 总分 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 水网漏损与传感器失真信念修复 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 5 | 48 |
| 2 | 陈旧 HD 地图信念维护与重观测 | 5 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 3 | 4 | 43 |
| 3 | 智能楼宇分层计量账本修复 | 4 | 5 | 4 | 4 | 5 | 4 | 5 | 3 | 4 | 5 | 43 |
| 4 | 配电网拓扑动作后果核验 | 4 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 3 | 4 | 42 |
| 5 | 电池多证据健康信念修复 | 4 | 4 | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 42 |
| 6 | 智能家居养老置信维护 | 4 | 5 | 5 | 4 | 5 | 3 | 4 | 4 | 4 | 4 | 42 |
| 7 | 工控执行后果核验 | 4 | 5 | 5 | 5 | 4 | 3 | 4 | 3 | 3 | 4 | 40 |
| 8 | 机器人后置条件核验 | 4 | 4 | 5 | 4 | 4 | 3 | 3 | 3 | 2 | 4 | 36 |

## 排名前八候选

### 水网漏损与传感器失真信念修复

**审稿人挑眉点**：把“漏损检测”从 anomaly detection 改写成**可校准的根因信念维护**——系统持续判断“是 leak、sensor fault 还是 demand shift”，并且输出“是否值得加测/复测某个点”的决策。**现实痛点**：水网维护真正消耗人力的是误派工、误报警和晚发现，而不是排行榜上的 clean F1。**社区证据**：2024 年起公开 benchmark 开始成形，研究者不再只拿 EPANET 配置文件而是直接提供可用数据；2025 年 DiTEC-WDN 又把多网络、多场景、大规模图状态推到公开基准层；2025–2026 的方法代表作则集中在 leak/blockage detection、explainable GNN 和 factor-graph localization，说明问题很活跃，但 formulation 仍偏“检测/定位”，还没有进化到 calibrated belief maintenance。citeturn5academia0turn5academia2turn33academia0turn33academia1turn33academia2

**未解之处**在于四件事还没被一起 formalize：第一，指标还是偏 detection/localization，而不是 Brier、ECE、risk-coverage 与 dispatch utility；第二，基准很少把**sensor bias/drift/dropout**与真实 leak 放在同一决策问题里；第三，在线方法处理 concept drift，但通常不输出“下一步该重观测谁”；第四，部署约束里真正重要的“少量传感器、需求漂移、误报成本高”还没有成为主指标。**为什么不挤**：水网是刚变热但尚未拥挤的窄领域，社区强基线并不统一。**为什么不会被 plain LoRA / 单模态轻易杀死**：这里既不是文本任务，也不是单一视觉任务；如果只看 pressure，需求漂移和 leak 很容易混淆，如果只看 topology 又缺乏瞬时证据，天然需要 pressure、flow、demand proxy、graph topology 与时间连续性的融合。**IF 适配**非常直接，因为这是标准的 heterogeneous evidence fusion + uncertainty maintenance；**ESWA 适配**也很强，因为最终输出天然是运维可执行的 belief、告警与重测建议，而不是抽象表征分数。citeturn33academia0turn33academia1turn33academia2turn21academia3

**公共数据与风险**：首选公开数据是 L-TOWN/Modena 等 WDN benchmark，以及 DiTEC-WDN；前者适合现实 leak 场景与已有基线对比，后者适合快速采样大量 nominal / shifted scenarios。**强基线**建议至少保留四类：压力阈值/CUSUM、Isolation Forest/One-Class SVM、LSTM-VAE + drift detector、GENConv/FGENConv 或已公开的 factor-graph localization。**首个 4–6 小时 pilot**：选 L-TOWN 与 Modena 两个网络；从公开 no-leak 场景中采 300 个短期窗口做 nominal，取 100 个 leak 窗口，再在 nominal 上人为注入 100 个 sensor bias/drift/dropout 和 100 个 demand-step；预处理只做 rolling residual、1-hop graph aggregation、昼夜周期特征；模型先用 **XGBoost 多分类 + 温度缩放/Dirichlet calibration + 简单 HMM/贝叶斯滤波平滑**；指标用 macro-F1、Brier、ECE、误派工率、budgeted re-observation utility。**Green criteria**：相对最佳 detection baseline，在匹配 leak recall 时误报下降至少 15%，且 ECE 降低至少 0.05；**Kill criteria**：如果 pressure-only 基线与融合模型差距低于 3 个百分点，或者 calibration 改善不转化为更好的重观测 utility，就应停。**ESWA 最低可发 claim**：在公开 WDN 上，根因 belief + calibration 比 detection-only baseline 更能降低误派工。**Information Fusion 更强 claim**：图拓扑、时间滤波与 selective re-observation 共同带来稳定的 decision-utility 提升，并且提升主要出现于冲突证据与 concept drift slice。**红旗**：合成 leak 与真实工况之间仍有 realism gap；传感器布设方案不同会显著改变收益上限。citeturn5academia0turn5academia2turn33academia0turn33academia1turn33academia2

### 陈旧 HD 地图信念维护与重观测

**审稿人挑眉点**：不要再把地图维护只做成 change detection；更有味道的对象是**stale-map belief**——系统何时该停止信旧图，何时只需忽略动态物体，何时必须触发 re-survey。**现实痛点**：2025–2026 的论文和数据都在强调 HD map 会因城市演化、临时施工和半静态目标而迅速过时，而道路施工区甚至长期缺乏公开数据。**社区证据**：SceneEdited 在 2025 年把 3D HD map updating 明确拉成 city-scale benchmark；MTD-Map 2026 说明长期维护仍在快速推进；刚刚发布的道路施工区多模态数据集则进一步说明“临时变化”本身已经成为独立问题。citeturn15academia0turn15academia1turn17academia0

**未解之处**主要在于：现有工作更关心 change mask / update quality，而不是**map trust calibration、change persistence、以及有限巡检预算下的 revisiting policy**。**为什么不挤**：这是自动驾驶外溢出来的基础设施维护问题，不是传统 VLM 排行榜赛道。**为什么不会被 plain LoRA / 单模态杀死**：如果只看当前图像，容易把光照、遮挡和临时车辆当变化；如果只看旧 LiDAR 地图，又会把临时施工与长期结构更新混在一起；这个任务天然要求旧图、当前图像/点云、跨时 persistence 共同决定 belief。**IF 适配**源于跨时间、跨模态、跨置信源的 stale-belief 更新；**ESWA 适配**则体现在“预算内先复查哪些 tile/road segment”这一非常工程化的输出。citeturn15academia0turn15academia1turn17academia0

**公共数据与风险**：SceneEdited 公开 GitHub/toolkit，适合作为首发数据；施工区数据可作为补充 slice。风险在于点云/影像预处理稍重，但远没有到 TB 级强制下载。**强基线**可用三类：geometry-only occupancy differencing、image-only pair classifier、early/late fusion 的 LightGBM 或小 MLP；若资源允许，再对比 MTD-like transition statistics。**首个 4–6 小时 pilot**：在 SceneEdited 中抽 200 对 outdated/current scene pair，只切 64m×64m tile；预处理用稀疏体素占据差分、DINOv2 before/after frame feature、简单 temporal persistence 统计；模型用 **LightGBM 二阶段头**，先做 stale-vs-not，再做 re-survey priority；指标用 AUROC、ECE、budgeted recall@top-k revisit、误巡检成本。**Green criteria**：在相同巡检预算下，top-k revisit recall 比 geometry-only 提升至少 10%，同时 ECE 低于 0.10；**Kill criteria**：若 image-only 或 geometry-only 几乎持平，说明融合意义不足。**ESWA 最低可发 claim**：轻量 stale-map belief 模型能把巡检预算更有效地分配到真正过时的路段。**Information Fusion 更强 claim**：融合跨模态与跨时 persistence 后，可在动态背景与临时施工 slice 上显著改善 risk-aware revisit policy。**红旗**：SceneEdited 中部分变化是合成的；配准误差可能伪造“变化”。citeturn15academia0turn15academia1turn17academia0

### 智能楼宇分层计量账本修复

**审稿人挑眉点**：把 building anomaly 从“某个 meter 看起来异常”改写成**分层计量账本的信任修复**——到底是负载真的变了，还是电表、点位映射、时钟同步或子表缺失坏了。**现实痛点**：商业楼宇的 HVAC/能源管理既关乎碳排，也关乎运维成本；公开基准刚开始改善，但 building ML/FDD 文献的可复现性与数据可得性仍很差。**社区证据**：2025 年公开的 smart company building 数据集给出了 6 年、72 个电表、9 个热表、天气站、分层计量结构与 labeled issues；Smart Buildings Control Suite 又把 11 栋楼的真实 telemetry、轻量模拟器和 PINN 基准一起开放；而 2025 的复现性研究指出，楼宇 ML/FDD 论文里大部分甚至没有说清数据是否公开。citeturn22academia0turn22academia1turn6academia1

**未解之处**不是“再做一个能耗预测器”，而是把**meter hierarchy、守恒关系、天气、冷热源与 issue taxonomy**联合起来，输出可操作的 trust state。**为什么不挤**：公开数据刚刚出现，绝大多数工作仍是控制或 forecasting，不是 belief repair。**为什么不会被 plain LoRA / 单模态杀死**：如果只做单表 forecasting，根本分不清“真实负荷变动”和“子表坏了/时间错位”；只有把 parent-child ledger、天气、冷热源状态与时序一致性一起看，问题才可判。**IF 适配**来自守恒账本、环境协变量与 issue evidence 的多源融合；**ESWA 适配**几乎是原生的，因为楼宇运维更关心“哪个点不可信、要不要派人查”。citeturn22academia0turn22academia1turn35academia0turn35academia3

**公共数据与风险**：smart company building 数据风险低；Smart Buildings Control Suite 可做跨楼泛化补充。**强基线**建议包括：meter-balance 阈值法、Isolation Forest、LEAD/GAN-LSTM 异常检测器、天气感知 XGBoost 预测器。**首个 4–6 小时 pilot**：从 smart company building 里取一个三层计量子树，约 20 个电表，加天气和冷热源；训练集 8 周、验证 2 周、测试 2 周；在测试上人工注入 bias、dropout、timestamp shift，同时保留真实 load shift；模型只用 **ledger residual features + weather + rolling seasonality + LightGBM 多类头 + 简单后验平滑**；指标用 macro-F1、Brier、time-to-isolation、parent-child residual closure。**Green criteria**：issue typing macro-F1 超过 0.70，且误报率相对最佳异常检测基线下降至少 20%；**Kill criteria**：如果简单守恒阈值已经接近全部收益，则无须继续复杂化。**ESWA 最低可发 claim**：分层账本一致性比黑箱 anomaly score 更能支撑实际楼宇排障。**Information Fusion 更强 claim**：把计量层级、环境信息和 issue priors 显式融合后，calibration 与 triage utility 同时改善。**红旗**：真实 labeled issue 的长尾分布可能过稀；不同建筑的 meter 命名/拓扑清洗成本不可低估。citeturn22academia0turn22academia1turn6academia1turn35academia0turn35academia3

### 配电网拓扑动作后果核验

**审稿人挑眉点**：把 topology change 从“离线标签”变成**持续追认的 belief**——开关真的变位了吗，还是 PMU/通信链路或 bad data 在撒谎。**现实痛点**：真实配电网里 topology changes、load transfers、数据丢失与非高斯噪声是同一个现场问题，而不是四个分开的 benchmark。**社区证据**：SoCal 28-Bus 2025 提供了真实配电网 PMU/WMU、拓扑变化、负荷转移与测量误差信息；同期 state-estimation 工作明确指出 topology changes 和 real-time data loss 仍然是关键难点。citeturn29academia1turn32academia0turn32academia1

**未解之处**在于：大多数工作优化的是 state-estimation error，而不是“对拓扑状态的 calibrated trust”与“命令是否生效”的 operational question。**为什么不挤**：真实公开 distribution-PMU 数据直到 2025 才明显改善，赛道远未像 CV/NLP 那样拥挤。**为什么不会被 plain LoRA / 单模态杀死**：单个 phasor 通道可以看见异常，但很难判断是拓扑变化、数据坏点还是局部设备扰动；需要 graph structure、多点相量、时间窗口和 action metadata 共同决策。**IF 适配**极强，因为这是典型的 graph-structured multi-sensor belief update；**ESWA 适配**也不错，因为调度员更需要可信状态与再确认建议。citeturn29academia1turn32academia0turn32academia1

**公共数据与风险**：SoCal 28-Bus 风险低；额外大规模事件合成可用 pmuBAGE 一类公开资源，但首发不必依赖。**强基线**：DC residual threshold、CUSUM、窗口级 XGBoost、topology-aware GNN state estimator。**首个 4–6 小时 pilot**：取 SoCal 数据中全部拓扑变化/负荷转移窗口，先下采样到 1 Hz phasor；构造 60 秒 pre/post window，特征为相角/幅值变化、graph Laplacian residual、相邻节点一致性；模型用 **XGBoost + HMM smoothing** 预测 {action confirmed, suspicious sensor, ambiguous}; 指标用 macro-F1、ECE、平均确认延迟。**Green criteria**：较 residual threshold 在相同召回下减少至少 20% 误确认，且 ECE 明显降低；**Kill criteria**：若简单 residual threshold 已稳稳压过融合模型，则说明方向不值当前资源投入。**ESWA 最低可发 claim**：轻量图特征 + 校准头比传统 residual threshold 更适合 real-time action verification。**Information Fusion 更强 claim**：跨节点时空证据融合在 topology-change 与 data-loss 共存时仍能保持良好 calibration。**红旗**：真实事件数量可能有限；波形通道虽然有价值，但首轮 pilot 不应贪多。citeturn29academia1turn32academia0turn32academia1

### 电池多证据健康信念修复

**审稿人挑眉点**：不要再做纯 BLP/SOH leaderboard；更值得做的是**端口信号、磁信号与快速脉冲测试发生分歧时，系统如何维护“健康 belief”并决定要不要复测**。**现实痛点**：二次利用和大规模储能场景里，错把有风险电池当健康、或把可用电池过早淘汰，代价都很高。**社区证据**：PulseBat 2025 给出 464 个退役电池的 field-accessible pulse diagnostics；2025 的 smart sensing 工作表明新型机械/热/气/光/电多传感能明显突破传统端口测量上限；2026 的 MagBridge-Battery 则第一次用公开桥接方式把磁测量与 SOH label、sensor-anomaly samples 和 regime-B extrapolation 放到一个公开 benchmark 里。同期的 Pace 2025 仍主要把问题做成 physics-aware health estimation，而不是 calibrated belief maintenance。citeturn14academia1turn13academia0turn14academia0turn14academia2

**未解之处**在于：当前多证据工作多追求 regression accuracy，较少讨论 sensor anomaly、OOD regime、abstention、risk-coverage 以及“何时需要第二种测量确认”。**为什么不挤**：公开磁-电化学桥接 benchmark 是 2026 才出现的，处于刚开赛道。**为什么不会被 plain LoRA / 单模态杀死**：如果 terminal-only 足够，MagBridge 不会专门构造 anomaly samples 与 regime-B OOD；而如果磁信号只带冗余，那它在 anomaly/OOD slice 上不该出现边际收益。这正好给方向设置了可杀死的实验。**IF 适配**体现在多传感、异步检测与 uncertainty-aware fusion；**ESWA 适配**则体现在可部署的 recertification / retest 策略。citeturn13academia0turn14academia0turn14academia1turn14academia2

**公共数据与风险**：MagBridge 与 PulseBat 风险低；不过磁桥数据带有 synthetic bridge 成分，必须把 realism 风险写进论文。**强基线**：terminal-only XGBoost/TCN、magnetic-only CNN/MLP、简单 late fusion MLP、physics-aware Pace-style feature baseline。**首个 4–6 小时 pilot**：用 MagBridge 主 split 中 2,000 个 grounded sample 训练，400/400 验证测试，再加入全部 600 anomaly sample 与 560 regime-B 作为 OOD/异常评测；磁信号支路用小 CNN，pulse/temperature 支路用 MLP 或 XGBoost，总头输出 SOH + anomaly flag + confidence；指标用 SOH 的 R²/MAE、anomaly AUROC、ECE、risk-coverage。**Green criteria**：相较 terminal-only，OOD anomaly AUROC 提升至少 0.05，且 ECE 相对下降至少 20%；**Kill criteria**：若 magnetic branch 仅带来极小 clean gain，且在 anomaly/OOD slice 没有帮助，就应停止。**ESWA 最低可发 claim**：多证据信念头比单一 SOH 回归更适合实际复测/分流。**Information Fusion 更强 claim**：冲突证据切片下，多模态 belief fusion 可显著提升 OOD reliability 与 abstention quality。**红旗**：bridge 数据的域差可能导致外推乐观；磁图像预处理要防止 leakage。citeturn14academia0turn14academia1turn14academia2turn13academia0

### 智能家居养老置信维护

**审稿人挑眉点**：把“异常检测”改成**老人状态 belief maintenance**——屋里很安静，到底是正常日常差异、设备状态异常，还是传感器失联，系统该不该主动重观测。**现实痛点**：智能家居助手最关键的能力之一正是发现“环境已不对劲”，而最新公开 benchmark 显示现有大模型在这件事上并不可靠。**社区证据**：SmartBench 2026 是面向 anomalous device states 与 transition contexts 的首个 smart-home LLM benchmark，主流模型在 context-dependent 异常上准确率并不高；DomusFM 2026 则说明面向 smart-home binary sensor events 的轻量 foundation model 仍是新方向，并且它在七个公开数据集的 leave-one-dataset-out 上表现更好；SmartHome-Bench 2025 还把 senior care 纳入了智能家居异常视频分类。citeturn36academia1turn36academia3turn36academia0

**未解之处**在于：当前 benchmark 要么偏视频异常，要么偏 LLM reasoning，而“结构化设备状态 + 稀疏二值传感事件 + re-observe policy”的 formulation 仍很松散。**为什么不挤**：这是一个真实但不主流的应用面，公开数据碎片化，尚未形成稳定 SOTA 堆栈。**为什么不会被 plain LoRA / 单模态杀死**：如果只看单设备状态，很难区分 routine change 和 sensor failure；如果只看语言解释，又会掉进 text-dominant 陷阱。更合理的是限定输入为结构化设备状态转移与二值事件流。**IF 适配**体现在设备、房间、时间上下文和不完全观测的持续融合；**ESWA 适配**则非常强，因为结论天然对应“提醒/复核/派人联系”的应用决策。citeturn36academia1turn36academia3turn11academia3

**公共数据与风险**：SmartBench 公开、可直接下手；DomusFM 所覆盖的公共数据适合后续外部验证。风险在于不同家庭/数据集的 ontology 不统一。**强基线**：规则引擎、HMM、GRU/TCN、DomusFM frozen encoder + linear head。**首个 4–6 小时 pilot**：先只用 SmartBench 的 context-dependent anomaly split，剥离自然语言解释，只保留结构化设备状态与转移上下文；模型用 **GRU + calibrated multiclass head**，输出 {likely-routine, likely-device-anomaly, likely-sensor-failure, reobserve}; 指标用 macro-F1、ECE、useful re-observation rate。**Green criteria**：比规则引擎或 context-free classifier 提高至少 8 个百分点 macro-F1，且 ECE 下降明显；**Kill criteria**：如果不看上下文也能解决，说明问题并不真的需要融合。**ESWA 最低可发 claim**：结构化上下文 belief 比单次 anomaly classifier 更适合家庭告警。**Information Fusion 更强 claim**：跨设备事件与时间上下文融合显著提升 calibration 与 safe abstention，尤其在 context-dependent anomalies。**红旗**：benchmark 仍偏实验室设定，真实居家长期 drift 更复杂。citeturn36academia1turn36academia3turn36academia0

### 工控执行后果核验

**审稿人挑眉点**：不是泛泛地做 ICS anomaly detection，而是问**泵/阀命令是否真的改变了过程状态**；如果没改变，是攻击、传感器欺骗，还是工况切换。**现实痛点**：2025–2026 的公开工作已经反复说明，工业 CPS 里的异常诊断若不显式利用 digital twin/causal reasoning，就很难降低误报并做根因解释。**社区证据**：Causal Digital Twins 2025、i-SDT 2026、System-aware Contextual DT 2026 都围绕 SWaT/WADI/HAI 做实时诊断、攻击区分与 resilient control，但重点仍偏 anomaly diagnosis，而不是更细粒度的 action-outcome verification。citeturn19academia0turn19academia1turn25academia1turn25academia2

**未解之处**在于：许多系统能说“异常了”，但说不清“命令没生效”的后果证据来自哪里，也不把“是否需要人工复核某个 actuator/sensor”做成第一类输出。**为什么不挤**：检测赛道已经热，但 action-effect verification 这个 formulation 仍空。**为什么不会被 plain LoRA / 单模态杀死**：单个 sensor residual 很难判定 actuator failure 与 state transition delay；必须结合控制命令、过程变量耦合与物理约束。**IF 适配**非常自然；**ESWA 适配**也不错，因为输出可直接进入 operator playbook。citeturn19academia0turn19academia1turn25academia1turn25academia2

**公共数据与风险**：近年工作持续使用 SWaT/WADI/HAI，说明数据路径可用，但镜像与预处理脚本的工作量比水网/楼宇更不确定，因此 access risk 记为中等。**强基线**：CUSUM residual、TCN autoencoder、简单 one-class detector、规则型 twin heuristics。**首个 4–6 小时 pilot**：先只拿 SWaT 的 actuator forcing / spoofing 这类典型场景，做 command-conditioned residual verifier；模型用轻量 TCN，根据命令和局部 tag 窗口判断 {effect-confirmed, effect-missing, ambiguous}；指标用 F1、告警延迟、ECE。**Green criteria**：在相同 recall 下显著减少 false positives，并更快确认“命令未生效”；**Kill criteria**：如果简单规则足以解决多数样例，那就不值得投入更复杂的 twin 层。**ESWA 最低可发 claim**：面向 actuator outcome 的 verifier 比通用 anomaly detector 更适合工艺操作支持。**Information Fusion 更强 claim**：引入 process graph / digital twin context 后，可稳定提升 ambiguous slice 的 calibration。**红旗**：公开攻击集不一定覆盖真实 process-change 多样性；容易被 reviewer 质疑“又做一遍 SWaT”。citeturn19academia0turn19academia1turn25academia1turn25academia2

### 机器人后置条件核验

**审稿人挑眉点**：与其继续卷 manipulation benchmark 清分，不如把任务改成**机器人动作后的后置条件是否满足**——“抽屉真开了吗”“物体真放到位了吗”“夹取只是看起来快成功吗”。**现实痛点**：2026 年的 manipulation benchmark audit 已经明确指出，LIBERO 与 CALVIN 等常用基准存在 shortcut solvability、数据依赖和统计意义不足等问题；与此同时，社区在 2025–2026 明显开始重视 pre-execution verification、safety contracts 和 execution monitoring，但 post-execution state verification 仍没有被单独做透。RoboTwin 2.0 等新基准又刚把鲁棒双臂、强 domain randomization 和公开生成器推出来。citeturn10academia1turn10academia0turn7academia2turn38academia0turn38academia2

**未解之处**在于：现在很多文章验证“任务成功率”，但不验证模型是否真正维护了可靠的 postcondition belief。**为什么不挤**：大家还在卷 policy score，而不是卷 state verification。**为什么不会被 plain LoRA / 单模态杀死**：真正的后置条件核验至少要看 pre/post observation、动作 token 与环境扰动；如果 post-image-only 就够了，那这个方向应立即被 kill，这反而给了它非常清楚的止损边界。**IF 适配**是中等偏强，因为这里是 pre-state、post-state、action、task context 的融合；**ESWA 适配**则取决于你把它包装成 execution monitoring/quality assurance，而不是 robotic policy 本身。citeturn10academia1turn10academia0turn7academia2turn38academia0turn38academia2

**公共数据与风险**：RoboTwin 2.0 有公开 benchmark/代码，但 state export、任务切分与标签清洗都比前几项更麻烦，因此工程风险偏高。**强基线**：action-only prior、post-frame-only classifier、frame-diff logistic、frozen DINOv2 before/after + linear head。**首个 4–6 小时 pilot**：从 RoboTwin 2.0 里挑三个单步后置条件清晰的任务，抽 5k 对 pre/post 样本；模型先用 **frozen visual features + action token MLP** 做二分类 success/failure/postcondition-satisfied；指标用 balanced accuracy、ECE、跨 clutter/language 随机化 slice 的稳健性。**Green criteria**：相对 post-image-only 基线提升至少 8–10 个点，且在 clutter shift 下 calibration 更稳；**Kill criteria**：如果 post-image-only 或静态视觉 probe 已接近天花板，说明该 formulation 没有真正利用多证据。**ESWA 最低可发 claim**：后置条件 verifier 可作为轻量 execution monitor 降低虚假成功。**Information Fusion 更强 claim**：显式融合 pre/post/action/context 后，能在扰动更强的 slice 上保持可靠 belief。**红旗**：很容易被 reviewer 追问与 planner verification 的边界；若标签依赖 simulator state，需诚实说明 perception gap。citeturn10academia1turn10academia0turn7academia2turn38academia0turn38academia2

## 前沿首选与备选

**首选**：**水网漏损与传感器失真信念修复**。它是当前最像“低资源实验室该打的仗”的方向：公开数据成熟、强基线存在但未锁死、不是文本/感知单模态可碾压的问题、pilot 可以很快、Information Fusion 与 ESWA 双向都顺。citeturn5academia0turn5academia2turn33academia0turn33academia1turn33academia2

**备选一**：**陈旧 HD 地图信念维护与重观测**。它更前沿、更有未来感，但第一轮工程清洗和几何预处理比水网重一档；如果实验室希望押更强的未来相关性和跨机器人/自动驾驶/城市场景的复用性，它是很好的第二选择。citeturn15academia0turn15academia1turn17academia0

**备选二**：**智能楼宇分层计量账本修复**。它最稳、最 ESWA、最容易形成“工程可交付”的故事，而且不容易被批评为只是在公开 benchmark 上加一个小模块。代价是前沿感略逊于地图和水网，但胜在数据清晰、pilot 极快。citeturn22academia0turn22academia1turn6academia1

按附件里的 operator bank，我只给前三候选做最小检索式映射：**水网**对应 *factor-graph-ization* 与 *belief-ization*；失败签名是局部压力/流量证据冲突、当前时刻插值不能解释事件、且需要决定下一个该测谁。**地图**对应 *memory-kernel-closure* 与 *belief-ization*；失败签名是短时视角噪声和长期结构变化混在一起，仅凭当前帧很难判断陈旧性。**楼宇**对应 *flux-conservation-ization* 与 *residual-ization*；失败签名是 parent-child 账本不闭合，但问题可能只出在少数 meter 或少数时段。相应的**cheap probe**应分别是：水网对比“当前时刻 estimator”与“带历史滤波 estimator”的校准收益；地图对比“单次图像 pair”与“跨时 persistence feature”的 revisit utility；楼宇对比“单表异常分数”与“账本闭合 residual”的 issue isolation。若这些 cheap probe 没有出现 operator 预测的增益，就直接 kill。fileciteturn0file0

## 首选方向小型提案

**题目**：**面向公开水网基准的根因信念维护：在漏损、传感器失真与需求漂移之间进行可校准融合，并学习何时重观测**。citeturn5academia0turn5academia2turn33academia0turn33academia1turn33academia2

**核心假设**：若把问题从“漏损检测”改写成“多源证据下的根因 belief tracking”，那么即便不使用大型模型，只用图局部残差、时间平滑和后验校准，也能在真实决策指标上超过 detection-only baseline。更具体地说，pressure/flow/topology/时间连续性 这几类证据的融合，应该主要改善两类 slice：一类是 **demand shift 与 leak 混淆**，另一类是 **sensor bias/drift 与 leak 混淆**。如果改善只出现在 clean slice，而在冲突 slice 上没有提升，这个方向就不成立。citeturn33academia0turn33academia1turn33academia2

**数据设计**：主数据用公开的 L-TOWN 和 Modena 相关 benchmark，再辅以 DiTEC-WDN 的大规模 nominal / shifted scenarios。第一阶段完全不追求最真实的 leak simulator，而是先验证 formulation 是否成立：用公开 no-leak 数据建立 nominal 残差分布，在测试集注入 sensor bias、sensor dropout、demand step，保留公开 leak 场景作为真实异常。这样可以在数小时内回答最关键的问题：**fusion 到底有没有把“根因 belief”做对，而不是只把 anomaly score 做高**。citeturn5academia0turn5academia2turn33academia0turn33academia1

**方法路线**：第一层是极轻量的 feature bank，包括 rolling residual、昼夜周期偏差、1-hop graph aggregation、上下游压力差、局部守恒残差。第二层是快速多类分类器，首发就用 XGBoost 或 LightGBM，不急着上 GNN。第三层是 calibration，建议用温度缩放或 Dirichlet calibration。第四层是递归 belief smoothing，用 HMM 或简单贝叶斯滤波维护节点/区域级后验。最后加一个极简的 re-observation policy：当 posterior entropy 高且代价收益比合适时，建议复测某个节点或时间窗。这样的方法非常“工程优先”，不会把精力浪费在大模型调参上。citeturn33academia0turn33academia1turn33academia2

**第一天就能执行的 pilot**：抽两个网络、五类场景、几百个窗口，先只看三件事——macro-F1、ECE、误派工率。若相较压力阈值、Isolation Forest、LSTM-VAE/drift detector，融合后验能同时提升 F1 与 calibration，并在固定召回下减少误派工，则 go；若只能提升 clean accuracy 而不能降低误派工，或者 pressure-only 模型几乎同样好，则 kill。这个 kill 机制非常清楚，适合小实验室。citeturn33academia1turn33academia2turn35academia0

**最小可发表产出**偏 ESWA：公开 WDN 上，提出一个面向根因 belief 的轻量框架，证明它比纯 anomaly detector 更适合运维 triage。**更强的 IF 版本**则是：把 graph evidence、时间 belief update 与 selective re-observation 放进统一评价，展示该统一框架在冲突证据 slice 上带来稳定的 decision-utility 提升，并提供 calibration-aware ablation。这样写，既不会沦为“+1 点 SOTA”，也更符合 Information Fusion 的口味。citeturn33academia0turn33academia1turn33academia2turn23academia3

## 避开方向与独立复核查询

应该明确避开的方向有几类。**第一类**是继续在 LIBERO/CALVIN 之类成熟 manipulation benchmark 上卷分数；2026 的 benchmark audit 已经说明其中不少分数并不能稳定代表你真正想证明的能力。**第二类**是纯 battery life prediction 排行榜赛道；BatteryLife 2025 本身就是在整顿 benchmark 和 baseline 混乱，Pace 2025 也把高性能 physics-aware baseline 拉上来了，如果不把问题转成 calibration/OOD/decision utility，论文很容易沦为再做一次 health estimation。**第三类**是吃满 TUM2TWIN 这类超大 urban twin 管线的 full-stack 复现，它虽然研究价值高，但 767GB 级别的数据量与首轮 4–6 小时 pilot 目标不匹配。**第四类**是继续做“generic fusion block + established multimodal benchmark”，这正好踩中你给出的负历史。**第五类**是把 ICS 继续写成泛 anomaly detection，如果不转成 action-outcome verification 或 selective re-check，近两年的 DT-based strong baselines 已经太近。citeturn10academia1turn1academia1turn14academia2turn30academia1turn19academia0turn19academia1turn25academia1turn25academia2

下面给出 **20 条可独立复核的精确搜索查询**，你可以直接丢给搜索引擎或 Scholar 复查我今天的判断。

1. `2025 2026 water distribution network leak detection sensor fault uncertainty public dataset`
2. `DiTEC-WDN 2025 public benchmark water distribution network`
3. `Factor Graph Optimization for Leak Localization in Water Distribution Networks 2025`
4. `2026 explainable fuzzy GNN leak detection water distribution networks`
5. `2025 2026 HD map maintenance city-scale benchmark change detection SceneEdited`
6. `MTD-Map 2026 long-term LiDAR map maintenance`
7. `2026 roadwork zone detection geo-localization multimodal dataset`
8. `2025 real-world energy management dataset smart company building hierarchical metering labeled issues`
9. `Smart Buildings Control Suite 2024 open source benchmark 11 buildings`
10. `2025 reproducibility machine learning HVAC fault detection diagnosis buildings empirical study`
11. `2025 SoCal 28-Bus PMU WMU dataset topology changes load transfers`
12. `2025 topology-aware graph neural network state estimation PMU unobservable topology changes data loss`
13. `PulseBat 2025 second-life battery diagnostics realistic histories public dataset`
14. `MagBridge-Battery 2026 magnetic electrochemical public benchmark anomaly regime-B`
15. `2025 smart sensing battery state monitoring eleven measurement types`
16. `SmartBench 2026 anomalous device states behavioral contexts smart home public dataset`
17. `DomusFM 2026 foundation model smart-home sensor data seven public datasets`
18. `Causal Digital Twins for Cyber-Physical Security SWaT WADI HAI 2025`
19. `Cyber-Resilient Digital Twins discriminating attacks SWaT WADI 2026`
20. `What Are We Actually Benchmarking in Robot Manipulation 2026 LIBERO CALVIN RoboTwin 2.0`

