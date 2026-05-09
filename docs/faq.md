# Frequently Asked Questions

## What is the compliance-catalog?

The compliance-catalog is an open-source, machine-readable library of regulatory obligations drawn from privacy, AI governance, and anti-spam laws covering Canada (federal and provincial), the United States (California, New York City, Colorado), and the European Union. Each obligation is encoded as an OSCAL-shaped control with a canonical ID, a plain-English statement of the requirement, and a mapping to one or more detection methods (static code analysis, runtime probes, or human questionnaire).

The catalog is a technical artifact that powers the `compliance-assess` command-line assessor and the `compliance-browser` web interface. It is not a compliance certification and it is not legal advice.

---

## Is this legal advice?

**No.** The compliance-catalog and all tooling in this repository are provided for informational and technical purposes only. They do not constitute legal advice, legal opinion, or a compliance determination. Regulatory compliance is a legal and organizational determination made by qualified professionals — legal counsel, auditors, and regulators.

The catalog may help engineering teams identify code-level gaps; it cannot tell you whether your organization is compliant. For the full scope boundary, see the DISCLAIMER section in the root `README.md`.

---

## How do I use it?

The catalog is consumed by the `compliance-assess` CLI. The general workflow is:

1. Select a profile that matches your jurisdiction and use case (e.g., `profiles/use-case/saas-canada-b2c.yaml`).
2. Run `compliance-assess scan --profile <path>` against your codebase.
3. Review the gap report; each finding references the control ID and the detection rule that fired.
4. Address gaps in code (semgrep findings) or organizational process (questionnaire findings).

Full CLI documentation is in the `compliance-assess` repository under `docs/`.

---

## How often is it updated?

The catalog follows a **quarterly cadence**: first Tuesday of January, April, July, and October. Emergency updates for regulations with near-term effective dates may be issued outside that schedule as `hotfix/` branches.

To stay current with source regulations, subscribe to regulator bulletins:

- OPC (Canada federal): https://www.priv.gc.ca/en/about-the-opc/what-we-do/newsletters/
- CAI (Quebec): https://www.cai.gouv.qc.ca/en/
- ICO (UK, informational): https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/
- CNIL (France, informational): https://www.cnil.fr/en/cnil-direct
- CPPA (California): https://cppa.ca.gov/newsroom/

See `docs/human-action-checklist.md` H-09 for the quarterly review checklist.

---

## How do I add a control?

Follow `docs/authoring-controls.md`. The short version: add a YAML entry to the relevant `regulations/<file>.yaml`, register it in `detection-rules/mapping.yaml`, run the validator and test suite, and open a PR. SME review of the obligation text is required before a control can move from `draft` to `final` status.

---

## My jurisdiction is not covered. What now?

Open an issue on the `compliance-catalog` repository describing the regulation, jurisdiction, and effective date. Version 0 covers:

- Canada: PIPEDA (federal), Quebec Law 25, PIPA-AB, PIPA-BC, CASL
- United States: CCPA/CPRA (California), NYC LL.144, Colorado AI Act
- European Union: GDPR (generic member state)

The following are intentionally deferred to later phases:

| Regulation | Reason for deferral |
|---|---|
| LGPD (Brazil) | Phase 4 — international expansion |
| UK GDPR / UK DPA 2018 | Phase 4 — post-Brexit divergence still settling |
| Israel Protection of Privacy Law | Phase 4 |
| HIPAA (US health) | Phase 4 — sector-specific; large control surface |
| Bill C-27 (CPPA + AIDA) | Awaiting Royal Assent |

---

## Why no full OSCAL JSON envelope? Why not use trestle?

Our regulation YAMLs use a simplified OSCAL-shaped structure (top-level `catalog` key with `groups` and `controls`) rather than the full OSCAL 1.0.2 JSON envelope expected by `compliance-trestle`'s validator. This decision was made on 2026-05-09 and recorded in `docs/phases/phase-1-catalog-v0.md` Decision Log.

The short reason: the full OSCAL envelope adds significant boilerplate (backmatter, metadata with parties and roles, link structures) that provides no value for v0's use case of powering a gap-finding assessor. Full OSCAL conformance is scoped to Phase 4, at which point trestle's toolchain can be adopted. Until then, our custom Pydantic v2 validator at `scripts/validate_catalog.py` enforces structural correctness, control ID format, UUID v4 validity, and minimum control counts.

---

## How is severity assigned?

Severity is assigned by the control author and reviewed by the SME during the `draft` to `final` transition:

| Severity | Criteria |
|---|---|
| `high` | Direct statutory obligation with an enforcement deadline, financial penalty trigger, or mandatory breach notification requirement |
| `medium` | Derived obligation, supporting record-keeping, or obligation that conditions a higher-severity right (e.g., maintaining the RoPA that enables a Subject Access Request) |
| `low` | Procedural obligation, housekeeping, or documentation that supports the above categories without independent enforcement risk |

If you disagree with a severity assignment, open a PR with a rationale referencing the specific penalty or enforcement provision.

---

## Where do I file a security issue with catalog content?

Do not open a public GitHub issue for security-sensitive findings (e.g., a control that contains a real person's data, or a detection rule that inadvertently surfaces secrets). Instead, follow the responsible disclosure process in the root `SECURITY.md`.

<!-- written-by: builder-sonnet | model: sonnet -->
