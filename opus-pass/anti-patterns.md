# Anti-Patterns — killed buzzword-transplants (opus-pass)

> These looked like operators but were KILLED at the corrosion gate — recorded so we never re-derive them.
> Kill reason is always one of: (a) fails the DELETION TEST (strip the new vocabulary, no prediction
> disappears ⇒ relabeling); (b) a bare carrier-noun mistaken for the *move*; (c) an engineering/scaling knob
> that changes coverage/compute but not the modeling object; (d) no cheap probe AND no differential.

| killed pseudo-operator | one-line reason it is not a taste operator |
|---|---|
| tokenization / "everything is tokens" | interface unification; predicts nothing new unless tokenizing changes what is predictable/controllable (it usually doesn't) — deletion test leaves every prediction intact. |
| backbone-swap (Conv→Transformer→Mamba→ViT) | changing the function approximator is not changing the modeling object; no differential prediction. |
| bigger-data scaling | more data changes statistical coverage, not the object being modeled. |
| bigger-model scaling | more parameters is a capacity knob, not an operator. |
| module-adding ("add memory / add a graph / add an adapter") | bolting on a component without switching the mediating object is engineering stacking; deletion test survives. |
| benchmark-ization ("propose a new benchmark") | a benchmark exposes problems but is not a research *move* that predicts a new observable. |
| bare carrier-nouns: "use a field / graph / energy / operator / latent / manifold" | these are mathematical carriers, not operators — an operator must say *why* you switch to it and what it predicts the old object doesn't. |
| multimodal-concatenation ("just concat the modalities") | concatenation adds no sufficient object; predicts no fusion-specific observable — killed transplant. |
| end-to-end-unification ("one unified model / one token space") | unification with no new differential prediction is interface theater. |
| "use diffusion here" | naming a method, not a move; unless it becomes correction-field / denoising-chain with a step-budget differential, no prediction appears. |
| "use optimal transport" | dies unless a coupling/transport object with a mass-flow or cross-space differential is actually built (see transport-coupling-ization for the real form). |
| "use causality / a causal graph" | a DAG drawn with no cross-environment invariance test or intervention differential is relabeling (the real form is invariant-ization). |
| "add geometry / make it equivariant" | claiming equivariance without a group object and a rotation-continuity/equivariance-error differential is decoration (real form: group-equivariance-ization). |
| "make it Bayesian" / "add uncertainty" | a variance head that never enters a decision or predicts info-value is not belief/particle/distribution-ization. |
| "quantum X" / "add attention" / "make it a foundation model" | method-name transplants with no old→new object and no cheap probe. |
| RT-2 / Gato "action-as-text" (pure form) | repacking actions into a shared token space is a boundary interface change; kept as a source-episode only because it altered the *statistical* object of "action," not because it is a transferable operator. |
| "energy model" as a bare label | calling any scalar head an "energy" without argmin/ranking/search use is a carrier-noun transplant (its real differential lives in correction-field / affordance-field). |
| "self-refinement" as a slogan | iterative refinement with no unified correction semantics (no noise level, no message object) predicts no step↔quality relation — only becomes real as correction-chain or factor-graph message passing. |
| "long-context = just a bigger window" | widening the window is a capacity knob; it is NOT memory-kernel-closure (which predicts a lag structure a window can't fix) — a frequent and important confusion. |
| "coarse-to-fine" as a slogan | cascading a small then big model is not multiscale-correction-hierarchy unless there's a restriction/prolongation error object and a resolution-independence differential. |
| framework-unification-naming ("unify N models into one framework", e.g. MPNN) | strip the framework noun and no prediction disappears — every prediction belongs to a member model; a naming/taxonomy act, not a move. (Ilya-27 pass, MPNN.) |
| differentiable-relaxation-of-discrete (NTM soft addressing / Gumbel / DARTS-style) | its "differential" (SGD trains where score-function estimators plateau) is a property of the OPTIMIZER, not an observable of the modeled system; the measure-over-choices carrier partially dedups to #13 particle-measure; also max canon. SOURCE-EPISODE only. |
| "Occam's razor / prefer simpler models" as a design principle | slogan-form (same class as "make it Bayesian"): with no bit-accounting there is no differential — the ACCOUNTING is the operator (N4 two-part-code-ization). |
| "just gzip it" / compression as a method NAME | without a two-part or prequential codelength LEDGER it predicts nothing a similarity kernel doesn't; the operator is the ledger (N4), not the compressor. |
| AIXI / "build the universal agent" | uncomputable and end-to-end-unification-flavored; no cheap probe exists before OR after training. Only the MEASURE survives (N9 simplicity-weighted-aggregation); the agent does not. |
| "evaluate on more / harder environments" | benchmark-ization; without the 2^(−K) codelength weighting the rank-inversion prediction disappears (the real form is N9). |
| vestige-removal ("delete inherited pooling/components when repurposing a net") | a methodology HABIT (ablate inherited structure across task-structure change), not a de-domained object with a stable differential. (Ilya-27 pass, Dilated Conv §4.) |
