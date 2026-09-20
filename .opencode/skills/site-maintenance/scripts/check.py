#!/usr/bin/env python3
"""Deterministic checks for the site maintainer.

Usage:
    check.py --domain content|platform|services|all

Gathers facts (read-only) and prints JSON findings: what the site claims versus
what the sources say. A finding is evidence for the model to act on; this script
never edits a file.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import common as c
import gather


def _table_rows(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            cells = [x.strip() for x in line.strip("|").split("|")]
            rows.append(cells)
    return rows


def _norm_text(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]\([^)]*\)", "", s)).strip()


def _doc_os(short: str, full: str):
    """Map a cluster osImage to the doc's short form, e.g. Debian 13."""
    m = re.search(r"Debian GNU/Linux (\d+)", full or "")
    return f"Debian {m.group(1)}" if m else (full or "").strip() or None


def check_content(cfg: dict) -> dict:
    facts = gather.gather_content(cfg)
    root = c.repo_root()
    findings = []

    for b in facts["links"]["broken"]:
        findings.append(
            {
                "kind": "broken-link",
                "severity": "high",
                "page": b["page"],
                "target": b["target"],
                "message": f"{b['kind']} '{b['target']}' is broken ({b['reason']})",
                "source": "site tree",
            }
        )

    cat = facts["catalogue"]
    in_scope = {r["name"]: r for r in facts["scope"] if r["in_scope"]}
    if not cat["exists"]:
        findings.append(
            {
                "kind": "catalogue-missing",
                "severity": "info",
                "page": cat["path"],
                "message": "the projects catalogue does not exist yet; drift cannot be compared",
                "source": "site tree",
            }
        )
    else:
        refs = set()
        for url in cat.get("github_refs", []):
            m = re.search(r"github\.com/([^/]+/[^/#?]+?)(?:\.git)?/?$", url)
            if m:
                refs.add(m.group(1))
        for name, r in sorted(in_scope.items()):
            if name not in refs:
                findings.append(
                    {
                        "kind": "repo-not-catalogued",
                        "severity": "medium",
                        "page": cat["path"],
                        "target": name,
                        "message": f"in-scope repository {name} has no catalogue card",
                        "evidence": {"url": r["url"], "pushed_at": r["pushed_at"]},
                        "source": "GitHub",
                    }
                )
        for name in sorted(refs):
            if name in in_scope and in_scope[name]["archived"]:
                findings.append(
                    {
                        "kind": "repo-archived",
                        "severity": "medium",
                        "page": cat["path"],
                        "target": name,
                        "message": f"{name} is archived; its card should be marked archived",
                        "source": "GitHub",
                    }
                )

    # Duplicated paragraphs across pages: one narrative, one place.
    seen: dict[str, list[str]] = {}
    for md in sorted((root / "docs").rglob("*.md")):
        rel = str(md.relative_to(root))
        if rel.startswith("openspec/") or rel.endswith("index.md") and "projects" in rel:
            pass
        text = md.read_text(encoding="utf-8", errors="replace")
        for block in re.split(r"\n\s*\n", text):
            norm = _norm_text(block)
            if len(norm) >= 240 and not norm.startswith("#"):
                seen.setdefault(norm, []).append(rel)
    for norm, pages in seen.items():
        uniq = sorted(set(pages))
        if len(uniq) > 1:
            findings.append(
                {
                    "kind": "duplicated-narrative",
                    "severity": "low",
                    "page": ", ".join(uniq),
                    "message": "the same passage appears on multiple pages; keep one source and link",
                    "evidence": {"excerpt": norm[:120]},
                    "source": "site tree",
                }
            )

    # Navigation integrity: every nav target must exist.
    mkdocs = root / "mkdocs.yml"
    if mkdocs.exists():
        try:
            nav_data = c.load_yaml_file(mkdocs) or {}
        except Exception:  # noqa: BLE001
            nav_data = {}

        def _walk(nav):
            for item in nav or []:
                if isinstance(item, dict):
                    for value in item.values():
                        yield from _walk(value)
                elif isinstance(item, str) and item.endswith(".md"):
                    yield item

        for rel in _walk(nav_data.get("nav")):
            if not (root / "docs" / rel).exists():
                findings.append(
                    {
                        "kind": "nav-target-missing",
                        "severity": "high",
                        "page": "mkdocs.yml",
                        "target": rel,
                        "message": f"navigation references docs/{rel}, which does not exist",
                        "source": "site tree",
                    }
                )

    # Conservative image refresh: a project image predates its repo's last push.
    manifest = root / "docs" / "assets" / "img" / "showcase" / "manifest.yaml"
    if manifest.exists():
        try:
            data = c.load_yaml_file(manifest) or {}
        except Exception:  # noqa: BLE001
            data = {}
        for slug, entry in (data or {}).items():
            generated = (entry or {}).get("generated_at")
            repo = (entry or {}).get("repo")
            if not (generated and repo and repo in in_scope):
                continue
            if in_scope[repo]["pushed_at"] and str(in_scope[repo]["pushed_at"]) > str(generated):
                findings.append(
                    {
                        "kind": "image-maybe-stale",
                        "severity": "low",
                        "page": f"docs/projects/{slug}",
                        "message": f"{slug} image predates the last push to {repo}; review for regeneration",
                        "evidence": {"image_generated_at": generated, "repo_pushed_at": in_scope[repo]["pushed_at"]},
                        "source": "GitHub",
                    }
                )

    return {"facts_summary": {"in_scope": len(in_scope), "broken": len(facts["links"]["broken"])},
            "findings": findings}


def check_platform(cfg: dict) -> dict:
    facts = gather.gather_platform(cfg)
    root = c.repo_root()
    pages = cfg.get("pages", {}) or {}
    arch = root / pages.get("architecture", "docs/architecture/overview.md")
    findings = []

    if facts["cluster_error"]:
        findings.append(
            {
                "kind": "cluster-unreachable",
                "severity": "high",
                "page": str(arch.relative_to(root)),
                "message": f"cluster is unreachable: {facts['cluster_error']}",
                "source": "cluster",
            }
        )
        return {"facts_summary": {"cluster": "unreachable"}, "findings": findings}

    nodes = {n["name"]: n for n in facts["cluster_nodes"] or []}
    doc_rows = _table_rows(arch)
    doc_nodes = {}
    for cells in doc_rows:
        if cells and "`datahublocal-" in cells[0]:
            name = cells[0].strip("`")
            doc_nodes[name] = cells

    for name in sorted(set(nodes) - set(doc_nodes)):
        findings.append(
            {
                "kind": "node-missing-from-docs",
                "severity": "high",
                "page": str(arch.relative_to(root)),
                "target": name,
                "message": f"cluster node {name} is not in the node table",
                "source": "cluster",
            }
        )
    for name in sorted(set(doc_nodes) - set(nodes)):
        findings.append(
            {
                "kind": "node-removed-from-cluster",
                "severity": "high",
                "page": str(arch.relative_to(root)),
                "target": name,
                "message": f"node table lists {name}, which is not in the cluster",
                "source": "cluster",
            }
        )

    # Per-node attribute drift where both sides are parseable.
    for name in sorted(set(nodes) & set(doc_nodes)):
        n, cells = nodes[name], doc_nodes[name]
        if len(cells) >= 8:
            # The docs column is "Cores / Threads"; the cluster reports logical
            # CPUs (threads), so compare against the larger of the two numbers.
            nums = [int(x) for x in re.findall(r"\d+", cells[4] or "")]
            if nums and n.get("capacity_cpu") and max(nums) != int(n["capacity_cpu"]):
                findings.append(
                    {
                        "kind": "node-cpu-drift",
                        "severity": "medium",
                        "page": str(arch.relative_to(root)),
                        "target": name,
                        "message": f"CPU (cores/threads): docs {cells[4]}, cluster logical CPUs {n['capacity_cpu']}",
                        "evidence": {"docs": cells[4], "cluster": n["capacity_cpu"]},
                        "source": "cluster",
                    }
                )
            # Physical RAM is not derivable from the cluster: node capacity is
            # usable memory after reservation, so it is deliberately not compared.
            os_doc = _doc_os(cells[7], n.get("os") or "")
            if os_doc and os_doc != (cells[7] or "").strip():
                findings.append(
                    {
                        "kind": "node-os-drift",
                        "severity": "low",
                        "page": str(arch.relative_to(root)),
                        "target": name,
                        "message": f"OS: docs '{cells[7]}', cluster '{os_doc}'",
                        "evidence": {"docs": cells[7], "cluster": n.get("os")},
                        "source": "cluster",
                    }
                )

    # Inventory versus cluster: the two sources must agree.
    inv_hosts = {h["host"] for h in facts["inventory_hosts"]}
    if facts["sources"]["inventory"]["available"]:
        for name in sorted(inv_hosts - set(nodes)):
            findings.append(
                {
                    "kind": "record-cluster-mismatch",
                    "severity": "high",
                    "page": facts["sources"]["inventory"]["path"],
                    "target": name,
                    "message": f"inventory lists {name}; the cluster does not have it (record vs cluster)",
                    "evidence": {"record": "inventory.yml", "cluster": sorted(nodes)},
                    "source": "inventory + cluster",
                }
            )
        for name in sorted(set(nodes) - inv_hosts):
            findings.append(
                {
                    "kind": "record-cluster-mismatch",
                    "severity": "high",
                    "page": facts["sources"]["inventory"]["path"],
                    "target": name,
                    "message": f"cluster has {name}; the inventory does not (record vs cluster)",
                    "evidence": {"record": "inventory.yml", "cluster": name},
                    "source": "inventory + cluster",
                }
            )
    else:
        findings.append(
            {
                "kind": "record-unavailable",
                "severity": "info",
                "page": facts["sources"]["inventory"]["path"],
                "message": f"inventory not readable, so record facts could not be cross-checked: {facts['sources']['inventory']['error']}",
                "source": "inventory",
            }
        )

    # Landing statistic versus cluster: only unambiguous counts are compared.
    index = root / "docs" / "index.md"
    if index.exists():
        text = index.read_text(encoding="utf-8", errors="replace")
        for num, label in re.findall(
            r'stat-number">([^<]+)</div>\s*<div class="stat-label">([^<]+)<', text
        ):
            if "node" in label.lower():
                digits = re.sub(r"\D", "", num)
                if digits and int(digits) != len(nodes):
                    findings.append(
                        {
                            "kind": "stat-stale",
                            "severity": "medium",
                            "page": "docs/index.md",
                            "target": label.strip(),
                            "message": f"'{label.strip()}' says {num.strip()}, cluster has {len(nodes)} nodes",
                            "evidence": {"docs": num.strip(), "cluster": len(nodes)},
                            "source": "cluster",
                        }
                    )

    # Namespace table versus cluster.
    doc_ns = set()
    for cells in doc_rows:
        if cells and cells[0].startswith("`") and cells[0].endswith("`") and "datahublocal-" not in cells[0]:
            doc_ns.add(cells[0].strip("`"))
    cluster_ns = set(facts.get("namespaces") or [])
    for ns in sorted(cluster_ns - doc_ns):
        if ns in {"default", "kube-node-lease", "kube-public"}:
            continue
        findings.append(
            {
                "kind": "namespace-missing-from-docs",
                "severity": "low",
                "page": str(arch.relative_to(root)),
                "target": ns,
                "message": f"namespace {ns} exists in the cluster but not in the namespace table",
                "source": "cluster",
            }
        )
    for ns in sorted(doc_ns - cluster_ns):
        findings.append(
            {
                "kind": "namespace-removed-from-cluster",
                "severity": "low",
                "page": str(arch.relative_to(root)),
                "target": ns,
                "message": f"namespace table lists {ns}, which is not in the cluster",
                "source": "cluster",
            }
        )

    return {
        "facts_summary": {"nodes": len(nodes), "doc_nodes": len(doc_nodes), "namespaces": len(cluster_ns)},
        "findings": findings,
    }


def _chart_name_version(chart: str):
    m = re.match(r"^(.*)-(\d+\.\d+\.\d+.*)$", chart or "")
    return (m.group(1), m.group(2)) if m else (chart, None)


def check_services(cfg: dict) -> dict:
    facts = gather.gather_services(cfg)
    findings = []
    record_versions = facts.get("helm_chart_version") or {}
    record_images = facts.get("container_image_version") or {}

    releases = facts.get("helm_releases") or []
    for rel in releases:
        name, ver = _chart_name_version(rel.get("chart", ""))
        rec = None
        for key, val in record_versions.items():
            ref = (val or {}).get("ref", "")
            if key == name or ref.split("/")[-1] == name:
                rec = (key, (val or {}).get("version"))
                break
        if rec and ver and rec[1] != ver:
            findings.append(
                {
                    "kind": "chart-version-mismatch",
                    "severity": "medium",
                    "page": "docs/services/",
                    "target": rel.get("chart"),
                    "message": f"{rec[0]}: record {rec[1]}, cluster {ver}",
                    "evidence": {"record": rec[1], "cluster": ver, "release": rel.get("name")},
                    "source": "_version.yaml + helm",
                }
            )

    def _split_tag(s: str):
        if "@sha256:" in s:
            tag, digest = s.split("@sha256:", 1)
            return tag, "sha256:" + digest
        return s, None

    deployed = facts.get("deployed_images") or []
    seen_pairs = set()
    for entry in deployed:
        image = entry.split("/", 1)[1] if "/" in entry else entry
        if ":" not in image:
            continue
        repo, tag_full = image.split(":", 1)
        tag, digest = _split_tag(tag_full)
        key = next((k for k in record_images if k == repo), None)
        if not key:
            continue
        rec_tag, rec_digest = _split_tag(str(record_images[key]))
        mismatch = None
        if rec_digest and digest and rec_digest != digest:
            mismatch = (rec_digest, digest)
        elif not rec_digest and not digest and tag != "latest" and rec_tag != tag:
            mismatch = (rec_tag, tag)
        if mismatch and (repo, mismatch) not in seen_pairs:
            seen_pairs.add((repo, mismatch))
            findings.append(
                {
                    "kind": "image-version-mismatch",
                    "severity": "medium",
                    "page": "docs/services/",
                    "target": repo,
                    "message": f"{repo}: record {mismatch[0]}, cluster {mismatch[1]}",
                    "evidence": {"record": record_images[key], "cluster": tag_full},
                    "source": "_version.yaml + cluster",
                }
            )

    if facts["sources"]["versions_file"]["available"] is False:
        findings.append(
            {
                "kind": "record-unavailable",
                "severity": "info",
                "page": facts["sources"]["versions_file"]["path"],
                "message": f"versions file not readable: {facts['sources']['versions_file']['error']}",
                "source": "_version.yaml",
            }
        )

    return {
        "facts_summary": {
            "helm_releases": len(releases),
            "record_charts": len(record_versions),
            "record_images": len(record_images),
        },
        "findings": findings,
    }


CHECKS = {
    "content": check_content,
    "platform": check_platform,
    "services": check_services,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", choices=[*CHECKS, "all"], required=True)
    args = parser.parse_args()
    cfg = c.load_config()
    if args.domain == "all":
        out = {name: fn(cfg) for name, fn in CHECKS.items()}
    else:
        out = {args.domain: CHECKS[args.domain](cfg)}
    total = sum(len(v["findings"]) for v in out.values())
    c.emit({"domain": args.domain, "total_findings": total, "results": out})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
