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
   > predict) | CHEAP PROBE (test before training). ≤110 words. Answer from your OWN knowledge — do NOT use web
   > search or any tools. Be concrete and independent; do not hedge or survey."
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

## 后面验收 (reconcile — the judge)
Opus 4.8 reconciles via the dispute-map (consensus / conflict / **unique-insight** / **blind-spot**), discounting
Claude-family correlation (opus46). The synthesis flows into `/prereg → /adversary`; CLAIM_STANDS stays independent.

## Tiering
Full differentiated panel fires on **high-value forks only** (mechanism design · direction selection · hard
problem-finding) — NOT every routine 刷分 iteration (it costs ~1min + N models). Routine = solo Opus; medium = Opus + 1.
