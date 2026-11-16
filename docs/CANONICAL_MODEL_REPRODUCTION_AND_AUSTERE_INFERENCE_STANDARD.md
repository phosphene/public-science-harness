# Canonical Model Reproduction & Austere Inference Standard

**Document Coordinate:** `docs/CANONICAL_MODEL_REPRODUCTION_AND_AUSTERE_INFERENCE_STANDARD.md`  
**Repository:** `phosphene/public-science-harness`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Standard & Methodological Charter  
**Date:** 2026-11-16  

---

## 1. The Core Methodological Imperative

> *"And then for each one we must reproduce the model that is canonical and we must be austere about the reality of its application and be very bounded and careful with any attempts at inference."* — Ed Phil (2026-11-16)

Whenever we approach an empirical domain—whether Cambrian stratigraphic turnovers, hominin radiations, plastome degradation in parasitic plants, or bacterial long-term evolution—we adhere to a four-stage discipline:

1. **Native Raw Preservation:** The empirical observations remain preserved in their native, uncompressed formats (TSV, CSV, XLSX, GBK) without lossy JSON transcoding.
2. **Canonical Model Reproduction:** Before proposing any novel hypothesis, alternative architecture, or speculative supposition, we reproduce the **canonical normal science model** established in that field's literature. We do not caricature existing methods; we implement their mathematical engines with exact fidelity.
3. **Austere Application Review:** We document the reality of the canonical model's physical application: its sampling limits, identifiability ridges, structural assumptions, and where the empirical substrate pushes the model beyond its mathematical validity.
4. **Bounded Inference:** Any inference drawn must be strictly demarcated: distinguishing between empirical observations (grounded in rocks or sequencing), illustrative physical calculations, and explicit speculative suppositions.

---

## 2. The Four Domain Batteries: Canonical Baselines & Austere Limits

```
                                DOMAIN METHODOLOGICAL MATRIX
┌──────────────────────┬───────────────────────────────┬───────────────────────────────┬───────────────────────────────┐
│ Empirical Domain     │ Canonical Model Engine        │ Mathematical Literature       │ Austere Reality & Limits      │
├──────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ 1. Cambrian Turnovers│ Continuous-Time Birth-Death-  │ Kendall (1948), Bartlett      │ 57.8% singletons; 87 bed      │
│                      │ Sampling Process (BDS)        │ (1949), Keiding (1975),       │ clusters; infaunal body count │
│                      │                               │ Foote (1997), Silvestro (2014)│ = 0 in Fortunian; identifi-   │
│                      │                               │                               │ ability ridge between q and μ.│
├──────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ 2. Hominin Diversity-│ Multi-Rate Diversity-Dependent│ Rabosky & Lovette (2008),     │ Small clade size (17 species);│
│    Dependence        │ Speciation/Extinction (DD)    │ Etienne et al. (2012),        │ high sensitivity to taxonomic │
│                      │                               │ Van Holstein & Foley (2024)   │ lump/split; preservation      │
│                      │                               │                               │ heterogeneity in East Africa. │
├──────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ 3. Plastome Genome   │ Phylogenetic Generalized Least│ Felsenstein (1985), Pagel     │ Relaxed selection makes same  │
│    Reduction         │ Squares (PGLS) & Discrete     │ (1994, 1999), Wicke et al.    │ directional prediction;       │
│                      │ Markov Character State Models │ (2013, 2016), Lewis (2001)    │ independent Cuscuta mashup;   │
│                      │ (Mk models)                   │                               │ non-continuous fractional data│
├──────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ 4. LTEE Bacterial    │ Clonal Interference & Periodic│ Lenski et al. (1991), Gerrish │ Selective sweeps drag neutral │
│    Evolution         │ Selection Kinetics            │ & Lenski (1998), Good et al.  │ mutations; discrete bursty    │
│                      │                               │ (2017), Tenaillon et al.(2016)│ loss breaks smooth ODEs.      │
└──────────────────────┴───────────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

## 3. Domain 1: Cambrian Substrate & Lineage Turnover

### Canonical Reproduction
- **The Engine:** Continuous-time Markov birth-death process conditioned on sampling and survival:
  $$\mathcal{L}(\mathbf{X} \mid \lambda, \mu, q) = \prod_{i=1}^N \mathcal{L}_i(t_{\text{FAD}, i}, t_{\text{LAD}, i}, k_i \mid \lambda, \mu, q)$$
  Following the canonical derivations of Kendall (1948), Keiding (1975), Foote (1997), and Silvestro et al. (2014).

### The Austere Application Reality
1. **The Singleton Trap:** Over **57.8% of taxa** appear exactly once ($k_i = 1$). A model attempting to infer individual taxon lifespans collapses unless strictly constrained by a shared, global preservation hazard $q$.
2. **Bed Contemporaneity vs Independent Resampling:** The 1,000 occurrences condense into 87 distinct collection horizons. Resampling occurrence dates independently (PyRate Anti-Pattern 2) breaks the stratigraphic reality that organisms in the same bedding plane lived together.
3. **The Infaunal Taphonomic Chiasm:** Body fossils have a 126:1 predator-to-infauna disparity, with zero infaunal bodies in the Fortunian. The canonical body-fossil model cannot infer infaunal dynamics without coupled ichnological trace evidence ($Z_{\max}$).

---

## 4. Domain 2: Hominin Diversity-Dependence

### Canonical Reproduction
- **The Engine:** Linear diversity-dependent speciation and extinction:
  $$\lambda(N_t) = \lambda_0 + Gl \cdot N_t, \qquad \mu(N_t) = \mu_0 + Gm \cdot N_t$$
  Reproduction of the Van Holstein & Foley (2024) PyRate MCMC configuration (Broad/Fine × NHPP/TPP).

### The Austere Application Reality
1. **Sample Scale Limits:** The entire hominin clade consists of just 17 recognized species (7 *Homo*, 10 non-*Homo*) across 4.2 Myr. Statistical power is inherently constrained.
2. **Taxonomic Lumping vs Splitting Sensitivity:** Reclassifying *Homo ergaster* as *Homo erectus* or lumping *Australopithecus anamensis* directly shifts $N_t$, altering $Gl$ estimates.
3. **Taphonomic Heterogeneity:** Rift Valley depositional basins have idiosyncratic preservation pulses. Inferences about positive diversity-dependence must be bounded by explicit awareness that human tool manufacture may increase the archaeological visibility of later species.

---

## 5. Domain 3: Parasitic Plant Plastome Degradation

### Canonical Reproduction
- **The Engine:** 
  1. Continuous trait evolution on phylogenies: Phylogenetic Generalized Least Squares (PGLS, Felsenstein 1985).
  2. Discrete morphological state transitions: Continuous-time Markov models (Mk models, Pagel 1994, Lewis 2001) evaluating transition rates between functional states:
     $$\text{Present} \xrightarrow{q_{01}} \text{Pseudogenized} \xrightarrow{q_{12}} \text{Deleted}$$

### The Austere Application Reality
1. **Taxonomic Conflation:** The 8-taxa matrix historically mixed true Orobanchaceae (*Epifagus*, *Conopholis*) with dodders (*Cuscuta*, Convolvulaceae). The canonical model must be reproduced on true monophyletic clades separately before evaluating cross-family convergence.
2. **Relaxed Selection Equifinality:** Total genome shrinkage is an inevitable consequence of relaxed selection. To achieve discriminating inference, the canonical model must test the **hierarchical sequence of gene shedding** (bioenergetics $\to$ light reactions $\to$ ATP synthase $\to$ translation) against neutral deletion models.
3. **NCBI Artifact Filtration:** All analyses must apply a hard $L > 10,000\text{ bp}$ filter to eliminate partial PCR marker fragments (e.g., the 71 bp records).

---

## 6. Domain 4: Microbial Experimental Evolution (LTEE)

### Canonical Reproduction
- **The Engine:** Clonal interference, periodic selection, and dynamic trajectory likelihoods (Lenski et al. 1991, Gerrish & Lenski 1998, Good et al. 2017).

### The Austere Application Reality
1. **Genetic Hitchhiking:** In asexual populations, selective sweeps cause passenger mutations to fix rapidly. A sudden step-drop in metabolic function count cannot be modeled as a smooth exponential decay without acknowledging that hitchhiking breaks Poisson rate independence.
2. **Discrete Multi-Phase Trajectories:** Adaptation in LTEE is biphasic or multi-phased (rapid early gains followed by power-law or logarithmic slowing), punctuated by hypermutator transitions.

---

## 7. Bounded Inference Protocol

Whenever an empirical calculation or model evaluation is executed within this harness, the final output must explicitly state its **Epistemic Classification**:
- `[EMPIRICAL_OBSERVATION]`: Directly observed in the rock, fossil, or sequence data.
- `[CANONICAL_REPRODUCTION]`: Strict execution of the normal-science mathematical model from the literature.
- `[AUSTERE_LIMITATION]`: Where the data sparseness or assumptions bound the validity of the result.
- `[SPECULATIVE_SUPPOSITION]`: Any counterfactual hypothesis or sensitivity envelope framed under conditions of empirical absence.
