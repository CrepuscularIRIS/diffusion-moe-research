#!/usr/bin/env bash
# moa_ask.sh — single-shot Q&A to ONE advisor lane; prints that advisor's answer to stdout.
# Part of the MoA advisor panel (design: plan/moa-advisor-panel-design-2026-07-04.md).
#
# Usage:  moa_ask.sh <lane> <prompt-file>
#   lanes (agy CLI):     gemini (Gemini 3.1 Pro) | opus46 (Claude Opus 4.6 — the Claude research-advisor)
#   lanes (codex CLI):   gpt5 (GPT-5.5)
#   lanes (OpenCode gw): deepseek | mimo | kimi | glm | qwen | minimax   (reasoning ON via enable_thinking)
#   NOTE: Sonnet 4.6 is the DEVELOPMENT subagent (native `Agent`, model:"sonnet") — NOT a research advisor.
#
#   ⚠ TOOL DISCIPLINE (honest — do NOT assume "pure Q&A" for every lane):
#     • deepseek/mimo/kimi/glm/qwen/minimax (gateway) = STRUCTURALLY tool-free (no tools passed). The only
#       guaranteed pure-Q&A lanes.
#     • gpt5 (codex) = web_search DISABLED, but codex RETAINS shell/MCP tools it *could* invoke; for a plain
#       question it answers directly, but it is NOT sandbox-guaranteed tool-free.
#     • gemini + opus46 (agy) = TOOL-CAPABLE / AGENTIC: --dangerously-skip-permissions AUTO-APPROVES any tool
#       the model invokes. The "answer from your own knowledge, no tools" PROMPT line (router) is a SOFT
#       request only, not an enforced guarantee.
#
# Contract: prints the answer to stdout; EMPTY stdout = dead advisor (caller filters/degrades gracefully).
# Diagnostics go to stderr. Env knobs: MOA_MAXTOK (default 800), MOA_TIMEOUT seconds (default 180).
set -uo pipefail
ENV_FILE="/home/lingxufeng/huggingface/.env"
gv(){ grep -m1 "^$1=" "$ENV_FILE" | cut -d= -f2- | sed -E "s/^[\"']//;s/[\"']\$//" | tr -d '\r'; }

LANE="${1:?usage: moa_ask.sh <lane> <prompt-file>}"
PF="${2:?usage: moa_ask.sh <lane> <prompt-file>}"
PROMPT="$(cat "$PF")"
MAXTOK="${MOA_MAXTOK:-16384}"  # HIGH cap: reasoning lanes (deepseek + mimo) need headroom to finish thinking,
TMO="${MOA_TIMEOUT:-240}"      # else content returns empty. Billed = ACTUAL tokens used. Answer brevity = the PROMPT.

# --- OpenCode gateway (OpenAI-compatible chat/completions) ---
gw(){
  local model="$1" url key payload
  url="$(gv OpenCode-URL)"; key="$(gv OpenCode-APIKEY1)"
  # enable_thinking:true turns on reasoning for MiMo (DeepSeek reasons by default; harmless where unsupported).
  payload="$(jq -n --arg m "$model" --arg c "$PROMPT" --argjson mt "$MAXTOK" \
    '{model:$m,messages:[{role:"user",content:$c}],max_tokens:$mt,temperature:0.7,enable_thinking:true}')"
  curl -s -m "$TMO" "$url" -H "Authorization: Bearer $key" -H "Content-Type: application/json" -d "$payload" \
    | jq -r 'if .error then "[ERR] "+((.error.message)//"?") elif ((.choices[0].message.content//"")|length)>0 then .choices[0].message.content else "" end'
}

case "$LANE" in
  gemini)   ( source ~/.bashrc 2>/dev/null; timeout "$TMO" /home/lingxufeng/.local/bin/agy --dangerously-skip-permissions --model gemini-3.1-pro -p "$PROMPT" 2>/dev/null ) ;;
  opus46)   ( source ~/.bashrc 2>/dev/null; timeout "$TMO" /home/lingxufeng/.local/bin/agy --dangerously-skip-permissions --model opus-4.6 -p "$PROMPT" 2>/dev/null ) ;;
  gpt5)     tmp="$(mktemp)"; timeout "$TMO" codex exec --disable web_search --output-last-message "$tmp" "$PROMPT" >/dev/null 2>&1; cat "$tmp" 2>/dev/null; rm -f "$tmp" ;;
  deepseek) gw deepseek-v4-pro ;;
  mimo)     gw mimo-v2.5-pro ;;
  kimi)     gw kimi-k2.6 ;;
  glm)      gw glm-5.2 ;;
  qwen)     gw qwen3.7-max ;;
  minimax)  gw minimax-m3 ;;
  *) echo "[moa_ask] unknown lane: $LANE" >&2; exit 2 ;;
esac
