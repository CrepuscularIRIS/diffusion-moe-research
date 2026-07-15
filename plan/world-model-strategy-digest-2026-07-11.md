# World-Model Topic-Selection — Strategy Digest (2026-07-11)

> **SOURCE:** `WorldModel/deep-research-report (4).md` (deep-research report for a 2×48GB-GPU world-model line;
> distilled here, citation markers stripped). REFERENCE for the on-deck direction — companion to
> `plan/world-model-direction-2026-07-11.md` (plan-of-record) and `plan/world-model-field-analysis-chatgpt-2026-07-11.md`.
> Context: 6–12 months, 2×48GB GPU, ONE AAAI compact-algorithm line + a parallel 一区-journal reliability/fusion line.

## Bottom line (Go / No-Go)
- **Route A (AAAI compact algorithm) = GO.** Central problem = *uncertainty-as-imagination-control* (below).
- **Route B (一区 journal, reliability/fusion) = conditional GO → aim Information Sciences.** Reframe as
  uncertainty-guided multi-source + multi-timescale fusion under missing/noisy/conflicting inputs.
- **Information Fusion = default NO-GO (scope mismatch)** unless the paper is *genuinely* source-aware +
  confidence-aware + time-aware fusion (not concat-into-RSSM). IF Aims&Scope demands multi-sensor/multi-source/
  multi-process, feature/decision/multilevel fusion, imperfect/incomplete environments.
- **Do NOT chase:** foundation-scale video world models · massively-multitask WM scaling (Newt/WPT) · Atari-100k
  pure-score race (IRIS/STORM/TWM/DIAMOND already deep, and misaligned with dynamics-shift/continuous-control).

## The scientific reframe (why this is worth doing)
Not "can the WM generate prettier video," but: **under unseen dynamics, policy-induced OOD, and long-horizon
imagination compounding error, can the model KNOW when it is unreliable and convert that into more robust
closed-loop decisions.** One-step error / PSNR-SSIM / final return each mislead in isolation.

## Baselines (repo-availability first, not paper scores)
- **R2-Dreamer = MAIN dev repo** (ICLR 2026, `NM512/r2dreamer`, PyTorch, MIT, decoder-free + no-aug, redundancy-
  reduced latent). Covers DMC Vision/Subtle · Meta-World · Crafter · Atari-100k · Memory Maze · IsaacLab; ships a
  ~5× faster PyTorch DreamerV3 baseline for fair ablation; ~1.59× faster than that baseline. RISK: new repo, ~8
  commits → **treat as high-value-but-verify (等级-0 first); do NOT treat paper curves as reproduced.**
- **TD-MPC2 = strong planning-oriented aux baseline** (ICLR 2024, `nicklashansen/tdmpc2`, MIT, 300+ checkpoints,
  104 continuous-control tasks, single-task online **≥8GB GPU**, 317M multitask needs ≥24GB). Decoder-free implicit
  model + value-guided MPC = a real mechanistic contrast to Dreamer's imagination-actor. Meta-World needs
  MuJoCo 2.1.0 + old gym (install baggage).
- **DreamerV3 = reference frame** (Nature 2025). Deploy official JAX to check behavior on ≥1 task, but use
  **R2-Dreamer's built-in PyTorch DreamerV3** as the modifiable/ablation version — not the JAX repo as base.

## Environments (by "can I do a rigorous experiment," not popularity)
- **DMC ecosystem = 1st priority:** DMC Vision/state · DMC-Subtle (tiny decision-relevant visual info) · DMC-GB2
  + Distracting Control (visual OOD). Unifies visual/OOD/long-control into one protocol.
- **CARL-DMC = 2nd priority (the dynamics-shift decoupler):** gravity/friction/mass/joint-strength as explicit
  context → the core Route-A experiment (train context fixed, test context changed); context is a natural 3rd source.
- **Meta-World = 3rd (task shift / manipulation), only when needed.**
- **DMC-VB = Route B's offline state+pixel-paired multi-source benchmark** (fusion, distractors).
- Keep **dynamics-shift, visual-shift, task-shift SEPARATE** in the protocol (CARL vs DMC-GB2 vs Meta-World) —
  else "robust to background" gets mis-sold as "robust to dynamics."

## Route A — the AAAI line
**Central hypothesis (recommended):** *if a lightweight decoder-free latent world model produces CALIBRATED
epistemic uncertainty on its multi-step prediction error, then using that uncertainty as an IMAGINATION-CONTROL
signal (not a passive diagnostic) improves closed-loop return + policy-ranking agreement + model-exploitability
robustness under unseen dynamics and policy-induced OOD.* Focus is uncertainty's USE, not its existence.

- **CAWM-H (main design):** R2-Dreamer + small latent epistemic head (3-head transition or bootstrap latent
  heads) + light h-step-error calibration (reliability loss or post-hoc monotonic calibrator) + **uncertainty-
  adaptive imagination horizon** (truncate/риск-adjust imagined rollout when cumulative epistemic risk exceeds
  threshold). Differentiator: controls imagination LENGTH/USE, not just estimates or penalizes uncertainty.
- **CAWM-C:** + short K-transition context-inference module → decompose uncertainty into context-mismatch
  epistemic vs env aleatoric; WM *reliability gating*, not full meta-RL.
- **CAWM-X:** + uncertainty-weighted conservative actor regularizer targeting **exploitability** directly.
- **Min publishable experiment:** R2-Dreamer (main) + TD-MPC2 + same-repo Dreamer baseline · DMC Vision 2 tasks +
  CARL-DMC 2 dynamics-shift tasks · shifts = gravity AND friction/mass · 3 seeds · metrics = return · uncertainty
  calibration · policy-ranking agreement · horizon-vs-error-growth · ablations = no-calib / fixed-horizon /
  uncertainty-for-logging-only / **parameter-matched extra-head baseline**.
- **6 required ablations:** uncertainty-head capacity · calibration on/off · fixed-vs-adaptive horizon · logging-
  vs-control · param-matched head · real-vs-inferred context (if CAWM-C).
- **5 rejection risks to pre-empt:** looks like "R2-Dreamer + uncertainty head" · return-only (no decision-centric
  eval) · dynamics∪visual shift conflated · ensemble-gain = param-gain · unfair budget (steps/preproc/action-repeat).
- Titles: *Calibrated Adaptive World Models for Robust Planning under Dynamics Shifts* / *When to Stop Imagining:
  Calibrated Uncertainty for Robust Latent World Models.* NOTE **AAAI-27 = 7-page body** (not 8).

## Decision-centric evaluation matrix (the real contribution surface)
Report BOTH model-metrics and decision-metrics at matched budget: **counterfactual action fidelity** (fix prefix,
branch action, compare real-env vs WM on short reward/successor/terminal) · **closed-loop rollout validity**
(return drop / trajectory divergence in real env) · **reward/value horizon-conditioned error growth** · **policy-
ranking agreement** (Kendall τ / Spearman across policies, WM vs real) · **optimization lift** (same real-interaction
budget, with vs without WM) · **model exploitability** (ranking inversion, fake-high imagined policies collapsing
in real env) · **uncertainty calibration** (ECE/ENCE, coverage, NLL, error-uncertainty correlation) · **OOD
detection** (dynamics/visual/task AUROC-AUPRC, reported separately) · **long-horizon consistency** (horizon sweep).

## Route B — the Information Sciences line
Framework = **Uncertainty-Guided Multi-Source & Multi-Timescale Fusion World Model**: (1) source-specific encoders
(pixel · proprio/state · context); (2) fusion-aware latent dynamics with **fast latent** (short-horizon control) +
**slow latent** (context/long-horizon) and uncertainty-gated fusion; (3) reliability head (rollout uncertainty +
source confidence + missingness consistency) → decision-level fusion / branch reweighting. Genuine-fusion test =
**source-aware + confidence-aware + time-aware** (for IF, replace layer-2 with an explicit multilevel-fusion +
source-conflict block). Substrates = DMC-VB + CARL-DMC (+ Meta-World). Three degradations = **missing modality ·
sensor noise/corruption · asynchronous/conflicting evidence**. Journal stats = paired bootstrap over tasks×seeds ·
Wilcoxon/paired-t · effect size · reliability diagrams (slope/intercept/coverage). Failure-case section is required.

## Compute organization (2×48GB)
**One-GPU-one-run, not one-big-model.** GPU0 = method/ablation, GPU1 = strong baseline / extra seed; DDP only if
the repo natively supports it. R2-Dreamer ~12–28GB; TD-MPC2 ~8–16GB single-task. Tiers: **等级-0** (2 tasks, 1 seed,
sanity) → **等级-1** (4–6 tasks, 3 seeds, feasibility) → **等级-2** (8–12 tasks, 3–5 seeds, full submission).
R2-Dreamer budgets: DMC Proprio 500K · DMC Vision/Subtle 1M · Meta-World 1M · Atari-100k 400K · Crafter 1M.

## 4-week plan (STEP ZERO → first Go/No-Go)
- **Wk1:** install R2-Dreamer + same-repo Dreamer baseline + TD-MPC2; minimal DMC train; log VRAM/steps-per-sec/
  ckpt-freq/video cost; unify DMC + CARL wrapper.
- **Wk2:** 等级-0 reproduce DMC Vision + CARL-DMC; build decision metrics (rollout-error-growth, uncertainty-error
  correlation, policy-ranking-agreement prototypes). No new algorithm yet.
- **Wk3:** minimal Route-A method (small ensemble/multi-head + calibration + adaptive horizon) on 2 DMC + 2 CARL
  shifts; look for "calib improves but return flat" / "return up but ranking flat" forks; if all fail → simpler version.
- **Wk4:** first **Go/No-Go**. Route-A positive → scale to 3 seeds + AAAI narrative. Route-A weak but DMC-VB paired
  data working → open Route-B fusion skeleton in parallel. R2-Dreamer unstable → promote TD-MPC2 to main base,
  keep R2 as the research object.

## Overlap discipline (two lines, shared infra, SEPARATE hypotheses)
Shared: R2-Dreamer base · DMC/CARL wrappers · logging · decision-eval toolkit · calibration plots. Separate:
Route A = *uncertainty controls imagination/planning* (pixel + latent uncertainty; key plot = return/ranking/
exploitability vs uncertainty-guided horizon); Route B = *imperfect multi-source multi-timescale fusion* (state/
proprio/context/missingness as the core; key plot = fusion under missing/noisy/async vs single-source). Novelty
landmine: "Dreamer + ensemble + uncertainty-penalty + multi-step-consistency" reads as module-soup and collides
with P2P / ROMBRL / RWM-U / WIMLE — the defensible slice is *calibrated uncertainty AS imagination controller
under dynamics shift*.

## Closest prior work (verify locally before it anchors a design)
R2-Dreamer · Plan-To-Predict (P2P) · Calibrated MBRL · RWM-U · Policy-Driven WM Adaptation (ROMBRL) · WIMLE ·
Imperfect World Models are Exploitable · "How Should World Models Be Evaluated?" (decision-centric position).
