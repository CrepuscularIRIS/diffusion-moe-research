# He-line first-shot objective design — S-MEx0 (Pro 扩展, 2026-06-30)

> Pro 扩展 (GPT-5.5 Pro) design for the Track-3 He-line first shot on LLaDA-8B-Instruct.
> NOT yet sealed — must pass `/taste-critic` + `/object-shift-audit` before it becomes a
> preregistered contract. Chat: "He-line目标函数设计".

## Verdict: first shot = **S-MEx0** (scaled Masked-Embedding clean-x0), not full ELF, not MeanFlow

Rationale: full ELF replaces the forward process + sampler + final discretization (not "only the
objective"); MeanFlow conflates objective-gain with one-step-sampling-gain (JVP, two time vars).
S-MEx0 = the LLaDA-minimal JiT clean-x0: change ONLY the masked-position target from CE to a
regression onto the **frozen output codebook** codeword; inference unchanged (still categorical).

## The objective (the ONLY change vs baseline)

At masked **response** positions, regress final hidden `h_i ∈ R^d` to a scaled, frozen clean-x0 codeword;
decode at inference still via `logits = h @ W0^T` (original readout). NOT naive `MSE(h, E[y])` (would
collapse the multimodal categorical posterior, desync decode, smooth 7-vs-8).

**Frozen codebook (critical control, BOTH arms):** freeze input-embedding + lm_head/output codebook in
baseline AND treatment (matched params; stops moving-target / codebook collapse). Trainable = all
Transformer blocks + final norm. **No new head.**

**Target construction (frozen `W0 = lm_head.weight` at init):**
- row RMS: `r_y = sqrt(mean(W0[y]^2) + eps)`  →  row-normalized `c_y = W0[y] / r_y`
- global scale: `a = (log V + 2) / (d * median_{y∉special}(r_y))`
- target: `u*_y = a * c_y`   (so `h≈u*` gives gold logit ≈ `log V + 2` → sharp enough readout)

**Primary loss (per masked pos i), 1/ρ-weighted like native LLaDA:**
- `L_x0(i) = (1/d) ||h_i - u*_{y_i}||^2`
- `L_margin(i) = mean_{j∈N_i} relu(m + z_ij - z_iy_i)`, `z_ij = h_i^T W0[j]`, `N_i = top-32 logits ∪ in-batch golds` (exclude gold/pad/mask), `m=2.0`
- `L = Σ_b Σ_{i∈M_b} w_i (L_x0 + β L_margin) / Σ w_i`, `w_i = 1/max(ρ_b, ρ_min)`, `ρ_min=1/L_resp`, **β=0.05**

**Baseline (matched):** same corrupted input / frozen codebook / trainable params, masked CE with the
same 1/ρ weighting: `CE(h_i W0^T, y_i)`.

**Grad-scale calibration (pre-registered, not tuning):** before training, on 32 fixed microbatches,
`s_grad = median||∇L_CE|| / median||∇L_SMEx0||`; treatment trains on `s_grad · L_SMEx0`. Loss-unit
normalization only; never looks at eval.

**Inference:** NO nearest-embedding. Original LLaDA sampler verbatim (same block size, semi-AR order,
steps/block, remasking, low-confidence rule, gen-length cap, prompt template, deterministic decode);
treatment differs ONLY in that hidden states were trained by the embedding-x0 loss.

## full-FT vs LoRA
Main thesis test = **full-FT** backbone (+ final norm), frozen embedding/lm_head. (clean-x0 must reshape
hidden geometry; LoRA could turn an objective failure into a false "adapter-capacity" failure.) bf16,
AdamW, ZeRO-2/3, grad-checkpointing, clip 1.0, identical LR/sched/warmup/wd/seeds/data-order/mask-replay.
LoRA is allowed ONLY for the cheap probe; a LoRA-only result is not the thesis test.

## matched-compute (pre-register)
Everything identical except the objective: base ckpt, tokenizer, train data (NuminaMath-hard deduped),
example order seed, template, max-len/packing, response-only masking, ρ~U(0,1) sampling, mask positions
(replayed), optimizer, LR sched, trainable-param mask, global batch tokens, optimizer steps, grad-accum,
precision/ckpt/ZeRO, eval prompt, sampler, diffusion steps/block, block length, gen cap, remasking rule,
math_verify version. FLOPs: S-MEx0 also does the masked-pos vocab matmul (hard negs) → ~CE FLOPs; if step
time differs >3%, also report GPU-hour-matched secondary (primary must not reverse under either). NO extra
params in the first shot.

## Pre-registered falsifier
- **Primary success:** `Δ = Acc_SMEx0 − Acc_CE ≥ 2.0 pp` on SEALED MATH-500 deterministic pass@1
  (≥10 more of 500 verified). Also report paired bootstrap / sign test; do NOT move the threshold.
- **Thesis-negative (any):** after full matched-compute, Δ<2pp; OR treatment only wins under a non-primary
  sampler/temperature/remask/CE-bridge change; OR proxy token metrics show embedding loss succeeds but
  decode rank/confidence collapses.
- **Strong mechanism falsifier:** embedding loss drops normally + held-out forced-denoise gold-token rank
  still >5pp worse top-1 than CE + Δ<2pp ⇒ continuous clean-x0 target does NOT convert to verified
  reasoning on this masked-diffusion substrate.

## Cheap 5%-budget go/no-go probe (before the full run)
`S_probe = min(1000 steps, 0.05·S_full)`, baseline+treatment synced (same data order, mask replay, steps),
on a held-out NuminaMath-hard proxy (stratified, 512–1024 problems, NOT MATH-500):
- **A forced-denoise token retrieval** (teacher-forced, ρ∈{.25,.5,.75,.9}): S-MEx0 top-1 not below CE by
  >5pp at ρ=.75/.9; top-5 not >2pp below; numeric/operator token top-1 not >3pp below; boxed-span top-1
  not >2pp below.
- **B confidence-remask correlation:** AUROC(correct vs confidence) ≥0.70 and not >0.05 below CE.
- **C proxy verified generation** (128–256 problems, full sampler): S-MEx0 verified ≥ CE−1pp; last-25%
  slope not below CE.
- **D embedding mechanism:** cos margin >0, gold median rank ≤3, p90 ≤20; gold rank drops as embed loss drops.

## Failure modes to watch
multimodal collapse (MSE↓ but top-1<CE, math symbols wrong); decode inconsistency (h≈u* but gold rank
high, confidence uncorrelated → early-commit wrong); math tokens smoothed (CE punishes 7-vs-8 hard, embed
regression sees neighbors → track numeric/operator-token accuracy separately); frozen codebook lowers
absolute acc (record a native CE full-FT sanity ref, NOT the matched baseline); margin sneaking in as
classification (pre-register β=0.05/m=2.0/top-32; β=0 is a diagnostic only).

## ⚠️ Substrate correction to verify FIRST
Pro: HF LLaDA-8B-Instruct config shows **`weight_tying=false`** → use the ACTUAL `lm_head`/`ff_out.weight`
as the codebook `W0`, NOT the input embedding. MUST verify the local checkpoint's tying + exact param
names before implementing.
