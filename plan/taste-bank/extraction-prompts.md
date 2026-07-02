# Taste Refinery — extraction prompts + run config (staging)

> Stage-1 collection engine: **LDR (ldr-mcp) with MiniMax-M3** (after the MCP restart) — hybrid: LDR for
> breadth, Gemini DeepResearch for the long-tail deep-dig later. Design: `plan/taste-refinery-design-2026-07-02.md`.
> Search engines (no API key, long-tail-biased): **semantic_scholar · openalex · arxiv** (+ searxng general).
> Strategy: `parallel` or `source-based`, iterations 3–4.

## The 3 broad-casts (Stage 1 — run each via detailed_research)

- **A. AI/ML modeling-object shifts** — "field-changing ML/generative/representation ideas whose key was a
  change in the MODELING OBJECT (not a new module/benchmark): the incumbent object → the new object + its
  mathematical carrier. Prioritize cross-domain reusable; avoid pure SOTA tricks."
- **B. Scientific-computing / physics / applied-math modeling shifts** — same, in physics-informed ML,
  numerical methods, dynamical systems, optimal transport, statistical mechanics, control, coding/information
  theory. **Long-tail bias: operators famous in these fields that never crossed into ML.**
- **C. Robotics / VLA / world-model / multimodal-grounding modeling shifts** — same, in policy learning,
  world models, multimodal fusion, grounding, affordance.

## Prompt 1 — broad-cast (find episodes, NOT a survey)
```
I am building a "Modeling Taste Atlas" for AI/ML research. Do NOT write a normal survey.
Find 40–80 field-changing research ideas [in <domain>] where the key contribution was a change in the
MODELING OBJECT, not merely a new module or benchmark. For each case output:
1 work/method name · 2 domain · 3 incumbent modeling object · 4 new modeling object · 5 mathematical
carrier (latent var / residual / score / energy / vector field / graph / operator / transport plan /
causal graph / simulator residual / information bottleneck …) · 6 what complexity it removed/compressed ·
7 what new prediction/measurement the framing enabled · 8 why it became influential · 9 source links.
Prioritize cross-domain-reusable cases. Avoid pure SOTA tricks.
```

## Prompt 2 — extract Taste Operators (Fable/Opus, on the collected episodes + our /autopsy [ANOMALY] ledger)
```
You are not summarizing papers. You are extracting reusable research taste. Given these research cases,
infer the latent "Taste Operators" that could have generated them. For each operator produce:
operator_name · one_sentence_core_move · old_object_pattern · new_object_pattern · mathematical_frame ·
failure_signature (when should a researcher reach for it?) · core_simplification (what does it make
simpler?) · differential_prediction (an observable it predicts that the incumbent framing does NOT) ·
cheapest_probe (test before expensive training) · positive_examples · negative_examples/when it misleads ·
transfer_targets (VLA, MLLM, diffusion LLM, speculative decoding, multimodal fusion, OOD, dataset eval,
distillation, systems). Merge duplicates. DISCARD any operator with no differential prediction.
```

## Prompt 3 — adversarial audit (independent — Codex hook / fresh Pro; reuses the v0.7 DIFF-PREDICTION gate)
```
Act as an adversarial research-taste auditor. Kill weak operators. For each, check: 1 buzzword relabel? ·
2 remove the new vocabulary — does any prediction disappear? · 3 does it SIMPLIFY the object or add
formalism? · 4 cheap probe? · 5 applies beyond one historical example? · 6 too broad to guide action? ·
7 could it generate a concrete candidate in VLA / diffusion LLM / multimodal fusion / dataset eval?
Verdict per operator: KEEP (generative, falsifiable, reusable) / MERGE / ARCHIVE (good concept, not
directly generative) / KILL (vocabulary / no differential / no probe). Return a cleaned operator bank.
```

## The 10-step 套话 ladder (per case, to push the model to the TASTE layer — not CoT)
1 what does the field default to modeling? 2 what structure does that default omit? 3 to make it simpler,
what object would you switch to? 4 which mathematical frame is that? 5 what does it predict beyond the old
object? 6 cheapest test? 7 what result kills the frame? 8 which domains have isomorphic structure? 9 which
buzzword-transplants look like it but aren't? 10 compress to one Taste Card.

## Corrosion gate (entry rules — do NOT let it rot into a vocabulary menu)
An operator enters `operators.md` only if it has `incumbent→new object` + `core_simplification` +
`differential_prediction` + `cheap_probe`. No cheap_probe → `archive` only (never `/forge`). Explains one
case but can't transfer → `source-episodes.md`. Bare buzzword → KILL. **Final validator = generation:** on a
held-out problem (VLA fusion / diffusion-LLM joint-assembly / speculative-decoding correction), the card
must generate a killable candidate we would not otherwise have thought of.

## Output files (this dir)
`source-episodes.md` (raw, provenance) · `operators.md` (30–60 clustered, KEEP-only) · `anti-patterns.md`
(buzzword-transplants killed). **Connect-back to /prospect·/forge·/autopsy·/compass is ✅ SHIPPED in
research-os v0.8.0** (commit 1ac2c69; `/forge` step 3‴ retrieves from the bank). The live bank is
`opus-pass/operators.md` (21 ★); this dir is the provenance/recipe staging.
