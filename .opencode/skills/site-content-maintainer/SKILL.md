---
name: site-content-maintainer
description: Maintain the showcase portfolio content — catalogue drift, links and assets, factual freshness, roadmap and project status, image staleness, and consistency — by comparing the site against the GitHub organizations. Use when the user says "maintain content", "refresh the showcase", "check the project cards", or runs /maintain-content.
allowed-tools: Bash(uv:*), Bash(gh:*), Bash(git:*)
license: Apache-2.0
compatibility: Requires gh, git, and uv with PyYAML. No cluster access needed.
metadata:
  author: datahub-local
  version: "1.0"
---

# Content maintainer

Keep the portfolio content true to the repositories. See `site-maintenance` for
the shared contract; this skill is the content domain only.

## Steps

1. Run the content checks from the site root:

   ```bash
   S=.opencode/skills/site-maintenance/scripts
   uv run python $S/check.py --domain content
   ```

2. For each finding, decide from the JSON whether it is real drift or
   deliberate. The finding carries its `source`; use `gather.py --domain content`
   when you need the wider fact bundle. Do not add a repository the scope
   excludes (forks, private, or listed under `repositories.exclude`).

3. Make the smallest edit that fixes it:
   - `broken-link`: fix or remove the reference.
   - `repo-not-catalogued`: add a card, or record why it is excluded.
   - `repo-archived`: mark the card archived.
   - `duplicated-narrative`: keep one source and link to it.
   - `image-maybe-stale`: only if the image no longer represents the project;
     regenerate through the `showcase-images` path. Never regenerate routinely.
   - Freshness: replace an unsupported figure with the verified value, or remove
     it. Never guess.

4. Publish:

   ```bash
   uv run python $S/publish.py --domain content --dry-run
   uv run python $S/publish.py --domain content --title "chore(content): <what>" \
     --summary-file /tmp/content-summary.md
   ```

## Rules

- Personal data never appears on a page or in a PR: describe method, schema, and
  aggregate outcomes only.
- A no-op run publishes nothing and reports the domain as current.
- Never edit `datahub-local-*` repositories from here.
