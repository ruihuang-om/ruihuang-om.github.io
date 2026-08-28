# Academic Homepage Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the public Academic Pages presentation with a modern Chenghuai-inspired GitHub Pages site containing a concise Home page, a complete Research page, and a direct PDF CV link.

**Architecture:** Keep Jekyll, GitHub Pages, and the existing `publications` collection as the content layer. Add a small custom presentation layer composed of one default layout, one masthead include, one research-entry include, and one focused stylesheet; convert page and publication front matter to structured data consumed by those components.

**Tech Stack:** Jekyll, Liquid, YAML front matter, HTML5, CSS3, GitHub Pages, Ruby/Bundler.

**Spec:** `docs/superpowers/specs/2026-08-28-academic-homepage-migration-design.md`

## Global Constraints

- Keep deployment on `ruihuang-om.github.io` with `baseurl: ""`.
- Keep the page content width near 1000 px and the accent color near `#39799b`.
- Use serif headings and Arial/Helvetica-style body text.
- Keep individual publication pages and stable unique permalinks.
- Do not invent authors, statuses, publication details, profile facts, or external URLs.
- Do not delete legacy template files during the first implementation pass.
- Support keyboard navigation, visible focus, semantic headings, and 320 px-wide screens without horizontal overflow.
- Link CV navigation directly to `/files/Rui_CV_2026_0827_V2.pdf`.

---

## File Map

- `_layouts/site.html`: shared HTML shell and metadata integration.
- `_includes/site-header.html`: top navigation and active-page state.
- `_includes/research-entry.html`: one reusable publication rendering unit.
- `assets/css/academic-home.css`: all new public styles and responsive rules.
- `_pages/about.md`: root Home page and selected-research composition.
- `_pages/publications.html`: complete Research page at `/research/`.
- `_data/navigation.yml`: Home, Research, and CV destinations.
- `_config.yml`: publication category names and custom site settings.
- `_publications/*.md`: normalized structured publication metadata.
- `scripts/validate_site.py`: deterministic source and generated-site checks.

### Task 1: Add Source-Level Validation and Repair Routing Data

**Files:**
- Create: `scripts/validate_site.py`
- Modify: `_data/navigation.yml`
- Modify: `_pages/about.md`
- Modify: `_pages/publications.html`

**Interfaces:**
- Consumes: repository root and YAML front matter.
- Produces: a command-line validator returning exit code 0 only when required routes, CV target, and unique publication permalinks are present.

- [ ] **Step 1: Create a validator that initially exposes the existing defects**

```python
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def front_matter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ""
    return text.split("---\n", 2)[1]


errors = []
about = front_matter(ROOT / "_pages/about.md")
research = front_matter(ROOT / "_pages/publications.html")
navigation = (ROOT / "_data/navigation.yml").read_text(encoding="utf-8")

if "permalink: /\n" not in about:
    errors.append("Home page must use permalink /")
if "permalink: /research/" not in research:
    errors.append("Research page must use permalink /research/")
if "url: /files/Rui_CV_2026_0827_V2.pdf" not in navigation:
    errors.append("Navigation must link the current CV PDF")

permalinks = {}
for path in (ROOT / "_publications").glob("*.md"):
    match = re.search(r"^permalink:\s*(\S+)", front_matter(path), re.M)
    if not match:
        continue
    permalink = match.group(1)
    if permalink in permalinks:
        errors.append(f"Duplicate permalink: {permalink}")
    permalinks[permalink] = path.name

if errors:
    print("\n".join(errors))
    sys.exit(1)
```

- [ ] **Step 2: Run validation and confirm the known failures**

Run: `python3 scripts/validate_site.py`

Expected: nonzero exit with missing Home route, missing Research route, and duplicate permalink messages.

- [ ] **Step 3: Rewrite navigation as valid YAML**

```yaml
main:
  - title: "Home"
    url: /
  - title: "Research"
    url: /research/
  - title: "CV"
    url: /files/Rui_CV_2026_0827_V2.pdf
    external: true
```

- [ ] **Step 4: Add valid front matter to the root and Research pages**

Use this Home front matter:

```yaml
---
layout: site
title: "Home"
permalink: /
nav_key: home
---
```

Use this Research front matter:

```yaml
---
layout: site
title: "Research"
permalink: /research/
nav_key: research
redirect_from:
  - /publications/
---
```

- [ ] **Step 5: Give each working paper a unique permalink**

Use `/publication/horizontal-mergers-electricity-markets` and `/publication/pigouvian-energy-surcharge`.

- [ ] **Step 6: Run validation again**

Run: `python3 scripts/validate_site.py`

Expected: exit 0 with no output.

- [ ] **Step 7: Commit the routing repair when working in the Git repository**

```bash
git add scripts/validate_site.py _data/navigation.yml _pages/about.md _pages/publications.html _publications
git commit -m "fix: repair homepage and publication routes"
```

### Task 2: Build the Custom Site Shell and Navigation

**Files:**
- Create: `_layouts/site.html`
- Create: `_includes/site-header.html`
- Create: `assets/css/academic-home.css`

**Interfaces:**
- Consumes: `site.data.navigation.main`, `page.title`, `page.nav_key`, and existing `_includes/head.html` SEO metadata.
- Produces: `.site-shell`, `.site-header`, `.site-nav`, and `.site-main` DOM elements used by every new page.

- [ ] **Step 1: Add generated-site assertions to the validator**

Append checks that run when `_site/index.html` exists:

```python
site_index = ROOT / "_site/index.html"
if site_index.exists():
    rendered = site_index.read_text(encoding="utf-8")
    for marker in ('class="site-header"', 'class="site-main"', 'href="/research/"'):
        if marker not in rendered:
            errors.append(f"Generated home page missing {marker}")
```

- [ ] **Step 2: Create the shared layout**

```html
<!doctype html>
<html lang="{{ site.locale | default: 'en-US' }}">
  <head>
    {% include head.html %}
    <link rel="stylesheet" href="{{ '/assets/css/academic-home.css' | relative_url }}">
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <div class="site-shell">
      {% include site-header.html %}
      <main id="main-content" class="site-main">
        {{ content }}
      </main>
      <footer class="site-footer">
        <span>&copy; {{ 'now' | date: '%Y' }} Rui Huang</span>
        <span>Built with Jekyll and GitHub Pages</span>
      </footer>
    </div>
  </body>
</html>
```

- [ ] **Step 3: Create semantic navigation**

```html
<header class="site-header">
  <nav class="site-nav" aria-label="Primary navigation">
    {% for link in site.data.navigation.main %}
      {% assign active = false %}
      {% if page.url == link.url or page.nav_key == link.title | downcase %}
        {% assign active = true %}
      {% endif %}
      <a class="site-nav__link{% if active %} is-active{% endif %}"
         href="{{ link.url | relative_url }}"
         {% if link.external %}target="_blank" rel="noopener"{% endif %}>
        {{ link.title }}
      </a>
    {% endfor %}
  </nav>
</header>
```

- [ ] **Step 4: Add foundation styling**

Implement these exact tokens at the top of `academic-home.css`:

```css
:root {
  --accent: #39799b;
  --accent-dark: #245c78;
  --text: #2f3337;
  --muted: #68727a;
  --rule: #b7c7d0;
  --surface: #ffffff;
  --max-width: 1000px;
}

* { box-sizing: border-box; }
html { font-size: 16px; scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--text);
  background: var(--surface);
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.58;
}
h1, h2, h3 { font-family: Georgia, "Times New Roman", serif; }
a { color: var(--accent-dark); }
a:focus-visible { outline: 3px solid rgba(57, 121, 155, .35); outline-offset: 3px; }
.site-shell { width: min(calc(100% - 32px), var(--max-width)); margin: 0 auto; }
.site-header { border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); margin-top: 18px; }
.site-nav { display: flex; justify-content: center; flex-wrap: wrap; }
.site-nav__link { padding: 8px 18px; color: var(--text); text-decoration: none; }
.site-nav__link:hover, .site-nav__link.is-active { color: #fff; background: var(--accent); }
.site-main { min-height: 70vh; padding: 42px 0; }
.site-footer { display: flex; justify-content: space-between; gap: 16px; border-top: 1px solid var(--rule); padding: 18px 0 28px; color: var(--muted); font-size: .875rem; }
.skip-link { position: absolute; left: -9999px; }
.skip-link:focus { left: 16px; top: 16px; z-index: 10; background: white; padding: 8px; }
@media (max-width: 640px) {
  .site-shell { width: min(calc(100% - 24px), var(--max-width)); }
  .site-main { padding: 28px 0; }
  .site-nav__link { flex: 1; min-width: 90px; padding: 9px 10px; text-align: center; }
  .site-footer { flex-direction: column; }
}
```

- [ ] **Step 5: Build and validate the shell**

Run: `bundle exec jekyll build`

Expected: exit 0 and `_site/index.html` includes the three required markers.

Run: `python3 scripts/validate_site.py`

Expected: exit 0.

- [ ] **Step 6: Commit the presentation shell**

```bash
git add _layouts/site.html _includes/site-header.html assets/css/academic-home.css scripts/validate_site.py
git commit -m "feat: add custom academic site shell"
```

### Task 3: Implement the Concise Home Page

**Files:**
- Modify: `_pages/about.md`
- Modify: `assets/css/academic-home.css`
- Modify: `_config.yml`

**Interfaces:**
- Consumes: `site.author`, `site.publications`, and publication field `selected`.
- Produces: `.profile-hero`, `.profile-links`, `.research-interests`, and `.selected-research` sections.

- [ ] **Step 1: Extend validation for Home content**

Require the generated Home page to contain `profile-hero`, `Research Interests`, `Selected Research`, the profile image, and a `View all research` link.

- [ ] **Step 2: Add missing identity settings without changing confirmed values**

Set `author.github: "ruihuang-om"` in `_config.yml`. Preserve the existing email, Scholar URL, ORCID URL, photo filename, name, and affiliation.

- [ ] **Step 3: Replace Home page body with the confirmed structure**

```html
<section class="profile-hero">
  <div class="profile-hero__media">
    <img src="{{ '/images/rui_profile.jpg' | relative_url }}" alt="Portrait of Rui Huang">
    <div class="profile-links" aria-label="Academic profiles">
      <a href="mailto:{{ site.author.email }}">Email</a>
      <a href="{{ site.author.googlescholar }}">Google Scholar</a>
      <a href="{{ site.author.orcid }}">ORCID</a>
      <a href="https://github.com/ruihuang-om">GitHub</a>
      <a href="{{ '/files/Rui_CV_2026_0827_V2.pdf' | relative_url }}">CV</a>
    </div>
  </div>
  <div class="profile-hero__copy">
    <h1>Hi! I'm Rui Huang</h1>
    <p>I am a Ph.D. candidate in Management Science and Engineering at the University of Science and Technology of China.</p>
    <p>My research focuses on sustainable operations, electricity markets, energy-efficiency investment, and supply chain contracting.</p>
    <p>I am currently a joint Ph.D. student in Operations Management at Ivey Business School, Western University.</p>
  </div>
</section>

<section class="content-section research-interests">
  <h2>Research Interests</h2>
  <p><strong>Topics:</strong> Sustainable Operations, Energy and Electricity Markets, Energy-Efficiency Investment, and Supply Chain Contracting.</p>
  <p><strong>Methods:</strong> Game Theory, Optimization, and Econometric Analysis.</p>
</section>

<section class="content-section selected-research">
  <h2>Selected Research</h2>
  {% assign selected = site.publications | where: "selected", true | sort: "order" %}
  <ol class="research-list">
    {% for post in selected limit:3 %}
      {% include research-entry.html post=post %}
    {% endfor %}
  </ol>
  <p class="section-link"><a href="{{ '/research/' | relative_url }}">View all research &rarr;</a></p>
</section>
```

- [ ] **Step 4: Add responsive Home styling**

Add a two-column desktop grid (`220px 1fr`), a portrait aspect ratio of `4 / 5`, centered section headings, and a single-column breakpoint at 720 px. The profile image must use `width: 100%`, `height: auto`, and `object-fit: cover`.

- [ ] **Step 5: Build and validate Home**

Run: `bundle exec jekyll build && python3 scripts/validate_site.py`

Expected: both commands exit 0.

- [ ] **Step 6: Commit Home page**

```bash
git add _pages/about.md _config.yml assets/css/academic-home.css scripts/validate_site.py
git commit -m "feat: build concise academic homepage"
```

### Task 4: Normalize Publication Metadata and Build Research Lists

**Files:**
- Create: `_includes/research-entry.html`
- Modify: `_pages/publications.html`
- Modify: `_config.yml`
- Modify: `_publications/huang-2026-working-paper-horizontal-merger.md`
- Modify: `_publications/huang-2026-working-paper-price surcharge.md`
- Modify: real publication files or add them when confirmed from the CV.
- Modify: `assets/css/academic-home.css`
- Modify: `scripts/validate_site.py`

**Interfaces:**
- Consumes: `post.title`, `post.authors`, `post.venue`, `post.year`, `post.paperurl`, `post.doi`, `post.category`, `post.selected`, and `post.order`.
- Produces: semantic `<li class="research-entry">` output shared by Home and Research.

- [ ] **Step 1: Expand validation for publication structure**

For every non-sample publication, require `title`, `category`, unique `permalink`, `authors`, `venue`, and `year`. Permit blank `paperurl` and `doi`.

- [ ] **Step 2: Normalize the horizontal-merger paper**

```yaml
---
title: "Horizontal Mergers in Electricity Markets: Forward Contracting, Renewable Generation, and Welfare"
collection: publications
category: under_review
permalink: /publication/horizontal-mergers-electricity-markets
date: 2026-01-01
authors:
  - "Rui Huang"
  - "Jason Nguyen"
  - "Qinglong Gou"
  - "Juzhi Zhang"
venue: "Under review at Production and Operations Management"
year: 2026
paperurl: ""
doi: ""
selected: true
order: 3
---
```

- [ ] **Step 3: Normalize the Pigouvian-surcharge paper**

```yaml
---
title: "Impacts of a Pigouvian-Like Energy Surcharge on Energy-Efficiency Investment, Competitiveness, and Social Welfare"
collection: publications
category: working_papers
permalink: /publication/pigouvian-energy-surcharge
date: 2026-06-11
authors:
  - "Jason Nguyen"
  - "Rui Huang"
  - "Qinglong Gou"
venue: "Manuscript in preparation for submission"
year: 2026
paperurl: ""
doi: ""
selected: true
order: 4
---
```

- [ ] **Step 4: Add the two published papers from the confirmed CV as structured publication files**

Create entries for the forthcoming EJOR paper with DOI `10.1016/j.ejor.2026.04.052` and the 2026 Energy Journal paper with DOI `10.1177/01956574251368288`. Use the confirmed author ordering from the CV and mark both `selected: true`, orders 1 and 2.

- [ ] **Step 5: Create the reusable publication renderer**

```html
<li class="research-entry">
  <h3 class="research-entry__title"><a href="{{ include.post.url | relative_url }}">{{ include.post.title }}</a></h3>
  {% if include.post.authors %}
    <p class="research-entry__authors">
      {% for author in include.post.authors %}
        {% if author == "Rui Huang" %}<strong>{{ author }}</strong>{% else %}{{ author }}{% endif %}{% unless forloop.last %}, {% endunless %}
      {% endfor %}
    </p>
  {% endif %}
  <p class="research-entry__meta"><em>{{ include.post.venue }}</em>{% if include.post.year %}, {{ include.post.year }}{% endif %}.</p>
  {% if include.post.paperurl or include.post.doi %}
    <p class="research-entry__links">
      {% if include.post.paperurl %}<a href="{{ include.post.paperurl }}">Paper</a>{% endif %}
      {% if include.post.doi %}<a href="{{ include.post.doi }}">DOI</a>{% endif %}
    </p>
  {% endif %}
</li>
```

- [ ] **Step 6: Replace Research page rendering**

Loop explicitly over `published`, `under_review`, and `working_papers`; display a section only when the filtered array is nonempty. Sort each group by `order`, then render each item through `research-entry.html`.

- [ ] **Step 7: Prevent template samples from appearing**

Add `published: false` to the two 2009/2010 demonstration files and filter Research queries with `where_exp: "post", "post.published != false"`.

- [ ] **Step 8: Add research-list styling**

Use an ordinary numbered list, 28--34 px vertical separation, compact author/meta spacing, and no card border or background.

- [ ] **Step 9: Build and validate Research**

Run: `bundle exec jekyll build && python3 scripts/validate_site.py`

Expected: exit 0; `/research/` contains all real papers, no sample titles, and no duplicate permalink.

- [ ] **Step 10: Commit Research page and metadata**

```bash
git add _includes/research-entry.html _pages/publications.html _config.yml _publications assets/css/academic-home.css scripts/validate_site.py
git commit -m "feat: add structured research portfolio"
```

### Task 5: Finish Individual Publication Pages and Remove Public Legacy UI

**Files:**
- Create: `_layouts/publication.html`
- Modify: `_config.yml`
- Modify: `_publications/*.md`
- Modify: `assets/css/academic-home.css`

**Interfaces:**
- Consumes: the same structured publication fields as `research-entry.html` plus Markdown body content.
- Produces: consistent detail pages under `/publication/*` using the custom shell.

- [ ] **Step 1: Create a publication detail layout**

```html
---
layout: site
---
<article class="publication-detail">
  <p class="eyebrow">Research</p>
  <h1>{{ page.title }}</h1>
  {% if page.authors %}<p class="publication-detail__authors">{{ page.authors | join: ", " }}</p>{% endif %}
  <p class="publication-detail__meta"><em>{{ page.venue }}</em>{% if page.year %}, {{ page.year }}{% endif %}.</p>
  {% if page.paperurl or page.doi %}
    <p class="publication-detail__links">
      {% if page.paperurl %}<a href="{{ page.paperurl }}">Download paper</a>{% endif %}
      {% if page.doi %}<a href="{{ page.doi }}">View DOI</a>{% endif %}
    </p>
  {% endif %}
  <div class="publication-detail__body">{{ content }}</div>
</article>
```

- [ ] **Step 2: Apply the publication layout through collection defaults**

Set the `publications` default layout in `_config.yml` to `publication` and turn off comments/share settings for the redesigned pages.

- [ ] **Step 3: Verify legacy UI is unreachable from primary navigation**

Check generated Home and Research HTML for `author_profile`, `sidebar`, `/talks/`, `/teaching/`, and placeholder CV copy; none should appear.

- [ ] **Step 4: Build and test detail URLs**

Run: `bundle exec jekyll build && python3 scripts/validate_site.py`

Expected: all real `/publication/*` pages exist and use `class="publication-detail"`.

- [ ] **Step 5: Commit publication detail pages**

```bash
git add _layouts/publication.html _config.yml _publications assets/css/academic-home.css scripts/validate_site.py
git commit -m "feat: redesign publication detail pages"
```

### Task 6: Visual, Responsive, and Delivery Verification

**Files:**
- Modify if required: `assets/css/academic-home.css`
- Modify if required: page/layout files implicated by validation.
- Create: `MIGRATION.md`

**Interfaces:**
- Consumes: generated `_site` output.
- Produces: verified desktop/mobile pages, migration instructions, and a distributable ZIP.

- [ ] **Step 1: Perform a clean production build**

Run:

```bash
bundle exec jekyll clean
JEKYLL_ENV=production bundle exec jekyll build
python3 scripts/validate_site.py
```

Expected: all commands exit 0.

- [ ] **Step 2: Serve the generated site locally**

Run: `bundle exec jekyll serve --host 0.0.0.0 --port 4000`

Expected: server reports the site at port 4000 without build errors.

- [ ] **Step 3: Inspect required routes at desktop width**

Inspect `/`, `/research/`, both published-paper pages, both working-paper pages, and `/files/Rui_CV_2026_0827_V2.pdf` at approximately 1365 px viewport width.

Expected: no missing assets, no Page Not Found, no Academic Pages sidebar, and no horizontal overflow.

- [ ] **Step 4: Inspect Home and Research at mobile width**

Inspect at 390 px and 320 px widths.

Expected: portrait stacks above biography, nav remains usable, research titles wrap, and `document.documentElement.scrollWidth <= window.innerWidth`.

- [ ] **Step 5: Check links and accessibility essentials**

Verify keyboard focus through navigation and profile links, image alt text, logical heading order, and HTTP/file existence for internal links.

- [ ] **Step 6: Write migration instructions**

Document:

```markdown
# Uploading the Redesigned Site

1. Back up the current GitHub repository.
2. Upload the contents of this folder to the repository root, preserving paths.
3. Commit to the branch configured under Settings > Pages.
4. Wait for the GitHub Pages workflow to finish.
5. Verify `/`, `/research/`, and `/files/Rui_CV_2026_0827_V2.pdf`.
6. Keep the previous ZIP until the deployed site is confirmed.
```

- [ ] **Step 7: Create the delivery ZIP without transient build artifacts**

Run from the parent directory:

```bash
zip -r ruihuang-om.github.io-redesigned.zip ruihuang-om.github.io-master \
  -x '*/_site/*' '*/.jekyll-cache/*' '*/.sass-cache/*' '*/vendor/*'
```

Expected: ZIP contains source, images, CV PDF, design, plan, validation script, and migration instructions; it does not contain build caches.

- [ ] **Step 8: Commit final validation adjustments when working in the Git repository**

```bash
git add assets/css/academic-home.css MIGRATION.md
git commit -m "docs: finalize homepage migration"
```
