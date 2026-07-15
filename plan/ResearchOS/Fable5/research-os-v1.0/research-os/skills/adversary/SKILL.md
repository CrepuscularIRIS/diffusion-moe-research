---
name: adversary
description: The single claim-boundary gate — fires ONLY when a claim leaves the loop ("works" / "beats X" / "structural negative" / "contribution"). Four TYPE-scoped checks — Δ-reality · baseline fairness (make the OPPOSING baseline win) · claim–evidence map (no artifact ⇒ hypothesis; claim ≤ contracted envelope) · worth. DOWN verdicts self-administrable; CLAIM_STANDS = independent substrate only; contribution promotion = human only. Requires a prior /exp-verify VERIFIED.
version: 1.0.0
tags: [Research, Verification, AntiGoodhart, Baselines, Claims]
dependencies: []
---

# Adversary — one gate, at the one place a gate belongs

Most work never sees this gate; it fires at exactly one event: **a claim is about to leave the loop.** One
adversarial pass, checks scoped to the claim's TYPE (from the prereg). Precondition: the runs behind it
are `/exp-verify` VERIFIED.

## The one invariant (operational)
> **A verdict that helps the proposer if gamed must never be granted by the proposer.**
- The proposer self-administers **DOWN only**: `REFUTED`, `DOWNGRADED_TO_HYPOTHESIS`, `TOY`,
  `GOALPOST_MOVED`.
- **`CLAIM_STANDS` requires an independent substrate** — a fresh context the proposer did not curate
  (dispatched reviewer / automatic review hook / external model). A failed pass is answered
  point-by-point, never re-rolled.
- **Cold-start the reviewer; beware the agreement illusion.** The independent pass gets a cold packet —
  claim + artifacts + prereg, NOT the proposer's persuasive framing — and a stance-separated prompt (tell
  the reviewer to REFUTE). Two engines agreeing under the same framing is not independence.
- **Memory is not evidence.** A claim resting on recollection ("this is novel", "the literature says") is
  a hypothesis until a live search or an artifact backs it — the proposer may not upgrade its own memory.
- **Contribution / paper promotion is never an AI verdict.** `CLAIM_STANDS` is advisory; the pass
  terminates in the human. Silence ≠ CLAIM_STANDS.

## The four checks (apply the blocks matching the claim TYPE)

### A. Δ-reality (improvement · systems · novelty)
≥3 seeds, mean±std, error bars clear of the prereg threshold — never best-run. **Per-example regression**:
where did the gain come from, and does the flip pattern match the claimed MECHANISM? **Negative control**:
did the should-not-move quantity move? Moved ⇒ the mechanism story is wrong even if the metric is up.
**Sealed holdout**: the reported number is from the sealed split, metric unchanged — any drift ⇒ REFUTED
as evidence, re-contract and re-run.

### B. Baseline fairness (any comparison claim)
**Actively try to make the OPPOSING baseline win**: equal tuning budget, same data, the strongest
configuration the literature knows — not the paper-default straw version; the strong serving stack if
wall-clock matters. Paired statistics per the prereg UNIT+TEST. If the adversary CAN make the baseline
win, the claim dies here — report the winning config so the proposer can re-attack honestly.

### C. Claim–evidence map (all types)
Decompose the claim into sentences; each sentence → its artifact. **No artifact ⇒ that sentence
auto-downgrades to a hypothesis** — no "obviously follows". **The claim may not exceed the prereg's
ALLOWED-CLAIM envelope**: scope matches evidence ("on Qwen3-4B GSM8K" does not support an unqualified
"improves speculative decoding"); a non-significant trend is not an "improvement". **A new metric offered
as evidence is GUILTY until it demonstrably corrects a misleading existing eval.** A structural-negative
claim needs the three-part gate: pre-declared falsifier fired + live negative controls clean + sealed
confirmation — anything less stays `scoped-negative`.

### D. Worth check (taste's only pure-filter appearance)
**Academic toy?** dies on the first realistic perturbation. **Goalpost moved?** wins by redefining the
task/metric. **He-bar, TYPE-relative** (`taste.md` §4) — do not demand 可命名 of a Δ-claim.
**Evaluation-type claims: name the decision that changes** — a measurement that changes no decision is a
certificate, not a result.

## Verdicts
| Verdict | Who may grant |
|---|---|
| `REFUTED` · `DOWNGRADED_TO_HYPOTHESIS` · `TOY` · `GOALPOST_MOVED` | proposer or independent |
| `CLAIM_STANDS` | **independent substrate only** |
| promotion to contribution/paper | **human only** (CLAIM_STANDS is advisory input) |

Output: per-check PASS/FAIL with evidence, the verdict, and — on any DOWN — what would re-admit the claim
(a failed pass sharpens the next attempt; hand the finding to `/autopsy`).

## Write-through
Verdict + per-check evidence → Arbor `tree_update_node`. A DOWN-verdicted direction may stay
`in_progress` with the finding recorded — it just cannot leave the loop as a claim.
