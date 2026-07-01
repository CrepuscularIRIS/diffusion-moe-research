# Methodology-OS Rigor Layer — Community Checklist Extraction (2026-06-29)

> Purpose: Ground our anti-reward-hacking gates in EXTERNAL community standards (not self-invented prose).
> Sources: ml-checklist/index.html (Lones arXiv:2108.02497), paper-quality-checklist/docs/*, artifact-evaluation/docs/checklist.md,
> aclrollingreview/responsibleNLPresearch.md + authorchecklist.md, and our own gates in plan/research-operating-system.md
> + plan/methodology-harvest.md §2.

---

## 1. Concrete Checklist Items Worth Lifting Verbatim

### 1A. Leakage / Contamination

> "leakage of information from the test set into the training process is a [critical problem]… carrying out
> feature selection before partitioning the data, and using the whole data set to carry out variable
> scaling" are examples of leakage. "only use this independent test set once to measure the generality."
> — ml-checklist/index.html (Lones §, lines 152–317)

> "No temporal or spatial leakage in splits: preprocessing fitted on train only."
> — paper-quality-checklist/docs/statistical-test-checklist.md §10 ML-Specific Pitfalls

> "Hyperparameters tuned on validation set; test set touched exactly once."
> — paper-quality-checklist/docs/statistical-test-checklist.md §10

> "No test set used for hyperparameter tuning."
> — paper-quality-checklist/docs/venue-checklists.md §3.1 NeurIPS

> "Dataset splits do not leak between train and test (especially for video-derived frames)."
> — paper-quality-checklist/docs/venue-checklists.md §3.6 CVPR/ICCV/ECCV

> "Spatial leakage: nearby road segments, intersections, or detectors are not split across train/test."
> — paper-quality-checklist/docs/statistical-test-checklist.md §9 (also §2.1 ACM SIGSPATIAL)

> "if you optimise the hyperparameters or features used by a model, you should ideally carry this out
> inside the cross-validation loop … doing hyperparameter optimisation and feature selection as an
> extra loop inside the cross-validation loop."
> — ml-checklist/index.html (Lones, lines 423–434)

---

### 1B. Baseline Fairness

> "Baselines are fair, current (≤ 3 years for fast-moving fields), and appropriate for the venue."
> — paper-quality-checklist/docs/universal-checklist.md §Results and Claims

> "Comparison baselines use same feature set, preprocessing, and tuning budget."
> — paper-quality-checklist/docs/statistical-test-checklist.md §10 ML-Specific Pitfalls

> "Research: ablation isolates each component; baselines are tuned under the same budget."
> — paper-quality-checklist/docs/venue-checklists.md §2.2 KDD

> "Strong recent baselines are included; a neural network beating a 2015 method is insufficient."
> — paper-quality-checklist/docs/venue-checklists.md §1.2 TR Part C

> "Comparison baselines include the best published result on each benchmark under comparable settings."
> — paper-quality-checklist/docs/venue-checklists.md §3.3 ICML

> "State-of-the-art claims use identical pre-training data and resolution."
> — paper-quality-checklist/docs/venue-checklists.md §3.6 CVPR/ICCV/ECCV

---

### 1C. Seed / Variance / CI

> "Results reported as mean ± std across ≥ 3 seeds, not best run."
> — paper-quality-checklist/docs/statistical-test-checklist.md §10 ML-Specific Pitfalls

> "Empirical papers: ≥3 random seeds per dataset; mean ± std or error bars on all main results."
> — paper-quality-checklist/docs/venue-checklists.md §3.1 NeurIPS

> "Empirical claims: confidence intervals over ≥3 seeds — not single-run numbers."
> — paper-quality-checklist/docs/venue-checklists.md §3.2 ICLR

> "Main results include uncertainty (CI, SE, std across seeds/folds) and effect size where applicable."
> — paper-quality-checklist/docs/universal-checklist.md §Results and Claims

> "when a result is reported, it should be clear if it is from a single run, the max across N random
> seeds, the average, etc. When reporting a result on a test set, be sure to report a result of the same
> model on the validation set (if available)."
> — aclrollingreview/responsibleNLPresearch.md §C3

> "Every result reports effect size, CI, and p-value together."
> — paper-quality-checklist/docs/statistical-test-checklist.md §11 Final Statistical Gate

> "p-value without effect size is an incomplete result."
> — paper-quality-checklist/docs/statistical-test-checklist.md §8 Reporting Standards

---

### 1D. Reproducibility / Artifact Provenance

> "Package versions, software versions, random seeds, hardware, and compute budget are documented
> where relevant. Model checkpoints, prompts, hyperparameters, and preprocessing scripts are recorded.
> Tables and figures can be regenerated from the documented analysis workflow."
> — paper-quality-checklist/docs/universal-checklist.md §Reproducibility

> "The total computational budget (e.g., GPU hours), and computing infrastructure used … this should
> include information about all experiments, not just the final runs that led to the results presented."
> — aclrollingreview/responsibleNLPresearch.md §C1

> "Run-time state: Is your artifact sensitive to run-time state (cold/hot cache, network/cache contentions)?"
> — artifact-evaluation/docs/checklist.md §Checklist

> "Do not forget to mention the maximum allowable variation of empirical results!"
> — artifact-evaluation/docs/checklist.md §Evaluation and expected results

> "Policy checkpoints, environment code, and random seeds available for reproducibility."
> — paper-quality-checklist/docs/venue-checklists.md §3.8 CoRL

> "Publicly available? Will your artifact be publicly available? … author-created artifacts … will
> receive the ACM 'artifact available' badge only if they have been placed on a publicly accessible
> archival repository such as Zenodo, FigShare or Dryad. A DOI will then be assigned."
> — artifact-evaluation/docs/checklist.md §Checklist (Archived?)

> "Report which dataset was used to determine the hyperparameters. Unless under special circumstances,
> hyperparameters should not be tuned on the evaluation (held-out) dataset."
> — aclrollingreview/responsibleNLPresearch.md §C2

---

### 1E. Statistical Test Validity

> "Write H0 and H1 before running any test. State the estimand explicitly."
> — paper-quality-checklist/docs/statistical-test-checklist.md §1 Formulate Before Testing

> "Exploratory analyses are reported as exploratory, not confirmatory."
> — paper-quality-checklist/docs/statistical-test-checklist.md §1

> "The full family of planned hypotheses is declared before testing (for multiple-comparison correction)."
> — paper-quality-checklist/docs/statistical-test-checklist.md §1

> "One-tailed tests are pre-registered or mechanistically justified, not chosen after seeing results."
> — paper-quality-checklist/docs/statistical-test-checklist.md §1

> "Holm [correction]: Default for any family of hypotheses; always more powerful than Bonferroni.
> BH-FDR: Large exploratory family (> 10 tests); discovery setting."
> — paper-quality-checklist/docs/statistical-test-checklist.md §6 Multiple Comparison Corrections

> "5×2CV paired t-test (Dietterich 1998) — correct when sharing training data."
> — paper-quality-checklist/docs/statistical-test-checklist.md §4.12 ML Model Comparison

> "Did not use an unpaired t-test on fold metrics when folds share training data."
> — paper-quality-checklist/docs/statistical-test-checklist.md §4.12

> "Post-hoc power is NOT reported for non-significant results — report CI width instead."
> — paper-quality-checklist/docs/statistical-test-checklist.md §7 Power and Sample Size

> "Every causal claim is backed by design, identification assumptions, and sensitivity checks."
> — paper-quality-checklist/docs/statistical-test-checklist.md §11 Final Statistical Gate

> "Significance testing for metric differences uses bootstrap resampling (p < 0.05)."
> — paper-quality-checklist/docs/venue-checklists.md §3.7 ACL/EMNLP/NAACL

---

### 1F. Ablation Sufficiency

> "Sensitivity, ablation, or robustness checks are included when the main result depends on modeling choices."
> — paper-quality-checklist/docs/universal-checklist.md §Method Validity

> "Alternative explanations for the main result are considered and addressed."
> — paper-quality-checklist/docs/universal-checklist.md §Method Validity

> "Ablation study justifies each major design choice."
> — paper-quality-checklist/docs/venue-checklists.md §3.1 NeurIPS

> "Ablation justifies each architectural or training decision."
> — paper-quality-checklist/docs/venue-checklists.md §3.2 ICLR

> "Negative, null, or mixed results are reported — not selectively hidden."
> — paper-quality-checklist/docs/universal-checklist.md §Results and Claims

> "No cherry-picked qualitative examples; include failure cases in supplement."
> — paper-quality-checklist/docs/venue-checklists.md §3.6 CVPR/ICCV/ECCV

> "Did you use statistical tests during model comparison? … if your training algorithm is stochastic,
> multiple repeats using the same data … case you later use a statistical test to compare models."
> — ml-checklist/index.html (Lones, lines 630–642)

---

## 2. Mapping Table: Our Gates → External Community Standards

| Our Gate | External Community Item(s) That Ground It | Source File:path |
|---|---|---|
| `/reward-hack-audit` | "Results reported as mean ± std across ≥ 3 seeds, not best run" · "Comparison baselines use same feature set, preprocessing, and tuning budget" · "Negative, null, or mixed results are reported — not selectively hidden" | statistical-test-checklist.md §10; universal-checklist.md §Results |
| `/exp-verify` | "Do not forget to mention the maximum allowable variation of empirical results!" · "Is your artifact sensitive to run-time state (cold/hot cache, network/cache contentions)?" · "Tables and figures can be regenerated from the documented analysis workflow" | artifact-evaluation/docs/checklist.md §Evaluation; universal-checklist.md §Reproducibility |
| `/baseline-champion` | "Baselines are fair, current (≤ 3 years), and appropriate" · "Comparison baselines use same feature set, preprocessing, and tuning budget" · "ablation isolates each component; baselines are tuned under the same budget" · "Strong recent baselines are included; a neural network beating a 2015 method is insufficient" | universal-checklist.md §Results; statistical-test-checklist.md §10; venue-checklists.md §KDD, §TR-C |
| `/bank-negative` | "Negative, null, or mixed results are reported — not selectively hidden" · "Alternative explanations for the main result are considered and addressed" · "Reflect on the scope of your claims, e.g., if you only tested your approach on a few datasets" | universal-checklist.md §Results and §Method Validity; responsibleNLPresearch.md §A1 |
| `/claim-evidence-matrix` | "The discussion does not claim causality from association unless the design supports causal inference" · "Every causal claim is backed by design, identification assumptions, and sensitivity checks" · "p-value without effect size is an incomplete result" · "Each table or figure answers a stated research question" | universal-checklist.md §Results; statistical-test-checklist.md §8 and §11 |
| `preregister` (sealed-holdout + timestamp) | "Write H0 and H1 before running any test. State the estimand explicitly" · "The full family of planned hypotheses is declared before testing" · "One-tailed tests are pre-registered or mechanistically justified, not chosen after seeing results" · "Hyperparameters tuned on validation set; test set touched exactly once" | statistical-test-checklist.md §1; statistical-test-checklist.md §10 |

---

## 3. What the Community Checklists Have That Our Gates Don't (Gaps)

1. **Formal H0/H1 notation required BEFORE experiments.** Our `/preregister` binds chronology and seals holdout, but does not require authors to write a formal null hypothesis with stated estimand. The statistical-test-checklist §1 is specific: name the estimand (mean, AUC, ΔF1, rate ratio) before you start.

2. **Multiple-comparison correction protocol.** Our gates don't specify which correction to use when reporting multiple results. Community standard: Holm always for any family; BH-FDR only for exploratory families > 10 tests. We run many ablations — this needs a rule.

3. **Paired inference for ML model comparison.** Our `/reward-hack-audit` checks per-example breakdowns but doesn't mandate paired-inference tests (5×2CV Dietterich, McNemar, DeLong). The community standard is explicit: "Did not use an unpaired t-test on fold metrics when folds share training data."

4. **Maximum allowable variation of empirical results (tolerance band).** artifact-evaluation explicitly requires declaring the accepted variance ceiling for reproduction. Our gates check that a run completed but don't seal a tolerance band against which a later reproducer validates.

5. **DOI-anchored artifact archival for reproducibility badge.** artifact-evaluation requires Zenodo/FigShare DOI for an "artifact available" badge; GitHub alone is insufficient. Our provenance harness records hashes but doesn't specify an archival endpoint.

6. **Power analysis / sample size declaration BEFORE experiments.** Community standard (stat-test §7): power analysis is pre-study; post-hoc power on null results is banned (report CI width instead). Our loop doesn't formally require power/sample-size justification before dispatch.

7. **Explicit "exploratory vs confirmatory" labeling.** stat-test §1 requires that exploratory analyses be labeled exploratory. Our current gates treat all results symmetrically — no mechanism forces the proposer to declare whether a hypothesis was pre-registered or post-hoc.

---

## 4. Top-5 Highest-Value Liftable Items for the Anti-Reward-Hacking Layer

**#1 — "Results reported as mean ± std across ≥ 3 seeds, not best run."**
Source: paper-quality-checklist/docs/statistical-test-checklist.md §10
Why: The single most common reward-hack in ML. Directly binds `/reward-hack-audit` to a minimum-seed threshold and reporting format. Zero ambiguity.

**#2 — "Write H0 and H1 before running any test. State the estimand explicitly."**
Source: paper-quality-checklist/docs/statistical-test-checklist.md §1
Why: Forces preregistration to be formal, not prose-narrative. Closes the gap where a pre-reg says "we expect improvement" but the estimand (ΔF1 on which subset, under what null) is unspecified — allowing post-hoc framing.

**#3 — "Comparison baselines use same feature set, preprocessing, and tuning budget."**
Source: paper-quality-checklist/docs/statistical-test-checklist.md §10
Why: The canonical formulation of baseline fairness. Gives `/baseline-champion` a concrete falsification criterion: the adversary checks that the champion baseline had equal tuning budget and identical preprocessing, not just an equal epoch count.

**#4 — "Negative, null, or mixed results are reported — not selectively hidden."**
Source: paper-quality-checklist/docs/universal-checklist.md §Results and Claims
Why: The community's standard anti-cherry-pick clause. Grounds `/bank-negative` in a publication-venue norm, not just internal discipline. Makes "we killed this hypothesis" a required disclosure, not optional housekeeping.

**#5 — "Did not use an unpaired t-test on fold metrics when folds share training data."**
Source: paper-quality-checklist/docs/statistical-test-checklist.md §4.12 ML Model Comparison
Why: Extremely specific anti-hack for exactly how ML practitioners over-report significance — pooling fold scores from shared-data cross-validation as if they were independent draws. Binding this to `/reward-hack-audit` closes a gap none of our current internal guards names explicitly.

---

## Appendix: Mapping to methodology-harvest.md §2 Threat Taxonomy

| Harvest §2 Threat | Closest Community Checklist Item | How to wire |
|---|---|---|
| #1 Forgery of completion (self-report DONE ≠ DONE) | AE checklist: "maximum allowable variation of empirical results" + artifact provenance DOI | `/exp-verify` binds to tolerance band + hash |
| #2 Aggregate-metric masking (per-file regression hidden) | stat-test §10: "Results reported as mean ± std … not best run" + "AUPRC not just AUROC for rare events" | `/reward-hack-audit` requires per-example breakdown |
| #3 Supervision-token leakage (AB-5 shuffle) | universal-checklist §Method Validity: "Sensitivity, ablation, or robustness checks … when main result depends on modeling choices" | `/token-shuffle-ablation` — label it a community-standard robustness check |
| #4 Silent no-op (intervention never fired) | AE checklist: "Run-time state: Is your artifact sensitive to run-time state?" | `/exp-verify` anti-no-op log_assertion |
| #5 Cache/leakage (stale cache, not clean run) | AE checklist: "Do not forget to mention the maximum allowable variation" + universal-checklist §Reproducibility: "Tables and figures can be regenerated" | `/exp-verify` clean-reproduce step |
| #6 Diagnostic-as-success (invalid proxy metric) | stat-test §11: "Every hypothesis has a matched test or model with stated H0 and H1" | preregister forces metric declaration before run |
| #7 Strong-score-masks-weak-mechanism (min-form) | universal-checklist: "Claims avoid words such as first, novel, robust, safe, causal, or generalizable unless the evidence directly supports them" | `/claim-evidence-matrix` enforces per-claim evidence TYPE |
| #8 Absence-as-confirmation | universal-checklist: "Alternative explanations for the main result are considered and addressed" | `/bank-negative` evidence-debt field |
