# Pipeline Enforcement — Implementation Plan (2026-07-10)

> Implements `plan/Audit/latent-issues-audit-2026-07-10.md` + `plan/Audit/missing-axes-2026-07-10.md`,
> adapted per user directive: **no reliance on manual verification — every gate is an executable PASS/BLOCK
> script or a machine-checkable artifact; the pipeline is ≥95% autonomous; human involvement only for
> contribution/paper promotion and forced domain/resource switches.** Security concerns are explicitly out of
> scope for this change-set.

## Global Constraints (bind every task)

1. **Autonomy:** no step introduced by this plan may require a human confirmation. Independent review
   substrates must be invocable non-interactively: `codex exec` (GPT CLI) and `agy` (Gemini CLI) are
   first-class automated CLAIM_STANDS substrates; the GPT-5.6 browser is an optional stronger lane. The ONLY
   human gates that remain: contribution/paper promotion, forced domain/dataset switch, new large
   resources, external publish, destructive ops.
2. **Anti-accretion:** zero new commands; additions are single lines/clauses folded into existing parts.
   Each guard script stays small (< ~60 lines) and prints PASS/BLOCK + reason; exit 0 = PASS, exit 1 = BLOCK.
3. **Git discipline:** NEVER `git add .` or `git add -A`. Commit ONLY the files the task names.
   `/home/lingxufeng/cli/research-os` is a SEPARATE repo — commit there separately; do NOT push either repo.
   `.claude/CLAUDE.md` is gitignored and `~/.claude/skills` + the memory dir are outside git: for every
   non-git file edited, first copy the pre-edit file to `.superpowers/sdd/pre/<name>` and after editing
   append `git diff --no-index .superpowers/sdd/pre/<name> <edited-path>` output to
   `.superpowers/sdd/task-<N>-nongit.diff` (create it; empty is fine if a task touches no non-git file).
4. **Bash scripts:** `set -euo pipefail`, no external deps beyond coreutils/grep/awk, executable bit set.
   Python: stdlib only.
5. **Exact clause texts given in a task are requirements** — transcribe them (whitespace/flow adaptation to
   the surrounding file is fine; meaning changes are not).
6. **Runtime sync invariant:** any edit to `/home/lingxufeng/cli/research-os/skills/<s>/SKILL.md` must be
   copied to `~/.claude/skills/<s>/SKILL.md` and verified byte-identical (`diff -q`).
7. Do not touch: `openbuild/` run logs, `plan/archive/`, `opus-pass/` (unless a task names a file there).

---

## Task 1: Executable guard + marker toolchain (`tools/`)

**Repo:** `/home/lingxufeng/huggingface` (work from repo root). TDD: write the test script first (RED), then
the tools (GREEN).

Create/modify these files:

**1a. `tools/exp_verify_mark.sh`** (new) — the mechanical write-through for `/exp-verify`.
Usage: `exp_verify_mark.sh <campaign> <node_id> <verdict> [evidence ...]`
- `<verdict>` ∈ {VERIFIED, FAILED-STRUCTURAL, FAILED-EXECUTION, FAILED-NOOP, FAILED-PLAUSIBILITY}; reject
  anything else (exit 2) and reject node_id containing `/`.
- Writes `openbuild/<campaign>/exp_verify/<node_id>.<verdict>` (mkdir -p) containing: ISO timestamp, verdict,
  and one evidence line per remaining arg. A new VERIFIED marker removes any stale `<node_id>.FAILED-*`
  markers for the same node (re-run after fix), and vice versa (a FAILED write removes a stale VERIFIED).
- Prints the marker path. Idempotent (re-running overwrites).

**1b. `tools/guards/no_adversary_without_expverify.sh`** (modify existing) — change the interface to
`<campaign> <node_id>`; the marker path becomes `openbuild/<campaign>/exp_verify/<node_id>.VERIFIED`.
Keep: PASS (exit 0) iff the VERIFIED marker exists; BLOCK (exit 1) with the expected path + the instruction
to run `/exp-verify` first; node-id `/` rejection (exit 2). Update the header comment: this guard fires
before `/adversary`, before any region-close, and before a backup/substrate promotion.

**1c. `tools/guards/claim_preflight.sh`** (new) — the substrate preflight gate (audit finding 5 + 6, axes
A1/A3/A4/A7 evidence). Usage: `claim_preflight.sh <campaign> <substrate>`.
- BLOCK unless BOTH exist: `openbuild/<campaign>/atlas/venue_taste.md` AND
  `openbuild/<campaign>/preflight/<substrate>.md`.
- BLOCK unless the preflight file contains ALL of these field lines (grep `^FIELD:` allowing leading `- `):
  `FIT-VERDICT:` · `METRIC-PROTOCOL:` · `OCCUPANCY:` · `RECONSTRUCTION:` · `RAW-FAILURES-READ:` ·
  `TYPICAL-PUBLISHED-DELTA:` — on BLOCK, list exactly which fields are missing.
- PASS prints the six field lines found. The guard checks PRESENCE (the loop must have produced the
  artifact); truth is `/adversary`'s job.

**1d. `tools/guards/stale_ref_check.sh`** (new) + `tools/guards/stale_terms.txt` (new) — the doc-drift
tripwire (audit finding 8). The term file ships with one term per line (`#` comments allowed):
`codex:rescue`, `Pro 扩展`, `GPT-5.5 Pro`, `DeepResearch`, `SubagentStop`, `mcp__agentmemory`.
The script greps the LIVE doc set only — `.claude/CLAUDE.md plan/goal-directive.md plan/README.md
plan/operating-manual.md plan/optical-sar-research-plan.md moa/router-protocol.md` (missing files are
skipped with a note, not errors) — PASS if zero hits; FAIL (exit 1) listing file:line:term for every hit.
Historical dirs (plan/Audit, plan/archive) are deliberately NOT scanned.

**1e. `tools/guards/tests.sh`** (new) — the test harness (this is the suite for this task). Using a mktemp
sandbox with fixture campaign dirs, assert at minimum: marker write + path/content; VERIFIED-clears-FAILED
and FAILED-clears-VERIFIED; bad verdict + bad node_id rejected; adversary guard BLOCK-then-PASS around a
marker write; preflight BLOCK on missing file, BLOCK naming a missing field, PASS on a complete fixture;
stale-ref PASS on a clean fixture doc-set and FAIL with correct file:line on a planted term (point the
script at fixture docs via an env override `LIVE_DOCS`/`TERMS_FILE` — add these overrides to 1d).
All tests green before commit; test output pristine.

**Also:** the real live-doc set must PASS `stale_ref_check.sh` at the end of the task (run it for real).

**Commit** (huggingface repo): `git add tools/exp_verify_mark.sh tools/guards/ tools/gpu_queue.py` then
commit `feat(guards): autonomous exp-verify marker + adversary/preflight/stale-ref guards + tests`
(gpu_queue.py is the existing verified scheduler being brought under version control — do not modify it;
exclude any `__pycache__`).

---

## Task 2: research-os skill folds (source + runtime sync)

**Repo:** `/home/lingxufeng/cli/research-os` (separate git repo). No TDD (doc/prompt layer); verification =
the grep assertions below + byte-identical runtime sync. All file paths relative to `skills/`.

**2a. `exp-verify/SKILL.md`** — in the Write-through section add:
> **Mechanical write-through (MANDATORY — no verdict without a marker).** Every verdict is written via
> `tools/exp_verify_mark.sh <campaign> <node_id> <verdict> [evidence…]` (project-side), producing
> `openbuild/<campaign>/exp_verify/<node_id>.<verdict>`. `/adversary`, any region-close, and any
> backup/substrate promotion are BLOCKED by `tools/guards/no_adversary_without_expverify.sh <campaign>
> <node_id>` unless the VERIFIED marker exists. A verdict that lives only in prose does not exist.

**2b. `adversary/SKILL.md`** — three folds:
- In the precondition paragraph (top, where the `/exp-verify` VERIFIED precondition is stated): add
  > Run `tools/guards/no_adversary_without_expverify.sh <campaign> <node_id>` FIRST; a BLOCK ends the pass
  > (run `/exp-verify`, not `/adversary`). The same guard fires before a region-close or backup promotion.
- In "The one invariant (operational)" bullet on `CLAIM_STANDS`: extend the independent-substrate sentence to
  > The reviewer must be a model family NOT listed in the prereg `PROPOSERS:` line. Automated substrates
  > (first choice — the loop self-serves review non-interactively): `codex exec` (GPT) or `agy` (Gemini),
  > context-free, framed to REFUTE; the GPT-5.6 browser is an optional stronger lane. Human review is for
  > exceptional cases only; contribution/paper promotion stays human.
- In check **A** (Δ-reality), append (axis A6):
  > **Worst-case, not only mean (reliability/selective-prediction claims):** report the worst-case
  > accepted-set error over the held-out shift family — the shift chosen to game the confidence signal — not
  > only the average corruption battery.

**2c. `prereg/SKILL.md`** — three folds:
- Contract card: after `MoA-GATE:` add a new line
  > `PROPOSERS:   <every engine/model that generated or refined this design (MoA lanes, external brain,
  >              local agent). The CLAIM_STANDS reviewer must NOT be on this list — cross-family only.>`
- Contract card: after `BRACKET:` add (axis A1)
  > `IDENTIFIABILITY: <attribution/source-separation claims ONLY: the synthetic-injection world where the
  >              latent ground truth (failure source / corruption / conflict) is KNOWN, and the method's
  >              score there. Fail in the known-answer world ⇒ dead before real data. n/a otherwise.>`
- CONFIRMATORY block: add (axis A5)
  > `SLOPE:       <optional but preferred for small-compute claims: Δ at 3 scales/data-sizes/held-out events
  >              + the fitted direction; a Δ that shrinks with scale scopes the claim to small-scale.>`

**2d. `forge/SKILL.md`** — three folds:
- Step 2, at the end (audit finding 6):
  > **New-substrate reconstruction pass (MANDATORY once per substrate).** The FIRST claim-bearing `/forge`
  > on a new substrate/territory carries a reconstruction pass first — the `/prospect` Reconstruction step
  > or the MoA reconstruction mode — and records its output as the `RECONSTRUCTION:` line of
  > `openbuild/<campaign>/preflight/<substrate>.md` (checked mechanically by `tools/guards/claim_preflight.sh`,
  > together with FIT-VERDICT/METRIC-PROTOCOL/OCCUPANCY/RAW-FAILURES-READ/TYPICAL-PUBLISHED-DELTA).
- Step 3, new forcing bullet (axis A2):
  > - **Force ONE data-intervention candidate when the atlas marks the failure signature data-shaped**
  >   (long-tail, coverage gap, label noise, event imbalance): targeted hard-case collection/synthesis,
  >   relabeling, re-weighting, or hard-negative mining — bracketed by its own oracle (train on the fixed
  >   data = the ceiling). The arsenal attacks the DATA as readily as the model.
- Card `FAILURE-SIGNATURE` field (axis A3): extend the field description with
  > `cite the artifact of >=20 raw failure cases actually read (path) — a signature from aggregate metrics
  > alone is not admissible`
- Bump `version:` to 1.1.0 in 2a–2d files (prospect is already 1.1.0).

**2e. `prospect/SKILL.md`** — Mine 2 (literature/survey), add one extraction target (axis A4):
> **negative space + incentive audit** (what the field systematically AVOIDS — unglamorous,
> cross-disciplinary, metric-inconvenient — and the incentive that maintains the avoidance; distinct from
> the future-work graveyard: these were never promised at all. Name the avoided object AND its maintaining
> incentive; the incentive also predicts adoption friction).

**Verification (run, include output in report):**
- `grep -c "exp_verify_mark.sh" skills/exp-verify/SKILL.md` ≥1; `grep -c "PROPOSERS" skills/prereg/SKILL.md
  skills/adversary/SKILL.md` ≥1 each; `grep -c "IDENTIFIABILITY" skills/prereg/SKILL.md` ≥1;
  `grep -c "SLOPE" skills/prereg/SKILL.md` ≥1; `grep -c "data-intervention" skills/forge/SKILL.md` ≥1;
  `grep -ci "negative space" skills/prospect/SKILL.md` ≥1; `grep -c "claim_preflight" skills/forge/SKILL.md` ≥1;
  `grep -c "worst-case" skills/adversary/SKILL.md` ≥1.
- Sync: `for s in prospect forge prereg exp-verify adversary autopsy; do cp skills/$s/SKILL.md
  ~/.claude/skills/$s/SKILL.md; diff -q skills/$s/SKILL.md ~/.claude/skills/$s/SKILL.md; done` — all identical.

**Commit** (research-os repo only): `git add skills/*/SKILL.md` →
`feat(skills): enforcement folds — exp-verify markers, PROPOSERS provenance, identifiability/slope/data-intervention/negative-space/worst-case, new-substrate reconstruction pass` — do NOT push.
Runtime copies are non-git: record them in the non-git diff file per Global Constraint 3.

---

## Task 3: Canon + catalog + memory wiring, PARK line, status stamps, integration check

**Repo:** `/home/lingxufeng/huggingface` (+ non-git files per Global Constraint 3). No TDD; verification =
running the Task-1 guards + grep assertions.

**3a. `.claude/CLAUDE.md`** (gitignored — non-git diff required) — five folds:
- §5 rule 2 (GPU), append:
  > Multi-job training/eval goes through `tools/gpu_queue.py` (one slot per GPU, per-job pinning + log +
  > 6h cap kill); its `gpu_queue_state.json` is the GPU-job monitor registry. A queued job waiting while a
  > GPU idles is a bug.
- §5 rule 3 (Monitor), append:
  > Downloads: arm the watcher/Monitor AT launch (before detach) + a `dl_logs/` entry; a detached download
  > without a live watcher is an ORPHAN (the 22h dead-Xet-partial lesson).
- §4 gate table: in the "Claim boundary `/adversary`" row, append to the Engine cell:
  > requires `tools/guards/no_adversary_without_expverify.sh <campaign> <node>` PASS (also fires before
  > region-close / backup promotion); first claim-bearing `/forge` on a substrate requires
  > `tools/guards/claim_preflight.sh <campaign> <substrate>` PASS.
  And in the DISPATCH row's cell append: `training/eval jobs via tools/gpu_queue.py`.
- §1 Playwright operational rules, add one bullet:
  > **Bank every external-brain session** as `openbuild/<campaign>/pro/<topic>-<date>.md` (the question +
  > the verbatim answer). Raw browser snapshots are never artifacts.
- §3: (i) in the venue-bar bullet add: `venue_taste rows carry a typical-published-Δ column — ACCEPT
  thresholds and MDE are calibrated from it, not guessed`; (ii) in the candidate-reframe bullet replace
  "adoption = human call." with `PARKED — REOPEN-IF: the user adopts it via /goal, or optical-SAR
  region-closes. adoption = human call.`
- §7 key-files: on the research-os line append: `Guards: tools/guards/ (exp-verify marker → adversary gate ·
  claim preflight · stale-ref tripwire) — run them, don't re-derive them.`
- Also §1 independent-review row: change "callable via bash for a specific cross-check" to "callable via
  bash — the AUTOMATED CLAIM_STANDS substrates (cross-family, context-free, non-interactive); the browser
  is the optional stronger lane".

**3b. `plan/aerial-world-model-reconstruction-2026-07-10.md`** — insert directly under the title:
> **STATUS: PARKED (2026-07-10). REOPEN-IF: the user adopts this direction via `/goal`, OR the optical-SAR
> campaign region-closes. Until then no compute; the kill-probe below is the reopen entry point.**

**3c. `plan/taste-bank/FableTrick.md`** — append a new family section in the file's existing style (axis A1):
> ## A8. Identifiability / synthetic-world validation (OSSE)
> Before testing an attribution/source-separation method on real data, build a controllable synthetic world
> where the latent ground truth is KNOWN and injected (leak injectors; OSSE nature-runs; controlled
> misregistration/corruption/conflict generators). The method must recover the known answer there FIRST —
> failing in a known-answer world kills the direction at near-zero GPU cost; succeeding calibrates what the
> real-data signal should look like. Evidence: the water campaign's injectors (GATE-2 5/5) vs the MM-OVSeg
> phenomenon gate that discovered non-separability empirically at much higher cost.
Also add one row to the B.0-style summary table if the file has one (pattern → when → cost).

**3d. Memory `diagnostic-experiment-tricks.md`**
(`/home/lingxufeng/.claude/projects/-home-lingxufeng-huggingface/memory/diagnostic-experiment-tricks.md`,
non-git) — add `identifiability/synthetic-world-first (OSSE)` to the pattern list in the body AND to the
frontmatter description's pattern enumeration (one phrase each).

**3e. Status stamps** (tracked files):
- `plan/Audit/latent-issues-audit-2026-07-10.md` §6: mark items 1/3/4 implemented — append to the section:
  `> IMPLEMENTED 2026-07-10 (plan/sdd-pipeline-enforcement-2026-07-10.md): guards wired (tools/guards/ +`
  `> skills), gpu_queue wired into CLAUDE.md rule 2, PROPOSERS provenance added, aerial-DA PARK line set.`
  `> Item 2 (BRIGHT preflight bundle) is now MACHINE-GATED by tools/guards/claim_preflight.sh — produced by`
  `> the research loop itself, not by this change-set.`
- `plan/Audit/missing-axes-2026-07-10.md`: after the "Adoption rule" section append:
  `> A1–A7 folds IMPLEMENTED 2026-07-10 — prereg (IDENTIFIABILITY · SLOPE · PROPOSERS), forge`
  `> (data-intervention · raw-failures · reconstruction pass), prospect (negative-space mine), adversary`
  `> (worst-case stress), venue-taste Δ column + FableTrick A8. Independence caveat still open: the`
  `> cross-family blind-spot query has not run yet.`
- `plan/phase1-refactor-review-2026-07-10.md` §4: annotate T4 as done:
  `(T4 DONE 2026-07-10 — gpu_queue + guards wired into CLAUDE.md via plan/sdd-pipeline-enforcement-2026-07-10.md)`.

**3f. Integration verification (run for real, paste outputs in report):**
- `tools/guards/stale_ref_check.sh` → must PASS on the live docs.
- `tools/guards/claim_preflight.sh optical_sar BRIGHT` → must BLOCK listing the missing preflight file
  (proves the gate is live for the next `/forge`).
- `tools/guards/no_adversary_without_expverify.sh optical_sar node-2` → must BLOCK (no marker yet).
- `bash tools/guards/tests.sh` → all green.

**Commit** (huggingface repo): `git add plan/Audit/latent-issues-audit-2026-07-10.md
plan/Audit/missing-axes-2026-07-10.md plan/phase1-refactor-review-2026-07-10.md
plan/aerial-world-model-reconstruction-2026-07-10.md plan/taste-bank/FableTrick.md
plan/sdd-pipeline-enforcement-2026-07-10.md` → `docs(pipeline): wire guards/queue into canon, PARK aerial-DA,
A1–A7 fold stamps, FableTrick A8`. CLAUDE.md + memory edits go in the non-git diff file.
