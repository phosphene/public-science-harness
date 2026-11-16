# Comprehensive Data Inventory & Evidentiary Landscape: What We Have, What Has Been Analyzed, and Where the Raw Data Sits

**Document Coordinate:** `studies/cambrian-substrate/data/DATA_INVENTORY_AND_EVIDENTIARY_LANDSCAPE.md`  
**Repository:** `phosphene/public-science-harness` (with links to `work/marsyas6/papers/valence-ingress/`)  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Evidentiary Ledger  
**Date:** 2026-11-16  

---

## 1. Executive Evidentiary Map

To maintain complete descriptive discipline and prevent cognitive conflation, our evidentiary assets are divided strictly into three tiers:
1. **Raw Observational Data:** Unmanipulated fossil occurrences, primary GSSP/Lagerstätte stratigraphic sections, and raw author packages.
2. **Curated & Relational Data:** SQLite databases, schema-enforced tables with foreign keys and check constraints, and immutable cryptographic receipts.
3. **Prior Analyses & Derivative Packages:** MCMC logs, R/Python re-analyses, literate profiles, and property-tested test suites.

```
                              EVIDENTIARY TOPOLOGY
                              
   RAW OBSERVATIONS                  CURATED HARNESS                  DERIVATIVE ANALYSES
┌────────────────────────┐      ┌────────────────────────┐      ┌─────────────────────────┐
│ • PBDB JSON (1,000 r)  │ ───► │ • SQLite DB (260 KB)   │ ───► │ • Taphonomic Profile    │
│ • Strat. CSV (6 GSSP)  │      │   - cambrian_occs      │      │ • Sediment Mechanics    │
│ • Van Holstein Figshare│      │   - strat_horizons     │      │ • Van Holstein Re-eval  │
│   (3.4 MB archive)     │      │ • Provenance Receipt   │      │ • Cichlid DD Contrast   │
│ • Acquired PDFs (12+)  │      │   (SHA-256 sealed)     │      │ • BDD & Pytest Suites   │
└────────────────────────┘      └────────────────────────┘      └─────────────────────────┘
```

---

## 2. Inventory of Raw Data Assets

### A. Cambrian Fossil Occurrences (`studies/cambrian-substrate/data/raw/`)
- **File:** `pbdb_cambrian_metazoa_raw.json` (376 KB)
- **Origin:** Curated extract from the Paleobiology Database (PBDB) Metazoan API covering the Ediacaran–Cambrian transition (558.0 to 486.85 Ma).
- **Scale:** **1,000 raw occurrence records**.
- **Fields Preserved:** Taxon name, taxonomic rank (order, family, genus), phylum, class, early interval, late interval, maximum geological age (`max_ma`), minimum geological age (`min_ma`), collection number (`pbdb_collection_no`), reference citation number (`reference_no`).
- **Status:** Unmanipulated, append-only JSON array.

### B. Stratigraphic Horizons & GSSP Sections (`studies/cambrian-substrate/data/raw/`)
- **File:** `stratigraphic_horizons_raw.csv` (1.3 KB)
- **Origin:** Ground-truth GSSP and Konservat-Lagerstätten horizons compiled from primary geological literature (Droser, Bottjer, Mángano, Buatois, Seilacher).
- **Scale:** **6 reference horizons** spanning 558 Ma to 505 Ma:
  1. `HZ_WHITE_SEA_ED_02`: White Sea / Zimnii Bereg (Russia, 550–558 Ma)
  2. `HZ_FORTUNE_HEAD_ED_01`: Fortune Head Bed 1–2 (Newfoundland, 539–543 Ma)
  3. `HZ_FORTUNE_HEAD_CB_01`: Fortune Head GSSP Bed 2A (Newfoundland, 535–538.8 Ma)
  4. `HZ_MEISHUCUN_CB_02`: Meishucun Section (Yunnan, China, 532–537 Ma)
  5. `HZ_MAOTIANSHAN_CB_03`: Chengjiang Yu'anshan Mbr (Yunnan, China, 518–521 Ma)
  6. `HZ_BURGESS_SHALE_CB_04`: Burgess Shale Stephen Fm (Canada, 505–508 Ma)
- **Fields Preserved:** Section name, country, stage name, age top/bottom, index ichnotaxon, substrate penetration dimension (`2D_SURFACE_MAT`, `2.5D_MICROBIAL_UNDERMAT`, `3D_VERTICAL_INFAUNAL`, `3D_NEKTONIC`), maximum burrow depth $Z_{\max}$ (mm), biomineralization flag, mineralogy type, primary DOI.

### C. Van Holstein & Foley (2024) Raw Archive (`work/marsyas6/papers/valence-ingress/data/van-holstein/`)
- **File:** `Data_Code_Final.zip` (3.4 MB archive downloaded from Figshare DOI 10.6084/m9.figshare.24183417.v1).
- **Contents:**
  1. `PyRate/Data/Occurrence_database.xlsx`: Full fossil occurrences for all hominin taxa.
  2. `WB_equivalent_taxonomy.csv`: 17 hominin species (7 *Homo*, 10 non-*Homo*) from 4.2 Ma to present.
  3. PyRate MCMC logs: Bayesian posterior samples across 4 configurations (Broad NHPP, Broad TPP, Fine NHPP, Wood-Boyle).
  4. `vanHolstein_Foley_2024_final.R`: Original authors' R code and DR diversification rate scripts.

### D. Acquired Primary Literature Corpus (`work/marsyas6/papers/valence-ingress/acquired/`)
Over 15 acquired high-resolution PDFs of primary literature:
- *Ferraioli et al. (2026)*: Ancient nervous system and Cambrian ctenophore preservation.
- *Douglas et al. (2011)*: The Cambrian Conundrum and early animal evolution.
- *Prang et al. (2025)*: Ardipithecus ramidus ankle and functional morphology.
- *Otarola-Castillo et al. (2023)* / *Courtenay (2017)*: Geometric morphometrics of bone cut marks.
- *Pineda (2023)* / *Finkel (2023)*: Lithic raw material and taphonomic alteration experiments.

---

## 3. Inventory of Curated & Relational Assets

### A. The Curated SQLite Database (`studies/cambrian-substrate/data/curated/cambrian_substrate.db`)
A 260 KB relational database with strict schema enforcement, primary keys, check constraints, and foreign key relations:
1. `stratigraphic_horizons`: 6 reference horizons with check constraints ensuring $Z_{\max} \ge 0$, valid age ranges, and mineralogy constraints.
2. `cambrian_occurrences`: 1,000 occurrences assigned to functional guilds (`SEDENTARY_FILTER_FEEDER`, `INFAUNAL_BURROWER`, `MOBILE_APEX_PREDATOR`, `OTHER_UNCLASSIFIED`).
3. `epistemic_data_annotations`: Registry of epistemic overrides, citations, and warrants.
4. `v_guild_richness_summary` & `v_calibrated_guild_diversity`: Analytical views computing stage-by-stage occurrences, distinct taxa, and mean durations.

### B. Cryptographic Provenance Receipt (`studies/cambrian-substrate/data/curated/PROVENANCE_RECEIPT.json`)
- Sealed metadata tracking source file sizes, row counts, ingest timestamps, and SHA-256 hashes for all raw files.

---

## 4. Prior Studies & Analyses Performed on This Data

### A. The Cambrian Taphonomic Evidentiary Profile (`TAPHONOMIC_EVIDENTIARY_PROFILE.md`)
- **Analyzed:** The entire 1,000-row occurrence dataset.
- **Findings:**
  - **Frequency Spectrum:** Severe singleton dominance. 249 of 431 taxa (57.8%) appear exactly once. 324 taxa (75.2%) appear $\le 2$ times. Only 12 taxa have $\ge 10$ occurrences.
  - **Spatial Clustering:** Occurrences condense into 87 distinct collection horizons. The top 5 collections contain 14.3% of all occurrences (e.g., `col:215` with 34 taxa in a single quarry bed).
  - **Guild Disparity:** Mobile predators/arthropods outnumber infaunal burrowers 126 to 1 (634 occurrences vs 5). Zero infaunal body fossils exist in the Fortunian stage.
  - **Temporal Resolution:** Interval widths range from 2.8 Myr (Paibian) to 51.95 Myr (unpartitioned Cambrian).

### B. Sediment Mechanics & Diagenesis Profile (`SEDIMENT_MECHANICS_AND_DIAGENESIS_PROFILE.md`)
- **Analyzed:** Continuous 1D diagenetic reaction-diffusion across the 6 reference horizons.
- **Findings:**
  - Solved steady-state porewater equations using finite-volume diagenetic solver (`diagenetic_tiering.py`).
  - Proved that the shift from Ediacaran matgrounds ($Z_{\max} = 2.0\text{ mm}$) to Fortunian infaunal burrowing ($Z_{\max} = 35.0\text{ mm}$) expands dissolved oxygen penetration from $\sim 1\text{ mm}$ to $\sim 15\text{ mm}$, expanding aerobic sub-benthos volume by $14.2\times$.
  - Articulated the *Agronomic Erasure*: bioturbation oxygenated the sediment and destroyed cyanobacterial seals, eliminating the anoxic pyritized "death mask" preservation conditions that previously fossilized soft-bodied organisms.

### C. Van Holstein & Foley Re-Analysis (`work/marsyas6/papers/valence-ingress/data/van-holstein-analysis.md`)
- **Analyzed:** Figshare MCMC posterior traces (post-burn-in > 1000 iterations).
- **Findings:**
  - Re-computed diversity-dependent speciation ($Gl$) and extinction ($Gm$) slopes across all 4 configurations (Broad NHPP, Broad TPP, Fine NHPP, Wood-Boyle).
  - Confirmed positive diversity-dependent speciation in *Homo* ($Gl = +2.119$, 84% probability positive) and negative diversity-dependent speciation in non-*Homo* ($Gl = -0.262$, 32% probability positive).
  - Confirmed negative diversity-dependent extinction in *Homo* ($Gm = -7.915$, 100% negative).

### D. Comparative Clade Analyses (Cichlids & Technological Scaling)
- **Cichlid DD Analysis (`cichlid-dd-test.md`):** Comprehensive literature audit of adaptive radiations in Lakes Malawi, Tanganyika, and Victoria. All published phylogenetic models (BAMM, ClaDS) confirm classic negative diversity-dependence (early burst followed by deceleration/niche filling). No positive DD exists in cichlids.
- **Technological Gradients (USPTO, PyPI, GitHub, Wikipedia):** Empirical time series measuring $\beta$ scaling exponents across technological and cultural corpora (`uspto-growth-analysis.md`, `pypi-beta-analysis.md`, `github-beta-analysis.md`).

---

## 5. Summary of Test Coverage & Harness Infrastructure

The dataset and its analytical derivatives are continuously verified by a hermetic CI pipeline:
- **Pytest:** 30 unit, property-based (Hypothesis), and invariant tests:
  - `test_data_standards_and_forensics.py`: Schema invariants, date formats, SHA-256 hashes.
  - `test_taphonomic_data_profile.py`: Singleton proportions, collection clustering, guild disparity ratios.
  - `test_sediment_mechanics_profile.py`: Matground diffusion shutoff, oxygen penetration expansion, tier monotonicity.
  - `test_lineage_horizon_evaluator.py`: Stratigraphically coupled horizon resampling.
- **Behave BDD:** 24 declarative acceptance scenarios across 123 individual steps:
  - `features/taphonomic_data_profile.feature`
  - `features/sediment_mechanics_profile.feature`
  - `features/lineage_horizon_evaluation.feature`
  - `features/transforms_provenance.feature`
- **Current CI Status:** 100% green on `main` under GitHub Actions.
