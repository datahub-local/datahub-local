---
name: site-maintenance
description: Shared foundation and umbrella for maintaining the DataHub.local showcase site. Use when the user asks to maintain, refresh, or audit the whole site, or to keep the portfolio content, platform facts (nodes, hardware, topology), and service versions true to GitHub and the live cluster. Also use when the user says "maintain site", "maintain the showcase", or runs /maintain-site.
allowed-tools: Bash(uv:*), Bash(gh:*), Bash(git:*), Bash(kubectl:*), Bash(helm:*)
license: Apache-2.0
compatibility: Requires gh, git, kubectl, helm, and uv with PyYAML (from the project's mkdocs dependencies).
metadata:
  author: datahub-local
  version: "1.0"
---

# Site maintenance

Keep the whole site true to its sources. This skill is the **umbrella**: it owns
the shared scripts and the contract, and delegates each domain to its own skill.

## The rule

**Code gathers; the model writes.** Every fact compared against the site must
come from `scripts/gather.py` or `scripts/check.py` output — never from memory,
never from prose on another page. If the scripts did not fetch it, it is not
evidence.

## Domains

| Domain   | Skill                      | Evidence                                             |
| -------- | -------------------------- | ---------------------------------------------------- |
| content  | `site-content-maintainer`  | GitHub organizations + the site tree                 |
| platform | `platform-maintainer`      | `inventory.yml` and the live cluster (nodes, ns)     |
| services | `service-maintainer`       | `values/_version.yaml` and the live cluster          |

## Running a pass

Run from the site repository root. The scripts are read-only; only `publish.py`
writes, and only to `docs/` and `mkdocs.yml`.

```bash
S=.opencode/skills/site-maintenance/scripts
uv run python $S/check.py --domain content     # findings as JSON
uv run python $S/check.py --domain platform
uv run python $S/check.py --domain services
uv run python $S/selftest.py                   # safety + synthetic-drift tests
```

`check.py --domain all` runs every domain. `gather.py --domain <d>` prints the
raw fact bundle when a finding needs its source.

For each pending finding, edit the smallest page change that makes the site
match the verified value, then publish:

```bash
uv run python $S/publish.py --domain <d> --dry-run     # show what would change
uv run python $S/publish.py --domain <d> --title "chore(<d>): <what>" \
  --summary-file /tmp/summary.md                        # branch + commit + PR
```

`publish.py` builds with `mkdocs build --strict` and blocks the PR on failure.
It never force-pushes, never commits to the default branch, never merges, and
never writes outside `docs/` and `mkdocs.yml`. Re-running a domain on the same
day updates its existing PR instead of opening another.

## Contract

- **Cite a source** for every change: the finding's `source`, plus the value.
- **Never invent** a figure, link, node, service, or project. Leave the content
  unchanged and report the gap when a value cannot be verified.
- **Record vs cluster**: when `inventory.yml` or `_version.yaml` disagrees with
  the cluster, report the mismatch in the PR summary; the site follows the
  cluster only where the two agree. Edit only this repository.
- **Privacy**: never publish real personal data (shopping invoices, bank rows).
- **No-op is success**: a domain with no findings opens nothing and says so.
- **Non-interactive safe**: no prompts; every choice is a parameter.

## Reasoning lives in the change, not here

Why the domains are split, why delivery is PR-only, and the record-vs-cluster
rule are recorded in `openspec/changes/showcase-maintainer/`. Do not restate
them in a prompt or a page.
