# PLANNING_STATE — n-cryptd.github.io

> **Ground truth** together with the filesystem and GitHub. Update after every state change.
> Operating manual: `AGENTS.md`. Snapshot date: **2026-10-06** (autonomous-dev scaffolding day; nightly dev loop starts this night — one combined 3 AM automation covers this repo and personalweb sequentially, this repo is PART 2).

## Last Updated
2026-10-06 (initial): Site went live earlier today (built from personalweb's mined content, Jekyll on legacy Pages build). Design flare added (aurora hero, flight path, scroll reveals — commit d5ee8ba). Name corrected to Nayib Martin Goushesh. Autonomous-dev scaffolding created (AGENTS.md + this file); seed issues #1–#5 opened; daily 4 AM cron scheduled. No code changes in this scaffolding pass.

## Mission
Make <https://n-cryptd.github.io> a genuinely good landing page for Nayib Martin Goushesh's projects — fast, honest, zero-JS, zero-maintenance — iteratively improved by the nightly agent within the guardrails in AGENTS.md.

## Current State
- Live, healthy, Pages legacy build green at commit `bc27bcd`+ (docs-only commits after).
- Content: single-page portfolio (hero, services, projects ×4, experience, education+certs, skills, contact) + blog (4 posts: 3 migrated from personalweb + 1 meta post) + 404 + feed + sitemap. All content in `_data/site.yml`.
- Known content gap: the projects section only shows the 4 projects inherited from the old portfolio; the user's GitHub has far more public work worth showcasing (math-channel, MyBrain, open-webSearch, SIERRA, CryptoCNN/CryptoCNNN, arc-agi-3-hermes, Alpaca-LoRA-Serve, rpi-hunter, ebayMarketAnalyzer — check each repo's actual public status before linking).
- No CI workflow yet; no OG images; meta descriptions only partially per-page; no project-detail pages.

## Roadmap (phases; each lands as small reviewed commits tracked by issues)
- **Phase 0 — Guardrails**: local build recipe verified, add a CI workflow that runs `jekyll build` (+ link check) on PRs/push so liquid/config errors are caught outside the live build. → issue #1
- **Phase 1 — Project showcase depth**: expand projects beyond the inherited 4 — curate from real public GitHub repos (read each repo, write honest 1–2 line descriptions, link only public ones); consider a dedicated `/projects/` page with richer cards while the homepage keeps a curated shortlist; per-project links to repos/demos/papers. → issue #2
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
- 2026-10-06 (scaffold session): AGENTS.md + PLANNING_STATE.md written, issues #1–#5 opened, scheduled as PART 2 of the combined nightly 3 AM dev-loop automation (shared with personalweb — platform allows one scheduled task per session). No code changes.
