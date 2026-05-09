# Contributor Ladder

<!-- written-by: builder-sonnet | model: sonnet -->

The compliance-catalog project uses three levels of community involvement. Each level has clear criteria, duties, and an off-boarding path. There are no minimum tenure requirements to _start_ — advancement is based on demonstrated contribution quality and consistency.

---

## Level 1: Contributor

**You are already a Contributor if you have merged at least one PR.**

### Criteria to reach this level

- Merged one or more PRs (control fix, documentation, or new tier-2 regulation).
- Signed all commits with the DCO (`Signed-off-by` trailer).
- Followed the source citation policy.

### Expected duties

- Maintain any tier-2 regulations you have claimed (respond to `regulatory-delta` issues within 14 days during each quarterly cycle).
- Participate in RFC discussions for regulations in your area of expertise.
- Be kind and constructive in code review comments.

### Tenure expectations

No minimum tenure. A single quality contribution qualifies you. Your name appears in `CONTRIBUTORS.md` after your first merge.

### Off-boarding

If you no longer maintain a claimed regulation, comment on the tracking issue to relinquish ownership. A maintainer will update `CODEOWNERS` and re-open the regulation for a new claimant. No hard feelings — life happens.

---

## Level 2: Reviewer

**Reviewers are trusted contributors who regularly review PRs and guide new contributors.**

### Criteria to advance from Contributor

- Five or more merged PRs across at least two quarterly cycles.
- Track record of substantive, constructive PR reviews (comments that improve quality, not just approve).
- Familiarity with at least one tier-1 regulation in depth.
- Nominated by an existing Reviewer or Maintainer; confirmed by maintainer consensus (no objections in 7 days).

### Expected duties

- Review 2–4 open PRs per month; aim to review within 5 business days of assignment.
- Help triage `regulatory-delta` issues each quarter.
- Mentor new Contributors: answer questions in GitHub Discussions, point to docs.
- Flag potential SME review needs to Maintainers.

### Tenure expectations

No fixed tenure requirement. Inactivity for 6 consecutive months (no reviews, no participation) results in a courtesy ping from a Maintainer. If there is no response in 14 days, Reviewer status is moved to Emeritus (see off-boarding below).

### Off-boarding

- **Voluntary:** Comment on the team issue thread: "I am stepping back from Reviewer duties." Maintainer updates the GitHub team.
- **Involuntary (inactivity):** After the 14-day ping with no response, status moves to Emeritus. Your past contributions are preserved and credited.
- **Conduct:** Code of Conduct violations may result in immediate removal after maintainer review.

---

## Level 3: Maintainer

**Maintainers are accountable stewards of the catalog's quality, regulatory fidelity, and community health.**

### Criteria to advance from Reviewer

- Consistent participation over at least two full quarterly cycles as a Reviewer.
- Demonstrated judgment on regulatory fidelity (not just technical correctness).
- Willingness to be listed as a named maintainer (public accountability).
- Nominated by an existing Maintainer; accepted by unanimous consent of current Maintainers.

### Expected duties

- Drive or delegate the quarterly update process (see [`quarterly-update-process.md`](quarterly-update-process.md)).
- Merge PRs after required approvals; cut release tags.
- Coordinate SME reviews for tier-1 regulation changes.
- Keep the `CODEOWNERS` file accurate.
- Monitor and triage issues weekly.
- Represent the catalog in RFC decisions.
- Onboard new Reviewers.

### Tenure expectations

No mandatory tenure. Maintainers are expected to remain active. If a Maintainer is unavailable for more than 60 days without advance notice, the remaining Maintainers may move the role to Emeritus and open a call for a replacement.

### Off-boarding

- **Voluntary:** Give at least 30 days notice if possible. Transition in-flight work to another Maintainer. GitHub team and `CODEOWNERS` updated on departure date.
- **Involuntary (inactivity):** After 60 days of unreachability, status moves to Emeritus automatically.
- **Conduct:** Code of Conduct violations result in immediate removal pending a maintainer review.

---

## Emeritus

Contributors, Reviewers, and Maintainers who step back move to **Emeritus** status. Emeritus members:

- Retain credit in `CONTRIBUTORS.md` and release notes.
- Lose write/merge access.
- Are welcome to return to active status at any level by resuming contributions; no special re-application required, though Reviewer and Maintainer re-advancement follow the same criteria.

---

## Recognition

All contributors at every level are credited in `CONTRIBUTORS.md` and in the GitHub Release notes for quarters in which they contributed. We do not distinguish between "big" and "small" contributions in credits — a citation fix matters as much as a new regulation.
