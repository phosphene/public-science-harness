"""
Bit-Boundary, String Truncation, and Homoglyph Forensics.
Conforms to Mertz (2021) Ch. 1 & Ch. 3 / PSH-002, PSH-003.
"""

from __future__ import annotations

import unicodedata
from typing import Sequence
from phosphene.harness.data.core.vitals import InvariantStatic


class BitBoundaryCheckResult(InvariantStatic):
    column_name: str
    min_value: float | int | None
    max_value: float | int | None
    is_clipped_at_int16: bool
    is_clipped_at_uint16: bool
    is_clipped_at_int32: bool
    is_clipped_at_uint32: bool
    has_boundary_warning: bool
    warning_message: str | None = None


class StringTruncationResult(InvariantStatic):
    column_name: str
    max_observed_length: int
    declared_schema_length: int | None
    is_truncated_at_schema_bound: bool
    length_spike_count: int
    warning_message: str | None = None


class HomoglyphCheckResult(InvariantStatic):
    original_string: str
    normalized_nfkc: str
    has_non_ascii: bool
    has_mixed_script: bool
    detected_scripts: list[str]
    has_homoglyph_risk: bool


class DataForensics:
    """
    Pure functional diagnostics for bit-boundaries, truncation, and character forensics.
    """

    INT16_MAX = 32_767
    INT16_MIN = -32_768
    UINT16_MAX = 65_535
    INT32_MAX = 2_147_483_647
    INT32_MIN = -2_147_483_648
    UINT32_MAX = 4_294_967_295

    @classmethod
    def audit_numeric_bit_boundaries(
        cls, column_name: str, values: Sequence[int | float | None]
    ) -> BitBoundaryCheckResult:
        valid_vals = [v for v in values if v is not None and not (isinstance(v, float) and (v != v))]
        if not valid_vals:
            return BitBoundaryCheckResult(
                column_name=column_name,
                min_value=None,
                max_value=None,
                is_clipped_at_int16=False,
                is_clipped_at_uint16=False,
                is_clipped_at_int32=False,
                is_clipped_at_uint32=False,
                has_boundary_warning=False,
            )

        min_val = min(valid_vals)
        max_val = max(valid_vals)

        c_int16 = (max_val == cls.INT16_MAX) or (min_val == cls.INT16_MIN)
        c_uint16 = max_val == cls.UINT16_MAX
        c_int32 = (max_val == cls.INT32_MAX) or (min_val == cls.INT32_MIN)
        c_uint32 = max_val == cls.UINT32_MAX

        has_warn = c_int16 or c_uint16 or c_int32 or c_uint32
        msg = None
        if has_warn:
            bounds_hit = []
            if c_int16: bounds_hit.append("INT16 (32767)")
            if c_uint16: bounds_hit.append("UINT16 (65535)")
            if c_int32: bounds_hit.append("INT32 (2147483647)")
            if c_uint32: bounds_hit.append("UINT32 (4294967295)")
            msg = f"Potential integer overflow/clipping detected at: {', '.join(bounds_hit)}"

        return BitBoundaryCheckResult(
            column_name=column_name,
            min_value=min_val,
            max_value=max_val,
            is_clipped_at_int16=c_int16,
            is_clipped_at_uint16=c_uint16,
            is_clipped_at_int32=c_int32,
            is_clipped_at_uint32=c_uint32,
            has_boundary_warning=has_warn,
            warning_message=msg,
        )

    @classmethod
    def audit_string_truncation(
        cls, column_name: str, strings: Sequence[str | None], declared_length: int | None = None
    ) -> StringTruncationResult:
        lengths = [len(s) for s in strings if s is not None]
        if not lengths:
            return StringTruncationResult(
                column_name=column_name,
                max_observed_length=0,
                declared_schema_length=declared_length,
                is_truncated_at_schema_bound=False,
                length_spike_count=0,
            )

        max_len = max(lengths)
        spike_count = lengths.count(max_len)
        is_trunc = False
        msg = None

        if declared_length is not None and max_len == declared_length and spike_count > 1:
            is_trunc = True
            msg = (
                f"Column '{column_name}' has {spike_count} entries exactly at schema bound "
                f"{declared_length}, indicating silent string clipping."
            )

        return StringTruncationResult(
            column_name=column_name,
            max_observed_length=max_len,
            declared_schema_length=declared_length,
            is_truncated_at_schema_bound=is_trunc,
            length_spike_count=spike_count,
            warning_message=msg,
        )

    @classmethod
    def audit_string_homoglyphs(cls, text: str) -> HomoglyphCheckResult:
        normalized = unicodedata.normalize("NFKC", text)
        has_non_ascii = any(ord(c) > 127 for c in text)
        scripts = set()
        for c in text:
            if c.isalnum():
                try:
                    script_name = unicodedata.name(c).split()[0]
                    scripts.add(script_name)
                except ValueError:
                    pass

        # Mixed scripts often indicate homoglyph injection (e.g. Latin + Cyrillic)
        has_mixed = len(scripts) > 1 and "LATIN" in scripts
        has_risk = has_mixed or ("CYRILLIC" in scripts and "LATIN" in scripts)

        return HomoglyphCheckResult(
            original_string=text,
            normalized_nfkc=normalized,
            has_non_ascii=has_non_ascii,
            has_mixed_script=has_mixed,
            detected_scripts=sorted(list(scripts)),
            has_homoglyph_risk=has_risk,
        )
