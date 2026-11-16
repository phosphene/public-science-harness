"""
Phosphene Public Science Harness — Transforms, Provenance, and Annotation Contracts
Conforms to docs/TRANSFORMS_PROVENANCE_AND_ANNOTATION.md and eval/provenance-event-v1.md.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from pydantic import Field

from phosphene.harness.data.core.vitals import InvariantStatic


class TransformCategory(str, Enum):
    """
    Taxonomy of data transformations conforming to Section 2 of the standard.
    """
    ISOMORPHIC_HYGIENE = "isomorphic_hygiene"
    SENTINEL_SANITIZATION = "sentinel_sanitization"
    TAXONOMIC_HARMONIZATION = "taxonomic_harmonization"
    TEMPORAL_BINNING = "temporal_binning"
    TAPHONOMIC_CALIBRATION = "taphonomic_calibration"
    AGGREGATION_REDUCTION = "aggregation_reduction"


class JudgmentType(str, Enum):
    """
    Epistemic judgment category for data annotations.
    """
    DISCLOSURE = "disclosure"
    CALIBRATION_OVERRIDE = "calibration_override"
    RECLASSIFICATION = "reclassification"
    FLAG_EXCLUSION = "flag_exclusion"


class TransformSpec(InvariantStatic):
    """
    A declarative contract governing a single data transformation step.
    """
    transform_id: str
    version: str = "1.0.0"
    title: str
    category: TransformCategory
    description: str
    input_datasets: List[str]
    output_tables: List[str]
    pre_invariants: List[str] = Field(default_factory=list)
    post_invariants: List[str] = Field(default_factory=list)


class DataAnnotationEvent(InvariantStatic):
    """
    An immutable epistemic annotation attached to a data entity.
    Directly aligns with Phosphene's BaseProvenanceEvent vocabulary.
    """
    annotation_id: str
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actor_id: str
    actor_role: str
    target_entity_type: str  # 'TABLE' | 'COLUMN' | 'RECORD' | 'VALUE'
    target_selector: str     # Predicate or coordinate, e.g. "functional_guild = 'INFAUNAL_BURROWER'"
    judgment_type: JudgmentType
    epistemic_warrant_doi: Optional[str] = None
    epistemic_warrant_citation: Optional[str] = None
    rationale: str
    recommended_action: str


class ArtifactFingerprint(InvariantStatic):
    """
    Cryptographic identity of an input or output dataset artifact.
    """
    path: str
    sha256: str
    record_count: Optional[int] = None
    size_bytes: Optional[int] = None


class DatasetProvenanceReceipt(InvariantStatic):
    """
    Machine-verifiable provenance receipt emitted upon pipeline completion.
    """
    receipt_id: str
    pipeline_id: str
    git_commit_sha: Optional[str] = None
    executed_at_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actor_id: str
    transform_specs_applied: List[str]
    input_artifacts: List[ArtifactFingerprint]
    output_artifacts: List[ArtifactFingerprint]
    annotations_emitted: List[DataAnnotationEvent] = Field(default_factory=list)
