# Research Plan — Index

> **Start here.** This file is a lightweight map. Active truth lives in `.claude/CLAUDE.md`,
> `plan/goal-directive.md`, `moa/router-protocol.md`, the research-os skills, and the current campaign artifacts.
>
> **CURRENT DIRECTION (adopted 2026-07-12): WORLD MODELS → Information Sciences + AAAI.** The contribution is
> the decision-relevant scientific claim (uncertainty / exploitability / event-triggered re-anchoring /
> context-adaptation family); the world model is the vehicle. Knowledge layer = `WorldModel/`; env =
> `/data/projects/world-model-lab/` (user-managed). Status detail = `.claude/CLAUDE.md` §3.

## Active Thesis

**One objective, one constraint.** Optimize everything for research competitive at top-tier Information Sciences
and AAAI. The only hard constraint is wall-clock + compute cost — priced per launch ({ETA · GPU-hours ·
expected info-gain · kill-checkpoint}), never hard-capped. The quality invariants that never relax: independent
context-isolated verification of important conclusions, sealed evals + artifact-read numbers, reproduce-first +
cheap-probe-first. Everything else is an editable design choice (`.claude/CLAUDE.md` §0).

## Core Docs

| Doc | Role |
|---|---|
| `.claude/CLAUDE.md` | design principles, engine division, live state, operating rules |
| `plan/goal-directive.md` | exact `/goal` input: objective + the one constraint + invariants |
| `plan/wm-consistency-index-directive-2026-07-14.md` | ACTIVE plan-of-record (campaign world-model-v2, directive v2: WS1–WS4 workstreams + Go/No-Go gates; writing paused) |
| `plan/world-model-direction-2026-07-11.md` | ARCHIVED — first world-model campaign's plan (restarted from scratch 2026-07-13) |
| `plan/world-model-strategy-digest-2026-07-11.md` | operational strategy (routes · baselines · envs · decision-centric eval) |
| `plan/world-model-field-analysis-chatgpt-2026-07-11.md` | external-brain field map (broader context) |
| `WorldModel/` | domain knowledge layer: operator bank (`wm-operator-bank-report.md`) + trick bank (`Trick.md`) + reconciliation (`README.md`) |
| `judgment/` | the judgment ledger: append-only forecast rows + curated calibration priors — the pipeline's model of its own research judgment |
| `moa/router-protocol.md` | MoA routing and model panel (domain-bank-first operator retrieval) |
| `plan/opencode-moa-architecture-2026-07-14.md` | OpenCode-MoA layer (advisor/jury/librarian roster + lanes) — T1–T5 SHIPPED · T6 sync · user script deep-fix pending |
| `opus-pass/operators.md` | de-domained general taste-operator bank |
| `plan/taste-bank/` | general diagnostic-trick catalog (FableTrick/SolTrick) |
| `plan/operating-manual.md` | reference/history only; does not override goal/CLAUDE |
| `plan/research-method-anatomy.md` | cognitive protocol |
| `plan/ai-research-conduct-principles.md` | science conduct protocol |

## History / Archive

Closed-campaign evidence (aerial-VLN, optical-SAR/BRIGHT, dLLM, VLA, water, BEV/C5, TbV/C2, …) lives in the
**memory topic files** + **`openbuild/<campaign>/`** + **`plan/archive/`** — it is not indexed in live canon.
Re-entry into a closed domain is a user call.

## Loop

ResearchOS v1.1:

```text
/prospect -> /forge -> /prereg -> run -> /exp-verify -> /adversary -> /autopsy
```

One invariant:

> A verdict that helps the proposer if gamed must never be granted by the proposer.

Proposer self-administers DOWN only. `CLAIM_STANDS` requires an independent substrate; final contribution/paper
promotion is human-granted.
