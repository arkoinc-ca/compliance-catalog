<!-- written-by: builder-sonnet | model: sonnet -->

# Self-Attestation Questionnaire Fragments

This directory holds structured questionnaire fragments for controls that cannot be detected automatically through static analysis (Semgrep) or runtime observation (OTel). These are process and policy obligations that require human attestation.

## Why Questionnaires

Many privacy and AI-governance obligations are organizational in nature and cannot be verified by scanning code or querying metrics. Examples:

- Has the organization designated a Privacy Officer? (PIPEDA Principle 1, QC Law 25)
- Is there a documented breach-notification procedure? (GDPR Art. 33, PIPEDA breach regulations)
- Has an external bias audit been commissioned for the AEDT? (NYC LL.144 — external auditor required by law)
- Does the organization maintain an AI impact assessment on file? (Colorado AI Act §6-1-1702)

These controls are marked as `detection-method: questionnaire` in `mapping.yaml`.

## Fragment Structure

Each file in this directory is a YAML list of question fragments. The assessor CLI (Phase 2) will load and prompt these interactively or via a web form (Phase 3).

```yaml
questionnaire:
  id: "governance-privacy-officer"
  title: "Privacy Officer Designation"
  controls:
    - "PIPEDA-1"
    - "QC-LAW25-1"
  questions:
    - id: "q-priv-officer-designated"
      text: "Has the organization designated an individual responsible for compliance with PIPEDA and applicable provincial privacy legislation?"
      type: boolean
      required: true
      evidence-prompt: "Provide name, title, and contact email of the designated Privacy Officer."

    - id: "q-priv-officer-accessible"
      text: "Is the Privacy Officer's contact information publicly accessible on the organization's website or in its privacy policy?"
      type: boolean
      required: true
      evidence-prompt: "Provide the URL where this information is published."
```

## File Naming

Files are named by the governance domain they cover.

| File | Domain |
|------|--------|
| `governance-privacy-officer.yaml` | Privacy Officer designation and accountability |
| `governance-breach-procedure.yaml` | Breach detection, containment, and notification |
| `ai-governance-impact-assessment.yaml` | AI impact assessment and risk documentation |
| `ai-bias-audit.yaml` | External bias audit for automated decision tools |
| `dsr-process.yaml` | Data subject request intake and fulfillment |
| `retention-policy.yaml` | Retention schedule documentation |

## Adding a Fragment

1. Identify the control(s) from `regulations/<file>.yaml` that require attestation.
2. Create or extend a domain file under `detection-rules/questionnaire/`.
3. Register the mapping in `detection-rules/mapping.yaml` with `detection-method: questionnaire`.
4. Keep questions binary (yes/no) or short-text; avoid composite questions.

Questionnaire authoring is scheduled alongside the assessor CLI in Phase 2.
