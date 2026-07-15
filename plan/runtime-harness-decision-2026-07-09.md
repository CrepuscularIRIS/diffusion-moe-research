# Runtime / Harness Decision — 2026-07-09

> Companion to `plan/workflow-audit-2026-07-09.md` (human/procedural audit) + the Claude
> systematic-debugging audit (same day). This file answers the open architectural fork:
> **fix the pipeline by doc-refactor, or by building/adopting an enforcing harness+runtime?**

## 1. The question (user's framing)

> "Arbor is not used properly, the pipeline is really heavy, the model may not follow prompt
> instructions and regulations. That requires a good harness and runtime — maybe we need this."

Two ways to go: **(Way 1)** bounded workflow refactor (tighten the docs, then launch the prompt-based
loop). **(Way 2)** build/adopt an enforcing harness+runtime so the model *cannot* skip steps.

## 2. What the evidence says (both audits CONVERGE)

Prompt-mandated rules are skipped systematically:
- No `optical-sar` Arbor tree though "tree-first at each verdict" is a rule; `.arbor/active-run` still
  = `aerial-vln`.
- No `/prereg` for the reproduction; the documented loop puts `/forge` **before** the baseline, contradicting reproduce-first.
- `adversary/SKILL.md` + two memory files still name the DELETED Codex auto-hook as the independent
  substrate → the `CLAIM_STANDS` invariant *looks* enforced but isn't.
- A co-proposer (Codex) can be reused as its own "independent" reviewer (reviewer-provenance unenforced).
- `HF_TOKEN` appeared in a download's argv (P0.4). 23/25 recent commits are tooling; **0 research numbers.**

**Diagnosis:** this is NOT "try harder to follow the prompt." At ~50 KB+ of manual+goal+router+skills held
in context every turn, an LLM WILL drop rules. **Prompt-based enforcement of a heavy pipeline is
structurally unreliable.** The user is right on the core point.

## 3. Verdict — updates my prior "don't build," with two corrections

**Conceded:** structural enforcement (a harness) is the durable fix for the compliance failure;
discipline-by-prompt is not. My earlier "just use discipline + go do research" underweighted how
unreliable prompt-compliance is at this pipeline weight.

**But the fork is a false binary — the two ways are SEQUENTIAL phases, not alternatives:**

1. **You cannot harness your way out of a bloated rule-set.** A harness that enforces a contradictory,
   duplicated doc-set just enforces the wrong thing faster. Both audits independently found "too many
   duplicated authorities." So **SIMPLIFY FIRST** — reduce to a small, non-duplicated, *testable*
   invariant-set (the human audit §4 hierarchy is the target). A light pipeline is one that BOTH the model
   can follow AND a thin harness can enforce.
2. **"Build a runtime" → "ADOPT comet + a few guards."** `@rpamis/comet` ALREADY is this runtime
   (per-change `.comet.yaml` state-machine + executable phase-guards + resumability + eval), a mature,
   tested npm package. Building a similar repo from scratch reinvents it AND is the maximal process
   investment at the exact moment the anti-accretion breaker fired. Adopt comet's guard mechanism (or comet
   itself) to enforce a SHORT invariant list — a thin guard layer, **not a new runtime repo**.

## 4. Recommended path: SIMPLIFY → ENFORCE (sequenced, time-boxed)

**Phase 1 — Simplify (the bounded refactor both audits demand).** Collapse duplicated authorities into the
audit §4 hierarchy (goal → manual → track-launch-contract → runtime manifests → Arbor → RUNLOG); move
history to `plan/archive/`; each surviving rule unique + concise + testable. Close the P0 drift (Arbor
active-run, reproduction contract, `/forge`-vs-reproduce ordering, credential-in-argv). **Target: the
invariant-set fits on one page.**

**Phase 2 — Enforce the few HARD invariants with a THIN harness (adopt comet OR ~6 git-hook guards).**
Enforce these as *executable* checks, never prose:
- `.arbor/active-run` == the current campaign before any node write.
- No claim-run without a sealed `/prereg` artifact (reproduce-first ordering baked in).
- No `CLAIM_STANDS` without an independent-verdict artifact from a **non-proposer** (reviewer-provenance).
- No secret in argv.
- A monitor-registry entry exists for every outliving wait.

**That short list IS the whole harness.** If comet's state-machine fits our loop, adopt it; else a thin
guard layer. Nothing more.

## 5. Guardrail — so the harness does not become the product

- Time-box Phase 1+2 HARD. The deliverable is still the **MM-OVSeg reproduction**, not the harness.
- The harness enforces only the ~6 invariants. If it grows past one page of guards, STOP — that is re-accretion.
- Do NOT build a from-scratch runtime repo. That answer stays **NO**. Adopt/borrow, don't rebuild.

## 6. Kill / revisit conditions

- If Phase 1 (simplify) alone makes the loop followable in a dry-run, Phase 2 may be deferred.
- If comet-adoption doesn't fit inside the time-box, fall back to the ~6 git-hook guards.
- Revisit "build our own" only if BOTH simplification AND comet-adoption fail AND compliance still breaks —
  evidence first, infrastructure last.

## 7. One-line answer

**Not a from-scratch runtime — but yes to structural enforcement: SIMPLIFY the pipeline to a one-page
invariant-set, then ADOPT comet (or ~6 guards) to enforce it. Time-boxed, thin, and it must not defer the
MM-OVSeg reproduction — which is the actual deliverable.**
