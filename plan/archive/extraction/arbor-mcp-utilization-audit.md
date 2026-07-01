# Arbor + MCP Utilization Audit (2026-06-29)

> Question: are the other Arbor commands and the MCP servers being fully used? Short answer: we use the
> **structure** layer well; the **automation** layer is dormant *by design* (and only pays off at Track-3
> scale). On MCP, the 3 that matter are used; 2 low-effort additions are worth it for Track 3.

## 1. Arbor MCP tools — used vs dormant
| Tool | Used? | Note / recommendation |
|---|---|---|
| `tree_view` | ✅ heavy | every OBSERVE |
| `tree_add_node` | ✅ | new leads |
| `tree_update_node` | ✅ | every 验收 |
| `tree_prune` | ◑ occasional | kill branches — use more consistently (see operating-manual §6.2) |
| `tree_set_meta` | ◑ PARTIAL | `dataset_info` + `metric_direction` set; **`baseline_score`/`trunk_score`/`test_*`/`eval_cmd` all N/A** → this is what blocks the automation tools below |
| `worktree_create` / `worktree_remove` | ❌ unused | we use Claude Code's `Agent isolation:"worktree"` (`.claude/worktrees/`) instead — **keep ours**; Arbor's is redundant |
| `eval_run` | ❌ unused | manual eval inside subagents. **Adopt for Track 3** once `eval_cmd`+metric are set |
| `git_merge_branch` | ❌ unused | manual git + Codex DECIDE. **Adopt for Track 3** to auto-gate merges on a sealed `B_test` score |
| `generate_report` | ❌ unused | manual RUNLOG + paper drafts. Optional end-of-track `REPORT.md` |
| `open_dashboard` | ❌ unused | optional monitoring |

**Verdict.** The dormancy is causal, not accidental: the automation chain
`tree_set_meta(baseline/trunk/test scores, eval_cmd)` → `eval_run` → `git_merge_branch` → `generate_report`
is gated on populated metadata scores, which we never set (all manual Codex DECIDE). For Track 1/2 (few,
bespoke experiments) that was the *right* call — automation overhead > benefit. **Track 3 changes the math:**
training many small adapter variants is exactly the regime where a populated eval contract + `eval_run` +
auto-merge-on-`B_test` pays for itself. → When variant count grows, populate `tree_set_meta`
(baseline_score, eval_cmd, B_dev/B_test) and turn the automation on. **Not a current blocker.**

## 2. Arbor skills — see operating-manual §6.3
Used: `tree_*` (MCP), `arbor-peer-review-gate`, `/ideate` + `arbor-agent-ideate`. Covered-by-hybrid:
`arbor-agent-search` (→ Pro 扩展 novelty), `setup-intake`/`coordinator` (→ goal-directive + goal mode).
Deliberately unused: `research-agent`/`orchestrator` (full-auto loop — wrong fit for human-in-loop).
Deferred-for-Track-3: `merge-eval` automation, executor `RunTraining` + `resume-report` checkpoint/resume.

## 3. MCP servers — used vs idle
| Server | Used? | Note |
|---|---|---|
| **arbor** | ✅ | tree only; automation dormant (§1) |
| **playwright-extension** | ✅ | the Pro 扩展 channel |
| **agentmemory** | ✅ | memory bridge (Codex hook just fixed) |
| `claude_ai_Claude_Code_Remote` | ◑ | triggers/sessions/repos — used minimally (scheduling) |
| **github** (plugin) | ❌ worthwhile | could automate PR/issue/release when we push the paper + code |
| **context7** | ❌ worthwhile | live library docs (unsloth/transformers/peft) — useful during Track-3 adapter coding |
| chrome-devtools / playwright (plugin) | ❌ | duplicate of the extension — skip |
| figma / google-drive / open-computer-use | ❌ | not research-relevant |
| ldr-mcp (deep-research) | ❌ (disconnected) | overlaps `/ideate`+Pro — skip |
| stagehand | ❌ (disconnected) | browser fallback only |

**Opportunity (low-effort, Track-3-timed):** `context7` for adapter-coding docs; `github` MCP if/when we
push the paper repo. Everything else is used, redundant, or not research-relevant.

## 4. Bottom line
- **Arbor:** structure layer fully used; automation layer dormant-by-design → unlock it (populate
  `tree_set_meta` scores) when Track-3 variant count makes it pay. No current blocker.
- **MCP:** the 3 that matter (arbor, playwright, agentmemory) are used. `context7` + `github` are the only
  additions worth wiring, both minor and Track-3-timed.
- **No ceremony to add now** — this matches the pragmatic-hybrid stance: turn on automation when scale
  demands it, not before.
