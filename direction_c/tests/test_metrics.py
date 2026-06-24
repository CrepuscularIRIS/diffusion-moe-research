"""Unit tests for direction_c.metrics using synthetic distributions only.

No DiffusionGemma model is required. Each test pins a known property of a
metric so that a regression in the analysis backbone is caught before the real
probe run.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from direction_c.metrics import (
    bootstrap_js_noise_floor,
    coefficient_of_variation,
    expert_usage_distribution,
    jensen_shannon_divergence,
    load_balance_aux_fraction,
    max_expert_share,
    normalized_entropy,
    pairwise_js_across_buckets,
    shannon_entropy,
    specialization_index,
)

E = 8  # synthetic number of experts


@pytest.mark.unit
def test_usage_distribution_normalizes() -> None:
    counts = np.array([1.0, 1.0, 2.0, 4.0])
    dist = expert_usage_distribution(counts)
    assert math.isclose(dist.sum(), 1.0, abs_tol=1e-9)
    assert math.isclose(dist[3], 0.5, abs_tol=1e-9)


@pytest.mark.unit
def test_usage_distribution_zero_total_is_uniform() -> None:
    dist = expert_usage_distribution(np.zeros(E))
    assert np.allclose(dist, 1.0 / E)


@pytest.mark.unit
def test_usage_distribution_rejects_negative() -> None:
    with pytest.raises(ValueError):
        expert_usage_distribution(np.array([-1.0, 2.0]))


@pytest.mark.unit
def test_uniform_has_max_entropy() -> None:
    uniform = np.full(E, 1.0 / E)
    assert math.isclose(shannon_entropy(uniform), math.log2(E), abs_tol=1e-9)
    assert math.isclose(normalized_entropy(uniform), 1.0, abs_tol=1e-9)


@pytest.mark.unit
def test_one_hot_has_zero_entropy_and_full_specialization() -> None:
    one_hot = np.zeros(E)
    one_hot[2] = 1.0
    assert math.isclose(shannon_entropy(one_hot), 0.0, abs_tol=1e-9)
    assert math.isclose(normalized_entropy(one_hot), 0.0, abs_tol=1e-9)
    assert math.isclose(specialization_index(one_hot), 1.0, abs_tol=1e-9)


@pytest.mark.unit
def test_specialization_uniform_is_zero() -> None:
    uniform = np.full(E, 1.0 / E)
    assert math.isclose(specialization_index(uniform), 0.0, abs_tol=1e-9)


@pytest.mark.unit
def test_max_expert_share_bounds() -> None:
    uniform = np.full(E, 1.0 / E)
    one_hot = np.zeros(E)
    one_hot[0] = 1.0
    assert math.isclose(max_expert_share(uniform), 1.0 / E, abs_tol=1e-9)
    assert math.isclose(max_expert_share(one_hot), 1.0, abs_tol=1e-9)


@pytest.mark.unit
def test_entropy_single_expert_normalized_is_zero() -> None:
    # Degenerate edge case: one expert -> no spread possible.
    assert math.isclose(normalized_entropy(np.array([5.0])), 0.0, abs_tol=1e-9)


@pytest.mark.unit
def test_cv_balanced_is_zero() -> None:
    balanced = np.full(E, 10.0)
    assert math.isclose(coefficient_of_variation(balanced), 0.0, abs_tol=1e-9)


@pytest.mark.unit
def test_cv_concentrated_is_large() -> None:
    concentrated = np.zeros(E)
    concentrated[0] = 100.0
    # All load on one of E experts: CV = sqrt(E-1).
    assert math.isclose(coefficient_of_variation(concentrated), math.sqrt(E - 1), abs_tol=1e-6)


@pytest.mark.unit
def test_cv_zero_mean_is_zero() -> None:
    assert math.isclose(coefficient_of_variation(np.zeros(E)), 0.0, abs_tol=1e-12)


@pytest.mark.unit
def test_aux_fraction_uniform_is_one() -> None:
    # Uniform dispatch and uniform router mass -> aux fraction == 1.0 (optimum).
    uniform_counts = np.full(E, 4.0)
    uniform_mass = np.full(E, 1.0 / E)
    assert math.isclose(
        load_balance_aux_fraction(uniform_counts, uniform_mass), 1.0, abs_tol=1e-9
    )


@pytest.mark.unit
def test_aux_fraction_concentrated_exceeds_one() -> None:
    counts = np.zeros(E)
    counts[0] = 32.0
    mass = np.zeros(E)
    mass[0] = 1.0
    # Both dispatch and mass on a single expert -> aux fraction == E.
    assert math.isclose(load_balance_aux_fraction(counts, mass), float(E), abs_tol=1e-6)


@pytest.mark.unit
def test_aux_fraction_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        load_balance_aux_fraction(np.ones(E), np.ones(E + 1))


@pytest.mark.unit
def test_js_identical_is_zero() -> None:
    p = np.array([0.1, 0.2, 0.3, 0.4])
    assert math.isclose(jensen_shannon_divergence(p, p.copy()), 0.0, abs_tol=1e-12)


@pytest.mark.unit
def test_js_disjoint_is_one_bit() -> None:
    p = np.array([1.0, 0.0, 0.0, 0.0])
    q = np.array([0.0, 0.0, 0.0, 1.0])
    # Disjoint supports -> JS divergence == 1 bit (base 2).
    assert math.isclose(jensen_shannon_divergence(p, q), 1.0, abs_tol=1e-9)


@pytest.mark.unit
def test_js_symmetric() -> None:
    p = np.array([0.5, 0.3, 0.2, 0.0])
    q = np.array([0.1, 0.1, 0.4, 0.4])
    assert math.isclose(
        jensen_shannon_divergence(p, q), jensen_shannon_divergence(q, p), abs_tol=1e-12
    )


@pytest.mark.unit
def test_js_shape_mismatch_raises() -> None:
    with pytest.raises(ValueError):
        jensen_shannon_divergence(np.ones(3), np.ones(4))


@pytest.mark.unit
def test_pairwise_js_identical_buckets_zero() -> None:
    base = np.array([0.25, 0.25, 0.25, 0.25])
    buckets = {0: base.copy(), 1: base.copy(), 2: base.copy()}
    result = pairwise_js_across_buckets(buckets)
    # All pairwise and vs-marginal comparisons must be ~0.
    assert all(math.isclose(v, 0.0, abs_tol=1e-9) for v in result.values())
    # Expect 3 pairs + 3 vs-marginal entries.
    assert (0, 1) in result and (1, 2) in result and (0, 2) in result
    assert (0, -1) in result and (1, -1) in result and (2, -1) in result


@pytest.mark.unit
def test_pairwise_js_divergent_buckets_positive() -> None:
    buckets = {
        0: np.array([1.0, 0.0, 0.0, 0.0]),
        1: np.array([0.0, 0.0, 0.0, 1.0]),
    }
    result = pairwise_js_across_buckets(buckets)
    assert result[(0, 1)] > 0.5  # disjoint -> large JS


@pytest.mark.unit
def test_pairwise_js_empty() -> None:
    assert pairwise_js_across_buckets({}) == {}


@pytest.mark.unit
def test_marginal_is_traffic_weighted_not_plain_mean() -> None:
    # MINOR 8: marginal must SUM raw counts (traffic-weighted), so a tiny
    # low-traffic bucket cannot pull the marginal toward its distribution.
    # Big bucket: all mass on expert 0 (1000 selections). Tiny bucket: all mass
    # on expert 3 (2 selections). A plain mean of the two normalized dists would
    # put 0.5 on expert 3; the correct traffic-weighted marginal puts ~0.002.
    buckets = {
        0: np.array([1000.0, 0.0, 0.0, 0.0]),
        1: np.array([0.0, 0.0, 0.0, 2.0]),
    }
    result = pairwise_js_across_buckets(buckets)
    # Big bucket vs marginal must be tiny (marginal ~= big bucket's dist).
    assert result[(0, -1)] < 0.05
    # Tiny bucket vs marginal must be near-maximal (it disagrees with the bulk).
    assert result[(1, -1)] > 0.8


@pytest.mark.unit
def test_bootstrap_noise_floor_same_law_is_small() -> None:
    # Null: both buckets route the same fixed way -> pooled resampling at their
    # sizes yields ~0 JS noise floor.
    num_tokens = 400
    top_k = 8
    fixed = np.arange(top_k)
    sel_a = np.tile(fixed, (num_tokens, 1))
    sel_b = np.tile(fixed, (num_tokens, 1))
    floor = bootstrap_js_noise_floor(sel_a, sel_b, num_experts=128, n_resamples=200, seed=1)
    assert floor.ci_high < 1e-6
    assert floor.n_resamples == 200


@pytest.mark.unit
def test_bootstrap_noise_floor_random_routing_has_floor() -> None:
    # Random-but-shared routing: pooled resampling still produces a small but
    # nonzero JS floor (sampling noise). This is the threshold a signal must beat.
    rng = np.random.default_rng(7)
    top_k = 8
    sel_a = rng.integers(0, 128, size=(300, top_k))
    sel_b = rng.integers(0, 128, size=(300, top_k))
    floor = bootstrap_js_noise_floor(sel_a, sel_b, num_experts=128, n_resamples=300, seed=2)
    assert floor.ci_high >= floor.mean >= floor.ci_low >= 0.0
    assert 0.0 < floor.ci_high < 0.5  # noise, not separation


@pytest.mark.unit
def test_bootstrap_noise_floor_unequal_bucket_sizes() -> None:
    # MAJOR 4: floor must scale to the ACTUAL (unequal) bucket sizes; a tiny
    # bucket vs a large one yields a wider null than two large buckets.
    rng = np.random.default_rng(21)
    top_k = 8
    big = rng.integers(0, 128, size=(1000, top_k))
    small = rng.integers(0, 128, size=(40, top_k))
    floor_unequal = bootstrap_js_noise_floor(big, small, num_experts=128, n_resamples=300, seed=5)
    floor_equal = bootstrap_js_noise_floor(big, big, num_experts=128, n_resamples=300, seed=5)
    # The small bucket's higher sampling variance widens its null floor.
    assert floor_unequal.ci_high > floor_equal.ci_high


@pytest.mark.unit
def test_divergent_buckets_beat_their_pair_floor() -> None:
    # Two t-buckets whose token routing genuinely differs; cross-t JS exceeds
    # the pair-specific within-t noise floor.
    rng = np.random.default_rng(11)
    num_experts = 128
    top_k = 8
    n = 400
    sel_a = rng.integers(0, 16, size=(n, top_k))
    sel_b = rng.integers(64, 80, size=(n, top_k))

    cross_t_js = jensen_shannon_divergence(
        np.bincount(sel_a.reshape(-1), minlength=num_experts),
        np.bincount(sel_b.reshape(-1), minlength=num_experts),
    )
    floor = bootstrap_js_noise_floor(sel_a, sel_b, num_experts, n_resamples=200, seed=3)
    assert cross_t_js > floor.ci_high


@pytest.mark.unit
def test_same_law_buckets_within_pair_floor() -> None:
    # Negative control: same routing law -> cross-t JS within the pair floor.
    rng = np.random.default_rng(13)
    num_experts = 128
    top_k = 8
    n = 400
    sel_a = rng.integers(0, 128, size=(n, top_k))
    sel_b = rng.integers(0, 128, size=(n, top_k))

    cross_t_js = jensen_shannon_divergence(
        np.bincount(sel_a.reshape(-1), minlength=num_experts),
        np.bincount(sel_b.reshape(-1), minlength=num_experts),
    )
    floor = bootstrap_js_noise_floor(sel_a, sel_b, num_experts, n_resamples=300, seed=4)
    assert cross_t_js <= floor.ci_high + 1e-9


@pytest.mark.unit
def test_bootstrap_empty_bucket_returns_zero_floor() -> None:
    floor = bootstrap_js_noise_floor(
        np.array([[0, 1]]), np.empty((0, 2), dtype=np.int32), num_experts=8, n_resamples=10
    )
    assert floor.ci_high == 0.0 and floor.n_resamples == 0


@pytest.mark.unit
def test_bootstrap_rejects_bad_shape() -> None:
    with pytest.raises(ValueError):
        bootstrap_js_noise_floor(np.array([0, 1, 2]), np.array([[0, 1]]), num_experts=8)


@pytest.mark.unit
def test_bootstrap_rejects_out_of_range_expert() -> None:
    with pytest.raises(ValueError):
        bootstrap_js_noise_floor(np.array([[0, 99]]), np.array([[0, 1]]), num_experts=8)
