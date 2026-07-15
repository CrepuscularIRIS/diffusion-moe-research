# Optical-SAR / BRIGHT-DFC25 — Culminating Verdict & Decision Brief (2026-07-11)

> Status: the full disciplined pipeline ran end-to-end on pre-registered criteria and produced a clean,
> well-characterized **negative screening result**. The first GPU-trained cure works DIRECTIONALLY but FAILS
> the screening bar. Everything banked/gated/exp-verified (tree 2.1–2.5, RUNLOG + memory current, 7
> external-brain sessions in `openbuild/optical_sar/pro/`). GPUs free. **Next fork = the user's call.**

## The pipeline that ran (all pre-registered)
reproduce → phenomenon → post-hoc kill → reframe → cheap gate → `/prereg` → GPU train → held-out eval.

## Result — real phenomenon, directionally-confirmed mechanism, sub-bar magnitude
- **Phenomenon real:** the BRIGHT baseline shows textbook **modality collapse** — real SAR HURTS
  (U_SAR −0.020, log-odds −1.42, ~zero damage on the held-out Noto event).
- **Cure moves every SAR-utility metric the right way:** U_SAR −0.020 → +0.001 · log-odds −1.42 → −0.86 ·
  severe-F1 ×8.6. The stochastic modality-sufficiency masking recipe (15k iters, budget-matched) works, but
  **barely dents the collapse**.
- **KILL vs frozen criteria:** U_SAR = +0.001 (CI includes 0; bar ≥0.05); severe-F1 0.012 (bar ≥0.15);
  log-odds still negative.

## The decisive diagnostic — recipe-insufficient, not underpowered
Cured-UNet severe-AP on real SAR = **0.134 ≤ Noto prevalence 0.146**, while a **logistic regression on
hand-crafted SAR features scored 0.276** (the node-2.4 gate). The trained network is NOT extracting a SAR
signal that even a linear classifier can → **input-masking does not route SAR into the damage decision.**
This points to *recipe-insufficient* (the head overrides SAR), not merely *needs-more-iters*.

## The fork (consequential — user's decision)
| Option | Read |
|---|---|
| **(a) Longer 50k run** (decoded-tile caching) | Skeptical — below-prevalence AP argues the ceiling is not iters. |
| **(b) Stronger routing recipe** (SAR-gating architecture / auxiliary SAR-damage head, not just input masking) | **Most promising** — the mechanism is real; it needs a design that FORCES SAR into the decision. |
| **(c) Escalate substrate** (audit §4: pre/post SAR, polarization/incidence metadata, another modality pair) | Fallback if (b) also fails. |

Also on deck from earlier nodes: the **latent-space Option B** (node 2.3) — SAR reaches the latents
(input-gradient γ≈0.6) but is overridden at the head; a no-retrain latent operator was left LIVE-but-unconfirmed.

## What is banked
Tree nodes 2.1–2.5 all `/exp-verify` VERIFIED · `openbuild/optical_sar/RUNLOG.md` (2026-07-11 tail) ·
`PREREG_cure_train_node2.5.md` · scripts `repro_logs/cure_run/` · 7 external-brain reads in `pro/`.
Reproduction anchor is honest and exact (standard_ML mIoU 64.94, Δ=0.00 vs paper Tables 5/6/10).

## Honest framing
Even if the cure needs more work, the **modality-collapse phenomenon + its favorable-but-weak cure are now
rigorously evidenced** — a real diagnosis, and a genuine foundation for a proper method IF a stronger routing
recipe lands. The user is treating this direction as walled; recorded as such pending their decision.
