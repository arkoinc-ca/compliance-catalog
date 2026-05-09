# Quarterly Update Process

<!-- written-by: builder-sonnet | model: sonnet -->

## Cadence

Four times per year, on the **first Monday of February, May, August, and November**.

| Quarter | Cut Date (first Monday) | Feature Freeze Starts |
|---------|-------------------------|-----------------------|
| Q1      | First Monday of February | Two weeks prior       |
| Q2      | First Monday of May      | Two weeks prior       |
| Q3      | First Monday of August   | Two weeks prior       |
| Q4      | First Monday of November | Two weeks prior       |

During the two-week feature-freeze window no new regulations or structural changes merge to `main`. Only bug fixes, validator fixes, and SME-requested corrections are accepted.

## Owner

**Catalog Maintainers** — the group holding the `@arkoinc-ca/catalog-maintainers` GitHub team role. A quorum of one maintainer suffices to drive each quarter; a second maintainer must approve the release PR. Acceptance gate: P4-G03 must be closed before the release tag is cut.

## Steps

### 1. Regulatory Monitoring (rolling, week −8 to −3 before cut)

- Review bulletin subscriptions established in H-09 (OPC, CAI, ICO, CNIL, CPPA).
- Check each regulation's official source page for amendments, new guidance, or enforcement orders.
- File a tracking issue for each discovered delta using the label `regulatory-delta`.

### 2. Triage Delta (week −3 to −2)

- For each `regulatory-delta` issue, assess:
  - **Critical** — misrepresents current law; blocks release if unresolved.
  - **Major** — material gap; target current quarter.
  - **Minor** — editorial or citation; can slip one quarter.
- Assign each issue to a milestone matching the upcoming release tag.
- Close issues that duplicate existing controls or are out of scope.

### 3. Feature Freeze (week −2 to cut)

- Post a freeze notice as a pinned issue: `Quarterly freeze: vX.Y.0+regs-YYYY-MM in effect`.
- Merge only: bug fixes, critical regulatory-delta corrections, SME-requested amendments.
- All other PRs are labelled `post-freeze` and retargeted to the next quarter.

### 4. SME Review

- For each critical or major delta, request written sign-off from the relevant SME (see H-07 for engagement process).
- SME leaves an approval comment on the PR: "Approved: control set accurately reflects [Regulation] as of [Date] — [Name], [Credentials]".
- Do not cut the release tag until all critical-delta PRs have SME approval.

### 5. Release PR

- Open a PR titled `chore: quarterly update vX.Y.0+regs-YYYY-MM`.
- PR body must include:
  - List of regulations changed and nature of change.
  - Links to SME approval comments.
  - Validator CI result (must be green: `uv run python scripts/validate_catalog.py`).
  - Changelog excerpt (append to `CHANGELOG.md` in catalog repo).
- Require two maintainer approvals before merge.

### 6. Release Tag

Cut the tag immediately after PR merge:

```bash
git tag -a "v0.X.0+regs-YYYY-MM" -m "Quarterly catalog update: <short description>"
git push origin "v0.X.0+regs-YYYY-MM"
```

Tag format: `v0.X.0+regs-YYYY-MM` where `YYYY-MM` is the ISO month of the cut date.

GitHub Actions release CI triggers on the tag push. Verify the workflow completes green before announcing.

### 7. Announcement

Post a brief release announcement in the project's GitHub Discussions (Announcements category) linking to the GitHub Release page.

---

## Automated Reminder

A GitHub Actions workflow (`.github/workflows/quarterly-update-reminder.yaml` in the meta-repo) runs on the 1st of each trigger month (December, March, June, September — 8 weeks prior to the target cut months of February, May, August, November) at 09:00 UTC and opens a tracking issue in the meta-repo. Maintainers should triage that issue within 48 hours to kick off the monitoring step.
