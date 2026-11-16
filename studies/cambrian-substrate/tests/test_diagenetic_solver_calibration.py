"""
Calibrated integration tests for the DiageneticTieringSolver.
Calibrates model outputs against the curated stratigraphic horizons database:
- Terminal Ediacaran (Radulichnus / Kimberella, Z_max = 1.5 - 2.0 mm)
- Fortunian Agronomic Revolution (Treptichnus pedum, Z_max = 35.0 - 45.0 mm)
- Stage 3-5 Deep Tiering (Cruziana / Nektonic, Z_max = 80.0 - 120.0 mm)
"""

import sys
import sqlite3
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from diagenetic_tiering import DiageneticTieringSolver


@pytest.fixture
def db_horizons():
    db_path = Path(__file__).parent.parent / "data/curated/cambrian_substrate.db"
    assert db_path.exists(), f"Database not found at {db_path}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT horizon_id, stage_name, max_burrow_depth_mm, ichnotaxon
        FROM stratigraphic_horizons
        ORDER BY age_bottom_ma DESC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


class TestDiageneticSolverStratigraphicCalibration:
    """Verifies physical solver calibration across the Ediacaran-Cambrian transition."""

    def test_stratigraphic_tiering_gradient_solver(self, db_horizons):
        solver = DiageneticTieringSolver(
            domain_depth_mm=100.0,
            n_points=101,
            molecular_diffusion_o2=20.0,
            surface_o2_umol=250.0,
            surface_c_org=10.0,
            volumetric_o2_consumption=30.0,
        )

        results = {}
        for row in db_horizons:
            hid, stage, depth_mm, ichnotaxon = row
            res = solver.solve_steady_state(z_max_mm=depth_mm, biodiffusion_db0=60.0)
            assert res.solver_success, f"Solver failed for horizon {hid}"
            results[hid] = {
                "stage": stage,
                "z_max": depth_mm,
                "o2_pen": res.o2_penetration_depth_mm,
                "niche_cap": res.aerobic_niche_capacity,
            }

        # Calibration assertions against real stratigraphy:
        # 1. Ediacaran baseline (Z_max ~ 1.5-2.0mm) yields shallow, cramped oxygen penetration
        ed_pen = results["HZ_FORTUNE_HEAD_ED_01"]["o2_pen"]
        ed_cap = results["HZ_FORTUNE_HEAD_ED_01"]["niche_cap"]
        assert ed_pen <= 20.0, f"Ediacaran O2 penetration too deep: {ed_pen}mm"

        # 2. Fortunian Agronomic boundary (Treptichnus pedum, Z_max = 35.0mm) breaks the barrier
        cb1_pen = results["HZ_FORTUNE_HEAD_CB_01"]["o2_pen"]
        cb1_cap = results["HZ_FORTUNE_HEAD_CB_01"]["niche_cap"]
        assert cb1_pen > ed_pen * 1.5, f"Fortunian failed to deepen O2 penetration: cb1={cb1_pen}, ed={ed_pen}"
        assert cb1_cap > ed_cap * 1.4, f"Fortunian failed to expand aerobic niche capacity: cb1={cb1_cap}, ed={ed_cap}"

        # 3. Middle Cambrian climax (Burgess / Nektonic, Z_max >= 80mm) ventilates deep sediment
        cb4_pen = results["HZ_BURGESS_SHALE_CB_04"]["o2_pen"]
        cb4_cap = results["HZ_BURGESS_SHALE_CB_04"]["niche_cap"]
        assert cb4_pen >= 60.0, f"Burgess sediment under-ventilated: {cb4_pen}mm"
        assert cb4_cap > cb1_cap * 1.3, "Deep tiering did not increase niche capacity over Fortunian"
