# Tasks

## 1. Specification and the human page (`datahub-local`)

- [x] 1.1 Add `docs/architecture/agent-workflow.md`: the lifecycle table (status,
  what moves it, who writes it), the help loop as a numbered sequence, the review
  handoff, and the serial limitation stated plainly.
- [x] 1.2 Add the page to the `Platform` nav in `mkdocs.yml`, after `Architecture`.
- [x] 1.3 State in `AGENTS.md` that a task starts when its issue reaches `Ready`
  with the `agent` label, and that the board status is the state.
- [x] 1.4 `uv run mkdocs build --strict` passes.

## 2. Hermes side (`datahub-local-core`)

- [ ] 2.1 Write the loop's instructions as a Hermes skill at
  `releases/automation/files/agent/taskboard-loop/SKILL.md`, rendered into a
  ConfigMap. It names its tools, its one job per tick, the exact transition
  evidence, and the reply format for Slack.
- [ ] 2.2 Mount it read-only at `/opt/data/skills/devops/taskboard-loop` in
  `values/hermes.yaml.gotmpl`.
- [ ] 2.3 Add an idempotent init container that runs
  `hermes cron create 10m --name taskboard-tick --skill taskboard-loop ...` only
  when `hermes cron list` does not already contain the job, so a fresh volume is
  provisioned and an existing one is left alone.
- [ ] 2.4 Give Hermes the values the job needs and cannot read from the skill: the
  owner login and the Slack delivery target, as `extraEnv`.
- [ ] 2.5 `helmfile template` renders: one ConfigMap, one mount, one init
  container, and the existing init containers unchanged.
- [ ] 2.6 Deploy, then confirm from inside the Pod that
  `hermes cron list` shows `taskboard-tick`, `hermes skills` lists
  `taskboard-loop`, and one manual `hermes cron run taskboard-tick` reaches the
  board and answers `idle` with nothing ready.

## 3. Agent side (`datahub-local-ai`)

- [ ] 3.1 Extend `agents/adapters/opencode/skills/taskboard/SKILL.md` with the
  session contract: read the issue named in the prompt, comment the claim, cut the
  branch, open the PR, comment its URL, and finish with the report. No board
  writes.
- [ ] 3.2 Add the help protocol to the same skill: when a decision is the owner's,
  call `question` once with concrete options and end the turn; never wait in a
  shell prompt and never guess.
- [ ] 3.3 Add the OpenSpec rule for non-trivial tasks, and the "one repository, one
  PR" boundary, if either is missing from `AGENTS.md`.
- [ ] 3.4 Rebuild `datahub-local-ai-opencode-adapter` and re-pin the digest in
  `datahub-local-core/values/_version.yaml`.

## 4. First real run (issue #116)

- [ ] 4.1 Move #116 to `Ready` (it already carries `agent`) and let one tick start
  it, or start it by hand with the same prompt the tick would send. No special
  casing.
- [ ] 4.2 Confirm the transitions: `In Progress` on dispatch, `Testing` on the PR,
  `Done` on the merge or close.
- [ ] 4.3 If the run needs a decision, confirm the help loop end to end: comment
  with the marker, `Blocked`, Slack ping, answer on the issue, resumed session,
  `In Progress`.

## 5. Record

- [ ] 5.1 Update this change with what the first run actually did, including every
  place the design was wrong, then archive it and add the capability spec.
