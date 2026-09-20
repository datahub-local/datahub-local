# Spec Delta

## Purpose

Keep the whole showcase site — its portfolio content and its platform facts —
true to the underlying repositories and the running cluster by regularly
comparing them and proposing reviewable corrections, without a human having to
remember to sweep every page.

## ADDED Requirements

### Requirement: Domain-scoped maintenance passes

The maintainer SHALL expose separately runnable maintenance passes per domain —
content, platform, and services — and SHALL also expose a combined pass that runs
all domains. Running one domain SHALL NOT require running the others.

#### Scenario: A single domain is maintained

- **WHEN** the maintainer is invoked for one domain
- **THEN** it checks and proposes corrections for that domain only
- **AND** it does not touch content owned by another domain

#### Scenario: The whole site is maintained

- **WHEN** the maintainer is invoked for all domains
- **THEN** each domain is checked and its corrections are proposed

### Requirement: Recurring maintenance run

A maintenance pass SHALL inspect the pages in its domain and the sources behind
them. When it finds corrections, it SHALL propose them as a pull request for that
domain. When it finds nothing, it SHALL report the domain as current and SHALL
NOT open a pull request.

#### Scenario: A domain has drifted

- **WHEN** a pass finds one or more corrections in its domain
- **THEN** it opens a pull request containing those corrections with a summary of
  what changed and why

#### Scenario: A domain is current

- **WHEN** a pass finds no corrections
- **THEN** it reports that the domain needs no changes
- **AND** no pull request or commit is created

### Requirement: Evidence before judgement

Before proposing any correction, the maintainer SHALL gather the relevant facts
deterministically from their sources. It SHALL NOT rely on values recalled from a
model or copied from prose.

#### Scenario: A fact is checked

- **WHEN** the maintainer evaluates a claim, version, count, node, or link on a
  site page
- **THEN** the value it compares against is fetched during the run from GitHub,
  the site tree, the config-of-record, or the live cluster as appropriate to the
  domain

### Requirement: Record-versus-cluster cross-check

For platform and service facts, the maintainer SHALL compare the
config-of-record against the live cluster. A disagreement between the two SHALL
be reported as a finding rather than silently resolved in favour of either side.

#### Scenario: The record and the cluster disagree

- **WHEN** a value in the config-of-record differs from the value observed in the
  live cluster
- **THEN** the pull request summary reports the mismatch, naming both values and
  their sources
- **AND** the site is corrected to match the live cluster unless doing so would
  contradict another verified source

#### Scenario: The record cannot be read

- **WHEN** the config-of-record is unavailable
- **THEN** the pass states which facts could not be cross-checked rather than
  assuming they match

### Requirement: Repository drift detection

The content maintainer SHALL detect repositories that are new, renamed, archived,
or removed relative to the showcase catalogue, and SHALL propose adding, updating,
or retiring the corresponding project cards.

#### Scenario: A new repository appears

- **WHEN** a repository relevant to the showcase exists but has no project card
- **THEN** the proposed pull request adds a card, or records why it was
  deliberately excluded

#### Scenario: A repository is archived

- **WHEN** a catalogued repository is archived or deleted
- **THEN** the proposed pull request marks or retires its card

### Requirement: Link and asset health

The maintainer SHALL check source links, documentation links, and image
references on site pages for dead targets and SHALL propose corrections.

#### Scenario: A reference is broken

- **WHEN** a link or image reference on a site page no longer resolves
- **THEN** the proposed pull request corrects it or removes the reference, and
  names the broken target in the summary

### Requirement: Content factual freshness

The maintainer SHALL detect content statements that have drifted from their
sources — including counts, statuses, and proof points — and SHALL propose
corrections, omitting any figure it cannot verify.

#### Scenario: A stated figure has changed

- **WHEN** a number or status on a site page no longer matches its source
- **THEN** the proposed pull request updates it to the verified value, or removes
  it when no source supports it

### Requirement: Platform facts maintenance

The platform maintainer SHALL keep the architecture and hardware pages true to
the cluster, covering nodes, hardware classes, roles, and namespace topology.

#### Scenario: The cluster changed

- **WHEN** a node is added, removed, renamed, or re-imaged, or a namespace or its
  contents change
- **THEN** the proposed pull request updates the affected node table, hardware
  list, topology diagram, or namespace table

#### Scenario: Hardware details drift

- **WHEN** a claimed hardware attribute (CPU, cores, memory, GPU, OS) no longer
  matches the cluster or the config-of-record
- **THEN** the proposed pull request corrects it, or reports the record-versus-
  cluster mismatch when the two sources disagree

### Requirement: Service and version maintenance

The service maintainer SHALL keep the service pages true to the deployed stack,
covering which services exist and their versions, including chart versions.

#### Scenario: A service version changed

- **WHEN** a deployed service or chart version differs from the version the site
  states, or from the config-of-record
- **THEN** the proposed pull request updates the stated version, or reports the
  mismatch when the record and the cluster disagree

#### Scenario: A service was added or removed

- **WHEN** a service is deployed that the site does not mention, or the site
  mentions a service that is no longer deployed
- **THEN** the proposed pull request adds or removes the corresponding entry

### Requirement: Roadmap and status upkeep

The maintainer SHALL review the Overview's forward-looking section and catalogued
project statuses against recent repository activity, and SHALL propose updates
when they no longer reflect reality.

#### Scenario: Work has moved on

- **WHEN** recent releases, merged work, or specs indicate a project's status has
  changed
- **THEN** the proposed pull request updates the affected status or
  forward-looking entry

### Requirement: Image refresh

The content maintainer SHALL detect when a project's subject has changed enough
that its showcase image no longer represents it, and SHALL propose regenerating
that image using the showcase image-generation path.

#### Scenario: A project changed meaningfully

- **WHEN** a project's scope or identity changes so its existing image is
  misleading
- **THEN** the proposed pull request regenerates the image through the documented
  generation path and updates the asset

### Requirement: Consistency checks

The maintainer SHALL check the site for internal consistency — brand and style,
duplicated content across sections, and navigation integrity — and SHALL propose
corrections.

#### Scenario: Content is duplicated

- **WHEN** the same narrative appears on more than one page
- **THEN** the proposed pull request replaces the duplicate with a link to the
  single source

### Requirement: Pull-request-only delivery

The maintainer SHALL propose its changes only through a pull request against a
non-default branch. It SHALL NOT push to the default branch, force-push, or merge
any pull request. The maintainer SHALL edit only this site repository and SHALL
NOT modify the repositories that hold the config-of-record.

#### Scenario: Changes are proposed

- **WHEN** the maintainer has corrections to submit
- **THEN** they exist as a branch and an open pull request requiring human review
- **AND** the default branch is never modified directly
- **AND** no repository other than the site is written to

### Requirement: Verifiable and non-personal content

All proposed content SHALL be verifiable against a source, and SHALL NOT publish
real personal data such as shopping or banking rows. The maintainer SHALL NOT
invent figures, links, nodes, services, or projects to fill a gap.

#### Scenario: A gap cannot be filled

- **WHEN** the maintainer cannot verify a value or find a source
- **THEN** it leaves the content unchanged or removes the unsupported claim, and
  records the gap in the pull request summary rather than guessing

### Requirement: Scheduler-agnostic execution

Each domain pass SHALL be runnable both on demand and by an external scheduler
without changes to its definition, so a scheduler (for example a Sympozium
persona) can drive any domain later without redesign.

#### Scenario: Run by a scheduler

- **WHEN** a domain pass is invoked non-interactively by a scheduler
- **THEN** it completes the same pass and delivers the same pull request or report
  as a manual run
