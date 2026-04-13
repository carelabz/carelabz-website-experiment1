# CareLAbz Migration Agent Team

This folder contains 7 specialized Claude Code subagents that together form a full WordPress → Strapi 5 → Next.js 14 migration pipeline for the CareLAbz website rebuild.

## The team

| Order | Agent | Role |
|---|---|---|
| Lead | **migration-orchestrator** | Conductor. Dispatches the other agents and verifies handoffs. |
| 1 | **wp-scraper** | Extracts content from a live WordPress URL → `data/wp-extracts/{slug}.json` |
| 2 | **content-transformer** | Maps extract to Strapi payload with AEO rewrites → `data/strapi-payloads/{slug}.json` |
| 3 | **strapi-loader** | Uploads payload to Strapi via API, publishes, verifies → `data/strapi-receipts/{slug}.json` |
| 4 | **nextjs-page-builder** | Creates the Next.js 14 App Router page that fetches from Strapi |
| 5 | **seo-aeo-auditor** | Runs the 37-point SEO + AEO audit, returns pass/fail |
| 6 | **qa-verifier** | Runs build, lint, dev server, redirect test, Lighthouse, screenshot |

## The pipeline

```
wp-scraper → content-transformer → strapi-loader → nextjs-page-builder → seo-aeo-auditor → qa-verifier
```

Each step writes an artifact that the next step reads. If any step fails, the pipeline stops for that page and the orchestrator escalates.

## How to use

### Migrate a single page

In Claude Code, at the project root, run:

```
/agents migration-orchestrator
```

Then give it a task like:

> Migrate `https://carelabz.com/short-circuit-analysis/` to the new route `/ae/services/study-analysis/short-circuit-analysis/`. Match the design of the existing arc-flash-study page. Add the 301 redirect.

The orchestrator will dispatch all six downstream agents and report progress.

### Migrate a batch (Phase 2)

Give the orchestrator a list:

> Migrate these 15 pages for the UAE. Run them sequentially, pause after every 3 so I can spot-check, and give me a final batch report at the end.
>
> 1. https://carelabz.com/short-circuit-analysis/ → /ae/services/study-analysis/short-circuit-analysis/
> 2. https://carelabz.com/load-flow-analysis/ → /ae/services/study-analysis/load-flow-analysis/
> 3. ... (etc)

### Run a single agent directly (for debugging)

If you just want to re-run the audit on a page that already shipped:

```
/agents seo-aeo-auditor
```

Then:

> Audit `src/app/ae/services/study-analysis/arc-flash-study/page.tsx` against the canonical `https://carelabz.com/ae/services/study-analysis/arc-flash-study/`.

## Directory layout the agents expect

```
website_rebuild_project/
├── .claude/agents/          ← this folder (7 agents + this README)
├── data/                    ← created on first run
│   ├── wp-extracts/         ← wp-scraper output
│   ├── strapi-payloads/     ← content-transformer output
│   ├── strapi-responses/    ← strapi-loader API responses (debug)
│   ├── strapi-receipts/     ← strapi-loader success receipts
│   ├── strapi-errors/       ← strapi-loader failures (debug)
│   ├── audits/              ← seo-aeo-auditor markdown reports
│   └── screenshots/         ← qa-verifier page screenshots
├── src/                     ← Next.js app
├── carelabz-cms/            ← Strapi 5 app
└── public/images/migrated/  ← images downloaded by wp-scraper
```

Add `data/` to `.gitignore` if you don't want the intermediate artifacts in version control. Or keep them for audit trail — your call. Recommended: keep `data/audits/` and `data/strapi-receipts/` checked in, ignore everything else.

## Handoff contracts (what each agent reads and writes)

| Agent | Reads | Writes |
|---|---|---|
| wp-scraper | WP URL | `data/wp-extracts/{slug}.json`, `public/images/migrated/{slug}/*` |
| content-transformer | `data/wp-extracts/{slug}.json`, Strapi schema | `data/strapi-payloads/{slug}.json` |
| strapi-loader | `data/strapi-payloads/{slug}.json`, `.env.local` | `data/strapi-receipts/{slug}.json` |
| nextjs-page-builder | Strapi API (live), `CLAUDE.md`, reference pages | `src/app/{route}/page.tsx`, `next.config.mjs`, `src/app/sitemap.ts` |
| seo-aeo-auditor | page file, layout, sitemap, next.config | `data/audits/{slug}-{timestamp}.md` |
| qa-verifier | page file, dev server | `data/screenshots/{slug}.png`, logs in `/tmp/` |

## Rules every agent follows

1. **Single responsibility.** No agent does another agent's job.
2. **Read-only contracts.** Upstream artifacts are never modified by downstream agents.
3. **Explicit failure.** Every agent returns a structured `{status: "success"|"error", ...}` JSON blob.
4. **No git commits mid-pipeline.** Only the orchestrator (or the user) commits after the full batch.
5. **No silent data loss.** If something can't be mapped, it goes into a `warnings` array — never dropped quietly.
6. **No secrets in logs.** API tokens are redacted from any Bash output.

## When to use the team vs. plain Claude Code

**Use the agent team when:**
- Migrating 3+ pages
- You want a repeatable, auditable pipeline
- You want Phase 2 (UAE rollout, ~20 pages) or Phase 3 (50 countries) to run unattended in batches

**Skip the team and use plain Claude Code when:**
- One-off edit to an existing page
- Experimenting with design changes
- Debugging a single component
- Any task that's not a full page migration

The orchestrator has overhead — it's worth it for batches, overkill for single-file edits.

## Extending the team

To add a new agent (e.g., `image-optimizer` or `i18n-translator`):
1. Create `.claude/agents/{name}.md` with YAML frontmatter (name, description, tools, model)
2. Write a strict single-responsibility system prompt
3. Define input/output contracts explicitly
4. Update this README and the `migration-orchestrator` agent's dispatch list
5. Test on one page before running a batch

## Troubleshooting

**The orchestrator doesn't dispatch the other agents.**
→ Check that all 7 files are in `.claude/agents/` and each has valid YAML frontmatter. Run `cat .claude/agents/*.md | head -20` to sanity check.

**An agent says "cannot find file".**
→ The upstream agent failed silently. Check that agent's output JSON for a `warnings` array.

**Strapi-loader returns 401.**
→ Token expired. Regenerate in Strapi admin, update `.env.local`, restart.

**Build fails in qa-verifier with a TypeScript error.**
→ The page-builder generated code that doesn't match the Strapi type. Hand back to page-builder with the error message.

**Lighthouse score is low.**
→ Usually images. Run the image-optimizer (if you've built one) or compress manually with `sharp-cli`.

## Changelog

- **2026-04-10** — Initial team created: orchestrator + 6 specialists. Optimized for Phase 2 (UAE rollout) and Phase 3 (50 countries).
