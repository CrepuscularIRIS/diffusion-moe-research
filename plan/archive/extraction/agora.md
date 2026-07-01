# Agora Cluster — Reusable Research Methodology Extraction

Date: 2026-06-29
Scope: `/home/lingxufeng/agent/agora`, `/home/lingxufeng/agent/agora-contract`, `/home/lingxufeng/research/AgoraArchive`
Purpose: Extract discipline and workflow patterns reusable in our DiffusionGemma autonomous research loop.

---

## 1. What It Is

Agora is a three-layer research runtime built by the same user over V18/V19 failures. The innermost layer (`AgoraArchive`) is a fully-implemented AutoResearch Kernel: an event-sourced, append-only ledger + worker pool + peer-agent subscription system with 8 verifier gates, driving a Failure-to-Hypothesis loop where GPU failures from a vision benchmark seed paper-retrieval, which seeds falsifiable hypotheses, which seed code patches, which get evaluated and promoted only after passing structural, semantic, execution, statistical, and reward-hacking gates. The middle layer (`agora-contract`) is a lightweight successor that delegates runtime to external agent fabrics (OpenClaw/Hermes) while keeping contract integrity (schemas + 4 gates + artifact lineage). The outermost layer (`agora`) is a standalone paper-corpus extraction pipeline that converts 55K OpenReview PDFs into structured knowledge tables (axioms, mechanisms, operator_moves, failure_modes) in SQLite, feeding the Experiment loop. The "Agora" in our `/ideate` skill refers specifically to the five-role model allocation matrix (Marshal/Muse/Weapon/Sapper/Herald) and the Diverge→Converge→Select discipline, which was formalized in `docs/model_allocation_2026-05-15.md`. The full system is substantially richer than those peer roles alone.

---

## 2. Core Methodology / Workflow Spine

### 2.1 Failure-to-Hypothesis Loop (AgoraArchive)

```
GPU failure cluster
  → AxiomMiner (Muse/Gemini divergent × N): extract first-principle axioms
  → PaperScout (Weapon/Codex search + Sapper/Kimi DR): retrieve prior evidence
  → HypothesisWriter (Gemini × N): write falsifiable hypotheses
  → HypothesisCritic (Weapon/Codex veto, cross-family): critique
  → OperatorTransform (Gemini × N): generate operator interventions
  → PatchCoder (Adjutant/Sonnet ACP): implement patch in worktree
  → EvalRunner (Script/GPU T0/T1/T2): measure
  → InterpretationPanel (Diverge+Challenge+Judge): explain
  → PromotionJudge (3-family vote → Marshal final): promote or retire
  → NegativeCaseCurator: record boundary conditions
```

### 2.2 Five-Role Model Allocation (the source of our "Agora peer-roles")

From `docs/model_allocation_2026-05-15.md` §0:

| Role | Chinese | Model | Function = Personality |
|---|---|---|---|
| **Marshal** | 元帅 | Claude Opus | Meta-cognition, final taste judgment, self-reflection |
| **Muse** | 缪斯 | Gemini CLI | Divergent generation — sycophancy is a FEATURE |
| **Weapon** | 武器 | GPT-5.5/Codex | Convergent veto, devil's advocate — rigor is a FEATURE |
| **Sapper** | 工兵 | Kimi | DeepResearch, long-context synthesis, grind |
| **Adjutant** | 副官 | Claude Sonnet | Structured execution, patch coding |
| **Herald** | 传令 | MiniMax | Chain orchestration — NEVER enters Critic/Judge chain |

**"Bounded Sycophancy" doctrine**: do not fight each model's natural personality; exploit it. Gemini's enthusiasm = divergent generation. GPT's cold rigor = veto. Opus's self-reflection = meta-taste. Kimi's tireless depth = DR. MiniMax's cheapness = routing.

### 2.3 Peer-Agent Subscription Architecture (decentralized)

Agents do NOT chat P2P. They subscribe to ledger event kinds and react:

```yaml
AxiomMiner:    subscribe: [benchmark.failure_clustered]  →  produce: axioms/*.json
PaperScout:    subscribe: [axiom.created]                →  produce: paper_candidate_cards/*.json
HypothesisCritic: subscribe: [hypothesis.created]       →  produce: critiques/*.json
PatchCoder:    subscribe: [operator.selected]            →  produce: patches/*/patch.diff
EvalRunner:    subscribe: [patch.codex_passed]           →  produce: evals/*/t0_result.json
```

The kernel does not call agents. It maintains a state matrix, assigns leases, wakes subscribers, checks artifact contracts, and writes an immutable ledger.

### 2.4 Diverge→Converge→Select Pattern (per capability)

| Phase | Width strategy | Engine |
|---|---|---|
| Axiom mining | Gemini × N (wide) | Muse |
| Hypothesis writing | Gemini × N (wide) | Muse |
| Critic/veto | Codex × N (parallel veto) | Weapon |
| Patch coding | Claude × 2-4 worktrees | Adjutant |
| T0 smoke | concurrent | Script |
| T1/T2 eval | top survivors only | Script |
| Interpretation | Diverge+Challenge+Judge | Muse+Weapon+Marshal |
| Promotion | 3-family vote + Marshal final | Weapon+Sapper+Muse → Marshal |

Budget rule: if T0 pass rate == 0, stop depth. If T0 high, narrow to top 1-2, deepen T1/T2. If 5 iterations no gain, reopen width with new axioms.

---

## 3. Experiment Standards / Specs (Gates, Checklists, Contracts, Review Discipline)

### 3.1 Eight Verifier Gates (AgoraArchive ROBUSTNESS_GATES.md)

All gates run as independent Python processes. Self-report "DONE" is never accepted. Promotion requires all 8 to pass.

| Gate | What it checks | Maps to our kernel |
|---|---|---|
| **IntegrityGate** | ledger seq continuous, ts monotone, UUID format, no bare mock, artifact has hash, no orphan files | — (new) |
| **SchemaGate** | JSON schema validation of every artifact | — (new) |
| **LineageGate** | 5-way join: artifact → producer_event → runtime_invocation → work_item → lease | — (new, strongest anti-forgery) |
| **SemanticGate** | hypothesis has cited axioms + falsifiability; critique has evidence_refs; paper_card has real paper_id | overlaps our falsifiability-first |
| **ExecutionGate** | patch diff exists + git apply passes; ACP session has tool.ended events with matching session/runtime/worker | overlaps our sealed eval |
| **TruthGate** | replay variance < 0.05 dB; ≥3 replays; adaptive up to 7 | overlaps our score≠mechanism |
| **RewardHackingGate** | PSNR↑ but LPIPS↑ detector; per-component asymmetry detector; holdout regression detector | new (strongest) |
| **PromotionGate** | all 7 gates ∧ tiered consensus (critic veto + 2-of-3 promoter families) | partial overlap arbor-peer-review-gate |

### 3.2 Anti-Forgery Discipline (15 LESSONS from V18/V19)

Source: `AgoraArchive/LESSONS.md` and `agora-contract/docs/LESSONS_inherited.md`

The five by-construction guards (G1-G5):

| Guard | Mechanism |
|---|---|
| **G1 Zero-forgery** | UUID format + field count + seq continuous + ts monotone + 5-way lineage join |
| **G2 Replayable** | append-only ledger + state_hash + deterministic replay |
| **G3 Failure-recoverable** | lease + heartbeat + watchdog reclaim + idempotent retry |
| **G4 No central master** | shared ledger + git-as-bus + peer cross-review |
| **G5 Zero mock whitewash** | mock must use `mock:*` namespace; bare "mock" = raise; missing upstream = raise, not fallthrough |

Critical L-lesson that maps directly to our loop:
- **L-13**: Audit is stateless — "state_hash" on every gate verdict; agent must NOT re-run same state. (We have this pattern implicitly in our Arbor loop but no enforcement.)
- **L-14**: Hyperparameter tuning ≠ architecture fix. Auto-trigger "axis change" after 3 consecutive HP moves without metric gain. (Direct analog to our "5 iterations no gain → reopen width".)
- **L-15**: Documentation update ≠ progress. Progress = new artifacts + dispatch traces + gate passes. (We need this in our RUNLOG discipline.)
- **L-2**: Agent will forge markers. The full 5-way lineage join is the only structural defense.
- **L-3**: `claude --print` wastes 95% of ClaudeCode's value. Use task-publish + long-running ACP session.

### 3.3 Artifact Contract (minimal required fields)

Every artifact entering the ledger must carry:
```json
{
  "producer_api_call_id": "UUID (must be in ledger)",
  "source_runtime_kind": "RuntimeKind enum or mock:*",
  "content_hash": "sha256 64-hex",
  "produced_at": "ISO 8601 with timezone"
}
```

Schema files (canonical, copy-ready): `agora-contract/schemas/` — 10 JSON Schema files.

### 3.4 Role-Boundary Gate (LineageGate §7)

```python
# Cross-family critic: critic model family must DIFFER from producer family
if role.endswith("Critic") and model_family(critic) == model_family(producer):
    raise GateFail("INV-CROSS-FAMILY")

# Judge must be Marshal (Opus only)
if role.endswith("Judge") and model_family(judge) not in {"anthropic"}:
    raise GateFail("INV-JUDGE-MUST-BE-MARSHAL")

# Herald (MiniMax) cannot enter Critic/Judge chain
if model_family(actor) in {"minimax"} and role in {Critic, Judge, ...}:
    raise GateFail("INV-HERALD-NOT-DECISION-MAKER")
```

Source: `agora-contract/docs/model_allocation_2026-05-15.md` §7, `contract/families.py`.

---

## 4. Reusable Artifacts — Quoted Prompts, Templates, Rubrics, Schemas

### 4.1 Axiom Card Schema (canonical)

File: `/home/lingxufeng/research/AgoraArchive/schemas/axiom_card.schema.json`

```json
{
  "required": ["axiom_id", "statement", "falsifiability", "source"],
  "properties": {
    "axiom_id": {"type": "string"},
    "statement": {"type": "string", "minLength": 8},
    "falsifiability": {"type": "string", "minLength": 8},
    "source": {"type": "string"},
    "created_at": {"type": "string", "format": "date-time"}
  }
}
```

Live examples from `AgoraArchive/blackboard/axioms/`:

```json
{
  "axiom_id": "axiom_ssim_locality",
  "statement": "Structural similarity (SSIM) preserves local perceptual structure better than per-pixel L2 because its window-based luminance/contrast/structure decomposition concentrates gradient where perceptual differences are large; therefore a mask-weighted SSIM term provides a more faithful supervision signal in salient regions than uniform L2 on the same region.",
  "falsifiability": "Falsified if a mask-weighted SSIM loss does not yield higher region-PSNR than a mask-weighted L2 baseline by at least 0.05 dB on a held-out subject, averaged over 3 replays with identical optimizer, schedule, and seed.",
  "source": "Wang et al., IEEE TIP 2004"
}
```

### 4.2 Hypothesis Schema (canonical)

File: `/home/lingxufeng/research/AgoraArchive/schemas/hypothesis.schema.json`

```json
{
  "required": ["hypothesis_id", "statement", "cited_axiom_ids", "expected_effect_direction", "falsifiability"],
  "properties": {
    "cited_axiom_ids": {"type": "array", "minItems": 1},
    "expected_effect_direction": {"enum": ["improve", "degrade", "neutral"]},
    "falsifiability": {"type": "string", "minLength": 8},
    "reasoning_chain": {"type": "array", "items": {"type": "string"}}
  }
}
```

SemanticGate requirement on hypothesis: `reasoning_chain` must contain `failure → axiom → paper` triple.

### 4.3 Critique Schema with Rubric (canonical)

File: `/home/lingxufeng/research/AgoraArchive/schemas/critique.schema.json`

```json
{
  "required": ["target_hypothesis_id", "verdict", "evidence_refs", "rubric_scores", "summary"],
  "properties": {
    "verdict": {"enum": ["pass", "fail", "conditional"]},
    "evidence_refs": {"type": "array", "minItems": 1},
    "rubric_scores": {
      "required": ["grounded", "falsifiable", "novel"],
      "properties": {
        "grounded":    {"type": "number", "minimum": 0, "maximum": 1},
        "falsifiable": {"type": "number", "minimum": 0, "maximum": 1},
        "novel":       {"type": "number", "minimum": 0, "maximum": 1}
      }
    }
  }
}
```

### 4.4 Paper Extraction Prompt v5 (8-aspect, anti-fabrication)

File: `/home/lingxufeng/agent/agora/scripts/extract_phase1_prompt_v5.txt` (hash: b5dc69d9cb58ee16)

Key rules (extractable for any structured paper extraction task):
- **RULE 1 TRUTHFULNESS**: only emit content literally visible in input text; empty array beats fabrication
- **RULE 2 REFUSAL CONTRACT**: garbled input → `{"status":"refuse","reason":"..."}` (first-class outcome, not failure)
- **RULE 3 CLOSED SETS**: `operator_rewrite`, `paper_move_template`, `confidence` from fixed enums
- **RULE 5 UNCERTAINTY DISCIPLINE**: empty array beats guessing
- **RULE 7 DISTINCTIONS**: axiom (first-principle about the world) vs mechanism (causal chain explaining failure) vs operator_move (high-level method transform)

Eight extracted aspects: metadata, axioms, experiment_design, claim_evidence_chain, limitations, failure_modes, mechanisms, operator_moves.

### 4.5 Operator Rewrite Closed Set (research vocabulary)

From `agora/Extension.md` and `scripts/extract_phase1_prompt_v5.txt`:

```
operator_rewrite (14 values):
  axis_rotation, fixed_to_adaptive, explicit_to_latent, one_pass_to_iterative,
  dense_to_state, posthoc_to_endogenous, scalar_to_field, module_to_protocol,
  average_to_routing, static_to_dynamical, local_to_conservation,
  benchmark_to_microscope, none, unknown

paper_move_template (10 values):
  Depth-as-Time, Reasoning-as-Dynamics, Memory-as-State, Failure-as-Signal,
  Metric-as-Mechanism, Ablation-as-Discovery, Boundary-first, Invariant-first,
  none, unknown
```

These are the most directly reusable abstractions for our gradient-field direction: "explicit_to_latent", "scalar_to_field", "Reasoning-as-Dynamics" all apply.

### 4.6 PaperCard v2 with Evidence Debt (retrieval format)

From `agora/Extension.md` §PaperCard v2:

```json
{
  "paper_id": "...",
  "relevance_type": ["supporting_evidence", "boundary_condition", "negative_result", "probe_template", "operator_move"],
  "supports": ["claim 1"],
  "refutes_or_limits": ["boundary condition"],
  "probe_templates": ["Compare X against Y as negative control"],
  "evidence_refs": [{"type": "quote", "table": "paper_failure_modes", "response_hash": "<hash>"}]
}
```

With explicit `evidence_debt` field in retrieval pack:
```json
{
  "evidence_debt": {
    "support_missing": false,
    "contradiction_missing": true,
    "probe_template_missing": false,
    "notes": "No explicit negative evidence found."
  }
}
```

**Key principle**: absence must be visible. If only supporting evidence exists, mark `evidence_debt` high rather than fabricating confidence.

### 4.7 PromotionJudge Hybrid (tiered consensus template)

From `docs/model_allocation_2026-05-15.md` §6:

```
Step1 (parallel ~3s, 3 family signal):
  ├── Weapon (Codex)   → veto / devil's advocate
  ├── Sapper (Kimi)    → DR-grounded check (any paper/repo counter-example)
  └── Muse (Gemini)    → math/distribution angle (mode collapse check)
  → ledger event: promotion.raw_vote × 3

Step2 (serial ~5s, Marshal meta-cognition):
  Marshal (Opus) reads 3 votes + artifact + critic verdicts
  → final ACCEPT / REJECT / REVIEW
  → ledger event: promotion.final_judged

Step3 (Herald writes outcome):
  Herald (MiniMax) translates final_judged to RunReporter summary
```

**Bottom logic**: Step1 = "3 families cannot all lie simultaneously". Step2 = "Opus catches blind spots all 3 missed". Step3 = "Herald echoes decision to operator, never influences it."

### 4.8 L-13 State-Hash Anti-Loop Pattern

```python
# Every gate verdict carries a state_hash
gate_verdict["state_hash"] = sha256(ledger_state + artifact_state)

# Scheduler rule: do not re-run same gate on same state_hash
if same_state_hash(prev_verdict, current_state):
    return cached_verdict  # not a new computation
```

Prevents agent loop from spending cycles re-running stateless audits that will return identical results.

---

## 5. Command / Skill Candidates

| Name | Purpose | Trigger | Engine |
|---|---|---|---|
| `/axiom-mine` | Extract ≤5 falsifiable first-principle axioms from a failure cluster or paper | After any failed experiment or when starting hypothesis generation | Muse (Gemini diverge) + Weapon (Codex veto) |
| `/hypothesis-write` | Convert axiom + paper evidence into a structured Hypothesis artifact (schema-valid, falsifier declared) | After axioms are selected | Muse (Gemini) + SemanticGate check |
| `/operator-select` | Map hypothesis to operator_rewrite and paper_move_template from closed set | Before patch dispatch | Weapon (Codex) |
| `/evidence-debt` | Run paper retrieval against our literature DB; return PaperCard v2 with explicit evidence_debt fields | Before promotion | Sapper (Kimi long-context) |
| `/promote-gate` | Run tiered consensus (3-family vote → Marshal final) on a hypothesis or experiment result | Before merging any "proven" claim into RUNLOG | Weapon + Sapper + Muse → Marshal |
| `/axis-change` | Detect plateau (3 consecutive HP moves, no metric gain) and trigger operator_rewrite pivot | After 3 failed experiment iterations | Opus (meta-cognition) |
| `/state-hash-audit` | Check current state_hash; skip if same as last verdict; report new gate results only | Before any audit loop | Script (deterministic) |
| `/paper-mine` | Extract 8-aspect structured knowledge from a PDF using the v5 prompt template | When adding papers to literature base | Any LLM (v5 prompt, Kimi preferred for cost) |

---

## 6. NEW vs Our Kernel

### ADOPT (genuinely novel relative to our L1/L2 kernel):

1. **Operator rewrite closed set + paper_move_template vocabulary** (`axis_rotation`, `scalar_to_field`, `Reasoning-as-Dynamics`, etc.). Our kernel has no equivalent. This gives a finite vocabulary for "what kind of change are we making" — directly applicable to gradient-field direction (explicit_to_latent, scalar_to_field are exact matches for MeanFlow/JiT/pMF operator types).

2. **Tiered consensus with Herald isolation**: The explicit rule that Herald (routing/cheap model) must NEVER enter the Critic or Judge chain, enforced by `LineageGate.check_role_boundaries()`. Our multi-engine isolation principle (§L2 kernel item 7) is equivalent in spirit but has no structural enforcement. The "critic veto is a hard veto" discipline — one Weapon NACK overrides all Muse/Sapper approvals — is stronger than our current arbor-peer-review-gate.

3. **5-way lineage join as completion proof**: `artifact → producer_event → runtime_invocation → work_item → lease`. Our system uses worktree isolation but has no equivalent structural proof that an artifact came from a real LLM call vs was hand-written or mock-injected. This is the anti-forgery backbone.

4. **evidence_debt field in retrieval results**: Making absence of contradicting evidence explicitly visible (not silently treating absence as confirmation) is a new discipline. Our kernel says "evidence ≠ memory" but doesn't have a structured field for it.

5. **L-13 state-hash discipline**: Gate verdict carries `state_hash`; same state = cached result; loop is blocked from re-running same audit. We have nothing equivalent — our RUNLOG sometimes shows loops repeating similar checks.

6. **L-14 hyperparameter plateau detector**: "3 consecutive HP moves, no gain → trigger axis change event". This is operationalized; our kernel says "score ≠ mechanism" but doesn't have the 3-move rule.

7. **PaperCard v2 structure**: Separating `supports` / `refutes_or_limits` / `boundary_conditions` / `probe_templates` into named buckets rather than a flat evidence list. The `probe_templates` bucket (what ablation experiment would test this mechanism) is especially useful for our gradient-field direction.

### OVERLAP (our kernel already covers):

- Cross-model critic isolation (our L2 item 7: generator/critic/selector isolation across distinct models = Agora cross-family critic rule)
- Sealed eval/test sets (our L2 item 3: sealed eval/test set = Agora ExecutionGate + TruthGate)
- Falsifiability-first (our L1 item 3 + L2 item 1: falsifiable > correct = Agora AxiomCard.falsifiability required)
- Failure shrinks search space (our L2 item 6 = Agora NegativeCaseCurator + Failure-to-Hypothesis loop)
- One-variable + negative-control + locality (our L2 item 5 = Agora probe structure: intervention + control + falsification_condition)
- Score ≠ mechanism (our L2 item 3 = Agora TruthGate + SemanticGate distinction between metric signal and mechanism)

### SKIP (specific to vision/NeRF domain or over-engineered for our use):

- GPU T0/T1/T2 eval cascade (vision benchmark specific)
- Heartbeat/watchdog/zombie infrastructure (we use simpler worktree-based isolation via Arbor)
- Full append-only ledger with SQLite + JSONL dual-write (our RUNLOG.md + Arbor idea tree is simpler and sufficient)
- ACP worker session management (we use Anthropic-native Agent tool for subagents)
- Paper corpus pipeline (already running; independent track)

---

## 7. Top-3 Highest-Value Takeaways

### T1: Operator Rewrite Vocabulary as Research Grammar

The 14 `operator_rewrite` values and 10 `paper_move_template` values are a **closed-set research grammar** — a finite vocabulary for labeling "what kind of intervention is this hypothesis proposing?" For our gradient-field direction:
- `explicit_to_latent` = discrete tokens → continuous embedding space (our core thesis)
- `scalar_to_field` = scalar loss → gradient/velocity field target (MeanFlow/JiT/pMF)
- `Reasoning-as-Dynamics` = map reasoning as a dynamical system in embedding space

**Action**: Adopt these as annotation fields in our Hypothesis artifacts. When writing a new hypothesis, require an `operator_rewrite` tag from the closed set. This prevents drift into vague "we improve the loss" language.

### T2: Evidence Debt — Making Absence Visible

The `evidence_debt` field in PaperCard v2 and retrieval packs is a **discipline rule**: if only supporting evidence exists for a hypothesis and contradicting evidence is absent, mark `contradiction_missing=true` rather than treating absence as confidence. Pair this with the PaperCard's `probe_templates` bucket — what ablation would test this mechanism — so the hypothesis lands in experiment design with a built-in negative-control requirement.

**Action**: When routing a hypothesis to GPT-5.5 Pro for novelty/design audit, include a structured `evidence_debt` report. If `contradiction_missing=true`, require the design to include an explicit negative-control experiment before promotion.

### T3: L-14 + L-13 Operational Rules for Our Loop

Two LESSONS have direct and immediate application:
- **L-14 (3-move plateau rule)**: if 3 consecutive experiment iterations change only hyperparameters and show no metric gain, the Arbor loop must auto-trigger an `operator_rewrite` pivot event (not just note "no gain" in RUNLOG). This prevents the `refine_epochs=120→150→180` trap.
- **L-13 (state_hash anti-loop)**: every time the loop considers re-running an audit or gate check, compute `state_hash(current_artifacts)`. If it matches the previous audit's state_hash, the verdict is cached — do not waste a Opus/GPT call re-analyzing unchanged evidence.

**Action**: Add both rules explicitly to our Arbor loop discipline in `plan/operating-manual.md` §5 (Operational Lessons). L-14 becomes: "3 HP-only iterations → mandatory `operator_rewrite` from closed set before dispatch". L-13 becomes: "audit call requires state_diff from last audit; no diff = no call".

---

*Sources: `/home/lingxufeng/agent/agora/CLAUDE.md`, `/home/lingxufeng/agent/agora/Extension.md`, `/home/lingxufeng/agent/agora/scripts/extract_phase1_prompt_v5.txt`, `/home/lingxufeng/research/AgoraArchive/ARCHITECTURE.md`, `/home/lingxufeng/research/AgoraArchive/AGENT_PROTOCOL.md`, `/home/lingxufeng/research/AgoraArchive/LESSONS.md`, `/home/lingxufeng/research/AgoraArchive/ROBUSTNESS_GATES.md`, `/home/lingxufeng/research/AgoraArchive/LEDGER_SCHEMA.md`, `/home/lingxufeng/research/AgoraArchive/schemas/`, `/home/lingxufeng/agent/agora-contract/README.md`, `/home/lingxufeng/agent/agora-contract/docs/assembly_design_2026-05-15.md`, `/home/lingxufeng/agent/agora-contract/docs/model_allocation_2026-05-15.md`, `/home/lingxufeng/agent/agora-contract/docs/LESSONS_inherited.md`, `/home/lingxufeng/agent/agora-contract/findings.md`*
