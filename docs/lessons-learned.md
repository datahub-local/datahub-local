# Lessons Learned

Building a homelab is as much about learning from failures as it is about getting things working. This page documents the honest account of what didn't work, why it was abandoned, and what was learned from each experience — both for future reference and as a portfolio signal that real engineering involves iteration and pragmatism.

---

## :material-server-off: Homelab Reliability

**What was tried:** Running critical workloads on a cluster of consumer ARM SBCs (OrangePi boards) with the expectation of close-to-cloud reliability.

**What went wrong:**

- **Device unreliability** — SBCs are consumer electronics, not server-grade hardware. SD card corruption, power irregularities, and thermal issues caused unexpected node failures.
- **Provider quality** — firmware support, kernel updates, and community documentation for ARM SBCs vary enormously. Some issues had no reliable fix; workarounds led to fragile configs.
- **No clear scope** — without a deliberate plan for what the homelab was for, it grew into an unmanageable web of services. Each new thing added was another point of failure and maintenance burden.
- **Home automation** — running Home Assistant and other home automation tools in the cluster seemed logical but caused more friction than it solved: the cluster going down for maintenance meant lights stopped working. Tight coupling between infrastructure and daily life is a bad design.

**Lesson:** Define the homelab's purpose before adding things. Keep life-critical automations (lights, heating) on dedicated, separate hardware. Server-grade mini-PCs are far more reliable than SBCs for always-on workloads.

---

## :material-television-off: Servarr / Self-Hosted Media

**What was tried:** A full Servarr stack (Jellyfin, Sonarr, Radarr, Prowlarr, qBittorrent, Bazarr) for self-hosted media management and streaming.

**What went wrong:**

- **Network blocking** — the home ISP blocked common torrent ports and flagged traffic, making the download pipeline unreliable without constant workarounds.
- **Content gaps** — non-English content, audiobooks, and niche media were hard or impossible to find. The mainstream media libraries that Servarr handles well were already well-served by existing streaming subscriptions.
- **Maintenance overhead** — keeping indexers, download clients, and the *arr apps in sync required frequent manual intervention. Prowlarr configs broke, indexers went offline, update cycles conflicted.
- **Resource cost** — Jellyfin transcoding is expensive on ARM. The OrangePi nodes struggled with 1080p transcoding, and the complexity of making it work wasn't worth the payoff.

**Lesson:** Self-hosted media works well when your ISP is cooperative and your content needs are mainstream. For niche or non-English content, streaming services remain the pragmatic choice. The [`servarr`](open-source/index.md) Helm chart was published as a usable artifact from this experiment.

---

## :material-cpu-64-bit: ARM Servers for Production Workloads

**What was tried:** Building the entire cluster on OrangePi 5B boards (ARM64, RK3588, 16 GB RAM) as cost-effective worker nodes.

**What went wrong:**

- **Performance gap** — for data-heavy workloads (Spark transformations, Trino queries, LLM inference), the ARM boards were significantly slower than equivalent x86 hardware. The RK3588 is impressive for a SBC but does not compete with a dedicated mini-PC on raw throughput.
- **Cost efficiency** — when total cost of ownership is considered (SD cards, NVMe drives, cases, power supplies, reliability overhead), a single x86 mini-PC at a similar or lower price delivered 3–5× the usable compute.
- **Software compatibility** — not all container images have ARM64 variants. Building custom images or waiting for upstream ARM64 support added friction and slowed iteration.
- **Kernel / firmware issues** — custom kernels, device tree blobs, and OrangePi-specific patches meant OS updates were riskier than on standard x86 hardware.

**Lesson:** ARM SBCs are excellent for learning, tinkering, and lightweight services. For a production-like data platform with real workloads, x86 mini-PCs (e.g. CHUWI UBox, CWWK X86-P5) offer far better performance-per-euro and far less operational pain. The cluster now uses ARM nodes for low-demand services and control plane, and x86 for compute-heavy workloads.

---

## :material-home-off: Under-Used Self-Hosted Services

**What was tried:** Self-hosting a broad set of personal productivity and home apps — Home Assistant, Mealie (recipe manager), and various others — under the assumption that self-hosted = better.

**What went wrong:**

- **Usage never materialised** — apps like Mealie sat mostly unused after an initial setup burst. The friction of a self-hosted tool vs. a polished commercial app was too high for daily personal use.
- **Maintenance doesn't scale** — every self-hosted app is another thing that can break, needs updates, and requires attention. For apps that don't provide real value, the maintenance cost isn't justified.
- **Home Assistant coupling** — see the homelab reliability note above. Running HA inside the Kubernetes cluster meant any cluster maintenance broke home automations. The wrong layer for something that needs to be always-on.

**Lesson:** Self-host services where the value is clear — data platform tools, developer tools, privacy-sensitive services, tools used daily. Don't self-host for ideological reasons alone. A good heuristic: if you haven't used it in two weeks, remove it. Quality over quantity.

---

## :material-package-variant-remove: Open Source Vendor Risk

**What was tried:** Relying on Helm charts and software maintained by companies that also have a commercial product — under the assumption that popular open-source projects are stable long-term dependencies.

**What went wrong, one incident at a time:**

### Bitnami chart removal (PostgreSQL & Redis)

Bitnami provided the de-facto standard Helm charts for stateful services. Almost every Kubernetes tutorial linked to them. One day, without much warning, Bitnami restructured their chart repository and removed a large number of charts from the old location.

The impact was significant: automated ArgoCD syncs started failing, and the migration path required:
1. Provisioning replacement charts (CloudNative PG for PostgreSQL, switching Redis to Valkey)
2. Dumping data from the running instances
3. Restoring into the new chart's schema and storage layout

Migrating stateful services in Kubernetes is painful. Postgres data dumps are manageable but stressful under time pressure; recovering from a failed migration mid-way is worse.

**Lesson:** Never depend on a single company's Helm chart for a critical stateful service. Prefer operator-based deployments (CloudNative PG, Strimzi) which are governed by community foundations and less likely to disappear overnight.

### Redis → Valkey

Redis Labs changed the Redis license to SSPL (not OSI-approved open source), effectively ending community distribution. The OpenValkey fork (`Valkey`) was created by the community almost immediately and is now the drop-in replacement under an OSI license.

In practice this was a smooth migration — the API is identical — but it required monitoring the license situation, making a decision, and updating all chart references before the Docker Hub images were removed.

**Lesson:** Watch license changes on core infrastructure dependencies. Community forks of widely-used tools happen quickly and are usually production-ready.

### MinIO removal — the worst one

MinIO was the clear leader in self-hosted S3-compatible object storage. It had the best documentation, the most integrations, and near-universal support in the data ecosystem (Spark, Trino, Airflow all listed it first in their docs).

Then MinIO changed its license and removed the open-source container images from Docker Hub with very short notice — less than 6 months from announcement to removal.

The timing was bad: the migration was delayed because MinIO seemed stable and the urgency wasn't obvious. By the time the removal date was close, it became a forced, rushed migration.

**Alternatives evaluated:**

| Option | Why rejected |
|--------|-------------|
| **Ceph** | Powerful but operationally complex — Ceph is practically a full-time job to run on a small cluster |
| **RustFS** | Promising but very new and not production-proven at the time |
| **SeaweedFS** | Good performance but the operational model and documentation were harder to follow |
| **Garage** | ✅ Chosen — single static binary, simple cluster model, low resource use, great fit for heterogeneous hardware |

Garage was the right choice but the official Helm chart was bare: no automatic cluster initialisation, no bucket or API key provisioning, and limited observability. A fork was created adding:

- Automatic cluster layout and node assignment on first deploy
- Bucket and key provisioning from `values.yaml`
- `ServiceMonitor` and Grafana dashboard out of the box
- Flexible ingress support

This became the [`garage-helm`](open-source/index.md) project, now published open source.

**Lesson:** For object storage (and any storage layer), choose software governed by a neutral foundation or a true community project — not a single commercial entity's "open core" product. Evaluate migration cost before you're forced to migrate.

---

## :material-check-all: What These Failures Produced

Every failure above contributed something concrete:

| Failure | What came out of it |
|---------|-------------------|
| ARM reliability issues | Clearer architecture: ARM for light workloads, x86 for data/AI compute |
| Servarr struggles | Published [`servarr`](open-source/index.md) Helm chart — useful for others even if not for this cluster |
| ARM cost/performance | Hardware evolution to CWWK NAS + CHUWI mini-PC; much better cluster performance |
| Under-used services | Leaner cluster; focus on services that are actually used — data platform, AI, monitoring |
| Over-scoping | Clear purpose statement: this is a **data platform and AI experimentation lab**, not a general home server |
| Bitnami removal | Migrated to operator-based deployments (CloudNative PG); more resilient chart strategy |
| MinIO removal | Built and published [`garage-helm`](open-source/index.md); Garage now running in production |
| Redis relicensing | Early adoption of Valkey; no disruption to services |

The current cluster is more focused, more reliable, and more interesting as a portfolio project precisely because of what was cut — and because of the fires that had to be fought along the way.
