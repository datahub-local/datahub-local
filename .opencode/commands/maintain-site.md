---
description: "Maintain the whole site (content, platform, services) against GitHub and the live cluster"
---

Run a full maintenance pass over the site and propose reviewable pull requests.

Use the `site-maintenance` skill for the shared contract, then run each domain
skill in turn: `site-content-maintainer`, `platform-maintainer`, and
`service-maintainer`.

Steps:

1. From the site repository root, run `uv run python
   .opencode/skills/site-maintenance/scripts/check.py --domain all`.
2. For each domain with findings, load that domain's skill and follow it.
3. Report a per-domain result: current, or the PR opened/updated.
4. A domain with no findings opens nothing and is reported as current.

Optional arguments: `--dry-run` to check without publishing; a domain name to
limit the pass. Never merge, never push the default branch, never edit any
repository other than this site.
