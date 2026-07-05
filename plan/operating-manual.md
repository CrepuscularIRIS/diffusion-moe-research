# Research Operating Manual

> The single "how we work" reference. Read at session start together with `plan/goal-directive.md`.
> This DISTILLS the operational content so `CLAUDE.md` can stay lean and just point here.
> Last updated: 2026-07-05 — **CURRENT SEED = Aerial VLN 刷分 (UAV vision-language navigation; OpenFly platform + AerialVLN benchmark)** (§0); MODE = 刷分-first HIGH-THROUGHPUT OODA (§5.7); research-os **v1.1** (6 cmds + Failure Atlas). §0 = live state only. **(Pre-2026-07-05 StarVLA / LIBERO-manipulation content below = SUPERSEDED history.)**
> **PATH NOTE:** `VLA/*` references throughout are **LOCAL working state (gitignored)** — present on this machine, NOT in a repo clone. They are intentional local pointers (campaign state is kept out of the repo by design), not tracked docs.

---

## 0. Current research state (read this first)
- **★★★ CURRENT SEED (2026-07-05, human) — Aerial VLN 刷分 (UAV vision-language navigation). THIS IS THE ANCHOR:**
  a cold `/goal` session runs the 刷分-first loop (§5.7) on the **OpenFly** platform (`/data/projects/VLA/aerial/`
  — LOCAL: code + 30G scenes + 29G lerobot + checkpoints, smoke-tested → **START HERE**) + the **AerialVLN**
  standardized benchmark (download AerialVLN / AerialVLN-S / AVDN, <1GB → `/data/huggingface/datasets/`). Anchor
  paper `VLA/paper/综述_Aerial_VLN.pdf`; inventory `VLA/aerial-vln-inventory-2026-07-05.md`; metrics SR / SPL / nDTW.
  首推方向 = viewpoint-robustness / long-horizon-instruction-decomposition (frozen-VLM + light adapter, ≤4h cap).
  **OUT-OF-DOMAIN: StarVLA (2604) manipulation · Orca (2606) — experiments STAY in Aerial VLN.**
  **⚠ The StarVLA / LIBERO / manipulation bullets BELOW in §0 are SUPERSEDED HISTORY (pre-pivot) — do NOT operate from them.**
  - **Platform (VERIFIED loads on our HW):** StarVLA policy-server + LIBERO-plus MuJoCo sim (two-process,
    `examples/LIBERO-plus/eval_files/` — `run_policy_server.sh` in `starvla` env + `eval_libero.sh` in
    `libero_plus` env); ckpt `.../Qwen2.5-VL-FAST-LIBERO-4in1/checkpoints/steps_30000_pytorch_model.pt` (8.1GB);
    ~2 min startup (torch.compile), ~9.2GB VRAM, binds a websocket port.
  - **All S-tier data READY ✅ (2026-07-04):** LIBERO clean 4 suites (`/data/datasets/LEROBOT_LIBERO_DATA/`) ·
    LIBERO-Para (5623 bddl + metrics) · LIBERO-Plus (9.5GB assets bundled in the repo clone) · base VLM
    Qwen2.5-VL-3B. All three runnable now; do NOT duplicate downloads (USER's session owns them).
  - **Baseline = the free atlas row (our EXACT ckpt):** Qwen2.5-VL-FAST LIBERO-Plus zero-shot total **48.9** —
    failure LOCALIZED to Camera **19.6** / Noise **27.4** / Robot **27.6** (near-random) vs Language 74.5 /
    Light 75.2 / BG 71.0 / Layout 62.7. For LIBERO-Para, measure the baseline directly (paper: 22–52pp drop,
    80–96% planning-level trajectory divergence). Reproduce on a SEALED subset before citing any Δ.
  - **Where the DEFENSIBLE Δ lives (taste filter):** Para/Language is fastest but MOST occupied by plain
    paraphrase-aug (highest necessity risk); the augmentation-resistant **Camera / Noise / Robot** axes are where
    a mechanism is most likely NECESSARY. GUARD (SpatiaLQA lesson, `/forge` SECONDARY + necessity gate): a
    *contribution* must BEAT a TUNED aug-LoRA baseline run FIRST — pure 刷分 (climb the number by any means)
    skips the gate.
  - **Eval-cost discipline (§5.7 throughput):** LIBERO-Plus = 10,030 tasks (MuJoCo rollouts, long). Inner OODA
    loop = SEALED stratified per-axis SUBSET (weighted to the 3 weak axes) + shard both GPUs + weak-axis SR
    proxy; the full 10,030 runs ONLY at the `/adversary` claim boundary.
- **CLOSED — do NOT revive / cross-contaminate** (narrative + full lessons in `VLA/RUNLOG.md` +
  `VLA/CAMPAIGN-CLOSEOUT-2026-07-03.md` + the research-os failure-atlas — NOT here): VLA-fusion / cross-stream
  (killed 2×, crux image-bridge NO-GAP, base ACS 0.997) · improvement-first QA (PRE-HAL / MathVista =
  tuned-incumbent *trap*; SpatiaLQA / VLDBench = frozen-base *wall*; SpatiaLQA Ledger-DAG 0.523 < plain-LoRA
  0.582 = KILLED). **Root lesson:** on an established frozen-VLM benchmark the model is too weak (wall) or a tuned
  incumbent already holds the headroom (trap) — the LIBERO OOD-robustness regime is the escape (clean base ~90%
  but COLLAPSES under perturbation = a transfer gap a mechanism can own; that's why the seed anchors there). The
  standing goal philosophy (AMBITION + VALUE BAR, do-not-ask-which-direction, progressive problemshift) lives in
  `plan/goal-directive.md`.
- **PAUSED (separate projects, do NOT cross-contaminate):** DSpark × speculative decoding (warm-start RSMH; the
  beyond-Markov head space is largely exhausted — `DSpark-analysis.md`, `plan/archive/dspark-deep-analysis-2026-07-01.md`) AND
  the entire dLLM/DiffusionGemma/LLaDA campaign (archived `plan/archive/`, Arbor tree 5.1-5.13 done/pruned).
  Both are SEPARATE, non-active projects.

## 1. Engine stack — the division of labor (Opus 4.8 · GPT-5.5 Pro · Codex hook)
> **One line — Pro generates · Opus operates · Codex checks · human sets taste.** GPT-5.5 Pro is the
> DEFAULT engine for the GENERATIVE acts (idea/problem generation in /prospect, approach+head DESIGN in
> /forge, failure→next-candidate in /autopsy) — a different model reaches the enrich-level reframe a local
> checklist misses; skipping Pro on a generative act needs a stated reason, and Pro is NOT used for
> tactical iteration. Opus OPERATES: routes, packages the Pro hand-off, runs the mechanical moves
> (/prereg, /exp-verify), TUNES what Pro designed, decides tactically, interprets, AND is the executor
> (subagents inherit the session model = Opus 4.8). The **Codex review hook** auto-audits every executor
> diff (DOWN-only). The human grants contribution promotion — most valuable EARLY (shaping problems at
> /prospect · /forge), not only at sign-off. Manual `/codex:rescue` is **RETIRED**.
>
> **★ GENERATIVE-ENGINE UPGRADE (2026-07-05) — the differentiated MoA advisor panel.** On HIGH-VALUE generative
> forks (mechanism design · direction selection · hard problem-finding), the generative act FANS OUT to a
> 5-advisor panel — Gemini 3.1 Pro (`agy`) · GPT-5.5 (`codex`) · DeepSeek V4 Pro · MiMo V2.5 Pro (OpenCode gw) ·
> Opus 4.6 (`agy`) — each given a DIFFERENTIATED prior (rotated operator + frame + school + structured dropout =
> the 前面路由 router); **Opus 4.8 reconciles** (consensus / conflict / unique-insight / blind-spot = 后面验收).
> Scripts `moa/moa_ask.sh` + `moa/moa_panel.sh --per-lane`; protocol `moa/router-protocol.md`; design
> `plan/moa-advisor-panel-design-2026-07-04.md`. **TIERED** — routine 刷分 = solo Opus; medium = Opus + 1; the
> full panel is for the FORKS, not every iteration (it costs ~1 min + N models). **Sonnet 4.6 = the DEVELOPMENT
> executor** (native `Agent` model:"sonnet") + Opus 4.8, GPT-5.5 Codex hook reviews — NOT a research advisor.

| Engine | How to invoke | Role |
|---|---|---|
| **Opus 4.8 (me)** | direct (main loop) | **PI / decision-owner / interpreter.** OBSERVE, `/prospect`, `/forge`, SELECT/DECIDE, assemble+package the taste-SHAPED Pro hand-off, `/autopsy` (carries the programme pulse, ex-`/compass`), update tree/RUNLOG. **Never self-grants `CLAIM_STANDS`.** Prefer Opus high; reserve xhigh for the hardest judgment. |
| **Opus 4.8 executor subagents** | `Agent` (+ `isolation: "worktree"` when mutating files); inherits session model | **ALL implementation / experiment plumbing / verification runs / repo exploration / debug** (effort high default; xhigh for a hard bug). Returns changed-files + commands + test-results + artifact-paths + known-risks. Does NOT judge worth, grant a PASS, touch a sealed holdout, or rewrite the thesis. |
| **GPT-5.5 Pro** | Playwright `browser_*`; model button = **`Pro 扩展` (the ONLY tier — never switch)** | **External brain — DESIGNS each new candidate architecture by DEFAULT** (the `/forge` step-7 flip: Pro designs, Opus only tunes; skipping Pro needs a written reason — "optional" Pro = never-used Pro = the better design path thrown away). Also: prior-art / occupancy reads, contested `/adversary` passes, AC meta-review. Compact Opus-packaged hand-off (never a repo dump). 1h+; **poll 15 min**; **new chat per query**; **keep Playwright alive — never close/restart**. |
| **Codex review hook** | AUTOMATIC (SubagentStop; `CODEX_REVIEW_GATE_GLOBAL=true`) | **Independent adversarial review of EVERY executor subagent's diff** — SPARK inline (`gpt-5.3-codex-spark`, fast triage) + DEEP background (`gpt-5.5 xhigh`, read-only), advisory / non-blocking, surfaced via `systemMessage`. An uncurated, un-re-rollable independent substrate. A finding = a **binding DOWN** verdict; it **never grants UP** (silence ≠ pass). |
| **Human** | HARD-BLOCK escalation + EARLY problem-shaping | Contribution / paper / "architecture-advantage" promotion; critic↔proposer deadlock; flagship go/no-go; writes the goals. RARE at the back of the loop — most valuable at the front. |

> **Browser division of labor (2026-07-05):** **playwright-extension** (real Chrome, bypasses Cloudflare, holds
> the login session) → **ChatGPT / Gemini web** (Pro 扩展, DeepResearch) = the DEEP-design / DeepResearch lane.
> **agent-browser** (its own **HEADLESS** Chrome, concurrent, no user interaction; login/profile = pass
> `session` + `extraArgs: ["--profile","Default"]` at the tool call, NOT a second MCP) → **arXiv fetch · blogs ·
> GitHub · docs · concurrent public reads** = the atlas-enrichment legwork. Fast model Q&A stays on the
> **codex / agy CLIs** (not a browser). The two **do NOT conflict** (separate Chromes; the extension's one-time
> "Allow" persists). Playwright is NOT retired — it keeps the real-browser / anti-bot niche.

## 2. The Arbor MCP — what we keep, what we dropped
Arbor offers two layers; we use only the first.
1. **MCP TOOL layer (KEEP — deterministic, immediately usable):** `tree_view` · `tree_add_node` ·
   `tree_update_node` · `tree_prune` · `tree_set_meta` · `worktree_create`/`worktree_remove` · `eval_run` ·
   `git_merge_branch` · `generate_report` · `open_dashboard`.
2. **`arbor-cycle` / `/arbor-research-agent` SKILL loop — DEPRECATED** (goal mode works better; user decision).
   Do not run it. The init scaffolding it left (`QUEUE.md`, `cycle-state.json`, `BLOCKED.md`, `review_debt.md`)
   is **vestigial** — ignore/archive.
- **Policy:** GOAL mode is the driver. The **Arbor MCP idea tree is the canonical research STRUCTURE**
  (`.arbor/sessions/<run>/.coordinator/idea_tree.json`). Maintain it at **every 验收 (tree FIRST,
  then RUNLOG)**. Use `worktree_create`/`eval_run`/`git_merge_branch`/`generate_report` opportunistically.
- **★ GOAL = a CONTINUOUS loop, not one stage.** `/prospect` → `/forge` → `/prereg` *(+ CONFIRMATORY block = ex-`/rigor`, once a probe shows the effect is likely real)* → run → `/exp-verify` →
  (claim → `/adversary` · null → `/autopsy`) → loop; the `/autopsy` **programme pulse** (ex-`/compass`) runs **after every 2nd `/autopsy`** (the countable
  trigger — "every 3–5 cycles" never fired in the DSpark campaign; §5.2). **★ THE ANTI-EXHAUSTION
  RULE (why past campaigns "kept stopping"): the backlog is ALIVE, never a menu.** Every `/autopsy` MUST
  emit its conversion-law output (a constraint, a new/reshaped candidate, or an explicit region-close that
  triggers a lateral `/prospect`). A null result is a per-cycle WIN **only if it generated something** —
  banking a negative that reshapes nothing is an incomplete autopsy, and halting after banking is the #1
  loop bug. **The loop picks its pivots itself by taste and NEVER stops to ask the user which direction.**
  A contribution/paper/"publishable" claim is **NOT** an autonomous loop outcome — it HARD-BLOCKS to
  human/external (§5.1); the loop only banks evidence and advances. Never end the session at "shortlist
  ready" or "one experiment done"; continue to the next live candidate. **Concrete caps (bounded
  autonomy):** ≤12 dispatched cycles/session; ≤3 consecutive inconclusive leads → stop+report; each experiment
  pre-declares a wall-clock budget (≤3h dev / ≤12h sealed), `kill -9` on overrun OR >30min zero-output.
  Otherwise the RUN stops ONLY when: a claim clears `/adversary` and reaches the promotion gate (→
  human/external); OR the `/autopsy` programme pulse says STOP_AND_REPORT (programme degenerated / caps); OR genuinely blocked
  (needs user). **A live backlog candidate means the run is NOT done — pivot to it.**
  **Safe background (ZERO orphans):** GPU concurrency is PLATFORM-SCOPED, re-derived at campaign
  start from the current model's memory footprint (26B-class → ONE job total; 4B/8B-class → one job
  PER GPU, pair candidate+control across the two 4090Ds — an idle second GPU during a training
  campaign is a bug, see §4 lesson 10) — `nvidia-smi` BEFORE dispatch, QUEUE don't collide. **EVERY long job MUST be TRACKED — no
  fire-and-forget:** prefer harness `run_in_background` (auto re-invokes on completion — ONE clean signal, no polling); a `setsid`-detached
  job is allowed ONLY if it writes a PID-file AND a RUNLOG registry line (cmd / PID / **cwd** / **start-time** /
  budget) AND arms a **`Monitor`** (a condition-watch → ONE clean notification when the job exits) — detach without all three is FORBIDDEN.
  **★ WAIT / PARK DISCIPLINE (2026-07-03 — supersedes; two failure modes closed). THE WAIT IS NOT THE
  DELIVERABLE — the VERDICT is.** An agent that ends a turn having only *armed a monitor* has done zero work;
  the terminal action is ALWAYS **read the artifact → produce the verdict.**
  - **Match the wait to the DURATION.** **MINUTES-long** (an inference kill-probe, a ~minutes verifier head) →
    run **SYNCHRONOUSLY in ONE turn**: foreground Bash, or `run_in_background` + a bounded read-loop, then READ
    the result and emit the verdict THIS turn. Do NOT arm a Monitor + end the turn for a minutes-long job — that
    adds a full turn-cycle of latency and invites the re-arm stall. **HOURS-long** (real training) → arm a
    **`Monitor`** + end the turn (you cannot block for hours).
  - **Consume → verdict, NEVER re-arm.** When the signal fires, the NEXT action is READ + DECIDE. Re-arming
    another monitor / re-checking-and-waiting is the **STALL** — the `arm-monitor → end-turn → notify → re-arm`
    loop that once burned ~220k tokens / 2h with no verdict.
  - **Do NOT dispatch a subagent for a minutes-long probe** — run it inline; a subagent's turn/monitor/notify
    cycle is heavier than the probe itself, and re-delegating a stuck executor compounds it.
  - **Circuit-breaker.** A wait that fires N times / runs past its ETA with no verdict artifact → STOP the wait,
    check **GROUND TRUTH** directly (`ps`, read the artifact file); do NOT re-arm or re-delegate.
  - **NEVER a `ScheduleWakeup` poll** (the earlier churn — a timed wakeup re-fires under an active Stop-hook).
    Browser→Pro waits → quiet **15-min** checks (never busy-poll). To PARK between steps → arm a `Monitor` and
    stop — but the run itself must still terminate in a verdict, not an infinite park.
  **★ THE SINGLE OWNERSHIP TEST (live-checkable; goal-directive + §4 lesson #5 reference THIS):** a process is
  **PROVABLY OURS** iff *(live) its cwd is under the project / `.claude/worktrees/` AND its cmd matches our job
  patterns*. A registry/PID-file entry only says WHICH PID to look at — **it NEVER proves ownership and NEVER
  authorizes a kill by itself.** A process owned by another project/user or with cwd OUTSIDE the project is the
  USER's own concurrent work (co-tenant, e.g. `JasonF/openpi` pi0, `gaussian-splatting` 3dgs; parent=systemd,
  cwd outside huggingface) → busy-GPU, QUEUE/wait, NEVER kill. **Unsure → WAIT, do not kill.**
  **★ PID-REUSE GUARD — a recorded PID NEVER authorizes a kill.** PIDs recycle: a stale PID-file may now point
  at an unrelated process (even a co-tenant). Before ANY `kill`, RE-VERIFY the LIVE process at that PID against
  the registry — its **cmd + cwd + start-time must ALL match** — AND it must pass the ownership test above. On
  any mismatch → the PID was recycled → do NOT kill; just clear the stale registry line.
  **Kill = ownership AND live re-verify AND a trigger:** (a) ON RESUME orphan-sweep — reconcile registry vs
  `ps`/`nvidia-smi`; adopt tracked jobs; kill only if owned + re-verified + stale-per-registry. (b) Overrun —
  kill our job (owned + re-verified) when it exceeds budget / >30min zero-output; clear the registry line.

## 3. Document conventions (the anti-drift contract)
| Artifact | Role | Cadence |
|---|---|---|
| `.claude/CLAUDE.md` | LEAN config: identity, engine routing, keys, hard rules, POINTERS | rarely |
| `plan/README.md` | **one-screen flow map** (the v0.5 loop) + plan/ doc index — START HERE | when structure changes |
| `plan/operating-manual.md` (this) | how-we-work reference (engines, Arbor, conventions, lessons, science kernel, §5 types+commands) | when process changes |
| `plan/goal-directive.md` | the exact `/goal` input (written by the user) | when goal changes |
| **research-os plugin** (`/home/lingxufeng/cli/research-os`) | the 7 commands + skills + `taste.md` + `research-types.md` — the canonical prompt layer | when the method changes |
| `plan/archive/research-operating-system.md` | HISTORY: the v0.4 gate design + its diagnosis — superseded by research-os v0.5 | archive-grade reference |
| `plan/archive/dspark-deep-analysis-2026-07-01.md` | DSpark technical breakdown + occupancy scan | when occupancy changes |
| `DSpark-analysis.md` | DSpark core ideas + transferable concepts | reference |
| `enrich.md` | the methodology schools + the MOS aesthetic (extended by the plugin's `taste.md`) | reference |
| **Arbor MCP tree** (`tree_view`) | **canonical STRUCTURE** — branches / status / result / insight / prune | **EVERY 验收, FIRST** |
| `plan/archive/` | CLOSED dLLM campaign + all prior experiment docs (do NOT load for DSpark work) | — |
> **The #1 process bug to never repeat:** updating the RUNLOG but not the tree → the tree goes stale and the
> research looks linear. Tree first, every cycle.

## 4. Hard-won lessons
1. **Substrate integrity.** Verify model/checkpoint integrity before trusting any metric. Ground-truth with a
   trivial task before committing compute. (Learned from a corrupted shard in the dLLM campaign — `plan/archive/`.)
2. **Metric validity.** Proxy metrics (loss, teacher-forced scores) often do NOT predict task quality. → Use
   **end-to-end generation / verifier metrics** as the primary signal.
3. **Failure-mode first.** Profile WHERE the model fails (generation-based) before designing a method.
4. **Tree discipline** (see §3). **Independent review** is mandatory (the Codex hook audits every executor
   diff); the proposer never self-grants `CLAIM_STANDS` — DOWN verdicts only.
5. Kill hung/overrunning jobs immediately — but ONLY a job that passes the §2 **ownership test** (live cwd
   under the project / `.claude/worktrees/` AND cmd matches our job patterns) AND the §2 **PID-reuse re-verify**
   (the live cmd + cwd + start-time all match the registry). **A recorded PID alone NEVER authorizes a kill**
   (PIDs recycle). **NEVER kill the user's concurrent co-tenant work** (e.g. `JasonF/openpi` pi0,
   `gaussian-splatting` 3dgs; cwd outside huggingface, parent=systemd) — when ownership is unsure, WAIT, don't
   kill. Measure-first (timing probe before heavy compute); only one 26B fits on the 2×4090 (serialize GPU
   jobs; `nvidia-smi` before dispatch); keep Playwright alive; **never modify sealed eval/test/baselines**.
6. **Subagent-dispatch discipline (perf — 2026-06-30, `subagent-dispatch-slowness` memory).** Heavy
   subagent-dense work is abnormally slow: per-turn latency scales with (context size × concurrency). →
   **Do small/clear tasks yourself** (a few-min direct edit beats a 30–50 min executor); **leaner prompts /
   less context per agent**; **serialize heavy agents — never 3–4 concurrent Opus subagents** (they
   rate-limit each other); **serialize heavy executors** (Sonnet 5 retired as unstable; executors now Opus 4.8). **The manual-`/codex:rescue`
   zombie-leak is RESOLVED — manual rescue is retired; the single managed Codex review hook (one dispatch per
   subagent, reaped at 30 min, registry-capped) replaces the leaky fan-outs.** GPU idle ≠ progress lost.
7. **The v0.4 framework lessons (2026-07-01 diagnosis — why the gates were rebuilt).** (a) Filters don't
   create value — problem selection does; (b) a gate-heavy system selects for gateable work → eval/certificate
   drift; (c) novelty gates must never judge improvement (刷分) work — occupancy is a cost signal, not a veto;
   (d) candidate MENUS exhaust — backlogs must regenerate from failures; (e) progress tokens are farmable by
   orderly retreat — count SURPRISES (plan-changes) instead; (f) process work is never the deliverable
   (>20% sustained = compass flag).
8. **★ ARTIFACT-FIDELITY (2026-07-02, DSpark archive audit — the most serious incident to date).** Every
   number in a shipped/banked document (report, README, tree result, memory) is READ FROM ITS ARTIFACT
   FILE at writing time, with the artifact path cited next to the table — NEVER recalled from working
   memory. The DSpark public archive shipped back-computed baselines, a wrong probe-model name, a
   cross-contaminated TV figure, and a "94% E[τ] ceiling" whose probe was never run (all corrected
   2026-07-02). A planned-but-unexecuted probe's numbers are NOT results. **Any push to a public remote
   REQUIRES `/artifact-acceptance` first, and its checklist includes: recompute each number from its
   cited source file — mismatch = HOLD.** (Full autopsy: `plan/archive/retrospective-workflow-audit-2026-07-02.md`.)
9. **★ LAUNCH ARITHMETIC + CHEAP-SIGNAL LADDER (2026-07-02).** Before ANY training launch, inside the
   `/prereg` (or, for exploratory runs, a 3-line note): (a) measured sec/step × total steps = ETA — ETA
   over the §2 cap (≤3h dev / ≤12h sealed) ⇒ redesign, never launch; (b) data-sufficiency ratio vs the
   reference recipe (4.5K vs DSpark's ~500K = 100× short — one division would have predicted the
   from-scratch failure); (c) a declared KILL-CHECKPOINT {step, threshold, action=KILL} — a checkpoint
   eval below threshold kills the run, and a RESUME FAILURE IS A STOP, never a silent restart-from-0;
   **ENFORCED, not declared: at launch ARM A MONITOR on the run log** (`grep -E` covering progress ·
   kill-threshold cross · `Traceback|resume-failed|OOM|Killed`) so the kill-checkpoint fires the moment it
   trips — even after attention has moved on (the DSpark step-500 signal was ignored because nothing was
   watching). Agent-armed per-run = zero conflict with the global hook stack; NO blocking PreToolUse hook.
   Design + the >30-min launch ritual: `plan/archive/workflow-enforcement-design-2026-07-02.md`.
   (d) never retrain what a released checkpoint already provides (the vanilla-retrain waste). LADDER:
   for head/method work the forge KILL experiment defaults to an inference-time replay / oracle probe
   when one exists — no training run before its oracle-replay upper bound is measured (the skipped
   Probe C would have sized the RSMH prize at zero training cost).
10. **GPU throughput defaults (2026-07-02).** Generation-heavy steps (data regen, sampling evals) use
   vLLM / batched generation, never unbatched HF `.generate()` (observed 0.1 samples/s, a ~20-50×
   waste); measure samples/s in the first minute and abort if ETA > budget. Small-model campaigns keep
   BOTH GPUs busy (candidate + control / next candidate in parallel).

## 5. Science protocol (the kernel) + research-os v1.0
Falsify-before-build (ship the kill-experiment WITH the idea) · score-up ≠ mechanism (require negative control
+ locality) · eval/test/baseline are a **sealed layer, never changed mid-run** · one variable per probe ·
isolation: **generator ≠ executor ≠ critic** (Opus generates/selects; executor subagents run in worktrees; the
Codex hook audits every diff; Pro designs/arbitrates) · **experiment has absolute veto over elegance** · every
claim-bearing run pre-declares its contract (`/prereg`) · when evidence contradicts the direction, **redesign
the program**, don't defend it. A negative result is a SUCCESS **iff its autopsy generated something**.

> **★ SUBSTRATE NOTE (applies to ALL of §5).** An "INDEPENDENT substrate" = the **automatic Codex review
> hook** (SubagentStop, advisory, uncurated, un-re-rollable), a dispatched fresh-context reviewer, or
> **GPT-5.5 Pro** — never the proposer. Independence grants DOWN bindingly and UP only through an actual
> pass (`CLAIM_STANDS`); **silence ≠ pass**; contribution/paper promotion = human only.

### 5.0 Research TYPES — name the type FIRST, verify by type
> Full taxonomy: research-os `skills/prospect/references/research-types.md`. Schools (enrich.md) = how to
> think; TYPES = what kind of output + how it is valued + verified. The v0.4 bug was type-blindness:
> novelty gates killed improvement work; gate pressure herded output toward evaluation certificates.

| Type | Value = | Verify | Characteristic failure |
|---|---|---|---|
| **Improvement 刷分/改进** | measured Δ vs honestly-tuned baseline; idea novelty IRRELEVANT | `/adversary` A+B (Δ-reality + baseline fairness). Occupancy = "has this EXACT change been measured here", never "does anyone work here" | unfair baseline; occupancy-as-veto |
| **Evaluation 评估** | a DECISION that changes because of the measurement | name the changed decision — no decision-change = certificate | certificate-production (audit theater) — the loop's most seductive failure |
| **Survey 综述** | a map that changes where people search + a mined PROBLEM LIST (surveys are a `/prospect` mine, not a reading assignment) | ≥1 problem someone would drop their work to attack | summarizing instead of mining |
| **Novelty 新对象** | a reframe that explains old failures AND predicts new ones (enrich MOS) | differential prediction where it applies (optional `/prereg` DPC block) | cosmetic relabel |
| **Systems 系统** | end-to-end wall-clock/cost lever at equal quality | end-to-end, never proxy | proxy wins, e2e loses |
| **Negative 证伪** | a killed assumption the community builds on | scope honesty; structural = independent-only | strawman; scope inflation |
| **Theory 理论** | many phenomena → one mechanism + ≥1 NEW prediction | the prediction, tested | post-hoc unification |
| **Tooling 工具** | an experiment class others can now run — and DO | used in anger within one cycle | infra for its own sake (v0.4's own disease) |
| **Reproduction 复现** | trust recalibration on a LOAD-BEARING result | pre-stated deltas + sealed protocol | reproducing the peripheral |

**Type-drift is the canonical loop failure** (the `/autopsy` programme pulse's type-drift check): goal says design/improvement, artifacts
trend evaluation-shaped (certificates/audits/probes). Detect structurally — type the last 3–5 artifacts.

### 5.1 The discipline moments + the one invariant (the filter, collapsed)
> Most work never sees a gate: plumbing, exploration, tactical runs, and cheap size-first probes flow
> freely. Discipline binds at a few late moments. One question replaces the old lane table: **"is this a
> claim leaving the loop?"** yes → `/adversary`; no → just go.

| Moment | Command | What it does |
|---|---|---|
| **At the CONFIRMATION boundary (LATE, opt-in)** | **`/prereg` CONFIRMATORY block** (ex-`/rigor`, folded v1.0) | ONCE a cheap probe shows the effect is likely real (NOT during ideation/exploration/size-first), the `/prereg` card adds its CONFIRMATORY block — statistical UNIT · valid paired TEST by data type (McNemar/bootstrap/Wilcoxon/rliable-IQM) · SEED-variance budget · required BASELINE spec (what `/adversary` B will fight) · ALLOWED-CLAIM envelope · **FAST-mode ablations = the 3 cheap catchers (necessity/negative-control/cost)**; FULL (sufficiency/stress/breakdown) only for a venue claim. Proposer-side DOWN-only. **Efficiency-first — running 5 ablations per candidate is the ceremony this avoids.** |
| **Before a claim-bearing run** | **`/prereg`** | SEAL the contract (base fields + the CONFIRMATORY block above): {HYPOTHESIS, MECHANISM, TYPE, METRIC, sealed SPLIT, ACCEPT-if, KILL-if, NEG-CONTROL, SEEDS ≥3, ONE-VAR} in 10–20 lines, via Arbor. Post-hoc edits void the run as evidence. **Exploration is free** — contract only what will be cited. Optional DPC block for novelty claims. |
| **After any run** | **`/exp-verify`** | 3-stage real-run check: no-mock → executed-on-real-data → **anti-no-op** (the intervention provably FIRED). A no-op FAILS even if the metric improved. VERIFIED = real run, not real effect. |
| **At the claim boundary ONLY** | **`/adversary`** | ONE independent pass, TYPE-scoped: **A** Δ-reality (≥3 seeds mean±std, per-example regression, neg-control, sealed holdout) · **B** baseline fairness (make the OPPOSING baseline win — equal budget, paired stats 5×2CV/McNemar/DeLong) · **C** claim–evidence map (no artifact ⇒ auto-downgrade to hypothesis; new-metric-as-evidence GUILTY until it corrects a misleading eval; structural-negative needs the 3-part gate) · **D** worth check (toy? goalpost-moved? He-bar graded TYPE-relative; eval claims must name the changed decision). |

**THE ONE INVARIANT (unchanged from v0.4 — the piece that was correct):** *a verdict that helps the
proposer if gamed must never be granted by the proposer.* Proposer self-administers **DOWN only**
(`REFUTED` / `DOWNGRADED_TO_HYPOTHESIS` / `TOY` / kill / `scoped-negative`). **`CLAIM_STANDS` = independent
substrate only** (fresh uncurated context; a failed pass is ANSWERED point-by-point, never re-rolled).
**Contribution / paper promotion = human only**; an AI `CLAIM_STANDS` is advisory input to that decision.

**Autonomy boundary** (unchanged): MAY unilaterally — observe · prospect · forge · prereg · dispatch
worktree executors · run dev/sealed eval under frozen contracts · autopsy · update tree/RUNLOG · kill its
own toys. MAY NOT — change the success metric after seeing results · broaden scope · self-grant
`CLAIM_STANDS` · promote to contribution. The human is a RARE escalation, not a per-cycle bottleneck.

### 5.2 The GENERATOR — /prospect · /forge · /autopsy (carries the programme pulse, ex-/compass) — the enrich layer, operationalized
> This is what v0.4 lacked: of 10 gates, zero generated. Research quality is decided at problem-selection
> time; these commands are where taste acts GENERATIVELY (ranking and shaping), not as a filter.
> Foundations: research-os `skills/forge/references/taste.md` (the taste model — extends enrich.md) +
> `references/schools.md` (the 14-school palette + the 10-question generator).

| Command | Fires | What it does |
|---|---|---|
| **`/prospect`** | goal start · compass "no surprises" · region-close lateral · any fresh corpus | Hunt problems through the FIVE MINES: ① literature/survey 综述 (contradictions between papers · silently-shared assumptions · future-work graveyards · missing head-to-heads · stale numbers predating a capability shift) ② own logs (anomalies, seed variance, baseline misbehavior — the cheapest original problems) ③ capability deltas ("X was designed under constraint C; C just disappeared") ④ benchmark critique ⑤ cross-domain transplants (transplant the precondition, not the buzzword). Output: 3–7 ranked problem cards `{Q, TYPE, WHY-NOW, STAKES, PROBE, SURPRISE}`. Discard: gap-filling without a WHY-EMPTY answer; no-stakes problems; gate-shaped (easy-to-verify) problems. |
| **`/forge`** | one problem chosen | Name the load-bearing variable → type-scoped occupancy re-pricing (≤15 min, NEVER a veto) → generate 3–5 candidates via the schools palette (**+1 rival school, always**; the MOS move is ONE move, used when the failure signature smells like a wrong object) → each card `{MECHANISM one-sentence-why, KILL cheapest-falsifier, COST, SURPRISE}` → taste-rank → He-bar in GENERATIVE mode ("what would make this beautiful?" — 5 real min simplifying) → **the REGENERATION RULE** (which failure promotes which candidate — the anti-menu clause) → **route the candidate DESIGN to Pro by DEFAULT** (Pro designs the architecture, Opus only tunes; skip only for tactical tuning of an already-Pro-designed arch, with a written reason — the fix for "the loop never uses Pro though Pro is better"). |
| **`/autopsy`** | every null / kill / DOWN verdict | Boring-first (bug/data/config — most negatives are bugs; fix, bank nothing) → mechanism-level why (which link of the MECHANISM sentence broke) → DOWN-only scope grade (structural = independent-only) → **THE CONVERSION LAW: emit ≥1 of (a) a CONSTRAINT (re-prices the backlog), (b) a CANDIDATE (run the regeneration rule; 10-question the RESULT), (c) a REGION-CLOSE (→ lateral `/prospect`). None ⇒ the autopsy is incomplete.** Tree FIRST, then RUNLOG, then backlog update. |
| **`/autopsy` programme pulse** (ex-`/compass`, folded v1.0) | **after every 2nd `/autopsy`** (a countable trigger — "every 3–5 cycles" never fired in the DSpark campaign) · stuck · before an expensive leg | ① TYPE-DRIFT (type the last 3–5 artifacts vs the goal's declared type — the eval-drift detector; on flag, name the next ON-type artifact) ② SURPRISE ACCOUNTING (which observation changed the plan? zero = farming process → force a generator move) ③ PROGRAMME HEALTH (Lakatos as questions: hard core intact? heuristic still generating? predicting or absorbing?) ④ PROCESS BUDGET (workflow >20% sustained → ship a run). Verdict: CONTINUE / REFRAME / LATERAL / STOP_AND_REPORT — advisory; redirects, never blocks. |

> **Two generative axes added to `/forge` since the table above (v0.7 + v0.8) — both are prompt-allocation,
> no new commands.** ③ **frames** (v0.7, `references/frames.md`): `/forge` step 3′ forces ONE non-incumbent
> mathematical-frame candidate carrying a `DIFF-PREDICTION` (no differential ⇒ relabeling ⇒ discard) — the
> fix for mathematical monoculture; a goal may inject a `FRAMES:` line. ④ **operators** (v0.8,
> `references/taste-operators.md`): step 3‴ forces ONE *retrieved+rotated* taste-bank operator candidate (a
> reusable modeling-object-SHIFT move) — retrieve 1–3 by failure-signature, never a sweep. The bank is
> project-side markdown (`opus-pass/operators.md`, the ★ generation-test survivors); it grows via `/autopsy`
> `[OPERATOR-CANDIDATE]` under the corrosion gate (3 load-bearing fields + deletion test) + an INDEPENDENT
> audit (never self-granted); GPT-5.5 Pro deep-reads the operator's source papers just-in-time before
> `/prereg`. `/prospect` retrieves operators as a mining prior + prints a frame-and-operator ledger;
> the `/autopsy` pulse's check 5 flags frame- AND operator-monoculture. **Four axes: schools · types · frames ·
> operators — the ceiling.**

**The loop:** `/prospect` → `/forge` → `/prereg` *(+ CONFIRMATORY block = ex-`/rigor`; big/committing run? cheap falsifier first — the folded irreversible-decision reflex)* → run → `/exp-verify` → (claim → `/adversary` → human if contribution · null → `/autopsy` →
back into the backlog) · the `/autopsy` **programme pulse** (ex-`/compass`) runs **after every 2nd `/autopsy`** (§5.2). The v1.0 folds of the old Layer-2 (§5.4): epistemic-calibration = the one invariant's memory-is-not-evidence corollary; irreversible-decision = the cheap-falsifier-first reflex; artifact-acceptance = the external-handoff checklist.

### 5.3 ★ ARBOR IS THE SUBSTRATE — write STRUCTURE through the MCP, not md/json
> **Arbor MCP is the canonical store and the execution substrate.** Every command PERSISTS its structural
> output through Arbor; md/json is reduced to the few sealed contracts a fixed-field node cannot hold.
> The tree is the source of truth; RUNLOG is secondary narrative (or `generate_report`).

Arbor node fields = `hypothesis · status · result · insight · score · test_score · code_ref`; session meta =
`eval_cmd/eval_cmd_test · baseline/trunk_score · metric_direction`. The write-through map:

| Loop point | Arbor MCP (PRIMARY) | sealed artifact (`node.code_ref` → it) |
|---|---|---|
| `/prospect` cards | `tree_add_node(hypothesis=card, status=pending)` | — |
| `/forge` choice + backlog | `tree_update_node(status=in_progress)`; backlog + regeneration rule in insight | — |
| `/prereg` contract | `tree_set_meta(eval_cmd, eval_cmd_test, baseline_score, metric_direction)` | the 10-field contract file (timestamped) |
| DISPATCH isolation | `worktree_create` / `worktree_remove` | the contract + exact inputs (no ambient dump) |
| run + score | **`eval_run(cmd, split=dev\|test, node_id, set_meta)`** | `/exp-verify` verdict = node insight |
| claim boundary | `tree_update_node(result, insight)` | `/adversary` per-check evidence |
| null / kill | `tree_prune(reason)` + `tree_update_node(insight=conversion-law output)` | — |
| merge / promote | **`git_merge_branch`** (already a no-regression gate) | human promotion record |
| programme pulse | append to programme node insight | `/autopsy` pulse verdict paragraph (ex-`/compass`) |
| the narrative | `generate_report` | — |

**Rule:** if Arbor has a tool/field for it, USE IT (don't re-implement in md/json).

### 5.4 Layer-2 reflexes (FOLDED into v1.0 — kept as reference for WHEN the reflexes apply, NOT as separate commands: epistemic-calibration → the one invariant's memory-is-not-evidence corollary; irreversible-decision → cheap-falsifier-first; artifact-acceptance → the external-handoff checklist)
> Three wrap skills around the core loop, fired ONLY at high-stakes moments (never every cycle). Each adds a
> decision boundary the core 7 do not gate; none duplicates them. Distilled from a Fable 5 methodology audit
> (archived: `plan/archive/fable5-methodology-extraction-2026-07-01/`).

| Command | Fires | Boundary it adds |
|---|---|---|
| **`/epistemic-calibration`** | before promoting/citing/contracting a claim, or spending compute/reputation | grade evidence **A–E**: A/B decide · C HOLD · D (memory/taste) can't-promote · E escalate. The novelty-by-memory + overclaiming guard; a grade-D "this is novel" → HOLD + live search, never a contracted claim. |
| **`/irreversible-decision-audit`** | before a committing step (benchmark/story/method/big-run/public-claim) | detect the lock (narrative/benchmark/method/evidence/compute/reputation/product) → **PROCEED/DELAY/RESCOPE/BLOCK** + a reversible substitute. This is the DETECTOR for the "external/irreversible commitment → human" boundary; DSpark default = a full run before the ceiling-probe → DELAY/BLOCK. |
| **`/artifact-acceptance`** | at a share/reuse/handoff of a deliverable (report/README/demo/skill) | is it usable by another person → **SHIP/REVISE/HOLD/KILL** (distinct from `/adversary`'s claim-truth). External SHIP still routes through the human promotion gate. |

Same invariant: proposer self-administers only DOWN verdicts; escalation → independent substrate (contested)
or human (external). The audit's `agent-governance` was NOT added as a skill (it IS the invariant + the
engine division); its two sharp bits — the **cold-start review packet** and the **agreement-illusion guard**
(stance-separated, REFUTE-prompted review) — are folded into `/adversary`.

### 5.5 ★ 2-GPU parallelism + the BUILD-on-evidence gate (the goal points here)
> DEFAULT = **pipeline**; SPLIT only when two evidenced targets are queued. Fixes "训练一直放不开" without dueling writes.

- **Pipeline (default).** A training/eval run occupies the GPU(s); the main loop does NOT idle-wait — it uses
  that window to DESIGN/SEARCH the next node (Pro-survey-mining · next-candidate design · reading results).
  Compute + cognition overlap; this is the productive form of the WAIT discipline (§4.9) — *the wait IS when
  you design the next node.*
- **Split (two evidenced targets queued, each fits one GPU).** GPU0=Idea-1, GPU1=Idea-2 as a parallel burst,
  then reconverge. **Each split run = its OWN Arbor node + its OWN worktree** (no shared state, no dueling tree
  writes); set `CUDA_VISIBLE_DEVICES` per run and label each node with its GPU.
- **The training GATE = BUILD-on-evidence (not free training).** Earn a ~4h run only on an EVIDENCED target: a
  survey-evidenced hard problem → a matching **HF dataset** → a cheap headroom eval on the REAL data shows the
  frozen base FAILS with Δ room. Kill only if the base already solves it, or it's a pure capability wall.
  (Retargets size-first from local synthetic probes — which kept saturating — to real-data headroom; the fix
  for the 0-positive stall.)
- **WAIT unchanged (§4.9).** 4h train → Monitor or Bash bg-wait firing ONCE on {verdict | crash | timeout};
  consume→verdict on fire, never re-arm, never a ScheduleWakeup poll. Launch arithmetic (§4.9-10) per run:
  ETA-vs-cap · data-sufficiency · kill-checkpoint · resume-fail = STOP.

### 5.6 ★ The Failure Atlas + Necessity Gate — depth memory (research-os 小修, 2026-07-04)
> The fix for "很会杀但不会越杀越懂" (great at killing, doesn't get smarter by killing): the loop had WRITES
> (kills, anomalies, region-closes) but no compounding READ per territory. Fable5-primary + Pro-secondary +
> the user's breadth-then-depth. Full spec = research-os `skills/autopsy/references/failure-atlas.md`. Four
> independent engines (Opus · Codex · Fable5 · GPT-5.5 Pro) converged on this.
- **Breadth THEN depth.** Within a domain: Phase A BREADTH scans candidate failure-signatures (necessity-gate
  each) to MAP the atlas; Phase B DEPTH commits to the top fracture and STAYS. Lateral is a legitimate mapping
  move; laterally FLEEING before mapping/exploiting is the bug. Three-tier lateral rule: within-domain breadth
  = allowed (budgeted) · commit-to-depth = the atlas picks · abandon-domain = ONLY on atlas-proven saturation + epitaph.
- **Necessity Gate (before ANY mechanism).** Design a mechanism ONLY for a failure that survives frozen-base +
  tuned-prompting + retrieval + fair plain-LoRA + data-scale + seed + OOD/robustness split + metric-sanity +
  neg-control. Any of them closes it → BENCHMARK_OCCUPIED (reject; NOT a mechanism failure). The SpatiaLQA
  ledger kill is the textbook trip (plain-LoRA precond-F1 0.582 ≥ ledger 0.523).
- **The atlas file.** `<campaign>/atlas/<territory>.md`; entry = claim · evidence-pointer · grade(own-run|lit)
  · what-it-re-prices; a region-close writes an EPITAPH (dead-because-X, reopen-if-Y). `/autopsy` writes;
  `/prospect` (Mine 0) + `/forge` read FIRST. Re-prices, NEVER vetoes (a contradicting run = an [ANOMALY]).
- **3-tier enrichment (anchored-territory ONLY).** FIND (Arbor alphaXiv + `Pro 扩展` + DeepResearch) → DOWNLOAD
  the arXiv PDF/source LOCAL → 精读 by an **Opus SUBAGENT per paper** (Read handles PDFs) returning ATLAS ROWS
  (strongest tuned baseline · method · hidden trap · what-they-didn't-measure · occupancy · probe). Output =
  atlas rows, NEVER "I read N papers" (anti-ceremony guard). Playwright→Pro alone is insufficient (browser
  summary, rate-limited) — hence the local download + subagent deep-read.
- **Arbor (adopt/reject).** ADOPT its worktree / held-out / merge-margin discipline + alphaXiv grounding; the
  atlas is the failure-typed per-territory UPGRADE of Arbor's `get_constraints_block` insight-block (ROOT
  insight + PRUNED LESSONS + VALIDATED FINDINGS). REJECT Arbor's score-plateau→"different approach family"
  convergence reflex — that IS the anti-depth lateral bug, mechanized.

### 5.7 ★ 刷分-first HIGH-THROUGHPUT loop + CORAL (2026-07-04, user pivot) — restore the v0.4 experiment velocity
> The mature endpoint of the generation diagnosis: **AI can't invent the harder problem — that comes from
> surveyed papers, not our experiments — but AI CAN climb a defined benchmark.** So play to the strength:
> 刷分 (improvement-type, `research-types.md`) is now PRIMARY; the novelty/necessity-gate strategy (§5.6) is
> secondary/optional. **What made us slow lately was META-WORK, not research-os** (the `taste.md`
> process-budget>20% trap). This restores "almost-always-刷分" velocity — *better* than v0.4, because gates
> fire only at the claim boundary and the target is a real paper-sourced benchmark, not gate-shaped nothing.
- **The insight (user):** in 刷分 the **metric-GAP IS the failure signature** — the most concrete, quantified,
  visible one (分数不够 = the failure case). So the taste武器库 (frames · operators · 视角转换/reframe · elegant
  math modeling) is **aimed at the score gap**, not at abstract problem-finding — a *constrained, well-posed*
  use of generation AI can actually do: *fix a measured bottleneck*, not *invent a problem*.
- **The FAST OODA loop:** `run → score → 分数不够 (the failure) → analyze WHY (which examples fail, what
  bottleneck = the per-benchmark ATLAS) → aim the taste武器库 at the bottleneck → fix → re-run.` The atlas is
  the failure-map; the score is the compass. Method-source = the arXiv-精读 pipeline (§5.6), not AI invention.
- **Gates only at the CLAIM boundary — never per-iteration.** Inside the loop: run/score/analyze/re-run, fast.
  `/adversary` fires ONLY when you want to say "this Δ is a contribution" (BIG honest Δ vs a TUNED baseline,
  ≥3 seeds, paired). Keep workflow/meta <20% of effort — if we're theorising instead of climbing, ship a run.
- **CORAL = an OPTIONAL 刷分 accelerator — NOT a dependency.** ⚠️ **The `coral` CLI is NOT yet installed**
  (only the plugin skills/subagents are, 2026-07-04). **So the DEFAULT 刷分 loop runs via the EXISTING path:
  an Opus executor subagent (worktree) runs training/eval directly on the built harness, fast OODA — exactly
  as we've been running.** Do NOT block the loop on CORAL. To ENABLE CORAL later: install the `coral` CLI
  (see `coral:coral-quickstart`) → `coral setup` to register the Claude runtime (`coral:setting-up-coral`,
  verify with `coral agents doctor`) → then `coral:coral-task-author` scaffolds a task (repo+grader →
  `coral validate`), `coral:running-coral-experiments` launches/monitors, `coral:coral-run-doctor` diagnoses.
  ⚠️ **2-GPU caveat (applies once enabled):** CORAL's edge is many *parallel* agents; on 2×4090D compute-bound
  attempts serialize — it still helps (code/method edits parallelize; the grader is the bottleneck), but don't
  expect its full multi-island throughput. **AI-Research-SKILLs framework SOPs** (verl/grpo/megatron/vllm…) = install
  on-demand for the method you're running; its `autoresearch` orchestrator = SKIP (a generation tool that
  competes with research-os).
- **The honest venue caveat:** 刷分-to-一区 is *tractable* but still competitive — target niche/underexplored
  benchmarks or tasks where compute isn't the moat, with a BIG honest Δ (climb where the incumbent genuinely
  fails, per the atlas), not "+0.5% by stacking 3 papers" (the incremental trap `/adversary` D rejects).

## 6. Arbor command routing & tree discipline
> A **pragmatic hybrid**: Arbor's tree for STRUCTURE, research-os for DECISIONS, multi-engine for REVIEW.
> We do NOT adopt the full Arbor skill suite (built for unattended full-auto; ours is human-in-the-loop
> goal mode).

### 6.1 Ideation layering (pick by altitude)
| Layer | Weight | Use when |
|---|---|---|
| **`/prospect` + `/forge`** (research-os) | HEAVY — the generator; may escalate to Pro | **DIRECTION-level**: goal start, a new problem, a fork after a region-close. Output = ranked problem cards / a live candidate backlog. |
| **arbor-agent-ideate** | LIGHT — single-engine, 4-line `tree_add_node`, in-loop | **TACTICAL in-loop**: draft the next node under an active candidate, a quick variant. Output = one tree node. |
> Heuristic: does it change the programme / need the external brain? → `/prospect`+`/forge`. Is it "the
> next experiment under this candidate"? → arbor-agent-ideate (or plain Opus-propose, disciplined by the
> Codex hook).

### 6.2 Tree-update checklist (fixes the #1 process bug — loose tree discipline)
At EVERY 验收, tree FIRST then RUNLOG:
- [ ] `tree_update_node` the dispatched node — status (done/pruned/in_progress) + result + insight
      (for a null: the `/autopsy` conversion-law output IS the insight).
- [ ] new candidate → `tree_add_node` BEFORE dispatch · dead branch → `tree_prune` + reason.
- [ ] node types = {idea, experiment, negative, `programme`}. A `programme` node is created only after a
      candidate survives its first claim boundary + human budget approval; its health is checked by
      the `/autopsy` programme pulse (questions, not scores).
- [ ] new track/eval at INIT → `tree_set_meta` the eval contract (B_dev/B_test, metric, metric_direction).
- [ ] **direction/campaign CLOSE → close-out sweep**: reconcile ALL descendant node statuses (no
      dangling in_progress/pending under a closed node) + purge any number lacking an artifact from
      tree/memory before it can propagate into reports (the phantom-E[τ] lesson, §4.8).
- [ ] THEN append the RUNLOG narrative.

### 6.3 Arbor commands: use / skip / adopt-later
| Capability | Status |
|---|---|
| `tree_view/add/update/prune` · peer-review-gate · arbor-agent-ideate | **USED** |
| novelty (`arbor-agent-search`) | covered by Pro 扩展 |
| setup-intake / coordinator | covered by `goal-directive.md` + goal mode |
| `arbor-agent-tools` (emulation layer) | N/A — we have the native MCP tools |
| research-agent / orchestrator (full-auto loop) | **deliberately NOT used** — goal mode fits human-in-loop |
| **`tree_set_meta`+`eval_run`+`git_merge_branch`** (merge-eval automation) | **ADOPT NOW** — `eval_run` writes scores into the tree from the actual command output, which is the structural antidote to write-from-memory number drift (§4.8; the deferral was load-bearing in the DSpark archive incident). |
| executor `RunTraining` + resume/checkpoint | consider for long training runs. |

### 6.4 Isolation discipline (kernel ⑥)
`/prospect`/`/forge` propose (Opus). A **routine tactical selection** (which backlog candidate to run) is
Opus's own call — a resource choice inside the autonomy boundary, disciplined by the KILL side of
`/adversary`/`/autopsy` and the **Codex hook** that independently audits the resulting work. A
**consequential direction / thesis selection** routes to an independent read (**GPT-5.5 Pro**, Playwright).
The anti-self-love discipline = DOWN-only self-verdicts + the automatic hook, not a mandatory pre-work
review call.
