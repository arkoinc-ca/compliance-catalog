# compliance-catalog

OSCAL JSON/YAML control definitions for privacy, AI governance, and anti-spam obligations across Canadian, US, and EU jurisdictions.

![Status](https://img.shields.io/badge/status-v0%20pre--release-orange)
![License](https://img.shields.io/badge/license-CC--BY--4.0-green)
![OSCAL](https://img.shields.io/badge/OSCAL-1.0.2-blue)

> **v0 — pre-release; awaiting Phase 1 controls authoring (target: June–August 2026)**

---

> **DISCLAIMER**
>
> This toolkit is software. It identifies potential compliance gaps in code and provides runtime technical controls. It does **not** constitute legal advice and does not guarantee regulatory compliance. It does not appoint Data Protection Officers, execute Data Processing Agreements, conduct Privacy Impact Assessments, certify compliance with any law or standard, or replace organizational policy, legal counsel, staff training, or incident response processes.
>
> Compliance with applicable laws — including but not limited to PIPEDA, Quebec Law 25, GDPR, CCPA/CPRA, CASL, and applicable AI regulations — is the responsibility of your organization and its qualified advisors. Outputs from this toolkit are technical findings, not legal determinations. Always engage qualified legal counsel for compliance decisions.

---

## What this catalog is

A machine-readable library of regulatory controls in [NIST OSCAL 1.0.2](https://pages.nist.gov/OSCAL/) format, organized by jurisdiction. It is the data layer that powers the `compliance-assess` scanner and `compliance-enforce` sidecar.

Each control entry includes:
- A structured identifier (`<short-code>-<num>`, e.g., `CA-PIPEDA-001`)
- A prose statement of the regulatory obligation
- Detection-rule references (semgrep patterns where applicable)
- Enforcement hook specifications for the sidecar
- Source citations with section and article references

Jurisdiction profiles compose controls across multiple regulations (e.g., a Canadian SaaS serving Ontario users needs PIPEDA + CASL; Quebec adds Law 25 on top).

## What this catalog is NOT

- Not a legal interpretation of any regulation.
- Not complete or exhaustive — catalog coverage is partial and evolves quarterly.
- Not self-updating — regulatory changes require human review and a catalog release.
- Not a substitute for legal counsel or a qualified compliance advisor.

---

## Directory structure

```
compliance-catalog/
├── regulations/          # Per-regulation OSCAL control files (flat layout)
│   ├── pipeda.yaml             # CA federal — PIPEDA
│   ├── quebec-law-25.yaml      # CA-QC — Law 25 (Bill 64)
│   ├── pipa-ab.yaml            # CA-AB — PIPA (Alberta)
│   ├── pipa-bc.yaml            # CA-BC — PIPA (BC)
│   ├── casl.yaml               # CA federal — anti-spam
│   ├── gdpr.yaml               # EU — GDPR
│   ├── ccpa-cpra.yaml          # US-CA — CCPA / CPRA
│   ├── nyc-ll144.yaml          # US-NY-NYC — Local Law 144 (employment)
│   ├── colorado-ai-act.yaml    # US-CO — Colorado AI Act
│   ├── cppa-placeholder.yaml   # CA — not yet in force (Bill C-27)
│   └── aida-placeholder.yaml   # CA — not yet in force (Bill C-27 Part 3)
├── profiles/             # Jurisdiction and use-case compositions
│   ├── region/                 # ca-on, ca-qc, ca-ab, ca-bc, us-ca, us-co, us-ny, eu-generic
│   └── use-case/               # saas-canada-b2c, saas-eu-b2b, ai-product-us
├── detection-rules/      # Detection rule structure (rules themselves come in Phase 1)
│   ├── semgrep/                # Static analysis rule conventions
│   ├── otel-queries/           # Runtime probe conventions
│   ├── questionnaire/          # Self-attestation fragments for non-detectable controls
│   └── mapping.yaml            # Control → detection-rule join schema
└── docs/                 # Authoring guides and FAQ
    ├── authoring-controls.md
    ├── regulation-sources.md
    └── faq.md
```

**Phase 4 expansion** (target: late 2026) adds 6+ jurisdictions including EU AI Act, additional US state privacy laws (VA, CT, UT, TX, CO, OR), Brazil LGPD, UK GDPR, and Canadian provincial health laws (PHIPA, PHIA, HIPA). See `docs/phases/phase-4-catalog-v1.md` for the full v1 scope.

---

## How to use

> Authoring and consumption guides are published at `docs/authoring-controls.md` once Phase 1 ships.

Until then:

1. Browse `regulations/` for raw OSCAL control files.
2. Validate any local edits with `trestle validate` (see `pyproject.toml` for the dev setup).
3. Compose a jurisdiction profile by referencing the relevant files in `profiles/region/`.

---

## Update cadence

The catalog is updated on the **first Tuesday of each calendar quarter** (March, June, September, December). Each release tag follows `catalog-vYYYY.QN` (e.g., `catalog-v2026.Q3`). Out-of-cycle patches are issued for corrections to existing controls within 14 days of a confirmed error report.

---

## License

This catalog is licensed under [CC-BY-4.0](LICENSE). You may copy, adapt, and redistribute the catalog contents with attribution to **Arkoinc Inc.** Attribution format: `Based on compliance-catalog by Arkoinc Inc. (https://github.com/arkoinc-ca/compliance-catalog), CC-BY-4.0`.

Client libraries and tooling that consume this catalog may carry different licenses — see the respective repositories.

<!-- written-by: builder-sonnet | model: sonnet -->
