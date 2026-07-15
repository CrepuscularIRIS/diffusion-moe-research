# Research-OS v4.0 "Four Gates" — Implementation Plan (2026-07-13)

## Context

The devil's-advocate audit (`plan/Audit/pipeline-devils-advocate-audit-2026-07-13.md`) found:
(1) ~70% of historical sunk cost went to directions rejectable at selection time — selection has no
binding gate; (2) binding gates (prereg/exp-verify/adversary, occupancy 精读, kill criteria, forecast
rows) decided everything that went right, while scripted generative procedure (card taxonomies, forced
axes, router tags, multi-step reasoning scripts) decided nothing; (3) the corpus (~2,400 lines) is
over-specified in exactly the generative places and accretes one rule per funeral; (4) failures feed
generation (marginal by construction) while successes have no memory; (5) the external brain — the only
live-search-grounded engine — fires almost exclusively post-hoc.

**v4.0 reframe — GATES, NOT SCRIPTS:** few binding gates + free reasoning between them + banks as
retrievable data, never procedure. One NEW gate (`/admit`, GATE 0) closes the selection hole. The
generative skills are gutted to kernels. Successes get a memory (`capabilities.md`). Net deletion:
skills+references ~2,383 → ≤ ~1,200 lines.

- Repo: `/home/lingxufeng/cli/research-os`, branch `v4.0-four-gates` (from 738ade3 / v3.7).
- Backup: git tag `v3.7-pre-v4.0-backup` + `/home/lingxufeng/huggingface/backups/pre-v4.0-2026-07-13/`.
- Loop shape after v4.0:

```
SELECT loop:  /prospect ──▶ /admit (GATE 0) ──▶ adopted direction
SOLVE  loop:  /forge ──▶ /prereg (GATE 1) ──▶ run ──▶ /exp-verify (GATE 2)
                 ▲                                        ├─ claim ─▶ /adversary (GATE 3) ─▶ human
                 └──────────── /autopsy ◀─────── null ────┘
```

## Global Constraints (binding on every task)

**GC1 — Preserved rulings.** Every one of these must survive somewhere sensible in the rewritten
corpus (reviewers check this list item-by-item):
1. The invariant: a verdict that helps the proposer if gamed is never proposer-granted — DOWN-only
   self-grant; `CLAIM_STANDS` = independent cross-family substrate; contribution/paper promotion =
   human only; silence ≠ pass.
2. Context isolation: generator ≠ executor ≠ verifier; independent review framed to REFUTE.
3. Honest evidence: sealed evals immutable mid-run; numbers read from artifacts at writing time;
   prereg before any claim-bearing run; exploration numbers never promoted retroactively.
4. Value bar is EXTERNAL: internal checks PRICE (conviction · cost · occupancy risk), never veto;
   pursue/drop = external venue review (role 4; full novelty NOT required — a clean Δ on a fair
   benchmark counts). **The new /admit gate must be phrased to respect this: its checks price; its
   drop authority is the external micro-review + human ack; its binding power is SPEND-gating
   (no direction-scale spend unadmitted), not idea-veto.**
5. External-verdicts-are-candidates: any consult may REFUTE unilaterally; none may SET direction —
   proposals enter the forge backlog against ≥2 local candidates.
6. HUNCH lane: ≤2h wall-clock · no GPU training · no sealed split ⇒ direct probe with 2-line
   `HUNCH/DROP-IF` note; exploration-grade numbers; graduates on surprise. Hunches and cheap probes
   live BELOW the admit gate — always free.
7. Symmetric gates (anti-ratchet): near-miss FAIL ⇒ exactly one fresh-frozen refinement prereg;
   a PASS cannot accrue undeclared extra screens.
8. Stall ≠ pivot: autopsy + relaxation ladder (now CAPPED — see Task 2) before any lateral;
   region-close needs the epitaph.
9. Teaching contract: every human course-correction → extract the violated principle into the
   relevant bank/lesson, report the extraction.
10. Operate physics stays explicit and near-verbatim: launch arithmetic (measured ETA ·
    kill-checkpoints), GPU policy, free-device auto-dispatch, ownership/kill safety, monitor
    discipline, artifact fidelity.
11. MoA: bank-first precondition; per-lane differentiation (operator/frame dropout); ≥4 live lanes
    for a full panel; panel lane never reviews its own round.
12. Never name a skill `goal`; no custom `/goal` command; conductor invoked via the built-in /goal
    bootstrap condition.

**GC2 — Line budgets (hard).** Sum of all `skills/*/SKILL.md` ≤ 800 lines; references total ≤ 420.
Per-file targets in tasks (±15% tolerance).

**GC3 — Frontmatter format.** Keep the v3.7 pattern: `name`, `description` ending with
`Use when <intent>. Prompt keywords — "…", "…"` (strict-YAML-safe: no bare `: ` sequences inside the
description), `version: 4.0.0`, `tags`. Descriptions stay keyword-dense (they are the auto-trigger
surface); re-scope keywords where a skill's role changed.

**GC4 — Voice.** Match the existing corpus: dense, imperative, no filler, no history/citations inside
skills. Skills are interfaces; mechanisms live in tools and banks. No project-specific paths in
skills (the BINDINGS pattern carries paths).

**GC5 — Process.** Commit per task on branch `v4.0-four-gates`, conventional-commit messages. Do not
touch `~/.claude` runtime in Tasks 1–3 (Task 4 syncs). Do not edit files owned by another task.

## Task 1: SELECT loop — conductor rewrite + new `admit` gate + prospect rewrite

**Files:** `skills/conductor/SKILL.md` (rewrite, target ~100 lines) · `skills/admit/SKILL.md` (NEW,
~55) · `skills/prospect/SKILL.md` (rewrite, ~45) · `commands/admit.md` (NEW thin wrapper matching
`commands/prospect.md` style).

**conductor/SKILL.md:**
- Goal-contract block gains two one-line fields: `NON-GOALS:` (results that do NOT count even if they
  succeed) and `DECISION-CHANGE:` (who changes what decision if the objective is met).
- State the v4.0 principle once, near the top: *four gates bind; everything between them is free
  reasoning; banks/tricks/operators are data to retrieve, never procedure to obey.*
- Replace the single-loop diagram with the two-loop diagram (SELECT: prospect→admit; SOLVE:
  forge→prereg→run→exp-verify→{adversary→human | autopsy}).
- Keep, compressed: session protocol (recall→inventory→orient→re-enter-through-state→reconcile
  orphans); bounded autonomy (≤12 cycles, ≤3 inconclusive ⇒ escalate-first-stop-second); HUNCH lane;
  external-verdicts-are-candidates; value-bar-external; knowledge-reuse heuristic; synthesis at
  reversibility forks; engine-division table (6 roles — the external brain's row adds "frontier
  scout at goal-start/region-close + admission micro-review"); autonomy §3; stall≠pivot pointer;
  sub-skill routing table (add `admit`); write-through §6.
- Drop: the first-principles-spine paragraph (superseded by the two-loop framing); any rule fully
  restated in a sub-skill (keep the pointer only).

**admit/SKILL.md (NEW — GATE 0):**
- Fires BEFORE direction-scale commitment: planned GPU-training-scale spend (> ~1 GPU-day) or a
  claim-bearing programme. Below it, everything is free (hunches, cheap probes, exploration).
- THE SIX CHECKS — each produces a NUMBER or named evidence; each PRICES, none vetoes internally:
  1. `SOTA-VERIFIED` — the substrate's strongest known result reproduced or artifact-verified;
     never invent atop an unvalidated base.
  2. `MAGNITUDE` — measured phenomenon size from a cheap probe: a number, not an adjective;
     marginal ⇒ priced steeply up.
  3. `GOAL-VARIANCE` — the optimal decision/policy actually differs across the studied conditions.
  4. `SUBSTRATE-MECHANICS` — replay-determinism / eval-noise floor / harness validity as relevant.
  5. `OCCUPANCY` — external triage + local 精读 seals; "partially done" prices, never kills.
  6. `VENUE MICRO-REVIEW` — one external-brain query (role 4): would a plausible-magnitude result
     clear the venue bar? A DROP here binds (external authority — GC1.4).
- The admission one-pager (the human-visible artifact): a short risk table (problem → consequence →
  mitigation) + **THE THREE KILL-FIRST EXPERIMENTS** — three cheapest experiments each of which can
  kill the direction, run before scale. GPU-scale commitment surfaces the one-pager to the human
  (ack; async below that threshold).
- Write-through: the six check results → the direction node's meta/insight in the tree (so the gate
  is mechanically auditable); every later death cites which check failed or was skipped.
- Description keywords: "should we pursue this direction", "is this worth a campaign", "admit the
  direction", "before we commit GPUs", "direction-scale decision".

**prospect/SKILL.md:**
- Mines reordered — Mine 0 constraints+atlas read-first (kept); **Mine 1 = EXTERNAL FRONTIER SCAN**
  (external brain, live search: field map, capability deltas, what-just-became-possible,
  contradictions) fired at goal-start / region-close / stall; Mine 2 = the capability bank +
  surprising own successes (path from BINDINGS); Mine 3 = own-log anomalies; Mine 4 = literature
  contradictions + negative space; Mine 5 = benchmark critique. Run every mine whose input exists,
  ≥2.
- Card = FOUR fields: `Q` · `WHY-NOW` (with magnitude evidence when any exists) · `PROBE/KILL`
  (cheapest surprise-symmetric experiment) · `STAKES` (phrased as decision-change: who changes what).
- Rank by STAKES × plausibility-of-surprise ÷ probe-cost; emit 3–7 cards + ONE recommended probe.
- HUNCH entry (2 lines) kept. Exit rule: a card heading toward direction-scale commitment goes to
  `/admit`. Reconstruction into another discipline's native object = one line, optional high-value
  move (no mandate). Write-through to tree.
- Drop: IDEATION-TAGs, the RECONSTRUCTION mandate + field, TYPE field on the card (TYPE enters at
  prereg where it routes adversary checks), latent-root ceremony (one pointer line to `abduce`),
  the re-price-on-sight subsection (fold to 2 lines).

## Task 2: generative half — forge, abduce, autopsy (+failure-atlas ref), externalize, tricks

**Files:** `skills/forge/SKILL.md` (~55) · `skills/abduce/SKILL.md` (~30) · `skills/autopsy/SKILL.md`
(~45) · `skills/autopsy/references/failure-atlas.md` (schema update, ~same length) ·
`skills/externalize/SKILL.md` (~40) · `skills/tricks/SKILL.md` (version bump only) · DELETE
`skills/forge/references/schools.md` and `skills/forge/references/frames.md` (keep `taste.md`,
`taste-operators.md`).

**forge:** kernel only — every candidate carries a one-line `KILL`; two-sentence mechanism test;
`ORACLE-CEILING/TRIVIAL-FLOOR` bracket before anything training-eating; on a NEW problem ≥1
rival-frame candidate carrying a `DIFF-PREDICTION` (deletion test: predicts something the incumbent
cannot, else it is relabeling — one line, no palette machinery); chosen candidate → `/prereg` before
citable runs. Card = `{MECHANISM (or HUNCH-class) · MVE · KILL · BRACKET · COST · DIFF-PREDICTION
(off-frame only)}`. Retrieval domain-bank-first by failure signature (1–3 cards, never browse);
KILL/BRACKET designs from `tricks`. Necessity check = one pricing line; occupancy re-prices never
vetoes = one line. Regeneration rule kept, compressed to its 3-branch form. External refinement
event-triggered (training-eating or post-kill), refines the chosen candidate, never re-picks. MoA on
irreversible forks only (pointer to moa-routing). Drop: schools/frames axes, IDEATION-TAG taxonomy,
MODELING-OBJECT paragraph, two-call blinded protocol, the long pricing-signals section.

**abduce:** the kernel — observation cluster in artifact numbers → ≥3 competing mechanisms (boring +
incumbent MANDATORY) → differential consequences → minimum discriminating diagnostic with EVERY
branch pre-mapped BEFORE looking → consistency-close against all observations → commit with evidence
grades (`[artifact] [paper] [repo] [claimed] [inferred] [guess]`). Anti-patterns as 3 bullets
(first-sufficient stop · post-hoc narrative · hedge-listing). Loop-moments table compressed to 3 rows.

**autopsy:** boring-first triage → why scaled to stakes (full abduce kernel only for claim-bearing
kills/surprises/region-closes; one line for cheap nulls) → DOWN-only scope grade → CONVERSION LAW
(≥1 of constraint/candidate/region-close) → **the EXTRACTION ROW (new, replaces prose):** every death
writes `{magnitude: <the number that was too small or absent> · admit-check: <which GATE-0 check
would have caught this, or "none — genuinely empirical"> · constraint: <transferable> ·
cost-of-kill: <GPU-h / wall-clock>}` → atlas + tree. **Ladder CAPPED:** generate ≤3 rungs; each rung
states its MINIMUM-STAKES (who would use even this weaker version — none ⇒ the rung is DROP-graded
at birth); MAX 2 descents per capability, then the close is legal with remaining rungs DROP-graded;
≥1 rung probed or priced-and-declined stays the floor before any close. Stall≠pivot compressed to
~4 lines. Programme pulse → 3 items (surprise accounting · process budget >20% ⇒ ship a run ·
diversity/monoculture) + at every REGION-CLOSE the red-team question written into the epitaph:
*"what evidence would stop this entire programme?"*. [ANOMALY]/[OPERATOR-CANDIDATE]/[ATLAS] ledgers
compressed to ~3 lines. `failure-atlas.md`: add the extraction-row schema; keep enrichment rules.

**externalize:** six write conventions (verbatim in spirit) + derived-synthesis rule +
re-entry reconstruction test (compressed) + the seven moments as one line-list. Drop the rest.

**tricks:** unchanged content; `version: 4.0.0`.

## Task 3: gates + ops + ledger + tool references

**Files:** `skills/prereg/SKILL.md` (~90) · `skills/exp-verify/SKILL.md` (~75) ·
`skills/adversary/SKILL.md` (~85, near-unchanged) · `skills/operate/SKILL.md` (near-verbatim, ≤87) ·
`skills/ledger/SKILL.md` (~70) · `skills/conductor/references/external-brain.md` (~100) ·
`skills/conductor/references/moa-routing.md` (~90) · `skills/conductor/references/artifact-contract.md`
(unchanged) · `skills/prospect/references/research-types.md` (unchanged).

**prereg:** keep the kernel verbatim in spirit: exploration/evidence line · HYPOTHESIS/LATENT-ROOT/
MECHANISM/TYPE/METRIC/BENCHMARK/SPLIT/UNIT+TEST/ACCEPT/KILL/BRACKET/IDENTIFIABILITY/NEG-CONTROL/
SEEDS/POWER-MDE/ONE-VAR/FAILURE-FORECAST/FORECAST/LAUNCH-ARITHMETIC · the paired-test table · the
confirmatory extension · symmetric-gates rule · sealed-layer rule · storage/merge-gate mechanics.
Trim: `MoA-GATE` field → one line inside the rules ("panel consult is priced, not gated, except
irreversible forks"); `PHASE`/`OCCUPANCY-GATE` compress — occupancy evidence primarily lives at
`/admit` now; a CONTRIBUTION-claim prereg cites the admit occupancy evidence (`related_work`) instead
of restating the two-path protocol (keep the browser-never-self-certifies line); `DIFF-PRED` optional
block → 3 lines.

**exp-verify:** keep 3 stages + surprising-result extension + critical rules + write-through. ADD a
fourth check block, `DESIGN-VALID` (runs at contract time or first verify, before interpretation):
unit defined + paired test valid for it · **positivity/coverage — the estimand can observe the events
it claims to measure; no missingness hole shaped like the signal (MNAR)** · one-variable honesty ·
identifiability where attribution is claimed. New verdict `FAILED-DESIGN`. One line scoping:
execution-validity says the run happened; design-validity says the run can answer the question.

**adversary:** content proven — keep all four checks + verdict table + invariant. Version bump,
tighten wording only where free.

**operate:** near-verbatim (GC1.10). Version bump; only trivially-redundant lines may go; ≤87 lines.

**ledger:** keep the five verbs + row schema + curation + gate-pressure check. Changes: the
gate-pressure line "binds at THREE late moments" → "binds at the FOUR gates (admit / prereg /
exp-verify / adversary)". ADD the third file: `capabilities.md` (path from BINDINGS) — at every
`CLAIM_STANDS` or surprising verified PASS, write a capability row
`{capability · minimal conditions (what it survived ablating) · corrosion check (contamination /
shortcut / slice-search — graded DISCOVERED/CONFIRMED/MECHANISTIC) · boundary (where it stopped) ·
transfer targets}` — successes get a memory symmetric to the failure atlas; `/prospect` Mine 2 reads
it. Lesson archetypes compressed to a name+one-line list.

**external-brain.md:** add role 0 `FRONTIER SCAN` — generative live-search mining at goal-start /
region-close / stall (field map · capability deltas · what-just-became-possible); note that role 4
(venue review) also fires at `/admit` as the one-query micro-review whose DROP binds. Keep the query
protocol, the four existing roles, the direction rule, the drift warning.

**moa-routing.md:** add PROBLEM-MODE — the differentiated panel may fire at problem GENERATION
(per-lane mines + structured dropout), not only approach generation; lane briefs MUST carry a 5-line
project inventory `{hardware · envs · checkpoints · measured throughputs}` so "cheap probe"
suggestions are runnable as stated; the diversity check is by DIFFERENTIAL PREDICTIONS, not
vocabulary (two lanes whose predictions match under every probe are one lane). DELETE the 6-round
chain section; replace with: chain depth defaults to 2–3 reconciled rounds; a further round is legal
only if the previous round CHANGED the dispute-map. Keep tiering, liveness quorum, reconciliation
discipline, per-advisor output contract.

## Task 4: packaging + project side + runtime sync

**Files (repo):** `README.md` · `.claude-plugin/plugin.json` · `marketplace.json` · `commands/*.md`.
**Files (project, `/home/lingxufeng/huggingface`):** `judgment/capabilities.md` (NEW seed) ·
`plan/goal-directive.md` (sync) · `.claude/CLAUDE.md` (sync). **Runtime:** `~/.claude/skills`,
`~/.claude/commands`.

1. Version 4.0.0 in plugin.json + marketplace.json. README: title v4.0, a provenance paragraph for
   v4.0 (gates-not-scripts reframe; the audit as source; line counts before/after), update the skill
   list (13 skills incl. `admit`).
2. Commands: add `commands/admit.md` (thin wrapper, `disable-model-invocation: true`); refresh the
   description lines of `prospect.md`/`forge.md`/`autopsy.md` wrappers to match the new skill
   descriptions; others unchanged.
3. `judgment/capabilities.md` seed: header explaining the bank (successes symmetric to the atlas),
   the row schema from Task 3's ledger spec, no rows yet.
4. `plan/goal-directive.md`: CONDUCT/LOOP lines updated to the two-loop + four-gates shape;
   OBJECTIVE section gains `NON-GOALS:` and `DECISION-CHANGE:` one-liners (draft sensible content
   for the world-models fresh restart: e.g. NON-GOALS = reproduction-only results, saturated-slice
   benchmark deltas that change no decision; DECISION-CHANGE = which practitioners/decisions the
   claim moves); BINDINGS adds the capabilities path `judgment/capabilities.md`.
5. `.claude/CLAUDE.md`: authority-map paragraph — v2.0 → v4.0 wording, mention the four gates +
   admit + capabilities bank in §2 bindings (2–4 lines changed, keep it slim).
6. Runtime sync: rsync each repo skill dir → `~/.claude/skills/<name>/` (including NEW `admit`,
   and DELETING the removed reference files in the runtime copies), and research-os-owned command
   wrappers → `~/.claude/commands/`.
7. Consistency pass (report results): `grep -rn "IDEATION-TAG\|schools.md\|frames.md\|six commands"
   skills/ commands/` must return nothing stale; total `wc -l` of skills + references reported
   against GC2; every SKILL.md front-matter parses as strict YAML (python yaml.safe_load check);
   every `Prompt keywords` clause intact.

## Acceptance (final whole-branch review checks)

- GC1 rulings all present (item-by-item), GC2 budgets met, GC3 frontmatter valid.
- The two loops + four gates are coherent across conductor/admit/prospect/prereg/ledger.
- No stale cross-references (deleted files, renamed fields, old loop diagram).
- Runtime == repo for all 13 skills + wrappers.
- Project files consistent with skill corpus (goal-directive, CLAUDE.md, capabilities seed).
