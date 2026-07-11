#!/usr/bin/env bash
# claim_preflight.sh — substrate preflight gate (audit finding 5+6, axes A1/A3/A4/A7).
# Usage: claim_preflight.sh <campaign> <substrate>
#   exit 0 = PASS  (venue_taste.md + preflight/<substrate>.md both exist, all 6 fields present)
#   exit 1 = BLOCK (missing file or missing field; lists what is missing)
#
# OPENBUILD_ROOT override allows test fixtures (defaults to <repo>/openbuild).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OPENBUILD_ROOT="${OPENBUILD_ROOT:-$REPO_ROOT/openbuild}"

campaign="${1:?usage: $0 <campaign> <substrate>}"
substrate="${2:?usage: $0 <campaign> <substrate>}"

VENUE_TASTE="$OPENBUILD_ROOT/$campaign/atlas/venue_taste.md"
PREFLIGHT="$OPENBUILD_ROOT/$campaign/preflight/$substrate.md"

blocked=0

if [ ! -f "$VENUE_TASTE" ]; then
  echo "BLOCK: missing venue_taste.md: $VENUE_TASTE" >&2
  blocked=1
fi

if [ ! -f "$PREFLIGHT" ]; then
  echo "BLOCK: missing preflight file: $PREFLIGHT" >&2
  blocked=1
fi

[ "$blocked" -eq 1 ] && exit 1

# Check all required fields (allow leading "- " before FIELD:)
REQUIRED_FIELDS="FIT-VERDICT METRIC-PROTOCOL OCCUPANCY RECONSTRUCTION RAW-FAILURES-READ TYPICAL-PUBLISHED-DELTA"
missing_fields=""
found_lines=""

for field in $REQUIRED_FIELDS; do
  line=$(grep -m1 -E "^(- )?${field}:" "$PREFLIGHT" 2>/dev/null || true)
  if [ -z "$line" ]; then
    missing_fields="$missing_fields $field"
  else
    found_lines="$found_lines\n$line"
  fi
done

if [ -n "$missing_fields" ]; then
  echo "BLOCK: preflight file missing required fields:$missing_fields" >&2
  for f in $missing_fields; do echo "  missing: $f:" >&2; done
  exit 1
fi

echo "PASS: preflight complete for campaign='$campaign' substrate='$substrate'"
printf "%b\n" "$found_lines" | grep -v '^$'
exit 0
