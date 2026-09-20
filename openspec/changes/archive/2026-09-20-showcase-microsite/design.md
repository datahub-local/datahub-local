# Design

## Context

See `proposal.md` — Why. Current state that shapes the approach:

- Static site built with **MkDocs Material** (`mkdocs.yml`), content in `docs/`
  Markdown, deployed to `datahub-local.alvsanand.com` via `mkdocs gh-deploy` in
  `.github/workflows/pages.yml`.
- A **MOSS brand palette** is already defined in `docs/stylesheets/extra.css`
  (`#0E1116`, `#F4F2EC`, `#5E8A3F`, `#7FAF5A`, `#A3CF7A`) with Space Grotesk /
  JetBrains Mono. Branding is a constraint to reuse, not to invent.
- Navigation is docs-shaped: Home, Architecture, Cluster Setup, Services, Open
  Source, Roadmap, Lessons Learned.
- The home page (`docs/index.md`) leads with hardware stats and an "About the
  author" card; project-like work (Invoice Service, AI agents, OSS charts) is
  buried in Roadmap and Open Source.
- The personal showcase site is a **separate artifact**; the only coupling is
  deep links and shared visual identity.

## Goals / Non-Goals

**Goals:**

- Add a case-study layer (lead claim + capability matrix + proof) above the docs.
- Add a Projects catalogue of 15 use cases, each with a full deep-dive case study.
- Make the landing sell the platform with a featured-project card grid.
- Keep the existing docs reachable and their URLs stable.
- Provide cross-links and shared brand tokens for the personal site.

**Non-Goals:**

- Building the personal showcase site in this repo.
- Migrating off MkDocs Material or redesigning the existing docs pages.
- Implementing new platform capabilities to fill matrix gaps.
- Gathering long-running impact metrics (deferred, see Open Questions).

## Decisions

### D1 — Keep MkDocs Material

Rationale: content is already Markdown, the brand CSS and deploy pipeline exist,
and the project cards/grid patterns are supported. Alternatives (Astro, Hugo,
Next) would buy landing-page freedom at the cost of rewriting content, rebuild-
ing brand CSS, and replacing CI. The showcase can be expressed with Material
grids, tables, and custom CSS.

### D2 — One selling landing that is also the case study

`docs/index.md` is both the sales page and the case study. It leads with the
claim and the featured-project cards, then carries the condensed capability
matrix, proof points, and "What's next" in alternating full-bleed bands.
Rationale: a separate Overview page split the argument from the pitch and
duplicated navigation. Folding the important parts into the landing keeps a
first-time visitor on one page while the deep dives in `docs/projects/` carry the
detail.

### D3 — Enterprise practices as feature rows, not a table

The practices are presented as feature rows grouped by theme (infrastructure and
delivery; identity, secrets and access; observability and reliability; data and
AI), each row naming the practices, the enterprise expectation, and the
implementation with links to the docs. Alternatives: a Markdown table or a
generated matrix. A table lost the landing's visual rhythm and read as dense
reference material; authored feature rows keep the showcase tone while covering
the same ground. Practices that cannot be verified are omitted rather than
filled with aspirational copy (see the spec's verifiable-proof-points
requirement).

### D4 — Projects: 15 cards, 15 deep dives

```
  docs/projects/index.md          catalogue: 15 cards in four groups
  docs/projects/<slug>.md         deep dive: problem / approach / tech / outcome / source
```

Every use case is both a card and a full case study. The catalogue is an entry
point; each card links straight to its deep dive, and the deep dive is the single
narrative source for that project.

| Group | Card | Slug |
| --- | --- | --- |
| Data & Analytics | Lakehouse core stack | `lakehouse-core` |
| Data & Analytics | Bodega shopping analytics | `bodega` |
| Data & Analytics | Personal finance datalake | `personal-finance` |
| Data & Analytics | Semantic layer for agents | `semantic-layer` |
| Data & Analytics | Data quality & lineage | `data-quality-lineage` |
| AI & Agents | SRE agents (Sympozium) | `sre-agents` |
| AI & Agents | MCP platform | `mcp-platform` |
| AI & Agents | Ask-your-cluster oracle | `oracle-responder` |
| AI & Agents | n8n AI content engine | `ai-content-engine` |
| AI & Agents | Local inference + GPU node | `local-inference` |
| Platform & Operations | Cloud-at-home on mini-PCs | `cloud-at-home` |
| Platform & Operations | GitOps & platform engineering | `gitops-platform` |
| Platform & Operations | Observability stack | `observability` |
| Open Source & Lessons | Published OSS Helm charts | `oss-charts` |
| Open Source & Lessons | Vendor-risk lessons | `vendor-risk` |

Two rules keep the catalogue honest:

- **Deep dives link to the reference docs for detail** rather than restating
  them — the catalogue is an entry point, not a second copy of `services/`.
- **Personal data is never published.** The Bodega and personal-finance deep
  dives describe method, schema, and aggregate outcomes only; no shopping or
  banking rows appear in the site or its assets.

Projects pages are the single source for project narratives; Open Source and the
landing link to them instead of restating. Rationale: avoids the current
duplication where the same work appears in three places.

### D5 — Navigation shape

```
  Home                  index.md              (selling landing + case study)
  Projects              projects/index.md     (catalogue -> 15 deep dives)
  Open Source & Lessons (section)
    Open Source         open-source/index.md  (slim list, links into Projects)
    Lessons Learned     lessons-learned.md
  Platform              (section)
    Architecture        architecture/overview.md
    Cluster Setup       cluster_setup/...     (Hardware, Provisioning)
    Services            services/...          (System, CI/CD, Security, Data,
                                               Automation, Monitoring, AI, Media)
```

Four top-level destinations. The showcase destinations — `Home`, `Projects`, and
`Open Source & Lessons` — sit first-class, and the remaining reference material
(architecture, cluster setup, services) groups under `Platform`. Lessons Learned
moves under `Open Source & Lessons` to match the Projects grouping. The separate
Overview destination is removed; its important content moved onto the landing
(see D2). Roadmap is no longer a destination (see D9).

### D6 — URL stability without new dependencies

New pages live under new directories (`projects/`); the existing docs keep their
current file paths, so no URLs move and no redirect plugin is required. If a
later step must relocate a page, adopt `mkdocs-redirects` at that point rather
than pre-emptively.

### D7 — Cross-link via configurable extra and macro

The personal site URL lives in `mkdocs.yml` under `extra.personal_site_url` and
is rendered by the existing `mkdocs-macros` plugin, so the link is one edit away
from becoming live and is not hard-coded across pages. Until the personal site
exists, the link is present but its target is resolved at config time.

### D8 — Brand components reuse existing tokens

New styles (matrix, project cards, cross-link) are added to `extra.css` using the
existing CSS variables, so both light and dark schemes work automatically and the
personal site can adopt the same variable names.

### D9 — Drop the maintained roadmap page

`roadmap.md` is removed rather than slimmed in place. It mixes two clocks: the
"Completed" half duplicates Projects and is effectively static, while the
"Now/Next" half changes weekly and is expensive to keep true. Issues and
milestones are not used on these repositories (8 open issues in total, no
milestones), so the forward-looking half cannot be derived from the tool where
the work already happens. The replacement is a three-bullet **What's next**
block on the landing, edited only when direction changes, not per task.

Alternatives considered: a data-file-driven page (`roadmap.yaml` rendered by the
existing macros plugin) — still a page to remember to touch; an auto
"Recently shipped" list built from the OSS chart release tags (the only repos
with releases) — backward-looking and would still omit the platform work, which
is untagged. Both are recorded here as the reasoning, not adopted.

This is the one URL this change removes: `/roadmap/` stops resolving. If that
matters, a single-entry `mkdocs-redirects` to the Overview is the fix; it is
tracked as an open question rather than added now, to keep D6's no-new-
dependency rule intact.

### D10 — Featured projects as illustrated cards

The landing's job is to make a visitor want the case study, so the first content
section after the hero shows the flagship projects as a card grid: each card has
an illustration, a domain tag, a title, a one-line pitch, and a link to its deep
dive. Rationale: a grid is more scannable than full-width rows and gives each
project a visual identity.

- Six projects are featured: Cloud-at-home, Lakehouse core, Semantic layer, MCP
  platform, SRE agents, and Bodega — infrastructure, data, AI, and a real
  application.
- Each card uses a distinct, abstract on-brand SVG illustration, since no real
  screenshots exist yet; swapping in a real image is a one-line change per card.
- No invented imagery: illustrations are abstract and branded, never stock photos
  that imply something untrue.
- Cards stack to two columns and then one on narrow screens.

### D11 — Alternating full-bleed bands

The landing alternates full-bleed bands of brand-dark (`#0E1116`) and brand-cream
(`#F4F2EC`): a dark hero, then alternating sections for the stack strip, featured
work, enterprise practices, proof, and a lessons quote. The bands use fixed brand
colours in both theme modes rather than following the light/dark toggle, so
scrolling produces strong rhythm and the page reads as a designed landing rather
than a documentation page.

Decisions:

- **Full-bleed** via the standard `margin-inline: calc(50% - 50vw)` technique,
  with `overflow-x: clip` on the body to avoid a horizontal scrollbar.
- **Fixed band palettes.** Band text, links, cards, and stats get band-specific
  colours from the MOSS palette; headings stay legible on each band regardless of
  the active scheme.
- **Reduced content.** The bands carry only the most important case-study
  material; the full technical detail stays in the reference docs and the deep
  dives.

### D12 — Landing information architecture

The landing is ordered as a pitch for a first-time visitor, front-loading the
hook and the evidence:

```
  Hero            claim + value proposition + headline metrics + CTAs
  Stack strip     the open-source technologies, as immediate credibility
  Featured work   six illustrated project cards
  Practices       six cards covering the thirteen enterprise practices
  Proof           verifiable numbers, each linked to its source
  Lessons + next  honesty as a competence signal, plus a short forward-looking view
  Author          who built it, with the personal-site cross-link
```

Rationale: an earlier version led with repeated full-width rows and buried the
proof; this order lets a visitor grasp what it is, see that it is credible, and
find something to click within one screen, while each section stays short.

## Risks / Trade-offs

- **Matrix claims outrun reality** -> Audit every row against `docs/` before
  publishing; omit rows that cannot be evidenced. The spec makes verifiability a
  requirement, not a preference.
- **Duplicate project content across Projects and Open Source** -> Make
  Projects the single source and convert Open Source to a summary + links.
- **Navigation churn confusing returning visitors** -> Preserve all existing
  paths and sections except the roadmap; verify with `uv run mkdocs build
  --strict` and a manual old-URL check.
- **The removed `/roadmap/` URL 404s for anyone who bookmarked it** -> Tracked
  as an open question; a one-entry `mkdocs-redirects` resolves it if we accept
  the dependency.
- **Broken personal-site link until that site exists** -> Keep the URL in
  `extra`; ship the link only once a real target is known (tracked as an open
  question).
- **Showcase styling fights the Material theme** -> Build on existing grid-card
  and table patterns already themed in `extra.css`.
- **A bespoke landing component could fight the theme** -> Use the theme's
  documented grid-card layout and a single placeholder image, so the landing is
  built from supported patterns and is easy to update when real imagery lands.

## Migration Plan

1. Build and check locally: `uv run mkdocs build --strict`, review nav and links.
2. Deploy through the existing `pages.yml` workflow on merge (no pipeline change).
3. Rollback: revert the change commit; `gh-deploy` rebuilds the previous site.

## Open Questions

- Final personal-site domain/URL (needed before the cross-link is enabled).
- Real imagery for the featured-project cards (a generic placeholder ships first).
- Whether all fifteen deep dives remain the right cut, or any is merged or split later.
- Whether to add a one-entry redirect for the removed `/roadmap/` URL.
- Which impact metrics to gather and their source, as a follow-up change.
