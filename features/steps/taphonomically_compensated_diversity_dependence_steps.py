import sys
from pathlib import Path
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "studies/cambrian-substrate/models"))
from diversity_dependence_estimator import (
    DiversityDependenceEstimator,
    EpistemicWarrantViolation,
)


@given("a curated Cambrian database containing functional guilds and epistemic annotations")
def step_setup_db(context):
    context.db_path = Path(__file__).parent.parent.parent / "studies/cambrian-substrate/data/curated/cambrian_substrate.db"
    assert context.db_path.exists()
    context.estimator = DiversityDependenceEstimator(db_path=context.db_path)


@given('the epistemic annotation flags "{status}" for "{guild}"')
def step_verify_flag(context, status, guild):
    calib = context.estimator._get_guild_calibration(guild)
    assert calib["calibration_status"] == status


@when('an estimation pipeline attempts to fit unweighted diversity dependence to "{guild}" body counts')
def step_attempt_unweighted(context, guild):
    context.violation = None
    try:
        context.estimator.fit_diversity_dependence(guild, z_max_mm=None)
    except EpistemicWarrantViolation as e:
        context.violation = e


@then("the estimator must reject execution with an epistemic warrant violation")
def step_assert_rejection(context):
    assert context.violation is not None, "Expected EpistemicWarrantViolation but execution succeeded"


@then('the violation message must cite DOI "{doi1}" or "{doi2}"')
def step_assert_citation(context, doi1, doi2):
    msg = str(context.violation)
    # Checks for Brasier (1994) or citation text
    assert ("Brasier" in msg or doi1 in msg or doi2 in msg), (
        f"Citation missing from violation message: {msg}"
    )


@then("the downstream birth-death model state must remain unpolluted")
def step_assert_clean_state(context):
    assert not hasattr(context, "polluted_fit")


@given("an infaunal lineage with {occs:d} observed body occurrences across {taxa:d} taxa")
def step_setup_infaunal_counts(context, occs, taxa):
    calib = context.estimator._get_guild_calibration("INFAUNAL_BURROWER")
    assert calib["raw_distinct_taxa"] == taxa
    assert calib["raw_occurrences"] == occs
    context.raw_taxa = taxa


@given("observed trace tiering depth Z_max = {z_max:f} mm from the Fortunian stage")
def step_setup_tiering_depth(context, z_max):
    context.z_max = z_max


@when("the taphonomically compensated estimator evaluates the effective standing diversity")
def step_eval_compensated(context):
    context.fit = context.estimator.fit_diversity_dependence("INFAUNAL_BURROWER", z_max_mm=context.z_max)


@then("the effective ecological capacity N_eff must scale with tiering penetration depth")
def step_assert_scaling(context):
    assert context.fit.effective_capacity_n_eff > context.raw_taxa


@then("N_eff must exceed the raw body count of {taxa:d} taxa by at least a factor of {factor:f}")
def step_assert_expansion_factor(context, taxa, factor):
    ratio = context.fit.effective_capacity_n_eff / taxa
    assert ratio >= factor, f"Expansion ratio {ratio:.2f} < {factor}"


@then("the resulting diversification slope Gl must reflect substrate ecological volume rather than body preservability")
def step_assert_gl_slope(context):
    assert context.fit.gl_speciation_slope > 0.0, (
        f"Expected positive/stabilizing Gl, got {context.fit.gl_speciation_slope}"
    )


@when('an estimation pipeline evaluates diversity dependence for "{guild}"')
def step_eval_skeletal(context, guild):
    context.skeletal_fit = context.estimator.fit_diversity_dependence(guild)


@then('the estimator must verify calibration status is "{status}"')
def step_verify_skeletal_status(context, status):
    calib = context.estimator._get_guild_calibration("SEDENTARY_FILTER_FEEDER")
    assert calib["calibration_status"] == status


@then("the estimator must allow direct body count fitting without tiering penalty")
def step_assert_direct_fitting(context):
    assert context.skeletal_fit.compensation_applied is False
    assert context.skeletal_fit.raw_body_taxa_count == 81
    assert context.skeletal_fit.effective_capacity_n_eff == 81.0
