#!/usr/bin/env bash
# moa_ask.sh — single-shot Q&A to ONE advisor lane; prints that advisor's answer to stdout.
# Part of the MoA advisor panel (design: plan/moa-advisor-panel-design-2026-07-04.md).
#
# Usage:  moa_ask.sh <lane> <prompt-file>
#   PANEL lanes (5 families — see moa_panel.sh):
#     agy CLI:          gemini (Gemini 3.1 Pro)          — native CLI, NOT on OpenCode
#     Claude Code:      opus46 (Claude Opus 4.6)         — native CLI, NOT on OpenCode
#     OpenCode advisor: mimo | deepseek | qwen — structurally tool-free primary agents
#                       (~/cli/opencode-moa/advisors; mode:primary + full permission-deny; verified denial)
#   SCOPE (user directive 2026-07-14): the OpenCode-MoA layer carries ONLY the three OpenCode-Go
#     models above (deepseek-v4-pro · mimo-v2.5-pro · qwen3.7-plus). Opus 4.6 and Gemini 3.1 Pro stay
#     in their native CLIs (claude -p / agy) — never fold them into the OpenCode runtime.
#   DISSECTION lane (LIVE 2026-07-15): sol — GPT-5.6 Sol High via codex CLI (MOA_SOL_MODEL /
#     MOA_SOL_EFFORT override). The DISSECTION-MODE parallel arm: fire N instances concurrently,
#     each a distinct algorithmic axis/paper. Same tool caveat as gpt5 (codex retains shell/MCP).
#   FORENSIC lane (NOT a panel lane since 2026-07-13):
#     codex CLI:   gpt5 — the /autopsy + /abduce consult lane (strong at subtle hidden errors);
#                  fire it single-shot here, never inside a panel round.
#   NOTE: Sonnet 4.6 is the DEVELOPMENT subagent (native `Agent`, model:"sonnet") — NOT a research advisor.
#
#   ⚠ TOOL DISCIPLINE (honest — do NOT assume "pure Q&A" for every lane):
#     • mimo/deepseek/qwen (OpenCode advisor) = STRUCTURALLY tool-free (full permission-deny in agent def).
#       The guaranteed pure-Q&A lanes. MOA_MAXTOK NOT forwarded (opencode run has no --max-tokens flag);
#       timeout guard (MOA_TIMEOUT) still applies.
#     • gpt5 (codex) = web_search DISABLED, but codex RETAINS shell/MCP tools it *could* invoke; for a plain
#       question it answers directly, but it is NOT sandbox-guaranteed tool-free.
#     • gemini (agy) = TOOL-CAPABLE / AGENTIC: --dangerously-skip-permissions AUTO-APPROVES any tool the model
#       invokes. The "answer from your own knowledge, no tools" PROMPT line (router) is a SOFT request only.
#     • opus46 (Claude Code) = Claude-family research advisor lane; in Claude Code proper this is dispatched as
#       an Agent subagent. This wrapper keeps the lane as Opus 4.6 and lets MOA_OPUS46_MODEL override the local
#       CLI model id if the installed Claude CLI uses a different spelling.
#
# Contract: prints the answer to stdout; EMPTY stdout = dead advisor (caller filters/degrades gracefully).
# Diagnostics go to stderr. Env knobs: MOA_MAXTOK (noted above — not forwarded to oc_advisor),
# MOA_TIMEOUT seconds PER-ATTEMPT (default 240; deepseek lane up to 2 models × 3 attempts each).
# deepseek falls back v4-pro → v4-flash; a fallback answer is TAGGED "[fallback-model: …]" so the
# judge can discount it at reconcile.
#
# CONCURRENCY (SQLite lock): parallel opencode run invocations contend on ~/.local/share/opencode/opencode.db
# (WAL). Losers fail fast (~1s) with "database is locked" on stderr and EMPTY stdout. oc_advisor() jitters
# launch (0–2.9s) and retries up to 3× ON LOCK ONLY; non-lock empty = dead lane, never retried.
set -uo pipefail
usage(){ sed -n '2,38p' "$0" | sed 's/^# \{0,1\}//' >&2; }
case "${1:-}" in -h|--help) usage; exit 0;; esac

LANE="${1:?usage: moa_ask.sh <lane> <prompt-file>}"
PF="${2:?usage: moa_ask.sh <lane> <prompt-file>}"
case "$PF" in -*) echo "[moa_ask] prompt path may not start with '-': $PF" >&2; exit 2;; esac
[ -f "$PF" ] || { echo "[moa_ask] prompt file not found: $PF" >&2; exit 2; }
PROMPT="$(cat -- "$PF")" || { echo "[moa_ask] failed to read prompt: $PF" >&2; exit 2; }
[ -n "$PROMPT" ] || { echo "[moa_ask] empty prompt file: $PF" >&2; exit 2; }
TMO="${MOA_TIMEOUT:-240}"

# Temp-file registry: accumulate paths here; EXIT trap cleans them up even on SIGKILL (panel quorum).
_OC_TMPFILES=()
trap 'rm -f "${_OC_TMPFILES[@]}"' EXIT

# --- OpenCode advisor substrate (structurally tool-free primary agents) ---
OC_DIR="${MOA_OC_DIR:-$HOME/cli/opencode-moa/advisors}"
OC_AGENT="${MOA_OC_AGENT:-advisor}"   # moa_jury.sh overrides with juror
oc_advisor(){
  local model="$1" attempt oc_stderr out
  oc_stderr="$(mktemp)"
  # Self-clean via a RETURN trap: oc_advisor is called inside $(...), so a tmpfile registered in the
  # parent's _OC_TMPFILES array (mutated in that subshell) is invisible to the parent EXIT trap and
  # would leak on every OpenCode-lane call. RETURN fires in THIS (sub)shell on every exit path.
  trap 'rm -f "$oc_stderr"' RETURN
  # Jitter launch (0–2.9s): spread so concurrent panel fan-outs don't all hit the SQLite db at t=0.
  local n; n=$((RANDOM % 30)); sleep "$((n/10)).$((n%10))"
  for attempt in 1 2 3; do
    out="$(timeout "$TMO" opencode run --dir "$OC_DIR" --agent "$OC_AGENT" -m "$model" \
        --format json -- "$PROMPT" 2>"$oc_stderr" \
      | jq -r 'select(.type=="text") | .part.text // empty')"
    if [ -n "$out" ]; then
      printf '%s\n' "$out"
      return 0
    fi
    # Retry ON LOCK ONLY — empty without lock signature = dead lane, never hammer it.
    if grep -q "database is locked" "$oc_stderr" 2>/dev/null; then
      if [ "$attempt" -lt 3 ]; then
        echo "[oc_advisor] lock-contention attempt $attempt/3 on $model — retrying" >&2
        sleep "$((attempt))"
        local m; m=$((RANDOM % 30)); sleep "$((m/10)).$((m%10))"
      fi
    else
      break
    fi
  done
  if grep -q "database is locked" "$oc_stderr" 2>/dev/null; then
    echo "[oc lock-contention: gave up after 3 attempts]" >&2
  fi
  # stdout stays empty = dead-lane semantics
}

case "$LANE" in
  # prompts go via STDIN wherever the CLI allows it — a prompt whose first char is '-' (e.g. a "---"
  # markdown divider) would otherwise be parsed as a flag and the 2>/dev/null would hide the death.
  gemini)   ( source ~/.bashrc 2>/dev/null; timeout "$TMO" /home/lingxufeng/.local/bin/agy --dangerously-skip-permissions --model "${MOA_GEMINI_MODEL:-Gemini 3.1 Pro (High)}" -p "$PROMPT" 2>/dev/null ) ;;  # agy takes DISPLAY names (`agy models`); "gemini-3.1-pro" went dead 2026-07-13
  opus46)   ( source ~/.bashrc 2>/dev/null; printf '%s' "$PROMPT" | timeout "$TMO" claude -p --model "${MOA_OPUS46_MODEL:-claude-opus-4-6}" 2>/dev/null ) ;;
  gpt5)     tmp="$(mktemp)"; _OC_TMPFILES+=("$tmp"); printf '%s' "$PROMPT" | timeout "$TMO" codex exec --disable web_search --skip-git-repo-check --output-last-message "$tmp" - >/dev/null 2>&1; cat "$tmp" 2>/dev/null ;;  # tmp registered for EXIT-trap cleanup (survives SIGTERM); skip-git-repo-check + stdin prompt ("-") works from ANY cwd/content
  mimo)     oc_advisor opencode-go-2/mimo-v2.5-pro ;;
  deepseek)
    out="$(oc_advisor opencode-go-2/deepseek-v4-pro)"
    if [ -z "$out" ]; then
      out2="$(oc_advisor opencode-go-2/deepseek-v4-flash)"
      if [ -n "$out2" ]; then
        printf '[fallback-model: deepseek-v4-flash]\n%s\n' "$out2"
      fi
    else
      printf '%s\n' "$out"
    fi
    ;;
  qwen)     oc_advisor opencode-go-2/qwen3.7-plus ;;
  sol)      # LIVE 2026-07-15: GPT-5.6 Sol High via codex CLI (verified: session header reports model+effort;
            # invalid -m errors ⇒ flag honored; parallel fan-out tested). The DISSECTION-MODE parallel arm.
            # Zen `brain` agent stays a dormant ALTERNATIVE substrate (structurally tool-free if ever funded).
    tmp="$(mktemp)"; _OC_TMPFILES+=("$tmp")
    printf '%s' "$PROMPT" | timeout "$TMO" codex exec -m "${MOA_SOL_MODEL:-gpt-5.6-sol}" \
      -c model_reasoning_effort="\"${MOA_SOL_EFFORT:-high}\"" \
      --disable web_search --skip-git-repo-check --output-last-message "$tmp" - >/dev/null 2>&1
    cat "$tmp" 2>/dev/null
    ;;
  *) echo "[moa_ask] unknown lane: $LANE" >&2; exit 2 ;;
esac
