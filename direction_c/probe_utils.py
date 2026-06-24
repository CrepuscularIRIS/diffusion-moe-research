"""Small helpers for the routing probe (kept separate to bound probe.py size).

These are pure utilities: parsing a router module's qualified name into
``(tower, layer_idx)`` and detaching a captured tensor to a CPU numpy array.
``_to_numpy`` is the only torch touch-point here; it is imported lazily by the
caller, so this module itself stays import-light.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def parse_router_location(qualified_name: str) -> tuple[str, int]:
    """Parse a router module path into ``(tower, layer_idx)``.

    Examples:
        ``model.decoder.layers.7.router`` -> ``("decoder", 7)``
        ``model.encoder.language_model.layers.3.router`` -> ``("encoder", 3)``

    Args:
        qualified_name: Dotted module path from ``named_modules``.

    Returns:
        Tuple of tower name and layer index (``-1`` if it cannot be parsed).
    """
    tower = "encoder" if ".encoder." in f".{qualified_name}." else "decoder"
    parts = qualified_name.split(".")
    layer_idx = -1
    for i, part in enumerate(parts):
        if part == "layers" and i + 1 < len(parts) and parts[i + 1].isdigit():
            layer_idx = int(parts[i + 1])
            break
    return tower, layer_idx


def to_numpy(tensor: Any) -> np.ndarray:
    """Detach a (possibly CUDA/bf16) tensor to a CPU float/int numpy array.

    Args:
        tensor: A torch tensor or array-like.

    Returns:
        A CPU numpy array (float tensors cast to fp32).
    """
    import torch  # local import keeps this module torch-free until called

    if isinstance(tensor, torch.Tensor):
        dtype = torch.float32 if tensor.is_floating_point() else None
        return tensor.detach().to("cpu", dtype).numpy()
    return np.asarray(tensor)
