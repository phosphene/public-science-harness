"""
Characterization and invariant test suite for the empirical taphonomic data layer.
Asserts the exact empirical properties, singleton spectrum, collection clustering,
and guild silences documented in TAPHONOMIC_EVIDENTIARY_PROFILE.md.
"""

import sqlite3
from pathlib import Path
import pytest


@pytest.fixture
def db_conn():
    db_path = Path(__file__).parent.parent / "data/curated/cambrian_substrate.db"
    assert db_path.exists(), f"Database not found at {db_path}"
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


class TestTaphonomicDataProfile:
    """Verifies empirical invariants of the Cambrian occurrence dataset."""

    def test_total_scale_and_singleton_dominance(self, db_conn):
        c = db_conn.cursor()
        c.execute("SELECT count(*), count(DISTINCT taxon_name) FROM cambrian_occurrences;")
        total_occs, distinct_taxa = c.fetchone()
        
        assert total_occs == 1000
        assert distinct_taxa == 431
        
        # Singleton count (taxa with exactly 1 occurrence)
        c.execute("""
            SELECT count(*) FROM (
                SELECT taxon_name FROM cambrian_occurrences GROUP BY taxon_name HAVING count(*) = 1
            );
        """)
        singletons = c.fetchone()[0]
        assert singletons == 249
        
        # Assert singleton ratio exceeds 50%
        singleton_ratio = singletons / distinct_taxa
        assert 0.55 <= singleton_ratio <= 0.60, f"Unexpected singleton ratio: {singleton_ratio}"

    def test_spatial_collection_clustering(self, db_conn):
        c = db_conn.cursor()
        c.execute("SELECT count(DISTINCT pbdb_collection_no) FROM cambrian_occurrences;")
        n_collections = c.fetchone()[0]
        assert n_collections == 87
        
        # Verify dense Lagerstätte beds (collections with >= 20 taxa)
        c.execute("""
            SELECT pbdb_collection_no, count(DISTINCT taxon_name) as n_taxa
            FROM cambrian_occurrences
            GROUP BY pbdb_collection_no
            HAVING count(*) >= 20
            ORDER BY count(*) DESC;
        """)
        dense_colls = c.fetchall()
        assert len(dense_colls) >= 5, "Expected at least 5 dense collection horizons"
        # Top collection has >= 30 taxa co-occurring
        assert dense_colls[0][1] >= 30

    def test_guild_taphonomic_chiasm(self, db_conn):
        c = db_conn.cursor()
        c.execute("""
            SELECT functional_guild, count(*), count(DISTINCT taxon_name)
            FROM cambrian_occurrences
            GROUP BY functional_guild;
        """)
        guild_counts = {row[0]: (row[1], row[2]) for row in c.fetchall()}
        
        # Infaunal burrowers have only 5 occurrences across 4 taxa in body records
        infaunal_occs, infaunal_taxa = guild_counts["INFAUNAL_BURROWER"]
        assert infaunal_occs == 5
        assert infaunal_taxa == 4
        
        # Mobile predators dominate (> 60% of occurrences)
        pred_occs, pred_taxa = guild_counts["MOBILE_APEX_PREDATOR"]
        assert pred_occs >= 600
        assert pred_taxa >= 250
        
        # Taphonomic disparity ratio between predators and infauna exceeds 100:1
        disparity_ratio = pred_occs / infaunal_occs
        assert disparity_ratio > 100.0, f"Disparity ratio {disparity_ratio} below expected threshold"

    def test_stratigraphic_horizon_coverage(self, db_conn):
        c = db_conn.cursor()
        c.execute("SELECT horizon_id, stage_name, max_burrow_depth_mm FROM stratigraphic_horizons ORDER BY age_bottom_ma DESC;")
        horizons = c.fetchall()
        
        assert len(horizons) == 6
        # Ediacaran horizons have <= 2.0 mm burrow depth
        assert horizons[0][2] <= 2.0  # White Sea
        assert horizons[1][2] <= 2.0  # Fortune Head Ediacaran
        
        # Fortunian horizons jump to >= 35.0 mm
        assert horizons[2][2] >= 35.0 # Fortune Head Treptichnus
        assert horizons[3][2] >= 40.0 # Meishucun
