---
name: showcase-image-generator
description: Add a showcase project's cover and hero images, or regenerate an image already catalogued, through the LiteLLM gateway from stored prompts. Use when the user says "add images for <project>", "generate art for the new project", "regenerate the bodega image", "refresh the hero art", or runs /showcase-images.
allowed-tools: Bash(uv:*), Bash(git:*), Bash(gh:*)
license: Apache-2.0
compatibility: Requires LITELLM_BASE_URL and LITELLM_API_KEY in the environment, uv with the project dependencies, and network access to the gateway.
metadata:
  author: datahub-local
  version: "1.0"
---

# Showcase image generator

Generate the on-brand cover and hero images for the showcase projects. The
prompts and the art direction live in `config/prompts.yaml`; the script is the
contract; this skill is the judgement around it.

The skill has two intents. **Add a project** is the default: the project has no
catalog entry yet, so you interview the user for the fields an entry needs, write
them to the catalog, and generate. **Regenerate** is explicit: the user (or the
`site-content-maintainer`, for one named slug) asked for an existing image to be
redone.

**Never regenerate an existing asset unless it was asked for.** A plain
invocation, or an add request, must not touch any image that already exists.

## Inputs

- `config/prompts.yaml`: the shared brand preamble, the negatives, the groups,
  and one entry per generated image (13 covers, 13 heroes). cloud-at-home is
  declared under `static` and reuses `docs/assets/img/homelab_20260920_ai.jpg`
  instead of generating.
- `config/manifest.yaml`: the record of what was generated (model, provider,
  seed, prompt hash, date, licence, file). The script writes it.
- Environment: `LITELLM_BASE_URL` and `LITELLM_API_KEY`. There is no default, so
  a missing value fails loudly rather than guessing a host.

## Commands

Run from the repository root. The script never edits the catalog; you do.

```bash
S=.opencode/skills/showcase-image-generator/scripts
uv run python $S/generate.py --check            # coverage only, no network
uv run python $S/generate.py --all --dry-run    # list every image, no network
uv run python $S/generate.py <slug> --dry-run   # list one project, no network
uv run python $S/generate.py <slug>             # generate one project (cover + hero)
uv run python $S/generate.py --all              # regenerate the whole set (paid)
uv run python $S/generate.py --reencode         # shrink assets to the surface caps
uv run python $S/generate.py --self-test        # offline end-to-end check
```

Generation is a paid upstream call billed per output token, so resolution drives
cost. Covers are generated at `512` and heroes at `1K`, and one candidate per
image is the default, making a full set 26 calls; each extra candidate adds 26.
Only run `--all` when the user explicitly asks for the whole set, and state the
scope and cost first.

## Intent: add a project (default)

Use this when the user wants imagery for a project that is not yet in the
catalog, or invokes the skill without naming an image to regenerate.

1. Confirm the catalog state. Search `config/prompts.yaml` for the project slug.
   If it already has entries, this is a regenerate, so switch to that intent and
   require an explicit request.
2. Interview the user with the questions in `## Questions to add a project` and
   collect every field. Do not invent a prompt, a group, or alt text.
3. Append the project's `cover` and `hero` entries to `config/prompts.yaml`,
   under the matching group's comment block, following the shape of the
   neighbouring entries. `prompt` is the subject only; the shared preamble and
   negatives are applied by the script. `alt` is the visitor-facing description.
4. `uv run python $S/generate.py --check`: it fails if any catalogued project
   lacks a cover or a hero.
5. `uv run python $S/generate.py <slug> --dry-run`: show the user exactly what
   will be produced, and confirm before spending.
6. `uv run python $S/generate.py <slug>`: generate cover and hero for that
   project only.
7. Review the assets (see `## Review before committing`), edit the prompts and
   rerun the slug if a surface is rejected.
8. Wire the images into the pages: the catalogue card and the landing keep the
   icon badge plus the cover; the deep-dive page shows its hero; every `<img>`
   gets the `alt` text from `config/prompts.yaml`.
9. `uv run mkdocs build --strict`. The build never calls the gateway.

## Intent: regenerate (explicit only)

Use this only when a specific image was asked for: the user named a slug, or the
`site-content-maintainer` reported `image-maybe-stale` for one project and asked
for it to be redone.

1. Confirm the request names the target slug (or `--all`, which the user must
   have asked for explicitly).
2. If the subject needs to change, edit that entry's `prompt` and `alt` in
   `config/prompts.yaml`. Commit the prompt change with the asset.
3. `--dry-run` the exact scope, then generate only that slug.
4. Review and wire as above, then `uv run mkdocs build --strict`.

Do not regenerate a project that was not named, and do not run a general pass to
"refresh" images. A stale-image finding is a reason to ask, not to act.

## Questions to add a project

Ask, and wait for answers:

- **Slug**: the existing project slug used by the page filename, e.g.
  `lakehouse-core`.
- **Group**: one of `data-analytics`, `ai-agents`, `platform-operations`,
  `open-source` (the catalogue group the project belongs to).
- **Cover subject**: the single invented physical object the cover should show,
  in a few words; the preamble supplies the style.
- **Cover alt**: the description a visitor who cannot see it would hear.
- **Hero subject**: the wider scene for the deep-dive banner.
- **Hero alt**: its description.
- **Static reuse**: only if the project has a real photograph that represents it
  honestly; record it under `static` instead of generating, as cloud-at-home does.

Keep prompts a subject, not a sentence about the project. Read the existing
entries first and match their voice, palette, and level of detail.

## Review before committing

Reject and regenerate any image that:

- drifts off the palette (no moss-family hue, washed out, oversaturated);
- contains text, numbers, logos, watermarks, people, or faces;
- implies something untrue (a fake screenshot, a real product, real data);
- is illegible as a thumbnail at 240px, or does not read on `#0E1116`.

For a rejected image, edit its `prompt` in `config/prompts.yaml` and rerun that
slug.

## Rules

- Never regenerate an existing asset unless the request names it. The default
  intent is to add, not to overwrite.
- Never run `--all` without an explicit whole-set request; it is a paid call that
  rewrites every asset.
- Never write a file for a failed project, so a good asset is never replaced by a
  broken one.
- Never commit a PNG master; the committed WebP is the source of truth.
- Never depict real personal data (shopping invoices, bank rows). The bodega and
  personal-finance images stay abstract.
- The model is never asked to draw a logo or signature. Attribution is the
  manifest and the file metadata, and the site carries no imagery colophon.
- Keep prompts in `config/prompts.yaml`; do not hard-code prompt text in pages.
