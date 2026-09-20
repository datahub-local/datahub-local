# Proposal

## Why

The site currently documents DataHub.local as a technical platform, organised by
tool. It reads as an operator's manual: hardware specs, service descriptions, and
configuration depth. For a visitor arriving from a personal brand site, it does
not demonstrate enterprise Data & AI leadership — it shows capability, not
outcomes, judgment, or breadth.

The personal showcase site (a separate artifact, out of scope here) will link to
this repo for the DataHub.local story. This site must therefore earn that link:
lead with a claim, prove it with an enterprise-capability matrix, and surface the
portfolio of projects built on the platform.

## What Changes

- Turn the landing into the case study: lead with the claim "Enterprise Data & AI
  at Home", then **enterprise-practice coverage** mapping each practice to how it
  runs here, concrete **proof points**, and a short "What's next".
- Add a **Projects** section that catalogues **15 use cases** across four groups
  — Data & Analytics, AI & Agents, Platform & Operations, and Open Source &
  Lessons. Every use case is a card and **every card links to a full case
  study** (MCP platform, semantic layer, Bodega, personal finance, SRE agents,
  cloud-at-home, and the remaining catalogued work) written in depth.
- Make the landing sell: the claim, **alternating feature rows** that showcase
  the flagship projects with imagery, and **alternating full-bleed brand bands**
  (dark/cream) carrying the condensed case-study content for visual impact while
  scrolling.
- Handle personal data safely in the catalogue: the Bodega and personal-finance
  case studies describe method, schema, and aggregate outcomes without
  publishing real shopping or banking rows.
- Reorganise the top navigation into four destinations — Home, Projects, Open
  Source & Lessons, and Platform — making the showcase sections first-class and
  grouping the remaining technical documentation (Architecture, Cluster Setup,
  Services) under **Platform**.
- Remove the standalone `roadmap.md`. Its completed work is already covered by
  Projects; the forward-looking "What's next" on the landing replaces it, so the
  roadmap is not a separately maintained page.
- Add a cross-link component back to the personal showcase site, and keep brand
  tokens (MOSS palette, typography) consistent so the two sites feel like one
  family.
- Keep the existing technical documentation (Architecture, Cluster Setup,
  Services, Open Source, Lessons Learned) reachable underneath.
- **BREAKING**: reorganise the `mkdocs.yml` navigation and remove the `/roadmap/`
  page. Existing documentation paths are preserved; only `/roadmap/` stops
  resolving (see design for the redirect option).

## Capabilities

### New Capabilities

- `project-showcase`: the microsite's showcase behaviour — the lead claim and
  enterprise-practice coverage on the landing, a grouped projects catalogue with
  a full deep-dive case study per use case, cross-linking to the personal brand
  site, and preservation of the underlying technical documentation.

### Modified Capabilities

<!-- No existing specs in this project; nothing to modify. -->

## Impact

- `mkdocs.yml` navigation and theme extras.
- `docs/index.md` home page (the selling landing and condensed case study) and
  new `docs/projects/` content.
- `docs/stylesheets/extra.css` for matrix, project-card, and cross-link styling,
  plus a generic placeholder image for the project cards.
- `overrides/` for the persistent personal-site cross-link.
- External contract: `datahub-local.alvsanand.com` URLs consumed by the personal
  site; existing deep links and the published OSS chart docs.
- No runtime services or APIs are affected — this is a static MkDocs site.
