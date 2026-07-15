# Judgment Lessons — curated calibration priors (the evolving layer)

> Operations + curation = the research-os `ledger` skill. **APPLY these as explicit corrections when
> writing any new forecast** (state the correction: "raw 0.7 → L2 caps at 0.4"). Recall at goal-start +
> before every claim-bearing `/forge`. Curated 2026-07-13: L7 (substrate & phenomenon pre-flight, merged
> from the old pre-2026-07-13 numbering's L7–L10 — NOT today's L9/L10) unchanged; **L8**
> (positivity/MNAR in pre-registered estimands) added from the v4→v5 contact-mode estimand-chain
> (J11/J12). **L9 (independent adversary catches proposer overclaim) + L10 (eliminative-only =
> pseudo-depth; definition-first) added 2026-07-14** from the world-model-v2 adversary + W5 human
> ruling. Originals preserved in `plan/archive/pre-researchos-v2-2026-07-12/lessons.md`; evidence rows
> in `ledger-archive.md`.

## Priors (apply to new forecasts)

- **L1 · FEASIBILITY OPTIMISM (direction-level).** Every 2026 campaign that reached a close died a
  feasibility death knowable at selection — historical P(direction survives to a method-win | selected
  without cheap feasibility evidence) ≈ 0/5. → Direction-level survival forecasts start ≤0.3 absent
  MEASURED evidence; each passed empirical gate (reproduce gate, probe-verified phenomenon) is what
  raises them (J4 showed a verified-by-download repo deserved >0.6).

- **L2 · PHENOMENON ≠ RECIPE (mechanism-conversion).** Phenomenon verified real ≠ first cure works
  (optical-SAR: implicit ~0.7 forecast, outcome 0; J7 confirmed the pattern — prediction gains don't
  route to decisions). → P(first mechanism recipe works | phenomenon real) capped at 0.4 until a cheap
  probe shows the mechanism ROUTES the signal (not merely correlates with it).

- **L3 · FIRST-CONTACT COST — SETUP ONLY, never steady-state.** New envs/repos overrun early estimates
  (dependency pins, dead downloads, fresh-repo debugging) → multiply SETUP/DEBUG ETA ×1.5–2 and widen
  UPWARD. But steady-state throughput is MEASURED, never multiplied: J5 conflated the two and priced a
  measured-3h run at 20h (6.5× over). Always run the 60s timing probe; price training wall-clock only
  from measured sec/step.

- **L4 · TRIAGE ≠ TRUTH (occupancy calls).** External-brain/search citations — especially future-dated
  arXiv IDs — are triage-grade with nonzero fabrication/inflation risk. → Occupancy/saturation forecasts
  cap at 0.85 until local 精读 (J1: the abstract even seemed to CONTRADICT the true occupancy); a
  novelty-OPEN call additionally decays toward submission time.

- **L5 · KILLS ARE BETTER-CALIBRATED THAN BUILDS.** Negative judgments (kill-probes, region-closes)
  keep being confirmed; positive build bets underperform (L1, L2; J7–J10 all died as forecast-low).
  → Asymmetric trust: a pipeline KILL at p≥0.8 is actionable; a pipeline BUILD at p≥0.8 still wants the
  cheap probe first.

- **L6 · VERIFY-THE-RESULT-IS-CAUSAL, not just executed.** A surprising DOWN passed structural
  exp-verify yet was an RNG-desync ARTIFACT (adapted module off the act-path; grad-steps consumed RNG,
  breaking CRN pairing). → Before interpreting ANY surprising paired result (including a kill):
  (a) intervention ON the causal path; (b) survives RNG-controlled / bit-exact replay; (c) route the
  INTERPRETATION to cross-family refutation first. Confirmation bias peaks when the result fits a
  pre-registered threat. (Now codified as `/exp-verify`'s surprising-result extension.)

- **L7 · SUBSTRATE & PHENOMENON PRE-FLIGHT (merged L7+L8+L9+L10 — the root cause of the four dead DMC
  slices).** Before investing in any decision-relevant claim, gate the SUBSTRATE with four cheap checks:
  1. **Magnitude** — does the substrate produce a LARGE, structured effect (not a ~0.5% seam against
     strong incumbents)? A large headroom prior (e.g. DALI's +96.4% context gain) is worth more than a
     defensible-but-tiny gap. Marginal ⇒ low-yield for both baselines and occupancy.
  2. **Goal-variance** — does the OPTIMAL POLICY actually differ across the contexts/conditions of the
     claim? DMC locomotion's goal is context-invariant (shift makes the same goal harder, never changes
     which action is best) → no decision lever exists; reacher/manipulation (goal varies per episode)
     pass. This was WHY every dynamics-side slice died — substrate mismatch, not bad luck.
  3. **Mode-vs-sample** — before any "policy under-exploits its representation" claim, evaluate the
     deterministic MODE and decompose mode-vs-sampling: stochastic-actor eval noise MIMICS a utilization
     gap on precision tasks (reacher 543↔916 was sampling noise; mode was 95% of oracle).
  4. **Replay-determinism** — before any snapshot-rollout / paired-counterfactual probe, check the sim
     replays deterministically in CLOSED LOOP (same policy + seed twice → same success?). Contact/GPU
     physics sims often don't (ManiSkill2 flipped 4/10) → forces a statistical design or a
     bit-deterministic sim. "Reproduces the aggregate number" ≠ "replays a trajectory".
  Pair with L2: a phenomenon must be REAL and LARGE and HOSTED BY the substrate before the recipe
  question is worth compute.

- **L8 · POSITIVITY / MNAR IN PRE-REGISTERED ESTIMANDS.** A pre-registered gate can itself carry a
  structural positivity failure — the v4 contact-mode episode-FE statistic was blind to 31/37 episodes
  (no far-free bucket in contact-dense engaged episodes where the mechanism lives; MNAR = the positivity
  hole is shaped like the signal). "Masked-positive-shaped hole ≠ clean negative" — never region-close
  on a known-bad measurement. → Freeze a POSITIVITY CHECK (all strata populated, no structural MNAR)
  alongside the decision rule; declare the estimand TERMINAL to prevent infinite re-cut; pre-register
  the replacement estimand before re-running after a post-hoc-bucket death. (v4→v5 defect-correction
  chain; codex refutation decisive; J11/J12.)

- **L9 · THE PROPOSER UNDER-DETECTS ITS OWN OVERCLAIM; THE INDEPENDENT ADVERSARY CATCHES 1–2 MORE LEVELS.**
  On world-model-v2, a careful SELF-administered `/adversary` pass (I scoped the claim to "locomotion" +
  flagged the non-universal cliff) STILL overclaimed — the independent cross-family reviewer (Grok, cold
  packet + real JSONs) returned NARROW-TO on S1–S5: the "accuracy inversion" rested on accuracy measured on
  the WRONG distribution (real trajectories, not the planner-query latents), the "mechanism" was thin
  (2–3 cells), and the fair baseline (a value adaptation that does NOT collapse) already sat in my own repo.
  A parallel venue-lane consult was POSITIVE (PURSUE-IF) — but the venue lane has pro-framing bias (esp. if
  it generated the framing), so it does NOT substitute for the refute-framed independent lane. → Run the
  independent adversary EARLY (before drafting), give it a cold packet + the raw artifacts (not the framing),
  and treat its DOWN as BINDING even when a venue consult is positive. Self-scoping ≈ one level short of the
  honest scope; budget for it. (Adversary gate, node 5.7.)

- **L10 · ELIMINATIVE-ONLY CHARACTERIZATION = PSEUDO-DEPTH (definition-first).** The WM-v2 draft
  isolated its cause against three named confounds (accuracy · scale/temperature · OOD) with genuinely
  rigorous experiments — and was still ruled below the top-tier bar (HUMAN, 2026-07-14, row W5): the
  central construct ("consistency") was named dozens of times and DEFINED zero times — no formula, no
  computable metric, no decision rule. Elimination establishes what the cause is NOT; only a computable
  definition gives leverage (prediction, sufficiency construction, principled mitigation, theory link).
  → Before a characterization claim leaves the loop, the named cause must exist as an INDEX (formula +
  threshold + decision rule), validated by RETRODICTION on the elimination experiments themselves, and
  pass the **five-minute test**: a stranger can predict the phenomenon on a NEW instance from cheap
  measurements without re-running the full closed loop. No index ⇒ the mechanism sentence is an
  interpretation, not a contribution. (Corollary: the elimination experiments are not wasted — they
  reinterpret as measurements of the index once it exists.) **W6 refinement — the two completion
  states:** EVIDENCE-COMPLETE (phenomenon + mechanism reliably characterized) ≠ CONTRIBUTION-COMPLETE
  (a computable construct, held-out-validated predictor, or baseline-beating intervention exists);
  the loop's characteristic failure mode is optimizing rigor/falsification/honesty while producing no
  new positive capability — files ever more rigorous, claims ever more conservative, nothing built.
  "All experiments finished" is never a completion criterion; writing unlocks at package P≥~0.85.
  **Algorithm-path corollary (user ruling 2026-07-14, dual-path):** for a Method-repair claim the
  "index" obligation is discharged by {the failure mechanism stated as a measurable quantity + the
  fix's ablation restoring the diagnosed failure} — an update-rule fix is NOT additionally required to
  mint a standalone index/object. L10 guards against undefined constructs, not against algorithm-path
  work; do not let the index demand force every candidate into an object-production narrative.

## Calibration summary (recomputed from resolved rows — never from memory)

| basis | n resolved | mean Brier | bias direction |
|---|---|---|---|
| OCCUPANCY (J1, J2-partial, J6-partial) | 2 | ~0.07 | well-calibrated; slight under-confidence when triage is double-sourced |
| SELECT/BUILD (J3, J4, J8, J9, J10, J11) | 6 | ~0.16 | builds die as forecast; L1/L2 corrections work on INDIVIDUAL probes — J3 outlier (0.49) from correlated-OR pricing; when probes share a substrate, price the aggregate DOWN |
| PREREG (J7, J12) | 2 | ~0.06 | well-calibrated low; L2 phenomenon≠recipe cap is the binding prior |
| COST (J5) | 1 | 0.36 | conflated setup with steady-state → fixed in L3; re-measure at next new substrate |
