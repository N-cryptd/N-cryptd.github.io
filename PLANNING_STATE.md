# PLANNING_STATE — n-cryptd.github.io

> **Ground truth** together with the filesystem and GitHub. Update after every state change.
> Operating manual: `AGENTS.md`. Snapshot date: **2026-10-06** (autonomous-dev scaffolding day; this repo gets its OWN nightly cron, created separately by the user — suggested 4 AM so it doesn't overlap personalweb's 3 AM cron; plain dev loop, NO agent harness — DeepSeek Harness is reserved for personalweb's Phase 3 agent layer only).

## Last Updated
2026-10-08 (run 3): Issue #2 closed — dedicated `/projects/` page landed in b01f081+c845979: new `open_projects:` block in site.yml (math-channel, arc-agi-3-hermes, SIERRA, CryptoCNN — descriptions from actual READMEs) + page with Featured/Open source/Private sections; homepage keeps the curated shortlist and gains an "All projects →" link; nav Projects → /projects/. Forks (MyBrain, open-webSearch, Alpaca-LoRA-Serve, ebayMarketAnalyzer, rpi-hunter, context-portal) excluded — zero commits by N-cryptd in them. Visual QA dark/light/390px passed; CI + Pages green at c845979; live /projects/ verified. #3 next.

## Mission
Make <https://n-cryptd.github.io> a genuinely good landing page for Nayib Martin Goushesh's projects — fast, honest, zero-JS, zero-maintenance — iteratively improved by the nightly agent within the guardrails in AGENTS.md.

## Current State
- Live, healthy, Pages legacy build green at commit `bc27bcd`+ (docs-only commits after).
- Content: single-page portfolio (hero, services, projects ×4 public + **private_projects ×4 reserved**: vertiport-v3, ARES, Aria/AOG, TRADER — user decision 2026-10-07, see AGENTS.md Conventions) + experience, education+certs, skills, contact) + blog (4 posts: 3 migrated from personalweb + 1 meta post) + 404 + feed + sitemap. All content in `_data/site.yml`.
- **Dedicated `/projects/` page (2026-10-08, c845979)**: featured ×4 + `open_projects` ×4 (math-channel, arc-agi-3-hermes, SIERRA, CryptoCNN) + private ×4. Curation rule: forks of other people's repos are never showcased (N-cryptd has zero own commits in MyBrain, open-webSearch, Alpaca-LoRA-Serve, ebayMarketAnalyzer, rpi-hunter, context-portal — verified via API 2026-10-08); `Scripts` (no README) and `Gitcoin_Nervos` (screenshot-only README, 2021) skipped as not showcaseable. `CryptoCNNN` from the original issue list does not exist (deleted/renamed).
- CI: "Build check" workflow (jekyll build + internal link check) green on main since 3780deb (2026-10-07). Still missing: OG images; meta descriptions only partially per-page; no project-detail pages.

## Roadmap (phases; each lands as small reviewed commits tracked by issues)
- **Phase 0 — Guardrails** ✅ done 2026-10-07: local build recipe verified, CI "Build check" workflow runs `jekyll build` + internal link check on PRs/push. → issue #1 (closed)
- **Phase 1 — Project showcase depth** ✅ done 2026-10-08: private-work extension (fd09f9a) + public-repo curation and dedicated `/projects/` page (b01f081, c845979). → issue #2 (closed)
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
- 2026-10-08 (run 3): Issue #2 closed — Phase 1 complete. Curated PUBLIC repos into a dedicated `/projects/` page (b01f081 site.yml `open_projects:`, c845979 page+nav): math-channel, arc-agi-3-hermes, SIERRA, CryptoCNN, each description derived from the repo's own README; homepage keeps the shortlist + "All projects →"; `private-head`→`sub-head` rename (pattern no longer private-specific). Honesty screening: all 6 fork candidates verified zero own commits via API → excluded; Scripts (no README), Gitcoin_Nervos (screenshot-only README) skipped; CryptoCNNN doesn't exist. Visual QA (browser: dark + light-palette + 390px, both pages) passed; link checker 105 refs OK; CI green 36s; Pages built at c845979; live home + /projects/ 200 with all 4 cards. Next: #3 (Phase 2 discoverability).
