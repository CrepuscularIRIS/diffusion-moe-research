"""Unit tests for the block-diffusion / encoder-AR losses and softcap (model-independent)."""

import math

import pytest
import torch
import torch.nn.functional as F

from diffusiongemma_sft.loss import (
    block_diffusion_loss,
    encoder_ar_loss,
    softcap_logits,
)


# ---------------------------------------------------------------------------
# softcap_logits.
# ---------------------------------------------------------------------------


def test_softcap_matches_formula_and_fp32():
    cap = 30.0
    logits = (torch.randn(2, 5, 7) * 100).to(torch.bfloat16)
    out = softcap_logits(logits, cap)
    assert out.dtype == torch.float32
    expected = torch.tanh(logits.float() / cap) * cap
    assert torch.allclose(out, expected, atol=1e-5)
    # Bounded into [-cap, cap] (tanh saturates to exactly +/-1 in fp32 for large x).
    assert out.abs().max() <= cap


def test_softcap_none_only_upcasts():
    logits = torch.randn(3, 4).to(torch.bfloat16)
    out = softcap_logits(logits, None)
    assert out.dtype == torch.float32
    assert torch.allclose(out, logits.float(), atol=1e-5)


# ---------------------------------------------------------------------------
# block_diffusion_loss: flat masked CE, no 1/t, noise_mask irrelevant.
# ---------------------------------------------------------------------------


def test_block_diffusion_loss_matches_manual_flat_ce():
    torch.manual_seed(0)
    b, r, v = 2, 6, 50
    logits = torch.randn(b, r, v)
    targets = torch.randint(0, v, (b, r))
    canvas_loss = torch.zeros(b, r, dtype=torch.bool)
    canvas_loss[0, 1:4] = True
    canvas_loss[1, 0:2] = True

    loss = block_diffusion_loss(logits, targets, canvas_loss)

    nll = F.cross_entropy(logits.reshape(-1, v), targets.reshape(-1), reduction="none").reshape(b, r)
    n = int(canvas_loss.sum().item())
    expected = (nll * canvas_loss.float()).sum() / n
    assert torch.allclose(loss, expected, atol=1e-6)


def test_block_diffusion_loss_mask_excludes_unselected():
    """Positions not in canvas_loss must not affect the loss at all."""
    torch.manual_seed(1)
    b, r, v = 1, 8, 30
    logits = torch.randn(b, r, v)
    targets = torch.randint(0, v, (b, r))
    canvas_loss = torch.zeros(b, r, dtype=torch.bool)
    canvas_loss[0, 2:5] = True

    base = block_diffusion_loss(logits, targets, canvas_loss)
    # Perturb logits ONLY at an unselected position; loss must be unchanged.
    # (Boost a WRONG class so it would change CE if scored — softmax is
    # shift-invariant, so a uniform bump on all classes would be a no-op.)
    wrong0 = (targets[0, 7].item() + 1) % v
    logits2 = logits.clone()
    logits2[0, 7, wrong0] += 100.0
    assert torch.allclose(base, block_diffusion_loss(logits2, targets, canvas_loss), atol=1e-6)
    # Perturb a SELECTED position toward a wrong class; loss must change.
    wrong3 = (targets[0, 3].item() + 1) % v
    logits3 = logits.clone()
    logits3[0, 3, wrong3] += 100.0
    assert not torch.allclose(base, block_diffusion_loss(logits3, targets, canvas_loss), atol=1e-6)


def test_block_diffusion_loss_noise_mask_unused():
    """The loss has no noise_mask argument; support is the full canvas_loss
    (corrupted AND uncorrupted), matching BlockDiffusionCrossEntropyLoss."""
    torch.manual_seed(2)
    b, r, v = 1, 4, 20
    logits = torch.randn(b, r, v)
    targets = torch.randint(0, v, (b, r))
    canvas_loss = torch.ones(b, r, dtype=torch.bool)
    loss = block_diffusion_loss(logits, targets, canvas_loss)
    nll = F.cross_entropy(logits.reshape(-1, v), targets.reshape(-1), reduction="none")
    assert torch.allclose(loss, nll.mean(), atol=1e-6), "flat mean over all canvas tokens"


def test_block_diffusion_loss_global_denominator():
    """num_diffusion_tokens overrides the local denominator (global token norm)."""
    torch.manual_seed(3)
    b, r, v = 1, 5, 25
    logits = torch.randn(b, r, v)
    targets = torch.randint(0, v, (b, r))
    canvas_loss = torch.zeros(b, r, dtype=torch.bool)
    canvas_loss[0, :3] = True

    nll = F.cross_entropy(logits.reshape(-1, v), targets.reshape(-1), reduction="none").reshape(b, r)
    numer = (nll * canvas_loss.float()).sum()
    # Use a global denom of 10 (e.g. 3 local + 7 from other microbatches).
    loss = block_diffusion_loss(logits, targets, canvas_loss, num_diffusion_tokens=10)
    assert torch.allclose(loss, numer / 10, atol=1e-6)


def test_block_diffusion_loss_empty_mask_no_div_by_zero():
    logits = torch.randn(1, 3, 8)
    targets = torch.randint(0, 8, (1, 3))
    canvas_loss = torch.zeros(1, 3, dtype=torch.bool)
    loss = block_diffusion_loss(logits, targets, canvas_loss)
    assert loss.item() == 0.0


def test_block_diffusion_loss_shape_validation():
    logits = torch.randn(2, 4, 10)
    targets = torch.randint(0, 10, (2, 5))  # wrong R
    canvas_loss = torch.ones(2, 5, dtype=torch.bool)
    with pytest.raises(ValueError):
        block_diffusion_loss(logits, targets, canvas_loss)


# ---------------------------------------------------------------------------
# encoder_ar_loss: causal next-token CE with proper shift + mask.
# ---------------------------------------------------------------------------


def test_encoder_ar_loss_shift_alignment():
    """logits[:, :-1] predict clean_ids[:, 1:]."""
    torch.manual_seed(4)
    b, s, v = 2, 7, 40
    logits = torch.randn(b, s, v)
    clean = torch.randint(0, v, (b, s))
    attn = torch.ones(b, s, dtype=torch.bool)

    loss = encoder_ar_loss(logits, clean, attn)

    pred = logits[:, :-1, :]
    tgt = clean[:, 1:]
    expected = F.cross_entropy(pred.reshape(-1, v), tgt.reshape(-1))
    assert torch.allclose(loss, expected, atol=1e-6)


def test_encoder_ar_loss_pad_mask_support():
    """Scored positions = attention_mask[:, :-1] & attention_mask[:, 1:]."""
    torch.manual_seed(5)
    b, s, v = 1, 6, 30
    logits = torch.randn(b, s, v)
    clean = torch.randint(0, v, (b, s))
    attn = torch.tensor([[1, 1, 1, 1, 0, 0]], dtype=torch.bool)  # last 2 are pad

    loss = encoder_ar_loss(logits, clean, attn)

    nll = F.cross_entropy(
        logits[:, :-1].reshape(-1, v), clean[:, 1:].reshape(-1), reduction="none"
    ).reshape(b, s - 1)
    mask = (attn[:, :-1] & attn[:, 1:]).float()
    expected = (nll * mask).sum() / mask.sum()
    assert torch.allclose(loss, expected, atol=1e-6)
    # Only pairs (0,1),(1,2),(2,3) are valid -> 3 scored positions.
    assert int(mask.sum().item()) == 3


def test_encoder_ar_loss_perturb_pad_region_no_effect():
    torch.manual_seed(6)
    b, s, v = 1, 6, 20
    logits = torch.randn(b, s, v)
    clean = torch.randint(0, v, (b, s))
    attn = torch.tensor([[1, 1, 1, 0, 0, 0]], dtype=torch.bool)
    base = encoder_ar_loss(logits, clean, attn)
    # Perturb logits at a fully-masked predicting position (index 4 predicts pad 5).
    logits2 = logits.clone()
    logits2[0, 4] += 100.0
    assert torch.allclose(base, encoder_ar_loss(logits2, clean, attn), atol=1e-6)


def test_encoder_ar_loss_global_denominator():
    torch.manual_seed(7)
    b, s, v = 1, 5, 15
    logits = torch.randn(b, s, v)
    clean = torch.randint(0, v, (b, s))
    attn = torch.ones(b, s, dtype=torch.bool)
    nll = F.cross_entropy(logits[:, :-1].reshape(-1, v), clean[:, 1:].reshape(-1), reduction="none")
    loss = encoder_ar_loss(logits, clean, attn, num_ar_tokens=100)
    assert torch.allclose(loss, nll.sum() / 100, atol=1e-6)


def test_encoder_ar_loss_no_mask_counts_all():
    torch.manual_seed(8)
    b, s, v = 2, 4, 12
    logits = torch.randn(b, s, v)
    clean = torch.randint(0, v, (b, s))
    loss = encoder_ar_loss(logits, clean, attention_mask=None)
    expected = F.cross_entropy(logits[:, :-1].reshape(-1, v), clean[:, 1:].reshape(-1))
    assert torch.allclose(loss, expected, atol=1e-6)


def test_encoder_ar_loss_shape_validation():
    logits = torch.randn(2, 6, 10)
    clean = torch.randint(0, 10, (2, 5))  # mismatched S
    with pytest.raises(ValueError):
        encoder_ar_loss(logits, clean)


# ---------------------------------------------------------------------------
# Integration: total = diffusion + 1.0 * AR (blueprint sec 4b).
# ---------------------------------------------------------------------------


def test_total_loss_is_sum():
    torch.manual_seed(9)
    b, r, s, v = 1, 4, 6, 20
    canvas_logits = torch.randn(b, r, v)
    canvas_targets = torch.randint(0, v, (b, r))
    canvas_loss = torch.ones(b, r, dtype=torch.bool)
    enc_logits = torch.randn(b, s, v)
    clean = torch.randint(0, v, (b, s))
    attn = torch.ones(b, s, dtype=torch.bool)

    diff = block_diffusion_loss(canvas_logits, canvas_targets, canvas_loss)
    ar = encoder_ar_loss(enc_logits, clean, attn)
    total = diff + 1.0 * ar
    assert math.isfinite(total.item())
    assert torch.allclose(total, diff + ar, atol=1e-7)
