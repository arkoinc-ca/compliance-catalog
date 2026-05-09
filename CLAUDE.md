# compliance-catalog — Dev Instructions

This repo contains OSCAL-formatted regulatory control data only. No Python application runtime code lives here; only validation tooling is permitted.

For general Python stack standards (uv, ruff, mypy, pytest patterns), see the project root: [`.claude/CLAUDE.md`](../../.claude/CLAUDE.md).

---

## Schema requirement

All control files must pass the structural validator at `scripts/validate_catalog.py` (Pydantic v2; enforces `catalog`/`profile` top-level key, control-ID regex `^[A-Z]{2,3}(-[A-Z0-9]+)+-\d{3}$`, UUID v4, no duplicates, per-file minimum control count). Full OSCAL 1.0.2 schema conformance via `compliance-trestle` is **not** wired in v0.x — our YAMLs use a simplified OSCAL-shaped structure that does not match trestle's full-envelope expectation. See `docs/phases/phase-1-catalog-v0.md` Decision Log (2026-05-09) for rationale.

Validate before committing:

```bash
uv sync
uv run python scripts/validate_catalog.py
uv run pytest
```

CI runs the same commands via `.github/workflows/oscal-validate.yaml`. Do not open PRs with files that fail validation or pytest.

---

## Authoring format

- **YAML over JSON** for human-authored files. JSON is acceptable for machine-generated output only.
- Every regulation file must begin with a top-level block:
  ```yaml
  oscal-version: 1.0.2
  last-modified: "YYYY-MM-DDTHH:MM:SSZ"  # ISO-8601, UTC
  ```
- Control IDs must follow the pattern `<JURISDICTION>-<CODE>-<NNN>` zero-padded to 3 digits (e.g., `CA-PIPEDA-001`, `EU-GDPR-017`, `CA-CASL-003`, `CA-QC-LAW25-001`, `US-CA-CCPA-001`). Sequential integers; no gaps.
- Every control must include `parts.statement.prose` — a plain-English prose statement of the regulatory obligation. Do not leave it blank or use a placeholder.
- Profile files must declare the source regulation files they import and must pin to a specific catalog release tag.

---

## Conventions

| Rule | Requirement |
|------|-------------|
| Control ID format | `<SHORT-CODE>-<NNN>` (zero-padded to 3 digits) |
| `parts.statement.prose` | Required on every control; no placeholders |
| `last-modified` | Required on every regulation file; ISO-8601 UTC |
| `oscal-version` | Must be exactly `1.0.2` in every file |
| YAML line length | Max 120 characters |
| File names | `kebab-case.yaml` only |

---

## What does NOT belong here

- Python application code (services, APIs, CLI handlers).
- Semgrep rule *implementations* — those live in `detection-rules/semgrep/`. Only schema-conforming rule references belong in control metadata.
- Legal text reproduced verbatim without proper citation and CC-BY-compatible source confirmation.

<!-- written-by: builder-sonnet | model: sonnet -->
