# Frontier Scouting Report: World-State & Belief-Centric Fusion Problems for Information Fusion / ESWA

**Prepared for:** small academic lab, 2×RTX 4090D 48GB, public-data-only, 4–6h go/no-go pilots
**Date:** July 2026
**Honesty note:** All community anchors below are cited from knowledge available up to early 2026 and from memory; a few titles/venues may be slightly off. Section 6 gives exact search queries so every anchor and every "not crowded" claim can be independently falsified before you commit a single GPU-hour. Treat the crowding assessments as hypotheses to be checked, not facts.

**Unifying thesis of this report.** Your negative history (dominant modalities, LoRA-closable gaps, knowledge-bound residuals, closed-loop belief injection failure) points to one consistent lesson: the surviving research surface is not "better fusion blocks for recognition," it is **calibrated belief over world state under conflicting, asynchronous, or untrusted evidence sources** — where the *metric itself* is about belief quality (calibration, conflict resolution, latency-to-correct-belief), not point accuracy. LoRA and tuned baselines optimize point accuracy; they do not, by construction, produce calibrated evidence-conflict dynamics unless you make that the task. Every candidate below is built on this asymmetry.

---

## Section 1 — Candidate Directions (11)

---

### C1. Occlusion-Persistent World-State Belief in Video Foundation Models

**1. Title.** Calibrated belief persistence: do video models maintain, decay, and recover object-state beliefs through occlusion — and can a recursive fusion head fix it?

**2. Reviewer eyebrow.** Video-LMs answer "where is X now?" from the last frame in which X was visible; they have grounding but no *persistence*, and no benchmark currently measures whether a model's uncertainty correctly widens during occlusion and snaps back on reappearance — the defining behavior of a world model versus a recognizer.

**3. Community evidence.**
- OpenEQA (Meta, CVPR 2024): explicitly shows the largest model–human gap on *episodic memory* questions, i.e., state that must be remembered rather than seen.
- CATER (2019) and CLEVRER (2020): long-standing containment/occlusion probes that mainline video architectures still treat as classification, not state estimation.
- V-JEPA 2 (Meta, 2025) and the broader JEPA program: predictive latent world-state as the stated goal, but public evaluations remain point-accuracy, not belief-calibration.
- Fei-Fei Li / World Labs "spatial intelligence" essays (2024–2025): world models framed as maintaining state of unseen parts of a scene.
- A cluster of 2024–2025 arXiv probing papers on object permanence / "out of sight, out of mind" failures in VLMs (verify via Q1 in Section 6).

**4. Under-solved.** There is no *metric* for belief-persistence calibration (uncertainty should grow monotonically with occlusion duration and collapse on re-observation), no benchmark split organized by occlusion horizon, and no standard formulation of "recursive evidence fusion over frozen video features" — i.e., a learned filter that treats each frame as an asynchronous, visibility-gated measurement.

**5. Why not crowded.** CVPR mainline optimizes tracking accuracy (SOT/MOT) or QA accuracy; the tracking community has occlusion handling but no calibration story and no connection to foundation-model features; the VLM-probing papers diagnose but do not build the state-estimation layer. The intersection (recursive Bayesian/evidential filtering *on frozen foundation features*, evaluated on calibration dynamics) is nearly empty.

**6. Why LoRA / tuned baselines won't close it.** LoRA on a video-LM improves point predictions but has no mechanism to produce time-consistent posterior dynamics; a tuned LSTM-over-frames baseline is exactly the thing your experiment is designed to beat *on NLL/ECE as a function of occlusion length*, which is a different axis than accuracy. If the LSTM matches calibrated behavior, the kill criterion fires cheaply.

**7. Venue fit.** Information Fusion: this is literally temporal fusion of asynchronous, reliability-varying evidence with an explicit filtering formulation. ESWA: an occlusion-robust state-tracking wrapper is a deployable component for surveillance/retail/warehouse monitoring.

**8. Data & baselines.** CATER (public, small), CLEVRER, MOVi/Kubric (generate controlled occlusion horizons locally), OpenEQA-EM as an eval-only transfer probe; baselines: last-visible-frame regressor, LSTM/transformer over frozen features, a fine-tuned VideoMAE head, off-the-shelf tracker (e.g., a SAM-2-style tracker) as a strong non-belief baseline.

**9. 4–6h pilot (2×4090D).**
- Data: CATER snitch-localization split (~5.5k train videos; use 2k), plus 500 Kubric clips with scripted occlusion horizons of 0/10/30/60 frames.
- Features: frozen DINOv2-B per-frame (precompute in ~1h on 2 GPUs).
- Models: (a) last-frame head; (b) 2-layer LSTM; (c) recursive Gaussian belief head (learned process noise, visibility-gated measurement update). Each trains in <30 min.
- Metrics: localization accuracy, NLL, and ECE *stratified by occlusion length*; monotonicity of predictive variance during occlusion.
- Green: (c) beats (b) on long-occlusion NLL by ≥20% relative and shows monotone variance growth; accuracy no worse.
- Kill: (b) achieves calibrated behavior too, or all methods saturate CATER (task too easy → escalate to Kubric-hard or kill).

**10. Minimum publishable claim.** ESWA: a plug-in belief-tracking layer over frozen video features that improves occluded-object localization and yields actionable confidence, demonstrated on CATER + Kubric + a real-video transfer (e.g., LaSOT occlusion subset). Information Fusion: a general recursive-evidential formulation + a new *persistence-calibration* metric, validated across ≥3 datasets, with theory-flavored analysis of visibility-gated evidence weighting.

**11. Red flags.** Data: synthetic-to-real gap (mitigate with LaSOT/GOT-10k occlusion subsets). SOTA reproduction: trackers like SAM-2 are strong point-estimators — you must show they are *uncalibrated under occlusion*, which is plausible but must be measured. Engineering: low. Knowledge-bound: low (nothing to know, only to remember). LoRA-closes-it: medium-low — calibration dynamics are the moat; if a tuned transformer is well-calibrated per occlusion-horizon, kill.

**12. Method family (after problem is established).** Visibility-gated learned Kalman/particle heads over frozen features; evidential (NIG) measurement models; occlusion-horizon curriculum; re-observation "snap" consistency loss.

---

### C2. Fusion with an Untrusted Prior: Map-versus-Reality Belief (FRONT-RUNNER)

**1. Title.** When the map lies: calibrated, temporally-accumulated belief over prior-map validity from onboard sensing.

**2. Reviewer eyebrow.** Every deployed AV/geospatial/robotics stack fuses live sensing with a *stale prior map*, yet the fusion literature almost universally treats the map as ground truth; deciding *where and when to stop trusting the prior* is a textbook conflicting-evidence problem with a public, underused benchmark (Argo's "Trust, but Verify") and enormous industrial pull (HD-map maintenance is a known cost center).

**3. Community evidence.**
- TbV — "Trust, but Verify: Cross-Modality Fusion for HD Map Change Detection" (NeurIPS 2021 Datasets & Benchmarks; Argoverse ecosystem): real vehicle logs with labeled map changes; strikingly thin follow-up literature relative to its industrial relevance (verify with Q1–Q2).
- The entire online-HD-map-construction wave (MapTR, MapTRv2, StreamMapNet, 2023–2025) is *motivated in its intros* by map staleness — the community acknowledges the problem, then routes around it by discarding the prior instead of fusing with it.
- 2024–2025 arXiv work on prior-map-conditioned online mapping (e.g., using SD/HD priors as an extra input) shows the pendulum swinging back to "use the prior, but how much?"
- Crowdsourced map-update / change-detection literature in ITS journals; OSM-vs-imagery change detection in geospatial venues.
- CVPR Workshop on Autonomous Driving (2024–2025) challenge tracks around mapping and long-tail perception.
- Industry pain: HD-map maintenance costs are a stated reason companies moved "map-lite" (blogs/talks from AV companies, 2023–2025).

**4. Under-solved.** TbV baselines are *single-snapshot binary classifiers* ("does this frame disagree with the map?"). Missing: (i) a per-map-element **validity belief** accumulated across frames and drives (recursive log-odds / evidential mass with explicit conflict term); (ii) calibration of that belief; (iii) latency-style metrics — *frames-to-confident-detection* and false-alarm rate under long unchanged stretches; (iv) a formulation of "prior as an untrusted modality with a staleness prior." Nobody has posed map verification as sequential evidence fusion with guarantees.

**5. Why not crowded.** Mainline CVPR went map-free (online construction) — that's the saturated direction. Map *maintenance/verification* sits between the AV perception community (which finds it unglamorous) and the geospatial community (which lacks the onboard-sensor data), so it fell into a gap. TbV citations are modest and mostly "related work" mentions (verify with Q2).

**6. Why LoRA / dominant modality won't close it.** The task is intrinsically two-source: neither the camera stream nor the map alone defines "change" — change *is* the disagreement between them, so no dominant modality exists by construction. A tuned single-frame fusion classifier is the strong baseline; your claim lives on the temporal-accumulation and calibration axes (frames-to-detection at fixed false-alarm rate), which single-frame LoRA cannot express.

**7. Venue fit.** Information Fusion: conflicting-evidence fusion between a prior knowledge source and a sensor stream is the journal's founding topic (Dempster–Shafer conflict, evidential updating), here modernized with foundation features and a real benchmark. ESWA: a deployable map-health monitor with calibrated trust scores and detection-latency curves is a clean applied-systems paper.

**8. Data & baselines.** TbV (public via Argoverse; per-log download, use a subset), Argoverse 2 maps; secondary/transfer: nuScenes + synthetically edited OSM/HD map elements (controlled perturbations: deleted crosswalks, moved lane boundaries) to get cheap, label-perfect evaluation. Baselines: TbV paper's fusion classifiers; single-frame CLIP/DINOv2 + map-raster head; frame-wise score averaging (naive temporal baseline).

**9. 4–6h pilot (2×4090D).**
- Data: 60–100 TbV logs balanced changed/unchanged (keep download <100 GB by taking ring-front-center camera only); rasterize local map crops around ego pose.
- Hour 1–2: precompute frozen DINOv2-B features for image crops and a lightweight CNN embedding for map rasters.
- Hour 2–4: train (a) single-frame fusion MLP (the tuned baseline), (b) same per-frame evidence fed into a recursive log-odds accumulator with learned observation reliability (viewpoint distance/angle gating).
- Hour 4–6: evaluate AUROC/AP at log level, ECE of the accumulated belief, and frames-to-detection @ 1% false-alarm.
- Green: (b) improves log-level AP by ≥5 pts over (a)'s best per-frame aggregation AND cuts frames-to-detection ≥30% at matched FA, with ECE < single-frame.
- Kill: single-frame classifier saturates (changes are visually obvious in one glance) — the problem would then be perception-bound, not fusion-bound. This is exactly the cheap falsification you want.

**10. Minimum publishable claim.** ESWA: an end-to-end map-verification module on TbV with calibrated per-element trust, detection-latency analysis, and an ablation showing temporal evidential accumulation beats tuned single-frame fusion — framed as a map-maintenance decision-support system. Information Fusion: the general formulation "sequential fusion with an untrusted prior," an explicit conflict/staleness-aware evidential update rule, results on TbV **plus** the controlled nuScenes+edited-map suite (cross-dataset), and an analysis of when Bayesian log-odds vs Dempster–Shafer conflict mass diverge in practice.

**11. Red flags.** Data: TbV full download is large — verify per-log/per-camera subsetting works before committing (Q1/Q2 + repo inspection); label granularity (log-level vs element-level) constrains claims. SOTA reproduction: light — TbV baselines are simple. Engineering: map rasterization + pose alignment plumbing (a day, not a week). Knowledge-bound risk: low. LoRA-closes-it: the pilot's kill criterion tests precisely this; also mitigated because temporal-latency metrics are outside single-frame model class.

**12. Method family.** Per-element evidential belief (Beta/Dirichlet or DS mass with explicit conflict), staleness prior on the map, viewpoint-geometry-weighted measurement reliability, cross-drive accumulation, optional conformal false-alarm control for the ESWA framing.

---

### C3. Stale-State Belief in GUI/Mobile Agents: Action-Conditioned State Verification

**1. Title.** Did the click work? Calibrated post-action world-state belief for GUI agents from fused screenshot + UI-tree + action-history evidence.

**2. Reviewer eyebrow.** Error analyses of web/OS agents keep finding the same failure — the agent acts on a *stale belief* about page state (unloaded page, toggle that didn't flip, dialog it didn't notice) — yet no benchmark measures action-conditioned state-belief accuracy or calibration, only end-task success.

**3. Community evidence.**
- WebArena / OSWorld error analyses (2023–2025) repeatedly attribute large failure shares to state-tracking/grounding rather than planning.
- AndroidControl (Google, 2024), GUI-Odyssey, Mind2Web: large public trajectory corpora with (state, action, next-state) structure — ideal offline probing material.
- 2024–2025 "agent reflection/verification" line (self-check, critic models) — verification exists but as prompt-level heuristics, not as a calibrated fused state estimator.
- NeurIPS/ICLR 2024–2025 workshops on agent safety/reliability calling for failure detection and monitoring.

**4. Under-solved.** A benchmark + metric for *post-action state prediction and action-success detection*, and a fusion formulation combining accessibility-tree (symbolic), screenshot (pixels), and action history into a calibrated belief — including detecting *disagreement* between tree and pixels (a real failure source: DOM updated, render lagged, or vice versa).

**5. Why not crowded.** Agent mainline chases end-to-end success rate with bigger models; monitoring/verification is treated as prompting. The diagnostic, offline, calibration-first framing is cheap and unfashionable at A-conferences — good sign for a journal problem.

**6. LoRA / dominant-modality risk.** Real risk that the UI tree alone dominates (text-dominant trap from your history). The pilot is explicitly designed to test this first: if tree-only ≥ fused on success-detection AUROC, kill immediately. The surviving claim, if any, lives where tree and pixels *disagree* — which no single modality can arbitrate.

**7. Venue fit.** Information Fusion: symbolic+pixel+temporal evidence fusion with conflict detection. ESWA: an agent-reliability monitor is an extremely on-brand applied system.

**8. Data & baselines.** AndroidControl, Mind2Web, GUI-Odyssey, OSWorld traces (all public). Baselines: tree-only classifier, screenshot-only (frozen SigLIP/DINOv2), naive concat fusion, prompted VLM verifier (GPT-style judge if API-free alternatives exist locally — use Qwen-VL class models).

**9. 4–6h pilot.**
- Data: 10k (s, a, s′) triples from AndroidControl; auto-label "action succeeded / state changed as expected" from trajectory metadata + heuristics; hand-verify 200.
- Models: three linear/MLP probes on frozen features (tree text via a small LM encoder; screenshot via SigLIP; fused) + a small temporal variant using the previous k states.
- Metrics: success-detection AUROC, ECE; stratified performance on tree-pixel-disagreement cases (mine these by rendering-lag heuristics).
- Green: fused beats best single modality by ≥5 AUROC on the disagreement stratum, calibrated.
- Kill: tree-only wins overall and on disagreement stratum.

**10. Claims.** ESWA: a calibrated action-verification monitor that flags agent failures before they compound, evaluated across 2–3 agent corpora with an end-task-success correlation analysis. Information Fusion: formulation of symbolic/pixel evidence conflict in agentic state estimation + a public disagreement-stratified benchmark split.

**11. Red flags.** Data: auto-labeling success is noisy (budget hand-verification). Text-dominance: the central risk — pilot kills it in hour 4. Knowledge-bound: low. LoRA: a fine-tuned VLM verifier may be strong — include a small tuned baseline before claiming. Engineering: low-moderate.

**12. Method family.** Conflict-aware late fusion with evidential weights; temporal consistency filter over state beliefs; disagreement-triggered escalation policy (fits ESWA decision-support framing).

---

### C4. Informative Missingness: Staleness-Aware SAR–Optical State Fusion

**1. Title.** When the cloud is the signal: asynchronous SAR–optical fusion for surface-state estimation under *endogenous* sensor availability.

**2. Reviewer eyebrow.** In flood/crop monitoring, optical imagery goes missing *because of* the weather events being monitored — missingness is correlated with the target state — yet essentially all multimodal EO fusion treats gaps as missing-at-random and reports accuracy on cloud-free test sets.

**3. Community evidence.**
- Sen1Floods11, PASTIS-R, DynamicEarthNet: public SAR+optical datasets with real acquisition irregularity.
- 2023–2025 satellite-image-time-series (SITS) literature on irregular sampling (temporal encodings, attention over acquisition times) — handles irregularity, ignores informativeness of the gap.
- GEO-Bench and EO-foundation-model wave (Prithvi, Clay, 2024–2025) creating strong frozen features that make small-lab pilots feasible.
- Operational-flood-mapping pain points (Copernicus EMS discussions): latency and cloud gaps dominate real error, not architecture.

**4. Under-solved.** A formulation where each source carries an explicit *staleness variable* and where the availability pattern itself enters the fusion as evidence (missing-not-at-random); metrics that stratify by optical staleness at decision time; latency-aware evaluation ("state estimate quality t hours after event onset").

**5. Why not crowded.** RS fusion papers are abundant (your banned category), but they are *classification under clean pairing*. The endogenous-missingness + decision-latency framing is a different problem statement; it is standard in biostatistics (MNAR) and nearly absent in EO fusion (verify with Q6).

**6. LoRA / dominant modality.** SAR is near-sufficient for water extent — that's the dominant-modality risk. The claim must therefore be about *calibration and staleness-conditioned improvement* (when/where does stale optical still help, and does the model know?), not raw IoU. If SAR-only matches everywhere including calibration, kill.

**7. Venue fit.** Information Fusion: multi-rate asynchronous fusion with MNAR evidence is squarely in scope. ESWA: an operational flood/crop decision-support system with latency curves.

**8. Data & baselines.** Sen1Floods11 (small, public), PASTIS-R; frozen Prithvi/Clay or ResNet features; baselines: SAR-only U-Net head, naive last-available-optical concat, temporal-encoding SITS baseline.

**9. Pilot.** Sen1Floods11 hand-labeled split (~4.4k chips): train SAR-only vs SAR+stale-optical (inject controlled staleness by shifting optical acquisition offsets) with a staleness-encoding head; metrics: IoU + ECE stratified by staleness; green: staleness-aware fusion beats naive concat at high staleness and degrades gracefully to SAR-only; kill: SAR-only matches everything.

**10. Claims.** ESWA: latency-aware flood-mapping system with staleness-calibrated confidence. IF: MNAR-aware fusion formulation + staleness-stratified benchmark protocol on two datasets.

**11. Red flags.** Dominant modality (SAR) is the big one — pilot tests it first. Data: small and public, low risk. Crowding: must be positioned very carefully against the RS-fusion pile; the intro must open with the MNAR/latency formulation, not the architecture. LoRA: moderate risk.

**12. Method family.** Staleness-conditioned evidence weighting; availability-pattern encoder as an additional evidence channel; evidential segmentation heads.

---

### C5. Self-Diagnosing Sensor Trust on Frozen 3D Detection Stacks

**1. Title.** Post-hoc, calibrated per-sensor reliability estimation for pretrained camera–LiDAR fusion under corruption — with risk–coverage guarantees.

**2. Reviewer eyebrow.** Three years of "robust BEV fusion" papers make detectors *survive* sensor corruption, but none make the system *say which sensor is failing and how much to trust the output* — which is what a safety case or an operator actually needs; and doing it post-hoc on frozen checkpoints is what deployment allows.

**3. Community evidence.**
- nuScenes-C / Robo3D corruption benchmarks (2023) and the robust-fusion line (BEVFusion robustness studies, MetaBEV, 2023–2024).
- Conformal prediction and risk-control wave in trustworthy ML (2023–2026), barely touched in multi-sensor 3D perception.
- Classic sensor-fault-diagnosis literature in Information Fusion itself — the journal's readership expects exactly this question posed for modern stacks.
- Safety-case / operational-design-domain discussions in AV standards communities (UL 4600-adjacent talks).

**4. Under-solved.** A post-hoc "diagnosis head" trained on internal features of a *frozen* detector that outputs (i) corruption type/severity per sensor, (ii) calibrated confidence in detections, with (iii) distribution-free risk–coverage guarantees. Robust-fusion papers retrain the whole stack; nobody offers the cheap monitoring layer.

**5. Why not crowded.** The crowded axis is "new robust architecture, +2 NDS under corruption." The uncrowded axis is "no retraining, diagnosis + guarantees." Different claim type, different metrics (attribution AUROC, risk–coverage AUC), journal-friendly.

**6. LoRA / tuned baseline.** A tuned baseline here is "fine-tune the detector on corruptions" — expensive and explicitly out of scope by the deployment constraint (frozen checkpoint), which you state as a *requirement*, not a limitation. Dominant modality: corruption identity is only inferable by cross-sensor disagreement, so fusion is constitutive.

**7. Venue fit.** IF: sensor reliability estimation is core canon. ESWA: a drop-in perception health monitor.

**8. Data & baselines.** nuScenes-mini + nuScenes-C corruption toolkit (public); pretrained BEVFusion/TransFusion checkpoints (mmdetection3d model zoo). Baselines: detection-score entropy, MC-dropout on heads, single-sensor consistency checks.

**9. Pilot.** nuScenes-mini (10 scenes, tiny): inject 6 corruption types × 3 severities; extract frozen BEV features + per-branch features; train a small attribution head; metrics: corruption-type AUROC, severity correlation, risk–coverage curve of detection confidence. Green: attribution AUROC >0.85 and risk–coverage clearly beats entropy baseline. Kill: score entropy already suffices.

**10. Claims.** ESWA: perception health-monitoring system, cross-checkpoint (2 detectors) and cross-corruption generalization. IF: formal per-sensor reliability posterior + conformal risk control on frozen fusion stacks, held-out corruption families.

**11. Red flags.** Engineering: mmdetection3d plumbing is the main cost (checkpoints exist, but environment setup can eat days). Data: nuScenes license (free for research, sign-up). Crowding: must survive a literature check that no 2025 paper already did post-hoc diagnosis (Q7). Knowledge-bound: none. LoRA: excluded by problem constraint — a genuinely nice moat, but reviewers may ask for one retrained baseline anyway.

**12. Method family.** Cross-branch disagreement features → evidential attribution head; split-conformal thresholds per ODD bin.

---

### C6. Verifying Video World Models: Calibrated Fusion of Physical-Consistency Probes

**1. Title.** A verification instrument for generative world models: fusing weak, heterogeneous physical-consistency probes into calibrated physics-violation verdicts.

**2. Reviewer eyebrow.** Industry is shipping video "world models" (Cosmos, Genie-class, V-JEPA-adjacent) with no accepted way to verify physical consistency — FVD is known to be blind to physics — and the natural instrument is not one metric but a *calibrated fusion of many weak probes* (permanence, collision, flow smoothness, depth consistency), which is an information-fusion problem wearing an evaluation costume.

**3. Community evidence.**
- VideoPhy (2024), Physics-IQ (2025), PhysBench-style physical-commonsense evals; WorldModelBench/EWMBench-type world-model evaluation papers (2025).
- NVIDIA Cosmos release materials (2025) explicitly flagging evaluation as open; 1X world-model challenge (2024–2025).
- Long-standing intuitive-physics probes (IntPhys, Physion/Physion++) providing labeled violation data.
- Workshop CFPs on world models at NeurIPS/ICLR 2025 listing evaluation as a named open problem.

**4. Under-solved.** Single metrics correlate poorly with human physics judgments; nobody has posed verdict formation as *calibrated evidence fusion* (per-probe reliability, per-domain weighting, conflict handling), nor released a probe-fusion verifier that transfers across generators.

**5. Why not crowded.** Eval papers publish leaderboards; probe-fusion-with-calibration as the contribution is a different, journal-shaped object. Risk: the space is moving fast — verify with Q8 that no 2026 paper fused probes with calibration claims.

**6. LoRA / dominant modality.** No modality to dominate; the "tuned baseline" is a single end-to-end video classifier trained to detect violations — plausible and must be included; your bet is that probe fusion generalizes across *unseen generators* better than an end-to-end judge (a distribution-shift claim).

**7. Venue fit.** IF: heterogeneous weak-evidence fusion with reliability modeling. ESWA: a QA tool for world-model pipelines (industrial digital-twin verification framing).

**8. Data & baselines.** Physion/Physion++ (labeled physical outcomes), IntPhys (violation pairs), released generations from open video models (check which benchmarks release model outputs — Physics-IQ did); probes: off-the-shelf tracker, monocular depth, RAFT flow, segment persistence. Baselines: FVD-style scores, single best probe, end-to-end violation classifier.

**9. Pilot.** IntPhys violation pairs (or Physion): compute 4 probe scores per clip (~2–3h GPU), fit a calibrated fusion (logistic + reliability weights), test violation-detection AUROC vs best single probe and vs a small trained classifier; hold out one violation category. Green: fusion beats best probe by ≥7 AUROC and holds on the held-out category. Kill: single probe (e.g., tracker persistence) suffices.

**10. Claims.** ESWA: a practical world-model QA verifier with human-correlation study on ≥2 public generation sets. IF: reliability-weighted probe-fusion formulation with cross-generator generalization evidence.

**11. Red flags.** Data: depends on *released generations* — if benchmarks don't release model outputs, generating them locally with small open video models is feasible but eats the budget. Fast-moving field: 6-month scoop risk is the highest in this list. Knowledge-bound: no. LoRA: the end-to-end judge is the real rival — must be beaten on transfer, not in-distribution.

**12. Method family.** Per-probe evidential reliability, domain-conditioned mixture-of-verifiers, conformal violation flags.

---

### C7. Asset-Condition Belief from Repeated Noisy Inspections

**1. Title.** From frames to assets: temporal evidence fusion for infrastructure condition belief and re-inspection scheduling (sewer/bridge CCTV).

**2. Reviewer eyebrow.** Inspection ML classifies single frames, but operators manage *assets* observed repeatedly over years with noisy, viewpoint-varying evidence — the operational object is a condition *belief* plus a decision of when to look again, and no public formulation exists.

**3. Community evidence.** Sewer-ML (ICCV 2021, 1.3M public images) and its follow-ups; CODEBRIM/bridge-defect datasets; digital-twin-for-infrastructure CFPs (civil-engineering + AI workshops, 2024–2025); ESWA/EAAI predictive-maintenance stream.

**4. Under-solved.** Asset-level evidence aggregation across frames/passes with label noise and degradation dynamics; value-of-information for inspection scheduling; calibration at the asset level.

**5. Why not crowded.** Vision venues stop at frame mAP; asset-level sequential-belief formulation lives in a venue gap. Very ESWA-shaped.

**6. LoRA.** Frame-level LoRA improves frame accuracy but the claim is asset-level belief quality and scheduling value — different objective; naive mean-pooling of frame scores is the tuned baseline to beat.

**7. Venue fit.** ESWA: excellent (decision support). IF: moderate (temporal evidence fusion), weaker theory hook.

**8. Data & baselines.** Sewer-ML (frames grouped by video/asset), CODEBRIM. Baselines: mean/max pooling of frame scores, MIL attention pooling.

**9. Pilot.** Sewer-ML subset (50k frames, video-grouped): frozen DINOv2 + frame head; compare pooling vs recursive per-asset evidential update; metrics: video/asset-level F2 + ECE; simulate revisit sequences by temporal subsampling. Green: evidential accumulation beats MIL pooling on asset-level calibrated F2. Kill: max-pooling suffices.

**10. Claims.** ESWA: asset-condition belief system + inspection-scheduling simulation showing cost reduction at fixed risk. IF: needs the sequential formulation + conflict handling to clear the bar.

**11. Red flags.** Data: Sewer-ML lacks true longitudinal revisits of the same asset — revisit simulation weakens the headline claim (main risk). Everything else low-risk, cheap, safe — a good "banker" project rather than a taste-maker.

**12. Method family.** Per-asset Beta/Dirichlet belief with degradation drift prior; VOI-based re-inspection policy.

---

### C8. The Physics Model as an Untrusted Modality: Conflict-Aware Hybrid Prognostics

**1. Title.** When the model and the sensors disagree: evidential fusion of physics-model predictions and data-driven estimates for degradation state, with disagreement as a first-class diagnostic.

**2. Reviewer eyebrow.** Hybrid digital twins fuse a physics model with sensor pipelines, but when they conflict, practice is ad-hoc weighting — even though the *disagreement itself* is the most informative signal (regime shift, model-form error, or sensor fault), and nobody treats model-form uncertainty as a calibrated modality.

**3. Community evidence.** Hybrid/physics-informed PHM surveys (2023–2025); NASA prognostics datasets ecosystem; model-form UQ literature in scientific ML; digital-twin standardization discussions (ISO 23247-adjacent) naming model-reality divergence monitoring; ESWA/RESS publishing hybrid prognostics continuously.

**4. Under-solved.** A principled conflict decomposition: given model prediction + data-driven prediction + raw sensors, attribute disagreement to (a) regime shift, (b) model-form error, (c) sensor fault, with calibrated posteriors — and show it improves RUL/SOH under *distribution shift between cycling regimes*, where static ensembles fail.

**5. Why not crowded.** PHM fusion papers exist in bulk, but almost all are "stack two predictors, weight statically." The conflict-attribution + shift-conditional-calibration formulation is the missing piece (verify Q9).

**6. LoRA / tuned baseline.** The rival is a tuned stacking ensemble — must be included; it cannot attribute conflict or adapt weights per-regime without being handed the formulation, which *is* the contribution. No dominant modality: physics model wins in some regimes, data in others (documented in PHM literature).

**7. Venue fit.** ESWA: extremely strong (applied decision support, industrial). IF: strong (evidential conflict between knowledge-based and data-based sources — classic journal theme).

**8. Data & baselines.** NASA & Oxford Li-ion battery datasets, N-CMAPSS turbofan (all public, tiny); physics side: equivalent-circuit/empirical degradation models (implementable in a day); data side: small GRU/TCN. Baselines: each alone, static ensemble, tuned stacking, Bayesian model averaging.

**9. Pilot (mostly CPU, trivially fits).** Battery SOH: train data-driven predictor on cycling profile A, test on profile B (regime shift); fuse with ECM prediction via (i) static ensemble, (ii) conflict-aware evidential weighting; metrics: SOH MAE + NLL on shifted regime, conflict-attribution sanity on injected sensor faults. Green: evidential fusion beats stacking on shifted-regime NLL ≥20% and attributes injected faults >0.8 AUROC. Kill: stacking matches under shift.

**10. Claims.** ESWA: hybrid prognostics system with conflict diagnosis, two datasets (battery + turbofan). IF: general knowledge-source-vs-data-source conflict formulation with theory (when does BMA fail under model-form error) — needs the second dataset and an ablation grid.

**11. Red flags.** PHM baseline zoo is deep — a hostile reviewer can always name another ensemble; pre-empt with a broad tuned-baseline table (cheap here). Data: pristine. Engineering: low. Knowledge-bound: no. This is the safest ESWA candidate in the list.

**12. Method family.** Evidential predictors on both branches; conflict mass → attribution head; regime-conditioned reliability priors.

---

### C9. Offline, Action-Conditioned Spatial Belief from Logged Embodied Trajectories

**1. Title.** Belief without the simulator: learning and evaluating calibrated goal/pose beliefs from logged navigation trajectories, as the missing substrate your VLN campaign identified.

**2. Reviewer eyebrow.** Your own aerial-VLN finding — belief injection fails when policies were trained to trust perfect hints — is a community-wide issue: nobody trains or even *measures* uncertainty-aware spatial belief, and doing so requires no closed loop: logged trajectories suffice for belief estimation and calibration evaluation.

**3. Community evidence.** VLN-CE/R2R ecosystems with released trajectory rollouts; 2024–2025 "do VLMs build cognitive maps / mental maps" probing papers; OpenEQA; semantic-mapping-with-uncertainty lines in robotics; World Labs / spatial-intelligence discourse.

**4. Under-solved.** Metrics for belief calibration along a trajectory (posterior over goal direction/distance, revisit recognition); fusion of dead-reckoned motion with frozen visual features into a recurrent belief state; an offline benchmark decoupled from policy learning.

**5. Why not crowded.** Embodied mainline is closed-loop success-rate; the offline belief-estimation framing is cheap, diagnostic, and unfashionable — and directly continuous with your prior negative result (great narrative for the paper's motivation).

**6. LoRA / dominant modality.** A tuned GRU over frozen features is the baseline; the claim is calibration under action-conditioning (belief must respond correctly to motion without observation — a filtering property). Dominant-modality risk low: neither vision-only nor odometry-only can localize the goal.

**7. Venue fit.** IF: action-conditioned recursive fusion of proprioceptive and visual evidence. ESWA: moderate (component for inspection robots/AGVs).

**8. Data & baselines.** Released VLN-CE episode rollouts / R2R trajectory dumps (verify redistribution status — MP3D licensing is the friction point, Q10); alternative: fully public Habitat-free datasets (e.g., real-world GoStanford/SCAND-style logs). Baselines: GRU, transformer-over-history, no-motion ablation.

**9. Pilot.** 5k logged trajectories: predict goal-relative direction/distance posterior at each step; compare GRU vs learned-filter head with explicit motion update; metrics: NLL/ECE vs steps-since-last-informative-observation; green: filter shows correct belief transport under motion (NLL gap grows with observation gaps); kill: GRU matches.

**10. Claims.** ESWA: uncertainty-aware localization belief module + downstream re-ranking of a frozen policy's actions (open-loop). IF: action-conditioned evidential filtering formulation + calibration-along-trajectory metrics; ideally two embodiments.

**11. Red flags.** Data licensing (MP3D) is the main risk; closed-loop validation will be demanded by some reviewers — pre-empt by scoping claims to belief quality + open-loop re-ranking. Simulator-adjacency may bother ESWA less than IF.

**12. Method family.** Learned particle/Gaussian belief over goal frame; motion-model process step; visibility-gated updates.

---

### C10. Fusion Under Unknown Temporal Misalignment (Audio-Visual Streams)

**1. Title.** Synchrony is a myth: joint offset-posterior estimation and alignment-uncertainty-aware audio-visual fusion.

**2. Reviewer eyebrow.** Deployed multi-stream systems (CCTV+audio, multi-camera) drift out of sync by unknown, time-varying offsets; fusion methods assume synchrony and their collapse under offset is undocumented — a one-afternoon experiment can establish the failure mode.

**3. Community evidence.** AV event localization datasets (AVE, LLP); AV robustness studies (2023–2025); self-supervised sync (SyncNet lineage) — sync estimation exists but is never *fused as a posterior* into downstream tasks; smart-surveillance ESWA literature.

**4. Under-solved.** Treating the offset as a latent variable with a posterior, propagated into fusion weights; degradation curves vs offset as a standard protocol.

**5–6.** Not crowded (sync and fusion communities don't talk), but novelty ceiling is moderate; dominant-modality risk real on AVE (visual-heavy). Tuned baseline with offset augmentation might close much of the gap — that is the pilot's kill test.

**7. Venue fit.** IF: yes (registration-uncertainty-aware fusion). ESWA: surveillance application.

**8–9. Data & pilot.** AVE (~4k clips): inject offsets (0–2s, drifting); baselines: standard fusion, offset-augmented fusion; method: offset-posterior (correlation-based) → uncertainty-weighted fusion. Metrics: accuracy vs offset curve, area-under-degradation. Green: posterior method beats augmented baseline at large/drifting offsets. Kill: augmentation alone suffices (plausible).

**10–12.** ESWA claim: robust AV surveillance module. IF claim: latent-alignment fusion formulation across 2 tasks. Red flags: augmentation-closes-it is the big one; keep as a cheap side probe, not a lead. Method family: differentiable alignment posterior + reliability-weighted fusion.

---

### C11. Which Sensor Is Lying? Calibrated Anomaly *Attribution* in Industrial Telemetry

**1. Title.** Beyond detection: evidential attribution of anomalies to sensor faults vs process faults in multivariate industrial streams.

**2. Reviewer eyebrow.** Anomaly detectors flag *that* something is wrong; operators must decide *whether the plant or the sensor is broken* — a distinction that determines whether you dispatch maintenance or shut down a line — and public benchmarks (Tennessee Eastman, SKAB) actually contain both fault classes, yet the attribution task is almost never posed with calibration.

**3. Community evidence.** Tennessee Eastman (includes sensor-drift and process-fault classes), SKAB (labeled fault types), MetroPT-3 (UCI, 2023); root-cause-analysis wave in AIOps/industrial AI (2024–2025); evidential deep learning surveys in Information Fusion; conformal anomaly detection line.

**4. Under-solved.** A calibrated posterior over {sensor fault s_i, process fault p_j, normal} from fused per-channel evidence; disagreement-decomposition (a lying sensor contradicts the correlation structure differently than a process shift); benchmark protocol separating the two on public data.

**5. Why not crowded.** Detection is hyper-crowded; attribution with calibration guarantees on public benchmarks is thin (verify Q9). Root-cause papers exist but mostly graph-heuristic, uncalibrated, and evaluated ad hoc.

**6. LoRA / tuned baseline.** Rival is a tuned multiclass classifier over fault types — include it; your moat is (i) zero-shot-to-unseen-fault-type behavior via the evidential formulation and (ii) calibration, which multiclass softmax notoriously lacks under novel faults.

**7. Venue fit.** ESWA: dead center. IF: strong (per-source reliability, conflict decomposition).

**8. Data & baselines.** TEP (public, tiny), SKAB, MetroPT-3; baselines: reconstruction-error AD + heuristics, multiclass classifier, Bayesian networks.

**9. Pilot (CPU-friendly).** TEP: train per-channel predictors (each sensor from the others); at anomaly time, fuse per-channel surprise into attribution posterior; metrics: sensor-vs-process attribution AUROC, ECE, novel-fault-type holdout. Green: attribution AUROC >0.85 with holdout generalization > multiclass baseline. Kill: multiclass classifier wins including on held-out fault types.

**10. Claims.** ESWA: attribution system + operator-decision cost analysis on 3 datasets. IF: disagreement-decomposition theory + evidential attribution with novel-fault calibration.

**11. Red flags.** TEP is old and heavily mined — the *detection* literature is saturated; you must show the *attribution* framing is genuinely unposed (Q9). Everything else: minimal risk, near-zero compute. Second-safest ESWA banker after C8.

**12. Method family.** Per-channel evidential surprise → DS-style mass over fault hypotheses; correlation-graph-informed conflict decomposition.

---

## Section 2 — Scoring Matrix (1–5; for the three "risk" rows, 5 = LOW risk)

| # | Candidate | Taste / surprise | Future relevance | IF fit | ESWA fit | Feasibility 2×4090D | Public data | Safe from tuned baselines | Safe from dominant modality | Safe from knowledge-bound | Pilot clarity | Mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Occlusion-persistent belief | 4 | 5 | 5 | 3 | 5 | 5 | 3 | 5 | 5 | 5 | 4.5 |
| C2 | Map-vs-reality belief | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 4.6 |
| C3 | GUI-agent stale state | 4 | 5 | 3 | 4 | 5 | 5 | 3 | 2 | 4 | 4 | 3.9 |
| C4 | Informative-missingness EO | 4 | 4 | 4 | 4 | 5 | 5 | 3 | 2 | 5 | 4 | 4.0 |
| C5 | Self-diagnosing sensor trust | 4 | 4 | 5 | 4 | 3 | 4 | 4 | 5 | 5 | 4 | 4.2 |
| C6 | World-model verification fusion | 5 | 5 | 4 | 3 | 3 | 3 | 3 | 5 | 4 | 3 | 3.8 |
| C7 | Asset-condition belief | 3 | 3 | 3 | 5 | 5 | 4 | 4 | 4 | 5 | 4 | 4.0 |
| C8 | Physics-model-as-modality | 4 | 4 | 4 | 5 | 5 | 5 | 3 | 4 | 5 | 5 | 4.4 |
| C9 | Offline spatial belief | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 4 | 5 | 4 | 3.8 |
| C10 | Alignment-uncertainty AV | 3 | 3 | 4 | 4 | 5 | 5 | 2 | 3 | 5 | 5 | 3.9 |
| C11 | Anomaly attribution | 4 | 4 | 4 | 5 | 5 | 5 | 3 | 4 | 5 | 5 | 4.4 |

---

## Section 3 — Top-5 Ranking

1. **C2 — Map-versus-reality belief (front-runner).** Highest taste score with a real public benchmark almost nobody exploits, structurally immune to dominant-modality and knowledge-bound failure (the target *is* cross-source disagreement), a 6-hour falsification that answers the single scariest question first, and a natural dual framing (IF theory paper / ESWA systems paper).
2. **C1 — Occlusion-persistent belief.** Cheapest pilot in the list, cleanest connection to the spatial-intelligence zeitgeist, strong IF fit; ranked second only because synthetic-first data makes the ESWA framing weaker and a calibrated tuned transformer is a live threat.
3. **C11 — Anomaly attribution (ESWA banker #1).** Near-zero compute, pristine public data, operator-relevant question the detection literature skipped; taste is solid rather than dazzling — an excellent parallel low-risk track.
4. **C8 — Physics-model-as-modality (ESWA banker #2).** Same virtues as C11 with a stronger IF theory hook (knowledge-source vs data-source conflict); main cost is a deep PHM baseline table.
5. **C5 — Self-diagnosing sensor trust.** Best pure-IF framing after C2; held back by mmdetection3d engineering overhead and license sign-up friction.

**Portfolio recommendation.** Run the C2 pilot first (it is the taste-maker); in parallel, on CPU/one GPU, run the C11 or C8 pilot as the banker. C1 is the designated pivot if C2's kill criterion fires.

- **Front-runner: C2.**
- **Backup A: C1.**  **Backup B: C11** (swap in C8 if your lab prefers a physics flavor).

---

## Section 4 — Front-Runner Mini-Proposal (one page)

**Title.** Trust Decay: Sequential Evidential Fusion with an Untrusted Prior Map for Calibrated Map-Change Belief.

**Thesis.** Deployed perception systems fuse live sensing with a prior map that is silently stale; the field's two existing answers — trust the map (classical localization) or discard it (online map construction) — bracket the actual problem, which is maintaining a *calibrated, per-element, temporally accumulated belief about where the prior is still valid*. We pose map verification as sequential fusion under source conflict, introduce latency-aware metrics (frames-to-confident-detection at fixed false-alarm rate, belief calibration error), and show that an evidential accumulation layer over frozen foundation features beats tuned single-frame fusion on exactly the axes that matter for deployment.

**Hypothesis.** H1: per-frame map–image disagreement evidence is individually weak (single-frame AP plateaus) but temporally accumulable — recursive fusion yields large gains in detection latency and calibration. H2: reliability-weighting evidence by viewpoint geometry (distance/angle to the map element, occlusion) further improves accumulation, and this weighting cannot be recovered by naive score averaging. H3: the resulting belief is transferable — a model fit on TbV detects synthetic map edits on nuScenes without retraining the evidence head.

**Dataset.** TbV (Argoverse map-change benchmark; per-log download, front camera only for the pilot; ~60–100 logs balanced). Secondary: nuScenes-mini with controlled map perturbations (deleted crosswalks, shifted lane boundaries, removed stop lines) — label-perfect, generated locally, gives the cross-dataset leg IF reviewers want.

**Baselines.** TbV paper's single-frame fusion classifiers (reimplemented light); frozen DINOv2 + map-raster MLP (tuned, our strong single-frame baseline); per-frame score mean/max over the log (naive temporal); optional: an off-the-shelf online-mapping model's output diffed against the prior (the "discard the prior" straw that motivates the paper).

**First experiment (the 6-hour go/no-go).** Precompute frozen features for image crops and rasterized map crops around ego pose (2h). Train the single-frame fusion head (1h). Train the recursive log-odds accumulator with learned per-observation reliability on the same evidence (1h). Evaluate log-level AP, ECE of accumulated belief, frames-to-detection @1% FA (1–2h). Go if accumulation beats the best single-frame aggregation by ≥5 AP and ≥30% latency reduction with better ECE. No-go if the tuned single-frame head saturates — which would mean map changes are perception-obvious and the problem is not fusion-bound.

**Expected failure mode.** The honest risk is exactly the no-go: many TbV changes (a repainted crosswalk) may be visible in one good frame. Mitigation baked into the design: stratify results by change subtlety and viewpoint quality; if only the subtle stratum needs accumulation, that stratum *is* the paper's operating regime, and the latency/false-alarm framing still stands (a deployed monitor cannot wait for the one perfect frame).

**Expected contribution.** (1) Problem formulation: fusion with an untrusted prior as sequential evidential updating with explicit conflict and staleness terms. (2) Metrics: latency-aware, calibration-first map-verification protocol. (3) System: a post-hoc, frozen-feature map-health monitor with cross-dataset evidence. (4) Analysis: Bayesian log-odds vs Dempster–Shafer conflict mass under real evidence dependence — a comparison IF's readership specifically values.

**Why this is not benchmark chasing.** The claim is not "+k points on TbV"; it is a new task axis (latency-to-correct-belief, calibrated trust) on which single-frame SOTA is not merely beaten but *structurally unable to compete*, motivated by a documented industrial cost center (map maintenance), with a falsification test that costs one afternoon. If the kill criterion fires, you have spent six hours to learn the problem is perception-bound — which is itself the exact discipline your negative history demands.

---

## Section 5 — Backup Snapshots

**Backup A (C1).** If C2 dies, pivot the same machinery (recursive evidential head over frozen features, visibility-gated updates, calibration-dynamics metrics) onto occlusion persistence — CATER/Kubric pilots run in an afternoon and the "persistence-calibration" metric is a standalone contribution. The two projects share ~70% of code; this is deliberate.

**Backup B (C11).** Independent of the vision stack entirely: anomaly *attribution* (sensor fault vs process fault) on Tennessee Eastman + SKAB + MetroPT-3 with evidential conflict decomposition and novel-fault calibration. Near-zero compute, pristine data, ESWA-native framing, and it exercises the same evidential-fusion toolkit — a publication-probability stabilizer for the lab.

---

## Section 6 — 10 Exact Verification Queries

Run these before committing (Google Scholar / arXiv / GitHub search):

1. `"Trust but Verify" HD map change detection Argoverse` — pull the citing papers; count how many go beyond single-snapshot classification. (Tests C2 crowding.)
2. `arXiv: "map change detection" OR "map validation" autonomous driving 2024..2026` — check for any temporal-belief or evidential formulation.
3. `"prior map" online HD map construction MapTR StreamMapNet staleness` — confirm the mainline discards rather than fuses the prior.
4. `evidential fusion "outdated map" OR "stale map" robot localization belief` — checks the robotics-side gap for C2.
5. `object permanence occlusion probing video language model calibration 2024..2026` — tests whether C1's calibration angle is taken.
6. `satellite image time series "missing not at random" OR "informative missingness" cloud SAR optical fusion` — tests C4's core claim of absence.
7. `post-hoc sensor reliability estimation frozen detector camera LiDAR corruption conformal` — tests C5 crowding.
8. `world model evaluation physical consistency probe fusion calibrated verifier 2025..2026` — tests C6 scoop risk (highest-velocity area; check twice).
9. `Tennessee Eastman sensor fault versus process fault attribution calibrated OR evidential` — tests C11's "attribution is unposed" claim.
10. `GUI agent state tracking "action success" detection screenshot accessibility tree fusion` — tests C3, and specifically whether tree-only solutions already dominate.

Also worth a 20-minute skim: recent tables of contents of *Information Fusion* (search the journal site for "map", "belief", "evidential", "conflict" in 2024–2026 issues) to calibrate which formulation language the editors are currently accepting.
