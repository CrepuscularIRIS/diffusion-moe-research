"""Track-structured data model for the H4 timestep-specialization test.

The H4 protocol (``plan/h4-test-protocol.md``) requires a representation that
makes the *trajectory-synchronous* permutation expressible: the exchangeability
unit is the denoising trajectory (= one prompt + one generated canvas), and the
permuted object is the per-call timestep-bucket label, shared across ALL
positions, layers, experts, and statistics.

This module holds :class:`H4Dataset` -- a compact, torch-free container of the
logged routing events organized so that:

- ``records[layer]`` is a flat list of routed visits at that layer, each
  carrying ``(traj_idx, call_idx, position, expert_ids, expert_mass)``;
- ``call_buckets[traj_idx]`` maps each call index ``s`` in trajectory ``r`` to
  its pre-registered timestep bucket ``b(t_{rs})``.

A trajectory-synchronous permutation draws ONE permutation of each trajectory's
call indices and relabels ``call_buckets`` accordingly; the same relabeling is
then applied to every layer's visits via the shared ``call_idx`` key.

The track key is ``i = (traj_idx, position)`` -- prompt and canvas are folded
into ``traj_idx`` (a trajectory IS one prompt+canvas), per the protocol's
``i = (prompt_id, trajectory/canvas_id, position p)``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

logger = logging.getLogger(__name__)

ExpertMassMode = str  # one of {"unweighted", "gate_weighted"}


@dataclass(frozen=True)
class VisitArray:
    """Columnar routed-visit records for ONE layer.

    All arrays share length ``n_visits`` (number of routed token-position visits
    at this layer across all trajectories/calls). ``expert_ids`` /
    ``expert_mass`` are 2-D ``(n_visits, top_k)``; each visit's mass sums to 1.

    Attributes:
        traj_idx: ``(n_visits,)`` trajectory index r per visit.
        call_idx: ``(n_visits,)`` denoising-call index s per visit.
        position: ``(n_visits,)`` token position p per visit.
        expert_ids: ``(n_visits, top_k)`` selected expert ids.
        expert_mass: ``(n_visits, top_k)`` per-rank mass (sums to 1 per visit).
    """

    traj_idx: np.ndarray
    call_idx: np.ndarray
    position: np.ndarray
    expert_ids: np.ndarray
    expert_mass: np.ndarray


@dataclass(frozen=True)
class H4Dataset:
    """Track-structured routing dataset for the H4 test.

    Attributes:
        num_experts: Total experts E.
        num_buckets: Pre-registered timestep buckets K.
        layers: Sorted layer indices present.
        visits_by_layer: ``layer -> VisitArray``.
        call_buckets: ``traj_idx -> {call_idx: bucket}`` observed labeling.
    """

    num_experts: int
    num_buckets: int
    layers: list[int]
    visits_by_layer: dict[int, VisitArray]
    call_buckets: dict[int, dict[int, int]] = field(default_factory=dict)

    @property
    def num_trajectories(self) -> int:
        """Number of distinct trajectories (exchangeability units)."""
        return len(self.call_buckets)


def expert_mass_from_topk(
    topk_ids: np.ndarray,
    *,
    top_k: int,
    gate_probs: np.ndarray | None = None,
    mode: ExpertMassMode = "unweighted",
) -> np.ndarray:
    """Compute per-rank expert mass for a batch of visits.

    Args:
        topk_ids: ``(n, top_k)`` selected expert ids.
        top_k: k (number of selected experts per visit).
        gate_probs: ``(n, top_k)`` router weights over the selected experts
            (required for ``"gate_weighted"``; must sum to 1 per visit).
        mode: ``"unweighted"`` (primary: uniform 1/k mass) or ``"gate_weighted"``.

    Returns:
        ``(n, top_k)`` mass array; each row sums to 1.

    Raises:
        ValueError: If ``mode`` is unknown or ``gate_probs`` missing/ill-shaped.
    """
    ids = np.asarray(topk_ids)
    n = ids.shape[0]
    if mode == "unweighted":
        return np.full((n, top_k), 1.0 / top_k, dtype=np.float64)
    if mode == "gate_weighted":
        if gate_probs is None:
            raise ValueError("gate_weighted mode requires gate_probs")
        w = np.asarray(gate_probs, dtype=np.float64)
        if w.shape != ids.shape:
            raise ValueError(f"gate_probs shape {w.shape} != topk_ids {ids.shape}")
        row_sums = w.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums > 0, row_sums, 1.0)
        return w / row_sums
    raise ValueError(f"unknown expert-mass mode '{mode}'")


def build_dataset(
    layer_visits: dict[int, dict[str, np.ndarray]],
    call_buckets: dict[int, dict[int, int]],
    num_experts: int,
    num_buckets: int,
    *,
    top_k: int,
    mode: ExpertMassMode = "unweighted",
) -> H4Dataset:
    """Assemble an :class:`H4Dataset` from raw per-layer visit columns.

    Args:
        layer_visits: ``layer -> {"traj_idx","call_idx","position","expert_ids"
            [,"gate_probs"]}``. ``expert_ids`` is ``(n, top_k)``.
        call_buckets: ``traj_idx -> {call_idx: bucket}``.
        num_experts: Total experts E.
        num_buckets: Pre-registered buckets K.
        top_k: k.
        mode: Expert-mass mode (see :func:`expert_mass_from_topk`).

    Returns:
        A populated :class:`H4Dataset`.

    Raises:
        ValueError: On malformed inputs (bad shapes, out-of-range experts).
    """
    visits_by_layer: dict[int, VisitArray] = {}
    for layer in sorted(layer_visits):
        cols = layer_visits[layer]
        ids = np.asarray(cols["expert_ids"], dtype=np.int64)
        if ids.ndim != 2 or ids.shape[1] != top_k:
            raise ValueError(f"layer {layer}: expert_ids must be (n, {top_k}), got {ids.shape}")
        if ids.size and (ids.min() < 0 or ids.max() >= num_experts):
            raise ValueError(f"layer {layer}: expert id out of range [0,{num_experts})")
        mass = expert_mass_from_topk(
            ids, top_k=top_k, gate_probs=cols.get("gate_probs"), mode=mode
        )
        visits_by_layer[layer] = VisitArray(
            traj_idx=np.asarray(cols["traj_idx"], dtype=np.int64),
            call_idx=np.asarray(cols["call_idx"], dtype=np.int64),
            position=np.asarray(cols["position"], dtype=np.int64),
            expert_ids=ids,
            expert_mass=mass,
        )
    return H4Dataset(
        num_experts=num_experts,
        num_buckets=num_buckets,
        layers=sorted(layer_visits),
        visits_by_layer=visits_by_layer,
        call_buckets={int(r): {int(s): int(b) for s, b in d.items()}
                      for r, d in call_buckets.items()},
    )
