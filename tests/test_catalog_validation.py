"""
Load-bearing tests for the compliance-catalog validation layer.

Test budget: 3 tests (at budget ceiling per testing.md for a new feature).
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
QC_LAW25_PATH = REPO_ROOT / "regulations" / "quebec-law-25.yaml"
FIXTURE_DUPLICATE = REPO_ROOT / "tests" / "fixtures" / "invalid-duplicate-id.yaml"

CONTROL_ID_RE = re.compile(r"^CA-QC-LAW25-\d{3}$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _collect_controls(groups: list[dict]) -> list[dict]:  # type: ignore[type-arg]
    """Recursively collect controls from OSCAL groups."""
    result: list[dict] = []  # type: ignore[type-arg]
    for group in groups:
        result.extend(group.get("controls", []))
        result.extend(_collect_controls(group.get("groups", [])))
    return result


# ---------------------------------------------------------------------------
# Test 1 — Quebec Law 25 catalog structural integrity
#
# Load-bearing filter:
# 1. Failure signal: yes — any missing/malformed control causes an assertion
# 2. User-visible consequence: yes — a control gap means compliance advice is wrong
# 3. Non-redundant: yes — no other test checks QC content
# 4. Not testing framework: yes — tests our data, not yaml.safe_load
# ---------------------------------------------------------------------------


def test_quebec_law25_controls_complete() -> None:
    """quebec-law-25.yaml has ≥20 controls with valid IDs, no duplicates."""
    with QC_LAW25_PATH.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)

    catalog = doc["catalog"]
    controls = _collect_controls(catalog.get("groups", []))

    # Minimum control count
    assert len(controls) >= 20, (
        f"Expected ≥20 controls, found {len(controls)}"
    )

    # All IDs match CA-QC-LAW25-NNN
    bad_ids = [c["id"] for c in controls if not CONTROL_ID_RE.match(c["id"])]
    assert not bad_ids, f"Controls with non-conforming IDs: {bad_ids}"

    # No duplicate IDs
    ids = [c["id"] for c in controls]
    assert len(ids) == len(set(ids)), (
        f"Duplicate control IDs found: {[x for x in ids if ids.count(x) > 1]}"
    )

    # No duplicate UUIDs (among controls that declare one)
    uuids = [c["uuid"] for c in controls if "uuid" in c]
    assert len(uuids) == len(set(uuids)), (
        f"Duplicate UUIDs found: {[x for x in uuids if uuids.count(x) > 1]}"
    )


# ---------------------------------------------------------------------------
# Test 2 — Validator rejects known-bad fixture with duplicate control ID
#
# Load-bearing filter:
# 1. Failure signal: yes — if the validator doesn't catch duplicates, this fails
# 2. User-visible consequence: yes — duplicate IDs corrupt profile composition
# 3. Non-redundant: yes — tests validator logic, not catalog content
# 4. Not testing framework: yes — tests our Pydantic+logic, not pyyaml
# ---------------------------------------------------------------------------


def test_validator_rejects_duplicate_control_id() -> None:
    """validate_catalog._validate_file reports an error for duplicate control IDs."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from validate_catalog import _validate_file  # type: ignore[import-not-found]

    errors = _validate_file(FIXTURE_DUPLICATE)
    assert any("duplicate control id" in e.lower() for e in errors), (
        f"Expected duplicate-id error, got: {errors}"
    )


# ---------------------------------------------------------------------------
# Test 3 — Validator passes on the actual catalog directory
#
# Load-bearing filter:
# 1. Failure signal: yes — any catalog regression causes nonzero exit / errors
# 2. User-visible consequence: yes — CI gate would break on broken catalog
# 3. Non-redundant: yes — test 1 checks content; this checks all regulation files
# 4. Not testing framework: yes — exercises our validator end-to-end
# ---------------------------------------------------------------------------


def test_validator_passes_on_catalog_directory() -> None:
    """validate_catalog.main() exits 0 (returns 0) on the real catalog."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from validate_catalog import main  # type: ignore[import-not-found]

    result = main()
    assert result == 0, "validate_catalog.main() reported validation errors"
