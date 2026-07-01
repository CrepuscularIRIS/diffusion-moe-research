# Methodology OS Skills Extraction — Comparison & Template (2026-06-29)

> Sources read: AI-research-SKILLs (23 categories, 98 skills), ARA Rigor Reviewer SKILL.md,
> brainstorming-research-ideas SKILL.md, creative-thinking-for-research SKILL.md, ARA Compiler
> SKILL.md, ARA Research Manager SKILL.md, hermes-agent reviewer-guidelines.md + experiment-patterns.md,
> openreviewer/README.md, our own research-operating-system.md + methodology-harvest.md.
>
> Purpose: find what we can ADOPT rather than build; identify the canonical SKILL.md structure.

---

## 1. Inventory of Existing Agent-Native Research Skills

### 1a. The ARA category (22-agent-native-research-artifact) — 3 skills

These are the closest match to our ROS commands. All three are true "agent-native" skills: they run
inside a Claude Code agent session, use only native file tools (Read, Write, Glob, Grep), produce
structured artifacts, and feed into each other.

| Skill | File | Purpose | Key Output |
|---|---|---|---|
| **ara-compiler** | `22-agent-native-research-artifact/compiler/SKILL.md` | Ingest any input (PDF, repo, logs, notes) → structured ARA with claims/exploration-graph/evidence | `ara/` directory with `logic/claims.md`, `trace/exploration_tree.yaml`, `evidence/` |
| **ara-research-manager** | `22-agent-native-research-artifact/research-manager/SKILL.md` | Post-task epilogue: scan conversation → extract decisions/experiments/dead-ends/pivots → write `ara/` with user-vs-AI provenance tags | Updated `ara/trace/exploration_tree.yaml`, `ara/logic/claims.md` |
| **ara-rigor-reviewer** | `22-agent-native-research-artifact/rigor-reviewer/SKILL.md` | Seal Level 2 semantic epistemic review: score 6 dimensions (evidence relevance · falsifiability · scope calibration · argument coherence · exploration integrity · methodological rigor) → `level2_report.json` | `level2_report.json` with grade (Strong Accept → Reject), severity-ranked findings |

The rigor-reviewer's 6 dimensions in full:
```
D1 Evidence Relevance  — does cited evidence substantively support each claim?
D2 Falsifiability      — are criteria actionable, non-trivial, scope-matched, independently testable?
D3 Scope Calibration   — do claims assert exactly what evidence supports, no more/less?
D4 Argument Coherence  — observation→gap→insight→solution→claims→evidence logical arc
D5 Exploration Integrity — does the tree document genuine process including failures?
D6 Methodological Rigor — baselines, ablations, statistical reporting, reproducibility
```

### 1b. Ideation skills (21-research-ideation) — 2 skills

| Skill | File | Purpose | Technique count |
|---|---|---|---|
| **brainstorming-research-ideas** | `21-research-ideation/brainstorming-research-ideas/SKILL.md` | 10 operational lenses: problem-first/solution-first · abstraction ladder · tension hunting · cross-pollination · "what changed" · failure analysis · simplicity test · stakeholder rotation · composition/decomposition · explain-it test | 10 frameworks + 3-phase workflow (diverge → converge → refine) |
| **creative-thinking-for-research** | `21-research-ideation/creative-thinking-for-research/SKILL.md` | 8 cognitive science frameworks: bisociation · problem reformulation · structure-mapping analogy · Boden constraint manipulation · negation/inversion (TRIZ) · abstraction laddering · adjacent possible (Kauffman) · Janusian/dialectical thinking | 8 frameworks; complements the brainstorm skill's workflow |

### 1c. Autoresearch — 1 skill (the orchestration layer)

`0-autoresearch-skill/` — two-loop architecture (inner optimization + outer synthesis), routes to all
domain skills, mandates `/loop` or heartbeat for continuous operation, produces `findings.md` as
persistent cross-session memory.

### 1d. Hermes-agent experiment-patterns.md (reference, not a SKILL.md)

Key patterns relevant to our commands:
- **Incremental saving + crash recovery** — skip-if-exists pattern for every experiment run
- **Artifact preservation** — save ALL intermediates, not just final result
- **Blind judge panels** — randomized labels + order per judge; Borda count; odd number of judges;
  conservative tiebreak (incumbent wins ties)
- **Separation of concerns** — generate / evaluate / visualize in separate scripts

---

## 2. Direct Comparison: Our 6 Commands vs. Existing Skills

### `/context-bundle`
**Our design:** prepend recent-negatives + forbidden-assumptions + must-read + hashes to every LLM
dispatch. Fail-closed: missing bundle → error not hallucination.

**Existing skill match:** PARTIAL. The hermes `experiment-patterns.md` has a config.yaml management
pattern and `run_experiment.py` skip-if-exists, but NO explicit forbidden-assumptions/negatives bundle.
The ARA Research Manager writes provenance but doesn't inject it at dispatch time. The ara-compiler
ingests context but doesn't auto-prepend it.

**Verdict:** BUILD. No adopt target. The closest prior art is in methodology-harvest.md §3 C8
("ContextBundle / forbidden-assumptions / failed-idea filter" from Experiment + InternAgent + Agora L-13)
which is also not yet a SKILL.md anywhere in this repo.

---

### `/exp-verify`
**Our design:** 3-stage gate: structural (no mock, all vars used) → execution (exit 0 + artifact exists)
→ plausibility (numbers in sane range) + anti-no-op log_assertion (intervention provably fired).

**Existing skill match:** PARTIAL. The hermes `experiment-patterns.md` has:
```python
def run_experiment(problems, strategies, output_dir):
    result_path = Path(output_dir) / problem["id"] / strategy / "result.json"
    if result_path.exists():
        print(f"Skipping {problem['id']}/{strategy} (already done)")
        continue
    result = execute_strategy(problem, strategy)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    with open(result_path, 'w') as f:
        json.dump(result, f, indent=2)
```
This handles the "artifact exists" check (structural layer) but has no mock-detection, no plausibility
check, and no log_assertion anti-no-op. The `D6 Methodological Rigor` dimension of ara-rigor-reviewer
checks "are experiment setups specific enough for independent replication" — but that is a post-hoc
reviewer, not a pre-promotion gate.

**Verdict:** BUILD. The 3-stage + anti-no-op pattern is unique to our design. Adopt the hermes
incremental-save pattern as a code skeleton for the "artifact exists" check (stage 2), but the
structural-no-mock and anti-no-op layers are ours to build.

---

### `/reward-hack-audit`
**Our design:** run the union guard set (min-form · per-example regression · neg-control consistency ·
holdout · token-shuffle) before any promote/bank/merge/write-up. Binds to external artifacts (sealed
holdout, pre-declared thresholds, code hashes).

**Existing skill match:** CLOSEST = ara-rigor-reviewer D1 (evidence relevance) + D6 (methodological
rigor). From the SKILL.md:
```
D1 — "Type-aware entailment: causal claim → needs isolating ablation;
      improvement claim → needs baseline comparison"
D6 — "Are baselines adequate? Ablation coverage? Statistical reporting? Metric-claim alignment?"
```
The rigor-reviewer is the closest to a reward-hack audit in spirit, but it operates POST-ARTIFACT on
an ARA (structured artifact), not as a before-promotion gate on raw experiment outputs. It also does NOT
run the token-shuffle ablation, per-example regression, or neg-control flat check.

**Verdict:** ADAPT. Use the rigor-reviewer's D1/D6 rubric and severity-ranking schema as the scoring
template for `/reward-hack-audit`, but extend it with: min-form gate, per-example regression check,
neg-control consistency, token-shuffle detection, cache/leakage check. Our command fires BEFORE the
ARA stage; the rigor-reviewer fires AFTER.

---

### `/baseline-champion`
**Our design:** an independently tasked + budgeted adversary with veto. Proposer may NOT choose the
baseline family, budget, stopping rule, or sign-off wording. Dispatched via Codex (+Pro).

**Existing skill match:** The hermes `experiment-patterns.md` blind judge panel is structurally
analogous:
```python
# Randomize labels and presentation order per judge
methods = list(outputs.keys())
random.shuffle(methods)
labels = {m: chr(65 + i) for i, m in enumerate(methods)}
# Conservative tiebreak: Incumbent/baseline wins ties (prevents false positives)
```
The "baseline wins ties" rule is exactly our "independent adversary with veto" principle operationalized
for LLM judge panels. The D6 rigor-reviewer checks "Are baselines recent and relevant? Flag experiments
with no baseline for comparative claims" — but again, post-hoc.

**Verdict:** ADAPT. Lift the hermes blind-judge panel's structure (randomize order + labels, Borda
count, odd judges, conservative tiebreak) as the judge-administration scaffold. Our `/baseline-champion`
is the dispatch-and-budget wrapper around this, with the adversary being Codex/Pro rather than an LLM
judge.

---

### `/bank-negative`
**Our design:** convert a kill into a structured NegativeCase — failure-type A–E, ≥2 ruled-out,
≥1 surviving alternative, concrete retry condition, next discriminating probe.

**Existing skill match:** PARTIAL. The ARA Research Manager writes dead-ends to `trace/exploration_tree.yaml`:
```yaml
# From research-manager SKILL.md:
Event Type: Dead End | Signals: "Approach abandoned, 'doesn't work', reverted"
Routes To: trace/exploration_tree.yaml
```
But the ARA Research Manager's dead-end record is minimal — it captures that a path was abandoned,
not a structured A–E failure taxonomy with ≥2-ruled-out and retry conditions. The ara-rigor-reviewer
D5 (Exploration Integrity) checks:
```
"Dead-end quality: Is the failure_mode specific enough to be actionable?
('Didn't work' is bad. 'Divergence after 1000 steps due to gradient explosion' is good.)
Is the lesson a genuine transferable insight?"
```
This is the *review criterion* for what a good dead-end looks like — which is exactly the spec for our
`/bank-negative` output format.

**Verdict:** ADAPT. Adopt the ARA Research Manager's `exploration_tree.yaml` node structure as the
file format for banked negatives, and use the ara-rigor-reviewer D5 "dead-end quality" rubric as the
VALIDATION criterion for what a well-formed negative case must contain. Extend with our A–E failure
taxonomy, ≥2-ruled-out field, and retry-condition.

---

### `/claim-evidence-matrix`
**Our design:** before paper-mode / external claim / upgrade — map every claim to evidence TYPE or
downgrade to hypothesis.

**Existing skill match:** DIRECT. The ara-rigor-reviewer D1–D3 combined IS a claim-evidence matrix:
- D1: "for each claim-experiment pair linked through Proof/Verifies: does evidence substantively support?"
- D3: "Scope Calibration — do claims assert exactly what evidence supports, no more/less?"

From SKILL.md (Step 3):
```
claim_proof_map: for each claim, the set of experiment IDs in its Proof
experiment_verifies_map: for each experiment, the set of claim IDs in its Verifies
```
And the type-aware entailment table:
```
Causal claim → needs isolating ablation
Generalization claim → needs heterogeneous test conditions
Improvement claim → needs baseline comparison
Descriptive claim → needs representative sampling
Scoping claim → needs declared bounds
```

**Verdict:** ADOPT AND EXTEND. The rigor-reviewer's D1+D3 rubric + claim_proof_map structure can be
lifted directly as the core of `/claim-evidence-matrix`. Our command fires as a pre-paper-mode GATE
(with auto-downgrade logic), whereas the rigor-reviewer is a full post-artifact audit. Extract the
type-aware entailment table and the claim→evidence-type→downgrade logic; wrap in a command that runs
before the ARA compiler (not after it).

---

## 3. Best SKILL.md Template Structure

The gold-standard template is the `ara-rigor-reviewer` SKILL.md
(`22-agent-native-research-artifact/rigor-reviewer/SKILL.md`, 323 lines).

Key structural pattern to use:

```markdown
---
name: <kebab-case-name>
description: <third-person, one-sentence: what it does + WHEN to use it>
version: 1.0.0
author: <org>
license: MIT
tags: [TitleCase, Tags, List]
dependencies: []
---

# <Display Title>

<One-paragraph framing: what role you play, what you produce, what tools you use, what you
DON'T do.>

**Prerequisite**: <what must already exist/pass before this fires>

---

## <Core Section — the procedure or frameworks>

### Step N: <Verb phrase>

<For procedural skills: numbered Steps with explicit sub-items>
<For framework skills: numbered Frameworks with Workflow + Self-Check per framework>

---

## <Scoring / Output Schema> (if applicable)

<For reviewer/gate skills: scoring anchors 1-5 per dimension, with examples at each anchor>
<Output: JSON schema or markdown template for the artifact this skill produces>

---

## Critical Rules

<3-7 numbered rules that override any default behavior; these are the "never do X" constraints>

---

## Reference

See [references/<file>.md](<path>) for <deeper detail>.
```

Key SKILL.md design principles observed across the best skills:

1. **Frontmatter is machine-readable** — `name`, `description`, `version`, `tags`, `dependencies`
   in YAML block. The `description` field is used for skill discovery; third-person, includes
   WHEN to use.
2. **"Do NOT use this skill when" block** — explicit anti-trigger prevents misuse and skill conflicts.
   The brainstorming skill uses it to redirect to creative-thinking (complementary, not duplicate).
3. **Scoring anchors are 5-point with concrete examples** — not vague rubrics. The rigor-reviewer
   gives verbatim examples at each anchor level (e.g., score 5 = "specific, actionable, independently
   testable falsification criteria matching the claim's scope").
4. **Output is a typed artifact** — every procedural skill names the exact file it writes
   (`level2_report.json`, `ara/trace/exploration_tree.yaml`, etc.) with a schema.
5. **Critical Rules section** — numbered, verb-imperative, put at end. These are the "never/always"
   guards that override any flexibility in the body (e.g., "No false grounding: support must flow
   through Proof → experiments.md → evidence/").
6. **Progressive disclosure via references/** — the SKILL.md is 50-350 lines of actionable guidance;
   deep documentation lives in `references/` (300KB+). Don't embed everything in SKILL.md.
7. **Agent-addressed** — the skill speaks directly to the agent in second person ("You are...",
   "Your job is...") for procedural skills, but uses third person in the description frontmatter.

---

## 4. What openreviewer and hermes reviewer-guidelines confirm about the un-gameable-core

### openreviewer/README.md

Explicit statement on the human-automation boundary:
> "OpenReviewer aims to assist authors with pre-submission feedback while maintaining the highest
> standards of scientific rigor. It is designed to **complement, not replace, human peer review.**"

The model is fine-tuned on 79K expert reviews and generates technical/methodology quality assessments —
soundness, experimental rigor, reproducibility. What it does NOT generate is a novelty/significance
verdict that stands alone: it mimics the written form of human reviews (which include novelty scores),
but the README's positioning statement makes clear the novelty judgment remains human-adjudicated.

### hermes-agent reviewer-guidelines.md

The four universal reviewer dimensions are: Quality (technical soundness), Clarity, Significance,
**Originality (Novelty)**. The guidelines note on Originality:

> "What reviewers ask: Does this provide new insights? How does it differ from prior work?
> Is the contribution non-trivial?
> Key insight from NeurIPS guidelines: 'Originality does not necessarily require introducing an
> entirely new method. Papers that provide novel insights from evaluating existing approaches or
> shed light on why methods succeed can also be highly original.'"

The "why methods succeed" framing reveals the core: novelty is a judgment about whether the INSIGHT
is new to the community — which requires community-level taste, not just text-matching. The
reviewer-guidelines explicitly list what reviewers should AVOID: "demanding unreasonable additional
experiments" and "rejecting for missing citations to reviewer's own work" — but nowhere do they
suggest novelty can be auto-decided.

### ara-rigor-reviewer SKILL.md — the structural proof

The 6 scored dimensions (D1–D6) are entirely absent of novelty and significance. The rigor-reviewer
explicitly scores what CAN be checked by an agent with read-only artifact access:
- Evidence supports claims (D1)
- Claims are falsifiable (D2)
- Claims are correctly scoped (D3)
- Argument is coherent (D4)
- Exploration is honestly documented (D5)
- Methodology is rigorous (D6)

And from the Critical Rules:
```
"Calibrated scoring: Most competent ARAs should land in the 3-4 range. A score of 5 means
genuinely excellent, not just 'no problems found.'"
```

The absence of "D7 Novelty" and "D8 Significance" is not an oversight — it confirms the design
principle: an agent can assess rigor and coherence but NOT whether the contribution is worth the
community's attention. That judgment requires external knowledge of what the community already knows
and what it needs — i.e., human taste.

### Synthesis for our un-gameable-core principle

The ARA rigor-reviewer's 6 dimensions map cleanly to our L1 (experiment rigor) layer:
- D1/D3/D6 → `/claim-evidence-matrix` + `/reward-hack-audit`
- D2 → pre-registered falsifier
- D4 → argument coherence = `/context-bundle` at dispatch
- D5 → `/bank-negative` + exploration integrity

What sits OUTSIDE all three sources (openreviewer + hermes + ara-rigor-reviewer) and remains
human-only:
- Novelty/significance judgment (is this worth the community's attention?)
- Claim scope decision (is this paper-worthy or workshop-worthy?)
- External decision precommitment (who changes their mind if X is shown?)
- Baseline family selection (what is the strongest realistic comparison?)

These are exactly the 4 items in our §3 GATE list — confirming the un-gameable-core is correct.

---

## 5. Recommended Build Strategy

### Commands to build from scratch (no close adopt target)
- `/context-bundle` — novel; no prior SKILL.md exists
- `/exp-verify` — novel; hermes patterns only cover stage 2 (artifact exists)

### Commands to build by ADAPTING existing SKILL.md content
- `/reward-hack-audit` — adapt ara-rigor-reviewer D1+D6 rubric + severity schema; extend with
  min-form, per-example, token-shuffle, cache layers
- `/baseline-champion` — adopt hermes blind-judge-panel structure (randomize/Borda/conservative
  tiebreak) as the judge-administration scaffold; wrap with dispatch+budget+veto logic
- `/bank-negative` — adopt ara-research-manager's `exploration_tree.yaml` dead-end node format;
  validate against ara-rigor-reviewer D5 "dead-end quality" rubric; extend with A–E taxonomy
- `/claim-evidence-matrix` — ADOPT ara-rigor-reviewer D1+D3 directly (claim_proof_map +
  type-aware entailment table); wrap as pre-paper-mode gate with auto-downgrade

### Commands that should NOT be built as agent-runnable gates
- Novelty/taste gate — confirmed un-gameable by openreviewer + hermes + rigor-reviewer absence
- Baseline family selection — adversary must be independent (per our §3 GATE + hermes blind-judge)
- Paper-worthiness decision — human only (confirmed by all three sources)

---

## 6. Summary (6 lines)

1. **The ara-rigor-reviewer** (`22-agent-native-research-artifact/rigor-reviewer/SKILL.md`) is the
   closest existing skill to our entire ROS: its D1+D3 = `/claim-evidence-matrix`; D2 = pre-registered
   falsifier; D5 = `/bank-negative`; D6 = `/reward-hack-audit` baseline check — adopt these directly.
2. **Two commands to build from scratch:** `/context-bundle` (no prior SKILL.md) and `/exp-verify`
   (hermes covers only the artifact-exists check; the no-mock + anti-no-op layers are novel).
3. **Best SKILL.md template:** use the ara-rigor-reviewer as the canonical structure — YAML frontmatter
   with third-person description + "Do NOT use when" block + numbered Steps + 5-point scoring anchors
   with concrete examples + typed output artifact + Critical Rules section + `references/` for depth.
4. **The un-gameable-core is confirmed by all three sources:** openreviewer says "complement, not
   replace"; hermes reviewer-guidelines treats novelty/significance as human-adjudicated; the
   ara-rigor-reviewer's 6 dimensions contain NO novelty or significance dimension by design.
5. **Ideation skills** (`brainstorming-research-ideas` + `creative-thinking-for-research`) cover the
   diverge/converge/refine workflow and 18 cognitive frameworks — fold the tension-hunting (F3),
   failure analysis (F6), constraint manipulation (F4), and adjacent-possible (F7) lenses into our
   `/ideate` Stage-1 rather than rebuilding them.
6. **The ara-research-manager** provides the right provenance format for our RUNLOG/tree discipline
   (user-vs-AI tags, event-type routing to the right ARA file) — adopt its event taxonomy and
   `exploration_tree.yaml` node schema as the canonical format for our Arbor tree updates.
