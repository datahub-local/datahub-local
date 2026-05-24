# CI/CD

The CI/CD layer enforces quality gates on every change, keeps all dependencies up-to-date automatically, and delivers the docs site without manual intervention. It sits entirely outside the cluster — hosted by GitHub and Renovate Cloud — and feeds into ArgoCD for the final deployment step.

---

## Architecture

```mermaid
flowchart TB
    classDef repo fill:#1e2b1c,color:#A3CF7A,stroke:#5E8A3F,stroke-width:1px
    classDef auto fill:#5E8A3F,color:#F4F2EC,stroke:#A3CF7A,stroke-width:2px
    classDef deploy fill:#3d5c28,color:#F4F2EC,stroke:#7FAF5A,stroke-width:2px

    subgraph REPOS["📦 Repositories (datahub-local org)"]
        BOOTSTRAP["datahub-local-bootstrap\nAnsible playbooks"]:::repo
        CORE["datahub-local-core\nHelm · ArgoCD ApplicationSets"]:::repo
        SECRETS["datahub-local-secrets\nEncrypted config"]:::repo
        WORKFLOWS["datahub-local-workflows\nn8n · Airflow · SQLMesh"]:::repo
        DOCS["datahub-local\nDocumentation"]:::repo
    end

    subgraph AUTOMATION["🤖 Automation"]
        RENOVATE["Renovate Cloud\nauto-PRs"]:::auto
        GHA["GitHub Actions\nquality gates"]:::auto
    end

    subgraph DEPLOY["🚀 Deployment"]
        ARGOCD["ArgoCD\nauto-sync"]:::deploy
        ANSIBLE["Ansible\nmanual run"]:::deploy
    end

    RENOVATE -->|"auto PRs on schedule"| BOOTSTRAP
    RENOVATE -->|"auto PRs on schedule"| CORE
    RENOVATE -->|"auto PRs on schedule"| SECRETS
    RENOVATE -->|"auto PRs on schedule"| WORKFLOWS
    RENOVATE -->|"auto PRs on schedule"| DOCS

    BOOTSTRAP --> GHA
    CORE --> GHA
    WORKFLOWS --> GHA
    DOCS --> GHA

    GHA -->|"ansible-lint · syntax check"| BOOTSTRAP
    GHA -->|"helm lint · schema validate"| CORE
    GHA -->|"mkdocs build · gh-deploy"| DOCS

    CORE -->|"watches HEAD"| ARGOCD
    SECRETS -->|"watches HEAD"| ARGOCD
    WORKFLOWS -->|"watches HEAD"| ARGOCD
    BOOTSTRAP -.->|"after merge (manual)"| ANSIBLE
```

---

## Services

### :simple-github: [GitHub](https://github.com/datahub-local)

<div class="svc-tags"><span class="svc-tag">source-control</span> <span class="svc-tag">git</span> <span class="svc-tag">collaboration</span> <span class="svc-tag">devops</span></div>

Central source of truth for every part of the platform. The organisation is split into focused repositories following a layered deployment model — each layer only depends on the one below it.

```
bootstrap  →  secrets  →  core  →  workflows
```

| Repository | Role | Deployed by |
|---|---|---|
| [datahub-local](https://github.com/datahub-local/datahub-local) | Documentation site (this site) | GitHub Actions → GitHub Pages |
| [datahub-local-bootstrap](https://github.com/datahub-local/datahub-local-bootstrap) | Ansible playbooks — OS provisioning, K3s install, ArgoCD bootstrap | Manual `ansible-playbook` run |
| [datahub-local-secrets](https://github.com/datahub-local/datahub-local-secrets) | Encrypted secrets and private config | ArgoCD (manual sync) |
| [datahub-local-core](https://github.com/datahub-local/datahub-local-core) | Helmfile ApplicationSets — all platform services | ArgoCD (manual sync) |
| [datahub-local-workflows](https://github.com/datahub-local/datahub-local-workflows) | n8n flows, Airflow DAGs, SQLMesh models | ArgoCD (manual sync) |

All changes flow through pull requests, providing a full audit trail before anything reaches the cluster or production environment.

---

### :material-rocket-launch: [GitHub Actions](https://github.com/features/actions)

<div class="svc-tags"><span class="svc-tag">ci-cd</span> <span class="svc-tag">automation</span> <span class="svc-tag">testing</span> <span class="svc-tag">deployment</span></div>

Runs quality gates on every pull request and on every merge to `main`. Pipelines are tailored per repository type — nothing lands in `main` without passing its full gate.

| Workload type | Checks applied |
|---|---|
| Python services & DAGs | Linting (`ruff`, `flake8`), unit tests (`pytest`), integration tests |
| Helm charts | `helm lint`, `helm template` dry-run, schema validation |
| Ansible playbooks | `ansible-lint`, syntax check |
| Docker images | Build, push to registry |
| SQLMesh models | Model parse, DAG validation |

---

### :material-refresh-auto: [Renovate Cloud](https://www.mend.io/renovate/)

<div class="svc-tags"><span class="svc-tag">dependency-management</span> <span class="svc-tag">automation</span> <span class="svc-tag">devops</span> <span class="svc-tag">security</span></div>

Keeps every dependency current without manual tracking. Renovate scans all repositories on a schedule and opens a pull request for each detected version bump — packages, container images, Helm chart versions, GitHub Actions, and Python dependencies are all covered.

| Repository | Renovate behaviour |
|---|---|
| `datahub-local` (docs) | PRs created **automatically**; GitHub Actions validates before merge |
| `datahub-local-core` | PRs created **automatically**; Helm lint must pass; ArgoCD **auto-syncs** after merge |
| `datahub-local-secrets` | PRs created **automatically** |
| `datahub-local-workflows` | PRs created **automatically**; pipeline validation must pass; ArgoCD **auto-syncs** after merge |
| `datahub-local-bootstrap` | Renovate PRs created **automatically**, but the Ansible playbook must be **run manually** after merge |

!!! info "ArgoCD auto-sync: applies resources, skips deletions"
    ArgoCD **auto-sync is enabled** — commits to watched repositories are reconciled to the cluster automatically. However, auto-sync deliberately **excludes prune**: resources that no longer exist in Git are not automatically deleted. Removing a service, renaming a Helm release, or any other deletion requires a **manual sync with prune** enabled in the ArgoCD UI.
