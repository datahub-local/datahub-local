"""Generate the showcase project imagery through the LiteLLM gateway.

This script is the contract behind the `showcase-image-generator` skill and the
`/showcase-images` command. It reads prompts from `config/prompts.yaml`, calls
the gateway's OpenRouter image passthrough, and writes WebP assets plus a
manifest entry per image.

Nothing here publishes on its own: a failed or empty gateway response aborts
with a non-zero status naming the project and writes no file.

Usage:
    uv run python .opencode/skills/showcase-image-generator/scripts/generate.py --check
    uv run python .opencode/skills/showcase-image-generator/scripts/generate.py --all --dry-run
    uv run python .opencode/skills/showcase-image-generator/scripts/generate.py lakehouse-core
    uv run python .opencode/skills/showcase-image-generator/scripts/generate.py --all
    uv run python .opencode/skills/showcase-image-generator/scripts/generate.py --self-test
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import io
import json
import os
import sys
from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
REPO_ROOT = SCRIPTS_DIR.parents[3]
CONFIG_PATH = SKILL_DIR / "config" / "prompts.yaml"
MANIFEST_PATH = SKILL_DIR / "config" / "manifest.yaml"

GATEWAY_URL_ENV = "LITELLM_BASE_URL"
GATEWAY_KEY_ENV = "LITELLM_API_KEY"
C2PA_CERT_ENV = "C2PA_SIGNING_CERT"
C2PA_KEY_ENV = "C2PA_SIGNING_KEY"

LICENCE_DEFAULT = "to-verify"
CREATOR_TOOL = "datahub-local showcase-image-generator"


class GenerationError(Exception):
    """A named, reportable failure for one project image."""


def load_config(path: Path = CONFIG_PATH) -> dict:
    with path.open() as fh:
        cfg = yaml.safe_load(fh)
    if not isinstance(cfg, dict) or "images" not in cfg:
        raise SystemExit(f"invalid prompts config at {path}")
    return cfg


def catalogue(cfg: dict) -> dict[str, list[dict]]:
    """Slug -> its generated image entries (zero or more), from the config."""
    by_slug: dict[str, list[dict]] = {}
    for entry in cfg["images"]:
        by_slug.setdefault(entry["slug"], []).append(entry)
    for entry in cfg.get("static", []):
        by_slug.setdefault(entry["slug"], [])
    return by_slug


def asset_path(cfg: dict, entry: dict) -> Path:
    return (
        REPO_ROOT
        / cfg["assets_dir"]
        / entry["group"]
        / f"{entry['slug']}-{entry['surface']}.webp"
    )


def build_prompt(cfg: dict, entry: dict) -> str:
    parts = [cfg["preamble"].strip(), entry["prompt"].strip()]
    note = (cfg.get("surface_notes") or {}).get(entry["surface"], "")
    if note and note.strip():
        parts.append(note.strip())
    parts.append(f"Avoid: {cfg['negatives'].strip()}")
    return "\n\n".join(parts)


def prompt_hash(prompt: str) -> str:
    return "sha256:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    if not path.exists():
        return {"version": 1, "images": {}}
    with path.open() as fh:
        data = yaml.safe_load(fh) or {}
    data.setdefault("version", 1)
    data.setdefault("images", {})
    return data


def save_manifest(manifest: dict, path: Path = MANIFEST_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        yaml.safe_dump(manifest, fh, sort_keys=True, allow_unicode=True)


def require_gateway_env() -> tuple[str, str]:
    base = os.environ.get(GATEWAY_URL_ENV)
    key = os.environ.get(GATEWAY_KEY_ENV)
    missing = [n for n, v in ((GATEWAY_URL_ENV, base), (GATEWAY_KEY_ENV, key)) if not v]
    if missing:
        raise SystemExit(
            "missing environment: "
            + ", ".join(missing)
            + " (the gateway URL and key are never defaulted)"
        )
    return base.rstrip("/"), key


def call_gateway(base: str, key: str, path: str, body: dict, timeout: float = 180.0):
    import httpx

    url = base + path
    resp = httpx.post(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=body,
        timeout=timeout,
    )
    if resp.status_code >= 400:
        raise GenerationError(f"gateway HTTP {resp.status_code}: {resp.text[:300]}")
    payload = resp.json()
    items = payload.get("data") or []
    if not items:
        raise GenerationError("gateway returned no image")
    item = items[0]
    b64 = item.get("b64_json")
    if not b64:
        raise GenerationError("gateway response had no b64_json")
    return base64.b64decode(b64), item.get("media_type", "image/png")


def center_crop(img, ratio: float):
    w, h = img.size
    current = w / h
    if abs(current - ratio) / ratio < 0.005:
        return img
    if current > ratio:
        new_w = round(h * ratio)
        x = (w - new_w) // 2
        return img.crop((x, 0, x + new_w, h))
    new_h = round(w / ratio)
    y = (h - new_h) // 2
    return img.crop((0, y, w, y + new_h))


def moss_fraction(img) -> float:
    """Fraction of pixels that sit in the moss-green hue band."""
    small = img.convert("RGB").resize((64, 64))
    hits = 0
    total = 64 * 64
    data = small.tobytes()
    for i in range(0, len(data), 3):
        r, g, b = data[i], data[i + 1], data[i + 2]
        mx, mn = max(r, g, b), min(r, g, b)
        if mx == mn:
            continue
        sat = (mx - mn) / mx
        if sat < 0.15:
            continue
        hue = 0.0
        if mx == r:
            hue = (60 * ((g - b) / (mx - mn))) % 360
        elif mx == g:
            hue = 60 * ((b - r) / (mx - mn)) + 120
        else:
            hue = 60 * ((r - g) / (mx - mn)) + 240
        if 70 <= hue <= 160:
            hits += 1
    return hits / total


def dark_fraction(img) -> float:
    small = img.convert("L").resize((64, 64))
    dark = sum(1 for p in small.tobytes() if p < 70)
    return dark / (64 * 64)


def build_xmp(meta: dict) -> bytes:
    def esc(value: str) -> str:
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    packet = f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
    xmlns:showcase="https://datahub-local.alvsanand.com/ns/1.0/">
   <dc:description><rdf:Alt><rdf:li xml:lang="x-default">{esc(meta['alt'])}</rdf:li></rdf:Alt></dc:description>
   <xmp:CreatorTool>{esc(CREATOR_TOOL)}</xmp:CreatorTool>
   <showcase:model>{esc(meta['model'])}</showcase:model>
   <showcase:provider>{esc(meta['provider'])}</showcase:provider>
   <showcase:promptHash>{esc(meta['prompt_hash'])}</showcase:promptHash>
   <showcase:generated>{esc(meta['date'])}</showcase:generated>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>"""
    return packet.encode("utf-8")


def build_exif(meta: dict):
    from PIL import Image

    exif = Image.Exif()
    exif[0x010E] = meta["alt"]  # ImageDescription
    exif[0x0131] = CREATOR_TOOL  # Software
    exif[0x013B] = "datahub-local"  # Artist
    return exif


def write_asset(img, path: Path, width: int, meta: dict) -> tuple[int, int]:
    from PIL import Image

    # `width` is a ceiling, not a target: never upscale a smaller model output.
    if img.width > width:
        height = round(img.height * width / img.width)
        img = img.resize((width, height), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    exif = build_exif(meta)
    xmp = build_xmp(meta)
    try:
        img.save(path, "WEBP", quality=82, method=6, exif=exif, xmp=xmp)
    except (TypeError, ValueError):
        # Older Pillow builds do not accept xmp on WebP; EXIF still carries it.
        img.save(path, "WEBP", quality=82, method=6, exif=exif)
    return img.size


def attach_c2pa(path: Path, meta: dict) -> str:
    """Best-effort C2PA. Needs a signing certificate and key in the env."""
    cert = os.environ.get(C2PA_CERT_ENV)
    key = os.environ.get(C2PA_KEY_ENV)
    if not cert or not key:
        return "xmp/EXIF (c2pa skipped: no signing certificate)"
    try:
        import c2pa

        manifest = {
            "claim_generator": CREATOR_TOOL,
            "title": path.name,
            "assertions": [
                {
                    "label": "c2pa.actions",
                    "data": {
                        "actions": [
                            {
                                "action": "c2pa.created",
                                "softwareAgent": CREATOR_TOOL,
                            }
                        ]
                    },
                }
            ],
        }
        with path.open("rb") as src, io.BytesIO(src.read()) as data:
            signed = c2pa.sign(
                data,
                manifest,
                cert,
                key,
                "image/webp",
            )
        path.write_bytes(signed)
        return "c2pa+xmp/EXIF"
    except Exception as exc:  # noqa: BLE001 - fall back, never fail the asset
        return f"xmp/EXIF (c2pa failed: {type(exc).__name__})"


def generate_entry(cfg, entry, base, key, seed=None):
    from PIL import Image

    surface = cfg["surfaces"][entry["surface"]]
    prompt = build_prompt(cfg, entry)
    body = {
        "model": cfg["model"]["name"],
        "prompt": prompt,
        "aspect_ratio": surface["aspect_ratio"],
        "resolution": surface.get("resolution", cfg["defaults"]["resolution"]),
        "temperature": cfg["defaults"]["temperature"],
    }
    if seed is not None:
        body["seed"] = seed
    raw, media_type = call_gateway(base, key, cfg["gateway"]["images_path"], body)
    img = Image.open(io.BytesIO(raw))
    img.load()
    ratio = surface["width"] / surface["height"]
    img = center_crop(img, ratio)
    return img, prompt, media_type


def plan(
    cfg: dict, slugs: list[str] | None, all_images: bool, surface: str | None = None
) -> list[dict]:
    by_slug = catalogue(cfg)
    if all_images:
        entries = list(cfg["images"])
    else:
        selected: list[dict] = []
        for slug in slugs or []:
            if slug not in by_slug:
                raise SystemExit(f"unknown slug: {slug}")
            if not by_slug[slug]:
                continue  # static asset (e.g. cloud-at-home); nothing to generate
            selected.extend(by_slug[slug])
        entries = selected
    if surface:
        entries = [e for e in entries if e["surface"] == surface]
    if not entries:
        raise SystemExit("nothing to generate: pass one or more slugs or --all")
    return entries


def run(cfg, entries, base, key, manifest, manifest_path, candidates):
    failures: list[str] = []
    for entry in entries:
        label = f"{entry['slug']}/{entry['surface']}"
        best = None
        best_score = -1.0
        try:
            for i in range(candidates):
                img, prompt, media_type = generate_entry(cfg, entry, base, key)
                score = moss_fraction(img) * 3 + dark_fraction(img)
                if best is None or score > best_score:
                    best, best_score = (img, prompt, media_type), score
            img, prompt, _ = best
        except GenerationError as exc:
            failures.append(label)
            print(f"FAIL {label}: {exc}", file=sys.stderr)
            continue
        except Exception as exc:  # noqa: BLE001 - named per project
            failures.append(label)
            print(f"FAIL {label}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue

        surface = cfg["surfaces"][entry["surface"]]
        path = asset_path(cfg, entry)
        now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
        meta = {
            "alt": entry["alt"],
            "model": cfg["model"]["name"],
            "provider": cfg["model"]["provider"],
            "prompt_hash": prompt_hash(prompt),
            "date": now,
        }
        final_size = write_asset(img, path, surface["width"], meta)
        provenance = attach_c2pa(path, meta)
        manifest["images"][label] = {
            **meta,
            "file": str(path.relative_to(REPO_ROOT)),
            "width": final_size[0],
            "height": final_size[1],
            "seed": None,
            "licence": cfg["model"].get("licence", LICENCE_DEFAULT),
            "provenance": provenance,
            "moss_fraction": round(moss_fraction(img), 3),
        }
        # Persist after each image so an interruption cannot leave a file with no
        # manifest entry.
        save_manifest(manifest, manifest_path)
        print(
            f"OK   {label}: moss={moss_fraction(img):.3f} -> {path.relative_to(REPO_ROOT)}"
        )
    save_manifest(manifest, manifest_path)
    return failures


def cmd_check(cfg: dict) -> int:
    by_slug = catalogue(cfg)
    problems = []
    for slug, entries in by_slug.items():
        surfaces = {e["surface"] for e in entries}
        static = [s for s in cfg.get("static", []) if s["slug"] == slug]
        if static:
            surfaces |= set(static[0]["surfaces"])
        if surfaces != {"cover", "hero"}:
            problems.append(f"{slug}: has {sorted(surfaces)}")
    if problems:
        print("coverage problems:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1
    print(f"coverage ok: {len(by_slug)} projects, {len(cfg['images'])} generated images")
    return 0


def cmd_dry_run(cfg: dict, entries: list[dict]) -> int:
    for entry in entries:
        surface = cfg["surfaces"][entry["surface"]]
        path = asset_path(cfg, entry).relative_to(REPO_ROOT)
        print(
            f"[dry-run] {entry['slug']}/{entry['surface']} "
            f"{surface['aspect_ratio']} {surface.get('resolution', '?')} "
            f"<= {surface['width']}px -> {path}"
        )
    print(f"[dry-run] {len(entries)} image(s); no network call")
    return 0


def cmd_reencode(cfg: dict, manifest: dict, manifest_path: Path) -> int:
    """Shrink already-generated assets to the current per-surface ceilings."""
    from PIL import Image

    if not manifest["images"]:
        print("manifest is empty; nothing to re-encode")
        return 0
    for label, meta in manifest["images"].items():
        _, _, surface_name = label.partition("/")
        surface = cfg["surfaces"].get(surface_name)
        path = REPO_ROOT / meta["file"]
        if surface is None or not path.exists():
            print(f"SKIP {label}: no surface config or missing file")
            continue
        img = Image.open(path)
        img.load()
        img = center_crop(img, surface["width"] / surface["height"])
        size = write_asset(img, path, surface["width"], meta)
        meta["width"], meta["height"] = size
        print(f"OK   {label}: {size[0]}x{size[1]}")
    save_manifest(manifest, manifest_path)
    return 0


def cmd_self_test() -> int:
    """End-to-end run against a local fake gateway. No network, no key."""
    import tempfile
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    from PIL import Image

    buf = io.BytesIO()
    img = Image.new("RGB", (640, 360), (14, 17, 22))
    for x in range(200, 440):
        for y in range(120, 240):
            img.putpixel((x, y), (127, 175, 90))
    img.save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            self.rfile.read(length)
            body = json.dumps(
                {"data": [{"b64_json": b64, "media_type": "image/png"}]}
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = load_config()
            cfg["assets_dir"] = os.path.relpath(tmp, REPO_ROOT)
            manifest_path = Path(tmp) / "manifest.yaml"
            entry = next(e for e in cfg["images"] if e["slug"] == "observability")
            os.environ[GATEWAY_URL_ENV] = f"http://127.0.0.1:{server.server_port}"
            os.environ[GATEWAY_KEY_ENV] = "self-test"
            failures = run(
                cfg, [entry], os.environ[GATEWAY_URL_ENV], "self-test",
                {"version": 1, "images": {}}, manifest_path, candidates=2,
            )
            assert not failures, failures
            written = list(Path(tmp).rglob("*.webp"))
            assert len(written) == 1, written
            loaded = load_manifest(manifest_path)
            key = f"{entry['slug']}/{entry['surface']}"
            assert key in loaded["images"], loaded
            assert loaded["images"][key]["prompt_hash"].startswith("sha256:")
        print("self-test ok")
        return 0
    finally:
        server.shutdown()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="project slugs to (re)generate")
    parser.add_argument("--all", action="store_true", help="generate every image")
    parser.add_argument("--dry-run", action="store_true", help="list without calling")
    parser.add_argument("--check", action="store_true", help="validate coverage only")
    parser.add_argument("--self-test", action="store_true", help="run offline")
    parser.add_argument(
        "--reencode",
        action="store_true",
        help="shrink existing assets to the current surface ceilings",
    )
    parser.add_argument(
        "--surface", choices=["cover", "hero"], help="limit to one surface"
    )
    parser.add_argument("--candidates", type=int, default=None)
    args = parser.parse_args(argv)

    if args.self_test:
        return cmd_self_test()

    cfg = load_config()

    if args.check:
        return cmd_check(cfg)

    if args.reencode:
        return cmd_reencode(cfg, load_manifest(), MANIFEST_PATH)

    entries = plan(cfg, args.slugs, args.all, args.surface)

    if args.dry_run:
        return cmd_dry_run(cfg, entries)

    base, key = require_gateway_env()
    candidates = args.candidates or cfg["defaults"]["candidates"]
    manifest = load_manifest()
    failures = run(cfg, entries, base, key, manifest, MANIFEST_PATH, candidates)
    if failures:
        print(f"\n{len(failures)} failure(s): {', '.join(failures)}", file=sys.stderr)
        return 1
    print(f"\n{len(entries)} image(s) generated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
