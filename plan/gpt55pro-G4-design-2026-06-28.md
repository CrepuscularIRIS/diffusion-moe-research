# GPT-5.5 Pro 扩展 — G4+N1 Novelty Audit + Formal Design (2026-06-28)

> Source: Playwright→GPT-5.5 **Pro 扩展**, chat "Model Audit and Design" (已思考 12m42s).
> Selected experiment (Codex SELECT) = **G4 training-free embedding-DDIM few-step sampler** + **N1 oracle
> companion**, Track-2 gradient-field/embedding-flow on FROZEN DiffusionGemma. This doc = the FROZEN BUILD
> CONTRACT (top) + the raw Pro response (bottom, provenance). Do NOT modify the sealed eval/test.

---

## ★ AREA-CHAIR VERDICT (Pro)
The defensible novel claim (disciplined, narrow): **"A frozen, shipped, large discrete masked-diffusion LM can
be externally probed for a *decodable continuous clean-data / average-velocity field* in its tied embedding
space, judged ONLY by verified few-step generation (not diffusion loss / teacher-forced CE)."**
- G4 alone ≈ **workshop / Findings** unless a surprisingly strong verified-gen win.
- **G4 + N1 falsification package = stronger** (top-venue-plausible as an empirical kill of a fashionable
  clean-data/velocity transfer hypothesis that prevents wasted adapter training).
- G4 + N1 + a learned adapter that closes the 4–12-NFE gap = top-venue-plausible.
- **Hard-snap-only G4 (no soft carryover) = weak novelty** (looks like ReMDM/Fast-dLLM sampler engineering).

## ★ NOVELTY (overlap classes; differentiate in the front matter)
| Claim | Class | Closest threats | Differentiator |
|---|---|---|---|
| (1) training-free embedding-DDIM on a frozen discrete dLLM | near-frontal-cite-and-differentiate | ELF, Loopholing, DDIM, D3PM/MDLM/RADD, ReMDM, Fast-dLLM | frozen shipped 26B, no retrain/distill, external tied-embedding integration, verified-math @4-12 NFE; **weak if hard-snap only** |
| (2) oracle few-step-integrability DIAGNOSTIC as a negative | defensible-slice (potentially strongest) | MeanFlow/iMF/pMF, consistency, CDLM bridges, DDIM | treats few-step continuous reachability as an **intervention-level falsifiable property** of a frozen discrete LM; **must avoid a tautological oracle** |
| (3) learned embedding-velocity / pMF-clean-out adapter | defensible-slice, high-risk | ELF, Loopholing, MeanFlow/pMF, JiT, SDTT, CDLM/consistency, DiMO | freezes the LM, learns only a light clean/velocity adapter, evaluated on verified reasoning; **"frozen-dLLM adapter exploiting tied-embedding geometry" not "MeanFlow for language"** |
No lethal pivot for the EXACT combination. Lead with the frozen-backbone / verified-generation / structural-
diagnostic angle. Cite **Loopholing** prominently (soft latent carryover already known to help discrete
diffusion → our answer: "not for FROZEN large dLLMs, not measured by verified gen, not with an oracle arm").

---

## ★ FROZEN BUILD CONTRACT (what the worktree subagent implements)
Notation: vocab V; d=2816; tied W∈R^{|V|×d}; scaled token embedding **e(v)=√d·W_v** (Gemma scale √2816);
mask embedding **m=e([MASK])**; canvas L=256; reverse steps j=K..1; **K∈{4,6,8,12}**; t_j=j/K (t_K=1,t_0=0).

**Schedule (PRIMARY = linear mask→clean bridge; keeps states on the [MASK]→clean segment):**
α_j = 1−t_j, σ_j = t_j;  surrogate forward bridge z_j ≈ α_j·x0 + σ_j·m.  (Cosine VP α=cos(πt/2),σ=sin(πt/2)
= SENSITIVITY ABLATION ONLY; primary result uses linear.)

**Clean estimate from one frozen forward** ℓ_j=f_θ(prompt,z_j) ∈ R^{L×|V|}:
- PRIMARY (soft centroid): x0_hat_soft[i] = Σ_v softmax(ℓ_{j,i}/T_clean)_v · e(v),  **T_clean=1.0**. Use the
  in-model `softmax(logits)@W·√d` path if exposed, else compute explicitly.
- ABLATION (argmax): x0_hat_argmax[i] = e(argmax_v ℓ_{j,i}). (Collapses the distribution → weaker field test.)
- Committed positions: x0_hat[i] = e(y_i).

**Deterministic embedding-DDIM update** (per uncommitted position i, ε=1e-4):
r_hat_{j,i} = (z_{j,i} − α_j·x0_hat[i]) / max(σ_j,ε);  z_{j-1,i} = α_{j-1}·x0_hat[i] + σ_{j-1}·r_hat_{j,i}.
Committed: z_{j-1,i}=e(y_i). Init z_K=m everywhere. At j=1, σ_0=0 ⇒ z_0=x0_hat (final snap decides output).

**Ingestion fork (THE key methodological axis):**
- **G4-SOFT (PRIMARY scientific test)** — no-parameter forward HOOK: build input_ids (prompt + [MASK]
  placeholders), let the normal embedding lookup run, then IMMEDIATELY replace the generation-canvas
  embeddings with z_j (leave prompt embeddings, position enc, attention mask, router, experts, all weights
  unchanged). torch.no_grad, bf16, eval. Still training-free; report as G4-SOFT (changed inference interface).
- **G4-HARD (control)** — snap/re-mask every step, feed token IDs only. A G4-HARD negative **does NOT**
  falsify the embedding-velocity program (it only tests hard Voronoi snapping). Predeclare both arms.
- If G4-SOFT cannot be implemented safely, the paper must NOT claim to test a continuous frozen-dLLM field.

**Snap rule (tied matrix only; no auxiliary decoder):**
- PRIMARY snap_E(z) = argmin_v ||z−e(v)||² = argmax_v [z·e(v) − ½||e(v)||²] over valid v.
- ABLATION snap_H(z) = argmax_v z·W_v. (If snap_E works but snap_H fails ⇒ input-embeds aren't valid final
  hidden states for the head — NOT proof the path is non-integrable.)
- Exclude only truly-invalid special tokens; ALLOW \boxed{}, punctuation, LaTeX, whitespace tokens.

**Commit / re-noise (reuse the shipped EntropyBoundSampler acceptance — change only ONE thing vs native):**
per step compute ℓ_j → z_{j-1} candidate → ỹ=snap_E(z_{j-1}) → use the SAME entropy-bound acceptance to pick
accepted set A; accepted: y=ỹ, z=e(y), commit; unaccepted: G4-SOFT keep continuous z, G4-HARD re-noise to m.
At j=1 force-decode all unresolved. **1 NFE per frozen forward**; report NFE AND wall-clock AND correct/sec.

**Baselines (FAIR — never "first K of 48"):**
- PRIMARY: **Native-K-rescaled** — reconfigure the EB sampler as if its max denoise budget were K (same temp /
  entropy-bound / re-noise / prompt / canvas / max-tokens / EOS / verifier; schedule compressed 48→K).
- ROBUSTNESS: **Native-K-subsampled** — uniform nodes q_j=round(48·j/K); execute only those transitions.
- Native_K := max(Native-K-rescaled, Native-K-subsampled). Forced-early-termination after K-of-48 = APPENDIX
  bad-control only (never the GO baseline).

**N1 oracle (decisive-negative arm; teacher y* = first verifier-correct full-NFE native completion, else
reference solution reformatted to same answer template, tokenized, math_verify-checked):**
- **N1a (codec/bridge sanity)** — x0_hat[i]=x*_i=e(y*_i) EVERY step; same DDIM bridge+snap+accept. Metric:
  intermediate wrong-token-rate WTR_j = frac{i: snap_E(z_{j,i}) ∉ {[MASK], y*_i}} (exclude fixed prompt/ctx);
  report max_j WTR_j + final verified acc. Tests whether the tied-embedding bridge is token-valid under the
  frozen interface.
- **N1b (oracle-to-basin; DECISIVE; avoids final-clamp tautology)** — oracle target for j=K..2; at j=1 use the
  MODEL'S OWN clean estimate x0_hat=softmax(f_θ(z_1))·W·√d, decode normally. Tests whether the oracle
  trajectory lands in a basin where the frozen model's own final estimate suffices.

**Eval (sealed):** MATH-L5 PRIMARY; AIME-2024 = holdout sign-check, run ONCE, NEVER select K on it. 1
candidate/problem, **pass@1 at matched NFE**, math_verify + \boxed{}. Acc(m)=mean_p 1{parseable ∧ verified}.
Problem-clustered PAIRED bootstrap (10000 reps), percentile 95% CIs per K (+ a max-over-K CI for the
best-K selection effect).

**Pre-declared thresholds:**
- **GO** (continue to learned adapter H2/H1): ∃K∈{4,6,8,12}: Δ_K = Acc(G4-SOFT_K) − Acc(Native_K) ≥ 0.03 AND
  paired-bootstrap 95% LB > 0.
- **KILL G4 (training-free)**: ∀K Δ_K < 0.01 AND upper 95% CI excludes +0.03.
- **N1 STRUCTURAL KILL** (kills the velocity-head program H1/H2): A_full≈0.83 ⇒ target 0.95·A_full≈0.7885;
  kill iff max_K A_{N1b,K} < 0.7885 AND upper 95% clustered-bootstrap CI also below target. If ONLY N1a fails →
  kill hard-snap embedding-DDIM only. If N1a passes but N1b fails → kill "frozen reads the continuous state
  without a learned terminal adapter" (NOT all adapters).
- **AIME-24**: same-sign/neutral-within-CI = acceptable; MATH-L5-positive but AIME-large-negative = red flag.

**Decision routing (post-run):**
- N1b PASS + G4-SOFT beats Native_K + G4-HARD does NOT → continuous carryover is the missing ingredient → build H2 (pMF clean-out) / H1.
- N1b PASS + G4 fails → a learned MeanFlow/pMF adapter is justified → H2.
- N1a or N1b FAIL decisively → STRUCTURAL NEGATIVE: frozen discrete dLLM does not host a few-step-integrable embedding field despite near-ceiling full-NFE accuracy → publishable kill of the velocity-head program (do NOT spend training budget).

**Compute / hygiene:** ~5–15 GPU-h on 2×4090, reuse the existing gen+verifier harness. 32-problem DEV slice
FIRST to confirm the hook / no-NaN / tokenizer / verifier; do NOT tune K/schedule/snap/temp on the sealed
MATH-L5/AIME sets after that. Verify checkpoint integrity (7+5→12) on load. Do NOT kill the co-tenant GPU jobs.

**False-negative controls:** FN1 soft-OOD → run N1a/N1b, log embedding norm / nearest-token dist / cosine /
router-expert overlap (soft vs token); optional pre-declared norm-clamp ablation. FN2 wrong snap → snap_E
primary, snap_H separate. FN3 schedule → linear primary, cosine sensitivity, K fixed.
**False-positive controls:** FP1 crippled baseline → use Native-K-rescaled/subsampled, not early-termination.
FP2 hidden compute → report NFE + wall-clock + correct/sec, count all forwards. FP3 format/verifier artifact →
report parse-fail / no-box / wrong-box / truncation rates; subset where native-full is correct but capped-K
truncates/no-box; AIME once; no manual adjudication.

---

## RAW Pro response (provenance; math glyphs are mangled by text extraction — the contract above is authoritative)

(See session transcript chat "Model Audit and Design" for the rendered original. Verbatim extraction:)

Area-chair verdict — "Your exact slice is defensible, but only if you are disciplined about the claim …
A frozen, shipped, large discrete masked-diffusion LM can be externally probed for a decodable continuous
clean-data / average-velocity field in its tied embedding space, and the probe is judged only by verified
few-step generation, not diffusion loss or teacher-forced CE. G4 alone is probably workshop/Findings-level …
The G4 + N1 falsification package is stronger. A downstream learned adapter could be top-venue material only if
it converts the N1/G4 evidence into a robust few-step verified-generation gain under frozen-backbone
constraints." [Full PART A novelty table + PART B B1–B13 equations, pseudocode, baselines, N1a/N1b oracle,
thresholds, and FN/FP controls captured in the BUILD CONTRACT above.]
