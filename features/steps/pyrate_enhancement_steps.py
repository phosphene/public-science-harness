import sys
import sqlite3
from pathlib import Path
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "studies/cambrian-substrate/models"))
from horizon_coupled_resampler import HorizonCoupledResampler, StratigraphicOccurrence
from phosphene.harness.data.transforms.provenance import DataAnnotationEvent


@given('{count:d} fossil occurrences recovered from the same geological horizon "{horizon_name}"')
def step_setup_occurrences(context, count, horizon_name):
    context.horizon_name = horizon_name
    context.count = count


@given('the horizon spans chronostratigraphic bounds {top:f} to {bottom:f} Ma')
def step_setup_bounds(context, top, bottom):
    context.top = top
    context.bottom = bottom
    context.occurrences = [
        StratigraphicOccurrence(
            occurrence_id=f"occ_{i}",
            taxon_name=f"Taxon_{i}",
            horizon_id=context.horizon_name,
            age_top_ma=top,
            age_bottom_ma=bottom,
        )
        for i in range(context.count)
    ]
    context.resampler = HorizonCoupledResampler(context.occurrences)


@when('Monte Carlo age resampling is performed with horizon coupling enabled')
def step_run_resampling(context):
    context.replicate = context.resampler.generate_replicate(replicate_id=101, seed=101)


@then('all {count:d} occurrences must receive the identical resampled age')
def step_check_identical(context, count):
    ages = list(context.replicate.occurrence_ages.values())
    assert len(ages) == count
    assert all(a == ages[0] for a in ages), f"Ages were not identical: {ages}"


@then('the resampled age must fall strictly within {top:f} and {bottom:f} Ma')
def step_check_bounds(context, top, bottom):
    age = list(context.replicate.occurrence_ages.values())[0]
    assert top <= age <= bottom, f"Age {age} fell outside bounds [{top}, {bottom}]"


@then('a deterministic SHA-256 provenance digest must be emitted')
def step_check_sha(context):
    assert len(context.replicate.sha256_digest) == 64
    rep2 = context.resampler.generate_replicate(replicate_id=101, seed=101)
    assert rep2.sha256_digest == context.replicate.sha256_digest


@given('an empirical occurrence database with {inf_count:d} infaunal body occurrences and {pred_count:d} predator occurrences')
def step_setup_db_counts(context, inf_count, pred_count):
    context.inf_count = inf_count
    context.pred_count = pred_count


@when('the guild diversity calibration pipeline evaluates taphonomic preservation tiers')
def step_eval_taphonomy(context):
    db_path = Path(__file__).parent.parent.parent / "studies/cambrian-substrate/data/curated/cambrian_substrate.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT functional_guild, calibration_status, epistemic_warrant_citation FROM v_calibrated_guild_diversity WHERE functional_guild = 'INFAUNAL_BURROWER';")
    context.infaunal_view_row = c.fetchone()
    
    c.execute("SELECT annotation_id, actor_id, actor_role, target_entity_type, target_selector, judgment_type, epistemic_warrant_doi, epistemic_warrant_citation, rationale, recommended_action FROM epistemic_data_annotations WHERE target_selector LIKE '%INFAUNAL_BURROWER%';")
    arow = c.fetchone()
    context.annotation = DataAnnotationEvent(
        annotation_id=arow[0],
        actor_id=arow[1],
        actor_role=arow[2],
        target_entity_type=arow[3],
        target_selector=arow[4],
        judgment_type=arow[5].lower(),
        epistemic_warrant_doi=arow[6],
        epistemic_warrant_citation=arow[7],
        rationale=arow[8],
        recommended_action=arow[9],
    )
    conn.close()


@then('the infaunal guild must be flagged with status "{status}"')
def step_assert_status(context, status):
    guild, cal_status, citation = context.infaunal_view_row
    assert cal_status == status, f"Expected {status}, got {cal_status}"


@then('naive unweighted body-count diversity-dependence fitting must be strictly blocked')
def step_assert_blocked(context):
    guild, cal_status, citation = context.infaunal_view_row
    assert cal_status == "BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED"
