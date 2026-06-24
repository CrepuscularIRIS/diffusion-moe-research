"""TEST-ONLY broken H4 variant + discrimination harness (review gap 1).

This module is NOT part of the production decision path. It exists solely so the
validation suite can PROVE that the production shared-draw maxT permutation is
load-bearing: it reimplements the global maxT test with a DELIBERATELY BROKEN
per-layer-INDEPENDENT permutation (a separate draw per layer), then a harness
collects global-null p-values under both the correct and broken variants so the
tests can show they are measurably different on a cross-layer-correlated null.

Do not import this from production code. The correct test lives in
``direction_c.h4_test.run_h4_test``.
"""

from __future__ import annotations

import logging

import numpy as np

from direction_c.h4_data import H4Dataset
from direction_c.h4_test import (
    _build_layer_index,
    _build_slot_map,
    _g_statistic,
    _permute_slot_buckets,
)

logger = logging.getLogger(__name__)


def _permute_independent_per_layer(smap, rng: np.random.Generator,
                                   num_layers: int) -> list[np.ndarray]:
    """BROKEN: draw a SEPARATE trajectory-synchronous relabel per layer.

    This violates the protocol's "one shared draw feeds all layers": each layer
    gets its own independent permutation, destroying the cross-layer correlation
    that the correct shared draw preserves. TEST-ONLY.

    Args:
        smap: The slot map.
        rng: RNG.
        num_layers: Number of layers (each gets its own draw).

    Returns:
        A list of ``num_layers`` independently-permuted slot-bucket arrays.
    """
    return [_permute_slot_buckets(smap, rng) for _ in range(num_layers)]


def global_pvalue(
    dataset: H4Dataset,
    *,
    shared_draw: bool,
    b_perm: int = 99,
    seed: int = 0,
) -> float:
    """Global maxT p-value under the correct (shared) or broken (per-layer) draw.

    Both variants compute ``M_obs = max_L T_L(D)`` identically; they differ ONLY
    in how the permutation null ``M^(m)`` is built:

    - ``shared_draw=True`` (CORRECT): one trajectory-synchronous relabel per
      permutation, applied to ALL layers (production behavior).
    - ``shared_draw=False`` (BROKEN): an INDEPENDENT relabel per layer each
      permutation -- the bug this harness exposes.

    Args:
        dataset: An :class:`H4Dataset` (under H0 for type-I characterization).
        shared_draw: Whether to use the correct shared draw.
        b_perm: Permutations.
        seed: RNG seed.

    Returns:
        The global maxT p-value ``(1 + #{M^(m) >= M_obs}) / (b_perm + 1)``.
    """
    layers = dataset.layers
    smap, key_to_slot = _build_slot_map(dataset.call_buckets)
    idx_by_layer = {L: _build_layer_index(dataset.visits_by_layer[L], key_to_slot)
                    for L in layers}

    t_obs = np.array([
        _g_statistic(idx_by_layer[L], smap.slot_bucket,
                     dataset.num_buckets, dataset.num_experts)[0]
        for L in layers
    ])
    m_obs = float(t_obs.max()) if len(layers) else 0.0

    rng = np.random.default_rng(seed)
    m_perm = np.zeros(b_perm)
    for m in range(b_perm):
        if shared_draw:
            perm = _permute_slot_buckets(smap, rng)
            stats = [
                _g_statistic(idx_by_layer[L], perm, dataset.num_buckets,
                             dataset.num_experts)[0]
                for L in layers
            ]
        else:
            perms = _permute_independent_per_layer(smap, rng, len(layers))
            stats = [
                _g_statistic(idx_by_layer[L], perms[j], dataset.num_buckets,
                             dataset.num_experts)[0]
                for j, L in enumerate(layers)
            ]
        m_perm[m] = max(stats) if stats else 0.0

    return float((1.0 + np.sum(m_perm >= m_obs)) / (b_perm + 1.0))


def collect_global_pvalues(
    make_null,
    *,
    shared_draw: bool,
    r_null: int,
    b_perm: int = 99,
    seed0: int = 0,
) -> np.ndarray:
    """Collect global-null p-values over ``r_null`` datasets from ``make_null``.

    Args:
        make_null: Callable ``(seed) -> H4Dataset`` generating an H0 dataset.
        shared_draw: Correct (True) or broken (False) permutation.
        r_null: Number of null datasets.
        b_perm: Permutations per test.
        seed0: Base seed.

    Returns:
        Array ``(r_null,)`` of global maxT p-values.
    """
    rng = np.random.default_rng(seed0)
    pvals = np.empty(r_null)
    for i in range(r_null):
        ds = make_null(int(rng.integers(1 << 30)))
        pvals[i] = global_pvalue(ds, shared_draw=shared_draw, b_perm=b_perm,
                                 seed=int(rng.integers(1 << 30)))
    return pvals
