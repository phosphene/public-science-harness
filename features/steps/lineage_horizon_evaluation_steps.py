import sys
from pathlib import Path
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "studies/cambrian-substrate/models"))
from horizon_coupled_resampler import StratigraphicOccurrence
from lineage_horizon_evaluator import LineageHorizonLifespanEvaluator


@given('{count:d} fossil occurrences for taxon "{taxon}" from horizon "{horizon}" spanning {top:f} to {bot:f} Ma')
def step_setup_single_taxon(context, count, taxon, horizon, top, bot):
    if not hasattr(context, "occurrences"):
        context.occurrences = []
        context.metadata = {}
    for i in range(count):
        occ_id = f"{taxon}_{horizon}_{i}"
        context.occurrences.append(
            StratigraphicOccurrence(
                occurrence_id=occ_id,
                taxon_name=taxon,
                horizon_id=horizon,
                age_top_ma=top,
                age_bottom_ma=bot,
            )
        )


@given('{count:d} fossil occurrences for taxon "{taxon}" from the same horizon "{horizon}"')
def step_setup_second_taxon(context, count, taxon, horizon):
    # Find bounds of existing horizon
    matching = [occ for occ in context.occurrences if occ.horizon_id == horizon]
    assert matching, f"Horizon {horizon} not found in existing occurrences"
    top = matching[0].age_top_ma
    bot = matching[0].age_bottom_ma
    for i in range(count):
        occ_id = f"{taxon}_{horizon}_{i}"
        context.occurrences.append(
            StratigraphicOccurrence(
                occurrence_id=occ_id,
                taxon_name=taxon,
                horizon_id=horizon,
                age_top_ma=top,
                age_bottom_ma=bot,
            )
        )


@when('the lineage horizon evaluator generates a coupled realization')
def step_evaluate_realization(context):
    evaluator = LineageHorizonLifespanEvaluator(context.occurrences, getattr(context, "metadata", None))
    context.receipt = evaluator.evaluate_realization(replicate_id=1, seed=123)


@then('the FAD of "{taxon1}" must exactly equal the FAD of "{taxon2}"')
def step_assert_fad_equal(context, taxon1, taxon2):
    fad1 = context.receipt.taxon_envelopes[taxon1].fad_ma
    fad2 = context.receipt.taxon_envelopes[taxon2].fad_ma
    assert fad1 == fad2, f"FAD mismatch: {taxon1}={fad1} != {taxon2}={fad2}"


@then('the LAD of "{taxon}" must equal its FAD with observed duration 0.0 Myr')
def step_assert_duration_zero(context, taxon):
    env = context.receipt.taxon_envelopes[taxon]
    assert env.fad_ma == env.lad_ma
    assert env.observed_duration_myr == 0.0


@then('both taxa must be recorded in horizon "{horizon}"')
def step_assert_horizon_recorded(context, horizon):
    for env in context.receipt.taxon_envelopes.values():
        assert horizon in env.horizons_sampled


@given('an ichnological trace occurrence "{occ_id}" for "{taxon}" in horizon "{horizon}" with burrow depth {depth:f} mm')
def step_setup_trace_occ(context, occ_id, taxon, horizon, depth):
    if not hasattr(context, "occurrences"):
        context.occurrences = []
        context.metadata = {}
    context.occurrences.append(
        StratigraphicOccurrence(
            occurrence_id=occ_id,
            taxon_name=taxon,
            horizon_id=horizon,
            age_top_ma=538.0,
            age_bottom_ma=540.0,
        )
    )
    context.metadata[occ_id] = {
        "preservation_mode": "trace",
        "burrow_depth_mm": depth,
    }


@then('taxon "{taxon}" must have body occurrence count {count:d}')
def step_assert_body_count(context, taxon, count):
    env = context.receipt.taxon_envelopes[taxon]
    assert env.channel.body_occurrence_count == count


@then('taxon "{taxon}" must have trace occurrence count {count:d}')
def step_assert_trace_count(context, taxon, count):
    env = context.receipt.taxon_envelopes[taxon]
    assert env.channel.trace_occurrence_count == count


@then('the maximum burrow depth for "{taxon}" must be {depth:f} mm')
def step_assert_max_depth(context, taxon, depth):
    env = context.receipt.taxon_envelopes[taxon]
    assert env.channel.max_burrow_depth_mm == depth


@then('its observed duration must be greater than or equal to 0.0 Myr')
def step_assert_duration_non_neg(context):
    for env in context.receipt.taxon_envelopes.values():
        assert env.observed_duration_myr >= 0.0
