# Study Module: Cambrian Substrate Shift & Diversity-Dependence (Paper 01)

## 1. Study Overview and Empirical Scope

This study module operationalizes the empirical substrate and baseline statistical replications for **Paper 01** (*Substrate Shift Foundations in Early Animal Evolution: Behavioral Decoupling, Ichnology, and Developmental Consolidation Across the Ediacaran–Cambrian Transition*).

In accordance with `docs/OPERATING_GUIDELINES.md` and `docs/DATA_STANDARDS.md`, this module implements:
1. **Empirical Ichnological Stratigraphy:** An audited, chronological occurrence matrix of trace fossils vs. biomineralized skeletal hardware across the Ediacaran–Cambrian boundary (555–515 Ma).
2. **Diversity-Dependence Replication:** Empirical calibration and Bayesian/Maximum Likelihood estimation of macroecological diversity-dependence slopes ($Gl$) across distinct functional marine guilds (sedentary filter feeders, infaunal burrowers, mobile apex predators).
3. **Reconciliation Audits:** Bit-level reconciliation checks against published Paleobiology Database (PBDB) occurrence records and canonical stratigraphic literature.

---

## 2. Directory Layout

```text
studies/cambrian-substrate/
├── data/
│   ├── raw/         # Upstream occurrence dumps, PBDB exports, and SHA256SUMS
│   ├── curated/     # Typed Parquet tables and DuckDB relational database
│   └── interop/     # Derived JSON-Schema-validated bundles for external handoff
├── schemas/         # Frictionless / JSON Schema definitions for ichnofossils & guild diversity
├── sql/
│   ├── ddl/         # DDL schemas with strict CHECK constraints and foreign keys
│   ├── views/       # SQL cohort views filtering stratigraphic stages and guilds
│   └── queries/     # Diversity-dependence and taxonomic rate queries
├── pipelines/       # Ingestion and audit scripts (raw -> curated Parquet/DuckDB)
├── models/          # Native diversity-dependence models (PyRate / diversitree standup)
└── tests/           # Reconciliation tests and property invariants
```

---

## 3. Data Intake Plan & Upstream Sources

### 3.1 Dataset A: Ediacaran–Cambrian Stratigraphic Horizon & Ichnofacies Matrix
* **Primary Sources:**
  - Narbonne et al. (1987) & Brasier et al. (1994): Fortune Head, Newfoundland GSSP boundary section (*Treptichnus pedum* datum).
  - Ivantsov (2013) & Gehling et al. (2014): Terminal Ediacaran White Sea / South Australia *Kimberella* and *Radulichnus* occurrences.
  - Kouchinsky et al. (2012): Chronology of early Cambrian Small Shelly Fossil (SSF) biomineralization.
  - Buatois & Mángano (2011): Ichnological depth tiering and agronomic revolution penetration metrics.

### 3.2 Dataset B: Cambrian Marine Functional Guild Diversity Time-Series
* **Primary Source:**
  - Paleobiology Database (PBDB) API occurrence records for Cambrian Stages (Fortunian through Drumian / Stage 5).
  - Categorization into 3 canonical functional guilds:
    1. *Sedentary Epibenthic Filter Feeders* (Porifera, stem Brachiopoda, Eocrinoidea)
    2. *Infaunal Bioturbators / Deposit Feeders* (Priapulida, early Polychaeta, vermiform burrows)
    3. *Mobile Pelagic / Epibenthic Predators* (Radiodonta, stem Euarthropoda)
* **Target Analytical Output:**
  - Pinned table: `cambrian_guild_diversity.parquet`
  - Replicated diversity-dependence parameter vector: $[Gl_{\text{sedentary}}, Gl_{\text{burrower}}, Gl_{\text{predator}}]$ with 95% credible intervals.
