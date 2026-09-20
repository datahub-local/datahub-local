# Proposal

## Why

The showcase refactor (`showcase-microsite`) turns the site into a portfolio of
data and AI projects, but a text-only portfolio undersells the work. One strong,
brand-consistent image per project makes the showcase memorable and signals craft.
The cluster already runs a LiteLLM gateway with image-generation models, so the
visuals can be produced on-brand from the same AI stack the site describes.

## What Changes

- Add a **repeatable image-generation capability**: a script that reads staged
  prompts, calls the LiteLLM gateway's image-generation endpoint, and writes the
  resulting assets into the site's image tree. Prompts live in the repository so
  any image can be regenerated or revised without a design tool.
- Expose that capability as a **skill and a slash command**
  (`showcase-image-generator`, `/showcase-images`) so future regeneration is one
  documented command, and `showcase-maintainer` can reuse the same path.
- Generate **26 brand-consistent images**: a cover for thirteen of the fourteen
  project cards and a hero for thirteen of the fourteen deep-dive case studies.
  Cloud-at-home keeps the existing real cluster photograph
  (`homelab_20260920_ai.jpg`) for both surfaces.
- Produce them with **`google/gemini-3.1-flash-image`** through the gateway, the
  model already proven on this path by the n8n diagram generator.
- Adopt one **art direction**: an abstract dark-studio still life, cream and moss
  on a `#0E1116` ground, 16:9 covers, 21:9 heroes, and **no text in the image**
  (generated lettering is unreliable).
- Wire the images into the showcase pages (landing, the Projects catalogue cards,
  and each deep-dive page) with meaningful alt text.
- Record **provenance** for every asset: model, provider, prompt hash, and date
  in a manifest and in the file metadata.
- Preserve the showcase's personal-data constraint: images MUST NOT depict real
  shopping or banking rows.
- Keep generation optional to the site build: the site builds and deploys from
  committed assets without calling any model.

## Capabilities

### New Capabilities

- `showcase-imagery`: brand-consistent, model-generated imagery for the showcase,
  a repeatable generation path from stored prompts (surfaced as a skill and a
  command), the asset layout, provenance, and the rules that bind images to
  showcase pages.

### Modified Capabilities

<!-- No requirement changes here. `showcase-microsite` was archived; its
     capability now lives at `openspec/specs/project-showcase/spec.md`. -->

## Impact

- New generation tooling: the `showcase-image-generator` skill and the
  `/showcase-images` command under `.opencode/`, its config and script under
  `.opencode/skills/showcase-image-generator/`, and new Python dependencies
  (`httpx`, `Pillow`, `PyYAML`, `c2pa`) in the site's `pyproject.toml` (today it
  only carries MkDocs plugins).
- New assets under `docs/assets/img/showcase/`, plus image references in the
  showcase pages. Cloud-at-home's card and hero keep using
  `docs/assets/img/homelab_20260920_ai.jpg`.
- Builds on the archived `showcase-microsite` change; page structure and project
  slugs now live in `openspec/specs/project-showcase/spec.md`.
- Prompts and the manifest live at
  `.opencode/skills/showcase-image-generator/config/`, outside the published
  `docs/` tree.
- External dependencies: the LiteLLM gateway and its OpenRouter-backed
  image-generation models. Image generation is a paid upstream call.
- No runtime services are affected. This is a static MkDocs site plus an offline
  generation script.
