---
id: transforms-provenance-and-annotation
uri: docs/transforms-provenance-and-annotation
title: Transforms, Provenance, and Annotation Standards
owner: edphos
contributors: [edphos, feelingflowingbot]
status: active
created: "2026-11-15"
updated: "2026-11-15"
tags: [data-standards, provenance, transforms, annotations, dff, calibration]
related: [docs/DATA_STANDARDS, docs/DFF_DATA_STANDARDS, docs/MERTZ_2021_DATA_CLEANING_STANDARDS, eval/provenance-event-v1]
---

# Transforms, Provenance, and Annotation Standards

## 1. Executive Summary & Epistemic Grounding

In computational empirical science, raw data never enters an estimator untouched. Every step between upstream collection (raw CSVs, API dumps, digitized museum logs) and statistical evaluation is an act of **translation**.

When transformations are undocumented or implicit:
1. **The Duhem–Quine Escape Hatch Opens:** Discrepancies between theory and observation are blamed on data handling quirks rather than model flaws.
2. **Auxiliary Assumptions Disappear:** Filtering choices (e.g. discarding unclassified taxa, grouping orders into functional guilds) disguise biological assumptions as mundane data cleaning.
3. **Reproducibility Decays:** Downstream users cannot reconstruct how raw bytes became calibrated estimators.

This standard establishes three mutually reinforcing contracts for all empirical packages in the `public-science-harness`:
- **The Transform Contract:** Every data mutation must be declared as a versioned, idempotent, mathematical operation with explicit category, pre-conditions, and post-conditions.
- **The Provenance Ledger:** Every curated dataset must emit a machine-verifiable cryptographic receipt linking input artifacts, pipeline script git commit, runtime environment, and output artifacts.
- **The Annotation Ledger:** Human domain judgments and expert calibrations (e.g., taphonomic hazard corrections, fossil reclassifications, stratigraphic tie-ins) must be recorded as typed epistemic provenance events rather than ad-hoc code edits.

---

## 2. Taxonomy of Data Transforms

Data transforms are categorized according to their mathematical and epistemic effect on the underlying empirical distribution:

| Transform Category | Mathematical Definition | Epistemic Risk | Pre/Post Invariant Requirements |
|---|---|---|---|
| **`ISOMORPHIC_HYGIENE`** | Bijective or lossless standardization (strip whitespace, trim trailing delimiters, fix UTF-8 mojibake, normalize case). | Low | Record count strictly preserved ($N_{\text{in}} = N_{\text{out}}$). Field semantics unchanged. |
| **`SENTINEL_SANITIZATION`** | Map magic codes ($-999, 9999, \text{"N/A"}$) and censored markers ($< \text{LOD}$) to `SanitizedValue[T]` and `MissingnessCategory`. | High (loss of degrees of freedom) | Sentinels must not be coerced to numerical zeroes; original sentinel code preserved in metadata. |
| **`TAXONOMIC_HARMONIZATION`** | Map varying upstream factors or taxonomic classifications to a canonical ontology or functional guild. | Medium (misclassification bias) | Every unmapped factor routed to an explicit unclassified bucket; zero silent discards. |
| **`TEMPORAL_BINNING`** | Discretize continuous geological ages ($\text{Ma}$) or radiometric dates into stratigraphic stages or chronozones. | Medium (boundary aliasing) | Monotonicity preserved ($\text{age}_{\text{bottom}} \ge \text{age}_{\text{top}}$); intervals strictly bounded. |
| **`TAPHONOMIC_CALIBRATION`** | Scale or weight raw occurrence frequencies using physical sampling proxies (sediment volume, formation count, ichnofacies tiering depth). | High (model distortion) | Raw unadjusted counts preserved alongside adjusted values; calibration formula and warrants recorded. |
| **`AGGREGATION_REDUCTION`** | Group occurrences into stage-level richness, sampling ratios, or guild counts. | Low | Dimension reduction; aggregation invariant (sum of parts equals total occurrences). |

---

## 3. The Transform Ruleset Schema

Every transformation pipeline must declare its ruleset as a declarative specification or typed Python schema conforming to `TransformSpec`:

```yaml
transform_id: TR-CAMBRIAN-001
version: "1.0.0"
title: "Ichnofacies Stratigraphic Horizon Calibration & Guild Mapping"
category: "TAPHONOMIC_CALIBRATION"
inputs:
  - dataset_uri: "data/raw/pbdb_cambrian_metazoa_raw.json"
    schema_version: "pbdb.v1.2"
  - dataset_uri: "data/raw/stratigraphic_horizons_raw.csv"
    schema_version: "gssp.ichno.v1"
outputs:
  - table_name: "v_guild_taphonomic_calibration"
    schema: "schemas/guild_calibration.schema.yaml"
invariants:
  pre_conditions:
    - "raw_records_count > 0"
    - "age_bottom_ma >= age_top_ma"
  post_conditions:
    - "calibrated_richness >= raw_richness"
    - "sampling_tier in ('SKELETAL_LAG', 'ICHNO_INFAUNAL', 'NEKTONIC_VISUAL')"
```

---

## 4. The Dataset Provenance Receipt

When a pipeline completes execution, it writes a `PROVENANCE_RECEIPT.json` alongside the curated database in `data/curated/`. This receipt satisfies the Phosphene platform provenance standard (`eval/provenance-event-v1.md`):

```json
{
  "receipt_id": "rcpt-20261115-cambrian-substrate-v1",
  "pipeline_id": "pipelines/03_calibrate_taphonomic_diversity.py",
  "git_commit_sha": "c6150ef093...",
  "executed_at_utc": "2026-11-15T23:15:00Z",
  "actor": {
    "id": "flow@feelingflowingbot",
    "type": "automated_pipeline",
    "role": "Data Integrity Engine"
  },
  "input_artifacts": [
    {
      "path": "data/raw/stratigraphic_horizons_raw.csv",
      "sha256": "8ea44c0a1242e6c35c602334f59bc02bfe88e285d05e263dbe6f00e95cb5b7be",
      "record_count": 6
    },
    {
      "path": "data/raw/pbdb_cambrian_metazoa_raw.json",
      "sha256": "f0071ae3d48818fa8d39f70cd59b7eaeb2491fa3571d871fe7e4e1a0fc1bc98b",
      "record_count": 1000
    }
  ],
  "output_artifacts": [
    {
      "path": "data/curated/cambrian_substrate.db",
      "sha256": "a34b22c9...",
      "tables": ["stratigraphic_horizons", "cambrian_occurrences", "taphonomic_annotations"]
    }
  ]
}
```

---

## 5. Epistemic Annotation Standard

Annotations represent domain corrections, taxonomic determinations, and taphonomic hazard disclosures. Rather than leaving annotations in untracked spreadsheets or ephemeral comments, annotations are treated as **typed epistemic events** recorded in an immutable relational table or append-only JSON-L ledger.

### 5.1 Schema (`DataAnnotationEvent`)

Every annotation record contains:
- **`annotation_id`**: Canonical UUID / URI (e.g. `annot-20261115-priapulida-taphonomy`).
- **`target_entity_type`**: `TABLE`, `RECORD`, `COLUMN`, or `VALUE`.
- **`target_selector`**: SQL predicate or identifier (e.g., `functional_guild = 'INFAUNAL_BURROWER'`).
- **`epistemic_warrant`**: DOI or published literature citation justifying the judgment.
- **`actor_id`**: Identifier of researcher or agent declaring the annotation.
- **`judgment_type`**: `DISCLOSURE`, `CALIBRATION_OVERRIDE`, `RECLASSIFICATION`, or `FLAG_EXCLUSION`.
- **`rationale`**: Structured text explaining why raw data without this annotation produces a false inference.

---

## 6. Worked Calibration Case: Paper 01 Cambrian Infaunal Diversity

### 6.1 The "Dirty Data" Baseline
- Upstream source: Paleobiology Database (PBDB) API query for `Metazoa`, `Cambrian`.
- Naive Query Result:
  - `MOBILE_APEX_PREDATOR` (Arthropoda): 634 occurrences across 295 distinct taxa.
  - `SEDENTARY_FILTER_FEEDER` (Brachiopoda, Porifera): 246 occurrences across 81 distinct taxa.
  - `INFAUNAL_BURROWER` (Priapulida, Hemichordata): **5 occurrences across 4 distinct taxa**.

### 6.2 The Epistemic Hazard
A naive diversity-dependence model ($Gl$) fitted directly to PBDB occurrences calculates a flattened or unconstrained diversification rate ($Gl = -0.031$) for infaunal burrowers. This is an auxiliary artifact: Priapulids and vermiform worms possess unmineralized cuticles that do not survive normal taphonomic windows, yet they extensively bioturbated the global seabed across the Fortunian Agronomic Revolution (*Treptichnus pedum* tiering depth increased from 1.5 mm to 120 mm).

### 6.3 The Calibrated Transform & Annotation Ruleset
1. **Rule TR-01 (Taphonomic Segregation):** Body fossil occurrences must be flagged with `preservation_mode = 'BODY_FOSSIL'`.
2. **Rule TR-02 (Ichnofacies Synthesis):** Where body fossil sampling ratio $\frac{\text{Occurrences}}{\text{Taxa}} < 2.0$, the guild's ecological presence must be cross-indexed against the maximum burrow penetration depth ($D_{\text{tier}}$ in mm) from Dataset 1.
3. **Rule TR-03 (Calibration Annotation):** An explicit `DataAnnotationEvent` must be permanently joined to the analytical view, citing Brasier et al. (1994) and Buatois & Mángano (2011), forbidding raw body count diversity-dependence fitting without ichnofacies weighting.
