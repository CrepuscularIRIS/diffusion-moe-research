#!/usr/bin/env bash
# moa_ping.sh — mechanized lane-liveness precheck (the routing skill's "≥4 live FAMILIES" rule,
# enforced by measurement instead of memory). Fires a 1-word probe at every lane IN PARALLEL and
# prints a liveness table. Run BEFORE any full differentiated panel; also pings the forensic lane.
#
#   exit 0 = panel quorum met (≥MOA_MIN_LANES live panel families, default 4)
#   exit 3 = quorum FAIL — do not fire a full panel; use conductor + strongest-external + reviewer
#
# Why this exists (2026-07-13 audit): panels silently degraded to 2/6 live lanes for days (agy model-id
# rot, OpenCode quota) — panel latency paid for near-zero diversity. Liveness is checked, not assumed.
# Panel = 5 families: gemini (agy) · opus46 (claude -p) · mimo/deepseek/qwen (OpenCode-Go advisors).
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
MIN="${MOA_MIN_LANES:-4}"
PANEL=(gemini opus46 mimo deepseek qwen)
PF="$(mktemp)"; trap 'rm -f "$PF"' EXIT
echo "Reply with exactly one word: ALIVE" > "$PF"
OUT="$(mktemp -d)"; trap 'rm -rf "$OUT" "$PF"' EXIT
for lane in "${PANEL[@]}" gpt5; do
  ( MOA_MAXTOK="${MOA_MAXTOK:-64}" MOA_TIMEOUT="${MOA_TIMEOUT:-90}" \
    "$DIR/moa_ask.sh" "$lane" "$PF" > "$OUT/$lane" 2>/dev/null ) &
done
wait
LIVE=0
echo "lane      role      status"
for lane in "${PANEL[@]}"; do
  if [ -s "$OUT/$lane" ]; then s=LIVE; LIVE=$((LIVE+1)); else s=DEAD; fi
  printf '%-9s panel     %s\n' "$lane" "$s"
done
[ -s "$OUT/gpt5" ] && g=LIVE || g=DEAD
printf '%-9s forensic  %s\n' "gpt5" "$g"
echo "panel families live: $LIVE/${#PANEL[@]} (quorum $MIN)"
if [ "$LIVE" -lt "$MIN" ]; then
  echo "[moa_ping] QUORUM FAIL — do NOT fire a full panel; substitute conductor + strongest-external + reviewer lane, and fix the dead lanes (agy model id? OpenCode quota? codex trust flags?)." >&2
  exit 3
fi
