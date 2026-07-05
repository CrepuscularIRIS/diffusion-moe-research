# DSpark — Core Architecture & Open Directions (2026-07-01)

> DSpark (arxiv:2606.19348, DeepSeek) = Confidence-Scheduled Speculative Decoding with Semi-Autoregressive
> Generation. Open-sourced 2026-06-27 as part of DeepSeek-V4. Training framework: **DeepSpec** (MIT,
> github.com/deepseek-ai/DeepSpec).

## Three-component architecture

| Component | What it does | Key detail |
|---|---|---|
| **Parallel backbone (DFlash)** | Generates base logits for all k draft positions simultaneously | Position-independent; fast but suffers suffix decay |
| **Sequential Markov head** | Adds prefix-dependent bias before sampling each token | 1st-order only (conditions on immediately preceding token); rank-256 low-rank factorization; near-zero overhead (+0.2-1.3% latency for 4→16 draft length) |
| **Confidence-scheduled verification** | Per-position acceptance probability → hardware-aware scheduler adjusts verification length by GPU load | Lossless (preserves target model's exact output distribution) |

## Performance
- Offline: accepted length **+26-31% vs EAGLE-3**, +16-18% vs DFlash
- Production (V4): per-user generation speed **+60-85%** (Flash), +57-78% (Pro) vs MTP-1

## The core insight: suffix decay
Parallel draft's acceptance drops for later positions because they're predicted without knowing earlier
tokens' actual sampled values. The Markov head fixes this by looking at the previous token and adjusting —
but only one step back (1st-order). DSpark acknowledged an **RNN variant tracking full prefix** showed
"marginal improvement" but shipped the Markov head for speed.

## Three transferable ideas (general, not model-specific)

### 1. Confidence head → selective verification
Predict acceptance probability per position → verify more tokens when spare compute exists; skip
low-confidence tails early. Hardware-aware: adapt to live GPU load.

### 2. Sequential correction beyond 1st-order Markov
The Markov head only conditions on the immediately preceding token — it is **under-modeled**. Higher-order
conditioning (2nd/3rd-order, attention-based, gated RNN) could capture longer-range intra-draft dependencies
and push accepted length further. **This is the primary open direction** (see `plan/archive/dspark-deep-analysis-2026-07-01.md`).

### 3. Suffix decay → structural intra-draft dependency
The deeper question: what dependency structure WITHIN a draft span matters most for acceptance? The answer
informs whether a Markov head, attention head, or structured prediction model is the right correction.

## Training (DeepSpec framework)
- Freezes target model, reuses embedding + output head
- Loss = **total-variation distance** (directly maximizes draft acceptance rate)
- Configs specify algorithm + target model; ~38 TB target cache for Qwen3-4B on 8 GPUs
- Supports training custom draft heads on any target model

## Open research direction (current goal)
**Beyond-first-order Markov sequential head for speculative decoding.** See `plan/goal-directive.md` and
`plan/archive/dspark-deep-analysis-2026-07-01.md` for the occupancy scan and candidate designs.
