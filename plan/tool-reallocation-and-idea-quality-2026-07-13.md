# Tool reallocation (DONE, v4.1) + idea-quality redesign (IMPLEMENTED 2026-07-14, v4.2) — 2026-07-13/14

> Three parts. **§1 = implemented 2026-07-13** (user-decided rebindings, research-os v4.1).
> **§2 = RESOLVED 2026-07-14** (user decision: Grok = repair/debug specialist complementing Sonnet;
> replacement REJECTED). **§3 = the idea-quality redesign — IMPLEMENTED 2026-07-14 as research-os
> v4.2 on the user's explicit "follow your idea" instruction** (grounded in the ARIS deep-read at
> `/home/lingxufeng/research/Auto-claude-code-research-in-sleep`), plus §4 (2026-07-14 addendum):
> the Brain.md audit adjudication, the phantom-panel fix, the cross-domain mine, and the
> core-component evaluation. Temporal-decoupling
> (`plan/research-os-temporal-decoupling-design-2026-07-13.md`) remains the one PARKED design.

## 1. External-tool reallocation — IMPLEMENTED (research-os v4.1.0, runtime synced)

| Change | Where |
|---|---|
| **Codex REMOVED from the MoA panel.** Panel = 5 families: opus46 · gemini (AGY Gemini 3.1 Pro) · deepseek (DSV4 Pro) · mimo (MiMo V2.5 Pro) · qwen (Qwen 3.7 Plus). | `moa/moa_panel.sh`, `moa/router-protocol.md` |
| **Multi-instance differentiated parallelism** replaces the lost breadth: default opus46×3 · gemini×5 · deepseek×3 · mimo×3 · qwen×3 (~17 instances). Per-instance prompt files `<lane>-<k>.txt`; every instance gets a distinct {operator × lens × dropout × STANCE}; quorum counts FAMILIES (≥4), never instances; within-family convergence discounted at reconcile ("one prior speaking twice"). | `moa_panel.sh` (parser + quorum), `moa-routing.md` §3b + reconcile |
| **Codex = FORENSIC lane** — `/autopsy` + `/abduce` consults only (its strength: subtle hidden errors). Fired single-shot via `moa_ask.sh gpt5`; the panel script rejects it. | `moa_ask.sh` header, `moa_panel.sh`, `router-protocol.md` |
| **Grok scope extended:** independent reviewer (claims) **+ implementation reviewer during experiment development** — function-logic / control-flow / silent-bug review of executor code routes to `grok review` / `adversarial-review` (cross-family eyes on same-family code). | `router-protocol.md`, CLAUDE.md §2 |
| **Chrome Extension (GPT-5.6 browser) unchanged**: review + search — novelty/duplication/similarity triage + live arXiv browser search (preferred over API-only scholar lookups). | CLAUDE.md §2 |
| **No-pause decision flow:** conductor §3 rewritten — (a) **named-resolver rule**: a step whose resolver a standing prereg/ledger row already names, crossing no human-reserved boundary, is NOT a fork — execute it (the quoted W2-replication episode is the type case); (b) genuine tactical forks → **MoA decides**, external brain checks novelty/occupancy, conductor reconciles + reports; human only for the short literal reserved list. | `conductor/SKILL.md` §3 + engine table, CLAUDE.md §2, goal-directive |

Verification: `bash -n` clean on all three scripts; live parse test — gpt5 file skipped with pointer,
6 instances / 5 families dispatched, `gemini-2`→gemini binding resolved; quorum-fail exits 3 at 2
families; shared-mode `gpt5` rejected. Runtime copies at `~/.claude/skills/conductor/` diff-identical.

## 2. PARKED proposal — Grok in the development lane (design only, DO NOT implement)

Motivation: Sonnet executors still make mistakes and are relatively slow. Two directions:

1. **Grok Composer as primary developer.** Potentially much faster. Cost: breaks the current
   context-isolation layout (executor worktree protocol, report contract, `operate` §ownership all
   assume native Agent subagents); Grok `task` is write-capable full-Bash — needs its own worktree +
   diff-review discipline before it can be trusted with executor volume. Migration test: give Grok
   Composer ONE bounded executor task per session (a probe implementation with a named covering
   test), diff-review with the current reviewer flow, and compare wall-clock + defect rate against a
   Sonnet baseline for ~5 tasks before any rebinding.
2. **Grok 4.5 as implementation reviewer only** (the conservative endpoint — §1 already binds this).
   Keep Sonnet as developer; Grok reviews every executor diff during the build stage.

Recommendation recorded, not decided: start with 2 (done), collect the defect-catch record in the
ledger, and run the direction-1 migration test only if implementation-review findings show Sonnet
defect rates staying high. Decision owner: user.

## 3. Idea-quality redesign — improve the DISTRIBUTION before the gates (v4.2 candidate)

### 3.1 Diagnosis — where the current SELECT loop loses quality

The v4.0 audit fixed *spend* (≈70% of sunk cost was rejectable at selection → `/admit`). But the
gates only **reject**; nothing upstream **raises** the distribution they sample from. Concretely:

- **D1 — the generator grades itself.** `prospect` ranks its own cards ("STAKES × plausibility ÷
  cost") and emits ONE recommended probe. By ARIS's Type-A/Type-B taxonomy (acceptance-gate.md:
  *"could a dumb script answer it? No → different model family"*), taste-ranking is a Type-B verdict
  being self-judged by the same family that generated — exactly the correlated-blind-spot failure the
  cross-family invariant exists to prevent. We enforce cross-family review at the CLAIM boundary but
  not at the SELECTION boundary, where (per our own audit) most value is decided.
- **D2 — cards die instead of evolving.** A card that fails pricing goes to the bottom or to
  `/autopsy`. There is no stage whose JOB is to make a promising-but-flawed card better before it
  meets the gate. (The aerial-VLN post-mortem — the coarse-belief rung that was never generated — is
  this gap at direction scale.)
- **D3 — generation is unconstrained by the acceptance predicate.** Generators don't see the six
  `/admit` checks or the venue bar at generation time, so a large fraction of cards are born
  failing checks that were knowable upfront (rejection sampling instead of constrained generation).
- **D4 — no empirical signal before ranking.** Ranking is prose-vs-prose; the cheap probes that
  would ground it run only after a card is already selected.
- **D5 — taste is asserted, never anchored.** No card is ever compared against exemplars of known
  good/bad problems, so "high taste" has no operational meaning at generation or triage time.

### 3.2 What ARIS demonstrably does about this (mined 2026-07-13; paths in the repo)

1. **Fan-out ≠ jury** (`shared-references/fan-out-pattern.md`): same-family subagents GENERATE only,
   mechanical dedup only (dedup_key clustering); ALL surviving candidates go to one cross-family
   devil's-advocate jury ("strongest objection · likely failure mode · is prior-work differentiable ·
   which 2-3 would YOU work on"). Generators never score.
2. **Annotation, not elimination** (`idea-creator/SKILL.md:242-250`): prior-work/novelty is attached
   as a NOTE for the jury, never used as a pre-filter — kills premature internal filtering (our own
   documented failure mode, value-bar ruling).
3. **Taste calibration with anchors** (`shared-references/taste-calibration.md`): named weighted
   axes + score 3 known-good / 3 known-bad exemplars FIRST; a rubric that ranks a bad exemplar above
   a good one is broken; mandatory GAP paragraph ("which exemplar does this fall short of, on which
   axis"). *"The model will not invent taste; it will only converge toward the taste you described."*
4. **Problem-anchored refinement loop** (`research-refine/SKILL.md`): freeze an immutable problem
   anchor, then refine method/specificity through cross-model review rounds until score ≥ threshold
   (≤5 rounds) — the stage whose job is IMPROVING the candidate.
5. **Micro-pilots re-rank before commitment** (`idea-creator` Phase 5): 1–2 h single-GPU pilots on
   the top 2-3; empirical signal outranks eloquence.
6. **Failed-idea banlist as generation INPUT** (`tools/research_wiki.py`): failed ideas are fed to
   the next generation round as "do not regenerate near-neighbors", not just archived.

### 3.3 The redesign — five moves, mapped to research-os

The through-line: **spend the new panel breadth on making 3 cards excellent, not 30 cards long.**

- **M1 — Cross-family SELECTION jury (fixes D1; ARIS 1+2).** `prospect` keeps generating (mines +
  PROBLEM-MODE multi-instance panel) but its self-ranking becomes ADVISORY. Mechanical steps stay
  local (dedup by question-slug, feasibility vs BINDINGS hardware). Then ONE reconciled
  devil's-advocate jury round — cross-family (external brain, or a 5-family panel round in
  judge-mode) — over the FULL annotated card set, occupancy annotated not pre-filtered. Jury output
  contract: per card {strongest objection · likeliest failure mode · prior-work differentiable? ·
  venue-plausible magnitude} + a forced "which 2-3 would you actually work on". Conductor reconciles;
  external-verdicts-are-candidates still governs (the jury ranks, the conductor SELECTs).
- **M2 — Taste anchors, both ends (fixes D5; ARIS 3).** New project-side bank
  `judgment/taste-anchors.md`: 3-5 GOOD problem cards distilled from high-impact papers in the live
  domain (each reduced to Q/WHY-NOW/PROBE/STAKES + one line on WHY it was a great problem) + 3 BAD
  cards from our own atlas/autopsies (with their extraction rows). Fed (a) to every generator
  instance as few-shot anchors, (b) to the M1 jury with the sanity rule: a rubric that ranks a bad
  anchor over a good one is void. Maintained by `ledger` curation; `prospect` Mine 2 reads it.
- **M3 — Constrained generation (fixes D3).** The generator brief carries the acceptance predicate:
  the six `/admit` check names + the venue bar + the 5-line project inventory (already mandated for
  panels) + the atlas banlist stated as "do NOT regenerate near-neighbors of these dead cards"
  (ARIS 6). Cards are born pre-priced; `/admit` stops being the first contact with reality.
- **M4 — REFINE pass: cards evolve before they meet the gate (fixes D2; ARIS 4).** For the jury's
  top 2-3 only: freeze the card's Q (immutable anchor), then 1-3 cross-family refinement rounds on
  WHY-NOW sharpness / probe design / differentiable-delta, each round forced to either strengthen a
  named weakness from the jury verdict or emit a relaxation rung (the autopsy ladder moved to
  BIRTH). Stop when the jury's strongest objection has a designed answer, or 3 rounds. Only then
  `/admit`.
- **M5 — Micro-pilot re-rank (fixes D4; ARIS 5).** Before `/admit`, run the top 2-3 cards' cheapest
  probes as a PARALLEL portfolio (hour-scale, free below the admit gate — this is also
  temporal-decoupling §3.3's probe-portfolio, same mechanism, one implementation). Empirical
  surprise re-ranks; a card whose probe lands enters `/admit` carrying its MAGNITUDE check
  pre-filled.

**What deliberately does NOT change:** the four gates and every honesty invariant; `/admit` stays
spend-gating; the venue review keeps the only drop authority; hunches stay free and ungated
(M1-M5 apply to direction-scale cards only — a hunch still skips everything).

### 3.4 Scope + files (for the v4.2 implementation pass)

`prospect/SKILL.md` (advisory-rank + jury step + constrained-brief fields + banlist line) ·
`conductor/references/moa-routing.md` (jury-mode output contract next to PROBLEM-MODE) ·
`conductor/SKILL.md` §1 (one line: selection jury before admit-scale commitment) · project-side
`judgment/taste-anchors.md` (new, seeded during the world-model-v2 campaign) · `ledger/SKILL.md`
(curate anchors at the pulse). Net +40-60 lines against the gates-not-scripts budget; no new gate —
M1/M4/M5 live in the free zone between prospect and admit. Implement together with the PARKED
temporal-decoupling design as v4.2, after the goal test; M5 needs no code at all and the conductor
may adopt it behaviorally in the current campaign (it is ordinary free-zone probing).

### 3.5 Honest counterpoints (recorded so v4.2 argues against something)

- ARIS validates 8-12 ideas/round with jury+pilots but has NO evidence its ideas clear top-venue
  bars (no acceptance record in the repo) — transplant the mechanisms, not the quality claim.
- M4's refinement rounds can polish a mediocre Q into eloquence without raising its ceiling — the
  immutable-anchor rule and the M5 empirical re-rank are the guards; if a refined card's probe still
  lands nothing, refinement stops (no 4th round, ever).
- More machinery between prospect and admit re-grows ceremony v4.0 just cut — hence: no new gate, no
  new artifact except the anchors bank, all of M1/M4/M5 expressible as conductor free-reasoning
  moves with ≤15 lines of skill text each.

## 4. Addendum 2026-07-14 — implementation record + Brain.md adjudication + component evaluation

### 4.1 What shipped as v4.2 (runtime synced)
M1–M5 all live: `prospect/SKILL.md` rewritten (selection invariant · constrained generation brief ·
**Mine 6 CROSS-DOMAIN INTERPOLATION** · dedup→jury→refine→pilot→exit select section);
`moa-routing.md` gained **JURY-MODE** (devil's-advocate contract, stance-differentiated lanes,
anchor sanity check) and reconstruction-mode now also takes vocabulary-stripped obstruction SHAPES
from Mine 6; `judgment/taste-anchors.md` SEEDED (G1 enabling-delta/Dreamer · G2 contradiction/double-
descent · G3 untested-assumption/BatchNorm + B1 J6-marginal-magnitude · B2 J1-occupied-niche ·
B3 contact-mode-phenomenon≠recipe); `ledger/SKILL.md` curates the anchors at the pulse; conductor
routes through the jury (§5 line). Mine 6 is the direct answer to "poor at cross-domain
interpolation": import (obstruction-shape → which field solved this shape → RECONSTRUCTION-MODE
panel) + export (capability bank → adjacent field's open problem), with the guard that transfer
machinery must carry a DIFF-PREDICTION or it is vocabulary.

### 4.2 Brain.md (independent allocation audit) — adjudicated
- **"MoA breadth is fictional" — CONFIRMED and fixed.** Live probe found gemini (agy model-id rot:
  `gemini-3.1-pro` → display-name ids) and gpt5 (codex cwd-trust + stdin) both DEAD. Fixed in
  `moa_ask.sh`; **NEW `moa/moa_ping.sh`** mechanizes the liveness precheck (exit 3 below family
  quorum); `moa_panel.sh` now reports post-run how many families actually ANSWERED and warns on a
  degraded round. All 6 lanes verified LIVE (5 panel + forensic), incl. dash-leading-prompt cases.
- **"GPT-5.6 overloaded / independence leak" — partially pre-existing, now sharpened.** The
  refiner≠reviewer firewall already existed (external-brain role separation); role 3 is now
  explicitly EVENT-TRIGGERED (claim-bearing stakes only) with routine design iteration pushed back
  to the conductor+banks, concentrating the browser lane on its two proven-leverage jobs (occupancy
  triage, mechanism refutation).
- **"Grok right but untested"** — stands; the ledger should collect Grok adjudication outcomes as
  they occur (no mechanism change needed — verdicts already get rows).

### 4.3 Core-component evaluation (Arbor · MoA · Tricks · Lessons · Ledger · Operators)
- **MoA** — was the weakest link (phantom panels); fixed above + jury-mode gives it a second
  distinct job (selection) matching its structure (cross-family taste).
- **Ledger/Lessons** — strong and demonstrably load-bearing (W1 Brier 0.04, W2 0.16; L-priors
  visibly correcting forecasts in `basis`). Added only anchor-curation; no structural change.
- **Tricks** — healthy (v5 sparse-spike redesign came straight from the palette). No change.
- **Operators/taste-bank** — healthy as retrieval data; the taste-anchors bank now covers the
  PROBLEM-shape axis the operator bank (mechanism-shape) never did — complementary, not duplicate.
- **Arbor** — adequate as canonical backlog + constraint memory; the jury/pilot verdicts write to
  node insights (no schema change). Deliberately NOT extended: a tree-side "idea-quality score"
  field would re-grow gateable-artifact pressure (ledger gate-pressure check).
- **Deliberately not done:** no new gate; no scoring rubric numbers (anchors are exemplars, not a
  0-1 scale — ARIS's weighted axes invite metric-gaming our adversary gate exists to kill);
  temporal-decoupling stays parked (one design at a time through the goal test).
