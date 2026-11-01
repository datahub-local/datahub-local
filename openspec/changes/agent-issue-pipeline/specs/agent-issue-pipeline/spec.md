# agent-issue-pipeline Specification

## Purpose

Turn a GitHub issue in the `datahub-local` taskboard into reviewed code without the
owner relaying instructions by hand: the issue carries the task, the Project board
carries its state, Hermes dispatches and reports, and the OpenCode agent does the
work and opens the pull request. A decision only the owner can make stops the work
at a known point and reaches the owner once.

## ADDED Requirements

### Requirement: The board status is the state of the work

The pipeline SHALL express the state of an issue only through its Project status,
using the existing `Backlog`, `Ready`, `In Progress`, `Blocked`, `Testing` and
`Done` options, and SHALL NOT introduce a parallel label or comment convention that
records the same fact.

#### Scenario: A status is changed

- **WHEN** an issue moves between statuses
- **THEN** the new status is one of the six board options
- **AND** no `status:*` label is added to carry the same information

### Requirement: Only Hermes writes the board

The pipeline SHALL have exactly one component that changes Project status. The
OpenCode agent SHALL NOT call the Projects API, and its reports SHALL be limited to
issue comments, a pull request, and the state the MCP shim returns.

#### Scenario: Agent finishes a turn

- **WHEN** the agent completes or parks a turn
- **THEN** it has written comments and possibly a pull request
- **AND** the Project status is unchanged until Hermes acts on that evidence

### Requirement: A Ready issue is dispatched by polling

Hermes SHALL run a scheduled job, at most every ten minutes, that dispatches issues
that are `Ready` and carry the `agent` label, and SHALL start them through the
`opencode` MCP server. Dispatch SHALL send the issue number, title, body and the
repository rule as one `run_task` prompt.

#### Scenario: Owner moves an issue to Ready

- **WHEN** an issue with the `agent` label has status `Ready`
- **THEN** the next tick starts a session and sets `In Progress`
- **AND** it comments the session id and the expected branch name on the issue

#### Scenario: Nothing is ready

- **WHEN** no issue is `Ready`
- **THEN** the tick changes nothing and reports that there was nothing to do
- **AND** it does not comment on any issue

### Requirement: Concurrency is bounded, configured, and never shared per checkout

The pipeline SHALL dispatch `Ready` issues in order until the agent reports `busy`,
and SHALL treat the agent's configured concurrency (`OPENCODE_MAX_CONCURRENT`,
default one) as the only limit. Two turns SHALL NEVER run in one checkout. A
session waiting on the owner SHALL NOT consume a concurrency slot, and a `Ready`
issue that cannot start SHALL stay `Ready` and be reported once, not every tick.

#### Scenario: The limit is one

- **WHEN** one turn is running and another issue is `Ready`
- **THEN** the second issue stays `Ready`
- **AND** no session is created for it

#### Scenario: The limit allows more than one

- **WHEN** the limit is three and two turns run in two different repositories
- **THEN** the third `Ready` issue starts in its own repository's checkout

#### Scenario: A session is waiting on the owner

- **WHEN** a session is parked on a question and a `Ready` issue exists
- **THEN** the parked session does not count against the limit
- **AND** the other issue may start

### Requirement: A session is durable and its id is recorded on the issue

Hermes SHALL record the session id on the issue when work starts, read it back on
later ticks, and resume the same session instead of starting a new one.

#### Scenario: Hermes restarts between ticks

- **WHEN** a later tick finds an issue `In Progress`
- **THEN** it reads the session id from the issue's comments
- **AND** it continues that session with `run_task(session_id=...)` or polls it
  with `get_session`

#### Scenario: The recorded session is gone

- **WHEN** the recorded session id no longer exists on the server
- **THEN** Hermes comments that the session was lost, leaves the status unchanged,
  and reports it

### Requirement: A question from the agent reaches the owner exactly once

When a session reports `needs_input`, Hermes SHALL post the question on the issue
with a stable marker, mention the owner, set `Blocked`, and send the same text to
the reporting channel. The question SHALL be posted once per prompt, not once per
tick.

#### Scenario: The agent asks a question

- **WHEN** `get_session` returns `needs_input` with a form or permission request
- **THEN** the issue receives one comment containing the question, its options, the
  owner mention and the help marker
- **AND** the issue status becomes `Blocked`
- **AND** the owner is notified in Slack

#### Scenario: The same question is still open on the next tick

- **WHEN** the session still reports the same form or request id
- **THEN** no second comment is posted and no second notification is sent

### Requirement: The first answer resumes the session

Hermes SHALL resume a blocked session with the first answer that arrives, whether it
is an owner comment newer than the help comment or an answer already given through
the session's form, and SHALL set `In Progress` on that transition.

#### Scenario: Owner answers on the issue

- **WHEN** an issue is `Blocked` and a comment newer than the help marker exists and
  was not written by the bot or the agent
- **THEN** Hermes passes that text to `respond`
- **AND** the issue becomes `In Progress`

#### Scenario: Owner answers in the session instead

- **WHEN** an issue is `Blocked` and the session no longer reports `needs_input`
- **THEN** Hermes forwards nothing and sets `In Progress`

#### Scenario: Both answers arrive

- **WHEN** an owner comment and a session answer exist on the same tick
- **THEN** the issue comment is forwarded
- **AND** the issue comment is treated as the answer of record

### Requirement: The agent opens the pull request, Hermes hands it over for review

The agent SHALL create one branch per issue, open one pull request in the repository
that holds the change with `Refs datahub-local/datahub-local#<n>` in the body, and
comment its URL on the issue. Hermes SHALL NOT push, open a second pull request, or
merge. On seeing the pull request, Hermes SHALL move the issue to `Testing`, request
the owner's review, and post the review request on the issue.

#### Scenario: The agent finishes its work

- **WHEN** the agent opens a pull request and comments its URL
- **THEN** Hermes sets `Testing`
- **AND** it requests review from the owner on the pull request
- **AND** it comments the pull request URL and what changed on the issue

#### Scenario: The agent pushed a branch but no pull request

- **WHEN** a session is idle and a branch exists with no pull request
- **THEN** Hermes reports the branch name on the issue and leaves the issue `In Progress`

### Requirement: Done follows the merge or the close

Hermes SHALL set `Done` when the linked pull request is merged or the issue is
closed, and SHALL tolerate the board's own automations reaching `Done` first.

#### Scenario: Owner merges the pull request

- **WHEN** a tick sees the linked pull request merged, or the issue closed as
  completed
- **THEN** the issue status is `Done`
- **AND** no further turn is started for it

### Requirement: Failures are distinguishable from questions

When the shim is unreachable, or a session returns `error`, Hermes SHALL report the
failure on the issue and in Slack without pretending the owner was asked a question,
and SHALL NOT retry the same turn automatically.

#### Scenario: The shim is down

- **WHEN** `run_task` fails with a transport error
- **THEN** the issue status is left as it was
- **AND** the failure is reported with the error text
- **AND** the next tick may try again

#### Scenario: A session errors

- **WHEN** `get_session` reports `error`
- **THEN** Hermes posts the last transcript lines, sets `Blocked`, and says the owner
  must decide whether to resume or abort

### Requirement: Intake produces an issue the agent can act on

An issue created for the pipeline SHALL carry `What`, `Why`, `Acceptance` and
`Repo`, the `agent` label, and one area label.

The issue SHALL NOT decide whether an OpenSpec change is needed. That is the
agent's judgement, made against the repository's own rule after it has read the
code: a capability the repository documents in `openspec/specs/` needs a delta when
its behaviour changes, a new capability needs a change, and a fix, a version bump, a
typo or a dependency update needs neither. The dispatch prompt therefore points at
the agent's rules and never at OpenSpec.

#### Scenario: Hermes creates an issue from a request

- **WHEN** the owner asks Hermes for a change in Slack
- **THEN** Hermes creates the issue in the taskboard with the four sections and the
  labels
- **AND** the issue lands in `Backlog`
- **AND** the issue does not say whether an OpenSpec change is required

#### Scenario: The change touches a documented capability

- **WHEN** the agent starts work and the capability already has `openspec/specs/<capability>/spec.md`
- **THEN** it writes the delta before implementing
- **AND** `openspec validate --all` is part of its gate

#### Scenario: The change is a fix

- **WHEN** the change is a one-line fix, a version bump, a typo or a dependency update
- **THEN** no OpenSpec change is created
- **AND** the issue and the pull request are the record

### Requirement: The loop is declared in the repositories

The instructions Hermes follows and the agent's session contract SHALL live in
`datahub-local-core` and `datahub-local-ai` respectively, and a fresh Hermes home
SHALL come up with the scheduled job already present.

#### Scenario: Hermes loses its volume

- **WHEN** Hermes starts with an empty `HERMES_HOME`
- **THEN** the init container creates the `taskboard-tick` job
- **AND** the skill is present from the image or the mounted ConfigMap
- **AND** no manual step is needed to restore the loop
