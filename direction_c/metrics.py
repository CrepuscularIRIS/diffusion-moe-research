"""Pure metric functions over recorded MoE expert-usage distributions.

These functions operate on plain NumPy arrays so they can be unit-tested with
synthetic distributions, without the DiffusionGemma model. They are the
analysis backbone for hypothesis H4 (do experts specialize by denoising
timestep t?).

Terminology
-----------
- ``num_experts`` (E): total experts in a MoE layer (DiffusionGemma: 128).
- ``usage counts``: for a given (layer, timestep-bucket), an integer vector of
  length E counting how many (token, top-k slot) selections landed on each
  expert. With top-k routing each token contributes k selections, so the
  counts sum to ``num_tokens * top_k``.
- ``usage distribution``: usage counts normalized to a probability vector.

H4 operational falsifier (implemented in ``bootstrap_js_noise_floor`` +
``pairwise_js_across_buckets``):
    H4 is FALSIFIED if, at *every* layer, the Jensen-Shannon divergence of
    expert-usage between denoising-timestep buckets does NOT exceed the upper
    bound of the within-t bootstrap null-distribution CI. In other words, if
    cross-t variation is statistically indistinguishable from within-t
    resampling noise everywhere, experts do not specialize by t.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

logger = logging.getLogger(__name__)

# Numerical floor to avoid log(0) / division-by-zero in entropy and KL terms.
_EPS: float = 1e-12


def expert_usage_distribution(
    usage_counts: np.ndarray,
    *,
    normalize: bool = True,
) -> np.ndarray:
    """Return the per-expert usage distribution from raw selection counts.

    Args:
        usage_counts: Non-negative array of shape ``(num_experts,)`` giving the
            number of selections for each expert.
        normalize: If ``True`` (default) divide by the total so the result sums
            to 1; if ``False`` return a float copy of the counts.

    Returns:
        Float array of shape ``(num_experts,)``. If ``normalize`` is ``True``
        and the total is zero, a uniform distribution is returned (no usage is
        treated as maximally uninformative rather than NaN).

    Raises:
        ValueError: If ``usage_counts`` is not 1-D or contains negatives.
    """
    counts = np.asarray(usage_counts, dtype=np.float64)
    if counts.ndim != 1:
        raise ValueError(f"usage_counts must be 1-D, got shape {counts.shape}")
    if np.any(counts < 0):
        raise ValueError("usage_counts must be non-negative")

    if not normalize:
        return counts

    total = counts.sum()
    if total <= 0:
        logger.warning("expert_usage_distribution: zero total usage; returning uniform")
        return np.full_like(counts, 1.0 / counts.shape[0])
    return counts / total


def shannon_entropy(distribution: np.ndarray, *, base: float = 2.0) -> float:
    """Compute the Shannon entropy of a probability distribution.

    Args:
        distribution: Array of shape ``(num_experts,)``. Need not be exactly
            normalized; it is renormalized internally.
        base: Logarithm base. ``2.0`` (default) gives entropy in bits, so the
            maximum for E experts is ``log2(E)``.

    Returns:
        Entropy as a non-negative float.

    Raises:
        ValueError: If ``distribution`` is not 1-D or contains negatives.
    """
    p = np.asarray(distribution, dtype=np.float64)
    if p.ndim != 1:
        raise ValueError(f"distribution must be 1-D, got shape {p.shape}")
    if np.any(p < 0):
        raise ValueError("distribution must be non-negative")

    total = p.sum()
    if total <= 0:
        return 0.0
    p = p / total
    nz = p > _EPS
    return float(-np.sum(p[nz] * (np.log(p[nz]) / np.log(base))))


def normalized_entropy(distribution: np.ndarray) -> float:
    """Return entropy normalized to ``[0, 1]`` by ``log(num_experts)``.

    Args:
        distribution: Array of shape ``(num_experts,)``.

    Returns:
        Normalized entropy in ``[0, 1]``; ``1.0`` for a uniform distribution,
        ``0.0`` for a one-hot distribution. Defined as ``0.0`` when there is at
        most one expert (no spread possible).
    """
    p = np.asarray(distribution, dtype=np.float64)
    num_experts = p.shape[0]
    if num_experts <= 1:
        return 0.0
    max_entropy = np.log2(num_experts)
    return float(shannon_entropy(p, base=2.0) / max_entropy)


def max_expert_share(distribution: np.ndarray) -> float:
    """Return the probability mass of the single most-used expert.

    Args:
        distribution: Array of shape ``(num_experts,)``.

    Returns:
        The maximum normalized share in ``[0, 1]``. ``1.0`` indicates a
        single expert captures all routing (extreme specialization);
        ``1/num_experts`` indicates perfectly uniform usage.
    """
    p = expert_usage_distribution(distribution, normalize=True)
    return float(np.max(p))


def specialization_index(distribution: np.ndarray) -> float:
    """Return a specialization index in ``[0, 1]`` (``1 - normalized entropy``).

    Args:
        distribution: Array of shape ``(num_experts,)``.

    Returns:
        ``0.0`` for uniform usage (no specialization), ``1.0`` for one-hot
        usage (maximal specialization). This is ``1 - normalized_entropy``.
    """
    return float(1.0 - normalized_entropy(distribution))


def coefficient_of_variation(usage_counts: np.ndarray) -> float:
    """Return the coefficient of variation (std / mean) of expert load.

    A standard load-balance diagnostic: ``0.0`` for perfectly balanced load,
    growing as load concentrates on fewer experts.

    Args:
        usage_counts: Array of shape ``(num_experts,)`` of per-expert loads
            (counts or fractions; CV is scale-invariant).

    Returns:
        The coefficient of variation as a non-negative float. Returns ``0.0``
        when the mean load is zero.
    """
    counts = np.asarray(usage_counts, dtype=np.float64)
    if counts.ndim != 1:
        raise ValueError(f"usage_counts must be 1-D, got shape {counts.shape}")
    mean = counts.mean()
    if mean <= _EPS:
        return 0.0
    # Population std (ddof=0): deterministic w.r.t. the observed load vector.
    return float(counts.std(ddof=0) / mean)


def load_balance_aux_fraction(
    usage_counts: np.ndarray,
    router_prob_mass: np.ndarray,
) -> float:
    """Switch-Transformer-style auxiliary load-balance term.

    Implements ``E * sum_i (f_i * P_i)`` where ``f_i`` is the fraction of
    tokens dispatched to expert ``i`` and ``P_i`` is the mean router
    probability assigned to expert ``i`` (Fedus et al., 2021, eq. 4 without the
    alpha coefficient). Minimized (== 1.0) under uniform dispatch and uniform
    router mass; larger values indicate imbalance.

    Args:
        usage_counts: Array of shape ``(num_experts,)`` of dispatch counts
            (``f_i`` is derived by normalizing).
        router_prob_mass: Array of shape ``(num_experts,)`` of summed (or mean)
            router probabilities per expert (``P_i`` is derived by
            normalizing).

    Returns:
        The auxiliary fraction as a float ``>= 1.0`` in the well-balanced limit.

    Raises:
        ValueError: If the two inputs have mismatched shapes.
    """
    f = expert_usage_distribution(usage_counts, normalize=True)
    p = np.asarray(router_prob_mass, dtype=np.float64)
    if p.shape != f.shape:
        raise ValueError(
            f"router_prob_mass shape {p.shape} != usage_counts shape {f.shape}"
        )
    if np.any(p < 0):
        raise ValueError("router_prob_mass must be non-negative")
    p_total = p.sum()
    p = p / p_total if p_total > 0 else np.full_like(p, 1.0 / p.shape[0])
    num_experts = f.shape[0]
    return float(num_experts * np.sum(f * p))


def jensen_shannon_divergence(
    dist_p: np.ndarray,
    dist_q: np.ndarray,
    *,
    base: float = 2.0,
) -> float:
    """Compute the Jensen-Shannon divergence between two distributions.

    JS divergence is symmetric and bounded: with ``base=2`` it lies in
    ``[0, 1]`` (0 for identical distributions, 1 for disjoint supports).

    Args:
        dist_p: Array of shape ``(num_experts,)``.
        dist_q: Array of shape ``(num_experts,)`` (same length as ``dist_p``).
        base: Logarithm base for the underlying KL terms.

    Returns:
        The JS divergence as a non-negative float.

    Raises:
        ValueError: If the inputs have mismatched shapes.
    """
    p = expert_usage_distribution(dist_p, normalize=True)
    q = expert_usage_distribution(dist_q, normalize=True)
    if p.shape != q.shape:
        raise ValueError(f"shape mismatch: {p.shape} vs {q.shape}")
    m = 0.5 * (p + q)
    js = 0.5 * _kl_divergence(p, m, base) + 0.5 * _kl_divergence(q, m, base)
    # JS divergence is mathematically non-negative; clamp away tiny float noise
    # introduced by the numerical epsilon in the KL denominator.
    return float(max(0.0, js))


def _kl_divergence(p: np.ndarray, q: np.ndarray, base: float) -> float:
    """KL(p || q) in the given log base; terms with ``p_i == 0`` contribute 0."""
    nz = p > _EPS
    return float(np.sum(p[nz] * (np.log(p[nz] / (q[nz] + _EPS)) / np.log(base))))


def pairwise_js_across_buckets(
    bucket_distributions: dict[int, np.ndarray],
) -> dict[tuple[int, int], float]:
    """Return pairwise JS divergence between every pair of timestep buckets.

    Also includes each-bucket-vs-marginal comparisons under the sentinel key
    ``(t_bucket, -1)``, where the marginal is the usage-weighted average over
    all buckets.

    Args:
        bucket_distributions: Mapping from timestep-bucket id to a
            ``(num_experts,)`` usage distribution (counts or normalized; each
            is renormalized internally).

    Returns:
        Mapping ``(t_a, t_b) -> js`` for every unordered pair ``t_a < t_b``,
        plus ``(t, -1) -> js`` for each bucket ``t`` against the marginal.
        Empty if fewer than one bucket is provided.
    """
    buckets = sorted(bucket_distributions.keys())
    if not buckets:
        return {}

    raw = {t: np.asarray(bucket_distributions[t], dtype=np.float64) for t in buckets}
    normed = {t: expert_usage_distribution(raw[t], normalize=True) for t in buckets}
    # Marginal = the pooled traffic distribution: SUM raw counts across buckets,
    # then normalize. Summing (not averaging the per-bucket distributions)
    # correctly weights buckets by their token traffic, so a low-traffic bucket
    # cannot dominate the marginal (fixes MINOR 8).
    marginal = expert_usage_distribution(
        np.sum(np.stack([raw[t] for t in buckets], axis=0), axis=0), normalize=True
    )

    result: dict[tuple[int, int], float] = {}
    for i, t_a in enumerate(buckets):
        result[(t_a, -1)] = jensen_shannon_divergence(normed[t_a], marginal)
        for t_b in buckets[i + 1:]:
            result[(t_a, t_b)] = jensen_shannon_divergence(normed[t_a], normed[t_b])
    return result


@dataclass(frozen=True)
class BootstrapNoiseFloor:
    """Within-t bootstrap null distribution for JS divergence.

    Attributes:
        mean: Mean of the bootstrap JS null distribution.
        ci_low: Lower confidence-interval bound (e.g. 2.5th percentile).
        ci_high: Upper confidence-interval bound (e.g. 97.5th percentile).
            This is the operational *noise floor*: an observed cross-t JS must
            exceed ``ci_high`` to count as specialization for H4.
        ci_level: The confidence level used (e.g. 0.95).
        n_resamples: Number of bootstrap resamples drawn.
    """

    mean: float
    ci_low: float
    ci_high: float
    ci_level: float
    n_resamples: int


def bootstrap_js_noise_floor(
    selections_a: np.ndarray,
    selections_b: np.ndarray,
    num_experts: int,
    *,
    n_resamples: int = 1000,
    ci_level: float = 0.95,
    seed: int = 42,
) -> BootstrapNoiseFloor:
    """Estimate the within-t JS noise floor for one specific bucket pair.

    The null hypothesis is "the two buckets are drawn from the SAME routing
    law". We pool the per-token selections of bucket A and bucket B, then
    repeatedly draw two disjoint samples *at the actual sizes* of A and B from
    the pool (sampling without replacement, matching the observed sizes), build
    a usage distribution for each, and measure their JS divergence. The
    resulting null distribution's upper CI bound is the noise floor that the
    observed cross-t JS for THIS pair must exceed.

    Resampling at the real (possibly unequal) bucket sizes -- rather than equal
    halves of a single bucket -- keeps the floor correctly scaled when buckets
    differ in token count (e.g. under early stopping). This fixes MAJOR 4.

    Args:
        selections_a: Integer array ``(n_a, top_k)`` of expert indices for
            bucket A. Values in ``[0, num_experts)``.
        selections_b: Integer array ``(n_b, top_k)`` of expert indices for
            bucket B.
        num_experts: Total number of experts (E).
        n_resamples: Number of bootstrap iterations.
        ci_level: Two-sided confidence level for the CI (e.g. 0.95).
        seed: RNG seed for reproducibility.

    Returns:
        A :class:`BootstrapNoiseFloor`. If either bucket has 0 tokens, an
        all-zero floor is returned.

    Raises:
        ValueError: On malformed input shapes or out-of-range expert indices.
    """
    sel_a = np.asarray(selections_a)
    sel_b = np.asarray(selections_b)
    for sel in (sel_a, sel_b):
        if sel.ndim != 2:
            raise ValueError(f"selections must be 2-D (n, top_k), got {sel.shape}")
        if sel.size and (sel.min() < 0 or sel.max() >= num_experts):
            raise ValueError("expert indices out of range [0, num_experts)")
    if not 0.0 < ci_level < 1.0:
        raise ValueError("ci_level must be in (0, 1)")

    n_a, n_b = sel_a.shape[0], sel_b.shape[0]
    pool = np.concatenate([sel_a, sel_b], axis=0) if (n_a or n_b) else sel_a
    n_total = pool.shape[0]
    if n_a < 1 or n_b < 1 or n_total < 2:
        logger.warning("bootstrap_js_noise_floor: empty bucket(s); returning zero floor")
        return BootstrapNoiseFloor(0.0, 0.0, 0.0, ci_level, 0)

    rng = np.random.default_rng(seed)
    js_values = np.empty(n_resamples, dtype=np.float64)
    for r in range(n_resamples):
        perm = rng.permutation(n_total)
        idx_a, idx_b = perm[:n_a], perm[n_a: n_a + n_b]
        counts_a = np.bincount(pool[idx_a].reshape(-1), minlength=num_experts)
        counts_b = np.bincount(pool[idx_b].reshape(-1), minlength=num_experts)
        js_values[r] = jensen_shannon_divergence(counts_a, counts_b)

    alpha = 1.0 - ci_level
    lo = float(np.quantile(js_values, alpha / 2.0))
    hi = float(np.quantile(js_values, 1.0 - alpha / 2.0))
    return BootstrapNoiseFloor(
        mean=float(js_values.mean()),
        ci_low=lo,
        ci_high=hi,
        ci_level=ci_level,
        n_resamples=n_resamples,
    )
