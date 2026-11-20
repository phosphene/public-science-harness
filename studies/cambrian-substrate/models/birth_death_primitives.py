"""
Canonical Macroevolutionary Birth-Death and Preservation Primitives.
Pure functional mathematical building blocks decomposed from first principles.
Delegates core mathematical primitives to phosphene-holonomy while maintaining
domain-specific interfaces for Cambrian substrate calibration.
Ref: Kendall (1948), Keiding (1975), Silvestro et al. (2014, 2019), van Holstein & Foley (2024).
"""

from __future__ import annotations

import math
from typing import Sequence
import numpy as np

from phosphene.holonomy.macroevo.primitives import (
    log_diversity_hazard as _holonomy_log_diversity_hazard,
    log_keiding_conditioning as _holonomy_log_keiding_conditioning,
    log_poisson_occurrences as _holonomy_log_poisson_occurrences,
    log_extinction_density as _holonomy_log_extinction_density,
)


def keiding_sampling_probability(
    s: float,
    e: float,
    q: float,
) -> float:
    """
    Primitive 1: Keiding (1975) conditioning probability P(K > 0 | s, e, q).
    Probability that a lineage spanning [e, s] leaves at least one preserved fossil.
    
    Formula:
      P(K > 0) = 1 - exp(-q * (s - e))
      
    Invariants:
      1. Returns 0.0 when duration (s - e) == 0.0 or q == 0.0.
      2. Strictly bounded within [0.0, 1.0].
      3. Monotonically increasing in duration and sampling intensity q.
      4. Requires s >= e >= 0.0 and q >= 0.0.
    """
    if s < e or e < 0.0 or q < 0.0:
        raise ValueError("Invalid boundaries: requires s >= e >= 0 and q >= 0.")
    
    duration = s - e
    expected_fossils = q * duration
    if expected_fossils <= 0.0:
        return 0.0
    return float(-math.expm1(-expected_fossils))


def diversity_dependent_hazard(
    n_standing: int | float | np.ndarray,
    rate_0: float,
    feedback_coeff: float,
    model: str = "exponential",
) -> float | np.ndarray:
    """
    Primitive 2: Evaluates diversity-dependent rate (speciation or extinction).
    
    Models:
      - 'exponential': rate(N) = rate_0 * exp(feedback_coeff * N)
      - 'linear': rate(N) = max(0.0, rate_0 + feedback_coeff * N)
      
    Invariants:
      1. Strictly non-negative.
      2. Returns rate_0 when feedback_coeff == 0 or N == 0.
      3. For feedback_coeff < 0 (niche saturation), monotonically decreasing with N.
      4. For feedback_coeff > 0 (niche construction), monotonically increasing with N.
    """
    if rate_0 < 0.0:
        raise ValueError("Baseline rate rate_0 must be non-negative.")
        
    n_arr = np.asarray(n_standing, dtype=np.float64)
    if np.any(n_arr < 0.0):
        raise ValueError("Standing diversity N cannot be negative.")
        
    if model == "exponential":
        if isinstance(n_standing, (int, float)):
            log_hazard = _holonomy_log_diversity_hazard(rate_0, feedback_coeff, float(n_standing), clamp_bound=50.0)
            return float(math.exp(log_hazard))
        rates = rate_0 * np.exp(np.clip(feedback_coeff * n_arr, -50.0, 50.0))
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
    """
    Primitive 3: Poisson process log-likelihood of observed occurrences between s and e.
    
    Formula:
      log L = sum(log q) - q * (s - e)
      
    Invariants:
      1. Returns -inf if any occurrence age is outside [e, s].
      2. Strictly penalizes non-occurrence interval via -q * (s - e).
    """
    if s < e or e < 0.0 or q < 0.0:
        raise ValueError("Invalid boundaries: requires s >= e >= 0 and q >= 0.")
        
    ages = np.asarray(occ_ages, dtype=np.float64)
    k = len(ages)
    
    if k == 0:
        return -float(q * (s - e))
        
    if np.any(ages > s) or np.any(ages < e):
        return -float("inf")
        
    if q <= 0.0:
        return -float("inf")
        
    return float(k * math.log(q) - q * (s - e))


def lineage_survival_loglik(
    s: float,
    e: float,
    lam_mean: float,
    mu_mean: float,
    is_extant: bool = False,
) -> float:
    """
    Primitive 4: Keiding continuous-time survival log-likelihood for a lineage interval.
    
    Formula:
      log L = - (lam + mu) * (s - e) + (0 if is_extant else log(mu))
      
    Invariants:
      1. Bounded above by log(mu) (or 0 for extant).
      2. Strictly decreasing with duration (s - e).
    """
    if s < e or e < 0.0 or lam_mean < 0.0 or mu_mean < 0.0:
        raise ValueError("Invalid parameters for lineage survival hazard.")
        
    duration = s - e
    turnover = lam_mean + mu_mean
    survival_term = -turnover * duration
    
    if is_extant or e == 0.0:
        return float(survival_term)
        
    if mu_mean <= 0.0:
        return -float("inf")
        
    return float(survival_term + math.log(mu_mean))


def standing_diversity_trajectory(
    lineage_intervals: Sequence[tuple[float, float]],
    eval_times: Sequence[float] | np.ndarray,
) -> np.ndarray:
    """
    Primitive 5: Reconstructs standing diversity N(t) across arbitrary time points.
    Lineage i is active at t if s_i >= t >= e_i.
    
    Invariants:
      1. Output values are strictly non-negative integers.
      2. Monotonically 0 outside the span of all lineages.
    """
    times = np.asarray(eval_times, dtype=np.float64)
    n_times = len(times)
    counts = np.zeros(n_times, dtype=np.int64)
    
    for s, e in lineage_intervals:
        if s < e:
            continue
        mask = (times <= s) & (times >= e)
        counts[mask] += 1
        
    return counts
