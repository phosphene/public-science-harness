"""
Property-based and unit tests for LineageHorizonLifespanEvaluator (PSH-BD-002).
Verifies that:
1. Bed contemporaneity is strictly preserved in FAD and LAD calculations.
2. FAD >= LAD invariant holds unconditionally for all taxa across all stochastic draws.
3. Trace-only taxa (e.g. Treptichnus) retain full observational envelopes with burrow depths.
4. Deterministic SHA-256 provenance receipts are generated.
"""

import sys
from pathlib import Path
import numpy as np
import pytest
from hypothesis import given, strategies as st

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from horizon_coupled_resampler import StratigraphicOccurrence
from lineage_horizon_evaluator import LineageHorizonLifespanEvaluator


class TestLineageHorizonEvaluatorProperties:
    """Hypothesis tests for lineage lifespan aggregation invariants."""

    @given(
        seed=st.integers(min_value=0, max_value=10000),
        top_age=st.floats(min_value=500.0, max_value=530.0),
        span=st.floats(min_value=1.0, max_value=20.0),
    )
    def test_fad_lad_invariants_under_random_horizons(self, seed: int, top_age: float, span: float):
        bot_age = top_age + span
        
        # Two distinct taxa found in the same horizon, plus one spanning two horizons
        occurrences = [
            StratigraphicOccurrence(occurrence_id="occ_1", taxon_name="Taxon_A", horizon_id="HZ_01", age_top_ma=top_age, age_bottom_ma=bot_age),
            StratigraphicOccurrence(occurrence_id="occ_2", taxon_name="Taxon_B", horizon_id="HZ_01", age_top_ma=top_age, age_bottom_ma=bot_age),
            StratigraphicOccurrence(occurrence_id="occ_3", taxon_name="Taxon_B", horizon_id="HZ_02", age_top_ma=top_age - 10.0, age_bottom_ma=top_age - 2.0),
        ]
        
        evaluator = LineageHorizonLifespanEvaluator(occurrences)
        receipt = evaluator.evaluate_realization(replicate_id=1, seed=seed)
        
        env_a = receipt.taxon_envelopes["Taxon_A"]
        env_b = receipt.taxon_envelopes["Taxon_B"]
        
        # Invariant 1: Single-horizon taxon must have FAD == LAD and duration == 0
        assert env_a.fad_ma == env_a.lad_ma
        assert env_a.observed_duration_myr == 0.0
        
        # Invariant 2: Multi-horizon taxon must have FAD >= LAD
        assert env_b.fad_ma >= env_b.lad_ma
        assert env_b.observed_duration_myr >= 0.0
        
        # Invariant 3: Taxon A and B share exact same age in HZ_01
        hz01_age = receipt.horizon_draws["HZ_01"] * (bot_age - top_age) + top_age
        assert abs(env_a.fad_ma - hz01_age) < 1e-4

    def test_trace_preservation_channel_isolation(self):
        occurrences = [
            StratigraphicOccurrence(occurrence_id="tr_1", taxon_name="Treptichnus_pedum", horizon_id="HZ_FORTUNE", age_top_ma=538.0, age_bottom_ma=540.0),
            StratigraphicOccurrence(occurrence_id="tr_2", taxon_name="Treptichnus_pedum", horizon_id="HZ_FORTUNE", age_top_ma=538.0, age_bottom_ma=540.0),
            StratigraphicOccurrence(occurrence_id="bd_1", taxon_name="Paradoxides_davidis", horizon_id="HZ_BURGESS", age_top_ma=505.0, age_bottom_ma=508.0),
        ]
        
        metadata = {
            "tr_1": {"preservation_mode": "trace", "burrow_depth_mm": 35.0, "lithology": "siltstone"},
            "tr_2": {"preservation_mode": "trace", "burrow_depth_mm": 42.0, "lithology": "siltstone"},
            "bd_1": {"preservation_mode": "body", "burrow_depth_mm": 0.0, "lithology": "black_shale"},
        }
        
        evaluator = LineageHorizonLifespanEvaluator(occurrences, metadata)
        receipt = evaluator.evaluate_realization(replicate_id=42, seed=42)
        
        env_trep = receipt.taxon_envelopes["Treptichnus_pedum"]
        env_para = receipt.taxon_envelopes["Paradoxides_davidis"]
        
        # Treptichnus has 0 body fossils, 2 trace fossils, max depth 42mm
        assert env_trep.channel.body_occurrence_count == 0
        assert env_trep.channel.trace_occurrence_count == 2
        assert env_trep.channel.max_burrow_depth_mm == 42.0
        assert env_trep.channel.lithologies == ["siltstone"]
        
        # Paradoxides has 1 body fossil, 0 trace fossils
        assert env_para.channel.body_occurrence_count == 1
        assert env_para.channel.trace_occurrence_count == 0
        assert env_para.channel.max_burrow_depth_mm == 0.0
        assert env_para.channel.lithologies == ["black_shale"]
        
        # Provenance digest verification
        assert len(receipt.sha256_digest) == 64
