"""
Phosphene Public Science Harness — Axiomatic Core Vitals
Conforms to Phosphene Python Standards and Mertz (2021) Missingness Taxonomy.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class InvariantStatic(BaseModel):
    """
    Fixed-width, read-only record.
    Enforces strict immutability and forbids arbitrary or unexpected fields.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        arbitrary_types_allowed=True,
    )


class MissingnessCategory(str, Enum):
    """
    Mertz (2021) Section 3.1 & DFF Section 2.1:
    Explicit taxonomy separating four missingness states that raw data conflates.
    """
    OBSERVED = "observed"                      # Valid empirical observation
    UNOBSERVED_NULL = "unobserved_null"        # Data was not recorded or missing
    NOT_COMPUTABLE_NAN = "not_computable_nan"  # Arithmetic failure / IEEE-754 NaN / div by zero
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
