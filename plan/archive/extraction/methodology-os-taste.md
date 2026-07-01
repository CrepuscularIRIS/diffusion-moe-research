# Methodology OS — Taste-Layer Extraction

> Extracted 2026-06-29. Focus: problem-selection, research taste, "what's worth doing," reframing, when-to-quit, reading-for-taste.
> Defer paper-writing content entirely. Cite by local path or external anchor.

---

## 1. Concrete Taste Heuristics Worth Lifting Verbatim

### 1.1 John Schulman — "An Opinionated Guide to ML Research"
Source: `/home/lingxufeng/research/scientist/research-methodology-os/research-advice/opinionated-guide-to-ml-research/README.md`

**Problem-selection questions (from conceptual contribution frame):**
> "What is new? (What is the novel insight?) / So what? (Why is it important? What implications does it have?) / Why so? (What are the justifications?) / Well done? (Is it complete and not brittle?) / Why now? (Is it timely?) / Who cares? (Is it relevant to broader audiences?)"

**Goal-driven vs. Idea-driven distinction (most important structural heuristic in the guide):**
> "Goal-driven research begins with a desired outcome or target capability (e.g., make X work for the first time). ... Idea-driven research begins when reading an existing method inspires an idea for how to do X even better."

Key warning:
> "Since your perspective may be similar to that of others reading the same literature, there is a high risk of being scooped or duplicating someone else's work." [idea-driven risk]

**When-to-pursue filter — complexity-impact test:**
> "Complexity must be justified by impact. For example, a minor improvement over the baseline (which is often the case if you are working on an incremental idea) should come from a method that is straightforward to implement."

**When-to-set-goals correctly:**
> "A goal should be high enough (i.e., in a way that has an important and long-term vision) so that you could do several incremental work towards achieving that goal."

**Generalizability test (a taste screen, not a method test):**
> "Would my empirical results transfer to other settings, contexts, or populations?"

---

### 1.2 Mila Research Tips
Source: `/home/lingxufeng/research/scientist/research-methodology-os/tips-research-mila/README.md`

**Reading-for-taste / ideas-worth-pursuing protocol:**
> "A crucial skill you will learn to develop is to identify (and shape) ideas worth pursuing. You can do this by drafting them as if writing a paper, including mathematical definitions, assumptions, hypotheses, and potential results. This process will help you uncover gaps in the ideas and give you an estimation of the necessary work, before even starting experiments."

**Research taste as the primary first-year goal (not paper count):**
> "The main goal in your first year is to develop a research taste. This means finding something that you have an unhealthy research obsession with and more importantly one that you have the skillset (or can develop the skillset) to tackle. This is the key to doing great work. See Paul Graham's essay on this topic."

**When-to-quit signal:**
> "Be wary of the sunk cost fallacy. Stop when you're not progressing (with caveats, e.g. try to understand why). Give yourself time limits. Don't give up too quickly, but do give up at some point (finding this balance is where your supervisor(s) and senior colleagues should be consulted)."

**Ego as an anti-taste force:**
> "Ego can be an enemy of scientific progress: we need to keep our mind flexible, be willing to change our opinion in the face of evidence, the arguments we are given."

**Downtime ideation note (attributed to Goodfellow's GAN story):**
> "A lot of research ideas come out during downtime (e.g. GANs came to Ian Goodfellow while he was having a beer with friends), provided that you've prepared your mind for these ideas to grow."

---

### 1.3 Hamming — "You and Your Research" (external anchor; local repo points to it)
Sources: `tips-research-mila/README.md` (YouTube link); `awesome-phd-advice/README.md` (text link); `Research-ScientificWriting/README.md` (text link); `README.md` L82 ("科研问题选择和长期研究品味")

No verbatim local copy. The repo README tags it as: "科研问题选择和长期研究品味" (problem selection and long-term research taste). The external essay's canonical taste heuristics (from the source itself, external anchor):

- **"Important problems" question**: "What are the important problems of your field? ... If you don't work on important problems, it's unlikely you'll do important work."
- **Adjacent possibility heuristic**: Work on problems where the field is ripe — where you can see a path from today to a result in 5–10 years.
- **Preparation + luck**: "Luck favors the prepared mind." Taste is cultivated, not inherited.
- **Closed-door heuristic**: If you keep the problem door open in your subconscious — "work in the cracks" — you keep returning to it. That returning is a taste signal.

The plan/ideas-* files in our project apply Hamming as "Q4 Hamming = YES/NO" — checking whether the candidate problem is genuinely important (not merely doable), which is exactly the intended usage.

---

### 1.4 Chris Olah — "Research Taste Exercises" (external anchor)
Source: `README.md` L80 ("直接训练 research taste，适合转成 taste gate exercises"); `deep-research-report (2).md` L13, L36, L112, L212

No local copy. Key heuristics captured in our deep-research-report synthesis:

- **Taste definition**: "Olah 直接把 taste 定义为「选择好问题的能力」" — taste is *problem-selection ability*, not execution ability.
- **Imagined paper heuristic**: "若别人发了这篇，你会真正想读吗？" (If someone else published this paper, would you actually want to read it?) — cited as the operational taste filter for the problem-discovery phase.
- **Cheap proxy feedback**: Taste is trainable via fast cheap feedback loops, not just by doing big projects.
- **Taste as decomposable**: The report derives 10 checkable dimensions from Olah's framing (see §3 of this doc for the mapping).

---

### 1.5 Keshav — "How to Read a Paper" (external anchor)
Sources: `research-advice/README.md` L19; `awesome-phd-advice/README.md` L164

No local content beyond the link. The repo's README marks it as "读论文流程，可转成 literature triage protocol." Key taste-relevant operational heuristics from the essay itself:

- **Three-pass method**: (1) scan for category/context/correctness/contributions in 5 min; (2) read with attention to figures/graphs; (3) re-implement to understand deeply.
- **Pass 1 as a taste filter**: The first pass can tell you whether a paper is worth deeper reading *before* you invest time — this is the "reading-for-taste" application.
- **Five C's of Pass 1**: Category, Context, Correctness, Contributions, Clarity. These map onto problem-selection tests: is the contribution real? Is the problem well-defined?

---

### 1.6 Our own deep-research-report synthesis
Source: `/home/lingxufeng/huggingface/plan/deep-research-report (2).md` (Chinese, full report)

**What a "fundamental problem" looks like (4-property test):**
> "一个「基础问题（fundamental problem）」通常满足四个性质：它挑战领域默认假设；能被一句简单语言精确定义；存在明确反事实或杀手实验；无论结果正负都能改变我们对机制的理解。"

Translation: (1) challenges a default domain assumption; (2) can be precisely defined in one simple sentence; (3) has a clear counterfactual or killer experiment; (4) regardless of outcome (positive or negative), changes our understanding of the mechanism.

**"Is X necessary?" as the canonical problem-reframing move:**
The report's 10-pattern table (L48–62) shows this is the most high-frequency Kaiming He-style move. The reframing template:
- Identify a component/assumption the field takes for granted (default assumption).
- Ask: "If we remove X, does the phenomenon still hold? If not, why?"
- Design compute-matched falsification (the falsification must control for data/compute — not just "we removed X and it got worse").

**Problem-discovery pipeline (the 7-class taxonomy for candidate problems):**
> "把问题分成 fundamental / engineering / evaluation / dataset / scaling / mechanism / deployment 七类" — Every candidate should be classified before investing; "fundamental" and "mechanism" are the highest-taste classes.

**Problem-compression as a taste signal:**
> "能把一个流行工程套路重写成一句更基础的问题句" — the ability to rewrite a popular engineering recipe into a more fundamental question sentence is itself a taste signal.

---

## 2. Mapping: Taste Card 8 Points → Canonical Source Heuristics

The Taste Card 8 fields (from `plan/ros-review/codex-C-wiring-and-demo.md` L56 and `plan/research-operating-system.md` L47–59):
`field belief · bottleneck · clean reformulation · minimal system · killer experiment · anti-reward-hack rule · understanding gain · title test`

| Taste Card Field | Canonical Source | Heuristic Being Applied |
|---|---|---|
| **1. Field belief** (what the community currently assumes) | Hamming "important problems" + Schulman goal-driven frame | Hamming: name the open important problem. Schulman: start from the desired outcome, not from what the literature says. The field belief is the default assumption to be challenged. |
| **2. Bottleneck** (what's blocking progress) | Schulman goal-driven research; deep-report "dominant assumption / hidden dependency" | Schulman: "experimenting with existing methods; when these prove insufficient, the researcher develops new methods." The bottleneck is why current methods fail on the goal. |
| **3. Clean reformulation** (one-sentence testable question) | Olah taste; Mila "draft as if writing a paper"; deep-report L8 | Olah: taste = selecting good problems; the clean reformulation IS the taste output. Mila: "drafting as if writing a paper... helps uncover gaps." Deep-report: "能被一句简单语言精确定义." |
| **4. Minimal system** (smallest instantiation that tests the thesis) | Deep-report "back to basics" pattern; He-line MAE/JiT/MoCo | "问最简单能工作的东西是什么." He-line: always compress to smallest mechanism before adding parts. Cheap falsification: "1–3 days, small model, subset, synthetic data." |
| **5. Killer experiment** (one experiment that falsifies the core claim) | Hamming "preparation + adjacent possibility"; deep-report cheap falsification; Schulman "Why now?" | Deep-report: "设计能最快杀死关键假设的实验，而非最快出正结果." The Schulman "Why now?" question is answered by whether the killer experiment is newly runnable. |
| **6. Anti-reward-hack rule** (how we prevent optimizing the proxy) | Our ROS (research-operating-system.md §0 + §1) — Goodhart principle | This field is largely *our own contribution*, not directly from Schulman/Mila/Olah/Hamming. The canonical closest anchor is Hamming's implicit warning against prestige-seeking over truth-seeking. Olah's "cheap feedback" implies the feedback must not be gameable. |
| **7. Understanding gain** (what we learn even if result is negative) | Deep-report L8: "无论结果正负都能改变我们对机制的理解"; Mila "fail but understand why" | Mila: "Stop when you're not progressing (with caveats, e.g. try to understand *why*)." Deep-report: negative result informativeness is a full scoring dimension. |
| **8. Title test** (could this be a real paper title?) | Olah "imagined paper heuristic" | Direct mapping: Olah's question "若别人发了这篇，你会真正想读吗?" is the exact taste exercise the title test operationalizes. |

**Weaknesses in our Taste Card vs. canonical sources:**
- **Missing: generalizability screen** (Schulman: "Would my empirical results transfer to other settings?") — our card has "minimal system" but no explicit transferability check. The 10-dim rubric has it (dim 9: cross-setting transferability) but the Taste Card 8 does not.
- **Missing: "Why now?" temporal readiness test** (Schulman). We have "killer experiment" but not the question of whether the field is *ripe* for this problem today.
- **Missing: "Who cares?" external-decision test** (Schulman's "Who cares?" + our ROS external-decision stub). The Taste Card has no field for naming a concrete decision-maker. The external-decision stub exists separately in the ROS but is not embedded in the Card.
- **Anti-reward-hack rule is unique to us** — it has no canonical counterpart in Schulman/Mila/Olah/Hamming. This is the OS's own novel contribution.

---

## 3. What Canonical Taste Literature Says That Our Taste Gate Is Missing

### 3.1 Schulman: "Seek advice from experienced researchers when *choosing* problems"
Schulman says: "Seek advice from experienced researchers when choosing problems to pursue. They may suggest many ideas, but ideas are cheap. Your job to decide which ones are worth pursuing and how to execute them effectively."

**What we're missing**: The Taste Card is a *self-administered* checklist. Canonical advice says taste judgment should include a peer/senior's read — not just the proposer's. Our gate says "human decision" but doesn't specify *whose* human — the proposer can be the human. Schulman implies a more adversarial external input ("they suggest many ideas; you must decide") which our system mostly routes to Codex, not to a human senior colleague.

### 3.2 Hamming: Long-term problem horizon ("work in the important problems of your time")
Hamming tests are being applied to individual experiments in our project (Q4 Hamming = YES/NO). But Hamming's original point is about *career-level* focus: repeatedly returning to the same important problem over years. Our taste gate has no longitudinal signal — it doesn't ask "Is this problem central enough that I'd want to return to it for 3+ years?"

### 3.3 Olah: Taste is trained by doing many small exercises with fast feedback
Olah's operational point (from "Research Taste Exercises"): you improve taste by deliberately practicing with cheap proxies — reading papers and asking "would I want to read this?" for many papers quickly. Our system has no taste-*training* loop. The Taste Card is a gate, not a training regimen. Olah says the gate improves through practice volume; we have no mechanism for that.

### 3.4 Mila: "Unhealthy obsession" as a taste signal
> "finding something that you have an unhealthy research obsession with" — this subjective emotional signal is missing from our Taste Card. None of the 8 fields capture "do you find yourself thinking about this when you're not working?" This is a weak but real prior that correlates with sustained engagement.

### 3.5 Schulman + Mila: Goal-level vs. problem-level distinction
Our card operates at the problem level (one candidate problem at a time). Schulman says the *goal* should be set high enough for "several incremental works." The Taste Card doesn't ask: "Is this problem a subset of a larger goal I've already taste-approved?" — i.e., are we doing tactical problem selection within an approved strategic direction, or are we taste-gating the strategic direction itself? The ROS §3 does distinguish tactical vs. direction-level (Codex can SELECT tactically; human must SELECT paper-aiming directions), but the Taste Card itself doesn't encode this.

---

## 4. The Single Most Important Operational Taste-Training Exercise

**The Imagined-Paper Exercise (Olah, operationalized for human gate use):**

For each candidate problem, perform the following ritual *before* filling in the Taste Card:

1. Write a two-sentence abstract for the imagined paper (what you'd want to claim, if you succeeded).
2. Ask: "If a strong researcher I respect published this paper — not me — would I genuinely want to read it? Or would I skim and move on?"
3. Ask: "Is my honest answer driven by the problem, or by my sunk cost / familiarity / proximity to existing results?"
4. Ask: "Would this paper title appear on a list of the 10 papers I most wish existed in this subfield right now?"

If the answer to question 2 is "I'd skim," stop. Do not fill in the Taste Card. Kill the direction now.

**Why this is the most important**: It externalizes the taste judgment. Instead of asking "is my research good?" (which triggers defensiveness and sunk-cost bias), it asks "would I read someone else's version of this?" This is cognitively much harder to self-deceive on. Olah identifies this as the core taste exercise because it decouples *problem value* from *proposer identity* — which is exactly the Goodhart risk our OS is designed to prevent.

**How to anchor it to the human gate**: The exercise must be done *before* any experiments are run (pre-registration moment). The human decision at the taste gate should reference the two-sentence abstract, not the post-hoc story. If the abstract written after seeing preliminary results is materially different from the one written before, that gap is itself evidence of drift — log it in the pivot ledger.

---

## 5. External Anchors (No Local Copy; Reference Only)

| Source | Taste-Relevant Content | Local Reference |
|---|---|---|
| Olah, "Research Taste Exercises" (2021) | Taste = problem-selection ability; imagined-paper heuristic; cheap feedback training | `README.md` L80; `deep-research-report (2).md` L13, L36, L112 |
| Hamming, "You and Your Research" (1986/1995) | Important-problems question; closed-door heuristic; preparation + luck | `tips-research-mila/README.md` L9; `awesome-phd-advice/README.md` L158; `README.md` L82 |
| Schulman, "Opinionated Guide to ML Research" (joschu.net) | Goal-driven vs idea-driven; complexity-impact test; generalizability screen | `research-advice/opinionated-guide-to-ml-research/README.md` (full takeaways) |
| Keshav, "How to Read a Paper" | 3-pass as a taste filter; Pass 1 = 5-min worthiness screen | `research-advice/README.md` L19; `awesome-phd-advice/README.md` L164 |
| Paul Graham, "Great Work" (linked from Mila tips) | Obsession as a taste signal | `tips-research-mila/README.md` L249 |
