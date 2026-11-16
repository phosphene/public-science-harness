"""
Property-based and unit tests for Macroevolutionary Birth-Death Primitives.
Uses Hypothesis to verify mathematical invariants, boundary conditions, and monotonicity.
"""

import math
import numpy as np
import pytest
from hypothesis import given, strategies as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from birth_death_primitives import (
    keiding_sampling_probability,
    diversity_dependent_hazard,
    poisson_occurrence_loglik,
    lineage_survival_loglik,
    standing_diversity_trajectory,
)


class TestKeidingSamplingProperties:
    """Hypothesis tests for Primitive 1: keiding_sampling_probability."""

    @given(
        s=st.floats(min_value=1.0, max_value=600.0),
        duration=st.floats(min_value=0.0, max_value=100.0),
        q=st.floats(min_value=0.0, max_value=10.0),
    )
    def test_keiding_probability_bounds_and_limits(self, s: float, duration: float, q: float):
        e = max(0.0, s - duration)
        prob = keiding_sampling_probability(s, e, q)
        
        # Invariant 1: Strictly within [0, 1]
        assert 0.0 <= prob <= 1.0
        
        # Invariant 2: Exactly 0 if duration is 0 or q is 0
        if s == e or q == 0.0:
            assert prob == 0.0

    @given(
        s=st.floats(min_value=50.0, max_value=100.0),
        e=st.floats(min_value=0.0, max_value=40.0),
        q1=st.floats(min_value=0.01, max_value=5.0),
        q2=st.floats(min_value=0.01, max_value=5.0),
    )
    def test_keiding_monotonicity_in_sampling_rate(self, s: float, e: float, q1: float, q2: float):
        low_q = min(q1, q2)
        high_q = max(q1, q2)
        p_low = keiding_sampling_probability(s, e, low_q)
        p_high = keiding_sampling_probability(s, e, high_q)
        assert p_low <= p_high + 1e-9


class TestDiversityDependentHazardProperties:
    """Hypothesis tests for Primitive 2: diversity_dependent_hazard."""

    @given(
        n=st.integers(min_value=0, max_value=500),
        rate_0=st.floats(min_value=0.01, max_value=5.0),
        gl=st.floats(min_value=-0.5, max_value=0.5),
    )
    def test_dd_hazard_positivity_and_baseline(self, n: int, rate_0: float, gl: float):
        r_exp = diversity_dependent_hazard(n, rate_0, gl, model="exponential")
        r_lin = diversity_dependent_hazard(n, rate_0, gl, model="linear")
        
        # Invariant 1: Strictly non-negative
        assert r_exp >= 0.0
        assert r_lin >= 0.0
        
        # Invariant 2: At N=0 or Gl=0, matches baseline
        if n == 0 or gl == 0.0:
            assert abs(r_exp - rate_0) < 1e-7
            assert abs(r_lin - rate_0) < 1e-7

    @given(
        rate_0=st.floats(min_value=0.1, max_value=2.0),
        gl_neg=st.floats(min_value=-0.1, max_value=-0.001),
        gl_pos=st.floats(min_value=0.001, max_value=0.1),
    )
    def test_dd_hazard_sign_reversal_monotonicity(self, rate_0: float, gl_neg: float, gl_pos: float):
        # Ecological guild (Gl < 0): rate monotonically decreases as diversity rises
        r_low_n = diversity_dependent_hazard(10, rate_0, gl_neg)
        r_high_n = diversity_dependent_hazard(50, rate_0, gl_neg)
        assert r_high_n < r_low_n

        # Hominin / cultural clade (Gl > 0): rate monotonically increases as diversity rises
        r_cul_low = diversity_dependent_hazard(10, rate_0, gl_pos)
        r_cul_high = diversity_dependent_hazard(50, rate_0, gl_pos)
        assert r_cul_high > r_cul_low


class TestPoissonOccurrenceProperties:
    """Tests for Primitive 3: poisson_occurrence_loglik."""

    def test_occurrence_outside_lifespan_is_strictly_impossible(self):
        s = 530.0
        e = 520.0
        q = 1.0
        # Valid occurrences within [520, 530]
        assert math.isfinite(poisson_occurrence_loglik([528.0, 522.0], s, e, q))
        
        # Occurrence younger than extinction e -> impossible
        assert poisson_occurrence_loglik([519.0], s, e, q) == -float("inf")
        
        # Occurrence older than origination s -> impossible
        assert poisson_occurrence_loglik([531.0], s, e, q) == -float("inf")


class TestStandingDiversityTrajectory:
    """Tests for Primitive 5: standing_diversity_trajectory."""

    def test_standing_diversity_count_reconstruction(self):
        lineages = [
            (530.0, 510.0),  # Lineage 1 active [510, 530]
            (525.0, 515.0),  # Lineage 2 active [515, 525]
            (512.0, 500.0),  # Lineage 3 active [500, 512]
        ]
        times = np.array([535.0, 528.0, 520.0, 513.0, 505.0, 495.0])
        counts = standing_diversity_trajectory(lineages, times)
        
        # 535: none active -> 0
        # 528: Lineage 1 active -> 1
        # 520: Lineage 1 & 2 active -> 2
        # 513: Lineage 1 active -> 1
        # 505: Lineage 3 active -> 1
        # 495: none active -> 0
        expected = np.array([0, 1, 2, 1, 1, 0])
        np.testing.assert_array_equal(counts, expected)
