"""Unit tests for D3PM-uniform corruption (model-independent, runnable now)."""

import torch

from diffusiongemma_sft.data.corruption import (
    CorruptionConfig,
    corrupt_uniform_random,
    corruption_generator,
)


def test_prompt_tokens_never_corrupted():
    """Positions with loss_mask=0 (prompt) must stay identical to clean."""
    ids = torch.arange(2 * 20).reshape(2, 20) % 100
    loss_mask = torch.zeros(2, 20)
    loss_mask[:, 10:] = 1  # only second half supervised
    noisy, _ = corrupt_uniform_random(ids, loss_mask, CorruptionConfig(vocab_size=100))
    assert torch.equal(noisy[:, :10], ids[:, :10]), "prompt region must be untouched"


def test_noise_mask_subset_of_loss_mask():
    """Every corrupted position must be a supervised position."""
    ids = torch.randint(0, 100, (4, 50))
    loss_mask = (torch.rand(4, 50) > 0.5).float()
    noisy, noise_mask = corrupt_uniform_random(ids, loss_mask, CorruptionConfig(vocab_size=100))
    assert (noise_mask & ~loss_mask.bool()).sum() == 0, "corruption leaked into prompt"
    # Where noise_mask is False, noisy must equal clean.
    assert torch.equal(noisy[~noise_mask], ids[~noise_mask])


def test_replacement_in_vocab_range():
    """Replacement tokens must be valid vocab ids."""
    ids = torch.randint(0, 256, (3, 30))
    loss_mask = torch.ones(3, 30)
    noisy, _ = corrupt_uniform_random(ids, loss_mask, CorruptionConfig(vocab_size=256))
    assert noisy.min() >= 0 and noisy.max() < 256


def test_reproducible_with_generator():
    """Same seed -> identical corruption."""
    ids = torch.randint(0, 1000, (2, 40))
    loss_mask = torch.ones(2, 40)
    cfg = CorruptionConfig(vocab_size=1000)
    g1 = corruption_generator(42, step=3, microbatch_idx=0, rank=0)
    g2 = corruption_generator(42, step=3, microbatch_idx=0, rank=0)
    n1, m1 = corrupt_uniform_random(ids, loss_mask, cfg, generator=g1)
    n2, m2 = corrupt_uniform_random(ids, loss_mask, cfg, generator=g2)
    assert torch.equal(n1, n2) and torch.equal(m1, m2)


def test_different_step_differs():
    """Different step -> different corruption stream."""
    ids = torch.randint(0, 1000, (2, 40))
    loss_mask = torch.ones(2, 40)
    cfg = CorruptionConfig(vocab_size=1000)
    g1 = corruption_generator(42, step=3, microbatch_idx=0, rank=0)
    g2 = corruption_generator(42, step=4, microbatch_idx=0, rank=0)
    n1, _ = corrupt_uniform_random(ids, loss_mask, cfg, generator=g1)
    n2, _ = corrupt_uniform_random(ids, loss_mask, cfg, generator=g2)
    assert not torch.equal(n1, n2)


def test_corruption_rate_roughly_matches_t():
    """Over many supervised tokens, corruption fraction should be plausible (0<frac<1)."""
    ids = torch.randint(0, 10000, (64, 256))
    loss_mask = torch.ones(64, 256)
    cfg = CorruptionConfig(vocab_size=10000, eps=1e-3)
    g = corruption_generator(7, step=0, microbatch_idx=0, rank=0)
    _, noise_mask = corrupt_uniform_random(ids, loss_mask, cfg, generator=g)
    frac = noise_mask.float().mean().item()
    # t ~ U(0,1) averaged over sequences -> expected ~0.5, but allow wide band.
    assert 0.1 < frac < 0.9, f"corruption fraction {frac} implausible"
