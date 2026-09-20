# MCP platform

Bounded, read-only fact-gathering tools that let local AI agents inspect the
cluster without handing them an unrestricted `kubectl` or Grafana session.

| | |
| --- | --- |
| **Area** | AI & Agents |
| **Status** | In progress, with the first implementation running |
| **Source** | [`datahub-local-ai/agents/mcp`](https://github.com/datahub-local/datahub-local-ai) |

## Problem

An agent is only as trustworthy as the facts it gathers. The easy path, giving a
model API keys to Prometheus, Loki, and the Kubernetes API, fails in practice.
A small local model with a large, similarly named tool surface makes unreliable
choices, and a mutating tool one hallucination away from the cluster is a safety
problem, not a convenience.

The platform already had the data: metrics in Prometheus, logs in Loki,
workload state in the Kubernetes API, and tables in Trino. What it lacked was a
narrow, explicit contract between that data and the agents.

## Approach

A dedicated MCP (Model Context Protocol) server exposes a small set of
purpose-named tools, one server per data source, and agents are restricted to
explicit allowlists rather than a general-purpose administrator surface.

- Each server answers one kind of question: query metrics, search logs, inspect
  workloads, or run SQL. Tool names describe intent rather than API shape.
- The operations path is read-only. Any mutating capability is a separate policy
  decision, not an inferred action.
- Tool names and arguments are verified against the live server, because a
  plausible-looking tool that returns nothing is worse than a missing one.

## Technologies

- **Model Context Protocol** server implementation in `datahub-local-ai`
- **Prometheus** and **Loki** for metrics and logs
- **Kubernetes API** with bounded, allowlisted operations
- **Trino**, **Polaris**, and **Garage** for lakehouse inspection
- **Sympozium** as the agent runtime that consumes the tools

## Outcome

The MCP servers give agents a verifiable evidence path instead of open cluster
access. They are the fact-gathering layer beneath the [SRE agents](sre-agents.md):
agents ask one bounded question, collect evidence from named tools, and report,
with missing data surfaced as uncertainty rather than converted into a healthy
result. The next step recorded on the landing is wider tool coverage with every
mutation gated behind explicit policy and approval.

## Further reading

- [Automation services](../services/automation.md): how agents, ensembles, and MCP tools fit together
- [AI & LLMs](../services/ai.md): the inference stack the agents run on
- [Monitoring](../services/monitoring.md): the proactive monitoring loop
