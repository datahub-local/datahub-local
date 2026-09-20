---
description: "Maintain platform facts (nodes, hardware, topology) against the cluster"
---

Maintain the platform domain: cluster nodes, hardware classes, roles, and
namespace topology, cross-checked between the bootstrap inventory and the live
cluster.

Use the `platform-maintainer` skill and follow it exactly. It owns the checks,
the record-versus-cluster rule, and the publish step. It requires `kubectl`
access and fails loudly when the cluster is unreachable.
