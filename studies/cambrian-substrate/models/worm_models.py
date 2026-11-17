"""Standing up Darwin's (1881) Earthworm Accretion Model alongside
the Ancient Worm / Cambrian Agronomic Revolution Bioturbation Model.

Implements:
1. Darwin's 1881 Physical Model of Vegetable Mould Formation:
   - Population density (Hensen census)
   - Empirical casting weight to tonnage per acre
   - Volumetric displacement and compaction correction
   - Long-term decadal burial accretion
2. The Ancient Trace Fossil / Cambrian Agronomic Revolution Model:
   - Droser & Bottjer (1986) / Seilacher (1999) Bioturbation Index (BI 1 to 6)
   - Transition from Ediacaran matgrounds to Cambrian mixgrounds
   - Mathematical comparison: Upward accretion vs downward biological mixing (biodiffusion)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class DarwinWormExperiment:
    """A single field experiment recorded in Darwin (1881, Chapter III)."""

    site_name: str
    sample_area_sq_yards: float
    duration_days: float
    measured_weight_lbs: float
    normalized_annual_lbs_per_sq_yd: float
    calculated_tons_per_acre: float  # In long tons (2240 lbs)
    measured_volume_cu_in: float | None = None
    annual_thickness_inches: float | None = None
    decadal_thickness_inches: float | None = None


# Darwin's exact experimental measurements from Chapter III (pp. 161-171)
DARWIN_1881_EXPERIMENTS: list[DarwinWormExperiment] = [
    DarwinWormExperiment(
        site_name="Dr. King, Nice (France)",
        sample_area_sq_yards=1.0 / 9.0,  # 1 square foot
        duration_days=365.0,
        measured_weight_lbs=0.75,  # 12 oz
        normalized_annual_lbs_per_sq_yd=6.75,
        calculated_tons_per_acre=14.58,
        measured_volume_cu_in=None,
        annual_thickness_inches=None,
        decadal_thickness_inches=None,
    ),
    DarwinWormExperiment(
        site_name="Valley in the Chalk (Down pasture)",
        sample_area_sq_yards=1.0,
        duration_days=45.0,  # Rolled 52 days prior; dry last 2-3 weeks
        measured_weight_lbs=1.84375,  # 1 lb 13.5 oz
        normalized_annual_lbs_per_sq_yd=8.387,  # Extrapolated over active season
        calculated_tons_per_acre=18.12,
        measured_volume_cu_in=None,
        annual_thickness_inches=None,
        decadal_thickness_inches=None,
    ),
    DarwinWormExperiment(
        site_name="Leith Hill Place (Old terrace)",
        sample_area_sq_yards=1.0,
        duration_days=369.0,
        measured_weight_lbs=3.479,
        normalized_annual_lbs_per_sq_yd=3.479,
        calculated_tons_per_acre=7.56,
        measured_volume_cu_in=124.77,
        annual_thickness_inches=0.090,  # Corrected for 1/16 compaction
        decadal_thickness_inches=0.90,
    ),
    DarwinWormExperiment(
        site_name="Leith Hill Common (Sandy heath)",
        sample_area_sq_yards=1.0,
        duration_days=367.0,
        measured_weight_lbs=7.453,
        normalized_annual_lbs_per_sq_yd=7.453,  # Darwin computed direct on 7.453 lbs
        calculated_tons_per_acre=16.10,
        measured_volume_cu_in=197.56,
        annual_thickness_inches=0.1429,  # Corrected for 1/16 compaction
        decadal_thickness_inches=1.429,
    ),
]


def evaluate_darwin_mould_model(
    annual_weight_lbs_per_sq_yd: float,
    measured_volume_cu_in_per_sq_yd: float | None = None,
    compaction_factor: float = 0.9375,  # 15/16 factor for field moisture and root compaction
) -> dict[str, float]:
    """Execute Darwin's exact mathematical equations for soil turnover and vertical accretion.

    Constants:
        1 square yard = 1,296 square inches.
        1 acre = 4,840 square yards = 6,272,640 square inches.
        1 long ton = 2,240 pounds.
    """
    total_lbs_acre = annual_weight_lbs_per_sq_yd * 4840.0
    long_tons_acre = total_lbs_acre / 2240.0

    if measured_volume_cu_in_per_sq_yd is not None:
        volume_per_sq_yd = measured_volume_cu_in_per_sq_yd
    else:
        # Default density from Leith Hill Common (7.453 lbs / 197.56 in^3)
        density = 7.453 / 197.56
        volume_per_sq_yd = annual_weight_lbs_per_sq_yd / density

    # Uncorrected layer thickness on 1 sq yard (1296 sq inches)
    uncorrected_annual_inches = volume_per_sq_yd / 1296.0

    # Compaction-corrected annual thickness (deduct 1/16)
    corrected_annual_inches = uncorrected_annual_inches * compaction_factor
    decadal_inches = corrected_annual_inches * 10.0
    century_inches = corrected_annual_inches * 100.0

    return {
        "tons_per_acre_year": round(long_tons_acre, 2),
        "uncorrected_annual_inches": round(uncorrected_annual_inches, 4),
        "corrected_annual_inches": round(corrected_annual_inches, 4),
        "decadal_accretion_inches": round(decadal_inches, 3),
        "century_accretion_inches": round(century_inches, 2),
    }


@dataclass(frozen=True)
class AncientBioturbationTier:
    """Ichnological tier and bioturbation metrics for ancient marine burrowers (Droser & Bottjer 1986)."""

    geological_epoch: str
    dominant_tracemakers: str
    burrowing_depth_cm: float  # Vertical penetration below sediment-water interface
    bioturbation_index: int  # BI 1 to 6 (Droser & Bottjer 1986)
    percentage_fabric_disturbed: tuple[float, float]
    sedimentary_mode: str  # "matground" vs "mixground"
    mechanical_action: str


ANCIENT_WORM_CHRONOSEQUENCE: list[AncientBioturbationTier] = [
    AncientBioturbationTier(
        geological_epoch="Late Ediacaran (550 Ma)",
        dominant_tracemakers="Primitive bilaterian grazers (e.g. Helminthoidichnites)",
        burrowing_depth_cm=0.2,  # Strictly surficial, 1-2 mm
        bioturbation_index=1,
        percentage_fabric_disturbed=(0.0, 0.0),
        sedimentary_mode="Matground (Microbial mat seal)",
        mechanical_action="Undermat mining; strictly two-dimensional bed skimming.",
    ),
    AncientBioturbationTier(
        geological_epoch="Basal Cambrian / Fortunian (535 Ma)",
        dominant_tracemakers="Treptichnus pedum (priapulid/annelid probe burrowers)",
        burrowing_depth_cm=3.0,  # Shallow three-dimensional penetration
        bioturbation_index=2,
        percentage_fabric_disturbed=(1.0, 10.0),
        sedimentary_mode="Early Mixground transition",
        mechanical_action="Probing branching tunnels; tearing microbial mat seal.",
    ),
    AncientBioturbationTier(
        geological_epoch="Cambrian Stage 3 / Series 2 (515 Ma)",
        dominant_tracemakers="Skolithos, Arenicolites, Diplocraterion (vertical pipe-rock)",
        burrowing_depth_cm=30.0,  # Deep vertical colonization
        bioturbation_index=5,
        percentage_fabric_disturbed=(60.0, 100.0),
        sedimentary_mode="True Mixground (Agronomic Revolution)",
        mechanical_action="Pervasive vertical bioturbation; complete homogenization of primary lamination.",
    ),
]


def compare_darwin_and_ancient_worm_models() -> dict[str, str]:
    """Formal mathematical and physical comparison of Darwin's worms vs Ancient trace worms."""
    return {
        "directional_vector": (
            "Darwin's earthworms deposit castings UPWARD onto the surface, creating positive "
            "vertical accretion (topsoil accretion at 1.0-1.5 inches/decade). Ancient marine worms "
            "burrow DOWNWARD into laminated sea floor, destroying primary stratification."
        ),
        "physical_preservation": (
            "Darwin's model is confirmed by buried physical objects (lime, cinders, Roman ruins) "
            "sinking into the homogenous mould. Ancient worm activity is confirmed by fossil ichnofabrics "
            "(Treptichnus branching tunnels and Skolithos vertical tubes preserved in quartzite)."
        ),
        "ecological_carrying_capacity": (
            "In Darwin's pasture, 53,767 worms/acre consume rotting organic matter under tight spatial "
            "crowding (burrows touching). In the Cambrian Agronomic Revolution, worms physically broke "
            "the microbial mat barrier, ventilating the upper 30 cm of ocean sediment and opening 3D ecospace."
        ),
    }
