# Pipeline Audit — current workflow vs Fable.md / GPT.md / spark.md (2026-07-05)

**Sources:** `plan/Audit/Pipeline/{Fable,GPT}.md` = the elite-lab PRACTICE checklist (Karpathy · Kaiming He ·
Schulman · Hamming). `plan/Audit/Pipeline/spark.md` = the META-thesis (判断质量 + 反馈闭环 + 标准强度; what AI
CAN vs CANNOT substitute). **Verdict on Fable+GPT:** the workflow already IMPLEMENTS the systematizable core; the
gaps are (a) paper-skeleton-early, (b) two explicit prompt-batteries from spark.md, (c) a few soft habits. It made
TWO deliberate tradeoffs (刷分-first · compressed timescale) — both real, both guarded, one of which just misfired.

Legend: ✅ done · ⚠️ partial · ❌ missing · 🔀 deliberate tradeoff.

## A. Problem selection
| Practice (Fable/GPT) | Live machinery | Verdict |
|---|---|---|
| Work backward from a BOTTLENECK, not forward from a technique | `/prospect` Mine 0 (own-log anomalies FIRST) + goal "metric-GAP = the failure" | ✅ |
| Prefer problems where the NULL result is informative | `/prospect` SURPRISE field + `/autopsy` conversion law (every null → constraint/candidate/region-close) | ✅ **strength** |
| Ride the rising tide, position ahead ("we leave X to future work" signal) | atlas/occupancy touches it; TIMING not formalized | ⚠️ (spark: 位置感 = AI-难补 → accepted) |
| SIMPLICITY as a selection criterion + "explain in 2 sentences, non-expert sees why" | `taste.md` + operator `core_simplification`; but the 2-sentence test is not an explicit admission gate | ⚠️ → **FIX** |
| Avoid incrementalism = REFORMULATE (change eval/assumption/framing) | necessity gate + 14-frame axis + anti-retreat guard | 🔀 **TRADEOFF**: goal is 刷分-first (accepts the field's metric = incrementalism risk) — guarded by anti-retreat + "occupancy re-prices ⇒ BEAT it", but this is the sharpest tension with Fable |

## B. Hypothesis & pre-experiment discipline
| Practice | Live machinery | Verdict |
|---|---|---|
| Write the PAPER SKELETON before main experiments (abstract, claims, empty table shells, Fig 1) | none — `/prereg` seals the evidence contract but there is no skeleton/table-shell artifact | ❌ **MISSING → FIX** (activate at band-hit) |
| ONE hypothesis/experiment, stated in advance, with a predicted outcome | `/prereg` + MoA DIFF-PREDICTION + operator `differential_prediction` | ✅ **strength** |
| Minimum-viable-experiment: overfit tiny batch · loss-at-init · visualize inputs before the model | cheap_probe + smoke tests + oracle probe (we do the spirit); Karpathy's paranoid checklist not formalized | ⚠️ (optional FIX) |

## C. Baselines & experimental hygiene
| Practice | Live machinery | Verdict |
|---|---|---|
| Tune the BASELINE as hard as your method | `/adversary` "make the OPPOSING baseline win" / goal "TUNED baseline" | ✅ **strength** |
| One-thing-at-a-time + canonical trunk + fixed seeds + MULTIPLE seeds | `/prereg` one-variable + Arbor trunk + ≥3 seeds paired | ✅ |
| Ablation = the ARGUMENT (mechanism), not an appendix | `/exp-verify` anti-no-op (intervention provably fired) + negative control + locality | ✅ **strength** |
| Failure analysis SCHEDULED · become-one-with-the-data · try to DESTROY your good number | `/autopsy` + `/adversary`; we found forward-collapse by reading raw rollouts | ✅ (but make the destroy-battery LITERAL — see spark §2) |

## D. Reading & idea generation
| Practice | Live machinery | Verdict |
|---|---|---|
| Read shallow-WIDE by default, deep-NARROW adversarial (reimplement key parts) | Rule 8 精读 reverse-inference = deep-narrow ✅; the daily shallow-wide skim is not a formal step | ⚠️ 🔀 (tradeoff for a focused campaign — minor miss of the "future-work signal") |
| Idea backlog with CHEAP KILL criteria | `/forge` REGENERATION RULE + KILL + cheap_probe per candidate | ✅ |
| Ideas come from FRICTION (own experiments), not literature | `/prospect` OWN-LOG ANOMALIES FIRST | ✅ **strength** |

## E. Collaboration structure
| Practice | Live machinery | Verdict |
|---|---|---|
| Small core, CLEAR ownership | single code-owner: Opus PI + executor subagents | ✅ |
| Frequent syncs · decisions IN WRITING · unit of discussion = a plot/table | RUNLOG + Arbor tree + numbers-from-artifacts | ✅ |
| Internal review as a REAL adversarial gate (Reviewer 2, pre-submission) | Codex review hook + `/adversary` + `arbor-peer-review-gate` | ✅ **strength** (genuine independent substrate) |

## F. Kill / scale decisions
| Practice | Live machinery | Verdict |
|---|---|---|
| TIME-BOXED gates; kill criteria written at project START | `/prereg` pre-declared falsifier + ≤4h cap + region-close discipline | ✅ 🔀 (compressed from weeks → hours) |
| Distinguish KILL from PARK + a one-page postmortem | `/autopsy` + atlas `EPITAPH` (kill) vs `REOPEN IF` (park) | ✅ **strength** |
| Scale only AFTER the small version is clean | cheap_probe → smoke → train ladder | ✅ |

## G. Writing & narrative  (mostly deferred — pre-contribution)
| Practice | Live machinery | Verdict |
|---|---|---|
| Start writing at ~50% completion | none yet | ❌ (same gap as B-skeleton; activate at band-hit) |
| Claim-FIRST · ONE claim/paper · Figure-1 effort | `/adversary` claim ≤ contracted envelope + single-contribution goal; craft deferred | ⚠️ (correctly deferred) |

## H. Anti-patterns — are we AVOIDING them?
| Anti-pattern | Guard | Status |
|---|---|---|
| Tune method, baseline at default | `/adversary` tuned baseline | ✅ guarded |
| Big system before toy verification | cheap_probe / smoke first | ✅ guarded |
| Grad-student descent (hp fiddling, no hypothesis) | `/prereg` hypothesis-first | ⚠️ RISK: fast-OODA "tactical tweaks LR/aug = Opus-solo" can drift into this |
| Reading for months to defer running | own-log-first, run NOW | ✅ guarded |
| Novelty-by-complexity | taste / simplicity / necessity gate | ✅ guarded |
| **Switch at week 3 ("all ideas feel bad at week 3")** | region-close requires ≥2 mechanisms, SAME root | ⚠️ **REAL RISK — JUST MISFIRED**: the compressed clock produced a PREMATURE region-close ("frozen-VLM can't beat AVDN"), retracted only after reading AerialVLA. **Rule 8 (SOTA-精读 before any region-close) is the fix — now applied.** |
| Believe a number without breaking it | `/exp-verify` + `/adversary` | ✅ guarded → make the 6-question battery LITERAL (spark §2) |
| Solo hero, no adversarial feedback | Codex hook + MoA + Pro | ✅ guarded |

## THE TWO DELIBERATE TRADEOFFS (取舍) — named, so they're chosen not drifted-into
1. **刷分-first / high-throughput OODA** vs Fable's "reformulate, don't accept the field's metric." Chosen for tractability + the ≤4h cap + a 一区 improvement bar. RISK = incrementalism. GUARD = anti-retreat + necessity gate + occupancy-re-prices-⇒-BEAT-it. *Keep, but the necessity gate must actually fire.*
2. **Compressed timescale** (a "project" = hours/days, not the 2wk/6-8wk cadence). Necessary given AI speed + the cap. RISK = the week-3 premature-switch anti-pattern at a faster clock (it MISFIRED once). GUARD = ≥2-mechanism-same-root region-close + Rule 8 read-the-field-before-closing.

---

# spark.md — the CORE. Mandatory angles for Goal / Claude / MoA.

spark's thesis: *一般工作者在任务里工作；顶级工作者在系统里工作* — pursue EVIDENCE-QUALITY, not output. And its
sharpest operational warning for an AI-run pipeline: **AI 放大功底 — 功底强时放大效率，功底弱时放大幻觉**; an AI
loop's native failure mode is producing 看起来像研究 (research-SHAPED output), not a 真实结论. These become two
standing prompt-batteries + one stance — ENCODED into CLAUDE.md rule 9 + the MoA router output contract.

### Battery 1 — SELECT (every cycle, uncertainty-first). Ask THESE, not "what's the next step":
1. 当前最大的未知是什么？ (What is the biggest UNKNOWN right now?)
2. 哪个实验能最快减少不确定性？ (Which experiment reduces it FASTEST — info-gain, not task-completion?)
3. 如果结果成立，它能支撑什么 claim？ (If it HOLDS → what claim does it support?)
4. 如果不成立，该 kill / park / reformulate？ (If NOT → kill / park / reformulate — pre-decided?)

### Battery 2 — BEFORE believing ANY good number (标准强度 = attack your own result):
1. 数据泄漏 / train-test 污染？   2. baseline 被低估 / 欠调？   3. metric 奖励了错误行为？
4. 随机种子偶然（跨 seed 翻转）？   5. 提升只是调参 budget 的产物？   6. 跨 seed / 数据集 / 规模仍成立？
> A number that has not survived all six is a HYPOTHESIS, not a result. This is `/exp-verify` + `/adversary` made
> into a literal, always-run checklist — and the MoA panel must apply it to every proposed mechanism in advance.

### The stance (validates the current design — do NOT try to automate these away):
- **选题品味 (problem taste)** + **主见 (informed-contrarian judgment)** = spark's AI-难补 layer → they STAY
  human (goal: human seeds + redirects; contribution = human). spark.md is external VALIDATION of the one-invariant.
- **标准强度 (standard intensity)** = the MOST systematizable of the "hard" layers → Battery 2 + the independent
  substrate (Codex/Pro) is exactly how we substitute for it. Lean into it.
- **杀项目 (kill ability)** = structurally solved (`/autopsy` + region-close + anti-retreat) — the residual is
  psychological, and an AI loop is LESS sunk-cost-bound than a human, which is an advantage to exploit.

## Applied this pass
- **CLAUDE.md rule 9** — the spark stance + Battery 1 + Battery 2 (always-loaded).
- **`moa/router-protocol.md` step 5** — output contract gains a `BIGGEST SELF-ATTACK` field (Battery 2 applied
  per advisor, in advance) so MoA pressure-tests a mechanism's claimed gain BEFORE it eats a training run.

## Recommended, NOT yet applied (need a trigger, not a config line)
- **Paper-skeleton-early** — at the moment a mechanism clears `/exp-verify` and is on track for the 24–28 band,
  draft {title · abstract · claim · main-table shells · Fig-1} and let each further run fill a cell or get cut.
- **Two-sentence simplicity test** — add to `/forge` operator admission ("explain the move in 2 sentences; does a
  non-expert see why it should work?").
- **Karpathy paranoid-pipeline checklist** — formalize {overfit tiny batch · loss-at-init · visualize inputs} as a
  cheap_probe sub-checklist (we do the spirit; make it explicit).

---

# InsightPlus.md / InsightPro.md — MODELABILITY map (2026-07-05)

**Reframe (user, 2026-07-05):** don't ask "can a human learn this" — ask **"can a Harness + Loop + MoA MODEL it
into a rule?"** The goal is to DESIGN a workflow that substitutes the human as far as possible, not to replicate
human learning. So each principle is scored by MODELABILITY, and the docs sort into THREE tiers. (Paper-writing
principles PARKED per user.)

## InsightPlus (15 explicit "hidden principles") — root = *treat yourself as the most dangerous error source;
design PROCESS to constrain yourself.* This IS the research-os design philosophy (gates · DOWN-only · independent
substrate · one invariant). **~90% ALREADY MODELED** → it VALIDATES the harness thesis.
| # | principle | live rule | status |
|---|---|---|---|
| 1 | good result false until broken | rule 9 Battery 2 · `/adversary` | ✅ RULE |
| 2 | baseline = enemy, tune it strong | `/adversary` tuned baseline | ✅ RULE |
| 3 | complexity = suspect; 2-3-sentence test | `taste.md`/`core_simplification`; 2-sent test not a gate | ⚠️ add to `/forge` |
| 4 | kill criteria at START | `/prereg` pre-declared falsifier | ✅ RULE |
| 5 | write a PREDICTION before every run | `/prereg` + DIFF-PREDICTION | ✅ RULE |
| 6 | prove small before big | cheap_probe → smoke → train | ✅ RULE |
| 7 | writing = a research TOOL (skeleton early) | — | ⏸ PARKED (user) |
| 8 | one core claim per paper | single-contribution goal | ✅ RULE |
| 9 | meetings judge EVIDENCE not status | artifact-first RUNLOG/tree | ✅ RULE |
| 10 | internal review crueler than external | Codex hook + `/adversary` + peer-gate | ✅ RULE |
| 11 | read to FIGHT (solved/not/assumptions/weakest) | rule 8 精读 reverse-inference → atlas rows | ✅ RULE |
| 12 | ideas from FRICTION not brainstorm | `/prospect` own-log-first | ✅ RULE |
| 13 | decisions in WRITING, distrust memory | RUNLOG/tree/agentmemory | ✅ RULE |
| 14 | real goal = FUTURE test set, not leaderboard | anti-retreat + occupancy-re-prices | ⚠️ sharpen: "current bench = training set" |
| 15 | output quality from ENVIRONMENT not willpower | the MoA/substrate design itself | ✅ = tier-2 |

## InsightPro (tacit layer — reverse-engineered from BEHAVIOR) — the HIGH-VALUE, UNDER-MODELED set. Yields **~6
NET-NEW modelable harness rules** (folded into CLAUDE.md rule 10):
| # | tacit behavior | modelable as | status |
|---|---|---|---|
| 4 | reversible vs irreversible; deliberate only on irreversible | **reversibility ROUTING**: reversible → decide instantly; irreversible (region-close · pivot · which mechanism eats ≤4h · publish) → MoA+Pro+`/adversary` | ★★ NET-NEW |
| 1 | understanding is the bottleneck; STOP at confusion | **confusion = HALT**: pay down an unexplained result BEFORE proceeding | ★ NET-NEW (fixes AVDN close) |
| 3 | response-to-reality latency ≈ 0 | **zero-latency to VERIFIED evidence, not noise** (pivot on `/exp-verify` VERIFIED, not a smoke number) | ★ refines fast-OODA |
| 10 | they FINISH (the boring last 20%) | **no 80%-done threads**: verify → bank → update atlas/tree (node-7/32B dangling = the anti-pattern) | ★ NET-NEW |
| 5 | protect calibration; never bluff; errors findable | **calibration tagging** {verified · inferred · guess}; "unknown" instantly | ★ NET-NEW |
| 9 | keep SLACK to exploit surprise | **reserve budget for anomaly-chasing** ([ANOMALY] ledger) | ★ NET-NEW |
| 6 | do whole job; inspect INTERFACES | failure concentrates at handoffs (subagent · probe→train · eval→model) | ✅ ~`/exp-verify` |
| 2 | all claims provisional until verified | rule 9 + numbers-from-artifacts | ✅ RULE |
| 7 | rehearse in private | cheap_probe / MoA pre-GPU battery | ✅ RULE |
| 11 | apologize/repair fast | honest-reporting | ✅ RULE |
| 12,13 | environment/peers set taste; consume only the BEST | MoA panel choice + SOTA-only 精读 diet | ✅ = tier-2 |
| 14 | look stupid only toward learning; no fake competence | AI-amplifies-功底 warning (rule 9) | ✅ RULE |
| 8 | energy as a production system (top 2-3 hrs) | weak AI analog: spend the ≤4h cap on the highest-value mechanism | ~✅ efficiency-first |

## THE 3-TIER SYNTHESIS — the answer to "what substitutes the human?"
1. **RULES (harness — deterministic self-constraint).** ~90% of InsightPlus + ~6 of InsightPro. Fully
   substitutable — this is what a Loop/Harness IS. Self-distrust externalized into gates.
2. **ENVIRONMENT (judgment that isn't a rule but is PRODUCED by a feedback structure).** "biggest unknown?",
   "where is this paper weakest?", "is this complexity necessary?", "is this real or noise?" — a SINGLE model
   can't reliably self-generate these, but a STRUCTURE can: MoA diversity votes + independent substrate attacks +
   the atlas accumulates the map. This is InsightPro #12 ("environment sets taste") applied to an AI: **the AI's
   taste = its PANEL + its GATES + its ATLAS, not its weights.** ← where "MoA substitutes the human" is exactly right.
3. **HUMAN SEED (irreversible + un-environmentable).** "important in 2–3 years?" (future-test-set timing), the ONE
   ambition, the external-publish call. spark.md's residue SHRINKS to the irreversible forks + the initial seed.
**Design principle:** push self-distrust into RULES, push taste into the ENVIRONMENT (MoA + substrate + atlas),
shrink the HUMAN to the irreversible seed + redirects. This REFINES spark.md, not contradicts it — spark said
"taste is AI-难补 *for a single model*"; the answer is "then don't use a single model — engineer the environment
that produces the judgment." **USEFUL: yes — InsightPro's tacit layer is the highest-value input, because it names
the modelable behaviors the explicit checklists omit.**
