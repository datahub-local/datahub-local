# Vendor-risk lessons

Three open-source licensing incidents, from Bitnami, Redis, and MinIO, and the
operational habits that came out of surviving them.

| | |
| --- | --- |
| **Area** | Open Source & Lessons |
| **Status** | Retold from experience |
| **Source** | [Lessons Learned](../lessons-learned.md) |

## Problem

Popular open-source infrastructure feels like a safe dependency. In practice it
can be an "open core" product owned by a single company, and that company can
change the license and remove distribution with little warning. For a platform
built largely from such components, that is an availability risk dressed up as a
convenience.

Three incidents made the risk concrete.

## Approach

Each incident was handled, then mined for the general lesson and turned into a
policy.

- **Bitnami chart removal (PostgreSQL, Redis).** Charts vanished from their
  former location and automated syncs broke. The migration moved to
  operator-based deployments: **CloudNative PostgreSQL** for Postgres and
  **Valkey** for Redis, both governed by community foundations rather than a
  single vendor.
- **Redis relicensing (SSPL).** The license stopped being OSI-approved, so the
  community fork **Valkey** was adopted early as a drop-in replacement before
  images were removed.
- **MinIO image removal.** The S3-compatible object store used across Spark,
  Trino, and Airflow changed license and pulled its open-source images. After
  evaluating Ceph, RustFS, SeaweedFS, and Garage, **Garage** was chosen and the
  [`garage-helm`](oss-charts.md) chart was built to fill its gaps.

The general habits: prefer foundation-governed or true-community projects for
stateful layers, watch license changes on core dependencies, and evaluate
migration cost before it is forced.

## Technologies

- **CloudNative PostgreSQL**, **Valkey**, and **Garage** as the resulting stack
- **ArgoCD** and **Helm** as the delivery path that made breakage visible
- **Kopia** and **Velero** as the backups that made migration survivable

## Outcome

The platform is now built on dependencies chosen for governance as much as
features, and the migrations produced two of its published projects. The deeper
result is a habit: treat the license and the owner of a critical component as
first-class operational facts, not fine print.

## Further reading

- [Lessons Learned](../lessons-learned.md): the full account of each incident
- [Published OSS Helm charts](oss-charts.md): what the migrations produced
- [Data Stack](../services/data.md): where Garage and Valkey now run
