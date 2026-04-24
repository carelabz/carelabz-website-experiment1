# Content Migration Audit — CO, CL, AR, PE

**Migration date:** 2026-04-25
**Source:** `www.carelabz.com/{cc}/` WordPress sites
**Target:** Carelabs Strapi Cloud (`region={cc}` filter)
**Script:** [scripts/seed-sa-content.py](../scripts/seed-sa-content.py)

## Discovery

Each of the 4 South American WordPress sites (CO, CL, AR, PE) was found to carry **the same 10 blog articles and 5 service pages as the Brazilian source** (`data/br-content-audit.md`), only with country-name substitutions — e.g., "Brazilian Business" → "Colombian Business", "Brazil Power System" → "Colombia Power System", city lists swapped, etc. The factual content and structure are identical.

Because the source content is templated, migration was executed via parameterised rewriting from the already-authored BR templates. Each country receives:

- Country name (Colombia / Chile / Argentina / Peru)
- Adjective form (Colombian / Chilean / Argentine / Peruvian)
- Local primary electrical-safety standard (RETIE / NCh Elec. 4/2003 / AEA 90364 / RM 111-2013-MEM)
- Local secondary standard (NTC 2050 / NSEG 5 En. 71 / IRAM 2281 / CNE)
- Regulatory authority (Min. de Minas y Energía / SEC / ENRE / OSINERGMIN)
- Major cities (per country config)

## What was changed per country

Every SA country now ships:

- 10 clean blog posts with unique titles, meta, category, seoKeywords, excerpt, and ~500-word AEO-structured markdown body
- 5 service pages with the full field set: eyebrow, definitionalLede, features[], safetyBody, safetyBullets[], reportsBody, reportsBullets[], processSteps[], faqs[], trustBadges[], CTAs, metaTitle, metaDescription, seoKeywords
- HomePage.services array with 5 cards pointing to real ServicePage slugs (not the old broken `/short-circuit-analysis/`, `/load-flow-analysis/`, `/relay-coordination-study/` URLs)

### Summary table

| Country | WP artifacts deleted | Bare-slug duplicates deleted | Blog posts updated | Service pages updated | HomePage fixed |
|---|---|---|---|---|---|
| CO Colombia | 4 | 5 | 10 | 5 | ✓ |
| CL Chile | 4 | 7 | 10 | 5 | ✓ |
| AR Argentina | 4 | 5 | 10 | 5 | ✓ |
| PE Peru | 4 | 5 | 10 | 5 | ✓ |
| **Totals** | **16** | **22** | **40** | **20** | **4** |

## Shape of each country's clean state

Post-migration, each country has:

**9 clean `-{cc}`-suffixed blog posts** with clean titles (no `| Carelabs` suffix), proper meta, clean excerpts (no `[...]` markers), and full markdown bodies. The 10th article (`examine-and-confirm-electrical-motor-performance-in-compliance-with-{adj}-regulations-{cc}`) gets new content about IEEE 112 / IEC 60034 motor compliance testing — this article was missing from BR and was authored fresh.

**5 service pages** with unique titles. Previously all 5 services per country carried the same dupe title "Arc Flash Analysis That Goes The Extra Mile" — same bug as BR had. All fixed and populated with real content.

**HomePage.services** pointing to the 5 real service slugs. Previously 3 of 5 cards pointed to non-existent slugs (same bug as BR: `/short-circuit-analysis/`, `/load-flow-analysis/`, `/relay-coordination-study/`). All fixed.

## WordPress content audit artefacts

Because the WP content was templated and identical in structure to BR's, per-country content audit markdowns were not generated. The authoritative source content lives in [data/br-content-audit.md](br-content-audit.md). Per-country deviations are handled by the templating system in `scripts/seed-sa-content.py`.

## Reproducibility

To regenerate the content for any country, run:

```bash
python scripts/seed-sa-content.py co     # single country
python scripts/seed-sa-content.py        # all 4
```

The script is idempotent — re-running it will re-PUT the same content (safe for editorial updates).

## Gaps flagged

- **Meta descriptions** on the live WordPress source are not set for any page — no prose was inherited. Carelabs' Strapi now fills these slots with authored copy that matches the brand voice.
- **Author / publishedDate** fields on blog posts are still empty in Strapi — the WP source does not expose these. Fill via Strapi admin if editorial attribution is required.
- **Hero images** for blog posts are empty in Strapi — WP source uses lazy-loaded placeholders. Upload via Strapi admin as needed.
- **Contact page** copy on CO/CL/AR/PE — the WP contact pages use a US placeholder phone (`+1 555 802 1083`) and do not list a country office. Carelabs' `countries-config.ts` uses the correct per-country placeholders (`+52 (55) 0000-0000` pattern). Flag for editorial review.

## Next passes

- Upload hero images to Strapi per blog post and service page
- Author real `author` and `publishedDate` fields per post
- Swap generic city lists for actual office addresses once available
- Consider creating `/case-studies/` entries in Strapi (currently the page is a placeholder on all 5 SA countries)
