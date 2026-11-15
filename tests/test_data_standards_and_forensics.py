"""
Tests for Phosphene Public Science Harness Data Standards & Forensics.
Verifies PSH-001 through PSH-006.
"""

import pytest
from phosphene.harness.data.core.vitals import InvariantStatic, MissingnessCategory, SanitizedValue
from phosphene.harness.data.forensics.bit_and_string import DataForensics
from phosphene.harness.data.forensics.outliers import OutlierAndInvariantEngine
from phosphene.harness.data.transforms.strict_sql import ColumnDef, StrictTableSchema


def test_invariant_static_immutability():
    class TestRecord(InvariantStatic):
        name: str
        value: float

    rec = TestRecord(name="cambrian_stage", value=541.0)
    assert rec.name == "cambrian_stage"

    # Attempt mutation -> must raise ValidationError
    with pytest.raises(Exception):
        rec.value = 520.0

    # Attempt adding unexpected field -> must raise ValidationError
    with pytest.raises(Exception):
        TestRecord(name="stage", value=500.0, extra_key="disallowed")


def test_bit_boundary_forensics():
    # Int16 overflow artifact detection
    values = [10, 20, 32767, 50]
    res = DataForensics.audit_numeric_bit_boundaries("sample_count", values)
    assert res.is_clipped_at_int16 is True
    assert res.has_boundary_warning is True
    assert "INT16" in (res.warning_message or "")

    # Clean values
    clean_vals = [100, 200, 300]
    clean_res = DataForensics.audit_numeric_bit_boundaries("clean_count", clean_vals)
    assert clean_res.has_boundary_warning is False


def test_string_truncation_forensics():
    # Detect spike at declared schema limit of 32 characters
    strings = ["Short", "Medium", "A" * 32, "B" * 32, "C" * 32]
    res = DataForensics.audit_string_truncation("specimen_tag", strings, declared_length=32)
    assert res.is_truncated_at_schema_bound is True
    assert res.length_spike_count == 3


def test_homoglyph_detection():
    # Cyrillic small letter 'а' (U+0430) disguised as Latin 'a'
    homoglyph_str = "Kimberell\u0430"
    res = DataForensics.audit_string_homoglyphs(homoglyph_str)
    assert res.has_non_ascii is True
    assert res.has_homoglyph_risk is True
    assert "CYRILLIC" in res.detected_scripts
    assert "LATIN" in res.detected_scripts

    # Clean ASCII
    clean_str = "Kimberella"
    clean_res = DataForensics.audit_string_homoglyphs(clean_str)
    assert clean_res.has_non_ascii is False
    assert clean_res.has_homoglyph_risk is False


def test_sample_size_scaled_outliers():
    # In large N, 3-sigma should not drop points if threshold scales to 4.0 sigma
    # Generate 15,000 points with mean 10, std 1
    import random
    random.seed(42)
    # Synthetic normal-ish data
    data = [random.gauss(10.0, 1.0) for _ in range(15_000)]
    # Add a point at 3.2 sigma (value ~ 13.2)
    data.append(13.2)

    res = OutlierAndInvariantEngine.compute_sample_scaled_outliers("metabolic_rate", data)
    assert res.sample_size == 15_001
    assert res.effective_sigma_threshold == 4.0  # Scaled up for N > 10,000


def test_multivariate_invariants():
    records = [
        {"horizon_id": "H1", "age_bottom_ma": 541.0, "age_top_ma": 529.0},
        {"horizon_id": "H2", "age_bottom_ma": 500.0, "age_top_ma": 515.0},  # Inverted!
    ]

    invariants = [
        ("temporal_ordering", lambda r: (r["age_bottom_ma"] >= r["age_top_ma"], "age_bottom < age_top"))
    ]

    violations = OutlierAndInvariantEngine.evaluate_invariants(records, invariants, id_key="horizon_id")
    assert len(violations) == 1
    assert violations[0].record_id == "H2"
    assert violations[0].invariant_name == "temporal_ordering"


def test_sqlite_strict_ddl():
    schema = StrictTableSchema(
        table_name="curated_observations",
        columns=[
            ColumnDef(name="obs_id", data_type="TEXT", is_primary_key=True),
            ColumnDef(name="depth_mm", data_type="REAL", check_expr="depth_mm >= 0.0"),
        ],
        table_checks=["depth_mm <= 5000.0"]
    )
    ddl = schema.to_sqlite_strict_ddl()
    assert "STRICT;" in ddl
    assert "obs_id TEXT PRIMARY KEY" in ddl
    assert "CHECK (depth_mm >= 0.0)" in ddl
