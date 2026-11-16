# Stratigraphically Coupled Lineage Horizon Lifespan Evaluator: Literate Specification & Mathematical Breakdown

**Ticket Coordinate:** `PSH-BD-002`  
**Study Coordinate:** `studies/cambrian-substrate/models/lineage_horizon_evaluator.py`  
**Repository:** `phosphene/public-science-harness`  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Specification & Literate Implementation Guide  
**Date:** 2026-11-16  

---

## 1. The Physical and Epistemic Setting

In classical paleontology, an empirical database is a collection of records stating:
> *"Taxon $T$ was observed in Geological Horizon $H$ at Geographic Location $L$ with Preservation Mode $M$."*

The geological horizon $H$ is a physical stratum of rock (a bed, a member, or a biozone) bounded in time by radiometric or biozonal anchor points:
$$H = [b_{\text{young}, H}, b_{\text{old}, H}]$$

When multiple taxa $T_1, T_2, \dots, T_k$ are excavated from the same horizon $H$, they were entombed in the exact same sedimentary depositional regime. 

---

## 2. The Mathematical Pathology in Legacy PyRate

In legacy PyRate (`PyRate.py`), uncertainty in the age of horizon $H$ was handled by **independent Monte Carlo jittering**:
$$\tau_{i,j} \sim \text{Uniform}(b_{\text{young}, H}, b_{\text{old}, H}) \quad \text{independently for each occurrence } (i,j)$$

### The Three Pathological Consequences:
1. **Destruction of Bed Contemporaneity:** If taxon $A$ and taxon $B$ were found on the exact same bedding slab in Chengjiang ($518.0\text{–}521.0\text{ Ma}$), independent jittering draws $\tau_A = 518.1\text{ Ma}$ and $\tau_B = 520.9\text{ Ma}$. The model is told that taxon $B$ went extinct nearly 3 million years before taxon $A$ appeared, inventing an artificial sequence of turnover where the rocks recorded simultaneous existence.
2. **Artificial Smearing of Catastrophic Boundaries:** A pulsed radiation (like the Fortunian appearance of *Treptichnus*) spanning $<1\text{ Myr}$ is artificially smeared across the entire 10-million-year width of the stage.
3. **Manufacture of False Stage-Boundary Rate Shifts:** Where adjacent geological stages differ in bin width (e.g. 5 Myr vs 15 Myr), independent uniform scattering creates an artificial density gradient, tricking reversible-jump MCMC into inserting a spurious speciation or extinction spike at the boundary.

---

## 3. The Canonical Resolution: Coupled Latent Horizon Projections

To preserve the integrity of the observational substrate without mutating raw files, we decompose the evaluation into two clean steps:

### Step 1: The Coupled Stratigraphic Projection
Every unique geological horizon $h$ is assigned a single latent realization parameter $u_h \in [0, 1]$ drawn per Monte Carlo replicate:
$$\tau_h = b_{\text{young}, h} + u_h \cdot (b_{\text{old}, h} - b_{\text{young}, h}), \qquad u_h \sim \text{Uniform}(0, 1)$$

Every fossil occurrence $j$ belonging to horizon $h$ inherits the exact same realized age:
$$\tau_{i,j} = \tau_{h(i,j)}$$

### Step 2: Lineage Lifespan Envelope Aggregation
For each distinct taxon $i$, its observed chronological bounds under realization $\mathbf{u}$ are the extreme horizons where it was sampled:
$$\text{FAD}_i(\mathbf{u}) = \max_{j \in \text{Occ}(i)} \tau_{i,j} \quad (\text{First Appearance Datum, oldest age})$$
$$\text{LAD}_i(\mathbf{u}) = \min_{j \in \text{Occ}(i)} \tau_{i,j} \quad (\text{Last Appearance Datum, youngest age})$$
$$\text{Duration}_i(\mathbf{u}) = \text{FAD}_i(\mathbf{u}) - \text{LAD}_i(\mathbf{u}) \ge 0$$

### Step 3: Latent Origination ($s_i$) and Extinction ($e_i$) Gating
Under the Signor-Lipps effect (1982) and Keiding survival conditioning (1975):
$$s_i \ge \text{FAD}_i(\mathbf{u}) \ge \text{LAD}_i(\mathbf{u}) \ge e_i \ge 0$$
Any proposed parameter state where $s_i < \text{FAD}_i$ or $e_i > \text{LAD}_i$ receives an exact likelihood penalty of $-\infty$ (falsification invariant).

---

## 4. Taphonomic Preservation Channel Isolation

Rather than collapsing body fossils and trace burrows into a single flattened count, the evaluator maintains two distinct observational channels:
- $K_{\text{body}, i}$: Count of body fossil occurrences (cuticle, carapace, shell, soft-tissue compression).
- $K_{\text{trace}, i}$: Count of ichnological trace occurrences (burrows, trails, trackways).
- $Z_{\max, i}$: Maximum observed vertical tiering depth (mm) associated with the taxon's trace occurrences.

If $K_{\text{body}, i} == 0$ and $K_{\text{trace}, i} > 0$ (e.g. *Treptichnus pedum*), the taxon's observed lifespan $[\text{LAD}_i, \text{FAD}_i]$ is fully defined by its trace record, and its tiering depth $Z_{\max}$ is passed to the downstream likelihood to prevent the zero-diversity taphonomic trap.
