# PLANNING_STATE — n-cryptd.github.io

> **Ground truth** together with the filesystem and GitHub. Update after every state change.
> Operating manual: `AGENTS.md`. Snapshot date: **2026-10-06** (autonomous-dev scaffolding day; this repo gets its OWN nightly cron, created separately by the user — suggested 4 AM so it doesn't overlap personalweb's 3 AM cron; plain dev loop, NO agent harness — DeepSeek Harness is reserved for personalweb's Phase 3 agent layer only).

## Last Updated
2026-10-07 (run 2 — user-directed): Private-projects showcase added to homepage per user decision ("most relevant private projects, more reserved, still some info"): new `private_projects:` block in site.yml (vertiport-v3, ARES, Aria/AOG, TRADER) + reserved rendering (no links, dashed PRIVATE badge) in fd09f9a. Visual QA dark/light/390px passed; Pages + CI green at fd09f9a. Rule recorded in AGENTS.md Conventions. #2 remains open for the public-repo expansion.

## Mission
Make <https://n-cryptd.github.io> a genuinely good landing page for Nayib Martin Goushesh's projects — fast, honest, zero-JS, zero-maintenance — iteratively improved by the nightly agent within the guardrails in AGENTS.md.

## Current State
- Live, healthy, Pages legacy build green at commit `bc27bcd`+ (docs-only commits after).
- Content: single-page portfolio (hero, services, projects ×4 public + **private_projects ×4 reserved**: vertiport-v3, ARES, Aria/AOG, TRADER — user decision 2026-10-07, see AGENTS.md Conventions) + experience, education+certs, skills, contact) + blog (4 posts: 3 migrated from personalweb + 1 meta post) + 404 + feed + sitemap. All content in `_data/site.yml`.
- Known content gap: the projects section only shows the 4 projects inherited from the old portfolio; the user's GitHub has far more public work worth showcasing (math-channel, MyBrain, open-webSearch, SIERRA, CryptoCNN/CryptoCNNN, arc-agi-3-hermes, Alpaca-LoRA-Serve, rpi-hunter, ebayMarketAnalyzer — check each repo's actual public status before linking).
- CI: "Build check" workflow (jekyll build + internal link check) green on main since 3780deb (2026-10-07). Still missing: OG images; meta descriptions only partially per-page; no project-detail pages.

## Roadmap (phases; each lands as small reviewed commits tracked by issues)
- **Phase 0 — Guardrails** ✅ done 2026-10-07: local build recipe verified, CI "Build check" workflow runs `jekyll build` + internal link check on PRs/push. → issue #1 (closed)
- **Phase 1 — Project showcase depth**: expand projects beyond the inherited 4 — curate from real public GitHub repos (read each repo, write honest 1–2 line descriptions, link only public ones); consider a dedicated `/projects/` page with richer cards while the homepage keeps a curated shortlist; per-project links to repos/demos/papers. Private-work extension DONE 2026-10-07 (fd09f9a). → issue #2 (open)
- **Phase 2 — Discoverability**: per-page meta descriptions, `og:image` (a generated static banner, no runtime JS), verified sitemap/feed, structured data (Person JSON-LD), favicon polish. → issue #3
- **Phase 3 — Quality passes**: a11y audit (contrast, focus order, landmarks), performance (image optimization if any images appear, font strategy — currently system fonts), visual QA light+dark on all pages, mobile. → issues #4, #5
- **Phase 4 — Content growth** (mostly pending-user): blog posts in the user's voice need his approval (see AGENTS.md Conventions); the agent may propose outlines as `pending-user` issues. Site-meta posts (like the hello-world one) are fair game.

## Pending User Decisions
- None blocking. Future: whether to add a Spanish version; whether any analytics is wanted (currently none, by design); custom domain.

## Working Agreements
- Small focused commits to main; local build green before every push; live Pages build verified after (errored build = P0).
- One issue or coherent chunk per nightly run; blockers + next step into this file before the run ends.
- Factual honesty rule applies to everything (AGENTS.md → Conventions).

## Run Journal (append one line per nightly run)
- 2026-10-06 (scaffold session): AGENTS.md + PLANNING_STATE.md written, issues #1–#5 opened. Scheduling: a separate cron for this repo is created BY THE USER (platform allows one scheduled task per session) — handover definition delivered: daily 4 AM, plain dev loop (the session does the work directly; no agent harness — dsh is reserved for personalweb's Phase 3). Until that cron exists, no autonomous runs happen here. No code changes.
- 2026-10-07 (run 1): Issue #1 closed — added `.github/workflows/ci.yml` (Build check: ruby 3.4, gem-install jekyll+whitelisted plugins, JEKYLL_ENV=production build) + `.github/scripts/check_internal_links.py` (stdlib-only internal link/fragment checker, negative-tested). Local build clean, checker 100/100 refs OK; pushed 3780deb; Actions run green 27s; Pages built at 3780deb; live home/blog/css all 200. Docs updated (Phase 0 ✅). Next: #2.
- 2026-10-07 (run 2, user-directed inter-run): User decision — showcase most relevant private projects, reserved. Implemented in fd09f9a: `private_projects:` in site.yml (vertiport-v3 research, ARES Rust sim engine, Aria AOG agent, TRADER platform; one-liners derived from actual repo READMEs/metadata, read via gh while authenticated — no other repo was modified), homepage sub-block "Selected private projects" with dashed PRIVATE badges, no links by template design. Visual QA (browser, dark + light-palette + 390px) passed. CI + Pages green at fd09f9a; live HTML verified. Standing rule added to AGENTS.md Conventions. #2 still open for public-repo curation.
