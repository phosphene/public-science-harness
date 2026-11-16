@author_edphos @author_flow @okr_empirical_modeling
Feature: Canonical Conditioned Birth-Death Likelihood Evaluation
  As a scientific platform engineer or evolutionary paleobiologist
  I require continuous-time birth-death likelihoods to be conditioned on Keiding observation probability
  So that unobserved extinct lineages do not artificially inflate extinction estimates and bed contemporaneity is preserved

  Scenario: Exact Joint Likelihood Decomposes into Occurrence, Survival, and Conditioning Terms (PSH-BD-003)
    Given a stratigraphic evaluation receipt containing "Kimberella" with FAD 552.5 Ma and LAD 552.5 Ma
    And candidate latent lifespan boundaries s = 554.0 Ma and e = 550.0 Ma
    And macroevolutionary parameters speciation 0.25, extinction 0.18, and preservation 1.5
    When the conditioned birth-death likelihood evaluator evaluates the cohort
    Then the total conditioned log-likelihood must be finite and negative
    And the Keiding conditioning log-probability must be strictly negative
    And the taxon breakdown must satisfy log L = log L_occ + log L_surv - log P_obs

  Scenario: Boundary Invariant Violation Returns Negative Infinity
    Given a stratigraphic evaluation receipt containing "Kimberella" with FAD 552.5 Ma and LAD 552.5 Ma
    When candidate latent origination s is set to 551.0 Ma which is younger than FAD 552.5 Ma
    Then the total conditioned log-likelihood must be negative infinity
