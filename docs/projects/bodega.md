# Bodega shopping analytics

Turning supermarket invoices into a structured, queryable dataset and a weekly
spend digest, described by method, schema, and aggregate outcomes only.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">Data &amp; Analytics</span>
  <span class="meta-pill meta-pill--privacy">No personal data</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-workflows">:fontawesome-brands-github: datahub-local-workflows</a>
</p>

<figure markdown="span">
  ![A blank receipt arcing across a dark studio into a receding grid of tiles](../assets/img/showcase/data-analytics/bodega-hero.webp){ width="1024" }
</figure>

<p class="project-meta__note">Method, schema, and aggregates only; no shopping rows are published.</p>

## Problem

Household spending lives in invoice emails and paper receipts spread across
supermarket loyalty accounts and photo libraries. Individually they say little.
Together they could answer practical questions: which categories cost the most,
which products are rising fastest, and how this month compares with the last.

The hard part is not the analysis. It is building a reliable pipeline from
unstructured, personal documents without ever publishing the underlying rows.

## Approach

The pipeline treats invoices as an ingestion problem and keeps a strict line
between raw personal data and published output.

- **Ingestion**: invoices are fetched from supermarket email accounts, and
  receipts photographed into Google Photos are extracted with OCR.
- **Parsing**: line items are normalized into a structured schema of store,
  product, category, quantity, unit price, line total, and purchase date.
- **Storage**: parsed rows land in **Iceberg** tables on the lakehouse, with
  history retained through the catalog.
- **Transformation**: **dbt** models aggregate spend by category, product, and
  store over time, and compute period-over-period changes.
- **Delivery**: **n8n** queries the marts through Trino and sends a weekly
  digest highlighting current spend, the products whose price rose most, and
  changes in shopping patterns.

Only the aggregation layer and the digest are shared. Raw invoices, receipt
images, and line-item rows stay private.

## Technologies

- **Apache Airflow** for scheduled ingestion and OCR
- **Iceberg on Garage S3** as the storage layer
- **dbt** for aggregation models and tests
- **Trino** for the query surface used by delivery
- **n8n** for the weekly digest and notifications

## Outcome

The dataset turns scattered receipts into a consistent spending history and an
automatic weekly summary: spend by category for the current month, the products
whose prices moved most, and shopping-pattern shifts against previous months.
What this page reports is the method and the shape of the output, never the
household's rows.

## Further reading

- [Data Stack](../services/data.md): ingestion, storage, and transformation components
- [Semantic layer for agents](semantic-layer.md): the governed surface the digest reads
