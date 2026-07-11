# Aerial Multimodal Navigation → Data-Assimilation Reconstruction (2026-07-10)

**STATUS: PARKED (2026-07-10). REOPEN-IF: the user adopts this direction via `/goal`, OR the optical-SAR campaign region-closes. Until then no compute; the kill-probe below is the reopen entry point.**

> Banked per user request ("document this for now"). PRIMARY effort = the pipeline redesign (why the
> Reconstruction step is suppressed — see `plan/reconstruction-step-pipeline-redesign-2026-07-10.md`).
> This file preserves the reconstruction itself + the 3 candidate abstractions so they are not lost.

## The reframe (Information Fusion framing, per user)
NOT "a small non-video world model" — incremental; latent/short-horizon/non-video aerial world-action models
already exist. Central contribution = **distributed belief fusion + reliability-aware uncertainty modeling +
closed-loop bias correction & control**. IF-native pipeline:
`multisource observations → uncertainty-calibrated belief fusion → action-conditioned state prediction → closed-loop decision`.
Essential question: how to fuse imperfect, partial, inconsistent modalities into a latent state **closer to
reality than any single modality** — and model that "essential modality" (the latent state that best explains
heterogeneous observations) as the PRIMARY learning objective, not left implicit in a large model.

## The reconstruction: a learned nonlinear DATA-ASSIMILATION problem
Stripped to essence — *sequentially fuse imperfect multi-source observations into a multimodal distribution over
a hidden world-state, act on it in closed loop, with truth available only at training* — the problem IS nonlinear
non-Gaussian **sequential data assimilation** (the discipline behind NWP / oceanography / target tracking).

| Brief element | Data-assimilation object (borrowed elegance) |
|---|---|
| distributed belief fusion | the **analysis step**: prior/forecast belief × multi-source observations |
| reliability-aware uncertainty | **observation-error covariance** R + adaptive inflation (reliability = R⁻¹) |
| point prediction inadequate | **non-Gaussian multimodal posterior** (off-screen goal ⇒ several plausible states) |
| conditional velocity field over the **posterior** | **particle-flow filters** (Daum–Huang / stochastic interpolants): transport prior particles→posterior along an ODE velocity field, degeneracy-free, natively **flow-matching-parameterizable** |
| conditional velocity field over the **transition residual** | **weak-constraint 4D-Var / bias-aware assimilation** (model-error increment) = closed-loop bias correction |
| oracle as **privileged teacher, training-only** | **OSSE** (Observing System Simulation Experiment): a known nature-run generates observations; assimilate, score vs truth. A 40-yr accepted practice ⇒ teacher-student is rigorous, not a hack |
| "essential modality / latent state" | the **analysis state** (assimilated estimate) |

**Why this is the elegant move (not "a VLA + diffusion head"):** flow-matching becomes the *principled
parameterization of the DA analysis step as measure transport*; DA / sensor-fusion / uncertainty-calibration is
Information Fusion's home turf; and DA is badly under-transferred to embodied multimodal fusion.

## Prediction target
A conditional velocity field over EITHER (a) the world-state **posterior** OR (b) the **transition residual**.
Must DEMONSTRATE the posterior is genuinely **multimodal** — that is the differential vs the aerial campaign's
failed LGBF (a Gaussian, point-measurement Kalman belief that structurally cannot represent multimodality).

## Three candidate abstractions
- **A. Data assimilation / particle-flow filter — TRUNK (recommended).**
- **B. Active inference / free-energy — NARRATIVE** (the cat/dog internal-model story; motivates, doesn't carry baselines).
- **C. Optimal transport / Schrödinger bridge — TOOL** (the parameterization of the transport, inside A).

## Cheap kill-probe (banked aerial data, no retrain, ~an afternoon CPU)
Fit a tiny conditional flow vs the point-estimate `goalpred` on the drifted-state dumps (`dead_reckon_real_fixed.json`
+ adapters). Test: (i) posterior is multimodal on off-screen frames (>1 mode); (ii) sampling/averaging the flow
posterior **reduces the committed step-0 bias** that killed dead-reckon (aerial Step 23). If neither holds ⇒ the
reconstruction dies cheap, before any training.

## Practical (relaxed constraints, per user)
Backbone need not be frozen; LoRA = engineering option, not a hard constraint; the real constraint = total train
≤ 4–6 h. Prompts state the DOMAIN first, dataset in parentheses: *"Aerial multimodal embodied navigation (initial
experiments: AVDN / OpenFly)."*
