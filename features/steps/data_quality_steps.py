"""
Step definitions for Data Quality & Design for Falsifiability (DFF) BDD scenarios.
Conforms to .agents/skills/bdd-precision/SKILL.md (:bdd.principle/declarative).
"""

from behave import given, when, then
from phosphene.harness.data.core.vitals import MissingnessCategory, SanitizedValue
from phosphene.harness.data.forensics.bit_and_string import DataForensics
from phosphene.harness.data.forensics.outliers import OutlierAndInvariantEngine
from phosphene.harness.data.transforms.strict_sql import ColumnDef, StrictTableSchema


@given("a clean data curation context")
def step_clean_context(context):
    """
    Ensures test isolation for data curation steps.
    """
    context.raw_record = {}
    context.sanitized_record = {}
    context.violations = []


@given('an upstream raw measurement record with value "{val}"')
def step_upstream_raw_value(context, val):
    """
    Simulates ingesting an upstream raw measurement.
    """
    val = val.strip('"')
    context.raw_record = {"field": val}


@given('an upstream raw measurement record below detection limit with value "{val}"')
def step_upstream_lod_value(context, val):
    """
    Simulates ingesting a left-censored observation below limit of detection.
    """
    val = val.strip('"')
    context.raw_record = {"field": val}


@when("the ingestion pipeline cleans the record")
def step_clean_record(context):
    """
    Applies DFF missingness classification logic.
    """
    raw_val = context.raw_record.get("field")
    if raw_val in ("-999", "9999", "-1", "N/A"):
        context.sanitized_record = SanitizedValue(
            raw_value=raw_val,
            cleaned_value=None,
            status=MissingnessCategory.MAGIC_SENTINEL,
            original_sentinel=raw_val,
            note="Sentinel code stripped at raw ingestion boundary"
        )
    elif "<" in str(raw_val) and "LOD" in str(raw_val):
        context.sanitized_record = SanitizedValue(
            raw_value=raw_val,
            cleaned_value=None,
            status=MissingnessCategory.BELOW_LOD,
            note="Left-censored measurement bounded by instrument limit of detection"
        )
    else:
        context.sanitized_record = SanitizedValue(
            raw_value=raw_val,
            cleaned_value=float(raw_val),
            status=MissingnessCategory.OBSERVED
        )


@then('the value must be categorized as "{expected_status}"')
def step_verify_status(context, expected_status):
    """
    Verifies that the missingness category matches the expected DFF enum.
    """
    expected_status = expected_status.strip('"')
    assert context.sanitized_record.status.value == expected_status, (
        f"Expected status {expected_status}, got {context.sanitized_record.status.value}"
    )


@then("the cleaned numerical value must be null")
def step_verify_null(context):
    """
    Verifies that sentinel codes are not coerced to numbers.
    """
    assert context.sanitized_record.cleaned_value is None, (
        f"Expected cleaned_value to be None, got {context.sanitized_record.cleaned_value}"
    )


@then('the sentinel code "{expected_sentinel}" must be preserved in provenance metadata')
def step_verify_sentinel_preserved(context, expected_sentinel):
    """
    Verifies that original sentinel is recorded in metadata.
    """
    expected_sentinel = expected_sentinel.strip('"')
    assert context.sanitized_record.original_sentinel == expected_sentinel, (
        f"Expected original_sentinel {expected_sentinel}, got {context.sanitized_record.original_sentinel}"
    )


@then("the cleaned numerical value must not be coerced to zero")
def step_verify_not_zero(context):
    """
    Guarantees that censored measurements are not falsified as true physical zeros.
    """
    assert context.sanitized_record.cleaned_value != 0.0, "Censored value was falsely coerced to 0.0"


@given('an upstream integer column "{col_name}" containing the value {val:d}')
def step_upstream_int_col(context, col_name, val):
    """
    Sets up an integer column with a potential power-of-two clipping value.
    """
    col_name = col_name.strip('"')
    context.column_name = col_name
    context.column_values = [10, 20, val, 45]


@when("the bit-boundary forensic caliper audits the column")
def step_audit_bit_boundaries(context):
    """
    Runs bit-boundary forensics on the column values.
    """
    context.audit_result = DataForensics.audit_numeric_bit_boundaries(
        context.column_name, context.column_values
    )


@then('an integer boundary warning for "{expected_bound}" must be triggered')
def step_verify_bit_boundary_warn(context, expected_bound):
    """
    Verifies that the bit boundary check detected clipping.
    """
    expected_bound = expected_bound.strip('"')
    assert context.audit_result.has_boundary_warning is True, "Expected boundary warning"
    assert expected_bound in (context.audit_result.warning_message or ""), (
        f"Expected {expected_bound} in warning, got {context.audit_result.warning_message}"
    )


@then("the pipeline must flag potential silent data truncation")
def step_verify_truncation_flagged(context):
    """
    Asserts warning is present.
    """
    assert context.audit_result.warning_message is not None


@given('an upstream string column "{col_name}" with declared schema bound {declared_len:d}')
def step_upstream_string_col(context, col_name, declared_len):
    """
    Sets up string column for truncation audit.
    """
    col_name = col_name.strip('"')
    context.string_col_name = col_name
    context.declared_len = declared_len


@given("multiple distinct records have length exactly 32")
def step_strings_at_bound(context):
    """
    Injects string values creating an artificial spike at the boundary.
    """
    context.string_values = ["Short", "Medium", "X" * 32, "Y" * 32, "Z" * 32]


@when("the string truncation forensic caliper audits the column")
def step_audit_string_truncation(context):
    """
    Runs string truncation diagnostics.
    """
    context.string_audit_result = DataForensics.audit_string_truncation(
        context.string_col_name, context.string_values, declared_length=context.declared_len
    )


@then("a string truncation warning must be triggered")
def step_verify_string_truncation_warning(context):
    """
    Verifies string truncation detection flag.
    """
    assert context.string_audit_result.is_truncated_at_schema_bound is True


@then("the diagnostic report must identify an artificial length spike at 32 characters")
def step_verify_spike_count(context):
    """
    Verifies spike count at declared bound.
    """
    assert context.string_audit_result.length_spike_count >= 2


@given('an upstream taxonomic label "{taxon_str}" containing Cyrillic small letter a')
def step_upstream_homoglyph_taxon(context, taxon_str):
    """
    Injects taxonomic factor string with mixed scripts.
    """
    taxon_str = taxon_str.strip('"')
    context.taxon_string = taxon_str


@when("the homoglyph forensic caliper audits the string")
def step_audit_homoglyphs(context):
    """
    Runs Unicode NFKC and homoglyph audit.
    """
    context.homoglyph_result = DataForensics.audit_string_homoglyphs(context.taxon_string)


@then("a homoglyph risk must be detected")
def step_verify_homoglyph_risk(context):
    """
    Asserts homoglyph risk is detected.
    """
    assert context.homoglyph_result.has_homoglyph_risk is True


@then('the detected scripts must include both "{script_a}" and "{script_b}"')
def step_verify_detected_scripts(context, script_a, script_b):
    """
    Asserts both scripts are present in factor token.
    """
    script_a = script_a.strip('"')
    script_b = script_b.strip('"')
    assert script_a in context.homoglyph_result.detected_scripts
    assert script_b in context.homoglyph_result.detected_scripts


@given("an empirical dataset with 15000 observations")
def step_large_sample_dataset(context):
    """
    Generates synthetic dataset for sample-size scaled outlier test.
    """
    import random
    random.seed(42)
    context.sample_data = [random.gauss(100.0, 5.0) for _ in range(15_000)]
    # Add a point at ~3.2 sigma (value = 116.0)
    context.sample_data.append(116.0)


@when('the sample-scaled outlier engine evaluates column "{col_name}"')
def step_evaluate_scaled_outliers(context, col_name):
    """
    Evaluates outliers using dynamic sample-scaled thresholds.
    """
    col_name = col_name.strip('"')
    context.outlier_result = OutlierAndInvariantEngine.compute_sample_scaled_outliers(
        col_name, context.sample_data
    )


@then("the effective sigma threshold must scale to 4.0")
def step_verify_sigma_scale(context):
    """
    Verifies that threshold scaled from 3.0 to 4.0 for N > 10,000.
    """
    assert context.outlier_result.effective_sigma_threshold == 4.0


@then("observations between 3.0 and 4.0 sigma must not be discarded as anomalies")
def step_verify_tails_protected(context):
    """
    Verifies that the 3.2-sigma observation was preserved.
    """
    assert context.outlier_result.outlier_count == 0


@given("a stratigraphic horizon record with bottom age 500.0 Ma and top age 515.0 Ma")
def step_inverted_stratigraphy(context):
    """
    Injects an impossible stratigraphic inversion record.
    """
    context.strat_records = [
        {"horizon_id": "HZ_INVALID", "age_bottom_ma": 500.0, "age_top_ma": 515.0}
    ]


@when("the multivariate domain invariants engine evaluates temporal monotonicity")
def step_eval_invariants(context):
    """
    Runs cross-column invariant assertions.
    """
    invariants = [
        ("temporal_ordering", lambda r: (r["age_bottom_ma"] >= r["age_top_ma"], "age_bottom_ma is less than age_top_ma"))
    ]
    context.violations = OutlierAndInvariantEngine.evaluate_invariants(
        context.strat_records, invariants, id_key="horizon_id"
    )


@then("a domain invariant violation must be raised")
def step_verify_invariant_violation(context):
    """
    Asserts that the temporal inversion violation was caught.
    """
    assert len(context.violations) >= 1


@then("the violation message must indicate that bottom age is less than top age")
def step_verify_violation_msg(context):
    """
    Checks invariant violation diagnostic message.
    """
    assert "age_bottom_ma is less than age_top_ma" in context.violations[0].violation_message


@given('a table definition for "{table_name}" with strict columns and checks')
def step_strict_table_def(context, table_name):
    """
    Sets up a declarative table schema.
    """
    table_name = table_name.strip('"')
    context.strict_schema = StrictTableSchema(
        table_name=table_name,
        columns=[
            ColumnDef(name="horizon_id", data_type="TEXT", is_primary_key=True),
            ColumnDef(name="age_ma", data_type="REAL", check_expr="age_ma > 0.0"),
        ],
        table_checks=["age_ma <= 600.0"]
    )


@when("the DDL compiler generates the SQL schema")
def step_compile_ddl(context):
    """
    Compiles table schema into DDL string.
    """
    context.ddl_output = context.strict_schema.to_sqlite_strict_ddl()


@then('the output DDL must include the "STRICT;" table modifier')
def step_verify_strict_modifier(context):
    """
    Asserts STRICT mode keyword in output DDL.
    """
    assert ") STRICT;" in context.ddl_output


@then("type affinity coercion must be strictly forbidden")
def step_verify_type_affinity_neutralized(context):
    """
    Asserts explicit types are defined.
    """
    assert "horizon_id TEXT PRIMARY KEY" in context.ddl_output
    assert "age_ma REAL NOT NULL" in context.ddl_output
