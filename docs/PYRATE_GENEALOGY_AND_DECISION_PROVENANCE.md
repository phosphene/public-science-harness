# PyRate Methodological Genealogy, Decision Provenance, and Enhancement Glossary

**Repository:** `phosphene/public-science-harness`  
**Topic Coordinate:** Topic 98577 (Public Evolutionary Science)  
**Parent Frameworks:**  
- `SPEC-genealogical-syntagma.md` (Semiotic triad: Seme / Pheme / Delome)  
- `SPEC-hickey-tellman-naming-discipline.md` (Coordinate cards & public language)  
- `docs/TRANSFORMS_PROVENANCE_AND_ANNOTATION.md` (Cryptographic receipts & epistemic ledgers)  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Standard & Methodological Reference  
**Date:** 2026-11-16  

---

## 1. Decision Provenance Architecture: The "What" and "Why" Chains

Every methodological choice, mathematical parameterization, and data transform in our public science modeling suite must be governed by an explicit **Decision Provenance Chain**.

A valid Decision Provenance Node consists of:
1. **The Context (Antecedent State):** The empirical dataset, modeling target, or mathematical boundary condition.
2. **The What (Intervention):** The exact specification, algorithm, or code transform introduced.
3. **The Why (Epistemic Warrant & Failure Mitigation):** The mathematical necessity, empirical pathology prevented, or literature precedent.
4. **The Verification Receipt:** Machine-verifiable test assertion, BDD acceptance scenario, or SHA-256 digest proving the invariant holds.

### Core Architectural Decision Log

| Decision ID | Context | The What | The Why | Verification Receipt |
|:---|:---|:---|:---|:---|
| **DEC-PYRATE-001** | Catastrophic boundary inference (Ediacaran-Cambrian GSSP, K-Pg) | **Regime-Matched Preservation Selection:** Mandatory comparison of `HPP` (Homogeneous) and `TPP` (Time-Variable) alongside `NHPP` (Non-Homogeneous). | PyRate default `NHPP` imposes a bell-shaped (PERT/Beta) curve assuming peak preservation mid-lifespan. Dense occurrences immediately preceding an abrupt boundary force inferred extinction times ($e_i$) forward into younger strata (Anti-Pattern 1). | `features/pyrate_enhancements.feature` Scenario 1; marginal likelihood comparison via stepping-stone sampling (`SS`). |
| **DEC-PYRATE-002** | Chronostratigraphic age uncertainty | **Horizon-Coupled Age Resampling:** Groups co-occurring fossils by unique geological bed/horizon, drawing a single latent offset $u_h \sim \text{Uniform}(0, 1)$ per horizon per replicate. | Independent uniform resampling of co-occurring fossils scatters synchronous assemblages across entire 5–10 Myr stages, flattening radiation pulses and generating false boundary spikes (Anti-Pattern 2). | Property test in `test_pyrate_horizon_resampling.py`; retains exact geological contemporaneity across MCMC replicates. |
| **DEC-PYRATE-003** | Sedimentary hiatuses & Lagerstätten intervals | **Covariate-Anchored Preservation & Ridge Regularization:** Penalizes extreme jump proposals ($>5\text{ Myr}^{-1}$) and conditions $q(t)$ on external rock availability proxies. | Sharp drops in fossil recovery create unidentifiable likelihood ridges where PyRate confounds drop in preservation ($q$) with an extinction surge ($\mu$) followed by a speciation surge ($\lambda$) (Anti-Pattern 3). | `test_pyrate_ridge_regularization.py`; asserts bounded diversification hazards under synthetic sampling drop. |
| **DEC-PYRATE-004** | Spatial heterogeneity & provincial bias | **Basin-Stratified Partitioning:** Mandates separate regional models across distinct paleobiogeographic provinces (e.g. South China vs. Laurentia). | Shifts in geographic sampling effort masquerade as global macroevolutionary rate shifts (Anti-Pattern 4). | Cross-basin consistency assertions in empirical calibration views. |
| **DEC-PYRATE-005** | Trace-fossil vs Body-fossil disparity in Cambrian infauna | **Stratigraphic Tiering Likelihood Weighting:** Overrides naive body counts ($N=5$) for soft-bodied infauna with calibrated burrow tiering depth ($Z_{\max} = 1.5 \to 45\text{ mm}$). | Soft-bodied burrowers (*Treptichnus*) radiated behaviorally, leaving abundant traces but negligible mineralized body fossils. Naive PyRate runs conclude infaunal extinction/failure (Anti-Pattern 5). | `v_calibrated_guild_diversity` SQLite view; epistemic annotation `annot-20261115-infaunal-taphonomic-bias` (Brasier et al. 1994). |
| **DEC-PYRATE-006** | MCMC replicate convergence diagnostics | **Nested Within-Replicate Convergence Enforcement:** Strict gating requiring Effective Sample Size ($\text{ESS} > 200$) and Gelman-Rubin ($\hat{R} < 1.01$) prior to posterior concatenation. | Concatenating MCMC chains across stratigraphic replicates without testing individual chain convergence masks non-convergence and conflates Monte Carlo error with stratigraphic error (Anti-Pattern 6). | Multi-chain diagnostic assertion suite. |

---

## 2. Intellectual Genealogy of PyRate and Its Enhancements

Following `SPEC-genealogical-syntagma.md`, we trace the semiotic and mathematical lineage across three planes:

```text
                  [Keiding 1975]
                  Continuous-time birth-death likelihood conditioned
                  on observation of at least one individual: P(K > 0 | s, e, q)
                                │
                                ▼
                  [Foote 2000 / Alroy 2008]
                  Boundary-crosser and three-timer taxonomic estimators
                  (Recognized Signor-Lipps edge truncation in fossil record)
                                │
                                ▼
                  [Silvestro et al. 2014, 2019: PyRate]
                  Hierarchical Bayesian joint estimation of speciation (λ),
                  extinction (μ), and preservation (q) via rjMCMC
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
[Cerny et al. 2021]                             [van Holstein & Foley 2024]
Demonstrated q-μ ridge instability              Empirical inversion of diversity-
over sedimentary hiatuses                       dependence slope (Gl > 0) in hominins
        │                                               │
        └───────────────────────┬───────────────────────┘
                                │
                                ▼
      [Phosphene Public Science Harness: PyRate Modernization]
      1. Horizon-Coupled Stratigraphic Latent Graph
      2. Regularized Continuous Shrinkage on Rates (Eliminating rjMCMC spikes)
      3. Covariate-Anchored Preservation Multipliers
      4. Taphonomic Override via Physical Substrate Tiering (Paper 01)
```

---

## 3. Glossary of Terms & Coordinate Cards

Under the **Hickey–Tellman–Frege discipline**, every technical term must be publicly grounded and assigned its genealogical coordinate:

### `:term/keiding-conditioning`
- **Sign:** $P(K_i > 0 \mid s_i, e_i, q_i) = 1 - \exp\left(-\int_{e_i}^{s_i} q_i(t)\,dt\right)$
- **Sense:** Conditioning the birth-death likelihood on the fact that an unobserved extinct lineage can only be sampled if it left at least one fossil in the geological record.
- **Genealogy:** Keiding (1975, *Annals of Statistics*); Silvestro et al. (2014, *Syst. Biol.*).
- **Public Domain Alignment:** Core probability invariant of continuous-time paleontological survival analysis.

### `:term/nhpp-boundary-trap`
- **Sign:** $\text{PERT}(s_i, e_i, m_i)$ boundary displacement artifact.
- **Sense:** The mathematical distortion where PyRate's non-homogeneous Poisson preservation model forces a taxon's estimated extinction time ($e_i$) millions of years beyond a known catastrophic boundary because dense occurrences right at the boundary are interpreted as a mid-lifespan peak ($m_i$).
- **Genealogy:** Identified by Silvestro et al. (2014); formally analyzed in `pyrate_methodological_evaluation_and_modernization_guide` (2026).
- **Mitigation:** Fallback to Homogeneous (`HPP`) or Time-Variable (`TPP`) models with marginal likelihood model selection.

### `:term/horizon-coupled-resampling`
- **Sign:** $\tau_{i,j} = b_{\text{young}, h} + u_h (b_{\text{old}, h} - b_{\text{young}, h}), \quad u_h \sim \text{Uniform}(0, 1)$
- **Sense:** A stratigraphic resampling protocol where all fossil occurrences recovered from the same geological horizon $h$ share a single stochastic draw $u_h$, preserving strict temporal contemporaneity across Monte Carlo replicates.
- **Genealogy:** Resolves Anti-Pattern 2 of legacy PyRate (independent uniform scattering).
- **Public Domain Alignment:** Stratigraphic sequence biostratigraphy / geochronological error propagation.

### `:term/taphonomic-identifiability-ridge`
- **Sign:** Equifinality between $q(t) \to 0$ and $\mu(t) \to \infty$.
- **Sense:** The inability of an unconstrained Poisson likelihood to distinguish between a genuine extinction pulse and an absence of sedimentary rock preservation.
- **Genealogy:** Raup (1976); Peters & Foote (2001); Cerny et al. (2021).
- **Mitigation:** Anchoring $\log q(t)$ to external sampling proxies ($\mathbf{X}_{r,t}$) such as formation counts or non-target taphonomic control groups.

### `:term/ichnofacies-tiering-compensation`
- **Sign:** $\mathcal{V}_{\text{aerobic}}(t) \propto A \cdot Z_{\max}(t)$
- **Sense:** Correcting macroevolutionary carrying capacity priors for soft-bodied infauna using continuous physical trace-burrow depth ($Z_{\max}$) rather than distorted raw body-fossil counts ($N_{\text{body}}$).
- **Genealogy:** Ausich & Bottjer (1982); Seilacher (1999); Paper 01 Diagenetic Tiering Model (`public-science-harness` Model 1).
- **Public Domain Alignment:** Ichnology, taphonomy, and the Agronomic Revolution.

### `:term/diversity-dependence-slope-gl`
- **Sign:** $Gl = \frac{d \log \lambda}{d N}$ (speciation feedback parameter)
- **Sense:** The rate at which per-lineage speciation changes as standing clade richness ($N$) increases. $Gl < 0$ denotes competitive niche saturation (Cambrian metazoans: $-0.031$ to $-0.089$). $Gl > 0$ denotes generative niche construction (van Holstein & Foley 2024 hominins: $+0.290$).
- **Genealogy:** Rabosky (2013); Etienne et al. (2012); Silvestro et al. (2015); van Holstein & Foley (2024).
