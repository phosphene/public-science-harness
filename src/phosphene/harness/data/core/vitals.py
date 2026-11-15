"""
Phosphene Public Science Harness — Axiomatic Core Vitals
Conforms to Phosphene Python Standards (Part 8) and Mertz (2021) Missingness Taxonomy.
Directly imports canonical operational modes from phosphene.core.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar
from pydantic import Field

# Canonical operational modes from phosphene.core (Part 8 Care Package)
from phosphene.core import (
    InvariantDynamic,
    InvariantStatic,
    MutableDynamic,
    MutableStatic,
)

T = TypeVar("T")


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
