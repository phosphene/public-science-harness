-- View 3: Calibrated Guild Diversity and Taphonomic Annotations
-- Joins empirical guild summaries with explicit taphonomic calibration tiers and annotations
-- Conforms to docs/TRANSFORMS_PROVENANCE_AND_ANNOTATION.md Section 6

CREATE VIEW IF NOT EXISTS v_calibrated_guild_diversity AS
WITH base_guilds AS (
    SELECT
        g.functional_guild,
        g.distinct_taxa AS raw_distinct_taxa,
        g.total_occurrences AS raw_occurrences,
        g.sampling_ratio,
        g.mean_occurrence_age_ma,
        CASE
            WHEN g.functional_guild = 'INFAUNAL_BURROWER' THEN 'ICHNO_INFAUNAL_TIER'
            WHEN g.functional_guild = 'SEDENTARY_FILTER_FEEDER' THEN 'SKELETAL_SHELL_BED'
            WHEN g.functional_guild = 'MOBILE_APEX_PREDATOR' THEN 'CUTICULAR_LAGERSTATTEN'
            ELSE 'UNCLASSIFIED'
        END AS preservation_mode_tier,
        CASE
            WHEN g.functional_guild = 'INFAUNAL_BURROWER' THEN
                (SELECT MAX(max_burrow_depth_mm) FROM stratigraphic_horizons WHERE stage_name = 'Fortunian')
            ELSE 0.0
        END AS fortunian_tiering_depth_mm,
        CASE
            WHEN g.functional_guild = 'INFAUNAL_BURROWER' THEN
                (SELECT MAX(max_burrow_depth_mm) FROM stratigraphic_horizons WHERE stage_name LIKE '%Wuliuan%')
            ELSE 0.0
        END AS wuliuan_tiering_depth_mm
    FROM v_guild_richness_summary g
)
SELECT
    b.functional_guild,
    b.raw_distinct_taxa,
    b.raw_occurrences,
    b.sampling_ratio,
    b.preservation_mode_tier,
    b.fortunian_tiering_depth_mm,
    b.wuliuan_tiering_depth_mm,
    CASE
        WHEN b.functional_guild = 'INFAUNAL_BURROWER' THEN 'BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED'
        ELSE 'OBSERVED_BODY_COUNT_REPRESENTATIVE'
    END AS calibration_status,
    a.annotation_id,
    a.judgment_type,
    a.epistemic_warrant_citation,
    a.recommended_action
FROM base_guilds b
LEFT JOIN epistemic_data_annotations a
    ON a.target_selector LIKE '%' || b.functional_guild || '%';
