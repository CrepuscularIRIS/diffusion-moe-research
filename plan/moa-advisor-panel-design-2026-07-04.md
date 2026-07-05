# MoA Advisor Panel — Design (方案)

> **Status: ✅ IMPLEMENTED + PROVEN (2026-07-05)** — scripts in `moa/` (`moa_ask.sh` · `moa_panel.sh` ·
> `router-protocol.md`), all lanes tested, differentiated smoke-test passed, wired into `manual §1`.
> 2026-07-04 design. Purpose: fuse a heterogeneous advisor panel into the
> **generative** side of research-os (`/prospect`, `/forge`) via single-shot **Q&A**, with **Opus 4.8 as the
> judge/aggregator**. Q&A mode is chosen deliberately: DeepSeek V4 Pro / Sonnet 4.6 / MiMo V2.5 Pro are
> **API-only** — a single-shot question→answer contract has no agent-loop or tool-calling surface to break.
> This is the OpenRouter-Fusion shape (panel answers in parallel → strong judge synthesizes) applied to
> research-os ideation. See [[moa-multi-model-strategy]] memory + `plan/operating-manual.md` §1.

## 0. The dividend we are buying
**Error-complementarity + independent perspectives + a strong aggregator** — NOT "the strongest single model."
N advisors answer the SAME question independently; Opus builds a structured dispute map (consensus / conflict /
unique-insight / blind-spot) and writes the final answer. The judge is where the value is won, not the panel size.

## 1. Roster & roles
| Model | Access path | Perspective | Heterogeneity vs Opus judge | Tier |
|---|---|---|---|---|
| **Gemini 3.1 Pro** | `agy` CLI (aliased, Q&A) | wide-retrieval / heterogeneous semantic view | **HIGH** | core advisor |
| **GPT-5.5** | `codex exec` (Q&A) | reasoning / audit / reframe | **HIGH** | core advisor |
| **DeepSeek V4 Pro** | OpenCode gateway (`OpenCode-APIKEY1`) | engineering / long-context / throughput | **HIGH** | core advisor |
| **Opus 4.6** | `agy --model opus-4.6 -p` (CLI) | Claude research-Q&A view (stronger than Sonnet for ideation) | **LOW** — same family as the judge | supplemental |
| **MiMo V2.5 Pro** | OpenCode gateway (`OpenCode-APIKEY1`); fallback `Mimo_API_KEY`/`Mimo_API_URL` | cheap additional view | MED | supplemental (panel-only, never load-bearing) |
| **Opus 4.8** | main loop (this agent) | **JUDGE / AGGREGATOR / DECIDER** | — | judge |

> The "heterogeneity" column is the honest MoA value per slot. **Opus 4.6 (the Claude advisor) shares the
> judge's family** ⇒ treat it as an extra *sample*, not an independent view; the three genuinely-orthogonal
> advisors are Gemini · GPT-5.5 · DeepSeek. **★ ROLE SPLIT: Sonnet 4.6 is NOT a research advisor — it is the
> DEVELOPMENT executor** (native `Agent`, `model:"sonnet"`). DEV = Sonnet 4.6 + Opus 4.8 (orchestrator); the
> GPT-5.5 Codex hook reviews the diffs. The Claude *research-Q&A* slot = Opus 4.6.

## 2. Access mechanics — single-shot Q&A, dispatched in PARALLEL
- **CLI advisors:** Gemini 3.1 Pro = `agy "<Q>"` · GPT-5.5 = `codex exec "<Q>"` — capture stdout
  **synchronously** (⚠ codex-rescue has fire-and-forgotten before: force a blocking `codex exec … > out.txt`
  capture, do NOT background).
- **Native ClaudeCode subagent:** Sonnet 4.6 = `Agent` tool with `model:"sonnet"` — subagents target a specific
  model ID directly, so Claude-family advisors need NO gateway. Opus 4.8 orchestrates + aggregates.
- **API advisors (OpenCode gateway):** DeepSeek V4 Pro + MiMo V2.5 Pro — POST to `$OpenCode-URL` with
  `$OpenCode-APIKEY1`, `model=<id>`, a single user message. One tiny reusable script `moa_ask.sh <model> <prompt-file>` → stdout.
- **Fan-out:** dispatch ALL advisors concurrently — wall-clock = slowest advisor, not the sum.
- **Graceful degradation:** per-advisor timeout; a failed/timed-out advisor drops to `null`; Opus proceeds with
  whoever returned. **A dead advisor never blocks the loop** (the panel is never a hard dependency).
- **Cache hygiene:** byte-stable system/framing prefix across advisors; the dynamic question at the tail.
- **Short outputs:** instruct each advisor to ~**400–800 tokens** (latency = slowest writer).

## 3. The hand-off (identical to every advisor ⇒ clean independence)
Every advisor receives the SAME packet:
- The taste-shaped question (a `/prospect` problem or a `/forge` design ask).
- Minimal framing (relevant school / frame / operator context, for a design ask).
- **Output contract:** *"Give your INDEPENDENT answer. State: (1) your key mechanism, (2) its differential
  prediction, (3) the one cheap probe that would kill it. ≤600 tokens. Don't hedge, don't survey, don't defer."*

## 4. Aggregation — the Opus judge (the crux; NOT a vote)
1. Collect all answers; drop the dead advisors.
2. Build the **dispute map**:
   - **CONSENSUS** — what ≥2 *independent* advisors converge on → high-confidence. *Weight the correlation:*
     Gemini+GPT+DeepSeek agreeing ≫ Sonnet+Opus agreeing (same family).
   - **CONFLICT** — where they disagree → Opus **adjudicates with reasons** (never majority vote).
   - **UNIQUE INSIGHT** — surfaced by only one → evaluate on merit, don't discard for being lonely.
   - **BLIND SPOT** — what none covered → flag (completeness critic).
3. Opus writes the final answer from the map, grafting the best of each.
Output = **reconciled answer + the dispute map** (so the reasoning is auditable, not a black-box merge).

## 5. Scoping — what the panel IS and ISN'T for
- **USE for:** generative ideation — `/prospect` (problem-finding) · `/forge` (candidate design). Where diverse
  priors/reasoning is the value and hallucination is cheap to filter downstream.
- **DO NOT use for:**
  - **Factual grounding / occupancy / prior-art** — the panel runs Q&A/UNGROUNDED (only the gateway lanes are
    structurally tool-free; the agy/codex lanes are *asked* not to use tools but are tool-CAPABLE), so treat all
    panel output as ungrounded reasoning that may hallucinate citations. Grounding stays on the dedicated
    tool-enabled paths (`agy research`, Playwright→Pro DeepResearch, web search).
  - **The claim boundary (`/adversary` CLAIM_STANDS)** — stays the disciplined **independent** check
    (Codex hook · `agy:review` Gemini · human). The panel is a **PROPOSER**; a Claude-heavy panel (Sonnet)
    shares the judge's family and is not a valid independent substrate for granting a claim.
- **TIER it:** full panel only on high-value forks (mechanism design, 一区 selection, hard problem-finding).
  Routine = solo Opus; medium = Opus + 1 advisor. Not every command.

## 6. Independence hygiene (protect the one invariant)
- Panel **proposes** → Opus **decides** → the independent **judge** of a resulting *claim* must be a model that
  did **not** co-propose it. If GPT-5.5 was in the panel, the independent claim-reviewer = **Gemini (`agy:review`)**
  or the human — not codex-GPT-5.5 again. Two independent judge-lanes now exist (Codex + agy:review), so we can
  always pick one that didn't co-propose.

## 7. Pre-flight validation (before ANY wiring)
1. Query the OpenCode gateway `/models` (apikey1) → record the **exact model IDs** for DeepSeek V4 Pro,
   Sonnet 4.6, MiMo V2.5 Pro. (These IDs are unknown until checked — the plan assumes they're served there.)
2. Confirm `agy "ping"` returns a Gemini 3.1 Pro answer; confirm `codex exec "ping"` returns synchronously.
3. **Smoke test:** one real `/forge`-style question through all 5 advisors + the Opus reconciliation; eyeball
   the dispute map for genuine heterogeneity (are Sonnet & Opus just echoing?).
4. **Degradation test:** kill one advisor mid-run; confirm Opus proceeds with the rest.

## 8. Cost / latency discipline
Per panel = 5 advisor calls (parallel) + 1 Opus synthesis. Acceptable on high-value ideation; **not per-turn.**
Levers: parallel fan-out · ≤600-tok advisor outputs · high-value-turns-only · graceful degradation ·
byte-stable prefix. The pipeline is already latency-sensitive (subagent-dense sessions run slow) — tiering is
not optional.

## 9. Integration point (FUTURE — do not wire yet)
When approved: the panel becomes the engine behind `/prospect` Mine + `/forge` candidate-generation — it
augments (does not replace) the current single-Pro dispatch with a 5-advisor fan-out + Opus reconcile. Build =
a small parallel dispatcher (`moa_ask.sh` per model + a fan-out wrapper) + the §4 reconciliation template,
codified into `operating-manual.md` §1. All keys already in `/home/lingxufeng/huggingface/.env`
(`OpenCode-APIKEY1`, `OpenCode-URL`; `agy`/`codex` auth already configured).

## 10. Tooling status for the advisor lanes (2026-07-04 — verified live)
- **`agy` (Gemini 3.1 Pro):** ✓ installed + authenticated (agy v1.0.16, antigravity plugin v0.16.1); locked via
  `alias agy='/home/lingxufeng/.local/bin/agy --dangerously-skip-permissions --model gemini-3.1-pro'`. Q&A lane ready.
- **`codex` (GPT-5.5):** ✓ present (`/usr/bin/codex`); Q&A via `codex exec` (force synchronous capture).
- **`agent-browser` MCP — the GPT-5.5-Pro browser lane (Playwright replacement):** ✓ **VERIFIED WORKING** —
  launches its **own** Chrome (no Playwright collision), typed tools + stable-ref accessibility snapshots
  (`snapshot` → `ref=e1` handles) = far more ergonomic than Playwright's painful turn-by-turn control. 8 tool
  profiles (`core` active = 29 tools; `state` = auth / Chrome-profiles / saved state; `network`/`debug`/`react`/…).
  **★ REMAINING GAP: ChatGPT auth** — the launched Chrome is NOT logged in (`restoreStatus: not_configured`); to
  drive Pro it needs the `state` profile (relaunch `--tools core,state`) + a one-time **headed login-and-save**
  (then `restore` on future runs) OR an existing logged-in Chrome profile.
  **RECOMMENDATION:** migrate the GPT-5.5-Pro hand-off Playwright → agent-browser once auth is wired — fixes the
  "every control is 煎熬" problem and makes the Pro advisor lane reliable. (Config change — held pending approval.)
- **`find-skills`:** ✓ installed (skill-discovery — "find a skill for X").
- **DeepSeek V4 Pro / MiMo V2.5 Pro:** ⏳ API-only via OpenCode gateway (`OpenCode-APIKEY1`) — pre-flight: confirm exact model IDs.

## Open questions for the human (before wiring)
1. **Exact OpenCode model IDs** for DeepSeek-V4-Pro / Sonnet-4.6 / MiMo-V2.5-Pro on the gateway?
2. **MiMo route:** OpenCode gateway, or its own `Mimo_API_KEY`/`Mimo_API_URL`? (both exist in `.env`)
3. **Dispute map:** surface it every panel run (auditable), or only the final answer + map-on-request?
4. **Sonnet 4.6:** keep it (extra sample, low heterogeneity) or swap for a more orthogonal model (e.g. Kimi K2.6,
   which is in `.env` as `KIMI_API_KEY1`)? — I'd lean swap, for cleaner error-complementarity.
