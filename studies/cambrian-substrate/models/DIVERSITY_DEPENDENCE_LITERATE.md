# Taphonomically Compensated Diversity-Dependence Estimator: Mathematical Rehearsal & Literate Specification (PSH-BD-004)

**Document Coordinate:** `studies/cambrian-substrate/models/DIVERSITY_DEPENDENCE_LITERATE.md`  
**Repository:** `phosphene/public-science-harness`  
**Mathematical Canon:** MacArthur & Wilson (1967), Walker & Valentine (1984), Sepkoski (1978, 1984), Rabosky & Lovette (2008), Etienne et al. (2012), Seilacher (1999), Mángano & Buatois (2014), Van Holstein & Foley (2024)  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Mathematical Specification & Architectural Contract  
**Date:** 2026-11-16  

---

## 1. The Precursor Lineage & Mathematical Canon

The concept that the rate of lineage origination ($\lambda$) or extinction ($\mu$) is governed by the number of co-occurring active lineages ($N_t$) has a rich fifty-year mathematical lineage:

### A. Island Biogeography & Equilibrium Speciation (MacArthur & Wilson 1967, Sepkoski 1978)
Robert MacArthur and Edward Wilson established that colonization and speciation slow down as an island fills with species. 
Jack Sepkoski (1978, 1984) translated this into the canonical logistic differential equation for marine metazoan diversification:
$$\frac{dN}{dt} = r N \left(1 - \frac{N}{K}\right)$$
Where $r = (\lambda_0 - \mu_0)$ is the intrinsic net diversification rate and $K$ is the carrying capacity of the marine shelf.

### B. Continuous-Time Multi-Rate Diversity-Dependence (Rabosky 2008, Etienne et al. 2012)
Modern macroevolutionary likelihood modeling formalized Sepkoski's logistic into linear feedback hazards:
$$\lambda(N_t) = \max\left(0, \lambda_0 + Gl \cdot N_t\right), \qquad \mu(N_t) = \max\left(0, \mu_0 + Gm \cdot N_t\right)$$
Where:
- $Gl < 0$: Speciation slowdown (niche-filling / competition).
- $Gl > 0$: Diversity-facilitated speciation (niche construction / evolutionary positive feedback).
- $Gm > 0$: Density-dependent extinction (overcrowding / resource depletion).

Van Holstein & Foley (2024) applied this continuous framework to hominin fossil records, finding $Gl > 0$ in tool-making *Homo* ($Gl = +2.119$).

---

## 2. The Taphonomic Pathology: The Infaunal Body Fallacy

When applying diversity-dependence ($Gl$) to the Cambrian explosion, normal science commits a disastrous error if it uses unweighted body counts:

1. **The Empirical Fact:** In the Fortunian stage (~538.8–529 Ma), the raw body fossil count for infaunal burrowers is **strictly zero ($N_{\text{body}} = 0$)**, and across the entire 1,000-occurrence dataset, infauna have only 5 occurrences across 4 taxa.
2. **The Naive Model Failure:** If an unweighted diversity-dependence model is fitted to infaunal body fossils, it measures $N_t = 0 \to N_t = 2 \to N_t = 4$. It concludes that infaunal animals diversified negligibly or suffered severe negative rates, mistaking **non-biomineralization** for biological absence.
3. **The Physical Reality:** The sediment itself records massive, three-dimensional infaunal engineering (*Treptichnus pedum* penetrating $35\text{–}45\text{ mm}$), transforming thousands of square kilometers of benthic seafloor into an oxidized, aerated volume.

---

## 3. The Canonical Resolution: Stratigraphic Tiering Compensation

Following Seilacher (1999), Droser & Bottjer (1986), and Mángano & Buatois (2014), the true ecological capacity of substrate-active organisms scales with the **bioturbated sediment volume**, parameterized by the maximum burrow tiering depth $Z_{\max}$:

$$N_{\text{eff}}(t) = N_{\text{body}}(t) + \beta_{\text{ichno}} \cdot \left( \frac{Z_{\max}(t)}{Z_{\text{ref}}} \right)^\gamma$$

Where:
- $Z_{\max}(t)$: Maximum observed penetrative burrow depth (mm) in horizon $t$ (e.g., $45.0\text{ mm}$ at Meishucun, $120.0\text{ mm}$ at Burgess Shale).
- $Z_{\text{ref}}$: Baseline Ediacaran surface tiering depth ($2.0\text{ mm}$).
- $\beta_{\text{ichno}}$: Calibration scale factor anchoring trace presence to effective population units.
- $\gamma$: Geometric dimension scaling ($\gamma = 1.0$ for linear tiering, $\gamma = 1.5$ for fractal burrow networks).

### Architectural Invariant:
The estimator queries `v_calibrated_guild_diversity` from `cambrian_substrate.db`. If a guild has status `BIASED_HIGH_ICHNO_COMPENSATION_REQUIRED`, unweighted fitting is **strictly forbidden**. Execution is halted with an `EpistemicWarrantViolation` unless tiering compensation is explicitly engaged.
