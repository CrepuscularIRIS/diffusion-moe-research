# Frontier Scouting Report v2 — Web-Grounded, Falsification-First
## Belief-repair problems under stale / conflicting / lying evidence, for Information Fusion & ESWA

**Prepared:** July 2026 · **Lab:** 2×RTX 4090D 48GB, public data, 4–6h go/no-go pilots
**Method note.** Unlike the previous pass, every crowding claim here was checked against live 2024–2026 web sources (arXiv, benchmark pages, GitHub, Zenodo, OEDI, journal/CFP pages). The operator bank was used per protocol: retrieval index scanned once; only the 1–3 matched cards opened (factor-graph-ization #6, belief-ization #25; index rows for coverage-set-ization #27 and residual-ization #32). Per your instruction, **any candidate that cannot be falsified in one afternoon is downgraded regardless of elegance** — this demoted two directions that scored high on taste last round.

**Three crowding reversals found by search (things memory got wrong or that moved in 2025–2026):**
1. **Robot action-outcome/failure detection is now saturated**: I-FailSense (arXiv:2509.16072), Guardian (arXiv:2512.01946), SAFE (NeurIPS 2025), VLA-FAIL (arXiv:2606.21386), AHA (aha-vlm.github.io), ViFailback (arXiv:2512.02787). → avoid list.
2. **GUI action-effect verification was just taken**: VeriGUI (arXiv:2604.05477) does exactly "did the click work" with pre/post verification; VisCritic (arXiv:2606.24525) does Siamese pre/post screenshot comparison as a process reward; D-GARA (arXiv:2511.16590) and FineState-Bench (arXiv:2604.27974) cover state-centered validation. → avoid list.
3. **Prior-map-informed HD map update is heating fast**: ExelMap (arXiv:2409.10178), ArgoTweak (arXiv:2509.08764, new dataset with structured priors), RTMap (arXiv:2507.00980), LDMapNet-U (KDD 2025), Mind-the-Map (WACV 2025, arXiv:2311.10517). The *map-generation/update* side is no longer open — but all of these are heavy BEV stacks focused on map quality, and none produces a calibrated, latency-scored, temporally accumulated *trust* signal; TbV itself still has thin direct follow-up (repo last push 2023, github.com/johnwlambert/tbv). → survives only as a repositioned monitoring problem, demoted to backup.

Also confirmed: TOC-Bench (arXiv:2605.09904, 2026) now benchmarks temporal object consistency in Video-LLMs — the pure "persistence benchmark" niche is taken; only the calibration/belief-dynamics angle remains.

---

## Ranked Candidates (top 8)

---

### #1 — FRONT-RUNNER. Is it a leak, a lying sensor, or a wrong model? Calibrated evidence attribution in water distribution networks

**1. Title.** Leak, lie, or wrong prior: calibrated attribution of hydraulic-model–SCADA disagreement in water networks, with detection-latency economics.

**2. Reviewer eyebrow.** The community's own flagship benchmark (BattLeDIM) *deliberately ships a mismatched nominal hydraulic model* and its competition report shows methods disagreeing wildly on detection latency — yet a decade of leak-detection papers still answers only "is there a leak?", never the operator's actual question: "is this residual a leak, a faulty sensor, a demand shift, or my model being wrong here?"

**3. Real-world pain point.** Water utilities lose 20–60% of water to leakage (BattLeDIM problem description, battledim.ucy.ac.cy); false dispatches on sensor faults and mis-calibrated models waste crews; the EU drinking-water directive pressures utilities >50k users to deploy leak-measurement tooling. The operational decision is dispatch vs recalibrate vs replace-sensor — an attribution, not a detection.

**4. Community evidence (searched).**
- BattLeDIM dataset & rules: 2 years of 5-min SCADA (33 pressure, 82 AMR demand, 3 flow, 1 level sensors) on the 782-node L-Town network, with a *deliberately imperfect* nominal EPANET model — "data were generated using a modified 'real' EPANET model, which differed from the nominal model in several important aspects" (arXiv:2512.15685; Zenodo record 4017659, CC-BY; problem PDF at battledim.ucy.ac.cy).
- Competition summary paper (ResearchGate: "Battle of the Leakage Detection and Isolation Methods") — teams evaluated on *economic* criteria; incipient leaks detected with 7–20 day delays even by the best methods (ASCE JWRPM 2022, LILA paper, par.nsf.gov/servlets/purl/10343901).
- LeakDB (github.com/KIOS-Research/LeakDB): 500 scenarios, multiple networks — the cross-network transfer leg.
- BATADAL (cyber-attack benchmark, cited in the BattLeDIM rules): sensor-spoofing attacks on the same kind of SCADA — literally "the sensor is lying" with labels.
- Active model-based fusion line exists but stops short: Dual-UKF sensor fusion for leak localization (arXiv:2412.11687, Dec 2024) assumes trusted sensors and a trusted-enough model; the 2025 multivariate framework (arXiv:2512.15685) does detection/classification/pre-localization, not calibrated source attribution.
- Water informatics is a standing ESWA/EAAI topic; KIOS (U. Cyprus) keeps the benchmark ecosystem maintained.

**5. Under-solved.** (i) The **attribution task itself**: posterior over {leak at region r, sensor fault at s_i, demand-regime shift, model-mismatch zone} given the model-vs-SCADA residual field — no public benchmark protocol poses this, even though BattLeDIM+LeakDB+BATADAL jointly contain all the ingredients. (ii) **Calibration and abstention**: no method reports whether its leak probabilities are calibrated, or abstains under novel fault types. (iii) **Latency-aware belief**: frames/hours-to-confident-attribution at fixed false-dispatch rate, priced with the battle's own economic scoring. (iv) **Value of re-observation**: which sensor to poll/inspect next to resolve the ambiguity fastest (the "when to re-observe" pattern).

**6. Why not crowded.** Leak *detection/localization* is crowded (the battle had dozens of entries); *source attribution with calibration* is absent from the benchmark's own summary and from the 2024–2025 arXiv follow-ups found. The chemical-process community has posed sensor-vs-process distinction classically (PMC7865985) but with uncalibrated MSPC machinery, on TEP, and nobody has transferred the question to water networks where the *untrusted physics model* is an explicit, benchmark-sanctioned third evidence source. Verify with Q1–Q4 below.

**7. Why LoRA / tuned baselines / dominant modality won't trivially kill it.** No pretrained backbone dominates 5-min SCADA tabular streams — the tuned baseline is a multiclass GBDT/TCN over residual features, which we include and must beat on *novel-fault-type abstention and calibration*, axes on which closed-set softmax classifiers are structurally weak. No dominant modality: a leak and a stuck pressure sensor can produce identical single-channel residuals; only the *spatial correlation structure across the network graph* separates them (a lying sensor violates only its own factor; a leak perturbs a neighborhood; model mismatch is persistent and flow-regime-correlated). This is a constitutive-fusion task.

**8. IF fit.** Conflict between a knowledge-based source (hydraulic model), distributed sensors, and priors is canonical Information Fusion material (evidential/DS conflict, per-source reliability); the network structure invites factor-graph message passing — a formulation IF's readership recognizes.

**9. ESWA fit.** Decision-support system for utilities with economic latency scoring (the battle's own metric), dispatch-cost analysis, and an off-the-shelf reproducible stack — squarely ESWA.

**10. Public data & access risk.** BattLeDIM (Zenodo 4017659, CC-BY, ~hundreds of MB), LeakDB (GitHub), BATADAL (public), EPANET models included; WNTR/EPANET run in seconds on CPU (light simulation, not "simulator-heavy" — used only to compute residuals and inject controlled sensor faults). Risk: near zero.

**11. Baselines.** (a) Nominal-model residual + CUSUM/SPC thresholds (the classical utility practice; LILA-style); (b) data-only autoencoder/PCA reconstruction; (c) tuned multiclass GBDT/TCN on residual windows (the LoRA-analogue killer baseline); (d) Dual-UKF-style model-based estimator (arXiv:2412.11687) as the trusted-model straw; (e) per-sensor leave-one-out consistency heuristic.

**12. First 4–6h pilot (mostly CPU; GPUs idle or used for sweep parallelism).**
- Data subset: BattLeDIM 2018 calibration year (labeled leaks) + nominal EPANET model; inject controlled sensor faults (bias, drift, stuck-at, spike) into 10 of 33 pressure channels on leak-free segments; keep 2019 for holdout.
- Preprocessing (h1): compute per-node residuals = SCADA − nominal-model prediction (WNTR batch run, ~minutes); window into 6h segments.
- Models (h2–4): (i) multiclass GBDT on flattened residuals (killer baseline); (ii) per-sensor evidential "surprise" (each sensor predicted from graph neighbors + model prior) fused into a posterior over {leak-region, sensor-fault-id, model-mismatch, normal} via network-local conflict decomposition.
- Metrics (h4–6): attribution accuracy; AUROC leak-vs-sensor-fault; ECE; hours-to-confident-attribution @ 5% false-dispatch; abstention quality on one held-out fault family (e.g., train without "stuck-at", test with it).
- **Green:** structured evidential attribution ≥ GBDT on held-out-family AUROC by ≥7 pts AND better ECE, with sensible latency curves; leak-vs-sensor separation AUROC > 0.85.
- **Kill:** GBDT matches on the held-out family and calibration — then attribution is just supervised classification and the formulation adds nothing; or leak and sensor-fault residual signatures are inseparable even with graph structure (task ill-posed at this sensor density).

**13. Minimum ESWA claim.** A calibrated leak/sensor/model attribution system on BattLeDIM with economic latency scoring, cross-validated on LeakDB networks, plus a re-observation (next-sensor-to-inspect) policy showing reduced time-to-attribution — an applied decision-support paper with full reproducibility.

**14. Stronger IF claim.** General formulation: *attribution of model–data conflict over a physical network as evidential message passing with per-source reliability*, with (i) a conflict-decomposition result distinguishing node-local vs neighborhood vs global-persistent evidence signatures, (ii) conformal false-dispatch control, (iii) three domains (water + BATADAL attacks + one non-water system, e.g., LBNL HVAC) showing the formulation transfers.

**15. Red flags.** All-synthetic benchmark data (generated by EPANET variants) — mitigated because the mismatch between nominal and generator models is *by design* the object of study, but a hostile reviewer may still ask for one real-data appendix (options: UK/DMA open datasets; flag as risk). Attribution labels for "model mismatch" must be constructed from the known nominal-vs-real model diff — bookkeeping, not blocker. Classical chemometrics prior art (TEP sensor-vs-process, PMC7865985) must be cited and beaten on calibration/abstention, not ignored. Baseline risk: the GBDT could win in-distribution — that's fine; the claim lives on held-out-family + calibration + latency, and the pilot tests exactly that in one afternoon.

**Operator mapping (bank protocol).**
- *Failure signature:* global residual solve is opaque; need to attribute failure to one constraint → **#6 factor-graph-ization**. Cheap probe: small factor graph vs dense classifier; check whether a single-factor intervention (injected sensor lie) is diagnosable from local messages. Differential prediction: message passing localizes the responsible factor; a dense classifier gives an answer but cannot localize or accept a modular swap. Kill: if dense = graph on single-factor interventions, the structure buys nothing.
- *Failure signature:* hidden state / partial observability, info-gathering matters → **#25 belief-ization**. Cheap probe: oracle-state substitution — give the model the true fault source; if a belief head approaches oracle performance while a history-stack GBDT doesn't, the belief object is real. Differential prediction: only the belief formulation prices the value of polling one more sensor (the re-observation policy). Kill: history stack ≈ belief head.
- *Must bound false-dispatch rate / abstain on novel faults* → **#27 coverage-set-ization** (conformal attribution sets). Kill: conformal sets are vacuous (too wide) at useful coverage.

---

### #2 — BACKUP A. Sensor lie vs equipment fault vs control fault: calibrated attribution with abstention on public HVAC benchmarks

**1. Title.** Who broke the building: cross-system, calibration-first fault-source attribution on the LBNL FDD datasets.

**2. Reviewer eyebrow.** The national-lab consortium built the world's largest labeled HVAC fault corpus precisely because commercial FDD tools mis-attribute — yet the 100+ papers using it report multiclass accuracy on known faults, while the deployment killers (is it the sensor or the chiller? what about a fault type never seen in training?) go unmeasured.

**3. Pain point.** FDD false alarms and mis-attributions are the stated #1 adoption barrier for building analytics (DOE FDD program page, energy.gov); a mis-attributed sensor fault dispatches a mechanic; a missed one silently corrupts the control loop for months.

**4. Community evidence (searched).** LBNL FDD Datasets (OEDI submission 5763, DOI 10.25984/1881324): 7 system types (AHU, RTU, VAV, FCU, chiller plant, boiler plant), 250+ fault/severity conditions *explicitly including sensor faults, mechanical faults, and control-sequence faults*, full-year time series, CSV + Brick schema, created by LBNL/PNNL/NREL/ORNL/Drexel. DOE is actively extending it ("world's largest publicly available dataset with verified ground truth", energy.gov FDD page, updated 2026). The LBNL review (eta-publications.lbl.gov) notes half of studies stop at detection. Real-building semi-labeled AHU dataset (DOI 10.1016/j.dib.2024.110956) provides a real-data transfer leg with sensor-fault labels.

**5. Under-solved.** Fault-*source* posterior {sensor s_i lies, equipment component c fails, control sequence wrong, normal} with calibration; abstention/coverage on held-out fault families and held-out *system types*; severity-monotone confidence; use of the Brick graph as fusion structure. Current work: closed-set multiclass, accuracy-only.

**6. Not crowded.** HVAC FDD is a large literature but concentrated in building-science venues on detection accuracy; searched combinations of {calibrated, conformal, abstention, sensor-vs-equipment attribution} × LBNL return thin results (verify Q5–Q7). The framing "which evidence source is corrupted" imported from fusion theory is absent.

**7. LoRA / dominant modality.** Same structure as #1: tabular streams, no pretrained giant to LoRA; killer baseline is tuned GBDT/TCN multiclass — beat it on held-out-family abstention + calibration + cross-system transfer, which closed-set training can't express. Sensor-vs-equipment separation requires multi-point physical-consistency reasoning (supply/return/mixed-air triangulation) — constitutively multi-source.

**8–9. Venue fit.** IF: per-source reliability + graph-structured evidence fusion. ESWA: building-operations decision support is a core ESWA vertical.

**10. Data risk.** None: open CSV downloads, DOI'd, no signup friction.

**11. Baselines.** APAR-style rule bank (the industry standard); PCA/AE reconstruction; tuned GBDT/TCN multiclass; per-point physics residuals (mixed-air balance) + thresholds.

**12. Pilot (one afternoon, CPU/1 GPU).** Single-duct AHU dataset: 20 fault conditions incl. sensor biases at 3 severities + fault-free year. h1: windowing + physics residual features (mixing-box energy balance). h2–4: GBDT multiclass vs evidential per-source surprise fusion (each sensor predicted from siblings via Brick relations). h4–6: attribution AUROC (sensor vs equipment), ECE, severity-monotonicity of confidence, abstention on one held-out fault family. **Green:** sensor-vs-equipment AUROC >0.85 with calibrated confidence and non-vacuous abstention; structured beats GBDT on held-out family by ≥7 AUROC. **Kill:** GBDT matches everywhere.

**13. ESWA claim.** Calibrated attribution + abstention system across ≥3 LBNL system types + one real-building dataset, with dispatch-cost analysis.

**14. IF claim.** The same evidential-attribution formulation as #1 demonstrated as *domain-general* (HVAC + water + BATADAL), with the Brick/hydraulic graph as the shared factor structure and conformal guarantees.

**15. Red flags.** Simulated majority of data (HVACSIM+/Modelica) — real-building leg partially mitigates; fault-family taxonomy must be defined carefully to avoid label leakage; some LBNL sub-datasets have quirks (documented per-PDF). Prior art in chemical-process sensor-vs-process distinction must be engaged. Afternoon-falsifiable: yes, fully.

*(Operator mapping: identical triple to #1 — #6, #25, #27 — which is exactly why this is Backup A: it is a portfolio replication of the front-runner's formulation on independent data.)*

---

### #3 — BACKUP B. Map-health monitoring, repositioned: calibrated frames-to-detection on TbV with frozen features

**1. Title.** Trust decay, not map regeneration: a post-hoc, calibrated, temporally-accumulated map-validity belief with latency metrics — the monitoring layer the 2025 map-update wave skipped.

**2. Reviewer eyebrow.** 2024–2026 produced a wave of prior-informed map-update stacks (ExelMap, ArgoTweak, RTMap, LDMapNet-U) — every one a heavy BEV network scored on map quality — while the deployment question their own intros cite (when, and how confidently, should the fleet flag an element stale?) still has no calibrated, latency-scored answer; TbV, the one public benchmark for exactly this, has near-zero direct follow-up (repo dormant since 2023).

**3. Pain point.** HD-map maintenance cost is the stated motivation of the entire online-mapping literature; fleets need a cheap monitor emitting per-element trust with controlled false-alarm rates, runnable beside any frozen perception stack.

**4. Community evidence (all URL-verified).** TbV: NeurIPS 2021 D&B, arXiv:2212.07312, public via Argoverse 2 (CC BY-NC-SA), 200+ real-change validation/test logs, synthetic-change training protocol, documented sim2real gap. ArgoTweak (arXiv:2509.08764) confirms "real-world stale maps are rare" and that TbV lacks post-change ground-truth maps — which blocks *update* methods but not *trust monitoring*. Mind-the-Map (WACV 2025, arXiv:2311.10517) explicitly declines to evaluate on TbV for the same reason — leaving TbV's actual task unclaimed. ExelMap (arXiv:2409.10178) documents that prior-informed models "return to reproducing the prior," i.e., the field's own evidence that trust weighting is unsolved. RTMap (arXiv:2507.00980) does crowdsourced recursive updating but no calibration/latency protocol.

**5. Under-solved.** Log-level and element-level *belief accumulation* (recursive log-odds / evidential mass with viewpoint-reliability gating) over frozen per-frame features; metrics: ECE of accumulated belief, frames-to-confident-detection @ fixed FA, sim2real calibration transfer (train on synthetic changes, measure calibration on real ones — TbV's own documented gap, restated as a calibration problem).

**6. Not crowded.** The update stacks optimize map quality with full BEV training (weeks of GPU, out of scope for them to also do calibration); the monitoring formulation on frozen features is untouched per searches Q8–Q10.

**7. LoRA / tuned baseline.** The killer baseline is a tuned single-frame fusion classifier (TbV's own) with score averaging; the claim axes (calibration, frames-to-detection at matched FA) are outside its class. No dominant modality: change *is* map–sensor disagreement.

**8–9. Venue fit.** IF: sequential fusion with an untrusted prior. ESWA: map-maintenance decision support (weaker than #1/#2 because the "expert system" user is an AV fleet, not a classic ESWA industry).

**10. Data risk — the reason this dropped to Backup B.** TbV is per-log downloadable but large (7.9M images total); a 60–100-log front-camera subset must be verified to stay <100 GB *before* committing; pose–map rasterization plumbing is a real day of engineering. Falsifiable in an afternoon only *after* that day of setup — per your downgrade rule, it cannot outrank #1/#2.

**11. Baselines.** TbV paper's single-frame fusion nets; frozen DINOv2 + map-raster MLP; per-log mean/max score aggregation.

**12. Pilot.** 60 balanced logs, front camera; frozen DINOv2 image features + CNN map-raster embedding (2h); single-frame fusion head vs recursive log-odds accumulator with learned viewpoint reliability (2h); log-level AP, ECE, frames-to-detection @1% FA (1–2h). **Green:** ≥5 AP and ≥30% latency reduction with better ECE vs best single-frame aggregation. **Kill:** single-frame saturates → changes are perception-obvious; problem is perception-bound, drop it.

**13. ESWA claim.** Deployable map-health monitor with latency/FA curves on TbV + synthetic-edit nuScenes transfer.
**14. IF claim.** "Fusion with an untrusted prior" formulation, evidential-vs-Bayesian conflict analysis, calibration transfer across the sim2real change gap.
**15. Red flags.** Download logistics; log-level (not element-level) labels cap the granularity of claims; the update-wave papers will be demanded as related work and one may pivot into monitoring within 12 months (moderate scoop risk); CC BY-NC-SA is fine for papers.

*(Operators: #25 belief-ization + #32 residual-ization — frozen perception base, learn only the map-disagreement deviation; probe per card: belief head vs frame-stack on frames-to-detection.)*

---

### #4. When the physics model and the data disagree: conflict-attributed hybrid prognostics under regime shift

**1. Title.** Model-form error as a first-class evidence source: evidential conflict decomposition for battery SOH / turbofan RUL across cycling regimes.

**2. Reviewer eyebrow.** Hybrid "physics + ML" prognostics papers fuse the two with static weights tuned in-distribution — so precisely when the plant enters a new regime and the sources start disagreeing (the only moment fusion matters), the weighting is stale and the disagreement, the most informative signal available, is discarded.

**3. Pain point.** Battery warranty/second-life decisions and turbine maintenance hinge on RUL estimates that must survive duty-cycle changes; digital-twin standards work (ISO 23247-adjacent) names model–reality divergence monitoring as a requirement.

**4. Community evidence.** NASA & Oxford battery datasets, N-CMAPSS (all public, small); hybrid-PHM survey stream 2023–2025; the "process fault vs model drift" diagnosis framing has just appeared in chemometrics (NNV contribution analysis, 2025 — found via TEP search), confirming timeliness of "is the model wrong or the regime new" — but in a monitoring-statistics idiom without calibrated fusion or transfer. *(Crowding partially unverified — Q11–Q13.)*

**5. Under-solved.** Attribution among {regime shift, model-form error, sensor fault} with calibrated posteriors; regime-conditioned reliability weights; shifted-regime NLL as the headline metric instead of in-distribution RMSE.

**6. Not crowded.** PHM fusion is plentiful but static-ensemble-shaped; the conflict-attribution + shift-calibration formulation appears open per searches to date.

**7. Baseline threat.** Tuned stacking ensemble — must be beaten on shifted-regime NLL and injected-fault attribution, not on in-distribution MAE. No dominant modality: literature documents physics winning in some regimes, data-driven in others.

**8–9. Fit.** IF: knowledge-source vs data-source conflict (core canon). ESWA: industrial prognostics decision support (very strong).

**10. Data.** Pristine, tiny, CPU-scale.
**11. Baselines.** ECM physics model alone; GRU/TCN alone; static ensemble; tuned stacking; BMA.
**12. Pilot.** Train data-driven SOH on NASA cycling profile A, test on profile B; fuse with equivalent-circuit model via (i) static ensemble (ii) conflict-aware evidential weights; inject synthetic sensor faults. Metrics: shifted-regime NLL/MAE, fault-attribution AUROC, conflict–error correlation. **Green:** ≥20% shifted-regime NLL gain over tuned stacking + attribution AUROC >0.8. **Kill:** stacking matches under shift. Fully afternoon-falsifiable.
**13–14. Claims.** ESWA: two-dataset hybrid prognostics with conflict diagnosis. IF: theory of when BMA fails under model-form error + evidential alternative.
**15. Red flags.** Deep PHM baseline zoo (pre-empt with a broad cheap baseline table); ECM implementation quality will be attacked — use an established open implementation; crowding check still owed (Q11–Q13).

*(Operators: #32 residual-ization — freeze the physics base, learn its systematic deviation; #26 distribution-output-ization; probe: does the residual head's *disagreement magnitude* predict regime shift before error does? Kill if conflict is uninformative about impending error.)*

---

### #5. The gap is the message: calibrated intent-vs-coverage attribution for AIS transmission gaps

**1. Title.** Dark or just unheard? Fusing reception-quality priors, trajectory context, and SAR co-observation into a calibrated posterior over why a vessel's AIS went silent.

**2. Reviewer eyebrow.** Global Fishing Watch operationalized a rule-based + boosted-trees pipeline to separate intentional AIS disabling from satellite-coverage gaps (Welch et al., Sci. Adv. 2022; globalfishingwatch.org) — an inherently probabilistic evidence-conflict problem currently solved with hard rules and no calibration, even though enforcement decisions (send the patrol boat?) are exactly cost-sensitive posterior decisions.

**3. Pain point.** IUU fishing and sanction-evading "shadow fleets" (GFW estimates 75k+ vessels; blog.turqoa.com 2026) are prioritized by gap alerts; false accusations are diplomatically costly; missed intentional gaps waste patrol budgets.

**4. Community evidence (searched).** GFW AIS-disabling dataset and press materials (globalfishingwatch.org, 2022–2024, "dataset is now operationalized… produced in real time"); GFW Sentinel-1 SAR vessel-detection dataset matched to AIS (2017–present, downloadable, from Paolo et al. 2024 *Nature*); xView3 SAR dark-vessel challenge data; DarkVesselNet (arXiv:2606.00445) — 2026 work already fusing SAR + trajectory for dark-vessel *detection*, signaling the area is warming.

**5. Under-solved.** Calibrated attribution posterior {intentional-disabling, coverage/reception gap, technical failure} with per-evidence reliability (reception quality is itself estimated); decision-cost evaluation (patrol dispatch); abstention. GFW's own pipeline is rule-based + BRT, uncalibrated, and its labels are model-derived — an opportunity (weak-label learning) and a threat (circularity).

**6. Not crowded (yet).** Detection of dark vessels in SAR is active (xView3, DarkVesselNet); the *gap-attribution-with-calibration* formulation on the cooperative-tracking side appears unclaimed (verify Q14–Q15).

**7. Baselines / dominance.** Tuned GBDT on gap features is the killer baseline; reception-quality alone may dominate (kill test). Trajectory-only vs reception-only vs fused is the pilot's core ablation.

**8–9. Fit.** IF: informative missingness + multi-source reliability (strong). ESWA: maritime-domain-awareness decision support (strong).

**10. Data risk — the main weakness.** GFW gap-events data requires (free) registration and has weak, model-derived intent labels; SAR co-observation join is engineering-heavy. Downloadable subsets ~GBs. Label circularity caps the IF-level claim unless SAR-verified gaps are used as a cleaner test set.

**11–12. Pilot.** GFW gap-events sample (~2 GB public per github.com/jessicarose00/Dark_to_Transparent) + reception-quality layer: logistic/GBDT vs reliability-weighted evidential fusion; metrics: attribution AUROC vs GFW rule labels, ECE, and — decisive — performance on the subset where SAR detections confirm presence during the gap. **Green:** fused model beats reception-only and trajectory-only by ≥5 AUROC on SAR-confirmed subset. **Kill:** reception-quality alone suffices, or SAR-confirmed subset too small (<300 events) to claim anything.

**13–15. Claims & flags.** ESWA: calibrated patrol-prioritization system. IF: informative-missingness fusion with observed-confirmation validation. Flags: label circularity; registration-gated data; geopolitics-adjacent framing needs care; DarkVesselNet trajectory may extend here within a year.

---

### #6. Informative missingness in flood mapping: staleness-aware SAR–optical fusion where clouds correlate with the event

**Summary (fields compressed — mid-rank).** Optical imagery is missing *because of* the storm being mapped: missing-not-at-random, universally ignored by EO fusion which tests on clean pairs. Data: Sen1Floods11 (public, ~4.4k chips), PASTIS-R. Pilot (afternoon): SAR-only U-Net head vs SAR + last-available-optical with staleness encoding; IoU + ECE stratified by injected optical staleness. Green: staleness-aware fusion beats naive concat at high staleness and degrades gracefully to SAR-only with honest confidence. Kill: SAR-only matches everywhere including calibration (dominant-modality trap — the known main risk). IF fit: MNAR/multi-rate fusion. ESWA fit: operational flood decision support with latency curves. Baselines: SAR-only, naive concat, temporal-encoding SITS. Red flags: RS-fusion pile positioning; SAR dominance; crowding on "cloud removal" adjacent literature (verify Q16). Not front-runner because the dominant-modality kill risk is the highest in the top 6 — but the kill costs one afternoon, so it's a legitimate parallel probe.

---

### #7. Persistence-calibration: does a video model's uncertainty know the object is behind the box?

**Summary (fields compressed — demoted by TOC-Bench).** TOC-Bench (arXiv:2605.09904) now benchmarks temporal object consistency in Video-LLMs — accuracy-only. The surviving niche: a *persistence-calibration metric* (posterior must widen monotonically with occlusion duration, snap on reappearance) + a recursive evidential head over frozen features (visibility-gated learned filter), evaluated on CATER + Kubric-controlled horizons, transferred to TOC-Bench/MOSE occlusion strata. Loci-Looped (arXiv:2310.10372) shows latent-imagination tracking through occlusion is learnable — but reports tracking error, not calibration. Pilot (afternoon, the cheapest vision pilot here): frozen DINOv2 per-frame features on CATER; last-frame head vs LSTM vs recursive Gaussian belief head; NLL/ECE stratified by occlusion length; green = filter beats LSTM on long-occlusion NLL ≥20% with monotone variance; kill = LSTM calibrates equally well. IF fit strong (asynchronous visibility-gated evidence); ESWA fit moderate (surveillance/warehouse monitoring framing). Red flags: synthetic-first data; TOC-Bench team may add calibration in v2; a strong tracker (SAM2-lineage) must be shown uncalibrated under occlusion, which is plausible but unproven. *(Operators: #25 belief-ization, #16 object-slot-ization; probe = oracle-state substitution per card #25.)*

---

### #8. Asset-condition belief from repeated noisy inspections (sewer CCTV)

**Summary (fields compressed — safe but least tasteful).** Frame-level defect models exist (Sewer-ML, ICCV 2021, 1.3M public images); the operational object is per-asset condition belief across repeated passes + when to re-inspect. Pilot: video-grouped Sewer-ML subset, frozen DINOv2 frame features; MIL/max pooling vs recursive evidential per-asset update; asset-level F2 + ECE; green = evidential accumulation beats MIL on calibrated asset-level F2; kill = max-pooling suffices. ESWA fit excellent (inspection scheduling with cost curves); IF fit moderate. Red flag that caps its rank: Sewer-ML lacks true longitudinal revisits — revisit sequences must be simulated by temporal subsampling, weakening the headline claim. Afternoon-falsifiable: yes.

---

## Scoring Matrix (1–5; for the two "risk" axes, 5 = LOW risk)

| # | Candidate | Taste | Practical necessity | Future relevance | IF fit | ESWA fit | Data availability | 6h pilot feasibility | Baseline risk (5=safe) | Engineering risk (5=safe) | Kill-criteria clarity | Mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Water: leak / lie / wrong model | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 4 | 5 | 5 | **4.8** |
| 2 | HVAC fault-source attribution | 4 | 5 | 4 | 4 | 5 | 5 | 5 | 4 | 5 | 5 | **4.6** |
| 3 | Map-health monitor (TbV) | 5 | 4 | 5 | 5 | 3 | 3 | 3 | 4 | 3 | 5 | **4.0** |
| 4 | Physics-vs-data conflict prognostics | 4 | 4 | 4 | 4 | 5 | 5 | 5 | 3 | 5 | 5 | **4.4** |
| 5 | AIS gap attribution | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 3 | 3 | 4 | **3.7** |
| 6 | MNAR flood fusion | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 2 | 4 | 5 | **4.1** |
| 7 | Persistence-calibration (video) | 4 | 3 | 5 | 4 | 3 | 5 | 5 | 3 | 4 | 5 | **4.1** |
| 8 | Asset-condition belief (sewer) | 3 | 4 | 3 | 3 | 5 | 4 | 5 | 4 | 5 | 4 | **4.0** |

**Ranking rationale.** #1 and #2 lead because they are the only candidates simultaneously: afternoon-falsifiable with zero setup debt, immune to pretrained-backbone/LoRA capture, structurally multi-source (attribution *is* cross-evidence reasoning), aligned with three operator cards, and publishable as a two-venue ladder (ESWA system → IF formulation) on the *same* codebase. #3 keeps the highest taste/IF scores but pays a day of setup before its afternoon test — your downgrade rule applies. #4 is the low-risk parallel probe. #6/#7 are cheap probes worth running only if GPUs are otherwise idle. #5 and #8 are held in reserve.

- **Front-runner: #1 (water networks).**
- **Backup A: #2 (HVAC)** — same formulation, independent data; de-risks the front-runner and sets up the cross-domain IF claim.
- **Backup B: #3 (map-health monitor)** — the taste/vision leg, activated only if the lab wants a perception-flavored second paper and accepts one day of data plumbing.

---

## Front-Runner Mini-Proposal (one page)

**Title.** Leak, Lie, or Wrong Prior: Calibrated Attribution of Model–Sensor Conflict in Water Distribution Networks.

**Thesis.** In monitored physical networks, the operator's question is not "is there an anomaly?" but "which evidence source is wrong?" — the process (a leak), a sensor (a lie), or the model (a stale prior). The field's own benchmark, BattLeDIM, encodes all three failure sources (labeled leaks; injectable/spoofable sensors via the BATADAL protocol; a deliberately mismatched nominal hydraulic model) yet is used only for detection. We pose *calibrated conflict attribution over a physical network* as the task, give it a protocol (attribution AUROC, ECE, hours-to-confident-attribution at fixed false-dispatch rate, abstention on held-out fault families, economic scoring inherited from the battle), and show that network-structured evidential fusion beats tuned closed-set classifiers exactly on the axes deployment needs.

**Hypothesis.** H1 (separability): leak, sensor-fault, and model-mismatch signatures are distinguishable by their *spatial factor structure* — node-local (lie) vs neighborhood-coherent (leak) vs persistent-and-regime-correlated (mismatch) — and a factor-graph evidential model exploits this where a dense classifier cannot generalize it to unseen fault families. H2 (belief value): a recursive belief over fault source yields shorter time-to-confident-attribution at matched false-dispatch than window-classification, and prices the value of polling the next sensor (re-observation policy). H3 (transfer): the same formulation, re-fit, attributes on BATADAL attacks and LBNL HVAC without redesign.

**Datasets.** BattLeDIM (Zenodo 4017659, CC-BY) as primary; LeakDB for cross-network; BATADAL for adversarial sensor lies; LBNL FDD AHU for cross-domain (stretch). Controlled sensor-fault injection (bias/drift/stuck/spike) on leak-free segments provides label-perfect attribution training data — squarely within your "controlled synthetic perturbations" capability.

**Baselines.** SPC/CUSUM residual thresholds; PCA/AE reconstruction; tuned GBDT and TCN multiclass over residual windows (the LoRA-analogue); Dual-UKF trusted-model estimator; leave-one-sensor-out consistency heuristic; (reported, not beaten) top BattLeDIM detection entries for context.

**First experiment (the afternoon).** Hours 1–2: WNTR nominal-model rollout → residual field; inject 4 sensor-fault types across 10 channels; window. Hours 2–4: GBDT multiclass vs per-sensor evidential surprise (each sensor predicted from graph neighbors + model prior) fused by local conflict decomposition. Hours 4–6: attribution AUROC, leak-vs-lie AUROC, ECE, latency @5% false-dispatch, held-out-family abstention. **Go:** structured ≥ GBDT +7 AUROC on held-out family with better ECE, leak-vs-lie >0.85. **No-go:** GBDT matches on held-out family and calibration (formulation adds nothing), or leak/lie inseparable at this sensor density (task ill-posed).

**Expected failure mode.** The honest risk is that at 33 pressure sensors on 782 nodes, spatial structure is too sparse to separate a small leak from a drifting sensor. If so, the negative result itself parameterizes the paper's fallback: *attribution feasibility as a function of sensor density* (subsample sensors; plot separability vs density) — still a useful ESWA contribution, and the afternoon tells you which paper you're writing.

**Expected contribution.** (1) Task + protocol: calibrated fault-source attribution with latency and abstention on public water benchmarks. (2) Method: factor-structured evidential fusion with conflict decomposition and a conformal false-dispatch guarantee. (3) Decision layer: value-of-information re-observation policy scored economically. (4) Transfer: BATADAL + (stretch) LBNL showing formulation generality — the IF-level claim.

**Why this is not benchmark chasing.** No leaderboard is being climbed: the battle's detection metric is left to the existing literature, and the paper's headline numbers (attribution AUROC on held-out families, ECE, time-to-attribution at fixed dispatch cost) do not exist yet for anyone. The formulation answers the question utilities actually adjudicate daily, on data anyone can download in ten minutes, with a falsification that costs one afternoon.

---

## Avoid / Already-Crowded List (verified 2025–2026)

1. **Robot manipulation failure/success detection** — I-FailSense, Guardian, SAFE (NeurIPS'25), VLA-FAIL, AHA, ViFailback; multiple datasets and VLM verifiers released. Occupied.
2. **GUI action-effect verification & state-change critics** — VeriGUI, VisCritic, D-GARA, FineState-Bench, WorldGUI. Occupied within the last ~9 months.
3. **Prior-informed online HD map construction/update** — ExelMap, ArgoTweak, RTMap, LDMapNet-U, Uni-PrevPredMap; heavy-stack arms race; do not enter with 2 GPUs. (The monitoring niche, #3 above, is the only surviving corner.)
4. **Microservice root-cause analysis** — RCAEval (WWW'25), FSE'26 propagation-aware benchmark; dense, fast, and text/graph-dominant.
5. **Video-LLM temporal-consistency benchmarks (accuracy-only)** — TOC-Bench just landed; only the calibration angle (#7) is open, and possibly not for long.
6. **Generic missing/noisy-modality fusion, text-dominant multimodal classification, +1-point robust-BEV blocks, world-model physics leaderboards** — per your negative history and confirmed velocity; leaderboard-shaped, not formulation-shaped.

---

## 20 Exact Verification Queries

Crowding checks for the front-runner and backups (run on Scholar/arXiv/Google):
1. `BattLeDIM leak detection sensor fault attribution calibrated`
2. `water distribution network "sensor fault" versus leak discrimination evidential`
3. `hydraulic model mismatch "model error" leak localization uncertainty water network 2024..2026`
4. `BATADAL attack detection sensor spoofing attribution water`
5. `LBNL FDD dataset calibrated uncertainty fault diagnosis abstention`
6. `HVAC "sensor fault" versus "equipment fault" attribution conformal 2024..2026`
7. `building fault detection open set unseen fault type abstention AHU`
8. `TbV "map change detection" temporal accumulation calibration 2025..2026`
9. `HD map validity belief "false alarm" latency monitoring fleet`
10. `ArgoTweak RTMap map change trust score calibrated`
11. `hybrid prognostics physics informed conflict "model form error" attribution battery`
12. `battery state of health regime shift "distribution shift" hybrid model fusion NLL`
13. `N-CMAPSS hybrid physics data fusion evidential 2024..2026`
14. `AIS gap intentional disabling classification calibrated probability`
15. `xView3 dark vessel AIS gap attribution reception quality`
16. `Sen1Floods11 SAR optical fusion cloud "missing not at random" staleness`
17. `Tennessee Eastman "sensor fault" "process fault" distinguish deep learning calibration 2024..2026`
18. `"informative missingness" sensor fusion time series industrial`
19. `Information Fusion journal 2025 evidential conflict attribution physical network` (journal ToC scan)
20. `Expert Systems with Applications 2025 water leak HVAC fault diagnosis calibration` (journal ToC scan — establishes the venue's current idiom and confirms the calibration gap)

**Standing caveat.** Anchors were gathered by live search in July 2026 but snippets are partial; before the pilot, spend 60 minutes on Q1–Q7 (front-runner + backup A) and read the BattLeDIM summary paper and one LBNL dataset PDF end-to-end. If Q1–Q4 surface a 2025–2026 paper doing calibrated leak/sensor/model attribution on BattLeDIM, promote Backup A immediately.
