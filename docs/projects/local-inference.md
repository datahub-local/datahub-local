# Local inference + GPU node

Private, offline inference on a dedicated GPU worker, used by the platform's
agents and available through a self-hosted chat UI.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">AI &amp; Agents</span>
  <span class="meta-pill meta-pill--status">Running</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-core">:fontawesome-brands-github: datahub-local-core</a>
</p>

<figure markdown="span">
  ![A dark room with a warm ceramic block pooling green light on the floor](../assets/img/showcase/ai-agents/local-inference-hero.webp){ width="1024" }
</figure>

## Problem

Not every AI workload can go to a cloud API. Operational data is sensitive, some
work must be available offline, and paying per token for routine tasks is hard
to justify when the hardware is already on the shelf. At the same time, a single
small GPU cannot serve everything, so a realistic strategy has to decide what
runs locally and what does not.

## Approach

The platform uses a hybrid strategy rather than a single provider, and runs the
local half on a purpose-chosen node.

- **A GPU worker**: a Lenovo Legion with an RTX 3060M is dedicated to inference.
  The NVIDIA device plugin advertises the GPU, so only workloads that request it
  are scheduled there.
- **Ollama** serves a local model (`qwen3.5:4b`) used by the [SRE
  agents](sre-agents.md) and available through **Open WebUI** for private chat.
- **Cloud models** cover interactive and high-volume work where capability or
  throughput matters more than locality: Claude for interactive assistance, and
  Gemini and OpenRouter for automation.
- **Budget control**: cloud access runs behind hard caps, and local inference
  absorbs the workloads that do not need a frontier model.

## Technologies

- **Ollama** and **Open WebUI** for local serving and private chat
- **NVIDIA device plugin** for GPU scheduling on Kubernetes
- **Claude**, **Google Gemini**, and **OpenRouter** for the cloud half of the strategy
- **`ollama-metrics`**, a published exporter giving inference observability

## Outcome

Sensitive and routine inference runs at home with no per-token cost, while cloud
models are used deliberately where they add capability. The GPU node is a
shared, contended resource, a constraint that shaped how agents are scheduled,
but it makes genuinely private AI a first-class part of the platform rather than
a demo.

## Further reading

- [AI & LLMs](../services/ai.md): the hybrid strategy in full
- [Monitoring](../services/monitoring.md): inference metrics and the observability stack
- [OSS charts](oss-charts.md): the `ollama-metrics` exporter
