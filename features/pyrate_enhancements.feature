@author_edphos @author_flow @okr_empirical_modeling
Feature: PyRate Methodological Enhancements and Decision Provenance
  As a scientific platform engineer or evolutionary paleobiologist
  I require macroevolutionary rate models to enforce horizon coupling and regime-matched preservation
  So that stratigraphic smearing, false boundary spikes, and taphonomic ridges are eliminated

  Scenario: Horizon-Coupled Age Resampling Retains Bed Contemporaneity (DEC-PYRATE-002)
    Given 5 fossil occurrences recovered from the same geological horizon "HZ_CHENGJIANG_BED"
    And the horizon spans chronostratigraphic bounds 518.0 to 521.0 Ma
    When Monte Carlo age resampling is performed with horizon coupling enabled
    Then all 5 occurrences must receive the identical resampled age
    And the resampled age must fall strictly within 518.0 and 521.0 Ma
    And a deterministic SHA-256 provenance digest must be emitted

  Scenario: Taphonomic Hazard Detection and Infaunal Tiering Override (DEC-PYRATE-005)
    Given an empirical occurrence database with 5 infaunal body occurrences and 634 predator occurrences
    When the guild diversity calibration pipeline evaluates taphonomic preservation tiers
    Then the infaunal guild must be flagged with status "BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED"
    And naive unweighted body-count diversity-dependence fitting must be strictly blocked
    And the epistemic warrant must cite DOI "10.1017/S001675689400001X"
