[![2023 The Mathematics and Computer Science Prize Laureates —— Kaiming HE ...](https://tse1.mm.bing.net/th/id/OIP.GtlLYVYRgt2Hhl3YwYsfpQHaHa?pid=Api)](https://www.futureprize.org/en/laureates/detail/72.html?utm_source=chatgpt.com)

顶会研究者的核心差异通常不在于“更聪明地调参”，而在于他们有一套稳定的科研操作系统：选题时看未来，实验时极端保守，表达时极端聚焦，发布时重视可复现和社区扩散。

先说 Karpathy。公开资料里，他最典型的策略是“从数据和可验证性开始，而不是从模型创意开始”。在《A Recipe for Training Neural Networks》中，他强调神经网络训练不是 plug-and-play，训练会“静默失败”，所以要从数据检查、简单 baseline、固定随机种子、验证初始 loss、overfit 一个 batch、逐步加复杂度、可视化输入和预测动态做起。这个流程的本质是：先建立可信实验管线，再谈 novelty。([Karpathy 博客][1]) 他的 Software 2.0 观点也很关键：深度学习系统的“源代码”很大程度上是数据集和网络架构，训练过程像把数据“编译”为模型，所以顶级研究者会极其重视数据分布、错误样本、评价协议，而不是只盯着模型结构。([Medium][2])

Karpathy 的另一条方法论是“单一核心贡献”。他在 PhD survival guide 里说，一篇论文不应是实验流水账，而应围绕一个 single core contribution 组织，intro、related work、model、experiments 都要服务于这个贡献；他还提到 Fei-Fei Li 组里有顶会截止前两周的内部 deadline，要求至少 5 页 draft 和接近最终的实验，这会暴露叙事和实验逻辑里的漏洞。([Karpathy 博客][3])([Karpathy 博客][3]) 这对学生很重要：论文不是最后几天把实验结果翻译成 LaTeX，而是从项目中期就开始检验“这个故事是否成立”。

再看何恺明。从他的论文和公开演讲看，他的风格是“简单、可扩展、可迁移、可消融”。ResNet 的贡献不是复杂堆模块，而是抓住“更深网络难训练”这个基础瓶颈，用 residual learning 让深层网络更容易优化，并用大量实验证明深度确实带来收益。([arXiv][4]) 后续 Identity Mappings 论文继续把 residual block 拆开，分析 forward/backward 信号传播，并用 ablation 支撑 identity mapping 的重要性。([arXiv][5]) Mask R-CNN 也是类似模式：在 Faster R-CNN 上加一个并行 mask branch，论文强调 conceptually simple、flexible、general、easy to train，并展示它能迁移到实例分割、检测、人体关键点等任务。([arXiv][6]) MAE 同样是两个核心设计：asymmetric encoder-decoder 和高比例随机 mask，使视觉自监督学习变得简单、可扩展、训练高效。([arXiv][7])

何恺明在 NeurIPS 2024 的公开 slides 里把研究类比为“混沌 landscape 上的 SGD”：选题要处理 risk taking、explore vs. exploit、bias/variance tradeoff；研究要寻找 surprise，而不是只做符合预期的增量；真正的 test set 是未来，所以要减少研究本身的 overfitting，关注方法在新数据、新配置、新用例、新上下文下是否仍成立。 这几句话非常像顶级研究者的选题原则：不要只优化当前 leaderboard，要问这个方向在 2–5 年后是否仍有生命力。

如果把这些方法压缩成一个可执行流程，我会这样定义顶会级科研策略：

第一，选题不是问“这个点能不能涨 1%”，而是问四件事：这个问题是否重要；现在是否刚好可做；你的方法是否能压缩成一句清晰贡献；如果数据、模型、算力扩大 10 倍，它是否更有价值。Karpathy 说要避免 purely incremental work；何恺明说 future is the real test set，这两者本质一致。([Karpathy 博客][3])

第二，实验从“可信 baseline”开始。不要一开始就堆新模块。先复现最相关论文的最简单强 baseline，然后确认数据加载、增强、label、loss、metric、eval 全部可信。Karpathy 的建议包括固定 seed、关掉不必要的 fancy trick、验证初始化 loss、训练 input-independent baseline、overfit 几个样本、可视化进入网络前的 tensor。([Karpathy 博客][1]) Meta AI 在 Detectron2 baseline 更新中也强调，没有可复现的 yardstick，就很难快速科学进展；baseline 必须随领域进展持续更新。([AI Meta][8])

第三，做 controlled ablation。每次只改一个变量，并且实验前写下预期结果。MIT 的计算机视觉研究指南也明确说，研究里要慢下来、验证假设、理解系统，实验时一次只改变一件事，才能知道结果意味着什么。([VisionBook][9]) 顶会论文里的 ablation 不是补表格，而是证明“这个方法为什么工作”的证据链。

第四，尽早写论文骨架。一个强组通常不是“实验完再写”，而是很早就写出标题、摘要、第一张图、方法图、主表、ablation 表的空壳。这样可以提前发现：贡献是否单一，baseline 是否公平，实验是否能支撑 claim，故事是否有断层。Karpathy 提到的两周前内部 review，本质就是把外部审稿压力前移。([Karpathy 博客][3])

第五，把研究当作社区过程。Karpathy 说顶会不仅是听 talk，很多未写进论文的知识在 hallway、poster、同行交流里传播；研究不是孤狼式活动，而是高度社会化的系统。([Karpathy 博客][3]) 对学生来说，这意味着要读论文、复现代码、参加 reading group、和同方向的人交流，而不是闭门造车。

一个实用版本的“顶会项目流程”可以是：

第 1–2 周：写 one-page problem memo。包括问题定义、为什么重要、最强 baseline、当前方法瓶颈、你的一句话贡献、可能失败原因。

第 2–4 周：复现 baseline，并建立可信训练/评测管线。要求能 overfit tiny batch，能解释每个 loss curve，能可视化错误样本。

第 4–6 周：做最小创新版本。不要堆复杂模块，只验证核心假设是否带来预期变化。

第 6–8 周：做 ablation 和错误分析。每个实验必须回答一个问题：哪个组件有用，为什么有用，在哪些场景无效。

第 8–10 周：scale up。换更大数据、更大模型、更强 baseline、更严设置，测试是否仍成立。

第 10–12 周：写作、内部审稿、补关键实验、压缩贡献。论文目标不是“我做了很多”，而是“我证明了一个值得相信的新事实”。

最重要的判断标准是这三个问题：你的方法是否比 baseline 更简单或更强；你的实验是否能让怀疑者闭嘴；你的结论是否会成为别人下一篇论文的起点。能同时满足这三点，才接近顶会研究者的策略。

[1]: https://karpathy.github.io/2019/04/25/recipe/ "A Recipe for Training Neural Networks"
[2]: https://karpathy.medium.com/software-2-0-a64152b37c35 "Software 2.0. I sometimes see people refer to neural… | by Andrej Karpathy | Medium"
[3]: https://karpathy.github.io/2016/09/07/phd/ "A Survival Guide to a PhD"
[4]: https://arxiv.org/abs/1512.03385?utm_source=chatgpt.com "Deep Residual Learning for Image Recognition"
[5]: https://arxiv.org/abs/1603.05027?utm_source=chatgpt.com "Identity Mappings in Deep Residual Networks"
[6]: https://arxiv.org/abs/1703.06870?utm_source=chatgpt.com "Mask R-CNN"
[7]: https://arxiv.org/abs/2111.06377 "Masked Autoencoders Are Scalable Vision Learners"
[8]: https://ai.meta.com/blog/advancing-computer-vision-research-with-new-detectron2-mask-r-cnn-baselines/ "New, improved Detectron2 Mask R-CNN baselines"
[9]: https://visionbook.mit.edu/how_to_do_research.html "52  How to Do Research – Foundations of Computer Vision"
