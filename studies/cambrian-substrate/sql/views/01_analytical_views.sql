-- SQL Views: Curated Analytical Views for Cambrian Substrate Study
-- Dialect: ANSI SQL (DuckDB / SQLite / PostgreSQL compatible)
-- Conforms to docs/DATA_STANDARDS.md Section 6.3

-- View 1: Chronological Stratigraphic Progression
-- Ranks horizons chronologically and flags physical substrate ingress depth
CREATE VIEW IF NOT EXISTS v_chronological_horizons AS
SELECT
    horizon_id,
    section_name,
    country,
    stage_name,
    age_bottom_ma,
    age_top_ma,
    ROUND((age_bottom_ma + age_top_ma) / 2.0, 2) AS mean_age_ma,
    ichnotaxon,
    substrate_penetration_dimension,
    max_burrow_depth_mm,
    biomineralized_tissue_present,
    mineralogy_type,
    primary_reference_doi
FROM stratigraphic_horizons
ORDER BY age_bottom_ma DESC, age_top_ma DESC;

-- View 2: Guild Richness and Sampling Summary
-- Computes taxonomic richness and occurrence volume per functional guild
CREATE VIEW IF NOT EXISTS v_guild_richness_summary AS
WITH guild_aggregates AS (
    SELECT
        functional_guild,
        COUNT(DISTINCT taxon_name) AS distinct_taxa,
        COUNT(DISTINCT genus) AS distinct_genera,
        COUNT(*) AS total_occurrences,
        ROUND(AVG((max_ma + min_ma) / 2.0), 2) AS mean_occurrence_age_ma,
        MIN(min_ma) AS youngest_age_ma,
        MAX(max_ma) AS oldest_age_ma
    FROM cambrian_occurrences
    WHERE functional_guild != 'OTHER_UNCLASSIFIED'
    GROUP BY functional_guild
)
SELECT
    functional_guild,
    distinct_taxa,
    distinct_genera,
    total_occurrences,
    ROUND(CAST(total_occurrences AS DOUBLE PRECISION) / NULLIF(distinct_taxa, 0), 2) AS sampling_ratio,
    mean_occurrence_age_ma,
    oldest_age_ma,
    youngest_age_ma
FROM guild_aggregates
ORDER BY distinct_taxa DESC;
