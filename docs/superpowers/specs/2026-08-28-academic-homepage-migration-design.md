# Rui Huang Academic Homepage Migration Design

Date: 2026-08-28

## 1. Objective

Redesign `ruihuang-om.github.io` as a modern GitHub Pages academic website inspired by Chenghuai Li's visual structure while retaining Jekyll, GitHub Pages deployment, the existing domain, and reusable publication data.

The new site will use a compact centered layout, a horizontal top navigation bar, a photo-and-biography hero section, restrained blue-gray styling, a concise home page, a complete Research page, and a direct PDF CV link.

## 2. Confirmed Information Architecture

### Home (`/`)

- Horizontal navigation: Home, Research, CV.
- Square or subtly rounded profile photograph on the left.
- Name, current position, affiliation, short biography, and advisors on the right.
- Compact external-link row for email, Google Scholar, ORCID, GitHub, and CV.
- Research Interests section.
- Selected Research section containing two or three representative papers.
- Link to the complete Research page.
- Compact contact block and footer.

### Research (`/research/`)

- Introductory sentence and Google Scholar link.
- Complete research list generated from the `publications` Jekyll collection.
- Sections:
  1. Publications
  2. Papers Under Review
  3. Working Papers
- Each entry displays title, ordered authors, journal or status, year, and available DOI/paper links.
- Individual publication pages remain available for details and stable URLs.

### CV

- Navigation link opens `/files/Rui_CV_2026_0827_V2.pdf` directly.
- The obsolete placeholder Markdown CV page is removed from navigation but may remain in the repository until final cleanup.

## 3. Technical Approach

Retain Jekyll and the existing Academic Pages repository as the content foundation, but replace its public presentation layer.

### New presentation components

- A custom site-wide default layout without the Academic Pages author sidebar.
- A dedicated home layout.
- A research-list include that reads structured publication front matter.
- A custom masthead/navigation include.
- A focused stylesheet for typography, spacing, responsive behavior, and link states.

### Preserved components

- `_publications/` collection and Markdown-based content management.
- Existing GitHub Pages build workflow and repository name.
- Existing domain and paths where practical.
- Existing profile photograph and identity links.
- Existing CV PDF.
- SEO metadata, sitemap, feed, and redirect plugins where compatible.

### Legacy components

Academic Pages layouts, Sass partials, sample posts, talks, teaching files, and placeholder publications will not be deleted during the first implementation pass. They will be made unreachable from the public navigation. Cleanup may happen only after the redesigned site builds and renders correctly.

## 4. Visual System

- Maximum content width: approximately 1000 px.
- Main accent: academic blue near `#39799b`.
- Body text: deep gray near `#2f3337`.
- Headings: Georgia/Times-style serif stack.
- Body and navigation: Arial/Helvetica-style sans-serif stack.
- Navigation: thin top and bottom rules with a blue active state.
- Portrait: square on desktop; centered above biography on narrow screens.
- Research entries: typography-led lists rather than heavy cards.
- Links: accessible blue with visible hover and keyboard-focus states.
- Desktop: two-column hero followed by single-column sections.
- Mobile: single-column content with a compact responsive navigation.

The design should resemble Chenghuai Li's clear academic hierarchy without copying Wix-specific code, assets, or branding.

## 5. Content Model

Each publication file should use consistent front matter:

```yaml
title: "Paper title"
collection: publications
category: published | under_review | working_papers
permalink: /publication/unique-slug
date: YYYY-MM-DD
authors:
  - "Author One"
  - "Rui Huang"
venue: "Journal or current status"
year: 2026
doi: "https://doi.org/..."
paperurl: ""
selected: true | false
order: 1
```

Existing `citation` values may be retained for compatibility, but visible pages should use the structured fields above. Missing facts will not be invented.

## 6. Known Repository Corrections

The migration must correct the following confirmed issues:

1. `_pages/about.md` lacks YAML front matter and therefore does not generate the root home page. It will receive a valid layout and `permalink: /`.
2. `_data/navigation.yml` has invalid indentation for the CV `url`. It will be rewritten as valid YAML.
3. Both current working-paper files use `/publication/working-paper-electricity-markets`. Each will receive a unique permalink.
4. Template demonstration publications from 2009 and 2010 must not appear in the live Research page.
5. The placeholder Markdown CV content must not be linked publicly.
6. Research navigation will move from `/publications/` to `/research/`, with a redirect retained from the old path where feasible.

## 7. Responsive and Accessibility Requirements

- Functional at desktop, tablet, and phone widths.
- No horizontal overflow at 320 px viewport width.
- Navigation accessible by keyboard.
- Visible focus styles for interactive controls.
- Sufficient text/background color contrast.
- Semantic headings in logical order.
- Meaningful image alternative text.
- External links labeled clearly; no essential information conveyed by icons alone.

## 8. Validation

Before delivery:

1. Build the site with the repository's supported Jekyll/GitHub Pages toolchain.
2. Confirm `/`, `/research/`, individual publication URLs, and the CV URL resolve.
3. Confirm no duplicate permalinks.
4. Inspect desktop and mobile screenshots.
5. Check the generated page for broken internal links and missing assets.
6. Confirm legacy sample content is absent from navigation and visible research lists.
7. Package the verified repository as a replacement ZIP and provide a concise GitHub upload checklist.

## 9. Scope Boundary

This migration does not include Wix hosting, a CMS, analytics setup, a custom domain purchase, publication scraping, or creation of new scholarly content. It also does not delete legacy source files until the redesigned site is verified and the user requests cleanup.
