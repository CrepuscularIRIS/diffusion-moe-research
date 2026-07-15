同意。按你现在的新要求，**水网应封存为 ESWA 保底，不再做主线**。主线应转到“主流视觉/机器人/自动驾驶 + 能吃 GPU + 训练周期可控”的方向。你贴的笔记里也已经把 IF/ESWA 更现代的方向指向 UAV/VLA、goal observability、belief/reliability head、HD-map trust 和 sensor reliability，而不是 CPU 小工程题。

我按“2×4090 48GB、不要长训、已有/易得数据、能 1 天内出 go/no-go”的标准重排如下。

| 优先级 | 数据集 / benchmark                    | 适合做什么                                                         | 推荐模型                                                 | 训练可行性                              | 判断         |
| --- | ---------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------- | ---------------------------------- | ---------- |
| 1   | **TbV / AV2 Map Change**           | prior map trust / map-health monitoring                       | DINOv2/SigLIP + map raster CNN + temporal trust head | 高，先 frozen feature + 小头            | 最该先跑       |
| 2   | **OpenFly**                        | Aerial VLA / keyframe memory reliability                      | openfly-agent-7b + LoRA/reliability head             | 中，eval-first；全量训练不可行               | 最贴 VLA 审美  |
| 3   | **nuScenes-C / Robo3D**            | camera-LiDAR sensor trust / corruption reliability            | BEVFusion / TransFusion / CenterPoint / PointPillars | 中，优先 pretrained + reliability head | 最主流自动驾驶    |
| 4   | **SceneEdited**                    | 2D-guided 3D HD map trust decay                               | DINOv2 + point/map trust MLP                         | 中，数据管线比训练重                         | 高品味 backup |
| 5   | **CATER / TOC-Bench / Physics-IQ** | video world-state / object persistence / physical consistency | DINOv2/VideoMAE + recurrent belief head              | 高，但更像 eval/method probe            | 前沿 backup  |
| 6   | **AerialVLN / TravelUAV**          | UAV VLN baseline / diagnosis                                  | CMA/STMR/AerialVLA-like small LoRA                   | 中低，sim/eval 工程重                    | 暂不首选       |

## 1. 最推荐先跑：TbV / AV2 Map Change

这个方向最符合“自动驾驶可信感知 / 地图信任”。TbV 的任务就是判断 sensor data 和 HD map 是否因为真实世界变化而不一致；官方 user guide 说明它有 1043 个 vehicle logs，平均 54 秒，每个 log 平均 536 个 LiDAR sweeps、7 个相机各约 1073 张图，总共 7.84M images、922GB extracted。([Argoverse][1])

这里不要做完整 HD map update。要做：

**Calibrated Trust Estimation for Prior Maps from Onboard Sensing**

第一阶段模型非常轻：

当前图像：DINOv2 / SigLIP frozen features
地图：局部 HD-map raster / vector element embedding
输出：当前 map element / local tile 是否可信
时间层：recursive log-odds / evidential accumulator
指标：AP、ECE、frames-to-detection @ fixed false alarm

训练量很小。真正耗时是数据读取、pose 对齐、map crop。你本地已有 `/data/tbv_tars` 和 av2-api，这比 OpenFly 全量下载更可控。

最小 6–12 小时 gate：

抽 20–60 个 logs，只用 front camera。
先做 single-frame DINOv2 + map-raster MLP。
再做 temporal score averaging / log-odds accumulator。
如果 temporal trust 在 ECE 和 frames-to-detection 上不超过 single-frame，就杀。
如果 single-frame 已经饱和，也杀，转 sensor reliability。

这个方向的论文味道比水网强很多，因为它是自动驾驶中的 **untrusted prior fusion**：旧地图、当前视觉、LiDAR/pose、时间证据发生冲突时，系统何时停止信地图。

## 2. 最贴 VLA 审美：OpenFly

OpenFly 很适合你“想回到 VLA/UAV”的感觉。它是 aerial VLN 平台和 benchmark，论文说数据集包含 100k trajectories、18 个 scenes，并使用 Unreal Engine、GTA V、Google Earth、3D Gaussian Splatting 等渲染源生成视觉数据。([arXiv][2])

但它的风险也明确：HF 数据集总大小是 **2.97TB**，README 为空，dataset viewer 不可用。([Hugging Face][3]) 所以不能 full train。好消息是有 **openfly-agent-7b** checkpoint，model card 说明它是 vision-language-navigation model，输入 language + image，输出 UAV actions，并且支持 Hugging Face Transformers 直接加载。([Hugging Face][4])

OpenFly 的正确路线不是“训练 SOTA”，而是：

**When Should an Aerial VLA Trust Its Memory? Calibrated Keyframe Reliability for OpenFly Navigation**

OpenFly-Agent 本身是 keyframe-aware。你可以围绕它做可靠性：

当前 observation 是否足够？
历史 keyframe 是否仍可信？
当前视觉和历史 keyframe 冲突时该信谁？
失败是否来自 keyframe selection / memory compression / goal unobservability？
能否用一个小 reliability head 降低盲信历史或盲信当前帧的失败？

最小 gate：

加载 openfly-agent-7b。
拿小样本 episode 做 inference，不训练。
记录 action、keyframe、history、failure type。
训练一个小头预测：当前帧是否 goal-observable / keyframe 是否 relevant / action 是否高风险。
如果 reliability head 的离线预测不能关联 failure，就杀。
如果能关联，再做 LoRA 或 gated inference。

这条比 TbV 更 VLA，但更容易被数据/代码卡住。因此我建议它做 **并行 gate**，不要阻塞 TbV。

## 3. 最主流自动驾驶：nuScenes-C / Robo3D + BEVFusion/TransFusion

如果你想“GPU 主流感”更强，这条最像自动驾驶论文。nuScenes 本身是大规模自动驾驶数据集，包含 1000 个 scenes，每个 20s，6 cameras、5 radars、1 LiDAR，并有 3D boxes 标注。([arXiv][5])

nuScenes-C / KITTI-C / Waymo-C 是 corruption robustness benchmark，论文构造了 27 种 LiDAR/camera corruptions，并发现 motion-level corruption 很危险、LiDAR-camera fusion 比单模态更鲁棒、camera-only 对 image corruption 极脆弱。([arXiv][6]) Robo3D 也直接覆盖 fog、wet ground、snow、motion blur、LiDAR beam missing、crosstalk、incomplete echo、cross-sensor 等真实 corruption。([GitHub][7])

推荐模型：

**PointPillars**：最轻，适合快速训练/调试。
**CenterPoint**：强 LiDAR-only baseline。
**TransFusion**：camera-LiDAR fusion，官方说明 LiDAR-only 训练 20 epochs，fusion 模型从 LiDAR backbone 继续训练 6 epochs，并冻结 LiDAR backbone 省显存。([GitHub][8])
**BEVFusion**：主流强 baseline，MIT repo 说明它支持 3D detection 和 BEV map segmentation，并在 nuScenes 上有强结果。([GitHub][9])
**MMDetection3D**：模型 zoo 提供 PointPillars、CenterPoint、DETR3D、PETR、TPVFormer、BEVFusion 等 nuScenes/KITTI/Waymo baseline。([MMDetection3D][10])

但注意：**不要 full retrain BEVFusion on full nuScenes**。2×4090 能跑，但不适合“时间不够”的状态。正确做法是：

加载 pretrained BEVFusion / TransFusion / CenterPoint。
在 clean + corrupted inputs 上跑 inference。
抽 detector internal features / confidence / cross-modal disagreement。
训练一个很小的 **sensor reliability head**：判断是 camera corrupted、LiDAR corrupted、both corrupted、clean；同时输出 detection risk / abstention set。
指标用 corruption attribution AUROC、risk-coverage、mAP/NDS drop prediction、ECE。

这条主张可以叫：

**Post-hoc Sensor Trust Estimation for Frozen BEV Perception under Camera–LiDAR Corruptions**

它比“再训一个 robust BEV detector”更小实验室友好，也更 IF：融合对象是 camera/LiDAR/BEV detector 的冲突证据与可靠性。

## 4. 高品味 backup：SceneEdited

SceneEdited 是非常贴 HD map trust 的新方向。论文称它是 city-scale 3D HD map updating benchmark，有 800+ up-to-date scenes、73km driving、约 3km² urban area、23,000+ synthesized object changes，并提供 calibrated RGB images、LiDAR scans、change masks 和 toolkit。([arXiv][11])

它比 TbV 更“新”，但也更像已经定义好的 map update benchmark。你不能直接做 “DINOv2 + MLP map update”。要做 trust：

**2D-Guided 3D Map Trust Decay without Full Map Regeneration**

模型：

旧 3D map points / map elements
current image features
2D-3D projection consistency
point-level trust score
calibration / transient occlusion rejection

风险：camera pose / projection / occlusion 处理比 TbV 更容易出 bug。适合作为 TbV 过 gate 后的第二数据集，不适合第一天主线。

## 5. OpenFly 和自动驾驶两条怎么取舍

如果你现在最想要的是 **VLA/UAV 审美**：

先跑 OpenFly。
但只做 eval-first + reliability head，不做 full dataset train。
一旦 checkpoint/eval 卡住，立刻切 TbV。

如果你现在最想要的是 **更主流、更像 IF/自动驾驶可信感知**：

先跑 TbV。
同时准备 nuScenes-C/Robo3D 的 pretrained detector 可靠性实验。
OpenFly 作为 VLA side branch。

我个人建议的实际顺序是：

**Day 1：TbV gate + OpenFly load gate 并行。**

GPU0：OpenFly-agent-7b 加载与小样本 inference。
GPU1：TbV front-camera DINOv2 feature extraction。
CPU：AV2 map crop / pose / log metadata 检查。

**Day 2：二选一推进。**

如果 OpenFly 跑通且 failure log 清楚，做 keyframe reliability。
如果 OpenFly 卡住，主线切 TbV trust accumulator。
如果 TbV single-frame 饱和，切 nuScenes-C / BEVFusion sensor trust。

## 最终推荐

我会把水网放进 rejected/parking lot，然后启动这三个：

1. **TbV / AV2：Prior-map trust decay**
   最推荐，主流、数据本地、训练短、IF 味道强。

2. **OpenFly：Aerial VLA keyframe/memory reliability**
   最贴你原始兴趣，但只做 eval-first，不碰全量训练。

3. **nuScenes-C / Robo3D：post-hoc sensor trust for BEVFusion/TransFusion**
   最像主流自动驾驶可信感知论文，适合 TbV 单帧饱和时接上。

一句话：**不要再做水网主线；现在最合理的是 TbV 主线 + OpenFly gate + nuScenes-C 备线。**

[1]: https://argoverse.github.io/user-guide/datasets/map_change_detection.html "Map Change Detection (TbV) - Argoverse User Guide"
[2]: https://arxiv.org/abs/2502.18041?utm_source=chatgpt.com "OpenFly: A Versatile Toolchain and Large-scale Benchmark for Aerial Vision-Language Navigation"
[3]: https://huggingface.co/datasets/IPEC-COMMUNITY/OpenFly "IPEC-COMMUNITY/OpenFly · Datasets at Hugging Face"
[4]: https://huggingface.co/IPEC-COMMUNITY/openfly-agent-7b "IPEC-COMMUNITY/openfly-agent-7b · Hugging Face"
[5]: https://arxiv.org/abs/1903.11027?utm_source=chatgpt.com "nuScenes: A multimodal dataset for autonomous driving"
[6]: https://arxiv.org/abs/2303.11040?utm_source=chatgpt.com "Benchmarking Robustness of 3D Object Detection to Common Corruptions in Autonomous Driving"
[7]: https://github.com/worldbench/Robo3D "GitHub - worldbench/Robo3D: [ICCV 2023] Robo3D: Towards Robust and Reliable 3D Perception against Corruptions · GitHub"
[8]: https://github.com/XuyangBai/TransFusion/blob/master/configs/nuscenes.md?utm_source=chatgpt.com "TransFusion/configs/nuscenes.md at master"
[9]: https://github.com/mit-han-lab/bevfusion?utm_source=chatgpt.com "mit-han-lab/bevfusion"
[10]: https://mmdetection3d.readthedocs.io/en/latest/model_zoo.html "Model Zoo — MMDetection3D 1.4.0 documentation"
[11]: https://arxiv.org/abs/2511.15153?utm_source=chatgpt.com "SceneEdited: A City-Scale Benchmark for 3D HD Map Updating via Image-Guided Change Detection"
