@author_edphos @author_flow @okr_empirical_modeling
Feature: Stratigraphically Coupled Lineage Horizon Lifespan Evaluation
  As a scientific platform engineer or evolutionary paleobiologist
  I require fossil occurrences to be aggregated into lineage lifespans under coupled horizon projections
  So that bed contemporaneity is mathematically preserved and soft-bodied trace burrowers are explicitly represented

  Scenario: Lineage Observation Envelopes Obey Stratigraphic Invariants (PSH-BD-002)
    Given 3 fossil occurrences for taxon "Kimberella" from horizon "HZ_WHITE_SEA" spanning 550.0 to 555.0 Ma
    And 2 fossil occurrences for taxon "Dickinsonia" from the same horizon "HZ_WHITE_SEA"
    When the lineage horizon evaluator generates a coupled realization
    Then the FAD of "Kimberella" must exactly equal the FAD of "Dickinsonia"
    And the LAD of "Kimberella" must equal its FAD with observed duration 0.0 Myr
    And both taxa must be recorded in horizon "HZ_WHITE_SEA"

  Scenario: Trace Channel Isolation Preserves Early Worms Without Shells
    Given an ichnological trace occurrence "tr_01" for "Treptichnus_pedum" in horizon "HZ_FORTUNIAN_01" with burrow depth 35.0 mm
    And an ichnological trace occurrence "tr_02" for "Treptichnus_pedum" in horizon "HZ_FORTUNIAN_02" with burrow depth 45.0 mm
    When the lineage horizon evaluator generates a coupled realization
    Then taxon "Treptichnus_pedum" must have body occurrence count 0
    And taxon "Treptichnus_pedum" must have trace occurrence count 2
    And the maximum burrow depth for "Treptichnus_pedum" must be 45.0 mm
    And its observed duration must be greater than or equal to 0.0 Myr
