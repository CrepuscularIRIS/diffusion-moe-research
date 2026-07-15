# OpenCode-MoA Layer — Architecture + Implementation Plan (2026-07-14)

> **Authority:** user directive 2026-07-14 (recorded as ledger row W8 at completion): migrate the MoA —
> panel advisors, the selection jury, literature intelligence — onto OpenCode agents; each instance a
> named role with a maintained system prompt; keep the pipeline clean, minimally intrusive, de-gated.
> Selection Jury runs on the OpenCode-MoA lane; `claude -p` + codex stay reserved for artifact-grounded
> due-process reviews (PaperJury channels). Research-os skills are NOT edited (verified: zero
> lane-specific references in `~/cli/research-os/skills/` — lanes live in bindings only).

**STATUS 2026-07-14:** T1–T5 shipped + reviewed (see `.superpowers/sdd/progress.md`); T6 = bindings sync.

**SCOPE CORRECTION 2026-07-14 (user directive — supersedes the kimi rows below):** the OpenCode-MoA
layer carries ONLY the three OpenCode-Go models — deepseek-v4-pro · mimo-v2.5-pro · qwen3.7-plus.
**kimi (`opencode-go/kimi-k2.6`) was REMOVED from the layer** (out of `moa_ask.sh`, `moa_ping.sh`,
`moa_jury.sh`, roster README). Consequences applied: panel = 5 families (kimi-not-in-`moa_panel.sh`
is now the correct state, not a gap); jury = 4 non-Claude families {deepseek qwen mimo gemini} with
quorum lowered 4→3 (`MOA_JURY_QUORUM`). Opus 4.6 stays on `claude -p`, Gemini 3.1 Pro on `agy` —
never folded into the OpenCode runtime. The "6 families / kimi 6th" language in §2–§3 below is
HISTORY, retained for provenance only.

## 0. Verified facts the design rests on (scout 2026-07-14, empirical)

| fact | consequence |
|---|---|
| Agents = `.opencode/agents/<name>.md` (frontmatter: description·mode·model·temperature·permission map); filename = agent name | roster is a directory of small markdown files — Superpowers-style |
| Tool-free is STRUCTURAL only for `mode: primary` agents; `opencode run --agent <subagent>` silently falls back to the tool-armed `build` agent | **every MoA agent is `mode: primary`**; T1 verifies denial empirically |
| Project `opencode.json` merges over global; per-server `{"enabled": false}` + `"lsp": false` kills the 6 global MCP servers | lean project dirs → cold `opencode run` ~8–9s (vs 1m52s full config) — acceptable; **no persistent server** (session-accumulation + no `--dir` gotchas avoided) |
| `opencode` (zen) provider models — claude-opus-4-6 · gemini-3.1-pro · gpt-5.6-sol · grok-4.5 — all return *Insufficient balance*; `opencode-go`/`opencode-go-2` keys work | today's tool-free substrate = **qwen3.7-plus · deepseek-v4-pro · mimo-v2.5-pro · kimi-k2.6** (4 families). Zen families = a DORMANT one-line flip (fund account → edit model strings) |
| `--format json` → NDJSON; final text = `jq -r 'select(.type=="text") | .part.text'`; no stdin; `"$(cat file)"` + `--` for flag-like prompts | moa_ask extraction contract |
| kimi-k2.6 also serves on the raw `go` gateway curl | raw-curl fallback lane possible for kimi if opencode breaks |

## 1. Architecture (three layers, one new directory)

```
~/cli/opencode-moa/                      NEW — the mind roster (git repo)
├── advisors/                            lean project: lsp:false, ALL global MCP disabled
│   ├── opencode.json
│   └── .opencode/agents/
│       ├── advisor.md                   MoA panel member (generic; differentiation stays in the
│       │                                per-instance prompt files per moa-routing — one agent, many prompts)
│       ├── juror.md                     selection-jury member (verdict contract from prospect §select-2)
│       ├── forensic.md                  hidden-error hunter role (DORMANT until zen billing; codex CLI
│       │                                remains the live forensic lane)
│       └── brain.md                     GPT-5.6-sol design-consult role (DORMANT until zen billing;
│                                        Chrome tab remains the live GPT-5.6 lane)
├── operators/                           lean project: MCP disabled, tools scoped per agent
│   ├── opencode.json
│   └── .opencode/agents/
│       └── librarian.md                 literature intelligence (paperseek + arXiv API + pdftotext;
│                                        bash/webfetch allowed; emits STRUCTURED cards, not dumps)
└── README.md                            roster map + invocation recipes + billing-flip instructions

huggingface/moa/                         UNCHANGED INTERFACE — the lanes
├── moa_ask.sh                           lane map refit: mimo/deepseek/qwen → opencode advisors;
│                                        + kimi lane; gemini/opus46/gpt5 unchanged (billing)
├── moa_ping.sh                          + kimi in the panel array
├── moa_panel.sh / moa_chain.sh          UNTOUCHED (they route through moa_ask.sh)
├── moa_jury.sh                          NEW — selection-jury fan-out (see §3)
├── moa_lit.sh                           NEW — librarian invocation wrapper (supersedes
│                                        paperseek/moa_search.sh as the bound lit lane)
└── router-protocol.md                   bindings tables updated (T6)
```

**Invocation pattern (all lanes):**
`opencode run --dir ~/cli/opencode-moa/<proj> --agent <role> -m <provider/model> --format json -- "$(cat prompt)"`
piped through the jq text-extractor. Empty stdout = dead lane (existing contract preserved).

## 2. Lane map (today → after zen billing)

| lane | today | honesty today | after billing flip |
|---|---|---|---|
| qwen / deepseek / mimo | opencode `advisor` @ opencode-go-2 models | STRUCTURALLY tool-free (verified primary-agent denial) | unchanged |
| kimi (NEW 6th family) | opencode `advisor` @ opencode-go/kimi-k2.6 | structurally tool-free | unchanged |
| gemini | agy CLI (unchanged) | tool-capable caveat REMAINS | → `advisor` @ opencode/gemini-3.1-pro (tool-free) |
| opus46 | claude -p (unchanged) | same-family discount | → `advisor` @ opencode/claude-opus-4-6 |
| gpt5 (forensic) | codex exec (unchanged) | retains-shell caveat REMAINS | → `forensic` @ opencode/gpt-5.3-codex |
| sol (NEW, dormant) | — (browser tab is the live GPT-5.6) | — | → `brain` @ opencode/gpt-5.6-sol — scriptable delegated-modeling briefs |
| grok | companion plugin (reviewer, unchanged) | repo-access by design | (optional) cold-packet juror @ opencode/grok-4.5 |

Panel quorum rule unchanged (≥4 distinct live families); kimi raises the family pool to 6.

## 3. Selection Jury (`moa_jury.sh <packet-dir>`)

- Packet dir: `cards.md` (full annotated card set) + `anchors.md` (taste anchors) + optional `context.md`.
- Fan-out IN PARALLEL to the `juror` agent × the **non-Claude families**: qwen · deepseek · mimo · kimi
  (+ gemini via agy until billing flips it) — the generator (Opus conductor) is structurally excluded
  from grading its own cards; Claude-family jurors would be same-family correlation on exactly the
  verdict that must be independent.
- Juror system prompt carries the verdict contract permanently (prospect §select-2): per card
  {strongest objection · likeliest failure mode · prior-work differentiable? · venue-plausible
  magnitude · REFINEMENT DEMAND} + forced pick 2–3 + anchor-sanity self-check.
- Output: `<packet>/verdicts/<family>.md` + mechanical footer (families answered / quorum warning /
  forced-pick tally). **Synthesis stays with the conductor** (jury RANKS, conductor SELECTs — the
  aggregator is the strong judge, per MoA design; no aggregation agent).

## 4. Literature intelligence (`librarian` + `moa_lit.sh`) — and the Scholar integration

`moa_lit.sh "<question>" [--deep] [--out <dir>]` → librarian agent (operators project). Its system
prompt encodes the WORKFLOW, not just retrieval:
1. Generate 3–5 diverse queries; run paperseek CLI (venv per moa_search.sh conventions); on
   paperseek failure/thinness fall back to the arXiv API (webfetch/curl) — paperseek is known-buggy,
   triage-grade (router-protocol).
2. For the top hits: wget PDF → pdftotext → read abstract+method (the 精读-prep pipeline).
3. Emit **structured extraction cards** — per paper: {title · venue/year · one-sentence claim ·
   method delta · evidence strength · relevance-to-question · occupancy implication} + a synthesis
   paragraph + a coverage-honesty line (what was NOT searchable this run).
4. **Scholar escalation contract:** the librarian cannot drive Chrome (single logged-in browser,
   owned by the conductor). When its API lanes are insufficient it ends its card set with a fenced
   `SCHOLAR-QUERIES:` block (exact query strings + what each would settle). The conductor executes
   them in Tab 1 per `plan/browser-two-tab-playbook.md` and feeds results back on a second
   `moa_lit.sh --resume <dir>` pass. Scholar becomes a defined escalation lane with a machine-readable
   handoff — integrated, not isolated.

## 5. What deliberately stays OUTSIDE OpenCode (and why)

- **Grok companion** — user-ruled implementation-review/repair specialist; needs repo access by design.
- **PaperJury channels** (`claude -p`, codex) — artifact-grounded due-process reviews need file access;
  gateway lanes are structurally tool-free (that is their honesty value, not a limitation).
- **Chrome two-tab** — live-retrieval-grounded external-brain work (novelty/occupancy triage, live
  arXiv) needs real browsing + the user's logged-in identity; also the only live GPT-5.6 until billing.
- **Sonnet executors** — native Agent worktree protocol untouched.
- **Arbor writes** — conductor-only (honest-evidence invariant). Arbor MCP stays DISABLED in both MoA
  projects; an `arbor-scribe` operator is a future adapter, deferred by the admission criterion (no
  current use case — advisors must not write research state).

## 6. Tasks (SDD; global constraints below)

- **T1 scaffold** — dirs + configs + git init + README skeleton. VERIFY: lean cold-run ≤15s; primary-agent
  tool-denial reproduced; `agent list` sees roster; `-m` overrides frontmatter model.
- **T2 roster** — the 5 agent .md files + README roster section. VERIFY: each live agent answers a probe
  in role; juror emits the verdict block on a 2-card toy packet; dormant agents carry billing notes.
- **T3 lane refit** — moa_ask.sh (3 lanes re-pointed + kimi + sol stub error) + moa_ping.sh (+kimi).
  VERIFY: `moa_ping.sh` all-lanes live table; per-lane spot answers; empty-stdout-on-dead preserved.
- **T4 jury** — moa_jury.sh per §3. VERIFY: toy packet (2 real-ish cards + 1 known-bad anchor card) →
  4-family verdicts parse, footer correct, known-bad ranked last (anchor sanity).
- **T5 librarian** — librarian.md + moa_lit.sh per §4. VERIFY: one live query end-to-end (cards + honest
  coverage line; SCHOLAR-QUERIES block appears when forced by --no-paperseek test flag or natural gap).
- **T6 bindings sync** — router-protocol.md lane tables (§2 map incl. dormant rows) + jury + lit-lane
  sections; CLAUDE.md §2 engines; memory file + MEMORY.md; ledger row W8; plan/README row.

**Global constraints (binding for every task):**
1. `moa_panel.sh` / `moa_chain.sh` are NOT edited; the moa_ask.sh lane interface (`<lane> <prompt-file>`,
   answer on stdout, EMPTY = dead, diagnostics on stderr, MOA_MAXTOK/MOA_TIMEOUT env) is preserved exactly.
2. Every MoA agent is `mode: primary`. Advisors project: `lsp:false` + all six global MCP servers
   `enabled:false` + full permission-deny (bash·edit·webfetch·task·todowrite·websearch·lsp·skill: deny).
3. No new secrets; providers come from global opencode.json; never print keys.
4. Scripts: bash, `set -uo pipefail`, ≤ ~120 lines each, header comment = usage + contract (house style
   of the existing moa scripts). Agent files ≤ ~60 lines.
5. Dormant lanes fail LOUD and helpful (`[lane sol] DORMANT: zen billing — see README`) — never a
   silent empty that mimics a dead advisor.
6. `opencode run` sessions accumulate in `~/.local/share/opencode/opencode.db` — README documents this
   + the prune recipe; scripts do not attempt auto-cleanup (user data).

## 7. Risks / gotchas carried from the scout
`--path .opencode` (not `.`) for agent create; `--` guard for flag-like prompts; subagent-mode silent
fallback (the reason for constraint 2); config MERGE semantics (disable each MCP server BY NAME);
title-generation adds one small call per run (accepted).
