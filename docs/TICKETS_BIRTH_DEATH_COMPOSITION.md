---
title: Macroevolutionary Birth-Death Engine: Genealogical Composition & Execution Plan
status: active
author: Ed Phil, Jan, and Flow (@feelingflowingbot)
date: 2026-11-16
---

# Macroevolutionary Birth-Death Engine: Genealogical Composition Plan

This ticket board operationalizes the canonical composition of our pure mathematical primitives into a typed, transparent, and reproducible macroevolutionary likelihood and parameter estimation engine (`studies/cambrian-substrate/models/`).

### Core Engineering Invariants:
1. **Genealogical Lineage Rehearsal:** Every module must open with a literate rehearsal of its precursors, historical literature context, and the exact mathematical pathologies it remedies.
2. **Pure Primitive Composition:** Functions compose the 5 canonical primitives (`birth_death_primitives.py`) and the horizon resampler (`horizon_coupled_resampler.py`) without global mutable state or monolithic God-script loops.
3. **Axiomatic Typing & Scoping:** Models inherit from `InvariantStatic` (`frozen=True, extra="forbid"`), keeping parameter priors, observed data tensors, and likelihood receipts strictly uncomplected.
4. **Property & Calibration Battery:** Hypothesis property tests and Gherkin BDD acceptance scenarios verify mathematical convergence, mass conservation, and stratigraphic calibration.

---

## Ticket Breakdown

| Ticket ID | Category | Title | Precursor Literature Rehearsal | Scope & Acceptance Criteria | Status |
|:---|:---|:---|:---|:---|:---|
| **PSH-BD-001** | Literate Specification | **Genealogical Precursor Rehearsal & Architecture Spec** | Kendall (1948), Bartlett (1949), Keiding (1975), Raup (1976), Foote (2000), Silvestro et al. (2014, 2019), van Holstein & Foley (2024). | Author literate markdown rehearsal tracing continuous-time birth-death likelihoods, conditionings, identifiability ridges, and diversity-dependence. Document the exact mathematical transition from scalar MCMC loops to vectorized likelihood evaluations. | **TODO** |
| **PSH-BD-002** | Composition Engine | **Stratigraphically Coupled Lineage Horizon Lifespan Evaluator** | Ausich & Bottjer (1982), Narbonne et al. (1987), Brasier et al. (1994). Resolves Anti-Pattern 2 (independent uniform scattering). | Compose `HorizonCoupledResampler` with occurrence timestamps to compute joint latent originations $s_i$ and extinctions $e_i$ across coupled horizons. Emit deterministic SHA-256 provenance receipts. | **TODO** |
| **PSH-BD-003** | Likelihood Engine | **Canonical Conditioned Birth-Death Likelihood Evaluator** | Keiding (1975), Silvestro et al. (2014). Resolves Anti-Pattern 1 (NHPP boundary smear) and Anti-Pattern 3 ($q$-$\mu$ ridge). | Implement `ConditionedBirthDeathLikelihood` composing Primitives 1–4. Evaluate joint log-likelihood $\log \mathcal{L}(\mathbf{D} \mid \lambda, \mu, q, \mathbf{s}, \mathbf{e})$. Support `HPP`, `TPP`, and tiering-compensated preservation modes without monolithic branching. | **TODO** |
| **PSH-BD-004** | Calibration Engine | **Taphonomically Compensated Diversity-Dependence Estimator** | Etienne et al. (2012), Rabosky (2013), Seilacher (1999), van Holstein & Foley (2024). | Implement `DiversityDependenceEstimator` evaluating guild speciation slopes ($Gl$). Ingest `cambrian_substrate.db` calibration views, strictly blocking unweighted body counts on infaunal burrowers and applying tiering depth ($Z_{\max}$) compensation. | **TODO** |
| **PSH-BD-005** | Diagnostics | **Multi-Chain Gelman-Rubin $\hat{R}$ and Nested ESS Verification** | Gelman & Rubin (1992), Brooks & Gelman (1998). Resolves Anti-Pattern 6 (chain concatenation masking). | Implement standalone convergence diagnostics asserting within-replicate $\text{ESS} > 200$ and across-chain $\hat{R} < 1.01$ before posterior summary reporting. | **TODO** |
| **PSH-BD-006** | Acceptance Suite | **BDD Scenarios & Continuous Integration Pipeline** | Phosphene CI Standards (`.github/workflows/ci.yml`). | Write declarative Gherkin features (`features/birth_death_composition.feature`) asserting horizon coupling, taphonomic compensation, and parameter recovery. Verify 100% green on GitHub Actions CI. | **TODO** |
