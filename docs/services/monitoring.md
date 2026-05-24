# Monitoring & Observability

The monitoring stack provides full-stack observability: metrics, logs, alerts, and Kubernetes-level automation. Every service in the cluster exposes Prometheus metrics, ships logs to Loki, and is covered by AlertManager rules.

---

## Stack Overview

```mermaid
flowchart TB
    subgraph Sources
        Pods["All Pods\n(metrics endpoints)"]
        Nodes["Nodes\n(node-exporter)"]
        K8sAPI["Kubernetes API\n(kube-state-metrics)"]
        Speedtest["Speedtest\n(internet monitoring)"]
    end

    subgraph Collection
        Prometheus["Prometheus\n(metrics scrape)"]
        Promtail["Promtail\n(log shipper, per node)"]
    end

    subgraph Storage
        Loki["Loki\n(log storage)"]
        PromDB["Prometheus TSDB\n(metric storage)"]
    end

    subgraph Visualization
        Grafana["Grafana\n(dashboards)"]
    end

    subgraph Alerting
        AlertManager["AlertManager"]
        Robusta["Robusta\n(enrichment + automation)"]
        Notify["Notifications\n(Slack, email, etc.)"]
    end

    Pods --> Prometheus
    Nodes --> Prometheus
    K8sAPI --> Prometheus
    Speedtest --> Prometheus
    Pods -->|"stdout/stderr"| Promtail
    Promtail --> Loki
    Prometheus --> PromDB
    PromDB --> Grafana
    Loki --> Grafana
    PromDB --> AlertManager
    AlertManager --> Robusta
    Robusta --> Notify
```

---

## Services

### :material-chart-timeline-variant: [Prometheus + AlertManager](https://github.com/prometheus-operator/kube-prometheus-stack)

<div class="svc-tags"><span class="svc-tag">monitoring</span> <span class="svc-tag">metrics</span> <span class="svc-tag">alerting</span> <span class="svc-tag">time-series</span></div>

Prometheus scrapes metrics from every service that exposes a `/metrics` endpoint, as well as from node-exporter (7 nodes) and kube-state-metrics. AlertManager routes firing alerts through configurable receivers. All scrape targets are auto-discovered via `ServiceMonitor` resources.

**Custom exporters running:**

- `node-exporter-textfiles` — custom metrics collected via shell scripts, exposed as Prometheus textfile format (custom open-source [project](https://github.com/datahub-local/node-exporter-textfiles))
- `speedtest-exporter` — periodic internet speed test results as metrics

---

### :material-view-dashboard: [Grafana](https://grafana.com/)

<div class="svc-tags"><span class="svc-tag">visualization</span> <span class="svc-tag">dashboards</span> <span class="svc-tag">observability</span></div>

Grafana provides dashboards for every layer of the stack, with SSO via OAuth2 / Dex OIDC. Data sources: Prometheus (metrics) and Loki (logs).

- **Cluster overview** — node CPU, memory, network, disk (from kube-prometheus-stack defaults)
- **Data services** — Airflow, Trino, Redpanda, PostgreSQL, Spark custom dashboards
- **Application metrics** — per-namespace resource usage
- **Internet performance** — Speedtest results over time

---

### :material-text-box-search: [Loki + Promtail](https://grafana.com/oss/loki/)

<div class="svc-tags"><span class="svc-tag">logging</span> <span class="svc-tag">log-aggregation</span> <span class="svc-tag">observability</span></div>

Promtail runs on every node as a DaemonSet, tailing all pod log files and shipping them to Loki with labels (`namespace`, `pod`, `container`). Loki stores logs in Garage S3 for long-term retention. All logs are queryable from Grafana using LogQL. Components: Loki (2 pods + gateway), Promtail (DaemonSet — 1 per node).

---

### :material-robot-excited: [Robusta](https://robusta.dev/)

<div class="svc-tags"><span class="svc-tag">alerting</span> <span class="svc-tag">kubernetes</span> <span class="svc-tag">automation</span> <span class="svc-tag">incident-response</span></div>

Robusta acts as a smart AlertManager webhook receiver. When an alert fires, Robusta:

1. **Enriches it** — attaches pod logs, recent events, resource graphs automatically
2. **Routes it** — sends enriched notifications to Slack/Teams/email with all context
3. **Can remediate** — configured playbooks can automatically restart pods, scale deployments, or run diagnostic commands

This dramatically reduces alert fatigue by providing context alongside every notification.

---

### :material-speedometer: [Speedtest Exporter](https://github.com/MiguelNdeCarvalho/speedtest-exporter)

<div class="svc-tags"><span class="svc-tag">monitoring</span> <span class="svc-tag">network</span> <span class="svc-tag">metrics</span> <span class="svc-tag">performance</span></div>

Runs Speedtest CLI periodically and exposes download speed, upload speed, ping, and jitter as Prometheus metrics. Grafana dashboards visualize internet performance trends over time — useful for detecting ISP issues or home network degradation before they affect cluster services.
