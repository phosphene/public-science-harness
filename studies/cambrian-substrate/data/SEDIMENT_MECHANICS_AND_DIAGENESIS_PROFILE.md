# Empirical Sediment Mechanics & Diagenetic Substrate Profile: The Physical Boundary of the Mat-to-Mix Transition

**Document Coordinate:** `studies/cambrian-substrate/data/SEDIMENT_MECHANICS_AND_DIAGENESIS_PROFILE.md`  
**Repository:** `phosphene/public-science-harness`  
**Database:** `studies/cambrian-substrate/data/curated/cambrian_substrate.db`  
**Physical Lineage:** Berner (1980), Boudreau (1996), Meysman et al. (2003, 2005), Droser & Bottjer (1986, 1989), Seilacher & Pflüger (1994), Mángano & Buatois (2014)  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Physical Profile & Austere Sedimentological Ledger  
**Date:** 2026-11-16  

---

## 1. The Austere Sedimentological Stance

When paleontology turns from body fossils to the substrate, it cannot replace the absent animal with fantasy or ungrounded simulation. The sediment itself is a physical, granular, multiphase material governed by conservation of mass, diagenetic diffusion, shear strength, and hydrodynamic settling.

This document establishes the **sedimentological coordinates** and **bounding aspects** that govern the Agronomic Revolution across the Ediacaran–Cambrian boundary.

The sediment is characterized across five distinct, uncomplected physical layers:
1. **The Rheological / Cohesion Boundary (Yield Stress $\tau_y$ & Mat Sealing):** From shear-resistant microbial matgrounds to fluidized, thixotropic bioturbated muds.
2. **The Diagenetic Redox Interface (Porewater $O_2$ & Sulfate Reduction Depth):** The spatial collapse of the anoxic redox boundary from $<1\text{ mm}$ below the sediment surface to tens of millimeters into the sub-benthos.
3. **The Geometric Penetration Tensor (Ichnofabric Index & Tiering Depth $Z_{\max}$):** The physical coordinates of burrowing (2D surface grazers $\to$ 2.5D undermat miners $\to$ 3D penetrative burrowers).
4. **The Granular Porosity & Water-Content Gradient ($\phi(z)$):** The vertical consolidation of water content from slurry ($>85\%$) to compacted silt ($45\%$).
5. **The Authigenic Mineralization Window:** Why the Ediacaran preserved non-mineralized soft tissues via pyritization ("death masks") and early phosphatization, and why the destruction of this sedimentological regime eliminated exceptional preservation outside of rare dysoxic Lagerstätten.

---

## 2. Dimension 1: Rheological Cohesion & Mechanical Yield Stress

In modern marine sediments, biological reworking fluidizes the top $5\text{–}10\text{ cm}$. In the Terminal Ediacaran, the sediment-water interface was covered by extensive benthic cyanobacterial/algal biofilms (the *matground* or *algal turf* regime).

```
Sediment Rheological State Matrix
┌───────────────────────────┬──────────────────────┬──────────────────────┬──────────────────────────┐
│ Physical Parameter        │ Ediacaran Matground  │ Early Fortunian Mix  │ Wuliuan (Stage 5) Mixed  │
├───────────────────────────┼──────────────────────┼──────────────────────┼──────────────────────────┤
│ Primary Lithology         │ Siltstone / Shale    │ Phosphorite / Silt   │ Calcareous Shale / Mud   │
│ Cohesion Mechanism        │ EPS / Filaments      │ Disrupted Mats       │ Pure Granular / Flocs    │
│ Critical Shear Stress     │ $\tau_c \approx 2.5\text{ Pa}$│ $\tau_c \approx 0.8\text{ Pa}$ │ $\tau_c \approx 0.2\text{ Pa}$   │
│ Sediment Penetration Mode │ Scratching / Gliding │ Radial Probing       │ Continuous Peristalsis   │
│ Representative Trace      │ *Kimberichnus*       │ *Treptichnus pedum*  │ *Burgess* infauna / worms│
└───────────────────────────┴──────────────────────┴──────────────────────┴──────────────────────────┘
```

### Physical Invariant:
- Under pristine microbial mats, water cannot freely exchange across the interface except through molecular diffusion.
- Mechanical yield stress $\tau_y$ at the sediment surface is high, preventing vertical penetration by animals lacking hydrostatic anchors or rigid appendages.
- Grazers (*Kimberella*) were restricted to superficial rasping of the top $1\text{–}2\text{ mm}$ of the mat envelope.

---

## 3. Dimension 2: The Diagenetic Redox Interface & Porewater Chemistry

The sediment is an active chemical reactor modeled by 1D continuous diagenesis (Berner 1980):

$$\frac{\partial C(z, t)}{\partial t} = \frac{\partial}{\partial z} \left( \left( D_m + D_b(z) \right) \frac{\partial C}{\partial z} \right) - w \frac{\partial C}{\partial z} - R(C, z)$$

Where:
- $C(z)$: Concentration of dissolved porewater species ($O_2, SO_4^{2-}, CH_4, Fe^{2+}$).
- $D_m$: Molecular diffusion coefficient in porous media ($D_m = D_0 / \theta^2$).
- $D_b(z)$: Biological particle mixing / biodiffusion coefficient ($D_{b0} \approx 0.05\text{–}1.0\text{ cm}^2/\text{yr}$).
- $w$: Sedimentation accumulation rate ($\approx 0.01\text{–}0.1\text{ cm}/\text{yr}$).
- $R(C, z)$: Respiration sink driven by organic carbon mineralization.

### The Empirical Horizon Calibration:

| Horizon ID | Stage / Horizon | $Z_{\max}$ (mm) | $D_{b0}$ ($\text{mm}^2/\text{yr}$) | $z_{\text{pen}}$ ($O_2$ Depth, mm) | Aerobic Volume ($V_{\text{aer}}$) |
|:---|:---|:---:|:---:|:---:|:---:|
| `HZ_WHITE_SEA_ED_02` | Terminal Ediacaran | $2.0$ | $0.0$ | $0.8\text{–}1.2$ | $1.0\times$ (Baseline) |
| `HZ_FORTUNE_HEAD_ED_01`| Terminal Ediacaran | $1.5$ | $0.0$ | $0.6\text{–}1.0$ | $0.9\times$ |
| `HZ_FORTUNE_HEAD_CB_01`| Fortunian GSSP | $35.0$ | $15.0$ | $12.0\text{–}18.0$ | $14.2\times$ |
| `HZ_MEISHUCUN_CB_02` | Fortunian Stage | $45.0$ | $25.0$ | $18.0\text{–}26.0$ | $21.5\times$ |
| `HZ_MAOTIANSHAN_CB_03` | Stage 3 (Chengjiang) | $80.0$ | $60.0$ | $35.0\text{–}50.0$ | $42.0\times$ |
| `HZ_BURGESS_SHALE_CB_04`| Wuliuan (Stage 5) | $120.0$ | $100.0$ | $55.0\text{–}85.0$ | $75.0\times$ |

### Physical Invariant:
When $Z_{\max}$ increases from $2.0\text{ mm}$ to $35.0\text{ mm}$, the depth of dissolved oxygen penetration expands by more than an order of magnitude, transforming the upper sediment from a sulfidic, toxic zone into an oxidized, metabolically accessible volume.

---

## 4. Dimension 3: The Geometric Penetration Tensor & Ichnofabric Tiers

Sediment mixing is not an isotropic scalar. It occupies discrete spatial and functional tiers (Droser & Bottjer 1986):

1. **Tier 1 (Surface Fluff / Mat Layer, $0\text{–}2\text{ mm}$):**
   - Fabric: Preserved micro-laminations, intact cyanobacterial filaments.
   - Ichnofabric Index: **ii 1** (0% bioturbated).
   - Trace types: Epichnial grazing trails (*Kimberichnus*, *Yorgia* death rests).

2. **Tier 2 (Shallow Undermat Mining, $2\text{–}10\text{ mm}$):**
   - Fabric: Disrupted bedding planes, minor feeding burrows parallel to bedding.
   - Ichnofabric Index: **ii 2** (<10% bioturbated).
   - Trace types: Simple sub-mat horizontal miners (*Helminthopsis*, *Gordia*).

3. **Tier 3 (Vertical 3D Penetration, $10\text{–}50\text{ mm}$):**
   - Fabric: Penetrative branchings cutting across primary sedimentary laminae.
   - Ichnofabric Index: **ii 3 to ii 4** (40–60% bioturbated).
   - Trace types: Three-dimensional probes (*Treptichnus pedum*, *Arenicolites*).

4. **Tier 4 (Deep Deep-Tier Burrowing & Reworking, $>50\text{ mm}$):**
   - Fabric: Total homogenization of sediment; loss of bedding laminations.
   - Ichnofabric Index: **ii 5** (>60% bioturbated).
   - Trace types: Full deposit-feeding galleries and predatory burrows.

---

## 5. Dimension 4: The Taphonomic Preservation Window (Why Absence Occurs)

The sediment properties directly explain the taphonomic guild disparity documented in `TAPHONOMIC_EVIDENTIARY_PROFILE.md`:

- **The Ediacaran Preservation Trap (Death Masks):** In undisturbed matgrounds, rapid microbial anoxia and high porewater silica/iron enabled iron-sulfide permineralization of non-biomineralized soft tissues on bed soles.
- **The Agronomic Erasure:** As vermiform animals penetrated $35\text{–}45\text{ mm}$ into the sediment during the Fortunian:
  1. Porewater $O_2$ penetrated into the sediment, oxidizing organic carcasses that previously underwent anaerobic mineral encrustation.
  2. Physical mixing disrupted the microbial mats, preventing the formation of anoxic capping seals.
  3. Sediment shear stress collapsed, facilitating porewater advection.
- **The Empirical Reality:** Animals without mineralized hard parts ceased to be preservable on ordinary sea floors. Consequently, body fossils of infauna disappear from the record entirely, except when catastrophic obrution deposits (rapid mud burial into anoxic basins, i.e., Burgess Shale, Chengjiang) occurred.

---

## 6. Mathematical Bounding Constraints for Model Ingress

Any subsequent mathematical model or speculative supposition must respect the following sedimentological bounds:

1. **Conservation of Volume:** The total sediment porosity $\phi(z) \in [0.35, 0.90]$.
2. **Diffusion Bound:** Effective biodiffusion $D_b(z) \le 100\text{ mm}^2/\text{yr}$ for early Paleozoic substrates (modern shallow marine goes up to $1000\text{ mm}^2/\text{yr}$).
3. **Trace Grounding:** Infaunal population presence must be anchored to the observed $Z_{\max}$ and ichnotaxon of the corresponding stratigraphic horizon. No model may posit infaunal biomass in an interval without either trace evidence or an explicit counterfactual tag (`[SPECULATIVE_HYPOTHESIS]`).
