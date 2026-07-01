# Scientist-B: Research Methodology Extraction
## Four Autonomous-AI-Research Frameworks — Distilled for DiffusionGemma Project

Date: 2026-06-29
Source repos: Curie · InternAgent · RD-Agent · research-town

---

## 1. What Each Is

**Curie** (`/home/lingxufeng/research/scientist/Curie/`) — First AI-agent framework explicitly designed for *rigorous controlled experimentation*. Accepts a natural-language question, runs clarification, generates an experiment plan with explicit control/experimental groups (independent / constant / dependent variables), parallelizes partitions into Docker containers, and gates every result through a three-layer verification pipeline (LLM structural verifier → execution verifier → patcher). Outputs a formal academic-style report. Top-performer on EXP-Bench ("Can AI conduct AI research experiments?").

**InternAgent 1.5** (`/home/lingxufeng/research/scientist/InternAgent/`) — Unified multi-agent framework for long-horizon autonomous scientific discovery (formerly NovelSeek). Orchestrates a full idea-generation pipeline: Deep-Research background → Generate N ideas → Reflect → Literature survey → Evolve top-k → Rank by weighted criteria → Develop method → Refine → Execute (MCTS optional) → Update memory. Includes a three-layer memory system (task memory with positive/neutral/negative labels, long-memory IdeaGraph with similarity edges, online memory). Supports 12+ scientific task types including paper reproduction (ResearchClawBench).

**RD-Agent** (`/home/lingxufeng/research/scientist/RD-Agent/`) — Microsoft's R&D automation framework separating *Research* (hypothesis) from *Development* (implementation). Core abstractions: `Hypothesis → Experiment → Feedback → Trace → KnowledgeBase`. Runs an RD-Loop: HypothesisGen → Hypothesis2Experiment → Coder (CoSTEER) → Runner → Experiment2Feedback → back. Always compares to a SOTA checkpoint, generates code diffs between iterations, and feeds structured feedback back into hypothesis generation. Top on MLE-bench (30.22% with o3+GPT-4.1 vs 16.9% previous best). Scenarios: quant trading, Kaggle, fine-tuning, general ML.

**research-town** (`/home/lingxufeng/research/scientist/research-town/`) — Not an experimentation engine. A *community-level research simulator* (FSM-based multi-agent). Simulates the full academic lifecycle: literature review → idea brainstorming → proposal writing (with/without RAG) → peer review (strength/weakness/score) → rebuttal → meta-review. Useful not for running experiments but for structuring proposals, running simulated peer review, and generating rebuttals.

---

## 2. Core Methodology / Workflow Spine

### Curie Spine
```
Question → [Clarify] → Supervisor proposes Experiment Plan (JSON)
  → Scheduler parallelizes into Partitions
  → Worker designs Control group workflow (.sh)
  → LLM Verifier: structural check (no mocks, all vars used, results exist)
  → Exec Verifier: run and check exit code
  → Patcher: fix errors (up to N rounds)
  → Experimental Group workers (parallel)
  → Analyzer: partial result holistic check, suggest continue/new plan
  → Concluder: decide conclude or add plans
  → Reporter: formal markdown report
```

Key discipline: **plan is a structured JSON** with explicit variable taxonomy. Every partition must be callable via a no-argument shell script and dump results to a fixed-name .txt file. Workers are forbidden to mock results — the LLM verifier catches this explicitly.

### InternAgent Spine
```
[Loop round 1..N]:
  DR Agent: generate task background (lit-based context)
  GenerationAgent: produce M ideas filtered against failed-memory
  ScholarAgent + SurveyAgent: literature retrieval (arxiv/crossref/web)
  ReflectionAgent: critique each idea (R rounds)
  EvolutionAgent: mutate top-k ideas
  RankingAgent: score on 4 weighted criteria → select top-k
  MethodDevelopmentAgent: write full method for each selected idea
  RefinementAgent: refine
  ExperimentRunner: execute (MCTS or linear, up to max_runs)
  ExpAnalyzeAgent: extract metrics, label outcome positive/neutral/negative
  OnlineMemory.save(idea, metrics, label)
  [PromptEvolver: evolve generation prompt based on experience library]
  [IdeaGraph: add nodes/edges, prune dead branches]
```

Common with Curie: generator → executor → evaluator pipeline, explicit feedback loop.

### RD-Agent Spine
```
[RD Loop]:
  ScenarioAnalysis: SOTA alignment / gap / domain-coherence / scenario-first
  HypothesisGen: propose Hypothesis with observation + justification + knowledge
  Hypothesis2Experiment: translate to concrete tasks (DataLoader/Feature/Model/Ensemble/Workflow)
  Coder (CoSTEER): implement incrementally
  Runner: execute in isolated workspace
  Experiment2Feedback:
    - compare metric to SOTA score
    - generate diff from SOTA workspace
    - decision: bool (accept as new SOTA?)
    - observations + hypothesis_evaluation + new_hypothesis
  KnowledgeBase.dump()  ← persist
  [if decision=True: update SOTA checkpoint]
  back to HypothesisGen with full trace
```

Distinctive: **SOTA checkpoint tracking** — every run is compared against the best previous result, not just the last. Code diff is generated between current and SOTA workspace to make changes explicit.

### research-town Spine
```
Engine (FSM) transitions:
  start → LiteratureReview (each researcher reads N related papers → Insight)
  → IdeaBrainstorm (each researcher proposes 1-2 sentence idea from Insight)
  → ProposalWriting (leader summarizes ideas → full proposal via 5Q CoT)
  → ReviewWriting (N reviewers: strength / weakness / score on 7 criteria)
  → RebuttalWriting (author responds to reviews via 5Q)
  → MetaReviewWriting (meta-reviewer aggregates reviews → accept/reject)
  → end
```

Evaluators run after each environment: IdeaQualityEvaluator, ProposalQualityEvaluator, ReviewQualityEvaluator, RebuttalQualityEvaluator, MetaReviewQualityEvaluator — all emit a 0-100 score + 6 dimension sub-scores.

### What All Four Share
- Iterative loop with persistent history (trace / memory / knowledge base)
- Generator / Critic / Selector role isolation (matches our L2 kernel #7)
- Structured hypothesis with fields beyond a plain string
- Feedback always references prior state (previous results / SOTA / failed ideas)
- Separate evaluation agent that does not generate (matches our isolation discipline)

---

## 3. Experiment Standards / Specs

### Curie's Experiment Plan Schema
File: `curie/curie/configs/base_config.json`, plans stored via `write_new_exp_plan` tool.

Plan JSON structure (reconstructed from agent prompts):
```json
{
  "question": "<full research question with all context>",
  "hypothesis": "<falsifiable claim>",
  "independent_variables": {"var_name": ["value1", "value2"]},
  "constant_variables": {"var_name": "fixed_value"},
  "dependent_variables": ["metric1", "metric2"],
  "controlled_experiment_setup_description": "<brief setup>",
  "control_group": {"partition_1": {"vars": {...}, "done": false}},
  "experimental_group": {"partition_1": {"vars": {...}, "done": false}},
  "priority": 1
}
```

### Curie's 5-Point Verifier Checklist
File: `curie/curie/prompts/llm-verifier.txt`
```
(5a) Legitimate handling of inputs and outputs
(5b) Proper integration between scripts
(5c) No hardcoded or mock data
(5d) No placeholder values (e.g., 'your_api_key_here') left in code
(5e) All variables (independent/constant/dependent) explicitly used in workflow
(5f) Workload details from question correctly generated or utilized
THEN: check results file exists and contains values for all variable values required
```

### Curie's Three-Stage Verification Gate
```
Stage 1 (LLM Verifier): inspect scripts statically — correct structure, no mocks, all vars used
Stage 2 (Exec Verifier): run script, check exit code, check results file exists
Stage 3 (Patcher): if Stage 1 or 2 fails, patcher agent debugs + retries; back to Stage 1
```
Patcher prompt (file: `curie/curie/prompts/exp-patcher.txt`) uses `patchagent_openhands` and records `is_correct` + `patcher_log_message`.

### Curie's Concluder Decision Protocol
File: `curie/curie/prompts/exp-concluder.txt`
```
1. Retrieve ALL plans via exp_plan_get (no plan_id = get all)
2. For each plan, read every partition result file
3. Holistic analysis: do results collectively answer the question?
4. Options:
   (3a) Conclude — repeat all key numbers in the conclusion statement
   (3b) Create new plan or partition
Record via concluder_record tool
```
Key: Concluder may override Analyzer's "suggest conclude" — final decision remains with Concluder.

### InternAgent's Ranking Criteria Weights
File: `InternAgent/config/default_config.yaml`
```yaml
criteria:
  novelty: 0.3
  plausibility: 0.4   # highest weight — must be scientifically sound
  testability: 0.2
  alignment: 0.1
```
Weights must sum to 1.0. RankingAgent normalizes if not. Strategy: "default" (pure weighted score) or "distinct" (maximize diversity across parent groups).

### InternAgent's Failed-Idea Filtering Gate
File: `InternAgent/config/default_config.yaml`, `InternAgent/internagent/mas/agents/generation_agent.py`
```yaml
filter_failed_ideas: true
failed_similarity_threshold: 0.7  # cosine similarity
max_regeneration_attempts: 2
```
Before accepting a generated idea, agent checks it against all negative-label memory records. If similarity > 0.7 to a failed idea, the idea is regenerated (up to 2 attempts). If still similar after 2 attempts, it passes with a warning.

### RD-Agent's Hypothesis Fields
File: `RD-Agent/rdagent/core/proposal.py`
```python
class Hypothesis:
    hypothesis: str          # the core falsifiable claim
    reason: str              # full justification
    concise_reason: str      # ≤2 sentences
    concise_observation: str # what observation prompted this
    concise_justification: str
    concise_knowledge: str   # which domain knowledge supports this
```

### RD-Agent's ScenarioAnalysis (Pre-Hypothesis Gate)
File: `RD-Agent/rdagent/scenarios/data_science/proposal/exp_gen/proposal.py`
```python
class ScenarioAnalysis(BaseModel):
    sota_alignment_analysis: str  # compare SOTA to data/domain insights
    gap_identification: str       # unaddressed challenges in successful solutions
    domain_implementation_coherence_check: str  # technical methods conflicting with domain rules
    scenario_first_focus: str     # foundational strategies if no SOTA exists
```
Then ScenarioChallenges selects "FEWER BUT BETTER" — at most 5 challenges, each with: reasoning, category (dataset-driven | domain-informed), statement, metric_impact, caption.

### RD-Agent's Feedback / SOTA-Delta Protocol
File: `RD-Agent/rdagent/scenarios/data_science/dev/feedback.py`
```
Feedback always includes:
  - decision: bool (should this become the new SOTA?)
  - observations: what did the results show
  - hypothesis_evaluation: did the hypothesis hold
  - new_hypothesis: suggested next direction
  - code_change_summary: what was changed
  - cur_vs_sota_score: "<current> vs <sota>; higher/lower is better"
  - diff from SOTA workspace (generated via generate_diff_from_dict)
If evaluation_not_aligned: exp.result = None (result is ignored)
```

### research-town's 5Q Proposal Framework
File: `research-town/configs/agent_prompt/write_proposal_cot.yaml`
```
[Q1] What is the problem? (one specific research question)
[Q2] Why is it interesting and important? (broader implications, future research impact)
[Q3] Why is it hard? (technical/theoretical obstacles, why naive approaches fail)
[Q4] Why hasn't it been solved before? (gaps, barriers, how this approach differs)
[Q5] What are the key components? (method, dataset, metric, expected outcomes)
Format: chain-of-thought reasoning THEN final labeled answer for each question
```

### research-town's 6-Dimension Evaluation Rubric
File: `research-town/configs/eval_prompt/proposal_quality.yaml`, `idea_quality.yaml`
```
1. Novelty (1-10): new perspective, new techniques vs existing, divergence from insights
2. Validity (1-10): theoretical foundations, logical consistency, sound methodology
3. Significance (1-10): potential contribution and impact, comparison to existing works
4. Rigorousness/Feasibility (1-10): methods clearly described, results well-analyzed, claims supported
5. Clarity (1-10): title/abstract quality, structure, ease of follow
6. Ethical Considerations (1-10): ethical guidelines, potential negative consequences addressed
Overall Score (0-100)
Output format: Overall Score=89 Dimension Scores=[8,9,9,9,9,9]
```

---

## 4. Reusable Artifacts — Quoted Prompts, Templates, Rubrics

### A. Curie — Clarification Prompt (5 targeted questions at session start)
File: `curie/curie/prompts/clarification.txt`
```
Focus on these key areas:
1. Baseline Solutions: Any existing solutions, code, or baselines the user has
2. Instructions: Specific constraints, requirements, or limitations for the implementation
3. Objectives: What specific metrics or outcomes are expected (e.g., accuracy, speed, memory usage)
4. Results Placement: Where results should be logged and how to interpret them
5. Assumptions: Any implicit context, constraints, or assumptions
Generate 4-5 concise, specific clarification questions based on the research question provided.
```
USE: Fire this before any major experiment cycle to surface hidden constraints.

### B. Curie — Supervisor Workflow Prompt (plan design discipline)
File: `curie/curie/prompts/exp-supervisor.txt` (key extract)
```
Think step by step and comprehensively before you propose a plan:
- Specify the exact values each variable should have in your groups.
- Redo specific partitions if their workflow is incorrect, rather than modifying the entire plan
  to prevent unintended changes.
Notes about your responsibilities:
- Experimental plans (and any changes to them) need to be stored for persistence.
- You may choose to only have 1 experimental plan (i.e., 1 hypothesis), or create other
  alternative plans as you see fit (e.g., as you receive new data from existing experiments),
  to best answer the user's question.
```

### C. Curie — LLM Verifier Workflow Prompt (anti-mock checklist)
File: `curie/curie/prompts/llm-verifier.txt` (key extract)
```
Verify that the workflow is designed to produce real results, not simulated or placeholder ones,
by checking for:
(5a) Legitimate handling of inputs and outputs.
(5b) Proper integration between scripts.
(5c) Any signs of hardcoded or mock data.
(5d) Any placeholder values (e.g., 'your_api_key_here') have been replaced with actual values.
(5e) Explicitly utilizes all variables (with values specified for this partition).
(5f) Workload details specified in the "question" are being utilized or generated correctly.
```

### D. Curie — Reporter Template (formal report sections)
File: `curie/curie/prompts/exp-reporter.txt`
```
Sections: Title + Abstract → Introduction (question + hypothesis) → Methodology
  (design + setup + challenges) → Results (metrics + table format + figures referenced as
  ![name](filename.png) *<small>Caption</small>*) → Conclusion + Future Work → Appendices
  (raw log dir + config + meta-info)
```

### E. InternAgent — Coder Prompt (baseline discipline)
File: `InternAgent/internagent/prompts.py` (`CODER_PROMPT_MCTS_DRAFT`)
```
Note that we already provide the vanilla baseline results, so you do not need to re-run it.
Any modifications to `argparse` parameters (new/updated) must enforce the improved
implementation as the default behavior. Set default=<revised_value> for all altered arguments
to ensure the enhanced logic activates automatically without CLI flags.
```

### F. InternAgent — Next Experiment Reflection Prompt
File: `InternAgent/internagent/prompts.py` (`NEXT_EXPERIMENT_PROMPT`)
```
Run {RUN_NUM} completed. Here are the results: {RESULTS}

Based on these results:
1. Analyze what worked and what didn't work in your approach.
2. Compare the current run with previous runs and baseline.
3. Decide if you need to re-plan your experiments or continue with your current strategy.
4. If continuing, implement the next improvement on your list.
5. If re-planning, explain why and outline your new approach.
If you believe you have completed all necessary experiments and found the optimal solution,
respond with 'ALL_COMPLETED'.
```
USE: Template for per-run reflection in our diffusion training loop.

### G. RD-Agent — Hypothesis Generation Prompt (Jinja2 template)
File: `RD-Agent/rdagent/components/proposal/prompts.yaml` (`hypothesis_gen.system_prompt`)
```
Your task is to analyze previous experiments, reflect on the decision made in each experiment,
and consider why experiments with a decision of true were successful while those with a decision
of false failed. Then, think about how to improve further — either by refining the existing
approach or by exploring an entirely new direction.

If one exists and you agree with it, feel free to use it.
If you disagree, please generate an improved version.
Important: If the hypothesis_specification outlines the next steps you need to follow,
ensure you adhere to those instructions.
```

### H. RD-Agent — Hypothesis2Experiment Prompt (translate hypothesis to tasks)
File: `RD-Agent/rdagent/components/proposal/prompts.yaml` (`hypothesis2experiment.user_prompt`)
```
The user will provide this information to you:
1. The target hypothesis you are targeting to generate {targets} for.
2. The hypothesis generated in the previous steps and their corresponding feedbacks.
3. Former proposed {targets} on similar hypothesis.
4. Some additional information to help you generate new {targets}.
Also provided: sota_hypothesis_and_feedback, last_hypothesis_and_feedback
```

### I. research-town — Proposal 5Q Chain-of-Thought Template
File: `research-town/configs/agent_prompt/write_proposal_cot.yaml` (`template`)
```
For each question, first think through the answer step by step, using the information from
the idea and external data, and write down your reasoning process as a chain of thought.
Then, provide the final answer to the question, clearly labeled in the format: [Question X].

Chain of Thought for Question 1:
Step-by-step reasoning and analysis...
[Question 1]: Final formulated research question ending with a question mark.

Chain of Thought for Question 2: ...
[Question 2]: Final answer...
(Continue for Q3, Q4, Q5)
```

### J. research-town — Idea Brainstorm Prompt (novelty discipline)
File: `research-town/configs/agent_prompt/brainstorm_idea.yaml` (`sys_prompt`)
```
It is not that innovative to combine several algorithms to solve one problem. However, it is
innovative to explore a new problem using tools at hand. It is also great to develop new
solutions for an existing problem. Your idea should be different from those in the related papers.
```

### K. research-town — Paper Review Criteria (full checklist)
File: `research-town/configs/agent_prompt/write_review_strength.yaml` (`template`)
```
Please evaluate the submission based on the following criteria:
Clarity: Is the writing clear, structured, and terms defined?
Baselines: Are baseline comparisons relevant, sufficient, and not excessive?
Novelty: Is the approach innovative or distinct from prior work?
Results: Are improvements significant, well-supported, and statistically robust?
Limitations: Are weaknesses acknowledged and future work discussed?
Related Work: Are key references cited and connections made?
Technical: Are methods detailed enough for replication?
When commenting on the experiments, refer to the exact numbers from the experiments.
```

---

## 5. Command/Skill Candidates

| Name | Purpose | Trigger | Engine |
|------|---------|---------|--------|
| `/controlled-exp-plan` | Generate a structured experiment plan JSON: hypothesis + control/experimental groups + variable taxonomy (independent/constant/dependent) + parallel partitions | Before dispatching any new experiment direction | Opus |
| `/exp-verify` | 3-stage verification of an experiment result: (1) LLM structural check — no mocks, all variables used; (2) execution check — result file exists, no errors; (3) result plausibility check | After every experiment run completes | Codex |
| `/idea-rank` | Score ≥2 candidate ideas on 4 weighted criteria (novelty 0.3 / plausibility 0.4 / testability 0.2 / alignment 0.1), select top-k and block ideas similar to failed attempts (cosine sim > 0.7) | After ideation, before dispatch | Opus |
| `/scenario-analysis` | Pre-hypothesis gap analysis: SOTA alignment, gap identification, domain-implementation coherence check, scenario-first focus → produce "FEWER BUT BETTER" ≤5 prioritized challenges | Start of every new research cycle | GPT-5.5 Pro |
| `/proposal-5q` | Structure a research claim or direction as 5Q CoT: problem → importance → hardness → why-not-before → key components + expected results | Before paper writing, rebuttal, or framing a new direction for stakeholders | Opus |
| `/self-review-6dim` | Evaluate a proposal or paper draft on 6 dimensions (novelty / validity / significance / rigorousness / clarity / ethics), each 1-10 + overall 0-100 | Before any submission or novelty audit | Opus |
| `/sota-feedback` | Generate structured feedback after an experiment: current score vs SOTA, diff from SOTA workspace, decision (bool), observations, hypothesis evaluation, new hypothesis suggestion | After each completed experiment, before deciding next hypothesis | Codex |

---

## 6. NEW vs Our Kernel

### GENUINELY NEW — ADOPT

**N1. Structured Controlled Experiment Plan Schema (Curie)**
Our kernel says "one-variable + negative-control + locality" (L2 #5) but never formalizes this into a stored artifact. Curie's JSON schema with explicit independent/constant/dependent variable dictionaries and parallel partitions is the operationalization missing from our workflow. Directly adoptable for DiffusionGemma ablation runs.
- File: `curie/curie/prompts/exp-supervisor.txt`, `curie/curie/prompts/exp-controlled-setup-worker.txt`

**N2. Three-Stage Verification Pipeline (Curie)**
Our kernel has "generator/critic/selector ISOLATION" (L2 #7) but no concrete verification checklist. Curie's 5-point LLM verifier checklist (no mocks, all variables used, results file exists) + exec verifier + patcher is a concrete implementation we lack. Critical for our training runs where "loss went down" is not evidence of quality.
- File: `curie/curie/prompts/llm-verifier.txt`, `curie/curie/prompts/exp-patcher.txt`

**N3. Failed-Idea Memory with Similarity Filtering (InternAgent)**
Our Arbor tree marks nodes as "pruned" but doesn't block similar ideas at generation time. InternAgent's approach of labeling outcomes positive/neutral/negative and rejecting new ideas with cosine similarity > 0.7 to failed ones would directly prevent our loop from re-proposing dead directions (e.g., re-trying naive embedding-flow approaches already killed).
- File: `InternAgent/internagent/mas/agents/generation_agent.py`, config `filter_failed_ideas: true`

**N4. SOTA-Delta Feedback with Code Diff (RD-Agent)**
Our L2 kernel says "score≠mechanism" but doesn't operationalize what feedback should contain. RD-Agent's protocol — always generate diff between current and SOTA workspace, always include `decision: bool`, always state `cur_vs_sota_score` with direction — is a concrete feedback schema. Adoptable as our post-experiment reflection template.
- File: `RD-Agent/rdagent/scenarios/data_science/dev/feedback.py`, `RD-Agent/rdagent/components/proposal/prompts.yaml`

**N5. ScenarioAnalysis as Pre-Hypothesis Gate (RD-Agent)**
Our L1 loop starts with "skeptical-default → cross-domain-map" but we have no structured analysis artifact before proposing a hypothesis. RD-Agent's ScenarioAnalysis (sota_alignment_analysis / gap_identification / domain_implementation_coherence_check / scenario_first_focus) would force us to articulate the gap before proposing direction C extensions.
- File: `RD-Agent/rdagent/scenarios/data_science/proposal/exp_gen/proposal.py` (ScenarioAnalysis class)

**N6. 5Q Proposal Format + 6-Dim Evaluation Rubric (research-town)**
We write free-form proposals and hypotheses. The 5Q chain-of-thought format (problem / importance / hardness / why-not-before / components) is a standalone structuring tool compatible with our per-direction framing. The 6-dim rubric (novelty / validity / significance / rigorousness / clarity / ethics → 0-100) gives us a reusable self-assessment gate before any novelty audit or GPT-5.5 Pro query.
- File: `research-town/configs/agent_prompt/write_proposal_cot.yaml`, `research-town/configs/eval_prompt/proposal_quality.yaml`

**N7. Clarification Protocol Before Long-Running Experiments (Curie)**
Our goal-mode loop dives in without eliciting hidden constraints. Curie's 4-5 targeted clarification questions (baseline solutions / constraints / objectives / results placement / assumptions) prevent wasted experiment budget. Directly useful before any new ablation series.
- File: `curie/curie/prompts/clarification.txt`

### OVERLAPS — ALREADY COVERED

**O1. Generator/Critic/Selector Isolation** — All 4 frameworks implement this; our L2 #7 already mandates it and our multi-engine setup (Opus/Codex/GPT-5.5 Pro) implements it structurally. No new action needed.

**O2. Falsifiable Hypothesis** — Curie requires a "hypothesis" field; RD-Agent has `Hypothesis.hypothesis`; our 5-field MechanismHypothesis already formalizes this. The fields overlap significantly (our "prediction" ≈ their hypothesis; our "falsifier" is more explicit than any of the 4 frameworks). We are ahead here.

**O3. Iterative Loop with History** — Curie's analyzer, InternAgent's trace, RD-Agent's Trace, our Arbor RUNLOG all serve the same purpose. Our goal-mode + RUNLOG is adequate.

**O4. Idea Tree / Memory** — InternAgent's IdeaGraph (ChromaDB + NetworkX) is more sophisticated than our Arbor tree, but the Arbor tree covers the structural need. The novelty is the *similarity-based filtering of failed ideas* (N3 above), not the graph itself.

**O5. MCTS for Exploration** — Both InternAgent and RD-Agent offer MCTS. Our goal-mode drives exploration deterministically with Opus. MCTS adds stochastic breadth we currently don't need for a focused 1-direction study.

### SKIP

**S1. Curie's Docker isolation** — Our environment (DiffusionGemma, conda dllm env) is fixed; containerizing adds overhead with no benefit.

**S2. research-town's full community simulation** — We only need the proposal-writing and peer-review primitives (N6), not the FSM orchestrator or agent-role management.

**S3. InternAgent's IdeaGraph / PromptEvolver** — The graph representation is infrastructure overhead. The filtering benefit (N3) can be implemented without ChromaDB by maintaining a simple failed-directions list in RUNLOG and checking against it with an LLM similarity call.

**S4. RD-Agent's CoSTEER coder** — Their collaborative code evolution system is valuable for iterative ML engineering. For our diffusion work the coder role is handled by worktree subagents; CoSTEER's specific architecture adds complexity without benefit.

---

## 7. Top-3 Highest-Value Takeaways Across All 4

### Takeaway 1: Curie's 3-Stage Verification Pipeline Is the Most Transferable Rigor Upgrade

Our current workflow accepts an experiment result when the training script exits 0 and reports a loss curve. Curie's pipeline forces three independent checks before any result is trusted: (1) Does the experimental workflow actually test what we said it tests — are all variables present, no mocks, no placeholder values? (2) Did execution succeed and produce a results artifact? (3) Is the result file populated with real numbers?

For DiffusionGemma this would manifest as: (1) an LLM check that the evaluation script actually measures token-level accuracy / step-skip rate and not just training loss; (2) an existence check on the output JSON; (3) a plausibility check that reported numbers fall in a sensible range (e.g., accuracy 0.4–0.99, not 0.001). Our "SEALED eval/test" kernel (L2 #3) says sealing is necessary but gives no protocol for verifying the seal held. Curie fills that gap.

Most directly adoptable as `/exp-verify` skill.

### Takeaway 2: RD-Agent's SOTA-Delta Feedback Operationalizes "score≠mechanism"

Our L2 kernel rule #3 ("score improvement alone never confirms a mechanism — require negative controls + locality") is conceptual. RD-Agent turns it into a required feedback artifact: every experiment produces a `decision: bool` (did this beat SOTA?), a human-readable `observations` field (what specifically changed in the output), a `hypothesis_evaluation` (did the hypothesis about the mechanism hold), and a diff of the code changed. The forced diff is particularly valuable: in our setting, if direction-C router change improved accuracy by 2%, the diff shows whether that came from the router or from an accidental regularization side-effect.

We should apply this discipline to every worktree merge decision: require a diff from the SOTA worktree, require a mechanism statement, require `decision: bool` before updating RUNLOG as "accepted."

Most directly adoptable as `/sota-feedback` skill, run by Codex at every merge gate.

### Takeaway 3: Pre-Hypothesis ScenarioAnalysis (RD-Agent) + 5Q Proposal Format (research-town) Together Form a Complete "Before You Run Anything" Gate

RD-Agent forces analysts to articulate four things before proposing a hypothesis: what SOTA alignment says, what gaps remain, whether the proposed method conflicts with domain constraints, and what the foundational baseline assumption is. research-town forces the proposal to answer five questions: what is the problem, why it matters, why it's hard, why prior work missed it, and what specifically will be measured.

Together, these two form a gate that would have caught several direction-C design issues in our loop (e.g., the "commit prior" ambiguity flagged in our peer-review notes, the "vanilla t-conditioning is too simple" concern). Running both gates before dispatching any experiment would surface these issues before burning GPU time.

Implement as `/scenario-analysis` (GPT-5.5 Pro, run before each new cycle) + `/proposal-5q` (Opus, run before framing for human review or paper).

---

## Appendix: Key File Paths for Quick Reference

| Artifact | Path |
|---------|------|
| Curie clarification prompt | `Curie/curie/prompts/clarification.txt` |
| Curie supervisor prompt | `Curie/curie/prompts/exp-supervisor.txt` |
| Curie LLM verifier prompt | `Curie/curie/prompts/llm-verifier.txt` |
| Curie patcher prompt | `Curie/curie/prompts/exp-patcher.txt` |
| Curie concluder prompt | `Curie/curie/prompts/exp-concluder.txt` |
| Curie analyzer prompt | `Curie/curie/prompts/exp-analyzer.txt` |
| Curie reporter prompt | `Curie/curie/prompts/exp-reporter.txt` |
| Curie base config | `Curie/curie/configs/base_config.json` |
| InternAgent default config | `InternAgent/config/default_config.yaml` |
| InternAgent prompts (coder, debug, reflection) | `InternAgent/internagent/prompts.py` |
| InternAgent generation agent (failed-idea filter) | `InternAgent/internagent/mas/agents/generation_agent.py` |
| InternAgent ranking agent (weighted criteria) | `InternAgent/internagent/mas/agents/ranking_agent.py` |
| InternAgent memory module docs | `InternAgent/docs/memory_module.md` |
| RD-Agent core Hypothesis class | `RD-Agent/rdagent/core/proposal.py` |
| RD-Agent RD loop | `RD-Agent/rdagent/components/workflow/rd_loop.py` |
| RD-Agent hypothesis gen prompts (Jinja2 YAML) | `RD-Agent/rdagent/components/proposal/prompts.yaml` |
| RD-Agent ScenarioAnalysis class | `RD-Agent/rdagent/scenarios/data_science/proposal/exp_gen/proposal.py` |
| RD-Agent SOTA feedback generator | `RD-Agent/rdagent/scenarios/data_science/dev/feedback.py` |
| research-town 5Q proposal prompt | `research-town/configs/agent_prompt/write_proposal_cot.yaml` |
| research-town brainstorm prompt | `research-town/configs/agent_prompt/brainstorm_idea.yaml` |
| research-town proposal quality rubric | `research-town/configs/eval_prompt/proposal_quality.yaml` |
| research-town idea quality rubric | `research-town/configs/eval_prompt/idea_quality.yaml` |
| research-town review criteria | `research-town/configs/agent_prompt/write_review_strength.yaml` |
| research-town rebuttal 5Q | `research-town/configs/agent_prompt/write_rebuttal.yaml` |
