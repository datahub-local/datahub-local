# Agentic code automation

One agent turns an issue into a reviewed pull request in any datahub-local
repository. The board carries the state, the issue carries the task, and the
owner's merge is the only step that stays human.

<p class="project-meta" markdown="span">
  <span class="meta-pill meta-pill--area">AI &amp; Agents</span>
  <span class="meta-pill meta-pill--status">Running, first cycle shipped</span>
  <a class="meta-pill meta-pill--github" href="https://github.com/datahub-local/datahub-local-core">:fontawesome-brands-github: datahub-local-core</a>
</p>

<figure markdown="span">
  ![A dark workbench with one arm threading green filament from a ticket across many slate plates](../assets/img/showcase/ai-agents/agentic-code-automation-hero.webp){ width="1024" }
</figure>

## Problem

Fifteen repositories, one owner, and a steady supply of small changes. The work
between "this should be done" and "this is ready to review" is where it stalls:
read the issue, find the repository, cut the branch, keep the gate green, open a
pull request that explains itself, and keep the board honest about where the work
stands. Every step is small. Together they are the reason a two-line fix waits a
month.

A fixed pipeline does not cover it. The step that matters, deciding what to change
and how, needs reading and judgement, and a scheduled script cannot open a pull
request that a reviewer would accept.

## Approach

The loop splits judgement from state. The agent decides and writes code. Hermes,
the chat-driven agent in the `automation` namespace, owns every board write, so no
two components can disagree about where a task stands.

- **The board is the state.** Six statuses on the GitHub Project, and each one is
  written by exactly one actor: `Backlog` by the issue creator, `Ready` by the
  owner, `In Progress`, `Blocked` and `Testing` by Hermes, `Done` when the pull
  request merges or the issue closes.
- **The issue is the record.** `What`, `Why`, `Acceptance` and `Repo`, labelled
  `agent`. Moving it to `Ready` is the whole trigger: no assignment, no second
  signal.
- **A tick every ten minutes.** Hermes reads the board and starts a session on the
  lowest-numbered `Ready` issue, one at a time, and stops when the agent has no
  free turn. The dispatch waits up to two minutes, long enough to catch a question
  the agent asks before it starts editing. A session parked on a question does not
  hold the queue.
- **Every board write is announced.** A card added at `Backlog` or moved between
  statuses posts one line to Slack. The helper that writes the board posts the
  line itself, so a forgotten report cannot hide a move. Pull request and merge
  links stay in full on the issue, where GitHub sends its own notifications.
- **The agent works in the repository.** It claims the issue, cuts
  `type/<issue>-<topic>`, implements, runs that repository's gate, and opens one
  pull request with `Refs datahub-local/datahub-local#<n>`. When the change touches
  a documented capability it writes the OpenSpec delta on the same branch, so the
  pull request merges a spec that is already true.
- **A second model reviews the diff** before the handover, read-only, on a
  different model. Findings are fixed or answered, the gate runs again, and the
  review happens at most twice.
- **Questions come back to the owner.** The agent asks once with concrete options
  and stops. The question lands on the issue, the card moves to `Blocked`, and one
  line goes to Slack. Both the comment and the Slack line carry the OpenCode
  session link, so the owner can answer in writing or pick an option in the web
  UI. The answer, written on the issue or in the channel, arrives as the agent's
  next turn.
- **The owner merges.** Nothing merges automatically.
- **The board answers in Slack.** `/hermes board list`, `show`, `move` and
  `comment` run the same helper the tick uses, so a chat request reads and writes
  state without starting a turn.

## Technologies

- **Hermes Agent** for dispatch, board writes, question handling, and the Slack
  front door, calling a model through the local LiteLLM gateway
- **OpenCode** behind an authenticated proxy for the code turn, reached through a
  seven-tool MCP shim
- **GitHub Apps**, one for the manager and one for the coder, with installation
  tokens minted by a sidecar on loopback instead of a personal token in the Pod
- **GitHub Projects** as the only state store, `agent` labels as the delegation
  switch
- **Slack** over Socket Mode, one slash command, private channel
- **OpenSpec** deltas carried inside the same pull request as the code
- Longhorn for the agent's home volume, gVisor for its pod

## Outcome

The first production cycle ran on 2026-11-02. Two issues were created, both were
dispatched by the loop, and both became pull requests: one straight through, one
that stopped to ask which of two page titles to use, went `Blocked`, took the
answer, resumed, and finished. No human touched a branch or a card.

Measured on that run: a tick with one dispatch took 59 seconds, a tick with a
dispatch plus a board transition 95 seconds, and the tick returns before the code
turn ends, so the ten-minute schedule never waits on a build. One turn at a time,
one checkout per repository, and three failed fixes end a turn as `BLOCKED`
instead of looping.

The limits are deliberate. The agent has no merge button and no board credential,
the manager owns every status write, and a missing tool or a permission it does not
hold is reported as a question rather than worked around.

## Further reading

- [Automation services](../services/automation.md): where the agent, its sidecars, and the tick live
- [Repositories](../repositories.md): which repository owns which part of the platform
- [`datahub-local-core`](https://github.com/datahub-local/datahub-local-core): the release, the board helper, and the skills the loop runs from
