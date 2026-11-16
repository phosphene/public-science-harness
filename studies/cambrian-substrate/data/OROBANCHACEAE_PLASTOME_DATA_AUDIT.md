# Empirical Plastome Evidentiary Profile: Orobanchaceae Genome Reduction & Retention Audits

**Document Coordinate:** `studies/cambrian-substrate/data/OROBANCHACEAE_PLASTOME_DATA_AUDIT.md`  
**Repository:** `phosphene/public-science-harness` (with links to `vi-foundry/data/`)  
**Data Sources:**  
- `vi-foundry/data/species_plastome_data.tsv` (144 accessions, NCBI GenBank download)
- `vi-foundry/data/orobanchaceae_retention_matrix.tsv` (8 taxa × 6 functional categories)
- `vi-foundry/data/cross_family_plastome_data.tsv` (91 species across 15 families)
**Primary Botanical Lineage:** Wicke et al. (2013, 2016), Barrett & Davis (2012), Gruzdev et al. (2019), Krause (2011)  
**Authors:** Ed Phil, Jan, and Flow (`@feelingflowingbot`)  
**Status:** Living Empirical Profile & Austere Botanical Audit  
**Date:** 2026-11-16  

---

## 1. The Austere Botanical Stance

Before any theoretical claim is made regarding "order of degradation" or "two-rate relaxation" in parasitic plants, the empirical files must be subjected to the exact same forensic scrutiny as the Cambrian occurrences:
- What rows exist?
- What are the units and definitions?
- Where are the data pipeline artifacts, truncated accessions, and naming collisions?
- What is directly observed in the GenBank accessions versus what is an analytical interpolation?

---

## 2. Dimension 1: The Macro Plastome Length Dataset (`species_plastome_data.tsv`)

### A. Raw Dimensions & Distribution
The dataset contains **144 records** across 5 discrete parasitism categories:

```
Plastome Length Spectrum Across Parasitism Tiers (N = 144)
┌───────────────────────────┬───────┬──────────────┬──────────────┬──────────────┐
│ Parasitism Category       │ Count │ Min (bp)     │ Mean (bp)    │ Max (bp)     │
├───────────────────────────┼───────┼──────────────┼──────────────┼──────────────┤
│ 0_autotroph               │ 21    │ 153,789      │ 154,980.8    │ 159,469      │
│ 1_hemiparasite            │ 98    │ 71*          │ 140,211.1    │ 191,085      │
│ 2_obligate_hemiparasite   │ 2     │ 143,840      │ 147,172.0    │ 150,504      │
│ 3_holoparasite            │ 20    │ 45,673       │ 81,078.9     │ 102,657      │
│ 4_extreme_holoparasite    │ 3     │ 86,073       │ 95,686.3     │ 114,774      │
└───────────────────────────┴───────┴──────────────┴──────────────┴──────────────┘
```

### B. Forensic Data Artifacts Discovered (The "71 bp" Contamination)
Three rows in `species_plastome_data.tsv` represent **PCR primer/marker fragments**, NOT complete circular plastomes:
1. `Agalinis auriculata` (accession `X64570`): **71 bp** (single gene fragment)
2. `Lamourouxia sp. UCB` (accession `X64571`): **71 bp** (single gene fragment)
3. `Castilleja indivisa` (accession `OK469601`): **515 bp** (partial Sanger sequence)

**Austerity Note:** Any naive linear regression or summary statistic that includes these records without an $L > 10,000\text{ bp}$ filter is calculating noise from incomplete NCBI accessions.

### C. Category Inversion Anomaly
- Category `4_extreme_holoparasite` (*Aeginetia*, 3 species) has a *larger* mean plastome ($95.7\text{ kb}$) than Category `3_holoparasite` (*Orobanche* / *Epifagus*, 20 species, mean $81.1\text{ kb}$, minimum $45.7\text{ kb}$).
- *Botanical Reality:* *Epifagus virginiana* (~$70\text{ kb}$) and *Conopholis americana* (~$45.7\text{ kb}$) have shed far more DNA than *Aeginetia*, yet *Aeginetia* was labeled "category 4". The categorization scheme contains an arbitrary ordinal label that conflicts with physical nucleotide length.

---

## 3. Dimension 2: The 8-Taxa Retention Matrix (`orobanchaceae_retention_matrix.tsv`)

### A. The Empirical Matrix
The table contains 48 rows tracking 8 representative taxa across 6 functional categories:

```
Empirical Gene Retention Grid (0.0 = Absent / Pseudogenized, 1.0 = Fully Retained)
┌───────────────┬───────┬────────┬────────┬────────┬────────┬────────┬──────────┐
│ Taxon         │ Score │ ndh    │ rpo    │ psa    │ psb    │ atp    │ rpl_rps  │
├───────────────┼───────┼────────┼────────┼────────┼────────┼────────┼──────────┤
│ Lindenbergia  │ 0.0   │ 1.00   │ 1.00   │ 1.00   │ 1.00   │ 1.00   │ 1.00     │
│ Pedicularis   │ 1.0   │ 0.00   │ 1.00   │ 1.00   │ 1.00   │ 1.00   │ 1.00     │
│ C.exaltata*   │ 1.5   │ 0.00   │ 1.00   │ 1.00   │ 1.00   │ 1.00   │ 0.78     │
│ C.gronovii*   │ 2.5   │ 0.00   │ 0.00   │ 1.00   │ 1.00   │ 1.00   │ 0.72     │
│ C.campestris* │ 3.0   │ 0.00   │ 0.00   │ 0.80   │ 1.00   │ 1.00   │ 0.50     │
│ Boulardia     │ 3.0   │ 0.00   │ 0.00   │ 0.00   │ 0.00   │ 0.50   │ 0.67     │
│ Epifagus      │ 3.0   │ 0.00   │ 0.00   │ 0.00   │ 0.00   │ 0.50   │ 0.67     │
│ Conopholis    │ 4.0   │ 0.00   │ 0.00   │ 0.00   │ 0.00   │ 0.00   │ 0.48     │
└───────────────┴───────┴────────┴────────┴────────┴────────┴────────┴──────────┘
```

### B. Major Forensic Caveats
1. **Genus Mashup (*Cuscuta* vs Orobanchaceae):**
   - The taxa `C.exaltata`, `C.gronovii`, and `C.campestris` are **dodders (*Cuscuta*)**, which belong to the family **Convolvulaceae** (morning glories), NOT Orobanchaceae!
   - *Cuscuta* represents a completely independent evolutionary origin of plant parasitism. Calling this table `orobanchaceae_retention_matrix.tsv` is a taxonomic mashup. Only *Lindenbergia*, *Pedicularis*, *Boulardia*, *Epifagus*, and *Conopholis* are true Orobanchaceae.
2. **Fractional Retention Units:**
   - Values like `0.78`, `0.72`, `0.50` represent gene counts normalized within a category (e.g., 6 of 12 ribosomal proteins retained), not a continuous trait.
3. **Phylogenetic Tree Mismatch:**
   - The associated tree (`vi-foundry/data/orobanchaceae_tree.nwk`) does not contain *Cuscuta* (because it is an Orobanchaceae tree). Only 3 of the 8 species match tree tips, making full PGLS mathematically invalid on this specific file without taxonomic correction.

---

## 4. What the Data Actually Tells Us (The Honest Empirical Signal)

Despite taxonomic mashups and PCR fragment contamination, the physical signal of the **retention hierarchy** is real when read austerely:

1. **`ndh` (chlororespiration) is uniformly lost first:** Even weak hemiparasites (*Pedicularis*) have $0.00$ retention.
2. **Photosystems (`psa`, `psb`) and RNA polymerase (`rpo`) are lost second:** When a plant becomes fully heterotrophic (holoparasite), light harvesting stops immediately.
3. **ATP synthase (`atp`) is retained longer:** Preserved at $0.50$ in *Boulardia* and *Epifagus* after photosystems are at $0.00$.
4. **Ribosomal proteins (`rpl_rps`) and translation machinery persist to the very bottom:** Even in *Conopholis* (plastome reduced to $45.7\text{ kb}$), $48\%$ of ribosomal machinery remains intact.

---

## 5. Bounding Protocols for Future Analysis

Before proposing any mathematical models for this data:
1. **Taxonomic Disentanglement:** Separate true Orobanchaceae (monophyletic family) from Convolvulaceae (*Cuscuta*). Compare them as convergent independent evolutions rather than a single blended matrix.
2. **Quality Control Filter:** Strip all NCBI accessions with length $< 10,000\text{ bp}$ to purge PCR marker fragments.
3. **Binary Discrete Transitions vs Continuous Curves:** Model gene loss as discrete, Markovian state-transition steps (present $\to$ pseudogene $\to$ absent), not as a smooth continuous differential equation.
