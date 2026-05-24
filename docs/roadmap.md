# Roadmap

What's coming next for DataHub.local — priorities are ordered by status: done, in progress, near-term, and medium-term.

---

## ✅ Completed

| Item | Details |
|------|---------|
| Homelab hardware & physical setup | Mixed ARM64/AMD64 cluster in a MicroATX case; CyberPower UPS; HORACO 2.5GbE managed switch |
| K3s Kubernetes cluster | 7-node cluster with GitOps, Longhorn, Traefik, cert-manager, Tailscale |
| Core services (GitOps) | ArgoCD ApplicationSet pipeline; encrypted secrets; Velero + Kopia backups; SSO via Dex |
| Data Lakehouse Infra | Trino + Project Nessie + Garage S3 + CloudNative PostgreSQL + Apache Spark |
| Streaming infrastructure | Redpanda 3-broker cluster (Kafka-compatible) |
| Local AI inference | Ollama + Open WebUI + VUI voice interface |
| Workflow automation | n8n with AI nodes |
| Active n8n Workflows | LinkedIn Professional Visibility workflow; AI Diagram Generation workflow |
| Observability stack | Prometheus + Grafana + Loki + Robusta + AlertManager |
| Open source publishing | [spark-apps-helm, garage-helm, servarr](open-source/index.md) |

---

## 🔄 In Progress

### :material-robot-happy: AI-Powered Personal Workflows (n8n + LLMs)

**Goal:** Automate repetitive personal tasks using local LLMs connected via n8n workflows.

| Workflow | Description | Status |
|---------|-------------|--------|
| 📰 Content post updater | Pull trending topics from Commafeed + Google Trends MCP → generate an updated version of posts to share | 🔄 Building |

---

### :material-table-arrow-right: Data Lakehouse — SQLMesh + Iceberg

**Goal:** Replace ad-hoc Airflow ETL scripts with a proper transformation layer using [SQLMesh](https://sqlmesh.com/).

SQLMesh brings software engineering practices to SQL transformations: version control, automated testing, CI/CD for data models, and incremental processing.

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
    Nessie["🗃️ Project Nessie\n(catalog)"]:::catalog

    Sources -->|"Airflow ingest"| Raw
    Raw -->|"SQLMesh staging"| Staging
    Staging -->|"SQLMesh transform"| Marts
    Marts -->|"Trino SQL"| Superset
    Nessie -.->|"versions"| Raw & Staging & Marts
```

---

## 📋 Near-Term

### :material-robot: Move to Claude — AI-Assisted Development

**Goal:** Adopt Claude as the primary AI assistant across the entire project — documentation, coding, repo management, and operations.

- Use Claude Code for all coding tasks and doc updates in every repository
- Initialise every datahub-local repo with a `CLAUDE.md` and project-specific skills
- Create reusable Claude skills for common tasks (deploy, lint, review, update docs)
- Use Claude for ongoing documentation maintenance so the docs stay in sync with the cluster

---

### :material-receipt-text: Invoice Service — Personal Spending Intelligence

**Goal:** Build a real-time pipeline that automatically ingests supermarket invoices and turns them into actionable spending insights.

**How it works:**

1. **Ingestion** — fetch invoice emails from Spanish supermarkets (Mercadona, Lidl, etc.) or extract receipts from Google Photos via OCR
2. **Storage** — parse and store structured line-item data in the Iceberg data lake
3. **Transformation** — SQLMesh models aggregate spend by category, product, and store over time
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
    Iceberg -->|"SQLMesh models"| Marts
    Marts -->|"Trino query"| n8n
    n8n -->|"weekly digest"| Notify
```

---

## 📅 Medium-Term

### :material-robot-excited: AI Agents — Sympozium

**Goal:** Autonomous LLM-powered SRE agents that monitor, diagnose, and remediate cluster issues without human intervention.

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
    Agent -->|"kubectl exec"| K8s
    Agent -->|"run playbook"| n8n
    Agent -->|"report"| Notify
```

---

### :material-server-network: MCP Servers for AI Tooling

**Goal:** Expose cluster capabilities as [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers so AI assistants can interact with the homelab directly.

| Server | Exposes |
|--------|---------|
| `mcp-prometheus` | Query metrics, inspect alerts, get service health |
| `mcp-loki` | Search logs, tail pod output, find errors |
| `mcp-kubernetes` | List / describe / restart workloads safely |
| `mcp-trino` | Run SQL queries against the data lakehouse |
| `mcp-nessie` | Browse Iceberg catalog, list tables, inspect schemas |
| `mcp-garage` | List buckets / objects, check storage usage |
