# **AI/ML 建模对象转移：从经验观察到基础数学载体的范式重构图谱**

在机器学习与人工智能的演进历程中，真正的突破性进展往往并非源于模型参数量的简单堆叠或工程架构的微调，而是源于核心“建模对象”的根本性转移。当旧有的计算范式在复杂性、泛化性或计算效率上遭遇不可逾越的瓶颈时，研究者通过重新审视“算法究竟在拟合什么”，将原本难以处理的物理现象、逻辑规则或概率分布，巧妙地映射到一个具备优良数学性质的新载体（Mathematical Carrier）上。这种转移不仅剥离了冗余的计算复杂性，更为系统赋予了前所未有的预测、测量与控制能力。  
本报告致力于构建一份深度的“建模品味图谱（Modeling Taste Atlas）”。本研究不满足于追踪性能指标（SOTA）的提升或新模块的堆砌，而是穿透工程表象，全面梳理并深度剖析那些真正改变了底层建模对象的经典与长尾案例。报告首先提供包含 40 个代表性案例的全局基准图谱，随后根据基础数学载体类型的内在逻辑将其分为五大演进群组，对 15 个具有跨领域启示意义的核心转移案例进行穷尽式拆解，最后提炼出推动这些范式转换的底层共性模式。

## **第一部分：AI/ML 建模对象转移全局基准图谱**

为了全面展现建模对象转移的广度与维度，下表系统性梳理了 40 个深刻改变 AI/ML 发展轨迹的范式转移案例。这些案例涵盖了从经典统计算法到现代基础模型的核心跳跃，每一个条目都代表着研究者视角的一次决定性重构。

| 转移核心领域 | 代表性工作或理论 | 旧对象 → 新对象 (Incumbent → New Modeling Object) | 底层数学载体 (Mathematical Carrier) |
| :---- | :---- | :---- | :---- |
| **概率与生成** | **Denoising Score Matching** | 包含难解配分函数的高维概率密度分布 ![][image1] → 对数概率密度的梯度空间 (Score) | Vector Field (向量场) |
| **概率与生成** | **Flow Matching** | SDE 驱动的随机马尔可夫去噪轨迹 → 连接先验与目标分布的确定性条件概率路径 | Transport Plan (传输计划) / Vector Field |
| **概率与生成** | **Diffusion Models** | 显式的直接数据空间映射关系 → 逐步加噪与去噪的随机微分动态过程 | Stochastic Process (随机过程) |
| **概率与生成** | **Generative Adversarial Nets** | 数据的显式对数似然概率函数 → 隐式生成分布与真实分布对抗的散度博弈 | Minimax Game / Divergence |
| **概率与生成** | **Energy-Based Models** | 严格归一化的概率分布测度 → 非归一化的玻尔兹曼能量曲面 | Energy Function (能量函数) |
| **概率与生成** | **Normalizing Flows** | 难以精确积分求导的隐变量后验 → 可逆微分同胚变换的雅可比行列式 | Diffeomorphism / Manifold (微分同胚/流形) |
| **概率推断** | **Stein Variational GD** | 马尔可夫链蒙特卡洛的单粒子随机游走状态 → RKHS 中最小化 KL 散度的确定性粒子流场 | Interacting Particles (相互作用粒子系) |
| **概率推断** | **Variational Inference** | 计算代价高昂的复杂贝叶斯后验积分运算 → 变分分布与真实分布之间的 KL 散度约束 | Latent Variable / ELBO (隐变量/证据下界) |
| **序列建模** | **Structured State Spaces** | 离散且存在记忆衰减的 token 序列交互或隐状态 → 连续时间的线性状态空间动力系统 | Dynamical System / Cauchy Kernel (动力系统) |
| **序列建模** | **Transformer as Kernel** | 序列特征的硬路由或启发式的绝对注意力分数 → 具有统计学意义的非参数化核密度估计器 | Kernel Smoother (核平滑器) |
| **序列建模** | **Word2Vec** | 极其稀疏且高维的离散符号化独热编码 (One-hot) → 基于局部共现概率约束的低维连续语义向量 | Vector Space (连续向量空间) |
| **科学计算** | **DeepONet** | 局限于固定有限维网格上的点到点函数映射 → 无限维连续函数空间到另一函数空间的算子 | Nonlinear Operator (非线性算子) |
| **科学计算** | **UltraModel** | 针对单一类型工业设备的具体物理机理方程 → 跨设备泛化的广义抽象变量特征映射函数 | Functional Mapping (泛函映射) |
| **科学计算** | **Physics-Informed NNs** | 纯数据驱动范式下的经验性回归误差最小化 → 支配系统演化的偏微分方程物理守恒残差 | PDE Residual (偏微分方程残差) |
| **强化学习** | **Direct Preference Opt.** | 独立训练的显式标量奖励模型 (Reward Model) → 策略模型本身隐式表达的对数概率比值 | Policy Log-Probability Ratio (对数概率比) |
| **强化学习** | **Physics-Based RL** | 基于网格邻接或全局状态空间的庞大马尔可夫转移概率 → 一阶物理定律驱动的逻辑谓词与碰撞因子 | Relational Graph / Logic (关系图/物理逻辑) |
| **强化学习** | **Object-centric World Models** | 将整体场景统一压缩的全局无结构潜向量 → 以“对象”为最小基本单位的离散因子化潜在集 | Factorized Latent Variable (因子化潜变量) |
| **强化学习** | **Soft Actor-Critic** | 单纯最大化期望累积奖励的单一目标 → 奖励最大化与策略动作分布信息熵最大化的双重目标 | Information Entropy (信息熵) |
| **表征学习** | **Concept Bottleneck Models** | 端到端深度网络中完全不可解释的高维黑盒隐藏特征 → 严格限制在人类可理解语义概念域内的流形 | Concept Manifold / Belief State (概念流形) |
| **表征学习** | **Clinical Foundation Models** | 混杂了记录习惯与设备噪声等多模态粗糙观测数据 → 底层解耦的生理学潜变量与特定环境无关不变量 | Invariant Latent Space (环境不变潜在空间) |
| **表征学习** | **Contrastive Learning** | 像素级别的生成式高保真重建误差目标 → 样本与其数据增强视图在隐空间的互信息下界 | Information Bottleneck (信息瓶颈) |
| **表征学习** | **Masked Autoencoders** | 对完整图像进行全局特征提取的监督学习 → 基于高度遮挡图像图块的自回归或局部自监督重建 | Patch Graph / Signal Masking (掩码图谱) |
| **动态网络** | **Modern Hopfield Networks** | 容量受限的离散二值神经元与简单的二次能量面 → 连续状态变量空间下的指数级对数和能量函数 | Continuous Energy Function (连续能量函数) |
| **动态网络** | **Spatio-Temporal FlowNet** | 基于统计特征相似度硬性计算的节点关联矩阵图 → 遵循物理源汇守恒定律的动态时空流传递量 | Flow / Transport Plan (动态流/传输计划) |
| **图表征** | **Graph Neural Networks** | 平铺或孤立分布的结构化表格节点固有属性 → 图拓扑结构约束下的节点间信息传递算子机制 | Message Passing Operator (消息传递算子) |
| **因果推断** | **Invariant Risk Minimization** | 试图在单一训练集上拟合所有可用特征的经验风险最小化 → 跨越多个干预环境保持不变的最优特征预测器 | Optimization Constraint (不变性约束) |
| **因果推断** | **Structural Causal Models** | 观测变量间基于联合分布规律的统计相关性网络 → 接受 do-calculus 干预的结构生成方程与反事实图 | Causal Graph (因果图 / 反事实流形) |
| **元学习** | **Neural Processes** | 映射特定输入到输出的单一确定性神经网络权重参数集 → 以给定的上下文观测集合为条件的连续函数分布 | Stochastic Process (随机过程) |
| **元学习** | **MAML** | 致力于在多个任务上找到平均表现最优的全局固定网络参数 → 寻找对新任务少量微调梯度最敏感的参数初始化空间 | Optimization Trajectory (优化轨迹几何) |
| **网络压缩** | **Knowledge Distillation** | 带有极端置信度的离散硬标签 (One-hot label) 交叉熵 → 教师网络输出蕴含类间关系的平滑软逻辑分布 | Soft Probability Distribution (软概率分布) |
| **视觉建模** | **NeRF** | 显示的三维体素网格、点云或多边形网格几何结构 → 连续欧氏空间中的隐式辐射场与沿射线方向的体积渲染积分 | Radiance Field / Ray Integral (辐射场/体积积分) |
| **泛化评估** | **Frechet Inception Distance** | 依赖人工主观评判或逐像素比对的生成图像均方误差 → 深度特征空间中真实数据与生成数据拟合高斯分布的距离 | Probability Metric / W2 (Wasserstein 距离) |
| **知识图谱** | **TransE** | 节点与边之间高维稀疏的三元组共现联合概率表 → 低维连续嵌入空间中的几何向量代数平移操作 | Vector Transport (几何向量平移) |
| **系统识别** | **Koopman Operator** | 在有限维度状态空间中高度非线性的复杂动力系统演化 → 在无限维度可观测函数空间上呈严格线性的全局演化算子 | Linear Operator (无穷维线性算子) |
| **拓扑数据** | **Topological Data Analysis** | 基于欧氏空间固定坐标度量框架下的点云刚性距离 → 随尺度变化的数据内在拓扑持久同调特征 (如 Betti numbers) | Algebraic Topology (代数拓扑) |
| **优化理论** | **Adam Optimizer** | 损失函数在当前参数点计算的单一全局一阶梯度向量 → 当前梯度的历史指数移动均值(一阶矩)与方差(二阶矩)的联合估计 | Exponential Moving Average (指数移动平均) |
| **混合物理** | **Residual Physics-ML** | 要求黑盒神经网络从头预测高度复杂非线性物理系统的全量最终状态 → 不精确的显式物理仿真器输出与真实实验结果之间的系统偏差残差 | Simulator Residual (仿真器残差流形) |
| **大模型解码** | **Speculative Decoding** | 大型自回归模型在长序列中高延迟的逐词独立概率分布采样计算 → 小型草稿模型的高速前瞻提议与大模型并行验证机制的接受率约束 | Markov Chain Rejection Rate (马尔可夫接受率) |
| **鲁棒控制** | **Control Barrier Functions** | 依赖启发式惩罚函数在庞大状态空间中定义的软性轨迹安全约束 → 严格保证系统动力学状态前向不变性的微分控制李雅普诺夫障碍边界 | Barrier Certificate (系统障碍证书) |
| **常微分网络** | **Neural ODEs** *(归属不确定)* | 由深度残差网络 (ResNet) 堆叠构成的离散固定层级前向传播映射 → 以连续时间作为深度的常微分方程初值问题的积分求解轨迹 | Ordinary Differential Equation (常微分方程) |

*(注：最后一条 Neural ODEs 的初始概念“将残差网络视作连续动力系统”在文献中存在较长演进周期，严格归属可能追溯至 Weinan E 等人的前期工作或 Chen 等人的成型定义，故标注其严格起源归属处于“不确定”的演进流变中。)*

## **第二部分：核心案例深度剖析与机制解构**

为深刻理解“建模对象转移”为何能突破复杂性屏障，本部分将所搜集的 15 个核心深度案例划分为五个具备内在数学联系的组别进行详尽阐释。每个组别将通过结构化表格精准定位核心要素，随后以连贯的叙述性分析揭示其深层运行机理与跨领域泛化价值。

### **组别 A：概率与生成域的几何流场演化**

本组案例展示了在概率密度估计与生成模型中，研究者如何放弃直接拟合高维概率密度函数或繁重的随机路径，转而利用几何流场与粒子传输体系来重构生成过程。

| 工作/方法名称 | 领域 | 代表论文信息 | 旧对象 → 新对象 | 数学载体 |
| :---- | :---- | :---- | :---- | :---- |
| **Denoising Score Matching (DSM)** | 概率生成 / 密度估计 | Vincent, *Neural Computation* (2011)1 | 包含难解配分函数的高维概率密度分布 ![][image1] → 对数概率密度的梯度空间 (Score) | Vector Field (向量场) |
| **Flow Matching (FM)** | 连续正则化流 / 生成模型 | Lipman et al., ICLR (2023)3 | SDE 驱动的随机马尔可夫去噪轨迹 → 连接先验与目标分布的确定性条件概率路径 | Transport Plan (传输计划) / Vector Field |
| **Stein Variational GD (SVGD)** | 贝叶斯推断 / 概率建模 | Liu & Wang, NeurIPS (2016)5 | 马尔可夫链蒙特卡洛的单粒子随机游走状态 → RKHS 中最小化 KL 散度的确定性粒子流场 | Interacting Particles (相互作用粒子系) |

#### **深度叙事分析**

在经典的能量模型与基于似然的概率生成模型中，研究者长期受困于一个根本性的数学障碍——配分函数（Partition Function, Z）。为了使得高维空间中的概率密度函数 ![][image1] 积分为 1，必须计算一个极其庞大且在计算上呈指数级复杂度的归一化常数。**Denoising Score Matching (DSM)** 的提出彻底颠覆了这一范式。Pascal Vincent 及其后续发展者不再试图直接拟合绝对的概率密度 ![][image1]，而是将建模对象转移为其对数密度的梯度（即 Score，![][image2]）2。这一极其精妙的数学载体转移瞬间移除了复杂性：由于对数求导操作的存在，常数项 ![][image3] 的导数为零，从而完全避开了配分函数的计算8。更重要的是，DSM 揭示了学习“如何对数据去噪”等价于学习“数据的梯度场”，这一思想在十年后直接奠定了 Diffusion 模型的底层数学框架，赋予了生成模型绕过 MCMC 采样直接生成极高分辨率图像的能力9。  
随着扩散模型的成熟，生成路径中强依赖于布朗运动与高斯噪声的复杂性开始成为推理速度的阻碍。**Flow Matching (FM)** 在此基础上进行了二次重构。它摒弃了扩散模型中非此即彼的随机微分方程 (SDE) 路径，将建模对象转移为连接任意先验分布到目标分布的“确定性条件概率路径向量场”3。借由最优传输（Optimal Transport）计划这一数学载体，Flow Matching 构建了一条在几何空间中最短且最直的传输路径4。这种确定性的流形映射不仅移除了随机路径带来的方差波动与模拟开销，还使得常规的常微分方程 (ODE) 求解器能在极少步数内完成高质量采样，彻底打开了非高斯先验与流形空间生成的大门，其思想目前正被迅速向视觉大语言模型 (MLLM) 领域迁移11。  
在贝叶斯推断领域，相似的“流场化”思想体现在 **Stein Variational Gradient Descent (SVGD)** 中。传统的 MCMC 推断依赖于单粒子的随机游走状态，不仅面临着严重的自相关性问题，且往往需要漫长的预热期。Liu 和 Wang 将推断任务视为一个确定性的动态传输过程，其建模对象转变为一组在再生核希尔伯特空间 (RKHS) 中交互的粒子群5。在新框架下，核函数的引入赋予了粒子间互斥的能力（Repulsive force）14。这一数学特性的转移完美移除了传统推断在复杂多峰（Multi-modal）分布中陷入局部坍塌（Mode collapse）的困境，使研究者能以极高的效率控制少量粒子精准勾勒出复杂的后验轮廓14。

### **组别 B：序列与时间依赖的连续代数抽象**

深度学习在处理时序与序列数据时，长期依赖于离散状态跳跃的模型。本组案例展现了研究者如何跨越离散到连续的鸿沟，将序列建模引入到无限维或连续动态系统的高度抽象层级。

| 工作/方法名称 | 领域 | 代表论文信息 | 旧对象 → 新对象 | 数学载体 |
| :---- | :---- | :---- | :---- | :---- |
| **Structured State Spaces (S4)** | 序列建模 / 长程依赖 | Gu et al., ICLR (2022)16 | 离散且存在记忆衰减的 token 序列交互或隐状态 → 连续时间的线性状态空间动力系统 | Dynamical System / Cauchy Kernel (常微分动力系统/柯西核) |
| **Transformer as Kernel** | 神经网络架构分析 | Tsai et al., EMNLP (2019)18 | 序列特征的硬路由或启发式的绝对注意力分数 → 具有统计学意义的非参数化核密度估计器 | Kernel Smoother (核平滑器) |
| **Neural Processes (NPs)** | 元学习 / 函数回归 | Garnelo et al., ICML (2018)20 | 映射特定输入到输出的单一确定性神经网络权重参数集 → 以给定的上下文观测集合为条件的连续函数分布 | Stochastic Process (随机过程/函数空间) |

#### **深度叙事分析**

当序列长度扩展至数万级别时，传统的 Transformer 受困于自注意力机制 ![][image4] 的复杂度，而 RNN 则无法摆脱长程梯度消失的宿命。**Structured State Spaces (S4)** 提出了一种极其优美的代数抽象，将离散的序列步长转移为连续时间下的动态微分状态空间模型16。S4 的核心突破在于其数学载体的重构：通过对系统演化矩阵 ![][image5] 施加特殊的低秩修正（Low-rank correction）与 HiPPO 正交多项式约束，它将复杂的连续时间离散化与卷积操作转化为求解病态条件极低的“柯西核（Cauchy Kernel）”问题17。这一转移瞬间移除了循环神经网络只能按顺序展开的并行瓶颈，使得极其漫长的依赖关系（如超长音频、数万字文本）能够以前所未有的并行卷积速度被处理，为如今大放异彩的 Mamba 等线性复杂度大语言模型奠定了底层的数学操作23。  
几乎在同时期，针对 Transformer 本身注意力机制的机理解释也发生了一次重大的对象转移。**Transformer as Kernel Smoother** 的研究者们发现，注意力机制在本质上并非基于特定规则的特征路由，其真正的数学等价物是一个经典的非参数化核密度估计器（Nadaraya-Watson Kernel Estimator）18。当注意力分数被重新建模为一个定义了输入样本距离的核函数（Kernel Smoother）时，大量原本基于直觉的经验性设计（如温度调节、特征缩放）变得在数学上完全透明19。更深刻的是，这一转换使得运用泰勒展开或随机特征映射（Random Features）以实现复杂度降维成为可能，让研究者可以基于核代数的严格法则开发新型自适应序列平滑模型，这一视角极大地影响了随后的 Efficient Transformer 设计风潮18。  
在元学习层面，**Neural Processes (NPs)** 实现了一次从“空间权重”到“函数分布”的极致飞跃。传统的深度回归模型致力于寻找一组在训练集上误差最小的固定参数。NPs 却借鉴了高斯过程的哲学，将其建模对象替换为一个以少量语境点（Context set）为条件的随机过程分布20。通过引入隐变量生成过程，NPs 兼备了神经网络极高的特征表达能力以及高斯过程在面临不确定性数据时的方差区间估计能力21。它移除了高斯过程在大规模数据下严苛的 ![][image6] 矩阵求逆开销，使得模型能够执行“分布的元学习”。这一泛函级别的模型转换已展现出强大的跨领域迁移能力，被成功应用于医疗时序补全和三维空间生成推理中21。

### **组别 C：人类对齐、环境表征与对象因果认知**

人工智能走向实用的关键在于它能否理解人类社会的复杂偏好，以及能否解构环境中的物理与逻辑实体。本组案例展现了在此层面的建模抽象转移。

| 工作/方法名称 | 领域 | 代表论文信息 | 旧对象 → 新对象 | 数学载体 |
| :---- | :---- | :---- | :---- | :---- |
| **Direct Preference Optimization (DPO)** | LLM 对齐 / 强化学习 | Rafailov et al., NeurIPS (2023)29 | 独立训练的显式标量奖励模型 (Reward Model) → 策略模型本身隐式表达的对数概率比值 | Policy Log-Probability Ratio (对数概率比 / Bradley-Terry 模型) |
| **Object-centric World Models (FOCUS)** | 世界模型 / 强化学习 | *Frontiers in Neurorobotics* (2025)31 | 将整体场景统一压缩的全局无结构潜向量 → 以“对象”为最小基本单位的离散因子化潜在集 | Factorized Latent Variable (因子化潜变量) |
| **Physics-Based RL (PBRL)** | 强化学习 / 机器人学 | Scholz et al., ICML32 | 基于网格邻接或全局状态空间的庞大马尔可夫转移概率 → 一阶物理定律驱动的逻辑谓词与碰撞因子 | Relational Graph / Logic (关系图 / 微分算子) |

#### **深度叙事分析**

随着大规模语言模型迈入指令微调时代，基于人类反馈的强化学习（RLHF）由于其极端复杂的训练管线（需维护独立的奖励模型、价值模型，并忍受 PPO 算法中超参数的极度脆弱性）而备受诟病。**Direct Preference Optimization (DPO)** 实施了一次外科手术般的数学转移。通过引入 Bradley-Terry 偏好模型，DPO 证明了奖励函数实际上可以解析地映射为最优策略与参考策略之间的对数概率比30。这就意味着，原本独立的标量奖励模型被完全吸纳进了生成策略的隐式概率分布中29。这种惊艳的置换彻底移除了在强化学习训练中必须执行的对抗性约束更新的复杂性，将极其不稳定的在线强化学习过程降维成了对预存对比数据集的单阶段监督分类任务29。DPO 因其强大的训练稳定性和显著降低的显存需求，迅速取代了 PPO 的统治地位，并正在加速向图像合成（Diffusion DPO）、视觉大模型等多个模态渗透33。  
在更为强调具身交互的强化学习与机器人学中，对状态表征的解构亦在发生转移。传统的强化学习习惯于利用庞大的神经网络将全局场景无差别地编码为一个高度纠缠的隐含状态。然而，**Object-centric World Models (如 FOCUS)** 将建模对象精细化为场景中各个独立实体的潜在表征分布31。通过强制建立因子化的潜在状态载体，模型学会了追踪“物体 A 移动不会无端导致物体 B 变形”这一物理先验。这种解耦消除了全局状态在遭遇动态遮挡或罕见环境时的过度反应灾难，赋予了智能体从零开始探索和操控未见物体的“内在认知动机”31。  
同样的哲学体现在 **Physics-Based RL (PBRL)** 中，其建模对象从宏观的马尔可夫转移矩阵缩小至一阶物理定律定义下的“实体碰撞预测”32。PBRL 不再试图记住每一种可能的状态转移，而是仅对局部关系的逻辑谓词集合进行回归32。数学载体的这一转变使得当环境从三个球变为十个球时，模型所依赖的局部碰撞物理规则并未发生改变，从而规避了状态空间随实体数量指数爆炸的“维数灾难”，大幅提升了样本的使用效率，为实现真正的神经符号混合人工智能（Neuro-symbolic AI）提供了一条可行路径32。

### **组别 D：物理世界的无穷维度算子映射与流传递**

当机器学习面临物理仿真与流体力学等遵循严密数理方程的领域时，直接的数据拟合显得苍白无力，其建模对象必须跨越到更高的泛函与泛化映射维度。

| 工作/方法名称 | 领域 | 代表论文信息 | 旧对象 → 新对象 | 数学载体 |
| :---- | :---- | :---- | :---- | :---- |
| **DeepONet** | AI for Science / 偏微分方程求解 | Lu et al., arXiv (2019)35 | 局限于固定有限维网格上的点到点函数映射 → 无限维连续函数空间到另一函数空间的非线性算子 | Nonlinear Operator (非线性算子 / 分支主干网络) |
| **Spatio-Temporal FlowNet** | 时空动态预测 / 图学习 | NeurIPS (2025)37 | 基于统计特征相似度硬性计算的节点关联矩阵图 → 遵循物理源汇守恒定律的动态时空流传递量 | Flow / Transport Plan (动态流 / 传输计划) |
| **UltraModel** | 工业建模 / 机制建模 | IJCAI (2025)38 | 针对单一类型工业设备的具体物理机理方程 → 跨设备泛化的广义抽象变量特征映射函数 | Functional Mapping (泛函映射) |

#### **深度叙事分析**

传统的物理仿真模型在求解偏微分方程（PDEs）时，算法极度依赖于在有限维空间中细分的固定网格。这种依赖导致了每当系统的初始状态或边界条件发生改变，求解器都不得不从头开始高昂的迭代运算。基于通用逼近定理在算子级别的扩展，**DeepONet** 完成了一次史诗级的对象转移36。该网络不再致力于拟合输入点到输出点的标量，而是引入了“Branch Net”（处理离散输入函数特征）与“Trunk Net”（处理连续查询域坐标）的双轨道架构，将其建模对象拔高为从一个无限维连续函数空间到另一个无限维函数空间的非线性映射算子（Nonlinear Operator）35。这一重组解除了神经网络被束缚在静态网格分布上的限制。在此框架下，一旦完成预训练，DeepONet 对未知物理边界条件的求解仅需极低复杂度的一次前向网络遍历，彻底改变了气象预测、流体力学以及随后的量子辅助计算等高维系统的演算范式39。  
面对包含密集交通网或地理气象的时空动态系统，大量现有的图神经网络（GNNs）和 Transformer 模型仅依赖数据间的统计学相关性，通过注意力机制拼凑节点间的关联矩阵。然而，**Spatio-Temporal FlowNet** 敏锐地指出统计学意义上的相似并不等同于演化机理。它将建模重点从静态的拓扑邻接矩阵转变为了具备方向性和流量大小的“物理守恒流（Flow Tokens）”37。在该载体中，节点之间的信息交互必须严格遵守“物质一旦从 A 流出，则必将汇入 B”的源汇守恒定律37。这看似施加了严苛的约束，实则完美移除了纯自注意力模型在捕捉时空关系时极易产生的、完全违反物理规律的“虚假超视距纠缠（Spurious long-range correlations）”，使其具备了对系统本质运行机制的深刻剖析与预测能力37。  
类似地，在工业物联网设备的数据利用中，旧有范式要求专家针对每一个工厂特定的阀门或锅炉建立定制的复杂机理模型。而 **UltraModel**38 致力于打破这一设备的物理隔阂，通过抽象的泛函映射将工业运行变量剥离具体设备外壳，转换为数字孪生中的普适特征变量表示。它消除的是高昂的定制化工程成本，并将通用表征学习成功降落于高度异构的工业控制流水线之上38。

### **组别 E：概念解耦、可解释约束与记忆分布流形**

在决策高风险领域与多模态数据面前，模型内部的不可视性成为了阻碍技术落地的关键。通过在隐空间引入强制流形与物理不变量，研究者重构了系统的认知过程。

| 工作/方法名称 | 领域 | 代表论文信息 | 旧对象 → 新对象 | 数学载体 |
| :---- | :---- | :---- | :---- | :---- |
| **Concept Bottleneck Models (CBMs)** | 可解释人工智能 / 表征约束 | Koh et al., ICML (2020)41 | 端到端深度网络中完全不可解释的高维黑盒隐藏特征 → 严格限制在人类可理解语义概念域内的流形 | Concept Manifold / Belief State (概念流形) |
| **Modern Hopfield Networks** | 动态网络 / 联想记忆 | Ramsauer et al., ICLR43 | 容量受限的离散二值神经元与简单的二次能量面 → 连续状态变量空间下的指数级对数和能量函数 | Continuous Energy Function (连续能量函数) |
| **Clinical Foundation Models** | 医疗大模型 / 分布外泛化 | arXiv (2025)45 | 混杂了记录习惯与设备噪声等多模态粗糙观测数据 → 底层解耦的生理学潜变量与特定环境无关不变量 | Invariant Latent Space (环境不变潜在空间) |

#### **深度叙事分析**

随着深度学习逐步入侵医疗等生命攸关的决策地带，让模型单纯“给出高准确率结果”已无法满足安全与合规的严苛要求。**Concept Bottleneck Models (CBMs)** 作为一种彻底的范式修正，直接介入了特征的表达层41。它禁止网络将输入直接映射为任务目标，而是强行插入一个人类可解释的“概念瓶颈层”。其建模对象变为一系列具备明确物理定义的概念集合（如病灶是否存在、体温是否正常）46。这一看似将表达能力降维的概念流形极大地重组了系统的复杂性，因为它不仅有效剔除了图像背景或无关伪影造成的虚假统计关联（Spurious correlations），还赋予了人类专家极为强大的“测试阶段实时干预（Test-time intervention）”特权46。专家可以直接修正瓶颈层中识别错误的概念，从而直接且透明地改变最终输出，这为后续多模态大规模语言模型在零样本生成（Zero-shot generation）下的逻辑修正铺平了道路47。  
对于更为具体的医疗时序数据分析，仅仅设置概念瓶颈可能不够。**Clinical Foundation Models** 面对的困境在于跨医院数据分布的剧烈偏移现象。不同诊疗单位所特有的设备采样率、报销驱动的诊断编码甚至医生打字习惯等，使得模型极易出现过拟合。研究者将其转移为在信息瓶颈下的联合分布优化：即模型在努力最大化疾病生理潜变量信息的同时，必须主动运用惩罚项以压制和抑制与具体“医院环境”高度相关的方向维度45。这一在潜变量空间中的不变性解耦动作，通过牺牲那些环境依赖但短暂有用的噪声，换取了系统在面对毫无交集的新医院时极高的稳健性（OOD robustness）45。  
最后，在关于网络架构的深度挖掘中，**Modern Hopfield Networks** 向我们展示了离散物理系统向连续微分空间转变时迸发的惊人能量。经典 Hopfield 联想记忆网络受制于二值神经元更新矩阵的线性依赖，只能存储极其有限的少量模式（约 ![][image7] 容量）。Ramsauer 等人对其进行了大刀阔斧的抽象，将状态方程的建模域扩张至连续变量，同时赋予其基于对数和指数（Log-Sum-Exp）极具陡峭特性的高维能量面44。这种从简单二次到连续非线性形式的惊人跨越，瞬间粉碎了原有记忆容量上限，使得网络能存储近乎指数级别的复杂图像。更震撼的是，其衍生出的梯度下降更新规则被证明在纯粹的数学代数形式上，与支撑目前全体大模型的 Transformer 架构的自注意力机制完全等价50。这不但消解了长久以来悬在深度学习上方对于 Attention 机制缺乏严格动力学物理依据的质疑，更为设计连续时间下的视觉和长文本生成大模型提供了最为锐利的数学理论基石51。

## **第三部分：总结——“建模对象转移”背后的底层抽象密码**

综上，在这数十个穿越时间与领域的 AI/ML 重大跳跃背后，那些看似截然不同的技术与繁复公式之中，实则潜伏着一组深刻而一致的“元模式（Meta-patterns）”。每一次建模对象的深刻转移，都是研究者在认知哲学层面对计算范式进行的剥茧抽丝：

1. **从“显式标量与固定映射”退行至“隐空间流形与演化算子” (From Points to Operators/Fields)**： 无论是 **DeepONet** 求解无穷维泛函映射36，**S4** 重构连续线性状态系统17，还是 **DSM** 与 **Flow Matching** 分别利用向量场捕捉分布对数梯度及传输路径2；它们不约而同地放弃了预测一个固定的具体结果。它们预测“变化的速度”、“演化的规律”甚至“偏好信息的流向”，这极大程度挣脱了离散计算带来的分辨率与拓扑束缚。  
2. **从“贪婪捕捉一切关联”升华至“物理、逻辑及因果的强制内化” (From Statistical Correlation to Mechanistic Invariance)**： 深度学习的黑箱长期被批评只是一个聪明的查表器。然而，正如 **FOCUS 世界模型**的因子化实体31、**Spatio-Temporal FlowNet** 对守恒定律的尊重37、以及 **Concept Bottleneck Models** 对可解释概念的极度坚持41。这表明前沿理论正试图切断模型依赖快捷方式（Shortcut learning）或虚假相关性的能力，强制将人类世界稳固的一阶物理法则与逻辑实体内化为其推断基座。  
3. **从“离散堆叠架构”还原为“基础非参数与积分方程框架” (From Neural Heuristics to Principled Math/Kernel Space)**： 在 AI 的高歌猛进中，无数直觉性的加层、正则化技巧充斥着顶会。但 **Transformer as Kernel** 揭示了复杂自注意力实际上只是一种经典的非参数核密度平滑器19；**Modern Hopfield** 则将深度网络解释为复杂能量盆地的吸引子下降过程44；**DPO** 则将复杂的 RLHF 反推回逻辑概率差值30。这证明，伟大的对象转移最终都会在最底层的数学分析、微分几何与泛函方程中找到其至简的、最普适的美学归宿。

每一次针对 AI/ML 建模对象的成功重置，本质上都是一次认知层面的革命——不仅在于决定计算机能够更有效地算什么，更在于定义人工智能该如何深刻地审视与解构这错综复杂的浩瀚宇宙。

#### **引用的著作**

1. Generative Models\* \- Purdue Engineering, [https://engineering.purdue.edu/DeepLearn/pdf-bouman/DL-week-15.pdf](https://engineering.purdue.edu/DeepLearn/pdf-bouman/DL-week-15.pdf)  
2. A Connection Between Score Matching and Denoising Autoencoders, [http://www.iro.umontreal.ca/\~vincentp/Publications/smdae\_techreport.pdf](http://www.iro.umontreal.ca/~vincentp/Publications/smdae_techreport.pdf)  
3. Flow Matching for Generative Modeling \- OpenReview, [https://openreview.net/forum?id=PqvMRDCJT9t](https://openreview.net/forum?id=PqvMRDCJT9t)  
4. Flow Matching for Generative Modeling \- Weizmann Institute of Science, [https://weizmann.elsevierpure.com/en/publications/flow-matching-for-generative-modeling/](https://weizmann.elsevierpure.com/en/publications/flow-matching-for-generative-modeling/)  
5. Stein Variational Gradient Descent with Matrix-Valued Kernels \- PMC, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6923147/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6923147/)  
6. code for the paper "Stein Variational Gradient Descent (SVGD) \- GitHub, [https://github.com/dilinwang820/Stein-Variational-Gradient-Descent](https://github.com/dilinwang820/Stein-Variational-Gradient-Descent)  
7. Stein Variational Gradient Descent: A General Purpose Bayesian Inference Algorithm \- arXiv, [https://arxiv.org/abs/1608.04471](https://arxiv.org/abs/1608.04471)  
8. Score Matching and Denoising Autoencoders: A Connection \- Hunter Heidenreich, [https://hunterheidenreich.com/notes/machine-learning/generative-models/score-matching-denoising-autoencoders/](https://hunterheidenreich.com/notes/machine-learning/generative-models/score-matching-denoising-autoencoders/)  
9. Denoising Score Matching \- Johannes Schusterbauer, [https://johfischer.com/2022/09/18/denoising-score-matching/](https://johfischer.com/2022/09/18/denoising-score-matching/)  
10. DENOISING LIKELIHOOD SCORE MATCHING FOR CONDITIONAL SCORE-BASED DATA GENERATION \- OpenReview, [https://openreview.net/pdf/ccc930d6cefd7ea8811e858a55d6318d0ea95abb.pdf](https://openreview.net/pdf/ccc930d6cefd7ea8811e858a55d6318d0ea95abb.pdf)  
11. On the continuity of flows \- arXiv, [https://arxiv.org/html/2512.12821v1](https://arxiv.org/html/2512.12821v1)  
12. 1 Introduction \- arXiv, [https://arxiv.org/html/2510.17991v1](https://arxiv.org/html/2510.17991v1)  
13. Elucidating the Design Choice of Probability Paths in Flow Matching for Forecasting \- arXiv, [https://arxiv.org/html/2410.03229v3](https://arxiv.org/html/2410.03229v3)  
14. Grassmann Stein Variational Gradient Descent \- Proceedings of Machine Learning Research, [https://proceedings.mlr.press/v151/liu22a/liu22a.pdf](https://proceedings.mlr.press/v151/liu22a/liu22a.pdf)  
15. Stein Variational Gradient Descent \- IMPA, [https://w3.impa.br/\~pauloo/teaching/seminar/slides/svgd.pdf](https://w3.impa.br/~pauloo/teaching/seminar/slides/svgd.pdf)  
16. \[PDF\] Efficiently Modeling Long Sequences with Structured State Spaces | Semantic Scholar, [https://www.semanticscholar.org/paper/Efficiently-Modeling-Long-Sequences-with-Structured-Gu-Goel/ac2618b2ce5cdcf86f9371bcca98bc5e37e46f51](https://www.semanticscholar.org/paper/Efficiently-Modeling-Long-Sequences-with-Structured-Gu-Goel/ac2618b2ce5cdcf86f9371bcca98bc5e37e46f51)  
17. EFFICIENTLY MODELING LONG SEQUENCES WITH STRUCTURED STATE SPACES \- OpenReview, [https://openreview.net/pdf?id=uYLFoz1vlAC](https://openreview.net/pdf?id=uYLFoz1vlAC)  
18. Rethinking Random Transformers as Adaptive Sequence Smoothers for Sleep Staging, [https://arxiv.org/html/2605.09905v1](https://arxiv.org/html/2605.09905v1)  
19. arXiv:1908.11775v4 \[cs.LG\] 11 Nov 2019, [https://arxiv.org/pdf/1908.11775](https://arxiv.org/pdf/1908.11775)  
20. \[1901.05761\] Attentive Neural Processes \- arXiv, [https://arxiv.org/abs/1901.05761](https://arxiv.org/abs/1901.05761)  
21. Sequential Neural Processes, [http://papers.neurips.cc/paper/9214-sequential-neural-processes.pdf](http://papers.neurips.cc/paper/9214-sequential-neural-processes.pdf)  
22. Modeling Long Sequences with Structured State Spaces | TransferLab — appliedAI Institute, [https://transferlab.ai/pills/2022/state-spaces-for-long-sequences/](https://transferlab.ai/pills/2022/state-spaces-for-long-sequences/)  
23. Efficiently Modeling Long Sequences with Structured State Spaces \- ResearchGate, [https://www.researchgate.net/publication/355841686\_Efficiently\_Modeling\_Long\_Sequences\_with\_Structured\_State\_Spaces](https://www.researchgate.net/publication/355841686_Efficiently_Modeling_Long_Sequences_with_Structured_State_Spaces)  
24. Structured State Space Models for In-Context Reinforcement Learning \- arXiv, [https://arxiv.org/html/2303.03982](https://arxiv.org/html/2303.03982)  
25. spectraformer \- arXiv, [https://arxiv.org/pdf/2405.15310?](https://arxiv.org/pdf/2405.15310)  
26. Spectraformer: A Unified Random Feature Framework for Transformer \- arXiv, [https://arxiv.org/html/2405.15310v5](https://arxiv.org/html/2405.15310v5)  
27. Rényi Neural Processes \- arXiv, [https://arxiv.org/html/2405.15991v3](https://arxiv.org/html/2405.15991v3)  
28. \[2101.03606\] The Gaussian Neural Process \- arXiv, [https://arxiv.org/abs/2101.03606](https://arxiv.org/abs/2101.03606)  
29. Direct Preference Optimization: Your Language Model is Secretly a Reward Model \- NIPS, [https://papers.nips.cc/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html](https://papers.nips.cc/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html)  
30. Direct Preference Optimization: Your Language Model is Secretly a Reward Model, [https://proceedings.neurips.cc/paper\_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf?utm\_source=chatgpt.com](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf?utm_source=chatgpt.com)  
31. FOCUS: object-centric world models for robotic manipulation \- Frontiers, [https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2025.1585386/full](https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2025.1585386/full)  
32. A Physics-Based Model Prior for Object-Oriented MDPs \- Proceedings of Machine Learning Research, [http://proceedings.mlr.press/v32/scholz14.pdf](http://proceedings.mlr.press/v32/scholz14.pdf)  
33. Curriculum Direct Preference Optimization for Diffusion and Consistency Models, [https://cvpr.thecvf.com/virtual/2025/poster/33027](https://cvpr.thecvf.com/virtual/2025/poster/33027)  
34. NeurIPS Poster $\\beta$-DPO: Direct Preference Optimization with Dynamic $\\beta$, [https://neurips.cc/virtual/2024/poster/94622](https://neurips.cc/virtual/2024/poster/94622)  
35. Deep Learning for Scientists and Engineers \- Schools CEA – EDF – INRIA, [https://ecoles-cea-edf-inria.fr/files/2025/06/Neural\_Operators\_new-Part1.pdf](https://ecoles-cea-edf-inria.fr/files/2025/06/Neural_Operators_new-Part1.pdf)  
36. \[1910.03193\] DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators \- arXiv, [https://arxiv.org/abs/1910.03193](https://arxiv.org/abs/1910.03193)  
37. FlowNet: Modeling Dynamic Spatio-Temporal Systems via Flow Propagation \- NIPS, [https://papers.nips.cc/paper\_files/paper/2025/file/c8db30c6f024a3f667232ed7ba5b6d47-Paper-Conference.pdf](https://papers.nips.cc/paper_files/paper/2025/file/c8db30c6f024a3f667232ed7ba5b6d47-Paper-Conference.pdf)  
38. UltraModel: A Modeling Paradigm for Industrial Objects \- IJCAI, [https://www.ijcai.org/proceedings/2025/0876.pdf](https://www.ijcai.org/proceedings/2025/0876.pdf)  
39. DeepONet: Learning nonlinear operators for identifying differential equations based on the universal approximation theorem of operators \- arXiv, [https://arxiv.org/pdf/1910.03193](https://arxiv.org/pdf/1910.03193)  
40. Quantum DeepONet: Neural operators accelerated by quantum computing \- arXiv, [https://arxiv.org/html/2409.15683v1](https://arxiv.org/html/2409.15683v1)  
41. Refining VLM-Guided Concept Bottleneck Models with Minimal Annotations \- arXiv, [https://arxiv.org/html/2605.16405v1](https://arxiv.org/html/2605.16405v1)  
42. CONCEPT BOTTLENECK MODELS UNDER LABEL NOISE \- OpenReview, [https://openreview.net/pdf/e16183c6351fa57a5fbd59a42ddc93188e1c0db1.pdf](https://openreview.net/pdf/e16183c6351fa57a5fbd59a42ddc93188e1c0db1.pdf)  
43. Modern Hopfield Networks with Continuous-Time Memories \- arXiv, [https://arxiv.org/html/2502.10122v4](https://arxiv.org/html/2502.10122v4)  
44. Modern Hopfield network \- Wikipedia, [https://en.wikipedia.org/wiki/Modern\_Hopfield\_network](https://en.wikipedia.org/wiki/Modern_Hopfield_network)  
45. Learning Clinical Representations Under Systematic Distribution Shift \- arXiv, [https://arxiv.org/pdf/2603.07348](https://arxiv.org/pdf/2603.07348)  
46. Debugging Concept Bottleneck Models through Removal and Retraining \- arXiv, [https://arxiv.org/html/2509.21385v1](https://arxiv.org/html/2509.21385v1)  
47. Editable Concept Bottleneck Models \- arXiv, [https://arxiv.org/html/2405.15476v3](https://arxiv.org/html/2405.15476v3)  
48. Multimodal Concept Bottleneck Models \- arXiv, [https://arxiv.org/html/2606.19882v1](https://arxiv.org/html/2606.19882v1)  
49. modern hopfield networks \- arXiv, [https://arxiv.org/pdf/2502.10122](https://arxiv.org/pdf/2502.10122)  
50. \[2502.05164\] In-context denoising with one-layer transformers: connections between attention and associative memory retrieval \- arXiv, [https://arxiv.org/abs/2502.05164](https://arxiv.org/abs/2502.05164)  
51. Modern Hopfield Networks and Attention for Immune Repertoire Classification \- arXiv, [https://arxiv.org/pdf/2007.13505](https://arxiv.org/pdf/2007.13505)  
52. Sparse and Structured Hopfield Networks \- arXiv, [https://arxiv.org/html/2402.13725v1](https://arxiv.org/html/2402.13725v1)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACYAAAAaCAYAAADbhS54AAACV0lEQVR4Xu2WS6hOURiGX5dco9wlKbeipJRLSu4DZSJRRs4vJcqZoFwGOhLJwMjEgE7JvSS3CAlFCBmJgTNTpNzKlPft25vltbfzn/0fZ/Q/9dRe37fW/tde+1tr/0CTnmMFPeTBOhhGL9GhnugOJtP7tJ8n6mQZvUn7eKIR+tNndJYnusgJusuDjdBKH3iwAvPoezrQE1V5TGserEgH3erBKkyhP+gYT1Sknd7xYBXW088ebICN9IsHUzbRW/QqHU+v04eIpV6T9DtCnyRtp0Yf0Rf0JKKOztGzdOXvbr9YiHgDYz0hJtJTiNejTq/ogizXQr/RcVn7PGKbF1GjexBHgApa93pOR9B7iAk7MxH9ZnhC7ECcK/ns0yfTtWJrs7YORj19EZdpr+x6GmKcdrAmqTGLslzKBES/xRb/g730Ox2cxHYiBuqUF1ox2RlbEOMmecJQ2aifFqaUa/SGxa4gBo7M2sdQ/ipTTtM3HixAr1D3n+2JnL6I3ZaexKMQK6iCz9G3sahWNP4AYqPoM/WRHk/yq+iGpJ2jWtbERnsiZy6ig55UddKbnkF8Dwck/XRz/aizFDFeh+Xm7PpgltMDapWHZO2UFvrBgynb6FfahliRp/Qw4ruYoprRj063uP4pqMC1+zSJ5Yjj5gLdh9iZRRxFbJpSLuLv+iqjA7GTuwOdies8mKPX9onu90QJu+lLD1ZgKn2HqM9C5iBez2pPlKCae0vne6KLtCNqrJTXiIlpFbZbrgxN6i7+8bSdsATxyfov6Aho82AdDKe36SBPNGnSk/wEc5BvjJMnrV0AAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGIAAAAaCAYAAABM1ImiAAAEzUlEQVR4Xu2Zd+xkUxTHv7qIHtHZn1VW7yREZLUIETX4R9QgVkRLtBCL6L1L9BpELyEEa3X/YHeVaCuiEzUIIpzP79y7c+d485t5b2QzZD7JN5l7zn1v7rx7z7nnvpGGDBkypBvjTfdEY4/cZFo/GgeRfU2nmG7QYA54PtNU00iw98rSptdMy0RHNxYw/WT6q6Ye4uIGHGyaIb/HxHbXQHCN6ahorMkBpkejsRcukj+YL01P9qCfTduOXtmMnTWYE7G6/LctHB01Iaq+MW0cHd1YzvSrPDIWC77IWqZno7EmO2owJ+IC0/XR2JAbTXdFYy9cIn84J0dH4HbTNtFYk+01mBPxiWmvaGzIgaY/TPNERzfYXIgK0tMiwZchGp6KxgZ0mogt5Ln1JdPLprNNc7f1kDY33WF6wnSfaZJpsumD5GvKOPmY1o2Ohqwqv98m0dELea+YHOwZomHraGxA1USwb3xu2jC1ybOPqL0o2Fu+ylYo2tyH6ovJqRobk3u3vJKZYLrU9Kpppumcot9u8nstWthKNpPvj6/IF+Om8sqPZ3Ji0a+EsTLG2hAVbFY/mBYPvjVNTwdbU+JEzG/6WJ4eS9aW99svte83fddyj44RPwuoijlMz8gn9Q3T16ZDkz1HwK6p7xGmP9PnyDqmW00LpjblLeNYTz6Z3Cf7SsguRGwjLpbf+PRgv8W0XbA1JU7EDqlNXi2ZM9nvTW0exi8t92hhgf+8wlbCqj1NPhE/ms4tfDw4rr0stY81fdFyt0GfFdNnJpFFQ5QB331I+hx5R35masSypt/kM57DdBXTi7N69E+ciMNTe//ULuHBv5k+T5T32ym1Wd08vJVTuxNbya8riwxSDbazUpuI+Krl7gj7JNdxVujGW/KF0Jir5V92RmpfKy85/y3iROT8HMN43mSfktobyfPyA/KwZ19YLfnG4gR5RBAZmePk986paR95Tu/GYfLrRoK9Cva8Y6KxDuPkUcFewQp4vt3dBlXNlabLTdfJv5iJ42F3Ip4jqNJY2TlNZNaQ98ub4ZHyk3ldHtY/T7pUZWy8c6V2HtNCs3q0YJJyqqZ4eK/wjcjTeRXsOXtGY1046jOwD+UVTSdYxfkE+bZ8Al7X2APAx73LKNvD9K184oFouNk0Tf4aBriO6oe8e5I8PXQrWXnQ38vTRE61pMLP1J7SxsvHtEFhA6KIB8rhjE37d9NzyccivE0eqZER+f0ocvpiJfkApss3qE7kUnJJecVFBTQWrHrOKwyS/F+WkLw24ftYrUQIkVWe9FmtRCnXluIacn4VLBL6nCk/n/AQebO6fNkpMVO+70TY5B+XvyNjv3ksiZM4k1MFZSv7LAVH3xxk2jIaO7CLvM4GVl63CakLJ9R35WmAw1L+gUvJ9wzSBVEUOVr+6iYeDKtg/3kwGhtyoTxlzzZIYeRuzgC5Ajle1XV1P+STatXrZQ6B+JiUCKt/SjR2gDTHhk3l2A9M+kdqpdnZwlXyA9Wpphfkf4yMtVH3A+eIK9S+8jlUEYlVf+QQRbwF7bSZVnGnfCH1A+chCpf/Lay0803vq/VK/lN5RRPT0u7yqohI4QDGxt8LS8iv4410E4jKqWoVGEP6YIIavsKWR9Qg/vM4ZMiQIUP+o/wNzXsXW3/vNu4AAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAaCAYAAADIUm6MAAACS0lEQVR4Xu2WTYhOYRTH/z4ajDKMYmHhI4U0WMjCR1NYTVYWSiEpNsrHbJiJKSs2SLJQJCFmSpoGJUnIDjNiKQtDlj5KFhL/v/Pccea89/2w0PvK/dWvee95nvvOuc8958wABQU1004P0xN0S1hraNbSu/QH7AH+KVpQv8SvwX73J/oAdojyYYp/o6tGdgcmoz6JT6If6Tk6wcWbYQ/xnW5y8RImoj6Jb6aXQ2wcHYDlU7XnyiU+i16kz+gj2GudOWqHnVQP7ad36DF6iPaiNKnIJbooxM7DctkV4rnkJT6PvqXbXUzrr2lruh5Pn9Kz6XosHaJ9tINeSPFyzA7XR2B57AnxsuQlfhV20h4l+h5Wk2I57L79IztsrCo2zcVqYRvsvu64UImYeNaseSemjv+QPi+E7Tvwe/lX4mqqqS5WjQ2w6XE0LlQjJt6WrlVvkZuwNdW/yEaX3sZ0OkiPp7VaWE+/0lMh3k67QqyEmLhqWNcql8h92OloZIkr9CB9RZ/QvSleC6vpZ1iPjAlrKkeVYkXy5rgmhBrNoy9/Q2+72Av3+U9YCis5TS01tWcdfR5iucyAJa5RlrGAvqNbXWw37C/cYhfTw52EPfQ+uhH2fZWYS4fpDdjc9vFO2O/QW6zIDtikUOLynlubT2/BktMYVD0vcetCMzy7NzOr2fj6xRRYWcV7onPS/r+CHlonpwbT/zsZOvUvdKeLNRSqzzMxmLhOT8dgo7AMVkJqtIwm2GRR461w8YZjDX2cVA+8TD9X+k0FBQX/CT8BEAKMgJRSIDsAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAaCAYAAAAJ1SQgAAADNklEQVR4Xu2YaahNURTHl3keCpmSuUSS+RuPkGT6RHkyFyFkHj5QIimUIZKUzJEpkSES+YIoUUTPF0O+iEKU+P/v2sfZd71zz+W8e+6j7q/+vXv/a+979t5n7bXPeSIl/imaQwegu9BFqHt2uPqoA52GOthAFdgLDXefV0LPoLphOONN9b4XjT3QRGtWkUvQVve5E/QTGvo7KlITugkN87zUmQKdsWaBKROdbGfjd4XeQE2M/0c0hdZCx6Dz0A3oDrQKquW1C+DqvoZG24CjMXQVeig62C9Qq6wWIhuhj6LxT6L703ICOmRNxwVouTXzwfx/Di0TnURAS+gBdB2q5/lkPPQCqmF8yzroleiEogY2QHRBou7QNNGJ1rcBxyzRBff3cyzcG2+hHjbgYKHgQNcb/zC0y3hRcG8NgX6Ipp1dtMnQBuORvtA20cXsAnXMDmfoJjq2oJjFMlu08Sgb8ODgONB7xmeFXGg8SyPRzCBHRa81Jwxn2C26GD4tRBeTBagM2iSV92xAhWhGxsI7+Vn0LIuDA+Yg33teM+dN8LwoxkHb3ed+on0eheEMj6HaxmPNYNtAXyW6bpArogsWC1OQPzTXBgxcdba77Xl9nGfviIUTHeN958DYb4T7zgU/G4YTcRI6bk0frtI70QvnSo+ALaLt/P050Hm9PS8KFh5W5QBWbvY7575zGywKw4nYD12zpk9DCVPEppBPG9FU/y7ZEwvuLP/mor1ED+K+aN/+omd0r+zwX7NP9JiMhXuFF21gAx7cC2yz2vh8NMyXxtOlcj9SLtqXE31qYklgCufdCqxwvKi/p3zmi8a5cpagaI21AQ9W00HWFM0kns/sf9DEknAZ2mlNC1P5JfRENF0DeEBvhr5BSyX3Q0MFtNiaDt55Vm/7xBTAfcrJFuJhng9D86wZRWtoB3RLtNzzbrC6rYDaeu2i4F05Yjw+BfG3eFRwMh8kekGYGVwMf5GTwP68zmAbKDQzRQfMV7zqguc8MzN1+OLA42uSDRQRZtYSa6bFAol+UykG/O8FT5RcLwkFh29IPEJG2kDK8Lqswj1tIG14Tp+C2tlAiqyBZlizRIkS/z+/APhLoB+HCTASAAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAbCAYAAACjkdXHAAAAvUlEQVR4XmNgGAU0AUFA/ApdkBggDMR3gPg/EHOiyREEBUC8gAGiWRVVCj/wZ4Bo6GKAaLZHlcYNBIE4BMouZoBojkBI4weZQMwIZccxQDQXIqRxA1cg1kHiezJANIOcjxcIAfETBohidLwYSR1WQJHmKUAsjiYmxwDRvBtNHAWAogYUr+iAmwGi+Sq6BAyA4vM2EHOhS0DBVyD+jC5oBsRngPgvA8J0NiT5BiA+BJUD4WNAXIokPwpGAW4AAOsgK922XdbHAAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAaCAYAAAAJ1SQgAAADLUlEQVR4Xu2XWahNYRiGX/PMDZmShIikjHeKEDJdGAplLELIPCRKJIVMkQs3pkSmyBiJ3CBKFNFxYcqNKESJ9z3f2ta/Pmvvzdlnn0Ptp9723u+3/v1P3z8soMQ/RQNqB7WNukiNToarjzrUCaqdDxTAampv9H0BVUbViMNYTk0JflcZe6ix3iyQZdT56PtM6gOSna1JXacGBl7RmUSd9GYlc5pa603SkXpNNfGBP6EpLH2OUGeoa9QtagVVK3gug0b3FTXMByIaU5ep+9QP6jPVIvEEsAE2a4p/pM4FsR6wNXuDahP4IWeppd7Mh/L/KbUE1okMzal71FWqXuALbRrPkEyvNNZQL2AdSmtYH9iAZJuhcdRLpHd4BmzA6/pANrZQb6iuPhAxCNbQdc4/SO1yXhpaWwOo77C084M2kVrvvPmIM6YLrP7xcfgXnWAxtTEvWvx6eKgPBKhxaugd5z+BNSoXjWCZIQ7D6poVh8vZDRuMEP23lo8YCau/fRxOoJ1aGZkTzeQn6rYPONRgNfJd4DWLvDGBl8Yo2LoTvWBlHsThch5StZ2nmdoKm/ED1PBENMkl2IDlRCmoymf7gEOjruduBl7PyPMz4lFHRwS/1TCVGxz91oCfisMV4hh11Jsh2l3fwiru4GKezbDnwvXZN/K0Y+ZCG4925Qxahyqn40RoGejSUAj7qSveDGkIq1TyKRTSCpbq35DsWGZm9ZmNtkhvxF1Y2d6wM7p7MvzX7IMdkznRWlGluodmQ2tBz6x0vq6G+dJ4Kn4vJybDyqqjj12sIiiF8y6FjbBKwzUVMhcW18h5MpuWdsps6Gjq501YJul8VnltPoVygdrpTY9S+Tn1CJauGXRAb6K+UouR/dJQRi30ZoRmXru3vzFl0DpVZyvjMq/L0BxvptGS2g67kumKqNnQ7qaLeOvguTQ0K4ecp1uQ/usLrDPvkT4gygwNRjjIFUHlVU9/H6hspsMarFe86kLnvDKz6OjFQcfXBB+oQpRZi7xZLOYh+aZSlXSGnSj1faBY6A1JR8gQHygyqle7cDcfKDY6p48j/RWsWKyipnmzRIkS/z8/Adu+oBGC07RnAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAaCAYAAAAT6cSuAAAClklEQVR4Xu2WS6hPURTGP0keKUK5EdeAPEKuRxggBopSZIBSShFG16sUChmYYOCRR/KcSAZKRiKvJEop8komkpKJgZD4vrvOcfde9+xzzuSWdH711X9/a+3z3+vsfc46QEPDP00LdYa6TT2i1sXhWgygBnkzgf5nrTe7gyHUM2pTNh5BvaH25Akl9KDGwG7GC2pLHC5kJfWbWu8D3cFBWHEhG6jPVC/ney5T96mLsAVXFdefeovy4o7DdlY50pI4jOXUhyz2k3pIjY4yAt7DFhmyADZ5jvNTzEK94vbDbqZyy47+XNi6lHctDnWgm64Cx/lAiJ41XeCk86dl/i7np6hTXCt1k5qJ6uL2Umuo17DcqXG4Y923nNeF6bDJR50/KfPPOj9FneIuUW3ozE0dS3GXGgp7PJR7IQ5jBbXTeV2Yh+LiJmS+FlSHquIUPxf8LituIPU4+92X+kj9oIb9zQBOU7ODcSFKKCpufOafd36KquLuoHNxVcUtow4EY+2Q8vcF3kuqZzAuZCxs4jHnT8z8w85PkS94qw+Q1Yif3arijlALg/Fg6itsB7WTk6krQTyJepz+SA08ZEbm73Z+ilRx/agHVO/AqyruKeJ8cQg2p53aTG2Mw2n0RrrqvEWwiy12fop8wdsSfpnCHjWKuhGMc1qpX7DXv+I6cbVQ73kF+9rI2Q47BmETV89bFYxD8iI0rwo14dTOqT34G5SjN6bmvfOBMvrAjs7SbKxzrd3Us5KjwnXudXHfc8R8WEz9qQrdIOX6o6V1qHep+CKmwOb5nlyJPnh3wF7Xp2BvLM896hPij2M9A89hRyY/Zk+oE0FOzkjYp9p3WN432DWHw/7zS+Yrrs+5Iq7DelxDQ0NDQ0PD/8ofcLaidoSfF5UAAAAASUVORK5CYII=>