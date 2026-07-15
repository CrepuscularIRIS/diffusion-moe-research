# WorldModel/ — the ACTIVE direction's knowledge layer (operators + tricks + strategy)

> **STATUS: ACTIVE (direction adopted 2026-07-12; venues = Information Sciences + AAAI).**
> This folder is the WM-domain instantiation of the research-os knowledge layer:
> `/prospect`/`/forge`/`/prereg` retrieve from it domain-first (`opus-pass/operators.md` is the general
> fallback). At campaign open, domain operator rows stage per convention at
> `openbuild/<campaign>/atlas/operators.md`, seeded FROM here; strong rows later promote to
> `opus-pass/operators.md`. Plan-of-record = `plan/world-model-direction-2026-07-11.md`; operational
> strategy = `plan/world-model-strategy-digest-2026-07-11.md`. Compute is PRICED per launch, never
> hard-capped (`.claude/CLAUDE.md` §0.2).

## File index (retrieval wiring)

| File | What it is | Which gate reads it |
|---|---|---|
| `wm-operator-bank-report.md` | **THE CANONICAL WM OPERATOR BANK** — full corrosion audit of the 45 opus-pass cards for WM (repo-verified 2026-07-11): 5 top-tier cards w/ full schema + kill criteria (§D), 20-signature failure map (§B), dedup map (§F), 7 new WM anti-patterns (§G), repo implementation table w/ verified code seams (§H), two-GPU Week-1/Week-2 generation-test plan (§I), venue routing (§J), retrieval index (§K) | `/forge` (retrieve 1–3 cards by failure signature via §K — never read all cards) · `/prospect` (candidate set + §I probe plan) · `/autopsy` (§B signature map) |
| `Trick.md` | WM adaptation of the diagnostic-trick catalog (`plan/taste-bank/` counterpart): 20 oracle/intervention families, terminology map, top-12 ranked strategy table, **the Bottleneck Panel (8 experiments, ~1 wk, 3 idea-killers)**, confound warnings | `/prereg` + every cheap-probe design · `/exp-verify` (confound checklist) · Day-0 harness validation |
| `Operators.md` | First-pass audit (independent second opinion, same brief). Superseded by the report where they disagree, but kept as the cross-check substrate — convergence between the two audits = confidence signal | dispute-map reference only |
| `deep-research-report (4).md` | Topic-selection deep-research source → distilled at `plan/world-model-strategy-digest-2026-07-11.md` | strategy layer (venue/route/compute) |

## Reconciled verdict (Opus dispute-map across the three externals, 2026-07-11)

**CONVERGENT (2–3 independent sources agree — high confidence):**
- **Top-tier WM operators (both audits):** `transition-family-factorization` (rewritten context-ization; absorbs invariant + operator-lifting) · `model-exploitability-objectization` (policy-conditioned error G replaces average loss — names the central WM pathology, sigs 2/10/11) · `policy-ranking-ization` (ordinal plan-order preservation; must beat value-equivalence in its pre-registered dissociation or die) · `belief-ization` rewritten (uncertainty must be decision-load-bearing; 2×2 ablation) · `event-triggered-re-anchoring` (innovation-gated replan/re-anchor; Trick.md's Route-A pick AND the report's best low-compute AAAI route).
- **`oracle-factorization-of-WM-errors` = standing META protocol** (component-swap bottleneck profile) — the bank's first move on any unexplained closed-loop failure; a probe/headroom instrument, NEVER a method claim.
- **Kills for WM (both audits):** bits-back-refund-pricing (the RSSM ELBO *is* the incumbent), chunk-ization, graph-ization, distribution-output-ization, polarization-ization. The bank SHRANK: 45 → 5 top + ~8 mid/meta — as required.
- **Information Fusion venue = narrow conditional-go only** in exactly one honest form: reliability/recoverability-modeled fusion of heterogeneous predictive evidence (STEVE-lineage multi-horizon value estimates + ensemble members + genuinely distinct sensor streams). Multiple heads on one latent / posterior-update-as-fusion = scope inflation, do not submit. Consistent with the strategy digest's IF default NO-GO.
- **All Week-1 probes are frozen-checkpoint / eval-time / logging-only** — ≤1 GPU-day each, piggyback on the Phase-1 reproduction runs' checkpoints. No new module before probes decide.

**DISPUTED → RESOLVED:**
1. **⚠ CAWM-H (uncertainty-adaptive imagination horizon) — the strategy digest's Route-A main design — is SATURATED.** Neubay (arXiv 2512.04341) makes uncertainty-quantile truncation its decisive component; ELVIS (arXiv 2605.04709) does uncertainty-triggered soft truncation for visual latent MPC. The report records `adaptive-horizon-as-novelty` as anti-pattern #1. **Resolution: adaptive horizon = incumbent/ablation arm, not the contribution. The Route-A slice shifts to event-triggered-re-anchoring** (when to LOOK/replan — open per AdaJEPA future-work note, arXiv 2606.32026) **or exploitability/context, decided by the Week-1 probes.** Re-run the saturation search at submission time.
2. **Primary direction:** first audit says exploitability-on-TD-MPC2; report says transition-family-factorization (w/ G-monitor instrumented throughout), event-triggered takes the slot if probes invert. **Resolution: don't pick by taste — §I's Week-1 three-probe decision gate picks empirically** (kill criteria pre-registered in the cards). This IS the research-os uncertainty-first SELECT.
3. **Repo facts:** Trick.md has a Jan-2026 knowledge cutoff and did not know R2-Dreamer (guessed R2I). **Resolution: the report's §H table ([repo] = verified by download 2026-07-11) is authoritative for code seams**; Trick.md remains authoritative for the diagnostic taxonomy, confounds (esp. naïve oracle-latent-injection interface mismatch — always pair injection with probing, report zero-shot AND adapter-tuned), and the Bottleneck Panel design.

## Week-1 probe plan (from report §I — runs INSIDE Phase-1 STEP-ZERO, not after)
GPU-A trains 2–3 TD-MPC2 ckpts (walker-run, quadruped-walk, 1 Meta-World) · GPU-B trains R2-Dreamer(rep_loss=dreamer) Memory-Maze-9×9 + 1 DMC-vision, ckpt every 100k. In parallel, three frozen probes w/ pre-registered kills: **(1) exploitability G(t) vs loss(t)** — demote to META if |partial corr(G, Δreturn | loss)| < 0.1; **(2) event-trigger threshold sweep** (eval-only wrapper on TD-MPC2) — kill if <40% planner-call cut at ≤2% return loss or triggers temporally uniform; **(3) context inference-gap** (param-modified DMC, frozen-encoder probe + oracle-context inject) — demote if oracle gap <2% on all 3 tasks. **Week-2 = decision gate:** rank survivors by measured headroom, commit both GPUs to the winner's minimal method; runner-up becomes the paper's diagnostic section. A probe that dies is banked as negative evidence, never re-tuned.

## Discipline flags
- Probes are `/prereg`'d (kill criteria are already written in the cards — carry them verbatim).
- Day-0 precondition = Trick.md's harness validation (deterministic replay, action-repeat/frame-stack audit, random-policy + scripted-oracle scores, reward/termination recomputation) — never skip; harness bugs are first-order.
- Anti-patterns §G are live `/forge` gates: adaptive-horizon-as-novelty · KL-refund-relabeling · ensemble-equals-belief · context-as-task-ID · representation-objective-swap-without-decision-differential · prediction-loss-as-decision-evidence · oracle-result-as-method.
- Citation caveat: 2026-numbered arXiv IDs in all three files are triage leads — verify locally (精读) before any anchors a design or a novelty claim.
