# research-os v1.0

> **Taste is a prior over expected-information-per-effort, and it acts BEFORE evidence exists.** A filter
> stack can only subtract; generative taste creates the value. So this system protects exactly two things —
> **the generator** and **the one invariant** — and refuses to grow anything else.

## The one invariant

> **A verdict that helps the proposer if gamed must never be granted by the proposer.**

- The proposer self-administers **DOWN verdicts only** (kill, downgrade, scope-shrink).
- **`CLAIM_STANDS` requires an independent substrate** — a fresh context the proposer did not curate
  (a dispatched reviewer, an automatic review hook, an external model).
- **Promotion to a contribution terminates in the human.**
- Corollary: **memory is not evidence** — the proposer may not upgrade its own recollection ("this is
  novel", "the number was X") into evidence. Novelty needs a live search; numbers are read from artifacts
  **this session** (artifact-fidelity).
- Silence is never a pass. A failed independent pass is answered point-by-point, never re-rolled.

## The loop — 6 commands: 3 generate, 3 discipline

```
/prospect ──▶ /forge ──▶ /prereg ──▶ run ──▶ /exp-verify ─┬─ claim? ──▶ /adversary ──▶ (human)
    ▲            ▲                                        └─ null?  ──▶ /autopsy ──┐
    │            └── new/reshaped candidates ◀─────────────────────────────────────┤
    └──────────────── region-close → lateral jump ◀────────────────────────────────┘
```

| Command | One line |
|---|---|
| **/prospect** | hunt problems from five mines (own-log anomalies FIRST) → ranked problem cards `{Q, TYPE, WHY-NOW, STAKES, PROBE, SURPRISE}` |
| **/forge** | one problem → 3–5 candidates through the four axes (forced rival school · forced off-frame with DIFF-PREDICTION · forced rotated operator) + the REGENERATION RULE |
| **/prereg** | freeze the evidence contract before any claim-bearing run; sealed eval layer; exploration stays free |
| **/exp-verify** | the run is real: no mock → executed on real data → anti-no-op (the intervention provably FIRED) |
| **/adversary** | THE claim-boundary gate — four TYPE-scoped checks; the one invariant lives here |
| **/autopsy** | every death feeds the generator: boring-first triage → mechanism-level why → THE CONVERSION LAW; carries the two continuous reflexes |

Most work never sees a gate. **Exploration is free.** Discipline binds at exactly three late moments:
before a cited run (`/prereg`), after any run (`/exp-verify`), at the claim boundary (`/adversary`).

## The four axes (the anti-monoculture forcing — this is essence, not ceremony)

**Schools** = how to think · **types** = what output · **frames** = which mathematics · **operators** =
which object-move. The generator samples the model's prior, so unforced output is monoculture. `/forge`
forces one candidate off each axis per round — one, rotated, **never a sweep** (sweeping is the menu
disease). Every off-axis candidate must carry a **DIFF-PREDICTION**: an observable the new frame/object
predicts that the incumbent cannot. *No differential ⇒ vocabulary, not an idea ⇒ discard* (the deletion
test: strip the new words; if no prediction disappears, it is relabeling).

References (the optional palettes the generator reaches for): `taste.md` · `schools.md` · `frames.md` ·
`taste-operators.md` · `research-types.md`. **Name the TYPE first; verify by type.**

## The two continuous reflexes (formerly a scheduled command)

1. **Surprise accounting** — the unit of progress is a SURPRISE: an observation that changed the plan.
   Zero surprises across recent cycles = farming process → force a generator move.
2. **Type-drift** — are recent artifacts the TYPE the goal asked for, or have they slid toward
   gate-friendly certificate work? Name the next ON-type artifact and dispatch it.

Both run inside `/autopsy`'s programme pulse and any time the loop feels stuck. Advisory; they redirect,
never block.

## Evidence taste (the reflex that saves compute)

**Cheap-probe first · kill before confirm · surprise-symmetric** — the cheapest experiment whose every
outcome teaches, and the kill experiment before the confirm experiment. A large run before the cheap
falsifier is compute-lock; an external/public/irreversible commitment routes to the human.

## Engine division

**The external brain generates · the local agent operates · an independent hook checks · the human sets
taste.** The generative acts — `/prospect` mining, `/forge` design, `/autopsy`'s next-candidate — default
to the external brain (a different model with independent context reaches the reframe a local checklist
misses; 视角转换). Skipping it needs a stated reason, because left "optional" it is never used. The
boundary: the external brain is for the generative act, never for tactical iteration on an
already-designed thing. Bind the concrete engines (which model, which review hook, which bank file) in
the deploying project, not here.

## Handoff (an external deliverable only)

Before anything leaves for another person: target user named · primary claim explicit and narrower than
the evidence · limits stated · a hostile reader cannot over-infer · `/adversary` cleared any claim it
carries. External release is a human promotion.

## THE ANTI-ACCRETION RULE (what makes this a 1.0 and not a v0.10)

The parts budget is **fixed: 6 commands · 5 references · 1 invariant.** When something breaks, try in
order — and stop at the first that works:

1. **Was it a bug, or did the agent simply not follow an existing simple rule?** (Most "framework
   failures" are this.)
2. **Can an existing piece absorb it** — a line in a command that already fires at that moment?
3. **Can we DELETE something** — is the failure caused by surface, not absence?
4. **Adding is the last resort, and requires deleting something else** (one-in-one-out; the budget
   never grows).

The system re-bloated once before: v0.5 deleted the v0.4 gate stack, then v0.6–v0.9 re-added an
axis/command per complaint. Process work is never the deliverable; if recent artifacts are mostly about
the workflow, the workflow has become the product.

## Arbor MCP (the substrate)

The Arbor idea-tree is the canonical store — no side-channel files that can drift. Cards →
`tree_add_node`; contracts → `tree_set_meta`; runs → **`eval_run`** (the score is written from the actual
command output, the structural antidote to write-from-memory drift); autopsies → `tree_update_node` /
`tree_prune`; merges → `git_merge_branch` (a no-regression gate). Tree first, then narrative.

## Install

```
/plugin marketplace add CrepuscularIRIS/research-os
/plugin install research-os@research-os
```

## Provenance

v0.4 was a 10-gate filter stack; it produced well-audited work on questions that didn't matter. v0.5
inverted it around a generator and the one invariant. v0.6–v0.9 accreted (Layer-2 wrap, frames axis,
operators axis, /rigor). v1.0 converges: the axes and the invariant stay; the ceremony folds into the six
commands; the anti-accretion rule keeps it converged. 大道至简.

MIT — see [LICENSE](LICENSE).
