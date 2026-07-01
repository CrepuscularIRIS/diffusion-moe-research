# GPT-5.5 Pro (Pro 扩展) design — O1 = Parallel Frontier Certificate (PFC) Training — 2026-07-01

> Pro designed the object (9m50s thinking); Opus packaged (verbatim from screenshots + snapshot).
> NOT self-certified — eligibility comes ONLY from /object-shift-audit. Arbor node 5.13.
> Chat: chatgpt.com/c/6a44cb4d-2654-83ea-9c7b-9d7686b8e4b5

## Recommendation: train Parallel Frontier Certificates rather than "parallel CoT"

## 1. O1 object: Parallel Frontier Certificate

Object type: mostly **training-data restructuring + loss modification**, with a tiny optional architecture tweak.

**Parallel Frontier Certificate training**: a supervised masked-diffusion training scheme where the model
learns to fill a compact, dependency-layered reasoning canvas: independent subcomputations occupy separate
cells in the same topological layer, each cell emits only a short locally checkable claim/result, and a
final merge cell synthesizes the answer.

This is a shift from "generate the solver's transcript" to "generate the dependency certificate sufficient
to verify the solution."

The key novelty vs. the obvious open slice: this is **not K independent full reasoning paths plus a summary**.
That version is very close to occupied: NAP, arXiv:2602.23225. Your open slice survives only if the object
is more dependency-compressed and less self-ensemble-like than NAP.

### Canvas format

```
<frontier>

<layer 0>
[cell A | role=given | deps=∅]
claim: ...
check: ...
[/cell]

[cell B | role=given | deps=∅]
claim: ...
check: ...
[/cell]
</layer>

<layer 1>
[cell C | role=compute | deps=A]
claim: ...
check: ...
[/cell]

[cell D | role=compute | deps=B]
claim: ...
check: ...
[/cell]
</layer>

<merge | deps=C,D>
therefore ...
</merge>

<final>
\boxed{...}
</final>
```

Each cell is a **certificate atom**:
```
claim: <one mathematical fact / equation / bound / case result>
check: <one local justification, ideally 1-2 equations>
```

The model is learning to output a **proof/computation memo**, not a story. Same-depth cells are deliberately
independent given the problem + their declared ancestors.

## 2. Training target: what the model learns, and from what signal

The model learns: Given a problem, predict a compact dependency-layered certificate whose cells are
conditionally recoverable from the problem plus their declared ancestors, and whose final merge yields the
verified answer.

### Data construction

For each solved problem:
1. Generate or collect several correct teacher traces
2. Keep only traces whose final answer passes your verifier
3. Convert a trace into atomic facts: variable definitions, case splits, computed quantities, lemmas,
   inequalities, substitutions, final synthesis
4. Build a dependency DAG: edge u → v if cell v uses the result of cell u
5. Topologically layer the DAG
6. Compress each node into `claim + check`
7. Discard or repair examples whose certificate does not fit the target budget or whose local checks fail

For MATH/AIME, the compiler can be partly heuristic: equations, variable reuse, numeric sub-results,
"case 1/case 2," "therefore," "substitute," "discriminant," "by AM-GM," and similar markers get you far
enough for a first pass. Use a stronger LLM or symbolic checker only to generate/validate the certificate,
not as a runtime component.

### Loss

Use the masked diffusion CE as the base objective, but change the mask distribution and weights.

Mask distribution:
```
40% standard i.i.d. token masks
25% whole-cell masks
20% whole-layer masks
10% ancestor-only masks: mask a cell while exposing only problem + declared deps
5%  merge/final masks: expose certificate cells, mask merge/final
```

Role/noise weighting:
```
high mask ratio: upweight frontier, cell IDs, deps, claim/result tokens
medium mask ratio: upweight local check tokens
low mask ratio: upweight merge and final answer tokens
downweight filler/prose everywhere
```

Then add the important auxiliary term: **dependency-selective invariance**.

For an independent cell v, predictions for v should not materially change when unrelated same-layer peer
cells are hidden or shown:
```
P0(v | problem + ancestors) ≈ P0(v | problem + ancestors + same-layer peers)
```

For a dependent cell v with ancestor u, predictions should improve when u is visible:
```
NLL(v | problem + ancestors including u) < NLL(v | problem + ancestors without u)
```

That is the core learning signal. It teaches the model that same-layer cells are parallel recoverable,
while dependency edges actually matter. NAP uses structured parallel paths and standard masked diffusion
training; this design uses **non-redundant dependency cells plus a loss that explicitly separates ancestor
dependence from peer invariance**.

Matched-compute baseline: train the same model for the same number of forward-pass FLOPs on the same
problems, but with standard masked CE over serialized teacher rationales or over a serialized version of
the same certificate. If the auxiliary loss uses extra forwards, give the baseline extra epochs or extra
examples to match FLOPs.

## 3. How it exploits PARALLEL generation

A dLLM can predict all masked positions under bidirectional context. But ordinary CoT data tells it that
the useful context for token t_i is usually the textual prefix t_{<i}, so arbitrary-order denoising
collapses toward an implicit AR path. NAP's diagnosis is similar: standard CoT supervision induces AR-like
dependency even in non-AR models.

Parallel Frontier Certificates instead make the useful conditioning set:
```
problem + declared ancestors
```
not:
```
all previous text
```

That lets the model fill multiple same-depth cells in the same denoising phase. The canvas positions become
independent work slots. The final merge cell then reads the completed frontier and emits the boxed answer.

This helps dLLMs more than AR models because the output object is spatially simultaneous. An AR model
still has to write cell A before cell B in token time. A masked dLLM can denoise cell A, B, C, and D
together if their dependencies are already available or inferable from the problem.

The intended effect is not faster inference as the primary metric. The intended effect is **higher verified
accuracy under the same token/step budget**, because wrong/truncated runs currently spend about twice the
token/step budget of correct runs in your probe.

## 4. Cheap no-training DPC: Parallel Frontier Recoverability Contract

Run this before full fine-tuning on your existing LLaDA-8B logs.

### Step A: Parse existing solutions into atoms
Identify boundaries using structural markers: variable assignments, case headers, computed numeric values,
lemma-like claims, "therefore/substitute/so" conclusions. For each atom, mark **result tokens**: numbers,
variables, equations, inequalities, case=..., final derived facts.

### Step B: Infer a dependency graph
Create edge u → v if:
- v reuses a variable/value introduced in u
- v substitutes an equation from u
- v depends on a case split from u
- v's claim is semantically downstream of u

This can be heuristic. For 164 problems, an LLM-assisted offline pass is cheap enough, but the scoring
should use LLaDA logits/logs.

### Step C: Compute stabilization times from logs
For token position p:
```
tau(p) = first denoising step where the eventual final token is top-1
         or becomes unmasked and remains unchanged to the end
```
For atom a:
```
tau(a) = median tau(p) over result tokens in a
```

GO conditions:
```
PMASS >= 0.30-0.40
ARNESS_resid low after depth control
same-layer atoms stabilize in overlapping windows
correct traces have lower DEPTH VIOLATION than wrong/truncated traces
```

If tau mostly follows text position even after dependency depth control, the current model is behaving
like an AR transcript writer, and the proposed training has to overcome a bigger prior.

### Step D: Optional cheap forward-pass counterfactual
For each atom v, make three corrupted canvases from the final trace:
```
PREFIX context:   problem + all text before v visible; v masked
ANCESTOR context: problem + inferred ancestor atoms visible; v masked; non-ancestors masked
PEER context:     problem + ancestors + same-layer peers visible; v masked
```

Score only v's result tokens:
```
Δprefix(v) = NLL(v | ANCESTOR) - NLL(v | PREFIX)
Δpeer(v)   = NLL(v | PEER) - NLL(v | ANCESTOR)
```

Pass signal:
```
median Δprefix <= 0.2-0.3 nats/token on independent result atoms
median |Δpeer| small for independent peers
ancestor removal hurts dependent atoms
```

This is the strongest no-training probe. It tells you whether LLaDA already has the latent ability to
predict a sub-result from the true dependency set, or whether it only knows how to continue the serialized text.

### Step E: Virtual compression estimate
The compiled certificate should land around the current correct-solution length or lower, not become a
3-path NAP-style internal ensemble.

## 5. Falsifiers: what kills this before training

Kill the project before full FT if any of these happen:
1. **No parallelizable mass.** The dependency graphs for MATH-L5/AIME are mostly chains: width-2-or-more
   layers cover less than ~25-30% of answer-critical atoms.
2. **Ancestor-only recoverability is bad.** If NLL(v | ancestors) is much worse than NLL(v | prefix) for
   most independent atoms, the base model is not ready to fill dependency cells without serialized prefix context.
3. **Stabilization time is just text order.** If tau(atom) strongly tracks textual position even after
   controlling for dependency depth, the logs do not show a latent parallel-frontier signal.
4. **Result tokens do not stabilize earlier than filler.** Your method depends on claim/result tokens being
   the high-utility substrate. If prose and result tokens are equally late/unstable, role-weighted certificate
   training has no obvious lever.
5. **Compiled certificates are not faithful.** If the teacher-to-DAG compiler cannot produce locally checkable,
   final-answer-preserving certificates with >90-95% validation pass rate on a held-out slice, do not train on them.
6. **The dumb brevity baseline ties.** If a terse standard masked CE baseline gets the same verifier gain,
   then the improvement was token compression, not structural parallelism.

## 6. DeadlineBox-style rival: the dumbest baseline

The dumb baseline is **DeadlineBox-Brevity SFT**.

Use the same teacher problems, same final-answer verifier, same training FLOPs, same max generation
tokens/steps, and standard masked CE. No DAG, no cells, no dependency loss, no column permutation, no
block-cell masks.

This baseline might capture most of the gain if your issue is simply "the model writes too much." It is
dangerous because your empirical result already screams token budget. If DeadlineBox-Brevity matches PFC,
then parallel structure was unnecessary.

A stronger matched baseline: **Serialized Certificate SFT** — take the same PFC cells but linearize them
into a normal topological order and train with standard masked CE. If PFC beats this, the win is more
likely from parallel layout/loss rather than data cleanup.

## 7. Honest closest rivals

The closest rival is **NAP: Non-Autoregressive Parallel DLMs**, arXiv:2602.23225. It directly argues that
DLMs collapse into AR-like generation because standard training data is sequential, then groups multiple
independent reasoning trajectories into a structured canvas and uses parallel-forced decoding. It also
reports that gains are strongest under aggressive parallel decoding, and that standard long-CoT degrades
as parallelism increases.

The distinction:
```
NAP = multiple full reasoning paths + summary; standard masked objective; internal ensemble
PFC = one non-redundant dependency DAG; locally checkable cells; dependency-selective loss
```

Other relevant but less direct rivals:
- **Diffusion of Thoughts**, arXiv:2402.07754: lets reasoning steps diffuse over time in a diffusion model
  and shows reasoning benefits, but it does not train a compact dependency-layered certificate object.
- **ThreadWeaver**, arXiv:2504.15466: trains models to orchestrate spawn/join parallel computations, but it
  is a broader language-model reasoning framework with RL and adaptive multithreaded inference, not a
  masked-diffusion certificate training target.

## 8. If this fails: jump target

Named jump target: **Verifier-Compressed Certificate Distillation**.

If the DPC says MATH/AIME traces are genuinely serial or ancestor-only recoverability is poor, abandon
explicit parallelization and attack the same empirical failure through **reasoning compression** instead:

```
problem → minimal verifier-checkable certificate → final boxed answer
```

No layer width requirement. No claim of parallelism. The object becomes the shortest faithful certificate
that preserves verifier accuracy. Train with standard and block-mask CE, select only by held-out verifier
accuracy, and compare against terse CoT.

## The concrete bet

Train LLaDA-8B to emit a compact dependency-layered certificate, not a long thought trace and not multiple
full thoughts. Use whole-cell masking, layer masking, column permutation, and dependency-selective invariance
so same-layer cells become independently denoisable. Evaluate only by verifier accuracy under the same
token/step budget.

The first thing to run is the no-training **Parallel Frontier Recoverability Contract** on the 164 logs.
If it passes, train three matched-compute models:
```
A. Standard Long/Terse CoT masked-CE baseline
B. Serialized Certificate masked-CE baseline
C. Parallel Frontier Certificate with cell/layer masks + dependency loss
```

PFC only counts as real if C beats both A and B on verified accuracy, not diffusion loss, with the same
FLOPs and token/step budget.

## Opus packaging notes
- author_engine: leap=Pro (GPT-5.5 Pro 扩展), packaging=Opus; self_certified=false
- Closest rival: NAP (arXiv:2602.23225) — PFC distinguishes via non-redundant DAG + dependency-selective loss
- FORBIDDEN cleared: NOT frozen post-hoc head (training-based); NOT compute-allocator (same budget); NOT He-line
