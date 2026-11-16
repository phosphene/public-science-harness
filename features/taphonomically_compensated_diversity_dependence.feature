@author_edphos @author_flow @okr_empirical_modeling
Feature: Taphonomically Compensated Diversity-Dependence Estimation
  As a scientific platform engineer or evolutionary paleobiologist
  I require macroevolutionary diversity-dependence models to condition on taphonomic preservation tiers
  So that unweighted body fossil counts do not generate artifactual negative speciation slopes for soft-bodied ecosystem engineers

  Background:
    Given a curated Cambrian database containing functional guilds and epistemic annotations
    And the epistemic annotation flags "BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED" for "INFAUNAL_BURROWER"

  Scenario: Unweighted Body Diversity Dependence Fitting is Strictly Forbidden
    When an estimation pipeline attempts to fit unweighted diversity dependence to "INFAUNAL_BURROWER" body counts
    Then the estimator must reject execution with an epistemic warrant violation
    And the violation message must cite DOI "10.1017/S001675689400001X" or "10.18814/epiiugs/1994/v17i1.2/002"
    And the downstream birth-death model state must remain unpolluted

  Scenario: Trace Tiering Depth Calibrates Effective Infaunal Ecological Capacity
    Given an infaunal lineage with 5 observed body occurrences across 4 taxa
    And observed trace tiering depth Z_max = 45.0 mm from the Fortunian stage
    When the taphonomically compensated estimator evaluates the effective standing diversity
    Then the effective ecological capacity N_eff must scale with tiering penetration depth
    And N_eff must exceed the raw body count of 4 taxa by at least a factor of 5.0
    And the resulting diversification slope Gl must reflect substrate ecological volume rather than body preservability

  Scenario: Skeletal Guilds Permit Direct Body Count Diversity Dependence
    When an estimation pipeline evaluates diversity dependence for "SEDENTARY_FILTER_FEEDER"
    Then the estimator must verify calibration status is "OBSERVED_BODY_COUNT_REPRESENTATIVE"
    And the estimator must allow direct body count fitting without tiering penalty
