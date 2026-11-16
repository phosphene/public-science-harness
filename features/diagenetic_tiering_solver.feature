@author_edphos @author_flow @okr_empirical_modeling
Feature: Physical Diagenetic Tiering and Agronomic Substrate Dynamics
  As a scientific platform engineer or evolutionary paleobiologist
  I require a numerically stable 1D coupled reaction-diffusion diagenetic solver
  So that the transition from planar mat-grazing to 3D infaunal tiering is quantified with physical invariants

  Scenario: Ediacaran Planar Baseline Restricts Aerobic Niche Volume
    Given an undisturbed Ediacaran sediment profile with mat tiering depth 1.5 mm
    When the diagenetic steady state is solved with surface bottom water O2 250 umol
    Then the steady state oxygen penetration depth must be less than or equal to 20.0 mm
    And the aerobic niche capacity must be bounded by planar boundary limits

  Scenario: Fortunian Treptichnus Ingress Expands 3D Infaunal Niche
    Given a Fortunian bioturbated sediment profile with tiering depth 35.0 mm
    When the diagenetic steady state is solved with biodiffusion coefficient 60.0 mm2/yr
    Then the steady state oxygen penetration depth must exceed the Ediacaran baseline by at least 1.5 times
    And the aerobic niche capacity must expand by at least 1.4 times over the Ediacaran baseline

  Scenario: Solver Convergence and Mass Conservation Invariants
    Given a continuous depth domain from 0 to 100 mm with 101 spatial grid nodes
    When the coupled BDF integrator solves the sediment advection-diffusion-reaction equations
    Then the solver must achieve numerical convergence with solver_success true
    And all reconstructed concentrations of O2 and C_org must be non-negative across the entire column
