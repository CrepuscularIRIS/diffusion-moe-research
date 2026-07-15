#!/usr/bin/env bash
# moa_panel.sh — fan a question out to the research advisor panel IN PARALLEL, then print a labeled
# collection for the JUDGE (the main loop) to reconcile via the dispute-map template
# (protocol: research-os skills/conductor/references/moa-routing.md; bindings: moa/router-protocol.md).
#
# TWO MODES:
#   SHARED    :  moa_panel.sh <prompt-file> [lane ...]     same prompt to every named lane (quick use)
#                explicit lane lists carry NO pre-dispatch quorum (a deliberate 2-lane cross-check is
#                the conductor's call) — but the post-run family count still warns if < MOA_MIN_LANES.
#   PER-LANE  :  moa_panel.sh --per-lane <prompt-dir>      one prompt PER INSTANCE, differentiated
#                files: <lane>.txt or <lane>-<k>.txt  (e.g. gemini-1.txt … gemini-5.txt, opus46-2.txt)
#                → the DIFFERENTIATED-PRIORS path: the router writes a DISTINCT prompt per instance
#                  {operator × lens × dropout × stance}; two instances with the same prompt = waste.
#
# PANEL FAMILIES (5) = opus46 · gemini · deepseek · mimo · qwen        (the judge is NOT a lane)
#   gpt5 (codex) is NOT a panel lane (rebound 2026-07-13): it is the FORENSIC lane for /autopsy +
#   /abduce consults (subtle hidden errors) — fire it via moa_ask.sh gpt5, never inside a panel.
# Default differentiated allocation (router may adjust): opus46×3 · gemini×5 · deepseek×3 · mimo×3 · qwen×3.
# Quorum = ≥MOA_MIN_LANES DISTINCT FAMILIES live (default 4) — instances add depth within a family's
# priors; only families add independence. Within-family convergence is discounted at reconcile.
# Graceful degradation: an instance that errors/times-out prints "[no response]" and never blocks others.
set -uo pipefail
usage(){ sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//' >&2; }
case "${1:-}" in -h|--help) usage; exit 0;; "") usage; exit 2;; esac
DIR="$(cd "$(dirname "$0")" && pwd)"
MIN_LANES="${MOA_MIN_LANES:-4}"   # quorum = distinct live FAMILIES (router-protocol); override deliberately
declare -A PROMPT_OF LANE_OF
is_panel_lane(){ case "$1" in gemini|opus46|mimo|deepseek|qwen) return 0;; *) return 1;; esac; }

if [ "${1:-}" = "--per-lane" ]; then
  PDIR="${2:?usage: moa_panel.sh --per-lane <prompt-dir>}"; MODE="DIFFERENTIATED (per-instance)"
  INSTANCES=(); SKIPPED=0
  for f in "$PDIR"/*.txt; do
    [ -e "$f" ] || continue
    inst="$(basename "$f" .txt)"
    case "$inst" in _*) continue;; esac
    lane="${inst%-[0-9]*}"                      # gemini-3 → gemini; opus46 → opus46
    if [ "$lane" = "gpt5" ]; then
      echo "[moa_panel] gpt5 is the FORENSIC lane (/autopsy + /abduce), not a panel lane — skipping $f (use moa_ask.sh gpt5)" >&2
      SKIPPED=$((SKIPPED+1)); continue
    fi
    if ! is_panel_lane "$lane"; then
      echo "[moa_panel] skip non-lane prompt file: $f" >&2; SKIPPED=$((SKIPPED+1))
      continue
    fi
    [ -s "$f" ] || { echo "[moa_panel] empty prompt file: $f" >&2; exit 2; }
    INSTANCES+=("$inst"); PROMPT_OF[$inst]="$f"; LANE_OF[$inst]="$lane"
  done
  [ ${#INSTANCES[@]} -eq 0 ] && { echo "no <lane>[-k].txt files in $PDIR" >&2; exit 2; }
  declare -A FAM_SEEN=()
  for inst in "${INSTANCES[@]}"; do FAM_SEEN[${LANE_OF[$inst]}]=1; done
  NFAM=${#FAM_SEEN[@]}
  if [ "$NFAM" -lt "$MIN_LANES" ]; then
    echo "[moa_panel] QUORUM FAIL: $NFAM distinct famil(ies) < MOA_MIN_LANES=$MIN_LANES (${#INSTANCES[@]} instances, skipped=$SKIPPED)." >&2
    echo "[moa_panel] Instances within one family share priors — they add depth, not independence. Use" >&2
    echo "[moa_panel] conductor + strongest-external + reviewer lane, or set MOA_MIN_LANES deliberately." >&2
    exit 3
  fi
else
  PF="${1:?usage: moa_panel.sh <prompt-file> [lanes...]  |  --per-lane <dir>}"; shift || true; MODE="shared"
  case "$PF" in -*) echo "[moa_panel] unknown flag or dash-prefixed prompt path: $PF" >&2; usage; exit 2;; esac
  [ -s "$PF" ] || { echo "[moa_panel] prompt file missing or empty: $PF" >&2; exit 2; }
  INSTANCES=("$@"); [ ${#INSTANCES[@]} -eq 0 ] && INSTANCES=(gemini opus46 mimo deepseek qwen)
  for inst in "${INSTANCES[@]}"; do
    if [ "$inst" = "gpt5" ]; then
      echo "[moa_panel] gpt5 is the FORENSIC lane (/autopsy + /abduce), not a panel lane — use moa_ask.sh gpt5" >&2; exit 2
    fi
    is_panel_lane "$inst" || { echo "[moa_panel] unknown lane: $inst" >&2; exit 2; }
    PROMPT_OF[$inst]="$PF"; LANE_OF[$inst]="$inst"
  done
fi

OUT="$(mktemp -d)"
for inst in "${INSTANCES[@]}"; do
  ( "$DIR/moa_ask.sh" "${LANE_OF[$inst]}" "${PROMPT_OF[$inst]}" > "$OUT/$inst.txt" 2>/dev/null ) &
done
wait

echo "===== MoA PANEL — ${#INSTANCES[@]} advisor instance(s) · mode: ${MODE} ====="
echo
declare -A FAM_LIVE=()
for inst in "${INSTANCES[@]}"; do
  ans="$(cat "$OUT/$inst.txt" 2>/dev/null)"
  echo "### advisor: $inst"
  if [ -n "$ans" ]; then echo "$ans"; FAM_LIVE[${LANE_OF[$inst]}]=1; else echo "[no response — advisor degraded/timed out]"; fi
  echo
done
NLIVE=${#FAM_LIVE[@]}
echo "===== END PANEL — ${NLIVE} famil(ies) actually ANSWERED — the judge reconciles: consensus / conflict / unique-insight / blind-spot (discount within-family convergence) ====="
if [ "$NLIVE" -lt "$MIN_LANES" ]; then
  echo "[moa_panel] ⚠ POST-RUN QUORUM WARNING: only $NLIVE live famil(ies) < $MIN_LANES — treat this round as a DEGRADED cross-check, not a panel; convergence here is weak evidence (run moa_ping.sh, fix lanes, or re-fire)." | tee /dev/stderr
fi
rm -rf "$OUT"
