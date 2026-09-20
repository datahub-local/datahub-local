#!/usr/bin/env python3
"""Safe, idempotent delivery for the site maintainer.

Usage:
    publish.py --domain content|platform|services [--dry-run]
               [--title T] [--summary-file PATH]

Stages only site files (docs/ and mkdocs.yml), builds the site, and proposes a
pull request on a per-domain branch. It never force-pushes, never writes to the
default branch, never touches another repository, and never merges.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

import common as c

ALLOWED_PREFIXES = ("docs/",)
ALLOWED_FILES = ("mkdocs.yml",)


def default_branch() -> str:
    res = c.run(["git", "symbolic-ref", "refs/remotes/origin/HEAD", "--short"])
    if res["rc"] == 0 and res["stdout"].strip():
        return res["stdout"].strip().split("/", 1)[-1]
    for cand in ("main", "master"):
        if c.run(["git", "rev-parse", "--verify", f"origin/{cand}"])["rc"] == 0:
            return cand
    return "main"


def current_branch() -> str:
    return c.run(["git", "rev-parse", "--abbrev-ref", "HEAD"])["stdout"].strip()


def changed_site_paths() -> list[str]:
    """Changed paths the maintainer is allowed to publish."""
    res = c.run(["git", "status", "--porcelain"])
    paths = []
    for line in res["stdout"].splitlines():
        if not line.strip():
            continue
        rest = line[3:].strip()
        if " -> " in rest:  # rename
            rest = rest.split(" -> ", 1)[1]
        path = rest.strip().strip('"')
        if path.startswith(ALLOWED_PREFIXES) or path in ALLOWED_FILES:
            paths.append(path)
    return sorted(set(paths))


def branch_name(domain: str) -> str:
    return f"{domain}-maintainer/{dt.datetime.now(dt.timezone.utc).date().isoformat()}"


def build_ok() -> tuple[bool, str]:
    res = c.run(["uv", "run", "mkdocs", "build", "--strict"], timeout=300)
    if res["rc"] != 0:
        return False, (res["stderr"] or res["stdout"])[-2000:]
    return True, ""


def open_pr(domain: str, branch: str, base: str, title: str, body_file: Path | None):
    existing = c.run(
        ["gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number,url"],
        timeout=45,
    )
    import json as _json

    try:
        prs = _json.loads(existing["stdout"]) if existing["rc"] == 0 else []
    except _json.JSONDecodeError:
        prs = []
    if prs:
        return "updated", prs[0].get("url", "")
    args = ["gh", "pr", "create", "--base", base, "--head", branch, "--title", title]
    if body_file and body_file.exists():
        args += ["--body-file", str(body_file)]
    else:
        args += ["--body", f"Automated `{domain}` maintenance pass. Review before merge."]
    res = c.run(args, timeout=90)
    if res["rc"] != 0:
        raise SystemExit(f"gh pr create failed: {res['stderr'].strip()}")
    return "created", res["stdout"].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True, choices=["content", "platform", "services"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--title", default=None)
    parser.add_argument("--summary-file", default=None)
    args = parser.parse_args()

    base = default_branch()
    branch = branch_name(args.domain)
    paths = changed_site_paths()
    title = args.title or f"chore({args.domain}): site maintenance pass"
    body_file = Path(args.summary_file) if args.summary_file else None

    if not paths:
        print(f"[{args.domain}] no changes; nothing to publish (base={base})")
        return 0

    if args.dry_run:
        print(f"[{args.domain}] dry-run: would open/update PR on {branch} -> {base}")
        for p in paths:
            print(f"  would stage: {p}")
        return 0

    cur = current_branch()
    if cur == base:
        # Branch off without disturbing the default branch working tree.
        res = c.run(["git", "checkout", "-B", branch])
        if res["rc"] != 0:
            raise SystemExit(f"could not create branch {branch}: {res['stderr'].strip()}")
    elif cur != branch:
        if c.run(["git", "rev-parse", "--verify", branch])["rc"] == 0:
            c.run(["git", "checkout", branch])
        else:
            res = c.run(["git", "checkout", "-b", branch])
            if res["rc"] != 0:
                raise SystemExit(f"could not create branch {branch}: {res['stderr'].strip()}")

    if current_branch() == base:
        raise SystemExit("refusing to publish on the default branch")

    # Stage only the files the maintainer may publish.
    res = c.run(["git", "add", "--", *paths])
    if res["rc"] != 0:
        raise SystemExit(f"git add failed: {res['stderr'].strip()}")

    ok, err = build_ok()
    if not ok:
        c.run(["git", "restore", "--staged", "--", *paths])
        raise SystemExit(f"mkdocs build --strict failed; PR blocked:\n{err}")

    subject = title
    res = c.run(["git", "commit", "-m", subject])
    if res["rc"] != 0:
        raise SystemExit(f"git commit failed: {res['stderr'].strip()}")

    res = c.run(["git", "push", "-u", "origin", branch])
    if res["rc"] != 0:
        raise SystemExit(f"git push failed: {res['stderr'].strip()}")

    action, url = open_pr(args.domain, branch, base, title, body_file)
    print(f"[{args.domain}] PR {action}: {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
