@author_edphos @author_flow @okr_DFF
Feature: Transforms Provenance and Epistemic Annotation Standards
  As a scientific platform engineer or evolutionary researcher
  I require all data transformations to declare versioned rulesets and cryptographic provenance receipts
  And I require domain calibrations to be recorded as typed epistemic annotations
  So that auxiliary data transformations and taphonomic corrections are fully addressable and falsifiable

  Background:
    Given a clean data curation context

  Scenario: Declaring versioned transformation specifications
    Given a raw input dataset "stratigraphic_horizons_raw.csv" with 6 records
    When the transformation engine compiles spec "TR-CAMBRIAN-001" under category "isomorphic_hygiene"
    Then the transform specification must enforce pre-conditions and post-conditions
    And the transform must be recorded as version "1.0.0"

  Scenario: Emitting a machine-verifiable dataset provenance receipt
    Given input artifacts "stratigraphic_horizons_raw.csv" and "pbdb_cambrian_metazoa_raw.json"
    And an executed pipeline "pipelines/03_calibrate_infaunal_diversity.py"
    When the pipeline completes execution and builds the curated database
    Then a cryptographic provenance receipt must be emitted
    And the receipt must capture SHA-256 hashes of all input and output artifacts
    And the receipt must link the active git commit SHA

  Scenario: Recording typed epistemic annotations for taphonomic bias
    Given an empirical guild "INFAUNAL_BURROWER" with sampling ratio below 2.0
    When the calibration engine registers an epistemic annotation
    Then the judgment type must be "calibration_override"
    And the epistemic warrant must cite DOI "10.1017/S001675689400001X"
    And the annotation must flag "BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED"
    And downstream unweighted body fossil diversity-dependence fitting must be forbidden
