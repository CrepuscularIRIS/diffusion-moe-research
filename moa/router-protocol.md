# MoA Router Protocol (前面路由) — how Opus builds N *differentiated* advisor prompts

> The router is **Opus's in-context job**, not a script (assigning operators/frames/schools needs taste +
> reading the banks). It turns ONE problem card into N distinct prompts so the panel COVERS the idea space
> instead of echoing. Output = `<dir>/<lane>.txt` per advisor → `moa/moa_panel.sh --per-lane <dir>`.

## Steps (per problem card + its `failure_signature`)
1. **Operators** — retrieve from `opus-pass/operators.md` by `failure_signature` (the retrieval index). Assign a
   **distinct** operator to each advisor (rotate — never repeat within a round).
2. **Frames** — assign a **distinct** mathematical frame from `skills/forge/references/frames.md` (14-frame
   palette); **≥1 non-incumbent** frame in the set.
3. **Schools** — assign a **distinct** methodology school (soul-question) from `skills/forge/references/schools.md`.
4. **Structured dropout** — for ~half the advisors, **WITHHOLD the incumbent framing**: state the phenomenon with
   the field's vocabulary STRIPPED (the `/forge` step-7 blinding protocol). The rest get the full framing.
   Surgical, never random — dropout forces off-frame ideas; Opus discounts any that come back degraded.
5. **Per-advisor prompt** = `{problem core, full or blinded}` + `{your operator: <name + one_sentence_core_move>}`
   + `{frame it as: <frame>}` + `{your school lens: <soul-question>}` + the **output contract**:
   > "Output EXACTLY: MECHANISM (1–2 sentences) | DIFFERENTIAL PREDICTION (an observable the incumbent does NOT
   > predict) | CHEAP PROBE (test before training) | BIGGEST SELF-ATTACK (of {data-leakage · under-tuned baseline
   > · metric-gaming · seed-luck · tuning-budget artifact · doesn't-scale}, which MOST threatens this mechanism's
   > claimed gain — and how the cheap probe defends). ≤140 words. Answer from your OWN knowledge — do NOT use web
   > search or any tools. Be concrete and independent; do not hedge or survey."
   > *(BIGGEST SELF-ATTACK = spark.md Battery 2, applied in advance — pressure-test the number BEFORE it eats a
   > training run, not after. See `plan/Audit/pipeline-audit-2026-07-05.md`.)*
6. Write to `<dir>/<lane>.txt`, then `moa/moa_panel.sh --per-lane <dir>`.

## Tool discipline per lane — HONEST (only the gateway is structurally tool-free)
- **deepseek / mimo (gateway):** STRUCTURALLY tool-free (no tools passed) + reasoning ON — the ONLY guaranteed pure-Q&A lanes.
- **gpt5 (codex):** `--disable web_search` (no search); RETAINS shell/MCP it *could* invoke — answers directly for a plain Q&A, but is NOT sandbox-guaranteed tool-free.
- **gemini / opus46 (agy):** TOOL-CAPABLE / AGENTIC — `--dangerously-skip-permissions` AUTO-APPROVES any tool the model invokes. The "no tools" prompt line is a SOFT request only, not enforcement.

## Assignment table (example, 5 advisors)
| advisor | operator | frame | school | dropout |
|---|---|---|---|---|
| gemini  | op₁ | frame₁ (non-incumbent) | school₁ | **blinded** |
| gpt5    | op₂ | frame₂ | school₂ | full |
| deepseek| op₃ | frame₃ | school₃ | full |
| mimo    | op₄ | frame₄ (non-incumbent) | school₄ | **blinded** |
| opus46  | op₅ | frame₅ | school₅ | full (agentic) |

## 连续询问 (DEPTH axis — the 5-question CHAIN; complements the breadth panel above)
**Do NOT ask MoA once. After 逆向溯因, Opus DECOMPOSES the problem into ~5 CONSECUTIVE questions and drills them —
query count = rounds × advisors, far more diverse. Opus DECOMPOSES + RECONCILES; it does NOT solo-answer.** Default drill:
1. **ROOT (溯因)** — what MOVE generated the SOTA / what is the TRUE load-bearing bottleneck?
2. **MECHANISM** — the sharpest attack on that root under the ≤4h envelope.
3. **RIVAL / OFF-FRAME** — what a DIFFERENT school/frame would do instead (force divergence).
4. **SELF-ATTACK** — the biggest failure reason (leakage·baseline·metric·seed·budget·scale; = Battery 2).
5. **CHEAP PROBE** — the fastest pre-GPU test that decides GO/KILL.
- **INFORMED chain:** run round-by-round — reconcile each, write the next round's prompts from the prior answers
  (q2 uses q1's root · q4 attacks q2 · q5 probes q4). Fire with `moa/moa_chain.sh <chain-dir>` (q1/ … q5/).
- **Route the HARDER rounds (q1 root · q2 design) to GPT-5.5 Pro** — deep design + literature-grounded root is
  the external brain's job, not the fast panel's. Rely on the ENVIRONMENT (panel + Pro), not Opus-solo.
  (DeepResearch DROPPED 2026-07-06 — Cloudflare-blocked, unreadable by ClaudeCode; Pro is the only browser lane.)

## 后面验收 (reconcile — the judge)
Opus 4.8 reconciles via the dispute-map (consensus / conflict / **unique-insight** / **blind-spot**), discounting
Claude-family correlation (opus46). **SELECT by the uncertainty-first battery, NOT "which sounds best":** pick the
candidate whose CHEAP PROBE kills the BIGGEST unknown fastest (info-gain); if a candidate's `BIGGEST SELF-ATTACK`
is unaddressed → it stays a HYPOTHESIS, not a pick. Any panel-surfaced CONFUSION (an unexplained result / disputed
premise) = HALT → resolve BEFORE dispatch. Synthesis flows into `/prereg → /adversary`; CLAIM_STANDS stays independent.

## Tiering — by REVERSIBILITY (CLAUDE.md rule 10), not vibes
Full differentiated panel fires on **IRREVERSIBLE forks**: mechanism design that will EAT a training run · direction
/ region-close / pivot · anything hard to undo. REVERSIBLE tweaks (LR · aug · which-smoke) = solo Opus, instant —
never panel them (costs ~1min + N models). Medium = Opus + 1.
> The panel IS the environment that produces the judgment a single model can't self-generate (taste = panel + gates
> + atlas, not weights). That's why irreversible forks route here. See `plan/Audit/pipeline-audit-2026-07-05.md`.
