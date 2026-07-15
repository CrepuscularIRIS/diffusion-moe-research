# Comet Adoption + Plugin/Review Cleanup — Plan (2026-07-09)

> Follows `plan/runtime-harness-decision-2026-07-09.md` (verdict: adopt comet, don't build; simplify → enforce)
> and `plan/workflow-audit-2026-07-09.md`. This is the execution plan for (a) trimming plugins, (b) the
> post-codex review architecture, (c) adopting comet as the enforcing harness.

## 1. Plugin dependency — the factual finding (answers "does MoA need the plugins?")

**MoA scripts invoke CLI BINARIES via bash, not the Claude Code plugins.** Evidence `moa/moa_ask.sh:59-64`:
- `gemini` → `~/.local/bin/agy --model gemini-3.1-pro -p` (the **agy CLI**)
- `gpt5` → `codex exec --disable web_search ...` (the **codex CLI**, `/usr/bin/codex`)
- `opus46` → `claude -p --model claude-opus-4-6`
- `mimo|deepseek|qwen` → OpenCode gateway via `curl`

The `codex` (`/usr/bin/codex`, npm `@openai/codex`) and `agy` (`~/.local/bin/agy`) binaries are installed
**independently of the Claude Code plugins** (`~/.claude/plugins/`). CLI auth (`~/.codex/auth.json`) is also
plugin-independent.

**⇒ Removing the `openai-codex` and `antigravity-for-claude-code` PLUGINS does NOT break MoA, as long as the
`codex` + `agy` CLI binaries stay on PATH.** MoA is bash-triggered CLIs, full stop.

## 2. Plugin rationalization (currently 8 plugins — "too many")

| Plugin | Verdict | Reason |
|---|---|---|
| `openai-codex` | **REMOVE** | misbehaving this session (hook hang ≤90s, 271 broker leak, fail-safe defect). Keep `/usr/bin/codex` CLI. |
| `antigravity-for-claude-code` | **REMOVE** | misbehaving per user; MoA uses the `agy` CLI directly, not the plugin. Keep `~/.local/bin/agy` CLI. |
| `claude-plugins-official` (superpowers) | **KEEP** | the skills we actually use (debugging, brainstorming, code-review). |
| `planning-with-files` | keep (light, used) | |
| `chrome-devtools`, `coral`, `pua-skills`, `anthropic-agent-skills`, `voltagent-subagents`, `arescope-gemini` | **AUDIT → remove unused** | user decides per actual use; each unused plugin is context + trigger surface. |
| research-os (skills at `~/.claude/skills`) | **KEEP** | the loop. |

**Acceptance:** after removal, `bash moa/moa_panel.sh gemini gpt5` still returns answers (CLIs intact); no
`/codex:*` or `/antigravity:*` command is referenced by any live doc.

## 3. Review architecture after dropping the codex plugin — DON'T collapse independence

There are **two distinct review roles**; the user's "Opus 4.8 subagent review" is right for one and wrong for the other:

- **Dev / diff review (catch bugs in a change)** → a Claude Code **Opus 4.8 subagent + the `code-review`
  skill / `code-reviewer` agent**. Same-family is FINE here — it's quality review, not a claim grant. This
  cleanly replaces the misbehaving codex review hook. ✅ (deliberate/manual, no auto-hook.)
- **`CLAIM_STANDS` — the one invariant (granting a research claim holds)** → STILL requires a **CROSS-FAMILY,
  non-proposer** substrate. **Opus-reviews-Opus is NOT independent** (both audits + the MoA design doc:
  a same-family reviewer cannot grant a claim; audit P1.5: a co-proposer can't validate its own claim). So:
  - **Primary = context-free GPT-5.6** (Playwright→ChatGPT, high-reasoning) — cross-family (vs Opus) AND
    stateless per query = a genuinely independent verifier (see §6). Frame the query to REFUTE
    (proof-by-contradiction). Alternates: **`agy` (Gemini)** or **`codex exec` (GPT CLI)** — bash-triggered,
    no plugin needed.
  - Reviewer-provenance rule (audit P1.5): if a model co-proposed the node, route its claim review to a
    DIFFERENT family or human. Context-free reduces contamination, but same-MODEL still shares systematic
    biases, so the highest-stakes claims prefer cross-family.

**Net:** review = skill-driven + bash-triggered CLIs. No misbehaving plugins/hooks. Dev-review Opus-subagent;
claim-review cross-family CLI. This is consistent with this session's earlier "auto-hook removed → manual"
decision, and it preserves the independence the invariant needs.

## 4. Comet adoption (the enforcing harness — adopt, don't build)

**Prerequisite (do FIRST):** Phase-1 simplify from the decision doc — collapse duplicated authorities to a
one-page invariant-set. A harness on a bloated doc-set enforces the wrong thing.

**Adoption steps:**
1. **Spike** — install/read `@rpamis/comet`; understand its `.comet.yaml` state-machine + `comet-guard.mjs`
   phase-guard mechanism + resumability. Map our loop (`prospect→forge→prereg→run→exp-verify→adversary→
   autopsy`) onto comet phases; decide: full adopt vs. borrow only the guard pattern.
2. **Wire the ~6 HARD invariants as executable guards** (comet guards OR a git-hook + scripts):
   - `.arbor/active-run` == current campaign before any node write.
   - No claim-run without a sealed `/prereg` artifact (reproduce-first ordering baked in).
   - No `CLAIM_STANDS` without a **non-proposer, cross-family** verdict artifact (§3).
   - No secret in argv (audit P0.4).
   - A monitor-registry entry exists for every outliving wait (audit P2.2).
3. **Stop there.** If the guard set grows past a page, it's re-accreting.

**Guardrail:** time-boxed; the deliverable stays the **MM-OVSeg reproduction**, not the harness.

## 5. Sequence

0. **DONE (2026-07-10):** `openai-codex` + `antigravity-for-claude-code` plugins REMOVED (their agents are
   gone); AgentMemory MCP disconnected → file-memory is now the sole memory layer (fine — it's canonical).
   Security (P0.4 token-in-argv) DEFERRED per user.
1. **Phase 1 (simplify):** collapse authorities, close P0 drift (Arbor active-run, reproduction contract,
   ordering, stale hook-refs), **collapse the browser lanes to one GPT-5.6 lane (§6)**, stand up the review
   skills (§3).
2. **Phase 2 (comet):** spike → adopt/borrow → wire the ~6 guards.
3. **Then:** resolve the MM-OVSeg HF asset gate and run the reproduction — the actual work.

## 6. External-brain strategy — GPT-5.6 high-reasoning, context-free (2026-07-10)

**Change:** retire **GPT-5.5 Pro (`Pro 扩展`)** as the primary external brain — slow, and not measurably
better. **Primary external brain = GPT-5.6 in high-reasoning mode** (Playwright→ChatGPT), interacted with
**iteratively** as needed.

**Collapse two browser lanes → ONE GPT-5.6 lane, three roles** (was `Pro 扩展` deep + `超高` occupancy):
1. **Search + triage (breadth) — the browser's real STRENGTH.** The Chrome extension has a stronger
   browsing/search experience (genuine web access) than local tools → use it as the wide-net searcher and
   "has this been done?" occupancy scout (replaces `超高`). **But it triages on HIGH-LEVEL SIGNALS ONLY —
   abstracts, keywords, citations, venue, recency — and must NOT close-read papers.** Output = a candidate
   list + triage signals, never "papers read" or a novelty verdict.
   → **Research-OS/Opus decides which papers to DOWNLOAD; 精读 (close reading) happens LOCALLY** — the
   faithful substrate that seals novelty. The browser never self-certifies novelty or does detailed analysis
   (parametric-hallucination risk).
2. **Proposal / claim review = the independent substrate** — see §3. Cross-family + stateless.
3. **Research-OS workflow execution** — delegate the GENERATIVE + REVIEW workflows (`/prospect` mining,
   `/forge` design, `/autopsy` next-candidate, `/adversary`) to GPT-5.6. Keep `/prereg`, `/exp-verify`, and
   the `run` LOCAL (tightly coupled to artifacts + the sealed eval; must not leave the machine).

**Why context-free is a FEATURE (the design principle, endorsed):** GPT-5.6 here carries almost no persistent
context — it interacts through prompts only. That is desirable: no accumulated conversational context forces
each query to reason **from first principles / by proof-by-contradiction**, instead of pattern-matching on the
proposer's framing. A fresh, uncontaminated mind per query is exactly what independent **review**,
**verification**, and **retrieval** need. This is the cleanest fix for the CLAIM_STANDS independence problem:
a context-free cross-family model cannot be biased by the proposer's context.

**Enabler + discipline:** because GPT-5.6 has no memory of the campaign, the Opus main agent must package a
**complete, self-contained prompt** each query (the existing "compact Opus-packaged hand-off" discipline —
never a repo dump). Iterate within a query when a problem needs drilling; start fresh per new problem.

**Decompose, don't single-shot (applies to MoA AND all follow-up / iterative analysis).** Opus/MoA DECOMPOSES
a problem into MULTIPLE TARGETED GPT-5.6 queries — each a sharp, self-contained sub-question — rather than one
broad query, and iterates follow-ups as the analysis deepens. Fan out across the many models/tools now
available (GPT-5.6 browser + the MoA panel); **multi-model × multi-query diversity is the idea-quality
dividend**, and Opus reconciles the returns (dispute-map: consensus / conflict / unique-insight / blind-spot).
This is the MoA 6-round chain pattern extended to the GPT-5.6 browser lane.

**Independence guardrail (preserved):** context-free ≠ fully independent of the model's own systematic biases.
For the highest-stakes `CLAIM_STANDS`: prefer a DIFFERENT family than the proposer (GPT-5.6 co-proposed ⇒
review via `agy`/Gemini or human), or at minimum a fresh GPT-5.6 query framed to REFUTE.

**Doc impact (folds into Phase-1 simplify):** `CLAUDE.md §1` + `moa/router-protocol.md` + `operating-manual`
browser-lane rules collapse from two lanes to one GPT-5.6 high-reasoning lane (retrieval + review +
workflow-exec). Net SIMPLIFICATION — fewer lanes, one clear external brain.
