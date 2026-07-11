#!/usr/bin/env bash
# Guard (autonomous PASS/BLOCK) — block /adversary unless a prior /exp-verify VERIFIED
# artifact exists for the node. Fires before /adversary, before any region-close,
# and before a backup/substrate promotion.
#
# Usage:  no_adversary_without_expverify.sh <campaign> <node_id>
#   exit 0 = PASS  (an /exp-verify VERIFIED artifact exists -> /adversary may proceed)
#   exit 1 = BLOCK (no VERIFIED artifact -> run /exp-verify first)
#   exit 2 = bad args (node_id contains '/')
#
# The /goal loop calls this before dispatching /adversary. No human interaction.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

campaign="${1:?usage: $0 <campaign> <node_id>}"
node_id="${2:?usage: $0 <campaign> <node_id>}"

case "$node_id" in
  */*) echo "ERROR: node-id must not contain '/': $node_id" >&2; exit 2 ;;
esac

marker="$REPO_ROOT/openbuild/$campaign/exp_verify/${node_id}.VERIFIED"

if [ -f "$marker" ]; then
  echo "PASS: /exp-verify VERIFIED artifact present for '$node_id' ($marker)"
  exit 0
fi

echo "BLOCK: no /exp-verify VERIFIED artifact for '$node_id'" >&2
echo "  expected: $marker" >&2
echo "  -> run /exp-verify first; it must write the VERIFIED marker after an anti-no-op pass." >&2
exit 1
