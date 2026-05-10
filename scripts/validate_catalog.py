"""
Catalog structure validator for compliance-catalog OSCAL YAML files.

Validates:
- Every YAML file under regulations/ and profiles/ loads without error.
- Each file has a top-level 'catalog' or 'profile' key.
- Required metadata fields are present (uuid, metadata with title).
- Control IDs match the canonical pattern ^[A-Z]{2,3}(-[A-Z0-9]+)+-\\d{3}$.
- UUIDs in controls match UUID v4 format.
- No duplicate control IDs within a file.
- No duplicate UUIDs within a file.
- quebec-law-25.yaml has at least 20 controls.
- Each regulation file has at least 1 control.

Exit code: 0 on success, 1 on any validation failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

CONTROL_ID_RE = re.compile(r"^[A-Z]{2,3}(-[A-Z0-9]+)+-\d{3}$")
UUID_V4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

# Minimum controls required per regulation file, keyed by filename stem.
# Enforces phase-1 P1-G02: each authored regulation has ≥5 controls; QC has ≥20.
# Placeholder regulations (not yet in force) keep the default min of 1.
MIN_CONTROLS: dict[str, int] = {
    "quebec-law-25": 20,
    "pipeda": 10,
    "pipa-ab": 8,
    "pipa-bc": 8,
    "casl": 8,
    "gdpr": 22,
    "ccpa-cpra": 15,
    "nyc-ll144": 5,
    "colorado-ai-act": 4,
    "eu-ai-act": 26,
    "phipa-on": 14,
    "virginia-vcdpa": 13,
    "connecticut-ctdpa": 11,
    "utah-ucpa": 10,
    "lgpd": 21,
    "uk-gdpr": 10,
    "illinois-bipa": 6,
}
DEFAULT_MIN_CONTROLS = 1


# ---------------------------------------------------------------------------
# Pydantic models (structural validation only — not full OSCAL schema)
# ---------------------------------------------------------------------------


class ControlPart(BaseModel):
    id: str
    name: str
    prose: str = ""


class Control(BaseModel):
    id: str
    uuid: str | None = None
    title: str
    props: list[dict[str, str]] = Field(default_factory=list)
    parts: list[ControlPart] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def id_matches_pattern(cls, v: str) -> str:
        if not CONTROL_ID_RE.match(v):
            raise ValueError(
                f"Control id '{v}' does not match pattern "
                r"^[A-Z]{2,3}(-[A-Z0-9]+)+-\d{3}$"
            )
        return v

    @field_validator("uuid")
    @classmethod
    def uuid_matches_v4(cls, v: str | None) -> str | None:
        if v is not None and not UUID_V4_RE.match(v):
            raise ValueError(f"UUID '{v}' is not a valid UUID v4")
        return v


class Group(BaseModel):
    id: str
    title: str
    controls: list[Control] = Field(default_factory=list)
    groups: list[Group] = Field(default_factory=list)


Group.model_rebuild()


class CatalogMetadata(BaseModel):
    title: str


class CatalogDoc(BaseModel):
    uuid: str
    metadata: CatalogMetadata
    groups: list[Group] = Field(default_factory=list)

    @field_validator("uuid")
    @classmethod
    def uuid_matches_v4(cls, v: str) -> str:
        if not UUID_V4_RE.match(v):
            raise ValueError(f"Catalog uuid '{v}' is not a valid UUID v4")
        return v


class ProfileDoc(BaseModel):
    uuid: str
    metadata: CatalogMetadata


# ---------------------------------------------------------------------------
# Helper: flatten controls from nested groups
# ---------------------------------------------------------------------------


def _collect_controls(groups: list[Group]) -> list[Control]:
    result: list[Control] = []
    for group in groups:
        result.extend(group.controls)
        result.extend(_collect_controls(group.groups))
    return result


# ---------------------------------------------------------------------------
# Per-file validation
# ---------------------------------------------------------------------------


def _validate_file(path: Path) -> list[str]:
    """Return a list of error strings (empty = pass)."""
    errors: list[str] = []

    # 1. Parse YAML
    try:
        with path.open(encoding="utf-8") as fh:
            raw: Any = yaml.safe_load(fh)
    except Exception as exc:
        return [f"{path}: YAML parse error: {exc}"]

    if not isinstance(raw, dict):
        return [f"{path}: top-level value must be a mapping, got {type(raw).__name__}"]

    # 2. Determine file type
    if "catalog" in raw:
        doc_type = "catalog"
        payload = raw["catalog"]
    elif "profile" in raw:
        doc_type = "profile"
        payload = raw["profile"]
    else:
        return [f"{path}: missing top-level 'catalog' or 'profile' key"]

    # 3. Structural validation via Pydantic
    controls: list[Control] = []
    try:
        if doc_type == "catalog":
            catalog = CatalogDoc.model_validate(payload)
            controls = _collect_controls(catalog.groups)
        else:
            ProfileDoc.model_validate(payload)
            return []  # profiles: structural check only for now
    except Exception as exc:
        errors.append(f"{path}: structural validation failed: {exc}")
        return errors

    # 4. Duplicate control ID check
    seen_ids: set[str] = set()
    for ctrl in controls:
        if ctrl.id in seen_ids:
            errors.append(f"{path}: duplicate control id '{ctrl.id}'")
        seen_ids.add(ctrl.id)

    # 5. Duplicate UUID check (among controls that declare UUIDs)
    seen_uuids: set[str] = set()
    for ctrl in controls:
        if ctrl.uuid is not None:
            if ctrl.uuid in seen_uuids:
                errors.append(f"{path}: duplicate control uuid '{ctrl.uuid}'")
            seen_uuids.add(ctrl.uuid)

    # 6. Minimum control count
    stem = path.stem
    required = MIN_CONTROLS.get(stem, DEFAULT_MIN_CONTROLS)
    if len(controls) < required:
        errors.append(
            f"{path}: expected at least {required} controls, found {len(controls)}"
        )

    # 7. Severity vocabulary check — props named "severity" must use the closed set
    _VALID_SEVERITIES = {"critical", "high", "medium", "low", "info"}
    for ctrl in controls:
        for prop in ctrl.props:
            if prop.get("name") == "severity":
                val = prop.get("value", "")
                if val not in _VALID_SEVERITIES:
                    errors.append(
                        f"{path}: control '{ctrl.id}' has unknown severity '{val}'; "
                        f"must be one of {sorted(_VALID_SEVERITIES)}"
                    )

    return errors


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

# tests/fixtures/ is excluded — invalid-fixture files must not poison real validation runs.
SCAN_DIRS = ["regulations", "profiles/region", "profiles/use-case"]


def main() -> int:
    repo_root = Path(__file__).parent.parent
    all_errors: list[str] = []
    file_count = 0

    for subdir in SCAN_DIRS:
        target = repo_root / subdir
        if not target.exists():
            continue
        for yaml_path in sorted(target.glob("*.yaml")):
            file_count += 1
            file_errors = _validate_file(yaml_path)
            all_errors.extend(file_errors)

    if all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(
            f"\nValidation FAILED: {len(all_errors)} error(s) across {file_count} files.",
            file=sys.stderr,
        )
        return 1

    print(f"Validation OK: {file_count} file(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
