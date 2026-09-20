# Tasks

## 1. Foundations and navigation

- [x] 1.1 Add `extra.personal_site_url` to `mkdocs.yml` (placeholder target) and verify `uv run mkdocs build --strict` still passes
- [x] 1.2 Restructure the `mkdocs.yml` `nav` into four destinations (Home, Projects, Platform, Open Source & Lessons), grouping architecture, cluster setup, and services under Platform and putting Open Source and Lessons Learned together under Open Source & Lessons; remove the Roadmap entry and the separate Overview destination, and verify all preserved page paths still exist

## 2. Selling landing (the case study)

- [x] 2.1 Lead `docs/index.md` with the claim, a one-line value proposition, headline metrics, and prominent actions into the projects and the platform; verify the claim is visible without scrolling
- [x] 2.2 Present the flagship projects as an illustrated card grid with a link to each deep dive
- [x] 2.3 Add an open-source stack strip as an early credibility signal
- [x] 2.4 Present the condensed case-study content in alternating full-bleed brand bands (dark/cream) that use fixed brand colours in both theme modes
- [x] 2.5 Present the enterprise practices as cards covering the thirteen practices, linking to the relevant technical documentation
- [x] 2.6 Present proof points as stat cards, each traceable to the live cluster, a repository, or another public source
- [x] 2.7 Add a lessons pull-quote and the three-bullet "What's next" block; verify no figure or promise cannot be evidenced
- [x] 2.8 Remove the separate `docs/overview/` page after folding its important content into the landing; verify no page or nav entry links to the removed URL

## 3. Projects catalogue (15 cards, 15 deep dives)

- [x] 3.1 Update `docs/projects/index.md` so all 15 use cases are cards grouped into Data & Analytics, AI & Agents, Platform & Operations, and Open Source & Lessons, and every card links to its own deep-dive page
- [x] 3.2 Write the deep-dive case studies for all 15 use cases (lakehouse-core, bodega, personal-finance, semantic-layer, data-quality-lineage, sre-agents, mcp-platform, oracle-responder, ai-content-engine, local-inference, cloud-at-home, gitops-platform, observability, oss-charts, vendor-risk) with problem, approach, technologies, outcome, and source link; verify each page builds and its source link is valid
- [x] 3.3 Review the bodega and personal-finance pages and any assets to confirm no real shopping or banking rows are published; verify only method, schema, and aggregate outcomes appear
- [x] 3.4 Replace catalogue restatements with links for cards that overlap a Services page; verify no section duplicates an existing docs page
- [x] 3.5 Remove `docs/roadmap.md` after confirming every completed item is represented as a Projects card; verify the catalogue covers the shipped work before deletion
- [x] 3.6 Slim `docs/open-source/index.md` to a short list linking to the Projects cards instead of restating; verify no duplicated narrative remains

## 4. Visuals, cross-linking, and brand

- [x] 4.1 Add the personal-site cross-link to a persistent region using the `extra.personal_site_url` macro; verify it renders in both light and dark schemes
- [x] 4.2 Add styles for the hero, stack strip, work cards, practice cards, stat cards, bands, quote, and cross-link to `docs/stylesheets/extra.css` reusing existing brand variables; verify new components use only existing tokens
- [x] 4.3 Create distinct abstract on-brand illustrations for the featured projects and wire them into the cards; verify they render and the grids stack on mobile
- [x] 4.4 Verify both colour schemes render the new showcase components, including the fixed-palette bands, correctly in a local build

## 5. Verification and release

- [x] 5.1 Run `uv run mkdocs build --strict` and resolve all warnings
- [x] 5.2 Regression-check previously published URLs (architecture, cluster_setup, services, open-source, lessons-learned) still resolve after the change, and confirm the intended behaviour of the removed `/roadmap/` URL
- [x] 5.3 Verify every pre-existing documentation section is reachable within two navigation steps from the site root
- [ ] 5.4 Deploy through the existing `pages.yml` workflow and confirm the showcase pages and cross-link are live
