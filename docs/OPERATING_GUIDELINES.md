# Platform Team Operating Guidelines: public-science-harness

## 1. Purpose and Mandate

`public-science-harness` is the active engineering and statistical workbench for public science. Working alongside `monograph-review`, this repository shifts the platform team's focus from post-hoc manuscript auditing to building the empirical substrates, instrumented models, and calibration tests required for reproducible normal science.

The platform team does not gate researchers or police their creative intuitions. Instead, we provide production-quality technical execution across five operational areas:

1. Data engineering and dataset standards
2. Model implementation, instrumentation, and claim scoping
3. Running empirical tests with calibration
4. Calibrating models against empirical tests
5. Reporting reproducible baseline and test results

---

## 2. Core Guidelines

### 2.1 Data Engineering and Standards (Data First / DFF)

Empirical inquiry begins with curated, falsifiable datasets before standing up models, taking observations, or testing extensions. (Purely deductive formalisms carry their own distinct rigor requirements, whereas every empirical model requires a verified data substrate first.)

* **Audit Precursor Data and Figures:** Pull the underlying records behind published tables and figures to verify whether reported counts, distributions, and summary curves recompute directly from the released data.
* **Design for Falsifiability (DFF):** Repair missing metadata, resolve inconsistent encodings, distinguish true zeros from missing or censored entries, and document physical units and observational structures before running statistical tests.
* **Standardize Analysis-Ready Outputs:** Keep raw published files immutable and generate clean, rectangular, schema-validated datasets via deterministic transformation scripts so downstream statistical testing is reproducible.

### 2.2 Model Implementation and Instrumentation

Before extending an existing formalism or applying it to a new problem, the platform team must stand up the precursor model under local, namespaced conditions of the giving and taking of reasons.

* **Native-Domain Standup:** Implement and run precursor models and numerical methods on the exact empirical domain they were originally built for, verifying solver convergence, numerical stability, and baseline reproduction.
* **Full Instrumentation:** Expose internal states, parameter bounds, priors, likelihood surfaces, and intermediate diagnostics in clean, observable software rather than treating models as opaque black boxes.

### 2.3 Claim Scoping and Empirical Calibration

A model is only reliable within the boundaries where its assumptions and parameters have been empirically tested and calibrated.

* **Map Exact Claim Boundaries:** Specify precisely what claims a model makes on its native terrain, separating parameters identified directly by empirical data from behavior driven by structural assumptions or priors.
* **Bidirectional Calibration Loop:** Run empirical tests with explicit calibration benchmarks, and calibrate models iteratively against well-characterized test datasets to quantify error, sensitivity, and breakdown regimes.
* **Disclose Analogical Transfer:** Whenever a model is ported by analogy into a new domain, explicitly label the transfer as speculative and disclose its lack of empirical calibration until native tests are established.

### 2.4 Reproducible Result Reporting

If public science is to hold weight for practitioners working in established disciplines, platform outputs must follow the standards of normal science.

* **Transparent Baseline Reporting:** Publish clear, reproducible reports covering dataset audits, baseline figure replications, statistical test outcomes, and calibration curves.
* **Explicit Scope Conditions:** Accompany every reported result with the exact data version, software environment, parameter configuration, and boundary conditions under which the result holds.

---

## 3. Standard Harness Workflow

```text
[1. Published Data & Literature]
 |
 v
[2. Data Engineering & DFF Standards] -> Audit precursor figures; emit clean, typed tables
 |
 v
[3. Model Standup & Instrumentation] -> Reproduce native baseline; expose solver internals
 |
 v
[4. Scoping & Calibration Testing] -> Run empirical tests; calibrate; flag uncalibrated regimes
 |
 v
[5. Public Science Result Report] -> Publish reproducible metrics, limits, and test artifacts
```

---

## 4. Division of Responsibility

* **Researchers** own scientific intuition, hypothesis generation, experimental framing, and deep field-specific hazard knowledge.
* **The Platform Team** owns dataset definition, data curation, numerical modeling, statistical methods, proper model calibration, software instrumentation, and reproducible result reporting.
