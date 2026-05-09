# RFC Process

<!-- written-by: builder-sonnet | model: sonnet -->

An RFC (Request for Comments) is required before proposing a new regulation catalog or any structural change to the catalog schema, directory layout, or validation rules. This keeps design discussions visible and ensures maintainers and the community have input before significant work begins.

## When to File an RFC vs. a PR

| Situation | Use |
|-----------|-----|
| New regulation (tier-1 or tier-2) | RFC first, then PR |
| Structural change (schema, directory layout, control ID convention) | RFC first, then PR |
| Bug fix in an existing control | PR directly |
| Citation correction | PR directly |
| Documentation improvement | PR directly |
| New detection-rule template for an existing regulation | PR directly (mention in PR body if non-trivial) |

If you are unsure, open a GitHub Discussion in the **Q&A** category and ask. A maintainer will advise.

## RFC Template Fields

When opening an RFC, use the **RFC** issue template (`.github/ISSUE_TEMPLATE/rfc.yaml`). Fill in every field:

| Field | Purpose |
|-------|---------|
| **Motivation** | Why is this regulation or change needed? What problem does it solve for users of the toolkit? |
| **Scope** | What regulations, jurisdictions, or schema elements are affected? What is explicitly out of scope? |
| **Impact** | How does this affect existing controls, CI, downstream consumers (compliance-assess), or SME review obligations? |
| **Alternatives** | What other approaches were considered and why were they rejected? |
| **Risks** | Legal accuracy risks, maintenance burden, coverage gaps, or license compatibility issues. |
| **Sponsor** | GitHub handle of the person who will drive authoring if the RFC is accepted. Must be a current Contributor or above. |

Incomplete RFCs are closed with a request to fill in missing fields.

## Comment Period

The comment period is **10 calendar days** from the date the RFC issue is opened.

- Community members and maintainers post questions, concerns, and suggestions as issue comments.
- The RFC author responds to substantive questions within the comment period.
- Maintainers may extend the comment period by 7 additional days for complex proposals by posting a comment on the issue.
- Maintainers may close an RFC early (before 10 days) only if it is clearly out of scope or a duplicate.

## Decision Process

After the comment period closes, a Maintainer records the decision as a comment on the RFC issue:

- **Accept** — The RFC is approved as written or with noted amendments. The sponsor may proceed to authoring. The RFC issue is labelled `rfc-accepted` and remains open until the implementing PR is merged.
- **Reject** — The RFC is declined with an explanation. The issue is labelled `rfc-rejected` and closed.
- **Defer** — The RFC has merit but is not prioritized for the current quarter. The issue is labelled `rfc-deferred` and remains open for the next quarterly planning cycle.

Decisions require consensus among active Maintainers. If Maintainers disagree, the project lead (see `CODEOWNERS`) has the casting vote.

## Archive Location

Accepted RFCs remain as closed GitHub issues with the label `rfc-accepted`. The implementing PR's description must reference the RFC issue number (`Closes #NNN`). This creates a permanent link from the merged regulation back to the design discussion.

Rejected and deferred RFCs are also retained as closed issues for historical reference. Do not delete them.

## Fast-Track for Minor Structural Changes

Minor structural changes (e.g., adding an optional field to the schema that is backward-compatible and does not affect existing controls) may be proposed directly in a PR with a detailed PR description in place of a formal RFC. A Maintainer decides at triage whether to accept the PR directly or require a full RFC. When in doubt, file the RFC — it costs less than a rejected PR.
