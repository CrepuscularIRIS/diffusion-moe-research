# AVDN 实验全记录 — 基于 Qwen2.5-VL 的 Aerial VLN 复现与探索

> **Benchmark**: AVDN (Aerial Vision-and-Dialog Navigation), 纯离线卫星俯视图
> **时间**: 2026-07-05 ~ 2026-07-08 (4 天)
> **硬件**: 2 × RTX 4090D (96 GB VRAM), 单次训练 ≤ 4 h
> **基线模型**: Qwen2.5-VL-7B (冻结) + LoRA r16 α32
> **背景**: AerialVLA (AAAI-26) 证明 frozen SigLIP + Qwen2-7B-LoRA 在 AVDN 可达 SR 28.3, 但其关键依赖 — GeoChat 遥感预训练初始化 — **未公开发布** (HuggingFace 上作者无任何公开模型, GitHub issue 无回复)。我们使用 Qwen2.5-VL-7B 作为替代基底, 从零构建整个训练/评估管线, 在此基底上系统性地探索了信息融合方法的可行空间。

---

## Step 0: 环境搭建与方向选定 (2026-07-05)

### 0.1 AVDN Benchmark 特征

AVDN 是唯一纯离线的空中 VLN 基准: 使用 xView 卫星俯视图裁剪, 无需 3D 仿真环境。智能体在对话引导下, 通过仿射裁剪操作导航到目标区域。

- **数据**: val_seen 567 / val_unseen 625 / test_unseen 1329 条对话轨迹
- **指标**: SR (Success Rate, IoU ≥ 0.4) · SPL (加权路径效率) · GP (Goal Progress) · oracle_sr (轨迹中任一步到达过目标)
- **优势**: 全离线 (快速迭代), 标准化 split, 足够 headroom

### 0.2 基底选择理由

AerialVLA 的训练路线需要:
1. GeoChat 遥感预训练初始化 (未发布)
2. LLaVA-OneVision 基底 (16GB+ 下载)
3. 结构化 grid 动作头 + progress token

由于核心权重不可获取, 我们选择 Qwen2.5-VL-7B (本地已有 3B/7B/32B) 作为替代, 构建独立管线。这意味着我们的基线不等价于 AerialVLA 的完整系统, 但可以在同一 benchmark 上进行受控实验。

---

## Step 1: 冻结 VLM 零射诊断 (2026-07-05)

冻结 Qwen2.5-VL-7B 在 AVDN val_unseen 上零射 (460 步 / 70 子轨迹):

| 指标 | 数值 | 参考 |
|---|---|---|
| 7-way 方向精度 | **0.272** | always-forward = 0.498, chance = 0.143 |
| STOP recall | 4 / 121 | 几乎不停 |

**低于 trivial forward baseline**。

**数据驱动的诊断**: AVDN 指令使用绝对罗盘方向 ("head west"), 但裁剪是 heading-normalized 自我中心 (forward = up), VLM 缺少无人机航向来桥接两个坐标系。这是一个纯粹的 **坐标系不匹配 / heading-fusion** 问题。

---

## Step 2: MoA Panel #1 — Heading-Fusion 方向设计 (2026-07-05)

### 2.1 MoA 面板 (3/5 响应: deepseek / gpt5 / mimo)

**问题**: 如何利用 AVDN 中绝对/自我中心坐标系不匹配的 gap？

| 顾问 | 核心建议 | SR 预测 |
|---|---|---|
| **deepseek** (最佳输出) | canonical-rotation kill-test: A(ego+heading) vs C(North-up 标准化) — 最便宜的验证 | SR ~48-50 |
| gpt5 | plain-LoRA + heading 先行 | SR 27-32 |
| mimo | 双帧/转弯执行保留方案 | SR ~25 |

**关键冲突**: plain-LoRA SR 预测差异大 (25 / 27-32 / 48-50) — 没有人测量过 plain-LoRA-VLM 在 AVDN 上的表现。

**Opus 调和决策**: 采纳 deepseek 的 canonical-rotation kill-test (18 分钟推理, 最便宜的验证), 然后全量训练。

### 2.2 Canonical-Rotation Kill-Test 结果

460 步推理, 18 分钟:

| 指令类型 | A (ego + heading) | C (North-up) | 判定 |
|---|---|---|---|
| ABSOLUTE | **0.436** | 0.372 | A > C |
| MIXED | A > C | — | A > C |
| ALL | — | −17.4% vs A | A ≫ C |

**结论**: heading TEXT token 已提取方向信号, 结构化图像标准化不带来额外增益。deepseek 的 kill-test 设计节省了一次完整训练。

**决策**: PRIMARY = plain-LoRA + heading-token capability-delta

---

## Step 3: Harness 构建 + 全量 2-Arm 训练 (2026-07-05)

### 3.1 管线构建

Executor 构建了完整的 AVDN 训练/评估管线:
- `build_records.py`: 构建训练记录 (30,242 recs / 4,472 trajs)
- `train_lora.py`: LoRA 训练 (r16 α32, q/k/v/o, 冻结 base + vision)
- `eval_closed_loop.py`: 闭环评估
- `avdn_common.py`: 动作编解码 (`A <rx> <ry>` / STOP)
- 动作表示: rx, ry ∈ {0..20}, 21-bin 量化

**Oracle rollout 验证** (teacher action): SR 26.67 / SPL 25.23 → eval 几何正确可达。

**Forward-collapse 问题**: 早期 smoke 测试中, 模型 greedy 解码输出 `A 10 20` 每一步 → SR 0。这是 class-imbalance 导致的 greedy-argmax 吸引子, 非 bug。Teacher-forced 模式下模型确实学到了条件策略 (stop_recall 0.44)。

### 3.2 全量 2-Arm 训练结果

30,242 records, 两个 arm 并行训练 (~1.85 h/arm):
- **FULL** (heading): GPU1
- **NONE** (no heading): GPU0

**Teacher-Forced Heading Lever** (val_unseen 1,323 recs):

| 指令类型 | 占比 | move-dir-MAE (FULL / NONE) | stop-recall (FULL / NONE) |
|---|---|---|---|
| ABSOLUTE | 15% | 2.85 / 3.33 = **−0.48** | 0.359 / 0.333 (+0.026) |
| MIXED | 26% | 3.17 / 3.15 (~0) | **0.427 / 0.281 (+0.146)** |
| EGOCENTRIC | 53% | 2.94 / 2.93 NEUTRAL | 0.360 / 0.360 NEUTRAL |

Heading 在 ABSOLUTE 子集提升 move 精度, 在 MIXED 子集提升 STOP recall, 在 EGOCENTRIC 子集中性 — 符合预期。no-heading LoRA 不能吸收 absolute→egocentric 的坐标系转换。

**闭环评估** (n=411, val_unseen):

| arm | SR | SPL |
|---|---:|---:|
| FULL (heading) | 5.84 | 4.4 |
| NONE (no heading) | 6.81 | 6.23 |

两个 arm 均出现 forward-collapse。rep-penalty 1.3 打破坍缩后 SR ~10。

**Eval 验证**: GT-replay (feed exact gt_path_corners) = **SR 100.0 / IoU 1.0 / SPL 87** → harness 正确, 可达上限 100%。

**分析**: heading lever 在 per-step teacher-forced 下真实, 但 move-MAE ~3/20 在 ~6 步 rollout 中误差 compounding, 使得子集增益对闭环 SR 无关紧要。

**产出**: **C1 rollout-metric law** — 子集 per-step 增益不传导到 compounding SR (当基础 move 误差主导时)。

---

## Step 4: Grounding Quality 诊断 (2026-07-05)

### 4.1 动作表示探针

`rep_vs_cap.py`, 291 moves, 在完整 adapter 上:

| 指标 | 数值 |
|---|---|
| pred-GT corr (rx) | 0.374 |
| pred-GT corr (ry) | 0.475 |
| move-dir-MAE | ~3 / 20 bins |

**结论**: corr 0.45 的表示已接近其理论最大提取量。改进解码方式 (回归 vs 离散 token) 不会带来实质提升。**瓶颈在冻结 7B 的 grounding 质量 (corr 0.45)**, 不在行动表示。

### 4.2 两个机制指向同一根因

1. heading-fusion — per-step lever 真实, 但对 compounding SR 无关紧要
2. action-rep decode — corr 0.45 已接近 rep 允许的最大提取量

两个机制在 **同一 grounding-quality 根因** 上失败。

---

## Step 5: 战略转折 — AerialVLA 存在性证明 (2026-07-05)

精读 AerialVLA (AAAI-26) 后发现: **frozen SigLIP + Qwen2-7B-LoRA → AVDN SR 28.3 / 30.9**。我们的 ~8% SR 对应 AerialVLA 的 video-only baseline (5.5 SPL)。

**AerialVLA 的梯子** (§9.3, 逐级 SPL):

```
video-only 5.5 → +OTDA 17.3 [+9.9, 最大增量]
               → +Global-Map 19.5 [+8.1, 在 OTDA 基础上]
               → +STA 26.6 [+7.1]
```

**关键洞察**: 我们处于梯子的最底层 (video-only); 之前的所有尝试 (heading/decode) 都是 sub-baseline 优化。OTDA 是第一级。

**但核心依赖不可得**: AerialVLA 的 SR 28.3 依赖 GeoChat 遥感预训练初始化, 该权重未公开发布。我们无法复现相同的基线强度, 但可以在我们自己的基底上爬梯子。

---

## Step 6: 时间历史 / 记忆表示实验 (2026-07-06)

### 6.1 两种历史表示并行训练

两种表示并行训练 (2 GPU), 各 ~3.4 h:

| 表示 | tf_corr (rx/ry) | oracle_sr | SR | vs base |
|---|---|---:|---:|---|
| **base (单帧)** | 0.374 / 0.475 | 11.19 | 5.84 | — |
| **raw-crop K=3** (最近 3 帧) | 0.548 / 0.718 | **15.82** | 3.41 | oracle +4.6, SR −2.4 |
| **rendered global-map** (BEV 历史图) | — | **15.33** | 5.60 | oracle +4.1, SR −0.2 |

**两种表示复现了相同模式**: teacher-forced grounding 大幅提升 (corr 0.45→0.72, MAE 3→2.3), oracle_sr 11→15, 但闭环 SR 停留在 baseline band (~5-7)。

**CONVERSION GAP** 诊断: oracle_sr 15 − SR 5 = 10 pp gap = exposure-bias + stopping 问题。表示独立地复现了这个 gap, 证明它不是特定表示的问题。

**洞察**: 独立重新推导了 AerialVLA 的梯子顺序 — OTDA 必须是第一级; 输入表示 without OTDA 不能转化为闭环性能提升。

---

## Step 7: MoA Panel #2 — OTDA 设计 (2026-07-06)

### 7.1 MoA 面板 (gemini / gpt5 / opus46 响应; deepseek / mimo 超时)

| 顾问 | 核心建议 | 关键规则 |
|---|---|---|
| gemini | GO OTDA | — |
| gpt5 | GO OTDA | 自有规则: never-touched failures > 60% → DAgger first |
| opus46 | GO OTDA | — |

**共识**: GO OTDA — never-reached-goal 占失败的 ~85%, 远超 gpt5 设定的 60% 门槛。OTDA 通过 STOP 标签同时解决 stopping 问题。

**主要自攻击**: 7B rollout 可能太慢 → 方案: 2-GPU 并行 + ≤1500 episodes

### 7.2 Exposure-Bias 探针

`probe_exposure.py`, map adapter, 150 val episodes:
- model↔expert action-MAE 随 drift 单调增长: low(0-24m) 4.03 → med 7.75 → high(87-738m) 11.08
- 按步数: early(t≤2) 5.49 → late(t≥5) 8.54
- collapse-free reppen 闭环 SR 也持平 (map 4.38 / hist 6.81 / baseline 7.30) → 解码独立的 conversion gap

---

## Step 8: 行动空间修正 — 2-DOF vs 3-DOF Bug 发现 (2026-07-06)

### 8.1 Bug 发现

在 exposure-bias 分析后, 运行了 `probe_action_ceiling.py` (纯几何, 无模型/图像) 检查行动空间上限:

| 行动空间 | 完美教师 oracle_sr |
|---|---:|
| GT teleport (直接走 GT corners) | **97.6** |
| 2-DOF (rx, ry) — 我们的 harness | **29.4** (budget-independent, 上限) |
| 3-DOF (rx, ry, altitude) — 正确的 | **97.1** |

**诊断**: `avdn_common.apply_action` + `encode_action` 默默丢弃了 AVDN 的 altitude/zoom 自由度。2-DOF 完美教师上限仅 29%, 恢复 zoom → 97%。

**修正**: 添加 altitude token 到 codec + teacher labels + eval apply。

### 8.2 3-DOF 修正后重训结果

| 配置 | SR | oracle_sr | SPL |
|---|---:|---:|---:|
| 3-DOF greedy | 4.38 | 18.98 | 2.82 |
| 3-DOF reppen | 7.79 | 18.73 | 3.59 |

vs 2-DOF baseline: SR 基本持平 (+0.5), oracle_sr +3.4。

**anti-no-op 验证**: alt_std 0.148, 24.9% 的 moves 改变 view-edge → zoom DOF 确实在使用。

**分析**: 3-DOF 修正将完美教师 ceiling 从 29 提升到 97, 但模型仅利用了 18.7/97 = 0.19。2-DOF 时模型利用了 15.3/29.4 = 0.53。3-DOF 释放了 ceiling, 但模型的 learning/exposure 成为新的瓶颈。

---

## Step 9: OTDA on 3-DOF (2026-07-06)

### 9.1 数据管线

基于 AerialVLA 的 DAgger 方法, 实施了在线纠正数据增强:

1. 600 训练 episode × 2 GPU 并行 rollout (~11.5 min/shard)
2. 6,918 drift 状态 (2,062 explore, ε=0.3)
3. 纠正标签: 6,918 条 (6,783 move / 135 STOP; 方向分布 60% BACK = 暴露偏差信号)
4. 聚合: 50/50 GT + corrective = 13,836 条 (STOP 12.5%)
5. Warm-start 训练 (从 3-DOF adapter), 1,730 步, 0.90 h

Anti-no-op 验证: 6918/6918 valid 3-DOF; corrective ≠ on-path-GT 在 81.6% 的 matched states。

### 9.2 结果

| 解码 | SR | oracle_sr | SPL |
|---|---:|---:|---:|
| base greedy | 4.38 | 18.98 | 2.82 |
| **OTDA greedy** | **7.30** | **29.44** | 2.14 |
| base reppen | 7.79 | 18.73 | 3.59 |
| **OTDA reppen** | **9.25** | **21.90** | 2.16 |

OTDA 提升了 oracle (greedy +10.5, reppen +3.2) 和 SR (+2.9, +1.5)。**此后所有实验以 3-DOF + OTDA 为工作基线** (greedy oracle_sr 29.44 / SR 7.30)。

---

## Step 10: 推理时 Commit 机制 (2026-07-06)

在 OTDA 之前, 尝试了 3 种推理时 commit 机制来关闭 oracle→SR 的转换差距:

| 机制 | SR | 判定 |
|---|---:|---|
| gated-governor (proximity→gain/zoom damp) | 6.5-7.0 | HURT (vs base 7.5) |
| EMA-smoothed temporal commit | 9.5 | WORSE |
| peak-aware commit | 8.5 | WORSE |
| per-step threshold-stop | 11.5 | 最佳 (trivial) |

**结论**: per-step P(STOP) (AUROC 0.83) 已是近充分因果统计量 — temporal smoothing/damping/peak 无额外提取。gap 是信号质量 + oracle-ceiling 约束。

---

## Step 11: Wall-Fork — MoA Panel #4 (2026-07-07)

在 5 个机制被否定后, 进入关键分叉。

### 11.1 MoA 面板 (gemini / gpt5 / deepseek / qwen)

| 顾问 | Within-envelope oracle-raiser? | 收敛 |
|---|---|---|
| gemini | EXHAUSTED | 贡献 = BOUNDARY result |
| gpt5 | EXHAUSTED → "More Context, Less Reachability" | IF/ESWA venue |
| deepseek | — | — |
| qwen | EXHAUSTED → "Fusion Tax" | IF/ESWA venue |

**共识**: within-envelope oracle-raiser 空间已穷尽; 没有高概率的 non-epicyclic raiser。

**Pro (GPT-5.5 扩展) 的 framing**: "frozen-VLM+LoRA AVDN agents are REPRESENTATION-limited, NOT SUPERVISION-limited"

**Opus 决策**: 转向 accessibility ladder 诊断。

---

## Step 12: Accessibility Ladder — 核心诊断发现 (2026-07-07)

### 12.1 实验设计

val_unseen n=411, 相同基底 (3-DOF + OTDA), 相同 LoRA 配置, **单变量控制**:

- **arm1 (base)**: 无额外注入
- **arm2 (memory IMAGE)**: 因果历史地图作为第 2 张图
- **arm3 (self-state TEXT)**: heading / cumulative-displacement / zoom / footprints (无目标)
- **arm4 (privileged goal TEXT)**: GT bearing + distance + zoom-to-goal (特权上界, 诊断用)

### 12.2 结果

| arm | 注入信号 | 类型 | oracle_sr | SR | SPL |
|---|---|---|---:|---:|---:|
| 1 | 无 (base) | — | 29.44 | 7.30 | 2.14 |
| 2 | 因果历史地图 | IMAGE | 24.57 | 3.65 | 1.34 |
| 3 | 自身状态 (无目标) | TEXT | 28.47 | 7.06 | 3.11 |
| 4 | **GT 目标几何 (特权)** | TEXT | **84.18** | **83.21** | 69.07 |

### 12.3 统计显著性

binomial, n=411:
- arm4 − base: **+54.7 oracle**, CI [49.1, 60.4]; **+75.9 SR**, CI [71.5, 80.3] — 25 个标准误, 确定性极强
- arm3 − base: −1.0 oracle, CI [−7.2, 5.2] **跨 0 = 统计平坦**
- arm2 − base: −4.9 oracle, CI [−10.9, 1.2]

### 12.4 arm4 有效性验证

真实目标趋近轨迹: iou 0.00 → 0.05 → 0.46 → **0.86**, 智能体在 iou 0.86 **自主 STOP** = 干净的导航+停止成功, 非退化伪影。

### 12.5 核心结论

1. **解码器在给定正确度量目标几何时高度胜任** (arm4 ~84, 接近 97 教师天花板)
2. **整个 oracle bottleneck = 冻结视觉无法从 nadir 像素推导度量目标几何**
3. **self-state 平坦** → 不是本体感觉的 gap
4. **图像记忆有害** → 提示可见像素不是有效状态表示
5. **目标文本接近天花板** → 缺失变量精确地是目标几何推导 (感知限制, 不是监督/行动限制)

---

## Step 13: /adversary 独立审查 (2026-07-07)

独立审查者 (cold packet + REFUTE stance, 源码验证):

### 13.1 通过项

- **Check A (Δ-reality)**: +54.7 oracle 真实, 25 SE, 确定性 n=411
- **Check B (baseline-fairness)**: arm4 与 base 使用完全相同的 13,836 条记录, 仅插入 goal-text 行, 相同 LoRA r16α32 — 单变量匹配控制

### 13.2 被降级的声明

1. **过度声明范围**: "REPRESENTATION-LIMITED (general)" → 范围限定为 "goal-geometry-ACCESSIBILITY-limited on Qwen2.5-VL-7B / AVDN / OTDA+LoRA"
2. **停止泄漏**: 特权距离通道 IS 一个 STOP 线索 (`avdn_common.py:352` 在 dist < 5m 时强制 bearing=0) → 但 oracle_sr 按定义与 STOP 无关 → **+55 oracle (reaching) 增益干净**
3. **"ENTIRE"**: arm4 84 < teacher ceiling 97 → 修改为 "~80% of the reaching-headroom"

### 13.3 占位分析

SpatialFly / GeoNav / FlightGPT 等方法论文建立几何模块但不运行特权上界实验。**定量 accessibility 隔离** (特权上界 + 表示形式阶梯 text-UP / image-DOWN / self-state-FLAT) 无人做过。

---

## Step 14: 目标方向转向 METHOD (2026-07-07)

用户重设 /goal: METHOD 是 PRIMARY; accessibility ladder 诊断是 BANKED evidence, 不是最终产出。

**信封放松**: 约束 = local compute (2×4090D, ≤4h), 不再限定冻结 VLM / LoRA / OTDA — 方法可以使用 vision-tower LoRA / partial ViT unfreeze / learned fusion / adapters / privileged-teacher distillation。

---

## Step 15: MoA Panel #3 — 方法蒸馏机制 (2026-07-07)

### 15.1 MoA 面板 (gemini / gpt5 / deepseek / qwen 全部收敛)

**强收敛的机制**: trainable vision-tower LoRA + dialog × vision 融合 → 目标几何回归头 (bearing sin/cos · log-dist · zoom, circular+L1+CE) 作为 DENSE auxiliary

| 顾问 | 最精确 framing | diff-pred | #1 自攻击 |
|---|---|---|---|
| gemini | Task-Aligned Bottleneck Fusion | oracle → 51 | 视野外不可识别 |
| **gpt5** | **privileged-to-deployable bottleneck DISTILLATION** | 37-55 | shortcut learning |
| deepseek | Visual-Grounded Goal Regression | 60-70 (乐观) | dead-reckoning shortcuts |
| qwen | Cross-Modal Metric Grounding | 55 w/ aux | metric gaming |

**一致的 kill-check**: OFFLINE 目标几何回归, 无闭环, 仅训练 vision+fusion+geom-head, 评估 scene-disjoint held-out

**一致的 #1 自攻击**: 目标在视野外时可能 UNIDENTIFIABLE → MANDATORY neg-controls: vision-only (dialog-masked) + shuffled-dialog

---

## Step 16: 目标几何回归探针 — 离线 (2026-07-07)

### 16.1 训练配置

adapter `avdn_lora_adapter_goalpred`: fresh LoRA, LLM-attn + FULL vision tower = 21.5M 可训练 (vision 11.45M); train loss 0.9→0.27, 2h37m。

### 16.2 Held-Out val_unseen 结果

n=2,536, 30 maps, 场景不相交:

| 指标 | overall | near (≤51m) | mid | far (>120m) | 冻结/trivial |
|---|---|---|---|---|---|
| bearing ang err° | **52.8** | 63.9 | 50.2 | **44.4** | frozen 75.7 / random 90 |
| distance corr (MAE m) | **0.514** (56.0) | 0.334 (30.6) | 0.176 (53.3) | 0.21 (84.2) | frozen ~0 / const-mean 65.7 |
| zoom exact / ±1 | **0.534 / 0.835** | 0.541 / 0.905 | 0.524 / 0.837 | 0.537 / 0.763 | majority 0.175 |

**离线结论**: 可训练感知确实安装了真正的目标几何 — distance corr 0.51 + zoom 0.53 (强), bearing 52.8° (中等, 远超 frozen 75.7°)。bearing 在 FAR 最佳 (44.4°, approach regime), NEAR 最差 (63.9°)。

### 16.3 Dialog × Vision 融合验证

masked vision-only control (dialog 替换为 "Navigate to the goal."):

| 分量 | full (dialog) | masked (vision-only) | dialog Δ |
|---|---|---|---|
| bearing° | 52.8 | 72.1 | **dialog 贡献 ~19°** (LOAD-BEARING) |
| distance corr | 0.514 | 0.361 | dialog 有帮助 |
| zoom exact | 0.534 | 0.544 | ~无 = VISION-ONLY (与 LCSP null 一致) |

**结论**: 几何预测器真正融合了 dialog (referent bearing + distance) × vision (zoom/scale)。真正的融合, 不是视觉先验。

---

## Step 17: 标定曲线 — Bearing 误差 → Oracle 传递函数 (2026-07-07)

arm4 adapter + per-step Gaussian bearing noise, n=200:

| bearing σ | realized MAE | oracle_sr | SR | SPL |
|---|---|---|---|---|
| 0 | 0.0 | 88.0 | 87.5 | 72.8 |
| 15 | 12.3 | 93.5 | 92.0 | 56.4 |
| 30 | 24.5 | 96.0 | 94.0 | 47.5 |
| 45 | 36.4 | 94.5 | 92.0 | 36.3 |
| 60 | 48.8 | 89.5 | 80.5 | 24.5 |
| 90 | 72.9 | 64.0 | 45.0 | 12.4 |

**读数**: 闭环 oracle_sr 对无偏 bearing 误差极其鲁棒 — MAE ≤ 49° 时保持 ≥ 89, 仅在 MAE ~73° (冻结基线水平) 时才崩溃。

**注意**: 这条曲线假设**无偏**噪声 (对称高斯)。真实预测器的有偏/结构化误差会更快退化。这一点在后续实验中被验证。

---

## Step 18: 离线预测几何的闭环注入 — 三种方式均低于 base (2026-07-07~08)

### 18.1 Naive Predicted Geometry

per-step goalpred → 注入 arm4 nav policy:

| 指标 | 数值 |
|---|---|
| oracle_sr | **12.17** |
| SR | 7.54 |
| SPL | 6.20 |
| 闭环 bearing MAE | **88.9°** (≈ random) |

vs offline held-out bearing MAE **52.8°**。Step 0 (on-distribution GT start) 预测良好; step 1+ (agent drifts off expert path) 预测退化到 garbage。= **COVARIATE SHIFT / EXPOSURE BIAS** (MoA panel 的 #1 自攻击, 确认)。

### 18.2 MoA Panel: On-Policy Fix

MoA fix-panel (gemini / gpt5 / mimo) 收敛: **on-policy / DAgger the geometry predictor**。gpt5 选择 on-policy over end-to-end (隔离机制, 更便宜)。

一致的 kill-check: offline drifted-state bearing MAE, GO ≤ 45-50°, KILL > 55°。

### 18.3 Drifted-State Geometry 结果

在 OTDA rollout 数据上重训 goalpred:

| 条件 | bearing MAE | dist corr | zoom exact |
|---|---:|---:|---:|
| expert-adapter on drifted states [BEFORE] | 89.5° | 0.316 | 0.109 |
| **drifted-adapter on drifted states [AFTER]** | **64.7°** | 0.381 | 0.124 |
| drifted-adapter on expert states [hard-kill control] | **133.1°** | — | — |

On-policy 训练恢复了部分 grounding (89.5→64.7°), 但**遗忘了 expert 状态** (133.1° > random) = distribution overfit。

### 18.4 Drifted-Only Adapter 闭环

| 指标 | 数值 |
|---|---|
| oracle_sr | **13.63** |
| SR | 2.92 |
| SPL | 1.38 |

低于 base (29.44), 也仅略高于 naive-predgeom (12.17)。

---

## Step 19: 记忆融合实验 — CRAM-RGB (2026-07-07)

### 19.1 Pro (GPT-5.5 扩展) 设计: CRAM-RGB

Pro 深度设计了 CRAM-RGB:
- 将记忆渲染为**第二张 RGB 图**通过外部确定性 Sim(2) 更新 (translation + scale)
- **Qwen 保持冻结**, 仅训练已有 LoRA
- **正确性规则**: CAUSAL memory only — 从模型执行的前缀构建, 不是 expert future / GT pose
- **关键判别器**: C(正确注册) ≫ B(未注册) ≈ D(置换命令), 判定项 = C − D

### 19.2 训练/评估分布不匹配 Bug

首次训练使用 GT expert path 渲染 histmap, 但评估使用 agent 自己的 rolled corners → 分布不匹配。

| 版本 | oracle_sr | SR | gp | 问题 |
|---|---:|---:|---:|---|
| GT-path 训练 (buggy) | 18.25 | 3.65 | −69 | 训练记忆 ≠ 评估记忆 |
| **causal 修正** | **24.57** | 3.65 | −46 | 修复后恢复但仍低于 base |
| base (无记忆) | 29.44 | 7.30 | — | — |

**结论**: 修正后 oracle_sr 从 18.25 恢复到 24.57 (+6.3, 证实分布不匹配是真正的毒害), 但仍 **低于 base** (−4.9)。正确注册的渲染历史图在冻结 VLM + LoRA 上是 net-negative。

### 19.3 LCSP 语言-缩放探针

冻结 Qwen text embedding → 是否预测 teacher zoom bin？

**结果 = NULL**: top-1 ≈ chance, 粗粒度三分 ≈ 0.333, 连续 r = 0.041-0.099。语言不携带泛化的 zoom/scale 信号。

---

## Step 20: MoA Panel #5 — 优雅机制设计 (2026-07-08)

### 20.1 MoA 面板 (gemini / gpt5 / deepseek / qwen 全部独立收敛; mimo / opus46 退化)

**一致的机制 = Latent Allocentric Goal-Belief Token (LABT)**:

- 丢弃 TEXT round-trip
- 添加可学习持久 `[GOAL_BELIEF]` token(s) 到 Qwen 输入序列
- 其 hidden state 融合 (i) 目标在视野内时的 VISUAL 证据 + (ii) 视野外时的 KINEMATIC/action-history 证据 (dead-reckoning)
- 回归到 **ALLOCENTRIC goal position** (固定起始坐标系 (x,y), 对 drift 不变)
- ACTION head 直接读取 LATENT belief token (连续, 不确定性感知, 无序列化)
- 在 ON-POLICY drifted trajectories 上训练

**为什么克服三种失败模式**:
1. 文本往返 → removed (latent)
2. covariate shift → on-policy + belief 平滑坏的单步预测
3. visual-horizon floor → belief PERSISTS 目标出视野 + dead-reckon

**diff-pred**: oracle 29.4 → ~45-60 (gemini 48-55, gpt5 38-47/50+, deepseek >60, qwen 55-65)

---

## Step 21: Pro (GPT-5.5 扩展) 深度设计 — LGBF (2026-07-08)

Pro 设计了完整的 4 组件机制:

### 21.1 测量头 M(o_t, D)

→ (bearing, dist, obs-covariance Σ_obs, zoom, confidence c)

INIT 从最佳 geometry checkpoint, 仅 tune 几何路径 (vision-LoRA + LLM-attn LoRA + uncertainty head)。损失: von-Mises/wrapped-Huber bearing + log-space distance + CE zoom。

### 21.2 解析递归 Belief Filter (LOAD-BEARING)

b_t = (μ ∈ R², Σ, zoom-logits)
- Ego-motion PROPAGATE: μ_{t+1|t} = R(-Δψ)(μ_t - Δp_t) (yaw-fixed → μ_{t+1} = μ_t - Δp_t)
- Kalman UPDATE: 仅在一致时 (NIS/Mahalanobis gate, ω = c · σ(τ - e))
- ZOOM 作为缓慢变化的 remembered latent (ρ-decay) → 修复 zoom-collapse

### 21.3 Latent Soft Goal Tokens \<GB0..3\>

MLP A_ψ over [μ, log‖μ‖, sinθ, cosθ, logΣ.., p_zoom, entropy, ω] → 4 × d_model soft embeddings

= ANTI-text-round-trip (连续几何+不确定性, 无需解析 "-32 deg")

### 21.4 Confidence-Gated RESIDUAL Policy (ANTI-12.2 fix)

logπ = (1-α) logπ₀(base nav) + α · logπ_student, α = clip(exp(-λ trΣ) · c̄, 0, 1)

不确定 belief → small residual → worst case reverts to ~29.4 (base), **NEVER collapses to 12.2**。

### 21.5 训练

DISTILL from 84.2 privileged GT-text teacher:
- L = 1.0 L_act + 0.25 L_belief + 0.10 L_meas + 0.05 L_contrast + 0.2 CE_expert
- Contrastive anti-shortcut: true-belief vs shuffled-belief KL margin

### 21.6 关键负控制 (Pro 设计)

SHUFFLED ego-motion deltas (Δp 来自另一条轨迹) → drifted bearing 应跳回 60-70°, oracle 降到 ~28-33。如果保持高 → 增益是 shortcut, 不是 goal-belief。

---

## Step 22: Dead-Reckon Kill-Check (2026-07-08)

### 22.1 CPU-Only 探针

`dead_reckon_probe.py`, n=588 trajectories / 6,313 drifted steps:

| 变体 | bearing MAE | frac < 50° |
|---|---:|---:|
| A: GT-start dead-reckon | **0.0°** | 100% |
| B-sim: pred-start + pure dead-reckon | **34.1°** | 75.5% |

**Variant A**: ego-motion/frame transport 数学**精确** (0.0° MAE) — 基础验证。

**Variant B**: dead-reckon 将 per-frame 91° → 34° — **打破了 visual-horizon floor**, 确认 MoA 和 Pro 的分析: visual-horizon floor 是 memoryless 估计器的伪影, 不是信息论限制。

### 22.2 单位 Bug 修正事件

`dead_reckon_real.py` 初始实现有 meters↔degrees 不匹配 (belief 用 meters ~145 初始化, ego frame 用 degrees ~0.001), 导致 74° 的假 KILL。

**修正后** (md/M_PER_DEG) smoke n=8: variant B = **18.5°** (93% < 50°)。

### 22.3 修正后全量确认

`dead_reckon_real_fixed.json`, n=200 trajectories / 2,115 drifted steps:

| 变体 | MAE | frac < 50° |
|---|---:|---:|
| raw per-frame prediction | 91.37° | — |
| B: dead-reckon (修正后) | **34.88°** | 76.3% |
| Btd (pred-bearing + true-distance) | **32.03°** | 79.3% |
| C: gated update | **38.95°** | 73.8% |

Btd ≈ B: 预测距离的偏差仅增加 ~3° → 距离预测对 dead-reckon 影响小。

---

## Step 23: Belief-Filtered 闭环结果 (2026-07-08)

### 23.1 结果

`eval_belief_deadreckon.json` (n=411):

| 指标 | 数值 |
|---|---|
| oracle_sr | **9.49** |
| SR | 7.06 |
| SPL | 5.96 |

**低于 base (29.44)**, 也低于 naive-predgeom (12.2) 和 drifted-adapter (13.6)。

### 23.2 三次部署注入总结

| 注入方式 | oracle_sr | SR | SPL |
|---|---:|---:|---:|
| base (无注入) | 29.44 | 7.30 | 2.14 |
| naive predicted geometry | 12.17 | 7.54 | 6.20 |
| drifted-only adapter | 13.63 | 2.92 | 1.38 |
| **dead-reckon belief** | **9.49** | 7.06 | 5.96 |

三次注入均低于 base。

### 23.3 根因分析: BIAS + COMMITMENT

离线 dead-reckon MAE (34.9°) 和标定曲线 (MAE 53° → oracle 85) 都假设**无偏、每步重新测量**的噪声 → 它**平均化**。

实际 belief **承诺**一个有偏的步-0 估计:
- 目标在起始时视野外 → ~53° 的固定方向偏差
- dead-reckon 忠实保持这个偏差
- 智能体**一致地走错方向**, 从不纠正
- 导航策略**信任**注入的目标文本 (因为 arm4 训练时总是正确的)
- 有偏估计使其自信地走错 → 比无目标更差

**核心洞察**:
- **无偏噪声有效** (标定曲线: MAE 53° → oracle 85)
- **有偏承诺有害** (belief 9.49 < base 29.44)
- 离线几何-MAE 和噪声标定是**闭环 oracle 的误导性代理**
- **BIAS + COMMITMENT** 才是真正的杀手

---

## Step 24: Domain 暂停 (2026-07-08)

### 24.1 暂停原因

AerialVLA 的 SR 28.3 依赖 GeoChat 遥感预训练初始化, 该权重未公开发布 (HuggingFace 上作者无任何公开模型, GitHub issue 无回复)。没有这一初始化, 我们的基线 (SR 7-9) 无法达到 AerialVLA 的基线强度, 这使得在当前基底上取得竞争性方法贡献不可行。

### 24.2 干净停止

- 所有 GPU 计算停止, GPUs idle
- AerialVLA base-model 下载暂停 (6.6/16GB, 可恢复)
- 所有 persistent Monitor 停止

### 24.3 恢复条件

- GeoChat 或其他遥感预训练初始化变得可用
- 或选择更低计算成本的 VLA 方向

---

## 总结: 积累的实验资产

### 完整指标汇总

| 实验 | oracle_sr | SR | SPL | 阶段 |
|---|---:|---:|---:|---|
| base 2-DOF greedy | ~11 | 5.84 | 4.4 | Step 3 |
| base 2-DOF reppen | 15.3 | 7.30 | 6.23 | Step 3 |
| base 3-DOF greedy | 18.98 | 4.38 | 2.82 | Step 8 |
| base 3-DOF reppen | 18.73 | 7.79 | 3.59 | Step 8 |
| +OTDA greedy | **29.44** | **7.30** | 2.14 | Step 9 |
| +OTDA reppen | **21.90** | **9.25** | 2.16 | Step 9 |
| CRAM (causal) greedy | 24.57 | 3.65 | 1.34 | Step 19 |
| accessibility arm3 (self-state) | 28.47 | 7.06 | 3.11 | Step 12 |
| accessibility arm4 (privileged goal) | **84.18** | **83.21** | **69.07** | Step 12 |
| goalpred offline bearing | 52.8° MAE | — | — | Step 16 |
| naive predgeom injection | 12.17 | 7.54 | 6.20 | Step 18 |
| drifted-only adapter | 13.63 | 2.92 | 1.38 | Step 18 |
| dead-reckon belief | 9.49 | 7.06 | 5.96 | Step 23 |

### 我们建立的基线系统的价值

1. **完整的 Qwen2.5-VL-7B + LoRA AVDN 管线**: build_records → train_lora → eval_closed_loop, 端到端验证 (GT-replay SR 100%)
2. **3-DOF 行动空间修正**: 将 perfect-teacher ceiling 从 29 提升到 97, 验证了行动空间保真度是基底正确性的前提
3. **OTDA 数据管线**: 600 episodes rollout → 6,918 drift states → corrective labels → 50/50 聚合, 可复用

### 有价值的实验发现

1. **Accessibility Ladder**: 首次精确定量分离了目标几何 (+54.7)、自身状态 (−1.0)、历史记忆 (−4.9) 对空中 VLN 性能的贡献
2. **CONVERSION GAP 复现**: 两种独立的历史表示复现了相同模式 (oracle 提升但 SR 不变), 证明 gap 是表示独立的
3. **Dialog × Vision 融合验证**: masked control 确认真正的跨模态融合 (dialog 贡献 ~19° bearing)
4. **Bias-Commitment Insight**: 离线 MAE 不预测闭环; 无偏噪声有效, 有偏承诺有害
5. **Dead-Reckon 打破 Visual-Horizon Floor**: variant A = 0.0° 证明 transport 数学精确; variant B 将 91° → 34°, 证明 floor 是 memoryless 伪影

### 文件索引

| 类别 | 文件 |
|---|---|
| 主叙事 | `openbuild/aerial/RUNLOG.md` (压缩版) |
| 完整存档 | `openbuild/aerial/RUNLOG.full.2026-07-08.md` |
| 教训 | `openbuild/aerial/LESSONS.md` |
| 创新索引 | `openbuild/aerial/INNOVATIONS.md` |
| 适配器 | `avdn_lora_adapter_{3dof,otda3dof,goalpred,gtgoal_text,selfstate_text,map3dof,map3dof_causal}` |
| 评估结果 | `val_*.json` (各 arm + 各注入方式) |
| Dead-reckon | `dead_reckon_probe_out.json`, `dead_reckon_real_fixed.json` |
| 标定 | `calib_noise/noise_*.json` |
| MoA 面板 | `scratchpad/moa_{method,fix,elegant}/panel_out.txt` |
| Pro 设计 | `probes/avdn_train/PRO_cram_design.md`, RUNLOG.full inline (LGBF) |
| 占位分析 | `atlas/avdn.md`, `probes/avdn_train/PSC_AVDN_occupancy.md` |
