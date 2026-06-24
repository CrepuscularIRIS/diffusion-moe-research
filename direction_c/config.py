"""Configuration and record dataclasses for the routing probe.

Split out of ``probe.py`` to keep that module focused on the hook mechanism.
``ProbeConfig`` is the frozen run configuration; ``RouterRecord`` is one
captured router invocation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class ProbeConfig:
    """Immutable configuration for a routing probe run.

    Attributes:
        num_experts: Total experts per MoE layer (DiffusionGemma: 128).
        top_k: Experts selected per token (DiffusionGemma: 8).
        num_timesteps: Number of denoising steps the loop will run
            (``max_denoising_steps``); used to map a forward-pass counter to a
            timestep ``t``. The loop counts ``t`` down from ``num_timesteps`` to 1.
        num_timestep_buckets: Number of buckets to group raw ``t`` into. Equal-
            width buckets over ``[1, num_timesteps]``. Use ``num_timesteps`` for
            no bucketing.
        capture_encoder: If ``True`` also hook encoder routers. Encoder routers
            fire once per canvas (prefill/AR step), not per denoising step, so
            their ``t`` tag is the canvas index, not a denoising timestep.
        capture_logits: If ``True`` store the full per-token router probability
            row (E floats). Memory-heavy; off by default.
        output_dir: Directory for persisted records. Created on demand.
        seed: RNG seed recorded for reproducibility.
    """

    num_experts: int = 128
    top_k: int = 8
    num_timesteps: int = 64
    num_timestep_buckets: int = 8
    capture_encoder: bool = False
    capture_logits: bool = False
    output_dir: Path = field(default=Path("direction_c/outputs"))
    seed: int = 42

    def bucket_of(self, timestep: int) -> int:
        """Map a raw denoising timestep ``t`` (1..num_timesteps) to a bucket id.

        Args:
            timestep: Raw timestep in ``[1, num_timesteps]``.

        Returns:
            Bucket id in ``[0, num_timestep_buckets)``.
        """
        if self.num_timestep_buckets <= 1:
            return 0
        t = max(1, min(self.num_timesteps, timestep))
        # Map t in [1, num_timesteps] -> [0, num_timestep_buckets-1].
        frac = (t - 1) / max(1, self.num_timesteps - 1)
        bucket = int(frac * self.num_timestep_buckets)
        return min(bucket, self.num_timestep_buckets - 1)


@dataclass
class RouterRecord:
    """One captured router invocation (one MoE layer at one denoising call).

    The H4 protocol (``plan/h4-test-protocol.md`` §5) requires the routing data
    to decompose into the exchangeability unit (trajectory = one prompt + one
    generated canvas), the denoising call index ``s`` within that trajectory,
    and the token position ``p``. The track key is ``(prompt_id, canvas_id,
    position)`` and the permutation unit is the trajectory. These fields carry
    exactly that metadata.

    Attributes:
        record_id: Globally unique id for this invocation. Combined with the
            per-record local token index it forms a collision-free token key.
        layer_idx: Index of the layer within its stack.
        tower: Either ``"decoder"`` or ``"encoder"``.
        timestep: Raw denoising timestep ``t`` (or canvas index for encoder).
        t_bucket: Pre-registered timestep bucket ``b(t)``.
        top_k_index: Array ``(num_tokens, top_k)`` of selected expert indices
            (PRE-capacity router top-k -- primary per protocol; see OPEN_RISKS).
        top_k_weights: Array ``(num_tokens, top_k)`` of normalized routing
            weights (gate probs over the selected experts).
        prompt_id: Prompt index (folded into the trajectory key).
        canvas_id: Autoregressive canvas index within the prompt.
        call_index: Denoising-call index ``s`` within the trajectory
            (resets per canvas).
        log_snr: Per-call noise level / log-SNR if exposed (else ``nan``).
        pre_capacity: ``True`` if ``top_k_index`` are pre-capacity router choices
            (primary). DiffusionGemma's router exposes pre-capacity top-k
            directly, so this is ``True`` for the real run.
        router_probabilities: Optional array ``(num_tokens, num_experts)`` of the
            full softmax router probabilities (only if ``capture_logits``).
    """

    record_id: int
    layer_idx: int
    tower: str
    timestep: int
    t_bucket: int
    top_k_index: np.ndarray
    top_k_weights: np.ndarray
    prompt_id: int = -1
    canvas_id: int = -1
    call_index: int = -1
    log_snr: float = float("nan")
    pre_capacity: bool = True
    router_probabilities: np.ndarray | None = None

    @property
    def trajectory_id(self) -> tuple[int, int]:
        """Exchangeability unit key = ``(prompt_id, canvas_id)``."""
        return (self.prompt_id, self.canvas_id)
