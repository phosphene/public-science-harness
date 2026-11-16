"""
Unit and invariant tests for the taphonomically compensated diversity-dependence estimator.
Verifies epistemic blocking on unweighted infaunal body counts, tiering depth scaling,
and skeletal representative passing.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from diversity_dependence_estimator import (
    DiversityDependenceEstimator,
    EpistemicWarrantViolation,
)


@pytest.fixture
def estimator():
    db_path = Path(__file__).parent.parent / "data/curated/cambrian_substrate.db"
    return DiversityDependenceEstimator(db_path=db_path)


class TestDiversityDependenceEstimator:
    """Verifies epistemic constraints and tiering compensation invariants."""

    def test_unweighted_infaunal_fitting_is_strictly_forbidden(self, estimator):
        with pytest.raises(EpistemicWarrantViolation) as excinfo:
            estimator.fit_diversity_dependence("INFAUNAL_BURROWER", z_max_mm=None)
        
        assert "Unweighted body fossil diversity-dependence fitting forbidden" in str(excinfo.value)
        assert "Brasier, M.D. et al. (1994)" in str(excinfo.value)

    def test_tiering_depth_compensation_expands_capacity(self, estimator):
        # Fortunian tiering depth Z_max = 45.0 mm
        fit = estimator.fit_diversity_dependence("INFAUNAL_BURROWER", z_max_mm=45.0)

        assert fit.compensation_applied is True
        assert fit.raw_body_taxa_count == 4
        # N_eff must expand significantly (> 20.0)
        assert fit.effective_capacity_n_eff > 20.0
        # Gl slope must be positive/stabilizing under expanded ecological substrate
        assert fit.gl_speciation_slope > 0.0
        assert len(fit.sha256_digest) == 64

    def test_skeletal_guild_permits_direct_body_fitting(self, estimator):
        fit = estimator.fit_diversity_dependence("SEDENTARY_FILTER_FEEDER")

        assert fit.compensation_applied is False
        assert fit.raw_body_taxa_count == 81
        assert fit.effective_capacity_n_eff == 81.0
        assert fit.gl_speciation_slope < 0.0  # Classical negative DD niche saturation
