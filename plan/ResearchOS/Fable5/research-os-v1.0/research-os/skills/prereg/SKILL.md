---
name: prereg
description: Freeze the evidence contract BEFORE any run whose numbers will be cited — hypothesis, mechanism, type, metric + sealed split, statistical unit + valid paired test, accept/kill thresholds, negative control, seeds, one-variable. 10–20 lines, timestamped via Arbor. Post-hoc edits void the run as evidence. Exploration stays free. Absorbs the old /rigor's FAST evidence contract.
version: 1.0.0
tags: [Research, Preregistration, Falsification, SealedEval, EvidenceContract]
dependencies: []
---

# Prereg — freeze the contract before the run

The proposer's judgment *after seeing results* is the least trustworthy object in the loop —
self-persuasion is the failure this defends against. The contract is decided while the answer is unknown.

## The exploration / evidence line (read first — it prevents ceremony)
- **Exploration is free.** Poking, plotting, debugging — no contract, ever. Exploration numbers are
  hypotheses.
- **Evidence is contracted.** The moment a number might be cited — a claim, a comparison, a report — the
  run needs a contract FIRST, and a fresh run under it. An exploration number is never promoted
  retroactively; re-run it under the frozen contract (cheap — you already know how).
- One contract per **claim-bearing run**, not per script invocation. A sweep feeding one claim = one
  contract. Cheap size-first probes and kill experiments skip everything below except KILL-if.

## The contract (10–20 lines — a card, not a document)
```
HYPOTHESIS:  <expected, one sentence>
MECHANISM:   <the mechanism-sentence from the /forge card>
TYPE:        <research type — sets /adversary's checks>
METRIC:      <primary (+secondary), EXACTLY as it will be reported>
SPLIT:       <the sealed eval split — eval scripts, test sets, baselines untouched from now on>
UNIT+TEST:   <what one data point is, and the VALID paired test — see table below.
              no unit ⇒ no valid test; never an unpaired t-test on shared units>
ACCEPT if:   <threshold decided NOW — Δ must clear the RELEVANT variance source, not merely > 0>
KILL if:     <the /forge KILL experiment made concrete>
NEG-CONTROL: <what must NOT move if the mechanism (not a confound) is doing the work>
SEEDS:       <sized to the effect and the noisiest variance source (training / eval-episode / env-reset /
              perturbation / checkpoint-selection — pre-declare the checkpoint rule); ≥3 for a claimed Δ;
              mean±std, never best-run>
ONE-VAR:     <the single thing that differs from baseline; more ⇒ split the experiment>
```

**For a CONFIRMATORY run** (a cheap probe already showed the effect is likely real) add the three cheap
fabrication-catchers + the envelope:
```
ABLATIONS:   necessity (remove the mechanism → effect must die) ·
             negative-control (a should-not-work setting must stay flat) ·
             cost (matched compute — is the gain the mechanism or just more FLOPs?)
BASELINES:   <the strongest honestly-tuned config, equal budget — the spec /adversary B will fight>
ALLOWED-CLAIM: <the exact claim this evidence will license, scoped to units tested;
                the overclaim it must NOT become ("one-axis gain ≠ general robustness")>
```
Fuller ablations (sufficiency, stress, per-suite breakdowns) are reserved for the one claim leaving for a
venue — five ablations on every candidate is the ceremony this line exists to avoid.

| Metric type | Valid paired test |
|---|---|
| binary success per example | McNemar / paired-binary; stratified bootstrap on the paired delta |
| continuous score | paired bootstrap · permutation · Wilcoxon signed-rank |
| multitask / RL aggregate | IQM + stratified-bootstrap CI (rliable-style) — never a single mean |
| two models on the same folds | 5×2CV / McNemar / DeLong — never pooled-unpaired |

### Optional block — differential prediction (novelty-type claims)
```
DIFF-PRED:   <a failure split in EXISTING logs the NEW object predicts and the old cannot — pre-training>
CONTROL:     <shuffled-S: the same split with the separating structure randomized must NOT predict>
```
Where the pattern doesn't apply (optimization-dynamics ideas), say so and state the alternative kill.

## Rules
- **Post-hoc edits void the run as evidence.** A changed contract = a new prereg + a fresh run — including
  "the threshold was clearly too strict" (that lesson goes in the NEXT contract).
- **The sealed layer is immutable mid-run.** A genuine eval bug ⇒ seal a new eval version + re-run
  everything that used the old one. One-tailed tests are declared here, not discovered later.
- Timestamped and stored via Arbor (`tree_set_meta` / `code_ref`) — no side file that can drift.
- Dispatch hygiene: the executor receives the contract + exactly the inputs it needs, not ambient context.
- A prereg over ~20 lines is documenting, not contracting.
