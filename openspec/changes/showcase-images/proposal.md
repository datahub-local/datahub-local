# Proposal

## Why

The showcase refactor (`showcase-microsite`) turns the site into a portfolio of
data and AI projects, but a text-only portfolio undersells the work. One strong,
brand-consistent image per project makes the showcase memorable and signals craft
— and the cluster already runs a LiteLLM gateway with image-generation models, so
the visuals can be produced on-brand from the same AI stack the site describes.

## What Changes

- Add a **repeatable image-generation capability**: a script that reads staged
  prompts, calls the LiteLLM gateway's image-generation endpoint, and writes the
  resulting assets into the site's image tree. Prompts live in the repository so
  any image can be regenerated or revised without a design tool.
- Generate **21 brand-consistent images**: one hero for each of the six deep-dive
  case studies, and one cover for each of the fifteen project cards.
- Wire the images into the showcase pages — landing, overview, the Projects
  catalogue cards, and each deep-dive page — with meaningful alt text.
- Enforce a single visual language: the MOSS palette (`#0E1116`, `#F4F2EC`,
  `#7FAF5A`), consistent composition and aspect ratios, and **no critical text in
  the image** (generated lettering is unreliable).
- Preserve the showcase's personal-data constraint: images MUST NOT depict real
  shopping or banking rows.
- Keep generation optional to the site build: the site builds and deploys from
  committed assets without calling any model.

## Capabilities

### New Capabilities

- `showcase-imagery`: brand-consistent, model-generated imagery for the showcase —
  a repeatable generation path from stored prompts, the asset layout, and the
  rules that bind images to showcase pages.

### Modified Capabilities

<!-- No main specs exist yet; `showcase-microsite` is still an unarchived change. -->

## Impact

- New generation tooling in this repository and its Python dependencies
  (the site's `pyproject.toml` currently only carries MkDocs plugins).
- New assets under `docs/assets/`, plus image references in the showcase pages
  created by `showcase-microsite`.
- Depends on `showcase-microsite` for the page structure and project slugs.
- External dependencies: the LiteLLM gateway and its OpenRouter-backed
  image-generation models; image generation is a paid upstream call.
- No runtime services are affected — this is a static MkDocs site plus an
  offline generation script.
