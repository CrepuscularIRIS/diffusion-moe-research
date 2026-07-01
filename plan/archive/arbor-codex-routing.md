# Arbor / Codex Routing Policy (for Opus, the research orchestrator)

v0.1 — **Arbor keyless-in-CC.** How Opus drives an Arbor research run *inside Claude
Code* and where it hands reasoning out to **Codex (gpt-5.5)** and to **web GPT-5.5 /
GPT Deep Research** (reached via Playwright/Stagehand). Companion to
`kimi-codex-routing-policy.md` — that policy governs **Superpowers SDD code work**; this
one governs **Arbor research-optimization loops**. Same orchestrator (Opus), different job.

## TL;DR architecture

- **Mode:** Arbor `keyless` — `arbor install` skills + `arbor mcp` deterministic tools.
  **No API key**: the **host model (Claude / Opus) does ALL of Arbor's reasoning** —
  Coordinator *and* Executor. Arbor contributes the durable skeleton only: Idea Tree,
  git-worktree isolation, dev/test discipline, merge guard, report.
- **Consequence:** the native `meta_model` / `agent_model` per-role model split is **inert
  here**. You cannot config "Coordinator=GPT-5.5, Executor=Claude" in keyless — there is
  one host model. So **balancing CC vs Codex is *where you inject a second opinion into the
  cycle*, not a config field.**
- **Three engines:**
  - **Claude / Opus (host)** — drives the arbor cycle, implements Executor diffs, owns the
    Idea Tree via arbor MCP tools. The engine.
  - **Codex (gpt-5.5, via `codex` plugin)** — correctness review of Executor diffs + merge
    decision authority. Same seat it holds in SDD. **Core.**
  - **Web GPT-5.5 + GPT Deep Research (via Playwright/Stagehand)** — novelty / 原创性验证,
    first-principles framing, idea generation, solution design. The **academic-reasoning
    lane**. **Core for science runs.**

## Headline rule

```
Ideation / first-principles / design   → web GPT-5.5 / Deep Research → fold back into IDEATE
Novelty / prior-art / 原创性            → GPT Deep Research  (alphaXiv degrades keyless — don't lean on it)
"Is this experiment worth the compute?" → Codex /codex:rescue  at SELECT
Executor diff correctness               → Codex  (SubagentStop review hook, automatic — see note)
Merge / prune / stop judgment           → Codex /codex:rescue  at DECIDE + Stop-gate
Drive loop · implement · bookkeeping    → Claude / Opus
```

## The arbor cycle → who + how to trigger

| Step | Arbor action | Lead | Trigger |
|------|--------------|------|---------|
| ① OBSERVE | re-read tree / evidence / frontier | **Opus** | — |
| ② IDEATE | propose 1–3 hypothesis branches | **web GPT-5.5 / Deep Research** | before `TreeAddNode`: ask GPT for directions / first-principles probe, then draft the node |
| — novelty | prior-art + 原创性验证 | **GPT Deep Research** | run a Deep Research pass on the hypothesis; paste verdict into the node's `related_work` |
| ③ SELECT | pick the highest-value pending leaf | **Codex** | `/codex:rescue` — "which experiment is worth this cycle's compute?" |
| ④ DISPATCH | Executor implements + runs eval in a worktree | **Opus** implements | run the Executor **as a CC subagent** so the Codex `SubagentStop` review fires on its diff |
| ⑤ BACKPROP | record result + abstract insight upward | **Opus** | — |
| ⑥ DECIDE | merge / prune / stop (held-out test) | **Codex audits** | `/codex:rescue` on the merge call + the gpt-5.5 Stop-gate before promoting trunk |

## Why (grounded)

- **keyless = one host model.** In source, `effective_meta_model = meta_model or llm.model`
  and the orchestrator deep-copies the `llm` block swapping only the model *name* — never
  the provider/base_url. So a keyless run has nothing to split across roles. (verified
  `src/coordinator/config.py`, `src/coordinator/orchestrator.py`)
- **alphaXiv backend "reuses your existing Arbor LLM credentials"** — keyless has none, so
  the built-in literature lane degrades. Use the **web Deep Research** path for 原创性
  instead. (README + `examples/research_config.example.yaml`)
- **CC `SubagentStop` payload does NOT expose the subagent model** (only `agent_id`,
  `agent_type`, transcript path, last message). So the Codex review hook fires on the
  Executor subagent's **diff** regardless of model — gate on **risk + evidence-debt**, not
  on "model == sonnet". (carried over from `kimi-codex-routing-policy.md`)
- **Codex has only `SessionStart/SessionEnd/Stop` hooks** → it is structurally a
  **low-frequency gate**, not a per-step checker (its own README warns of long CC/Codex
  usage loops). Map it to **SELECT / DECIDE gates + the per-subagent Stop review**, never to
  every cycle step.

> **Note — making the auto Codex review fire on Executor diffs:** it only triggers if the
> Executor runs as a **CC subagent** (dispatch via the Task tool). If Opus implements the
> Executor inline in the main loop, `SubagentStop` never fires — then trigger the diff
> review **manually** with `/codex:rescue` at ④.

## Run protocol (keyless, inside CC)

1. **Build the harness with CCC first.** Use gstack/superpowers to produce a clean-git
   target: a runnable `run_eval.py`, a **dev split + a held-out test split**, baseline
   committed. *Arbor optimizes a harness; it does not build one.*
2. `/arbor-research-agent <goal>`. At the **intake checkpoint** set:
   - `scope: novelty-leaning` (science runs) · `interaction_mode: review` (→ `direction`
     → `auto` once trusted)
   - permissions explicit (edit code? run training/GPU? install pkgs? internet?)
   - budget small first (**smoke**), then real; cap `max_cycles`.
3. **Per cycle, route by the table above.** Keep Codex at the gates (SELECT/DECIDE + diff
   review); keep web GPT / Deep Research on the IDEATE + novelty lanes.
4. **Merge guard:** promote `trunk → main` only after the held-out test clears the margin
   **and** a Codex DECIDE pass (`git merge research/run_xxx/trunk`).

## Interaction modes ↔ routing

- `review` — pauses before each node and Executor. This is your hook to call Codex /
  Deep Research. **Start here.**
- `direction` — asks only at ideation; the GPT ideation lane still applies, less friction.
- `auto` — hands-off. Codex still fires automatically on Executor diffs (Stop hook), but
  the GPT ideation/novelty lanes go quiet unless you pre-wire `search.auto_search_on_add`.

## Tradeoffs (be honest)

- keyless **ties up the CC session + usage for the whole run** → this is *supervised*
  research, not fire-and-forget. Mitigate: cheap deterministic eval, small `max_cycles`,
  move to `auto` once you trust the loop.
- web GPT / Deep Research via Playwright is **manual/interactive** — best spent at the
  decision gates (②/novelty/③/⑥), not on every cycle.
- For true unattended long runs, the **native runtime + a unified gateway** (one endpoint
  serving `claude-*` and `gpt-5.5`, set `model`=Claude executor + `meta_model`=GPT-5.5
  coordinator) is the upgrade path. Out of scope while we stay subscription-only/keyless.

## Install state (this machine — 2026-06-24)

- `arbor-agent[mcp]` **0.1.2** — uv tool at `~/.local/bin/arbor` (5 execs:
  `arbor/coordinator/executor/review-research/run-research`).
- Skills (11 each): `~/.claude/skills/arbor-*` and `~/.codex/skills/arbor-*`.
- MCP server `arbor` (`arbor mcp`): Claude → `~/.claude.json` (user scope) ✔ connected;
  Codex → `~/.codex/config.toml` `[mcp_servers.arbor]` ✔ (backup:
  `config.toml.bak-arbor-20260624-*`).
- `arbor doctor`: install ✓, git ✓, **`! no API key` = expected for keyless**.
- Restart Codex to load its new skills + MCP; new CC sessions pick them up automatically.

## Quick reference

```
arbor replay --demo        # watch a recorded run, zero cost
/arbor-research-agent ...   # CC: start a keyless research run (Codex: $arbor-research-agent ...)
arbor web <session>         # read-only browser monitor
arbor report <session>      # re-render REPORT.md
/codex:rescue ...           # hand SELECT/DECIDE/diff reasoning to gpt-5.5
```
