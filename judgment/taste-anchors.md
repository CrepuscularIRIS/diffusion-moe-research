# Taste anchors — calibration exemplars for problem generation + the selection jury

> Read by `/prospect` (fed verbatim to every generator instance AND to the JURY-MODE panel).
> Contract: 3–5 GOOD cards (venue-proven problems, distilled to the four fields + one WHY-GREAT
> line) + ~3 BAD cards (our own autopsied kills, with the extraction row's reason). Sanity rule: a
> jury/rubric that ranks a BAD anchor above a GOOD one is VOID — rewrite the prompt, don't trust the
> round. Curated by the `ledger` pulse: replace a GOOD anchor when a better exemplar lands (incl.
> our own CLAIM_STANDS results); append a BAD anchor at each region-close whose kill was foreseeable
> at carding time. Seeded 2026-07-14; anchors are EXEMPLARS of problem-shape, not literature claims.

## GOOD (what a great problem card looks like — note each came from a DIFFERENT mine)

**G1 — enabling-delta mine (Dreamer-class, "train in imagination").**
- Q: Can gradients through a learned latent world model replace real environment interaction for
  learning control?
- WHY-NOW: latent dynamics models had JUST crossed the fidelity where multi-step imagination stops
  diverging — the capability delta made a previously-dead idea live.
- PROBE/KILL: one task, fixed model, compare imagination-trained vs replay-trained policy at equal
  wall-clock — both outcomes decisive.
- STAKES: changes how anyone with an expensive simulator/robot allocates samples.
- WHY-GREAT: the card is TIMING, not cleverness — the question was old, the enabling condition was
  new; magnitude was order-of-magnitude (sample efficiency), not a margin.

**G2 — contradiction mine (deep double descent).**
- Q: Does test error rise then FALL again past the interpolation threshold — contradicting the
  bias-variance curve every textbook teaches?
- WHY-NOW: two credible literatures (classical statistics vs modern over-parameterized practice)
  could not both be true, and compute had just made the sweep cheap.
- PROBE/KILL: width/data sweeps on standard benchmarks — no new method, pure measurement, surprise
  in either direction publishes.
- STAKES: changes model-size and regularization decisions for every practitioner.
- WHY-GREAT: it attacked a SHARED SILENT ASSUMPTION with a measurement anyone could have run for a
  decade; taste = noticing the contradiction, not building the apparatus.

**G3 — untested-assumption mine (does BatchNorm work via internal covariate shift?).**
- Q: Is the mechanism everyone cites for a ubiquitous method actually the mechanism?
- WHY-NOW: the assumption had hardened into textbook fact with zero direct tests, while the method
  sat in every pipeline — maximal exposure, zero scrutiny.
- PROBE/KILL: inject the alleged cause (noise reintroducing covariate shift) while keeping the
  method — if performance survives, the story dies; a mechanism-level loss-landscape measurement
  replaces it.
- STAKES: redirects an entire line of "reduce covariate shift" method design.
- WHY-GREAT: cheapest possible intervention (one counterfactual injection), aimed at the HIGHEST-
  traffic assumption in the field — stakes ÷ probe-cost near the maximum.

**G4 — incumbent-algorithm-autopsy mine (Double Q-learning, diagnose→minimal-fix).**
- Q: Why does Q-learning systematically OVERESTIMATE action values — and what is the smallest
  structural change to the update rule that removes the diagnosed bias?
- WHY-NOW: the max-operator's positive bias under noisy estimates was derivable from the update rule
  itself (Jensen: E[max] ≥ max[E]) — a structural flaw sitting in the field's most-used algorithm, no
  new phenomenon or dataset needed.
- PROBE/KILL: measure the bias directly on a known-answer toy MDP (estimator vs true Q*); the fix —
  decouple selection from evaluation across two estimators — must remove the measured bias AND
  ablating the decoupling must restore it.
- STAKES: every DQN-descendant changed its update rule; the diagnosis predicted WHERE the fix pays
  (high-variance, many-action regimes) before any benchmark run.
- WHY-GREAT: the fix is one line; the contribution is the DIAGNOSIS that predicts the fix's gain —
  algorithm-path, object unchanged, no new construct minted. The card asks "given what we already
  model, why does the current algorithm fail?" — the co-equal twin of G1–G3's object questions.

## BAD (our own kills that were foreseeable at carding time — the shapes to not regenerate)

**B1 — marginal-magnitude vs strong incumbent (J6, event-triggered WM param-adaptation).**
Card looked novel ("selective scheduling of adaptation"), but the phenomenon's measured size was
Δ≈+0.7 return against an always-adapt incumbent — a margin, not a mechanism. Died at the
operator-strength sweep (ceiling). LESSON (L7): a card whose MAGNITUDE clause reads "small but
consistent" against a tuned incumbent is priced to the bottom at BIRTH, not after two weeks.

**B2 — occupied niche mis-read as gap (J1, adaptive-horizon truncation).**
The "gap" was three papers deep (ELVIS · Neubay · Frauenknecht) — visible in one occupancy triage
that was run only AFTER investment. LESSON: WHY-NOW without an occupancy annotation is a hope, not
a field-state; annotate before the jury, not after the kill.

**B3 — phenomenon that cannot become a recipe (contact-mode localization, node 5.1).**
The onset-aligned regret spike was REAL (5×) but not sparse-exploitable — the card conflated
"effect exists" with "effect converts to a decision-change". Died after v3→v4→v5 estimand churn.
LESSON (L2): the STAKES field must name the conversion step (who exploits the phenomenon, HOW);
"localization exists" is a diagnosis card, not an intervention card — type it honestly at birth.

**B4 — eliminative characterization with an undefined construct (WM-v2 draft, 2026-07-14).**
Three-layer confound isolation, teacher-forcing crossover, rank-normalization, rollout audits — deep,
rigorous, and HOLLOW: the causal construct ("consistency") was never given a formula, metric, or
decision rule, so the work had no leverage (no prediction, no sufficiency test, no principled fix) and
was ruled below the top-tier bar by the human (row W5). LESSON (L10): a card/claim whose mechanism
noun cannot be written as a computable index by claim time is a characterization CEILING, priced as
such at birth; the STAKES field should name the index the work will produce, not just the decision it
changes.
