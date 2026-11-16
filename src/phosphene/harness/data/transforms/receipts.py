"""
Receipt Dispatcher & Artifact Fingerprinting.
Pure functional receipt construction decoupled from storage medium.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from phosphene.harness.data.transforms.provenance import (
    ArtifactFingerprint,
    DataAnnotationEvent,
    DatasetProvenanceReceipt,
    TransformSpec,
)


class ReceiptCompiler:
    """
    Pure compiler creating verifiable provenance receipts from artifact states.
    """

    @staticmethod
    def fingerprint_path(path: Path) -> ArtifactFingerprint:
        """
        Computes SHA-256 fingerprint for a path.
        """
        if not path.exists():
            raise FileNotFoundError(f"Artifact not found: {path}")
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        return ArtifactFingerprint(
            path=str(path.name),
            sha256=h,
            size_bytes=path.stat().st_size,
        )

    @classmethod
    def compile_receipt(
        cls,
        pipeline_id: str,
        git_commit_sha: str,
        actor_id: str,
        applied_transforms: Sequence[TransformSpec],
        input_paths: Sequence[Path],
        output_paths: Sequence[Path],
        annotations: Sequence[DataAnnotationEvent],
    ) -> DatasetProvenanceReceipt:
        """
        Builds an immutable DatasetProvenanceReceipt.
        """
        input_fps = [cls.fingerprint_path(p) for p in input_paths]
        output_fps = [cls.fingerprint_path(p) for p in output_paths]
        receipt_id = f"rcpt-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{Path(pipeline_id).stem}"

        return DatasetProvenanceReceipt(
            receipt_id=receipt_id,
            pipeline_id=pipeline_id,
            git_commit_sha=git_commit_sha,
            actor_id=actor_id,
            transform_specs_applied=[s.transform_id for s in applied_transforms],
            input_artifacts=input_fps,
            output_artifacts=output_fps,
            annotations_emitted=list(annotations),
        )
