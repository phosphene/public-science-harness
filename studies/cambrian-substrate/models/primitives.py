"""
Diagenetic Tiering Primitives — Pure Mathematical Functions.
Decomposed into clean, uncomplected coordinates following Hickey/Tellman principles.
Ref: Berner (1980), Boudreau (1996), Meysman et al. (2003).
"""

from __future__ import annotations

import math
from typing import Sequence
import numpy as np


def biodiffusion_kernel(
    z_mm: float | np.ndarray,
    z_max_mm: float,
    d_b0: float,
    sigma_b_mm: float = 5.0,
) -> float | np.ndarray:
    """
    Primitive 1: Organism-mediated biodiffusion coefficient as a function of depth.
    
    Invariants:
    1. Returns d_b0 for z <= z_max_mm.
    2. Attenuates smoothly (Gaussian tail) for z > z_max_mm.
    3. Strictly non-negative: D_b(z) >= 0 for all z >= 0.
    4. Monotonically non-increasing: D_b(z2) <= D_b(z1) for z2 > z1 >= z_max_mm.
    5. If z_max_mm == 0, returns pure boundary attenuation or zero.
    """
    if z_max_mm < 0.0 or d_b0 < 0.0 or sigma_b_mm <= 0.0:
        raise ValueError("Physical parameters (z_max, d_b0, sigma_b) must be non-negative.")

    if isinstance(z_mm, (int, float)):
        if z_mm < 0.0:
            raise ValueError("Depth z cannot be negative.")
        if z_mm <= z_max_mm:
            return float(d_b0)
        excess = z_mm - z_max_mm
        return float(d_b0 * math.exp(-0.5 * (excess / sigma_b_mm) ** 2))

    # Array handling
    z_arr = np.asarray(z_mm, dtype=np.float64)
    if np.any(z_arr < 0.0):
        raise ValueError("Depth z cannot contain negative coordinates.")
    
    out = np.empty_like(z_arr)
    mask_plateau = z_arr <= z_max_mm
    out[mask_plateau] = d_b0
    
    mask_tail = ~mask_plateau
    excess = z_arr[mask_tail] - z_max_mm
    out[mask_tail] = d_b0 * np.exp(-0.5 * (excess / sigma_b_mm) ** 2)
    return out


def respiration_sink(
    c_org: float | np.ndarray,
    o2: float | np.ndarray,
    k_c: float,
    k_m_o2: float = 2.0,
) -> float | np.ndarray:
    """
    Primitive 2: Respiration kinetics with Michaelis-Menten oxygen dependence.
    
    Invariants:
    1. Strictly non-negative: R(c, o2) >= 0 when c >= 0, o2 >= 0.
    2. Bounded above: R(c, o2) <= k_c * c.
    3. Approaches 0 as o2 -> 0 (hypoxic shutdown).
    4. Linear in c (first-order in organic substrate).
    """
    if k_c < 0.0 or k_m_o2 <= 0.0:
        raise ValueError("Kinetics constants must be positive.")
    
    c_arr = np.maximum(0.0, np.asarray(c_org, dtype=np.float64))
    o2_arr = np.maximum(0.0, np.asarray(o2, dtype=np.float64))
        
    limiter = o2_arr / (k_m_o2 + o2_arr)
    rate = k_c * c_arr * limiter
    
    if isinstance(c_org, (int, float)) and isinstance(o2, (int, float)):
        return float(rate)
    return rate


def diagenetic_divergence_1d(
    c_grid: np.ndarray,
    d_eff_grid: np.ndarray,
    dz_mm: float,
    advection_w_mm_per_yr: float = 0.0,
) -> np.ndarray:
    """
    Primitive 3: 1D Spatial divergence operator for advection-diffusion.
    Computes d(J)/dz where J = -D * dC/dz + w * C.
    Uses conservative finite volume interface flux discretization.
    
    Boundary conditions:
    - Dirichlet at surface (z=0): c_grid[0]
    - Zero-gradient (Neumann) at bottom (z=L): dC/dz = 0
    """
    n = len(c_grid)
    if n < 3:
        raise ValueError("Grid must contain at least 3 points.")
    if dz_mm <= 0.0:
        raise ValueError("Spatial step dz must be positive.")
        
    # Harmonize effective diffusion at cell interfaces (harmonic mean for flux continuity)
    d_inter = 0.5 * (d_eff_grid[:-1] + d_eff_grid[1:])
    
    # Diffusive flux at internal interfaces (1/2, 3/2, ..., N-3/2)
    # J_diff = - D * (C[i+1] - C[i]) / dz
    diff_flux = -d_inter * (c_grid[1:] - c_grid[:-1]) / dz_mm
    
    # Advective flux at internal interfaces (upwind scheme for w >= 0)
    w = advection_w_mm_per_yr
    if w >= 0.0:
        adv_flux = w * c_grid[:-1]
    else:
        adv_flux = w * c_grid[1:]
        
    total_interface_flux = diff_flux + adv_flux
    
    # Internal divergence dC/dt = - d(Flux)/dz
    # For interior cells i in [1, N-2]:
    dC_dt = np.zeros_like(c_grid)
    dC_dt[1:-1] = -(total_interface_flux[1:] - total_interface_flux[:-1]) / dz_mm
    
    # Boundary cells:
    # Surface cell (i=0) is fixed Dirichlet boundary condition in solver: dC/dt = 0
    dC_dt[0] = 0.0
    # Bottom cell (i=N-1) with Neumann dC/dz = 0 (zero diffusive flux at bottom)
    flux_bottom = 0.0 if w == 0.0 else w * c_grid[-1]
    dC_dt[-1] = -(flux_bottom - total_interface_flux[-1]) / dz_mm
    
    return dC_dt


def aerobic_niche_integral(
    z_grid_mm: np.ndarray,
    c_profile: np.ndarray,
    o2_profile: np.ndarray,
    o2_threshold: float = 2.0,
) -> float:
    """
    Primitive 4: Integrates accessible organic carbon in the oxygenated zone.
    Niche Volume = integral of C(z) dz over regions where O2(z) >= o2_threshold.
    
    Invariant:
    Monotonically increases as O2 penetration depth increases.
    """
    mask = o2_profile >= o2_threshold
    if not np.any(mask):
        return 0.0
        
    # Trapezoidal integration over the active mask
    z_sub = z_grid_mm[mask]
    c_sub = c_profile[mask]
    if len(z_sub) < 2:
        return 0.0
        
    return float(np.trapezoid(c_sub, z_sub) if hasattr(np, "trapezoid") else np.trapz(c_sub, z_sub))


def analytical_steady_state_exponential(
    z_mm: np.ndarray,
    c_0: float,
    d_total: float,
    k_decay: float,
) -> np.ndarray:
    """
    Exact analytical solution for 1D diffusion + first-order decay under constant D:
    C(z) = C_0 * exp(-z * sqrt(k / D))
    Used for exact property-based solver verification.
    """
    if d_total <= 0.0 or k_decay <= 0.0:
        raise ValueError("Diffusion and decay must be positive.")
    attenuation_scale = math.sqrt(k_decay / d_total)
    return c_0 * np.exp(-z_mm * attenuation_scale)
