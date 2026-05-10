"""
Load-bearing tests for the compliance-catalog validation layer.

Test budget: 6 tests (3 original + 1 for C-H5 GPAI controls + 1 for Wave-2A MEDIUM batch
+ 1 for W3-A1 severity vocabulary enforcement).
JUSTIFIED: +1 (W3-A1) because the severity closed-set validator is new behaviour; without
this test a regression to open-string severity would be invisible until a broken file
reached CI.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

import pytest

REPO_ROOT = Path(__file__).parent.parent
QC_LAW25_PATH = REPO_ROOT / "regulations" / "quebec-law-25.yaml"
EU_AI_ACT_PATH = REPO_ROOT / "regulations" / "eu-ai-act.yaml"
FIXTURE_DUPLICATE = REPO_ROOT / "tests" / "fixtures" / "invalid-duplicate-id.yaml"
FIXTURE_BAD_SEVERITY = REPO_ROOT / "tests" / "fixtures" / "invalid-severity.yaml"

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


# ---------------------------------------------------------------------------
# Test 4 — EU AI Act GPAI controls (C-H5) are present with non-empty prose
#
# Load-bearing filter:
# 1. Failure signal: yes — omitting or blanking a GPAI control causes failure
# 2. User-visible consequence: yes — missing GPAI controls means Art 53/54/55
#    obligations are invisible to any SaaS product using the EU profile
# 3. Non-redundant: yes — no other test checks EU AI Act GPAI content
# 4. Not testing framework: yes — tests our authored data, not pyyaml
# ---------------------------------------------------------------------------


def test_eu_ai_act_gpai_controls_present() -> None:
    """EU AI Act catalog contains EU-AI-ACT-017/018/019 with non-empty statement prose."""
    with EU_AI_ACT_PATH.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)

    catalog = doc["catalog"]
    controls = _collect_controls(catalog.get("groups", []))
    by_id = {c["id"]: c for c in controls}

    gpai_ids = ["EU-AI-ACT-017", "EU-AI-ACT-018", "EU-AI-ACT-019"]
    missing = [cid for cid in gpai_ids if cid not in by_id]
    assert not missing, f"Missing GPAI controls: {missing}"

    for cid in gpai_ids:
        ctrl = by_id[cid]
        parts = {p["name"]: p for p in ctrl.get("parts", [])}
        statement = parts.get("statement", {}).get("prose", "").strip()
        assert statement, f"{cid} has empty statement prose"


# ---------------------------------------------------------------------------
# Test 5 — Wave-2A MEDIUM batch: key new controls present with non-empty prose
#
# Load-bearing filter:
# 1. Failure signal: yes — omitting or blanking any of these controls causes failure
# 2. User-visible consequence: yes — a missing control means a compliance obligation
#    is invisible to every product using the affected region/use-case profile
# 3. Non-redundant: yes — test 4 covers GPAI; this covers GDPR/CCPA/LGPD/CASL/LL144/AI Act
# 4. Not testing framework: yes — tests our authored data, not pyyaml
#
# Representative IDs chosen: first new control per regulation (sufficient sentinel).
# ---------------------------------------------------------------------------

_WAVE2A_SENTINELS: list[tuple[str, str]] = [
    # (regulation filename stem, control ID)
    ("gdpr", "EU-GDPR-019"),          # C-M1: GDPR controller responsibility
    ("ccpa-cpra", "US-CA-CCPA-013"),  # C-M2: CCPA exemptions
    ("eu-ai-act", "EU-AI-ACT-020"),   # C-M3: EU AI Act Annex III biometric
    ("lgpd", "BR-LGPD-015"),          # C-M6: LGPD definitions
    ("casl", "CA-CASL-007"),          # C-M11: CASL implied consent
    ("nyc-ll144", "US-NY-LL144-005"), # C-M12: NYC LL144 scope
]


@pytest.mark.parametrize("stem,control_id", _WAVE2A_SENTINELS)
def test_wave2a_sentinel_controls_present(stem: str, control_id: str) -> None:
    """Each Wave-2A sentinel control exists in its regulation file with non-empty statement prose."""
    reg_path = REPO_ROOT / "regulations" / f"{stem}.yaml"
    with reg_path.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)

    controls = _collect_controls(doc["catalog"].get("groups", []))
    by_id = {c["id"]: c for c in controls}

    assert control_id in by_id, (
        f"{stem}.yaml is missing control {control_id}"
    )
    parts = {p["name"]: p for p in by_id[control_id].get("parts", [])}
    prose = parts.get("statement", {}).get("prose", "").strip()
    assert prose, f"{control_id} in {stem}.yaml has empty statement prose"


# ---------------------------------------------------------------------------
# Test 6 — Validator rejects fixture with unknown severity value (W3-A1)
#
# Load-bearing filter:
# 1. Failure signal: yes — if severity check is removed/broken, this fixture passes
# 2. User-visible consequence: yes — unknown severity silently ignored means
#    findings are miscategorised in the scanner output
# 3. Non-redundant: yes — no other test exercises severity vocabulary enforcement
# 4. Not testing framework: yes — tests our severity-check logic, not Pydantic
# ---------------------------------------------------------------------------


def test_validator_rejects_unknown_severity() -> None:
    """validate_catalog._validate_file reports an error for an unknown severity value."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from validate_catalog import _validate_file  # type: ignore[import-not-found]

    errors = _validate_file(FIXTURE_BAD_SEVERITY)
    assert any("unknown severity" in e.lower() for e in errors), (
        f"Expected unknown-severity error, got: {errors}"
    )
