# Diagenetic Tiering & Substrate Dynamics: Genealogical Derivation & Primitive Decomposition

**Study Coordinate:** `studies/cambrian-substrate/models/`  
**Authors:** Ed Phil & Flow (`@feelingflowingbot`)  
**Status:** Living Specification & Mathematical Derivation  
**Date:** 2026-11-16  

---

## 1. Intellectual Genealogy (The Seme / Pheme / Delome Triad)

Following `SPEC-genealogical-syntagma.md`, we trace the physical substrate and diagenetic models from their ancestral geochemical roots to our 1D PDE / ODE solver:

```text
                  [Berner 1980: Early Diagenesis]
                  General diagenetic equation for porewater & solid phase
                  (Pure diffusive-advective sediment transport)
                                │
                                ▼ [Biological Coupling]
[Boudreau 1996 / Meysman 2003]            [Droser & Bottjer 1986 / Ausich 1982]
Biodiffusion & Non-local Biotic Transport  Ichnofabric Index (ii1-ii5) &
(Benthic boundary mixing D_b)              Tiering Depth Invariants (Z_max)
       │                                          │
       └────────────────────┬─────────────────────┘
                            │
                            ▼
              [Seilacher 1999: Agronomic Revolution]
              Substrate revolution: microbial mat sealing (2D) to
              active infaunal mining & vertical bio-irrigation (3D)
                            │
                            ▼
              [Phosphene Public Science Harness: Paper 01]
              Coupled Diagenetic Infaunal Tiering Model
              (Analytical steady-state & MOL numerical ODE/PDE solver)
```

### Triadic Mapping:
1. **`:seme/lineage`:**
   - `:term/biodiffusion`: Organism-induced random mixing of sediment particles and porewater ($D_b$).
   - `:term/infaunal-tiering`: Depth-stratified vertical niche segregation ($Z_{\max}$).
   - `:term/respiration-ceiling`: Aerobic vs anaerobic diagenetic consumption bounds ($R_{\text{met}}$).
2. **`:pheme/priors`:**
   - **Berner (1980):** Classic early diagenesis equation with solid deposition velocity $w$ and molecular diffusion $D_0$.
   - **Boudreau (1996) / Meysman et al. (2003):** Formulation of biodiffusion profiles: constant or Gaussian attenuation over the mixed layer ($z \le Z_{\max}$).
   - **Droser & Bottjer (1986) / Mángano & Buatois (2014):** Quantitative Cambrian ichnofabric expansion: Fortunian Stage 1 ($Z_{\max} \approx 30\text{–}45\text{ mm}$, *Treptichnus pedum*) expanding to Stage 3–5 ($Z_{\max} \ge 80\text{–}120\text{ mm}$, arthropod and priapulid deep tiering).
3. **`:delome/derivation`:**
   - **Ancestral Form (Berner 1980):** 
     $$\frac{\partial C}{\partial t} = D_0 \frac{\partial^2 C}{\partial z^2} - w \frac{\partial C}{\partial z} - k C$$
   - **Biological Invariant Transformation:**
     Introduce space-dependent biological mixing $D_b(z; Z_{\max})$ and non-linear metabolic consumption $R_{\text{met}}(C, O_2)$:
     $$\frac{\partial C}{\partial t} = \frac{\partial}{\partial z} \left( [D_0 + D_b(z; Z_{\max})] \frac{\partial C}{\partial z} \right) - w \frac{\partial C}{\partial z} - k C$$

---

## 2. Decompose into Primitives (Tellman / Hickey Clean Coordinates)

To avoid complecting biological mixing, molecular transport, and metabolic kinetics into a single monolithic loop, we decompose the system into 4 pure mathematical primitives:

### Primitive 1: Depth Profile & Biodiffusion Kernel (`biodiffusion_kernel`)
- **Signature:** `D_b(z: float, z_max: float, D_b0: float) -> float`
- **Definition:**
  $$D_b(z) = \begin{cases} D_{b0} & \text{for } 0 \le z \le Z_{\max} \\ D_{b0} \cdot \exp\left(-\frac{(z - Z_{\max})^2}{2 \sigma_b^2}\right) & \text{for } z > Z_{\max} \end{cases}$$
- **Invariant:** Monotonically non-increasing with depth; strictly non-negative; zero when $Z_{\max} = 0$ (Ediacaran microbial mat ground state).

### Primitive 2: Reaction Flux & Respiration Kinetics (`respiration_flux`)
- **Signature:** `metabolic_sink(C: float, O2: float, k_c: float, K_m: float) -> float`
- **Definition:**
  $$R(C, O_2) = k_c \cdot C \cdot \frac{O_2}{K_m + O_2}$$
- **Invariant:** Non-negative; bounded above by $k_c C$; smoothly approaches zero as $O_2 \to 0$ (Michaelis-Menten limit).

### Primitive 3: Spatial Discretization & Flux Operator (`diagenetic_flux_1d`)
- **Signature:** `compute_spatial_divergence(C_grid, D_grid, dz, w) -> dC_dt_transport`
- **Definition:**
  $$\left[ \frac{\partial J}{\partial z} \right]_i = \frac{J_{i+1/2} - J_{i-1/2}}{\Delta z}$$
  using central difference for diffusion and upwind flux for advection.
- **Invariant:** Total mass conservation under zero boundary fluxes ($\sum \Delta C = 0$).

### Primitive 4: Available Aerobic Niche Volume & Carrying Capacity (`aerobic_niche_integral`)
- **Signature:** `integrate_niche_volume(C_profile, O2_profile, dz, O2_threshold) -> float`
- **Definition:**
  $$\mathcal{V}_{\text{aerobic}} = \int_0^{Z_{\text{depth}}} \mathbb{I}(O_2(z) \ge O_2^{\text{crit}}) \cdot C(z) \, dz$$
- **Invariant:** Monotonically non-decreasing with increasing $Z_{\max}$ (Agronomic expansion).

---

## 3. Calibrated Analytical Baselines

Under uniform steady-state mixing ($D = D_0 + D_b$, $w \approx 0$, first-order consumption $k$), the system admits the exact analytical solution:
$$C(z) = C_0 \cdot \exp\left( - \sqrt{\frac{k}{D}} \cdot z \right)$$
$$\text{Penetration Scale } \lambda = \sqrt{\frac{D}{k}}$$

This provides an exact closed-form benchmark for property-based testing and solver tolerance verification.
