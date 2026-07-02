# 1. Audit of `enrich.md`

Audited as a PI deciding whether to let this document govern a lab's idea flow.

## 1.1 The strongest part — the non-obvious core value

It is **not** the old-object/new-object table. The table is the marketing layer, and it
is the most dangerous part of the document (see 1.2).

The real value is two structural commitments:

**(a) The falsification contract welded to abduction.** The 7-step template's spine —
phenomenological puzzle → identify what is actually modeled → name the missing object →
explain existing failures → specify the kill experiment — is abduction with a mandatory
exit condition. Steps 6 and 7 are what separate this from idea generation: the reframing
must *retrodict documented failures* and must *name the experiment that kills it*. Most
ideation systems have neither. This converts "I have an intuition about diffusion" from
a mood into a decidable claim. If only one thing survives from this document, it should
be: **no object proposal exists until its kill experiment is written.**

**(b) The layer ordering is honest.** The document places Modeling-Object Shift at
Layer 2 of 5 — below research-program design and evaluation-system rewriting — and the
closing loop (identify community defaults → rewrite as testable objects → kill cheaply)
is the actual usable engine. It correctly frames object shift as an *intermediate move*,
not a terminal achievement. Most methodology documents sell their move as the top layer;
this one doesn't. That self-placement is the most credible thing in it.

Derived, and worth stating explicitly: the methodology's best use is as a **rejection
filter**, not a generator. "State your modeling object or your idea does not exist" kills
80% of shallow proposals in one sentence. As a generator it is much weaker (see below).

## 1.2 The most dangerous failure mode — the attack

**Primary: post-hoc object laundering.** The vocabulary is expressive enough that *any*
trick can be re-described as an object shift after the fact. "I added a contrastive
auxiliary loss" becomes "I shifted the modeling object from the closed-set posterior to
semantic support geometry." Filling in Old Object / New Object table cells costs nothing,
and nothing in the document verifies that the new object is **load-bearing** rather than
decorative. Failure signature: the method would perform identically if you deleted the
object-language from the paper. The document contains no deletion test. This is fatal,
because the document will be operated by LLMs inside a Research-OS — systems whose
comparative advantage is exactly fluent re-description.

**Second: survivorship reasoning.** Every exemplar — ResNet, diffusion, flow matching,
attention — is drawn from the ~five winners out of thousands of attempted
reparameterizations in the same period. The document reasons from winners only and has
no mechanism for estimating whether a proposed shift sits in the fat or the thin part of
the success distribution. The honest base rate for "proposed object shift becomes a
recognized reframing" is well under 1%. A methodology that doesn't internalize its own
base rate manufactures overconfidence.

**Third: the taste machine amplifies its own substrate's failure mode.** The selection
criteria — "natural," "geometric," "elegant," "retellable" — reward writing quality.
The operator most at risk of confusing writing quality with research quality is an
LLM-driven ideation loop. The methodology, run inside your Research-OS without hard
gates, is a machine for producing sophisticated academic rhetoric at scale — your own
named failure mode, industrialized.

**Fourth: diagnosis overproduction.** The template generates object-proposals far faster
than 2×4090 can run kill experiments. Unkilled beautiful objects accumulate and start
being *treated as validated* because they survived (unexamined) for months. Idea
inventory without expiry is a form of self-deception.

**Fifth — and note this carefully — the document's own flagship example is occupied.**
"OOD should model support/energy rather than p(y|x)" was the field's move in 2020
(energy-based OOD, Liu et al.), matured through 2023 surveys. The document cites this
history and still presents the example as if room remains. That is the exact failure the
methodology is supposed to prevent, demonstrated inside the methodology's own text. Treat
it as a permanent warning label.

## 1.3 Missing hard constraints — the minimum set

Six rules. Any fewer and it's idea theater; many more and it's bureaucracy.

1. **Occupancy-first.** No object proposal survives 24 hours without a prior-art
   occupancy map: who already models this object, in what form, with what results,
   produced by *live search*, not model memory. If occupied, the proposal must be
   restated as a delta against the strongest occupant, or killed. (The document's own
   OOD example fails this rule.)

2. **Deletion test (load-bearing check).** Every proposal must specify an ablation in
   which the new object is removed at **equal parameters and equal compute** and a
   pre-registered metric degrades. If no such ablation can be written, the object is
   decorative and the proposal does not exist.

3. **Falsifier before poetry.** The kill experiment — dataset, metric, threshold,
   seed count, GPU-hour budget — must be written *before* any prose about the object's
   naturalness or beauty. Budget cap: the falsifier must run within ~48 GPU-hours on
   the actual substrate (2×4090). If it can't, the idea goes to HOLD with a written
   falsifier, never to the writing queue.

4. **Metric contract (anti-Goodhart).** The new object must improve a metric that
   either (a) existed before the proposal, or (b) is validated against ground truth
   external to the paper. A paper may never introduce a metric and the method that
   optimizes it as its only evidence. Self-licking benchmarks are auto-KILL.

5. **Two-failure retrodiction.** The object must explain ≥2 documented, pre-existing
   failure phenomena it was not fitted to, at least one checked quantitatively before
   any new experiment is run. Explaining only what every competing story also explains
   counts as zero.

6. **Conversion or expiry.** Every killed object must emit a search-space constraint, a
   reshaped candidate, or an explicit region-closure. Every *unkilled but unrun* object
   expires after 6 weeks and must re-pass rules 1–3 to re-enter. This is the only
   defense against the zombie inventory of beautiful ideas.

These six are gates, not paperwork: each one is a sentence to check, and each one can
kill.
