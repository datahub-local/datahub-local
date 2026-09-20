# Design

## Context

See `proposal.md` — Why. Current state that shapes the approach:

- The site is **MkDocs Material**; pages are Markdown and the build
  (`mkdocs gh-deploy` in `.github/workflows/pages.yml`) is deterministic and
  network-free today.
- The **MOSS palette** is defined in `docs/stylesheets/extra.css`: `#0E1116`
  shell, `#F4F2EC` cream, `#5E8A3F` / `#7FAF5A` / `#A3CF7A` moss.
- Page structure and project slugs come from the `showcase-microsite` change
  (still in planning). The 21 images are one hero per deep dive (6) and one cover
  per catalogue card (15); the six deep-dive projects therefore have both.
- The cluster runs a **LiteLLM gateway** (`datahub-local-core`) with four
  image-generation models registered with `mode: image_generation`:
  `openrouter/openai/gpt-image-2.5-sunburst`,
  `openrouter/google/gemini-3.1-flash-image`,
  `openrouter/qwen/qwen-image-3-pro`, and
  `openrouter/bytedance-seed/seedream-5-0-pro`. They are reached through
  OpenRouter's unified Image API; LiteLLM's comment records that all but
  `gemini-3.1-flash-image` are absent from `/chat/completions`, so the image
  models are called on `/v1/images/generations`.
- Precedent: the n8n **Diagram Generator** already produces images through this
  gateway using `google/gemini-3.1-flash-image`, confirming the path works.
- `proposal.md` decided the model (`gemini-3.1-flash-image`), the on-brand style,
  and a repeatable script with stored prompts. This document covers how.

## Goals / Non-Goals

**Goals:**

- Generate the 21 images reproducibly from versioned prompts.
- Keep the site build offline and deterministic (assets are committed).
- Make single-image and whole-set regeneration a one-command operation.
- Keep the visuals recognisable as one family and legally attributable.

**Non-Goals:**

- Generating images during CI or page builds.
- Replacing Mermaid architecture diagrams with raster images — diagrams that must
  be accurate stay as Mermaid.
- Building a general-purpose image service or an n8n UI for this.
- Publishing any real personal data in imagery.

## Decisions

### D1 — Generate through the LiteLLM gateway, not the provider directly

Call the cluster's LiteLLM gateway at `/v1/images/generations` with
`openrouter/google/gemini-3.1-flash-image`. Rationale: the showcase should use
the AI stack it documents, the gateway centralises the provider key and budget,
and gemini-3.1-flash-image is the one image model already proven on this path by
the n8n diagram generator. Alternatives considered: calling OpenRouter directly
(bypasses the platform's own gateway and its key management) and the other three
models (`gpt-image-2.5-sunburst` is more cinematic but less brand-literal;
seedream/qwen are untested here). Model choice stays a per-request parameter so
switching is a prompt-file edit, not a code change.

### D2 — A committed Python script, run on demand

A small script under the repository's tooling calls the gateway with `httpx`,
writes assets, and is run manually. Alternatives: an n8n workflow (prompts and
prompt history would live outside the repo, and the Diagram Generator already
shows how quickly that UI grows), or generation inside CI (paid, non-deterministic,
and would couple a docs build to an external service). The script is the whole
surface: no new service, no schedule.

### D3 — Prompts stored per project, with a shared brand preamble

One data file (e.g. `docs/assets/img/showcase/prompts.yaml`) maps each project
slug to its prompt and parameters, plus a shared brand preamble that fixes the
palette, composition, and aspect ratio. Rationale: reviewable in a diff, editable
without touching code, and one place to change the look across all images. Kept
consistent with the repo's existing "config carries values" habit.

### D4 — Asset layout and format

```
  docs/assets/img/showcase/<group>/<slug>-card.<ext>   cover for a catalogue card
  docs/assets/img/showcase/<group>/<slug>-hero.<ext>   hero for a deep dive
  docs/assets/img/showcase/prompts.yaml                prompts for all images
  docs/assets/img/showcase/manifest.yaml               slug -> file, model, prompt hash
```

Group directories mirror the four catalogue groups. A raster format supported by
browsers is chosen for size (WebP preferred where the model output allows,
otherwise PNG), and one aspect ratio is fixed per surface so the grid stays even.
The manifest makes the set auditable and lets regeneration skip unchanged prompts.

### D5 — Images are decorative; the page carries the meaning

Prompts forbid text as required content, and every image gets descriptive alt
text in the page. Rationale: generated lettering is unreliable and
non-localisable, so any label a visitor needs is rendered by the site, not baked
into the pixels.

### D6 — Regeneration never publishes silently

Generation is explicit: the whole set, or a named subset. A failed or empty
response for a project aborts with a non-zero status naming it and writes no
file, so a prior good asset is never replaced by a broken one. Rationale: a paid,
non-deterministic call should not be able to quietly degrade the showcase.

### D7 — Keys never enter the repository

The script reads the gateway URL and API key from the environment (the same
credentials n8n and the agents use), with no default that could point at the
wrong host. Rationale: matches the platform's "no guessed address" rule and keeps
secrets out of git.

## Risks / Trade-offs

- **Generated images look generic or off-brand** → Enforce the palette and
  composition in the shared preamble, review each image before committing, and
  regenerate individual projects.
- **Garbled text inside images** → Ban required text in prompts; render any
  needed label as site text.
- **Non-determinism: a regenerated image changes look** → Commit the chosen
  assets; the manifest records model and prompt hash so a change is deliberate.
- **Paid per-image calls** → Generate on demand only, in a small batch, and skip
  unchanged prompts via the manifest.
- **Model/provider terms for generated assets** → Confirm the upstream image
  model's usage terms before publishing; record the chosen model in the manifest.
- **Aspect-ratio parameters differ per model** → The gateway drops non-OpenAI
  params; where an aspect ratio is needed, use the gateway's OpenRouter
  pass-through rather than assuming the OpenAI-shaped body applies it.
- **Slugs drift from `showcase-microsite`** → Generate after that change lands,
  and have the script fail on a slug with no target page.

## Migration Plan

1. Add the script, the prompt file, and the manifest.
2. Generate the set, review, and commit the chosen assets.
3. Wire images into the showcase pages (alt text included) and rebuild with
   `uv run mkdocs build --strict`.
4. Deploy through the existing `pages.yml` workflow — no pipeline change.
5. Rollback: revert the commit; the previous assets and references return.

## Open Questions

- Final aspect ratio per surface (hero vs card) after the first generation pass.
- Whether the six deep-dive projects keep distinct cover and hero images, or the
  hero is reused as the card later.
- Whether the chosen model supports a seed for closer reproducibility.
- Exact output format (WebP vs PNG) once model output is inspected.
