-- DDL: Epistemic Data Annotations & Provenance Registry
-- Dialect: ANSI SQL (DuckDB / SQLite / PostgreSQL compatible)
-- Conforms to docs/TRANSFORMS_PROVENANCE_AND_ANNOTATION.md Section 5

CREATE TABLE IF NOT EXISTS epistemic_data_annotations (
    annotation_id TEXT PRIMARY KEY,
    timestamp_utc TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    actor_role TEXT NOT NULL,
    target_entity_type TEXT NOT NULL,
    target_selector TEXT NOT NULL,
    judgment_type TEXT NOT NULL,
    epistemic_warrant_doi TEXT,
    epistemic_warrant_citation TEXT,
    rationale TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    CHECK (target_entity_type IN ('TABLE', 'COLUMN', 'RECORD', 'VALUE')),
    CHECK (judgment_type IN ('DISCLOSURE', 'CALIBRATION_OVERRIDE', 'RECLASSIFICATION', 'FLAG_EXCLUSION'))
);

CREATE TABLE IF NOT EXISTS dataset_provenance_receipts (
    receipt_id TEXT PRIMARY KEY,
    pipeline_id TEXT NOT NULL,
    git_commit_sha TEXT NOT NULL,
    executed_at_utc TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    transforms_applied_json TEXT NOT NULL,
    input_artifacts_json TEXT NOT NULL,
    output_artifacts_json TEXT NOT NULL
);
