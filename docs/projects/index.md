# Projects

The platform is not the point. What it produces is. This catalogue lists the
fourteen use cases built on DataHub.local across four areas. Every card opens a
full case study with the problem, approach, technologies, outcome, and source.

---

## Data & Analytics

<div class="grid cards" markdown>

- ![A stratified core sample of translucent sediment layers under a still surface](../assets/img/showcase/data-analytics/lakehouse-core-cover.webp)

    :material-database: **[Lakehouse core stack](lakehouse-core.md)**

    Ingestion, Iceberg storage in Garage, a Polaris catalog, Trino federation,
    dbt transformations, and Superset dashboards.

- ![A blank paper receipt curling into a tidy grid of blank tiles](../assets/img/showcase/data-analytics/bodega-cover.webp)

    :material-cart: **[Bodega shopping analytics](bodega.md)**

    Supermarket invoices turned into a structured Iceberg dataset and a weekly
    spend digest, described by method and aggregates only.

- ![A sealed frosted-glass ledger box, closed and unmarked](../assets/img/showcase/data-analytics/personal-finance-cover.webp)

    :material-cash-multiple: **[Personal finance datalake](personal-finance.md)**

    A private analytics pipeline over personal documents with a governed SQL
    surface and no source rows published.

- ![A precision lens aligning several thin light beams onto one plane](../assets/img/showcase/data-analytics/semantic-layer-cover.webp)

    :material-table: **[Semantic layer for agents](semantic-layer.md)**

    A catalogued, versioned SQL surface over the lakehouse so agents and BI
    tools query the same governed definitions.

- ![A branching root system with lit inspection nodes, one branch marked](../assets/img/showcase/data-analytics/data-quality-lineage-cover.webp)

    :material-check-decagram: **[Data quality & lineage](data-quality-lineage.md)**

    dbt tests, explicit model lineage, and Iceberg snapshots applied to the
    lakehouse tables.

</div>

## AI & Agents

<div class="grid cards" markdown>

- ![Small matte survey drones hovering over a dark contoured surface](../assets/img/showcase/ai-agents/sre-agents-cover.webp)

    :material-robot-excited: **[SRE agents (Sympozium)](sre-agents.md)**

    Narrow, scheduled agents that investigate alerts and trends through bounded
    MCP tools and report in a fixed format.

- ![A docking hub of six identical read-only ports](../assets/img/showcase/ai-agents/mcp-platform-cover.webp)

    :material-connection: **[MCP platform](mcp-platform.md)**

    Read-only Model Context Protocol servers exposing Prometheus, Loki,
    Kubernetes, Trino, Polaris, and Garage facts to agents safely.

- ![A paper lantern hanging in a dark studio as motes gather into a shape](../assets/img/showcase/ai-agents/oracle-responder-cover.webp)

    :material-help-circle: **[Ask-your-cluster oracle](oracle-responder.md)**

    A natural-language front door over cluster and repository state for
    operational questions.

- ![A loom weaving threads of light into a blank page](../assets/img/showcase/ai-agents/ai-content-engine-cover.webp)

    :material-newspaper-variant: **[n8n AI content engine](ai-content-engine.md)**

    Versioned, LLM-powered workflows for content drafting, diagram generation,
    and notification pipelines.

- ![A ceramic compute block glowing like a hearth](../assets/img/showcase/ai-agents/local-inference-cover.webp)

    :material-gpu: **[Local inference + GPU node](local-inference.md)**

    A GPU worker serving a local model through Ollama for private, offline
    inference and agent workloads.

</div>

## Platform & Operations

<div class="grid cards" markdown>

- ![The DataHub.local cluster, a seven-node mini-PC rack in a dark studio setting](../assets/img/homelab_20260920_ai.jpg)

    :material-server-network: **[Cloud-at-home on mini-PCs](cloud-at-home.md)**

    A seven-node heterogeneous Kubernetes cluster assembled, provisioned, and
    operated from Git.

- ![Concentric brass rings converging on one aligned notch](../assets/img/showcase/platform-operations/gitops-platform-cover.webp)

    :material-source-branch: **[GitOps & platform engineering](gitops-platform.md)**

    ArgoCD reconciliation, layered repositories, quality gates, and automated
    dependency updates.

- ![A macro lens over a field of faint pulses, one ringed](../assets/img/showcase/platform-operations/observability-cover.webp)

    :material-chart-line: **[Observability stack](observability.md)**

    Metrics, logs, dashboards, and enriched alerting, plus a proactive AI
    monitoring loop above the rule-based one.

</div>

## Community

<div class="grid cards" markdown>

- ![A short stack of plain shipping crates, one open with green light](../assets/img/showcase/open-source/oss-charts-cover.webp)

    :material-package-variant: **[Giving Back to the Community](oss-charts.md)**

    Five published charts and exporters: Spark apps, Garage, Servarr,
    node-exporter textfiles, and Ollama metrics.

</div>
