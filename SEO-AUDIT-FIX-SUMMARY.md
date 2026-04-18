# SEO Audit Fix Summary — Branch: fix/us-seo-audit-fixes

## What was fixed

### Strapi Content (via API — 4 fixes)
1. **Blog slug mismatch** — `importance-of-electrical-safety-inspection-usa` renamed to `upgrading-your-power-system-short-circuit-analysis` (content was about short circuits, not inspections)
2. **Arc flash facts slug** — `importance-arc-flash-hazard-analysis-mitigation-usa` renamed to `which-of-these-facts-about-arc-flashes-are-true` (matches article title)
3. **Electrical inspection "near me"** — restored local SEO keyword in metaTitle/metaDescription
4. **Arc flash facts metaDescription** — restored "arc flash analysis in the USA" keyword

### Code Changes (5 fixes)
5. **301 redirects updated** — old blog slug URLs now redirect to new correct slugs
6. **Blog index metadata** — title updated to include "Power System Studies & Analysis"
7. **JSON-LD on all service pages** — added LocalBusiness (with address/phone/email), Speakable, HowTo schemas to the shared `[slug]/page.tsx`. All 9 US service pages now have 6 schemas: WebPage, Service (with LocalBusiness provider + Speakable), FAQPage, BreadcrumbList, HowTo
8. **Dynamic sitemap** — now fetches blog post slugs from Strapi at build time (was hardcoded list)
9. **Static sitemap.xml removed** — `public/sitemap.xml` deleted, dynamic `src/app/sitemap.ts` is now the sole source

## Schema coverage after fix

| Page Type | WebPage | Service | FAQPage | BreadcrumbList | HowTo | Speakable | LocalBusiness |
|-----------|---------|---------|---------|----------------|-------|-----------|---------------|
| Service pages (9) | ✅ | ✅ | ✅ (if FAQs) | ✅ | ✅ (if steps) | ✅ | ✅ (in provider) |
| Blog posts (5) | — | — | — | — | — | — | — |
| Blog posts have | Article schema with datePublished, dateModified, author, publisher |
| Homepage | Organization JSON-LD from layout.tsx |
| Other pages | WebPage + BreadcrumbList via jsonld.ts helpers |

## What needs Strapi content updates
See `STRAPI-CONTENT-FIXES.md` — all 4 fixes were applied via API.

## Remaining for Phase 2
- Add Article JSON-LD with dateModified to blog posts
- Add Organization + LocalBusiness JSON-LD to homepage
- Consider adding SearchAction schema (old WordPress had it)
- Add og:image to all pages (requires Strapi media uploads)
