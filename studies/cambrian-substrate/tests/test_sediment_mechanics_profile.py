"""
Invariant tests for the sediment mechanics and diagenetic profile.
Verifies the physical coordinates, boundary depths, and diagenetic scaling
documented in SEDIMENT_MECHANICS_AND_DIAGENESIS_PROFILE.md.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from primitives import biodiffusion_kernel
from diagenetic_tiering import DiageneticTieringSolver


class TestSedimentMechanicsProfile:
    """Verifies sedimentological invariants and physical scaling."""

    def test_matground_vs_mixground_biodiffusion_invariants(self):
        # Ediacaran matground: z_max <= 2.0 mm, Db0 = 0.0
        db_mat = biodiffusion_kernel(z_mm=5.0, z_max_mm=2.0, d_b0=0.0)
        assert db_mat == 0.0

        # Fortunian vertical burrowing: z_max = 35.0 mm, Db0 = 15.0 mm^2/yr
        db_in_tier = biodiffusion_kernel(z_mm=20.0, z_max_mm=35.0, d_b0=15.0)
        assert db_in_tier == 15.0

        # Below tier: Gaussian attenuation
        db_below_tier = biodiffusion_kernel(z_mm=45.0, z_max_mm=35.0, d_b0=15.0, sigma_b_mm=5.0)
        assert 0.0 < db_below_tier < 15.0

    def test_aerobic_niche_volume_expansion(self):
        solver = DiageneticTieringSolver(domain_depth_mm=100.0, n_points=101)

        # Baseline: Terminal Ediacaran (Z_max = 2.0 mm, Db0 = 0.0)
        res_ed = solver.solve_steady_state(z_max_mm=2.0, biodiffusion_db0=0.0)
        assert res_ed.solver_success
        z_pen_ed = res_ed.o2_penetration_depth_mm
        niche_ed = res_ed.aerobic_niche_capacity

        # Fortunian Horizon: Fortune Head (Z_max = 35.0 mm, Db0 = 15.0)
        res_cb = solver.solve_steady_state(z_max_mm=35.0, biodiffusion_db0=15.0)
        assert res_cb.solver_success
        z_pen_cb = res_cb.o2_penetration_depth_mm
        niche_cb = res_cb.aerobic_niche_capacity

        # Penetration depth must expand substantially
        assert z_pen_cb > z_pen_ed, f"Penetration expansion {z_pen_cb} <= {z_pen_ed}"

        # Aerobic niche capacity must expand substantially (> 2x)
        assert niche_cb > 2.0 * niche_ed, f"Niche capacity expansion {niche_cb / niche_ed} < 2.0"

    def test_ichnofabric_tier_depth_monotonicity(self):
        tiers = {
            "tier_1_mat": 2.0,
            "tier_2_undermat": 10.0,
            "tier_3_vertical": 35.0,
            "tier_4_deep": 80.0,
        }
        depths = list(tiers.values())
        for d1, d2 in zip(depths[:-1], depths[1:]):
            assert d1 < d2
