# World-Model Direction — Plan-of-Record (2026-07-11 · ADOPTED 2026-07-12)

> **STATUS: ACTIVE — the adopted research direction (2026-07-12). Venues = Information Sciences + AAAI.**
> Compute is PRICED per launch ({ETA · GPU-hours · expected info-gain · kill-checkpoint}), never hard-capped;
> sim/RL fully allowed (`.claude/CLAUDE.md` §0.2). **Env `/data/projects/world-model-lab/` is user-managed —
> INVENTORY it first; never rebuild what exists; heavy execution begins on the user's `/goal` trigger.**
> Reproduce-first STEP-ZERO still applies before any novel module — it is a quality invariant, not a cap.

## 2026-07-12 ACTIVATION UPDATE (verified — supersedes stale slice framing below)
- **Reproduce gate is CHEAP:** R2-Dreamer DMC-vision measured **~100 steps/s on one 4090 ≈ 3h/1M-step task**
  (not 12-30h). R2D walker reproducing (eval 903 > ~870 target @ 22% budget). Both GPUs busy (walker/GPU0,
  cheetah/GPU1). TD-MPC2 (aux) needs env fixes (submitit-launcher + enable_wandb=false + tensordict-vs-torch2.8
  skew, executor resolving). GPU1 = primary per user directive.
- **AAAI slice SHARPENED (J1/J2/J6, 精读 + cross-family occupancy search — all local-verified):**
  adaptive-horizon = SATURATED (ELVIS/Neubay, kill correct). Naive **event-triggered REPLANNING** in latent WMs
  is now **PRE-EMPTED/CLOSED** — AdaReP (2606.23079) gates planner invocation (>80% fewer queries, WM-frozen);
  changepoint-reset = ARCADE (2512.14331); surprise-gated sensor-trust reset = WISER (2512.01119).
  **The OPEN, defensible slice is NARROWER:** decision-theoretic **scheduling of costly WM PARAMETER-update**
  (suppress the expensive test-time adaptation until a CALIBRATED / anytime-valid / false-alarm-controlled
  trigger fires) **+ joint {no-op · re-anchor · replan · adapt} triage by decision-benefit-vs-compute**, evaluated
  decision-centrically. Incumbents to beat: AdaJEPA (always-adapt) · ARCADE (continuous changepoint) · AdaReP
  (replan-only). Banks: `openbuild/world-model/pro/{load-bearing-citations-精读,occupancy-search-event-triggered}-2026-07-12.md`;
  judgment rows J1/J2/J5/J6. The Week-1/Week-2 empirical gate still PICKS the direction — this shapes the design
  + differential prediction, not the gate.

## Framing / venue routes
- **The contribution is the decision-relevant CLAIM** (uncertainty / exploitability / event-triggered
  re-anchoring / context-adaptation); the world model is the VEHICLE.
- **Venue routes:** **AAAI** (compact algorithm — event-triggered-re-anchoring is the current best slice) ·
  **Information Sciences** (systematic study — transition-family-factorization is the current best slice).

## Phase 1 — MUST deploy + reproduce (= STEP ZERO, before any new module)

| Prio | Repo / paper | Role | Minimum reproduction |
|---|---|---|---|
| P0-1 | **R2-Dreamer** (ICLR 2026, `NM512/r2dreamer`, PyTorch) | main dev framework | DMC Vision 2 tasks + DMC-Subtle 1 task |
| P0-2 | **TD-MPC2** (ICLR 2024, `nicklashansen/tdmpc2`) | decoder-free, planning-based strong baseline | same DMC tasks as R2-Dreamer |
| P0-3 | **DreamerV3** (Nature 2025, `danijar/dreamerv3`, JAX) | world-model reference frame | ≥1 DMC task run + curve check |
| P0-4 | **dm_control** (`google-deepmind/dm_control`) | base continuous-control env | pin version; emit BOTH state + pixel obs |
| P0-5 | **CARL** (`automl/CARL`) | dynamics-shift / OOD platform | context change on mass / friction / gravity |

### Algorithm repos — notes
- **R2-Dreamer = MAIN dev repo.** Decoder-free + no-aug; redundancy-reduced objective → decision-relevant repr.
  PyTorch (easy to add uncertainty / fusion / new losses); ships RSSM + actor-critic + its own efficient
  DreamerV3 + DMC / DMC-Subtle / Meta-World interfaces; no image-recon branch to maintain; DMC-Subtle probes
  "is small-but-critical info preserved by the WM." Min repro: `walker_walk` + `cheetah_run` + 1 DMC-Subtle;
  also run the repo's DreamerV3 baseline; log return / VRAM / FPS / train-time / latent-dim / seed; resumable
  ckpt + full env config. **CAVEAT: new 2026 repo, short commit history → verify stability FIRST; do not treat
  the paper curves as already reproduced.**
- **TD-MPC2 = heterogeneous strong baseline (must keep).** Local trajectory optimization in latent space
  (decoder-free, planning-oriented) — a real mechanistic contrast to Dreamer's "train actor by imagination."
  Tests whether our method is Dreamer-architecture-specific; separates repr-improvement from generation-quality;
  strong official code + per-task/per-seed checkpoints. Min repro: same DMC tasks; state version first, then
  pixel; reproduce one official checkpoint / near-official curve; log #MPC candidates / horizon / model-update
  ratio / inference cost. **Do NOT start with the 317M multitask model — Phase 1 needs a stable modifiable
  single-task baseline.**
- **DreamerV3 = reference frame.** Deploy the official JAX repo (run ≥1 DMC task to check official behavior) +
  use R2-Dreamer's built-in **PyTorch** DreamerV3 as the main modifiable / fair-ablation version. Compare
  learning TRENDS (JAX vs PyTorch), not step-exact numbers; log img-size / action-repeat / batch-length /
  train-ratio / model-size; keep later experiments inside the one PyTorch framework to avoid framework as a
  confound.

### Environment repos — notes
- **dm_control:** standardized MuJoCo tasks, interpretable dynamics, state + pixel, easy physics edits. PIN:
  Python / MuJoCo / dm-control version / img-resolution / camera-id / action-repeat / episode-length /
  EGL-headless. First tasks: `walker_walk` (standard) · `cheetah_run` (fast dynamics) · `cartpole_swingup`
  (debug) · 1 DMC-Subtle (tiny decision-relevant visual info).
- **CARL:** wraps RL envs as configurable contextual-RL (gravity / friction / mass / joint-strength) → the
  dynamics-shift / OOD / fast-adaptation / uncertainty axis. Min experiment: train-distribution + interpolation
  (unseen in-range) + extrapolation (out-of-range); context-visible vs hidden; single vs joint param change;
  compare return-drop / multi-step pred-error / uncertainty. **NOTE: may not drop-in to every WM repo → first
  confirm context-change works standalone, THEN wire into R2-Dreamer / TD-MPC2.**

## Phase-1 EXIT (strict — NO new uncertainty/fusion module before all 5 pass)
1. R2-Dreamer reproduces 3 tasks · 2. TD-MPC2 reproduces 2 of the same · 3. DreamerV3 reproduces 1 of the same ·
4. dm_control unified env wrapper done · 5. CARL one physical-param train/interpolation/extrapolation split done.
Until these 5 are done: do NOT deploy DIAMOND / OC-STORM / large video datasets; do NOT write the new module.

## Phase 2 — read now, deploy ONLY if that route is chosen
- **STORM** (NeurIPS 2023) — Transformer WM / Atari-100k (single 3090). Original repo unmaintained → OC-STORM.
  Read the paper; not a P0 repo; deploy only for the Atari / Transformer / object-centric route.
- **OC-STORM** (ICLR 2026, `weipu-zhang/OC-STORM`) — object-centric WM from few-shot annotations; small-but-key
  objects in visual WMs. **The strongest Information Fusion fit (pixel + object-feature fusion),** but adds
  seg-foundation-model + annotation pipeline complexity → NOT concurrent with Phase-1.
- **DIAMOND** (NeurIPS 2024 Spotlight, `eloialonso/diamond`) — diffusion WM, Atari, visual-detail ↔ decision.
  Read; deploy only for the diffusion / generation-quality / visual-counterfactual route. Diverges from
  DMC/CARL → not early (splits engineering).

## Must-read papers (no code deploy)
- **"How Should World Models Be Evaluated? A Decision-Making-Centric Position"** (arXiv 2606.15032) — layered
  eval: counterfactual-action fidelity · closed-loop rollout · reward/value prediction · policy ranking ·
  optimization gain · model exploitability · uncertainty calibration. **Defines our metrics.**
- **"Calibrated Model-Based Deep RL"** (arXiv 1906.08312) — planning uncertainty must be CALIBRATED, not just
  output variance. Theory anchor for the uncertainty-aware WM route.

## Local directory (the user is setting this up in parallel — reference only)
```
world-model-lab/
├── algorithms/{r2dreamer(main), tdmpc2(planning baseline), dreamerv3-official(behavior check)}
├── environments/{dm_control, CARL, dmcgb2(phase-2 visual generalization)}
├── third_party/{storm, oc-storm(fusion candidate), diamond(diffusion candidate)}
└── configs/ checkpoints/ datasets/ logs/ evaluation/
```

## Discipline (from `plan/goal-directive.md` — active)
- **CLAIM-FIRST:** the contribution is the decision-relevant claim — not "a world model."
- **REPRODUCE-FIRST = STEP ZERO:** the Phase-1 5-item exit IS the reproduce gate; no novel module before it.
- **COMPUTE = PRICED, not capped:** measure per-task wall-clock at 等级-0 (launch arithmetic: sec/step × steps =
  ETA + GPU-hours + expected info-gain + kill-checkpoint) before every training launch. Full-budget DMC-vision
  runs (~1M steps) and multi-seed sweeps are legitimate when priced; the bug is an unpriced launch or an
  unkilled overrun. Statistical floor on DMC-class benches: ≥5 seeds + paired stats (rliable-IQM).
- **EMPIRICAL GATES (replace the old adoption gate):** (a) R2-Dreamer / TD-MPC2 reproduce on our box
  (Phase-1 exit)? (b) do the Week-1 frozen-checkpoint probes show measured headroom (their pre-registered kill
  criteria decide)? — the Week-2 gate picks the direction by headroom, never by taste.

## Deep-research refinement (2026-07-11) — the operational strategy
Source: `WorldModel/deep-research-report (4).md`; distilled → **`plan/world-model-strategy-digest-2026-07-11.md`**
(the actionable strategy — READ THIS when activating). Key decisions that sharpen this plan:
- **Two lines, shared infra, SEPARATE hypotheses.** **Route A (AAAI compact algorithm) = GO** · **Route B (一区
  journal) = conditional GO → Information Sciences** · **Information Fusion = default NO-GO** unless the paper is
  genuinely source-aware + confidence-aware + time-aware fusion (concat-into-RSSM ≠ fusion).
- **Route A central hypothesis:** a compact decoder-free latent WM giving CALIBRATED epistemic uncertainty on
  multi-step error, used as an **imagination-control signal** (not a passive diagnostic), improves closed-loop
  return + policy-ranking agreement + exploitability robustness under unseen dynamics + policy-induced OOD.
  Main design = CAWM-H (epistemic head + h-step calibration + uncertainty-adaptive imagination horizon).
  **⚠ SUPERSEDED IN PART by the operator-bank audit (section below): the adaptive-horizon component is
  SATURATED (Neubay 2512.04341 · ELVIS 2605.04709) — keep it as ablation arm, not the contribution; the
  Route-A slice shifts to event-triggered-re-anchoring / exploitability / context, decided by Week-1 probes.**
- **Baseline roles confirmed:** R2-Dreamer = MAIN (verify-first, new repo) · TD-MPC2 = planning-oriented aux +
  fallback main if R2 unstable · DreamerV3 = reference via R2's PyTorch reproduction (not the JAX repo).
- **Env priorities:** DMC ecosystem (Vision/Subtle/GB2/Distracting = visual OOD) **+ CARL-DMC (dynamics-shift
  decoupler, the core Route-A experiment)**; Meta-World (task shift) 3rd; **DMC-VB (state+pixel paired) for
  Route B fusion**. Keep dynamics/visual/task shift SEPARATE in the protocol.
- **Decision-centric evaluation is the contribution surface** (report with model-metrics at matched budget):
  counterfactual-action fidelity · closed-loop rollout validity · policy-ranking agreement · optimization lift ·
  model exploitability · uncertainty calibration (ECE/ENCE/coverage/error-corr) · dynamics/visual/task OOD-AUROC ·
  long-horizon consistency. Return-only is a documented reject risk.
- **4-week ramp = our STEP ZERO refined:** Wk1 install R2/Dreamer-baseline/TD-MPC2 + unify DMC/CARL wrapper · Wk2
  等级-0 reproduce DMC Vision + CARL-DMC + build decision metrics · Wk3 minimal method (small ensemble + calib +
  adaptive horizon) on 2 DMC + 2 CARL shifts · Wk4 first Go/No-Go. AAAI-27 = **7-page body**.
- Compute confirms our caveat: **one-GPU-one-run, not one-big-model**; R2 ~12–28GB, TD2 ~8–16GB single-task;
  DMC Vision budget ~1M steps → measure wall-clock at 等级-0 before scaling.

## WM operator + trick bank (2026-07-11) — wired into research-os
The knowledge layer for this direction is pre-built at **`WorldModel/`** (see `WorldModel/README.md` for the
reconciled dispute-map + retrieval wiring). Contents:
- **`WorldModel/wm-operator-bank-report.md` = the canonical WM operator bank** — full corrosion audit of the
  45 `opus-pass/operators.md` cards against the WM domain (repo-verified 2026-07-11). Net: 45 → **5 top-tier
  cards** (`transition-family-factorization` · `model-exploitability-objectization` ·
  `event-triggered-re-anchoring` · `policy-ranking-ization` · `belief-ization` rewritten) + ~8 mid/conditional
  + `oracle-factorization-of-WM-errors` as the standing META protocol. Each top card carries a numerical kill
  criterion pre-registered before its probe. `/forge` retrieves by failure signature via the report's §K
  index; `/autopsy` uses the §B 20-signature map; §G adds 7 WM anti-patterns as live gates.
- **`WorldModel/Trick.md`** = the WM adaptation of `plan/taste-bank/` — 20 oracle/intervention families +
  the **Bottleneck Panel** (8 experiments, ~1 wk, 3 idea-killers) + confound warnings. Feeds `/prereg` and
  every cheap probe. Day-0 harness validation is a non-skippable precondition.
- **KEY CORRECTION to the digest:** adaptive imagination horizon (CAWM-H's differentiator) is **saturated**
  (Neubay/ELVIS 2025–26) → recorded as anti-pattern `adaptive-horizon-as-novelty`. The open AAAI slice =
  **event-triggered-re-anchoring** (innovation-gated replan/re-anchor; AdaJEPA lists it as future work).
- **Week-1 probes run INSIDE Phase-1 STEP-ZERO** (piggyback on reproduction checkpoints; all frozen-ckpt /
  eval-only / logging-only, ≤1 GPU-day each): exploitability-G(t) logging · event-trigger threshold sweep ·
  context inference-gap w/ oracle injection. **Week-2 = empirical decision gate** — rank survivors by
  measured headroom; the winner gets the minimal method run; no direction picked by taste.
- Venue routing per the bank: AAAI = event-triggered-re-anchoring · Information Sciences =
  transition-family-factorization · Information Fusion = only the STEVE-lineage reliability-fusion form.

## External reference (broader field context, not a decision)
- `plan/world-model-field-analysis-chatgpt-2026-07-11.md` — external-brain (ChatGPT) field map of world models /
  autonomous driving / quadruped / VLA. Broader-field context (robotics/safety/verifier emphasis): the field's
  open problem = action-conditioned causal prediction + state estimation under partial observability +
  uncertainty/safety verification; a compact latent dynamics WM beats generative video for a small team on
  1×3090/4090. Complements — but the deep-research digest above is the operational plan (it matches the repos
  actually being installed: R2-Dreamer / TD-MPC2 / DreamerV3 + DMC/CARL).
