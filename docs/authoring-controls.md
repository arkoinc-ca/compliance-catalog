# Authoring Controls

A **control** in this catalog is an OSCAL-shaped statement of a single regulatory obligation traceable to a specific statutory section. Controls power two downstream tools: the `compliance-assess` command-line assessor (gap detection) and the `compliance-browser` web interface (search and browsing). The three load-bearing files are:

- `regulations/<regulation>.yaml` — the control definitions
- `profiles/` — compositions of controls into region or use-case sets
- `detection-rules/mapping.yaml` — the join table that maps each control ID to detection method(s)

---

## File anatomy

A minimal control inside a regulation YAML looks like this:

```yaml
- id: "CA-PIPEDA-007"               # canonical ID — see Control IDs section
  uuid: "a1b2c3d4-0072-4000-8000-100000000072"  # UUID v4 — see UUIDs section
  title: "Safeguards — Protect personal information with security appropriate to sensitivity"
  props:
    - name: "severity"
      value: "high"                 # high | medium | low — see Severity section
    - name: "source-section"
      value: "Schedule 1, Principle 7"
    - name: "effective-date"
      value: "2001-01-01"
    - name: "jurisdiction"
      value: "CA"
    - name: "status"
      value: "final"                # skeleton | draft | final | deprecated
  parts:
    - id: "CA-PIPEDA-007-stmt"
      name: "statement"
      prose: |
        Personal information shall be protected by security safeguards
        appropriate to the sensitivity of the information.
  links:
    - href: "https://laws-lois.justice.gc.ca/eng/acts/P-8.6/"
      rel: source
      text: "PIPEDA — Schedule 1, Principle 7"
```

---

## Required fields

| Field | Regex / constraint | Example |
|---|---|---|
| `id` | `^[A-Z]{2,3}(-[A-Z0-9]+)+-\d{3}$` | `CA-PIPEDA-007` |
| `uuid` | UUID v4 | `a1b2c3d4-0072-4000-8000-100000000072` |
| `title` | Non-empty string | `"Safeguards — ..."` |
| `parts[name=statement].prose` | Non-empty plain English | Full obligation text |
| `props[name=severity].value` | `high`, `medium`, or `low` | `high` |
| `props[name=source-section].value` | Statute section reference | `"Schedule 1, Principle 7"` |
| `props[name=effective-date].value` | ISO-8601 date | `"2001-01-01"` |
| `props[name=jurisdiction].value` | Jurisdiction prefix | `"CA"` |
| `props[name=status].value` | Lifecycle status | `"draft"` |
| `links[rel=source].href` | Authoritative government URL | `https://laws-lois.justice.gc.ca/...` |

---

## Control IDs

The canonical format is `<JURISDICTION>-<CODE>-<NNN>`:

- `<JURISDICTION>` — 2–3 uppercase letters from the table below
- `<CODE>` — short regulation code; may include dashes and numbers (`PIPEDA`, `QC-LAW25`, `AB-PIPA`, `BC-PIPA`, `CASL`, `GDPR`, `CCPA`, `NY-LL144`, `CO-AI`) (Note: a regulation's `<CODE>` (used in control IDs) may be a shortened form of its `regulation-short-code` metadata (e.g., `CO-AI` in IDs vs. `CO-AI-ACT` in metadata).)
- `<NNN>` — zero-padded three-digit integer, sequential, no gaps

Jurisdiction prefixes in use:

| Prefix | Meaning |
|---|---|
| `CA` | Canada (federal) |
| `CA-QC` | Canada — Quebec |
| `CA-AB` | Canada — Alberta |
| `CA-BC` | Canada — British Columbia |
| `EU` | European Union |
| `US-CA` | United States — California |
| `US-NY` | United States — New York |
| `US-CO` | United States — Colorado |

Examples: `CA-PIPEDA-001`, `CA-QC-LAW25-025`, `EU-GDPR-018`, `US-CA-CCPA-012`.

IDs must be sequential within a file. Do not reuse or skip numbers.

---

## UUIDs

Each regulation file uses a sequential UUID bank following the pattern `a1b2c3d4-<NNNN>-4000-8000-1000000000NN` where `<NNNN>` encodes the regulation and control number. New regulations should start a fresh bank. `uuidgen` is acceptable for generating new UUIDs — just ensure they are v4 and unique within the file.

The validator checks for UUID v4 format and rejects duplicates within a file.

---

## Validation locally

```bash
uv sync
uv run python scripts/validate_catalog.py
uv run pytest
```

Both commands must exit 0 before opening a PR. CI runs the same commands via `.github/workflows/oscal-validate.yaml`.

---

## Adding a new regulation

Follow these seven steps in order:

1. **Get the authoritative source URL.** Use government sources only (see `docs/regulation-sources.md`). Do not start from third-party summaries.
2. **Draft the control list with statutory references.** Map each distinct obligation to a section number. Aim for 5–20 controls per regulation; split complex articles if they impose independent obligations.
3. **Get an SME to review the obligation list before YAML.** A legal or privacy SME should confirm the obligation list reflects the statute accurately before you invest time authoring YAML. Record the review in a GitHub issue comment or PR review.
4. **Write the YAML.** Use an existing regulation file as a template (e.g., `regulations/casl.yaml` for a short regulation, `regulations/gdpr.yaml` for a complex one). Every control needs `id`, `uuid`, `title`, `props`, `parts.statement.prose`, and `links[rel=source]`.
5. **Update the validator `MIN_CONTROLS` threshold.** Open `scripts/validate_catalog.py` and add your regulation's stem to the `MIN_CONTROLS` dict with the expected minimum count.
6. **Add to relevant region and use-case profiles.** Identify which region profiles (`profiles/region/`) should import the new regulation and add it to their `imports` list with all control IDs.
7. **Add mappings to `detection-rules/mapping.yaml`.** Every new control needs at least one detection method. See the Detection method choice section below.

---

## Detection method choice

Choose the detection method based on where the obligation manifests:

| Method | When to use | Example controls |
|---|---|---|
| `questionnaire` | Organizational or policy obligation that can only be attested by a human | Privacy officer designation, breach notification SOPs, vendor contracts, training records |
| `semgrep` | Code pattern that can be flagged by static analysis | PII written to logs, missing consent gate before data collection endpoint, missing DSR handler route, no retention TTL constant |
| `otel` | Runtime behavior observable via OpenTelemetry instrumentation | Consent events emitted at runtime, deletion completion metrics, bias/fairness metric streams, automated decision event traces |

Most controls use `questionnaire` as the primary (or only) method. `semgrep` and `otel` are additive — a control can have more than one method when it has both a detectable code pattern and a non-detectable organizational component.

---

## Source citation policy

- `links[rel=source]` must point to the **primary government source**: `laws-lois.justice.gc.ca`, `eur-lex.europa.eu`, `leginfo.legislature.ca.gov`, `bclaws.gov.bc.ca`, `qp.alberta.ca`, `leg.colorado.gov`, `nyc.gov`.
- Regulator guidance documents (OPC guidance, EDPB opinions, CPPA regulations) are acceptable as `parts.guidance` content but must not replace the primary statute citation in `links[rel=source]`.
- Never cite IAPP summaries, law firm memos, or blog posts as the primary source.

---

## Control status lifecycle

| Status | Meaning |
|---|---|
| `skeleton` | Placeholder structure; `prose: "TODO"` |
| `draft` | Control text authored; SME review pending |
| `final` | SME-reviewed against source legislation |
| `deprecated` | Superseded; kept for audit history |

For SME sign-off cadence, see `docs/human-action-checklist.md` H-07.

<!-- written-by: builder-sonnet | model: sonnet -->
