# Extraction: Autonomous AI-Research Frameworks
**Date:** 2026-06-29
**Source repos:** AgentLaboratory · AI-Researcher · ai-scientist-v2
**Purpose:** Harvest workflow patterns for our frozen/adapter DiffusionGemma research loop

---

## 1. What Each Framework Is

**AgentLaboratory** (`SamuelSchmidgall/AgentLaboratory`)
A human-in-the-loop multi-agent research assistant. Runs a sequential pipeline — Literature Review → Plan Formulation → Data Prep → Running Experiments → Results Interpretation → Report Writing → Report Refinement — using a cast of named role agents (PhD Student, Postdoc, Professor, ML Engineer, SW Engineer, Reviewers) that collaborate through fenced-command dialogue. Notable extension: **AgentRxiv**, where agents upload completed papers to a shared archive and retrieve prior agent-generated work as literature before generating their own. Designed for modest-compute academic ML tasks. Compute tolerance is controlled by an explicit `max_steps` budget per phase.

**AI-Researcher** (`HKUDS/AI-Researcher`)
A two-entry-level system for autonomous scientific innovation, accepted as a NeurIPS 2025 Spotlight paper. Entry Level 1: user gives a detailed idea spec + reference papers → system implements and validates. Entry Level 2: user gives only reference papers → system generates the idea and then implements. Runs three phases: Literature Review + Idea Generation → Algorithm Design/Implementation/Validation/Refinement → Paper Writing. Key innovation is its **innovation graph construction** pipeline (5-step citation-influence analysis) and a structured benchmark (Inno-Bench, 4 domains, 5 ML categories) that uses expert-written papers as ground truth and evaluates on Novelty, Experimental Comprehensiveness, Theoretical Foundation, Result Analysis, Writing Quality.

**ai-scientist-v2** (`SakanaAI/AI-Scientist-v2`)
A fully autonomous, template-free scientific discovery system. First produced a workshop paper accepted through peer review. Runs a best-first tree search (BFTS) over experiment implementations, guided by an AgentManager that stages experiments in 4 progressive phases: basic implementation → hyperparameter tuning → creative research → ablation studies. Each phase (stage) has pre-declared goals and structured completion/progression gates. Uses a mixed-model strategy (Claude 3.5 Sonnet for coding at temp=1.0, GPT-4o for feedback/VLM analysis, o1/o3-mini for review/writeup). Notable: v2 removes reliance on human-authored templates (unlike v1), generalizes across ML domains, and generates experimental plots reviewed by a VLM.

---

## 2. Core Methodology / Workflow Spine

### Common to All Three
- **Linear macro-pipeline:** literature survey → idea/plan → implement → validate → write. All three share this skeleton.
- **Iterative refinement within each phase:** reflection loops (v2: `--num-reflections`; AgentLab: dialogue turns up to `max_steps`; AI-Researcher: Design→Implementation→Validation→Refinement sub-loop).
- **Automated paper writing:** all three generate LaTeX/PDF manuscripts as a terminal artifact.
- **Multi-model or multi-agent separation:** different roles or models assigned to coding vs. review vs. writing.
- **Checkpointing:** all save state to resume from failures.

### Per-Framework Differences

| Dimension | AgentLaboratory | AI-Researcher | ai-scientist-v2 |
|-----------|----------------|---------------|----------------|
| Loop structure | Phase-sequential + second round | Design→Impl→Validate→Refine within phase 2 | Best-first tree search, 4 main stages |
| Idea source | User provides topic; agents plan | Level 1: user idea; Level 2: agents generate from papers | LLM generates + Semantic Scholar novelty check |
| Isolation | Per-phase `max_steps` budget | Docker container per run | Parallel workers on separate process |
| Selection | Not explicit (submit when ready) | Not explicit (iteration-based) | `select_best_implementation` function spec |
| Review | 3-reviewer weighted ensemble | Evaluator agent on 5 dimensions | NeurIPS rubric + VLM plot review |
| Novelty check | Not systematic | Innovation graph (citation influence) | Semantic Scholar search before FinalizeIdea |
| Staging | 7 named sub-phases | 4 conceptual sub-phases | 4 explicit numbered stages with goals |

### ai-scientist-v2 Stage Structure (most structured of the three)
```
Stage 1: initial_implementation
  Goals: basic working impl, simple dataset, functional correctness
Stage 2: baseline_tuning
  Goals: hyperparameter search (lr, epochs, bs), NO architecture change,
         TWO new HuggingFace datasets introduced
Stage 3: creative_research
  Goals: novel improvements, new insights, THREE HuggingFace datasets total
Stage 4: ablation_studies
  Goals: systematic component analysis, same datasets as Stage 3
```
Stage transition is gated by `stage_progress_eval_spec` (ready_for_next_stage / reasoning / recommendations / suggested_focus). Stage completion gated by `stage_completion_eval_spec` (is_complete / reasoning / missing_criteria).

---

## 3. Experiment Standards / Specs

### AgentLaboratory — Phase Notes System
Each task phase accepts phase-specific notes injected at inference time:
```yaml
# file: experiment_configs/MATH_agentlab.yaml (representative structure)
task-notes:
  plan-formulation:
    - 'You should come up with a plan for only ONE experiment...'
    - 'Please use gpt-4o-mini for your experiments'
    - 'You must evaluate on the entire 500 test questions of MATH'
  data-preparation:
    - 'Please use gpt-4o-mini for your experiments'
    - '...Here is a sample code you can use to load MATH...'
```
Notes are filtered per phase at inference time. The `max_steps` budget triggers an urgency signal at 70%:
```python
# file: agents.py line 254
if step/(self.max_steps-1) > 0.7:
    complete_str = "You must finish this task and submit as soon as possible!"
```
History is pruned with optional expiration dates on individual turns (for rolling context).

### ai-scientist-v2 — Structured Metric Schema
All metric output is parsed into a normalized schema (prevents "train/val" ambiguity):
```python
# file: ai_scientist/treesearch/parallel_agent.py (metric_parse_spec)
{
  "valid_metrics_received": bool,
  "metric_names": [
    {
      "metric_name": "train accuracy",       # PRECISE, no vague labels
      "lower_is_better": bool,
      "description": "...",
      "data": [
        {
          "dataset_name": "CIFAR-10",        # NEVER 'train'/'val'/'test'
          "final_value": float,
          "best_value": float
        }
      ]
    }
  ]
}
```
Node-level bug detection is explicit (is_buggy: always True if exc_type not None OR no valid metric). VLM feedback on plots is structured:
```python
# file: parallel_agent.py (vlm_feedback_spec)
{
  "plot_analyses": [{"analysis": "..."}],
  "valid_plots_received": bool,
  "vlm_feedback_summary": "..."
}
```

### ai-scientist-v2 — Tree Search Config (bfts_config.yaml)
Key experiment discipline parameters:
```yaml
agent:
  num_workers: 4
  stages:
    stage1_max_iters: 20
    stage2_max_iters: 12
    stage3_max_iters: 12
    stage4_max_iters: 18
  code:
    model: anthropic.claude-3-5-sonnet-20241022-v2:0
    temp: 1.0
    max_tokens: 12000
  feedback:
    model: gpt-4o-2024-11-20
    temp: 0.5
  search:
    max_debug_depth: 3      # max retries on a failing node
    debug_prob: 0.5         # probability of retrying vs. abandoning
    num_drafts: 3           # initial root nodes per tree
```

### AI-Researcher — Innovation Graph (5-step citation analysis)
Evaluation pipeline for literature influence:
```
Step 1 (file: create_innovation_graph_instruction_step1.md):
  Citation frequency map — count, sections, context quotes → JSON

Step 2 (file: create_innovation_graph_instruction_step2.md):
  Context analysis — influence indicators ("based on", "extends"), depth (detailed/moderate/brief), is_method → JSON

Step 3 (file: create_innovation_graph_instruction_step3.md):
  Evidence collection — borrowed concepts, modifications, type (foundation/component/inspiration) → JSON

Step 4 (file: create_innovation_graph_instruction_step4.md):
  Impact scoring — frequency 30% + location 25% + depth 25% + influence 20% → ranked JSON

Step 5 (file: create_innovation_graph_instruction_step5.md):
  Overall ranking + graph construction
```

### AI-Researcher — Benchmark Evaluation Dimensions
```
Novelty: innovation and uniqueness
Experimental Comprehensiveness: design, execution, rigor
Theoretical Foundation: strength of theoretical background
Result Analysis: depth and accuracy of interpretation
Writing Quality: clarity, coherence, structure
```
Two task difficulty levels: Task 1 (full technical spec provided), Task 2 (motivation/goals only, solution hidden).

### ReviewersAgent (AgentLab + v2 — shared rubric)
Both use the NeurIPS review form. Three reviewers with biased personas (not identical to each other):
```python
# file: agents.py lines 192-200 (AgentLaboratory)
reviewer_1 = "You are a harsh but fair reviewer and expect good experiments that lead to insights."
reviewer_2 = "You are a harsh and critical but fair reviewer who is looking for an idea that would be impactful in the field."
reviewer_3 = "You are a harsh but fair open-minded reviewer that is looking for novel ideas that have not been proposed before."

# file: perform_llm_review.py lines 17-24 (v2)
reviewer_system_prompt_neg = base + "If a paper is bad or you are unsure, give it bad scores and reject it."
reviewer_system_prompt_pos = base + "If a paper is good or you are unsure, give it good scores and accept it."
```
Scoring JSON fields (shared between both):
```json
{
  "Summary": "...", "Strengths": [...], "Weaknesses": [...],
  "Originality": 1-4, "Quality": 1-4, "Clarity": 1-4, "Significance": 1-4,
  "Questions": [...], "Limitations": [...], "Ethical Concerns": bool,
  "Soundness": 1-4, "Presentation": 1-4, "Contribution": 1-4,
  "Overall": 1-10, "Confidence": 1-5, "Decision": "Accept|Reject"
}
```
AgentLab weighted aggregate formula:
```python
# file: agents.py lines 161-176
performance = (
  soundness_weight*soundness + presentation_weight*presentation +
  confidence_weight*confidence + contribution_weight*contribution +
  overall_weight*overall + originality_weight*originality +
  significance*significance_weight + clarity_weight*clarity + quality_weight*quality
) / max_score * 10
# weights: overall=1.0, contribution=0.4, presentation=0.2, others=0.1
```

---

## 4. Reusable Artifacts — Quoted Prompts / Templates / Rubrics

### A. Idea Finalization Schema (ai-scientist-v2)
**file:** `ai_scientist/perform_ideation_temp_free.py` lines 27-38
```python
{
  "Name": "short_descriptor_lowercase_underscores",
  "Title": "catchy and informative title",
  "Short Hypothesis": "Concise statement. Clarify the need for this specific direction, ensure this is the best setting to investigate this idea, and there are not obvious other simpler ways to answer the question.",
  "Related Work": "Brief discussion of most relevant related work and how proposal clearly distinguishes from it, and is not a trivial extension.",
  "Abstract": "~250 words in conference format",
  "Experiments": "List of experiments. Ensure these are simple and feasible. Be specific in exactly how you would test the hypothesis, and detail precise algorithmic changes. Include evaluation metrics.",
  "Risk Factors and Limitations": "List of potential risks and limitations"
}
```

### B. Ideation System Prompt (ai-scientist-v2)
**file:** `ai_scientist/perform_ideation_temp_free.py` lines 61-96
```
"You are an experienced AI researcher who aims to propose high-impact research ideas resembling
exciting grant proposals. Feel free to propose any novel ideas or experiments; make sure they
are novel. Be very creative and think out of the box. Each proposal should stem from a simple
and elegant question, observation, or hypothesis about the topic. For example, they could
involve very interesting and simple interventions or investigations that explore new
possibilities or challenge existing assumptions. Clearly clarify how the proposal distinguishes
from the existing literature.

Ensure that the proposal does not require resources beyond what an academic lab could afford.
These proposals should lead to papers that are publishable at top ML conferences.

[...tool descriptions...]

Note: You should perform at least one literature search before finalizing your idea to ensure
it is well-informed by existing research."
```

### C. Idea Reflection Prompt (ai-scientist-v2)
**file:** `ai_scientist/perform_ideation_temp_free.py` lines 111-125
```
"Round {current_round}/{num_reflections}.

In your thoughts, first carefully consider the quality, novelty, and feasibility of the
proposal you just created. Include any other factors that you think are important in
evaluating the proposal. Ensure the proposal is clear and concise, and the JSON is in
the correct format. Do not make things overly complicated. In the next attempt, try to
refine and improve your proposal. Stick to the spirit of the original idea unless there
are glaring issues.

If you have new information from tools, such as literature search results, incorporate
them into your reflection and refine your proposal accordingly."
```

### D. Stage Goals (ai-scientist-v2) — Directly Liftable Stage Specs
**file:** `ai_scientist/treesearch/agent_manager.py` lines 150-167
```python
stage1_goals = """
  - Focus on getting basic working implementation
  - Use a simple dataset
  - Aim for basic functional correctness
  - If you are given "Code To Use", you can directly use it as a starting point."""

stage2_goals = """
  - Change hyperparameters such as learning rate, number of epochs, batch size to improve
  - DO NOT change the model architecture from the previous stage
  - Introduce TWO more new datasets from HuggingFace to test the model."""

stage3_goals = """
  - Explore novel improvements
  - Come up with experiments to reveal new insights
  - Be creative and think outside the box
  - MAKE SURE you use THREE HuggingFace datasets in total to test your models"""

stage4_goals = """
  - Conduct systematic component analysis that reveals the contribution of each part
  - Use the same datasets you used from the previous stage"""
```

### E. Stage Progression Gate (ai-scientist-v2)
**file:** `ai_scientist/treesearch/agent_manager.py` lines 49-75
```python
stage_progress_eval_spec = FunctionSpec(
  name="evaluate_stage_progression",
  # required fields:
  # ready_for_next_stage: bool
  # reasoning: str  -- detailed reasoning for progression decision
  # recommendations: list[str]  -- specific recommendations
  # suggested_focus: str  -- key areas for next stage
)

stage_completion_eval_spec = FunctionSpec(
  name="evaluate_stage_completion",
  # required fields:
  # is_complete: bool
  # reasoning: str
  # missing_criteria: list[str]  -- what's still needed
)
```

### F. Task 1 Instruction Template (AI-Researcher)
**file:** `benchmark_collection/prompts/create_innovation_task_instruction_task1.md`
```
"Analyze the given research paper and write a detailed technical instruction paragraph for
researchers to implement its core methodology without reading the full paper. Your instruction
must include:

1. What task does the model work on
2. Core techniques/algorithms used in the paper
3. Purpose and function of each major technical component
4. Implementation details for each component:
   - Key parameters and configurations
   - Input/output specifications
   - Important constraints or requirements
5. Step-by-step description of how these components interact and combine
6. Critical implementation details that affect performance

Focus only on the technical methodology and implementation aspects. Exclude background,
literature review, and experimental results. Write in a clear, sequential format that a
technical researcher could follow to reproduce the core method.

Don't mention the specific names of the proposed model, or exact module names that are
special to this paper."
```

### G. Innovation Graph Step 4 Impact Scoring
**file:** `benchmark_collection/prompts/create_innovation_graph_instruction_step4.md`
```
Score each reference based on:
- Citation frequency (30%)
- Location importance (25%)
- Discussion depth (25%)
- Direct influence (20%)

Output: { "scores": [{ "reference": "...", "total": N, "breakdown": { ... } }] }
```

### H. Postdoc Plan Formulation Prompt (AgentLaboratory)
**file:** `agents.py` lines 424-435
```
"You are directing a PhD student to help them come up with a good plan, and you interact
with them through dialogue.

Your goal is to produce plans that would make good experiments for the given topic. You
should aim for a very simple experiment that showcases your plan, not a complex one. You
should integrate the provided literature review and come up with plans on how to expand
and build on these works for the given topic. Your plans should provide a clear outline
for how to achieve the task, including what machine learning models to use and implement,
what types of datasets should be searched for and used to train the model, and the exact
details of the experiment. Your idea should be very innovative and unlike anything seen
before."
```

### I. Review Format (THOUGHT + JSON)
**file:** `agents.py` / `perform_llm_review.py` (both use identical structure)
```
THOUGHT:
<brief, specific intuitions for this paper — not generic>

REVIEW JSON:
```json
{ "Summary": ..., "Strengths": [...], "Weaknesses": [...],
  "Originality": 1-4, "Quality": 1-4, "Clarity": 1-4, "Significance": 1-4,
  "Soundness": 1-4, "Presentation": 1-4, "Contribution": 1-4,
  "Overall": 1-10, "Confidence": 1-5, "Decision": "Accept|Reject" }
```
```

---

## 5. Command / Skill Candidates

| Name | 1-line purpose | Trigger | Engine |
|------|---------------|---------|--------|
| `/stage-protocol` | Progress an experiment through the 4-stage sequence (impl→tune→creative→ablation) with pre-declared goals and formal completion gates | Before `/dispatch` worktree agent | Opus as coordinator; Codex for stage-gate evaluation |
| `/ideate-schema` | Generate a structured idea in the FinalizeIdea schema (Name/Title/Short Hypothesis/Related Work/Abstract/Experiments/Risk Factors) with at least one lit-search before finalizing | IDEATE phase of goal loop | Opus drafts; GPT-5.5 Pro for novelty check; Codex selects |
| `/lit-influence` | Run the 5-step citation-influence pipeline on a target paper to map prior art dependency graph (foundation/component/inspiration typology) | Before IDEATE when given reference papers | Opus |
| `/ensemble-review` | 3-persona reviewer ensemble (experiments-rigor, impact, novelty) using NeurIPS rubric; weighted aggregate score | DECIDE gate, before merge/prune | Codex + GPT-5.5 Pro (independent instances) |
| `/metric-schema` | Emit structured metric output (precise metric_name, lower_is_better, dataset_name, final/best value) from experiment output; flag is_buggy if no valid metric | After experiment run in worktree | Opus |
| `/idea-reflect` | N-round reflection on a generated idea: quality / novelty / feasibility / simplicity; refine without losing spirit unless glaring flaw | After initial IDEATE | Opus |

---

## 6. NEW vs Our Kernel

### ADOPT — Genuinely Novel

**1. 4-stage progressive experiment design (ai-scientist-v2)**
Our kernel has falsify-before-build and one-variable + negative-control + locality, but no concrete staging sequence. The v2 pattern — Stage 1 basic → Stage 2 hyperparameter tuning (architecture FROZEN) → Stage 3 creative research → Stage 4 ablation — gives a disciplined scaffolding that forces us to not jump to creative variants before the baseline is solid. The "DO NOT change the model architecture from Stage 2" rule is a direct operationalization of one-variable discipline. ADOPT as `/stage-protocol`.

**2. Structured completion/progression gates (ai-scientist-v2)**
`stage_completion_eval_spec` forces an explicit `missing_criteria` list before advancing; `stage_progress_eval_spec` forces `ready_for_next_stage + reasoning + recommendations + suggested_focus`. We have goal re-anchoring but no formal stage completion gate that produces a structured `missing_criteria` list. ADOPT into the Arbor tree's 验收 step.

**3. Idea schema with explicit Risk Factors and "not a trivial extension" test (ai-scientist-v2)**
Our 5-field MechanismHypothesis has (hypothesis / mechanism / prediction / control / kill-condition). v2 adds: (a) `Short Hypothesis` must state "not obvious other simpler ways to answer the question" — this operationalizes our falsifiability-first rule at the idea stage; (b) `Risk Factors and Limitations` as a first-class field — this matches our kill-condition but v2 requires it to survive the schema, not just exist in prose. ADOPT to extend our MechanismHypothesis with these two checks.

**4. Multi-biased reviewer ensemble with THOUGHT + JSON (AgentLab + v2)**
We have generator/critic/selector isolation and multi-perspective analysis, but no formalized 3-reviewer rubric with different mandates (experiments-rigor, impact, novelty) producing structured JSON scores. The NeurIPS-form rubric + biased pos/neg ensemble (v2) + weighted aggregate formula (AgentLab) is directly liftable for our DECIDE gate. ADOPT as `/ensemble-review`.

**5. Structured metric schema with `lower_is_better` and `valid_metrics_received` gate (ai-scientist-v2)**
Our science kernel says "score improvement alone never confirms a mechanism", but we have no formal contract for what a valid metric output must contain. The `metric_parse_spec` schema — precise metric_name (no 'train'/'val'), dataset_name (no 'train'/'val'/'test'), final_value, best_value, valid_metrics_received flag — is a precision layer that eliminates ambiguity. ADOPT for all experiment nodes.

**6. Innovation graph / citation influence pipeline (AI-Researcher)**
We have Semantic Scholar novelty checks (via GPT-5.5 Pro) but no systematic 5-step citation-influence extraction to understand HOW prior art relates (foundation vs. component vs. inspiration). This is particularly valuable for our Track 2 gradient-field direction where Kaiming He's line (JiT/MeanFlow/pMF/ELF) is complex prior art. ADOPT as `/lit-influence`.

**7. Compute budget with urgency signal at 70% (AgentLaboratory)**
We track cycle count in RUNLOG but have no explicit per-phase step budget with an urgency trigger. The `max_steps` + urgency-at-70% pattern keeps phases from diverging. ADOPT as a per-phase budget in goal mode.

### OVERLAPS — Already in Our Kernel

- Multi-engine isolation (Opus generates, Codex selects, GPT-5.5 novelty) — equivalent to all three frameworks' multi-agent/multi-model separation.
- Idea reflection loops (`--num-reflections`) — already in our IDEATE cycle.
- Literature review before plan — already in our L1 cognitive loop.
- Multi-perspective analysis (generator/critic/selector isolation) — equivalent to their 3-reviewer types, though our version is less formalized.
- Sequential phase pipeline with checkpointing — equivalent to our RUNLOG + Arbor tree.
- Novelty check via Semantic Scholar (v2) or Innovation Graph (AI-Researcher) — we use GPT-5.5 Pro for novelty audits; different mechanism but same function.
- ArXiv search + summarize in lit review (AgentLab) — our `literature-reviewer` agent does this.

### SKIP — Not Relevant to Our Loop

- AgentLaboratory's inter-agent dialogue model for plan formulation (PhD↔Postdoc↔Professor turns) — adds latency; our Opus → Codex handoff achieves the same isolation more efficiently.
- HuggingFace dataset requirement hardcoded into experiment phases (AgentLab) — domain-specific to their use case.
- Docker container isolation (AI-Researcher) — we already have worktrees for isolation.
- AgentRxiv cross-session paper sharing infrastructure — interesting but requires significant infra overhead; not relevant to our current project.
- The level-2 "generate idea from papers only" workflow (AI-Researcher) — we already do this in goal mode via Opus + GPT-5.5 Pro.
- Copilot mode (AgentLab) — we have human-in-loop from CLAUDE.md rules already.

---

## 7. Top-3 Highest-Value Takeaways

**Takeaway 1: 4-stage progressive experiment protocol with formal gates (ai-scientist-v2)**
The concrete sequence — basic impl (architecture only) → tune hyperparameters (architecture FROZEN) → creative research → ablation — plus the structured `stage_completion_eval_spec` with `missing_criteria` output is the single most directly adoptable pattern. It operationalizes our "one-variable + negative-control" kernel as a staged timeline rather than a principle, making it enforceable by the Arbor tree. In our DiffusionGemma context: Stage 1 = verify baseline routing/adapter; Stage 2 = tune lr/schedule (NO architecture change); Stage 3 = gradient-field variants; Stage 4 = ablation (which components contribute).
**Source:** `ai_scientist/treesearch/agent_manager.py` lines 143-167.

**Takeaway 2: Idea schema with "not trivial extension" test + Risk Factors as first-class field (ai-scientist-v2)**
The `Short Hypothesis` field's required qualifier — "ensure this is the best setting to investigate this idea, and there are not obvious other simpler ways to answer the question" — is a precision version of our first-principles reduction that can be mechanically checked before dispatch. The `Risk Factors and Limitations` field forces pre-mortems into the idea schema itself, not just prose notes. Together these extend our 5-field MechanismHypothesis with two missing pieces: the "not simpler" check and a structured risk register. Directly lift the FinalizeIdea schema into `/ideate-schema`.
**Source:** `ai_scientist/perform_ideation_temp_free.py` lines 27-96.

**Takeaway 3: Multi-biased reviewer ensemble with NeurIPS rubric + THOUGHT+JSON format (AgentLab + v2)**
Using three reviewers with orthogonal mandates (experiments-rigor, impact, novelty/open-mindedness) — not three identical reviewers — generates structured disagreement that surfaces different kill-conditions. The THOUGHT section (required: specific to this paper, not generic) prevents the reviewer from pattern-matching. The weighted aggregate (overall weight=1.0, contribution=0.4, presentation=0.2, others=0.1) gives a principled scalar for the DECIDE gate. Currently we route to Codex for merge/prune decisions but without a formal rubric. This pattern could make the Codex review step at our DECIDE gate both more principled and audit-able.
**Source:** `agents.py` lines 37-200, `perform_llm_review.py` lines 13-122.

---

*End of extraction. 6-line summary follows:*

**What they are:** AgentLaboratory = multi-role dialogue loop (PhD/Postdoc/Professor) for lit-review→plan→code→write; AI-Researcher = two-level system (full spec or ref-papers-only) with 5-step citation-influence graph and Inno-Bench; ai-scientist-v2 = template-free best-first tree search over 4 progressive experiment stages with structured gates.

**Top-3 takeaways:** (1) 4-stage progressive experiment protocol (impl→tune-only→creative→ablation) with formal `missing_criteria` completion gates — operationalizes our one-variable rule as enforceable stages; (2) Idea schema with mandatory "not simpler" test and first-class `Risk Factors` field — extends our MechanismHypothesis with two precision checks; (3) 3-persona reviewer ensemble (experiments/impact/novelty mandates) with THOUGHT+NeurIPS-JSON + weighted aggregate — makes the DECIDE gate auditable.

**Command candidates:** 6 new skills identified: `/stage-protocol`, `/ideate-schema`, `/lit-influence`, `/ensemble-review`, `/metric-schema`, `/idea-reflect`.
