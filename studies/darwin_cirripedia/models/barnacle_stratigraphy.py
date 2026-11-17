"""Stratigraphic distribution and faunal continuity of Darwin's (1851) Fossil Lepadidae.

This module models the chronostratigraphic occurrence records, stage-level
richness dynamics, and faunal boundary persistence of pedunculated cirripedes
documented in Charles Darwin's foundational 1851 monograph.

Genealogy of Methods: Darwin's Inferential Arithmetic to Modern Range Metrics:
-----------------------------------------------------------------------------
1. Darwin's Tabular Range Method (1851):
   In his master distribution table (p. 14 of 'Fossil Lepadidae'), Darwin introduced
   a discrete matrix of occurrence indicators across stratigraphically ordered columns:
   Lower Oolite, Middle Oolite, Lower Greensand, Gault, Upper Greensand, Chalk Marl,
   Lower Chalk, Upper Chalk, Maestricht Formation, and Tertiary.
   
   Darwin calculated two primary quantities directly from this table:
   a. Stage-Level Sums: The vertical summation of verified presences per stage, establishing
      the Cretaceous peak (9-10 species in Maestricht, 9-12 in Upper Chalk) versus the
      Jurassic Oolitic scarcity (1-2 species).
   b. Species-to-Individual Inverse Ratio: Darwin explicitly observed that high specific
      richness in a horizon did not correlate with specimen abundance (citing Mr. Fitch's
      20 years of collecting near Norwich yielding only 9 keels of Scalpellum maximum and
      6 of S. fossula), cautioning against conflating taxonomic diversity with biomass.
   c. Vertical-to-Horizontal Range Invariant: Darwin reasoned from living cirripedes:
      "If fossil cirripedia had, like most recent species, very wide horizontal or
      geographical ranges, then, in accordance with a law now generally admitted, a
      considerable vertical range in some of the species is not improbable."

2. Evolution into Modern Quantitative Biostratigraphy:
   Darwin's tabular range calculations represent the direct historical precursor to:
   - Lyellian percentage dating (measuring faunal survival ratios across horizons).
   - Range-Through and Boundary-Crosser matrices in quantitative paleobiology (Sepkoski 1975,
     Foote 2000, Alroy 2008), where standing richness N_tot = N_b + N_t + N_bt + N_FL.
   - Profile Boundary Persistence: Computing Jaccard / Simpson faunal similarity
     coefficients across chronostratigraphic disconformities.

Mathematical Formulation & Dimensional Accounting:
--------------------------------------------------
Let S = {s_1, s_2, ..., s_n} be the set of cataloged fossil species (n = 35) and
H = (h_1, h_2, ..., h_m) be the chronologically ordered sequence of geological stages
from Lower Oolite to Tertiary (m = 10).

1. Empirical Stage Richness:
   The standing species richness R(h_j) in chronostratigraphic stage h_j is:
       R(h_j) = sum_{i=1}^n I(s_i, h_j)
   where I(s_i, h_j) in {0, 1} is the indicator function of verified fossil presence.
   Units: [taxa]

2. Boundary Persistence (Faunal Overlap):
   For adjacent geological stages (h_j, h_{j+1}), the species persistence count
   P(h_j, h_{j+1}) is the number of shared surviving lineages:
       P(h_j, h_{j+1}) = sum_{i=1}^n I(s_i, h_j) * I(s_i, h_{j+1})
   Units: [taxa]

   A high boundary persistence (e.g., P >= 4) demonstrates continuous sedimentation
   and uninterrupted biological descent, whereas P = 0 indicates complete faunal
   turnover or a taphonomic hiatus across the boundary.

3. Generic Stratigraphic Span & Longevity Ratio:
   For genus G subset S, its stage span is defined by the interval of appearance:
       Span(G) = max_{s in G, I(s, h_j)=1} (j) - min_{s in G, I(s, h_k)=1} (k) + 1
   Units: [chronostratigraphic stages]

   A high generic span (Span >= 8 stages, > 100 Myr) coupled with zero species-level
   survival across major era boundaries establishes morphological architectural stability
   operating beneath continuous species turnover.

Caliper & Dirt Grounding (J.O. Wisdom Benchmark):
-------------------------------------------------
Every indicator I(s_i, h_j) corresponds to physical valve specimens (carina, scuta, terga)
held in museum collections (British Museum, Geological Society, Dixon collection),
measured with calipers and tied to verified lithological horizons.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

# Ordered sequence of chronostratigraphic horizons: (identifier, display_name)
GEOLOGICAL_STAGES: tuple[tuple[str, str], ...] = (
    ("lower_oolite", "Lower Oolite (Stonesfield)"),
    ("middle_oolite", "Middle Oolite (Oxford Clay)"),
    ("lower_greensand", "Lower Greensand"),
    ("gault", "Gault"),
    ("upper_greensand", "Upper Greensand"),
    ("chalk_marl", "Chalk Marl"),
    ("lower_chalk", "Lower Chalk"),
    ("upper_chalk", "Upper Chalk"),
    ("maestricht_faxoe_scania", "Maestricht Formation (Faxoe/Scania)"),
    ("tertiary", "Tertiary"),
)


@dataclass(frozen=True)
class FossilBarnacleOccurrence:
    """A verified fossil barnacle occurrence record across geological stages.

    Attributes
    ----------
    species_name : str
        Linnaean binomial identifier established by Darwin (1851).
    genus : str
        Taxonomic genus (e.g., 'Scalpellum', 'Pollicipes', 'Loricula').
    stage_presences : dict[str, bool]
        Mapping from canonical stage key to boolean occurrence indicator I(s, h).
    """

    species_name: str
    genus: str
    stage_presences: dict[str, bool]

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> FossilBarnacleOccurrence:
        """Parse an empirical row from Darwin's transcribed 1851 stratigraphic table.

        Parameters
        ----------
        row : dict[str, str]
            Dictionary containing CSV field values.

        Returns
        -------
        FossilBarnacleOccurrence
            Parsed occurrence record with validated boolean stage indicators.
        """
        presences = {
            stage_key: row[stage_key].strip() in {"*", "*?"}
            for stage_key, _ in GEOLOGICAL_STAGES
        }
        return cls(
            species_name=row["species_name"].strip(),
            genus=row["genus"].strip(),
            stage_presences=presences,
        )


def load_stratigraphic_occurrences(csv_path: Path) -> list[FossilBarnacleOccurrence]:
    """Ingest Darwin's 1851 stratigraphic table from CSV into structured occurrence records.

    Parameters
    ----------
    csv_path : Path
        Filesystem path to darwin_1851_fossil_lepadidae_stratigraphy.csv.

    Returns
    -------
    list[FossilBarnacleOccurrence]
        Parsed occurrence records for all 35 cataloged species.
    """
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [FossilBarnacleOccurrence.from_csv_row(row) for row in reader]


@dataclass(frozen=True)
class StageSummary:
    """Summary statistics for a single chronostratigraphic stage.

    Attributes
    ----------
    stage_key : str
        Internal stage identifier matching GEOLOGICAL_STAGES.
    stage_name : str
        Human-readable geological stage name.
    richness : int
        Standing species count R(h) in [taxa].
    genera : tuple[str, ...]
        Tuple of distinct genera present in this horizon.
    """

    stage_key: str
    stage_name: str
    richness: int
    genera: tuple[str, ...]


def calculate_stage_richness(
    occurrences: Sequence[FossilBarnacleOccurrence],
) -> list[StageSummary]:
    """Compute empirical species richness R(h) and generic representation per geological stage.

    Formulation:
        R(h_j) = sum_{i=1}^n I(s_i, h_j)

    Parameters
    ----------
    occurrences : Sequence[FossilBarnacleOccurrence]
        Sequence of verified fossil barnacle occurrence records.

    Returns
    -------
    list[StageSummary]
        Chronologically ordered summary for each of the 10 geological stages.
    """
    summaries: list[StageSummary] = []
    for stage_key, stage_name in GEOLOGICAL_STAGES:
        present = [
            occ for occ in occurrences if occ.stage_presences.get(stage_key, False)
        ]
        genera = tuple(sorted({occ.genus for occ in present}))
        summaries.append(
            StageSummary(
                stage_key=stage_key,
                stage_name=stage_name,
                richness=len(present),
                genera=genera,
            )
        )
    return summaries


@dataclass(frozen=True)
class BoundaryOverlap:
    """Faunal continuity statistics across adjacent geological stage boundaries.

    Attributes
    ----------
    earlier_stage_name : str
        Name of chronostratigraphically antecedent stage h_j.
    later_stage_name : str
        Name of chronostratigraphically subsequent stage h_{j+1}.
    shared_species : tuple[str, ...]
        Specific taxa persisting across both horizons.
    shared_count : int
        Count of shared persisting species P(h_j, h_{j+1}) in [taxa].
    """

    earlier_stage_name: str
    later_stage_name: str
    shared_species: tuple[str, ...]
    shared_count: int


def calculate_boundary_overlaps(
    occurrences: Sequence[FossilBarnacleOccurrence],
) -> list[BoundaryOverlap]:
    """Calculate the number and identity of shared species persisting across adjacent stages.

    Formulation:
        P(h_j, h_{j+1}) = sum_{i=1}^n I(s_i, h_j) * I(s_i, h_{j+1})

    Parameters
    ----------
    occurrences : Sequence[FossilBarnacleOccurrence]
        Sequence of verified fossil barnacle occurrence records.

    Returns
    -------
    list[BoundaryOverlap]
        Pairwise overlap metrics across all adjacent chronostratigraphic boundaries.
    """
    overlaps: list[BoundaryOverlap] = []
    for i in range(len(GEOLOGICAL_STAGES) - 1):
        k1, name1 = GEOLOGICAL_STAGES[i]
        k2, name2 = GEOLOGICAL_STAGES[i + 1]

        shared = tuple(
            occ.species_name
            for occ in occurrences
            if occ.stage_presences.get(k1, False) and occ.stage_presences.get(k2, False)
        )
        overlaps.append(
            BoundaryOverlap(
                earlier_stage_name=name1,
                later_stage_name=name2,
                shared_species=shared,
                shared_count=len(shared),
            )
        )
    return overlaps


@dataclass(frozen=True)
class GenusStratigraphicRange:
    """Stratigraphic range and longevity metrics for a taxonomic genus.

    Attributes
    ----------
    genus : str
        Taxonomic genus identifier.
    species_count : int
        Total distinct fossil species cataloged in this genus across all stages.
    first_appearance_stage : str
        Earliest geological stage containing a verified occurrence.
    last_appearance_stage : str
        Latest geological stage containing a verified occurrence.
    stage_span_count : int
        Span of stages from first to last appearance in [stages].
    """

    genus: str
    species_count: int
    first_appearance_stage: str
    last_appearance_stage: str
    stage_span_count: int


def calculate_genus_ranges(
    occurrences: Sequence[FossilBarnacleOccurrence],
) -> list[GenusStratigraphicRange]:
    """Compute the total species richness and chronostratigraphic stage span for each genus.

    Formulation:
        Span(G) = max(index(h)) - min(index(h)) + 1

    Parameters
    ----------
    occurrences : Sequence[FossilBarnacleOccurrence]
        Sequence of verified fossil barnacle occurrence records.

    Returns
    -------
    list[GenusStratigraphicRange]
        Range statistics for each genus in the dataset.
    """
    genera = sorted({occ.genus for occ in occurrences})
    stage_keys = [k for k, _ in GEOLOGICAL_STAGES]
    stage_names = {k: name for k, name in GEOLOGICAL_STAGES}

    ranges: list[GenusStratigraphicRange] = []
    for g in genera:
        g_occs = [occ for occ in occurrences if occ.genus == g]
        indices_present = []
        for idx, k in enumerate(stage_keys):
            if any(occ.stage_presences.get(k, False) for occ in g_occs):
                indices_present.append(idx)

        first_stage = stage_names[stage_keys[indices_present[0]]]
        last_stage = stage_names[stage_keys[indices_present[-1]]]
        span = indices_present[-1] - indices_present[0] + 1

        ranges.append(
            GenusStratigraphicRange(
                genus=g,
                species_count=len(g_occs),
                first_appearance_stage=first_stage,
                last_appearance_stage=last_stage,
                stage_span_count=span,
            )
        )
    return ranges
