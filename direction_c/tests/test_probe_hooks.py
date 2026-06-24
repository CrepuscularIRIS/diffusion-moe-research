"""Unit tests for the RoutingProbe hook mechanism using a tiny FAKE MoE model.

No DiffusionGemma model is loaded. We build a minimal torch module that mimics
the *interface* of the real model: router modules whose class is named
``DiffusionGemmaTextRouter`` and that return the real 3-tuple
``(router_probabilities, top_k_weights, top_k_index)``, plus a decoder-model
wrapper named ``DiffusionGemmaDecoderModel`` so the probe's timestep tracking
fires. This verifies the probe captures correct indices/weights/shapes and tags
records by denoising timestep, entirely without the 26B model.
"""

from __future__ import annotations

import numpy as np
import pytest
import torch
from torch import nn

from direction_c.metrics import load_balance_aux_fraction
from direction_c.persistence import (
    load_router_prob_mass,
    load_token_selections,
    load_usage_counts,
)
from direction_c.probe import (
    ProbeConfig,
    RoutingProbe,
    _parse_router_location,
)

NUM_EXPERTS = 16
TOP_K = 4
HIDDEN = 8


class DiffusionGemmaTextRouter(nn.Module):
    """Fake router matching the real class name and return signature.

    Mirrors transformers' ``DiffusionGemmaTextRouter.forward``: returns
    ``(router_probabilities[B*S, E], top_k_weights[B*S, K], top_k_index[B*S, K])``.
    """

    def __init__(self, hidden: int, num_experts: int, top_k: int) -> None:
        super().__init__()
        self.proj = nn.Linear(hidden, num_experts, bias=False)
        self.top_k = top_k

    def forward(self, hidden_states: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        scores = self.proj(hidden_states)
        probs = torch.softmax(scores, dim=-1, dtype=torch.float32)
        top_k_weights, top_k_index = torch.topk(probs, k=self.top_k, dim=-1)
        top_k_weights = top_k_weights / top_k_weights.sum(dim=-1, keepdim=True)
        return probs, top_k_weights, top_k_index


class _FakeLayer(nn.Module):
    """A layer holding a router (mirrors DiffusionGemma*TextLayer.router)."""

    def __init__(self) -> None:
        super().__init__()
        self.router = DiffusionGemmaTextRouter(HIDDEN, NUM_EXPERTS, TOP_K)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        flat = x.reshape(-1, x.shape[-1])
        self.router(flat)  # routing happens here, like the real layer
        return x


class DiffusionGemmaDecoderModel(nn.Module):
    """Fake decoder model: stack of layers; one forward == one denoising step."""

    def __init__(self, num_layers: int) -> None:
        super().__init__()
        self.layers = nn.ModuleList([_FakeLayer() for _ in range(num_layers)])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x)
        return x


class DiffusionGemmaEncoderModel(nn.Module):
    """Fake encoder model: one forward == one canvas boundary (no routers)."""

    def __init__(self) -> None:
        super().__init__()
        self.dummy = nn.Linear(HIDDEN, HIDDEN)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dummy(x)


class _FakeModel(nn.Module):
    """Top-level wrapper exposing ``model.encoder`` and ``model.decoder``.

    ``simulate_generation`` mimics the real ``generate`` structure: one encoder
    forward per canvas (the canvas boundary), then ``num_steps`` decoder
    forwards (the denoising loop). This lets tests exercise the per-canvas /
    per-prompt counter reset (FATAL 2) without the 26B model.
    """

    def __init__(self, num_layers: int, with_encoder: bool = False) -> None:
        super().__init__()
        if with_encoder:
            self.encoder = DiffusionGemmaEncoderModel()
        self.decoder = DiffusionGemmaDecoderModel(num_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.decoder(x)

    def simulate_generation(
        self,
        num_canvases: int,
        num_steps: int,
        *,
        batch: int = 2,
        seq: int = 5,
    ) -> None:
        """Run encoder-then-denoising-loop with stationary (null) routing.

        Args:
            num_canvases: Autoregressive canvases to simulate.
            num_steps: Denoising steps (decoder forwards) per canvas.
            batch, seq: Token grid per forward.
        """
        for _canvas in range(num_canvases):
            self.encoder(_make_inputs(batch, seq))  # canvas boundary
            for _step in range(num_steps):
                self.decoder(_make_inputs(batch, seq))


def _make_inputs(batch: int = 2, seq: int = 5) -> torch.Tensor:
    torch.manual_seed(0)
    return torch.randn(batch, seq, HIDDEN)


@pytest.mark.unit
def test_parse_router_location_decoder() -> None:
    assert _parse_router_location("model.decoder.layers.7.router") == ("decoder", 7)


@pytest.mark.unit
def test_parse_router_location_encoder() -> None:
    assert _parse_router_location(
        "model.encoder.language_model.layers.3.router"
    ) == ("encoder", 3)


@pytest.mark.unit
def test_attach_finds_all_routers() -> None:
    num_layers = 4
    model = _FakeModel(num_layers)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=3, num_timestep_buckets=3)
    probe = RoutingProbe(model, cfg)
    n = probe.attach()
    try:
        assert n == num_layers
    finally:
        probe.detach()


@pytest.mark.unit
def test_attach_raises_without_routers() -> None:
    cfg = ProbeConfig()
    probe = RoutingProbe(nn.Linear(4, 4), cfg)
    with pytest.raises(RuntimeError):
        probe.attach()


@pytest.mark.unit
def test_hook_captures_correct_shapes() -> None:
    num_layers = 3
    batch, seq = 2, 5
    model = _FakeModel(num_layers)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=1, num_timestep_buckets=1)
    probe = RoutingProbe(model, cfg)
    probe.attach()
    try:
        with torch.no_grad():
            model(_make_inputs(batch, seq))
    finally:
        probe.detach()

    # One decoder forward == one denoising step -> one record per layer.
    assert len(probe.records) == num_layers
    n_tokens = batch * seq
    for rec in probe.records:
        assert rec.tower == "decoder"
        assert rec.top_k_index.shape == (n_tokens, TOP_K)
        assert rec.top_k_weights.shape == (n_tokens, TOP_K)
        assert rec.top_k_index.dtype == np.int32
        # Indices must be valid experts.
        assert rec.top_k_index.min() >= 0
        assert rec.top_k_index.max() < NUM_EXPERTS
        # Weights normalized per token.
        assert np.allclose(rec.top_k_weights.sum(axis=1), 1.0, atol=1e-5)


@pytest.mark.unit
def test_hook_indices_match_manual_topk() -> None:
    # Confirm the hook records EXACTLY the indices the router computes.
    model = _FakeModel(num_layers=1)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=1, num_timestep_buckets=1)
    probe = RoutingProbe(model, cfg)
    probe.attach()
    x = _make_inputs(batch=1, seq=3)
    try:
        with torch.no_grad():
            model(x)
            # Recompute the router output independently.
            flat = x.reshape(-1, HIDDEN)
            _, _, expected_idx = model.decoder.layers[0].router(flat)
    finally:
        probe.detach()

    captured = probe.records[0].top_k_index
    assert np.array_equal(captured, expected_idx.cpu().numpy().astype(np.int32))


@pytest.mark.unit
def test_timestep_tagging_counts_down() -> None:
    # Three decoder forwards == three denoising steps; t must count down N..1.
    num_layers = 2
    num_steps = 3
    model = _FakeModel(num_layers)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS,
        top_k=TOP_K,
        num_timesteps=num_steps,
        num_timestep_buckets=num_steps,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach()
    try:
        with torch.no_grad():
            for _ in range(num_steps):
                model(_make_inputs())
    finally:
        probe.detach()

    # Group recorded timesteps by decoder forward order.
    by_layer0 = [r.timestep for r in probe.records if r.layer_idx == 0]
    assert by_layer0 == [num_steps, num_steps - 1, num_steps - 2]  # i.e. 3,2,1
    # Bucket ids should also differ across the three steps.
    buckets0 = sorted({r.t_bucket for r in probe.records if r.layer_idx == 0})
    assert len(buckets0) == num_steps


@pytest.mark.unit
def test_capture_logits_stores_full_probabilities() -> None:
    model = _FakeModel(num_layers=1)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS,
        top_k=TOP_K,
        num_timesteps=1,
        num_timestep_buckets=1,
        capture_logits=True,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach()
    x = _make_inputs(batch=1, seq=4)
    try:
        with torch.no_grad():
            model(x)
    finally:
        probe.detach()
    rec = probe.records[0]
    assert rec.router_probabilities is not None
    assert rec.router_probabilities.shape == (4, NUM_EXPERTS)
    assert np.allclose(rec.router_probabilities.sum(axis=1), 1.0, atol=1e-5)


@pytest.mark.unit
def test_save_roundtrip(tmp_path) -> None:
    num_layers = 2
    batch, seq = 1, 3
    model = _FakeModel(num_layers)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS,
        top_k=TOP_K,
        num_timesteps=1,
        num_timestep_buckets=1,
        output_dir=tmp_path,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach()
    try:
        with torch.no_grad():
            model(_make_inputs(batch, seq))
    finally:
        probe.detach()

    path = probe.save("unit")
    assert path.exists()
    data = np.load(path)
    n_rows = num_layers * (batch * seq) * TOP_K
    assert data["expert"].shape[0] == n_rows
    assert set(np.unique(data["layer_idx"]).tolist()) == set(range(num_layers))
    assert data["num_experts"][0] == NUM_EXPERTS
    assert data["top_k"][0] == TOP_K
    # record_id column present and one unique id per router invocation.
    assert "record_id" in data
    assert np.unique(data["record_id"]).size == num_layers
    # Every recorded expert index must be in range.
    assert data["expert"].min() >= 0 and data["expert"].max() < NUM_EXPERTS


@pytest.mark.unit
def test_multi_record_per_cell_roundtrip_no_overwrite(tmp_path) -> None:
    # MAJOR 5 + FATAL 1: >=3 prompts land in the SAME (layer, bucket) cell.
    # The OLD code keyed tokens by local token_idx only, so records overwrote
    # each other -> counts and reconstructed selections would be missing rows.
    # This test runs the ACTUAL save->load cycle and asserts every selection is
    # preserved. It FAILS on the old persistence and PASSES after the fix.
    num_layers = 2
    batch, seq = 2, 4
    n_prompts = 4  # >= 3, all into bucket 0 (single timestep bucket)
    n_tokens = batch * seq

    model = _FakeModel(num_layers, with_encoder=True)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS,
        top_k=TOP_K,
        num_timesteps=1,
        num_timestep_buckets=1,
        output_dir=tmp_path,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach(expected_decoder_layers=num_layers)
    # Ground-truth count of selections per (layer) summed over prompts.
    expected_total = n_prompts * n_tokens * TOP_K
    try:
        with torch.no_grad():
            for _ in range(n_prompts):
                probe.start_prompt()
                model.simulate_generation(num_canvases=1, num_steps=1, batch=batch, seq=seq)
    finally:
        probe.detach()
    path = probe.save("multi")

    counts = load_usage_counts(path, tower="decoder")
    assert set(counts.keys()) == {(0, 0), (1, 0)}
    for vec in counts.values():
        # ALL prompts' selections must be counted (no silent overwrite).
        assert int(vec.sum()) == expected_total

    # Reconstructed per-token selections must contain every prompt's tokens.
    sel = load_token_selections(path, layer_idx=0, t_bucket=0, tower="decoder")
    assert sel.shape == (n_prompts * n_tokens, TOP_K)
    assert sel.min() >= 0 and sel.max() < NUM_EXPERTS
    # Bincount of reconstructed selections must match the aggregated counts.
    recon_counts = np.bincount(sel.reshape(-1), minlength=NUM_EXPERTS)
    assert np.array_equal(recon_counts, counts[(0, 0)])


@pytest.mark.unit
def test_save_records_empty_is_safe(tmp_path) -> None:
    from direction_c.persistence import save_records

    cfg = ProbeConfig(output_dir=tmp_path)
    path = save_records([], cfg, "empty")
    data = np.load(path)
    assert data["expert"].shape[0] == 0


@pytest.mark.unit
def test_router_prob_mass_persisted_and_aux_loss_reproducible(tmp_path) -> None:
    # MINOR 7: with capture_logits, summed router prob mass is persisted so the
    # switch-transformer aux-loss metric can be recomputed offline.
    num_layers = 1
    batch, seq = 2, 4
    model = _FakeModel(num_layers, with_encoder=True)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS,
        top_k=TOP_K,
        num_timesteps=1,
        num_timestep_buckets=1,
        capture_logits=True,
        output_dir=tmp_path,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach(expected_decoder_layers=num_layers)
    try:
        with torch.no_grad():
            for _ in range(3):
                probe.start_prompt()
                model.simulate_generation(num_canvases=1, num_steps=1, batch=batch, seq=seq)
    finally:
        probe.detach()
    path = probe.save("aux")

    mass = load_router_prob_mass(path, tower="decoder")
    counts = load_usage_counts(path, tower="decoder")
    assert (0, 0) in mass and mass[(0, 0)].shape == (NUM_EXPERTS,)
    # The aux fraction is finite and >= 1.0 (optimum), computable purely offline.
    aux = load_balance_aux_fraction(counts[(0, 0)], mass[(0, 0)])
    assert aux >= 1.0 - 1e-6 and np.isfinite(aux)


@pytest.mark.unit
def test_router_prob_mass_absent_without_capture(tmp_path) -> None:
    model = _FakeModel(num_layers=1, with_encoder=True)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=1,
        num_timestep_buckets=1, output_dir=tmp_path,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach(expected_decoder_layers=1)
    try:
        with torch.no_grad():
            model.simulate_generation(num_canvases=1, num_steps=1)
    finally:
        probe.detach()
    path = probe.save("noaux")
    assert load_router_prob_mass(path) == {}


@pytest.mark.unit
def test_reset_clears_records() -> None:
    model = _FakeModel(num_layers=1)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=1, num_timestep_buckets=1)
    probe = RoutingProbe(model, cfg)
    probe.attach()
    try:
        with torch.no_grad():
            model(_make_inputs())
        assert len(probe.records) > 0
        probe.reset()
        assert len(probe.records) == 0
    finally:
        probe.detach()


@pytest.mark.unit
def test_decoder_pass_resets_per_canvas_no_timestep_contamination() -> None:
    # FATAL 2: across multiple canvases, the encoder pre-hook must reset the
    # decoder pass counter so each canvas's step k maps to the SAME timestep t.
    # On the OLD code (_decoder_pass never reset) the modulo would drift and a
    # canvas-2 early step would be tagged with a late-canvas-1 timestep.
    num_layers = 1
    num_steps = 4
    num_canvases = 3
    model = _FakeModel(num_layers, with_encoder=True)
    cfg = ProbeConfig(
        num_experts=NUM_EXPERTS,
        top_k=TOP_K,
        num_timesteps=num_steps,
        num_timestep_buckets=num_steps,
    )
    probe = RoutingProbe(model, cfg)
    probe.attach(expected_decoder_layers=num_layers)
    try:
        with torch.no_grad():
            probe.start_prompt()
            model.simulate_generation(num_canvases=num_canvases, num_steps=num_steps)
    finally:
        probe.detach()

    decoder_recs = [r for r in probe.records if r.tower == "decoder"]
    # The recorded timesteps must be exactly [N..1] repeated per canvas, NOT a
    # monotonically drifting modulo sequence.
    timesteps = [r.timestep for r in decoder_recs]
    expected = list(range(num_steps, 0, -1)) * num_canvases
    assert timesteps == expected
    # Each timestep t must appear exactly once per canvas (no contamination).
    for t in range(1, num_steps + 1):
        assert timesteps.count(t) == num_canvases


@pytest.mark.unit
def test_attach_asserts_full_decoder_coverage() -> None:
    # MAJOR 6: if the expected layer set is not fully hooked, attach must fail.
    model = _FakeModel(num_layers=3)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=1, num_timestep_buckets=1)
    probe = RoutingProbe(model, cfg)
    # Demand 5 layers but only 3 exist -> must raise, not silently undercount.
    with pytest.raises(RuntimeError, match="coverage mismatch"):
        probe.attach(expected_decoder_layers=5)
    probe.detach()


@pytest.mark.unit
def test_attach_full_coverage_passes() -> None:
    model = _FakeModel(num_layers=3)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=1, num_timestep_buckets=1)
    probe = RoutingProbe(model, cfg)
    n = probe.attach(expected_decoder_layers=3)
    try:
        assert n == 3
    finally:
        probe.detach()


@pytest.mark.unit
def test_external_timestep_overrides_fallback() -> None:
    # FATAL 2 preferred path: a stamped cur_step is used verbatim.
    model = _FakeModel(num_layers=1, with_encoder=True)
    cfg = ProbeConfig(num_experts=NUM_EXPERTS, top_k=TOP_K, num_timesteps=10, num_timestep_buckets=10)
    probe = RoutingProbe(model, cfg)
    probe.attach(expected_decoder_layers=1)
    try:
        with torch.no_grad():
            probe.start_prompt()
            for true_t in (7, 3, 9):  # arbitrary, not the fallback order
                probe.set_external_timestep(true_t)
                model.decoder(_make_inputs())
    finally:
        probe.detach()
    decoder_recs = [r for r in probe.records if r.tower == "decoder"]
    assert [r.timestep for r in decoder_recs] == [7, 3, 9]
