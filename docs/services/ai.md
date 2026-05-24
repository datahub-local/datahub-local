# AI Services

DataHub.local uses a **hybrid cloud AI strategy** — two complementary providers cover different use cases, keeping costs under control without compromising capability.

| Use case | Provider |
|---|---|
| **Interactive chat & coding assistant** | Claude (Anthropic) |
| **Agents & automated workflows** | Gemini (free plan) + OpenRouter |

---

## Stack Overview

```mermaid
flowchart LR
    subgraph "Cloud Inference"
        Claude["Claude\n(Anthropic)"]
        Gemini["Google Gemini\n(free plan)"]
        OpenRouter["OpenRouter\n(multi-model gateway)"]
    end

    subgraph "Automation"
        n8n["n8n\n(AI agents & workflows)"]
        Airflow["Airflow\n(AI pipelines)"]
    end

    User["👤 User"]

    User -->|"chat / coding"| Claude
    Gemini -->|"OpenAI-compatible API"| n8n
    OpenRouter -->|"OpenAI-compatible API"| n8n
    OpenRouter -->|"OpenAI-compatible API"| Airflow
```

---

## Services

### :simple-anthropic: [Claude](https://claude.ai)

<div class="svc-tags"><span class="svc-tag">llm</span> <span class="svc-tag">chat</span> <span class="svc-tag">coding-assistant</span> <span class="svc-tag">cloud</span></div>

Primary AI assistant for interactive use: chat, pair programming, document analysis, and ad-hoc reasoning. Claude covers all interactive use cases via Claude.ai and Claude Code (CLI). It replaces what Open WebUI + Ollama would have done locally, with significantly better quality and no infrastructure overhead. Models: Claude Sonnet (default), Opus for complex tasks.

---

### :material-google: [Google Gemini](https://aistudio.google.com/)

<div class="svc-tags"><span class="svc-tag">llm</span> <span class="svc-tag">agents</span> <span class="svc-tag">cloud</span> <span class="svc-tag">free-tier</span></div>

Gemini's free plan handles the bulk of agent workloads in n8n — email summarisation, news digests, document processing, and similar high-volume, low-sensitivity tasks. The OpenAI-compatible endpoint (`https://generativelanguage.googleapis.com/v1beta/openai/`) means standard n8n AI nodes work without any custom integration. Models used: Gemini 2.0 Flash, Gemini 1.5 Flash.

---

### :material-swap-horizontal: [OpenRouter](https://openrouter.ai/)

<div class="svc-tags"><span class="svc-tag">llm</span> <span class="svc-tag">gateway</span> <span class="svc-tag">multi-model</span> <span class="svc-tag">cloud</span></div>

Multi-model gateway used as overflow and fallback when Gemini free-tier limits are hit. The **Banana routing tier** keeps per-token spend predictable. A single API key, built-in budget caps, and a unified OpenAI-compatible endpoint make it easy to swap between Gemini direct and OpenRouter without changing any workflow logic.

**Why OpenRouter alongside direct Gemini?**

- Hard budget caps prevent surprise spend
- Seamless fallback — same model family, no prompt changes needed
- Single key covers multiple model families if requirements grow

---

### :material-robot-happy: [n8n AI Agents](https://n8n.io/)

<div class="svc-tags"><span class="svc-tag">ai-agents</span> <span class="svc-tag">automation</span> <span class="svc-tag">llm</span> <span class="svc-tag">workflows</span></div>

n8n hosts all AI agent workflows, combining AI nodes (AI Agent, OpenAI → Gemini/OpenRouter, LangChain, embeddings, vector stores) with real-world integrations. Workflows are stored in [datahub-local-workflows/n8n/](https://github.com/datahub-local/datahub-local-workflows).

**Example workflows:**

- 📧 **Email summarisation** — classify and summarise incoming emails
- 📰 **News digest** — fetch RSS feeds (via CommaFeed), summarise, send daily briefing to Slack
- 📄 **Document processing** — extract structured data from PDFs using LLM + regex
- 🔔 **Alert enrichment** — take Prometheus alerts, query Loki for logs, generate root cause hypotheses
- 🏠 **Home automation** — integrate with Home Assistant events and produce natural-language status reports
