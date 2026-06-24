"""Track-stratified conditional-MI / G test for H4 with FWER control.

Implements the protocol in ``plan/h4-test-protocol.md`` EXACTLY:

- **Statistic** (primary, per layer L): track-stratified G / conditional MI
  ``T_L = 2 Σ_i Σ_b Σ_e C_ibe · log( (C_ibe · n_i) / (n_ib · C_i·e) )`` with
  track ``i = (trajectory, position)``, ``C`` from per-visit expert mass,
  C=0 terms contribute 0, NO pseudocounts, NO asymptotic chi-square.
- **Permutation** (the core fix): TRAJECTORY-SYNCHRONOUS. For each trajectory r
  draw ONE permutation of its denoising-call indices; the SAME relabeling of the
  per-call bucket labels is applied to every position, layer, and expert.
- **FWER**: ``M = max_L T_L``; one shared permutation draw feeds ALL layers each
  iteration; global ``p = (1+#{M^(m) >= M_obs})/(B_perm+1)``; layer-wise
  single-step maxT adjusted p-values use the SAME ``M^(m)`` draws.
- **Effect sizes**: ``I_L = T_L/(2 N_L)`` (nats/visit), ``NMI_L``, bias-corrected
  ``ΔNMI_L`` (subtract permutation-null median), cluster-bootstrap 95% CIs over
  trajectories.

Pre-registration (lock BEFORE seeing results; see README): ``alpha = 0.05``,
``K = 8`` equal-count timestep buckets, layer set = decoder layers 0..29,
``B_perm = 19999`` (paper) / ``>= 9999`` (min); primary statistic = stratified-G;
primary permutation = trajectory-synchronous; correction = shared-draw maxT.

Honesty caveat (must appear in the paper): passive logs establish *within-
trajectory timestep ASSOCIATION* only. A causal "experts read t" claim needs a
timestep-swap intervention (freeze canvas, replay router with a different
t-embedding, test if expert selection changes). This module proves association.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from direction_c.h4_data import H4Dataset, VisitArray

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _SlotMap:
    """Global ``(traj, call) -> slot`` map enabling vectorized permutation.

    A trajectory-synchronous permutation permutes the per-slot bucket labels
    *within each trajectory's contiguous slot block*. Each routing event then
    gathers its bucket via ``slot_buckets[event_slot]`` -- a single vectorized
    index, no per-trajectory Python loop in the hot path.

    Attributes:
        slot_bucket: ``(n_slots,)`` observed bucket per slot.
        traj_of_slot: ``(n_slots,)`` trajectory of each slot (sorted blocks).
        traj_starts: start offset of each trajectory's slot block.
        traj_lengths: number of slots (= calls) per trajectory.
        n_slots: total slots.
    """

    slot_bucket: np.ndarray
    traj_of_slot: np.ndarray
    traj_starts: np.ndarray
    traj_lengths: np.ndarray
    n_slots: int


@dataclass(frozen=True)
class _LayerIndex:
    """Precomputed flattened indices for fast repeated G evaluation of one layer.

    Each (visit, rank) event carries its compacted track id, expert id, mass,
    and the GLOBAL SLOT id of its (trajectory, call). The per-permutation bucket
    of an event is ``slot_bucket[event_slot]`` (vectorized gather).
    """

    track_id: np.ndarray   # (n_events,) compacted track index i
    expert_id: np.ndarray  # (n_events,) expert e
    mass: np.ndarray       # (n_events,) per-event mass
    event_slot: np.ndarray  # (n_events,) global slot id of the (traj, call)
    n_tracks: int


@dataclass(frozen=True)
class LayerH4Result:
    """Per-layer test result and effect sizes.

    Attributes:
        layer_idx: Decoder layer index.
        t_stat: Observed stratified-G statistic ``T_L``.
        n_visits: Total visit mass ``N_L``.
        p_adj_maxt: Single-step maxT FWER-adjusted layer p-value.
        mi_nats: ``I_L = T_L/(2 N_L)`` (nats per routed visit).
        nmi: Normalized MI ``I_L / H(B|track)``.
        delta_nmi: Bias-corrected excess NMI (obs minus perm-null-median MI).
    """

    layer_idx: int
    t_stat: float
    n_visits: float
    p_adj_maxt: float
    mi_nats: float
    nmi: float
    delta_nmi: float


@dataclass(frozen=True)
class H4Result:
    """Outcome of the full H4 test.

    Attributes:
        supported: ``True`` iff global null rejected (``p_global <= alpha``).
        alpha: Significance level.
        p_global: Shared-draw maxT global p-value.
        m_obs: Observed ``max_L T_L``.
        b_perm: Number of permutations.
        significant_layers: Layers with ``p_adj_maxt <= alpha``.
        per_layer: Per-layer results + effect sizes.
        h_bucket_given_track: ``H(B|track)`` used to normalize MI.
    """

    supported: bool
    alpha: float
    p_global: float
    m_obs: float
    b_perm: int
    significant_layers: list[int]
    per_layer: list[LayerH4Result] = field(default_factory=list)
    h_bucket_given_track: float = 0.0


def _build_slot_map(call_buckets: dict[int, dict[int, int]]) -> tuple[_SlotMap, dict[tuple[int, int], int]]:
    """Build the global ``(traj, call) -> slot`` map and observed slot buckets.

    Slots are laid out in contiguous per-trajectory blocks (trajectories sorted
    ascending, calls sorted ascending within each), so a trajectory-synchronous
    permutation is a within-block shuffle.

    Returns:
        ``(slot_map, key_to_slot)`` where ``key_to_slot[(traj, call)] = slot``.
    """
    trajs = sorted(call_buckets)
    slot_bucket: list[int] = []
    traj_of_slot: list[int] = []
    traj_starts: list[int] = []
    traj_lengths: list[int] = []
    key_to_slot: dict[tuple[int, int], int] = {}
    cursor = 0
    for r in trajs:
        c2b = call_buckets[r]
        calls = sorted(c2b)
        traj_starts.append(cursor)
        traj_lengths.append(len(calls))
        for s in calls:
            key_to_slot[(r, s)] = cursor
            slot_bucket.append(int(c2b[s]))
            traj_of_slot.append(r)
            cursor += 1
    smap = _SlotMap(
        slot_bucket=np.asarray(slot_bucket, dtype=np.int64),
        traj_of_slot=np.asarray(traj_of_slot, dtype=np.int64),
        traj_starts=np.asarray(traj_starts, dtype=np.int64),
        traj_lengths=np.asarray(traj_lengths, dtype=np.int64),
        n_slots=cursor,
    )
    return smap, key_to_slot


def _build_layer_index(visits: VisitArray, key_to_slot: dict[tuple[int, int], int]) -> _LayerIndex:
    """Flatten a layer's visits into per-(visit,rank) event arrays + slot ids."""
    n_visits, top_k = visits.expert_ids.shape
    if n_visits == 0:
        empty = np.empty(0, dtype=np.int64)
        return _LayerIndex(empty, empty, np.empty(0), empty, 0)
    track_keys = visits.traj_idx.astype(np.int64) * (int(visits.position.max()) + 1) \
        + visits.position.astype(np.int64)
    _, track_id_per_visit = np.unique(track_keys, return_inverse=True)
    n_tracks = int(track_id_per_visit.max()) + 1
    slot_per_visit = np.array(
        [key_to_slot[(int(r), int(s))] for r, s in zip(visits.traj_idx, visits.call_idx)],
        dtype=np.int64,
    )
    track_id = np.repeat(track_id_per_visit, top_k)
    expert_id = visits.expert_ids.reshape(-1).astype(np.int64)
    mass = visits.expert_mass.reshape(-1).astype(np.float64)
    event_slot = np.repeat(slot_per_visit, top_k)
    return _LayerIndex(track_id, expert_id, mass, event_slot, n_tracks)


def _g_statistic(idx: _LayerIndex, slot_bucket: np.ndarray, num_buckets: int,
                 num_experts: int) -> tuple[float, float]:
    """Compute stratified-G ``T_L`` and total mass ``N_L`` for one layer.

    Args:
        idx: Precomputed layer event index.
        slot_bucket: ``(n_slots,)`` bucket per global slot (the permuted labels).
        num_buckets: K.
        num_experts: E.

    Returns:
        ``(T_L, N_L)``.
    """
    if idx.track_id.size == 0:
        return 0.0, 0.0
    bucket_of_event = slot_bucket[idx.event_slot]
    nt = idx.n_tracks
    tbe = (idx.track_id * num_buckets + bucket_of_event) * num_experts + idx.expert_id
    tb = idx.track_id * num_buckets + bucket_of_event
    te = idx.track_id * num_experts + idx.expert_id

    c_tbe = np.bincount(tbe, weights=idx.mass, minlength=nt * num_buckets * num_experts)
    n_tb = np.bincount(tb, weights=idx.mass, minlength=nt * num_buckets)
    c_te = np.bincount(te, weights=idx.mass, minlength=nt * num_experts)
    n_i = np.bincount(idx.track_id, weights=idx.mass, minlength=nt)

    nz = np.nonzero(c_tbe)[0]
    if nz.size == 0:
        return 0.0, float(n_i.sum())
    c = c_tbe[nz]
    track = nz // (num_buckets * num_experts)
    rem = nz % (num_buckets * num_experts)
    b = rem // num_experts
    e = rem % num_experts
    nib = n_tb[track * num_buckets + b]
    cie = c_te[track * num_experts + e]
    ni = n_i[track]
    ratio = (c * ni) / (nib * cie)
    t_stat = float(2.0 * np.sum(c * np.log(ratio)))
    return t_stat, float(n_i.sum())


def _permute_slot_buckets(smap: _SlotMap, rng: np.random.Generator) -> np.ndarray:
    """Trajectory-synchronous relabel: shuffle bucket labels within each block."""
    out = smap.slot_bucket.copy()
    for start, length in zip(smap.traj_starts, smap.traj_lengths):
        if length > 1:
            block = out[start:start + length]
            rng.shuffle(block)
            out[start:start + length] = block
    return out


def _bucket_entropy_given_track(idx: _LayerIndex, slot_bucket: np.ndarray,
                                num_buckets: int) -> float:
    """``H(B|track)`` (nats), mass-weighted over tracks; uses one layer's events."""
    if idx.track_id.size == 0:
        return 0.0
    bucket_of_event = slot_bucket[idx.event_slot]
    nt = idx.n_tracks
    tb = idx.track_id * num_buckets + bucket_of_event
    n_tb = np.bincount(tb, weights=idx.mass, minlength=nt * num_buckets).reshape(nt, num_buckets)
    n_i = n_tb.sum(axis=1)
    total = n_i.sum()
    if total <= 0:
        return 0.0
    h = 0.0
    for i in range(nt):
        if n_i[i] <= 0:
            continue
        probs = n_tb[i] / n_i[i]
        nz = probs > 0
        h += n_i[i] * float(-np.sum(probs[nz] * np.log(probs[nz])))
    return h / total


def run_h4_test(
    dataset: H4Dataset,
    *,
    alpha: float = 0.05,
    b_perm: int = 19999,
    seed: int = 12345,
) -> H4Result:
    """Run the full H4 test: stratified-G + trajectory-synchronous maxT FWER.

    Args:
        dataset: Track-structured :class:`H4Dataset`.
        alpha: Significance level (pre-registered 0.05).
        b_perm: Permutations (pre-registered 19999; >=9999 min; smaller for tests).
        seed: RNG seed for reproducibility.

    Returns:
        An :class:`H4Result` with the global decision, layer maxT p-values, and
        effect sizes.
    """
    layers = dataset.layers
    smap, key_to_slot = _build_slot_map(dataset.call_buckets)
    idx_by_layer = {L: _build_layer_index(dataset.visits_by_layer[L], key_to_slot)
                    for L in layers}

    t_obs = np.zeros(len(layers))
    n_obs = np.zeros(len(layers))
    for j, L in enumerate(layers):
        t_obs[j], n_obs[j] = _g_statistic(
            idx_by_layer[L], smap.slot_bucket, dataset.num_buckets, dataset.num_experts)
    m_obs = float(t_obs.max()) if len(layers) else 0.0

    h_bgt = (_bucket_entropy_given_track(idx_by_layer[layers[0]],
                                         smap.slot_bucket, dataset.num_buckets)
             if layers else 0.0)

    rng = np.random.default_rng(seed)
    t_perm = np.zeros((b_perm, len(layers)))
    m_perm = np.zeros(b_perm)
    for m in range(b_perm):
        perm_slot_bucket = _permute_slot_buckets(smap, rng)
        for j, L in enumerate(layers):
            t_perm[m, j], _ = _g_statistic(
                idx_by_layer[L], perm_slot_bucket, dataset.num_buckets, dataset.num_experts)
        m_perm[m] = t_perm[m, :].max() if len(layers) else 0.0

    p_global = float((1.0 + np.sum(m_perm >= m_obs)) / (b_perm + 1.0))
    i_obs = np.where(n_obs > 0, t_obs / (2.0 * np.maximum(n_obs, 1e-12)), 0.0)
    i_perm = t_perm / (2.0 * np.maximum(n_obs[None, :], 1e-12))
    i_perm_median = np.median(i_perm, axis=0) if b_perm > 0 else np.zeros(len(layers))

    per_layer: list[LayerH4Result] = []
    significant: list[int] = []
    for j, L in enumerate(layers):
        p_adj = float((1.0 + np.sum(m_perm >= t_obs[j])) / (b_perm + 1.0))
        if p_adj <= alpha:
            significant.append(L)
        nmi = i_obs[j] / h_bgt if h_bgt > 0 else 0.0
        delta_nmi = (i_obs[j] - i_perm_median[j]) / h_bgt if h_bgt > 0 else 0.0
        per_layer.append(LayerH4Result(
            layer_idx=L, t_stat=float(t_obs[j]), n_visits=float(n_obs[j]),
            p_adj_maxt=p_adj, mi_nats=float(i_obs[j]), nmi=float(nmi),
            delta_nmi=float(delta_nmi),
        ))

    return H4Result(
        supported=p_global <= alpha,
        alpha=alpha,
        p_global=p_global,
        m_obs=m_obs,
        b_perm=b_perm,
        significant_layers=sorted(significant),
        per_layer=per_layer,
        h_bucket_given_track=h_bgt,
    )


def cluster_bootstrap_nmi(
    dataset: H4Dataset,
    layer: int,
    *,
    n_boot: int = 2000,
    seed: int = 7,
) -> tuple[float, float]:
    """Cluster-bootstrap 95% CI for a layer's NMI, resampling trajectories.

    Args:
        dataset: The dataset.
        layer: Layer to bootstrap.
        n_boot: Bootstrap resamples (protocol: >= 2000).
        seed: RNG seed.

    Returns:
        ``(ci_low, ci_high)`` 95% percentile CI of NMI over trajectory resamples.
    """
    rng = np.random.default_rng(seed)
    trajs = np.array(sorted(dataset.call_buckets))
    if trajs.size == 0:
        return 0.0, 0.0
    visits = dataset.visits_by_layer[layer]
    # Index visits by trajectory once for fast resampling.
    visit_rows_by_traj = {int(r): np.nonzero(visits.traj_idx == r)[0] for r in trajs}
    vals = np.empty(n_boot)
    for bsi in range(n_boot):
        chosen = rng.choice(trajs, size=trajs.size, replace=True)
        # Relabel each draw with a fresh trajectory id so duplicate draws keep
        # DISTINCT tracks/slots (resampling-with-replacement correctness).
        sub_traj, sub_call, sub_pos, sub_ids, sub_mass = [], [], [], [], []
        sub_cb: dict[int, dict[int, int]] = {}
        for new_r, orig_r in enumerate(chosen):
            rows = visit_rows_by_traj[int(orig_r)]
            sub_traj.append(np.full(rows.size, new_r, dtype=np.int64))
            sub_call.append(visits.call_idx[rows])
            sub_pos.append(visits.position[rows])
            sub_ids.append(visits.expert_ids[rows])
            sub_mass.append(visits.expert_mass[rows])
            sub_cb[new_r] = dict(dataset.call_buckets[int(orig_r)])
        sub = VisitArray(
            traj_idx=np.concatenate(sub_traj), call_idx=np.concatenate(sub_call),
            position=np.concatenate(sub_pos), expert_ids=np.concatenate(sub_ids),
            expert_mass=np.concatenate(sub_mass),
        )
        smap, key_to_slot = _build_slot_map(sub_cb)
        idx = _build_layer_index(sub, key_to_slot)
        t, n = _g_statistic(idx, smap.slot_bucket, dataset.num_buckets, dataset.num_experts)
        h = _bucket_entropy_given_track(idx, smap.slot_bucket, dataset.num_buckets)
        i_nats = t / (2.0 * n) if n > 0 else 0.0
        vals[bsi] = i_nats / h if h > 0 else 0.0
    return float(np.quantile(vals, 0.025)), float(np.quantile(vals, 0.975))
