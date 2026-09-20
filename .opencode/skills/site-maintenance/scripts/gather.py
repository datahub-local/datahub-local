#!/usr/bin/env python3
"""Deterministic fact gatherer for the site maintainer.

Usage:
    gather.py --domain content|platform|services|all

Reads GitHub, the config-of-record, and the live cluster and prints one compact
JSON object. It never writes to any source. The model reasons over this output;
it must not recall values the gatherer can fetch.
"""

from __future__ import annotations

import argparse

import common as c


def _gh_repo_list(org: str):
    data, err = c.run_json(
        [
            "gh",
            "repo",
            "list",
            org,
            "--limit",
            "200",
            "--json",
            (
                "name,nameWithOwner,description,isArchived,isFork,isPrivate,pushedAt,url,"
                "primaryLanguage,repositoryTopics,stargazerCount"
            ),
        ],
        timeout=90,
    )
    return data, err


def gather_content(cfg: dict) -> dict:
    repos_cfg = cfg.get("repositories", {}) or {}
    include = set(repos_cfg.get("include", []) or [])
    exclude = set(repos_cfg.get("exclude", []) or [])
    orgs = cfg.get("orgs", []) or []

    repos, errors = [], {}
    for org in orgs:
        data, err = _gh_repo_list(org)
        if err:
            errors[org] = err
            continue
        repos.extend(data or [])

    scope = []
    for r in sorted(repos, key=lambda x: x["nameWithOwner"]):
        name = r["nameWithOwner"]
        reason = None
        if name in include:
            in_scope = True
        elif name in exclude:
            in_scope, reason = False, "excluded"
        elif r.get("isFork"):
            in_scope, reason = False, "fork"
        elif c.org_of(name) not in orgs:
            in_scope, reason = False, "org not listed"
        else:
            in_scope = True
        scope.append(
            {
                "name": name,
                "in_scope": in_scope,
                "reason": reason,
                "archived": bool(r.get("isArchived")),
                "fork": bool(r.get("isFork")),
                "private": bool(r.get("isPrivate")),
                "pushed_at": r.get("pushedAt"),
                "url": r.get("url"),
                "description": r.get("description"),
            }
        )

    release_tracked = set(cfg.get("release_tracked", []) or [])
    releases = {}
    for full in sorted(name for name in include | {f"{o}/{r}" for o in orgs for r in release_tracked}):
        repo = c.repo_of(full)
        if repo not in release_tracked and full not in include:
            continue
        data, err = c.run_json(
            ["gh", "release", "list", "-R", full, "--limit", "5", "--json", "tagName,publishedAt"],
            timeout=45,
        )
        releases[full] = {"releases": data or [], "error": err}

    # Local link and asset health across the documentation tree.
    root = c.repo_root()
    link_cfg = cfg.get("links", {}) or {}
    ignores = tuple(link_cfg.get("ignore_prefixes", []) or ())
    check_remote = bool(link_cfg.get("check_remote"))
    broken, checked = [], 0
    for md in sorted((root / "docs").rglob("*.md")):
        for kind, target in c.markdown_links(md):
            if not target or target.startswith("#") or target.startswith(ignores):
                continue
            checked += 1
            entry = {"page": str(md.relative_to(root)), "kind": kind, "target": target}
            if c.is_external(target):
                if check_remote:
                    res = c.run(["curl", "-fsS", "-o", "/dev/null", "-m", "15", target], timeout=20)
                    if res["rc"] != 0:
                        broken.append({**entry, "reason": "remote unreachable"})
                continue
            base = target.split("#", 1)[0]
            if not base:
                continue
            resolved = (md.parent / base).resolve()
            if not resolved.exists():
                broken.append({**entry, "reason": "missing local target"})

    catalogue_path = root / "docs" / "projects" / "index.md"
    catalogue = {
        "path": str(catalogue_path.relative_to(root)),
        "exists": catalogue_path.exists(),
    }
    if catalogue_path.exists():
        import re as _re

        text = catalogue_path.read_text(encoding="utf-8", errors="replace")
        catalogue["github_refs"] = sorted(
            set(_re.findall(r"https?://github\.com/[^\s)\"'>]+", text))
        )

    return {
        "sources": {"github": {"available": not errors, "errors": errors}},
        "scope": scope,
        "releases": releases,
        "catalogue": catalogue,
        "links": {"checked": checked, "broken": broken, "remote_checked": check_remote},
    }


def gather_platform(cfg: dict) -> dict:
    paths = cfg.get("paths", {}) or {}
    inv_path = c.resolve_config_path(paths.get("bootstrap_inventory", {}))
    inventory, inv_error = None, None
    if inv_path and inv_path.exists():
        try:
            inventory = c.load_yaml_file(inv_path)
        except Exception as exc:  # noqa: BLE001 - reported, never fatal here
            inv_error = str(exc)
    else:
        inv_error = f"not found: {inv_path}"

    hosts = []
    if isinstance(inventory, dict):
        groups = (inventory.get("k3s_cluster", {}) or {}).get("children", {}) or {}
        for role, body in groups.items():
            for host, attrs in ((body or {}).get("hosts", {}) or {}).items():
                hosts.append(
                    {
                        "host": host,
                        "role": role,
                        "ansible_host": attrs.get("ansible_host"),
                        "ansible_user": attrs.get("ansible_user"),
                        "agent_role": attrs.get("k3s_agent_role_name"),
                        "gpu": bool(attrs.get("k3s_gpu_nvidia_enabled")),
                        "extra_volumes": list((attrs.get("extra_volumes") or {}).keys()),
                    }
                )

    nodes, nodes_error = None, None
    data, err = c.run_json(["kubectl", "get", "nodes", "-o", "json"], timeout=30)
    if err:
        nodes_error = err
    else:
        nodes = []
        for it in (data or {}).get("items", []):
            meta = it.get("metadata", {})
            status = it.get("status", {})
            info = status.get("nodeInfo", {})
            labels = meta.get("labels", {}) or {}
            roles = [k.split("/", 1)[1] for k in labels if k.startswith("node-role.kubernetes.io/")]
            nodes.append(
                {
                    "name": meta.get("name"),
                    "arch": info.get("architecture"),
                    "os": info.get("osImage"),
                    "kernel": info.get("kernelVersion"),
                    "roles": sorted(roles) or ["worker"],
                    "capacity_cpu": (status.get("capacity", {}) or {}).get("cpu"),
                    "capacity_memory": (status.get("capacity", {}) or {}).get("memory"),
                    "gpu_present": labels.get("nvidia.com/gpu.present"),
                }
            )
        nodes.sort(key=lambda n: n["name"] or "")

    namespaces, ns_error = None, None
    data, err = c.run_json(["kubectl", "get", "namespaces", "-o", "json"], timeout=30)
    if err:
        ns_error = err
    else:
        namespaces = sorted(
            it["metadata"]["name"] for it in (data or {}).get("items", []) if it.get("metadata")
        )

    return {
        "sources": {
            "inventory": {"path": str(inv_path), "available": inventory is not None, "error": inv_error},
            "cluster": {"available": nodes is not None, "error": nodes_error or ns_error},
        },
        "inventory_hosts": hosts,
        "cluster_nodes": nodes,
        "cluster_error": nodes_error,
        "namespaces": namespaces,
        "namespaces_error": ns_error,
    }


def gather_services(cfg: dict) -> dict:
    paths = cfg.get("paths", {}) or {}
    ver_path = c.resolve_config_path(paths.get("core_versions", {}))
    versions, ver_error = None, None
    if ver_path and ver_path.exists():
        try:
            versions = c.load_yaml_file(ver_path)
        except Exception as exc:  # noqa: BLE001
            ver_error = str(exc)
    else:
        ver_error = f"not found: {ver_path}"

    helm, helm_error = c.run_json(["helm", "list", "-A", "-o", "json"], timeout=45)

    images, img_error = None, None
    data, err = c.run_json(["kubectl", "get", "pods", "-A", "-o", "json"], timeout=45)
    if err:
        img_error = err
    else:
        seen: dict[str, set] = {}
        for pod in (data or {}).get("items", []):
            ns = pod.get("metadata", {}).get("namespace")
            for spec in (pod.get("spec", {}) or {}).get("containers", []) or []:
                image = spec.get("image")
                if image:
                    seen.setdefault(f"{ns}/{image}", set())
        images = sorted(seen)

    return {
        "sources": {
            "versions_file": {"path": str(ver_path), "available": versions is not None, "error": ver_error},
            "cluster": {"available": helm is not None, "error": helm_error or img_error},
        },
        "container_image_version": (versions or {}).get("container_image_version"),
        "helm_chart_version": (versions or {}).get("helm_chart_version"),
        "helm_releases": helm,
        "deployed_images": images,
    }


DOMAINS = {
    "content": gather_content,
    "platform": gather_platform,
    "services": gather_services,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", choices=[*DOMAINS, "all"], required=True)
    args = parser.parse_args()

    cfg = c.load_config()
    if args.domain == "all":
        out = {name: fn(cfg) for name, fn in DOMAINS.items()}
    else:
        out = {args.domain: DOMAINS[args.domain](cfg)}
    c.emit({"domain": args.domain, "facts": out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
