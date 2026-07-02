# 5. Kill Review — Candidate 3, attacked as the harshest AC

Target: **"The Unmasking Policy as the Modeling Object of Masked Diffusion LLMs."**
I choose it because it is my weakest candidate and I knew that while writing it.
No balance. The attack, then the verdict.

---

## The attack

**1. Prior-art occupancy — the observation is six years old.**
The candidate's founding claim — "parallel unmasking commits conditional-independence
errors; ordering carries the joint structure" — is the founding observation of the
*non-autoregressive translation* literature. Mask-Predict (2019) is literally
iterative confidence-based unmasking built because of this problem. The permutation-
order question is older still (XLNet, Insertion Transformer, 2019). In the modern
masked-diffusion era, remasking samplers (ReMDM-class), planned-denoising (DDPD-class),
and entropy/margin ordering papers occupy the exact "sampler as first-class object"
ground, some with explicit planner modules — i.e., the *method half* of this candidate
is not just occupied, it is occupied by multiple groups with more compute, in a subfield
whose publication velocity means three more sampler papers will appear between your
oracle run and your submission. Rubric C3 (occupancy differential): what survives after
an honest map is "learn the policy with a frozen backbone via oracle distillation on
verifiable tasks" — an increment on occupied ground, not an object shift.

**2. Disguised old idea — the framing is the laundering `enrich.md` warns about.**
Strip the modeling-object vocabulary (rubric C1 deletion test): what remains is an
adaptive decoding-order heuristic with a learned scorer. The community has a name for
this genre — "inference-time trick paper" — and it will be read as one no matter what
the abstract says. Calling the sampler "the modeling object" does not make the network
model anything different; the training objective, the network, and the marginals are
untouched. This is *perspective shift dressed as object shift* — Layer 1 sold as
Layer 2, the precise failure mode of the methodology under audit. That my own candidate
did this is evidence of how strong the laundering gradient is.

**3. Baseline dominance and a moving target.**
Equal-NFE comparisons will be demanded against every sampler released up to the review
date. The candidate's edge case — "oracle gap is large" — most plausibly shrinks as
released models improve and as better samplers land, because the gap is a property of
*current* checkpoints, not of the problem. A result of the form "on LLaDA-8B-2025,
learned ordering beats confidence by X at 32 steps" has a shelf life of months.

**4. The only durable contribution is not the method.**
The genuinely novel piece is the **oracle-gap decomposition**: attributing masked-
diffusion error to sampler-limited vs model-limited components on verifiable tasks. That
is a measurement result. It requires no learned policy at all — a thorough study of
existing samplers plus oracle search delivers it. Ergo the candidate, as designed, is a
measurement paper wearing a method costume, and the costume is the part reviewers will
shoot.

**5. Where it dies, by category:** prior-art occupancy (primary), invalid object shift
(the "object" is a decoding procedure; C1 fails on the method half), baseline dominance
(secondary), weak publication story (the method half adds risk without adding claim).

---

## Verdict: **RESCOPE** — with a kill inside it.

- **KILL the method half** (learned unmasking policy) as a headline contribution. It is
  an increment on fast-moving occupied ground and fails the deletion test.
- **KEEP the measurement half**, rescoped to: *"How much of masked-diffusion's quality
  gap is sampler-limited? An oracle-ordering decomposition on verifiable tasks."*
  It is cheap (~1 week of frozen-model inference), self-killing (small oracle gap =
  clean negative, still informative), durable (a decomposition method outlives any
  particular sampler), and it feeds Candidate 2's instrument-science methodology.
- **Gate:** the oracle experiment runs first. Only if the gap is embarrassingly large
  does the method half re-enter through the rubric — as a follow-up, never as the
  flagship.

Why not outright KILL: the falsifier costs one week on hardware you own and settles a
question the fast-moving subfield keeps assuming an answer to. Killing before running a
one-week decisive experiment would be taste theater — the inverse error of idea theater.
