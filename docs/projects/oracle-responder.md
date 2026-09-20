# Ask-your-cluster oracle

A natural-language front door over cluster and repository state, for operational
questions that would otherwise mean several dashboards and a `kubectl` session.

| | |
| --- | --- |
| **Area** | AI & Agents |
| **Status** | Running |
| **Source** | [`datahub-local-ai`](https://github.com/datahub-local/datahub-local-ai) |

## Problem

Operational questions are usually cross-cutting: *why is this service
restarting, what changed recently, and has it happened before?* Answering them
means checking metrics, searching logs, inspecting workloads, and reading recent
commits. That is four tools and the judgement to link them, and it is exactly
the kind of question a language model is good at phrasing and bad at answering
from memory.

The opportunity was to let a question be asked in plain language while keeping
the answer grounded in gathered evidence.

## Approach

The oracle is the human-facing arm of the [SRE agents](sre-agents.md): the
`homelab-responder` ensemble answers questions using the same bounded MCP tools
as the scheduled investigations.

- A question becomes a bounded investigation, drawing metrics from Prometheus,
  logs from Loki, workload state from the Kubernetes API, and history from
  repositories.
- The locally served model composes an answer from the collected evidence, in a
  fixed format, rather than from recall.
- The responder has its own policy and context, separate from the read-only
  operations ensemble.
- Missing evidence is reported as uncertainty. The oracle does not paper over a
  gap with a plausible guess.

## Technologies

- **Sympozium** ensembles for the responder persona
- **MCP tools** for Prometheus, Loki, Kubernetes, and repository facts
- **Ollama** with a local model for inference
- **GitHub** history as the change record

## Outcome

The cluster can be interrogated in the way an operator actually thinks, as
questions rather than queries, and answers arrive with the evidence attached. It
is a usability layer over the observability and GitOps investments, not a new
source of truth.

## Further reading

- [Automation services](../services/automation.md): ensembles and trust boundaries
- [MCP platform](mcp-platform.md): the tool layer beneath the oracle
- [Monitoring](../services/monitoring.md): where the evidence originates
