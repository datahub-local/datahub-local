# Lakehouse core stack

An end-to-end data lakehouse for ingestion, object storage, catalog, query,
transformation, and visualization, assembled and operated at home.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">Data &amp; Analytics</span>
  <span class="meta-pill meta-pill--status">Running</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-core">:fontawesome-brands-github: datahub-local-core</a>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-ai">:fontawesome-brands-github: datahub-local-ai</a>
</p>

<figure markdown="span">
  ![A wide dark lake surface with a wall of translucent layered strata rising from it](../assets/img/showcase/data-analytics/lakehouse-core-hero.webp){ width="1024" }
</figure>

## Problem

A data platform is a set of capabilities that only work together: a place to
land raw data, a format that supports analytics, a catalog that knows what
tables exist, an engine that can query across sources, and a transformation
layer that turns raw tables into something trustworthy. Assembling this on cloud
infrastructure is a procurement exercise. Assembling it at home means choosing
components that fit a heterogeneous cluster and wiring them so each one is
replaceable.

The goal was a lakehouse that behaves like a managed data platform. New
pipelines can be added without redesigning storage or query, and the whole thing
stays small enough to run in a home rack.

## Approach

The stack is built in layers, each with a single responsibility and a stable
interface to the next.

- **Ingestion and orchestration**: **Apache Airflow** schedules DAGs that pull
  from APIs and submit batch work, while **Spark** runs heavier transformations
  as on-demand jobs.
- **Storage**: **Garage** provides S3-compatible object storage, and lakehouse
  data is written as **Iceberg** tables so schema and snapshots are managed
  rather than treated as files.
- **Catalog**: **Apache Polaris** tracks the Iceberg tables and their versions,
  giving Trino and Spark a shared, consistent view.
- **Query**: **Trino** federates across the lakehouse and relational data, so a
  single SQL query can join Iceberg and PostgreSQL tables without moving data.
- **Transformation**: **dbt** models build staging and mart layers on top of the
  raw tables, while **dlt** handles ingestion and reverse-ETL around the edges.
- **Serving**: **Apache Superset** provides dashboards and SQL Lab over Trino,
  and **CloudNative PostgreSQL** backs the metadata-heavy services.

## Technologies

- **Apache Airflow** and **Apache Spark** for orchestration and batch processing
- **Garage S3**, **Iceberg**, and **Apache Polaris** for storage and catalog
- **Trino** for federated SQL
- **dbt** and **dlt** for transformation and ingestion
- **Apache Superset**, **CloudNative PostgreSQL**, and **Valkey** for serving and backing services

## Outcome

The lakehouse is the foundation the other data projects build on. Pipelines can
land raw data, transform it with tested, versioned models, and expose it to BI
and to agents through the same SQL surface, all on hardware owned outright. It
is the clearest expression of the site's claim: an enterprise data platform is a
set of practices, not a vendor.

## Further reading

- [Data Stack](../services/data.md): the full component descriptions
- [Semantic layer for agents](semantic-layer.md): the governed surface on top
- [Data quality & lineage](data-quality-lineage.md): how trust is enforced
