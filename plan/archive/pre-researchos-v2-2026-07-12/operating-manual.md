# Research Operating Manual

> **REFERENCE / history only.** Active rules live in `.claude/CLAUDE.md` (§0 design principles first),
> `plan/goal-directive.md`, the research-os skills, and `moa/router-protocol.md`; they win on conflict.
> Last updated: 2026-07-12. Live state is NOT duplicated here — read `.claude/CLAUDE.md` §3. ACTIVE direction =
> **world models → Information Sciences + AAAI** (adopted 2026-07-12), `plan/world-model-direction-2026-07-11.md`.
> Compute is PRICED per launch, never hard-capped; sim/RL fully allowed (`.claude/CLAUDE.md` §0.2).

---

## 1. Engine stack — MoA generates · GPT-5.6 refines+reviews · Opus conducts · human grants contribution

| Engine | Invoke | Role |
|---|---|---|
| **Opus 4.8 (main loop)** | direct | PI / decision-owner / interpreter. Runs `/prospect`·`/forge`·`/autopsy`, decomposes ideation into the MoA chain, reconciles (dispute-map), makes the tactical SELECT, packages external hand-offs, updates tree/RUNLOG. Never self-grants `CLAIM_STANDS`. |
| **Sonnet 4.6 executor subagents** | `Agent` `model:"sonnet"` (+ `isolation:"worktree"` when mutating files) | ALL implementation / experiment plumbing / verification runs / repo exploration / debug. Returns changed-files + commands + test-results + artifact-paths + known-risks. Does NOT judge worth, grant a PASS, touch a sealed holdout, or rewrite the thesis. Escalate a single subagent to Opus only for a genuinely hard bug. |
| **MoA advisor panel** | `moa/moa_panel.sh --per-lane` / `moa/moa_chain.sh` | The DEFAULT GENERATOR on high-value forks: 6 differentiated advisors — Gemini 3.1 Pro (`agy`) · GPT-5.5 (`codex`) · Opus 4.6 · MiMo V2.5 Pro · DeepSeek V4 Pro · Qwen3.7 Plus (last three via the OpenCode gateway). Each gets a rotated operator + frame + school + structured dropout; Opus reconciles. TIERED: routine 刷分 = solo Opus; medium = Opus + 1; the full panel is for forks, not every iteration. |
| **GPT-5.6 external brain** | Playwright → ChatGPT, high-reasoning, ONE lane, context-free | Three roles: (a) SEARCH + TRIAGE — occupancy ("做过没有?") on abstracts/keywords/citations, never close-reading; (b) CLAIM/PROPOSAL review — cross-family + stateless = the independent substrate (frame it to REFUTE); (c) refine the SELECTED design / execute generative research-os workflows. Compact self-contained hand-off per query (no campaign memory); new chat per problem; poll ~15 min; keep Playwright alive — never close/restart. Never picks direction or seals novelty. |
| **Human** | last-resort escalation + final authority | Forced domain/dataset switch, new large resource/cloud/hardware, destructive/irreversible ops, external publish/submission, or a repeated no-progress block. Contribution/paper promotion is always human. |

- **Independent review** = a deliberate, context-free, cross-family query (GPT-5.6 browser or `agy`-Gemini) — the
  first escalation sink before the human, and the only `CLAIM_STANDS` substrate. A finding = binding DOWN; it never
  grants UP; silence ≠ pass. Dev/diff review = an Opus subagent + the `code-review` skill; `codex exec` / `agy` CLIs
  are callable via bash for a specific cross-check.
- **Browser division:** **playwright-extension** (real Chrome, holds logins, anti-bot) → the ChatGPT/GPT-5.6 lane.
  **agent-browser** (own headless Chrome, concurrent) → arXiv / blogs / GitHub / docs legwork. Separate Chromes, no
  conflict. Fast model Q&A stays on the `codex`/`agy` CLIs, not a browser.

## 2. Arbor + the goal loop — state, waits, ownership

**Arbor MCP is the canonical state/execution layer**: `tree_view` · `tree_add_node` · `tree_update_node` ·
`tree_prune` · `tree_set_meta` · `worktree_create`/`worktree_remove` · `eval_run` · `git_merge_branch` ·
`generate_report` · `open_dashboard`. The idea tree is the canonical research STRUCTURE — update it at **every 验收,
tree FIRST, then RUNLOG**.

**GOAL = a continuous loop, not one stage.** `/prospect → /forge → /prereg → run → /exp-verify →
(claim → /adversary · null → /autopsy) → loop`; the `/autopsy` programme pulse runs after every 2nd `/autopsy`.
- **Anti-exhaustion: the backlog is ALIVE, never a menu.** Every `/autopsy` MUST emit its conversion-law output
  (constraint / candidate / region-close → lateral `/prospect`). Banking a negative that reshapes nothing is an
  incomplete autopsy; halting after banking is the #1 loop bug. Never end a session at "shortlist ready" — continue
  to the next live candidate.
- **Bounded autonomy:** ≤12 dispatched cycles/session; ≤3 consecutive inconclusive leads → stop+report; each
  experiment pre-declares its PRICED budget {measured ETA · GPU-hours · expected info-gain · kill-checkpoint} —
  no fixed cap; kill on budget overrun or >30 min zero-output.
  The run stops only when: a claim clears `/adversary` and reaches the human promotion gate; the programme pulse says
  STOP_AND_REPORT; or genuinely blocked after external-brain + cheap probes.
- A contribution/paper claim is NEVER an autonomous outcome — it hard-blocks to human (§5.1).

**GPU concurrency is platform-scoped**, re-derived at campaign start from the model's memory footprint (26B-class →
one job total; 4B/8B-class → one job per GPU, candidate+control paired across the two 4090Ds — an idle second GPU
during a training campaign is a bug). `nvidia-smi` BEFORE dispatch; queue, don't collide. Every long job is
main-agent tracked: PID/log/artifact + a main-agent `Monitor`; subagent-local monitors do not count.

**WAIT / PARK discipline — the wait is not the deliverable; the VERDICT is.**
- **Match the wait to the duration.** Minutes-long (inference probe, small verifier) → run synchronously in ONE turn
  and emit the verdict. Hours-long (real training) → arm a main-agent `Monitor` + end the turn.
- **Consume → verdict, never re-arm.** On signal-fire the next action is READ + DECIDE. The
  `arm-monitor → end-turn → notify → re-arm` loop is the canonical stall (once ~220k tokens / 2h with no verdict).
- Do NOT dispatch a subagent for a minutes-long probe — run it inline.
- **Subagent handoff invariant:** a subagent-launched job returns `{cmd,cwd,PID,log/artifact,ETA,budget,kill}`;
  the parent records it and owns the Monitor. No parent monitor = ORPHAN → verify with `ps` + artifact, attach or stop.
- **Circuit-breaker:** a wait that fires repeatedly / runs past ETA with no verdict artifact → stop waiting, check
  ground truth directly (`ps`, read the artifact). Never a `ScheduleWakeup` poll; browser waits = quiet 15-min checks.

**Ownership + kill safety.**
- **The single ownership test:** a process is provably ours iff (live) its cwd is under the project /
  `.claude/worktrees/` AND its cmd matches our job patterns. A registry/PID-file entry only says which PID to look
  at — it never proves ownership or authorizes a kill. A process with cwd outside the project is the user's
  co-tenant work (e.g. `JasonF/openpi`, `gaussian-splatting`) → busy-GPU, queue/wait, NEVER kill. Unsure → wait.
- **PID-reuse guard:** before ANY kill, re-verify the live process against the registry — cmd + cwd + start-time must
  ALL match, plus the ownership test. Mismatch = recycled PID → do not kill; clear the stale registry line.
- Kill triggers: on-resume orphan sweep (reconcile registry vs `ps`/`nvidia-smi`), or overrun (>budget / >30 min
  zero-output) — both require owned + re-verified.

## 3. Document conventions (the anti-drift contract)

| Artifact | Role | Cadence |
|---|---|---|
| `.claude/CLAUDE.md` | engine division + live state + hard rules + pointers | rarely |
| `plan/README.md` | one-screen flow map + plan/ index — START HERE | when structure changes |
| `plan/operating-manual.md` (this) | how-we-work reference: engines, Arbor, lessons, science kernel, types, commands | when process changes |
| `plan/goal-directive.md` | the exact `/goal` input (boundaries + hard stops) | when the goal changes |
| research-os plugin (`/home/lingxufeng/cli/research-os`) | the 6 commands + 4 axis references — the canonical prompt layer | when the method changes |
| **Arbor MCP tree** (`tree_view`) | canonical STRUCTURE — branches / status / result / insight / prune | **every 验收, FIRST** |
| `openbuild/<campaign>/` | RUNLOG + atlas + operators for the active campaign | per run |
| `plan/archive/` | closed campaigns and superseded process docs | — |

> **The #1 process bug to never repeat:** updating the RUNLOG but not the tree → the tree goes stale and the
> research looks linear. Tree first, every cycle.

## 4. Hard-won lessons

1. **Substrate integrity.** Verify model/checkpoint integrity before trusting any metric; ground-truth with a
   trivial task before committing compute.
2. **Metric validity.** Proxy metrics (loss, teacher-forced scores) often do not predict task quality — use
   end-to-end generation / verifier metrics as the primary signal.
3. **Failure-mode first.** Profile WHERE the model fails (generation-based) before designing a method.
4. **Tree discipline** (§3) + **independent review**: the proposer never self-grants `CLAIM_STANDS` — DOWN
   verdicts only; audit consequential executor diffs deliberately (GPT-5.6/agy or an Opus `code-review` subagent).
5. **Kill safety.** Kill hung/overrunning jobs immediately — but only after the §2 ownership test + PID-reuse
   re-verify. Never kill co-tenant work; unsure → wait. Measure-first (timing probe before heavy compute);
   `nvidia-smi` before dispatch; keep Playwright alive; never modify sealed eval/test/baselines.
6. **Subagent-dispatch discipline.** Per-turn latency scales with context size × concurrency. Do small clear tasks
   yourself (a few-minute direct edit beats a 30–50 min executor); leaner prompts; serialize heavy agents — never
   3–4 concurrent; executors = Sonnet 4.6.
7. **Filters don't create value — problem selection does.** A gate-heavy system selects for gateable work
   (eval/certificate drift); novelty gates must never judge 刷分 work; candidate menus exhaust — backlogs regenerate
   from failures; count SURPRISES (plan-changes), not progress tokens; process work >20% sustained = pulse flag.
8. **★ ARTIFACT-FIDELITY.** Every number in a banked/shipped document is READ FROM ITS ARTIFACT FILE at writing
   time, with the path cited — never recalled from memory. A planned-but-unexecuted probe's numbers are NOT
   results. Any push to a public remote requires the artifact-acceptance checklist: recompute each number from its
   cited source; mismatch = HOLD. (The DSpark archive shipped back-computed baselines and a phantom probe number.)
9. **★ LAUNCH ARITHMETIC + CHEAP-SIGNAL LADDER.** Before any training launch, in the `/prereg` (or a 3-line note):
   (a) measured sec/step × steps = ETA — over the declared budget ⇒ re-price (is the info-gain worth it?) or
   redesign; never an UNPRICED launch; (b) data-sufficiency ratio vs the
   reference recipe; (c) a declared KILL-CHECKPOINT {step, threshold, action=KILL}, enforced by a main-agent
   Monitor armed at launch (`grep -E` progress · threshold-cross · `Traceback|resume-failed|OOM|Killed`) — a resume
   failure is a STOP, never a silent restart; (d) never retrain what a released checkpoint provides. LADDER: the
   forge KILL experiment defaults to an inference-time replay / oracle probe when one exists — no training before
   its oracle-replay upper bound is measured.
10. **GPU throughput defaults.** Generation-heavy steps use vLLM / batched generation, never unbatched HF
    `.generate()` (~20–50× waste); measure samples/s in the first minute and abort if ETA > budget. Small-model
    campaigns keep BOTH GPUs busy.

## 5. Science protocol (the kernel) + research-os v1.1

Falsify-before-build (ship the kill-experiment WITH the idea) · score-up ≠ mechanism (needs negative control +
locality) · eval/test/baselines are a **sealed layer, never changed mid-run** · one variable per probe · isolation:
generator ≠ executor ≠ critic · experiment has absolute veto over elegance · every claim-bearing run pre-declares
its contract (`/prereg`) · when evidence contradicts the direction, redesign the program, don't defend it. A
negative result is a SUCCESS iff its autopsy generated something.

> **Independent substrate** = a context-free cross-family model (GPT-5.6 browser / agy-Gemini), a dispatched
> fresh-context reviewer, or the human — never the proposer. Independence grants DOWN bindingly and UP only through
> an actual pass; silence ≠ pass; contribution/paper promotion = human only.

### 5.0 Research TYPES — name the type FIRST, verify by type
> Full taxonomy: research-os `skills/prospect/references/research-types.md`. Type-blindness is the classic failure:
> novelty gates killing improvement work; gate pressure herding output toward evaluation certificates.

| Type | Value = | Verify | Characteristic failure |
|---|---|---|---|
| **Improvement 刷分** | measured Δ vs honestly-tuned baseline; idea novelty irrelevant | `/adversary` A+B. Occupancy = "has this EXACT change been measured here", never a veto | unfair baseline; occupancy-as-veto |
| **Evaluation 评估** | a DECISION that changes because of the measurement | name the changed decision | certificate-production (audit theater) |
| **Survey 综述** | a map that changes where people search + a mined problem list | ≥1 problem someone would drop their work to attack | summarizing instead of mining |
| **Novelty 新对象** | a reframe that explains old failures AND predicts new ones | differential prediction where it applies | cosmetic relabel |
| **Systems 系统** | end-to-end wall-clock/cost lever at equal quality | end-to-end, never proxy | proxy wins, e2e loses |
| **Negative 证伪** | a killed assumption the community builds on | scope honesty; structural = independent-only | strawman; scope inflation |
| **Theory 理论** | many phenomena → one mechanism + ≥1 NEW prediction | the prediction, tested | post-hoc unification |
| **Tooling 工具** | an experiment class others can now run — and DO | used in anger within one cycle | infra for its own sake |
| **Reproduction 复现** | trust recalibration on a load-bearing result | pre-stated deltas + sealed protocol | reproducing the peripheral |

**Type-drift is the canonical loop failure** (the programme pulse checks it): goal says design/improvement,
artifacts trend evaluation-shaped. Detect structurally — type the last 3–5 artifacts.

### 5.1 The discipline moments + the one invariant
> Most work never sees a gate: plumbing, exploration, tactical runs flow freely. Discipline binds at a few late
> moments. One question replaces any lane table: **"is this a claim leaving the loop?"** yes → `/adversary`; no → go.

| Moment | Command | What it does |
|---|---|---|
| **Before a claim-bearing run** | **`/prereg`** | Seal the contract: {HYPOTHESIS, LATENT-ROOT, MECHANISM, TYPE, METRIC, sealed SPLIT, ACCEPT/KILL-if, BRACKET, NEG-CONTROL, SEEDS ≥3, POWER/MDE, ONE-VAR…} in 10–20 lines via Arbor. Post-hoc edits void the run as evidence. Exploration is free — contract only what will be cited. |
| **At the CONFIRMATION boundary (late, opt-in)** | **`/prereg` CONFIRMATORY block** | Once a cheap probe shows the effect is likely real: statistical UNIT + valid paired TEST (McNemar/bootstrap/Wilcoxon/rliable-IQM) · seed-variance budget · BASELINE spec (what `/adversary` B will fight) · ALLOWED-CLAIM envelope · FAST ablations (necessity / negative-control / cost). Full ablations only for a venue claim — five ablations per candidate is the ceremony this avoids. |
| **After any run** | **`/exp-verify`** | 3-stage real-run check: no-mock → executed-on-real-data → anti-no-op (the intervention provably FIRED). A no-op FAILS even if the metric improved. VERIFIED = real run, not real effect. |
| **At the claim boundary ONLY** | **`/adversary`** | One independent TYPE-scoped pass: **A** Δ-reality (≥3 seeds mean±std, per-example regression, neg-control, sealed holdout) · **B** baseline fairness (make the OPPOSING baseline win — equal budget, paired stats) · **C** claim–evidence map (no artifact ⇒ hypothesis; claim ≤ contracted envelope) · **D** worth (toy? goalpost moved? decision named?). |

**THE ONE INVARIANT:** *a verdict that helps the proposer if gamed must never be granted by the proposer.*
Proposer self-administers DOWN only (`REFUTED` / `DOWNGRADED_TO_HYPOTHESIS` / `TOY` / kill / `scoped-negative`).
`CLAIM_STANDS` = independent substrate only (a failed pass is answered point-by-point, never re-rolled).
Contribution/paper promotion = human only; an AI `CLAIM_STANDS` is advisory input to that decision.

**Autonomy boundary:** MAY unilaterally — observe · prospect · forge · prereg · dispatch worktree executors · run
dev/sealed eval under frozen contracts · autopsy · update tree/RUNLOG · kill its own toys. MAY NOT — change the
success metric after seeing results · broaden scope · self-grant `CLAIM_STANDS` · promote to contribution. Tactical
uncertainty goes to the external brain first; the human is a last-resort escalation, not a per-cycle bottleneck.

**High-stakes reflexes** (fired only at committing moments, not per cycle): grade evidence before promoting/citing
(memory-grade evidence can't promote — live search first); before an irreversible step (benchmark/story/method/
big-run/public claim) prefer the cheap falsifier / a reversible substitute; at any external handoff run the
artifact-acceptance checklist (usable by another person; every number recomputed from its cited artifact).

### 5.2 The GENERATOR — /prospect · /forge · /autopsy
> Research quality is decided at problem-selection time; these commands are where taste acts GENERATIVELY.
> Foundations: `skills/forge/references/taste.md` + `schools.md` (14 schools) + `frames.md` (14 frames) +
> `taste-operators.md` (the operator bank machinery).

| Command | Fires | Core moves |
|---|---|---|
| **`/prospect`** | goal start · "no surprises" · region-close lateral · fresh corpus | Mine 0 atlas-read first, then the five mines (own-log anomalies FIRST · literature contradictions/silent assumptions/future-work graveyards · capability deltas · benchmark critique · transplant discipline). Latent-root compression → **Reconstruction** (reformulate the compressed root into ≥2 other disciplines' native abstractions; kill-gates apply at the claim boundary, never to a reframe at birth) → 3–7 ranked cards `{Q, TYPE, IDEATION-TAG, RECONSTRUCTION, WHY-NOW, STAKES, PROBE, SURPRISE}` + the frame/operator ledger. Discard gap-filling without WHY-EMPTY, no-stakes, gate-shaped problems. |
| **`/forge`** | one problem chosen | Load-bearing variable → atlas read + type-scoped occupancy (≤15 min, never a veto) + necessity gate for mechanism/novelty types → 3–5 candidates, one forced per axis (rival school · off-frame with DIFF-PREDICTION · rotated operator) + ORACLE-CEILING/TRIVIAL-FLOOR brackets → cards `{FAILURE-SIGNATURE, LATENT-ROOT, MECHANISM, MVE, KILL, BRACKET, COST, SURPRISE…}` → taste-rank + He-bar in generative mode → **REGENERATION RULE** (which failure promotes which candidate) → the external brain refines the SELECTED design by default (skip needs a written reason). |
| **`/autopsy`** | every null / kill / DOWN verdict | Boring-first triage (most negatives are bugs; fix, bank nothing) → mechanism-level why (which link broke) → DOWN-only scope grade (structural = independent-only) → **CONVERSION LAW: emit ≥1 of constraint / candidate / region-close** (none ⇒ incomplete) → `[ANOMALY]` + `[OPERATOR-CANDIDATE]` + `[ATLAS]` ledgers. Tree first, then RUNLOG, then backlog. |
| **programme pulse** (inside `/autopsy`) | after every 2nd `/autopsy` · stuck · before an expensive leg | ① type-drift ② surprise accounting (zero = farming process → force a generator move) ③ Lakatos health (core intact? heuristic still generating? predicting or absorbing?) ④ process budget (>20% sustained → ship a run) ⑤ frame+operator monoculture ⑥ reproduction-inertia (parity done ⇒ next mechanism must be a CONTRIBUTION candidate). Advisory: CONTINUE / REFRAME / LATERAL / STOP_AND_REPORT. |

**Four generative axes — schools (how to think) · types (what output) · frames (which mathematics) · operators
(which modeling move) — declared the ceiling; no fifth.** Frames: force ONE non-incumbent-frame candidate carrying a
`DIFF-PREDICTION` (none ⇒ relabeling ⇒ discard); a goal may inject a `FRAMES:` line. Operators: retrieve 1–3 from
the bank (`opus-pass/operators.md`) by failure-signature, force one candidate, rotate — never a sweep. The bank
grows via `/autopsy` `[OPERATOR-CANDIDATE]` under the corrosion gate (3 load-bearing fields + deletion test) + an
independent audit.

### 5.3 Arbor write-through — structure goes through the MCP, not md/json
Node fields = `hypothesis · status · result · insight · score · test_score · code_ref`; session meta =
`eval_cmd/eval_cmd_test · baseline/trunk_score · metric_direction`.

| Loop point | Arbor MCP (primary) | Sealed artifact (`code_ref` → it) |
|---|---|---|
| `/prospect` cards | `tree_add_node(hypothesis=card, status=pending)` | — |
| `/forge` choice + backlog | `tree_update_node(status=running)`; backlog + regeneration rule in insight | — |
| `/prereg` contract | `tree_set_meta(eval_cmd, eval_cmd_test, baseline_score, metric_direction)` | the contract file (timestamped) |
| dispatch isolation | `worktree_create` / `worktree_remove` | contract + exact inputs, no ambient dump |
| run + score | `eval_run(cmd, split, node_id)` | `/exp-verify` verdict = node insight |
| claim boundary | `tree_update_node(result, insight)` | `/adversary` per-check evidence |
| null / kill | `tree_prune(reason)` + conversion-law insight | — |
| merge / promote | `git_merge_branch` (no-regression gate) | human promotion record |
| narrative | `generate_report` | — |

**Rule:** if Arbor has a tool/field for it, use it — `eval_run` writes scores from actual command output, the
structural antidote to write-from-memory number drift (§4.8).

### 5.4 2-GPU parallelism + the BUILD-on-evidence gate
- **Pipeline (default).** A training run occupies the GPU(s); the main loop uses that window to design/search the
  next node — compute + cognition overlap. This is the productive form of the wait discipline.
- **Split** (two evidenced targets, each fits one GPU): GPU0=idea-1, GPU1=idea-2 as a parallel burst, then
  reconverge. Each split run = its own Arbor node + its own worktree; `CUDA_VISIBLE_DEVICES` per run.
- **The training gate = BUILD-on-evidence.** Earn a training run only on an evidenced target: a surveyed hard problem →
  matching real data → a cheap headroom eval shows the frozen base FAILS with Δ room. Kill if the base already
  solves it or it's a pure capability wall.
- Launch arithmetic (§4.9) per run: ETA-vs-cap · data-sufficiency · kill-checkpoint · resume-fail = STOP.

### 5.5 The Failure Atlas + Necessity Gate — depth memory
> The fix for "很会杀但不会越杀越懂": the loop had writes (kills, anomalies) but no compounding per-territory read.
> Full spec: research-os `skills/autopsy/references/failure-atlas.md`.
- **Breadth THEN depth.** Phase A breadth-scans candidate failure signatures (necessity-gate each) to MAP the atlas;
  Phase B commits to the top fracture and STAYS. Lateral is a legitimate mapping move; laterally fleeing before
  mapping is the bug. Abandon a domain ONLY on atlas-proven saturation + an epitaph.
- **Necessity gate (before ANY mechanism).** Design a mechanism only for a failure that survives frozen-base +
  tuned-prompting + retrieval + fair plain-LoRA + data-scale + seed + OOD split + metric-sanity + neg-control.
  Any of them closes it → `BENCHMARK_OCCUPIED` (not a mechanism failure).
- **The atlas file** `<campaign>/atlas/<territory>.md`: claim · evidence-pointer · grade(own-run|lit) ·
  what-it-re-prices; a region-close writes an EPITAPH (`dead because X; reopen if Y`). `/autopsy` writes;
  `/prospect` Mine 0 + `/forge` read first. Re-prices, never vetoes.
- **Enrichment:** GPT-5.6 browser finds/triages → download the arXiv PDF locally → `pdftotext` → subagent 精读 as
  reverse-inference ("what MOVE derives this paper?") returning atlas rows + operator rows. Output = rows, never
  "I read N papers". Browser triage alone is insufficient — local 精读 seals.

### 5.6 刷分-first high-throughput loop
> AI can't invent the harder problem (that comes from surveyed papers), but it CAN climb a defined benchmark — so
> improvement-type work is PRIMARY and the novelty/necessity machinery (§5.5) is the secondary track.
- **The insight:** in 刷分 the metric-GAP IS the failure signature — concrete, quantified, visible. Aim the taste
  arsenal (frames · operators · reframing · elegant modeling) at the score gap: a constrained, well-posed use of
  generation.
- **The fast OODA loop:** `run → score → 分数不够 → analyze WHY (which examples fail = the per-benchmark atlas) →
  aim the arsenal at the bottleneck → fix → re-run.` Method-source = the arXiv-精读 pipeline, not AI invention.
- **SOTA-first substrate gate:** a new direction starts with a bounded strong-baseline smoke — record recipe,
  missing pieces, ETA, first actual metric. Do not refute a known rung without its recipe.
- **Gates only at the claim boundary — never per-iteration.** `/adversary` fires only for "this Δ is a
  contribution" (big honest Δ vs a TUNED baseline, ≥3 seeds, paired). Keep workflow/meta <20% of effort.
- **CORAL** (`coral` CLI, installed) = an optional 刷分 accelerator: `coral-task-author` scaffolds repo+grader,
  `running-coral-experiments` launches/monitors, `coral-run-doctor` diagnoses. 2-GPU caveat: compute-bound attempts
  serialize, so expect code/method-edit parallelism, not full multi-island throughput. Never a dependency — the
  default loop is a Sonnet executor on the built harness.
- **Venue caveat:** an improvement claim competitive at Information Sciences / AAAI needs a BIG honest Δ where the
  incumbent genuinely fails — not "+0.5% by stacking 3 papers"; decision-centric evidence, never return-only.

## 6. Ideation layering + tree discipline

| Layer | Weight | Use when |
|---|---|---|
| **`/prospect` + `/forge`** (research-os) | HEAVY — the generator; may escalate to the external brain | DIRECTION-level: goal start, a new problem, a fork after a region-close |
| **Opus-propose + `tree_add_node`** | LIGHT — in-loop, single-engine | TACTICAL: the next node under an active candidate, a quick variant |

> Heuristic: changes the programme / needs the external brain → `/prospect`+`/forge`. "The next experiment under
> this candidate" → plain Opus-propose + `tree_add_node`. A routine tactical selection is Opus's own call inside the
> autonomy boundary; a consequential direction/thesis selection routes to an independent GPT-5.6 read.

**Tree-update checklist (every 验收, tree FIRST then RUNLOG):**
- [ ] `tree_update_node` the dispatched node — status (done/pruned/running) + result + insight (for a null, the
      conversion-law output IS the insight).
- [ ] New candidate → `tree_add_node` BEFORE dispatch · dead branch → `tree_prune` + reason.
- [ ] Node types = {idea, experiment, negative, programme}; a programme node only after a candidate survives its
      first claim boundary + human budget approval.
- [ ] New track/eval at INIT → `tree_set_meta` the eval contract (B_dev/B_test, metric, metric_direction).
- [ ] Direction/campaign CLOSE → close-out sweep: reconcile all descendant statuses; purge any number lacking an
      artifact before it can propagate (the phantom-number lesson, §4.8).
- [ ] THEN append the RUNLOG narrative.
