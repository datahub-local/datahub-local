# Repositories

Fifteen repositories are public under [`github.com/datahub-local`](https://github.com/datahub-local).
Five are the platform and carry the work. The other ten are support artifacts:
a chart, an image, or an example the platform consumes.

The [project catalogue](projects/index.md) is organised by use case. This page is
organised by repository, so you can go from a question to the place that answers
it.

---

## The platform

| Repository | Owns | Read first |
| --- | --- | --- |
| [`datahub-local`](https://github.com/datahub-local/datahub-local) | The published documentation site (MkDocs). Project pages, architecture, lessons learned. | `mkdocs.yml`, `docs/` |
| [`datahub-local-core`](https://github.com/datahub-local/datahub-local-core) | The helmfile releases ArgoCD applies: every service, its values, its patches. | `releases/<namespace>/helmfile.yaml.gotmpl`, `releases/<namespace>/values/` |
| [`datahub-local-ai`](https://github.com/datahub-local/datahub-local-ai) | AI workflows and the data pipelines: n8n exports and prompts, Sympozium ensembles, dbt/dlt/Airflow, Superset bundles, adapter images. | `AGENTS.md`, then the deep dive for the path you touch |
| [`datahub-local-ai-mcp`](https://github.com/datahub-local/datahub-local-ai-mcp) | The MCP servers agents call: `homelab_facts`, `semantic`, `semantic-finance`, `utils`, `opencode`. | `README.md`, `servers/<name>/` |
| [`datahub-local-bootstrap`](https://github.com/datahub-local/datahub-local-bootstrap) | Ansible that brings a machine up as a cluster node. Owner only. | `README.md`, `playbook/` |

## Where to go with a question

- "How is this deployed, and why does this Pod fail?" [`datahub-local-core`](https://github.com/datahub-local/datahub-local-core).
  The values file for that release is the answer; the chart is upstream.
- "Why did this automation fail?" [`datahub-local-ai`](https://github.com/datahub-local/datahub-local-ai),
  under `agents/n8n/`.
- "What does this metric mean, and what SQL computes it?"
  [`datahub-local-ai-mcp`](https://github.com/datahub-local/datahub-local-ai-mcp)
  (`semantic`) with the registry in
  `datahub-local-ai/workflows/dbt/semantic/`.
- "Add or fix a dashboard."
  [`datahub-local-ai/workflows/superset/`](https://github.com/datahub-local/datahub-local-ai/tree/main/workflows/superset).
- "Change a page or a diagram." [`datahub-local`](https://github.com/datahub-local/datahub-local).
- "Change what an agent reports or when it runs."
  [`datahub-local-ai/agents/sympozium/`](https://github.com/datahub-local/datahub-local-ai/tree/main/agents/sympozium).
- "Add or fix an MCP tool." [`datahub-local-ai-mcp`](https://github.com/datahub-local/datahub-local-ai-mcp).
- "Why does a host behave like this?"
  [`datahub-local-bootstrap`](https://github.com/datahub-local/datahub-local-bootstrap)
  for the role, read only. The running host itself is the owner's machine.
- "How do I describe the platform?" [`datahub-local`](https://github.com/datahub-local/datahub-local),
  which is the published text.

## Support repositories

Nothing routine lands in these. A task that names one is the only reason to open
it. Several are archived, and GitHub marks them on the repository page.

| Repository | What it carries |
| --- | --- |
| [`garage-helm`](https://github.com/datahub-local/garage-helm) | Helm chart for Garage, the S3-compatible object store the lakehouse writes to. |
| [`spark-apps-helm`](https://github.com/datahub-local/spark-apps-helm) | Helm chart for Apache Spark applications on Kubernetes. |
| [`node-exporter-textfiles`](https://github.com/datahub-local/node-exporter-textfiles) | Container image for textfile exporter scripts that `node_exporter` collects. |
| [`ollama-metrics`](https://github.com/datahub-local/ollama-metrics) | Metrics collector and proxy that exposes Prometheus metrics for Ollama. |
| [`servarr`](https://github.com/datahub-local/servarr) | Helm chart for a Servarr media stack. |
| [`Byparr`](https://github.com/datahub-local/Byparr) | FlareSolverr drop-in replacement for browser-based scraping. |
| [`dagster-celery-k8s-oci`](https://github.com/datahub-local/dagster-celery-k8s-oci) | Dagster image for Kubernetes and Celery deployments on ARM. |
| [`dagster-user-code-example`](https://github.com/datahub-local/dagster-user-code-example) | Example user-code repository for the Dagster images. |
| [`container-helm-version-updater`](https://github.com/datahub-local/container-helm-version-updater) | Action that updates container image and Helm chart versions. |
| [`docker-lineageos`](https://github.com/datahub-local/docker-lineageos) | Docker-based build environment for LineageOS. |

## Not public

`datahub-local-secrets` and `datahub-local-private-config` are private and out of
scope. Nothing here links to them, quotes them, or describes their values. If a
task needs a value that lives there, ask for that one setting.

The org keeps other private repositories for personal configuration. They are
out of scope for the same reason.

---

The agent skill `repo-map` in
[`datahub-local-ai`](https://github.com/datahub-local/datahub-local-ai/blob/main/agents/adapters/opencode/skills/repo-map/SKILL.md)
carries the same table. Change both in the same pass.
