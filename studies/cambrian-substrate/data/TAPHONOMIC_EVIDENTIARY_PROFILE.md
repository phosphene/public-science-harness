# Empirical Taphonomic Profile: The Shape, Sparseness, and Silences of the Cambrian Substrate

**Document Coordinate:** `studies/cambrian-substrate/data/TAPHONOMIC_EVIDENTIARY_PROFILE.md`  
**Repository:** `phosphene/public-science-harness`  
**Database:** `studies/cambrian-substrate/data/curated/cambrian_substrate.db`  
**Dataset Scale:** $N = 1,000$ occurrences, $431$ distinct taxa, $87$ collections, $6$ reference GSSP/Lagerstätte horizons  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Empirical Profile & Austere Taphonomic Audit  
**Date:** 2026-11-16  

---

## 1. The Austere Empirical Stance

Before any birth-death rates ($\lambda, \mu$), diversification slopes ($Gl, Gm$), or physical carrying capacities ($K$) are fitted, we must document **what the rock record actually preserves and what it leaves in total silence**.

In the Paleobiology Database (PBDB) slice for the Cambrian substrate transition, we do not have a uniform video stream of evolutionary history. We have an intensely filtered, highly clustered, and taphonomically skewed collection of physical rock samples.

This profile characterizes the data across four physical dimensions:
1. **The Frequency Spectrum (Singleton Skew):** The severe sparseness of occurrences per lineage.
2. **The Spatial-Stratigraphic Clustering (The Bed Reality):** The condensation of occurrences into discrete depositional horizons.
3. **The Taphonomic Guild Disparity:** The dramatic over-representation of biomineralized/cuticular predators versus the near-total absence of soft-bodied infaunal bodies.
4. **The Temporal Resolution Hierarchy:** The variation between narrow biozonal beds ($<2\text{ Myr}$) and coarse stage umbrellas ($>30\text{ Myr}$).

---

## 2. Dimension 1: The Frequency Spectrum & Extreme Singleton Skew

In classical statistical ecology and survival analysis, inference quality depends on sampling redundancy. The empirical Cambrian distribution exhibits an extreme right-tailed decay:

```
Occurrences per Taxon Distribution (N = 431 Distinct Taxa)
┌──────────────────┬──────────────┬──────────────────┬────────────────────────────────────────────┐
│ Occurrences (k)  │ Taxon Count  │ Pct of Clade (%) │ Cumulative Spectrum                        │
├──────────────────┼──────────────┼──────────────────┼────────────────────────────────────────────┤
│ k = 1 (Singletons│ 249          │ 57.77%           │ ████████████████████████████ 57.8%         │
│ k = 2 (Doubletons│ 75           │ 17.40%           │ ████████ 75.2%                             │
│ k = 3            │ 29           │ 6.73%            │ ███ 81.9%                                  │
│ k = 4            │ 35           │ 8.12%            │ ████ 90.0%                                 │
│ k = 5            │ 8            │ 1.86%            │ █ 91.9%                                    │
│ k = 6            │ 8            │ 1.86%            │ █ 93.7%                                    │
│ k = 7 to 9       │ 15           │ 3.48%            │ █ 97.2%                                    │
│ k >= 10          │ 12           │ 2.78%            │ █ 100.0%                                   │
└──────────────────┴──────────────┴──────────────────┴────────────────────────────────────────────┘
```

### Empirical Reality:
- **57.77% of all taxa appear exactly once in the entire record.**
- **75.17% appear twice or fewer.**
- Only **12 taxa (2.78%)** have 10 or more occurrences (long-ranging cosmopolitan forms like *Hyolithes*, *Lingulella*, *Micromitra*, *Kootenia*, *Pseudagnostus*).
- **Austerity Note:** Any statistical model attempting to estimate independent per-taxon origination ($s_i$) and extinction ($e_i$) on this dataset will fail unless heavily regularized by the shared sampling process ($q$) and horizon-level grouping.

---

## 3. Dimension 2: Spatial-Stratigraphic Clustering (The Bed Reality)

The 1,000 occurrences do not arrive as a continuous Poisson stream. They are physically clustered into **87 distinct collection horizons**:

- **Mean occurrences per collection:** $11.49$
- **Top 5 collections represent 14.3% of the entire dataset:**
  - `col:215`: 34 occurrences (34 distinct taxa) — Dyeran Stage, Laurentia
  - `col:207`: 33 occurrences (31 distinct taxa) — Delamaran Stage, Laurentia
  - `col:198`: 33 occurrences (31 distinct taxa) — Delamaran Stage, Laurentia
  - `col:216`: 28 occurrences (28 distinct taxa) — Dyeran Stage, Laurentia
  - `col:192`: 24 occurrences (24 distinct taxa) — Dyeran Stage, Laurentia
- **Austerity Note:** In these rich Lagerstätte quarries, dozens of species were buried in the exact same sedimentary event. Independent uniform age resampling (PyRate Anti-Pattern 2) breaks this physical contemporaneity. The data demands that all taxa in `col:215` share a single coupled horizon draw.

---

## 4. Dimension 3: The Taphonomic Guild Chiasm

When the occurrences are grouped by functional ecological guilds, the taphonomic filter creates an immense structural chiasm:

```
Functional Guild Breakdown in Body-Fossil Occurrences
┌──────────────────────────┬──────────────┬──────────────┬──────────────────┬────────────────────┐
│ Functional Guild         │ Occurrences  │ Distinct Taxa│ Mean Occs/Taxon  │ Dominant Tissue    │
├──────────────────────────┼──────────────┼──────────────┼──────────────────┼────────────────────┤
│ MOBILE_APEX_PREDATOR     │ 634 (63.4%)  │ 295 (68.4%)  │ 2.15             │ Sclerotized Cuticle│
│ SEDENTARY_FILTER_FEEDER  │ 246 (24.6%)  │ 81 (18.8%)   │ 3.04             │ Calcareous/Phosph. │
│ OTHER_UNCLASSIFIED       │ 115 (11.5%)  │ 51 (11.8%)   │ 2.25             │ Variable           │
│ INFAUNAL_BURROWER        │ 5 (0.5%)     │ 4 (0.9%)     │ 1.25             │ Soft Vermiform     │
└──────────────────────────┴──────────────┴──────────────┴──────────────────┴────────────────────┘
```

### The 5 Infaunal Body Occurrences:
1. `PBDB_OCC_occ:1340`: *Selkirkia* (Priapulida, Dyeran, `col:192`) — organic tube preservation.
2. `PBDB_OCC_occ:1584`: *Selkirkia* (Priapulida, Delamaran, `col:207`) — organic tube preservation.
3. `PBDB_OCC_occ:2186`: *Dendrograptus* (Hemichordata, Trempealeauan, `col:256`).
4. `PBDB_OCC_occ:2216`: *Acanthograptus* (Hemichordata, Sunwaptan, `col:258`).
5. `PBDB_OCC_occ:2217`: *Dendrograptus hallianus* (Hemichordata, Sunwaptan, `col:258`).

### The Taphonomic Silence:
- In the Fortunian Stage (~$538.8\text{–}529\text{ Ma}$), the body occurrence count for infaunal burrowers is **strictly zero ($N = 0$)**.
- Yet, the ichnological record across Fortune Head, Meishucun, and the Chapel Island Formation preserves thousands of meters of three-dimensional *Treptichnus pedum* branching burrows penetrating $30\text{–}45\text{ mm}$ into the sediment.
- **Austerity Note:** Under pure body-fossil inference, infaunal animals do not exist at the Cambrian boundary. This is an artifact of non-biomineralization. Trace fossils provide the physical presence proof; body fossils record only the later acquisition of resistant tubes or skeletal cuticles.

---

## 5. Dimension 4: The Temporal Resolution Hierarchy

The 1,000 occurrences span 17 named stratigraphic bins whose age spans differ by a factor of 15:

- **Narrow Biozones ($2\text{–}4\text{ Myr}$):** 
  - *Paibian:* 2.8 Myr ($494.2\text{–}497.0\text{ Ma}$)
  - *Ordian:* 3.2 Myr ($508.0\text{–}511.2\text{ Ma}$)
  - *Trempealeauan:* 3.35 Myr ($486.85\text{–}490.2\text{ Ma}$)
- **Intermediate Stages ($5\text{–}10\text{ Myr}$):**
  - *Dyeran:* 5.6 Myr ($509.7\text{–}515.3\text{ Ma}$, 141 occs)
  - *Delamaran:* 4.4 Myr ($505.3\text{–}509.7\text{ Ma}$, 104 occs)
  - *Marjumian:* 7.5 Myr ($497.0\text{–}504.5\text{ Ma}$, 101 occs)
  - *Dresbachian / Franconian / Merioneth:* 10.15 Myr ($486.85\text{–}497.0\text{ Ma}$, ~140 occs each)
- **Coarse Regional Umbrellas ($30\text{–}50\text{ Myr}$):**
  - *Caerfai:* 32.3 Myr ($506.5\text{–}538.8\text{ Ma}$, 22 occs)
  - *Cambrian (Unpartitioned):* 51.95 Myr ($486.85\text{–}538.8\text{ Ma}$, 13 occs)

### Austerity Note:
Fossils tied to coarse regional umbrellas cannot be uniformly mixed with high-resolution biozonal tie points without smearing the chronostratigraphic signal. The hierarchical horizon sampler must preserve the distinct uncertainty boundaries of each collection.
