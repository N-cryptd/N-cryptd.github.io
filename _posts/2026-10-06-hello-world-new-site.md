---
title: "Hello world — a new site on GitHub Pages"
description: "Why I rebuilt my personal website as a static Jekyll site on GitHub Pages, and how to keep it running."
date: 2026-10-06
tags: [Meta]
---

Welcome to the new home of my personal website. If you've been here before, you might notice the URL is simpler, the pages load instantly, and — most importantly — I'll actually keep this one updated.

**Why the rebuild?** My previous attempt was a full Next.js application with a database, authentication, payments, background jobs, and monitoring. It could do everything except stay online and stay maintained. A personal website doesn't need any of that: it needs to be readable, fast, and trivially easy to change. So I moved to a static Jekyll site hosted directly on GitHub Pages — no server, no database, no build pipeline to babysit. GitHub builds the site automatically on every push.

**How maintenance works now** — and this is the part I care about:

- **Publishing a post** means creating one markdown file: `_posts/YYYY-MM-DD-title.md` with a small front-matter block (title, date, description, tags) and the content below it. Commit, push, and the site rebuilds in about a minute. It can even be done from the GitHub web editor on my phone.
- **Editing projects, experience, or skills** means changing one data file: `_data/site.yml`. All the sections of the homepage are generated from it.
- **Design changes** live in a single stylesheet, `assets/css/style.css`. There is no JavaScript, no framework, and nothing to update for security.

The old articles — on deep reinforcement learning for vertiport operations, the European U-space framework, and building agents with LangChain and local LLMs — were migrated from the previous site, and they're all listed in the [blog archive](/blog/).

Here's to shipping the boring, reliable version.
