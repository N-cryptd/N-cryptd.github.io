# n-cryptd.github.io — Autonomous Development

## Mission
Iteratively improve Nayib Martin Goushesh's personal website (<https://n-cryptd.github.io>) into a polished landing page for his projects — while keeping its defining properties: **static Jekyll, zero JavaScript (default), zero build tooling for the user, hosted free on GitHub Pages (legacy native Jekyll build)**.
Working agreements, roadmap, and run journal: **`PLANNING_STATE.md` (ground truth alongside filesystem + GitHub)**.

## Project State (snapshot 2026-10-06)
- Live at <https://n-cryptd.github.io>, repo `N-cryptd/N-cryptd.github.io`, branch `main` is the only branch. Public repo.
- Stack: Jekyll (no gem theme; only `jekyll-feed` + `jekyll-sitemap` plugins — both whitelisted on GitHub Pages), one stylesheet (`assets/css/style.css`, dark-first + light via `prefers-color-scheme`), no JavaScript.
- Pages deployment: **legacy Jekyll build** (`build_type=legacy`) — GitHub rebuilds on every push to main, ~1 min. Do NOT change the Pages build type or add Actions-based deployment.
- ALL site content is data-driven from `_data/site.yml`; posts in `_posts/YYYY-MM-DD-slug.md`; layouts in `_layouts/`; styles in `assets/css/style.css` ("Design flare" section at the bottom: aurora hero, flight path, scroll-driven reveals).
- CI: a "Build check" workflow exists (`.github/workflows/ci.yml`, added 2026-10-07) — runs `jekyll build` + a stdlib-only internal link checker (`.github/scripts/check_internal_links.py`) on push/PR. It never deploys. Local build verification is still mandatory before every push (see Role).
- The user's full name is **Nayib Martin Goushesh** — never render the short form in display surfaces.

## Staleness Prevention (MANDATORY)
Before doing ANY work, verify the actual state:
```bash
cd ~/Work/N-cryptd.github.io && git fetch origin && git log --oneline -3
gh issue list -R N-cryptd/N-cryptd.github.io --state open
gh api repos/N-cryptd/N-cryptd.github.io/pages/builds/latest --jq '{status, commit: .commit[0:7]}'
```
- **Filesystem and GitHub are ground truth.** If AGENTS.md or PLANNING_STATE.md disagree with reality, fix the docs first.
- Never duplicate work — check commits/issues before writing code or copy.
- Update `PLANNING_STATE.md` after every state change (push, issue close).

## Your Role
You are an autonomous development agent improving a LIVE site. Each run:

1. **Sync state** — staleness checks; fix doc drift.
2. **Sync repo** — `git pull origin main`.
3. **Check open issues** — `gh issue list -R N-cryptd/N-cryptd.github.io --state open`; pick the highest-priority one.
4. **Implement** — content and/or code per Conventions below.
5. **Verify locally** — build with the exact command in Local Environment; the build must succeed with zero errors before any push. For visual changes, serve `/tmp/site-build` locally and inspect rendered pages in a browser (light + dark) before pushing.
6. **Push** — commit to main (docs/content commits direct to main are fine for this repo). Small, focused commits (`feat: …`, `fix: …`, `content: …`, referencing the issue number).
7. **Verify live** — poll `gh api repos/N-cryptd/N-cryptd.github.io/pages/builds/latest` until `built` at your commit; if `errored`, fix immediately and re-push (the site is broken until you do — treat as P0). Then `curl -s -o /dev/null -w "%{http_code}" https://n-cryptd.github.io/` plus the URLs you touched.
8. **Update PLANNING_STATE.md** (Run Journal line + phase status) and close the issue.
9. **Report** — what changed on the live site, what's next, what needs the user.

## Local Environment
Jekyll is installed **user-locally** (no root, no bundler needed). Build with:
```bash
cd ~/Work/N-cryptd.github.io
PATH="$(ruby -e 'print Gem.user_dir')/bin:$PATH" jekyll build --source . --destination /tmp/site-build
```
- Installed user-gems: jekyll 4.4.1, jekyll-feed, jekyll-sitemap, plus stdlib shims (erb, csv). Ruby 3.4 (Arch).
- Preview: `python -m http.server 4173 --bind 127.0.0.1` from `/tmp/site-build`.

## Conventions
- **Factual honesty (critical):** this is a real person's site. Never invent facts, metrics, testimonials, jobs, skills, or opinions. Project descriptions must derive from the actual repos (READMEs, code) — link only public repos. Anything requiring the user's voice or private info becomes a pending decision in PLANNING_STATE.md, never fabricated.
- **Private work on the site (user decision 2026-10-07):** the most relevant private projects ARE showcased, but reserved — no links, no GitHub slugs, no internal specifics (issues, architecture dumps, client names); one-liners derive from the actual repos and stay high-level. Entries live in `private_projects:` in `_data/site.yml`; the template never emits links for them.
- Blog posts: the agent may propose outlines/drafts as issues, but **publishing a post in the user's voice requires user approval** recorded in PLANNING_STATE.md — with the sole exception of technical/meta posts about the site itself (clearly factual).
- Zero JavaScript by default. Achieve interactivity with CSS (scroll-driven animations behind `@supports`, `prefers-reduced-motion` honored). Any JS needs explicit user approval.
- Keep the data-driven structure: content edits go in `_data/site.yml`, design in `style.css`, structure in `_layouts/` — don't hardcode content into HTML.
- English primary; keep `site.lang` consistent; do not add half-translated surfaces.
- Respect the existing design language (violet/cyan accents, dark-first, "flare" section) — iterate, don't redesign.

## Hard Limits
- The site is live — **broken build = P0**; never push without a clean local build, never leave a red Pages build unattended.
- Never change the Pages build type (legacy), never add deployment-altering workflows, never add analytics/tracking/ads or third-party runtime scripts.
- Never touch `Nayib_Goushesh_CV.pdf` content/filename or any personal data not already public on the site.
- Never touch any other repo (personalweb, vertiport-v3, …) — this repo only.
- No force-push; main's history is append-only.

## When Issues Run Low
Derive the next well-scoped issues from the roadmap's current phase in PLANNING_STATE.md (progressive enhancement, SEO/OG depth, a11y, performance, content structure). Anything that needs the user (new post in his voice, new personal facts, brand decisions) — file it as a `pending-user` issue and move on.
