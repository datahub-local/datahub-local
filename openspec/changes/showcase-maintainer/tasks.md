# Tasks

## 1. Shared foundation

- [x] 1.1 Create the umbrella skill `.opencode/skills/site-maintenance/SKILL.md` and the `/maintain-site` command that runs all domains; verify the command loads the skill and reports a result per domain
- [x] 1.2 Implement the shared gatherer emitting a compact per-domain JSON fact bundle — content (repositories, releases, forks/archived, links), platform (inventory hosts, live nodes, namespaces), services (versions file, deployed charts and images) — driven by an include/exclude list; verify each bundle parses and no source is written
- [x] 1.3 Add dry-run and non-interactive modes; verify a dry-run performs every check and changes no file

## 2. Content domain

- [x] 2.1 Create `.opencode/skills/site-content-maintainer/` and the `/maintain-content` command; verify the skill is discovered and runs without cluster access
- [x] 2.2 Implement catalogue drift detection (new, renamed, archived, removed repos versus the catalogue); verify a synthetic new and archived repo each produce a proposed card change
- [x] 2.3 Implement link and asset health checks; verify a deliberately broken link and image reference are each reported with their exact target
- [ ] 2.4 Implement content freshness plus roadmap and project-status review; verify a stale count or status is proposed with its verified source, and an unsupported claim is proposed for removal rather than guessed
- [ ] 2.5 Implement consistency checks for duplicated content, navigation integrity, and brand usage; verify a duplicated narrative is proposed as a link to the single source
- [x] 2.6 Implement the conservative image-refresh rule using the showcase image-generation path; verify it triggers only on a meaningful project change and never on a routine pass

## 3. Platform domain

- [x] 3.1 Create `.opencode/skills/platform-maintainer/` and the `/maintain-platform` command; verify the skill is discovered and declares the cluster and inventory as required sources
- [x] 3.2 Implement node, hardware, and topology checks against the architecture and hardware pages; verify a synthetic node addition, rename, or removal produces the corresponding page change
- [x] 3.3 Implement the inventory-versus-cluster cross-check; verify a disagreement is reported with both values and their sources, and that an unreachable cluster fails loudly rather than reporting the site as correct

## 4. Service domain

- [x] 4.1 Create `.opencode/skills/service-maintainer/` and the `/maintain-services` command; verify the skill is discovered and declares the versions file and cluster as required sources
- [ ] 4.2 Implement service inventory and version checks against the service pages; verify a synthetic version change and an added/removed service each produce the corresponding page change
- [x] 4.3 Implement the `_version.yaml`-versus-cluster cross-check; verify a chart or image mismatch is reported with both values and their sources

## 5. Pull-request delivery

- [ ] 5.1 Implement per-domain branch creation, conventional commit, and `gh pr create` with a per-change summary; verify one PR per domain touching only intended files
- [x] 5.2 Implement the no-op path; verify a domain with no findings opens no branch or PR and exits successfully with a summary
- [x] 5.3 Implement per-domain idempotency; verify a second run updates the existing open PR for that domain instead of opening another
- [x] 5.4 Enforce the safety rules in each skill and its allowed tools; verify no skill can push to the default branch, force-push, merge, or write to a repository other than the site, exercised by a test or explicit review step
- [x] 5.5 Run `uv run mkdocs build --strict` on the branch before opening a PR; verify a failing build blocks that PR

## 6. Verification

- [x] 6.1 Dry-run each domain; verify the gathered facts match `gh`, the inventory, the versions file, and the cluster, and that no file changes
- [ ] 6.2 Run each domain for real; verify each PR summary explains every change and cites its source
- [x] 6.3 Invoke each domain non-interactively without a TTY; verify it completes the same pass and delivers the same outcome as an interactive run
- [x] 6.4 Verify each domain runs with only its own sources available and fails clearly when a required source is missing
- [x] 6.5 Audit the proposed changes for verifiability and privacy; verify no unverifiable figure, no record-versus-cluster mismatch left unreported, and no real personal data appear
