#!/usr/bin/env bash
# moa_jury.sh — cross-family selection jury: fan the card set out to 4 non-Claude juror lanes
# in parallel, collect FORCED-PICK tallies for the conductor (/prospect JURY-MODE gate).
#
# Usage:  moa_jury.sh <packet-dir>
#   packet-dir MUST contain:
#     cards.md    — the FULL annotated problem-card set (ids like CARD A / CARD B / …)
#     anchors.md  — taste anchors: GOOD + BAD exemplars calibrating the jury
#   optional:
#     context.md  — project inventory / extra constraints forwarded verbatim
#   output:
#     <packet-dir>/verdicts/<lane>.md   — one file per live juror
#     stdout footer: lane→stance table, per-lane LIVE/DEAD, families answered, FORCED-PICK tally
#
# Jury composition (Claude-family excluded — generator must not grade its own output):
#   OpenCode-Go lanes (thin `juror` agent): deepseek qwen mimo   ·   gemini lane (agy, no system prompt)
#   The VERDICT CONTRACT is the SINGLE SOURCE OF TRUTH (juror-contract.md) injected into EVERY lane's
#   brief — no copy baked into any agent prompt, so nothing drifts. (opus46 is Claude-family → excluded;
#   the OpenCode-MoA layer carries only the 3 Go models per the 2026-07-14 scope directive, so 4
#   non-Claude families is the ceiling here.)
#
# Stances map 1:1 to the four lanes: venue-reviewer · replication-skeptic · builder-of-the-probe ·
#   adjacent-field-outsider
#
# Env knobs: MOA_TIMEOUT (default 300 for jurors; reasoning models need headroom)
set -uo pipefail
usage(){ sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//' >&2; }
case "${1:-}" in -h|--help) usage; exit 0;; "") usage; exit 2;; esac

PDIR="${1}"
case "$PDIR" in -*) echo "[moa_jury] packet-dir may not start with '-': $PDIR" >&2; exit 2;; esac
[ -d "$PDIR" ] || { echo "[moa_jury] packet-dir not found: $PDIR" >&2; exit 2; }
[ -f "$PDIR/cards.md" ]   || { echo "[moa_jury] missing cards.md in $PDIR" >&2; exit 2; }
[ -f "$PDIR/anchors.md" ] || { echo "[moa_jury] missing anchors.md in $PDIR" >&2; exit 2; }
DIR="$(cd "$(dirname "$0")" && pwd)"

# ---- juror contract: SINGLE SOURCE OF TRUTH ----
# The verdict contract lives in ONE file (juror-contract.md) and is injected VERBATIM into EVERY
# lane's brief — the thin juror.md agent prompt delegates to it, so there is no second copy to drift.
# We inject only the body below the `---CONTRACT---` marker (the header above it is documentation).
CONTRACT_FILE="${MOA_JUROR_CONTRACT:-$HOME/cli/opencode-moa/advisors/juror-contract.md}"
[ -f "$CONTRACT_FILE" ] || { echo "[moa_jury] juror-contract.md not found: $CONTRACT_FILE" >&2; exit 2; }
JUROR_CONTRACT="$(awk 'f{print} /^---CONTRACT---[[:space:]]*$/{f=1}' "$CONTRACT_FILE")"
[ -n "$JUROR_CONTRACT" ] || { echo "[moa_jury] no contract body in $CONTRACT_FILE (missing ---CONTRACT--- marker?)" >&2; exit 2; }

CARDS="$(cat "$PDIR/cards.md")"
ANCHORS="$(cat "$PDIR/anchors.md")"
CONTEXT_BLOCK=""
if [ -f "$PDIR/context.md" ]; then
  CONTEXT_BLOCK="$(printf '=== CONTEXT ===\n%s' "$(cat "$PDIR/context.md")")"
fi

# Jury lanes (4, no Claude-family): 3 OpenCode-Go advisors + gemini(agy)
LANES=(deepseek qwen mimo gemini)
# Stances: one per lane (1:1)
STANCES=(venue-reviewer replication-skeptic builder-of-the-probe adjacent-field-outsider)

TMO="${MOA_TIMEOUT:-300}"
VDIR="$PDIR/verdicts"
mkdir -p "$VDIR"
# clear stale verdicts from any prior run on this packet
rm -f "$VDIR"/*.md

# ---- derive card-id vocabulary from cards.md ----
# Accept ids of the form: CARD <token>  (single uppercase letter, digit, or short word)
# We extract them from lines like "## CARD A" or "**CARD A**" or bare "CARD A"
mapfile -t CARD_IDS < <(
  grep -oiE 'CARD [A-Z0-9]+' "$PDIR/cards.md" \
    | awk '{print toupper($2)}' \
    | sort -u
)

# ---- prompt construction ----
# The contract is injected into EVERY lane's brief (single source of truth) — the OpenCode juror
# agent and the gemini/agy lane (which has no system prompt at all) receive the identical contract.
build_prompt(){
  local stance="$1"
  printf '=== VERDICT CONTRACT (authoritative — grade EXACTLY per this) ===\n%s\n\n' "$JUROR_CONTRACT"
  printf 'STANCE: %s\n' "$stance"
  printf 'You are one juror on a cross-family selection jury. Grade the cards per the VERDICT CONTRACT above.\n'
  printf '=== TASTE ANCHORS ===\n%s\n' "$ANCHORS"
  if [ -n "$CONTEXT_BLOCK" ]; then
    printf '%s\n' "$CONTEXT_BLOCK"
  fi
  printf '=== CARDS ===\n%s\n' "$CARDS"
}

# ---- announce stance assignments ----
echo "=== moa_jury: lane→stance assignments ==="
for i in "${!LANES[@]}"; do
  echo "  ${LANES[$i]}  →  ${STANCES[$i]}"
done
echo "Firing ${#LANES[@]} juror lanes in parallel (MOA_TIMEOUT=${TMO}s) ..."
echo

# ---- fan out in parallel ----
TMPDIR_JURY="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_JURY"' EXIT

for i in "${!LANES[@]}"; do
  lane="${LANES[$i]}"
  stance="${STANCES[$i]}"
  pf="$TMPDIR_JURY/${lane}.txt"
  build_prompt "$stance" > "$pf"
  (
    export MOA_TIMEOUT="$TMO"
    export MOA_OC_AGENT=juror
    out="$("$DIR/moa_ask.sh" "$lane" "$pf" 2>/dev/null)"
    # trim whitespace before non-empty test
    trimmed="${out#"${out%%[![:space:]]*}"}"
    trimmed="${trimmed%"${trimmed##*[![:space:]]}"}"
    if [ -n "$trimmed" ]; then
      printf '%s\n' "$out" > "$VDIR/${lane}.md"
    fi
  ) &
done
wait

# ---- footer: LIVE/DEAD + tally ----
echo "=== moa_jury: per-lane results ==="
LIVE_COUNT=0
LIVE_LANES=()
for lane in "${LANES[@]}"; do
  vf="$VDIR/${lane}.md"
  if [ -s "$vf" ]; then
    echo "  $lane  LIVE  → $vf"
    LIVE_COUNT=$((LIVE_COUNT+1))
    LIVE_LANES+=("$lane")
  else
    echo "  $lane  DEAD  (empty or no output)"
    rm -f "$vf"
  fi
done
echo
echo "families answered: ${LIVE_COUNT}/${#LANES[@]}"

# Quorum = 3 of the 4 non-Claude families (was 4-of-5 before the kimi scope removal; 4-of-4 would be
# all-or-nothing and gemini/agy is the flakiest lane, so a single dead lane must not void the jury).
QUORUM_MIN="${MOA_JURY_QUORUM:-3}"
if [ "$LIVE_COUNT" -lt "$QUORUM_MIN" ]; then
  echo >&2
  echo "⚠ QUORUM FAIL: only ${LIVE_COUNT} famil(ies) answered — need ≥${QUORUM_MIN}." >&2
  echo "  Verdicts that did arrive are on disk in $VDIR." >&2
  echo "  Re-run the jury when lanes recover (moa_ping.sh to triage)." >&2
  exit 3
fi

# ---- FORCED-PICK tally ----
# PICK-REGION parse: strip the post-colon text; split on ';'; scan only pick regions.
# Segment 0: scan pre-dash part (dash = — – or " - "); no dash means scan full segment 0.
# Later segments: skip if they contain no dash (reason-text continuation); else scan pre-dash part.
# Residual bias: a dash-less first segment means the full first segment is scanned (juror
# wrote no rationale separator), but later segments are still gated — this is the tightest
# parse achievable without requiring strict format compliance.
echo
echo "=== FORCED-PICK tally (conductor synthesises; script only counts) ==="
declare -A TALLY=()

for lane in "${LIVE_LANES[@]}"; do
  vf="$VDIR/${lane}.md"
  # per-file deduplication: build a set of picked ids for THIS verdict
  declare -A FILE_PICKS=()
  while IFS= read -r line; do
    # strip everything up to and including the first colon. Match in ORIGINAL CASE (card ids are
    # uppercase by contract) so the article "a" / any lowercase prose word cannot collide with id
    # "A" — matching the uppercased region conflated "a"↔"A" and miscounted dash-less pick regions.
    rest="${line#*:}"

    # split on ';' into segments
    IFS=';' read -ra segs <<< "$rest"

    for i in "${!segs[@]}"; do
      seg="${segs[$i]}"
      # locate first dash of any flavor and take pre-dash as the pick region
      region="$seg"
      region="${region%%—*}"; region="${region%%–*}"; region="${region%% - *}"
      # later segments with no dash are reason continuations — skip them
      if [ "$i" -gt 0 ] && [ "$region" = "$seg" ]; then
        continue
      fi
      # vocabulary-match card ids in the pick region, CASE-SENSITIVELY and only at id-list/CARD-prefix
      # boundaries (comma/space/slash/&/"CARD ") — so a lowercase word never matches an uppercase id,
      # and a real "A, B" id list still counts. Residual (rare): a prose sentence starting with an
      # uppercase id letter, or pronoun "I" when a card "I" exists — accepted as triage-grade.
      for cid in "${CARD_IDS[@]}"; do
        if printf '%s' "$region" | grep -qE "(^|[[:space:],;/&]|CARD )${cid}([[:space:],.;/&]|\$)"; then
          FILE_PICKS["$cid"]=1
        fi
      done
    done
  done < <(grep -i '^FORCED-PICK:' "$vf" 2>/dev/null)

  # merge this verdict's deduped set into the global tally
  for cid in "${!FILE_PICKS[@]}"; do
    TALLY["$cid"]=$(( ${TALLY["$cid"]:-0} + 1 ))
  done
  unset FILE_PICKS
done

if [ ${#TALLY[@]} -eq 0 ]; then
  echo "  (no FORCED-PICK lines parsed from live verdicts)"
else
  # sort descending by count
  for card in "${!TALLY[@]}"; do
    printf '%d %s\n' "${TALLY[$card]}" "$card"
  done | sort -rn | while read -r cnt id; do
    printf '  CARD %-8s  %d vote(s)\n' "$id" "$cnt"
  done
fi
echo
echo "=== END moa_jury (${LIVE_COUNT}/${#LANES[@]} families live; verdicts → $VDIR) ==="
