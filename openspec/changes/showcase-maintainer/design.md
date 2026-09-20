# Design

## Context

See `proposal.md` — Why. Current state that shapes the approach:

- opencode discovers **skills** at `.opencode/skills/<name>/SKILL.md` and
  **commands** at `.opencode/commands/<name>.md`; the existing `openspec-*`
  skills are the working example, and `.opencode/package.json` is gitignored.
- The site makes claims with two different evidence sources:
  - **content** — GitHub repositories (`datahub-local/*`, `alvsanand/*`) and the
    site tree, reachable with `gh`.
  - **platform / services** — the config-of-record and the live cluster:
    `datahub-local-bootstrap/inventory.yml` (hosts, roles, GPU flags),
    `datahub-local-core/values/_version.yaml` (container image and Helm chart
    versions), and the running cluster (`kubectl get nodes`, namespaces, deployed
    images and chart versions via `helm`).
- The pages that carry those claims: `architecture/overview.md` (node table,
  namespace table), `cluster_setup/hardware.md` (hardware components), and the
  `services/*` pages.
- `showcase-microsite` and `showcase-images` define the content structure and
  assets; both are still in planning, so this change consumes their outputs.
- Precedent: the Sympozium `homelab-reviewer` ensemble runs a scheduled GitHub
  persona that may only comment. This design stays read-mostly and delivers a
  branch + PR instead.
- The platform's standing rule is **"code gathers; the model writes"**.

## Goals / Non-Goals

**Goals:**

- Keep both content and platform facts true, with a separately runnable pass per
  domain and a combined run.
- Deterministic, verifiable inputs from GitHub, the record, and the cluster.
- Surface record-versus-cluster disagreements instead of hiding them.
- Safe by construction: PR only, site repo only, never the default branch, never
  a merge.
- Runnable manually now, by a scheduler later, with no definition change.

**Non-Goals:**

- Scheduling inside Sympozium (a follow-up change).
- Editing `datahub-local-bootstrap`, `datahub-local-core`, or any repository
  other than this site; drift found there is reported, not fixed.
- Judging or merging pull requests (that is `renovate-reviewer`'s job).
- Inventing new site content beyond correcting what exists.
- A general-purpose GitHub or Kubernetes agent.

## Decisions

### D1 — Three domain skills plus an umbrella, sharing one gatherer

```
  .opencode/skills/site-maintenance/          umbrella + shared gatherer scripts
  .opencode/skills/site-content-maintainer/   content/portfolio checks
  .opencode/skills/platform-maintainer/       machines, hardware, topology
  .opencode/skills/service-maintainer/        services, versions, charts

  .opencode/commands/maintain-site.md         run all domains
  .opencode/commands/maintain-content.md
  .opencode/commands/maintain-platform.md
  .opencode/commands/maintain-services.md
```

Rationale: the domains have different evidence sources, different blast radii,
and different runtime requirements (cluster access for platform and services,
none for content). Separate skills keep each prompt to one job — the same reason
the Sympozium fleet splits personas — and let a domain run where its evidence
lives. Alternatives considered: one skill with subcommands (a single large
prompt and one runtime that must have both `gh` and `kubectl`) and a single
GitHub Action (cannot reason, and cannot reach the cluster safely).

### D2 — Two layers: a deterministic gatherer, then judgement

```
  gather (code)                              judge (model, via domain skill)
  -------------                              --------------------------------
  content:  gh repo list/view/release        compare facts to site pages
            link + image existence            decide drift vs. deliberate
  platform: inventory + kubectl nodes         propose minimal edits
            namespaces, roles                 open branch + PR, or report no-op
  services: _version.yaml + helm/images
  emit compact JSON facts per domain
```

A shared gatherer emits a compact fact bundle per domain; the domain skill
reasons only over that bundle and the page contents. Rationale: matches the
platform's division of labour, keeps prompts short, and makes every proposed edit
traceable to a fetched fact.

### D3 — Cross-check the record against the cluster

```
  config-of-record            live cluster
  inventory.yml        <-->   kubectl get nodes / namespaces
  values/_version.yaml <-->   helm list / deployed image tags
              \                      /
               +-- mismatch -> finding (reported)
               +-- agreement -> site corrected to the agreed value
```

The site is corrected to match the live cluster when the sources agree; when they
disagree, the mismatch is reported as a finding naming both values and their
sources. The maintainer writes only to this site repository, so record drift in
another repository is surfaced, never fixed here.

### D4 — Scope is defined by data, not by prose

The repository set and its mapping to catalogue cards are read from the
catalogue plus the two organizations, with an explicit include/exclude list for
forks, archived repositories, and deliberate omissions. Platform scope comes
from the inventory and the live node list; service scope from `_version.yaml` and
the deployed releases. The maintainer fails loudly when a catalogued repository
or a referenced service no longer exists.

### D5 — PR-only, idempotent, one PR per domain

```
  branch per domain:  <domain>-maintainer/<YYYY-MM-DD>
  if an open PR for that domain exists -> update it, do not open a second
  if there are no corrections          -> open nothing; report and exit 0
  never commit to the default branch; never merge; never force-push
```

Rationale: separation keeps review boundaries clear and matches the domain
split; per-domain idempotency means a weekly run cannot accumulate open PRs.

### D6 — Image refresh stays conservative and delegated

Image refresh is part of the content domain and reuses the `showcase-images`
generation path, running only when a project's subject changed enough to make its
image misleading. Generation is paid and non-deterministic, so churn here defeats
the "one family" goal; the decision is recorded in the PR summary.

### D7 — Facts, not guesses; privacy is a hard boundary

No invented figure, link, node, service, or project. When a value cannot be
verified it is left unchanged or the unsupported claim removed, and the gap is
recorded. Real personal data (shopping, banking) never appears on the site or in
a PR.

### D8 — Credentials from the environment, least privilege

`gh` authenticates from the environment (an authenticated identity or
`GH_TOKEN`); the cluster is read through the ambient kubeconfig. No committed
secret. The token needs repository read plus pull-request write on the target
organizations — no administration, no merge rights — and the kubeconfig needs
read-only access, which the platform and service domains require and the content
domain does not.

## Risks / Trade-offs

- **The model proposes an incorrect change** → Every edit cites a fetched fact; a
  human reviews the PR before merge.
- **Three PRs per run could feel noisy** → Per-domain idempotency and quiet no-op
  runs; a combined run reports which domains were current.
- **The cluster is unreachable where a domain runs** → The platform and service
  passes fail loudly and name the unreachable source rather than reporting the
  site as correct.
- **Record-versus-cluster disagreement mis-scoped** → Reported, not fixed; the
  site follows the cluster only where sources agree.
- **Token or kubeconfig scope too broad** → Read + PR write only; no admin, no
  merge; cluster access is read-only.
- **False content drift from forks, archived, or private repos** → Explicit
  include/exclude list.
- **Site changes break the build** → The relevant skill runs `mkdocs build
  --strict` on the branch before opening its PR.
- **Later scheduler lacks interactive context** → Domain skills take no
  interactive input; orgs, branch, and dry-run are parameters.

## Migration Plan

1. Add the shared gatherer and the umbrella skill.
2. Add the content, platform, and service skills and their commands.
3. Dry-run each domain: gather facts, list proposed corrections, write nothing.
4. Run each domain for real; confirm only intended files changed and the site
   builds.
5. Rollback: close the PRs and delete the branches; the default branch never
   changed.

## Open Questions

- The exact include/exclude repository list once the catalogue exists.
- Whether the gatherer is shell or Python, and how it obtains cluster facts
  (`kubectl` vs. the `mcp-k8s` server used by the agents).
- The intended cadence (proposed weekly) and which domains a Sympozium schedule
  should own first.
- Whether an umbrella run should ever combine domains into a single PR.
- How to route reported record-versus-cluster drift to the owning repository
  (for example, an issue rather than only a PR summary).
