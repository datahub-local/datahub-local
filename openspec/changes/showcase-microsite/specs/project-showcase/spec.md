# Spec Delta

## Purpose

Present DataHub.local as a verifiable showcase of enterprise Data & AI practice
run at home, so a visitor arriving from the personal brand site sees a claim, the
proof behind it, and the portfolio of projects built on the platform.

## ADDED Requirements

### Requirement: Lead claim on the landing experience

The site SHALL present the claim "Enterprise Data & AI at Home" as the primary
message in the first screen a visitor sees, together with a clear path into the
case study.

#### Scenario: First-time visitor lands

- **WHEN** a visitor opens the site root
- **THEN** the lead claim is visible without scrolling
- **AND** at least one prominent action leads into the case-study content

### Requirement: Alternating brand bands on the landing

The landing SHALL present the case-study content in alternating full-bleed bands
using the brand dark and cream colours, so scrolling produces clear visual
rhythm. The bands SHALL render the same fixed brand colours regardless of the
visitor's light/dark scheme choice.

#### Scenario: Visitor scrolls the landing

- **WHEN** a visitor scrolls past the featured projects
- **THEN** consecutive content sections alternate between brand-dark and
  brand-cream backgrounds
- **AND** text, links, and tables in each band remain legible in both theme
  modes

### Requirement: Featured projects on the landing

The landing experience SHALL present the platform's flagship projects as a card
grid with imagery, so a first-time visitor can see the most important work
immediately.

#### Scenario: Visitor sees the featured projects

- **WHEN** a visitor opens the site root
- **THEN** a card grid presents the featured projects, each with a title, a
  one-line pitch, an image, and a link to that project's case study

#### Scenario: Project imagery is honest

- **WHEN** a featured project has no real screenshot yet
- **THEN** its card shows an abstract, on-brand illustration rather than a stock
  photo that implies something untrue

### Requirement: Enterprise-capability coverage

The landing SHALL present how enterprise practices are implemented on this
platform, using feature rows rather than a table. The coverage SHALL include at
minimum: infrastructure as code, GitOps delivery, CI/CD, identity and access,
secrets management, observability, reliability and backups, data platform,
streaming, orchestration, AI platform, governance, and cost management.

#### Scenario: Visitor reads the enterprise practices

- **WHEN** a visitor reaches the enterprise-practices section of the landing
- **THEN** each practice group states the enterprise expectation and the
  concrete implementation used here
- **AND** the practices link to the relevant technical documentation pages

### Requirement: Projects catalogue

The site SHALL provide a Projects section that catalogues the platform's use
cases across four groups — Data & Analytics, AI & Agents, Platform & Operations,
and Open Source & Lessons. The index SHALL present every catalogued use case as a
summary card, and **every catalogued use case SHALL have a full case study**,
each stating the problem addressed, the approach taken, the technologies
involved, the outcome, and a link to its source or artifact.

#### Scenario: Visitor browses the catalogue

- **WHEN** a visitor opens the Projects index
- **THEN** every catalogued use case is listed as a card with a one-line
  summary, grouped by domain
- **AND** each card links to that use case's full case study

#### Scenario: Visitor reads a deep-dive case study

- **WHEN** a visitor opens a deep-dive case study
- **THEN** the page states the problem, approach, technologies, outcome, and a
  source or artifact link

#### Scenario: Personal data is not published

- **WHEN** a case study covers personal data such as shopping invoices or bank
  transactions
- **THEN** the page describes method, schema, and aggregate outcomes without
  publishing real rows

#### Scenario: Catalogue does not duplicate the documentation

- **WHEN** a case study covers a component already described in the Services
  documentation
- **THEN** the case study links to that documentation for reference instead of
  restating it

### Requirement: Showcase navigation

The primary navigation SHALL expose the showcase destinations — home, projects,
and open source & lessons — as first-class entries, and SHALL group the remaining
technical documentation (architecture, cluster setup, and services) under a
single section so the showcase is not buried.

#### Scenario: Visitor scans the navigation

- **WHEN** a visitor opens any page
- **THEN** the home, projects, and open source & lessons destinations are visible
  in the primary navigation
- **AND** the architecture, cluster setup, and services documentation is
  reachable under one grouped section

### Requirement: Forward-looking signal without a maintained roadmap

The landing SHALL present a short forward-looking view of what comes next. The
site SHALL NOT maintain a separate roadmap page that restates shipped work.

#### Scenario: Visitor looks for what is next

- **WHEN** a visitor reaches the end of the landing case study
- **THEN** a concise forward-looking section states current and upcoming
  directions
- **AND** no standalone roadmap page duplicates shipped projects

### Requirement: Technical documentation preserved

The existing technical documentation (architecture, cluster setup, services,
open source, lessons learned) SHALL remain reachable from the site navigation
after the refactor. Previously published page paths that move SHALL resolve to
their new location rather than returning a not-found page.

#### Scenario: Existing deep link still resolves

- **WHEN** a visitor follows a previously published documentation URL that was
  restructured by this change
- **THEN** the visitor reaches the corresponding content, either directly or via
  a redirect

#### Scenario: Documentation remains reachable

- **WHEN** a visitor opens the site navigation
- **THEN** every pre-existing documentation section is reachable within two
  navigation steps from the site root

### Requirement: Cross-link to the personal brand site

The site SHALL include a discoverable link to the personal brand site so a
visitor can move between the project microsite and the personal showcase.

#### Scenario: Visitor follows the cross-link

- **WHEN** a visitor looks for the author's personal site
- **THEN** a link to the personal brand site is present in a persistent site
  region and opens without a broken target

### Requirement: Brand consistency

The site SHALL reuse the established brand tokens (MOSS colour palette and
typography) for all new showcase components, so the microsite and the personal
brand site present as one visual family.

#### Scenario: New components match the brand

- **WHEN** a showcase component (matrix, project card, band, or cross-link) is
  rendered in either the light or dark scheme
- **THEN** it uses the established brand colours and typography

### Requirement: Verifiable proof points

Any quantitative proof point shown on the site SHALL be verifiable against the
running platform or a public artifact. The site SHALL NOT present unverifiable
or estimated figures as fact.

#### Scenario: A proof point is displayed

- **WHEN** the landing or a project page states a quantity or outcome
- **THEN** that figure is traceable to the live cluster, a repository, or another
  public source
