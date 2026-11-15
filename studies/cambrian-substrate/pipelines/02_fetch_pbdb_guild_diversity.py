#!/usr/bin/env python3
"""
Pipeline 02: Pull and Curate Cambrian Functional Guild Diversity from PBDB API (Paper 01, Section 3, Table 1)
Conforms to docs/DATA_STANDARDS.md.
"""

import csv
import hashlib
import json
import sqlite3
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STUDY_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = STUDY_DIR / "data" / "raw"
CURATED_DIR = STUDY_DIR / "data" / "curated"
SQL_DIR = STUDY_DIR / "sql" / "ddl"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)

# Functional guild taxonomical classification mapping for early Cambrian
# Sedentary Filter Feeders: Porifera, Brachiopoda, Echinodermata (Eocrinoidea)
# Infaunal Burrowers: Priapulida, Annelida, Hemichordata
# Mobile Apex Predators: Radiodonta, stem Euarthropoda (Anomalocarididae, Hurdiidae)
GUILD_MAP = {
    "Porifera": "SEDENTARY_FILTER_FEEDER",
    "Brachiopoda": "SEDENTARY_FILTER_FEEDER",
    "Echinodermata": "SEDENTARY_FILTER_FEEDER",
    "Priapulida": "INFAUNAL_BURROWER",
    "Annelida": "INFAUNAL_BURROWER",
    "Radiodonta": "MOBILE_APEX_PREDATOR",
    "Arthropoda": "MOBILE_APEX_PREDATOR"  # refined below by genus / class
}

def fetch_pbdb_occurrences():
    print("=== [Pipeline 02] Fetching Cambrian Occurrences from Paleobiology Database (PBDB) ===")
    
    # Query PBDB API for Cambrian marine metazoans with taxonomic classification
    base_url = "https://paleobiodb.org/data1.2/occs/list.json"
    params = {
        "base_name": "Metazoa",
        "interval": "Cambrian",
        "show": "class,phy,coords,loc",
        "limit": "1000"  # Bounded initial fetch for baseline standup
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    print(f"  [HTTP GET] {url}")
    
    req = urllib.request.Request(url, headers={"User-Agent": "PhosphenePublicScienceHarness/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw_json_bytes = r.read()
    
    data = json.loads(raw_json_bytes.decode("utf-8"))
    records = data.get("records", [])
    print(f"  [PBDB Response] Retrieved {len(records)} raw occurrence records.")
    
    # 1. Store Raw JSON Snapshot with cryptographic hash
    raw_file = RAW_DIR / "pbdb_cambrian_metazoa_raw.json"
    raw_file.write_bytes(raw_json_bytes)
    sha256 = hashlib.sha256(raw_json_bytes).hexdigest()
    
    manifest_path = RAW_DIR / "MANIFEST.json"
    manifest_data = {}
    if manifest_path.exists():
        try:
            manifest_data = json.loads(manifest_path.read_text())
        except Exception:
            pass
    manifest_data["pbdb_cambrian_metazoa_raw.json"] = {
        "sha256": sha256,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": url,
        "record_count": len(records)
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))
    print(f"  [Raw] Saved {raw_file.name} (SHA-256: {sha256[:16]}...)")
    
    # 2. Curate and Classify into Functional Guilds
    db_path = CURATED_DIR / "cambrian_substrate.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    ddl_file = SQL_DIR / "02_cambrian_occurrences.sql"
    if ddl_file.exists():
        cur.executescript(ddl_file.read_text())
    
    cur.execute("DELETE FROM cambrian_occurrences;")
    
    curated_rows = []
    for rec in records:
        occ_id = f"PBDB_OCC_{rec.get('oid')}"
        taxon_name = rec.get("tna", "Unknown")
        taxon_rank = str(rec.get("rnk", "unknown"))
        phylum = rec.get("phl")
        class_name = rec.get("cll")
        order_name = rec.get("odl")
        family = rec.get("fml")
        genus = rec.get("gnl")
        early_interval = rec.get("oei", "Cambrian")
        late_interval = rec.get("oli")
        eag = float(rec.get("eag", 541.0))
        lag = float(rec.get("lag", 485.4))
        coll_no = str(rec.get("cid", "0"))
        ref_no = str(rec.get("rid", "0"))
        
        # Guild assignment heuristic
        guild = "OTHER_UNCLASSIFIED"
        if phylum in ("Porifera", "Brachiopoda", "Echinodermata"):
            guild = "SEDENTARY_FILTER_FEEDER"
        elif phylum in ("Priapulida", "Annelida", "Hemichordata"):
            guild = "INFAUNAL_BURROWER"
        elif class_name in ("Dinocaridida", "Radiodonta") or genus in ("Anomalocaris", "Hurdia", "Amplectobelua", "Isoxys"):
            guild = "MOBILE_APEX_PREDATOR"
        elif phylum == "Arthropoda":
            guild = "MOBILE_APEX_PREDATOR"
        
        curated_rows.append((
            occ_id, taxon_name, taxon_rank, phylum, class_name, order_name, family, genus,
            guild, early_interval, late_interval, eag, lag, coll_no, ref_no
        ))
        
        cur.execute("""
            INSERT OR REPLACE INTO cambrian_occurrences (
                occurrence_id, taxon_name, taxon_rank, phylum, class, order_name, family, genus,
                functional_guild, early_interval, late_interval, max_ma, min_ma,
                pbdb_collection_no, reference_no
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, curated_rows[-1])
    
    conn.commit()
    print(f"  [Curated] Loaded {len(curated_rows)} occurrences into 'cambrian_occurrences'.")
    
    # 3. Compute Guild Diversity Summary across Guilds
    cur.execute("""
        SELECT
            functional_guild,
            COUNT(DISTINCT taxon_name) as richness,
            COUNT(*) as total_occs,
            ROUND(AVG((max_ma + min_ma) / 2.0), 2) as mean_age
        FROM cambrian_occurrences
        GROUP BY functional_guild
        ORDER BY richness DESC;
    """)
    summary = cur.fetchall()
    print("  [Guild Summary Breakdown]:")
    for g, rich, occs, age in summary:
        print(f"    - {g:25s}: {rich:4d} distinct taxa | {occs:4d} occurrences (mean age ~{age} Ma)")
    
    conn.close()
    print("=== [Pipeline 02] Complete ===")

if __name__ == "__main__":
    fetch_pbdb_occurrences()
