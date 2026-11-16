@author_edphos @author_flow @okr_empirical_modeling
Feature: Empirical Taphonomic Evidentiary Profile
  As a scientific platform engineer or evolutionary paleobiologist
  I require the empirical occurrence and taphonomic data to be characterized by strict structural invariants
  So that model inference operates under the austere reality of the rock record before hypotheses are tested

  Scenario: Frequency Spectrum Reveals Severe Singleton Dominance
    Given an audited Cambrian occurrence database with 1000 total occurrences
    When the occurrence frequency per taxon is profiled
    Then exactly 431 distinct taxa must be identified
    And exactly 249 taxa must appear as singletons with occurrence count 1
    And the singleton proportion must exceed 55 percent of all taxa

  Scenario: Spatial Clustering Confirms Bed Contemporaneity Reality
    Given an audited Cambrian occurrence database with 1000 total occurrences
    When the spatial clustering across collections is evaluated
    Then the occurrences must be distributed across exactly 87 distinct collections
    And at least 5 collections must represent dense Lagerstatte beds with 20 or more taxa

  Scenario: Taphonomic Guild Disparity Confirms Infaunal Body Absence
    Given an audited Cambrian occurrence database with 1000 total occurrences
    When occurrences are partitioned by functional ecological guild
    Then the infaunal burrower guild must contain exactly 5 body occurrences across 4 taxa
    And mobile predators with cuticular hardware must contain over 600 occurrences
    And the taphonomic body disparity ratio between predators and infauna must exceed 100 to 1
