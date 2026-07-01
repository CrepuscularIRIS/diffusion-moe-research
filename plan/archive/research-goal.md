# Diffusion MoE Research Goal — Autonomous Loop Spec

> This document is the single source of truth for the research goal AND the
> operational loop that pursues it. It is designed to be fed directly to
> `/arbor-research-agent` or a `/loop` / goal-mode session. Everything an
> autonomous agent needs to run, review, and self-correct is here.

---

## 0. Ultimate Goal

**Produce a publishable paper** (target: NeurIPS / ICML / ICLR) demonstrating that:

> On verifiable tasks, a **learned commitment policy** (lightweight controller
> on frozen block-diffusion MoE denoiser, trained with trajectory-level RL)
> combined with **timestep-aware MoE routing** closes the quality gap against
> AR MoE at matched compute — and that the gains come from the learned policy,
> not from more compute or bigger models.

Deliverables:
1. Reproducible experiments with clean ablations on DiffusionGemma 26B-A4B
2. Analysis of MoE expert specialization by denoising timestep
3. Paper draft with falsifiable claims backed by controlled experiments

---

## 1. Core Thesis

Diffusion's quality deficit vs AR is not fundamental. The factorization
barrier (L1) is already mitigated by block diffusion. The real gap is
**L2 — heuristic sampling**: commitment/remask decisions are hand-crafted
schedules, not learned. A lightweight learned controller + timestep-aware
expert routing can close this gap in verifiable domains, where diffusion's
"rewrite until correct" advantage over AR's "write once" is maximized.

See `plan/diffusion-moe-first-principles-framing.md` for full theoretical
framing.

---

## 2. Three Directions (sequential dependencies)

```
Direction C (analysis, cheap)
    │
    │  "Do experts specialize by t?"
    │   Yes → justifies routing work
    │   No  → clean negative result, still publishable
    │
    ├──→ Direction SFT (baseline, gate)
    │       │
    │       │  "Does our pipeline produce a working fine-tuned model?"
    │       │   Yes → proceed
    │       │   No  → debug pipeline, do NOT proceed to A
    │       │
    │       └──→ Direction A (main contribution)
    │               │
    │               │  "Does learned commitment beat fixed schedule?"
    │               │   Yes → paper
    │               │   No after 3 seeds → kill direction
    │
    └──→ (C's training experiments also depend on SFT gate)
```

### Direction C — Timestep-Aware Routing Analysis

| Item | Detail |
|------|--------|
| Question | Do MoE experts specialize by denoising timestep t? |
| Method | Inference at various t, record per-layer expert activation distributions |
| Metrics | Entropy, specialization index, load balance, JS-divergence across t |
| Training | None — pure analysis on pretrained checkpoint |
| Cost | Low (~hours) |
| Falsifier | Activation distribution invariant to t → thesis dead |
| Positive result | Experts differentiate → justifies t-conditioned router training |

### Direction SFT — Block-Diffusion SFT Baseline

| Item | Detail |
|------|--------|
| Question | Can we fine-tune DiffusionGemma on GSM8K with our custom pipeline? |
| Pipeline | `diffusiongemma_sft/`: D3PM-uniform corruption, block-causal attention, response-window collation |
| LoRA targets | attention q/k/v/o + dense MLP gate/up/down; experts & router frozen |
| Hardware | 2x RTX 4090 D (96GB), bf16 |
| Gate condition | This MUST succeed before A or C-training proceeds |
| Falsifier | SFT diverges or degrades below pretrained after debugging |
| Blueprint | `plan/diffusiongemma-sft-blueprint.md` |

### Direction A — Learned Commitment Policy (main contribution)

| Item | Detail |
|------|--------|
| Question | Can a learned controller outperform fixed-schedule commitment? |
| Method | Lightweight controller on **frozen** denoiser; trajectory-level RL (GSPO-style IS ratio + group baseline + verifier reward) |
| Narrowing | Small controller network, NOT full denoiser RL (avoids d1/TraceRL overlap) |
| Death sentence | No improvement over fixed schedule at matched compute on B_dev after 3 seeds → kill |
| Key risk | IS variance over long trajectories; validate on short trajectories first |
| Falsifier | No gain at matched compute |

---

## 3. Evaluation Protocol

| Item | Value |
|------|-------|
| B_dev | GSM8K train split — all iteration here |
| B_test | GSM8K test split — **SEALED**, merge verification only |
| Primary metric | exact_match |
| Secondary metrics | NFE-at-parity, expert entropy by t, commitment ratio variance |
| Negative controls | Random controller, trivial baseline (e.g. always-commit) |
| Locality check | Verify gain comes from changed component |
| Seeds | 42, 123, 7 (minimum 3 for statistical significance) |
| Compute matching | Report total FLOPs for both AR baseline and diffusion; Pareto by NFE |

**Sealed invariant**: eval scripts, B_test split, and baseline numbers are
NEVER modified during a run. Any modification → run is contaminated.

---

## 4. Falsifiable Hypotheses

| # | Hypothesis | Kill method | Direction |
|---|-----------|-------------|-----------|
| H1 | Quality gap mainly from L2, not L1 | Block-size sweep + oracle-commitment upper bound | C/A |
| H2 | Learned commitment > fixed schedule at matched compute | B_dev comparison, 3 seeds | A |
| H3 | Trajectory-level IS ratio has manageable variance | Measure ratio variance: toy → short → full | A |
| H4 | MoE experts specialize by timestep t | Activation distribution analysis | C |
| H5 | Timestep-conditioned router > frozen router | Ablation after confirming H4 | C |
| H6 | Combined A+C beats each alone | Component ablation | A+C |
| H7 | Gains generalize beyond GSM8K | Cross-task transfer (code, structured) | A |
| H8 | Diffusion achieves better quality-NFE Pareto than AR | Pareto curve comparison | A |

---

## 5. Reference Architecture: Arbor Loop

This research runs as an **Arbor keyless research loop** inside Claude Code.
Arbor provides: Idea Tree, worktree isolation, dev/test discipline, merge
guard, and structured reporting.

### Entry point

```
/arbor-research-agent <paste this file or describe goal>
```

At intake, load the project-specific profile skill:

```
Skill: diffusion-moe-research-profile
```

This injects: pre-filled research contract, three-engine routing table,
executor science protocol, and IDEATE probe anchors.

### Arbor cycle (one iteration)

```
① OBSERVE   → Read tree state, evidence, frontier, experiment logs
② IDEATE    → Probe Block (Q1-Q4) → 4 idea moves → self-check → TreeAddNode
③ SELECT    → Pick highest-value pending leaf
④ DISPATCH  → Executor implements in isolated worktree → eval on B_dev
⑤ BACKPROP  → Record result, propagate insight upward
⑥ DECIDE    → Merge / prune / continue based on evidence
```

### Who does what (three-engine routing)

| Step | Engine | How to invoke |
|------|--------|---------------|
| OBSERVE | Opus 4.8 | Direct (read tree, logs, code) |
| IDEATE (routine) | Opus 4.8 | Skeptical probe + cross-domain mapping |
| IDEATE (deep) | Playwright → GPT 5.5 Pro | When design is unsatisfying; poll 15min |
| Novelty check | Playwright → DeepResearch | Before merging novel claims; 10-30min |
| SELECT | Codex (GPT-5.5) | `/codex:rescue "Given tree: <TreeView>. Which leaf maximizes info/compute?"` |
| DISPATCH | Opus subagent (worktree) | Agent tool with `isolation: "worktree"` |
| Diff review | Codex (GPT-5.5) | Automatic on subagent completion |
| DECIDE | Codex (GPT-5.5) | `/codex:rescue "Node <id> scored <X> vs trunk <Y>. Merge/prune/continue?"` |

### Arbor MCP tools available

`tree_view`, `tree_add_node`, `tree_update_node`, `tree_set_meta`,
`tree_prune`, `git_merge_branch`, `worktree_create`, `worktree_remove`,
`eval_run`, `generate_report`, `open_dashboard`.

---

## 6. Per-Cycle Review Checkpoints

At the end of EVERY Arbor cycle (after DECIDE), run these 6 checks.
If any check fails, take the prescribed action BEFORE starting the next cycle.

### Check 1: Direction Drift

> "Is the current experiment still serving one of the three directions (C/SFT/A)?"

- Read the node hypothesis and compare against §2 direction definitions.
- If the experiment is exploring something outside C/SFT/A → PRUNE the node.
- If repeated drift (≥2 consecutive off-direction nodes) → pause and
  re-anchor: re-read this goal document, re-read framing doc §5.
- **Why**: research wanders when the optimizer finds interesting tangents.
  Tangents are for future work, not this run.

### Check 2: Hypothesis Fidelity

> "Does the experiment test a pre-declared hypothesis from §4, or is it ad-hoc?"

- Every experiment must map to at least one H1-H8 hypothesis.
- If an experiment produces interesting results but wasn't tied to a
  hypothesis → record it as "exploratory observation", do NOT claim it
  confirms anything. Formulate a new hypothesis for the next cycle.
- If a hypothesis has been tested and killed → mark it dead in the tree,
  do NOT revisit unless genuinely new evidence appears.

### Check 3: Experiment Blocking

> "Is the current direction blocked by a dependency?"

- Direction A blocked if SFT baseline doesn't exist → redirect to SFT.
- Direction C-training blocked if SFT doesn't exist → redirect to SFT.
- Direction A blocked if H3 (IS variance) not validated → do toy validation first.
- SFT blocked by code bug → debug, do NOT start new experiments.
- **Action on block**: log the blocker explicitly in tree metadata, switch
  to the unblocked direction or debug the blocker. Never work around a
  gate by skipping it.

### Check 4: Evidence Quality

> "Is the latest result actually evidence, or just a number?"

- Score improvement alone is NOT evidence. Check:
  - Was there a negative control?
  - Is the gain localized to the changed component?
  - Was B_test untouched?
  - Was the implementation correct (not a bug masquerading as a finding)?
- If any check fails → the result is "inconclusive", not "positive".
  Record it honestly and re-run with proper controls.

### Check 5: Compute Budget

> "Are we spending compute wisely?"

- Check cumulative GPU hours and remaining budget.
- If a direction has consumed >40% of total budget without clear signal →
  escalate: either narrow the experiment or prune the direction.
- Prefer cheap diagnostic experiments (Direction C style) over expensive
  training runs when the mechanism is unclear.

### Check 6: Novelty Integrity

> "Are we still novel, or has someone published this while we were running?"

- Every 3 cycles (or before any merge of a novel claim): run a DeepResearch
  novelty scan via Playwright.
- If prior art found → assess overlap. Partial overlap is OK (cite and
  differentiate). Full overlap → pivot the contribution angle.
- Update tree metadata `related_work` field with scan results.

### Check 7: Review Debt

> "Is there outstanding review debt from the last peer-review panel?"

- If the last `arbor-peer-review-gate` run produced a "Reject→Accept
  Action List", those items are **review debt**.
- Review debt has PRIORITY over new exploratory ideas.
- The next IDEATE cycle must address at least one debt item before
  proposing new directions.
- Debt items are tracked as tree nodes with tag `[REVIEW-DEBT]`.
- Debt is cleared when: the action is implemented AND the next panel
  run no longer flags it as a weakness.
- If debt accumulates (>5 unresolved items) → pause exploration entirely,
  focus all cycles on debt reduction.

---

## 7. Blocking & Recovery Protocols

### Experiment fails to run (code error)

1. Read error traceback carefully.
2. Fix in the experiment branch (not main).
3. Re-run. If fails 3 times → escalate to user or try a different
   implementation approach.
4. Do NOT record a broken run as "negative result."

### SFT training diverges

1. Check: learning rate, gradient norms, data pipeline, mask correctness.
2. Halve learning rate and retry.
3. If still diverges → check corruption/mask/loss implementation against
   `plan/diffusiongemma-sft-blueprint.md`.
4. If fundamentally broken → pause all directions, report to user.

### GPU OOM

1. Reduce batch size (not model precision — stay bf16).
2. Enable gradient checkpointing.
3. If still OOM → reduce LoRA rank or sequence length.
4. Document the constraint in tree metadata for future experiments.

### Playwright disconnected

1. **STOP all Playwright-dependent operations** (DeepResearch, GPT 5.5 Pro).
2. Log: "Playwright disconnected, novelty/deep-reasoning lane unavailable."
3. Continue with Opus + Codex only.
4. Do NOT attempt to restart Playwright — requires human intervention.
5. On next cycle review, flag this to user.

### Codex unavailable

1. Fall back to Opus-only for SELECT/DECIDE (reduced independence but
   functional).
2. Log: "Codex unavailable, single-model mode."
3. Apply extra scrutiny: re-read the science protocol before each merge.

---

## 8. Loop Engineering: How This Runs Autonomously

### Start command

```
/arbor-research-agent Pursue the Diffusion MoE research goal defined in
plan/research-goal.md. Load diffusion-moe-research-profile skill at intake.
Start with Direction C (timestep routing analysis), then SFT baseline, then
Direction A. Follow the three-engine routing and per-cycle review checkpoints
in the goal document. Scope: novelty-leaning, interaction_mode: review,
max_cycles: 8.
```

### One full loop iteration

```
┌─────────────────────────────────────────────────────┐
│  CYCLE START                                        │
│                                                     │
│  ① OBSERVE: read tree + evidence + logs             │
│  ② IDEATE:  probe block → idea moves → self-check   │
│     └─ deep? → Playwright GPT 5.5 Pro (15min poll) │
│  ③ SELECT:  /codex:rescue (which leaf?)             │
│  ④ DISPATCH: Opus subagent in worktree              │
│     └─ on completion: Codex diff review             │
│  ⑤ BACKPROP: record result, propagate insight       │
│  ⑥ DECIDE:  /codex:rescue (merge/prune/continue?)  │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │  PER-CYCLE REVIEW (§6)                      │    │
│  │  □ 1. Direction drift?                       │    │
│  │  □ 2. Hypothesis fidelity?                   │    │
│  │  □ 3. Experiment blocking?                   │    │
│  │  □ 4. Evidence quality?                      │    │
│  │  □ 5. Compute budget?                        │    │
│  │  □ 6. Novelty integrity? (every 3 cycles)    │    │
│  │  □ 7. Review debt? (from peer-review panel)  │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  IF Direction milestone reached:                    │
│  ┌─────────────────────────────────────────────┐    │
│  │  PEER-REVIEW GATE (arbor-peer-review-gate)  │    │
│  │  → 5 reviewer agents (R1-R5) + AC           │    │
│  │  → Verdict + "Reject→Accept" action list    │    │
│  │  → Actions become review debt for next cycle │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  IF all checks pass → next cycle                    │
│  IF any check fails → take prescribed action first  │
│  IF review debt exists → address before new ideas   │
│  IF max_cycles reached → final panel → REPORT.md    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Peer-review gate (publishability check)

At Direction milestones, a full adversarial peer-review panel runs BETWEEN
the DECIDE step and the next cycle. This is the bridge from "it works" to
"it's publishable."

```
Direction milestone reached (C done / SFT done / A has results)
    │
    ▼
Load skill: arbor-peer-review-gate
    │
    ▼
Assemble input packet (claims, evidence, mechanism, novelty, weaknesses)
    │
    ▼
Spawn 5 independent reviewer agents (parallel):
  R1 Soundness      → Opus subagent
  R2 Significance   → Opus subagent
  R3 Novelty        → Codex or DeepResearch
  R4 Rigor          → Codex
  R5 Clarity/Repro  → Opus subagent
    │
    ▼
AC meta-reviewer synthesizes → verdict + "Reject→Accept Action List"
    │
    ▼
Action list items become REVIEW DEBT
  → Review debt has PRIORITY over new ideas in next IDEATE
  → "Need ablation X" → new node
  → "Baseline too weak" → new node
  → "Mechanism unclear" → diagnostic experiment
  → "Prior art missed" → DeepResearch scan
    │
    ▼
Continue Arbor cycle (addressing debt first)
```

**Trigger points**: Direction C complete, SFT baseline established,
Direction A first positive result, Direction A final result (3 seeds),
before REPORT.md. Do NOT run every cycle — only at milestones.

### Stop conditions

The loop stops when ANY of these is true:
- `max_cycles` reached
- All three directions completed or killed
- Compute budget exhausted
- User interrupts
- Unrecoverable blocker (see §7)

On stop: load `arbor-agent-resume-report`, run **final peer-review panel**,
then run final B_test evaluation (if authorized), generate `REPORT.md`
with all artifacts + review verdicts + remaining review debt.

---

## 9. Reference Files

The autonomous loop must know where everything is. Read these as needed:

| File | What it contains | When to read |
|------|-----------------|--------------|
| `.claude/CLAUDE.md` | Always-loaded: routing rules, API keys, Playwright protocol | Auto-loaded every session |
| `plan/diffusion-moe-first-principles-framing.md` | Full theoretical framing, L1/L2/L3 analysis, RL analogy | At INIT, when formulating hypotheses |
| `plan/ai-research-conduct-principles.md` | 8-point science protocol + 11-point arbor constraint | Before every DECIDE (merge gate) |
| `plan/research-method-anatomy.md` | Cognitive protocol: skeptical default, cross-domain mapping | During IDEATE |
| `plan/diffusiongemma-sft-blueprint.md` | SFT pipeline technical blueprint | When working on Direction SFT |
| `plan/arbor-codex-routing.md` | Detailed three-engine routing policy | At INIT, when routing decisions unclear |
| `diffusiongemma_sft/` | Implementation: corruption, mask, collator, loss, dataset, tests | During DISPATCH for SFT/training experiments |
| `/home/lingxufeng/huggingface/.env` | API keys — NEVER commit or log contents | When making API calls |

### Skills to load

| Skill | When |
|-------|------|
| `diffusion-moe-research-profile` | At Arbor intake (auto via description match) |
| `arbor-research-agent` | Entry point |
| `arbor-agent-*` (11 phase skills) | Auto-loaded by orchestrator at appropriate phases |
| `arbor-peer-review-gate` | At Direction milestones + before final REPORT.md |

### Tools available

| Tool | Purpose |
|------|---------|
| Arbor MCP (`tree_view`, `tree_add_node`, etc.) | Idea Tree management |
| Playwright MCP (`browser_navigate`, `browser_snapshot`, etc.) | ChatGPT access |
| Codex Plugin (`/codex:rescue`) | Independent review at gates |
| Standard CC tools (Bash, Read, Write, Edit, Agent) | Implementation |

---

## 10. Success Criteria (final)

### Minimum publishable result
1. ✅ Direction C analysis (positive OR negative) with clean methodology
2. ✅ Working SFT baseline with reproducible numbers on GSM8K
3. ✅ Direction A: statistically significant gain over fixed schedule on
   B_dev AND B_test (3 seeds, p < 0.05)

### Strong result (target)
4. ✅ Component ablation showing A+C > A alone > baseline
5. ✅ Quality-NFE Pareto curve beating matched AR on verifiable tasks
6. ✅ Cross-task generalization (GSM8K → code or structured)

### Stretch
7. ✅ Formal analysis of optimal IS granularity for discrete diffusion
8. ✅ Demonstration on a second model (not just DiffusionGemma)

---

## 11. Model & Hardware

| Item | Value |
|------|-------|
| Model | DiffusionGemma 26B-A4B (`google/diffusiongemma-26b-a4b-it`) |
| Loading | unsloth FastDiffusionModel |
| LoRA targets | attention q/k/v/o + dense MLP gate/up/down |
| Frozen | MoE experts, router (unless Direction C unfreezes router) |
| GPU | 2x NVIDIA RTX 4090 D (48GB each, 96GB total) |
| Precision | bf16 full (not 4-bit) |
| Conda env | `dllm` (PyTorch 2.7.1, transformers ≥5.12.1, unsloth --no-deps) |
