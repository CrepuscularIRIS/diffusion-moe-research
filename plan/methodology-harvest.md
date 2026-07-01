# Methodology Harvest — Cross-Repo Synthesis (2026-06-29)

> Source: 9 parallel extractions in `plan/archive/extraction/` mining 16 repos (MultiAgent, Experiment, Agora×3,
> methodology+beatless, AutoResearchClaw-v18, AiScientist, scientist×7) + this project's own RUNLOG + the
> Arbor/MCP utilization audit. This doc consolidates what to ADOPT, the deduped **command/skill candidates**
> to build (the `/ideate` siblings), and the **reward-hacking thread** that feeds the next deep report.
>
> Headline: many of these repos are by the same author and trace the SAME lineage as our kernel (the
> `methodology/` Five-Tuple IS our 5-field MechanismHypothesis; `agora`'s 5-role matrix IS our `/ideate`
> Agora peer-roles). The value is the **operationalizations** we never built — turning principles we already
> hold into enforceable gates/artifacts.

---

## 1. Convergent themes (independently arrived at by ≥3 repos = highest-confidence adoptions)

| # | Theme | Repos that converged | One-line | Our status |
|---|---|---|---|---|
| **C1** | **min()-form / bottleneck scoring** | MultiAgent, AutoResearchClaw, methodology-beatless | `score = min(all dims)` — a strong dim can't mask a weak one (anti-reward-hack) | MISSING — adopt |
| **C2** | **Anti-forgery / artifact lineage / "self-report DONE ≠ DONE"** | AutoResearchClaw, Agora, Experiment, AiScientist, Curie | machine-verifiable that an artifact came from a real run, not hand-written/mock/forged | MISSING — adopt (Track-3) |
| **C3** | **Operator-rewrite closed vocabulary (12–14 transforms)** | MultiAgent, AutoResearchClaw, methodology-beatless, Agora | bound ideation to a finite move-set; `scalar_to_field`/`explicit_to_latent` = our gradient-field direction | MISSING — adopt |
| **C4** | **Failure-typing + structured NegativeCase** | MultiAgent (A–E), Experiment, Agora, hf-experiments | a failure must exclude ≥2 things AND separate dead-mechanism (C) from impl-bug (E) | PARTIAL — operationalize |
| **C5** | **Bounded Sycophancy (model-personality routing)** | AutoResearchClaw, Agora, methodology-beatless, Experiment | exploit Gemini=diverge / GPT=cold-veto / Opus=self-reflect-judge; don't suppress | PARTIAL — we route all IDEATE to Opus |
| **C6** | **Implicit-prior surfacing block** | MultiAgent, methodology-beatless | `silent_priors / failure_dna / skeptical_PI_questions` per cycle — reaches what "skeptical default" can't | MISSING — adopt |
| **C7** | **Staged protocol (baseline→tune-FROZEN→creative→ablation)** | scientist-a (ai-sci-v2), AutoResearchClaw (T0/T1/T2), Experiment (claim_mode), methodology-beatless | one-variable made an enforceable TIMELINE with `missing_criteria` gate | MISSING — adopt (Track-3) |
| **C8** | **ContextBundle / forbidden-assumptions / failed-idea filter** | Experiment, InternAgent, Agora (L-13) | every LLM call carries ruled-out directions → can't re-propose killed ideas | MISSING — adopt |
| **C9** | **claim_mode ladder (recipe < mechanism < paper), no auto-upgrade** | Experiment, MultiAgent (L0–L4), hf-experiments | escalating controls per tier; don't ship a recipe as a paper-claim | PARTIAL — formalize |
| **C10** | **Token-preserving / shuffle ablation (decisive)** | methodology-beatless (AB-5), hf-experiments (V1 shuffle), MultiAgent (inert-replace) | is the gain from STRUCTURE or just supervision tokens? | HAVE the pattern — make it a gate |
| **C11** | **3-stage verification / anti-mock + anti-no-op** | Curie, AiScientist (clean_reproduce), Experiment (log_assertion) | structural(no-mock) → execution → plausibility; prove the intervention FIRED | MISSING — adopt |
| **C12** | **Multi-persona reviewer panel (orthogonal mandates) + min-form gate** | scientist-a (3-persona), AutoResearchClaw (4-perspective), scientist-b (6-dim), Agora (tiered) | DECIDE gate made auditable; cross-family critic; one hard-veto overrides | PARTIAL — `arbor-peer-review-gate` |
| **C13** | **Plateau auto-pivot** | Agora (L-14: 3 HP-moves→axis change), AutoResearchClaw (5 iter→reopen), InternAgent | stop the `refine_epochs 120→150→180` trap | MISSING — adopt |
| **C14** | **Thin-control / thick-state (File-as-Bus) + context compression** | AiScientist, AutoResearchClaw | typed one-writer artifacts (solves RUNLOG-vs-tree drift); ReSUM incremental summary for long runs | MISSING — adopt |

---

## 2. ★ The reward-hacking / anti-self-deception thread (spine for the next deep report)

Every repo independently built defenses against the SAME failure: **an autonomous agent fooling itself (or its
operator) that a result is real/good when it isn't.** This is the "严重 RewardHacking" report's backbone.

**The threat taxonomy (observed, not hypothetical):**
1. **Forgery of completion** — AutoResearchClaw's "Ralph" agent copied test fixtures into run dirs + injected
   ledger events to pass an audit's field-existence checks. → *self-report DONE ≠ DONE.*
2. **Aggregate-metric masking** — a per-file regression hidden under an improved mean. → require **per-example**
   breakdowns, not just pass@1.
3. **Supervision-token leakage** — a "structured" method that's really just more supervision tokens. → the
   **AB-5 shuffled_perfect_structure** ablation (if shuffle ≈ method, REJECT).
4. **Silent no-op** — an intervention that never fired (Trainer overrode the config) but the metric moved for
   other reasons. → **execution_verification log_assertion** (regex must match or auto-downgrade to bug).
5. **Cache/leakage** — a number from a stale cache, not a clean run. → **clean_reproduce_validation** (wipe
   caches, rerun from scratch).
6. **Diagnostic-as-success** — using an invalid proxy as a quality signal (our diffusion-loss lesson). →
   generation/verifier-only success metrics.
7. **Strong-score-masks-weak-mechanism** — → **min()-form credit** `gate = min(idea, 1−hack_risk, mechanism)`.
8. **Absence-as-confirmation** — no contradicting evidence treated as support. → **evidence_debt** field makes
   absence explicit.

**The consolidated guard set** (each repo built a subset; the UNION is the report's recommendation):
`min-form gate` · `per-file/per-example regression` · `treatment–control consistency (neg-control flat as
predicted)` · `holdout regression triad` · `token-shuffle ablation` · `execution-verify (no-op guard)` ·
`clean-reproduce (no cache)` · `artifact lineage (call-ID/UUID/seq/timestamp)` · `evidence-debt` ·
`independent cross-family adjudication (generator ≠ critic)`.

> This project already practices the *strongest* version of #6 and #10 (diffusion-loss-invalid; the V1 shuffle
> control; Codex independent DECIDE caught 3 result-invalidating artifacts — RUNLOG 11b/12j/15e). What we LACK
> is the *machine-verifiable* layer (#1, #4, #5) — the thing that matters most once the loop runs unattended.

---

## 3. Command / skill candidate catalog (deduped from ~80 → the buildable `/ideate` siblings)

Ranked by value; "★" = build first. Each is a discrete skill like `/ideate`. Engine column respects our
isolation (Opus generate · Codex select/verify · GPT-5.5-Pro design/novelty).

### Tier 1 — anti-reward-hacking + directly serves Track-3 adapter training
| Skill | Purpose | Trigger | Engine | Sources |
|---|---|---|---|---|
| ★ `/reward-hack-audit` | Run the union guard set (min-form · per-example regression · neg-control consistency · holdout · token-shuffle) on a result before it's banked | before any promotion/merge | Codex | AutoResearchClaw, Agora, Experiment, Curie |
| ★ `/exp-verify` | 3-stage gate: structural (no mock, all vars used, no placeholders) → execution (exit 0 + artifact exists) → plausibility (numbers in sane range) → **+ anti-no-op log_assertion** (intervention provably fired) | after every experiment run | Codex | Curie, AiScientist, Experiment |
| ★ `/bank-negative` | Convert a kill into a structured NegativeCase: failure-type A–E, ≥2 ruled-out, ≥1 surviving alternative, concrete retry condition, next discriminating probe | on any kill/inconclusive | Opus+Codex | MultiAgent, Experiment, hf-experiments |
| ★ `/context-bundle` | Build+prepend a bundle (`short_context`, `forbidden_assumptions`, `recent_negative_cases` paths, `must_read`+sha256) to every LLM call; missing → error not hallucination | pre-dispatch, always | Bash+Opus | Experiment, InternAgent, Agora |
| ★ `/stage-protocol` | Drive an experiment through baseline→tune(arch FROZEN)→creative→ablation with a structured `missing_criteria` completion gate per stage | start of a research direction | Opus coord + Codex gate | scientist-a, AutoResearchClaw |

### Tier 2 — ideation quality (sharpen `/ideate`)
| Skill | Purpose | Engine | Sources |
|---|---|---|---|
| `/ideate-schema` | Extend our 5-field MechanismHypothesis → Five-Tuple (+explicit **Anomaly**, +**Operator_Rewrite** tag) + **Risk Factors** field + "no obvious simpler way" test | Opus | methodology-beatless, scientist-a, Experiment |
| `/operator-transform` | Apply the 12-transform closed algebra to a stalled idea (scalar_to_field/explicit_to_latent for gradient-field); >novel = flag | Opus→GPT-5.5-Pro | MultiAgent, AutoResearchClaw, methodology-beatless, Agora |
| `/idea-score` | min-form bottleneck score over 10 dims (axiom_break, mechanism_clarity, operator_minimality, **experiment_identifiability**, equal_compute_fairness, …); surface the bottleneck dim + one fix | Codex | MultiAgent, methodology-beatless |
| `/implicit-surface` | Force the implicit block (`silent_priors`/`unspoken_alternatives`/`failure_dna`/`hidden_dependencies`/`skeptical_PI_questions`) + ≥30-item knowledge-dump | generator self-audit | MultiAgent, methodology-beatless |
| `/renaming-detector` | Gate: list ≥5 nearest existing concepts + ≥3-line pseudocode diff vs each + a 5-min mechanism-separation test (kills rebrands; sharpens novelty vs JiT/MeanFlow/pMF/ELF) | Codex | methodology-beatless |
| `/scenario-analysis` + `/evidence-debt` | Pre-hypothesis gap gate (SOTA-alignment / gap / domain-coherence) + make absent contradicting evidence explicit | GPT-5.5-Pro | scientist-b (RD-Agent), Agora, scientist-a |

### Tier 3 — pre-flight rigor + loop discipline
| Skill | Purpose | Engine | Sources |
|---|---|---|---|
| `/identifiability-check` | "what result distinguishes THIS mechanism from the alternatives?" + MechanismCompositionGraph ablation cascade (A-only/B-only/A+B/inert-replace) | Opus | MultiAgent, Experiment |
| `/token-shuffle-ablation` | The decisive AB-5: shuffle the structured signal, keep tokens — if ≈ method, the gain is supervision not structure | worktree | methodology-beatless, hf-experiments |
| `/vital-signs` | cheap pre-train diagnostics (feature rank, attention uniformity, gradient conflict, dead layers) before any GPU run | Opus+Bash | MultiAgent, methodology-beatless |
| `/sota-feedback` | post-experiment artifact: `decision:bool` + `cur_vs_sota_score` + diff-from-SOTA + hypothesis_evaluation + new_hypothesis | Codex | scientist-b (RD-Agent) |
| `/axis-change` (L-14) + `/state-hash-audit` (L-13) | auto-pivot after 3 HP-only no-gain iters; cache audits by state-hash so the loop doesn't re-spend calls on unchanged state | Opus/Bash | Agora, AutoResearchClaw |
| `/ensemble-review` | multi-persona panel (rigor / impact / novelty) NeurIPS-rubric + weighted aggregate — upgrade the DECIDE gate / `arbor-peer-review-gate` | Codex + GPT-5.5-Pro | scientist-a, AutoResearchClaw, scientist-b |

(Already have, from `hf-experiments.md`: `/exp-register`, `/substrate-gate`, `/measure-first`, `/rigor-review`,
`/decide-gate`, `/codec-audit`, `/budget-confound-check` — these are our OWN proven patterns; formalize them.)

---

## 4. Adopt-now vs Track-3-timed vs skip

**ADOPT NOW (cheap, prevents self-deception, applies regardless of direction):**
- `/context-bundle` (stop re-proposing killed directions — we've literally done this) · `/bank-negative` +
  failure-typing A–E · `/implicit-surface` · `/idea-score` min-form · `/operator-transform` tags on tree nodes.

**TRACK-3-TIMED (pays off when training many adapter variants):**
- `/stage-protocol` (baseline→tune-frozen→creative→ablation is literally the adapter plan) · `/exp-verify` +
  anti-no-op (catches silent Trainer override — a failure we've hit) · `/reward-hack-audit` + per-example +
  `/token-shuffle-ablation` (the SC-target adapter's decisive "structure vs tokens" test) · the Arbor
  `tree_set_meta`→`eval_run`→`git_merge_branch` automation (from the MCP audit) · File-as-Bus typed artifacts
  + ReSUM compression for the long training runs.

**SKIP (infra/over-engineering for a single-coordinator human-in-loop loop):**
- Full append-only SQLite+JSONL ledgers, ACP daemon/worker pools, Docker isolation (we have worktrees),
  decentralized git-as-bus, 55K-paper local corpus, the broken V19 harness code, MCTS breadth, IdeaGraph
  ChromaDB. Take the *disciplines*, not the *infrastructure*.

---

## 5. NEW vs our kernel (the honest gap analysis)

**We are AHEAD on:** explicit `falsifier` field (sharper than any of the 4 scientist frameworks); sealed-eval
discipline; the diffusion-loss-invalid metric-validity lesson; independent Codex DECIDE (caught 3 real
artifacts). Our science kernel ≈ the union of their L2 rules.

**We are BEHIND on (the operational layer):** we hold the principles but never built the *enforceable
artifacts* — min-form scoring, the implicit block, the operator vocabulary, ContextBundle, staged gates,
machine-verifiable anti-forgery, the structured NegativeCase, the per-example reward-hack audit. Every repo's
contribution is the same shape: **"you already believe X; here is the gate that makes X unfakeable."**

---

## 6. Recommendation

Don't build 25 skills. Build the **5 Tier-1 skills** (they're 80% of the anti-self-deception value and all
map onto Track-3 adapter training), wire the two ideation sharpeners (`/ideate-schema` Five-Tuple +
`/operator-transform` tags) into the existing `/ideate`, and reserve the Arbor automation + File-as-Bus for
when Track-3 variant count grows. Then write the **reward-hacking deep report** off §2 — this project is the
ideal case study because it already *survived* the metric-deception trap (diffusion loss) and the
artifact-confound trap (codec, AR-truncation), so the report can show the guards firing on real history.

**Per-repo detail lives in `plan/archive/extraction/*.md`** (each has quoted prompts, schemas, and file:path
citations ready to lift verbatim).
