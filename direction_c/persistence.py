"""Disk persistence for recorded MoE routing selections.

Records are flattened into columnar arrays keyed by
``(record_id, tower, layer_idx, t_bucket/timestep, token, slot, expert)`` and
stored as a single compressed ``.npz``. This format is torch-free on read, so
the metrics / decision layers can load it without importing transformers/CUDA.

``record_id`` is the globally-unique key for each router invocation. Combined
with the per-record local ``token_idx`` it forms a collision-free token key:
distinct invocations that fall in the same ``(layer, t_bucket)`` are kept
separate, so reconstruction never silently overwrites tokens (fixes FATAL 1).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:  # avoid a runtime import cycle with probe.py
    from direction_c.probe import ProbeConfig, RouterRecord

logger = logging.getLogger(__name__)

# Numeric codes for the ``tower`` column.
TOWER_DECODER: int = 0
TOWER_ENCODER: int = 1


def save_records(
    records: list["RouterRecord"],
    config: "ProbeConfig",
    run_name: str,
) -> Path:
    """Persist routing records to ``<output_dir>/<run_name>_routing.npz``.

    Stores one row per (record, token, slot) selection, plus -- when router
    probabilities were captured -- a per-cell summed probability-mass matrix so
    the switch-transformer aux-loss metric is reproducible offline (MINOR 7).

    Args:
        records: Captured :class:`~direction_c.probe.RouterRecord` objects.
        config: The probe configuration (supplies ``output_dir`` and metadata).
        run_name: Output file stem.

    Returns:
        Path to the written ``.npz`` file.
    """
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{run_name}_routing.npz"

    cols: dict[str, list[np.ndarray]] = {
        k: [] for k in ("rid", "layer", "tower", "t", "tb", "token", "slot",
                        "expert", "weight", "prompt", "canvas", "call")
    }
    # Optional per-(record) summed router probability mass.
    prob_keys: list[tuple[int, int, int, int]] = []
    prob_mass: list[np.ndarray] = []
    # Per-record log-SNR table keyed by record_id (H4 sensitivity field).
    log_snr_keys: list[int] = []
    log_snr_vals: list[float] = []

    for rec in records:
        num_tokens, top_k = rec.top_k_index.shape
        n = num_tokens * top_k
        tower_code = TOWER_DECODER if rec.tower == "decoder" else TOWER_ENCODER
        token_grid = np.repeat(np.arange(num_tokens, dtype=np.int32), top_k)
        slot_grid = np.tile(np.arange(top_k, dtype=np.int8), num_tokens)

        cols["rid"].append(np.full(n, rec.record_id, dtype=np.int64))
        cols["layer"].append(np.full(n, rec.layer_idx, dtype=np.int32))
        cols["tower"].append(np.full(n, tower_code, dtype=np.int8))
        cols["t"].append(np.full(n, rec.timestep, dtype=np.int32))
        cols["tb"].append(np.full(n, rec.t_bucket, dtype=np.int32))
        cols["token"].append(token_grid)
        cols["slot"].append(slot_grid)
        cols["expert"].append(rec.top_k_index.reshape(-1).astype(np.int32))
        cols["weight"].append(rec.top_k_weights.reshape(-1).astype(np.float32))
        # H4 trajectory metadata (constant within a record; compresses well).
        cols["prompt"].append(np.full(n, rec.prompt_id, dtype=np.int32))
        cols["canvas"].append(np.full(n, rec.canvas_id, dtype=np.int32))
        cols["call"].append(np.full(n, rec.call_index, dtype=np.int32))

        log_snr_keys.append(rec.record_id)
        log_snr_vals.append(rec.log_snr)
        if rec.router_probabilities is not None:
            prob_keys.append((rec.record_id, rec.layer_idx, tower_code, rec.t_bucket))
            prob_mass.append(rec.router_probabilities.sum(axis=0).astype(np.float64))

    def _cat(name: str, dtype: type) -> np.ndarray:
        parts = cols[name]
        return np.concatenate(parts) if parts else np.empty(0, dtype=dtype)

    payload: dict[str, np.ndarray] = {
        "record_id": _cat("rid", np.int64),
        "layer_idx": _cat("layer", np.int32),
        "tower": _cat("tower", np.int8),
        "timestep": _cat("t", np.int32),
        "t_bucket": _cat("tb", np.int32),
        "token_idx": _cat("token", np.int32),
        "slot": _cat("slot", np.int8),
        "expert": _cat("expert", np.int32),
        "weight": _cat("weight", np.float32),
        "prompt_id": _cat("prompt", np.int32),
        "canvas_id": _cat("canvas", np.int32),
        "call_index": _cat("call", np.int32),
        "log_snr_keys": np.asarray(log_snr_keys, dtype=np.int64),
        "log_snr_vals": np.asarray(log_snr_vals, dtype=np.float64),
        "num_experts": np.asarray([config.num_experts], dtype=np.int32),
        "top_k": np.asarray([config.top_k], dtype=np.int32),
        "seed": np.asarray([config.seed], dtype=np.int32),
    }
    if prob_mass:
        payload["prob_keys"] = np.asarray(prob_keys, dtype=np.int64)
        payload["prob_mass"] = np.stack(prob_mass, axis=0)

    np.savez_compressed(path, **payload)
    logger.info("Saved %d selection rows to %s", payload["expert"].shape[0], path)
    return path


def load_usage_counts(
    path: str | Path,
    tower: str = "decoder",
) -> dict[tuple[int, int], np.ndarray]:
    """Aggregate usage counts per (layer, t_bucket) across ALL records.

    Counts every (token, slot) selection from every record, so multiple
    prompts/steps in the same cell accumulate correctly.

    Args:
        path: Path to a ``*_routing.npz`` produced by :func:`save_records`.
        tower: Which tower to aggregate (``"decoder"`` or ``"encoder"``).

    Returns:
        Mapping ``(layer_idx, t_bucket) -> usage_counts[num_experts]``.
    """
    data = np.load(Path(path))
    num_experts = int(data["num_experts"][0])
    tower_code = TOWER_DECODER if tower == "decoder" else TOWER_ENCODER
    mask = data["tower"] == tower_code

    layers = data["layer_idx"][mask]
    buckets = data["t_bucket"][mask]
    experts = data["expert"][mask]

    result: dict[tuple[int, int], np.ndarray] = {}
    for layer in np.unique(layers):
        layer_mask = layers == layer
        for bucket in np.unique(buckets[layer_mask]):
            sel = layer_mask & (buckets == bucket)
            counts = np.bincount(experts[sel], minlength=num_experts).astype(np.int64)
            result[(int(layer), int(bucket))] = counts
    return result


def load_token_selections(
    path: str | Path,
    layer_idx: int,
    t_bucket: int,
    tower: str = "decoder",
) -> np.ndarray:
    """Reconstruct ALL token selections for one (layer, bucket) cell.

    Tokens are keyed by ``(record_id, local token_idx)`` so selections from
    distinct invocations never collide (fixes FATAL 1). Every selected token in
    the cell -- across all records -- is returned.

    Args:
        path: Path to a ``*_routing.npz``.
        layer_idx: Layer to extract.
        t_bucket: Timestep bucket to extract.
        tower: Which tower (``"decoder"`` or ``"encoder"``).

    Returns:
        Integer array ``(num_tokens, top_k)`` of selected expert indices for the
        whole cell. Empty ``(0, top_k)`` if the cell has no records.
    """
    data = np.load(Path(path))
    top_k = int(data["top_k"][0])
    tower_code = TOWER_DECODER if tower == "decoder" else TOWER_ENCODER
    mask = (
        (data["tower"] == tower_code)
        & (data["layer_idx"] == layer_idx)
        & (data["t_bucket"] == t_bucket)
    )
    experts = data["expert"][mask]
    if experts.size == 0:
        return np.empty((0, top_k), dtype=np.int32)

    rids = data["record_id"][mask]
    tokens = data["token_idx"][mask]
    slots = data["slot"][mask]
    # Build a unique row per (record_id, local token) so nothing overwrites.
    pair = np.stack([rids, tokens], axis=1)
    _, row_of = np.unique(pair, axis=0, return_inverse=True)
    out = np.full((row_of.max() + 1, top_k), -1, dtype=np.int32)
    out[row_of, slots] = experts
    return out


def load_h4_dataset(
    path: str | Path,
    *,
    tower: str = "decoder",
    mode: str = "unweighted",
):
    """Load a saved ``.npz`` into a track-structured :class:`H4Dataset`.

    Reconstructs, for the H4 protocol test:
    - the exchangeability unit = trajectory ``(prompt_id, canvas_id)`` (mapped to
      a contiguous integer ``traj_idx``);
    - the denoising-call index ``s`` per visit (from the ``call_index`` column);
    - the token position ``p`` (from ``token_idx``);
    - per-layer top-k selections + gate weights;
    - the observed ``call_buckets[traj] = {s: bucket}`` table.

    Args:
        path: Path to a ``*_routing.npz``.
        tower: Which tower (``"decoder"`` -- decoder is the denoising loop).
        mode: Expert-mass mode passed to :func:`build_dataset`
            (``"unweighted"`` primary, ``"gate_weighted"`` robustness).

    Returns:
        An :class:`direction_c.h4_data.H4Dataset`.
    """
    from direction_c.h4_data import build_dataset  # local import: torch-free

    data = np.load(Path(path))
    top_k = int(data["top_k"][0])
    num_experts = int(data["num_experts"][0])
    num_buckets = int(data["t_bucket"].max()) + 1 if data["t_bucket"].size else 1
    tower_code = TOWER_DECODER if tower == "decoder" else TOWER_ENCODER
    base = data["tower"] == tower_code

    # Map trajectory (prompt, canvas) -> contiguous traj_idx.
    pc = np.stack([data["prompt_id"][base], data["canvas_id"][base]], axis=1)
    uniq_traj, traj_of_row = np.unique(pc, axis=0, return_inverse=True)
    call_col = data["call_index"][base]

    # Observed call_buckets table.
    call_buckets: dict[int, dict[int, int]] = {}
    tb_col = data["t_bucket"][base]
    for r in range(uniq_traj.shape[0]):
        rmask = traj_of_row == r
        for s, b in zip(call_col[rmask], tb_col[rmask]):
            call_buckets.setdefault(int(r), {})[int(s)] = int(b)

    layer_visits: dict[int, dict[str, np.ndarray]] = {}
    layer_col = data["layer_idx"][base]
    for layer in np.unique(layer_col):
        lmask = layer_col == layer
        if not lmask.any():
            continue
        rids = data["record_id"][base][lmask]
        tokens = data["token_idx"][base][lmask]
        slots = data["slot"][base][lmask]
        experts = data["expert"][base][lmask]
        weights = data["weight"][base][lmask]
        # Unique visit row per (record_id, token).
        pair = np.stack([rids, tokens], axis=1)
        _, row_of = np.unique(pair, axis=0, return_inverse=True)
        n_rows = int(row_of.max()) + 1
        ids = np.full((n_rows, top_k), 0, dtype=np.int64)
        gates = np.zeros((n_rows, top_k), dtype=np.float64)
        ids[row_of, slots] = experts
        gates[row_of, slots] = weights
        # Per-visit traj/call/position (constant within a (record, token) row).
        v_traj = np.empty(n_rows, dtype=np.int64)
        v_call = np.empty(n_rows, dtype=np.int64)
        v_pos = np.empty(n_rows, dtype=np.int64)
        v_traj[row_of] = traj_of_row[lmask]
        v_call[row_of] = call_col[lmask]
        v_pos[row_of] = tokens
        layer_visits[int(layer)] = {
            "traj_idx": v_traj, "call_idx": v_call, "position": v_pos,
            "expert_ids": ids, "gate_probs": gates,
        }

    return build_dataset(layer_visits, call_buckets, num_experts, num_buckets,
                         top_k=top_k, mode=mode)


def load_router_prob_mass(
    path: str | Path,
    tower: str = "decoder",
) -> dict[tuple[int, int], np.ndarray]:
    """Aggregate summed router probability mass per (layer, t_bucket).

    Available only if the run captured router probabilities
    (``ProbeConfig.capture_logits=True``). Used by the switch-transformer
    aux-loss metric for reproducible offline computation (MINOR 7).

    Args:
        path: Path to a ``*_routing.npz``.
        tower: Which tower (``"decoder"`` or ``"encoder"``).

    Returns:
        Mapping ``(layer_idx, t_bucket) -> summed_prob_mass[num_experts]``.
        Empty if no probabilities were captured.
    """
    data = np.load(Path(path))
    if "prob_mass" not in data:
        return {}
    tower_code = TOWER_DECODER if tower == "decoder" else TOWER_ENCODER
    keys = data["prob_keys"]  # (n, 4): record_id, layer, tower, t_bucket
    mass = data["prob_mass"]  # (n, E)
    result: dict[tuple[int, int], np.ndarray] = {}
    for i in range(keys.shape[0]):
        _rid, layer, twr, tb = (int(x) for x in keys[i])
        if twr != tower_code:
            continue
        key = (layer, tb)
        if key in result:
            result[key] = result[key] + mass[i]
        else:
            result[key] = mass[i].copy()
    return result
