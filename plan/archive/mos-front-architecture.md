# MOS-Front — the Modeling-Object-Shift FRONT-HALF (generator) of the Research-OS

> The **front-half** (idea GENERATOR) that complements the existing **back-half** (the 7 anti-Goodhart
> FILTER gates in `research-operating-system.md`). Source: `enrich.md` (the aesthetic) → GPT-5.5-Pro deep
> design → Opus integration. The back-half answers *"is this result real/honest?"*; MOS-Front answers
> *"is this even the right KIND of question, posed at the right modeling object?"* — which happens BEFORE
> the back-half fires. Built 2026-06-30. Parallel reference: `plan/research-operating-system.md`.

---

## 0. The core principle (read this first)
**Generation can be bold; eligibility must be conservative. The card is not evidence — it only packages a
*killable* hypothesis.** The whole front-half exists to convert "an elegant reparameterization story" into a
**pre-registered, machine-checkable, falsifiable claim** before any compute is spent. It reuses the back-half's
governing invariant verbatim: the proposer (Opus) GENERATES; an independent substrate (Codex) AUDITS/KILLS;
the consequential grant (contribution / new programme) is human/external. The generator never certifies its
own object-shift.

## 1. The generative engine (Opus's §18 correction, the sharpest insight)
The missing unit is **NOT** the "Modeling-Object Card." It is **O0-equivalence failure mining**. A card
without contrast-mining is just narrative. The real generative move, the front-half analog of
falsification-first:
> **Find the cases the OLD object treats as EQUIVALENT but reality SEPARATES → name the structure `S` that
> separates them → build the new object around `S` → preregister the failure-split BEFORE training.**

Governing chain (the front-half invariant):
> No object-shift claim without an **omitted-structure contrast**. No omitted-structure contrast without
> **pre-existing observed failures**. No eligibility without a **differential prediction**. No contribution
> without the **existing back-half**.

## 2. What counts as a REAL object-shift (the 4 conditions)
A modeling-object is a tuple `{state_space, observation_map, equivalence_relation, native_operators,
evidence_proxy}`. A claimed shift O0→O1 is real only if:
- **C1 non-collapse** — O1 exposes a structure `S` that O0 collapses / ignores / cannot naturally operate on.
- **C2 observed-failure anchor** — `S` explains ≥1 *pre-existing observed* failure (not a newly-invented toy).
- **C3 differential prediction** — *before training*, O1 predicts a measurable failure split that O0 would
  not, under O0-matched controls.
- **C4 killability** — a preregistered experiment can kill the *object-shift claim* (not merely an implementation).

*"Calling classification an energy field" is NOT a shift. "Showing closed-set p(y|x) collapses the semantic
support boundary AND baseline failures show a preregistered split on a support-distance-matched contrast"
might be.*

## 3. Two lanes + one gate (the anti-over-proceduralization answer)
A lightweight `front_mode` triage at IDEATE — most ideas are NOT object-shifts and must not pay the ceremony:
| Mode | For | Requirement |
|---|---|---|
| **SKIP_TACTICAL** | tactical variant under an existing programme (ablation, impl-fix, baseline, infra, replication, data-clean) | minimal, but MUST declare `claimed_object_shift: false` + carry a local kill-experiment + **may NOT use object-shift language** ("new object", "reparameterizes", "new paradigm") |
| **MOC_LITE** | object-shift *flavor* but not a new programme | the **6-line card** (observed-puzzle · old-object · omitted-structure · new-object · differential-prediction · kill-experiment). **The 80% value path.** Runs a **lightweight `/object-shift-audit`**. |
| **MOC_FULL** | genuine object-shift: new direction / programme root / new eval-metric language / paper main-claim / needs Pro deep design | full MOC + DPC; **must pass the independent `/object-shift-audit`** during SELECT (before DISPATCH) |

## 4. The keystone — the Differential Prediction Contract (DPC)
The machine-checkable answer to *"real object-shift vs cosmetic relabel?"*. A DPC declares, BEFORE training,
a prediction checkable on **existing baseline logs**: within O0-matched buckets, O0 says failure does NOT vary
with `S`; O1 says it does (e.g. failure rate rises monotonically with `S`-quartile), with a **shuffled-S
negative control** and a **generic-difficulty control** and a **rival old-object baseline**. the DPC check
(the fail-closed validator) emits `DIFFERENTIAL_PATTERN_FOUND / NO_DIFFERENTIAL_PATTERN /
INCONCLUSIVE_INSUFFICIENT_POWER / CONTROL_FAILURE / NOT_RUN` (the last = LITE / not-yet-executed; it can
**never** support an `ELIGIBLE_FOR_BACK_HALF` verdict — only `DIFFERENTIAL_PATTERN_FOUND` does). This is the
front-half's enforceable contract — same discipline as the back-half's `bank-negative` validator (JSON schema
+ fail-closed + pytest).
**The #1 residual risk (Opus flag): "S predicts failure" is necessary but NOT sufficient for "S is the right
object" — many confounds predict failure.** The rival-baseline + generic-difficulty + shuffled-S controls are
therefore MANDATORY, not optional. Front-half analog of "a new metric is guilty until it corrects a misleading eval."

## 5. The command surface (3 commands; methodologies embedded, like /ideate)
The enrich methodologies are *operationalized inside* these commands, not lost:
- **`/mos-front`** (Opus, propose-only) — the generative front pass: `front-trigger` (SKIP/LITE/FULL) →
  Phenomenon-Bundle → Default-Object-Map → **Omitted-Structure Miner** (the 5 angle-miners: equivalence-split ·
  residual-field · invariant-break · support-boundary · trajectory) → **School-Router** (the ~14 enrich
  "schools" as primary + optional-secondary + **mandatory rival**) → MOC (LITE/FULL) + DPC draft. Embeds the
  Modeling-Object-Shift trajectory, the 14 schools, the 10-question generator, the 5-layer ladder.
  References: `~/.claude/skills/mos-front/references/schools.md`.
- **`/object-shift-audit`** (Codex, independent, **kill-only**) — the binding honesty gate: tests T1–T6
  (distinct-object · observable-S · pre-training differential-prediction · rival-baseline-attack ·
  negative-control · kill-action-defined) + runs the DPC validator. Verdict ∈ `KILL_COSMETIC_RESHIFT /
  DOWNGRADE_TO_TACTICAL_VARIANT / ELIGIBLE_FOR_BACK_HALF / NEEDS_PRO_DEEP_DESIGN / NEEDS_HUMAN_TASTE_REVIEW`.
  **`ELIGIBLE` is NOT a contribution pass** — only "not obviously cosmetic; may enter the kill-filter."
  Fail-closed validator + JSON schema + pytest (bank-negative discipline).
- **`/programme-audit`** (Codex, tree-level) — the Lakatos progressive-vs-degenerating **budget** signal on a
  `programme` node: a numeric `programme_progress_score` (ex-ante-prediction-passed +2 … hard-core-edit-after-
  failure −4) → `PROGRESSIVE / STABLE_BUT_UNPROVEN / DEGENERATING_WATCH / DEGENERATED_RETIRE_OR_FORK`. It does
  not decide truth; it decides whether a programme deserves more research budget.

## 6. Plug-in to the loop (where each fires)
```
OBSERVE(Opus) → + Phenomenon Bundle (pre-existing, sealed failures)
IDEATE(Opus)  → /mos-front  (front-trigger → mining → school-router → MOC + DPC draft)
SELECT(Codex) → /object-shift-audit (cosmetic-reshift KILL + DPC-check + rival attack) → existing /taste-critic
DISPATCH(wt)  → /context-bundle  (now REQUIRES MOC + DPC + preregistered kill for MOC_FULL; fail-closed)
VERIFY(Codex) → /exp-verify → /reward-hack-audit → /baseline-champion (gets the rival-attack packet)
DECIDE(Codex) → /bank-negative (new types: cosmetic_reshift vs object_shift_valid_but_method_failed) → /claim-evidence-matrix
BACKPROP      → Arbor: tree_update_node/tree_prune (+programme node via tree_add_node) → /programme-audit → generate_report
```
Promotion to "contribution" / a new programme still HARD-BLOCKS to human/external (unchanged asymmetry).
**Persistence (operating-manual §5.3):** ALL structure is written THROUGH Arbor MCP (the substrate is more
reliable than md/json). The ONLY files that persist are the sealed, schema-VALIDATED contracts Arbor's
fixed-field node can't hold — the `MOC + DPC`, the `object_shift_audit` verdict, the `programme` ledgers, the
`negative_case` — each referenced from its node's `code_ref`. There is no parallel structure-JSON pile.

## 7. Engine assignment (isolation preserved)
Opus GENERATES (Phenomenon-Bundle, Default-Object-Map, Miner, Router-draft, MOC, DPC-draft) — **propose only,
cannot certify**. Codex AUDITS (`/object-shift-audit`, `/programme-audit`) — kill/downgrade/eligible, never a
contribution grant. Pro refines deep design — does not self-grant contribution. **Human/external** grants the
consequential contribution / programme promotion.

## 8. Coupling to the 7 back-half gates (extensions, not new gates)
- **/taste-critic** — gains a kill-only `COSMETIC_RESHIFT` awareness test (guilty until O0 named + S measurable
  + pre-existing failure + differential prediction registered + rival attacked); does NOT certify contribution.
- **/context-bundle** — MOC_FULL dispatch fail-closed unless the bundle has exactly these top-level keys:
  {`phenomenon_bundle`, `default_object_map`, `moc`, `dpc`, `object_shift_audit`, `baseline_report`}. (The
  preregistered kill lives in `dpc.kill_condition`+`dpc.preregister_hash`; the `claim_language_restrictions`
  live inside `object_shift_audit` — neither is a separate top-level artifact.)
- **/exp-verify** — DPC becomes a first-class experiment spec: dpc-hash-matches-preregister, S-extractor /
  O0-matcher / primary-statistic not changed post-hoc, negative-controls run.
- **/reward-hack-audit** — adds sealed-failure-bundle, sealed-S-extractor, shuffled-S control, generic-difficulty
  control, baseline-champion old-object alternative, holdout-not-reused-for-router.
- **/baseline-champion** — receives the rival-school attack packet; if old-object machinery explains the same
  differential pattern, the object-shift is DOWNGRADED.
- **/bank-negative** — new negative types incl. the crucial **`object_shift_valid_but_method_failed`** (keep the
  programme alive, bank only the implementation negative) vs **`cosmetic_reshift`** (kill the object-shift claim).
- **/claim-evidence-matrix** — `modeling_object_shift` is a typed claim; required-evidence = {object_shift_audit:
  ELIGIBLE, dpc_check: DIFFERENTIAL_PATTERN_FOUND, exp_verify, baseline_champion: not_explained_by_old_object,
  reward_hack_audit, human/external for contribution}; else downgrade to "we hypothesize S as a diagnostic lens."

## 9. The Lakatos `programme` (an Arbor node + a sealed ledger)
A programme = a durable object-shift with `hard_core` + `positive_heuristic` (next ex-ante predictions, each a
linked DPC) + `negative_heuristic` (forbidden patches) + `protective_belt` + `anomaly_ledger` +
`corroboration_ledger` + `degeneration_metrics`. **It is an Arbor node** (`tree_add_node` with the hypothesis =
the hard_core; status/insight/score via `tree_update_node`), and its rich `programme.v1` ledger is the sealed,
validated artifact referenced by `node.code_ref` (the part Arbor's fixed fields can't hold). The argument
relations a tree can't express — `corroborates / refutes` (prediction↔experiment), `rules_out`, `supersedes` —
live as a thin typed-edge layer in research-os keyed by the Arbor node IDs (a typed DAG over the tree backbone,
acyclic; NOT a fork of Arbor). Promote to a programme ONLY after the first `DIFFERENTIAL_PATTERN_FOUND` + human
budget approval (avoids programme bloat).

## 10. Front-half failure modes + guards (the front-half's own anti-Goodhart)
| Failure | How gamed | Guard |
|---|---|---|
| Buzzword relabel | "we model residual/support/energy", nothing changes | `/object-shift-audit` T1 + T3 (DPC) |
| Cherry-picked puzzle | inventing failures after the idea | Phenomenon-Bundle must be pre-existing, sealed |
| Post-hoc prediction | DPC written after seeing results | preregister hash; S-extractor/stat/matcher frozen |
| School shopping | try aesthetics until one sounds deep | router = primary + optional-secondary + **mandatory rival** |
| Confounder as structure | S is just difficulty/length/domain | O0-matched controls + generic-difficulty negative control |
| Programme degeneration | patch each failure by editing the hard-core | `/programme-audit` (hard-core-edit-after-failure → watch/retire) |
| Over-proceduralization | more time filling cards than thinking | SKIP_TACTICAL + MOC_LITE default; MOC_FULL only for consequential shifts |
| Proposer self-certification | Opus makes it sound deep + approves | Opus generates only; Codex audits; human for contribution |

## 11. ★ Orchestration cheat-sheet — WHEN /goal calls what
- **New direction / thesis / "let's reparameterize X"** → `/mos-front` (MOC_FULL) → `/object-shift-audit`
  (must be ELIGIBLE, not KILL) → preregister → DISPATCH. Object-shift CLAIM in a write-up → human/external.
- **Object-shift flavor under an existing programme** → `/mos-front` (MOC_LITE, 6-line) → `/object-shift-audit`
  (lightweight) → DISPATCH.
- **Tactical variant / ablation / impl-fix / replication** → `/mos-front` (SKIP_TACTICAL waiver) → straight to
  the back-half. No object-shift language allowed.
- **Every cycle on an active programme** → `/programme-audit` at BACKPROP (is it progressive or degenerating?).
- **Always**: a "beats X" claim → `/baseline-champion`; a positive result → `/reward-hack-audit`; a null →
  `/bank-negative`; pre-paper → `/claim-evidence-matrix`; promotion → human/external (§5.1 asymmetry).

## 12. Build order (cheap-first, Pro's recommendation — followed)
1. claim-language restriction (block object-shift language without a MOC_LITE). 2. MOC_LITE 6-line schema.
3. `/object-shift-audit`. 4. the DPC check validator (the real-vs-cosmetic, made executable). 5. `programme`
node only after the first `DIFFERENTIAL_PATTERN_FOUND`.
