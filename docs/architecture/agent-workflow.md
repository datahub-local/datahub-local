# Agent workflow

How a task moves from an idea to a reviewed pull request. One owner, one coding
agent, and a GitHub issue that carries the task the whole way.

## The pieces

| Piece | Where it runs | What it owns |
| --- | --- | --- |
| Taskboard | GitHub issues in `datahub-local/datahub-local`, Project board `datahub-local#1` | The task, its status, and the conversation about it |
| Hermes | `automation` namespace, `datahub-local-core-automation-hermes` | Dispatch, status changes, Slack notifications, the review request |
| OpenCode | `automation` namespace, `opencode-server` behind the `opencode-web` proxy | Reading the repository, editing, testing, committing, opening the pull request |
| MCP shim | `automation` namespace, `opencode-mcp` | The seven tools Hermes calls to drive a session |

The agent is reachable two ways: a browser session through the proxy, and Hermes
through the shim. The issue is the shared record.

## The lifecycle

Status lives on the Project board, not in labels. The board has six statuses and
every one of them is written by exactly one actor.

| Status | Set by | Evidence |
| --- | --- | --- |
| `Backlog` | the issue creator | an issue exists, nobody started it |
| `Ready` | the owner | the issue is read, scoped, and labelled `agent` |
| `In Progress` | Hermes | Hermes started or resumed a session |
| `Blocked` | Hermes | the agent asked a question the owner has to answer |
| `Testing` | Hermes | a pull request exists and is open |
| `Done` | Hermes, or the board automation | the pull request merged, or the issue closed |

Nobody else moves a card. The agent has no `project` token scope, and that is on
purpose: one writer means no two components disagree about what state a task is
in.

## What happens, in order

1. **Intake.** The owner, or Hermes on the owner's behalf, opens an issue with
   `What`, `Why`, `Acceptance` and `Repo`, labelled `agent` and one area label. It
   lands in `Backlog`.
2. **Ready.** The owner moves it to `Ready`. That move is the whole trigger; there
   is no assignment and no second signal.
3. **Dispatch.** Hermes runs a tick every ten minutes. It reads the board, takes
   the lowest-numbered `Ready` issue with the `agent` label, and starts a session
   with a prompt that carries the issue number, its title and its body.
4. **Work.** The agent reads the issue, comments that it started, cuts a branch
   named `type/<issue>-<topic>`, implements, runs the repository's gate, and opens
   one pull request with `Refs datahub-local/datahub-local#<n>` in the body.
5. **Review.** Hermes moves the issue to `Testing`, requests the owner's review on
   the pull request, and posts the link on the issue with one line in Slack.
6. **Done.** When the owner merges, the issue closes and the tick moves it to
   `Done`.

## When the agent needs an answer

The agent asks once, with the `question` tool, and stops. It does not wait inside a
shell prompt and it does not guess.

1. Hermes sees the session report `needs_input`, and reads the question and its
   options.
2. It comments the question on the issue, mentions the owner, and sets `Blocked`.
3. It sends the same text to Slack.
4. The owner answers wherever is convenient: as a comment on the issue, or in the
   session form in the browser.
5. The next tick forwards the answer and sets `In Progress`. The issue comment
   wins when both exist, because the issue is the record.

## What is not automated

- No merge. The owner reviews and merges every pull request.
- No parallelism today, though the design allows it. The agent runs one turn at a
  time (`OPENCODE_MAX_CONCURRENT`), and two turns never share a checkout whatever
  the limit: one repository, one writer. A session waiting on a question does not
  hold the queue, because it is not consuming anything.
- No issue creation from anywhere except a person or Hermes in Slack. An issue is
  a decision, and the `Ready` move is the owner reading it.
- No status guessing. When the shim is down or a turn fails, Hermes reports the
  failure and leaves the status alone, so an outage never looks like a question.

## Where the rules live

- This page: the lifecycle, for a person.
- `datahub-local-core`, `files/agent/taskboard-loop/`: the tick's instructions and
  the script that reads and writes the board.
- `datahub-local-ai`, `agents/adapters/opencode/`: the agent's `AGENTS.md` and its
  `taskboard` skill, baked into the adapter image.
- `datahub-local-ai-mcp`, `servers/opencode/`: the MCP tools both sides use.
