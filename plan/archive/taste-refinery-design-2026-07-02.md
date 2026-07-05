# The Taste Refinery — a taste-mining supply chain (design + as-shipped status)

> **★ STATUS UPDATE (2026-07-02): the connect-back IS NOW WIRED — research-os v0.8.0 (commit 1ac2c69).**
> The user said "先改进工作流吧" (improve the workflow now), so §7's connect-back was implemented. **What
> actually shipped differs from §6/§7 in three ways** (the as-shipped reality wins over the design text
> below): (1) the bank is **`opus-pass/operators.md`** (project root, 21 ★ operators), NOT
> `plan/taste-bank/operators.md`; (2) it is **project-side markdown read like `frames.md`**, NOT an Arbor
> `taste-bank` run — a shadow tree was rejected as a drift risk (Arbor's only role = a live cross-link
> `operator:<name>` on the campaign node); (3) `/compass` gained an OPERATOR half of **check 5**
> (frame- & operator-monoculture), NOT a "6th check", and the `/forge` step is **3‴** (not 3″). The COLLECT
> stage (LDR/MiniMax + Gemini breadth) is still partly pending — a parallel Fable5 extraction pass is
> running and MERGES later via the `/autopsy` accumulation gate. The sections below are the ORIGINAL design
> of record; read them for rationale, but trust the status note above for what the live workflow does.
>
> Authored by the user (the 9-section design) + Fable5 refinements + the resolved engine choices.

## 1. What this is (and what it is NOT)

**Not** "collect more good ideas." The problem is not idea-scarcity — it is that the generator samples from
the model's prior, so its ideas cluster (the monoculture Fable5 diagnosed). This builds the missing
**fourth axis** of research-os:

```
schools.md      = how to think          (methodology)
research-types  = what output           (value)
frames.md       = which mathematics     (the carrier)
taste-bank      = which modeling OPERATOR  ← NEW (the 建模对象迁移 move)
```

It is a **reverse-generative system**: a paper/method is *observable evidence*; the taste operator is the
*latent cause*; taste-mining infers latent ← observable, to **expand the frame/operator-selection prior.**
This directly serves the Fable5 insight: an LLM won't *choose* an off-consensus operator, but it *will
execute* one you hand it — so we mine a bank of operators to hand it.

The atomic unit is not a paper. It is:
`failure-signature → incumbent object → omitted structure → new modeling object → math frame →
differential prediction → cheap probe.`

## 2. The pipeline — 3 stages, 3 engine roles (the collector ≠ the extractor)

**The load-bearing constraint:** the COLLECTOR must be web-grounded external breadth. If Fable/Opus both
collects and extracts, the episodes come from its prior = the monoculture the bank exists to break. So:

| Stage | Engine | Role |
|---|---|---|
| **1. COLLECT episodes** (breadth, web) | **HYBRID: `ldr-mcp` (breadth, headless, batch) → Gemini DeepResearch (deep-dig on the long-tail)** | `ldr-mcp` runs the 3 broad-casts headless (no browser contention with the VLA-Pro channel); Gemini (separate browser) deep-digs the best cross-disciplinary / under-transferred episodes. Returns raw episodes, NOT a survey. |
| **2. EXTRACT → de-domain → operator** (套话) | **Fable/Opus** (or a Sonnet agent) on the *collected* episodes | infer the latent operator; blind it to `de-domain → operator`. "套话" = the auditable **rationale** (old→new object · simplification · diff-prediction · probe), NEVER the CoT. |
| **3. AUDIT + cluster** (kill pseudo-taste) | **independent adversary** (Codex hook / a fresh Pro call) | KEEP / MERGE / ARCHIVE / KILL via the reused `DIFF-PREDICTION` gate. The extractor must not grade its own operators (the one invariant). |

Engine-question answers, explicit: **"用 Fable 套话?"** → Fable is the EXTRACTOR (Stage 2), not the
collector. **"Sonnet 跑 DeepResearch?"** → a Sonnet agent may *orchestrate* Stage 1, but the breadth comes
from the search engine, not Sonnet's prior. **"Playwright→Gemini?"** → yes, Gemini is the deep-dig engine —
on a **separate browser session**, never the VLA loop's Pro channel.

## 3. The two input streams (own-anomalies are the higher-value one)

- **External episodes** (Stage 1) — field-changing modeling-object shifts. **Bias toward the LONG TAIL:**
  operators famous in one field (statistical mechanics, control theory, queueing, coding theory, OT) that
  *never crossed into ML*. The canon (ResNet/Diffusion/MAE) is already in every model's prior — re-deriving
  it adds nothing.
- **Own anomalies** (first-class, higher value) — the `/autopsy` `[ANOMALY]` ledger. These are the one
  **off-distribution** input we own; operators mined from *our* failures are ones no external search has.
  Feed the ledger into Stage 2 alongside the papers. (The "~3 nats" episode is the archetype.)

## 4. The Taste Card schema (the 3 load-bearing fields decide entry)

```yaml
id:  source:  domain:
incumbent_object:      new_object:      carrier_math:      # the frame (frames.md)
core_simplification:       # what it makes SIMPLER (enrich §8 — 让任务变简单)   ← load-bearing
differential_prediction:   # an observable the new object predicts, incumbent does not  ← load-bearing
cheap_probe:               # test it BEFORE expensive training                  ← load-bearing
failure_signature:  transfer_targets:  anti_pattern:  positive/negative_examples:
```
Without `core_simplification` + `differential_prediction` + `cheap_probe` it is **术语, not taste**.

## 5. The corrosion gate (this is the whole ballgame)

The system rots into a "高级词汇菜单" the instant an operator without a diff-prediction gets in. Hard rules
(reuse the v0.7 `DIFF-PREDICTION` gate — no new machinery):
1. no `incumbent→new object` → not in. 2. no `core_simplification` → not in. 3. no `differential_prediction`
→ not in. 4. no `cheap_probe` → archive only, never `/forge`. 5. explains one historical case but can't
transfer → demote to source-episode. 6. too broad to guide action → split. 7. bare buzzword
("use diffusion/OT/causality") → KILL.

**The real validator is generation, not coverage** (the Day-5 test): on a held-out problem, *can the card
generate a killable candidate with a DIFF-PREDICTION + cheap-probe that we would not otherwise have thought
of?* Only generation-passing operators enter the bank.

## 6. Staging layout (design intent — see the as-shipped note: the live BANK moved to `opus-pass/`)

> **As-shipped:** the operator BANK is `opus-pass/{operators.md, source-episodes.md, anti-patterns.md}`
> (project root — the retrieval source `/forge` reads). `plan/taste-bank/` holds the raw DeepResearch source
> episodes + `extraction-prompts.md` (provenance + the reusable recipe). The design below assumed one
> `plan/taste-bank/` dir; the split (bank at root, raw reports under `plan/taste-bank/`) is the shipped shape.

```
plan/taste-bank/                 (staging; NOT skills/forge/references/ yet)
  operators.md                   # the 30-60 clustered operators
  source-episodes.md             # the raw episodes (provenance)
  anti-patterns.md               # buzzword-transplants that look like operators but aren't
  extraction-prompts.md          # Prompt 1/2/3 + the 10-step 套话 ladder (verbatim, reusable)
```

## 7. The connect-back (✅ SHIPPED in research-os v0.8.0 — see the status note at the top for as-shipped deltas)

Wired into the existing pipeline (mirrors the frames-axis wiring; ZERO new commands). As-shipped: `/forge`
step is **3‴** (not 3″); `/compass` extends **check 5** to cover operator-monoculture (not a "6th check");
the bank is markdown at `opus-pass/operators.md`. The four insertion points below are what shipped:
- **`/prospect`** — add **Taste-Bank retrieval** as a mining input (operators whose `failure_signature`
  matches the problem).
- **`/forge` step 3‴** — **operator-card forcing**: force ≥1 candidate derived from a bank operator (with a
  `DIFF-PREDICTION`), symmetric to the rival-school and off-frame rules.
- **`/autopsy`** — every surprise also asks: *did this produce a NEW operator, or correct an existing one?*
  (the bank grows from our own anomalies, closing the loop).
- **`/compass`** — **check 5** extended to **operator-monoculture** (are all recent `/forge` rounds using
  the same operator?), symmetric to frame-monoculture (now "frame- & operator-monoculture").

## 8. Execution plan (a separate offline batch — the "Refinery run")

1. `ldr-mcp` × 3 broad-casts (AI/ML shifts · sci-computing/physics/applied-math shifts · robotics/VLA/
   world-model/grounding shifts), long-tail-biased → raw episodes. Gemini deep-dig on the best.
2. Extractor prompt (Fable/Opus) on episodes + the `/autopsy` anomaly ledger → 80-150 raw cards.
3. Adversary prompt (independent) → cluster to 30-60 operators; KILL/ARCHIVE the rest.
4. Pick the ~15 most relevant to current directions (VLA fusion · diffusion-LLM joint-assembly ·
   speculative-decoding correction) → `plan/taste-bank/`.
5. **Validate by generation** on 3 held-out problems — each surviving card must generate a killable
   candidate. Non-generating cards drop.

## 9. What this deliberately does NOT do
No new research-os command, no new gate (reuses `DIFF-PREDICTION`). No modification of the live workflow
while the VLA goal runs. Does not use Fable as the collector (that would re-derive the prior). Does not use
the VLA loop's Pro/Playwright channel. Compressed to one line:

> **The taste-bank = a library of 建模对象迁移 operators reverse-inferred from external episodes AND our own
> anomalies; an operator enters only if it makes the object simpler, predicts a differential, and has a
> cheap probe — expanding the operator-selection prior the way frames.md expanded the frame-selection prior.**
