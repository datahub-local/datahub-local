# Proposal

## Why

The site makes two kinds of claims, and both drift. **Content claims** —
repositories, links, project status — change as the organizations change.
**Platform claims** — machines, hardware, services, versions, topology — change
as the cluster changes. Today nothing notices, so the site is only true on the
day it was written, and keeping it honest depends on a human remembering to
sweep every page. A recurring, domain-split maintainer that compares the site
against GitHub and against the running cluster, then opens reviewable PRs,
removes that chore.

## What Changes

- Replace the single maintainer with **domain-scoped skills** that share one
  deterministic gatherer: a **content** maintainer, a **platform** maintainer, a
  **service** maintainer, and an umbrella run that executes all three.
- **Content domain**: catalogue drift (new/renamed/archived repos), link and
  asset health, factual freshness, roadmap and project status, image refresh, and
  consistency checks.
- **Platform domain**: cluster nodes, hardware, roles, and namespace topology,
  cross-checked between the config-of-record and the live cluster.
- **Service domain**: service inventory, component versions, and chart versions,
  cross-checked between the config-of-record and the live cluster.
- Keep gathering **deterministic in code**, so the model judges over fetched
  facts rather than recollecting them — the platform's "code gathers; the model
  writes" discipline.
- **Cross-check, do not pick a side**: when the config-of-record and the live
  cluster disagree, the mismatch is itself a finding. The maintainer edits only
  this site repository and *reports* record-versus-cluster drift rather than
  editing the repositories that hold the record.
- Deliver every change as a **pull request**; the maintainer never pushes to the
  default branch and never merges. Each domain proposes its own PR.
- Keep every skill **scheduler-agnostic**, so a Sympozium persona can run any
  domain later without redesign. Scheduling in Sympozium is a **follow-up**.

## Capabilities

### New Capabilities

- `showcase-maintenance`: the whole-site maintenance contract — the content,
  platform, and service domains; deterministic gathering; the record-versus-
  cluster cross-check; the safety rules (PR only, no personal data, verifiable
  facts); and the expected output.

### Modified Capabilities

<!-- No requirement changes here. `showcase-microsite` was archived; its
     capability now lives at `openspec/specs/project-showcase/spec.md`. -->

## Impact

- New skills under `.opencode/skills/` (one umbrella plus three domain skills)
  and matching commands under `.opencode/commands/`.
- A shared gatherer and its dependencies: `gh` for GitHub facts, `kubectl` and
  `helm` for cluster facts.
- Builds on the archived `showcase-microsite` change for the catalogue and page
  structure (now `openspec/specs/project-showcase/spec.md`) and on the
  `showcase-image-generator` skill for the asset layout and generation path.
- Requires an authenticated `gh` identity, and a kubeconfig with read access
  wherever the platform and service domains run.
- Reads `datahub-local-bootstrap/inventory.yml` and
  `datahub-local-core/values/_version.yaml` as the config-of-record; it never
  writes to those repositories.
- No runtime services are affected, and the site build is untouched.
