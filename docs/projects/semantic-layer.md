# Semantic layer for agents

A catalogued, versioned SQL surface over the lakehouse, so dashboards and AI
agents query the same governed definitions instead of raw object storage.

| | |
| --- | --- |
| **Area** | Data & Analytics |
| **Status** | Running |
| **Source** | [dbt and dlt projects in `datahub-local-ai`](https://github.com/datahub-local/datahub-local-ai) |

## Problem

Raw Iceberg tables in object storage are a poor interface. Column names drift,
transformation logic is duplicated between pipelines, and anything querying the
lakehouse, whether a dashboard, a notebook, or an agent, has to know the
physical layout. AI agents make this worse: they have no tolerance for ambiguity
in a schema, and an incorrect assumption produces a confident wrong answer.

The platform needed one stable, documented query surface that sits above
storage and below consumers.

## Approach

The semantic layer is built from existing lakehouse components rather than a new
product. Models define the meaning, a catalog tracks the state, and a query
engine serves it.

- **dbt** models turn raw and staging tables into marts with explicit names and
  tests, so the transformation from source to metric is version-controlled.
- **Apache Polaris** catalogs the Iceberg tables and versions their state, which
  allows changes to be branched and traced rather than applied in place.
- **Trino** serves the resulting tables over SQL and federates them with
  relational sources, so a consumer joins lakehouse and database tables in one
  query.
- An **MCP Trino tool** lets agents run bounded SQL against the same surface,
  closing the loop with [MCP platform](mcp-platform.md).

## Technologies

- **dbt** for modeled, tested transformations
- **Apache Polaris** and **Iceberg** for catalog and table versioning
- **Trino** for federated SQL
- **Apache Superset** for BI on the same tables
- **Apache Airflow** to schedule model runs

## Outcome

Consumers now address the data by name and meaning, not by storage path. BI
dashboards and AI agents share one surface, table history is versioned through
the catalog, and a model change is a reviewed commit rather than a manual
correction. The layer is the reason the other data projects, including
[Bodega](bodega.md) and [personal finance](personal-finance.md), can expose
results without exposing their pipelines.

## Further reading

- [Data Stack](../services/data.md): the full lakehouse this layer sits on
- [Data quality & lineage](data-quality-lineage.md): how tests and versioning are applied
