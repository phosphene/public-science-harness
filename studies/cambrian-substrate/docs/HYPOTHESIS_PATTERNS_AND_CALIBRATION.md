# Hypothesis Testing Patterns, Conservation Standards, and Substrate Invariants

## Executive Mandate

This document codifies the property testing standards and physical conservation invariants in `cambrian-substrate`.

In modeling diagenetic tiering, bioturbational mixing, and vertical substrate restructuring (Droser & Bottjer 1989 ichnofabric indices BI 1 to BI 5), continuous depth coordinates $z \in [0, 200]\text{ cm}$ and diffusion coefficients $D_{b0}$ must strictly respect physical mass conservation, asymptotic exponential decay, and non-negativity.

---

## 1. Input Geometry and Generator Hygiene

### 1.1 Strict Physical and IEEE-754 Finite-Domain Hygiene
* Depth $z$, mixed layer depth $z_{\text{max}}$, and biodiffusion rates $D_{b0}$ must be strictly positive, non-NaN, non-infinite, and non-subnormal:
  `allow_nan=False, allow_infinity=False, allow_subnormal=False`.

---

## 2. Invariants and Variational Defect Hunting (`hypothesis.target()`)

### 2.1 Physical Conservation and Plateau Invariants
* For all $z \le z_{\text{max}}$, $D_b(z) \equiv D_{b0}$.
* For all $z > z_{\text{max}}$, $\frac{\partial D_b}{\partial z} \le 0$ (monotonic decrease).
* Variational residuals are exposed directly to `hypothesis.target()` to verify asymptotic convergence to zero at deep substrate layers.
