-- DDL: Cambrian Marine Functional Guild Diversity
-- Dialect: ANSI SQL (DuckDB / SQLite / PostgreSQL compatible)
-- Conforms to docs/DATA_STANDARDS.md Section 6.2

CREATE TABLE IF NOT EXISTS cambrian_occurrences (
    occurrence_id TEXT PRIMARY KEY,
    taxon_name TEXT NOT NULL,
    taxon_rank TEXT NOT NULL,
    phylum TEXT,
    class TEXT,
    order_name TEXT,
    family TEXT,
    genus TEXT,
    functional_guild TEXT NOT NULL,
    early_interval TEXT NOT NULL,
    late_interval TEXT,
    max_ma DOUBLE PRECISION NOT NULL,
    min_ma DOUBLE PRECISION NOT NULL,
    pbdb_collection_no TEXT NOT NULL,
    reference_no TEXT NOT NULL,
    CHECK (max_ma >= min_ma),
    CHECK (functional_guild IN ('SEDENTARY_FILTER_FEEDER', 'INFAUNAL_BURROWER', 'MOBILE_APEX_PREDATOR', 'OTHER_UNCLASSIFIED'))
);

CREATE TABLE IF NOT EXISTS cambrian_guild_diversity_summary (
    stage_id TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    mean_age_ma DOUBLE PRECISION NOT NULL,
    functional_guild TEXT NOT NULL,
    taxonomic_richness INTEGER NOT NULL,
    total_occurrences INTEGER NOT NULL,
    PRIMARY KEY (stage_id, functional_guild),
    CHECK (taxonomic_richness >= 0),
    CHECK (total_occurrences >= taxonomic_richness)
);
