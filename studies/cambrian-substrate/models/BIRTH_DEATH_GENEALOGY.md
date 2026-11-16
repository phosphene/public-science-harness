# Macroevolutionary Birth-Death & Preservation Dynamics: Canonical Primitives

**Study Coordinate:** `studies/cambrian-substrate/models/`  
**Authors:** Ed Phil & Flow (`@feelingflowingbot`)  
**Status:** Canonical Primitive Specification  
**Date:** 2026-11-16  

---

## 1. Intellectual Lineage & semiotic Triad

Following `SPEC-genealogical-syntagma.md`, we trace the birth-death preservation process to its root mathematical primitives:

```text
                  [Kendall 1948 / Bartlett 1949]
                  Generalized continuous-time Markov birth-death processes
                                │
                                ▼
                  [Keiding 1975]
                  Conditioned birth-death likelihood with incomplete observation:
                  P(K > 0 | s, e, q) = 1 - exp(-∫ q(t) dt)
                                │
                                ▼
                  [Nee, May & Harvey 1994 / Foote 2000]
                  Reconstructed evolutionary lineages & per-capita rate metrics
                                │
                                ▼
                  [Silvestro et al. 2014, 2019 / Etienne et al. 2012]
                  Diversity-dependent feedback on speciation and extinction:
                  λ(N) = λ_0 exp(Gl * N),  μ(N) = μ_0 exp(Gm * N)
                                │
                                ▼
                  [Canonical Primitives Suite]
                  Decomposed, pure functional implementation in public-science-harness
```

---

## 2. The 5 Canonical Primitives

### Primitive 1: `keiding_sampling_probability(s, e, q)`
- **Mathematical Form:**
  $$P(K > 0 \mid s, e, q) = 1 - \exp\left( - \int_e^s q(t) \, dt \right)$$
- **Sense:** Conditioning probability that a lineage spanning true origination $s$ and extinction $e$ leaves at least one preserved fossil given sampling rate $q(t)$.
- **Invariants:**
  - $0 \le P(K > 0) \le 1$ for all $s \ge e \ge 0, q \ge 0$.
  - Strictly monotonic in duration $(s - e)$ and sampling intensity $q$.
  - Approaches 0 as $(s - e) \to 0$ or $q \to 0$.

### Primitive 2: `lineage_survival_hazard(s, e, lam, mu)`
- **Mathematical Form:**
  $$\log \mathcal{L}_{\text{survival}}(s, e) = - \int_e^s [\lambda(t) + \mu(t)] \, dt + \mathbb{I}(e > 0) \cdot \log \mu(e)$$
- **Sense:** Continuous-time survival log-likelihood of a lineage born at $s$ and dying at $e$ (or surviving to modern day if $e = 0$).
- **Invariants:**
  - Bounded above by 0 (probabilities $\le 1$).
  - Strictly penalizes longer lifespans under non-zero turnover hazards.

### Primitive 3: `diversity_dependent_rates(n_standing, lam0, mu0, gl, gm)`
- **Mathematical Form:**
  $$\lambda(N) = \lambda_0 \cdot \exp(Gl \cdot N) \quad \text{or} \quad \max(0, \lambda_0 + Gl \cdot N)$$
  $$\mu(N) = \mu_0 \cdot \exp(Gm \cdot N) \quad \text{or} \quad \max(0, \mu_0 + Gm \cdot N)$$
- **Sense:** Evaluates instantaneous per-lineage speciation $\lambda$ and extinction $\mu$ as a function of current standing clade richness $N$.
- **Invariants:**
  - Strictly non-negative: $\lambda(N) \ge 0, \mu(N) \ge 0$.
  - When $Gl = 0, Gm = 0$, reduces to constant-rate birth-death process.
  - When $Gl < 0$, monotonically decreases with $N$ (competitive niche saturation).
  - When $Gl > 0$, monotonically increases with $N$ (generative niche construction).

### Primitive 4: `poisson_occurrence_loglik(occ_ages, s, e, q)`
- **Mathematical Form:**
  $$\log \mathcal{L}_{\text{occ}}(\mathbf{t} \mid s, e, q) = \sum_{j=1}^K \log q(t_j) - \int_e^s q(t) \, dt$$
- **Sense:** Poisson process likelihood for the timestamps of $K$ observed fossil occurrences between $s$ and $e$.
- **Invariants:**
  - Rejects with $-\infty$ if any $t_j > s$ or $t_j < e$ (occurrences outside true lifespan are impossible).

### Primitive 5: `standing_diversity_trajectory(lineage_intervals, eval_times)`
- **Mathematical Form:**
  $$N(t) = \sum_{i=1}^M \mathbb{I}(s_i \ge t \ge e_i)$$
- **Sense:** Vectorized counting of lineages active at time $t$.
- **Invariants:**
  - Integer-valued and non-negative ($N(t) \in \mathbb{N}_{\ge 0}$).
