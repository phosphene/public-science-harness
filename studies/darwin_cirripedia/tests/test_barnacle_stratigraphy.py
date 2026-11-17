"""Tests for Darwin (1851) Fossil Lepadidae stratigraphic range analysis."""

from __future__ import annotations

from pathlib import Path
import pytest

from studies.darwin_cirripedia.models.barnacle_stratigraphy import (
    calculate_boundary_overlaps,
    calculate_genus_ranges,
    calculate_stage_richness,
    load_stratigraphic_occurrences,
)

CSV_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "raw"
    / "darwin_1851_fossil_lepadidae_stratigraphy.csv"
)


def test_load_stratigraphic_occurrences():
    """Verify loading of Darwin's 1851 table produces expected counts and genera."""
    assert CSV_PATH.exists(), f"Missing CSV at {CSV_PATH}"
    occurrences = load_stratigraphic_occurrences(CSV_PATH)

    assert len(occurrences) == 35
    genera = {occ.genus for occ in occurrences}
    assert genera == {"Scalpellum", "Pollicipes", "Loricula"}


def test_calculate_stage_richness():
    """Verify stage richness reproduces Jurassic scarcity and Cretaceous peak."""
    occurrences = load_stratigraphic_occurrences(CSV_PATH)
    summaries = calculate_stage_richness(occurrences)

    richness_map = {s.stage_name: s.richness for s in summaries}

    # Oolite scarcity
    assert richness_map["Lower Oolite (Stonesfield)"] == 1
    assert richness_map["Middle Oolite (Oxford Clay)"] == 2

    # Cretaceous peak
    assert richness_map["Upper Chalk"] == 11
    assert richness_map["Maestricht Formation (Faxoe/Scania)"] == 11


def test_calculate_boundary_overlaps():
    """Verify boundary persistence across chalk stages and disconformity at Tertiary."""
    occurrences = load_stratigraphic_occurrences(CSV_PATH)
    overlaps = calculate_boundary_overlaps(occurrences)

    overlap_map = {
        (o.earlier_stage_name, o.later_stage_name): o.shared_count for o in overlaps
    }

    # Overlap within chalk series
    assert (
        overlap_map[("Upper Chalk", "Maestricht Formation (Faxoe/Scania)")] == 6
    )
    assert overlap_map[("Lower Chalk", "Upper Chalk")] == 4

    # Disconformity / no species survival into Tertiary
    assert (
        overlap_map[("Maestricht Formation (Faxoe/Scania)", "Tertiary")] == 0
    )


def test_calculate_genus_ranges():
    """Verify generic longevity across stages."""
    occurrences = load_stratigraphic_occurrences(CSV_PATH)
    ranges = calculate_genus_ranges(occurrences)

    range_map = {r.genus: r for r in ranges}

    # Pollicipes spans from Lower Oolite through Maestricht
    pollicipes = range_map["Pollicipes"]
    assert pollicipes.first_appearance_stage == "Lower Oolite (Stonesfield)"
    assert pollicipes.species_count >= 20

    # Scalpellum spans from Lower Greensand to Tertiary
    scalpellum = range_map["Scalpellum"]
    assert scalpellum.first_appearance_stage == "Lower Greensand"
    assert scalpellum.last_appearance_stage == "Tertiary"
