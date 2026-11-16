# Canonical Conditioned Birth-Death Likelihood Engine: Mathematical Rehearsal & Literate Specification (PSH-BD-003)

**Document Coordinate:** `studies/cambrian-substrate/models/CONDITIONED_LIKELIHOOD_LITERATE.md`  
**Repository:** `phosphene/public-science-harness`  
**Mathematical Canon:** Kendall (1948), Bartlett (1949), Keiding (1975), Foote (1997, 2000), Silvestro et al. (2014, 2019)  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Mathematical Specification & Architectural Contract  
**Date:** 2026-11-16  

---

## 1. The Precursor Lineage: Rehearsal of the Canon

When an empirical paleontologist measures fossil occurrences in rock horizons, we seek to infer the continuous-time rates of lineage origination ($\lambda$), extinction ($\mu$), and preservation/sampling ($q$).

This problem was not solved by ad-hoc curve fitting; it rests on a foundational 50-year lineage in applied probability:

### A. The Kendall-Bartlett Continuous-Time Markov Foundation
David Kendall (1948) and Maurice Bartlett (1949) solved the master equations for continuous-time linear birth-death Markov processes:
$$\frac{\partial P_n(t)}{\partial t} = \lambda (n-1) P_{n-1}(t) - (\lambda + \mu) n P_n(t) + \mu (n+1) P_{n+1}(t)$$
From this, the fundamental probability generating function $G(z, t)$ yielded the exact survival probability $P(\text{lineage survives to } t)$ and extinction probability $P(\text{extinct by } t)$.

### B. The Keiding (1975) Survival & Observation Conditioning
Niels Keiding recognized that historical observation records are severely **conditioned on ascertainment**: we only observe lineages that left at least one surviving record.
For a lineage originating at unobserved time $s_i$ and going extinct at unobserved time $e_i$ ($s_i \ge \text{FAD}_i \ge \text{LAD}_i \ge e_i$), the total number of fossil finds $K_i$ follows a Poisson process with rate $q$.
The probability of observing at least one fossil during its lifespan $(s_i - e_i)$ is:
$$P(K_i > 0 \mid s_i, e_i, q) = 1 - \exp\left( -q (s_i - e_i) \right)$$
Keiding proved that failing to divide the likelihood by this conditioning probability inflates the estimated extinction rate $\mu$ by treating unobserved extinct lineages as if they had a zero probability of escaping detection.

### C. The Silvestro et al. (2014) Joint Likelihood Decomposition
Silvestro, Schnitzler, Liow, Harmon, and Salamin unified the Kendall birth-death process with the Poisson preservation hazard into a clean joint log-likelihood:
$$\log \mathcal{L}(\mathbf{D} \mid \lambda, \mu, q, \mathbf{s}, \mathbf{e}) = \sum_{i=1}^N \left[ \log \mathcal{L}_{\text{occ}}(k_i \mid s_i, e_i, q) + \log \mathcal{L}_{\text{surv}}(s_i, e_i \mid \lambda, \mu) - \log P(K_i > 0 \mid s_i, e_i, q) \right]$$

Where:
1. **Occurrence Log-Likelihood:**
   $$\log \mathcal{L}_{\text{occ}}(k_i \mid s_i, e_i, q) = k_i \ln(q) - q (s_i - e_i)$$
2. **Lineage Survival Log-Likelihood:**
   $$\log \mathcal{L}_{\text{surv}}(s_i, e_i \mid \lambda, \mu) = - (\lambda + \mu)(s_i - e_i) + \ln(\mu) \quad (\text{if extinct})$$
3. **Keiding Conditioning Normalizer:**
   $$\ln P(K_i > 0 \mid s_i, e_i, q) = \ln\left(1 - \exp\left(-q (s_i - e_i)\right)\right)$$

---

## 2. Pathologies of Legacy Implementations (PyRate Pitfalls Remedied)

While the mathematical canon is pure, legacy software implementations (such as standalone PyRate scripts) introduced severe software pathologies that our engine explicitly remedies:

| Legacy PyRate Pathology | Mathematical Consequence | Canonical Remedy (PSH-BD-003) |
|:---|:---|:---|
| **1. The NHPP Boundary Smear** | Truncating Poisson processes with smooth polynomial hats smeared sharp extinction boundaries across 10 Myr. | **Piecewise Homogeneous Preservation:** Exact epoch-wise intervals without artificial boundary smoothing. |
| **2. Independent Horizon Jittering** | Independently resampling ages for occurrences in the same bed destroyed bed contemporaneity. | **Coupled Horizon Realization:** Ingests `StratigraphicEvaluationReceipt`, forcing all occurrences in a quarry bed to share a single realization time $\tau_h$. |
| **3. The $q$-$\mu$ Identifiability Ridge** | Unconstrained MCMC runs on sparse datasets wander along $q \cdot \lambda / \mu \approx \text{const}$. | **Explicit Ridge Detection & Bounded Priors:** Monitors likelihood Hessian condition number; flags flat parameter valleys. |
| **4. Monolithic God-Script Branching** | 5,000-line monolithic scripts blending parsing, likelihoods, and plotting with global mutable state. | **Pure Primitive Composition:** Composes Primitives 1–4 from `birth_death_primitives.py` into an immutable `InvariantStatic` evaluator. |

---

## 3. The Composition Architecture

The engine accepts:
1. `cohort_receipt: StratigraphicEvaluationReceipt`: The evaluated FAD/LAD envelopes and preservation channels from `lineage_horizon_evaluator.py`.
2. `latent_spans: dict[str, tuple[float, float]]`: The candidate true origination and extinction boundaries $(s_i, e_i)$ satisfying $s_i \ge \text{FAD}_i \ge \text{LAD}_i \ge e_i \ge 0$.
3. `parameters: BirthDeathParameters`: The macroevolutionary rates $(\lambda, \mu, q)$ and optional diversity-dependence slopes $(Gl, Gm)$.

It evaluates the exact log-likelihood decomposition vectorially and deterministically, emitting an immutable `BirthDeathLikelihoodReceipt` sealed with a SHA-256 digest.
