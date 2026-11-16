"""
Sample-Size Scaled Outliers and Multivariate Invariants.
Conforms to Mertz (2021) Ch. 4 / PSH-004, PSH-006.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence
from phosphene.harness.data.core.vitals import InvariantStatic


class OutlierAuditResult(InvariantStatic):
    column_name: str
    sample_size: int
    mean: float
    std_dev: float
    effective_sigma_threshold: float
    outlier_count: int
    outlier_indices: list[int]
    outlier_values: list[float]


class DomainInvariantViolation(InvariantStatic):
    invariant_name: str
    row_index: int
    record_id: str | None
    violation_message: str


class OutlierAndInvariantEngine:
    """
    Computes sample-size adjusted outlier fences and evaluates cross-column multivariate invariants.
    """

    @classmethod
    def compute_sample_scaled_outliers(
        cls, column_name: str, values: Sequence[float | None]
    ) -> OutlierAuditResult:
        valid_pairs = [(i, float(v)) for i, v in enumerate(values) if v is not None and not math.isnan(float(v))]
        n = len(valid_pairs)
        if n < 4:
            return OutlierAuditResult(
                column_name=column_name,
                sample_size=n,
                mean=0.0,
                std_dev=0.0,
                effective_sigma_threshold=3.0,
                outlier_count=0,
                outlier_indices=[],
                outlier_values=[],
            )

        mean_val = sum(v for _, v in valid_pairs) / n
        variance = sum((v - mean_val) ** 2 for _, v in valid_pairs) / (n - 1)
        std_val = math.sqrt(variance) if variance > 0 else 1e-12

        # Scale threshold with sample size N:
        # For small N (< 1000), standard 3.0 sigma
        # For medium N (1,000 - 10,000), 3.5 sigma
        # For large N (10,000 - 100,000), 4.0 sigma
        # For very large N (> 100,000), 4.5 sigma
        if n < 1_000:
            k_sigma = 3.0
        elif n < 10_000:
            k_sigma = 3.5
        elif n < 100_000:
            k_sigma = 4.0
        else:
            k_sigma = 4.5

        outlier_indices = []
        outlier_values = []
        for idx, val in valid_pairs:
            z_score = abs(val - mean_val) / std_val
            if z_score > k_sigma:
                outlier_indices.append(idx)
                outlier_values.append(val)

        return OutlierAuditResult(
            column_name=column_name,
            sample_size=n,
            mean=mean_val,
            std_dev=std_val,
            effective_sigma_threshold=k_sigma,
            outlier_count=len(outlier_indices),
            outlier_indices=outlier_indices,
            outlier_values=outlier_values,
        )

    @classmethod
    def evaluate_invariants(
        cls,
        records: Sequence[dict],
        invariants: list[tuple[str, Callable[[dict], tuple[bool, str]]]],
        id_key: str | None = None,
    ) -> list[DomainInvariantViolation]:
        violations = []
        for idx, rec in enumerate(records):
            rec_id = str(rec.get(id_key)) if id_key and id_key in rec else None
            for inv_name, inv_fn in invariants:
                passed, msg = inv_fn(rec)
                if not passed:
                    violations.append(
                        DomainInvariantViolation(
                            invariant_name=inv_name,
                            row_index=idx,
                            record_id=rec_id,
                            violation_message=msg,
                        )
                    )
        return violations
