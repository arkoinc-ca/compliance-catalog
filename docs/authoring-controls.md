<!-- written-by: builder-sonnet | model: sonnet -->

# Authoring Controls

This guide shows how to add a new control to an existing regulation catalog.

## Prerequisites

- Basic familiarity with YAML
- Access to the authoritative regulation text (see `docs/regulation-sources.md`)
- A GitHub account and a fork of this repository

---

## Step 1 — Pick a Regulation

Identify which regulation file the control belongs to. Files live under `regulations/`.

```
regulations/pipeda.yaml
regulations/quebec-law-25.yaml
regulations/pipa-ab.yaml
regulations/pipa-bc.yaml
regulations/casl.yaml
regulations/gdpr.yaml
regulations/ccpa-cpra.yaml
regulations/nyc-ll144.yaml
regulations/colorado-ai-act.yaml
```

If the regulation does not exist yet, open an issue before authoring.

---

## Step 2 — Find the Source Citation

Read the regulation text from the authoritative URL listed in `docs/regulation-sources.md`. Identify:

- The article or section number (e.g., GDPR Art. 17, PIPEDA Principle 4)
- The exact obligation imposed
- Whether it is technically detectable (code pattern) or requires human attestation

---

## Step 3 — Open the Regulation YAML

Open `regulations/<file>.yaml`. The file follows OSCAL catalog structure. Add your control inside the relevant `groups[].controls[]` list.

**Control ID convention:** `<SHORT-CODE>-<CONTROL-NUM>`, for example `PIPEDA-7`, `GDPR-17`, `QC-LAW25-10`.

---

## Step 4 — Add the Control Entry

```yaml
# Example diff — adding PIPEDA-7 (Safeguards) to regulations/pipeda.yaml
groups:
  - id: "pipeda-fair-info-principles"
    title: "Fair Information Principles (Schedule 1)"
    controls:
      - id: "PIPEDA-7"
        title: "Safeguards — Protect personal information with security appropriate to its sensitivity"
        props:
          - name: "status"
            value: "draft"
          - name: "source-article"
            value: "Schedule 1, Principle 7"
        parts:
          - id: "PIPEDA-7-stmt"
            name: "statement"
            prose: |
              Personal information shall be protected by security safeguards
              appropriate to the sensitivity of the information. The safeguards
              shall protect personal information against loss or theft, as well
              as unauthorized access, disclosure, copying, use, or modification.
              Organizations shall protect personal information regardless of the
              format in which it is held.
          - id: "PIPEDA-7-guidance"
            name: "guidance"
            prose: |
              Safeguards appropriate to sensitivity means: encryption at rest
              and in transit for high-sensitivity data; access controls; audit
              logging of access events; and incident response procedures.
```

Change `status` from `skeleton` to `draft` when you add real content, and to `final` after peer review.

---

## Step 5 — Map to a Detection Rule (or Mark as Questionnaire-Only)

After adding the control, register it in `detection-rules/mapping.yaml`:

```yaml
- control-id: "PIPEDA-7"
  regulation: "PIPEDA"
  title: "Safeguards — Security appropriate to sensitivity"
  detection-methods:
    - method: semgrep
      file: "detection-rules/semgrep/pii-in-logs.yaml"
      rule-id: "pii-log-001"
      notes: "PII in logs violates the safeguards principle."
    - method: questionnaire
      file: "detection-rules/questionnaire/governance-breach-procedure.yaml"
      fragment-id: "q-incident-response-documented"
      notes: "Documented incident response is not statically detectable."
```

If the control has no detectable code pattern, use only `method: questionnaire`.

---

## Step 6 — Add Tests

Run YAML validation locally:

```bash
uv run python -m pytest tests/ -v
```

The test suite validates that:
- All control IDs in `mapping.yaml` exist in the corresponding regulation YAML.
- All regulation YAMLs parse as valid YAML.
- All profile imports reference control IDs that exist.

---

## Step 7 — Open a PR

1. Commit your changes with message: `feat(catalog): add <REGULATION>-<NUM> — <short title>`
2. Open a pull request against `main`.
3. CI will run `oscal-validate` to confirm OSCAL 1.0.2 schema compliance.
4. A maintainer will peer-review the control text against the source legislation.

---

## Control Status Lifecycle

| Status | Meaning |
|--------|---------|
| `skeleton` | Placeholder structure; `prose: "TODO"` |
| `draft` | Control text authored; peer review pending |
| `final` | Peer-reviewed against source legislation |
| `deprecated` | Superseded; kept for history |
