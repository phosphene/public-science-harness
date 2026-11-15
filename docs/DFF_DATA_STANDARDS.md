# Why Data Hygiene Is Core to Design for Falsifiability (DFF)

## 1. The Core Connection: Eliminating Escape Hatches

In textbook philosophy of science, a hypothesis $H$ is falsifiable if there exists an observable outcome that would prove $H$ false. In empirical and computational science, however, we never compare a theory directly against raw nature. We compare a **statistical or numerical model** against a **dataset**.

This creates a fundamental diagnostic problem (the Duhem-Quine problem): when a model fails to match the data, or when a statistical test yields an unexpected result, there are always two competing explanations:

1. **The scientific claim is wrong** (the hypothesis has been falsified).
2. **The data representation is broken** (an auxiliary failure in units, missing-value codes, or table structure distorted the test).

**Design for Falsifiability (DFF)** in data engineering means systematically removing that second escape hatch before running any statistical test. If the data pipeline leaves ambiguities in place, a failed test cannot cleanly falsify a bad hypothesis, and a passing test can easily manufacture a false positive out of a software or encoding artifact.

---

## 2. How Each Data Hygiene Rule Protects Falsifiability

Every data curation rule in `OPERATING_GUIDELINES.md` and `DATA_STANDARDS.md` prevents a specific failure mode that would otherwise make empirical claims unfalsifiable:

### 2.1 Distinguishing True Zeros from Missing or Censored Entries

* **The failure mode:** Upstream datasets routinely encode unrecorded entries as `-999`, `9999`, or `0`, or collapse values below an instrument's limit of detection (LOD) into `0.0`.
* **Why it breaks falsifiability:**
  * If a model ingests `-999` as a real measurement, sample variance ($\sigma^2$) explodes, inflating standard errors so wide that **no hypothesis can be rejected** — a false null becomes immune to falsification.
  * Conversely, replacing left-censored observations (`< LOD`) with true `0.0` creates an artificial step-function cliff in the distribution, allowing a researcher to claim a sharp physical or biological threshold where none exists.
* **The DFF fix:** Separating `NULL` (unobserved), `censored` (bounded by detection limits), and `0.0` (verified zero magnitude) ensures the likelihood function tests actual empirical measurements rather than sentinel codes.

### 2.2 Documenting Physical Units and Normalizing Scales

* **The failure mode:** Merging tables where one cohort measures concentration in $\mu\text{mol/L}$ and another in $\text{mg/dL}$, or mixing seconds and milliseconds, without explicit unit normalization.
* **Why it breaks falsifiability:** Mechanistic models and rate laws make dimensionally specific predictions. If units are implicit or inconsistent, a mismatch between predicted and observed values can always be excused as a scaling discrepancy rather than a failure of the model. Worse, statistical regressions with unconstrained slope parameters will silently absorb a $1000\times$ unit error into a biased coefficient.
* **The DFF fix:** Enforcing explicit units (preferably SI) in schemas guarantees dimensional consistency so quantitative discrepancies actually count against the model.

### 2.3 Documenting Observational Structures (Keys and Dependencies)

* **The failure mode:** Flattening nested or longitudinal data — such as $50$ repeated measurements taken from each of $20$ subjects — into a single table of $N = 1000$ rows without primary/foreign keys or subject grouping identifiers.
* **Why it breaks falsifiability:** Standard statistical tests assume independent observations. Treating $20$ subjects as $1000$ independent samples (pseudo-replication) artificially shrinks standard errors by roughly $\sqrt{50} \approx 7\times$. Random subject-level noise produces tiny $p$-values ($p < 0.001$), making almost any false hypothesis appear statistically confirmed and impossible to refute.
* **The DFF fix:** Defining one observational unit per table and enforcing explicit keys ensures that statistical tests use honest degrees of freedom and appropriate hierarchical or clustered error structures.

### 2.4 Resolving Inconsistent Encodings and Missing Metadata

* **The failure mode:** Leaving `"Control"`, `"ctrl"`, and `"0"` unstandardized across batches, or omitting batch, instrument, and protocol metadata.
* **Why it breaks falsifiability:** Unrecorded batch or protocol differences act as hidden confounders. Any observed difference between groups can be attributed to unmeasured batch drift, and any failure to replicate an effect can be blamed on unknown experimental conditions.
* **The DFF fix:** Canonicalizing categorical vocabularies and preserving experimental context metadata locks down the boundary conditions under which a claim is tested.

---

## 3. How Falsifiability Depends on Data Quality and Data Quantity

Falsifiability is tied to both the **quality** and the **amount** of data. In modern statistical inference, these two dimensions govern two different requirements of a valid empirical test:

### 3.1 Data Quality Governs Epistemic Sharpness

Data quality determines **whether the test is measuring what the theory actually predicts**. High-quality metadata, verified provenance, exact units, and explicit missingness codes sharpen the link between theoretical variables and empirical numbers. Without data quality, increasing sample size does not move you closer to truth.

### 3.2 Amount of Data ($N$) Governs Statistical Power and Severe Testing

Unlike deductive logic — where a single black swan falsifies "all swans are white" — empirical science works with noisy measurements and stochastic models. A single noisy outlier neither proves nor refutes a statistical claim. Instead, empirical falsifiability relies on **statistical power** ($1 - \beta$) and **estimation precision**:

* **The Underpowered Trap (Too Little Data):** If sample size $N$ is too small, confidence intervals are wide and statistical power is low. Failing to detect an effect in a small dataset does **not** falsify the hypothesis; it simply means the dataset was too small to distinguish signal from noise. An underpowered study cannot falsify much of anything.
* **Severe Testing:** In statistical philosophy (notably Deborah Mayo's framework of severe testing), a claim is only credibly tested when the test procedure had a **high probability of detecting an error** if the claim were false. Sufficient sample size $N$ provides the resolution needed for a false model to fail cleanly.

### 3.3 Why Quality Must Precede Quantity (The Large-$N$ Trap)

While both quality and quantity matter, they are not interchangeable:

* **Large $N$ with high quality** shrinks random sampling error ($\text{SE} \propto 1/\sqrt{N}$), yielding tight confidence intervals that rigorously test fine-grained predictions.
* **Large $N$ with poor quality** shrinks standard errors around a **biased or corrupted number**. When a dataset has $10,000,000$ rows with an uncleaned sentinel value or pseudo-replicated keys, random noise averages out to zero while systematic data bugs remain — producing extreme statistical certainty ($p \approx 0$) for a completely false conclusion.

In `public-science-harness`, data standards come first because sample size only strengthens falsifiability after the underlying data representation is structurally sound.
