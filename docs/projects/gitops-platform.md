# GitOps & platform engineering

Every service delivered from Git through ArgoCD, with quality gates before merge
and automated dependency updates.

| | |
| --- | --- |
| **Area** | Platform & Operations |
| **Status** | Running |
| **Source** | [`datahub-local-core`](https://github.com/datahub-local/datahub-local-core) |

## Problem

Managing a heterogeneous cluster by hand does not scale and leaves no audit
trail. A homelab is exactly where a manual habit is most tempting, because there
is no team to enforce process, and exactly where it hurts most, because there is
no one else to fix the drift you introduced at midnight.

The platform needed the delivery discipline of an enterprise without the
headcount: a single source of truth, reviewed changes, and continuous
reconciliation.

## Approach

The delivery model layers repositories, each depending only on the one below it,
with ArgoCD reconciling the cluster against Git.

- **Bootstrap layer**: Ansible installs the OS and K3s and seeds ArgoCD. After
  that, manual access is the exception, not the workflow.
- **Secrets layer**: a private repository holds sealed secrets, synced before
  anything that depends on them.
- **Core layer**: Helmfile ApplicationSets expand into one ArgoCD Application
  per namespace, using server-side apply to avoid Helm field-ownership
  conflicts, with automated sync on `HEAD`.
- **AI layer**: workflows, DAGs, dbt and dlt projects, MCP servers, and agent
  ensembles deploy through the same path.
- **Quality gates**: GitHub Actions run lint, tests, and dry-runs per repository
  type, while **Renovate** opens version-bump pull requests on a schedule and
  AI-assisted, versioned development workflows keep changes reviewed.

Auto-sync deliberately excludes prune, so deletions remain a conscious, manual
step rather than an accident of a commit.

## Technologies

- **ArgoCD** with ApplicationSets and server-side apply
- **Helmfile** and **Helm** for service packaging
- **Ansible** for provisioning and bootstrap
- **GitHub Actions** and **Renovate** for gates and dependency hygiene

## Outcome

The cluster's desired state is always a commit, drift is reconciled
continuously, and every change has a review and a history. Rebuilding or
migrating the platform is a matter of pointing ArgoCD at the repositories, which
is what makes the rest of this catalogue reproducible rather than anecdotal.

## Further reading

- [CI/CD](../services/cicd.md): repositories, gates, and Renovate behaviour
- [Automation services](../services/automation.md): ArgoCD patterns in detail
- [Provisioning](../cluster_setup/provisioning.md): the bootstrap to GitOps handover
