---
title: "How every post gets its social preview banner"
description: "Link previews here come from a committed Python script that renders one SVG template into a PNG per post. Stdlib only, design-time only, zero JavaScript."
og_image: /assets/og/how-every-post-gets-its-social-preview-banner.png
date: 2026-10-14
tags: [Meta]
---

The last post covered this site's whole discoverability stack, and mentioned the social preview cards in a single bullet. This post goes a level deeper, because the banner pipeline is the one part of the stack that isn't Jekyll: every post carries its own 1200×630 image, and none of them was made in an image editor or is generated when someone pastes a link. They are rendered from a single SVG template by a committed Python script — `tools/generate_og_images.py` — and every claim below maps to a file you can open in the repo.

**One template, written as code.** The design mirrors the homepage hero: the dark background (`#0b0d12`), three soft "aurora" ellipses in violet, cyan, and amber, the post title in a white-to-violet gradient, and a small violet-to-cyan accent bar. In the script, that template is just Python f-strings emitting SVG markup — gradients defined once, blob placement fixed, the title dropped in per post. The site-wide banner (`assets/og-image.png`) comes from the same file with its own layout: name, role, location.

**Front matter, parsed with the standard library.** For each file in `_posts/`, the script needs exactly three keys — `title`, `date`, `tags` — plus the filename for the slug. Instead of pulling in a YAML library, it uses a ~15-line parser for the flat `key: value` and `key: [a, b]` shapes these posts use. That is a deliberate trade-off: it is not a general YAML parser, and nested front matter would confuse it — but every key it needs is flat, so the dependency list stays at "the Python standard library". Titles and meta lines go through `html.escape` before entering the SVG, so a stray `&` or `<` in a title can't break the markup.

**Wrapping text without a font library.** SVG text doesn't line-break itself, and measuring real glyph widths would need a text-shaping library. The script approximates: a bold glyph is roughly 0.56× the font size wide, so it tries title sizes from 64 px down to 46 px until the whole title fits in at most three lines, and uses the estimate only to choose the line breaks. The actual rendering — and any place the estimate is slightly off — is pango's job inside `rsvg-convert`.

**Rendering happens at design time.** `rsvg-convert` (librsvg's command-line tool) turns each SVG into a 1200×630 PNG. This is the only step that isn't pure Python, and it runs once, locally, when a post is added. Visitors never touch it; GitHub Pages' build never runs it; nothing is rendered at request time anywhere — when a link is pasted into a chat app, the image is already sitting in the repo.

**Everything ships as committed files.** Per-post PNGs land in `assets/og/<slug>.png`, the site banner overwrites `assets/og-image.png`, and the SVG sources stay in `tools/og-svg/` for reference. The whole `tools/` directory is in Jekyll's exclude list, so none of the machinery ships — only the images. Adding a post means two manual steps: run the script, then add one front-matter line (`og_image: /assets/og/<slug>.png`).

**The fallback is one line of Liquid.** In `_layouts/default.html`, the `og:image` tag emits `page.og_image` when present and the site banner otherwise — same for the alt text. A post whose banner hasn't been generated yet still gets a correct, on-brand card instead of nothing. Every page also declares `og:image:width` and `og:image:height` (1200×630), which the script guarantees by passing explicit dimensions on every render.

**What this deliberately isn't:** no headless browser, no image-rendering service, no per-request work, and no JavaScript anywhere in the chain. The whole pipeline is ~230 lines of stdlib Python plus one external binary, re-runnable by anyone who clones the repo — which is the same standard the rest of this site is held to.
