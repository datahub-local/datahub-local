---
description: "Maintain service and version facts against the deployed stack"
---

Maintain the service domain: which services exist and their versions, including
Helm chart and container image versions, cross-checked between the core versions
file and the live cluster.

Use the `service-maintainer` skill and follow it exactly. It owns the checks, the
record-versus-cluster rule, and the publish step. It requires `kubectl` and
`helm` access.
