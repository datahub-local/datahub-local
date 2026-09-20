# CLAUDE.md

Guidance for working in this repository.

## Writing style

### Do not use em dashes to join thoughts

Em dashes (`—`) are the easiest tell that prose was generated. They flatten
every sentence into the same rhythm and make the writing sound like a machine
listing clauses. In this repository, **do not use an em dash to link two
thoughts**. Rewrite the sentence instead, using a period, comma, colon,
semicolon, parentheses, or a short connector such as *and*, *but*, *so*,
*which*, *because*, *that is*, or *for example*.

A spaced en dash (`–`) is acceptable only inside a genuine range (`1–3`, `May
2026–present`), never as a substitute for an em dash. Hyphens in compound words
(`read-only`, `open-source`) are fine.

The goal is prose a person would actually write and say. Vary sentence length,
prefer active voice, use concrete nouns, and let short sentences do the work.

### How to rewrite an em dash

Pick the connector that expresses the real relationship between the two ideas.
The dash hides that relationship; the connector names it.

| Relationship | Instead of the dash, use | Example |
| --- | --- | --- |
| Result | *so*, *therefore*, a new sentence | "The port was blocked, so the pipeline was unreliable." |
| Contrast | *but*, *yet*, *although* | "It started ARM-only, but x86 proved cheaper." |
| Cause | *because*, *since* | "Schedules are staggered because one GPU serves one request." |
| Explanation | a colon | "The stack has three pillars: metrics, logs, and alerts." |
| Appositive | commas or parentheses | "Ollama serves a local model, qwen3.5:4b, on the GPU node." |
| List preamble | a colon | "It exposes four tools: metrics, logs, workload state, and SQL." |
| Addition | *and* | "The chart adds cluster init and bucket provisioning." |
| Emphasis | a separate sentence | "Every figure is traceable. Nothing is an estimate." |

### Examples: don't and do

**Don't:** "A seven-node cluster running a lakehouse, agents, and observability — built from open source."

**Do:** "A seven-node cluster running a lakehouse, agents, and observability. It is built from open source."

**Don't:** "Read-only MCP servers give agents facts — never unrestricted access."

**Do:** "Read-only MCP servers give agents facts, but never unrestricted access."

**Don't:** "The lakehouse is the foundation — every other project builds on it."

**Do:** "The lakehouse is the foundation that every other project builds on."

**Don't:** "Ingestion, storage, catalog, query, and BI — all assembled at home."

**Do:** "Ingestion, storage, catalog, query, and BI, all assembled at home."

**Don't:** "Every figure is traceable to the cluster — nothing is an estimate."

**Do:** "Every figure is traceable to the cluster. Nothing is an estimate."

**Don't:** "The cluster started ARM-only — x86 mini-PCs proved more cost-effective."

**Do:** "The cluster started ARM-only, but x86 mini-PCs proved more cost-effective."

**Don't:** "Three incidents — Bitnami, Redis, and MinIO — shaped the policy."

**Do:** "Three incidents shaped the policy: Bitnami, Redis, and MinIO."

**Don't:** "The reviewer — which owns the only write action — comments on pull requests."

**Do:** "The reviewer, which owns the only write action, comments on pull requests."

**Don't:** "It is read-only by default — mutations need approval."

**Do:** "It is read-only by default, and mutations need approval."

**Don't:** "It is not a demo — it is a working platform."

**Do:** "It is not a demo. It is a working platform."

**Don't:** "The pipeline kept failing — we rebuilt it around schema checks."

**Do:** "The pipeline kept failing, so we rebuilt it around schema checks."

**Don't:** "Several tools — Prometheus, Loki, and Trino — answer the question."

**Do:** "Several tools answer the question, including Prometheus, Loki, and Trino."

**Don't:** "The vendor changed the license — with almost no warning."

**Do:** "The vendor changed the license with almost no warning."

**Don't:** "A small model cannot cover a large tool surface — context runs out."

**Do:** "A small model cannot cover a large tool surface because context runs out."

### More human, not just dash-free

Removing em dashes is necessary but not sufficient. Also:

- Prefer short, declarative sentences. A period is usually stronger than a dash.
- Prefer active voice: "ArgoCD reconciles the cluster", not "the cluster is reconciled".
- Use "you" and "we" where it reads naturally. This is a personal project, not a press release.
- Be concrete. "Six nodes across two architectures" beats "a heterogeneous environment".
- Cut hedges and filler: *just*, *simply*, *very*, *really*, *in order to*.
- Vary how sentences start. A page where every paragraph opens the same way reads as generated.
- Say what is true and, where it helps, what is uncertain. Honesty reads as competence.
