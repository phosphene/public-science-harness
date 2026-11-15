-- DDL: Stratigraphic Horizons & Ichnofacies Matrix
-- Dialect: ANSI SQL (DuckDB / SQLite / PostgreSQL compatible)
-- Conforms to docs/DATA_STANDARDS.md Section 6.2

CREATE TABLE IF NOT EXISTS stratigraphic_horizons (
    horizon_id TEXT PRIMARY KEY,
    section_name TEXT NOT NULL,
    country TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    age_top_ma DOUBLE PRECISION NOT NULL,
    age_bottom_ma DOUBLE PRECISION NOT NULL,
    ichnotaxon TEXT NOT NULL,
    substrate_penetration_dimension TEXT NOT NULL,
    max_burrow_depth_mm DOUBLE PRECISION NOT NULL,
    biomineralized_tissue_present BOOLEAN NOT NULL,
    mineralogy_type TEXT NOT NULL,
    primary_reference_doi TEXT NOT NULL,
    CHECK (age_bottom_ma >= age_top_ma),
    CHECK (age_top_ma >= 480.0 AND age_bottom_ma <= 600.0),
    CHECK (max_burrow_depth_mm >= 0.0),
    CHECK (substrate_penetration_dimension IN ('2D_SURFACE_MAT', '2.5D_MICROBIAL_UNDERMAT', '3D_VERTICAL_INFAUNAL', '3D_NEKTONIC')),
    CHECK (mineralogy_type IN ('NONE', 'CARBONATE', 'PHOSPHATIC', 'AGGLUTINATED', 'SILICEOUS'))
);
