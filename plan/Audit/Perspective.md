## A. Do elite researchers actually operate this way?

Mostly yes — but implicitly, compressed, and with an important difference in *texture* that's worth naming upfront.

Your framework is a faithful reconstruction of habits that are observable in strong work. The parts that map directly onto documented practice:

**Q1–Q3 (shared root cause, wrong object, more natural representation)** is the single most recognizable move in landmark papers. ResNet is exactly this: the field saw "deep nets degrade" as an optimization nuisance to patch (better init, better normalization, careful tuning); He reframed the object — learn residuals F(x) = H(x) − x instead of H(x) — and a family of patches became unnecessary. Word2vec, attention, diffusion models, MoCo all have this shape: many symptoms, one representational error. Strong researchers do ask "are these five failures actually one failure?" though they'd phrase it as "what's *really* going on here?" over a whiteboard, not as reverse abduction.

**Q4 (novel prediction)** is the most elite and most neglected question on your list. It's the Popperian filter: a reframing that only re-explains existing results is a terminology change; one that predicts something incumbents can't is a theory. Very few papers pass this, and the ones that do (scaling laws predicting performance at unseen compute; the lottery ticket hypothesis predicting sparse trainable subnetworks exist) become field-defining. Most researchers, even good ones, skip this question — they check that the new framing is *consistent* with evidence, not that it's *discriminating*.

**Q5 (cheapest discriminator)** is a genuine tacit norm at compute-rich labs, ironically. The internal reflex is "what's the fastest thing that could kill this?" — a probe on a frozen model, a log dive, an oracle experiment where you inject ground truth to upper-bound the possible gain. Oracle probes especially are an elite habit: before building a retrieval system, check what happens with perfect retrieval. If the ceiling is +0.5%, stop.

**Q6, Q7, Q11 (prior-art collision, baseline self-attack, artifact audit)** are the internal-review culture of FAIR/DeepMind-style labs made explicit. Strong researchers run a simulated Reviewer 2 continuously, and the very strong ones attack their own result harder than any reviewer will — leakage checks, seed variance, tuning-budget parity. This is real and documented in how these labs' papers preempt objections.

**Q8–Q10, Q12 (mechanism necessity, predicted slices, upstream vs. downstream, invariants)** is where you're describing the top decile rather than the median of elite. Most published work, even at top venues, does *not* do mechanistic slice prediction ("if my mechanism is real, the gain should concentrate on slice X and vanish on slice Y"). The researchers who do — the empirical-science-of-deep-learning crowd, mechanistic interpretability, the best analysis papers — produce disproportionately durable work. So this part of your framework is aspirational-but-correct: it's what the best work looks like in retrospect, not what most strong researchers explicitly do prospectively.

**Q13 (negative space)** is real but rarer, and it operates on longer timescales. ImageNet (data when models were prestigious), scaling laws (engineering regularity when theory was prestigious), and RLHF (human factors when benchmarks were prestigious) all came from someone targeting an avoided object. It's a career-level question more than a project-level one.

The texture difference: elite researchers run this as a **fast, felt, iterative loop**, not a sequential audit. The questions fire in seconds as intuitions ("hmm, that baseline smells under-tuned," "wait, wouldn't perfect retrieval only buy 1%?"), interleaved with cheap experiments. The checklist is what the intuition looks like when serialized. That matters for how you should use it — see B.

## B. What's most valuable, what's overweight

**Highest value, keep at full strength:**

- **Q4 (novel prediction)** — the single best filter for "real reframing vs. renaming." Almost nobody applies it.
- **Q5 (cheapest discriminator)** — the highest ROI-per-minute question in empirical ML. It converts weeks of GPU time into hours of log analysis.
- **Q7 (what kills the gain)** — pre-mortem on the baseline. Directly prevents the most common cause of non-replicating results.
- **Q2/Q3 as a pair (wrong object → natural object)** — the core creative move. Q1 is really a special case of this pair.
- **Q8–Q9 (necessity + predicted slices)** — this is what turns "we got +2%" into "we understand why," and it's what separates cited-once papers from built-upon papers.

**Valuable but should be merged (redundancy):**

- Q1 folds into Q2–Q3 (shared root cause is just the evidence that the object is wrong).
- Q10 folds into Q2 (patching downstream symptoms *is* optimizing the wrong object).
- Q12 (invariants) is Q3 phrased in physics vocabulary — "what invariant do successful methods protect?" and "what's the natural object?" are the same question approached from opposite ends. Keep whichever phrasing generates ideas for you, but they're one slot, not two.
- Q9 is the operational form of Q8. Merge into one: "name the necessary component and the slice where removing it kills the effect."

So the 13 questions compress to about 7 without loss. That compression matters because:

**The real risk of this framework is not that it's wrong — it's that it becomes a procrastination engine.** Three specific failure modes:

1. **Audit paralysis.** Every question can be answered more thoroughly. A weak researcher will spend three weeks producing a beautiful pre-design document and zero experiments. The elite version of this framework is time-boxed to hours, answered in bullet points, and *revised after contact with evidence* — it's a living document, not a gate you pass once.
2. **Premature demand for depth.** Q1–Q3 assume there *is* a hidden unifying cause. Often there isn't — failures really are separate, and honest incremental work on one of them is the right move. A framework that always pushes toward "deeper modeling error" will occasionally push you into manufactured profundity: inventing a unifying story where the truth is three boring bugs. The audit needs an explicit escape hatch: "or these are genuinely independent, and that's fine."
3. **Sequencing error.** Several questions (Q8, Q9 especially) can only be answered well *after* preliminary evidence exists. Asking them at day zero produces speculation dressed as analysis. The audit should run in two passes: a light pass pre-experiment (Q2–Q7, Q13) and a heavy pass at the first gate (Q4, Q8–Q9, Q11) when you have something real to interrogate.

One more overweight element: "reverse abduction" as branding. The move is real (inference to the smallest explanation), but formalizing the vocabulary adds no power and risks the terminology-change failure your own Q4 is designed to catch. Elite practice is unpretentious about this.

## C. Missing high-leverage angles

Your list covers the epistemics of *the method*. What's missing is mostly the epistemics of *the problem, the measurement, and the researcher*:

**1. The oracle ceiling (upper-bound before you build).** Before designing any component, compute what perfect performance of that component would buy. Inject ground-truth retrieval, ground-truth labels, ground-truth plans. If the oracle gain is small, the whole direction is dead before it starts. This is the strongest missing question and the cheapest to run.

**2. The trivial-baseline floor.** The dual of the oracle: what does the dumbest possible method get? Majority class, nearest-neighbor, copy-the-input, GPT-with-a-prompt. A shocking fraction of published gains sit between an unreported trivial floor and the proposed method, and the trivial floor captures most of it. Elite labs run this reflexively; it never appears in advice lists.

**3. Benchmark validity audit (does the metric measure the construct?).** You have "metric gaming" defense, but the deeper question is whether the benchmark measures the thing at all. Is the test set contaminated in pretraining? Is inter-annotator agreement above your claimed gain? Does the benchmark saturate? Can the benchmark be solved by a shortcut that has nothing to do with the capability's name? Many "advances" are advances on a broken proxy.

**4. Effect-size realism / power analysis.** Given seed variance and eval-set size, what's the minimum detectable effect? If your expected gain is 1% and seed noise is ±1.5%, the project is unpowered regardless of whether the idea is right. Almost nobody in ML does this, and it silently invalidates a large fraction of small-gain papers.

**5. Why now? (the enabling-condition question).** If this idea is good and simple, why doesn't it exist? Legitimate answers: a new dataset, new compute regime, a recent result that unlocked it, an interdisciplinary import, or genuine field blindness (your negative space). If you can't name the enabling condition, the most likely explanations are (a) it exists and you haven't found it, or (b) it was tried and failed silently. This question routes you either to better prior-art search or to a real differentiating insight.

**6. Who inherits this? (the downstream-user test).** A result is influential in proportion to how easily others can build on it. Ask: what's the follow-up paper someone else writes using my result as a lemma? If you can't imagine one, you may have a terminal result — publishable, uninfluential. This question also enforces simplicity (complex methods have no inheritors).

**7. The incentive audit (why does the field believe the current story?).** Fields hold wrong defaults for reasons: a metric that's easy to compute, a dataset that's free, a story that flatters an incumbent method, an evaluation everyone's code already supports. Understanding *why* the wrong object is entrenched tells you both how confident to be that it's wrong and how hard adoption will fight you.

**8. Reverse-generating papers from their hidden move (your suggestion — endorsed, formalized below).** Take 5 landmark papers in your area and, for each, write one sentence: "the field optimized/represented X; this paper switched to Y; that switch predicted Z." Doing this for your subfield builds a catalog of *move types* — and, more importantly, reveals which move types your subfield hasn't used yet. This is trainable taste.

**9. Terminology-change detection (your suggestion — the operational test).** A framing is real, not nominal, iff it changes at least one of: (a) a prediction (different expected outcome on some concrete input), (b) a computation (different algorithm, not a renamed one), or (c) a measurement (a new quantity becomes observable/checkable). If a "new perspective" changes none of the three, it's a synonym. This test is cheap and brutal and should run on your own framings first.

**10. The failure-mode forecast.** Before running the main experiment, write down the three most likely ways it fails and what each failure would *mean* (bug / wrong hypothesis / underpowered / wrong slice). This converts failures from demoralizing events into pre-planned branches, and it's a strong bias-detector: if you can't imagine failure modes, you don't understand your own experiment.

## D. Reusable prompt templates

Each designed for AI-assisted thinking (paste your project context, then the template), but they work equally as solo writing prompts.

**T1 — Wrong-Object Probe**
"Here are the observed failures/limitations of current methods in [area]: [list]. For each, state what quantity the current method is implicitly optimizing or what representation it assumes. Then propose 2–3 alternative objects/representations/invariants under which several of these failures would become the *same* failure or disappear. For each alternative, state one concrete phenomenon it predicts that the incumbent framing does not. If the failures appear genuinely independent, say so explicitly and stop."

**T2 — Oracle & Floor Bracket**
"I am considering building [component] to improve [system] on [metric]. Design (a) an oracle experiment that upper-bounds the achievable gain by injecting ground truth for [component], and (b) the most embarrassing trivial baseline that might capture part of the gain. Specify exactly how to run both in under [X] GPU-hours / with no training. State the decision rule: at what oracle ceiling and trivial floor is the project dead?"

**T3 — Cheapest Discriminator**
"My hypothesis is: [one sentence]. List discriminating observations available *before any training run*, ordered by cost: existing-log analysis, frozen-model probes, subset/slice evaluation, trajectory statistics, synthetic minimal cases. For each: what result supports the hypothesis, what result kills it, and what result is uninformative. Flag any proposed observation that cannot actually distinguish my hypothesis from the default explanation."

**T4 — Baseline Self-Attack**
"My method shows [gain] over [baseline] under [setup]. Act as the strongest possible defender of the baseline. List everything the baseline would need to receive parity: tuning budget, data, tricks portable from my method, modern defaults it lacks. Then list the artifact checks in order of likelihood: leakage, contaminated eval, seed variance vs. effect size, metric quirks, budget asymmetry, eval-set overfitting via repeated peeking. Output a table: threat → concrete check → status."

**T5 — Mechanism Necessity & Slice Forecast**
"My claimed mechanism is: [sentence]. (1) Name the component whose removal must destroy the effect if the mechanism is real, and the minimal ablation that tests it. (2) Predict, *before looking*, the data slice where the gain should concentrate and the slice where it should be absent. (3) State one alternative mechanism that explains the same aggregate number, and the slice pattern that would distinguish the two. Format: mechanism / kill-ablation / success-slice / null-slice / rival mechanism / discriminating slice."

**T6 — Prior-Art Collision & Why-Now**
"Idea: [description]. (1) List the 5–10 papers a hostile expert reviewer would cite as 'this already exists,' including work under different terminology and from adjacent fields. For each, state the *specific* delta of my idea — prediction, computation, or measurement that differs — or admit there is none. (2) Answer: why does this idea not already exist? Name the enabling condition (new data/compute/result/import) or the specific field blind spot. 'Nobody thought of it' is not an accepted answer."

**T7 — Terminology-Change Test**
"Here is my proposed reframing: [description]. Apply the three-part test: (a) name one concrete input where my framing predicts a different outcome than the standard framing; (b) name one algorithmic step that is genuinely different, not renamed; (c) name one quantity that becomes measurable that wasn't before. If all three fail, output: 'This is a vocabulary change' and identify the standard concept it renames."

**T8 — Hidden-Move Extraction (paper reverse-engineering)**
"For each of these papers [list 3–5 landmark papers], produce one line: 'Field optimized/represented X → paper switched to Y → switch predicted/enabled Z.' Then: which switch-types appear repeatedly in this subfield, and which switch-types (from other fields' catalogs: change of variable, change of objective, change of granularity, change of what's held fixed, change of what's measured) have *not* yet been applied here?"

**T9 — Power & Failure Forecast**
"Planned experiment: [design], expected effect: [size], eval set: [n], known seed variance: [σ or 'unknown']. (1) Is the expected effect detectable above noise with this design? If variance is unknown, specify the cheapest variance-estimation run. (2) List the three most probable failure outcomes and classify what each would mean: implementation bug / hypothesis false / underpowered / wrong slice. (3) For each, the immediate next action. If I cannot generate failure modes, say what that indicates."

**T10 — Negative-Space Scan**
"In [subfield], list: (a) objects/quantities that appear in many papers' 'limitations' or 'future work' sections but rarely as the main target; (b) evaluation practices everyone privately distrusts but keeps using; (c) questions that are avoided because they're unglamorous, cross-disciplinary, expensive to evaluate, or threaten a popular method. For each avoided object: what incentive maintains the avoidance, and what would a direct attack look like?"

## E. Usage guide per template

**T1 (Wrong-Object Probe).**
*When:* project inception, or when you notice yourself planning the third patch to the same system. *Prevents:* careers spent patching symptoms; incrementalism by default. *Output format:* table of failure → implicit object → candidate reframing → novel prediction; plus an explicit "independent failures" verdict option. *Weak misuse:* forcing a grand unifying story onto unrelated bugs, then falling in love with the story; treating the AI's most poetic reframing as true because it's elegant. *Strong use:* generates 3 candidate reframings, immediately routes each into T7 (is it real?) and T3 (what's the cheap test?), and is genuinely willing to conclude "no hidden cause, the boring project is correct."

**T2 (Oracle & Floor Bracket).**
*When:* before building any pipeline component; before any project whose pitch is "X will improve Y." *Prevents:* months building a component whose perfect version buys 0.4%; publishing gains that a trivial baseline matches. *Output:* two experiment specs with explicit compute cost and a pre-committed kill threshold. *Weak misuse:* running the oracle, seeing a small ceiling, and rationalizing ("the ceiling underestimates the real potential because..."); or designing a strawman oracle. *Strong use:* writes the kill threshold *before* running, treats the bracket [floor, ceiling] as the honest room the method lives in, and reports both numbers in the eventual paper.

**T3 (Cheapest Discriminator).**
*When:* the moment a hypothesis forms, before requesting compute. *Prevents:* the "train for two weeks to learn what a log grep would have shown" failure; also prevents undiscriminating experiments (ones where every outcome is explainable). *Output:* ranked list, each entry with support/kill/uninformative outcomes pre-stated. *Weak misuse:* choosing the cheap test whose outcome they already know will look supportive; skipping the "what kills it" column. *Strong use:* runs the top two discriminators same-day, updates or abandons the hypothesis within 48 hours, and treats "uninformative" results as a design flaw in the test, not a license to proceed.

**T4 (Baseline Self-Attack).**
*When:* the first time your method beats the baseline, and again before submission. *Prevents:* non-replicating results; rebuttal-stage catastrophes; the slow reputational damage of gains that evaporate. *Output:* threat-model table with checkboxes and evidence links. *Weak misuse:* performing the audit rhetorically ("we believe leakage is unlikely") without running checks; giving the baseline a token tuning sweep. *Strong use:* allocates the baseline the *same* tuning budget as the method, ports every portable trick to it, and is privately pleased when the gain shrinks but survives — because a surviving gain is now defensible.

**T5 (Mechanism Necessity & Slice Forecast).**
*When:* after the first positive result, before believing your own explanation of it. *Prevents:* the "right result, wrong story" paper — the most insidious failure, because it replicates but misleads the field. *Output:* the six-slot format (mechanism / kill-ablation / success-slice / null-slice / rival / discriminator), written before looking at slice data. *Weak misuse:* writing slice predictions after peeking; choosing a rival mechanism that's a strawman. *Strong use:* registers predictions in the project log with a date, then checks — and when the slice pattern contradicts the story, treats that as the most interesting result of the project so far.

**T6 (Prior-Art Collision & Why-Now).**
*When:* inception, and again after the method stabilizes (the final method often collides with different prior work than the initial idea). *Prevents:* rediscovery; rejection-by-citation; and its subtler cousin, differentiating your work by misrepresenting prior work. *Output:* paper list with per-paper specific delta; one-sentence enabling condition. *Weak misuse:* searching only their own subfield's terminology; accepting "our setting is slightly different" as a delta. *Strong use:* searches adjacent fields' vocabulary (the same idea is called different things in NLP, vision, RL, statistics), emails authors of the closest work, and treats a genuine collision as good news received early rather than bad news received from Reviewer 2.

**T7 (Terminology-Change Test).**
*When:* whenever anyone (including you, including an AI assistant) proposes a "new perspective," "unified view," or "novel framing." *Prevents:* the most seductive failure of AI-assisted research specifically — LLMs are fluent generators of framings that sound deep and change nothing. *Output:* pass/fail on each of prediction/computation/measurement; if fail, the named standard concept. *Weak misuse:* grading their own framing generously ("it predicts differently... in spirit"); applying the test only to rivals' framings. *Strong use:* applies it most harshly to their own favorite ideas, and uses a failed test constructively — "what would I have to add to this framing to make it predict something?"

**T8 (Hidden-Move Extraction).**
*When:* ongoing practice, one paper per week; intensively when entering a new subfield. *Prevents:* shallow reading (knowing results without knowing moves); reinventing moves the field already exhausted; and move-blindness (not seeing which transformations are available). *Output:* the one-line X→Y→Z per paper, accumulated into a personal catalog, plus a "moves not yet tried here" list. *Weak misuse:* extracting the *stated* contribution (which is marketing) rather than the actual hidden move; collecting the catalog and never consulting it. *Strong use:* notices that the stated and actual moves differ, cross-indexes moves across fields, and uses the "untried moves" list as a hypothesis generator that feeds T1.

**T9 (Power & Failure Forecast).**
*When:* before any experiment longer than a day; mandatory before any experiment you'd be tempted to trust. *Prevents:* unpowered studies read as real effects; demoralization-by-surprise; the "mysterious failure → random thrashing" spiral. *Output:* detectability verdict; three-branch failure tree with classifications and next actions. *Weak misuse:* skipping variance estimation because "we don't have compute for multiple seeds" (then the single-seed result is uninterpretable anyway); writing failure modes so vague they don't branch. *Strong use:* runs the small variance-estimation study first, sizes the experiment to the effect, and on failure executes the pre-planned branch the same day instead of improvising under disappointment.

**T10 (Negative-Space Scan).**
*When:* quarterly, and at every project-selection moment; not useful mid-execution. *Prevents:* a career of competing in the most crowded, most efficient part of the idea market where your marginal value is lowest. *Output:* avoided-object list with the maintaining incentive named for each — the incentive analysis is what separates real negative space from "things nobody does because they're bad ideas." *Weak misuse:* mistaking graveyards for gaps (some spaces are empty because ten groups died there silently — check for the corpses); using contrarianism as identity rather than as a filter. *Strong use:* pairs every candidate gap with T6's why-now question and T2's oracle bracket before committing, and accepts that most negative space is empty for good reason — one real gap per few years is a great hit rate.

## F. The compact pre-design audit

Designed to be answered in **one sitting (60–90 minutes), in bullet points**, then revisited at the first evidence gate. If a question can't be answered yet, write "unknown — resolved by [cheap test]" rather than speculating.

---

**ELITE PRE-DESIGN AUDIT — run before any AI/CS research project**

*Context to paste: problem area, observed failures/limitations motivating the project, current standard methods, my proposed direction (one paragraph max).*

**1. Object.** What is the incumbent method implicitly optimizing or representing? State my candidate alternative object/invariant in one sentence. Do the motivating failures become one failure under it — or are they genuinely independent (acceptable answer; if so, name the single failure worth attacking and skip to Q4)?

**2. Reality of the reframing.** Name one input where my framing predicts a different outcome, one computation that genuinely differs, or one newly measurable quantity. If none: this is vocabulary, not a contribution — return to Q1 or abandon the reframing and keep the concrete method.

**3. Novel prediction.** What phenomenon should be observable if I'm right that incumbents do not predict? On what slice should my effect concentrate, and where should it be absent?

**4. Bracket.** Oracle ceiling: what does a perfect version of my component buy (spec the injection experiment)? Trivial floor: what does the dumbest baseline get? Pre-commit: at what ceiling/floor is this project dead?

**5. Cheapest discriminator.** The fastest pre-training observation (logs, frozen-model probe, subset eval, synthetic minimal case) with pre-stated support/kill outcomes. Schedule it within 48 hours.

**6. Collision & why-now.** The 5 closest prior works (including other fields' vocabulary) and my specific delta against each. The enabling condition that explains why this doesn't already exist. If the answer is "nobody thought of it," search harder.

**7. Baseline pre-mortem.** What would the strongest fairly-tuned baseline need to erase my gain? Equal tuning budget, portable tricks, modern defaults. Artifact checklist: leakage / contamination / seed variance vs. effect size / metric quirks / budget asymmetry.

**8. Power.** Expected effect size vs. known or estimated noise. Is the main experiment capable of detecting the effect? If variance unknown: spec the cheap variance run first.

**9. Failure forecast.** The three most likely failure outcomes, each classified (bug / false hypothesis / underpowered / wrong slice) with a pre-planned next action.

**10. Kill criteria & inheritance.** Dated, written conditions under which I kill or park this within 6–8 weeks. And: what follow-up paper does someone *else* write using my result as a lemma? If I can't imagine one, is this worth a year?

*Rules of use: bullets, not prose; time-boxed; answers are provisional and get revised at the first gate; "unknown + cheap resolver" beats confident speculation; if the audit is more fun than the experiments, the audit has become the procrastination.*

---

A final calibration note, because it's the difference between this framework helping and hurting: the audit's purpose is to make you **fast**, not careful. Every question either kills a doomed direction early or pre-loads a decision you'd otherwise agonize over mid-project. If you find it slowing you down — polishing answers, deferring the first experiment past week one — you're using it as armor against contact with reality, which is precisely the failure mode it exists to prevent. The elite version of this document is scrappy, dated, half-wrong, and updated weekly.