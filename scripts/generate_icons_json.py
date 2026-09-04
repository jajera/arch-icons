#!/usr/bin/env python3
"""Generate icons.json from multi-vendor architecture icon marks."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
OUTPUT = ROOT / "icons.json"
FAMILIES_FILE = Path(__file__).resolve().parent / "product_families.json"

ACCENT = "#334155"

FAMILY_NAMES = {
    "cdn-edge": "CDN / Edge",
    "data": "Data",
    "dev-platforms": "Dev Platforms",
    "hashicorp": "HashiCorp",
    "iac": "IaC",
    "linux-containers": "Containers",
    "networking": "Networking",
    "observability": "Observability",
    "os": "Operating Systems",
    "security": "Security",
    "vcs-ci": "VCS / CI",
    "virt": "Virtualization",
}

PRODUCT_NAMES = {
    "almalinux": "AlmaLinux",
    "ansible": "Ansible",
    "artifactory": "Artifactory",
    "bitbucket": "Bitbucket",
    "boundary": "Boundary",
    "circleci": "CircleCI",
    "clickhouse": "ClickHouse",
    "consul": "Consul",
    "datadog": "Datadog",
    "debian": "Debian",
    "docker": "Docker",
    "fedora": "Fedora",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "grafana": "Grafana",
    "hashicorp": "HashiCorp",
    "helm": "Helm",
    "jenkins": "Jenkins",
    "jfrog": "JFrog",
    "kafka": "Kafka",
    "keycloak": "Keycloak",
    "kong": "Kong",
    "libvirt": "libvirt",
    "linux": "Linux",
    "lxd": "LXD",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "nginx": "NGINX",
    "nomad": "Nomad",
    "npm": "npm",
    "packer": "Packer",
    "podman": "Podman",
    "postgresql": "PostgreSQL",
    "pulp": "Pulp",
    "pulumi": "Pulumi",
    "pypi": "PyPI",
    "quay": "Quay",
    "rabbitmq": "RabbitMQ",
    "redis": "Redis",
    "rocky": "Rocky Linux",
    "rust": "Rust",
    "sentry": "Sentry",
    "snyk": "Snyk",
    "sonarqube": "SonarQube",
    "sonatype": "Sonatype",
    "terraform": "Terraform",
    "traefik": "Traefik",
    "ubuntu": "Ubuntu",
    "vault": "Vault",
}

TOKEN_NAMES = {
    "ci": "CI",
    "dd": "DD",
    "iac": "IaC",
    "lxd": "LXD",
    "nginx": "NGINX",
    "os": "OS",
    "vcs": "VCS",
}


def humanize(slug: str) -> str:
    words = []
    for word in re.split(r"[-_]+", slug):
        if not word:
            continue
        words.append(TOKEN_NAMES.get(word.lower(), word.capitalize()))
    return " ".join(words)


def load_families() -> dict[str, str]:
    if FAMILIES_FILE.exists():
        return json.loads(FAMILIES_FILE.read_text(encoding="utf-8"))
    return {}


def variant_of(slug: str) -> str | None:
    lower = slug.lower()
    for variant in ("color", "black", "white"):
        if lower.endswith(variant) or f"-{variant}" in lower or f"_{variant}" in lower:
            return variant
    if "ocean-blue" in lower:
        return "color"
    return None


SPECIAL_SLUG_NAMES = {
    "logo_without_text": "",
    "pulumi_mark_on_light": "",
    "dd_icon_rgb": "",
    "dd_icon_white": "white",
    "sonar-vortex-icon": "",
    "jfrog-logo-2022": "",
    "Apache_Kafka_logo": "",
    "Nginx_logo_hexagon": "",
    "traefik-icon-color": "color",
    "containers": "",
    "logo-square": "",
    "logo-sentry": "",
    "grafana_icon": "",
    "tux": "",
    "snyk-dog": "",
    "git-icon": "",
    "jenkins": "",
}


def display_name(product: str, slug: str) -> str:
    product_label = PRODUCT_NAMES.get(product, humanize(product))
    if slug in SPECIAL_SLUG_NAMES:
        forced = SPECIAL_SLUG_NAMES[slug]
        return f"{product_label} ({forced})" if forced else product_label
    variant = variant_of(slug)
    # Drop redundant product prefixes from slug for cleaner titles
    cleaned = slug
    for prefix in (
        f"{product}-",
        f"{product}_",
        product,
        "docker-mark-",
        "docker-",
        "logo-",
        "Logo-",
        "Kong-",
        "Bitbucket-",
        "pulumi_",
        "opensearch_",
        "Nginx_",
        "Fedora_",
        "Logo-ubuntu_",
    ):
        if cleaned.lower().startswith(prefix.lower()):
            cleaned = cleaned[len(prefix) :]
            break

    cleaned = re.sub(
        r"[-_]?(logomark|logo|icon|mark|transparent|only|default|on_light|cof-orange-hex|2021|2022|vortex)[-_]?",
        "-",
        cleaned,
        flags=re.I,
    )
    cleaned = re.sub(r"[-_]+", "-", cleaned).strip("-").lower()
    for variant_name in ("color", "black", "white"):
        if cleaned == variant_name or cleaned.endswith(f"-{variant_name}"):
            cleaned = cleaned[: -len(variant_name)].strip("-")
            break

    if not cleaned or cleaned in {"rgb", "icon", "mark"}:
        base = product_label
    else:
        base = f"{product_label} {humanize(cleaned)}"

    if variant:
        return f"{base} ({variant})"
    return base


def tags_for(family: str, product: str, slug: str) -> list[str]:
    tags = {product, family}
    variant = variant_of(slug)
    if variant:
        tags.add(variant)
    return sorted(tags)


def build_entries() -> list[dict[str, object]]:
    families = load_families()
    entries: list[dict[str, object]] = []
    for svg_path in sorted(ICONS_DIR.glob("*/*.svg")):
        relative = svg_path.relative_to(ROOT)
        product = relative.parts[1]
        slug = svg_path.stem
        family = families.get(product, "other")
        family_label = FAMILY_NAMES.get(family, humanize(family))
        product_label = PRODUCT_NAMES.get(product, humanize(product))
        fullname = display_name(product, slug)
        entries.append(
            {
                "path": relative.as_posix(),
                "tags": tags_for(family, product, slug),
                "category": product,
                "family": family,
                "color": ACCENT,
                "description": f"{fullname} architecture icon ({product_label}, {family_label}).",
                "fullname": fullname,
                "name": slug,
            }
        )

    entries.sort(
        key=lambda icon: (
            str(icon.get("family", "")).casefold(),
            str(icon["category"]).casefold(),
            str(icon["fullname"]).casefold(),
            str(icon["path"]),
        )
    )
    return entries


def main() -> None:
    entries = build_entries()
    if not entries:
        raise SystemExit(f"No SVG icons found under {ICONS_DIR}")

    OUTPUT.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(entries)} icons to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
