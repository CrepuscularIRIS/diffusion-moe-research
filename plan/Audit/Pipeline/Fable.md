There's no secret system, but there is a surprisingly consistent set of habits that shows up across the most productive labs and researchers. What follows is a synthesis of what's publicly observable — from Karpathy's writing and talks, Kaiming He's paper trail, the internal cultures described by people who've worked at FAIR, DeepMind, and OpenAI, and the advice documents that circulate from top academic labs (Hamming's "You and Your Research," Schulman's "An Opinionated Guide to ML Research," Michael Nielsen's essays, the CMU/Stanford PhD guides). I'll flag where something is inference rather than documented practice.

## Problem selection: where most of the leverage actually is

The strongest recurring pattern is that elite researchers spend disproportionate effort choosing *what* to work on, and they select problems using a few repeatable filters:

**Work backward from a bottleneck, not forward from a technique.** Kaiming He's career is the cleanest example: ResNet came from asking "why can't we train deeper networks?" — a concrete, measurable obstruction everyone had hit. MoCo and MAE came from "why does self-supervised learning work in NLP but not vision?" The pattern is identifying a *gap between what should be possible and what is*, where the gap itself is the research question. Contrast this with the failure mode of "I know transformers, what can I apply them to?"

**Prefer problems where the null result is also informative.** Schulman's guide makes this explicit: good problems are ones where any outcome teaches you something. If your idea only pays off in the narrow case that it works, expected value is low.

**Ride a rising tide, but position slightly ahead of it.** Fei-Fei Li's ImageNet is the canonical case — she bet on data scale before the field valued it, when the prestige work was in clever models. DeepMind bet on RL + deep learning before it was fashionable. The observable heuristic: identify what the field will care about in 2–3 years, which is usually visible as a small but growing pain point in current papers ("we leave X to future work" appearing repeatedly is a signal).

**Simplicity as a selection criterion, not just an aesthetic.** He's papers are famous for being almost embarrassingly simple (MAE is "mask patches, reconstruct pixels"). This is a deliberate strategy: simple methods are easier to ablate, easier to reproduce, harder to dismiss as tuning artifacts, and become platforms others build on — which is what drives citations and influence. A useful test used informally at FAIR-style labs: "can you explain the core idea in two sentences to someone outside your subfield, and do they immediately see why it should work?"

**Avoiding incrementalism is mostly about the question, not the ambition.** Incremental work usually comes from accepting the field's problem formulation and improving a number. Non-incremental work re-formulates: it changes the evaluation, the assumption, or the framing. Karpathy's advice (paraphrasing his blog and talks) is that the "10x" projects look almost the same as the "1.1x" projects day-to-day; the difference was set at problem-selection time.

## Hypothesis formation and the pre-experiment discipline

**Write the paper skeleton before running the main experiments.** This is near-universal advice from productive labs (and explicit in Jacob Steinhardt's and Sasha Rush's guides). Not the full paper — the abstract, the claims, and the table shells with empty cells. This forces you to articulate: what claim am I making, what table would prove it, what would a skeptical reviewer's first objection be? Every experiment then either fills a cell or gets cut. This single habit kills more wasted compute than anything else.

**One hypothesis per experiment, stated in advance, with a predicted outcome.** The discipline that separates strong empirical labs from weak ones is writing down "I expect X because Y" *before* the run. If the result surprises you, that's signal — either your model of the system is wrong (interesting) or your code is wrong (common). Labs that skip this drift into "run stuff, look at numbers, tell a story afterward," which produces papers that don't replicate.

**The "minimum viable experiment" reflex.** Karpathy's public workflow (visible in nanoGPT, his "recipe for training neural networks" post) is emphatic here: before any real experiment, overfit a tiny batch, verify loss at init matches theory, visualize inputs right before they hit the model, establish that the pipeline can learn *anything*. He describes neural net training as failing silently, so the workflow is paranoid, incremental verification — never write a full system and then debug it end-to-end.

## Baselines and experimental hygiene

This is where top labs are most different from average ones, and it's boring on purpose:

**Tune the baseline as hard as your method.** The most common reason results don't replicate is an under-tuned baseline. He's papers are respected partly because his baselines are often *stronger* than the numbers in the original papers he compares against. The internal norm at strong labs is: if your gain disappears when the baseline gets the same tuning budget, you have nothing.

**Change one thing at a time, and keep a canonical config.** There's a "trunk" configuration that's known-good and version-pinned; every experiment is a named diff from trunk. Seeds, data order, and eval protocols are fixed. Multiple seeds for any headline number — at DeepMind-style rigor, a result that flips sign across seeds is not a result.

**Ablations are the argument, not an appendix chore.** The best papers use ablations to establish *mechanism*: which component carries the effect, does the effect scale, does it survive changing the dataset/architecture. A practical heuristic: your ablation table should be designed so that a reader could reconstruct your design reasoning from it — "we tried the obvious simpler thing, here's where it breaks, that's why the method looks like this."

**Failure analysis is scheduled, not incidental.** Strong empirical researchers look at raw model outputs and individual errors constantly (Karpathy: "become one with the data"). Aggregate metrics hide bimodal behavior, data leakage, and evaluation bugs. A recurring internal-lab practice: before believing a good number, actively try to destroy it — check for train/test contamination, check the metric implementation, check whether a trivial baseline gets most of the gain.

## Reading and idea generation

**Read shallow-wide by default, deep-narrow on demand.** Nobody productive reads most papers fully. The observable pattern: skim abstracts/figures of everything in your area (an hour-ish daily or a weekly batch), fully read only papers you intend to build on or beat — and *those* you read adversarially, reimplementing key parts. Karpathy has said the best way to understand a paper is to reimplement it; his career is partly a sequence of pedagogical reimplementations (micrograd, minGPT, nanoGPT) that doubled as research infrastructure.

**Maintain an idea backlog with cheap kill criteria.** Ideas are logged with a one-line hypothesis and a one-line "cheapest experiment that could kill this." Most ideas die in the doc, which is the point. Schulman's guide calls the alternative failure mode "idea churn" — hopping to a new idea every two weeks, which guarantees you never get past the stage where every idea looks bad (all ideas look bad at week 3).

**Ideas come mostly from friction, not from reading.** The consistent testimony from productive researchers is that their best ideas came from something breaking or behaving strangely in their own experiments, from teaching/reimplementing, or from conversations — not from a literature gap analysis. This is an argument for keeping hands on code even as you get senior.

## Collaboration structure

The recurring pattern across FAIR, DeepMind, OpenAI, and top academic labs:

**Small core, clear ownership.** Papers typically have 1–2 people who own the codebase and run everything, plus advisors/collaborators who contribute framing, red-teaming, and specific expertise. Diffuse ownership ("we'll all run experiments") is a known project-killer.

**Frequent short syncs, decisions in writing.** Weekly (often twice-weekly near deadlines) meetings where the unit of discussion is a plot or table, not a status narrative. Decisions and current hypotheses live in a running doc. OpenAI and DeepMind project culture, as described by alumni, is heavy on shared experiment logs and dashboards so anyone can inspect the evidence directly.

**Internal review as a real adversarial gate.** Strong labs run internal "red team" reads or practice talks 2–4 weeks before submission, where colleagues explicitly play Reviewer 2: attack the baselines, the claims-vs-evidence gap, the missing ablation. The papers you see from these labs already survived a harsher review internally. A grad student can approximate this by trading adversarial reads with 2–3 peers as a standing arrangement.

## Kill/scale decisions

**Time-boxed gates.** A common informal structure: 2 weeks to a first signal (does the minimum viable experiment show *anything*?), 6–8 weeks to a decision point (does the effect survive one scale-up and basic ablations?). At each gate the question is not "do I like this project" but "what evidence arrived since the last gate?" Sunk-cost is the dominant failure; the counter-habit is writing the kill criteria *at project start*, when you're not attached.

**Distinguish "kill" from "park."** Many famous results were parked ideas revived when a missing ingredient arrived (compute, a dataset, a trick from another paper). Parked projects get a one-page postmortem: what we learned, what would need to change to revive it. That doc is cheap and occasionally extremely valuable.

**Scale only after the small version is clean.** The pattern at compute-rich labs is still: prove it small, ablate it small, then scale — because scaling amplifies both effects and bugs, and debugging at scale is ruinously expensive.

## Writing and narrative

**Start writing at ~50% experimental completion, not 90%.** Writing exposes which claims lack evidence while there's still time to run the missing experiment. The intro and the main table are drafted first; the intro is rewritten most.

**The narrative is claim-first, not chronology-first.** The paper is not the story of what you did; it's the shortest path from a question the reader already cares about to a claim your tables support. The strongest openings (look at ResNet, Attention Is All You Need, MAE) state a puzzle or a simple bold claim in the first paragraph and put the headline evidence in Figure 1.

**One claim per paper.** Multi-claim papers dilute review scores and citations. If you have two results, that's usually two papers.

**Figure 1 gets absurd effort.** Reviewers and readers form their judgment from the abstract + Figure 1 + main table. Productive labs iterate on Figure 1 like a product.

## Anti-patterns (the negative space, equally consistent across sources)

- Tuning your method while leaving the baseline at default settings.
- Building a big system before verifying the pipeline can learn on a toy case.
- "Grad student descent": weeks of hyperparameter fiddling with no hypothesis, mistaking motion for progress.
- Reading for months as a way to defer the discomfort of running something.
- Novelty-by-complexity: adding components until reviewers can't dismiss it, which also means no one can build on it.
- Switching projects at week 3 because the idea "feels bad" (all ideas feel bad at week 3).
- Writing the paper in the last two weeks, discovering the missing ablation with no time to run it.
- Believing a good number without trying to break it.
- Solo hero mode: no adversarial feedback until the actual reviews arrive.

## A concrete operating cadence for a grad student

**Daily (research days):** One deliberate experiment with a written hypothesis and prediction; check results and update the running log; ~30–60 min of skimming new papers with one-line notes; end the day by writing tomorrow's first action so you don't start cold.

**Weekly:** A written review (30 min, for yourself): what did I learn, what died, what's the single most informative experiment I can run next week? One advisor/collaborator meeting anchored on a plot or table. One deep, adversarial paper read, ideally with partial reimplementation. Update the paper skeleton — move numbers into table shells as they arrive.

**Monthly:** A gate review against the kill criteria you wrote at project start: has evidence accumulated or just effort? Give one informal talk or writeup of current state to peers and collect objections. Prune the idea backlog; promote at most one idea to a 2-week probe if your main project has slack.

**Per project:** Week 0 — one-page doc: hypothesis, why now, minimum viable experiment, kill criteria, target venue, paper skeleton with empty tables. Weeks 1–2 — MVE and pipeline verification (overfit tiny data, sanity-check everything). Weeks 3–8 — core result + strongest-possible baseline; gate decision. Weeks 8–16 — ablations, robustness, failure analysis, scale-up; writing runs in parallel from ~week 8. Final 3–4 weeks — internal adversarial review, Figure 1 iteration, rebuttal-anticipation experiments (run the experiments Reviewer 2 will ask for *before* submission).

Two honest caveats. First, some of what makes FAIR/DeepMind/OpenAI output strong is compute, infrastructure, and dense peer quality — inputs you can only partially substitute (pick problems where your compute is sufficient; manufacture peer pressure via reading groups and paper-swaps). Second, survivorship bias is real: for every ImageNet-style contrarian bet that worked, many didn't, and the people above also produced parked and failed projects you never saw. The system above doesn't guarantee hits; it raises your shots-on-goal per year and the reliability of each shot, which is the only part actually under your control.