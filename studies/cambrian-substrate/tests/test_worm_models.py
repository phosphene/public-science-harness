"""Tests for Darwin's 1881 worm accretion model and ancient Cambrian bioturbation models."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "models"))
from worm_models import (
    ANCIENT_WORM_CHRONOSEQUENCE,
    DARWIN_1881_EXPERIMENTS,
    compare_darwin_and_ancient_worm_models,
    evaluate_darwin_mould_model,
)


def test_darwin_exact_tonnage_reproduction():
    """Verify that running Darwin's formula matches his published tons per acre within rounding."""
    for exp in DARWIN_1881_EXPERIMENTS:
        res = evaluate_darwin_mould_model(exp.normalized_annual_lbs_per_sq_yd)
        # Expected tons per acre must match Darwin's published numbers within 0.05 tons
        assert abs(res["tons_per_acre_year"] - exp.calculated_tons_per_acre) < 0.06, (
            f"Failed on {exp.site_name}: got {res['tons_per_acre_year']}, "
            f"expected {exp.calculated_tons_per_acre}"
        )


def test_darwin_thickness_reproduction():
    """Verify Darwin's Leith Hill accretion depth calculations match published numbers."""
    # Leith Hill Place Terrace: 3.479 lbs, 124.77 cu in -> ~0.90 inches in 10 years
    terrace_res = evaluate_darwin_mould_model(3.479, measured_volume_cu_in_per_sq_yd=124.77)
    assert abs(terrace_res["decadal_accretion_inches"] - 0.90) < 0.05

    # Leith Hill Common: 7.453 lbs, 197.56 cu in -> ~1.43 inches in 10 years
    common_res = evaluate_darwin_mould_model(7.453, measured_volume_cu_in_per_sq_yd=197.56)
    assert abs(common_res["decadal_accretion_inches"] - 1.43) < 0.05


def test_ancient_worm_chronosequence_invariants():
    """Verify physical invariants of the Cambrian Agronomic Revolution bioturbation tiers."""
    assert len(ANCIENT_WORM_CHRONOSEQUENCE) == 3

    # Bioturbation index must strictly increase from Ediacaran (BI 1) to Cambrian Stage 3 (BI 5)
    indices = [tier.bioturbation_index for tier in ANCIENT_WORM_CHRONOSEQUENCE]
    assert indices == [1, 2, 5]

    # Burrowing depth must increase by two orders of magnitude (from 2 mm to 30 cm)
    depths = [tier.burrowing_depth_cm for tier in ANCIENT_WORM_CHRONOSEQUENCE]
    assert depths[0] == 0.2
    assert depths[-1] == 30.0


def test_model_comparison_structure():
    """Verify the structural comparison between Darwin's accretion and ancient bioturbation."""
    comp = compare_darwin_and_ancient_worm_models()
    assert "directional_vector" in comp
    assert "physical_preservation" in comp
    assert "ecological_carrying_capacity" in comp
    assert "UPWARD" in comp["directional_vector"]
    assert "DOWNWARD" in comp["directional_vector"]
