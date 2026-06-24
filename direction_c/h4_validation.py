"""Type-I and power validation generators for the H4 test (protocol §4).

Implements the three pre-registered null generators and the planted-effect power
generator, plus the Clopper-Pearson one-sided upper bound used as the pass
criterion. All torch-free and model-independent: these validate the FULL test
pipeline (track construction, bucketization, trajectory-synchronous permutation,
shared-draw maxT correction, p-values) without the 26B model.

- **Null A (SYNTHETIC permutation-orbit):** relabel each trajectory's bucket
  labels via the test's own allowed group on a SYNTHETIC dataset. NOTE: this is
  a synthetic-structure code check, NOT the protocol's true Null A (which must
  run the orbit relabel on REAL captured logs -- see ``null_a_real_orbit`` and
  the mandatory pre-publication gate documented in the README).
- **Null B (heterogeneous-track generative):** sample expert mass from a
  per-track baseline ``q_hat`` independent of bucket.
- **Null C (autocorrelated):** AR(1) within trajectory; tests robustness to
  block-diffusion adjacent-timestep dependence.
- **Null X-corr (cross-layer-correlated):** a shared per-(trajectory,call)
  latent perturbs routing similarly across ALL layers (positive cross-layer
  correlation of ``T_L``) but is INDEPENDENT of the timestep bucket (H0 holds).
  This is the discriminating null: a BROKEN per-layer-independent permutation
  mis-calibrates here, while the correct shared draw stays calibrated.
- **Power:** planted-effect tilt ``q(δ) ∝ q_hat · exp(δ g_b h_e)``.

Pass criterion (protocol §4): one-sided 95% Clopper-Pearson upper bound on the
empirical global-FWER ``U_0.95 <= 0.065`` at ``alpha = 0.05``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
from scipy.stats import beta

from direction_c.h4_data import H4Dataset, build_dataset

logger = logging.getLogger(__name__)


def clopper_pearson_upper(n_reject: int, n_total: int, *, conf: float = 0.95) -> float:
    """One-sided upper Clopper-Pearson bound on a binomial proportion.

    Args:
        n_reject: Number of rejections (successes).
        n_total: Number of trials.
        conf: One-sided confidence level (0.95 -> the 95% upper bound).

    Returns:
        The upper confidence bound on the true rejection probability.
    """
    if n_total <= 0:
        return 1.0
    if n_reject >= n_total:
        return 1.0
    # Upper bound = Beta inverse-CDF at conf with shape (k+1, n-k).
    return float(beta.ppf(conf, n_reject + 1, n_total - n_reject))


@dataclass(frozen=True)
class SyntheticDesign:
    """A reusable synthetic logging design (the EXCHANGEABILITY structure).

    Attributes:
        num_trajectories: R.
        calls_per_traj: T_r (constant here for simplicity).
        positions: token positions per call.
        num_layers: decoder layers.
        num_experts: E.
        num_buckets: K.
        top_k: k.
    """

    num_trajectories: int
    calls_per_traj: int
    positions: int
    num_layers: int
    num_experts: int
    num_buckets: int
    top_k: int

    def call_buckets(self) -> dict[int, dict[int, int]]:
        """Equal-count bucket labels assigned cyclically across each trajectory's calls."""
        out: dict[int, dict[int, int]] = {}
        for r in range(self.num_trajectories):
            out[r] = {s: (s % self.num_buckets) for s in range(self.calls_per_traj)}
        return out


def _draw_topk(rng: np.random.Generator, probs: np.ndarray, top_k: int) -> np.ndarray:
    """Draw top_k DISTINCT expert ids per row from per-row probability vectors.

    Args:
        rng: RNG.
        probs: ``(n, E)`` row-normalized probabilities.
        top_k: k.

    Returns:
        ``(n, top_k)`` distinct expert ids.
    """
    n, e = probs.shape
    out = np.empty((n, top_k), dtype=np.int64)
    for i in range(n):
        out[i] = rng.choice(e, size=top_k, replace=False, p=probs[i])
    return out


def make_null_b(design: SyntheticDesign, *, seed: int = 0,
                concentration: float = 0.3) -> H4Dataset:
    """Null B: per-track baseline expert law, INDEPENDENT of timestep bucket.

    Each track ``(traj, position)`` gets its own Dirichlet-drawn expert baseline
    ``q_hat``; every visit samples top-k from it regardless of bucket. No bucket
    dependence -> the test must not reject beyond alpha.

    Args:
        design: The synthetic design.
        seed: RNG seed.
        concentration: Dirichlet concentration (lower -> more heterogeneous tracks).

    Returns:
        An :class:`H4Dataset`.
    """
    rng = np.random.default_rng(seed)
    n_tracks = design.num_trajectories * design.positions
    track_baseline = rng.dirichlet(np.full(design.num_experts, concentration), size=n_tracks)
    return _generate_from_track_law(design, track_baseline, rng, bucket_tilt=None)


def make_null_c(design: SyntheticDesign, *, seed: int = 0, rho: float = 0.8,
                concentration: float = 0.3) -> H4Dataset:
    """Null C: autocorrelated (AR(1)) perturbation with CONSTANT marginal.

    Adjacent calls share a smoothly drifting latent that perturbs the expert
    logits, but the perturbation is independent of the bucket label and averages
    out, so there is no genuine timestep specialization. Tests robustness to
    block-diffusion adjacent-timestep dependence.

    Args:
        design: The synthetic design.
        seed: RNG seed.
        rho: AR(1) coefficient (strength of adjacent-call dependence).
        concentration: Dirichlet concentration for the per-track baseline.

    Returns:
        An :class:`H4Dataset`.
    """
    rng = np.random.default_rng(seed)
    n_tracks = design.num_trajectories * design.positions
    base_logits = np.log(rng.dirichlet(np.full(design.num_experts, concentration),
                                        size=n_tracks) + 1e-9)
    # AR(1) latent over calls, shared across tracks within a trajectory; a fixed
    # random direction in expert space. Independent of bucket label.
    direction = rng.standard_normal(design.num_experts)
    layer_visits: dict[int, dict[str, np.ndarray]] = {}
    for L in range(design.num_layers):
        cols = _empty_cols()
        for r in range(design.num_trajectories):
            z = 0.0
            for s in range(design.calls_per_traj):
                z = rho * z + rng.standard_normal()
                for p in range(design.positions):
                    track = r * design.positions + p
                    logits = base_logits[track] + z * direction * 0.1
                    probs = _softmax(logits)
                    ids = _draw_topk(rng, probs[None, :], design.top_k)[0]
                    _append(cols, r, s, p, ids)
        layer_visits[L] = _finalize(cols)
    return build_dataset(layer_visits, design.call_buckets(), design.num_experts,
                         design.num_buckets, top_k=design.top_k)


def make_null_xcorr(design: SyntheticDesign, *, seed: int = 0,
                    concentration: float = 0.3, coupling: float = 1.5) -> H4Dataset:
    """Cross-layer-correlated null: shared per-(traj,call) latent, NO bucket dep.

    For each ``(trajectory, call)`` we draw ONE random latent vector ``z_rs`` in
    expert space and apply the SAME ``z_rs`` (scaled per layer) to the routing
    logits of EVERY layer. This induces strong POSITIVE cross-layer correlation
    of the per-layer statistic ``T_L`` (a call whose routing happens to look
    bucket-aligned by chance does so in all layers at once). Crucially ``z_rs``
    is drawn INDEPENDENTLY of the bucket label ``b(t_rs)``, so ``Y ⟂ b | track``
    holds and the global null is true.

    This is the discriminating null (review gap 1): the correct shared-draw maxT
    stays calibrated (``M^(m)`` keeps the same cross-layer correlation as
    ``M_obs``), whereas a BROKEN per-layer-independent permutation destroys that
    correlation and mis-calibrates -- so the suite can tell them apart.

    Args:
        design: The synthetic design.
        seed: RNG seed.
        concentration: Dirichlet concentration for the per-track baseline.
        coupling: Strength of the shared latent perturbation.

    Returns:
        An :class:`H4Dataset` under H0 with cross-layer-correlated ``T_L``.
    """
    rng = np.random.default_rng(seed)
    n_tracks = design.num_trajectories * design.positions
    base_logits = np.log(
        rng.dirichlet(np.full(design.num_experts, concentration), size=n_tracks) + 1e-9)
    # Per-(traj, call) shared latent, INDEPENDENT of the bucket. Same z across
    # all layers (scaled by a fixed per-layer gain) -> correlated T_L.
    latent = {(r, s): rng.standard_normal(design.num_experts)
              for r in range(design.num_trajectories)
              for s in range(design.calls_per_traj)}
    layer_gain = 0.6 + 0.4 * rng.random(design.num_layers)  # all positive
    layer_visits: dict[int, dict[str, np.ndarray]] = {}
    for L in range(design.num_layers):
        cols = _empty_cols()
        gain = coupling * layer_gain[L]
        for r in range(design.num_trajectories):
            for s in range(design.calls_per_traj):
                z = latent[(r, s)]
                for p in range(design.positions):
                    track = r * design.positions + p
                    probs = _softmax(base_logits[track] + gain * z)
                    ids = _draw_topk(rng, probs[None, :], design.top_k)[0]
                    _append(cols, r, s, p, ids)
        layer_visits[L] = _finalize(cols)
    return build_dataset(layer_visits, design.call_buckets(), design.num_experts,
                         design.num_buckets, top_k=design.top_k)


def make_planted(design: SyntheticDesign, delta: float, *, seed: int = 0,
                 planted_layers: tuple[int, ...] = (1,),
                 concentration: float = 0.3) -> tuple[H4Dataset, tuple[int, ...]]:
    """Planted-effect generator: bucket-dependent tilt on selected layers.

    ``q_iLbe(δ) ∝ q_hat_iLe · exp(δ g_b h_e)`` with ``g_b`` centered/standardized
    over buckets and ``h_e = +1`` for early specialists A, ``-1`` for late
    specialists B, ``0`` otherwise. Non-planted layers use ``δ = 0`` (null).

    Args:
        design: The synthetic design.
        delta: Effect size (0 -> no effect).
        seed: RNG seed.
        planted_layers: Layers receiving the tilt.
        concentration: Dirichlet concentration for per-track baselines.

    Returns:
        ``(dataset, planted_layers)``.
    """
    rng = np.random.default_rng(seed)
    n_tracks = design.num_trajectories * design.positions
    track_baseline = rng.dirichlet(np.full(design.num_experts, concentration), size=n_tracks)
    n_spec = max(1, design.num_experts // 16)
    h = np.zeros(design.num_experts)
    h[:n_spec] = 1.0
    h[n_spec:2 * n_spec] = -1.0
    buckets = np.arange(design.num_buckets)
    g = (buckets - buckets.mean()) / (buckets.std() + 1e-12)

    layer_visits: dict[int, dict[str, np.ndarray]] = {}
    call_to_bucket = design.call_buckets()
    for L in range(design.num_layers):
        tilt = delta if L in planted_layers else 0.0
        cols = _empty_cols()
        for r in range(design.num_trajectories):
            for s in range(design.calls_per_traj):
                b = call_to_bucket[r][s]
                factor = np.exp(tilt * g[b] * h)
                for p in range(design.positions):
                    track = r * design.positions + p
                    q = track_baseline[track] * factor
                    q = q / q.sum()
                    ids = _draw_topk(rng, q[None, :], design.top_k)[0]
                    _append(cols, r, s, p, ids)
        layer_visits[L] = _finalize(cols)
    return (build_dataset(layer_visits, call_to_bucket, design.num_experts,
                          design.num_buckets, top_k=design.top_k),
            planted_layers)


def _generate_from_track_law(design: SyntheticDesign, track_baseline: np.ndarray,
                             rng: np.random.Generator, bucket_tilt) -> H4Dataset:
    """Sample a dataset where each track draws top-k from its baseline law."""
    layer_visits: dict[int, dict[str, np.ndarray]] = {}
    call_to_bucket = design.call_buckets()
    for L in range(design.num_layers):
        cols = _empty_cols()
        for r in range(design.num_trajectories):
            for s in range(design.calls_per_traj):
                for p in range(design.positions):
                    track = r * design.positions + p
                    q = track_baseline[track]
                    ids = _draw_topk(rng, q[None, :], design.top_k)[0]
                    _append(cols, r, s, p, ids)
        layer_visits[L] = _finalize(cols)
    return build_dataset(layer_visits, call_to_bucket, design.num_experts,
                         design.num_buckets, top_k=design.top_k)


def permutation_orbit_relabel(dataset: H4Dataset, rng: np.random.Generator) -> H4Dataset:
    """Relabel each trajectory's bucket labels via the allowed group (orbit step).

    Produces a new dataset whose ``call_buckets`` is a trajectory-synchronous
    permutation of the input's; visits are unchanged. This is the per-replicate
    relabeling step shared by both the synthetic and the real-log Null A.

    Args:
        dataset: The base dataset (real or synthetic).
        rng: RNG.

    Returns:
        A new :class:`H4Dataset` with relabeled call buckets.
    """
    new_cb: dict[int, dict[int, int]] = {}
    for r, c2b in dataset.call_buckets.items():
        calls = sorted(c2b)
        buckets = [c2b[s] for s in calls]
        perm = rng.permutation(len(buckets))
        new_cb[r] = {s: int(buckets[perm[j]]) for j, s in enumerate(calls)}
    return H4Dataset(
        num_experts=dataset.num_experts, num_buckets=dataset.num_buckets,
        layers=dataset.layers, visits_by_layer=dataset.visits_by_layer,
        call_buckets=new_cb,
    )


def null_a_real_orbit(
    real_dataset: H4Dataset,
    *,
    r_null: int = 5000,
    alpha: float = 0.05,
    b_perm: int = 9999,
    seed: int = 0,
) -> dict[str, float]:
    """Protocol Null A on REAL captured logs (MANDATORY pre-publication gate).

    The protocol's true Null A: take the REAL routing dataset, repeatedly relabel
    timesteps within each trajectory via the test's own allowed group, treat each
    relabeled dataset as "observed," and run the full test. Because the labels
    were randomized from the test's own null group, the global FWER MUST be
    controlled if the implementation is correct -- on the real data's actual
    track heterogeneity, top-k dependence, cross-layer dependence, sparsity, and
    missingness, none of which a synthetic generator fully reproduces.

    This CANNOT run until the 26B model produces real logs (load with
    :func:`direction_c.persistence.load_h4_dataset`). It is a required gate for
    the C2/H4 run, separate from the synthetic in-test checks.

    Args:
        real_dataset: An :class:`H4Dataset` built from REAL probe logs.
        r_null: Number of orbit replicates (protocol: >= 5000).
        alpha: Significance level.
        b_perm: Permutations per replicate.
        seed: RNG seed.

    Returns:
        ``{"r_null", "rejections", "fwer", "u95", "passed"}`` where ``passed`` is
        ``1.0`` iff the Clopper-Pearson 95% upper bound ``<= 0.065``.
    """
    from direction_c.h4_test import run_h4_test

    rng = np.random.default_rng(seed)
    rejections = 0
    for _ in range(r_null):
        relabeled = permutation_orbit_relabel(real_dataset, rng)
        res = run_h4_test(relabeled, alpha=alpha, b_perm=b_perm,
                          seed=int(rng.integers(1 << 30)))
        rejections += int(res.supported)
    u95 = clopper_pearson_upper(rejections, r_null)
    return {
        "r_null": float(r_null),
        "rejections": float(rejections),
        "fwer": rejections / r_null if r_null else 1.0,
        "u95": u95,
        "passed": 1.0 if u95 <= 0.065 else 0.0,
    }


# -- small array helpers ------------------------------------------------------

def _softmax(x: np.ndarray) -> np.ndarray:
    z = x - x.max()
    e = np.exp(z)
    return e / e.sum()


def _empty_cols() -> dict[str, list]:
    return {"traj_idx": [], "call_idx": [], "position": [], "expert_ids": []}


def _append(cols: dict[str, list], r: int, s: int, p: int, ids: np.ndarray) -> None:
    cols["traj_idx"].append(r)
    cols["call_idx"].append(s)
    cols["position"].append(p)
    cols["expert_ids"].append(ids)


def _finalize(cols: dict[str, list]) -> dict[str, np.ndarray]:
    return {
        "traj_idx": np.asarray(cols["traj_idx"], dtype=np.int64),
        "call_idx": np.asarray(cols["call_idx"], dtype=np.int64),
        "position": np.asarray(cols["position"], dtype=np.int64),
        "expert_ids": np.asarray(cols["expert_ids"], dtype=np.int64),
    }
