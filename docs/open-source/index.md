# Open Source Projects

While building DataHub.local we ran into gaps in the ecosystem — charts that didn't exist, tools that didn't support ARM64, or upstream projects that suddenly changed their license. Rather than keeping the fixes private, we published them so other homelab builders and data engineers can benefit too.

Each project below is actively used in production inside this cluster.

---

## spark-apps-helm

[![GitHub](https://img.shields.io/badge/GitHub-spark--apps--helm-181717?logo=github)](https://github.com/datahub-local/spark-apps-helm)

A Helm chart for deploying `SparkApplication` resources on Kubernetes using the [Spark Operator](https://github.com/kubeflow/spark-operator).

**Why we created it:** Every `SparkApplication` resource requires significant boilerplate YAML — driver/executor resources, image pull secrets, S3 credentials, Nessie catalog config, and more. We needed a way to define shared runtime defaults once and let each job override only what it needs, without copy-pasting hundreds of lines per pipeline.

---

## garage-helm

[![GitHub](https://img.shields.io/badge/GitHub-garage--helm-181717?logo=github)](https://github.com/datahub-local/garage-helm)

A Helm chart for deploying [Garage](https://garagehq.deuxfleurs.fr/) — a lightweight, distributed, S3-compatible object storage system — on Kubernetes.

**Why we created it:** MinIO changed its license and removed its open-source container images with little notice, forcing a migration. Garage was the best replacement for a small heterogeneous cluster (single binary, ARM64-friendly, no commercial lock-in) but its official Helm chart was minimal — no automatic cluster initialisation, no bucket provisioning, no observability. We built what was missing and published it.

---

## servarr

[![GitHub](https://img.shields.io/badge/GitHub-servarr-181717?logo=github)](https://github.com/datahub-local/servarr)

A comprehensive Helm chart that deploys the complete Servarr media management stack — Jellyfin, Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr, Jellyseerr, and Flaresolverr — in a single command.

**Why we created it:** Deploying the *arr ecosystem meant managing many separate, inconsistent Helm charts. We wanted one chart with shared NFS storage, selective app enabling, and Traefik ingress already wired up — so the whole stack comes up with a single `helm install`.

---

## node-exporter-textfiles

[![GitHub](https://img.shields.io/badge/GitHub-node--exporter--textfiles-181717?logo=github)](https://github.com/datahub-local/node-exporter-textfiles)

A collection of shell scripts that generate Prometheus textfile metrics for node-exporter — covering custom hardware and system metrics not provided by the standard exporter.

**Why we created it:** Several metrics specific to our hardware (SBC temperatures, GPIO states, UPS status) were not exposed by the standard node-exporter. These scripts fill that gap and feed into our Grafana dashboards.

---

All charts are published as OCI artifacts via **GitHub Container Registry (GHCR)**:

```bash
helm install <release-name> oci://ghcr.io/datahub-local/<chart-name>
```
