#!/usr/bin/env bash
# moa_chain.sh — fire a CONSECUTIVE chain of questions at the MoA panel (the DEPTH axis; complements
# moa_panel.sh's BREADTH). After 逆向溯因 (reverse-inference), Opus DECOMPOSES ONE problem into rounds
# and drills them in sequence instead of asking once. Query count = rounds × advisors → far more diverse.
# NOTE: per-lane round dirs inherit moa_panel's ≥MOA_MIN_LANES FAMILY quorum — for a deliberately
# focused (e.g. 2-lane) deep round, set MOA_MIN_LANES explicitly for that invocation.
#
# Round MENU (Opus writes the prompts; each round = a per-lane dir or a shared .txt). DEFAULT = 2–3
# reconciled rounds per the routing skill (a further round only if the dispute-map CHANGED); the six
# below are the palette, not a schedule:
#   q1 ROOT       — LATENT-ROOT / 逆向溯因: do the bottlenecks share ONE hidden cause?
#                   Return ROOT=<common cause> or SPLIT=<causes + ROOT-DISCRIMINATOR>; no fixes yet.
#   q1b DISCRIM   — optional: if q1 roots conflict, ask the cheapest root-discriminator before mechanism design
#   q2 SIGNAL     — model each signal's physical role before proposing a head
#   q3 MECHANISM  — sharpest attack on that upgraded object/root; name MVE
#   q4 RIVAL      — what a DIFFERENT school/frame would do, plus the one-step-up object
#   q5 SELF-ATTACK— the biggest failure reason (leakage·baseline·metric·seed·budget·scale)
#   q6 CHEAP PROBE— fastest pre-GPU GO/KILL; prefer ORACLE-CEILING, TRIVIAL-FLOOR, or ROOT-DISCRIMINATOR
#
# INFORMED chain: run round-by-round — Opus RECONCILES each round and writes the NEXT round's prompts from the
# prior answers (q2 uses q1's root; q1b resolves root conflicts; q5 attacks q3; q6 probes q5). This wrapper fires the rounds PRESENT and labels
# them; it does NOT auto-generate follow-ups (decompose + reconcile is Opus's job). Opus does NOT solo-answer —
# the panel ANSWERS (diversity); route the HARDER rounds (q1 root, q2 design) to GPT-5.6 Pro instead.
# (DeepResearch DROPPED 2026-07-06 — Cloudflare-blocked, ClaudeCode cannot read its output.)
#
# ROUTING TRUTH: this script fires the PANEL rounds ONLY (moa_panel.sh). It does NOT call Pro. The harder rounds
# routed to GPT-5.6 Pro are BROWSER/MANUAL artifacts — save each Pro reply as <round>_pro.md in the chain dir
# (e.g. q1_pro.md, q2_pro.md). This script SKIPS *_pro.md|*_pro.txt from the panel loop and lists them at the end;
# Opus reconciles the panel rounds + the *_pro.md Pro artifacts together before /prereg.
#
# Usage:
#   moa/moa_chain.sh <chain-dir>     # fires, in natural-sort order, every q*/ (per-lane) or q*.txt (shared)
set -uo pipefail
case "${1:-}" in -h|--help) sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 0;; -*) echo "[moa_chain] unknown flag: $1" >&2; exit 2;; esac
DIR="$(cd "$(dirname "$0")" && pwd)"
CH="${1:?usage: moa_chain.sh <chain-dir>  (contains q1/ q2/ ...  or  q1.txt q2.txt ...)}"
[ -d "$CH" ] || { echo "[moa_chain] chain dir not found: $CH" >&2; exit 2; }
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
  echo "########## PRO ROUNDS (GPT-5.6 Pro browser/manual artifacts — NOT fired by this script) ##########"
  for p in "${PRO[@]}"; do echo "  fold in at reconcile: $p"; done
else
  echo "########## NOTE: no q*_pro.md Pro artifacts — were the harder rounds (q1 root · q2 design) routed to GPT-5.6 Pro? save each reply as <round>_pro.md here ##########"
fi
echo "########## END CHAIN (${#ROUNDS[@]} panel rounds, ${#PRO[@]} Pro artifacts) — Opus reconciles panel + Pro, then /prereg ##########"
