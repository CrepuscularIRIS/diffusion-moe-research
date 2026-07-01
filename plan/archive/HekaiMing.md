[![Kaiming He](https://tse3.mm.bing.net/th/id/OIP.EwFLmVKbutQ-ApHeN8KIVAHaHa?pid=Api)](https://people.csail.mit.edu/kaiming/?utm_source=chatgpt.com)



你记的“git”大概率不是 **Git/GIT**，而是 **JiT = Just image Transformers**。它是何恺明/李天宏 2025–2026 这条“回到生成模型基本原理”路线里的关键论文：不用 VAE/tokenizer，直接在 pixel space 里用大 patch Transformer 做 denoising，并且主张**预测 clean image / x0，而不是预测 noise 或 velocity**。([ar5iv][1])



## 1. 何恺明最近这条生成模型主线



按重要性和与你的 diffusion 研究相关性，我建议这样看：



| 论文                                              |      arXiv | 核心一句话                                                                                   | 你该关注什么                     |

| ----------------------------------------------- | ---------: | --------------------------------------------------------------------------------------- | -------------------------- |

| **Mean Flows for One-step Generative Modeling** | 2505.13447 | 用“平均速度”替代普通 Flow Matching 的“瞬时速度”，从 scratch 训练一跳生成模型                                    | 一步生成的理论核心                  |

| **Improved Mean Flows / iMF**                   | 2512.02012 | 修正 MeanFlow 训练目标和 CFG 机制，提升稳定性与灵活性                                                      | MeanFlow 的更实用版本            |

| **Pixel Mean Flows / pMF**                      | 2601.22158 | 把 MeanFlow 推到 pixel space：网络预测 x0，但 loss 在 velocity/MeanFlow 空间                         | “输出空间”和“loss 空间”分离         |

| **Back to Basics / JiT**                        | 2511.13720 | 让 denoising model 真正 denoise：直接预测 clean data；纯 pixel Transformer，无 VAE、无 tokenizer、无预训练 | 对“训练目标”最有启发                |

| **Generative Modeling via Drifting**            | 2602.04770 | 不在 inference 里迭代，而是在 training 过程中推进 pushforward distribution                            | 另一种一步生成范式                  |

| **ELF: Embedded Language Flows**                | 2605.10938 | 把 language diffusion 从离散 token 迁移到连续 embedding flow，最后一步才离散化                            | 最像你 DiffusionGemma/dLLM 方向 |

| **MAR + DiffLoss**                              | 2406.11838 | AR 图像生成不一定需要 VQ token，可以用 diffusion loss 建模连续 token 概率                                  | 连续 token / language 迁移的桥   |

| **Diffuse and Disperse**                        | 2506.09027 | 给 diffusion/flow 的中间表征加无正样本 contrastive-style regularizer                               | 训练稳定性与表征正则                 |



何恺明主页的 publication list 已经把 2025–2026 的生成模型线排得很清楚：ELF、Drifting、pMF、BiFlow、iMF、JiT、Dispersive Loss、MeanFlow、Noise Conditioning、Fractal Generative Models 等都在这一段。([people.csail.mit.edu][2])



## 2. MeanFlow 到底怎么“一步建模”



普通 diffusion / flow matching 是这样：



训练时学一个 **瞬时速度场** `vθ(x_t, t)`，表示在时间 `t` 的当前位置应该往哪里走。生成时必须从噪声开始，沿着 ODE/SDE 一步一步积分，所以需要很多 NFE。



MeanFlow 的关键替换是：不直接学瞬时速度，而是学两个时间点之间的 **平均速度** `uθ(x_t, r, t)`。直观上：



> 普通 flow：每一小步都问“现在该往哪走？”

> MeanFlow：直接问“从 r 到 t 这一整段平均该怎么走？”



论文把 average velocity 定义成两个时间点之间位移除以时间间隔，并推导出它和瞬时速度之间的 **MeanFlow Identity**。训练时仍然可以用瞬时速度作为 ground-truth 信号，但模型学的是平均速度，因此 inference 时可以直接从噪声一步跳到数据附近。MeanFlow 报告 ImageNet 256×256 上 1-NFE FID 3.43，并且强调不需要预训练、蒸馏或 curriculum。([ar5iv][3])



所以“一步生成”不是把原来的 diffusion sampler 硬压成一步，而是**训练目标本身变了**：从“学局部微分方程”变成“学跨时间区间的平均传输”。



## 3. iMF 和 pMF 为什么重要



**iMF** 发现原始 MeanFlow 有两个实际问题：第一，训练 target 依赖网络自身，容易不稳定；第二，原版 guidance scale 在训练时固定，测试时不够灵活。iMF 把目标改写成一个更标准的 instantaneous-velocity regression，同时让平均速度网络作为重参数化，并把 guidance 变成显式 conditioning variable。它报告 ImageNet 256×256 上 1-NFE FID 1.72，不用 distillation。([ar5iv][4])



**pMF** 更像是 JiT 和 MeanFlow 的合体。它说：网络输出可以是 clean image / x0，让输出落在自然图像 manifold 上；但 loss 不一定直接在 pixel L2 上算，而是在 MeanFlow velocity space 里算。也就是：



> 网络预测空间：on-manifold 的 clean data

> 训练约束空间：MeanFlow/velocity field



这点对你很关键，因为迁移到语言时也可以分开：网络最终输出 token logits / clean embedding，但训练 loss 可以设计在连续 embedding-flow 或 logit-flow 空间。pMF 报告 ImageNet 256×256 FID 2.22、512×512 FID 2.48，目标是 one-step latent-free generation。([arXiv][5])



## 4. JiT：你说的“git”应该是这个



**JiT = Just image Transformers**。核心不是一步生成，而是“让 denoising 真正预测 clean data”。它批评主流 diffusion 往往预测 noise 或 velocity，而不是 clean image；根据 manifold assumption，自然图像在低维 manifold 上，clean image 是 on-manifold，noise/velocity 是 off-manifold，所以高维 pixel space 下预测 x0 反而更合理。JiT 用简单大 patch Transformer，在 ImageNet 256/512 上做 pixel-space diffusion，不用 tokenizer、无预训练、无额外 loss。([ar5iv][1])



这篇对你的迁移启发是：不要默认“diffusion LM 就必须预测 mask/noise/velocity”。可以设计一个 head 直接预测 **clean token distribution / clean embedding / clean logits**，再用一个更合适的 loss 去约束它。



## 5. ELF：最值得你迁移到 DiffusionGemma/dLLM 的论文



ELF 直接做语言。它不是在离散 token 上 mask-denoise，而是把 token 映射到连续 embedding space，在连续空间里做 Flow Matching，最后一步才用 shared-weight network 映射回离散 token。论文明确说，这样可以把图像 diffusion 里的成熟技巧，比如 CFG，更自然地迁移到语言模型中；实验上 ELF 比已有离散/连续 DLM 有更好 generation quality，并且采样步数更少。([ar5iv][6])



对你现在的 DiffusionGemma 方向，ELF 的意义大于 JiT/MeanFlow：

**MeanFlow/JiT 告诉你训练目标怎么改；ELF 告诉你语言域该在哪里做 diffusion：不要死磕离散 token，转到 embedding/simplex/logit 连续空间。**



## 6. 怎么迁移到你的训练路线



我建议不要一上来“把 MeanFlow 直接塞进 DiffusionGemma 离散 token”。MeanFlow 是连续流场方法，直接对 token id 做平均速度没有意义。更合理的迁移路线是三层：



### 第一层：训练目标迁移，最稳



在 frozen DiffusionGemma 上加小 head / adapter，做 **clean prediction audit**：



输入：当前 masked/noisy canvas + timestep

输出：每个位置的 clean token logits 或 clean embedding

loss：正常 CE / embedding regression / logit distillation



这对应 JiT 的思想：不要只预测噪声或 mask recovery，而是直接预测 clean data。你可以比较：



`standard diffusion loss`

vs

`clean-token CE`

vs

`clean-embedding regression + token CE`



如果 clean prediction 明显提升 held-out diffusion loss 或 self-conditioned PLL gap，这就是一个很强的实验信号。



### 第二层：连续 embedding-flow 迁移，最像 ELF



把 token 序列映射到 embedding：



`x_clean = Embedding[token_ids]`



然后加 Gaussian noise 或 interpolation：



`x_t = α(t) x_clean + σ(t) ε`



训练一个小 adapter/head 学：



`vθ(x_t, t, condition)` 或 `x0θ(x_t, t, condition)`



最后用 tied LM head：



`logits = x0θ @ W_embed^T`



这条路线的优点是：你避免了“离散 token 没有速度场”的问题，同时保留语言模型 vocabulary 映射。ELF 官方代码也走这个思路：T5 tokenizer/encoder 预处理，连续 embedding diffusion，最后离散化。([GitHub][7])



### 第三层：MeanFlow / 一步化迁移，最有论文味但风险最高



等第二层跑通后，再把 ordinary flow 改成 MeanFlow/iMF：



普通训练问：



`从 x_t 的瞬时速度 v 是什么？`



MeanFlow 训练问：



`从 r 到 t 的平均更新 u 是什么？`



在语言 embedding 里可以做：



`uθ(z_t, r, t, prompt)`

目标不是 token id，而是 embedding trajectory 的平均速度或由 x0 推导出的 velocity target。



最后采样时尝试：



`z_1 = z_0 + uθ(z_0, 0, 1)`



然后：



`tokens = argmax(z_1 @ W_embed^T)`



这就是“language MeanFlow”的雏形。但要明确：**图像里已经成立，语言里目前还属于研究迁移，不是已有定论**。最近 ELF 仍然使用多步 SDE/ODE sampling，不是一步 MeanFlow；所以你的创新点可以是“在 embedded language diffusion 中验证 MeanFlow/iMF 是否能一步化”。([ar5iv][6])



## 7. 给你一个清晰执行规划



**Phase 0：文献复现优先级**



先读顺序：



1. JiT：理解 x-pred / clean prediction 为什么重要。

2. MeanFlow：理解 average velocity 和 one-step。

3. iMF：理解原版 MeanFlow 的训练坑。

4. pMF：理解“输出 x0、loss 在 velocity space”的分离思想。

5. ELF：迁移到语言 diffusion 的主依据。

6. MAR + DiffLoss：理解连续 token 下怎么用 diffusion loss 替代 categorical CE。([ar5iv][1])



**Phase 1：小实验，不碰大模型生成**



在 frozen DiffusionGemma 上只做 forward-pass audit：



* baseline：原始 diffusion loss

* clean-token head：预测 clean token CE

* clean-embedding head：预测 clean embedding，再投影 vocabulary

* timestep/noise conditioning ablation

* 指标：held-out CE、gold top-k、self-conditioned PLL gap、不同 timestep 分层表现



目标是证明：**clean prediction / embedding-flow 目标比原始 mask denoising 更适合 frozen dLLM 的错误定位。**



**Phase 2：ELF-style adapter**



冻结 backbone，只训练：



* embedding denoising adapter

* timestep/noise/progress conditioning

* tied LM projection

* 可选 CFG/self-conditioning



目标不是立刻超过 DiffusionGemma，而是证明：**连续 embedding denoising 能稳定学习，并且比离散 mask head 更少 joint incoherence。**



**Phase 3：MeanFlow-style 一步化**



在 embedding space 里训练 `uθ(z_t, r, t)`：



* 先做 8-step / 4-step / 2-step / 1-step schedule ablation

* 再比较 ordinary flow vs MeanFlow vs iMF target

* 最后做 generation quality / verifiable tasks



论文问题可以写成：



> Can embedded diffusion language models be trained to learn average transition fields, enabling few-step or one-step language generation without discrete-token masking?



这是比“我把 MeanFlow 套到 token 上”更稳、更像 A 会论文的问题。



## 8. 最后判断



你要抓住何恺明这条线的核心，不是“又一个 diffusion trick”，而是三个思想：



1. **从复杂系统回到简单目标**：JiT 说直接预测 clean data。

2. **从多步积分变成跨时间平均传输**：MeanFlow/iMF 说学 average velocity。

3. **从离散符号转到连续空间再离散化**：ELF/MAR 说语言或图像 token 不一定要 VQ/离散建模。



对你当前 DiffusionGemma 研究，最高价值路线是：

**ELF-style continuous embedding diffusion + JiT/pMF-style clean prediction + iMF-style average transition head。**

不要一开始追求“一步生成 SOTA”，先证明训练目标和错误定位确实更好。



[1]: https://ar5iv.org/abs/2511.13720 "[2511.13720] Back to Basics: Let Denoising Generative Models Denoise"

[2]: https://people.csail.mit.edu/kaiming/publications.html "Kaiming He - Publications"

[3]: https://ar5iv.org/abs/2505.13447 "[2505.13447] Mean Flows for One-step Generative Modeling"

[4]: https://ar5iv.org/abs/2512.02012 "[2512.02012] Improved Mean Flows: On the Challenges of Fastforward Generative Models"

[5]: https://arxiv.org/abs/2601.22158 "[2601.22158] One-step Latent-free Image Generation with Pixel Mean Flows"

[6]: https://ar5iv.org/abs/2605.10938 "[2605.10938] ELF: Embedded Language Flows"

[7]: https://github.com/lillian039/ELF "GitHub - lillian039/ELF · GitHub"