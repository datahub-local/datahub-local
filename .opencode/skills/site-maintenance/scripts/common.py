"""Shared helpers for the site maintainer skills.

Everything here is read-only: it gathers facts and parses files. No helper in
this module writes to any source. Delivery lives in publish.py.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS_DIR.parent
CONFIG_PATH = SKILL_DIR / "config" / "sources.yaml"


def repo_root() -> Path:
    """The site repository root (the directory that owns .opencode)."""
    env = os.environ.get("SITE_MAINTAINER_ROOT")
    if env:
        return Path(env).resolve()
    # scripts/ -> site-maintenance/ -> skills/ -> .opencode/ -> repo root
    return Path(__file__).resolve().parents[4]


def load_config() -> dict:
    import yaml  # provided by the project's mkdocs dependency tree

    with CONFIG_PATH.open() as fh:
        cfg = yaml.safe_load(fh)
    if not isinstance(cfg, dict):
        raise SystemExit(f"invalid config at {CONFIG_PATH}")
    return cfg


def resolve_config_path(spec: dict) -> Path | None:
    """Resolve a {default, env} path entry relative to the site root."""
    if not spec:
        return None
    env_name = spec.get("env")
    if env_name and os.environ.get(env_name):
        return Path(os.environ[env_name]).expanduser().resolve()
    default = spec.get("default")
    if not default:
        return None
    p = Path(default).expanduser()
    if not p.is_absolute():
        p = repo_root() / p
    return p.resolve()


def run(cmd: list[str], timeout: int = 60, cwd: Path | None = None) -> dict:
    """Run a command, never raising. Returns rc/stdout/stderr/found."""
    exe = shutil.which(cmd[0])
    if exe is None:
        return {"found": False, "rc": None, "stdout": "", "stderr": f"{cmd[0]} not found"}
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "found": True,
            "rc": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"found": True, "rc": None, "stdout": "", "stderr": f"timeout after {timeout}s"}


def run_json(cmd: list[str], timeout: int = 60, cwd: Path | None = None):
    """Run a command that prints JSON. Returns (value, error)."""
    res = run(cmd, timeout=timeout, cwd=cwd)
    if not res["found"]:
        return None, res["stderr"]
    if res["rc"] != 0:
        return None, (res["stderr"] or res["stdout"]).strip() or f"exit {res['rc']}"
    try:
        return json.loads(res["stdout"]), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON from {' '.join(cmd)}: {exc}"


def load_yaml_file(path: Path):
    import yaml

    with path.open() as fh:
        return yaml.safe_load(fh)


def emit(obj) -> None:
    json.dump(obj, sys.stdout, indent=2, sort_keys=True, default=str)
    sys.stdout.write("\n")


LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMG_RE = re.compile(r"<img[^>]*\bsrc=\"([^\"]+)\"")


def markdown_links(md_path: Path):
    """Yield (kind, target) for markdown links and images in a file."""
    text = md_path.read_text(encoding="utf-8", errors="replace")
    for bang, target in LINK_RE.findall(text):
        yield ("image" if bang == "!" else "link", target)
    for target in HTML_IMG_RE.findall(text):
        yield ("image", target)


def is_external(target: str) -> bool:
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target)) or target.startswith("//")


def org_of(full_name: str) -> str:
    return full_name.split("/", 1)[0]


def repo_of(full_name: str) -> str:
    return full_name.split("/", 1)[1]
