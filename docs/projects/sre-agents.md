# SRE agents (Sympozium)

Narrow, scheduled agents that investigate alerts and trends through bounded MCP
tools and report in a fixed format. They enrich the observability stack rather
than replacing it.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">AI &amp; Agents</span>
  <span class="meta-pill meta-pill--status">Running, with three ensembles</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-ai">:fontawesome-brands-github: datahub-local-ai</a>
</p>

<figure markdown="span">
  ![A wide dark terrain surveyed by drones casting thin green light cones](../assets/img/showcase/ai-agents/sre-agents-hero.webp){ width="1024" }
</figure>

## Problem

Rule-based monitoring detects conditions but cannot easily explain them.
Chronic alerts, slow trends, and missing signals fall between thresholds, and
every alert arrives without the operational context that makes it actionable.
Cloud AI could help, but the cluster's operational data is exactly the kind that
should not leave the house.

The goal was a proactive monitoring loop on local hardware that adds correlation
and context without becoming an autonomous administrator.

## Approach

Sympozium runs ensembles: groups of narrow agent personas, each with one
question, a schedule, a prompt, memory, and an allowlisted set of MCP tools.

- **Three ensembles, three trust boundaries**: `homelab-ops` performs read-only
  operational investigation, `homelab-responder` handles the human-facing
  response, and `homelab-reviewer` owns the fleet's only write action, commenting
  on pull requests.
- **One question per agent**: personas such as the SRE sentinel, endpoint
  warden, database steward, service janitor, and GitOps auditor keep tool
  selection reliable.
- **Local inference**: Ollama serves `qwen3.5:4b` on the GPU worker, and
  schedules are staggered because one GPU serves one request at a time.
- **Hard boundaries**: the agent sandbox uses gVisor and blocks shell execution,
  local file writes, delegation, and arbitrary code execution. Agents act only
  through allowlisted tools.
- **Evidence discipline**: missing data must be reported as uncertainty, never
  as a healthy result, and AI enriches detection rather than replacing
  Prometheus, AlertManager, or Robusta.

## Technologies

- **Sympozium** for ensemble and agent orchestration
- **Ollama** with a local model for inference, plus the NVIDIA device plugin
- **MCP servers** for Prometheus, Loki, Kubernetes, and repository facts
- **Prometheus**, **AlertManager**, and **Robusta** for deterministic detection
  and enrichment
- **gVisor** for sandboxing

## Outcome

The result is a second monitoring loop above the rule-based one. Prometheus
detects measurable conditions, the agents investigate trends, chronic alerts,
missing signals, and changes across nodes, and Sympozium delivers each report in
a fixed format. The design is deliberately conservative: read-only by default,
one isolated write capability, and a documented catalogue of the ways a small
model and a single GPU constrain agent reliability.

## Further reading

- [Automation services](../services/automation.md): ensembles, schedules, and boundaries
- [Monitoring](../services/monitoring.md): the observability stack and the proactive loop
- [Hard Lessons](../lessons-learned.md): what the AI monitoring experiment taught
