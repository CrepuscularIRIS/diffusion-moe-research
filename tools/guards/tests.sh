#!/usr/bin/env bash
# Test harness for Task 1 guard + marker toolchain.
# Runs in a mktemp sandbox; all assertions use real tool invocations.
# Usage: bash tools/guards/tests.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOOLS="$REPO_ROOT/tools"
GUARDS="$REPO_ROOT/tools/guards"

PASS_COUNT=0
FAIL_COUNT=0

ok() {
  echo "  PASS: $1"
  PASS_COUNT=$((PASS_COUNT + 1))
}

fail() {
  echo "  FAIL: $1"
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

# ── Setup sandbox ────────────────────────────────────────────────────────────
SANDBOX=$(mktemp -d)
trap 'rm -rf "$SANDBOX" "$REPO_ROOT/openbuild/test_campaign"' EXIT

echo "=== Task 1 guard + marker tests (sandbox: $SANDBOX) ==="

# ── 1. exp_verify_mark.sh: basic marker write ────────────────────────────────
echo ""
echo "-- 1. exp_verify_mark.sh: marker write --"

out=$("$TOOLS/exp_verify_mark.sh" test_campaign node001 VERIFIED 2>&1) || true
marker_path="$REPO_ROOT/openbuild/test_campaign/exp_verify/node001.VERIFIED"
if [ -f "$marker_path" ]; then
  ok "1a: VERIFIED marker file created"
  if grep -q "verdict: VERIFIED" "$marker_path"; then ok "1b: marker contains verdict field"; else fail "1b: verdict field missing"; fi
  if grep -q "^timestamp:" "$marker_path"; then ok "1c: marker contains timestamp"; else fail "1c: timestamp missing"; fi
  if echo "$out" | grep -q "node001.VERIFIED"; then ok "1d: path printed to stdout"; else fail "1d: path not in stdout"; fi
else
  fail "1a: VERIFIED marker file not created (path: $marker_path)"
  fail "1b: skipped"
  fail "1c: skipped"
  fail "1d: skipped"
fi

# ── 2. VERIFIED clears FAILED markers ────────────────────────────────────────
echo ""
echo "-- 2. VERIFIED clears FAILED-* markers --"

"$TOOLS/exp_verify_mark.sh" test_campaign node002 FAILED-EXECUTION "run crashed" >/dev/null 2>&1
failed_path="$REPO_ROOT/openbuild/test_campaign/exp_verify/node002.FAILED-EXECUTION"
if [ -f "$failed_path" ]; then ok "2a: FAILED-EXECUTION marker created"; else fail "2a: FAILED-EXECUTION marker missing"; fi

"$TOOLS/exp_verify_mark.sh" test_campaign node002 VERIFIED "fixed" >/dev/null 2>&1
if [ ! -f "$failed_path" ]; then ok "2b: FAILED marker removed on VERIFIED write"; else fail "2b: stale FAILED marker not removed"; fi
if [ -f "$REPO_ROOT/openbuild/test_campaign/exp_verify/node002.VERIFIED" ]; then ok "2c: VERIFIED marker present after clearing FAILED"; else fail "2c: VERIFIED marker missing"; fi

# ── 3. FAILED clears VERIFIED marker ─────────────────────────────────────────
echo ""
echo "-- 3. FAILED clears VERIFIED marker --"

"$TOOLS/exp_verify_mark.sh" test_campaign node003 VERIFIED >/dev/null 2>&1
"$TOOLS/exp_verify_mark.sh" test_campaign node003 FAILED-STRUCTURAL >/dev/null 2>&1
if [ ! -f "$REPO_ROOT/openbuild/test_campaign/exp_verify/node003.VERIFIED" ]; then
  ok "3a: VERIFIED cleared by FAILED write"
else
  fail "3a: stale VERIFIED not cleared"
fi

# ── 4. Bad verdict rejected (exit 2) ─────────────────────────────────────────
echo ""
echo "-- 4. Bad verdict / bad node_id rejected --"

ec=0; "$TOOLS/exp_verify_mark.sh" test_campaign node004 BOGUS_VERDICT 2>/dev/null || ec=$?
if [ "$ec" -eq 2 ]; then ok "4a: bad verdict exits 2"; else fail "4a: expected exit 2, got $ec"; fi

ec=0; "$TOOLS/exp_verify_mark.sh" test_campaign "node/bad" VERIFIED 2>/dev/null || ec=$?
if [ "$ec" -eq 2 ]; then ok "4b: node_id with / exits 2"; else fail "4b: expected exit 2, got $ec"; fi

# ── 5. Evidence lines written ─────────────────────────────────────────────────
echo ""
echo "-- 5. Evidence lines --"

"$TOOLS/exp_verify_mark.sh" test_campaign node005 VERIFIED "ev1" "ev2 with spaces" >/dev/null 2>&1
ev_path="$REPO_ROOT/openbuild/test_campaign/exp_verify/node005.VERIFIED"
if grep -q "ev1" "$ev_path" && grep -q "ev2 with spaces" "$ev_path"; then
  ok "5a: multiple evidence args written to marker"
else
  fail "5a: evidence args not in marker"
fi

# ── 6. Adversary guard: BLOCK then PASS ──────────────────────────────────────
echo ""
echo "-- 6. no_adversary_without_expverify.sh: BLOCK then PASS --"

ec=0; "$GUARDS/no_adversary_without_expverify.sh" test_campaign node_adv_new 2>/dev/null || ec=$?
if [ "$ec" -eq 1 ]; then ok "6a: guard BLOCKs when no marker"; else fail "6a: expected BLOCK (exit 1), got $ec"; fi

"$TOOLS/exp_verify_mark.sh" test_campaign node_adv_new VERIFIED >/dev/null 2>&1
ec=0; "$GUARDS/no_adversary_without_expverify.sh" test_campaign node_adv_new 2>/dev/null || ec=$?
if [ "$ec" -eq 0 ]; then ok "6b: guard PASSes after marker written"; else fail "6b: expected PASS (exit 0), got $ec"; fi

# ── 7. Adversary guard: node_id with / rejected (exit 2) ─────────────────────
echo ""
echo "-- 7. Adversary guard: bad node_id --"

ec=0; "$GUARDS/no_adversary_without_expverify.sh" test_campaign "bad/node" 2>/dev/null || ec=$?
if [ "$ec" -eq 2 ]; then ok "7a: adversary guard exits 2 for / in node_id"; else fail "7a: expected exit 2, got $ec"; fi

# ── 8. claim_preflight.sh: missing preflight dir/file ────────────────────────
echo ""
echo "-- 8. claim_preflight.sh: BLOCK on missing files --"

FAKE_CAMPAIGN="$SANDBOX/camp"
mkdir -p "$FAKE_CAMPAIGN/atlas"
echo "dummy" > "$FAKE_CAMPAIGN/atlas/venue_taste.md"

# Missing preflight file
ec=0; OPENBUILD_ROOT="$SANDBOX" "$GUARDS/claim_preflight.sh" camp testsubstrate 2>/dev/null || ec=$?
if [ "$ec" -eq 1 ]; then ok "8a: BLOCKs when preflight file missing"; else fail "8a: expected BLOCK (exit 1), got $ec"; fi

# Missing venue_taste.md (and no preflight)
mkdir -p "$FAKE_CAMPAIGN/preflight"
rm "$FAKE_CAMPAIGN/atlas/venue_taste.md"
ec=0; OPENBUILD_ROOT="$SANDBOX" "$GUARDS/claim_preflight.sh" camp testsubstrate 2>/dev/null || ec=$?
if [ "$ec" -eq 1 ]; then ok "8b: BLOCKs when venue_taste.md missing"; else fail "8b: expected BLOCK (exit 1), got $ec"; fi

# ── 9. claim_preflight.sh: BLOCK naming missing fields ───────────────────────
echo ""
echo "-- 9. claim_preflight.sh: BLOCK listing missing fields --"

echo "dummy" > "$FAKE_CAMPAIGN/atlas/venue_taste.md"
cat > "$FAKE_CAMPAIGN/preflight/testsubstrate.md" <<'EOF'
FIT-VERDICT: seems ok
METRIC-PROTOCOL: mIoU
EOF
# OCCUPANCY, RECONSTRUCTION, RAW-FAILURES-READ, TYPICAL-PUBLISHED-DELTA missing

out=""; ec=0
out=$(OPENBUILD_ROOT="$SANDBOX" "$GUARDS/claim_preflight.sh" camp testsubstrate 2>&1) || ec=$?
if [ "$ec" -eq 1 ]; then ok "9a: BLOCKs with incomplete preflight"; else fail "9a: expected BLOCK (exit 1), got $ec"; fi
if echo "$out" | grep -q "OCCUPANCY"; then ok "9b: lists OCCUPANCY as missing"; else fail "9b: OCCUPANCY not listed"; fi
if echo "$out" | grep -q "RECONSTRUCTION"; then ok "9c: lists RECONSTRUCTION as missing"; else fail "9c: RECONSTRUCTION not listed"; fi
if echo "$out" | grep -q "RAW-FAILURES-READ"; then ok "9d: lists RAW-FAILURES-READ as missing"; else fail "9d: RAW-FAILURES-READ not listed"; fi
if echo "$out" | grep -q "TYPICAL-PUBLISHED-DELTA"; then ok "9e: lists TYPICAL-PUBLISHED-DELTA as missing"; else fail "9e: TYPICAL-PUBLISHED-DELTA not listed"; fi

# ── 10. claim_preflight.sh: PASS on complete fixture ─────────────────────────
echo ""
echo "-- 10. claim_preflight.sh: PASS with all fields --"

cat > "$FAKE_CAMPAIGN/preflight/testsubstrate.md" <<'EOF'
FIT-VERDICT: strong fit
METRIC-PROTOCOL: mIoU+AURC
OCCUPANCY: sparse 3 venues, not saturated
RECONSTRUCTION: treat as selective classifier under domain shift
RAW-FAILURES-READ: 12 failure cases read
TYPICAL-PUBLISHED-DELTA: +2-4pp mIoU
EOF

ec=0
out=$(OPENBUILD_ROOT="$SANDBOX" "$GUARDS/claim_preflight.sh" camp testsubstrate 2>&1) || ec=$?
if [ "$ec" -eq 0 ]; then ok "10a: PASSes with all fields present"; else fail "10a: expected PASS (exit 0), got $ec"; fi
if echo "$out" | grep -q "FIT-VERDICT"; then ok "10b: PASS output includes field lines"; else fail "10b: field lines not in PASS output"; fi

# ── 11. stale_ref_check.sh: PASS on clean fixture ────────────────────────────
echo ""
echo "-- 11. stale_ref_check.sh: PASS on clean docs --"

CLEAN_DOC="$SANDBOX/clean_doc.md"
echo "This is a totally clean document with no stale terms." > "$CLEAN_DOC"

ec=0
out=$(LIVE_DOCS="$CLEAN_DOC" TERMS_FILE="$GUARDS/stale_terms.txt" "$GUARDS/stale_ref_check.sh" 2>&1) || ec=$?
if [ "$ec" -eq 0 ]; then ok "11a: PASSes on clean doc"; else fail "11a: expected PASS (exit 0), got $ec (output: $out)"; fi

# ── 12. stale_ref_check.sh: FAIL with file:line on planted term ──────────────
echo ""
echo "-- 12. stale_ref_check.sh: FAIL on planted stale term --"

DIRTY_DOC="$SANDBOX/dirty_doc.md"
printf "Line 1\nLine 2 has codex:rescue planted here\nLine 3\n" > "$DIRTY_DOC"

ec=0
out=$(LIVE_DOCS="$DIRTY_DOC" TERMS_FILE="$GUARDS/stale_terms.txt" "$GUARDS/stale_ref_check.sh" 2>&1) || ec=$?
if [ "$ec" -eq 1 ]; then ok "12a: FAILs on planted stale term (exit 1)"; else fail "12a: expected FAIL (exit 1), got $ec"; fi
if echo "$out" | grep -q "codex:rescue"; then ok "12b: output includes the stale term"; else fail "12b: term not reported"; fi
# Expect file:line format
if echo "$out" | grep -qE "dirty_doc\.md:2"; then ok "12c: output includes file:line"; else fail "12c: file:line not in output"; fi

# ── 13. Idempotence: re-running overwrites ────────────────────────────────────
echo ""
echo "-- 13. Idempotence --"

"$TOOLS/exp_verify_mark.sh" test_campaign node_idem VERIFIED "first" >/dev/null 2>&1
sleep 1
"$TOOLS/exp_verify_mark.sh" test_campaign node_idem VERIFIED "second" >/dev/null 2>&1
count=$(ls "$REPO_ROOT/openbuild/test_campaign/exp_verify/" | grep "^node_idem" | wc -l)
if [ "$count" -eq 1 ]; then ok "13a: idempotent: still one marker file"; else fail "13a: expected 1 marker, got $count"; fi
if grep -q "second" "$REPO_ROOT/openbuild/test_campaign/exp_verify/node_idem.VERIFIED"; then
  ok "13b: marker overwritten with new content"
else
  fail "13b: marker not updated"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "============================================"
echo "Results: $PASS_COUNT passed, $FAIL_COUNT failed"
echo "============================================"
if [ "$FAIL_COUNT" -gt 0 ]; then exit 1; fi
exit 0
