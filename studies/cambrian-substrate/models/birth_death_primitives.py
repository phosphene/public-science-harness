"""Canonical Macroevolutionary Birth-Death and Preservation Primitives.

Delegates strictly to ``phosphene.holonomy.macroevo.primitives`` so ``public-science-harness``
consumes the single canonical Phosphene implementation with zero forked math.
"""

from __future__ import annotations

from typing import Sequence
import numpy as np

from phosphene.holonomy.macroevo.primitives import (
    diversity_hazard,
    keiding_observability_prob,
    log_poisson_process_density,
    log_turnover_survival,
    preservation_effort,
    standing_diversity_trajectory,
)


def keiding_sampling_probability(s: float, e: float, q: float) -> float:
    """Delegate to ``holonomy.macroevo.primitives.keiding_observability_prob``."""
    if s < e or e < 0.0 or q < 0.0:
        raise ValueError("Invalid boundaries: requires s >= e >= 0 and q >= 0.")
    return keiding_observability_prob(preservation_effort(duration=s - e, preservation_rate=q))


def diversity_dependent_hazard(
    n_standing: int | float | np.ndarray,
    rate_0: float,
    feedback_coeff: float,
    model: str = "exponential",
) -> float | np.ndarray:
    """Evaluate exponential (via ``holonomy``) or linear diversity-dependent hazard."""
    if rate_0 < 0.0:
        raise ValueError("Baseline rate rate_0 must be non-negative.")

    n_arr = np.asarray(n_standing, dtype=np.float64)
    if np.any(n_arr < 0.0):
        raise ValueError("Standing diversity N cannot be negative.")

    if model == "exponential":
        if rate_0 == 0.0:
            rates = np.zeros_like(n_arr, dtype=np.float64)
        elif isinstance(n_standing, (int, float)):
            return diversity_hazard(rate_0, feedback_coeff, float(n_standing))
        else:
            rates = np.array(
                [diversity_hazard(rate_0, feedback_coeff, float(n)) for n in n_arr.flat],
                dtype=np.float64,
            ).reshape(n_arr.shape)
    elif model == "linear":
        rates = np.maximum(0.0, rate_0 + feedback_coeff * n_arr)
    else:
        raise ValueError(f"Unknown diversity dependence model: {model}")

    if isinstance(n_standing, (int, float)):
        return float(rates)
    return rates


def poisson_occurrence_loglik(
    occ_ages: Sequence[float] | np.ndarray,
    s: float,
    e: float,
    q: float,
) -> float:
    """Delegate to ``holonomy.macroevo.primitives.log_poisson_process_density``."""
    return log_poisson_process_density(
        occurrence_times=occ_ages,
        origin_age=s,
        extinction_age=e,
        preservation_rate=q,
    )


def lineage_survival_loglik(
    s: float,
    e: float,
    lam_mean: float,
    mu_mean: float,
    is_extant: bool = False,
) -> float:
    """Delegate to ``holonomy.macroevo.primitives.log_turnover_survival``."""
    if s < e or e < 0.0 or lam_mean < 0.0 or mu_mean < 0.0:
        raise ValueError("Invalid parameters for lineage survival hazard.")
    return log_turnover_survival(
        duration=s - e,
        speciation_rate=lam_mean,
        extinction_rate=mu_mean,
        is_extant=(is_extant or e == 0.0),
    )


__all__ = [
    "keiding_sampling_probability",
    "diversity_dependent_hazard",
    "poisson_occurrence_loglik",
    "lineage_survival_loglik",
    "standing_diversity_trajectory",
]
