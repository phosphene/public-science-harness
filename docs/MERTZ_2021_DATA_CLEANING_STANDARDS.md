# Review of Data Standards and Cleaning Techniques (Mertz, 2021)

This document synthesizes the core data engineering standards, format warnings, and statistical cleaning techniques from David Mertz's *Cleaning Data for Effective Data Science* (Packt, 2021), pairing each proviso with Mertz's verbatim observations and evaluating how they reinforce or extend `DATA_STANDARDS.md` in `public-science-harness`.

---

## 1. Foundational Philosophy and Alignment

Mertz's overarching framework aligns directly with our Design for Falsifiability (DFF) and Normal Science mandates:

* **Universal Dirtiness and Imbesi's Law:** All empirical datasets contain integrity defects within some margin of error. Cleaning data does not eliminate uncertainty; it isolates and documents defects so downstream statistical models test actual empirical variation rather than software artifacts.
  > "Certainly, some data is better and some is worse. But all data is dirty, at least within a very small margin of error in the tally. ... Even after our best pre-processing, a more attainable goal should be to make our data less dirty; making it clean remains unduly utopian in aspiration." — David Mertz (Preface)

* **Data Quality vs. Data Utility:** Quality (internal structural and numerical integrity) and utility (fitness for a specific scientific question) are orthogonal. A mechanically clean table can still suffer from fatal selection bias, while a noisy table can remain useful once its defects are bounded.
  > "By all means we should distinguish data quality from data utility. These descriptions are roughly orthogonal to each other. Data can be dirty (up to a point) but still be enormously useful. Data can be (relatively) clean but have little purpose, or at least not be fit for purpose." — David Mertz (Preface)

* **Structural Grime vs. Content Grime:**
  * *Structural grime* puts values in the wrong place (ragged CSV rows, broken escaping, multi-table spreadsheet layouts, character encoding corruption). It must be resolved at ingestion.
  * *Content grime* puts wrong values in the right place (sentinel codes, sign inversions, integer overflows, unit mismatches). It requires domain bounds and statistical forensics.
  > "On the structural branch a format used to encode a dataset might simply 'put values in the wrong place' in one way or another. On the content side, the data format itself is correct, but implausible or wrong values have snuck in via flawed instruments, transcription errors, numeric overflows, or through other pitfalls of the recording process." — David Mertz (Preface)

* **Scripted Provenance and Idempotence:** Never overwrite raw source files, and never rely on interactive notebook state as the record of truth. Every transformation must live in version-controlled scripts (`pipelines/` or `sql/`) and, wherever possible, be **idempotent** ($f(f(x)) = f(x)$) so re-running a pipeline step produces identical results.
  > "The exploration is an integral part of data science, but reproducibility should not be lost in that process. Good practice is to retain your original dataset—in whatever data format it originally presents itself—and generate the final version via scripts (maintained in version control) rather than within notebooks or interactive shells." — David Mertz (Ch. 4)

---

## 2. Format Standards and Ingestion Traps (Part I: Chapters 1–3)

### 2.1 Tabular and Relational Formats

* **Tidy Data and Third Normal Form (3NF):** Following Hadley Wickham and E. F. Codd, variables must live in columns, observational units in rows, and single values in cells. Wide human-readable tables (e.g., separate columns for `4th_grade`, `5th_grade`, `6th_grade`) encode values as column headers and must be melted/pivoted into normalized relational tables before statistical modeling.
  > "In brief, tidy data carefully separates variables (the columns of a table, also called features or fields) from observations (the rows of a table, also called samples). At the intersection of these two, we find values, one data item (datum) in each cell." — David Mertz (Ch. 1)

* **Delimited Text (CSV / TSV) and Greedy Type Inference:** Delimited files carry no embedded type metadata. Data frame readers (`pandas.read_csv`, `readr::read_csv`) infer column types from a sample of leading rows (e.g., the first $1,000$ or $100,000$ rows). If an identifier like `part_no` is purely numeric in early rows (`12345`) and alphanumeric later (`A9922`), lazy or partial inference fails or corrupts types. Always specify explicit schemas (`dtype` / `col_types`) at ingestion.
  > "I have myself, in a 'throw-away script,' written `print(",".join([1,2,3,4]), file=csv)` countless times; that works well, until it doesn't. Of course, throw-away scripts become fixed standard procedures for data flow far too often." — David Mertz (Ch. 1)

* **Spreadsheets Considered Harmful:** Spreadsheets must be quarantined and converted to typed tables immediately at the raw boundary because they permit **per-cell typing** rather than per-column typing, hide formulas across arbitrary grid coordinates, encourage multiple non-contiguous tables per sheet, and silently coerce domain strings (e.g., turning gene symbols like `SEPT2` into calendar dates).
  > "To no less of a degree, spreadsheets in general, and Excel in particular, are anathema to effective data science. ... Metaphorically, the danger posed by spreadsheet UIs resembles the concept in tort law of an 'attractive nuisance'—they do not directly create the harm, but they make harm exceedingly likely with minor inattention." — David Mertz (Ch. 1)

* **SQL RDBMS Strengths and Failure Modes:**
  * *Truncation of Fixed-Width Strings:* Legacy schemas using `CHAR(N)` or narrow `VARCHAR(N)` silently clip strings at $N$ characters. Detect this by plotting a histogram of string lengths (`LENGTH(col)`): an artificial spike at the exact column width $N$ signals truncation.
  * *Integer Clipping and Wrap-Around:* Narrow integer types (`SMALLINT`, 16-bit signed) clip or fail at $2^{15} - 1 = 32,767$ (or wrap positive magnitudes into negative numbers). Always check column maxima and minima against power-of-two boundaries ($2^7 - 1$, $2^{15} - 1$, $2^{31} - 1$) and leave at least an order-of-magnitude headroom.
  * *SQLite Type Affinity Quirk:* Standard SQLite stores types per value rather than strictly enforcing column types (nudging values via *type affinity* instead of rejecting mismatched strings in integer columns). When using SQLite in `public-science-harness`, enforce `STRICT` table definitions or explicit `CHECK (typeof(col) = ...)` constraints.
  > "Data typing in SQLite is something of a chimera." — David Mertz (Ch. 1)

* **Scientific Binary and Columnar Stores:**
  * *Apache Parquet:* Preferred for medium-to-large tabular data; enforces per-column types and supports fast columnar scans.
  * *HDF5 and NetCDF-4:* Designed for homogeneous $N$-dimensional numerical arrays with attached metadata attributes (`units`, `_FillValue`, `valid_range`) and lazy disk slicing (`h5py`, `rhdf5`). Note that array axis ordering transposes between Python (row-major C order) and R (column-major Fortran order).
  > "Unlike with the data frame model, arrays within these scientific formats are of homogeneous type throughout. That is, there is no mechanism (by design) to store a text column and a numeric column within the same object, nor even numeric columns of different bit-widths." — David Mertz (Ch. 1)

### 2.2 Hierarchical and Configuration Formats

* **JSON Is Syntax, Not Semantics (RFC 8259):**
  * *Numeric Ambiguity and Missing Specials:* JSON has a single `number` syntax with no distinction between integers, floats, or fixed-point decimals, and standard JSON forbids `NaN` and `Infinity`. Different parsers handle extensions inconsistently: Python's `json` accepts `NaN` by default; strict JavaScript `JSON.parse` throws a `SyntaxError`; R's `rjson` serializes them as strings (`"NaN"`) that fail to round-trip; `jq` clamps `Infinity` to $\pm 1.7976931348623157 \times 10^{308}$.
  * *Validation Gate:* Validate any incoming or outgoing JSON payload against an explicit **JSON Schema** before processing. Use **JSON Lines** (`ndjson`) when streaming line-oriented records.
  > "An important thing to understand about JSON is that it specifies a syntax, but not a semantics. Each language has to make decisions about how to process text conforming with JSON grammar." — David Mertz (Ch. 2)

* **XML Complexity:** XML splits data arbitrarily between element bodies and tag attributes, relies heavily on namespaces, and lacks automatic type coercion into native data structures even when an XSD or RELAX NG schema is present. Extract XML to flat typed tables at ingestion and discard it downstream.
  > "I take violence to always be unacceptable, and XML only mostly so. Both remain far too common in our world. This corrective paraphrase only partially fixes the concern: 'XML is like violence: useful only in specific situations, and totally unacceptable everywhere else.'" — David Mertz (Ch. 2)

* **Configuration Files:** Prefer **TOML** (which supports native datetimes, integers, floats, and arrays) or well-scoped **YAML** (using `yaml.safe_load`) over ad-hoc `.ini` or custom text configs.
  > "The greatest difficulty comes with numerous software projects that have, for various reasons (few of them good), adopted their own custom configuration format." — David Mertz (Ch. 2)

* **NoSQL and Key-Value Stores:** Document stores (MongoDB) suffer from ragged schemas (missing keys across documents) and denormalization drift (duplicated fields falling out of sync across collections). Key-value stores (Redis, DBM) frequently accumulate inconsistent ad-hoc key delimiters (e.g., `entity::info::phone` vs. `entity//ratings`) over time.
  > "There is often—even usually—an impedance mismatch between hierarchical data and data science. ... Data science is about summarization and aggregation. It is almost never about individual entities in themselves." — David Mertz (Ch. 2)

### 2.3 Repurposing Non-Data Sources and Character Encodings

* **Web Scraping and PDFs:** Pin immutable historical URLs (such as Wikipedia `oldid` revision parameters) for reproducibility. Use DOM parsers (`rvest`, `BeautifulSoup`) or text-mode renderers (`lynx -dump`, `links -dump`) for HTML, and `tabula-java` or `pdftotext -layout` for PDFs — never proprietary GUI extractors.
  > "Let us wave goodbye to the Scylla of HTML, as we pass by, and fall into the Charybdis of PDF. ... If you have the misfortune of having data that is only available in printed and scanned form, you most certainly have my deep sympathy." — David Mertz (Ch. 3)

* **Character Encodings and Mojibake:** Legacy files encoded in `ISO-8859-*`, `Windows-1252`, or `GB18030` decoded as `UTF-8` either raise decode errors or silently produce *mojibake* (garbled characters). Automated detectors like `chardet` rely on byte validity and character/digraph frequencies and frequently misclassify short categorical strings; always record explicit source encodings in `data/raw/MANIFEST.json` and normalize all curated text to `UTF-8`.
  > "The sometimes amusing, but usually frustrating, result of trying to decode a byte sequence using the wrong encoding is called mojibake (meaning 'character transformation' in Japanese, or, more holistically, 'corrupted text'). ... Merely being not obviously wrong in a language you are not familiar with is a weak standard to meet." — David Mertz (Ch. 3)

---

## 3. Anomaly Detection and Data Quality (Part II: Chapters 4–5)

### 3.1 Missingness Taxonomy

A sound curation pipeline separates four distinct states that raw files routinely conflate:

1. **Unobserved / Not Available (`NULL` / `NA`):** Data was not recorded or is missing.
2. **Not Computable (`NaN`):** IEEE-754 floating-point arithmetic failure (e.g., $0/0$ or overflow).
3. **Not Applicable (`""` or explicit enum):** The attribute does not apply to the entity (e.g., a subject with no middle name).
4. **Magic Sentinels (`-1`, `-999`, `999.9`, `'?'`, `'UNKNOWN'`):** Legacy placeholder codes that severely bias means and inflate sample variance ($\sigma^2$) if ingested as real numbers. Inspect column `.min()`, `.max()`, and value counts at ingestion to strip all sentinels into explicit `NULL`s paired with status flags.
  > "The map is not the territory and data is not the world observed. Data is messy, inconsistent, and unreliable. The world is messier, less consistent, and less reliable. ... Unfortunately, undocumented or underdocumented field constraints are the rule in published data, not the exception." — David Mertz (Ch. 4)

### 3.2 Categorical Hygiene and Code-Point Forensics

* Inspect `value_counts()` on every categorical field to detect rare typos, leading/trailing whitespace, and inconsistent capitalization.
* **Unicode Homoglyph Detection:** Visually identical strings can contain mixed scripts (e.g., Cyrillic small letter `е` at `U+0435` substituted for Latin `e` at `U+0065`). Inspect character code points (`ord(c)`) or normalize text with Unicode NFKC/NFC checks during ingestion.
  > "However, keep in mind a software developers' motto that 'documentation' is a synonym for 'lies.' It may not accurately reflect the data itself..." — David Mertz (Ch. 4)

### 3.3 Bounds, Univariate Outliers, and Sample-Size Scaling

* **Hard Physical and Instrument Bounds:** Enforce domain limits (e.g., non-negative physical lengths, instrument ceiling limits) prior to statistical modeling. Distinguish true physical zeros from sentinel `-1` values by examining the distribution of boundary violations.
* **Distribution-Aware Univariate Outliers:**
  * Check approximate normality (e.g., via Anderson-Darling statistics or histograms) before applying $Z$-scores ($Z = (x - \mu) / \sigma$). $Z$-scores and interquartile range (IQR) fences break down on power-law or heavily skewed distributions without prior log or root transformations.
  * **Scale Thresholds to Sample Size ($N$):** Under a normal distribution, $|Z| > 3$ occurs in roughly $1$ out of $370$ observations (about $75$ expected points in $N = 25,000$). Dropping $|Z| > 3$ points in large datasets deletes valid tail observations; adjust thresholds to $4\sigma$ or $4.5\sigma$ (or tuned IQR whisker multipliers) based on $N$.
* **Multivariate Outliers:** Individual columns may fall inside valid marginal bounds while violating joint physical or domain relationships (e.g., an impossible combination of height and weight exposed only after computing $\text{BMI} = \text{kg} / \text{m}^2$). Always run cross-column domain invariant checks.
  > "Since BMI is a derived feature that combines height and weight—and moreover since each of those is within reasonable bounds on its own—the correct approach is almost surely simply to discard these problem rows. Nothing in the data themselves guides us toward knowing whether weight or height is the problem value, and no remediation is sensible." — David Mertz (Ch. 4)

### 3.4 Structural Quality, Bias, and Signal Separation

* **Biased Missingness Across Parameter Space:** Always check whether missingness correlates with covariates (e.g., missing survey responses concentrated in the $20\text{--}40$ age bracket). Dropping incomplete rows under non-random missingness hollows out regions of parameter space and biases regression estimates.
  > "While, as data scientists, we never want to declare a task hopeless, as responsible researchers we need to consider the possibility that particular data simply cannot support any conclusions." — David Mertz (Ch. 5)

* **External Baseline Comparison and Digit Forensics:**
  * Compare sample subgroup proportions against known external population baselines (e.g., Census state populations) and inspect normalized variance across strata to detect undisclosed oversampling or selection bias.
  * For scale-invariant positive numerical measurements spanning orders of magnitude, test leading digits against **Benford's Law** ($P(d) = \log_{10}(1 + 1/d)$) to screen for fabrication, rounding artifacts, or arbitrary truncation.
  > "An old joke observes someone looking for their lost keys at night in the area under a street light. Asked why they do not also look elsewhere, they answer that it is because the visibility is better where they are looking. This is a children's joke, not told particularly engagingly, but it also lays the pattern for most data collection of most datasets." — David Mertz (Ch. 5)

* **Class Imbalance and Weighting:** Distinguish target-variable imbalance from feature-level imbalance. Where rare classes or high-reliability measurements require emphasis without fabricating synthetic observations, use model `sample_weight` or `class_weight` parameters rather than duplicating rows.
  > "Understanding data integrity issues resembles either a scientific process of experimentation and hypothesis, or perhaps even more so a murder mystery. Developing a reasonable theory of why the data is dirty is always a good first step in remediating it..." — David Mertz (Ch. 5)

* **Scaling and Floating-Point Tolerance:** Distance-based models (KNN, SVM, regularized linear models) fail when features span mismatched orders of magnitude. Choose scalers deliberately: `StandardScaler` for roughly symmetric features, `QuantileTransformer` when extreme outliers remain (note that `RobustScaler` divides by IQR and still leaves a single extreme outlier far out in transformed space). Never test floating-point transformations with exact equality (`==`); allow 1-ULP numerical tolerances (`np.allclose` / R `all.equal`).
  > "Comparing for strict equality of floating-point values is almost always the wrong thing to do; measurements have finite precision and operations introduce 1-ULP (unit in the last place) errors frequently." — David Mertz (Ch. 5)

* **Cyclicity and Autocorrelation:** Separate known deterministic cycles (annual seasonal trends, diurnal $\sin/\cos$ harmonics) and inspect autocorrelation functions (`acf`) at domain-relevant lags (e.g., $12\text{h}$, $24\text{h}$, $7\text{d}$) so periodic structure is not mistaken for independent noise or anomalous spikes.
  > "Our goal is not to remove the underlying variability altogether but rather to emphasize the more extreme magnitude measurements, which this has done." — David Mertz (Ch. 5)

* **Bespoke Domain and Collation Validation:** Implement custom domain assertions to catch multi-record collation errors — such as exact duplicate sequences tagged under conflicting taxonomic ranks or impossible intra-record repetitions.

---

## 4. Rectification, Imputation, and Feature Engineering (Part III: Chapters 6–7)

### 4.1 The Imputation Boundary in `public-science-harness`

Mertz highlights two critical statistical consequences of imputation and resampling:
1. Imputation reduces residual variance and heteroscedasticity by pulling missing points toward central or local trends.
2. Synthetic oversampling (such as SMOTE or ADASYN) manufactures artificial observations in feature space.

**Harness Rule:** Imputed or synthetically resampled tables are valid for training predictive machine learning models, **never** for primary hypothesis testing or estimating degrees of freedom ($N$) in inferential statistics. Keep imputed/resampled outputs strictly separated from `data/curated/` inferential tables, and flag every imputed cell with a boolean provenance indicator.
  > "In somewhat technical terms, we can note that imputation usually reduces heteroscedasticity since almost every kind of imputation follows a trend, not variability from that trend. For almost all data science purposes, that is desirable, or at least acceptable, but we should avoid stating many kinds of statistical generalizations on imputed data (usually using the raw data for those purposes instead)." — David Mertz (Ch. 6)

### 4.2 Imputation Techniques

* **Central Tendency Selection:** Match the estimator to the variable's scale: arithmetic mean or median for linear scales, **geometric mean** for quantities spanning orders of magnitude or exponential growth, and **harmonic mean** for rates and velocities.
  > "Keep in mind that these several averages are often numerically close to each other, and since an imputation is a guess to begin with, the choice among them may be striving for a false precision." — David Mertz (Ch. 6)

* **Spatial Locality and Trend Interpolation:** Use neighbor averaging for spatial grids, time-weighted interpolation (`interpolate(method='time')`) for unevenly spaced timestamps, and group-scoped interpolation (`groupby(entity_id)`) so missing leading/trailing entries never bleed across distinct subjects or parcels.
  > "Choosing the best interpolation technique is an art." — David Mertz (Ch. 7)

### 4.3 Time-Series Regularization and Feature Engineering

* **Timestamp Hygiene:** Verify `is_monotonic_increasing` on time indices (catching Daylight Saving Time backward jumps), resolve duplicate timestamps explicitly (deduplicating or aggregating after screening for sensor cross-talk outliers), and reindex onto regular time grids (`asfreq`) so missing intervals become explicit `NULL` rows.
* **NOIR Scale Discipline:** Classify every variable as **Nominal**, **Ordinal**, **Interval**, or **Ratio** before encoding:
  * Never treat arbitrary numeric IDs as additive or ordinal.
  * Never compute ratios on interval scales lacking a natural zero (e.g., temperatures in $^\circ\text{C}$ or $^\circ\text{F}$).
  * Use **One-Hot Encoding** for nominal categories so models do not infer false ordering.
  > "But data science has no interest in books, articles, nor even in short free-form annotations. We only like categorical, numeric, ordinal, and date/time data. *De minimis non curat lex.*" — David Mertz (Ch. 7)

* **String Canonicalization:** Prefer linear-time phonetic canonicalization (**Double Metaphone**) over quadratic ($O(N^2)$) pairwise edit distance (`Levenshtein`) when unifying transliterated names across large tables, while accounting for non-transitivity.
* **Dimensionality Discipline:** When generating interaction/polynomial features or decompositions (PCA with whitening), respect the $p \le N / 10$ rule of thumb (keeping feature count $p$ well below one-tenth of observation count $N$) and prune uninformative dimensions via cross-validated recursive feature elimination (`RFECV`).
  > "After the entropy is accounted for, all that is left is noise." — David Mertz (Ch. 7)

* **Human Judgment Over Blind Automation:** Automated pipelines and AutoML suites accelerate execution, but domain-grounded epistemic decisions cannot be delegated to black-box automation.
  > "You can—and quite likely should—rent massive parallelism for large data and sophisticated modeling pipelines, but this is still somehow ontologically shy of machines genuinely guiding analytic decisions." — David Mertz (Closure)

---

## 5. Actionable Upgrades for `DATA_STANDARDS.md`

To operationalize Mertz's strongest safeguards inside `public-science-harness`, incorporate the following six concrete checks into our standard curation checklist:

1. **SQLite `STRICT` Enforcement:** Require `STRICT` tables in all `.sqlite` curated databases so dynamic type affinity cannot silently store strings inside numeric columns.
  > Proviso anchor: *"Data typing in SQLite is something of a chimera."* (Ch. 1)

2. **Truncation and Bit-Boundary Audits:** Run automated SQL/Python diagnostics on every ingested table checking string length distributions (`MAX(LENGTH(col))` vs. schema limits) and numeric extrema against signed/unsigned integer bounds ($2^{15}-1$, $2^{31}-1$).
  > Proviso anchor: *"In general, if you ever see a measurement that is exactly one of these bounds, you should take a second look and think about whether it might be an artifactual number rather than a genuine value."* (Ch. 1)

3. **Unicode and Homoglyph Normalization:** Enforce `UTF-8` decoding and scan categorical string columns for non-ASCII code points (`ord(c) > 127`) and leading/trailing whitespace before finalizing factor vocabularies.
  > Proviso anchor: *"Merely being not obviously wrong in a language you are not familiar with is a weak standard to meet."* (Ch. 3)

4. **Multivariate Domain Invariants:** Require at least one cross-column consistency assertion (e.g., physical ratios, temporal ordering `start_utc <= end_utc`, or conservation laws) in addition to single-column range checks.
  > Proviso anchor: *"Sometimes univariate features can fall within relatively moderate z-score boundaries, and yet combinations of those features are unlikely or unreasonable."* (Ch. 4)

5. **Segregation of Imputed and Resampled Artifacts:** Store imputed or SMOTE-balanced datasets in a separate derived artifact tier (e.g., `data/model_inputs/`) with explicit `is_imputed` flags, preserving `data/curated/` strictly for observed measurements used in statistical tests.
  > Proviso anchor: *"...we should avoid stating many kinds of statistical generalizations on imputed data (usually using the raw data for those purposes instead)."* (Ch. 6)

6. **Tolerance-Based Regression Assertions:** Mandate relative/absolute floating-point tolerances (e.g., `rtol=1e-12`, `atol=1e-12`) rather than exact `==` comparisons in all precursor baseline replication scripts to accommodate 1-ULP cross-language arithmetic differences between Python, R, and SQL engines.
  > Proviso anchor: *"Comparing for strict equality of floating-point values is almost always the wrong thing to do; measurements have finite precision and operations introduce 1-ULP (unit in the last place) errors frequently."* (Ch. 5)
