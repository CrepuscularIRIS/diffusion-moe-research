# AiScientist Methodology Extraction

**Source repo**: `/home/lingxufeng/research/AiScientist`
**Date extracted**: 2026-06-29
**Extractor**: Claude (Sonnet 4.6), run from huggingface/plan/extraction/

---

## 1. What It Is

AiScientist is an artifact-mediated virtual research lab for long-horizon ML research engineering, published 2026-04-17 (arXiv 2604.13018). It runs two autonomous tracks — `paper` (given a paper PDF/MD, reproduce it end-to-end) and `mle` (given a Kaggle-style competition, maximize the metric over repeated cycles) — both using a shared control architecture called **File-as-Bus**: workspace files on disk are the system of record, not conversation state. The orchestrator stays "thin" (stage-level directives, compact workspace map) while specialists stay "thick" (read full artifact files on demand). It runs host-side Python + Docker-sandboxed code execution, with SQLite for job state and a TUI dashboard. Benchmarked on PaperBench (33.73 with GLM-5, +11.15 over baseline) and MLE-Bench Lite (81.82 Any Medal on both Gemini-3-Flash and GLM-5).

---

## 2. Core Methodology / Workflow Spine

### 2.1 Two-Layer Architecture: "Thin Control / Thick State"

The orchestrator only sends stage-level directives and compact summaries. Subagents pull thick state by reading task-relevant workspace files themselves. This prevents context bloat at the top and reduces hallucination from stale in-context state.

```
CLI (aisci_app/cli.py)
  → JobService creates JobRecord in SQLite store
  → JobService.spawn_worker forks worker process
    → JobRunner → Adapter stages inputs into jobs/<job_id>/workspace/
    → Adapter resolves LLM profile from config/llm_profiles.yaml
    → Adapter starts Docker sandbox session
    → EmbeddedEngine runs the main agent loop:
        LLM chat → tool dispatch → subagent delegation → message management
    → Adapter collects artifacts, runs validation
    → JobRunner records artifacts/events in SQLite, exports bundle
```

### 2.2 File-as-Bus Coordination Protocol

All inter-agent state lives in workspace files, NOT in message handoffs. This makes every run inspectable, resumable, and auditable after the fact.

**Paper track workspace map:**
```
workspace/
  paper/ or data/                  # input
  code/                            # mle only
  submission/
    submission.csv
    submission_registry.jsonl      # champion decisions
    candidates/                    # candidate snapshots
  agent/
    paper_analysis/                # per-subagent analysis md files
    prioritized_tasks.md           # P0-P3 task list
    plan.md
    impl_log.md
    exp_log.md
    final_self_check.{md,json}     # paper track only
```

The key principle: every agent reads from the bus before acting and writes results back to the bus after acting. An "orphan" file not traceable to a real LLM invocation is a forgery signal (adopted from V19's Problem.md anti-forgery audit but independently arrived at in AiScientist).

### 2.3 Agent-as-Tool Hierarchy

Subagents are invoked as tools by the orchestrator. Each gets its own LLM conversation, tool set, time budget, and step budget (defined in `config/paper_subagents.yaml`):

- `implementation`: max_steps=500, time_limit=28800s (8h)
- `experiment`: max_steps=500, time_limit=36000s (10h)
- `explore`, `plan`, `general`: lighter budgets
- `paper_structure`, `paper_reader`, `paper_synthesis`, `prioritization`: 36000s each

The orchestrator NEVER does heavy work itself; it dispatches and integrates outputs.

### 2.4 Implement → Experiment Loop (the core iterative cycle)

```
implement(mode="full")
  → clean_reproduce_validation()   [catches env bugs early]
  → run_experiment()
  → [if fail] implement(mode="fix", context="<diagnosis>")
  → run_experiment()
  → ...
  → clean_reproduce_validation()   [final gate]
  → submit()
```

Rules enforced by the prompt:
1. After an experiment fails, NEXT action MUST be `implement(mode="fix")` — never re-run the same experiment.
2. Never run more than 2 consecutive experiments without an `implement()` in between.
3. Each cycle must address a specific, different issue.

### 2.5 Paper Track Specific Loop: Read → Prioritize → Implement → Experiment → Self-Check

```
read_paper()      [4 parallel subagents: Structure, Algorithm, Experiments, Baseline]
  → prioritize_tasks()
  → implement(mode="full")
  → clean_reproduce_validation()
  → run_experiment()  [compare against target values from paper]
  → [fix cycles]
  → final_self_check
```

### 2.6 MLE Track: Analyze → Prioritize → Baseline-First → Iterate

```
analyze_data()
  → prioritize_tasks()
  → implement(mode="full")  [baseline that generates valid submission.csv first]
  → run_experiment()        [validate submission format]
  → implement(mode="explore"|"refine"|"ensemble")  [improve]
  → run_experiment()
  → ...
  → compare candidates via submission_registry.jsonl
  → submit()
```

---

## 3. Experiment Standards / Gates / Falsifier Discipline

### 3.1 The Primacy-of-Artifact Rule

From `src/aisci_domain_paper/prompts/templates.py`, render_main_agent_system_prompt:

> "THE #1 RULE: reproduce.sh First. Without it, ALL Code Execution and Result Analysis rubric items automatically score 0."

The equivalent in MLE:

> "THE #1 RULE: submission.csv First. Without it, your competition score is automatically zero."

**Translation to our context**: Every experiment run must produce a durable artifact (file on disk) that is the primary evidence. An experiment that only produces in-context output is not trusted.

### 3.2 Hyperparameter Fidelity vs Time-Budget Trade-off (explicit scale rule)

From the paper track main agent prompt:

```
1. Default to paper's hyperparameters in code: LR, optimizer, scheduler, architecture, batch size MUST match paper.
2. Smart scaling for time management in reproduce.sh:
   - If total time for all experiments > 16h: scale epochs proportionally so everything fits in ~20h
   - If single experiment > 8h: reduce epochs for THAT experiment only
   - NEVER reduce to < 10% of paper's epochs
   - Prefer reducing seeds (use 1 seed) over reducing epochs
   - Prefer reducing dataset size slightly over slashing epochs
3. Result quality threshold: If metrics deviate > ~20% from the paper, investigate. If within ~20%, accept and move on.
4. After 2-3 failed fix attempts, move to the next task.
```

### 3.3 Anti-Reward-Hacking by Design

From paper track MLE system prompt:
- Never use `torch.randn()` or `np.random.rand()` as substitutes for real data (explicit prohibition)
- `clean_reproduce_validation()` tool simulates grading environment (wipes cache, runs from scratch)
- Competition data in `/home/data/` must NEVER be modified

### 3.4 Reproducibility Gate (paper track)

The paper track requires a `final_self_check.{md,json}` and `artifacts/validation_report.json`. The system collects whatever is committed to git at time-out, so "commit early, commit often" is an explicit rule baked into every subagent prompt.

### 3.5 Experiment Coverage Check (built-in completeness gate)

From experiment agent prompt:

```
After running solution:
1. Check task coverage: review prioritized_tasks.md and verify P0/P1 tasks attempted
2. Check for silent failures: verify training printed progress
3. Verify submission.csv completely (shape, columns, NaN, inf)
4. In report, include coverage summary: succeeded / failed / missing
```

### 3.6 Parallel Training Discipline

From MLE implementation agent prompt (a rarely-seen operational pattern):

```
Goal: avoid leaving GPU idle because single small job under-uses VRAM.
How:
- Each job in its own directory: /home/code/runs/exp_001/, exp_002/, ...
- Start long runs in background with nohup → poll with tail/grep
- Single GPU: cap at 2-4 small jobs
- submission.csv: only ONE canonical file; parallel jobs write per-run predictions under runs/
- After winner selected, run single inference → write submission.csv
Risks: OOM, disk exhaustion, zombie processes, shell timeouts
```

### 3.7 Time-Budget Discipline (explicit thresholds)

From MLE main agent:
- > 50% time remains: keep implementing P1/P2
- ~30% time remains: finalize current model, ensure submission valid
- ~15% time remains: only fix critical submission issues, submit

From paper track:
- ~15% time (3.5h of 24h): run `clean_reproduce_validation()` once, fix critical issues

---

## 4. Reusable Artifacts — Prompts, Templates, Rubrics

### 4.1 Paper Structure Extractor System Prompt (verbatim key rubric)

**File**: `src/aisci_domain_paper/prompts/templates.py:STRUCTURE_SYSTEM_PROMPT`

This is a high-quality prompt for decomposing any paper into: metadata, section index with exact line numbers, abstract verbatim, core contributions, constraint extraction, and agent task assignment. Critical snippet:

```
### Gist
Each section's Gist should describe **what the section contributes to reproduction** (not just its topic).
  - Good: "Defines loss function and update rule"
  - Bad: "Method description"
```

Section output schema:
```markdown
| # | Section Name | Gist (reproduction value) | Start Line | Line Count |
```

### 4.2 Algorithm Extractor System Prompt

**File**: `src/aisci_domain_paper/prompts/templates.py:ALGORITHM_SYSTEM_PROMPT`

Key discipline: "Nothing implicit" — if the paper says "we use Adam" without specifying β values, note "Adam (default params assumed — β1=0.9, β2=0.999 not explicitly stated)". Every hyperparameter must cite a line number. "When in doubt, extract it."

### 4.3 Experiments Extractor System Prompt

**File**: `src/aisci_domain_paper/prompts/templates.py:EXPERIMENTS_SYSTEM_PROMPT`

Key schema for experiment inventory:
```
| ID | Name | Section | Lines | Type | Priority | Datasets |
| Table 1 | Main results | 4.1 | 340-355 | Main result | P0 | Dataset-A, Dataset-B |
```

Type classification: Main result / Baseline comparison / Ablation / Analysis-Visualization.

Critical rule: "Copy target numbers verbatim — Expected Results should mirror the paper's tables exactly. These numbers are what the Experiment Agent will compare against."

### 4.4 Baseline Extractor System Prompt

**File**: `src/aisci_domain_paper/prompts/templates.py:BASELINE_SYSTEM_PROMPT`

Key insight that is DIRECTLY applicable to our work: **each model variant is a separate graded item**.

```
### Model Variants
Many papers evaluate their method across multiple model architectures or sizes.
Each model variant is a SEPARATE grading item — they are NOT optional configurations.
If Table 1 shows results for 3 model sizes, that's 3 independently scored rows.
```

Implementation Category taxonomy:
- Library Available → Low effort
- Repo Available → Medium effort
- Custom Required → High effort
- Blocked → Cannot use

### 4.5 Synthesis Agent System Prompt

**File**: `src/aisci_domain_paper/prompts/templates.py:SYNTHESIS_SYSTEM_PROMPT`

The synthesis agent creates an "Executive Summary" that is the FIRST thing the main orchestrator reads. Key schema:

```markdown
## Quick Reference
### Section Navigator
| Section | Gist | Lines | Read For |
## Key Takeaways
### Algorithms to Implement
### Experiments to Run
| Experiment | Type | Datasets | Seeds | Key Config | Target Values |
### Reproducibility Checklist
- [ ] Random seeds: ...
- [ ] Hardware: ...
- [ ] Expected training time: ...
## Suggested Implementation Order
## Gaps & Warnings
```

### 4.6 Prioritization Framework (P0-P3 with Elevation Rules)

**File**: `src/aisci_domain_paper/prompts/templates.py:render_prioritization_system_prompt`

Elevation rules (verbatim):
```
Elevate to P0 if:
- Rubric weight is significantly above average
- Task is core algorithm implementation
- Task mentions "core" or "main" contribution
- Required for other high-weight tasks
- Task is a baseline or model variant that appears in a main-text table
  (baselines in main tables are graded with equal weight to proposed method)

Keep at P1 if:
- Rubric weight is around or above average
- [baselines appearing ONLY in appendix]

P2 — Ablation studies, sensitivity analyses, additional datasets
P3 — Appendix-only experiments, edge cases briefly mentioned
```

### 4.7 MLE Main Agent Orchestration Principles (verbatim key section)

**File**: `src/aisci_domain_mle/prompts/templates.py:MAIN_AGENT_SYSTEM_PROMPT`

```
Design Principles:
1. No rigid workflow — agent decides its own strategy
2. Accurate tool documentation — matches actual available tools
3. Decision heuristics — not step-by-step SOPs
4. Concise critical constraints — no redundant repetition
5. Time budgets and gates come from task prompt, periodic reminders, tools
```

### 4.8 MLE System Prompt (core identity)

**File**: `src/aisci_domain_mle/assets/mle_system_prompt.md`

```
You are the mle-mode lead agent for AI Scientist Workbench.
Primary goal: Turn a task workspace plus evaluation contract into a valid submission and tracked candidate set.
Non-negotiable rules:
- Always preserve a valid `submission.csv`.
- Track candidate snapshots and champion decisions through `submission_registry.jsonl`.
- Keep generated code in the code workspace and validation artifacts in the agent workspace.
- Treat sample submission shape and evaluation protocol as first-class constraints.
```

### 4.9 Context Summarization (ReSUM-style for long runs)

**File**: `src/aisci_domain_mle/prompts/templates.py:SUMMARY_FIRST_TIME_PROMPT` and `SUMMARY_INCREMENTAL_PROMPT`

```
Produce a concise summary that preserves:
- Key decisions and conclusions
- Important file paths, metrics, and outcomes
- What has been tried and what remains to do

Output your summary under the heading "Essential Information:" (nothing else).
```

Incremental variant merges previous summary with new segment, producing a single updated summary. This is a production-grade context compression protocol for multi-hour autonomous runs.

### 4.10 File-as-Bus vs No-Bus Toggle

**File**: `src/aisci_domain_mle/prompts/templates.py` lines 710-822

AiScientist has a `file_as_bus: bool` flag that produces two variants of each subagent prompt — one with shared log files (`impl_log.md`, `exp_log.md`) as shared memory, one without. This demonstrates that File-as-Bus coordination is configurable, not baked in. The no-bus variant passes state through the orchestrator's message context instead.

---

## 5. Command / Skill Candidates

| Name | 1-line purpose | Trigger | Recommended engine |
|------|---------------|---------|-------------------|
| `/paper-structure-extract` | Decompose a paper into line-numbered section index + constraint map | Have a paper.md or paper PDF that needs systematic analysis before implementation | Opus (reading quality critical) |
| `/experiment-inventory` | Extract all experiments from a paper as typed, prioritized table with target values | Before any reproduction run; or to build ablation plan | Opus |
| `/baseline-scan` | Classify every comparison method by implementation effort + blocked status | After paper read; before implementation | Opus/GPT-5.5-Pro |
| `/reproduce-sh-skeleton` | Generate a compliant `reproduce.sh` skeleton that survives `git clean -fd` | Immediately after first implementation round | Codex |
| `/implement-experiment-loop` | Enforce the implement→experiment cycle with anti-backslide rules | Any multi-round experiment campaign | Codex (diagnose) + Opus (plan) |
| `/candidate-registry` | Snapshot current best submission/result to a dated candidate registry (`submission_registry.jsonl` schema) | After any experiment that produces metrics | Codex |
| `/clean-validation-gate` | Run reproduce.sh / validation script from scratch in a clean env, catch cached-state bugs | Before declaring a run complete; after major implementation rounds | Opus subagent |
| `/workspace-map` | Generate a compact, line-number-linked workspace map for session bootstrap | At session start for any long-running research task | Opus/Sonnet |
| `/time-budget-allocator` | Given experiment count + GPU hours, output per-experiment epoch reduction plan | Before running reproduce.sh if total estimated time > 16h | Codex |
| `/execution-order-dag` | Build a dependency DAG from prioritized_tasks.md and output a serialized execution order | After prioritization, before implementation | Codex |

---

## 6. NEW vs Our Kernel

### 6.1 ADOPT — Genuinely New

**A. File-as-Bus as a first-class coordination protocol (not just a logging convention)**

Our kernel uses `RUNLOG.md` and the Arbor tree as state, but they are monolithic and session-scoped. AiScientist's insight: split workspace into a TYPED artifact bus where each file type has a contract (`impl_log.md` = implementation record, `exp_log.md` = experiment record, `submission_registry.jsonl` = champion ledger). Multiple agents can read/write the same bus concurrently without conflicting because their write targets are disjoint.

Concrete adaptation: for our diffusion-MoE loop, introduce:
- `workspace/agent/direction_log.md` — ideation trace (currently RUNLOG.md conflates this)
- `workspace/agent/experiment_cards/` — per-experiment typed JSON (currently we mix prose + numbers in RUNLOG)
- `workspace/submission/candidate_registry.jsonl` — champion tracking (currently we re-examine checkpoints manually)

**B. "Thin Control / Thick State" as an explicit orchestrator design rule**

Our Opus coordinator currently re-reads RUNLOG.md wholesale at each cycle to reconstruct context. AiScientist's approach: orchestrator holds only a compact workspace map; subagents pull what they need. This directly solves the RUNLOG drift problem (cycle 1-8 updated RUNLOG, tree stale at nodes 1-4) — the workspace map IS the authoritative summary, the orchestrator doesn't need to reconstruct.

**C. Branched implement modes (`full` / `fix` / `explore` / `refine` / `ensemble`)**

Our current loop runs monolithic "implement + experiment" with no mode differentiation. AiScientist's mode taxonomy maps directly:
- `full` → first dispatch to a fresh direction
- `fix` → post-experiment failure recovery (what we currently do ad hoc)
- `explore` → cheap bounded hypothesis test (matches our Direction A/C/D structure)
- `refine` → tuning a known-good direction
- `ensemble` → combining checkpoints

**D. Context compression protocol (ReSUM-style incremental summarization)**

For runs >4h, our Opus context fills with RUNLOG content and verbose outputs. AiScientist's `SUMMARY_FIRST_TIME_PROMPT` + `SUMMARY_INCREMENTAL_PROMPT` provide a production-grade incremental summarization that can be triggered automatically at context threshold. The "Essential Information:" section header makes parsing deterministic.

**E. Anti-Reward-Hacking gates: `clean_reproduce_validation()` pattern**

Our kernel says "score≠mechanism + SEALED eval/test" but we don't have an operational gate that enforces it. AiScientist's `clean_reproduce_validation()` wipes venv, HF cache, torch cache, then reruns from scratch — mechanically forcing honest evaluation. We should adopt an equivalent: a `sealed_eval_gate` that re-runs with no cached artifacts before claiming any result.

**F. Submission registry / champion ledger schema**

```jsonl
{"candidate_path": "...", "method_summary": "...", "metrics": {...}, "eval_protocol": "..."}
```

We do not track our experiment candidates this way. Each new checkpoint decision currently requires re-reading multiple files. A jsonlines registry directly solves this.

**G. Parallel training job management discipline** (Section 3.6 above)

Our diffusion experiments are sequential. The parallel training protocol (per-job directories, background nohup, GPU VRAM budget, single winner writes the canonical result) is a concrete operational pattern we're missing.

**H. Paper type classification for effort allocation**

The STRUCTURE_SYSTEM_PROMPT classifies papers as: algorithm-focused / empirical / theoretical / systems. This allows the orchestrator to allocate reading and implementation effort by type. For our Track 2 (gradient-field/embedding-flow), this would flag "algorithm-focused" and direct more effort to the method section.

### 6.2 OVERLAPS — Already in Our Kernel

| AiScientist | Our kernel | Assessment |
|-------------|-----------|------------|
| P0-P3 prioritization with explicit elevation rules | L2 science kernels: "failure must shrink search space" + Arbor tree priority | Functionally equivalent; AiScientist's formulation is more operational (P0 = "must-do or score is 0"). Our elevation rules are more research-oriented (novel claim quality). Keep both. |
| Generator/critic/selector isolation | L2 kernel rule 7: "generator/critic/selector ISOLATION" + multi-engine isolation | Full overlap. AiScientist uses subagent-as-tool isolation; we use worktree + engine separation. Different mechanism, same principle. |
| Implement→experiment anti-backslide rules | L1 "falsify-before-build" + L2 "one-variable + negative-control" | Partial overlap. AiScientist's rules are operational (max 2 experiments before fix); ours are epistemological. Combine: adopt their operational gates. |
| Rubric/evaluation is sealed / "commit early, commit often" | L2 "SEALED eval/test set" | Overlap, but AiScientist's `git clean -fd` mechanism is a concrete enforcement we lack. |
| Time-budget discipline with thresholds | Not explicit in our kernel | NEW (flagged above in 6.1). |

### 6.3 SKIP — Not Applicable

- Docker sandbox infrastructure: not relevant for our GPU cluster setup (we use conda envs, not Docker)
- MLE-Bench competition framing: we're doing academic research, not Kaggle
- venv vs conda (paper track always uses venv): our environment uses conda dllm env which is correct for our substrate
- SQLite job store: too heavy for our loop; Arbor tree + RUNLOG.md serve this purpose
- PaperBench benchmark integration: we're using our own evaluation protocol
- `blacklist.txt` per-paper constraint: not applicable to open-ended research ideation

---

## 7. Top-3 Highest-Value Takeaways

### #1: File-as-Bus with Typed Artifact Contracts (adopt now)

The single highest-value pattern. Our RUNLOG drift bug (tree stale, RUNLOG advanced) is a direct symptom of not having typed contracts. AiScientist's workspace map pattern — `impl_log.md` (implementation), `exp_log.md` (experiments), `submission_registry.jsonl` (champions) — solves the problem mechanically because each artifact has ONE writer and ONE purpose. Immediate action: introduce typed workspace artifacts in our next Arbor cycle.

### #2: Sealed Clean-Environment Gate Before Claiming Any Result

AiScientist's `clean_reproduce_validation()` is an operational enforcement of L2 science kernel "score≠mechanism + SEALED eval/test." We say it in principle but don't enforce it mechanically. For our frozen dLLM experiments, the equivalent is: before recording any metric as a valid result, re-run the evaluation script in a fresh subprocess with no cached model outputs, and verify the metric matches the live generation (not a stale cache). This directly guards against the generation/verifier metric confusion we hit with diffusion loss as a quality proxy (lesson #2 in our operating-manual).

### #3: Context Compression Protocol (incremental ReSUM)

For our Track 2 gradient-field runs (which are expected to run >24h), Opus context fills and degrades. AiScientist's incremental summarization (`SUMMARY_INCREMENTAL_PROMPT`) — merge previous summary + new segment → output "Essential Information:" — is a production pattern for maintaining coherence across long autonomous runs. We should wire this into our goal-mode loop: trigger summarization when context reaches 80% (matching our L2 "compactor" design from V19 §14.2, but AiScientist provides the actual prompt templates).

---

*End of extraction. Files cited: `src/aisci_domain_paper/prompts/templates.py`, `src/aisci_domain_mle/prompts/templates.py`, `src/aisci_domain_mle/assets/mle_system_prompt.md`, `config/paper_subagents.yaml`, `README.md`, `CLAUDE.md`.*
