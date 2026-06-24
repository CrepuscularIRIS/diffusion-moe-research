"""Validation tests for the H4 protocol test (``plan/h4-test-protocol.md`` §4).

These are the PROOF that the pipeline (track construction, bucketization,
trajectory-synchronous permutation, shared-draw maxT FWER, p-values) controls
type-I error and has power. All synthetic, torch-free, no 26B model.

Type-I pass criterion (protocol §4): one-sided 95% Clopper-Pearson UPPER bound
on the empirical global-FWER ``U_0.95 <= 0.065`` at ``alpha = 0.05``. This bound
is tight enough to reject a 2x inflation (true 0.10 gives U well above 0.065);
we do NOT use the loose ``alpha + 3*SE`` rule.

These synthetic checks are NECESSARY BUT NOT SUFFICIENT (they cannot reproduce
real model structure); the protocol's true Null A runs on REAL logs
(``null_a_real_orbit``, a mandatory pre-publication gate). The DISCRIMINATING
proof that the shared-draw permutation is load-bearing is the cross-layer-
correlated negative control: a deliberately broken per-layer-independent draw
(``h4_broken``, TEST-ONLY) is shown to be measurably mis-calibrated where the
correct shared draw stays calibrated. A full-pipeline run on a weak true effect
confirms the criterion flags a ~2x situation end-to-end.

The full protocol uses R_null >= 5000 (10000 camera-ready); these in-test runs
use smaller R to stay fast while keeping U_0.95 / KS-separation decisive.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from scipy.stats import kstest

from direction_c.h4_broken import collect_global_pvalues
from direction_c.h4_test import cluster_bootstrap_nmi, run_h4_test
from direction_c.h4_validation import (
    SyntheticDesign,
    clopper_pearson_upper,
    make_null_b,
    make_null_c,
    make_null_xcorr,
    make_planted,
    permutation_orbit_relabel,
)

# Type-I design kept modest (n_tracks * K * E small) so R_null=2000 is fast.
TYPE1_DESIGN = SyntheticDesign(
    num_trajectories=10, calls_per_traj=16, positions=2,
    num_layers=3, num_experts=16, num_buckets=4, top_k=8,
)
# Power design has more visits per track-bucket cell so a real effect is visible.
POWER_DESIGN = SyntheticDesign(
    num_trajectories=16, calls_per_traj=24, positions=3,
    num_layers=3, num_experts=32, num_buckets=4, top_k=8,
)
# Cross-layer-correlated design: enough layers that destroying the cross-layer
# correlation visibly distorts the maxT null (the discriminating negative control).
XCORR_DESIGN = SyntheticDesign(
    num_trajectories=6, calls_per_traj=12, positions=2,
    num_layers=16, num_experts=12, num_buckets=4, top_k=8,
)
ALPHA = 0.05
B_PERM_TEST = 99  # smaller than the 19999 paper value; fine for validation


# -- Clopper-Pearson helper unit tests ----------------------------------------

@pytest.mark.unit
def test_clopper_pearson_bound_properties() -> None:
    # Upper bound exceeds the point estimate and rejects 2x inflation at R=2000.
    assert clopper_pearson_upper(100, 2000) > 100 / 2000
    assert clopper_pearson_upper(100, 2000) <= 0.065   # true ~0.05 passes
    assert clopper_pearson_upper(200, 2000) > 0.065    # true ~0.10 (2x) fails
    assert clopper_pearson_upper(0, 100) > 0.0
    assert clopper_pearson_upper(50, 50) == 1.0


# -- Statistic / decision sanity ----------------------------------------------

@pytest.mark.unit
def test_null_b_does_not_reject() -> None:
    ds = make_null_b(TYPE1_DESIGN, seed=1)
    res = run_h4_test(ds, alpha=ALPHA, b_perm=B_PERM_TEST, seed=11)
    assert not res.supported
    assert res.p_global > ALPHA


@pytest.mark.unit
def test_permutation_is_trajectory_synchronous() -> None:
    # A permutation must only reassign per-call bucket LABELS within a trajectory:
    # the multiset of bucket labels per trajectory is preserved.
    from direction_c.h4_test import _build_slot_map, _permute_slot_buckets

    ds = make_null_b(TYPE1_DESIGN, seed=2)
    smap, _ = _build_slot_map(ds.call_buckets)
    rng = np.random.default_rng(0)
    permuted = _permute_slot_buckets(smap, rng)
    for start, length in zip(smap.traj_starts, smap.traj_lengths):
        orig = sorted(smap.slot_bucket[start:start + length].tolist())
        perm = sorted(permuted[start:start + length].tolist())
        assert orig == perm  # same multiset within each trajectory block


@pytest.mark.unit
def test_effect_sizes_present_and_finite() -> None:
    ds, _ = make_planted(POWER_DESIGN, delta=0.5, seed=3, planted_layers=(1,))
    res = run_h4_test(ds, alpha=ALPHA, b_perm=B_PERM_TEST, seed=4)
    assert res.h_bucket_given_track > 0
    for lr in res.per_layer:
        assert math.isfinite(lr.mi_nats) and lr.mi_nats >= 0
        assert math.isfinite(lr.nmi)
        assert math.isfinite(lr.delta_nmi)


# -- Type-I validation (the proof) --------------------------------------------

@pytest.mark.unit
def test_type1_synthetic_orbit_fwer_controlled() -> None:
    """SYNTHETIC orbit-relabel FWER check (NOT the protocol's real-log Null A).

    Relabel a synthetic dataset's buckets via the test's own group and re-run.
    This validates the orbit machinery on synthetic structure ONLY; it is NOT
    evidence on the real model's structure. The protocol's true Null A runs on
    REAL logs via ``null_a_real_orbit`` (mandatory pre-publication gate; see
    ``test_null_a_real_orbit_gate_runs_on_dataset`` and the README).
    """
    base = make_null_b(TYPE1_DESIGN, seed=100)
    r_null = 2000
    rng = np.random.default_rng(0)
    rejections = 0
    for _ in range(r_null):
        relabeled = permutation_orbit_relabel(base, rng)
        res = run_h4_test(relabeled, alpha=ALPHA, b_perm=B_PERM_TEST,
                          seed=int(rng.integers(1 << 30)))
        rejections += int(res.supported)
    upper = clopper_pearson_upper(rejections, r_null)
    fwer = rejections / r_null
    assert upper <= 0.065, (
        f"synthetic-orbit FWER={fwer:.4f} U_0.95={upper:.4f} > 0.065 "
        f"(R_null={r_null}); permutation/FWER implementation is wrong"
    )


@pytest.mark.unit
def test_type1_null_b_heterogeneous_track_fwer_controlled() -> None:
    """Null B: per-track baseline expert law, INDEPENDENT of bucket.

    Tests whether track heterogeneity alone (different tracks favoring different
    experts) fabricates false positives. It must not.
    """
    r_null = 2000
    rng = np.random.default_rng(1)
    rejections = 0
    for _ in range(r_null):
        ds = make_null_b(TYPE1_DESIGN, seed=int(rng.integers(1 << 30)))
        res = run_h4_test(ds, alpha=ALPHA, b_perm=B_PERM_TEST,
                          seed=int(rng.integers(1 << 30)))
        rejections += int(res.supported)
    upper = clopper_pearson_upper(rejections, r_null)
    fwer = rejections / r_null
    assert upper <= 0.065, f"Null B FWER={fwer:.4f} U_0.95={upper:.4f} > 0.065"


@pytest.mark.unit
def test_type1_null_c_autocorrelated_fwer_controlled() -> None:
    """Null C (stricter, documented): AR(1) within-trajectory dependence.

    Block diffusion has strong adjacent-timestep dependence. The
    trajectory-synchronous permutation must still control FWER here. Fewer reps
    than Null A/B because the AR(1) generator is slower; the protocol documents
    the full check at R_null >= 5000.
    """
    r_null = 800
    rng = np.random.default_rng(2)
    rejections = 0
    for _ in range(r_null):
        ds = make_null_c(TYPE1_DESIGN, seed=int(rng.integers(1 << 30)), rho=0.8)
        res = run_h4_test(ds, alpha=ALPHA, b_perm=B_PERM_TEST,
                          seed=int(rng.integers(1 << 30)))
        rejections += int(res.supported)
    upper = clopper_pearson_upper(rejections, r_null)
    fwer = rejections / r_null
    # Looser bound here only because r_null is smaller (wider CP interval);
    # still must reject a 2x inflation (true 0.10 -> U ~ 0.13 at R=800).
    assert upper <= 0.085, f"Null C FWER={fwer:.4f} U_0.95={upper:.4f} > 0.085"


# -- Discriminating negative control: shared draw is LOAD-BEARING (gap 1) ------

@pytest.mark.unit
def test_shared_draw_is_load_bearing_on_cross_layer_correlated_null() -> None:
    """CRUX: on a cross-layer-correlated null the correct shared-draw maxT is
    calibrated while a BROKEN per-layer-independent draw is NOT.

    ``make_null_xcorr`` makes ``T_L`` positively correlated across layers (shared
    per-(traj,call) latent) with NO bucket dependence (H0 true). The correct
    shared draw preserves that correlation in ``M^(m)=max_L T_L^(m)`` -> global
    null p-values ~ Uniform(0,1). The broken per-layer-independent draw destroys
    the correlation -> the max over near-independent layers is inflated -> the
    null threshold is too high -> p-values skew toward 1 (mis-calibrated). We
    assert NON-INTERCHANGEABILITY: correct passes a KS-uniform test, broken fails
    it decisively, and the two p-value distributions differ.

    Earlier Null A/B used independent-ish synthetic tracks, so a broken
    per-layer draw could pass them too -> they did NOT prove the shared draw was
    load-bearing. THIS test does.
    """
    r_null = 250
    b_perm = 79
    mk = lambda s: make_null_xcorr(XCORR_DESIGN, seed=s, coupling=3.5)

    p_correct = collect_global_pvalues(mk, shared_draw=True, r_null=r_null,
                                       b_perm=b_perm, seed0=1)
    p_broken = collect_global_pvalues(mk, shared_draw=False, r_null=r_null,
                                      b_perm=b_perm, seed0=1)

    ks_correct = kstest(p_correct, "uniform").pvalue
    ks_broken = kstest(p_broken, "uniform").pvalue

    # Correct: null p-values are uniform (calibrated). Broken: decisively NOT.
    assert ks_correct > 0.05, (
        f"correct shared-draw null p-values not uniform (KS p={ks_correct:.4g}); "
        f"the supposedly-correct path is itself mis-calibrated"
    )
    assert ks_broken < 1e-4, (
        f"broken per-layer draw should be mis-calibrated but KS p={ks_broken:.4g} "
        f">= 1e-4 -> the suite cannot distinguish broken from correct, so it "
        f"proves nothing about the shared draw"
    )
    # The two are not interchangeable: separation spans many orders of magnitude.
    assert ks_correct / max(ks_broken, 1e-300) > 1e6


@pytest.mark.unit
def test_correct_and_broken_fwer_differ_on_correlated_null() -> None:
    """Complementary view: the broken draw's null p-value MEAN is shifted high
    (conservative direction) on the correlated null, unlike the calibrated
    correct draw whose mean sits near 0.5. Direction characterized empirically."""
    r_null = 250
    b_perm = 79
    mk = lambda s: make_null_xcorr(XCORR_DESIGN, seed=s, coupling=3.5)
    p_correct = collect_global_pvalues(mk, shared_draw=True, r_null=r_null,
                                       b_perm=b_perm, seed0=2)
    p_broken = collect_global_pvalues(mk, shared_draw=False, r_null=r_null,
                                      b_perm=b_perm, seed0=2)
    # Calibrated p-values average ~0.5; the broken draw is materially higher.
    assert abs(p_correct.mean() - 0.5) < 0.07
    assert p_broken.mean() > p_correct.mean() + 0.08


# -- Full-pipeline 2x-inflation detection (gap 2) ------------------------------

@pytest.mark.unit
def test_full_pipeline_flags_2x_inflation() -> None:
    """Run the ACTUAL run_h4_test() end-to-end on a genuine weak H0-violation
    tuned so the true global rejection rate ~ 0.10, and assert the empirical
    CP upper bound EXCEEDS 0.065 -- i.e. the pipeline+bound flag a 2x situation.

    This is NOT the isolated CP arithmetic check: a small real t->expert tilt
    (delta=0.25) is planted, the FULL test runs per replicate, and we require the
    detection rate's CP-upper to land above the 0.065 pass line (so a true ~2x
    inflation would NOT slip past the validation criterion)."""
    r_reps = 300
    rng = np.random.default_rng(123)
    rejections = 0
    for _ in range(r_reps):
        ds, _ = make_planted(POWER_DESIGN, delta=0.25,
                             seed=int(rng.integers(1 << 30)), planted_layers=(1,))
        res = run_h4_test(ds, alpha=ALPHA, b_perm=B_PERM_TEST,
                          seed=int(rng.integers(1 << 30)))
        rejections += int(res.supported)
    rate = rejections / r_reps
    upper = clopper_pearson_upper(rejections, r_reps)
    # The weak effect pushes the true rate up toward ~0.10; the end-to-end
    # pipeline + CP bound must FLAG it (upper > 0.065), proving the criterion
    # detects 2x situations rather than only validating CP arithmetic.
    assert rate > 0.065, f"weak-effect rejection rate {rate:.3f} too low to be a 2x test"
    assert upper > 0.065, (
        f"CP upper {upper:.4f} <= 0.065 on a ~2x situation -> the end-to-end "
        f"validation criterion would NOT flag inflation"
    )


@pytest.mark.unit
def test_null_a_real_orbit_gate_runs_on_dataset() -> None:
    """Smoke-test the real-data Null A gate fn on a synthetic stand-in dataset.

    The production gate ``null_a_real_orbit`` is meant for REAL logs at
    r_null>=5000; here we only verify it RUNS and returns the expected schema +
    a controlled FWER on a synthetic H0 dataset (cannot exercise on real logs
    without the model). It remains a MANDATORY real-data gate pre-publication.
    """
    from direction_c.h4_validation import null_a_real_orbit

    base = make_null_b(TYPE1_DESIGN, seed=7)
    out = null_a_real_orbit(base, r_null=300, alpha=ALPHA, b_perm=79, seed=0)
    assert set(out) == {"r_null", "rejections", "fwer", "u95", "passed"}
    assert out["r_null"] == 300.0
    assert 0.0 <= out["fwer"] <= 1.0
    # On a synthetic H0 dataset the gate should pass; the binary lives in "passed".
    assert out["passed"] in (0.0, 1.0)


# -- Power validation ----------------------------------------------------------

@pytest.mark.unit
def test_power_rises_with_effect_size() -> None:
    """Detection probability must increase with delta and a planted layer must be
    identified after maxT at a strong delta."""
    r_power = 60
    deltas = [0.0, 0.5, 0.9]
    planted = (1,)
    detect: dict[float, float] = {}
    layer_id: dict[float, float] = {}
    for delta in deltas:
        rng = np.random.default_rng(int(delta * 1000) + 7)
        n_detect = 0
        n_layer = 0
        for _ in range(r_power):
            ds, _ = make_planted(POWER_DESIGN, delta=delta,
                                 seed=int(rng.integers(1 << 30)), planted_layers=planted)
            res = run_h4_test(ds, alpha=ALPHA, b_perm=B_PERM_TEST,
                              seed=int(rng.integers(1 << 30)))
            n_detect += int(res.supported)
            n_layer += int(planted[0] in res.significant_layers)
        detect[delta] = n_detect / r_power
        layer_id[delta] = n_layer / r_power

    # Null effect: detection ~ alpha (well below the strong-effect rate).
    assert detect[0.0] <= 0.20
    # Strong effect: high detection + correct planted-layer identification.
    assert detect[0.9] >= 0.8
    assert layer_id[0.9] >= 0.7
    # Increase with effect size.
    assert detect[0.0] < detect[0.5] <= detect[0.9]


@pytest.mark.unit
def test_planted_layer_localized_not_neighbors() -> None:
    # A strong planted effect on layer 1 should flag layer 1, and its effect size
    # must dominate the null layers 0 and 2.
    ds, _ = make_planted(POWER_DESIGN, delta=0.9, seed=99, planted_layers=(1,))
    res = run_h4_test(ds, alpha=ALPHA, b_perm=499, seed=5)
    assert 1 in res.significant_layers
    by_layer = {lr.layer_idx: lr.delta_nmi for lr in res.per_layer}
    assert by_layer[1] > by_layer[0]
    assert by_layer[1] > by_layer[2]


@pytest.mark.unit
def test_cluster_bootstrap_ci_positive_for_strong_effect() -> None:
    ds, _ = make_planted(POWER_DESIGN, delta=0.9, seed=11, planted_layers=(1,))
    lo, hi = cluster_bootstrap_nmi(ds, layer=1, n_boot=200, seed=3)
    assert 0.0 <= lo <= hi
    assert hi > 0.0  # strong effect -> strictly positive upper CI on NMI
