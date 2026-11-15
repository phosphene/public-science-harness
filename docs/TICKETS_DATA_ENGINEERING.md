---
title: Data Engineering and Quality Standards Implementation Plan (Mertz 2021 / DFF)
status: active
author: Ed Phil & Flow (@feelingflowingbot)
date: 2026-11-15
---

# Data Engineering & DFF Implementation Plan

This ticket board operationalizes the technical standards established in:
- `docs/DATA_STANDARDS.md`
- `docs/DFF_DATA_STANDARDS.md`
- `docs/MERTZ_2021_DATA_CLEANING_STANDARDS.md`

Following Phosphene Python standards:
- **Axiomatic Vitals:** All models inherit from `InvariantStatic` (`frozen=True, extra="forbid"`).
- **Logic / IO Separation:** Pure mathematical and forensic transformations are decoupled from filesystem or network I/O.
- **Strict Typing:** Python 3.11+, typed enums, explicit bounds.
- **Fail-Fast Validation:** Boundary conductance gates before data touches model evaluation.

---

## Ticket Breakdown

| Ticket ID | Category | Title | Scope & Acceptance Criteria | Status |
|---|---|---|---|---|
| **PSH-001** | Core | Axiomatic Vitals & Missingness Taxonomy | Define `InvariantStatic`, `MissingnessCategory`, and `SanitizedField` models cleanly distinguishing `NULL` (unobserved), `NaN` (uncomputable), `NOT_APPLICABLE`, and sentinel flags. | **READY** |
| **PSH-002** | Forensics | Bit-Boundary & String Truncation Forensics | Implement `BitBoundaryForensics` and string clipping diagnostics checking column extrema against $2^{15}-1, 2^{31}-1$ and length histograms against max schema bounds. | **READY** |
| **PSH-003** | Forensics | Categorical & Homoglyph Forensics | Implement Unicode normalization, NFKC checks, and non-ASCII / Cyrillic homoglyph detection across categorical factor vocabularies. | **READY** |
| **PSH-004** | Forensics | Sample-Size Scaled Outlier Calipers | Implement `SampleScaledOutliers` scaling $Z$-score and IQR fence thresholds to sample size $N$ ($4\sigma$, $4.5\sigma$) to avoid lopping legitimate tail points in large $N$. | **READY** |
| **PSH-005** | Hygiene | SQLite STRICT DDL Generator | Implement declarative schema-to-SQL compiler enforcing `STRICT` mode tables or explicit `typeof(col)` constraints to eliminate SQLite type affinity chimera. | **READY** |
| **PSH-006** | Invariant | Multivariate Domain Invariants Engine | Implement cross-column joint assertions (temporal monotonicity `start <= end`, physical ratios, conservation laws) evaluating records before promotion to `data/curated/`. | **READY** |
| **PSH-007** | Pipeline | Cambrian Substrate Pipeline Hardening | Integrate PSH-001 through PSH-006 into `studies/cambrian-substrate/` pipelines and verify via automated pytest suite. | **READY** |
