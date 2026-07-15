# Judgment Lessons — curated calibration priors (the evolving layer)

> Distilled from resolved ledger rows + banked campaign history; refined at every programme pulse and campaign
> close, like memory. **APPLY these as explicit corrections when writing any new forecast** (state the
> correction: "raw 0.7 → L2 caps at 0.4"). Recall at goal-start + before every claim-bearing `/forge`.
> Priors below seeded 2026-07-12 from campaign history — grade {inferred}; they will be recomputed from actual
> ledger scores once rows resolve.

## Priors (apply to new forecasts)

- **L1 · FEASIBILITY OPTIMISM (direction-level).** Every 2026 campaign that reached a close (VLA-manipulation,
  aerial-VLN, optical-SAR/BRIGHT, water-parked, BEV/C5) died a feasibility death knowable at selection —
  historical P(direction survives to a method-win | selected without cheap feasibility evidence) ≈ 0/5.
  → Direction-level survival forecasts start ≤0.3 absent MEASURED evidence (a passed reproduce gate, a
  probe-verified phenomenon); each passed empirical gate is what raises them.
- **L2 · PHENOMENON ≠ RECIPE (mechanism-conversion).** Optical-SAR: phenomenon verified real (modality collapse,
  exp-verified) yet the first cure recipe failed the screening bar (input-masking didn't route SAR into the
  decision). The implicit forecast was ~0.7; outcome 0. → P(first mechanism recipe works | phenomenon real)
  capped at 0.4 until a cheap probe shows the mechanism ROUTES the signal (not merely correlates with it).
- **L3 · FIRST-CONTACT COST OPTIMISM.** New envs/repos historically overrun early estimates (bright-benchmark
  env build died on a dependency pin; the 22h dead-Xet download; fresh-repo debugging). → Multiply first-contact
  ETA estimates ×1.5–2 and widen ranges UPWARD until a measured sec/step exists; never forecast cost on a new
  substrate as {verified}.
- **L4 · TRIAGE ≠ TRUTH (occupancy calls).** External-brain/deep-research citations — especially future-dated
  arXiv IDs — are triage-grade with nonzero fabrication/inflation risk. → Occupancy/saturation forecasts cap at
  0.85 until local 精读; a novelty-OPEN call additionally decays toward submission time (others read the same
  future-work notes).
- **L5 · KILLS ARE BETTER-CALIBRATED THAN BUILDS.** The pipeline's negative judgments (kill-probes, region-closes)
  have repeatedly been confirmed by later evidence (aerial DA kill-probe → shrinkage-kill; MM-OVSeg NO-GO), while
  its positive build bets underperform (L1, L2). → Asymmetric trust: a pipeline KILL at p≥0.8 is actionable; a
  pipeline BUILD at p≥0.8 still wants the cheap probe first.

- **L6 · VERIFY-THE-RESULT-IS-CAUSAL, not just executed (2026-07-12, from the Week-1 R2-Dreamer Gate-1 artifact).**
  A surprising DOWN (ρ<0, "adaptation hurts return") passed STRUCTURAL exp-verify (ran, artifacts exist, "the
  intervention changed state vs baseline") AND I built a mechanism story (frozen-actor-basis-break) with a confirming
  G_t — but independent cross-family review + a bit-exact replay audit proved it was an **RNG-desync ARTIFACT**: the
  adapted module (`_img_net`) was OFF the eval decision path, and the adaptation grad-steps consumed RNG (Gumbel
  rsample), breaking the CRN pairing → spurious return diff. → Before interpreting ANY surprising paired-comparison
  result: (a) confirm the intervention is ON the causal path to the measured outcome (not merely "a module changed");
  (b) confirm the effect survives RNG-controlled / bit-exact replay — **exp-verify's anti-no-op "state changed" is
  necessary but NOT sufficient for stochastic/gradient interventions in paired designs**; (c) route the INTERPRETATION
  (not just the run) to cross-family refutation BEFORE investing in the next step. Confirmation bias is highest when the
  result fits a pre-registered threat (here: "adaptation-false-negative"). Corollary to L5: even a KILL can be an
  artifact — verify the RESULT's validity, not just its direction.

- **L7 · PHENOMENON-MAGNITUDE GATE (2026-07-12, from 3 dead slices: adaptive-horizon, param-adaptation-scheduling,
  reliability-diagnostic).** All three died on MARGINAL phenomena (effect sizes ~0.4–0.5%; AUROC lifts ~0) against strong
  incumbents. Chasing a marginal effect in a crowded incumbent field is low-yield — the effect is too small to beat
  baselines OR to survive occupancy. → Before investing in a decision-relevant claim, add a SUBSTRATE-ADEQUACY / phenomenon-
  magnitude pre-check: does the substrate produce a LARGE, STRUCTURED effect to explain (not marginal)? A large headroom
  prior (e.g. DALI's +96.4% for context) is worth more than a defensible-but-tiny seam. Pair with L2 (phenomenon≠recipe):
  a phenomenon must be both REAL and LARGE before the recipe question is worth the compute. Corollary: DMC/CARL small
  dynamics-shifts generate only mild decision-gaps → inadequate substrate for a reliability-under-shift claim.

- **L8 · SUBSTRATE-GOAL-VARIANCE GATE (2026-07-12, the root cause of all 4 dead slices).** A decision-relevant
  context/value/uncertainty claim needs a substrate whose OPTIMAL POLICY actually DIFFERS by context — not one where the
  shift merely makes the SAME goal harder. DMC LOCOMOTION (walker/cheetah "walk/run forward") has a context-INVARIANT
  goal: gravity/mass shift changes difficulty, never which action is best → no decision-relevant context/value lever
  exists (the decision-bifurcation gate found a real but sub-threshold, decision-INERT context effect; BIF high yet
  wrong-context regret ~0). This is WHY every dynamics-side slice died: not bad luck, a substrate mismatch. → Before a
  context/decision claim, GATE the substrate: does the optimal action CHANGE with the context/goal? Substrates that pass:
  reacher (target position varies per episode — the goal itself changes), manipulation (object/task varies),
  sign-flipped/multimodal-reward-per-context tasks. Pairs with L7 (magnitude) + the failure-mode-first manual lesson #3:
  pick the substrate from where the model's OPTIMAL BEHAVIOR is context-sensitive, grounded in an own-run anomaly.

- **L9 · MODE-vs-SAMPLE before a "policy under-exploits" claim (2026-07-12, reacher_subtle post-mortem).** The
  reacher_subtle 543↔916 instability looked like a decision-utilization gap (target decodable R²=0.97 yet reach fails),
  but the DETERMINISTIC actor MODE is near-oracle (95%) — the failures are stochastic ACTION-SAMPLING at eval, not a
  policy dead zone (mode_failures=0). → Before claiming "the policy fails to exploit a sufficient representation," always
  evaluate the deterministic MODE + decompose mode-vs-sample. Stochastic-actor eval noise MIMICS a utilization gap on
  precision tasks. Pairs with L7 (magnitude) + L8 (goal-variance): an own-run anomaly can be a mundane eval-protocol
  artifact — verify the phenomenon is in the deterministic policy, not the sampling.

- **L10 · SUBSTRATE-REPLAY-DETERMINISM GATE before any snapshot-rollout / paired-counterfactual probe (2026-07-12,
  from the ManiSkill2 PickYCB contact-rerank blocker).** The J12 probe (oracle candidate rescoring via
  set_state→rollout→restore, + a bit-exact paired-arm design) silently ASSUMES the sim replays deterministically in
  CLOSED LOOP. It does not: ManiSkill2/SAPIEN PickYCB is deterministic for FIXED action sequences (~1e-8) but a frozen
  policy run twice on the same seed FLIPS success 4/10 — ~1e-7 GPU/sim float noise amplifies chaotically through
  contact dynamics + the closed-loop planner. torch deterministic-algos + CUBLAS_WORKSPACE_CONFIG do NOT fix it. The
  reproduce-gate's "set_state bit-identical" was validated on ONE step, not an episode. → BEFORE designing any probe
  that relies on trajectory reproducibility (paired counterfactuals, snapshot-restore rescoring, bit-exact no-op
  gates), run the cheap CLOSED-LOOP determinism check FIRST: same policy + same seed twice → does SUCCESS agree? If
  not, the substrate forces a STATISTICAL design (large-N two-proportion + a placebo control for the chaos-reroll),
  or a switch to a bit-deterministic sim (Mujoco: DMC/Meta-World replay exactly; SAPIEN/Isaac contact sims often do
  not). Corollary to L6 (verify-causal) + the reproduce-first gate: "reproduces the aggregate number" (72% over 25
  eps) does NOT imply "replays a single trajectory" — they are different guarantees, and snapshot-probes need the
  latter. Add this check to the reproduce gate for any contact-rich / GPU-physics substrate.

## Calibration summary (recomputed from resolved rows — never from memory)

| basis | n resolved | mean Brier | bias direction |
|---|---|---|---|
| (no rows resolved yet — first resolutions land at activation: J1/J2 at 精读, J3–J5 at Phase-1/Week-1) | — | — | — |
