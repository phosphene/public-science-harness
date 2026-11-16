"""
Phosphene Public Science Harness — Axiomatic Core Vitals
Conforms to Phosphene Python Standards and Mertz (2021) Missingness Taxonomy.
Directly implements canonical operational modes with Invariant/Mutable x Static/Dynamic semantics.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class InvariantStatic(BaseModel):
    """
    A fixed-width, read-only record (Axioms).
    Rejects unknown keys — extra='forbid', frozen=True.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")


class InvariantDynamic(BaseModel):
    """
    A read-only snapshot of arbitrary data (OWA Ingestion).
    Accepts unknown keys — extra='allow', frozen=True.
    """
    model_config = ConfigDict(frozen=True, extra="allow")


class MutableStatic(BaseModel):
    """
    A controlled state machine.
    Rejects unknown keys — extra='forbid', frozen=False.
    """
    model_config = ConfigDict(frozen=False, extra="forbid")


class MutableDynamic(BaseModel):
    """
    A flexible, type-aware dictionary.
    Accepts unknown keys — extra='allow', frozen=False.
    """
    model_config = ConfigDict(frozen=False, extra="allow")


class MissingnessCategory(str, Enum):
    """
    Mertz (2021) Section 3.1 & DFF Section 2.1:
    Explicit taxonomy separating four missingness states that raw data conflates.
    """
    OBSERVED = "observed"                      # Valid empirical observation
    UNOBSERVED_NULL = "unobserved_null"        # Truly unmeasured or missing
    NOT_COMPUTABLE_NAN = "not_computable_nan"  # Numerical calculation failure, division by zero
    NOT_APPLICABLE = "not_applicable"          # Attribute does not apply to observational unit
    BELOW_LOD = "below_lod"                    # Bounded by instrument limit of detection (< LOD)
    ABOVE_CEILING = "above_ceiling"            # Bounded by instrument saturation ceiling (> saturation)
    MAGIC_SENTINEL = "magic_sentinel"          # Known sentinel code (-999, 9999, -1, '?') stripped


class SanitizedValue(InvariantStatic, Generic[T]):
    """
    Wraps an extracted value with its explicit missingness and provenance status.
    Ensures that sentinels and detection limits never silently pollute numerical likelihoods.
    """
    raw_value: Any
    cleaned_value: T | None
    status: MissingnessCategory
    original_sentinel: str | None = None
    note: str | None = None


__all__ = [
    "InvariantDynamic",
    "InvariantStatic",
    "MissingnessCategory",
    "MutableDynamic",
    "MutableStatic",
    "SanitizedValue",
]
