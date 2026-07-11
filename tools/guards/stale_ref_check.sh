#!/usr/bin/env bash
# stale_ref_check.sh — doc-drift tripwire (audit finding 8).
# Greps the LIVE doc set for stale terms that have been retired.
# exit 0 = PASS (zero hits); exit 1 = FAIL (lists file:line:term for every hit).
#
# Env overrides for testing:
#   LIVE_DOCS  — space- or newline-separated list of doc paths (default: the canonical set)
#   TERMS_FILE — path to the terms file (default: tools/guards/stale_terms.txt)
#
# Historical dirs (plan/Audit, plan/archive) are deliberately NOT scanned.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TERMS_FILE="${TERMS_FILE:-$REPO_ROOT/tools/guards/stale_terms.txt}"

# Canonical live doc set (missing files are skipped with a note)
DEFAULT_LIVE_DOCS="
$REPO_ROOT/.claude/CLAUDE.md
$REPO_ROOT/plan/goal-directive.md
$REPO_ROOT/plan/README.md
$REPO_ROOT/plan/operating-manual.md
$REPO_ROOT/plan/optical-sar-research-plan.md
$REPO_ROOT/moa/router-protocol.md
"

# Allow override (split on newlines and spaces)
if [ -n "${LIVE_DOCS:-}" ]; then
  doc_list="$LIVE_DOCS"
else
  doc_list="$DEFAULT_LIVE_DOCS"
fi

hits=0

while IFS= read -r term; do
  # Skip blank lines and comments
  [[ "$term" =~ ^[[:space:]]*$ ]] && continue
  [[ "$term" =~ ^# ]] && continue

  for doc in $doc_list; do
    [ -z "$doc" ] && continue
    if [ ! -f "$doc" ]; then
      echo "NOTE: skipping missing doc: $doc" >&2
      continue
    fi
    # grep -n: line numbers; -F: fixed string (handles special chars); suppress no-match
    while IFS= read -r match; do
      lineno="${match%%:*}"
      echo "STALE: ${doc}:${lineno}:${term}"
      hits=$((hits + 1))
    done < <(grep -nF "$term" "$doc" 2>/dev/null | sed 's/:.*$//' || true)
  done
done < "$TERMS_FILE"

if [ "$hits" -eq 0 ]; then
  echo "PASS: no stale terms found in live doc set"
  exit 0
fi

echo "FAIL: $hits stale reference(s) found — update the live docs before proceeding"
exit 1
