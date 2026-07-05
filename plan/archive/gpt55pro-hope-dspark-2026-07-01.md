# GPT-5.5 Pro design — O1 = HOPE-DSpark (Higher-Order Prefix Encoder head) — 2026-07-01

> Pro designed (10m thinking + research); Opus packaged. NOT self-certified — eligibility from /object-shift-audit.
> Arbor run: dspark-head, node 1. Chat: chatgpt.com/c/6a44fcb9-1fd8-83ea-b324-cb4b75c7baa5

## Recommendation: O1 = HOPE-DSpark, a residual higher-order prefix-sketch head

NOT a generic RNN. A residual, gated, higher-order correction ON TOP of the existing Markov head.

**HOPE-DSpark: Higher-Order Prefix Encoder head** — conditions position k on:
1. the previous sampled token (preserving DSpark's Markov path)
2. the previous two-token pair (capturing cheap trigram/code-pattern effects)
3. a tiny causal attention sketch over the sampled draft prefix (longer-range intra-block consistency)
4. DFlash position features and entropy (correction fires mostly where parallel drafter is uncertain)

All higher-order terms emit **low-rank coefficients into the same vocabulary-bias basis** U used by the
Markov head. The expensive V×r multiply is reused — only the coefficient computation changes.

## 1. Specific O1 architecture

Let B = draft block length (5-16), x0 = last verified context token, x1...xk-1 = sampled draft tokens.
ℓD_k ∈ R^V = DFlash logits for position k, hD_k = DFlash hidden feature before LM head.

DSpark Markov baseline: `ℓ_k = ℓ_k^D + U·a_1(x_{k-1})`

HOPE-DSpark: `ℓ_k^HOPE = ℓ_k^D + U·[a_1(x_{k-1}) + g_k ⊙ (W_p·p_k + W_c·c_k)] + b_k`

Where:
- **A. Markov path** a_1(x_{k-1}): initialized from trained DSpark Markov head (warm start)
- **B. Pair path** p_k: factorized bigram feature from (x_{k-2}, x_{k-1}) via learned pair MLP (hidden=128)
- **C. Prefix attention** c_k: tiny causal attention (1-2 heads, dim=64) over sampled draft prefix buffer
- **D. Entropy gate** g_k = σ(w·[entropy(ℓD_k), margin(ℓD_k), hD_k projection] + bias): gate initialized
  with bias=-5 so higher-order path is initially OFF; model learns to turn it on where DSpark is uncertain

Parameters: prefix_attention_heads=1-2, prefix_attention_dim=64, pair_MLP_hidden=128, prefix_window=8,
output_basis_U=reuse DSpark Markov basis. Only a few MB additional parameters.

## 2. Integration with DSpark's DFlash backbone

DFlash remains the parallel backbone (one forward pass for all block logits + hidden states).

Runtime loop:
```
Input: verified context C
DFlash forward: produce ℓD_1...ℓD_B and hD_1...hD_B
prefix buffer: initialize with last m verified context tokens
for k in 1..B:
    compute Markov coefficient a1(x_{k-1})
    compute pair feature p_k from x_{k-2}, x_{k-1}
    compute prefix-attention feature c_k over sampled prefix buffer
    compute gate g_k from DFlash entropy/margin/hD_k
    compute final logits: ℓ_k = ℓD_k + U[a1 + g_k(Wp·p_k + Wc·c_k)]
    sample x_k ~ softmax(ℓ_k)
    append x_k to prefix buffer
return draft x_1...x_B and draft probabilities
```

Per-position overhead: one pair-MLP eval + one tiny attention over ≤B+m tokens + gate. All O(1) in vocab
size (the V×r multiply is shared with DSpark). Target: <5% per-round latency increase.

## 3. Training inside DeepSpec

Loss: same as DSpark — 0.9×TV(draft, target) + 0.1×CE + confidence loss + exponential position decay.
The higher-order head must be trained on sampled prefixes it will see at inference.

### Prefix schedule
```
Phase 0: DPC only, no new head training
Phase 1: head-only residual training
    freeze DFlash backbone, freeze/lightly-tune existing Markov basis U
    train pair path + prefix-attention path + gates
    80% teacher-forced target prefixes, 20% DSpark-sampled prefixes
Phase 2: mixed-prefix TV training
    50% teacher-forced, 50% HOPE-sampled prefixes
    target model frozen, DFlash frozen for first run
Phase 3: optional joint fine-tune
    unfreeze Markov coefficients and final draft projection
    keep DFlash backbone mostly frozen, low LR, strong residual regularizer
```

**KEY INSIGHT (why RNN was "marginal")**: Exposure bias. The RNN was trained with teacher-forced (correct)
prefixes but tested on DSpark-sampled (potentially incorrect) prefixes. HOPE fixes this with 50% sampled-
prefix training in Phase 2.

### Regularizers
- L2 on higher-order residual: λ_r ||g_k(W_p·p_k + W_c·c_k)||²
- KL/TV-to-DSpark warm-start term for first few thousand steps
- Higher-order path starts near zero (gate bias=-5) and only grows if it helps

## 4. DPC: Draft Prefix Conditionality probe

Three probes, run BEFORE training:

**Probe A**: For each position k>1 in DSpark Markov drafts, measure TV(target(x_k | x_{<k}), target(x_k | x_{<k} with x_{k-2} swapped)). If swapping x_{k-2} changes the target distribution, 2nd-order info exists.

**Probe B**: Same with different earlier sampled prefixes. If the target changes materially when only earlier draft prefix changes, Markov head is leaving signal on the table.

**Probe C: Offline acceptance replay**: Use top-K corrected DSpark distribution to rescore, compute expected
accepted length E[τ] ≈ Σ_{k=1}^B Π_{i=1}^k α_i, with α_i = Σ_v min(p_i(v), q'_i(v)).

### DPC pass threshold (at least one):
- ≥2-3% relative TV reduction on suffix positions k>4
- ≥0.05-0.10 expected accepted-length gain in offline replay
- ≥0.02 AUC improvement for predicting suffix rejection after conditioning on previous token
- clear gains on code/math, even if chat is flat

If DPC is flat → 1st-order already captures most useful intra-head information → do not train.

## 5. Falsifiers
1. **DPC fails**: no higher-order TV signal in suffix positions
2. **Latency exceeds 5%**: head too expensive → remove prefix attention, keep only pair path
3. **No accepted-length gain ≥3%** relative over DSpark Markov after matched training
4. **Only wins with different verification length/confidence thresholds** → not a drafter improvement

## 6. DeadlineBox rival: PairMarkov-Hash
DSpark Markov + hashed previous-two-token correction. A scalar entropy gate. No attention, no learned MLP.
May capture most gain if missing info is trigram-like (code punctuation, formatting, brackets).
If HOPE cannot beat PairMarkov-Hash at matched latency, HOPE is overdesigned.

## 7. Honest closest rival
**TreeFlash**: Parallel AR-Approximation for Faster Speculative Decoding, arXiv:2606.03819. Targets same
causal-conditioning failure. Adds MLP conditioned on drafter hidden + prev token with one-shot complexity.
But tree-oriented, not single DSpark linear-chain prefix head.

**Hydra** (arXiv:2402.05109): sequentially dependent draft heads for Medusa. Multi-head architecture,
distinct from DSpark's single sequential correction head.

## 8. If this fails → jump target
**Pathwise-TV DSpark Markov training**: keep 1st-order Markov architecture, retrain with on-policy sampled
prefixes and pathwise accepted-prefix weighting. Tests whether DSpark's "marginal" RNN result was
capacity-limited (then HOPE would help) or training-mismatch-limited (then pathwise-TV fixes it without
adding parameters). Adds zero inference latency.

## Pro's bet
HOPE's pair path will give most of the improvement, prefix attention will help mainly on code/math, and a
generic RNN will remain marginal unless trained on sampled prefixes.

## Opus packaging notes
- author_engine: leap=Pro (GPT-5.5 Pro 扩展), packaging=Opus; self_certified=false
- Closest rival: TreeFlash (arXiv:2606.03819)
- FORBIDDEN cleared: NOT dLLM/DiffusionGemma/LLaDA; NOT He-line; NOT compute-allocator
