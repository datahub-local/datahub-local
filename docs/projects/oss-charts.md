# Giving Back to the Community

The platform stands on open source that other people wrote and gave away freely.
That is why most of this site can be read, run, and rebuilt at no licence cost.
When we hit a gap, the choice was to keep the workaround private or hand it back.
These five projects are the work we returned: the charts and exporters the
ecosystem did not have.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">Community</span>
  <span class="meta-pill meta-pill--status">Published</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local">:fontawesome-brands-github: datahub-local</a>
</p>

<figure markdown="span">
  ![A dark loading bay with a stack of crates, one open and glowing green](../assets/img/showcase/open-source/oss-charts-hero.webp){ width="1024" }
</figure>

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

- **[`garage-helm`](https://github.com/datahub-local/garage-helm)**: Garage's
  official chart was minimal, so the fork adds automatic cluster initialisation,
  bucket and key provisioning, a `ServiceMonitor`, and flexible ingress.
- **[`spark-apps-helm`](https://github.com/datahub-local/spark-apps-helm)**: wraps
  `SparkApplication` boilerplate behind shared runtime defaults, so jobs override
  only what they need.
- **[`servarr`](https://github.com/datahub-local/servarr)**: deploys the whole
  Servarr media stack with shared storage and ingress in a single `helm install`.
- **[`node-exporter-textfiles`](https://github.com/datahub-local/node-exporter-textfiles)**:
  exports hardware metrics such as SBC temperatures, GPIO, and UPS state that the
  standard exporter does not provide.
- **[`ollama-metrics`](https://github.com/datahub-local/ollama-metrics)**: an
  Ollama sidecar and proxy exposing token, latency, speed, and model-memory
  metrics.

All charts are published as OCI artifacts via GitHub Container Registry, so they
install with a single command:

```bash
helm install <release-name> oci://ghcr.io/datahub-local/<chart-name>
```

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

- [Hard Lessons](../lessons-learned.md): the incidents that forced several of these projects
