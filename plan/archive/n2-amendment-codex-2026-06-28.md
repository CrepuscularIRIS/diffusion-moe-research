# N2 Build-Contract Amendment — Codex independent review (2026-06-28)

> Independent reviewer: Codex/GPT-5.5 (mandatory rigor gate). Verdict on
> `plan/gpt55pro-N2-codecfree-2026-06-28.md` = **BUILD-WITH-FIXES**. This doc folds the
> material fixes into the build contract. The builder implements the N2 contract **as amended here**.
> Tree node 5.3.1.1 (N2). Branch: `n2-embflow` (off embflow `67d0314`).

## Why amend (the material gap)
Pro's N2 removes the *snap codec* confound but leaves a THIRD confound uncontrolled: the rectified
mask↔clean line `Z=(1−λ)·e_mask+λ·X0` is a **non-native interpolant**. The frozen model trained ONLY on
D3PM-uniform DISCRETE token corruption (corrupted token ids → normal embedding lookup; "mask" = valid-vocab
centroid). It never saw continuous embedding mixtures. So a clean negative on the rectified line could be
misattributed to "model can't consume a continuous field" when the true cause is "model can't consume *this*
non-native interpolant / off-manifold inputs per se." N2a, even un-snapped, still feeds off-manifold mixture
states → its failure could be pure continuous-OOD, not codec and not capacity.

## FIX 1 (decisive, cheap) — native-corruption 3-way control
At each noise level, build the active-block input THREE ways and compare (no training, just input construction):

- **(i) `nat_discrete`** — native DISCRETE oracle: SAMPLE actual D3PM-uniform corrupted tokens from x0=y*
  at level j (keep-prob = the model's native cumulative ᾱ_j; replaced positions = uniform valid-vocab draw),
  then NORMAL embedding lookup. On-manifold, in-distribution — what the model was trained on. Upper bound for
  "can the model denoise its own corruption" in this multi-block harness. (≈ native few-step with oracle tokens.)
- **(ii) `nat_cont`** — native-schedule CONTINUOUS expectation: feed the expectation embedding under the model's
  actual D3PM-uniform marginal at the NATIVE ᾱ schedule: `Z_j = ᾱ_j·E[y*] + (1−ᾱ_j)·ē`, where `ē` = mean
  valid-vocab embedding (= the centroid that serves as the mask). Off-manifold (a mean embedding) but matched to
  the native marginal. Tests the **Jensen / off-manifold gap** at the native schedule.
- **(iii) `n2*` (rectified DDIM line)** — the N2 interpolant `Z_j=(1−λ_j)·e_mask+λ_j·X0` at the DDIM a_j/b_j
  schedule. Tests interpolant SHAPE/SCHEDULE on top of off-manifold-ness.

Math note for the implementer: if `e_mask == ē` (uniform-vocab mean — VERIFY against the checkpoint's mask
construction), then (ii) and (iii) have the SAME functional form `λ·E[y*]+(1−λ)·ē`; they differ ONLY in the
SCHEDULE (native ᾱ_j vs DDIM a_j/b_j). So (ii) = (iii) with the native schedule substituted. Reconstruct the
model's native ᾱ_t schedule from `schedule.py`/the native sampler. The genuinely new contrast is **(i) discrete
vs (ii) continuous-at-native-schedule** = the Jensen/off-manifold gap (model is nonlinear: E[f(e(x_t))] ≠
f(E[e(x_t)])); plus **(ii) vs (iii)** = schedule/shape.

Decomposition the control buys:
- (i) works & (ii) fails ⇒ failure is OFF-MANIFOLD continuous inputs (Jensen gap), NOT the interpolant.
- (ii) works & (iii) fails ⇒ failure is the DDIM SCHEDULE/SHAPE specifically.
- (i) FAILS ⇒ the multi-block harness can't even denoise in-distribution discrete corruption (harness/codec
  problem) — invalidates over-claiming anything about continuous consumption.

Run (i)+(ii) as ORACLE arms (X0=E[y*]) at the same K grid as N2a, on the dev gate first; promote to sealed only
the arms needed for the final verdict.

## FIX 2 — CI-based decision bins (replace cliff thresholds)
Use the existing problem-clustered paired bootstrap (10000). Classify each arm vs target `T=0.95·A_full=0.893`:
- **PASS** iff CI lower bound ≥ T.
- **FAIL** iff CI upper bound < T.
- **INCONCLUSIVE** otherwise.
Apply the same PASS/FAIL/INCONCLUSIVE bins to the consumability gate (GoldTop1(K−1) vs 0.90 and the
continuous-vs-discrete read-curve gap vs 5pp) using CIs, not point estimates. Round-trip: treat ≥0.995 as a
NUMERIC sanity check (log embedding norms to rule out scale drift), not a semantic cliff — relax to ≥0.99 if the
only shortfall is fp/scale noise and gold-token argmax round-trip is otherwise saturated.

## FIX 3 — explicit INCONCLUSIVE branches + per-declared-K COVERAGE (no forced verdict, no overclaim)
**COVERAGE GUARD (overrides everything below):** NO definitive verdict (qualified-B, codec-culprit, or the
schedule-specific branch) may emit unless EVERY gating arm the branch references is PRESENT and DEFINITIVE
(not missing, not INCONCLUSIVE unless the branch explicitly permits it) at EVERY declared K (the run's `ks`,
not whatever data happens to be present). A present+PASS K must never mask a missing/FAIL K. Empty/None
declared-K ⇒ never definitive. This applies to n2a round-trip, n2b, nat_discrete, nat_cont, g4_soft_cont,
consumability — per K, with `all(declared_ks: ...)` conjunctions.

The decision MUST emit `mechanism_unresolved_INCONCLUSIVE` when:
- N2a passes acc but fails round-trip at any declared K (interface only partially valid) → actually route to
  `sanity_failed_STOP` if round-trip FAILs (<0.99) at any declared K.
- N2b or G4-SOFT-CONT recover at one declared K but not another (split — no consistent direction across K).
- Any gating arm is missing/INCONCLUSIVE at any declared K (coverage gap).
- (i)/(ii)/(iii) contrasts conflict (e.g. (i) nat_discrete FAILs — harness-limited → `harness_limited_INCONCLUSIVE`).

**A→qualified-B** (broad negative: "no usable continuous tied-embedding interface few-step") only when ALL hold
at ALL declared K: N2a round-trip PASS; (i) nat_discrete PASS; N2b FAIL (CI upper bound < T); consumability
FAIL near commit; G4-SOFT-CONT does NOT recover (FAIL); AND **(ii) nat_cont is NOT a clear PASS** (must be FAIL
or INCONCLUSIVE — because a clear nat_cont PASS would mean a continuous interface DOES work at the native
schedule, contradicting the broad claim → see schedule-specific branch). Attribution label on qualified-B:
nat_cont FAIL all K ⇒ `off_manifold_general` (strongest); nat_cont INCONCLUSIVE ⇒ use the Jensen gap
(`off_manifold_jensen` if (i)-vs-(ii) CI lb >5pp, else `unspecified`).

**NATIVE-SCHEDULE-CONTINUOUS-WORKS** (NEW branch, NOT qualified-B — a narrower/partial-positive finding): when
nat_cont (ii) is a clear PASS at ALL declared K AND n2b (iii) FAILs at all K (with n2a/round-trip/nat_discrete
coverage OK) ⇒ "an oracle continuous interface IS usable few-step at the model's native schedule; the
training-free DDIM-schedule decoder fails — the failure is DDIM-schedule/shape-specific, not continuous-inputs
per se." This WEAKENS the broad negative and must be reported as its own verdict, never folded into qualified-B.

**codec-is-culprit (withdraw N1b)** only when, at ALL declared K: N2a round-trip PASS AND N2b PASS (CI lb ≥ T)
AND g4_soft_cont and nat_discrete are PRESENT+DEFINITIVE (coverage). Sub-attribution from g4_soft_cont: PASS all
K ⇒ snap was the main culprit; FAIL all K ⇒ model reads oracle continuous states but training-free soft
estimates don't define a usable field. If g4_soft_cont/nat_discrete missing or INCONCLUSIVE at any declared K
⇒ NOT definitive → `mechanism_unresolved_INCONCLUSIVE` (incomplete_or_split_k_coverage).

## FIX 4 — narrow phrasing (scope every claim)
N2a is a sanity gate for THIS specific continuous interface, NOT a general "can a frozen discrete dLLM consume
continuous fields" test. All claims scoped to: this checkpoint / tied-embedding interface / no-training / the
tested mask↔clean (and native-ᾱ) paths.

## Builder deliverables (code-only; NO GPU; NO 26B load; NO full eval — GPU busy with decisive sealed run)
1. N2 generation in `blockgen.py` (or new `n2.py`): methods `n2a`, `n2b`, `g4_soft_cont`, plus controls
   `nat_discrete`, `nat_cont`. NO intermediate NN-snap (assert it). Match embedding scale √d. Reuse
   hook.py/embedding.py/teacher.py/schedule.py. Reconstruct native ᾱ_t schedule for the controls.
2. Per-step consumability logging: GoldTop1(j), GoldNLL(j), GoldMargin(j); decisive node j=K−1.
3. Wire into `run_eval.py`: extend GEN_METHODS; add CI-bin classifier + INCONCLUSIVE branches + the 3-way
   contrast to `analyze()`; keep resumable JSONL + sealed/dev plumbing UNCHANGED (sealed verifier/test sealed).
4. Self-conditioning = LOGGED condition (primary SC=P_j; controls SC=δ_{y*}, SC=0); report if conclusions differ.
5. Controls/assertions: no-re-discretization assert; perturbation test (nudge one active row → next logits must
   change); log router entropy / soft-vs-token expert overlap; log norms (scale check).
6. Unit tests (logic only, tiny synthetic tensors / fake model — DO NOT load the 26B): schedule endpoints
   (a_0=0,b_0=1,a_K=1,b_K=0), native-ᾱ reconstruction, expectation-embedding formula, no-snap assertion,
   CI-bin classifier, perturbation scaffold. Commit to `n2-embflow`. Leave a one-command launch line ready for
   when the GPU frees (dev gate first: `--dataset dev --n 32`, eager env per SEALED_REPORT §E).
