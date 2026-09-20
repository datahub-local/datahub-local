# Design

## Context

See `proposal.md` — Why. Current state that shapes the approach:

- The site is **MkDocs Material**; pages are Markdown and the build
  (`mkdocs gh-deploy` in `.github/workflows/pages.yml`) is deterministic and
  network-free today.
- The **MOSS palette** is defined in `docs/stylesheets/extra.css`: `#0E1116`
  shell, `#F4F2EC` cream, `#5E8A3F` / `#7FAF5A` / `#A3CF7A` moss.
- Page structure and project slugs come from the archived `showcase-microsite`
  change, now the `project-showcase` main spec. The site has **14 catalogued
  projects, each with a full deep-dive case study**, and the landing features six
  of them. The 26 images are one hero per deep dive and one cover per catalogue
  card, except cloud-at-home, whose card and hero both keep the existing real
  photograph `docs/assets/img/homelab_20260920_ai.jpg`.
- The catalogue currently uses icon-only Material grid cards; the covers are
  added to those cards and the icons stay as a small badge.
- The cluster runs a **LiteLLM gateway** (`datahub-local-core`) with four
  image-generation models registered with `mode: image_generation`:
  `openrouter/openai/gpt-image-2.5-sunburst`,
  `openrouter/google/gemini-3.1-flash-image`,
  `openrouter/qwen/qwen-image-3-pro`, and
  `openrouter/bytedance-seed/seedream-5-0-pro`. They are reached through
  OpenRouter's unified Image API; LiteLLM's comment records that all but
  `gemini-3.1-flash-image` are absent from `/chat/completions`, so the image
  models are called on the gateway's `/openrouter/images` pass-through.
- Precedent: the n8n **Diagram Generator** already produces images through this
  gateway using `google/gemini-3.1-flash-image`, confirming the path works.
- This design fixes **`gemini-3.1-flash-image`** as the default model, chosen
  because it is the one image model already proven on this path, and the design
  targets one house style. `proposal.md` covers the motivation; this document
  covers how.

## Goals / Non-Goals

**Goals:**

- Generate the 26 images reproducibly from versioned prompts.
- Keep the site build offline and deterministic (assets are committed).
- Make adding a new project's images a guided one-command operation, and
  single-image or whole-set regeneration an explicit one.
- Keep the visuals recognisable as one family and legally attributable.

**Non-Goals:**

- Generating images during CI or page builds.
- Replacing Mermaid architecture diagrams with raster images — diagrams that must
  be accurate stay as Mermaid.
- Building a general-purpose image service or an n8n UI for this.
- Publishing any real personal data in imagery.

## Decisions

### D1 — Generate through the LiteLLM gateway, not the provider directly

POST to the cluster's LiteLLM gateway at `/openrouter/images` with the OpenRouter
model id, `google/gemini-3.1-flash-image`, and an OpenAI-shaped body carrying
`aspect_ratio` and `resolution`. Rationale: the showcase should use
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

One data file (e.g.
`.opencode/skills/showcase-image-generator/config/prompts.yaml`) maps each project
slug to its prompt and parameters, plus a shared brand preamble that fixes the
palette, composition, and aspect ratio. Rationale: reviewable in a diff, editable
without touching code, and one place to change the look across all images. Kept
consistent with the repo's existing "config carries values" habit.

### D4 — Asset layout and format

```
  docs/assets/img/showcase/<group>/<slug>-card.webp   cover for a catalogue card
  docs/assets/img/showcase/<group>/<slug>-hero.webp   hero for a deep dive
  .opencode/skills/showcase-image-generator/config/prompts.yaml    prompts for all images
  .opencode/skills/showcase-image-generator/config/manifest.yaml   slug -> file, model, seed, prompt hash, date
```

Group directories mirror the four catalogue groups. Covers are 16:9 and heroes
are 21:9, matching the existing `.work-card__art` CSS so one cover file serves
both the landing and the catalogue. Resolution is chosen per surface because the
model bills per output token and a higher tier costs several times more: covers
render small in the card grid and are generated at `512`, heroes span a deep-dive
banner and are generated at `1K`. The delivered WebP is capped at the model
output and never upscaled, so the committed files stay small. The model produces a
PNG, the script converts it to WebP for delivery, and the PNG master is not
committed, so the committed WebP is the source of truth. Prompts and the manifest
live under the skill's `config/` directory rather than `docs/`, so they are never
published. The manifest makes the set auditable and lets regeneration skip
unchanged prompts.

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

The default intent is the other direction: **onboarding a new project**, not
refreshing existing assets. The skill writes the new catalog entry first, then
generates only that project. It never regenerates an asset that was not named,
because a routine sweep that rewrites committed images would churn the "one
family" look for no gain and spend money doing it.

### D7 — Keys never enter the repository

The script reads the gateway URL and API key from the environment (the same
credentials n8n and the agents use), with no default that could point at the
wrong host. Rationale: matches the platform's "no guessed address" rule and keeps
secrets out of git.

### D8 — One art direction: abstract dark-studio still life

Every image is a still life of one invented physical object, photographed on a
dark seamless studio backdrop `#0E1116`, lit by a single moss key and a cream
rim. The prompt preamble fixes the palette ratio (about 70% dark ground, 20%
cream, 10% moss), the light, one camera per surface, a short material list (matte
ceramic, brushed metal, frosted glass, cream paper, dark stone), a centered
composition with generous negative space, and the negatives (text, letters,
numerals, logos, people, hands, faces, UI, labelled charts, borders, watermarks,
extra limbs). Per-project prompts name only the subject and its action.

Rationale: a single grammar keeps 26 images reading as one family, and the
abstract object stays honest, because nobody mistakes it for a screenshot of
software that does not exist. Alternatives considered: photoreal product shots
(drift across 26 and can imply equipment that is not there), 3D isometric
diagrams (they duplicate the Mermaid diagrams this design keeps), and editorial
surreal scenes (memorable but hard to keep uniform).

The approved metaphor slate, one per project:

| Project | Object |
| --- | --- |
| lakehouse-core | core sample of stratified translucent sediment under a calm surface |
| bodega | a blank receipt unspooling into a tidy grid of tiles, no legible lines |
| personal-finance | a sealed ledger box in frosted glass, closed, no figures |
| semantic-layer | one precision lens aligning many beams onto a single plane |
| data-quality-lineage | a root system with lit inspection nodes, one branch flagged |
| sre-agents | small matte survey drones over a dark contour field |
| mcp-platform | a docking hub with six read-only ports, no labels |
| oracle-responder | a lantern lowering into fog, motes gathering into a shape |
| ai-content-engine | a loom weaving threads of light into a page |
| local-inference | a ceramic compute block glowing like a hearth |
| cloud-at-home | the existing real cluster photograph, not generated |
| gitops-platform | concentric rings converging on one aligned notch |
| observability | a macro lens over a field of faint pulses, one ringed |
| oss-charts | a short stack of shipping crates, one open, moss light escaping |

### D9 — Generation surface: a script, a skill, and a command

```
  .opencode/skills/showcase-image-generator/scripts/generate.py   the contract
  .opencode/skills/showcase-image-generator/config/               prompts + manifest
  .opencode/skills/showcase-image-generator/SKILL.md              judgement
  .opencode/commands/showcase-images.md                           entry point
```

The script owns the deterministic work: reading prompts, calling the gateway,
generating one candidate per image by default, checking the palette, writing the
asset, updating the manifest, and attaching provenance. The candidate count is a
parameter and multiplies the paid cost, so the default is one and a rejected image
is regenerated on its own. The skill owns the judgement:
when to run, how to review (palette, no text, no logos or faces, honesty, dark
legibility), how to promote a chosen candidate, alt text, and the strict build.
The command is the explicit door. The skill carries two intents: onboarding a new
project (the default, which interviews for the entry fields and writes them to the
catalog before generating) and regenerating a named project (explicit only).
`showcase-maintainer` reuses the same path, asking for one named slug when its
image-refresh check finds a stale image, or onboarding the imagery for a card it
just added.

Rationale: a paid call that holds a secret and must not overwrite committed assets
cannot depend on an agent improvising HTTP. The script is the contract and the
skill is the review habit. This is the same split the maintainer skills use, where
`check.py` gathers and the SKILL.md carries the rules. Alternatives considered:
logic in the command body (fragile and untestable) and an n8n workflow (prompts
and history leave the repository).

### D10 — Provenance, not a visible watermark

No image carries a baked-in watermark or signature, and the site carries no
imagery colophon. Attribution is two layers: a manifest entry per image (slug,
file, model, provider, seed, prompt hash, date, licence) and embedded file
metadata (C2PA Content Credentials when the pipeline supports them, otherwise
XMP/EXIF). The model is never asked to draw a logo, because generated lettering is
unreliable and the negative prompt bans letters anyway.

Rationale: a visible mark on 26 small card images adds noise and can garble, and a
site colophon is noise a visitor does not need, while provenance in metadata
survives the build (assets are copied byte for byte) and stays machine-readable.
Alternatives considered: an icon watermark composited on heroes (possible later,
but not needed for attribution) and manifest-only provenance (loses metadata if a
file is copied out of the repository).

### D11 — The skill's default is onboarding, and the interview is the gate

The skill opens on "add a project" unless a specific image was asked for. It asks
for the slug, group, subject, and alt text, writes the entry to
`config/prompts.yaml`, then generates. Rationale: the prompts are the one
hand-authored input, and a generated prompt is not reviewable. Making the
interview the default keeps a human in the loop for the art direction while the
script stays the deterministic contract. Regeneration is a separate, named
intent, so a general run can never spend money or overwrite committed assets.

## Risks / Trade-offs

- **Generated images look generic or off-brand** → Enforce the palette and
  composition in the shared preamble, review each image before committing, and
  regenerate individual projects.
- **Palette drift across the set** → The script samples each candidate's dominant
  colours and fails review if no moss-family hue is present.
- **Catalogue card markup change breaks the grid** → Keep the existing icon as a
  small badge beside the image and verify the grid in both colour schemes.
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
- **Slugs drift from the catalogue** → Read slugs from the `project-showcase` spec
  and the live `docs/projects/` tree, and have the script fail on a slug with no
  target page.

## Migration Plan

1. Add the skill, the `/showcase-images` command, the script, the prompt file,
   and the manifest.
2. Generate the 26 images, build a contact sheet, review, and commit the chosen
   assets.
3. Wire images into the showcase pages (the catalogue cards, the six landing
   cards, the 14 deep-dive heroes, and alt text) and rebuild with
   `uv run mkdocs build --strict`.
4. Deploy through the existing `pages.yml` workflow. No pipeline change.
5. Rollback: revert the commit; the previous assets and references return.

## Open Questions

- Whether the deployed gateway honors the OpenRouter aspect-ratio passthrough, or
  whether the center-crop fallback is the path in practice (verified in task 1.3).
- Whether the model exposes a seed or attaches C2PA (verified in task 1.4).
