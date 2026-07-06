#!/usr/bin/env bash
# moa_chain.sh — fire a CONSECUTIVE chain of questions at the MoA panel (the DEPTH axis; complements
# moa_panel.sh's BREADTH). After 逆向溯因 (reverse-inference), Opus DECOMPOSES ONE problem into ~5 questions
# and drills them in sequence instead of asking once. Query count = rounds × advisors → far more diverse.
#
# Default 5-question drill (Opus writes the prompts; each round = a per-lane dir or a shared .txt):
#   q1 ROOT       — 溯因: what MOVE generated the SOTA / what is the TRUE load-bearing bottleneck?
#   q2 MECHANISM  — the sharpest attack on that root under the ≤4h envelope
#   q3 RIVAL      — what a DIFFERENT school/frame would do instead (force divergence)
#   q4 SELF-ATTACK— the biggest failure reason (leakage·baseline·metric·seed·budget·scale)
#   q5 CHEAP PROBE— the fastest pre-GPU test that decides GO/KILL
#
# INFORMED chain: run round-by-round — Opus RECONCILES each round and writes the NEXT round's prompts from the
# prior answers (q2 uses q1's root; q4 attacks q2; q5 probes q4). This wrapper fires the rounds PRESENT and labels
# them; it does NOT auto-generate follow-ups (decompose + reconcile is Opus's job). Opus does NOT solo-answer —
# the panel ANSWERS (diversity); route the HARDER rounds (q1 root, q2 design) to GPT-5.5 Pro instead.
# (DeepResearch DROPPED 2026-07-06 — Cloudflare-blocked, ClaudeCode cannot read its output.)
#
# ROUTING TRUTH: this script fires the PANEL rounds ONLY (moa_panel.sh). It does NOT call Pro. The harder rounds
# routed to GPT-5.5 Pro are BROWSER/MANUAL artifacts — save each Pro reply as <round>_pro.md in the chain dir
# (e.g. q1_pro.md, q2_pro.md). This script SKIPS *_pro.md|*_pro.txt from the panel loop and lists them at the end;
# Opus reconciles the panel rounds + the *_pro.md Pro artifacts together before /prereg.
#
# Usage:
#   moa/moa_chain.sh <chain-dir>     # fires, in natural-sort order, every q*/ (per-lane) or q*.txt (shared)
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
CH="${1:?usage: moa_chain.sh <chain-dir>  (contains q1/ q2/ ...  or  q1.txt q2.txt ...)}"
shopt -s nullglob
ALL=( "$CH"/q* )
# split: PANEL rounds (fired here) vs Pro browser/manual artifacts q*_pro.md|q*_pro.txt (NOT fired — listed at end)
ROUNDS=(); PRO=()
for f in "${ALL[@]}"; do
  case "$f" in *_pro.md|*_pro.txt) PRO+=("$f");; *) ROUNDS+=("$f");; esac
done
[ ${#ROUNDS[@]} -eq 0 ] && { echo "no q*/ or q*.txt PANEL rounds in $CH (only Pro artifacts?)" >&2; exit 2; }
IFS=$'\n' ROUNDS=($(sort -V <<<"${ROUNDS[*]}")); unset IFS
n=0
for r in "${ROUNDS[@]}"; do
  n=$((n+1))
  echo "########## MoA CHAIN — round $n/${#ROUNDS[@]}: $(basename "$r") ##########"
  if [ -d "$r" ]; then "$DIR/moa_panel.sh" --per-lane "$r"; else "$DIR/moa_panel.sh" "$r"; fi
  echo
done
if [ ${#PRO[@]} -gt 0 ]; then
  IFS=$'\n' PRO=($(sort -V <<<"${PRO[*]}")); unset IFS
  echo "########## PRO ROUNDS (GPT-5.5 Pro browser/manual artifacts — NOT fired by this script) ##########"
  for p in "${PRO[@]}"; do echo "  fold in at reconcile: $p"; done
else
  echo "########## NOTE: no q*_pro.md Pro artifacts — were the harder rounds (q1 root · q2 design) routed to GPT-5.5 Pro? save each reply as <round>_pro.md here ##########"
fi
echo "########## END CHAIN (${#ROUNDS[@]} panel rounds, ${#PRO[@]} Pro artifacts) — Opus reconciles panel + Pro, then /prereg ##########"
