# The mathematical-frame palette — the third axis (`/forge` step 3′)

> Schools = *how to think* · types = *what output* · **frames = which mathematics carries the object.**
> The monoculture ("a probabilistic/linear-algebra module bolted onto a net") lives in FRAME-SELECTION,
> which the pipeline controls — not in the model's prior. LLMs are weak at *choosing* an off-consensus
> frame but strong at *deriving* under one. So the pipeline ASSIGNS the frame; the model derives.
> Three levers: **FORCE** (assign the frame) · **BLIND** (strip the field's vocabulary in the hand-off) ·
> **DISCRIMINATE** (demand a DIFF-PREDICTION the incumbent frame does not make).

| Frame | Natural object | Fits a signature of |
|---|---|---|
| **Probability / Markov** ⚑incumbent | conditional next-state, transition matrix | local one-step dependence (the default — displace it) |
| **Branching / renewal** | offspring distribution, extinction probability, generating function | multiplicative survival/decay over depth |
| **Optimal transport** | coupling / transport plan, Wasserstein geodesic | matching two distributions under a cost/geometry |
| **Dynamical systems & control** | vector field, fixed points, Lyapunov function, controller | an iterative process whose stability/steering is the question |
| **Spectral / operator** | eigenvalues of an operator, spectral gap | mixing rate, propagation speed |
| **Information geometry** | statistical manifold, Fisher metric, natural gradient | the space of distributions has curvature the Euclidean view misses |
| **Statistical mechanics / mean-field** | partition function, order parameter, phase transition | large-N emergence; a sharp transition in a control parameter |
| **Convex duality** | the dual problem, Lagrangian, saddle point | a constrained optimization whose dual is simpler |
| **Algebraic / group** | symmetry group, invariants, equivariant maps | a transformation the answer must respect |
| **Extremal combinatorics** | extremal set/graph, counting bound | "how many / does there exist"; a hard discrete bound |
| **Queueing** | arrival/service processes, Little's law, waiting-time | a resource with jobs arriving & served; throughput under load |
| **Rate-distortion / coding** | rate-distortion function, channel capacity | a lossy-representation tradeoff; "how few bits preserve what matters" |
| **Causal graphs** | the DAG, do-operator, interventions | correlation-vs-mechanism; cross-environment invariance |
| **Random matrix theory** | spectral density, universality, bulk/outlier split | high-dim covariance/weight spectra |

## Use (`/forge` step 3′)
1. **Name the incumbent frame** in one line (the frame ledger) — making the default visible is half the fix.
2. **Force ≥1 candidate derived in a NON-incumbent frame**, chosen by signature match — or by the goal's
   optional `FRAMES:` field (the human's mathematical taste, injected at framing time; it takes priority).
3. That candidate carries **DIFF-PREDICTION**: one observable this frame predicts that the incumbent
   cannot. **No differential ⇒ vocabulary, not a frame ⇒ discard** (deletion test).

## Hard rules
- **ONE forced off-frame per round, rotation across rounds — never a 14-frame sweep** (the menu disease).
- **A frame is admitted only if it makes the object SIMPLER** (the He-bar rules). Exotic math earns no
  points; a simpler object does.
- Print the frame ledger in every `/prospect` and `/forge` report so the human can inject/override.
