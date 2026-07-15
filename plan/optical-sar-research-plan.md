# Optical-SAR Research Launch Plan

> Status 2026-07-10. History lives in `openbuild/optical_sar/RUNLOG.md`; this file is the launch contract.

## Decision

Domain question: reliable Optical-SAR decisions under semantic and sensor uncertainty — failure-source
attribution + selective prediction that changes accepted decisions. The claim-bearing object is a trained
decision operator, not another quality-weighted fusion network. Venue: Information Fusion / ESWA (Pattern
Recognition secondary).

**P0 (MM-OVSeg selective prediction) is REGION-CLOSED (2026-07-10).** Reproduction PASSED (DDHR-SK mIoU 73.61
vs paper 73.1) but the phenomenon gate was NO-GO: modality-ablation signals add only ~+0.02 AUROC over a tuned
confidence+boundary+brightness floor; additive fusion moves confidence, not decisions; novelty is trivially
entropy. Independent review confirmed the kill. Epitaph: `openbuild/optical_sar/atlas/mm-ovseg-selective.md`.
Banked anomaly (feeds P2): unseen-class water is high-entropy-but-correct (SAR-rescued) while unseen road is
confident-but-wrong → class-conditional semantic calibration.

## Portfolio

| Priority | Track | Baseline | Status / promotion condition |
|---|---|---|---|
| **P1 → ACTIVE** | BRIGHT/DFC25-Track2 cross-modal building-damage (pre-event optical + post-event SAR) under misregistration/cross-event shift | `bda_benchmark` + DFC25 leaderboard/winner repos | Reproduce the official DFC25 baseline number first; then the misregistration/reliability phenomenon gate |
| P2 | DELIVER class-conditioned reliability | CMNeXt + MAGIC++/StitchFusion-style rivals | Class-conditional reliability beats global confidence on unseen compound failures |
| P3 | Generic calibration/TTA | existing methods | Mechanism library only; never promoted alone |
| Closed | MM-OVSeg selective prediction | official checkpoint (reproduced) | Region-closed; reopen only if a trained (non-additive) fusion signal emerges |
| Parked | CAU-Flood change detection; missing-modality federated learning | CMCDNet | CAU-Flood is Baidu-Pan-locked — reopen only if the user supplies the tarball |

## Active Launch Contract — BRIGHT / DFC25-Track2

- Code: `/data/projects/optical_sar/BRIGHT_baseline` (official `bda_benchmark`, PyTorch supervised, torch 2.2.1,
  conda `bright-benchmark`). `umcd_benchmark` rejected (MATLAB/Windows, classical unsupervised, not GPU-trained).
- Data: HF `Kullervo/BRIGHT` → `/data/datasets/optical_sar/BRIGHT` (DFC25 setup skips UA/MY/MX events).
- Split: 9 events train/val + 2 held-out test events (Noto-EQ, Marshall-Wildfire) — built-in cross-event
  generalization = the reliability axis. B_test = the held-out events; sealed until confirmatory evaluation.
- Baseline number: DFC25 leaderboard / winner-repo metric — `unknown - measure during reproduction`.
- Constraints: do not alter labels/splits/evaluator; no test-set threshold tuning; ≤4h dev / 6h hard cap.

## Gates (in order)

1. **Asset:** archives complete and unzipped (pre-event, post-event, target); inventory recorded in
   `openbuild/optical_sar/DATA_ASSETS.md`. Check `/data/projects/optical_sar/dl_logs/` before any re-download.
2. **Environment:** official imports + one-pair inference run.
3. **Reproduction:** the official recipe reproduces the published/leaderboard baseline within a declared
   tolerance. If not, diagnose versions/preprocessing before any method work.
4. **Phenomenon:** the claimed failure sources (misregistration / cross-modal conflict / cross-event shift)
   are separable beyond entropy/energy, boundary-distance, brightness/severity, and unimodal-confidence
   controls — including a held-out event type.
5. **Method:** a trained operator changes accepted predictions and improves risk-coverage / accepted-set
   metrics without hiding errors by collapsing coverage.

## Stop / Pivot Rules

- Baseline cannot reproduce after a clean official env/data retry → foundation-fail: context-free GPT-5.6
  audit, then STOP_AND_REPORT.
- Failure-source separation no better than simple controls → autopsy, promote the next backup (P2).
- Selective gains come only from dropping boundary/dark pixels or easy cases → mechanism no-go.
- Calibration improves but task decisions do not → bank as diagnostic; not the contribution.

## Candidate reframe on deck (not yet /goal-adopted)

Aerial multimodal belief fusion reconstructed as learned **data assimilation** (multimodal posterior ·
flow-parameterized analysis step · OSSE privileged teacher) — `plan/aerial-world-model-reconstruction-2026-07-10.md`.
Next: cheap kill-probe on banked aerial dumps + GPT-5.6 occupancy triage; adoption is the human's call.
