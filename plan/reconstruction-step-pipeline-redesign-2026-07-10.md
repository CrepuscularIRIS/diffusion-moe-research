# Reconstruction Step — `/prospect` Pipeline Redesign (2026-07-10)

> User directive: the classic spine **Decomposition → Simplification → Reconstruction** was missing its last
> step; "Research-OS is not meeting my expectations"; make model-proposed reconstruction/hypotheses first-class
> and investigate why the step is suppressed. This note records the diagnosis + the implemented fix. Worked
> example banked separately: `plan/aerial-world-model-reconstruction-2026-07-10.md` (aerial nav → data assimilation).

## Diagnosis — grounded in the actual `/prospect` SKILL (not a hunch)
The step wasn't absent; it was **demoted and gagged**:
- Decomposition ✓ (the five mines) · Simplification ✓ (latent-root compression) · Reconstruction ✗ — present
  only as **Mine 5 "cross-domain transplant," last & optional**, and framed *defensively* ("transplant the
  precondition-**check**"), i.e. import a mechanism A→B, not reformulate the problem AS a member of field A.
- **Discipline applied at generation time = the real gag.** To become a problem, a candidate must pass the
  NECESSITY GATE ("a failure surviving fair plain-LoRA + tuned prompting + data-scale + seed/OOD") + occupancy +
  WHY-EMPTY. A *reconstruction* has no benchmarked failure yet → killed at birth by gates meant for claims.
- The problem **card had no reconstruction field** (what isn't a field doesn't get produced).
- **MoA was told to "reconcile"** (converge to a consensus mechanism), never to reconstruct (diverge into a new
  discipline). The aerial record confirms: every panel converged on a mechanism *inside* aerial-navigation.

Root cause: the pipeline front-loads its (excellent) *filtering* discipline onto the *generation* stage, and
reconstruction — pure divergence — is the first casualty.

## Fix — Option 1 (minimal; no new command; flat parts budget)
Edits to `/home/lingxufeng/cli/research-os/skills/prospect/SKILL.md` (v1.0.0 → **1.1.0**; runtime synced to
`~/.claude/skills/prospect/SKILL.md`) + `moa/router-protocol.md`:
1. **Forced Reconstruction step** after latent-root compression: reformulate the compressed root into ≥2 other
   disciplines' native abstractions (field · canonical object · machinery unlocked). Pure divergence.
2. **Optional MoA reconstruction sub-step** (tiered, HIGH-VALUE only): each advisor reframes the SAME root into a
   DIFFERENT discipline; coordinator PRESERVES the divergent reframe-map, does NOT reconcile to one mechanism.
3. **Card field** `RECONSTRUCTION: <discipline : native object>`.
4. **Firewall:** NECESSITY GATE / occupancy / WHY-EMPTY apply in DEPTH at the CLAIM boundary only — never to a
   reframe at birth. A reframe dies only from "no differential prediction survives once developed."
5. **Mine 5 absorbed** into the Reconstruction step (its precondition-check retained as the discipline applied
   AFTER a reconstruction is chosen) — one-in/one-out, parts count flat.
6. **Ledger line** → `INCUMBENT FRAME = X · RECONSTRUCTIONS = <field:object>,… · candidate operators = p,q`;
   `moa/router-protocol.md` gains a **Reconstruction mode** section (diverge, preserve reframe-map, gates OFF).

## Anti-accretion guardrail (explicit, because we just fought process-over-product)
The fix is **generative** (one protected divergence step), NOT more filtering machinery. Deliberately avoided a
7th command and a superpowers spec-doc. **Watch-for:** if reconstruction becomes ceremony — reframes that never
reach a cheap probe, or a card that lists five disciplines and tests none — cut it back. The step earns its keep
only when a reconstruction produces a differential prediction + cheap probe that the incumbent frame wouldn't.
