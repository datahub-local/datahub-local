# Published OSS Helm charts

Five pieces of missing infrastructure, built for this cluster and published so
other homelab builders and data engineers can use them.

| | |
| --- | --- |
| **Area** | Open Source & Lessons |
| **Status** | Published |
| **Index** | [Open Source artifacts](../open-source/index.md) |

## Problem

Building a platform at home repeatedly runs into gaps in the ecosystem: charts
that don't exist, tools that don't support ARM64, or projects that change
license without warning. Forking privately solves the immediate problem and
leaves the next person to hit the same wall.

Publishing, by contrast, turns each workaround into a maintained artifact and
forces the quality bar up, because someone else may depend on it.

## Approach

Each project addresses a gap the cluster actually hit and is used in production
here before publication.

- **`garage-helm`**: Garage's official chart was minimal, so the fork adds
  automatic cluster initialisation, bucket and key provisioning, a
  `ServiceMonitor`, and flexible ingress.
- **`spark-apps-helm`**: wraps `SparkApplication` boilerplate behind shared
  runtime defaults, so jobs override only what they need.
- **`servarr`**: deploys the whole Servarr media stack with shared storage and
  ingress in a single `helm install`.
- **`node-exporter-textfiles`**: exports hardware metrics such as SBC
  temperatures, GPIO, and UPS state that the standard exporter does not provide.
- **`ollama-metrics`**: an Ollama sidecar and proxy exposing token, latency,
  speed, and model-memory metrics.

All charts are published as OCI artifacts via GitHub Container Registry, so they
install with a single `helm install` command.

## Technologies

- **Helm** and **OCI registries (GHCR)**
- **Garage**, **Spark Operator**, **Servarr**, and **Ollama** for the problems solved
- **Prometheus** for the observability gaps filled

## Outcome

The gaps that cost this platform time are now maintained projects with a public
home, and the act of publishing raised their quality. It is the platform giving
back to the ecosystem it depends on, the concrete output of the vendor-risk
lessons.

## Further reading

- [Open Source](../open-source/index.md): the artifact list and install command
- [Vendor-risk lessons](vendor-risk.md): the incidents that produced these charts
- [Lessons Learned](../lessons-learned.md): the full write-up
