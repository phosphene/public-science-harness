import math
import sys
from pathlib import Path
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "studies/cambrian-substrate/models"))
from horizon_coupled_resampler import StratigraphicOccurrence
from lineage_horizon_evaluator import LineageHorizonLifespanEvaluator
from conditioned_likelihood_evaluator import (
    BirthDeathParameters,
    ConditionedBirthDeathLikelihoodEvaluator,
)


@given('a stratigraphic evaluation receipt containing "{taxon}" with FAD {fad:f} Ma and LAD {lad:f} Ma')
def step_setup_receipt(context, taxon, fad, lad):
    # Setup single horizon occurrence to produce exact FAD/LAD
    occs = [
        StratigraphicOccurrence(
            occurrence_id="occ_1",
            taxon_name=taxon,
            horizon_id="HZ_TEST",
            age_top_ma=fad,
            age_bottom_ma=fad,
        )
    ]
    evaluator = LineageHorizonLifespanEvaluator(occs)
    context.receipt = evaluator.evaluate_realization(replicate_id=1, seed=1)
    context.taxon = taxon


@given('candidate latent lifespan boundaries s = {s:f} Ma and e = {e:f} Ma')
def step_setup_latent_spans(context, s, e):
    context.latent_spans = {context.taxon: (s, e)}


@given('macroevolutionary parameters speciation {lam:f}, extinction {mu:f}, and preservation {q:f}')
def step_setup_params(context, lam, mu, q):
    context.params = BirthDeathParameters(
        lambda_0=lam,
        mu_0=mu,
        q_0=q,
    )


@when('the conditioned birth-death likelihood evaluator evaluates the cohort')
def step_eval_likelihood(context):
    context.ll_receipt = ConditionedBirthDeathLikelihoodEvaluator.evaluate_cohort_likelihood(
        context.receipt, context.latent_spans, context.params
    )


@then('the total conditioned log-likelihood must be finite and negative')
def step_assert_finite_negative(context):
    ll = context.ll_receipt.total_log_likelihood
    assert math.isfinite(ll), f"Expected finite log-likelihood, got {ll}"
    assert ll < 0.0, f"Expected negative log-likelihood, got {ll}"


@then('the Keiding conditioning log-probability must be strictly negative')
def step_assert_keiding_negative(context):
    keid = context.ll_receipt.log_keiding_conditioning_total
    assert keid < 0.0, f"Expected negative Keiding log-prob, got {keid}"


@then('the taxon breakdown must satisfy log L = log L_occ + log L_surv - log P_obs')
def step_assert_decomposition(context):
    bd = context.ll_receipt.taxon_breakdowns[context.taxon]
    expected = bd.loglik_occurrences + bd.loglik_survival - bd.log_keiding_conditioning
    assert math.isclose(bd.total_conditioned_loglik, expected, rel_tol=1e-5), (
        f"Decomposition mismatch: {bd.total_conditioned_loglik} != {expected}"
    )


@when('candidate latent origination s is set to {s:f} Ma which is younger than FAD {fad:f} Ma')
def step_eval_invalid_span(context, s, fad):
    invalid_spans = {context.taxon: (s, 550.0)}
    params = BirthDeathParameters(lambda_0=0.2, mu_0=0.15, q_0=1.0)
    context.invalid_receipt = ConditionedBirthDeathLikelihoodEvaluator.evaluate_cohort_likelihood(
        context.receipt, invalid_spans, params
    )


@then('the total conditioned log-likelihood must be negative infinity')
def step_assert_neg_inf(context):
    assert context.invalid_receipt.total_log_likelihood == -float("inf")
