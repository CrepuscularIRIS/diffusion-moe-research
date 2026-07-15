# MoA lane bindings (project file — BINDINGS ONLY)

> **The protocol lives in ONE place:** research-os `skills/conductor/references/moa-routing.md`
> (router steps · per-advisor output contract · chain rounds · reconstruction mode · reconcile
> discipline · reversibility tiering · family-quorum liveness precheck · instance-level
> differentiation · bank-first mechanical precondition). This file carries only what the skill
> cannot know: which lanes exist, their honesty properties, and the scripts that fire them.
> Duplicating protocol text here is a drift bug — delete it on sight.

## Scripts
- **Liveness precheck (run BEFORE any full panel): `moa/moa_ping.sh`** — 1-word probe to every lane,
  exit 3 on family-quorum fail. Mechanizes the routing skill's precheck; panels silently degraded to
  2/6 lanes for days before this existed (2026-07-13 audit) — liveness is measured, never assumed.
- Panel (breadth): `moa/moa_panel.sh --per-lane <dir>` (per-instance prompts `<dir>/<lane>[-k].txt`,
  written by the conductor per the routing skill) · shared-prompt mode: `moa/moa_panel.sh <prompt-file>`.
  Post-run footer reports how many families actually ANSWERED (warns below quorum).
- Chain (depth): `moa/moa_chain.sh <chain-dir>` — rounds per the skill's ceiling rule.
- Single lane: `moa/moa_ask.sh <lane> <prompt-file>` (also how the forensic lane fires).
- Selection jury: `moa/moa_jury.sh <packet-dir>` — the `/prospect` SELECTION-JURY binding (lane section below).
- Literature: `moa/moa_lit.sh "<question>" [--deep] [--out] [--resume <dir> <scholar-results-file>]` — the librarian lane (lane section below).
- Substrate + roster: the mimo/deepseek/qwen lanes + jurors + librarian run as OpenCode agents
  (advisors/jurors structurally tool-free; librarian bash+webfetch only; the gemini juror stays on
  agy) — roster, agent contracts, and invocation recipes live in `~/cli/opencode-moa/` (README).
  SCOPE (user directive 2026-07-14): the OpenCode-MoA layer carries ONLY the three OpenCode-Go
  models (deepseek-v4-pro · mimo-v2.5-pro · qwen3.7-plus). Opus 4.6 (`claude -p`) and Gemini 3.1 Pro
  (`agy`) stay in their native CLIs — never folded into the OpenCode runtime.
- Domain bank (bank-first precondition): `WorldModel/wm-operator-bank-report.md` (§B signature map ·
  §K index · §G anti-patterns; discount §G matches at reconcile) · fallback `opus-pass/operators.md`.

## Panel lanes (5 FAMILIES — codex REMOVED 2026-07-13; kimi REMOVED from the layer 2026-07-14 per scope directive) — HONEST
| lane | binding | honesty |
|---|---|---|
| mimo / deepseek / qwen | OpenCode advisor substrate — `opencode run --dir ~/cli/opencode-moa/advisors --agent advisor -m <model> --format json`; mimo = `opencode-go-2/mimo-v2.5-pro`, deepseek = `opencode-go-2/deepseek-v4-pro` (→flash fallback, tagged), qwen = `opencode-go-2/qwen3.7-plus`. These THREE are the entire OpenCode-MoA layer (user directive 2026-07-14 — no other models on OpenCode). | **STRUCTURALLY tool-free** (`mode: primary`, ALL tools permission-denied — denial VERIFIED live 2026-07-14), reasoning ON. Cold-run overhead ~6–9s. |
| gemini | `agy --dangerously-skip-permissions --model "Gemini 3.1 Pro (High)"` (agy takes DISPLAY names; `MOA_GEMINI_MODEL` overrides) — native CLI, NOT on OpenCode | TOOL-CAPABLE / AGENTIC — the "no tools" prompt line is a soft request, not enforcement (tool-free upgrade would require zen billing, but the scope directive keeps Gemini on agy regardless) |
| opus46 | Claude Code `claude -p --model claude-opus-4-6` (env `MOA_OPUS46_MODEL` overrides) — native CLI, NOT on OpenCode | same-family as the conductor — discount Claude-family correlation at reconcile (stays on `claude -p` per the scope directive — not folded into OpenCode) |

**Multi-instance parallelism (replaces the codex lane's breadth):** each family fields SEVERAL
parallel instances with DELIBERATELY DIFFERENTIATED prompts — distinct roles, assumptions, and lines
of inquiry per instance, never the same question twice (protocol: moa-routing.md "instance-level
differentiation"). **Default allocation: opus46×3 · gemini×5 · deepseek×3 · mimo×3 · qwen×3**
(≈17 instances / 5 families); the router adjusts per fork. Quorum = ≥4 distinct live FAMILIES —
instances add depth within one prior, only families add independence.

## Selection-jury lane (bound 2026-07-14 — the `/prospect` SELECTION JURY)
`moa/moa_jury.sh <packet-dir>` (packet = cards.md + anchors.md [+ context.md]) → parallel jurors on
the 4 NON-CLAUDE families {deepseek qwen mimo gemini} — the generator (Claude conductor) never
grades its own cards, and opus46 is Claude-family so it is excluded too; the 3 OpenCode-Go advisors
+ gemini(agy) are the full non-Claude set under the scope directive. **Single source of truth:** the
verdict contract lives once in `~/cli/opencode-moa/advisors/juror-contract.md` and `moa_jury.sh`
injects it VERBATIM into EVERY lane's brief (the thin `juror.md` agent delegates to it; gemini/agy —
which has no system prompt — gets the same injected block) — no second copy to drift. Each lane draws
one of four stances 1:1 (venue-reviewer ·
replication-skeptic · builder-of-the-probe · adjacent-field-outsider); the conductor may also pass a
per-lane DOMAIN-OVERLAY (program-chair assignment) which the juror reasons from on top of its stance.
**Verdict contract now embodies the full due-process requirement** (`moa-routing.md §due-process`,
absorbed from PaperJury): per card an evidence-anchored STRONGEST-OBJECTION + a VENUE-MAGNITUDE
significance floor (CLEARS/BELOW-FLOOR) + a THREE-WAY VERDICT {PURSUE · REFINE(+the close-criterion) ·
DROP(+reason)} — a below-floor card is barred from FORCED-PICK — plus a batched MINORS digest and one
CONFIDENCE. This is the "better jury" refill (2026-07-14): the OpenCode selection juror carries the
same due-process rigor as PaperJury, which itself stays on `claude -p`/codex (it needs file access, so
it cannot live on the tool-free OpenCode substrate). Output = `verdicts/<lane>.md` + a mechanical tally
footer; quorum ≥3 of 4 families (`MOA_JURY_QUORUM` overrides) else exit 3 — 3-of-4 keeps a single
dead lane (gemini/agy is the flakiest) from voiding the jury. The jury RANKS, the conductor SELECTs.
Protocol: moa-routing JURY-MODE + §due-process; binding: `moa_jury.sh`.

## Dissection lane (bound 2026-07-14 — the `/prospect` Mine-7 DISSECTION-MODE executor)
Protocol authority = `moa-routing.md` DISSECTION-MODE (adversarial algorithm analysis: experienced-
algorithm-engineer stance, evidence-anchored weaknesses, testable failure hypotheses, minimal
counterexamples). **The packet comes first:** the conductor/executors assemble the cold DISSECTION
PACKET (verbatim update equations · implementation seams with file:line · stated+silent assumptions ·
target task distribution · known anomalies) — advisor lanes are tool-free, so the packet IS their only
evidence; no packet, no round.
Lanes:
- **Panel arm** — the full 5-family panel via `moa_panel.sh`, each lane a distinct algorithmic axis ×
  the engineer stance (standard differentiation rules apply).
- **Parallel GPT-5.6 arm (PRIMARY — LIVE 2026-07-15): `sol` — N parallel `moa_ask.sh sol`
  instances**, each a distinct axis or a distinct paper. Bound to **codex CLI with
  `-m gpt-5.6-sol -c model_reasoning_effort="high"`** (user directive; verified: session header
  reports model+effort, invalid `-m` errors ⇒ flag honored, 2-instance parallel fan-out tested through
  the script). Env overrides `MOA_SOL_MODEL` / `MOA_SOL_EFFORT`. Same tool caveat as the gpt5 lane
  (codex retains shell/MCP — not sandbox-guaranteed tool-free). Fallback if codex-Sol is down: browser
  GPT-5.6 Tab 0 as N separate FRESH chats (context-free, serialized in wall-clock).
The reconcile discards unanchored weaknesses (verbatim-quote rule), prices by regime-of-bite +
STAKES; output = Mine-7 problem cards + counterexample probes.

## Forensic lane (NOT a panel lane — bound 2026-07-13)
| lane | binding | role |
|---|---|---|
| gpt5 (codex) | `codex exec --disable web_search` via `moa_ask.sh gpt5` | **`/autopsy` + `/abduce` consult** — subtle-hidden-error hunting on unexplained results, silent confounds, why-did-this-die forensics. Retains shell/MCP it *could* invoke (not sandbox-guaranteed tool-free). Never sits on a panel; never sets direction (external-verdicts-are-candidates applies). Gateway twin `forensic` agent (gpt-5.3-codex) ships ready but DORMANT (zen billing). |

## Dormant lanes (zen billing — "Insufficient balance" today; fund the zen workspace + flip the model string to wake)
- `brain` agent (gpt-5.6-sol) — design-consult / delegated-modeling lane; the Chrome tab remains the live GPT-5.6 lane.
- ~~`sol` panel lane~~ — **WOKEN 2026-07-15 via codex** (`-m gpt-5.6-sol`, high reasoning) — see the
  Dissection lane above. The zen `brain`-agent path below stays a dormant ALTERNATIVE substrate
  (structurally tool-free, if ever funded).
- `forensic` agent (gpt-5.3-codex) — gateway twin of the codex forensic lane above.
- gemini/opus46 tool-free upgrade — flipping to zen `gemini-3.1-pro` / `claude-opus-4-6` puts them on the structurally tool-free advisor substrate.

## Literature search-review lane (bound 2026-07-14 — the PEER-REVIEW grounding)
| lane | binding | role |
|---|---|---|
| MoA literature | `moa/moa_lit.sh "<question>" [--deep] [--out] [--resume <dir> <scholar-results-file>]` → `librarian` OpenCode operator (bash+webfetch only; paperseek CLI first, arXiv-API fallback — load-bearing, paperseek was fully dead in the live run; wget+pdftotext deep-read ≤5 PDFs) | Structured extraction cards {VENUE/YEAR·CLAIM·METHOD-DELTA·EVIDENCE·RELEVANCE·OCCUPANCY} + SYNTHESIS + honest COVERAGE. Escalation = a `SCHOLAR-QUERIES:` MARKER LINE (not a fence) → conductor runs them in the Scholar tab (browser playbook) → `--resume` feeds results back. TRIAGE-grade; 精读 still seals novelty. **SUPERSEDES `~/cli/paperseek/moa_search.sh` as the bound lit lane.** |
| Browser two-tab | `plan/browser-two-tab-playbook.md` — Tab 0 = ChatGPT (GPT-5.6 review) · Tab 1 = Google Scholar (search→scrape→wget PDF→pdftotext); title-verified tab switch, never navigate-in-place, never close | The standing external-brain + Scholar lanes; the Scholar tab = the librarian's `SCHOLAR-QUERIES` escalation target (and the direct retrieval path when the lit lane is down). |

**Draft-scale peer-review rule (external-brain.md role 4):** a review of an assembled contribution
must be literature-grounded (prior art RETRIEVED this session — this lane — never model memory) and
multi-family (≥1 reviewing family beyond the browser lane: Grok cold-packet, or an MoA panel review
round). GPT-5.6 alone reviewing a draft it helped refine is self-review with extra steps.

## Idea/package review channels (bound 2026-07-14 — the PaperJury pair)
| channel | binding | role |
|---|---|---|
| PaperJury-Claude | `claude -p` + the PaperJury skill (`~/cli/paperjury` — courtroom review engine: N domain reviewers → contestability routing → trial → three-way verdict) | Review channel #1 for idea formulations + experimental packages (pre-writing). |
| PaperJury-Codex | `codex exec` + the PaperJury-Codex twin (github.com/u7079256/paperjury-codex) | Review channel #2 — cross-family second jury on the same cold packet. |

**Absorb, don't reproduce (user ruling):** PaperJury targets complete manuscripts; our object is the
PRE-WRITING idea + experimental package. The absorbed components (evidence anchors · program-chair
domain-overlay assignment · three-way verdict + close-criterion · significance floor · confidence
scrutiny) are canonical in research-os `moa-routing.md` §due-process — that contract governs even
when a channel is down, fired via `moa_ask.sh opus46/gpt5` with a due-process prompt. Both channels
get COLD packets (claim + artifacts, never the proposer's framing). Codex here = the review channel;
its forensic lane (autopsy/abduce) is unchanged; it still never sits on the generation panel.

## Reviewer lane (NOT part of the panel — bound 2026-07-13, scope EXTENDED same day)
Independent review = **Grok** (xAI family) — the CLAIM_STANDS / kill-adjudication /
reconstruction-test substrate of first choice, **and the IMPLEMENTATION reviewer during the
experiment-development stage**: flawed function logic, incorrect control flow, silent
implementation-level bugs in executor-written code route to `grok review` / `adversarial-review`
(not to a Claude-family code-reviewer — cross-family eyes on same-family code). A panel lane never
reviews its own round's output.

*(RESOLVED 2026-07-14, user decision: Grok stays the code-repair + implementation-debugging
specialist COMPLEMENTING Sonnet; replacing Sonnet as primary developer is REJECTED — it would
disrupt the executor worktree protocol, report contracts, and ownership discipline built around
native subagents. Division: Sonnet writes; Grok reviews diffs + debugs implementation-level
failures + takes tightly-scoped delegated repairs via `task`.)*

**Invocation (the conductor runs the companion script DIRECTLY via Bash — the `/grok:review` and
`/grok:rescue` slash commands are interactive wrappers around the same script and are not
auto-invocable mid-loop):**
```bash
GROK_MJS=/home/lingxufeng/.claude/plugins/cache/grok/grok/0.3.0/scripts/grok-companion.mjs
# review (read-only; findings returned as text; verdict line = ship / needs-attention):
node "$GROK_MJS" review [--base <ref>] [--scope auto|working-tree|branch] <focus text>
# adversarial review variant:
node "$GROK_MJS" adversarial-review <focus text>
# delegated investigation/repair (WRITE-CAPABLE by default — full Bash; scope the task text tightly):
node "$GROK_MJS" task [--read-only] [--resume-last|--fresh] [--model <m>] [--effort <low..max>] <task text>
```
CAUTION: `task` without `--read-only` can modify the repo — use `--read-only` for adjudication/analysis;
write-capable runs only for explicitly delegated fixes, and review the diff after. Flag-like text must
not lead the argument list (a `--help`-style token is consumed as focus/task text, not usage).

## Authority (the research-os conductor engine table governs)
MoA GENERATES candidates for the `/forge` backlog **and DECIDES tactical research forks the loop
would otherwise have escalated** (conductor §3 — the human is never a per-cycle decision sink).
**"MoA decides" is scoped by reversibility:** on a REVERSIBLE/tactical fork the conductor EXECUTES
the reconciled panel verdict; on anything direction-scale (pivot, region-close, plan-of-record) the
verdict is a CANDIDATE carded vs ≥2 local alternatives — the two rules never collide because they
apply to different tiers (moa-routing tiering);
GPT-5.6 browser refines the SELECTED design + triages occupancy/novelty/duplication + searches
arXiv live (browser search preferred over API-only scholar lookups); the forensic lane hunts hidden
errors at `/autopsy`/`/abduce`; Grok reviews/adjudicates (claims + implementation); the conductor
decomposes, reconciles, SELECTs. **No single consult sets a plan-of-record** — external proposals
are carded against ≥2 local candidates (audit: refutes 4-for-4, single-consult direction adoptions
0-for-3).
