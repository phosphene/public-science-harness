# Raw Data Preservation Ethic: Format Invariance, Non-Conversion, and Pre-Question Grounding

**Document Coordinate:** `studies/cambrian-substrate/data/RAW_DATA_PRESERVATION_AND_FORMAT_ETHIC.md`  
**Repository:** `phosphene/public-science-harness`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Foundational Platform Ethic & Invariant Directive  
**Date:** 2026-11-16  

---

## 1. The Core Principle: Zero Premature Conversion

> *"In all these cases, the first objective is to preserve the raw data in the format that it's in. We never want to convert anything to JSON if it wasn't already there because we know we can lose lots of information that way. So whatever the data is, we just first want to get a hold of it before we ask any questions."* — Ed Phil (2026-11-16)

When raw data is acquired—whether TSV matrices, Excel spreadsheets, CSV tables, FASTQ/variant call files, or GenBank flat files—the primary scientific imperative is **format preservation**:
1. **Never transcode raw formats prematurely:** If raw data is in CSV or TSV, it stays in CSV or TSV. If it is in GenBank (`.gbk`), GFF, or FASTA, it remains in its native representation.
2. **Lossy JSON Conversions are Forbidden:** Converting rich columnar tabular data or domain-specific flat files into JSON structures often silently drops header metadata, destroys trailing precision, strips type annotations, collapses sparse matrices, and alters whitespace/coordinate semantics.
3. **Format Integrity over Convenience:** Tooling and parsers must adapt to the data's native format, not coerce the data into whatever schema happens to be easy to ingest in Python or JavaScript.

---

## 2. Manifest of Raw Empirical Assets in Native Formats

The workspace contains primary data across multiple distinct biological and historical domains. Every asset is preserved in its authentic native format:

```
NATIVE FORMAT INVENTORY
┌──────────────────────┬────────────────────────────────────────────────────────┬─────────────────────────┐
│ Domain               │ Native File Coordinate                                 │ Native Format           │
├──────────────────────┼────────────────────────────────────────────────────────┼─────────────────────────┤
│ Cambrian Occurrences │ `studies/cambrian-substrate/data/raw/pbdb...raw.json`  │ Native JSON (API dump)  │
│ Cambrian Horizons    │ `studies/cambrian-substrate/data/raw/strat...raw.csv`  │ Native CSV              │
│ Hominin Radiations   │ `work/marsyas6/.../Occurrence_database.xlsx`           │ Native Excel (.xlsx)    │
│ Hominin Taxonomy     │ `work/marsyas6/.../WB_equivalent_taxonomy.csv`         │ Native CSV              │
│ Parasitic Plants     │ `vi-foundry/data/species_plastome_data.tsv`            │ Native TSV              │
│ Retention Matrix     │ `vi-foundry/data/orobanchaceae_retention_matrix.tsv`   │ Native TSV              │
│ Cross-Family Plants  │ `vi-foundry/data/cross_family_plastome_data.tsv`       │ Native TSV              │
│ LTEE E. coli         │ `tools/ltee/data/p1_annotated_timecourse.txt`          │ Native Comma/Colon Table│
│ LTEE E. coli         │ `vi-foundry/data/t7-ltee/LTEE-metagenomic/...all.csv`  │ Native CSV              │
│ E. coli Reference    │ `vi-foundry/data/t7-ltee/.../additional_data/REL606.gbk│ Native GenBank Flatfile │
└──────────────────────┴────────────────────────────────────────────────────────┴─────────────────────────┘
```

---

## 3. How Loss Occurs During Premature Transcoding

Documented failure modes of converting native scientific tables into JSON:

1. **Header & Comment Eradication:**
   - In bioinformatics files (e.g., GFF3, VCF, CSV), comments starting with `#` or headers containing metadata (assembly build, run parameters, citation coordinates) are typically ignored or discarded when read into JSON objects.
2. **Column Structure & Sparse Representation:**
   - In the LTEE timecourse files (`p1_annotated_timecourse.txt`), there are 140+ paired columns (`AC:gen, DP:gen`). Converting this to nested JSON inflates disk footprints by 10x and risks numeric precision drift on floating-point p-values (`9.999e-05` becoming rounded strings).
3. **Taxonomic & Factor Typing:**
   - In TSV matrices (`orobanchaceae_retention_matrix.tsv`), categorical retention scores (`0.0, 0.5, 0.67, 1.0`) represent discrete fraction counts. Coercing these into arbitrary JSON numbers or strings obscures whether they were counts, proportions, or flags.
4. **Coordinate Integrity:**
   - Genomic and stratigraphic coordinates rely on exact 1-based or 0-based boundary semantics. Serializing through ad-hoc JSON wrappers frequently introduces off-by-one errors or breaks bed synchronization.

---

## 4. The Invariant Protocol for Data Ingress

Whenever new empirical data is introduced to the platform:
- **Phase 1: Ingest Native File As-Is.** Store the file in `data/raw/` with its original extension, original encoding, and native byte sequence.
- **Phase 2: Cryptographic Sealing.** Generate SHA-256 hashes and row/byte counts directly on the native file.
- **Phase 3: Forensic Inspection in Native Format.** Inspect row counts, delimiter structure, column schemas, and anomalies directly against the native text or binary structure (e.g., discovering the 71 bp PCR fragment artifacts directly in the TSV).
- **Phase 4: Read-Only Query Adapters.** If the data is queried in Python or SQL, read directly from the native format via streaming readers or load into an append-only relational database with strict schema check constraints. Never overwrite or replace the raw native file.
