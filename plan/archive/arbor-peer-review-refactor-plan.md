# Arbor Peer-Review Gate — Refactor Plan (diff-level)

v0.1 · scope = **wire the existing `arbor-peer-review-gate` into Arbor's master
instruction** and formalize the review-debt feedback loop · trigger policy =
**every Direction milestone** (+ a final pre-REPORT panel). Plan-only — no code
touched yet; this is the spec to review before editing.

Companion docs: `arbor-codex-routing.md` (3-engine routing), the gate skill
itself (`~/.claude/skills/arbor-peer-review-gate/SKILL.md`).

---

## 0. TL;DR

- The gate skill **already exists and is good** (5 reviewers + AC meta-review,
  GPT-5.5 authority, input packet, output format, Reject→Accept feedback,
  OpenReview calibration, honest limits). It is **project-tailored** (DiffusionGemma,
  Directions A/C, d1/TraceRL/CoDD prior art) and references `plan/research-goal.md §6`.
- The only gap: it's an **orphan** — not in any master instruction, so it never
  runs as a first-class phase, the review-debt loop isn't formalized, and it's
  missing from Codex.
- This refactor = **graft + formalize**, not new logic. 3 SKILL.md edits + 1 new
  artifact + install/sync. Native-runtime changes are an optional appendix (§6).

---

## 1. What exists vs what's missing

| Piece | State |
|---|---|
| `arbor-peer-review-gate` reviewer logic | ✅ exists (264 lines, Claude only) |
| Registered in `arbor-research-agent` Bootstrap Sequence | ❌ missing |
| In `arbor-agent-orchestrator` Phase Loading Order | ❌ missing |
| Triggered from `arbor-agent-coordinator` DECIDE | ❌ missing |
| `review_debt` artifact + OBSERVE consumes it | ❌ missing |
| Installed in Codex (`~/.codex/skills`) + CCC snapshot | ❌ missing (Claude only) |
| Native runtime (`prompts.py`) aware of it | ❌ missing (deferred, §6) |

---

## 2. Target control flow (the new master loop)

```
INIT → [loop:]
  OBSERVE
    └─[NEW] read review_debt FIRST. Non-empty ⇒ debt items are the
            mandatory IDEATE inputs this cycle (priority over new directions).
  IDEATE (consume review debt → ablation / stronger-baseline / diagnostic /
          positioning / claim-rewrite nodes; only then explore new ideas)
  SELECT → DISPATCH → BACKPROP
  DECIDE  (metric gate, unchanged: merge / prune / continue / stop)
    └─[NEW] Direction-milestone check:
            if a depth-1 Direction hit a milestone (§3)
              → load arbor-peer-review-gate
              → assemble Input Packet (gate §3) from tree artifacts
              → 5 reviewers + AC meta-review (GPT-5.5 authority)
              → append AC "Reject→Accept action list" to review_debt[direction_id]
  loop back to OBSERVE
[before REPORT.md:]
  → FINAL full panel = pre-submission review.
    Unresolved [FATAL]/[MAJOR] weaknesses are logged as REPORT caveats,
    not silently dropped.
```

Key principle (from the gate skill §5): **review debt has priority over new
ideas.** The metric gate (merge-eval) and the publishability gate (peer-review)
are two separate gates; peer-review sits ON TOP, never replaces merge-eval.

---

## 3. "Direction milestone" — the trigger predicate (precise)

A **Direction** = a depth-1 Idea Tree node (broad strategy). With trigger policy
= *every Direction milestone*, the **full panel** fires when a depth-1 Direction
transitions through any of:

1. **First positive** — the Direction's first depth-2 child reaches `status=done`
   with `score` beating `baseline_score` (or `trunk_score` if set).
2. **Child merged** — any descendant of the Direction reaches `status=merged`.
3. **Direction concluded** — the Direction is about to be pruned/closed (so its
   net lesson gets reviewed before it's filed away).

Plus two policy points from the gate skill §6:
- **Baseline established** → *quick* panel (R4 rigor + R5 reproducibility only).
- **Before `REPORT.md`** → *final full* panel (the pre-submission review).

Dedup guard: hash the Direction's claim+evidence; do not re-run the full panel on
an unchanged Direction state (mirror the subagent-review diff-hash pattern).

---

## 4. File-by-file changes (skill layer — primary)

### 4.1 `arbor-research-agent/SKILL.md` — register the skill

**Anchor** (Bootstrap Sequence, step 3 list). Add the gate to the loadable set
and a milestone note:

```diff
 3. Let the orchestrator load phase skills as needed:
    - `arbor-agent-coordinator`
    - `arbor-agent-ideate`
    - `arbor-agent-executor`
    - `arbor-agent-merge-eval`
    - `arbor-agent-search`
    - `arbor-agent-plugins-hitl-budget`
    - `arbor-agent-resume-report`
    - `arbor-agent-tools`
+   - `arbor-peer-review-gate`
+4. At every Direction milestone and once before `REPORT.md`, the orchestrator
+   loads `arbor-peer-review-gate` (publishability gate on top of merge-eval).
```
(renumber the old step 4 "Keep the user-facing behavior…" → 5.)

Also add to **Hard Rules**:
```diff
+- Do not present a novel/scientific claim as a contribution in REPORT.md until
+  it has passed `arbor-peer-review-gate`, or its unresolved [FATAL]/[MAJOR]
+  weaknesses are logged as explicit caveats.
```

### 4.2 `arbor-agent-orchestrator/SKILL.md`

**(a) Phase Loading Order — add Phase 10:**
```diff
 9. **No native Arbor tools**: load `arbor-agent-tools`.
    ...
+10. **Peer-review gate (publishability)**: load `arbor-peer-review-gate` at
+    every Direction milestone (a depth-1 Direction's first positive result, a
+    descendant merge, or the Direction being concluded) AND once before
+    `REPORT.md`. It runs a 5-lens reviewer panel + AC meta-review with GPT-5.5
+    as the authority, and appends a Reject→Accept action list to `review_debt`.
+    This is a gate ON TOP of merge-eval (metric), not a replacement.
```

**(b) Minimal Run Skeleton — insert into the per-cycle loop and finalization:**
```diff
    - Load `arbor-agent-merge-eval`; merge, prune, or continue.
+   - If a depth-1 Direction hit a milestone (see arbor-peer-review-gate §3 /
+     orchestrator Phase 10), load `arbor-peer-review-gate`; append its AC action
+     list to `.arbor/sessions/<run>/review_debt.md`.
 4. Load `arbor-agent-resume-report`; run final B_test ...; 
+   run a FINAL `arbor-peer-review-gate` panel before writing `REPORT.md`;
    write `REPORT.md`; summarize artifact paths.
```

**(c) Non-Negotiable Invariants — add two:**
```diff
+- Review debt has priority over new ideas. If `review_debt.md` has open items,
+  the next IDEATE MUST address them before exploring a new Direction.
+- The publishability gate is separate from the metric gate. merge-eval decides
+  "did it beat the metric"; `arbor-peer-review-gate` decides "would reviewers
+  accept it". A merge can pass the metric gate and still owe review debt.
```

**(d) Common Failure Corrections — add one:**
```diff
+- If a Direction reached a milestone but no peer-review ran, the run is
+  "metric-validated but unreviewed" — run the gate before treating that
+  Direction's claim as a contribution.
+- If review_debt is non-empty but IDEATE explored a new tangent, restart IDEATE
+  and consume the debt first.
```

### 4.3 `arbor-agent-coordinator/SKILL.md`

**(a) Step 1 OBSERVE — consume review debt first:**
```diff
 ### Step 1: OBSERVE

+First, read `review_debt.md` for this run. Review debt has priority: any open
+Reject→Accept item from `arbor-peer-review-gate` becomes a mandatory IDEATE
+input THIS cycle, before any new direction. Classify each item (gate §5):
+ablation → experiment node · weak baseline → stronger-baseline node · unclear
+mechanism → diagnostic node · missing prior art → DeepResearch + related_work ·
+overclaim → claim rewrite (no experiment) · missing error bars → re-run w/ seeds.
+
 Read code, logs, prior experiment reports, tree insights, failure cases, and
 score patterns. Focus on failure classes and bottlenecks, not just symptoms.
```

**(b) Step 5 DECIDE — add the milestone trigger after the metric bullets:**
```diff
 - Stop: cap/budget reached, diminishing returns, or no pending ideas.

+**Direction-milestone peer review (publishability gate).** After the metric
+decision, check whether a depth-1 Direction hit a milestone: (1) first child
+`done` beating baseline, (2) a descendant `merged`, or (3) the Direction is
+being concluded. If so, load `arbor-peer-review-gate`, assemble its Input
+Packet from the tree (claim, evidence, mechanism, novelty, known weaknesses,
+TreeView markdown), run the 5+AC panel (GPT-5.5 authority), and append the AC
+Reject→Accept action list to `.arbor/sessions/<run>/review_debt.md` keyed by the
+Direction id. Do NOT re-run on an unchanged Direction state (claim+evidence
+hash). This gate never blocks a merge — it produces debt the next cycle must pay.
+
 Before stopping, run final B_test only if it is available, the contract permits
```

**(c) Idea Tree schema note** (Tool Mapping / schema section) — document the new
artifact so resume/report tooling preserves it:
```diff
+Session artifact: `review_debt.md` — open Reject→Accept items from
+`arbor-peer-review-gate`, keyed by Direction id, each marked open/addressed.
+Preserve it across resume (arbor-agent-resume-report) alongside the tree.
```

### 4.4 New artifact — `review_debt.md` (schema + lifecycle)

Path: `.arbor/sessions/<run>/review_debt.md`. Markdown so OBSERVE reads it and
IDEATE consumes it without new tooling. Lifecycle:

```
DECIDE (milestone) → gate appends:
  ## Direction <id> — reviewed <cycle N>  (AC decision: <accept|borderline|reject>)
  - [ ] [MAJOR] add ablation removing X            (→ experiment node)
  - [ ] [MAJOR] baseline B is too weak, add B'      (→ baseline node)
  - [ ] [MINOR] cite prior art Z                     (→ DeepResearch)
OBSERVE next cycle → reads open `- [ ]` items → IDEATE turns them into nodes →
when the node lands, coordinator checks the box `- [x]`.
REPORT → any remaining `- [ ]` [FATAL]/[MAJOR] become explicit caveats.
```
(Optional: also mirror into tree metadata via `arbor_state.py meta --set` so the
WebUI/dashboard can surface review debt. Not required for v0.1.)

### 4.5 Install / sync

```
arbor install --codex            # gate is Claude-only now; add to ~/.codex/skills
cp ~/.claude/skills/arbor-peer-review-gate/SKILL.md  →  CCC snapshot (if tracked)
```
Update `MEMORY.md` pointer + `arbor-codex-routing.md` (add the DECIDE→peer-review
row to its 6-step table).

---

## 5. Trigger / cost policy — "every Direction milestone"

| Event | Panel | Agents |
|---|---|---|
| Direction first-positive | FULL | 5 + AC |
| Direction descendant merged | FULL | 5 + AC |
| Direction concluded | FULL | 5 + AC |
| Baseline established | QUICK (R4+R5 only) | 2 + AC |
| Before REPORT.md | FINAL FULL (calibrated) | 5 + AC |

Cost is real: a full panel = 6 GPT-5.5 calls. "Every Direction milestone" with
~3–5 Directions and 2–3 milestones each ⇒ tens of panels per run. Mitigations:
- **Claim-hash dedup** — never re-run on an unchanged Direction state.
- **Quick panel** (R4+R5) for baselines/low-stakes milestones.
- **GPT-5.5 pool is independent** of Spark/Opus quotas (per your setup), so panel
  cost doesn't compete with implementation — but Deep-Research (R3) is browser-
  driven and slower; cap R3's lit-scan depth.
- Routing per gate skill §2: R1/R2/R5 → Playwright→GPT-5.5; R3/R4/AC → Codex
  GPT-5.5; AC MUST be GPT-5.5 (not Opus) to avoid author-is-editor bias.

---

## 6. Native-runtime appendix (optional — only if you later run `arbor` CLI)

Not needed for keyless-in-CC. If/when you run the native Python runtime:

- `src/coordinator/prompts.py`:
  - add `_peer_review_section(config)` and include it in
    `build_coordinator_system_prompt()` (after `_decision_section`).
  - in `_arbor_cycle_protocol_section`, add **"### Step 6: PEER-REVIEW"** after
    DECIDE describing the milestone trigger + review-debt loop.
- `src/coordinator/config.py`: add `peer_review_enabled: bool`, `peer_review_mode:
  Literal["off","milestone","final-only"]`, and a `review_debt` store.
- Reviewer fan-out would need a tool (e.g., reuse the SearchAgent dispatch
  pattern) — heavier; the skill layer gets you the behavior without forking Arbor.

> Recommendation: do the **skill layer only** first (zero Python, keyless-live).
> Treat the native layer as a later port if you move to API-key runs.

---

## 7. Validation plan (before declaring done)

1. **Static**: after edits, have GPT-5.5 (codex exec) verify the three SKILL.md
   files are internally consistent (phase numbers, cross-refs, the OBSERVE/DECIDE
   loop closes).
2. **Smoke**: a dry run where a fake Direction hits "first-positive" → confirm
   the orchestrator loads the gate, a `review_debt.md` is written, and the next
   OBSERVE reads it as priority input. (Can mock the panel to 1 reviewer to save
   quota during plumbing.)
3. **One real panel**: on an actual diffusion Direction milestone, run the full
   panel once; confirm the AC action list lands in review_debt and is sensible.

---

## 8. Rollout & risks

- **Advisory first**: the gate produces debt + caveats; it never blocks a merge
  or hard-stops the run. Keep it that way until calibrated.
- **Calibrate** (gate §7) against real OpenReview reviews in discrete-diffusion /
  diffusion-RL / MoE-routing BEFORE trusting scores.
- **Honest limit** (gate §8): simulated review ≠ real review. Value is the action
  list, not the scores. Treat as pre-mortem.
- **Cost discipline**: "every milestone" is the expensive setting you chose —
  keep the claim-hash dedup and quick-panel tiers on, or it balloons.

---

## 9. Execution checklist (when you approve)

- [ ] 4.1 edit `arbor-research-agent/SKILL.md`
- [ ] 4.2 edit `arbor-agent-orchestrator/SKILL.md` (a–d)
- [ ] 4.3 edit `arbor-agent-coordinator/SKILL.md` (a–c)
- [ ] 4.4 define `review_debt.md` lifecycle (doc in coordinator skill)
- [ ] 4.5 `arbor install --codex` + CCC sync + MEMORY/routing-doc update
- [ ] 7.1 static GPT-5.5 consistency check
- [ ] 7.2 smoke run
- [ ] 7.3 one real calibrated panel
```
