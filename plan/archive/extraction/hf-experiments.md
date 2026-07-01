# HF Project — Experiment Discipline Extraction
> Extracted 2026-06-29 from RUNLOG cycles 1–18, plan/frozen-pareto-negative-synthesis.md,
> plan/research-redesign-verified-wallclock-frontier.md, plan/research-redesign-equivalence-class.md,
> plan/rescue-audit-protocol.md, plan/saturation-experiment-protocol.md,
> plan/operating-manual.md §4–5, plan/ai-research-conduct-principles.md,
> plan/research-method-anatomy.md, and diffusiongemma_sft/.

---

## 1. What This Project's Experiment Practice Is

This project runs a "falsify-before-build, redesign-on-contradiction" research loop over a frozen 26B diffusion-language MoE. The practice is empirical and adversarial: every hypothesis enters a pre-registration step where its exact kill condition is written down before any sealed data is seen; a budget-probe fires first to prevent expensive failures; all results are independently reviewed by a separate model (Codex GPT-5.5) before being accepted; and negative results — including two fully-killed leads (E-kill: trace dynamics carry no rescue signal; A-falsified: the 2.3% non-observability was a t=1.0 artifact) — are treated as primary deliverables that redirect the program rather than embarrassments to suppress. The connective tissue is the science kernel from `plan/ai-research-conduct-principles.md`: score-up does not equal mechanism; eval/test/baseline are a sealed layer never touched mid-run; the generator (Opus) proposes but never selects (Codex does); and an elegant idea is vetoed unconditionally by a result that contradicts it.

---

## 2. The Experiment Lifecycle That Emerged

```
HYPOTHESIS
  └─ Falsifier + Acceptance + Negative controls + Locality check (written, frozen)
       └─ MEASURE-FIRST PROBE (cheap, timing/oracle, no sealed data)
            └─ [gate: ceiling healthy / confounds absent?] ──NO──► redesign
                 └─ CODEX RIGOR-REVIEW-BEFORE-BUILD (adversarial, independent)
                      └─ [SOUND / SOUND-WITH-FIXES / NEEDS-REDESIGN]
                           └─ DISPATCH (worktree-isolated subagent, setsid-detached + tracked waiter)
                                └─ [experiment runs; sealed data touched for the first time]
                                     └─ ADJUDICATE (Codex independent DECIDE-gate)
                                          └─ [RATIFIED / WIN-NEEDS-FIX / KILL-NEEDS-FAIR-RETEST]
                                               └─ BANK (tree-update FIRST, then RUNLOG)
                                                    └─ loop: redesign on contradiction / advance on ratification
```

Key invariants that hold at every step:
- Falsifier frozen before sealed data is seen (anti-p-hacking)
- Generator (Opus) and selector (Codex) are on different substrates (isolation kernel)
- Every experiment produces reproducible evidence: fixed seeds, checkpoint SHA verified, commands + exit codes logged
- A kill is a success, not a failure; it must exclude ≥2 competing explanations

---

## 3. Experiment Standards / Specs — The Rigor Checklist That Fired Here

### S1: Substrate Integrity Gate (verify before trusting any result)
**Pattern:** Before running any probe, run a trivial sanity check (`7+5→12`, `12×3→36`); verify checkpoint shard SHAs against canonical hashes.
**Where it fired:** RUNLOG Cycle 7 — the local shard `model-00001-of-00011.safetensors` was silently corrupted (digit-token rows zeroed ~91%), making M-PCRH, H5, and all pre-fix results invalid. The "broken generation eval" was a misdiagnosis; the real cause was a corrupt embedding. RUNLOG Cycle 7 (fixed), `plan/operating-manual.md` Lesson #1.
**Rule:** Never cite a metric on an unverified checkpoint. Every experiment begins with the integrity gate.

### S2: Measure-First Probe Before Heavy Compute
**Pattern:** Before a multi-hour GPU sweep, run a 3-problem timing probe and extrapolate; kill any job that overruns 2× the estimate. Before a long calibration, run an inline pilot on a subsample.
**Where it fired:**
- RUNLOG Cycle 2 — the H4 gate failure (fwer=0.142) was diagnosed via an inline measure-first probe on synthetic H0 data (3 configs, minutes) before running R=1000+ calibration. The probe localized the bug without wasting compute. `plan/rescue-audit-protocol.md` §8: "subagent MUST run a 3-problem timing probe and extrapolate before launching the full sweep."
- RUNLOG Cycle 15 — the @2048 dev-smoke (n=32, non-sealed) caught a FATAL budget confound (L=256 ceiling 0.094 → truncation, not meaningful headroom) and 4 code bugs before the sealed MATH-L5 run. "LESSON reinforced: measure-first (cheap dev-smoke) caught a confound + 4 bugs BEFORE wasting a sealed run." RUNLOG Cycle 15.
- `plan/operating-manual.md` §5: "Measure-first (timing probe before heavy compute)."

### S3: Pre-Declared Falsifier Frozen Before Sealed Run (Anti-P-Hacking)
**Pattern:** The exact falsifier (what result will kill this hypothesis) is written into the RUNLOG and/or protocol document before any sealed data is touched. No post-hoc adjustment.
**Where it fired:**
- `plan/frozen-pareto-negative-synthesis.md` §PRE-REGISTERED FALSIFIER: "The synthesis is BROKEN by: any fixed-generator intervention that beats native AND always-deepen-to-matched-mean by ≥2pp verified accuracy at matched NFE AND matched wall-clock, with the negative/locality/anti-verifier-surface controls intact, on a sealed hard set. No such intervention has been found across six attempts."
- `plan/rescue-audit-protocol.md` §v2.C: "KILL (E is engineering → fall back to A) iff any trivial/non-learned control matches the learned ranker within the paired-bootstrap CI, OR the Phase-0 gate fails (<~25 positives)."
- `plan/saturation-experiment-protocol.md` §1: "Surface-recovery falsifier: by K=30, Top10@K ≥ 0.80 AND median target rank ≤ 10 → weaken claim. Predictive falsifier (kills A): Spearman ≥ 0.5, OR AUC ≥ 0.75 with CI-LB ≥ 0.65 → A is DEFEATED."
- RUNLOG Cycle 3 (feasibility): "FALSIFIER (strong-H4 untestable): the router has NO separable t-input → strong-H4 dead on the existing arch." Triggered immediately.

### S4: Diffusion Loss Is an Invalid Proxy — Use Generation/Verifier Metrics
**Pattern:** Reference-token CE / held-out diffusion loss / teacher-forced metrics are diagnostic-only and must not be used as success signals. Only generation-based verifier metrics (exact-match, math_verify, code-exec) count.
**Where it fired:**
- RUNLOG Cycle 7b: "SFT halved diffusion loss (7.66→3.62) for ZERO task accuracy gain. GSM8K pretrained=0.900, SFT=0.883 (tied). Held-out diffusion loss is a POOR proxy for task quality." The metric-validity lesson then propagated to invalidating H5, M-PCRH oracle, and the equivalence-class A thesis.
- RUNLOG Cycle 7b: "teacher-forced per-position argmax matches the gold-REFERENCE token only 2.3% while free-generation exact-match = 0.90."
- `plan/operating-manual.md` Lesson #2: "Held-out diffusion loss / reference-token CE do NOT predict task quality. Use generation / verifier metrics."
- `plan/research-redesign-equivalence-class.md` §Metric family: "Reference CE / diffusion loss / gold-in-top-k / teacher-forced argmax appear ONLY as diagnostics, never as success metrics."

### S5: Sealed Dev/Test Split — Never Touched Until the Final Run
**Pattern:** The test set (B_test / sealed holdout) is defined, committed as a code assertion, and never evaluated until the sealed verdict. Dev set is used for early stopping and parameter tuning only.
**Where it fired:**
- RUNLOG Cycle 2: "SFT.1 BACKPROP MUST eval GSM8K-dev holdout on step_400/step_600/step_1000 and take the best (early-stopping). B_test (GSM8K test split) stays SEALED." No sealed evaluation was run until a final verdict was warranted.
- `plan/rescue-audit-protocol.md` §3: "TEST pool (cross-distribution, primary): AIME-2024 = 30 problems. Sealed layer (NEVER modified): verifier, dataset rows, the EB sampler config."
- `plan/saturation-experiment-protocol.md` §2: "Verifier-backed, problem-deduplicated set. On-policy verifier label / pass-rate per problem. Sealed layer: verifier + dataset rows."
- `plan/frozen-pareto-negative-synthesis.md` §Sealed confirmation: "Pre-registered NON-SEALED dev = MATH-500 L5[:40]; SEALED HOLDOUT = L5[40:134] (n=94, CPU-verified disjoint, overlap 0). Integrity gate `7+5→12 ok=True` on both seal halves."

### S6: Negative Controls + Locality Check (or the Result Is Uninterpretable)
**Pattern:** Every experiment declares (a) a negative control that must show a DIFFERENT result from the test arm to prove the probe is not dead; (b) a locality check showing the effect concentrates in the targeted mechanism and disappears when it is removed.
**Where it fired:**
- `plan/rescue-audit-protocol.md` §6: "NC1 score-shuffle: permute ranker scores → must collapse to ≈ random (proves ranker carries real signal). NC2 genuine-flip filter: rescue = truncation rescue only. NC3 budget-inversion audit: count correct@768→wrong@1280."
- RUNLOG Cycle 3 (H5 confound ablation): shuffle of the t-level (decisive negative control) gave real(4.30) < shuffled(4.83) by +0.27-0.42 nats, ruling out the input-scale artifact. "shuffle (the decisive test) decisively HURTS → the adapter reads the PER-ROW level." Also: loophole-closer (per-seq real beats best-fixed-constant) confirmed locality.
- `plan/frozen-pareto-negative-synthesis.md` §V1 sealed: "Negative control LIVE: shuffled (wrong-SC) 0.5532, joint−shuffled Δ=+0.1915 CI[0.117,0.277] (18 damaged) → the harness demonstrably CAN detect a real effect, so the null is NOT a dead probe."
- RUNLOG Cycle 11c (E-kill retest): "★ FAIRNESS arm learned(dynamics+nfe) 566.3 vs nfe-alone 544.7 → dynamics add no marginal value EVEN WHEN allowed nfe ⇒ the kill is FAIR, not a leakage-contract handicap."

### S7: Codex Independent DECIDE-Gate (Generator Never Self-Ratifies)
**Pattern:** Opus (coordinator) proposes experiments and observes results. Codex (GPT-5.5 xhigh) is the mandatory independent SELECT/DECIDE gatekeeper before any result is ratified, merged, or advanced. The two are always on separate substrates.
**Where it fired:**
- RUNLOG Cycle 11b: Codex caught a CONTROL-DIRECTION ARTIFACT in the E-kill — native_eb AUC used ascending NFE (favoring easier problems first) instead of the pre-declared descending causal direction. The "KILL STRICTLY WORSE" headline was retracted; the fair retest yielded a weaker but honest kill. "Never self-ratify; M-PCRH kill was once an artifact."
- RUNLOG Cycle 12j: Codex identified that the @768 dLLM "win" was an AR budget-truncation artifact (AR no-box 63% = truncation, not capability gap). Fixed by adding AR@2048 fair comparison.
- RUNLOG Cycle 12m: Codex RE-RAN the AUC from raw JSONL and CONFIRMED the numbers before ratification.
- `plan/operating-manual.md` §5: "isolation: generator ≠ critic ≠ selector (Opus generates/observes; Codex selects/reviews; Playwright-Pro designs/audits)."
- `plan/ai-research-conduct-principles.md` §6: "生成者、批评者、选择者用独立的上下文，绝不自我背书。真正独立的审查来自不同的推理主体。"

### S8: A Failure Must Exclude ≥2 Things (Not Just "Didn't Work")
**Pattern:** A single failed experiment must be able to rule out at least two competing explanations. Otherwise it is inconclusive and does not count as a negative.
**Where it fired:**
- `plan/ai-research-conduct-principles.md` §5: "一次失败如果不能排除 ≥2 个东西，只算 inconclusive，不算 reject." (A failure that can't exclude ≥2 things is only inconclusive, not a reject.)
- RUNLOG Cycle 2 (H4 gate): The "GATE_FAILED" verdict excluded both (a) the statistical test machinery (confirmed calibrated on synthetic H0) and (b) the data structure (localized to contiguity × autocorrelation). Two things were excluded.
- RUNLOG Cycle 4 (M-PCRH): All 3 pre-registered kill conditions had to fire simultaneously (coverage<0.60 AND oracle-rescuable<0.10 AND unary_explains≥0.80) to declare a structural kill; each excluded a different candidate explanation.
- `plan/frozen-pareto-negative-synthesis.md` §Evidence: "It excludes ≥5 plausible directions with controls + locality + matched-compute, not by failure-to-tune."

### S9: Codec Confound / Artifact-Leakage Detection
**Pattern:** Before claiming a positive, audit whether the effect could be reproduced by a simpler confound — a leaking signal from the test arm, a regime mismatch, or a codec that is itself lossy.
**Where it fired:**
- RUNLOG Cycle 15e (embedding-DDIM): N1a oracle (full oracle every step) only reached 0.72–0.84, not ~1.0 → the tied-embedding snap codec was ITSELF LOSSY (92-96% WTR at intermediate steps). N1b structural-kill was therefore codec-confounded. Honest framing required: "can't cleanly separate 'model can't land in basin' from 'snap codec lossy'."
- `plan/frozen-pareto-negative-synthesis.md` §PSC-Bridge row: "direct-oracle +5pp over native_24 is reproduced EXACTLY (acc+strata) by the final-SC leakage control → trajectory leakage, not a deployable mechanism." ARTIFACT_KILL.
- RUNLOG Cycle 11k/11l: "The dramatic 2.3%/4.3% hook was a t=1.0 WORST-CASE artifact. The shipped EntropyBound Sampler denoises in t∈[0.4,0.8]; dramatic non-observability occurs ONLY at t=1.0 (which the sampler never uses)." The strong A thesis was falsified not by a replanning, but by a regime-mismatch audit.

### S10: Budget-Truncation / AR-Fairness Confound Check
**Pattern:** When comparing two systems' accuracy, audit whether apparent differences are capability differences or budget-truncation artifacts. AR must be run at a budget where no-box rate is low (<~15%).
**Where it fired:**
- RUNLOG Cycle 12j: "AR parse-fails (63%@768) are 509/510 no_box at ~768/768 tokens (verbose AR truncates mid-derivation), 0 boxed-wrong → no intrinsic capability gap." Added AR@2048 fair arm; at @2048 AR no-box = 0.144 and accuracy = 0.836 ≈ dLLM 0.823. The win held at the fair budget.
- `plan/research-redesign-verified-wallclock-frontier.md` §v2 fix #1: "Naive eager unbatched AR is DISALLOWED as a headline. dLLM uses batched parallel-canvas decode. Report BOTH serial per-problem latency AND saturated throughput. Explicit KILL: dLLM advantage vanishes under matched AR batching."
- RUNLOG Cycle 12k: "@768 acc-gap correctly DROPPED as truncation artifact."

### S11: Cheap-Decisive-First Experiment Design
**Pattern:** The first experiment under any lead must be cheap (hours not days), maximally decisive (a clean GO/NO-GO), and consume nothing from the sealed test set.
**Where it fired:**
- `plan/research-redesign-verified-wallclock-frontier.md` §2-week plan: "Day 1: freeze protocol. Day 2 (CHEAP — existing 984 traces): estimate pass@1/2/3. Days 3–5 (decisive): matched AR/dLLM frontier on MATH-L5 + AIME-2024. Kill criteria by end of Day 5."
- `plan/research-redesign-equivalence-class.md` §Cheapest decisive first experiment: "For 100–200 prompts across GSM8K + MATH + code: reference pool R_x; decisive if reference-token rankings FLIP across correct references while verifier accuracy is unchanged."
- RUNLOG Cycle 3 (before H5 3-seed run): 1-seed plumbing pilot (NOT the falsifier) dispatched first to validate t-threading, sealed bank, and capacity match; Codex diff review BEFORE the 3-seed run.

### S12: Rigor-Review-Before-Build Gate
**Pattern:** Before any worktree subagent begins building an experiment, a Codex rigor-review must issue SOUND / SOUND-WITH-FIXES / NEEDS-REDESIGN. The build does not start without this gate.
**Where it fired:**
- RUNLOG Cycle 10: "★ Codex rigor-review-before-build. Verdict: SOUND-WITH-FIXES." Identified the dead-on-arrival make-or-break flaw: the unconditional question was a near-oracle trivial control, reframing to CONDITIONAL (within-C) before any code was written.
- RUNLOG Cycle 11i: "Froze the Codex-hardened build contract plan/saturation-experiment-protocol.md (Pro Q1 design + Codex's 8 must-fixes + sharpened non-self-defeating claim + 2 separate falsifiers)."
- RUNLOG Cycle 14: "Pro 扩展 novelty+formal design = plan/gpt55pro-G4-design-2026-06-28.md (FROZEN BUILD CONTRACT)."

### S13: Kill Criterion Is Itself a Success (Redesign When Evidence Contradicts)
**Pattern:** A clean, well-controlled kill of a hypothesis is a scientific positive, not a project failure. When both leads die, the program pivots (Pro 扩展 redesign) rather than trying to rescue a dead direction.
**Where it fired:**
- RUNLOG Cycle 11c: "VERDICT: KILL E (clean, fair, well-controlled negative = SUCCESS) → A is the LEAD spine."
- RUNLOG Cycle 11l: "PROGRAM STATE: both leads under-delivered strong claims — E KILLED, A WEAKENED/FALSIFIED. Per the science kernel (redesign when evidence contradicts) → PROGRAM REDESIGN."
- `plan/ai-research-conduct-principles.md` §8: "一个被实验否定的想法，无论多优雅、多符合第一性原理、已经投入多少，都必须砍掉。"
- `plan/frozen-pareto-negative-synthesis.md` §Why non-obvious: "It excludes ≥5 plausible directions with controls + locality + matched-compute, not by failure-to-tune."

---

## 4. Reusable Artifacts — Quoted Templates and Protocol Blocks

### 4a. The Invariant Science Kernel (from `plan/operating-manual.md` §5)

```
Falsify-before-build (ship the kill-experiment WITH the idea) ·
score-up ≠ mechanism (require negative control + locality) ·
eval/test/baseline are a SEALED layer, never changed mid-run ·
one variable per probe ·
isolation: generator ≠ critic ≠ selector ·
experiment has absolute veto over elegance ·
every experiment pre-declares
{hypothesis, falsifier, acceptance, negative control, locality check,
 reproducible evidence, recorded commands+exit codes} ·
when evidence contradicts the direction, REDESIGN the program, don't defend it.
Negative results / eliminated confounds / killed directions = SUCCESS.
```
File: `/home/lingxufeng/huggingface/plan/operating-manual.md` §5

### 4b. Pre-Declared Falsifier Block (from `plan/frozen-pareto-negative-synthesis.md`)

```markdown
## ★ PRE-REGISTERED FALSIFIER (frozen before the sealed confirmation; anti-p-hacking)
The synthesis is BROKEN by: **any fixed-generator (no-weight-change) intervention that beats
native AND always-deepen-to-matched-mean by ≥2pp verified accuracy at matched NFE AND matched
wall-clock, with the negative/locality/anti-verifier-surface controls intact, on a sealed hard
set (L5-holdout or AIME).** No such intervention has been found across six attempts.
```
File: `/home/lingxufeng/huggingface/plan/frozen-pareto-negative-synthesis.md` §PRE-REGISTERED FALSIFIER

### 4c. Codex-Hardened Acceptance/Kill Block (from `plan/rescue-audit-protocol.md`)

```markdown
## v2.C Frozen acceptance / kill (revised)
- **PAPER (E is the lead method) iff,** on the CONDITIONAL (within-C) matched-NFE / AUC metric:
  learned ranker beats the **best non-learned control** with **paired problem-cluster bootstrap 95%
  CI lower bound > 0**, AND a meaningful effect size = recovers **≥ 20% of the oracle-within-C
  recoverable uplift**, AND the truncation-failure fraction on the reallocated set is **at least halved**.
- **KILL (E is engineering → fall back to A) iff** any trivial/non-learned control (esp.
  final-entropy or length) matches the learned ranker **within the paired-bootstrap CI**, OR the
  Phase-0 gate fails (<~25 positives). A KILL here is a SUCCESS per the goal (clean negative).
```
File: `/home/lingxufeng/huggingface/plan/rescue-audit-protocol.md` §v2.C

### 4d. K-Saturation Criterion (from `plan/saturation-experiment-protocol.md`)

```markdown
## 6. K-saturation criterion — both required for SATURATED
SATURATED iff **(K20→30 improvement) < 25% of (K1→10 improvement)** AND
**absolute ΔTop10(K20→30) < 0.02**; else INCONCLUSIVE (cannot claim "multi-ref fails"
while the curve climbs).
```
File: `/home/lingxufeng/huggingface/plan/saturation-experiment-protocol.md` §6

### 4e. The 11-Point Science Protocol (from `plan/ai-research-conduct-principles.md` §4)

```
做科研时遵守:
1. 先把现象/失败转成可观测的机制变量，再改代码。没有可测的"为什么"，不动手。
2. 每个假设自带 ≥1 个会推翻它的 falsifier 和 ≥1 个竞争解释。选最干净可证伪的，不选最易实现的。
3. 检索/记忆/直觉不是证据，只能提问。能裁决真假的只有受控实验的可重放结果。说"完成"不算完成。
4. 分数涨 ≠ 机制成立。eval/test/baseline 永不改。任一作弊信号→整体作废。警惕自己把 bug 说成洞见。
5. 声称越强，控制越多：配方→机制(+负控+locality+反事实)→论文(+holdout+跨目标+novelty)。
6. 一次只动一个变量，预声明成功信号。纯调参不支撑机制结论。
7. 失败要排除 ≥2 个东西才算负例，并记录"错解为何曾可信"。
8. 生成/批评/选择相互隔离，不自我背书。候选阶段不看答案。
9. 昂贵实验前固定 env/命令/metric/split。缺工具 fail-closed，不用 mock 冒充。
10. 最少活动部件。先跑通一个可重放的最小完整周期再扩张。
11. 实验结果对理论优雅有绝对否决权。每个想法上手前先写死死刑条件；实验否定时无条件砍。
```
File: `/home/lingxufeng/huggingface/plan/ai-research-conduct-principles.md` §4

### 4f. Negative-Control Battery Template (from `plan/rescue-audit-protocol.md` §6)

```markdown
## Negative controls & locality (or the result is uninterpretable)
- **NC1 score-shuffle:** permute the learned ranker's scores across problems → must collapse
  to ≈ random (proves the ranker carries real signal, not a label leak).
- **NC2 genuine-flip filter:** rescues must be TRUNCATION rescues. Stratify rescued problems
  by B0 failure mode; a "rescue" of a problem that was `genuine-wrong-answer@B0` (emitted a
  wrong \boxed{}, then correct @B1) is stochastic noise, NOT budget.
- **NC3 budget-inversion audit:** count correct@B0→wrong@B1. If inversions ≈ rescues,
  "budget helps" is noise not signal.
- **LOCALITY:** the learned ranker's advantage must concentrate on no-box/hit-cap problems;
  show the gain vanishes when those strata are removed.
```
File: `/home/lingxufeng/huggingface/plan/rescue-audit-protocol.md` §6

### 4g. Evidence Emission Template (from `plan/rescue-audit-protocol.md` §7)

```markdown
## Reproducible evidence to emit (the 验收 artifact)
- `outputs/.../traces_*.jsonl` (per problem×seed×budget; features+correct+NFE)
- `outputs/.../paired_table.csv` (problem, correct@B0, correct@B1, NFE@B0, NFE@B1, B0 features)
- `outputs/.../matched_compute_curves.json` (Acc vs total-NFE per policy + bootstrap CIs)
- `outputs/.../VERDICT.md` (the decision table: each acceptance/kill criterion with number+CI)
- All commands + exit codes appended to RUNLOG; git branch/commit recorded; seeds fixed;
  checkpoint shard SHA integrity asserted at load.
```

---

## 5. Command/Skill Candidates

| Skill name | One-line purpose | Trigger | Engine |
|---|---|---|---|
| `/exp-register` | Write and freeze the pre-registration block (H, falsifier, acceptance, NCs, locality, budget cap) before any sealed data is seen | Whenever a new experiment is proposed | Opus-draft → Codex-APPROVE |
| `/substrate-gate` | Run checkpoint SHA verification + `7+5→12` sanity before any probe; catch corrupt shards | Session start, before every heavy experiment | Opus (bash probe) |
| `/measure-first` | Run a 3-problem timing probe; estimate full-sweep wall-clock; produce go/kill + extrapolation artifact | Before any GPU sweep ≥1h | Opus (bash probe) |
| `/rigor-review` | Codex adversarial review of an experiment design: find dead-on-arrival confounds, control-direction bugs, trivial-control dominance, power problems | Before dispatch to worktree subagent | Codex (GPT-5.5 xhigh) |
| `/decide-gate` | Independent Codex adjudication of a completed result: check for artifacts, rerun key numbers, issue RATIFIED / WIN-NEEDS-FIX / KILL-NEEDS-FAIR-RETEST | After any result lands | Codex (GPT-5.5 xhigh) |
| `/bank-negative` | Package a clean kill into a banked structural negative: scope the claim, pre-declare what would break it, document the excluded hypotheses | When ≥2 arms consistently null | Opus + Codex |
| `/codec-audit` | Check whether an apparent positive or negative is a codec-confound, regime-mismatch, or leakage artifact | When a control arm fails to reach expected ceiling | Opus + Pro 扩展 |
| `/budget-confound-check` | Verify that system A's accuracy gap over system B is not a budget-truncation artifact; mandate a fair-budget arm (no-box rate <15%) | Before citing an accuracy comparison across model families | Opus (bash analysis) |

---

## 6. Failure Modes This Project Hit — and the Guard That Caught Each

| Failure | What happened | Guard that caught it |
|---|---|---|
| **Silent checkpoint corruption** | Shard `model-00001-of-00011.safetensors` digit-token rows zeroed ~91% (partial download); all prior results (H5, M-PCRH, SFT) contaminated. RUNLOG Cycle 6–7. | Substrate integrity gate (`7+5→12`; shard SHA comparison to published hash). `plan/operating-manual.md` Lesson #1. |
| **Diffusion loss as proxy** | SFT halved diffusion loss with zero task accuracy gain. Led to premature "SFT validated" claims. RUNLOG Cycle 7b. | Switching to generation/verifier metrics; declaring diffusion-loss diagnostic-only. `plan/operating-manual.md` Lesson #2. |
| **Regime-mismatch artifact (t=1.0 outside sampler band)** | The 2.3%/4.3% reference non-observability headline was real at t=1.0 but the shipped sampler never uses t=1.0 (band t∈[0.4,0.8]). At fair regime, Top10 recovered to 0.99. RUNLOG Cycle 11k/11l. | Codex must-fix #2: "sampler-matched t PRIMARY, t=1.0 worst-case only." The saturation protocol's PRIMARY metric was the sampler-matched distribution; t=1.0 results were explicitly SECONDARY. |
| **Budget-truncation confound (AR@768)** | AR at 768-token budget had 63% no-box rate (mid-computation truncation), inflating the apparent dLLM accuracy advantage. RUNLOG Cycle 12i/12j. | Codex WIN-NEEDS-FIX audit; added AR@2048 fair-budget arm; mandatory threshold: "no-box <~15% for a headline accuracy comparison." `plan/research-redesign-verified-wallclock-frontier.md` §v2 fix #1. |
| **Control-direction artifact in ranker evaluation** | native_eb control (best non-learned control in E-kill) was scored with ASCENDING NFE (easier-first), inverting its causal meaning. The "STRICTLY WORSE" headline was invalid. RUNLOG Cycle 11b. | Mandatory Codex DECIDE-gate before ratification. Never self-ratify; Codex re-ran the AUC with pre-declared causal direction. |
| **MC variance masquerading as gate failure** | H4 validity gate fwer=0.142 at r_null=200 looked like "gate inflated." A team of 7 agents spent cycles diagnosing a bug that did not exist (the gate was Hemerik-Goeman exact). The real problem was r_null too small. RUNLOG Cycle 2. | Fix-verify focused agent with the correct mathematical framing: power analysis showed P(pass at r=200)=0.21 even for a PERFECT test; the 0.065 bar needed r≥1000. Never commit to "bug exists" before quantifying MC variance. |
| **Dead-on-arrival method claim (trivial-control dominance)** | The unconditional E question (learned ranker vs uniform-bigger-budget) was dead-on-arrival because `no_box@cap` ≈ oracle trivial control. All experiments would have been uninterpretable. RUNLOG Cycle 10. | Codex RIGOR-REVIEW-BEFORE-BUILD issuing SOUND-WITH-FIXES + CONDITIONAL REFRAME before any code was written. |
| **Codec-confound in structural-kill claim** | N1b (oracle-to-basin) structural kill for embedding-DDIM was potentially confounded by N1a's lossy codec (WTR 0.92-0.96 even at oracle). The kill could be "codec lossy" not "model can't reach basin." RUNLOG Cycle 15e. | Honest framing from the Pro 扩展 codec-confound resolution: separated "codec lossy" from "field unreachable" and added N2 (codec-free arm). `plan/gpt55pro-N2-codecfree-2026-06-28.md`. |
| **In-session background jobs dying on CC exit** | Cycle 1: H4 and SFT jobs dispatched as non-detached children died when CC exited. Lost ~35min of H4 computation. RUNLOG Cycle 1 restart resilience test. | setsid-detached dispatch + tracked waiter (run_in_background marker) that writes DONE file + armed ScheduleWakeup on PID. `plan/operating-manual.md` §2 safety rules. |
| **PID reuse authorizing wrong kill** | A recorded PID might recycle to a co-tenant (JasonF/openpi pi0; JasonF/gaussian-splatting 3dgs) with cwd outside the project. RUNLOG Cycles 12d–12e. | PID reuse guard: before any kill, re-verify LIVE process cmd + cwd + start-time against registry. Ownership test: cwd under project AND cmd matches job patterns. "A recorded PID NEVER authorizes a kill." `plan/operating-manual.md` §2. |
| **Overclaiming mechanism from a 1-seed pilot** | H5 1-seed (seed 42) gave B-A = -0.41 nats. This was preliminary and NOT the falsifier. "Skeptical flags (do not over-claim from 1 seed)." RUNLOG Cycle 3. | Mandatory 3-seed run for falsifier statistics. Codex review of the diff BEFORE the 3-seed run. The 1-seed pilot was explicitly labeled "NOT the falsifier." |

---

## 7. Top-3 Highest-Value Takeaways

### T1: The Measure-First + Sealed-Split Pair Is the Core Anti-Waste Loop
The most expensive failed experiments here would have been caught much earlier by two simple gates: (1) a 3-problem timing probe that extrapolates to the full sweep and kills the job on 2× overrun, and (2) a non-sealed dev evaluation (or a cheap synthetic oracle) that checks whether the ceiling is healthy and the confounds are absent before spending GPU time on the sealed set. In this project, the L=256 budget confound (Cycle 15) was caught by a 32-problem dev smoke that ran in minutes; the H4 gate inflation was diagnosed by a synthetic-H0 inline probe in Cycle 2. By contrast, the saturation experiment (Cycle 11i–11l) ran ~4.3 GPU-hours to falsify A-strong, which required the full saturated-K sweep on the sealed set — an unavoidably expensive but correctly scoped experiment because all cheaper checks had already passed. The rule is: exhaust cheap probes (smoke, synthetic, dev, oracle-bound) before spending sealed compute.

### T2: Diffusion Loss Is Systematically Deceptive — The Right Metric Is Verifier-Based
This lesson fired first (SFT halved diffusion loss, zero task accuracy gain; Cycle 7b), then recurred in A's equivalence-class work (reference-token collapse at t=1.0 was a worst-case regime artifact; sampler-band agreement was high), and again in the embedding-flow campaign (N1a oracle codec WTR 0.92-0.96 = codec lossy, not model incapable). The general form: any metric that scores a FIXED reference or a teacher-forced target under a masked-diffusion corruption is measuring a proxy that can diverge radically from generation quality. The only trustworthy metrics here are: exact-match via an independent verifier (math_verify, code-exec), verified-accuracy (free generation), or paired problem-level bootstrap CIs over generation output. Every experiment that used diffusion loss as a success signal had to be re-done or retracted.

### T3: Independent Adjudication Catches Artifacts That Self-Ratification Cannot
Three independent Codex DECIDE-gate interventions found result-invalidating bugs that would have propagated into the paper: the control-direction artifact in the E-kill (Cycle 11b, the "STRICTLY WORSE" claim was retracted and replaced with a weaker but honest kill); the AR budget-truncation confound (Cycle 12j, the @768 accuracy gap was truncation not capability); and the codec-confound in the N1b structural kill (Cycle 15e, the snap codec was itself lossy). In all three cases Opus-as-coordinator could not have caught these because it was in the same context as the experiment. The multi-engine isolation — Opus proposes + observes, Codex selects/adjudicates, Pro 扩展 designs/audits — is the structural reason the eventual ratified positive (wall-clock frontier) and the banked structural negative (frozen-Pareto) are defensible. Any experiment-rigor skill that omits independent adjudication will have blind spots in exactly the places the generator is most confident.
