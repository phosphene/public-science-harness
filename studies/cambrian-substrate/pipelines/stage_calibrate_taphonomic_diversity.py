#!/usr/bin/env python3
"""
Pipeline Stage: Calibrate Taphonomic Diversity & Emit Provenance Receipt.
Coordinates I/O for applying pure TaphonomicCalibrator rules to SQLite database.
Follows Hickey/Tellman naming: stage_calibrate_taphonomic_diversity.py
"""

from __future__ import annotations

import json
import sqlite3
import subprocess
from pathlib import Path

from phosphene.harness.data.transforms.receipts import ReceiptCompiler
from phosphene.harness.data.transforms.taphonomy import (
    CAMBRIAN_EPISTEMIC_ANNOTATIONS,
    CAMBRIAN_TRANSFORM_SPECS,
    TaphonomicCalibrator,
)

STUDY_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = STUDY_DIR / "data" / "raw"
CURATED_DIR = STUDY_DIR / "data" / "curated"
SQL_DIR = STUDY_DIR / "sql"
DB_PATH = CURATED_DIR / "cambrian_substrate.db"


def resolve_git_commit() -> str:
    """Safely retrieves active git commit SHA."""
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unversioned"


def execute_taphonomic_calibration_stage() -> None:
    print("=== [Pipeline Stage] Calibrate Taphonomic Diversity & Emit Provenance ===")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Apply Declarative SQL Schemas and Analytical Views
    ddl_file = SQL_DIR / "ddl" / "03_epistemic_annotations.sql"
    if ddl_file.exists():
        cur.executescript(ddl_file.read_text())

    views_file = SQL_DIR / "views" / "02_calibrated_guild_views.sql"
    if views_file.exists():
        cur.executescript(views_file.read_text())

    # 2. Materialize Epistemic Data Annotations
    cur.execute("DELETE FROM epistemic_data_annotations;")
    for a in CAMBRIAN_EPISTEMIC_ANNOTATIONS:
        cur.execute(
            """
            INSERT INTO epistemic_data_annotations (
                annotation_id, timestamp_utc, actor_id, actor_role, target_entity_type,
                target_selector, judgment_type, epistemic_warrant_doi, epistemic_warrant_citation,
                rationale, recommended_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                a.annotation_id,
                a.timestamp_utc,
                a.actor_id,
                a.actor_role,
                a.target_entity_type,
                a.target_selector,
                a.judgment_type.value.upper(),
                a.epistemic_warrant_doi,
                a.epistemic_warrant_citation,
                a.rationale,
                a.recommended_action,
            ),
        )
    conn.commit()
    print(f"  [Annotations] Stored {len(CAMBRIAN_EPISTEMIC_ANNOTATIONS)} epistemic data annotations in SQLite.")

    # 3. Query Calibrated View to verify taphonomic gating
    print("\n  [Calibrated View: v_calibrated_guild_diversity]")
    cur.execute(
        """
        SELECT functional_guild, raw_distinct_taxa, raw_occurrences, sampling_ratio,
               preservation_mode_tier, fortunian_tiering_depth_mm, calibration_status
        FROM v_calibrated_guild_diversity;
        """
    )
    for r in cur.fetchall():
        print(f"    - {r[0]:25s}: Taxa={r[1]:3d} | Occs={r[2]:3d} | Ratio={r[3]:4.2f} | Tier={r[4]:24s} | Depth={r[5]:4.1f}mm | Status={r[6]}")

    # 4. Pure Functional Receipt Compilation
    git_sha = resolve_git_commit()
    input_files = [
        RAW_DIR / "stratigraphic_horizons_raw.csv",
        RAW_DIR / "pbdb_cambrian_metazoa_raw.json",
    ]
    output_files = [DB_PATH]

    receipt = ReceiptCompiler.compile_receipt(
        pipeline_id="pipelines/stage_calibrate_taphonomic_diversity.py",
        git_commit_sha=git_sha,
        actor_id="flow@feelingflowingbot",
        applied_transforms=CAMBRIAN_TRANSFORM_SPECS,
        input_paths=[p for p in input_files if p.exists()],
        output_paths=[p for p in output_files if p.exists()],
        annotations=CAMBRIAN_EPISTEMIC_ANNOTATIONS,
    )

    # 5. Persist Receipt to SQLite and Curated Disk Artifact
    cur.execute(
        """
        INSERT OR REPLACE INTO dataset_provenance_receipts (
            receipt_id, pipeline_id, git_commit_sha, executed_at_utc, actor_id,
            transforms_applied_json, input_artifacts_json, output_artifacts_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            receipt.receipt_id,
            receipt.pipeline_id,
            receipt.git_commit_sha,
            receipt.executed_at_utc,
            receipt.actor_id,
            json.dumps([s.model_dump() for s in CAMBRIAN_TRANSFORM_SPECS]),
            json.dumps([fp.model_dump() for fp in receipt.input_artifacts]),
            json.dumps([fp.model_dump() for fp in receipt.output_artifacts]),
        ),
    )
    conn.commit()
    conn.close()

    receipt_json = CURATED_DIR / "PROVENANCE_RECEIPT.json"
    receipt_json.write_text(json.dumps(receipt.model_dump(), indent=2))
    print(f"\n  [Receipt] Emitted machine-verifiable receipt to {receipt_json.name}")
    print("=== [Pipeline Stage Complete] ===")


if __name__ == "__main__":
    execute_taphonomic_calibration_stage()
