"""
Property and invariant tests for the canonical conditioned birth-death likelihood evaluator.
Verifies Keiding conditioning normalizers, occurrence log-likelihoods, boundary violations,
and parameter monotonicity.
"""

import sys
from pathlib import Path
import pytest
from hypothesis import given, strategies as st

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from horizon_coupled_resampler import StratigraphicOccurrence
from lineage_horizon_evaluator import LineageHorizonLifespanEvaluator
from conditioned_likelihood_evaluator import (
    BirthDeathParameters,
    ConditionedBirthDeathLikelihoodEvaluator,
)


@pytest.fixture
def mock_cohort_receipt():
    """Generates a small deterministic cohort receipt for testing."""
    occs = [
        StratigraphicOccurrence(occurrence_id="occ_1", taxon_name="Kimberella", horizon_id="HZ_ED", age_top_ma=550.0, age_bottom_ma=555.0),
        StratigraphicOccurrence(occurrence_id="occ_2", taxon_name="Kimberella", horizon_id="HZ_ED", age_top_ma=550.0, age_bottom_ma=555.0),
        StratigraphicOccurrence(occurrence_id="occ_3", taxon_name="Dickinsonia", horizon_id="HZ_ED", age_top_ma=550.0, age_bottom_ma=555.0),
        StratigraphicOccurrence(occurrence_id="occ_4", taxon_name="Cloudina", horizon_id="HZ_CB", age_top_ma=540.0, age_bottom_ma=543.0),
    ]
    evaluator = LineageHorizonLifespanEvaluator(occs)
    return evaluator.evaluate_realization(replicate_id=1, seed=42)


class TestConditionedLikelihoodEvaluator:
    """Verifies likelihood evaluation invariants."""

    def test_valid_likelihood_evaluation_and_components(self, mock_cohort_receipt):
        params = BirthDeathParameters(
            lambda_0=0.2,
            mu_0=0.15,
            q_0=1.2,
        )

        # Candidate spans consistent with FAD/LAD
        k_env = mock_cohort_receipt.taxon_envelopes["Kimberella"]
        d_env = mock_cohort_receipt.taxon_envelopes["Dickinsonia"]
        c_env = mock_cohort_receipt.taxon_envelopes["Cloudina"]

        latent_spans = {
            "Kimberella": (k_env.fad_ma + 2.0, k_env.lad_ma - 1.0),
            "Dickinsonia": (d_env.fad_ma + 1.5, d_env.lad_ma - 0.5),
            "Cloudina": (c_env.fad_ma + 0.5, c_env.lad_ma - 0.2),
        }

        receipt = ConditionedBirthDeathLikelihoodEvaluator.evaluate_cohort_likelihood(
            mock_cohort_receipt, latent_spans, params
        )

        assert receipt.total_log_likelihood < 0.0
        assert math.isfinite(receipt.total_log_likelihood)
        assert receipt.n_taxa == 3
        assert len(receipt.sha256_digest) == 64

        # Check individual breakdown math: log L = log L_occ + log L_surv - log P_keid
        for taxon, bd in receipt.taxon_breakdowns.items():
            expected = bd.loglik_occurrences + bd.loglik_survival - bd.log_keiding_conditioning
            assert pytest.approx(bd.total_conditioned_loglik, rel=1e-5) == expected

    def test_boundary_violation_returns_negative_infinity(self, mock_cohort_receipt):
        params = BirthDeathParameters(lambda_0=0.2, mu_0=0.15, q_0=1.2)
        k_env = mock_cohort_receipt.taxon_envelopes["Kimberella"]

        # Latent origination younger than observed FAD (impossible)
        invalid_spans = {
            "Kimberella": (k_env.fad_ma - 1.0, k_env.lad_ma - 2.0),
            "Dickinsonia": (560.0, 545.0),
            "Cloudina": (545.0, 538.0),
        }

        receipt = ConditionedBirthDeathLikelihoodEvaluator.evaluate_cohort_likelihood(
            mock_cohort_receipt, invalid_spans, params
        )

        assert receipt.total_log_likelihood == -float("inf")

    @given(
        q1=st.floats(min_value=0.1, max_value=2.0),
        q2=st.floats(min_value=2.1, max_value=5.0),
    )
    def test_keiding_conditioning_monotonicity_in_q(self, q1, q2):
        from birth_death_primitives import keiding_sampling_probability
        s = 10.0
        e = 5.0
        p1 = keiding_sampling_probability(s, e, q1)
        p2 = keiding_sampling_probability(s, e, q2)
        assert 0.0 < p1 < p2 <= 1.0


import math
