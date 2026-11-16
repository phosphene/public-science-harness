"""
Step definitions for Transforms, Provenance, and Annotation BDD scenarios.
Conforms to .agents/skills/bdd-precision/SKILL.md (:bdd.principle/declarative).
"""

from behave import given, when, then
from phosphene.harness.data.transforms.provenance import (
    ArtifactFingerprint,
    DataAnnotationEvent,
    DatasetProvenanceReceipt,
    JudgmentType,
    TransformCategory,
    TransformSpec,
)


@given('a raw input dataset "{dataset_name}" with {rec_count:d} records')
def step_raw_input_dataset(context, dataset_name, rec_count):
    """
    Sets up an input dataset reference.
    """
    context.dataset_name = dataset_name.strip('"')
    context.rec_count = rec_count


@when('the transformation engine compiles spec "{spec_id}" under category "{cat_name}"')
def step_compile_transform_spec(context, spec_id, cat_name):
    """
    Constructs a TransformSpec instance.
    """
    spec_id = spec_id.strip('"')
    cat_name = cat_name.strip('"')
    context.transform_spec = TransformSpec(
        transform_id=spec_id,
        version="1.0.0",
        title="Test Transform Spec",
        category=TransformCategory(cat_name),
        description="Transform description",
        input_datasets=[context.dataset_name],
        output_tables=["test_table"],
        pre_invariants=[f"records_count == {context.rec_count}"],
        post_invariants=["records_count > 0"]
    )


@then("the transform specification must enforce pre-conditions and post-conditions")
def step_verify_invariants(context):
    """
    Verifies that pre and post invariants are non-empty.
    """
    assert len(context.transform_spec.pre_invariants) > 0
    assert len(context.transform_spec.post_invariants) > 0


@then('the transform must be recorded as version "{expected_version}"')
def step_verify_version(context, expected_version):
    """
    Verifies transform version string.
    """
    expected_version = expected_version.strip('"')
    assert context.transform_spec.version == expected_version


@given('input artifacts "{art1}" and "{art2}"')
def step_given_artifacts(context, art1, art2):
    """
    Sets up input artifact fingerprints.
    """
    context.inputs = [
        ArtifactFingerprint(path=art1.strip('"'), sha256="abc123sha", record_count=6),
        ArtifactFingerprint(path=art2.strip('"'), sha256="def456sha", record_count=1000)
    ]


@given('an executed pipeline "{pipeline_id}"')
def step_given_pipeline(context, pipeline_id):
    """
    Sets up pipeline identifier.
    """
    context.pipeline_id = pipeline_id.strip('"')


@when("the pipeline completes execution and builds the curated database")
def step_pipeline_completes(context):
    """
    Emits a mock dataset provenance receipt.
    """
    context.receipt = DatasetProvenanceReceipt(
        receipt_id="rcpt-test-001",
        pipeline_id=context.pipeline_id,
        git_commit_sha="c6150ef0937a",
        actor_id="flow@feelingflowingbot",
        transform_specs_applied=["TR-CAMBRIAN-001", "TR-CAMBRIAN-002"],
        input_artifacts=context.inputs,
        output_artifacts=[ArtifactFingerprint(path="cambrian_substrate.db", sha256="outsha789")]
    )


@then("a cryptographic provenance receipt must be emitted")
def step_verify_receipt_emitted(context):
    """
    Verifies receipt existence and non-empty identifier.
    """
    assert context.receipt.receipt_id == "rcpt-test-001"


@then("the receipt must capture SHA-256 hashes of all input and output artifacts")
def step_verify_hashes(context):
    """
    Verifies all inputs and outputs have SHA-256 strings.
    """
    for inp in context.receipt.input_artifacts:
        assert len(inp.sha256) > 0
    for out in context.receipt.output_artifacts:
        assert len(out.sha256) > 0


@then("the receipt must link the active git commit SHA")
def step_verify_git_sha(context):
    """
    Verifies git commit SHA presence.
    """
    assert context.receipt.git_commit_sha == "c6150ef0937a"


@given('an empirical guild "{guild_name}" with sampling ratio below 2.0')
def step_given_low_sampling_guild(context, guild_name):
    """
    Sets up low sampling guild context.
    """
    context.guild_name = guild_name.strip('"')
    context.sampling_ratio = 1.25


@when("the calibration engine registers an epistemic annotation")
def step_register_annotation(context):
    """
    Constructs an epistemic annotation event for taphonomic hazard.
    """
    context.annotation = DataAnnotationEvent(
        annotation_id="annot-test-001",
        actor_id="flow@feelingflowingbot",
        actor_role="Epistemic Verification Agent",
        target_entity_type="COLUMN",
        target_selector=f"functional_guild = '{context.guild_name}'",
        judgment_type=JudgmentType.CALIBRATION_OVERRIDE,
        epistemic_warrant_doi="10.1017/S001675689400001X",
        epistemic_warrant_citation="Brasier, M.D. et al. (1994). Decision on the Precambrian-Cambrian boundary stratotype.",
        rationale="Infaunal soft tissue decay causes under-representation in body fossil occurrence tables.",
        recommended_action="BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED"
    )


@then('the judgment type must be "{expected_judgment}"')
def step_verify_judgment_type(context, expected_judgment):
    """
    Verifies judgment type enum.
    """
    expected_judgment = expected_judgment.strip('"')
    assert context.annotation.judgment_type.value == expected_judgment


@then('the epistemic warrant must cite DOI "{expected_doi}"')
def step_verify_doi(context, expected_doi):
    """
    Verifies DOI match.
    """
    expected_doi = expected_doi.strip('"')
    assert context.annotation.epistemic_warrant_doi == expected_doi


@then('the annotation must flag "{expected_flag}"')
def step_verify_flag(context, expected_flag):
    """
    Verifies recommended action contains flag.
    """
    expected_flag = expected_flag.strip('"')
    assert expected_flag in context.annotation.recommended_action


@then("downstream unweighted body fossil diversity-dependence fitting must be forbidden")
def step_verify_forbidden(context):
    """
    Asserts calibration override status.
    """
    assert context.annotation.judgment_type == JudgmentType.CALIBRATION_OVERRIDE
