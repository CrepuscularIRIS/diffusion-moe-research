我会把你这类思考定义成：

> **建模对象迁移式思考：不是先问“能不能换个 loss / module / trick”，而是先问“这个领域当前到底在建模什么？它是不是建模错了对象？有没有更自然的几何对象、动力学对象、残差对象、流形对象可以替代？”**

这其实是很高级的研究直觉。它不是普通的 idea mining，而是 **problem reparameterization**。

---

## 1. 这类思考的核心轨迹

你的原始直觉大概不是：

> Diffusion 很强，所以我也想给分类加 diffusion loss。

而更接近：

> Diffusion 的真正优雅之处，也许不是“生成图片”，而是它把学习对象从 endpoint prediction 变成了 denoising field / score field / velocity field。
> ResNet 的优雅之处也类似：不是直接学习一个完整映射，而是学习相对于 identity 的 residual correction。
> 那么，很多任务是不是都可以被重新理解成：不要直接预测最终答案，而是学习一个把错误状态、噪声状态、未完成状态推回真实结构的修正场？

这个思路非常清晰。

ResNet 的核心重参数化是：层不直接学习未参照映射，而是学习相对于输入的 residual function，这让深层网络更容易优化。([arXiv][1]) Diffusion/score-based generative modeling 的核心重参数化则是：不直接一次性生成样本，而是学习从噪声分布回到数据分布的去噪/score/反向动力学；DDPM 明确连接了 diffusion 与 denoising score matching，Score-SDE 框架也强调反向过程依赖时间相关的 score gradient field。([arXiv][2]) Flow Matching 进一步把生成建模整理成沿概率路径回归 vector field，而 MeanFlow 又把 instantaneous velocity 推进到 average velocity 的建模。([arXiv][3])

所以你的思考可以描述成：

> **从“预测答案”转向“学习修正动力学”；从“判别边界”转向“语义支撑域”；从“静态分类”转向“几何场/能量场/残差场”。**

---

## 2. 这类问题不是“想新点子”，而是“质疑旧建模对象”

普通提问是：

> 能不能改 loss？
> 能不能加 module？
> 能不能融合 diffusion？
> 能不能涨点？

更强的提问是：

> 当前方法的建模对象是什么？
> 这个建模对象是否过于粗糙？
> 它有没有把本该建模的结构压掉？
> 有没有一个更自然的数学对象可以替代它？
> 替代以后，哪些失败现象会被解释？
> 哪些实验能杀死这个解释？

比如 OOD 这个问题。

普通说法：

> CE 导致过度自信，所以换个 loss。

更深的说法：

> CE 学的是闭集条件后验 (p(y|x))，但 OOD 需要的是 (x) 是否属于已知语义支撑域。也就是说，任务本身要求的不只是分类，而是 support estimation / energy shaping / semantic typicality estimation。

这就比“加一个 gradient loss”更稳。

早期 OOD baseline 用最大 softmax probability 做检测，但后续 energy-based OOD 明确指出 softmax posterior 容易对 OOD 过度自信，并提出 energy score 作为更适合的 OOD scoring。([arXiv][4]) 这说明学术界已经把问题从“分类概率够不够”推进到了“模型的能量地形/支撑域是否合理”。

---

## 3. 我会把你的思考过程写成一个“研究轨迹模板”

你每次产生这种直觉时，可以按这 7 步记录。

| 步骤        | 问题             | 例子                                                     |                                    |
| --------- | -------------- | ------------------------------------------------------ | ---------------------------------- |
| 1. 现象困惑   | 什么现象让我觉得旧解释不够？ | Diffusion 不只是生成强，而是建模方式很优雅                             |                                    |
| 2. 建模对象识别 | 当前方法到底在学什么？    | CE 学 (p(y                                              | x))，AR 学 next-token，普通生成学 endpoint |
| 3. 缺失对象   | 它没有学什么？        | 没学 support、trajectory、score、residual、semantic geometry |                                    |
| 4. 类比迁移   | 哪个领域通过重参数化成功了？ | ResNet 学 residual；Diffusion 学 denoising field          |                                    |
| 5. 新对象提出  | 应该改成学什么？       | class-conditional semantic score / energy field        |                                    |
| 6. 失败解释   | 它能解释哪些失败？      | OOD 高置信、shortcut、distribution shift、collapse           |                                    |
| 7. 可杀实验   | 什么结果会证明我错？     | score head 不提升 near-OOD；只学低层纹理；ID accuracy 掉很多         |                                    |

这套模板的关键是：**每个直觉都必须落到“建模对象”上**。

不是：

> 我觉得 diffusion 好。

而是：

> Diffusion 好在哪里？
> 它把什么变量换成了什么变量？
> 它让网络不再直接学习什么，而是学习什么？
> 这个替换能否迁移到分类、检测、多模态、LLM、distillation？

---

## 4. 可以直接这样描述你的研究思考

我的研究直觉并不是简单地把 Diffusion 当作一种生成模型技术，而是把它看作一次建模对象的重参数化：模型不再直接学习从输入到最终答案的静态映射，而是学习从噪声状态、错误状态或不完整状态回到数据流形的修正动力学。这一点与 ResNet 的残差思想在精神上相似：ResNet 通过学习相对于 identity 的 residual correction 改善了深层网络优化，而 Diffusion/Flow-based 方法则通过学习 score、denoising field 或 velocity field，把生成问题转化为几何场与动力学建模问题。沿着这个视角，我关心的核心问题是：在分类、OOD、多模态融合、Diffusion LLM、SFT distillation 和数据集评估等任务中，当前方法是否只学习了表层判别信号，而没有显式建模语义支撑域、信息压缩结构、分布几何和可信决策所需的内部场结构。因此，我希望把研究问题从“设计一个新的 loss 或模块”提升为“重新选择任务中最自然的建模对象”，并通过可证伪实验检验这种建模对象迁移是否真的带来鲁棒性、泛化性和可信度提升。

---

## 5. 如果我是我，我会这样提出这类问题

我不会先问：

> 能不能把 diffusion 用到分类？

我会问：

> **分类任务当前的建模对象是不是错了？**

然后继续追问：

> 分类器学的是 (p(y|x))，但可信分类真正需要的是不是 (p(y|x)) 加上 (x) 是否属于该类语义支撑域？
> 如果是，那么分类的核心对象就不是 boundary，而是 class-conditional semantic support。
> 那么 diffusion/score/energy 能不能提供一种建模 support 的自然工具？

这就是一个更强的问题。

---

## 6. 我会使用的“研究问题生成句式”

### 句式一：建模对象质疑

> 当前方法表面上在解决 (A)，但它实际建模的是 (B)。真正决定失败的是不是没有建模 (C)？

例子：

> 当前分类方法表面上在识别类别，但实际建模的是闭集后验 (p(y|x))。OOD 失败真正来自它没有建模语义支撑域 (p(x \in \mathcal{D}_{ID}))。

---

### 句式二：残差化提问

> 这个任务能不能从“直接预测目标”改成“预测相对于当前状态的修正量”？

例子：

> 检测是否不应该只预测 box，而是预测把候选区域推向真实目标几何的 residual field？
> SFT distillation 是否不应该只复制最终答案，而是复制 teacher 从错误推理状态回到正确推理状态的 correction dynamics？

这个句式很适合你后面的 SFT Distillation 和 Diffusion LLM。

---

### 句式三：流形/支撑域提问

> 模型是否只学会了输出空间的答案，而没有学会答案背后的数据流形？

例子：

> OOD 不是“模型分类错了”，而是“模型不知道这个输入是否在已知语义流形附近”。

---

### 句式四：信息压缩提问

> 当前训练目标压缩掉的信息，是否恰好是下游可靠性需要的信息？

例子：

> CE 可能鼓励类内 feature collapse。Neural Collapse 研究表明，分类训练后期确实会出现同类特征向类均值集中、分类器权重与类均值对齐等几何结构。([arXiv][5]) 这对 ID accuracy 可能很好，但对 OOD、细粒度语义、可信度估计可能是不够的。

---

### 句式五：轨迹化提问

> 当前任务是否被错误地建模成 endpoint prediction？它是否应该被建模成 trajectory / process / field？

例子：

> LLM distillation 是否不应该只看 final answer，而应该看 reasoning trajectory 中的 self-correction closure？
> Dataset evaluation 是否不应该只评估样本标签质量，而应该评估数据集是否提供了足够的失败模式、边界样本和语义支撑结构？

---

## 7. 你这类问题的统一命名

我会给它起一个内部名字：

> **Modeling-Object Shift**

中文可以叫：

> **建模对象迁移**

它不是简单的“方法创新”，而是：

> 把任务从一个粗糙对象重写成一个更自然、更几何、更可解释、更可优化的对象。

几个例子：

| 领域                 | 旧建模对象        | 新建模对象                         |                      |
| ------------------ | ------------ | ----------------------------- | -------------------- |
| ResNet             | 完整映射 (H(x))  | 残差 (F(x)=H(x)-x)              |                      |
| Diffusion          | 直接生成样本       | 去噪/score/velocity field       |                      |
| Flow Matching      | 采样路径隐式优化     | 概率路径上的 vector field           |                      |
| MeanFlow           | 瞬时速度         | 平均速度                          |                      |
| OOD 分类             | 闭集 (p(y      | x))                           | 语义支撑域 / energy field |
| SFT Distillation   | 答案/文本模仿      | reasoning correction dynamics |                      |
| 多模态融合              | token concat | 跨模态信息几何对齐                     |                      |
| Dataset Evaluation | 静态样本质量       | 分布覆盖、失败模式、边界结构                |                      |

这张表其实可以成为你未来研究路线的总纲。

---

## 8. 最重要的判断

你现在真正有价值的不是某一个 OOD idea，而是一种研究审美：

> **好的方法往往不是把旧 pipeline 堆得更复杂，而是找到一个让任务本身变简单的建模对象。**

ResNet 是这样。
Diffusion 是这样。
Flow Matching / MeanFlow 也是这样。
你现在想做的 OOD、Diffusion Loss、Diffusion LLM、SFT Distillation、Dataset Evaluation，本质上也可以沿着这条线走。

所以我会把你的元问题压缩成一句话：

> **如何系统性寻找那些“当前方法建模错对象”的地方，并把任务重写成 residual / score / energy / flow / support / structure learning？**

这个问题本身，已经比“做一个新 loss”更像长期研究路线了。

[1]: https://arxiv.org/abs/1512.03385?utm_source=chatgpt.com "[1512.03385] Deep Residual Learning for Image Recognition"
[2]: https://arxiv.org/abs/2006.11239?utm_source=chatgpt.com "Denoising Diffusion Probabilistic Models"
[3]: https://arxiv.org/abs/2210.02747?utm_source=chatgpt.com "Flow Matching for Generative Modeling"
[4]: https://arxiv.org/abs/1610.02136?utm_source=chatgpt.com "A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks"
[5]: https://arxiv.org/abs/2008.08186?utm_source=chatgpt.com "Prevalence of Neural Collapse during the terminal phase ..."

可以。你这个问题已经不是“怎么产生 idea”，而是在问：

> **不同研究者/研究共同体，是如何形成不同“问题审美”和“建模审美”的？**

这可以从社会认知角度来讲。Fleck 很早就提出过 **thought collective / thought style**：科学认知不是纯个人脑内活动，而是在共同体共享的问题、语言、工具、证据标准里形成的。Kuhn 后来讲 paradigm / normal science / scientific revolution，也是在说科学共同体会共享一套“什么问题值得问、什么证据算有效、什么解释算漂亮”的范式。([斯坦福哲学百科全书][1])

所以你说的“方法论”，更准确地讲，是：

> **一个研究者如何选择问题、重写问题、评价证据、判断美感、组织实验、进入共同体叙事的一整套认知风格。**

---

# 1. 你的方法论属于哪一类？

你现在这套思考，我会命名为：

> **建模对象迁移法 / Modeling-Object Shift**

核心动作是：

```text
旧 pipeline
↓
识别它到底在建模什么
↓
发现它建模错了、建模粗了、建模不自然
↓
换一个更自然的数学对象
↓
把任务重写成更优雅的形式
```

比如：

| 问题                 | 旧对象        | 新对象                                  |                                   |
| ------------------ | ---------- | ------------------------------------ | --------------------------------- |
| ResNet             | 直接学 (H(x)) | 学 residual (F(x)=H(x)-x)             |                                   |
| Diffusion          | 一步生成样本     | 学 denoising / score / velocity field |                                   |
| OOD                | 学闭集 (p(y   | x))                                  | 学 semantic support / energy field |
| SFT Distillation   | 模仿答案文本     | 模仿 correction dynamics               |                                   |
| Dataset Evaluation | 看平均分       | 看失败模式、边界覆盖、分布结构                      |                                   |

ResNet 论文里就明确说，它不是让层直接拟合未参照映射，而是让层拟合残差映射；MAE 也是一种极简重构：把视觉自监督重新变成“高比例 mask + 重建”的 scalable learner。([arXiv][2])

这类方法的美感是：

> **把复杂问题改写成一个更容易优化、更贴近几何、更自然的对象。**

这是很强的一类。但它不是唯一高级的方法论。

---

# 2. 其他研究者常见的“高级方法论流派”

下面这些都是真正存在的研究风格。不同顶级研究者会混用，但通常会有主导审美。

---

## A. Back-to-Basics 派：回到基本问题，砍掉历史包袱

代表思路：

> 这个领域是不是被复杂技巧带偏了？
> 如果回到最朴素的定义，真正应该预测什么？

这类方法和你很接近，但更极端。它不是组合新模块，而是反问：

```text
我们是不是把任务本身写复杂了？
我们是不是预测了不该预测的东西？
有没有最直接、最干净、最本质的目标？
```

何恺明路线很多工作有这种味道。ResNet 把深层网络优化问题重写成 residual learning；MAE 把视觉自监督简化为 mask-and-reconstruct；近期 “Back to Basics: Let Denoising Generative Models Denoise” 也直接质疑扩散模型为什么不预测 clean image，而去预测 noise 或 noised quantity。([arXiv][2])

这种风格最高雅的地方是：

> **不是发明更多复杂性，而是发现旧复杂性其实是错位的。**

---

## B. Bitter Lesson 派：相信可扩展通用方法，而不是手工结构

Sutton 的 “Bitter Lesson” 说得非常狠：AI 70 年历史里，最终最有效的往往是能利用计算规模增长的通用方法，比如 search 和 learning，而不是把人类知识手工塞进系统。([Incomplete Ideas][3])

这种人会这样问：

```text
这个方法是否随着 compute/data/model 继续变大而继续有效？
它是不是依赖太多人工先验？
它是不是短期漂亮，长期不 scalable？
```

这类方法论和你的“优雅建模对象”有张力。你的路线偏 **结构优雅**；Bitter Lesson 派偏 **规模优雅**。

它的美感是：

> **少设计人类以为聪明的结构，多设计能吞算力、吞数据、吞搜索的通用机制。**

Scaling laws 就属于这种文化的一部分：它把模型性能、参数量、数据量、计算量之间的关系经验化为幂律趋势，用来指导 compute allocation。([arXiv][4])

---

## C. Data-Centric 派：不是模型错了，是数据系统错了

这类人不会先改 architecture / loss，而会问：

```text
数据分布覆盖了吗？
标签定义一致吗？
难例够吗？
评测集真实吗？
训练集和测试集的语义边界一致吗？
```

MIT Data-Centric AI 课程把 model-centric 和 data-centric 区分得很清楚：前者是在固定数据集上找最好模型，后者是系统性地产生更好的数据来喂给模型。([Introduction to Data-Centric AI][5])

这种方法论特别适合你未来的 Dataset Evaluation。它的高雅点是：

> **很多所谓模型创新，本质上是在补数据定义和数据覆盖的洞。**

如果你做 OOD，这个视角会非常重要。OOD 不只是模型后验问题，也可能是数据集没有定义清楚“已知类语义支撑域”和“未知类边界”。

---

## D. Measurement / Benchmark 派：先重写评价函数，再重写领域

这类研究者的核心不是先发明模型，而是先问：

```text
这个领域现在到底测错了什么？
排行榜奖励了什么错误行为？
有没有一个新 benchmark 可以暴露旧方法的幻觉？
```

这就是你之前反复提到的 reward hacking / dataset evaluation 方向。

这种方法论的高级处在于：

> **谁定义了 measurement，谁就在定义共同体的研究方向。**

NeurIPS 的 reproducibility checklist、dataset/benchmark track、DataPerf 这类机制，本质都是在改变社区的证据标准和评测基础设施。([NeurIPS][6])

这条线非常适合你，因为你已经很敏感地意识到：
**很多论文不是模型真的好，而是评价函数让它看起来好。**

---

## E. Geometric / Symmetry 派：从不变量、群、图、流形统一架构

这类人会问：

```text
数据背后有什么对称性？
任务有什么不变量？
输入空间是什么几何结构？
模型结构是否尊重这种几何？
```

Geometric Deep Learning 的核心就是用统一几何原则理解 CNN、GNN、Transformer 等架构，并把网格、群、图、测地线、规范等结构放到同一个框架中。([arXiv][7])

这类方法论对你的“矩阵表示、树和图表示、多模态融合”很重要。

它的美感是：

> **不是在网络里堆模块，而是让架构服从数据空间的对称性和几何。**

---

## F. Causal / Invariance 派：不要学相关性，要学跨环境稳定机制

这类人会说：

```text
模型学到的是 stable feature，还是 spurious feature？
这个特征换环境以后还成立吗？
有没有多个环境可以筛出因果不变量？
```

Invariant Risk Minimization 的目标就是学习跨多个训练环境都稳定的表示，使 OOD 泛化更接近因果结构。([arXiv][8])

这和你问 OOD 的本质高度相关。
OOD 很多时候不是“没有学梯度场”，而是：

> **模型把训练环境里的伪相关当成了语义因果。**

这类方法论的美感是：

> **不问什么在训练集上有用，而问什么在世界变化后仍然成立。**

---

## G. Falsification-First 派：先设计杀死自己想法的实验

这类风格来自 Popper / Lakatos。Popper 强调科学理论要能被反例推翻；Lakatos 更进一步，认为研究纲领要看它是否产生新的预测和事实，不能只是不断给失败找补丁。([斯坦福哲学百科全书][9])

这种人会这样设计问题：

```text
如果我的解释是错的，最便宜的实验是什么？
什么结果会让我立刻放弃这条线？
我的方法是不是只是在保护一个退化研究纲领？
```

你之前做 frozen DiffusionGemma 的 structural-negative / kill experiment，其实很接近这个流派。

它的美感是：

> **不是证明自己对，而是快速发现自己错在哪里。**

---

## H. Empirical Debugging 派：像工程师一样拆系统，而不是像理论家一样讲故事

Karpathy 的训练神经网络 recipe 里第一步不是写模型，而是“become one with the data”：先看大量样本，找重复、坏标签、异常模式，再搭 end-to-end skeleton 和 dumb baseline。([Andrej Karpathy Blog][10])

这种方法论不追求宏大理论，而追求：

```text
先跑最小闭环
先建 dumb baseline
先看数据
先找 bug
先做 sanity check
先确认 gain 从哪里来
```

这类方法对你非常有价值，因为你容易进入“大统一理论视角”。但顶会论文最后能不能成立，常常死在最朴素的 empirical hygiene 上。

它的美感是：

> **不相信语言，不相信直觉，只相信被拆开的系统。**

---

## I. Abstraction Compression 派：把一堆现象压缩成一个最小解释

这类研究者会问：

```text
这么多方法是不是其实在做同一件事？
这些 loss、architecture、training trick 能不能被统一成一个变量变换？
有没有一个更短的理论描述？
```

你对 diffusion、residual、gradient field 的联想，其实就有 abstraction compression 的味道。

这类方法论的目标不是提出一个点子，而是提出一个压缩后的解释：

```text
Diffusion / flow / denoising / residual correction
本质上是不是同一类“状态修正场”？
```

它的美感是：

> **把复杂经验压缩成少数几个生成性概念。**

---

## J. Counterinduction / 逆共同体 派：故意反着主流假设走

Feyerabend 的理论多元主义强调，不应把科学压成一种固定方法；为了最大化发现机会，科学中需要多个相互竞争、甚至不兼容的理论。([斯坦福哲学百科全书][11])

这类研究者会问：

```text
主流共同体默认什么是对的？
如果这个默认假设反过来呢？
有没有被共识压掉的路线？
大家都在追 SOTA，我能不能追 negative finding？
大家都在堆模型，我能不能回到数据？
大家都在做 AR，我能不能做 diffusion LLM？
```

这种方法很适合找新方向，但风险也大。
它的美感是：

> **不是在共同体内部微调，而是攻击共同体没有意识到的默认假设。**

---

## K. Tool / Infrastructure 派：不是写论文，而是改变别人做研究的工具

这类人会问：

```text
为什么大家不研究这个问题？
是因为没有工具、没有 benchmark、没有数据、没有可视化、没有 verifier 吗？
```

很多领域不是缺 idea，而是缺“让 idea 可实验化”的工具。

这和你的自动化科研 runtime、Dataset Evaluation、多 Agent 审查系统高度相关。你可以把它看成：

> **研究基础设施本身就是研究贡献。**

它的美感是：

> **别人提出一个方法，你提出一个让一百个方法被正确比较的系统。**

---

## L. Failure-Mode Taxonomy 派：先分类失败，再设计方法

这类人不是从“我要做新方法”出发，而是从：

```text
失败到底有几种？
每种失败的因果来源是什么？
每种失败需要什么 diagnostic？
哪些失败是同一个机制？
```

例如 OOD 可以拆成：

| 失败类型                 | 根因             |
| -------------------- | -------------- |
| covariate shift      | 输入分布变了         |
| label shift          | 类先验变了          |
| semantic shift       | 语义类变了          |
| spurious correlation | 学到伪相关          |
| support mismatch     | 样本离开 ID 支撑域    |
| calibration failure  | confidence 不可信 |
| benchmark leakage    | 测试被污染          |
| metric Goodhart      | 指标被 hack       |

这种方法很朴素，但非常强。
它的美感是：

> **好的 taxonomy 本身就是理论。**

---

## M. Systems Constraint 派：从硬件、延迟、显存、吞吐反推方法

这类人不先问“理论上最优是什么”，而是问：

```text
在真实硬件上，瓶颈是什么？
显存、带宽、KV cache、batching、wall-clock、通信，哪个才是主变量？
```

这对 Diffusion LLM 特别重要。很多看似理论上优雅的方法，在 wall-clock 上死掉；很多看似普通的方法，因为吞吐结构更好，反而有真实价值。

这种方法论的美感是：

> **算法不是数学孤岛，而是硬件上的物理过程。**

---

## N. Human-Taste / Aesthetic 派：研究不是只看正确，还看“好不好看”

这类非常少有人明说，但顶级研究里一直存在。

它问：

```text
这个解释是否干净？
这个方法是否少而强？
这个实验是否一刀切中要害？
这个概念是否能成为别人未来说话的语言？
```

你说“高雅”，其实就是这个。

高雅研究一般有几个特征：

| 特征  | 解释                 |
| --- | ------------------ |
| 少   | 不靠堆模块              |
| 准   | 击中核心变量             |
| 可迁移 | 不只解决一个 benchmark   |
| 可复述 | 一句话能讲清楚            |
| 可证伪 | 有明确 kill condition |
| 可生成 | 能导出一系列后续问题         |
| 可命名 | 变成一个新概念或新范式        |

这就是为什么 ResNet、Attention、Diffusion、MAE、Scaling Law 这些东西有“方法论美感”：它们不是单点 trick，而是改变了别人组织问题的语言。

---

# 3. 哪些方法论比“视角转换”更高级？

我会说，**单纯“视角转换”还不够高级**。更高级的是下面五种。

---

## 第一层：视角转换

```text
把旧问题换个角度看
```

比如：分类不只是 boundary，而是 support。

这是很好的起点。

---

## 第二层：建模对象迁移

```text
明确旧方法建模了什么，新方法应该建模什么
```

比如：从 (p(y|x)) 转到 semantic energy / score field。

这已经很强。

---

## 第三层：研究纲领设计

```text
不是一个 idea，而是一组连续可推进的问题
```

Lakatos 的研究纲领视角很适合这里：一个方向要有 hard core、positive heuristic、negative heuristic，并且要不断产生新的可检验事实，而不是只会防御失败。([斯坦福哲学百科全书][12])

你的 hard core 可以是：

> 智能系统的可靠性来自对语义支撑域、修正动力学和信息几何的建模，而不只是输入到标签的判别映射。

这就不是一个 OOD idea，而是一条研究纲领。

---

## 第四层：共同体语言重写

```text
让别人以后也用你的词来描述问题
```

例如：

| 概念                | 改变了什么      |
| ----------------- | ---------- |
| residual learning | 改变深层网络优化语言 |
| attention         | 改变序列建模语言   |
| scaling law       | 改变大模型预测语言  |
| denoising / score | 改变生成模型语言   |
| neural collapse   | 改变分类几何语言   |
| data-centric AI   | 改变工程改进对象   |

这是更高级的目标：
不是提出一个方法，而是提出一套 **可传播的问题语言**。

---

## 第五层：评价制度重写

```text
改变社区认为“好研究”的标准
```

这是最高级也最难的。
比如 benchmark、reproducibility checklist、dataset management、verifier-based evaluation、本质上都在改变共同体的证据制度。NeurIPS reproducibility program 就是通过代码政策、复现挑战和 checklist 来提高 ML 研究可靠性的社区级尝试。([arXiv][13])

如果你未来做 Dataset Evaluation 或自动化科研审查，这一层非常关键。

---

# 4. 我会如何提出这类问题？

我会用一个“十问法”。

## 1. 对象问

> 当前领域真正建模的对象是什么？这个对象是不是任务真正需要的对象？

例子：
分类建模 (p(y|x))，但 OOD 需要 (p(x\in \mathcal D_\text{ID}))。

---

## 2. 残差问

> 能不能不直接预测答案，而预测从当前状态到正确状态的修正？

例子：
SFT distillation 不复制答案，而复制 self-correction dynamics。

---

## 3. 支撑域问

> 模型是否知道自己什么时候离开了训练语义支撑域？

例子：
OOD / calibration / trustworthy perception。

---

## 4. 不变量问

> 哪些特征跨环境稳定？哪些只是训练集伪相关？

例子：
causal feature / IRM / domain generalization。

---

## 5. 几何问

> 数据空间有什么对称性、图结构、矩阵结构、流形结构？

例子：
多模态融合不是 concat，而是跨模态几何对齐。

---

## 6. 压缩问

> 当前训练目标压缩掉的信息，是否正是可靠性需要的信息？

例子：
CE 可能压掉类内几何；distillation 可能压掉纠错因果结构。

---

## 7. 轨迹问

> 这个任务是不是被错误地建模成 endpoint prediction？它是否应该是 trajectory modeling？

例子：
Diffusion LLM、reasoning、agent workflow、dataset evolution。

---

## 8. 证据问

> 当前 benchmark 奖励了什么？它有没有奖励 reward hacking？

例子：
Dataset Evaluation / verifier / anti-Goodhart benchmark。

---

## 9. 规模问

> 这个方法能不能随着数据、模型、计算继续变强？还是只在小实验里漂亮？

例子：
Bitter Lesson / scaling law / compute frontier。

---

## 10. 杀死问

> 什么最小实验会证明这个想法是错的？

例子：
如果 latent score 不提升 near-OOD，说明“类流形建模”可能只是漂亮故事。

---

# 5. 给你一个总表：不同研究方法论的“灵魂问题”

| 方法论                 | 灵魂问题              | 适合你的方向                              |
| ------------------- | ----------------- | ----------------------------------- |
| 建模对象迁移              | 我们是不是建模错对象了？      | Diffusion Loss、OOD、Diffusion LLM    |
| Back-to-Basics      | 最朴素的正确定义是什么？      | Diffusion Loss、视觉基础模型               |
| Bitter Lesson       | 什么方法能无限吃 compute？ | Diffusion LLM、RL Training           |
| Data-Centric        | 是不是数据定义错了？        | Dataset Evaluation                  |
| Benchmark 派         | 现在的指标奖励了什么幻觉？     | Dataset Evaluation、SFT Distillation |
| Geometric 派         | 数据有什么不变量和结构？      | 矩阵、树、图、多模态                          |
| Causal 派            | 哪些特征跨环境稳定？        | OOD、多模态、安全感知                        |
| Falsification 派     | 什么实验能杀死我？         | 所有方向                                |
| Empirical Debugging | gain 到底来自哪里？      | 所有实验                                |
| Systems 派           | 真实瓶颈是算力还是算法？      | Diffusion LLM、RL Training           |
| Tooling 派           | 为什么别人无法研究这个？      | 自动化科研、Dataset Evaluation            |
| Aesthetic 派         | 这个想法是否少、准、可复述？    | 论文 framing                          |

---

# 6. 对你最重要的结论

你现在最应该训练的不是“多想 idea”，而是训练三种能力：

第一，**识别共同体默认假设**。
比如：分类默认闭集，LLM 默认 AR，distillation 默认模仿答案，benchmark 默认平均分。

第二，**把默认假设改写成可检验建模对象**。
比如：闭集分类 → semantic support modeling；答案模仿 → correction dynamics preservation。

第三，**用最小实验杀死或保留这个对象**。
比如：latent score 是否真的提升 near-OOD；distilled CoT 是否真的保留因果自纠闭环。

所以比“视角转换”更高级的完整形态是：

> **共同体假设识别 → 建模对象迁移 → 研究纲领设计 → 证据制度重写。**

你如果把这套方法稳定下来，后面的多个方向就不会散。它们可以统一成一句话：

> **我研究的是：智能系统如何从表层预测，走向对结构、支撑域、修正动力学和可信证据的建模。**

[1]: https://plato.stanford.edu/entries/fleck/?utm_source=chatgpt.com "Ludwik Fleck - Stanford Encyclopedia of Philosophy"
[2]: https://arxiv.org/abs/1512.03385?utm_source=chatgpt.com "Deep Residual Learning for Image Recognition"
[3]: https://www.incompleteideas.net/IncIdeas/BitterLesson.html?utm_source=chatgpt.com "The Bitter Lesson"
[4]: https://arxiv.org/abs/2001.08361?utm_source=chatgpt.com "Scaling Laws for Neural Language Models"
[5]: https://dcai.csail.mit.edu/2024/data-centric-model-centric/?utm_source=chatgpt.com "Data-Centric AI vs. Model-Centric AI"
[6]: https://neurips.cc/public/guides/PaperChecklist?utm_source=chatgpt.com "NeurIPS Paper Checklist Guidelines"
[7]: https://arxiv.org/abs/2104.13478?utm_source=chatgpt.com "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges"
[8]: https://arxiv.org/abs/1907.02893?utm_source=chatgpt.com "[1907.02893] Invariant Risk Minimization"
[9]: https://plato.stanford.edu/entries/popper/?utm_source=chatgpt.com "Karl Popper - Stanford Encyclopedia of Philosophy"
[10]: https://karpathy.github.io/2019/04/25/recipe/?utm_source=chatgpt.com "A Recipe for Training Neural Networks"
[11]: https://plato.stanford.edu/entries/feyerabend/?utm_source=chatgpt.com "Paul Feyerabend - Stanford Encyclopedia of Philosophy"
[12]: https://plato.stanford.edu/entries/lakatos/?utm_source=chatgpt.com "Imre Lakatos - Stanford Encyclopedia of Philosophy"
[13]: https://arxiv.org/abs/2003.12206?utm_source=chatgpt.com "Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)"
