# Data Inventory & Provenance: Darwin Cirripedia Monographs (1851–1854)

**Coordinate:** `data/raw/darwin_cirripedia_1851_1854/DATA_PROVENANCE.md`  
**Authors:** Charles Darwin (1851, 1854); Ingestion by Flow (@feelingflowingbot)  
**Date:** 2026-11-17  
**Repo:** `phosphene/hominin-morphodynamics`  

---

## 1. Primary Sources & Ingestion Ledger

The complete primary texts and catalogs of Charles Darwin's four foundational monographs on the Sub-class Cirripedia (barnacles) have been ingested into `data/raw/darwin_cirripedia_1851_1854/`:

| Canonical File | Volume / Monograph Title | Sponsoring Society & Year | Source Archive Identifier | Size (bytes) | SHA-256 Checksum |
|---|---|---|---|---|---|
| `darwin_1851_living_lepadidae_ray_soc.txt` | *A Monograph on the Sub-class Cirripedia: The Lepadidae; or, Pedunculated Cirripedes* | Ray Society (London, 1851) | `amonographonthes31558gut/31558-8.txt` | 851,243 | `388bdc0abb2f53fc82ccb2b8a40f5ecd976498330407259bc369a4cf73db2665` |
| `darwin_1854_living_balanidae_ray_soc.txt` | *A Monograph on the Sub-class Cirripedia: The Balanidae, Verrucidae, etc.* | Ray Society (London, 1854) | `amonographonthes46408gut/46408-0.txt` | 1,854,389 | `ccf1e6d91e58b2ff2b9bf27d21312a68b359ff65565f006795fd50d03b8165ab` |
| `darwin_1851_fossil_lepadidae_palaeont_soc.txt` | *A Monograph on the Fossil Lepadidae, or, Pedunculated Cirripedes of Great Britain* | Palaeontographical Society (London, 1851) | `darwin-online_1851_FossilLep_F342.1` | 299,647 | `3071d89b29ba9f6e60c40b51bc6ed2ca555ceb314c637cc8e7bb672580e488a0` |
| `darwin_1854_fossil_balanidae_palaeont_soc.txt` | *A Monograph on the Fossil Balanidae and Verrucidae of Great Britain* | Palaeontographical Society (London, 1854) | `darwin-online_1854_FossilBal_F342.2` | 138,127 | `723a853495ef32f96b48c9fbcb19b710596d1b5bb04d80c9e31e330e8871eec8` |

---

## 2. Structured Empirical Tables

- **`darwin_1851_fossil_lepadidae_stratigraphy.csv`**: Complete transcription of Darwin’s master stratigraphic range table from page 14 of the 1851 *Fossil Lepadidae* monograph.
  - Documents 35 distinct fossil species (*Scalpellum*, *Pollicipes*, *Loricula*) across 10 geological stages from the Lower Oolite (Jurassic) to the Tertiary.
  - Documents the Cretaceous peak of pedunculated cirripedes (9–10 species in the Maestricht stage, 9–12 in Upper Chalk) contrasting with their extreme rarity in the Oolite.
