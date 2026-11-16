"""
Stratigraphically Coupled Lineage Horizon Lifespan Evaluator.
Implements PSH-BD-002 and DEC-PYRATE-002: Evaluates taxon observation spans
(FAD, LAD, occurrence channels) while strictly preserving bed contemporaneity.
Ref: Kendall (1948), Keiding (1975), Signor & Lipps (1982), Marshall (1990).
"""

from __future__ import annotations

import hashlib
from typing import Dict, List, Sequence
import numpy as np
from pydantic import Field

from phosphene.harness.data.core.vitals import InvariantStatic
from horizon_coupled_resampler import HorizonCoupledResampler, StratigraphicOccurrence


class ObservationalChannel(InvariantStatic):
    """Counts and physical metrics per observation modality."""
    body_occurrence_count: int
    trace_occurrence_count: int
    max_burrow_depth_mm: float
    lithologies: list[str]


class LineageObservationEnvelope(InvariantStatic):
    """
    Evaluated observation envelope for a single taxon under a specific stratigraphic realization.
    """
    taxon_name: str
    fad_ma: float                       # First Appearance Datum (oldest observed age in Ma)
    lad_ma: float                       # Last Appearance Datum (youngest observed age in Ma)
    observed_duration_myr: float        # fad_ma - lad_ma (>= 0.0)
    total_occurrences: int
    channel: ObservationalChannel
    horizons_sampled: list[str]


class StratigraphicEvaluationReceipt(InvariantStatic):
    """
    Complete evaluated receipt for a cohort of taxa under a coupled stratigraphic draw.
    """
    replicate_id: int
    seed: int
    taxon_envelopes: dict[str, LineageObservationEnvelope]
    horizon_draws: dict[str, float]
    sha256_digest: str


class LineageHorizonLifespanEvaluator:
    """
    Aggregates raw fossil occurrences into coupled lineage observation envelopes.
    """

    def __init__(
        self,
        occurrences: list[StratigraphicOccurrence],
        occurrence_metadata: dict[str, dict] | None = None,
    ):
        if not occurrences:
            raise ValueError("Occurrences list cannot be empty.")
        self.occurrences = occurrences
        self.resampler = HorizonCoupledResampler(occurrences)
        self.metadata = occurrence_metadata or {}

        # Index occurrences by taxon
        self.taxon_to_occs: dict[str, list[StratigraphicOccurrence]] = {}
        for occ in occurrences:
            t = occ.taxon_name
            if t not in self.taxon_to_occs:
                self.taxon_to_occs[t] = []
            self.taxon_to_occs[t].append(occ)

    def evaluate_realization(
        self,
        replicate_id: int,
        seed: int | None = None,
    ) -> StratigraphicEvaluationReceipt:
        """
        Draws one coupled stratigraphic age realization and evaluates all lineage envelopes.
        """
        # Step 1: Draw coupled ages where occurrences sharing a horizon receive identical ages
        rep = self.resampler.generate_replicate(replicate_id=replicate_id, seed=seed)
        occ_ages = rep.occurrence_ages

        envelopes: dict[str, LineageObservationEnvelope] = {}

        # Step 2: Aggregate per-taxon FAD, LAD, and preservation channels
        for taxon_name, occ_list in sorted(self.taxon_to_occs.items()):
            ages = [occ_ages[occ.occurrence_id] for occ in occ_list]
            fad = max(ages)
            lad = min(ages)
            duration = round(fad - lad, 4)

            # Extract preservation channel metrics
            body_count = 0
            trace_count = 0
            max_depth = 0.0
            lithologies = set()
            horizons = []

            for occ in occ_list:
                horizons.append(occ.horizon_id)
                meta = self.metadata.get(occ.occurrence_id, {})
                mode = meta.get("preservation_mode", "body").lower()
                if mode == "trace":
                    trace_count += 1
                else:
                    body_count += 1
                depth = meta.get("burrow_depth_mm", 0.0)
                if depth > max_depth:
                    max_depth = depth
                litho = meta.get("lithology")
                if litho:
                    lithologies.add(litho)

            envelope = LineageObservationEnvelope(
                taxon_name=taxon_name,
                fad_ma=round(fad, 4),
                lad_ma=round(lad, 4),
                observed_duration_myr=duration,
                total_occurrences=len(occ_list),
                channel=ObservationalChannel(
                    body_occurrence_count=body_count,
                    trace_occurrence_count=trace_count,
                    max_burrow_depth_mm=round(max_depth, 2),
                    lithologies=sorted(list(lithologies)),
                ),
                horizons_sampled=sorted(list(set(horizons))),
            )
            envelopes[taxon_name] = envelope

        # Step 3: Compute deterministic provenance hash
        hash_input = f"{replicate_id}:{seed}:{sorted([(k, v.fad_ma, v.lad_ma) for k, v in envelopes.items()])}"
        sha = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

        return StratigraphicEvaluationReceipt(
            replicate_id=replicate_id,
            seed=seed if seed is not None else replicate_id,
            taxon_envelopes=envelopes,
            horizon_draws=rep.horizon_draws,
            sha256_digest=sha,
        )
