# Water Attribution TODO — REJECTED / PARKED

Purpose: historical backlog for the water/HVAC/ledger portfolio. On 2026-07-08 the user rejected this portfolio as
too niche and too CPU-heavy for the desired 一区/GPU-heavy direction. Keep this file for traceability only; do not
route here automatically.

## Sources And Priority

1. `plan/scouting/frontier_scouting_report_v2.md` is the primary ranking source.
2. `plan/scouting/deep-research-report-2.md` supplies the broader candidate descriptions and ESWA framing.
3. `plan/scouting/frontier_scouting_report.md` is retained for the earlier C2/TbV map-health design, now promoted
   into the active autodrive-trust line.

## Compute Profile

Do not re-rank directions just to use the 2x4090D. The active water/HVAC/ledger thesis is valuable only if it wins on calibrated conflict attribution, not on model size.

CPU-first / GPU optional:

- Water: BattLeDIM, LeakDB, BATADAL, DiTEC, LILA. EPANET/WNTR, residuals, GBDT, calibration, conformal, and light TCN/CNN baselines. GPU may accelerate small neural baselines, but is not the research core.
- HVAC: LBNL FDD. Rule/residual/GBDT/light TCN; GPU optional.
- Building ledger: hierarchical metering or sbsim-style data. Ledger residual + weather/seasonality + GBDT; CPU-first.
- TEP/SKAB/MetroPT, AIS gap attribution, and SoCal-28Bus-style grid probes: mostly tabular/time-series/graph residual work; light GPU at most.

Light-to-medium GPU:

- PHM backup: PINN4SOH/XJTU battery and N-CMAPSS. GPU useful for retraining PINN/CNN/TCN models, but pretrained or small-model paths are available.
- PyScrew and Sewer-ML: GPU helpful for feature extraction or small sequence/vision heads, not a large-training commitment.

GPU-oriented reserve / parking lot:

- HD map: TbV, SceneEdited, ArgoTweak, MapTR, StreamMapNet, Waymo/nuScenes transfer. Vision/BEV/map-raster feature extraction and temporal trust heads are real GPU work and data-plumbing heavy.
- EO/flood: Sen1Floods11, PASTIS-R. SAR/optical segmentation is GPU-native.
- Video occlusion/world-state: CATER, Kubric/MOVi, CLEVRER, Physion/IntPhys. Video belief/filtering is GPU-heavy.
- Robot and smart-home foundation-model tracks: RoboTwin, SmartBench/DomusFM. GPU likely if promoted.

Operational rule is superseded: no active water/HVAC/ledger work unless the user explicitly reopens this backlog.

## Former Main Line: Water

Name: Leak, Lie, or Wrong Prior.

Claim object: calibrated attribution of hydraulic-model vs SCADA disagreement into leak, sensor fault, demand shift, or model mismatch.

Immediate gate:

1. Run the 60-minute occupancy check Q1-Q7 from `frontier_scouting_report_v2.md`.
2. Verify/fetch BattLeDIM and LeakDB first; BATADAL and DiTEC-WDN are second-stage data.
3. Prove plumbing before model work: WNTR/EPANET model load, SCADA alignment, residual computation, controlled sensor-fault injection, window labels.
4. Pilot within 4-6h: tuned GBDT/TCN residual-window baseline vs factor-structured evidential attribution + calibration/belief smoothing.
5. Anti-overfit split discipline: no random-window headline. Seal train/dev/test by time first (2018 -> dev, 2019 -> test), plus held-out fault family, held-out sensor set, and later cross-network/attack transfer (LeakDB/BATADAL). In-domain AUROC is diagnostic only.
6. Primary metrics: held-out-family attribution AUROC, leak-vs-sensor AUROC, ECE/Brier, hours-to-confident-attribution at fixed false-dispatch, abstention/coverage size, and degradation from in-domain to held-out.
7. Kill if gains exist only on injected/random/in-domain splits, if GBDT/TCN matches held-out calibration/latency, if abstention sets are vacuous, or if leak/lie signatures are inseparable at the available sensor density.

Termination / pivot rules:

1. Continue water only while it has an objective transfer gap that a point detector cannot explain. The current reason to continue is specific: synthetic-trained black-box classifiers failed on real BattLeDIM leaks, while physics mass-conservation transferred strongly.
2. Next hard gate: AMR/DMA demand model + conformal abstention. Kill water if this cannot reduce demand-aliasing enough for moderate/mature leaks, or if the abstention set becomes vacuous at useful false-dispatch rates.
3. Kill water if a tuned residual/GBDT/TCN or no-learning residual baseline matches the proposed method on sealed 2019, held-out sensor set, held-out fault family, calibration, and latency. In-domain AUROC or random-window gains do not count.
4. Kill water if occupancy finds an already-published calibrated leak-vs-sensor-vs-demand/model attribution method with abstention/conformal coverage and dispatch-latency evaluation.
5. Region-close only after two independent mechanisms fail for the same root cause. Do not close water just because detection is saturated; detection saturation is already known and is not the contribution.
6. Promote HVAC immediately if water fails these gates. If water passes, run HVAC as cross-domain replication, not as a competing distraction.

Research-first reading packet:

1. BattLeDIM challenge paper and official site: understand L-Town, 2018/2019 split, SCADA sensors, rules, economic scoring, and published result table.
2. BattLeDIM special-collection/SOTA methods, especially LILA: extract the strongest reproducible detection/localization anchor and its reported number.
3. LeakDB paper/repo: understand cross-network benchmark, scoring, and available baseline algorithms.
4. DiTEC-WDN paper/repo: use as large synthetic hydraulic-state substrate only after the BattLeDIM anchor is clear.
5. Review papers: read one broad leak detection/localization review and one recent data-limitation/AI review to map method families and avoid redoing a crowded detector.
6. Occupancy-specific search: look for calibrated leak-vs-sensor-vs-model attribution, abstention, conformal/coverage sets, and sensor/process fault distinction in WDNs.

Starter sources:

- BattLeDIM official: https://battledim.ucy.ac.cy/
- BattLeDIM paper: https://doi.org/10.1061/(ASCE)WR.1943-5452.0001601
- LILA repo/paper pointer: https://github.com/SWN-group-at-TU-Berlin/LILA
- LeakDB repo: https://github.com/KIOS-Research/LeakDB
- DiTEC-WDN paper: https://www.nature.com/articles/s41597-025-06026-0
- Review: Leak detection and localization in water distribution networks: https://www.sciencedirect.com/science/article/pii/S1367578823000160
- Review/data limits: Addressing data limitations in leakage detection of water distribution systems: https://www.sciencedirect.com/science/article/pii/S0043135424013708

ArXiv occupancy packet:

Use these for trend/occupancy checks and SOTA-anchor selection, not as a bulk download list. Default: inspect metadata/abstract first; download PDF only if the paper becomes an anchor, close neighbor, or required 精读 target.

1. Factor Graph Optimization for Leak Localization in Water Distribution Networks: https://arxiv.org/abs/2509.10982
2. Algorithm-Informed Graph Neural Networks for Leakage Detection and Localization in Water Distribution Networks: https://arxiv.org/abs/2408.02797
3. Investigating the Suitability of Concept Drift Detection for Detecting Leakages in Water Distribution Networks: https://arxiv.org/abs/2401.01733
4. Large-Scale Multipurpose Benchmark Datasets For Assessing Data-Driven Deep Learning Approaches For WDNs: https://arxiv.org/abs/2404.15386
5. Leakage Localization in Water Distribution Networks: A Model-Based Approach: https://arxiv.org/abs/2204.00050
6. A Graph Partitioning Algorithm for Leak Detection in Water Distribution Networks: https://arxiv.org/abs/1606.01754
7. Iterative Water Leak Localization with Physical Simulation: https://arxiv.org/pdf/2406.19900
8. A comparison between joint and dual UKF for WDN leak/sensor-fusion context: https://arxiv.org/abs/2510.24228

Minimum reading order:

1. BattLeDIM.
2. LILA.
3. Factor Graph 2025.
4. GNN 2024.
5. Data-limitation review.
6. DiTEC-WDN.

If the arXiv packet already contains leak-vs-sensor-vs-model attribution with calibration/abstention, demote water and promote HVAC.

Go path:

1. Create paper skeleton early.
2. Extend to LeakDB cross-network and BATADAL sensor-lie/attack attribution.
3. Add conformal false-dispatch control and a simple value-of-re-observation policy.
4. Use HVAC as the cross-domain replication only after the water mechanism is real.

## Homologous Backup Queue

### Backup A: HVAC Fault-Source Attribution

Question: sensor drift, equipment fault, or control-sequence fault?

Data: LBNL FDD first; real-building AHU data if needed.

Pilot: single-duct AHU, physics residual features, tuned GBDT/TCN vs evidential per-source surprise fusion. Same metrics family as water: source AUROC, ECE/Brier, severity-monotone confidence, held-out-fault abstention.

Use when: water data plumbing or attribution separability fails, or after water GO as an IF cross-domain replication.

### Backup B: Building Energy Ledger Repair

Question: parent-child meter mismatch means real load shift, bad meter, wrong mapping, timestamp skew, or missing submeter?

Data: smart company building / hierarchical metering datasets from `deep-research-report (2).md`.

Pilot: ledger residual features + weather + rolling seasonality + LightGBM multiclass head + posterior smoothing. Metrics: issue type macro-F1, Brier/ECE, time-to-isolation, parent-child residual closure.

Use when: a lower-risk ESWA path is needed.

### Backup C: HD Map Trust Decay

Question: when should a fleet stop trusting an old map and trigger re-survey?

Data: TbV/AV2 under `/data/tbv_tars/`; SceneEdited or other map-update data only after a specific scope call.

Pilot: frozen DINOv2/map-raster single-frame baseline vs recursive log-odds/evidential trust accumulator. Metrics: log-level AP/AUROC, ECE, frames-to-confident-detection at fixed false alarm.

Use when: the project deliberately wants a spatial/world-state paper and accepts the extra data-plumbing cost. Do not run active TbV training while water/HVAC/ledger gates are live.

### Backup D: Physics-vs-Data Conflict Prognostics

Question: physics model and data model disagree because of regime shift, model-form error, sensor fault, or abnormal degradation?

Data: small public battery / turbofan PHM datasets.

Pilot: physics-only, data-only, tuned stacking/BMA, and conflict-aware evidential weights. Metrics: shifted-regime NLL/MAE, fault-attribution AUROC, conflict-error correlation, calibration.

Use when: water/HVAC are blocked and a low-engineering ESWA banker is needed.

## Parking Lot

Keep these as observation-only unless a future scouting pass promotes them: distribution-grid topology-action verification, AIS gap attribution, SAR-optical MNAR flood fusion, video occlusion persistence calibration, sewer/bridge asset belief, PyScrew process monitoring.
