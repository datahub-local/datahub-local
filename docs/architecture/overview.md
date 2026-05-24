# Architecture Overview

This page describes the logical and physical cluster architecture, storage design, observability, and the GitOps deployment pipeline that powers DataHub.local.

---

## General

High-level view of the cluster: how nodes, networking, and storage components relate to each other.

```mermaid
graph TB
    classDef internet fill:#1A237E,color:#fff,stroke:#3F51B5,stroke-width:2px
    classDef control fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef armWorker fill:#2E7D32,color:#fff,stroke:#66BB6A,stroke-width:2px
    classDef amdWorker fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef network fill:#00695C,color:#fff,stroke:#26C6DA,stroke-width:2px
    classDef storage fill:#E65100,color:#fff,stroke:#FFA726,stroke-width:2px

    subgraph Internet
        DNS["🌍 External DNS"]:::internet
        GHCR["📦 GitHub Container Registry"]:::internet
    end

    subgraph "Home Network"
        Router["🏠 Home Router"]:::network

        subgraph "K3s Cluster"
            subgraph "Control Plane"
                CP["🎛️ orpi-0\nOrangePi 4 LTS"]:::control
            end

            subgraph "ARM64 Workers"
                W1["🟠 orpi-1\nOrangePi 5B 16G"]:::armWorker
                W2["🟠 orpi-2\nOrangePi 5B 16G"]:::armWorker
                W3["🟠 orpi-3\nOrangePi 5B 16G"]:::armWorker
            end

            subgraph "AMD64 Workers"
                W4["🔵 amd-1\nCHUWI UBox 32G"]:::amdWorker
                W5["💾 nas\nCWWK X86-P5 N305"]:::amdWorker
                W6["💻 laptop\nLenovo Legion WSL2"]:::amdWorker
            end

            subgraph "Networking"
                Traefik["🔀 Traefik\nIngress"]:::network
                Tailscale["🔒 Tailscale\nVPN"]:::network
            end

            subgraph "Storage"
                Longhorn["💾 Longhorn\nDistributed Block"]:::storage
                Garage["🪣 Garage\nS3 Object Store"]:::storage
                NFS["📁 NFS\nNAS Shares"]:::storage
            end
        end
    end

    Router --> Traefik
    Traefik --> CP
    CP --> W1 & W2 & W3 & W4 & W5 & W6
    Longhorn --> W1 & W2 & W3
    Garage --> W1 & W2 & W3
    NFS --> W5
    DNS --> Router
```

---

## Physical Layout

The cluster is a **heterogeneous mix of ARM64 and AMD64** machines — an OrangePi SBC for the control plane, OrangePi 5B boards as initial workers, and x86 mini-PCs that have progressively replaced them for better performance-per-euro.

```mermaid
graph TB
    classDef control fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef armNode fill:#2E7D32,color:#fff,stroke:#66BB6A,stroke-width:2px
    classDef amdNode fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef netNode fill:#00695C,color:#fff,stroke:#26C6DA,stroke-width:2px

    UPS["⚡ CyberPower UPS\nPower Protection"]:::netNode
    SW["🌐 HORACO 2.5GbE\nManaged Switch"]:::netNode

    CP["🎛️ datahublocal-orpi-0\nOrangePi 4 LTS · 4 GB\nARM64 RK3399 · Control Plane"]:::control

    W1["🟠 datahublocal-orpi-1\nOrangePi 5B · 16 GB\nARM64 RK3588\nWorker · Longhorn · Garage"]:::armNode
    W2["🟠 datahublocal-orpi-2\nOrangePi 5B · 16 GB\nARM64 RK3588\nWorker · Longhorn · Garage"]:::armNode
    W3["🟠 datahublocal-orpi-3\nOrangePi 5B · 16 GB\nARM64 RK3588\nWorker · Longhorn · Garage"]:::armNode

    W4["🔵 datahublocal-amd-1\nCHUWI UBox · 32 GB\nAMD Ryzen 5 6600H\nHeavy Compute Worker"]:::amdNode
    W5["💾 datahublocal-nas\nCWWK X86-P5 N305 · 16 GB\n3×1 TB HDD RAID + 128 GB NVMe\nNAS Worker · Garage S3 · NFS"]:::amdNode
    W6["💻 datahublocal-legion-laptop\nLenovo Legion · AMD64\nWSL2 · Dev Worker"]:::amdNode

    UPS --> SW
    SW --> CP
    SW --> W1
    SW --> W2
    SW --> W3
    SW --> W4
    SW --> W5
    SW --> W6
```

### Cluster Nodes

| Node | Hardware | Role | CPU Arch | OS |
|------|----------|------|----------|----|
| `datahublocal-orpi-0` | OrangePi 4 LTS (4 GB) | Control Plane | ARM64 (RK3399) | Debian 13 |
| `datahublocal-orpi-1` | OrangePi 5B (16 GB) | Worker | ARM64 (RK3588) | Debian 13 |
| `datahublocal-orpi-2` | OrangePi 5B (16 GB) | Worker | ARM64 (RK3588) | Debian 13 |
| `datahublocal-orpi-3` | OrangePi 5B (16 GB) | Worker | ARM64 (RK3588) | Debian 13 |
| `datahublocal-amd-1` | CHUWI UBox (AMD 6600H, 32 GB) | Worker | AMD64 | Debian 13 |
| `datahublocal-nas` | CWWK X86-P5 (N305, 16 GB, RAID 3×1TB + 128 GB NVMe) | NAS + Worker | AMD64 | Debian 12 |
| `datahublocal-legion-laptop` | Lenovo Legion laptop | Dev + Worker | AMD64 (WSL2) | Ubuntu 24.04 |

**Kubernetes distribution:** K3s v1.36 (lightweight, production-ready)  
**Container runtime:** containerd 2.2

> **Architecture evolution:** The cluster started ARM-only with OrangePi 5B boards, but over time x86 mini-PCs proved significantly more cost-effective for compute-heavy workloads (Spark, Trino). The ARM nodes remain useful for lightweight services and multi-arch testing — see [Lessons Learned](../lessons-learned.md) for more context.

---

## Namespace Layout

Services are organized into **namespaces by concern**, each managed as a separate ArgoCD Application:

| Namespace | Contents |
|-----------|----------|
| `kube-system` | K3s system components, Traefik, Longhorn CSI, cert-manager, ExternalDNS, reloader, reflector, snapshot-controller, NVIDIA plugin |
| `automation` | ArgoCD, n8n, Velero, Kopia backup agents |
| `data` | Airflow, Trino, Superset, Redpanda, Nessie, Spark, PostgreSQL, Garage, Ollama, Open WebUI, Valkey |
| `monitoring` | Prometheus, AlertManager, Grafana, Loki, Promtail, Robusta, Speedtest exporter |
| `security` | cert-manager, Dex (OIDC), OAuth2-proxy, Tailscale |
| `media` | CommaFeed (RSS), MusicGrabber |
| `other` | Homepage dashboard, ConvertX, IT Tools, Mazanoke, Omni Tools, Stirling PDF |

---

## Networking & Access

| Method | Use Case |
|--------|----------|
| **Traefik IngressRoutes** | Internal HTTP/HTTPS routing for all web UIs (Grafana, Superset, ArgoCD, etc.) |
| **Tailscale VPN** | Secure remote access from anywhere — no port forwarding needed |
| **ExternalDNS** | Automatically manages DNS records for exposed services |
| **cert-manager** | Automatic TLS certificates via Let's Encrypt |
| **OAuth2-proxy + Dex** | SSO authentication for all web services using OIDC |

---

## Storage

Storage is split by access pattern and cost profile — fast NVMe for latency-sensitive workloads, spinning HDD RAID for bulk data that doesn't need IOPS.

| Tier | Technology | Backing hardware | Use case |
|------|-----------|-----------------|----------|
| **High-performance block** | Longhorn | NVMe SSDs on OrangePi 5B nodes | Stateful apps that need low latency: PostgreSQL, Redpanda, Valkey — replicated across nodes for HA |
| **High-capacity object (S3)** | Garage | NVMe SSD on CWWK NAS | Data lake (Iceberg tables, Spark outputs, Loki logs, backups) — fast random reads for analytics workloads without the cost of full NVMe replicas across every node |
| **Bulk shared filesystem** | NFS (CWWK NAS RAID) | 3×1 TB HDD RAID | Large sequential files: media library, raw data exports, archives — big and cheap, latency-tolerant |

> **Design principle:** Put the _right_ data on the _right_ storage. Longhorn replicas on NVMe make PostgreSQL snappy; Garage on a single NVMe NAS node is fast enough for object storage at a fraction of the cost; HDD RAID covers everything that just needs capacity.

---

## Observability

All services expose Prometheus metrics via `ServiceMonitor` resources. Logs are shipped via Promtail to Loki. Alerts flow from Prometheus AlertManager to notification channels.

```mermaid
flowchart LR
    classDef source fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef collector fill:#2E7D32,color:#fff,stroke:#66BB6A,stroke-width:2px
    classDef store fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef alerting fill:#B71C1C,color:#fff,stroke:#EF5350,stroke-width:2px
    classDef viz fill:#00695C,color:#fff,stroke:#26C6DA,stroke-width:2px
    classDef notify fill:#E65100,color:#fff,stroke:#FFA726,stroke-width:2px

    Pods["📦 All Pods\n(metrics + logs)"]:::source
    NodeExporter["📊 Node Exporter\n(per node)"]:::collector
    Promtail["📋 Promtail\n(log shipper)"]:::collector
    Prometheus["🔥 Prometheus\n(metrics)"]:::store
    Loki["🗃️ Loki\n(logs)"]:::store
    AlertManager["🚨 AlertManager"]:::alerting
    Grafana["📈 Grafana\n(dashboards)"]:::viz
    Robusta["🤖 Robusta\n(K8s monitoring)"]:::alerting
    Notifications["📲 Slack / Email"]:::notify

    Pods --> Promtail
    Pods --> NodeExporter
    NodeExporter --> Prometheus
    Promtail --> Loki
    Prometheus --> AlertManager
    Prometheus --> Grafana
    Loki --> Grafana
    AlertManager --> Robusta
    Robusta -->|"enriched alerts"| Notifications
```

---

## GitOps

Everything in the cluster is managed as code. No manual `kubectl apply` for services — all changes flow through Git.

```mermaid
flowchart LR
    classDef dev fill:#1565C0,color:#fff,stroke:#42A5F5,stroke-width:2px
    classDef bootstrap fill:#2E7D32,color:#fff,stroke:#66BB6A,stroke-width:2px
    classDef secrets fill:#B71C1C,color:#fff,stroke:#EF5350,stroke-width:2px
    classDef core fill:#4527A0,color:#fff,stroke:#9575CD,stroke-width:2px
    classDef workflow fill:#00695C,color:#fff,stroke:#26C6DA,stroke-width:2px
    classDef cluster fill:#E65100,color:#fff,stroke:#FFA726,stroke-width:2px

    Dev["👨‍💻 Developer / Me\n(git push)"]:::dev

    subgraph "Bootstrap Layer"
        Ansible["datahub-local-bootstrap\n(Ansible)\n• Install K3s\n• Configure OS\n• Deploy ArgoCD"]:::bootstrap
    end

    subgraph "Secrets Layer"
        Secrets["datahub-local-secrets\n(Private)\n• Encrypted secrets\n• API keys\n• Credentials"]:::secrets
    end

    subgraph "Core Layer"
        Core["datahub-local-core\n(Helmfile)\n• ApplicationSets\n• All services\n• 7 namespaces"]:::core
    end

    subgraph "Workflow Layer"
        Workflows["datahub-local-workflows\n• n8n flows\n• Airflow DAGs\n• SQLMesh models"]:::workflow
    end

    subgraph "K3s Cluster"
        ArgoCD["🔄 ArgoCD\n(GitOps controller)"]:::cluster
        Services["🚀 Running Services\n(Pods, Deployments,\nStatefulSets)"]:::cluster
    end

    Dev -->|"1. provision"| Ansible
    Ansible -->|"2. installs"| ArgoCD
    Secrets -->|"3. sync"| ArgoCD
    Core -->|"4. sync"| ArgoCD
    Workflows -->|"5. sync"| ArgoCD
    ArgoCD -->|"reconciles"| Services
```

### Deployment Flow

1. **Bootstrap** — Ansible provisions OS on bare metal, installs K3s, and deploys ArgoCD as the first application.
2. **Secrets** — ArgoCD syncs `datahub-local-secrets` (private repo) to deploy encrypted secrets into the `security` namespace.
3. **Core** — ArgoCD syncs `datahub-local-core`, which contains Helmfile-based ApplicationSets that expand into one Application per namespace × service.
4. **Workflows** — n8n flow JSONs, Airflow DAG Python files, and SQLMesh models are synced from `datahub-local-workflows`.
5. **Reconciliation** — ArgoCD continuously watches all repos and auto-syncs on any commit to `HEAD`.
