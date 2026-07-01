# Research Operating System — Taste Gate + Anti-Goodhart Layer (2026-06-29, v1.0)

> Synthesis of `plan/archive/deep-research-report (2).md` + the user's Goodhart critique, sitting ABOVE the
> experiment-rigor gates in `plan/methodology-harvest.md` (Layer 1). v1.0 reconciles three independent
> Codex GPT-5.5-xhigh reviews (`plan/archive/ros-review/codex-{A,B,C}-*.md`): A = command-ize SELECT, B = adversarial
> un-gameable-core, C = wiring + a live kill-review of our own paper.

---

## 0. Diagnosis
Not "too few auto-research agents." The default failure is an **objective-function leak**: the loop slides
from *"discover a fact that changes an external decision"* → *"maximize a paper-story's acceptability under
AI-review standards."* **Goodhart, not fraud** — no fabricated data; it optimizes the *provable proxy*
(novelty self-consistency, caveat completeness, clean-negative framing). Symptoms: topic convergence ·
experiment reward-hacking · papers that look complete but carry no insight. Two constraints: taste can't be
auto-scored (LLMs do recall, not taste); over-specifying the workflow is itself harmful (Anthropic AAR).

## 1. Governing principle (the one structural rule — Codex-B)
> **A success-defining gate must NEVER be runnable by the proposing agent.** Split roles: **proposer ·
> executor · adversary · decision-owner.** The agent may *prepare, falsify, verify, record*. It may NOT
> choose the success metric after seeing results, score its own taste, certify its own baseline fairness,
> decide a negative is non-fatal, or promote a result to paper-mode. Every gate whose output changes
> *continue/stop · claim/downgrade · paper/internal* must terminate **outside** the proposer (a human
> decision-owner or an external fact).

## 2. Two-layer OS
- **L1 — experiment rigor** (*is this result real?*): `methodology-harvest.md`. Agent-runnable, checkable.
- **L2 — taste + anti-Goodhart** (*is this the right problem? is success honest? is the claim scoped?*):
  this doc. **Mostly human-gated / external-fact-bound.**

## 3. ★ FINAL command-ization decision (reconciled A+B+C)
Key reconciliation: a thing can be a **command** (agent-runnable prep/falsification) OR a **gate** (binds
to human/external) OR **folded** OR **cut**. Commands prepare evidence; gates decide. (A answered "commands,"
B answered "what binds," C answered "where it fires" — no real conflict.)

### BUILD — 6 agent-runnable commands (prep/falsification; each must bind to an EXTERNAL artifact per B)
| Command | Trigger | Engine | Binds via (B's sharpening) |
|---|---|---|---|
| `/context-bundle` | before any nontrivial LLM dispatch; fail-closed | Opus | recent-negatives + forbidden-assumptions + must-read + hashes |
| `/exp-verify` | after every run, before any number is recorded | Codex | an **independent provenance harness** (logs/config/hashes/cache-state captured outside the proposer) — else it only proves "a program ran" |
| `/reward-hack-audit` | before promote/bank/merge/write-up | Codex | only where checks touch **external artifacts**: sealed holdout, per-example outputs, code hashes, fresh reruns, pre-declared thresholds |
| `/baseline-champion` | any "beats X"/frontier/architecture claim | Codex(+Pro) | an **independently tasked + budgeted adversary with veto**; proposer may NOT choose the baseline family, budget, stopping rule, or sign-off wording |
| `/bank-negative` | any kill/inconclusive/abandoned hypothesis | Codex | NegativeCase memory (absorbs `negative-grade` as a FIELD; grade only indexes memory — promotion-affecting grades need independent adjudication) |
| `/claim-evidence-matrix` | before paper-mode / external claim / upgrade | Codex | every claim → evidence TYPE or DOWNGRADE to hypothesis |

### GATE — the un-gameable core (NOT commands; human/external; B's 5)
1. **Independent taste gate — ASYMMETRIC authority (v1.2, the stop-gate fix).** Codex-B's invariant is
   **ISOLATION, not species** (never the *proposer*, not "must be *human*"), BUT isolation is only real when
   the proposer cannot manufacture the verdict — and in autonomous goal mode the proposer *dispatches*
   `/taste-critic`, *curates the context* it sees, and *can re-run it*. That makes a proposer-routed critic
   gameable **toward a false PASS, never a false KILL** (the "kill-reviewers GAMEABLE" failure: sanitized
   context + narrowed claim + re-run until clean). So authority splits by direction:
   - **KILL / DOWNGRADE = autonomous (AI does this, no human).** The independent **`/taste-critic`** (He-bar,
     kill-only, on Codex/Pro in a FRESH context) may BLOCK/downgrade the proposer's own academic-toy /
     standard-redefinition-hack with no human in the loop. Killing one's own work cannot be gamed toward
     over-promotion — this is the **"minimize human" win** (taste-FILTERING is genuinely AI-doable here).
   - **PASS / promotion = human or genuinely external (NOT self-grantable).** A `REAL-CONTRIBUTION` verdict
     from a proposer-dispatched critic is **advisory evidence that UNBLOCKS** promotion; it does NOT, by
     itself, promote a result to "contribution"/paper/"architecture advantage." That grant terminates in a
     **human (or an external decider the proposer does not control)** — rare, because only survivors of the
     autonomous kill-filter reach it.
   The proposer may only *prepare* advisory inputs (Taste Card + Olah's imagined-paper ritual *"if someone I
   respect, NOT me, published this, would I want to read it?"*), tagged `TASTE-UNVERIFIED`; a proposer scoring
   its own taste is the forbidden "taste cosplay" (§1). `ENGINEERING` ≠ `REAL-CONTRIBUTION`; **a new metric as
   the contribution is GUILTY until it corrects a misleading existing eval.** The HUMAN is touched on the
   **promotion PASS**, a critic↔proposer deadlock, or a flagship go/no-go — **not** per cycle. External
   backing: the community's agent-native rigor-reviewer **structurally omits** novelty/significance;
   openreviewer "complements, not replaces" human review — i.e. taste-as-an-independent-judge is the field norm.
2. **Named external-decision owner** — a real decision-maker precommits *"if evidence E under protocol P, I
   change decision D."* Generic "could inform practitioners" prose does NOT count.
3. **Content-addressed preregistration + sealed held-out** — timestamp binds chronology; sealed data binds
   adaptivity (agent can't see holdout or alter metric/stop/downgrade rules post-hoc).
4. **Independent baseline champion w/ veto** — (dispatched by the command above, but authority is external).
5. **Independent provenance/execution harness** — binds the *fact a run occurred* with given code/config/data.

### FOLD (into existing skills/manual — not new commands)
- `/external-decision-gate` → a **required field** in `/ideate` candidate cards + promotion briefs.
- `/problem-structure-extract` (He-style: Problem→Assumption→Minimal-mechanism→Killer-exp→Failure-boundary→
  Missing-evidence→Reusable-principle) + the **Taste Card** → `/ideate` Stage-1/output.
- `/preregister`, `/stage-protocol` (baseline→tune-frozen→creative→ablation) → **operating-manual rules**
  (stage-protocol is an *overrideable default*, never rigid — AAR lesson).

### CUT as standing commands (retain only as noted)
- `/kill-reviewers` — CUT as a per-cycle authority gate (A: high ceremony; B: gameable without a human veto).
  **Retain as an on-demand AUDIT instrument** (exactly how Codex-C just verdicted our paper — that worked).
- `/pivot-ledger` — fold into RUNLOG/tree discipline, but **generated from immutable logs/branch metadata,
  not retrospective self-report** (B). · `/negative-grade` — field inside `/bank-negative`.
- `/taste-gate` as an *auto-scored* command — the single most dangerous element (B's worst false friend): a
  swarm-filled Taste Card + self-assigned /50 is "taste cosplay." The Card lives in `/ideate`; the PASS is human.

## 4. Goal-mode wiring (PROPOSED — Codex-C; pending user go)
Two edits, both minimal (the goal prompt carries only the hard boundary; routing detail lives in the manual):

- **`goal-directive.md`** — replace the RULES line with (compact):
  `RULES: prereg H/falsifier/accept/neg-ctrl+metric/split; gen/verifier metrics; B_test sealed. ROS: SELECT
  taste-card→human; compare→baseline-champion; DECIDE→reward-hack-audit; paper→human gate. AUTONOMY: run the
  loop autonomously; NEVER self-set success/scope/paper-worthiness.`
- **`operating-manual.md` §5.1** — add the routing table (SELECT taste-card · external-decision stub ·
  pre-experiment preregister · cross-compare baseline-champion · DECIDE reward-hack-audit + negative-grade ·
  pivot ledger from logs · paper-mode claim-evidence + human gate) + the explicit **autonomy boundary**:
  agent may observe/ideate/tactical-variant/preregister/dispatch/tune/eval-under-frozen-contract/bank-evidence;
  agent may NOT pick a new paper-worthy direction, change metrics post-hoc, broaden scope, declare publishable,
  or say "architecture advantage." "Don't ask the user to choose" = tactical choices only; it does NOT override
  the human taste+decision gate.

## 5. ★ Live demo result — verdict on our own wall-clock paper (Codex-C)
Running the 4 kill-only reviewers on `plan/paper-draft.md` (the framework, applied to ourselves):
- **True status: workshop-MEASUREMENT** (strong internal positive + a scoped structural-negative companion).
  **NOT top-venue. NOT a systems artifact.** Most defensible as "the correct utility for verifier-rich
  branching, on a specific shipped pair + serving stack."
- **Before any "architecture advantage" language is allowed (3 hard conditions):**
  1. **Baseline champion** signs off on a strongest-realistic AR (vLLM/SGLang or documented impossibility;
     tuned batching/KV/continuous-batching/parallel sampling; 2nd HW if the claim is wall-clock-general).
  2. **Scope** expands (≥ AIME + code/Olympiad verifier tasks, ideally a 2nd matched pair) **or** a
     mirrored/controlled ablation separates architecture from model-family + serving.
  3. **Claim-evidence matrix** splits *deployment-win · serving-artifact · forward-pass-depth · architecture*
     — only the last may use architecture language, and only after profiler/FLOP/latency survives the champion.
- This **independently confirms** the handoff-memory's existing "workshop now; generality phase for top-venue"
  call — and demonstrates the OS catches our own Goodhart risk on real history.

## 6. Build order (pending greenlight)
1. Wire the 2 doc edits (§4) — establishes the autonomy boundary + routing. *(reversible; changes loop policy)*
2. Build the 6 commands (§3 BUILD), each bound to its external artifact per B. Highest-value first:
   `/baseline-champion` (the strongest anti-Goodhart) · `/reward-hack-audit` · `/exp-verify` · `/bank-negative`
   · `/context-bundle` · `/claim-evidence-matrix`.
3. Fold the Taste Card + external-decision field + problem-structure extract into `/ideate`; preregister +
   stage-protocol into the manual.
4. Apply §5's 3 conditions to the wall-clock paper before any architecture-advantage framing.
> Per-review detail: `plan/archive/ros-review/codex-A-select.md` (dispositions), `codex-B-adversarial.md` (attacks +
> un-gameable core), `codex-C-wiring-and-demo.md` (exact edits + the full per-persona paper kill-list).

---

## 7. v1.1 STRENGTHENING — grounded in `research-methodology-os`
> The user's `research-methodology-os` (4-layer Taste/Rigor/Review/Workflow + a 00–07 module tree + a 3-gate
> plan) is the SAME OS, independently built — strong convergent validation. The decisive upgrade: ground each
> gate in a **real community standard** so it binds to an external fact, not self-invented prose (Codex-B).
> Detail: `plan/archive/extraction/methodology-os-{rigor,taste,skills}.md`. **Paper layer (06) deferred per user.**

### 7.1 Gate grounding map (cite the venue norm, not ourselves)
| Gate/command | Now grounded in (external community standard) |
|---|---|
| `/reward-hack-audit` | stat-test checklist: **≥3 seeds, mean±std, not best run**; Lones ML-pitfalls (leakage/comparability); universal-checklist "negative/null results reported" |
| `/preregister` | stat-test §1: **write H0/H1 + named estimand before running; one-tailed must be pre-registered** |
| `/baseline-champion` | stat-test §10: baselines use **same feature set, preprocessing, AND tuning budget** (the adversary's checklist) |
| `/exp-verify` | ACM artifact-evaluation checklist (provenance/reproducibility); hermes artifact-exists check |
| `/bank-negative` | universal-checklist "negative/null/mixed reported, not hidden"; `ara-research-manager` dead-end node schema |
| human **taste gate** | **Olah imagined-paper ritual** (advisory when agent-run, §4 #1); Schulman goal-vs-idea-driven + "So-what/Why-so/Well-done" test; Mila "draft-as-paper-first" + when-to-quit |
| **claim-evidence matrix** | REFORMS + ACL author checklist + `ara-rigor-reviewer` D1/D3 |

### 7.2 ★ Adopt-don't-rebuild (Skills extractor)
`AI-research-SKILLs/22.../rigor-reviewer/SKILL.md` (`ara-rigor-reviewer`, 323 lines) is the closest existing
skill to our whole L1: its **D1+D3 = `/claim-evidence-matrix`, D2 = preregistered falsifier, D5 = `/bank-negative`,
D6 = `/reward-hack-audit` baseline check** — adopt/adapt directly. **Only 2 of the 6 commands are genuinely new
and must be built from scratch: `/context-bundle` and `/exp-verify`** (no-mock + anti-no-op log_assertion).
Use the `ara-rigor-reviewer` **SKILL.md template** (YAML frontmatter · "Do NOT use when" block · numbered Steps
· 5-point scoring anchors with examples · typed output artifact · Critical Rules · `references/`). Adopt
`ara-research-manager`'s provenance format (user-vs-AI tags, `exploration_tree.yaml` dead-end schema) as the
canonical `/bank-negative` + Arbor-tree file format. Fold the two ideation skills' frameworks (tension-hunting,
failure-analysis, Boden constraint-manipulation, adjacent-possible) into `/ideate` Stage-1.

### 7.3 Two design fixes from the grounding
- **Taste Card v2** — add the two missing fields the canonical literature requires: **"Why now?"** (Schulman
  field-ripeness) and **"Who cares?"** (the named external-decision owner, folded INTO the card so it's
  self-contained). Keep the agent-run output advisory (`TASTE-UNVERIFIED`, §4 #1).
- **Paired statistical inference** — biggest gap: model-vs-model comparison must use **paired** tests
  (5×2CV Dietterich / McNemar / DeLong); unpaired t-tests on shared-CV folds are community-banned. Add to
  `/reward-hack-audit` + `/baseline-champion`. (Our DiffusionGemma-vs-AR paired bootstrap already aligns; this
  sharpens it.)

### 7.4 The un-gameable core, externally re-confirmed
The community's OWN agent tooling proves the invariant is a norm, not our quirk: `ara-rigor-reviewer`
**structurally omits** novelty/significance from its 6 dimensions; `openreviewer` is "designed to complement,
not replace, human peer review"; hermes treats novelty/significance as human-adjudicated. → taste/novelty =
human-only is the standard, not a constraint we invented.

### 7.5 Unified executable module tree (research-only; user's 00–07 ↔ our gates)
`00_taste` (Olah ritual + Schulman/Mila tests → human gate) · `01_field-map` + `02_topic-select` +
`03_novelty-audit` → fold into `/ideate` · `04_experiment-design` → `/preregister` + `/exp-verify` ·
`05_anti-reward-hacking` → `/reward-hack-audit` + `/baseline-champion` + `/bank-negative` (each grounded per
7.1) · `07_agent-runtime` → the goal-mode wiring (§4) + `/context-bundle`. **`06_paper-writing` = DEFERRED.**

### 7.6 Build plan (the user's "先做 3 个 gate，不急着自动化")
1. **Gates-as-checklists first** (not automation): wire the 3 binding gates — **Taste** (independent
   `/taste-critic`, He-bar, kill-only; **ASYMMETRIC authority §4 #1** — KILL autonomous, PASS human/external;
   Card v2 + Olah ritual as advisory prep), **Experiment** (`/preregister` + `/exp-verify` + the
   ≥3-seed/paired-stats rigor checklist), **Reviewer** (`/claim-evidence-matrix` + `/baseline-champion`) —
   each as a grounded checklist that fires BEFORE the work, not as post-hoc rescue. ✅ `/taste-critic`
   (skill+command), `/baseline-champion`, and the §4 goal/manual wiring (v1.2 asymmetry) are BUILT.
2. **Adopt** `ara-rigor-reviewer` (D1–D6) + its SKILL.md template + `ara-research-manager` provenance format.
   ✅ DONE — `/reward-hack-audit` (D1+D6), `/claim-evidence-matrix` (D1+D3), `/bank-negative` (D5 + A–E
   taxonomy + structural-negative gate) all built (skill+command), on the ara SKILL.md template.
3. **Build from scratch only** `/context-bundle` + `/exp-verify`. ✅ DONE — both built (skill+command):
   `/context-bundle` (fail-closed must-read/forbidden-assumptions/sealed-split/hashes/contract);
   `/exp-verify` (3-stage structural→execution→plausibility + anti-no-op log_assertion).
   **→ ALL 6 BUILD commands + `/taste-critic` are now built; the §5.1 gate references are live, not dangling.**
4. **ENFORCEABLE-CONTRACT pattern (meta-lesson, learned the hard way over 7 stop-hooks).** A gate invariant
   written only as SKILL.md prose / a `//constraint` comment enforces NOTHING — an agent can emit a
   non-conforming artifact and cite the prose. Convert a *machine-checkable* invariant into a runnable
   contract: a **JSON Schema** + a **fail-closed validator** with ALL of:
   (a) a dependency-free pure-Python path that enforces the FULL contract — must NOT fail open when
   `jsonschema` is absent (#4); (b) the dep-free path must not be MORE LENIENT than the schema on any field,
   incl. nested `required` keys — `.get()` defaulting conflated "missing" with "null" (#5); (c) it must REJECT
   cleanly, never CRASH, on ANY input — `x in <set>` raises on unhashable list/dict enum values, so enum
   checks use `isinstance(str) and x in SET` + a top-level `except Exception` backstop (#6); and the READ must
   fail closed via `read_bytes()` + `json.loads` + a broad `except`, because `read_text()` raises
   `UnicodeDecodeError` (a `ValueError`, NOT `OSError`/`JSONDecodeError`) on non-UTF-8/undecodable bytes (#7).
   Ship it with a **pytest suite** including a **schema-PARITY guard** (mutate every required field / enum /
   array-bound / unhashable value and assert dep-free ≡ schema on accept/reject), `jsonschema`-unavailable
   tests, crash-safety tests, and malformed/non-UTF-8/binary read tests; invoke it as a MANDATORY command
   step (exit≠0 ⇒ not banked). **Worked example = `/bank-negative`**: `schema/negative_case.schema.json` +
   `validate_negative_case.py` + `tests/` (26 cases) make a proposer-self-certified `structural-negative`
   mechanically impossible, with or without `jsonschema`, and never crash on any input. Apply this template —
   *parity guard + crash-safety + fail-closed read* — to any gate whose invariant must bind.
5. Apply the §4 wiring (autonomy boundary) + §5's 3 conditions to the wall-clock paper.
> Defer all paper-writing tooling (06 + the Review-Layer writing repos) per the user's current scope.
