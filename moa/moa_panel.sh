#!/usr/bin/env bash
# moa_panel.sh — fan a question out to the research advisor panel IN PARALLEL, then print a labeled
# collection for the JUDGE (Opus 4.8, the main loop) to reconcile via the dispute-map template
# (plan/moa-advisor-panel-design-2026-07-04.md §4). Wall-clock = slowest advisor, not the sum.
#
# TWO MODES:
#   SHARED    :  moa_panel.sh <prompt-file> [lane ...]        same prompt to every lane (quick use)
#   PER-LANE  :  moa_panel.sh --per-lane <prompt-dir>         <prompt-dir>/<lane>.txt, one prompt PER lane
#                → the DIFFERENTIATED-PRIORS path: the router (Opus) writes a distinct prompt per advisor
#                  {rotated operator + frame + school + structured dropout}. Lanes = the .txt files present.
#
# Default panel = gemini gpt5 deepseek mimo opus46   (Opus 4.8 = judge, NOT a lane; Sonnet 4.6 = dev, NOT a lane)
# Graceful degradation: an advisor that errors/times-out prints "[no response]" and never blocks the others.
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
declare -A PROMPT_OF

if [ "${1:-}" = "--per-lane" ]; then
  PDIR="${2:?usage: moa_panel.sh --per-lane <prompt-dir>}"; MODE="DIFFERENTIATED (per-lane)"
  LANES=()
  for f in "$PDIR"/*.txt; do [ -e "$f" ] || continue; l="$(basename "$f" .txt)"; LANES+=("$l"); PROMPT_OF[$l]="$f"; done
  [ ${#LANES[@]} -eq 0 ] && { echo "no <lane>.txt files in $PDIR" >&2; exit 2; }
else
  PF="${1:?usage: moa_panel.sh <prompt-file> [lanes...]  |  --per-lane <dir>}"; shift || true; MODE="shared"
  LANES=("$@"); [ ${#LANES[@]} -eq 0 ] && LANES=(gemini gpt5 deepseek mimo opus46)
  for l in "${LANES[@]}"; do PROMPT_OF[$l]="$PF"; done
fi

OUT="$(mktemp -d)"
for lane in "${LANES[@]}"; do
  ( "$DIR/moa_ask.sh" "$lane" "${PROMPT_OF[$lane]}" > "$OUT/$lane.txt" 2>/dev/null ) &
done
wait

echo "===== MoA PANEL — ${#LANES[@]} advisors · mode: ${MODE} ====="
echo
for lane in "${LANES[@]}"; do
  ans="$(cat "$OUT/$lane.txt" 2>/dev/null)"
  echo "### advisor: $lane"
  [ -n "$ans" ] && echo "$ans" || echo "[no response — advisor degraded/timed out]"
  echo
done
echo "===== END PANEL — Opus 4.8 reconciles: consensus / conflict / unique-insight / blind-spot ====="
rm -rf "$OUT"
