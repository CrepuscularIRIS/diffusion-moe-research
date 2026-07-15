---
name: prospect
description: The problem-generator — hunt problems worth an experiment from five mines, OWN-LOG ANOMALIES FIRST, plus taste-operator retrieval as a prior. Output = 3–7 taste-ranked problem cards {Q, TYPE, WHY-NOW, STAKES, PROBE, SURPRISE} + a frame/operator ledger line. Run at goal start, after a "no surprises" flag, after a region-close, or on any fresh corpus.
version: 1.0.0
tags: [Research, Generator, ProblemFinding, Taste]
dependencies: []
---

# Prospect — hunt problems worth an experiment

Research quality is decided mostly at problem-selection time, before evidence exists (`taste.md` §1).
Filters preserve value; this is where value is created. **The generative mining defaults to the external
brain** — a different model reaches the reframe a local checklist misses (视角转换); skip only for a
thin/obvious corpus, with the reason written.

## The five mines (run every mine whose input exists; at least two)

1. **Own logs — the ANOMALY LEDGER, FIRST.** An unexplained pattern in YOUR artifacts is the only
   structurally off-distribution data you possess; literature mining interpolates the field's consensus.
   Consume every un-mined `[ANOMALY]` entry `/autopsy` has written. Also: unexplained seed variance,
   misbehaving baselines, disagreeing metrics, the subgroup where all methods degrade together.
   **Artifact-fidelity:** the hand-off carries raw numbers read from the artifact this session, never a
   remembered summary.
2. **Literature / survey (综述 = a problem MINE, not a reading assignment).** Extract, don't summarize:
   **contradictions** (two credible papers that can't both be true — someone's hidden variable is
   load-bearing) · **shared silent assumptions** (the field's single point of failure) · the
   **future-work graveyard** (promised ≥3 times, never delivered — find WHY) · **missing head-to-heads**
   · **stale numbers** that predate a capability shift.
3. **Capability deltas.** "X was designed under constraint C; C just disappeared — what does X look like
   without C?" This is where WHY-NOW answers come from.
4. **Benchmark critique.** Where does the metric disagree with the goal it proxies? Yields evaluation-type
   problems — valuable ONLY if a decision changes downstream.
5. **Cross-domain transplant.** Transplant the precondition-check, not the buzzword: state WHY the
   structure worked in domain A and show the same why holds in B.

**Operator retrieval (cross-cutting):** match the territory's failure signature to the taste-bank
(`../forge/references/taste-operators.md`); a fitting operator surfaces a candidate PROBLEM. A prior, not
a problem — it still needs STAKES + SURPRISE.

## The problem card (all six fields, no exceptions)
```
Q:        <the problem as a question, one sentence>
TYPE:     <one of the 9 — references/research-types.md>
WHY-NOW:  <the capability delta / new failure / fresh contradiction that makes it live TODAY>
STAKES:   <what changes if answered — a decision, method, or belief. "nothing" ⇒ discard>
PROBE:    <the cheapest surprise-symmetric experiment — both outcomes teach>
SURPRISE: <what result would genuinely surprise. no outcome surprising ⇒ discard>
```

## Rank and emit
Rank by **STAKES × plausibility-of-surprise ÷ PROBE-cost**. Output 3–7 cards + ONE recommended first
probe + the ledger line: `INCUMBENT FRAME = <X> · candidate off-frames = <a,b> · candidate operators =
<p,q>`. A hunting list, not a report — no literature summary, no coverage claims.

## Discard on sight
- **Gap-filling**: "nobody has done X" is not a reason — most empty territory is empty because it is
  worthless; demand a WHY-EMPTY. Occupancy is a cost signal, never a value signal — in both directions.
- Problems whose every outcome changes nothing; problems needing apparatus outside the goal's constraints.
- **Gate-shaped problems**: proposed because they're easy to verify, not because a decision hangs on them.

## Write-through
Cards → Arbor `tree_add_node`; rank + recommended probe → the parent node insight. The tree is the
canonical backlog — no side list.
