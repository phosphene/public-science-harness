# Data Engineering, Preservation, and SQL Standards

## 1. Purpose and Scope

This document defines the binding technical standards for acquiring, cleaning, storing, querying, and exchanging empirical datasets in `public-science-harness`. It operationalizes Section 2.1 (Data Engineering and Standards / Design for Falsifiability) of `OPERATING_GUIDELINES.md`.

Every dataset entering the harness must satisfy two requirements:
1. **Bit-level provenance:** Any cleaned table can be deterministically reconstructed from immutable upstream source files.
2. **Statistical readiness:** Schemas, units, keys, and missing-value semantics are explicit so downstream numerical models and statistical tests do not fail silently on malformed inputs.

---

## 2. Canonical Directory Layout

Every project or study module within the repository must separate raw inputs, curated analytical tables, schemas, SQL definitions, and external exchange bundles:

```text
study-module/
├── data/
│   ├── raw/         # Read-only upstream files + SHA256SUMS manifest
│   ├── curated/     # Canonical Parquet, DuckDB/SQLite, or clean CSV tables
│   └── interop/     # Ephemeral JSON/JSONL bundles for external team handoff
├── schemas/         # JSON Schema definitions and data dictionaries
├── sql/
│   ├── ddl/         # CREATE TABLE statements and integrity constraints
│   ├── views/       # Deterministic cleaning and cohort-filtering views
│   └── queries/     # Parameterized analytical and audit queries
└── pipelines/       # Deterministic ingestion, cleaning, and audit scripts
```

---

## 3. Storage Formats and Serialization Boundaries

Choosing the right format prevents silent type corruption, precision loss, and schema drift. The harness enforces strict boundaries across storage, configuration, and exchange layers.

### 3.1 Canonical Primary Storage Formats

All curated, analysis-ready datasets (`data/curated/`) must be stored in one of three formats:

1. **Apache Parquet (`.parquet`):** The default format for medium-to-large tabular datasets. Preserves strict column types (integers, IEEE-754 floats, booleans, timestamps), supports efficient columnar scans, and embeds schema metadata directly in the file.
2. **Embedded Relational Databases (`.duckdb` or `.sqlite`):** The default format for multi-table relational datasets requiring foreign-key integrity, indexed joins, or complex SQL view hierarchies.
3. **Strict Delimited Text (`.csv` or `.tsv`):** Permitted only for small, human-inspectable lookup tables or baseline reference tables (< 50 MB). Must conform strictly to RFC 4180, use UTF-8 encoding (ASCII-compatible wherever possible), use Unix line endings (`\n`), and pair with an explicit schema file in `schemas/`.

### 3.2 Strict JSON Policy

JSON (`.json`) and newline-delimited JSON (`.jsonl` / `.ndjson`) are **prohibited** for primary data storage and long-term archival of tabular records. JSON lacks native distinction between integers and floats, has no built-in date/timestamp type, omits relational constraints, and inflates storage overhead.

JSON is permitted **only** in the following four roles:
1. **Configuration Files:** Pipeline parameters, solver settings, and environment manifests.
2. **Schema Definitions:** Machine-readable table contracts (e.g., JSON Schema or Frictionless Data Table Schema) stored in `schemas/`.
3. **Wire Serialization:** Ephemeral payloads passed between local processes or APIs during runtime execution.
4. **External Interoperability Bundles (`data/interop/`):** Packaged exports generated specifically when collaborating with external teams whose tooling requires JSON ingestion.

### 3.3 Strict XML Prohibition

XML (`.xml`) is **strictly prohibited** across storage, configuration, schema definition, and internal serialization.

* Do not store datasets, configs, or metadata in XML.
* If an upstream public data source distributes records exclusively in XML, convert the raw XML file at the immediate ingestion boundary into a typed Parquet or SQL table, archive the untouched upstream file in `data/raw/`, and discard XML from all downstream stages.

---

## 4. Data Preservation and Provenance

### 4.1 Immutable Raw Snapshots

* Files placed in `data/raw/` are strictly read-only. Never edit, overwrite, or re-save raw files using spreadsheets or interactive editors.
* Every raw directory must maintain a `MANIFEST.json` (or `SHA256SUMS` file) recording:
  * Exact filename and SHA-256 cryptographic hash.
  * Upstream source URL, DOI, or accession identifier.
  * UTC retrieval timestamp (`YYYY-MM-DDTHH:MM:SSZ`).
  * License or terms of use.

### 4.2 Deterministic Curation Pipelines

* All transformations from `data/raw/` to `data/curated/` must execute via version-controlled scripts (`pipelines/`) or declarative SQL (`sql/`).
* Manual cleaning steps are forbidden. If a specific upstream row contains a known typographical error documented in an erratum, patch it programmatically via an explicit rule in the pipeline script with a comment citing the erratum.
* Any randomized operation (such as stratified train/test splitting or bootstrap resampling) must use an explicit, recorded PRNG seed.

---

## 5. Data Cleaning and Design for Falsifiability (DFF)

Before a curated dataset can support model standup or statistical inference, it must pass five hygiene rules:

### 5.1 Missingness, Nulls, and Sentinel Values

* **Eliminate Magic Sentinels:** Upstream datasets frequently encode missing values as `-999`, `9999`, `-1`, `0`, or strings like `"N/A"`, `"unk"`, or `"."`. All magic sentinel values must be stripped at ingestion and converted to true database `NULL` / `NA`.
* **Preserve Missingness Semantics:** Never collapse distinct failure modes into a single untyped blank if the distinction matters statistically. Where applicable, pair a nullable measurement column with a categorical status column (e.g., `measurement_status` in `{'observed', 'below_lod', 'censored', 'missing_at_random', 'instrument_fault'}`).
* **Zero vs. Null:** Explicitly verify whether `0` in an upstream table represents a true measured zero or an unrecorded entry.

### 5.2 Units, Types, and Temporal Standards

* **Explicit Units:** Every physical or quantitative column must document its unit (preferring SI units) in `schemas/`. Never rely on implicit units buried in paper prose. Convert mixed units (e.g., milligrams vs. grams) during ingestion so each column holds a single uniform scale.
* **Temporal Formatting:** Store all dates as ISO-8601 (`YYYY-MM-DD`) and all timestamps in UTC (`YYYY-MM-DDTHH:MM:SSZ`). Never store locale-dependent date strings (e.g., `03/04/2025`).
* **Identifier Types:** Store IDs (subject IDs, sample barcodes, FIPS codes, taxonomic IDs) as `TEXT` / `VARCHAR` rather than integers so leading zeros are never truncated and arithmetic is prevented.

### 5.3 Observational Units and Normalization

* **One Observational Unit per Table:** Do not mix subject-level baseline covariates and repeated time-series measurements in a single unnormalized flat table without explicit keys.
* **Normal Form Discipline:** Structure relational tables to at least Third Normal Form (3NF) during curation so entity attributes live in one canonical place. Denormalized analytical views may be derived downstream via SQL `VIEW`s for specific statistical models.
* **Explicit Keys:** Every table must define a natural or surrogate `PRIMARY KEY`, and every child table must enforce `FOREIGN KEY` relationships to its parent entity so orphaned records and accidental Cartesian joins are impossible.

### 5.4 Precursor Reconciliation Audits

Every curation pipeline must conclude with an automated reconciliation check comparing `data/curated/` against the published figures and summary tables of the source paper:

* Verify exact row counts ($N$), group sizes ($n_k$), and missing-data counts.
* Recompute baseline means, medians, standard deviations, and proportions, logging any discrepancy beyond floating-point tolerance.
* Any unexplained discrepancy between the released raw data and the published paper must be documented in an audit note before statistical modeling begins.

---

## 6. SQL Standards and Relational Hygiene

SQL is the primary language for defining relational schemas, expressing deterministic data transformations, and executing cohort queries.

### 6.1 Engine and Dialect Portability

* Write standard ANSI SQL compatible with **DuckDB** and **SQLite** for local, single-node reproducible execution, and **PostgreSQL** for shared multi-user stores.
* Avoid vendor-specific syntactic shortcuts unless isolated inside an engine-specific adapter script.

### 6.2 Schema-First DDL and Integrity Constraints

Never rely on dynamic type inference (`CREATE TABLE AS SELECT` from untyped CSVs) for canonical curated tables. Define schemas explicitly using Data Definition Language (`sql/ddl/`) with strict types and `CHECK` constraints:

```sql
CREATE TABLE observations (
    observation_id        TEXT PRIMARY KEY,
    subject_id            TEXT NOT NULL,
    sampled_at_utc        TIMESTAMP NOT NULL,
    concentration_umol_l  DOUBLE PRECISION,
    status_flag           TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id),
    CHECK (concentration_umol_l IS NULL OR concentration_umol_l >= 0.0),
    CHECK (status_flag IN ('observed', 'below_lod', 'censored', 'missing'))
);
```

### 6.3 Query Structure and Readability

* **CTEs over Nested Subqueries:** Structure multi-step transformations using sequential Common Table Expressions (`WITH` clauses) where each CTE performs one logical step (filtering, unit standardization, aggregation, joining).
* **Explicit Join Syntax:** Always use explicit `INNER JOIN`, `LEFT JOIN`, or `CROSS JOIN` with explicit `ON` predicates. Implicit comma-separated joins (`FROM a, b WHERE a.id = b.id`) are forbidden.
* **Mandatory Table Qualification:** Prefix every column reference with a clear table alias in multi-table queries (`obs.subject_id`, never bare `subject_id`).
* **Deterministic Ordering:** Any query whose output feeds row-order-dependent downstream code, window functions, or file exports must specify a deterministic `ORDER BY` clause including a unique tie-breaker key.
* **Safe Division and Null Handling:** Guard denominators with `NULLIF(denominator, 0)` and handle null propagation explicitly with `COALESCE` rather than assuming default zero behavior.

Example canonical query pattern (`sql/views/v_subject_summary.sql`):

```sql
WITH valid_observations AS (
    SELECT
        obs.subject_id,
        obs.sampled_at_utc,
        obs.concentration_umol_l
    FROM observations AS obs
    WHERE obs.status_flag = 'observed'
      AND obs.concentration_umol_l IS NOT NULL
),
subject_aggregates AS (
    SELECT
        vo.subject_id,
        COUNT(*) AS n_valid_samples,
        AVG(vo.concentration_umol_l) AS mean_concentration_umol_l,
        MIN(vo.sampled_at_utc) AS first_sample_utc,
        MAX(vo.sampled_at_utc) AS last_sample_utc
    FROM valid_observations AS vo
    GROUP BY vo.subject_id
)
SELECT
    subj.subject_id,
    subj.cohort_group,
    COALESCE(agg.n_valid_samples, 0) AS n_valid_samples,
    agg.mean_concentration_umol_l,
    agg.first_sample_utc,
    agg.last_sample_utc
FROM subjects AS subj
LEFT JOIN subject_aggregates AS agg
    ON subj.subject_id = agg.subject_id
ORDER BY subj.subject_id ASC;
```

### 6.4 Separation of SQL and Host Languages

* Store non-trivial SQL statements in standalone `.sql` files under `sql/` rather than embedding multi-line query strings inside Python or R scripts.
* Never build SQL queries via string concatenation or f-strings. Pass runtime filter thresholds strictly through bound query parameters (`?` or `$1`).

---

## 7. External Interoperability Bundles (`data/interop/`)

When collaborating with external teams or external services that require JSON payloads, export ephemeral interoperability bundles derived from `data/curated/`:

1. **Derive, Do Not Author:** Generate JSON (`bundle.json`) or newline-delimited JSON (`records.jsonl`) strictly by exporting verified Parquet or SQL tables. Never maintain hand-edited JSON data files.
2. **Bundle Packaging Requirements:** Every export directory in `data/interop/` must contain:
   * `records.jsonl` (or `bundle.json`): The serialized records with ISO-8601 timestamps and explicit `null` values.
   * `schema.json`: A valid JSON Schema describing every field, type, unit, and allowed enum value.
   * `METADATA.json`: Provenance metadata linking the export back to the exact `data/curated/` SHA-256 checksums, SQL view version, and git commit hash that produced it.
3. **Treat as Ephemeral Artifacts:** Do not commit large generated `data/interop/` payloads to git unless required for small integration fixtures; regenerate them deterministically from the canonical storage layer on demand.
