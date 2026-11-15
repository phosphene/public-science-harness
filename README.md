# `public-science-harness`

**Active Engineering and Statistical Workbench for Public Science**

`public-science-harness` is the platform engineering and statistical workbench of Phosphene. Working alongside `monograph-review`, this repository shifts the platform team's focus from post-hoc manuscript auditing to building the empirical substrates, instrumented models, and calibration tests required for reproducible normal science.

---

## Mandate & Operating Scope

The platform team does not gate researchers or police their creative intuitions. Instead, we provide production-quality technical execution across five core areas:

1. **Data Engineering & Dataset Standards:** Curating reproducible, schema-validated empirical datasets before model standup (*Data First / Design for Falsifiability*).
2. **Model Implementation & Instrumentation:** Standing up precursor models on their native benchmark terrain and exposing solver convergence, likelihood surfaces, and internal state diagnostics.
3. **Empirical Calibration & Testing:** Running empirical tests with explicit calibration benchmarks and quantifying error envelopes and breakdown regimes.
4. **Claim Scoping:** Mapping exact parameter identification boundaries and explicitly disclosing analogical transfers as speculative until calibrated.
5. **Reproducible Baseline Reporting:** Publishing transparent reports with pinned data versions, software environments, and verifiable test artifacts.

---

## Canonical Repository Layout

Every study module within the harness separates data, schemas, SQL definitions, pipelines, and tests:

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
├── pipelines/       # Deterministic ingestion, cleaning, and audit scripts
├── models/          # Standup implementations of precursor models & solvers
└── tests/           # Reconciliation audits and property-based regression suites
```

---

## Documentation & Standards

- **[Operating Guidelines](docs/OPERATING_GUIDELINES.md):** The five operational mandates, standard harness workflow, and division of responsibility between research and platform.
- **[Data Engineering, Preservation, and SQL Standards](docs/DATA_STANDARDS.md):** Bit-level provenance, canonical directory layout, primary storage formats (Parquet/DuckDB/SQLite vs. strict JSON/XML rules), DFF data hygiene, and ANSI SQL standards.

---

## Active Studies

- **`cambrian-substrate/` (Paper 01):** Empirical data curation and baseline replication for trace fossil stratigraphy (ichnology), diversity-dependence slopes across Cambrian functional guilds, and substrate shift dynamics across the Ediacaran–Cambrian transition.

---

## License

BSD-3-Clause © 2026 Phosphene / Independent Media Institute
