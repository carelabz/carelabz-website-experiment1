# v0 Upload Guide — CareLAbz Arc Flash Page

Everything Claude Code built is packaged and ready to upload to v0 at `v0.app`.

## What's in the bundle

**Zip file:** `v0-upload-bundle.zip` (1.2 MB) — 29 files total

```
v0-bundle/
├── src/
│   ├── app/
│   │   ├── ae/services/study-analysis/arc-flash-study/
│   │   │   └── page.tsx                     ← Main page (1216 lines, 11 sections, 5 JSON-LD)
│   │   ├── layout.tsx                       ← Root layout with fonts + skip link
│   │   └── globals.css                      ← Tailwind v3 base styles
│   ├── components/
│   │   ├── sticky-navbar.tsx                ← Sticky nav with scroll behavior
│   │   ├── faq-accordion.tsx                ← Client component FAQ
│   │   ├── mobile-nav.tsx                   ← Hamburger menu
│   │   └── JsonLd.tsx                       ← Structured data helper
│   └── lib/
│       └── strapi.ts                        ← Strapi 5 API client + TypeScript types
├── public/
│   ├── images/hero-arc-flash.jpg            ← Hero image
│   ├── images/arc-flash-report.jpg
│   ├── images/safety-assessment.jpg
│   ├── images/industries/*.jpg              ← 8 industry images
│   ├── images/insights/*.jpg                ← 3 insight cards
│   ├── images/logo/carelabs-logo.png
│   └── og/arc-flash-study.jpg               ← Open Graph image
├── tailwind.config.ts                       ← Navy/orange/offWhite colors
├── next.config.mjs                          ← 301 redirects + trailing slash
├── postcss.config.mjs
├── tsconfig.json
└── package.json                             ← Next 14.2.35, React 18, Tailwind 3.4.1, Lucide
```

## How to upload to v0

**Option A — Chat attachment (easiest)**

1. Go to `v0.app` and start a new chat
2. Click the paperclip icon
3. Attach `v0-upload-bundle.zip`
4. Paste the prompt below
5. Hit send

**Option B — Drag-and-drop individual files**

If v0 rejects the zip, drag in the most important files one at a time:
1. `src/app/ae/services/study-analysis/arc-flash-study/page.tsx` — the page you want to redesign
2. `tailwind.config.ts` — so v0 knows your color tokens
3. `src/components/sticky-navbar.tsx`, `faq-accordion.tsx`, `mobile-nav.tsx` — the custom components
4. A few reference images from `public/images/` — so v0 knows what the content looks like

**Option C — GitHub import**

If your repo `ridashabanashah-bot/carelabz_website_experiment1` is public (or you've connected GitHub to v0), just paste the repo URL and point v0 at the specific file path.

## Prompt to paste alongside the upload

Here's the prompt that matches your tech stack and design goals. Tweak the "what to change" section to describe what you want v0 to redesign:

---

**Context:** I'm attaching my existing Next.js 14 App Router + TypeScript + Tailwind CSS 3.4.1 project. The main file to redesign is `src/app/ae/services/study-analysis/arc-flash-study/page.tsx`. The page pulls content from Strapi 5 via `src/lib/strapi.ts` — do NOT change how data is fetched, only change the visual layout and JSX structure.

**Tech stack requirements (do not deviate):**

- Next.js 14 App Router, server component by default (only `'use client'` for interactivity)
- TypeScript with the existing `ServicePage` and `PageData` interfaces from the attached files
- Tailwind CSS 3.4.1 utility classes only — no inline styles, no CSS modules, no Tailwind v4 syntax (`@utility`, `@theme inline`, `@import 'tailwindcss'`). Use `@tailwind base/components/utilities`.
- Colors must come from the existing `tailwind.config.ts`: `bg-navy` (#0B1A2F), `text-orange-500` (#F97316), `bg-offWhite` (#F8FAFC), `bg-slateCard` (#1E293B). Do NOT introduce new color tokens.
- Lucide React for all icons (already installed)
- `next/image` for all images with explicit `width`/`height` or `fill` + `sizes`
- Reuse the existing components: `StickyNavbar`, `FaqAccordion`, `MobileNav`, `JsonLd` — don't rewrite them unless I ask
- Keep ALL 5 JSON-LD schemas exactly as they are (Service, FAQPage, LocalBusiness, BreadcrumbList, HowTo)
- Keep `generateMetadata` intact with the canonical URL, hreflang, Open Graph, and Twitter card settings
- Keep the `fetchStrapiSafe()` pattern and the `buildPageDataFromStrapi()` mapper

**What to change:** [REPLACE THIS SECTION with what you want redesigned — examples below]

- *"Redesign the hero section to use a full-bleed video background with the circuit pattern overlay, and make the trust badges horizontal-scrolling on mobile."*
- *"Replace the 4-column industries grid with a carousel that auto-rotates every 5 seconds, keeping the same images and alt text."*
- *"Modernize the Insights cards — add hover lift, subtle border glow in orange, and move the category tag to overlay the image instead of below it."*
- *"Keep the whole page, but add a floating sticky 'Request a Quote' button on mobile that appears after 40% scroll."*

**Constraints:**

- Keep proper heading hierarchy (one H1, then H2, then H3)
- Keep `aria-expanded`, `aria-label`, `aria-controls`, and all focus-visible outlines
- Keep the breadcrumb nav in the hero section
- Keep the visible "Last updated" time element
- Keep the bold definitional lede paragraph with ETAP/DEWA/IEEE 1584/NFPA 70E inline links
- Mobile-first responsive — test at 375px, 768px, 1024px, 1440px
- Do not bloat the bundle — no shadcn/ui library, no framer-motion unless I specifically ask

**Output:** Return only the modified files in their original paths so I can drop them back into my repo with zero edits.

---

## Quick tips for working with v0

1. **Attach a reference screenshot** of whatever design you're trying to replicate. v0 matches colors and spacing better when it has a visual.
2. **Iterate in small chunks.** Don't ask v0 to redesign the entire page in one shot — redesign one section at a time (hero first, then insights, then industries). You'll get cleaner results.
3. **If v0 switches you to Tailwind v4 syntax**, reject the change and tell it explicitly: *"Use Tailwind 3.4.1 syntax only — no `@theme inline`, no `@utility`, no `@import 'tailwindcss'`, use `@tailwind base/components/utilities` directives."*
4. **If v0 adds shadcn/ui components you don't want**, tell it: *"Do not use shadcn/ui — use plain HTML elements styled with Tailwind utility classes."*
5. **When v0 gives you the final version**, paste it back here and I'll help you diff it against your current page and merge only the parts you want.
