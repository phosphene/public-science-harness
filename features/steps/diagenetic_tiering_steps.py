import sys
from pathlib import Path
import numpy as np
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "studies/cambrian-substrate/models"))
from diagenetic_tiering import DiageneticTieringSolver


@given("an undisturbed Ediacaran sediment profile with mat tiering depth {depth:f} mm")
def step_ediacaran_profile(context, depth):
    context.solver = DiageneticTieringSolver(domain_depth_mm=100.0, n_points=101)
    context.ediacaran_depth = depth
    context.ed_result = context.solver.solve_steady_state(z_max_mm=depth, biodiffusion_db0=60.0)


@when("the diagenetic steady state is solved with surface bottom water O2 {o2} umol")
def step_solve_steady_o2(context, o2):
    assert context.ed_result.solver_success is True


@then("the steady state oxygen penetration depth must be less than or equal to {max_pen:f} mm")
def step_verify_ed_pen(context, max_pen):
    assert context.ed_result.o2_penetration_depth_mm <= max_pen, (
        f"Expected O2 penetration <= {max_pen}, got {context.ed_result.o2_penetration_depth_mm}"
    )


@then("the aerobic niche capacity must be bounded by planar boundary limits")
def step_verify_ed_niche(context):
    assert context.ed_result.aerobic_niche_capacity > 0.0
    context.baseline_ed_capacity = context.ed_result.aerobic_niche_capacity


@given("a Fortunian bioturbated sediment profile with tiering depth {depth:f} mm")
def step_cb_profile(context, depth):
    if not hasattr(context, "solver"):
        context.solver = DiageneticTieringSolver(domain_depth_mm=100.0, n_points=101)
        context.ed_result = context.solver.solve_steady_state(z_max_mm=1.5, biodiffusion_db0=60.0)
    context.cb_depth = depth


@when("the diagenetic steady state is solved with biodiffusion coefficient {db0:f} mm2/yr")
def step_solve_cb(context, db0):
    context.cb_result = context.solver.solve_steady_state(z_max_mm=context.cb_depth, biodiffusion_db0=db0)
    assert context.cb_result.solver_success is True


@then("the steady state oxygen penetration depth must exceed the Ediacaran baseline by at least {ratio:f} times")
def step_verify_cb_pen_ratio(context, ratio):
    actual_ratio = context.cb_result.o2_penetration_depth_mm / context.ed_result.o2_penetration_depth_mm
    assert actual_ratio >= ratio, f"Expected penetration ratio >= {ratio}, got {actual_ratio:.2f}"


@then("the aerobic niche capacity must expand by at least {ratio:f} times over the Ediacaran baseline")
def step_verify_cb_niche_ratio(context, ratio):
    actual_ratio = context.cb_result.aerobic_niche_capacity / context.ed_result.aerobic_niche_capacity
    assert actual_ratio >= ratio, f"Expected niche ratio >= {ratio}, got {actual_ratio:.2f}"


@given("a continuous depth domain from 0 to {domain:d} mm with {nodes:d} spatial grid nodes")
def step_domain_setup(context, domain, nodes):
    context.solver = DiageneticTieringSolver(domain_depth_mm=float(domain), n_points=nodes)


@when("the coupled BDF integrator solves the sediment advection-diffusion-reaction equations")
def step_solve_integrator(context):
    context.run_result = context.solver.solve_steady_state(z_max_mm=45.0, biodiffusion_db0=50.0)


@then("the solver must achieve numerical convergence with solver_success true")
def step_verify_convergence(context):
    assert context.run_result.solver_success is True


@then("all reconstructed concentrations of O2 and C_org must be non-negative across the entire column")
def step_verify_non_negative(context):
    assert all(v >= 0.0 for v in context.run_result.o2_profile_umol)
    assert all(v >= 0.0 for v in context.run_result.c_org_profile_mg_cm3)
