"""Direction C analysis toolchain for the Diffusion MoE project.

This package provides model-independent instrumentation and a calibrated
statistical test for hypothesis H4: *DiffusionGemma's MoE experts specialize by
denoising timestep t.*

Modules
-------
- ``config``       : ``ProbeConfig`` (frozen run config) and ``RouterRecord``.
- ``probe``        : forward-hook instrumentation (needs torch; lazy-imported).
- ``persistence``  : columnar ``.npz`` save/load (torch-free).
- ``runner``       : ``run_probe`` orchestration around ``model.generate``
  (needs torch; lazy-imported).
- ``metrics``      : pure descriptive functions over expert-usage distributions.
- ``h4_data``      : track-structured ``H4Dataset`` for the test.
- ``h4_test``      : the H4 protocol test -- track-stratified conditional-MI/G
  statistic, trajectory-synchronous permutation, shared-draw maxT FWER, effect
  sizes. See ``plan/h4-test-protocol.md``.
- ``h4_validation``: null generators (A/B/C) + planted-effect power generator +
  Clopper-Pearson upper bound for type-I / power validation.

IMPORTANT (torch-free import): the analysis layer (``metrics``, ``persistence``,
``h4_data``, ``h4_test``, ``h4_validation``, ``config``) imports with NO torch
dependency. The torch-dependent names (``RoutingProbe``, ``run_probe``) are
lazy-loaded via module ``__getattr__`` so the test/metrics code runs in a
torch-free environment.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from direction_c.config import ProbeConfig, RouterRecord
from direction_c.h4_data import (
    H4Dataset,
    VisitArray,
    build_dataset,
    expert_mass_from_topk,
)
from direction_c.h4_test import (
    H4Result,
    LayerH4Result,
    cluster_bootstrap_nmi,
    run_h4_test,
)
from direction_c.h4_validation import (
    SyntheticDesign,
    clopper_pearson_upper,
    make_null_b,
    make_null_c,
    make_null_xcorr,
    make_planted,
    null_a_real_orbit,
    permutation_orbit_relabel,
)
from direction_c.metrics import (
    BootstrapNoiseFloor,
    bootstrap_js_noise_floor,
    coefficient_of_variation,
    expert_usage_distribution,
    jensen_shannon_divergence,
    load_balance_aux_fraction,
    max_expert_share,
    pairwise_js_across_buckets,
    shannon_entropy,
    specialization_index,
)
from direction_c.persistence import (
    load_h4_dataset,
    load_router_prob_mass,
    load_token_selections,
    load_usage_counts,
    save_records,
)

if TYPE_CHECKING:  # for type checkers only; runtime uses __getattr__
    from direction_c.probe import RoutingProbe  # noqa: F401
    from direction_c.runner import run_probe  # noqa: F401

# Names that pull in torch; loaded lazily so the analysis layer stays torch-free.
_LAZY_TORCH = {"RoutingProbe": "probe", "run_probe": "runner"}


def __getattr__(name: str) -> Any:
    """Lazily import torch-dependent names on first access (PEP 562)."""
    if name in _LAZY_TORCH:
        import importlib

        module = importlib.import_module(f"direction_c.{_LAZY_TORCH[name]}")
        return getattr(module, name)
    raise AttributeError(f"module 'direction_c' has no attribute '{name}'")


__all__ = [
    # config + probe (probe is lazy)
    "ProbeConfig",
    "RouterRecord",
    "RoutingProbe",
    "run_probe",
    # persistence
    "save_records",
    "load_usage_counts",
    "load_token_selections",
    "load_router_prob_mass",
    "load_h4_dataset",
    # metrics (descriptive)
    "BootstrapNoiseFloor",
    "bootstrap_js_noise_floor",
    "coefficient_of_variation",
    "expert_usage_distribution",
    "jensen_shannon_divergence",
    "load_balance_aux_fraction",
    "max_expert_share",
    "pairwise_js_across_buckets",
    "shannon_entropy",
    "specialization_index",
    # h4 data + test + validation
    "H4Dataset",
    "VisitArray",
    "build_dataset",
    "expert_mass_from_topk",
    "H4Result",
    "LayerH4Result",
    "run_h4_test",
    "cluster_bootstrap_nmi",
    "SyntheticDesign",
    "make_null_b",
    "make_null_c",
    "make_null_xcorr",
    "make_planted",
    "permutation_orbit_relabel",
    "null_a_real_orbit",
    "clopper_pearson_upper",
]
