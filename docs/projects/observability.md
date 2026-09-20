# Observability stack

Metrics, logs, dashboards, and enriched alerting across every layer, plus a
proactive AI loop above the rule-based one.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">Platform &amp; Operations</span>
  <span class="meta-pill meta-pill--status">Running</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-core">:fontawesome-brands-github: datahub-local-core</a>
</p>

<figure markdown="span">
  ![A dark field of ripples with a suspended lens and one ringed pulse](../assets/img/showcase/platform-operations/observability-hero.webp){ width="1024" }
</figure>

## Problem

A platform you cannot see is a platform you cannot operate or trust. In an
enterprise the observability stack is bought and integrated. At home it has to
be assembled, and it still has to cover the same ground: are nodes healthy, are
services up, what happened when an alert fired, and is anything trending toward
failure before a rule catches it.

Alert fatigue compounds the problem. A notification without context is a task,
not a signal.

## Approach

The stack follows the standard three pillars and adds context at the alerting
edge.

- **Metrics**: **Prometheus** scrapes node-exporter on every node,
  kube-state-metrics, control-plane targets, and application exporters, with 20
  `ServiceMonitor` resources discovering the scrape surface.
- **Logs**: **Promtail** runs as a per-node DaemonSet and ships pod logs to
  **Loki**, stored in Garage S3 and queryable from Grafana with LogQL.
- **Dashboards**: **Grafana** sits over both datasources with cluster, data
  service, and application views.
- **Alerting with context**: **AlertManager** routes firing alerts to
  **Robusta**, which enriches each one with pod logs, events, and resource
  graphs before delivery.
- **Custom metrics**: purpose-built exporters (`node-exporter-textfiles`,
  `ollama-metrics`, `speedtest-exporter`) cover hardware and inference details
  the standard exporters miss.
- **A proactive loop**: the [SRE agents](sre-agents.md) sit above the rules,
  investigating trends and chronic alerts through MCP tooling.

## Technologies

- **Prometheus** and **AlertManager** for metrics and alert routing
- **Loki** and **Promtail** for log aggregation
- **Grafana** for dashboards and LogQL
- **Robusta** for alert enrichment
- **Garage S3** for log retention

## Outcome

Every layer of the platform is measured, logged, and alertable, and alerts
arrive with the evidence needed to act. The AI monitoring loop extends coverage
to the signals a threshold rule cannot express, without replacing the
deterministic detection underneath it.

## Further reading

- [Monitoring](../services/monitoring.md): the full component detail
- [SRE agents (Sympozium)](sre-agents.md): the proactive loop in practice
- [Cloud-at-home on mini-PCs](cloud-at-home.md): the estate being observed
