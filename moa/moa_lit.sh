#!/usr/bin/env bash
# moa_lit.sh — literature-intelligence lane: fires the `librarian` operator agent
# (~/cli/opencode-moa/operators, scoped tools: bash+webfetch only) on a research question and
# prints its 5-line summary; the real product is <outdir>/lit-cards.md (extraction cards +
# SYNTHESIS + COVERAGE). Supersedes ~/cli/paperseek/moa_search.sh as the bound literature lane.
#
# Usage:  moa_lit.sh "<research question>" [--out <dir>] [--deep] [--resume <dir> <scholar-results-file>]
#   --out <dir>    output dir (default: fresh mktemp -d, printed to stderr)
#   --deep         allow the agent to deep-read up to 8 PDFs (default 5)
#   --resume ...   Scholar handoff, leg 2 (see contract below)
#
# SCHOLAR-HANDOFF CONTRACT (3 lines):
#   If the API lanes were insufficient, lit-cards.md ends with a SCHOLAR-QUERIES: marker line
#   followed by the query list.  The conductor runs those queries in the logged-in Scholar browser
#   tab, saves findings to a file, then re-invokes:
#   moa_lit.sh "<same question>" --resume <same outdir> <results-file>
#   → the agent merges them into the existing cards and removes the marker block.
#
# Env knobs: MOA_TIMEOUT seconds (default 900) · MOA_OC_OPDIR operators dir override.
# Contract: agent summary → stdout; diagnostics → stderr; exit 1 if lit-cards.md was not produced.
set -uo pipefail
usage(){ sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//' >&2; }
case "${1:-}" in -h|--help|"") usage; exit 2;; esac

Q="$1"; shift
OUTDIR="" DEEP=0 RESUME_DIR="" RESUME_FILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --out)    OUTDIR="${2:?--out needs a dir}"; shift 2;;
    --deep)   DEEP=1; shift;;
    --resume) RESUME_DIR="${2:?--resume needs <dir> <file>}"; RESUME_FILE="${3:?--resume needs <dir> <file>}"; shift 3;;
    *) echo "[moa_lit] unknown arg: $1" >&2; usage; exit 2;;
  esac
done

OC_OPDIR="${MOA_OC_OPDIR:-$HOME/cli/opencode-moa/operators}"
TMO="${MOA_TIMEOUT:-900}"

if [ -n "$RESUME_DIR" ]; then
  OUTDIR="$RESUME_DIR"
  [ -d "$OUTDIR" ] || { echo "[moa_lit] resume dir not found: $OUTDIR" >&2; exit 2; }
  [ -f "$RESUME_FILE" ] || { echo "[moa_lit] scholar-results file not found: $RESUME_FILE" >&2; exit 2; }
  # Capture lit-cards.md checksum before the merge agent runs so we can
  # detect a no-op (agent failed silently and the file was not updated).
  _CARDS_PRE=""
  if [ -f "$OUTDIR/lit-cards.md" ]; then
    _CARDS_PRE="$(sha256sum "$OUTDIR/lit-cards.md" | awk '{print $1}')"
  fi
elif [ -n "$OUTDIR" ]; then
  mkdir -p "$OUTDIR" || { echo "[moa_lit] cannot create outdir: $OUTDIR" >&2; exit 2; }
else
  # /tmp/opencode/* is the operator runtime's allowed external-directory pattern — stay inside it.
  mkdir -p /tmp/opencode && OUTDIR="$(mktemp -d /tmp/opencode/moa_lit.XXXXXX)" || exit 2
fi
echo "[moa_lit] outdir: $OUTDIR" >&2

MSG="RESEARCH QUESTION: $Q
OUTPUT DIR: $OUTDIR"
[ "$DEEP" = 1 ] && MSG="$MSG
FOCUS: deep — read up to 8 PDFs."
if [ -n "$RESUME_DIR" ]; then
  MSG="$MSG

SCHOLAR-RESULTS:
$(cat -- "$RESUME_FILE")"
fi

timeout "$TMO" opencode run --dir "$OC_OPDIR" --agent librarian --format json -- "$MSG" \
  | jq -r 'select(.type=="text") | .part.text // empty'
RC="${PIPESTATUS[0]}"   # timeout's exit, not jq's — under pipefail a jq failure would mask the 124
[ "$RC" -eq 124 ] && echo "[moa_lit] agent timed out after ${TMO}s" >&2

if [ ! -s "$OUTDIR/lit-cards.md" ]; then
  echo "[moa_lit] FAILED: $OUTDIR/lit-cards.md was not produced (agent rc=$RC)" >&2
  exit 1
fi
# On the --resume leg: fail if the agent did not actually update lit-cards.md.
if [ -n "${_CARDS_PRE:-}" ]; then
  _CARDS_POST="$(sha256sum "$OUTDIR/lit-cards.md" | awk '{print $1}')"
  if [ "$_CARDS_PRE" = "$_CARDS_POST" ]; then
    echo "[moa_lit] FAILED: --resume did not update lit-cards.md (checksum unchanged, agent rc=$RC)" >&2
    exit 1
  fi
fi
echo "[moa_lit] lit-cards: $OUTDIR/lit-cards.md" >&2
