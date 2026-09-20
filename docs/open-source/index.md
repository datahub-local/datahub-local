# Open Source Projects

While building DataHub.local we ran into gaps in the ecosystem: charts that
didn't exist, tools that didn't support ARM64, or upstream projects that suddenly
changed their license. Rather than keeping the fixes private, we published them.

Each project below is actively used in production inside this cluster. The
[Projects catalogue](../projects/index.md#open-source-lessons) is the place for
narratives and lessons, while this page is the index of artifacts.

---

| Project | What it is | Source |
| ------- | ---------- | ------ |
| **spark-apps-helm** | Helm chart for deploying `SparkApplication` resources with shared runtime defaults | [GitHub](https://github.com/datahub-local/spark-apps-helm) |
| **garage-helm** | Helm chart for Garage S3 object storage, adding cluster init, bucket provisioning, and observability | [GitHub](https://github.com/datahub-local/garage-helm) |
| **servarr** | One Helm chart for the complete Servarr media stack with shared storage and ingress | [GitHub](https://github.com/datahub-local/servarr) |
| **node-exporter-textfiles** | Shell scripts exporting custom hardware and system metrics as Prometheus textfiles | [GitHub](https://github.com/datahub-local/node-exporter-textfiles) |
| **ollama-metrics** | Ollama metrics sidecar and proxy exposing token, latency, and model metrics | [GitHub](https://github.com/datahub-local/ollama-metrics) |

---

All charts are published as OCI artifacts via **GitHub Container Registry (GHCR)**:

```bash
helm install <release-name> oci://ghcr.io/datahub-local/<chart-name>
```

See also [Vendor-risk lessons](../lessons-learned.md) for the incidents that
produced several of these projects.
