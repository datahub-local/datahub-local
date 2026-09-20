---
name: platform-maintainer
description: Maintain the platform facts on the site — cluster nodes, hardware classes, roles, and namespace topology — by cross-checking the bootstrap inventory against the live cluster. Use when the user says "maintain platform", "refresh the architecture page", "check the nodes", or runs /maintain-platform.
allowed-tools: Bash(uv:*), Bash(gh:*), Bash(git:*), Bash(kubectl:*)
license: Apache-2.0
compatibility: Requires kubectl access to the cluster, the bootstrap inventory, git, and uv with PyYAML.
metadata:
  author: datahub-local
  version: "1.0"
---

# Platform maintainer

Keep the architecture and hardware pages true to the cluster. See
`site-maintenance` for the shared contract.

## Required sources

- `datahub-local-bootstrap/inventory.yml` — the config-of-record (hosts, roles,
  GPU flags). Override with `SITE_MAINTAINER_BOOTSTRAP_INVENTORY`.
- The live cluster via `kubectl` — the authoritative state.

A pass **fails loudly** when the cluster is unreachable; it must never report the
page as correct in that case.

## Steps

1. Run the platform checks:

   ```bash
   S=.opencode/skills/site-maintenance/scripts
   uv run python $S/check.py --domain platform
   ```

2. For each finding, edit the smallest page change:
   - `node-missing-from-docs` / `node-removed-from-cluster`: update the node
     table and the topology diagram in `docs/architecture/overview.md`, and the
     hardware list in `docs/cluster_setup/hardware.md`.
   - `node-cpu-drift` / `node-os-drift`: correct the stated attribute to the
     cluster value.
   - `namespace-missing-from-docs` / `namespace-removed-from-cluster`: update
     the namespace table.
   - `record-cluster-mismatch`: do **not** silently choose a side. Report the
     mismatch in the PR summary naming both values; correct the site only where
     the record and the cluster agree.
   - `record-unavailable`: state which facts could not be cross-checked.

3. Publish:

   ```bash
   uv run python $S/publish.py --domain platform --dry-run
   uv run python $S/publish.py --domain platform --title "chore(platform): <what>" \
     --summary-file /tmp/platform-summary.md
   ```

## Rules

- Edit only this site repository. Drift in the inventory or core is reported,
  never fixed here.
- Physical RAM is not compared: node capacity is usable memory after
  reservation, not the module size the page states.
