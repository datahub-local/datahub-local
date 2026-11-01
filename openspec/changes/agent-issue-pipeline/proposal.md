# Proposal

## Why

The code agent exists and nothing dispatches it. Today an issue reaches `Ready` on
the Project board and stops there: no session starts, no state moves, and the only
way to get work done is to open a Slack thread and ask Hermes for it. The pieces
are deployed (the OpenCode server, the `opencode` MCP shim with seven tools, the
Hermes GitHub MCP server with the `projects` toolset, and the board itself), but
the loop that connects them is written down nowhere and exists in no repository.

That loop is also the part that drifts. `AGENTS.md` in the agent image, the
`taskboard` skill, the Project board statuses and Hermes' behaviour each describe a
piece of it, and they disagree: the skill says the pull request is Hermes' job, the
agent's `AGENTS.md` says the agent opens it, the board has six statuses nobody
sets, and nothing says what "help" looks like.

## What Changes

- **One documented lifecycle** for a unit of work: `Backlog → Ready → In Progress →
  Blocked ⇄ In Progress → Testing → Done`, with the event that moves each edge.
- **Hermes becomes the only writer of board state.** The OpenCode Pod has no
  `project` token scope, so it must not move the board. It signals through issue
  comments and the session state; Hermes reads the evidence and moves the status,
  pings Slack, and posts the review request.
- **A poll tick replaces a webhook.** Hermes runs a scheduled job every ten minutes
  that reads the board, starts work on `Ready` + `agent` issues through the
  `opencode` MCP shim, resumes blocked sessions when the owner answers, and closes
  the loop when a pull request is merged.
- **A stated help protocol.** The agent calls `question`; the shim reports
  `needs_input`; Hermes sets `Blocked`, comments the question on the issue with
  `@alvsanand`, and pings Slack. The first answer wins, from the issue or from the
  session form, and the issue comment is the record.
- **The agent owns its pull request.** It pushes the branch and opens the PR with
  `Refs datahub-local/datahub-local#<n>`, which is what `AGENTS.md` and the
  `taskboard` skill already say and what the image toolchain makes possible. Hermes
  reviews the diff, moves the issue to `Testing`, requests the owner's review, and
  reports on the issue.
- **Declared configuration.** The loop's instructions live as a Hermes skill in
  `datahub-local-core` as a ConfigMap, and the cron job is created idempotently by
  an init container, so a fresh `HERMES_HOME` comes up with the loop running.

## Capabilities

### New Capabilities

- `agent-issue-pipeline`: intake, dispatch, the help loop, pull-request handoff,
  board state transitions, the operator-visible signals, and the failure and
  serialization rules.

### Modified Capabilities

None. The agent's rule skills and the documentation are edited to match, but no
existing capability changes meaning.

## Impact

- `datahub-local`: this change and a page under `docs/architecture/` that states the
  lifecycle for a human reader; `AGENTS.md` gains the one line that a task starts
  when an issue reaches `Ready`.
- `datahub-local-core`: a Hermes skill ConfigMap, its volume mount, an idempotent
  cron-seed init container, and the job's schedule and delivery target in the
  `hermes` release values.
- `datahub-local-ai`: the OpenCode adapter's `AGENTS.md` and `taskboard` skill gain
  the session contract (claim, ask, open, report), and the adapter image is
  rebuilt and re-pinned in core.
- `datahub-local-ai-mcp`: unchanged. The seven `opencode` tools already cover the
  loop, and adding a ninth tool would be the wrong place to fix an orchestration
  gap.

Not in scope: a GitHub App for the agent, a merge bot, parallel sessions (the shim
is serial by design), and webhook-driven dispatch.
