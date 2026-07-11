#!/usr/bin/env bash
# exp_verify_mark.sh — mechanical write-through for /exp-verify.
# Usage: exp_verify_mark.sh <campaign> <node_id> <verdict> [evidence ...]
#   verdict ∈ {VERIFIED, FAILED-STRUCTURAL, FAILED-EXECUTION, FAILED-NOOP, FAILED-PLAUSIBILITY}
#   exit 0 = marker written; exit 2 = bad args (invalid verdict or node_id with /)
#
# Writes openbuild/<campaign>/exp_verify/<node_id>.<verdict>
# A new VERIFIED marker removes stale FAILED-* markers for the same node, and vice versa.
# Idempotent: re-running overwrites. Prints the marker path.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

campaign="${1:?usage: $0 <campaign> <node_id> <verdict> [evidence ...]}"
node_id="${2:?usage: $0 <campaign> <node_id> <verdict> [evidence ...]}"
verdict="${3:?usage: $0 <campaign> <node_id> <verdict> [evidence ...]}"
shift 3

# Validate node_id
case "$node_id" in
  */*) echo "ERROR: node_id must not contain '/': $node_id" >&2; exit 2 ;;
esac

# Validate verdict
case "$verdict" in
  VERIFIED|FAILED-STRUCTURAL|FAILED-EXECUTION|FAILED-NOOP|FAILED-PLAUSIBILITY) ;;
  *) echo "ERROR: invalid verdict '$verdict'; must be one of VERIFIED FAILED-STRUCTURAL FAILED-EXECUTION FAILED-NOOP FAILED-PLAUSIBILITY" >&2; exit 2 ;;
esac

VERIFY_DIR="$REPO_ROOT/openbuild/$campaign/exp_verify"
mkdir -p "$VERIFY_DIR"
MARKER="$VERIFY_DIR/${node_id}.${verdict}"

# Remove stale opposing markers
if [ "$verdict" = "VERIFIED" ]; then
  rm -f "$VERIFY_DIR/${node_id}.FAILED-STRUCTURAL" \
        "$VERIFY_DIR/${node_id}.FAILED-EXECUTION" \
        "$VERIFY_DIR/${node_id}.FAILED-NOOP" \
        "$VERIFY_DIR/${node_id}.FAILED-PLAUSIBILITY"
else
  rm -f "$VERIFY_DIR/${node_id}.VERIFIED"
fi

# Write marker
{
  printf "timestamp: %s\n" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf "verdict: %s\n" "$verdict"
  for ev in "$@"; do
    printf "evidence: %s\n" "$ev"
  done
} > "$MARKER"

echo "$MARKER"
