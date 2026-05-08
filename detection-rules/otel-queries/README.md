<!-- written-by: builder-sonnet | model: sonnet -->

# OpenTelemetry Runtime Probes

This directory holds OpenTelemetry-based runtime probe templates. These complement the static Semgrep rules by catching compliance gaps that only manifest at runtime — such as a retention window being exceeded, a consent receipt never being stored, or a data-subject request sitting unacknowledged past the legal deadline.

## What Goes Here

Each file in this directory is a YAML template describing an OTel-backed probe. Templates reference:

- **PromQL expressions** for Prometheus-scraped metrics emitted by the enforcer sidecar.
- **OTel metric names and attribute filters** for SDK-instrumented services.
- **Alert thresholds** tied to specific regulatory deadlines (e.g., 72-hour GDPR breach notification window).

## Template Structure

```yaml
probe:
  id: "retention-window-exceeded-001"
  title: "Retention Window Exceeded — Data held past configured retention period"
  controls:
    - "PIPEDA-5"       # Limiting Use, Disclosure, and Retention
    - "GDPR-5-1-e"    # Storage limitation
    - "QC-LAW25-12"   # Retention period
  engine: promql
  query: |
    (time() - compliance_data_record_created_at_seconds{dataset=~".+"})
    / 86400
    > on(dataset) compliance_retention_limit_days
  threshold:
    severity: ERROR
    description: "Data record age exceeds configured retention limit in days."
  references:
    - https://laws-lois.justice.gc.ca/eng/acts/P-8.6/
    - https://eur-lex.europa.eu/eli/reg/2016/679/oj
```

## Categories

| File | Category |
|------|----------|
| `retention-violation.yaml` | Data held past retention window |
| `dsr-deadline-breach.yaml` | DSR response past statutory deadline (30 days CA / 30 days GDPR) |
| `consent-receipt-missing.yaml` | Transaction processed with no consent record emitted |
| `audit-gap.yaml` | Access event with no corresponding audit-log emission |
| `breach-notification-window.yaml` | Incident open > 72 hours without notification record |

## Adding a Probe

1. Identify the control ID(s) from `regulations/<file>.yaml` that this probe enforces.
2. Create or extend a category file under `detection-rules/otel-queries/`.
3. Add the `controls` list referencing those IDs.
4. Register the mapping in `detection-rules/mapping.yaml`.
5. Confirm the OTel metric names are emitted by the enforcer sidecar (see `repos/compliance-enforce/`).

OTel probe authoring is scheduled for Phase 2 of the implementation plan alongside the assessor sidecar.
