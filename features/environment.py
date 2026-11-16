"""
BDD Environment configuration for public-science-harness.
Conforms to .agents/skills/bdd-precision/SKILL.md (:bdd.file/environment).
"""

from pathlib import Path


def before_all(context):
    """
    Initialize dynamic repository root and shared engine paths.
    """
    context.repo_root = Path(__file__).resolve().parent.parent


def before_scenario(context, scenario):
    """
    Context isolation: reset scenario state before each run.
    """
    context.raw_record = None
    context.sanitized_record = None
    context.audit_result = None
    context.violations = []
    context.ddl_output = None
