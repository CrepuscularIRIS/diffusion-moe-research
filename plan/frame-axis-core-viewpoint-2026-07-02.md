# Core Viewpoint — The Mathematical-Frame Axis (the third axis of research-os)

> **Status: CORE VIEWPOINT (adopted 2026-07-02).** This is the project's central methodological insight on
> *idea novelty*, and the design of research-os **v0.7**. Authored by Fable5, adopted by the user.
> Operationalized in the research-os plugin (`frames.md` + edits to `/forge`, `/prospect`, `/autopsy`,
> `/compass`). This doc is the durable record of *why*; the plugin is the *how*.

## 1. The problem it solves

AI-generated ideas feel un-novel and "mostly don't work," and — the sharpest tell — they show a
**mathematical monoculture**: every candidate is "a probabilistic / linear-algebra module bolted onto a
net" (conditional probability · low-rank factorization · weighting · gating). No geometric, dynamical,
algebraic, information-geometric, spectral, or stochastic-process object ever appears as the *primitive*.

## 2. The mechanism (why prompt allocation CAN fix this)

**The monoculture does not live in the model's unconditional prior — it lives in frame-selection, and
frame-selection is entirely controlled by the packet we send.** We sample `P(idea | packet)`, and today
every packet is `(problem + the field's papers + the field's vocabulary)`, so the model dutifully returns
the field's interpolation. The empirical fact that saves the fix:

> **LLMs are weak at spontaneously *choosing* an off-consensus frame, but genuinely strong at *executing* a
> specified one.** ("State accepted-length as a branching process and derive the natural object" — Pro will
> do this well; it will just never volunteer it.)

## 3. The design principle

> **Separate frame-selection from idea-generation.** The *pipeline* chooses the frame (forced coverage, off
> the model's prior); the *model* derives under the frame (where it is actually strong).

This is exactly `enrich.md`'s own move — 建模对象迁移 is a human choosing a new object *family* (residual /
score / energy / support) and letting the derivation follow; enrich §7's `旧对象 → 新对象` table is a
frame-shift table. The pipeline had absorbed enrich's **methodology axis** (the 14 schools = *how to
think*) and its **output axis** (the 9 types = *what output*) — but never operationalized its
**mathematics axis** (*which mathematics carries the object*). That missing third axis is the hole the
branching-random-walk episode fell through (we *noticed* the frame existed in our own notes, and had no
slot that forced anyone to derive under it).

## 4. The three levers (each kills one failure mode)

- **FORCE** — the pipeline assigns the frame → kills consensus frame-selection.
- **BLIND** — strip the field's vocabulary from the packet → kills interpolation-by-vocabulary.
- **DISCRIMINATE** — demand a prediction the incumbent frame does not make → kills relabeling theater.

## 5. The six insertion points (zero new commands, zero new gates)

1. **`forge/references/frames.md`** — a ~14-frame math palette (the third axis), parallel to `schools.md`:
   probability/Markov (the **named incumbent**) · branching/renewal · optimal transport · dynamical
   systems & control · spectral/operator · information geometry · statistical mechanics/mean-field · convex
   duality · algebraic/group · extremal combinatorics · queueing · rate-distortion/coding · causal graphs ·
   random matrix theory. Each with its *natural object* + *fits-a-signature-of* column.
2. **`/forge` step 3′** — a **frame ledger** ("incumbent frame = X") + a hard rule symmetric to the rival
   school: **≥1 candidate derived in a non-incumbent frame**, with a fifth card field **`DIFF-PREDICTION`**
   (an observable this frame predicts that the incumbent formulation does not — *no differential ⇒ it is
   vocabulary, not a frame ⇒ discard*). Self-administrable (DOWN-only; respects the invariant).
3. **`/forge` step 7** — the Pro hand-off splits into a **two-call protocol**: **Call A (blinded reframe)** —
   the phenomenon *as data* (raw curves/rates), field vocabulary stripped, the assigned frame, derive the
   natural object + its differential prediction, map back only at the end; **Call B (standard design)** —
   today's packet unchanged. Opus compares: no differential ⇒ frame failed honestly (cost = one call);
   a differential ⇒ that IS the probe, surprise-symmetric by construction, usually measurable at inference
   *before any training* (composes with the cheap-signal ladder).
4. **`/prospect`** — **Mine 2 (own logs) promoted to Mine 1**, fed by an **anomaly ledger**: `/autopsy`
   writes every *surprise* (not only failures) as a one-line anomaly into the tree node insight; `/prospect`
   consumes that ledger FIRST and its Pro hand-off carries the raw anomaly numbers (artifact-fidelity).
   Own-log anomalies are the one input the model's prior has never seen — the only structurally
   off-distribution data we possess.
5. **Goal directive — an optional `FRAMES:` field** (the user's injection point, moved to the *front*):
   `FRAMES: branching-process, information-geometry`. When present, the forced off-frame candidate tries
   the user's frames first; absent, the pipeline rotates from the palette by signature match. Relocates the
   user's mathematical taste from promotion-time to framing-time at the cost of one line. `/prospect` and
   `/forge` reports each print a visible **frame-ledger line** so the user can inject/override from any
   report without breaking goal-mode autonomy.
6. **`/compass`** — a **frame-monoculture counter**: across the last N `/forge` rounds, how many distinct
   frames were the primary object? `1 ⇒ monoculture flag; next /forge must rotate`. Countable, advisory.

## 6. What it deliberately does NOT do
- **No frame checklist sweep.** Running all 14 frames per problem = the v0.4 menu disease reborn. **ONE
  forced off-frame per round; rotation across rounds** (`/compass` tracks it).
- **No exotic-math points.** The He-bar still rules: a frame is admitted only if it makes the object
  *simpler* (enrich §8 — 让任务变简单的建模对象). Fancy formalism that adds parts fails 少/准 and dies.
- **No new commands, no new gates.** Six edits: one reference file + surgical additions to
  forge/prospect/autopsy/compass + one optional goal field. Pure prompt allocation.

## 7. The honest residual
Allocation forces coverage of **known-but-unused** frames; it **cannot mint mathematics outside every
textbook.** But that is not the binding constraint — the branching-random-walk episode proves we were
failing at a *much lower* bar: a relevant frame sat in our own notes and no slot forced a derivation under
it. This design closes exactly that gap; the one-line `FRAMES:` injection covers most of what remains.
