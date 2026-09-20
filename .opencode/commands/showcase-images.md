---
description: "Add a showcase project's cover and hero images, or regenerate catalogued images, via the LiteLLM gateway"
---

Add or regenerate showcase imagery from the prompts stored in the skill's config.

Use the `showcase-image-generator` skill and follow it exactly. It owns the
interview, the generation call, the best-of-N review, the asset and manifest
writes, and provenance.

Arguments: a project slug to add or regenerate one image pair, or `--all` to
regenerate the whole set. With no argument, the skill adds a new project: it asks
the questions an entry needs, writes them to the catalog, then generates.

Never regenerate an image that was not asked for. With no arguments the default
is to add a project, not to refresh existing assets. Generation is a paid
external call: `--all` needs an explicit request, every image is reviewed before
committing, and the script writes no file for a failed project.
