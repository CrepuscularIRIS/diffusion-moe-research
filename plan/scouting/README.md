# Scouting Portfolio — ⛔ ARCHIVED SNAPSHOT (2026-07-08)

> **Do NOT route from this file.** Every direction ranked below (TbV/AV2, OpenFly, C5/BEV, C1) is now ARCHIVED
> and some referenced data was deleted. The active direction lives in `.claude/CLAUDE.md` §3 +
> `plan/optical-sar-research-plan.md` (BRIGHT/DFC25). This file is kept only as the 2026-07-08 scouting record.

Status at the time: **water rejected / parked**; portfolio reset toward mainstream, GPU-heavy CV/AV directions.

Asset manifest: `openbuild/auto_trust/DATA_ASSETS.md`. Downloaded repo/paper root: `/data/autodrive/`.

## Active Ranking

1. **TbV/AV2 — Autodrive map-health / trust decay**
   - Source reports: `frontier_scouting_report.md`, `frontier_scouting_report_v2.md`.
   - Data already local: `/data/tbv_tars/TbV_v1.0_shard0.tar.gz`, `/data/tbv_tars/av2-api/`.
   - First gate: TbV/AV2 plumbing, then reproduce a tuned TbV single-frame baseline before any mechanism.
   - Method axis: temporal/evidential trust accumulator over frozen image + map-raster evidence.

2. **OpenFly — aerial VLA keyframe/memory reliability**
   - Source packet: `current-autodrive-recommendation/`.
   - Data already local: OpenFly-Platform + `openfly-agent-7b`.
   - First gate: checkpoint load + small-sample inference + failure/reliability logging.
   - Method axis: goal-observability, keyframe relevance, and action-risk reliability heads.

3. **C5 — Frozen BEV/camera-LiDAR sensor trust**
   - Source report: `frontier_scouting_report.md`.
   - Candidate substrate: nuScenes-C + BEVFusion/TransFusion.
   - Method axis: post-hoc per-sensor reliability and risk-coverage on frozen perception stacks.

4. **C1 — Video object-persistence belief**
   - Source reports: `frontier_scouting_report.md`, `frontier_scouting_report_v2.md`.
   - Candidate substrate: CATER/Kubric/TOC-Bench-style occlusion slices.
   - Method axis: recursive belief/filter head with occlusion-length calibration.

5. **C4 — SAR-optical staleness / informative missingness**
   - Source reports: all three scouting reports.
   - Keep as reserve only; remote-sensing fusion is crowded, so the claim must be MNAR/staleness-calibration, not
     generic segmentation.

## Parked

Water, HVAC, building ledger, PHM, industrial telemetry, and similar CPU-heavy engineering directions are no longer
active. They can remain as ESWA fallback material, but do not route there automatically.

## Report Files

- `frontier_scouting_report.md` — original broad 11-candidate map; best for GPU-heavy directions C1/C2/C5/C6.
- `frontier_scouting_report_v2.md` — web-grounded falsification-first revision; useful for crowding and kill criteria.
- `deep-research-report-2.md` — Chinese IF/ESWA scouting report; useful for alternative engineering backups.
- `deep-research-report-root-copy.md` — separate root copy kept for traceability; content differs from the plan copy.
- `current-autodrive-recommendation/` — latest concise recommendation packet for TbV/OpenFly/nuScenes-C/SceneEdited.
