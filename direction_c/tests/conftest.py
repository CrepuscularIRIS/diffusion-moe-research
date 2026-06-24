"""Pytest configuration for the Direction C test suite.

Registers the ``unit`` marker (per the project Python testing rules) so the
suite runs without ``PytestUnknownMarkWarning`` noise, and ensures the repo
root is importable as ``direction_c`` when pytest is invoked from elsewhere.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Repo root = direction_c/tests/conftest.py -> parents[2].
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def pytest_configure(config) -> None:
    """Register custom markers used by this suite."""
    config.addinivalue_line("markers", "unit: fast, isolated unit test (no model)")
    config.addinivalue_line(
        "markers", "integration: requires the DiffusionGemma model (skipped by default)"
    )
