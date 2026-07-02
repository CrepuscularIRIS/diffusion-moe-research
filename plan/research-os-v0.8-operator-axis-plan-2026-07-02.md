# research-os v0.8 — Operator Axis + Living Taste Bank — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Add the 4th generative axis (modeling-object-shift **operators**) to research-os, backed by a
persistent, self-optimizing **Taste Operator Bank** on the Arbor substrate — seeded from `opus-pass`, grown
via `/autopsy` under the corrosion gate + independent audit, and sharpened just-in-time by GPT-5.5 Pro
deep-reads of the source papers.

**Architecture:** Bank STRUCTURE = a dedicated persistent Arbor run `taste-bank` (operators = nodes grouped
by family; `code_ref` → sealed card `.md`) + research-os's typed-edge md layer (`inferred-from / generates /
refines / rivals`, keyed by node-id, with cross-run refs to campaign runs). Bank CONTENT = sealed operator
`.md` cards. WIRING = retrieval-based edits to `/forge` (step 3‴), `/prospect`, `/compass`, `/autopsy` —
mirroring exactly how v0.7 wired the frames axis. No new commands, no new gates; reuses the corrosion gate,
the audit invariant, and `/epistemic-calibration`.

**Tech Stack:** Claude Code plugin (markdown skills + commands), Arbor MCP (`mcp__arbor__tree_*`), GPT-5.5
Pro via Playwright, `/epistemic-calibration` (evidence grades). No code / no pytest — verification is
grep + consistency checks + one end-to-end `/forge` dispatch.

**Verification model (read once):** research-os removed its validator/test suite in v0.5 (the diagnosis: the
validators never caught a real error). So every "verify" step here is a **grep / consistency check** (does
the wiring text exist; are there dangling refs or contradictions like the v0.7 "four checks" bug), plus a
final end-to-end dispatch. Treat a failed grep exactly like a failed test: do not proceed.

---

## File Structure (decomposition locked here)

**research-os plugin** (`/home/lingxufeng/cli/research-os/`):
- CREATE `skills/forge/references/taste-operators.md` — the operator-axis MACHINERY (schema, retrieval rule,
  corrosion-gate entry, accumulation rule, paper-read rule, Arbor mapping). Parallel to `frames.md`. Ships
  the *mechanism* + 2 exemplars, NOT the project's operators.
- MODIFY `skills/forge/SKILL.md` — add step 3‴ (operator retrieval + forcing) + step-7 paper-read for
  operator candidates + one hard rule.
- MODIFY `skills/prospect/SKILL.md` — add operator-retrieval as a mining input + a report line.
- MODIFY `skills/autopsy/SKILL.md` — add `[OPERATOR-CANDIDATE]` emission (gated by corrosion + audit).
- MODIFY `skills/compass/SKILL.md` — extend check 5 to cover operator-monoculture.
- MODIFY the 4 command files `commands/{forge,prospect,autopsy,compass}.md` — reflect the above.
- MODIFY `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md` — v0.8.0 + the axis.

**Project** (`/home/lingxufeng/huggingface/`):
- CREATE `taste-bank/operators/*.md` — the sealed operator cards (seeded from `opus-pass/operators.md` ★).
- CREATE `taste-bank/edges.json` — the typed-edge layer (inferred-from/generates/refines/rivals + cross-run).
- Arbor run `taste-bank` — operator nodes (via `mcp__arbor__tree_add_node`).
- MODIFY `plan/operating-manual.md` §5.2 — the operator axis + accumulation/paper-read rules.
- MODIFY `.claude/CLAUDE.md` — Key Project Files (the bank + axis) [gitignored, local only].
- MODIFY `plan/README.md` — note the 4th axis.

**One question the plan resolves in Phase 0:** whether the Arbor typed-edge layer can reference node-ids
across runs. If yes → cross-run edges (operator→campaign-candidate). If no → operators live in the
`taste-bank` run with intra-bank edges, and campaign cross-links are node-id strings in `edges.json`.

---

## Phase 0 — Substrate check (Arbor)

### Task 0.1: Verify Arbor supports a dedicated persistent run + stable node-ids

**Files:** none (a spike).

- [ ] **Step 1: Confirm a fresh run can be created and read**

Run (via the Arbor MCP): `mcp__arbor__tree_view(run_name="taste-bank", fmt="compact")`.
Expected: either an empty/new tree for `taste-bank`, or an error that the run does not exist yet.

- [ ] **Step 2: Add a throwaway node and confirm a stable node-id is returned**

Run: `mcp__arbor__tree_add_node(run_name="taste-bank", parent_id=<root>, hypothesis="PROBE — delete me", status="pending")`.
Expected: a node-id string is returned. Record whether node-ids look **run-scoped** (e.g. `taste-bank/3`) or
**global** (e.g. a uuid).

- [ ] **Step 3: Decide the edge model and record it**

If node-ids are global/stable → `edges.json` may reference campaign-run node-ids (cross-run edges OK).
If run-scoped → cross-run edges are stored as `{run_name, node_id}` pairs in `edges.json`.
Write the decision as a one-line comment at the top of `taste-bank/edges.json` in Task 1.4.

- [ ] **Step 4: Prune the probe node**

Run: `mcp__arbor__tree_prune(run_name="taste-bank", node_id=<probe id>, reason="probe")`.
Expected: node marked pruned. (Do NOT delete the run — Phase 1 reuses it.)

- [ ] **Step 5: Commit (nothing to commit — record the decision in the plan)**

No file change. Note the edge-model decision in your working notes; it is consumed in Task 1.4.

---

## Phase 1 — Build the Taste Operator Bank (structure + seed from opus-pass ★)

### Task 1.1: Create the bank directory + select the ★ operators

**Files:**
- Create: `/home/lingxufeng/huggingface/taste-bank/` (dir) and `taste-bank/operators/` (dir)
- Source (read-only): `/home/lingxufeng/huggingface/opus-pass/operators.md` (611 lines, 21 ★)

- [ ] **Step 1: Create the directories**

Run: `mkdir -p /home/lingxufeng/huggingface/taste-bank/operators`
Expected: dirs created.

- [ ] **Step 2: List the ★ operators to seed**

Run: `grep -nE '^### [0-9]+\. .*★' /home/lingxufeng/huggingface/opus-pass/operators.md`
Expected: ~21 lines (the ★ generation-test survivors). These are the seed set. Non-★ operators stay in
`opus-pass/` as provenance and are NOT seeded (avoid a 38-item menu).

- [ ] **Step 3: Split each ★ operator into its own sealed card file**

For each ★ operator `### N. <name> ★`, write its full block (from `### N.` up to the next `###`) verbatim to
`taste-bank/operators/<name>.md` (kebab-case name, e.g. `memory-kernel-closure.md`). Preserve all fields.
Do NOT re-author — copy the existing card content exactly.

- [ ] **Step 4: Verify the cards are complete (corrosion gate holds)**

Run:
```bash
cd /home/lingxufeng/huggingface/taste-bank/operators
for f in *.md; do
  ok=1
  for field in core_simplification differential_prediction cheap_probe; do
    grep -q "$field" "$f" || { echo "MISSING $field in $f"; ok=0; }
  done
  [ $ok = 1 ] && echo "OK $f"
done
```
Expected: every card prints `OK` (all 3 load-bearing fields present). Any `MISSING` → fix by re-copying that
card's block from `opus-pass/operators.md`.

- [ ] **Step 5: Commit**

```bash
cd /home/lingxufeng/huggingface
git add taste-bank/operators/
git commit -m "feat(taste-bank): seed the operator bank with the opus-pass ★ operators (sealed cards)"
```

### Task 1.2: Register each ★ operator as an Arbor node in the `taste-bank` run

**Files:** Arbor run `taste-bank` (no local file).

- [ ] **Step 1: Create the family group nodes**

For each family in `opus-pass/operators.md` (the `## Family N — …` headers), add one grouping node:
`mcp__arbor__tree_add_node(run_name="taste-bank", parent_id=<root>, hypothesis="Family N — <title>", status="done")`.
Record the returned family node-ids.

- [ ] **Step 2: Add one node per ★ operator under its family**

For each ★ operator: `mcp__arbor__tree_add_node(run_name="taste-bank", parent_id=<family node-id>,
hypothesis="<one_sentence_core_move>", status="done")`, then
`mcp__arbor__tree_update_node(run_name="taste-bank", node_id=<op node-id>,
insight="DIFF: <differential_prediction> · PROBE: <cheap_probe>", code_ref="taste-bank/operators/<name>.md")`.

- [ ] **Step 3: Verify the tree**

Run: `mcp__arbor__tree_view(run_name="taste-bank", fmt="compact")`.
Expected: root → families → ~21 operator nodes, each with an insight and a `code_ref` to its card.

- [ ] **Step 4: Commit (Arbor state persists itself; commit the run pointer if the project tracks it)**

```bash
cd /home/lingxufeng/huggingface
git add -A .arbor 2>/dev/null || true
git commit -m "feat(taste-bank): register ★ operators as Arbor nodes (run=taste-bank)" --allow-empty
```

### Task 1.3: Write the typed-edge layer

**Files:**
- Create: `/home/lingxufeng/huggingface/taste-bank/edges.json`

- [ ] **Step 1: Write edges.json with the edge model + the inferred-from + intra-bank edges**

Content (fill node-ids from Task 1.2; the header comment records the Phase-0 decision):
```json
{
  "_edge_model": "global-node-ids | run-scoped-pairs  (set per Phase-0 Task 0.1 Step 3)",
  "edges": [
    {"from": "<op node-id>", "type": "inferred_from", "to_episode": "<report#/case>"},
    {"from": "<op node-id>", "type": "rivals", "to": "<op node-id>"},
    {"from": "<op node-id>", "type": "refines", "to": "<op node-id>"}
  ],
  "cross_run": [
    {"from": "<op node-id>", "type": "generates", "to_run": "<campaign run>", "to_node": "<candidate node-id>"}
  ]
}
```
Populate `inferred_from` from each card's `source_episodes`, and `rivals/refines` from obvious relations
(e.g. `observable-lifting` refines `memory-kernel-closure`; `residual-ization` rivals `memory-kernel-closure`).
Leave `cross_run` empty for now (campaigns add to it via `/autopsy` and `/forge`).

- [ ] **Step 2: Verify valid JSON**

Run: `python3 -c "import json; json.load(open('/home/lingxufeng/huggingface/taste-bank/edges.json')); print('valid')"`
Expected: `valid`.

- [ ] **Step 3: Commit**

```bash
cd /home/lingxufeng/huggingface
git add taste-bank/edges.json
git commit -m "feat(taste-bank): typed-edge layer (inferred-from/rivals/refines + cross-run stub)"
```

---

## Phase 2 — Wire the operator axis into research-os (the plugin)

### Task 2.1: Create the operator-axis machinery reference

**Files:**
- Create: `/home/lingxufeng/cli/research-os/skills/forge/references/taste-operators.md`

- [ ] **Step 1: Write the machinery doc**

Write this exact content:
```markdown
# The Taste Operator palette — the FOURTH axis (`/forge` step 3‴)

> `schools.md` = how to think · `research-types.md` = what output · `frames.md` = which mathematics ·
> **taste-operators = which modeling MOVE** (the 建模对象迁移 operator). Operators are reverse-inferred
> from breakthroughs + our own anomalies; each is DE-DOMAINED and admitted only with all 3 load-bearing
> fields (`core_simplification` · `differential_prediction` · `cheap_probe`) surviving the deletion test.

## Where the bank lives (deployment)
The plugin ships the MECHANISM (this file + the wiring). The BANK is project-side: a persistent Arbor run
`taste-bank` (operators = nodes grouped by family; `code_ref` → a sealed card `.md`) + a typed-edge layer
(`inferred_from / generates / refines / rivals`). Read the cards the retrieval surfaces; do not inline a menu.

## Retrieval, not a menu (the anti-disease rule)
`/forge` matches the problem's `failure_signature` to 1–3 operators, forces ≥1 candidate from ONE of them,
and ROTATES across rounds. Never load all operators. `/compass` tracks operator diversity.

## The card schema (each sealed card)
operator_name · one_sentence_core_move · old_object_pattern · new_object_pattern · mathematical_frame
(frames.md) · core_simplification[LOAD-BEARING] · differential_prediction[LOAD-BEARING] ·
cheap_probe[LOAD-BEARING] · failure_signature · transfer_targets · positive_examples ·
negative_examples/when_it_misleads · source_episodes.

## Accumulation (按规定累计 — the bank grows only through the gate)
A new operator enters ONLY via: (1) the corrosion gate (all 3 load-bearing fields + deletion test), AND
(2) an INDEPENDENT audit (the one invariant — the proposer cannot self-grant an operator into the bank;
route to the Codex hook / a fresh reviewer). Sources: `/autopsy` own-anomalies (`[OPERATOR-CANDIDATE]`) +
future DeepResearch collections. Register the survivor as a node+edge in the `taste-bank` run.

## Paper-read optimization (just-in-time, GPT-5.5 Pro)
When an operator is about to drive a REAL candidate (right before `/prereg`), GPT-5.5 Pro deep-reads the
operator's `source_episodes` papers and verifies the `differential_prediction` + `cheap_probe` are FAITHFUL
to the actual method (not a mis-read of a summary). Refine the card; upgrade its evidence grade via
`/epistemic-calibration` (B summary → A paper-verified). This shares the single Playwright→Pro channel with
any live loop, so it serializes with those queries — acceptable because it is low-volume / just-in-time.

## Two exemplars (format reference only — the real bank is project-side)
### memory-kernel-closure ★
- core_move: coarse-grain but rewrite the dropped DOFs as an explicit memory kernel + noise on what you kept.
- differential_prediction: a non-Markov lag structure a longer context window does NOT fix but a kernel does.
- cheap_probe: fit Markov baseline + a small kernel head; kill if kernel weight ≈ 0 or long-rollout error unchanged.
### transport-coupling-ization ★
- core_move: matching/similarity → a mass-flow coupling (incl. Gromov-Wasserstein across different spaces).
- differential_prediction: predicts a transport plan whose marginals + cost a soft-attention map cannot expose.
- cheap_probe: compare an OT coupling vs attention on a cross-modal swap test before training.

## Guardrail
An operator grants a candidate NO validity — it still faces `/prereg` + `/adversary`. The bank expands the
PRIOR, not the evidence. Four axes is the ceiling (schools · types · frames · operators) — do not add a 5th.
```

- [ ] **Step 2: Verify the file has the 3 load-bearing fields + the retrieval rule**

Run: `grep -cE "core_simplification|differential_prediction|cheap_probe|Retrieval, not a menu|four axes is the ceiling" /home/lingxufeng/cli/research-os/skills/forge/references/taste-operators.md`
Expected: ≥5.

- [ ] **Step 3: Commit**

```bash
cd /home/lingxufeng/cli/research-os
git add skills/forge/references/taste-operators.md
git commit -m "feat(operators): the 4th-axis machinery reference (taste-operators.md)"
```

### Task 2.2: Wire `/forge` (step 3‴ + step-7 paper-read + hard rule)

**Files:**
- Modify: `skills/forge/SKILL.md` (insert after line 60, before `### 4. One card per candidate`; edit `## Hard rules` at line 125; edit step 7)
- Modify: `commands/forge.md`

- [ ] **Step 1: Insert step 3‴ after the frames step**

Insert immediately before `### 4. One card per candidate`:
```markdown
### 3‴. Operator retrieval + one FORCED operator candidate (the FOURTH axis — `references/taste-operators.md`)
The `taste-bank` Arbor run holds reusable modeling-move operators. Do NOT load them all.
- **Retrieve**: match this problem's failure signature to 1–3 operators (query the `taste-bank` run /
  the sealed cards by `failure_signature`). Print the matched operator names in the report.
- **Force ≥1 candidate** derived from ONE retrieved operator (symmetric to the rival-school + off-frame
  rules); rotate the chosen operator across rounds — never the same one twice running.
- That candidate's card carries the operator's `differential_prediction` in its DIFF-PREDICTION field —
  if the operator does not yield a differential here, it did not fit; pick another or drop it.
- The operator grants NO validity; the candidate still faces `/prereg` + `/adversary`.
```

- [ ] **Step 2: Add the paper-read to step 7 (operator candidates)**

Append to the end of step 7 (`### 7. Route the design to the external brain …`):
```markdown
- **Operator candidates get a just-in-time paper-read** (before `/prereg`): if the forced candidate came
  from a `taste-bank` operator, the Pro hand-off ALSO deep-reads that operator's `source_episodes` papers
  and verifies the `differential_prediction` + `cheap_probe` are faithful to the real method; refine the
  card and upgrade its evidence grade via `/epistemic-calibration` (B→A). Low-volume, so it serializes with
  any live Pro loop on the shared Playwright channel.
```

- [ ] **Step 3: Add the hard rule**

After the line `- ≥1 non-incumbent-**frame** candidate, always …` in `## Hard rules`, add:
```markdown
- ≥1 **operator** candidate from the `taste-bank` (step 3‴), retrieval-based + rotated — never a menu. An
  operator with no differential prediction *here* did not fit; do not force it.
```

- [ ] **Step 4: Verify + update the command file**

Run: `grep -cE "3‴|Operator retrieval|taste-bank" /home/lingxufeng/cli/research-os/skills/forge/SKILL.md` → Expected: ≥3.
Then add to `commands/forge.md` "How to run" a `3‴.` bullet mirroring step 3‴ (retrieval + forced operator
candidate + rotate), and note step-7's operator paper-read.

- [ ] **Step 5: Commit**

```bash
cd /home/lingxufeng/cli/research-os
git add skills/forge/SKILL.md commands/forge.md
git commit -m "feat(forge): step 3‴ operator retrieval+forcing + just-in-time paper-read"
```

### Task 2.3: Wire `/prospect` (operator retrieval as a mining input)

**Files:** Modify `skills/prospect/SKILL.md` (after Mine 5, line 69) + `commands/prospect.md`.

- [ ] **Step 1: Add the operator-retrieval mining note**

After `### Mine 5 — Cross-domain transplant`, add:
```markdown
### Operator retrieval (the taste-bank, cross-cutting)
Beyond the five mines: query the `taste-bank` operators whose `failure_signature` matches the current
territory. An operator that fits surfaces a candidate PROBLEM ("this looks like a place for
memory-kernel-closure — is there a non-Markov lag we're paying for?"). This is a prior, not a problem —
it still needs STAKES + SURPRISE on its card.
```

- [ ] **Step 2: Add the frame+operator ledger line to Rank-and-emit**

In `## Rank and emit`, extend the existing frame-ledger line to also print
`· candidate operators = <a, b>` (the retrieved operator names).

- [ ] **Step 3: Verify + command file**

Run: `grep -cE "Operator retrieval|taste-bank|candidate operators" /home/lingxufeng/cli/research-os/skills/prospect/SKILL.md` → Expected: ≥2.
Add a one-line operator-retrieval note to `commands/prospect.md` step 1.

- [ ] **Step 4: Commit**

```bash
cd /home/lingxufeng/cli/research-os
git add skills/prospect/SKILL.md commands/prospect.md
git commit -m "feat(prospect): taste-bank operator retrieval as a mining input"
```

### Task 2.4: Wire `/autopsy` (`[OPERATOR-CANDIDATE]` emission)

**Files:** Modify `skills/autopsy/SKILL.md` (in `### 4′.`, line 65) + `commands/autopsy.md`.

- [ ] **Step 1: Extend 4′ to also emit an operator candidate**

Append to `### 4′. Log the SURPRISE to the anomaly ledger`:
```markdown
**Also — operator accumulation (按规定累计):** if the anomaly reveals a *reusable modeling move* (not just a
one-off constraint), emit `[OPERATOR-CANDIDATE]` with the card fields drafted (all 3 load-bearing fields +
the deletion test). It enters the `taste-bank` ONLY after an INDEPENDENT audit (Codex hook / fresh reviewer)
— the proposer cannot self-grant an operator into the bank (the one invariant). On PASS: `tree_add_node` in
the `taste-bank` run + an `inferred_from` edge from this anomaly's node. On FAIL: keep as a scoped constraint.
```

- [ ] **Step 2: Verify + command file**

Run: `grep -cE "OPERATOR-CANDIDATE|taste-bank|INDEPENDENT audit" /home/lingxufeng/cli/research-os/skills/autopsy/SKILL.md` → Expected: ≥2.
Add a `4′.`-adjacent bullet to `commands/autopsy.md` for the operator-candidate emission.

- [ ] **Step 3: Commit**

```bash
cd /home/lingxufeng/cli/research-os
git add skills/autopsy/SKILL.md commands/autopsy.md
git commit -m "feat(autopsy): emit [OPERATOR-CANDIDATE] (corrosion gate + independent audit) into taste-bank"
```

### Task 2.5: Wire `/compass` (operator-monoculture)

**Files:** Modify `skills/compass/SKILL.md` (check 5, line 61) + `commands/compass.md`.

- [ ] **Step 1: Extend check 5 to cover operators**

In `### 5. FRAME-MONOCULTURE`, rename the heading to `### 5. FRAME- & OPERATOR-MONOCULTURE` and add:
```markdown
- **Operator diversity:** across the last N `/forge` rounds, how many DISTINCT `taste-bank` operators were
  forced? 1 (or none) → operator-monoculture flag; the next `/forge` must retrieve+rotate to a different
  operator, or `/prospect` on fresh territory. Same failure shape as frame-monoculture — the retrieved
  operator quietly losing the taste-rank round after round.
```
Keep the description consistent — do NOT leave a stale "frame-monoculture only" line (avoid the v0.7
"four checks" contradiction bug: update every reference to "check 5" wording).

- [ ] **Step 2: Verify no stale single-axis wording**

Run: `grep -niE "frame-monoculture" /home/lingxufeng/cli/research-os/skills/compass/SKILL.md`
Expected: every hit reads "frame- & operator-monoculture" or explicitly covers both — no bare
"frame-monoculture" that contradicts the new operator clause.

- [ ] **Step 3: Update the command file + commit**

Update `commands/compass.md` check 5 wording to "frame- & operator-monoculture".
```bash
cd /home/lingxufeng/cli/research-os
git add skills/compass/SKILL.md commands/compass.md
git commit -m "feat(compass): check 5 now covers operator-monoculture as well as frame-monoculture"
```

### Task 2.6: Version bump + README

**Files:** Modify `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`.

- [ ] **Step 1: Bump both manifests 0.7.0 → 0.8.0**

In `plugin.json` and `marketplace.json`, change `"version": "0.7.0"` → `"0.8.0"` and append to each
description: "v0.8 adds the FOURTH generative axis — taste-operators (modeling-move palette) on a persistent
Arbor `taste-bank` (grows via /autopsy under the corrosion gate + independent audit; sharpened by
just-in-time GPT-5.5 Pro paper-reads)."

- [ ] **Step 2: Add the README axis section**

After the "## The mathematics axis" section in `README.md`, add a "## The operator axis — the fourth axis
(v0.8)" section: schools · types · frames · **operators**; retrieval not menu; the Arbor `taste-bank`;
accumulation gate + audit; paper-read optimization; the "operator grants no validity" guardrail; four axes
is the ceiling.

- [ ] **Step 3: Verify versions + commit**

Run: `grep -h '"version"' /home/lingxufeng/cli/research-os/.claude-plugin/*.json` → Expected: both `0.8.0`.
```bash
cd /home/lingxufeng/cli/research-os
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json README.md
git commit -m "docs(readme): v0.8.0 — the operator axis (fourth generative axis)"
```

### Task 2.7: Sync `~/.claude` + push research-os

**Files:** `~/.claude/skills/*`, `~/.claude/commands/*`.

- [ ] **Step 1: Sync the changed skills + commands + the new reference**

```bash
cd /home/lingxufeng/cli/research-os
cp skills/forge/references/taste-operators.md ~/.claude/skills/forge/references/taste-operators.md
for s in forge prospect autopsy compass; do cp skills/$s/SKILL.md ~/.claude/skills/$s/SKILL.md; done
cp commands/{forge,prospect,autopsy,compass}.md ~/.claude/commands/
```

- [ ] **Step 2: Verify the sync landed the operator wiring**

Run: `grep -lE "taste-operators|3‴|OPERATOR-CANDIDATE|operator-monoculture" ~/.claude/skills/forge/SKILL.md ~/.claude/skills/forge/references/taste-operators.md ~/.claude/skills/autopsy/SKILL.md ~/.claude/skills/compass/SKILL.md | wc -l` → Expected: 4.

- [ ] **Step 3: Push**

```bash
cd /home/lingxufeng/cli/research-os
git push origin HEAD 2>&1 | tail -2
```
Expected: a successful push line.

---

## Phase 3 — Project-doc sync

### Task 3.1: operating-manual §5.2 — the operator axis

**Files:** Modify `/home/lingxufeng/huggingface/plan/operating-manual.md` (§5.2 generator table).

- [ ] **Step 1: Add an operator-axis row/note to §5.2**

In the §5.2 generator table (the `/forge` row), append: "+ **step 3‴ operator retrieval** from the
`taste-bank` (4th axis; retrieval+rotate, never a menu); the operator's paper-read fires just-in-time before
`/prereg` (Pro deep-read → evidence upgrade)." Add one line under the table: "The `taste-bank` is a
persistent Arbor run (`run_name=taste-bank`) + sealed cards under `taste-bank/operators/`; it grows via
`/autopsy [OPERATOR-CANDIDATE]` under the corrosion gate + independent audit."

- [ ] **Step 2: Verify + commit**

Run: `grep -cE "taste-bank|step 3‴|OPERATOR-CANDIDATE" /home/lingxufeng/huggingface/plan/operating-manual.md` → Expected: ≥2.
```bash
cd /home/lingxufeng/huggingface
git add plan/operating-manual.md
git commit -m "docs(manual): §5.2 — the operator axis + the taste-bank"
```

### Task 3.2: CLAUDE.md Key Files (gitignored — local only)

**Files:** Modify `/home/lingxufeng/huggingface/.claude/CLAUDE.md`.

- [ ] **Step 1: Add the bank to Key Project Files**

Add a bullet: "`taste-bank/` (operators/ sealed cards + edges.json) + Arbor run `taste-bank` — the 4th-axis
modeling-move operator bank (seed = opus-pass ★; research-os v0.8 wires /forge step 3‴, /prospect, /autopsy,
/compass to it)." And in the research-os plugin line, bump v0.7.0 → v0.8.0 and add `taste-operators.md` +
"operators" to the axes list.

- [ ] **Step 2: Verify (no commit — .claude is gitignored)**

Run: `grep -c "taste-bank" /home/lingxufeng/huggingface/.claude/CLAUDE.md` → Expected: ≥1. (Do NOT git add —
`.claude/` is gitignored; this stays local.)

### Task 3.3: plan/README + push

**Files:** Modify `/home/lingxufeng/huggingface/plan/README.md`.

- [ ] **Step 1: Note the 4th axis**

In the research-os description in `plan/README.md`, add "operators (taste-bank, v0.8)" to the axes list.

- [ ] **Step 2: Commit + push**

```bash
cd /home/lingxufeng/huggingface
git add plan/README.md plan/research-os-v0.8-operator-axis-plan-2026-07-02.md
git commit -m "docs(plan): note the operator axis + land the v0.8 plan"
git push origin HEAD 2>&1 | tail -2
```
Expected: a successful push line.

---

## Phase 4 — End-to-end validation

### Task 4.1: Prove the operator axis fires on a live problem

**Files:** none (a dispatch).

- [ ] **Step 1: Run `/forge` on a real problem via the operator axis**

Invoke `/forge` on the paused DSpark problem ("beyond-Markov sequential head"). Expected in the output: a
frame-ledger line AND a **retrieved-operators line**; and among the 3–5 candidates, ≥1 **operator candidate**
(e.g. from `memory-kernel-closure`) carrying a concrete `DIFF-PREDICTION` (gain only where lag>1, vanishes on
a shuffle control) + a cheap probe.

- [ ] **Step 2: Confirm the operator granted no validity**

Verify the operator candidate's card still lists a KILL experiment and would route to `/prereg` + `/adversary`
— i.e. the operator did not shortcut the discipline.

- [ ] **Step 3: (No commit — this is a read-only proof.)**

### Task 4.2: Consistency scan (the stop-hook-style check)

**Files:** none.

- [ ] **Step 1: No dangling refs / no axis-count contradictions**

Run:
```bash
cd /home/lingxufeng/cli/research-os
grep -rniE "four axes|three axes|3 axes|4 axes" skills/ README.md | grep -viE "four axes is the ceiling"
grep -rniE "frame-monoculture" skills/compass/ | grep -viE "operator"
```
Expected: the first returns nothing that says "three axes" (everything now = four); the second returns nothing
(every frame-monoculture mention also covers operators). Any hit → fix the stale wording, re-sync `~/.claude`,
re-commit.

- [ ] **Step 2: Confirm the Arbor bank is populated**

Run: `mcp__arbor__tree_view(run_name="taste-bank", fmt="compact")` → Expected: ~21 operator nodes with
`code_ref`s. Any node missing a `code_ref` → fix via `tree_update_node`.

---

## Self-Review (author checklist — completed)

**Spec coverage:** ✓ 4th-axis wiring (Task 2.2–2.5) · Arbor bank structure (Phase 1) · seed from opus-pass ★
(1.1) · accumulation gate + independent audit (2.4) · paper-read via Pro just-in-time (2.2 step 2) · the
Arbor-cross-run-edge unknown (Phase 0) · project-doc sync (Phase 3) · end-to-end proof (4.1). Fable's pass:
merges later as the first `/autopsy`/collection accumulation event (out of scope for this plan — it enters
via Task 2.4's gate).
**Placeholder scan:** ✓ no TBD/TODO; exact paths + exact insert text on every edit; the operator card content
is COPIED from `opus-pass` (a real source, Task 1.1 Step 3), not invented.
**Type consistency:** ✓ the axis is named "operators"/"taste-operators"/"taste-bank" consistently; step is
"3‴" everywhere; the run is `taste-bank` everywhere; the emission tag is `[OPERATOR-CANDIDATE]` everywhere.
**Scope:** one feature (the operator axis) in four phases; each phase leaves the repo working (Phase 1 = a
usable bank; Phase 2 = wired plugin; Phase 3 = synced docs; Phase 4 = proof). Not decomposed further —
the phases share the one axis and are sequentially dependent.
