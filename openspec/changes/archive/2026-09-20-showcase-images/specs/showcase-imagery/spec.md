# Spec Delta

## Purpose

Give every showcase project a striking, brand-consistent image so the portfolio
reads as a designed showcase rather than a text-only catalogue, with the images
regenerable from prompts stored in the repository.

## ADDED Requirements

### Requirement: Image coverage across the showcase

The showcase SHALL provide a dedicated image for each deep-dive case study and a
cover image for each project catalogue card. Every catalogued project SHALL be
visually represented. An existing real photograph MAY serve as both the cover and
the deep-dive image for a project it already represents honestly.

#### Scenario: Deep-dive page shows its image

- **WHEN** a visitor opens a deep-dive case study
- **THEN** the page displays the image generated for that project

#### Scenario: Every catalogue card is covered

- **WHEN** a visitor opens the Projects index
- **THEN** every project card displays its cover image
- **AND** no card falls back to a missing or broken image

### Requirement: Brand-consistent visual language

Generated images SHALL use the established MOSS brand palette and a consistent
composition and aspect ratio, so the images read as one family across the site.

#### Scenario: Images match the brand

- **WHEN** any showcase image is displayed in either the light or dark scheme
- **THEN** its dominant colours are drawn from the brand palette and its shape is
  consistent with the other showcase images

### Requirement: Images carry no required text

Images SHALL NOT contain text that a visitor must read to understand the page.
Any generated lettering SHALL be treated as decorative, since generated text is
unreliable.

#### Scenario: A label is needed

- **WHEN** a project needs a visible label or caption
- **THEN** the text is rendered by the site rather than embedded in the image

### Requirement: Accessible alternative text

Every showcase image SHALL carry descriptive alternative text that conveys its
purpose to a visitor who cannot see it.

#### Scenario: Image alternative text

- **WHEN** a showcase image is rendered
- **THEN** it has alternative text describing the project it represents, not a
  generic label such as "image"

### Requirement: Repeatable generation from stored prompts

Each showcase image SHALL be regenerable from a prompt and parameters stored in
the repository, through a single documented command, without editing source code.
The documented command SHALL be reachable both by a person and by an agent
through a named skill, so regeneration never depends on improvised code.

#### Scenario: Regenerate a single image

- **WHEN** a maintainer runs the documented command for one project
- **THEN** only that project's image is regenerated and written to the site

#### Scenario: Regenerate the whole set

- **WHEN** a maintainer runs the documented command for all projects
- **THEN** every showcase image is regenerated from the stored prompts

#### Scenario: Generation is invoked by an agent

- **WHEN** a maintainer asks the agent to regenerate one project or the whole set
- **THEN** the agent runs the documented command and only the requested images are
  produced

### Requirement: Catalog-first onboarding

A project SHALL have a prompt-catalog entry before any of its images are
generated. For a project that is not yet catalogued, the generation path SHALL
collect the fields the entry needs (slug, group, cover subject and alt text, hero
subject and alt text), write them to the catalog, and then generate only that
project.

#### Scenario: A project is added

- **WHEN** a project has no cover or hero in the catalog
- **THEN** the generation path collects the entry fields, writes them to the
  catalog, and generates that project's images
- **AND** no other project's images are touched

#### Scenario: The entry fields are missing

- **WHEN** a required entry field has not been supplied
- **THEN** generation does not start and the missing field is requested

### Requirement: Regeneration is explicit and targeted

The generation path SHALL regenerate an existing image only when the request
names that project or the whole set. An invocation that names no existing project
SHALL default to onboarding a new project and SHALL leave every existing asset
unchanged.

#### Scenario: A general invocation

- **WHEN** the generation path is invoked without naming an existing project
- **THEN** no existing image is regenerated
- **AND** the run either onboards a new project or reports nothing to do

### Requirement: Imagery provenance is recorded

Each generated image SHALL record its model, provider, prompt hash, and
generation date in a manifest and in the image file's metadata.

#### Scenario: Provenance of a committed image

- **WHEN** an image is committed to the repository
- **THEN** its model, provider, prompt hash, and date are retrievable from the
  manifest

### Requirement: The site builds without generating

The site SHALL build and deploy from committed image assets, without calling the
image-generation service during the build.

#### Scenario: Offline build

- **WHEN** the site is built without access to the image-generation service
- **THEN** the build succeeds and every image resolves from the committed assets

### Requirement: Generation fails loudly

Image generation SHALL report a clear failure for a project whose image could not
be produced, and SHALL NOT silently leave a broken or placeholder image in the
showcase.

#### Scenario: Generation service is unavailable

- **WHEN** the image-generation service returns an error or no image for a project
- **THEN** the command exits with a non-zero status naming the affected project
- **AND** no image file is written for it

### Requirement: Personal data is not depicted

Generated images SHALL NOT depict real personal data such as shopping invoices or
bank transactions.

#### Scenario: An image would show personal data

- **WHEN** a project's subject involves personal data
- **THEN** its image represents the concept abstractly and shows no real rows,
  figures, or account details
