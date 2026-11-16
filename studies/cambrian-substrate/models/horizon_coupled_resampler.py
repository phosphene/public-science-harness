"""
Horizon-Coupled Stratigraphic Age Resampler.
Implements DEC-PYRATE-002: Groups co-occurring fossil records sharing a unique
geological bed or collection, drawing a single shared stochastic offset u_h per replicate.
Prevents Anti-Pattern 2 (artificial stage smearing and false boundary spikes).
Ref: PyRate Modernization Guide (2026).
"""

from __future__ import annotations

import hashlib
import numpy as np
from pydantic import Field
from phosphene.harness.data.core.vitals import InvariantStatic


class StratigraphicOccurrence(InvariantStatic):
    """Immutable record of a single fossil occurrence with its geological horizon."""
    occurrence_id: str
    taxon_name: str
    horizon_id: str
    age_top_ma: float     # Young boundary
    age_bottom_ma: float  # Old boundary


class ResampledReplicate(InvariantStatic):
    """A single Monte Carlo stratigraphic replicate with preserved contemporaneity."""
    replicate_id: int
    seed: int
    occurrence_ages: dict[str, float]       # occurrence_id -> resampled age (Ma)
    horizon_draws: dict[str, float]         # horizon_id -> u_h in [0, 1]
    sha256_digest: str


class HorizonCoupledResampler:
    """
    Resamples stratigraphic ages while preserving assemblage-level contemporaneity.
    """

    def __init__(self, occurrences: list[StratigraphicOccurrence]):
        if not occurrences:
            raise ValueError("Occurrences list cannot be empty.")
        self.occurrences = occurrences
        
        # Index occurrences by horizon_id to enforce coupling
        self.horizon_map: dict[str, list[StratigraphicOccurrence]] = {}
        self.horizon_bounds: dict[str, tuple[float, float]] = {}
        
        for occ in occurrences:
            hid = occ.horizon_id
            if hid not in self.horizon_map:
                self.horizon_map[hid] = []
                self.horizon_bounds[hid] = (occ.age_top_ma, occ.age_bottom_ma)
            self.horizon_map[hid].append(occ)

    def generate_replicate(self, replicate_id: int, seed: int | None = None) -> ResampledReplicate:
        """
        Draws one random offset u_h ~ Uniform(0, 1) per horizon, then assigns
        tau_i = age_top + u_h * (age_bottom - age_top) to all taxa in that horizon.
        """
        rng = np.random.default_rng(seed if seed is not None else replicate_id)
        
        horizon_draws: dict[str, float] = {}
        occurrence_ages: dict[str, float] = {}
        
        # Sort keys for deterministic hash digest
        for hid in sorted(self.horizon_map.keys()):
            top, bottom = self.horizon_bounds[hid]
            u_h = float(rng.uniform(0.0, 1.0))
            horizon_draws[hid] = round(u_h, 6)
            
            # Coupled age for all occurrences in this horizon
            coupled_age = top + u_h * (bottom - top)
            for occ in self.horizon_map[hid]:
                occurrence_ages[occ.occurrence_id] = round(coupled_age, 4)
                
        # Cryptographic provenance digest
        digest_input = f"{replicate_id}:{seed}:{sorted(occurrence_ages.items())}"
        sha = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
        
        return ResampledReplicate(
            replicate_id=replicate_id,
            seed=seed if seed is not None else replicate_id,
            occurrence_ages=occurrence_ages,
            horizon_draws=horizon_draws,
            sha256_digest=sha,
        )
