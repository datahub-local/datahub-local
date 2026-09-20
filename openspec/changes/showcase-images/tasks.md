# Tasks

## 1. Tooling and prompts

- [ ] 1.1 Add the image-generation script under the repository's tooling and add `httpx` to `pyproject.toml`; verify `uv run <command> --help` runs and `uv run ruff check .` passes
- [ ] 1.2 Create `docs/assets/img/showcase/prompts.yaml` with a shared brand preamble and one entry for each of the 21 images (6 deep-dive heroes, 15 card covers); verify every project slug from the `showcase-microsite` catalogue has an entry and the script fails on an unknown slug
- [ ] 1.3 Implement the gateway call to `/v1/images/generations` with the model as a per-request parameter and the gateway URL and key read from the environment; verify a list/dry-run mode makes no network call and a missing URL or key raises a named error
- [ ] 1.4 Implement asset writing and the manifest (slug, file, model, prompt hash); verify regenerating one slug writes only that file and records it in the manifest

## 2. Generate and review

- [ ] 2.1 Generate all 21 images into `docs/assets/img/showcase/<group>/`; verify 21 files exist and the manifest lists each with a model and prompt hash
- [ ] 2.2 Review the generated set for the brand palette, consistent composition, absence of required text, and absence of real personal data; verify any rejected image is regenerated and replaced before commit
- [ ] 2.3 Exercise the failure path with an unavailable gateway and an unknown slug; verify the command exits non-zero naming the project and writes no file, leaving any existing asset untouched

## 3. Wire into the showcase pages

- [ ] 3.1 Add card cover images with descriptive alt text to the Projects catalogue and to the landing's featured projects; verify the build succeeds and every card image resolves
- [ ] 3.2 Add hero images with descriptive alt text to the six deep-dive case studies; verify the build succeeds and each page displays its hero
- [ ] 3.3 Confirm the bodega and personal-finance images depict no real rows or account details; verify only abstract representations appear

## 4. Verification and release

- [ ] 4.1 Run `uv run mkdocs build --strict` and resolve all warnings
- [ ] 4.2 Build the site without access to the gateway and verify it succeeds with all images resolved from committed assets
- [ ] 4.3 Deploy through the existing `pages.yml` workflow and confirm the images and their alt text are live on the showcase pages
