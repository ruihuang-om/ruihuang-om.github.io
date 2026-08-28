# Uploading the Redesigned Site

1. Keep the original repository ZIP as a backup.
2. Open the `ruihuang-om/ruihuang-om.github.io` repository on GitHub.
3. Upload the contents of this folder to the repository root, preserving all paths.
4. Commit the changes to the branch configured under **Settings > Pages** (currently expected to be `master`).
5. Wait for the GitHub Pages deployment workflow to finish.
6. Verify these public URLs:
   - `https://ruihuang-om.github.io/`
   - `https://ruihuang-om.github.io/research/`
   - `https://ruihuang-om.github.io/files/Rui_CV_2026_0827_V2.pdf`
7. Keep the original ZIP until the deployed pages have been checked on desktop and mobile.

## Files central to the redesign

- `_layouts/site.html`
- `_layouts/publication.html`
- `_includes/site-header.html`
- `_includes/research-entry.html`
- `assets/css/academic-home.css`
- `_pages/about.md`
- `_pages/publications.html`
- `_data/navigation.yml`
- `_publications/*.md`

## Updating publications later

Add or edit a file in `_publications/` and keep these front-matter fields:

```yaml
title: "Paper title"
collection: publications
category: published
permalink: /publication/unique-slug
date: 2026-01-01
authors:
  - "Rui Huang"
venue: "Journal or status"
year: 2026
paperurl: ""
doi: ""
selected: false
order: 5
```

Allowed categories are `published`, `under_review`, and `working_papers`. Set `selected: true` only for papers that should appear on the Home page.
