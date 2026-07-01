# Research Operating Manual

> The single "how we work" reference. Read at session start together with `plan/goal-directive.md`.
> This DISTILLS the operational content so `CLAUDE.md` can stay lean and just point here.
> Last updated: 2026-07-01.

---

## 0. Current research state (read this first)
- **★ ACTIVE — DSpark × AR Speculative Decoding: beyond-first-order Markov sequential head.**
  DSpark (arxiv:2606.19348, DeepSeek) proved a 1st-order Markov head cuts suffix decay +26-31% vs EAGLE-3,
  but is under-modeled (RNN variant = "marginal improvement", unexplored). GOAL: design and train a BETTER
  sequential head (higher-order / attention-based / context-aware) that achieves measurably higher accepted
  length. Platform = Qwen3-4B or LLaMA-3-8B (fits 96GB), trained via DeepSpec (MIT, freeze target, TV-distance
  loss). Metric = accepted length (primary) + tokens/sec. Key refs: `DSpark-analysis.md`,
  `plan/dspark-deep-analysis-2026-07-01.md`. Goal directive = `plan/goal-directive.md`.
- **CLOSED (archived to `plan/archive/`, do NOT cross-contaminate):** the entire dLLM/DiffusionGemma/LLaDA
  campaign — frozen heads, He-line, wall-clock frontier, training-based reasoning. That is a SEPARATE,
  COMPLETED project (Arbor tree 5.1-5.13 all done/pruned).

## 1. Engine stack — the division of labor (Opus 4.8 · GPT-5.5 Pro · Codex hook)
> **One line:** Opus is the PI (route + decide + interpret) AND the executor (subagents inherit the session
> model = Opus 4.8); GPT-5.5 Pro is the external brain (the generative leap + prior-art + deep taste); the
> **Codex review hook** auto-audits every executor diff; the human only grants the flagship contribution.
> Manual `/codex:rescue` is **RETIRED** — replaced by the automatic hook.

| Engine | How to invoke | Role |
|---|---|---|
| **Opus 4.8 (me)** | direct (main loop) | **PI / router / decision-owner / interpreter.** ROUTE-FIRST lane triage (§5.0), OBSERVE, IDEATE (skeptical + cross-domain), SELECT/DECIDE, assemble+package the Pro hand-off, run the CHEAP inline gates, update tree/RUNLOG. **Never self-grants a strong (UP) verdict.** Prefer Opus high; reserve xhigh for the hardest judgment. |
| **Opus 4.8 executor subagents** | `Agent` (+ `isolation: "worktree"` when mutating files); inherits session model | **ALL implementation / experiment plumbing / verification runs / gate work / repo exploration / debug** (effort high default; xhigh for a hard bug). Returns changed-files + commands + test-results + artifact-paths + known-risks. Does NOT judge novelty, grant a PASS, touch a sealed holdout, or rewrite the thesis. |
| **GPT-5.5 Pro** | Playwright `browser_*`; model button = **`Pro 扩展` (the ONLY tier — never switch)** | **External brain:** the object-shift generative LEAP (F4.5), prior-art / occupancy scan, deep/contested taste-KILL, novelty/AC meta-review. Compact Opus-packaged hand-off (never a repo dump). 1h+; **poll 15 min**; **new chat per query**; **keep Playwright alive — never close/restart**. |
| **Codex review hook** | AUTOMATIC (SubagentStop; `CODEX_REVIEW_GATE_GLOBAL=true`) | **Independent adversarial review of EVERY executor subagent's diff** — SPARK inline (`gpt-5.3-codex-spark`, fast triage) + DEEP background (`gpt-5.5 xhigh`, read-only), advisory / non-blocking, surfaced via `systemMessage`. This IS the independent substrate now (replaces manual `/codex:rescue`). A finding = a **binding DOWN** verdict; it **never grants UP** (silence ≠ pass). |
| **Human** | HARD-BLOCK escalation | Contribution / paper / "architecture-advantage" promotion; critic↔proposer deadlock; flagship go/no-go. RARE — not a per-cycle bottleneck. |

## 2. The Arbor MCP — what we keep, what we dropped
Arbor offers two layers; we use only the first.
1. **MCP TOOL layer (KEEP — deterministic, immediately usable):** `tree_view` · `tree_add_node` ·
   `tree_update_node` · `tree_prune` · `tree_set_meta` · `worktree_create`/`worktree_remove` · `eval_run` ·
   `git_merge_branch` · `generate_report` · `open_dashboard`.
2. **`arbor-cycle` / `/arbor-research-agent` SKILL loop — DEPRECATED** (goal mode works better; user decision).
   Do not run it. The init scaffolding it left (`QUEUE.md`, `cycle-state.json`, `BLOCKED.md`, `review_debt.md`)
   is **vestigial** — ignore/archive.
- **Policy:** GOAL mode is the driver. The **Arbor MCP idea tree is the canonical research STRUCTURE**
  (`.arbor/sessions/diffusion-moe/.coordinator/idea_tree.json`). Maintain it at **every 验收 (tree FIRST,
  then RUNLOG)**. Use `worktree_create`/`eval_run`/`git_merge_branch`/`generate_report` opportunistically.
- **★ GOAL = a CONTINUOUS loop, not one stage.** OBSERVE → IDEATE → SELECT → DISPATCH+verify → DECIDE →
  (experiment pass: bank EVIDENCE & advance · FAIL **or decisive NEGATIVE**: BANK it, then **AUTO-PIVOT** —
  re-IDEATE / dispatch the next surfaced lead; **the loop picks the pivot itself by taste and NEVER stops to ask
  the user which direction**) → loop. **★ A banked negative is a per-cycle WIN that feeds the NEXT pivot — it is
  NOT a run-stop, and NOT "inconclusive" (only a no-decision cycle counts as inconclusive). Banking a negative
  and then halting is the #1 loop bug — do not repeat it.** **★ EFFICIENCY (the fix for "always failing", full
  rules §5.2): IDEATE runs an OCCUPANCY-SCAN FIRST (cheap-kill an occupied/substrate-mismatched lever BEFORE any
  design or Pro round); the object-shift generative LEAP is DESIGNED BY Pro (not Opus-checklisted); after 2
  occupied/substrate kills in ONE region the next IDEATE makes a LATERAL JUMP (new task-family/substrate, never
  another neighbor); DSpark-flavored systems leads take the `/baseline-champion` lane, not the object-shift
  machinery.** A
  contribution/paper/"publishable" claim is **NOT** an autonomous loop outcome — it HARD-BLOCKS to
  human/external (§5.1 taste-gate asymmetry); the loop only banks evidence and advances. **`/ideate` "stops at
  ideas" ends the IDEATE STAGE ONLY — it does NOT stop the goal loop.** Never end the session at "shortlist
  ready" or "one experiment done"; continue to dispatch the next un-run lead. **Concrete caps (bounded
  autonomy):** ≤12 dispatched cycles/session; ≤3 consecutive inconclusive leads → stop+report; each experiment
  pre-declares a wall-clock budget (≤3h dev / ≤12h sealed), `kill -9` on overrun OR >30min zero-output.
  Otherwise the RUN stops ONLY when: a result reaches the promotion gate (→ human/external, §5.1); OR the
  shortlist is drained — i.e. **every surfaced lead has ITSELF been killed** (a surfaced-but-untried lead is the
  NEXT cycle, never a stop) — AND 2 re-ideate rounds are dry (meta-saturation); OR a hard cap is hit; OR
  genuinely blocked (needs user). **A surviving/untried lead means the run is NOT done — pivot to it.** **Safe background (ZERO orphans):** only ONE 26B GPU job at a
  time — `nvidia-smi` BEFORE dispatch, QUEUE don't collide. **EVERY long job MUST be TRACKED — no
  fire-and-forget:** prefer harness `run_in_background` (auto re-invokes on completion); a `setsid`-detached
  job is allowed ONLY if it writes a PID-file AND a RUNLOG registry line (cmd / PID / **cwd** / **start-time** /
  budget) AND arms a ScheduleWakeup monitor on that PID — detach without all three is FORBIDDEN.
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
| `plan/README.md` | **one-screen flow map** (Arbor loop + gate optimizations) + plan/ doc index — START HERE | when structure changes |
| `plan/operating-manual.md` (this) | how-we-work reference (engines, Arbor, conventions, lessons, science kernel, §5.1 gates) | when process changes |
| `plan/goal-directive.md` | the exact `/goal` input | when goal/workflow changes |
| `plan/research-operating-system.md` | BACK-half (filter) DESIGN — 7 gates, the asymmetry, the enforceable-contract pattern | when a gate changes |
| `plan/dspark-deep-analysis-2026-07-01.md` | DSpark technical breakdown + occupancy scan | when occupancy changes |
| `DSpark-analysis.md` | DSpark core ideas + transferable concepts | reference |
| `enrich.md` | the Modeling-Object-Shift methodology | reference |
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
   diff); the generator never self-grants — tactical SELECT is Opus's, but the KILL gates + hook discipline it.
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

## 5. Science protocol (the kernel — gate every move)
Falsify-before-build (ship the kill-experiment WITH the idea) · score-up ≠ mechanism (require negative control
+ locality) · eval/test/baseline are a **sealed layer, never changed mid-run** · one variable per probe ·
isolation: **generator ≠ executor ≠ critic** (Opus generates/observes/selects-tactically; **Opus executor
subagents** run in worktrees; the **Codex review hook** independently audits every executor diff; Playwright-Pro
designs the leap / audits) · **experiment has absolute veto over elegance** · every experiment pre-declares
{hypothesis, falsifier, acceptance, negative control, locality check, reproducible evidence, recorded
commands+exit codes} · when evidence contradicts the direction, **redesign the program**, don't defend it.
Negative results / eliminated confounds / killed directions = SUCCESS.

> **★ SUBSTRATE NOTE (read once, applies to ALL of §5).** Everywhere below, an "INDEPENDENT substrate (Codex)"
> now means the **automatic Codex review hook** (SubagentStop → independent `gpt-5.5 xhigh`, advisory), NOT a
> manual `/codex:rescue` dispatch (retired). Operationally: **run the gate work as an executor subagent
> (Opus 4.8, inherits session model) and the hook audits its diff.** A hook finding is a **binding DOWN** verdict (kill/flag); the hook **never
> grants an UP verdict** — a taste PASS, `structural-negative`, `ELIGIBLE`, `PROGRESSIVE`, reward-hack `CLEAN`,
> or baseline dominance is granted only by the **machine validator** (where one exists) + **human promotion**,
> never by the hook's silence. For a deep/contested UP judgment, route to **GPT-5.5 Pro** (Playwright, awaited).

### 5.0 ROUTE-FIRST — the gate budget (efficiency: don't run promotion machinery on plumbing)
Before running ANY gate, Opus classifies the task into ONE lane; only that lane's gates fire. Most work is
cheap and never touches the heavy promotion suite — that is the fix for "rigorous but slow."
| Lane | What | Owner | Gates that fire |
|---|---|---|---|
| **FAST_CODE** | impl / refactor / bugfix / experiment plumbing | executor subagent | `/exp-verify` only + the Codex hook's auto-review of the diff |
| **EXPERIMENT_RUN** | a real experiment / ablation / verifier run | executor subagent | `/context-bundle` (pre-dispatch) → run → `/exp-verify` |
| **NEW_DIRECTION** | a new idea / object-shift lead | Opus assembles + **Pro** designs | `/mos-front` (occupancy-scan FIRST) → `/object-shift-audit` |
| **DSPARK_SYSTEMS** | a measured throughput/quality/compute lever, NO new object | executor subagent | `/baseline-champion` + measured Δ (skip the object-shift ceremony) |
| **POSITIVE_RESULT** | any improved metric / "it works" (CLAIM BOUNDARY) | independent | `/exp-verify` → `/reward-hack-audit` → `/taste-critic` → `/claim-evidence-matrix` |
| **COMPARISON** | "beats / faster / Pareto / frontier / architecture advantage" | baseline adversary | `/baseline-champion` BEFORE the wording is allowed |
| **NEGATIVE_RESULT** | a null / killed branch | Opus (+ independent if structural) | `/exp-verify` → `/bank-negative` |
| **PROGRAMME_BUDGET** | continue this programme? | Opus + independent for a favorable status | `/programme-audit` |

**The budget rule:** FAST_CODE / EXPERIMENT_RUN do **NOT** trigger taste / reward-hack / claim-matrix — those
fire ONLY at a **CLAIM BOUNDARY** (a "works / beats X / is a contribution" assertion). **Every cycle emits ONE
progress token** — `VALID_CODE_MERGED` · `REAL_RUN_VERIFIED` · `NEGATIVE_BANKED` · `POSITIVE_BLOCKED_AS_HACK` ·
`POSITIVE_CLEARED` · `OBJECT_SHIFT_ELIGIBLE` · `LATERAL_JUMP` · `PROGRAMME_RETIRED`. A cycle that emits none is
spinning ("thinking hard, not advancing") → force a lateral jump or bank the null and pivot.

### 5.1 Research-OS taste & anti-Goodhart gates (the ROS layer)
> Full design + grounding: `plan/research-operating-system.md`. **Principle:** goal mode is autonomous for
> SEARCH + FALSIFICATION; it is NOT autonomous for defining success, broadening scope, or declaring a
> CONTRIBUTION. The success-defining gates run on an **INDEPENDENT substrate (never the proposing agent)** —
> Codex-B's invariant: *a success-defining gate must never be runnable by the proposer.*
>
> **Taste-gate ASYMMETRY (the fix for the gameable-pass hole).** In autonomous goal mode the SAME orchestrator
> that proposes also *dispatches* `/taste-critic`, *curates the context* it sees, and *can re-run it* — so a
> proposer-routed critic's verdict is NOT a true independent gate (exactly the "kill-reviewers GAMEABLE"
> failure: sanitized context + narrowed claim + re-run until clean). The gaming failure mode is a **false
> PASS**, never a false KILL. So authority splits by direction:
> - **KILL / DOWNGRADE = autonomous and safe.** The agent SHOULD run `/taste-critic` to kill its own
>   academic-toys / standard-redefinition early; a kill-only critic cutting the proposer's *own* work cannot
>   be gamed toward over-promotion. This is the "minimize human" win — AI filters out toys with no human.
> - **PASS / promotion = NOT autonomously self-grantable.** A proposer-dispatched critic's "no standing kill"
>   is **advisory only**; it does NOT authorize promoting a result to "contribution" / paper / "architecture
>   advantage." Promotion HARD-BLOCKS in autonomous mode and terminates in a **human (or a genuinely external
>   critic the proposer does not control)**. Rare — only survivors of the autonomous kill-filter reach it.
>
> **GENERAL INVARIANT (this asymmetry is not taste-specific — it governs EVERY gate below).** The proposer
> may self-administer a verdict only in the **conservative / DOWNward direction** — the direction where
> gaming cannot help it: KILL/downgrade a direction, grade a null `scoped-negative`, downgrade an unsupported
> claim to a hypothesis. The **strong / consequential / "this counts as a result" verdict** — a taste PASS, a
> `structural-negative`, a baseline-champion dominance sign-off, a `/reward-hack-audit` CLEAN — is a
> success-defining decision and is **NEVER proposer-self-granted**: it runs on an independent substrate
> (Codex/Pro) and, for anything written up as a contribution, terminates in a human/external decider. One-line
> test before trusting any verdict: *"would gaming this verdict help the proposer? then the proposer can't be
> the one who grants it."*

| Loop point | Gate | Required action | Decider |
|---|---|---|---|
| SELECT (NEW direction/thesis) | **Taste gate (KILL — autonomous)** | Run `/taste-critic` (He-bar, kill-only) on an INDEPENDENT substrate (Codex/Pro, fresh context). `ACADEMIC-TOY` / `STANDARD-REDEFINITION-HACK` → BLOCKED; re-ideate (never reword to pass). A `no-kill` clears the direction for *work*, NOT for *promotion* (see promotion row). | independent AI critic KILLS autonomously; `no-kill` ≠ a contribution-pass |
| Pre-experiment | **Preregister** | Freeze {hypothesis, falsifier, acceptance, metric, split, neg-control}, timestamped, before sealed data. Sealed splits immutable; one-tailed tests pre-registered (stat norm). | the frozen contract |
| Cross-system compare | **Baseline champion** | Before any "beats X"/frontier/architecture claim, an independent agent (NOT the proposer) optimizes the OPPOSING baseline to win — same feature set/preprocessing/tuning budget; vLLM/SGLang if serving matters. No dominance claim without sign-off. Model-vs-model = **PAIRED** stats (5×2CV/McNemar/DeLong), never unpaired t-test on shared CV folds. | independent adversary; veto |
| DECIDE / pre-promotion | **Reward-hack audit** | `/reward-hack-audit` on EXTERNAL artifacts: **≥3 seeds mean±std (not best run)**, per-example regression, neg-control consistency, sealed holdout, token-shuffle ablation, no-mock + anti-no-op log_assertion. | Codex (independent) |
| DECIDE | **Negative grade (DOWNward self-grade only)** | `/bank-negative`. The proposer self-assigns **only `failed-attempt` / `scoped-negative`** (conservative — self-grading allowed DOWNward only, since a `structural-negative` is a publishable contribution-equivalent and Goodhart pressure pushes UP). A `structural-negative` is **NOT self-certifiable**: Codex independently verifies the 3-part gate (pre-declared falsifier fired + live controls clean + sealed confirm) against external artifacts; absent that, it stays `scoped-negative (structural-PENDING)`. **ENFORCED, not prose:** every banked case must pass `~/.claude/skills/bank-negative/validate_negative_case.py` (JSON Schema + fail-closed check; `structural_certified_by` has no `proposer` value; regression-tested) — exit≠0 ⇒ not banked. Writing a structural-negative up as a contribution routes through the promotion row. No over-generalizing a scoped null to "direction dead." | self-grade ≤ scoped autonomous; **structural cert = Codex (independent), never proposer — machine-enforced**; write-up → promotion row |
| Contribution/paper promotion (PASS — NOT autonomous) | **Taste-critic + claim-evidence** | A `/taste-critic` `REAL-CONTRIBUTION` classification + every claim mapped to an evidence type are **necessary advisory evidence, not a self-grantable pass**. Promoting a result to "contribution"/paper/"architecture advantage" HARD-BLOCKS in autonomous mode → terminates in a **human (or external critic the proposer doesn't control)**. ENGINEERING ≠ contribution; **a new metric/benchmark is GUILTY until it corrects a misleading existing eval (REFORMS).** | proposer-dispatched critic = advisory; the PASS is **human / external**, never proposer-self-granted |

**Autonomy boundary** ("do not ask the user to choose" = TACTICAL choices only):
- MAY unilaterally: observe · ideate · tactical variants · preregister · dispatch worktree executors · tune ·
  run dev/sealed eval under frozen contracts · update tree/RUNLOG · bank EVIDENCE · **run `/taste-critic` to
  KILL/downgrade its own toys early** (the autonomous kill-filter).
- MAY NOT: change the success metric after seeing results · broaden scope · **self-grant a taste PASS that
  promotes a result to CONTRIBUTION / publishable / "architecture advantage"** — that PASS terminates in a
  human (or a genuinely external critic the proposer does not control); a proposer-dispatched critic's
  "no-kill" is advisory evidence, NOT the pass.
- **AI CAN do taste — but only the KILL side autonomously.** As an INDEPENDENT, kill-only critic the agent
  filters out toys with no human in the loop (taste-FILTERING, autonomous; this is the "minimize human" win).
  It may NOT autonomously grant the promotion PASS, because a proposer that dispatches + curates + re-runs the
  critic can manufacture a false pass — gaming pushes toward false-PASS, never false-KILL. The human is a RARE
  escalation: the **promotion PASS**, critic↔proposer deadlock, or flagship go/no-go — **not** a per-cycle
  bottleneck (most work is killed or stays internal and never reaches the human).
- **External backing for "taste = independent, not proposer":** the community agent-native rigor-reviewer
  structurally omits novelty/significance; openreviewer "complements, not replaces" human review.

### 5.2 MOS-Front — the front-half GENERATOR gates (the enrich layer)
> Full design: `plan/mos-front-architecture.md`. The §5.1 gates are the **filter** (is the result real?);
> MOS-Front is the **generator** (is this the right modeling OBJECT?), firing at IDEATE→SELECT, BEFORE the
> filter. **Role split (efficiency + the "near-original" engine):** Opus ASSEMBLES context + PACKAGES;
> **GPT-5.5 Pro DESIGNS the generative leap** (the new object — a different model + independent context reaches
> what an Opus checklist would not; this is where enrich's scheme-types become near-original content); Codex
> AUDITS/kills; human grants the consequential contribution. **Two efficiency rules (the fix for "always
> failing"):** (1) **occupancy-scan FIRST** — cheap-kill a lever that is occupied / fails-on-substrate BEFORE
> any design or Pro round (most past cycles wasted the design first, then died "occupied"); (2) **lateral-jump**
> — after 2 occupied/substrate kills in ONE region, the next `/mos-front` MUST change task-family/substrate (no
> more neighbors of the dead idea). Generative engine = **O0-equivalence failure mining**; keystone = the
> **DPC** (a pre-training, O0-matched, S-stratified failure-split prediction with shuffled-S + generic-difficulty
> controls) — the machine-checkable real-vs-cosmetic test. **DSpark-flavored systems leads** (a measured lever,
> no new object) skip this machinery → the systems lane (`/baseline-champion` + measured Δ); it is co-equal.

| Loop point | Gate | Required action | Decider |
|---|---|---|---|
| IDEATE (new direction / object-shift lead) | **`/mos-front`** (Opus assembles + Pro designs the leap) | **Occupancy-scan FIRST** (F2.5: occupied/substrate-fail → `LATERAL_JUMP`, no design; 2 region-kills → forced jump). Then two-lane triage `SKIP_TACTICAL` / `MOC_LITE` / `MOC_FULL`. For LITE/FULL: phenomenon-bundle → default-object-map → omitted-structure miner → school-router (+ **mandatory rival**) → **route the generative LEAP to Pro** (F4.5 hand-off: occupancy-map + substrate-constraints + omitted-structure → Pro designs O1 + DPC) → Opus packages into MOC + **DPC**. SKIP_TACTICAL/LATERAL_JUMP may NOT use object-shift language. | Pro DESIGNS, Opus PACKAGES (`self_certified:false`); eligibility = independent `/object-shift-audit`, never self-granted |
| SELECT (object-shift claim — **both MOC_LITE & MOC_FULL**) | **`/object-shift-audit`** (Codex, kill-only) | T1–T6 (distinct-object · observable-S · pre-training differential-prediction · rival-baseline · neg-control · kill-action) + the DPC check (LITE = lightweight). Verdict `KILL_COSMETIC_RESHIFT` / `DOWNGRADE_TO_TACTICAL_VARIANT` / `ELIGIBLE_FOR_BACK_HALF` (NOT a contribution — only "may enter the kill-filter"). **Machine-enforced** by `validate_object_shift.py`. | proposer self-assigns only KILL/DOWNGRADE; **`ELIGIBLE_FOR_BACK_HALF` = Codex (independent), machine-enforced** |
| BACKPROP (active programme) | **`/programme-audit`** (Codex, tree) | Lakatos progressive-vs-degenerating BUDGET signal: deterministic `programme_progress_score` from immutable ledgers → `PROGRESSIVE` / `STABLE_BUT_UNPROVEN` / `DEGENERATING_WATCH` / `DEGENERATED_RETIRE_OR_FORK`. Hard-core-edit-after-failure = −4. **Machine-enforced** by `validate_programme.py`. | self-claim ≤ canonical; **`PROGRESSIVE` = independent, machine-enforced** |

**Orchestration (when /goal calls what):** new direction → `/mos-front`: **occupancy-scan FIRST** (occupied/
substrate-fail → `LATERAL_JUMP`, re-IDEATE on a new region — do NOT design) → else FULL (Pro designs the leap)
→ `/object-shift-audit`(must be ELIGIBLE_FOR_BACK_HALF) → preregister → DISPATCH. Object-shift-flavored lead
under a programme → `/mos-front`(LITE). Tactical variant → `/mos-front`(SKIP_TACTICAL waiver) → straight to the
back-half. **DSpark-flavored systems lead (measured lever, no new object) → skip object-shift machinery →
`/baseline-champion` + measured Δ (co-equal lane).** Every cycle on an active programme → `/programme-audit`.
The §5.1 filter gates fire unchanged after. (Cheat-sheet: `mos-front-architecture.md` §11.)

### 5.3 ★ ARBOR IS THE SUBSTRATE — write STRUCTURE through the MCP, not md/json
> **Arbor MCP is the canonical store and the execution substrate; it is more reliable than hand-written
> md/json. So every gate PERSISTS its STRUCTURAL output through Arbor MCP, and md/json is reduced to ONLY the
> sealed, VALIDATED typed contracts research-os adds that Arbor's fixed-field node cannot hold.** The Arbor
> tree (`idea_tree.json` via the MCP) is the source of truth for structure; RUNLOG is secondary narrative (or
> generate it with `generate_report`). "Research-OS keeps only what Arbor can't express."

Arbor node fields = `hypothesis · status · result · insight · score · test_score · code_ref`; session meta =
`eval_cmd/eval_cmd_test · baseline/trunk_score · metric_direction`. The write-through map:

| Loop point | Arbor MCP (the substrate — PRIMARY) | research-os-only (sealed artifact, `node.code_ref` → it) |
|---|---|---|
| OBSERVE | `tree_view` | — |
| new direction / hypothesis | `tree_add_node(hypothesis, status)` | — |
| preregister the eval contract | `tree_set_meta(eval_cmd, eval_cmd_test, baseline_score, metric_direction)` | the {falsifier, neg-control} not in meta → 1 small sealed prereg file |
| DISPATCH isolation | `worktree_create` / `worktree_remove` | the `/context-bundle` (built from `tree_view` recent insights) |
| run eval + record score | **`eval_run(cmd, split=dev|test, node_id, set_meta)`** | the `/reward-hack-audit` rigor checks (≥3-seed/neg-control/shuffle) |
| DECIDE outcome | `tree_update_node(result, insight, score, status)` | — |
| bank a null | `tree_prune(reason)` + `tree_update_node(insight)` | the `/bank-negative` GRADE (validator) → sealed `negative_case` |
| merge / promote | **`git_merge_branch`** (already a no-regression gate: beat-trunk-on-B_test + required_outputs + protected_paths) | the `/baseline-champion` "is the baseline STRONG?" check (Arbor only checks beat-trunk) |
| programme node | `tree_add_node` + `tree_update_node` | the `programme` ledgers + `/programme-audit` score (validator) |
| object-shift | `tree_update_node(insight=verdict, code_ref→bundle)` | the sealed `MOC + DPC` + `/object-shift-audit` (validator) |
| the narrative | `generate_report` | — |

**Rule:** if Arbor has a tool/field for it, USE IT (don't re-implement in md/json). Only the **validated typed
contracts** (MOC, DPC, object_shift_audit, programme ledgers, negative_case) persist as sealed files — because
they need fail-closed schema validation Arbor doesn't do — and the node's `code_ref` points at them. This
deletes the parallel structure-JSON pile (the old `mos-front-architecture.md §16` packet).

## 6. Arbor command routing & tree discipline
> We run a **pragmatic hybrid**: Arbor's tree for STRUCTURE, our methodology for DECISIONS, multi-engine for
> REVIEW. We do NOT adopt the full Arbor skill suite — that's built for an *unattended full-auto* loop; ours
> is *human-in-the-loop goal mode* (the user decides at Track turns). Forcing the full INIT→…→DECIDE ceremony
> every cycle would slow the research. This section writes down the routing that was previously implicit.

### 6.1 Two ideate skills — NOT in conflict; correct layering (pick by altitude)
| Skill | Weight | Use when |
|---|---|---|
| **/ideate** (`research-ideation`) | HEAVY — multi-engine (Opus Explore + Opus generators + Codex-hook rigor + Pro 扩展 novelty/AC), 1h+ Playwright poll | **DIRECTION-level**: a Track turn, a new thesis, a fork after a kill. Output = ranked falsifiable shortlist. |
| **arbor-agent-ideate** | LIGHT — single-engine, 4-line `tree_add_node`, in-loop | **TACTICAL in-loop**: draft the next node under an active lead, a quick variant. Output = one tree node. |
> Heuristic: would you route it to Pro 扩展 / does it change the program? → `/ideate`. Is it "what's the next
> experiment under this lead"? → `arbor-agent-ideate` (or just Opus-propose → Opus tactical SELECT, disciplined
by the KILL gates + Codex hook; Pro for a consequential direction).
> **Front-half (§5.2):** if the direction claims a new modeling OBJECT (not a new module/loss), run
> `/mos-front` to turn it into a falsifiable MOC+DPC → `/object-shift-audit`. `/ideate` and `/mos-front`
> compose: `/ideate` surfaces directions; `/mos-front` makes an object-shift direction *killable*.

### 6.2 Tree-update checklist (fixes the #1 process bug — loose tree discipline)
At EVERY 验收, tree FIRST then RUNLOG:
- [ ] `tree_update_node` the dispatched node — status (done/pruned/in_progress) + result + insight.
- [ ] new lead → `tree_add_node` (4-line hypothesis) BEFORE dispatch · dead branch → `tree_prune` + reason.
- [ ] **node types = {idea, experiment, negative, `programme`}** (§5.2). A `programme` node (durable
  object-shift: hard_core + positive/negative heuristic + corroboration/degeneration ledgers) is created ONLY
  after the first `DIFFERENTIAL_PATTERN_FOUND` + human budget approval (avoids programme bloat); audit it with
  `/programme-audit` each cycle.
- [ ] new track/eval at INIT → `tree_set_meta` the eval contract (B_dev/B_test, metric, metric_direction).
- [ ] THEN append the RUNLOG narrative.

### 6.3 Arbor commands: use / skip / adopt-for-Track-3
| Capability | Status |
|---|---|
| `tree_view/add/update/prune` · peer-review-gate · `/ideate`+`arbor-agent-ideate` | **USED** |
| novelty (`arbor-agent-search`) | covered by Pro 扩展 |
| setup-intake / coordinator | covered by `goal-directive.md` + goal mode |
| `arbor-agent-tools` (emulation layer) | N/A — we have the native MCP tools |
| research-agent / orchestrator (full-auto loop) | **deliberately NOT used** — goal mode fits human-in-loop |
| **`tree_set_meta`+`eval_run`+`git_merge_branch`** (merge-eval automation) | **NOT YET — worth ADOPTING for Track 3.** metadata has been N/A all project (manual Opus DECIDE + Codex-hook review of the merge diff — works, but doesn't scale). Track 3 trains MANY adapter variants → populated trunk/test scores + automated eval finally pay off. NOT a current blocker; the infra to add when variant-count grows. |
| executor `RunTraining` + resume/checkpoint (`arbor-agent-resume-report`) | **consider for Track 3** — long training runs need checkpoint/resume; standardizes train→eval. |

### 6.4 Isolation discipline (kernel ⑥ — occasionally broke)
IDEATE proposes (Opus). **SELECT** (with manual `/codex:rescue` retired): a **routine tactical selection**
(which of N surfaced leads to run) is Opus's own call — a resource choice inside the autonomy boundary,
disciplined by the KILL gates (taste-KILL + `/object-shift-audit` can veto a pick), the occupancy-scan, and the
**Codex hook** that independently audits the resulting work. A **consequential direction / thesis selection**
routes to an independent read (**GPT-5.5 Pro**, Playwright). The old "Codex decides every SELECT" pre-work
dispatch is gone — the anti-self-love discipline is now the KILL gates + the automatic hook, not a mandatory
Codex call before work starts.
