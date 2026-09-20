# Spec Delta

## Purpose

Give every showcase project a striking, brand-consistent image so the portfolio
reads as a designed showcase rather than a text-only catalogue, with the images
regenerable from prompts stored in the repository.

## ADDED Requirements

### Requirement: Image coverage across the showcase

The showcase SHALL provide a dedicated image for each deep-dive case study and a
cover image for each project catalogue card. Every catalogued project SHALL be
visually represented.

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

#### Scenario: Regenerate a single image

- **WHEN** a maintainer runs the documented command for one project
- **THEN** only that project's image is regenerated and written to the site

#### Scenario: Regenerate the whole set

- **WHEN** a maintainer runs the documented command for all projects
- **THEN** every showcase image is regenerated from the stored prompts

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
