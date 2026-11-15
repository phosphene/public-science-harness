"""
SQLite STRICT DDL Compiler.
Conforms to Mertz (2021) Ch. 1 & DATA_STANDARDS.md Section 6.2 / PSH-005.
"""

from __future__ import annotations

from typing import Sequence
from phosphene.harness.data.core.vitals import InvariantStatic


class ColumnDef(InvariantStatic):
    name: str
    data_type: str  # INT, INTEGER, REAL, TEXT, BLOB, ANY
    is_primary_key: bool = False
    is_not_null: bool = True
    check_expr: str | None = None


class StrictTableSchema(InvariantStatic):
    table_name: str
    columns: list[ColumnDef]
    table_checks: list[str] = []
    foreign_keys: list[str] = []

    def to_sqlite_strict_ddl(self) -> str:
        """
        Emits DDL enforcing SQLite's STRICT table mode to eliminate type affinity loopholes.
        """
        col_lines = []
        for col in self.columns:
            parts = [f"    {col.name} {col.data_type}"]
            if col.is_primary_key:
                parts.append("PRIMARY KEY")
            if col.is_not_null and not col.is_primary_key:
                parts.append("NOT NULL")
            if col.check_expr:
                parts.append(f"CHECK ({col.check_expr})")
            col_lines.append(" ".join(parts))

        for tc in self.table_checks:
            col_lines.append(f"    CHECK ({tc})")

        for fk in self.foreign_keys:
            col_lines.append(f"    {fk}")

        inner = ",\n".join(col_lines)
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (\n{inner}\n) STRICT;\n"
