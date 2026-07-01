# DiffusionGemma Research — Plan Index & Flow

> **Start here.** The whole operating model on one screen: the **Arbor research loop** + the **Research-OS
> gate optimizations**. This is the map; `operating-manual.md` is the detailed reference it points to.
> Last updated: 2026-06-30.

---

## The flow (Arbor loop + anti-Goodhart gates)

```
        ┌────────────────────────────────────────────────────────────────────────┐
        │                                                                          │
        ▼                                                                          │
   OBSERVE ──▶ IDEATE ──▶ SELECT ──▶ DISPATCH ──▶ VERIFY ──▶ DECIDE ──▶ BACKPROP ──┘
   (Opus)     (Opus)     (Codex)    (worktree)   (Codex)    (Codex)    (tree FIRST,
   tree +     /ideate    indep.     executor                indep.      then RUNLOG)
   RUNLOG     skeptical  select                 
                │           │           │           │           │
                │           │           │           │           ├─ null → /bank-negative (graded;
                │           │           │           │           │  structural = Codex-CERTIFIED, enforced)
                │           │           │           │           └─ active programme → /programme-audit
                │           │           │           │              (Lakatos progressive/degenerating budget)
                │           │           │           └─ /exp-verify (real run? no-mock, anti-no-op)
                │           │           │              → /reward-hack-audit (real effect? ≥3 seeds,
                │           │           │                neg-control, sealed holdout — Codex)
                │           │           ├─ /context-bundle (freeze: must-read + forbidden-assumptions
                │           │           │  + sealed-split + hashes; fail-closed). ONE 26B GPU job.
                │           │           └─ OBJECT-SHIFT claim → /object-shift-audit (Codex kill-only;
                │           │              T1–T6 + DPC; ELIGIBLE machine-enforced, not a contribution)
                │           ├─ NEW direction → /taste-critic KILL-gate (He-bar, independent)
                │           │  + preregister {hypothesis, falsifier, acceptance, metric, neg-control}
                │           └─ OBJECT-SHIFT direction (front-half) → /mos-front (is this the right
                │              modeling OBJECT? SKIP_TACTICAL / MOC_LITE / MOC_FULL + DPC)
                └─ deep design / novelty → route to GPT-5.5 Pro (Playwright, `Pro 扩展`)

   cross-system "beats X" claim, anywhere → /baseline-champion (independent adversary, veto)

   ════════════════════════════════════════════════════════════════════════════════
   PROMOTION to "contribution" / paper / "architecture advantage" is NOT a loop output.
   It HARD-BLOCKS → human (or external decider). The loop only banks EVIDENCE and advances.
```

The loop is autonomous for **SEARCH + FALSIFICATION**. It is **not** autonomous for **defining success,
broadening scope, or declaring a contribution** — those terminate off the proposer (the gate asymmetry below).

---

## "Arbor" vs "our optimizations" (what's borrowed vs what we added)

| Layer | Source | What it is |
|---|---|---|
| Idea **tree** (`tree_view/add/update/prune`), worktree isolation, loop shape | **Arbor MCP** | the canonical research STRUCTURE — branches, status, result, insight, prune |
| **Goal-mode** as the driver (replaced the deprecated `arbor-cycle` skill loop) | ours | human-in-loop continuous loop; `goal-directive.md` is the input |
| **Multi-engine isolation** (Opus proposes · Codex selects+reviews · Pro designs/audits) | ours | the generator never selects or self-evaluates |
| **7 anti-Goodhart gates + taste asymmetry** | ours | the optimization this repo is "the previous framework + …" — see below |
| **Enforceable-contract discipline** (machine-checked, not prose) | ours | a gate invariant must be a runnable validator + tests, not a SKILL.md sentence |
| **Science kernel** (falsify-before-build · sealed eval · one-variable · neg-controls) | ours | gates every move; negatives = success |

---

## The gates (the "optimizations") — one line each

**Front-half — MOS-Front GENERATOR** (is this the right modeling object? — fires at IDEATE→SELECT; design: `mos-front-architecture.md`):
| Gate (command) | Fires at | Strong verdict is… |
|---|---|---|
| **/mos-front** | IDEATE (object-shift direction) | Opus GENERATES (SKIP_TACTICAL / MOC_LITE / MOC_FULL + DPC); never self-certifies |
| **/object-shift-audit** | SELECT (object-shift claim) | `ELIGIBLE` ⇒ **Codex independent + machine-enforced** (T1–T6 + DPC; "S predicts failure" ≠ sufficient) |
| **/programme-audit** | BACKPROP (active programme) | `PROGRESSIVE` ⇒ **independent + machine-enforced** Lakatos budget score (hard-core-edit = −4) |

**Back-half — FILTER** (is the result real/honest?):
| Gate (command) | Fires at | Strong verdict is… |
|---|---|---|
| **/taste-critic** | SELECT (new direction) + pre-promotion | KILL = autonomous; **PASS = human/external** (never proposer-self-granted) |
| **/context-bundle** | DISPATCH | fail-closed frozen context; missing piece ⇒ no dispatch |
| **/exp-verify** | post-run | 3-stage real-run check (no-mock, anti-no-op log_assertion) |
| **/reward-hack-audit** | DECIDE / pre-promotion | CLEAN ⇒ **Codex independent** (≥3-seed, neg-control, sealed holdout, token-shuffle) |
| **/baseline-champion** | any "beats X" claim | dominance sign-off ⇒ **independent adversary**, veto |
| **/bank-negative** | DECIDE (null) | `scoped` self-grade OK; **`structural` = Codex-certified, machine-enforced** |
| **/claim-evidence-matrix** | pre-paper | every claim → typed evidence or auto-downgrade to hypothesis |

**The governing invariant:** *"would gaming this verdict help the proposer? then the proposer can't grant
it."* The proposer self-administers only **conservative/DOWNward** verdicts (kill, scoped-negative,
claim-downgrade); every **strong/consequential** verdict runs on an independent substrate (Codex/Pro) and,
for anything written up as a contribution, terminates in a human/external decider.
Design + grounding: `research-operating-system.md`. Routing table: `operating-manual.md §5.1`.

---

## Core docs (live)

| Doc | Role |
|---|---|
| **operating-manual.md** | THE how-we-work reference: engines, the loop, GPU/process safety, lessons, science kernel, §5.1 gate routing |
| **goal-directive.md** | the exact `/goal` input (current = **Track 3** SC-target adapter training) |
| **research-operating-system.md** | the BACK-half (filter) design — the 7 gates, the asymmetry, the enforceable-contract pattern |
| **mos-front-architecture.md** | the FRONT-half (generator) design — Modeling-Object-Shift, the DPC keystone, the 3 front gates, the Lakatos programme |
| **frozen-pareto-negative-synthesis.md** | Track 2 banked structural NEGATIVE (7 kills converge on native Pareto) — the lever for Track 3 |
| **paper-draft.md** / **paper-outline.md** | Track 1 wall-clock-frontier paper (COMPLETED; parked) |
| **ideas-he-level-frozen-dllm.md** / **ideas-gradient-field.md** | active ideation shortlists / substrate |
| **research-method-anatomy.md** | cognitive protocol (skeptical default · cross-domain · first-principles · falsifiability) |
| **ai-research-conduct-principles.md** | the science conduct protocol (8-point kernel) |
| **methodology-harvest.md** / **methodology-portable.md** | the 16-repo methodology synthesis + portable extraction recipe |
| **priorart_pdfs/** | raw prior-art PDFs |

> Prior-art landscape for the active track lives at repo root: `HekaiMing.md`.

## Archived (`plan/archive/`)
Superseded / one-off / already-distilled: the `gpt55pro-*` Pro query logs, `n2-amendment-*` and
`research-redesign-*` (superseded redesigns), `deep-research-report (2).md` (distilled into the harvest),
`rescue-audit-protocol.md` + `saturation-experiment-protocol.md` (dead protocols), and `extraction/` +
`ros-review/` (already synthesized into `methodology-harvest.md` + `research-operating-system.md`). Nothing
deleted — all moved for reference.
