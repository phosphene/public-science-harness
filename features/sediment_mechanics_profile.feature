@author_edphos @author_flow @okr_empirical_modeling
Feature: Empirical Sediment Mechanics and Diagenetic Substrate Bounding
  As a scientific platform engineer or evolutionary paleobiologist
  I require the sediment physical boundaries, diagenetic diffusion, and tiering mechanics to be explicitly bounded
  So that model ingress cannot invent soft-bodied biomass without honoring sedimentological conservation laws

  Scenario: Microbial Matground Restricts Bioturbation to Surface Envelopes
    Given a Terminal Ediacaran matground with tiering depth 2.0 mm and biological mixing 0.0 mm2/yr
    When biodiffusion is evaluated at depth 1.5 mm
    Then the biodiffusion coefficient must be 0.0 mm2/yr
    And the oxygen penetration depth must remain strictly confined to under 20.0 mm

  Scenario: Fortunian Infaunal Bioturbation Expands Aerobic Sedimentary Niche
    Given a Fortunian substrate horizon with tiering depth 35.0 mm and biological mixing 15.0 mm2/yr
    When the coupled diagenetic steady state is evaluated
    Then the oxygen penetration depth must exceed that of the Ediacaran baseline
    And the aerobic niche capacity must expand by more than a factor of 2.0
    And biodiffusion below the tier depth 35.0 mm must decay smoothly toward zero

  Scenario: Ichnofabric Tier Monotonicity Obays Stratigraphic Invariants
    Given the 4 discrete physical sediment tiers: mat, undermat, vertical, and deep
    When their characteristic tier penetration depths are ordered
    Then tier depth must increase strictly monotonically from 2.0 mm to 80.0 mm
