---
name: forge
description: The approach-generator — turn ONE problem card into a live, taste-ranked backlog of 3–5 candidates, each {MECHANISM, KILL, COST, SURPRISE, FRAME, DIFF-PREDICTION}. Forces one candidate per diversity axis (rival school · non-incumbent frame · rotated taste-operator) and ends with the REGENERATION RULE so the backlog never becomes a menu. Run after /prospect, before /prereg.
version: 1.0.0
tags: [Research, Generator, Ideation, Taste, Schools, Frames, Operators]
dependencies: []
---

# Forge — turn one problem into a live attack backlog

`/prospect` finds problems; `/forge` designs attacks. The output's most important property: it is
**ALIVE** — every `/autopsy` reshapes it. A backlog that only shrinks is a menu, and menus exhaust (that
is why campaigns "keep stopping": the stop was designed in).

References: `references/taste.md` · `references/schools.md` · `references/frames.md` ·
`references/taste-operators.md` · `../prospect/references/research-types.md`.

## Steps

### 1. Name the load-bearing variable
What actually controls the outcome? One sentence. Can't name it ⇒ the first backlog entry is a PROBE to
find it, not a design (designing against an unknown variable breeds compensation-stacks).

### 2. Occupancy check — TYPE-scoped, ≤15 minutes, re-prices but NEVER vetoes
Improvement type → "has this EXACT change been measured on this target?" — a neighbor is a cost signal;
read what the occupant did NOT measure. Novelty type → "is this object already named?" — if yes, note what
its owner's framing cannot predict.

### 3. Generate 3–5 candidates — one forced per axis, rotated, never a sweep
- Pick the 2–3 **schools** whose soul-question matches the failure signature; **always add one candidate
  from a RIVAL school** — the rival is where the non-obvious candidate comes from. The
  Modeling-Object-Shift move is one move among many: use it when the signature smells like a wrong object,
  not by default.
- **Force ≥1 non-incumbent-FRAME candidate** (step logic in `frames.md`): name the incumbent frame (the
  frame ledger), assign an off-frame by signature match — or the goal's `FRAMES:` field first. It must
  carry a **DIFF-PREDICTION** or be discarded as relabeling.
- **Force ≥1 OPERATOR candidate**: retrieve 1–3 taste-bank operators by failure signature, derive one
  candidate from ONE of them, rotate across rounds. Its DIFF-PREDICTION is the operator's differential
  *instantiated for this problem* — no live differential here ⇒ it didn't fit; don't force it.
- **ONE forced candidate per axis per round, rotation across rounds — never a palette sweep** (the menu
  disease).

### 4. One card per candidate
```
MECHANISM:       <WHY it should work — one mechanistic sentence, stated BEFORE running.
                  no mechanism-sentence ⇒ a lottery ticket, not a candidate>
KILL:            <the cheapest experiment that would kill it — becomes the /prereg falsifier>
COST:            <build + run estimate>
SURPRISE:        <what success would imply beyond the number>
FRAME:           <which frame carries the object; "incumbent" allowed but must be labeled>
DIFF-PREDICTION: <required for off-frame/operator candidates: one observable the new frame/object
                  predicts that the incumbent cannot. none ⇒ relabeling ⇒ discard>
```

### 5. Taste-rank and choose
Rank by **mechanism-clarity × expected-surprise ÷ cost**. Pick #1, then run the He-bar in **generative
mode** (`taste.md` §4): five real minutes on *"what would make this beautiful?"* — fewer parts? a more
natural object? does the fix explain the failure (自解释)? Simplify before building.

### 6. The REGENERATION RULE (the anti-menu clause — mandatory)
For each plausible failure mode of #1, state what it promotes:
```
if #1 fails because <mechanism-level reason A> → promote #3 / spawn <sketch>
if #1 fails because <reason B>                → the load-bearing variable was misnamed → step 1
if #1 fails for boring reasons (bug/data)     → fix and re-run; no backlog change
```
This is what `/autopsy` executes against. A forge output without it is incomplete.

### 7. The external brain designs — DEFAULT, not optional
Left "optional," the external route is never taken and self-design is measurably weaker. **The external
brain designs each candidate's architecture once; the local agent tunes it.** Package a one-page hand-off
`{problem card, constraints, occupancy notes, failure signature, backlog}` — not a repo dump. Skip only
for tactical tuning of an already-designed thing or trivial plumbing — write the reason in the card.

**The forced off-frame candidate gets the two-call blinded protocol:** Call A sends the phenomenon *as
data* (raw numbers from artifacts, the assigned frame, the field's vocabulary STRIPPED — state the
phenomenon in the frame first, map back to the application last); Call B is the standard incumbent-frame
design. Compare: A predicts nothing B doesn't ⇒ the frame failed honestly, discard; A does ⇒ that
differential IS the probe, surprise-symmetric by construction, usually measurable before any training. An
externally-designed candidate still gets its own card — external origin exempts nothing.

## Hard rules
- No candidate without MECHANISM + KILL — the falsification-first kernel.
- One forced rival-school, one forced off-frame (with DIFF-PREDICTION), one forced rotated operator.
- Occupancy re-prices; it never vetoes.
- The chosen candidate goes to `/prereg` before any run whose numbers might be cited.
- The backlog is written to survive failures, not enumerate them: expect `/autopsy` to add entries.

## Write-through
Chosen candidate → Arbor `tree_update_node` (`in_progress`, card as description); backlog + regeneration
rule → the node insight. Tree canonical; no side-files.
