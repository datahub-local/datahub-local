# Data quality & lineage

Tests, snapshots, and a versioned catalog that make the lakehouse's tables
trustworthy rather than merely present.

| | |
| --- | --- |
| **Area** | Data & Analytics |
| **Status** | Running |
| **Source** | [dbt and Iceberg projects](https://github.com/datahub-local/datahub-local-ai) |

## Problem

A pipeline that runs on schedule is not the same as one you can trust. Silent
failures are the expensive kind: an upstream API changes shape, a join drops
rows, a column quietly becomes null, and a dashboard reports a confident wrong
number. Without lineage, the first symptom is a bad decision.

The lakehouse needed the same quality discipline an enterprise applies:
assertions on data, and a way to see how a table came to be.

## Approach

Quality is enforced at the transformation layer and preserved at the storage
layer, so checks live where the logic does and history lives where the data does.

- **dbt tests** assert expected properties such as uniqueness, not-null,
  accepted values, and relationships between models. They fail the pipeline when
  a contract breaks rather than publishing a bad mart.
- **Modeled, layered transformations** make lineage explicit. Every mart can be
  traced back through staging to the raw source, so the origin of a number is a
  matter of reading the models, not guessing.
- **Iceberg snapshots** keep each table's history, so a bad write can be
  reasoned about against the version before it.
- **Polaris cataloging** keeps the authoritative list of tables and their
  versions consistent across query engines.

## Technologies

- **dbt** tests and model graph
- **Iceberg** table snapshots
- **Apache Polaris** catalog
- **Trino** for validating and querying results
- **Apache Airflow** for scheduled runs and failure surfacing

## Outcome

Broken assumptions fail loudly at the model that introduces them instead of
surfacing as an anomaly weeks later, and every published table has a traceable
path back to its source. It is a modest amount of tooling for a large change in
how much the platform's numbers can be trusted.

## Further reading

- [Data Stack](../services/data.md): the transformation and storage components
- [Semantic layer for agents](semantic-layer.md): the surface the tests protect
- [Lakehouse core stack](lakehouse-core.md): the platform these checks run on
