"""
Property-based and unit tests for Diagenetic Tiering Primitives.
Uses Hypothesis to verify physical invariants, monotonicity, and analytical baselines.
"""

import math
import numpy as np
import pytest
from hypothesis import given, strategies as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'models'))
from primitives import (

    analytical_steady_state_exponential,
    aerobic_niche_integral,
    biodiffusion_kernel,
    diagenetic_divergence_1d,
    respiration_sink,
)


class TestBiodiffusionKernelProperties:
    """Hypothesis tests for Primitive 1: biodiffusion_kernel."""

    @given(
        z=st.floats(min_value=0.0, max_value=200.0),
        z_max=st.floats(min_value=0.0, max_value=100.0),
        d_b0=st.floats(min_value=0.1, max_value=100.0),
        sigma=st.floats(min_value=1.0, max_value=20.0),
    )
    def test_positivity_and_plateau_invariant(self, z: float, z_max: float, d_b0: float, sigma: float):
        val = biodiffusion_kernel(z, z_max, d_b0, sigma)
        # Invariant 1: Strictly non-negative
        assert val >= 0.0
        # Invariant 2: Bounded by d_b0
        assert val <= d_b0 + 1e-9
        # Invariant 3: Equal to d_b0 within the mixed layer
        if z <= z_max:
            assert abs(val - d_b0) < 1e-9

    @given(
        z1=st.floats(min_value=0.0, max_value=100.0),
        z2=st.floats(min_value=0.0, max_value=100.0),
        z_max=st.floats(min_value=0.0, max_value=50.0),
        d_b0=st.floats(min_value=1.0, max_value=50.0),
    )
    def test_monotonicity_beyond_mixed_layer(self, z1: float, z2: float, z_max: float, d_b0: float):
        low_z = min(z1, z2)
        high_z = max(z1, z2)
        if low_z >= z_max:
            val_low = biodiffusion_kernel(low_z, z_max, d_b0)
            val_high = biodiffusion_kernel(high_z, z_max, d_b0)
            # Invariant 4: Monotonically non-increasing with depth
            assert val_low >= val_high - 1e-9


class TestRespirationSinkProperties:
    """Hypothesis tests for Primitive 2: respiration_sink."""

    @given(
        c=st.floats(min_value=0.0, max_value=100.0),
        o2=st.floats(min_value=0.0, max_value=500.0),
        k_c=st.floats(min_value=0.01, max_value=10.0),
        km=st.floats(min_value=0.1, max_value=10.0),
    )
    def test_kinetics_bounds(self, c: float, o2: float, k_c: float, km: float):
        sink = respiration_sink(c, o2, k_c, km)
        # Invariant 1: Non-negative
        assert sink >= 0.0
        # Invariant 2: Bounded by first-order uninhibited ceiling k_c * C
        assert sink <= (k_c * c) + 1e-9
        # Invariant 3: Zero when either substrate is zero
        if c == 0.0 or o2 == 0.0:
            assert abs(sink) < 1e-9


class TestConservationAndAnalyticalVerification:
    """Tests spatial flux divergence against analytical solutions."""

    def test_diffusion_decay_analytical_match(self):
        """
        Asserts that diagenetic_divergence matches analytical steady state:
        D * d2C/dz2 - k*C = 0 => C(z) = C0 * exp(-z * sqrt(k/D))
        """
        n = 101
        dz = 1.0  # 1 mm
        z_grid = np.linspace(0.0, 100.0, n)
        c0 = 10.0
        d_val = 50.0
        k_val = 0.5

        # Analytical steady profile
        c_ana = analytical_steady_state_exponential(z_grid, c0, d_val, k_val)
        d_grid = np.full(n, d_val)

        # Spatial divergence
        div = diagenetic_divergence_1d(c_ana, d_grid, dz)
        # Decay sink: - k * C
        sink = k_val * c_ana

        # Net dC/dt = div - sink should be approximately zero on interior cells
        residual = div[5:-5] - sink[5:-5]
        max_err = np.max(np.abs(residual))
        assert max_err < 0.05  # Within 2nd-order spatial discretization error


class TestAerobicNicheMonotonicity:
    """Verifies that deepening tiering expands available aerobic niche."""

    def test_tiering_depth_monotonically_increases_niche_capacity(self):
        z_grid = np.linspace(0.0, 100.0, 101)
        c_profile = np.full(101, 10.0)

        # Case 1: Ediacaran shallow O2 penetration (e.g. 5 mm)
        o2_ediacaran = 250.0 * np.exp(-z_grid / 2.0)
        niche_ed = aerobic_niche_integral(z_grid, c_profile, o2_ediacaran, o2_threshold=2.0)

        # Case 2: Cambrian deep bioturbated O2 penetration (e.g. 40 mm)
        o2_cambrian = 250.0 * np.exp(-z_grid / 15.0)
        niche_cb = aerobic_niche_integral(z_grid, c_profile, o2_cambrian, o2_threshold=2.0)

        assert niche_cb > niche_ed * 3.0
