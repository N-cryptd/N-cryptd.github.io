# n-cryptd.github.io

Personal website of Nayib Goushesh — static Jekyll site, hosted free on **GitHub Pages** at <https://n-cryptd.github.io>.

No build step, no CI, no JavaScript, no dependencies to update. GitHub builds the site natively (Jekyll) every time something is pushed to `main`.

## How to publish a blog post

Create a file `_posts/YYYY-MM-DD-short-title.md`:

```markdown
---
title: "My post title"
description: "One-line summary shown in listings and search results."
date: 2026-10-06
tags: [Aerospace]
---

Your content in **markdown**.
```

Commit and push — the site rebuilds automatically in ~1 minute. (This can be done from the GitHub web UI too: *Add file → Create new file*, and name the path `_posts/2026-10-06-my-post.md`.)

## How to edit the rest of the site

Everything on the homepage is generated from **one file**: [`_data/site.yml`](_data/site.yml).
Edit projects, experience, services, education, certifications, skills, social links there.

- Design/colors: `assets/css/style.css` (CSS variables at the top).
- Nav/footer skeleton: `_layouts/default.html`.
- Your CV: replace `assets/Nayib_Goushesh_CV.pdf` (same filename).

## Optional local preview

Not required, but if you want to preview before pushing:

```bash
cd N-cryptd.github.io
docker run --rm -p 4000:4000 -v "$PWD:/srv/jekyll" jekyll/jekyll jekyll serve
# open http://localhost:4000
```

## Repo history note

This replaces two earlier attempts:

- `personalweb` — Next.js 16 full-stack app (Prisma/Postgres/Stripe/Redis). Far too heavy for a personal site and impossible to host on GitHub Pages. Kept private as reference.
- `N-cryptd-blog` — Jekyll `minima` starter with one test post. Its purpose is fulfilled by this repo.
