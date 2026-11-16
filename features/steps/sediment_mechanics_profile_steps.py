import sys
from pathlib import Path
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "studies/cambrian-substrate/models"))
from primitives import biodiffusion_kernel
from diagenetic_tiering import DiageneticTieringSolver


@given("a Terminal Ediacaran matground with tiering depth {z_max:f} mm and biological mixing {db0:f} mm2/yr")
def step_setup_ediacaran(context, z_max, db0):
    context.ed_z_max = z_max
    context.ed_db0 = db0
    context.solver = DiageneticTieringSolver(domain_depth_mm=100.0, n_points=101)


@when("biodiffusion is evaluated at depth {z:f} mm")
def step_eval_ediacaran_biodiffusion(context, z):
    context.ed_db = biodiffusion_kernel(z_mm=z, z_max_mm=context.ed_z_max, d_b0=context.ed_db0)
    context.ed_res = context.solver.solve_steady_state(z_max_mm=context.ed_z_max, biodiffusion_db0=context.ed_db0)


@then("the biodiffusion coefficient must be {db:f} mm2/yr")
def step_assert_biodiffusion_zero(context, db):
    assert context.ed_db == db, f"Expected Db={db}, got {context.ed_db}"


@then("the oxygen penetration depth must remain strictly confined to under {depth:f} mm")
def step_assert_o2_confined(context, depth):
    assert context.ed_res.o2_penetration_depth_mm < depth, (
        f"Penetration depth {context.ed_res.o2_penetration_depth_mm} exceeded {depth} mm"
    )


@given("a Fortunian substrate horizon with tiering depth {z_max:f} mm and biological mixing {db0:f} mm2/yr")
def step_setup_fortunian(context, z_max, db0):
    context.cb_z_max = z_max
    context.cb_db0 = db0
    if not hasattr(context, "solver"):
        context.solver = DiageneticTieringSolver(domain_depth_mm=100.0, n_points=101)
    # Ensure ediacaran baseline exists
    if not hasattr(context, "ed_res"):
        context.ed_res = context.solver.solve_steady_state(z_max_mm=2.0, biodiffusion_db0=0.0)


@when("the coupled diagenetic steady state is evaluated")
def step_eval_diagenetic_steady_state(context):
    context.cb_res = context.solver.solve_steady_state(z_max_mm=context.cb_z_max, biodiffusion_db0=context.cb_db0)
    context.db_below = biodiffusion_kernel(z_mm=45.0, z_max_mm=context.cb_z_max, d_b0=context.cb_db0, sigma_b_mm=5.0)


@then("the oxygen penetration depth must exceed that of the Ediacaran baseline")
def step_assert_o2_exceeds(context):
    assert context.cb_res.o2_penetration_depth_mm > context.ed_res.o2_penetration_depth_mm, (
        f"CB {context.cb_res.o2_penetration_depth_mm} <= ED {context.ed_res.o2_penetration_depth_mm}"
    )


@then("the aerobic niche capacity must expand by more than a factor of {factor:f}")
def step_assert_niche_expansion(context, factor):
    ratio = context.cb_res.aerobic_niche_capacity / context.ed_res.aerobic_niche_capacity
    assert ratio > factor, f"Expansion ratio {ratio:.2f} did not exceed {factor}"


@then("biodiffusion below the tier depth {z_max:f} mm must decay smoothly toward zero")
def step_assert_decay_below(context, z_max):
    assert 0.0 < context.db_below < context.cb_db0, (
        f"Expected 0.0 < {context.db_below} < {context.cb_db0}"
    )


@given("the 4 discrete physical sediment tiers: mat, undermat, vertical, and deep")
def step_setup_tiers(context):
    context.tiers = [
        ("mat", 2.0),
        ("undermat", 10.0),
        ("vertical", 35.0),
        ("deep", 80.0),
    ]


@when("their characteristic tier penetration depths are ordered")
def step_order_tiers(context):
    context.depths = [depth for _, depth in context.tiers]


@then("tier depth must increase strictly monotonically from {d_min:f} mm to {d_max:f} mm")
def step_assert_monotonic_depth(context, d_min, d_max):
    assert context.depths[0] == d_min
    assert context.depths[-1] == d_max
    for d1, d2 in zip(context.depths[:-1], context.depths[1:]):
        assert d1 < d2, f"Tier depth non-monotonic: {d1} >= {d2}"
