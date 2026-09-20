# Tasks

## 1. Tooling, prompts, and the generation surface

- [x] 1.1 Add the generation dependencies (`httpx`, `Pillow`, `PyYAML`, `c2pa`) to `pyproject.toml`; verify `uv sync` succeeds and `uv run ruff check .` passes
- [x] 1.2 Create `.opencode/skills/showcase-image-generator/config/prompts.yaml` with the shared brand preamble (palette ratio, light, camera, materials, composition, negatives) and one entry per image for the 26 images (13 covers, 13 heroes); verify cloud-at-home points at `homelab_20260920_ai.jpg`, every catalogue slug has its entries, and the script fails on an unknown slug
- [x] 1.3 Implement the gateway call to the `/openrouter/images` pass-through with the model as a per-request parameter and the gateway URL and key read from the environment, requesting the target aspect ratio and resolution in the body with a center-crop fallback; verify a list/dry-run mode makes no network call and a missing URL or key raises a named error
- [x] 1.4 Implement candidate generation (configurable, default one) with per-surface resolution, a seed when the model supports one (otherwise low temperature, recorded as no seed), a dominant-colour palette check, WebP writing capped at the surface width, the manifest (slug, file, model, provider, seed, prompt hash, date, licence, width, height), and provenance metadata (C2PA when available, otherwise XMP/EXIF); verify regenerating one slug writes only that file and records it in the manifest
- [x] 1.5 Create the `showcase-image-generator` skill (`SKILL.md`) and the `/showcase-images` command; verify the command runs a dry-run for one slug and for `--all`, and that the skill loads
- [x] 1.6 Make onboarding the skill's default intent (interview for slug, group, subject, and alt; write the catalog entry; generate that project) and regeneration explicit and named; verify a general invocation regenerates no existing asset and `--all` is refused without an explicit whole-set request

## 2. Generate and review

- [x] 2.1 Generate all 26 images into `docs/assets/img/showcase/<group>/`; verify 26 WebP files exist and the manifest lists each with a model, seed state, and prompt hash
- [x] 2.2 Build a contact sheet of the set and review it for the brand palette, one-family composition, absence of text, no logos or faces, and legibility at 240px on a `#0E1116` background; verify any rejected image is regenerated and replaced before commit
- [x] 2.3 Review the bodega and personal-finance images specifically for absence of real rows, figures, or account details; verify only abstract representations appear
- [x] 2.4 Exercise the failure path with an unavailable gateway and an unknown slug; verify the command exits non-zero naming the project and writes no file, leaving any existing asset untouched

## 3. Wire into the showcase pages

- [x] 3.1 Add a cover image and keep the icon badge on all fourteen Projects catalogue cards, with the cloud-at-home card using `homelab_20260920_ai.jpg`; verify the build succeeds and every card image resolves
- [x] 3.2 Replace the five placeholder illustrations on the landing's featured projects with their covers, keeping the cloud-at-home real photo; verify the grid renders in both colour schemes
- [x] 3.3 Add a hero image with descriptive alt text to each of the thirteen deep-dive case studies other than cloud-at-home; verify the build succeeds and each page displays its hero
- [x] 3.4 Keep attribution in the manifest and file metadata only; verify the site carries no imagery colophon or other visitor-facing imagery attribution
- [x] 3.5 Remove the replaced `project-*.svg` placeholder files, including any unused `project-cloud.svg`, after confirming none are still referenced; verify no page or stylesheet points at a removed file

## 4. Verification and release

- [x] 4.1 Run `uv run mkdocs build --strict` and resolve all warnings
- [x] 4.2 Build the site without access to the gateway and verify it succeeds with all images resolved from committed assets
- [x] 4.3 Verify the committed assets carry provenance metadata (C2PA or XMP/EXIF) and that each manifest entry matches its file
- [x] 4.4 Deploy through the existing `pages.yml` workflow and confirm the images and their alt text are live on the showcase pages
