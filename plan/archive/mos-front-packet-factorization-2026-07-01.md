# mos-front packet — factorization-barrier improvement (DSpark × DiffusionMoE) — 2026-07-01

> The enrich / mos-front hand-off for the ACTIVE direction (Arbor tree **5.11**). **Occupancy-scan (F2.5) runs
> FIRST**; the Pro design (F4.5) fires ONLY if the slice is OPEN. Neither Opus nor Pro self-certifies →
> `/object-shift-audit`. This is OPTIMIZATION/IMPROVEMENT, not evaluation.

## The difficulty (OBSERVE target)
The **factorization barrier**: block-parallel denoising in DiffusionGemma-26B MoE predicts masked positions
quasi-independently, so committing many tokens per step degrades quality. DSpark patches it with a
**first-order Markov head** (a trained, lightweight intra-block dependency model) — *under-modeled*: a
first-order chain can't capture longer-range intra-block structure. The user's read: "DSpark only got to
Markov → there's still large room."

## The object-shift (enrich)
- **WRONG object O0** = per-position independent prediction over the block (given the current canvas).
- **RIGHT object O1** (to design) = the dependency-structured joint prediction the Markov head under-models — a
  cheap, **MoE-/routing-informed, higher-order** intra-block dependency head that lets the model reliably
  **commit further per step WITHOUT re-serializing** generation.

## Occupancy-scan FIRST (F2.5 — Opus + web + prior-art; MUST pass before any Pro design)
Is the "trained, beyond-Markov / MoE-native intra-block dependency head for GENERATION-QUALITY" slice **OPEN**?
Probe:
- DSpark's own Markov head — order / structure (the ceiling to beat).
- Discrete-diffusion joint-modeling prior-art: CoDD, ADJUST, ADAS, block-diffusion / semi-AR heads,
  any-order / energy / copula heads over the block.
- The project's own kills: tree 5.5 (M-PCRH committed-set joint), 5.9 (post-hoc joint axes), 5.10.3
  (factorization-for-reasoning) — **but** those are FROZEN post-hoc for REASONING-novelty; THIS is a TRAINED
  head for GENERATION-QUALITY (distinct goal + substrate). State the distinction or the direction dies here.
- Substrate-fit: does the MoE routing / multi-step trajectory carry usable dependency signal?
- **Decision:** OPEN → F4.5 Pro design. OCCUPIED / substrate-fail → `LATERAL_JUMP` (record the occupant), do
  NOT design.

## Pro design brief (F4.5 — fires ONLY if OPEN; Pro channel must be re-attached first)
Design ONE elegant **O1**: the cheapest structure that captures longer-range intra-block dependency and lets
the model commit further per step at equal-or-better quality. Return: (1) O1, one paragraph; (2) why it is
unoccupied + MoE-native; (3) a **Differential Prediction Contract** — pre-training, matched-control
failure-split: where does independent prediction commit *wrong* that O1 predicts *right*, with a
shuffled-dependency control + generic-difficulty control + the **DSpark Markov-head rival baseline**;
(4) the single decisive train+measure experiment.

## Metric / acceptance
Generation / verifier-based: **more tokens committed per step at matched verified quality**, OR **higher
verified quality at matched compute**, vs (a) the base sampler and (b) the DSpark Markov-head baseline. Must
SOLVE the difficulty (a real Δ), not merely measure it. diffusion-loss / reference-token = INVALID.
