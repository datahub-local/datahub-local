# Roadmap

What's coming next for DataHub.local — completed work is listed first, followed by active work and ideas for what comes next.

---

| Item                              | Details                                                                                                                    |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Homelab hardware & physical setup | Mixed ARM64/AMD64 cluster in a MicroATX case; CyberPower UPS; HORACO 2.5GbE managed switch                                 |
| K3s Kubernetes cluster            | 7-node heterogeneous cluster with GitOps, Longhorn, Traefik, cert-manager, Tailscale, gVisor, and multiple runtime classes |
| Core services (GitOps)            | ArgoCD ApplicationSet pipeline; encrypted secrets; Velero + Kopia backups; SSO via Dex                                     |
| Data Lakehouse Infra              | Trino + Apache Polaris + Garage S3 + CloudNative PostgreSQL + Apache Spark                                                 |
| Streaming infrastructure          | Redpanda 3-broker cluster (Kafka-compatible)                                                                               |
| Local and agentic AI              | Ollama + Open WebUI, Sympozium autonomous ensembles, and Prometheus/Kubernetes MCP tooling                                 |
| AI automation                     | n8n with AI nodes, LinkedIn Professional Visibility, and AI Diagram Generation                                             |
| Observability stack               | Prometheus + Grafana + Loki + Promtail + Robusta + AlertManager; 20 ServiceMonitors                                        |
| Open source publishing            | [spark-apps-helm, garage-helm, servarr, node-exporter-textfiles, ollama-metrics](open-source/index.md)                     |

---

## ✅ Completed

### :material-robot-happy: AI-Powered Personal AI (n8n + LLMs)

**Completed:** Automated repetitive personal tasks using n8n AI nodes and LLM integrations.

| AI capability          | Description                                                                                             | Status |
| ---------------------- | ------------------------------------------------------------------------------------------------------- | ------ |
| 📰 Content post updater | Pull trending topics from Commafeed + Google Trends MCP → generate an updated version of posts to share | ✅ Done |

---

### :material-table-arrow-right: Data Lakehouse — DBT + dlt + Iceberg

**Completed:** Replaced ad-hoc Airflow transformations with [DBT](https://www.getdbt.com/) models and [dlt](https://dlthub.com/) ingestion/export pipelines.

DBT provides version-controlled, tested SQL transformations, while dlt handles ingestion and reverse-ETL integration around the Iceberg lakehouse.

```mermaid
flowchart LR
    classDef source fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef layer fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef catalog fill:#00695C,color:#fff,stroke:#26C6DA,stroke-width:2px
    classDef viz fill:#E65100,color:#fff,stroke:#FFA726,stroke-width:2px

    Sources["🌐 External Sources\n(APIs, GDrive, etc.)"]:::source
    Raw["📦 Raw Layer\n(Garage S3 / Iceberg)"]:::layer
    Staging["🔄 Staging Layer\n(Iceberg)"]:::layer
    Marts["✨ Mart Layer\n(Iceberg)"]:::layer
    Superset["📊 Superset\nDashboards"]:::viz
    Polaris["🗃️ Apache Polaris\n(REST catalog)"]:::catalog

    Sources -->|"Airflow ingest"| Raw
    Raw -->|"DBT staging"| Staging
    Staging -->|"DBT transform"| Marts
    Marts -->|"Trino SQL"| Superset
    Polaris -.->|"catalog"| Raw & Staging & Marts
```

---

### :material-robot: Move to Claude — AI-Assisted Development

**Completed:** Adopted Claude as the primary AI assistant across the project for documentation, coding, repository management, and operations.

- Claude Code is used for coding tasks and documentation updates
- DataHub.local repositories are being standardised with `CLAUDE.md` guidance
- Reusable workflows cover deployment, linting, review, and documentation maintenance

---

### :material-receipt-text: Invoice Service — Personal Spending Intelligence

**Completed:** Built a real-time pipeline that ingests supermarket invoices, stores structured data in Iceberg, transforms it with DBT, and integrates ingestion/export with dlt.

**How it works:**

1. **Ingestion** — fetch invoice emails from Spanish supermarkets (Mercadona, Lidl, etc.) or extract receipts from Google Photos via OCR
2. **Storage** — parse and store structured line-item data in the Iceberg data lake
3. **Transformation** — DBT models aggregate spend by category, product, and store over time
4. **Notifications** — send a weekly digest via n8n with highlights like:
    - 💸 Current month spend by category
    - 📈 Products whose price has risen the most
    - 🛒 Shopping pattern changes vs. previous months

```mermaid
flowchart LR
    classDef source fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef process fill:#2E7D32,color:#fff,stroke:#66BB6A,stroke-width:2px
    classDef store fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef notify fill:#E65100,color:#fff,stroke:#FFA726,stroke-width:2px

    Email["📧 Email / Google Photos"]:::source
    Airflow["⚙️ Airflow"]:::process
    Iceberg["🏔️ Iceberg\n(Garage S3)"]:::store
    Marts["📊 Spend Marts"]:::store
    n8n["🔄 n8n"]:::process
    Notify["📲 Slack / Notification"]:::notify

    Email -->|"fetch + OCR"| Airflow
    Airflow -->|"structured rows"| Iceberg
    Iceberg -->|"DBT models"| Marts
    Marts -->|"Trino query"| n8n
    n8n -->|"weekly digest"| Notify
```

---

### :material-robot-excited: AI Agents — Sympozium

**Completed:** Three active ensembles (`homelab-ops`, `homelab-responder`, and `homelab-reviewer`) run in `automation`, with permissions, sandboxing, evaluation, and human approval boundaries implemented.

```mermaid
flowchart LR
    classDef alerting fill:#B71C1C,color:#fff,stroke:#EF5350,stroke-width:2px
    classDef agent fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef data fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef notify fill:#E65100,color:#fff,stroke:#FFA726,stroke-width:2px

    Alert["🚨 AlertManager"]:::alerting
    Robusta["🤖 Robusta"]:::alerting
    Agent["🧠 AI Agent\n(Sympozium)"]:::agent
    Loki["🗃️ Loki"]:::data
    Prometheus["📊 Prometheus"]:::data
    K8s["☸️ Kubernetes API"]:::data
    n8n["🔄 n8n"]:::data
    Notify["📲 Slack / Dashboard"]:::notify

    Alert --> Robusta
    Robusta -->|"enriched alert"| Agent
    Agent -->|"query logs"| Loki
    Agent -->|"query metrics"| Prometheus
    Agent -->|"bounded Kubernetes tools"| K8s
    Agent -->|"run playbook"| n8n
    Agent -->|"report"| Notify
```

---

## 🔄 In Progress

### :material-server-network: MCP Servers for AI Tooling

**Status:** In progress. The first implementation is available in `datahub-local-ai/agents/mcp`, with Prometheus and Kubernetes-backed homelab facts tools. The next step is to expand coverage and keep all mutating operations behind explicit policy and approval checks.

| Server           | Exposes                                              |
| ---------------- | ---------------------------------------------------- |
| `mcp-prometheus` | Query metrics, inspect alerts, get service health    |
| `mcp-loki`       | Search logs, tail pod output, find errors            |
| `mcp-kubernetes` | List / describe / restart workloads safely           |
| `mcp-trino`      | Run SQL queries against the data lakehouse           |
| `mcp-polaris`    | Browse Iceberg catalog, list tables, inspect schemas |
| `mcp-garage`     | List buckets / objects, check storage usage          |

## 📋 Next

Additional platform and AI capabilities will be added as they are designed, implemented, tested, and validated against the live cluster.

More soon…
