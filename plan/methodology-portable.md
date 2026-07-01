# Portable Research Methodology — extraction & cross-domain transfer

> Extracts the domain-agnostic core from `research-method-anatomy.md` (personal cognitive
> protocol) + `ai-research-conduct-principles.md` (science-conduct kernel) + `research-goal.md`
> / `.claude/CLAUDE.md` (operational infrastructure), and shows how it transfers to a second
> domain. Source docs were extracted FROM the DiffusionGemma project; this doc lifts them OUT
> of it so the same engine can drive any research domain.

---

## 0. How the methodology was extracted (the meta-method)

The two methodology docs are not invented — they are **reverse-engineered from real evidence**.
This is itself a reusable extraction recipe:

1. **Anatomize real moves as evidence.** `research-method-anatomy.md` cites actual conversation
   turns ("难道 diffusion 一定比不过 moe 吗", "NuminaMath 为啥需要这个数据集") and names the
   cognitive operation each one performs. *Evidence-first, not aspiration.*
2. **Abstract to named operations.** Each recurring move becomes a first-class, nameable
   operation (质疑 / 跨域映射 / 第一性原理 / 可证伪 / 目标锚定).
3. **Distill the engineering framework to its kernel.** `ai-research-conduct-principles.md`
   takes the Experiment/agora-contract scaffolding and **strips all engineering** to leave the
   8 behavioral kernels + the root axiom.
4. **Compile to a loadable protocol.** Both docs end in a copy-paste **prompt protocol**
   (anatomy §5, principles §4) — the methodology becomes a "思考操作系统" you load at session start.

> To extract from a NEW project: collect the turning-point moves → name the operation each
> performs → strip the project-specific scaffolding → compile to a loadable protocol.

---

## 1. The three-layer stack (all domain-agnostic)

### Layer 1 — Cognitive protocol (*how to think*, from `research-method-anatomy.md`)
The 5-step loop, falsify-before-build:
1. **质疑 / Skeptical Default** — make *acceptance* the thing that needs a reason; trace every
   claim to first-hand grounding. ("接受本身设为需要理由的状态")
2. **跨域映射 / Cross-Domain Structural Mapping** — find a *structural* isomorphism to a mature
   field and borrow its validated tools; **also write down where the analogy misleads**.
3. **第一性原理 + 奥卡姆 / First-Principles + Occam** — strip to the basic quantities
   (information / probability / compute budget) and rederive; elegance = fewest moving parts.
4. **可证伪 / Falsifiability-First** — find the counterexample *before* building; every idea
   ships with the experiment that would kill it.
5. **看结果 / Results-Only Judgment** — the result is the only judge; never defend a pretty story.
   Plus **目标锚定 / Goal Re-anchoring** — pull attention back to the real target when diverging.

### Layer 2 — Science-conduct kernel (*what counts as evidence*, from `ai-research-conduct-principles.md`)
Root axiom: **failures → observable mechanism variables → before code mutation.** Then 8 kernels:
falsifiable-over-correct · evidence ≠ retrieval/memory/intuition · score-up ≠ mechanism (sealed
eval) · stronger-claim-more-control · one-variable-at-a-time · failure must shrink the search
space · multi-perspective must be *isolated* (no self-endorsement) · **experiment has absolute
veto over elegance** (kernel ⑧, the highest rule — kills sunk-cost / aesthetic-attachment /
frame-lock). One-line purpose: *make AI (and the human) unable to lie to itself.*

### Layer 3 — Operational infrastructure (*who runs it*, from `CLAUDE.md` + `research-goal.md`)
- **Multi-engine routing (isolation = credibility):** Opus (ideate/build) · Codex GPT-5.5
  (SELECT/DECIDE/diff-review — *independent model*) · Playwright→GPT-5.5-Pro / DeepResearch
  (deep design + novelty audits). Generator ≠ critic ≠ selector, by different reasoning substrates.
- **Arbor loop:** Idea Tree (MCP) · worktree isolation · sealed dev/test · merge guard · 6-step
  cycle (OBSERVE→IDEATE→SELECT→DISPATCH→BACKPROP→DECIDE).
- **Per-cycle review (7 checks):** direction-drift · hypothesis-fidelity · blocking · evidence-
  quality · compute-budget · novelty-integrity · **review-debt**.
- **Peer-review gate:** 5 reviewer agents (R1 soundness, R2 significance, R3 novelty, R4 rigor,
  R5 clarity) + AC meta-review → a "Reject→Accept Action List" that becomes **review debt with
  priority over new ideas**.
- **Stop-hook / review gate:** an independent model reviews before a turn/session can end.

L1 and L2 are "the same thing from two views" (human intuition vs. executable framework); L3 is
the bandwidth that runs them at scale.

---

## 2. The 串联 — worked example: it already transferred to domain 2

The **CoT distillation-fidelity audit** (`cot-distillation-fidelity-audit/`) is a *different
domain* (LLM-judge auditing, not diffusion modeling) — yet every methodology element shows up,
which is the proof of portability:

| Methodology element | What it became in the distillation audit |
|---|---|
| 质疑 / skeptical default | Falsified the prior "Claude = closure gold standard"; chased the critique-density paradox instead of accepting it |
| 跨域映射 | Borrowed **information theory** (MI-collapse `I(critique;answer_change)`) and **graph centrality** (PageRank-Gini ICI) to score reasoning text |
| 第一性原理 | The **natural experiment** (same question, different teacher) as the irreducible clean contrast |
| 可证伪 + falsifier-first | Every hypothesis (H1–H5) shipped with a kill condition; CCS's flagship status was **killed** by Pearson −0.01 |
| 看结果 vetoes elegance (kernel ⑧) | The "method determines closure" story was **pulled back** when Codex caught the ⅔ length confound; CCS dropped despite being the "most ingenious" metric |
| isolation / multi-perspective | **5-judge fleet** + **4-agent adversarial verify** before publishing — generator ≠ critic |
| score ≠ mechanism | Refused to read CCR magnitudes as mechanism; required the length control + the paired design |
| review debt | The **Codex stop-review** flagged the .gitignore bug + report inconsistencies → fixed *before* ending, exactly as "review debt has priority" prescribes |

It ran *lighter* than the full Arbor loop (no Idea Tree, no worktrees), but the **kernel was
identical**. That is the串联: the engine is domain-independent; only the instruments change.

---

## 3. Instantiation template for domain N (load when starting any new research)

```
NEW-DOMAIN CONTRACT (fill before any experiment)
1. Target claim (one falsifiable sentence) + the experiment that would kill it.
2. The irreducible clean contrast (the domain's "natural experiment"): what is held
   fixed so only the variable of interest moves?
3. Cross-domain borrow: which mature field's validated tool maps here, and where does
   the analogy break?
4. Sealed layer: eval script / test set / baseline — declared and frozen now.
5. Evidence ladder: recipe(score) → mechanism(+neg-control+locality) → publishable(+holdout+novelty).
6. Engine routing: who ideates (Opus), who selects/decides independently (Codex),
   who audits novelty/does deep design (Playwright→GPT-5.5-Pro), who verifies before ship.
7. Kill conditions written NOW for every idea (kernel ⑧): the result that forces a cut,
   executed unconditionally.

Then run the L1 loop (质疑→映射→第一性原理→可证伪→看结果), gated by the L2 kernels,
on the L3 infrastructure. Every assertion tagged "how to doubt / how to falsify / how to test."
```

The scarce asset is not domain knowledge (that is bandwidth, outsourced to AI). It is this
**"systematically close every self-deception channel" discipline** — and it is the most
transferable thing you own.
