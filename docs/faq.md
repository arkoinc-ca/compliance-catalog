<!-- written-by: builder-sonnet | model: sonnet -->

# Frequently Asked Questions

## What is a control?

A control is a machine-readable statement of an obligation derived from a regulation. Each control has a unique ID (e.g., `GDPR-5-1-a`), a title, a plain-text statement of the requirement, and references to detection rules or questionnaire questions that let the assessor determine whether the obligation is met.

Controls are stored in OSCAL catalog YAML files under `regulations/`. They are not legal advice — they are structured summaries intended to help engineering teams identify code-level gaps.

## Can I use this catalog for compliance certification?

**No.** This catalog is a gap-finding aid, not a certification path. Compliance certification is a legal and organizational determination made by qualified humans — legal counsel, auditors, and regulators. The catalog can help you identify what to fix; it cannot certify that you have fixed it.

See the DISCLAIMER section in the root `README.md` for the full scope boundary.

## Can I use the NYC LL.144 section to self-certify my bias audit?

**No.** NYC Local Law 144 (DCWP §5-300) explicitly requires an **independent external auditor**. The toolkit can help you prepare evidence (bias metrics, model cards, test results) to present to an auditor, but self-audit is not permitted under the law.

## How often does the catalog update?

The catalog is updated on a **quarterly cadence**: the first Tuesday of each quarter (January, April, July, October). Emergency updates for regulatory changes that are effective sooner may be issued outside that schedule; they are tagged as `hotfix/` branches.

## How do I add a regulation?

1. Open an issue describing the regulation, jurisdiction, and effective date.
2. A maintainer will assign it to a catalog milestone and create a skeleton file.
3. Follow the authoring guide in `docs/authoring-controls.md` to add controls.

## How do I add a control to an existing regulation?

Follow `docs/authoring-controls.md`. The short version: add a YAML entry to the relevant `regulations/<file>.yaml`, register it in `detection-rules/mapping.yaml`, run the test suite, and open a PR.

## What does "skeleton" status mean?

A skeleton control has the correct OSCAL structure but the `prose` field contains `"TODO: Author full control statement in Phase 1."`. The ID is reserved and the shape is correct; the text will be filled in by contributors during Phase 1 authoring.

## Where is the full implementation plan?

`docs/compliance-toolkit-implementation-plan.md` at the repository root contains the full architecture, phasing, and regulatory scope decisions.
