#!/usr/bin/env python3
"""
Pipeline 01: Build Stratigraphic Horizon & Ichnofacies Matrix (Paper 01, Section 2)
Conforms to docs/DATA_STANDARDS.md.
"""

import csv
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

STUDY_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = STUDY_DIR / "data" / "raw"
CURATED_DIR = STUDY_DIR / "data" / "curated"
SQL_DIR = STUDY_DIR / "sql" / "ddl"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)

# Curated stratigraphic horizon raw entries based on GSSP and canonical literature
# (Brasier 1994, Narbonne 1987, Kouchinsky 2012, Buatois & Mángano 2011, Ivantsov 2013)
HORIZON_RECORDS = [
    {
        "horizon_id": "HZ_FORTUNE_HEAD_ED_01",
        "section_name": "Fortune Head GSSP",
        "country": "Canada (Newfoundland)",
        "stage_name": "Terminal Ediacaran",
        "age_top_ma": 541.0,
        "age_bottom_ma": 555.0,
        "ichnotaxon": "Radulichnus cf. kimberelloides",
        "substrate_penetration_dimension": "2D_SURFACE_MAT",
        "max_burrow_depth_mm": 1.5,
        "biomineralized_tissue_present": 0,
        "mineralogy_type": "NONE",
        "primary_reference_doi": "10.1017/S001675680001099X"
    },
    {
        "horizon_id": "HZ_WHITE_SEA_ED_02",
        "section_name": "White Sea / Zimnii Bereg",
        "country": "Russia",
        "stage_name": "Terminal Ediacaran",
        "age_top_ma": 550.0,
        "age_bottom_ma": 558.0,
        "ichnotaxon": "Kimberichnus teruzzii",
        "substrate_penetration_dimension": "2D_SURFACE_MAT",
        "max_burrow_depth_mm": 2.0,
        "biomineralized_tissue_present": 0,
        "mineralogy_type": "NONE",
        "primary_reference_doi": "10.1130/G34221.1"
    },
    {
        "horizon_id": "HZ_FORTUNE_HEAD_CB_01",
        "section_name": "Fortune Head GSSP",
        "country": "Canada (Newfoundland)",
        "stage_name": "Fortunian",
        "age_top_ma": 529.0,
        "age_bottom_ma": 541.0,
        "ichnotaxon": "Treptichnus pedum",
        "substrate_penetration_dimension": "3D_VERTICAL_INFAUNAL",
        "max_burrow_depth_mm": 35.0,
        "biomineralized_tissue_present": 0,
        "mineralogy_type": "NONE",
        "primary_reference_doi": "10.1017/S001675689400001X"
    },
    {
        "horizon_id": "HZ_MEISHUCUN_CB_02",
        "section_name": "Meishucun Section (Xiaowaitoushan Mbr)",
        "country": "China (Yunnan)",
        "stage_name": "Fortunian",
        "age_top_ma": 535.0,
        "age_bottom_ma": 539.0,
        "ichnotaxon": "Saronichnus / Arenicolites",
        "substrate_penetration_dimension": "3D_VERTICAL_INFAUNAL",
        "max_burrow_depth_mm": 45.0,
        "biomineralized_tissue_present": 1,
        "mineralogy_type": "PHOSPHATIC",
        "primary_reference_doi": "10.1016/j.precamres.2012.01.004"
    },
    {
        "horizon_id": "HZ_MAOTIANSHAN_CB_03",
        "section_name": "Chengjiang (Yu'anshan Mbr)",
        "country": "China (Yunnan)",
        "stage_name": "Stage 3",
        "age_top_ma": 518.0,
        "age_bottom_ma": 521.0,
        "ichnotaxon": "Rusophycus / Cruziana / predatory trackways",
        "substrate_penetration_dimension": "3D_NEKTONIC",
        "max_burrow_depth_mm": 80.0,
        "biomineralized_tissue_present": 1,
        "mineralogy_type": "CARBONATE",
        "primary_reference_doi": "10.1126/science.1070052"
    },
    {
        "horizon_id": "HZ_BURGESS_SHALE_CB_04",
        "section_name": "Burgess Shale (Stephen Fm)",
        "country": "Canada (British Columbia)",
        "stage_name": "Wuliuan (Stage 5)",
        "age_top_ma": 505.0,
        "age_bottom_ma": 508.0,
        "ichnotaxon": "Nektonic predatory traces / Anomalocaris predation bites",
        "substrate_penetration_dimension": "3D_NEKTONIC",
        "max_burrow_depth_mm": 120.0,
        "biomineralized_tissue_present": 1,
        "mineralogy_type": "CARBONATE",
        "primary_reference_doi": "10.1126/science.1169514"
    }
]

def run_pipeline():
    print("=== [Pipeline 01] Ingesting Stratigraphic Horizon & Ichnofacies Matrix ===")
    
    # 1. Write raw snapshot (immutable)
    raw_csv_path = RAW_DIR / "stratigraphic_horizons_raw.csv"
    fieldnames = list(HORIZON_RECORDS[0].keys())
    with open(raw_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(HORIZON_RECORDS)
    
    # Compute SHA256
    sha256 = hashlib.sha256(raw_csv_path.read_bytes()).hexdigest()
    manifest_path = RAW_DIR / "MANIFEST.json"
    manifest_data = {}
    if manifest_path.exists():
        try:
            manifest_data = json.loads(manifest_path.read_text())
        except Exception:
            pass
    manifest_data["stratigraphic_horizons_raw.csv"] = {
        "sha256": sha256,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "GSSP Fortune Head, White Sea, Meishucun canonical compilations (Brasier 1994, Kouchinsky 2012)",
        "row_count": len(HORIZON_RECORDS)
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))
    print(f"  [Raw] Saved {raw_csv_path.name} (SHA-256: {sha256[:16]}...)")

    # 2. Build Curated SQLite Relational Database
    db_path = CURATED_DIR / "cambrian_substrate.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Run DDL
    ddl_file = SQL_DIR / "01_stratigraphic_horizons.sql"
    if ddl_file.exists():
        cur.executescript(ddl_file.read_text())
    
    # Insert rows
    cur.execute("DELETE FROM stratigraphic_horizons;")
    for r in HORIZON_RECORDS:
        cur.execute("""
            INSERT INTO stratigraphic_horizons (
                horizon_id, section_name, country, stage_name, age_top_ma, age_bottom_ma,
                ichnotaxon, substrate_penetration_dimension, max_burrow_depth_mm,
                biomineralized_tissue_present, mineralogy_type, primary_reference_doi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["horizon_id"], r["section_name"], r["country"], r["stage_name"],
            r["age_top_ma"], r["age_bottom_ma"], r["ichnotaxon"],
            r["substrate_penetration_dimension"], r["max_burrow_depth_mm"],
            bool(r["biomineralized_tissue_present"]), r["mineralogy_type"],
            r["primary_reference_doi"]
        ))
    conn.commit()
    
    # Verify count
    cur.execute("SELECT COUNT(*) FROM stratigraphic_horizons;")
    count = cur.fetchone()[0]
    conn.close()
    
    print(f"  [Curated] Loaded {count} rows into {db_path.name} table 'stratigraphic_horizons'")
    print("=== [Pipeline 01] Complete ===")

if __name__ == "__main__":
    run_pipeline()
