# Personal finance datalake

A private analytics pipeline over personal documents such as bank exports,
statements, and spreadsheets, with a governed SQL surface and no source rows
published.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">Data &amp; Analytics</span>
  <span class="meta-pill meta-pill--privacy">No personal data</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-ai">:fontawesome-brands-github: datahub-local-ai</a>
</p>

<figure markdown="span">
  ![A wall of closed frosted drawers in a dark room, one lit from within](../assets/img/showcase/data-analytics/personal-finance-hero.webp){ width="1024" }
</figure>

<p class="project-meta__note">Method, schema, and aggregates only; no transactions or balances are published.</p>

## Problem

Personal finance data is sensitive, inconsistent, and spread across formats:
bank exports, statements, and hand-maintained spreadsheets. Existing tools
either require handing the data to a third party or lock analysis behind a
closed product. The goal was to own the pipeline end to end and keep the data
inside the cluster.

The privacy constraint shapes every decision. The pipeline must be useful for
questions about trends and categories while guaranteeing that no individual
transaction is ever published.

## Approach

The pipeline treats personal documents as another data source and applies the
same lakehouse discipline used for the platform's workloads.

- **Ingestion**: a gateway syncs files from personal Google Drive into object
  storage, alongside exported statement files.
- **Normalization**: **dlt** loads the raw files, and a schema standardizes
  dates, descriptions, amounts, categories, and accounts while preserving a link
  back to the source document.
- **Storage**: normalized records are stored as **Iceberg** tables, with the
  catalog retaining history.
- **Modelling**: **dbt** models build categories, monthly aggregates, and
  period-over-period comparisons on top of the transaction grain.
- **Access**: **Trino** and **Superset** provide SQL and dashboards over the
  aggregates, while the raw grain stays behind the privacy boundary.

As with [Bodega](bodega.md), the published artifacts describe the method and the
schema. No transactions, balances, or account details appear on this site or in
its assets.

## Technologies

- **S3-GDrive gateway** for getting personal documents into object storage
- **dlt** for ingestion and normalization
- **Iceberg on Garage S3** for storage
- **dbt** for modeled aggregates and tests
- **Trino** and **Apache Superset** for the query and dashboard surface

## Outcome

Personal finance analysis now runs on the same platform as the rest of the data
estate: versioned transformations, a governed query surface, and dashboards that
answer category and trend questions. The system shows that a sensitive workload
can be analysed rigorously without the data leaving the cluster and without any
of it being published.

## Further reading

- [Data Stack](../services/data.md): the platform components used here
- [Semantic layer for agents](semantic-layer.md): how the governed surface is built
