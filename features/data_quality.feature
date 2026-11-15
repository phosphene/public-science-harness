@author_edphos @author_flow @okr_DFF
Feature: Empirical Data Quality and Design for Falsifiability
  As a scientific platform engineer or researcher
  I require empirical datasets to enforce strict data hygiene, typed boundaries, and forensic auditing
  So that auxiliary data representation errors are eliminated before model calibration and hypothesis testing

  Background:
    Given a clean data curation context

  Scenario: Distinguishing unobserved nulls from magic sentinels
    Given an upstream raw measurement record with value "-999"
    When the ingestion pipeline cleans the record
    Then the value must be categorized as "magic_sentinel"
    And the cleaned numerical value must be null
    And the sentinel code "-999" must be preserved in provenance metadata

  Scenario: Bounded detection limits are preserved as censored states
    Given an upstream raw measurement record below detection limit with value "< LOD"
    When the ingestion pipeline cleans the record
    Then the value must be categorized as "below_lod"
    And the cleaned numerical value must not be coerced to zero

  Scenario: Auditing bit-boundary clipping and integer overflow artifacts
    Given an upstream integer column "sample_count" containing the value 32767
    When the bit-boundary forensic caliper audits the column
    Then an integer boundary warning for "INT16 (32767)" must be triggered
    And the pipeline must flag potential silent data truncation

  Scenario: Auditing string truncation at schema boundaries
    Given an upstream string column "specimen_code" with declared schema bound 32
    And multiple distinct records have length exactly 32
    When the string truncation forensic caliper audits the column
    Then a string truncation warning must be triggered
    And the diagnostic report must identify an artificial length spike at 32 characters

  Scenario: Detecting Unicode homoglyph injection in taxonomic factors
    Given an upstream taxonomic label "Kimberellа" containing Cyrillic small letter a
    When the homoglyph forensic caliper audits the string
    Then a homoglyph risk must be detected
    And the detected scripts must include both "LATIN" and "CYRILLIC"

  Scenario: Scaling univariate outlier fences to sample size N
    Given an empirical dataset with 15000 observations
    When the sample-scaled outlier engine evaluates column "metabolic_rate"
    Then the effective sigma threshold must scale to 4.0
    And observations between 3.0 and 4.0 sigma must not be discarded as anomalies

  Scenario: Evaluating cross-column multivariate domain invariants
    Given a stratigraphic horizon record with bottom age 500.0 Ma and top age 515.0 Ma
    When the multivariate domain invariants engine evaluates temporal monotonicity
    Then a domain invariant violation must be raised
    And the violation message must indicate that bottom age is less than top age

  Scenario: Compiling SQLite strict DDL to eliminate type affinity loopholes
    Given a table definition for "curated_stratigraphy" with strict columns and checks
    When the DDL compiler generates the SQL schema
    Then the output DDL must include the "STRICT;" table modifier
    And type affinity coercion must be strictly forbidden
