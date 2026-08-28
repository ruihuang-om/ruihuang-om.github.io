#!/usr/bin/env python3
"""Validate source and generated output for the redesigned academic site."""

from pathlib import Path
import re
import sys
import yaml


ROOT = Path(__file__).resolve().parents[1]


def front_matter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    return text.split("---\n", 2)[1]


def front_matter_data(path: Path) -> dict:
    raw = front_matter(path)
    return yaml.safe_load(raw) if raw else {}


errors: list[str] = []
about = front_matter(ROOT / "_pages/about.md")
research = front_matter(ROOT / "_pages/publications.html")
navigation = (ROOT / "_data/navigation.yml").read_text(encoding="utf-8")

for required_path in (
    ROOT / "_layouts/site.html",
    ROOT / "_layouts/publication.html",
    ROOT / "_includes/site-header.html",
    ROOT / "assets/css/academic-home.css",
):
    if not required_path.exists():
        errors.append(f"Missing presentation file: {required_path.relative_to(ROOT)}")

config_source = (ROOT / "_config.yml").read_text(encoding="utf-8")
if not re.search(r"type:\s*publications\s+values:\s+layout:\s*publication", config_source, re.S):
    errors.append("Publication collection must use the publication layout")

if "permalink: /\n" not in about:
    errors.append("Home page must use permalink /")
if "permalink: /research/" not in research:
    errors.append("Research page must use permalink /research/")
if "url: /files/Rui_CV_2026_0827_V2.pdf" not in navigation:
    errors.append("Navigation must link the current CV PDF")

about_source = (ROOT / "_pages/about.md").read_text(encoding="utf-8")
for marker in (
    'class="profile-hero"',
    "Research Interests",
    "Selected Research",
    "View all research",
    "/images/rui_profile.jpg",
):
    if marker not in about_source:
        errors.append(f"Home page source missing {marker}")

if not (ROOT / "_includes/research-entry.html").exists():
    errors.append("Missing presentation file: _includes/research-entry.html")

permalinks: dict[str, str] = {}
real_publications: list[dict] = []
for path in (ROOT / "_publications").glob("*.md"):
    match = re.search(r"^permalink:\s*(\S+)", front_matter(path), re.M)
    if not match:
        continue
    permalink = match.group(1)
    if permalink in permalinks:
        errors.append(
            f"Duplicate permalink: {permalink} "
            f"({permalinks[permalink]}, {path.name})"
        )
    permalinks[permalink] = path.name
    if path.name.startswith(("2009-", "2010-")):
        continue
    data = front_matter_data(path)
    real_publications.append(data)
    for field in ("title", "category", "permalink", "authors", "venue", "year"):
        if not data.get(field):
            errors.append(f"Publication {path.name} missing {field}")

if len([p for p in real_publications if p.get("category") == "published"]) < 2:
    errors.append("Research data must contain two published papers")
if len([p for p in real_publications if p.get("selected") is True]) < 3:
    errors.append("Research data must contain at least three selected papers")

research_source = (ROOT / "_pages/publications.html").read_text(encoding="utf-8")
for marker in ("Publications", "Papers Under Review", "Working Papers", "research-entry.html"):
    if marker not in research_source:
        errors.append(f"Research page source missing {marker}")

site_index = ROOT / "_site/index.html"
if site_index.exists():
    rendered = site_index.read_text(encoding="utf-8")
    for marker in (
        'class="site-header"',
        'class="site-main"',
        'href="/research/"',
    ):
        if marker not in rendered:
            errors.append(f"Generated home page missing {marker}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
