# Design

## Context

Three things already run: `opencode-server` (the agent, its workspace and its
state), `opencode-mcp` (a stateless shim that exposes `run_task`, `get_session`,
`respond`, `abort_session`, `get_diff`, `list_sessions`, `get_transcript`), and
Hermes with the `opencode` server registered at a 900 second timeout. The Project
board `datahub-local#1` has `Backlog`, `Ready`, `In Progress`, `Blocked`,
`Testing`, `Done`, and its own automation adds items, closes them and archives
them. Hermes' GitHub token carries the `project` scope, and its MCP instance is
built with `GITHUB_TOOLSETS=default,projects`.

What does not exist is the part that reads `Ready`, starts a session, and writes
the result back. This change is that part, plus the rules the agent needs so its
behaviour is predictable from the issue alone.

## Decisions

### 1 — Hermes is the only writer of board state

The OpenCode Pod's token has no `project` scope, and the `taskboard` skill forbids
calling the Projects API from that Pod. That constraint is worth keeping: it makes
the issue the record and the board a view, and it leaves exactly one component
that can move a card.

So the agent never sets a status. It comments, it opens a pull request, and it
returns a state from the shim. Hermes reads those three signals and owns every
transition. A transition that cannot be justified by evidence in the issue, the
session or the pull request does not happen.

### 2 — Polling, not a webhook

Hermes runs one scheduled job, `taskboard-tick`, every ten minutes. Each run is a
short tool loop: read the board, act on what changed, reply `idle` and stop when
nothing did. A webhook was rejected because it means a public ingress, a shared
secret and a receiver inside the Pod, which is three new failure surfaces to save
at most ten minutes of latency. Ten minutes is also the floor at which a human
notices nothing.

The job carries `--skill taskboard-loop`, so its instructions live in the skill
file, in this repository, and the cron entry stays a schedule plus a name.

### 3 — Parallel by design, one slot by default

The shim owns the limit: `OPENCODE_MAX_CONCURRENT`, default 1. The tick does not
count sessions itself; it dispatches `Ready` issues in order and stops at the first
`busy`, so raising the environment variable is the whole change.

Two rules make that safe rather than optimistic:

- **A checkout is single-writer.** The shim reads each working session's directory
  from the session itself and refuses a new task in a directory that already has a
  turn, whatever the limit. `/workspace/<repo>` therefore serialises per
  repository, which is the only collision that corrupts work.
- **A question is not work.** `/api/session/active` reports a session waiting for an
  answer as running. It spends no CPU and makes no progress, so the shim does not
  count it against the limit. Without that rule, one question stops the queue until
  the owner replies, which is the behaviour "serial by construction" had.

The tick passes `directory=<repo>` when the issue names exactly one repository, so
two issues in different repositories run in parallel once the limit is raised, and
two in the same repository queue behind each other. Raising the limit above one
also needs a resource bump on `opencode-server`, whose 2 CPU / 4Gi is sized for a
single turn.

### 4 — The session is the work, and the issue remembers its id

Sessions run for days and survive shim and server restarts, but Hermes does not
hold state between cron runs. The mapping lives where a human can read it: when a
session starts, Hermes comments `Started session <id> on branch <type>/<n>-<topic>`
on the issue, and every later tick reads the newest such comment back. If the
agent replaced the branch or restarted, the pull request is the newer evidence and
wins.

`list_sessions` is the fallback when the comment is missing, not the primary path,
because a title search can match the wrong session and a dropped comment is
visible.

### 5 — The help loop, and what "wait for both" means

The agent asks by calling `question`, which the agent image allows on purpose.
The call returns a form id or a permission request, the turn ends in
`needs_input`, and the session stays alive and idle.

Then, in one tick:

1. Hermes reads the question text and options from `get_session`.
2. It comments on the issue: the question verbatim, the options, and
   `@alvsanand please answer here or in the session`, and it tags the comment with
   the marker `<!-- taskboard:help -->`.
3. It sets `Blocked` and sends the same text to Slack.
4. It records nothing else. The comment is the marker.

Resume is the first answer to arrive. On a later tick, if the issue is `Blocked`
and a comment newer than the marker exists and it is not authored by the bot or
the agent, Hermes passes that text to `respond` and sets `In Progress`. If instead
the owner answered the form in the OpenCode web UI, `get_session` no longer says
`needs_input`, and the tick sets `In Progress` without forwarding anything. When
both happen, the issue comment is forwarded first and the form answer is ignored,
because the issue is the record and the dashboard answer may have been a
half-formed click.

### 6 — The agent opens the pull request

Design §4 of `add-opencode-agent` said pull requests stay Hermes' job. That predates
`gh` and the token being in the agent image, and it contradicts the agent's own
`AGENTS.md`. Two writers for one pull request is how a branch ends up with a
duplicate PR, so this change makes the agent the single author:

- branch `type/<issue>-<topic>`, cut from `main`;
- one PR in the repository that holds the change, body `Why`/`What`/`Checks` plus
  `Refs datahub-local/datahub-local#<n>`;
- the PR URL commented on the issue;
- the agent's last text is a short report: what changed, what was verified, what
  was left out.

Hermes then reviews with `get_diff`, sets `Testing`, requests `@alvsanand` as
reviewer, and comments the review request on the issue. Hermes never merges and
never pushes.

### 7 — Done comes from the merge, not from the agent

The agent cannot know whether the owner merged. The tick sees the linked pull
request in `MERGED` or the issue `CLOSED` and sets `Done`. The board's own
`Pull request merged` and `Item closed` automations may get there first; Hermes
setting the same value is idempotent, so a race is harmless.

### 8 — Intake stays human-shaped

The owner, or Hermes on the owner's behalf, creates the issue with `What`, `Why`,
`Acceptance` and `Repo`, labelled `agent` plus one area label. Creation is not
automated further: an issue is a decision, and the point of the `Ready` move is
that the owner read it. A non-trivial task dispatches with the instruction to
write an OpenSpec change first, which is the same rule the repositories already
carry.

Labels do not encode state. `agent` marks delegation and is what puts the issue on
the board; the status is the state. Adding `status:*` labels would create a second
source of truth for the same fact.

### 9 — Where each piece lives

| Piece | Repository | Why there |
| --- | --- | --- |
| The lifecycle, as a human page | `datahub-local` | This is the published site and the taskboard's home |
| The tick's instructions (Hermes skill) | `datahub-local-core` | It ships beside the Hermes release it configures, as a ConfigMap |
| The cron entry | `datahub-local-core` | Idempotent init container, so a fresh `HERMES_HOME` gets the loop |
| The agent's session contract | `datahub-local-ai` | It is baked into the adapter image, next to `AGENTS.md` |
| Nothing | `datahub-local-ai-mcp` | The seven tools already cover the loop |

The Hermes skill is a ConfigMap and not a write into `/opt/data/skills`, because
`/opt/data` is a Longhorn volume: a file written once by a human drifts from the
repository and survives a reinstall. A read-only mount at
`/opt/data/skills/devops/taskboard-loop` is reviewable and replaced on every
deploy.

### 10 — Failure behaviour

- Shim unreachable: comment the failure on the issue, leave the status alone, and
  report in Slack. A status that flips to `Blocked` on an infrastructure failure
  hides the difference between "the agent needs you" and "the agent is down".
- Session returns `error`: post the last transcript lines, set `Blocked`, and let
  the owner decide whether to resume or abort. Never retry silently, because a
  retry loop against a broken workspace spends tokens and hides the cause.
- `busy` on a `Ready` issue: leave it `Ready` and say so in Slack once, not every
  tick.
- Agent pushed a branch but no PR: comment the branch name, keep `In Progress`, and
  tell the owner. That is a bug in the agent's turn, not a review.

## Non-goals

- Parallel issue execution. The shim is serial and the workspace is shared.
- Auto-merge, auto-approve, or a review bot that can approve.
- Webhook dispatch, and any new public surface.
- Issue creation from any source other than a human or Hermes in Slack.
- A changes-requested loop. Review comments reach the agent only when Hermes
  forwards them as a new turn, which is the same `run_task(session_id=…)` path the
  help loop already uses; automating the trigger is a follow-up.
