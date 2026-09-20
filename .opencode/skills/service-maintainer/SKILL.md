---
name: service-maintainer
description: Maintain the service pages — which services exist and their versions, including Helm chart and container image versions — by cross-checking the core versions file against the live cluster. Use when the user says "maintain services", "refresh versions", "check the service stack", or runs /maintain-services.
allowed-tools: Bash(uv:*), Bash(gh:*), Bash(git:*), Bash(kubectl:*), Bash(helm:*)
license: Apache-2.0
compatibility: Requires kubectl and helm access to the cluster, the core versions file, git, and uv with PyYAML.
metadata:
  author: datahub-local
  version: "1.0"
---

# Service maintainer

Keep the service pages true to the deployed stack. See `site-maintenance` for the
shared contract.

## Required sources

- `datahub-local-core/values/_version.yaml` — the config-of-record for container
  image and Helm chart versions. Override with
  `SITE_MAINTAINER_CORE_VERSIONS`.
- The live cluster via `helm list` and `kubectl` — the deployed versions.

## Steps

1. Run the service checks:

   ```bash
   S=.opencode/skills/site-maintenance/scripts
   uv run python $S/check.py --domain services
   ```

2. For each finding, edit the smallest page change:
   - `chart-version-mismatch` / `image-version-mismatch`: correct the version the
     site states, and report the record-vs-cluster mismatch in the summary when
     the two disagree. Never choose a side silently.
   - A service deployed but unmentioned, or mentioned but gone: add or remove the
     entry in the relevant `docs/services/*.md` page.
   - `record-unavailable`: state which facts could not be cross-checked.

3. Publish:

   ```bash
   uv run python $S/publish.py --domain services --dry-run
   uv run python $S/publish.py --domain services --title "chore(services): <what>" \
     --summary-file /tmp/services-summary.md
   ```

## Rules

- Edit only this site repository; drift in core is reported, never fixed here.
- A version with no source is left unchanged and recorded as a gap.
