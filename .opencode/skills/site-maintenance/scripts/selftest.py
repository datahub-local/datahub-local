#!/usr/bin/env python3
"""Self-tests for the site maintainer.

Exercises the safety guards in publish.py and the synthetic-drift behaviour of
check.py without touching any real source. Run:

    uv run python .opencode/skills/site-maintenance/scripts/selftest.py
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import check
import common as c
import gather
import publish

PASS, FAIL = [], []


def expect(name: str, cond: bool, detail: str = ""):
    (PASS if cond else FAIL).append(name)
    mark = "ok  " if cond else "FAIL"
    print(f"  {mark} {name}{(' :: ' + detail) if (detail and not cond) else ''}")


def _git(args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)


def test_publish_guards():
    print("publish guards")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "docs").mkdir()
        (tmp / "openspec").mkdir()
        (tmp / "docs" / "a.md").write_text("hello")
        (tmp / "openspec" / "x.md").write_text("plan")
        _git(["init", "-b", "main"], tmp)
        _git(["config", "user.email", "t@t"], tmp)
        _git(["config", "user.name", "t"], tmp)
        _git(["add", "-A"], tmp)
        _git(["commit", "-m", "init"], tmp)
        (tmp / "docs" / "a.md").write_text("changed")
        (tmp / "openspec" / "x.md").write_text("changed too")

        here = os.getcwd()
        os.chdir(tmp)
        try:
            paths = publish.changed_site_paths()
            expect("only site paths are publishable", paths == ["docs/a.md"], str(paths))
            expect("default branch detected as main", publish.default_branch() == "main", publish.default_branch())
            for domain in ("content", "platform", "services"):
                b = publish.branch_name(domain)
                expect(f"branch for {domain} is not a default branch", b not in ("main", "master"), b)
        finally:
            os.chdir(here)

    src = Path(publish.__file__).read_text()
    expect("publish never force-pushes", "--force" not in src)
    expect("publish never merges", "pr merge" not in src)
    expect("publish never pushes the base branch directly",
           "push\", \"-u\", \"origin\", base" not in src)


def test_idempotency():
    print("PR idempotency")
    real_run = publish.c.run

    def fake_existing(cmd, **kw):
        if cmd[:3] == ["gh", "pr", "list"]:
            return {"found": True, "rc": 0, "stdout": '[{"number":5,"url":"http://x/5"}]', "stderr": ""}
        return {"found": True, "rc": 0, "stdout": "", "stderr": ""}

    calls = []

    def record(cmd, **kw):
        calls.append(cmd)
        return fake_existing(cmd, **kw)

    publish.c.run = record  # type: ignore[assignment]
    try:
        action, url = publish.open_pr("content", "content-maintainer/2026-01-01", "main", "t", None)
        expect("existing PR is updated, not recreated", action == "updated" and url == "http://x/5")
        expect("no create call when a PR exists", not any(c[:3] == ["gh", "pr", "create"] for c in calls))
    finally:
        publish.c.run = real_run  # type: ignore[assignment]

    def fake_none(cmd, **kw):
        if cmd[:3] == ["gh", "pr", "list"]:
            return {"found": True, "rc": 0, "stdout": "[]", "stderr": ""}
        if cmd[:3] == ["gh", "pr", "create"]:
            return {"found": True, "rc": 0, "stdout": "http://x/new", "stderr": ""}
        return {"found": True, "rc": 0, "stdout": "", "stderr": ""}

    publish.c.run = fake_none  # type: ignore[assignment]
    try:
        action, url = publish.open_pr("content", "b", "main", "t", None)
        expect("new PR created when none exists", action == "created" and url == "http://x/new")
    finally:
        publish.c.run = real_run  # type: ignore[assignment]


def test_record_unavailable():
    print("record unavailable is reported")
    real_gather = gather.gather_platform
    gather.gather_platform = lambda cfg: {  # type: ignore[assignment]
        "sources": {"inventory": {"path": "missing.yml", "available": False, "error": "not found"},
                    "cluster": {"available": True, "error": None}},
        "inventory_hosts": [], "cluster_nodes": [], "cluster_error": None,
        "namespaces": [], "namespaces_error": None,
    }
    try:
        out = check.check_platform({"pages": {"architecture": "docs/architecture/overview.md"}})
        kinds = {f["kind"] for f in out["findings"]}
        expect("unreadable record is reported", "record-unavailable" in kinds)
    finally:
        gather.gather_platform = real_gather  # type: ignore[assignment]


def test_build_guard():
    print("build guard")
    real_run = publish.c.run
    publish.c.run = lambda cmd, **kw: (  # type: ignore[assignment]
        {"found": True, "rc": 1, "stdout": "", "stderr": "boom"} if "mkdocs" in cmd else real_run(cmd, **kw)
    )
    try:
        ok, err = publish.build_ok()
        expect("failing build is reported", ok is False and "boom" in err, err)
    finally:
        publish.c.run = real_run  # type: ignore[assignment]
    publish.c.run = lambda cmd, **kw: (  # type: ignore[assignment]
        {"found": True, "rc": 0, "stdout": "ok", "stderr": ""} if "mkdocs" in cmd else real_run(cmd, **kw)
    )
    try:
        ok, _ = publish.build_ok()
        expect("passing build is accepted", ok is True)
    finally:
        publish.c.run = real_run  # type: ignore[assignment]


def test_content_synthetic():
    print("content checks (synthetic)")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs").mkdir()
        (root / "docs" / "p.md").write_text("# Page\n")
        real_root = c.repo_root
        real_gather = gather.gather_content
        c.repo_root = lambda: root  # type: ignore[assignment]
        gather.gather_content = lambda cfg: {  # type: ignore[assignment]
            "sources": {"github": {"available": True, "errors": {}}},
            "scope": [
                {"name": "datahub-local/new-repo", "in_scope": True, "archived": False,
                 "fork": False, "private": False, "pushed_at": "2026-09-01", "url": "u", "description": "d"},
                {"name": "datahub-local/gone", "in_scope": True, "archived": True,
                 "fork": False, "private": False, "pushed_at": "2026-08-01", "url": "u2", "description": "d"},
            ],
            "releases": {},
            "catalogue": {"path": "docs/projects/index.md", "exists": True,
                          "github_refs": ["https://github.com/datahub-local/gone"]},
            "links": {"checked": 1, "broken": [{"page": "docs/p.md", "kind": "link",
                                                "target": "missing.md", "reason": "missing local target"}],
                      "remote_checked": False},
        }
        try:
            out = check.check_content({})
            kinds = {f["kind"] for f in out["findings"]}
            expect("broken link reported", "broken-link" in kinds)
            expect("new repo not catalogued reported", "repo-not-catalogued" in kinds)
            expect("archived repo reported", "repo-archived" in kinds)
        finally:
            c.repo_root = real_root  # type: ignore[assignment]
            gather.gather_content = real_gather  # type: ignore[assignment]


def test_platform_synthetic():
    print("platform checks (synthetic)")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs" / "architecture").mkdir(parents=True)
        (root / "docs" / "architecture" / "overview.md").write_text(
            "## Cluster Nodes\n\n"
            "| Node | Hardware | Role | CPU | Cores / Threads | GPU | RAM | OS |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            "| `datahublocal-old` | X | Worker | ARM64 | 4 / 4 | - | 8GB | Debian 13 |\n"
        )
        real_root = c.repo_root
        real_gather = gather.gather_platform
        c.repo_root = lambda: root  # type: ignore[assignment]
        gather.gather_platform = lambda cfg: {  # type: ignore[assignment]
            "sources": {"inventory": {"path": "inv.yml", "available": True, "error": None},
                        "cluster": {"available": True, "error": None}},
            "inventory_hosts": [{"host": "datahublocal-inv-only"}],
            "cluster_nodes": [{"name": "datahublocal-new", "arch": "amd64",
                               "os": "Debian GNU/Linux 13 (trixie)", "kernel": "6", "roles": ["worker"],
                               "capacity_cpu": "8", "capacity_memory": "16Gi", "gpu_present": None}],
            "cluster_error": None,
            "namespaces": ["data"],
            "namespaces_error": None,
        }
        try:
            out = check.check_platform({"pages": {"architecture": "docs/architecture/overview.md"}})
            kinds = {f["kind"] for f in out["findings"]}
            expect("node missing from docs reported", "node-missing-from-docs" in kinds)
            expect("node removed from cluster reported", "node-removed-from-cluster" in kinds)
            expect("inventory mismatch reported", "record-cluster-mismatch" in kinds)
        finally:
            c.repo_root = real_root  # type: ignore[assignment]
            gather.gather_platform = real_gather  # type: ignore[assignment]


def test_platform_unreachable():
    print("platform unreachable fails loudly")
    real_gather = gather.gather_platform
    gather.gather_platform = lambda cfg: {  # type: ignore[assignment]
        "sources": {"inventory": {"path": "inv.yml", "available": True, "error": None},
                    "cluster": {"available": False, "error": "connection refused"}},
        "inventory_hosts": [], "cluster_nodes": None, "cluster_error": "connection refused",
        "namespaces": None, "namespaces_error": "connection refused",
    }
    try:
        out = check.check_platform({"pages": {"architecture": "docs/architecture/overview.md"}})
        kinds = {f["kind"] for f in out["findings"]}
        expect("unreachable cluster reported as high severity", "cluster-unreachable" in kinds)
    finally:
        gather.gather_platform = real_gather  # type: ignore[assignment]


def test_services_synthetic():
    print("services checks (synthetic)")
    real_gather = gather.gather_services
    gather.gather_services = lambda cfg: {  # type: ignore[assignment]
        "sources": {"versions_file": {"path": "v.yaml", "available": True, "error": None},
                    "cluster": {"available": True, "error": None}},
        "container_image_version": {"alpine/k8s": "1.37.0"},
        "helm_chart_version": {"garage": {"ref": "garage-helm/garage", "version": "0.8.0"}},
        "helm_releases": [{"name": "garage", "chart": "garage-0.7.0"}],
        "deployed_images": ["data/alpine/k8s:1.36.0"],
    }
    try:
        out = check.check_services({})
        kinds = {f["kind"] for f in out["findings"]}
        expect("chart version mismatch reported", "chart-version-mismatch" in kinds)
        expect("image version mismatch reported", "image-version-mismatch" in kinds)
    finally:
        gather.gather_services = real_gather  # type: ignore[assignment]


def main() -> int:
    print("site-maintenance self-tests")
    test_publish_guards()
    test_idempotency()
    test_record_unavailable()
    test_build_guard()
    test_content_synthetic()
    test_platform_synthetic()
    test_platform_unreachable()
    test_services_synthetic()
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("failed:", ", ".join(FAIL))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
