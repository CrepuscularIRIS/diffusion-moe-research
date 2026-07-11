# Latent-Issues Audit — 2026-07-10 (post skill/plugin consolidation)

> Scope: re-read of `plan/` (root + Audit + taste-bank + ResearchOS + scouting + archive) and `opus-pass/`,
> plus `openbuild/*` run logs, checked against the live workflow (CLAUDE.md · goal-directive · research-os
> skills · router-protocol · Arbor state · tools/). Security excluded per user. Question: what can still
> degrade pipeline effectiveness / reliability / output quality, and are the established methods
> (decomposition · perspective-shift · simplification · reconstruction) actually enforced?

## 0. Verdict

The rule-set is in the best shape it has ever been (current, de-duplicated, single-authority). The dominant
residual risk is not missing rules — it is the **enforcement gap**: the archive shows the same top failure
across every campaign — *the violated rule existed in a document at the time* — and two structural guards
built to close it (`tools/guards/no_adversary_without_expverify.sh`, `tools/gpu_queue.py`) are verified but
**wired to nothing**. The single most predictive fact: `/exp-verify` was diagnosed on 2026-07-10 as "0 uses
ever = the process-over-product breaker, north-star 0→1" — and the SAME DAY, the MM-OVSeg reproduction, both
phenomenon-gate probes, and the P0 region-close all ran **without one `/exp-verify` artifact**
(`openbuild/optical_sar/exp_verify/` does not exist).

## 1. The meta-pattern (highest-confidence prediction of the next failure)

**RULES-EXIST-BUT-NOT-INVOKED.** Evidence chain across archives (subagent-mined):
ceiling-probe-first existed → skipped (DSpark, 10h train before the probe) · kill-checkpoint existed →
ignored (step-500 kill signal, silent restart-from-0) · tree-first existed → water deferred the tree to the
pilot · `/adversary` required → −16% claim shipped with a known confound, adversary never ran ·
`/exp-verify` required → never once executed. Prose rules lose to momentum at hot moments; only executable
gates and artifacts survive. The 2026-07-09 runtime-harness decision reached exactly this conclusion
(simplify → enforce ~6 invariants); Phase-1 simplify is now ~done, **Phase-2 enforce stalled at 1 guard
built / 0 wired** — the harness plan itself is an 80%-done thread (the FINISH anti-pattern at the meta-level).

## 2. Findings (ranked)

### P0 — will bite the very next experiment
1. **`/exp-verify` still never fires; the guard is unwired.** The P0 NO-GO rests on probe code whose runs
   were never anti-no-op verified (RUNLOG's own caveats: 24×24 majority grid; post-hoc zeroing ≠ trained
   ablation). The kill had independent review, so it stands — but the NEXT claim-bearing number (BRIGHT
   reproduction) must go 0→1, and nothing forces it. **Fix (~15 min):** wire into CLAUDE.md §4 DISPATCH/claim
   rows: `/exp-verify` writes `openbuild/<campaign>/exp_verify/<node>.VERIFIED`; `/adversary` and any
   region-close/promotion require `tools/guards/no_adversary_without_expverify.sh <campaign> <node>` PASS.
2. **`.arbor/active-run` pointed at `aerial-vln`** while optical_sar nodes were being written (explicit-path
   writes saved us; any implicit resume would have oriented on the archived campaign). **FIXED in this audit**
   (switched to `optical_sar`; backup kept).
3. **`gpu_queue.py` verified but unwired** (T4 deferred) — the BRIGHT reproduction will launch ad-hoc and
   repeat the idle-GPU pattern the queue was built to kill. **Fix:** one paragraph in CLAUDE.md rule 2:
   training/eval jobs go through `tools/gpu_queue.py`; its state json doubles as the missing monitor registry.

### P1 — must close before claim-bearing BRIGHT runs
4. **Reviewer-provenance unrecorded (audit P1.5), and the risk has GROWN**: GPT-5.6 is now both the default
   design REFINER (`/forge` step 7) and the primary `CLAIM_STANDS` substrate. A co-proposer reviewing its own
   design is the agreement-illusion the archive documents (F5-09:G1/G2). **Fix:** add a `PROPOSERS:` line to
   the `/prereg` card (every engine that touched the design); `/adversary` routes CLAIM_STANDS to a family
   NOT on that line (agy-Gemini / human when GPT-5.6 co-proposed).
5. **BRIGHT evaluation protocol undefined** (audit P1.1/P1.2 retargeted to the new substrate): exact DFC25
   metric + formula, statistical unit (event/scene — never pixels), seed policy, failure-source label
   provenance under building-damage/cross-event shift, held-out-event discipline. Also the **venue-taste
   5-line fit verdict for BRIGHT is not yet written** (mandatory before claim-bearing `/forge`), and
   occupancy triage for "reliability/misregistration on BRIGHT/DFC25" has not run.
6. **Reconstruction has no trigger on the live path.** The step is installed (`/prospect` v1.1.0 + MoA
   reconstruction mode + firewall) but only fires when `/prospect` fires — and the loop legally bypasses it:
   `/autopsy` conversion → `/forge` directly; backup promotion → reproduce → `/forge` directly. The aerial
   history shows the cost (the data-assimilation reframe had to be human-injected). **Fix:** one sentence in
   `/forge` step 2 or goal: *first claim-bearing `/forge` on a NEW substrate/territory must carry a
   reconstruction pass (the `/prospect` step or MoA reconstruction mode) before candidate generation.*
7. **Monitor discipline is still artifact-less** (audit P2.2): the BRIGHT download sat 22h as a dead Xet
   partial with no watcher armed (armed only after diagnosis) — the live demonstration. Minimal fix: watcher
   armed AT launch (rule already exists in prose) + `gpu_queue` state json as the registry for GPU jobs;
   downloads get a `dl_logs/` entry + Monitor before detach.

### P2 — reliability hygiene
8. **Doc-drift is systemic, not incidental** — even the 2026-07-10 refresh initially left 3 stale routers
   (scouting README ranking archived directions; plan/README pointing to it as current; moa-design doc
   presenting the Codex-era stack as implemented-status). All three **FIXED in this audit** (archival banners
   + pointer rewrite). Standing rule that would have prevented it: a capability/direction change is not done
   until `grep` across plan/ + memory for the old name comes back clean.
9. **External-brain session artifacts:** the `loose-root-2026-07/` files are raw ChatGPT DOM snapshots saved
   as "research artifacts" — zero extractable content. Rule: every GPT-5.6 session banks a labeled
   `pro-<topic>-<date>.md` with the question + the answer; raw browser state is never an artifact.
10. **Banked-anomaly mining:** the P0 kill banked a real anomaly (unseen water = uncertain-but-correct,
    SAR-rescued vs unseen road = confident-but-wrong → class-conditional SEMANTIC calibration, feeds
    Backup B). It is in the epitaph + memory; the next optical-SAR `/prospect` must consume it (Mine 1) —
    the "~3-nats banked-never-mined" leak is the documented precedent.
11. **The aerial-DA candidate is an unowned open thread** (banked, kill-probe designed, nobody triggers it).
    Give it explicit PARK semantics: `REOPEN-IF: user adopts via /goal, or optical-SAR region-closes` — else
    it becomes the dangling-80% pattern.

## 3. Methodology enforcement check (the user's specific question)

| Step | Where it lives | Fires in practice? |
|---|---|---|
| **Decomposition** | `/prospect` five mines; MoA 6-round chain (router 连续询问); "decompose, don't single-shot" (CLAUDE.md rule 6) | ✅ evidenced (aerial NODE12 MoA ideation; chain design). Watch: tactical in-line decisions legally bypass it — acceptable under reversibility tiering, but irreversible forks MUST panel. |
| **Perspective transformation (视角转换)** | frames axis (forced non-incumbent frame + DIFF-PREDICTION); structured dropout/blinding (router step 4; forge two-call blinded protocol); rival school | ✅ machinery present + operator bank healthy (61 ★, corrosion gate, anti-patterns ledger). N1 recoverability-gated-fusion effectively fired in the MM-OVSeg ablation kill. |
| **Simplification** | latent-root compression (`/prospect`); He-bar generative mode + two-sentence test (forge hard rules — the pipeline-audit fix landed) | ✅ present; prompt-enforced only. |
| **Reconstruction** | `/prospect` v1.1.0 forced step + card field + firewall; MoA reconstruction mode | ⚠ installed but **never yet exercised**, and the live path can bypass `/prospect` entirely (finding 6). The BRIGHT first `/forge` is the test case. |

Bottom line: all four are now *documented and machined*, three of four are evidenced in artifacts, but every
one of them is prompt-enforced — and §1 says prompt-enforcement is exactly what historically fails. The two
executable guards that exist must be wired, and reconstruction needs its substrate-switch trigger.

## 4. What is healthy (verified, not assumed)

- **Reproduce-first actually happened** (MM-OVSeg 73.61 vs 73.1, eval-only, faithful) — the aerial ROOT
  LESSON took hold.
- **The phenomenon gate killed P0 cheaply BEFORE method-building** — kill-before-build working as designed;
  ~zero GPU wasted on a doomed mechanism (contrast: aerial burned a campaign on an unvalidated base).
- **Conversion law + epitaph discipline real**: `mm-ovseg-selective.md` epitaph written, anomaly banked, tree
  region-closed with no dangling nodes, Backup A promoted per the pre-declared rule without a human menu
  (autonomy rule 1 exercised correctly — only the Baidu branch was human-gated).
- **Artifact-fidelity followed** in the recent RUNLOG (numbers carry artifact paths).
- Operator bank hygiene (retrieval-index-first, dedomaining, deletion test, demotions recorded) is the
  strongest-governed asset in the repo.

## 5. Fixes applied during this audit
1. `.arbor/active-run` → `optical_sar` (backup at `.arbor/active-run.bak-2026-07-10`).
2. `plan/scouting/README.md` → archival do-not-route banner; `plan/README.md` scouting row corrected.
3. `plan/moa-advisor-panel-design-2026-07-04.md` → historical-design banner (router-protocol is authority).

## 6. Recommended next actions (ranked by risk-per-minute)
1. Wire the two built tools (finding 1+3): exp-verify marker + adversary guard + gpu_queue paragraph. ~15 min.
2. BRIGHT preflight bundle before first claim-bearing `/forge`: venue-taste verdict · metric/unit/label
   protocol · GPT-5.6 occupancy triage · **reconstruction pass** (findings 5+6).
3. `PROPOSERS:` provenance line in `/prereg` + reviewer-exclusion in `/adversary` (finding 4). ~10 min.
4. PARK line for the aerial-DA candidate (finding 11).

> IMPLEMENTED 2026-07-10 (plan/sdd-pipeline-enforcement-2026-07-10.md): guards wired (tools/guards/ +
> skills), gpu_queue wired into CLAUDE.md rule 2, PROPOSERS provenance added, aerial-DA PARK line set.
> Item 2 (BRIGHT preflight bundle) is now MACHINE-GATED by tools/guards/claim_preflight.sh — produced by
> the research loop itself, not by this change-set.
