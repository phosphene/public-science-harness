# Canonical Precursors, Mathematical Genealogy, and Literature Rehearsal for Normal Science Reproduction

**Document Coordinate:** `docs/CANONICAL_PRECURSORS_AND_LITERATURE_REHEARSAL.md`  
**Repository:** `phosphene/public-science-harness`  
**Topic:** Topic 98577 (Public Evolutionary Science)  
**Parent Frameworks:**  
- `docs/TICKETS_BIRTH_DEATH_COMPOSITION.md` (Ticket PSH-BD-001)  
- `docs/PYRATE_GENEALOGY_AND_DECISION_PROVENANCE.md`  
- `SPEC-ashby-epistemological-boundary.md`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Canonical Literature Specification  
**Date:** 2026-11-16  

---

## 1. The Methodological Imperative: Reproducing Normal Science Under Austere Inference

In public evolutionary science, our goal is not to invent ungrounded, idiosyncratic formalisms, nor to dismiss the hard-won achievements of paleobiology and applied probability. 

Our imperative is to **reproduce the state of normal science** at its highest rigorous standard, but to do so under **austere conditions of inference**:
1. **Preserving the Best of What Is Available:** Classical continuous-time birth-death theory (Kendall, Bartlett, Keiding), taphonomic sampling discipline (Raup, Foote, Marshall), and diversity-dependent feedback (Etienne, Rabosky, van Holstein & Foley).
2. **Eliminating Compensatory Software Pathology:** Purging the 8,000-line monolithic God-script patterns (lossy pre-processing, independent uniform age scrambling, destructive data flattening, unconstrained parameter ridges).
3. **Preserving the Observational Substrate Intact:** Treating the physical rock column—beds, lithologies, horizons, and taphonomic modes—as an immutable, unmutated relational foundation.
4. **Demarcating Physical Permissiveness from Causal Engines:** Treating mathematical models (like 1D diagenesis or birth-death likelihoods) as bounded calculations of geometric and kinetic boundary conditions, never as ungrounded causal "proofs" of evolutionary prime movers.

---

## 2. Detailed Precursor Literature Rehearsal

### A. The Stochastic Process Lineage: Continuous-Time Markov Transitions
* **David G. Kendall (1948, 1949):**
  - *Primary Text:* "On the Generalized 'Birth-and-Death' Process" (*Annals of Mathematical Statistics*, 1948); "Stochastic Processes and Population Growth" (*JRSS-B*, 1949).
  - *The Foundation:* Formulated continuous-time Markov population dynamics where individual lineages undergo instantaneous birth hazard $\lambda(t)$ and death hazard $\mu(t)$. Kendall solved the differential-difference forward Kolmogorov equations, deriving the probability generating functions for clade size and extinction probabilities over time.
  - *The Invariant:* Lineages transition independently conditioned on current state; extinction is an absorbing boundary state ($N=0 \implies N(t')=0 \ \forall t' > t$).
* **M. S. Bartlett (1949, 1955):**
  - *Primary Text:* "Some Evolutionary Stochastic Processes" (*JRSS-B*, 1949); *An Introduction to Stochastic Processes* (1955).
  - *The Foundation:* Extended birth-death formulations to density-dependent and epidemic kinetics, laying the groundwork for non-linear feedback on turnover rates.

### B. The Observational Incompleteness Breakthrough: Conditioning on Sampling
* **Niels Keiding (1975):**
  - *Primary Text:* "Maximum Likelihood Estimation in the Birth-and-Death Process" (*Annals of Statistics*, 1975).
  - *The Crucial Problem:* If an extinct lineage lived and died without leaving an observation, it never enters the observation register. Naive maximum likelihood over observed lineages underestimates extinction ($\mu$) and overestimates speciation ($\lambda$) because the zero-observation class is truncated.
  - *The Mathematical Solution:* Condition the joint probability on leaving at least one sampled record ($K_i > 0$):
    $$P(K_i > 0 \mid s_i, e_i, q_i) = 1 - \exp\left(-\int_{e_i}^{s_i} q_i(t) \, dt\right)$$
  - *The Normal Science Standard:* This conditioning factor is the non-negotiable denominator of any principled paleontological likelihood.

### C. The Stratigraphic & Taphonomic Foundation
* **David M. Raup (1972, 1976):**
  - *Primary Text:* "Taxonomic Diversity During the Phanerozoic" (*Science*, 1972); "Species Diversity in the Phanerozoic: An Interpretation" (*Paleobiology*, 1976).
  - *The Warning:* Apparent taxonomic diversity curves in the fossil record mirror the volume and surface area of exposed sedimentary rock ("the geological filter"). If preservation intensity $q(t)$ is treated as unconstrained, inference algorithms confuse an unconformity or drop in rock availability with an extinction pulse.
* **Philip W. Signor & Jere H. Lipps (1982):**
  - *Primary Text:* "Sampling Bias, Gradual Extinction Patterns, and Catastrophes in the Fossil Record" (*Geological Society of America Special Papers*, 1982).
  - *The Principle:* The Signor-Lipps effect proves that observed First Appearance Datums (FAD) always post-date true biological origination ($s_i \ge \text{FAD}_i$), and observed Last Appearance Datums (LAD) always pre-date true biological extinction ($e_i \le \text{LAD}_i$). Sudden catastrophic extinctions are artificially smeared into gradual declines.
* **Charles R. Marshall (1990, 1994, 1997):**
  - *Primary Text:* "Confidence Intervals on Stratigraphic Ranges" (*Paleobiology*, 1990); "Using Presence/Absence Data to Measure Rarefaction" (1994).
  - *The Mechanism:* Derived analytical confidence intervals on fossil range endpoints based on the physical distribution and spacing of fossiliferous horizons within the local stratigraphic column.
* **Mike Foote (2000):**
  - *Primary Text:* "Origination and Extinction Components of Taxonomic Diversity: General Problems" (*Paleobiology*, 2000).
  - *The Discrete Benchmark:* Established discrete per-capita boundary-crosser rates ($p, q$), providing the exact comparative baseline against which continuous-time Poisson rates are validated.

### D. Modern Diversification & Niche Dynamics
* **Rampal S. Etienne et al. (2012) & Dan L. Rabosky (2006, 2013):**
  - *Primary Text:* "A New Dynamic Model of Diversity-Dependent Diversification" (*Syst. Biol.*, 2012); "Diversity-Dependence and the Regulation of Clade Diversity" (*Ann. Rev. Ecol. Evol. Syst.*, 2013).
  - *The Formulation:* Replaced static birth-death rates with explicit dependence on standing clade richness $N(t)$:
    $$\lambda(N) = \lambda_0 \exp(Gl \cdot N) \quad \text{or} \quad \max(0, \lambda_0 + Gl \cdot N)$$
* **Daniele Silvestro et al. (2014, 2019):**
  - *Primary Text:* "Bayesian Inference of Species Turnovers from Fossil Occurrence Data" (*Syst. Biol.*, 2014); "Improved Estimation of Macroevolutionary Rates" (*Paleobiology*, 2019).
  - *The Achievement:* Jointly estimated latent lifespans $(s_i, e_i)$, continuous preservation rate $q$, and diversification hazards $(\lambda, \mu)$ without requiring a resolved phylogeny.
  - *The Engineering Breakdown:* Implemented as an 8,143-line monolithic scalar script (`PyRate.py`) with lossy pre-processing, independent uniform age jittering, and unanchored $q$-$\mu$ ridges.
* **Laura van Holstein & Robert A. Foley (2024):**
  - *Primary Text:* "Diversity-Dependent Speciation and Extinction in Hominins" (*Nature Ecology & Evolution*, 2024).
  - *The Empirical Benchmark:* Demonstrated that non-hominin mammalian clades follow classical negative diversity-dependence ($Gl < 0$, competitive niche saturation), whereas *Homo* uniquely inverts this slope ($Gl > 0$, generative niche construction via cultural and technological accumulation).

---

## 3. The Architecture of Reproduction

By decomposing this fifty-year canon into pure, typed mathematical primitives (`studies/cambrian-substrate/models/birth_death_primitives.py`) and preserving the physical rock column (`horizon_coupled_resampler.py`), we achieve:

1. **Axiomatic Clarity:** Pure functional primitives with zero global mutable state.
2. **Stratigraphic Fidelity:** Geological horizons preserved as first-class relational entities; co-occurring fossils retain shared temporal offsets across all iterations.
3. **Epistemic Rigor:** Soft-bodied infauna evaluated via joint trace-and-body likelihoods with physical tiering depth overrides ($Z_{\max} = 1.5 \to 45\text{ mm}$), preventing the artificial "infaunal failure" artifact of legacy scripts.
4. **Reproducibility:** Self-contained, headless CLI drivers verified by Hypothesis property tests, Gherkin BDD scenarios, and automated GitHub Actions CI.
