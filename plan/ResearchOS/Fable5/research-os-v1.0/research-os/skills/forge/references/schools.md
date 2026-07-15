# The 14 methodology schools — the generative palette

> Lenses that PRODUCE candidates. Pick the 2–3 whose soul-question matches the failure signature, plus
> **always one rival** — the rival is where the non-obvious candidate comes from. Never run all 14 as a
> checklist. Schools = *how to think*; types (`research-types.md`) = *what output* — orthogonal axes.

| School | Soul-question | Fits a signature of | Typical rival |
|---|---|---|---|
| **Modeling-Object-Shift** | are we modeling the wrong object? | equivalence-split / residual / trajectory signals | Back-to-Basics |
| **Back-to-Basics** | the simplest correct definition once we delete history? | over-complex pipeline; "is X necessary?" | Bitter-Lesson |
| **Bitter-Lesson** | what keeps winning as compute/data/model scale? | failure family changes with scale; hand-priors | Geometric |
| **Data-Centric** | is the data definition/coverage wrong, not the model? | coverage holes / label inconsistency | Modeling-Object-Shift |
| **Measurement/Benchmark** | what does the leaderboard reward or hide? | benchmark average misleading | Data-Centric |
| **Geometric/Symmetry** | what invariant/group/manifold should the architecture respect? | invariant-break under transforms | Bitter-Lesson |
| **Causal/Invariance** | which features are stable across environments vs spurious? | cross-environment prediction flips | Data-Centric |
| **Falsification-First** | the cheapest experiment that kills my idea? | (always — the kernel; lives in `/prereg`) | — |
| **Empirical-Debugging** | where exactly does the gain come from? | (always — sanity before theory; `/autopsy` step 1) | — |
| **Abstraction-Compression** | are these many methods secretly one variable-change? | residual structure after a strong baseline | Empirical-Debugging |
| **Counterinduction** | what does the community assume — what if the reverse? | everyone chases one paradigm | Bitter-Lesson |
| **Tooling/Infrastructure** | why can't people study this — missing tool/benchmark? | new infra unlocks a new experiment | Measurement |
| **Failure-Mode-Taxonomy** | how many KINDS of failure; same mechanism? | mixed failure population | Causal |
| **Systems-Constraint** | the real hardware/latency/throughput bottleneck? | elegant-on-paper, dies on wall-clock | Bitter-Lesson |
| **Human-Aesthetic** | few, sharp, restateable, killable, generative, namable? | (the He-bar — `taste.md` §4) | — |

## The 10-question generator (surface the omitted structure — run on problems AND on results)
1. **Object** — what does the field truly model; is it the object the task needs?
2. **Residual** — predict the correction from the current state, not the answer directly?
3. **Support** — does the model know when it left the training semantic support?
4. **Invariant** — which features are stable across environments vs train-set spurious?
5. **Geometry** — what symmetry / graph / manifold structure does the space have?
6. **Compression** — does the objective compress away exactly what reliability needs?
7. **Trajectory** — wrongly modeled as endpoint-prediction; should it be a process?
8. **Evidence** — what does the benchmark reward; does it reward reward-hacking?
9. **Scale** — does it keep working as data/model/compute grow?
10. **Kill** — what minimal experiment proves the idea wrong?

`/autopsy` re-runs the relevant questions on every RESULT — the generator metabolizes evidence, not just priors.
