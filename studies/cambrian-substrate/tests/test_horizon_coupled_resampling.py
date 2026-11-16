"""
Property-based and unit tests for HorizonCoupledResampler (DEC-PYRATE-002).
Verifies that contemporaneity within geological horizons is strictly preserved,
preventing Anti-Pattern 2 (independent scattering and false boundary spikes).
"""

import sys
from pathlib import Path
import numpy as np
import pytest
from hypothesis import given, strategies as st

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from horizon_coupled_resampler import HorizonCoupledResampler, StratigraphicOccurrence


class TestHorizonCoupledProperties:
    """Hypothesis tests for stratigraphic coupling invariants."""

    @given(
        u_seed=st.integers(min_value=0, max_value=10000),
        top_age=st.floats(min_value=500.0, max_value=530.0),
        span=st.floats(min_value=1.0, max_value=20.0),
    )
    def test_strict_horizon_contemporaneity(self, u_seed: int, top_age: float, span: float):
        bottom_age = top_age + span
        
        # Create 5 distinct taxa from the exact same bonebed/horizon
        occurrences = [
            StratigraphicOccurrence(
                occurrence_id=f"occ_{i}",
                taxon_name=f"Taxon_{chr(65+i)}",
                horizon_id="HZ_CHENGJIANG_BED_01",
                age_top_ma=top_age,
                age_bottom_ma=bottom_age,
            )
            for i in range(5)
        ]
        
        resampler = HorizonCoupledResampler(occurrences)
        rep = resampler.generate_replicate(replicate_id=1, seed=u_seed)
        
        # Invariant 1: All occurrences from the same horizon MUST have the EXACT same age
        ages = list(rep.occurrence_ages.values())
        first_age = ages[0]
        for a in ages[1:]:
            assert a == first_age, f"Coupled age violation: {a} != {first_age}"
            
        # Invariant 2: Age must lie strictly within [age_top, age_bottom]
        assert top_age <= first_age <= bottom_age + 1e-4

    def test_distinct_horizons_have_independent_draws(self):
        occurrences = [
            StratigraphicOccurrence(
                occurrence_id="occ_1",
                taxon_name="Kimberella",
                horizon_id="HZ_WHITE_SEA",
                age_top_ma=550.0,
                age_bottom_ma=558.0,
            ),
            StratigraphicOccurrence(
                occurrence_id="occ_2",
                taxon_name="Treptichnus",
                horizon_id="HZ_FORTUNE_HEAD",
                age_top_ma=529.0,
                age_bottom_ma=541.0,
            ),
        ]
        resampler = HorizonCoupledResampler(occurrences)
        rep = resampler.generate_replicate(replicate_id=42, seed=42)
        
        age1 = rep.occurrence_ages["occ_1"]
        age2 = rep.occurrence_ages["occ_2"]
        
        assert 550.0 <= age1 <= 558.0
        assert 529.0 <= age2 <= 541.0
        # Stratigraphic ordering between terminal Ediacaran and Fortunian is preserved
        assert age1 > age2
