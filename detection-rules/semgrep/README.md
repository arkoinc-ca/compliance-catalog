<!-- written-by: builder-sonnet | model: sonnet -->

# Semgrep Detection Rules

This directory holds Semgrep rule YAML files that map statically to OSCAL control IDs from `regulations/`.

## Convention

Each rule file follows standard [Semgrep rule syntax](https://semgrep.dev/docs/writing-rules/rule-syntax/) with one required extension in the `metadata` block: a `controls` list that references the OSCAL control IDs this rule detects a violation of.

```yaml
rules:
  - id: pii-in-logs-001
    patterns:
      - pattern: logger.info(..., $PII, ...)
      - pattern-not: logger.info(..., redact($PII), ...)
    message: |
      Potential PII written to application log. Logging personal information may violate
      PIPEDA Principle 7 (Safeguards) and GDPR Art. 32 (Security of processing).
    languages: [python]
    severity: ERROR
    metadata:
      controls:
        - "PIPEDA-7"       # Safeguards
        - "GDPR-5-1-f"    # Integrity and confidentiality
        - "QC-LAW25-10"   # Security measures
      category: pii-in-logs
      confidence: MEDIUM
      false-positive-rate: "0.12"
      references:
        - https://laws-lois.justice.gc.ca/eng/acts/P-8.6/
```

## File Naming

Files are named by the detection category they cover, not by a specific regulation. One rule file may reference controls across multiple regulations.

| File | Category |
|------|----------|
| `pii-in-logs.yaml` | PII written to application logs |
| `missing-consent.yaml` | Absence of consent collection mechanism |
| `missing-dsr-handler.yaml` | No data-subject-request endpoint or handler |
| `missing-audit-emission.yaml` | Audit event not emitted at access/mutation boundary |
| `unprotected-sensitive-field.yaml` | Sensitive field stored without encryption marker |

## Adding a New Rule

1. Identify the control ID(s) from `regulations/<file>.yaml` that this rule enforces.
2. Create or append to the appropriate category file under `detection-rules/semgrep/`.
3. Add the `metadata.controls` list referencing those IDs.
4. Register the mapping in `detection-rules/mapping.yaml`.
5. Open a PR; CI will validate YAML syntax and confirm all referenced control IDs exist in the catalog.

## Control ID Reference Format

Control IDs follow the pattern `<SHORT-CODE>-<CONTROL-NUM>` as defined in each regulation catalog, for example:

- `PIPEDA-1`, `PIPEDA-7`
- `QC-LAW25-1`, `QC-LAW25-10`
- `GDPR-5-1-a`, `GDPR-32`
- `CASL-1`

Semgrep rules are scheduled for authoring in Phase 2 of the implementation plan.
