# Contributing to compliance-catalog

<!-- written-by: builder-sonnet | model: sonnet -->

Thank you for helping improve this catalog. This guide covers everything you need to propose a regulation, author controls, and get your contribution merged.

## Code of Conduct

All participants must follow the project [Code of Conduct](../../CODE_OF_CONDUCT.md). Be respectful, assume good faith, and keep discussions on-topic.

## Ways to Contribute

| Contribution type | Where to start |
|-------------------|----------------|
| Propose a new regulation | File an RFC (see RFC process below) |
| Fix a control error | Open a PR with a `fix:` commit |
| Improve a citation | Open a PR; primary source required |
| Report a regulatory gap | Open an issue with label `regulatory-delta` |
| Improve documentation | Open a PR targeting `docs/` |

## Proposing a New Regulation

Before writing a single YAML line, file an RFC. This prevents duplicate work and ensures the scope is agreed upon before authoring begins.

1. Open a new issue using the **RFC** issue template (`.github/ISSUE_TEMPLATE/rfc.yaml`).
2. Fill in all required fields: motivation, scope, impact, alternatives, risks, and sponsor.
3. The comment period is **10 calendar days**. Maintainers may extend it for complex proposals.
4. After the comment period, a maintainer records the decision (accept / reject / defer) as a comment and closes the RFC issue.
5. Accepted RFCs move to the authoring stage below.

Full RFC process: [`docs/rfc-process.md`](docs/rfc-process.md).

## Authoring Controls

See [`docs/authoring-controls.md`](docs/authoring-controls.md) for the full quickstart. Key points:

- Each control is a YAML file under `regulations/<jurisdiction>/`.
- Run `uv run python scripts/validate_catalog.py` locally before pushing; CI will reject invalid files.
- Each control needs a `source` field pointing to the **primary government source** (official gazette, legislation portal, or regulator guidance page). Secondary sources (law firm summaries, Wikipedia) are not accepted for tier-1 controls.
- Follow the control ID convention: `<REGION>-<ABBREV>-<SEQ>` (e.g., `CA-QC-LAW25-001`).

## Tier Policy

| Tier | Meaning | Who maintains | Source requirement |
|------|---------|---------------|--------------------|
| **Tier 1 (maintained)** | Core regulations actively maintained by the Catalog Maintainers team | `@arkoinc-ca/catalog-maintainers` | Primary government source required |
| **Tier 2 (community)** | Regulations contributed and maintained by the community | Contributor who claimed it | Primary government source strongly recommended |

To claim a regulation (commit to maintaining it for at least two quarterly cycles), comment on the relevant RFC or tracking issue with "I am claiming ownership of [Regulation]." A maintainer will add you to the `CODEOWNERS` entry for that regulation file.

## Severity Guidance

When authoring or filing a delta issue, classify the control using the `severity` field:

| Severity | When to use |
|----------|-------------|
| `critical` | Directly required by statute; non-compliance triggers enforcement action |
| `high` | Strongly implied by guidance or regulators' stated enforcement priorities |
| `medium` | Best practice aligned with regulation intent; enforcement is possible but less direct |
| `low` | Informational; supports audit evidence but not independently enforceable |

## Source Citation Policy

- Tier-1 controls **must** cite a primary government source in the `source` field.
- Acceptable: official legislation portals, government gazette URLs, ICO/OPC/CNIL/CAI guidance pages.
- Not acceptable: law firm blog posts, Wikipedia, news articles, or secondary summaries.
- Include the access date in the `source_accessed` field (ISO 8601, e.g., `2026-05-09`).

## Signing Your Work (DCO)

This project uses the [Developer Certificate of Origin (DCO)](https://developercertificate.org/). Add a `Signed-off-by` trailer to every commit:

```
git commit -s -m "fix: correct source URL for CA-QC-LAW25-003"
```

The `-s` flag appends `Signed-off-by: Your Name <email@example.com>` automatically. PRs without DCO sign-off will not be merged.

## Pull Request Checklist

Before opening a PR, confirm:

- [ ] `uv run python scripts/validate_catalog.py` exits 0
- [ ] Primary government source cited for every new or modified control
- [ ] `Signed-off-by` trailer on each commit
- [ ] PR title follows conventional commit format (`feat:`, `fix:`, `chore:`, `docs:`)
- [ ] RFC accepted (for new regulations)
- [ ] SME review requested if the control set covers a tier-1 regulation

## Getting Help

Open a [GitHub Discussion](https://github.com/arkoinc-ca/compliance-catalog/discussions) in the **Q&A** category. Maintainers aim to respond within 5 business days.

## Contributor Ladder

Want to grow from contributor to reviewer to maintainer? See [`docs/contributor-ladder.md`](docs/contributor-ladder.md).
